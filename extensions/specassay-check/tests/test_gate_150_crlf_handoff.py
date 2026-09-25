"""FR-GATE-150, AC-GATE-150: a file Python writes and Bash reads must match
even when the write lands CRLF.

Found on the first Windows run of the Bang walk, 2026-09-24: Git Bash,
Python 3.12.10. `trace-manifest.json` came back `"ok": false` with eleven
failures, all of one shape:

    untraced scope (test name): AC-UI-10\\r not in registry

with `GAP: 0` and the same IDs carrying `proven` rows and passing tests.
Nothing was wrong with the code under test. The Gate was failing on its own
plumbing: the junit filter rewrote `test_acs.txt` through Python's text mode,
which on Windows turns every `\\n` into `\\r\\n`, and the Bash reads that
follow compare `AC-UI-10\\r` against a registry holding `AC-UI-10`.

The asymmetry is what made it look like a data problem rather than a line
ending one: the manifest's own reader strips whitespace per line, so statuses
stayed right, while the Bash-side `grep -qx` and `comm` comparisons, which do
not, went wrong. A reader saw correct statuses beside impossible failures.

Reproduced here without Windows by injecting a Python shim that writes the
handoff files the way Windows text mode does. The shim is the only thing
pretending to be Windows; every line of the script under test is the real one.
"""

import json
import os
import stat
import sys

import pytest

SHIM = """#!/usr/bin/env bash
# Stand in for a Windows Python: run the real interpreter, then rewrite every
# file it was handed as an argument so it carries CRLF, which is what text
# mode does there.
"{real}" "$@"
rc=$?
for arg in "$@"; do
  case "$arg" in
    *.txt)
      if [[ -f "$arg" ]]; then
        "{real}" - "$arg" <<'PY'
import sys
p = sys.argv[1]
data = open(p, "rb").read()
if b"\\r\\n" not in data:
    open(p, "wb").write(data.replace(b"\\n", b"\\r\\n"))
PY
      fi
      ;;
  esac
done
exit $rc
"""


@pytest.fixture
def windows_python(tmp_path_factory):
    """A python3 that writes its .txt outputs with CRLF, as Windows does."""
    d = tmp_path_factory.mktemp("winpy")
    shim = d / "python3-crlf"
    shim.write_text(SHIM.format(real=sys.executable))
    shim.chmod(shim.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return str(shim)


def _fixture_with_passing_proof(project):
    """One AC, fully traced, with a real passing test named for it."""
    project.prd("- AC-UI-10 — the sign-in form shows an error on a bad password.")
    project.write("specs/ui/spec.md", "AC-UI-10\n")
    project.write("specs/ui/tasks.md", "- [x] T1 sign-in — **Carries**: AC-UI-10\n")
    project.write("src/ui.py", "# @covers AC-UI-10\ndef sign_in():\n    return True\n")
    project.write(
        "tests/test_ui.py",
        "def test_AC_UI_10_bad_password_shows_error():\n    assert True\n",
    )
    junit = project.root / "junit-results.xml"
    junit.write_text(
        '<?xml version="1.0"?>\n'
        '<testsuite>\n'
        '  <testcase classname="tests.test_ui" '
        'name="test_AC_UI_10_bad_password_shows_error"/>\n'
        '</testsuite>\n'
    )
    project.config(test_results=str(junit))


def test_AC_GATE_150_crlf_handoff_does_not_invent_untraced_scope(project, windows_python):
    """The reported failure, reproduced: CRLF in the handoff file must not
    turn a proven, registered AC into an orphan."""
    _fixture_with_passing_proof(project)
    proc, manifest = project.run(env={"SPECASSAY_PYTHON": windows_python})

    assert manifest is not None, proc.stderr
    failures = [f["detail"] for f in manifest["gate"].get("failures", [])]
    assert not any("not in registry" in d for d in failures), (
        "CRLF in a Python-written handoff file was read back with the carriage "
        "return attached, so a registered ID did not match the registry:\n  "
        + "\n  ".join(failures)
    )
    assert manifest["gate"]["ok"] is True, failures
    assert proc.returncode == 0, proc.stderr


def test_AC_GATE_150_crlf_handoff_keeps_the_row_proven(project, windows_python):
    """The other half of the reported picture: statuses were right while the
    failures were wrong, because the manifest's reader strips and the Bash
    comparisons do not. Both must be right, and for the same reason."""
    _fixture_with_passing_proof(project)
    proc, manifest = project.run(env={"SPECASSAY_PYTHON": windows_python})

    assert manifest is not None, proc.stderr
    row = project.row(manifest, "AC-UI-10")
    assert row["status"] == "proven", row
    assert manifest["gate"]["executionVerified"] is True
    # No ID anywhere in the manifest may carry a stray carriage return.
    blob = json.dumps(manifest)
    assert "\\r" not in blob, "a carriage return survived into the manifest"


def test_AC_GATE_150_crlf_does_not_fabricate_uncovered_proof(project, windows_python):
    """`comm -23 test_acs.txt covers.txt` is the other Bash-side comparison
    the handoff feeds. With CRLF on one side and not the other, every proven
    ID looks uncovered, so the diagnostic fires on IDs whose @covers line is
    right there in the source."""
    _fixture_with_passing_proof(project)
    proc, manifest = project.run(env={"SPECASSAY_PYTHON": windows_python})

    assert manifest is not None, proc.stderr
    diagnostics = [d["detail"] for d in manifest["gate"].get("diagnostics", [])]
    assert not any("uncovered proof" in d for d in diagnostics), diagnostics


def test_AC_GATE_150b_a_config_checked_out_with_crlf_reads_the_same(project):
    """The same defect one file over, found while fixing the handoff.

    Git for Windows defaults to `core.autocrlf=true`, so a checked-out
    `specassay-check-config.yml` can arrive with CRLF. The readers took the
    rest of the line verbatim, so `registry: "PRD.md"` parsed as a filename
    with a carriage return on the end and the Gate refused with
    `registry not found: PRD.md`, naming a file that is right there.

    The reported Windows run never hit this, because the extension installer
    writes the config with LF. A user who edits or re-checks-out that file on
    Windows would.
    """
    project.prd("- AC-UI-10 — the sign-in form shows an error on a bad password.")
    project.write("specs/ui/spec.md", "AC-UI-10\n")
    project.write("specs/ui/tasks.md", "- [ ] T1 sign-in — **Carries**: AC-UI-10\n")

    # Run it twice, LF then CRLF, and compare: "reads the same" is the claim,
    # so assert it against the LF run rather than against a status this test
    # guesses at. The first draft guessed wrong, which is the argument.
    project.config()
    lf_text = project._config.read_text()
    lf_proc, lf_manifest = project.run()
    assert lf_manifest is not None, lf_proc.stderr

    project._config.write_bytes(lf_text.replace("\n", "\r\n").encode("utf-8"))
    crlf_proc, crlf_manifest = project.run()

    assert crlf_manifest is not None, crlf_proc.stderr + crlf_proc.stdout
    assert "registry not found" not in crlf_proc.stderr, crlf_proc.stderr
    # The scalar reader (registry) and the list reader (test_globs, src_globs)
    # are separate code paths, and a whole manifest exercises both.
    assert crlf_manifest["rows"] == lf_manifest["rows"]
    assert crlf_manifest["gate"]["ok"] == lf_manifest["gate"]["ok"]
    assert crlf_manifest["gate"]["ok"] is True, crlf_manifest["gate"].get("failures")
