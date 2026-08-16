#!/usr/bin/env bash
# SpecAssay Check (Gate 2) — portable traceability check + trace-manifest.json matrix emitter.
# The check is the assay: it hallmarks the Golden Thread from intent to build to proof.
# Exact-set registry ≡ specs ≡ tasks. Silent AC gaps and untraced scope fail.
# Tracked debt is allowed. US/FR/NFR without own carrier are backlog (planning altitude) — not silent-gap candidates.
# Anointed backlog: a registry ID whose only carrier is an open Carries TODO is backlog, not drift — minting into
# backlog is deliberate (the TODO proves intent); unclaimed IDs with no TODO still fail exact-set.
# Always writes trace-manifest.json (even on failure) so the manifest reflects GAPs + gate.
set -euo pipefail

export LC_ALL=C

EXT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="${SPECASSAY_PROJECT_ROOT:-}"
if [[ -z "$PROJECT_ROOT" ]]; then
  # Spec Kit install: <project>/.specify/extensions/<ext>/ → three levels up.
  # SpecAssay repo layout: <specassay>/extensions/<ext>/ → two levels up.
  parent_dir="$(basename "$(dirname "$EXT_DIR")")"
  grandparent_dir="$(basename "$(dirname "$(dirname "$EXT_DIR")")")"
  if [[ "$parent_dir" == "extensions" && "$grandparent_dir" == ".specify" ]]; then
    PROJECT_ROOT="$(cd "$EXT_DIR/../../.." && pwd)"
  else
    PROJECT_ROOT="$(cd "$EXT_DIR/../.." && pwd)"
  fi
fi
cd "$PROJECT_ROOT"

CONFIG="${SPECASSAY_CONFIG:-$EXT_DIR/specassay-check-config.yml}"
if [[ ! -f "$CONFIG" ]]; then
  if [[ -f "$EXT_DIR/config-template.yml" ]]; then
    CONFIG="$EXT_DIR/config-template.yml"
    echo "WARN: using config-template.yml; copy to specassay-check-config.yml for real projects" >&2
  else
    echo "FAIL: no specassay-check-config.yml (looked in $EXT_DIR)" >&2
    exit 2
  fi
fi

yaml_scalar() {
  local key="$1"
  awk -v k="$key" '
    $0 ~ "^"k":[[:space:]]*" {
      sub("^[^:]+:[[:space:]]*", "")
      gsub(/^"/, ""); gsub(/"$/, "")
      print
      exit
    }
  ' "$CONFIG"
}

yaml_list() {
  local key="$1"
  awk -v k="$key" '
    $0 ~ "^"k":[[:space:]]*$" { inlist=1; next }
    inlist && /^[^[:space:]-]/ { exit }
    inlist && /^[[:space:]]*-[[:space:]]*/ {
      sub(/^[[:space:]]*-[[:space:]]*/, "")
      gsub(/^"/, ""); gsub(/"$/, "")
      print
    }
  ' "$CONFIG"
}

REGISTRY="$(yaml_scalar registry)"
SPECS_GLOB="$(yaml_scalar specs)"
TASKS_GLOB="$(yaml_scalar tasks)"
ID_RE="$(yaml_scalar id_regex)"
COVERS_RE="$(yaml_scalar covers_regex)"
CARRIES_RE="$(yaml_scalar carries_regex)"
TEST_AC_RE="$(yaml_scalar test_ac_regex)"
MANIFEST_OUT="$(yaml_scalar manifest_path)"
TARGET_NAME="$(yaml_scalar target_name)"

[[ -n "$REGISTRY" ]] || { echo "FAIL: config missing registry" >&2; exit 2; }
[[ -n "$ID_RE" ]] || ID_RE='(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?'
[[ -n "$COVERS_RE" ]] || COVERS_RE='@covers[[:space:]]+.*'
# The task-side mark. Accept both **Carries**: (new) and **Traces**: (pre-rename) during transition.
[[ -n "$CARRIES_RE" ]] || CARRIES_RE='\*\*(Carries|Traces)\*\*:'
[[ -n "$TEST_AC_RE" ]] || TEST_AC_RE='AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?'
[[ -n "$SPECS_GLOB" ]] || SPECS_GLOB='specs/**/spec.md'
[[ -n "$TASKS_GLOB" ]] || TASKS_GLOB='specs/**/tasks.md'
[[ -n "$MANIFEST_OUT" ]] || MANIFEST_OUT='trace-manifest.json'
[[ -n "$TARGET_NAME" ]] || TARGET_NAME="$(basename "$PROJECT_ROOT")"

fail=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
: > "$tmp/failures.jsonl"

# kind | id-or-empty | detail — collected for trace-manifest.json gate.failures
record_fail() {
  local kind="$1"
  local id="${2:-}"
  local detail="$3"
  echo "FAIL: $detail" >&2
  fail=1
  python3 -c '
import json,sys
kind, id_, detail = sys.argv[1], sys.argv[2], sys.argv[3]
row = {"kind": kind, "detail": detail}
if id_:
    row["id"] = id_
print(json.dumps(row, ensure_ascii=False))
' "$kind" "$id" "$detail" >> "$tmp/failures.jsonl"
}

if [[ ! -f "$REGISTRY" ]]; then
  record_fail "registry-missing" "" "registry not found: $REGISTRY"
  # Still try to emit an empty-ish manifest below if possible; exit after emit.
fi

# Registry extraction is scoped to definition-shaped lines only (shared
# with mint-id.sh's own style-detection pattern), not a blind grep over
# the whole file. A registry row's own prose can legitimately cite
# another ID (a cross-reference, a range-summary table endpoint, a
# different project's ID mentioned for context) without that citation
# being mistaken for a mint of it; the earlier blind-grep version did
# make exactly that mistake, so this scoping isn't optional.
source "$EXT_DIR/scripts/lib-def-line.sh"
DEF_LINE_RE="$(def_line_regex "$ID_RE")"
: > "$tmp/def_line_hits.txt"
if [[ -f "$REGISTRY" ]]; then
  grep -nE "$DEF_LINE_RE" "$REGISTRY" 2>/dev/null | while IFS= read -r line; do
    lineno="${line%%:*}"
    rest="${line#*:}"
    id="$(grep -Eo "$ID_RE" <<<"$rest" | head -1 || true)"
    [[ -n "$id" ]] && printf '%s|%s\n' "$id" "$lineno"
  done >> "$tmp/def_line_hits.txt" || true
fi

# registry.txt is the ground-truth ID set everything else (spec-orphan,
# task-orphan, silent-gap, the manifest's own row list) is compared
# against; it must come from the same definition-line scoping as
# duplicate-id detection below, or the two checks could disagree about
# what's actually minted.
cut -d'|' -f1 "$tmp/def_line_hits.txt" 2>/dev/null | sort -u > "$tmp/registry.txt" || : > "$tmp/registry.txt"

# Duplicate-id: two independent mints of the same ID, usually two branches
# that each computed the same "next" number before either saw the other's
# commit. registry.txt's sort -u above already erases this silently for
# exact-set purposes (presence is presence, regardless of how many lines
# produced it) -- this check exists because minting a duplicate is real
# drift that deserves a refusal, not silent same-first-line-wins in the
# manifest.
cut -d'|' -f1 "$tmp/def_line_hits.txt" 2>/dev/null | sort | uniq -d > "$tmp/dup_ids.txt" || : > "$tmp/dup_ids.txt"
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  lines="$(grep "^${id}|" "$tmp/def_line_hits.txt" | cut -d'|' -f2 | paste -sd, -)"
  record_fail "duplicate-id" "$id" "duplicate definition line(s) for $id at $REGISTRY:$lines"
done < "$tmp/dup_ids.txt"

expand_glob() {
  local pattern="$1"
  local dir base
  if [[ "$pattern" == *\*\*/* ]]; then
    dir="${pattern%%/\*\*/*}"
    base="${pattern##*/}"
    [[ -d "$dir" ]] || return 0
    find "$dir" -type f -name "$base" 2>/dev/null
  elif [[ "$pattern" == */* ]]; then
    dir="$(dirname "$pattern")"
    base="$(basename "$pattern")"
    if [[ "$base" == "**" ]]; then
      [[ -d "$dir" ]] || return 0
      find "$dir" -type f 2>/dev/null
      return 0
    fi
    [[ -d "$dir" ]] || return 0
    find "$dir" -type f -name "$base" 2>/dev/null
  else
    find . -type f -name "$pattern" 2>/dev/null
  fi
}

: > "$tmp/spec.txt"
while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  grep -Eoh "$ID_RE" "$f" | sort -u >> "$tmp/spec.txt" || true
done < <(expand_glob "$SPECS_GLOB")
sort -u "$tmp/spec.txt" -o "$tmp/spec.txt"

: > "$tmp/tasks.txt"
: > "$tmp/pending.txt"
: > "$tmp/pending_hits.txt"
while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  grep -Eoh "$ID_RE" "$f" | sort -u >> "$tmp/tasks.txt" || true
  # Open checkbox tasks that name registry IDs (usually via Carries:) — the tracked-debt tasks.
  # Excerpt is NOT truncated here: `cut -c1-N` is byte-oriented under this
  # script's own `LC_ALL=C`, so it can slice a multi-byte UTF-8 character
  # (e.g. an em dash) in half, corrupting the excerpt and crashing the
  # Python side downstream. Truncation happens in Python instead, where
  # string slicing is codepoint-safe.
  grep -nE '^- \[ \]' "$f" 2>/dev/null | while IFS= read -r line; do
    lineno="${line%%:*}"
    rest="${line#*:}"
    excerpt="$(printf '%s' "$rest" | tr '\t' ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    while IFS= read -r id; do
      [[ -n "$id" ]] || continue
      printf '%s|%s|%s|%s\n' "$f" "$lineno" "$id" "$excerpt"
    done < <(grep -Eo "$ID_RE" <<<"$rest" || true)
  done >> "$tmp/pending_hits.txt" || true
done < <(expand_glob "$TASKS_GLOB")
sort -u "$tmp/tasks.txt" -o "$tmp/tasks.txt"
cut -d'|' -f3 "$tmp/pending_hits.txt" 2>/dev/null | sort -u > "$tmp/pending.txt" || : > "$tmp/pending.txt"


# covers: path|line|id|excerpt
: > "$tmp/covers_hits.txt"
while IFS= read -r g; do
  [[ -z "$g" ]] && continue
  while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    grep -nE "$COVERS_RE" "$f" 2>/dev/null | while IFS= read -r line; do
      lineno="${line%%:*}"
      rest="${line#*:}"
      # Not truncated here -- same byte-vs-codepoint reasoning as
      # pending_hits.txt above; Python truncates this excerpt instead.
      excerpt="$(printf '%s' "$rest" | tr '\t' ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
      # One hit per ID — @covers may list several (e.g. FR-HOME-04, AC-HOME-15).
      while IFS= read -r id; do
        [[ -n "$id" ]] || continue
        printf '%s|%s|%s|%s\n' "$f" "$lineno" "$id" "$excerpt"
      done < <(grep -Eo "$ID_RE" <<<"$rest" || true)
    done
  done < <(expand_glob "$g")
done < <(yaml_list src_globs) >> "$tmp/covers_hits.txt" || true

cut -d'|' -f3 "$tmp/covers_hits.txt" 2>/dev/null | sort -u > "$tmp/covers.txt" || true

# proofs: path|line|id|name
: > "$tmp/proof_hits.txt"
while IFS= read -r g; do
  [[ -z "$g" ]] && continue
  while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    grep -nE "$TEST_AC_RE" "$f" 2>/dev/null | while IFS= read -r line; do
      lineno="${line%%:*}"
      rest="${line#*:}"
      raw="$(grep -Eo "$TEST_AC_RE" <<<"$rest" | head -1 || true)"
      [[ -n "$raw" ]] || continue
      id="$(printf '%s' "$raw" | tr '_' '-')"
      name="$(grep -Eo 'test_[A-Za-z0-9_]+|func test_[A-Za-z0-9_]+' <<<"$rest" | head -1 | sed 's/^func //' || true)"
      [[ -n "$name" ]] || name="$raw"
      printf '%s|%s|%s|%s\n' "$f" "$lineno" "$id" "$name"
    done
  done < <(expand_glob "$g")
done < <(yaml_list test_globs) >> "$tmp/proof_hits.txt" || true

cut -d'|' -f3 "$tmp/proof_hits.txt" 2>/dev/null | sort -u > "$tmp/test_acs.txt" || true

# Domains actually present in this registry (the middle TYPE-DOMAIN-NN
# segment of each real local ID). Used below to tell a genuine local
# orphan/typo apart from prose citing another project's real ID by name
# (e.g. "the AC-USER-03-class bug"): spec.md and tasks.md have no single
# canonical shape the way registry rows do, so unlike registry.txt's own
# def_line_regex fix, orphan detection here can't be scoped to a line
# shape. A citation's ID still has to parse as ID_RE-shaped, but its
# domain segment won't be one this registry has ever minted into; a real
# local typo almost always keeps the real local domain and gets the
# number (or the domain itself) wrong in a way that still matches one of
# these domains, or fails the separate unclaimed check below regardless.
cut -d'-' -f2 "$tmp/registry.txt" 2>/dev/null | sort -u > "$tmp/local_domains.txt" || : > "$tmp/local_domains.txt"
is_local_domain() {
  grep -qx "$(cut -d'-' -f2 <<<"$1")" "$tmp/local_domains.txt"
}

# 1) Exact-set drift: registry ≡ specs, registry ≡ tasks (HomesFlow Gate 2 parity).
#    Specs/tasks may not invent IDs; registry IDs may not sit unclaimed in either
#    artifact — except anointed backlog: a registry ID whose only carrier is an
#    open Carries TODO is backlog (deliberate, visible), not drift.
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  is_local_domain "$id" || continue
  record_fail "spec-orphan" "$id" "spec references ID not in registry: $id"
done < <(comm -13 "$tmp/registry.txt" "$tmp/spec.txt")

while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  # Anointed backlog: an open Carries TODO carries the claim until a spec picks
  # the ID up. Unclaimed IDs with no TODO still fail (drift / fat-finger).
  if grep -qx "$id" "$tmp/pending.txt"; then
    continue
  fi
  record_fail "spec-unclaimed" "$id" "registry ID missing from specs: $id"
done < <(comm -23 "$tmp/registry.txt" "$tmp/spec.txt")

while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  is_local_domain "$id" || continue
  record_fail "task-orphan" "$id" "tasks reference ID not in registry: $id"
done < <(comm -13 "$tmp/registry.txt" "$tmp/tasks.txt")

while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  record_fail "task-unclaimed" "$id" "registry ID missing from tasks: $id"
done < <(comm -23 "$tmp/registry.txt" "$tmp/tasks.txt")

# 2) Every task with a checkbox should carry its ID(s) via a Carries mark
while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  while IFS= read -r line; do
    if [[ "$line" =~ ^-\ \[[x\ ]\]\ T ]]; then
      if ! grep -Eq "$CARRIES_RE" <<<"$line"; then
        record_fail "missing-carries" "" "task missing Carries field: ${line:0:80}"
      fi
    fi
  done < "$f"
done < <(expand_glob "$TASKS_GLOB")

# 3) Untraced scope
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  grep -qx "$id" "$tmp/registry.txt" || record_fail "orphan-covers" "$id" "untraced scope (@covers): $id not in registry"
done < "$tmp/covers.txt"

while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  grep -qx "$id" "$tmp/registry.txt" || record_fail "orphan-test" "$id" "untraced scope (test name): $id not in registry"
done < "$tmp/test_acs.txt"

# 4) Silent gaps — ACs only (coverage altitude: AC is the atomic proof unit)
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  [[ "${id%%-*}" == "AC" ]] || continue
  if grep -qx "$id" "$tmp/test_acs.txt"; then
    continue
  fi
  if grep -qx "$id" "$tmp/pending.txt"; then
    continue
  fi
  record_fail "silent-gap" "$id" "silent gap: $id has no test and no open tracked-debt task"
done < "$tmp/registry.txt"

# --- Emit trace-manifest.json (always; the manifest should show GAPs even when Gate fails) ---
export MANIFEST_OUT REGISTRY TARGET_NAME PROJECT_ROOT
export MANIFEST_TMP="$tmp"
export MANIFEST_FAIL="$fail"
export EXT_VERSION="$(awk '/^  version:/{gsub(/"/,""); print $2; exit}' "$EXT_DIR/extension.yml" 2>/dev/null || echo 0.0.0)"
python3 - <<'PY'
import json, os, re, datetime
from pathlib import Path

tmp = Path(os.environ["MANIFEST_TMP"])
registry_path = Path(os.environ["REGISTRY"])
out_path = Path(os.environ["MANIFEST_OUT"])
target = os.environ.get("TARGET_NAME") or "project"
repo = os.environ.get("PROJECT_ROOT") or str(Path.cwd())
gate_failed = os.environ.get("MANIFEST_FAIL", "0") != "0"

ids = [ln.strip() for ln in (tmp / "registry.txt").read_text().splitlines() if ln.strip()]
pending = {ln.strip() for ln in (tmp / "pending.txt").read_text().splitlines() if ln.strip()}
tested = {ln.strip() for ln in (tmp / "test_acs.txt").read_text().splitlines() if ln.strip()}
covered = {ln.strip() for ln in (tmp / "covers.txt").read_text().splitlines() if ln.strip()}
spec_ids = {ln.strip() for ln in (tmp / "spec.txt").read_text().splitlines() if ln.strip()}

failures = []
fail_path = tmp / "failures.jsonl"
if fail_path.exists():
    for ln in fail_path.read_text().splitlines():
        if ln.strip():
            failures.append(json.loads(ln))

statements = {}
registry_refs = {}
if registry_path.is_file():
    reg_text = registry_path.read_text(encoding="utf-8", errors="replace").splitlines()
else:
    reg_text = []
try:
    registry_rel = os.path.relpath(os.path.realpath(registry_path), os.path.realpath(repo))
except ValueError:
    registry_rel = str(registry_path)

# Same definition-line scoping registry.txt itself already uses (v0.4.2):
# a blind "id_ in line" substring scan also matches inside a *longer*
# sibling ID's own prose citation, since a shorter ID can be a literal
# substring of a longer one (e.g. "FR-SPOOL-20" inside "NFR-SPOOL-20"),
# so the displayed statement/line for one ID could silently come from a
# completely different ID's bullet, or from a prose citation instead of
# a real definition. def_line_hits.txt (id|lineno, definition-shaped
# lines only) is already computed above; reuse it instead of re-deriving
# a second, disagreeing match here.
def_line_by_id = {}
def_hits_path = tmp / "def_line_hits.txt"
if def_hits_path.exists():
    for ln in def_hits_path.read_text().splitlines():
        if not ln.strip():
            continue
        parts = ln.split("|", 1)
        if len(parts) != 2:
            continue
        hid, hline = parts
        if hid not in def_line_by_id:
            try:
                def_line_by_id[hid] = int(hline)
            except ValueError:
                pass

for id_ in ids:
    statements[id_] = id_
    n = def_line_by_id.get(id_)
    if n and 1 <= n <= len(reg_text):
        s = re.sub(r"^[\s#\-*\[\]xX]+", "", reg_text[n - 1]).strip()
        statements[id_] = s or id_
        registry_refs[id_] = {"path": registry_rel, "line": n}

impl_by = {i: [] for i in ids}
covers_file = tmp / "covers_hits.txt"
if covers_file.exists():
    for ln in covers_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.strip():
            continue
        parts = ln.split("|", 3)
        if len(parts) < 3:
            continue
        path, line, id_ = parts[0], parts[1], parts[2]
        # Truncated here, not in bash: codepoint-safe, never slices a
        # multi-byte character in half the way byte-oriented `cut -c1-N`
        # could under this script's own LC_ALL=C.
        excerpt = parts[3][:160] if len(parts) > 3 else ""
        if id_ not in impl_by:
            continue
        try:
            line_n = int(line)
        except ValueError:
            line_n = 0
        impl_by[id_].append({"path": path, "line": line_n, "excerpt": excerpt})

proof_by = {i: [] for i in ids}
proofs_file = tmp / "proof_hits.txt"
if proofs_file.exists():
    for ln in proofs_file.read_text().splitlines():
        if not ln.strip():
            continue
        parts = ln.split("|", 3)
        if len(parts) < 3:
            continue
        path, line, id_ = parts[0], parts[1], parts[2]
        name = parts[3] if len(parts) > 3 else id_
        if id_ not in proof_by:
            continue
        try:
            line_n = int(line)
        except ValueError:
            line_n = 0
        proof_by[id_].append({"name": name, "path": path, "line": line_n})

debt_by = {i: [] for i in ids}
pending_hits = tmp / "pending_hits.txt"
seen_debt = set()
if pending_hits.exists():
    for ln in pending_hits.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.strip():
            continue
        parts = ln.split("|", 3)
        if len(parts) < 3:
            continue
        path, line, id_ = parts[0], parts[1], parts[2]
        # Truncated here, not in bash: same codepoint-safety reasoning
        # as covers_hits.txt above.
        excerpt = parts[3][:200] if len(parts) > 3 else ""
        if id_ not in debt_by:
            continue
        key = (path, line, id_)
        if key in seen_debt:
            continue
        seen_debt.add(key)
        try:
            line_n = int(line)
        except ValueError:
            line_n = 0
        debt_by[id_].append({"path": path, "line": line_n, "excerpt": excerpt})

def status_for(id_: str) -> str:
    typ = id_.split("-", 1)[0]
    # Open TODO splits by whether work started: spec/impl presence means debt
    # (excused incompleteness); registry entry + TODO and nothing else means
    # anointed backlog (minted on purpose, not yet picked up).
    started = id_ in spec_ids or id_ in covered
    if typ == "AC":
        if id_ in tested:
            return "proven"
        if id_ in pending:
            return "tracked-debt" if started else "backlog"
        return "GAP"
    # US/FR/NFR: planning altitude — backlog when no own carrier; not silent-gap / GAP.
    if id_ in covered or id_ in tested:
        return "proven"
    if id_ in pending:
        return "tracked-debt" if started else "backlog"
    return "backlog"

rows = []
status_counts = {"proven": 0, "tracked-debt": 0, "GAP": 0, "backlog": 0}
ac_count = 0
covered_count = 0
for id_ in ids:
    typ = id_.split("-", 1)[0]
    st = status_for(id_)
    status_counts[st] += 1
    if typ == "AC":
        ac_count += 1
        if st == "proven":
            covered_count += 1
    rows.append({
        "id": id_,
        "type": typ,
        "statement": statements.get(id_, id_),
        "registry": registry_refs.get(id_),
        "status": st,
        "implementations": impl_by.get(id_, []),
        "proofs": proof_by.get(id_, []),
        "carryingTasks": debt_by.get(id_, []),
        "attestedBy": None,
    })

doc = {
    "schemaVersion": 4,
    "format": "trace-manifest",
    "emitter": "specassay-check",
    "targetName": target,
    "repoPath": repo,
    "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    "gate": {
        "ok": not gate_failed and len(failures) == 0,
        "failures": failures,
    },
    "totals": {
        "registryIdCount": len(ids),
        "acCount": ac_count,
        "coveredCount": covered_count,
    },
    "statusCounts": status_counts,
    "rows": rows,
}

# Prefer structured failures if bash recorded any; else respect MANIFEST_FAIL.
if failures:
    doc["gate"]["ok"] = False

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

# trace-manifest v5 (beta, docs/trace-manifest-v5.md): emitted alongside v4,
# never in place of it -- the doc's own stated bar for the real Gate to
# switch its primary emit is "once the beta settles" (the first external
# emitter, clew, having pushed on the field shapes), which hasn't happened.
# This is v4's own already-known data reshaped, not new computation: tier
# from the type prefix SpecAssay already parses, origin as registry's own
# {path,line} under its new spelling. parents/rollup are left absent on
# purpose -- SpecAssay has no real per-ID parent edge today (only a domain
# grouping convention), and the v5 doc explicitly designs for that: absent
# parents falls back to domain-grouping in any v5 reader, so this stays
# honest about what the Gate actually knows rather than inventing edges.
tier_by_type = {"US": "intent", "FR": "requirement", "NFR": "requirement", "AC": "criterion"}
v5_rows = []
for row in rows:
    v5_row = dict(row)
    v5_row["tier"] = tier_by_type.get(row["type"], row["type"])
    if row.get("registry"):
        v5_row["origin"] = {"kind": "registry-line", **row["registry"]}
    v5_rows.append(v5_row)

ext_version = os.environ.get("EXT_VERSION", "0.0.0")
v5_doc = {
    "schemaVersion": 5,
    "format": "trace-manifest",
    "emitter": {"name": "specassay-check", "version": ext_version},
    "targetName": target,
    "repoPath": repo,
    "generatedAt": doc["generatedAt"],
    "gate": doc["gate"],
    "totals": doc["totals"],
    "statusCounts": doc["statusCounts"],
    "rows": v5_rows,
}
v5_path = out_path.with_name(out_path.name.replace(".json", ".v5beta.json"))
v5_path.write_text(json.dumps(v5_doc, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {v5_path.name} ({len(v5_rows)} rows, schemaVersion 5, beta)")
print(f"Wrote {out_path} ({len(rows)} rows) gate.ok={doc['gate']['ok']}", flush=True)
PY

if [[ "$fail" -ne 0 ]]; then
  echo "SpecAssay Check (Gate 2): FAILED" >&2
  exit 1
fi

echo "SpecAssay Check (Gate 2): OK ($(wc -l < "$tmp/registry.txt" | tr -d ' ') registry IDs)"
