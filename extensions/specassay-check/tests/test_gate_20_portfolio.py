"""FR-GATE-20, AC-GATE-20a/b: --portfolio re-presents the same run's
already-computed status data as portfolio-snapshot.md -- narrative framing
for a cold reader with zero prior context, never the CI-oriented banner
--matrix carries. Same boundary line as FR-GATE-10 (a document, never a
viewer); "portfolio" is scoped explicitly to this one repo's own whole
thread, never a cross-repo aggregate (see PRD.md's FR-GATE-20 entry).
"""


def test_AC_GATE_20a_portfolio_writes_from_same_run_no_ci_banner(project):
    project.prd(
        "- AC-WIDGET-01 — proven candidate.",
        "- AC-WIDGET-02 — backlog candidate.",
    )
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [x] T0 proven carrier — **Carries**: AC-WIDGET-01\n"
        "- [ ] T1 backlog carrier — **Carries**: AC-WIDGET-02\n",
    )
    project.write("src/thing.py", "# @covers AC-WIDGET-01\n")
    project.write("tests/test_thing.py", "def test_AC_WIDGET_01_proven():\n    pass\n")
    project.config()
    proc, manifest = project.run(["--portfolio"])
    assert proc.returncode == 0, proc.stderr

    md = (project.root / "portfolio-snapshot.md").read_text()
    assert "AC-WIDGET-01" in md
    assert "AC-WIDGET-02" in md
    # Narrative framing, not the CI banner --matrix carries.
    assert "GENERATED FILE" not in md
    assert "no prior context" in md
    # Same run's data, not independently recomputed.
    assert manifest["totals"]["registryIdCount"] == 2
    # coverage.svg is a shared asset, written even without --matrix, and
    # embedded rather than a second image being generated.
    assert (project.root / "coverage.svg").exists()
    assert "![Coverage bar](coverage.svg)" in md
    # --matrix's own coverage.md is NOT written when --portfolio runs alone.
    assert not (project.root / "coverage.md").exists()


def test_AC_GATE_20b_snapshot_names_only_this_repo(project):
    project.prd("- AC-WIDGET-01 — proven candidate.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [x] T0 done — **Carries**: AC-WIDGET-01\n")
    project.write("src/thing.py", "# @covers AC-WIDGET-01\n")
    project.write("tests/test_thing.py", "def test_AC_WIDGET_01_proven():\n    pass\n")
    project.config(target_name="solo-repo")
    proc, manifest = project.run(["--portfolio"])
    assert proc.returncode == 0, proc.stderr

    md = (project.root / "portfolio-snapshot.md").read_text()
    assert "solo-repo" in md
    # No cross-repo language anywhere in the emitted document.
    for banned in ("other repo", "across projects", "multiple repos", "federation"):
        assert banned not in md.lower()


def test_long_statements_are_truncated_for_cold_reader(project):
    long_statement = "Given a lengthy paragraph-shaped registry statement " * 5
    project.prd(f"- AC-WIDGET-01 — {long_statement.strip()}")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T0 backlog — **Carries**: AC-WIDGET-01\n")
    project.config()
    proc, manifest = project.run(["--portfolio"])
    assert proc.returncode == 0, proc.stderr

    md = (project.root / "portfolio-snapshot.md").read_text()
    bullet_line = next(line for line in md.splitlines() if line.startswith("- **AC-WIDGET-01**"))
    assert len(bullet_line) < 200
    assert bullet_line.endswith("…")


def test_both_flags_together_write_all_three_files_once(project):
    project.prd("- AC-WIDGET-01 — proven candidate.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [x] T0 done — **Carries**: AC-WIDGET-01\n")
    project.write("src/thing.py", "# @covers AC-WIDGET-01\n")
    project.write("tests/test_thing.py", "def test_AC_WIDGET_01_proven():\n    pass\n")
    project.config()
    proc, manifest = project.run(["--matrix", "--portfolio"])
    assert proc.returncode == 0, proc.stderr
    assert (project.root / "coverage.md").exists()
    assert (project.root / "coverage.svg").exists()
    assert (project.root / "portfolio-snapshot.md").exists()
