"""AC-CASE-50c: the rollup colour rule is stated in the schema page itself.

FR-CASE-50 puts the rule in `docs/trace-manifest-v5.md` and not only in the
registry, with the reason written into the row: a count does not tell a
renderer what colour to paint, every viewer that wanted one has so far decided
for itself, and a manifest whose readers disagree is the capture-method failure
`PROMOTION-CONTRACT.md` rule 12 names. So the page a viewer author actually
reads has to carry the rule in full, with no access to this repository's
registry.

This test is the only thing standing between that and a page that drifts from
the emitter. It reads the shipped document, not a copy.
"""

from pathlib import Path

DOC = Path(__file__).resolve().parents[1] / "docs" / "trace-manifest-v5.md"


def _rollup_section() -> str:
    text = DOC.read_text(encoding="utf-8")
    start = text.index("#### The colour rule")
    end = text.index("\n## ", start)
    return text[start:end]


def test_AC_CASE_50c_the_colour_rule_is_stated_in_the_v5_schema_page():
    section = _rollup_section()

    # The weakest-started rule, its order of weakness, and both edge cases: a
    # viewer implementing from this page alone needs every one of them.
    assert "weakest started" in section
    assert "`GAP`, then `tracked-debt`, then `proven`" in section
    assert "counted but never coloured" in section
    assert "nothing started beneath it is" in section
    for value in ("GAP", "tracked-debt", "proven", "backlog", "retired"):
        assert value in section, value

    # The basis, which is the half a reader gets wrong: the subtree, not the
    # children alone.
    assert "subtree, not the children alone" in section

    # And where the colour is published, since SpecAssay puts it on a row's
    # own `status` for objectives and nowhere else.
    assert "objective" in section


def test_AC_CASE_50c_the_rule_is_dated_so_a_reader_can_place_it():
    assert "ratified 2026-09-22" in _rollup_section()
