# DOCS room — content that has actually shipped

Claims DOCS-area registry IDs once their content has actually been written
and carries a real `@covers` mark, the same way `specs/self-gate-config/spec.md`
claims this repo's own engine work. Anointed backlog is for content not yet
written; this spec is where the ID lands once it has.

- FR-DOCS-10 — Quickstart (install, config, first check, first honest red).
  Shipped 2026-08-18 in `README.md`'s "Install (catalog path)" section,
  including the "See a real refusal" walkthrough against the bundled
  `example-app` and a real Loupe screenshot of the broken-thread state.
- FR-DOCS-20 — Trace-manifest format reference, versioned with the schema.
  `docs/trace-manifest-schema.md` already covered the v4 shape in full; the
  one real gap (never mentioning `trace-manifest.v5beta.json`, which the
  Gate has emitted on every run since v0.4.5) is closed 2026-08-18.
