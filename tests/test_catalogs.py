"""The three hosted catalogs, held to the release they claim.

`catalogs/*.json` is what `specify bundle install specassay` reads, so a value
that drifts here is not a typo in a document: it is an install that resolves the
wrong thing, or fails to resolve at all because the bundle pins component versions
it cannot find.

Nothing checked these until 0.5.5. What went wrong without a check: the per-entry
`updated_at` in the extension and preset catalogs read 2026-09-23 while the entries
beside it described 0.5.4, released 2026-10-01, so the file said two things about
when it was last touched. A date is a small lie to leave lying around in the one
file a stranger's install trusts.

The digest is deliberately NOT checked here. It is removed by the release pull
request and restored by a second one that computes it from the published assets,
which do not exist until the tag, so a test demanding it would fail for the whole
window in which it is correctly absent.
"""

import json
import re
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = {
    "bundles": ROOT / "catalogs" / "bundles.json",
    "extensions": ROOT / "catalogs" / "extensions.json",
    "presets": ROOT / "catalogs" / "presets.json",
}


def bundle_version() -> str:
    m = re.search(r'^\s+version:\s*"([^"]+)"', (ROOT / "bundle.yml").read_text(), re.M)
    assert m, "bundle.yml has no version"
    return m.group(1)


def entries(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    key = next(k for k in ("bundles", "extensions", "presets") if k in d)
    return d, list(d[key].items())


@pytest.mark.parametrize("name", sorted(CATALOGS))
def test_AC_GATE_210a_the_catalogs_name_the_release_they_claim(name):
    want = bundle_version()
    _, items = entries(CATALOGS[name])
    for entry_id, entry in items:
        assert entry["version"] == want, (
            f"{name}.json's {entry_id} says {entry['version']}, bundle.yml says {want}"
        )


@pytest.mark.parametrize("name", sorted(CATALOGS))
def test_every_download_url_points_at_that_version(name):
    want = bundle_version()
    _, items = entries(CATALOGS[name])
    for entry_id, entry in items:
        url = entry.get("download_url", "")
        assert f"/v{want}/" in url, (
            f"{name}.json's {entry_id} downloads from {url}, which is not v{want}"
        )
        assert want in url.rsplit("/", 1)[-1], (
            f"{name}.json's {entry_id} names a file that is not {want}: {url}"
        )


@pytest.mark.parametrize("name", sorted(CATALOGS))
def test_a_per_entry_updated_at_agrees_with_its_own_file(name):
    """The drift this test was written for. Not every entry carries one; the ones
    that do must not disagree with the file they sit in."""
    doc, items = entries(CATALOGS[name])
    top = doc["updated_at"]
    for entry_id, entry in items:
        if "updated_at" in entry:
            assert entry["updated_at"] == top, (
                f"{name}.json's {entry_id} was updated at {entry['updated_at']} "
                f"while the file says {top}"
            )


def test_the_three_catalogs_agree_on_when_they_were_updated():
    stamps = {name: json.loads(p.read_text())["updated_at"] for name, p in CATALOGS.items()}
    assert len(set(stamps.values())) == 1, (
        f"the three catalogs disagree about when they were updated: {stamps}"
    )


def test_the_update_stamp_is_not_in_the_future():
    """A catalog dated tomorrow is a copy-paste, not a release."""
    stamp = json.loads(CATALOGS["bundles"].read_text())["updated_at"]
    stamped = date.fromisoformat(stamp.split("T")[0])
    assert stamped <= date.today(), f"catalogs are dated {stamped}, which is in the future"


def test_AC_GATE_210b_the_catalog_repeats_the_bash_floor():
    """The catalog is the copy Spec Kit reads before anything is downloaded, so a
    floor that lives only in extension.yml is a floor an installer never sees.
    FR-GATE-200."""
    manifest = (ROOT / "extensions" / "specassay-check" / "extension.yml").read_text()
    floor = re.search(r'-\s*name:\s*"?bash"?.*?version:\s*"([^"]+)"', manifest, re.S)
    assert floor, "extension.yml declares no bash floor"
    _, items = entries(CATALOGS["extensions"])
    for entry_id, entry in items:
        tools = entry.get("requires", {}).get("tools", [])
        bash = [t for t in tools if t.get("name") == "bash"]
        assert bash, f"{entry_id} lists no bash in requires.tools"
        assert bash[0].get("version") == floor.group(1), (
            f"{entry_id} says bash {bash[0].get('version')}, extension.yml says "
            f"{floor.group(1)}"
        )
