# Filing cheat sheet — three issues, in this order

Each row: open the **form**, then copy everything below the `---` rule in the
**paste-from** doc into it. The forms are GitHub issue templates on the
Spec Kit repo; the paste-from docs mirror their fields exactly, catalog JSON
included — no other tabs needed.

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
- Release with artifacts: <https://github.com/rdryfoos/specassay/releases/tag/v0.3.3>
- Catalogs: <https://github.com/rdryfoos/specassay/tree/main/catalogs>
- Extension README: <https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md>
- Preset contract: <https://github.com/rdryfoos/specassay/blob/main/PROMOTION-CONTRACT.md>

Expected turnaround: a maintainer validates catalog entry and URLs in 3–7
business days (they do not audit code). A version update later is a new
issue noting it updates the existing entry.

## Amending a filed issue

The three issues are filed and validated; each has a generated catalog PR
behind it. They are **edited in place**, not refiled: open the issue, use
the `...` menu on the first comment, choose **Edit**.

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
