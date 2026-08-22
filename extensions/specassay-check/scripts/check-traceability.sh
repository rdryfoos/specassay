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

# @covers FR-GATE-10, AC-GATE-10a -- --matrix is a portfolio-snapshot
# renderer, not a second scan: it rides the SAME run that already computed
# rows/status, then additionally re-presents that data as coverage.md +
# coverage.svg. No other flags exist yet.
MATRIX_MODE=0
for arg in "$@"; do
  case "$arg" in
    --matrix) MATRIX_MODE=1 ;;
    *)
      echo "FAIL: unknown argument: $arg" >&2
      echo "  Recognized: --matrix" >&2
      exit 2
      ;;
  esac
done

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

# @covers FR-GATE-70, AC-GATE-70a, AC-GATE-70b, AC-GATE-70c -- a list-type
# key present but malformed (inline array) or bare (no items) used to
# parse to an empty list with zero signal: exactly the silent-gap shape
# this tool exists to refuse in adopters' own work, never checked for in
# its own config. Fires before any scanning -- a manifest built on a
# misread config would carry confident wrong claims, worse than no
# manifest at all -- so this refuses and exits without writing one.
validate_list_key() {
  local key="$1"
  local present well_formed lineno rawline
  present="$(grep -nE "^${key}:" "$CONFIG" 2>/dev/null | head -1 || true)"
  [[ -n "$present" ]] || return 0   # absent entirely -- means "none"

  well_formed="$(grep -nE "^${key}:[[:space:]]*\$" "$CONFIG" 2>/dev/null | head -1 || true)"
  if [[ -z "$well_formed" ]]; then
    lineno="${present%%:*}"
    rawline="$(sed -n "${lineno}p" "$CONFIG")"
    {
      echo "FAIL: config key '$key' is present but didn't parse to any entries."
      echo "  Offending line ($CONFIG:$lineno):"
      echo "    $rawline"
      echo "  Only block-style lists are read here, never inline arrays:"
      echo "    $key:"
      echo "      - \"example/**\""
      echo "  See docs/troubleshooting.md -> \"The Gate finds no sources or tests at all\""
      echo "  (https://github.com/rdryfoos/specassay/blob/main/docs/troubleshooting.md)"
    } >&2
    exit 2
  fi

  if [[ -z "$(yaml_list "$key")" ]]; then
    lineno="${well_formed%%:*}"
    {
      echo "FAIL: config key '$key' is present but has no items under it."
      echo "  ($CONFIG:$lineno)"
      echo "  To mean \"none\", omit the key entirely. To list globs:"
      echo "    $key:"
      echo "      - \"example/**\""
      echo "  See docs/troubleshooting.md -> \"The Gate finds no sources or tests at all\""
      echo "  (https://github.com/rdryfoos/specassay/blob/main/docs/troubleshooting.md)"
    } >&2
    exit 2
  fi
}

# @covers FR-GATE-30, AC-GATE-30c -- there is no settable status field; "retired"
# derives entirely from this record, so a malformed one is unreadable in
# the same sense a malformed src_globs/test_globs key is (FR-GATE-70):
# refuses loudly before any scanning rather than emitting a manifest built
# on a guess. Shape: **Retires**: <id-list> (<YYYY-MM-DD>): <reason>.
validate_retires_format() {
  local f
  while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    while IFS= read -r line; do
      [[ -n "$line" ]] || continue
      local lineno="${line%%:*}"
      local rest="${line#*:}"
      local after
      after="$(sed -E "s/^.*${RETIRES_RE}[[:space:]]*//" <<<"$rest")"
      if [[ -z "$(grep -Eo "$ID_RE" <<<"${after%%(*}" || true)" ]]; then
        {
          echo "FAIL: malformed **Retires** record ($f:$lineno) -- names no registry ID before the dated reason."
          echo "  Got: $after"
          echo "  Expected shape: **Retires**: AC-EXAMPLE-01 (2026-08-18): reason."
        } >&2
        exit 2
      fi
      if ! grep -qE '\([0-9]{4}-[0-9]{2}-[0-9]{2}\):[[:space:]]*.+' <<<"$after"; then
        {
          echo "FAIL: malformed **Retires** record ($f:$lineno) -- no \"(YYYY-MM-DD): reason\" after the ID list."
          echo "  Got: $after"
          echo "  Expected shape: **Retires**: AC-EXAMPLE-01 (2026-08-18): reason."
        } >&2
        exit 2
      fi
    done < <(grep -nE "$RETIRES_RE" "$f" 2>/dev/null || true)
  done < <(expand_glob "$TASKS_GLOB")
}

REGISTRY="$(yaml_scalar registry)"
SPECS_GLOB="$(yaml_scalar specs)"
TASKS_GLOB="$(yaml_scalar tasks)"
ID_RE="$(yaml_scalar id_regex)"
COVERS_RE="$(yaml_scalar covers_regex)"
CARRIES_RE="$(yaml_scalar carries_regex)"
RETIRES_RE="$(yaml_scalar retires_regex)"
TEST_AC_RE="$(yaml_scalar test_ac_regex)"
MANIFEST_OUT="$(yaml_scalar manifest_path)"
TARGET_NAME="$(yaml_scalar target_name)"
BLOCK_UNCOVERED_PROOF="$(yaml_scalar block_uncovered_proof)"
TEST_RESULTS="$(yaml_scalar test_results)"
MATRIX_MD="$(yaml_scalar matrix_md)"
MATRIX_SVG="$(yaml_scalar matrix_svg)"

[[ -n "$REGISTRY" ]] || { echo "FAIL: config missing registry" >&2; exit 2; }
[[ -n "$ID_RE" ]] || ID_RE='(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?'
[[ -n "$COVERS_RE" ]] || COVERS_RE='@covers[[:space:]]+.*'
# The task-side mark. Accept both **Carries**: (new) and **Traces**: (pre-rename) during transition.
[[ -n "$CARRIES_RE" ]] || CARRIES_RE='\*\*(Carries|Traces)\*\*:'
# FR-GATE-30 -- parallel to Carries: an explicit, dated, reasoned retirement
# record on an open task, naming the withdrawn ID(s). There is no settable
# status field; "retired" derives from this record alone.
[[ -n "$RETIRES_RE" ]] || RETIRES_RE='\*\*Retires\*\*:'
[[ -n "$TEST_AC_RE" ]] || TEST_AC_RE='AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?'
[[ -n "$SPECS_GLOB" ]] || SPECS_GLOB='specs/**/spec.md'
[[ -n "$TASKS_GLOB" ]] || TASKS_GLOB='specs/**/tasks.md'
[[ -n "$MANIFEST_OUT" ]] || MANIFEST_OUT='trace-manifest.json'
[[ -n "$MATRIX_MD" ]] || MATRIX_MD='coverage.md'
[[ -n "$MATRIX_SVG" ]] || MATRIX_SVG='coverage.svg'
[[ -n "$TARGET_NAME" ]] || TARGET_NAME="$(basename "$PROJECT_ROOT")"

# Every yaml_list() consumer, present and future: not a special case for
# the one that bit us.
validate_list_key "src_globs"
validate_list_key "test_globs"

fail=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
: > "$tmp/failures.jsonl"
: > "$tmp/diagnostics.jsonl"

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

# kind | id-or-empty | detail — collected for trace-manifest.json gate.diagnostics.
# Report-only: unlike record_fail, never sets $fail and never affects gate.ok.
# A named, visible finding that hasn't (yet) been ruled blocking or diagnostic
# (Rule 4a, PROMOTION-CONTRACT.md): the finding is real either way, so it is
# always emitted; only the pass/fail consequence is undecided.
record_diagnostic() {
  local kind="$1"
  local id="${2:-}"
  local detail="$3"
  echo "DIAGNOSTIC: $detail" >&2
  python3 -c '
import json,sys
kind, id_, detail = sys.argv[1], sys.argv[2], sys.argv[3]
row = {"kind": kind, "detail": detail}
if id_:
    row["id"] = id_
print(json.dumps(row, ensure_ascii=False))
' "$kind" "$id" "$detail" >> "$tmp/diagnostics.jsonl"
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

# Needs expand_glob, just defined above; also before any TASKS_GLOB scanning
# below so a malformed record refuses before anything is built from it.
validate_retires_format

# @covers FR-GATE-40, AC-GATE-40, AC-GATE-41 — a mark inside a markdown fenced code block (three
# backticks or three tildes, indented fences included) or an inline
# single-backtick code span is a quotation, not a live mark -- distinguishing
# use from mention the way is_local_domain() already does for spec/task
# orphan checks, but for the case that scoping can't reach: a project's own
# real, local ID quoted as a teaching example (docs/**'s own future use once
# FR-DOCS-50 restores it to src_globs). Blanks matched spans instead of
# deleting lines, so line numbers reported downstream still match the
# original file.
strip_code_spans() {
  awk '
    BEGIN { in_fence = 0 }
    {
      line = $0
      if (line ~ /^[[:space:]]*(```|~~~)/) { in_fence = !in_fence; print ""; next }
      if (in_fence) { print ""; next }
      out = ""; rest = line
      while (match(rest, /`[^`]*`/)) {
        out = out substr(rest, 1, RSTART - 1)
        rest = substr(rest, RSTART + RLENGTH)
      }
      print out rest
    }
  ' "$1" 2>/dev/null
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

# retires: path|line|id|rest (rest = "<id-list> (<date>): <reason>", already
# validated well-formed above). FR-GATE-30 -- one hit per ID, same pattern
# as covers/proof hits below (a Retires line may name several IDs).
: > "$tmp/retires_hits.txt"
while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  grep -nE "$RETIRES_RE" "$f" 2>/dev/null | while IFS= read -r line; do
    lineno="${line%%:*}"
    rest="${line#*:}"
    after="$(sed -E "s/^.*${RETIRES_RE}[[:space:]]*//" <<<"$rest")"
    while IFS= read -r id; do
      [[ -n "$id" ]] || continue
      printf '%s|%s|%s|%s\n' "$f" "$lineno" "$id" "$after"
    done < <(grep -Eo "$ID_RE" <<<"${after%%(*}" || true)
  done
done < <(expand_glob "$TASKS_GLOB") >> "$tmp/retires_hits.txt" || true
cut -d'|' -f3 "$tmp/retires_hits.txt" 2>/dev/null | sort -u > "$tmp/retired.txt" || : > "$tmp/retired.txt"


# covers: path|line|id|excerpt
: > "$tmp/covers_hits.txt"
while IFS= read -r g; do
  [[ -z "$g" ]] && continue
  while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    strip_code_spans "$f" | grep -nE "$COVERS_RE" 2>/dev/null | while IFS= read -r line; do
      lineno="${line%%:*}"
      rest="${line#*:}"
      # Not truncated here -- same byte-vs-codepoint reasoning as
      # pending_hits.txt above; Python truncates this excerpt instead.
      excerpt="$(printf '%s' "$rest" | tr '\t' ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
      # One hit per ID — a coverage mark may list several (e.g. FR-HOME-04, AC-HOME-15).
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
    strip_code_spans "$f" | grep -nE "$TEST_AC_RE" 2>/dev/null | while IFS= read -r line; do
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

# Rule 6a: "proven" derives from a passing proof, not a matching name.
# A test_ac_regex match in a source file only shows a test *claims* to
# answer for an ID; it says nothing about whether that test currently
# passes, or whether it is a stub, a skip, or dead code a grep still
# sees. If test_results (a JUnit XML report the project's own test run
# already produces -- pytest --junit-xml, node:test's junit reporter,
# vitest's junit reporter, all already emit this format) is configured,
# rewrite test_acs.txt in place to keep only IDs with at least one
# *passing* testcase, so every downstream consumer (the silent-gap
# check below, uncovered-proof, and status_for()'s own "tested" set)
# inherits the execution-verified meaning for free, from one place.
: > "$tmp/execution_verified.txt"
if [[ -n "$TEST_RESULTS" && -f "$TEST_RESULTS" ]]; then
  echo "true" > "$tmp/execution_verified.txt"
  python3 - "$TEST_RESULTS" "$tmp/proof_hits.txt" "$tmp/test_acs.txt" <<'PY'
import re
import sys
import xml.etree.ElementTree as ET

results_path, proof_hits_path, test_acs_path = sys.argv[1:4]

tree = ET.parse(results_path)
passing_names = []
for testcase in tree.getroot().iter("testcase"):
    failed = testcase.find("failure") is not None or testcase.find("error") is not None
    skipped = testcase.find("skipped") is not None
    if failed or skipped:
        continue
    label = f'{testcase.get("classname", "")} {testcase.get("name", "")}'
    passing_names.append(label)

def id_forms(id_):
    # AC-BIND-10 (as it appears in JS description-string test names) and
    # AC_BIND_10 (as it appears in Python test_AC_BIND_10_... function
    # names) are the two conventions this project family actually uses.
    return {id_, id_.replace("-", "_")}

verified = set()
with open(proof_hits_path, encoding="utf-8", errors="replace") as f:
    for line in f:
        parts = line.rstrip("\n").split("|", 3)
        if len(parts) < 3:
            continue
        id_ = parts[2]
        if id_ in verified:
            continue
        forms = id_forms(id_)
        if any(any(form in label for form in forms) for label in passing_names):
            verified.add(id_)

with open(test_acs_path, "w") as f:
    for id_ in sorted(verified):
        f.write(id_ + "\n")
PY
elif [[ -n "$TEST_RESULTS" ]]; then
  echo "WARN: test_results configured ($TEST_RESULTS) but the file does not exist; falling back to name-matching only, executionVerified=false in the manifest" >&2
fi

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
# -- or, FR-GATE-30, a Retires record, which is its own claim over the IDs
# it names and needs no separate Carries line alongside it.
while IFS= read -r f; do
  [[ -f "$f" ]] || continue
  while IFS= read -r line; do
    if [[ "$line" =~ ^-\ \[[x\ ]\]\ T ]]; then
      if ! grep -Eq "$CARRIES_RE" <<<"$line" && ! grep -Eq "$RETIRES_RE" <<<"$line"; then
        record_fail "missing-carries" "" "task missing Carries field: ${line:0:80}"
      fi
    fi
  done < "$f"
done < <(expand_glob "$TASKS_GLOB")

# 3) Untraced scope. Domain-scoped like spec-orphan/task-orphan (FR-GATE-40):
# a citation of another project's real ID (a domain this registry never
# minted into) isn't local drift, the same reasoning is_local_domain()
# already applies above; only registry absence *and* a locally-shaped
# domain together mean a real orphan.
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  grep -qx "$id" "$tmp/registry.txt" && continue
  is_local_domain "$id" || continue
  record_fail "orphan-covers" "$id" "untraced scope (@covers): $id not in registry"
done < "$tmp/covers.txt"

while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  grep -qx "$id" "$tmp/registry.txt" && continue
  is_local_domain "$id" || continue
  record_fail "orphan-test" "$id" "untraced scope (test name): $id not in registry"
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
  # FR-GATE-30: a retired AC is withdrawn, not a silent gap -- its own
  # terminal state, checked ahead of the ordinary proof/debt logic.
  if grep -qx "$id" "$tmp/retired.txt" 2>/dev/null; then
    continue
  fi
  record_fail "silent-gap" "$id" "silent gap: $id has no test and no open tracked-debt task"
done < "$tmp/registry.txt"

# 5) Uncovered proof (Rule 4a). The mirror of orphan-covers (3, above):
# that check catches an @covers claim naming an ID that isn't real; this
# catches the reverse, an ID with a real, passing proof that no file's
# own @covers line claims at all. Both directions are Rule 4's own text
# ("source that serves an intent carries an @covers mark"); only the
# forward direction was ever gated before v0.4.7. Any type, not only AC:
# status_for() grants "proven" via tested OR covered for US/FR/NFR too, so
# the same silent asymmetry applies there as well.
#
# Report-only by default (record_diagnostic, never affects gate.ok): the
# finding needed to exist and be measured across real projects before
# anyone could responsibly decide whether it blocks (2026-08-17 survey,
# dryfoos-sites/docs/field-notes/2026-08-17-uncovered-proof.md). A project
# opts into blocking explicitly, once its own backlog is clear, via
# block_uncovered_proof: true in its own specassay-check-config.yml --
# a dated line in that project's own config (or constitution, if the
# project mirrors this into its own paste-ready article) is the record
# of *when* and *why* that project's enforcement status changed, so the
# flip itself stays traceable, not a silent behavior change on upgrade.
uncovered_kind="uncovered-proof"
uncovered_recorder="record_diagnostic"
if [[ "$BLOCK_UNCOVERED_PROOF" == "true" ]]; then
  uncovered_recorder="record_fail"
fi
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  "$uncovered_recorder" "$uncovered_kind" "$id" "uncovered proof: $id has a passing test but no file's @covers line names it"
done < <(comm -23 "$tmp/test_acs.txt" "$tmp/covers.txt")

# --- Emit trace-manifest.json (always; the manifest should show GAPs even when Gate fails) ---
export MANIFEST_OUT REGISTRY TARGET_NAME PROJECT_ROOT MATRIX_MODE MATRIX_MD MATRIX_SVG
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

# @covers FR-GATE-30, AC-GATE-30a -- retired derives from this record alone,
# never a settable status field. Shape validated in bash before any
# scanning ran (validate_retires_format); "<id-list>(<date>): <reason>" is
# trusted here.
retired_by = {}
retires_file = tmp / "retires_hits.txt"
if retires_file.exists():
    retire_re = re.compile(r"\((\d{4}-\d{2}-\d{2})\):\s*(.+)$")
    for ln in retires_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if not ln.strip():
            continue
        parts = ln.split("|", 3)
        if len(parts) < 4:
            continue
        path, line, id_, rest = parts
        if id_ in retired_by:
            continue
        m = retire_re.search(rest)
        if not m:
            continue
        try:
            line_n = int(line)
        except ValueError:
            line_n = 0
        retired_by[id_] = {
            "date": m.group(1),
            "reason": m.group(2).strip(),
            "task": {"path": path, "line": line_n},
        }

failures = []
fail_path = tmp / "failures.jsonl"
if fail_path.exists():
    for ln in fail_path.read_text().splitlines():
        if ln.strip():
            failures.append(json.loads(ln))

diagnostics = []
diagnostics_path = tmp / "diagnostics.jsonl"
if diagnostics_path.exists():
    for ln in diagnostics_path.read_text().splitlines():
        if ln.strip():
            diagnostics.append(json.loads(ln))

execution_verified_path = tmp / "execution_verified.txt"
execution_verified = (
    execution_verified_path.exists() and execution_verified_path.read_text().strip() == "true"
)

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
seen_impl = set()
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
        # @covers FR-GATE-50, AC-GATE-50 -- dedup on (normpath, line): overlapping
        # src_globs entries (e.g. "ios/**" and a narrower
        # "ios/HomesFlow/**" both listed) or a "./x" vs "x" spelling of
        # the same glob can hand the same mark to expand_glob() twice
        # under different literal path strings. 62 of 100 rows duplicated
        # in a real emit before this fix (2026-08-18).
        key = (id_, os.path.normpath(path), line_n)
        if key in seen_impl:
            continue
        seen_impl.add(key)
        impl_by[id_].append({"path": path, "line": line_n, "excerpt": excerpt})

proof_by = {i: [] for i in ids}
seen_proof = set()
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
        # Same dedup, same reason -- test_globs can overlap exactly the
        # same way src_globs does (FR-GATE-50).
        key = (id_, os.path.normpath(path), line_n)
        if key in seen_proof:
            continue
        seen_proof.add(key)
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
    # FR-GATE-30: retired is a terminal state derived from an explicit
    # retirement record, checked ahead of proven/tracked-debt/backlog/GAP
    # for every type -- withdrawn is not the same claim as violated (GAP)
    # or excused (tracked-debt), regardless of what proof state a
    # retired ID happens to still show.
    if id_ in retired_by:
        return "retired"
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
status_counts = {"proven": 0, "tracked-debt": 0, "GAP": 0, "backlog": 0, "retired": 0}
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

# @covers AC-GATE-30b -- v4 freezes at exactly four status values (proven/
# tracked-debt/backlog/GAP) -- a published schema with strict validators, not a place to
# grow a fifth enum member. A retired row leaves v4's rows[] table entirely
# rather than carrying a value v4 never declared; nothing disappears
# silently, because the same information moves to a new top-level `retired`
# list (id, date, reason) instead. v5beta is where `retired` is a first-class
# row status from the start (below) -- see docs/trace-manifest-schema.md.
v4_rows = [r for r in rows if r["status"] != "retired"]
v4_status_counts = {k: status_counts[k] for k in ("proven", "tracked-debt", "GAP", "backlog")}
retired_list = [
    {"id": id_, "date": retired_by[id_]["date"], "reason": retired_by[id_]["reason"]}
    for id_ in sorted(retired_by)
]

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
        "diagnostics": diagnostics,
        "executionVerified": execution_verified,
    },
    "totals": {
        "registryIdCount": len(ids),
        "acCount": ac_count,
        "coveredCount": covered_count,
        "retiredCount": len(retired_list),
    },
    "statusCounts": v4_status_counts,
    "rows": v4_rows,
    "retired": retired_list,
}

# Prefer structured failures if bash recorded any; else respect MANIFEST_FAIL.
if failures:
    doc["gate"]["ok"] = False

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

# @covers FR-GATE-10, AC-GATE-10a, AC-GATE-10b, AC-GATE-10c -- --matrix
# re-presents THIS run's already-computed v4_rows/v4_status_counts; it
# never re-scans the target or re-derives status of its own. Family color
# tokens and canonical ordering (INTERFACE-CANON.md Sec.2: backlog ->
# tracked-debt -> proven -> GAP), self-dated with this manifest's own
# generatedAt. Retired IDs are absent here the same way they're absent
# from v4_rows -- no separate handling needed, so no fifth segment exists
# to draw.
if os.environ.get("MATRIX_MODE") == "1":
    STATUS_COLOR = {
        "backlog": "#9ed4ff",
        "tracked-debt": "#c9903a",
        "proven": "#219653",
        "GAP": "#eb5757",
    }
    STATUS_ORDER = ["backlog", "tracked-debt", "proven", "GAP"]
    TYPE_ORDER = [
        ("AC", "Acceptance criteria"),
        ("FR", "Functional requirements"),
        ("NFR", "Non-functional requirements"),
        ("US", "User stories"),
    ]

    matrix_md_path = Path(os.environ["MATRIX_MD"])
    matrix_svg_path = Path(os.environ["MATRIX_SVG"])

    md = []
    md.append(f"# Coverage Matrix: {target}")
    md.append("")
    md.append("**GENERATED FILE — do not edit.** Regenerate with "
               "`bash .../check-traceability.sh --matrix` (or the "
               "`speckit.specassay-check.matrix` command).")
    md.append("Portfolio snapshot for a cold reader; CI enforces the golden "
               "thread via the Gate script itself, not this file's freshness.")
    md.append(f"Source of truth: `{registry_rel}` registry × specs × tasks × "
               "`@covers` × tests.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("| Status | Count |")
    md.append("|---|---|")
    for st in STATUS_ORDER:
        md.append(f"| {st} | {v4_status_counts[st]} |")
    md.append(f"| **Total** | **{len(v4_rows)}** |")
    md.append("")

    for typ, label in TYPE_ORDER:
        typed_rows = [r for r in v4_rows if r["type"] == typ]
        if not typed_rows:
            continue
        md.append(f"## {label}")
        md.append("")
        md.append("| ID | Status | Statement |")
        md.append("|---|---|---|")
        for r in sorted(typed_rows, key=lambda row: row["id"]):
            statement = r["statement"].replace("|", "\\|").replace("\n", " ")
            md.append(f"| {r['id']} | {r['status']} | {statement} |")
        md.append("")

    matrix_md_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    ac_rows = [r for r in v4_rows if r["type"] == "AC"]
    ac_total = len(ac_rows) or 1
    ac_proven = len([r for r in ac_rows if r["status"] == "proven"])
    pct = ac_proven * 100 // ac_total

    bar_w, bar_x = 744, 8
    total_rows = len(v4_rows) or 1
    # Integer-division rounding leaves leftover pixels; give them to whichever
    # status has the most rows, never unconditionally to the last one in
    # STATUS_ORDER (GAP) -- a GAP:0 registry must never show so much as a
    # 1px red sliver from rounding alone. Caught smoke-testing this against
    # this repo's own registry before shipping.
    widths = {st: (v4_status_counts[st] * bar_w // total_rows) for st in STATUS_ORDER}
    leftover = bar_w - sum(widths.values())
    if leftover > 0:
        biggest = max(STATUS_ORDER, key=lambda st: v4_status_counts[st])
        widths[biggest] += leftover

    segments = []
    x = bar_x
    for st in STATUS_ORDER:
        w = widths[st]
        if w > 0:
            segments.append(f'<rect x="{x}" y="62" width="{w}" height="26" fill="{STATUS_COLOR[st]}"/>')
        x += w
    segments_svg = "\n    ".join(segments)

    legend_rows = []
    for i, st in enumerate(STATUS_ORDER):
        row_y = 116 + i * 22
        legend_rows.append(
            f'<circle cx="16" cy="{row_y}" r="6" fill="{STATUS_COLOR[st]}"/>'
            f'<text x="28" y="{row_y + 5}" class="leg">{st} ({v4_status_counts[st]})</text>'
        )
    legend_svg = "\n    ".join(legend_rows)

    footer_y = 116 + len(STATUS_ORDER) * 22 + 14
    height = footer_y + 20

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}" role="img" aria-label="Golden Thread coverage: {ac_proven} of {ac_total} acceptance criteria proven">
  <style>
    text {{ font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
    .title {{ font-size: 20px; font-weight: 600; fill: #1f2328; }}
    .sub   {{ font-size: 13px; fill: #57606a; }}
    .leg   {{ font-size: 13px; fill: #1f2328; }}
  </style>
  <text x="8" y="26" class="title">Golden Thread Coverage — {ac_proven}/{ac_total} acceptance criteria proven ({pct}%)</text>
  <text x="8" y="48" class="sub">{len(v4_rows)} registry IDs · generated {doc["generatedAt"]}</text>
  <rect x="{bar_x}" y="62" width="{bar_w}" height="26" rx="7" fill="#eaeef2"/>
  {segments_svg}
  {legend_svg}
  <text x="8" y="{footer_y}" class="sub">Generated by check-traceability.sh --matrix -- CI enforces the golden thread via the Gate script, not this file's freshness.</text>
</svg>
'''
    matrix_svg_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_svg_path.write_text(svg, encoding="utf-8")
    print(f"Wrote {matrix_md_path} and {matrix_svg_path} ({len(v4_rows)} IDs; {ac_proven}/{ac_total} ACs proven)")

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
    # Full 5-value counts (retired included) -- v4's doc carries the
    # 4-value-only view (v4_status_counts) instead; the two documents
    # disagree on this by design, per the version-boundary ruling.
    "statusCounts": status_counts,
    "rows": v5_rows,
}
v5_path = out_path.with_name(out_path.name.replace(".json", ".v5beta.json"))
v5_path.write_text(json.dumps(v5_doc, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {v5_path.name} ({len(v5_rows)} rows, schemaVersion 5, beta)")
print(f"Wrote {out_path} ({len(v4_rows)} rows) gate.ok={doc['gate']['ok']}", flush=True)
# FR-GATE-30: T900's actual unblock check is a human (or CI) reading this
# console output, not just the JSON -- the record lives in the manifest's
# top-level `retired` list either way, but the signal that matters for a
# real "can this task close" judgment call needs to be visible here too.
if retired_list:
    names = ", ".join(r["id"] for r in retired_list)
    print(f"Retired: {len(retired_list)} ({names})", flush=True)
PY

if [[ "$fail" -ne 0 ]]; then
  echo "SpecAssay Check (Gate 2): FAILED" >&2
  exit 1
fi

echo "SpecAssay Check (Gate 2): OK ($(wc -l < "$tmp/registry.txt" | tr -d ' ') registry IDs)"
