# SpecAssay backlog

Product-level open questions and the proposed build order, minted so they don't
evaporate. Three kinds of entry: **hypotheses** we want to put to the test, **open
decisions** we've named but not settled, and the **roadmap** of proposed work.

## H1 — Does SpecAssay only work in a greenfield environment?

**Status:** anointed backlog (minted, carried by this note, not yet tested).

**Hypothesis to falsify:** SpecAssay only makes sense when a project starts fresh — durable IDs from day one, no legacy sea, Spec Kit already in hand.

**Why we suspect it's *false* (codebase axis):** the gate governs only
*declared* intent; it never enumerates all code, so un-marked legacy is invisible
to it. That is the same "blind spot" that lets un-marked vibe-code slip past — and
it is precisely what makes brownfield adoption tractable. You **govern the
margin**: mint IDs for new intent, mark that slice, and the gate checks only that
thread. The registry *is* the scope boundary — start it empty, grow it one intent
at a time. `tracked-debt` and `anointed backlog` are the on-ramp for legacy
behavior you can't prove yet: admit it, don't refuse the whole repo.

**Where it might actually bite (org axis):** "greenfield *business* environment"
is the harder read. An established org with entrenched Jira / RTM / compliance
tooling and no Spec Kit is a bigger adoption gap than any legacy codebase.
Process inertia and politics, not the technique, are the real risk. HomesFlow was
greenfield on *both* axes, so the incremental-brownfield story is untested.

**How we'd test it:** adopt SpecAssay on a real brownfield repo for *new work
only* — empty/small registry, mark just the new intents, leave the legacy
un-gated — and see whether the thread grows cleanly at the margin without a
retrofit, and whether a team actually tolerates the ceremony mid-stream.

## Open decision — a replacement for `FR`

**Status:** named, not settled. The `FR` type code expands to "Functional
Requirement," which fights the intent framing now that "requirement" is retired.
`NFR` stays (entrenched acronym), which makes `FR` the lone holdout.

**Candidates:**

- **`FI` = Functional Intent** — on-message, but asymmetric beside a kept `NFR`
  (intent vs requirement).
- **`FUNC` = Functional** — neutral; carries neither "requirement" nor "intent",
  so it sidesteps the asymmetry, at the cost of a longer prefix.
- **Zero-cost fallback** — keep both `FR` / `NFR` as opaque type codes and stop
  expanding them in prose.

**Cost of doing it:** migrating `FR` is a full tombstone-and-remint of every `FR`
ID (immutability forbids in-place renumbering). Not worth it as a standalone
change — fold it into the next time the registry churns for another reason.

## Roadmap — proposed build order

Lifted from `scope-and-pull-requests.md` §6. Every item there is tagged
**(proposed)**; this is the order to build them in. Converging strategies, not one
silver bullet:

1. **Manifest diff + Thread Report** (scope note §4) — ✅ **shipped.** The
   base↔head diff, changed-file bucketing, and the sticky PR briefing all exist:
   see [`thread-report.md`](thread-report.md) and live
   [PR #1](https://github.com/rdryfoos/specassay/pull/1). (Still open: a Loupe
   "PR view" that renders the same diff visually.)
2. **Intent-diff legibility** (§5) — surfacing ✅ **shipped** as the Thread
   Report's *What moved* + *Intent Changed* (see
   [`thread-report.md`](thread-report.md)); the **immutability gate** on the same
   diff remains proposed — small.
3. **Full intent-PR workflow** (§5) — the destination.

None of it asks the developer to tag more code. The value comes from *reading the
diff against the thread you already have* and *handing author and reviewer a
briefing instead of a checkmark.*
