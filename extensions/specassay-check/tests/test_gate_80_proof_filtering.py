"""FR-GATE-80, AC-GATE-80: proofs[] population used to trust proof_hits.txt's
own raw text match unconditionally -- a name matching test_ac_regex anywhere
in a test file's text, including a comment, was good enough to appear in the
manifest, even when test_results (Rule 6a) was configured and would have
said otherwise. Citing incident: a SpecCost engine finding relayed to this
repo (SpecCost doesn't own this code) -- AC-WALK-10's proofs[] listed a test
name that survived only inside a rename-explanation comment after the real
test was renamed away, with no status-integrity risk (status_for() already
kept it honestly tracked-debt) but a legibility/trust defect on a field
whose whole job is being trustworthy at a glance.
"""

import json


def test_AC_GATE_80_comment_only_match_excluded_when_test_results_configured(project):
    # The real incident's shape: no function named test_AC_WIDGET_01_... exists
    # anywhere -- only a comment mentioning the old, renamed-away name.
    project.prd("- AC-WIDGET-01 — proof owed, not yet real.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T0 backlog — **Carries**: AC-WIDGET-01\n")
    project.write(
        "tests/test_thing.py",
        "# renamed away: def test_AC_WIDGET_01_old_ghost_name(): pass\n"
        "def test_unrelated_thing():\n    pass\n",
    )
    junit = project.root / "junit-results.xml"
    junit.write_text(
        '<?xml version="1.0"?>\n'
        '<testsuite>\n'
        '  <testcase classname="tests.test_thing" name="test_unrelated_thing"/>\n'
        '</testsuite>\n'
    )
    project.config(test_results=str(junit))
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["executionVerified"] is True

    row = project.row(manifest, "AC-WIDGET-01")
    # No status-integrity risk -- this was never the bug: status_for() already
    # keeps this honestly tracked-debt (no real passing test).
    assert row["status"] == "tracked-debt"
    # The actual fix: the ghost comment-derived name must not appear at all.
    assert row["proofs"] == []


def test_ghost_match_still_appears_without_test_results_unfiltered_mode(project):
    # Backward compatibility: with no test_results configured, there is no
    # execution truth to filter against, so behavior is unchanged from
    # before this fix -- a text match is still a text match.
    project.prd("- AC-WIDGET-01 — proof owed, not yet real.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T0 backlog — **Carries**: AC-WIDGET-01\n")
    project.write(
        "tests/test_thing.py",
        "# renamed away: def test_AC_WIDGET_01_old_ghost_name(): pass\n",
    )
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["executionVerified"] is False

    row = project.row(manifest, "AC-WIDGET-01")
    names = [p["name"] for p in row["proofs"]]
    assert "test_AC_WIDGET_01_old_ghost_name" in names


def test_real_passing_test_still_appears_when_test_results_configured(project):
    # The fix must not throw out real proofs along with ghost ones.
    project.prd("- AC-WIDGET-01 — proven via a real test.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T0 backlog — **Carries**: AC-WIDGET-01\n")
    project.write(
        "tests/test_thing.py",
        "def test_AC_WIDGET_01_real():\n    pass\n",
    )
    junit = project.root / "junit-results.xml"
    junit.write_text(
        '<?xml version="1.0"?>\n'
        '<testsuite>\n'
        '  <testcase classname="tests.test_thing" name="test_AC_WIDGET_01_real"/>\n'
        '</testsuite>\n'
    )
    project.config(test_results=str(junit))
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "AC-WIDGET-01")
    assert row["status"] == "proven"
    names = [p["name"] for p in row["proofs"]]
    assert "test_AC_WIDGET_01_real" in names
