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
