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

- **HEAD**: `0fa8dd6` — `T919` (dig structure emission, `rowId` +
  table-adjacency `candidateParent`) shipped. Prior HEAD was `6ad4cab` —
  `T918` (dig level three, `candidateBuild` dug from the proof test's own
  project-package imports). Before that, `3625978` — `T915`
  (`FR-GATE-90`, parentage: derived parent edges + recursive all-rows
  rollup), closing the queue `T907`→`T905`→`T906`→`T914`→`T915`. Real
  dogfooding bug found and fixed in that same pass: enabling
  `parent_derivation: heading-nesting` against this repo's own `PRD.md`
  exposed several DIG-section ACs mis-nested under the wrong FR (invisible
  while indentation was purely cosmetic); fixed directly. 68+ tests
  passing, including 7 new `test_gate_90_parentage.py` cases with
  verified-real-teeth (reverted the rollup to direct-children-only,
  confirmed the multi-depth test fails, restored the fix).
- **v0.4.12 community submission**, filed 2026-08-21, checked 2026-08-22:
  extension issue #4252 → PR #4254 **MERGED**. Preset #4253 → PR #4256
  **open**, bundle #4255 → PR #4257 **open**, both awaiting maintainer
  merge — nothing further to do on our side, just watch.
- **`specassay.com` messaging surgery** (`docs/specassay-messaging-surgery-v1-2026-08-22.md`,
  executed and closed this session): hero rewritten (Rik's H1/subline cut,
  braid animation retired entirely with `thread.js`, replaced by a real
  Thread Report screenshot from PR #5 linking to `/thread-report`), page
  reordered to the ratified running order (no-overhead beat, dig-on-ramp,
  machinery, pedigree), `EDITING-CANON.md` append-only commit records the
  hero vocabulary law. Both landed in `dryfoos-sites`:
  `04588a3` (canon append), `7959f67` (the surgery deploy, already pushed
  and live).
  **Complication resolved**: `7959f67` was accidentally bundled with
  unrelated in-flight Tally work (`FR-GHOST-60`/`FR-GHOST-70`, swept in by
  that repo's own sync automation between staging and commit, which then
  pushed it before the mistake was caught). Per Rik's ruling, left as-is —
  no history rewrite, no force-push on a shared, already-deployed repo.
  Annotated in `dryfoos-sites/NOTES.md` as `e82d491`; confirmed on
  `origin/main` as of this session (pushed, either by the sync automation
  or carried along by this session's own later, narrowly-granted push).
  **`dryfoos-sites` §2 resolution upgrade, 2026-08-22 (later same day,
  fresh narrow grant, one commit, expired on push)**: native-resolution
  Thread Report captures — hero image recropped from Rik's real capture
  (`docs/images/ThreadReport.png`), the complete capture now leads
  `/thread-report`, eyebrow kept (not retired) with the disposition map's
  RETIRE call marked superseded in `EDITING-CANON.md`, one-word polish
  applied ("...for your codebase" → "...for your specs", Rik-confirmed).
  Shipped as `c264b3a`, browser-verified locally before commit, pushed.
  Grant expired on push, per its own terms; no further `dryfoos-sites`
  access without a fresh, explicit grant.
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
  vocabulary yet for "proven by trial"); `T905`/`T906`/`T907`/`T914`/`T915`/
  `T916`/`T917`/`T918`/`T919` all closed; `T908` open backlog, low urgency;
  `T912` open, blocked on its own design question (author-declared vs.
  inferred `provenVia`).
- **`T918`/`T919` (dig level three + structure emission) both closed this
  session** — see their own task lines above for the full acceptance
  reports. `samples/insurance-java.dig-report.json` at generatorVersion
  0.4.0 is the canonical consumer shape now. §5's ghost-viewer render
  check (level three's own closing step, previously logged as Rik's) was
  also done this session: real 0.3.0 sample loaded into
  `samples/dig-ghost-viewer-reference.html` via its file input, correct
  counts/provenance/click-through, zero console errors — see `T918`'s own
  line. The 0.4.0 re-dig (structure emission) has not yet had its own
  ghost-viewer pass; the viewer doesn't render `candidateParent` at all
  (out of scope per both handoffs — design room owns viewer work), so
  there is nothing there to re-check visually; the acceptance report's own
  field-by-field diff is this task's proof instead.
- **Next expected**: test-class containment (the dig's orphan-adopter,
  named in the structure-emission handoff §2) is the next rung, pending a
  Rik ruling on its dedup-against-table-parents design question — not
  sequenced yet. The view-route heuristic (`docs/backlog.md`) stays
  deferred pending a second real, non-REST, server-rendered target, per
  level two's own §2d ruling.

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
- [ ] T921 Ship dig v-next: a docs read that is complete or says it is not, doc-derived rows with a reason, and a human-driven path from a report row to a first minted ID — **Carries**: FR-DIG-80, FR-DIG-90, FR-DIG-100 (anointed backlog). Minted 2026-09-04 from the v0.4.13 release commission's dig verdict, which recommended the manual mint-first-ID on-ramp over `dig` for a docs-heavy brownfield stranger for exactly these three reasons; the verdict and its receipts went to that tester verbatim. **Ruling, 2026-09-04 (Rik), closing FR-DIG-100's design question:** a dug-then-minted line records its origin in the intent PR and the merge commit, never in the registry row. Origin is a fact of the mint event, not a property of the promise, so the minted line is indistinguishable from a hand-minted one and the provenance lives where the mint happened (the `mint-id.sh` reminder to state the coverage basis in the mint commit is already the right place for it). Not sequenced: FR-DIG-80/90 are cheap once anyone reopens `dig.py`, and FR-DIG-100 is now buildable without a further ruling. Test-class containment (the orphan-adopter named in `T919`) remains the other pending dig rung.
- [x] T913 Refuse loudly on a malformed or bare list-type config key, before any scanning — **Carries**: FR-GATE-70, AC-GATE-70a, AC-GATE-70b, AC-GATE-70c
- [x] T914 Filter `proofs[]`-population the way `status_for()`'s `tested` set already is: no comment-only text match counts, and when `test_results` is configured the passing-testcase filter applies to `proof_by` too, not just `test_acs.txt` — **Carries**: FR-GATE-80, AC-GATE-80. Fixed at the point `proof_by` is populated: when `execution_verified` is true, an entry is kept only if its ID is also in the (junit-filtered) `tested` set — a no-op when `test_results` isn't configured, so unfiltered projects see no behavior change. **Priority ruling, 2026-08-20 (design room):** sequenced behind `T905`/`T906`/`T907`, not bumped to the end of the list — pull next once those three close. Escalation was requested at three citing instances (`AC-WALK-10`, `FR-TOUCH-60`, and this same mechanism independently reconfirmed from inside SpecAssay's own boundary) and is agreed well-scoped and cheap when picked up, but `T905`–`T907` carry a harder claim: `T907`/`FR-GATE-30` is HomesFlow's own `T900`'s literal unblock condition (a real room's task cannot close without it), and `T905`/`T906`'s matrix/portfolio-snapshot modes are the named trigger for HomesFlow retiring its own bespoke gate script, a compounding cost every day they don't ship. `T914` is a correctness/clarity fix — the derived statuses have been right the whole time; only the displayed proof evidence occasionally shows a stale or ghost name. Nobody is blocked by it, unlike the three ahead of it. Sequence by blocking cost, not list position.
- [x] T915 Derive `parent` edges from registry-document heading/section nesting at emit time, plus a recursive all-rows composition rollup per row with descendants — **Carries**: FR-GATE-90, AC-GATE-90a, AC-GATE-90b, AC-GATE-90c. Built after DIG and `T905`/`T906`, both conditions satisfied. Dogfooded for real (`parent_derivation: heading-nesting` in this repo's own config) — caught and fixed a genuine mis-nesting in `PRD.md`'s own DIG section (several ACs indented under the wrong FR, invisible while indentation was purely cosmetic before this feature gave it meaning). Additive/optional fields, no `formatVersion` bump, named first-class in `trace-manifest-schema.md`'s v5beta section. The Loupe-side COMPOSITION card stays out of scope, held for the viewer room.
- [x] T916 Ship `specassay dig` (archaeology mode, no-LLM floor) — **Carries**: US-DIG-10, FR-DIG-10, FR-DIG-20, AC-DIG-10, AC-DIG-20, AC-DIG-30. Per `docs/archaeology-mode-build-handoff-v1-2026-08-20.md` (receipted by version line 2026-08-20 before this build). Rungs (b) local-model and (c) user-supplied-API-key, the anointment/PR-generation flow, Tally-side ghost-layer rendering, and commit-history row-minting are all explicitly deferred per the handoff §6 — not built, not silently dropped. Real-target run against `github.com/SpecDriven/insurance-java` (handoff §7 step 5, permission on record in the handoff itself) and the fixture dry-run/no-write confirmation (§7 step 4) both done, reported. **Amendment, 2026-08-21:** the real insurance-java run itself surfaced a defect in this task's own close condition — the default output location depended on the scanned target, and this session had improvised a session-scratch location as the workaround, which is cleanup-eligible, not durable. Fixed: default is now the operator's own current working directory, never the target path, never scratch. AC-DIG-30 mint + fix + regression test closes this same task, not a new one — the citing incident happened while this task's own report-back was still open.
- [x] T917 Ship dig level two (`docs/dig-level-two-handoff-v2-2026-08-22.md`, receipted by version line before this build) — **Carries**: FR-DIG-30, FR-DIG-40, FR-DIG-50, AC-DIG-40, AC-DIG-50, AC-DIG-60. Standing strategic ruling on record in the handoff §0: rungs (b)/(c) are PARKED INDEFINITELY, not sequenced — the deterministic floor IS the dig, no LLM ships inside the product, the `--engine` flag surface stays a deliberate, documented omission. §2d (a UI-view route heuristic) is investigate-then-propose per the handoff, not built — a paragraph, not code, held for a separate ruling. §3's rerun against `github.com/SpecDriven/insurance-java` (row-count deltas, full-table-recovery confirmation, splitter specimens, re-committed sample diff, honest-usefulness paragraph) reported alongside this close.
- [x] T918 Ship dig level three (`docs/dig-level-three-handoff-v3-2026-08-22.md`, receipted by version line before this build) — **Carries**: FR-DIG-60, AC-DIG-70. `candidateBuild` first-class on every candidateProof-carrying row: the proof test's own project-package imports, package-prefix-filtered against a base package derived from the source tree itself (`derive_base_package`, longest common package-declaration prefix — documented, not hardcoded), each surviving import resolved to a real declaration file. Statement-template law from `specs/dig/spec.md` respected: a candidateBuild entry is a file citation with import-line provenance, never prose-ified into a behavior claim. §5's rerun against `github.com/SpecDriven/insurance-java` at 0.3.0 held row count at 56 (unchanged from 0.2.0 — additive schema only), 41 of 42 candidateProof-carrying rows gained candidateBuild entries (median list length 5; the lone empty list is `contextLoads`, importing nothing of the repo's own), ~19% of entries are fixture/base-class noise (`SpecTest`, `PolicyFixtures`) against ~81% real domain types — the noise question the handoff's §3 asked for, answered honestly rather than filtered silently. §4's sanctioned second specimen (Python import shape) dogfooded against `speccost`'s own test suite same session, not deferred: 187 of 190 rows gained entries, confirming the heuristic isn't fitted to Java's single specimen alone. Multi-line parenthesized Python imports (`from x import (\n  A,\n  B,\n)`) are a named, documented gap — resolution is skipped for those, not guessed at. Post-close, loaded the regenerated sample into `samples/dig-ghost-viewer-reference.html` (the design room's own reference viewer) and confirmed it renders sanely: correct provenance line, correct row/type/source counts, click-through descent panel populates real statement/confidence/area/provenance for every node tried, zero console errors.
- [x] T919 Ship dig structure emission (`docs/dig-structure-emission-handoff-v3-1-2026-08-22.md`, receipted by version line before this build) — **Carries**: FR-DIG-70, AC-DIG-80. Two additive fields on every row: `rowId` (stable, ordering-derived, `assign_row_ids`) and `candidateParent` (a LIST — inferred structure isn't bound by the registry's single-parent law, the human picks at anointment). Tonight emits exactly one basis, `"table-adjacency"`: `dig_readme_tables` now marks each scenario row with a reference to its own physical table row's spec row (`_parentCandidates`), resolved to a real `rowId` by `attach_candidate_parent` once every row has one. §3's rerun against `github.com/SpecDriven/insurance-java` at 0.4.0 held row count at 56, confirmed purely additive by direct field-by-field comparison against the 0.3.0 sample (every prior value on every row byte-identical, only `rowId`/`candidateParent` added), emitted 17 edges into 12 distinct parents matching the published table exactly, and left 39 honest orphans (25 test-derived ACs, 2 readme-heading USs, the 12 table spec/US rows themselves, which correctly propose no parent for a row that IS a spec). Test-class containment (the orphan-adopter that would shrink the 25-row test orphan pile) is explicitly deferred per handoff §2, pending a Rik ruling on its dedup-against-table-parents question — named as the next rung, not silently dropped.
- [x] T920 Ship the cold-install on-ramp (empty-registry words, interpreter detection, config self-report) — **Carries**: FR-GATE-100, AC-GATE-100a, AC-GATE-100b, AC-GATE-100c. Commissioned 2026-09-03 from the first Windows cold-install findings on record (senior engineer, Git Bash, no Spec Kit experience, brownfield repo with specs under `docs/**`). Exit codes unchanged on every path that already existed (empty registry still 0); the one new exit is 2 for "no usable Python 3", which previously died as `python3: command not found` at the first `record_fail`. Docs in the same pass: the extension README rewritten for a user who just installed (dev notes moved to `DEVELOPING.md`), the root README gained a "Before you install" section (Spec Kit pointer, the three-install dependency chain, supported platforms with Windows stated as bash-only), the "if config wasn't scaffolded" sentence now points at the script's own startup report, and two troubleshooting entries cite this incident. Verified in a clean `specify init` project: install scaffolds the config, an empty registry prints the on-ramp, the printed mint command works, the next run refuses exactly as the on-ramp says, and a spec mention plus one open Carries line turns it green.
