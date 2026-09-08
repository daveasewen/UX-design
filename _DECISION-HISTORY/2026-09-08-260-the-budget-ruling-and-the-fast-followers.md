# #260 — the budget ruling, the eight fast followers, and a release that was blocked by arithmetic

provenance: 260 · 2026-09-08
status: observed

*The WHY and HOW of session #260. The WHAT — rulings, commits, figures — lives in
`knowledge/_rulings.json` (entries 404–407), the `#### 2026-09-08 #260` stratum of
`notes/_GAUGE-LOG.md`, the ★ LATEST banner and the ⏱ LATEST delta. This file holds the arc:
what we believed at the opener, what moved, and what it cost to find out.
Both-way links: `_LIVE-STATE.md` ⏱ LATEST DELTA #260 · `GOOD-MORNING.md` ★ LATEST #260 ·
`knowledge/_rulings.json` § `s260-D1` … `s260-D4`.*

---

## 1. The premise at the opener: "two reds block the release"

#259 ended with the chart engine in the library and two gates red — `_validate_behaviour`'s page
budget (Chart-combo 43,518 and Chart-donut 37,787 against 34,816) and `_validate_dataviz`'s
**dv-004** on the donut. #257 had already established that cutting a release over a red gate is
laundering, so v1.0.8 was genuinely blocked.

**What moved: neither red was a defect.** Both were the same shape from opposite ends —
a gate measuring the wrong thing:

- The budget gate was charging the shared 9KB engine core to **every member page that loads it**.
  Six member pages, one file, six charges. Nothing had grown; the accounting had.
- dv-004 reads authored markup for gap geometry. On an engine-drawn chart there **is** no authored
  markup — the marks are painted at runtime — so the gate failed safe on an artefact it could not
  see [[no-gate-parses-the-artefact]].

That reframing is why the day's first work was a decision request rather than a fix. Dave was
offered three shapes for the budget (price the core once per page · raise the literal · drop
`dv-legend` from engine-drawn members) and two for dv-004 (driven receipts become the evidence ·
or the engine self-reports and the static gate trusts it).

**His answers, and the reasoning worth keeping.** He took option 1 on the budget — *"11 but I feel
like the budget might have to be raised at some point in the future"* — which is a ruling **and**
a flagged expectation, and the two are recorded separately: the literal did not move, and the
possible future raise is carried as his caveat rather than pre-authorised. On dv-004 he took (a),
the driven receipt. Option (b) was recommended against for a reason this repo has paid for before:
an engine that grades itself is an instrument with no consumer, and the gate would have been
asserting the engine's own opinion back at itself [[instrument-without-a-consumer]].

## 2. The gate that was built, and the twelve pages it could not see

Lane A built the driver, the committed receipt store and the gate route in one pass, and a cold
verifier (V) confirmed 5 of 5 claims with two of its own mutations — correcting one along the way
(pie is not engine-drawn in the shipped snippet, so V's correction narrowed a claim rather than
breaking it).

**Then the second verifier found the real hole.** V2 drove the STALE arm — the half of the gate
that is supposed to refuse an out-of-date receipt — and found it **unreachable for 12 of 13
pages**. The green had been real for the FRESH path and vacuous for the RED path.

★ **The lesson, and it is the one that keeps recurring: a gate's green says nothing until its red
path has been driven** [[mutation-tests-the-clause-not-the-feature]]. Both verifier seats paid for
themselves in one session, and neither finding would have surfaced from reading the lane's report.

## 3. Eight chart types in one wave, after six had cost a whole session

#259 spent an entire window on six chart types. #260 landed the remaining eight in one parallel
wave of four lanes. The difference is not effort — it is that `s259-D1`'s six had to invent the
engine, and the eight only had to plug into it. Two of the eight cost no new code at all: **pie
composes `dv-render-donut`'s ri = 0 arm**, and a lane explicitly refused to write a
`dv-render-pie.js` that would have duplicated one routine.

★ **The cheapest thing in this session was the thing #259 declined to rush.** Dave's *"do the 6
types but i want the rest as a fast follower"* bought a stable core before the volume arrived; the
fast follower then cost one wave instead of a second session.

⚠ **And the four lanes independently asked for the same things.** Three of them wanted a furniture
opt-out; three wanted a zero-clamp. None had seen another's report. Collated in
`notes/_lanes/260/_CORE-REQUESTS-collated.md` — **the votes are the finding**, because three
independent authors converging on one missing affordance is evidence in a way one request is not.

## 4. What we did NOT do, and why

- **The 2dp donut-gap emission patch was measured (2.109 → 2.194) and NOT applied.** Changing what
  the engine emits changes every drawn chart in the library; a lane measured it, filed it, and left
  it. Correct call, recorded so nobody re-derives it.
- **`_validate_screen.py` was not run** — it clobbers tracked ledger rows keyed on basename, a
  known defect carried since #258 and still unrepaired.
- **`test_gates.py` was not run** — it copytrees ≈5 GB and cannot execute in this sandbox at all.
  A gate that can only pass in one of its two environments is a gate whose green is an environment
  fact [[gate-cannot-pass-in-one-environment]].
- **Nothing was pushed.** Sixteen commits, including the v1.0.8 release, stand local.

## 5. The stop line moved, and the thing that moved it was a field nobody was using

`s260-D2` repriced the delegated-wrap advisory from 150,929 to 180,000. What made that a
measurement rather than a preference is the `wrap-handover:` line `s214-D5` added at #214: six
sessions of MEASURED hand-over deltas (4,077 · 4,154 · 4,799 · 10,434 · 10,382 · ≈9,870) against a
worst case of 10,434, leaving a 20,000 reserve at the new line.

★ **This is a staged re-derivation actually discharging, which is rare enough to note.** `s214-D4`
was written to fire when the field reached n ≥ 2; it sat unused for six wraps while the field
filled, and then the ruling was made on data rather than on a feeling about how big wraps are.
The instrument had a consumer, and it waited for one.

## 6. The record refused to be tidied, and that is the correct outcome

The #259 opener wrote a ceiling-discharge block into `notes/_GAUGE-LOG.md` keyed
`#### 2026-09-08 #259`. `_key_session` reads the key, not the suffix — so when this wrap tried to
roll #259's real stratum out of `GOOD-MORNING.md`, the mover refused: *"already carries a block for
#259 … NOTHING written"*.

⛔ **The available repair — renaming the discharge heading so the key frees up — was not taken.**
`ds-022 (d)`'s own docstring records what happened last time a key was edited to quiet a parser:
three unrolled sessions looked rolled, and a handoff instructed a roll of twelve blocks that was
really nine. De-keying is the same move with the sign flipped. The three options (exempt · re-key ·
teach the discharge form a non-session key) were put to Dave at #259 and remain his.

**Resolved state:** `GOOD-MORNING.md` closes carrying two live strata against a cap of one, the
refusal is quoted verbatim in three places, and nothing was edited to make a gate read green.

## 7. Still open

The push · the driver's scope (only one of thirteen pages measures anything, and two gates pass on
a JS string literal) · `--full-stage` silently deciding the ship set · the sanctioned commit path
that cannot leave a clean tree while `--release` requires one · two unrunnable gates · the 2dp
emission and the pie's magic 0.35·ro · seven core requests · three lane-made changes to ruled or
fenced material · 37 uncounted sub-24px a11y marks and a histogram that cannot satisfy the 24px
floor and stay contiguous · a behaviour gate that rewrites its own tracked ledger · the boot arm ·
the unrollable stratum. All of it with ages and receipts in `_CARRIES.md` § `## residual → #261`.
