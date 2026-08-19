"""FR-GATE-70: a list-type config key (src_globs, test_globs, or any later
yaml_list() consumer) that's present but malformed or bare refuses loudly
before any scanning, instead of silently parsing to an empty list. The
self-referential case of the silent-gap shape this tool exists to refuse
in adopters' own work.

The two verbatim-incident tests use the exact broken configs handed over
in the real capture session (2026-08-19) -- the regression fixtures are
the incidents, not a paraphrase of them.
"""


def test_AC_GATE_70a_inline_array_refuses_before_scanning(project):
    project.prd("- AC-FIX-01 — thing.")
    project.write("src/thing.py", "# @covers AC-FIX-01\ndef thing(): return True\n")
    project.raw_config(
        'registry: "PRD.md"\n'
        'target_name: "fixture"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\n'
        'tasks: "specs/**/tasks.md"\n'
        'src_globs: ["src/**"]\n'
        'test_globs: ["tests/**"]\n'
        'id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"\n'
        'covers_regex: "@covers[[:space:]]+.*"\n'
        r'carries_regex: "\*\*(Carries|Traces)\*\*:"' "\n"
        'test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"\n'
    )

    proc, manifest = project.run()

    assert proc.returncode == 2
    assert manifest is None, "a config known to be misread must not emit a manifest"
    assert "config key 'src_globs' is present but didn't parse to any entries" in proc.stderr
    assert 'src_globs: ["src/**"]' in proc.stderr
    assert "block-style" in proc.stderr
    assert "troubleshooting.md" in proc.stderr


def test_AC_GATE_70b_bare_key_refuses_before_scanning(project):
    project.prd("- AC-FIX-01 — thing.")
    project.raw_config(
        'registry: "PRD.md"\n'
        'target_name: "fixture"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\n'
        'tasks: "specs/**/tasks.md"\n'
        "src_globs:\n"
        "test_globs:\n"
        '  - "tests/**"\n'
        'id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"\n'
        'covers_regex: "@covers[[:space:]]+.*"\n'
        r'carries_regex: "\*\*(Carries|Traces)\*\*:"' "\n"
        'test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"\n'
    )

    proc, manifest = project.run()

    assert proc.returncode == 2
    assert manifest is None
    assert "config key 'src_globs' is present but has no items under it" in proc.stderr
    assert 'omit the key entirely' in proc.stderr


def test_AC_GATE_70c_absent_key_still_means_none(project):
    # Backward compatible: a key never mentioned at all is unchanged
    # behavior, not an error.
    project.prd("- FR-FIX-01 — thing.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.raw_config(
        'registry: "PRD.md"\n'
        'target_name: "fixture"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\n'
        'tasks: "specs/**/tasks.md"\n'
        'id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"\n'
        'covers_regex: "@covers[[:space:]]+.*"\n'
        r'carries_regex: "\*\*(Carries|Traces)\*\*:"' "\n"
        'test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"\n'
    )

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest is not None
    assert manifest["gate"]["ok"] is True


def test_valid_block_list_is_unaffected(project):
    project.prd("- FR-FIX-01 — thing.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.write("src/thing.py", "# @covers FR-FIX-01\ndef thing(): return True\n")
    project.config()  # the normal builder always writes block-style lists

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True


def test_generalizes_to_test_globs_too(project):
    # Not a src_globs special case: the same malformed key anywhere in
    # the yaml_list() family refuses the same way.
    project.prd("- AC-FIX-01 — thing.")
    project.raw_config(
        'registry: "PRD.md"\n'
        'target_name: "fixture"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\n'
        'tasks: "specs/**/tasks.md"\n'
        'src_globs:\n'
        '  - "src/**"\n'
        'test_globs: ["tests/**"]\n'
        'id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"\n'
        'covers_regex: "@covers[[:space:]]+.*"\n'
        r'carries_regex: "\*\*(Carries|Traces)\*\*:"' "\n"
        'test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"\n'
    )

    proc, manifest = project.run()

    assert proc.returncode == 2
    assert manifest is None
    assert "config key 'test_globs' is present but didn't parse to any entries" in proc.stderr


def test_incident_1_verbatim_exec_verified_demo(project):
    # Exact config text handed to the capture session for entry 1
    # (executionVerified: false) -- this is the incident, not a
    # reconstruction of it.
    project.prd("- AC-FIX-01 — Proven by a matching test name; execution not yet verified.")
    project.raw_config(
        'registry: "PRD.md"\n'
        'target_name: "exec-verified-demo"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\n'
        'tasks: "specs/**/tasks.md"\n'
        'src_globs: ["src/**"]\n'
        'test_globs: ["tests/**"]\n'
        'test_results: "junit-results.xml"\n'
        'id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"\n'
        'covers_regex: "@covers[[:space:]]+.*"\n'
        r'carries_regex: "\*\*(Carries|Traces)\*\*:"' "\n"
        'test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"\n'
    )

    proc, manifest = project.run()

    assert proc.returncode == 2
    assert manifest is None
    assert "config key 'src_globs' is present but didn't parse to any entries" in proc.stderr


def test_incident_2_verbatim_uncovered_proof_demo(project):
    # Exact config text handed to the capture session for entry 2
    # (uncovered-proof) -- same incident class, independently confirmed.
    project.prd("- AC-FIX-01 — Proven by test alone; no file's @covers line names it.")
    project.raw_config(
        'registry: "PRD.md"\n'
        'target_name: "uncovered-proof-demo"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\n'
        'tasks: "specs/**/tasks.md"\n'
        'src_globs: ["src/**"]\n'
        'test_globs: ["tests/**"]\n'
        'id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"\n'
        'covers_regex: "@covers[[:space:]]+.*"\n'
        r'carries_regex: "\*\*(Carries|Traces)\*\*:"' "\n"
        'test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"\n'
    )

    proc, manifest = project.run()

    assert proc.returncode == 2
    assert manifest is None
    assert "config key 'src_globs' is present but didn't parse to any entries" in proc.stderr
