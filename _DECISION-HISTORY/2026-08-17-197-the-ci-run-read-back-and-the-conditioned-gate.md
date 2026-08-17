# #197 — the CI run was read back, and the WARN gate got a condition

```
provenance: 197 · 2026-08-17
status: observed
```

*The narrative dossier for session #197 (capture-ritual step 1b). The WHAT lives in
`GOOD-MORNING.md`'s ★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST delta, and
`knowledge/_rulings.json` § `s197-D1`. This file holds the WHY and HOW.
Written by the DELEGATED wrap sub; every sha here is read back from `git log`.*

---

## 1. The debt the session opened on, and why it was the right one

#196 built `knowledge/_validate_queue_fresh.py` — the class fix for "we keep missing decisions
already made" — and shipped it **WARN**, routed in CI, with two honest holes on its residual:
the CI arm had never been observed green *in CI* (only locally), and the WARN→BLOCKING flip was
deferred to Dave with **no date and no condition**.

Those two are the same defect in different clothes: a claim whose truth is *asserted* rather than
*observed*. #197 closed both, and it closed them in the only order that works — **observe first,
then rule**.

## 2. The read-back, and what it actually proved

Run **`32067526100`** on **`e95ea60`**, read via the API. **124 steps read by AST** — not by
eyeballing a log, because a log read by eye is a count, and a count is not a measurement
[[measure-dont-convert-units]].

- The new gate's selftest **`[55]` was GREEN in CI, 13 bites, both mutation directions.** That is
  the CI arm, proven, and it is the only thing that could have proven it.
- The run as a whole was **RED — on exactly one step**, `[110]`, the graph mention-map determinism
  check, stale. Reproduced locally, map regenerated, fixed at **`165bb72`**, green locally.
- The **6 COULD-NOT-ASK entries are the documented #173/#193 environment class** and are unchanged.
  They are not new damage and were not counted as such.

★ **The finding worth carrying: one read-back answered two carries.** #195's CI-count item and
#196's CI-arm item were the same question addressed to the same run, so the second was marked
**SUBSUMED with its reason named on the line**, rather than dropped silently. A silently vanished
carry is indistinguishable from a lost one, which is what the 2c EXIT CHECK exists to prevent.

## 3. Why the flip was CONDITIONED rather than dated — `s197-D1`

The obvious move was to flip the gate to BLOCKING now that CI had blessed it. Dave did not do
that, and the reason is the more interesting part of the session.

CI green proves the **selftest** passes. It does not prove the gate behaves correctly **in anger** —
against a real banner roll, on the real file, at a real wrap. Those are different claims, and a
mutation test proves the CLAUSE, not the FEATURE [[mutation-tests-the-clause-not-the-feature]].

So the ruling attaches the promotion to an **event, not a date**:

> `s197-D1` — `_validate_queue_fresh.py` stays **WARN** until it survives **one real banner roll
> in anger**; it flips **BLOCKING at the following session**.

Inscribed through `knowledge/_inscribe_ruling.py` (the only sanctioned writer), reconstruction
proof passed, rulings **183 → 184**, commit **`e86b144`**.

★ **Why this is an improvement on "deferred to Dave":** an undated deferral has no failure mode —
it can sit forever and nothing ever notices. A conditioned one has a **trigger and a return**, and
the return is now a carried residual with an owner. That is the difference between a decision and
a postponement [[conclusions-are-debt-s129-d5]].

## 4. The condition's first drive — and the honest bound on it

This wrap performed a real banner roll (2c/2d/2f, through `_gm_move.py`), which makes it the
gate's first live drive across roll machinery. Driven immediately after, verbatim, rc=0:

```
queue freshness — §C·1 items measured: 7 (severity: warn)
RESULT: PASS — no §C·1 item's stated state is contradicted by disk or git. This proves no claim
is STALE; it does not prove the queue is RIGHT.
```

It did not warn and it did not misfire. **But the evidence is bounded and the bound matters:**
the roll moved the BANNER stack, the LS DELTA stack and the STRATA stack — it did **not** touch
**§C·1**, which is the only region this gate reads. So the drive proves the gate **survives** a
real roll; it does **not** prove the gate would **notice** a roll that moved §C·1.

⚠ And a second bound, declared rather than reconstructed: **no pre-roll baseline was captured**.
The gate was driven only after the rolls, so a before/after comparison is unavailable. Saying so
is cheaper than a clean-sounding claim that cannot be re-derived
[[feedback-check-ran-never-reached-plan]].

## 5. `--pri-hover` — Dave chose to look, not to rule, and looking found something

The carried item was a promotion: the stored colour-equivalents `#626262` / `#B7B7B7` were derived
at the retired `0.70` rather than the live `--alpha-68`. Dave declined to rule from the numbers and
asked for a live comparison instead — his standing pattern, and the right one for colour
[[feedback-review-live-variant-spread]].

The page is `reviews/PRI-HOVER-COMPARE-2026-08-17-v1.html`, doc row **`W-37`**, and it closes when
he rules.

★ **The finding that fell out of building it, surfaced and NOT ruled:** the **dark** stored hex
reproduces `0.70` exactly; the **light** stored hex implies **α≈0.6856**. The light value was
therefore **never a clean `0.70` composite** — the record's own premise about how it was derived is
wrong, independently of which value wins. That is a premise defect, not a colour defect
[[premise-ages-faster-than-rule]], and it is Dave's eye next session.

⛔ **No re-derived hex was written into canon, tokens, or any record by this session.** They exist
on the compare page and nowhere else, which is what "promotion is Dave's alone" has to mean in
practice.

## 6. The memory-index compaction, and the method that made it safe

#196's residual ⑧ closed from the conductor's seat (a delegated wrap sub cannot reach the store —
⚠ **NON-REPO**, declared per `s191-D2`'s home-or-declare rule). **20.3K → 17.75K** against a
**17.1K** target ⇒ **651 bytes over, DECLARED as a residual** rather than rounded away.

The method is the part worth keeping: **home by addition, then cut** — detail was written into
`memento-closeout-plan.md`, `borrowed-instruments-brief.md`, `retrieval-default-hides-the-ruling.md`,
`stop-line-repriced-93.md`, `write-once-principle-floated-192.md`, `b3-review-ruled-182.md` and
`delegation-cost-inversion-110.md` **before** any index line was cut; 14 settled
look-up-by-name entries were archived to `MEMORY-ARCHIVE.md` in two dated batches; **zero memory
files were deleted** [[memory-compaction-mechanics]] [[home-by-addition-then-cut]].

★ The 651-byte miss is recorded rather than closed because a target hit by deleting something
retrievable is not a target hit.

## 7. Two refusals that behaved exactly as designed

- T3's **reused-msgfile** gate fired once on the conductor: T3 writes the session prefix back into
  the msgfile after a `SESSION_N` refusal, so the second attempt read a mutated file. The remedy was
  the runbook's **fresh `printf` msgfile** — not an improvisation — and **nothing was staged on the
  refusal.**
- The worker sub's commit script **refused on a STALE `_CHAIN.md`** and the sub ran **the named
  remedy (`_gen_chain.py`)** rather than treating the refusal as a syntax puzzle. That is precisely
  the behaviour `_RUNBOOK-git-commit.md` line 36 was written to produce after #117, #133 and #185
  each failed to produce it [[feedback-read-the-runbook]].

Both are recorded because a gate that fires and is obeyed is the only evidence that the gate is
alive [[instrument-without-a-consumer]].

## 8. What is still open

Carried onto the ★ LATEST banner's `residual → #198`, with ages. The two that are this session's
own: **Dave's eye on the compare page** (⬛ his, including the α≈0.6856 finding) and **`s197-D1`'s
return** — after the first real banner roll, read the gate's behaviour back and flip it to
BLOCKING. This wrap performed a roll and recorded what the gate did; it did **not** flip the tier,
because the tier is Dave's and the ruling names the session, not this one.

---

*Both-way links: `GOOD-MORNING.md` ★ LATEST #197 · `_LIVE-STATE.md` ⏱ LATEST DELTA #197 ·
`knowledge/_rulings.json` § `s197-D1` · `knowledge/_REVIEW-SIGNOFF.md` (the compare-page row) ·
commits `165bb72` · `e86b144` · this wrap's own commit.*
