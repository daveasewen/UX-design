# The gauge becomes a throttle — and the ruling was invisible to the handoff that should have carried it

provenance: apollo-sds-2026-07-27-5 · 2026-07-27
status: ruled · knowledge/_RUNBOOK-context-gauge.md § ★ Half 0b

*Session #5, Monday 2026-07-27, Opus 5 solo self-conducting, effort MAX. Dave ruled four calls in one
window. The session's own subject was how much work a window can hold, so it is the first one that
could be graded by its own rule.*

---

## 1. The session opened by picking the wrong task, twice

The handoff's § DO THIS FIRST carried a ★★★ block labelled **NEW AND UNRULED — ds-016**, so ds-016 was
ranked as the task. Dave: *"read the 'do first' in the good morning it should have a new task."* Then,
when that produced the same answer: *"should be teh pre-flight work, is that correct?"*

It was not correct **by the handoff**, and that is the finding. The real item was in `_FUTURE-STATE.md`:
**★★ FLOATED 2026-07-27 (#4 wrap) — "the gauge must be a THROTTLE, not a thermometer"**, carrying Dave's
words (*"the pre-flighting needs work, we cant keep hitting red, its a waste of effort"*) **and its own
sequencing instruction**: *"~10 minutes at the FRONT of the next window; it does not displace ds-016 /
the `CTRL` sweep, it precedes them."*

**The handoff not only failed to carry it — it handed forward the superseded posture.** DO FIRST's
pre-flight paragraph restated the **three-term rule**, which the same session's wrap had already
concluded *did not work*. A Polaroid presenting a known-insufficient rule as live guidance.

⇒ Logged as **`ds-017`**. Same signature as the silent-lookup class (ds-010 · ds-013 · ds-015 · ds-016):
record correct, retrieval path absent, nothing reports the gap. The 2c/2d EXIT CHECK carries §C·4 items
*up*; it has no clause for the inverse — a FLOATED item that **supersedes a standing instruction**.

## 2. What was ruled

Dave ruled cold, exactly as the floated entry asked (it was authored at ~97% fill and deliberately kept
out of canon on the grounds that *a rule about not working past your budget must not itself be inscribed
past budget*).

- **(a) The reserve is RING-FENCED, ~15%** — a budget you may not spend without asking, **not** a fourth
  addend. *The correction to the floated shape:* an additive term is absorbed by an optimistic plan and
  becomes padding; only a fence can trigger anything.
- **(b) Spending it triggers a re-price, and the fork goes to Dave** — log-and-stop / narrow / chase
  knowingly. Not a decision the agent makes silently from inside the sunk cost, *which is exactly how
  ds-016 got chased for +17 the previous session.*
- **(c) A new session is a REFILL, not a penalty** — *"we can reset the budget at any time by starting a
  new session."* The fork's option (b) had been written as a last resort; it is the normal way budget is
  obtained.
- **Every job is priced and debited**, stated out loud when it could move the band — *"like real life."*
  **The ~10% floor is removed:** every overrun on record arrived as steps each individually under it,
  which is how a floor fails.

**★ The finding that made it cheap: the throttle already existed and its trigger was at the wrong time.**
Half 0's fork — *projects into Red? say so and offer (a)(b)(c), Dave chooses* — is precisely what Dave
was asking for. It fired **only before starting**, so a finding landing mid-job could never reach it.
The fix is one clause: **before starting AND on any unplanned finding.** *(Third instance this week of
"the right rule, unreachable at the moment it is needed".)*

## 3. Dave's two refinements, which beat the version being written

1. *"the individual budgets stay the same but we can always pull from a larger 'bank' of tokens by
   moving to a new window."* ⇒ **The window is the BUDGET; the bank is the constraint** — and **the cold
   read is a transaction fee** on every withdrawal (MEASURED this session: ~22% to reach working state
   on `GOOD-MORNING` + `_LIVE-STATE` + memory index, *n*=1). A fresh window buys ~78%, not 100%.
2. The plan-usage panel, and *"the overall weekly budget, which we need to max-out or loose."*
   ⇒ **A THIRD TIER, and it inverts the objective.** MEASURED 2026-07-27 12:07 (Max 20×): week **51%
   elapsed, 33% consumed = 0.65× pro-rata**; **Fable 28% = 0.55×**, the most under-used line. 83h and
   67% of allowance left ⇒ **1.36× pro-rata needed** merely to avoid losing it.

   **This forced a same-window reversal.** The section had just been written to say *"minimising Reds and
   minimising flushes are the same objective — fewer tokens spent against the bank for the same work."*
   Under a perishable allowance that is **wrong**: under-spending converts allowance into nothing, exactly
   as a Red session does. Both wordings are in the runbook, the old one quoted — per the standing rule
   that a reversal is inscribed as loudly as the claim, so it can never read as agent drift.

   ⇒ **Behind pace ⇒ MORE WINDOWS, not longer ones.** Red is still the failure; hoarding is now also one.
   And: **rationing a model against its own separately-metered, separately-perishable line is not
   discipline, it is waste** — which puts the Fable-shaped ruling batch on the critical path.

## 4. What was built, and the honest limit of it

`_capture_gate.py --wrap` now checks the **FORM** of the handoff's `pre-flight:` stamp: three terms
present (the wrap is the historically omitted one), arithmetic that closes, and the named band matched
against the band table. **7 bites + 2 green controls**, including both band boundaries (44/45, 59/60);
**the bite was proven able to fail** by neutering the band check in a copy and confirming the selftest
goes red. Verified end-to-end against the real handoff, not only fixtures.

**⚠ The gate proves the STAMP, not the RULE.** A well-formed stamp carrying invented numbers passes.
Whether the fill figure is honest, and whether a mid-job re-price actually happened, are **not
observable** — declared unenforced in the module header, the runbook and the gate's own output. By
ADR-0016's vocabulary the *form check* is PROVEN and *the rule* is UNPROVEN, and the gap between them is
the "dangerous middle". Flagged at inscription rather than discovered later.

## 5. Concerns the author is recording against his own work

*(Dave, this session: "you are super clever, but agreeable… I must insist you should flag concerns.")*
Fair, and two of these should have been raised without being asked for.

1. **The 15% is weaker than the shape it sits in** (~40% confidence in the number, ~85% in ring-fencing).
   *n*=3, one unknown, keyed off a single unusual event. A tail observation doing a distribution's job.
   ⇒ Marked provisional in canon; record each session's actual overrun so it can be re-derived.
2. **"Unspent allowance is LOST" went into a canon table as fact for twenty minutes.** It is `inferred`
   (~75%) — from a percentage bar and Dave's reading of it. Not verified: what the percentage meters,
   whether Fable draws the same pool, whether anything rolls over. ⇒ Provenance note added.
3. **"1.36× pro-rata needed" is a number that looks like a target, and targets get hit.** The same
   mechanism criticised one paragraph earlier (a reserve becoming an allowance) is reproduced here if
   pace is ever read as a quota. **Spending allowance on low-value work is not a win, it is spending.**
4. **The Fable recommendation had a bias in it** — the ruling batch was recommended partly *because* the
   Fable line is under-used. It survives on merit (15 items, unmoved for days, gating §C·1(c)
   templates+shells), but the reasoning was allowance-led and is named as such.

## 6. Resolved state / still open

**Resolved:** the throttle is canon (`_RUNBOOK-context-gauge.md` § ★ Half 0b) · the FORM check is built,
bitten and wired into `--wrap` · `_FUTURE-STATE`'s floated entry retired to RULED with its diagnosis kept
verbatim · `ds-017` logged with three unruled remedies.

**Open:** ds-017's remedy (a/b/c — Dave's) · the 15% re-derivation · ds-016 and the `CTRL` sweep, both
untouched today and both still ruled-and-waiting · the ruling batch (15), now the recommended next
window.

**Links:** `knowledge/_RUNBOOK-context-gauge.md` § ★ Half 0b · `_FUTURE-STATE.md` § the throttle ·
`knowledge/_DS-IMPROVEMENTS.md` § ds-017 · `knowledge/_capture_gate.py` ·
`_DECISION-HISTORY/2026-07-27-the-index-cannot-see-the-rule.md` (the session that produced the +17).
