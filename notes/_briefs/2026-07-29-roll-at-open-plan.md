# Plan — roll at OPEN, not at wrap: what it is, what it buys, and what it does not fix

```
provenance: #40 opener · 2026-07-29 (Wed afternoon) · Opus solo, Dave live
status: PROPOSED — nothing enacted, nothing ruled. Dave asked for the plan before committing.
```

*Written because #40's survey of item 2 turned up three things the mast brief does not have,
and one of them changes what item 2 is for. **No code has been written.***

---

## §0 — THE SHAPE, reflected back so it can be corrected before it is built

**Dave's reading, and it is correct:** this moves part of the wrapping ritual to the beginning of a
session. Precisely:

- **What MOVES to the opener:** the four *displacement* steps — **2c** (banner stack), **2d** (LS
  delta stack), **2e** (DO-FIRST strata), **2f** (§C stratum). These are mechanical: find the
  overflow past a ruled `N`, move it verbatim to an archive. No judgment, no authorship.
- **What STAYS at wrap:** everything that requires the session to know what it did — writing the
  ★ LATEST banner, the ⏱ delta, the §C stratum, the commit, the index rebuild (2g), the dossier.

⚠ **One step does not cleanly belong to either, and it is §5's first question:** the **EXIT CHECK**
is currently a precondition of the roll. If the roll moves, the check moves with it — and is then
performed by a session that did not write the thing it is checking.

---

## §1 — WHY. The mast brief's §1 loop has a second half nobody has written down

The brief established that the cap fired *after* the record was written, so the only response left
was to shave live record. Item 2's answer was automatic displacement: roll instead of trim.

**But the roll runs at wrap, and so does the pressure.** A session runs out of window at its wrap —
and the sessions most likely to run out are the ones that did the most, which are exactly the
sessions whose roll matters most. Cheapening the roll does not help when there is no window left to
run anything.

★ **This is not a prediction. It is one session old and the gate is red on it right now.**
Step **2f is already scripted** — `roll_2f`, enacted #34, and the runbook says in bold that the roll
*"is no longer done by hand."* **#39 did not run it.** `ds-022` continuity: GM's ★ LATEST says #39,
the newest §C stratum key says #38.

★★ **And this is the strong form of the argument, not the weak one: #39 DECLARED it.**
`notes/_GAUGE-LOG.md`: *"**HOLE #39** — 2f not run by this session either, and it is **DECLARED not
slipped**… #39 chose to commit the durable record — ruling, brief, ledger, three lane receipts —
rather than half-do a roll it could not verify."* **This was not laxity and it was not forgetting.**
A session with the step scripted, knowing it was owed, naming it in the log, still could not run it —
**because the window was gone.** That is the mechanism, stated by the session that hit it.

⇒ **Scripting a step lowers its cost. It does not buy the window to run it.** §4 of the mast brief
claims displacement makes growth *"bounded by construction, not by restraint."* That claim is too
strong: a construction that only executes at wrap inherits the wrap's budget. The counter-example
predates the brief by a day.

---

## §2 — WHAT IT ACTUALLY BUYS. Recovery, not prevention — and the distinction is the whole point

A roll at the opener does **not** stop a session skipping its wrap. Nothing can. What it does is
make the skip **self-repairing instead of accumulating**:

| | roll at WRAP (today) | roll at OPEN (proposed) |
|---|---|---|
| paid by | the window that has least left | a fresh window |
| a skipped roll becomes | **debt** the next session must notice and clear by hand | **nothing** — the next opener rolls it automatically |
| runs when the previous session died mid-wrap | no | yes |
| safe to run unconditionally | n/a | **yes — a roll with no overflow is a no-op** |

★ **Idempotence is what makes this cheap.** Rolling when there is nothing to roll costs one call and
changes no bytes, so it can run at *every* opener without anyone deciding whether it is needed.
Deciding whether a step is needed is the thing that fails.

★ **And the enforcement consumer already exists.** [[instrument-without-a-consumer]] — a gate that
does not run cannot fail. The opener has one thing guaranteed read by every session: the
`GOOD-MORNING.md` header, which *is* the read chain. That is where the instruction goes.

---

## §3 — WHAT IT DOES NOT FIX, MEASURED. Displacement has a floor, exactly like retirement did

⛔ **This is the finding that should change how item 2 is priced, and it was measured today, not
reasoned about.**

**The banner region is over its warn while fully compliant with its ruled `N`.**

| | measured #40 |
|---|---|
| banners in `GOOD-MORNING.md` | **2** — ★ LATEST #39, ★ PRIOR #38 |
| ruled `N` (2c) | **LATEST + 1 PRIOR = 2** ✅ compliant |
| banner region | **4,715 tape / ~7,403 bill** |
| warn / block | 4,000 / 5,000 tape |

**There is nothing to displace, and the region is 715 tape over warn and 285 from its block.**
The header is 1,614 tape; the two banners are 1,278 and 1,758.

⇒ **Displacement has a floor, and the floor is `N` × the size of one unit.** This is #38's retirement
lesson one level up — retiring a verified-dead item netted **+16 tape** because the region has a
floor; rolling has one too, and it is much higher. **Item 2 cannot relieve the banner region at all.**
Only a smaller `N`, or smaller banners, can — and both of those are yours.

⚠ **Corollary, and it should be said out loud:** the mast brief's items 1 and 2 do not overlap the
way the sequence implies. Item 2 was placed first *"because it shrinks the file, so the seam in item 1
is cut on a smaller thing."* **On the banner region it shrinks nothing.**

---

## §4 — CORRECTIONS TO THE LIVE RECORD, found by verifying rather than reading

1. **⚠ LIVE-WRONG — #39's banner says *"2c ROLL IS OWED — this block was inserted, not moved…
   #38's banner is still below as ★ LATEST and #36's as ★ PRIOR."*** The file carries ★ LATEST #39
   and ★ PRIOR #38 — **two banners, compliant** — and #36's banner is **in `_GM-ARCHIVE.md`**
   (observed at line 4; which batch it sits under is not established here and does not bear on this).
   **The 2c roll is not owed.** Strike at source when the record is next touched.
2. **✅ `ds-022`'s evidence is ALIVE — it is the MIRROR of `HOLE #35`.** #39 wrote the **log** half
   (`notes/_GAUGE-LOG.md` § `#### 2026-07-29 #39`) and not the **GM stratum** half. #35 failed the
   other way round. ⇒ the FAIL is dischargeable **by ADDITION from real testimony**, not by
   reconstruction. [[gap-in-record-vs-gap-in-evidence]], applied.
3. **⬛ GENUINELY OWED from #39 — four, and the list is shorter than #39's own:** the §C stratum
   above · the `_LIVE-STATE.md` ⏱ delta (LS is one session stale — it carries #38 / #37 / #36,
   compliant at `N`=3, but #39 never wrote one) · the tape/bill pair · the #37 and #39 dossiers.
   ⚠ **#39's owed-list opens with *"resolve `HOLE #38` (check GM §C first)"* and that instruction is
   already spent** — `HOLE #38` was **WITHDRAWN in the same log block**, by the gate, an hour after it
   was declared. [[unmatched-grep-is-not-an-absence]]. **A session following the list in order would
   spend its first move on a closed item** — which is the [[premise-ages-faster-than-rule]] class
   appearing *inside a handoff instruction*, not in canon.
4. **Your NUMBER 2 is mostly already ruled.** All four regions carry an `N` you set: 2c = LATEST+1 ·
   2d = LATEST+2 · 2e = LATEST+1 · 2f = LATEST only. Item 2 needs a new number only for a region that
   has none.

---

## §5 — WHAT IS YOURS TO RULE. Named, not resolved — three, and none of them are the timing

The timing change itself is small. These are the parts that are not.

1. ⬛ **Who runs the EXIT CHECK.** Today the session that *wrote* a banner scans it for ⚠/⬛/AWAITING
   items before it rolls. Move the roll and a **cold** session does it instead. Arguably better — a
   cold reader is closer to how the record will actually be read, and #38's catch happened one op
   before a roll. Arguably worse — that session does not know *why* something was deferred.
   **A third option exists: split it.** The check stays at wrap, the move goes to the opener.
2. ⬛ **Parallel lanes.** [[feedback-parallel-conductor]] — rolls currently happen at wrap under the
   conductor rule. An unconditional opener roll in a worker lane could collide with the conductor's.
   Cheapest answer is *conductor rolls, workers never* — but it needs saying, not assuming.
3. ⬛ **The banner `N`, or the banner size.** §3 says displacement cannot help this region. `N`=1
   would; so would a cap on a single banner. **Both are re-dials of numbers you ruled**, and
   ds-023 is the standing case against an agent promoting one because it noticed.

⚠ **Not a question, a warning:** if the roll moves to the opener and *nothing* is added at the wrap
end, the wrap gets cheaper and the opener gets more expensive. The opener is the window with room, so
that is the right direction — but it should be **measured after one session**, not assumed.

---

## §6 — THE WORK, if you rule GO. Sized, in order

| # | step | shape | cost |
|---|---|---|---|
| 1 | Discharge `ds-022` by addition — write #39's §C stratum from the live gauge-log block | mechanical, evidence exists | ~1–2 calls |
| 2 | Generalise `roll_2f` → `roll(region, n)` over the four regions, ruled `N`s, extend the existing selftest | worker-lane / Sonnet | ~half a session |
| 3 | Move the four roll steps to an OPEN block in `_RUNBOOK-capture-ritual.md`; header instruction in the chain | doc + one contract line | small |
| 4 | Opener check in `_capture_gate.py --open`, **ADVISORY at birth** | gate | small |
| 5 | Measure the opener and the wrap for one session; report the shift | measurement | free at next wrap |

⚠ **Step 2 does not need step 3, and step 3 does not need step 2.** They are separable, so a short
window can take either.
⚠ **Step 4 is born ADVISORY on purpose.** Promotion is Dave's word — ds-023.

## §7 — WHAT WOULD UNDO THIS

- **Declaring it fixed.** Every mechanism here is silent when healthy. The mast brief's §5 tripwire
  applies unchanged.
- **Letting the opener roll become a reason not to roll at wrap.** It is a *safety net*, not a
  replacement. If wrap-rolling stops entirely, the file carries `N`+1 regions permanently and the
  chain grows by one banner — ~1,500 tape, which is a third of the whole chain.
- **Believing item 2 relieves the banner region.** §3. It does not.

## Entry points

`knowledge/_gm_move.py` (`roll_2f` + selftest — the pattern to generalise) ·
`knowledge/_RUNBOOK-capture-ritual.md` steps 2c–2f ·
`knowledge/_capture_gate.py` (`ds-022` continuity check, `SIZE_BUDGET_TK`) ·
`notes/_briefs/2026-07-30-nail-it-to-the-mast-structural-brief.md` (the parent brief — §4's
"bounded by construction" is what §1 above qualifies) ·
`notes/_GAUGE-LOG.md` § `#### 2026-07-29 #39` (the surviving half of #39's 2f).
