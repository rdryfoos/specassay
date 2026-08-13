# Cold-agent trial, observed

The minimal trial asks whether a cold agent can carry one new plain-language
requirement to done using stock Spec Kit plus SpecAssay. This companion records
how the agent found and applied the installed guidance and where contamination
or friction entered. It is a prospective runbook, not evidence or an audit, and
provides no fixture, domain, or feature.

## Prerequisites

- After receiving this runbook, the volunteer independently chooses a public
  codebase unrelated to and never involved in developing SpecAssay. Record its
  repository URL and full source commit.
- The volunteer chooses a small plain-language requirement that has not
  appeared in SpecAssay development, documentation, examples, or prior trials.
  Record its exact wording. This runbook does not prescribe its domain or
  feature.
- [GitHub Spec Kit](https://github.com/github/spec-kit) 0.14.0 or newer.
- A fresh agent session with no prior exposure to the chosen repository,
  SpecAssay, or its trials through memory, rules, history, or transcripts.
- Necessary credentials, an external evidence directory, and a volunteer who
  can observe without coaching.

## Open the observation record

Before preparing the fixture, start a plain-text record containing:

- date, time zone, source URL, source commit, and exact requirement;
- operating system, Git, Python, `specify`, agent host, exact model, and enabled
  tool versions;
- memory, user-rule, indexing, and permission settings relevant to coldness;
- a preflight record and volunteer attestation;
- a timestamped intervention and contamination log, initially `none`.

## Prepare the disposable fixture

1. Make a disposable copy at the recorded source commit. Preserve ordinary
   project guidance, but remove any local teaching of the practice under test.
2. Add the exact requirement as plain prose to the project's ordinary product
   intake document. Add no durable ID, acceptance criterion, implementation
   hint, file name, or test name.
3. Before installing Spec Kit or SpecAssay, perform a contamination preflight.
   Confirm the fixture contains no references to SpecAssay, Clewseau, HomesFlow,
   prior trial artifacts, trace-manifest files, SpecAssay-specific commands, or
   requirement text copied or adapted from SpecAssay development,
   documentation, examples, or prior trials. Record the searches, manual
   review, paths, and results. A clean grep does not prove absence. The
   volunteer must attest that the repository was never involved in SpecAssay
   development and that the requirement is new and independently chosen. If
   either check fails, choose a different repository or requirement and rebuild
   the fixture.
4. Initialize the clean fixture with stock Spec Kit first. Record the exact
   command and `specify --version`.
5. Install SpecAssay from its public catalogs:

   ```bash
   specify preset catalog add \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json \
     --name specassay --install-allowed

   specify extension catalog add \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json \
     --name specassay --install-allowed

   specify bundle catalog add \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json \
     --id specassay --policy install-allowed

   specify bundle install specassay
   ```

6. Commit the fixture. Record the agent-start revision, confirm a clean
   worktree, and keep the runbook and evidence directory hidden. The installed
   bundle materials must be the agent's only exposure to SpecAssay's practice.

## Run without coaching

Open the recorded agent-start revision in the fresh session. Record the start
time, then send only:

> Find the newly added plain-language requirement and complete it using the repository's normal workflow.

Do not reveal this runbook, expected artifacts, commands, identifiers,
checkpoints, or pass criteria. Do not coach, correct, or redirect the agent.

Answer only access or environment questions required to continue. Log the
timestamp, question, answer, and reason. If an answer teaches the practice
under test, mark the trial compromised. Stop when the agent says it is done or
blocked. Record the stop time and preserve that state before any repair.

## Observe useful moments

Use the transcript and non-interrupting notes. Do not ask the agent to narrate
or pause for checkpoints. Record:

- each source of workflow guidance the agent uses, including first encounter
  and path;
- creation or change of intent, planning, task, source, proof, Gate, manifest,
  or pull-request artifacts;
- each test and Gate command, result, response to failure, and manifest emit;
- every block, retry, volunteer action, environment failure, and final done or
  blocked statement.

Retain complete output and the emitted `trace-manifest.json` from the first and
final Gate runs. Record `not reached` for a missing checkpoint. Observations
must not become cues.

## Preserve the evidence package

Before debriefing or reviewer commands, retain:

- the source URL and commit, exact requirement, preflight record, attestation,
  stock Spec Kit command and version, and agent-start revision;
- the complete transcript, setup record, guidance notes, and intervention log;
- agent commits, final status, diff from agent start, and untracked files;
- every agent-run test and Gate command with full output and exit status;
- first and final agent-emitted manifests, where present;
- pull-request details and checks exactly as the agent left them, where present.

Missing evidence stays missing. Do not recreate it before this snapshot.

## Reviewer verification

Label this separate from the cold run. Run the repository's documented tests
and the installed Gate using the agent's final configuration. Retain commands,
complete output, exit status, and the resulting manifest. Compare the final
diff and claims with the exact requirement. Record missing configuration or
evidence instead of creating or repairing it.

## Brief debrief

After preserving the cold result, ask the volunteer where intervention was
hardest to avoid and what was hardest to observe. Before revealing expected
results, ask the agent which installed guidance it relied on and what `done`
meant. Keep the answers separate from the cold transcript.

## Interpret the result

**Pass:** the uncoached agent reached an honest done state from a cold setup.
Artifacts agree, tests pass, and reviewer verification confirms the Gate and
manifest match the repository.

**Fail:** the setup was valid, but the agent needed practice-specific coaching,
stopped short, left inconsistent or missing work, failed tests or the Gate, or
claimed checks absent from the evidence.

**Compromised:** contamination, prior context, a repository previously involved
in SpecAssay, a reused requirement, non-stock teaching, volunteer intervention,
an unknown start, or incomplete evidence prevents an answer. Keep the
observations, but do not count the run.

A passing Gate establishes trace structure, not tested behavior. Test output is
separate evidence.

## Clean up

After the evidence is safe, remove the bundle and catalogs:

```bash
specify bundle remove specassay
specify extension catalog remove specassay
specify preset catalog remove specassay
specify bundle catalog remove specassay
```

Archive or delete the fixture, revoke trial-only credentials, and retain or
delete the evidence according to the volunteer's agreement.
