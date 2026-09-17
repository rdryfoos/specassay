"""The Thread Report's display contract.

The report's job is to be read, and the first real one rendered on a live
estate was longer than a reviewer would read: every moved row appeared twice
(once as a bullet, once as a table row marked changed), the family tables
listed rows that had not moved beside the ones that had, and the gate log that
produced the report sat open at the bottom.

These tests hold the shape the trims settled on: a verdict line a reader can
take in whole, the moves in one place and not two, unchanged rows footnoted
rather than listed, and everything else one click down. They are display tests
on purpose — none of them asserts a status, and every fact the old report
carried is still reachable in the new one. Collapsed is not dropped, so most
of what follows checks that something folded is still *there*.

Six of them carry `AC_THREAD_10` in their names and are that criterion's real
proof, one per clause of it: the verdict line, said-once, unchanged-footnoted,
and the three things about folding — what folds, and the two that never do.
The rest are the same contract read from other angles, and prove nothing on
their own; they exist so a break names itself precisely.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "thread-report.py"


def row(id_, status, line=10, statement=None, proofs=(), impls=()):
    return {
        "id": id_,
        "status": status,
        "statement": statement or f"{id_} — a promise.",
        "registry": {"path": "PRD.md", "line": line},
        "proofs": [{"name": f"test_{id_}", "path": p, "line": 1} for p in proofs],
        "implementations": [{"path": p, "line": 1} for p in impls],
    }


def report(tmp_path, base_rows, head_rows, changed=(), gate_ok=True, **flags):
    """Render through the real CLI, the way CI calls it."""
    (tmp_path / "base.json").write_text(
        json.dumps({"rows": list(base_rows), "gate": {"ok": True}}))
    (tmp_path / "head.json").write_text(
        json.dumps({"rows": list(head_rows), "gate": {"ok": gate_ok}}))
    (tmp_path / "changed.txt").write_text("\n".join(changed) + ("\n" if changed else ""))
    cmd = [sys.executable, str(SCRIPT),
           "--base", str(tmp_path / "base.json"),
           "--head", str(tmp_path / "head.json"),
           "--changed-files", str(tmp_path / "changed.txt")]
    for key, value in flags.items():
        cmd += ["--" + key.replace("_", "-"), str(value)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, f"the report refused, which it must never do:\n{proc.stderr}"
    return proc.stdout, proc


def verdict_line(text: str) -> str:
    """The one line a reader is meant to take in whole."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return lines[1]


# --- the five-second read -------------------------------------------------


def test_AC_THREAD_10_verdict_line_carries_the_counts_a_reader_came_for(tmp_path):
    base = [row("AC-SYNC-10", "backlog"), row("AC-SYNC-20", "backlog"),
            row("US-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",)),
            row("AC-SYNC-20", "proven", proofs=("tests/test_sync.py",)),
            row("US-SYNC-10", "tracked-debt")]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "docs/notes.md"])

    line = verdict_line(out)
    assert "Golden Thread intact" in line
    assert "**2** proved" in line
    assert "**1** to admitted debt" in line
    assert "**1** files off thread" in line
    # The whole verdict is one line, not a section to scroll.
    assert "\n" not in line


def test_a_broken_thread_says_so_in_the_same_place(tmp_path):
    base = [row("AC-SYNC-10", "tracked-debt")]
    head = [row("AC-SYNC-10", "GAP")]
    out, _ = report(tmp_path, base, head, gate_ok=False)

    line = verdict_line(out)
    assert "🔴 **Golden Thread broken**" in line
    assert "**1** now GAP" in line


def test_a_carrier_added_with_the_status_held_is_not_no_rows_moved(tmp_path):
    base = [row("AC-SYNC-10", "tracked-debt", impls=("src/sync.py",))]
    head = [row("AC-SYNC-10", "tracked-debt",
                impls=("src/sync.py", "src/reconcile.py"))]
    out, _ = report(tmp_path, base, head, ["src/reconcile.py"])

    line = verdict_line(out)
    assert "no rows moved" not in line, f"a row moved and the verdict denied it:\n{line}"
    assert "**1** carrier added, status held" in line


def test_nothing_moving_says_nothing_moved_rather_than_going_silent(tmp_path):
    rows = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, rows, rows)

    line = verdict_line(out)
    assert "**no rows moved**" in line
    assert "**nothing** off thread" in line


# --- said once, not twice -------------------------------------------------


def test_AC_THREAD_10_a_moved_row_is_reported_once_not_twice(tmp_path):
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py"])

    # The ID appears in the table row and in nothing else that states the move.
    move_statements = [ln for ln in out.splitlines()
                       if "AC-SYNC-10" in ln and "proven" in ln]
    assert len(move_statements) == 1, (
        "the same move is stated more than once:\n" + "\n".join(move_statements))
    assert move_statements[0].startswith("|"), "the surviving statement should be the table row"
    assert "◀ changed" not in out, (
        "the 'changed' marker belonged to a table that also held unmoved rows; "
        "every row in this table moved, so the marker says nothing")


def test_the_table_carries_what_the_bullet_list_used_to_say(tmp_path):
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",),
                impls=("src/sync.py",))]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "src/sync.py"])

    line = next(ln for ln in out.splitlines() if ln.startswith("| `AC-SYNC-10`"))
    assert "`backlog`" in line and "`proven`" in line, "the transition is gone"
    assert "test_sync.py" in line and "sync.py" in line, "the changed carriers are gone"


# --- moved shown, unchanged footnoted -------------------------------------


def test_AC_THREAD_10_unchanged_rows_are_footnoted_with_their_states_not_listed(tmp_path):
    base = [row("AC-SYNC-10", "backlog")] + [
        row(f"AC-SYNC-{n}", "proven", proofs=("tests/test_sync.py",)) for n in (20, 30)
    ] + [row("AC-SYNC-40", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))] + base[1:]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py"])

    assert "| `AC-SYNC-10`" in out
    for unmoved in ("AC-SYNC-20", "AC-SYNC-30", "AC-SYNC-40"):
        assert f"| `{unmoved}`" not in out, f"{unmoved} did not move and is listed anyway"
    assert "+3 unchanged rows in this family, not listed:" in out
    # The state is footnoted, not merely counted away.
    assert "2 🟢 proven" in out and "1 🔵 backlog" in out


def test_a_family_with_nothing_unchanged_carries_no_footnote(tmp_path):
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py"])
    assert "unchanged" not in out


# --- collapsed is not dropped ---------------------------------------------


def test_a_retired_row_survives_the_collapse(tmp_path):
    base = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",)),
            row("AC-SYNC-20", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head)

    assert "AC-SYNC-20" in out, "a retired row vanished when the bullet list went"
    assert "retired" in out
    assert "**1** retired" in verdict_line(out)


def test_a_minted_row_survives_and_points_at_the_registry(tmp_path):
    base = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    head = base + [row("AC-SYNC-20", "backlog", line=42)]
    out, _ = report(tmp_path, base, head, ["PRD.md"],
                    pr_url="https://github.com/o/r/pull/7", head_sha="abc123")

    line = next(ln for ln in out.splitlines() if "AC-SYNC-20" in ln and ln.startswith("|"))
    assert "🆕 minted" in line
    assert "PRD.md" in line, "a mint's move lives in the registry; the row should point there"
    assert "**1** minted" in verdict_line(out)


def test_a_row_that_moved_with_no_carrier_to_point_at_renders_absence_as_absence(tmp_path):
    # A backlog row gaining an open **Carries** line moves to tracked-debt, and
    # the task file that moved it carries no mark of its own. The em-dash law:
    # absence renders as absence, never as an invented link.
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "tracked-debt")]
    out, _ = report(tmp_path, base, head)

    line = next(ln for ln in out.splitlines() if ln.startswith("| `AC-SYNC-10`"))
    assert line.rstrip().endswith("| — |"), f"expected an em dash for the absent link:\n{line}"


def test_the_off_thread_files_are_still_named_under_the_fold(tmp_path):
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["docs/notes.md", "Makefile"])

    assert "<summary><b>Off thread</b> — 2 changed files sit off the thread</summary>" in out
    assert "docs/notes.md" in out and "Makefile" in out


# --- what must not fold ----------------------------------------------------


def test_AC_THREAD_10_intent_changed_is_never_folded(tmp_path):
    base = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — within 5s of reconnect.",
                proofs=("tests/test_sync.py",))]
    head = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — within 2s of reconnect.",
                proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head)

    assert "### Intent Changed" in out
    heading = out.index("### Intent Changed")
    before = out[:heading]
    assert before.count("<details>") == before.count("</details>"), (
        "Intent Changed sits inside a fold; it asks the reader to do something, "
        "so it must be visible without a click")
    assert "**1** restated" in verdict_line(out)


def test_AC_THREAD_10_a_required_human_tick_stays_outside_the_fold(tmp_path):
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["docs/notes.md"], offthread_ack="required")

    tick = next(ln for ln in out.splitlines() if ln.startswith("- [ ]"))
    before = out[:out.index(tick)]
    assert before.count("<details>") == before.count("</details>"), (
        "a required tick is hidden inside a fold; it holds a merge, so nobody "
        "can be asked to find it first")


# --- receipts --------------------------------------------------------------


def test_AC_THREAD_10_receipts_render_folded_and_verbatim(tmp_path):
    (tmp_path / "run.md").write_text("```\ngate: verdict GREEN, exit 0\n```\n")
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, receipts=str(tmp_path / "run.md"))

    assert "<summary><b>Receipts</b> — the run behind this report</summary>" in out
    assert "gate: verdict GREEN, exit 0" in out
    # Folded: the receipt sits inside a details, not in the lead.
    lead = out[:out.index("gate: verdict GREEN")]
    assert lead.count("<details>") == lead.count("</details>") + 1


def test_a_missing_receipts_file_loses_the_appendix_not_the_report(tmp_path):
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, proc = report(tmp_path, base, head, receipts=str(tmp_path / "nope.md"))

    assert "## 🧵 Thread Report" in out
    assert "Receipts" not in out
    assert "warning" in proc.stderr.lower()


def test_no_receipts_flag_renders_no_receipts_section(tmp_path):
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head)
    assert "Receipts" not in out


# --- the folds themselves --------------------------------------------------


def test_every_fold_is_balanced_and_renders_its_markdown(tmp_path):
    base = [row("AC-SYNC-10", "backlog"), row("AC-SYNC-20", "proven",
                                              proofs=("tests/test_sync.py",))]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",)), base[1]]
    (tmp_path / "run.md").write_text("gate: green\n")
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "docs/notes.md"],
                    receipts=str(tmp_path / "run.md"))

    lines = out.splitlines()
    assert out.count("<details>") == out.count("</details>") == 3
    for i, ln in enumerate(lines):
        if ln.startswith("<summary>"):
            assert lines[i - 1] == "<details>"
            assert lines[i + 1] == "", (
                "GitHub renders Markdown inside <details> only after a blank line; "
                f"line {i + 2} is {lines[i + 1]!r}")
