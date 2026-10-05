# SpecAssay preset

Appends SpecAssay's durable-ID rules and vocabulary onto Spec Kit core templates via `append` strategy. Does not replace Spec Kit's workflow.

<!-- @covers FR-COLD-10, AC-COLD-10b -->

**This preset is the templates, and only the templates.** The Gate, the thing that
reads your registry and refuses a silent gap, lives in the `specassay-check`
extension. A preset install on its own leaves you with templates that name a check
your project does not have. The one line that brings both is
`specify bundle install specassay`, and the [quickstart](https://github.com/rdryfoos/specassay#install-catalog-path)
gives it with the three `catalog add` lines it needs. The preset declares the
extension as a dependency, so Spec Kit itself names what is missing after a
preset-only install (1.0.4 and later; <!-- specassay:pinned Spec Kit --> earlier
releases ignore the declaration):

```text
!  This preset depends on extensions that are not satisfied:
    specassay-check is not installed
      Install with: specify extension add specassay-check
```

Install from the latest released pack (the URL is version-agnostic: GitHub redirects `releases/latest/download/specassay-preset.zip` to the newest release's unversioned copy of the preset zip, so this line never goes stale):

```bash
specify preset add --from https://github.com/rdryfoos/specassay/releases/latest/download/specassay-preset.zip
```

Or pin the exact release, which is the form a catalog entry carries:

```bash
specify preset add --from https://github.com/rdryfoos/specassay/releases/download/v0.5.6/specassay-preset-0.5.6.zip
```

Or from a checkout, for development:

```bash
specify preset add --dev /path/to/specassay/presets/specassay
```

Vocabulary (trace-manifest, statuses, Gate 2) lands in the constitution template. For projects that keep a separate glossary, also merge [`GLOSSARY.md`](./GLOSSARY.md).

See the repo root [`PROMOTION-CONTRACT.md`](../../PROMOTION-CONTRACT.md).
