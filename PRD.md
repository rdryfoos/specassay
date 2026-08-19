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
- FR-DOCS-50 — Once FR-GATE-40 ships, restore `docs/**` to `specassay-check-config.yml`'s `src_globs`. Companion to FR-GATE-40, minted the same day: the current exclusion is a tracked temporary, not a settlement.

## GATE

Migrated from `docs/backlog.md`'s existing anointed items 2026-08-18.
Coverage basis: registration of existing intent, not newly attributed — the
asks below predate this mint; see `docs/backlog.md` for the full narrative
each was minted from.

- FR-GATE-10 — `--matrix`: regenerate a human-readable coverage table + SVG summary bar from the current registry/gate state.
- FR-GATE-20 — Portfolio-snapshot mode: the same coverage data, framed for a cold reader rather than CI.
- FR-GATE-30 — `retired`: a terminal state alongside proven/tracked-debt/backlog/GAP, distinguishing an intent withdrawn on purpose (a tombstoned registry statement on a closed carrying task) from a silent GAP.
- FR-GATE-40 — `orphan-covers` gains domain scoping consistent with `orphan-spec` and `orphan-task`, so `@covers` detection distinguishes use from mention: marks inside fenced code blocks, documentation files, and the checker's own comments are not live marks. Minted 2026-08-18, citing the DOCS-room founding finding: `docs/**` had to be excluded from the assayer's own self-governance because the Gate could not yet read its own documentation without believing it (`docs/docs-gaps.md`).
  - AC-GATE-40 — Given a docs file quoting an `@covers` line as a teaching example, when the Gate runs with docs in `src_globs`, then no `orphan-covers` finding derives from the quotation.
  - AC-GATE-41 — Given `check-traceability.sh`'s own source, when scanned, then its comments and regex definitions never self-match.
- FR-GATE-50 — The manifest emitter dedupes `implementations` (and `proofs`) on `(id, normpath, line)` before writing the manifest, so the same mark reached twice (overlapping `src_globs` entries, or a `./x` vs `x` path spelling) is listed once. Minted 2026-08-18, citing a real emit where 62 of 100 rows carried duplicated implementations.
  - AC-GATE-50 — Given the same `@covers` mark reachable via two overlapping `src_globs` entries or a `./x` vs `x` path spelling, when the manifest is emitted, then that mark appears exactly once in `implementations`.
- FR-GATE-70 — A list-type config key (`src_globs`, `test_globs`, or any later `yaml_list()` consumer) that's present but malformed (an inline YAML array) or bare (no items under it) refuses loudly before any scanning, instead of silently parsing to an empty list. Minted 2026-08-19: the self-referential case of the silent-gap shape this tool exists to refuse in adopters' own work — found twice in one day, once in the docs room's own reproduction recipe and once in the capture session that followed it.
  - AC-GATE-70a — Given a list-type config key written as an inline array, when the Gate runs, then it refuses before any scanning: stderr names the key, quotes the offending raw line, shows the accepted block-style shape, and points at the troubleshooting entry — no `trace-manifest.json` is written.
  - AC-GATE-70b — Given a list-type config key present with no items under it, when the Gate runs, then it refuses the same way, and the message states plainly that omitting the key entirely is what means "none."
  - AC-GATE-70c — Given a list-type config key absent from the file entirely, when the Gate runs, then behavior is unchanged: an empty list, no refusal.
- FR-GATE-60 — An additive `provenVia` (delegated-proof) field on FR/US rows, naming the AC(s) whose proof stands in for a row that carries no `@covers`/test of its own, so Loupe's PROOF stage can render the chain instead of "No proof." Minted 2026-08-18, design-room proposal, considered not built: **open design question** — the registry has no existing FR→AC parent/child edge (shared ID-domain prefix is a naming convention, not a declared relationship), so `provenVia` needs either (a) an explicit author-declared link (e.g. a `**Provenvia**:`/registry-annotation grammar, honest but one more thing to write) or (b) an inferred one (the emitter guesses from domain/statement adjacency, convenient but a real risk of a false chain — exactly the kind of self-report Rule 6a exists to refuse). No AC yet; needs that ruling first.

## SELF

One bounded meta-row, minted 2026-08-18: retroactive coverage for this
repo's own pre-existing behavior. Burns down over time; explicitly does not
block DOCS-room work.

- FR-SELF-10 — Backfill `@covers` marks across specassay's own existing extension/preset behavior that already works but was never annotated.
