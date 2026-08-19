# Upgrading an existing install

For an adopter already running SpecAssay 0.3.x or 0.4.x. Three real
frictions below, each tested directly against the real `specify` CLI
(0.15.3.dev0) — not assumed, not carried over from an old note without
checking it still holds.

## 1. Presets have no update command

`specify preset --help` lists `list / add / remove / search / resolve /
info / set-priority / enable / disable / catalog` — no `update`. Compare
`specify extension --help`, which does have one (`extension update`).
This asymmetry is real today, not fixed in this release.

**What does work:** `specify bundle update <bundle-id>` (SpecAssay ships
as a bundle) reports success and does touch the installed preset files —
but it's still bound by friction #3 below, so on its own it isn't a
reliable way to get newer content.

## 2. A pinned-tag catalog can mask new versions

If your catalog URL points at a specific release tag rather than `main`
— a reasonable thing to do for reproducibility — it will never surface a
newer version, because the catalog JSON itself is frozen at that tag.
This repo's own README install commands point at `main`
(`raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/*.json`), so
a fresh install today doesn't hit this. If you're upgrading an older
install, check what your `.specify/preset-catalogs.yml`,
`extension-catalogs.yml`, and `bundle-catalogs.yml` actually point at —
an earlier version of these instructions, or a deliberate pin, may have
you on a tagged URL that will silently never move.

## 3. The local catalog cache doesn't refresh on its own

Tested directly, not assumed: `specify bundle update`, and even a full
`specify preset remove` + `specify preset add` cycle, left
`.specify/presets/.cache/catalog-*-metadata.json`'s `cached_at`
timestamp completely unchanged — the cache survives reinstall. The only
thing that actually forced a fresh fetch (confirmed: `cached_at` jumped
to the real current time) was deleting the cache directory first:

```bash
rm -rf .specify/presets/.cache .specify/extensions/.cache

specify preset remove specassay
specify preset add specassay

specify extension remove specassay-check
specify extension add specassay-check

# or, for the whole bundle in one pass:
specify bundle remove specassay
specify bundle install specassay
```

There's no `--refresh`/`--no-cache` flag on any of these commands as of
0.15.3.dev0 — the cache directory itself is the only lever.

## After upgrading

Diff your own `specassay-check-config.yml` against the current
`config-template.yml` for keys that didn't exist when you first
installed — `block_uncovered_proof` (v0.4.8) and `test_results` (v0.4.9)
are both opt-in and won't appear in an older config automatically. Then
run the Gate once locally to confirm it still passes before trusting CI:

```bash
bash .specify/extensions/specassay-check/scripts/check-traceability.sh
```

## What already works cleanly

Adding a *new* catalog, or installing a component for the first time, is
unaffected by any of the above — the frictions are specifically about
getting *already-installed* components to see *newer* content. A brand
new `specify bundle install specassay` on a project that's never had it
picks up the current version correctly, every time this was tested.
