# Docs-gaps list

Running log for the docs room (opened 2026-08-18). Working method: the
room's own cold start is the instrument — every question about SpecAssay
that can't be answered from the repo alone is a gap, logged here before
it's resolved. This is FR-DOCS-30's raw material: each troubleshooting
entry it eventually produces should cite the incident here that taught it.

Format per entry: what broke, how it was found, resolution (or `open` if
still unresolved), and the commit that closed it.

## Resolved

1. **Two dead links in the public quickstart.** `README.md`'s "Does it work
   cold? / Want to test it on real work?" sentence linked
   `./docs/evidence-cold-agent-trial.md` and `./docs/real-work-test.md`;
   neither existed. Found by cold-reading `README.md` top to bottom as a
   cold installer would. Real files: `docs/testing/completed/
   evidence-cold-agent-trial.md` (itself moved out of a literally-named
   `docs/testing/*completed/` directory) and `docs/testing/4-real-work-test.md`.
   Resolved: commit `de6995b` (docs: fix two dead README quickstart links).
2. **`orphan-covers` has no domain-scoping, unlike `orphan-spec`/`orphan-task`.**
   Founding this repo's own registry (`PRD.md`, 2026-08-18) with `docs/**`
   in `src_globs` failed the Gate immediately — not on real drift, but on
   `docs/testing/*.md` trial write-ups quoting other projects' `@covers`
   lines as teaching examples (`AC-HOME-15`, `FR-HOME-04`, `AC-FIX-01`,
   etc.), plus a coverage-regex false match inside `check-traceability.sh`'s
   own comment. The spec/task orphan checks already had `is_local_domain()`
   to tell a citation apart from a real claim; `orphan-covers`/`orphan-test`
   never got the same scoping. Fixed as `FR-GATE-40` (design room,
   2026-08-18): `is_local_domain()` now gates both checks the same way, and
   a new `strip_code_spans()` blanks markdown fenced-code-block and
   inline-backtick content before `@covers`/test-name extraction runs —
   the domain check alone can't catch a project quoting its *own* real ID
   as a teaching example, which is exactly what DOCS-room docs will do.
   Verified against the real repo (restoring `docs/**` now passes clean)
   and against three scratch fixtures: a same-domain quote inside an inline
   span and a fenced block (both correctly ignored), and a real unfenced
   mark in a docs file (still detected, `proven`). Companion `FR-DOCS-50`
   (restore `docs/**` to `src_globs`) shipped in the same pass — see
   `PRD.md` and `specs/self-gate-config/spec.md`.
3. **Manifest emitter double-counted implementations/proofs.** Found while
   fixing the above: `impl_by[id_].append(...)` had no dedup, unlike the
   `debt_by` loop right next to it, which already deduped on
   `(path, line, id_)`. Overlapping `src_globs` entries or a `./x` vs `x`
   glob spelling hand `expand_glob()` the same file under two literal path
   strings, so the same mark got appended twice — a real emit carried the
   bug in 62 of 100 rows. Fixed as `FR-GATE-50`: dedup on
   `(id, normpath(path), line)` before appending, applied to both
   `impl_by` and the identically-unguarded `proof_by`. Verified against a
   scratch fixture reproducing the exact `./ios/...` vs `ios/...` shape
   (collapsed to one entry) and a second fixture confirming two genuinely
   different marks for the same ID are not over-collapsed.

## Open

4. **CLI version skew, real and already biting.** The design room's
   independent `v0.4.12` cold-install trial (2026-08-20, Linux container,
   fully disjoint from the Mac trial) installed `specify` fresh from
   source the same day and got `0.16.6.dev0` — `init`'s flags had already
   changed since the Mac trial's `0.15.3.dev0` (`--no-git` and `--ai` both
   gone). Neither this repo's quickstart nor `docs/migration.md` pins a
   `specify` version or calls out which flags are version-specific;
   a cold installer following the docs today meets a CLI neither trial's
   evidence was written against. Not yet resolved: needs a decision on
   whether to pin a version, or state the docs are flag-minimal by design
   and let Spec Kit's own docs own CLI-flag currency.
   <!-- specassay:stale-ok the record of one trial and of the CLI it met; re-observing it would delete the skew this item exists to report -->
5. **`specify extension add --from` rejects local paths and `file://`.**
   Found in the same trial: only `https://` URLs work. Not documented
   anywhere in this repo — worth one line in `docs/troubleshooting.md` so
   someone who tries a local zip during development doesn't read the
   rejection as a broken build.
6. **The "20 minutes" install claim doesn't account for interactive
   prompts or first-fetch latency.** Same trial: `specify init` and
   `specify extension add` both prompt interactively, and the first
   `https` catalog fetch ran long. Neither is a defect, but the README's
   "Install in 20 minutes" framing (and the `specassay.com` CTA of the
   same name) implicitly assumes a fast, unattended run. Worth a line
   somewhere naming the friction, or softening the claim.

7. **Inputs for ONBOARD.md, from the 2026-09-03 and 2026-09-04
   commissions.** No onboarding doc exists yet; when its commission runs,
   these are the facts it inherits, each verified in a clean `specify init`
   project and recorded in `docs/submission/test-evidence.md` (v0.4.13) or
   `extensions/specassay-check/README.md`:
   - `specify bundle install specassay` (the README's catalog path) does
     **not** scaffold `specassay-check-config.yml`; `specify extension add`
     does. The Gate's first lines say which state you are in and print the
     one `cp` command that fixes it. The onboarding doc should tell readers
     to read those three lines before anything else, and never claim the
     config "was scaffolded on install" without saying by which command.
   - Green on an empty registry is the first thing a cold installer sees,
     and it means nothing. Onboarding starts from "you are green and it
     proves nothing" and walks to the first honest red; red is the
     tutorial, not the failure case.
   - Brownfield is the more common first state (existing docs, no IDs).
     The on-ramp is "point `registry:` at the doc you already have, or
     mint one ID that cites it", never backfill. Say that before the
     greenfield story. `dig` is not the first instruction for that reader
     until `FR-DIG-80/90/100` ship (`T921`).
   - Every step's output belongs in the doc verbatim; readers compare
     their screen to the page. The exact refusal after the first mint and
     the exact status after each way of clearing it are the lesson.
   - The status ladder for one ID, as a table: open task alone is
     `backlog`; add a spec and it is `tracked-debt`; add the named test and
     it is `proven`; spec and test with no task is a refusal. Verified
     2026-09-03 by running all four.
   - The upgrade command is two lines and the first is not optional
     (`docs/migration.md`, "The upgrade command that works"); the raw
     catalog URL lags a push by up to five minutes (friction 4).
   - Prerequisites and platforms as the root README's "Before you install"
     now states them: Spec Kit first, three installs by design, macOS and
     Linux first-class, Windows under Git Bash or WSL, Python found as
     `python3` or `python`.

   **Resolved 2026-09-15** by `ONBOARD.md` (rung one of the onboarding
   ladder: blank session to a first Thread Report in one short sitting).
   Every input above is carried: the Gate's own three setup lines are what
   the reader is told to read first; empty-green opens the walk and says it
   proves nothing; the brownfield first move is stated before the reader
   mints anything of their own; every receipt is that run's real output;
   the status ladder appears as a table, all five lines re-run and verified
   the same day. Two inputs are deliberately not carried: the upgrade
   command (rung one installs cold, it never upgrades) and `dig` (still
   not the first instruction for a brownfield reader). The whole document
   was verified by extracting its own paste-blocks and running them in
   order in a clean project, against SpecAssay v0.4.13 and Spec Kit v1.0.4.
   It quotes no duration: no cold operator has produced a measured one yet,
   and the document asks its first one for it.

8. **`thread-report.py` mangles dotted paths.** `norm()` is
   `p.lstrip("./")`, which strips *characters*, not a prefix, so any path
   whose first segment starts with a dot loses it: a changed `.gitignore`
   renders in the Off Thread list as `gitignore`, and
   `.github/workflows/ci.yml` would render as `github/workflows/ci.yml`.
   Found 2026-09-15 while writing `ONBOARD.md`, in a real report from the
   tour project (the quickstart now commits `.gitignore` before the
   comparison point, so the tour never displays it). Display is the visible
   half; the same normalization feeds on-thread/off-thread matching, so a
   dotfile governed by a `specs`/`tasks` glob could bucket wrong too. Open:
   the fix is a prefix strip (`p[2:] if p.startswith("./") else p`), and it
   wants a named test before it lands.

9. **The agent commands are `/speckit-specassay-check-gate`, not
   `speckit.specassay-check.gate`, for a Claude Code install.** The root
   README and the extension README both spell the commands with dots. On
   Spec Kit 1.0.4 with `--integration claude`, `specify bundle install`
   writes them as Claude Code *skills* at
   `.claude/skills/speckit-specassay-check-{gate,mint,matrix,portfolio,dig}/SKILL.md`,
   and that hyphenated name is what the reader can actually type. Found
   2026-09-15 in the `ONBOARD.md` verification run. Open: the dotted form
   may still be right for other integrations, so this needs one line saying
   the spelling follows your agent, not a blanket find-and-replace.

10. **The Gate's own CI filter did not cover the docs the Gate reads.**
    `.github/workflows/self-gate.yml`'s `pull_request` trigger was
    path-filtered to `PRD.md`, `specs/**`, `extensions/specassay-check/**`,
    `presets/specassay/**`, and `specassay-check-config.yml`. None of the
    four documentation paths in this repo's own `src_globs` was listed:
    `README.md`, `ONBOARD.md`, `docs/**`, `PROMOTION-CONTRACT.md`. Those
    files are scanned for live `@covers` marks, so a docs-only PR could
    orphan a mark or remove a row's last carrier and still show green
    checks at review time; the refusal would land only after merge, on the
    unfiltered `push` trigger. Found 2026-09-15 on PR #7: it changed only
    `ONBOARD.md`, no Self Gate run was created for its head, and the only
    status on the PR was a review bot's skip. PR #8, the title-and-sweep
    change, went through the same hole the same day. The irony is the
    point: this repo's own README says CI is the property line, and the
    property line had a gate on the driveway and none on the footpath.
    Resolved: the four paths added to the filter, verified by the Gate
    running at PR time on the very PR that adds them (it touches
    `docs/**`). The `push` trigger stays unfiltered, so `main` was never
    unprotected. **Closed in full 2026-09-15**, in two rulings: the four
    documentation paths first, then `.github/workflows/*` after PR #10
    became the second workflow-editing PR in a day to reach a hand merge
    with no PR-time Gate run of its own. A change to how the Gate runs is
    a change to whether the Gate runs, so it now re-runs the Gate. The
    glob is deliberately `*` and not `**`: these workflows are flat files
    in one directory, and a shallow glob says so rather than promising to
    watch a tree that does not exist.

    **Reopened and closed differently, 2026-09-18.** It came back. The
    2026-09-15 fix named the four documents that existed then, which is
    the only thing a list can do. Three root-level pages were born after
    it (`FIRST-LIGHT.md`, `FIRST-LIGHT-NOTES.md`, `CASE-TEMPLATE.md`),
    each joined the version checker's governed set, none joined this
    filter, and PR #32 touched only `FIRST-LIGHT.md` and produced no
    checks at all. Worse than the original shape: there a reviewer saw
    green that meant nothing, here they see an empty check list, which
    reads as "none required" rather than "none ran".

    Two lists needed a human to remember them, in two files, and they had
    drifted by three entries. Both are deleted rather than synchronised:
    the `pull_request` path filter is gone, so Self Gate runs on every
    pull request, and root-level documents are governed by glob rather
    than by name. The cost was measured rather than assumed before
    deleting the filter: fourteen real runs span 23 to 35 seconds, median
    28, one billed minute each, on a public repository where Actions
    minutes are free.

    The lesson, which is the part that outlives both fixes: closing this
    by extending a list was closing it at the altitude of the instances
    rather than of the cause. The second occurrence was in the design of
    the first repair.

11. **`ONBOARD.md`'s receipts were pinned to v0.4.13 while the catalogs moved
    on.** **Closed 2026-09-17.** The quickstart's contract is that every block's
    quoted output is that block's real output from one run against the pinned
    versions, never a sketch. That run had happened on 2026-09-15 against
    v0.4.13, and two releases landed after it, so a reader following the page
    installed a version the page was not captured on. For a week the divergence
    was named in a note under the pin table rather than papered over, because
    re-pinning the table without re-running the sitting would have broken
    requirement one of the commission that wrote the page.

    Resolved the way the entry always said it had to be: by re-running it. All
    twelve blocks were replayed in order on v0.5.1 on 2026-09-17, installing
    through the documented catalog path, and **every receipt reproduced
    unchanged**. The pin table now names v0.5.1 and the divergence note is gone,
    because there is no divergence left to name. That the receipts held is worth
    recording and is not the same as having assumed they would: the assumption
    was stated in this entry for a week, and it is now a measurement.

    One incident worth keeping from the replay, since it is what a cold reader
    could hit: `specify bundle install specassay` failed once with
    `HTTP Error 500` fetching the preset asset from GitHub, and said
    `No changes were recorded`. Both asset URLs returned 200 when probed
    directly a moment later and the retry installed cleanly, so it was transient
    on GitHub's side rather than a defect here. The CLI's own behaviour was
    correct: it refused to record a partial install.

12. **Version numbers and receipts are written by hand into prose and go stale
    silently at every cut.** Open, 2026-09-17. Items 8 and 11 above, the README's
    Spec Kit compatibility line, and the README's clean-project verification line
    are four instances of one failure: a number observed once, typed into a
    sentence, and then left to rot while the thing it describes moves. Each cut
    has been patched by hand afterwards, which works and does not scale.
    **Closed 2026-09-18** by `scripts/check-doc-versions.py`, which refuses a
    governed document that states a version without saying which kind of claim
    it is making. Registered as `FR-DOCS-70`. The proposal, the ruling, and what
    the proposal got wrong are in `docs/version-assertion-proposal.md`.
    **Widened 2026-09-18** from ten governed documents to the whole repository
    except the fixture project: 54 documents, 47 refusals before the sweep, 0
    after. No new lie was found, and two more corrections to the checker were,
    both forced by the corpus rather than by thought. Same file for both.
