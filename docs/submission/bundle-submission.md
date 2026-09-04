# Bundle Submission draft — specassay

Paste-ready answers for Spec Kit's **Bundle Submission** form
(<https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml>).
Fields below appear in the form's exact order.
Title: `[Bundle]: Add specassay`.

**Update note:** this is a version-bump filing, not a first submission.
The original (`v0.3.4`) merged as #4125, closed via #4059; the `v0.4.12`
update filed as #4255 merged as #4257. Per
`docs/submission/CHEATSHEET.md`, file a **new** issue (say it updates
#4255), after the extension and preset issues for this version exist, and
reference both by number in Additional Context, below.

---

**Bundle ID:** `specassay`

**Bundle Name:** SpecAssay

**Version:** 0.4.13

**Role or Team:** developer

**Description:**
Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and
trace-manifest emission.

**Author:** Rik Dryfoos

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.4.13/specassay-0.4.13.zip

**Digest (sha256):** `8529e8b7542a712542321856368b4f3d7f2f820f98350f7c7f7115670005f18d`
*(from the release asset itself — `gh api repos/rdryfoos/specassay/releases/tags/v0.4.13`
— and independently re-verified by downloading the zip and hashing it locally;
see `docs/submission/test-evidence.md`.)*

**Documentation URL:**
https://github.com/rdryfoos/specassay/blob/main/README.md

**License:** MIT

**Required Spec Kit Version:** >=0.14.0

**Integration Target (optional):** *(leave empty — integration-agnostic)*

**Components Provided:**

```
- extensions: specassay-check@0.4.13
- presets: specassay@0.4.13
```

**Required Component Catalogs:**

```
- Extensions: https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json
- Presets: https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json
```

**Tags:** traceability, governance, durable-ids, gate, sdd

**Key Features:**

```
- Installs the durable-ID contract (preset) and the Gate that enforces it (extension) as one stack
- Gate 2 refuses silent acceptance-criterion gaps; every run emits trace-manifest.json, including refusals
- Thread Report: one CI briefing per PR, with restated-intent detection and optional human-ack gates
- Components pinned to release-tested versions; the artifact is built by `specify bundle build` in CI through these same catalogs
- New in 0.4.13: the Gate talks a first-time installer through its own state (empty-registry on-ramp, Python detected as python3 or python, config state reported every run); since 0.4.12: --matrix, --portfolio, the retired status, derived parentage, and the dig archaeology command
- New in 0.4.x: uncovered-proof (report-only, ratcheted to blocking per project), domain-scoped orphan checks, and loud refusal on malformed config instead of a silent no-op
```

**Testing Checklist:** tick all seven — the full transcript is
[test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md)
(digest check, validate, build, clean-project install by bundle ID
through the install-allowed catalog stack, and a real Gate run).

**Submission Requirements:** tick all six.

**Testing Details:**

```
**Tested on:**
- macOS, Spec Kit CLI `specify 0.15.3.dev0`

**Test project:** clean `specify init` project; full transcript in
https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md

**Test scenarios:**
1. Downloaded the three release assets directly and verified their sha256 against the digests GitHub's API reports for the same release
2. Added the three hosted catalogs (extensions, presets, bundles) as install-allowed
3. `specify bundle validate --path <repo>` at the exact tagged commit (`git describe --tags --exact-match HEAD` → `v0.4.13`) — valid
4. `specify bundle build --path <repo>` — produces the submitted artifact (same command CI runs for releases)
5. `specify bundle install specassay` by ID from the catalog stack in the clean project — 2 components installed, both reporting v0.4.13
6. Verified with `specify bundle list`, `specify extension list`, `specify preset list`
7. Ran the installed Gate on the fresh project (real, loud FAIL — no registry minted yet — trace-manifest still written) and on a real project, HomesFlow (https://github.com/rdryfoos/HomesFlow) — ~81-row trace-manifest
```

**Example Usage:**

```bash
# Add the component catalogs, then the bundle catalog (all install-allowed)
specify extension catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json
specify preset catalog add --name specassay --install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json
specify bundle catalog add --id specassay --policy install-allowed \
  https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json

# Install by bundle ID
specify bundle install specassay

# Or install the downloaded artifact directly
curl -L -o specassay-0.4.13.zip https://github.com/rdryfoos/specassay/releases/download/v0.4.13/specassay-0.4.13.zip
specify bundle install ./specassay-0.4.13.zip
```

**Proposed Catalog Entry:**

```json
{
  "specassay": {
    "name": "SpecAssay",
    "id": "specassay",
    "version": "0.4.13",
    "role": "developer",
    "description": "Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and trace-manifest emission.",
    "author": "Rik Dryfoos",
    "license": "MIT",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.4.13/specassay-0.4.13.zip",
    "repository": "https://github.com/rdryfoos/specassay",
    "requires": {
      "speckit_version": ">=0.14.0"
    },
    "provides": {
      "extensions": 1,
      "presets": 1,
      "steps": 0,
      "workflows": 0
    },
    "tags": ["traceability", "governance", "durable-ids", "gate", "sdd"],
    "verified": false
  }
}
```

*(kept in sync with [`catalogs/bundles.json`](https://github.com/rdryfoos/specassay/blob/main/catalogs/bundles.json);
paste it verbatim under the top-level `bundles` object)*

**Additional Context:**

```
Updates #4255 (closed, merged as #4257 at v0.4.12; the original #4059 merged as #4125 at v0.3.4). Component submissions for the two bundled components at this version, each itself an update to its own closed 0.4.12 issue: the extension issue (updates #4252) and the preset issue (updates #4253), filed first and referenced here by number.

The emitted trace-manifest is deliberately vendor-neutral (`format` + `schemaVersion` are the contract); a v5 interop revision is in beta with a second emitter (docs/trace-manifest-schema.md). The walkthrough site (https://www.specassay.com) shows the Thread Report and intent-PR behavior on live PRs in this repository.
```
