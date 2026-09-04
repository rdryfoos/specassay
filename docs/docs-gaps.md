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
