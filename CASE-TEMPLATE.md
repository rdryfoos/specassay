# CASE

**What is this file?** It is the thing you write before any code exists.
It says what you want, who it is for, and how you will know it worked.
Everything the machine builds later gets tied back to what you write
here.

**How to use it.** Fill it in by hand, in your own words, in one
sitting. Do not look things up. Do not make it good. A rough honest
version beats a polished vague one, and you will rewrite it anyway
once you see the first working piece.

**How long?** Half an hour. If a section stumps you, write "not sure
yet" and move on. Not sure yet is a real answer and a useful one.

---

## 1. The problem

What is annoying, slow, or lost today? Write it as a story about a
real moment, not as a feature request.

Two or three sentences.

-

## 2. Who has this problem

Who is this for? If it is just you, say so. That is a fine answer and
it makes everything downstream easier.

-

## 3. What you are promising

If this thing existed and worked, what would it do for that person?
Write three to five promises. Each one should be something you could
later point at and say yes or no about.

Write them as plain sentences, not features. "I can tell at a glance
which plants need watering this week" is a promise. "Reminder screen"
is a feature.

1.
2.
3.
4.
5.

## 4. How you would know it is working

For each promise above, what would you see, do, or count that tells
you it is true? If you cannot think of anything, say so. A promise
nobody can check is worth knowing about now rather than later.

1.
2.
3.
4.
5.

## 5. What you are assuming

List what has to be true for this to be worth building. Put the one
that scares you most at the top. The scary one is usually where to
start.

-
-
-

## 6. The smallest first piece

What is the smallest version that would teach you whether the scary
assumption holds? Not the smallest product. The smallest thing that
settles the question.

-

## 7. Not now

What are you deliberately leaving out of the first pass? Writing this
down keeps it from creeping back in on a Tuesday.

-
-
-

## 8. Open questions

Anything you are unsure about, including questions about the tools
themselves. These are notes to yourself and to whoever helps you.

-
-
-

---

## Things to leave out of this file

- **Technology choices.** No frameworks, no databases, no model
  names. Those decisions come later and they come easier once the
  promises are clear.
- **Screens and layouts.** Describe what someone can do, not where
  the button goes.
- **ID numbers.** You do not write those. The machine mints them
  later and attaches them to your promises. That is the whole point:
  you write in plain language, and the thread gets added around it.
- **Anything you would be embarrassed to be held to.** If you would
  not want to be asked "did you do this?" in six weeks, do not
  promise it here.

## What happens next

Nothing, until you decide to build it. The file is worth having on its
own: it is the clearest half hour you will spend on an idea, and the
promises in it are yours whether or not any machine ever reads them.

When you do build, this file is what the work is tied to. An agent
reads your promises, gives each one a durable identifier, and from
then on every piece of code and every test it writes points back to
the promise it serves. When you look at the work later, you can ask
any line of it why it exists and get your own words back.

If you are joining a project someone else runs, hand this file to
whoever sent you. If the idea is your own, keep it. The path from a
case to a project of your own is being written, and the page that
brought you here will point at it when it exists.
