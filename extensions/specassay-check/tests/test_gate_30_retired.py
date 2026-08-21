"""FR-GATE-30, AC-GATE-30: retired is a genuine fifth status, derived only
from an explicit, dated, reasoned **Retires** record -- never a settable
status field. Citing incident: HomesFlow's US/FR/AC-CLEW-01 (the Clewseau
cold-agent trial slice, 2026-08-18), hand-improvised with a tombstone
comment before this feature existed -- see docs/backlog.md's "Pattern
candidate" section for the full incident this design is built from.

Version boundary: v4 freezes at exactly four status values and a retired
row leaves v4's rows[] table for a new top-level `retired` list (id, date,
reason) instead; v5beta carries `retired` as a normal fifth row status from
the start.
"""

import json


def test_AC_GATE_30b_retired_id_leaves_v4_rows_and_gains_top_level_entry(project):
    project.write("specs/backlog/spec.md", "# Backlog spec\n\nAC-CLEW-01\n")
    project.prd(
        "- AC-CLEW-01 — Given a home display name string, when normalized, "
        "then whitespace collapses."
    )
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Clewseau retirement carrier — **Carries**: AC-CLEW-01 "
        "**Retires**: AC-CLEW-01 (2026-08-18): cold-agent probe concluded; "
        "tooling archived at tag clew-era-final.\n",
    )
    project.config()
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    ids_in_rows = [r["id"] for r in manifest["rows"]]
    assert "AC-CLEW-01" not in ids_in_rows
    assert "retired" not in manifest["statusCounts"]
    assert set(manifest["statusCounts"]) == {"proven", "tracked-debt", "GAP", "backlog"}

    assert manifest["totals"]["retiredCount"] == 1
    assert manifest["retired"] == [
        {"id": "AC-CLEW-01", "date": "2026-08-18",
         "reason": "cold-agent probe concluded; tooling archived at tag clew-era-final."}
    ]

    assert "Retired: 1 (AC-CLEW-01)" in proc.stdout


def test_AC_GATE_30a_retired_row_is_first_class_in_v5beta(project):
    project.write("specs/backlog/spec.md", "# Backlog spec\n\nAC-CLEW-01\n")
    project.prd("- AC-CLEW-01 — Retirement candidate.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Retirement carrier — **Carries**: AC-CLEW-01 "
        "**Retires**: AC-CLEW-01 (2026-08-18): trial concluded.\n",
    )
    project.config()
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr

    v5 = json.loads((project.root / "trace-manifest.v5beta.json").read_text())
    row = next(r for r in v5["rows"] if r["id"] == "AC-CLEW-01")
    assert row["status"] == "retired"
    assert v5["statusCounts"]["retired"] == 1


def test_retired_ac_is_not_a_silent_gap(project):
    # No test, no pending task naming it as tracked-debt -- would ordinarily
    # be GAP, except it's retired.
    project.write("specs/backlog/spec.md", "# Backlog spec\n\nAC-CLEW-01\n")
    project.prd("- AC-CLEW-01 — Retirement candidate.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Retirement carrier — **Retires**: AC-CLEW-01 "
        "(2026-08-18): trial concluded.\n",
    )
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    kinds = [f["kind"] for f in manifest["gate"]["failures"]]
    assert "silent-gap" not in kinds


def test_retires_alone_satisfies_missing_carries(project):
    # A task whose only marker is Retires (no separate Carries line) should
    # not be flagged missing-carries -- Retires is its own claim.
    project.write("specs/backlog/spec.md", "# Backlog spec\n\nAC-CLEW-01\n")
    project.prd("- AC-CLEW-01 — Retirement candidate.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Retirement carrier — **Retires**: AC-CLEW-01 "
        "(2026-08-18): trial concluded.\n",
    )
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    kinds = [f["kind"] for f in manifest["gate"]["failures"]]
    assert "missing-carries" not in kinds


def test_retired_id_exempt_from_spec_unclaimed_same_as_anointed_backlog(project):
    # pending.txt already exempts any ID named on an open checkbox line from
    # spec-unclaimed, regardless of which marker put it there (Carries,
    # Retires, or plain prose) -- Retires gets the same pre-existing
    # exemption anointed backlog already relies on, no special case needed.
    project.prd("- AC-CLEW-01 — Retirement candidate.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Retirement carrier — **Retires**: AC-CLEW-01 "
        "(2026-08-18): trial concluded.\n",
    )
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr
    kinds = [f["kind"] for f in manifest["gate"]["failures"]]
    assert "spec-unclaimed" not in kinds


def test_AC_GATE_30c_malformed_retires_no_date_refuses_before_scanning(project):
    project.write("specs/backlog/spec.md", "# Backlog spec\n\nAC-CLEW-01\n")
    project.prd("- AC-CLEW-01 — Retirement candidate.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Retirement carrier — **Retires**: AC-CLEW-01, no date given.\n",
    )
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 2, proc.stdout
    assert "malformed **Retires** record" in proc.stderr
    assert manifest is None, "no manifest should be written on a malformed retirement record"


def test_AC_GATE_30c_malformed_retires_no_id_refuses_before_scanning(project):
    project.write("specs/backlog/spec.md", "# Backlog spec\n")
    project.prd("- AC-CLEW-01 — Retirement candidate.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 Retirement carrier — **Retires**: (2026-08-18): no ID named.\n",
    )
    project.config()
    proc, manifest = project.run()
    assert proc.returncode == 2, proc.stdout
    assert "malformed **Retires** record" in proc.stderr
    assert manifest is None
