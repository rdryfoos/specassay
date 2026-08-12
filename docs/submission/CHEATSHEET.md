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
