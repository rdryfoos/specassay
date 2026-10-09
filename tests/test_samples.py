"""The refused sample cannot drift from the note beside it.

`samples/HomesFlow.refused.trace-manifest.json` exists so a picture of a
refusal can be shot from a file in a repository rather than from a scratch copy
nobody kept. A sample like that is only worth having if the prose beside it
still describes it, so these tests read both and compare them: the counts, the
row that refuses, the verdict lines, and the test whose name was removed.

Nothing here re-runs the Gate. The sample is the Gate's own output, and the
claim under test is that the note tells the truth about it.
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "samples" / "HomesFlow.refused.trace-manifest.json"
NOTE = ROOT / "samples" / "HomesFlow.refused.md"

# Spelled with hyphens on purpose. The underscore form is what a test name
# looks like, and this file is inside test_globs: writing it here would make
# this repository's own Gate read it as a test naming another project's
# criterion, and refuse the ID as untraced scope.
REFUSED_ID = "AC-GUEST-05"


@pytest.fixture(scope="module")
def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def note():
    return NOTE.read_text(encoding="utf-8")


def test_the_sample_is_refused(manifest):
    assert manifest["gate"]["ok"] is False, "a refused sample that passes is not a specimen"


def test_exactly_one_row_refuses_and_it_is_the_named_one(manifest):
    failures = manifest["gate"]["failures"]
    assert len(failures) == 1, failures
    assert failures[0]["id"] == REFUSED_ID
    assert failures[0]["kind"] == "silent-gap"
    assert manifest["statusCounts"]["GAP"] == 1
    gaps = [r["id"] for r in manifest["rows"] if r["status"] == "GAP"]
    assert gaps == [REFUSED_ID]


def test_the_refused_row_has_code_behind_it_and_no_test(manifest):
    """The shape worth photographing: @covers marks, and nothing naming it."""
    row = next(r for r in manifest["rows"] if r["id"] == REFUSED_ID)
    assert row["proofs"] == [], "the proof is supposed to be the thing removed"
    assert len(row["implementations"]) == 2, row["implementations"]
    for impl in row["implementations"]:
        assert REFUSED_ID in impl["excerpt"], impl


def test_the_note_names_the_row_the_manifest_refuses(note, manifest):
    assert REFUSED_ID in note
    other_gaps = {r["id"] for r in manifest["rows"] if r["status"] == "GAP"} - {REFUSED_ID}
    assert not other_gaps


def test_the_note_quotes_the_verdict_the_manifest_carries(note, manifest):
    """The FAIL line in the note is the detail the manifest recorded."""
    detail = manifest["gate"]["failures"][0]["detail"]
    assert f"FAIL: {detail}" in note, detail
    assert "SpecAssay Check (Gate 2): FAILED" in note


def test_the_note_counts_what_the_manifest_counts(note, manifest):
    counts = manifest["statusCounts"]
    stated = f"{counts['proven']} proven, {counts['tracked-debt']} tracked-debt, {counts['GAP']} GAP, {counts['backlog']} backlog"
    assert stated in note, stated
    assert f"| Rows | {len(manifest['rows'])} |" in note


def test_the_note_names_the_test_whose_name_was_removed(note, manifest):
    """The note carries both names, and neither is in the manifest any more.

    Built from the note rather than hardcoded, so this file never spells a test
    name that this repository's Gate would read as its own.
    """
    names = re.findall(r"`(test_[A-Za-z0-9_]+)`", note)
    before = [n for n in names if REFUSED_ID.replace("-", "_") in n]
    after = [n for n in names if REFUSED_ID.replace("-", "_") not in n]
    assert len(before) == 1, f"the note should name the test it renamed: {names}"
    assert len(after) >= 1, f"the note should name what it renamed it to: {names}"
    assert before[0].endswith(after[0].removeprefix("test_")), (before, after)

    blob = json.dumps(manifest)
    assert before[0] not in blob, "the removed proof is still in the manifest"


def test_the_note_names_the_base_commit_and_the_gate_that_ran(note):
    assert "`0b6da37`" in note, "a sample nobody can re-make is a sketch"
    assert "0.5.6" in note


def test_the_note_owns_up_to_the_preparation(note):
    """Ten findings were corrected before the one that matters was made.

    A note that hid that would make the sample look cleaner than it is, and the
    next person to re-make it would get eleven refusals and no idea why.
    """
    assert "already refused by the released Gate" in note
    assert "ten" in note.lower()
    assert "FR-GATE-170" in note


# --- this repository's own demo workflow -------------------------------------

WORKFLOW = ROOT / ".github" / "workflows" / "thread-report.yml"


def test_the_demo_workflow_copies_the_v5_sidecar_beside_the_head_manifest():
    """Without it, every Thread Report this repo posts loses its author counts.

    `thread-report.py` reads authorship from the v5 manifest sitting beside
    `--head`. This workflow copies the manifests by hand, predating the shipped
    `ci-thread-report.sh` that does the same job correctly, and for as long as
    it copied only `trace-manifest.json` the comment carried "No author counts:
    the v5 manifest was not found beside the head manifest" directly under the
    verdict line. Seen on the live comment on PR #74, 2026-10-09.
    """
    body = WORKFLOW.read_text(encoding="utf-8")
    assert 'cp "$APP/trace-manifest.json" /tmp/head.json' in body
    assert 'cp "$APP/trace-manifest.v5beta.json" /tmp/head.v5beta.json' in body, (
        "the head manifest is copied without its v5 sidecar, so the report "
        "cannot read authorship"
    )


def test_the_shipped_ci_copies_the_sidecar_too():
    """The adopters' path, which was never broken, pinned so it stays that way."""
    shipped = ROOT / "extensions" / "specassay-check" / "scripts" / "ci-thread-report.sh"
    body = shipped.read_text(encoding="utf-8")
    assert 'v5="${HEAD_REL%.json}.v5beta.json"' in body
    assert 'cp "$ROOT/$v5" "$OUT_DIR/head.v5beta.json"' in body
