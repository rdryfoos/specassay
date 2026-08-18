# SpecAssay backlog

Product-level open questions and the proposed build order, minted so they don't
evaporate. Three kinds of entry: **hypotheses** we want to put to the test, **open
decisions** we've named but not settled, and the **roadmap** of proposed work.

## H1: Does SpecAssay only work in a greenfield environment?

**Status:** anointed backlog (minted, carried by this note, not yet tested).

**Hypothesis to falsify:** SpecAssay only makes sense when a project starts fresh: durable IDs from day one, no legacy sea, Spec Kit already in hand.

**Why we suspect it's *false* (codebase axis):** the gate governs only
*declared* intent; it never enumerates all code, so un-marked legacy is invisible
to it. That is the same "blind spot" that lets un-marked vibe-code slip past, and
it is precisely what makes brownfield adoption tractable. You **govern the
margin**: mint IDs for new intent, mark that slice, and the gate checks only that
thread. The registry *is* the scope boundary: start it empty, grow it one intent
at a time. `tracked-debt` and `anointed backlog` are the on-ramp for legacy
behavior you can't prove yet: admit it, don't refuse the whole repo.

**Where it might actually bite (org axis):** "greenfield *business* environment"
is the harder read. An established org with entrenched Jira / RTM / compliance
tooling and no Spec Kit is a bigger adoption gap than any legacy codebase.
Process inertia and politics, not the technique, are the real risk. HomesFlow was
greenfield on *both* axes, so the incremental-brownfield story is untested.

**How we'd test it:** adopt SpecAssay on a real brownfield repo for *new work
only*: empty/small registry, mark just the new statements of intent, leave the legacy
un-gated, and see whether the thread grows cleanly at the margin without a
retrofit, and whether a team actually tolerates the ceremony mid-stream.

## Open decision: a replacement for `FR`

**Status:** named, not settled. The `FR` type code expands to "Functional
Requirement," which fights the intent framing now that "requirement" is retired.
`NFR` stays (entrenched acronym), which makes `FR` the lone holdout.

**Candidates:**

- **`FI` = Functional Intent**: on-message, but asymmetric beside a kept `NFR`
  (intent vs requirement).
- **`FUNC` = Functional**: neutral; carries neither "requirement" nor "intent",
  so it sidesteps the asymmetry, at the cost of a longer prefix.
- **Zero-cost fallback**: keep both `FR` / `NFR` as opaque type codes and stop
  expanding them in prose.

**Cost of doing it:** migrating `FR` is a full tombstone-and-remint of every `FR`
ID (immutability forbids in-place renumbering). Not worth it as a standalone
change; fold it into the next time the registry churns for another reason.

## Feature request: coverage matrix + portfolio-snapshot emission

**Status:** anointed backlog (minted, carried by this note, not yet built).

**From:** HomesFlow — the family's oldest user, running the longest, on a real
brownfield-adjacent codebase (see H1 above).

**The ask:** two engine capabilities the vendored `specassay-check` doesn't have
yet, both of which HomesFlow's own bespoke `scripts/check-traceability.sh`
already does for itself: `--matrix` (regenerate a human-readable coverage table
+ SVG summary bar from the current registry/gate state) and a portfolio
snapshot mode (the same, framed for a cold reader rather than CI). Neither is
exotic; both are re-renderings of data the gate already computes.

**Why this matters beyond one repo:** HomesFlow forked its own gate tooling
before `specassay-check`'s lineage existed, and the fork earned real,
documented, relied-upon modes (`--matrix`, `--canvas`, `--refresh`) that the
2026-08-18 migration deliberately did not touch — grafting Rule 6a onto the
bespoke script rather than forcing a premature full-engine swap, precisely so
none of that got silently dropped. The full swap has a named trigger: **when
SpecAssay ships matrix/portfolio-snapshot emission, the bespoke script
retires.** Until then, HomesFlow runs two enforcement paths in parallel by
design, not by accident.

**Evidence for urgency, not just want:** wiring the vendored engine's Rule 6a
graft into the bespoke script the same night surfaced a real bug born of
exactly this divergence — the bespoke script's task-tracking check had a
hardcoded single-file path (`specs/001-mvp/tasks.md`) where the vendored
engine already used a proper recursive glob (`specs/**/tasks.md`), so three
IDs honestly tracked in `specs/backlog/tasks.md` read as a false gap under the
bespoke script and correctly as `backlog` under the vendored one. Two engines
covering the same registry drifted apart on a basic correctness question
within one migration session. That is the cost of the fork continuing to
exist; the sooner these modes ship, the sooner it stops accruing.

## Pattern candidate: "retired" as a first-class terminal state

**Status:** observed once, not yet a rule. No ID minted for this; recording
the pattern before it's forgotten, not proposing a build.

**From:** HomesFlow — the family's first intent retirement (US/FR/AC-CLEW-01,
the Clewseau cold-agent trial slice, 2026-08-18).

**What happened:** the trial concluded without ever getting a real carrier —
no `@covers`, no passing test — because the thing it was probing (that a
stock Spec Kit + Clewseau agent could take one AC end-to-end) was answered by
running the trial itself, not by shipping `HomeDisplayName.normalized(_:)`.
Closing the single task that had been carrying the three IDs as tracked-debt
(`T900`) immediately flipped `AC-CLEW-01` to `GAP` under both the vendored
engine and HomesFlow's own bespoke script — independently, same root cause.
Gate 2's AC status logic treats a closed task with no proof as silent gap by
design, because normally closing a task *means* the thing got built. It has
no vocabulary for "closed on purpose, deliberately never built."

**The improvised fix, by hand (revised once, same day):** first attempt
suffixed the registry statement with a `[TOMBSTONED <date>: ...]` note and
closed the carrying task — which immediately proved the point by flipping
`AC-CLEW-01` to `GAP` under both engines. Closing the task was the error, not
the tombstone note: a closed task with no proof reads as gap by design.
Corrected shape, still hand-improvised: the tombstone suffix stays, the
carrying task (`T900`) stays *open*, and its text is rewritten to say plainly
that it's a retirement carrier, not undone work — it closes only when this
feature ships. Both engines read `backlog`/tracked-debt for all three IDs as
of this correction, honestly: the pending work (finishing the retirement once
`retired` exists) is real, so `backlog` is the true status today, not a
disguise for `GAP`.

**The shape of the fix, if it becomes one:** a `retired` status alongside
`proven`/`tracked-debt`/`backlog`/`GAP` — an AC (or US/FR/NFR) whose registry
statement carries a tombstone annotation is `retired`, not `GAP`, regardless
of proof state, closed rather than open. Same append-only ethos as everything
else here: retirement doesn't remove the ID or its history, it names a
terminal state the gate can recognize instead of misreading as decay.

**The requirement, stated precisely:** `retired` must be a terminal state
both engines distinguish from `GAP`, triggered by an explicit retirement
marker on a closed carrying task. Closed-with-no-proof means `GAP` *only in
the absence of that marker* — the marker is what separates a violated promise
from a withdrawn one. `GAP` stays reserved for violated promises; withdrawn
is not violated, and 2026-08-18 proved the gate can't yet tell them apart —
that inability to distinguish is itself the requirement. `T900` is the named
first customer: the feature ships when it can close this exact task.

## Roadmap: proposed build order

Lifted from `scope-and-pull-requests.md` §6. Every item there is tagged
**(proposed)**; this is the order to build them in. Converging strategies, not one
silver bullet:

1. **Manifest diff + Thread Report** (scope note §4): ✅ **shipped.** The
   base↔head diff, changed-file bucketing, and the sticky PR briefing all exist:
   see [`thread-report.md`](thread-report.md) and live
   [PR #1](https://github.com/rdryfoos/specassay/pull/1). (Still open: a Loupe
   "PR view" that renders the same diff visually.)
2. **Intent-diff legibility** (§5): surfacing ✅ **shipped** as the Thread
   Report's *What moved* + *Intent Changed* (see
   [`thread-report.md`](thread-report.md)); the **immutability gate** on the same
   diff remains proposed; small.
3. **Full intent-PR workflow** (§5): the destination.

None of it asks the developer to tag more code. The value comes from *reading the
diff against the thread you already have* and *handing author and reviewer a
briefing instead of a checkmark.*
