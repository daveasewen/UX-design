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
2. **Degradation shows up well before 100%** ("context rot"). Fine under ~50%, watch it 50–60%,
   move by ~60%. We do not wait for full.

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

- 🟢 **GREEN  <50%** (<~100k) — work freely.
- 🟡 **AMBER  50–60%** (~100–120k) — get economical, pre-stage the handoff, confirm before the next big read. **PROACTIVELY surface the band to Dave here and offer to start wrapping / capture soon — do NOT wait to be asked** (Dave, 2026-07-20: *"I would set it at amber too"*; the agent suggesting session-end from the estimate, unprompted, is the whole point — silence while the tally climbs is the failure mode). **★ Also fire the light SPINE-FLUSH here (Amber tier, ruled 2026-07-21 — see trigger below): write current state to `_LIVE-STATE.md` now, WITHOUT ending the session.**
- 🔴 **RED  >60%** (>~120k) — **fire the full trigger** (below): the complete capture ritual + fresh session.

**The tally is a protocol, not a stop signal** (routing audit #11, ratified Dave 2026-07-23):
below Amber, work at full quality with no economising — the bands change behaviour only at their
thresholds. This line exists because a surfaced token count is a documented trigger for premature
wrap-up in Fable-class models (the primary source's own remedy is exactly this reassurance); the
gauge's numbers stay BY DESIGN — deliberate wrap at threshold is the mechanism, not the failure mode.

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

> ⚠ **HALF 2 IS CURRENTLY BROKEN in the Cowork env (observed 2026-07-21 late night #3) — do not
> trust its number.** Two failure modes, both observed: (1) `read_transcript` renders tool calls as
> one-line stubs with RESULTS STRIPPED — the real fuel-burners (file reads, tool dumps) are absent,
> so it under-reads catastrophically (13KB rendered for a session whose receipts alone are bigger);
> (2) the LIVE session is hard to identify in `list_sessions` (untitled mid-flight), so the subagent
> measured the *previous night's* session — then rationalised the bad number ("the reading is
> valid"). **Until rebuilt, Half 1 (the in-head tally) governs**; a Half-2 reading that disagrees
> with the tally by >2× is presumed wrong, not reassuring.

## The trigger — TWO TIERS (ruled by Dave, 2026-07-21)

Compaction is not one event. Firing the full ritual + fresh session at every Amber would churn
sessions needlessly; never flushing until Red risks losing state to a crash or an abrupt end. So the
trigger is **tiered** — a cheap save at Amber, the full handoff at Red:

- 🟡 **AMBER → light SPINE-FLUSH (no session end).** Do capture-ritual **step 1 only** — refresh
  `_LIVE-STATE.md` (and `_FUTURE-STATE`/`_DECISION-HISTORY` if touched), stamped from `date`. This
  makes the current state durable *now*, so if the session ends abruptly the loss is bounded. The
  session continues — do NOT write `GOOD-MORNING`, do NOT rename, do NOT open a fresh window. Repeat
  the flush if the session runs long and state moves materially. *(Rationale: this is our hand-rolled
  equivalent of platform context-compaction — keep the invariants in high-signal text, cheaply, before
  the window is under pressure. Native equivalents now exist — memory tool GA · context-editing ·
  compaction beta — but aren't exposed as Cowork knobs, so the ritual stays the mechanism.)*
- 🔴 **RED → the FULL trigger + fresh session** (below). Everything the Amber flush already saved makes
  this handoff faster and safer to author.

## The Red trigger — wired to the existing ritual

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
