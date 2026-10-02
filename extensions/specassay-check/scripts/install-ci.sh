#!/usr/bin/env bash
# Put the SpecAssay workflow where GitHub will run it.
#
# @covers FR-COLD-30, AC-COLD-30a, AC-COLD-30b
#
# Why a script and not the installer: Spec Kit's extension installer cannot write
# outside `.specify/extensions/<id>/`. Its `provides` section carries commands,
# templates, scripts and config, every one of them deployed under that directory,
# and the only `.github` paths the CLI writes at all are Copilot prompts and
# `.github/hooks/speckit.json` (read from Spec Kit 1.0.5's own source,
# 2026-10-02). Hooks are agent-side events, not install-time ones. So the bundle
# ships the workflow and this one command places it, which is the whole of what a
# stranger has to do by hand to get a Thread Report onto a pull request.
#
# Idempotent: refuses rather than overwrite a workflow that differs, and says
# nothing has changed when the installed copy already matches.
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

# The workflow belongs to the repository, which is not always the project root: a
# project in a subdirectory still has one .github at the top of its checkout.
REPO_ROOT="$PROJECT_ROOT"
if git -C "$PROJECT_ROOT" rev-parse --show-toplevel >/dev/null 2>&1; then
  REPO_ROOT="$(git -C "$PROJECT_ROOT" rev-parse --show-toplevel)"
fi

SRC="$EXT_DIR/ci/specassay.yml"
DEST_DIR="$REPO_ROOT/.github/workflows"
DEST="$DEST_DIR/specassay.yml"
FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1

[[ -f "$SRC" ]] || { echo "FAIL: workflow not found at $SRC" >&2; exit 2; }

# The project root the workflow reads, relative to the repository root, so a
# project in a subdirectory needs no hand edit.
rel="${PROJECT_ROOT#"$REPO_ROOT"}"
rel="${rel#/}"
[[ -z "$rel" ]] && rel="."

# Render what this project's workflow should contain, then compare that against
# what is installed. Comparing the shipped file directly would call a workflow
# "unchanged" when it carries the wrong project root: the substitution below is
# part of the file's correct content, not a step after the decision.
rendered="$(mktemp)"
trap 'rm -f "$rendered"' EXIT
if [[ "$rel" == "." ]]; then
  cp "$SRC" "$rendered"
else
  # One line, matched on the key, so the comment above it is left alone.
  sed "s|^  SPECASSAY_PROJECT: \".\"$|  SPECASSAY_PROJECT: \"$rel\"|" "$SRC" > "$rendered"
  grep -q "^  SPECASSAY_PROJECT: \"$rel\"$" "$rendered" || {
    echo "FAIL: could not set SPECASSAY_PROJECT in the shipped workflow; set it by hand after copying" >&2
    exit 2
  }
fi

if [[ -f "$DEST" ]]; then
  if cmp -s "$rendered" "$DEST"; then
    echo "already installed, unchanged: ${DEST#"$REPO_ROOT"/}" >&2
    exit 0
  fi
  if (( FORCE == 0 )); then
    echo "FAIL: ${DEST#"$REPO_ROOT"/} exists and differs from the workflow this project should have" >&2
    echo "  Look at the difference before deciding; your edits may be deliberate:" >&2
    echo "    diff ${DEST#"$REPO_ROOT"/} ${SRC#"$REPO_ROOT"/}" >&2
    echo "  Replace it with the shipped copy: bash $0 --force" >&2
    exit 2
  fi
fi

mkdir -p "$DEST_DIR"
cp "$rendered" "$DEST"

echo "wrote ${DEST#"$REPO_ROOT"/} (project root: $rel)" >&2
echo "  On every pull request it runs the Gate on the head and on the base, posts one Thread Report comment saying what the change did to your promises, and fails the check if the Gate refuses. A local run before you push is still worth having; this is the run that protects the thread." >&2
echo "  Commit it along with .specify/, then open a pull request." >&2
