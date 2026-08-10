# The trace-manifest schema (`trace-manifest.json`)

Portable, vendor-neutral **trace-manifest** (matrix artifact). SpecAssay's Gate 2 always emits this file (default path `trace-manifest.json`); any emitter honoring this schema can write one.

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
| `gate`          | `{ ok: boolean, failures: GateFailure[] }`: the full Gate refuse set, including non-row failures |
| `totals`        | `registryIdCount`, `acCount`, `coveredCount`                 |
| `statusCounts`  | Counts for `proven`, `tracked-debt`, `GAP`, `backlog`        |
| `rows`          | Matrix rows                                                  |

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

**Registry drift:** Gate 2 requires **exact set** match: registry IDs ≡ IDs found under configured `specs` globs ≡ IDs found under configured `tasks` globs. Feature specs inherit; they do not mint. Registry IDs may not wait unclaimed.

**Invariant for viewers:** Gate PASS (`gate.ok`) ⇔ contiguous descent braid; Gate FAIL ⇔ fray, the Golden Thread broken. Tracked debt and excused incompleteness may still show amber (owed) or blue (not-yet) nodes without fray.

## Row shape

| Field             | Meaning                                                      |
| ----------------- | ------------------------------------------------------------ |
| `id`              | Durable ID from the registry                                 |
| `type`            | `AC` / `FR` / `NFR` / `US` (prefix)                          |
| `statement`       | Best-effort prose from the registry line                     |
| `registry`        | `{ path, line }` where the ID sits in the registry (relative to `repoPath`); `null` if the registry file was unreadable |
| `status`          | `proven` | `tracked-debt` | `GAP` | `backlog`                |
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

Backlog rows are "covered" in the promotion-contract sense when their child ACs are proven or debt, not by requiring `@covers` on the US/FR/NFR ID itself.

Older manifest files may omit `carryingTasks` / `registry` or still carry unused `blocked` / `blockedCount` fields. Gate emits `carryingTasks` (possibly empty) and `registry` (possibly `null`); Loupe treats missing fields as `[]` / absent. (Schema v3 carried this field under its former name; readers alias it on load, see **Version history**.)

## Consumers

**Loupe** (viewer) reads `trace-manifest.json` only. It must not re-scan the target. Every rendering must carry its meaning at rest: printed or screenshotted, the record still reads true. Links, hovers, expands, and live source fetches are courtesies to the reader, never load-bearing parts of the record.

## Version history

- **v4**: renames the row field `debtTasks` → `carryingTasks`. **Semantics unchanged.** The field holds the open `Carries:` tasks that excuse a row, and those tasks excuse **two** honest states: `tracked-debt` (work started, proof missing) and anointed `backlog` (minted ahead of the work, one open TODO). The old name implied everything in it was debt; the accurate name is `carryingTasks`, and the row's `status` says which state the carriers excuse. **Viewer authors: key color on `status`, never on the presence of carrying tasks**: amber for `tracked-debt`, blue for `backlog`. Readers accept schema `3` and `4` and alias `debtTasks` → `carryingTasks` on load; no data moved, so a v3 file and its v4 twin are identical apart from this key and the version integer. The rename was cheap here because the format has a single emitter and a single viewer, both first-party, with no external adopters yet.
