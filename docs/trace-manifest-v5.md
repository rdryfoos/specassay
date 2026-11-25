# trace-manifest v5: interop rev (beta)

**Status: beta.** `schemaVersion: 5` is live but explicitly revisable: field names and
shapes here may still move as the first external emitter (clew) pushes on them, without a
version bump. Loupe reads schema **3–5** today, uploads included. Two v5 samples ship in
[`samples/`](../samples/): [`sample-v5.trace-manifest.json`](../samples/sample-v5.trace-manifest.json)
(FieldKit: SpecAssay-dialect, tiers + parents + rollups, ~31 rows) and
[`clew-style-v5.trace-manifest.json`](../samples/clew-style-v5.trace-manifest.json)
(ledger origins, Swift symbol anchors, `nativeStatus`). SpecAssay's own Gate still emits v4;
it bumps once the beta settles. When it does, this doc folds into
[`trace-manifest-schema.md`](trace-manifest-schema.md).

## Why v5

v4 is a single-emitter, single-viewer format: SpecAssay writes it, Loupe reads it, and the
requirement→criterion hierarchy is *inferred* from the `US/FR/NFR/AC` prefix and the domain
token in the ID. That convention is load-bearing, and it only holds for SpecAssay's own
naming.

v5 opens the format to a **second emitter**, Thorsten Schlathölter's *clew* /
Ariadne-Thread, built on CAS-DD (Code-Anchored Spec-Driven Development), so he can extract
clew's data into a manifest and render it through the same glass. Three facts about clew
drive the rev:

1. **It models the tier explicitly.** In CAS-DD, "a requirement is covered once all of its
   acceptance criteria are covered" is a real edge, not a naming convention. v5 must carry
   that edge as data.
2. **Its IDs are ledger-minted.** clew mints immutable IDs from a sequence held in a ledger;
   they survive rewrites. v4's `registry: {path, line}` assumes an ID sits on a markdown
   line. v5 must generalize where an ID comes from.
3. **It is code-anchored.** Anchors may be spans or symbols, and should survive reflow the
   same way the IDs do.

## Design principles

- **Additive and optional.** Every v5 field is optional. A valid v4 file is a valid v5 file
  minus the new fields. Loupe reads schema `3`, `4`, and `5`.
- **Emitter-neutral core.** The `US/FR/NFR/AC` prefixes stay as *SpecAssay's* dialect. The
  format's core speaks in `tier` and explicit edges, which any emitter can populate.
- **Edges are canonical; rollup is a courtesy.** The parent/child edges are the single source
  of truth. A precomputed `rollup` may accompany them so a viewer need not recompute, but
  when they disagree, the edges win. (This is option **B**: carry both.)
- **The `status` core is fixed; native terms map onto it.** Loupe's colors key on a
  four-value core. An emitter with a different coverage model records its own `nativeStatus`
  and maps it to one of the four.

## Top-level shape (v5)

| Field           | Meaning                                                      | v5 |
| --------------- | ------------------------------------------------------------ | -- |
| `schemaVersion` | `5`                                                          | ✎ |
| `format`        | Always `"trace-manifest"`                                    |   |
| `emitter`       | **Now an object** `{ name, version }`. `name` is the tool (`"specassay-check"`, `"clew"`); `version` is its own release string. A bare string is still accepted and read as `{ name }`. | ✎ |
| `targetName`    | Project label                                                |   |
| `repoPath`      | Absolute path scanned                                        |   |
| `generatedAt`   | ISO-8601 UTC                                                 |   |
| `gate`          | `{ ok, failures[] }`: the emitter's refuse set              |   |
| `totals`        | `registryIdCount`, `acCount`, `coveredCount`                 |   |
| `statusCounts`  | Counts for the four core statuses                            |   |
| `rows`          | Matrix rows                                                  |   |
| `ext`           | **NEW.** Reserved object for emitter-specific data a generic viewer ignores. Key by emitter name: `ext: { clew: { … } }`. | ＋ |

`✎` changed · `＋` new.

## Row shape (v5)

| Field             | Meaning                                                      | v5 |
| ----------------- | ------------------------------------------------------------ | -- |
| `id`              | Durable ID                                                   |   |
| `type`            | Emitter dialect kind (`AC`/`FR`/`NFR`/`US` for SpecAssay). Free-form; the portable altitude is `tier`. |   |
| `tier`            | **NEW.** Portable altitude, decoupled from prefix: `"objective" \| "intent" \| "requirement" \| "criterion"`. SpecAssay maps `OBJ→objective`, `US→intent`, `FR/NFR→requirement`, `AC→criterion`; clew maps its own kinds. Viewers order the descent by `tier`, falling back to `type` prefix when absent. | ＋ |
| `statement`       | Best-effort prose from the source                            |   |
| `parents`         | **NEW.** `[id]`: the upward edges (a criterion's requirement, a requirement's intent, an intent's objective), declared not inferred, **more than one allowed**, and **ordered: the first parent is the next tier up**. Empty/absent ⇒ fall back to the domain-grouping convention. | ＋ |
| `origin`          | **NEW.** Where the ID comes from (see below). Generalizes `registry`. **Where the row lives, never who wrote it** — see `authorship`. | ＋ |
| `authorship`      | **NEW.** `"case" \| "design" \| "retrospective" \| "constitution"`: **who authored the row** (see below). Absent when undeclared. | ＋ |
| `registry`        | `{ path, line }`: retained. Equivalent to `origin` with `kind: "registry-line"`; readers alias one to the other. |   |
| `status`          | One of the four core statuses                                |   |
| `nativeStatus`    | **NEW.** Optional emitter-native coverage term, when it differs from the core. Informational; color keys on `status`. | ＋ |
| `implementations` | Coverage anchors (see anchor shape)                          |   |
| `proofs`          | Proof anchors (`{ name, … }`)                                |   |
| `carryingTasks`   | Open `Carries:` tasks that excuse `tracked-debt` / anointed `backlog` |   |
| `rollup`          | **NEW, courtesy.** Precomputed coverage over children (see below). | ＋ |
| `attestedBy`      | Optional operator stamp                                      |   |

### `authorship`: who authored the row

```jsonc
"authorship": "case" | "design" | "retrospective" | "constitution"
```

**Authorship names who authored the row, not where the row lives.** Where it lives is
`origin`, directly above. The two were nearly one field and must not be: a reader asking
"did the business ask for this, or did we decide it?" is asking something a file path
cannot answer.

One value per row, set when the row is minted, by a hand. Four values, and no fifth:

| Value | The row exists because |
| --- | --- |
| `case` | it states a promise from the project's CASE, in the reader's words or on their behalf |
| `design` | a design decision: a screen rule, a control, an order, something the reader assumed rather than promised |
| `retrospective` | it was minted from a retrospective or a defect |
| `constitution` | a principle demanded it — not that the row sits in `CONSTITUTION.md` |

**A sentence carrying two authors.** The row takes the authorship of **the clause that
caused it to be minted**. The other clause is a finding for the registry's owner, not a
second value. There is no list value, and no fifth value: a row that none of the four will
take is a finding to report, not a reason to invent one.

**How a registry line declares it.** On the definition line itself, after the statement, in
the shape every other line-level declaration in this tool uses (`**Carries**:` on a task,
`**Retires**:` on a task):

```markdown
- AC-PAY-10 — Given a declined card, when checkout submits, then the reason is shown. **Authorship**: case
```

The declaration is stripped out of the row's `statement`, so it never appears as prose in
the coverage matrix, the portfolio snapshot or the Thread Report. The value is matched
without regard to case and stored lowercase: the field is filled by a hand, one row at a
time, and spending a refusal on a capital letter would teach nothing. Anything that is not
one of the four is still refused.

**What the check does.** A row with **no** authorship is a diagnostic naming the ID and does
not fail the Gate: every registry predates this field, and refusing an unfilled row would
red every adopter on upgrade for work nobody has asked them to do. A row with a value
**outside the four** fails, naming both the ID and the value it declined, because a row
claiming an author that does not exist reads as answered.

**What the Thread Report says.** One sentence above the table, this shape and no other:

> 10 requirements came from the case, 21 from the project (design 19, retrospective 2, constitution 0).

While any row is unassigned the sentence says how many instead of presenting part of the
registry as the whole:

> No author named on 99 of 104 requirements; of the rest, 0 came from the case, 5 from the project (design 0, retrospective 5, constitution 0).

When *every* row is unassigned there is no rest to count, and the sentence says only that:

> No author named on any of the 104 requirements.

### The objective tier: the row above the story

<!-- @covers AC-CASE-50c -->

v5's first three tiers stopped one short of the question a reader of a thread ends up
asking. A walk up from a test reached the story and stopped, because the row above the
story had nowhere to live, and a registry can be entirely green while nobody can say what
any of it was for. `tier: "objective"` is that row.

An objective is **not a registry row**. It is defined in the project's *case* (the document
that holds the bets), where SpecAssay reads it by its own definition line, and it reaches
the manifest as a row like any other:

```jsonc
{
  "id": "OBJ-WALK-10",
  "type": "OBJ",
  "tier": "objective",
  "statement": "A walker gets home without stopping to read a map.",
  "origin": { "kind": "case-line", "path": "CASE.md", "line": 5 },
  "parents": [],
  "status": "proven",
  "rollup": { "rows": 3, "proven": 1, "tracked-debt": 0, "backlog": 2, "GAP": 0, "retired": 0 }
}
```

Five things a reader of this file needs to know about those rows:

- **`rows` holds both kinds.** `statusCounts` still counts the registry's rows only, and
  `totals.objectiveCount` says how many of the rows are objectives. An objective's status
  is a rollup of rows already counted, so adding it would count the same work twice.
- **An objective has no parent.** The tier is the top, and `parents` is `[]`.
- **A story's first parent is its objective**, declared on the story's own line and never
  inferred from a shared ID family: `US-WALK-01` and `OBJ-WALK-10` share a domain and that
  is all they share. Below the story the first parent is the row above it in the registry
  document, with any objectives that row also serves riding after it.
- **The edges are many-to-one, so they do not partition.** A story cited by two objectives
  sits in both their rollups. An objective's rollup is a count over its own subtree and
  must never be summed with another objective's. The registry document's own parent tree is
  unaffected and stays single-parent, which is what keeps its recursive rollup cycle-safe
  (see `docs/trace-manifest-schema.md`). These edges cannot make a cycle: they only ever
  point from a registry row up into the case, and no objective has a parent.
- **An objective can be called off, and says so.** A bet a project no longer holds is
  marked `**Superseded**: (YYYY-MM-DD): reason` on its own definition line in the case.
  Its row keeps its ID and its statement, carries `"superseded": {"date", "reason"}`,
  reads `status: "retired"`, and is not counted as unserved: a finished bet is not a
  neglected one. The alternative, deleting the objective, loses both the ID and the
  record of the change of mind, which is the thing a case is kept for.

  ```jsonc
  {
    "id": "OBJ-GROUP-10",
    "tier": "objective",
    "statement": "A walker can see where the rest of the group is.",
    "status": "retired",
    "superseded": { "date": "2026-11-25", "reason": "nobody walked in a group" }
  }
  ```

### `origin`: generalized ID provenance

```jsonc
"origin": {
  "kind": "registry-line" | "ledger" | "external",
  "path": "specs/PRD.md",   // registry-line: the file…
  "line": 14,               // …and the line
  "ledger": ".clew/ledger", // ledger: the ledger reference…
  "seq": 4271               // …and the immutable sequence number
}
```

`registry-line` is SpecAssay's world; `ledger` is clew's. A viewer links whatever it's given
and treats an ID with no resolvable origin as a plain durable token. `registry: {path,line}`
and `origin: {kind:"registry-line",path,line}` are two spellings of the same fact; emitters
may write either, readers accept both.

### Anchor shape (implementations / proofs)

```jsonc
{ "path": "src/sync.py", "line": 51, "endLine": 58, "symbol": "reconcile", "sha": "…", "excerpt": "…" }
```

v4 anchors are `{ path, line, excerpt }` (proofs add `name`). v5 adds optional `endLine`,
`symbol`, and `sha` so a code-anchored emitter can point at a span or a symbol that survives
reflow. `line` remains the common case; everything else is optional enrichment.

### `rollup`: precomputed coverage (option B)

```jsonc
"rollup": {
  "covered": true,
  "children": ["AC-SYNC-01", "AC-SYNC-02"],
  "coveredChildren": 2
}
```

A requirement is *covered* when all of its child criteria are covered (`proven` or excused
debt). The `children` are derivable from the `parents` edges; `rollup` carries the emitter's
own answer so a viewer need not recompute. **The edges are canonical**: if `rollup.covered`
contradicts what the edges imply, a viewer trusts the edges and may flag the disagreement.

SpecAssay's own emitter carries the count form instead, which is the shape a renderer can
name its basis from: per-status counts over the whole subtree at any depth, plus `rows` for
the subtree's total.

```jsonc
"rollup": { "rows": 3, "proven": 1, "tracked-debt": 0, "backlog": 2, "GAP": 0, "retired": 0 }
```

#### The colour rule

<!-- @covers AC-CASE-50c -->

A count does not tell a renderer what colour to paint, so every viewer that wanted one has
so far decided for itself, which is how two renderings of one manifest come to disagree.
**The rule, ratified 2026-09-22, in full, so no viewer has to invent one:**

> A parent's colour is the **weakest started** status beneath it, in this order of
> weakness: **`GAP`, then `tracked-debt`, then `proven`**. `backlog` and `retired` are
> **counted but never coloured**. A parent with nothing started beneath it is
> **`backlog`**.

Read it as: if anything beneath the parent is a `GAP`, the parent is a `GAP`, whatever else
is green; if nothing is a `GAP` but something is tracked debt, the parent is tracked debt;
if the only started rows are proven, the parent is proven; and a parent whose subtree is
entirely backlog or retired is backlog, not green and not red.

Two notes a viewer needs:

- **The basis is the subtree, not the children alone**, which is the same basis the counts
  use: a mid-tier `GAP` must not vanish from an ancestor because the row between them is
  green.
- **An emitter may publish the colour as the parent row's own `status`.** SpecAssay does
  exactly that on objective rows, and nowhere else: registry rows carry their own measured
  status, and `rollup` beside it. Where a row's `status` is a rolled-up colour rather than
  its own, the row is an objective, which `tier` already says.
- **A superseded objective takes no colour at all.** Where an objective carries
  `superseded`, its `status` is `retired` and the rule above is not applied to it: a
  called-off bet must not be painted by the state of work that outlived it, and `retired`
  is the status core's own word for a row that is no longer measured. This is the rule's
  only exception, added 2026-11-25 with `FR-CASE-70`; every other objective row's status
  is the colour the rule gives.

## Status core (unchanged) + native mapping

The four core statuses and their colors are fixed; this is Loupe's contract:

| Status         | Color | Meaning                                                      |
| -------------- | ----- | ----------------------------------------------------------- |
| `proven`       | green | Named carrier exists                                        |
| `tracked-debt` | amber | Work started, proof missing, excused by an open `Carries:` task |
| `GAP`          | red   | Criterion with neither proof nor open debt; the gate refuses |
| `backlog`      | blue  | Planning altitude; not a silent gap                         |

An emitter whose model doesn't divide the world this way records its own `nativeStatus`
(e.g. `"partial"`, `"anchored"`) and maps it onto one of the four. Loupe never colors on
`nativeStatus`; it's there for round-tripping and tooltips.

## Back-compat

- Loupe accepts `schemaVersion` `3`, `4`, `5`. v3's `debtTasks` aliases to `carryingTasks`
  on load (unchanged from v4).
- Every v5 field is optional; a v4 file needs no migration to read as v5.
- SpecAssay's emitter keeps writing `type`, `registry`, and domain-grouped IDs. It *gains*
  `tier`, `parents`, and `rollup` (all derivable from what it already knows), so a SpecAssay
  v5 manifest is self-describing without relying on the prefix convention, but the
  convention still works as the fallback.

## Emitter-conformance checklist

The minimum a manifest needs for Loupe to render the intent → build → proof descent truthfully.
**This is the page to hand a new emitter.** The schema doc is the reference; this is the
contract.

- [ ] `format: "trace-manifest"` and `schemaVersion: 5`.
- [ ] `emitter: { name, version }`.
- [ ] `gate: { ok: boolean, failures: [] }`: `ok` drives braid-vs-fray; `failures` may be empty.
- [ ] `rows[]`, each with:
  - [ ] `id`: a durable, stable token.
  - [ ] `tier`: `objective` \| `intent` \| `requirement` \| `criterion` (or a `type` prefix Loupe can map).
  - [ ] `status`: one of the four core values.
  - [ ] `statement`: human-readable prose (best effort).
  - [ ] `parents: [id]` for anything below the top tier: **the edges Loupe draws the thread from**, first parent = the next tier up.
- [ ] Proofs/implementations as anchors (`{ path, line? }` minimum) where they exist.
- [ ] `origin` (or `registry`) where an ID is locatable: optional, purely a courtesy link.
- [ ] `rollup` on requirements: optional; Loupe recomputes from edges if absent.

Everything not on this list is enrichment. A manifest that satisfies it renders; a manifest
that adds `ext`, `symbol`, `sha`, `nativeStatus`, `rollup`, etc. renders richer.

## Worked example: a clew-style row mapped to v5

A ledger-minted requirement and one of its criteria, code-anchored, as clew might emit them:

```jsonc
{
  "schemaVersion": 5,
  "format": "trace-manifest",
  "emitter": { "name": "clew", "version": "0.9.0" },
  "targetName": "ariadne-demo",
  "rows": [
    {
      "id": "REQ-0042",
      "tier": "requirement",
      "type": "requirement",
      "statement": "Offline edits reconcile across devices on reconnect.",
      "status": "proven",
      "origin": { "kind": "ledger", "ledger": ".clew/ledger", "seq": 42 },
      "rollup": { "covered": true, "children": ["CRIT-0043"], "coveredChildren": 1 }
    },
    {
      "id": "CRIT-0043",
      "tier": "criterion",
      "type": "acceptance-criterion",
      "statement": "A change made offline appears on a second device within 2s of reconnect.",
      "status": "proven",
      "parents": ["REQ-0042"],
      "origin": { "kind": "ledger", "ledger": ".clew/ledger", "seq": 43 },
      "implementations": [{ "path": "Sources/Sync/Reconcile.swift", "symbol": "reconcile", "line": 88 }],
      "proofs": [{ "name": "testReconcileWithinBudget", "path": "Tests/SyncTests.swift", "line": 40 }],
      "nativeStatus": "anchored"
    }
  ]
}
```

Loupe reads this with no knowledge of clew: it orders `REQ-0042` above `CRIT-0043` by `tier`,
draws the thread along `parents`, colors both green on `status`, and links the Swift anchors.
The `nativeStatus`, `symbol`, and ledger `origin` ride along untouched.

## Non-goals

- Not OMG ReqIF / OSLC / W3C traceability; those remain optional future adapters.
- v5 does not standardize *how* an emitter decides coverage; it standardizes how the result
  is expressed. clew and SpecAssay may compute "covered" differently and both round-trip.
