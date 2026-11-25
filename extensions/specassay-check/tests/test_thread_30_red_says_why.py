"""FR-THREAD-30, AC-THREAD-30a and AC-THREAD-30b: a red report says what
refused, and a report carrying objectives says something of them.

Found 2026-11-25, when a room took the objective tier and met a comment whose
verdict read `Do not merge yet · no requirements changed` while nine findings
of one kind sat in the job log. The state was there and the cause was not.

The fixtures are hand-built manifest pairs, the way this file's neighbour
builds them: the display contract is what is under test, so the input is a
manifest and the output is the comment's own text.
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
THREAD_REPORT = SCRIPTS / "thread-report.py"


def _report(tmp_path, v4, v5_rows=None):
    base = {"gate": {"ok": True}, "rows": []}
    (tmp_path / "base.json").write_text(json.dumps(base))
    (tmp_path / "head.json").write_text(json.dumps(v4))
    if v5_rows is not None:
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


def _head(failures=(), diagnostics=(), ok=None, rows=()):
    return {
        "gate": {
            "ok": (not failures) if ok is None else ok,
            "failures": list(failures),
            "diagnostics": list(diagnostics),
        },
        "statusCounts": {"proven": 0, "tracked-debt": 0, "GAP": 0, "backlog": len(rows)},
        "rows": [
            {"id": i, "type": i.split("-")[0], "status": "backlog",
             "statement": i, "proofs": [], "implementations": []} for i in rows
        ],
    }


# The shape the live case hit: many findings, all of one kind, and a change
# that moved nothing in the thread, so every count in the verdict was zero.
NINE_DUPES = [
    {"kind": "objective-duplicate", "id": f"OBJ-{n}",
     "detail": f"duplicate objective: OBJ-{n} is defined again at CASE.md:{40 + n}"}
    for n in range(1, 10)
]


def test_AC_THREAD_30a_a_red_report_names_the_refusal_and_counts_it(tmp_path):
    report = _report(tmp_path, _head(failures=NINE_DUPES, rows=["AC-A-10"]))

    assert "🔴 **Do not merge yet**" in report
    assert "The Gate refused: 9 refusals, **9** `objective-duplicate`." in report
    # The first thing under the verdict: a reader just told not to merge is
    # owed the reason before anything else on the page.
    verdict_at = report.index("Do not merge yet")
    assert report.index("The Gate refused:") > verdict_at
    assert report.index("The Gate refused:") < report.index("What changed")


def test_AC_THREAD_30a_several_kinds_lead_with_the_biggest(tmp_path):
    failures = NINE_DUPES[:2] + [
        {"kind": "silent-gap", "id": "AC-A-10", "detail": "..."},
        {"kind": "silent-gap", "id": "AC-B-10", "detail": "..."},
        {"kind": "silent-gap", "id": "AC-C-10", "detail": "..."},
        {"kind": "orphan-story", "id": "US-A-10", "detail": "..."},
    ]
    report = _report(tmp_path, _head(failures=failures, rows=["AC-A-10"]))
    assert ("The Gate refused: 6 refusals, **3** `silent-gap`, "
            "**2** `objective-duplicate`, **1** `orphan-story`.") in report


def test_AC_THREAD_30a_one_refusal_reads_as_one(tmp_path):
    report = _report(tmp_path, _head(failures=NINE_DUPES[:1], rows=["AC-A-10"]))
    assert "The Gate refused: 1 refusal, **1** `objective-duplicate`." in report


def test_AC_THREAD_30a_a_green_report_says_nothing_of_refusals(tmp_path):
    report = _report(tmp_path, _head(rows=["AC-A-10"]))
    assert "🟢 **Ready to review**" in report
    assert "The Gate refused" not in report


def test_AC_THREAD_30b_the_comment_says_what_the_case_defines(tmp_path):
    v5 = [
        {"id": "OBJ-WALK-10", "tier": "objective", "status": "proven"},
        {"id": "OBJ-POWER-10", "tier": "objective", "status": "backlog"},
        {"id": "OBJ-TRUST-10", "tier": "objective", "status": "backlog"},
        {"id": "US-WALK-01", "tier": "intent", "parents": ["OBJ-WALK-10"]},
        {"id": "AC-WALK-01", "tier": "criterion", "parents": ["US-WALK-01"],
         "authorship": "case"},
    ]
    orphans = [{"kind": "orphan-story", "id": "US-PHONE-01", "detail": "..."}]
    report = _report(tmp_path, _head(diagnostics=orphans, rows=["AC-WALK-01"]), v5)

    assert ("The case defines 3 objectives, 2 that no story serves, "
            "1 story serving none.") in report
    # Beside the authorship sentence, which counts requirements only: the two
    # non-objective rows here, one of them unmarked. The three objectives are
    # not requirements and are not in its arithmetic.
    assert ("No author named on 1 of 2 requirements; of the rest, 1 came from "
            "the case, 0 from the project (design 0, retrospective 0, "
            "constitution 0).") in report
    # Order on the page: the objectives sentence above the authorship one.
    assert report.index("The case defines") < report.index("No author named")


def test_AC_THREAD_30b_a_superseded_objective_is_counted_as_superseded(tmp_path):
    v5 = [
        {"id": "OBJ-WALK-10", "tier": "objective", "status": "proven"},
        {"id": "OBJ-TRUST-10", "tier": "objective", "status": "retired",
         "superseded": {"date": "2026-11-24", "reason": "the aim was dropped"}},
        {"id": "US-WALK-01", "tier": "intent", "parents": ["OBJ-WALK-10"]},
        {"id": "AC-WALK-01", "tier": "criterion", "parents": ["US-WALK-01"],
         "authorship": "design"},
    ]
    report = _report(tmp_path, _head(rows=["AC-WALK-01"]), v5)
    # Two objectives are DEFINED here and one of them is called off. The
    # subject of the sentence is what the case defines, so it counts both and
    # names the superseded one as a subtraction: a sentence that led with the
    # live count would read "1 objective (1 superseded)" over a case holding
    # two, and the reader would have to open the manifest to find that out.
    assert ("The case defines 2 objectives, 1 of them superseded, "
            "every live one served.") in report
    assert "(1 superseded)" not in report


def test_AC_THREAD_30b_an_unserved_live_objective_beside_a_superseded_one(tmp_path):
    """The unserved count is measured over the live objectives only, and says
    so in the word `live` once a superseded one is in the sentence."""
    v5 = [
        {"id": "OBJ-WALK-10", "tier": "objective", "status": "proven"},
        {"id": "OBJ-POWER-10", "tier": "objective", "status": "backlog"},
        {"id": "OBJ-TRUST-10", "tier": "objective", "status": "retired",
         "superseded": {"date": "2026-11-24", "reason": "the aim was dropped"}},
        {"id": "US-WALK-01", "tier": "intent", "parents": ["OBJ-WALK-10"]},
        {"id": "AC-WALK-01", "tier": "criterion", "parents": ["US-WALK-01"],
         "authorship": "design"},
    ]
    report = _report(tmp_path, _head(rows=["AC-WALK-01"]), v5)
    # Three defined, one called off, and of the two live one is unserved: the
    # superseded one is NOT among the unserved, which is the whole point of
    # FR-CASE-70.
    assert ("The case defines 3 objectives, 1 of them superseded, "
            "1 live that no story serves.") in report


def test_AC_THREAD_30b_no_objectives_means_no_sentence(tmp_path):
    """Most projects have not turned the tier on, and a sentence about a tier
    nobody uses is noise."""
    v5 = [{"id": "AC-A-10", "tier": "criterion", "authorship": "case"}]
    report = _report(tmp_path, _head(rows=["AC-A-10"]), v5)
    assert "The case defines" not in report
    assert "1 requirement came from the case" in report


def test_AC_THREAD_30b_no_v5_file_means_no_sentence(tmp_path):
    report = _report(tmp_path, _head(rows=["AC-A-10"]))
    assert "The case defines" not in report
