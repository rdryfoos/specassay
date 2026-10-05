"""FR-GATE-220: an AC ID counts as a test's name only in name position.

Found in Loupe, 2026-10-02, running 0.5.5 against it. Six IDs appeared nowhere
but inside fixture rows handed to a forest builder, written

    row({ id: "AC-UI-40", type: "AC" })

and the Gate read all six as passing tests, then refused the project twice over
for each: once as untraced scope, once as an uncovered proof. Loupe's own titles,
`it("AC-BUILD-10: ...")`, were right the whole time. The scan was a per-line grep
and a grep cannot tell a test's name from a test's argument.

Every vitest, jest and node:test adopter writes its test names as strings, so
narrowing `test_ac_regex` is not a workaround available to any of them.
"""

HYPHEN_AC_RE = "AC-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"


def _project(project, prd_rows, test_files, covers=(), **config):
    project.prd(*(f"- {row}" for row in prd_rows))
    spec = "\n".join(f"- {row.split(' ')[0]} — in the spec." for row in prd_rows)
    project.write("specs/thing/spec.md", f"# Spec\n\n{spec}\n")
    carries = ", ".join(row.split(" ")[0] for row in prd_rows)
    project.write(
        "specs/thing/tasks.md",
        f"- [x] T001 Build the thing — **Carries**: {carries}\n",
    )
    project.write(
        "src/thing.js",
        "".join(f"// @covers {id_}\n" for id_ in covers) + "export const thing = 1;\n",
    )
    for rel, body in test_files.items():
        project.write(rel, body)
    config.setdefault("test_ac_regex", HYPHEN_AC_RE)
    project.config(**config)
    return project.run()


def test_AC_GATE_220a_fixture_data_is_not_a_test_name(project):
    """@covers AC-GATE-220a"""
    proc, manifest = _project(
        project,
        ["AC-REAL-10 — Given a real promise, when the Gate runs, then it is proven."],
        {
            "tests/descent.test.js": (
                'import { buildForest } from "./descent";\n'
                "\n"
                'describe("buildForest", () => {\n'
                '  it("AC-REAL-10: a story node carries its children", () => {\n'
                '    const rows = [row({ id: "AC-GHOST-10", type: "AC" })];\n'
                '    expect(ids(rows)).toEqual(["AC-GHOST-20", "AC-GHOST-30"]);\n'
                "    // AC-GHOST-40 is the shape this fixture is standing in for\n"
                "  });\n"
                "});\n"
            )
        },
        covers=["AC-REAL-10"],
    )

    assert project.row(manifest, "AC-REAL-10")["status"] == "proven", (
        "the title's own ID stopped counting"
    )
    output = proc.stdout + proc.stderr
    for ghost in ("AC-GHOST-10", "AC-GHOST-20", "AC-GHOST-30", "AC-GHOST-40"):
        assert ghost not in output, f"{ghost} is test data and the Gate named it"
    assert [r["id"] for r in manifest["rows"]] == ["AC-REAL-10"]
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]


def test_AC_GATE_220b_a_title_is_a_name_wrapped_or_not(project):
    """@covers AC-GATE-220b

    Prettier and friends put a long title on its own line, which leaves `it(`
    alone on one line and the name on the next.
    """
    proc, manifest = _project(
        project,
        [
            "AC-ONE-10 — Given a one-line title, when the Gate runs, then it names the test.",
            "AC-TWO-10 — Given a wrapped title, when the Gate runs, then it names the test.",
        ],
        {
            "tests/wrap.test.js": (
                'it("AC-ONE-10: the title sits on the call", () => {});\n'
                "\n"
                "it(\n"
                '  "AC-TWO-10: the title sits on its own line, which is how a formatter leaves it",\n'
                "  () => {},\n"
                ");\n"
            )
        },
        covers=["AC-ONE-10", "AC-TWO-10"],
    )

    for id_ in ("AC-ONE-10", "AC-TWO-10"):
        assert project.row(manifest, id_)["status"] == "proven", (
            f"{id_} is in title position and was not counted"
        )
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]


def test_AC_GATE_220c_any_delimiter_after_the_id(project):
    """@covers AC-GATE-220c

    The three shapes Loupe actually writes, including the AMENDED titles whose
    ID is followed by a space and a parenthetical rather than a colon, plus the
    one shape that is not an ID at all: an ID with more name run onto it.
    """
    proc, manifest = _project(
        project,
        [
            "AC-COLON-10 — Given a colon after the ID, when the Gate runs, then the title names it.",
            "AC-SPACE-10 — Given a space after the ID, when the Gate runs, then the title names it.",
            "AC-PAREN-10 — Given a parenthesis after the ID, when the Gate runs, then the title names it.",
        ],
        {
            "tests/shapes.test.js": (
                'it("AC-COLON-10: the ordinary shape", () => {});\n'
                'it("AC-SPACE-10 (AMENDED 2026-08-28, Cards retirement): the shape Loupe writes", () => {});\n'
                'it("AC-PAREN-10(surviving clause) still returns to the field", () => {});\n'
                'it("AC-RUNON-10X is not an ID and names nothing", () => {});\n'
            )
        },
        covers=["AC-COLON-10", "AC-SPACE-10", "AC-PAREN-10"],
    )

    for id_ in ("AC-COLON-10", "AC-SPACE-10", "AC-PAREN-10"):
        assert project.row(manifest, id_)["status"] == "proven", (
            f"{id_} is in title position and was not counted"
        )
    assert "AC-RUNON-10" not in proc.stdout + proc.stderr, (
        "AC-RUNON-10X was read as AC-RUNON-10 with a stray X"
    )
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]


def test_AC_GATE_220d_a_row_proven_only_by_data_is_named(project):
    """@covers AC-GATE-220d

    The one upgrade this rule can change under a project's feet: a registry row
    that 0.5.5 called proven because its ID sat in a fixture. The run says so
    rather than letting the status move in silence.
    """
    proc, manifest = _project(
        project,
        [
            "AC-REAL-10 — Given a real promise, when the Gate runs, then it is proven.",
            "AC-DATA-10 — Given a promise named only in test data, when the Gate runs, then it is not proven.",
        ],
        {
            "tests/descent.test.js": (
                'it("AC-REAL-10: the title names this one", () => {\n'
                '  const rows = [row({ id: "AC-DATA-10", type: "AC" })];\n'
                "});\n"
            )
        },
        covers=["AC-REAL-10", "AC-DATA-10"],
    )

    diagnostics = manifest["gate"]["diagnostics"]
    named = [
        d
        for d in diagnostics
        if d.get("id") == "AC-DATA-10" and d["kind"] == "test-data-not-a-name"
    ]
    assert named, f"AC-DATA-10 lost a proof without a word: {diagnostics}"
    detail = named[0]["detail"]
    assert "tests/descent.test.js:2" in detail, detail
    assert "test data, not a test name" in detail, detail
    assert project.row(manifest, "AC-DATA-10")["status"] != "proven"

    # Once, not once per reader.
    assert len(named) == 1, named


def test_AC_GATE_220e_a_function_named_suite_is_unchanged(project):
    """@covers AC-GATE-220e

    The stock grammar, where the ID lives in the function's own name. No string
    title is declared anywhere in the file, so the file keeps the old reading:
    every match in it is a name. A project on this convention sees no change.
    """
    proc, manifest = _project(
        project,
        ["AC-STOCK-10 — Given a function-named suite, when the Gate runs, then it reads as before."],
        {
            "tests/test_stock.py": (
                "def test_AC_STOCK_10_the_name_is_the_function():\n"
                "    assert True\n"
            )
        },
        covers=["AC-STOCK-10"],
        test_ac_regex="AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?",
    )

    assert project.row(manifest, "AC-STOCK-10")["status"] == "proven", (
        "the stock grammar stopped being read"
    )
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]


def test_AC_GATE_220e_test_code_as_data_declares_nothing(project):
    """@covers AC-GATE-220e

    The file this very suite is: a function-named pytest file that carries
    `it("AC-X-10: ...")` inside a Python string, to hand the Gate a fixture.
    The characters are there; the declaration is not. Reading that file as
    string-named cost the stock grammar its names, which is how the shape was
    found: this suite stopped proving its own criteria.
    """
    proc, manifest = _project(
        project,
        ["AC-STOCK-10 — Given test code held as data, when the Gate runs, then it declares nothing."],
        {
            "tests/test_fixtures.py": (
                "FIXTURE = (\n"
                '    \'it("AC-OTHER-10: a title the fixture hands to the checker", () => {});\\n\'\n'
                ")\n"
                "\n"
                "\n"
                "def test_AC_STOCK_10_the_name_is_still_the_function():\n"
                "    assert FIXTURE\n"
            )
        },
        covers=["AC-STOCK-10"],
        test_ac_regex="AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?",
    )

    assert project.row(manifest, "AC-STOCK-10")["status"] == "proven", (
        "a quoted it( was read as a declaration, and the function's own name "
        "stopped counting"
    )
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]
