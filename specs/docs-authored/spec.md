# DOCS room — content that has actually shipped

Claims DOCS-area registry IDs once their content has actually been written
and carries a real `@covers` mark, the same way `specs/self-gate-config/spec.md`
claims this repo's own engine work. Anointed backlog is for content not yet
written; this spec is where the ID lands once it has.

- US-DOCS-10 — As a cold installer, I want to reach a working Gate on my
  own repo from the public quickstart alone. Proven 2026-08-19 by a real,
  independently-reverified cold-agent trial: `docs/testing/completed/
  evidence-cold-agent-trial-observed-2026-08-19.md`. Its child `AC-DOCS-10`
  stays `tracked-debt`, not `proven` — see `specs/backlog/tasks.md` (T900)
  for why field-trial evidence can't mechanically satisfy Rule 6's
  named-test requirement for an AC, even a real one.
- FR-DOCS-10 — Quickstart (install, config, first check, first honest red).
  Shipped 2026-08-18 in `README.md`'s "Install (catalog path)" section,
  including the "See a real refusal" walkthrough against the bundled
  `example-app` and a real Loupe screenshot of the broken-thread state.
- FR-DOCS-20 — Trace-manifest format reference, versioned with the schema.
  `docs/trace-manifest-schema.md` already covered the v4 shape in full; the
  one real gap (never mentioning `trace-manifest.v5beta.json`, which the
  Gate has emitted on every run since v0.4.5) is closed 2026-08-18.
- FR-DOCS-30 — Troubleshooting built from real failure classes, each entry
  citing the incident that taught it. Shipped 2026-08-18 as
  `docs/troubleshooting.md`: seven entries, each citing a real incident
  (`docs/docs-gaps.md`, a CHANGELOG.md version, or a real trial finding) —
  no hypothetical entries.
- FR-DOCS-40 — Every documented behavior cites the registry row(s) it
  documents. Shipped 2026-08-18 as a visible citation line added to each
  DOCS-authored section (README's quickstart, `trace-manifest-schema.md`,
  `docs/troubleshooting.md`'s own intro) pointing back to its `FR-DOCS-NN`
  row in `PRD.md` — distinct from the invisible `@covers` marks, which are
  for the Gate, not the reader. Scoped honestly: this repo's own registry
  only covers the docs room's own founding-era work, not the whole tool's
  behavior (that's governed by `PROMOTION-CONTRACT.md`'s numbered rules,
  which predate this registry and aren't IDs in it) — so this FR's
  citation discipline applies to what this registry actually tracks, not
  a claim that every sentence in every doc now cites something.
