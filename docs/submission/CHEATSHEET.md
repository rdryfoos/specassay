# Filing cheat sheet: three issues, in this order

Each row: open the **form**, then copy everything below the `---` rule in the
**paste-from** doc into it. The forms are GitHub issue templates on the
Spec Kit repo; the paste-from docs mirror their fields exactly, catalog JSON
included, no other tabs needed.

| # | Issue | Form (opens the template) | Paste from |
| --- | --- | --- | --- |
| 1 | Extension | <https://github.com/github/spec-kit/issues/new?template=extension_submission.yml> | [extension-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md) |
| 2 | Preset | <https://github.com/github/spec-kit/issues/new?template=preset_submission.yml> | [preset-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/preset-submission.md) |
| 3 | Bundle | <https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml> | [bundle-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/bundle-submission.md) |

File 1 and 2 first, note their issue numbers, then reference both in the
bundle issue (the bundle depends on both components being cataloged).

Tips:

- On each paste-from page, the **Copy raw file** button (two-squares icon,
  top right of the file view) grabs the whole document in one click.
- Every checkbox on the forms is honestly tickable; if a maintainer asks for
  proof, point at
  [test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md).
- If the template picker misbehaves, the chooser is
  <https://github.com/github/spec-kit/issues/new/choose>.

Links the forms ask for (all live):

- Repository: <https://github.com/rdryfoos/specassay>
- Release with artifacts: <https://github.com/rdryfoos/specassay/releases/tag/v0.3.4>
- Catalogs: <https://github.com/rdryfoos/specassay/tree/main/catalogs>
- Extension README: <https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md>
- Preset contract: <https://github.com/rdryfoos/specassay/blob/main/PROMOTION-CONTRACT.md>

Expected turnaround: a maintainer validates catalog entry and URLs in 3–7
business days (they do not audit code). For what happens at the next
version bump, see **Updating to a new version** below.

## Updating to a new version

Verified against Spec Kit's own docs on 2026-08-14, not inferred from
bot behavior. The three component types do not all work the same way.

**Extension:** file a **new** [Extension Submission
issue](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml)
with the new version and download URL, and say in it that this updates
#4057 (now closed). Source: `extensions/EXTENSION-PUBLISHING-GUIDE.md`,
"Updating an Existing Extension"; do not edit the closed issue.

**Bundle:** same pattern. File a **new** [Bundle Submission
issue](https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml),
new version and download URL, mention it updates #4059 (now closed).
Source: `docs/community/bundles.md`, "Updating a Bundle."

**Preset:** no documented issue-based update path.
`presets/PUBLISHING.md`'s Release Workflow instead describes a **direct
PR** against `presets/catalog.community.json` in `github/spec-kit`,
bumping `version` and `download_url` for the `specassay` entry.
`docs/community/presets.md` has no "Updating a Preset" section at all.
Try the issue-based route first anyway (a new [Preset Submission
issue](https://github.com/github/spec-kit/issues/new?template=preset_submission.yml)
noting it updates #4058): the same bot machinery that generated #4070
and #4123 from issue edits worked three times this round and is the
better-tested path. If a maintainer redirects to the PR route, that's
the documented fallback, and it means forking `spec-kit` and opening a
PR by hand rather than filing an issue and waiting.

Either way: bump `bundle.yml` / `extension.yml` / `preset.yml` and the
three `catalogs/*.json` first (`scripts/build-release.sh` refuses to
build if they disagree with what's declared). **Also grep
`presets/specassay/README.md` and `extensions/specassay-check/README.md`**
for old version strings and asset names — round 3 (below) shipped a
stale install command in the preset's own README for two version bumps
running specifically because the sweep only ever touched the manifests
and catalogs, never the READMEs that ship *inside* the zips themselves.
Then cut the release, and verify the published zips before filing
anything — unzip and check, don't trust the source tree: that's how
round 3's stale file was finally caught, after three prior sweeps had
all missed it by reading the source tree instead of the artifact.

## v0.4.13 cut, 2026-09-04; filing not yet done

Tag `v0.4.13` at `105c4845f8ae88f1af361d56c0de458089b50fad`, release
<https://github.com/rdryfoos/specassay/releases/tag/v0.4.13>, built by the
Release workflow (<https://github.com/rdryfoos/specassay/actions/runs/33883485224>).
The sweep above was followed in full: all three manifests, the three
catalogs (plus the `commands` count, 2 to 5, stale since dig, matrix, and
portfolio shipped), and the preset README that ships inside its zip. The
published zips were unzipped and checked, digests verified three ways,
and the upgrade from a real v0.4.12 catalog install was run and recorded
(`docs/submission/test-evidence.md`). The three paste-from docs are
regenerated at 0.4.13 with the real digests.

**Still to do, by a human:** file the three new issues, in this order,
each naming its 0.4.12 predecessor: extension (updates #4252, merged as
#4254), preset (updates #4253, merged as #4256; the issue route worked for
the preset last time, so use it again), bundle (updates #4255, merged as
#4257; reference the two new component issues by number). Until those
merge, Spec Kit's own community catalog still lists 0.4.12; this repo's
hosted catalogs already serve 0.4.13.

One thing to know for the next cut: `raw.githubusercontent.com` caches
the catalogs for five minutes (`docs/migration.md`, friction 4), so an
install in the minutes right after the push can still resolve the old
version. Wait it out before declaring the push broken.

## v0.4.12 filed, 2026-08-21

Following this section's own "Updating to a new version" pattern: three
**new** issues, each naming its closed 0.3.4 predecessor, in dependency
order. Extension [#4252](https://github.com/github/spec-kit/issues/4252)
(updates #4057), preset
[#4253](https://github.com/github/spec-kit/issues/4253) (updates #4058),
bundle [#4255](https://github.com/github/spec-kit/issues/4255) (updates
#4059, references #4252 and #4253 by number). All three verified against
`docs/submission/{extension,preset,bundle}-submission.md` after filing —
version, download URL, and cross-references all checked, not assumed.
Preceded by the design room's own independent cold-install verification
(`RELEASE-HANDOFF.md`, "Wall passed, 2026-08-20") before any of the three
were filed.

## Amending a filed issue (closed history, 2026-08-13 – 08-14)

**All three merged 2026-08-14.** Extension via #4113, preset via #4123,
bundle via #4125, all at v0.3.4. The three original issues (#4057,
#4058, #4059) are closed. Everything below this heading describes how
that submission got through three review rounds while the issues were
still open; it doesn't apply anymore, since a closed issue isn't where
the next update happens (see **Updating to a new version**, below the
history). Kept for the record and as a worked example.

The three issues were filed and validated; each had a generated catalog
PR behind it. While open, they were **edited in place**, not refiled:
open the issue, use the `...` menu on the first comment, choose **Edit**.

Two review rounds have needed this. The first (author metadata, v0.3.2) is
closed. The second is below.

### Round 2, 2026-08-13: required tools and version alignment (done)

All three issues were edited to 0.3.3 and both replies posted on
2026-08-13. Kept as the worked example of what a review round takes.

Two findings, from Copilot review on the generated PRs:

- On **#4069**: the catalog entry dropped the `python3 (>=3.8)` constraint
  the submission promised, so every Python 3 read as compatible. The
  extension now declares its tools properly.
- On **#4070**: the preset was 0.2.1 while its download URL pointed into
  the v0.3.2 release. Spec Kit's preset workflow wants a release tag
  matching the preset's own version. Fixed by moving all three components
  onto the bundle's version, permanently.

Everything is now **0.3.3**, released as **v0.3.3**. Edit each issue:

| Issue | Field | New value |
| --- | --- | --- |
| [#4057 extension](https://github.com/github/spec-kit/issues/4057) | Version | `0.3.3` |
| | Download URL | `https://github.com/rdryfoos/specassay/releases/download/v0.3.3/specassay-check-0.3.3.zip` |
| | Required Tools | `bash (required); python3 >=3.8 (required, standard library only)` |
| | Example Usage | point the `--from` URL at the 0.3.3 zip |
| | Proposed Catalog Entry | copy the JSON from [extension-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md), which now carries the `requires.tools` block |
| [#4058 preset](https://github.com/github/spec-kit/issues/4058) | Version | `0.3.3` |
| | Download URL | `https://github.com/rdryfoos/specassay/releases/download/v0.3.3/specassay-preset-0.3.3.zip` |
| [#4059 bundle](https://github.com/github/spec-kit/issues/4059) | Version | `0.3.3` |
| | Download URL | `https://github.com/rdryfoos/specassay/releases/download/v0.3.3/specassay-0.3.3.zip` |
| | Components Provided | `specassay-check@0.3.3`, `specassay@0.3.3` |
| | Example Usage | the `curl` line names the zip twice |
| | Proposed Catalog Entry | version and download_url |

Reply on **#4057** (where the tools finding was raised):

> Fixed in v0.3.3. `extension.yml` carried `tools: []`, so the generated
> entry had nothing to carry the constraint. It now declares `bash` and
> `python3 >=3.8` in the same shape other catalog entries use, and the
> submission and proposed catalog entry match. The floor is deliberate:
> the shipped code parses on 3.7, and 3.8 is what is supported and tested.

And on **#4058** (the preset mismatch):

> Fixed in v0.3.3, taking the second option: all three components now share
> the bundle's version, so the release tag always matches every component
> version. The preset is 0.3.3, published as
> `specassay-preset-0.3.3.zip` in the v0.3.3 release, and the bundle
> reference is updated to match. Component versions will move together from
> here, so this cannot drift again.

The generated PRs (#4069, #4070, #4072) are refreshed by maintainers from
the edited issues; that side is theirs, not yours.

### Round 3, 2026-08-13: the preset README shipped a stale link (done)

Copilot review on the regenerated preset PR caught what round 2 missed:
`presets/specassay/README.md` ships inside the preset zip itself, and its
install command still named `v0.3.1/specassay-preset-0.2.0.zip` through
two prior bumps because neither sweep grepped that file. Fixed, and
because the fix lives inside the artifact, it needed a real release
rather than a docs edit: republishing v0.3.3's assets under the same tag
with different contents would have repeated the exact mismatch this
bundle exists to catch. Everything moved to **0.3.4**.

Edit each issue to `0.3.4` (Version and Download URL on all three;
Components Provided on #4059 becomes `specassay-check@0.3.4`,
`specassay@0.3.4`). Reply on **#4058**, where this finding landed:

> Fixed in v0.3.4. The preset README shipped inside the preset zip still
> pointed at the v0.3.1 asset name through the last two bumps; that file
> wasn't in either sweep's grep pattern. It now points at v0.3.4, and
> since the fix lives inside the artifact rather than just the issue
> text, this went out as a real release, not an edit.
