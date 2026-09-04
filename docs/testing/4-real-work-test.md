# The real-work test: a runbook

You ran the twenty-minute cold install and the tool didn't scare you off.
This is the bigger test: put SpecAssay on work you actually care about and
let the PR comment earn its keep over a handful of pull requests.

**Time:** 20 to 30 minutes of setup, then no ceremony beyond three
one-line habits. **Exit:** one command uninstalls the bundle, any time
(see the last section; the path is tested). **Privacy:** the tool writes
only into your repo and phones nothing home. Nobody needs to see your
code; the feedback we want is your impressions.

## What you need

- A GitHub repo with Actions enabled, where real PRs happen.
- Spec Kit 0.14 or newer with any agent integration; bash (macOS, Linux,
  or Git Bash/WSL on Windows); Python 3.8 or newer, found as `python3` or
  `python`.
- Requirements written as acceptance criteria while you build (stock
  Spec Kit flow).

**Brownfield is welcome, and is its own experiment.** Do not backfill
the legacy code. Start with an empty registry, mint IDs only for new
requirements, mark only new work, and let the thread grow at the edges.
Legacy files will show up as "off the thread," which is true, and part
of what we want to observe.

## Setup

1. **Install the bundle** in your project root:

   ```bash
   specify extension catalog add --name specassay \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json
   specify preset catalog add --name specassay \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json
   specify bundle catalog add --id specassay --policy install-allowed \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json
   # set install_allowed: true in .specify/extension-catalogs.yml and
   # .specify/preset-catalogs.yml, then:
   specify bundle install specassay
   ```

2. **Create the Gate config** at your project root:

   ```bash
   cp .specify/extensions/specassay-check/config-template.yml specassay-check-config.yml
   ```

   Edit it for your layout. The three fields that matter: `registry`
   (where your requirement IDs live, usually the PRD), `src_globs`, and
   `test_globs`. Brownfield note: pointing `src_globs` at only your new
   code's tree is a legitimate scoping move.

3. **Run the Gate once locally** before wiring CI, so config problems
   surface on your machine and not in a workflow log:

   ```bash
   bash .specify/extensions/specassay-check/scripts/check-traceability.sh
   ```

   It writes `trace-manifest.json` and exits non-zero only on a silent
   gap (a criterion with neither a named test nor an open TODO). On a
   fresh registry it should pass quietly.

4. **Wire the PR comment.** Copy two workflow files from this repo into
   your `.github/workflows/`:
   [`thread-report.yml`](../.github/workflows/thread-report.yml) and
   [`ack-gate.yml`](../.github/workflows/ack-gate.yml). They ship
   pointed at this repo's bundled example app, so adjust three things
   for your project: the `on.pull_request.paths` trigger, the
   `SPECASSAY_PROJECT_ROOT` / `SPECASSAY_CONFIG` paths, and the script
   path (in your repo the script lives at
   `.specify/extensions/specassay-check/scripts/check-traceability.sh`).
   If this adjustment fights you, that is exactly the feedback we want;
   note where.

## The three habits

Everything else is machinery. The practice you are testing is:

1. When a requirement is written down, it gets a permanent ID (the
   installed templates prompt for this).
2. Code written to satisfy it carries a one-line comment:
   `@covers AC-XXX-01`.
3. The test that answers for it carries the ID in its test name:
   `test_AC_XXX_01_...`.

And the honest fourth: when a proof is still owed, say so on an open
task with `**Carries**: AC-XXX-01` instead of leaving silence. The Gate
treats admitted debt as honest and silence as a refusal.

## Live with it

Work normally for three to five PRs. Read the Thread Report comment on
each one. Do not perform for the tool; the test is what it feels like
when you forget about it.

## The feedback we want

Impressions, not code. The questions, roughly in order of value:

1. Did "What moved" match your own mental diff of the PR, or surprise
   you? Surprises in either direction are the finding.
2. Was the off-thread list useful attention or noise? Did anything land
   there that deserved a mark, or carry a mark it did not deserve?
3. Did the Gate ever refuse wrongly? A false refusal is the worst bug we
   could have; please describe it in detail.
4. Did the three habits survive deadline pressure? Which one slipped
   first?
5. If a requirement's wording changed mid-test: did the Intent Changed
   section catch it, and did the re-confirm pointer help?
6. Where did the docs lose you?

Send it however you like: email rik@dryfoos.com, or open an issue on
this repo.

## Tearing it out

The uninstall path is tested (install, remove, diff against a pristine
tree):

```bash
specify bundle remove specassay
specify extension catalog remove specassay
specify preset catalog remove specassay
specify bundle catalog remove specassay
```

That removes everything the bundle installed. Three things remain, all
yours by then: the two workflow files you copied by hand (delete them),
the `specassay-check-config.yml` you created (delete it), and any
`@covers` marks, test names, and IDs you wrote in your own files, which
are inert comments and names that harm nothing if left. Cached catalog
JSON under `.specify/*/.cache/` can be deleted or ignored.
