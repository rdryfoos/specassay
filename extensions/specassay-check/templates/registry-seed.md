# Registry

The one file that holds this project's durable IDs. Everything else in SpecAssay
reads it: the specs reference these IDs, the tasks carry them, the tests are named
for them, and the Gate refuses any promise here that nothing answers for.

Written by `mint-id.sh --init`. Edit it freely; it is yours from here. The Gate
reads this file by the `registry:` key in
`.specify/extensions/specassay-check/specassay-check-config.yml`, so renaming or
moving it means changing that key too.

## The grammar

```text
<TYPE>-<DOMAIN>-<NUMBER>
```

- **TYPE** is `US` (a story), `FR` (a functional requirement), `NFR` (a
  non-functional requirement) or `AC` (an acceptance criterion: one independently
  testable assertion).
- **DOMAIN** is 2 to 6 characters of your own choosing, uppercase, naming the area
  of the product the row belongs to: `GREET`, `AUTH`, `SYNC`. Rows sharing a domain
  are one family, and the Thread Report groups them that way.
- **NUMBER** is two or more digits, with an optional single lowercase letter for a
  sibling criterion: `AC-AUTH-10`, then `AC-AUTH-10a` beside it.

Primary numbers are minted on multiples of ten, and `1` to `9` off each decade is
reserved for resolving a collision between two branches that minted the same next
number. You never have to work any of this out: `mint-id.sh` composes the ID and
prints the line to paste.

```sh
bash .specify/extensions/specassay-check/scripts/mint-id.sh AC GREET \
  --authorship case \
  --append 'Given a name, when the greeter runs, then it returns "Hello, <name>!".'
```

An ID is minted once, at the moment the promise is made, and never renumbered: the
name is what ties a promise to the test that answers for it, so it has to hold
still. A row that is finished with is retired by a record on a task, never deleted
and never reused.

## One row of each kind

Copy a line out of this block and edit it. The block is fenced, so the Gate reads
it as a quotation rather than as four promises nobody made.

```markdown
- US-GREET-10 — As a visitor, I want to be greeted by name, so that the product feels like it knows me. **Authorship**: case
- FR-GREET-10 — The greeter renders a greeting from a supplied name. **Authorship**: design
- NFR-GREET-10 — The greeter answers within 50ms at the 99th percentile. **Authorship**: constitution
- AC-GREET-10 — Given a name, when the greeter runs, then it returns "Hello, <name>!". **Authorship**: design
```

`**Authorship**:` names **who authored the row**, in one of four words, and it is
set by a hand when the row is minted. **`case`**: the row states a promise from the
project's case, in the reader's words or on their behalf. **`design`**: a decision
you made rather than one you were asked for. **`retrospective`**: minted from a
defect or a review. **`constitution`**: a principle demanded it. A row with no
authorship is reported, not refused, so an unfilled registry is visible without
being blocked.

## Rows

