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
    assert "🟢 **Ready to review**" in line
    assert "**2** now have a test" in line
    assert "**1** now has a declared debt" in line
    assert "**1** changed file no requirement claims" in line
    # The whole verdict is one line, not a section to scroll.
    assert "\n" not in line


def test_a_broken_thread_says_so_in_the_same_place(tmp_path):
    base = [row("AC-SYNC-10", "tracked-debt")]
    head = [row("AC-SYNC-10", "GAP")]
    out, _ = report(tmp_path, base, head, gate_ok=False)

    line = verdict_line(out)
    assert "🔴 **Do not merge yet**" in line
    assert "**1** has neither" in line


def test_a_carrier_added_with_the_status_held_is_not_no_rows_moved(tmp_path):
    base = [row("AC-SYNC-10", "tracked-debt", impls=("src/sync.py",))]
    head = [row("AC-SYNC-10", "tracked-debt",
                impls=("src/sync.py", "src/reconcile.py"))]
    out, _ = report(tmp_path, base, head, ["src/reconcile.py"])

    line = verdict_line(out)
    assert "no requirements changed" not in line, (
        f"a requirement changed and the verdict denied it:\n{line}"
    )
    assert "**1** gained code or a test, state unchanged" in line


def test_nothing_moving_says_nothing_moved_rather_than_going_silent(tmp_path):
    rows = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, rows, rows)

    line = verdict_line(out)
    assert "**no requirements changed**" in line
    assert "**every changed file is claimed**" in line


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
    assert "+3 requirements in this area did not change, not listed:" in out
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
    assert "🆕 new" in line
    assert "PRD.md" in line, "a mint's move lives in the registry; the row should point there"
    assert "**1** new requirement" in verdict_line(out)


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

    assert "<summary><b>Changed files no requirement claims</b> — 2 files</summary>" in out
    assert "docs/notes.md" in out and "Makefile" in out


# --- what must not fold ----------------------------------------------------


def test_AC_THREAD_10_intent_changed_is_never_folded(tmp_path):
    base = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — within 5s of reconnect.",
                proofs=("tests/test_sync.py",))]
    head = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — within 2s of reconnect.",
                proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head)

    assert "### Reworded requirements" in out
    heading = out.index("### Reworded requirements")
    before = out[:heading]
    assert before.count("<details>") == before.count("</details>"), (
        "Reworded requirements sits inside a fold; it asks the reader to do something, "
        "so it must be visible without a click")
    assert "**1** reworded" in verdict_line(out)


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

    assert "<summary><b>The run behind this report</b></summary>" in out
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


# --- plain words, and a verdict that says the next action ------------------
#
# FR-THREAD-20, ruled 2026-10-02. The first line a stranger reads says what to do
# next, in three states and no more, and the house words live in the footer with
# their definitions beside them.

HOUSE_WORDS = (
    "Golden Thread", "gilt", "hallmark", "named proof", "Loupe",
    "mint", "minted", "anoint", "intact", "off thread", "Intent Changed",
    "promise", "promises",
)


def test_AC_THREAD_20a_a_clean_pass_reads_ready_to_review(tmp_path):
    """@covers AC-THREAD-20a"""
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py"])

    line = verdict_line(out)
    assert "🟢 **Ready to review**" in line, line
    assert "Needs a person" not in out
    assert "Do not merge yet" not in out


def test_AC_THREAD_20a_a_reworded_requirement_needs_a_person(tmp_path):
    """@covers AC-THREAD-20a

    Amber with the gate green: the wording moved under code written against the
    old text, and nobody but a person can say whether it still holds.
    """
    base = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — Retries after 5s.",
                proofs=("tests/test_sync.py",))]
    head = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — Retries after 2s.",
                proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["PRD.md"])

    line = verdict_line(out)
    assert "🟡 **Needs a person**" in line, line
    assert "Ready to review" not in out


def test_AC_THREAD_20a_a_required_tick_needs_a_person(tmp_path):
    """@covers AC-THREAD-20a

    A required tick is unticked the moment the report renders, so a green line
    here would have been true about the gate and misleading about the merge.
    """
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "Makefile"],
                    offthread_ack="required")

    assert "🟡 **Needs a person**" in verdict_line(out)

    # And `record`, which asks for nothing, leaves the verdict green.
    out2, _ = report(tmp_path, base, head, ["tests/test_sync.py", "Makefile"],
                     offthread_ack="record")
    assert "🟢 **Ready to review**" in verdict_line(out2)


def test_AC_THREAD_20a_a_refusing_gate_says_do_not_merge_yet(tmp_path):
    """@covers AC-THREAD-20a

    Red outranks amber: a reworded requirement on a broken gate still reads
    "do not merge yet", because that is the action either way.
    """
    base = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — Retries after 5s.",
                proofs=("tests/test_sync.py",))]
    head = [row("AC-SYNC-10", "GAP", statement="AC-SYNC-10 — Retries after 2s.")]
    out, _ = report(tmp_path, base, head, ["PRD.md"], gate_ok=False,
                    intent_ack="required")

    line = verdict_line(out)
    assert "🔴 **Do not merge yet**" in line, line
    assert "Needs a person" not in out


def test_AC_THREAD_20b_no_house_word_appears_above_the_footer(tmp_path):
    """@covers AC-THREAD-20b

    The whole report, in its loudest state: every section rendered, both ticks
    required, a receipt attached. Nothing above the footer may teach a word.

    The fixture statements are deliberately free of house words, because the
    report quotes a requirement's own wording verbatim in the reworded section. A
    project that writes "promise" into its registry will see it here, and should:
    those are its words, not the comment's.
    """
    (tmp_path / "run.md").write_text("gate: verdict GREEN, exit 0\n")
    base = [row("AC-SYNC-10", "backlog"),
            row("AC-SYNC-20", "proven", statement="AC-SYNC-20 — Retries after 5s.",
                proofs=("tests/test_retry.py",)),
            row("AC-SYNC-30", "proven", proofs=("tests/test_keep.py",))]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",)),
            row("AC-SYNC-20", "proven", statement="AC-SYNC-20 — Retries after 2s.",
                proofs=("tests/test_retry.py",)),
            row("AC-SYNC-30", "proven", proofs=("tests/test_keep.py",)),
            row("AC-NEW-10", "backlog")]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "PRD.md", "Makefile"],
                    offthread_ack="required", intent_ack="required",
                    receipts=str(tmp_path / "run.md"))

    body, footer = out.rsplit("\n---\n", 1)
    for word in HOUSE_WORDS:
        assert word not in body, (
            f"the house word {word!r} is above the footer:\n"
            + "\n".join(ln for ln in body.splitlines() if word in ln)
        )


def test_AC_THREAD_20b_the_footer_defines_the_three_words_it_uses(tmp_path):
    """@covers AC-THREAD-20b"""
    out, _ = report(tmp_path, [row("AC-SYNC-10", "proven", proofs=("tests/t.py",))],
                    [row("AC-SYNC-10", "proven", proofs=("tests/t.py",))])
    footer = out.rsplit("\n---\n", 1)[1]

    assert "<b>Words used here:</b>" in footer
    for word, definition in (
        ("Golden Thread", "the chain from a requirement to the code and test"),
        ("Off thread", "a changed file no requirement claims"),
        ("Mint", "to write a new requirement into the registry"),
    ):
        assert f"<b>{word}</b>, {definition}" in footer, word
    # One line, so it reads as a footnote rather than a glossary.
    assert len([ln for ln in footer.splitlines() if ln.strip()]) == 1


def test_AC_THREAD_20c_every_count_of_one_agrees_in_number(tmp_path):
    """@covers AC-THREAD-20c

    The bug this clause was minted for: the verdict line printed `1 files off
    thread` while the fold summary under it said `1 changed file` correctly, which
    is two readers of one count disagreeing inside one comment.
    """
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",)),
            row("AC-NEW-10", "backlog")]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "stray.py"])

    line = verdict_line(out)
    assert "**1** changed file no requirement claims" in line, line
    assert "1 files" not in out
    assert "**1** now has a test" in line
    assert "**1** new requirement" in line
    assert "— 1 file</summary>" in out
    assert "— 2 requirements in 2 areas" in out


def test_AC_THREAD_20d_a_required_tick_keeps_the_shape_the_workflows_match(tmp_path):
    """@covers AC-THREAD-20d

    Three workflows find the tick lines with
    `/^- \\[[ x]\\] .*required`\\)_\\s*$/gm`. The words inside changed with this
    pass; the shape around them cannot, or a required tick stops holding a merge
    and nothing says so.
    """
    import re as _re
    pattern = _re.compile(r"^- \[[ x]\] .*required`\)_\s*$", _re.M)

    base = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — Retries after 5s.",
                proofs=("tests/test_sync.py",))]
    head = [row("AC-SYNC-10", "proven", statement="AC-SYNC-10 — Retries after 2s.",
                proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["PRD.md", "Makefile"],
                    offthread_ack="required", intent_ack="required")

    found = pattern.findall(out)
    assert len(found) == 2, f"the workflows would find {len(found)} tick(s), not 2:\n{out}"
    assert all(ln.startswith("- [ ] ") for ln in found)
    assert any("offthread_ack: required" in ln for ln in found)
    assert any("intent_ack: required" in ln for ln in found)

    # `record` renders a tick the workflows must NOT find: it asks for nothing.
    out2, _ = report(tmp_path, base, head, ["PRD.md", "Makefile"],
                     offthread_ack="record", intent_ack="record")
    assert pattern.findall(out2) == []
    assert out2.count("- [ ] ") == 2
