#!/usr/bin/env python3
"""thread-report — the SpecAssay *illuminate* rung.

Diffs a base trace-manifest against a PR-head trace-manifest and buckets the
PR's changed files, then emits a Markdown **Thread Report** for a PR comment:

  0. The verdict line — the thread's state and the counts that answer "what did
     this card do": rows proved, rows moved to admitted debt, files off thread.
     Everything else is one click down, in a <details>.
  1. Intent Changed — statements of intent whose wording was restated, with the
     blast-radius re-confirm list (the build and proof written against the old
     wording). Never folded: it asks the reader to do something.
  2. What moved — the family tables, carrying both the move and the state, with
     unchanged rows footnoted rather than listed. One section, not two: the
     tables hold the state, so a bullet list saying the same thing twice is
     display, not truth.
  3. Off thread — changed files that carry no mark tying them to any intent this
     PR moved. Not a defect; a visibility call. Any human tick stays outside the
     fold, because a checkbox nobody can see is not a ceremony.
  4. Receipts — whatever the caller passes with --receipts (a gate log, a
     toolchain line). A receipt, not a headline, so it renders folded.

Doctrine: this **illuminates, never refuses**. It always exits 0 and never
blocks a merge — even when the head Gate is broken, it posts a briefing that
*explains* the break (the blocking ✗ is a separate CI step, not this tool).
"Off thread" is not machine-decidable as a defect (a refactor and a rogue
feature look identical), so it earns a briefing, not a gate. A team can
escalate the off-thread signal to a human tick via `offthread_ack` in the
SpecAssay config.

When given `--pr-url` (and ideally `--head-sha`), files and IDs render as links:
changed files point at their diff hunk in the PR; IDs point at their registry
line. Without PR context the report degrades gracefully to plain code spans.

Zero dependencies. Reads schema v3 / v4 trace-manifests.

Usage:
  thread-report.py --base base.json --head head.json \
      --changed-files changed.txt [--config specassay-check-config.yml]
      [--pr-url https://github.com/o/r/pull/1] [--head-sha SHA]
      [--offthread-ack off|record|required] [--receipts run-log.md]

  --changed-files accepts a file (one path per line) or `-` for stdin.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# @covers FR-THREAD-10, AC-THREAD-10 -- the display contract this file is held
# to: one verdict line with the counts, every moved row stated once, unmoved
# rows footnoted rather than listed, everything else inside a <details>, and two
# things that never fold -- Intent Changed, and a required human tick.

BADGE = {"proven": "🟢", "tracked-debt": "🟠", "backlog": "🔵", "GAP": "🔴"}
ACK_CHOICES = ("off", "record", "required")


def load_manifest(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"rows": [], "gate": {"ok": True}}


def rows_by_id(manifest: dict) -> dict:
    return {r["id"]: r for r in manifest.get("rows", [])}


def domain_of(id_: str) -> str:
    """US-SYNC-01 -> SYNC. The middle token groups a 'story' thread."""
    parts = id_.split("-")
    return parts[1] if len(parts) >= 3 else parts[0]


# ---- config (minimal, zero-dep reader for the few keys we need) ----

def read_config(path: str | None) -> dict:
    """Pull registry / specs / tasks globs and offthread_ack from the SpecAssay
    config. Only simple `key: "value"` lines matter here; unknown lines ignored."""
    cfg = {
        "registry": "PRD.md",
        "specs": "specs/**/spec.md",
        "tasks": "specs/**/tasks.md",
        "offthread_ack": "off",
        "intent_ack": "off",
    }
    if not path or not Path(path).is_file():
        return cfg
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(
            r'^\s*(registry|specs|tasks|offthread_ack|intent_ack)\s*:\s*["\']?([^"\'#]+?)["\']?\s*(#.*)?$',
            line,
        )
        if m:
            cfg[m.group(1)] = m.group(2).strip()
    for key in ("offthread_ack", "intent_ack"):
        if cfg[key] not in ACK_CHOICES:
            cfg[key] = "off"
    return cfg


def glob_to_regex(glob: str) -> re.Pattern:
    """Path-aware glob: ** matches across /, * within a segment, ? one char."""
    out, i, n = [], 0, len(glob)
    while i < n:
        c = glob[i]
        if glob.startswith("**", i):
            out.append(".*"); i += 2
            if i < n and glob[i] == "/":
                out.append("/?"); i += 1
        elif c == "*":
            out.append("[^/]*"); i += 1
        elif c == "?":
            out.append("[^/]"); i += 1
        else:
            out.append(re.escape(c)); i += 1
    return re.compile("^" + "".join(out) + "$")


def norm(p: str) -> str:
    return p.lstrip("./").replace("\\", "/")


def norm_ws(s: str) -> str:
    """Collapse whitespace so only substantive wording changes count as a
    restatement (a typo/reflow in whitespace alone is not a restatement)."""
    return re.sub(r"\s+", " ", s or "").strip()


def strip_id_prefix(id_: str, statement: str) -> str:
    """`AC-SYNC-02 — Disjoint field edits…` -> `Disjoint field edits…` for display."""
    return re.sub(rf"^\s*{re.escape(id_)}\s*[—–-]\s*", "", statement or "").strip()


# A "concrete token": a value a reword might change that could be objectively
# grepped for in the code — a number-with-optional-unit (5s, 200ms, 60fps, 1000,
# 3.5), a quoted string literal, or an ALL-CAPS identifier/acronym. Ordinary
# words are excluded so prose rewording doesn't false-flag.
CONCRETE_TOKEN = re.compile(
    r'"[^"]*"|\'[^\']*\'|\b\d+(?:\.\d+)?[A-Za-z%]*\b|\b[A-Z][A-Z0-9_]{2,}\b'
)


def concrete_tokens(s: str) -> set:
    return set(CONCRETE_TOKEN.findall(s or ""))


def find_token_in_file(text: str, tok: str):
    """Return (matched, line_no) if `tok` (verbatim) or its numeric core appears
    in `text`, else None. Verbatim wins; the numeric fallback catches `5s` in the
    statement landing as a bare `5` / `5.0` in code."""
    lines = text.split("\n")
    for i, ln in enumerate(lines, 1):
        if tok and tok in ln:
            return tok, i
    m = re.match(r"^(\d+(?:\.\d+)?)", tok or "")
    if m:
        pat = re.compile(r"\b" + re.escape(m.group(1)) + r"\b")
        for i, ln in enumerate(lines, 1):
            if pat.search(ln):
                return m.group(1), i
    return None


# ---- links (optional; only when PR context is supplied) ----

class Linker:
    """Builds GitHub URLs for files (PR diff hunk) and IDs (registry line).

    Diff-hunk anchors use `#diff-<sha256(repo-relative path)>`, GitHub's stable
    (if undocumented) convention. Blob links are the fully-documented fallback.
    `project_prefix` re-prepends the project dir stripped for manifest matching,
    so a project-relative path becomes repo-relative for the URL.
    """

    def __init__(self, pr_url: str, head_sha: str | None, project_prefix: str):
        m = re.match(r"(https?://[^/]+/[^/]+/[^/]+)/pull/(\d+)", pr_url.rstrip("/"))
        self.ok = bool(m)
        self.pr_url = pr_url.rstrip("/")
        self.repo_url = m.group(1) if m else ""
        self.head_sha = head_sha or "HEAD"
        self.prefix = norm(project_prefix).rstrip("/")

    def _repo_rel(self, project_rel: str) -> str:
        p = norm(project_rel)
        return f"{self.prefix}/{p}" if self.prefix else p

    def file_hunk(self, project_rel: str) -> str:
        rr = self._repo_rel(project_rel)
        digest = hashlib.sha256(rr.encode("utf-8")).hexdigest()
        return f"{self.pr_url}/files#diff-{digest}"

    def blob_line(self, project_rel: str, line: int | None) -> str:
        rr = self._repo_rel(project_rel)
        anchor = f"#L{line}" if line else ""
        return f"{self.repo_url}/blob/{self.head_sha}/{rr}{anchor}"


# ---- classification ----

def on_thread_paths(head: dict) -> set:
    """Every path the head manifest ties to an intent: coverage marks, proofs,
    and the registry file itself."""
    paths = set()
    for r in head.get("rows", []):
        for h in r.get("implementations", []):
            if h.get("path"):
                paths.add(norm(h["path"]))
        for pr in r.get("proofs", []):
            if pr.get("path"):
                paths.add(norm(pr["path"]))
        reg = r.get("registry")
        if reg and reg.get("path"):
            paths.add(norm(reg["path"]))
    return paths


def classify_changed(changed: list, head: dict, cfg: dict, project_prefix: str = "") -> tuple:
    """Split changed files into on-thread vs off-thread.

    On the thread = the file carries a mark tying it to an intent (it appears in
    the head manifest's coverage/proofs/registry) OR it is a registry / spec /
    tasks file (glob match). Everything else changed is 'off'.

    `changed` paths are repo-relative (as `git diff` gives them); manifest paths
    and config globs are relative to the *project* root. `project_prefix` (the
    project dir within the repo, e.g. "examples/example-app") bridges the two:
    files under it are matched project-relative; files outside it belong to no
    SpecAssay project here and are skipped.
    """
    on_paths = on_thread_paths(head)
    reg = norm(cfg.get("registry", ""))
    spec_re = glob_to_regex(cfg.get("specs", "specs/**/spec.md"))
    task_re = glob_to_regex(cfg.get("tasks", "specs/**/tasks.md"))
    pref = norm(project_prefix).rstrip("/")

    near, far = [], []
    for raw in changed:
        p = norm(raw)
        if not p:
            continue
        if pref:
            if p == pref:
                continue
            if p.startswith(pref + "/"):
                rel = p[len(pref) + 1:]
            else:
                continue  # outside the governed project — not this thread's concern
        else:
            rel = p
        is_on = (
            rel in on_paths
            or rel == reg
            or bool(spec_re.match(rel))
            or bool(task_re.match(rel))
        )
        # `distance` is binary today (0 on-thread / 1 far); the field is reserved
        # so a future grader (same-dir, import-adjacent, call-graph) can refine it.
        (near if is_on else far).append({"path": rel, "distance": 0 if is_on else 1})
    return near, far


# ---- what moved ----

def what_moved(base: dict, head: dict) -> dict:
    b, h = rows_by_id(base), rows_by_id(head)
    minted = [i for i in h if i not in b]
    retired = [i for i in b if i not in h]
    changes = []
    restated = []
    for id_ in h:
        if id_ not in b:
            continue
        bo, ho = b[id_], h[id_]
        # Restatement: the intent's own wording moved (whitespace-insensitive).
        bs, hs = bo.get("statement", ""), ho.get("statement", "")
        if bs and hs and norm_ws(bs) != norm_ws(hs):
            restated.append({"id": id_, "was": bs, "now": hs})
        if bo.get("status") != ho.get("status"):
            changes.append({
                "id": id_, "from": bo.get("status"), "to": ho.get("status"),
                "kind": "status",
            })
        else:
            added_proof = len(ho.get("proofs", [])) - len(bo.get("proofs", []))
            added_cover = len(ho.get("implementations", [])) - len(bo.get("implementations", []))
            if added_proof > 0 or added_cover > 0:
                changes.append({
                    "id": id_, "kind": "carrier",
                    "proofs": added_proof, "covers": added_cover,
                })
    return {"minted": minted, "retired": retired, "changes": changes, "restated": restated}


# ---- render ----

def fold(summary: str, body: list) -> list:
    """One click down. GitHub only renders Markdown inside <details> when a
    blank line separates it from the tags, so the blank lines are load-bearing."""
    while body and not body[-1].strip():
        body = body[:-1]
    return ["<details>", f"<summary>{summary}</summary>", ""] + body + ["", "</details>", ""]


def render(base: dict, head: dict, near: list, far: list, ack: str,
           link: Linker | None = None, project_root: str = "",
           intent_ack: str = "off", receipts: str = "") -> str:
    moved = what_moved(base, head)
    h = rows_by_id(head)
    gate_ok = head.get("gate", {}).get("ok", True)
    near_set = {n["path"] for n in near}
    # Rows whose move is a registry edit (minted or restated) rather than a carrier
    # change — for these, the change that moved the row lives in the registry file.
    registry_moved = set(moved["minted"]) | {r["id"] for r in moved["restated"]}
    out = []

    # What each moved row did, as one line per row. Built once and read twice:
    # by the verdict line's counts and by the family tables. A row can do more
    # than one thing (minted AND restated), so notes accumulate per ID.
    move_note: dict = {}

    def note(id_: str, text: str) -> None:
        move_note.setdefault(id_, []).append(text)

    landed: dict = {}  # status -> how many rows moved INTO it in this PR
    carrier_only = 0
    for c in moved["changes"]:
        if c["kind"] == "status":
            landed[c["to"]] = landed.get(c["to"], 0) + 1
            note(c["id"], f"`{c['from']}` → {BADGE.get(c['to'],'')} **`{c['to']}`**")
        else:
            carrier_only += 1
            got = []
            if c.get("covers", 0) > 0:
                got.append(f"+{c['covers']} `@covers`")
            if c.get("proofs", 0) > 0:
                got.append(f"+{c['proofs']} proof")
            held = h.get(c["id"], {}).get("status", "")
            note(c["id"], f"{', '.join(got)} · status held at {BADGE.get(held,'')} `{held}`")
    for i in moved["minted"]:
        st = h.get(i, {}).get("status", "backlog")
        move_note.setdefault(i, []).insert(0, f"🆕 minted ({BADGE.get(st,'')} `{st}`)")
    for r in moved["restated"]:
        note(r["id"], "✍️ restated")
    for i in moved["retired"]:
        note(i, "🪦 retired (tombstoned)")

    # Header — the name, then one line a reader can take in whole: the thread's
    # verdict and the counts that say what this card did. Everything else folds.
    out.append("## 🧵 Thread Report")
    out.append("")
    verdict = "🟢 **Golden Thread intact**" if gate_ok else "🔴 **Golden Thread broken**"
    tally = []
    if landed.get("proven"):
        tally.append(f"**{landed['proven']}** proved")
    if landed.get("tracked-debt"):
        tally.append(f"**{landed['tracked-debt']}** to admitted debt")
    if landed.get("GAP"):
        tally.append(f"**{landed['GAP']}** now GAP")
    if landed.get("backlog"):
        tally.append(f"**{landed['backlog']}** back to backlog")
    if moved["minted"]:
        tally.append(f"**{len(moved['minted'])}** minted")
    if moved["retired"]:
        tally.append(f"**{len(moved['retired'])}** retired")
    if moved["restated"]:
        tally.append(f"**{len(moved['restated'])}** restated")
    if carrier_only:
        noun = "carrier" if carrier_only == 1 else "carriers"
        tally.append(f"**{carrier_only}** {noun} added, status held")
    if not tally:
        tally.append("**no rows moved**")
    tally.append(f"**{len(far)}** files off thread" if far else "**nothing** off thread")
    out.append(" · ".join([verdict] + tally))
    out.append("")

    def fmt_id(id_: str) -> str:
        row = h.get(id_)
        reg = (row or {}).get("registry") or {}
        if link and link.ok and reg.get("path"):
            return f"[`{id_}`]({link.blob_line(reg['path'], reg.get('line'))})"
        return f"`{id_}`"

    def changed_carriers(id_: str) -> list:
        """The proof/impl files this PR changed that carry this ID — on-thread
        files, rendered inline so the reviewer can click straight to the change."""
        row = h.get(id_) or {}
        seen, hits = set(), []
        for kind, key in (("proof", "proofs"), ("covers", "implementations")):
            for c in row.get(key, []):
                p = norm(c.get("path", ""))
                if p and p in near_set and p not in seen:
                    seen.add(p)
                    hits.append((kind, p))
        return hits

    def changed_in(id_: str) -> str:
        """Where in this PR the change that moved this row lives — the carrier
        files it touched, or the registry file when the move was a mint or a
        restatement. Blank when the move came from a file carrying no mark of
        its own (a task line gaining a **Carries**, say): the table says the row
        moved, and does not invent a link it cannot stand behind."""
        hits = changed_carriers(id_)
        if hits:
            return " ".join(
                f"[`{p.rsplit('/', 1)[-1]}`]({link.file_hunk(p)})" if (link and link.ok)
                else f"`{p.rsplit('/', 1)[-1]}`"
                for _kind, p in hits
            )
        if id_ in registry_moved:
            reg = (h.get(id_) or {}).get("registry", {}).get("path")
            if reg:
                label = reg.rsplit("/", 1)[-1]
                return f"[`{label}`]({link.file_hunk(reg)})" if (link and link.ok) else f"`{label}`"
        return "—"

    # 1. Intent Changed — restated statements of intent + blast-radius re-confirm list
    if moved["restated"]:
        _carrier_cache: dict = {}

        def carrier_text(prel: str) -> str:
            if prel not in _carrier_cache:
                try:
                    base_dir = Path(project_root) if project_root else Path(".")
                    _carrier_cache[prel] = (base_dir / prel).read_text(
                        encoding="utf-8", errors="replace")
                except OSError:
                    _carrier_cache[prel] = ""
            return _carrier_cache[prel]

        def clink(p: str, ln, matched_line=None) -> str:
            target = matched_line or ln
            label = p.rsplit("/", 1)[-1] + (f":{target}" if target else "")
            return f"[`{label}`]({link.blob_line(p, target)})" if (link and link.ok) else f"`{label}`"

        # The two honest shapes of an intent PR, told apart by the carriers:
        # a discovery PR moves them in the same PR as the restatement (coherent),
        # an intent-first PR leaves them untouched (they owe a re-confirm).
        changed_set = {n["path"] for n in near} | {f["path"] for f in far}

        def updated_mark(p: str, inline: bool = False) -> str:
            if p not in changed_set:
                return ""
            label = "updated here" if inline else "◀ updated in this PR"
            body = f"[{label}]({link.file_hunk(p)})" if (link and link.ok) else label
            return f" ({body})" if inline else f" — {body}"

        out.append("### Intent Changed")
        n = len(moved["restated"])
        lead = "statement of intent was" if n == 1 else "statements of intent were"
        poss = "its" if n == 1 else "their"
        out.append(
            f"⚠️ {n} {lead} restated — {poss} wording moved under the code and tests "
            "written against the old text. Re-confirm each still satisfies the new statement."
        )
        out.append("")
        for r in moved["restated"]:
            id_ = r["id"]
            out.append(f"- **{fmt_id(id_)}** — restated")
            out.append(f"  - was: _{strip_id_prefix(id_, r['was'])}_")
            out.append(f"  - now: _{strip_id_prefix(id_, r['now'])}_")
            row = h.get(id_) or {}
            carriers = [(norm(c["path"]), c.get("line"))
                        for c in row.get("implementations", []) + row.get("proofs", [])
                        if c.get("path")]
            left = concrete_tokens(r["was"]) - concrete_tokens(r["now"])
            arrived = concrete_tokens(r["now"]) - concrete_tokens(r["was"])

            if not carriers:
                out.append("  - _no code or tests to re-confirm (backlog intent)._")
                continue

            # Look for an old concrete value still living in a carrier (Tier 1).
            hits: dict = {}
            if left:
                for (p, ln) in carriers:
                    txt = carrier_text(p)
                    for tok in sorted(left):
                        found = find_token_in_file(txt, tok) if txt else None
                        if found:
                            hits[(p, ln)] = found  # (matched, line_no)
                            break

            if hits:  # Tier 1 — pinpointed
                out.append("  - re-confirm:")
                for (p, ln) in carriers:
                    if (p, ln) in hits:
                        matched, mline = hits[(p, ln)]
                        out.append(f"    - {clink(p, ln, mline)} — ⚠ still contains the old `{matched}`{updated_mark(p)}")
                    else:
                        out.append(f"    - {clink(p, ln)}{updated_mark(p)}")
            elif left:  # Tier 2 — value changed, not found verbatim
                chg = "`" + "`, `".join(sorted(left)) + "`"
                to = (" → `" + "`, `".join(sorted(arrived)) + "`") if arrived else ""
                out.append(
                    f"  - _Value {chg}{to} changed, but not found verbatim in the "
                    "code or tests — re-confirm by reading._"
                )
                out.append("  - re-confirm: " + " · ".join(f"{clink(p, ln)}{updated_mark(p, inline=True)}" for (p, ln) in carriers))
            else:  # Tier 3 — prose / semantic, the default
                out.append(
                    "  - _Prose change — no literal value to pin down; re-confirm the "
                    "code and its test by reading them against the new wording._"
                )
                out.append("  - re-confirm: " + " · ".join(f"{clink(p, ln)}{updated_mark(p, inline=True)}" for (p, ln) in carriers))
        # Affirm rung: escalate re-confirmation to a human tick via `intent_ack`.
        if intent_ack == "record":
            out.append("")
            out.append("- [ ] **Each restated intent still holds — its code and tests re-confirmed.** _(tick to record — informational)_")
        elif intent_ack == "required":
            out.append("")
            out.append("- [ ] **Each restated intent still holds — its code and tests re-confirmed.** _(a human must tick this before merge — `intent_ack: required`)_")
        out.append("")

    # 2. What moved — the family tables. One section, not two: the table carries
    # the move AND the state, so the reader is not told the same fact twice. Only
    # rows this PR moved are listed; the rest of each family is footnoted with its
    # status counts, so the state is still there without the reading.
    type_rank = {"US": 0, "FR": 1, "NFR": 2, "AC": 3}
    moved_ids = set(move_note)
    if moved_ids:
        families: dict = {}
        for id_ in moved_ids:
            families.setdefault(domain_of(id_), []).append(id_)
        fam_count = len(families)
        row_noun = "row" if len(moved_ids) == 1 else "rows"
        fam_noun = "family" if fam_count == 1 else "families"
        body = []
        for dom in sorted(families):
            ids = sorted(families[dom], key=lambda i: (type_rank.get(i.split("-")[0], 9), i))
            body.append(f"**{dom}**")
            body.append("")
            body.append("| ID | Moved | Changed in |")
            body.append("|----|-------|------------|")
            for id_ in ids:
                body.append(
                    f"| {fmt_id(id_)} | {' · '.join(move_note[id_])} | {changed_in(id_)} |"
                )
            rest: dict = {}
            for r in head.get("rows", []):
                if domain_of(r["id"]) == dom and r["id"] not in moved_ids:
                    rest[r["status"]] = rest.get(r["status"], 0) + 1
            if rest:
                total = sum(rest.values())
                noun = "row" if total == 1 else "rows"
                breakdown = ", ".join(
                    f"{rest[st]} {BADGE.get(st,'')} {st}"
                    for st in sorted(rest, key=lambda k: (-rest[k], k))
                )
                body.append(
                    f"\n<sub>+{total} unchanged {noun} in this family, not listed: "
                    f"{breakdown}.</sub>"
                )
            body.append("")
        out.extend(fold(
            f"<b>What moved</b> — {len(moved_ids)} {row_noun} in {fam_count} {fam_noun}",
            body,
        ))

    # 3. Off thread. The list folds; the human tick does not — a checkbox nobody
    # can see is not a ceremony, and `offthread_ack: required` holds a merge on it.
    if far:
        n = len(far)
        verb = "sits" if n == 1 else "sit"
        noun = "file" if n == 1 else "files"
        pron = "it" if n == 1 else "them"
        body = [
            f"Changed, but nothing in {pron} carries a mark tying {pron} to an intent "
            "this PR moved. Not a defect (a refactor and unwanted scope look identical "
            "here); just worth a glance:",
            "",
        ]
        for f in far:
            fp = f["path"]
            body.append(f"- [`{fp}`]({link.file_hunk(fp)})" if (link and link.ok) else f"- `{fp}`")
        out.extend(fold(f"<b>Off thread</b> — {n} changed {noun} {verb} off the thread", body))
        if ack == "record":
            out.append("- [ ] **These untraced changes are incidental.** _(tick to record — informational)_")
            out.append("")
        elif ack == "required":
            out.append("- [ ] **These untraced changes are incidental.** _(a human must tick this before merge — `offthread_ack: required`)_")
            out.append("")
    else:
        out.append("_Every changed file carries a mark tying it to an intent. Nothing sits off the thread._")
        out.append("")

    # 4. Receipts — the run behind the report. A receipt, not a headline.
    if receipts.strip():
        out.extend(fold("<b>Receipts</b> — the run behind this report",
                        receipts.rstrip().split("\n")))

    out.append("---")
    ack_note = (
        "Set `offthread_ack: record|required` in the SpecAssay config to add a human tick."
        if ack == "off"
        else f"Off-thread acknowledgement: **{ack}**."
    )
    out.append(
        "<sub>Thread Report **illuminates; it does not refuse.** "
        f"\"Off thread\" is a visibility call, not a gate. {ack_note}</sub>"
    )
    return "\n".join(out).rstrip() + "\n"


def read_changed(arg: str) -> list:
    if arg == "-":
        text = sys.stdin.read()
    else:
        text = Path(arg).read_text(encoding="utf-8")
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit a Thread Report (Markdown).")
    ap.add_argument("--base", required=True, help="base-branch trace-manifest.json")
    ap.add_argument("--head", required=True, help="PR-head trace-manifest.json")
    ap.add_argument("--changed-files", required=True, help="file with one changed path per line, or - for stdin")
    ap.add_argument("--config", default=None, help="specassay-check-config.yml (registry/specs/tasks/offthread_ack)")
    ap.add_argument("--project-root", default=None,
                    help="project dir within the repo (e.g. examples/example-app); "
                         "defaults to the --config file's directory. Bridges repo-relative "
                         "changed paths to the project-relative manifest paths.")
    ap.add_argument("--pr-url", default=None,
                    help="PR URL (https://github.com/o/r/pull/N); enables file/ID links")
    ap.add_argument("--head-sha", default=None, help="head commit SHA for blob (ID) links")
    ap.add_argument("--offthread-ack", default=None, choices=ACK_CHOICES,
                    help="the affirm ceremony on the off-thread list; overrides the config key")
    ap.add_argument("--intent-ack", default=None, choices=ACK_CHOICES,
                    help="the affirm ceremony on restated intent; overrides the config key")
    ap.add_argument("--receipts", default=None,
                    help="a Markdown file whose contents render folded at the end of the "
                         "report (a gate log, a toolchain line). The report never reads or "
                         "reformats it; a receipt belongs under one click, not in the lead.")
    ap.add_argument("--out", default="-", help="write report here (default stdout)")
    args = ap.parse_args()

    base = load_manifest(args.base)
    head = load_manifest(args.head)
    cfg = read_config(args.config)
    changed = read_changed(args.changed_files)
    project_root = args.project_root
    if project_root is None and args.config:
        project_root = str(Path(args.config).parent)
    project_root = project_root or ""

    ack = args.offthread_ack if args.offthread_ack is not None else cfg.get("offthread_ack", "off")
    intent_ack = args.intent_ack if args.intent_ack is not None else cfg.get("intent_ack", "off")
    link = Linker(args.pr_url, args.head_sha, project_root) if args.pr_url else None

    receipts = ""
    if args.receipts:
        try:
            receipts = Path(args.receipts).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            # Illuminate, never refuse: a missing receipt loses the appendix, not
            # the report, and says so on stderr rather than in the reader's face.
            print(f"warning: --receipts {args.receipts}: {exc}", file=sys.stderr)
    near, far = classify_changed(changed, head, cfg, project_root)
    report = render(base, head, near, far, ack, link, project_root,
                    intent_ack=intent_ack, receipts=receipts)

    if args.out == "-":
        sys.stdout.write(report)
    else:
        Path(args.out).write_text(report, encoding="utf-8")
    return 0  # illuminate, never refuse


if __name__ == "__main__":
    raise SystemExit(main())
