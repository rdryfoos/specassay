# Backlog — Anointed (minted on purpose, not yet picked up)

Anointed backlog = a registry ID whose **only** carrier is an open `- [ ]`
TODO. It is deliberately *not* in any spec, has no `@covers` mark, and no
`test_AC_*` proof. The open TODO below is what proves the intent is minted
and keeps Gate 2 from flagging it as drift. Pick one up end-to-end and watch
the status flip from `backlog` → `proven`.

Founding pass, 2026-08-18 (docs room, design-room ruling): every row in
`PRD.md` lands here at once, on purpose — no row is minted `proven` by
declaration.

- [ ] T900 Prove AC-DOCS-10 mechanically — **Carries**: AC-DOCS-10, US-DOCS-10 (US-DOCS-10 already reads `proven` via a real `@covers` mark and `specs/docs-authored/spec.md`; named here too only so exact-set has a task-side mention — it is not what's carrying it). Real cold-agent trial run and documented 2026-08-19 (`docs/testing/completed/evidence-cold-agent-trial-observed-2026-08-19.md`, real Gate output, independently reverified) — that's why this reads `tracked-debt`, not `backlog`. Stays open on purpose: an AC only reaches `proven` via a *named test* (Rule 6), and field-trial evidence has no test to name — the registry currently has no vocabulary for "proven by a real, documented trial" the way it does for `retired` being proposed for withdrawn intent (`FR-GATE-30`). Closes when either a repeatable automated cold-install check exists, or the registry gains real attestation vocabulary for this shape of proof — not before, and not by closing this task without one.
- [x] T901 Write FR-DOCS-10: quickstart (install, config, first check, first honest red) — **Carries**: FR-DOCS-10
- [x] T902 Write FR-DOCS-20: trace-manifest format reference, versioned with the schema — **Carries**: FR-DOCS-20
- [x] T903 Write FR-DOCS-30: troubleshooting from real failure classes — **Carries**: FR-DOCS-30
- [x] T904 Cite the registry row(s) from every documented behavior — **Carries**: FR-DOCS-40
- [ ] T905 Ship `--matrix`: coverage table + SVG summary emission — **Carries**: FR-GATE-10 (anointed backlog)
- [ ] T906 Ship portfolio-snapshot mode — **Carries**: FR-GATE-20 (anointed backlog)
- [ ] T907 Ship the `retired` terminal state — **Carries**: FR-GATE-30 (anointed backlog)
- [ ] T908 Backfill `@covers` marks across specassay's own existing extension/preset behavior — **Carries**: FR-SELF-10 (anointed backlog)
- [x] T909 Give `orphan-covers` domain scoping (fenced code blocks, doc files, the checker's own comments are not live marks) — **Carries**: FR-GATE-40, AC-GATE-40, AC-GATE-41
- [x] T910 Restore `docs/**` to `src_globs` once FR-GATE-40 ships — **Carries**: FR-DOCS-50
- [x] T911 Dedupe manifest implementations/proofs on (id, normpath, line) — **Carries**: FR-GATE-50, AC-GATE-50
- [ ] T912 Rule on how `provenVia` gets populated (author-declared vs. inferred), then ship it — **Carries**: FR-GATE-60 (anointed backlog)
- [x] T913 Refuse loudly on a malformed or bare list-type config key, before any scanning — **Carries**: FR-GATE-70, AC-GATE-70a, AC-GATE-70b, AC-GATE-70c
- [ ] T914 Filter `proofs[]`-population the way `status_for()`'s `tested` set already is: no comment-only text match counts, and when `test_results` is configured the passing-testcase filter applies to `proof_by` too, not just `test_acs.txt` — **Carries**: FR-GATE-80, AC-GATE-80 (anointed backlog)
