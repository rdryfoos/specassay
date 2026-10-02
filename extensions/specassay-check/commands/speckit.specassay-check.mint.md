---
description: Mint the next durable ID for a prefix and area (e.g. AC HOME), or resolve a duplicate-id Gate refusal
argument-hint: "--init  |  <PREFIX> <AREA> [--authorship <value>] [--append \"statement text\"]  |  --resolve <DUPLICATE-ID>"
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
   exists and its `registry` field points at this project's registry file.
   If it is missing, the script says so and prints the `cp` command that
   scaffolds it from `config-template.yml`; run that once.
2. **If the registry file itself does not exist yet** (first mint in a new
   project): run `mint-id.sh --init`. It writes the registry from the seed the
   extension ships, which states the ID grammar in full and carries one fenced
   example row of each kind. `--init` never overwrites an existing registry; it
   refuses and names the file. Do not create the file empty: the seed is what a
   person reads to learn what a row looks like, and a fenced example row is a
   quotation rather than a promise, so a Gate run on the untouched seed is green
   with zero rows.
3. Parse `$ARGUMENTS`:
   - `<PREFIX> <AREA>`, optionally followed by `--authorship <value>` and
     `--append "statement text"`, in either order — mints the next primary ID (a
     multiple of ten past the highest existing number for that prefix+area; a
     brand-new area starts at 10). The whole line to paste is always printed;
     without `--append` nothing is written.
   - `--authorship` takes one of `case`, `design`, `retrospective` or
     `constitution` and writes `**Authorship**: <value>` on the minted line. It
     is the one field the tool will not fill in: ask the person which it is
     rather than choosing for them. A fifth value is refused. With no value the
     row reads as unassigned, which the Gate reports and does not refuse.
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

5. Report the ID mint-id.sh prints on stdout, and the whole line it prints
   beside it. If `--append` was used, the registry file now has that line; if
   not, mint again with `--append` once the statement text is ready — re-running
   without having written anything is safe and does not skip a number.
