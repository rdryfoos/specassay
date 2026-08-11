# Extension Submission draft — specassay-check

Paste-ready answers for Spec Kit's **Extension Submission** issue form
(`https://github.com/github/spec-kit/issues/new?template=extension_submission.yml`).

---

**Extension ID:** `specassay-check`

**Extension Name:** SpecAssay Check

**Version:** 0.3.1

**Description:**
Gate 2 — refuse silent gaps and emit a trace-manifest (`trace-manifest.json`).

**Category:** visibility · **Effect:** read-write

**Author:** Rik Dryfoos / Dryfoos Consulting

**Repository URL:** https://github.com/rdryfoos/specassay

**Download URL:**
https://github.com/rdryfoos/specassay/releases/download/v0.3.1/specassay-check-0.3.1.zip

**Documentation URL:**
https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md

**License:** MIT

**Required Spec Kit Version:** >=0.14.0

**Provides:** 1 command (`speckit.specassay-check.gate`), 1 optional
`after_implement` hook, 1 required config template
(`specassay-check-config.yml`).

**Tags:** traceability, gate, ci, governance, sdd

**What it does:**
Scans the registry (PRD), specs, tasks, `@covers` source marks, and named
tests; refuses on silent acceptance-criterion gaps, invented IDs, and
registry↔specs↔tasks drift; writes `trace-manifest.json` on every run —
including refusals — so the evidence trail survives the failure. Honest debt
(`tracked-debt`) and planned work (`backlog`) pass and stay visible. Also
ships the Thread Report CI tooling: a per-PR briefing comment with
restated-intent detection and optional human-tick gates
(`offthread_ack` / `intent_ack`).

**Proposed Catalog Entry:**
*(the `specassay-check` object from
[`catalogs/extensions.json`](../../catalogs/extensions.json))*
