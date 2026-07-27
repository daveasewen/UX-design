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
2. **Degradation shows up well before 100%** ("context rot"). Fine under ~45%, watch it 45–60%,
   move by ~60%. We do not wait for full.

## The gauge is two halves

### ★ Half 0 — PRE-FLIGHT: price the job BEFORE committing to it (RULED by Dave, 2026-07-27)

**Dave, at the wrap that forced this:** *"this needs to be flagged before embarking on big jobs, you
have to estimate before committing to a big task."*

Halves 1 and 2 both answer *"where am I now?"* — a question whose answer arrives **after** the tokens
are spent. That is why the gauge kept failing while being technically present: it was consulted at
wrap, when the only remaining option is to stop. **A gauge that only reports is not a gauge, it is a
postmortem.**

**The rule: before starting any job with a plausible cost above ~10% of the window, state TWO numbers
to Dave, unprompted, in the same breath as the plan.**

```
current fill  +  estimated cost of this job  =  projected band at completion
```

- **Projects into Red?** Say so **before** starting, and offer the fork: **(a)** narrow the job to
  fit, **(b)** flush + hand the build to a fresh window, **(c)** proceed knowingly with a Red stamp.
  **Dave chooses. Do not choose silently by starting.**
- **Jobs that need pricing** (all observed to blow past estimate): a render-verify harness built from
  scratch · a new gate + its selftest · a review sheet or interactive prototype · a corpus-wide sweep ·
  an ADR plus the build it describes. *Rough anchors, 2026-07-27: standing up render-verify cold ≈
  15–20% · a generator + wiring + its ADR ≈ 25–30%.*
- **Re-price when the job changes shape.** The 2026-07-27 session priced nothing, then absorbed a
  discriminator, a render env rebuild, two probe rewrites, a generator, an ADR and the full ritual —
  each individually reasonable, cumulatively 85%.

### ⚠ READ THE BAND TABLE. DO NOT RECALL IT.

**Recalled bands were WRONG on 2026-07-27:** the agent reported **"🟡 Amber ~70%"** and then
**"Amber ~85%"** — both Red by the table twelve lines below, which had been correct all along. The
mislabel propagated into the `GOOD-MORNING` banner, `_LIVE-STATE` and Dave's summary before he caught
it. **A false reading of the very instrument built to catch false inscription**, and it is the same
failure class as [[stale-reading-failure-mode]]: the corpus was right, the recall was not.

⇒ **Quote the band from this file, or `grep` it. A band asserted from memory is not a reading.**
⇒ **State the NUMBER and the BAND together** (`~85% → RED`) so a mismatch is visible to Dave in one
glance — he caught this one exactly that way.

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
| **★ THE INSTRUMENTS THEMSELVES — see below. They are NOT free.** | |
| — the capture ritual | **+~5% (MEASURED 2026-07-27)** |
| — the task list (create + each update; it re-renders) | +0.5–1k per burst |
| — a Half-2 gauge confirmation (subagent + transcript) | +1–3k |
| — a consult, a build run, a gate report read | +1–4k each |

### ★★ PRICE THE INSTRUMENT, NOT JUST THE WORK (Dave, 2026-07-27: *"remember that it self consumes tokens too"*)

**The measuring costs what it measures out of.** Every row in the block above is overhead the agent spends
*observing and reporting* rather than doing the job — and it is the row most often left out of a pre-flight,
because it does not feel like work.

**This is not hypothetical; it is the exact failure of 2026-07-27 (later morning #2).** The render job was
priced in advance (*"38% + 15% = 53%"*) and the estimate **held**. Then the **capture ritual ran unpriced**
and cost ~5%, taking a true 🟡 Amber ~58% to 🔴 Red ~63%. **The pre-flight rule was obeyed for the work and
skipped for the instrument** — which is the same omission one step later, and it is why the band stamped on
that handoff had to be corrected at close.

**⇒ THE MECHANISM, and it is one line:**
> **A pre-flight estimate that does not include the wrap is not a pre-flight estimate.**
> `fill + job + WRAP (~5%) = projected band` — always three terms, never two.

**Two consequences that bite:**
- **Reserve the wrap before starting the job, not after.** At 🟡 Amber, an unreserved ritual is what pushes
  the session Red — so the honest question at Amber is never *"can I fit this job?"* but **"can I fit this
  job AND the ritual?"** If not, the job does not start; the flush does.
- **Instrumentation is subject to its own bands.** At Amber, get economical with the instruments too —
  fewer, tighter task entries; skip the Half-2 confirmation unless the band is genuinely in doubt; do not
  re-read a gate report you have already read. *(Dave, same day: "be careful with the tasks.")*
  ⚠ **But never economise by skipping the READING of the band table** — that is the one instrument whose
  omission caused a wrong band twice, and it costs a `grep`.

Bands as fraction of the ~200k window:

- 🟢 **GREEN  <45%** (<~90k) — work freely.
- 🟡 **AMBER  45–60%** (~90–120k) — get economical, pre-stage the handoff, confirm before the next big read. **PROACTIVELY surface the band to Dave here and offer to start wrapping / capture soon — do NOT wait to be asked** (Dave, 2026-07-20: *"I would set it at amber too"*; the agent suggesting session-end from the estimate, unprompted, is the whole point — silence while the tally climbs is the failure mode). **★ Also fire the light SPINE-FLUSH here (Amber tier, ruled 2026-07-21 — see trigger below): write current state to `_LIVE-STATE.md` now, WITHOUT ending the session.** **★ AND DO NOT START A NEW BUILD ARTEFACT AT AMBER** — a review sheet, an interactive prototype, a new component. They are deceptively token-heavy and are exactly where hot-session "silly mistakes" land (2026-07-24: two review sheets/prototypes built *past* Amber → a render bug + Dave calling the handover, *"we're obviously hot, there are silly mistakes"*). Design/decision **writing + inscription** is fine hot; a new **interactive build** is not — flush and hand the BUILD to a fresh window.
- 🔴 **RED  ≥60%** (≥~120k) — **fire the full trigger** (below): the complete capture ritual + fresh session.

*(Bands recalibrated by Dave 2026-07-25: **Green <45 · Amber 45–60 · Red ≥60**. Amber floor moved 50→45; earlier the runbook read Amber 50–60. The move-by point is unchanged at 60.)*

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

## The authoring-time STAMP — record the gauge ON the artefact (Dave, 2026-07-24)

Every handoff artefact records the author's gauge reading **at the moment of authoring**, as a
**scrutiny indicator on that artefact's reliability — NOT a quality verdict.** A record already carries
provenance and confidence, not just content (`memento-framing`); the fill level it was written at is
exactly such a confidence annotation. A Red-authored commit or handoff is where confident-false
inscription is most likely — so the reader deserves to know. A Red artefact is not *necessarily*
wrong, and a Green one is not *guaranteed* right; the stamp predicts **inscription-risk**, and the
useful thing is the action it implies, not the number:

- 🔴 **Red at authoring → the next reader RE-VERIFIES before trusting** (re-run `_build_all.py`,
  spot-check the reconcile / every "landed" claim's evidence) — treat the artefact as suspect.
- 🟡 **Amber → skim-check** the load-bearing claims. 🟢 **Green → normal trust.**

**Where + format.**
- The **creator** (conductor/solo) stamps it in `GOOD-MORNING.md`'s COMMIT STATE block.
- Each **worker** stamps it in its receipt header (`_RUNBOOK-parallel-conductor.md` worker step 4).
- One line: `Context gauge at authoring: 🟢/🟡/🔴 BAND ~NN% (in-head tally, ESTIMATE ±15% — Half-2
  broken).` This already appears informally as "wrapped Red / ~Amber" in the ★ banner; the rule
  formalises it as a REQUIRED field and extends it to receipts.

**Live proof — the session that added this rule (2026-07-24):** the prior conductor wrapped *deep Red*
and left a real showroom-sync gap — the committed tree failed `_build_all.py` while the spine claimed
"53/53 green." The follow-up conductor, authoring in Green, re-ran the build, caught it, and fixed it
(`eb9c9ec`). Had the Red wrap carried this stamp, it would have told that reader to scrutinise the
commit *before* trusting the "green" claim — which is the whole point.

## Entry points

`_RUNBOOK-capture-ritual.md` (where Red sends us) · `knowledge/_context_gauge.py` (the engine) ·
memory `feedback-context-gauge` · `session-title-convention` · `memento-framing`.
