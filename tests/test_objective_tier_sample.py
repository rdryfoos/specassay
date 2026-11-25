"""The objective-tier sample cannot drift from the emitter or from its note.

`samples/objective-tier.trace-manifest.v5beta.json` is a committed copy of
what the Gate emits for `samples/objective-tier/`. A committed artifact is
only worth having if it still matches the thing that produced it, so this
re-runs the Gate on the sample in a scratch copy and compares, field by field,
ignoring only what is volatile by construction (the timestamp, the absolute
repository path, and the emitter's version, which moves every release).

The IDs here are spelled with hyphens on purpose. The underscore form is what
a test name looks like, and this file sits inside this repository's own
`test_globs`.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "objective-tier"
COMMITTED = ROOT / "samples" / "objective-tier.trace-manifest.v5beta.json"
NOTE = ROOT / "samples" / "objective-tier.md"
SCRIPT = ROOT / "extensions" / "specassay-check" / "scripts" / "check-traceability.sh"

VOLATILE = ("generatedAt", "repoPath", "emitter")


@pytest.fixture(scope="module")
def committed():
    return json.loads(COMMITTED.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def emitted(tmp_path_factory):
    """What the Gate in this working tree emits for the sample, right now."""
    work = tmp_path_factory.mktemp("objective-tier") / "sample"
    shutil.copytree(SAMPLE, work)
    for stale in ("trace-manifest.json", "trace-manifest.v5beta.json"):
        (work / stale).unlink(missing_ok=True)
    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=work,
        env={
            **dict(__import__("os").environ),
            "SPECASSAY_PROJECT_ROOT": str(work),
            "SPECASSAY_CONFIG": str(work / "specassay-check-config.yml"),
        },
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    assert "OK (4 registry IDs)" in proc.stdout + proc.stderr
    return json.loads((work / "trace-manifest.v5beta.json").read_text(encoding="utf-8"))


def test_the_committed_sample_is_what_the_gate_emits_today(committed, emitted):
    assert {k: v for k, v in emitted.items() if k not in VOLATILE} == {
        k: v for k, v in committed.items() if k not in VOLATILE
    }


def test_the_sample_carries_the_objective_rows(committed):
    objectives = [r for r in committed["rows"] if r["tier"] == "objective"]
    assert [r["id"] for r in objectives] == [
        "OBJ-WALK-10", "OBJ-POWER-10", "OBJ-TRUST-10", "OBJ-GROUP-10",
    ]
    assert committed["totals"]["objectiveCount"] == 4
    assert committed["totals"]["registryIdCount"] == 4
    for row in objectives:
        assert row["origin"]["kind"] == "case-line"
        assert row["origin"]["path"] == "CASE.md"
        assert row["parents"] == []


def test_the_sample_shows_a_case_keeping_its_own_history(committed):
    """The case quotes three objectives' superseded wording and fences an
    example. Four definitions outside the quotes, four rows, no duplicate."""
    case = (SAMPLE / "CASE.md").read_text(encoding="utf-8")
    assert "## History" in case
    assert "> - OBJ-WALK-10 The walker is never lost" in case
    assert "> OBJ-TRUST-10." in case
    assert "- OBJ-EXAMPLE-10" in case  # the fenced example

    assert committed["gate"]["ok"] is True
    assert len([r for r in committed["rows"] if r["tier"] == "objective"]) == 4
    # The quoted IDs are the ones already defined above, and the fenced one is
    # defined nowhere: a mint from either would show up here.
    assert "OBJ-EXAMPLE-10" not in [r["id"] for r in committed["rows"]]


def test_the_sample_shows_an_objective_that_was_called_off(committed):
    rows = {r["id"]: r for r in committed["rows"]}
    row = rows["OBJ-GROUP-10"]
    assert row["status"] == "retired"
    assert row["superseded"]["date"] == "2026-11-25"
    assert row["superseded"]["reason"]
    assert "Superseded" not in row["statement"]
    # Nothing serves it and nothing complains about that.
    assert not any(
        d.get("kind") == "objective-unserved" and d.get("id") == "OBJ-GROUP-10"
        for d in (committed["gate"].get("diagnostics") or [])
    )


def test_the_sample_walks_from_a_test_up_to_an_objective(committed):
    rows = {r["id"]: r for r in committed["rows"]}
    start = rows["AC-WALK-01"]
    assert start["proofs"], "the criterion in the sample has a real proof"

    walk = [start["id"]]
    while rows[walk[-1]]["parents"]:
        walk.append(rows[walk[-1]]["parents"][0])
        assert len(walk) < 10, walk

    assert walk == ["AC-WALK-01", "FR-WALK-01", "US-WALK-01", "OBJ-WALK-10"]
    assert [rows[i]["tier"] for i in walk] == [
        "criterion", "requirement", "intent", "objective",
    ]


def test_the_sample_carries_a_row_serving_two_objectives(committed):
    rows = {r["id"]: r for r in committed["rows"]}
    assert rows["FR-WALK-01"]["parents"] == [
        "US-WALK-01", "OBJ-WALK-10", "OBJ-POWER-10",
    ]


def test_the_note_describes_the_manifest_beside_it(committed):
    note = NOTE.read_text(encoding="utf-8")
    rows = {r["id"]: r for r in committed["rows"]}

    # The counts the note quotes.
    assert f"({len(committed['rows'])} rows, schemaVersion 5, beta)" in note
    assert f"OK ({committed['totals']['registryIdCount']} registry IDs)" in note

    # The rolled-up colour it names, and the one it says has no rollup.
    assert rows["OBJ-WALK-10"]["status"] == "proven"
    assert rows["OBJ-WALK-10"]["rollup"]["rows"] == 3
    assert rows["OBJ-WALK-10"]["rollup"]["proven"] == 1
    assert rows["OBJ-WALK-10"]["rollup"]["backlog"] == 2
    assert "rollup" not in rows["OBJ-POWER-10"]
    assert rows["OBJ-POWER-10"]["status"] == "backlog"
    assert "`OBJ-POWER-10` is served by a requirement rather than by a" in note
    assert "reads `backlog` with no rollup at all" in note


def test_the_note_owns_up_to_what_the_sample_does_not_show(committed):
    note = NOTE.read_text(encoding="utf-8")
    # The sample is green, so neither refusal is visible in it, and the note
    # has to say where they are instead of implying this file shows them.
    assert committed["gate"]["ok"] is True
    assert "block_orphan_story" in note
    assert "FR-CASE-10" in note and "not built" in note


@pytest.mark.skipif(sys.platform == "win32", reason="the sample's own suite is POSIX-pathed")
def test_the_samples_own_test_passes(tmp_path):
    """The proof in the sample is a real passing test, not a name."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(SAMPLE / "tests")],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
