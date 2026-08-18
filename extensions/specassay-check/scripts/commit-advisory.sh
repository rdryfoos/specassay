#!/usr/bin/env bash
# Commit-time mark advisory (paved road for PROMOTION-CONTRACT.md Rule 4,
# "marks at work time"): warns, never blocks, when a commit message names
# a registry ID but none of the staged files carry an @covers mark for
# it. Advisory only, per speccost-honesty-economics-2026-08-17_1.md's own
# "Explicitly not in scope: no blocking of commits by the mark advisory,
# warn only" -- this script exits 0 unconditionally, even when it warns,
# so it can never fail a commit on its own.
#
# Install as a commit-msg hook (one command, run once per clone):
#   ln -sf ../../.specify/extensions/specassay-check/scripts/commit-advisory.sh \
#     .git/hooks/commit-msg
#
# Usage: commit-advisory.sh <path-to-commit-msg-file>
set -uo pipefail

EXT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

CONFIG="${SPECASSAY_CONFIG:-$EXT_DIR/specassay-check-config.yml}"
[[ -f "$CONFIG" ]] || CONFIG="$EXT_DIR/config-template.yml"
[[ -f "$CONFIG" ]] || exit 0  # No config anywhere: nothing to advise against.

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

ID_RE="$(yaml_scalar id_regex)"
[[ -n "$ID_RE" ]] || ID_RE='(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?'
COVERS_RE="$(yaml_scalar covers_regex)"
[[ -n "$COVERS_RE" ]] || COVERS_RE='@covers[[:space:]]+.*'

msg_file="${1:-}"
[[ -n "$msg_file" && -f "$msg_file" ]] || exit 0

mentioned_ids="$(grep -Eo "$ID_RE" "$msg_file" 2>/dev/null | sort -u || true)"
[[ -n "$mentioned_ids" ]] || exit 0  # Nothing named, nothing to check.

staged_files="$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)"
[[ -n "$staged_files" ]] || exit 0  # Nothing staged (e.g. an amend with no file changes).

# IDs actually marked with @covers across every staged file's own
# post-staging content -- a mark already present from an earlier commit
# counts too, same as check-traceability.sh's own covers scan.
covered_ids="$(
  while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    grep -Eo "$COVERS_RE" "$f" 2>/dev/null
  done <<< "$staged_files" | grep -Eo "$ID_RE" | sort -u || true
)"

missing=""
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  grep -qx "$id" <<< "$covered_ids" || missing="$missing $id"
done <<< "$mentioned_ids"

if [[ -n "$missing" ]]; then
  echo "ADVISORY: commit message names$missing, but no staged file carries a matching @covers mark." >&2
  echo "           Not blocking -- this is a reminder, not a refusal (Rule 4a)." >&2
fi

exit 0
