# Extension Submission draft — specassay-check

Paste-ready answers for Spec Kit's **Extension Submission** form
(<https://github.com/github/spec-kit/issues/new?template=extension_submission.yml>).
Fields below appear in the form's exact order; copy each answer into the
matching field. Title: `[Extension]: Add specassay-check`.

**Update note:** this is a version-bump filing, not a first submission.
The original (`v0.3.4`) merged as #4113, closed via #4057; the `v0.4.12`
update merged as #4254, filed as #4252. Per
`docs/submission/CHEATSHEET.md`, this must go out as a **new** issue, not
an edit to a closed one. Say in the new issue that it updates #4252.

---

**Extension ID:** `specassay-check`

**Extension Name:** SpecAssay Check

**Version:** 0.4.13

**Description:**
Gate 2 refuses silent gaps and emits a trace-manifest (`trace-manifest.json`).

**Author:** Rik Dryfoos

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.4.13/specassay-check-0.4.13.zip

**Digest (sha256):** `d7ac14c271b99aff0b649def9c3444b6e03090649df43ea2b9c3949ded91ed9f`
*(from the release asset itself — `gh api repos/rdryfoos/specassay/releases/tags/v0.4.13`
— and independently re-verified by downloading the zip and hashing it locally;
see `docs/submission/test-evidence.md`.)*

**License:** MIT

**Homepage (optional):** https://www.specassay.com

**Documentation URL (optional):**
https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md

**Changelog URL (optional):**
https://github.com/rdryfoos/specassay/blob/main/CHANGELOG.md

**Required Spec Kit Version:** >=0.14.0

**Required Tools (optional):**

```
- bash - required
- python3 (>=3.8) - required
```

**Number of Commands:** 5

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
- New in 0.4.13: green on an empty registry now prints the on-ramp to a first ID (greenfield and brownfield, runnable commands) instead of a bare OK; Python 3 is detected as python3 or python (Windows Git Bash works) with a one-line install hint when neither is usable; the Gate reports its own config state on its first lines every run
- Since 0.4.12: --matrix (coverage.md + coverage.svg), --portfolio (portfolio-snapshot.md), a genuine `retired` status from dated Retires: records, parent edges derived from registry nesting with a composition rollup, and `dig` (archaeology mode: a no-LLM candidate registry from tests, routes, and docs, written only to dig-report.json)
- New in 0.4.x: uncovered-proof (Rule 4a) catches a real, passing, named test whose ID never appears in an @covers line — report-only by default, with a documented per-project ratchet to make it blocking; orphan-covers/orphan-test are now domain-scoped so a doc quoting another project's real @covers line as an example doesn't misread as a local orphan; malformed src_globs/test_globs config now refuses loudly instead of silently matching nothing
```

**Testing Checklist:** tick all five — evidence for each is in
[test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md).

**Submission Requirements:** tick all six.

**Testing Details:**

```
**Tested on:**
- macOS, Spec Kit CLI `specify 0.15.3.dev0`

**Test project:**
- A clean `specify init` project (install-path evidence, including a
  sha256 digest check against the published release asset:
  https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md)
- HomesFlow, a real example app (https://github.com/rdryfoos/HomesFlow) — real registry, ~81-row trace-manifest

**Test scenarios:**
1. Added the hosted install-allowed catalogs and installed by ID in a clean project; verified the installed extension reports v0.4.13
2. Verified the downloaded release zip's sha256 matches the digest GitHub's API reports for the same release asset
3. Ran /speckit.specassay-check.gate on a green project (passes, emits manifest)
4. Ran it on a broken thread (refuses, still emits manifest)
5. Live CI demos on the repository: PR #1 (green Thread Report), PR #2 (refusal), PR #4 and #5 (restated intent)
```

**Example Usage:**

```bash
# Install extension
specify extension add specassay-check --from https://github.com/rdryfoos/specassay/releases/latest/download/specassay-check.zip
# (version-agnostic: redirects to the newest release; the CLI asks once to confirm a URL install)

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
    "version": "0.4.13",
    "description": "Gate 2 refuses silent gaps and emits a trace-manifest (`trace-manifest.json`).",
    "author": "Rik Dryfoos",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.4.13/specassay-check-0.4.13.zip",
    "repository": "https://github.com/rdryfoos/specassay",
    "homepage": "https://www.specassay.com",
    "documentation": "https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md",
    "license": "MIT",
    "category": "visibility",
    "effect": "read-write",
    "requires": {
      "speckit_version": ">=0.14.0",
      "tools": [
        { "name": "bash", "required": true },
        { "name": "python3", "version": ">=3.8", "required": true }
      ]
    },
    "provides": {
      "commands": 5,
      "hooks": 1
    },
    "tags": ["traceability", "gate", "ci", "governance", "sdd"],
    "verified": false
  }
}
```

*(kept in sync with [`catalogs/extensions.json`](https://github.com/rdryfoos/specassay/blob/main/catalogs/extensions.json), which the catalogs point installers at — pasted verbatim from that file, not retyped)*

**Additional Context:**

```
Updates #4252 (closed, merged as #4254 at v0.4.12; the original #4057 merged as #4113 at v0.3.4). The emitted trace-manifest is deliberately vendor-neutral (`format` + `schemaVersion` are the contract); a v5 interop revision is in beta with a second emitter (docs/trace-manifest-schema.md). The walkthrough site (https://www.specassay.com) shows the Gate, the Thread Report, and the intent-PR behavior on live PRs in this repository. Pairs with the `specassay` preset, which installs the durable-ID contract the Gate enforces.
```
