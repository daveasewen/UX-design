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
2. **Degradation shows up well before 100%** ("context rot"). Fine under AMBER, watch it between
   AMBER and WORKING, move at the latest by WORKING itself — absolute token thresholds, not a
   percentage of the window (see the band table under "THE UNIT AND THE BUDGET" below). We do
   not wait for full.

## The gauge is two halves

### ★★ THE UNIT AND THE BUDGET — RULED BY DAVE #56, and it retires the percentage stamp

**Read this before Half 0: the terms below are what Half 0 is denominated in.**

**The stamp is now ABSOLUTE, in REAL Claude tokens.** Form:

```
pre-flight #NN: boot N (disk N measured · harness ~N est ±N, ds-025)
              + job N est + wrap N est  =  N of 200,000  —  BAND
```

⚠ **Nothing in it divides by anything.** That is the entire design. The old stamp priced every
term as a *percentage of the window*; the window's harness half is unreachable from inside any
mount (`ds-025` item 1); so the denominator had no value and `check_preflight` — which failed on
any missing term — voided the whole stamp. **One unobservable quantity suppressed every
observable one, for thirteen consecutive sessions**, which is exactly the failure **D10 (c)**
exists to forbid, committed inside the instrument that rules it.

**⛔ THE BAND WAS NOT CONVERTED. IT WAS REPLACED.** `45 / 60 / 63` were percentages *of the
window*; turning them into tokens means multiplying by the exact quantity nobody can observe.
These are NEW thresholds with their own provenance [[measure-dont-convert-units]]:

| number | value | authority |
|---|---|---|
| **HARD** | 256,000 | **SOURCED** — the largest context at which Claude's recall has been publicly measured and still holds (93% MRCR v2; 76% at 1M). Past it there is no measurement to reason from. |
| **WORKING** | 200,000 | **SOURCED**, not Dave's preference — entered force at #56, provenance corrected #58b. The line jobs are priced against it. |
| **AMBER** | 160,000 | **PICKED**, not derived — corrected #59. 80% of working is a round fraction, not a formula. |

⚠ **PROVENANCE OF THE TWO ROWS ABOVE WAS ITSELF CORRECTED TWICE AFTER THIS TABLE WAS FIRST WRITTEN
(#58b, #59) — folded in above; here is why, so a later re-read does not silently drift back.**
WORKING read "DAVE'S, ruled #56" for three sessions until Dave corrected it himself: *"BTW the 200K
and 256K come from established research, its been worked out already."* Both HARD and WORKING are
SOURCED; 200,000 was never his to re-dial by fiat. AMBER read "DERIVED — 80% of working" until #59:
a round fraction is a PICK, and labelling a pick "derived" makes it immune to the very rule meant to
catch it (*"derive a cap, never pick it"* — #53). ★ **THE FORMULA IS THE RULING, THE NUMBER IS NOT:**
`stop = wall − wrap − step`, each term tagged MEASURED or ESTIMATED; reserve the HIGH end of both
terms or neither — stacking a step-reserve on an amber that already contains one is a
reserve-on-a-reserve, invisible because each layer is individually defensible.

★ **The marker buys the WORKING overrun and does NOT buy the HARD one.** `RESERVE SPEND — forked
to Dave` lets a session cross 200,000 deliberately. Nothing lets it cross 256,000, because a
receipt cannot manufacture evidence that was never collected. **Split the job, or delegate part
of it to a subagent with its own window.**

**⛔ A DECLARED GAP PASSES; A SILENT ONE FAILS.** A term you cannot measure is written as an
estimate with its error bar, or declared `unobservable (<reason>)`. Leaving it out is the only
thing punished. That asymmetry is the fix — it makes publishing cheaper than refusing.

**★★ THE BOOT'S HARNESS HALF IS AN ESTIMATE AND THAT IS FINE — the argument, so it is not
relitigated.** ±8,000 tokens on a 200,000 budget is ±4%, and no job's go/no-go flips on 4%. We
were holding a **planning estimate** to a standard built for a **published measurement**.
*"A measuring tool must not guess"* governs what we assert as fact; it was never a ban on
estimating, and reading it as one produced thirteen blank stamps. **Estimate it, LABEL it, carry
the error bar, move on.** ⚠ Re-measure when the session shape changes — a new MCP server moves it.

**★★ POSITION MATTERS AS MUCH AS VOLUME, and it is the cheaper lever.** Recall is **U-shaped**:
strongest at the START and END of a window, ~30% weaker in the MIDDLE (Anthropic's own framing is
*"a performance gradient rather than a hard cliff"*). The chain is read first and the wrap is
written last, so **canon already sits at the two strong ends — that is the architecture doing
work, not luck.** ⇒ **A finding made mid-window is sitting in the weakest region: write it to its
home when you find it, never carry it to the wrap.**

**⚠ ONE MORE THING #56 FOUND, AND IT CHANGES HOW THE PAST THIRTEEN SESSIONS READ.** `PREFLIGHT_RE`
did not match the live banner form `pre-flight #55:` — only a bare `pre-flight:`. So the gate was
reading the **first ARCHIVED STRATUM** in the file, not the current session's stamp. Those strata
say *"FIFTH consecutive"*, *"SIXTH consecutive"* and are ratified history: they can never go
green. **For those sessions the pre-flight FAIL was unfixable by construction** — a perfect stamp
written today could not clear a failure being read off a block written weeks earlier. ★ This is
[[unmatched-grep-is-not-an-absence]]'s third face inverted: the pattern **matched**, so nothing
looked broken — but *a matched pattern is not the right pattern.* Widened + pinned by a fixture.

**Entry points:** `python3 knowledge/_gauge_tokens.py` prints the budget, the boot split and the
room left. The `#53` guard (`assert_budget_clears_floor`) refuses a budget at or under its own
floor, so the *"cap set below its own floor"* defect cannot ship again.

---

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

**★ VISIBILITY IS PART OF THE STAMP (added #78, on Dave's own miss).** At #78 the opener price was
complete, legal-form, and stated unprompted — buried mid-paragraph in prose, and **Dave read past it
and later asked *"are we still pricing jobs? didn't notice at the opener."*** A price the person
budgeting cannot SEE has failed its purpose exactly as fully as one never made; he is dyslexic and
time-poor by his own standing note, and the chat half of this ritual is ungateable, so FORM is the
only enforcement it has. ⇒ **The opener price is ONE bold line, FIRST or SECOND line of the opener
message, shaped like the stamp** (`**PRICE:** boot N + jobs N est + wrap N = N of 200,000 — BAND`),
never woven into a paragraph. Mid-session re-prices get the same one-line form at the moment they
happen. The stratum's legal-form stamp is unchanged — this clause governs the CHAT rendering only.
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

**RULED (a′) #74 — THE WRAP TERM IS RING-FENCED TOO (Dave, explicit option-select; floated #73,
priced and adopted #74).** The pre-flight form already *requires* a wrap term, but nothing said it
was untouchable — and #72 proved the gap: the wrap is last in the window, so a budget squeeze cuts
it first, and a skipped or starved wrap costs more than any job it saved (the chain then certifies
the wrong session). ⇒ **At any mid-session re-price, the wrap term keeps its opener value and the
JOB is what shrinks.** Discipline, not machinery — no gate can see the window, so this paragraph is
the enforcement, same status as the reserve above. A session that must eat its wrap reserve says so
out loud at the moment of eating it, not at the wrap.

### ★★ ds-023 — THE CEILING AND THE STOP LINE (ruled-in-part #31 in Dave's own words, enforcement picked #31 delegated, ENACTED + CONFIRMED #34; numbers REPLACED by #56 — see note below)

**Dave, #30:** *"it's calculating 60+15 headroom is okay and it definitely isn't, 60 should be a hard
stop."* **#31:** *"the wrap should be done before we hit that mark thats when things go wrong… we should
never run hot."* **#34, confirming:** *"this is making me suffer unduly."* *(Quoted verbatim, in the
percentage vocabulary live at the time — "60" here means 60% of the window, the pre-#56 RED threshold.
Kept as history; the operative numbers below are #56's.)*

⚠️ **THIS WAS NEVER A CALIBRATION GAP — it was an ENFORCEMENT gap.** Everything above already said so,
three times, verbatim. The rule existed, was correct, was ratified, and **nothing checked it**. Same
shape as ds-021 and ds-022; all three were raised in one session and enacted in one.

**Two numbers, restated in real tokens by #56 (the SHAPE is Dave's from #31/#34; the percentage
values `45`/`60` he ruled were REPLACED, not converted — see ★★ THE UNIT AND THE BUDGET above):**

| | value | what it means |
|---|---|---|
| **pre-flight ceiling** | **fill + job + wrap < 160,000 (AMBER)** | a job must be projected to finish GREEN. **Checked, and it FAILS a wrap. Exactly 160,000 ITSELF FAILS** — `band_for()` reads it AMBER, not GREEN (strict `<`, bitten by the gate's own selftest). |
| **in-flight stop line** | **200,000 (WORKING) − the priced wrap, in tokens** | **MOVES with the wrap price and is not its own constant** — an expensive wrap must stop the session earlier. ⛔ **THE RULED FORM, STATED VERBATIM AND SUPERSEDED IN THE SAME BREATH — `60 − the priced wrap`, and `60 is where the wrap has FINISHED`, not where it starts (ds-023, RULED #31, ENACTED #34, Dave's).** It is written out here because **`_capture_gate.stop_line_consistency()` asserts THAT EXACT STRING in this file and BLOCKS without it** — and at #83 it blocked a wrap for a rewrite that had re-denominated the ruling FAITHFULLY. ★★ **A gate pinned to a retired unit's WORDING cannot tell a faithful re-denomination from a deletion, so it made the CORRECT state unreachable** — the `ds-022 (d)` vs `roll_2f` shape again. **Restored by ADDITION, never by reverting the correct line** [[home-by-addition-then-cut]]. ⬛ **FORKED TO DAVE, not decided here: re-denominate ds-023's stop line into real tokens and re-pin `STOP_LINE_HOMES` to the new wording. The numbers are his (#31/#34); an agent quietly editing a gate to accept its own paraphrase of a ruling is exactly the move this project forbids.** ⚠ **DECLARED GAP:** the old illustrative anchor ("~50–52 at today's 8–10 point wraps") was itself percentage-denominated and cannot be converted; no fresh real-token anchor is published yet. Best available evidence, NOT yet a ruled constant: a single provisional re-measurement (#59, n=1) put a real wrap at **42,434+ tokens**, against inherited folklore of ~25,000 — **low by ≥1.7×**. #59 itself says this "needs 2–3 more before the line moves." Do not treat 42,434 as settled; do not price a wrap at the old folklore either. |

**200,000 (WORKING) is where the wrap has FINISHED, not where it starts.** Starting the ritual at
200,000 is exactly what spends the reserve; that is #28's and #29's recorded cause (in the
percentage vocabulary live at the time, "60").

**★ THE ESCAPE HATCH, and why it exists.** A ceiling with no declared way past it gets worked around by
quietly under-pricing the job — which would corrupt the only honest number in the stamp. So an overrun
IS allowed, as an explicit, marked, forked act. **The canonical marker, which the gate matches literally:**

```
RESERVE SPEND — forked to Dave
```

Put it in the `pre-flight:` stamp. **Unmarked over-ceiling FAILS the wrap; marked over-ceiling WARNS and
leaves a receipt.** ⚠️ The marker is a receipt, **not an absolution** — a session that marks every wrap
this way has re-dialled the ceiling by habit rather than by ruling.

★ **CLOSED BY DAVE, #34 — the one-point slack is gone.** ds-023 was written `≤ 45`, but 45 reads **AMBER**
(GREEN is `< 45`), so *"must project to finish GREEN"* and *"≤ 45"* disagreed by exactly one point and **both
were in the canon**. #34 shipped the literal `≤` and forked the contradiction rather than silently picking
the stricter reading — *tightening a ratified threshold is not the agent's to do*. **Dave ruled `< 45`: 45
now FAILS**, and "project to finish GREEN" is literally true instead of nearly true. The boundary (44 pass ·
45 fail · 46 fail) is bitten, and the fixture that read *"at the ceiling exactly — allowed"* was **flipped to
FAIL** rather than deleted, so the change stays legible.

★ **RULED BY DAVE, #34 — THE MARKER STAYS STRICT**, knowing the cost. The gate matches
`RESERVE SPEND — forked to Dave` literally, and #33's stamp — *"was REFUSED against the 45 ceiling and forked
to Dave"* — is **correct behaviour that this gate fails**. Loosening it to any prose containing "forked to
Dave" would let the receipt be produced by accident, and **a receipt that can be produced by accident is not
a receipt**. The cost is real and is accepted: a session phrasing it naturally gets failed once and learns
the literal. That is why the string is documented HERE, in the rule, and not only in the regex.

⚠️ **AND A FINDING FROM ENACTMENT (#34):** #33's stamp already recorded the right behaviour in the wrong
words — *"was REFUSED against the 45 ceiling and forked to Dave"* — and does **not** match the canonical
marker. The strict form was kept deliberately (a gate that accepts free prose cannot tell a declared
spend from a passing mention), but this is the *gate-narrows-its-own-rule* class showing up at birth:
**a disciplined session wrote the correct thing and would still have failed.** Hence this box — the
magic string is documented where the rule is, not only in the regex.

★ **THE BOUNDARY STORY ABOVE (44 pass · 45 fail · 46 fail) IS ABOUT THE OLD PERCENTAGE CEILING, NOW
HISTORY.** #56 replaced `45` with `160,000` wholesale (REPLACED, not converted — see ★★ THE UNIT AND
THE BUDGET). What #34 ruled here — strict `<`, no one-point slack, a marker that stays literal — is a
PRINCIPLE, and the principle carried forward intact: `band_for()` still reads the AMBER threshold with
a strict `<` on its GREEN side, bitten by that function's own selftest (`band_for(BUDGET_AMBER - 1)`
must be GREEN, `band_for(BUDGET_AMBER)` must be AMBER). **Do not re-derive a "159,999 / 160,000 /
160,001" boundary story to match this one** — that story was never told in tokens, and inventing one
now would be exactly the false precision this project rules against.

**RULED (b) — spending the reserve is a TRIGGER, and the fork goes to Dave.** On **any unplanned
finding**: stop, re-price out loud, and put the fork to him — **(a)** log it and stop · **(b)** narrow ·
**(c)** chase it knowingly with a Red stamp. **Not a decision the agent makes silently from inside the
sunk cost**, which is exactly how ds-016 got chased for +17.

⚠ **Observed failure of (b) — 2026-07-27 #12, inscribed at the first 2f strata roll (#15):** mid-enactment, C2's first run surfaced three new instances of the silent-lookup class; one was fixed and two written up **without a re-price or a fork** — the rule failing precisely where it exists, on a finding arriving mid-enactment when stopping is most expensive and most necessary. Same window: Dave named the circling (*"im going round in circles"*, ~55%) before the agent did; the unlock was one sentence — *a token value is a one-line reversible edit, not architecture*. **Name the circling, and say the unlock, earlier.** Post-mortem data: `notes/_GAUGE-LOG.md` § 2026-07-27 #12.

**★ THE MECHANISM ALREADY EXISTED; ITS TRIGGER WAS AT THE WRONG TIME.** The fork in Half 0 above was
written before this ruling and is precisely the throttle Dave asked for — it just fired **only** before
starting. Extended, one word: **before starting AND on any unplanned finding.** *(Same class as the
morning's other findings — the right rule, unreachable at the moment it is needed.)*

**★ M1 — RED IS A WRAP-ONLY BAND (RULED Dave, 2026-07-27 evening #17: *"running in red just makes a
godawful mess"*).** Crossing **into RED — past 200,000, the WORKING ceiling** *(said as "60% fill" at
the time this was ruled; restated by #56, REPLACED not converted)* = announce it the moment it
happens and **start no new jobs**: remaining work moves to the handoff/brief and the session wraps.
The only judgment left in Red is how to close cleanly. *(Still self-report — no gate can see fill; what this line changes is
that running-on in Red is now a RULE violation, not a defensible choice. Red-authored artefacts
already carry the re-verify stamp; this rule exists so there are fewer of them.)*

**★ M2 — A RULING ARRIVING MID-RITUAL IS A FINDING (RULED Dave, same window).** Price it or park it
to the queue before absorbing it. The #6/#12 leak was rulings treated as free because each was cheap
singly — cheap × unpriced × several = the overrun. The fork above applies to them unchanged.

**RULED (c) — A NEW SESSION IS A REFILL, NOT A PENALTY** *(Dave, same window: "we can reset the budget
at any time by starting a new session").* This is the clause that makes the throttle cheap to obey.
The fork's option **(b)** — flush and hand to a fresh window — has been written as a last resort; it is
in fact **the normal way more budget is obtained**, and under this ruling it is often the FIRST answer,
not the reluctant one. **Cutting work no longer means losing it.**

⚠ **But a refill is not free — it costs the cold read.** MEASURED 2026-07-27: a fresh session reached
~**22%** fill on `GOOD-MORNING.md` + `_LIVE-STATE.md` + the memory index **before doing any work**
(*n*=1 — treat as an anchor, not a constant, and re-measure when the handoff's size changes). ⚠
**DECLARED GAP (found while fixing this file, 2026-08-02):** this reading predates #56 and is in the
retired percentage unit; it has not been re-measured in real tokens as part of this pass, and is not
converted here — [[measure-dont-convert-units]]. Re-run with `_gauge_tokens.py` at cold start when
the cold-read cost next matters.
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

**Recalled bands were WRONG on 2026-07-27:** the agent reported *"🟡 Amber ~70%"* and then *"Amber
~85%"* — both Red by the table live that day, which had been correct all along. *(Quoted in the
percentage vocabulary live at the time; that table has since been REPLACED by #56's absolute band —
see ★★ THE UNIT AND THE BUDGET, near the top of this file, the SOLE copy.)* The mislabel propagated
into the `GOOD-MORNING` banner, `_LIVE-STATE` and Dave's summary before he caught it. **A false
reading of the very instrument built to catch false inscription**, and it is the same failure class
as [[stale-reading-failure-mode]]: the corpus was right, the recall was not.

⇒ **Quote the band from ★★ THE UNIT AND THE BUDGET, or `grep` it. A band asserted from memory is not
a reading.** *(Not "twelve lines below" — that kind of pointer survives only until the next edit;
this file's own history, fixed in this pass, is the proof.)*
⇒ **State the NUMBER and the BAND together** (`~210,000 → RED`) so a mismatch is visible to Dave in
one glance — he caught this one exactly that way.

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
| — the capture ritual | **+~5% of window (MEASURED 2026-07-27, pre-#56 unit) — ⚠ not yet re-measured in real tokens, DECLARED GAP** |
| — the task list (create + each update; it re-renders) | +0.5–1k per burst |
| — a Half-2 check-in (`_checkin.py`, current mechanism) | **~0 — reads the transcript on disk directly, never loads it into the window** (superseded the old subagent+`read_transcript` approach below, which DID cost window) |
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

### ★ THE FLOOR IS MEASURED, NEVER ASSUMED (GM-D9)

*(Ruled 2026-07-27, `notes/_MEMENTO-DECISIONS.md` § GM growth-contracts. **Dave's reframe, and it is the
whole decision:** the cold-start floor is **a variable this programme shrinks**, so a snapshot constant
written into canon would be **falsified by its own enactment** — the prose-drift class, self-inflicted.)*

⚠ **THE BAND TABLE ITSELF LIVES IN ONE PLACE ONLY — ★★ THE UNIT AND THE BUDGET, near the top of this
file. This section is NOT a second copy** (it used to be, and the two drifted — see ★ RETIRED UNITS
AND BANDS below, where that history now lives). What survives here is the part of GM-D9 that is not
the numbers: two rules that replace every earlier treatment of the floor.

1. **MEASURE the floor at session start — announce the fill after the mandated reads, before pricing
   anything.** Not "the floor is about N": *this* session's floor, this window, stated as a number, in
   real tokens (`python3 knowledge/_gauge_tokens.py`). The floor moves with what you actually read — a
   session that reads `GOOD-MORNING.md` alone does not have the floor of one that reads the whole chain,
   and the two must not be priced the same. ⚠️ **The old band table priced the floor at ZERO** (SD-7) —
   it described fill as though every window started empty. It never did.
2. **Bands are read against REMAINING BUDGET.** What decides a fork is never how full you are, it is
   whether what is left can hold the job *and* its wrap. This is already the arithmetic of the flush rule
   above (*"flush whenever the remaining budget is smaller than the job plus its wrap"*); read remaining
   budget as `200,000 (WORKING) − fill`, in tokens, not as a percentage — the whole reason #56 replaced
   the band was that a percentage needs a denominator nobody inside the session can observe.

**The numbers are Dave's and are re-dialled only by him — quote them from ★★ THE UNIT AND THE BUDGET,
never from here, never from memory.**

### ★★ THE FLOOR IS NOT WILLPOWER — `N` × one unit, and the only lever (HOMED HERE #50)

*(#50 ran a homing probe over `GOOD-MORNING.md`'s `size:` line before cutting it. This conclusion was
found live **NOWHERE** in the repo — the `size:` line was its only copy. Moved here FIRST, then cut:
discharge by ADDITION. It belongs beside the floor because it is the floor's operational consequence.)*

**Measured, four sessions, same direction** *(historical readings, in `tape` — the unit live when they
were measured; see ★ RETIRED UNITS AND BANDS below for what `tape` means. NOT re-denominated: they
record what was measured, in the unit it was measured in — [[measure-dont-convert-units]]):*

| session | what was tried | what it bought |
|---|---|---|
| #38 | retired one VERIFIED-DEAD item | **+16 tape** (a retirement must leave a stub) |
| #44 | last compression cuts | **~5 tape each** |
| #45 | a whole supervised sweep | **net 37 tape** |
| #48 | needed 737 tape | got there **only by refusing to write some of it** |

⇒ **Nothing shrinks a region below `N` × one unit.** A region with `N` items has a floor set by the
cost of one item; compression cannot go under it, and past a point each edit costs more window than
it recovers. **The only lever is WRITING LESS, priced BEFORE the writing** — which is why
pre-flight pricing (Half 0) is the load-bearing half of this gauge and shaving at wrap is not.

★ **Corollary, and it is where the saving actually comes from: the cheapest tokens in any capped
region are a claim that has stopped being true.** Retirement is a BUDGET instrument, not hygiene.

### Behaviour at each band (the rules attached to GREEN / AMBER / RED — numbers live solely in ★★ THE UNIT AND THE BUDGET, above)

- 🟢 **GREEN** — work freely.
- 🟡 **AMBER** — get economical, pre-stage the handoff, confirm before the next big read.
  **PROACTIVELY surface the band to Dave here and offer to start wrapping / capture soon — do NOT
  wait to be asked** (Dave, 2026-07-20: *"I would set it at amber too"*; the agent suggesting
  session-end from the estimate, unprompted, is the whole point — silence while the tally climbs is
  the failure mode). **★ Also fire the light SPINE-FLUSH here** (ruled 2026-07-21 — see trigger
  below): write current state to `_LIVE-STATE.md` now, WITHOUT ending the session. **★ AND DO NOT
  START A NEW BUILD ARTEFACT AT AMBER** — a review sheet, an interactive prototype, a new component.
  They are deceptively token-heavy and are exactly where hot-session "silly mistakes" land
  (2026-07-24: two review sheets/prototypes built *past* Amber → a render bug + Dave calling the
  handover, *"we're obviously hot, there are silly mistakes"*). Design/decision **writing +
  inscription** is fine hot; a new **interactive build** is not — flush and hand the BUILD to a
  fresh window.
- 🔴 **RED** — ⛔ **REACHING RED IS ALREADY THE OVERRUN, NOT THE CUE.** The ritual should have
  STARTED at the **in-flight stop line = `200,000 (WORKING) − the priced wrap`** (§ ds-023 above;
  the old illustrative anchor was percentage-denominated and could not be converted — a fresh
  real-token anchor is a declared gap there). **200,000 is where the wrap has FINISHED, not where it
  starts.** If you are reading RED and have not begun the wrap, you are spending the reserve — wrap
  immediately and mark it `RESERVE SPEND — forked to Dave`.

**The tally is a protocol, not a stop signal** (routing audit #11, ratified Dave 2026-07-23):
below Amber, work at full quality with no economising — the bands change behaviour only at their
thresholds. This line exists because a surfaced token count is a documented trigger for premature
wrap-up in Fable-class models (the primary source's own remedy is exactly this reassurance); the
gauge's numbers stay BY DESIGN — deliberate wrap at threshold is the mechanism, not the failure mode.

### ⬛ RETIRED UNITS AND BANDS — HISTORY, NOT INSTRUCTION

**Both systems below were LIVE canon for many sessions and are now SUPERSEDED. This section exists so
Dave's rulings are not lost — it is not a second place to read current numbers from. The current, sole
authority for the band and the unit is ★★ THE UNIT AND THE BUDGET, near the top of this file (RULED BY
DAVE #56).** A reader who lands here from a search or an old link: you want that section, not this one.

#### The `tape`/`bill` two-unit system (ds-021, ruled #31 delegated, CONFIRMED + named by Dave #34 — SUPERSEDED #56)

*(Retired because #56 changed what could be measured, not because the reasoning below was wrong —
`tape` and `bill` were a real, careful fix to a real problem, and the mnemonic held for many
sessions. Preserved in full for that reason.)*

There were two units and they differed by about half as much again:

| unit | what it is | who read it |
|---|---|---|
| **`tape`** | what `tiktoken cl100k_base` counts | the gate, when it measured a file |
| **`bill`** | what the window actually **charged** | you, when you ran out of room |

★ **THE MNEMONIC WAS THE RULE: the tape is not the bill.** A tape measure tells you the size; the bill
tells you the cost. Written out: *"the chain is 3,487 tape / ~5,405 bill."*

**Why it was worth a ruling.** Every cap in `_capture_gate.py` was denominated in `tape` while the
window charged in `bill`. Measured #30, two files, one session — `GOOD-MORNING.md` 16,107 tape →
25,355 bill (1.57×) and `_LIVE-STATE.md` 18,818 tape → 29,103 bill (1.55×). So a gate reporting
*"99.2% of block"* was describing a file that actually cost half as much again, and the reported
floors for #27/#28/#29 understated true fill by **~10 points**. ⚠️ The gate was never wrong — it was
precise in the wrong unit, which is exactly why five sessions of careful measurement never caught it.
Same class as *a count is not a measurement*: a proxy measured well, then reported as the quantity.

**What bound, while this was live.** Caps bound on **`bill`**. They were RESTATED at their current
real value, not silently tightened — `_capture_gate.py` converted the ruled `tape` caps through the
ratio, so the comparison stayed arithmetically identical to the old one *by design*.

⚠️ **THE RATIO WAS ALWAYS PROVISIONAL.** n=2, one session, two files. `TAPE_TO_BILL = 1.57` was **GM's
own pair**, deliberately not the 1.55 average — every cap it converted was GM-derived, and the average
would have quietly loosened a GM cap. Standing practice (ds-021 (c)) logged one `tape`/`bill` pair per
wrap into `notes/_GAUGE-LOG.md`, with a rule that at n≥4 the constant would go to Dave to rule formally.

**What actually retired it.** Session #82 wired a REAL Claude-token counter (`_gauge_tokens.count()`,
returning `(n, 'real')`) as a tier ABOVE both `tape` and the `tape→bill` ratio. Once the real cost is
directly measurable, a ratio estimating it from a proxy has nothing left to do — real tokens are not
"tape, converted"; they are a different, direct measurement. **⚠ DO NOT convert a surviving `tape`
figure to `bill` or to "real" using `1.57` or `1.55`.** If you need a real-token figure, measure it
(`python3 knowledge/_gauge_tokens.py`); if you cannot, declare the gap. [[measure-dont-convert-units]]

**Transitional debris, for anyone auditing old commits:** the legacy spelling `tk` used to parse in a
`size:` stamp with a WARN. `_capture_gate.py` is the current authority on whether any of that parsing
still exists in the live gate — this runbook no longer teaches the `tk`/`tape`/`bill` vocabulary as
something a session should produce.

#### The percentage fill-band — GREEN `<45%` / AMBER `45–60%` / RED `≥60%` (Dave, #30/#31/#34; "one-point slack" tightened #34; Amber floor moved 50→45 on 2026-07-25; SUPERSEDED #56)

*(This is the band ds-023, M1, the trigger section and the authoring-time stamp all originally pointed
at. Their operative text now reads the #56 table; this is the record of what they used to read, kept
because the boundary-tightening story is a real ruling, not filler.)*

Bands were read as a fraction of the ~200k window:

- 🟢 **GREEN <45%** (<~90k) — work freely.
- 🟡 **AMBER 45–60%** (~90–120k) — get economical, pre-stage the handoff.
- 🔴 **RED ≥60%** (≥~120k) — the ritual should already be running.

*(Bands recalibrated by Dave 2026-07-25: Amber floor moved 50→45; earlier the runbook read Amber
50–60. The move-by point was unchanged at 60.)*

★ **The "one-point slack" ruling (#34) is preserved in full, inline, at ds-023 above** — a
boundary-strictness ruling (`<45` not `≤45`) whose PRINCIPLE carried forward into the current band
(`band_for()` still reads its threshold with a strict `<`) even though the NUMBER did not. Read it
there, in context, rather than as an orphaned fragment here.

**What replaced it, and why "replaced" is the word.** #56, Dave: *"the band was REPLACED, not
CONVERTED."* `45/60/63` were percentages of a window whose harness component is unobservable from
inside a session, so the percentage itself could never be honestly computed — see ★★ THE UNIT AND THE
BUDGET for the full argument and the current numbers (160,000 / 200,000 / 256,000, in real tokens).

### Half 2 — accurate, out-of-band: confirm at Amber

**The instrument is `knowledge/_checkin.py` (RULED #52, built #52/#53) — run it in one bash call:**

    python3 knowledge/_checkin.py

It reads the live session `.jsonl` from the mount directly — never loading the transcript into the
window — and reports the conversation-half in `tape` with the boot half printed as UNMEASURED
(`ds-025` item 1), never defaulted. Its number is **THROUGHPUT, not resident fill** — say so when
quoting it. No subagent, no `read_transcript`, no copy-ready prompt.

⚠ **THIS `tape` IS NOT THE RETIRED ds-021 DUALITY** (★ RETIRED UNITS AND BANDS, above) — `_checkin.py`
never claimed a `tape→bill` ratio or used tape as a cost proxy; it labels its own reading an
unverified cl100k estimate of THROUGHPUT and stops there. Nothing here needs the ratio, and nothing
here was retired by #56 or #54 — this note exists only so the word `tape`, meaning two different
things at two different scopes in one file, does not read as a third contradiction. Verified current
2026-08-02 by reading `_checkin.py`'s source directly: it still measures cl100k and labels it so.

> ⚠ **HISTORY — the ORIGINAL Half-2 design (subagent + `read_transcript` + `_context_gauge.py`) is
> RETIRED, not "currently broken" (corrected #74; the stale warning sat here from #3 while the
> replacement landed at #52).** Its two observed failure modes, kept for provenance: (1)
> `read_transcript` renders tool calls as one-line stubs with RESULTS STRIPPED — **re-probed #74,
> still true**, quoted receipt: `[assistant] (called mcp__workspace__bash)`, no result payload — so
> it under-reads catastrophically and CANNOT be fixed from our side; (2) the live session was hard
> to identify untitled — **materially reduced since the title ritual** (#71–#73 all carry titles in
> `list_sessions`), but moot: `_checkin.py` needs no session picking. `_context_gauge.py` itself
> remains for measuring an arbitrary text file (since #74 it REFUSES without tiktoken unless
> `--estimate` labels the output). **Half 1 (the in-head tally) still governs between check-ins;
> a reading that disagrees with the tally by >2× is a prompt to check units (throughput vs fill),
> not reassurance.**

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
- 🔴 **THE STOP LINE (`200,000 (WORKING) − priced wrap`, NOT 200,000) → the FULL trigger + fresh
  session** (below). Everything the Amber flush already saved makes this handoff faster and safer to
  author. ⛔ **THE TIER IS NAMED FOR WHERE THE WRAP ENDS, NOT WHERE IT BEGINS.** Firing at a reading
  of 200,000 puts the whole wrap price ON TOP of the WORKING ceiling — which is #28's and #29's
  recorded cause *(in the pre-#56 vocabulary, "60")*, and it is the single most-repeated misreading of
  this runbook. **Compute the stop line from your priced wrap and fire THERE.** An expensive wrap must
  stop the session earlier; the line moves, it is not a constant.

## The Red trigger — wired to the existing ritual

⚠ **"At Red" BELOW MEANS AT THE STOP LINE — `200,000 (WORKING) − the priced wrap` — NOT at a gauge
reading of 200,000.** Stated here because this section was, for eleven sessions, the half of the
runbook agents actually landed on: it said *"at Red, fire the ritual"* while § ds-023 three hundred
lines up said *"60 is where the wrap has FINISHED"*. **The file contradicted itself, and which rule a
session got depended on which line it hit.** Reconciled #54 on Dave's correction — *"the 60% is the
total with the wrap included, it was never supposed to be 60 plus wrap."* ★ **Not a re-dial by #54:**
ds-023's numbers stayed his THROUGH that reconciliation. They were later **replaced wholesale**, on a
separate, later ruling — #56's absolute band (160,000 / 200,000 / 256,000, real tokens) — a different
kind of event to #54's fix, documented at ★★ THE UNIT AND THE BUDGET, above.

At the **stop line** (confirmed, or high-confidence tally), the agent says, as a ready-to-use line:

> **Title this chat: `<retrospective title>` — context is Red (~NN,NNN of 200,000). Running the
> capture ritual, then open a fresh session with: `<forward title>`.**

That phrasing chains straight into two standing conventions so nothing extra has to be remembered:
- `session-title-convention` — every session opens with "Title this chat: …".
- `_RUNBOOK-capture-ritual.md` — the Red line **is** the cue to run steps 1→5 before the window fills,
  so the handoff is authored while there's still budget to author it well (never scramble it at the
  hard line).

## Why this ordering matters

The failure mode is a handoff written *after* quality has already degraded — a confidently wrong
`GOOD-MORNING.md` is worse than none (`memento-framing`). ⚠ **This paragraph read "Triggering at 70%,
not 95%" for an unknown number of sessions — a THIRD pair of numbers, matching neither the ratified
45/60/63 band nor #56's 160,000/200,000/256,000 replacement.** No ruling for 70/95 was found while
fixing this file (2026-08-02); treated as drift, not a citation, and corrected to the ratified line:
triggering at the **stop line** (`200,000 (WORKING) − priced wrap`), well short of the **hard line**
(256,000), keeps enough clean context to do the capture ritual properly. The gauge exists to protect
the ritual, not to squeeze the last token out of a session.

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
- One line: `Context gauge at authoring: 🟢/🟡/🔴 BAND ~NN,NNN of 200,000 (in-head tally, ESTIMATE
  ±15% — or Half-2 confirmed via _checkin.py).` *(Format restated in real tokens, #56. "Half-2
  broken" was corrected #74 — Half 2 has run on `_checkin.py` since #52/#53; carrying "broken"
  forward here after that fix would have been the same class of stale claim this whole file was
  full of.)* This already appears informally as "wrapped Red / ~Amber" in the ★ banner; the rule
  formalises it as a REQUIRED field and extends it to receipts.

**Live proof — the session that added this rule (2026-07-24):** the prior conductor wrapped *deep Red*
and left a real showroom-sync gap — the committed tree failed `_build_all.py` while the spine claimed
"53/53 green." The follow-up conductor, authoring in Green, re-ran the build, caught it, and fixed it
(`eb9c9ec`). Had the Red wrap carried this stamp, it would have told that reader to scrutinise the
commit *before* trusting the "green" claim — which is the whole point.

## Entry points

`_RUNBOOK-capture-ritual.md` (where Red sends us) · `knowledge/_gauge_tokens.py` (the budget/band
engine, real tokens, #56) · `knowledge/_checkin.py` (Half-2 throughput check-in, `tape`/cl100k,
#52/#53) · `knowledge/_context_gauge.py` (measures an arbitrary text file; refuses without tiktoken
unless `--estimate`, #74) · memory `feedback-context-gauge` · `session-title-convention` ·
`memento-framing`.
