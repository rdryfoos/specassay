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
