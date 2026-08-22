# Backlog — Anointed (minted on purpose, not yet picked up)

Anointed backlog = a registry ID whose **only** carrier is an open `- [ ]`
TODO. It is deliberately *not* in any spec, has no `@covers` mark, and no
`test_AC_*` proof. The open TODO below is what proves the intent is minted
and keeps Gate 2 from flagging it as drift. Pick one up end-to-end and watch
the status flip from `backlog` → `proven`.

Founding pass, 2026-08-18 (docs room, design-room ruling): every row in
`PRD.md` lands here at once, on purpose — no row is minted `proven` by
declaration.

## Session resume, 2026-08-22 (read this + PRD.md; nothing else should be needed)

Verified against real state before writing, not carried over from memory:

- **HEAD**: `f96559b` — 12 commits ahead of the published `v0.4.12` tag
  (`FR-GATE-30`/`FR-GATE-90` mint/`FR-DIG-*`/`T905`/`T906`/`T914` all
  landed since that tag; no new release has been cut for any of it yet).
- **v0.4.12 community submission**, filed 2026-08-21, checked 2026-08-22:
  extension issue #4252 → PR #4254 **MERGED**. Preset #4253 → PR #4256
  **open**, bundle #4255 → PR #4257 **open**, both awaiting maintainer
  merge — nothing further to do on our side, just watch.
- **`specassay.com`**: the hero rewrite in the standalone `specassay.com`
  repo (`/Users/spudnik/specassay.com`) is orphaned — that repo was never
  the real deploy source. The actual production fix (Install CTA pinned
  to the `v0.4.12` release) shipped in `dryfoos-sites` (`5a0d718`) and is
  live. Nothing pending here.
- **Known, accepted, non-blocking diagnostic**: every Gate run on this
  repo reports `uncovered proof: AC-ZK9Q-01 has a passing test...`. This
  is `extensions/specassay-check/tests/test_dig_no_llm_floor.py`'s own
  fixture text (a deliberately fictional ID, chosen specifically to avoid
  colliding with a real one) being read as a citation by this repo's own
  Gate — the exact `FR-GATE-80`-class defect, on a field (`uncovered-proof`)
  that doesn't yet have `orphan-covers`/`orphan-test`'s domain-scoping.
  Not a bug to fix reflexively; not yet re-minted as its own row either.
- **`docs/backlog.md`**: "Pattern candidate: a view-route heuristic family
  for `dig`" — investigated (§2d of the dig-level-two handoff), deferred
  on purpose. Trigger: a second real, non-REST, server-rendered target.
- **`samples/dig-ghost-viewer-reference.html`**: untracked, not created by
  this room, not committed — the handoff's own §4 names viewer work as
  design-room scope. Leave it alone.
- **Per-task status**: `T900` open on purpose (structural gap, no
  vocabulary yet for "proven by trial"); `T905`/`T906`/`T907`/`T914`/`T916`/
  `T917` closed this session; `T908` open backlog, low urgency; `T912`
  open, blocked on its own design question (author-declared vs. inferred
  `provenVia`); **`T915` in progress, starting now** (see below).

**Build reminders for `T915` (parentage), restated so nothing re-litigates:**
parent edges **derive** from the registry document's own heading/section
nesting at emit time (per-project `parent_derivation` config) — never
authored, never inferred by a viewer. Document structure yields a tree by
construction: single-parent v1. Rollup basis is **recursive over ALL
rows**, ratified — a non-leaf's own status counts join its parent's
rollup alongside its descendants', so a mid-tier `GAP`/`backlog` can't
vanish from an ancestor's card; labels name the basis ("N rows"). Cite the
Q2 interlock directly in the rows: the recursion is cycle-safe only
because single-parent holds — anyone relaxing single-parent later must
notice they're touching rollup safety. Schema note: parent edges are
**additive optional fields** — no `formatVersion` bump — but name them
first-class in `trace-manifest-schema.md`'s v5beta section. The Loupe-side
COMPOSITION card stays out of scope, held for the viewer room.

- [ ] T900 Prove AC-DOCS-10 mechanically — **Carries**: AC-DOCS-10, US-DOCS-10 (US-DOCS-10 already reads `proven` via a real `@covers` mark and `specs/docs-authored/spec.md`; named here too only so exact-set has a task-side mention — it is not what's carrying it). Real cold-agent trial run and documented 2026-08-19 (`docs/testing/completed/evidence-cold-agent-trial-observed-2026-08-19.md`, real Gate output, independently reverified) — that's why this reads `tracked-debt`, not `backlog`. Stays open on purpose: an AC only reaches `proven` via a *named test* (Rule 6), and field-trial evidence has no test to name — the registry currently has no vocabulary for "proven by a real, documented trial" the way it does for `retired` being proposed for withdrawn intent (`FR-GATE-30`). Closes when either a repeatable automated cold-install check exists, or the registry gains real attestation vocabulary for this shape of proof — not before, and not by closing this task without one.
- [x] T901 Write FR-DOCS-10: quickstart (install, config, first check, first honest red) — **Carries**: FR-DOCS-10
- [x] T902 Write FR-DOCS-20: trace-manifest format reference, versioned with the schema — **Carries**: FR-DOCS-20
- [x] T903 Write FR-DOCS-30: troubleshooting from real failure classes — **Carries**: FR-DOCS-30
- [x] T904 Cite the registry row(s) from every documented behavior — **Carries**: FR-DOCS-40
- [x] T905 Ship `--matrix`: coverage table + SVG summary emission — **Carries**: FR-GATE-10, AC-GATE-10a, AC-GATE-10b, AC-GATE-10c. Boundary line written into `FR-GATE-10` before build, per design-room instruction: CI-runnable, no browser, embeds in a README, never drifts into a second viewer. New command `speckit.specassay-check.matrix`. Modeled on HomesFlow's own bespoke `--matrix` mode for structure (summary table, per-type sections, generated-file banner), not its pre-canon colors — feature parity here is that fork's own named retirement trigger, alongside `T906`.
- [x] T906 Ship portfolio-snapshot mode — **Carries**: FR-GATE-20, AC-GATE-20a, AC-GATE-20b. Three guardrails ratified and written into `FR-GATE-20` before build: name the audience (cold reader, zero context), same boundary line as `--matrix` (document, never a viewer), and "portfolio" scoped explicitly to this repo's own whole thread (single-repo) — cross-repo aggregation fenced out, mints as a new row in a future federation era if it's ever needed. New command `speckit.specassay-check.portfolio`; `coverage.svg` is a shared asset between `--matrix` and `--portfolio`, rendered once regardless of which flags are passed. HomesFlow's own bespoke `--matrix`/`--refresh` modes are this fork's own named retirement trigger, alongside `T905`.
- [x] T907 Ship the `retired` terminal state — **Carries**: FR-GATE-30, AC-GATE-30a, AC-GATE-30b, AC-GATE-30c. **Addition, 2026-08-20 (design room):** when this lands, HomesFlow's own eventual retirement record for its bespoke `scripts/check-traceability.sh` (already named: retires once `T905`/`T906`'s matrix/portfolio-snapshot modes ship, giving the vendored engine feature parity) should pin the exact last-active commit hash plus a one-line reactivation procedure (branch/tag name pointing at that commit, invocation command) — same discipline the `clew-era-final` tag already established for the older clewseau-gate fork. Goal: resurrecting the old script later, for a deliberate comparison or test run, is a documented single command, not git archaeology performed from memory months later. Cheap to add while the retirement record is already being written; costly to reconstruct later if it isn't. This is HomesFlow's own future action, informed here so the requirement isn't lost between now and whenever `T905`–`T907` actually close.
- [ ] T908 Backfill `@covers` marks across specassay's own existing extension/preset behavior — **Carries**: FR-SELF-10 (anointed backlog)
- [x] T909 Give `orphan-covers` domain scoping (fenced code blocks, doc files, the checker's own comments are not live marks) — **Carries**: FR-GATE-40, AC-GATE-40, AC-GATE-41
- [x] T910 Restore `docs/**` to `src_globs` once FR-GATE-40 ships — **Carries**: FR-DOCS-50
- [x] T911 Dedupe manifest implementations/proofs on (id, normpath, line) — **Carries**: FR-GATE-50, AC-GATE-50
- [ ] T912 Rule on how `provenVia` gets populated (author-declared vs. inferred), then ship it — **Carries**: FR-GATE-60 (anointed backlog)
- [x] T913 Refuse loudly on a malformed or bare list-type config key, before any scanning — **Carries**: FR-GATE-70, AC-GATE-70a, AC-GATE-70b, AC-GATE-70c
- [x] T914 Filter `proofs[]`-population the way `status_for()`'s `tested` set already is: no comment-only text match counts, and when `test_results` is configured the passing-testcase filter applies to `proof_by` too, not just `test_acs.txt` — **Carries**: FR-GATE-80, AC-GATE-80. Fixed at the point `proof_by` is populated: when `execution_verified` is true, an entry is kept only if its ID is also in the (junit-filtered) `tested` set — a no-op when `test_results` isn't configured, so unfiltered projects see no behavior change. **Priority ruling, 2026-08-20 (design room):** sequenced behind `T905`/`T906`/`T907`, not bumped to the end of the list — pull next once those three close. Escalation was requested at three citing instances (`AC-WALK-10`, `FR-TOUCH-60`, and this same mechanism independently reconfirmed from inside SpecAssay's own boundary) and is agreed well-scoped and cheap when picked up, but `T905`–`T907` carry a harder claim: `T907`/`FR-GATE-30` is HomesFlow's own `T900`'s literal unblock condition (a real room's task cannot close without it), and `T905`/`T906`'s matrix/portfolio-snapshot modes are the named trigger for HomesFlow retiring its own bespoke gate script, a compounding cost every day they don't ship. `T914` is a correctness/clarity fix — the derived statuses have been right the whole time; only the displayed proof evidence occasionally shows a stale or ghost name. Nobody is blocked by it, unlike the three ahead of it. Sequence by blocking cost, not list position.
- [x] T915 Derive `parent` edges from registry-document heading/section nesting at emit time, plus a recursive all-rows composition rollup per row with descendants — **Carries**: FR-GATE-90, AC-GATE-90a, AC-GATE-90b, AC-GATE-90c. Built after DIG and `T905`/`T906`, both conditions satisfied. Dogfooded for real (`parent_derivation: heading-nesting` in this repo's own config) — caught and fixed a genuine mis-nesting in `PRD.md`'s own DIG section (several ACs indented under the wrong FR, invisible while indentation was purely cosmetic before this feature gave it meaning). Additive/optional fields, no `formatVersion` bump, named first-class in `trace-manifest-schema.md`'s v5beta section. The Loupe-side COMPOSITION card stays out of scope, held for the viewer room.
- [x] T916 Ship `specassay dig` (archaeology mode, no-LLM floor) — **Carries**: US-DIG-10, FR-DIG-10, FR-DIG-20, AC-DIG-10, AC-DIG-20, AC-DIG-30. Per `docs/archaeology-mode-build-handoff-v1-2026-08-20.md` (receipted by version line 2026-08-20 before this build). Rungs (b) local-model and (c) user-supplied-API-key, the anointment/PR-generation flow, Tally-side ghost-layer rendering, and commit-history row-minting are all explicitly deferred per the handoff §6 — not built, not silently dropped. Real-target run against `github.com/SpecDriven/insurance-java` (handoff §7 step 5, permission on record in the handoff itself) and the fixture dry-run/no-write confirmation (§7 step 4) both done, reported. **Amendment, 2026-08-21:** the real insurance-java run itself surfaced a defect in this task's own close condition — the default output location depended on the scanned target, and this session had improvised a session-scratch location as the workaround, which is cleanup-eligible, not durable. Fixed: default is now the operator's own current working directory, never the target path, never scratch. AC-DIG-30 mint + fix + regression test closes this same task, not a new one — the citing incident happened while this task's own report-back was still open.
- [x] T917 Ship dig level two (`docs/dig-level-two-handoff-v2-2026-08-22.md`, receipted by version line before this build) — **Carries**: FR-DIG-30, FR-DIG-40, FR-DIG-50, AC-DIG-40, AC-DIG-50, AC-DIG-60. Standing strategic ruling on record in the handoff §0: rungs (b)/(c) are PARKED INDEFINITELY, not sequenced — the deterministic floor IS the dig, no LLM ships inside the product, the `--engine` flag surface stays a deliberate, documented omission. §2d (a UI-view route heuristic) is investigate-then-propose per the handoff, not built — a paragraph, not code, held for a separate ruling. §3's rerun against `github.com/SpecDriven/insurance-java` (row-count deltas, full-table-recovery confirmation, splitter specimens, re-committed sample diff, honest-usefulness paragraph) reported alongside this close.
