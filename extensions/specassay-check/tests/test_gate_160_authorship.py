"""FR-GATE-160, AC-GATE-160 / 160b / 160c / 160d: authorship names who authored
a registry row.

Minted 2026-09-30 from a reading pass over Bang's 31 rows, which sorted them by
hand (case 10, design 19, retrospective 2, constitution 0) and had nowhere to
write the answer down.

The field is NOT `origin`. `origin` already ships on every v5 row as
`{kind: "registry-line", path, line}` -- the file and line where the row lives,
which is the one meaning the ruling excludes -- and its `ledger` kind belongs to
another emitter. So authorship is its own field, and one test here holds `origin`
to exactly what it was.
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
THREAD_REPORT = SCRIPTS / "thread-report.py"


def _v5(project):
    return json.loads((project.root / "trace-manifest.v5beta.json").read_text())


def _row(manifest, id_):
    for r in manifest["rows"]:
        if r["id"] == id_:
            return r
    raise AssertionError(f"{id_} not in {[r['id'] for r in manifest['rows']]}")


def _traced(project, *lines):
    """A registry with the given lines, each ID fully traced so the only
    findings in play are authorship's own."""
    project.prd(*lines)
    ids = [ln.split("—")[0].strip("- ").strip() for ln in lines]
    project.write("specs/f/spec.md", "\n".join(ids) + "\n")
    project.write(
        "specs/f/tasks.md",
        "".join(f"- [ ] T{i} work — **Carries**: {i_d}\n" for i, i_d in enumerate(ids)),
    )
    project.config()
    return ids


def test_AC_GATE_160_declared_authorship_reaches_the_v5_row(project):
    _traced(
        project,
        "- AC-PAY-10 — Given a declined card, then the checkout says so. **Authorship**: case",
        "- AC-PAY-20 — Given a long list, then it paginates at 25. **Authorship**: design",
    )
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr

    v5 = _v5(project)
    assert _row(v5, "AC-PAY-10")["authorship"] == "case"
    assert _row(v5, "AC-PAY-20")["authorship"] == "design"

    # The declaration is metadata about the row, not part of the promise: it
    # must not survive into the prose every consumer prints.
    for id_ in ("AC-PAY-10", "AC-PAY-20"):
        assert "Authorship" not in _row(v5, id_)["statement"], _row(v5, id_)["statement"]


def test_AC_GATE_160_all_four_values_are_accepted(project):
    _traced(
        project,
        "- AC-AA-10 — one. **Authorship**: case",
        "- AC-BB-10 — two. **Authorship**: design",
        "- AC-CC-10 — three. **Authorship**: retrospective",
        "- AC-DD-10 — four. **Authorship**: constitution",
    )
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr
    v5 = _v5(project)
    got = {r["id"]: r.get("authorship") for r in v5["rows"]}
    assert got == {
        "AC-AA-10": "case",
        "AC-BB-10": "design",
        "AC-CC-10": "retrospective",
        "AC-DD-10": "constitution",
    }


def test_AC_GATE_160_origin_is_unchanged_on_every_row(project):
    """The point of the separate field, held to directly: adding authorship
    changes `origin` on no row, and never moves inside it."""
    lines = [
        "- AC-PAY-10 — Given a declined card, then the checkout says so. **Authorship**: case",
        "- AC-PAY-20 — Given a long list, then it paginates at 25.",
    ]
    _traced(project, *lines)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr

    for r in _v5(project)["rows"]:
        origin = r["origin"]
        assert set(origin) == {"kind", "path", "line"}, origin
        assert origin["kind"] == "registry-line"
        assert origin["path"] == "PRD.md"
        assert isinstance(origin["line"], int)
        assert "authorship" not in origin


def test_AC_GATE_160b_a_value_outside_the_four_fails_naming_it(project):
    _traced(
        project,
        "- AC-PAY-10 — Given a declined card, then the checkout says so. **Authorship**: roadmap",
    )
    proc, manifest = project.run()

    assert proc.returncode != 0, "a value outside the four must fail the Gate"
    assert manifest["gate"]["ok"] is False
    bad = [f for f in manifest["gate"]["failures"] if f["kind"] == "authorship-invalid"]
    assert len(bad) == 1, manifest["gate"]["failures"]
    assert bad[0]["id"] == "AC-PAY-10"
    # Names the ID *and* the value, so the fix does not need a second look.
    assert "roadmap" in bad[0]["detail"]
    assert "AC-PAY-10" in bad[0]["detail"]
    # An unusable value is not quietly kept.
    assert "authorship" not in _row(_v5(project), "AC-PAY-10")


def test_AC_GATE_160c_an_unassigned_row_warns_and_does_not_fail(project):
    _traced(
        project,
        "- AC-PAY-10 — Given a declined card, then the checkout says so. **Authorship**: case",
        "- AC-PAY-20 — Given a long list, then it paginates at 25.",
    )
    proc, manifest = project.run()

    # Every project's registry predates the field; an unfilled row must not red
    # an adopter on the upgrade.
    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    warns = [d for d in manifest["gate"]["diagnostics"] if d["kind"] == "authorship-unassigned"]
    assert [w["id"] for w in warns] == ["AC-PAY-20"], warns
    assert "AC-PAY-20" in warns[0]["detail"]
    assert not any(f["kind"] == "authorship-unassigned" for f in manifest["gate"]["failures"])


def _report(tmp_path, v4, v5_rows):
    """Run the real thread-report.py over a hand-built pair of manifests."""
    base = {"gate": {"ok": True}, "rows": []}
    (tmp_path / "base.json").write_text(json.dumps(base))
    (tmp_path / "head.json").write_text(json.dumps(v4))
    (tmp_path / "head.v5beta.json").write_text(json.dumps({"rows": v5_rows}))
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


def _v4_rows(ids):
    return {
        "gate": {"ok": True},
        "statusCounts": {"proven": 0, "tracked-debt": 0, "GAP": 0, "backlog": len(ids)},
        "rows": [{"id": i, "type": i.split("-")[0], "status": "backlog",
                  "statement": i, "proofs": [], "implementations": []} for i in ids],
    }


def test_AC_GATE_160d_the_report_sentence_counts_by_authorship(tmp_path):
    ids = ["AC-A-10", "AC-B-10", "AC-C-10", "AC-D-10", "AC-E-10"]
    v5 = [
        {"id": "AC-A-10", "authorship": "case"},
        {"id": "AC-B-10", "authorship": "case"},
        {"id": "AC-C-10", "authorship": "design"},
        {"id": "AC-D-10", "authorship": "retrospective"},
        {"id": "AC-E-10", "authorship": "constitution"},
    ]
    report = _report(tmp_path, _v4_rows(ids), v5)
    # The shape is fixed, so it is asserted whole rather than by keywords.
    assert ("2 promises from the case, 3 from the project "
            "(design 1, retrospective 1, constitution 1).") in report
    # Above the table, and unfolded: before the What moved section.
    assert report.index("promises from the case") < report.index("What moved")


def test_AC_GATE_160d_the_report_sentence_says_how_many_are_unassigned(tmp_path):
    ids = ["AC-A-10", "AC-B-10", "AC-C-10"]
    v5 = [
        {"id": "AC-A-10", "authorship": "case"},
        {"id": "AC-B-10"},
        {"id": "AC-C-10"},
    ]
    report = _report(tmp_path, _v4_rows(ids), v5)
    # It says how many, instead of presenting one row's breakdown as the whole.
    assert "Authorship unassigned on 2 of 3 rows; of the rest, 1 promises from the case, 0 from the project (design 0, retrospective 0, constitution 0)." in report


def test_AC_GATE_160d_a_missing_v5_file_loses_the_numbers_not_the_report(tmp_path):
    """Illuminate, never refuse: with no v5 manifest beside the head, every row
    is unassigned, which is what the sentence then says."""
    ids = ["AC-A-10", "AC-B-10"]
    base = {"gate": {"ok": True}, "rows": []}
    (tmp_path / "base.json").write_text(json.dumps(base))
    (tmp_path / "head.json").write_text(json.dumps(_v4_rows(ids)))
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
    report = out.read_text()
    assert "Authorship not reported: no v5 manifest was found beside the head manifest." in report
    # Specifically NOT a confident breakdown of nothing.
    assert "0 promises from the case" not in report
