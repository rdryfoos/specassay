"""FR-COLD-20: a registry to start from, and the grammar beside it.

Gap (b) and (c) of the cold path. Reproduced 2026-10-02 on 0.5.4: the install left
87 files under `.specify/` and `.claude/` and nothing at the project root, the
composed spec template forbade minting where the user was standing, and
`mint-id.sh` refused with `registry not found`, so the one shipped command that
mints could not create the file it mints into. Every row it had ever written also
came out with no authorship, which nothing in the documented command hinted at.
"""

import re
import subprocess
from pathlib import Path

EXT = Path(__file__).resolve().parents[1]
MINT = EXT / "scripts" / "mint-id.sh"
SEED = EXT / "templates" / "registry-seed.md"

AUTHORSHIP_VALUES = ("case", "design", "retrospective", "constitution")


def _mint(project, *args):
    return subprocess.run(
        ["bash", str(MINT), *args],
        cwd=project.root,
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "SPECASSAY_PROJECT_ROOT": str(project.root),
            "SPECASSAY_CONFIG": str(project._config),
        },
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_AC_COLD_20a_init_writes_the_seed_and_refuses_to_overwrite(project):
    """@covers AC-COLD-20a"""
    project.config()
    registry = project.root / "PRD.md"
    assert not registry.exists()

    # Before --init existed, a mint here said only "registry not found". It now
    # names the command that fixes it.
    refusal = _mint(project, "AC", "GREET")
    assert refusal.returncode != 0
    assert "--init" in refusal.stderr, refusal.stderr

    proc = _mint(project, "--init")
    assert proc.returncode == 0, proc.stderr
    assert registry.exists()
    assert registry.read_text() == SEED.read_text()
    assert "PRD.md" in proc.stderr

    before = registry.read_text()
    again = _mint(project, "--init")
    assert again.returncode != 0
    assert "already exists" in again.stderr
    assert "PRD.md" in again.stderr
    assert registry.read_text() == before, "--init overwrote an existing registry"


def test_AC_COLD_20b_authorship_rides_on_the_minted_line(project):
    """@covers AC-COLD-20b

    Both halves of the promise: the mark is written in the shape the Gate reads,
    and the Gate then records that authorship on the row. Asserting the text alone
    would pass on a mark the Gate's own parser rejects.
    """
    project.prd()
    project.config()
    proc = _mint(
        project, "AC", "GREET", "--authorship", "case",
        "--append", "Given a name, when the greeter runs, then it returns a greeting.",
    )
    assert proc.returncode == 0, proc.stderr
    line = [
        ln for ln in (project.root / "PRD.md").read_text().splitlines()
        if "AC-GREET-10" in ln
    ][0]
    assert line.endswith("**Authorship**: case"), line

    project.write("specs/greet/spec.md", "# Spec\n\n- AC-GREET-10 — the greeting.\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T001 Greet — **Carries**: AC-GREET-10\n",
    )
    proc, _ = project.run()
    v5 = project.root / "trace-manifest.v5beta.json"
    import json
    rows = {r["id"]: r for r in json.loads(v5.read_text())["rows"]}
    assert rows["AC-GREET-10"].get("authorship") == "case", (
        "the Gate did not read the mark the mint wrote"
    )
    assert "authorship unassigned" not in proc.stdout + proc.stderr


def test_AC_COLD_20b_a_fifth_authorship_value_is_refused(project):
    """@covers AC-COLD-20b"""
    project.prd()
    project.config()
    proc = _mint(project, "AC", "GREET", "--authorship", "vibes", "--append", "A thing.")
    assert proc.returncode != 0
    for value in AUTHORSHIP_VALUES:
        assert value in proc.stderr, f"the refusal does not name {value}"
    assert "AC-GREET-10" not in (project.root / "PRD.md").read_text(), (
        "a refused mint still wrote a row"
    )


def test_AC_COLD_20c_the_line_to_paste_is_printed_and_the_id_stands_alone(project):
    """@covers AC-COLD-20c"""
    project.prd()
    project.config()
    proc = _mint(project, "AC", "GREET", "--authorship", "design")
    assert proc.returncode == 0, proc.stderr

    # stdout is what a caller captures: the ID, and nothing else.
    assert proc.stdout.strip() == "AC-GREET-10", repr(proc.stdout)

    # The line to paste is printed beside it, whole, so nobody composes one.
    assert re.search(
        r"- AC-GREET-10 .*\*\*Authorship\*\*: design", proc.stderr
    ), proc.stderr
    assert "AC-GREET-10" not in (project.root / "PRD.md").read_text(), (
        "a mint without --append wrote to the registry"
    )


def test_AC_COLD_20d_the_seed_states_the_grammar_and_gates_green(project):
    """@covers AC-COLD-20d"""
    seed = SEED.read_text()

    # The grammar, in the detail the Gate actually enforces.
    assert "<TYPE>-<DOMAIN>-<NUMBER>" in seed
    for piece in ("2 to 6 characters", "two or more digits", "sibling"):
        assert piece in seed, f"the seed does not state: {piece}"
    for type_ in ("US", "FR", "NFR", "AC"):
        assert re.search(rf"^- {type_}-GREET-10 ", seed, re.M), (
            f"the seed carries no example {type_} row"
        )
    for value in AUTHORSHIP_VALUES:
        assert value in seed, f"the seed does not say what {value} means"

    # Every example row sits inside a fence, so an untouched seed promises nothing.
    project.write("PRD.md", seed)
    project.config()
    proc, manifest = project.run()
    assert manifest["rows"] == [], (
        f"the seed minted rows: {[r['id'] for r in manifest['rows']]}"
    )
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]
    assert "registry empty" in proc.stdout
