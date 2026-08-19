"""Core Gate rules (PROMOTION-CONTRACT.md): exact-set, silent-gap, anointed
backlog, tracked-debt. The four honest states, proved against the real
script rather than asserted from reading it.
"""


def test_golden_path_proven(project):
    project.prd("- AC-FIX-01 — A thing that works.")
    project.write(
        "specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n"
    )
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
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert project.row(manifest, "AC-FIX-01")["status"] == "proven"


def test_silent_gap_fails_the_gate(project):
    # An AC with a real spec/task claim but neither proof nor open debt is
    # exactly Rule 6's silent gap: the Gate must refuse, not go quiet.
    project.prd("- AC-FIX-01 — A thing with no carrier at all.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n")
    project.write(
        "specs/f/tasks.md",
        "- [x] T001 Build it — **Carries**: AC-FIX-01\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 1
    assert manifest["gate"]["ok"] is False
    assert project.row(manifest, "AC-FIX-01")["status"] == "GAP"
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "silent-gap" in kinds


def test_anointed_backlog_is_not_a_gap(project):
    # Rule 5a: a registry ID whose only carrier is an open Carries TODO is
    # backlog, not drift -- minting ahead of the work is a deliberate,
    # visible "coming soon", the whole reason anointed backlog exists.
    project.prd("- AC-FIX-01 — Not built yet, on purpose.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: AC-FIX-01 (anointed backlog)\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert project.row(manifest, "AC-FIX-01")["status"] == "backlog"


def test_tracked_debt_excuses_missing_proof(project):
    # Work started (spec + @covers) but the proof is still an open task:
    # honest debt, visible, not a silent gap.
    project.prd("- AC-FIX-01 — Started, proof still owed.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n")
    project.write(
        "specs/f/tasks.md",
        "- [x] T001 Build it — **Carries**: AC-FIX-01\n"
        "- [ ] T002 Prove it — **Carries**: AC-FIX-01\n",
    )
    project.write(
        "src/thing.py",
        "# @covers AC-FIX-01\ndef thing():\n    return True\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    row = project.row(manifest, "AC-FIX-01")
    assert row["status"] == "tracked-debt"
    assert len(row["carryingTasks"]) == 1
