#!/usr/bin/env bash
# Shared definition-line pattern. A registry bullet that actually *mints*
# an ID (bullet marker, optional bold, the ID, matching optional bold,
# then a separator and prose) as opposed to any other line that merely
# contains an ID-shaped token: a range-summary table row, a prose
# cross-reference, an index entry. mint-id.sh (style detection) and
# check-traceability.sh (duplicate-id detection) must agree on this shape,
# or one could treat a line as a real entry that the other doesn't.
#
# Usage: def_line_regex "$ID_RE"   (ID_RE is the caller's own resolved
# grammar, e.g. from config or a hardcoded default -- this function only
# owns the surrounding bullet/bold/separator shape, not the ID grammar
# itself.)
def_line_regex() {
  local id_re="$1"
  printf '^[[:space:]]*[*-][[:space:]]+\\*{0,2}%s\\*{0,2}[[:space:]]+.*$' "$id_re"
}
