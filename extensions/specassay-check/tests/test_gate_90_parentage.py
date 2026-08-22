"""FR-GATE-90, AC-GATE-90a/b/c: parent edges DERIVE from the registry
document's own heading/section nesting at emit time -- never authored,
never inferred by a viewer, never guessed from ID-prefix naming. Document
structure yields a tree by construction (single-parent v1). Rollup is
recursive over ALL rows in a subtree at any depth (ratified basis: a
non-leaf's own status joins its parent's rollup alongside its
descendants'). Per docs/hierarchy-parentage-brief-2026-08-20.md and the
two design-room rulings that settled Q1-Q4.
"""

import json


def test_AC_GATE_90a_nested_rows_get_parent_edges(project):
    project.prd(
        "- FR-WIDGET-10 — top-level requirement.",
        "  - AC-WIDGET-10 — nested criterion.",
        "  - AC-WIDGET-20 — another nested criterion.",
    )
    project.write("specs/backlog/spec.md", "FR-WIDGET-10 AC-WIDGET-10 AC-WIDGET-20\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T1 — **Carries**: FR-WIDGET-10, AC-WIDGET-10, AC-WIDGET-20\n",
    )
    project.config(parent_derivation="heading-nesting")
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr

    assert project.row(manifest, "AC-WIDGET-10")["parent"] == "FR-WIDGET-10"
    assert project.row(manifest, "AC-WIDGET-20")["parent"] == "FR-WIDGET-10"
    assert project.row(manifest, "FR-WIDGET-10")["parent"] is None


def test_AC_GATE_90a_absence_means_no_edges(project):
    # Same fixture, no parent_derivation configured at all -- absence
    # renders as absence, never inferred by default.
    project.prd(
        "- FR-WIDGET-10 — top-level requirement.",
        "  - AC-WIDGET-10 — nested criterion.",
    )
    project.write("specs/backlog/spec.md", "FR-WIDGET-10 AC-WIDGET-10\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: FR-WIDGET-10, AC-WIDGET-10\n")
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert project.row(manifest, "AC-WIDGET-10")["parent"] is None


def test_same_depth_siblings_get_no_parent(project):
    # Un-indented bullets at the same level are siblings, not nested --
    # this repo's own DOCS section (AC-DOCS-10 sits at the same indent as
    # its neighboring FRs) is exactly this shape.
    project.prd(
        "- FR-WIDGET-10 — first requirement.",
        "- FR-WIDGET-20 — second requirement, same depth.",
    )
    project.write("specs/backlog/spec.md", "FR-WIDGET-10 FR-WIDGET-20\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: FR-WIDGET-10, FR-WIDGET-20\n")
    project.config(parent_derivation="heading-nesting")
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert project.row(manifest, "FR-WIDGET-20")["parent"] is None


def test_AC_GATE_90b_rollup_includes_all_depths_not_just_direct_children(project):
    # Three-tier tree: US > FR > AC. The US's rollup must include the AC
    # (a grandchild), not just its direct FR child.
    project.prd(
        "- US-WIDGET-10 — the story.",
        "  - FR-WIDGET-10 — the requirement.",
        "    - AC-WIDGET-10 — the criterion, proven.",
    )
    project.write("specs/backlog/spec.md", "US-WIDGET-10 FR-WIDGET-10 AC-WIDGET-10\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [x] T1 — **Carries**: US-WIDGET-10, FR-WIDGET-10, AC-WIDGET-10\n",
    )
    project.write(
        "src/thing.py",
        "# @covers AC-WIDGET-10\n# @covers FR-WIDGET-10\n# @covers US-WIDGET-10\n",
    )
    project.write("tests/test_thing.py", "def test_AC_WIDGET_10_criterion():\n    pass\n")
    project.config(parent_derivation="heading-nesting")
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr

    ac_row = project.row(manifest, "AC-WIDGET-10")
    assert ac_row["parent"] == "FR-WIDGET-10"
    fr_row = project.row(manifest, "FR-WIDGET-10")
    assert fr_row["parent"] == "US-WIDGET-10"

    us_row = project.row(manifest, "US-WIDGET-10")
    # AC-GATE-90b: includes the direct child's own status too, not only
    # descendants' -- FR-WIDGET-10 itself (proven, via @covers/spec
    # presence) counts alongside AC-WIDGET-10 (proven, via named test).
    assert us_row["rollup"]["rows"] == 3
    assert us_row["rollup"]["proven"] == 3

    fr_rollup = fr_row["rollup"]
    assert fr_rollup["rows"] == 2  # FR-WIDGET-10 itself + AC-WIDGET-10


def test_AC_GATE_90c_rollup_carries_total_alongside_per_status(project):
    project.prd(
        "- FR-WIDGET-10 — mixed-status parent.",
        "  - AC-WIDGET-10 — proven.",
        "  - AC-WIDGET-20 — backlog.",
    )
    project.write("specs/backlog/spec.md", "FR-WIDGET-10 AC-WIDGET-10\n")
    project.write(
        "specs/backlog/tasks.md",
        "- [x] T1 — **Carries**: FR-WIDGET-10, AC-WIDGET-10\n"
        "- [ ] T2 — **Carries**: AC-WIDGET-20\n",
    )
    project.write("src/thing.py", "# @covers AC-WIDGET-10\n# @covers FR-WIDGET-10\n")
    project.write("tests/test_thing.py", "def test_AC_WIDGET_10_thing():\n    pass\n")
    project.config(parent_derivation="heading-nesting")
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr

    rollup = project.row(manifest, "FR-WIDGET-10")["rollup"]
    assert rollup["rows"] == 3
    assert rollup["rows"] == sum(
        rollup[k] for k in ("proven", "tracked-debt", "backlog", "GAP", "retired")
    )
    assert rollup["backlog"] == 1


def test_leaf_rows_carry_no_rollup_key(project):
    project.prd(
        "- FR-WIDGET-10 — parent.",
        "  - AC-WIDGET-10 — leaf, no children of its own.",
    )
    project.write("specs/backlog/spec.md", "FR-WIDGET-10 AC-WIDGET-10\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: FR-WIDGET-10, AC-WIDGET-10\n")
    project.config(parent_derivation="heading-nesting")
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert "rollup" not in project.row(manifest, "AC-WIDGET-10")
    assert "rollup" in project.row(manifest, "FR-WIDGET-10")


def test_parent_and_rollup_are_additive_no_format_version_bump(project):
    project.prd("- FR-WIDGET-10 — solo row, no nesting.")
    project.write("specs/backlog/spec.md", "FR-WIDGET-10\n")
    project.write("specs/backlog/tasks.md", "- [ ] T1 — **Carries**: FR-WIDGET-10\n")
    project.config(parent_derivation="heading-nesting")
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert manifest["schemaVersion"] == 4

    v5 = json.loads((project.root / "trace-manifest.v5beta.json").read_text())
    assert v5["schemaVersion"] == 5
    row = next(r for r in v5["rows"] if r["id"] == "FR-WIDGET-10")
    assert "parent" in row
