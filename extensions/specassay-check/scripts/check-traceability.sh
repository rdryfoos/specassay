#!/usr/bin/env bash
# SpecAssay Check (Gate 2) — the entry point, and the one part of the Gate that
# is never allowed to be the thing that breaks.
#
# @covers FR-GATE-190, AC-GATE-190a, AC-GATE-190b, AC-GATE-190c
#
# Why this file exists, and why it is boring on purpose.
#
# 0.5.4 shipped a construct macOS's system bash (3.2.57, the only bash on a
# stock Mac) cannot parse. The check did not run at all: no manifest, no
# verdict, no registry count. Found on a Mac Mini, 2026-10-02. The status bash
# returns for a parse failure is 2, which is honest, but two ordinary ways of
# calling a checker throw that status away: a pipeline (`check | tail`) reports
# the filter's 0, and `2>/dev/null` hides the message. Either one turns "this
# check did not run" into a green line.
#
# So the check is split in two. Everything the Gate does lives in
# check-traceability.impl.sh. This file runs it and refuses to let silence pass
# for a pass:
#
#   1. It parses the implementation before running it, with the same bash that
#      is running this file, and says so in one line if it cannot. That is the
#      one failure the implementation can never report from inside itself.
#   2. It requires the implementation to have written its manifest before any
#      exit 0 is allowed through. The implementation touches a sentinel the
#      moment the manifest lands; no sentinel means no green, whatever status
#      came back.
#   3. It says the one line on BOTH stdout and stderr, because a pipeline eats
#      the status and a redirect eats the stream, and the whole point is that no
#      caller can end up with nothing.
#
# Keep this file inside what bash 3.2 can parse and run: no here-document inside
# a command substitution, no associative arrays, no `${v^^}`, no `mapfile`. It
# is the floor the bundle claims in extension.yml.
set -u

NAME="SpecAssay Check (Gate 2)"
HERE="$(cd "$(dirname "$0")" && pwd)"
IMPL="$HERE/check-traceability.impl.sh"

# One line, on both streams, and never more than one: this is the sentence a
# caller sees where the verdict should have been.
refuse() {
  echo "$NAME: FAILED to run -- $1"
  echo "$NAME: FAILED to run -- $1" >&2
}

if [ ! -f "$IMPL" ]; then
  refuse "the check itself is missing at $IMPL"
  exit 2
fi

# The running bash, not whatever `bash` happens to be first in PATH: on a Mac
# with Homebrew's bash installed, those are different shells, and the one that
# matters is the one the caller used.
SELF_BASH="${BASH:-bash}"
parse_err="$("$SELF_BASH" -n "$IMPL" 2>&1)"
if [ $? -ne 0 ]; then
  refuse "this bash cannot parse the check (bash ${BASH_VERSION:-unknown})"
  echo "$parse_err" >&2
  echo "  SpecAssay supports bash 3.2 and newer. Please report this with the line above." >&2
  exit 2
fi

# A path only this file knows, so the implementation's own temp dir (which it
# removes on exit) cannot take the evidence with it.
sentinel="${TMPDIR:-/tmp}/specassay-gate-ran.$$"
rm -f "$sentinel"

SPECASSAY_RUN_SENTINEL="$sentinel" "$SELF_BASH" "$IMPL" "$@"
rc=$?

if [ $rc -eq 0 ] && [ ! -f "$sentinel" ]; then
  rm -f "$sentinel"
  refuse "the check exited 0 without writing a manifest, so there is no run to trust"
  exit 2
fi
rm -f "$sentinel"
exit $rc
