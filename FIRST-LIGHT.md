# FIRST-LIGHT

Welcome. This page takes you from a computer with nothing on it to a working setup, ready for the
rest of the instructions. It is the only page you need to start, and you were handed it because
everything else assumes things you do not have yet.

You do not need to be a programmer to follow it. You do need about an hour, an account you can
install software on, and one person who can give you access to the project's code. That person is
whoever sent you here.

## What this will ask of you

Four things, and none of them are hidden further down:

1. **A download and an install.** The desktop app, from a page you click.
2. **Two sign-ins.** One in the app, and a second one in the terminal. They are genuinely
   separate, which surprises most people, and it is explained where it happens.
3. **Access to the project's code**, which only the person who sent you here can give you.
4. **Your permission**, each time anything is installed or changed on your machine, at the moment
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

## Step 0: Where you are

**Something the session does.** Before anything else, it reads your machine and tells you, in
plain words: which account you are signed in as, whether that account can install software, which
operating system this is, and whether you are reading this inside the desktop app or in a terminal
window.

Nothing is changed or installed. This is only so you know where you are standing, and so the rest
of the page can tell you which parts apply to you.

If you are reading on your own, this is that same look, and it changes nothing:

```
whoami; sw_vers 2>/dev/null || uname -a; id -Gn | tr ' ' '\n' | grep -qx admin && echo "this account can install software" || echo "this account cannot install software"
```

If your account cannot install software, stop here and ask the person who sent you. The rest of
this page needs it.

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
it, download, and install the app the way you install any other app. Then open the app and sign
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
curl -fsSL https://claude.ai/install.sh -o "$TMPDIR/claude-install.sh" && bash "$TMPDIR/claude-install.sh" && echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

Two things worth knowing about that block:

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

**Not tested:** whether `claude --help` works in a window that was already open before you ran
that block. If it does not, close that window and open a new one.

### If it is installed but your terminal cannot find it

**A block to paste.** This is the second half of the block above, on its own:

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

## Step 4: Does it actually run

**Something the session does.** It asks the tool for its version and shows you the answer, and
compares it with the version the installer reported.

On your own:

```
claude --version
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
env -i HOME="$HOME" USER="$USER" PATH="$HOME/.local/bin:/usr/bin:/bin" claude auth status
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

**Something the session does.** It checks for two programs and tells you which are present:

- `git`, which is what actually copies the project onto your machine;
- `gh`, which is how you sign in to the place the project is kept.

On your own:

```
command -v git || echo "git missing"; command -v gh || echo "gh missing"
```

On the machine where this page was tested, both were already present, so neither installation was
tried. If either is missing on yours, **ask the person who sent you** rather than following an
instruction from here. Installing developer tools differs by machine, and this page will not hand
you a command that nobody checked.

## Step 7: Signing in to where the code lives

**Something the session does.** It asks whether you are already signed in, with the app's settings
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

## Step 8: Where the project is, and getting let in

This is the one thing neither this page nor you can supply, and it is worth saying clearly rather
than letting you discover it: **the project's location is not written on this page, and access to
it is not something you can grant yourself.**

On the machine where this was tested, a new account had no way to find the project at all. There
was no copy of it, no address, and no pointer to one anywhere the account could read. That is the
gap this page exists to close, and this is the step where it closes.

**What to ask for**, from the person who sent you here:

1. the project's address;
2. read access to it, for the account you signed in with in step 7.

**Something the session does**, once you have both: it checks that your sign-in can actually reach
the project, and tells you plainly if it cannot. A refusal here almost always means the access has
not come through yet, not that you did anything wrong.

## Step 9: Your copy of the project

**Something the session does, with your permission.** It makes a copy of the project on your
machine, in a folder you choose, and tells you where it put it.

It will ask before it writes anything. If you would rather do it yourself, the session will give
you the exact command once you have the address from step 8, since the address is the part this
page cannot print.

## Step 10: Where you are now

**Something the session does.** It runs every check on this page once more, from the top, and tells
you the state of each one. Nothing is installed or changed in this pass. You end with a short list
of what is true on your machine.

When all of them pass, you have: the app, the command line tool, both sign-ins, the tools for
handling code, access to the project, and a copy of it on your machine.

That is the whole purpose of this page, and it is where the project's own instructions begin.
Their first section starts by checking the same things this page just finished, which is
deliberate: you should be able to start there and be told, in its words, that you are ready.

## If something here did not work

Keep what your screen printed, exactly, and take it to the person who sent you. A message you
copied is worth more than a description of it, and none of this is your fault to sort out alone.

---

## Receipts

Everything quoted on this page was observed on 2026-09-17, on a Mac Mini, on a newly created
non-admin account with no previous use, from a session in the Claude desktop app. Anything not
observed is marked as untested where it appears, rather than being written as though it were
known.

Quoted above, verbatim: the installer's setup warning and its success block; the installer's
`Next: Run claude --help to get started` line; `claude not found` on an account with the desktop
app installed and signed in; the sign-in state showing `loggedIn false` on that same account; and
the GitHub tool's "You are not logged into any GitHub hosts" message.

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
