#!/usr/bin/env bash
# SpecAssay mint helper. Mints the next primary ID for a prefix+area, or
# resolves a duplicate-id Gate refusal by handing back the next free
# offset in that ID's reserved lane.
#
# Minting scheme (see SpecCost design discussion, 2026-08):
#   - Primary mints always land on a multiple of ten: the smallest one
#     strictly greater than the highest existing number (decade or
#     offset) already used under that prefix+area. A brand-new area
#     starts at 10.
#   - The step size does NOT reduce how often two branches collide on
#     the same next number -- both compute from the same last-observed
#     state regardless of step size. What it buys: the 1-9 offset off
#     every decade is reserved exclusively for collision resolution,
#     never issued by a primary mint, so resolving a duplicate is a
#     purely local "+1" with no need to recompute current registry
#     state. The ones digit doubles as a free collision counter for
#     that slot.
#
# Usage:
#   mint-id.sh <PREFIX> <AREA>                 print the next primary ID
#   mint-id.sh <PREFIX> <AREA> --append "TEXT"  also append a registry line
#   mint-id.sh --resolve <DUPLICATE_ID>         print the next free offset
#
# Config discovery mirrors check-traceability.sh exactly (same
# specassay-check-config.yml / config-template.yml, same registry).
set -euo pipefail

export LC_ALL=C

EXT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="${SPECASSAY_PROJECT_ROOT:-}"
if [[ -z "$PROJECT_ROOT" ]]; then
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

REGISTRY="$(yaml_scalar registry)"
[[ -n "$REGISTRY" ]] || { echo "FAIL: config missing registry" >&2; exit 2; }
[[ -f "$REGISTRY" ]] || { echo "FAIL: registry not found: $REGISTRY" >&2; exit 2; }

usage() {
  echo "Usage:" >&2
  echo "  mint-id.sh <PREFIX> <AREA> [--append \"statement text\"]" >&2
  echo "  mint-id.sh --resolve <DUPLICATE_ID>" >&2
  exit 2
}

# Style-detection: find the first registry line shaped like a real
# definition (bullet, optional bold, an ID, a dash) -- not a summary
# table row or a prose mention -- and reuse its exact bullet/bold/dash
# characters so a minted line matches house style instead of guessing.
# Shared with check-traceability.sh's duplicate-id detection so both
# scripts agree on what a "real" registry entry looks like.
source "$(dirname "$0")/lib-def-line.sh"
DEF_LINE_RE="$(def_line_regex '(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?')"

style_template() {
  grep -Em1 "$DEF_LINE_RE" "$REGISTRY" || true
}

# Split a style-template line into (prefix-up-to-and-including-bold-open,
# id, bold-close-and-separator) using its own ID as the split point.
render_line() {
  local new_id="$1" statement="$2" sample
  sample="$(style_template)"
  if [[ -z "$sample" ]]; then
    # No existing definition line to imitate -- fall back to a plain,
    # unambiguous style.
    echo "- ${new_id} — ${statement}"
    return
  fi
  local sample_id before after
  sample_id="$(grep -Eo '(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?' <<<"$sample" | head -1)"
  before="${sample%%"$sample_id"*}"
  after="${sample#*"$sample_id"}"
  # after starts with whatever closes the ID (e.g. "** — " or " — ")
  # followed by the sample's own statement text; keep only the closer
  # + separator, not the old statement.
  local sep
  sep="$(grep -Eo '^\*{0,2}[[:space:]]*[—–-]+[[:space:]]*' <<<"$after" || true)"
  if [[ -z "$sep" ]]; then
    sep=' — '
  fi
  echo "${before}${new_id}${sep}${statement}"
}

highest_number() {
  local prefix="$1" area="$2"
  # `|| true` on the grep: no existing entries (a brand-new area) is a
  # normal case, not a failure -- without this, pipefail + set -e would
  # abort the whole script silently on the very first mint in an area.
  { grep -Eo "\\b${prefix}-${area}-[0-9]+\\b" "$REGISTRY" 2>/dev/null || true; } \
    | sed -E "s/^${prefix}-${area}-//" \
    | sort -n | tail -1
}

mint_primary() {
  local prefix="$1" area="$2" append_text="${3:-}"
  local highest next
  highest="$(highest_number "$prefix" "$area")"
  if [[ -z "$highest" ]]; then
    next=10
  else
    next=$(( (highest / 10 + 1) * 10 ))
  fi
  local new_id="${prefix}-${area}-${next}"
  echo "$new_id"
  if [[ -n "$append_text" ]]; then
    render_line "$new_id" "$append_text" >> "$REGISTRY"
    echo "appended to $REGISTRY" >&2
  fi
}

resolve_duplicate() {
  local dup_id="$1"
  local prefix area decade
  if [[ ! "$dup_id" =~ ^(FR|NFR|AC|US)-([A-Z][A-Z0-9]{1,5})-([0-9]+)$ ]]; then
    echo "FAIL: '$dup_id' doesn't look like PREFIX-AREA-NUMBER" >&2
    exit 2
  fi
  prefix="${BASH_REMATCH[1]}"
  area="${BASH_REMATCH[2]}"
  decade="${BASH_REMATCH[3]}"
  if (( decade % 10 != 0 )); then
    echo "FAIL: $dup_id is not a primary (multiple-of-ten) mint -- only primary mints collide under this scheme; resolve was given an already-offset ID" >&2
    exit 2
  fi
  # decade is always a multiple of ten, so its offsets (decade+1 .. decade+9)
  # are exactly "decade with the trailing zero swapped for the offset digit" --
  # e.g. decade=20: offsets are 21..29, i.e. "2" + [1-9], not "20" + [1-9].
  local decade_tens=$((decade / 10))
  local used offset=1
  used="$({ grep -Eo "\\b${prefix}-${area}-${decade_tens}[1-9]\\b" "$REGISTRY" 2>/dev/null || true; } \
    | sed -E "s/^${prefix}-${area}-${decade_tens}//" | sort -n)"
  while grep -qx "$offset" <<<"$used"; do
    offset=$((offset + 1))
  done
  if (( offset > 9 )); then
    echo "FAIL: all 9 offsets for ${prefix}-${area}-${decade} are used -- this decade has collided 9 times, look at what's going on here" >&2
    exit 1
  fi
  echo "${prefix}-${area}-$((decade + offset))"
}

[[ $# -ge 1 ]] || usage

if [[ "$1" == "--resolve" ]]; then
  [[ $# -eq 2 ]] || usage
  resolve_duplicate "$2"
elif [[ $# -ge 2 ]]; then
  prefix="$1"; area="$2"; shift 2
  append_text=""
  if [[ "${1:-}" == "--append" ]]; then
    [[ $# -eq 2 ]] || usage
    append_text="$2"
  elif [[ $# -ne 0 ]]; then
    usage
  fi
  mint_primary "$prefix" "$area" "$append_text"
else
  usage
fi
