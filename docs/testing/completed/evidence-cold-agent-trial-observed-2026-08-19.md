# Evidence: the cold-agent trial, observed protocol

<!-- @covers US-DOCS-10, AC-DOCS-10 -->

Run against [`docs/testing/2-cold-agent-trial-observed.md`](../2-cold-agent-trial-observed.md), 2026-08-19. This is the second real cold-agent trial this project has run (the first: [`evidence-cold-agent-trial.md`](evidence-cold-agent-trial.md), 2026-08-06) — same method, a different target, run to gain real confidence before submitting a version update.

## Honest caveats, up front

- **Self-administered.** The docs room that built this session's `FR-GATE-40/50/70` fixes and wrote this session's docs also prepared this trial's fixture and reviewed its result. Not independently witnessed by a third party, unlike the 2026-08-06 trial's use of a real production repo (HomesFlow) as the target.
- **Same model family as the orchestrating session.** The cold agent was a fresh Claude Code subagent — zero conversation memory, not a fork — but not a different AI vendor. The protocol doesn't require vendor diversity; worth naming anyway.
- Full raw evidence (the agent's complete transcript, the fixture's git history, the independently-rerun manifests) is preserved outside this repo, not committed here in raw form — this document and [`samples/cold-trial-imei.trace-manifest.json`](../../../samples/cold-trial-imei.trace-manifest.json) are the durable record.

## Setup

- **Target**: [`python-validators/validators`](https://github.com/python-validators/validators), commit `70de324322def13a49a93d222f798ec1ab700885` — a real, small, public MIT-licensed Python library, chosen for having no connection whatsoever to SpecAssay or the family of projects around it.
- **Contamination preflight**: `grep -rniE "specassay|clewseau|homesflow|trace-manifest|golden thread|@covers|dryfoos"` across the full checkout, before installing anything — no matches. `README.md` and `CONTRIBUTING.md` read in full — ordinary validators-library content.
- **The requirement**, added as plain prose to a new `TODO.md` (the project has no existing backlog doc), no ID, no acceptance criterion, no hint, no file name:

  > We should support validating IMEI numbers (International Mobile Equipment Identity, used to identify mobile phones) — a way to check whether a given string is a valid 15-digit IMEI, including the Luhn checksum digit.

- Stock Spec Kit (`specify init --here --integration claude --force`) initialized clean, then SpecAssay installed via the **exact four commands in this repo's own public README**, against the real public catalog URLs — nothing local, nothing dev-path.
- Checked whether Gate config was auto-scaffolded: it was not — only `config-template.yml` existed after install. Left as-is on purpose; discovering and copying it was left for the agent, since that's a real step the README's own quickstart names.
- Fixture committed clean at this point — the agent-start revision — before the agent ever saw it.
- The agent received **one sentence**, nothing else: *"Find the newly added plain-language requirement and complete it using the repository's normal workflow."* No mention of SpecAssay, Spec Kit, IDs, or that this was a trial.

## Result

The agent discovered and used the full installed workflow entirely on its own:

1. **Minted** `FR-IMEI-10` and four atomic acceptance criteria (`AC-IMEI-10/20/30/40`) into a new `PRD.md`, via the installed `mint-id.sh`.
2. **Specified, planned, tasked** — `specs/001-imei-validation/{spec,plan,tasks}.md` plus a requirements checklist, via the installed `speckit-specify`/`speckit-plan`/`speckit-tasks` skills, every task carrying `**Carries**:` marks and a pre-written test name.
3. **Built test-first**: `tests/test_imei.py` written and confirmed *failing* before `src/validators/imei.py` existed.
4. **Built** `imei()` (reusing the library's existing `card_number` Luhn implementation), carrying `# @covers FR-IMEI-10, AC-IMEI-10, AC-IMEI-20, AC-IMEI-30, AC-IMEI-40`.
5. **Ran Gate 2** via the installed `speckit-specassay-check-gate` hook and reported `gate.ok=true`, 5/5 `proven`, 0 GAP.
6. **Ran the full suite**, found 17 pre-existing failures in an unrelated module, and confirmed via a clean `git stash` that they predated this change before reporting them as irrelevant.

## Independent reverification (not taken on the agent's word)

Everything below was re-run by the docs room, fresh, after the agent finished:

| Claim | Reverified how | Result |
| --- | --- | --- |
| Files changed match the report | `git diff --stat` from the agent-start commit | Identical: 3 modified, 12 new, nothing else |
| The new tests pass | `pytest tests/test_imei.py -v`, run fresh | 9/9 pass |
| The Gate really passes | A **second, independent** `check-traceability.sh` run, config untouched, manifest moved aside first (not overwritten blind) | `gate.ok=true`, 5/5 `proven`, 0 GAP — `statusCounts` diffed byte-for-byte against the agent's own manifest: **identical** |
| "887 passed, 17 unrelated failures" | Full suite re-run fresh | 17 failed / 887 passed, exact match; all 17 are `test_eth_address.py`, all the same missing-optional-dependency `ImportError`, confirmed unrelated by inspection |
| "Followed the constitution's traceability article" | Read `.specify/memory/constitution.md` directly | Real, present — the SpecAssay preset's own appended article, not an invented justification |

## What a stock Spec Kit run would not have produced

| SpecAssay addition | Where it shows |
| --- | --- |
| Durable IDs minted into a registry | `PRD.md` |
| `**Carries**:` on every task | `specs/001-imei-validation/tasks.md` |
| `@covers` annotation in source | `src/validators/imei.py` |
| Proof named to a checkable grammar | `tests/test_imei.py` |
| Machine-checkable emit proving the chain held | [`samples/cold-trial-imei.trace-manifest.json`](../../../samples/cold-trial-imei.trace-manifest.json) (real, unedited — `repoPath`/`targetName` scrubbed the same way `samples/sample.trace-manifest.json` is, nothing else touched) |

## Verdict

**Pass**, per the protocol's own definition: the uncoached agent reached an honest done state from a cold setup; artifacts agree; tests pass; independent reviewer verification confirms the Gate and manifest match the repository. This is the evidence behind `AC-DOCS-10` and `RELEASE-HANDOFF.md` Must #3 ("cold-install proof, attached").
