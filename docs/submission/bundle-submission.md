# Bundle Submission: specassay, v0.5.6

Paste-ready answers, in the form's own order. Nothing on this page is
history or commentary: every line below is a value for this round.

Form: <https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml>

Title:

```
[Bundle]: Add SpecAssay (update to 0.5.6)
```
<!-- specassay:current -->

The filing history for this component lives in
[filing-history.md](filing-history.md).

---

**Bundle ID:** `specassay`

**Bundle Name:** SpecAssay

**Version:** 0.5.6

**Role or Team:** developer

**Description:**

```
Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and trace-manifest emission.
```

**Author:** Rik Dryfoos

**Repository URL:** <https://github.com/rdryfoos/specassay>

**Download URL:**

```
https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-0.5.6.zip
```

**Documentation URL:**

```
https://github.com/rdryfoos/specassay/blob/main/README.md
```

**License:** MIT

**Required Spec Kit Version:** `>=0.14.0,<2.0.0`

**Integration Target (optional):** leave empty. The bundle is
integration-agnostic.

**Components Provided:**

```
- extensions: specassay-check@0.5.6
- presets: specassay@0.5.6
- workflows: none
- steps: none
```

**Required Component Catalogs:**

```
The three SpecAssay catalogs, added as install-allowed, because the community
catalog is discovery-only and cannot install:

  specify preset catalog add https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json --name specassay --install-allowed
  specify extension catalog add https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json --name specassay --install-allowed
  specify bundle catalog add https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json --id specassay --policy install-allowed

Both components can alternatively be installed directly with
`specify extension add ... --from <url>` and `specify preset add ... --from <url>`.
```

**Tags:**

```
traceability, governance, durable-ids, gate, sdd
```

**Key Features:**

```
- One install provisions the whole thread: templates that mint durable IDs, and the Gate that refuses a silent gap
- Registry, specs and tasks must agree as an exact set; drift fails rather than passing quietly
- Emits a trace-manifest any viewer can read, so proof is a file rather than a claim
- Components are pinned to matching versions, so a partial upgrade cannot leave the bundle half-resolved
```

**Testing Checklist:** tick all 7.

**Submission Requirements:** tick all 5.

**Testing Details:**

```
This updates the existing catalog entry from 0.5.2 to 0.5.6, superseding
issue #4715 (merged as catalog PR #4737). Neither v0.5.3 nor v0.5.4 nor v0.5.5
was ever filed, so this carries four releases of change.

Tested on: Linux, Spec Kit 1.0.4 pinned from its own tag, Python 3.11.15, on
2026-10-06, against the published v0.5.6 assets in a throwaway project built
from nothing.

sha256 of the submitted artifact. The release page reports it, and the
downloaded archive computes to the same thing, 2026-10-06:

  $ curl -fsSL -O https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-0.5.6.zip
  $ sha256sum specassay-0.5.6.zip
  56d701b47c1482b526dcb27ef4d78a99cb63a1c03ae8cba58097aecba5595e7f  specassay-0.5.6.zip

Component digests, same run, each also matching the release page:
  1f7112e2e550aacc7dd466cc83b315c0d846f318a611fb93c394bde46cea355b  specassay-check-0.5.6.zip
  6f70580f9b349df8b850f31cf02601a24263b9faaa79c48b14a6d2ff50c1260d  specassay-preset-0.5.6.zip

The three unversioned aliases on the same release (specassay.zip,
specassay-check.zip, specassay-preset.zip) carry the same three digests and
the same three sizes, which is what makes them aliases rather than rebuilds.

Test scenarios, run on 2026-10-06 in a throwaway project:

  $ specify init specassay-tour --integration claude --non-interactive
  $ <the three catalog add commands above>
  $ specify bundle install specassay
  Updated execute permissions on 7 script(s) recursively
  OK Installed 'specassay' (2 added, 0 already present).

  $ specify bundle list
  specassay v0.5.6 (2 components, installed 2026-10-06T11:44:33Z)
  $ specify preset list
  SpecAssay (specassay) v0.5.6 — enabled — priority 10
  $ specify extension list
  SpecAssay Check (v0.5.6)

All three resolve 0.5.6 on the first try. A thread was then driven from an
empty registry through the mint, the Gate's honest refusal, a clear to green as
tracked debt, a proof, a deliberate break that left the test suite green while
the Gate refused, and the one-line repair back to green.
```

**Example Usage:**

```bash
# Add the three SpecAssay catalogs as install-allowed (community is discovery-only)
specify preset catalog add https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json --name specassay --install-allowed
specify extension catalog add https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json --name specassay --install-allowed
specify bundle catalog add https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json --id specassay --policy install-allowed

# Install the bundle
specify bundle install specassay

# Mint an ID at intent, then let the Gate refuse anything unproven
/speckit.specassay-check.mint AC LOGIN "Given a wrong password, when the user signs in, then the form shows an error."
/speckit.specassay-check.gate
```

**Proposed Catalog Entry:**

```json
{
  "specassay": {
    "name": "SpecAssay",
    "id": "specassay",
    "version": "0.5.6",
    "role": "developer",
    "description": "Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and trace-manifest emission.",
    "author": "Rik Dryfoos",
    "license": "MIT",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-0.5.6.zip",
    "repository": "https://github.com/rdryfoos/specassay",
    "requires": {
      "speckit_version": ">=0.14.0,<2.0.0"
    },
    "provides": {
      "extensions": 1,
      "presets": 1,
      "steps": 0,
      "workflows": 0
    },
    "tags": [
      "traceability",
      "governance",
      "durable-ids",
      "gate",
      "sdd"
    ],
    "verified": false,
    "sha256": "56d701b47c1482b526dcb27ef4d78a99cb63a1c03ae8cba58097aecba5595e7f"
  }
}
```

**Additional Context:**

```
Update to the existing entry, which reads 0.5.2.
Companion issues: the extension and the preset, filed just before this one; the bundle pins both component versions, so all three land together.
```
