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

# @covers FR-GATE-180, AC-GATE-180
# A registry line inside a fenced code block is a quotation, not a mint.
#
# The ruling is FR-GATE-40's, applied to the file FR-GATE-40 did not reach. That
# row settled the question for `@covers` marks and test names: a mark inside a
# fence is a teaching example, and counting it as a live claim makes a document
# that explains the tool refuse the project that reads it. The registry's own
# reader never got the same treatment, so a `PRD.md` that showed a reader what a
# row looks like minted four promises nobody had made, and the Gate refused the
# project over its own documentation. Found 2026-10-02 writing the registry seed
# the bundle now ships: the seed could not carry an example of the thing it
# exists to explain.
#
# Lines are blanked rather than deleted so every line number downstream still
# points at the real line in the real file, the same way strip_code_spans does
# in check-traceability.sh. Inline code spans are deliberately left alone here:
# the definition-line shape admits no backtick around the ID, so an ID inside a
# span is already not a definition, and blanking spans would have let a
# statement's own prose damage the line it was read from.
strip_fenced_lines() {
  awk '
    BEGIN { in_fence = 0 }
    {
      if ($0 ~ /^[[:space:]]*(```|~~~)/) { in_fence = !in_fence; print ""; next }
      if (in_fence) { print ""; next }
      print
    }
  ' "$1" 2>/dev/null
}
