---
description: Archaeology mode (no-LLM floor) — propose a first-pass candidate registry from an unfamiliar repo's tests, routes, structure, docs, and history
argument-hint: "[path] [--out <path>] [--sources <list>] [--dry-run]"
---

# SpecAssay Dig

<!-- @covers US-DIG-10 -->

Static, no-LLM heuristics over a target repo's own test names/bodies,
routes/API surface, module/directory structure, README/docs prose, and
commit history propose a first-pass candidate registry — a starting map
for a stranger dropped into someone else's codebase, not a minted one.

**The one hard law:** no dug row is ever written into a real registry, by
this command or any other means. `dig` only ever produces `dig-report.json`
— flat data the Gate never loads, never chains, never governs anything
with. There is no `--anoint` flag. Turning a proposed row into a real,
dated, minted registry row is separate, later, human work.

## User Input

```text
$ARGUMENTS
```

## Steps

1. From the project root (or any target repo you want a first-pass read
   of — this command never requires a SpecAssay-governed project), run:

   ```sh
   python3 <path-to-specassay>/extensions/specassay-check/scripts/dig.py $ARGUMENTS
   ```

   Once installed via the extension's scaffold, the shipped copy lives at
   `.specify/extensions/specassay-check/scripts/dig.py`.

2. Without `--dry-run`, this writes `dig-report.json` at the target repo's
   root (or wherever `--out` points) and prints row counts by type and
   source. With `--dry-run`, it prints the same counts and writes nothing
   at all.

3. Read `dig-report.json` yourself. Every row carries `epistemicClass:
   "inferred"` and cites exactly where it came from (`provenance`) — treat
   it as a first draft to review, never as something already true. Nothing
   in this file is registered, covered, or gated until a person looks at
   it and, separately, mints what's real.
