# The Dig — Level Two Build Handoff v2.0 FROZEN 2026-08-22

For: the SpecAssay room. Receipt by version line. Builds on the shipped no-LLM floor (2ce3ee9 lineage) and the insurance-java run's own honest assessment — every item below is that assessment's finding converted to work. The archaeology hard law stands unchanged: inferred and attested never conflate; the dig writes only its report; anointment is a pull request.

## 0. Standing strategic ruling (Rik, 2026-08-22): the floor IS the dig

Rungs (b) local-model and (c) user-supplied-API-key are PARKED INDEFINITELY — not sequenced, parked. No LLM ships inside the product. Rationale on record (purpose-on-record rule): the deterministic floor's inferences are themselves auditable — every row cites reproducible evidence, no consent surface exists because nothing leaves the machine, runs are free and offline — and that auditability is brand-aligned for an assay office. LLMs remain room tools (design, build), never runtime dependencies. The anticipated-but-absent --engine flag surface stays a deliberate omission; annotate the parking in the dig's docs so the omission reads as ruled, not forgotten. Revisiting requires a new Rik ruling, not accumulated convenience.

## 1. Schema: candidateProof becomes first-class

Add candidateProof to the row schema: { test, file, line, basis } where basis is "same-artifact" (the provenance test playing its second role — today's only case) or "matched" (a future heuristic pairing an intent from one source with a test found elsewhere). Viewers stop inferring candidacy from provenance.source == "test". Bump generatorVersion; regenerate and re-commit the insurance-java sample; the dig-report schema gets the derive-don't-transcribe treatment the cube got — a generated field reference or, at minimum, the committed sample as the canonical shape consumers build against.

## 2. Heuristics (the assessment's own list)

a. README table mining — the found gap: the floor mines headings only, and insurance-java's richest signal (the hand-maintained Spec → Scenario → Test table) sat unread in table rows. Mine markdown table rows: spec/scenario-shaped columns yield US/AC candidates; a test-shaped column yields candidateProof with basis "matched". On this repo, this heuristic should largely recover the published table — which is also its acceptance test.
b. Humanization splitter — the cosmetic glitch, now guarded territory: split on a capitalized article butting a capitalized word (issuesAPolicy → "issues a policy"; …WithoutAFiledRate… → "without a filed rate"). Extend the existing pinned humanization test with these specimens.
c. Known-smoke noise — contextLoads-class framework smoke tests: keep them (never silently drop a finding) but mark confidence low with a stated reason ("framework smoke test"), so the anointment reviewer's two-second toss is pre-labeled.
d. UI-view route heuristic — the honest zero's scope gap (Vaadin-style server-rendered apps yield no FR candidates): INVESTIGATE-THEN-PROPOSE, not build. One paragraph on what a view-class heuristic would key on and its false-positive risk, before any code. Pause point.

## 3. Acceptance: the rerun

Re-dig insurance-java with level two. Report: row-count deltas by type and source; whether table mining recovered the published spec table (and how completely); splitter specimens fixed; the re-committed sample's diff shape. Same honest-usefulness paragraph as last time — the assessment is the test.

## 4. Out of scope

LLM rungs (parked per §0) · anointment/PR flow · any viewer work (design room owns the ghost reference; the engine ghost layer rides the unification) · committing anything to insurance-java (read-only, as ever).

Receipt, then run the queue; tripwires: §2d's propose-before-build pause, and the §3 report.

Please edit this file as we go along; edits after crossing require re-delivery with a version bump.
