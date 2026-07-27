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

**The rule: EVERY job is priced and debited — and the estimate is stated to Dave, unprompted, in the
same breath as the plan, whenever it could move the band or reach the reserve. THREE terms plus a fence.**

*(RULED by Dave 2026-07-27: *"every job should be priced, so we have a budget for everything, like real
life."* **Like real life** is the operative phrase and it sets the ceremony: every purchase debits the
account, but you do not hold a board meeting over a coffee. **Debit always; state out loud when it
matters.** The old rule had a ~10% floor — and every overrun on record arrived as a series of steps each
individually under it, which is precisely how a floor fails.)*

```
fill  +  job  +  WRAP (~5%)          =  projected band at completion
RESERVE (~15%, RING-FENCED)          =  the line you may not cross without asking
```

*(The three-term rule is below under "the wrap is part of the job". The RESERVE is the fence ruled on
2026-07-27 — see ★ Half 0b. It is **not** a fourth addend: adding it to the projection is exactly the
mistake it exists to prevent.)*

- **Projects into Red?** Say so **before** starting, and offer the fork: **(a)** narrow the job to
  fit, **(b)** flush + hand the build to a fresh window, **(c)** proceed knowingly with a Red stamp.
  **Dave chooses. Do not choose silently by starting.**
  ⇒ **★ Since 2026-07-27 this fork has TWO triggers, not one — see ★ Half 0b.** It used to fire only
  before starting, which is why a finding landing mid-job could never reach it.
- **Jobs that need pricing** (all observed to blow past estimate): a render-verify harness built from
  scratch · a new gate + its selftest · a review sheet or interactive prototype · a corpus-wide sweep ·
  an ADR plus the build it describes. *Rough anchors, 2026-07-27: standing up render-verify cold ≈
  15–20% · a generator + wiring + its ADR ≈ 25–30%.*
- **Re-price when the job changes shape.** The 2026-07-27 session priced nothing, then absorbed a
  discriminator, a render env rebuild, two probe rewrites, a generator, an ADR and the full ritual —
  each individually reasonable, cumulatively 85%.

### ★ Half 0b — THE THROTTLE: the gauge must be able to CUT WORK (RULED by Dave, 2026-07-27)

**Dave, at the wrap that forced this:** *"the pre-flighting needs work, we cant keep hitting red, its a
waste of effort."* Ruled cold the following window, deliberately — the diagnosis was authored at ~97%
fill, and a rule about not working past your budget must not itself be inscribed past budget.

**The evidence: three Red sessions running — 🔴 ~92% · 🔴 ~63% · 🔴 ~72%**, overruns of **+?, +5, +17**.
The three-term rule was inscribed *during* the last of those and **did not stop it.**

**★ THE FINDING: hitting Red is a SCOPE failure, not a MEASUREMENT failure.** A better estimate would
not have saved any of those three sessions; **only cutting would have.** The gauge was being used as a
**thermometer** — it reported how hot the session was and never once told it to stop.

**RULED (a) — the reserve is RING-FENCED, not additive. ~15%.** It is a budget you **may not spend
without asking**, not a term you add to make the projection fit. Sized from the observed **worst**
overrun (+17), not the mean: *n*=3 with one unknown, so a mean would be false precision, and the error
is **asymmetric** — under-reserving costs a wasted session (*"a waste of effort"*), over-reserving costs
a slightly early wrap.

⚠ **THE NUMBER IS PROVISIONAL AND WEAKER THAN THE SHAPE.** The *shape* (ring-fenced, not additive) is
firm. **15% is sized from n=3 with one value unknown, and the +17 it keys off was a single unusual event**
(chasing ds-016) — that is a tail observation doing the work of a distribution. ⇒ **Re-derive after ~5
more sessions of recorded overrun**, and record each session's actual overrun at wrap so there is
something to re-derive *from*. Flagged at inscription by the author, not discovered later.

**RULED (b) — spending the reserve is a TRIGGER, and the fork goes to Dave.** On **any unplanned
finding**: stop, re-price out loud, and put the fork to him — **(a)** log it and stop · **(b)** narrow ·
**(c)** chase it knowingly with a Red stamp. **Not a decision the agent makes silently from inside the
sunk cost**, which is exactly how ds-016 got chased for +17.

**★ THE MECHANISM ALREADY EXISTED; ITS TRIGGER WAS AT THE WRONG TIME.** The fork in Half 0 above was
written before this ruling and is precisely the throttle Dave asked for — it just fired **only** before
starting. Extended, one word: **before starting AND on any unplanned finding.** *(Same class as the
morning's other findings — the right rule, unreachable at the moment it is needed.)*

**RULED (c) — A NEW SESSION IS A REFILL, NOT A PENALTY** *(Dave, same window: "we can reset the budget
at any time by starting a new session").* This is the clause that makes the throttle cheap to obey.
The fork's option **(b)** — flush and hand to a fresh window — has been written as a last resort; it is
in fact **the normal way more budget is obtained**, and under this ruling it is often the FIRST answer,
not the reluctant one. **Cutting work no longer means losing it.**

⚠ **But a refill is not free — it costs the cold read.** MEASURED 2026-07-27: a fresh session reached
~**22%** fill on `GOOD-MORNING.md` + `_LIVE-STATE.md` + the memory index **before doing any work**
(*n*=1 — treat as an anchor, not a constant, and re-measure when the handoff's size changes).
⇒ **A fresh window buys ~78%, not 100%**, which gives the fork an arithmetic:

> **Flush whenever the remaining budget is smaller than the job plus its wrap.** You are trading ~22%
> of re-read for ~78% of clean room — a good trade well before Red, and a bad one for a job that would
> have fitted.

**★ THE MODEL, in Dave's words (2026-07-27):** *"the individual budgets stay the same but we can always
pull from a larger 'bank' of tokens by moving to a new window."* ⇒ **The window is the BUDGET; the BANK
is the constraint.** The budget per window is fixed and non-negotiable; the bank behind it is large but
finite and it is what actually gets spent.

⇒ **The re-read is a TRANSACTION FEE on every withdrawal** — ~22% of a window, pure overhead, buying no
work. That single fact resolves the posture in both directions and neither extreme is right:
- **Never flushing** spends the fee zero times but wastes whole sessions in Red — *"a waste of effort."*
- **Flushing freely** never goes Red but pays ~22% every time, and the fee comes out of the bank.
⇒ **So: SIZE JOBS TO FIT A WINDOW so the fee is paid rarely; and when a job genuinely will not fit, pay
it rather than burn the session.**

### ★★ THE THIRD TIER — the weekly allowance is PERISHABLE, and it inverts the objective

**⚠ CORRECTION, inscribed as loudly as the claim it replaces (2026-07-27, same window).** This section
first read: *"minimising Reds and minimising flushes are the same objective — fewer tokens spent against
the bank for the same work."* **That is wrong, and Dave corrected it within minutes** by showing the
plan-usage panel: *"the overall weekly budget, which we need to max-out or loose."*

**There are THREE tiers, not two:**

| tier | unit | behaviour | resets |
|---|---|---|---|
| **the job** | one task | priced + debited, always | — |
| **the window** | ~200k context | fixed, non-negotiable, refillable by starting a new session | per session |
| **★ the week** | plan allowance | **PERISHABLE — unspent allowance is LOST** *(INFERRED, see below)* | Thu 23:00 |

⚠ **PROVENANCE OF THE PERISHABLE CLAIM — `status: inferred`, not observed.** It rests on the plan-usage
panel (a percentage bar with a reset time) plus Dave's reading of it (*"which we need to max-out or
loose"*). **Not verified:** whether the percentage meters tokens, messages or a composite; whether the
Fable line draws from the same pool as "all models"; whether anything rolls over. Confidence ~75% —
enough to act on, **not** enough to have gone into a canon table as a fact, which is what happened for
twenty minutes on 2026-07-27 before this line was added. *(The failure this project exists to prevent is
confident false inscription; the correction is the record working, not an embarrassment to hide.)*

⇒ **The objective is NOT to minimise tokens. It is to MAXIMISE WORK DONE PER WEEK.** Under-spending the
weekly allowance is a failure of exactly the same kind as burning a session in Red — both convert
allowance into nothing. *(MEASURED 2026-07-27 12:07, Max 20×: week 51% elapsed, **33% consumed = 0.65×
pro-rata**; Fable **28% = 0.55×**, the most under-used line of all. 83h and 67% of allowance left ⇒
**1.36× pro-rata needed** for the rest of the week just to avoid losing it.)*

**⇒ THE PACE CHECK sets the posture for tier 2.** Compare weekly-consumed % against week-elapsed %:

- **BEHIND pace** (consumed < elapsed) — allowance is expiring. **Flush freely; run more windows; do not
  economise.** The ~22% re-read fee is close to irrelevant, because the alternative is not saving the
  tokens, it is **losing them at Thu 23:00.** Prefer the bigger model, the fuller proof, the extra bite.
- **ON or AHEAD of pace** — the fee is real. Size jobs to fit, flush reluctantly, economise at Amber.

⚠ **This does NOT license Red sessions.** A Red session wastes allowance *and* produces the silly
mistakes Dave has called out; a flush converts allowance into work. **Behind pace, the correct move is
MORE WINDOWS, not longer ones.** Red is still the failure; hoarding is now also a failure.

⚠ **Rationing a model against its own line is a hoarding trap.** Fable is "reserved for open-judgment"
by routing — but its allowance is separately metered and separately perishable, so **reserving it past
the point where it can be spent is not discipline, it is waste.** If the Fable line is behind pace and
Fable-shaped work is queued (the ruling batch), spend it.

#### ⚠ ANTI-FALSE-FIX

1. **Do not fold the reserve into the job estimate** so the projection fits the band you wanted. That
   converts the throttle straight back into padding, and padding is a thermometer.
2. **The reserve is a LINE, not an allowance.** `fill + job + wrap + 15%` is not a budget to run to;
   crossing the line is a **question put to Dave.**
0. **⚠ THE GATE PROVES THE STAMP, NOT THE RULE — and that gap is ADR-0016's "dangerous middle".**
   `_capture_gate.py` has a selftest proving its FORM check can fail, so *the form check* is PROVEN.
   **The RULE this section states — price every job, re-price on a finding, take the fork to Dave —
   is UNPROVEN and unprovable by any gate in this repo.** A well-formed stamp carrying invented
   numbers passes. ⇒ **Do not let the green tick be read as compliance.** Registering it otherwise
   would make it a CLAIMED row, and *"a green light from a blind check is worse than no check."*
   *(Flagged by the author at inscription, 2026-07-27, unprompted-by-a-gate.)*
3. **What a gate can honestly check is the FORM of the stamp** — term count, arithmetic, and that the
   named band matches the band table. **It cannot check whether the fill figure is honest, and it cannot
   observe whether a mid-job re-price happened.** Those are discipline. Claiming otherwise would be the
   false inscription this programme exists to stop. *(Enforced form: `_capture_gate.py --wrap`.)*

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
| **Session baseline** (system prompt + tool defs + `MEMORY.md`) at start, THIS env | ~35k — ⚠️ **SUSPECT, see note** |
| Heavy file read (canon CSS/HTML, long runbook) | +2–8k (use the real line/char count) |
| Big tool dump / review render / subagent return | +1–5k |
| Normal exchange turn | +0.5–1.5k |
| A long agent output (like this build) | count it too |
| **★ THE INSTRUMENTS THEMSELVES — see below. They are NOT free.** | |
| — the capture ritual | **+~5% (MEASURED 2026-07-27)** |
| — the task list (create + each update; it re-renders) | +0.5–1k per burst |
| — a Half-2 gauge confirmation (subagent + transcript) | +1–3k |
| — a consult, a build run, a gate report read | +1–4k each |

⚠️ **NOTE ON THE ~35k BASELINE — it is a snapshot constant and the harness has moved under it
(flagged 2026-07-27 #14, the GM-D9 enactment window).** The row was written when every tool schema
loaded up front. This env now **defers most tool schemas** — they arrive as bare names and are fetched
on demand — which removes a large, previously unavoidable block from the opening fill. The enacting
session's own estimate put its baseline nearer **~12–15k**.
**That figure is NOT inscribed, deliberately: it is an estimate, not an observation** — there is no token
meter, and replacing one unmeasured constant with another is the defect, not the fix
(`measuring-tool-must-not-guess`: observe, don't infer; UNKNOWN is never defaulted).
⇒ **Treat the row as an upper bound of unknown tightness, and MEASURE the floor per session (GM-D9 below).**
The whole point of the D9 mechanism is that this row should not need to be right.

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

### ★ THE FLOOR IS MEASURED, NEVER ASSUMED — and this is the only copy of the band table (GM-D9)

*(Ruled 2026-07-27, `notes/_MEMENTO-DECISIONS.md` § GM growth-contracts. **Dave's reframe, and it is the
whole decision:** the cold-start floor is **a variable this programme shrinks**, so a snapshot constant
written into canon would be **falsified by its own enactment** — the prose-drift class, self-inflicted.)*

**Two rules, and they replace every earlier treatment of the floor:**

1. **MEASURE the floor at session start — announce the fill after the mandated reads, before pricing
   anything.** Not "the floor is about 22–24%": *this* session's floor, this window, stated as a number.
   The floor moves with what you actually read — a session that reads `GOOD-MORNING.md` alone does not
   have the floor of one that reads the whole chain, and the two must not be priced the same.
   ⚠️ **The old band table priced the floor at ZERO** (SD-7) — it described fill as though every window
   started empty. It never did.
2. **Bands are read against REMAINING BUDGET.** What decides a fork is never how full you are, it is
   whether what is left can hold the job *and* its wrap. This is already the arithmetic of the flush rule
   above (*"flush whenever the remaining budget is smaller than the job plus its wrap"*); the table below
   is now stated the same way so the two cannot drift apart.

| Band | Remaining budget | ≡ fill (unchanged) |
|---|---|---|
| 🟢 GREEN | **> 55%** left | <45% used |
| 🟡 AMBER | **40–55%** left | 45–60% used |
| 🔴 RED | **< 40%** left | ≥60% used |

**The numbers are Dave's and are re-dialled only by him, here.** The table above is a restatement, not a
recalibration — the thresholds are byte-identical to the ratified bullets below, which stay as he wrote them.

★ **THIS FILE IS THE ONLY COPY.** `GOOD-MORNING.md` used to carry an inline band table; per GM-D9 it now
carries a **pointer to this section**. ⚠️ **Two copies of a band table WILL drift** — and this one has
already been misquoted from memory twice in one day (below). Quote it from here or `grep` it; never recall it.

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
