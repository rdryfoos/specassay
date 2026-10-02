"""FR-COLD-30: the bundle ships the CI that posts the Thread Report.

Gap (d) and (e) of the cold path. Reproduced 2026-10-02 on 0.5.4: `find .github
-type f` after a full install returned nothing, so a pull request ran nothing and
no comment appeared, and what a stranger had to write for themselves was the
124-line workflow this repository had written for its own example app.

These tests run the real installer against throwaway directories and read the
shipped workflow as text. What they cannot do is run GitHub Actions; the end-to-end
proof that the workflow's own sequence reaches a report lives in
`test_cold_path_end_to_end.py`.
"""

import re
import subprocess
from pathlib import Path

EXT = Path(__file__).resolve().parents[1]
INSTALL = EXT / "scripts" / "install-ci.sh"
WORKFLOW = EXT / "ci" / "specassay.yml"


def _repo(tmp_path, project_sub=""):
    """A git repo with the extension installed, optionally in a subdirectory."""
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "."], cwd=repo, check=True)
    project = repo / project_sub if project_sub else repo
    project.mkdir(parents=True, exist_ok=True)
    ext = project / ".specify" / "extensions" / "specassay-check"
    (ext / "scripts").mkdir(parents=True)
    (ext / "ci").mkdir(parents=True)
    for name in ("install-ci.sh", "check-traceability.sh"):
        (ext / "scripts" / name).write_text((EXT / "scripts" / name).read_text())
    (ext / "ci" / "specassay.yml").write_text(WORKFLOW.read_text())
    return repo, project, ext


def _install(project, ext, *args):
    return subprocess.run(
        ["bash", str(ext / "scripts" / "install-ci.sh"), *args],
        cwd=project,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin",
             "SPECASSAY_PROJECT_ROOT": str(project)},
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_AC_COLD_30a_install_ci_writes_the_workflow_and_is_idempotent(tmp_path):
    """@covers AC-COLD-30a"""
    repo, project, ext = _repo(tmp_path)
    installed = repo / ".github" / "workflows" / "specassay.yml"
    assert not installed.exists()

    first = _install(project, ext)
    assert first.returncode == 0, first.stderr
    assert installed.exists()
    assert installed.read_text() == WORKFLOW.read_text()
    # One line saying what the thing it just installed does, which is the half of
    # this promise a file comparison cannot see.
    assert "pull request" in first.stderr and "Gate" in first.stderr

    again = _install(project, ext)
    assert again.returncode == 0, again.stderr
    assert "unchanged" in again.stderr
    assert installed.read_text() == WORKFLOW.read_text()


def test_AC_COLD_30a_a_project_in_a_subdirectory_gets_its_own_root(tmp_path):
    """@covers AC-COLD-30a

    The workflow lands at the repository root, not beside the project, because
    that is the only place GitHub reads it from; and it carries the project's own
    root so nothing has to be edited by hand.
    """
    repo, project, ext = _repo(tmp_path, project_sub="app")
    proc = _install(project, ext)
    assert proc.returncode == 0, proc.stderr

    installed = repo / ".github" / "workflows" / "specassay.yml"
    assert installed.exists(), "the workflow was not written at the repository root"
    assert not (project / ".github").exists()
    assert '  SPECASSAY_PROJECT: "app"' in installed.read_text()

    # And a rerun on that project still reads as unchanged: the comparison is
    # against what this project's workflow should contain, not against the shipped
    # file. An earlier draft compared the shipped file and called a workflow
    # carrying the wrong project root "unchanged".
    again = _install(project, ext)
    assert "unchanged" in again.stderr, again.stderr


def test_AC_COLD_30b_a_differing_workflow_is_refused_not_overwritten(tmp_path):
    """@covers AC-COLD-30b"""
    repo, project, ext = _repo(tmp_path)
    installed = repo / ".github" / "workflows" / "specassay.yml"
    installed.parent.mkdir(parents=True)
    mine = "name: SpecAssay\n# my own edits\n"
    installed.write_text(mine)

    proc = _install(project, ext)
    assert proc.returncode != 0
    assert "differs" in proc.stderr
    assert ".github/workflows/specassay.yml" in proc.stderr
    assert installed.read_text() == mine, "a refusal still overwrote the file"

    forced = _install(project, ext, "--force")
    assert forced.returncode == 0, forced.stderr
    assert installed.read_text() == WORKFLOW.read_text()


def test_AC_COLD_30c_the_shipped_workflow_is_not_this_repository_s_own():
    """@covers AC-COLD-30c

    The workflow this repository runs on itself names `examples/example-app` and
    `extensions/specassay-check/scripts/...`, paths that exist nowhere else. A
    shipped workflow carrying any of them would run on nobody's project but ours.

    The four data steps live in `ci-thread-report.sh` rather than in the YAML, so
    that the end-to-end proof drives the same sequence CI drives; the workflow
    holds the two steps that need GitHub. Both halves are read here.
    """
    text = WORKFLOW.read_text()
    driver = (EXT / "scripts" / "ci-thread-report.sh").read_text()

    for body, label in ((text, "workflow"), (driver, "CI driver")):
        assert "examples/example-app" not in body, f"the {label} names our example app"
        # A path rooted at the repository rather than at the project: ours is
        # `extensions/specassay-check/...`, an adopter's is
        # `.specify/extensions/specassay-check/...`, so the test has to tell the
        # two apart rather than search for the shorter string inside the longer.
        assert not re.search(r"(?<!\.specify/)extensions/specassay-check", body), (
            f"the {label} names a path rooted at this repository"
        )

    # Every path derives from the project root the workflow is given.
    assert "SPECASSAY_PROJECT" in text
    assert "ci-thread-report.sh" in text
    assert "--project" in text

    # The four data steps, in the driver the proof runs.
    for piece in (
        "check-traceability.sh",   # the Gate, on the head
        "git worktree add",        # and on the base
        "git diff --name-only",    # the changed files
        "thread-report.py",        # the report
    ):
        assert piece in driver, f"the CI driver has no {piece} step"

    # The two steps that need GitHub, in the workflow.
    for piece in (
        "specassay-thread-report",  # the sticky comment's marker
        "updateComment",            # updated in place, not piled up
        "Requirements check failed", # the verdict, read from the manifest
    ):
        assert piece in text, f"the shipped workflow has no {piece} step"

    # The verdict is a separate step from the comment: the red tick is the block,
    # the comment never is.
    assert text.index("createComment") < text.index("Requirements check failed")
