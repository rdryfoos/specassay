"""The cold path's own contract: a stranger reaches a Thread Report with no
plumbing of their own.

These tests read the shipped files rather than running an install, on purpose.
What they protect is a promise about what the repository ships: a declaration in
a manifest, and a sentence in each document a stranger meets first. An install
run proves a release; these prove the source of one, on every pull request, which
is where a deletion would otherwise go unnoticed until somebody cold tried it.

The reproduction behind them, 2026-10-02 on 0.5.4 with Spec Kit 1.0.5: `specify
preset add specassay` printed `Preset 'SpecAssay' v0.5.4 installed`, `specify
extension list` then read `No extensions installed.`, and nothing in between said
the Gate was absent. With the declaration below in place the same install ends
`specassay-check is not installed / Install with: specify extension add
specassay-check`.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUNDLE_LINE = "specify bundle install specassay"

# A paragraph earns the warning only by naming the preset-only install itself.
# An earlier draft accepted any paragraph carrying "preset", "Gate" and "only",
# which the start page's own description of the two components already satisfied:
# the test passed with the warning deleted. Caught by deleting it on purpose.
WARNING_PHRASES = (
    "preset add specassay",
    "preset-only install",
    "preset install on its own",
    "preset is the templates",
)

# The three documents a stranger meets before anything else: the start page
# served at specassay.com/start, the project's own front page, and the README
# that ships inside the preset and is therefore the one a preset-only installer
# is left holding.
FRONT_DOORS = [
    Path("ONBOARD.md"),
    Path("README.md"),
    Path("presets/specassay/README.md"),
]


def _preset_manifest_text() -> str:
    return (ROOT / "presets" / "specassay" / "preset.yml").read_text(encoding="utf-8")


def test_AC_COLD_10a_the_preset_declares_the_extension_dependency():
    """@covers AC-COLD-10a

    Read as text rather than as parsed YAML: there is no yaml dependency in this
    suite, and the shape being asserted is a two-line declaration a human edits.
    """
    text = _preset_manifest_text()
    requires = text.split("requires:", 1)[1].split("\nprovides:", 1)[0]
    body = "\n".join(
        line for line in requires.splitlines() if not line.lstrip().startswith("#")
    )
    assert "extensions:" in body, (
        "presets/specassay/preset.yml declares no requires.extensions, so a "
        "preset-only install says nothing about the missing Gate"
    )
    assert re.search(r'-\s+id:\s*"?specassay-check"?', body), (
        "requires.extensions does not name specassay-check"
    )


def test_AC_COLD_10b_the_three_front_doors_name_the_bundle_line():
    """@covers AC-COLD-10b

    Two assertions per document, because naming the right command is not the
    whole promise. A page that lists four commands in order and leaves the reader
    to work out which one matters is the state this row was minted to end, so the
    page must also say, in one paragraph, that the preset on its own does not
    bring the Gate.
    """
    for rel in FRONT_DOORS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert BUNDLE_LINE in text, f"{rel} never names `{BUNDLE_LINE}`"

        warned = False
        for para in re.split(r"\n\s*\n", text):
            flat = " ".join(para.split())
            if "preset" not in flat.lower():
                continue
            if "Gate" not in flat:
                continue
            if any(phrase in flat for phrase in WARNING_PHRASES):
                warned = True
                break
        assert warned, (
            f"{rel} names the bundle line but nowhere says in one paragraph that "
            "the preset on its own leaves the Gate out"
        )
