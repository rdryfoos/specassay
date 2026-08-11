# Preset Submission draft — specassay

Paste-ready answers for Spec Kit's **Preset Submission** issue form
(`https://github.com/github/spec-kit/issues/new?template=preset_submission.yml`).

---

**Preset ID:** `specassay`

**Preset Name:** SpecAssay

**Version:** 0.2.0

**Description:**
Appends durable-ID, Carries, and SpecAssay vocabulary onto Spec Kit spec,
tasks, and constitution templates.

**Author:** Rik Dryfoos / Dryfoos Consulting

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-preset-0.2.0.zip

**Documentation URL:**
https://github.com/rdryfoos/specassay/blob/main/PROMOTION-CONTRACT.md

**License:** MIT

**Required Spec Kit Version:** >=0.14.0

**Provides:** 3 templates (spec, tasks, constitution), append strategy —
stock Spec Kit templates stay intact; SpecAssay's durable-ID and `Carries:`
requirements are appended.

**Tags:** traceability, durable-ids, governance, sdd

**What it does:**
Gives every intent a durable ID (`US-`/`FR-`/`NFR-`/`AC-`) minted at intent
time, requires `Carries:` marks on open tasks, and makes the constitution's
vocabulary article self-sufficient (mark/`@covers`, `Carries:`, anointed
backlog). Pairs with the `specassay-check` extension, which enforces the
contract at the Gate.

**Proposed Catalog Entry:**
```json
{
  "specassay": {
    "name": "SpecAssay",
    "id": "specassay",
    "version": "0.2.0",
    "description": "Appends durable-ID and Carries requirements onto Spec Kit spec, tasks, and constitution templates.",
    "author": "Rik Dryfoos / Dryfoos Consulting",
    "repository": "https://github.com/rdryfoos/specassay",
    "download_url": "https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-preset-0.2.0.zip",
    "homepage": "https://github.com/rdryfoos/specassay",
    "documentation": "https://github.com/rdryfoos/specassay/blob/main/PROMOTION-CONTRACT.md",
    "license": "MIT",
    "requires": {
      "speckit_version": ">=0.14.0"
    },
    "provides": {
      "templates": 3,
      "commands": 0
    },
    "tags": [
      "traceability",
      "durable-ids",
      "governance",
      "sdd"
    ],
    "created_at": "2026-08-06T00:00:00Z",
    "updated_at": "2026-08-06T00:00:00Z"
  }
}
```

*(kept in sync with [`catalogs/presets.json`](https://github.com/rdryfoos/specassay/blob/main/catalogs/presets.json), which the catalogs point installers at)*
