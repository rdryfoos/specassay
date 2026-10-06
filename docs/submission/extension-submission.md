# Extension Submission draft — specassay-check

Paste-ready answers for Spec Kit's **Extension Submission** form
(<https://github.com/github/spec-kit/issues/new?template=extension_submission.yml>).
Fields below appear in the form's exact order; copy each answer into the
matching field. Title: `[Extension]: Add SpecAssay Check (update to 0.5.6)`.
<!-- specassay:stale-ok the 0.5.2 round these forms served landed 2026-09-24 (#4717, #4735, #4737); these values are the record of what was filed and merged, not a claim about the version being cut -->

## Filing history <!-- specassay:stale-ok which issue numbers the past filings got; the numbers are the point and do not move -->

**Prepared 2026-10-06 at 0.5.6, not yet filed.** The fields below carry 0.5.6, read from the published release and from `catalogs/extensions.json`. Filing is a human step: it needs an issue opened on `github/spec-kit`, which the room that prepared this could not reach from its own session. It updates #4711.

**Landed 2026-09-24.** #4711 was closed by [github/spec-kit#4735](https://github.com/github/spec-kit/pull/4735), "[extension] Update SpecAssay Check extension to v0.5.2", opened by the submission workflow and merged the same day by KSchlobohm with all 17 checks passing. `extensions/catalog.community.json` on `main` now reads 0.5.2. No comment was ever posted on the issue; the verdict arrived as labels and a generated pull request.

**Filed 2026-09-23 at 0.5.2 as [github/spec-kit#4711](https://github.com/github/spec-kit/issues/4711), superseding #4690.** The fields below are what #4711 carries.

**Refused 2026-09-23 on the default-branch manifest mismatch, and superseded.** The validator read `bundle.yml` on `main`, which v0.5.2 had moved to 0.5.2, against a submission filed at 0.5.1, and asked for the 0.5.2 release with matching artifact and metadata. #4690 was pre-empted rather than left to fail the same way. The filing moves to 0.5.2 with the catalogs.

**Refiled 2026-09-23 as [github/spec-kit#4690](https://github.com/github/spec-kit/issues/4690), superseding #4649.** #4649 failed on the validator's fetch alone, twice; see the CHEATSHEET's
**v0.5.1 refiled** section for the run IDs and what each one meant. #4690
carried these fields at 0.5.1.

**Filed 2026-09-20 as [github/spec-kit#4649](https://github.com/github/spec-kit/issues/4649).**
A version-bump filing, not a first submission. The original (`v0.3.4`) merged as
#4113, closed via #4057; the `v0.4.12` update merged as #4254, filed as #4252.
Per the Extension Publishing Guide's "Updating an Existing Extension", an update
goes out as a **new** issue, never an edit to a closed one, and #4649 says in its
body that it updates #4252.

**Two skipped versions, stated plainly.** Neither `v0.4.13` nor `v0.5.0` was ever
filed on a submission form, so #4649 carries three releases of change and names
the last issue actually filed rather than a 0.4.13 or 0.5.0 issue, neither of
which exists.

---

**Extension ID:** `specassay-check`

**Extension Name:** SpecAssay Check

**Version:** 0.5.6

**Description:**

```
Gate 2 refuses silent gaps and emits a trace-manifest (`trace-manifest.json`).
```

**Author:** Rik Dryfoos

**Repository URL:** <https://github.com/rdryfoos/specassay>

**Download URL:**

```
https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-check-0.5.6.zip
```

**License:** MIT

**Homepage (optional):** <https://www.specassay.com>

**Documentation URL (optional):**

```
https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md
```

**Changelog URL (optional):**

```
https://github.com/rdryfoos/specassay/blob/main/CHANGELOG.md
```

**Required Spec Kit Version:** `>=0.14.0,<2.0.0`

#### Declared range, as observed 2026-09-20

The three manifests shipped inside the zips declare
`>=0.14.0,<2.0.0`, while `catalogs/*.json` publish `>=0.14.0`, and the issues
filed today inherited the catalogs' string. The upper bound is the honest one:
a catalog that claims a wider range than the zip inside it is the exact failure
the CHEATSHEET's sweep rule exists to prevent. Named here rather than quietly
corrected, because fixing `catalogs/*.json` is a release artifact and is not
this PR's to change.

**Closed 2026-09-23 by Rik's ruling.** The catalogs align at v0.5.6; until that
cut, an issue is written from the manifests and every declaration inside one
issue must match. Recorded because a divergence inside a single issue is what
failed #4651.

**Required Tools (optional):**

```
- bash - required
- python3 (>=3.8) - required
```

**Number of Commands:** 5

**Number of Hooks (optional):** 1

**Tags:**

```
traceability, gate, ci, governance, sdd
```

**Key Features:**

```
- Gate 2 refuses a silent gap: an acceptance criterion with no test and no open tracked-debt task fails the build rather than passing quietly
- Emits trace-manifest.json (v4) and trace-manifest.v5beta.json, one row per registry ID with its status and the evidence behind it
- Five statuses, including `retired` for an intent withdrawn on purpose, so a withdrawal is never mistaken for a gap
- Mints durable IDs at intent and refuses an ID the project's own configured grammar would reject
- Coverage matrix and portfolio snapshot for CI and for cold readers
```

**Testing Checklist:** tick all 5.

**Submission Requirements:** tick all 6.

**Testing Details:**

```
This updates the existing catalog entry from 0.5.2 to 0.5.6. It supersedes
issue #4711, filed at 0.5.2 and merged as catalog PR #4735. Neither v0.5.3 nor
v0.5.4 nor v0.5.5 was ever filed, so this one carries four releases of change.

Tested on: Linux, Spec Kit 1.0.4 pinned from its own tag, Python 3.11.15, on
2026-10-06, against the published v0.5.6 assets in a throwaway project built
from nothing. The >=0.14.0 floor was exercised at v0.5.1 on 2026-09-17: the
bundle installs and the Gate runs on 0.14.0, though that version does not
scaffold the settings file, so the Gate reports `config: MISSING` and continues
on defaults.

sha256 of the submitted archive. The release page reports it, and the downloaded
archive computes to the same thing, 2026-10-06:

  $ curl -fsSL -O https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-check-0.5.6.zip
  $ sha256sum specassay-check-0.5.6.zip
  1f7112e2e550aacc7dd466cc83b315c0d846f318a611fb93c394bde46cea355b  specassay-check-0.5.6.zip

The catalog's digest is load-bearing, not decorative. With one hex character
changed and the catalog served over localhost, the install refuses and names
both digests rather than unpacking anything:

  Error: Integrity check failed for 'specassay-check': the catalog declares
  sha256 0f7112e2..., but the downloaded archive is 1f7112e2.... The archive
  may be corrupted or tampered with.

Test scenarios, run in order on 2026-10-06 in a throwaway project, which is the
same sequence the public quickstart walks a stranger through:

1. Installed as a bundle from the three catalogs:
     $ specify bundle install specassay
     Updated execute permissions on 7 script(s) recursively
     OK Installed 'specassay' (2 added, 0 already present).
     both components report version 0.5.6
2. Wrote the registry from the shipped seed and ran the Gate on it:
     $ bash .../mint-id.sh --init
     wrote PRD.md from the registry seed (64 lines)
     SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
   It passes and says the pass proves nothing, then prints both mint routes.
3. Minted a first ID:
     $ bash .../mint-id.sh AC GREET --authorship case --append "Given a name, ..."
     AC-GREET-10
4. Ran the Gate again. It refuses honestly, which is the intended first red:
     FAIL: registry ID missing from specs: AC-GREET-10
     FAIL: registry ID missing from tasks: AC-GREET-10
     FAIL: silent gap: AC-GREET-10 has no test and no open tracked-debt task
     exit 1
5. Added a spec line and one open task carrying the ID, the documented way to
   clear it without writing code:
     SpecAssay Check (Gate 2): OK (1 registry IDs)
     exit 0, and trace-manifest.json reports AC-GREET-10 as tracked-debt.
6. Wrote the code and a test named for the ID:
     SpecAssay Check (Gate 2): OK (1 registry IDs)
     trace-manifest.json reports AC-GREET-10 as proven.
7. Renamed the test only, leaving the code and the ticked task alone. The test
   suite still passes and the Gate refuses, which is the whole point:
     Ran 1 test in 0.000s
     OK
     FAIL: silent gap: AC-GREET-10 has no test and no open tracked-debt task
     exit 1, and the row reads GAP.
8. Put the name back. Green again, exit 0, the row reads proven.

The extension is also run against its own repository on every pull request, on
Linux and macOS runners, where it currently reports OK on 152 registry IDs.
```

**Example Usage:**

```bash
# Install from the release archive
specify extension add specassay-check --from https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-check-0.5.6.zip

# Mint a durable ID at intent
/speckit.specassay-check.mint AC LOGIN "Given a wrong password, when the user signs in, then the form shows an error and no session starts."

# Run Gate 2; a silent gap fails the build
/speckit.specassay-check.gate
```

**Proposed Catalog Entry:**

```json
{
  "specassay-check": {
    "name": "SpecAssay Check",
    "id": "specassay-check",
    "version": "0.5.6",
    "description": "Gate 2 refuses silent gaps and emits a trace-manifest (`trace-manifest.json`).",
    "author": "Rik Dryfoos",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-check-0.5.6.zip",
    "repository": "https://github.com/rdryfoos/specassay",
    "homepage": "https://www.specassay.com",
    "documentation": "https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md",
    "license": "MIT",
    "category": "visibility",
    "effect": "read-write",
    "requires": {
      "speckit_version": ">=0.14.0,<2.0.0",
      "tools": [
        {
          "name": "bash",
          "required": true,
          "version": ">=3.2"
        },
        {
          "name": "python3",
          "version": ">=3.8",
          "required": true
        }
      ]
    },
    "provides": {
      "commands": 5,
      "hooks": 1
    },
    "tags": [
      "traceability",
      "gate",
      "ci",
      "governance",
      "sdd"
    ],
    "verified": false,
    "created_at": "2026-08-06T00:00:00Z",
    "updated_at": "2026-10-05T00:00:00Z",
    "sha256": "1f7112e2e550aacc7dd466cc83b315c0d846f318a611fb93c394bde46cea355b"
  }
}
```

**Additional Context:**

```
Update to an existing entry. Replaces #4690 which was filed at 0.5.1 before v0.5.6 shipped.
provides.commands moves from 2 to 5; dig, matrix and portfolio shipped after the 0.4.12 entry.
```
