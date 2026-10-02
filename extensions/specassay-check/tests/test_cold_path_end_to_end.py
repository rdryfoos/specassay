"""US-COLD-10, FR-COLD-40: the cold path, performed, with nothing done by hand.

The test the 2026-09-26 ledger lacked. It builds a throwaway git repository, puts
the bundle's files where an install puts them, and then walks a stranger's whole
path to a Thread Report comment using **only commands the bundle ships** plus the
ordinary git and editor actions any project involves.

How it fails if a step needs a hand: every command is declared in `STEPS` before it
runs, and `test_the_cold_path_needs_no_plumbing` asserts that each one is either a
shipped script or a plain `git` call. A hand-built step could not be added to make
this pass without failing that assertion, which is the whole point: the ledger's
complaint was never that the path was impossible, it was that the path was
undocumented plumbing.

What is not covered here, stated plainly rather than implied: GitHub posting the
comment. The comment's body is the marker line plus `report.md`, which this test
produces and reads, so what is untested is one API call in a workflow step whose
script is asserted elsewhere (`test_cold_30_ci_workflow.py`). A test that posted a
real comment would need a real repository and a real pull request.
"""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
EXT_SRC = REPO / "extensions" / "specassay-check"
PRESET_SRC = REPO / "presets" / "specassay"

# What a stranger types. Each entry is (label, argv). argv[0] is either `git` or a
# path under the installed extension; nothing else is allowed, and the assertion
# at the end of this file is what enforces it.
SHIPPED = ".specify/extensions/specassay-check/scripts"


def assert_only_shipped(commands):
    """Every step was a shipped script or a plain git call, or this raises.

    The rule the whole path is held to, in one function so that the rule itself
    can be tested rather than only applied.
    """
    for argv in commands:
        if argv and argv[0] == "git":
            continue
        if not (len(argv) > 1 and argv[0] == "bash"
                and argv[1].startswith(SHIPPED + "/")):
            raise AssertionError(
                f"a step outside the shipped tools: {' '.join(argv)}"
            )


def _run(argv, cwd, check=True):
    proc = subprocess.run(
        argv, cwd=cwd, capture_output=True, text=True, timeout=120,
        env={**os.environ, "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
             "GIT_AUTHOR_NAME": "Cold Path", "GIT_AUTHOR_EMAIL": "cold@example.com",
             "GIT_COMMITTER_NAME": "Cold Path", "GIT_COMMITTER_EMAIL": "cold@example.com"},
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"{' '.join(argv)} failed ({proc.returncode})\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )
    return proc


def _install(root: Path):
    """What `specify init` plus `specify bundle install specassay` leaves on disk.

    Copied rather than installed through the CLI on purpose: this test has to run
    in CI against *this branch*, and `specify bundle install` resolves the last
    released version from the public catalogs. The install's own shape is proved
    elsewhere, by running the real CLI; what is proved here is that the files it
    places are enough.
    """
    ext = root / ".specify" / "extensions" / "specassay-check"
    ext.parent.mkdir(parents=True)
    shutil.copytree(EXT_SRC, ext)
    shutil.copytree(PRESET_SRC, root / ".specify" / "presets" / "specassay")
    # `specify extension add` scaffolds the config from the template.
    shutil.copy(ext / "config-template.yml", ext / "specassay-check-config.yml")


@pytest.fixture
def cold_repo(tmp_path):
    root = tmp_path / "strangerrepo"
    root.mkdir()
    _run(["git", "init", "-q", "-b", "main", "."], root)
    _install(root)
    (root / "README.md").write_text("# A project with nothing on it yet\n")
    _run(["git", "add", "-A"], root)
    _run(["git", "commit", "-qm", "A blank repository, plus Spec Kit, plus SpecAssay"], root)
    return root


def test_AC_COLD_40a_the_cold_path_needs_no_plumbing(cold_repo):
    """@covers US-COLD-10, FR-COLD-40, AC-COLD-40a"""
    root = cold_repo
    commands = []

    def shipped(script, *args, check=True):
        argv = ["bash", f"{SHIPPED}/{script}", *args]
        commands.append(argv)
        return _run(argv, root, check=check)

    def git(*args, check=True):
        argv = ["git", *args]
        commands.append(argv)
        return _run(argv, root, check=check)

    # 1. A registry to start from. Nothing was created by the install, and this is
    #    the command /start gives.
    init = shipped("mint-id.sh", "--init")
    assert (root / "PRD.md").exists()
    assert "registry seed" in init.stderr

    # 2. The Gate on a registry with no promises in it: green, and saying the green
    #    proves nothing.
    first = shipped("check-traceability.sh", check=False)
    assert first.returncode == 0, first.stderr
    assert "registry empty" in first.stdout
    assert json.loads((root / "trace-manifest.json").read_text())["rows"] == [], (
        "the seed's fenced example rows were read as promises"
    )

    # 3. Mint one promise, with its author named. No ID is composed by hand.
    mint = shipped(
        "mint-id.sh", "AC", "GREET", "--authorship", "case",
        "--append", 'Given a name, when the greeter runs, then it returns "Hello, <name>!".',
    )
    assert mint.stdout.strip() == "AC-GREET-10"
    assert "**Authorship**: case" in (root / "PRD.md").read_text()

    # 4. The first honest red: a promise with nothing behind it.
    red = shipped("check-traceability.sh", check=False)
    assert red.returncode == 1
    assert "silent gap: AC-GREET-10" in red.stderr

    # 5. The spec and the task. A stranger writes these through Spec Kit's own
    #    /speckit-specify and /speckit-tasks, whose templates the preset has
    #    already amended; the files are the user's own content either way, which is
    #    why writing them here is not a hand-built step.
    (root / "specs" / "greet").mkdir(parents=True)
    (root / "specs" / "greet" / "spec.md").write_text(
        "# Feature Spec — Greeter\n\n"
        "Inherits its registry IDs from `PRD.md`.\n\n"
        "## Acceptance criteria\n\n"
        '- AC-GREET-10 — Given a name, when the greeter runs, then it returns "Hello, <name>!".\n'
    )
    (root / "specs" / "greet" / "tasks.md").write_text(
        "# Tasks — Greeter\n\n"
        "- [ ] T001 Build the greeter and write its proof — **Carries**: AC-GREET-10\n"
    )
    green = shipped("check-traceability.sh", check=False)
    assert green.returncode == 0, green.stderr
    assert "OK (1 registry IDs)" in green.stdout

    # 6. The base commit: the thread as it stands before the change.
    git("add", "-A")
    git("commit", "-qm", "Mint AC-GREET-10 with its spec and task")
    base_sha = _run(["git", "rev-parse", "HEAD"], root).stdout.strip()

    # 7. The CI that posts the report. One command, and nothing to wire up.
    ci = shipped("install-ci.sh")
    assert (root / ".github" / "workflows" / "specassay.yml").exists()
    assert "pull request" in ci.stderr

    # 8. Build it and prove it: the change the pull request would carry.
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src" / "greet.py").write_text(
        '"""The greeter.\n\n@covers AC-GREET-10\n"""\n\n\ndef greet(name):\n'
        '    return f"Hello, {name}!"\n'
    )
    (root / "src" / "banner.py").write_text(
        '"""A helper written along the way. It carries no @covers mark."""\n\n\n'
        'def banner(text):\n    return "=" * len(text)\n'
    )
    (root / "tests" / "test_greet.py").write_text(
        "from src.greet import greet\n\n\n"
        "def test_AC_GREET_10_greets_by_name():\n"
        '    assert greet("Tom") == "Hello, Tom!"\n'
    )
    (root / "specs" / "greet" / "tasks.md").write_text(
        "# Tasks — Greeter\n\n"
        "- [x] T001 Build the greeter and write its proof — **Carries**: AC-GREET-10\n"
    )
    git("add", "-A")
    git("commit", "-qm", "Build and prove AC-GREET-10")

    # 9. What CI does on the pull request, run by the same script CI runs.
    out = root / "ci-out"
    report_run = shipped(
        "ci-thread-report.sh", "--base-sha", base_sha, "--out-dir", str(out),
    )
    assert report_run.returncode == 0, report_run.stderr

    report = (out / "report.md").read_text()

    # The comment's text: the verdict line, the row that moved, who authored it,
    # and the file that changed alongside with nothing tying it to the thread.
    assert "🧵 Thread Report" in report
    assert "🟢 **Ready to review**" in report
    assert re.search(r"`AC-GREET-10` \| `tracked-debt` → .*`proven`", report), report
    assert "came from the case" in report, "the authorship sentence is missing"
    assert "src/banner.py" in report, "the off-thread file is missing"

    head = json.loads((out / "head.json").read_text())
    assert head["gate"]["ok"] is True, head["gate"]["failures"]

    # 10. Nothing in the path was plumbing. Every command was a shipped script or
    #     a plain git call; a hand-built step would show up here.
    assert_only_shipped(commands)
    scripts = {Path(a[1]).name for a in commands if a[0] == "bash"}
    assert scripts == {
        "mint-id.sh", "check-traceability.sh", "install-ci.sh", "ci-thread-report.sh",
    }, scripts


def test_AC_COLD_40b_a_step_outside_the_shipped_tools_fails_the_proof():
    """@covers AC-COLD-40b

    The guard above is what makes the path's claim mean anything: without it, the
    test could be made to pass by adding whatever hand-built step the path turned
    out to need. So the guard is held to its own test.
    """
    ok = [
        ["git", "commit", "-qm", "x"],
        ["bash", f"{SHIPPED}/mint-id.sh", "--init"],
    ]
    assert_only_shipped(ok)

    for hand_built in (
        ["bash", "scripts/my-own-plumbing.sh"],
        ["python3", f"{SHIPPED}/thread-report.py", "--base", "b.json"],
        ["gh", "pr", "comment", "1", "--body-file", "report.md"],
        ["bash", "-c", "cp report.md /tmp/"],
    ):
        with pytest.raises(AssertionError) as caught:
            assert_only_shipped([*ok, hand_built])
        assert " ".join(hand_built) in str(caught.value), (
            "the failure does not name the step it refused"
        )
