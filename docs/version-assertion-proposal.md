# Proposal: make a stale version number impossible to ship <!-- specassay:stale-ok the record of one argument and the examples it was argued from; rewriting its numbers would rewrite the argument -->

Status: **ruled on and built, 2026-09-18.** Proposed 2026-09-17. Kept as written
below, with the outcome recorded here, because what the proposal got wrong is
more useful than what it got right.

**The ruling.** Assertion over generation, on the reason argued below. All three
rules, with the classification rule leading. The reason itself is now
`PROMOTION-CONTRACT.md` rule 11 and `PRD.md`'s `FR-DOCS-70`.

**What shipped.** `scripts/check-doc-versions.py`, `tests/test_doc_versions.py`,
wired into Self Gate at pull-request time and into the release workflow as a
refusal before anything is built. Ten documents are governed; the CHANGELOG and
the dated handoff archives are excluded with the reason written into the script.

**What the proposal got wrong, found by running it rather than reasoning about
it.** The three rules survived intact. The classification did not: it named
three classes and needed five.

| Added | Why |
| --- | --- |
| Pinned dependency | ONBOARD pins Spec Kit v1.0.4. Marking that a current claim made the checker demand it equal SpecAssay's own version. |
| Provenance | "Since v0.4.5 the Gate writes a manifest on refusal too" is a fact about history. It does not go stale, and it is the commonest idiom in the troubleshooting and migration pages. |

Four bugs in the checker itself surfaced the same way, each now a named
regression test: a sub-heading cleared the date its parent section had set, so a
correctly organised ledger failed 91 times; a section titled for the release it
describes was age-refused although its own title says how old it is; a mark
covered only its own line, so an author had to break their line wrapping to
satisfy the checker; and `stale-ok` exempted the age rule without satisfying the
classification rule, so a marked line was still refused as unclassified.

**The sweep.** 304 refusals on the first run, 0 at the end with two honest
warnings. Five were real defects rather than missing annotations. The sharpest:
a submission checklist row claiming the latest release was v0.4.13 while naming
`specassay-0.3.4.zip` as its artifact, two different stale numbers in one table
cell, carried for months and read past by everyone including me.

## Phase two, 2026-09-18: the whole corpus

Ruled the same day phase one merged: widen past the ten governed documents, as
its own change with its own sweep. Governed went from 10 documents to 54, which
is everything in the repository except `examples/**`, the fixture project whose
pages are specimen material for the tests rather than claims this repo makes.

The CHANGELOG came in, reversing phase one's own stated exclusion. That
exclusion was written while the checker refused the ledger 91 times, on the
argument that a dated ledger passes by construction and so adds nothing. Both
halves were wrong in the same direction: the 91 was a bug in the checker, not a
property of the ledger, and once fixed the CHANGELOG refused twice, both real.
A reason that only held while a bug held is not a reason. The archives came in
too, on a narrower argument: nobody acting on a version number in a closed
handoff is probably true, and is not the same as the number being allowed to sit
there unlabelled.

**Before the sweep: 47 refusals**, measured and reported first, as in phase one.
Nine in `specs/backlog/tasks.md`, six in this file, five each in
`RELEASE-HANDOFF.md` and the structure-emission handoff, the rest scattered.
Every one was a missing annotation on something correctly historical. Phase two
found no new lie, which is the honest result and a thinner one than phase one's.

**What the corpus forced, again.** Two things, and neither came from thinking
about the checker.

The first is a finding rather than a nuisance. The dig handoffs say
"generatorVersion bumps (0.3.0 to 0.4.0)". That is not a pin of somebody else's
tool, and it is not an observation of the bundle: it is a **second version line
living inside this repository**, versioning the dig report format on its own
schedule. The checker had assumed a repository has one version line and that
every other number in its prose is either an observation of that line or a
dependency's. Neither was true. The mechanism needed no change, which is exactly
what makes it worth writing down: what was wrong was the class's stated meaning,
"a deliberate pin of somebody else's version", which is the sentence the refusal
prints at an author. An author with their own second version line reads that and
concludes the class is not for them. The class is now "a version belonging to
another subject", and the subject is allowed to be ours. A checker that accepts
the right thing for a reason nobody can find is one document away from being
worked around.

**One discipline the sweep taught, worth writing down because the checker
cannot enforce it.** A heading-level mark scopes everything beneath it, so a
mark placed inside a scoped section does nothing at all, and a reader cannot
tell which of the two is carrying the weight. Both directions were in the first
pass of this sweep: `RELEASE-HANDOFF.md` had three provenance marks under a
title-level `stale-ok` that made them unreachable, and the two cold-agent trial
pages had a title-level `stale-ok` that was not needed, since the single pinned
Spec Kit line was doing the work. Both were fixed by the same rule: use the
narrowest annotation that suffices, and prove it is the narrowest by removing
the wider one and watching the check refuse. A mark that does nothing is a claim
nobody can test, which is the shape this tool exists to refuse.

The second is a fifth bug, the same shape as the fourth one level up: a heading
carrying `stale-ok` scoped its section out of the age rule but did not classify
it, so an author who had answered the question on the heading was still refused
for not answering it. Both are the checker ignoring the answer it asked for.

Phase one's count was five of six corrections found by pointing the checker at
real documents. Phase two adds two more, both from the same source and neither
from thinking harder about it. The ratio has not moved between phases, which is
the reason `PROMOTION-CONTRACT.md` rule 13 exists: a rule proposed from a desk
names three classes, a rule met by the corpus needs five.

---


## The failure being answered

Four instances of one thing, all patched by hand after the fact:

| Where | What it said | How long it was wrong |
| --- | --- | --- |
| `README.md`, install verification | "both report v0.4.13" | three releases |
| `README.md`, Spec Kit compatibility | verified versions, dated 2026-09-04 | three releases |
| `ONBOARD.md`, pin table | captured on v0.4.13 | two releases |
| `docs/submission/*`, paste-from digests | the previous release's digests | one release, each time |

Each was caught by a person noticing. That works and does not scale, and the
noticing has been getting later: the README line was three releases stale before
anyone read it cold.

## The ruling this asks for

Two candidate mechanisms were named. I argue for the second, for the reason given
plus one that is sharper, and then argue that as stated it catches less than it
looks like it does.

### Why not generate the receipts

Generating version strings and receipt blocks at release time removes the drift
completely. It also removes something worth more.

A generated number is a number nobody looked at. That is the stated objection and
it is correct. The sharper version is this: a generated receipt is
**unfalsifiable by its reader**. Someone reading a generated line cannot check it
against anything; they can only trust the generator. The claim and its
verification collapse into one act, performed by the machine, with no independent
party.

That shape has a name in this repository. It is a self-report, and refusing to
accept self-reports is the entire premise of the tool. Rule 6a exists because a
status a project declares about itself is worth less than a status derived from
evidence. Generated docs would make this repository's own documentation the one
kind of claim its product refuses to accept from anybody else.

So: the receipt stays human-written. The machine's job is not to write it. The
machine's job is to refuse it when it is false.

### What the assertion catches, and what it does not

The proposed rule is: fail the release when a version string quoted in the docs
does not match the tag being cut.

That rule would not have caught three of the four rows in the table above.

Look at what the README actually said: *"Verified 2026-09-04 in a clean project:
both report v0.4.13."* That sentence was **true**. It was true on the day it was
written and it was still true, as a statement about 2026-09-04, on the day it was
three releases stale. There is no lie in it for an assertion to catch. It carried
its own date, which is exactly what this repo's doctrine asks for.

What was wrong with it was not falsity. It was that a reader arriving at the repo
root read it as current guidance, because it was the only such sentence on the
page and nothing told them it was old. The failure is **staleness of relevance**,
and an equality check against the tag cannot see it.

The same is true of the ONBOARD pin table and the Spec Kit compatibility line.
Only the paste-from digests were ever going to be *false*, and those are already
handled by the convention of blanking them at the sweep.

This matters because a mechanism that appears to cover the class, and covers one
of four cases, is worse than no mechanism: it would have been trusted.

## The mechanism

Three rules, not one. The first is what makes the other two possible.

### Rule 1: no unclassified version number in prose

Every version-shaped token in a governed document is one of exactly two things,
and the author says which:

- **A current claim.** A sentence asserting something about the release being
  cut. Marked with a trailing `<!-- specassay:current -->` comment on the line.
- **A dated observation.** A record of what was seen. Must contain the shape
  `on vX.Y.Z, YYYY-MM-DD`, which is the convention the docs already use.

Anything else fails the check, naming the file, the line and the token. A bare
version number in a sentence is not a small sin here; it is the thing that rots,
because nobody can tell later whether it was meant as current or historical.

Tokens inside fenced code blocks are skipped. They are quoted output, which is
data, not a claim.

### Rule 2: a current claim must name the tag

Mechanical equality. This is the proposed rule, kept, and it now has a
well-defined set to operate on rather than every number on the page.

### Rule 3: a dated observation has an age, and the age is checked

The checker counts how many released tags sit between the observed version and
the tag being cut. Past a threshold, the release refuses, and the message says
which sentence and how old.

The threshold is a judgement, not a fact. My recommendation is **two releases,
warn at one**. That is the rule that would have caught the README line at v0.5.0
rather than v0.5.1, and it is loose enough that a genuinely historical note
survives by being re-observed or excused.

An excuse is written in the document, not in a config file, and looks like
`<!-- specassay:stale-ok reason -->`. A reader of the page sees the reason. The
cost of keeping an old number is that you have to say, in the page, why it is
still worth keeping. That is the same design as an open task carrying
`**Carries**`: debt is allowed, but only admitted debt.

### Where it runs

Both places, and the order matters:

- **Self Gate, at PR time.** This is where the failure should be seen. A doc
  check that only runs at the cut turns every release into a scramble.
- **The release workflow, before it builds.** The tag must not be able to produce
  assets while a governed document lies. This is the one that makes it a refusal
  rather than a suggestion.

## What it would cost

The first run will refuse on a good deal of existing prose, because most version
numbers in the repository are currently unclassified. That is a one-time sweep,
and it is most of the work. I would not describe this as a small change.

The checker also becomes a thing that can itself rot, and it is checking
documents, so it wants the same treatment as anything else here: a registry row,
a named test per rule, and fixtures that fail against the version before it.

## What it does not solve

Two things, stated so nobody assumes otherwise.

**Receipt blocks.** The quoted output under each ONBOARD block is not a version
string. No assertion can tell whether `Ran 1 test in 0.000s` is this release's
output or the last one's. Re-capturing receipts stays a human sitting, and the
honest mitigation remains what the page does now: state the release and date the
capture was taken on, so a reader can judge.

**The site pin.** It lives in another repository. This mechanism cannot reach it,
which is worth saying plainly given that pin is currently two releases stale and
was missed by two consecutive sweeps.

## The recommendation

Build rules 1 and 2 together, and rule 3 with the threshold at two releases. Wire
it into Self Gate first, sweep the existing prose until it passes, then add it to
the release workflow as a refusal.

If only part of this is wanted, rule 1 alone is worth more than rules 2 and 3
without it. Forcing every number to declare whether it is a claim or a record is
the change that alters how the docs get written; the other two are enforcement on
top of that distinction.
