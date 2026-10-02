"""FR-GATE-180: a fenced registry line is a quotation, not a mint.

Found writing the registry seed the bundle now ships (2026-10-02). FR-GATE-40 had
already settled this question for `@covers` marks and test names; the registry's
own reader was left out of that fix, so a `PRD.md` showing a reader what a row
looks like minted promises nobody had made, and the Gate refused the project over
its own documentation.

The second test covers the readers nobody thinks of: a fenced row must not raise
the next mint, lend its style, or look like a collision.
"""

import subprocess
from pathlib import Path

MINT = Path(__file__).resolve().parents[1] / "scripts" / "mint-id.sh"

FENCED_REGISTRY = """# Fixture PRD

Here is what a row looks like:

```markdown
- AC-DEMO-10 — Given a thing, when it happens, then the result. **Authorship**: design
- FR-DEMO-10 — The thing happens. **Authorship**: design
```

And a tilde fence, which Markdown allows just as much:

~~~markdown
- AC-DEMO-20 — Given another thing, when it happens, then another result.
~~~

- AC-REAL-10 — Given a real promise, when the Gate runs, then it is read as one. **Authorship**: case
"""


def _mint(project, *args):
    return subprocess.run(
        ["bash", str(MINT), *args],
        cwd=project.root,
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "SPECASSAY_PROJECT_ROOT": str(project.root),
            "SPECASSAY_CONFIG": str(project._config),
        },
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_AC_GATE_180_a_fenced_row_is_not_a_promise(project):
    """@covers AC-GATE-180"""
    project.write("PRD.md", FENCED_REGISTRY)
    project.config()
    project.write(
        "specs/thing/spec.md",
        "# Spec\n\n- AC-REAL-10 — the real promise.\n",
    )
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T001 Do the thing — **Carries**: AC-REAL-10\n",
    )
    proc, manifest = project.run()

    ids = [r["id"] for r in manifest["rows"]]
    assert ids == ["AC-REAL-10"], (
        "a fenced row reached the manifest; the registry reader is still counting "
        f"quotations as mints: {ids}"
    )
    assert manifest["gate"]["ok"] is True, manifest["gate"]["failures"]
    for fenced in ("AC-DEMO-10", "FR-DEMO-10", "AC-DEMO-20"):
        assert fenced not in proc.stdout + proc.stderr, (
            f"{fenced} was named in the Gate's output"
        )

    # The line number for the real row still points at the real line: blanking a
    # fenced line keeps the file's numbering, deleting it would not.
    expected = FENCED_REGISTRY.splitlines().index(
        [ln for ln in FENCED_REGISTRY.splitlines() if ln.startswith("- AC-REAL-10")][0]
    ) + 1
    assert project.row(manifest, "AC-REAL-10")["registry"]["line"] == expected


def test_AC_GATE_180b_a_fenced_row_does_not_move_the_next_mint(project):
    """@covers AC-GATE-180b

    AC-DEMO-10 and AC-DEMO-20 sit in fences. If the next-number scan read them,
    the next DEMO mint would be AC-DEMO-30 instead of AC-DEMO-10.
    """
    project.write("PRD.md", FENCED_REGISTRY)
    project.config()

    proc = _mint(project, "AC", "DEMO")
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "AC-DEMO-10", (
        f"a fenced row raised the next mint: {proc.stdout.strip()}"
    )

    # And the style imitated is the real row's, not a fenced one's. Both happen to
    # be written the same way here, so the assertion that carries weight is the
    # one above; this one guards the scan that picks the template from crashing
    # or picking a line inside a fence.
    assert "- AC-DEMO-10 —" in proc.stderr
