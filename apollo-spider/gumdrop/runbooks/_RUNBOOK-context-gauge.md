# Runbook — the context gauge (knowing when to stop)

*Memento — Gumdrop v1.0.4, for VS Code + GitHub Copilot.*
<!-- The version above is STAMPED at bake from the pack manifest's carries.version (s225-D3).
     Do not hand-edit it; a hand-typed version is what shipped the v1.0.0/v1.0.2 disagreement. -->

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

## ⚠ What can and cannot be measured here

> **⚠ THIS SECTION WAS WRONG UNTIL v1.0.3, AND THE CORRECTION IS THE POINT.** Every pack up to
> v1.0.2 said, in bold, *"Copilot in VS Code does not expose a token count to itself. There is no
> reading to take."* On 2026-08-29 that was **proven false** on a locked-down corporate machine:
> Copilot's agent can be told to write a debug log, and that log carries **the server's own
> reported token usage for the live session**. The gap this runbook declared is closeable, and the
> next section says how to close it. The correction is left visible rather than quietly swapped,
> because a runbook that silently rewrites its own history teaches the wrong lesson about records.

There are still **two different questions** here, and they are the thing most easily confused:

| question | what answers it | status in this pack |
|---|---|---|
| *How big is this piece of text?* | an **encoder** — `memento-package/machinery/_encoder_home.py`, exact `cl100k_base` | ✅ **shipped and working**, no network needed |
| *How full is this session?* | a **session usage reading** — Copilot's own agent debug log | ⚠ **available, but you must turn it on** (next section) |

The second is the gauge. It is not something this pack computes: nothing in here can count the
tokens of a conversation it cannot see. What it can do is **read back the number the server already
reported**, which is a real measurement rather than an estimate, and which is exactly what the next
section sets up.

Until you turn that on — and on any machine, any Copilot version, where it does not work — you are
on the **estimate tier**, and it must be named as such:

| tier | what it is | say it like this |
|---|---|---|
| **measured** | a real count from an instrument | "the debug log reports 144,266 input tokens on the last turn" — and say where it came from |
| **estimated** | your own running sense of the session's size | "we are maybe two thirds through the room I'd want for this" |
| **unknown** | you genuinely do not know | "I have lost track of how long this session is" — which is itself a reason to wrap |

⛔ **Never report an estimate as a measurement.** Do not invent a percentage. Do not say "we're at
60%" when nothing counted anything — a number with no instrument behind it gets believed, quoted,
and acted on, and it is the confident false inscription in its purest form.

**A declared gap passes; a silent one fails.** Saying "I cannot measure this, here is my estimate
and what I am basing it on" is a complete and honest answer. Saying nothing while the session
quietly fills up is the failure.

---

## 📖 Taking the reading by hand (Copilot's agent debug log)

This is a **manual reading**. The pack ships the settings that make the number exist; it does not
ship a parser that goes and fetches it. That is deliberate — see *Why there is no reader* below.

### 1. The settings that turn it on

They ship with this pack, at **`.vscode/settings.json`** in the pack root, so opening the pack as
your workspace is enough:

```json
{
  "github.copilot.chat.agentDebugLog.fileLogging.enabled": true,
  "github.copilot.chat.summarizeAgentConversationHistory.enabled": true,
  "github.copilot.chat.summarizeAgentConversationHistoryThreshold": 220000
}
```

- The **first** key is the one that matters for the gauge: it tells Copilot's agent to persist its
  debug log to a file instead of only to the output panel. The server-reported usage rides in it.
- The **second and third** are the automatic-conversation-compaction guard: they tell Copilot to
  summarise the conversation history when it crosses the named threshold. They are not the reading —
  they are the thing the reading lets you anticipate rather than be surprised by.
- **Reload the window after changing them** (⇧⌘P / Ctrl+Shift+P → *Developer: Reload Window*).
  The logging is decided when the agent starts, so a session already running will not begin writing.

⚠ **Honestly stated: these three keys are UNVERIFIED by us.** They were found working on one
designer's machine and are shipped on that evidence. We have not been able to drive them in our own
environment — no Copilot, no network. If a key has been renamed in your Copilot version, VS Code's
settings editor will grey it out or drop it; that is the symptom, and the remedy is to search
Settings for `agentDebugLog` and take whatever it is called now. **If the log never appears, you are
on the estimate tier — say so and carry on. Do not guess a number to fill the hole.**

### 2. Where the log lives

⚠ **KNOWN vs UNVERIFIED, kept apart on purpose.**

- **KNOWN:** the file is named **`main.jsonl`**, it is written by the Copilot Chat agent once
  file logging is enabled, and each request record carries the **server's reported usage** for that
  turn — input tokens, and how many of them were cached.
- **UNVERIFIED:** the exact directory. It sits under VS Code's own per-extension log directory,
  which is versioned, dated and platform-specific, and **we have not confirmed the path on any
  machine.** It is also undocumented by Copilot, which means it can move without warning.

**Find it, do not assume it.** The reliable route is VS Code's own command, which opens the right
folder whatever the layout is this month:

    ⇧⌘P / Ctrl+Shift+P → "Developer: Open Extension Logs Folder"  → GitHub Copilot Chat → main.jsonl

⛔ **A path written down here would age into a confident wrong answer.** If you find yours, write it
into your own `memento-package/_LIVE-STATE.md` — a fact about *your* machine, in *your* record,
which is where a machine-specific fact belongs.

### 3. What the number actually means

The last request record gives you three or four figures. They are worth quoting **together**,
because any one of them alone misleads:

| figure | what it is |
|---|---|
| **input tokens** | the server's count for what it was sent on that turn — **cumulative session usage**, not the size of your last message |
| **cached** | how much of that was a cache hit rather than fresh work — a cost figure, not a fullness figure |
| **compaction threshold** | the `…HistoryThreshold` you set above (220,000 as shipped): where Copilot will summarise the history to make room |
| **model maximum prompt** | the hard ceiling the model will accept |

*A real reading, from the machine this was found on:* **144,266 input tokens, of which 143,657
cached; threshold 220,000, so 75,734 of headroom; model maximum 271,997, so 127,731 of hard
headroom.* Three numbers, an absolute budget, and a declared threshold — that is a fuel gauge.

⛔ **DO NOT COMPARE THIS NUMBER TO ANYTHING ELSE IN THIS PACK.** It answers *how much has this
session sent the server*. It is **not** the size of any file, not the `tape` figure stamped on
`_CHAIN.md`, and not "how much of the conversation is still in front of the model". The encoder
measures **text you hand it**; this measures **a session**. They are different instruments answering
different questions, and putting them in the same sentence — or worse, subtracting one from the
other — produces a number that means nothing and will be believed anyway.

### 4. How to eyeball it as a rot warning

The reading's job is the one this runbook opens with: **it must change what you do.**

- **Take it at the seams**, not continuously — when a big piece of work finishes, and before
  committing to the next one. A gauge you read every turn is a thermometer again.
- **Watch the direction, not the digit.** The useful signal is the input-token figure climbing turn
  over turn while the *work* is not getting bigger. That is session rot: the conversation is
  carrying weight that is no longer earning its place.
- **Approaching the compaction threshold is a cue to wrap, not to panic.** Compaction is not a
  failure — it is Copilot summarising to keep going. But a summarised history is a *lossier* one,
  and the honest move is to write the handoff while the detail is still there rather than after.
  Crossing the threshold mid-task is exactly the "slow decline" this runbook opens by describing.
- **Say the number out loud when you quote it**, with its source: *"the debug log reports 190k input
  tokens against a 220k compaction threshold — I'd rather wrap now than have the history summarised
  underneath us."* That sentence is the throttle doing its job.

### 5. ⚠ Why there is no threshold in this runbook, and no reader

**No threshold**, because nobody has calibrated one on a designer's machine. A stop line is
*full, minus the price of the wrap*, and the price of a wrap in this environment has never been
measured. A threshold invented here would be a number with no instrument behind it — the exact
thing the tier table above forbids. **Set your own, from your own readings, and write it in your
`_LIVE-STATE.md`.** The first designer to record a few readings and what they cost has calibrated
it for real; that is worth more than a figure we guessed.

**No reader**, because the log path is undocumented and version-fragile. A shipped parser that
cannot find `main.jsonl` after a Copilot update would either crash or — far worse — return a
confident wrong number. Reading it by eye costs one command and never lies about its own source.
A built reader is *deferred, not dropped*: it becomes worth shipping the day Copilot documents the
log format, or the day a designer reports rot that this manual reading missed.

---

## The three postures

**With** a reading, the posture follows the number: where the input-token figure sits against your
compaction threshold. **Without** one — the log is off, or the keys do not exist in your Copilot —
judge the posture from what is actually observable: how long the session has run, how many files
have been opened, how much has been built, and — the most reliable signal — whether you are still
holding the thread of it. The observable signals below stay useful either way; a number that
disagrees with all of them is a number worth doubting.

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
