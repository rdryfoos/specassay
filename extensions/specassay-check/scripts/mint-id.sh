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
    echo "WARN: config MISSING at $CONFIG; using config-template.yml defaults (registry PRD.md)" >&2
    echo "  scaffold it once: cp $EXT_DIR/config-template.yml $EXT_DIR/specassay-check-config.yml" >&2
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

usage() {
  echo "Usage:" >&2
  echo "  mint-id.sh --init" >&2
  echo "  mint-id.sh <PREFIX> <AREA> [--authorship <case|design|retrospective|constitution>] [--append \"statement text\"]" >&2
  echo "  mint-id.sh --resolve <DUPLICATE_ID>" >&2
  exit 2
}

# @covers FR-COLD-20, AC-COLD-20a -- the registry a project starts from.
#
# Until today the first mint in a new project refused with "registry not found"
# and the mint command told the agent to `touch` the file, which left a stranger
# holding an empty document and no account of what a row looks like. The seed
# carries the grammar, one fenced example of each kind of row, and what the
# Authorship mark means, where a person is standing when they need it.
SEED="$EXT_DIR/templates/registry-seed.md"

init_registry() {
  if [[ -f "$REGISTRY" ]]; then
    echo "FAIL: $REGISTRY already exists ($(grep -c "" "$REGISTRY") lines); --init never overwrites a registry" >&2
    echo "  Mint into it instead: mint-id.sh <PREFIX> <AREA> --authorship <value> --append \"statement\"" >&2
    exit 2
  fi
  if [[ ! -f "$SEED" ]]; then
    echo "FAIL: registry seed not found at $SEED" >&2
    exit 2
  fi
  cp "$SEED" "$REGISTRY"
  echo "wrote $REGISTRY from the registry seed ($(grep -c "" "$REGISTRY") lines)" >&2
  echo "  It holds the ID grammar, one fenced example of each kind of row, and no promises: the Gate reads a fenced line as a quotation, so a first run on it is green and says the green proves nothing." >&2
  echo "  Mint your first row: mint-id.sh <PREFIX> <AREA> --authorship <case|design|retrospective|constitution> --append \"statement\"" >&2
}

require_registry() {
  [[ -f "$REGISTRY" ]] && return 0
  echo "FAIL: registry not found: $REGISTRY" >&2
  echo "  Create it from the seed, which carries the grammar and an example of each kind of row:" >&2
  echo "    bash $0 --init" >&2
  echo "  Or point the config's registry: key at the document that already holds your requirements." >&2
  exit 2
}

# Style-detection: find the first registry line shaped like a real
# definition (bullet, optional bold, an ID, a dash) -- not a summary
# table row or a prose mention -- and reuse its exact bullet/bold/dash
# characters so a minted line matches house style instead of guessing.
# Shared with check-traceability.sh's duplicate-id detection so both
# scripts agree on what a "real" registry entry looks like.
source "$(dirname "$0")/lib-def-line.sh"
ID_RE="$(yaml_scalar id_regex)"
[[ -n "$ID_RE" ]] || ID_RE='(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?'
DEF_LINE_RE="$(def_line_regex "$ID_RE")"

# @covers FR-GATE-180, AC-GATE-180b -- one rule for every reader of the registry.
# A fenced line is a quotation, so it cannot lend its style to a mint, cannot
# raise the next number, and cannot be mistaken for a collision.
style_template() {
  strip_fenced_lines "$REGISTRY" | grep -Em1 "$DEF_LINE_RE" || true
}

# Split a style-template line into (prefix-up-to-and-including-bold-open,
# id, bold-close-and-separator) using its own ID as the split point.
# @covers FR-COLD-20, AC-COLD-20b -- the Authorship mark rides on the minted
# line. Every row this helper wrote before today came out unassigned, so a
# project that used the documented command got a diagnostic on every row it
# minted and no hint that a word was missing. The value is validated here
# against the same four the Gate accepts, because a mint that writes a value
# the Gate refuses is worse than a mint that writes none.
AUTHORSHIP_VALUES="case design retrospective constitution"

validate_authorship() {
  local v="$1"
  local lower
  lower="$(printf '%s' "$v" | tr '[:upper:]' '[:lower:]')"
  for known in $AUTHORSHIP_VALUES; do
    [[ "$lower" == "$known" ]] && { printf '%s' "$lower"; return 0; }
  done
  echo "FAIL: --authorship $v is not one of the four: $AUTHORSHIP_VALUES" >&2
  echo "  case: the row states a promise from the project's case. design: a decision you made rather than one you were asked for. retrospective: minted from a defect or a review. constitution: a principle demanded it." >&2
  exit 2
}

render_line() {
  local new_id="$1" statement="$2" authorship="${3:-}" sample mark=""
  if [[ -n "$authorship" ]]; then
    # The statement keeps its own full stop and the mark follows it, which is the
    # shape the Gate's AUTHORSHIP_RE reads and the shape every row in this
    # repository's own registry is written in.
    mark=" **Authorship**: ${authorship}"
  fi
  sample="$(style_template)"
  if [[ -z "$sample" ]]; then
    # No existing definition line to imitate -- fall back to a plain,
    # unambiguous style.
    echo "- ${new_id} — ${statement}${mark}"
    return
  fi
  local sample_id before after
  sample_id="$(grep -Eo "$ID_RE" <<<"$sample" | head -1)"
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
  echo "${before}${new_id}${sep}${statement}${mark}"
}

highest_number() {
  local prefix="$1" area="$2"
  # `|| true` on the grep: no existing entries (a brand-new area) is a
  # normal case, not a failure -- without this, pipefail + set -e would
  # abort the whole script silently on the very first mint in an area.
  # Lettered ACs (AC-GATE-90a) count toward the highest number too: the
  # grammar allows an optional [a-z] suffix, and a mint that ignored it
  # handed back AC-GATE-90 while AC-GATE-90a/b/c already existed (found
  # 2026-09-03 running the documented command as a receipt).
  { strip_fenced_lines "$REGISTRY" | grep -Eo "\\b${prefix}-${area}-[0-9]+[a-z]?\\b" 2>/dev/null || true; } \
    | sed -E "s/^${prefix}-${area}-//; s/[a-z]$//" \
    | sort -n | tail -1
}

mint_primary() {
  local prefix="$1" area="$2" append_text="${3:-}" authorship="${4:-}"
  local highest next
  highest="$(highest_number "$prefix" "$area")"
  if [[ -z "$highest" ]]; then
    next=10
  else
    next=$(( (highest / 10 + 1) * 10 ))
  fi
  local new_id="${prefix}-${area}-${next}"
  # @covers FR-GATE-130, AC-GATE-130 -- this decade scheme *is* the stock
  # TYPE-DOMAIN-NN grammar, written out.
  # A project may configure another, and then the ID composed here is one
  # the Gate will refuse the moment it is used: the tool would be issuing
  # scope its own checker rejects. Say so instead, and let the registry's
  # own grammar be minted by hand.
  if ! grep -qE "^${ID_RE}$" <<<"$new_id"; then
    echo "FAIL: mint-id composes ${prefix}-${area}-NN, which this project's configured id_regex does not admit:" >&2
    echo "  id_regex: $ID_RE" >&2
    echo "  would have minted: $new_id" >&2
    echo "  Mint this ID by hand into $REGISTRY in the grammar the config declares; the Gate reads the registry, not this helper." >&2
    exit 2
  fi
  echo "$new_id"

  # @covers FR-COLD-20, AC-COLD-20c -- print the whole line, not only the ID, so
  # nobody composes a registry line by hand. The ID stays alone on stdout, which
  # is what a caller captures; everything advisory goes to stderr, where this
  # script already puts the config warning and the coverage-basis reminder.
  local statement="${append_text:-<your statement: given ..., when ..., then ...>}"
  local line
  line="$(render_line "$new_id" "$statement" "$authorship")"

  if [[ -n "$append_text" ]]; then
    printf '%s\n' "$line" >> "$REGISTRY"
    echo "appended to $REGISTRY:" >&2
    echo "  $line" >&2
    echo "REMINDER: state the coverage basis plainly in the mint commit." >&2
    echo "  Already-built work this mint is only now registering: \"coverage registered, not newly attributed.\"" >&2
    echo "  New work this mint is starting: say that instead. Either is honest; silence about which is not." >&2
  else
    echo "nothing written. The line to paste into $REGISTRY, in the file's own style:" >&2
    echo "  $line" >&2
  fi

  if [[ -z "$authorship" ]]; then
    echo "NOTE: no --authorship, so this row will read as unassigned until a hand adds one." >&2
    echo "  One of: $AUTHORSHIP_VALUES. The Gate reports an unassigned row; it does not refuse it." >&2
  fi
}

resolve_duplicate() {
  local dup_id="$1"
  local prefix area decade
  if [[ ! "$dup_id" =~ ^(FR|NFR|AC|US)-([A-Z][A-Z0-9]{1,5})-([0-9]+)$ ]]; then
    echo "FAIL: '$dup_id' doesn't look like PREFIX-AREA-NUMBER" >&2
    echo "  --resolve allocates from the stock grammar's reserved 1-9 offset lane, which only exists in that grammar." >&2
    echo "  This project's configured id_regex is: $ID_RE" >&2
    echo "  If that is not the stock shape, resolve the duplicate by hand in $REGISTRY." >&2
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
  used="$({ strip_fenced_lines "$REGISTRY" | grep -Eo "\\b${prefix}-${area}-${decade_tens}[1-9]\\b" 2>/dev/null || true; } \
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

if [[ "$1" == "--init" ]]; then
  [[ $# -eq 1 ]] || usage
  init_registry
elif [[ "$1" == "--resolve" ]]; then
  [[ $# -eq 2 ]] || usage
  require_registry
  resolve_duplicate "$2"
elif [[ $# -ge 2 ]]; then
  require_registry
  prefix="$1"; area="$2"; shift 2
  append_text=""
  authorship=""
  # --append and --authorship in either order, each at most once: the two were
  # added a release apart and a user should not have to remember which came
  # first.
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --append)
        [[ $# -ge 2 && -z "$append_text" ]] || usage
        append_text="$2"; shift 2 ;;
      --authorship)
        [[ $# -ge 2 && -z "$authorship" ]] || usage
        authorship="$(validate_authorship "$2")"; shift 2 ;;
      *) usage ;;
    esac
  done
  mint_primary "$prefix" "$area" "$append_text" "$authorship"
else
  usage
fi
