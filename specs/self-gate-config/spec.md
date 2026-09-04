# This repo's own Gate work

Claims registry IDs whose "build" is a real, shipped change to this repo's
own governance of itself — `specassay-check-config.yml`, the engine
(`check-traceability.sh`), or its new test suite — once that change has
actually landed (real `@covers` mark or a passing named test, not an
anointment). Anointed backlog is for work not yet started; this spec is
where that same ID lands once it has.

- FR-DOCS-50 — `docs/**`, `README.md`, and `PROMOTION-CONTRACT.md` are back
  in `src_globs` (specassay-check-config.yml itself joined the list too, so
  the config's own `@covers` marks count). Shipped 2026-08-18 in the same
  pass as FR-GATE-40, which is what made restoring them safe.
- FR-GATE-40 — `orphan-covers`/`orphan-test` domain-scoping + code-span/fence
  stripping. Shipped 2026-08-18, proven by `@covers` in
  `check-traceability.sh` and by `extensions/specassay-check/tests/test_gate_40_orphan_scoping.py`.
  - AC-GATE-40 — proven by `test_AC_GATE_40_same_domain_quote_in_inline_span_does_not_orphan`.
  - AC-GATE-41 — proven by `test_AC_GATE_41_own_source_never_self_matches`.
- FR-GATE-50 — manifest emitter dedup on `(id, normpath, line)`. Shipped
  2026-08-18, proven by `@covers` in `check-traceability.sh` and by
  `extensions/specassay-check/tests/test_gate_50_dedupe.py`.
  - AC-GATE-50 — proven by `test_AC_GATE_50_overlapping_src_globs_do_not_double_count`.
- FR-GATE-70 — malformed/bare list-type config keys refuse loudly before
  any scanning, no manifest written. Shipped 2026-08-19, proven by
  `@covers` in `check-traceability.sh` and by
  `extensions/specassay-check/tests/test_gate_70_config_validation.py`,
  including the two real incident configs verbatim.
  - AC-GATE-70a — proven by `test_AC_GATE_70a_inline_array_refuses_before_scanning`.
  - AC-GATE-70b — proven by `test_AC_GATE_70b_bare_key_refuses_before_scanning`.
  - AC-GATE-70c — proven by `test_AC_GATE_70c_absent_key_still_means_none`.
- FR-GATE-30 — `retired`: a genuine fifth status derived only from an
  explicit `**Retires**:` record, never a settable field; v4 freezes at
  four values and moves retired rows to a top-level `retired` list,
  v5beta carries `retired` as a normal fifth row status. Shipped
  2026-08-20, proven by `@covers` in `check-traceability.sh` and by
  `extensions/specassay-check/tests/test_gate_30_retired.py`.
  - AC-GATE-30a — proven by `test_AC_GATE_30a_retired_row_is_first_class_in_v5beta`.
  - AC-GATE-30b — proven by `test_AC_GATE_30b_retired_id_leaves_v4_rows_and_gains_top_level_entry`.
  - AC-GATE-30c — proven by `test_AC_GATE_30c_malformed_retires_no_date_refuses_before_scanning`
    and `test_AC_GATE_30c_malformed_retires_no_id_refuses_before_scanning`.
- FR-GATE-10 — `--matrix`: `coverage.md` + `coverage.svg` re-presenting
  the same run's already-computed data (boundary line written into this
  entry before build: portfolio-snapshot renderer, never a second scan,
  never a second viewer). Shipped 2026-08-22, proven by `@covers` in
  `check-traceability.sh` and `commands/speckit.specassay-check.matrix.md`,
  and by `extensions/specassay-check/tests/test_gate_10_matrix.py`.
  - AC-GATE-10a — proven by `test_AC_GATE_10a_matrix_writes_from_same_run_no_second_scan`.
  - AC-GATE-10b — proven by `test_AC_GATE_10b_family_colors_canonical_order_and_self_dated`
    and `test_AC_GATE_10b_zero_count_status_has_no_bar_sliver`.
  - AC-GATE-10c — proven by `test_AC_GATE_10c_retired_ids_absent_from_matrix_like_v4_rows`.
- FR-GATE-20 — `--portfolio`: `portfolio-snapshot.md` re-presenting the
  same run's already-computed data as `--matrix` (guardrails written into
  this entry before build: names the cold-reader audience explicitly,
  same document-not-viewer boundary as `FR-GATE-10`, "portfolio" scoped
  to this one repo). Shipped 2026-08-22, proven by `@covers` in
  `check-traceability.sh` and `commands/speckit.specassay-check.portfolio.md`,
  and by `extensions/specassay-check/tests/test_gate_20_portfolio.py`.
  - AC-GATE-20a — proven by `test_AC_GATE_20a_portfolio_writes_from_same_run_no_ci_banner`.
  - AC-GATE-20b — proven by `test_AC_GATE_20b_snapshot_names_only_this_repo`.
- FR-GATE-80 — `proofs[]`-population inherits the same execution-verified
  filtering `status_for()`'s own `tested` set already has: when
  `test_results` is configured, a name matching `test_ac_regex` only
  inside a comment (never a real, currently-passing test) no longer
  appears in that ID's `proofs[]`. Shipped 2026-08-22, proven by
  `@covers` in `check-traceability.sh` and by
  `extensions/specassay-check/tests/test_gate_80_proof_filtering.py`.
  - AC-GATE-80 — proven by `test_AC_GATE_80_comment_only_match_excluded_when_test_results_configured`.
- FR-GATE-90 — Parentage: `parent` edges derived from the registry
  document's own heading/section nesting (per-project opt-in,
  `parent_derivation: heading-nesting`), plus a recursive all-rows
  composition rollup. Shipped 2026-08-22, proven by `@covers` in
  `check-traceability.sh` and by
  `extensions/specassay-check/tests/test_gate_90_parentage.py`. Dogfooded
  for real (`specassay-check-config.yml` turns this on): doing so caught
  and fixed a genuine mis-nesting in this repo's own `PRD.md` (several DIG
  ACs sat indented under the wrong FR, invisible while indentation was
  purely cosmetic).
  - AC-GATE-90a — proven by `test_AC_GATE_90a_nested_rows_get_parent_edges`
    and `test_AC_GATE_90a_absence_means_no_edges`.
  - AC-GATE-90b — proven by `test_AC_GATE_90b_rollup_includes_all_depths_not_just_direct_children`.
  - AC-GATE-90c — proven by `test_AC_GATE_90c_rollup_carries_total_alongside_per_status`.
- FR-GATE-100 — Cold-install on-ramp: an empty registry stays green but
  says what to do next (both greenfield and brownfield first mints, as
  runnable commands); the interpreter is detected (`SPECASSAY_PYTHON`,
  `python3`, `python`, each probed for 3.8+) with a one-line install hint
  when none works; the config state is reported at startup every run.
  Shipped 2026-09-03, proven by `@covers` in `check-traceability.sh` and by
  `extensions/specassay-check/tests/test_gate_100_cold_install.py`.
  Verified end to end in a clean `specify init` project the same day:
  empty registry, first mint via the printed command, the expected honest
  refusal, then green.
  - AC-GATE-100a — proven by `test_AC_GATE_100a_empty_registry_stays_green_and_names_the_on_ramp`,
    `test_AC_GATE_100a_populated_registry_keeps_the_plain_ok_line`, and
    `test_AC_GATE_100a_missing_registry_file_points_at_the_on_ramp`.
  - AC-GATE-100b — proven by `test_AC_GATE_100b_falls_back_to_python_when_python3_is_unusable`,
    `test_AC_GATE_100b_no_usable_python_fails_with_one_line_install_hint`, and
    `test_AC_GATE_100b_explicit_override_wins`.
  - AC-GATE-100c — proven by `test_AC_GATE_100c_config_found_is_reported_with_its_path` and
    `test_AC_GATE_100c_config_missing_names_the_file_and_the_copy_command`.
