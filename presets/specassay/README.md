# SpecAssay preset

Appends SpecAssay's durable-ID rules and vocabulary onto Spec Kit core templates via `append` strategy. Does not replace Spec Kit's workflow.

Install from the latest released pack (the URL is version-agnostic: GitHub redirects `releases/latest/download/specassay-preset.zip` to the newest release's unversioned copy of the preset zip, so this line never goes stale):

```bash
specify preset add --from https://github.com/rdryfoos/specassay/releases/latest/download/specassay-preset.zip
```

Or from a checkout, for development:

```bash
specify preset add --dev /path/to/specassay/presets/specassay
```

Vocabulary (trace-manifest, statuses, Gate 2) lands in the constitution template. For projects that keep a separate glossary, also merge [`GLOSSARY.md`](./GLOSSARY.md).

See the repo root [`PROMOTION-CONTRACT.md`](../../PROMOTION-CONTRACT.md).
