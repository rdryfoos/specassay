# SpecAssay Check

Every **intent** is on the **Golden Thread** with its **build** and its **proof**; this check stops the line at any loose end, then strikes a hallmark on what it found — the **trace-manifest**.

Gate 2: compare the ID registry to specs, tasks, coverage annotations, and test names. **Exact-set** registry ≡ specs ≡ tasks. Silent AC gaps and untraced scope fail. **Always writes a trace-manifest** (default `trace-manifest.json`, configurable via `manifest_path`) for Loupe or any matrix consumer.

**CI is the property line.** Run this script on every PR / protected-branch push and fail the build on non-zero exit. Local runs are hygiene; CI is what stops a cowboy (or any machine without SpecAssay) from merging unmarked work. Keep the emitted trace-manifest from the CI run as evidence.

Install:

```bash
specify extension add --dev /path/to/specassay/extensions/specassay-check
```

Install scaffolds `specassay-check-config.yml` from `config-template.yml`. Edit `registry`, `manifest_path`, `specs`, `tasks`, `src_globs`, and `test_globs` for your repo.

**No registry yet?** IDs are minted, not hand-typed. Run
`/speckit.specassay-check.mint` (or `mint-id.sh` directly, same
env-var pattern as the Gate script above) to create the file on its
first call and mint your first ID. Minting always lands on a multiple
of ten; a duplicate the Gate later refuses resolves with
`mint-id.sh --resolve <ID>`. See `scripts/mint-id.sh` and
`commands/speckit.specassay-check.mint.md`.
