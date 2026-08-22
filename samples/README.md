# Sample `trace-manifest.json` files

All five are **real Gate 2 emits** — no hand-curated JSON.

| File | What |
|------|------|
| `homesflow.trace-manifest.json` | Real emit against HomesFlow — 82 rows, `gate.ok: true`, 0 GAP. The production-scale baseline. |
| `sample.trace-manifest.json` | Real emit from the shipped [`examples/example-app`](../examples/example-app) playground — 10 rows (3 proven / 1 tracked-debt / 6 backlog), `gate.ok: true`. The shareable "shape" artifact and Loupe's preview fallback. |
| `sample-gap.trace-manifest.json` | The same `example-app` emit with one acceptance criterion's proof removed, so it gilts into a silent **GAP** — `gate.ok: false`, one frayed row. Demos the refusal / broken-thread state. |
| `sample-duplicate-id.trace-manifest.json` | The same `example-app` emit with a second, independently-minted `AC-SYNC-01` definition line appended (a different statement, same ID — the two-branch-collision shape) — `gate.ok: false`, one `duplicate-id` failure naming both line numbers. Demos the v0.4.0 refusal that closes the `sort -u` silent-collision hole. |
| `cold-trial-imei.trace-manifest.json` | Real emit from the 2026-08-19 cold-agent trial ([`docs/testing/completed/evidence-cold-agent-trial-observed-2026-08-19.md`](../docs/testing/completed/evidence-cold-agent-trial-observed-2026-08-19.md)) — an uncoached agent's own IMEI-validator feature on a real, unrelated public repo (`python-validators/validators`), 5 rows, `gate.ok: true`, 0 GAP. `repoPath`/`targetName` scrubbed the same way `sample.trace-manifest.json` is; nothing else touched. |

## Sample `dig-report.json` files

Not a trace-manifest — `specassay dig`'s own output (archaeology mode, no-LLM floor). Real, not hand-curated.

| File | What |
|------|------|
| `insurance-java.dig-report.json` | Real `dig` run (2026-08-21) against `github.com/SpecDriven/insurance-java`, cloned read-only per the archaeology-mode build handoff's §0 permission-on-record — 27 candidate rows (25 AC from test names, 2 US from README headings, 0 FR since the app is Vaadin-style UI + services, not a REST API). `sourceRepoPath` scrubbed from the local clone's absolute path to `insurance-java`; nothing else touched. This is the run that caught `dig`'s default-output-location defect (`AC-DIG-30`) — first written to a session scratchpad, not durable ground; regenerated here after the fix. |

## Regenerating them

**`sample`** — re-run Gate 2 against the bundled example project and copy it in (then scrub the absolute `repoPath` to `example-app`):

```bash
SPECASSAY_PROJECT_ROOT="$PWD/examples/example-app" \
SPECASSAY_CONFIG="$PWD/examples/example-app/specassay-check-config.yml" \
bash extensions/specassay-check/scripts/check-traceability.sh
cp examples/example-app/trace-manifest.json samples/sample.trace-manifest.json
```

**`sample-gap`** — `sample` with one AC's proof removed (`AC-SYNC-01` → `GAP`, `gate.ok: false`). It exists only to show a fray; regenerate it from `sample` after refreshing that file.

**`sample-duplicate-id`** — a scratch copy of `example-app` with one extra line appended to `PRD.md`, `- AC-SYNC-01 — A second, conflicting definition minted independently on another branch.`, then Gate 2 run and the manifest copied in (same `repoPath`/`targetName` scrub as `sample`). Never append to the real `examples/example-app/PRD.md` to generate this — use a throwaway copy.

**`homesflow`** — from a machine (or CI) that can see HomesFlow:

```bash
cd /path/to/HomesFlow && bash .specify/extensions/specassay-check/scripts/check-traceability.sh
cp /path/to/HomesFlow/trace-manifest.json samples/homesflow.trace-manifest.json
```

Silent-gap refusal is **AC-only**. US/FR/NFR without `@covers` are `backlog`, not `GAP`.
