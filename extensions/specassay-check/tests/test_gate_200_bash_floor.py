"""FR-GATE-200: the bash floor the bundle claims, held to on every runner.

0.5.4 shipped `carries_verdict="$( ... <<'CARRIESPY' ... )"`: a here-document
inside a command substitution. bash 4 and newer parse it. bash 3.2.57, which is
macOS's system bash and the only bash on a stock Mac, does not: it scans for the
closing paren without honouring the here-document, reads the Python body as
shell, and the file then fails to parse hundreds of lines further on with an error
that names neither the line nor the cause. The Gate ran nothing on every Mac for
one release.

Two guards, because one was not enough and never will be. The macOS CI job runs
the real 3.2 against the real scripts, which is the only authority on what 3.2
accepts. These tests are the cheap one that runs everywhere, including on the
Linux runner that missed this: they refuse the known construct by shape, and they
hold `extension.yml` to naming the floor rather than saying "bash" and meaning
"whichever bash the author happened to have".
"""

import re
import subprocess
from pathlib import Path

EXT = Path(__file__).resolve().parents[1]
SHIPPED = sorted(EXT.glob("scripts/*.sh"))


def _heredocs_inside_command_substitution(text: str):
    """Line numbers where a here-document opens while a `$(` is still open.

    Crude on purpose: it counts `$(` against `)` rather than parsing bash, which
    is exactly the accounting bash 3.2 gets wrong, and it is looking for a shape
    rather than proving a grammar. A false positive is a line to rewrite anyway.
    """
    depth, hits = 0, []
    for n, line in enumerate(text.splitlines(), 1):
        if depth > 0 and re.search(r"<<-?'?[A-Za-z_]", line):
            hits.append(n)
        depth += line.count("$(") - line.count(")")
        if depth < 0:
            depth = 0
    return hits


def test_AC_GATE_200a_no_shipped_script_hides_a_heredoc_in_a_command_substitution():
    """@covers AC-GATE-200a"""
    assert SHIPPED, "no shipped scripts found; this test is not looking where it thinks"
    for path in SHIPPED:
        hits = _heredocs_inside_command_substitution(path.read_text(encoding="utf-8"))
        assert hits == [], (
            f"{path.name} opens a here-document inside a command substitution at "
            f"line(s) {hits}. bash 3.2, which is macOS's system bash, cannot parse "
            "that. Redirect the here-document to a file and read the file."
        )


def test_AC_GATE_200a_every_shipped_script_parses():
    """@covers AC-GATE-200a

    Under this runner's bash, which on the Linux job is 5.x and on the macOS job is
    3.2.57. The same test, two parsers, and the one that matters is whichever one
    the caller has.
    """
    for path in SHIPPED:
        proc = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        assert proc.returncode == 0, f"{path.name} does not parse:\n{proc.stderr}"


def test_AC_GATE_200b_the_manifest_names_the_bash_floor():
    """@covers AC-GATE-200b

    `tools: bash` with no version said nothing, and what nobody wrote down nobody
    tested. The floor is 3.2 because that is what a stock Mac has.
    """
    manifest = (EXT / "extension.yml").read_text(encoding="utf-8")
    block = manifest.split("tools:", 1)[1].split("provides:", 1)[0]
    bash_entry = re.search(r'-\s*name:\s*"?bash"?(.*?)(?=-\s*name:|\Z)', block, re.S)
    assert bash_entry, "extension.yml does not list bash under requires.tools"
    assert re.search(r'version:\s*"?>=\s*3\.2', bash_entry.group(1)), (
        "extension.yml does not declare the bash floor it is tested against"
    )


def test_AC_GATE_200c_ci_runs_the_suite_on_a_mac_with_its_system_bash():
    """@covers AC-GATE-200c

    Read from the workflow rather than trusted: the Linux-only job is how a
    release shipped that could not run on any Mac.
    """
    wf = (EXT.parents[1] / ".github" / "workflows" / "self-gate.yml").read_text(encoding="utf-8")
    assert "macos" in wf, "no macOS runner in self-gate.yml"
    # The system bash, by absolute path: `bash` in PATH on a GitHub macOS runner
    # can be Homebrew's 5.x, which is not what an adopter's Mac runs by default.
    assert "/bin/bash" in wf, (
        "the macOS job does not name /bin/bash, so it may be testing Homebrew's bash"
    )
