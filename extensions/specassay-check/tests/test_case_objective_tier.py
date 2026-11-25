"""FR-CASE-20 / 40 / 50 and their criteria: the objective tier, first build.

v5 named three tiers, intent, requirement and criterion, so a walk up from a
test reached the story and stopped: the row above the story had nowhere to
live. This is that row, defined in the case file rather than the registry,
reached by a `Serves` declaration on the story's own registry line, and
refused when the link is false.

The tier's rules were ratified 2026-09-22 and minted as `FR-CASE-10` through
`FR-CASE-60` before any code. This file proves the ones built on 2026-11-19
and names the ones still carried by `T929`: objective IDs assigned by the Gate
and written back into the case (`FR-CASE-10`), nesting as a second citation
form (`AC-CASE-30b`), and measures as objective-level proof (`FR-CASE-60`).

The fixture is invented whole: a night-walking app nobody has written, three
objectives nobody has promised. Nothing in it is copied from any real
project's case, and the IDs are made up to be read.
"""

import json

CASE = """\
# CASE

## What are you betting?

- OBJ-WALK-10 — A walker gets home without stopping to read a map.
- OBJ-POWER-10 — A walker's phone still has charge at the end of the night.
- OBJ-TRUST-10 — Nothing about a walk leaves the walker's own phone.

## Why it matters

The walk is the point, not the phone. OBJ-WALK-10 is the one that scares me:
say the turn too late and the walker has already missed it.
"""

# One story serving one objective, one requirement serving two (the
# cross-cutting shape the list spelling was waiting for), one criterion with a
# real proof behind it, and a second story serving the third objective.
TRUE_REGISTRY = [
    "## Night walking",
    "",
    "- US-WALK-01 — As a walker, I am told the next turn out loud. Serves OBJ-WALK-10",
    "  - FR-WALK-01 — Turns are spoken, never shown. **Serves**: OBJ-WALK-10, OBJ-POWER-10",
    "    - AC-WALK-01 — Given a turn fifty metres ahead, when the walker is moving, then the turn is spoken once.",
    "",
    "## Keeping the lights on",
    "",
    "- US-PHONE-01 — As a walker, I can see how much night the battery has left. Serves OBJ-TRUST-10",
]

IDS = ["US-WALK-01", "FR-WALK-01", "AC-WALK-01", "US-PHONE-01"]


def _fixture(project, registry_lines=None, case_text=CASE, proof=True, **config_overrides):
    """The whole fixture project: case, registry, specs, tasks, source, proof.

    Everything but the registry lines is constant across these tests, so a
    test that changes one line changes exactly one thing.
    """
    registry_lines = TRUE_REGISTRY if registry_lines is None else registry_lines
    project.write("CASE.md", case_text)
    project.prd(*registry_lines)
    ids = [ln.strip().lstrip("- ").split(" ")[0] for ln in registry_lines if " — " in ln]
    project.write("specs/walk/spec.md", "\n".join(ids) + "\n")
    # Every task closed, so that each row's status comes from its own proof
    # and nothing is tracked debt by accident: the criterion is proven by its
    # test, the story and the requirement are planning-altitude backlog, and
    # with `proof=False` the criterion is a real silent gap.
    project.write(
        "specs/walk/tasks.md",
        "".join(f"- [x] T{n} work — **Carries**: {i}\n" for n, i in enumerate(ids, start=1)),
    )
    project.write("src/walk.py", "# @covers AC-WALK-01\ndef speak_turn():\n    return 'left'\n")
    if proof:
        project.write(
            "tests/test_walk.py",
            "def test_AC_WALK_01_speaks_the_turn_once():\n    assert True\n",
        )
    config = {"case": "CASE.md", "parent_derivation": "heading-nesting"}
    config.update(config_overrides)
    project.config(**config)
    return ids


def _v5(project):
    return json.loads((project.root / "trace-manifest.v5beta.json").read_text())


def _row(manifest, id_):
    for r in manifest["rows"]:
        if r["id"] == id_:
            return r
    raise AssertionError(f"{id_} not in {[r['id'] for r in manifest['rows']]}")


def _kinds(manifest, bucket):
    return sorted(f["kind"] for f in manifest["gate"][bucket])


def test_AC_CASE_20a_the_true_fixture_stays_green(project):
    """The control. Every link in it is true, so nothing here is refused."""
    _fixture(project)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert manifest["gate"]["failures"] == []


def test_AC_CASE_50a_the_case_defines_the_objective_rows(project):
    _fixture(project)
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr

    v5 = _v5(project)
    objectives = [r for r in v5["rows"] if r["tier"] == "objective"]
    assert [r["id"] for r in objectives] == ["OBJ-WALK-10", "OBJ-POWER-10", "OBJ-TRUST-10"]
    assert objectives[0]["statement"] == "A walker gets home without stopping to read a map."
    assert objectives[0]["type"] == "OBJ"
    # Where the row lives: the case file and the line, the same shape a
    # registry row's origin carries, under its own kind.
    assert objectives[0]["origin"] == {"kind": "case-line", "path": "CASE.md", "line": 5}
    assert objectives[0]["parents"] == []
    # The set the Gate knows is exactly the set the case defines: a prose
    # citation of OBJ-WALK-10 further down the case is not a second mint.
    assert len([r for r in objectives if r["id"] == "OBJ-WALK-10"]) == 1
    # Counted beside the registry count, because `rows` now holds both kinds.
    assert v5["totals"]["objectiveCount"] == 3
    assert v5["totals"]["registryIdCount"] == len(IDS)

    # v4 is a frozen contract and gains nothing: no objective row reaches it.
    assert sorted(r["id"] for r in manifest["rows"]) == sorted(IDS)


def test_AC_CASE_20a_a_second_definition_of_one_objective_is_refused(project):
    """The same two-sided rule the ID registry gets one tier down."""
    _fixture(project, case_text=CASE + "\n- OBJ-WALK-10 — Said twice, by accident.\n")
    proc, manifest = project.run()

    assert proc.returncode != 0, "a duplicate objective must fail"
    bad = [f for f in manifest["gate"]["failures"] if f["kind"] == "objective-duplicate"]
    assert [f["id"] for f in bad] == ["OBJ-WALK-10"], manifest["gate"]["failures"]
    assert "CASE.md" in bad[0]["detail"]


def test_AC_CASE_20c_numbering_on_the_case_headings_is_decoration(project):
    """Ruled 2026-09-22: a reader that keyed on the numbering would make one
    house style a requirement and lose every objective written in the other."""
    numbered = CASE.replace("- OBJ-", "3. OBJ-")
    assert "3. OBJ-WALK-10" in numbered

    _fixture(project)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr
    plain_rows = [r for r in _v5(project)["rows"] if r["tier"] == "objective"]

    _fixture(project, case_text=numbered)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr
    numbered_rows = [r for r in _v5(project)["rows"] if r["tier"] == "objective"]

    assert [(r["id"], r["statement"]) for r in plain_rows] == [
        (r["id"], r["statement"]) for r in numbered_rows
    ]


def test_AC_CASE_30a_a_story_carries_its_objective_as_its_first_parent(project):
    _fixture(project)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr
    v5 = _v5(project)

    # The story's next tier up IS the objective, so it comes first.
    assert _row(v5, "US-WALK-01")["parents"] == ["OBJ-WALK-10"]
    assert _row(v5, "US-PHONE-01")["parents"] == ["OBJ-TRUST-10"]

    # Below the story, the row above it in the document comes first and the
    # objectives it also serves ride after: a walk down must not jump a tier.
    # Two objectives on one row is the cross-cutting case the list spelling
    # was drafted for and never had until now.
    assert _row(v5, "FR-WALK-01")["parents"] == [
        "US-WALK-01", "OBJ-WALK-10", "OBJ-POWER-10",
    ]
    assert _row(v5, "AC-WALK-01")["parents"] == ["FR-WALK-01"]


def test_AC_CASE_30a_a_walk_from_a_test_reaches_an_objective(project):
    """The whole point, walked the way a viewer walks it: from the proof, up
    the first parent at each hop, until something has no parent."""
    _fixture(project)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr
    v5 = _v5(project)

    start = _row(v5, "AC-WALK-01")
    assert [p["name"] for p in start["proofs"]] == ["test_AC_WALK_01_speaks_the_turn_once"]

    walk = [start["id"]]
    row = start
    while row["parents"]:
        row = _row(v5, row["parents"][0])
        walk.append(row["id"])
        assert len(walk) < 10, f"walk does not terminate: {walk}"

    assert walk == ["AC-WALK-01", "FR-WALK-01", "US-WALK-01", "OBJ-WALK-10"]
    assert [_row(v5, i)["tier"] for i in walk] == [
        "criterion", "requirement", "intent", "objective",
    ]


def test_AC_CASE_30a_the_declaration_does_not_survive_into_the_statement(project):
    """`Serves` is metadata about the row, not part of the promise, so it is
    cut out of the statement the way `**Authorship**` is."""
    _fixture(project)
    proc, manifest = project.run()
    assert proc.returncode == 0, proc.stderr

    for id_ in ("US-WALK-01", "FR-WALK-01", "US-PHONE-01"):
        statement = project.row(manifest, id_)["statement"]
        assert "Serves" not in statement, statement
        assert "OBJ-" not in statement, statement
    assert project.row(manifest, "US-WALK-01")["statement"].endswith("out loud.")


def test_AC_CASE_30a_an_objective_the_case_does_not_hold_turns_the_check_red(project):
    """The false link, and the one shape of it that is a refusal by default:
    the row names a reason that does not exist, which reads as answered."""
    lines = list(TRUE_REGISTRY)
    lines[2] = "- US-WALK-01 — As a walker, I am told the next turn out loud. Serves OBJ-MAP-99"
    _fixture(project, lines)
    proc, manifest = project.run()

    assert proc.returncode != 0, "a story serving an objective the case does not hold must fail"
    assert manifest["gate"]["ok"] is False
    bad = [f for f in manifest["gate"]["failures"] if f["kind"] == "objective-unknown"]
    assert len(bad) == 1, manifest["gate"]["failures"]
    assert bad[0]["id"] == "US-WALK-01"
    # Names the row, the objective and the file, so the fix needs no second look.
    assert "OBJ-MAP-99" in bad[0]["detail"]
    assert "US-WALK-01" in bad[0]["detail"]
    assert "CASE.md" in bad[0]["detail"]
    # The false link is the only failure: the true links are left alone.
    assert _kinds(manifest, "failures") == ["objective-unknown"]


def test_AC_CASE_30c_a_shared_domain_is_not_an_edge(project):
    """FR-CASE-30's refusal, held directly: `US-WALK-01` and `OBJ-WALK-10`
    share a domain and that is all they share."""
    lines = list(TRUE_REGISTRY)
    lines[2] = "- US-WALK-01 — As a walker, I am told the next turn out loud."
    _fixture(project, lines)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr

    v5 = _v5(project)
    assert _row(v5, "US-WALK-01")["parents"] == []
    # And the objective sharing its domain has no story beneath it.
    assert "rollup" not in _row(v5, "OBJ-WALK-10")


def test_AC_CASE_40a_a_story_that_serves_nothing_is_reported_not_refused(project):
    """FR-CASE-40: report-only is the shipped default, and the reason is
    written into that row -- a real registry carries a backlog of orphan
    stories the first time this runs, and a check that reds every adopter on
    first contact is a check they turn off."""
    lines = list(TRUE_REGISTRY)
    lines[2] = "- US-WALK-01 — As a walker, I am told the next turn out loud."
    _fixture(project, lines)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    orphans = [d for d in manifest["gate"]["diagnostics"] if d["kind"] == "orphan-story"]
    assert [d["id"] for d in orphans] == ["US-WALK-01"], manifest["gate"]["diagnostics"]
    assert "OBJ-WALK-10" in orphans[0]["detail"]
    assert not any(f["kind"] == "orphan-story" for f in manifest["gate"]["failures"])
    # Counted in the run's own output, because a backlog nobody can count is
    # a backlog nobody burns down.
    assert "orphan stories: 1 of 2" in proc.stderr
    assert "block_orphan_story" in proc.stderr

    # Only the intent tier is held to it. The requirement and the criterion
    # below this story reach the objective through it, and making every row
    # restate the link would turn one edge into four.
    assert not any(
        d["id"] in ("FR-WALK-01", "AC-WALK-01")
        for d in manifest["gate"]["diagnostics"]
        if d["kind"] == "orphan-story"
    )


def test_AC_CASE_40b_the_ratchet_turns_an_orphan_story_red(project):
    """The same project, on its own word, once its backlog is clear."""
    lines = list(TRUE_REGISTRY)
    lines[2] = "- US-WALK-01 — As a walker, I am told the next turn out loud."
    _fixture(project, lines, block_orphan_story=True)
    proc, manifest = project.run()

    assert proc.returncode != 0, "with the ratchet set, an orphan story must fail"
    assert manifest["gate"]["ok"] is False
    bad = [f for f in manifest["gate"]["failures"] if f["kind"] == "orphan-story"]
    assert [f["id"] for f in bad] == ["US-WALK-01"], manifest["gate"]["failures"]
    assert not any(d["kind"] == "orphan-story" for d in manifest["gate"]["diagnostics"])


def test_AC_CASE_40a_the_word_serves_in_prose_is_not_a_declaration(project):
    """A sentence is not a broken link. `Serves` with no objective after it is
    left as prose, and the story still reads as serving nothing."""
    lines = list(TRUE_REGISTRY)
    lines[2] = "- US-WALK-01 — As a walker, I am told the next turn out loud. Serves the walker, not the phone."
    _fixture(project, lines)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert [d["id"] for d in manifest["gate"]["diagnostics"] if d["kind"] == "orphan-story"] == [
        "US-WALK-01"
    ]
    # The prose stayed prose: nothing was cut out of the statement.
    assert "Serves the walker" in project.row(manifest, "US-WALK-01")["statement"]


def test_AC_CASE_20b_an_objective_no_story_serves_is_backlog_and_named(project):
    """FR-CASE-20's asymmetry, which is the whole design: an unserved
    objective is a promise nobody has started, honest and common."""
    lines = list(TRUE_REGISTRY)
    lines[8] = "- US-PHONE-01 — As a walker, I can see how much night the battery has left. Serves OBJ-POWER-10"
    _fixture(project, lines)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    unserved = [d for d in manifest["gate"]["diagnostics"] if d["kind"] == "objective-unserved"]
    assert [d["id"] for d in unserved] == ["OBJ-TRUST-10"], unserved
    assert "OBJ-TRUST-10" in unserved[0]["detail"]
    assert not any(f["kind"] == "objective-unserved" for f in manifest["gate"]["failures"])

    # Carried as backlog, and with no rollup at all: nothing beneath it.
    row = _row(_v5(project), "OBJ-TRUST-10")
    assert row["status"] == "backlog"
    assert "rollup" not in row


def test_AC_CASE_50b_the_colour_rule_is_the_weakest_started_status(project):
    """Ratified 2026-09-22: the weakest started status among GAP,
    tracked-debt and proven; backlog and retired counted, never coloured; and
    nothing started is backlog."""
    _fixture(project)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr
    v5 = _v5(project)

    # OBJ-WALK-10's subtree is the story, its requirement and the proven
    # criterion. The two planning-altitude rows are backlog, which is counted
    # and never coloured, so the weakest started status beneath it is proven.
    walk = _row(v5, "OBJ-WALK-10")
    assert walk["status"] == "proven"
    assert walk["rollup"] == {
        "rows": 3, "proven": 1, "tracked-debt": 0, "backlog": 2, "GAP": 0, "retired": 0,
    }

    # OBJ-TRUST-10's one story has nothing started beneath it: backlog, and
    # the backlog child is counted even though it is not coloured.
    trust = _row(v5, "OBJ-TRUST-10")
    assert trust["status"] == "backlog"
    assert trust["rollup"] == {
        "rows": 1, "proven": 0, "tracked-debt": 0, "backlog": 1, "GAP": 0, "retired": 0,
    }

    # A requirement that declares Serves keeps the edge without becoming a
    # child of the objective: the tier's children stay one level.
    assert _row(v5, "OBJ-POWER-10")["status"] == "backlog"
    assert "rollup" not in _row(v5, "OBJ-POWER-10")


def test_AC_CASE_50b_a_gap_beneath_a_story_colours_its_objective(project):
    """The weakest started status wins, and a GAP is the weakest: the one
    reading that stops an objective from showing green over a hole."""
    _fixture(project, proof=False)
    proc, manifest = project.run()

    # The criterion lost its proof and its open task, which is a silent gap:
    # the Gate fails on it, and the manifest still has to say what it is.
    assert proc.returncode != 0
    assert project.row(manifest, "AC-WALK-01")["status"] == "GAP"

    v5 = _v5(project)
    assert _row(v5, "OBJ-WALK-10")["status"] == "GAP"
    assert _row(v5, "OBJ-WALK-10")["rollup"]["GAP"] == 1


def test_AC_CASE_20a_the_tier_is_off_until_the_config_names_the_case(project):
    """The upgrade guarantee: with no `case:` key the same fixture reads
    exactly as it did before this change existed. FR-CASE-20 puts the switch
    here on purpose, rather than letting the Gate infer the tier from a
    filename it happens to find."""
    _fixture(project, case="")
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert manifest["gate"]["failures"] == []
    assert not any(
        "objective" in d["kind"] or d["kind"] == "orphan-story"
        for d in manifest["gate"]["diagnostics"]
    )

    v5 = _v5(project)
    assert [r for r in v5["rows"] if r["tier"] == "objective"] == []
    assert v5["totals"]["objectiveCount"] == 0
    assert _row(v5, "US-WALK-01")["parents"] == []
    assert _row(v5, "FR-WALK-01")["parents"] == ["US-WALK-01"]
    # Off means off, down to the prose: with nothing reading the mark, the
    # declaration stays in the statement where the hand wrote it.
    assert "Serves OBJ-WALK-10" in project.row(manifest, "US-WALK-01")["statement"]


def test_AC_CASE_20a_a_case_with_no_objectives_says_so_and_refuses_nothing(project):
    """The config names the case, the case holds nothing yet: a diagnostic,
    not a refusal, and no story is held to a tier nothing has minted."""
    _fixture(project, case_text="# CASE\n\n## What are you betting?\n\nNot sure yet.\n")
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert [
        d["kind"] for d in manifest["gate"]["diagnostics"]
        if d["kind"].startswith("objective")
    ] == ["objectives-none-found"]
    assert manifest["gate"]["failures"] == []
    assert not any(d["kind"] == "orphan-story" for d in manifest["gate"]["diagnostics"])


# A case that keeps its own superseded wording, the way a project that has
# changed its mind writes it: the live objectives defined once each, and the
# old text quoted under a history heading. Invented whole; the three quoted
# shapes are the ones a hand actually writes.
CASE_WITH_HISTORY = CASE + """
## History

The first pass aimed at the phone rather than the walk, and the wording below
is kept so the change of mind can be read.

> - OBJ-WALK-10 An older wording of the first objective
> - OBJ-POWER-10 An older wording of the second
> OBJ-POWER-10 through OBJ-TRUST-10 were seeded from a page that no longer exists
> OBJ-TRUST-10.

A fenced example of the shape, which teaches and mints nothing:

```
- OBJ-WALK-10 — the shape an objective line takes
```
"""


def test_AC_CASE_20e_a_quoted_line_in_the_case_is_history(project):
    """The blocker, found by the first room to take the tier: its case defines
    seven objectives once each and quotes its own superseded wording, and every
    quoted line read as a second definition. Nine refusals on a right file.

    All three shapes are here, and the fenced example with them."""
    _fixture(project, case_text=CASE_WITH_HISTORY)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert not any(
        f["kind"] == "objective-duplicate" for f in manifest["gate"]["failures"]
    ), manifest["gate"]["failures"]

    # The three objectives are the three defined outside the quotes, each once,
    # and each keeps the statement its own definition line gives it.
    v5 = _v5(project)
    objectives = [r for r in v5["rows"] if r["tier"] == "objective"]
    assert [r["id"] for r in objectives] == ["OBJ-WALK-10", "OBJ-POWER-10", "OBJ-TRUST-10"]
    assert objectives[0]["statement"] == "A walker gets home without stopping to read a map."
    assert objectives[0]["origin"]["line"] == 5
    assert v5["totals"]["objectiveCount"] == 3


def test_AC_CASE_20e_a_quoted_line_is_not_a_first_definition_either(project):
    """The rule is about what a quoted line is, not about which one came first:
    an objective that appears ONLY inside a quote is history too, and is not
    minted at all."""
    case = CASE.replace(
        "- OBJ-TRUST-10 — Nothing about a walk leaves the walker's own phone.",
        "> - OBJ-TRUST-10 — An aim this case only ever quoted.",
    )
    lines = list(TRUE_REGISTRY)
    lines[8] = "- US-PHONE-01 — As a walker, I can see how much night the battery has left. Serves OBJ-POWER-10"
    _fixture(project, lines, case_text=case)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    v5 = _v5(project)
    assert [r["id"] for r in v5["rows"] if r["tier"] == "objective"] == [
        "OBJ-WALK-10", "OBJ-POWER-10",
    ]
    # And a story serving it would now be serving an objective the case does
    # not hold, which is the refusal that already exists.
    assert manifest["gate"]["ok"] is True


def test_AC_CASE_20e_a_real_second_definition_is_still_refused(project):
    """The narrowing does not blunt the rule it narrows: two definitions of one
    objective, neither quoted nor fenced, is still drift."""
    _fixture(project, case_text=CASE_WITH_HISTORY + "\n- OBJ-WALK-10 — Said twice, by accident.\n")
    proc, manifest = project.run()

    assert proc.returncode != 0
    bad = [f for f in manifest["gate"]["failures"] if f["kind"] == "objective-duplicate"]
    assert [f["id"] for f in bad] == ["OBJ-WALK-10"], manifest["gate"]["failures"]


def test_AC_CASE_20f_an_anchor_after_the_id_is_read_past(project):
    """A deep-link anchor a hand hangs on the ID is not the first word of the
    objective, and nor is the punctuation holding it."""
    case = CASE.replace(
        "- OBJ-WALK-10 — A walker gets home without stopping to read a map.",
        "- OBJ-WALK-10 {#obj-walk-10}, A walker gets home without stopping to read a map.",
    )
    _fixture(project, case_text=case)
    proc, _ = project.run()
    assert proc.returncode == 0, proc.stderr

    row = _row(_v5(project), "OBJ-WALK-10")
    assert row["statement"] == "A walker gets home without stopping to read a map."


def test_AC_CASE_20d_a_configured_case_file_that_is_not_there_is_refused(project):
    """Ruled 2026-11-23 and shipped in 0.6.0, reversing this room's own first
    call that a missing case file should refuse nothing.

    The first reading was "illuminate, never refuse": the key set and no file
    yet is a state a project passes through while being set up. What that
    missed is what the silence says. The config declares that this project's
    objectives matter; with the file gone the tier switches itself off and the
    run comes back green, so a project that moved or renamed its case is told
    that every link in it is fine when nothing was checked at all. That is the
    one shape of silence this tool exists to refuse.
    """
    _fixture(project, case="objectives/CASE.md")
    proc, manifest = project.run()

    assert proc.returncode != 0, "a case: key naming a file that is not there must fail"
    assert manifest["gate"]["ok"] is False
    bad = [f for f in manifest["gate"]["failures"] if f["kind"] == "case-missing"]
    assert len(bad) == 1, manifest["gate"]["failures"]
    assert bad[0]["detail"] == "case not found: objectives/CASE.md"

    # In plain words, naming the file it looked for, with the path it looked
    # at and all three ways out: create it, repoint the key, or remove it.
    assert "objectives/CASE.md" in proc.stderr
    assert "The config's case: key names the file that holds your objectives" in proc.stderr
    assert "Nothing was checked against your objectives" in proc.stderr
    assert "remove the case: key to turn the objective tier off" in proc.stderr

    # One fault, one finding: the empty-case diagnostic is not also raised.
    assert not any(
        d["kind"] == "objectives-none-found" for d in manifest["gate"]["diagnostics"]
    )
    # And the manifest is still written, the way registry-missing writes it.
    assert _v5(project)["totals"]["objectiveCount"] == 0


def test_AC_CASE_20d_the_same_fixture_with_the_file_back_is_green(project):
    """The other half of the pair: nothing else about the project changed."""
    _fixture(project, case="objectives/CASE.md")
    project.write("objectives/CASE.md", CASE)
    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    assert manifest["gate"]["ok"] is True
    assert manifest["gate"]["failures"] == []
    assert not any(f["kind"] == "case-missing" for f in manifest["gate"]["failures"])

    v5 = _v5(project)
    assert v5["totals"]["objectiveCount"] == 3
    # Read from where the key points, and the origin says so.
    assert _row(v5, "OBJ-WALK-10")["origin"]["path"] == "objectives/CASE.md"
    assert _row(v5, "US-WALK-01")["parents"] == ["OBJ-WALK-10"]
