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
# The grammar is wrapped in a group at the point of interpolation. Without
# it, a configured id_regex with a top-level alternation ("AC-[0-9]+|FR-[0-9]+")
# splits this whole pattern in two: the trailing branch loses the leading
# anchor and the bullet prefix, and matches anywhere on any line. A registry
# that mints each ID once then reads as dozens of definition lines, and the
# duplicate-id check refuses it. POSIX ERE has no non-capturing group, so
# this is a plain group; nothing here back-references, and grep -o still
# returns the whole match, so the numbering is free to change.
def_line_regex() {
  local id_re="$1"
  printf '^[[:space:]]*[*-][[:space:]]+\\*{0,2}(%s)\\*{0,2}[[:space:]]+.*$' "$id_re"
}
