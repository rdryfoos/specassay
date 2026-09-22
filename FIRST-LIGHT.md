# FIRST-LIGHT

By the end of this page you will have Claude Code installed on this machine, signed in, and your
own case written down: what you are setting out to do, in your own words. That last part is the
point of the rest.

You do not need to be a programmer, and you do not need to be an administrator of this computer.

Why this page says what it says, and everything that was tested to write it, is in
[FIRST-LIGHT-NOTES.md](https://raw.githubusercontent.com/rdryfoos/specassay/main/FIRST-LIGHT-NOTES.md).
You do not need it to follow along.

## You are already here

This page is the instructions. A terminal beside it is where the blocks below get pasted.
Nothing to install yet. Read on.

While you are reading: the space bar moves a page, and the down arrow moves a single line.

**Open a terminal window now.** With Terminal in front of you, hold Command and press N. That way
you never have to leave the instructions to run something and then find your place again.

These are Mac instructions. Nobody has run this page on Linux or Windows, so the steps may be
right there and the keystrokes are not.

## The desktop app

**You will not use the desktop app here.** If you have it, leave it alone; if you do not, there is
nothing to install. Everything on this page is pasted into the terminal window beside it.

## What this page asks of you

Three steps and one browser trip:

1. **Install the tool.** One block to paste.
2. **Sign in.** You type one word, approve it in a browser, and come back.
3. **Write your case.** Half an hour with a blank page, and nothing installed.

Each block is safe to run twice. If you stop and come back tomorrow, start at the top.

## Step 1: Install

**A block to paste.** It downloads the installer, runs it, tells your machine where the tool went,
and asks the tool its version so you see it worked:

```
curl -fsSL https://claude.ai/install.sh -o "$TMPDIR/claude-install.sh" && bash "$TMPDIR/claude-install.sh" && echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshenv && export PATH="$HOME/.local/bin:$PATH" && claude --version
```

It takes about a minute, and it prints a good deal on the way. Two things it says are worth
knowing in advance:

- **It will tell you to add a line to `~/.zshrc`.** The block above adds the same line to
  `~/.zshenv` instead, which works both when you type commands and when something runs them for
  you. You do not need to follow the installer's version as well, and no harm is done if you did.
- **It ends by suggesting `claude --help`.** You do not need it here; it prints several hundred
  lines of options.

When the block finishes it prints a version number. That is step 1 done.

## Step 2: Sign in

**Yours to do.** Type this and press Return:

```
claude
```

The first time it runs, it asks which colors suit your terminal, then how you want to sign in,
offering three ways. Choose the one that matches the account you have. It opens a page in your
browser; approve it there and come back to the terminal, where you will see two lines: that you
are logged in as your own address, and that the login succeeded. Press Return.

**Then get your prompt back.** The tool keeps the window once you are in it. Type `/exit` and
press Return to leave. If that does not work, close the window and open another with Command and
N.

This is the only place on this page where a browser opens.

## Step 3: Write your case

This is what the setup was for.

**Yours to do, and it needs nothing installed.** Sit down with a blank page, away from the
machine if you like, and write what you are setting out to do. Half an hour is the intent: short
enough to do today, long enough to be worth doing. Five questions:

1. **What is the problem?** The thing that is wrong or missing now, as it actually shows up.
2. **Who has it?** Real people you could name or describe. If it is just you, say so.
3. **What are you promising?** What will be true for them that is not true today, and the one
   thing this will deliberately refuse to do.
4. **How would you know it is working?** Things you could look at and see plainly.
5. **What are you assuming?** What has to be true for any of it to matter, and which one would
   hurt most to be wrong about.

There is a template that walks you through the same questions with three more:
https://raw.githubusercontent.com/rdryfoos/specassay/main/CASE-TEMPLATE.md. It is a page
to read, not a block to paste.

Nobody needs to see what you write. Nothing checks it. It is what everything afterward gets built
against, so that the work can be held to your promises rather than to somebody's generic idea of
done.

## Where you are now

**A block to paste**, which prints what is true and changes nothing:

```
"$HOME/.local/bin/claude" --version; "$HOME/.local/bin/claude" auth status
```

You have the tool, your sign-in, and your case. That is the whole of this page.

**What comes next** is turning your case into a working project, with your promises at the center
of it and a thread from each promise to the code and tests that answer for it. That part is being
built now and is not automated yet, so it is not on this page. When it exists, this page will
point at it.

If you want to see the machinery itself before then, there is a tutorial at
https://specassay.com/start. It builds a small sample project and takes it through the whole
cycle; it does not touch the case you just wrote. It is twelve blocks where this page is three
steps, so it is a longer and denser sit than this one, and it is optional.

## If something did not work

Keep exactly what your screen printed and take it to whoever sent you here. A message you copied
is worth more than a description of it.

---

## If you are joining someone else's project

Everything above applies to you too. This section is the extra part, and only this section.

You need two things this page cannot give you: **where the project is**, and **permission to read
it**. Ask the person who sent you for both. On the machine this page was tested on, a new account
had no way to find a project on its own, which is why this asks rather than guesses.

**A block to paste.** It checks the two programs that copy a project onto your machine and sign
you in to where it is kept:

```
if git --version >/dev/null 2>&1; then git --version; else echo "git did not answer"; fi; if gh --version >/dev/null 2>&1; then gh --version | head -1; else echo "gh did not answer"; fi
```

If either says it did not answer, ask the person who sent you rather than following an
instruction from here: installing those differs by machine, and nobody has tested a command for
it. If a window appears offering to install developer tools, accept it, let it finish, and paste
the block again.

**Yours to do.** Sign in to where the code is kept:

```
gh auth login
```

It asks a few questions, then opens a browser page to approve.

Once you have the project's address and your access has come through, a copy of the project can be
made on your machine, in a folder you choose. If a Claude session is helping you, it will do that
and tell you where it put it; on your own, the person who sent you can give you the one line that
does it, since the address is the part this page cannot print.

After that, that project's own instructions take over, and they begin by checking the same things
this page just finished.
