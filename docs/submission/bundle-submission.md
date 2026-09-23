# Bundle Submission draft — specassay

Paste-ready answers for Spec Kit's **Bundle Submission** form
(<https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml>).
Fields below appear in the form's exact order; copy each answer into the
matching field. Title: `[Bundle]: Add SpecAssay (update to 0.5.2)`.
<!-- specassay:current -->

File this **third**, after the extension and preset issues, and name both in it.

## Filing history <!-- specassay:stale-ok which issue numbers the past filings got; the numbers are the point and do not move -->

**Refused 2026-09-23 on the default-branch manifest mismatch, and superseded.** The validator read `bundle.yml` on `main`, which v0.5.2 had moved to 0.5.2, against #4692 filed at 0.5.1, and asked for the 0.5.2 release with matching artifact and metadata. This is the issue that caught it; #4690 and #4691 were pre-empted. The filing moves to 0.5.2 with the catalogs.

**Refiled 2026-09-23 as [github/spec-kit#4692](https://github.com/github/spec-kit/issues/4692), superseding #4651,** after the extension (#4690) and the preset (#4691).
#4651 failed on the version-string mismatch and the validator's fetch; see the
CHEATSHEET's **v0.5.1 refiled** section for the run IDs and what each one meant.
The fields below are what #4692 carries.

**Filed 2026-09-20 as [github/spec-kit#4651](https://github.com/github/spec-kit/issues/4651),**
after the extension (#4649) and the preset (#4650). A version-bump filing: the
`v0.4.12` update was filed as #4255 and merged as catalog PR #4257, and #4651
says in its body that it updates #4255.

**Two skipped versions, stated plainly.** Neither `v0.4.13` nor `v0.5.0` was ever
filed, so #4651 carries three releases of change.

---

**Bundle ID:** `specassay`

**Bundle Name:** SpecAssay

**Version:** 0.5.2

**Role or Team:** developer

**Description:**

```
Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and trace-manifest emission.
```

**Author:** Rik Dryfoos

**Repository URL:** <https://github.com/rdryfoos/specassay>

**Download URL:**

```
https://github.com/rdryfoos/specassay/releases/download/v0.5.2/specassay-0.5.2.zip
```

**Documentation URL:**

```
https://github.com/rdryfoos/specassay/blob/main/README.md
```

**License:** MIT

**Required Spec Kit Version:** `>=0.14.0,<2.0.0`

#### Declared range, as observed 2026-09-20

The three manifests shipped inside the zips declare
`>=0.14.0,<2.0.0`, while `catalogs/*.json` publish `>=0.14.0`, and the issues
filed today inherited the catalogs' string. The upper bound is the honest one:
a catalog that claims a wider range than the zip inside it is the exact failure
the CHEATSHEET's sweep rule exists to prevent. Named here rather than quietly
corrected, because fixing `catalogs/*.json` is a release artifact and is not
this PR's to change.

**Closed 2026-09-23 by Rik's ruling.** The catalogs align at v0.5.2; until that
cut, an issue is written from the manifests and every declaration inside one
issue must match. Recorded because a divergence inside a single issue is what
failed #4651.

**Integration Target (optional):** leave empty. The bundle is
integration-agnostic.

**Components Provided:**

```
- extensions: specassay-check@0.5.2
- presets: specassay@0.5.2
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
`specify extension add ... --from <url>` and `specify preset add ... --from <url>`,
which was also tested on 2026-09-20.
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
This updates the existing catalog entry from 0.4.12 to 0.5.2, superseding
issue #4255 (merged as catalog PR #4257). Neither v0.4.13 nor v0.5.0 was ever
filed, so this carries three releases of change.

Tested on: Linux, Spec Kit 1.0.5, Python 3.11.15, on 2026-09-23, against the
published v0.5.2 assets in a clean project.

sha256 of the submitted artifact, computed from the published v0.5.2 assets on 2026-09-23:

  $ curl -fsSL -O https://github.com/rdryfoos/specassay/releases/download/v0.5.2/specassay-0.5.2.zip
  $ sha256sum specassay-0.5.2.zip
  a9acd0848132bee975be7ca6759a531ff02b736c99a98b1bc4e7d8da90da7c82  specassay-0.5.2.zip

Component digests, same run:
  f481c6794d0cffc6d532721c1acc378287ba291b3e74dbe1e54eef083d1e7a20  specassay-check-0.5.2.zip
  9920daf8b7ebe2d5e0d5e723409719afeaaa7c59788a6f3ecda67e2f7543d0b9  specassay-preset-0.5.2.zip

All three match the digests this project recorded independently at release on
2026-09-17.

Test scenarios, clean project:

  $ specify init . --here --force --non-interactive --integration claude
  $ <the three catalog add commands above>
  $ specify bundle install specassay
  Installed 'specassay' (2 added, 0 already present).

  $ specify bundle list
  specassay v0.5.2 (2 components, installed 2026-09-23T17:41:00Z)
  $ specify preset list
  SpecAssay (specassay) v0.5.2 - enabled - priority 10
  $ specify extension list
  SpecAssay Check (v0.5.2)

All three resolve 0.5.2 on the first try. A thread was then driven from an
empty registry through mint, the Gate's honest refusal, and a clear to green as
tracked debt.
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
    "version": "0.5.2",
    "role": "developer",
    "description": "Durable-ID promotion for stock Spec Kit: templates, Gate 2 refusal, and trace-manifest emission.",
    "author": "Rik Dryfoos",
    "license": "MIT",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.5.2/specassay-0.5.2.zip",
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
    "tags": ["traceability", "governance", "durable-ids", "gate", "sdd"],
    "verified": false
  }
}
```

**Additional Context:**

```
Update to an existing entry. Replaces #4692 which was filed at 0.5.1 before v0.5.2 shipped.
```
