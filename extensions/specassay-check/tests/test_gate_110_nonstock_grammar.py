"""The configured grammar must be consumed as configured.

Every test here fails against v0.4.13 and passes after the fix. They exist
because all four defects share one root: the front door accepts a
configurable grammar (`id_regex`, `test_ac_regex`, `retires_regex`) and the
back rooms assume the stock one. Found by running SpecAssay against a real
estate with dotted IDs (Chalkup's as-built audit, 2026-09-16, corroborated
by rdryfoos/chalkup#27); reproduced here independently, with fixtures that
own their own grammar rather than quoting that estate's.

The consequence that makes this class dangerous is not that the Gate is
wrong. It is that the Gate is *silently* wrong: an unreachable proof leaves
its criterion in `backlog`, which is a legal, passing state, so the Gate
stays green for ever while nothing ever becomes proven.
"""

import re
import subprocess
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
MINT = SCRIPTS / "mint-id.sh"

# A dotted grammar: AC-5.6.1a, FR-2.1. No domain segment, dots as
# separators, an optional trailing letter.
DOTTED_ID_RE = r"(AC|FR)-[0-9]+(\.[0-9]+)*[a-z]?"
DOTTED_TEST_AC_RE = r"AC_[0-9]+(_[0-9]+)*(_[a-z])?"

# An underscore-bearing grammar: AC_LOGIN_10. The stock hyphen/underscore
# swap cannot round-trip this either, in the opposite direction.
UNDERSCORE_ID_RE = r"AC_[A-Z]+_[0-9]+"
UNDERSCORE_TEST_AC_RE = r"AC_[A-Z]+_[0-9]+"


def write_config(project, **overrides) -> Path:
    """Exact config text, so a non-stock grammar reaches the script verbatim.

    conftest's `config()` appends the stock regexes after any override, which
    is fine for stock fixtures and confusing here.
    """
    cfg = {
        "registry": "PRD.md",
        "target_name": "fixture",
        "manifest_path": "trace-manifest.json",
        "specs": "specs/**/spec.md",
        "tasks": "specs/**/tasks.md",
        "id_regex": DOTTED_ID_RE,
        "covers_regex": "@covers[[:space:]]+.*",
        "carries_regex": r"\*\*(Carries|Traces)\*\*:",
        "retires_regex": r"\*\*Retires\*\*:",
        "test_ac_regex": DOTTED_TEST_AC_RE,
    }
    cfg.update(overrides)
    lines = [f'{k}: "{v}"' for k, v in cfg.items()]
    lines += ['src_globs:', '  - "src/**"', 'test_globs:', '  - "tests/**"']
    return project.raw_config("\n".join(lines) + "\n")


# --- DEFECT ONE: the proof direction ----------------------------------


def test_dotted_id_is_proven_by_its_named_test(project):
    """A test named for a dotted criterion proves it.

    v0.4.13 reconstructs the ID from the test name with `tr '_' '-'`, so
    `test_AC_5_6_1_a_...` yields `AC-5-6-1-a`, which matches no registry
    entry, and the criterion can never be reached by any test.
    """
    write_config(project)
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")
    project.write("specs/cards/spec.md", "# Cards\n\n- AC-5.6.1a — as above.\n")
    project.write(
        "specs/cards/tasks.md",
        "# Tasks\n\n- [x] T001 Replay on reconnect — **Carries**: AC-5.6.1a\n",
    )
    project.write("src/cards.py", '"""Cards.\n\n@covers AC-5.6.1a\n"""\n')
    project.write(
        "tests/test_cards.py",
        "def test_AC_5_6_1_a_replays_queued_cards():\n    assert True\n",
    )

    proc, manifest = project.run()
    row = project.row(manifest, "AC-5.6.1a")

    assert row["status"] == "proven", (
        f"dotted criterion unreachable by its own test; got {row['status']} "
        f"with proofs={row.get('proofs')}. stdout:\n{proc.stdout}"
    )
    assert len(row["proofs"]) == 1
    assert row["proofs"][0]["name"] == "test_AC_5_6_1_a_replays_queued_cards"


def test_dotted_id_gap_is_not_silently_green(project):
    """The dangerous shape: green for ever while nothing is proven.

    With the criterion carried by an open task it sits in `backlog`, a
    legal passing state, so v0.4.13 exits 0 and reports nothing wrong even
    though a real, passing, correctly named test exists and is ignored.
    """
    write_config(project)
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")
    project.write(
        "specs/cards/tasks.md",
        "# Tasks\n\n- [ ] T001 Replay on reconnect — **Carries**: AC-5.6.1a\n",
    )
    project.write(
        "tests/test_cards.py",
        "def test_AC_5_6_1_a_replays_queued_cards():\n    assert True\n",
    )

    proc, manifest = project.run()
    row = project.row(manifest, "AC-5.6.1a")

    assert row["status"] == "proven", (
        "a named, passing test existed and the criterion still read "
        f"{row['status']} on a green run (exit {proc.returncode}); that is "
        "the silent failure this class produces"
    )


def test_underscore_bearing_id_round_trips(project):
    """The same defect in the other direction: IDs that contain underscores."""
    write_config(
        project,
        id_regex=UNDERSCORE_ID_RE,
        test_ac_regex=UNDERSCORE_TEST_AC_RE,
    )
    project.prd("- AC_LOGIN_10 — A wrong password shows an error.")
    project.write("specs/login/spec.md", "# Login\n\n- AC_LOGIN_10 — as above.\n")
    project.write(
        "specs/login/tasks.md",
        "# Tasks\n\n- [x] T001 Sign-in errors — **Carries**: AC_LOGIN_10\n",
    )
    project.write(
        "tests/test_login.py",
        "def test_AC_LOGIN_10_shows_an_error():\n    assert True\n",
    )

    proc, manifest = project.run()
    row = project.row(manifest, "AC_LOGIN_10")

    assert row["status"] == "proven", (
        f"underscore-bearing ID did not round-trip; got {row['status']}. "
        f"stdout:\n{proc.stdout}"
    )


def test_dotted_id_is_execution_verified_from_a_junit_report(project):
    """The JUnit matcher carries the same hardcode as the proof scan.

    `id_forms()` offered only `{id, id.replace("-", "_")}`, so a dotted ID
    never matched a test label even once the proof scan found it.
    """
    write_config(project, test_results="report.xml")
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")
    project.write("specs/cards/spec.md", "# Cards\n\n- AC-5.6.1a — as above.\n")
    project.write(
        "specs/cards/tasks.md",
        "# Tasks\n\n- [x] T001 Replay — **Carries**: AC-5.6.1a\n",
    )
    project.write(
        "tests/test_cards.py",
        "def test_AC_5_6_1_a_replays_queued_cards():\n    assert True\n",
    )
    project.write(
        "report.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<testsuites><testsuite name="CardTests" tests="1" failures="0">\n'
        '  <testcase classname="CardTests" '
        'name="test_AC_5_6_1_a_replays_queued_cards()" time="0.01"/>\n'
        "</testsuite></testsuites>\n",
    )

    proc, manifest = project.run()
    row = project.row(manifest, "AC-5.6.1a")

    assert manifest["gate"]["executionVerified"] is True
    assert row["status"] == "proven", (
        f"passing testcase in the report did not verify the dotted ID; got "
        f"{row['status']}. stdout:\n{proc.stdout}"
    )


# --- DEFECT TWO: the interpolation ------------------------------------


def test_alternation_in_id_regex_does_not_escape_the_def_line_anchor(project):
    """A top-level alternation in `id_regex` must not unanchor the pattern.

    `def_line_regex` interpolated the configured value bare into
    `^...%s...$`, so the trailing branch matched anywhere on any line. Every
    prose mention then read as a definition line, and the duplicate-ID
    check refused a registry that mints each ID exactly once.
    """
    write_config(
        project,
        id_regex="AC-[0-9]+|FR-[0-9]+",
        test_ac_regex="AC_[0-9]+",
    )
    project.prd(
        "- FR-2 — The deck syncs across devices.",
        "",
        "Prose that merely cites FR-2 is not a second mint of it.",
        "Nor is this table row:",
        "",
        "| FR-2 | sync | shipped |",
    )
    project.write("specs/sync/spec.md", "# Sync\n\n- FR-2 — as above.\n")
    project.write(
        "specs/sync/tasks.md",
        "# Tasks\n\n- [ ] T001 Sync the deck — **Carries**: FR-2\n",
    )

    proc, manifest = project.run()

    failures = [f["kind"] for f in manifest["gate"].get("failures", [])]
    assert "duplicate-id" not in failures, (
        "a prose mention was read as a second definition line, so the "
        f"alternation escaped the anchor. failures={failures}\n{proc.stdout}"
    )
    assert manifest["gate"]["ok"] is True, proc.stdout


# --- DEFECT THREE: the rest of the family -----------------------------


def test_retires_regex_containing_a_slash_still_parses(project):
    """A configured mark is data, not part of a sed command's syntax.

    `sed -E "s/^.*${RETIRES_RE}[[:space:]]*//"` interpolated the configured
    pattern into the substitution itself, so a value containing `/` broke
    the command rather than changing its meaning.
    """
    write_config(project, retires_regex=r"\*\*Retires/Withdraws\*\*:")
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")
    project.write(
        "specs/cards/tasks.md",
        "# Tasks\n\n"
        "- [ ] T001 Withdraw the card replay — "
        "**Retires/Withdraws**: AC-5.6.1a (2026-09-16): superseded by the "
        "new queue design.\n",
    )

    proc, manifest = project.run()

    # v4 carries retirement as a top-level record; the row leaves rows[].
    retired = manifest.get("retired", [])
    assert [r["id"] for r in retired] == ["AC-5.6.1a"], (
        f"retirement record did not parse with a slash in the mark; "
        f"retired={retired}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    )
    assert retired[0]["date"] == "2026-09-16"
    assert "new queue design" in retired[0]["reason"]


def test_invented_id_is_reported_when_the_grammar_has_no_domain(project):
    """Orphan scoping must not go silent on a grammar without a domain.

    `is_local_domain()` took the second hyphen-separated field as the
    domain. A dotted ID has no such field, so every unknown ID looked
    foreign and no orphan was ever reported: a silent miss of exactly the
    drift the Gate exists to catch.
    """
    write_config(project)
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")
    project.write(
        "specs/cards/spec.md",
        "# Cards\n\n- AC-5.6.1a — as above.\n- AC-9.9.9 — invented here.\n",
    )
    project.write(
        "specs/cards/tasks.md",
        "# Tasks\n\n- [ ] T001 Replay — **Carries**: AC-5.6.1a\n",
    )

    proc, manifest = project.run()

    details = " ".join(f["detail"] for f in manifest["gate"].get("failures", []))
    assert "AC-9.9.9" in details, (
        "an ID invented in a spec was not reported; orphan scoping went "
        f"silent under a domain-less grammar. stdout:\n{proc.stdout}"
    )


def test_AC_GATE_130_mint_refuses_rather_than_emit_an_id_the_grammar_rejects(project):
    """mint-id.sh must not hand back an ID this project could never carry.

    Its PREFIX-AREA-NN scheme is the stock grammar hardcoded. Against a
    dotted registry it emitted `AC-5-10`, which `id_regex` rejects, so the
    Gate would refuse the very ID the tool had just issued.
    """
    write_config(project)
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")

    proc = subprocess.run(
        ["bash", str(MINT), "AC", "5"],
        cwd=project.root,
        env={
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "SPECASSAY_PROJECT_ROOT": str(project.root),
            "SPECASSAY_CONFIG": str(project._config),
            "HOME": str(project.root),
        },
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert proc.returncode != 0, (
        f"mint emitted {proc.stdout.strip()!r} under a grammar that rejects "
        "it, instead of refusing"
    )
    assert "id_regex" in (proc.stdout + proc.stderr), (
        "the refusal should name the configured grammar it could not fit; "
        f"got:\n{proc.stdout}\n{proc.stderr}"
    )


# --- The empty report: a loud refusal, not a silent demotion -----------


def test_AC_GATE_110_empty_junit_report_is_refused_not_trusted(project):
    """Zero test cases cannot verify anything, and must say so.

    Observed on Swift 6.3.3, where `swift test --xunit-output` wrote only
    the swift-testing file, with zero cases, for an XCTest-only run. Whose
    bug that is belongs to the toolchain question; trusting the file is
    ours. v0.4.13 read it as "nothing passed", demoted every criterion, and
    reported a green run with `executionVerified: true`.
    """
    write_config(project, test_results="report.xml")
    project.prd("- AC-5.6.1a — A reconnect replays the queued cards.")
    project.write(
        "specs/cards/tasks.md",
        "# Tasks\n\n- [ ] T001 Replay — **Carries**: AC-5.6.1a\n",
    )
    project.write(
        "tests/test_cards.py",
        "def test_AC_5_6_1_a_replays_queued_cards():\n    assert True\n",
    )
    project.write(
        "report.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<testsuites><testsuite name="EmptySuite" tests="0" failures="0"/>'
        "</testsuites>\n",
    )

    proc, _ = project.run()

    assert proc.returncode == 2, (
        f"an empty report was trusted; exit={proc.returncode}\n{proc.stdout}"
    )
    assert "no test cases" in proc.stdout.lower() or "no test cases" in proc.stderr.lower(), (
        f"the refusal did not say what was wrong:\n{proc.stdout}\n{proc.stderr}"
    )


# --- New refusal introduced by the fix, so it carries its own proof ----


def test_AC_GATE_120_ids_differing_only_in_punctuation_are_refused(project):
    """Separator-insensitive matching must not guess between two IDs.

    `AC-1-2` and `AC-12` reduce to the same key, so a test named for either
    could be credited to the wrong row. The engine cannot settle that; the
    registry has to, so the Gate says so instead of picking.
    """
    write_config(project, id_regex="AC-[0-9-]+", test_ac_regex="AC_[0-9_]+")
    project.prd(
        "- AC-1-2 — The deck opens on the last card.",
        "- AC-12 — The deck opens on the first card.",
    )
    project.write(
        "specs/deck/tasks.md",
        "# Tasks\n\n"
        "- [ ] T001 Opening card — **Carries**: AC-1-2\n"
        "- [ ] T002 First card — **Carries**: AC-12\n",
    )

    proc, manifest = project.run()

    kinds = [f["kind"] for f in manifest["gate"].get("failures", [])]
    assert "ambiguous-id-key" in kinds, (
        f"two IDs differing only in punctuation were accepted silently; "
        f"failures={kinds}\n{proc.stdout}"
    )
    assert proc.returncode == 1


def test_no_configured_pattern_reaches_awk_through_a_v_assignment():
    """A config value must not travel through `awk -v`, in any script.

    `-v` runs escape processing on its value, so gawk reads the `\\*` in a
    mark like `\\*\\*Retires\\*\\*:` as a plain `*` and mawk does not: the same
    config then parses on one machine and not on another. This one was
    caught by CI rather than by the suite, because the container that wrote
    the fix runs mawk and the runner runs gawk. A behavioural test cannot
    see that difference without both awks present; reading the scripts can,
    anywhere.
    """
    offenders = []
    pattern = re.compile(
        r"""awk\s+(-[A-Za-z]+\s+)*-v\s+\w+=["']?\$\{?"""
        r"""(ID_RE|COVERS_RE|CARRIES_RE|RETIRES_RE|TEST_AC_RE|\d)"""
    )
    for script in sorted(SCRIPTS.glob("*.sh")):
        for lineno, line in enumerate(script.read_text().splitlines(), 1):
            if pattern.search(line):
                offenders.append(f"{script.name}:{lineno}: {line.strip()}")

    assert not offenders, (
        "a configured pattern is passed to awk through -v, which is "
        "escape-processed; pass it through the environment and read it with "
        "ENVIRON[] instead:\n  " + "\n  ".join(offenders)
    )
