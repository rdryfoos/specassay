# Preset Submission: specassay, v0.5.6

Paste-ready answers, in the form's own order. Nothing on this page is
history or commentary: every line below is a value for this round.

Form: <https://github.com/github/spec-kit/issues/new?template=preset_submission.yml>

Title:

```
[Preset]: Add SpecAssay (update to 0.5.6)
```
<!-- specassay:current -->

The filing history for this component lives in
[filing-history.md](filing-history.md).

---

**Preset ID:** `specassay`

**Preset Name:** SpecAssay

**Version:** 0.5.6

**Description:**

```
Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec, tasks, and constitution templates.
```

**Author:** Rik Dryfoos

**Repository URL:** <https://github.com/rdryfoos/specassay>

**Download URL:**

```
https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-preset-0.5.6.zip
```

**Documentation URL:**

```
https://github.com/rdryfoos/specassay/blob/main/presets/specassay/README.md
```

**License:** MIT

**Required Spec Kit Version:** `>=0.14.0,<2.0.0`

**Required Extensions (optional):**

```
specassay-check
```

`preset.yml` declares this dependency by id, with no version constraint, so the
value above is the whole of it. The preset writes the vocabulary and the
extension enforces it: the templates are useful on their own, and nothing
refuses a silent gap until the extension is installed, which is why the
documented install is the bundle.

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

Update to the existing entry, which reads 0.5.2, and carries four releases of
change: 0.5.3, 0.5.4 and 0.5.5 were never filed.

Tested on Spec Kit 1.0.4 pinned from its own tag, Linux, 2026-10-06, against
the published v0.5.6 asset:

  $ specify preset add specassay --from https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-preset-0.5.6.zip
  ✓ Preset 'SpecAssay' v0.5.6 installed (priority 10)
      specassay-check is not installed

  $ specify preset list
    SpecAssay (specassay) v0.5.6 — enabled — priority 10
      Templates: 3

All three templates resolve, and the tasks template carries its `Carries`
vocabulary intact after installation. The second line of the install is the
preset naming the extension it depends on, which is why the documented install
is the bundle rather than the preset alone.

sha256. The release page reports it, and the downloaded archive computes to the
same thing, 2026-10-06:
  6f70580f9b349df8b850f31cf02601a24263b9faaa79c48b14a6d2ff50c1260d  specassay-preset-0.5.6.zip
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
