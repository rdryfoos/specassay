# SpecAssay preset

Appends SpecAssay's durable-ID rules and vocabulary onto Spec Kit core templates via `append` strategy. Does not replace Spec Kit's workflow.

Install from the released pack:

```bash
specify preset add --from https://github.com/rdryfoos/specassay/releases/download/v0.3.4/specassay-preset-0.3.4.zip
```

Or from a checkout, for development:

```bash
specify preset add --dev /path/to/specassay/presets/specassay
```

Vocabulary (trace-manifest, statuses, Gate 2) lands in the constitution template. For projects that keep a separate glossary, also merge [`GLOSSARY.md`](./GLOSSARY.md).

See the repo root [`PROMOTION-CONTRACT.md`](../../PROMOTION-CONTRACT.md).
