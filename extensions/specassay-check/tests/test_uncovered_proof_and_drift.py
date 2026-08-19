"""Rule 4a (uncovered-proof, report-only by default / opt-in blocking) and
exact-set drift (registry <-> specs <-> tasks). Both are named,
enforcement-bearing rules in PROMOTION-CONTRACT.md with no prior automated
coverage.
"""


def test_uncovered_proof_is_report_only_by_default(project):
    # A real, passing-shaped proof with no @covers claiming it: a named
    # finding, but report-only (gate.diagnostics), never gate.ok=false,
    # unless the project has opted into blocking.
    project.prd("- AC-FIX-01 — Proven by test alone, no @covers anywhere.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n")
    project.write(
        "specs/f/tasks.md",
        "- [x] T001 Build it — **Carries**: AC-FIX-01\n",
    )
    project.write(
        "tests/test_thing.py",
        "def test_AC_FIX_01_thing_works():\n    assert True\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    diag_kinds = {d["kind"] for d in manifest["gate"]["diagnostics"]}
    assert "uncovered-proof" in diag_kinds
    fail_kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "uncovered-proof" not in fail_kinds


def test_uncovered_proof_blocks_once_opted_in(project):
    project.prd("- AC-FIX-01 — Proven by test alone, no @covers anywhere.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n")
    project.write(
        "specs/f/tasks.md",
        "- [x] T001 Build it — **Carries**: AC-FIX-01\n",
    )
    project.write(
        "tests/test_thing.py",
        "def test_AC_FIX_01_thing_works():\n    assert True\n",
    )
    project.config(block_uncovered_proof=True)

    proc, manifest = project.run()

    assert proc.returncode == 1
    assert manifest["gate"]["ok"] is False
    fail_kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "uncovered-proof" in fail_kinds


def test_uncovered_proof_clears_once_covers_added(project):
    project.prd("- AC-FIX-01 — Now genuinely self-documented.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n")
    project.write(
        "specs/f/tasks.md",
        "- [x] T001 Build it — **Carries**: AC-FIX-01\n",
    )
    project.write(
        "src/thing.py",
        "# @covers AC-FIX-01\ndef thing():\n    return True\n",
    )
    project.write(
        "tests/test_thing.py",
        "def test_AC_FIX_01_thing_works():\n    assert True\n",
    )
    project.config(block_uncovered_proof=True)

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert manifest["gate"]["diagnostics"] == []


def test_spec_unclaimed_id_fails_exact_set(project):
    # A registry ID absent from every spec.md, with no anointed-backlog
    # TODO to excuse it: real drift, not backlog.
    project.prd("- FR-FIX-01 — Never claimed anywhere.")
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 1
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "spec-unclaimed" in kinds


def test_spec_orphan_id_fails_exact_set(project):
    # A spec claiming an ID the registry never minted, in this project's
    # own domain: real drift, the mirror direction.
    project.prd("- FR-FIX-01 — The only real ID.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.write("specs/f/spec.md", "# Feature\n\nCarries FR-FIX-02.\n")
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 1
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "spec-orphan" in kinds


def test_duplicate_definition_lines_fail(project):
    project.prd(
        "- FR-FIX-01 — First mint.",
        "- FR-FIX-01 — Accidental second mint, same ID.",
    )
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 1
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "duplicate-id" in kinds


def test_missing_carries_on_checkbox_fails(project):
    project.prd("- FR-FIX-01 — Has a task, but the task forgot Carries.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries FR-FIX-01.\n")
    project.write("specs/f/tasks.md", "- [x] T001 Build it, no mark at all\n")
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 1
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "missing-carries" in kinds
