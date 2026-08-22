# The Dig — Level Three Build Handoff v3.0 FROZEN 2026-08-22

For: the SpecAssay room. Receipt by version line. Builds on level two (d7cd42f lineage, generatorVersion 0.2.0). Ruled by Rik 2026-08-22, three choices on record: build it · imports-only first · Monday-timeboxed. The archaeology hard laws stand unchanged: inferred and attested never conflate; the dig writes only its report; anointment is a pull request; NO LLM ever (§0 of level two, standing).

## 0. Timebox and fallback truth

If the regenerated insurance-java sample is not built, verified, and committed by SUNDAY EVENING, STOP — Monday's demo runs on the current proven 56-row sample (d7cd42f) and this level ships post-demo as the product's first "it got better since you saw it." This handoff is upside-only; nothing Monday needs depends on it. The frozen Tally demo build is NOT touched by this work in any case (different repo; the viewer's Proposed Build card already renders candidates when present and "none proposed" when absent — level two's schema discipline means no viewer change is required or permitted).

## 1. The one new capability: PROPOSED BUILD, dug from the test's own imports

For every row carrying a candidateProof (test-derived or table-matched), parse THAT TEST FILE's import declarations and class references. Project-package imports only — framework and stdlib imports (org.junit.*, org.springframework.*, java.*, jakarta.*, com.vaadin.*, etc.) are excluded by package-prefix filter against the repo's own base package (derivable from the source tree; document the derivation). Each surviving import yields a candidate build reference: the imported type's declaration file, resolved to file path (content-search resolution per level two's own fix — one-class-per-file convention makes this reliable in Java) with the import statement's own file:line as provenance.

This is reading a declaration the compiler already enforces, not inference: the test names what it exercises. Statement template per-evidence-kind (standing law): a Proposed Build candidate is a FILE CITATION with provenance ("exercises src/main/java/.../CollectPremium.java — dug from the test's imports, CollectPremiumFeatureTest.java:5"), never prose-ified into a claim about behavior.

## 2. Schema (additive, builder authors the real shape)

Per-row addition: candidateBuild — a LIST (tests often exercise several types): each entry { file, importedType, provenance: { file, line }, basis: "test-imports" }. Basis is first-class from birth (the level-two candidateProof lesson applied in advance — co-change and other future sources will need their own basis values). generatorVersion bumps (0.2.0 → 0.3.0). Regenerate and re-commit the insurance-java sample; the committed sample remains the canonical consumer shape.

## 3. Confidence honesty

Import presence proves the test TOUCHES the type, not that the type IMPLEMENTS the criterion — a test may import helpers, fixtures, builders. State this gap: candidateBuild entries carry no per-entry confidence in v1 (the basis names the method; the gap is documented in the dig's docs and the report's own field docs). Do NOT attempt to rank imports by relevance — that is inference beyond the floor; list them all, cited, and let the human reviewer's eye do what it is good at. If the list for a typical test is noisy in practice (fixture-heavy tests), report that honestly in §5's assessment rather than filtering silently.

## 4. Explicitly OUT

Commit co-change attribution (ruled: follow-up, its own basis value, after imports prove out on real ground). Any viewer work (the ghost viewer and Tally slice already render what the schema provides; design room owns references). Any LLM anything (parked indefinitely, standing). Non-Java import idioms beyond what insurance-java needs — EXCEPT: a dogfood run against specassay or speccost themselves (Python import shape) is SANCTIONED as the second specimen if time permits inside the timebox, satisfying no-heuristic-from-single-specimen; if time does not permit, note the single-specimen status honestly in the sample's provenance and the second specimen becomes the post-demo acceptance test.

## 5. Acceptance: the rerun

Re-dig insurance-java at 0.3.0. Report: how many rows gained candidateBuild entries; typical list length per row (the noise question); a handful of representative entries with their provenance; the re-committed sample's diff shape; and the honest-usefulness paragraph, same test as always — does the Proposed Build card now show a reviewer something a junior engineer's first-pass read would have found, with citations? Then Rik loads the regenerated sample in the ghost viewer and the Tally slice, verifies the three-legged ghost renders sanely, and the timebox closes.

Receipt, then run straight through; tripwires: §0's Sunday-evening stop, and the §5 report.

Please edit this file as we go along; edits after crossing require re-delivery with a version bump.
