# FIRST-LIGHT

Welcome. This page takes you from a computer with nothing on it to a working setup, and then to
the thing all of it is for: writing down what you are actually promising, in your own words, so
that later you can watch those promises come back proven.

You do not need to be a programmer to follow it, and you do not need to be an administrator of
this computer: everything here installs into your own account. You do need enough of an unhurried
stretch to get through it without rushing the last step.

Two kinds of people arrive here, and both are expected. Some were sent by someone who already has
a project and wants them to join it. Some found this page on their own and have an idea of their
own. The setup is the same for both. Where the two part company, near the end, the page says so
and points each one onward.

## Reading this page

The window everything here happens in is called **Terminal**. On a Mac, hold down Command and
press the space bar, type `terminal`, and press Return. A window opens with some text and a
blinking cursor.

**A block to paste**, and the only one that has to come before the others. It puts this page in
front of you, in that window:

```
curl -fsSL https://raw.githubusercontent.com/rdryfoos/specassay/first-light-v3/FIRST-LIGHT.md | less
```

The page appears. Press the space bar to move down a screen at a time, and press `q` when you want
to leave it. Nothing is installed and nothing is changed by reading it this way.

If you would rather read in a browser, the same page is at
https://github.com/rdryfoos/specassay/blob/main/FIRST-LIGHT.md. Either way is fine; the command
above is here because it needs nothing but the window you just opened.

## Two windows

Open a second Terminal window the same way, with Command and the space bar.

**Window one is where you read this page.** **Window two is where you paste the blocks.** Keeping
them apart means you never have to leave the instructions to run something, then find your place
again. The reader who tried this page without the second window ended up quitting the page,
scrolling back, and retyping from memory, which is friction you can avoid by opening one more
window now.

## If you already have the Claude desktop app

You may already have the Claude app on this machine, or you may have met Claude that way. That is
fine, and it is not what this page uses. **You do not need the desktop app for anything here, and
nothing on this page opens it.** Everything happens in the terminal window you just opened. If you
have the app, leave it alone; if you do not, there is nothing to install.

## What this will ask of you

Four things, and none of them are hidden further down:

1. **One installation**, which is a block you paste and which installs into your own account.
2. **One sign-in**, in the terminal, which opens a browser page for you to approve.
3. **A stretch with a blank page**, writing what you are setting out to do, by hand and in your
   own words. Half an hour is the intent. This is the part that matters most, and it needs
   nothing installed.
4. **If you are joining someone's project: access to it**, which only they can give you.

Plus your permission, each time anything is installed or changed on your machine, at the moment it
happens rather than all at once up front.

## What this will not do

It will not change anything on your machine without asking you first. It will not read another
person's files on this computer, even if you share it. It will not ask you to type a password into
anything but the official sign-in page in your browser, and it will never ask you for one
directly.

## How to read it

You can read this whole page first, before running anything at all. Nothing here happens just
because you read it, and reading it end to end is the best way to know what you are agreeing to.

The page is a sequence of checks. Each one looks at your machine, tells you what it found, and
only then offers a fix if a fix is needed. If you already have some of this, those parts are
skipped. If you stop halfway and come back tomorrow, start at the top again: the checks will pass
over everything already done.

Every step is one of three kinds, and each says which it is:

- **A link to click.** The address is written out, so you can see where it goes before you go.
- **A block to paste.** It works from any folder, and there is nothing in it for you to fill in
  or edit. Copy the whole block, paste it into window two, and press Return.
- **Something a helper does.** If a Claude session is helping you through this page, it does the
  work and tells you what happened, asking before it changes anything. Where that is the case, the
  same block is written out too, so you can paste it yourself instead.

Nothing is more than one step pretending to be one step. Where two things must happen together,
they are in the same block.

**Where this was tested.** Everything quoted here was observed on a Mac, on brand new accounts, on
2026-09-17, in a plain terminal window. Where something was not tested, this page says so rather
than guessing. On Windows or Linux the shape is the same, but the exact messages are not ones
anyone has checked.

**Which copy you are holding.** This page lives at a fixed address, the one the command at the top
of the page uses, and that address always shows this exact version:

```
https://raw.githubusercontent.com/rdryfoos/specassay/first-light-v3/FIRST-LIGHT.md
```

If you are not sure the copy you hold is the newest, the current one is always at
https://github.com/rdryfoos/specassay/blob/main/FIRST-LIGHT.md, and starting over from there costs
nothing: no step here is harmed by being run twice.

## Step 0: Where you are

**A block to paste.** This asks your machine who you are signed in as and which version of macOS
this is. It changes nothing.

```
whoami; sw_vers 2>/dev/null || uname -a
```

You should see a short name, which is your account, and a version. That is all this step is for:
knowing where you are standing before anything happens.

## Step 1: The tool this page installs

The thing you are installing is called Claude Code. It is a program you run by typing its name in
the terminal window. It is not the desktop app, and having the app does not give you this.

**A block to paste.** This checks whether you already have it. It changes nothing.

```
command -v claude || echo "not installed yet, which is expected"
```

If that printed a path, you already have it: skip to step 2.

If it said "not installed yet", here is the install.

**A block to paste.** It downloads the installer, runs it, tells your machine where to find the
tool afterward, and then asks the tool for its version so you see it working:

```
curl -fsSL https://claude.ai/install.sh -o "$TMPDIR/claude-install.sh" && bash "$TMPDIR/claude-install.sh" && echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshenv && export PATH="$HOME/.local/bin:$PATH" && claude --version
```

It takes under a minute. Three things about it are worth knowing, and all three are things the
installer itself will show you.

**The installer says to add a line to a file called `~/.zshrc`. This page adds it to `~/.zshenv`
instead.** The reason is small and it matters: `~/.zshrc` is read only by a window you typed in
yourself, while `~/.zshenv` is read both by that window and by commands run for you in the
background. Using the file the installer names would work while you type and fail when a helper
runs something for you. If you have already followed the installer's version, no harm done:
running this block as well is safe.

**The installer prints a warning about that same file, twice**, once above its success message and
once below. It looks like this, and it is why the line above is part of this block rather than a
separate step:

```
⚠ Setup notes:
  ● Native installation exists but ~/.local/bin is not in your PATH. Run:

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

**The installer ends by suggesting `claude --help`.** You do not need it. It prints several
hundred lines listing every option the tool has, which is useful once you know the tool and
overwhelming before that. Nothing on this page asks you to run it.

When the installer succeeds it prints a block like this one, with the version and the location:

```
✔ Claude Code successfully installed!

  Version: 2.1.274

  Location: ~/.local/bin/claude
```

**Not tested:** whether the tool works in a terminal window that was already open before you ran
that block. If a window says it cannot find `claude`, close it and open a new one.

## Step 2: Does it actually run

**A block to paste.** It asks the tool for its version:

```
"$HOME/.local/bin/claude" --version
```

It names the exact place the tool was installed rather than relying on your window having noticed
it yet, so it answers the same whether you paste it or a helper runs it for you.

If this prints a version, you are installed. If it prints anything else, stop and keep what it
printed: that message is what the person helping you will need.

## Step 3: Signing in

This is the one sign-in on this page. It happens in the terminal, and it opens a browser page for
you to approve.

**A block to paste.** First, are you already signed in:

```
if [ -x "$HOME/.local/bin/claude" ]; then "$HOME/.local/bin/claude" auth status; else echo "The tool is not installed: go back to step 1."; fi
```

You will see a short report. The line that matters is the first one:

- `"loggedIn": true` means you are signed in already. Skip to step 4.
- `"loggedIn": false` means the tool is installed and not yet signed in, which is the normal
  answer at this point. Carry on below.

**This one is yours to do.** Type the tool's name and press Return:

```
claude
```

The first time it runs it asks two questions before anything else. First it asks which colors suit
your terminal; any answer is fine, and it can be changed later. Then it asks how you want to sign
in, and offers three ways. Choose the one that matches the account you have.

It then opens a page in your browser. Approve it there, and come back to the terminal window,
where you will see something like this:

```
Logged in as you@example.com
Login successful. Press Enter to continue…
```

The address shown will be your own. Press Return, and you are signed in. You can leave the tool
running or close that window; either is fine.

Run the check at the top of this step again if you want to see it say `"loggedIn": true`.

## Step 4: Two more tools, if your project needs them

These two matter only if you are joining a project that already exists. If you came here with your
own idea, skip to step 6; nothing you do needs them.

- `git` is what copies a project onto your machine.
- `gh` is how you sign in to the place the project is kept.

**A block to paste.** It asks each one for its version rather than only asking whether it exists,
because on a Mac there is a stand-in for `git` that is present before the real thing is installed,
and asking it a question is what tells the two apart:

```
git --version || echo "git did not answer"; gh --version | head -1 || echo "gh did not answer"
```

If a window appears offering to install developer tools, that is the stand-in answering: accept
it, let it finish, and paste the block again.

On the machines where this page was tested, both were already present and both answered, so
neither installation was tried here. If either is missing on yours, **ask the person who sent
you** rather than following an instruction from this page. Installing developer tools differs by
machine, and this page will not hand you a command that nobody has run.

## Step 5: Signing in to where the code lives

**This step is only for people joining someone else's project.** If you came here with an idea of
your own, skip it, along with steps 7 and 8, and go to step 6, which is the one that matters most.

**A block to paste.** Are you already signed in:

```
gh auth status
```

On a new account this answers:

```
You are not logged into any GitHub hosts. To log in, run: gh auth login
```

If that is your answer, **this one is yours to do**:

```
gh auth login
```

It asks a short series of questions and then opens a browser page for you to approve. Follow it to
the end, then come back.

## Step 6: Write down what you are actually promising

Everything up to here was plumbing. This step is the reason for it.

**Yours to do, and it needs nothing installed.** Before you get access to anything, before any
code is copied to your machine, sit down with a blank page and write your case: what you are
setting out to do and why. Half an hour is what this step is meant to take, which is a design
intent rather than a measurement: short enough to do today, long enough to be worth doing. By
hand, in your own words, in whatever you write in.

There is a template beside this page that walks you through it, and it is worth opening before you
start:

```
https://raw.githubusercontent.com/rdryfoos/specassay/first-light-v3/CASE-TEMPLATE.md
```

It has eight sections. The five below are its heart; the other three ask what the smallest first
piece would be, what you are deliberately leaving out for now, and what you are still unsure
about. You do not need it: the questions below are the same ones, and a blank page works.

Five questions, and honest short answers beat polished long ones:

1. **What is the problem?** The thing that is wrong or missing now, described as it actually
   shows up, not as a feature you already want to build.
2. **Who has it?** Real people you could name or describe, not "users". If you are one of them,
   say so.
3. **What are you promising?** What will be true for those people that is not true today, and the
   one thing this will deliberately refuse to do.
4. **How would you know it is working?** A handful of things you could look at and see plainly,
   even a rough one. If you cannot name any, that is worth knowing now.
5. **What are you assuming?** The things you believe that, if wrong, make the rest pointless.
   Which one would hurt most to be wrong about, and how cheaply could you find out?

Nobody needs to see this. It is not a document to submit, and nothing checks it. The template says
the same, and tells you what to leave out: no technology choices, no screens, and no identifiers,
because those are minted later and attached to what you wrote. It is the thing that makes
everything afterward mean something: from here on, the work is built against what you wrote, and
the proofs that come back are proofs of these promises rather than of somebody's generic idea of
done. A setup without this is the wrong half of the gift.

If you are joining someone else's project, write it anyway, about your own part in it. You will
read their promises soon enough, and this is what tells you whether you agree with them.

## Step 7: Where the project is, and getting let in

This is where the two kinds of reader part company.

### If you were sent here to join a project

The project's location is not written on this page, and access to it is not something you can
grant yourself. Saying that plainly is better than letting you discover it after six steps.

On the machine where this was tested, a new account had no way to find the project at all. There
was no copy of it, no address, and no pointer to one anywhere the account could read. That is the
gap this page exists to close, and this is the step where it closes.

**What to ask for**, from the person who sent you here:

1. the project's address;
2. read access to it, for the account you signed in with in step 5.

**Something a helper does**, once you have both: it checks that your sign-in can reach the
project, and tells you plainly if it cannot. A refusal here almost always means the access has not
come through yet, not that you did anything wrong.

### If you came on your own, with your own idea

There is nothing for you to ask for and nobody to wait on. You have a working machine and you have
your case, which is more than most projects start with.

What comes next for you is the part that turns a case into a working project of its own, with the
promises you just wrote at the center of it. That is being written now, and this page will point
to it when it exists. No date is promised here, because a date nobody can keep is worse than an
honest gap.

In the meantime, your case is yours and it keeps. Nothing you did today goes to waste: the machine
is set up, and the time you spent on those five questions is the part that would have been hardest
to go back and do later.

## Step 8: Your copy of the project

Skip this step if you came with your own idea; there is nothing yet to copy.

**Something a helper does, with your permission.** It makes a copy of the project on your machine,
in a folder you choose, and tells you where it put it.

It will ask before it writes anything. If you would rather do it yourself, you will be given the
exact block once you have the address from step 7, since the address is the part this page cannot
print.

## Step 9: Where you are now

**A block to paste.** This runs the checks from this page once more and prints what is true.
Nothing is installed or changed:

```
"$HOME/.local/bin/claude" --version; "$HOME/.local/bin/claude" auth status; git --version 2>/dev/null; gh auth status 2>&1 | head -2
```

When those answer, you have: the tool, your sign-in, and, if you are joining a project, the two
code tools and access to it. Along with your case, written in your own words, which is the part
none of the rest was any use without.

For someone joining a project, this is where that project's own instructions begin. Their first
section starts by checking the same things this page just finished, which is deliberate: you
should be able to start there and be told, in its words, that you are ready.

For someone who came with their own idea, this is where you stop for now, with the machine ready
and the promises written. What follows is being written, and it will be linked from this page.

## If something here did not work

Keep what your screen printed, exactly, and take it to the person who sent you. A message you
copied is worth more than a description of it, and none of this is your fault to sort out alone.

---

## Receipts

Everything quoted on this page was observed on 2026-09-17, on a Mac Mini, on newly created
non-admin accounts with no previous use. The first two runs went through the Claude desktop app's
own terminal; the third, which this version is written from, went through a plain Terminal window
on an account with no desktop app on it at all. Anything not observed is marked as untested where
it appears, rather than being written as though it were known.

Quoted above, verbatim: the installer's setup warning and its success block; `You are not logged
into any GitHub hosts`; the sign-in state lines `"loggedIn": true` and `"loggedIn": false`; and
the two lines the tool prints when a sign-in finishes, with the account's address replaced by a
placeholder because this page is public.

The sign-in sequence is recorded as it happened: a question about colors, then a choice of three
ways to sign in, then a browser page to approve, then those two lines in the terminal.

Timing, measured on an earlier run of this page, before it was simplified to the terminal alone:
about 100 seconds of machine time in total, of which roughly 80 were the first pass of checks and
16 the install. That number excludes the sign-in and the writing step, because those are a person
thinking rather than a machine working. This version has fewer steps than the one that was timed,
so it should be faster; nobody has put a stopwatch on it yet, and the half hour named for the
writing step is still a design intent rather than a measurement.

The install's path fix was checked directly, in a throwaway home directory with a stand-in tool on
it, asking the same question four ways. With nothing set up, neither a typed window nor a
background command could find the tool. With the line in `~/.zshrc`, which is what the installer
suggests, a typed window found it and a background command still did not. With the line in
`~/.zshenv`, which is what this page does, both found it.

## A note for whoever edits this page next

Two things are worth keeping in front of anyone tempted to tidy this page.

**Name the tool's location rather than assuming the window found it.** The blocks in steps 2, 3
and 9 spell out `$HOME/.local/bin/claude` instead of the shorter `claude`. That is not fussiness.
A command run for you in the background has not read the file that teaches a window where the tool
lives, and the short form failed in exactly that mode during an earlier cold run. Before
simplifying a command here, ask which window will run it and what that window has read.

**A check must tell apart the states it is describing.** An earlier version of the sign-in step
decided "installed or not" from whether the check succeeded, but the sign-in check reports failure
when you are simply not signed in yet, which is the normal answer at that point. It sent a reader
backward to reinstall a tool they already had. A guard that cannot tell "missing" from "present
and not yet signed in" will send someone in a circle.
