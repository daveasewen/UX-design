# Runbook — context gauge ("fuel gauge")

*Stood up 2026-07-19 at Dave's request: "I can tell when you're getting 'tired' — I need a method
of estimating token use … a hook for when we reach some threshold, run the ritual and move to a
new context window." This runbook is the method. Anchor: the capture ritual (`_RUNBOOK-capture-ritual.md`)
is where a Red reading sends us; this gauge decides **when**.*

---

## The problem, honestly

There is **no live token meter** exposed to the agent mid-conversation. Nothing says "you are 60%
full." So "tired" — the real thing Dave notices: fuzzier recall of early detail, more re-reading,
thinner attention — cannot be *read*, only **estimated** from proxies.

Two facts that shape the method:

1. **The budget is fixed** (~200k tokens for this model class). The system prompt, the full deferred
   tool list, the `MEMORY.md` index, every file read, and every tool-result dump all spend it —
   usually **more** than the agent's own word-generation does. In our sessions the real fuel-burners
   are canon file reads, review-round renders, and long review back-and-forths.
2. **Degradation shows up well before 100%** ("context rot"). Fine under ~45%, watch it 45–70%,
   move by ~70%. We do not wait for full.

## The gauge is two halves

### Half 1 — cheap, always-on: the running tally (near-free)

The agent keeps a rough cumulative token estimate **in-head** and reports a one-word band at the end
of substantive turns. No tooling, roughly ±15%. Reckoning (round to nearest 5k):

| Event | Rough cost |
|---|---|
| **Session baseline** (system prompt + tool defs + `MEMORY.md`) at start, THIS env | ~35k |
| Heavy file read (canon CSS/HTML, long runbook) | +2–8k (use the real line/char count) |
| Big tool dump / review render / subagent return | +1–5k |
| Normal exchange turn | +0.5–1.5k |
| A long agent output (like this build) | count it too |

Bands as fraction of the ~200k window:

- 🟢 **GREEN  <45%** (<~90k) — work freely.
- 🟡 **AMBER  45–70%** (~90–140k) — get economical, pre-stage the handoff, confirm before the next big read.
- 🔴 **RED  >70%** (>~140k) — **fire the trigger** (below).

### Half 2 — accurate, out-of-band: confirm at Amber

When the tally hits Amber, **confirm** with a real measurement before triggering — but measure
*without* polluting the main window. A throwaway Haiku subagent does the reading; the main agent gets
back only three numbers.

Subagent prompt (copy-ready):

> Call `list_sessions`. Find the parent session — the most recent one that is **not** yourself and not
> your own child. Call `read_transcript` on it with `format:"full"` and a high `limit`. Write the full
> transcript text to `/tmp/transcript.txt`. Then run:
> `python3 knowledge/_context_gauge.py /tmp/transcript.txt`
> Report back **only** the script's output (band, %, token estimate). Do not summarise the transcript.

The engine is `knowledge/_context_gauge.py` — tiktoken if available, else chars/4; flags
`--window` and `--baseline` are adjustable if the model/env changes.

## The trigger — wired to the existing ritual

At **Red** (confirmed, or high-confidence tally), the agent says, as a ready-to-use line:

> **Title this chat: `<retrospective title>` — context is Red (~NN%). Running the capture ritual, then
> open a fresh session with: `<forward title>`.**

That phrasing chains straight into two standing conventions so nothing extra has to be remembered:
- `session-title-convention` — every session opens with "Title this chat: …".
- `_RUNBOOK-capture-ritual.md` — the Red line **is** the cue to run steps 1→5 before the window fills,
  so the handoff is authored while there's still budget to author it well (never scramble it at 95%).

## Why this ordering matters

The failure mode is a handoff written *after* quality has already degraded — a confidently wrong
`GOOD-MORNING.md` is worse than none (`memento-framing`). Triggering at 70%, not 95%, keeps enough
clean context to do the capture ritual properly. The gauge exists to protect the ritual, not to
squeeze the last token out of a session.

## Entry points

`_RUNBOOK-capture-ritual.md` (where Red sends us) · `knowledge/_context_gauge.py` (the engine) ·
memory `feedback-context-gauge` · `session-title-convention` · `memento-framing`.
