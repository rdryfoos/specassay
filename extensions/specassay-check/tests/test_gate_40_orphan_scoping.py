"""FR-GATE-40: orphan-covers/orphan-test distinguish use from mention.
Regression coverage for the domain-scoping + code-span/fence stripping
fix (2026-08-18) -- these four cases are exactly the ones the docs-room
founding pass hit for real and hand-verified before this suite existed.
"""

from pathlib import Path

REAL_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-traceability.sh"


def test_foreign_domain_citation_does_not_orphan(project):
    # A doc quoting another project's real @covers line (a domain this
    # registry never minted into) is a citation, not local drift.
    project.prd("- FR-FIX-01 — Something real, local domain only.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.write(
        "docs/example.md",
        "The other project's file carries `@covers FR-HOME-04, AC-HOME-15`.\n",
    )
    project.config(src_globs=["docs/**"])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "orphan-covers" not in kinds


def test_AC_GATE_40_same_domain_quote_in_inline_span_does_not_orphan(project):
    # The harder case domain-scoping alone can't solve: a project's own
    # real, local ID quoted as a teaching example.
    project.prd("- FR-WIDGET-99 — Something real.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-WIDGET-99 (anointed backlog)\n",
    )
    project.write(
        "docs/quickstart.md",
        "Your source should carry a mark like `@covers FR-WIDGET-99`.\n",
    )
    project.config(src_globs=["docs/**"])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "FR-WIDGET-99")
    assert row["status"] == "backlog"
    assert row["implementations"] == []


def test_same_domain_quote_in_fenced_block_does_not_orphan(project):
    project.prd("- FR-WIDGET-99 — Something real.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-WIDGET-99 (anointed backlog)\n",
    )
    project.write(
        "docs/quickstart.md",
        "Example:\n\n```python\n# @covers FR-WIDGET-99\ndef thing():\n    pass\n```\n",
    )
    project.config(src_globs=["docs/**"])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "FR-WIDGET-99")
    assert row["status"] == "backlog"
    assert row["implementations"] == []


def test_real_unfenced_mark_in_docs_still_detected(project):
    # The positive control: FR-GATE-40 must not blind the Gate to a real
    # mark just because it lives in a docs file.
    project.prd("- FR-WIDGET-99 — Something real.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-WIDGET-99 (anointed backlog)\n",
    )
    project.write(
        "docs/quickstart.md",
        "Quickstart body.\n\n<!-- @covers FR-WIDGET-99 -->\n",
    )
    project.config(src_globs=["docs/**"])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "FR-WIDGET-99")
    assert row["status"] == "proven"
    assert len(row["implementations"]) == 1


def test_AC_GATE_41_own_source_never_self_matches(project):
    # The literal AC: point src_globs at check-traceability.sh's own real
    # file (not a synthetic copy) and confirm scanning it produces no
    # orphan-covers findings from its own comments or regex definitions.
    project.prd("- FR-FIX-01 — Unrelated local ID, just to have a registry.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.config(src_globs=[str(REAL_SCRIPT)])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "orphan-covers" not in kinds
    assert "orphan-test" not in kinds


def test_real_local_orphan_still_fails(project):
    # Domain-scoping must not swallow a genuine local orphan: a real typo
    # in this project's own domain still has to fail.
    project.prd("- FR-FIX-01 — Something real.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.write(
        "src/thing.py",
        "# @covers FR-FIX-02\ndef thing():\n    return True\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 1
    kinds = {f["kind"] for f in manifest["gate"]["failures"]}
    assert "orphan-covers" in kinds
