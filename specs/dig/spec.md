# Archaeology mode (the no-LLM floor)

Claims registry IDs whose "build" is the real, shipped `specassay dig`
command — once that change has actually landed (real `@covers` mark or a
passing named test, not an anointment). Per
`docs/archaeology-mode-build-handoff-v1-2026-08-20.md` (receipted by
version line before this build): rung (a) of the three-rung ladder only;
rungs (b) local-model and (c) user-supplied-API-key remain out of scope.

- US-DIG-10 — the command exists (`speckit.specassay-check.dig`), proven by `@covers` in `extensions/specassay-check/commands/speckit.specassay-check.dig.md`.
- FR-DIG-10 — `specassay dig` command + the one hard law (no write outside the configured output path, no `--anoint` flag), amended 2026-08-21 for a durable default output location. Shipped 2026-08-20 (amended 2026-08-21), proven by `@covers` in `extensions/specassay-check/scripts/dig.py` and by `extensions/specassay-check/tests/test_dig_no_llm_floor.py`.
  - AC-DIG-10 — proven by `test_AC_DIG_10_dry_run_writes_nothing`, `test_AC_DIG_10_real_run_writes_only_dig_report`, and `test_AC_DIG_10_no_anoint_flag_exists`.
  - AC-DIG-30 — proven by `test_AC_DIG_30_default_out_is_cwd_relative_not_target_relative`. Found running `dig` for real against an external, read-only clone (`github.com/SpecDriven/insurance-java`), where the operator (this session) first pointed the default at a session scratchpad — cleanup-eligible, not durable.
- FR-DIG-20 — dig-report schema (epistemicClass, provenance, confidence, suggestedArea, document-level metadata). Shipped 2026-08-20, proven by `@covers` in `extensions/specassay-check/scripts/dig.py`.
  - AC-DIG-20 — proven by `test_AC_DIG_20_dry_run_prints_counts_by_type_and_source`.
- FR-DIG-30 — README table mining. Shipped 2026-08-22 (`docs/dig-level-two-handoff-v2-2026-08-22.md` §2a), proven by `@covers` in `extensions/specassay-check/scripts/dig.py` (`dig_readme_tables`) and by `extensions/specassay-check/tests/test_dig_no_llm_floor.py`.
  - AC-DIG-60 — proven by `test_AC_DIG_60_table_mining_recovers_spec_scenario_test_table`. Real-target confirmation: re-run against `github.com/SpecDriven/insurance-java` recovered its published 12-spec/17-scenario table completely (29 of 29 table rows, all 17 scenario rows' `candidateProof` resolved to a real test file:line) — see `samples/insurance-java.dig-report.json`.
- FR-DIG-40 — `candidateProof` first-class on every row. Shipped 2026-08-22, proven by `@covers` in `extensions/specassay-check/scripts/dig.py` (`attach_candidate_proof`, `dig_readme_tables`).
  - AC-DIG-40 — proven by `test_AC_DIG_40_same_artifact_for_test_rows` and `test_AC_DIG_40_null_when_no_test_known`.
- FR-DIG-50 — Known-smoke noise labeling. Shipped 2026-08-22, proven by `@covers` in `extensions/specassay-check/scripts/dig.py` (`KNOWN_SMOKE_TESTS`).
  - AC-DIG-50 — proven by `test_AC_DIG_50_known_smoke_test_labeled_low_confidence_with_reason`.
- FR-DIG-60 — `candidateBuild` first-class on every row, dug from the proof test's own project-package imports. Shipped 2026-08-22 (`docs/dig-level-three-handoff-v3-2026-08-22.md`), proven by `@covers` in `extensions/specassay-check/scripts/dig.py` (`attach_candidate_build`, `dig_build_candidates_java`, `dig_build_candidates_python`, `derive_base_package`).
  - AC-DIG-70 — proven by `test_AC_DIG_70_candidate_build_from_java_test_imports`, `test_candidate_build_empty_list_when_no_candidate_proof`, and `test_candidate_build_from_python_test_imports`. Real-target confirmation: re-run against `github.com/SpecDriven/insurance-java` at 0.3.0 held the row count at 56 (unchanged from 0.2.0) and populated `candidateBuild` on 41 of 42 candidateProof-carrying rows (median list length 5; the one empty list is `contextLoads`, the framework smoke test, which imports nothing of the repo's own) — see `samples/insurance-java.dig-report.json`. Second-specimen (Python import shape) sanctioned by handoff Sec.4 dogfooded against `speccost`'s own test suite, confirming the heuristic isn't fitted to Java's single specimen alone.

## Laws (minted from the §2d investigation, 2026-08-22)

Two design principles, ratified alongside the decision to defer the
view-route heuristic itself (see `docs/backlog.md`'s "Pattern candidate:
a view-route heuristic family for `dig`" for the deferred feature).

1. **Statement templates are per-evidence-kind.** A dug statement
   describes what the evidence actually shows — a REST route candidate
   reads "the system accepts GET /path"; a future view-route candidate
   must read "the system presents a view at /path," never the REST
   wording force-fit onto a different evidence kind. Every heuristic that
   ever gets added owns its own template; none inherits another's by
   default.
2. **No heuristic ships from a single specimen.** One real target shows
   the shape of one family member, not the family — building against it
   alone risks a heuristic fitted to that one specimen's idiom rather
   than the general case it's meant to cover. The floor's own deliberate
   avoidance of framework-type knowledge (no heuristic checks what a
   class *extends*, only what it's *shaped like* in text) is itself a
   design principle under this same law, not an oversight: it keeps every
   heuristic honestly declarable as text-pattern matching, with whatever
   verification gap that leaves (a false positive from an unrelated
   annotation of the same name, say) named directly via the row's own
   `confidence` tier rather than silently assumed away.
