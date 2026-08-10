# trace-manifest v5 — interop rev (draft proposal)

**Status:** draft. Targets `schemaVersion: 5`. Nothing here is emitted yet — this is the
artifact we iterate on before touching the emitter, the Loupe reader, or the samples. When
it settles, it folds into [`trace-manifest-schema.md`](trace-manifest-schema.md) and the
version integer bumps.

## Why v5

v4 is a single-emitter, single-viewer format: SpecAssay writes it, Loupe reads it, and the
requirement→criterion hierarchy is *inferred* from the `US/FR/NFR/AC` prefix and the domain
token in the ID. That convention is load-bearing, and it only holds for SpecAssay's own
naming.

v5 opens the format to a **second emitter** — Thorsten Schlathölter's *clew* /
Ariadne-Thread, built on CAS-DD (Code-Anchored Spec-Driven Development) — so he can extract
clew's data into a manifest and render it through the same glass. Three facts about clew
drive the rev:

1. **It models the tier explicitly.** In CAS-DD, "a requirement is covered once all of its
   acceptance criteria are covered" is a real edge, not a naming convention. v5 must carry
   that edge as data.
2. **Its IDs are ledger-minted.** clew mints immutable IDs from a sequence held in a ledger —
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
  of truth. A precomputed `rollup` may accompany them so a viewer need not recompute — but
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
| `gate`          | `{ ok, failures[] }` — the emitter's refuse set              |   |
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
| `tier`            | **NEW.** Portable altitude, decoupled from prefix: `"intent" \| "requirement" \| "criterion"`. SpecAssay maps `US→intent`, `FR/NFR→requirement`, `AC→criterion`; clew maps its own kinds. Viewers order the descent by `tier`, falling back to `type` prefix when absent. | ＋ |
| `statement`       | Best-effort prose from the source                            |   |
| `parents`         | **NEW.** `[id]` — the upward edges (a criterion's requirement, a requirement's intent), declared not inferred. Empty/absent ⇒ fall back to the domain-grouping convention. | ＋ |
| `origin`          | **NEW.** Where the ID comes from (see below). Generalizes `registry`. | ＋ |
| `registry`        | `{ path, line }` — retained. Equivalent to `origin` with `kind: "registry-line"`; readers alias one to the other. |   |
| `status`          | One of the four core statuses                                |   |
| `nativeStatus`    | **NEW.** Optional emitter-native coverage term, when it differs from the core. Informational; color keys on `status`. | ＋ |
| `implementations` | Coverage anchors (see anchor shape)                          |   |
| `proofs`          | Proof anchors (`{ name, … }`)                                |   |
| `carryingTasks`   | Open `Carries:` tasks that excuse `tracked-debt` / anointed `backlog` |   |
| `rollup`          | **NEW, courtesy.** Precomputed coverage over children (see below). | ＋ |
| `attestedBy`      | Optional operator stamp                                      |   |

### `origin` — generalized ID provenance

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

### `rollup` — precomputed coverage (option B)

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

## Status core (unchanged) + native mapping

The four core statuses and their colors are fixed — this is Loupe's contract:

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
  v5 manifest is self-describing without relying on the prefix convention — but the
  convention still works as the fallback.

## Emitter-conformance checklist

The minimum a manifest needs for Loupe to render the wish → work → proof descent truthfully.
**This is the page to hand a new emitter** — the schema doc is the reference; this is the
contract.

- [ ] `format: "trace-manifest"` and `schemaVersion: 5`.
- [ ] `emitter: { name, version }`.
- [ ] `gate: { ok: boolean, failures: [] }` — `ok` drives braid-vs-fray; `failures` may be empty.
- [ ] `rows[]`, each with:
  - [ ] `id` — a durable, stable token.
  - [ ] `tier` — `intent` \| `requirement` \| `criterion` (or a `type` prefix Loupe can map).
  - [ ] `status` — one of the four core values.
  - [ ] `statement` — human-readable prose (best effort).
  - [ ] `parents: [id]` for anything below the top tier — **the edges Loupe draws the thread from.**
- [ ] Proofs/implementations as anchors (`{ path, line? }` minimum) where they exist.
- [ ] `origin` (or `registry`) where an ID is locatable — optional, purely a courtesy link.
- [ ] `rollup` on requirements — optional; Loupe recomputes from edges if absent.

Everything not on this list is enrichment. A manifest that satisfies it renders; a manifest
that adds `ext`, `symbol`, `sha`, `nativeStatus`, `rollup`, etc. renders richer.

## Worked example — a clew-style row mapped to v5

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

- Not OMG ReqIF / OSLC / W3C traceability — those remain optional future adapters.
- v5 does not standardize *how* an emitter decides coverage; it standardizes how the result
  is expressed. clew and SpecAssay may compute "covered" differently and both round-trip.
