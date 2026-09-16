# Preset Submission draft — specassay

Paste-ready answers for Spec Kit's **Preset Submission** form
(<https://github.com/github/spec-kit/issues/new?template=preset_submission.yml>).
Fields below appear in the form's exact order.
Title: `[Preset]: Add specassay`.

**Update note:** this is a version-bump filing, not a first submission.
The original (`v0.3.4`) merged as #4123, closed via #4058; the `v0.4.12`
update filed as #4253 merged as #4256, through the issue route, so that
route is proven for presets now. Per
`docs/submission/CHEATSHEET.md`, presets have no documented issue-based
update path — file a **new** issue (say it updates #4253); if a
maintainer redirects, the documented fallback is a direct PR against
`presets/catalog.community.json` in `github/spec-kit`, bumping `version`
and `download_url` for the `specassay` entry.

**Skipped version, stated plainly:** `v0.4.13` was cut and released but its
submission-form issue was never filed; only the catalog-pointer PR
([github/spec-kit#4448](https://github.com/github/spec-kit/pull/4448)) went out for
it. This 0.5.0 filing therefore carries two versions' worth of change, and the issue
it updates is the last one actually filed, named above — not a 0.4.13 issue, which
does not exist.

---

**Preset ID:** `specassay`

**Preset Name:** SpecAssay

**Version:** 0.5.0

**Description:**
Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec,
tasks, and constitution templates.

**Author:** Rik Dryfoos

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.5.0/specassay-preset-0.5.0.zip

**Digest (sha256):** `d5e4e75b3f07c0555ffb2fc318a6a5c308126ef73a4df1f0b8241b3da9fc2a8b`
*(read from the release asset itself — `gh api repos/rdryfoos/specassay/releases/tags/v0.5.0` — then independently re-verified by
downloading the published zip and hashing it locally, and a third time by unzipping it and
reading the version the manifest inside actually declares; see `docs/submission/test-evidence.md`.)*

**Documentation URL:**
https://github.com/rdryfoos/specassay/blob/main/presets/specassay/README.md
*(preset-scoped README; contains the `specify preset add --from <download-url>`
command the form requires — checked directly and it correctly names the
`v0.4.13` asset, not an older one; checked inside the published zip, not the source tree)*

**License:** MIT

**Required Spec Kit Version:** >=0.14.0

**Required Extensions (optional):** *(leave empty — works standalone; pairs
with `specassay-check`, noted under Key Features)*

**Templates Provided:**

```
- spec-template.md — append: inherited durable IDs (US-/FR-/NFR-/AC-) and a risk table traced to FR/AC IDs
- tasks-template.md — append: `Carries:` required on every task
- constitution-template.md — append: End-to-End Traceability article and the SpecAssay vocabulary
```

**Commands Provided:**

```
None
```

**Number of Scripts (optional):** *(leave empty)*

**Tags:** traceability, durable-ids, governance, sdd

**Key Features:**

```
- Durable IDs minted once at spec time and inherited downstream, never re-derived
- `Carries:` marks connect every open task to the intent it serves
- Constitution vocabulary article is self-sufficient (maker's mark/@covers, Carries:, anointed backlog rows)
- Pure `append` strategy — layers onto stock Spec Kit templates without replacing the workflow
- Pairs with the specassay-check extension, which enforces this contract at the Gate
```

**Testing Checklist:** tick all four — install and template-resolution
evidence is in
[test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md),
which now also verifies the downloaded preset zip's sha256 against the
release's own published digest; the real-project run is HomesFlow
(<https://github.com/rdryfoos/HomesFlow>).

**Submission Requirements:** tick all five.

*(This form has no Testing Details, Example Usage, or Proposed Catalog Entry
fields. For reference, the live catalog entry is the `specassay` object in
[`catalogs/presets.json`](https://github.com/rdryfoos/specassay/blob/main/catalogs/presets.json).)*
