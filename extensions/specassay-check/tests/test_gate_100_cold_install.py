"""FR-GATE-100, AC-GATE-100a/b/c: the cold-install on-ramp. Taught by the
first Windows tester on record (senior engineer, Git Bash, no Spec Kit
experience, brownfield repo with existing specs under docs/**, 2026-09-03).
His run ended at "OK (0 registry IDs)" with no idea what was supposed to
happen next, his box had `python` but no `python3`, and he could not tell
whether install had scaffolded the Gate config. Three fixes, three ACs.
"""

import os
import stat
import sys


def _shim(dir_, name, body):
    p = dir_ / name
    p.write_text("#!/usr/bin/env bash\n" + body + "\n")
    p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return p


def _shim_path(tmp_path, python3_body, python_body):
    """A PATH whose first entry answers `python3` and `python` with the
    given shim bodies, ahead of whatever the real machine has."""
    shims = tmp_path / "shims"
    shims.mkdir()
    _shim(shims, "python3", python3_body)
    _shim(shims, "python", python_body)
    return f"{shims}{os.pathsep}{os.environ.get('PATH', '')}"


# --- AC-GATE-100a: empty registry green says what next --------------------


def test_AC_GATE_100a_empty_registry_stays_green_and_names_the_on_ramp(project):
    project.write("PRD.md", "# Fixture PRD\n\nNo IDs minted yet.\n")
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest is not None and manifest["rows"] == []
    assert manifest["gate"]["ok"] is True
    out = proc.stdout
    assert "registry empty (0 IDs in PRD.md)" in out
    assert "Nothing is promised yet" in out
    assert "stays green until a first ID exists" in out
    assert "greenfield" in out and "brownfield" in out
    assert "mint-id.sh AC LOGIN --append" in out
    assert "Expect a refusal" in out
    assert "**Carries**: AC-LOGIN-10" in out
    assert "anointed backlog" in out and "proven" in out and "tracked-debt" in out
    # The bare, teach-nothing line is gone on this path.
    assert "OK (0 registry IDs)" not in out


def test_AC_GATE_100a_populated_registry_keeps_the_plain_ok_line(project):
    project.prd("- AC-FIX-01 — thing.")
    project.write("specs/backlog/spec.md", "AC-FIX-01\n")
    project.write("specs/backlog/tasks.md", "- [x] T1 — **Carries**: AC-FIX-01\n")
    project.write("tests/test_fix.py", "def test_AC_FIX_01_thing(): pass\n")
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert "SpecAssay Check (Gate 2): OK (1 registry IDs)" in proc.stdout
    assert "registry empty" not in proc.stdout


def test_AC_GATE_100a_missing_registry_file_points_at_the_on_ramp(project):
    # Fresh Spec Kit project, nothing minted, no PRD.md at all: still a
    # refusal (the config names a file that isn't there), but one that says
    # what to do about it instead of only what is wrong.
    project.config(registry="PRD.md")
    (project.root / "PRD.md").unlink(missing_ok=True)

    proc, manifest = project.run()

    assert proc.returncode == 1
    assert "registry not found: PRD.md" in proc.stderr
    assert "touch PRD.md" in proc.stderr
    assert "point registry: at the doc that already holds your requirements" in proc.stderr
    assert manifest is not None and manifest["gate"]["ok"] is False


# --- AC-GATE-100b: interpreter detection ---------------------------------


def test_AC_GATE_100b_falls_back_to_python_when_python3_is_unusable(project, tmp_path):
    project.prd("- AC-FIX-01 — thing.")
    project.write("specs/backlog/spec.md", "AC-FIX-01\n")
    project.write("specs/backlog/tasks.md", "- [x] T1 — **Carries**: AC-FIX-01\n")
    project.write("tests/test_fix.py", "def test_AC_FIX_01_thing(): pass\n")
    project.config()
    # python3: present on PATH but unusable (the Microsoft Store stub
    # shape: an executable that only fails). python: a real Python 3.
    path = _shim_path(
        tmp_path,
        python3_body="exit 127",
        python_body=f'exec "{sys.executable}" "$@"',
    )

    proc, manifest = project.run(env={"PATH": path, "SPECASSAY_PYTHON": None})

    assert proc.returncode == 0, proc.stderr
    assert "  python: python (" in proc.stderr
    assert manifest is not None and manifest["gate"]["ok"] is True


def test_AC_GATE_100b_no_usable_python_fails_with_one_line_install_hint(project, tmp_path):
    project.prd("- AC-FIX-01 — thing.")
    project.config()
    path = _shim_path(
        tmp_path,
        python3_body="exit 127",
        python_body='echo "Python 2.7.18"; exit 1',
    )

    proc, manifest = project.run(env={"PATH": path, "SPECASSAY_PYTHON": None})

    assert proc.returncode == 2
    assert manifest is None, "no interpreter means no scanning and no manifest"
    assert "FAIL: no usable Python 3 found (tried python3 and python; need 3.8 or newer)." in proc.stderr
    assert "https://www.python.org/downloads/" in proc.stderr
    assert "SPECASSAY_PYTHON=" in proc.stderr


def test_AC_GATE_100b_explicit_override_wins(project, tmp_path):
    project.prd("- AC-FIX-01 — thing.")
    project.write("specs/backlog/spec.md", "AC-FIX-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: AC-FIX-01\n")
    project.config()
    path = _shim_path(tmp_path, python3_body="exit 127", python_body="exit 127")

    proc, manifest = project.run(env={"PATH": path, "SPECASSAY_PYTHON": sys.executable})

    assert proc.returncode == 0, proc.stderr
    assert f"  python: {sys.executable} (" in proc.stderr


# --- AC-GATE-100c: config state reported at startup ----------------------


def test_AC_GATE_100c_config_found_is_reported_with_its_path(project):
    project.prd("- AC-FIX-01 — thing.")
    project.write("specs/backlog/spec.md", "AC-FIX-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: AC-FIX-01\n")
    config = project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert "SpecAssay Check (Gate 2) starting" in proc.stderr
    # Shown relative to the project root, the way a user would type it.
    assert f"  config: {config.relative_to(project.root)} (from SPECASSAY_CONFIG)" in proc.stderr


def test_AC_GATE_100c_config_missing_names_the_file_and_the_copy_command(project):
    project.prd("- AC-FIX-01 — thing.")
    project.write("specs/backlog/spec.md", "AC-FIX-01\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: AC-FIX-01\n")
    project.config()
    missing = project.root / "nowhere" / "specassay-check-config.yml"

    proc, manifest = project.run(env={"SPECASSAY_CONFIG": str(missing)})

    # Falls back to the extension's own config-template.yml (its registry
    # is PRD.md, same as the fixture), so the run still completes...
    assert proc.returncode == 0, proc.stderr
    # ...but says so, names the missing file, and gives the one command
    # that makes the message go away.
    assert f"  config: MISSING at {missing.relative_to(project.root)} (looked via SPECASSAY_CONFIG)" in proc.stderr
    assert "running on config-template.yml defaults for now" in proc.stderr
    assert "scaffold it once: cp " in proc.stderr
    assert "config-template.yml" in proc.stderr and "specassay-check-config.yml" in proc.stderr
