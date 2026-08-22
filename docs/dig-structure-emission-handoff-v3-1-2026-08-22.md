# The Dig — Structure Emission Handoff v3.1 FROZEN 2026-08-22 (evening)

For: the SpecAssay room. Receipt by version line. Builds on level three (0.3.0 lineage, T918). Ruled by Rik tonight: the dig learns to emit PROPOSED STRUCTURE — the story-map tree it already mined but never wrote down. Standing laws unchanged: no LLM ever; inferred never conflates with attested; the dig writes only its report; statement templates per evidence kind; no heuristic from a single specimen.

## 0. Timebox and fallback

Tonight. If the regenerated sample is not built, verified, and committed by end of evening, STOP — everything downstream falls back to the 0.3.0 sample (d7cd42f lineage) and this ships tomorrow. Nothing Monday needs depends on it; this is the wow's data layer, upside-only.

## 1. Scope — two additive fields, one heuristic, already-mined data

a. STABLE ROW IDS: every row gains rowId (e.g. r001…r056, stable within a report, ordering-derived is fine). Additive; edges need addresses.
b. candidateParent: a LIST per row (schema allows multiple proposals with bases — inferred structure is not bound by the registry's single-parent law; the human picks at anointment). Entry shape: { parentRowId, basis }. TONIGHT EMITS ONE BASIS ONLY: "table-adjacency" — the Spec → Scenario row pairings level two already recovered from the published table. Expected yield on insurance-java: each of the 17 table-derived AC scenarios gains its spec US row as candidateParent; the 12 table US rows and everything else gain none.
c. HONEST ORPHANS: the 25 test-derived ACs and the 2 readme-heading US rows carry empty candidateParent — correctly. Do not stretch the adjacency heuristic to adopt them; that is the class-containment heuristic's job (see §2). An honest partial tree beats a complete guessed one.
d. generatorVersion 0.3.0 → 0.4.0. Regenerate and re-commit samples/insurance-java.dig-report.json as the canonical shape.

## 2. Explicitly OUT (each with its named future)

- TEST-CLASS CONTAINMENT (the class is the feature, methods are its scenarios): the orphan-adopter, deliberately deferred — it mints NEW proposed parent rows from class names and needs the dedup-against-table-parents design question answered first (fuzzy-matching "Collect Premium" to a table spec statement is a ruling, not a default). Candidate for tomorrow if Rik rules it; record as the named next rung.
- README heading nesting as a parent source; any depth beyond two levels; any viewer work (design room owns the reference; the Tally mirror is a separate exception); LLM anything, ever.

## 3. Acceptance: the rerun

Re-dig insurance-java at 0.4.0. Report: edge count and shape (expect ~17 edges into 12 parents); orphan count by source (expect 25 test-derived + 2 readme-heading, stated plainly); confirmation that no row, statement, or prior field changed (purely additive diff); the re-committed sample's diff stat; and the honest-usefulness line — does the emitted tree match the published table's own structure, and would a human recognize it as this product's story map?

Receipt, then run straight through; tripwire is §3's report only.

Please edit this file as we go along; edits after crossing require re-delivery with a version bump.
