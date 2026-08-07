# #118 — THE BUCKET SORT, FOR DAVE'S CHALLENGE BEFORE I ACT

> **Status: floated.** Nothing here is enacted. Dave ruled at the #118 opener:
> *"Show me the bucket sort before you act."* This is that.
> ⚠ **8 of 17 verified by DRIVING the thing. 9 are sorted on their nature, not a probe — marked UNPROBED.**

---

## ★★★ THE HEADLINE: THE HANDOFF'S OWN PROOF CASE IS WRONG

`_HANDOFF-117` named **item 8** — `_validate_type_composites.py` — as the proof case for bucket D:
*"The gate has never been built. Three months of knowledge, zero enforcement, one live defect."*

**MEASURED, this session:**

| Claim | Reality |
|---|---|
| "the gate has never been built" | **It was built 2026-07-18.** `knowledge/_validate_type_composites.py`, 10,602 bytes |
| implied: it doesn't work | `--selftest` → **OK**. Three checks (TYPE-001/002/003), Dave's own 2026-07-18 scope ruling encoded |
| implied: it can't fail | True exit code **1**. **1,101 violations across 90/90 files** — 81 real component snippets, only 9 demo |
| `MEMORY.md`: *"the gate is a TODO, NOT built"* | **FALSE** |
| #117: archived it *claiming a gate enforced it* | **FALSE, the other way** |

⇒ **The gate is not missing. It is UNWIRED.** No reference to it exists in `_build_all.py`. Twenty-odd
sibling validators are in that list; this one never joined.

★★★ **This sharpens the bucket-D diagnosis rather than refuting it.** The handoff said *knowledge does
not throttle behaviour*. The truth is worse and more specific: **the gate was WRITTEN, and writing it
changed nothing, because it was never connected to a consumer.** Building the instrument was never the
hard part — *wiring* it was, and wiring is the step with no gate on it.
⇒ **Three records described one file's state wrongly, in three different directions, for three weeks.**
Nobody ran it. **A file's existence is not evidence of its enforcement** — the same shape as
[[instrument-without-a-consumer]] and [[premise-ages-faster-than-rule]].

⚠ **And the wiring is not a one-liner**, which is probably why it never happened: connecting it
BLOCKING turns the whole build red on 1,101 violations today. See the recommendation below.

---

## THE SORT

### (B) MIS-ESCALATED — MINE. I take these back. *(the test: if you said "you decide", nothing is lost)*

| # | Item | Verified? | What I'll do |
|---|---|---|---|
| **8** | type-composite gate | ✅ **DRIVEN** — built, green selftest, rc=1, 1,101 violations | **Wire it as a shrink-only RATCHET at 1,101**, not blocking-at-zero. See the caveat below — I want your eye on it |
| **15** | `#89-D2` ruled-not-enacted | ✅ **CONFIRMED** — 0 occurrences in `_state.json` across 4 probes; ×6 in `_MEMENTO-DECISIONS.md` | Enact it into the store |
| **13** | `CTRL` gate vocabulary unswept | ✅ **CONFIRMED** — `_DS-IMPROVEMENTS.md:676` states it verbatim; **1,869 selectors skipped** by the `CTRL` regex | Run the sweep. Measurement, not judgement |
| **9** | `--pri-hover`: 35 of 40 names unmeasured | ✅ **CONFIRMED not started** | Sweep them **PER THEME** — a global sweep manufactures ~35 false findings, because your four themes are *expected* to diverge on the same name. ⚠ The *scope ruling* that follows the sweep stays **yours** |
| **7** | surface-recorder stale constants | ⚠ PARTIAL — found `NOISE_FLOOR_TK = 708` + `55_025` refs, didn't isolate all three | Re-measure and refresh |
| **10** | `ds-025` — split the 56,308 | UNPROBED | Tokenisable off disk in one pass |
| **11** | G5 ceilings denominated in TAPE | UNPROBED | Re-denominate to real. ⚠ measure BOTH sides in the ceiling's unit first |
| **14** | p4/p6/p7 reachability | ⚠ **CONTRADICTED** — `_validate_standing_instructions.py` **PASSES**: 28 standing docs reachable | ⛔ **NOT closing it.** There is a known **P-SET COLLISION** — two sets share these numbers with opposite statuses. I must confirm which set before declaring anything |

### (C) STALE / SELF-ANSWERED — close by addition, once confirmed

| # | Item | Evidence |
|---|---|---|
| **17** | "ds-020 FENCED" | ⚠ **Looks stale.** `_DATAVIZ-DECISIONS.md:707` — **`ds-020` ENACT was APPROVED by you at #69 (D1)**. The "FENCED" label appears to predate your own approval. Confirming, then closing by addition |

### (D) NOT A DECISION — AN UNGATEABLE HABIT. Mine entirely, and none of it is yours to answer

The seam, in each case, is *the moment the omission becomes durable*:

- **The wiring seam** — item 8 is the specimen. A validator can be written, reviewed, committed and
  remembered without ever entering `_build_all.py`. **Gate: assert that every `_validate_*.py` on disk
  appears in the build list, or carries an explicit declared exemption.** That gate would have caught
  this on 18 July. It is small, and I'll build it.
- **The stale-mount seam** — see the correction at the foot of this file. A quiet repo and a stale
  read are indistinguishable from inside.

### (A) GENUINELY YOURS — kept, exact original wording, put to you ONE AT A TIME with a recommendation

Not asked here. Listed so you can see I haven't quietly absorbed any of them:
**1** boot re-base to 54,859 ±850 · **2** v1 designer pack, frozen-until-rebaked vs belt-and-braces ·
**3** mono grey ramp "calculated wrong" (you said NOT NOW) · **4** SC dark, G14 · **5** dv-lockup's
3 placeholder titles · **6** graph-mark demote (blocked on my `--tally`, not on you) ·
**12** G8 retire-or-pin · **16** chart-expansion residue (mixed — I'll split it before asking).

---

## THE FINDING YOU ASKED ME TO PROVE OR REFUTE

The handoff claimed: *"roughly half this list was never Dave's."*

**Sorted: 8 of 17 are B, 1 is C, and bucket D is new work of mine. That leaves 8 genuinely yours —
and 2 of those (6 and 16) are blocked on me, not on you.** ⇒ **The claim holds.** Rather better than
half of what has been sitting in front of you was mine to take back.

⚠ **Counter-evidence, stated plainly:** I sorted 9 of the 17 on their *nature* without probing them.
Every one of those went to A or B on a judgement call, and item 8 is this session's proof that a
confident judgement about an unprobed item can be wrong in three directions at once.

---

## ⛔ THE ONE THING IN BUCKET B I WANT YOUR EYE ON

Wiring item 8 is mechanical; **choosing the tier is not, and I don't want to slip it past you.**

- **(a) BLOCKING now** — honest, and the build goes red immediately on 1,101 violations. Nothing else
  ships until they're fixed.
- **(b) SHRINK-ONLY RATCHET at 1,101** — enforcing *today* against any new violation, existing debt
  declared and drawn down.

**My recommendation is (b).** But I have to name the risk myself, because it is a rule of this project:
**a baseline set to today's count has exactly the shape of "a cap raised to clear its own gate".**
The difference I'm claiming is that it may *only shrink* and is declared as debt rather than absorbed
as a pass — and if you don't buy that distinction, (b) is not defensible and (a) is what's left.

---

## ⚠ CORRECTION — MY OWN OPENER WAS WRONG

I told you at the opener that #117's work was *"committed nowhere"* and that there were *8 structural
fails*. **Both were false.** A prior #118 recovery sub had already run the full wrap and committed at
`675a626` (Aug 6, 21:30) — subject self-certifies as #117, chain routes to #118, structural fails **0**.

**Cause: the mount served me `_CHAIN.md` at its 20:03 state while disk held 21:30.** I read the
handoff's premise and the stale file, and they agreed with each other — which is exactly why I didn't
catch it. ★ **A stale mount looks like a quiet repo**, and two stale sources corroborating each other
feel like verification.

⚠ **Also inherited, and still uncorrected in the record:** `notes/_GAUGE-LOG.md`'s #117 post-mortem
carries **wrong compaction figures** (18,367 / −12.1% / 105 entries). Disk says **19,088 / −8.69% /
107 entries**, and the handoff is the one that's right. To be corrected at #118's wrap **by addition**,
leaving #117's lines verbatim.
