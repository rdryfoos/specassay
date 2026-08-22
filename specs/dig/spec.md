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
