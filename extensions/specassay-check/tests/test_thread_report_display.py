"""The SpecAssay Report's display contract.

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
    # The script looks for a CODEOWNERS file under the repository root, which
    # defaults to the directory the test happens to run from. Pointed at the
    # scratch directory, no test reads this repository's own file by accident.
    flags.setdefault("repo_root", tmp_path)
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


def test_AC_THREAD_20j_a_row_with_nothing_to_point_at_says_none(tmp_path):
    """@covers AC-THREAD-20j

    A backlog row gaining an open **Carries** line moves to tracked-debt, and
    the task file that moved it carries no mark of its own. Absence renders as
    absence, never as an invented link. The cell held an em dash until
    2026-11-28; it now holds a word, and the cell is not left empty either,
    because an empty cell reads as a table that failed to fill.
    """
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "tracked-debt")]
    out, _ = report(tmp_path, base, head)

    line = next(ln for ln in out.splitlines() if ln.startswith("| `AC-SYNC-10`"))
    assert line.rstrip().endswith("| none |"), f"expected the word none for the absent link:\n{line}"

    # The control: a row that does have a file to point at names the file.
    head2 = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out2, _ = report(tmp_path, base, head2, ["tests/test_sync.py"])
    line2 = next(ln for ln in out2.splitlines() if ln.startswith("| `AC-SYNC-10`"))
    assert "test_sync.py" in line2 and "| none |" not in line2, line2


def test_the_off_thread_files_are_still_named_under_the_fold(tmp_path):
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["docs/notes.md", "Makefile"])

    assert "<summary><b>Changed files no requirement claims</b>: 2 files</summary>" in out
    assert "docs/notes.md" in out and "Makefile" in out


def test_a_changed_path_keeps_the_dot_its_name_begins_with(tmp_path):
    """A leading `./` is noise and comes off; a leading `.` is the name.

    `norm()` dropped both, because `lstrip` takes a set of characters and not a
    prefix, so every dot-directory in the repository printed one character short
    and the links built from the same string pointed at a path that is not there.
    """
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head,
                    [".ci/workflows/check.yml", "./docs/notes.md", "...dots/odd.md"])

    lines = out.splitlines()
    assert "- `.ci/workflows/check.yml`" in lines, (
        "the dot the name begins with was eaten:\n"
        + "\n".join(ln for ln in lines if "check.yml" in ln))
    assert "- `...dots/odd.md`" in lines, "every leading dot came off, not just the first"
    # The noise still goes: `./docs/notes.md` is `docs/notes.md`.
    assert "- `docs/notes.md`" in lines
    assert "- `./docs/notes.md`" not in lines


def test_a_project_root_of_one_dot_still_means_the_repository_root(tmp_path):
    """`--config specassay-check-config.yml` and no `--project-root` makes the
    project root exactly `.`, and the prefix matching needs the empty prefix.

    The old `norm()` supplied that by eating the dot. Dropping the dot-eating
    without saying so turned every changed file into one outside the governed
    project, and the report then claimed every changed file was claimed. This
    holds the answer whichever spelling of the root arrives.
    """
    base = head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    for root in (".", "./", ""):
        out, _ = report(tmp_path, base, head, ["docs/notes.md"], project_root=root)
        assert "**1** changed file no requirement claims" in verdict_line(out), (
            f"with project_root={root!r} an unclaimed file went missing:\n"
            + verdict_line(out))
        assert "- `docs/notes.md`" in out.splitlines()


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

    assert out.startswith("## SpecAssay Report")
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


def test_AC_THREAD_20a_an_added_or_a_retired_requirement_needs_a_person(tmp_path):
    """@covers AC-THREAD-20a

    Amended 2026-11-28. Each of the two alone, with the gate green and no tick
    asked for, so neither can pass on the strength of the other or of a
    rewording.
    """
    kept = row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))

    added, _ = report(tmp_path, [kept], [kept, row("AC-NEW-10", "backlog")], ["PRD.md"])
    assert "🟡 **Needs a person**" in verdict_line(added), verdict_line(added)
    assert "Ready to review" not in added

    retired, _ = report(tmp_path, [kept, row("AC-OLD-10", "backlog")], [kept], ["PRD.md"])
    assert "🟡 **Needs a person**" in verdict_line(retired), verdict_line(retired)
    assert "Ready to review" not in retired

    # The control: the registry file changed and no requirement did.
    same, _ = report(tmp_path, [kept], [kept], ["PRD.md"])
    assert "🟢 **Ready to review**" in verdict_line(same), verdict_line(same)


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


def test_AC_THREAD_20b_no_house_word_appears_anywhere_in_the_comment(tmp_path):
    """@covers AC-THREAD-20b

    The whole report, in its loudest state: every section rendered, both ticks
    required, a receipt attached. Until 2026-11-28 this read only above the
    footer, because the footer was where three house words were defined. The
    footer is read now too.

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

    assert "\n---\n" in out, "the footer is gone, so this would read nothing of it"
    for word in HOUSE_WORDS:
        for spelling in (word, word.capitalize()):
            assert spelling not in out, (
                f"the house word {spelling!r} is in the comment:\n"
                + "\n".join(ln for ln in out.splitlines() if spelling in ln)
            )


def test_AC_THREAD_20b_the_footer_carries_no_glossary(tmp_path):
    """@covers AC-THREAD-20b

    The list defined Golden Thread, off thread and mint. With the first two
    retired from the comment it would have taught one word the comment never
    prints, so the whole list went.
    """
    for out in every_shape(tmp_path):
        footer = out.rsplit("\n---\n", 1)[1]
        assert "Words used here" not in footer
        for word in ("Golden Thread", "Off thread", "Mint"):
            assert word not in footer, word
        # Still one line, so it reads as a footnote.
        assert len([ln for ln in footer.splitlines() if ln.strip()]) == 1


# --- the name, and what blocks ---------------------------------------------
# Amended 2026-11-27: the comment is named the SpecAssay Report. Its title line
# says what it is for, its footer says what blocks and what never does, and the
# footer's hint stops handing a reader a configuration key.

PLAIN_LINE = ("What this change was asked to do, and what it changed that no "
              "requirement asked for.")


def every_shape(tmp_path):
    """The report in the shapes that print the most: a quiet green, a refusal,
    and a reworded requirement with both ticks required and a receipt attached."""
    (tmp_path / "run.md").write_text("gate: verdict GREEN, exit 0\n")
    quiet = [row("AC-SYNC-10", "proven", proofs=("tests/t.py",))]
    yield report(tmp_path, quiet, quiet)[0]
    yield report(tmp_path, quiet, [row("AC-SYNC-10", "GAP")], gate_ok=False)[0]
    yield report(
        tmp_path,
        [row("AC-SYNC-20", "proven", statement="AC-SYNC-20 — Retries after 5s.",
             proofs=("tests/test_sync.py",))],
        [row("AC-SYNC-20", "proven", statement="AC-SYNC-20 — Retries after 2s.",
             proofs=("tests/test_sync.py",)),
         row("AC-NEW-10", "backlog")],
        ["tests/test_sync.py", "PRD.md", "Makefile"],
        offthread_ack="required", intent_ack="required",
        receipts=str(tmp_path / "run.md"),
    )[0]


def test_AC_THREAD_20e_the_title_line_is_the_name_and_the_plain_line(tmp_path):
    """@covers AC-THREAD-20e

    One source line, so the verdict stays where AC-THREAD-10 holds it. The old
    name is checked in every shape, not in one: a name that survives in a
    section only a refusal prints is still a name a reader meets.
    """
    for out in every_shape(tmp_path):
        lines = [ln for ln in out.splitlines() if ln.strip()]
        title = lines[0]
        assert title.startswith("## SpecAssay Report"), title
        assert PLAIN_LINE in title, title
        for dash in ("—", "–", " - "):
            assert dash not in title, f"a dash joins the name to the plain line: {title}"
        assert any(lines[1].startswith(dot) for dot in ("🟢", "🟡", "🔴")), (
            f"the verdict is no longer the second non-empty line:\n{lines[1]}"
        )
        assert "Thread Report" not in out
        assert "🧵" not in out


def test_AC_THREAD_20f_the_footer_says_what_blocks_and_what_never_does(tmp_path):
    """@covers AC-THREAD-20f"""
    for out in every_shape(tmp_path):
        footer = out.rsplit("\n---\n", 1)[1]
        assert "This comment reports; it never blocks." in footer
        assert "The check blocks when the Gate refuses." in footer
        assert "A changed file no requirement claims is a note, not a failure." in footer


def test_AC_THREAD_20g_the_footer_hint_prints_no_configuration_key(tmp_path):
    """@covers AC-THREAD-20g

    The negative control is the tick line: with a tick required the key is still
    printed there, because AC-THREAD-20d holds that suffix for the workflows. So
    this test cannot be passed by scrubbing the key from the whole comment.
    """
    quiet = [row("AC-SYNC-10", "proven", proofs=("tests/t.py",))]
    out, _ = report(tmp_path, quiet, quiet, ["Makefile"])
    footer = out.rsplit("\n---\n", 1)[1]
    assert "can ask a person to tick off the unclaimed files" in footer
    assert "_ack" not in out, "a configuration key is printed with no tick asked for"
    assert "`" not in footer, "the footer still prints something as code"

    held, _ = report(tmp_path, quiet, quiet, ["Makefile"], offthread_ack="required")
    assert "`offthread_ack: required`)_" in held


# --- who should read it -----------------------------------------------------
# Added 2026-11-28. A pull request that changes the requirements themselves is
# a different kind of thing from one that changes code, and one line says so.

CHANGES_LEAD = "⚠️ This pull request changes what the code is required to do."
NO_OWNER = CHANGES_LEAD + " Someone who owns the requirements should read it before it merges."


def non_empty(text: str) -> list:
    return [ln for ln in text.splitlines() if ln.strip()]


def test_AC_THREAD_20h_a_change_to_the_requirements_is_marked_under_the_verdict(tmp_path):
    """@covers AC-THREAD-20h

    One requirement change at a time, so each of the three is shown to raise
    the line on its own. The line is the third non-empty one: the title, the
    verdict, then this.
    """
    kept = row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))
    was = row("AC-SYNC-20", "proven", statement="AC-SYNC-20 — Retries after 5s.",
              proofs=("tests/test_sync.py",))
    now = row("AC-SYNC-20", "proven", statement="AC-SYNC-20 — Retries after 2s.",
              proofs=("tests/test_sync.py",))
    shapes = {
        "added": ([kept], [kept, row("AC-NEW-10", "backlog")]),
        "retired": ([kept, row("AC-OLD-10", "backlog")], [kept]),
        "reworded": ([kept, was], [kept, now]),
    }
    for name, (base, head) in shapes.items():
        out, _ = report(tmp_path, base, head, ["PRD.md"])
        lines = non_empty(out)
        assert lines[2] == NO_OWNER, f"{name}: the third line is\n{lines[2]}"
        assert out.count(CHANGES_LEAD) == 1, name
        # No counts: the verdict line above carries them.
        assert not any(ch.isdigit() for ch in lines[2]), lines[2]


def test_AC_THREAD_20h_a_change_to_code_alone_is_not_marked(tmp_path):
    """@covers AC-THREAD-20h

    The negative control, on the common pull request: a requirement gains its
    test, a file nobody claims changes, and no requirement is added, retired or
    reworded.
    """
    base = [row("AC-SYNC-10", "backlog")]
    head = [row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))]
    out, _ = report(tmp_path, base, head, ["tests/test_sync.py", "Makefile"])

    assert "changes what the code is required to do" not in out
    assert "🟢 **Ready to review**" in verdict_line(out)


def test_AC_THREAD_20h_on_a_refused_run_the_refusal_is_still_named_first(tmp_path):
    """@covers AC-THREAD-20h

    AC-THREAD-30a keeps the line that names the refusals first under the
    verdict, so on a red report this line is the fourth, not the third.
    """
    (tmp_path / "base.json").write_text(json.dumps(
        {"rows": [row("AC-SYNC-10", "proven", proofs=("tests/t.py",))],
         "gate": {"ok": True}}))
    (tmp_path / "head.json").write_text(json.dumps(
        {"rows": [row("AC-SYNC-10", "proven", proofs=("tests/t.py",)),
                  row("AC-NEW-10", "GAP")],
         "gate": {"ok": False, "failures": [
             {"id": "AC-NEW-10", "kind": "silent-gap", "detail": "no test names it"}]}}))
    (tmp_path / "changed.txt").write_text("PRD.md\n")
    proc = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--base", str(tmp_path / "base.json"), "--head", str(tmp_path / "head.json"),
         "--changed-files", str(tmp_path / "changed.txt"),
         "--repo-root", str(tmp_path)],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    lines = non_empty(proc.stdout)

    assert lines[1].startswith("🔴 **Do not merge yet**"), lines[1]
    assert lines[2].startswith("The Gate refused:"), lines[2]
    assert lines[3] == NO_OWNER, lines[3]


def codeowners_report(tmp_path, codeowners, place=".github/CODEOWNERS", **flags):
    """A report on a pull request that adds one requirement, rendered beside a
    CODEOWNERS file. Every handle in these files is made up."""
    target = tmp_path / place
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(codeowners)
    kept = row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))
    out, _ = report(tmp_path, [kept], [kept, row("AC-NEW-10", "backlog")],
                    ["PRD.md"], **flags)
    return non_empty(out)[2]


def test_AC_THREAD_20i_the_line_names_the_owner_codeowners_names(tmp_path):
    """@covers AC-THREAD-20i"""
    line = codeowners_report(tmp_path, "# who reviews what\nPRD.md @acme/product\n")
    assert line == (CHANGES_LEAD + " @acme/product owns the requirements file "
                    "and should read it before it merges."), line


def test_AC_THREAD_20i_the_verb_agrees_with_the_number_of_owners(tmp_path):
    """@covers AC-THREAD-20i, AC-THREAD-20c"""
    two = codeowners_report(tmp_path, "/PRD.md @acme/product @river\n")
    assert "@acme/product and @river own the requirements file and should" in two, two

    three = codeowners_report(tmp_path, "/PRD.md @acme/product @river @acme/qa\n")
    assert "@acme/product, @river and @acme/qa own the requirements file" in three, three


def test_AC_THREAD_20i_the_last_matching_pattern_wins_as_it_does_on_github(tmp_path):
    """@covers AC-THREAD-20i

    Three rules match the registry file here. GitHub asks the owners on the
    last of them, so the comment names those and no others.
    """
    line = codeowners_report(
        tmp_path,
        "*        @acme/everyone\n"
        "*.md     @acme/docs\n"
        "/PRD.md  @acme/product   # the requirements\n"
        "/src/    @acme/engineers\n",
    )
    assert "@acme/product owns" in line, line
    for other in ("@acme/everyone", "@acme/docs", "@acme/engineers"):
        assert other not in line, line


def test_AC_THREAD_20i_the_first_file_github_would_read_is_the_one_read(tmp_path):
    """@covers AC-THREAD-20i"""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "CODEOWNERS").write_text("PRD.md @acme/from-docs\n")
    (tmp_path / "CODEOWNERS").write_text("PRD.md @acme/from-root\n")
    line = codeowners_report(tmp_path, "PRD.md @acme/from-github\n")
    assert "@acme/from-github owns" in line, line

    (tmp_path / ".github" / "CODEOWNERS").unlink()
    kept = row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))
    out, _ = report(tmp_path, [kept], [kept, row("AC-NEW-10", "backlog")], ["PRD.md"])
    assert "@acme/from-root owns" in non_empty(out)[2]


def test_AC_THREAD_20i_a_registry_in_a_subdirectory_is_matched_from_the_root(tmp_path):
    """@covers AC-THREAD-20i

    CODEOWNERS names paths from the repository root; the config names the
    registry from the project. A project living in a subdirectory needs the two
    joined, or its owner is never found.
    """
    (tmp_path / "apps" / "lending").mkdir(parents=True)
    config = tmp_path / "apps" / "lending" / "specassay-check-config.yml"
    config.write_text('registry: "REQUIREMENTS.md"\n')
    line = codeowners_report(
        tmp_path,
        "/REQUIREMENTS.md               @acme/wrong-project\n"
        "/apps/lending/REQUIREMENTS.md  @acme/lending\n",
        config=config, project_root="apps/lending",
    )
    assert "@acme/lending owns" in line, line


def test_AC_THREAD_20i_with_no_owner_to_name_the_line_is_whole(tmp_path):
    """@covers AC-THREAD-20i

    Four ways to have no owner, and the line reads the same in each: no file; a
    file that does not cover the registry; a last match that deliberately names
    nobody; and an owner given only as an email address, which a public comment
    does not print.
    """
    kept = row("AC-SYNC-10", "proven", proofs=("tests/test_sync.py",))
    out, _ = report(tmp_path, [kept], [kept, row("AC-NEW-10", "backlog")], ["PRD.md"])
    assert non_empty(out)[2] == NO_OWNER

    for codeowners in (
        "/src/ @acme/engineers\n",
        "* @acme/everyone\n/PRD.md\n",
        "/PRD.md owner@example.com\n",
    ):
        line = codeowners_report(tmp_path, codeowners)
        assert line == NO_OWNER, f"{codeowners!r} gave:\n{line}"
        assert "@" not in line


def test_AC_THREAD_20j_the_comments_own_words_carry_no_em_dash(tmp_path):
    """@covers AC-THREAD-20j

    Every shape, plus the two that print the cell and a retirement. The fixture
    statements open `ID — text`, which the report strips before quoting, so an
    em dash found here is one the comment wrote itself.
    """
    shapes = list(every_shape(tmp_path))
    shapes.append(report(tmp_path, [row("AC-SYNC-10", "backlog")],
                         [row("AC-SYNC-10", "tracked-debt")])[0])
    kept = row("AC-SYNC-10", "proven", proofs=("tests/t.py",))
    shapes.append(report(tmp_path, [kept, row("AC-OLD-10", "backlog")], [kept],
                         ["PRD.md", "Makefile"], offthread_ack="record",
                         intent_ack="record")[0])
    for out in shapes:
        for dash in ("—", "–"):
            assert dash not in out, (
                "a dash is in the comment's own words:\n"
                + "\n".join(ln for ln in out.splitlines() if dash in ln)
            )


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
    assert "</b>: 1 file</summary>" in out
    assert "</b>: 2 requirements in 2 areas" in out


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
