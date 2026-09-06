# #250 — the adversary moves to the brief, and a byte cap gets an honest unit

provenance: 250 · 2026-09-06
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #250 · banner: `GOOD-MORNING.md` ★ LATEST #250 ·
ruling: `knowledge/_rulings.json` § `s250-D1` · working shape: `MODEL-ROUTING.md` rule 7 ·
lane reports: `notes/_subreports/2026-09-06-250-PROBE-byte-gate.md` ·
`…-250-E-byte-gate-unit.md` · `…-250-V-byte-gate-verifier.md` (+ `…-V-byte-gate.challenges.jsonl`
and `notes/_subreports/assets/2026-09-06-250-V-byte-gate-verifier/`) · wrap report:
`notes/_subreports/2026-09-06-250-wrap.md`.*

*The ledgers hold the WHAT. This file holds the WHY and HOW — including the parts that went
wrong, which is the half a ledger line cannot carry.*

---

## 1. The day opened on the quota panel, not on the queue

`#249` closed with a fork sitting on Dave's desk — the ADR-0015 byte gate had gone red under the
FIT build and the four options were his. That is what #250 was titled for. It is not what set the
day's shape.

Dave opened with *"fable is racing ahead"* and a reading: Fable **51%** of its weekly line against
**27%** for all models. Then the instruction: *"lets start rinsing opus 5 subs on max and keep you
for sound judgment, i need fable until thursday at 8ish"*.

**Why this mattered more than the queue.** The gauge's third tier says the weekly allowance is
perishable and the objective is work-per-week, not tokens-saved. But the tiers are metered
*separately*, and the panel showed the Fable line burning at roughly twice the rate of the pooled
one with a hard need for Fable through Thursday. ⇒ the binding constraint for the day was not the
window and not the pooled quota: **it was the Fable bucket specifically.** That makes the routing
question arithmetic rather than taste — every lane that Fable does not have to run is Fable line
saved for the judgment Dave actually needs it for.

So: every lane an Opus 5 sub, Fable kept for brief, judge, read-back and wrap. Three lanes ran and
**zero Fable lanes ran** — the routing was enacted, not merely agreed, which is the part worth
recording, because the failure mode here is agreeing to a routing rule and then quietly running
the convenient model.

## 2. A mistake made early, named by the person who made it

Before any lane went out, the conductor fetched three Fable 5.1 documentation URLs **in-conductor**
— roughly **35,000 real tokens of FILL** — and the findings reduced to *API knobs*, plus two loop
behaviours worth a single line each in a brief (one tool call per turn; whole-file rewrites).

**Why it is written down.** This is precisely the class `_RUNBOOK-context-gauge.md` already homes
from #239, where a CI read-back cost ≈55,692 real for one verdict and one blocker name: the route
is what costs, not the answer. A documentation read is a *lane's* job. The conductor named it in
the wrap brief rather than letting the wrap discover it, which is the behaviour the record is
supposed to reward — a declared gap passes, a silent one fails — but the money was still spent.
It moves no constant; it is a second datapoint under a clause that already exists.

## 3. The adversary was asked for, and then argued with

Dave: *"maybe we use the adversarial PM tactic we used before"*.

The obvious move is to build an output verifier: a second model reads the lane's report and
attacks it. The conductor retrieved the prior shapes (`s204-D1`, `s215-D3`, rule 5) and then did
the thing that is easy to skip — **tested the proposal against our own failure record**:

- **#244** — a lane was briefed on a wrong premise about `derived`, and correctly built 0 of 4.
- **#238** — a polarity gate was built clean, and then falsified.
- **#202** — a vocabulary collision, with every assertion green.

**An output verifier catches none of these.** In #244 the lane's output was *correct* given its
brief; a verifier reading the output would ratify it. In #238 the build was internally sound. In
#202 the instruments agreed with each other and disagreed with reality. All three failed at the
**premise**, upstream of anything an output check can see.

⇒ the adversary moves to the **BRIEF**: a premise probe runs before a canon build, a verifier is
kept only for lanes that touch canon, and coherence between lanes is carried by naming ruling ids
in the brief plus a `CITES:` line. Dave: *"go for it"* — but preceded by *"i might be wrong dont
follow me blindly"*.

**Why rule 7 has no `s250-*` id, and why that was deliberate.** Those two sentences are not a
ruling; they are permission to try. Inscribing them as a ruling would convert Dave's hedge into
his law, and the id is the one thing a later session cannot argue with. So `MODEL-ROUTING.md`
rule 7 landed as **one line, by addition, a WORKING SHAPE**, and the fact that it is not a ruling
is stated in the brief, in the banner, in the spine and here. Confirm-or-retire is his.

## 4. The probe killed the brief's own recommendation, on day one

Dave came back to the byte fork with: *"do you have a recommendation, i like cheap completeness,
would that be c?"* — option (c) being *shave ≥3.7 KB of comments out of the three dataviz sources*.

Under the old shape, the honest answer would have been "yes, probably" and a builder would have
gone out to do it. Under rule 7, a probe lane went out first. It came back with five findings, and
the first one is the whole argument for the rule:

- **(c) does not clear both caps.** The shave gets `dv-behaviour.js` to **16,068**, under
  `MAX_BYTES` 16,384 — and leaves the page at **36,710** against `PAGE_BYTES` 34,816. **Short by
  1,894 bytes.** The premise was false, and it was false by a margin no amount of care in the
  builder would have recovered.
- **(b) was un-writable.** There is no waiver form in the gate at all. The option existed in the
  brief and nowhere in the code.
- **The #96 re-dial never finished.** The gate was still *printing* "32 KB" while `PAGE_BYTES` had
  been 34,816 since #96 — an artefact that had been lying to every reader for a session count
  nobody had counted.
- **`check_group` ignored `consumes`.** It summed every source for every member, so only
  Chart-donut — which genuinely loads all three — was being priced correctly at 40,410; the other
  fourteen were being charged for partials they never load.
- **`knowledge/_rulings.json` carried no byte-cap ruling at all.** `#96-D5` lives at
  `notes/_MEMENTO-DECISIONS.md:3874`, in a ledger. The store the wrap reads back from had nothing
  to read back.

★ **The fourth finding is what turned the fork.** Once you know the page sum was over-counting by
construction, "the cap is too small" stops being obviously true. The cap was not the problem; the
*unit* was.

## 5. Option (e), and why a fifth option was legitimate to offer

The conductor put back a fifth option: **measure code-only bytes, sum the page `consumes`-aware,
and move neither cap.** Dave: **"e"**.

**Why this is not a re-dial in disguise** — the objection is real and Amendment 3 records it rather
than dismissing it. A re-dial says *the same measurement, a bigger number*. Option (e) says *a
different measurement, the same number* — and the difference is falsifiable: under the new unit a
source can still fail, and does, if its **code** grows past 16 KB. What it stops charging for is
provenance text, which is exactly the material this project generates by policy and would
otherwise be taxed for writing.

**What it does cost, stated at the ruling and not discovered later.** Amendment 1's cap existed
partly to keep a partial *legible*, and a code-only unit prices comments at zero. So a source may
now grow unboundedly in comment bytes while reading as small. Amendment 3 **re-points that
conflict; it does not answer it**, and the raw figure is still printed beside the code-only one so
the question stays visible instead of becoming invisible. That is carry ② into #251, and it is
Dave's — there is no measurement of legibility anywhere in this repo.

## 6. The build, and the mutation that found a live hole in the old suite

Lane E's diff is +317/−44 on `knowledge/_validate_behaviour.py`: a code-only scanner that strips
comments and blank lines while *preserving strings and regex literals* (a naive stripper eats a
`//` inside a string and under-counts), a `consumes`-aware `check_group`, both figures printed,
the stale "32 KB" strings corrected, and three new mutation modes — `code-pad`, `comment-pad`,
`string-slash` — wired into `--selftest` for **9 new bites**.

★ **The mutation work paid immediately, and against the suite itself.** Two *pre-existing* pads in
the old selftest were COMMENT-padded. Under the old byte unit they bit; under the new unit they
would have passed silently — a green selftest proving nothing. They were converted to `CODE_PAD()`
rather than left to pass for the wrong reason. This is the [[mutation-tests-the-clause-not-the-feature]]
shape arriving inside the instrument that enforces it: **changing a unit can blind a test without
changing a line of the test.**

No canon `.js` byte was touched by any of this. The gate went from exit 1 to exit 0 on the same
tree.

## 7. The verifier could not break it, and named the place where it is breakable

Lane V ran cold — no access to the build lane's reasoning, 22 evidence rows filed beside the
report. Of 13 claims: **12 CONFIRMED, 1 CONFIRMED+REFINED, 0 CONTRADICTED, 5 NEW.**

The part worth keeping is *how* it tried:

- It wrote 15 adversarial JS constructs — regex literals containing `//`, strings containing
  `/*`, template literals, division that looks like a comment — and the scanner counted all 15
  correctly.
- It then ran **six deliberate under-count attacks**, and all six failed. ★ **The direction of the
  error was probed rather than assumed:** the scanner errs *larger*, never smaller. A byte gate
  that can be made to under-count is worse than no gate; one that over-counts is merely
  conservative.
- It cross-checked all 15 members' declared `consumes` against their injected blocks — all match.

**And then it named the hole.** `V-MUT-5`: the page sum *trusts* `consumes` and never reads the
snippet. A member that under-declares its sources goes green on a page it would in fact blow. ⛔
**An unguarded invariant, not a live defect** — nothing is mis-declared today. The distinction is
the point: the verifier did not report a bug, it reported that a property everyone assumes is
being *checked* is in fact being *taken on trust*. That is carry ① into #251, and it is Dave's
because it changes what the gate refuses.

⚠ **One incident, declared by the lane:** its own HEAD-gate probe overwrote
`knowledge/_BEHAVIOUR-GATE.md`. It regenerated the file, deleted its temp copies, and said so.

## 8. The refinement nobody was looking for

While reading a neighbouring gate, lane V found that `_validate_composition.py --selftest`'s
fixture anchor is found **zero** times: the template's `data-c` drifted **3 → 1** at `deb172a`
(#247), and the selftest has been passing by finding nothing to mutate. **Dark for two sessions.**

★ This is [[unmatched-grep-is-not-an-absence]] and [[instrument-without-a-consumer]] in one
artefact, and it was found by a lane pointed at a *different* gate. A selftest that cannot fail
looks exactly like a selftest that passes.

## 9. Where this leaves the wrap

`s250-D1` is inscribed in Dave's verbatim words and the store parses at **371**. The caps did not
move — that is the ruling's own text, not a wrap's restraint. `_validate_behaviour.py` was
re-driven at the wrap seat rather than quoted from the lane: **exit 0**, `--selftest` OK.

Two premises in the wrap brief were checked and one was stale: the brief said the tree was five
commits ahead of `origin/master`; `git status -sb` reads **ahead 7** — the two #249 DESK commits
landed after the figure was written. It is corrected in the spine, in the banner and in the carry
set, from the probe and not from the brief. ★ The rule that produced the correction is the same
rule the day was about: **a premise ages faster than the document that states it.**

The ceiling arm is still red, and #250's own boot — **69,293 real, the first post-diet reading
UNDER the 70,000 ceiling** — does not clear it: `boot_constant_drift_check` still names #247 and
#248 as readings over, and #242's breach as not discharged. It was **graded, not acted on**;
nothing moved; the `--wrap` form is refused for the fourth wrap running and the commit is made in
the #243 form with the refusal named rather than worked around.

---

## Still open, and whose

**Dave's:** the `consumes` guard (`V-MUT-5`) · legibility, unmeasured (ADR-0015 A1 vs A3) ·
rule 7 — confirm, keep as prose, or retire · DP-08 A+B (`s249-D1`, *"maybe"*) · the R/A signal
(`s249-D3`) · item 6 laid out visually (`s249-D6`) · META's and DESK's seven RSQs each · the
ceiling arm's three options (residual → #244 ⑤) · the push and its CI read-back.

**Claude's:** re-point and bite `_validate_composition.py --selftest` · W3 · the twelve unproven
dataviz members · a consumer for `_TEMPLATE-premise-probe.md`, if ⑤ survives.
