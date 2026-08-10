#!/usr/bin/env python3
"""thread-report — the SpecAssay *illuminate* rung.

Diffs a base trace-manifest against a PR-head trace-manifest and buckets the
PR's changed files, then emits a Markdown **Thread Report** for a PR comment:

  1. What moved — status changes, IDs minted / retired, proofs & covers added.
  2. The thread now — per domain touched by the PR.
  3. Far from the thread — changed files that carry no mark tying them to any
     intent this PR moved. Not a defect; a visibility call.

Doctrine: this **illuminates, never refuses**. It always exits 0 and never
blocks a merge. "Far from the thread" is not machine-decidable as a defect
(a refactor and a rogue feature look identical), so it earns a briefing, not
a gate. A team can escalate the off-thread signal to a human-affirmation step
via `offthread_ack` (see the config), but that is a *human* verdict, not this
tool's.

Zero dependencies. Reads schema v3 / v4 trace-manifests.

Usage:
  thread-report.py --base base.json --head head.json \
      --changed-files changed.txt [--config specassay-check-config.yml]
      [--offthread-ack off|record|required]

  --changed-files accepts a file (one path per line) or `-` for stdin.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

BADGE = {"proven": "🟢", "tracked-debt": "🟠", "backlog": "🔵", "GAP": "🔴"}
# Rank for describing a status move as advance (⬆) or regress (⬇).
RANK = {"GAP": 0, "backlog": 1, "tracked-debt": 2, "proven": 3}


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
    """Pull registry / specs / tasks globs from the SpecAssay config. Only the
    simple `key: "value"` lines matter here; unknown lines are ignored."""
    cfg = {"registry": "PRD.md", "specs": "specs/**/spec.md", "tasks": "specs/**/tasks.md"}
    if not path or not Path(path).is_file():
        return cfg
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r'^\s*(registry|specs|tasks)\s*:\s*["\']?([^"\'#]+?)["\']?\s*(#.*)?$', line)
        if m:
            cfg[m.group(1)] = m.group(2).strip()
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


def classify_changed(changed: list, head: dict, cfg: dict) -> tuple:
    """Split changed files into on-thread vs far-from-thread.

    On the thread = the file carries a mark tying it to an intent (it appears in
    the head manifest's coverage/proofs/registry) OR it is a registry / spec /
    tasks file (glob match). Everything else changed is 'far'.
    """
    on_paths = on_thread_paths(head)
    reg = norm(cfg.get("registry", ""))
    spec_re = glob_to_regex(cfg.get("specs", "specs/**/spec.md"))
    task_re = glob_to_regex(cfg.get("tasks", "specs/**/tasks.md"))

    near, far = [], []
    for raw in changed:
        p = norm(raw)
        if not p:
            continue
        is_on = (
            p in on_paths
            or p == reg
            or bool(spec_re.match(p))
            or bool(task_re.match(p))
        )
        # `distance` is binary today (0 on-thread / 1 far); the field is reserved
        # so a future grader (same-dir, import-adjacent, call-graph) can refine it.
        (near if is_on else far).append({"path": p, "distance": 0 if is_on else 1})
    return near, far


# ---- what moved ----

def what_moved(base: dict, head: dict) -> dict:
    b, h = rows_by_id(base), rows_by_id(head)
    minted = [i for i in h if i not in b]
    retired = [i for i in b if i not in h]
    changes = []
    for id_ in h:
        if id_ not in b:
            continue
        bo, ho = b[id_], h[id_]
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
    return {"minted": minted, "retired": retired, "changes": changes}


# ---- render ----

def arrow(frm: str, to: str) -> str:
    if RANK.get(to, 0) > RANK.get(frm, 0):
        return "⬆"
    if RANK.get(to, 0) < RANK.get(frm, 0):
        return "⬇"
    return ""


def render(base: dict, head: dict, near: list, far: list, ack: str) -> str:
    moved = what_moved(base, head)
    h = rows_by_id(head)
    gate_ok = head.get("gate", {}).get("ok", True)
    out = []
    out.append("## 🧵 SpecAssay Thread Report")
    out.append("")
    gate_line = "✅ Golden Thread intact" if gate_ok else "🔴 Golden Thread broken — the Gate refuses"
    status_changes = [c for c in moved["changes"] if c["kind"] == "status"]
    proven_up = sum(1 for c in status_changes if c.get("to") == "proven")
    other_moves = len(status_changes) - proven_up
    carriers = sum(1 for c in moved["changes"] if c["kind"] == "carrier")
    bits = []
    if proven_up:
        bits.append(f"+{proven_up} proven")
    if other_moves:
        bits.append(f"{other_moves} moved")
    if carriers:
        bits.append(f"{carriers} carrier{'s' if carriers != 1 else ''} added")
    if moved["minted"]:
        bits.append(f"{len(moved['minted'])} minted")
    if moved["retired"]:
        bits.append(f"{len(moved['retired'])} retired")
    summary = " · ".join(bits) if bits else "no thread changes"
    out.append(f"**Gate:** {gate_line}  ·  **This PR:** {summary}")
    out.append("")

    # 1. What moved
    out.append("### What moved")
    lines = []
    for c in moved["changes"]:
        if c["kind"] == "status":
            a = arrow(c["from"], c["to"])
            lines.append(
                f"- {BADGE.get(c['to'],'')} **{c['id']}** — `{c['from']}` → **`{c['to']}`** {a}".rstrip()
            )
        else:
            got = []
            if c.get("covers", 0) > 0:
                got.append(f"+{c['covers']} `@covers`")
            if c.get("proofs", 0) > 0:
                got.append(f"+{c['proofs']} proof")
            lines.append(f"- **{c['id']}** — carrier added ({', '.join(got)}), status held")
    for i in moved["minted"]:
        st = h.get(i, {}).get("status", "backlog")
        lines.append(f"- 🆕 **{i}** — minted ({st})")
    for i in moved["retired"]:
        lines.append(f"- 🪦 **{i}** — retired (tombstoned)")
    out.append("\n".join(lines) if lines else "_Nothing on the thread changed in this PR._")
    out.append("")

    # 2. The thread now, per domain the PR touched
    touched = sorted({domain_of(c["id"]) for c in moved["changes"]}
                     | {domain_of(i) for i in moved["minted"]})
    if touched:
        out.append("### The thread now")
        moved_ids = {c["id"] for c in moved["changes"]} | set(moved["minted"])
        for dom in touched:
            fam = [r for r in head.get("rows", []) if domain_of(r["id"]) == dom]
            # Top-down thread order: story -> feature -> non-functional -> criterion.
            type_rank = {"US": 0, "FR": 1, "NFR": 2, "AC": 3}
            fam.sort(key=lambda r: (type_rank.get(r["id"].split("-")[0], 9), r["id"]))
            out.append(f"**{dom}**")
            out.append("")
            out.append("| ID | Status | |")
            out.append("|----|--------|--|")
            for r in fam:
                mark = "◀ changed" if r["id"] in moved_ids else ""
                out.append(f"| `{r['id']}` | {BADGE.get(r['status'],'')} {r['status']} | {mark} |")
            out.append("")

    # 3. Far from the thread
    out.append("### Far from the thread")
    if far:
        out.append(
            f"{len(far)} changed file(s) sit **far from the thread** — they changed, "
            "but nothing in them carries a mark tying it to an intent this PR moved. "
            "Not a defect (a refactor and unwanted scope look identical here); just worth a glance:"
        )
        out.append("")
        for f in far:
            out.append(f"- `{f['path']}`")
        out.append("")
        if ack == "record":
            out.append("> ☐ **These untraced changes are incidental.** _(tick to record — informational)_")
        elif ack == "required":
            out.append("> ☐ **These untraced changes are incidental.** _(a human must tick this before merge — `offthread_ack: required`)_")
    else:
        out.append("_Every changed file carries a mark tying it to an intent. Nothing sits far from the thread._")
    out.append("")

    out.append("---")
    out.append(
        "<sub>SpecAssay **illuminates; it does not refuse.** "
        "\"Far from the thread\" is a visibility call, not a gate. "
        "Tune the signal with `offthread_list` / `offthread_ack`.</sub>"
    )
    return "\n".join(out).rstrip() + "\n"


def read_changed(arg: str) -> list:
    if arg == "-":
        text = sys.stdin.read()
    else:
        text = Path(arg).read_text(encoding="utf-8")
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit a SpecAssay Thread Report (Markdown).")
    ap.add_argument("--base", required=True, help="base-branch trace-manifest.json")
    ap.add_argument("--head", required=True, help="PR-head trace-manifest.json")
    ap.add_argument("--changed-files", required=True, help="file with one changed path per line, or - for stdin")
    ap.add_argument("--config", default=None, help="specassay-check-config.yml (for registry/specs/tasks globs)")
    ap.add_argument("--offthread-ack", default="off", choices=["off", "record", "required"],
                    help="the affirm ceremony on the off-thread list (default off = pure illuminate)")
    ap.add_argument("--out", default="-", help="write report here (default stdout)")
    args = ap.parse_args()

    base = load_manifest(args.base)
    head = load_manifest(args.head)
    cfg = read_config(args.config)
    changed = read_changed(args.changed_files)
    near, far = classify_changed(changed, head, cfg)
    report = render(base, head, near, far, args.offthread_ack)

    if args.out == "-":
        sys.stdout.write(report)
    else:
        Path(args.out).write_text(report, encoding="utf-8")
    return 0  # illuminate, never refuse


if __name__ == "__main__":
    raise SystemExit(main())
