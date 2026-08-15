---
description: Mint the next durable ID for a prefix and area (e.g. AC HOME), or resolve a duplicate-id Gate refusal
argument-hint: "<PREFIX> <AREA> [--append \"statement text\"]  |  --resolve <DUPLICATE-ID>"
---

# SpecAssay Mint

Mints the next ID for a prefix (`FR`/`NFR`/`AC`/`US`) and area by scanning
the registry for the highest existing number, so nobody has to eyeball the
file and guess. Also resolves a `duplicate-id` Gate refusal.

## User Input

```text
$ARGUMENTS
```

## Steps

1. Confirm `.specify/extensions/specassay-check/specassay-check-config.yml`
   exists (copy from `config-template.yml` if missing) and its `registry`
   field points at this project's registry file.
2. **If the registry file itself does not exist yet** (first mint in a new
   project): create it empty (`touch <registry-path>`). The first mint
   below will fall back to a plain `- ID — statement` line style since
   there is no existing line to imitate; that is expected and fine.
3. Parse `$ARGUMENTS`:
   - `<PREFIX> <AREA>`, optionally followed by `--append "statement text"`
     — mints the next primary ID (a multiple of ten past the highest
     existing number for that prefix+area; a brand-new area starts at 10).
     Without `--append`, only the new ID is printed; nothing is written.
   - `--resolve <DUPLICATE-ID>` — given an ID the Gate flagged as
     `duplicate-id`, prints the next free offset in that decade's reserved
     `1`-`9` lane (e.g. `AC-HOME-20` → `AC-HOME-21`). Only accepts a
     multiple-of-ten input; rejects anything else with a clear error.
4. From the project root, run:

   ```sh
   SPECASSAY_PROJECT_ROOT="$PWD" \
   SPECASSAY_CONFIG="$PWD/.specify/extensions/specassay-check/specassay-check-config.yml" \
     bash .specify/extensions/specassay-check/scripts/mint-id.sh $ARGUMENTS
   ```

5. Report the ID mint-id.sh prints. If `--append` was used, the registry
   file now has the new line; if not, mint again with `--append` once the
   statement text is ready — re-running without having written anything
   is safe and does not skip a number.
