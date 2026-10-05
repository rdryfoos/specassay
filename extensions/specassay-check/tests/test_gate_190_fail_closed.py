"""FR-GATE-190: a check that cannot run must be red.

0.5.4 shipped a construct macOS's system bash cannot parse, so on a stock Mac the
Gate ran nothing: no manifest, no verdict, no registry count. Found on a Mac Mini,
2026-10-02.

bash itself is honest about it: a parse failure exits 2 and executes nothing after
the point it gave up. What is not honest is what two ordinary ways of calling a
checker do with that status. A pipeline reports its last element's status, so
`check | tail` is 0. A `2>/dev/null` throws the message away. Either one turns
"this did not run" into a green line, which is how a broken Gate shipped and was
found by a person rather than by CI.

So the entry point is a small launcher that cannot itself be the thing that
breaks, and these tests hold it to three promises: it refuses an implementation it
cannot parse, it refuses any exit 0 that did not write a manifest, and it says so
on both streams, because the status is the one thing a caller can lose.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

EXT = Path(__file__).resolve().parents[1]
LAUNCHER = EXT / "scripts" / "check-traceability.sh"
IMPL = EXT / "scripts" / "check-traceability.impl.sh"


def _fixture(tmp_path):
    """A project the Gate passes, with its own copy of the extension to break."""
    ext = tmp_path / "ext"
    shutil.copytree(EXT, ext)
    proj = tmp_path / "proj"
    (proj / "specs" / "backlog").mkdir(parents=True)
    (proj / "PRD.md").write_text(
        "# Fixture PRD\n\n- AC-FIX-10 — a thing. **Authorship**: design\n")
    (proj / "specs" / "backlog" / "spec.md").write_text("# spec\n\n- AC-FIX-10 — a thing.\n")
    (proj / "specs" / "backlog" / "tasks.md").write_text(
        "- [ ] T1 Do it — **Carries**: AC-FIX-10\n")
    (ext / "specassay-check-config.yml").write_text(
        'registry: "PRD.md"\ntarget_name: "fixture"\n'
        'manifest_path: "trace-manifest.json"\n'
        'specs: "specs/**/spec.md"\ntasks: "specs/**/tasks.md"\n'
        'src_globs:\n  - "src/**"\ntest_globs:\n  - "tests/**"\n')
    return ext, proj


def _run(ext, proj, pipe=False):
    cmd = ["bash", str(ext / "scripts" / "check-traceability.sh")]
    env = {**os.environ,
           "SPECASSAY_PROJECT_ROOT": str(proj),
           "SPECASSAY_CONFIG": str(ext / "specassay-check-config.yml")}
    return subprocess.run(cmd, cwd=proj, env=env, capture_output=True, text=True,
                          timeout=120)


def test_the_launcher_passes_a_good_run_through_untouched(tmp_path):
    """The guard must not change what a working run says or returns."""
    ext, proj = _fixture(tmp_path)
    proc = _run(ext, proj)
    assert proc.returncode == 0, proc.stderr
    assert "OK (1 registry IDs)" in proc.stdout
    assert "FAILED to run" not in proc.stdout + proc.stderr
    assert (proj / "trace-manifest.json").is_file()


def test_AC_GATE_190a_an_unparseable_check_is_refused_not_passed(tmp_path):
    """@covers AC-GATE-190a

    The deliberately broken copy. An unterminated `if` is the same failure class
    as the 0.5.4 defect: bash reports it at a line far from the cause, or at the
    end of the file, and nothing the implementation contains can report it,
    because the implementation never starts.

    Appended rather than inserted at a line number. A fixed line number drifts
    with every edit to the implementation, and on 2026-10-05 it drifted into a
    Python here-document, where `if true; then` is text and the copy parsed
    perfectly well. The control now proves the copy is broken before it asks
    the launcher to notice.
    """
    ext, proj = _fixture(tmp_path)
    impl = ext / "scripts" / "check-traceability.impl.sh"
    impl.write_text(impl.read_text() + "\nif true; then : # deliberately never closed\n")
    parse = subprocess.run(
        ["bash", "-n", str(impl)], capture_output=True, text=True, timeout=30
    )
    assert parse.returncode != 0, "the broken copy parses; this control proves nothing"

    proc = _run(ext, proj)
    assert proc.returncode != 0, "a Gate that cannot run returned success"
    assert proc.returncode == 2
    assert not (proj / "trace-manifest.json").exists(), (
        "a run that never happened left a manifest behind")
    assert "FAILED to run" in proc.stdout
    assert "cannot parse the check" in proc.stdout
    # The bash that could not parse it is named, because that is the whole
    # diagnosis: on the Mac Mini it was 3.2.57 and nothing said so.
    assert "bash " in proc.stdout
    # And the parser's own words are kept, for a bug report.
    assert "syntax error" in proc.stderr


def test_AC_GATE_190b_an_exit_zero_without_a_manifest_is_refused(tmp_path):
    """@covers AC-GATE-190b

    The implementation replaced by one that parses, runs, prints a cheerful line
    and writes nothing. That is what every silent-startup failure looks like from
    outside, and it is the shape the launcher exists to catch.
    """
    ext, proj = _fixture(tmp_path)
    impl = ext / "scripts" / "check-traceability.impl.sh"
    impl.write_text("#!/usr/bin/env bash\necho 'SpecAssay Check (Gate 2): OK (0 registry IDs)'\nexit 0\n")

    proc = _run(ext, proj)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "FAILED to run" in proc.stdout
    assert "without writing a manifest" in proc.stdout
    assert not (proj / "trace-manifest.json").exists()


def test_AC_GATE_190c_the_refusal_reaches_both_streams_and_is_one_line(tmp_path):
    """@covers AC-GATE-190c

    A pipeline keeps its last element's status, so no checker can force a caller
    to read its exit code. What it can do is put the refusal where the verdict
    would have been, so `check | tail -1` reads the refusal rather than a green
    line. One line on each stream, and no more: this is the sentence a caller
    sees instead of a verdict.
    """
    ext, proj = _fixture(tmp_path)
    impl = ext / "scripts" / "check-traceability.impl.sh"
    impl.write_text("#!/usr/bin/env bash\nexit 0\n")

    proc = _run(ext, proj)
    out_lines = [l for l in proc.stdout.splitlines() if l.strip()]
    err_lines = [l for l in proc.stderr.splitlines() if l.strip()]
    assert len(out_lines) == 1, out_lines
    assert out_lines == err_lines, "the two streams disagree about what happened"
    assert out_lines[0].startswith("SpecAssay Check (Gate 2): FAILED to run -- ")

    # What a caller that pipes and ignores the status actually reads.
    piped = subprocess.run(
        f'bash {ext}/scripts/check-traceability.sh 2>/dev/null | tail -1',
        shell=True, cwd=proj, capture_output=True, text=True, timeout=120,
        env={**os.environ, "SPECASSAY_PROJECT_ROOT": str(proj),
             "SPECASSAY_CONFIG": str(ext / "specassay-check-config.yml")})
    assert "FAILED to run" in piped.stdout, (
        "a piping caller still reads something that looks like a pass")


def test_a_missing_implementation_is_refused_by_name(tmp_path):
    ext, proj = _fixture(tmp_path)
    (ext / "scripts" / "check-traceability.impl.sh").unlink()
    proc = _run(ext, proj)
    assert proc.returncode == 2
    assert "the check itself is missing" in proc.stdout
    assert "check-traceability.impl.sh" in proc.stdout
