#!/usr/bin/env python3
"""Refuse a document that states a version number without saying what kind of
claim it is making.

Built 2026-09-18 on a ruling, answering four instances of one failure: a version
observed once, typed into a sentence, and then left to rot while the thing it
described moved on. Each was caught by a person noticing, later each time.

The mechanism is deliberately not a generator. A generated receipt is
unfalsifiable by its reader: they cannot check it against anything, they can only
trust the generator, which makes the documentation a self-report. Refusing to
accept self-reports is the premise of this whole tool, so the receipt stays
human-written and the machine's job is to refuse it when it lies.

Three rules. The first is what makes the other two possible.

  1. No unclassified version number in prose. Every version token is a CURRENT
     CLAIM, a DATED OBSERVATION, a DECLARED RANGE, or a PINNED DEPENDENCY, and
     the author says which. A bare number is refused, because nobody can tell
     later whether it was meant as current or historical, and that ambiguity is
     what rots.

     The fourth class was not in the proposal. It was forced by running the
     check against real pages: ONBOARD pins Spec Kit v1.0.4, which is a claim
     about somebody else's version, and the only classes on offer made the
     checker demand it equal SpecAssay's own. Three of the bugs in this file
     were found the same way, by pointing it at documents rather than reasoning
     about it.

  2. A current claim names the version being cut. Mechanical equality.

  3. A dated observation has an age, counted in releases between what it records
     and what is being cut. Past the threshold it is refused, and the way to keep
     it is to write the reason in the page where a reader sees it.

Rule 3 is the one the original proposal lacked. The README line that started all
this said "Verified 2026-09-04 in a clean project: both report v0.4.13". That
sentence was true, stayed true, and carried its own date. An equality check finds
no lie in it. What was wrong was staleness of relevance, not falsity, and only an
age rule sees that.

Zero dependencies. Exits 0 when clean, 1 on any refusal.
"""
# @covers FR-DOCS-70, AC-DOCS-20 -- the three rules and their classifications.

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# A version token, as prose writes one: three dot-separated numbers, optionally
# prefixed with v. Two-part versions ("Python 3.8") are deliberately out of
# scope; they are nearly always a floor, not an observation.
VERSION = re.compile(r"\bv?(\d+\.\d+\.\d+)\b")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
HEADING = re.compile(r"^(#{1,6})\s")
FENCE = re.compile(r"^\s*(```|~~~)")

CURRENT_MARK = "<!-- specassay:current -->"
STALE_OK = re.compile(r"<!--\s*specassay:stale-ok\s+(.+?)\s*-->")

# A deliberate pin of somebody else's version: Spec Kit, Python, uv. It is
# neither an observation nor a claim about what this repo is cutting, so
# equality and age both mean nothing for it. The class exists because real
# pages forced it: ONBOARD pins Spec Kit v1.0.4, and marking that "current"
# made the checker demand it equal SpecAssay's own version.
PINNED = re.compile(r"<!--\s*specassay:pinned\s+(.+?)\s*-->")

# A version naming WHEN something changed: "since v0.4.5 the Gate writes a
# manifest on refusal too", "taught by the repair in v0.4.9". Provenance does
# not go stale, because it is a fact about history rather than a report of the
# present. This is the commonest idiom in the troubleshooting and migration
# pages, and the fifth class this checker grew: the proposal named three, and
# every addition after that came from pointing it at a real document rather
# than from thinking harder about it.
PROVENANCE = re.compile(r"<!--\s*specassay:provenance\s*-->")

# A token sitting inside a range expression is a declared constraint, not a
# claim about what was observed. `>=0.14.0,<2.0.0` says what the manifests
# accept; it is checked against the manifests instead of against the tag.
RANGE_NEAR = re.compile(r"(>=|<=|==|~=|\^|>|<)\s*v?\d+\.\d+\.\d+")

# How many releases a dated observation may fall behind the version being cut
# before the check refuses it. Two is a judgement, not a fact: it is loose
# enough that a note written one release ago survives untouched, and tight
# enough that nothing reaches a cold reader three releases stale, which is what
# happened to the README.
MAX_AGE_WARN = 2
MAX_AGE_REFUSE = 3


# The documents that make a live claim to a reader. A version number here is
# something somebody will act on, which is why they are governed first.
GOVERNED = [
    "README.md",            # the repo root, where a cold installer lands
    "ONBOARD.md",           # the quickstart, read start to finish by strangers
    "docs/troubleshooting.md",
    "docs/migration.md",
    "docs/submission/README.md",
    "docs/submission/CHEATSHEET.md",
    "docs/submission/test-evidence.md",
    "docs/submission/bundle-submission.md",
    "docs/submission/extension-submission.md",
    "docs/submission/preset-submission.md",
]

# Not governed, and each for a reason rather than because it was noisy.
#
#   CHANGELOG.md          A ledger. Every released section is dated by its own
#                         heading, so the released part passes by construction
#                         and adds nothing. The Unreleased section is undated by
#                         definition, and governing it would fail every pull
#                         request between two cuts for saying "since 0.4.12".
#
#   docs/*-handoff-*.md   Dated records of work already done. They are archives:
#   docs/testing/*        nobody acts on a version number in them, and rewriting
#   docs/*-brief-*.md     history to satisfy a checker is the opposite of the
#                         point.
#
# Widening this list is one line. It was kept narrow on purpose for the first
# cut, so the convention is established on the pages that matter before it is
# imposed on the ones that do not.


def governed_files(root: Path) -> list[Path]:
    return [root / name for name in GOVERNED if (root / name).is_file()]


def released_versions(root: Path) -> list[str]:
    """Release order, read from the CHANGELOG's own headings, newest first.

    Deliberately not `git tag`: the check has to run at pull-request time in a
    shallow checkout with no tags fetched, and the CHANGELOG is this repo's own
    ordered ledger of what shipped.
    """
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    seen, out = set(), []
    for m in re.finditer(r"^##\s+v?(\d+\.\d+\.\d+)", text, re.M):
        v = m.group(1)
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def age_in_releases(observed: str, current: str, order: list[str]) -> int | None:
    """How many releases sit between an observed version and the one being cut.

    None when either version is not a release this repo has recorded, which is
    not a refusal: a note about some other project's version has no age here.
    """
    if observed not in order or current not in order:
        return None
    return order.index(observed) - order.index(current)


def scan(path: Path, current: str, order: list[str], root: Path):
    """Yield (severity, line_no, token, message) for one file."""
    lines = path.read_text(encoding="utf-8").splitlines()

    # A mark covers the block it sits in, not just its own line. Prose wraps,
    # and a list item or paragraph carrying a version in its first line and the
    # mark in its last is one claim, not two. Requiring the mark on the exact
    # line meant an author had to break their own line wrapping to satisfy the
    # checker, which is the checker serving itself.
    block_marks: dict = {}
    start = 0
    for idx in range(len(lines) + 1):
        if idx == len(lines) or not lines[idx].strip():
            block = "\n".join(lines[start:idx])
            for n in range(start, idx):
                block_marks[n + 1] = block
            start = idx + 1

    in_fence = False
    # A date on a heading classifies everything under it, and a sub-heading does
    # not clear its parent's date. Getting this wrong was the first bug in this
    # checker: `### Some detail` under `## 0.5.1 (2026-09-17)` was reading as
    # undated, so a correctly-organised ledger failed 91 times. Dates are held
    # per heading level, and a heading clears only levels at or below its own.
    dated_at_level: dict = {}
    scoped_at_level: dict = {}

    for i, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            # Quoted output is data, not a claim. Nobody is asserting it is
            # current; it is a record of what a command printed.
            continue
        h = HEADING.match(line)
        if h:
            level = len(h.group(0).strip())
            for deeper in [k for k in dated_at_level if k >= level]:
                del dated_at_level[deeper]
            for deeper in [k for k in scoped_at_level if k >= level]:
                del scoped_at_level[deeper]
            if DATE.search(line):
                dated_at_level[level] = True
            if VERSION.search(line) or STALE_OK.search(line):
                # A heading that names a version declares the section's subject.
                # Everything under "## v0.4.13 cut, 2026-09-04" is about v0.4.13,
                # and asking how old it is answers itself. Age-refusing a
                # correctly labelled historical section was the second bug here.
                #
                # A heading may also carry stale-ok, which scopes a section that
                # is closed history spanning several versions. One mechanism,
                # three carriers: a date, a version name, or a stated reason.
                scoped_at_level[level] = True
        heading_has_date = bool(dated_at_level)
        version_scoped = bool(scoped_at_level)

        for m in VERSION.finditer(line):
            token = m.group(1)
            span = line[max(0, m.start() - 12):m.end() + 12]
            if RANGE_NEAR.search(span):
                continue  # a declared range, checked separately

            block = block_marks.get(i, line)

            if PINNED.search(block) or PROVENANCE.search(block):
                continue

            # An author who says "this old number stays, and here is why" has
            # classified it. stale-ok satisfies rule 1 as well as rule 3;
            # treating it as an age-only escape left a marked line still
            # refused as unclassified, which read as the checker ignoring the
            # answer it had asked for.
            if STALE_OK.search(block):
                continue

            if CURRENT_MARK in block:
                if token != current:
                    yield ("REFUSE", i, token,
                           f"current claim says {token}, but the version being "
                           f"cut is {current}")
                continue

            if DATE.search(block) or heading_has_date:
                if version_scoped:
                    continue  # a section about that version; its age is its title
                age = age_in_releases(token, current, order)
                if age is None or age <= 0:
                    continue
                if age >= MAX_AGE_REFUSE:
                    yield ("REFUSE", i, token,
                           f"dated observation is {age} releases behind {current}. "
                           f"Re-observe it, or write the reason for keeping it "
                           f"into the page: <!-- specassay:stale-ok why -->")
                elif age >= MAX_AGE_WARN:
                    yield ("WARN", i, token,
                           f"dated observation is {age} releases behind {current}")
                continue

            yield ("REFUSE", i, token,
                   "unclassified version number. Say which kind of claim this "
                   f"is: {CURRENT_MARK} if it describes the release being cut, "
                   "<!-- specassay:provenance --> if it names when something "
                   "changed, <!-- specassay:pinned NAME --> if it is a "
                   "deliberate pin of somebody else's version, or give the "
                   "sentence the date it was observed on")


def check_declared_range(root: Path) -> list[str]:
    """The range a document quotes must be the range the bundle declares."""
    bundle = (root / "bundle.yml").read_text(encoding="utf-8")
    m = re.search(r"speckit_version:\s*\"([^\"]+)\"", bundle)
    if not m:
        return ["bundle.yml declares no requires.speckit_version"]
    declared = m.group(1)
    problems = []
    for path in governed_files(root):
        dated_at_level: dict = {}
        in_fence = False
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            h = HEADING.match(line)
            if h:
                level = len(h.group(0).strip())
                for deeper in [k for k in dated_at_level if k >= level]:
                    del dated_at_level[deeper]
                if DATE.search(line):
                    dated_at_level[level] = True
            if DATE.search(line) or dated_at_level:
                # A range quoted in a dated section records what was declared
                # then, not what is declared now. The CHANGELOG's own account of
                # widening the range is the obvious case.
                continue
            for quoted in re.findall(r"`(>=[^`]+)`", line):
                if quoted != declared:
                    problems.append(
                        f"{path.relative_to(root)}:{i}: quotes the range "
                        f"`{quoted}`, but bundle.yml declares `{declared}`")
    return problems


def bundle_version(root: Path) -> str:
    text = (root / "bundle.yml").read_text(encoding="utf-8")
    m = re.search(r"^\s+version:\s*\"([^\"]+)\"", text, re.M)
    if not m:
        raise SystemExit("bundle.yml has no version")
    return m.group(1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", default=None,
                    help="the version being cut; defaults to bundle.yml's")
    ap.add_argument("--root", default=".", help="repository root")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    current = (args.version or bundle_version(root)).lstrip("v")
    order = released_versions(root)

    refusals, warnings = [], []
    for path in governed_files(root):
        for severity, line_no, token, message in scan(path, current, order, root):
            entry = f"{path.relative_to(root)}:{line_no}: {token}: {message}"
            (refusals if severity == "REFUSE" else warnings).append(entry)

    refusals += check_declared_range(root)

    for w in warnings:
        print(f"WARN: {w}")
    for r in refusals:
        print(f"FAIL: {r}", file=sys.stderr)

    if refusals:
        print(f"\ndoc-versions: REFUSED ({len(refusals)} problems, "
              f"version being cut: {current})", file=sys.stderr)
        return 1
    print(f"doc-versions: OK (version being cut: {current}, "
          f"{len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
