# Submission package — status and checklist

## v0.5.6, cut 2026-10-05: one filing, four releases of arrears

Where the community catalog actually stands, re-observed 2026-10-05 against
`raw.githubusercontent.com/github/spec-kit/main/{extensions,presets,bundles}/catalog.community.json`:
**all three entries read 0.5.2**, with 0.5.2 download URLs. That round was filed
2026-09-23 and landed 2026-09-24 as
[#4717](https://github.com/github/spec-kit/issues/4717),
[#4735](https://github.com/github/spec-kit/issues/4735) and
[#4737](https://github.com/github/spec-kit/issues/4737). The sections below this
one are the record of the rounds before it and are not re-written.

So 0.5.3, 0.5.4, 0.5.5 and 0.5.6 are all unfiled, and the next filing carries the
four of them at once. One issue per component, three in all, because the bundle
pins its own components: a filing that moved one of them would describe a bundle
that does not exist.

**The three bodies are prepared, at 0.5.6, and filing is the human step.**
Corrected 2026-10-06: an earlier version of this page said each form asks for the
asset's sha256. It does not. Reading the three upstream templates
(`.github/ISSUE_TEMPLATE/{extension,preset,bundle}_submission.yml` on
`github/spec-kit`), **no field asks for a digest at all**. The digest reaches the
reviewer only inside the **Proposed Catalog Entry** textarea, which is pasted from
`catalogs/*.json`, and those carry it only after the digests pull request. The
dependency is the same; the sentence was wrong about where it lives.

| Field | Source | State |
| --- | --- | --- |
| version `0.5.6` | `bundle.yml`, `extension.yml`, `preset.yml` | in the bodies |
| download URL | `catalogs/*.json`, naming the v0.5.6 assets | in the bodies |
| Proposed Catalog Entry, digest and all | pasted verbatim from `catalogs/*.json` | in the bodies |
| the receipts each form asks to see | a run against the published assets | re-run 2026-10-06 |

So [bundle-submission.md](bundle-submission.md),
[extension-submission.md](extension-submission.md) and
[preset-submission.md](preset-submission.md) are paste-ready. What remains is
opening three issues on `github/spec-kit`, which is a human step: that repository
was not reachable from the session that prepared these, so nothing was filed.
Order matters, because the bundle pins its components: the extension and preset
issues go first, the bundle issue last.

## v0.5.1, released 2026-09-17: filing not yet done

Tag `v0.5.1`, release
<https://github.com/rdryfoos/specassay/releases/tag/v0.5.1>. A display release (the
Thread Report's trims, `--receipts`, the `THREAD` rows, a dated correction to the
0.5.0 notes); the Gate is untouched. Digests verified three ways and the three
paste-from docs filled from them; the clean-project install and the upgrade from a
real v0.5.0 are recorded in `test-evidence.md`, including the block it unblocks —
`--receipts` is refused outright by v0.5.0 and works after one `bundle update`.
**Chalkup is unblocked.** Two steps remain: the site's hero pin, still on the
v0.4.13 README anchor and now two releases stale, and the submission-form issues.

## v0.5.0, released 2026-09-16: never filed

Tag `v0.5.0`, release
<https://github.com/rdryfoos/specassay/releases/tag/v0.5.0>. Digests were verified
three ways and the clean-project install and v0.4.13 upgrade are recorded in
`test-evidence.md`, but its three submission-form issues were never filed, so the
arrears now stand at two releases.

## v0.4.13, released 2026-09-04: catalog pointer filed, forms not

Catalog pointer PR open upstream: [github/spec-kit#4448](https://github.com/github/spec-kit/pull/4448) (all three entries, one PR, because the bundle pins its components). Its submission-form issues were never filed**, so the
0.5.0 filing carries two versions' worth of change and updates the last issues actually filed
(#4252 extension, #4253 preset, #4255 bundle). v0.4.12 is the version Spec Kit's community
catalog currently carries (#4254, #4256, #4257 all merged).

## v0.3.4, filed 2026-08-11

**Filed 2026-08-11** — all three issues are in Spec Kit's queue:
[#4057](https://github.com/github/spec-kit/issues/4057) (extension) ·
[#4058](https://github.com/github/spec-kit/issues/4058) (preset) ·
[#4059](https://github.com/github/spec-kit/issues/4059) (bundle).
A maintainer applies the submission label at triage, which starts automated
catalog validation (3–7 business days). The
[cheat sheet](https://github.com/rdryfoos/specassay/blob/main/docs/submission/CHEATSHEET.md)
stays for the next version-update filing.

Everything Spec Kit's community submission process asks for, what state it's
in, and what remains. The submission path is **issues, not PRs**: file one
issue per component using Spec Kit's templates; a maintainer validates the
catalog entry and URLs (3–7 business days; they do not audit code).

## What's done ✅

| Item | Where | Verified |
| --- | --- | --- |
| `bundle.yml` / `extension.yml` / `preset.yml` manifests | repo root, `extensions/specassay-check/`, `presets/specassay/` | `specify bundle validate` ✓ |
| Versioned release with the `specify bundle build` artifact | [latest release](https://github.com/rdryfoos/specassay/releases/latest): v0.5.5's three assets, observed 2026-10-05. v0.5.6's are built and published by the Release workflow at the tag, which is why this row names the last one published rather than the one being cut. | built in CI by the real CLI |
| Hosted catalogs with live download URLs | [`catalogs/*.json`](https://github.com/rdryfoos/specassay/tree/main/catalogs) | assets download and install ✓ |
| Clean-project install, end to end, by bundle ID | — | [test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md) |
| LICENSE (MIT) · README · CHANGELOG | repo root | — |
| Command namespace rule (`speckit.{extension-id}.{command}`) | `speckit.specassay-check.gate` | installer accepts ✓ (it refused the old name, see CHANGELOG 0.3.1) <!-- specassay:stale-ok a citation of a CHANGELOG section, which does not move --> |
| Paste-ready issue bodies | [bundle](https://github.com/rdryfoos/specassay/blob/main/docs/submission/bundle-submission.md) · [extension](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md) · [preset](https://github.com/rdryfoos/specassay/blob/main/docs/submission/preset-submission.md) | mirror the actual issue-form fields |

## What a human does (the actual filing) 🖐 — done 2026-08-11, see issue links above

1. File the **Extension Submission** issue → paste from
   [extension-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md).
2. File the **Preset Submission** issue → paste from
   [preset-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/preset-submission.md).
3. File the **Bundle Submission** issue → paste from
   [bundle-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/bundle-submission.md), and reference the other two
   issues (the bundle depends on both components being cataloged).
   - Templates: <https://github.com/github/spec-kit/issues/new/choose>
   - The form's checkboxes are all honestly tickable; the evidence for each
     is in [test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md).
4. Optional cleanup: delete releases v0.1.0/v0.2.0 (pre-rename `clewseau-*`
   asset names) and v0.3.0 (pre-namespace-fix command). Nothing references
   them. <!-- specassay:stale-ok names three specific old release artifacts to delete; the names are the point -->

## Cutting the next release 🔁

Bump versions in the three manifests + `catalogs/*.json` (and refresh the
catalog entries inlined in the three issue bodies here), update
CHANGELOG.md, then run the **Release** workflow
(`Actions → Release → Run workflow`) with the new tag, which is the one you just wrote into the manifests, and it
creates the tag, validates and builds with the real CLI through the hosted
catalogs, and publishes the assets the catalogs point at. (Tag pushes also
trigger it, where the git remote allows tag pushes.)

For a version update in the community catalog: file a new submission issue
noting it's an update to the existing entry.
