# Bundle Submission draft — specassay

Paste-ready answers for Spec Kit's **Bundle Submission** form
(<https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml>).
Fields below appear in the form's exact order.
Title: `[Bundle]: Add specassay`.

File the [extension](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md)
and [preset](https://github.com/rdryfoos/specassay/blob/main/docs/submission/preset-submission.md)
issues first — the bundle references both (see Additional Context below).

---

**Bundle ID:** `specassay`

**Bundle Name:** SpecAssay

**Version:** 0.3.1

**Role or Team:** developer

**Description:**
Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and
trace-manifest emission.

**Author:** Rik Dryfoos

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-0.3.1.zip

**Documentation URL:**
https://github.com/rdryfoos/specassay/blob/main/README.md

**License:** MIT

**Required Spec Kit Version:** >=0.14.0

**Integration Target (optional):** *(leave empty — integration-agnostic)*

**Components Provided:**

```
- extensions: specassay-check@0.3.1
- presets: specassay@0.2.0
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
```

**Testing Checklist:** tick all seven — the full transcript is
[test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md)
(validate, build, clean-project install by bundle ID through the
install-allowed catalog stack).

**Submission Requirements:** tick all six.

**Testing Details:**

```
**Tested on:**
- Linux (containerized), Spec Kit CLI `specify 0.16.3.dev0` (installed from main)

**Test project:** clean `specify init` project; full transcript in
https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md

**Test scenarios:**
1. Added the three hosted catalogs (extensions, presets, bundles) as install-allowed
2. `specify bundle validate --path <repo>` — valid
3. `specify bundle build --path <repo>` — produces the submitted artifact (same command CI runs for releases)
4. `specify bundle install specassay` by ID from the catalog stack in the clean project — 2 components installed
5. Verified with `specify bundle list`, `specify extension list`, `specify preset list`
6. Ran the installed Gate on a real project (HomesFlow, https://github.com/rdryfoos/HomesFlow) — ~81-row trace-manifest
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
curl -L -o specassay-0.3.1.zip https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-0.3.1.zip
specify bundle install ./specassay-0.3.1.zip
```

**Proposed Catalog Entry:**

```json
{
  "specassay": {
    "name": "SpecAssay",
    "id": "specassay",
    "version": "0.3.1",
    "role": "developer",
    "description": "Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and trace-manifest emission.",
    "author": "Rik Dryfoos",
    "license": "MIT",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-0.3.1.zip",
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
Component submissions for the two bundled components: extension issue #___ and preset issue #___ (fill in after filing those first).

The emitted trace-manifest is deliberately vendor-neutral (`format` + `schemaVersion` are the contract); a v5 interop revision is in beta with a second emitter (docs/trace-manifest-v5.md). The walkthrough site (https://www.specassay.com) shows the Thread Report and intent-PR behavior on live PRs in this repository.
```
