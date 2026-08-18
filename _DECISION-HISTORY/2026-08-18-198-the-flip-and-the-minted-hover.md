# #198 — the WARN gate flipped to BLOCKING, and `--pri-hover` was ruled and minted

```
provenance: 198 · 2026-08-18
status: observed
```

*The narrative dossier for session #198 (capture-ritual step 1b). The WHAT lives in
`GOOD-MORNING.md`'s ★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST delta, and
`knowledge/_rulings.json` § `s198-D1` / `s198-D2`. This file holds the WHY and HOW.
Written by the DELEGATED wrap sub; every sha here is read back from `git log`, never from
the brief this sub was given.*

---

## 1. The condition was met by a roll nobody performed on purpose

`s197-D1` did not flip the stale-queue gate — it gave the flip a **condition**: the gate had to
survive one real banner roll in anger, and then flip at the following session. What made that
ruling work is that the evidence it demanded was produced as a **side effect** of the #197 wrap
itself (`5b77cce`, recorded verbatim at `GOOD-MORNING.md:522`). #198 opened, read that record
back rather than asserting it, put it to Dave, and got the word.

The WHY worth keeping: a conditioned deferral is cheap when the condition is something the
project already does every session. An undated "Dave will decide" would still be open.

## 2. The flip moved two things, because one of them is a join key

`f0ab051` moved the **route row (ADVISORY → GATE)** and **`SEVERITY=blocking`** together. The
temptation was to flip severity alone — the behaviour lives there. But a severity flip with a
stale route label is [[instrument-without-a-consumer]] in its documentation form: the table a
reader consults would disagree with the code that runs. It was refused.

⚠ And it was not fully paid: the route **label** still reads `(WARN, #196)`. Labels are join
keys (#166), so correcting it is a two-table edit, and it is owed rather than done.

## 3. The de-risk drove the real grammar, not a fixture

Three mutations plus a control, all on the live surface: a **fake sha** FAILED and *named the
item*; a **stripped annotation tail** FAILED on presence; the **unmutated** file PASSED; and the
real `GOOD-MORNING.md` came back **byte-identical** after the drive. That last one matters more
than it looks — it is the evidence that a blocking gate driven over the live record does not
rewrite it.

★ What is still NOT proven, and is carried: the gate reads **§C·1 only**, and no roll performed
so far has moved §C·1. Survival is proven twice now (WARN at #197, BLOCKING at this wrap, and
this time with a **pre-roll baseline** as well as a post-roll one — the comparison #197 had to
declare unavailable). **Detection across a §C·1-moving roll remains unobserved.**

## 4. The colour: a compare page beat a proposal

#197 declined to rule `--pri-hover` and built a live compare page instead. #198 is the payoff —
Dave ruled off the page in one pass (*"the suggestions are approved"*, readback confirmed):
`s198-D1` re-derives the stored hover at **0.68** (light `#626262`→`#636363`, dark
`#B7B7B7`→`#B2B2B2`) and `s198-D2` **mints** `color/mono/hover-1|hover-2` with neutral mirrors
and re-points the aliases. Both inscribed by the conductor via `_inscribe_ruling.py`
(184 → 186), enacted at `5297f47`.

The method note: the re-derivation had been sitting as a *promotion awaiting Dave* since #106.
What unstuck it was not a better argument — it was showing him the two colours side by side.

## 5. The dead-end that would have shipped silently

The first regeneration would have **dropped Supercharge's hover to the mono greys**. Nothing
would have failed; the theme would simply have stopped being itself. Scope-preserving overrides
were added (`neutral/hover-1` → warm/7, `hover-2` → warm/10) for **zero pixel change**.

⚠ Declared, not smoothed: that is a **ramp SNAP, not a 0.68 warm derivation**. Supercharge is
now correct by pinning rather than by construction, and whether it should get its own derivation
is **Dave's**. Same shape as the icon-button, which hardcodes **70%** at `canon.css:~7836` while
the button family now renders 0.68 — a pre-existing divergent render, found here, priced as a
TODO, not repaired in passing.

## 6. What the commit path taught, again

Five refusals, every one answered by its named remedy: **chain-stale ×2** (`_gen_chain.py`),
**reused-msgfile ×2** (T3 writes the session prefix back into the file — so a msgfile is
single-use, *including after a refusal*), and **no-paths ×1** (`--all-dirty` after a path-by-path
reconcile). Nothing was staged on any refusal and nothing was improvised.

★ The reused-msgfile class bit **twice in one session**. That is the tell that "use a fresh
`printf` msgfile" is not yet mechanical — it is still a thing sessions remember.

## Resolved state, and what is still open

**Resolved:** the stale-queue gate is BLOCKING (`f0ab051`) · `--pri-hover` is ruled, minted and
enacted (`5297f47`) · `W-36` and `W-37` are CLOSED · #197's residuals ①, ② and ③ are all
consumed.

**Open (carried to #199):** the `hover-1`/`hover-2` **naming**, Dave's · Supercharge's snapped
hover, Dave's · the icon-button's hardcoded 70% · Group B components (`cn-modals`/action-bar/
confirmation/drawer) rendering `var(--pri-hover)` flat, unrendered by eye, and the console theme
inheriting the change by design, also unrendered · the stale-queue gate's **detection** across a
§C·1-moving roll, its `(WARN, #196)` route label, and its selftest docstring saying 6 bites where
it runs 13 · downstream **baked artefacts stale** wrt the four new canon vars (`_build_all.py`
deliberately NOT run — a partial run strands the tree) · **memory step 3**, owed from the
conductor's seat because the store is non-repo and a wrap sub cannot reach it.

⛔ Not pushed. Push is Dave's word and it was not given this session.

*Spine links: `GOOD-MORNING.md` ★ LATEST #198 · `_LIVE-STATE.md` ⏱ LATEST DELTA #198 ·
`knowledge/_rulings.json` § `s198-D1`, `s198-D2` · `notes/_GAUGE-LOG.md` § `#### 2026-08-18 #198`.*
