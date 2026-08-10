# Scope, the pull request, and intent PRs

> **Status: design note.** Every claim below is tagged **(shipped)** — true of
> the gate as it stands today — or **(proposed)** — intended direction, not yet
> built. SpecAssay does not describe unbuilt behavior as real; neither does this
> file.

SpecAssay hallmarks the Golden Thread from intent to build to proof. This note is
about the *edge* of that guarantee: what a passing Gate does and does not
promise, why the pull request is the backstop for the rest, and how the same
durable IDs that make the forward thread possible can carry pull requests that
change the intents themselves.

## 1. Completeness, not minimality (shipped)

Gate 2 walks in one direction only: **intent → build → proof**. It reads the
registry, the specs, and the tasks; it opens source files *only* to pull out
`@covers` marks and test names. Everything it refuses is a hole in *declared*
intent:

- **exact-set drift** — registry ≢ specs, or registry ≢ tasks
- **missing `Carries:`** — a task that names no ID
- **silent AC gap** — a registry AC with neither a test nor an open `Carries:` TODO
- **untraced scope** — an `@covers` or test whose ID **is not in the registry**

Read that last one carefully, because its name misleads: *"untraced scope"*
fires when code claims a **fake** ID, never when code claims **no** ID. The gate
never enumerates the source tree and asks "does this file correspond to an
intent?" There is no **build → intent** direction.

The consequence is a precise scope line:

> A passing Gate proves **completeness of declared intent** — every intent you
> wrote down is built and proven, with nothing *hidden* at AC altitude. It does
> **not** prove **minimality** — that nothing was built *beyond* what was
> intended.

This is by design, not oversight. You do **not** paste an ID onto every line of
code (see the field guide) — most legitimate code is unmarked, so the gate
*cannot* treat unmarked code as suspicious. An honest developer who takes a
side-track and writes something nobody asked for — unmarked — is invisible to
the Gate; the build stays green and the Thread reads intact. Two further limits
sharpen the point:

- **Attribution is not authentication** (Promotion Contract, rule 9). `@covers`
  is author-written; the Gate trusts the mark, it never validates the code
  behind it.
- **`proven` is a traceability claim, not a quality claim.** It means a test
  *names* the AC — not that the code is correct or that the test asserts
  anything. An empty `test_AC_…()` still reads `proven`.

Even the "bidirectional" language in the constitution is bidirectional over
**IDs** (no gaps forward, no invented IDs backward), not over **code**.

## 2. The backstop is the pull request (shipped)

Catching *undeclared* work is not the Gate's job; it is the job of the human
layer SpecAssay sits beside — the **pull request** and **Gate 1 judgment**
(`/speckit.analyze`). SpecAssay is explicit that it is not a replacement for
Spec Kit and not the judgment layer.

This backstop is **necessary but not sufficient**, and it is weakest in exactly
the conditions SpecAssay exists for:

- **Volume is the enemy of review.** The side-track problem is worst when a lot
  of code arrives fast — the same velocity that makes reviewers skim.
- **Green can lower vigilance.** A single "Gate green · Thread intact" signal
  borrows credibility for *everything* in the diff, including the parts the Gate
  never looked at. Automation bias means the tool can inadvertently provide
  cover for the one thing it cannot see.

The design response is **not** to add a refusal. It is to make the review
*legible*: decompose the single green check into named claims, and hand the
reviewer a spotlight on what traces to nothing. The rest of this note is *how* —
organized around a single ladder, three rungs of it.

## 3. The three-rung ladder

Everything that follows stands on a single ladder — three postures the machine can take,
in **increasing intervention and decreasing frequency**:

- **Illuminate** — surface it; render no verdict, force no action. The default,
  always on.
- **Affirm** — require a human to look and attest; block until they do. Opt-in.
- **Refuse** — the machine's own verdict; block on a **provable** defect. Only
  when the defect is machine-decidable.

The governing rule is an asymmetry: **burden of proof rises with intervention.**
Visibility carries no verdict, so it needs no proof — the machine may surface
anything decision-relevant. Refusal carries the machine's verdict, so it needs
full proof. Affirmation carries no machine verdict at all — it defers to a
person. That is what lets the machine be maximally *helpful* in exactly the zone
where it is forbidden to be *authoritative*: where it cannot judge, it
illuminates.

> **Make the truth visible; refuse only what you can prove; for the rest, make a
> human look.**

The rest of this note is that ladder applied: **illuminate** is the briefing
(§4), **affirm** is the off-thread acknowledgment (§4b), **refuse** is the two
cheap gates (§6). And §7 shows why, in steady state, almost all the value lives
on the *illuminate* rung.

### 3a. Colors are states, not postures

The ladder is about the machine's *posture*; the Loupe palette is about the
work's *state*. Two different axes:

- **Palette (states):** green = proven · blue = not-yet · amber = owed · red =
  broken. Answers *"what condition is this thread in?"*
- **Ladder (postures):** illuminate · affirm · refuse. Answers *"what may the
  machine do about it?"*

They coincide at exactly one point — **refuse = red** (a Gate refusal and a
broken thread are the same event: Gate fail ⇔ fray). Elsewhere they must not be
conflated: green stays **proven**; illuminate has no color of its own (it is the
lens the colors are seen *through*); affirm gets its own affordance — a
chip/checkbox — not a node color.

## 4. The pull request as a briefing — the *illuminate* rung (shipped)

> The mechanism below now ships as the **Thread Report** — tool, CI workflow,
> and a live [PR #1](https://github.com/rdryfoos/specassay/pull/1). This section
> is the argument; [`thread-report.md`](thread-report.md) is the reference.


Threat model: the **honest** developer who side-tracks, not the adversary who
mislabels. For honest developers the goal is not to *refuse* — it is to make the
discrepancy cheap to see and cheap to reconcile. Two reframes make this
low-friction (often friction-*negative*):

1. **Illuminate, don't refuse.** Compute and surface; never gate on undeclared
   code (that would false-positive on every legitimate refactor).
2. **Diff, not repo.** Ask the bidirectional question of the **PR diff**, not
   the whole tree. The diff is small, it is already the review unit, and it is
   the one altitude where build → intent is affordable.

### 4a. The manifest diff (shipped)

Gate 2 already emits a trace-manifest per commit, so CI has two: **base** and
**PR head**. Diff them, and diff the code, and bucket every changed file:

- **on-thread** — gained/holds an `@covers`, is a test naming an AC, or is a
  registry / spec / task edit
- **off-thread** — changed, but nothing in or near it touches any intent in
  this PR

The off-thread bucket is where a side-track hides — now a short, named list,
computed for free, requiring no new marks. **Ceiling, stated honestly:** this
cannot tell a legitimate refactor from unwanted scope; both land off-thread.
What it does is collapse the reviewer's search space from *the whole diff* to
*the untraced subset*, and label it. For an honest team that is the whole game.

### 4b. The Thread Report (shipped)

On every PR, SpecAssay posts a generated briefing — friction-negative, because
the developer receives more than they give:

- **what moved** — statuses that changed (backlog → proven, proofs added, IDs
  minted or retired): the manifest diff in prose
- **story-scoped view** — "this PR advances US-X; here is its thread now, end to
  end"
- **the off-thread signal** — two parts, deliberately split by a lightweight
  config control so a team chooses its own rung:
  - `offthread_list: always` — the *information*: the named list of changed
    files that touch no intent. Every report, not a toggle. (Pure **illuminate**.)
  - `offthread_ack: off | record | required` — the *ceremony*: default **off**;
    `record` shows a one-click *"these untraced changes are incidental"* tick and
    logs it; `required` blocks the merge until a human ticks it. That `required`
    mode is the **affirm** rung — a human-affirmation gate, not a machine verdict.
- **intent changes** — see §5

This is the direct counter to the automation-bias trap: not one green check, but
the green decomposed into legible claims, including an explicit "here is what
traces to nothing."

## 5. Pull requests that change intents (surfacing shipped; enforcement proposed)

The reason SpecAssay is *unusually* suited to this: mint-at-intent, immutable
IDs, and registry-as-source-of-truth already made intents **first-class
version-controlled artifacts with stable identity.** An intent is diffable,
reviewable, and mergeable — keyed by an ID that survives the change. Most shops
cannot meaningfully PR an intent because their intents live in a ticket
tracker with no durable identity; here they live in git.

What SpecAssay can add on top:

- **Legible intent diffs.** A PR touching the registry shows IDs *added*
  (minted), *retired* (tombstoned), *restated* (wording changed). This surfacing
  **ships** in the Thread Report (*What moved* plus *Intent Changed*). The
  immutability **gate** is the proposed part: renumber or reuse an ID → fail —
  cheap, rare, high-value. It almost never fires, so it costs no friction.

- **Blast-radius on intent change** — the integrity property from the
  *Bidirectional Traceability* field note, made mechanical. When an AC's
  statement changes, its build and proof (the `@covers` code and the `test_AC_…`
  proof) were written against the *old* wording. SpecAssay lists them and marks
  them **"re-confirm — the intent moved under the proof."** This surfacing
  **ships** today as the Thread Report's *Intent Changed* section
  ([`thread-report.md`](thread-report.md)); *enforcing* the re-confirm is the
  proposed part. The PR that changes the intent carries its own list of what it
  may have invalidated.

- **Two honest shapes of intent-PR:**
  - **Intent-only PR** (intent changes, no code): the changed ID rides as
    `backlog` — minted, no carrier yet. The Gate stays green *and honest*:
    "intent moved; here is the new open thread." A later code PR closes it; the
    durable ID stitches the two across time.
  - **Discovery PR** (mid-build, the spec was found wrong): changes the
    intent *and* the code together, reviewed as one, the thread showing both
    moved in lockstep. SpecAssay's job is coherence — no orphaned proofs, no ACs
    pointing at deleted code, immutability intact.

## 6. Friction stance — the *refuse* rung (proposed)

A bolt-alongside **gate** on undeclared code is both high-friction and wrong for
honest developers, so we hold a hard line: **the machine may only refuse what it
can prove is a defect.** "Off-thread" is not machine-decidable as a defect (a
refactor and a rogue feature look identical), so it never earns a machine
refusal — only illumination (§4) or, at a team's option, human affirmation (§4b).
A noisy false gate would be worse than useless: people learn to override it
reflexively, and that reflex leaks onto the gates that *are* meaningful.

Everything above is assistive except two gates that *are* cheap, rare, and
machine-decidable:

- **immutability** — never renumber, never reuse
- **coherence after an intent change** — no orphaned proofs

The build order for everything still tagged **(proposed)** above — the
immutability gate, then blast-radius *enforcement*, then the full intent-PR
workflow (the manifest diff and restatement surfacing already shipped) —
lives in [`docs/backlog.md`](./backlog.md) under *Roadmap*. None of it asks the
developer to tag more code: the value comes from *reading the diff against the
thread you already have* and *handing author and reviewer a briefing instead of a
checkmark.*

## 7. What a refusal actually means (shipped)

Gate 2 refuses on **bookkeeping** breakdowns — drift, missing `Carries:`, a
silent AC gap, an invented ID — never on whether the code is *good*. A working
feature with a forgotten test refuses; a broken feature with a present-but-wrong
test passes. The Gate does not measure whether the system works; it measures
whether the thread's paperwork is intact.

In steady state that means a healthy traced repo **sits green** — which is the
design working, not idling. (Breaks have to be *synthesized* for demos for
exactly that reason.) Genuine refusals cluster at two moments:

- **In-flight, pre-merge** — frequent and healthy: you wrote an AC but haven't
  written its test yet, so it's a silent gap until you test it or admit the debt.
  The refusal is the ordinary "finish the thread or admit it before you ship"
  nudge.
- **Rarely, on a mature repo** — a refactor / rename / merge silently severs an
  existing link. Uncommon, and the high-value catch.

So the everyday value is not the refusal — it is the **manifest emitted on every
run** (pure illumination, §3) plus the deterrence of a gate that *could* refuse.
Judge the Gate by how often it refuses and you are judging a smoke detector by
how often it alarms.

## Vocabulary (applied)

The consolidated vocabulary — Intent → Build → Proof, status `proven`, the
retired terms, the metaphor lanes, and the ID grammar — is locked and propagated
across the schema, gate, Loupe UI, samples, and docs. It lives as the source of
truth in [`presets/specassay/GLOSSARY.md`](../presets/specassay/GLOSSARY.md); the
one open item, a replacement for `FR`, is tracked in
[`docs/backlog.md`](./backlog.md).
