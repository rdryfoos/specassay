# FIRST-LIGHT

Welcome. This page takes you from a computer with nothing on it to a working setup, and then to
the thing all of it is for: writing down what you are actually promising, in your own words, so
that later you can watch those promises come back proven.

You do not need to be a programmer to follow it, and you do not need to be an administrator of
this computer: everything here installs into your own account. You do need enough of an unhurried
stretch to get through it without rushing the last step.

How long the whole thing takes, honestly: nobody knows yet. Nobody has run this page start to
finish and timed it, so there is no number here to give you. The one part that has a length is the
writing near the end, and that is half an hour by design rather than by measurement: it is meant
to be short enough to do today and long enough to be worth doing. When someone has run the whole
page through in one sitting, the time it took will be written here.

Two kinds of people arrive here, and both are expected. Some were sent by someone who already has
a project and wants them to join it. Some found this page on their own and have an idea of their
own. The setup is the same for both. Where the two part company, near the end, the page says so
and points each one onward.

## What this will ask of you

Five things, and none of them are hidden further down:

1. **A download and an install.** The desktop app, from a page you click.
2. **Two sign-ins.** One in the app, and a second one in the terminal. They are genuinely
   separate, which surprises most people, and it is explained where it happens.
3. **A stretch with a blank page**, writing what you are setting out to do, by hand and in your
   own words. Half an hour is the intent. This is the part that matters most, and it needs
   nothing installed.
4. **If you are joining someone's project: access to it**, which only they can give you.
5. **Your permission**, each time anything is installed or changed on your machine, at the moment
   it happens rather than all at once up front.

## What this will not do

It will not change anything on your machine without asking you first. It will not read another
person's files on this computer, even if you share it. It will not ask you to type a password into
anything but the official sign-in pages, and it will never ask you for one directly.

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
  or edit. Copy the whole block.
- **Something the session does.** If you are reading this inside a Claude session, it does the
  work and tells you what happened, asking before it changes anything. Where that is the case,
  the same command is also written out, so you can run it yourself if you prefer, or if you are
  reading this on your own.

Nothing is more than one step pretending to be one step. Where two things must happen together,
they are in the same block.

**Where this was tested.** Everything quoted here was observed on a Mac, on a brand new account,
on 2026-09-17. Where something was not tested, this page says so rather than guessing. On Windows
or Linux the shape is the same, but the exact messages are not ones anyone has checked.

**Which copy you are holding.** This page lives at a fixed address, and that address always shows
this exact version:

```
https://raw.githubusercontent.com/rdryfoos/specassay/first-light-v2/FIRST-LIGHT.md
```

If you are not sure the copy you hold is the newest, the current one is always at
https://github.com/rdryfoos/specassay/blob/main/FIRST-LIGHT.md, and starting over from there costs
nothing: no step here is harmed by being run twice.

## Step 0: Where you are

**Something the session does.** Before anything else, it reads your machine and tells you, in
plain words: which account you are signed in as, which operating system this is, and whether you
are reading this inside the desktop app or in a terminal window.

Nothing is changed or installed. This is only so you know where you are standing, and so the rest
of the page can tell you which parts apply to you.

If you are reading on your own, this is that same look, and it changes nothing:

```
whoami; sw_vers 2>/dev/null || uname -a; [ -n "$ANTHROPIC_BASE_URL" ] && echo "you appear to be reading this inside the desktop app" || echo "you appear to be in a terminal window"
```

That last line is a guess from one clue: the desktop app sets something in the environment that a
plain terminal does not. Step 1 explains why that matters. If it guesses wrong, nothing here
breaks.

**You do not need to be an administrator of this machine.** Everything this page installs goes
into your own account, and nothing it runs asks for a password. The one exception is the desktop
app in step 2, which may ask for an administrator password depending on where you choose to put
it, and that step says so.

## Step 1: A quirk of the desktop app, and why some checks look odd

**Something the session does, and it is mostly an explanation.**

If you are reading this inside the Claude desktop app, then commands run here inherit some
settings from the app itself. That matters in one specific way: a question like "am I signed in?"
can be answered by the app's own settings rather than by your actual terminal, and you would be
told everything is fine when it is not.

So when this page checks anything about signing in, it deliberately runs the check in a stripped
environment, one with the app's settings removed. You will see that in the blocks as `env -i`
followed by a short list. It looks strange, and that is why it is there: it asks your machine the
question, not the app.

This was tested. The app really does hand its own settings down, and a check run without that
precaution measures the app.

## Step 2: The desktop app

**A check first.** The session looks for the Claude desktop app on this machine and tells you
whether it is there.

If it is missing, here is the step:

**A link to click:**

```
https://claude.com/download
```

That page tells you what you are installing and offers the right version for your computer. Open
it, download, and install the app the way you install any other app. This is the one place on the
page that may ask for an administrator password, depending on where you put the app; if you do not
have one, you can keep the app in your own account's Applications folder, or ask whoever looks
after the machine. Then open the app and sign
in. That is the first of the two sign-ins.

**This one is yours to do.** Installing an application and signing into an account are things you
do, not things this page does for you.

When the app is open and signed in, come back here.

## Step 3: The command line tool, and the surprise that catches everyone

There are two different things called Claude: the app you just installed, and a command line tool
of the same name. **Installing the app does not install the tool**, and this catches almost
everyone.

Tested on a new account with the app installed and signed in, asking the machine where the tool
was gave exactly this:

```
claude not found
```

That is expected at this point. It is not a sign that anything went wrong.

**Something the session does.** It checks two separate things, because they fail differently:
whether the tool is installed at all, and whether your terminal can find it. A tool that is
installed but cannot be found is the most common outcome, and it has its own fix below.

If you are reading on your own:

```
command -v claude || echo "not on PATH"; ls -l "$HOME/.local/bin/claude" 2>/dev/null || echo "not installed at the usual place"
```

### If it is not installed

**A block to paste.** This downloads the installer, runs it, and makes sure your terminal can find
the tool afterward. All three are in one block on purpose, which is explained just below.

```
curl -fsSL https://claude.ai/install.sh -o "$TMPDIR/claude-install.sh" && bash "$TMPDIR/claude-install.sh" && echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshenv && export PATH="$HOME/.local/bin:$PATH" && claude --version
```

Three things worth knowing about that block:

**Why the last part is in the same block.** The installer finishes by printing this, word for
word:

```
  Next: Run claude --help to get started
```

On a new account that instruction does not work yet, because your terminal does not know where the
tool was put. The installer knows, and says so in its own warning, printed just above and below
its success message:

```
⚠ Setup notes:
  ● Native installation exists but ~/.local/bin is not in your PATH. Run:

    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

So the fix is part of the same block, and you are not left following an instruction that fails.

**Why the fix is not word for word what the installer suggests.** The installer says to add the
line to `~/.zshrc`. That file is read by terminal windows you open and type in, and not by
commands run for you in the background, which is how this page runs things when a session is
helping you. The block above puts the same line in `~/.zshenv` instead, which is read by both. If
you have already followed the installer's version, no harm done: running this block as well is
safe, and the only cost is the line appearing in two places.

**Why this is not the command on the website.** The download page publishes a shorter form that
pipes the installer straight into a shell. That form is not wrong, and you may have seen it. The
block above downloads the installer first and then runs it, which is the form that was actually
tested end to end for this page. You can see the file before it runs, and a page that hands you a
command should hand you the one that was tried.

When the installer succeeds it prints a block like this one, with the version and the location:

```
✔ Claude Code successfully installed!

  Version: 2.1.274

  Location: ~/.local/bin/claude
```

The block ends by asking the tool for its version, so you see it work in the same breath as
installing it.

**Not tested:** whether `claude --help` works in a window that was already open before you ran
that block. If it does not, close that window and open a new one.

### If it is installed but your terminal cannot find it

**A block to paste.** This is the second half of the block above, on its own:

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshenv && export PATH="$HOME/.local/bin:$PATH" && claude --version
```

## Step 4: Does it actually run

If step 3 did not finish, come back to this one afterward. A half-finished install answers these
checks with plumbing errors rather than the messages this page quotes, and then the page is
describing a different problem than the one on your screen.

**Something the session does.** It asks the tool for its version and shows you the answer, and
compares it with the version the installer reported.

On your own:

```
command -v claude >/dev/null 2>&1 && claude --version || echo "the tool is not on this shell's path yet: finish step 3, including the last part of its block"
```

If this prints a version, the tool is installed and reachable. If it prints anything else, stop
and keep what it printed; that message is what the person helping you will need.

## Step 5: The second sign-in

This is the part that surprises people, so here it is plainly: **signing into the app does not
sign you into the tool.** They keep separate sign-ins, and the tool cannot borrow the app's.

This was tested on a new account, with the app installed and signed in. Asking the tool about its
sign-in answered with a short report whose first two lines were these:

```
  "loggedIn": false,
  "authMethod": "none",
```

**Something the session does.** It asks the same question on your machine, with the app's settings
stripped out for the reason given in step 1, and tells you the answer.

On your own:

```
env -i HOME="$HOME" USER="$USER" PATH="$HOME/.local/bin:/usr/bin:/bin" sh -c 'command -v claude >/dev/null 2>&1 && claude auth status || echo "the tool is not installed yet: go back to step 3"'
```

If it says you are signed in, skip to step 6.

If it says you are not, **this one is yours to do**: start the tool by typing its name in a
terminal window and follow what it shows you.

```
claude
```

**What happens next, honestly.** The first time it runs, it asks you a few setup questions before
anything else, starting with how it should look in your terminal. Answer those, then complete the
sign-in it offers. This page does not describe what a finished sign-in looks like, because nobody
has run one through to the end while writing this down, and describing a screen nobody has seen is
how pages start lying to you.

When you are through it, come back and run the check above again. It should say you are signed in.

## Step 6: The tools for handling code

**Something the session does.** It checks that two programs are present and actually work:

- `git`, which is what copies the project onto your machine;
- `gh`, which is how you sign in to the place the project is kept.

On your own:

```
git --version || echo "git did not answer"; gh --version | head -1 || echo "gh did not answer"
```

It asks each one for its version rather than only asking whether a file exists, because on a Mac
there is a stand-in for `git` that is present before the real thing is installed. Asking it a
question is what tells the two apart. If a window appears offering to install developer tools,
that is the stand-in answering: accept it, let it finish, and run the block again.

On the machine where this page was tested, both were already present and both answered, so
neither installation was tried. If either is missing on yours, **ask the person who sent you** rather than following an
instruction from here. Installing developer tools differs by machine, and this page will not hand
you a command that nobody checked.

## Step 7: Signing in to where the code lives

**This step is only for people joining someone else's project.** If you came here with an idea of
your own, skip it, along with steps 9 and 10, and go to step 8, which is the one that matters
most. Step 9 says more about why, and nothing later needs this sign-in.

**Something the session does**, for the joining reader. It asks whether you are already signed in, with the app's settings
stripped out again.

On your own:

```
env -i HOME="$HOME" USER="$USER" PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin" gh auth status
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

## Step 8: Write down what you are actually promising

Everything up to here was plumbing. This step is the reason for it.

**Yours to do, and it needs nothing installed.** Before you get access to anything, before any
code is copied to your machine, sit down with a blank page and write your case: what you are
setting out to do and why. Half an hour is what this step is meant to take, which is a design
intent rather than a measurement: short enough to do today, long enough to be worth doing. By
hand, in your own words, in whatever you write in.

There is a template beside this page that walks you through it, and it is worth opening before you
start:

```
https://raw.githubusercontent.com/rdryfoos/specassay/first-light-v2/CASE-TEMPLATE.md
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
because those are minted later and attached to what you wrote. It is the thing
that makes everything afterward mean something: from here on, the work is built against what you
wrote, and the proofs that come back are proofs of these promises rather than of somebody's
generic idea of done. A setup without this is the wrong half of the gift.

If you are joining someone else's project, write it anyway, about your own part in it. You will
read their promises soon enough, and this is what tells you whether you agree with them.

## Step 9: Where the project is, and getting let in

This is where the two kinds of reader part company.

### If you were sent here to join a project

The project's location is not written on this page, and access to it is not something you can
grant yourself. Saying that plainly is better than letting you discover it after seven steps.

On the machine where this was tested, a new account had no way to find the project at all. There
was no copy of it, no address, and no pointer to one anywhere the account could read. That is the
gap this page exists to close, and this is the step where it closes.

**What to ask for**, from the person who sent you here:

1. the project's address;
2. read access to it, for the account you signed in with in step 7.

**Something the session does**, once you have both: it checks that your sign-in can actually reach
the project, and tells you plainly if it cannot. A refusal here almost always means the access has
not come through yet, not that you did anything wrong.

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

## Step 10: Your copy of the project

Skip this step if you came with your own idea; there is nothing yet to copy.

**Something the session does, with your permission.** It makes a copy of the project on your
machine, in a folder you choose, and tells you where it put it.

It will ask before it writes anything. If you would rather do it yourself, the session will give
you the exact command once you have the address from step 9, since the address is the part this
page cannot print.

## Step 11: Where you are now

**Something the session does.** It runs every check on this page once more, from the top, and tells
you the state of each one. Nothing is installed or changed in this pass. You end with a short list
of what is true on your machine.

When all of them pass, you have: the app, the command line tool, both sign-ins, the tools for
handling code, and your case written in your own words. If you were joining a project, you also
have access to it and a copy on your machine.

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

Everything quoted on this page was observed on 2026-09-17, on a Mac Mini, on a newly created
non-admin account with no previous use, from a session in the Claude desktop app. The page was
then run start to finish by a second fresh non-admin account, which is where the six corrections
in this version come from and where the timing below was measured. Anything not observed is marked
as untested where it appears, rather than being written as though it were
known.

Quoted above, verbatim: the installer's setup warning and its success block; the installer's
`Next: Run claude --help to get started` line; `claude not found` on an account with the desktop
app installed and signed in; the sign-in state showing `loggedIn false` on that same account; and
the GitHub tool's "You are not logged into any GitHub hosts" message.

Timing, measured on the first cold run of this page from end to end: about 100 seconds of machine
time in total. Roughly 80 of those are the first pass of checks, 16 are the install, and
everything after it is under a second. That number deliberately excludes the two parts with real
duration in them, the two sign-ins and the writing step, because those are a person thinking and
typing rather than a machine working. The half hour named for the writing step is still that
step's design intent rather than a stopwatch reading, and what a finished terminal sign-in prints
is still unrecorded.

The PATH fix in step 3 was checked directly, in a throwaway home directory with a stand-in tool
on it, asking zsh the same question four ways. With nothing set up, neither a background command
nor a typed window could find the tool. With the line in `~/.zshrc`, which is what the installer
suggests, a typed window found it and a background command still did not. With the line in
`~/.zshenv`, which is what this page does, both found it.

## A note for whoever edits this page next

The cold run turned up one thing worth keeping in front of anyone tempted to tidy this page.

The most elaborate commands here, the `env -i` blocks in the sign-in steps, are the most robust
ones. They name an explicit path, so they work whether or not the shell that runs them has been
set up. The simplest command, a bare `claude --version`, was the most fragile: it depended on a
shell having read a file that a background command never reads, and it failed in exactly the mode
this page is most often run in.

The elaboration was added for an unrelated reason, to stop the desktop app answering for the
machine, and it incidentally made those steps immune. That was luck rather than design. So: before
simplifying a command here, ask which shell will run it and what that shell has read. A command
that only works when a person types it into a window is not one this page can rely on.

Recorded as untested, and therefore not described here: what a completed terminal sign-in prints;
whether `claude --help` resolves in a terminal window opened before the PATH line was run; and any
way to install `git` or `gh`, neither of which was needed on the machine tested.

One more thing worth recording, because it affects anyone testing this page as much as anyone
reading it: the desktop app passes its own settings down to commands run inside it, including an
override of which service the tool talks to. Any check of sign-in state run inside the app without
stripping that first measures the app rather than the machine. That is why several checks above
look more elaborate than they need to.

The install form published on the download page pipes the installer directly into a shell. This
page hands over the downloaded-then-run form instead, because that is the form that was tested.
