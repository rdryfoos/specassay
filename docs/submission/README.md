# Submission package — status and checklist

**Filing today? Start with the [cheat sheet](https://github.com/rdryfoos/specassay/blob/main/docs/submission/CHEATSHEET.md)** — three links, three pastes.

Everything Spec Kit's community submission process asks for, what state it's
in, and what remains. The submission path is **issues, not PRs**: file one
issue per component using Spec Kit's templates; a maintainer validates the
catalog entry and URLs (3–7 business days; they do not audit code).

## What's done ✅

| Item | Where | Verified |
| --- | --- | --- |
| `bundle.yml` / `extension.yml` / `preset.yml` manifests | repo root, `extensions/specassay-check/`, `presets/specassay/` | `specify bundle validate` ✓ |
| Versioned release with the `specify bundle build` artifact | [v0.3.1](https://github.com/rdryfoos/specassay/releases/tag/v0.3.1): `specassay-0.3.1.zip` + component packs | built in CI by the real CLI |
| Hosted catalogs with live download URLs | [`catalogs/*.json`](https://github.com/rdryfoos/specassay/tree/main/catalogs) | assets download and install ✓ |
| Clean-project install, end to end, by bundle ID | — | [test-evidence.md](https://github.com/rdryfoos/specassay/blob/main/docs/submission/test-evidence.md) |
| LICENSE (MIT) · README · CHANGELOG | repo root | — |
| Command namespace rule (`speckit.{extension-id}.{command}`) | `speckit.specassay-check.gate` | installer accepts ✓ (it refused the old name — see CHANGELOG 0.3.1) |
| Paste-ready issue bodies | [bundle](https://github.com/rdryfoos/specassay/blob/main/docs/submission/bundle-submission.md) · [extension](https://github.com/rdryfoos/specassay/blob/main/docs/submission/extension-submission.md) · [preset](https://github.com/rdryfoos/specassay/blob/main/docs/submission/preset-submission.md) | mirror the actual issue-form fields |

## What a human does (the actual filing) 🖐

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
   them.

## Cutting the next release 🔁

Bump versions in the three manifests + `catalogs/*.json` (and refresh the
catalog entries inlined in the three issue bodies here), update
CHANGELOG.md, then run the **Release** workflow
(`Actions → Release → Run workflow`) with the new tag (e.g. `v0.4.0`) — it
creates the tag, validates and builds with the real CLI through the hosted
catalogs, and publishes the assets the catalogs point at. (Tag pushes also
trigger it, where the git remote allows tag pushes.)

For a version update in the community catalog: file a new submission issue
noting it's an update to the existing entry.
