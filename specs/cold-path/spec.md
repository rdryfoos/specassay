# The cold path

A stranger with an empty repository reaches a Thread Report on a pull request
using the standard Spec Kit workflow and nothing else. This spec claims the COLD
rows as each one ships; the family was minted 2026-10-02 from a reproduction of
the 2026-09-26 cold-path ledger, one gap per row and one pull request per gap.

- US-COLD-10 — The outcome this family serves. Claimed here because every row below
  is a step of it, and answered by the end-to-end proof in `FR-COLD-40`: it is
  `proven` by `test_the_cold_path_needs_no_plumbing`, which performs the whole path
  rather than asserting that it is possible.
- FR-COLD-10 — The install path never leaves a reader holding half the tool.
  Shipped: `presets/specassay/preset.yml` declares `specassay-check` under
  `requires.extensions`, and the three documents a stranger reads first name the
  one line that brings the Gate. Proven by
  `tests/test_cold_path.py`.
  - AC-COLD-10a — proven by `test_AC_COLD_10a_the_preset_declares_the_extension_dependency`.
  - AC-COLD-10b — proven by `test_AC_COLD_10b_the_three_front_doors_name_the_bundle_line`.
- FR-COLD-20 — The bundle ships a registry a stranger can start from, with the
  grammar beside it. Shipped:
  `extensions/specassay-check/templates/registry-seed.md`, written into place by
  `mint-id.sh --init`; the mint prints the whole line to paste and carries the
  Authorship mark. Proven by
  `extensions/specassay-check/tests/test_cold_20_seed_and_mint.py`.
  - AC-COLD-20a — proven by `test_AC_COLD_20a_init_writes_the_seed_and_refuses_to_overwrite`.
  - AC-COLD-20b — proven by `test_AC_COLD_20b_authorship_rides_on_the_minted_line`
    and `test_AC_COLD_20b_a_fifth_authorship_value_is_refused`.
  - AC-COLD-20c — proven by `test_AC_COLD_20c_the_line_to_paste_is_printed_and_the_id_stands_alone`.
  - AC-COLD-20d — proven by `test_AC_COLD_20d_the_seed_states_the_grammar_and_gates_green`.
- FR-COLD-30 — The bundle ships the CI that posts the Thread Report, and one
  command places it. Shipped: `extensions/specassay-check/ci/specassay.yml` and
  `extensions/specassay-check/scripts/install-ci.sh`. Proven by
  `extensions/specassay-check/tests/test_cold_30_ci_workflow.py`.
  - AC-COLD-30a — proven by `test_AC_COLD_30a_install_ci_writes_the_workflow_and_is_idempotent`
    and `test_AC_COLD_30a_a_project_in_a_subdirectory_gets_its_own_root`.
  - AC-COLD-30b — proven by `test_AC_COLD_30b_a_differing_workflow_is_refused_not_overwritten`.
  - AC-COLD-30c — proven by `test_AC_COLD_30c_the_shipped_workflow_is_not_this_repository_s_own`.
- FR-COLD-40 — The cold path is proved by performing it. Shipped:
  `extensions/specassay-check/tests/test_cold_path_end_to_end.py`, run by
  `self-gate.yml` on every pull request and every push to main, and the sequence it
  drives is `ci-thread-report.sh`, the same one the shipped workflow drives.
  - AC-COLD-40a — proven by `test_AC_COLD_40a_the_cold_path_needs_no_plumbing`.
  - AC-COLD-40b — proven by
    `test_AC_COLD_40b_a_step_outside_the_shipped_tools_fails_the_proof`, which holds
    the path's own guard to a test rather than trusting it.
