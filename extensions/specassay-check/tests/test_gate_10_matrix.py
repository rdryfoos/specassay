"""FR-GATE-10, AC-GATE-10a/b/c: --matrix re-presents the same run's
already-computed status data as coverage.md + coverage.svg -- a
portfolio-snapshot renderer, never a second scan, never a second viewer
(see PRD.md's boundary line, written before this was built). Family color
tokens and canonical ordering per INTERFACE-CANON.md Sec.2; self-dated
with the manifest's own generatedAt; retired IDs absent the same way
they're absent from trace-manifest.json's own v4 rows[].
"""

import re


def test_AC_GATE_10a_matrix_writes_from_same_run_no_second_scan(project):
    project.prd(
        "- AC-WIDGET-01 — proven candidate.",
        "- AC-WIDGET-02 — backlog candidate.",
    )
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\nAC-WIDGET-02\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [x] T0 proven carrier — **Carries**: AC-WIDGET-01\n"
        "- [ ] T1 backlog carrier — **Carries**: AC-WIDGET-02\n",
    )
    project.write("src/thing.py", "# @covers AC-WIDGET-01\n")
    project.write("tests/test_thing.py", "def test_AC_WIDGET_01_proven():\n    pass\n")
    project.config()
    proc, manifest = project.run(["--matrix"])
    assert proc.returncode == 0, proc.stderr

    md = (project.root / "coverage.md").read_text()
    svg = (project.root / "coverage.svg").read_text()

    assert "AC-WIDGET-01" in md and "proven" in md
    assert "AC-WIDGET-02" in md and "backlog" in md
    # Same run's data: the manifest's own registryIdCount matches what
    # coverage.md's Total row reports -- not independently recomputed.
    assert f"| **Total** | **{manifest['totals']['registryIdCount']}** |" in md
    assert svg.startswith("<svg")


def test_AC_GATE_10b_family_colors_canonical_order_and_self_dated(project):
    project.prd("- AC-WIDGET-01 — proven candidate.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write("specs/backlog/tasks.md", "- [x] T1 done — **Carries**: AC-WIDGET-01\n")
    project.write("src/thing.py", "# @covers AC-WIDGET-01\n")
    project.write("tests/test_thing.py", "def test_AC_WIDGET_01_proven():\n    pass\n")
    project.config()
    proc, manifest = project.run(["--matrix"])
    assert proc.returncode == 0, proc.stderr

    svg = (project.root / "coverage.svg").read_text()
    # Canonical family tokens (INTERFACE-CANON.md Sec.2), not invented locally.
    for hexcode in ("#9ed4ff", "#c9903a", "#219653", "#eb5757"):
        assert hexcode in svg
    # Canonical order backlog -> tracked-debt -> proven -> GAP: the legend
    # always lists all four regardless of count (unlike the bar, which
    # only draws a segment for a nonzero count), so check order there.
    order = ["#9ed4ff", "#c9903a", "#219653", "#eb5757"]
    legend_circles = re.findall(r'<circle[^>]*fill="(#[0-9a-f]+)"', svg)
    assert legend_circles == order
    # Self-dating: the manifest's own generatedAt is visible text in the SVG.
    assert manifest["generatedAt"] in svg


def test_AC_GATE_10b_zero_count_status_has_no_bar_sliver(project):
    # Regression: integer-division rounding must never give a zero-count
    # status (GAP here) a visible segment -- caught smoke-testing this
    # against this repo's own registry before shipping. Needs a total that
    # does NOT divide the 744px bar evenly (5 rows here) for the rounding
    # remainder to actually appear; a single-row fixture divides exactly
    # and never exercises the bug at all.
    project.prd(
        "- AC-WIDGET-01 — proven.",
        "- AC-WIDGET-02 — backlog.",
        "- AC-WIDGET-03 — backlog.",
        "- AC-WIDGET-04 — tracked-debt.",
        "- AC-WIDGET-05 — tracked-debt.",
    )
    # 02/03 stay OUT of spec.md -- "started" (spec presence or @covers) is
    # what separates tracked-debt from anointed backlog; they're exempted
    # from exact-set via Carries alone, same as any anointed-backlog ID.
    project.write("specs/backlog/spec.md", "AC-WIDGET-01 AC-WIDGET-04 AC-WIDGET-05\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [x] T1 proven carrier — **Carries**: AC-WIDGET-01\n"
        "- [ ] T2 backlog carrier — **Carries**: AC-WIDGET-02, AC-WIDGET-03\n"
        "- [ ] T3 debt carrier — **Carries**: AC-WIDGET-04, AC-WIDGET-05\n",
    )
    project.write(
        "src/thing.py",
        "# @covers AC-WIDGET-01\n# @covers AC-WIDGET-04\n# @covers AC-WIDGET-05\n",
    )
    project.write("tests/test_thing.py", "def test_AC_WIDGET_01_proven():\n    pass\n")
    project.config()
    proc, manifest = project.run(["--matrix"])
    assert proc.returncode == 0, proc.stderr
    assert manifest["statusCounts"] == {
        "proven": 1, "tracked-debt": 2, "GAP": 0, "backlog": 2,
    }

    svg = (project.root / "coverage.svg").read_text()
    assert 'fill="#eb5757"' not in re.sub(r"<circle[^>]*fill=\"#eb5757\"[^>]*/>", "", svg)


def test_AC_GATE_10c_retired_ids_absent_from_matrix_like_v4_rows(project):
    project.prd("- AC-WIDGET-01 — Retirement candidate.")
    project.write("specs/backlog/spec.md", "AC-WIDGET-01\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T1 retirement carrier — **Retires**: AC-WIDGET-01 (2026-08-22): trial concluded.\n",
    )
    project.config()
    proc, manifest = project.run(["--matrix"])
    assert proc.returncode == 0, proc.stderr
    assert manifest["retired"] == [
        {"id": "AC-WIDGET-01", "date": "2026-08-22", "reason": "trial concluded."}
    ]

    md = (project.root / "coverage.md").read_text()
    assert "AC-WIDGET-01" not in md
