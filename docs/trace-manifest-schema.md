# The trace-manifest schema (`trace-manifest.json`)

Portable, vendor-neutral **trace-manifest** (matrix artifact). SpecAssay's Gate 2 always emits this file (default path `trace-manifest.json`); any emitter honoring this schema can write one.

*This reference is `FR-DOCS-20` in this repo's own registry — see [`PRD.md`](../PRD.md).*

## Framing

- **Practice lineage:** software RTM discipline (safety-critical / Spec Kit outer loop). Not a claim of certification.
- **Not** OMG ReqIF or OSLC (requirements exchange / live linking). Those remain optional future adapters.
- **Not** W3C supply-chain "traceability" vocabularies.
- The `format` value is deliberately vendor-neutral: `trace-manifest` belongs to no single tool, so any emitter can write the same shape for one viewer. `format` + `schemaVersion` are the interop contract.

## Top-level shape

| Field           | Meaning                                                      |
| --------------- | ------------------------------------------------------------ |
| `schemaVersion` | `4`                                                          |
| `format`        | Always `"trace-manifest"`                                    |
| `emitter`       | Identifies the emitting tool. SpecAssay's Gate 2 writes `"specassay-check"`; other emitters write their own identifier |
| `targetName`    | Project label                                                |
| `repoPath`      | Absolute path scanned                                        |
| `generatedAt`   | ISO-8601 UTC                                                 |
| `gate`          | `{ ok: boolean, failures: GateFailure[], diagnostics: GateFailure[], executionVerified: boolean }`: the full Gate refuse set, including non-row failures, plus named findings that do not (yet) affect `ok`, plus whether `proven` on this run was derived from a passing test-results report or from name-matching alone |
| `totals`        | `registryIdCount`, `acCount`, `coveredCount`, `retiredCount` |
| `statusCounts`  | Counts for `proven`, `tracked-debt`, `GAP`, `backlog` — exactly these four keys, frozen; see **`retired`**, below |
| `rows`          | Matrix rows. Never includes retired IDs — see **`retired`** |
| `retired`       | `{ id, date, reason }[]`. IDs withdrawn on purpose; absent or `[]` if none. See **`retired`**, below |

### `gate.failures[]`

Each failure: `{ kind, detail, id? }`.

| `kind`                              | Meaning                                                  |
| ----------------------------------- | -------------------------------------------------------- |
| `silent-gap`                        | AC with neither named proof nor open `Carries:` task     |
| `orphan-covers`                     | `@covers` ID not in registry                             |
| `orphan-test`                       | Test-encoded ID not in registry                          |
| `missing-carries`                   | Checkbox task line without `Carries:`                    |
| `spec-orphan` / `task-orphan`       | Spec or tasks reference an ID not in the registry        |
| `spec-unclaimed` / `task-unclaimed` | Registry ID absent from specs or tasks (exact-set drift) |
| `registry-missing`                  | Configured registry file absent                          |
| `duplicate-id`                      | Two independent definition lines mint the same ID (v0.4.0+) |

**Registry drift:** Gate 2 requires **exact set** match: registry IDs ≡ IDs found under configured `specs` globs ≡ IDs found under configured `tasks` globs. Feature specs inherit; they do not mint. Registry IDs may not wait unclaimed.

### `gate.diagnostics[]`

Same shape as a failure (`{ kind, detail, id? }`), but never sets `gate.ok` to `false`. A named, visible finding whose pass/fail consequence hasn't been decided yet — the finding is real either way, so it is always emitted; only whether it blocks is open (PROMOTION-CONTRACT.md Rule 4a).

| `kind`             | Meaning                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| `uncovered-proof`   | ID with a real, passing proof that no file's `@covers` mark names (v0.4.7+) |

`uncovered-proof` is the mirror of `orphan-covers`: that failure catches an `@covers` mark naming an ID that isn't registered; this catches the reverse, a registered, tested, `proven` ID that no file's own `@covers` mark claims. Applies to any type (`AC`, `FR`, `NFR`, `US`), since rule 6 grants `proven` from a test alone for every type, not only `AC`.

### `gate.executionVerified`

`true` when `test_results` (config key, a JUnit XML path) was configured and found: `proven` on this run was derived from a *passing* test-results report, not name-matching alone (Rule 6a, v0.4.9+). `false` when `test_results` was absent or the file did not exist: `proven` fell back to the pre-6a name-matching-only meaning, and the Gate said so on stderr rather than silently proceeding. Viewers should render this distinction, not hide it: a `proven` row under `executionVerified: false` is a weaker claim than the same row under `true`.

**Invariant for viewers:** Gate PASS (`gate.ok`) ⇔ contiguous descent braid; Gate FAIL ⇔ fray, the Golden Thread broken. Tracked debt and excused incompleteness may still show amber (owed) or blue (not-yet) nodes without fray.

## Row shape

| Field             | Meaning                                                      |
| ----------------- | ------------------------------------------------------------ |
| `id`              | Durable ID from the registry                                 |
| `type`            | `AC` / `FR` / `NFR` / `US` (prefix)                          |
| `statement`       | Best-effort prose from the registry line                     |
| `registry`        | `{ path, line }` where the ID sits in the registry (relative to `repoPath`); `null` if the registry file was unreadable |
| `status`          | `proven` \| `tracked-debt` \| `GAP` \| `backlog` in this file; `trace-manifest.v5beta.json` adds a fifth, `retired` |
| `implementations` | `{ path, line, excerpt }` from coverage annotations          |
| `proofs`          | `{ name, path, line }` from test-encoded AC IDs              |
| `carryingTasks`   | `{ path, line, excerpt }` open checkbox tasks that name this ID (via `Carries:`): the carriers that excuse **both** `tracked-debt` and anointed `backlog`. The row's `status` says which state they excuse; viewers must key color on `status`, not on the presence of carrying tasks. |
| `attestedBy`      | Optional operator stamp; `null` until attribution exists     |

### Status vocabulary (coverage altitude)

| Status         | Who                                                  | Meaning                                                      |
| -------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| `proven`       | AC: named proof; US/FR/NFR: `@covers` or named proof | Named carrier exists (not "tests ran green")                 |
| `tracked-debt` | Any                                                  | Work started (spec/impl presence), proof missing, excused by an open task with `Carries:` (`carryingTasks` lists those tasks) |
| `GAP`          | **AC only** (silent gap)                             | Neither named proof nor open debt; the Gate refuses; the viewer frays |
| `backlog`      | Any                                                  | Planning altitude: US/FR/NFR without own carrier, or any ID **anointed into backlog** (registry entry + open `Carries:` TODO and nothing else). **Not** a silent gap; do not fray |
| `retired`      | Any (v5beta only)                                    | Withdrawn on purpose, not violated: derives entirely from an explicit `**Retires**: <id-list> (<YYYY-MM-DD>): <reason>` record on an open task — there is no settable status field. Checked ahead of every other branch, so a retired ID's underlying proof/pending state never shows through. In this file (v4), the row is absent from `rows[]` entirely; see **`retired`**, below |

Backlog rows are "covered" in the promotion-contract sense when their child ACs are proven or debt, not by requiring `@covers` on the US/FR/NFR ID itself.

Older manifest files may omit `carryingTasks` / `registry` or still carry unused `blocked` / `blockedCount` fields. Gate emits `carryingTasks` (possibly empty) and `registry` (possibly `null`); Loupe treats missing fields as `[]` / absent. (Schema v3 carried this field under its former name; readers alias it on load, see **Version history**.)

### `retired`

`trace-manifest.json` (v4) is a published schema with strict validators; it freezes at exactly the four status values above rather than growing a fifth enum member. A retired ID's row leaves `rows[]` entirely instead of carrying a value v4 never declared, and the same information — the retirement record itself — moves to this file's top-level `retired` array instead, so nothing disappears silently:

```json
"retired": [
  { "id": "AC-CLEW-01", "date": "2026-08-18", "reason": "cold-agent probe concluded; tooling archived at tag clew-era-final." }
]
```

`totals.retiredCount` mirrors this array's length. `statusCounts` in this file never gains a `retired` key — exactly the original four, always.

`trace-manifest.v5beta.json` takes the opposite approach on purpose: `retired` is a normal fifth row `status` there from the start (see **The second file**, below), and its own `statusCounts` does carry a `retired` key. The two files disagree about where a retired ID lives by design — v4 stays a closed, frozen contract; v5beta is where the format grows.

**Consumers: any exhaustive four-value switch on `status` — an engine's own internal logic, a viewer's legend, a `statusCounts` reader — must add the fifth value if it reads `trace-manifest.v5beta.json`, or declare itself v4-only if it doesn't.** Nothing reading v4 alone needs to change.

## The second file: `trace-manifest.v5beta.json`

<!-- @covers FR-DOCS-20 -->

Every Gate 2 run writes **two** files, not one: `trace-manifest.json` (this
schema, v4, the primary emit) and `trace-manifest.v5beta.json` alongside it
(since v0.4.5). If you're running the Gate for the first time and see a line
like `Wrote trace-manifest.v5beta.json (N rows, schemaVersion 5, beta)` you
haven't done anything wrong — that's expected, every run. v4 stays primary
and unchanged; the beta file is an early, additive look at schema v5, which
opens the format to a second emitter (`clew`). `retired` (see above) is the
first status value to debut in v5beta rather than v4 — a template for how
the two files are meant to diverge going forward: v4 stays a closed,
frozen contract; new vocabulary grows in v5beta first. Full spec:
[`trace-manifest-v5.md`](trace-manifest-v5.md). Nothing in this doc requires
reading that one — the beta file is safe to ignore until you have a reason
not to.

## Consumers

**Loupe** (viewer) reads `trace-manifest.json` only. It must not re-scan the target. Every rendering must carry its meaning at rest: printed or screenshotted, the record still reads true. Links, hovers, expands, and live source fetches are courtesies to the reader, never load-bearing parts of the record.

## Version history

- **FR-GATE-30** (2026-08-20): adds `retired`, a genuine fifth status, derived only from an explicit `**Retires**:` record. Deliberately asymmetric between the two files: v4 (this schema) freezes its four `statusCounts`/`status` values and gains a new top-level `retired` array instead of a fifth row status; v5beta carries `retired` as a normal fifth `status` value from the start. See **`retired`**, above.
- **v4**: renames the row field `debtTasks` → `carryingTasks`. **Semantics unchanged.** The field holds the open `Carries:` tasks that excuse a row, and those tasks excuse **two** honest states: `tracked-debt` (work started, proof missing) and anointed `backlog` (minted ahead of the work, one open TODO). The old name implied everything in it was debt; the accurate name is `carryingTasks`, and the row's `status` says which state the carriers excuse. **Viewer authors: key color on `status`, never on the presence of carrying tasks**: amber for `tracked-debt`, blue for `backlog`. Readers accept schema `3` and `4` and alias `debtTasks` → `carryingTasks` on load; no data moved, so a v3 file and its v4 twin are identical apart from this key and the version integer. The rename was cheap here because the format has a single emitter and a single viewer, both first-party, with no external adopters yet.
