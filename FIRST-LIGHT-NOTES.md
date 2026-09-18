# FIRST-LIGHT: the notes behind the page

This is the record that FIRST-LIGHT.md is built from: what was observed, on what date, by whom,
and why each choice in the page is the choice it is. The page is the instruction; this is the
evidence.

The split exists because a human ran the fourth version of the page cold and gave up before the
end. His words: "this is a lot and mostly I do not care, I just want the next steps." Every
explanation in that page had been added for a real reason and each one was true. Together they
buried the instruction. So the page now carries only what changes what a reader does next, and
everything else lives here.

Nothing was dropped in the move. A claim that is not in the page is still a claim this practice
stands behind; it is simply not in the reader's way.

<!-- specassay:pinned Claude Code -->

## How the page was tested

| When | Who | Through what | What it produced |
|---|---|---|---|
| 2026-09-17 | a session | the desktop app's terminal, fresh non-admin account | the first receipts: installer output, the two-sign-in problem, no pointer to any project |
| 2026-09-17 | a session | the same, a second fresh account | six corrections, including the PATH defect |
| 2026-09-17, evening | a human | a plain Terminal, fresh account, no desktop app | the page became terminal only; the sign-in receipt was captured |
| 2026-09-18, morning | a session | a real terminal, fresh account | five corrections: the fork, the tool check, the fenced address, the occupied window, the version claim |
| 2026-09-18 | a human | a real terminal, fresh account | gave up before the end; this split, and the ten findings behind version five |

Every quotation below was observed on one of those runs. Anything not observed is named as
untested rather than described.

## The installer, quoted

The success block, printed 2026-09-17, on the machine the page was written from. The version is
that machine's, on that date; a reader today will see a higher number, which is expected:

```
✔ Claude Code successfully installed!

  Version: 2.1.274

  Location: ~/.local/bin/claude
```

The warning it prints twice, once above the success block and once below:

```
⚠ Setup notes:
  ● Native installation exists but ~/.local/bin is not in your PATH. Run:

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

The page no longer quotes either at length. A reader who has just watched the installer run does
not need to be shown what it printed, and the fourth version's reader followed the installer's
advice instead of the page's block precisely because the page quoted that warning so loudly.

## Why the page writes `~/.zshenv` and the installer says `~/.zshrc`

Checked directly, in a throwaway home directory with a stand-in tool on it, asking zsh the same
question four ways:

| Setup | A window you typed in | A command run for you |
|---|---|---|
| nothing | not found | not found |
| line in `~/.zshrc` | found | **not found** |
| line in `~/.zshenv` | found | found |

`~/.zshrc` is read only by an interactive shell. A command a helper runs for you is not one, so
the installer's own advice fixes half the cases. `~/.zshenv` is read by both.

## The `Next: Run claude --help` line, and whether it can be suppressed

It cannot, and here is why. `install.sh` does not print it. That script ends at "Installation
complete!"; the success block and the `Next:` line come from the downloaded binary's own install
step, which `install.sh` invokes as `claude install`. That step takes two options and neither is
quiet:

```
Options:
  --force     Force installation even if already installed
  -h, --help  Display help for command
```

Filtering the output would also hide the failures, which is a worse trade for a beginner than one
unhelpful suggestion. So the page spends one clause warning that the line is coming and that it
is not needed here.

## The sign-in, as observed

Recorded 2026-09-17 by a human on a fresh account, in a plain terminal. The first run asks which
colors suit the terminal, then how to sign in, offering three ways, then opens a browser page.
On return the terminal shows:

```
Logged in as you@example.com
Login successful. Press Enter to continue…
```

The address is the reader's own; it is shown here as a placeholder because this page is public.

**Still untested:** the exact keystroke that leaves the tool afterward. The page says `/exit`, with
closing the window as a fallback that always works. A cold human run will settle it.

## Timing

About 100 seconds of machine time, measured on 2026-09-17 on a version of the page with more steps
than this one: roughly 80 seconds for the first pass of checks and 16 for the install. It excludes
the sign-in and the writing step, because those are a person thinking rather than a machine
working. Nobody has timed the current page, and the half hour named for the writing step is its
design intent rather than a stopwatch reading.

## Defects this page has had, and what each taught

**A check that could not report its own failure.** `gh --version | head -1 || echo "…"` binds the
`||` to the whole pipeline, and `head` succeeds on empty input, so a missing tool printed a raw
shell error instead of the page's sentence. Both checks now use an `if`. The lesson: a check must
tell apart the states it is describing.

**A guard that sent a reader backward.** An earlier sign-in check decided "installed or not" from
whether the check succeeded, but the sign-in check reports failure when you are simply not signed
in, which is the normal answer at that point. It told a reader to reinstall a tool they already
had. The fifth version removes the check entirely: the page now just tells the reader to run the
tool, which asks for a sign-in if it needs one.

**A caveat that arrived after the machine spoke.** The joining-only step printed the GitHub tool's
own "To log in, run: gh auth login" to a reader who had nothing to log in to. The page's hedge was
correct and sat below the block, and terminal output arrives ahead of any prose that qualifies it.
That generalizes: a caveat printed after a machine speaks is a caveat nobody reads.

**An address inside a fence.** The page teaches that fenced blocks are for pasting. The template's
address sat in one, on the step that matters most, and pasting an address errors. Addresses now
sit in running prose.

**A step that left the window occupied.** The page said leaving the tool running was fine, which
leaves a full-screen program where the prompt was, and every later block needs that prompt.

**An admin gate that stopped the page dead.** The first version halted any account that could not
install software, while nothing on the page writes outside the account's own home, and the
receipts had been taken on a non-admin account.

**An invented number.** The opening once claimed the page took about an hour and a half. Nobody had
timed it. The number came out and the measurement above went in when there was one.

## A note for whoever edits the page next

**Name the tool's location rather than assuming the window found it.** The final check spells out
`$HOME/.local/bin/claude`. A command run for you in the background has not read the file that
teaches a window where the tool lives, and the short form failed in exactly that mode on a cold
run.

**Ask what changes what the reader does next.** That is the test the fifth version applied to every
sentence in the page. If a sentence explains why a choice was made, or records what was seen once,
it belongs in this file instead. This file has no length limit; the page does.

**The reader arriving with their own idea is the default.** Four earlier versions opened four
sections with "skip this if you are not joining someone else's project", which is most readers.
The page is now written for the person with their own idea, and everything a joining reader needs
extra sits in one marked section at the end.
