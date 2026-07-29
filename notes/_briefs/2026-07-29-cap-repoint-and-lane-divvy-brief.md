# Brief — the compactable cap is mis-pointed, and the lane divvy that follows

```
provenance: local_0e7e56cf-3e2d-4190-a103-cf753cd95409 · 2026-07-29
status: observed
```

*Written at #38's close, on Dave's ruling: **"we need to run subagents to get this fixed quickly, we
are going round in circles again because we dont have the context budget to do the jobs."** He is
right about the circles. #38 found the cause and it is not job size — it is a cap aimed at a cost
that stopped existing five sessions ago. Both halves are below: **the finding**, then **the divvy**.
Written so the fresh window does not pay to re-derive any of it.*

---

## 1. THE FINDING — measured at #38, and it reframes the whole problem

**`SIZE_BUDGET_TK = {"compactable": 8000}`** (warn) / **12,000** (block) lives in
`knowledge/_capture_gate.py` ~line 275. **Its own comment, dated 2026-07-27, states the purpose:**

> *"the whole-file figure is ALWAYS published beside it so **true cold-start cost** is never hidden
> by the exclusion."*

**The cap was sizing what a cold session pays at boot.** That was correct on 2026-07-27.

**Then #33 (2026-07-28) CUT the read chain.** A cold session now reads three things — GM header →
★ LATEST banner → the ⏱ LATEST delta of `_LIVE-STATE.md`. **Measured at #38's wrap: 4,400 tape.**

⇒ **Of the 11,955 tape the cap governs, only ~2,924 is in the chain. Roughly 9,000 tape is never
paid at cold start at all** — DO-FIRST, §C·1, §C·2, §C·4 and the strata are reached by
`_memento_search.py`, not by reading. **The cap is charging boot prices for a retrieval-only queue.**

**This is why every wrap grinds.** The only way to satisfy a cap pointed at the wrong region is to
shave live queue: **#35 did six trimming rounds, #38 did three** (12,784 → 11,955), and both were
cutting their own session record to fit a number that no longer describes anything a session pays.

★ **Same shape as #35's own finding, one layer up:** *the job was aimed at a cost the previous
session had already eliminated.* An instrument's READING ages faster than its RULE — and here the
reading is the cap's own referent.

### What is NOT claimed

- **Not** that GM should grow without limit. It should have a contract; the question is *which
  region, against which cost*.
- **Not** that the number 12,000 is wrong. It may be exactly right for the chain. **Untested.**
- **Not** that this is the agent's to change. ⬛ **The SHAPE (`budget applies to the compactable
  region`) is Dave's D8(a) ruling; the NUMBER was agent-recommended.** Re-pointing it is a **RULING**,
  and ds-023 — where a delegated agent's pick became an enforcement Dave never made — is the standing
  cautionary case. **The conductor puts the fork; Dave rules. No lane touches this.**

### The likely shape of the answer, offered as a starting point ONLY

The chain already has its own gate (**M10**, `read_chain_tk`, warn 4,500 / block-candidate 6,000,
**ADVISORY and agent-derived, also awaiting Dave**). If the chain is what a cold start pays, then
**M10 is the real cold-start budget and should be the binding one**, while the compactable region
needs a different, looser contract answering a different question: *how big may the retrieval surface
get before retrieval itself degrades?* ⚠ **Two agent-derived advisory numbers cannot be promoted by
an agent noticing they should be.** That is the whole fork.

---

## 2. THE DIVVY PLAN — lanes · model · serial set · shared files

**Dave's rule, better than the runbook's (#36):** ★ **"a sub-agent may do the working, never the
judging."** Every lane below is measurement, assembly or transcription. **Every judgment is the
conductor's, and every ruling is Dave's.**

⚠ **The overhead is real and was measured at #36: 4–6 pts per lane, plus the hand-back reconcile.**
Lanes earn their keep here only because each one is genuinely parallel and none needs the others'
output. **If the conductor finds itself waiting on a lane, the divvy was wrong.**

⚠⚠ **EACH LANE PAYS ITS OWN COLD READ — that is the fee this brief exists to minimise.** Every lane
below carries a **READ EXACTLY THIS** list. **A lane that reads `GOOD-MORNING.md` top-to-bottom has
already spent its budget and defeated the point.**

### Lane A — MEASURE THE REGIONS (Sonnet)

**Job:** produce the evidence table the cap decision needs. **Pure measurement, zero judgment.**

- For each GM region (`HDR LATEST PRIOR DOFIRST A C1 C2 C4 STRATA`) and each LS region: **tape now**,
  and **which are in the read chain vs retrieval-only**.
- **Growth per region per session** across the `section-sizes` series already in `notes/_GAUGE-LOG.md`
  and the GM strata — the dataset exists and has never been read as a series for SIZE (only usage was,
  at #35).
- **What a cold start ACTUALLY costs today**, itemised: chain + `MEMORY.md` + the skills descriptions.
  ⚠ **The harness half is UNREACHABLE from any mount (`ds-025`) — report it as UNKNOWN, never estimate.**

**READ EXACTLY THIS:** `knowledge/_gm_usage.py` (docstring + `--sizes`/`--history`) ·
`notes/_GAUGE-LOG.md` (the `section-sizes` lines only) · `knowledge/_capture_gate.py` §
`SIZE_BUDGET_TK` + `read_chain_tk`. **Do not read GM or LS prose.**
**Output:** `notes/_receipts/2026-07-29-lane-a-region-measurement.md`. **Numbers and provenance only —
no recommendation.** ⚠ `pip install tiktoken --break-system-packages` FIRST; the gate silently
estimates without it and under-reports by ~414 tape.

### Lane B — ASSEMBLE DAVE'S SIX OPENS FOR RULING (Sonnet, or Opus if it stalls)

**Job:** for each of the six opens in GM §C·4, assemble **what Dave needs in order to rule** — his
own verbatim words where they exist, what has changed since, and what each option would cost.
**ASSEMBLING, NOT DECIDING. A lane that arrives at a recommendation has exceeded its brief.**

The six: **(1)** what happens above 63 · **(2)** `ds-025`'s remedy (a)/(b)/(c) · **(3)** the read
chain's SCOPE · **(4)** the #35 LS offloads + `LS:LIFECYCLE` de-materialise + the deferred register ·
**(5)** the FLOATED degradation note · **(6)** the mid-flight-handover state the gauge log lacks.

**READ EXACTLY THIS:** `GOOD-MORNING.md` §C·4 § ⬛ DAVE'S SIX OPENS (fetch it, don't scroll to it) ·
`knowledge/_DS-IMPROVEMENTS.md` ds-023 + ds-025 · `notes/_MEMENTO-DECISIONS.md` § ★ #35 / #36 / #38.
⚠ **`_DS-IMPROVEMENTS.md` IS NOT REACHABLE BY RETRIEVAL** (GM §C·4 ⚠ RETRIEVAL GAP #2) — open it by
path; a search will return nothing and that absence is a known defect, not an answer.
**Output:** `notes/_receipts/2026-07-29-lane-b-six-opens-assembled.md`, one section per open.

### Lane C — WRITE THE #37 DOSSIER (Sonnet)

**Job:** ritual step 1b for #37, owed since its flush. **Transcription of an arc that already exists,
not reconstruction.**

**READ EXACTLY THIS, AND NOTHING ELSE:** `git log -4 --format="%h%n%B" 3488332..aa8f66b`. ⚠ **The four
commit messages ARE the record.** #37 flushed without a dossier, so its reasoning survives only there
and in state lines. **Do not reconstruct it from `_LIVE-STATE.md` deltas — they are state lines and
will give you the WHAT without the WHY, which is the one thing a dossier is for.**
**Output:** `_DECISION-HISTORY/2026-07-29-the-boot-measured-and-the-auditors-frozen-clock.md`, obeying
`_DECISION-HISTORY/README.md` (lands whole · dated from `date` · `provenance:`/`status:` fields ·
both-way links). ⚠ **`status: observed`, never `ruled`** — #37 ruled nothing.

### Conductor — Opus. SERIAL SET, no lane touches any of these:

`GOOD-MORNING.md` · `_LIVE-STATE.md` · `_GM-ARCHIVE.md` · `_LIVE-STATE-ARCHIVE.md` ·
`notes/_GAUGE-LOG.md` · `notes/_MEMENTO-DECISIONS.md` · `knowledge/_capture_gate.py` ·
`knowledge/_memento-index.json` · **git — ONE commit, explicit paths, never `git add -A`.**

**Conductor's own job, and it is the judging:** put the **cap fork** to Dave with Lane A's numbers ·
inscribe whatever he rules · reconcile three receipts · run the wrap. ⚠ **Collect the hand-backs —
#37 left a worker's receipt uncollected because it read the files as "not my paths"; the conductor
reconciles and commits, workers hand back and stop.**

---

## 3. STANDING CONDITIONS — Dave's, at #38

⬛ **THE FLOATED NOTE MUST BE RETURNED TO.** `notes/2026-07-29-context-degradation-research.md`
(339 lines, `status: floated`, a worker lane's research). Dave, #38, deferring it: **"but we must
return to it when we get this fixed."** ⚠ **This is a FIRM condition on the cap work, not a nicety** —
it is research into this exact problem and has now been unread across three sessions while two of them
re-derived findings it may already contain. **Lane B surfaces it; adjudicating it is Dave's.**
⚠ **A floated item is not authority — surface the contradiction, never auto-promote.**

⚠ **CHECK THE PACE PANEL AT THE OPENER.** No gate can see it, the allowance is perishable, and it sets
the posture: **behind pace ⇒ MORE WINDOWS, not longer ones** — which is the correct answer to *"we
don't have the context budget"* far more often than lanes are. Last reading (#37): all models 70%,
Fable 82%, resets Thu 22:59.

⚠ **GM HAS ZERO HEADROOM until the cap is re-pointed.** Anything added to GM must DISPLACE. If the
conductor finds itself trimming live queue to fit, **that IS the bug this brief describes — stop and
put the fork, do not shave.**

## Entry points

`knowledge/_RUNBOOK-parallel-conductor.md` (worker/conductor checklists, receipts, guardrails) ·
`knowledge/_RUNBOOK-context-gauge.md` § ★ Half 0b (the throttle + the fork) ·
`knowledge/_capture_gate.py` § `SIZE_BUDGET_TK` / `read_chain_tk` · `GOOD-MORNING.md` §C·4 ·
`notes/_MEMENTO-DECISIONS.md` § ★ #38.
