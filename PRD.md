# SpecAssay — Product Requirements (ID Registry)

This PRD is the **authoritative ID registry** for the `specassay` repo's own
work — the tool dogfooding itself. Founded 2026-08-18 by the docs room
(design-room ruling), scoped explicitly as **founding, not backfill**: no row
below is minted `proven` by declaration. Every ID here rides as **anointed
backlog** (registry entry + one open `**Carries**:` TODO in
`specs/backlog/tasks.md`) until real work picks it up — the registry opens
honest-empty and earns its greens from there, per Rule 6a.

SpecAssay Gate 2 enforces the exact-set rule: the IDs defined here must equal
the IDs referenced in `specs/` and `tasks.md` (the one exception is
*anointed backlog*, an ID carried only by an open TODO).

## DOCS

First citizens of this registry — new work, minted 2026-08-18 (US-DOCS-10,
anointed backlog: reach a working Gate from the public quickstart alone).

- US-DOCS-10 — As a cold installer, I want to reach a working Gate on my own repo from the public quickstart alone, so adoption needs no author in the loop.
- FR-DOCS-10 — Quickstart: install, config, first check, first honest red.
- FR-DOCS-20 — Trace-manifest format reference, versioned with the schema.
- FR-DOCS-30 — Troubleshooting built from real failure classes, each entry citing the incident that taught it.
- FR-DOCS-40 — Every documented behavior cites the registry row(s) it documents.
- AC-DOCS-10 — Given a cold installer with no prior context, when following the public quickstart alone, then a working Gate on their own repo within 30 minutes, zero questions asked of the author.

## GATE

Migrated from `docs/backlog.md`'s existing anointed items 2026-08-18.
Coverage basis: registration of existing intent, not newly attributed — the
asks below predate this mint; see `docs/backlog.md` for the full narrative
each was minted from.

- FR-GATE-10 — `--matrix`: regenerate a human-readable coverage table + SVG summary bar from the current registry/gate state.
- FR-GATE-20 — Portfolio-snapshot mode: the same coverage data, framed for a cold reader rather than CI.
- FR-GATE-30 — `retired`: a terminal state alongside proven/tracked-debt/backlog/GAP, distinguishing an intent withdrawn on purpose (a tombstoned registry statement on a closed carrying task) from a silent GAP.

## SELF

One bounded meta-row, minted 2026-08-18: retroactive coverage for this
repo's own pre-existing behavior. Burns down over time; explicitly does not
block DOCS-room work.

- FR-SELF-10 — Backfill `@covers` marks across specassay's own existing extension/preset behavior that already works but was never annotated.
