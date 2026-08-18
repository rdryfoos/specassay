# Docs-gaps list

Running log for the docs room (opened 2026-08-18). Working method: the
room's own cold start is the instrument — every question about SpecAssay
that can't be answered from the repo alone is a gap, logged here before
it's resolved. This is FR-DOCS-30's raw material: each troubleshooting
entry it eventually produces should cite the incident here that taught it.

Format per entry: what broke, how it was found, resolution (or `open` if
still unresolved), and the commit that closed it.

## Resolved

1. **Two dead links in the public quickstart.** `README.md`'s "Does it work
   cold? / Want to test it on real work?" sentence linked
   `./docs/evidence-cold-agent-trial.md` and `./docs/real-work-test.md`;
   neither existed. Found by cold-reading `README.md` top to bottom as a
   cold installer would. Real files: `docs/testing/completed/
   evidence-cold-agent-trial.md` (itself moved out of a literally-named
   `docs/testing/*completed/` directory) and `docs/testing/4-real-work-test.md`.
   Resolved: commit `de6995b` (docs: fix two dead README quickstart links).

## Open

1. **`orphan-covers` has no domain-scoping, unlike `orphan-spec`/`orphan-task`.**
   Founding this repo's own registry (`PRD.md`, 2026-08-18) with `docs/**`
   in `src_globs` failed the Gate immediately — not on real drift, but on
   `docs/testing/*.md` trial write-ups quoting other projects' `@covers`
   lines as teaching examples (`AC-HOME-15`, `FR-HOME-04`, `AC-FIX-01`,
   etc.), plus a coverage-regex false match inside `check-traceability.sh`'s
   own comment. The spec/task orphan checks already have `is_local_domain()`
   to tell a citation apart from a real claim (see the script's own
   comment at the top of that function); `orphan-covers`/`orphan-test`
   never got the same scoping. Worked around for founding by narrowing
   `src_globs` to `extensions/**` + `presets/**` only (excludes `docs/**`
   for now) and rewording the one colliding comment
   (`extensions/specassay-check/scripts/check-traceability.sh`) so it
   doesn't literally match `covers_regex`. Not fixed at the engine level —
   that's a real gap in the check itself, out of scope for a docs-room
   founding pass. `docs/**` re-enters `src_globs` once FR-DOCS-10 starts
   writing doc files that need real `@covers` marks of their own, at which
   point this either needs the engine fix or a narrower docs glob.
