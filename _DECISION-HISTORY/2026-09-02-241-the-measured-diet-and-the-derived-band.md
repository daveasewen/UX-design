# #241 — the diet measured, the band derived, and a headline that was counted once and attributed twice

```
provenance: 241 · 2026-09-02
status: observed
```

*Both-way links: spine entry `_LIVE-STATE.md` § ⏱ LATEST DELTA #241 · record `GOOD-MORNING.md` § ★ LATEST
#241 · ledger `knowledge/_rulings.json` § `s241-D1` · `s241-D2` · carries `_CARRIES.md`
§ `## residual → #242` · brief `notes/_briefs/2026-09-02-241-delegated-wrap-brief.md` · lane reports
`notes/_subreports/2026-09-02-241-lane-B-boot-band.md` · `…-lane-D-ritual-diet.md` · `…-lane-E-diet-apply.md`.*

⚠ **Scope, stated first so nothing here is read as more than it is.** This dossier was written at the WRAP
SUB'S seat from the conductor's brief, the repo, the two ruling records and the three filed lane reports.
Dave's words are **chat testimony relayed by the brief and quoted inside each ruling's `says` field** — they
are attributed, never asserted, and they are not repo-verifiable. Everything mechanical below was re-driven
at this seat or is quoted from the report that drove it, and it says which.

---

## 1. The measurement that #240 could only promise

#240 ended with an UNPROVEN in its own report: *"the roster diet's effect on boot — no post-diet first-turn
reading exists. Price to prove: one reading at #241's opener."* That reading is **69,092 real**, taken at the
first turn from `message.usage` through `knowledge/_checkin.py`, and re-read first-hand at this wrap seat
where it agrees to the token.

Against #240's **76,138** it is **−7,046**.

The important part is what the number is NOT. It is one figure covering two acts — Dave removing the Figma
connector and switching computer use off, and the `MEMORY.md` compaction from 21,064 to 12,454 bytes. **One
reading cannot decompose into two causes**, so the attribution stays exactly where #240 left it: a claim
[[feedback-measuring-tool-must-not-guess]]. What changed is that the TOTAL stopped being a prediction.

This matters more than the seven thousand tokens, because the whole `s228-D6` sequence — *shrink first, then
re-base* — was staged on a measurement nobody had yet taken. It has now been taken, and the ruling that
depended on it could be made the same morning.

## 2. Why the ceiling is 70,000 and not 69,092

Dave was offered three options: the exact reading (69,092), the rounded one (70,000, ~900 headroom for
turn-to-turn noise), or holding the ceiling open for a second post-diet boot. He took the rounded one, and
`s241-D1` records that choice with its reasoning intact.

The dead end worth recording is the third option. Waiting for a second boot would have been the cautious
move, and it was rejected for a reason that is structural rather than impatient: `s240-D2` had already ruled
the ceiling **shrink-only**. A shrink-only number set slightly high can always come down; a number never set
at all leaves `boot-drift`'s ceiling arm inert for another session, which is the state the ruling exists to
end. Caution about the value was cheap; caution about setting one was not.

⚠ **And the sentence that came with it is the session's real hinge:** *"2 is fine, but I still think this is
getting excessive :("*. It is quoted in `s241-D1`'s `says` field and **deliberately not inscribed as a
ruling of its own** — a complaint is not a ruling, and turning one into a ruling would be inventing his
word. But it is what redirected the session: everything from lane D onward exists because of it.

## 3. Two lanes were launched from a complaint, not from a plan

The conductor's answer to *"this is getting excessive"* was to ask what the ritual layer actually costs, and
Dave's answer was *"both, go for it"* — build the derived band AND diet the ritual layer.

**Lane B (`W-386`)** enacted `s240-D1`, `s240-D2` and `s241-D1` in one motion. `BOOT_FIRSTTURN_TK` and
`BOOT_FIRSTTURN_ERR` are DELETED rather than commented out; the band is computed at check time by
`derived_boot_band()`; `BOOT_CEILING_TK = 70_000` is the single typed number left, and it is shrink-only.

Two things inside that lane deserve to survive the session:

- **The #240 parser finding was not a duplicate-line bug.** It was **ordinal mis-attribution**: the parser
  took the first `#N` anywhere on the line, so #239's reading — which restates its own boot and cites #238
  in a later clause — was filed under #238, and eleven `Context gauge at authoring:` lines that cite
  `#56-D1` were all filed under session 56, each clobbering the last. The fix takes the ordinal from label
  POSITION or from the enclosing stratum, and its blast radius was **measured, not asserted**: 105 readings
  parsed before and after, 0 gained, 0 lost, **14 re-attributed**.
- **The red line's multiplier was forced by the ruling, not chosen.** `s240-D1` has two clauses — a step
  change goes red, slow drift never needs a re-base — and at 1σ the second is false: a linear ramp puts the
  newest reading at 1.39σ, which reinstates the treadmill the ruling ends. `BOOT_BAND_SIGMA = 2.0` satisfies
  both. ⛔ **It is ruling-shaped and was NOT inscribed** — `s240-D1` names no multiplier, so the number is
  Dave's, and it is carried.

## 4. The correction: a figure counted once and attributed twice

**Lane D** surveyed 33 ritual components and measured 24 of them. Its headline recommendation, D1, was
priced at *"≥22,400 tk/session, the single most expensive thing the process layer does"*.

**It was wrong, and lane E caught it by re-driving the probe rather than trusting the table.** Lane D's own
measurement was of `_capture_gate.run(mode="wrap")` — the wrap-gate dump. The check-in does not call that;
it calls `run(rehearse=True)`, which has printed terse since before HEAD: **3 lines, 171 tape**, measured on
captured stdout. The 7,534-tape figure is real, but it belongs to `--wrap`, which is **S7's** subject. So the
package's headline saving was counted once and attributed twice, and the honest floor for the package as
built is **≈4,100 tape/session**, not ~27,300.

The conductor had already relayed the inflated 27–42K figure to Dave, and **corrected it in chat**.

⛔ **Then the correction met a write-once record.** `s241-D2`'s `ruled` text carries the inflated estimate,
and a ruling is not edited after inscription [[write-once-principle-floated-192]]. The correction is
therefore inscribed in the two places that CAN carry it — the ⏱ LATEST DELTA and this dossier — and the
store was not touched. That asymmetry is uncomfortable and it is the right way round: a ledger whose text
can be improved after the fact is a ledger nobody can cite.

★ **The generalisable defect is not the arithmetic. It is that a survey's figure did not name which
mode/command it measured.** `7,534 tape` and `171 tape` are both true statements about "the gate"; only one
of them is about the thing the recommendation proposed to cut. That is carried to #242 as a rule for
surveys, not as a complaint about lane D.

## 5. What the diet actually bought, and where the next cut is

**Lane E applied all seven items** and measured each rather than claiming the package total:

- **D2** is the real saving: `_CHAIN.md` **11,319 → 9,030 tape**, the 461 bare ids replaced by one line that
  keeps every generated count. That is 2,289 tape off **every cold session's first read**, permanently.
- **S7** is the other: the wrap gate's WARN block **1,793 → 380 tape** per run, and 59 wrap-open runs were
  logged on 2026-09-02 alone.
- **D3** removed the 119-sweep expiry nag (107 tape per check-in) and deliberately did **not** retire the
  sweep — that is still Dave's.
- **D4** retired `_measure_tokenizer.py` after probing for importers and finding **zero**.
- **S1 and S5 buy no tokens at all.** S1 is a cap on the NEXT banner; S5 is a correctness gate that costs
  135 tape a wrap to keep the boot band honest. They are in the package because the package was about the
  record's trustworthiness as much as its size.

⚠ **And the honest closing measurement inverts the target:** of 15,955 tape of `--wrap` stdout, the NOTE
block is 15,469 (97%) and **the trigger index alone is 10,294 (65%)**. The warns that S7 was aimed at were
1,793. The next cut is `_governs`'s render, and it is not in this package.

## 6. Two consequences the next session inherits rather than discovers

1. **S1's cap binds THIS wrap and no other has ever met it.** The #240 banner is 3,353 tape over 13
   substantive lines against 10 lines / 1,200 tape. ⚠ The gate can enforce LENGTH and cannot enforce
   HONESTY: a banner cut by dropping its declared gaps passes exactly as well as one cut by writing tighter.
   The cap's own message says so, and it is the reason the ⏱ LATEST DELTA is now the declared sole home for
   gauge / declared-skip / not-done detail.
2. **S5 can block a wrap over a line a previous session wrote.** It binds strata from #241 on, because 18
   ordinals in the live gauge log already double-count their boot and a retroactive rule could never pass
   [[gate-cannot-pass-in-one-environment]].

## 7. What is still open, and whose it is

1. **`BOOT_BAND_SIGMA = 2.0`** — measured, argued, not ruled. Dave's.
2. **`W-387`, the polarity receipt** — `s240-D3` is ruled and unbuilt, and **V2 stays gated on it**.
3. **Diet S2/S3/S4/S6** — open, each with lane D's measured cost beside it. Dave's.
4. **The `s203-D1` CI read-back** — `a09a3ea` and this wrap's push, route capped at the run page plus one JS
   grep, because #239 measured the uncapped route at ≈55K of conductor FILL.
5. **The 119 sweep's retirement**, and one re-run owed before it.
6. **The inherited M10 selftest failure** — a 24-line fixture against a restamped `CHAIN_BUDGET_TK`; it fails
   identically on HEAD and is not this session's.
7. **`notes/_dream/_MEMORY-GRADES.json` entry 40** now names a path D4 deleted. It is a path-resolution
   grade, it will drop at the next dream pass, and **no agent may edit the memory store to make that
   consequence disappear.**

⛔ **Nothing above was ruled at the wrap seat.** Two rulings were inscribed at the conductor's seat before it,
and not one word of either was re-worded here.
