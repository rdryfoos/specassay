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
- Release with artifacts: <https://github.com/rdryfoos/specassay/releases/tag/v0.3.2>
- Catalogs: <https://github.com/rdryfoos/specassay/tree/main/catalogs>
- Extension README: <https://github.com/rdryfoos/specassay/blob/main/extensions/specassay-check/README.md>
- Preset contract: <https://github.com/rdryfoos/specassay/blob/main/PROMOTION-CONTRACT.md>

Expected turnaround: a maintainer validates catalog entry and URLs in 3–7
business days (they do not audit code). A version update later is a new
issue noting it updates the existing entry.

## Amending a filed issue (2026-08-13: the v0.3.2 metadata fix)

The three issues are filed and validated; each has a maintainer-approved
catalog PR behind it. They are **edited in place**, not refiled. On
2026-08-13 KSchlobohm asked for consistent author metadata across the
release assets, so v0.3.2 republished them and these fields need to
follow.

Open each issue, click the `...` menu (top right of the first comment),
choose **Edit**, and change only these two fields:

| Issue | Field | New value |
| --- | --- | --- |
| [#4057 extension](https://github.com/github/spec-kit/issues/4057) | Version | `0.3.2` |
| | Download URL | `https://github.com/rdryfoos/specassay/releases/download/v0.3.2/specassay-check-0.3.2.zip` |
| [#4058 preset](https://github.com/github/spec-kit/issues/4058) | Version | `0.2.1` |
| | Download URL | `https://github.com/rdryfoos/specassay/releases/download/v0.3.2/specassay-preset-0.2.1.zip` |
| [#4059 bundle](https://github.com/github/spec-kit/issues/4059) | Version | `0.3.2` |
| | Download URL | `https://github.com/rdryfoos/specassay/releases/download/v0.3.2/specassay-0.3.2.zip` |

The bundle issue also lists its components; set those to
`specassay-check@0.3.2` and `specassay@0.2.1`. Everything else on all
three forms stays as filed. The paste-from docs above already carry
these values if you would rather copy whole fields.

Then reply once, on [#4059](https://github.com/github/spec-kit/issues/4059),
where the request was made:

> Fixed. The author field was already "Rik Dryfoos" on `main`, but the
> v0.3.1 assets were built before that landed. v0.3.2 republishes all
> three with matching metadata in `extension.yml`, `preset.yml`, and
> `bundle.yml`; catalog entries and the submission issues here are
> updated to match.
>
> - specassay-check 0.3.2: `https://github.com/rdryfoos/specassay/releases/download/v0.3.2/specassay-check-0.3.2.zip`
> - specassay (preset) 0.2.1: `https://github.com/rdryfoos/specassay/releases/download/v0.3.2/specassay-preset-0.2.1.zip`
> - specassay (bundle) 0.3.2: `https://github.com/rdryfoos/specassay/releases/download/v0.3.2/specassay-0.3.2.zip`

Note the open catalog PRs (#4069, #4070, #4072) were generated from the
issue bodies as filed, so they carry the old versions until a maintainer
regenerates or updates them. Editing the issues is the part that is
yours; the PRs are theirs.
