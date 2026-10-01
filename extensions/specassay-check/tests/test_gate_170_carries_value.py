"""FR-GATE-170, AC-GATE-170 / 170b / 170c / 170d: a Carries mark must name what
it carries.

Until 2026-10-01 the check tested only that the mark was present. `CARRIES_RE`
is `\\*\\*(Carries|Traces)\\*\\*:` and it was read in exactly one place, so
`**Carries**: TBD` satisfied it: a task could declare that it carries something
and name nothing. That is the shape of undeclared debt this tool exists to
refuse, sitting inside the field that exists to declare it.

Reported by the Bang room. The lines the report cited (717-726) were the
test_results error handling, which an earlier fix had shifted down; the
substance was right and the regex was where they said it behaved.
"""

import json
import subprocess
import sys
from pathlib import Path

THREAD_REPORT = Path(__file__).resolve().parents[1] / "scripts" / "thread-report.py"


def _registry(project, *task_lines):
    """One registered, fully traced ID plus whatever task lines a test needs."""
    project.prd("- AC-PAY-10 — Given a declined card, then the reason is shown.")
    project.write("specs/f/spec.md", "AC-PAY-10\n")
    project.write("specs/f/tasks.md", "".join(task_lines))
    project.config()


def _carries_failures(manifest):
    return [f for f in manifest["gate"]["failures"] if f["kind"] == "carries-not-an-id"]


def test_AC_GATE_170_an_id_list_passes_even_with_prose_after_it(project):
    # The shape every real task line in this repository uses: the IDs, then the
    # reasoning, on one line. Reading must stop at the prose, not refuse it.
    _registry(
        project,
        "- [ ] T1 Build the decline path — **Carries**: AC-PAY-10. Ruled 2026-10-01 "
        "after the card vendor changed its error codes; see the retro.\n",
    )
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert _carries_failures(manifest) == []
    assert manifest["totals"]["carriesNoneCount"] == 0


def test_AC_GATE_170b_the_word_none_passes_and_is_counted(project):
    _registry(
        project,
        "- [ ] T1 Build the decline path — **Carries**: AC-PAY-10\n",
        "- [ ] T2 Rename a local variable — **Carries**: none. No promise rides on this.\n",
    )
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert _carries_failures(manifest) == []
    # Counted, never hidden: the number is the point.
    assert manifest["totals"]["carriesNoneCount"] == 1


def test_AC_GATE_170c_tbd_fails_naming_the_task_and_the_value(project):
    _registry(
        project,
        "- [ ] T1 Build the decline path — **Carries**: AC-PAY-10\n",
        "- [ ] T2 Something we have not thought about — **Carries**: TBD\n",
    )
    proc, manifest = project.run()
    assert proc.returncode != 0, "a Carries value naming nothing must fail the Gate"
    assert manifest["gate"]["ok"] is False
    bad = _carries_failures(manifest)
    assert len(bad) == 1, manifest["gate"]["failures"]
    # Names the task and the value, so the fix needs no second look.
    assert "T2" in bad[0]["detail"]
    assert "TBD" in bad[0]["detail"]


def test_AC_GATE_170c_an_empty_carries_value_fails(project):
    _registry(
        project,
        "- [ ] T1 Build the decline path — **Carries**: AC-PAY-10\n",
        "- [ ] T2 A mark and nothing after it — **Carries**:\n",
    )
    proc, manifest = project.run()
    assert proc.returncode != 0
    bad = _carries_failures(manifest)
    assert len(bad) == 1, manifest["gate"]["failures"]
    assert "T2" in bad[0]["detail"]
    # An absent value is named as absent rather than reported as some token.
    assert "(empty)" in bad[0]["detail"]


def test_AC_GATE_170c_none_is_the_only_word_that_passes(project):
    """`none` is a declaration, not a category of excuse: "nothing", "n/a" and
    "later" are all the same silence `TBD` was."""
    for word in ("nothing", "n/a", "later"):
        _registry(
            project,
            "- [ ] T1 Build the decline path — **Carries**: AC-PAY-10\n",
            f"- [ ] T2 A near miss — **Carries**: {word}\n",
        )
        proc, manifest = project.run()
        assert proc.returncode != 0, f"{word!r} must not pass"
        assert word in _carries_failures(manifest)[0]["detail"]


def _report(tmp_path, carries_none):
    v4 = {
        "gate": {"ok": True},
        "statusCounts": {"proven": 0, "tracked-debt": 0, "GAP": 0, "backlog": 1},
        "totals": {"carriesNoneCount": carries_none, "registryIdCount": 1},
        "rows": [{"id": "AC-PAY-10", "type": "AC", "status": "backlog",
                  "statement": "AC-PAY-10", "proofs": [], "implementations": []}],
    }
    (tmp_path / "base.json").write_text(json.dumps({"gate": {"ok": True}, "rows": []}))
    (tmp_path / "head.json").write_text(json.dumps(v4))
    (tmp_path / "changed.txt").write_text("PRD.md\n")
    out = tmp_path / "report.md"
    proc = subprocess.run(
        [sys.executable, str(THREAD_REPORT),
         "--base", str(tmp_path / "base.json"),
         "--head", str(tmp_path / "head.json"),
         "--changed-files", str(tmp_path / "changed.txt"),
         "--out", str(out)],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return out.read_text()


def test_AC_GATE_170d_the_report_says_how_many_carry_no_promise(tmp_path):
    report = _report(tmp_path, 3)
    assert "Three task lines carry no promise, declared as `none`." in report
    # Beside the authorship sentence, both above the table.
    assert report.index("carry no promise") < report.index("What moved")
    assert "Authorship" in report


def test_AC_GATE_170d_one_line_reads_in_the_singular(tmp_path):
    assert "One task line carries no promise, declared as `none`." in _report(tmp_path, 1)


def test_AC_GATE_170d_the_report_says_nothing_when_none_carry_nothing(tmp_path):
    # A zero said out loud every time is noise; the sentence earns its place
    # only when there is something to report.
    assert "carry no promise" not in _report(tmp_path, 0)
