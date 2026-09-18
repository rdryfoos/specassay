"""The doc-version checker's own contract.

One test per rule, and one per bug the first sweep found in the checker itself.
That second group is the more useful half. Every one of those bugs was found by
pointing the checker at real documents rather than by reasoning about it, which
is the same lesson as the capture method that lied about the thing it captured:
an instrument is not trustworthy until you have watched it work on the real
material.
"""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-doc-versions.py"

CHANGELOG = """# Changelog

## 0.5.1 (2026-09-17)

Something.

## 0.5.0 (2026-09-16)

Something.

## 0.4.13 (2026-09-04)

Something.

## 0.4.12 — 2026-08-20

Something.
"""

BUNDLE = """schema_version: "1.0"

bundle:
  id: "specassay"
  version: "0.5.1"

requires:
  speckit_version: ">=0.14.0,<2.0.0"
"""


def build(tmp_path, readme: str, changelog: str = CHANGELOG) -> Path:
    (tmp_path / "CHANGELOG.md").write_text(changelog)
    (tmp_path / "bundle.yml").write_text(BUNDLE)
    (tmp_path / "README.md").write_text(readme)
    return tmp_path


def run(root: Path, version: str | None = None):
    cmd = [sys.executable, str(SCRIPT), "--root", str(root)]
    if version:
        cmd += ["--version", version]
    return subprocess.run(cmd, capture_output=True, text=True)


# --- rule 1: no unclassified version number in prose ----------------------


def test_AC_DOCS_20_a_bare_version_number_in_prose_is_refused(tmp_path):
    proc = run(build(tmp_path, "# T\n\nWe verified this on 0.4.13 and it worked.\n"))
    assert proc.returncode == 1
    assert "unclassified version number" in proc.stderr


@pytest.mark.parametrize("line,why", [
    ("Both components report 0.5.1. <!-- specassay:current -->", "current claim"),
    ("Checked on 2026-09-17: both report 0.5.1.", "dated observation"),
    ("Pinned to Spec Kit 1.0.4. <!-- specassay:pinned Spec Kit -->", "pinned"),
    ("Since 0.4.13 the Gate says so. <!-- specassay:provenance -->", "provenance"),
    ("The manifests accept `>=0.14.0,<2.0.0`.", "declared range"),
])
def test_AC_DOCS_20_every_classification_is_accepted(tmp_path, line, why):
    proc = run(build(tmp_path, f"# T\n\n{line}\n"))
    assert proc.returncode == 0, f"{why} was refused:\n{proc.stderr}"


# --- rule 2: a current claim names the version being cut ------------------


def test_AC_DOCS_20_a_current_claim_naming_the_wrong_version_is_refused(tmp_path):
    proc = run(build(tmp_path, "# T\n\nBoth report 0.4.13. <!-- specassay:current -->\n"))
    assert proc.returncode == 1
    assert "current claim says 0.4.13" in proc.stderr
    assert "0.5.1" in proc.stderr


# --- rule 3: a dated observation has an age ------------------------------


def test_AC_DOCS_20_a_dated_observation_too_far_behind_is_refused(tmp_path):
    # 0.4.12 is three releases behind 0.5.1 in the fixture CHANGELOG.
    proc = run(build(tmp_path, "# T\n\nOn 2026-08-20 it reported 0.4.12.\n"))
    assert proc.returncode == 1
    assert "3 releases behind" in proc.stderr


def test_AC_DOCS_20_a_recent_dated_observation_warns_without_refusing(tmp_path):
    proc = run(build(tmp_path, "# T\n\nOn 2026-09-04 it reported 0.4.13.\n"))
    assert proc.returncode == 0
    assert "2 releases behind" in proc.stdout


def test_AC_DOCS_20_a_stated_reason_keeps_an_old_observation(tmp_path):
    proc = run(build(tmp_path,
        "# T\n\nOn 2026-08-20 it reported 0.4.12.\n"
        "<!-- specassay:stale-ok the only record of that trial -->\n"))
    assert proc.returncode == 0, proc.stderr


# --- the declared range must match the manifest --------------------------


def test_AC_DOCS_20_a_quoted_range_must_match_the_bundle(tmp_path):
    proc = run(build(tmp_path, "# T\n\nThe manifests accept `>=0.14.0`.\n"))
    assert proc.returncode == 1
    assert "bundle.yml declares" in proc.stderr


# --- regressions: the bugs the first sweep found in this checker ----------


def test_a_subheading_does_not_clear_the_date_its_parent_section_set(tmp_path):
    """Bug one. A dated ledger failed 91 times because `### detail` under
    `## 0.5.1 (2026-09-17)` read as undated."""
    proc = run(build(tmp_path,
        "# T\n\n## Release notes, 2026-09-17\n\n### A detail\n\nIt reported 0.4.13 then.\n"))
    assert proc.returncode == 0, proc.stderr


def test_a_heading_that_names_a_version_scopes_its_section(tmp_path):
    """Bug two. A section titled for the release it describes was being
    age-refused, though its own title says how old it is."""
    proc = run(build(tmp_path,
        "# T\n\n## v0.4.12 cut, 2026-08-20\n\nThe assets were 0.4.12.\n"))
    assert proc.returncode == 0, proc.stderr


def test_a_mark_covers_the_block_it_sits_in_not_only_its_line(tmp_path):
    """Bug three. Prose wraps, so requiring the mark on the exact line made an
    author break their own line wrapping to satisfy the checker."""
    proc = run(build(tmp_path,
        "# T\n\nA long sentence that mentions 0.4.13 and then wraps\n"
        "onto a second line. <!-- specassay:provenance -->\n"))
    assert proc.returncode == 0, proc.stderr


def test_a_pinned_dependency_is_not_measured_against_our_own_version(tmp_path):
    """Bug four. Marking Spec Kit's pinned 1.0.4 as a current claim made the
    checker demand it equal SpecAssay's version."""
    proc = run(build(tmp_path,
        "# T\n\nPinned to Spec Kit 1.0.4. <!-- specassay:pinned Spec Kit -->\n"))
    assert proc.returncode == 0, proc.stderr


def test_quoted_output_in_a_fenced_block_is_data_not_a_claim(tmp_path):
    proc = run(build(tmp_path,
        "# T\n\n```text\nSpecAssay Check 0.4.13\n```\n"))
    assert proc.returncode == 0, proc.stderr


def test_the_version_being_cut_defaults_to_the_bundle_manifest(tmp_path):
    proc = run(build(tmp_path, "# T\n\nBoth report 0.5.1. <!-- specassay:current -->\n"))
    assert proc.returncode == 0
    assert "version being cut: 0.5.1" in proc.stdout


def test_an_explicit_version_overrides_the_manifest(tmp_path):
    """What the release workflow does: check the docs against the tag."""
    proc = run(build(tmp_path, "# T\n\nBoth report 0.5.1. <!-- specassay:current -->\n"),
               version="v0.6.0")
    assert proc.returncode == 1
    assert "the version being cut is 0.6.0" in proc.stderr


# --- regressions: what phase two's corpus forced --------------------------


def test_a_scoping_heading_classifies_its_section_not_only_its_age(tmp_path):
    """Bug five, same shape as bug four one level up. A heading carrying
    stale-ok exempted its section from the age rule but did not classify it, so
    an author who had answered the question on the heading was still refused
    for not answering it."""
    proc = run(build(tmp_path,
        "# T <!-- specassay:stale-ok closed history, kept as written -->\n"
        "\nThe assets were 0.4.12 and the floor was 0.4.9.\n"))
    assert proc.returncode == 0, proc.stderr


def test_a_version_of_another_subject_in_this_repo_is_pinnable(tmp_path):
    """Phase two's finding. The dig report carries its own generatorVersion,
    bumped on its own schedule. It is not a dependency and not an observation
    of the bundle: it is a second version line inside this repository, which
    the checker had assumed away.

    This test passes against the pre-phase-two checker too, and is pinned here
    anyway. Nothing in the mechanism had to change; what was wrong was the
    class's stated meaning, "somebody else's version", which tells an author
    reading the refusal that their own second version line does not qualify. A
    checker that accepts the right thing for a reason nobody can find is one
    document away from being worked around."""
    proc = run(build(tmp_path,
        "# T\n\ngeneratorVersion bumps 0.3.0 to 0.4.0.\n"
        "<!-- specassay:pinned dig report generatorVersion -->\n"))
    assert proc.returncode == 0, proc.stderr


def test_an_unclassified_number_is_told_about_every_class(tmp_path):
    """The refusal has to name the way out, including the class phase two
    renamed. An author reading 'somebody else's version' does not see that
    their own second version line qualifies."""
    proc = run(build(tmp_path, "# T\n\nIt was 0.4.13.\n"))
    assert proc.returncode == 1
    assert "belonging to another subject" in proc.stderr
