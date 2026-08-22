"""FR-DIG-10, FR-DIG-20, AC-DIG-10, AC-DIG-20: the no-LLM floor of
`specassay dig`. Per docs/archaeology-mode-build-handoff-v1-2026-08-20.md
Sec.5 (THE ONE HARD LAW): no dug row is ever written into a real registry,
and this command must be trivially provable to never write anything outside
its own dig-report.json -- that's the pinned test below, not an incidental
one.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "dig.py"


def run_dig(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
    )


def snapshot(root: Path) -> dict:
    """path -> sha256 for every file under root, for before/after comparison."""
    out = {}
    for p in root.rglob("*"):
        if p.is_file():
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def make_fixture(root: Path) -> None:
    (root / "src").mkdir(parents=True)
    (root / "tests").mkdir(parents=True)
    (root / "src" / "app.py").write_text(
        "def add(a, b):\n"
        "    return a + b\n"
    )
    (root / "tests" / "test_math.py").write_text(
        "def test_addition_returns_sum():\n"
        "    assert add(2, 2) == 4\n"
        "\n"
        "# example: def test_this_is_only_a_comment(): pass\n"
    )
    (root / "README.md").write_text(
        "# Fixture App\n\n"
        "## Adds two numbers\n\n"
        "A tiny example app.\n"
    )


def test_AC_DIG_10_dry_run_writes_nothing(tmp_path):
    make_fixture(tmp_path)
    before = snapshot(tmp_path)
    proc = run_dig([str(tmp_path), "--dry-run"])
    assert proc.returncode == 0, proc.stderr
    assert "dry run" in proc.stdout
    after = snapshot(tmp_path)
    assert before == after, "dry-run must not change or create any file"
    assert not (tmp_path / "dig-report.json").exists()


def test_AC_DIG_10_real_run_writes_only_dig_report(tmp_path):
    make_fixture(tmp_path)
    before = snapshot(tmp_path)
    proc = run_dig([str(tmp_path)])
    assert proc.returncode == 0, proc.stderr

    report_path = tmp_path / "dig-report.json"
    assert report_path.exists()

    after = snapshot(tmp_path)
    new_files = set(after) - set(before)
    assert new_files == {"dig-report.json"}, f"unexpected new files: {new_files}"
    changed = {p for p in before if before[p] != after.get(p)}
    assert not changed, f"existing files must not change: {changed}"


def test_AC_DIG_10_no_anoint_flag_exists(tmp_path):
    make_fixture(tmp_path)
    proc = run_dig([str(tmp_path), "--anoint"])
    assert proc.returncode != 0
    assert "unrecognized" in proc.stderr.lower() or "usage" in proc.stderr.lower()


def test_epistemic_class_always_inferred(tmp_path):
    make_fixture(tmp_path)
    run_dig([str(tmp_path)])
    report = json.loads((tmp_path / "dig-report.json").read_text())
    assert report["rows"], "fixture should produce at least one row"
    assert all(r["epistemicClass"] == "inferred" for r in report["rows"])


def test_AC_DIG_20_dry_run_prints_counts_by_type_and_source(tmp_path):
    make_fixture(tmp_path)
    proc = run_dig([str(tmp_path), "--dry-run"])
    assert "by type" in proc.stdout
    assert "by source" in proc.stdout


def test_dig_report_schema_shape(tmp_path):
    make_fixture(tmp_path)
    run_dig([str(tmp_path)])
    report = json.loads((tmp_path / "dig-report.json").read_text())
    for key in ("format", "generatorVersion", "sourceRepoPath", "generatedAt", "rows"):
        assert key in report
    assert report["format"] == "dig-report"
    for row in report["rows"]:
        for key in ("type", "statement", "epistemicClass", "confidence", "provenance"):
            assert key in row
        assert "source" in row["provenance"]
        assert "file" in row["provenance"]


def test_test_name_humanization_preserves_acronym_digit_runs(tmp_path):
    # Regression: an embedded acronym+digit run like "ZK9Q" must not get
    # split at the digit-to-uppercase boundary (-> "zk9" + "q") -- caught
    # dogfooding this against specassay's own test suite before shipping,
    # where the real incident used "A11Y". Domain deliberately fictional
    # here (not a real registered ID anywhere) so this fixture's own text
    # can't be misread as a real proof claim by whatever repo's Gate
    # happens to scan this test file -- the exact collision the real "A11Y"
    # version of this fixture caused the first time it was written.
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_widget.py").write_text(
        "def test_AC_ZK9Q_01_keyboard_reachable_and_announced():\n    pass\n"
    )
    proc = run_dig([str(tmp_path), "--dry-run"])
    assert proc.returncode == 0, proc.stderr
    run_dig([str(tmp_path)])
    report = json.loads((tmp_path / "dig-report.json").read_text())
    row = next(r for r in report["rows"] if r["provenance"].get("testName") == "test_AC_ZK9Q_01_keyboard_reachable_and_announced")
    assert "zk9q" in row["statement"]
    assert "zk9" not in row["statement"].replace("zk9q", "")


def test_comment_lines_are_not_mined(tmp_path):
    # Regression: a comment describing an example pattern (e.g. "# Flask:
    # @app.route('/x')") must not itself be mined as a real route/test --
    # this tool's own dig.py source self-matched before this fix.
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        "# Example: @app.route('/should-not-appear')\n"
        "@app.route('/real-path')\n"
        "def handler():\n"
        "    pass\n"
    )
    run_dig([str(tmp_path)])
    report = json.loads((tmp_path / "dig-report.json").read_text())
    paths = [r["statement"] for r in report["rows"] if r["type"] == "FR"]
    assert any("/real-path" in s for s in paths)
    assert not any("/should-not-appear" in s for s in paths)


def test_flask_route_statement_has_no_double_space(tmp_path):
    # Regression: Flask's @app.route(...) captures only a path, no HTTP
    # method group -- the naive f"accepts {method} {path}".strip() left a
    # double space when method was empty ("accepts  /policies/<id>").
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        "@app.route('/policies/<id>')\n"
        "def get_policy(id):\n"
        "    return {}\n"
    )
    run_dig([str(tmp_path)])
    report = json.loads((tmp_path / "dig-report.json").read_text())
    row = next(r for r in report["rows"] if r["type"] == "FR")
    assert "  " not in row["statement"]
    assert row["statement"] == "the system accepts /policies/<id>"


def test_sources_filter_limits_output(tmp_path):
    make_fixture(tmp_path)
    run_dig([str(tmp_path), "--sources", "tests", "--out", str(tmp_path / "tests-only.json")])
    report = json.loads((tmp_path / "tests-only.json").read_text())
    sources = {r["provenance"]["source"] for r in report["rows"]}
    assert sources <= {"test"}
    assert "readme" not in sources
