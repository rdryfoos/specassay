# Reading a trace-manifest

This guide teaches you to read a SpecAssay **trace-manifest** (`trace-manifest.json`) the way the workflow means it: intent → build → proof, then what the Gate wrote down, then what **Loupe** paints.

Field-level schema details live in [`trace-manifest-schema.md`](./trace-manifest-schema.md). This is the story version.

## What a trace-manifest is

Every piece of tracked work has three legs: an **intent** (a durable ID in the registry, usually the PRD), a **build** (code carrying an `@covers` mark), and a **proof** (a test named after the acceptance criterion it answers for).

Gate 2 scans the project for all three legs on every ID and writes what it found into one file: the trace-manifest. Default path is `trace-manifest.json` at the repo root. Portable samples use `{name}.trace-manifest.json`.

Two things to hold onto before reading any row:

**Loupe only reads the file.** It never re-scans the project. If it isn't in the manifest, Loupe doesn't know it.

**A passing Gate does not mean everything is done.** It means nothing unfinished is *hidden* at acceptance-criterion altitude, and the ID inventory is consistent (registry ≡ specs ≡ tasks, called **exact-set**). Unfinished work is allowed. Hidden unfinished work is refused.

## The four statuses

Every row lands in one of four states. The question that sorts them is simple: *if this work is unfinished, can you see that from the durable record?*

| Status           | Plain meaning                                                |
| ---------------- | ------------------------------------------------------------ |
| **proven**       | A named carrier exists (an AC test, or `@covers`/proof for US/FR/NFR). A fact that a carrier exists, not a claim the code is correct. |
| **tracked-debt** | Work started, proof missing, but an open task says so with `Carries:`. Unfinished and visible. |
| **backlog**      | Planning altitude. A US/FR/NFR with no carrier of its own, or any ID anointed into backlog (see below). Not started, and honestly so. |
| **GAP**          | An AC with neither a proof nor an open debt task. Unfinished and *hidden*. The Gate refuses. |

Two rules keep this fair:

**Silent-gap refusal is AC-only.** Acceptance criteria are the atomic unit of "covered." A user story or feature ID with no carrier of its own is `backlog`, never `GAP`. Parents count as covered when their child ACs are proven or tracked debt, not by sticking `@covers US-…` on a file.

**Minting an ID is a promise, and the Gate holds you to it immediately.** An ID that sits in the registry claimed by nothing fails exact-set; that's drift, and it's often just a fat-fingered rename in a spec. To mint ahead of the work on purpose, use **anointed backlog**: mint the ID *and* write one open `Carries:` TODO for it (the conventional home is `specs/backlog/tasks.md`, which the standard tasks glob already matches). The TODO proves the intent is real and names who carries it. The ID rides as `backlog`, visible, until a spec claims it and normal rules take over. A typo'd ID never comes with a matching TODO, so the drift tripwire still fires.

## How to read one row

For any ID, ask five questions in order:

1. **Where does the intent live?** Find the ID's statement in the PRD / registry.
2. **What build work is done vs open?** Look for `Carries:` on checkbox tasks.
3. **What carriers exist?** `@covers` marks in source; tests named for the AC.
4. **What did the Gate emit?** The row's `status`, `implementations[]`, and `proofs[]`.
5. **What does Loupe paint?** Colors on Intent / Build / Proof, and whether the braid frays.

## Loupe's colors

| Signal                | Meaning                                                      |
| --------------------- | ------------------------------------------------------------ |
| Green node            | A carrier is present for that step.                          |
| Amber node, braid solid | Owed — tracked debt, admitted on an open task. The Golden Thread is intact. |
| Blue node, braid solid | Not yet — an empty backlog step or an honest-missing carrier. The Golden Thread is intact. |
| Fray / red banner     | The Golden Thread is broken: a silent AC gap, or any other refusal (`gate.ok: false`). |

Amber and blue don't mean broken. On a solid braid they mean "unfinished and admitted" — amber for owed, blue for not-yet. Only fray means broken, and fray appears only when the Gate refused.

## Worked examples (HomesFlow)

The examples below come from a real Gate 2 emit against HomesFlow: `gate.ok: true`, 82 rows, 67 proven / 10 tracked-debt / 5 backlog / 0 GAP. That emit is checked in as `samples/homesflow.trace-manifest.json`. The other sample, `samples/sample.trace-manifest.json`, is a clean synthetic demo (honest today; a future mocked version may show states HomesFlow doesn't have, like a GAP).

### `AC-GUEST-01`: proven

The story: a guest opens a home and sees only guest-marked fields, with edit controls disabled. The work is done, and a test answers for it.

1. **Intent:** the PRD owns the guest-visibility AC.
2. **Build:** the guest restriction work is done and traced in tasks.
3. **Carriers:** `@covers AC-GUEST-01, …` on the guest test module, and a named proof: `test_AC_GUEST_01_guest_fields_only`.
4. **Manifest:** `implementations: [{…}]`, `proofs: [{ name: test_AC_GUEST_01_… }]`, status `proven`.
5. **Loupe:** Intent, Build, and Proof green. Braid solid.

A variation: `AC-A11Y-01` is proven with *proofs only* (named accessibility tests, empty `implementations[]`). Still `proven`, because AC altitude keys on the named proof.

### `AC-HOME-09`: tracked-debt

The story: the iPad layout work shipped, but its snapshot test is waiting on test infrastructure. Someone wrote that down instead of staying quiet.

1. **Intent:** the PRD owns AC-HOME-09 (iPad trailing column is content only).
2. **Build done:** task `T021a` is checked off.
3. **Proof still open:** task `T024d` (snapshot/UI test, deferred until XCUITest infra lands; manual iPad pass until then) carries the admission: `Carries: AC-HOME-09`.
4. **Manifest:** `implementations: []`, `proofs: []`, status `tracked-debt`. The ID rides on an open checkbox task.
5. **Loupe:** Intent **amber** (owed) with the open `Carries:` task listed; Build **blue** (no `@covers` yet); Proof **blue** with "No proof — tracked as debt." Braid solid, because nothing is hidden.

### `AC-HOME-10`: tracked-debt, build further along

Same shape as AC-HOME-09, one difference: the code carries `@covers AC-HOME-10`, so the Build step has a carrier even though the named proof is still open (task `T024e`). Manifest: `implementations: [{…}]`, `proofs: []`, status `tracked-debt`. In Loupe, Build is green with an expandable file:line source; Proof is blue but excused; braid solid.

This pair is worth comparing: two ACs, same status, different amounts of progress. `tracked-debt` is a range, not a point, and the manifest shows where in the range you are.

### `US-EDIT-01` / `FR-GUEST-02`: backlog

The story: a user story or feature ID living at planning altitude. Its child ACs may have plenty of work; the parent ID itself carries nothing, and doesn't have to.

Manifest: empty arrays, status `backlog`, not `GAP`. Loupe mutes the empty steps and keeps the braid solid. A story label is never frayed for lacking its own carrier.

### `US-SHARE-01`: anointed backlog

The story: an Owner story minted ahead of any work (a read-only procedure-share link). No spec, no code, no tests. What keeps it honest is one line:

```
- [ ] T901 Deliver read-only procedure sharing link — **Carries**: US-SHARE-01
```

That TODO in `specs/backlog/tasks.md` is the whole thread, and that's the point. Manifest: status `backlog`, `carryingTasks` lists the carrying TODO, `gate.ok: true`. Loupe shows the carrying TODO under the Intent. Delete the TODO without picking up the work, and the next Gate run fails exact-set.

### What a GAP would look like (HomesFlow has none)

Take any AC and remove both its named proof and its open `Carries:` task. The intent still sits in the PRD. The build may even look "done" in conversation. But nothing durable admits the missing proof.

Manifest: status `GAP`, `silent-gap` added to `gate.failures[]`, `gate.ok: false`. Loupe: fray, plus the Gate-failed banner.

Hold that next to AC-HOME-09. The difference between `tracked-debt` and `GAP` is not how much work is finished; AC-HOME-09 might be *less* finished. The difference is one open task admitting it. Visible unfinished work passes. Hidden unfinished work frays.

## Where this sits in the Spec Kit loop

```text
PRD / registry  →  specs inherit IDs  →  tasks with Carries:
        ↓
   implement + @covers + named AC tests
        ↓
   Gate 2 (exact-set + AC silent-gap refusal)  →  trace-manifest.json
        ↓
   Loupe (view only)
```

Gate 1 judgment (`/speckit.analyze` and human review) still matters. Gate 2 is the deterministic check that refuses silent AC gaps and inventory drift, then leaves a trace-manifest anyone can open without re-running the scan.

## Further reading

- [the field guide](https://specassay.com/field-guide): the same story with screenshots
- [`../PROMOTION-CONTRACT.md`](../PROMOTION-CONTRACT.md): the rules this doc walks through
- [`trace-manifest-schema.md`](./trace-manifest-schema.md): field-level shape
- [`../presets/specassay/GLOSSARY.md`](../presets/specassay/GLOSSARY.md): the vocabulary registry
- [`../samples/README.md`](../samples/README.md): regenerating the HomesFlow sample
