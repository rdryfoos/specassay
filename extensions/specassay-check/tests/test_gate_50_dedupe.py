"""FR-GATE-50: the manifest emitter dedupes implementations/proofs on
(id, normpath, line). Regression coverage for a real bug found founding
this repo's own registry: a real emit carried this in 62 of 100 rows.
"""


def test_AC_GATE_50_overlapping_src_globs_do_not_double_count(project):
    # Two src_globs entries that both reach the same file under a
    # different literal path spelling (the ./x vs x shape this bug
    # actually took in production) must still yield one implementation.
    project.prd("- FR-FIX-01 — A thing.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.write(
        "src/thing.py",
        "# @covers FR-FIX-01\ndef thing():\n    return True\n",
    )
    project.config(src_globs=["src/**", "./src/**"])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "FR-FIX-01")
    assert row["status"] == "proven"
    assert len(row["implementations"]) == 1


def test_genuinely_distinct_marks_are_not_over_collapsed(project):
    # The false-positive-dedup risk check: two real marks in two
    # different files for the same ID must both survive.
    project.prd("- FR-FIX-01 — A thing.")
    project.write(
        "specs/backlog/tasks.md",
        "- [ ] T900 stub — **Carries**: FR-FIX-01 (anointed backlog)\n",
    )
    project.write(
        "src/a.py",
        "# @covers FR-FIX-01\ndef a():\n    return True\n",
    )
    project.write(
        "src/b.py",
        "# @covers FR-FIX-01\ndef b():\n    return True\n",
    )
    project.config()

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "FR-FIX-01")
    paths = {impl["path"] for impl in row["implementations"]}
    assert paths == {"src/a.py", "src/b.py"}
    assert len(row["implementations"]) == 2


def test_proofs_are_deduped_the_same_way(project):
    # proof_by had the identical unguarded-append bug as impl_by; same
    # fix, same test shape.
    project.prd("- AC-FIX-01 — A thing.")
    project.write("specs/f/spec.md", "# Feature\n\nCarries AC-FIX-01.\n")
    project.write(
        "specs/f/tasks.md",
        "- [x] T001 Build it — **Carries**: AC-FIX-01\n",
    )
    project.write(
        "src/thing.py",
        "# @covers AC-FIX-01\ndef thing():\n    return True\n",
    )
    project.write(
        "tests/test_thing.py",
        "def test_AC_FIX_01_thing_works():\n    assert True\n",
    )
    project.config(test_globs=["tests/**", "./tests/**"])

    proc, manifest = project.run()

    assert proc.returncode == 0, proc.stderr
    row = project.row(manifest, "AC-FIX-01")
    assert row["status"] == "proven"
    assert len(row["proofs"]) == 1
