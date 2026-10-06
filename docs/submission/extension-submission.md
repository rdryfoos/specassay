# Extension Submission: specassay-check, v0.5.6

Paste-ready answers, in the form's own order. Nothing on this page is
history or commentary: every line below is a value for this round.

Form: <https://github.com/github/spec-kit/issues/new?template=extension_submission.yml>

Title:

```
[Extension]: Add SpecAssay Check (update to 0.5.6)
```
<!-- specassay:current -->

The filing history for this component lives in
[filing-history.md](filing-history.md).

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
from nothing.

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
Update to the existing entry, which reads 0.5.2. Beyond the version, the download URL and the digest, one declaration changes: requires.tools now gives bash a floor of >=3.2, which is macOS's system bash and the lowest this release supports. provides is unchanged at 5 commands and 1 hook.
```
