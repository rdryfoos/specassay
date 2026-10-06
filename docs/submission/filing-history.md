# Filing history, per component

Moved here 2026-10-06 so the three paste-from bodies carry nothing but the
values for the round being filed. This page is the record: which issue each
round was filed as, what closed it, and what each one superseded.

## Extension (specassay-check)

## Filing history <!-- specassay:stale-ok which issue numbers the past filings got; the numbers are the point and do not move -->

**Prepared 2026-10-06 at 0.5.6, not yet filed.** The fields below carry 0.5.6, read from the published release and from `catalogs/extensions.json`. Filing is a human step: it needs an issue opened on `github/spec-kit`, which the room that prepared this could not reach from its own session. It updates #4711.

**Landed 2026-09-24.** #4711 was closed by [github/spec-kit#4735](https://github.com/github/spec-kit/pull/4735), "[extension] Update SpecAssay Check extension to v0.5.2", opened by the submission workflow and merged the same day by KSchlobohm with all 17 checks passing. `extensions/catalog.community.json` on `main` now reads 0.5.2. No comment was ever posted on the issue; the verdict arrived as labels and a generated pull request.

**Filed 2026-09-23 at 0.5.2 as [github/spec-kit#4711](https://github.com/github/spec-kit/issues/4711), superseding #4690.** The fields below are what #4711 carries.

**Refused 2026-09-23 on the default-branch manifest mismatch, and superseded.** The validator read `bundle.yml` on `main`, which v0.5.2 had moved to 0.5.2, against a submission filed at 0.5.1, and asked for the 0.5.2 release with matching artifact and metadata. #4690 was pre-empted rather than left to fail the same way. The filing moves to 0.5.2 with the catalogs.

**Refiled 2026-09-23 as [github/spec-kit#4690](https://github.com/github/spec-kit/issues/4690), superseding #4649.** #4649 failed on the validator's fetch alone, twice; see the CHEATSHEET's
**v0.5.1 refiled** section for the run IDs and what each one meant. #4690
carried these fields at 0.5.1.

**Filed 2026-09-20 as [github/spec-kit#4649](https://github.com/github/spec-kit/issues/4649).**
A version-bump filing, not a first submission. The original (`v0.3.4`) merged as
#4113, closed via #4057; the `v0.4.12` update merged as #4254, filed as #4252.
Per the Extension Publishing Guide's "Updating an Existing Extension", an update
goes out as a **new** issue, never an edit to a closed one, and #4649 says in its
body that it updates #4252.

**Two skipped versions, stated plainly.** Neither `v0.4.13` nor `v0.5.0` was ever
filed on a submission form, so #4649 carries three releases of change and names
the last issue actually filed rather than a 0.4.13 or 0.5.0 issue, neither of
which exists.


## Preset (specassay)

## Filing history <!-- specassay:stale-ok which issue numbers the past filings got; the numbers are the point and do not move -->

**Prepared 2026-10-06 at 0.5.6, not yet filed.** The fields below carry 0.5.6, read from the published release and from `catalogs/presets.json`. Filing is a human step: it needs an issue opened on `github/spec-kit`, which the room that prepared this could not reach from its own session. It updates #4713.

**Landed 2026-09-24, first of the three.** #4713 was closed by [github/spec-kit#4717](https://github.com/github/spec-kit/pull/4717), "[preset] Update SpecAssay preset to v0.5.2", opened by the submission workflow and merged the same day by KSchlobohm. `presets/catalog.community.json` on `main` now reads 0.5.2, and the documentation row needed no change. No comment was ever posted on the issue; the verdict arrived as labels and a generated pull request.

**Filed 2026-09-23 at 0.5.2 as [github/spec-kit#4713](https://github.com/github/spec-kit/issues/4713), superseding #4691.** The fields below are what #4713 carries.

**Refused 2026-09-23 on the default-branch manifest mismatch, and superseded.** The validator read `bundle.yml` on `main`, which v0.5.2 had moved to 0.5.2, against a submission filed at 0.5.1, and asked for the 0.5.2 release with matching artifact and metadata. #4691 was pre-empted rather than left to fail the same way. The filing moves to 0.5.2 with the catalogs.

**Refiled 2026-09-23 as [github/spec-kit#4691](https://github.com/github/spec-kit/issues/4691), superseding #4650.** #4650 failed on the Documentation URL and the validator's fetch; see the CHEATSHEET's
**v0.5.1 refiled** section for the run IDs and what each one meant. #4691
carried these fields at 0.5.1.

**Filed 2026-09-20 as [github/spec-kit#4650](https://github.com/github/spec-kit/issues/4650).**
A version-bump filing. The `v0.4.12` update was filed as #4253 and merged as
catalog PR #4256, and #4650 says in its body that it updates #4253.

**The issue route works for presets.** An earlier reading of this file hedged
that `presets/PUBLISHING.md` documented only a direct catalog PR and that the
issue route might be redirected. That hedge is withdrawn: the issue route has now
carried the preset three times running, and the direct-PR alternative is the one
that gets closed. See the CHEATSHEET's **v0.5.1 filed** section.

**Two skipped versions, stated plainly.** Neither `v0.4.13` nor `v0.5.0` was ever
filed, so #4650 carries three releases of change.


## Bundle (specassay)

File this **third**, after the extension and preset issues, and name both in it.

## Filing history <!-- specassay:stale-ok which issue numbers the past filings got; the numbers are the point and do not move -->

**Prepared 2026-10-06 at 0.5.6, not yet filed.** The fields below carry 0.5.6, read from the published release and from `catalogs/bundles.json`. Filing is a human step: it needs an issue opened on `github/spec-kit`, which the room that prepared this could not reach from its own session. It updates #4715, and goes last of the three, after the component issues, because the bundle pins them.

**Landed 2026-09-24, last of the three.** #4715 was closed by [github/spec-kit#4737](https://github.com/github/spec-kit/pull/4737), "[bundle] Update SpecAssay bundle to v0.5.2", opened by the submission workflow and merged the same day by KSchlobohm at commit `ac53c9f`, with all 17 checks passing. It went last in both directions: filed third, validated third, merged third. With `bundles/catalog.community.json` on `main` at 0.5.2, the bundle install receipt that PR #48 could only rehearse became takeable, and was taken; it is in the CHEATSHEET under **The bundle install receipt**. No comment was ever posted on the issue; the verdict arrived as labels and a generated pull request.

**Filed 2026-09-23 at 0.5.2 as [github/spec-kit#4715](https://github.com/github/spec-kit/issues/4715), superseding #4692,** after the extension ([#4711](https://github.com/github/spec-kit/issues/4711)) and the preset ([#4713](https://github.com/github/spec-kit/issues/4713)). The fields below are what #4715 carries.

**Refused 2026-09-23 on the default-branch manifest mismatch, and superseded.** The validator read `bundle.yml` on `main`, which v0.5.2 had moved to 0.5.2, against #4692 filed at 0.5.1, and asked for the 0.5.2 release with matching artifact and metadata. This is the issue that caught it; #4690 and #4691 were pre-empted. The filing moves to 0.5.2 with the catalogs.

**Refiled 2026-09-23 as [github/spec-kit#4692](https://github.com/github/spec-kit/issues/4692), superseding #4651,** after the extension (#4690) and the preset (#4691).
#4651 failed on the version-string mismatch and the validator's fetch; see the
CHEATSHEET's **v0.5.1 refiled** section for the run IDs and what each one meant.
#4692 carried these fields at 0.5.1.

**Filed 2026-09-20 as [github/spec-kit#4651](https://github.com/github/spec-kit/issues/4651),**
after the extension (#4649) and the preset (#4650). A version-bump filing: the
`v0.4.12` update was filed as #4255 and merged as catalog PR #4257, and #4651
says in its body that it updates #4255.

**Two skipped versions, stated plainly.** Neither `v0.4.13` nor `v0.5.0` was ever
filed, so #4651 carries three releases of change.


## The declared Spec Kit range, and how it closed

Carried in all three bodies from 2026-09-20 until today. The three manifests
inside the zips declared `>=0.14.0,<2.0.0` while `catalogs/*.json` published the
same floor with no upper bound, so a catalog claimed a wider range than the zip
inside it. Ruled
closed 2026-09-23: an issue is written from the manifests, and every
declaration inside one issue must match, because a divergence inside a single
issue is what failed #4651.

**Observed 2026-10-06 <!-- specassay:provenance -->, and now agreed everywhere.** All six declarations, the three
manifests and the three catalogs, read `>=0.14.0,<2.0.0`. The note is retired
rather than carried: there is nothing left for it to warn about.
