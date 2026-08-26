# Runbook — the context gauge (knowing when to stop)

*Memento — Gumdrop v1.0.0, for VS Code + GitHub Copilot.*

## The problem, honestly

An AI assistant has a finite amount of room in a session, and it runs out mid-task if nobody is
counting. The failure is not dramatic. It is a slow decline: answers get shorter, earlier
decisions get forgotten, the same file gets re-read, small mistakes appear in work that was
careful an hour ago. By the time it is obvious, the session no longer has enough room left to
write a decent handoff — so the next one starts from a bad note, and pays twice.

The gauge is the discipline that stops this. It has one job.

---

## ⛔ THE GAUGE IS A THROTTLE, NOT A THERMOMETER

This is the whole idea, and it is the part most people get wrong.

A thermometer tells you how hot it is. A throttle **changes what you do**. A gauge that only
reports a number, and never causes a piece of work to be cut, deferred or handed on, has done
nothing — it has just added a number to the conversation.

So every reading has to be attached to a decision:

- **Price the job before committing to it.** Before a big piece of work, say roughly what it
  will cost: getting oriented, doing the work, and writing the record at the end. If the room
  left will not cover all three, the job is too big for this session — say so *now*, and split
  it, rather than discovering it two thirds of the way through.
- **The wrap is part of the price, not an extra.** The stop line is not "when you are full". It
  is **full, minus what the wrap will cost**. An expensive wrap must stop the session *earlier*.
  This is the single most common miscalculation, and it is why sessions end badly: the stop line
  was treated as the place the wrap *finishes* rather than where it *starts*.
- **Cut work, out loud.** When room is short the honest move is to name what is being dropped
  and why, not to quietly do a thinner version of everything.

---

## ⚠ What cannot be measured here, and what to do instead

**Copilot in VS Code does not expose a token count to itself.** There is no reading to take. The
machinery Apollo uses to measure its own sessions in real tokens is not in this pack, because it
depends on an API key and a session log file that do not exist in this environment. Shipping it
would ship an instrument that returns a confident wrong number, which is worse than none.

So this is a **declared gap**, and the substitute is an **estimate tier**, named as such:

| tier | what it is | say it like this |
|---|---|---|
| **measured** | a real count from an instrument | *not available in this environment* |
| **estimated** | your own running sense of the session's size | "we are maybe two thirds through the room I'd want for this" |
| **unknown** | you genuinely do not know | "I have lost track of how long this session is" — which is itself a reason to wrap |

⛔ **Never report an estimate as a measurement.** Do not invent a percentage. Do not say "we're at
60%" when nothing counted anything — a number with no instrument behind it gets believed, quoted,
and acted on, and it is the confident false inscription in its purest form.

**A declared gap passes; a silent one fails.** Saying "I cannot measure this, here is my estimate
and what I am basing it on" is a complete and honest answer. Saying nothing while the session
quietly fills up is the failure.

---

## The three postures

Without a number, judge the posture from what is actually observable: how long the session has
run, how many files have been opened, how much has been built, and — the most reliable signal —
whether you are still holding the thread of it.

### 🟢 Early — work freely

Full quality, no economising. **Do not pad, do not hedge, do not shorten work to save room you
have not run out of.** The postures change behaviour at their thresholds and not before; a
session spent being frugal from the first minute wastes the room it was protecting.

### 🟡 Middle — get economical, and say so

Signals: the session has covered real ground; you have opened a lot of files; you are starting to
re-read things you have already read.

- **Surface it, unprompted.** Tell the person where you think the session is and offer to start
  wrapping soon. Do not wait to be asked. Silence while the session fills is the failure mode.
- **Flush the spine now.** Write current state into `memento-package/_LIVE-STATE.md` *without*
  ending the session. If things go wrong from here, that file is what survives.
- **⛔ Do not start a new build artefact.** Not a new prototype, not a new review page, not a new
  component from scratch. These are deceptively heavy and they are exactly where late-session
  mistakes land. Writing, deciding and inscribing are all fine when the session is long. Starting
  a fresh interactive build is not — hand that to a new session.

### 🔴 Late — you are already over

⛔ **Reaching here is the overrun, not the cue.** The wrap should have started at the stop line —
*room left, minus the price of the wrap.* If you are here and have not begun, you are spending
the reserve. Wrap immediately, run
`_RUNBOOK-capture-ritual.md` in this folder, and say in `_LIVE-STATE.md` that the session ran
over. That sentence costs nothing and saves the next session from trusting a rushed handoff.

---

## Starting a fresh session is cheap

This is the clause that makes the throttle easy to obey: **ending a session is not a defeat.** A
clean handoff plus a fresh session is faster and better than a long one running on fumes. If the
work is bigger than the room, the correct move is to write a good note and open a new session —
not to push on and produce work that has to be redone.

---

## The trigger, in two tiers

- **Middle** → run **step 3 only** of the capture ritual: a light `_LIVE-STATE.md` flush. The
  session continues. No `GOOD-MORNING.md` rewrite, no chain regeneration, no new session.
- **Late / stop line** → run the whole ritual, steps 1 → 5, and open a fresh session.

A cue line that works well, said out loud rather than thought quietly:

> *This session has covered a lot and I'd rather write the handoff while it will still be a good
> one. Shall I wrap — worklist, then the state files, then regenerate the chain?*

---

## Two things worth stamping on your own work

**Say which you are quoting.** If you give any figure at all — files touched, components built,
gates run — say what it is a count of and how you got it. A count is not a measurement.

**Say what is unproven.** If a check did not run, "unproven" is the honest word. "Verified" is a
claim about a moment, and it starts ageing the second it is written.

---

## Why this runbook is shorter than Apollo's

Apollo's own gauge is long because it carries real instruments, ruled numeric bands, and the
history of how those numbers were arrived at and corrected. None of that transfers: the numbers
are specific to a different environment, and quoting them here would be quoting constants that
were never measured for your setup.

What transfers is the method, and the method is all of the above: **price the job before you
start it, count the wrap inside the price, throttle rather than report, declare what you cannot
measure, and end the session while you can still write a good note.**
