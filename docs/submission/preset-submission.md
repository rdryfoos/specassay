# Preset Submission draft — specassay

Paste-ready answers for Spec Kit's **Preset Submission** form
(<https://github.com/github/spec-kit/issues/new?template=preset_submission.yml>).
Fields below appear in the form's exact order; copy each answer into the
matching field. Title: `[Preset]: Add SpecAssay (update to 0.5.2)`.
<!-- specassay:current -->

## Filing history <!-- specassay:stale-ok which issue numbers the past filings got; the numbers are the point and do not move -->

**Refused 2026-09-23 on the default-branch manifest mismatch, and superseded.** The validator read `bundle.yml` on `main`, which v0.5.2 had moved to 0.5.2, against a submission filed at 0.5.1, and asked for the 0.5.2 release with matching artifact and metadata. #4691 was pre-empted rather than left to fail the same way. The filing moves to 0.5.2 with the catalogs.

**Refiled 2026-09-23 as [github/spec-kit#4691](https://github.com/github/spec-kit/issues/4691), superseding #4650.** #4650 failed on the Documentation URL and the validator's fetch; see the CHEATSHEET's
**v0.5.1 refiled** section for the run IDs and what each one meant. The fields
below are what #4691 carries.

**Filed 2026-09-20 as [github/spec-kit#4650](https://github.com/github/spec-kit/issues/4650).**
A version-bump filing. The `v0.4.12` update was filed as #4253 and merged as
catalog PR #4256, and #4650 says in its body that it updates #4253.

**The issue route works for presets.** An earlier reading of this file hedged
that `presets/PUBLISHING.md` documented only a direct catalog PR and that the
issue route might be redirected. That hedge is withdrawn: the issue route has now
carried the preset three times running, and the direct-PR alternative is the one
that gets closed. See the CHEATSHEET's **v0.5.1 filed** section.

**Two skipped versions, stated plainly.** Neither `v0.4.13` nor `v0.5.0` was ever
filed, so #4650 carries three releases of change.

---

**Preset ID:** `specassay`

**Preset Name:** SpecAssay

**Version:** 0.5.2

**Description:**

```
Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec, tasks, and constitution templates.
```

**Author:** Rik Dryfoos

**Repository URL:** <https://github.com/rdryfoos/specassay>

**Download URL:**

```
https://github.com/rdryfoos/specassay/releases/download/v0.5.2/specassay-preset-0.5.2.zip
```

**Documentation URL:**

```
https://github.com/rdryfoos/specassay/blob/main/presets/specassay/README.md
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

**Required Extensions (optional):**

```
specassay-check (>=0.5.2) - optional. The preset writes the vocabulary; the
extension enforces it. The templates are useful without it, but nothing refuses
a silent gap until the extension is installed.
```

**Templates Provided:**

```
3 - spec-template.md, tasks-template.md, constitution-template.md
```

**Commands Provided:** 0

**Number of Scripts (optional):** 0

**Tags:**

```
traceability, durable-ids, governance, sdd
```

**Key Features:**

```
- Spec template inherits durable IDs from the registry rather than inventing new ones per spec
- Tasks template carries a `**Carries**:` line, the declaration that binds a task to the IDs it serves
- Constitution template carries the end-to-end traceability article as a non-negotiable
- Append strategy at priority 10, so it layers onto stock Spec Kit templates rather than replacing them

Update to an existing entry. Replaces #4691 which was filed at 0.5.1 before v0.5.2 shipped.

Tested on Spec Kit 1.0.5, Linux, 2026-09-23, against the published v0.5.2 asset:

  $ specify preset add specassay --from https://github.com/rdryfoos/specassay/releases/download/v0.5.2/specassay-preset-0.5.2.zip
  Preset 'SpecAssay' v0.5.2 installed (priority 10)

  $ specify preset list
  SpecAssay (specassay) v0.5.2 - enabled - priority 10
    Templates: 3

All three templates resolve, and the tasks template carries its `Carries`
vocabulary intact after installation.

sha256, computed from the published v0.5.2 assets on 2026-09-23:
  9920daf8b7ebe2d5e0d5e723409719afeaaa7c59788a6f3ecda67e2f7543d0b9  specassay-preset-0.5.2.zip

Companion issues: the extension (updates #4252) and the bundle (updates #4255).
```

**Testing Checklist:** tick all 4.

**Submission Requirements:** tick all 5. The linked README carries a working
`specify preset add --from <download-url>` line using the exact download URL
above.

---

**Note on this form's shape.** The preset template has no Testing Details,
Example Usage or Proposed Catalog Entry field, unlike the extension and bundle
templates. The receipts that would go in Testing Details are folded into Key
Features above, which is the only free-text field that accepts them.
