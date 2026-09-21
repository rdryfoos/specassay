"""A task's Carries list that wraps must read the same to every scan.

Found in the Bang rehearsal on v0.5.1. A tasks.md task whose **Carries**
list ran onto a second line produced three acceptance criteria that the
exact-set scan counted as claimed and the pending scan never saw. The two
scans read the same file and disagreed about it, so the Gate reported
silent gaps with nothing to say about why: the truth was not "gap", it was
"your parser and my parser differ".

The cause is one line apart in the source. tasks.txt is built by scanning
every line of the file; pending.txt is built from `grep -nE '^- \\[ \\]'`,
which sees the checkbox line and nothing after it. An ID on a continuation
line therefore lands in one set and not the other.

That is the capture method lying about what it captures, which this
repository's own PROMOTION-CONTRACT rule 12 names. These tests pin the
agreement rather than either scan's private answer.
"""

TASK_WRAPPED = (
    "- [ ] T900 A task whose promise list runs past one line "
    "— **Carries**: AC-WRAP-10, AC-WRAP-20,\n"
    "  AC-WRAP-30\n"
)

TASK_ONE_LINE = (
    "- [ ] T900 A task whose promise list fits on one line "
    "— **Carries**: AC-WRAP-10, AC-WRAP-20, AC-WRAP-30\n"
)


def _fixture(project, task_text):
    project.prd(
        "## WRAP",
        "- FR-WRAP-10 — the wrapped-carries fixture's parent intent.",
        "  - AC-WRAP-10 — first criterion.",
        "  - AC-WRAP-20 — second criterion.",
        "  - AC-WRAP-30 — third criterion, the one that wraps.",
    )
    project.write(
        "specs/backlog/spec.md",
        "# Fixture spec\n\n- FR-WRAP-10\n- AC-WRAP-10\n- AC-WRAP-20\n- AC-WRAP-30\n",
    )
    project.write("specs/backlog/tasks.md", "# Tasks\n\n" + task_text)
    project.config()
    return project.run()


def test_AC_GATE_140_wrapped_carries_reads_the_same_to_both_scans(project):
    """The contract. Whatever the Gate decides a wrapped task carries, it
    must decide it once. A row may be backlog or tracked debt, but it may
    not be claimed by one scan and invisible to the other, which is what
    produces a GAP nobody can explain."""
    proc, manifest = _fixture(project, TASK_WRAPPED)
    assert manifest is not None, proc.stderr

    statuses = {r["id"]: r["status"] for r in manifest["rows"] if r["id"].startswith("AC-WRAP")}
    assert statuses, "fixture produced no AC-WRAP rows"

    # The row on the continuation line must not be treated differently from
    # the rows on the checkbox line. They are one claim.
    assert len(set(statuses.values())) == 1, (
        "the wrapped Carries list split one claim into two verdicts: "
        f"{statuses}\nstderr:\n{proc.stderr}"
    )


def test_AC_GATE_140_wrapping_a_carries_list_changes_no_verdict(project):
    """Same three IDs, same task, only the line breaks differ. A soft wrap
    is a typographic accident; it must not move a row between statuses."""
    _, wrapped = _fixture(project, TASK_WRAPPED)
    _, flat = _fixture(project, TASK_ONE_LINE)
    assert wrapped is not None and flat is not None

    def statuses(m):
        return {r["id"]: r["status"] for r in m["rows"] if r["id"].startswith("AC-WRAP")}

    assert statuses(wrapped) == statuses(flat), (
        f"wrapped: {statuses(wrapped)}\nflat:    {statuses(flat)}"
    )


def test_AC_GATE_140_a_wrapped_task_is_not_a_silent_gap(project):
    """The symptom as the rehearsal met it: a GAP with nothing to say why.
    An open task naming an AC is that AC's tracked debt, wrapped or not."""
    proc, manifest = _fixture(project, TASK_WRAPPED)
    gaps = [r["id"] for r in manifest["rows"] if r.get("status") == "GAP"]
    assert not gaps, f"wrapped Carries produced silent gaps: {gaps}\n{proc.stderr}"


TASK_MARK_ON_SECOND_LINE = (
    "- [ ] T901 A task whose promise list begins on the next line\n"
    "  **Carries**: AC-WRAP-10, AC-WRAP-20, AC-WRAP-30\n"
)


def test_AC_GATE_140_a_carries_mark_on_a_continuation_line_is_found(project):
    """The same defect one field over. `missing-carries` also read a task as
    a single physical line, so a task whose mark wrapped was reported as
    having no Carries field at all while plainly having one."""
    proc, manifest = _fixture(project, TASK_MARK_ON_SECOND_LINE)
    assert "missing-carries" not in proc.stderr, proc.stderr
    assert "task missing Carries field" not in proc.stderr, proc.stderr
