# The modified Spec Kit install test: a runbook

The clean-project install is already on record. This is the harder edge:
install SpecAssay over a Spec Kit project that already has local decisions in
it, then prove those decisions are still there.

This is a proposed test, not evidence that the property holds. Do not turn its
future result into a claim until the commands have been run and the retained
evidence has been reviewed.

**Time:** 30 to 45 minutes. **Exit:** the project is disposable, the bundle is
removed before deletion, and the complete local Git history is retained as
evidence. **Scope:** Spec Kit templates, workflow run state, integration files,
agent skills, commands, presets, extensions, and Gate 2.

## What you need

- A POSIX shell, Git, bash, and python3 3.8 or newer.
- A Spec Kit CLI build that provides `bundle`, `extension`, `preset`, and
  `workflow`, plus the Claude integration's `.claude/skills/` layout. Keep the
  same CLI build for the whole run and retain `specify --version`.
- Network access to the three hosted SpecAssay catalogs and release assets.
- No valuable files in the test directory. The commands below create their own
  temporary project.
- One shell session for the whole run. Later commands reuse `FIXTURE`,
  `EVIDENCE`, `RUN_ID`, `STOCK`, and `BASELINE`.

The fixture deliberately exercises three different kinds of prior state:

1. modified stock templates plus a supported project-local template override;
2. a modified stock Spec Kit skill, a custom skill, and a custom agent;
3. a real Spec Kit workflow run paused at a human gate.

The tiny PRD, spec, task, source, and proof files exist only so the installed
Gate can be run against something honest.

## Setup

1. **Create an isolated project and record the toolchain:**

   ```bash
   set -euo pipefail

   FIXTURE="$(mktemp -d "${TMPDIR:-/tmp}/specassay-compat.XXXXXX")"
   EVIDENCE="${FIXTURE}-evidence"
   mkdir -p "$EVIDENCE"
   export FIXTURE EVIDENCE

   cd "$FIXTURE"
   {
     date -u
     specify --version
     git --version
     python3 --version
   } | tee "$EVIDENCE/versions.txt"

   git init
   specify init --here --integration claude --script sh \
     --ignore-agent-tools | tee "$EVIDENCE/specify-init.txt"

   test -f .specify/templates/spec-template.md
   test -f .specify/templates/tasks-template.md
   test -f .specify/templates/constitution-template.md
   test -f .claude/skills/speckit-plan/SKILL.md

   git add -A
   git -c user.name="SpecAssay Fixture" \
     -c user.email="fixture@example.invalid" \
     commit -m "Stock Spec Kit fixture"
   STOCK="$(git rev-parse HEAD)"
   export STOCK
   ```

2. **Make the existing Spec Kit setup unmistakably local:**

   ```bash
   printf '\n<!-- COMPAT-FIXTURE: customized core spec template -->\n' \
     >> .specify/templates/spec-template.md
   printf '\n<!-- COMPAT-FIXTURE: customized core constitution template -->\n' \
     >> .specify/templates/constitution-template.md

   mkdir -p .specify/templates/overrides
   cp .specify/templates/tasks-template.md \
     .specify/templates/overrides/tasks-template.md
   printf '\n<!-- COMPAT-FIXTURE: project tasks override wins -->\n' \
     >> .specify/templates/overrides/tasks-template.md

   printf '\n<!-- COMPAT-FIXTURE: customized stock plan skill -->\n' \
     >> .claude/skills/speckit-plan/SKILL.md

   mkdir -p .claude/skills/team-review .claude/agents
   cat > .claude/skills/team-review/SKILL.md <<'EOF'
   ---
   name: team-review
   description: Run the fixture team's existing review command.
   user-invocable: true
   ---

   Preserve this command byte for byte.
   EOF

   cat > .claude/agents/team-reviewer.md <<'EOF'
   ---
   name: team-reviewer
   description: Existing fixture agent that must survive bundle installation.
   ---

   Review only the fixture team's local conventions.
   EOF
   ```

   The direct template edits test that installation does not rewrite the
   existing core files. The override tests Spec Kit's supported highest
   precedence customization path. It should remain authoritative rather than
   being replaced with either the stock or SpecAssay task template.

3. **Create a real paused workflow state:**

   ```bash
   mkdir -p .assay-fixture
   cat > .assay-fixture/team-paused-review.yml <<'EOF'
   schema_version: "1.0"
   workflow:
     id: "team-paused-review"
     name: "Team Paused Review"
     version: "1.0.0"
     author: "Fixture Team"
     description: "A local workflow whose paused state must survive installation."

   steps:
     - id: "keep-paused"
       type: "gate"
       message: "Leave this run paused for the compatibility test."
       options: ["approve", "reject"]
       on_reject: "abort"
   EOF

   specify workflow run .assay-fixture/team-paused-review.yml --json \
     > "$EVIDENCE/workflow-run.json"

   RUN_ID="$(python3 - "$EVIDENCE/workflow-run.json" <<'PY'
   import json
   import sys

   data = json.load(open(sys.argv[1], encoding="utf-8"))
   assert data["status"] == "paused", data
   print(data["run_id"])
   PY
   )"
   export RUN_ID

   specify workflow status "$RUN_ID" --json \
     | tee "$EVIDENCE/workflow-before-install.json"
   test -f ".specify/workflows/runs/$RUN_ID/state.json"
   ```

   Do not resume the run. Its `paused` status and persisted files are the
   workflow-state canary.

4. **Create the smallest Gate-clean work slice:**

   ```bash
   mkdir -p specs/001-compatibility src tests

   cat > PRD.md <<'EOF'
   # Compatibility fixture registry

   - FR-FIX-01: The disposable fixture preserves prior Spec Kit customization.
   - AC-FIX-01: Installing SpecAssay leaves every named prior-state canary unchanged.
   EOF

   cat > specs/001-compatibility/spec.md <<'EOF'
   # Compatibility fixture

   This slice carries FR-FIX-01 and AC-FIX-01.
   EOF

   cat > specs/001-compatibility/tasks.md <<'EOF'
   # Tasks

   - [x] T001 Add the fixture marker. **Carries**: FR-FIX-01, AC-FIX-01
   EOF

   cat > src/fixture.py <<'EOF'
   def prior_setup_is_present():
       # @covers FR-FIX-01, AC-FIX-01
       return True
   EOF

   cat > tests/test_fixture.py <<'EOF'
   from src.fixture import prior_setup_is_present


   def test_AC_FIX_01_prior_setup_is_present():
       assert prior_setup_is_present()
   EOF
   ```

5. **Commit the exact pre-install baseline:**

   ```bash
   git add -A
   git -c user.name="SpecAssay Fixture" \
     -c user.email="fixture@example.invalid" \
     commit -m "Deliberately modify Spec Kit fixture"
   BASELINE="$(git rev-parse HEAD)"
   export BASELINE

   git diff --binary "$STOCK" "$BASELINE" \
     > "$EVIDENCE/fixture-customizations.patch"
   git ls-tree -r "$BASELINE" \
     > "$EVIDENCE/baseline-tree.txt"
   printf 'FIXTURE=%s\nRUN_ID=%s\nSTOCK=%s\nBASELINE=%s\n' \
     "$FIXTURE" "$RUN_ID" "$STOCK" "$BASELINE" \
     > "$EVIDENCE/session.txt"

   PRESERVED=(
     .specify/integration.json
     .specify/templates/spec-template.md
     .specify/templates/constitution-template.md
     .specify/templates/overrides/tasks-template.md
     .claude/skills/speckit-plan/SKILL.md
     .claude/skills/team-review/SKILL.md
     .claude/agents/team-reviewer.md
     .assay-fixture/team-paused-review.yml
     ".specify/workflows/runs/$RUN_ID"
   )

   test -z "$(git status --porcelain)"
   ```

## Install the bundle

1. **Add only the catalogs the bundle needs and retain the install plan:**

   ```bash
   specify extension catalog add --name specassay --install-allowed \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/extensions.json
   specify preset catalog add --name specassay --install-allowed \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/presets.json
   specify bundle catalog add --id specassay --policy install-allowed \
     https://raw.githubusercontent.com/rdryfoos/specassay/main/catalogs/bundles.json

   specify bundle info specassay --json \
     > "$EVIDENCE/bundle-info-before-install.json"
   ```

   Review that JSON before continuing. The proposed SpecAssay bundle contains
   one preset and one extension. It contains no workflow or step.

2. **Install by bundle ID:**

   ```bash
   specify bundle install specassay \
     | tee "$EVIDENCE/bundle-install.txt"

   specify bundle list | tee "$EVIDENCE/bundle-list.txt"
   specify extension list | tee "$EVIDENCE/extension-list.txt"
   specify preset list | tee "$EVIDENCE/preset-list.txt"
   ```

## The compatibility checks

1. **Demand byte-for-byte preservation of every prior-state canary:**

   ```bash
   git diff --exit-code "$BASELINE" -- "${PRESERVED[@]}" \
     | tee "$EVIDENCE/preserved-paths.diff"

   test -f .claude/skills/speckit-plan/SKILL.md
   test -f .claude/skills/team-review/SKILL.md
   test -f .claude/agents/team-reviewer.md
   grep -Fq 'COMPAT-FIXTURE: customized stock plan skill' \
     .claude/skills/speckit-plan/SKILL.md

   test -d .specify/presets/specassay
   test -d .specify/extensions/specassay-check
   test -f \
     .claude/skills/speckit-specassay-check-gate/SKILL.md
   ```

   This is the central assertion. A restored stock file, a rewritten custom
   file, a changed active integration, or a changed workflow state fails here.
   The new Gate skill is allowed because its name did not exist in the
   baseline.

2. **Confirm the paused workflow is still the same paused workflow:**

   ```bash
   specify workflow status "$RUN_ID" --json \
     | tee "$EVIDENCE/workflow-after-install.json"

   python3 - \
     "$EVIDENCE/workflow-before-install.json" \
     "$EVIDENCE/workflow-after-install.json" <<'PY'
   import json
   import sys

   before = json.load(open(sys.argv[1], encoding="utf-8"))
   after = json.load(open(sys.argv[2], encoding="utf-8"))
   for key in ("run_id", "workflow_id", "status", "current_step_id"):
       assert before[key] == after[key], (key, before, after)
   assert after["status"] == "paused", after
   PY
   ```

3. **Check template resolution, not just files on disk:**

   ```bash
   bash -c \
     'source .specify/scripts/bash/common.sh; resolve_template_content "spec-template" "$PWD"' \
     > "$EVIDENCE/resolved-spec-template.md"
   bash -c \
     'source .specify/scripts/bash/common.sh; resolve_template_content "tasks-template" "$PWD"' \
     > "$EVIDENCE/resolved-tasks-template.md"
   bash -c \
     'source .specify/scripts/bash/common.sh; resolve_template_content "constitution-template" "$PWD"' \
     > "$EVIDENCE/resolved-constitution-template.md"

   grep -Fq 'COMPAT-FIXTURE: customized core spec template' \
     "$EVIDENCE/resolved-spec-template.md"
   grep -Fq 'SpecAssay (append)' \
     "$EVIDENCE/resolved-spec-template.md"

   grep -Fq 'COMPAT-FIXTURE: customized core constitution template' \
     "$EVIDENCE/resolved-constitution-template.md"
   grep -Fq 'Article: End-to-End Traceability' \
     "$EVIDENCE/resolved-constitution-template.md"

   grep -Fq 'COMPAT-FIXTURE: project tasks override wins' \
     "$EVIDENCE/resolved-tasks-template.md"

   specify preset resolve spec-template \
     | tee "$EVIDENCE/resolve-spec-stack.txt"
   specify preset resolve tasks-template \
     | tee "$EVIDENCE/resolve-tasks-stack.txt"
   specify preset resolve constitution-template \
     | tee "$EVIDENCE/resolve-constitution-stack.txt"
   ```

   The spec and constitution checks prove that SpecAssay's `append` strategy
   layers onto the customized lower template. The tasks override is different
   on purpose: project-local overrides have the highest precedence in Spec
   Kit, so that file remains the effective tasks template without being
   rewritten. If the team later wants SpecAssay's task prompt in that override,
   it can merge the addendum deliberately. Silent replacement is not an
   acceptable shortcut.

## Run the Gate

1. **Give the installed extension an explicit fixture config:**

   ```bash
   cat > \
     .specify/extensions/specassay-check/specassay-check-config.yml <<'EOF'
   registry: "PRD.md"
   target_name: "modified-spec-kit-fixture"
   manifest_path: "trace-manifest.json"
   specs: "specs/**/spec.md"
   tasks: "specs/**/tasks.md"
   src_globs:
     - "src/**"
   test_globs:
     - "tests/**"
   id_regex: "(FR|NFR|AC|US)-[A-Z][A-Z0-9]{1,5}-[0-9]{2,}[a-z]?"
   covers_regex: "@covers[[:space:]]+.*"
   carries_regex: "\*\*(Carries|Traces)\*\*:"
   test_ac_regex: "AC_[A-Z][A-Z0-9]{1,5}_[0-9]{2,}[a-z]?"
   EOF
   ```

2. **Run Gate 2 and inspect the emit:**

   ```bash
   SPECASSAY_PROJECT_ROOT="$PWD" \
   SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
     bash .specify/extensions/specassay-check/scripts/check-traceability.sh \
     2>&1 | tee "$EVIDENCE/gate.txt"

   cp trace-manifest.json "$EVIDENCE/trace-manifest.json"

   python3 - trace-manifest.json <<'PY'
   import json
   import sys

   manifest = json.load(open(sys.argv[1], encoding="utf-8"))
   assert manifest["format"] == "trace-manifest", manifest
   assert manifest["gate"]["ok"] is True, manifest["gate"]
   rows = {row["id"]: row for row in manifest["rows"]}
   assert rows["FR-FIX-01"]["status"] == "proven", rows["FR-FIX-01"]
   assert rows["AC-FIX-01"]["status"] == "proven", rows["AC-FIX-01"]
   assert not any(row["status"] == "GAP" for row in rows.values()), rows
   PY
   ```

   A passing Gate here proves only that the installed command is runnable and
   the fixture's declared thread is coherent. It does not prove preservation;
   the earlier Git and workflow assertions answer that separate question.

## Install it again

Spec Kit documents bundle installation as idempotent: components already
present are skipped. Test that property without using `bundle update`, which is
a refresh operation and answers a different question.

```bash
git add -A
git -c user.name="SpecAssay Fixture" \
  -c user.email="fixture@example.invalid" \
  commit -m "Installed SpecAssay fixture"
INSTALLED="$(git rev-parse HEAD)"
export INSTALLED

specify bundle install specassay \
  | tee "$EVIDENCE/bundle-reinstall.txt"

git diff --exit-code "$INSTALLED" \
  | tee "$EVIDENCE/reinstall.diff"
test -z "$(git status --porcelain)"

git diff --exit-code "$BASELINE" -- "${PRESERVED[@]}"
specify workflow status "$RUN_ID" --json \
  | tee "$EVIDENCE/workflow-after-reinstall.json"
```

Pass this section only if the second install exits zero, changes no file, keeps
the original customizations byte-for-byte, and leaves the workflow paused.
Do not require a particular prose message from the CLI; the exit status and
empty diff are the durable evidence.

## Tearing it out

First remove SpecAssay through its own lifecycle, then remove the catalogs that
were added by hand:

```bash
cp .specify/extensions/specassay-check/specassay-check-config.yml \
  "$EVIDENCE/specassay-check-config.yml"

specify bundle remove specassay \
  | tee "$EVIDENCE/bundle-remove.txt"
specify extension catalog remove specassay
specify preset catalog remove specassay
specify bundle catalog remove specassay

rm -f trace-manifest.json
rm -rf .specify/extensions/.backup/specassay-check
```

The backup removal is fixture-only cleanup. The config was copied to evidence
first. Do not generalize that command to a real project without reviewing the
backup.

Now demand that the prior setup, including the paused run, is exactly the
pre-install baseline:

```bash
test ! -e .specify/presets/specassay
test ! -e .specify/extensions/specassay-check
test ! -e .claude/skills/speckit-specassay-check-gate

git diff --exit-code "$BASELINE" \
  | tee "$EVIDENCE/tear-out.diff"
test -z "$(git ls-files --others --exclude-standard)"

git diff --exit-code "$BASELINE" -- "${PRESERVED[@]}"
specify workflow status "$RUN_ID" --json \
  | tee "$EVIDENCE/workflow-after-tear-out.json"

git bundle create "$EVIDENCE/fixture-history.bundle" --all
git diff --name-status "$BASELINE" \
  > "$EVIDENCE/final-baseline-status.txt"
```

Catalog download caches under `.specify/*/.cache/` are not project behavior.
Retain or delete them, but list any that remain in the test report. They must
not be confused with a preserved customization or a SpecAssay-owned component.

After the evidence has been reviewed, delete only the disposable fixture:

```bash
cd "$(dirname "$FIXTURE")"
case "$(basename "$FIXTURE")" in
  specassay-compat.*) rm -rf "$FIXTURE" ;;
  *) printf 'Refusing to delete unexpected path: %s\n' "$FIXTURE" >&2; exit 1 ;;
esac
printf 'Evidence retained at %s\n' "$EVIDENCE"
```

## The evidence we want

Retain the evidence directory intact. At minimum it should contain:

- exact Spec Kit, Git, and Python versions;
- the stock-to-customized fixture patch and both baseline commit IDs;
- the bundle's pre-install JSON plan and all install, list, and remove output;
- workflow status before install, after install, after reinstall, and after
  tear-out;
- resolved spec, tasks, and constitution templates plus resolution-stack
  output;
- the Gate transcript, explicit Gate config, and emitted
  `trace-manifest.json`;
- empty preservation, reinstall, and tear-out diffs;
- `fixture-history.bundle`, so the disposable repository can be reconstructed.

Record every non-zero exit and unexpected diff. Do not clean a failure until
its evidence has been copied out.

## Pass or fail

**Pass** only if every one of these is true:

1. The fixture was demonstrably modified before installation.
2. The first install added the SpecAssay preset, extension, and new Gate skill
   without changing the active integration or any named prior-state canary.
3. The paused workflow kept the same run ID, workflow ID, current step, stored
   files, and `paused` status.
4. Customized lower templates remained present in composed output, while the
   project-local tasks override remained authoritative and unchanged.
5. The custom agent, custom skill, and customized stock plan skill remained
   byte-for-byte identical.
6. Gate 2 ran from the installed extension, returned zero, and emitted a
   passing manifest with both fixture IDs proven and no GAP.
7. A second `bundle install specassay` returned zero and produced an empty
   worktree diff.
8. Bundle removal plus catalog cleanup removed only SpecAssay-owned material,
   and the complete project tree matched the pre-install baseline.
9. The retained evidence is sufficient for another reviewer to reconstruct
   what happened without trusting the operator's summary.

**Fail** on any overwrite, deletion, stock restoration, workflow transition,
integration change, command collision, non-idempotent reinstall, Gate failure,
tear-out residue that changes project behavior, or missing evidence. There is
no partial pass. A failure is the finding this runbook exists to surface.
