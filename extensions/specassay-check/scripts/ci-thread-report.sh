#!/usr/bin/env bash
# Everything a Thread Report comment needs, in one place: the Gate on the head,
# the Gate on the base commit, the changed files, and the report itself.
#
# @covers FR-COLD-40, AC-COLD-40a
#
# This exists as a script rather than as steps inside the workflow so that the
# sequence CI runs is the sequence a test can run. The end-to-end proof
# (tests/test_cold_path_end_to_end.py) drives this file, so the workflow and the
# proof cannot drift apart: what remains in the workflow is the part that needs
# GitHub, posting the comment and setting the statuses.
#
# Usage:
#   ci-thread-report.sh --base-sha <sha> --out-dir <dir> [options]
#     --project <rel>    project root relative to the repository root (default ".")
#     --pr-url <url>     pull request URL, which turns on file and ID links
#     --head-sha <sha>   head commit, for the blob links
#
# Writes into <dir>: head.json, base.json (when the base has the extension),
# changed.txt, report.md. Exits 0 whenever it produced a report, including when
# the Gate refused: the refusal is in head.json for the caller to act on, and a
# broken thread must still get its briefing.
set -euo pipefail

export LC_ALL=C

BASE_SHA=""
OUT_DIR=""
PROJECT="."
PR_URL=""
HEAD_SHA=""

usage() {
  echo "Usage: ci-thread-report.sh --base-sha <sha> --out-dir <dir> [--project <rel>] [--pr-url <url>] [--head-sha <sha>]" >&2
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-sha) [[ $# -ge 2 ]] || usage; BASE_SHA="$2"; shift 2 ;;
    --out-dir)  [[ $# -ge 2 ]] || usage; OUT_DIR="$2"; shift 2 ;;
    --project)  [[ $# -ge 2 ]] || usage; PROJECT="$2"; shift 2 ;;
    --pr-url)   [[ $# -ge 2 ]] || usage; PR_URL="$2"; shift 2 ;;
    --head-sha) [[ $# -ge 2 ]] || usage; HEAD_SHA="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -n "$BASE_SHA" && -n "$OUT_DIR" ]] || usage

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT="${PROJECT#./}"
PROJECT="${PROJECT%/}"
[[ -z "$PROJECT" ]] && PROJECT="."
if [[ "$PROJECT" == "." ]]; then
  ROOT="$REPO_ROOT"
else
  ROOT="$REPO_ROOT/$PROJECT"
fi
EXT="$ROOT/.specify/extensions/specassay-check"
CONFIG="$EXT/specassay-check-config.yml"

if [[ ! -f "$EXT/scripts/check-traceability.sh" ]]; then
  echo "FAIL: no SpecAssay extension at $EXT" >&2
  echo "  Install it (specify bundle install specassay) and commit .specify/, or pass --project <dir> naming the project root." >&2
  exit 2
fi
[[ -f "$CONFIG" ]] || CONFIG="$EXT/config-template.yml"

mkdir -p "$OUT_DIR"

PYTHON="${SPECASSAY_PYTHON:-}"
if [[ -z "$PYTHON" ]]; then
  if command -v python3 >/dev/null 2>&1; then PYTHON=python3; else PYTHON=python; fi
fi

manifest_path() {
  # The config may send the manifest somewhere other than the project root.
  local cfg="$1" rel
  rel="$(awk '/^manifest_path:[[:space:]]*/ { sub("^[^:]+:[[:space:]]*", ""); gsub(/^"/, ""); gsub(/"$/, ""); print; exit }' "$cfg")"
  [[ -n "$rel" ]] || rel="trace-manifest.json"
  printf '%s' "$rel"
}

# The Gate on the PR head. It always writes the manifest and then exits non-zero
# if the thread is broken, so the refusal is carried in the file rather than by
# stopping here: a broken thread still gets its report.
HEAD_REL="$(manifest_path "$CONFIG")"
SPECASSAY_PROJECT_ROOT="$ROOT" SPECASSAY_CONFIG="$CONFIG" \
  bash "$EXT/scripts/check-traceability.sh" || true
cp "$ROOT/$HEAD_REL" "$OUT_DIR/head.json"
v5="${HEAD_REL%.json}.v5beta.json"
[[ -f "$ROOT/$v5" ]] && cp "$ROOT/$v5" "$OUT_DIR/head.v5beta.json"

# The Gate on the base commit, in a throwaway worktree. A base that predates the
# install has no script to run: the report then treats every row as new, which is
# what it does when given no base at all.
BASE_WT="$(mktemp -d)"
rm -rf "$BASE_WT"
git worktree add --quiet --detach "$BASE_WT" "$BASE_SHA"
if [[ "$PROJECT" == "." ]]; then BROOT="$BASE_WT"; else BROOT="$BASE_WT/$PROJECT"; fi
BEXT="$BROOT/.specify/extensions/specassay-check"
if [[ -f "$BEXT/scripts/check-traceability.sh" ]]; then
  BCONFIG="$BEXT/specassay-check-config.yml"
  [[ -f "$BCONFIG" ]] || BCONFIG="$BEXT/config-template.yml"
  BASE_REL="$(manifest_path "$BCONFIG")"
  SPECASSAY_PROJECT_ROOT="$BROOT" SPECASSAY_CONFIG="$BCONFIG" \
    bash "$BEXT/scripts/check-traceability.sh" || true
  [[ -f "$BROOT/$BASE_REL" ]] && cp "$BROOT/$BASE_REL" "$OUT_DIR/base.json"
else
  echo "No SpecAssay on the base commit; every row reads as new." >&2
fi
git worktree remove --force "$BASE_WT"

git diff --name-only "${BASE_SHA}...HEAD" > "$OUT_DIR/changed.txt"

args=(
  --base "$OUT_DIR/base.json"
  --head "$OUT_DIR/head.json"
  --changed-files "$OUT_DIR/changed.txt"
  --config "$CONFIG"
  --project-root "$PROJECT"
  --out "$OUT_DIR/report.md"
)
[[ -n "$PR_URL" ]] && args+=(--pr-url "$PR_URL")
[[ -n "$HEAD_SHA" ]] && args+=(--head-sha "$HEAD_SHA")
"$PYTHON" "$EXT/scripts/thread-report.py" "${args[@]}"

echo "wrote $OUT_DIR/report.md" >&2
