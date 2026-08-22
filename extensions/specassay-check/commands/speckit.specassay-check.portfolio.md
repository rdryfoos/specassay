---
description: Regenerate portfolio-snapshot.md — a narrative, cold-reader coverage snapshot (not CI output, not a second viewer)
---

# SpecAssay Portfolio Snapshot

<!-- @covers FR-GATE-20 -->

Runs the same Gate 2 script as `speckit.specassay-check.gate`, with one
extra flag: after computing status for every registry row exactly as the
Gate always does, it additionally re-presents that same run's data as
`portfolio-snapshot.md` — a plain-prose document for a reader with zero
prior context (a stakeholder, a new joiner), never the `GENERATED FILE —
do not edit` CI banner `--matrix`'s `coverage.md` carries. It embeds
`coverage.svg` (a shared asset — written whenever either `--matrix` or
`--portfolio` runs) as its one visual, rather than rendering a second
image.

**Scope, stated plainly:** "portfolio" here means *this one repo's own
whole thread* — every registry ID, single-repo. It is not a cross-repo
aggregate; that's a different, bigger feature, explicitly out of scope
(see `PRD.md`'s `FR-GATE-20` entry).

## Steps

1. Confirm `.specify/extensions/specassay-check/specassay-check-config.yml`
   exists (copy from `config-template.yml` if missing). Optional key
   `portfolio_md` overrides the default `portfolio-snapshot.md` path.
2. From the project root, run:

   ```sh
   SPECASSAY_PROJECT_ROOT="$PWD" \
   SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
     bash .specify/extensions/specassay-check/scripts/check-traceability.sh --portfolio
   ```

   Writes `trace-manifest.json` (as `speckit.specassay-check.gate` always
   does) plus `coverage.svg` and `portfolio-snapshot.md`, and exits
   non-zero under the exact same conditions the plain Gate run would.
   Pass both `--matrix --portfolio` in one invocation to get all three
   generated files from a single run.
3. Share `portfolio-snapshot.md` with whoever needs the zero-context
   version. It carries no CI-style banner by design (that would undercut
   the audience it's for) — but it's still a generated artifact: treat it
   the same way, regenerate it, never hand-edit it.
