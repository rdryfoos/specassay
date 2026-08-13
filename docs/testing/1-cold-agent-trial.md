# Cold-agent trial

This prospective trial asks whether stock Spec Kit plus the public SpecAssay
bundle can guide a genuinely cold agent through one new plain-language
requirement. It is a runbook, not evidence, and provides no fixture, domain, or
feature.

## Prerequisites

- After receiving this runbook, the volunteer independently chooses or
  creates a codebase that has never been touched by SpecAssay.
- Within that codebase, the volunteer chooses a small plain-language
  requirement that has not appeared in SpecAssay development, documentation,
  examples, or prior trials.
  Record its exact wording. This runbook does not prescribe its domain or
  feature.
- Stock [GitHub Spec Kit](https://github.com/github/spec-kit) and a `specify`
  CLI that supports presets, extensions, and bundles.
- Any credentials required by the agent's normal workflow, plus an evidence
  directory outside the fixture.
- A fresh agent session with no prior exposure to the chosen codebase,
  SpecAssay, or any prior trial through memory, rules, history, or transcripts.

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
   review, and results. A clean grep does not prove absence. The volunteer must
   attest that the repository was never involved in SpecAssay development and
   that the requirement is new and independently chosen. If either check
   fails, choose a different repository or requirement and rebuild the fixture.
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

## Run the trial

Open the recorded agent-start revision in the fresh session and send only:

> Find the newly added plain-language requirement and complete it using the repository's normal workflow.

Do not reveal this runbook, expected artifacts, commands, identifiers, or pass
criteria. Do not coach, correct, or redirect the agent.

Answer only access or environment questions required to continue. Preserve
each question and answer verbatim. If an answer teaches the practice under
test, mark the trial compromised. Stop when the agent says it is done or
blocked, and preserve that state before any repair or rerun.

## Return this evidence package

- The repository URL, source commit, exact requirement, preflight record,
  volunteer attestation, stock Spec Kit command, version, and agent-start
  revision.
- The complete transcript, including tool calls, output, errors, and final
  response.
- Agent commits, final status, diff from agent start, and untracked files.
- Every agent-run test and Gate command, with full output and exit status.
  State plainly if none ran.
- The emitted `trace-manifest.json`, or a note that none was emitted.

Do not polish the result before collecting it. Redact credentials and unrelated
account details only in a separate sharing copy.

## Interpret the result

**Pass:** the setup was cold and the uncoached agent reached an honest done
state. Its artifacts agree, its tests pass, and the Gate output and
trace-manifest agree with the repository.

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
