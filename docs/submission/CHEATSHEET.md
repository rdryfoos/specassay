# Filing cheat sheet: three issues, in this order

A copy-and-paste walk. Each issue is a GitHub issue form on the Spec Kit repo;
open the form, then work down this page filling each field in the order the form
asks for it. The values below are for **v0.5.2**. See **v0.5.2 refiled**, below, for why the
previous round had to be filed again.
<!-- specassay:current -->

**The issue route is the only route.** A direct pull request against
`presets/catalog.community.json` and its siblings is triaged out of scope and
closed; that has now happened twice, to #4448 and #4648. File the issues and an
automated workflow validates the release and generates the catalog PR itself.

**Order matters.** File the extension and the preset first, note their issue
numbers, then name both in the bundle issue. The bundle pins its component
versions, so a partial landing leaves `specify bundle install` unable to resolve.

Full field-by-field values live in the three paste-from docs, which mirror each
form exactly, catalog JSON included:

| # | Issue | Form | Paste from | Filed 2026-09-23 at 0.5.2 | Landed by | Supersedes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Extension | <https://github.com/github/spec-kit/issues/new?template=extension_submission.yml> | [extension-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md) | [#4711](https://github.com/github/spec-kit/issues/4711) | [#4735](https://github.com/github/spec-kit/pull/4735) | [#4690](https://github.com/github/spec-kit/issues/4690), [#4649](https://github.com/github/spec-kit/issues/4649) |
| 2 | Preset | <https://github.com/github/spec-kit/issues/new?template=preset_submission.yml> | [preset-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/preset-submission.md) | [#4713](https://github.com/github/spec-kit/issues/4713) | [#4717](https://github.com/github/spec-kit/pull/4717) | [#4691](https://github.com/github/spec-kit/issues/4691), [#4650](https://github.com/github/spec-kit/issues/4650) |
| 3 | Bundle | <https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml> | [bundle-submission.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/bundle-submission.md) | [#4715](https://github.com/github/spec-kit/issues/4715) | [#4737](https://github.com/github/spec-kit/pull/4737) | [#4692](https://github.com/github/spec-kit/issues/4692), [#4651](https://github.com/github/spec-kit/issues/4651) |

## Issue 1: Extension

Form: <https://github.com/github/spec-kit/issues/new?template=extension_submission.yml>

Title:

```
[Extension]: Add SpecAssay Check (update to 0.5.2)
```

Then, in the form's own order:

1. **Extension ID**: `specassay-check`
2. **Extension Name**: `SpecAssay Check`
3. **Version**: `0.5.2` <!-- specassay:current -->
4. **Description**, **Author**, **Repository URL**, **Download URL**, **License**: paste-from doc
5. **Homepage**, **Documentation URL**, **Changelog URL** (all optional): paste-from doc
6. **Required Spec Kit Version**: paste-from doc
7. **Required Tools** (optional), **Number of Commands** (`5`), **Number of Hooks** (`1`)
8. **Tags**, **Key Features**: paste-from doc
9. **Testing Checklist**: tick all 5
10. **Submission Requirements**: tick all 6
11. **Testing Details**, **Example Usage**, **Proposed Catalog Entry**: paste-from doc
12. **Additional Context**: paste-from doc; say it updates **#4252**

Note the issue number the form gives you. It is the extension number the bundle
issue must name.

## Issue 2: Preset

Form: <https://github.com/github/spec-kit/issues/new?template=preset_submission.yml>

Title:

```
[Preset]: Add SpecAssay (update to 0.5.2)
```

Then, in the form's own order:

1. **Preset ID**: `specassay`
2. **Preset Name**: `SpecAssay`
3. **Version**: `0.5.2` <!-- specassay:current -->
4. **Description**, **Author**, **Repository URL**, **Download URL**: paste-from doc
5. **Documentation URL**, **License**, **Required Spec Kit Version**: paste-from doc
6. **Required Extensions** (optional), **Templates Provided** (`3`), **Commands Provided** (`0`), **Number of Scripts** (optional, `0`)
7. **Tags**, **Key Features**: paste-from doc; say it updates **#4253**
8. **Testing Checklist**: tick all 4
9. **Submission Requirements**: tick all 5

This form has **no** Testing Details, Example Usage or Proposed Catalog Entry
field, unlike the other two. The receipts go in Key Features, which is the only
free-text field that will hold them.

## Issue 3: Bundle

File this **last**. Form:
<https://github.com/github/spec-kit/issues/new?template=bundle_submission.yml>

Title:

```
[Bundle]: Add SpecAssay (update to 0.5.2)
```

Then, in the form's own order:

1. **Bundle ID**: `specassay`
2. **Bundle Name**: `SpecAssay`
3. **Version**: `0.5.2` <!-- specassay:current -->
4. **Role or Team**: `developer`
5. **Description**, **Author**, **Repository URL**, **Download URL**: paste-from doc
6. **Documentation URL**, **License**, **Required Spec Kit Version**: paste-from doc
7. **Integration Target** (optional): leave empty; the bundle is integration-agnostic
8. **Components Provided**: paste-from doc
9. **Required Component Catalogs**: paste-from doc. This field is where the
   discovery-only fact belongs: the community catalog cannot install, so the
   three SpecAssay catalogs must be added as install-allowed first
10. **Tags**, **Key Features**: paste-from doc
11. **Testing Checklist**: tick all 7
12. **Submission Requirements**: tick all 5
13. **Testing Details**, **Example Usage**, **Proposed Catalog Entry**: paste-from doc
14. **Additional Context**: paste-from doc; say it updates **#4255**, and name
    the extension and preset issue numbers from steps 1 and 2

## Tips

- On each paste-from page, the **Copy raw file** button (two-squares icon, top
  right of the file view) grabs the whole document in one click.
- Every checkbox on all three forms is honestly tickable. If a maintainer asks
  for proof, point at
  [test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md).
- If the template picker misbehaves, the chooser is
  <https://github.com/github/spec-kit/issues/new/choose>.
- Read the templates before filing a new version. They move: the bundle form
  gained a **Required Component Catalogs** field, and its testing checklist now
  names bundle-ID installation from an install-allowed catalog, neither of which
  existed in August.

Links the forms ask for, all live:

- Repository: <https://github.com/rdryfoos/specassay>
- Release with artifacts: <https://github.com/rdryfoos/specassay/releases/latest> (redirects to the newest tag; the forms want the versioned asset URL from `catalogs/*.json`, not this link)
- Catalogs: <https://github.com/rdryfoos/specassay/tree/main/catalogs>
- Extension README: <https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md>
- Preset contract: <https://github.com/rdryfoos/specassay/blob/main/PROMOTION-CONTRACT.md>

Expected turnaround: a maintainer applies the submission label at triage, which
starts automated catalog validation, 3 to 7 business days. They validate the
catalog entry and URLs; they do not audit code. For what happens at the next
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

**Preset:** same pattern as the other two. File a **new** [Preset Submission
issue](https://github.com/github/spec-kit/issues/new?template=preset_submission.yml)
noting which issue it updates.

**Hedge withdrawn, 2026-09-20.** This paragraph used to say the preset had no
documented issue-based update path, that `presets/PUBLISHING.md` described a
direct catalog PR instead, and that the PR route was "the documented fallback"
if a maintainer redirected. That reading was wrong in the direction that costs
time. The issue route has now carried the preset three filings running, and it is
the direct catalog PR that gets closed: #4448 and #4648 both were, as triage out
of scope. There is no PR fallback. Forking `spec-kit` to bump a catalog file by
hand is not a slower path to the same place, it is a path to a closed PR.

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

Two more fields ride in the same sweep, learned 2026-09-04. (1) The
`requires.speckit_version` claim lives in six places (the three manifests,
the three `catalogs/*.json`) plus the three paste-from docs, and
`build-release.sh` compares versions only, never this field: change it in
the manifests first, and the catalogs and paste-from docs follow at the
cut, so a catalog never claims a range the zip inside does not. (2) Every
test-evidence entry names the `specify --version` it ran on, in its first
paragraph; an entry that does not is not evidence of compatibility with
anything.

**No site step, since 2026-09-16.** This used to carry a hero-pin bump:
specassay.com's CTA pointed at a tagged README anchor, one `href` in
`sites/specassay/src/index.html` in `dryfoos-sites`, and every cut had to move
it. **That pin no longer exists.** The CTA moved to `/start` on 2026-09-16
(dryfoos-sites `0b23272`) and names no tag, which the sites room's
`check-version-pins.mjs` confirms. There is nothing to bump here at a cut, and
the item this file carried as "still outstanding" for two releases is struck
rather than closed: it stopped being true before it was ever done.

If a tagged anchor is ever reintroduced, the old verification recipe should not
come back with it. It read `curl -sL <blob URL> | grep -c install-catalog-path`,
expecting nonzero. Measured 2026-09-20: against the rendered `blob/` page that
returns **2**, because GitHub emits the heading slug as an anchor `id` and
`href` in the HTML. Against the raw markdown it returns **0**, because the slug
is generated at render time and appears nowhere in the source. So the recipe was
passing on the rendered page for a reason unrelated to what it was checking, and
would have gone silently to zero the moment anyone pointed it at raw. Check the
heading itself instead, at the ref, in the source:

```
curl -fsSL https://raw.githubusercontent.com/rdryfoos/specassay/<tag>/README.md \
  | grep -c 'Install (catalog path)'
```

Measured the same day, 2026-09-20: **1** at `v0.5.1`. A count of 1 means the heading the
anchor is derived from exists at that ref, which is the thing worth knowing.

**Not a step of the sweep: specassay.com/start.** That page renders
`ONBOARD.md` at build time, and since 2026-09-15 a push to `main` that
touches `ONBOARD.md` pings the sites room's Vercel deploy hook by itself
(`.github/workflows/rebuild-start-page.yml`, secret
`VERCEL_DEPLOY_HOOK_START`). Do not add a manual rebuild for it here; if
that page ever looks stale, read that workflow's run for the release
rather than rebuilding by hand and leaving the cause in place. The hero
pin above stays manual on purpose: it names a tag, which only a human cut
decides.

## v0.5.2 landed, 2026-09-24

**All three merged, in one day, by one maintainer.** Every verdict arrived as a
label and a generated pull request. **Not one comment was ever posted on any of
the three issues**, by the validator or by anyone else, so a reader watching for
a reply would have seen nothing happen while the whole round completed.

| Component | Issue | Generated PR | Merged |
| --- | --- | --- | --- |
| Preset | [#4713](https://github.com/github/spec-kit/issues/4713) | [#4717](https://github.com/github/spec-kit/pull/4717) | 2026-09-24, KSchlobohm |
| Extension | [#4711](https://github.com/github/spec-kit/issues/4711) | [#4735](https://github.com/github/spec-kit/pull/4735) | 2026-09-24, KSchlobohm |
| Bundle | [#4715](https://github.com/github/spec-kit/issues/4715) | [#4737](https://github.com/github/spec-kit/pull/4737) | 2026-09-24, KSchlobohm, merge commit `ac53c9f` |

**The shape of a verdict.** Each issue went `enhancement, needs-triage` to a
submission label plus `triage-must-have` plus `validation-passed`, then a bot
opened the catalog PR as a draft, a review approved it, and a maintainer merged.
The bundle was last at every step: it carried `triage-can-wait` alongside
`triage-must-have` for about an hour before the pair resolved, and it got its
`validation-passed` after both components already had theirs.

**The manifest-freeze rule, which is what this round cost and taught.** The
validator reads the catalogs and `bundle.yml` on **the default branch**, not on
the tag an issue names. So while a submission is open, `main` is load-bearing:

- Do not cut a release while a submission is open at the previous version.
- Do not move `catalogs/*.json` or `bundle.yml` on `main` while a submission is
  open, except to move them **with** a refiling.
- Freeze the manifest for the duration, or expect to refile all three.

The reverse of this rule was tried first, pinning the catalogs while the
submissions were open, and it is what made the round fail: it protected the
artifacts the issue pointed at and left the manifest the validator actually
reads free to move underneath them.

## The bundle install receipt, taken 2026-09-24 after the merges

Not takeable before them: `specify bundle install specassay` resolves through
the community catalog, which read 0.4.12 until #4737 merged.
<!-- specassay:provenance -->
Taken in a clean `specify init` project outside this repository, on Spec Kit
1.0.5, Python 3.11.15, Linux.

**The community catalog resolves both components at 0.5.2, and will not install
them.** `policy=discovery-only` is Spec Kit's setting, not ours:

```text
$ specify bundle info specassay
specassay v0.5.2 — SpecAssay
  Source: community (discovery-only)
  Requires Spec Kit: >=0.14.0,<2.0.0
  Components (added on install):
    extensions:
      - specassay-check v0.5.2
    presets:
      - specassay v0.5.2 (priority=10, strategy=append)
  This source is discovery-only; the bundle cannot be installed from here.

$ specify bundle install specassay
Error: Bundle 'specassay' resolves only from a discovery-only source
('community'); it cannot be installed from there.
```

**So the install runs the README's catalog path**, which adds our three
catalogs `--install-allowed` and then installs:

```text
$ specify bundle install specassay
Updated execute permissions on 4 script(s) recursively
✓ Installed 'specassay' (2 added, 0 already present).

$ specify bundle list
  specassay v0.5.2 (2 components, installed 2026-09-24T17:21:31Z)

$ specify preset list
  SpecAssay (specassay) v0.5.2 — enabled — priority 10 / Templates: 3

$ specify extension list
  ✓ SpecAssay Check (v0.5.2)
     Commands: 5 | Hooks: 1 | Priority: 10 | Status: Enabled
```

**Confirmed on disk, not only in the listings.** `.specify/bundle-records.json`
records `specassay` 0.5.2 with both contributed components at 0.5.2, and the
installed manifests agree: `.specify/extensions/specassay-check/extension.yml`
reads `version: "0.5.2"` and `.specify/presets/specassay/preset.yml` reads
`version: "0.5.2"`. Nothing resolved to either of the versions these entries
carried before, 0.5.1 and 0.4.12, anywhere in the project.
<!-- specassay:provenance -->

**And the Gate runs.** On the fresh project it refuses for the documented
reason, no registry file, and after one `touch PRD.md` it is green and says why
it is green rather than implying the project is proved:

```text
  config: .specify/extensions/specassay-check/specassay-check-config.yml (from specassay-check-config.yml)
Wrote trace-manifest.json (0 rows) gate.ok=True
SpecAssay Check (Gate 2): OK, registry empty (0 IDs in PRD.md)
```

## v0.5.2 refiled, 2026-09-23

**A release makes an open submission stale.** v0.5.2 shipped while #4690, #4691
and #4692 were open at 0.5.1. Spec Kit's validator reads `bundle.yml` on the
repository's **default branch**, found 0.5.2 there against a submission filed at
0.5.1, and refused #4692 asking for the 0.5.2 release with matching artifact and
metadata. #4690 and #4691 were pre-empted rather than left to fail the same way.

**The catalogs moved with it.** The earlier ruling pinned `catalogs/*.json` at
v0.5.1 so nothing an open submission pointed at would change underfoot. That is
reversed: the submission is what moves, so the catalogs move too and everything
reads 0.5.2 at once.

| Component | Filed 0.5.2 | Supersedes | Originally |
| --- | --- | --- | --- |
| Extension | [#4711](https://github.com/github/spec-kit/issues/4711) | #4690 | #4649, #4252 |
| Preset | [#4713](https://github.com/github/spec-kit/issues/4713) | #4691 | #4650, #4253 |
| Bundle | [#4715](https://github.com/github/spec-kit/issues/4715) | #4692 | #4651, #4255 |

Filed in that order on 2026-09-23, by Rik's hand, and #4715 names the other two
in its Additional Context.

**The catalogs now carry `sha256`.** The field is optional in Spec Kit's schema
and **verified before install**, so an entry that carries it is checkable by the
tool rather than only by a reader. Ours never carried one until this round.

**The lesson, which is the reason this section exists:** do not cut a release
while a submission is open at the previous version, or expect to refile. The
validator's reference is the default branch, not the tag, so publishing v0.5.2
invalidated three open issues the moment `main` carried the new manifest.

## v0.5.1 refiled, 2026-09-23

The 2026-09-20 round was closed and refiled. **#4650 and #4651 were closed by a
maintainer asking for new clean issues; #4649 was still open and was superseded
rather than left, so there would not be two open issues for one extension.**

| Component | Filed 2026-09-23 | Supersedes |
| --- | --- | --- |
| Extension | #4690 | #4649 |
| Preset | #4691 | #4650 |
| Bundle | #4692 | #4651 |

**What each of the old three actually failed on**, from the validator's own
comments:

| Issue | Failure | Fixed by |
| --- | --- | --- |
| #4649 | the validator's fetch, twice: runs [35620079292](https://github.com/github/spec-kit/actions/runs/35620079292) and [35732690224](https://github.com/github/spec-kit/actions/runs/35732690224) | nothing to fix; refiled clean |
| #4650 | Documentation URL, and the fetch: run [35612050208](https://github.com/github/spec-kit/actions/runs/35612050208) | the URL now points at the preset README, which carries the pinned install line |
| #4651 | version-string mismatch, and the fetch: run [35645864929](https://github.com/github/spec-kit/actions/runs/35645864929) | every declaration in the issue now reads `>=0.14.0,<2.0.0` |

**All four fetch failures read "permission denied" or "blocked by the validation
environment", not 404.** That matters for the next round: it is not a bad URL
and there is nothing in this repository to fix. Measured independently on
2026-09-22, all three assets fetch anonymously at HTTP 200 with byte counts and
sha256 digests matching GitHub's own recorded asset digests, from a container
holding no credentials for that repository.

**Two lessons, both cheap to lose.**

*Every declaration inside one issue must agree.* #4651 failed because the form
field said `>=0.14.0,<2.0.0` while its own Proposed Catalog Entry said
`>=0.14.0`. The manifests and `catalogs/*.json` still diverge the same way; that
is ruled closed, with the catalogs aligning at v0.5.2. Until then, the issue is
written from the manifests, and both places in one issue are checked before
filing.

*The preset's Documentation URL has to carry the install line the entry
declares.* `releases/latest` is the right line for a reader and the wrong one
for a validator comparing it against a pinned catalog entry, so the preset
README now carries both.

## v0.5.1 cut, 2026-09-17; filed 2026-09-20, refiled 2026-09-23

Tag `v0.5.1` at `0f5976e52bccd374471f615fca37da0e8c6c76ee`, release
<https://github.com/rdryfoos/specassay/releases/tag/v0.5.1>.

A display release: the Thread Report's trims, `--receipts`, the `THREAD`
registry rows, and a dated correction to the 0.5.0 notes. The Gate is untouched.

The sweep above was followed in full, in two passes either side of the tag. The
first pass, on branch `claude/amazing-cray-lgftgd`: all three manifests, the three catalogs (version,
`download_url`, both `updated_at` fields), the three paste-from docs, the
CHANGELOG, `docs/submission/README.md`, and a v0.5.1 entry in
`docs/submission/test-evidence.md`. The in-zip READMEs needed no edit for the
second release running, which is round 3's version-agnostic fix holding.

Two things were left for the cut rather than guessed at, the same two as 0.5.0.
The paste-from digests are **now filled** from the published assets. **The site
pin is still on `v0.4.13`** — it was not bumped at 0.5.0 either, so it is now two
releases behind and is the oldest outstanding item in this file.

**The paste-from docs now name two skipped filings, not one.** Neither v0.4.13
nor v0.5.0 was ever filed on a submission form — v0.4.13 got only the catalog
PR, and v0.5.0's three issues were swept but never filed. The 0.5.1 filing
therefore carries three versions' worth of change and updates the last issues
actually filed (#4252 extension, #4253 preset, #4255 bundle). Worth deciding
before filing: whether to keep deferring, or file once and stop the arrears
growing.

Verified before the tag: 110 tests; this repo's own Gate `OK (67 registry IDs)`;
`specify bundle validate` well-formed; `scripts/build-release.sh` three zips
with `Artifacts and catalog download URLs agree.`

The second pass, after the tag, is in the same test-evidence entry under
**Post-tag**: digests verified three ways and the paste-from docs filled from
them; the unversioned aliases confirmed byte-identical to their versioned twins;
a clean-project install by bundle ID resolving **v0.5.1** first try and driven to
`proven`; and the upgrade from a real published v0.5.0, which also **reproduced
the block itself** — on v0.5.0 the report renders the old shape and
`--receipts` exits `unrecognized arguments`, while one `specify bundle update`
later the same project renders the new shape with the receipt folded. The
catalog-priority artefact recorded at 0.5.0 was avoided by removing the pinned
entries before adding `main`'s, rather than adding them alongside.

## v0.5.0 cut, 2026-09-16; filing not yet done

Tag `v0.5.0` at `899420356a4b0fa89366034787d793b561ee1e0a`, release
<https://github.com/rdryfoos/specassay/releases/tag/v0.5.0>, built by the Release
workflow (<https://github.com/rdryfoos/specassay/actions/runs/35151943499>).

The sweep above was followed in full, in two passes either side of the tag. The
first pass, on branch `claude/proof-direction`: all three manifests, the three catalogs
(version, `download_url`, both `updated_at` fields), the three paste-from
docs, the CHANGELOG, `docs/submission/README.md`, and a v0.5.0 entry in
`docs/submission/test-evidence.md`. The in-zip READMEs needed no edit this
round: both now install from the version-agnostic
`releases/latest/download/...` URLs, which is round 3's fix working as
intended.

Two things were left for the cut rather than guessed at. The paste-from digests
said "not yet known — fill at the cut", with the commands, because carrying the
0.4.13 digests under 0.5.0 URLs would have been a false claim about a specific
file; **they are now filled from the published assets.** The site pin was
recorded here as the one step still outstanding. **Struck 2026-09-20:** there is
no pin. The CTA moved to `/start` on 2026-09-16 (dryfoos-sites `0b23272`) and
names no tagged README, so the outstanding item had already ceased to exist when
this paragraph was written.

Verified before the tag, in this order: `python3 -m pytest
extensions/specassay-check/tests/ -q` (92 passed) under both mawk and gawk;
the eleven new regression tests copied into a `v0.4.13` worktree (`10 failed,
1 passed`, the pass being the static `awk -v` guard, which names a shape
v0.4.13 does not have); the repo's own Gate (`OK (65 registry IDs)`,
`gate.ok=True`); `specify bundle validate` (well-formed); `bash
scripts/build-release.sh` (three zips, `Artifacts and catalog download URLs
agree.`); and a clean `specify init` project on `specify 1.0.4` where the
built extension installs as v0.5.0, scaffolds its config, refuses honestly on
a missing registry, goes green on a stock thread, and proves a dotted
`AC-5.6.1a` from `test_AC_5_6_1_a_replays_queued_cards` — the case v0.4.13
could not reach. Receipts in `docs/submission/test-evidence.md`.

The second pass, after the tag, is recorded in the same entry under
**Post-tag**: digests verified three ways (release API, local hash of the
downloaded bytes, and the manifests read from inside the zips), the three
paste-from docs filled from those digests, a clean-project install by bundle ID
that resolved 0.5.0 on the first try, the Gate driven from empty registry to
`proven` on the published bits, the `FR-GATE-120` refusal read cold, and the
upgrade path run from a real published v0.4.13 install — where the same project,
the same files and the same edited config go from `('AC-5.6.1a', 'tracked-debt',
[])` to `('AC-5.6.1a', 'proven', ['test_AC_5_6_1_a_replays_queued_cards'])` one
command apart. The cache clear that 0.4.12 → 0.4.13 needed is still needed;
`docs/migration.md`'s upgrade command is unchanged and correct.

Still owed: the site pin, and the three submission-form issues, which now carry
two versions' worth of change because v0.4.13's were never filed.

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

**Site pin bumped 2026-09-04:** specassay.com's hero CTA moved from the
v0.4.12 README to v0.4.13 (dryfoos-sites `2a72872`), anchor verified live
at the tag. The step is now written into the sweep above.

**Signpost repaired 2026-09-04, same day:** one direct PR against all
three community catalog files, [github/spec-kit#4448](https://github.com/github/spec-kit/pull/4448),
bumping `version`, `download_url`, `updated_at`, and the extension's
`provides.commands` (2 to 5), exactly the fields the bot-generated
#4254/#4256/#4257 changed. One PR rather than three because the bundle
pins its component versions and a partial bump breaks `bundle install`
resolution. The extension and bundle guides document the issue route for
updates; if a maintainer redirects, the three paste-from docs are already
at 0.4.13 and the issues become the fallback. Also new this day:
unversioned release aliases (`specassay.zip`, `specassay-check.zip`,
`specassay-preset.zip`) so `releases/latest/download/<name>.zip` always
resolves; every community-facing install link now uses one, and
`release.yml` publishes them automatically. Catalog `download_url`s stay
versioned on purpose.

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

## Amending a filed issue (closed history, 2026-08-13 – 08-14) <!-- specassay:stale-ok closed history of the 0.3.x filings, kept as the record of how the bot behaved -->

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
