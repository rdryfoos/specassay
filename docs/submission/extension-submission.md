# Extension Submission draft — specassay-check

Paste-ready answers for Spec Kit's **Extension Submission** form
(<https://github.com/github/spec-kit/issues/new?template=extension_submission.yml>).
Fields below appear in the form's exact order; copy each answer into the
matching field. Title: `[Extension]: Add specassay-check`.

---

**Extension ID:** `specassay-check`

**Extension Name:** SpecAssay Check

**Version:** 0.3.1

**Description:**
Gate 2 refuses silent gaps and emits a trace-manifest (`trace-manifest.json`).

**Author:** Rik Dryfoos / Dryfoos Consulting

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-check-0.3.1.zip

**License:** MIT

**Homepage (optional):** https://www.specassay.com

**Documentation URL (optional):**
https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md

**Changelog URL (optional):**
https://github.com/rdryfoos/specassay/blob/main/CHANGELOG.md

**Required Spec Kit Version:** >=0.14.0

**Required Tools (optional):**

```
- bash — required (the Gate script)
- python3 (>=3.8, standard library only) — required (manifest emission and Thread Report CI tooling)
```

**Number of Commands:** 1

**Number of Hooks (optional):** 1

**Tags:** traceability, gate, ci, governance, sdd

**Key Features:**

```
- Refuses silent acceptance-criterion gaps, invented IDs, and registry/specs/tasks drift
- Emits trace-manifest.json on every run — including refusals — so the evidence trail survives failure
- Honest debt (tracked-debt) and planned work (backlog) pass and stay visible
- Thread Report: one CI briefing per PR — what moved on the thread, the touched story end to end, and changed files that sit off the thread
- Restated-intent detection with graded re-confirm hints
- Optional human-tick gates (offthread_ack / intent_ack) enforced via a specassay/ack commit status
```

**Testing Checklist:** tick all five — evidence for each is in
[test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md).

**Submission Requirements:** tick all six.

**Testing Details:**

```
**Tested on:**
- Linux (containerized), Spec Kit CLI `specify 0.16.3.dev0` (installed from main)

**Test project:**
- A clean `specify init` project (install-path evidence: https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md)
- HomesFlow, a real example app (https://github.com/rdryfoos/HomesFlow) — real registry, ~81-row trace-manifest

**Test scenarios:**
1. Added the hosted install-allowed catalogs and installed by ID in a clean project
2. Ran /speckit.specassay-check.gate on a green project (passes, emits manifest)
3. Ran it on a broken thread (refuses, still emits manifest)
4. Live CI demos on the repository: PR #1 (green Thread Report), PR #2 (refusal), PR #4 and #5 (restated intent)
```

**Example Usage:**

```bash
# Install extension
specify extension add specassay-check --from https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-check-0.3.1.zip

# Use the command (in your integration, e.g. Claude)
/speckit.specassay-check.gate
# → refuses silent gaps; writes trace-manifest.json either way
```

**Proposed Catalog Entry:**

```json
{
  "specassay-check": {
    "name": "SpecAssay Check",
    "id": "specassay-check",
    "version": "0.3.1",
    "description": "Gate 2 refuses silent gaps and emits a trace-manifest (`trace-manifest.json`).",
    "author": "Rik Dryfoos / Dryfoos Consulting",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-check-0.3.1.zip",
    "repository": "https://github.com/rdryfoos/specassay",
    "homepage": "https://www.specassay.com",
    "documentation": "https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md",
    "license": "MIT",
    "category": "visibility",
    "effect": "read-write",
    "requires": {
      "speckit_version": ">=0.14.0"
    },
    "provides": {
      "commands": 1,
      "hooks": 1
    },
    "tags": ["traceability", "gate", "ci", "governance", "sdd"],
    "verified": false
  }
}
```

*(kept in sync with [`catalogs/extensions.json`](https://github.com/rdryfoos/specassay/blob/main/catalogs/extensions.json), which the catalogs point installers at)*

**Additional Context:**

```
The emitted trace-manifest is deliberately vendor-neutral (`format` + `schemaVersion` are the contract); a v5 interop revision is in beta with a second emitter (docs/trace-manifest-v5.md). The walkthrough site (https://www.specassay.com) shows the Gate, the Thread Report, and the intent-PR behavior on live PRs in this repository. Pairs with the `specassay` preset, which installs the durable-ID contract the Gate enforces.
```
