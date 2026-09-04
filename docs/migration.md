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

## The upgrade command that works (re-verified 2026-09-04, v0.4.12 to v0.4.13)

For a project that installed the bundle by ID through the catalogs, from
the project root:

```bash
rm -rf .specify/extensions/.cache .specify/presets/.cache
specify bundle update specassay
```

Receipt: `docs/submission/test-evidence.md`, "Upgrade path". Without the
first line, `specify extension update specassay-check` reports `Up to
date (v0.4.12)` and `specify bundle update specassay` stops with `Error:
Extension 'specassay-check' is pinned to version 0.4.13 in the bundle
manifest, but the resolved version is 0.4.12`. With it, both components
move to 0.4.13 in one command, and an edited
`specassay-check-config.yml` survives untouched. `specify extension
update specassay-check` after the same cache clear also works but prompts
`[y/N]`, so it needs a terminal.

For a git-clone install, pull the tag and re-add with `--force`:

```bash
git -C /path/to/specassay fetch --tags
git -C /path/to/specassay checkout "$(git -C /path/to/specassay describe --tags --abbrev=0 origin/main)"
specify extension add --dev /path/to/specassay/extensions/specassay-check --force
```

The second line checks out the newest tag reachable from `main`, so the
snippet does not name a version and does not go stale.

## 4. The raw catalog URL lags a push by up to five minutes

`raw.githubusercontent.com` serves `catalogs/*.json` with
`cache-control: max-age=300`. If anyone fetched the catalog in the five
minutes before a version bump was pushed, the old JSON keeps being served
until that window expires. Measured 2026-09-04: a fresh `specify bundle
install specassay` resolved 0.4.12 two minutes after the 0.4.13 catalogs
were on `main` (`x-cache: HIT`, `source-age: 285`), then 0.4.13 four
minutes later with nothing else changed. If an install or update lands on
the previous version right after a release, wait five minutes and rerun;
nothing is broken.

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
