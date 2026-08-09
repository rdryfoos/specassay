# Sample `trace-manifest.json` files

| File | What |
|------|------|
| `homesflow.trace-manifest.json` | Real Gate 2 emit against HomesFlow — fully SpecAssay-native (`**Carries**:`, no `clew`/`Traces`); 82 rows, `gate.ok: true`, 0 GAP |
| `sample.trace-manifest.json` | Clean synthetic demo (`example-app`) — the shareable "shape" artifact and Loupe's preview default |
| `sample-gap.trace-manifest.json` | The `example-app` demo with one AC gilted into a silent **GAP** — `gate.ok: false`, one frayed row. Demos the refusal / broken-thread state. |

`homesflow.trace-manifest.json` is the real baseline; `sample.trace-manifest.json` is a curated synthetic demo, and `sample-gap.trace-manifest.json` is that same demo with a single silent gap so viewers can see a fray. All three are clean, post-rename manifests.

Regenerate the HomesFlow twin (the synthetic `sample` is curated by hand, not synced):

```bash
# from a machine (or CI) that can see HomesFlow
cd /path/to/HomesFlow && bash .specify/extensions/specassay-check/scripts/check-traceability.sh
cp /path/to/HomesFlow/trace-manifest.json samples/homesflow.trace-manifest.json
```

Silent-gap refusal is **AC-only**. US/FR/NFR without `@covers` are `backlog`, not `GAP`.
