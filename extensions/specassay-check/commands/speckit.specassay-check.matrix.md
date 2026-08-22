---
description: Regenerate coverage.md + coverage.svg (CI/PR-oriented) from the current registry/gate state — not a second viewer
---

# SpecAssay Coverage Matrix

<!-- @covers FR-GATE-10 -->

Runs the same Gate 2 script as `speckit.specassay-check.gate`, with one
extra flag: after computing status for every registry row exactly as the
Gate always does, it additionally re-presents that same run's data as two
static, committed artifacts — `coverage.md` (a summary table + one table
per ID type) and `coverage.svg` (a colored bar + legend). Nothing here is
a second scan or a second source of truth: if `coverage.svg` and Loupe's
live rendering of the same manifest ever disagree, the manifest is what's
wrong, not either renderer. CI enforces the golden thread via the Gate
script itself, on every push, regardless of whether these two files were
regenerated that push — `coverage.md`/`coverage.svg` exist for a CI log,
a PR diff, or a README badge: a terse, table-first rendering. For a
narrative document written for a reader with zero prior context, see
`speckit.specassay-check.portfolio` instead — same underlying data,
deliberately different audience and tone.

## Steps

1. Confirm `.specify/extensions/specassay-check/specassay-check-config.yml`
   exists (copy from `config-template.yml` if missing). Optional keys
   `matrix_md` / `matrix_svg` override the default `coverage.md` /
   `coverage.svg` output paths.
2. From the project root, run:

   ```sh
   SPECASSAY_PROJECT_ROOT="$PWD" \
   SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
     bash .specify/extensions/specassay-check/scripts/check-traceability.sh --matrix
   ```

   Writes `trace-manifest.json` (as `speckit.specassay-check.gate` always
   does) plus `coverage.md` and `coverage.svg`, and exits non-zero under
   the exact same conditions the plain Gate run would.
3. Commit the two generated files if you want them tracked (e.g. embedded
   in a README) — they're marked `GENERATED FILE — do not edit` at the
   top; regenerate them, never hand-edit.
