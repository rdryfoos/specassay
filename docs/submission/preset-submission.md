# Preset Submission draft — specassay

Paste-ready answers for Spec Kit's **Preset Submission** form
(<https://github.com/github/spec-kit/issues/new?template=preset_submission.yml>).
Fields below appear in the form's exact order.
Title: `[Preset]: Add specassay`.

---

**Preset ID:** `specassay`

**Preset Name:** SpecAssay

**Version:** 0.3.4

**Description:**
Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec,
tasks, and constitution templates.

**Author:** Rik Dryfoos

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.3.4/specassay-preset-0.3.4.zip

**Documentation URL:**
https://github.com/rdryfoos/specassay/blob/main/presets/specassay/README.md
*(preset-scoped README; contains the `specify preset add --from <download-url>`
command the form requires)*

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
[test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md);
the real-project run is HomesFlow
(<https://github.com/rdryfoos/HomesFlow>).

**Submission Requirements:** tick all five.

*(This form has no Testing Details, Example Usage, or Proposed Catalog Entry
fields. For reference, the live catalog entry is the `specassay` object in
[`catalogs/presets.json`](https://github.com/rdryfoos/specassay/blob/main/catalogs/presets.json).)*
