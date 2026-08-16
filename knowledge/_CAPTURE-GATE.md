# Capture gate report — mode: build
*Generated 2026-08-16 by `_capture_gate.py`. Scope: 145 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 20 found. READ BEFORE RE-DERIVING:
  ▸ ds-021 — RULED #54 (2026-07-30, Dave): ONE unit: REAL Claude tokens. cl100k/tiktoken is a LABELLED estimator and is 'never a unit a cap is stated in'.
      status: RULED #54, ENACTMENT SHAPE (C) ruled #81-D1, enactment IN PROGRESS #81
      ⚠ The three homes were declared UNTOUCHED at #54 and were still untouched at #80. Do not re-derive the ratio; it is measured and ruled.
      evidence: notes/_MEMENTO-DECISIONS.md:1782 — COLLAPSE TO REAL TOKENS, KEEP THE PRICE/BUDGET ANALOGY
      evidence: _DECISION-HISTORY/2026-07-30-the-gauge-re-denomination.md
      evidence: notes/_GAUGE-LOG.md:461 — aggregate over five registers
      evidence: knowledge/_DS-IMPROVEMENTS.md:1424 — observed on two files in one
  ▸ ds-021-C — RULED #81-D1 (2026-08-02, Dave): Enactment shape (C) - a CROSS-INSTRUMENT gate - chosen over (A) unit-as-type, (B) one authority, (D) calibrate-and-keep. tape/bill machinery KEPT as labelled legacy, not retired.
      status: BUILT #81
      ⚠ Dave's condition, verbatim: 'be careful, i want rigorousness, check for peripheral effects.' The gate checks VOCABULARY, never the live reading - demanding a REAL reading would refuse an honest offline estimate.
      evidence: notes/2026-08-02-81-cross-instrument-gate-blast-radius.md
  ▸ ds-023 — RULED #31/#34 (2026-07-28, Dave): Pre-flight ceiling: fill + job + wrap < 45 (45 itself FAILS). In-flight stop line = 60 minus the priced wrap. 60 is where the wrap has FINISHED.
      status: ENACTED #34
      ⚠ The escape hatch is the literal string 'RESERVE SPEND - forked to Dave'. Matched literally on purpose: a receipt producible by accident is not a receipt.
      evidence: knowledge/_RUNBOOK-context-gauge.md:217 — THE CEILING AND THE STOP LINE
  ▸ gauge-band — RULED #56 (2026-07-31, Dave): Budget in ABSOLUTE real tokens: amber 160,000 - working 200,000 (Dave's) - hard 256,000 (sourced). The 45/60/63 percentage band was REPLACED, not converted.
      status: RULED #56; the % path is DORMANT in code, retire-or-pin FORKED TO DAVE and still open
      ⚠ Read the band table from the runbook; never recall it. It has been misquoted from memory twice in one day.
      evidence: knowledge/_RUNBOOK-context-gauge.md:29 — RULED BY DAVE #56, and it retires the percentage stamp
  ▸ gauge-refusal — RULED #79-D1 (2026-08-02, Dave): The gauge must REFUSE rather than guess. MeasurementRefused, paired with a handler that records refusal as a FAILURE - an unmeasurable floor is not a cleared floor.
      status: BUILT #80, mutation-tested x3
      ⚠ NOT SystemExit - count() is a library function inside a 39+-check gate and BaseException would slip _arm()'s except Exception. A precedent is a claim about a CALL SITE, not a repo.
      evidence: _DECISION-HISTORY/2026-08-02-the-79-dossier.md
  ▸ derivation-governance — RULED ADR-0016 era (2026-07-29, Dave): The engine never derives-and-promotes. Promotion is Dave's alone; a threshold reached must FORK TO DAVE, never self-apply.
      status: STANDING
      ⚠ This is why ratio_status() must SAY something at n>=4 rather than silently firming the constant.
      evidence: knowledge/_DS-IMPROVEMENTS.md
  ▸ ds-021-D1-82 — RULED #82-D1 (2026-08-02, Dave): WIRE measure_tokens() to the native counter AND re-stamp the LIVE budget claims in the SAME pass. Historical readings are NOT re-denominated -- re-denominating history is a false inscription.
      status: RULED #82-D1 (Dave) and ENACTED the same window. measure_tokens() returns (n,'real'); MEASURERS registers _capture_gate.py 'real'; GM size: stamp (45,869) and _CHAIN.md footer (10,830) re-stamped in real tokens and verified against the artefacts. History in notes/_GAUGE-LOG.md and the archived strata was NOT re-denominated -- that would be a false inscription.
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: _DECISION-HISTORY/2026-08-02-the-real-tier.md
      evidence: notes/2026-08-02-81-cross-instrument-gate-blast-radius.md
      evidence: knowledge/_capture_gate.py
  ▸ gauge-log-one-writer — RULED #96 (2026-08-05, Dave): ONE WRITER: only roll_2f creates gauge-log session sections; wraps never hand-write them. Collisions are marked exceptions by addition.
      status: RULED #96 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s110-D1 — RULED #110 (2026-08-06, Dave): Open the four-phase boot-rent plan (ds-036); P1 delegated to a Sonnet sub. Chosen over P2-first, over cranking the design queue, and over research candidates 1+2.
      status: RULED #110 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: GOOD-MORNING.md
      evidence: _LIVE-STATE.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s110-D3 — RULED #110 (2026-08-06, Dave): P3 - gate the boot floor. Chosen over banking P2's small win and over closing the boot lane, taken AFTER the P1 finding re-priced P2 downward (five MCP servers already gone, remaining candidates worth only 2-4% of the 75,899 floor). Governs knowledge/_capture_gate.py::boot_constant_drift_check(), BOOT_DRIFT_BLOCKING and BOOT_DRIFT_WINDOW.
      status: RULED #110 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: GOOD-MORNING.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: notes/_GAUGE-LOG.md
  ▸ s111-D1 — RULED #111 (2026-08-06, Dave): BOOT_DRIFT_BLOCKING stays BLOCKING; the defect was the missing legal discharge, not the tier. Verbatim: 'Keep it BLOCKING, but the gate as built has no legal discharge - that's the defect, not the tier ... the gate bites SILENCE, not reality ... No session should ever be blocked with no honest way forward.' A declaration only discharges if its mean/constant/error-bar/delta MATCH what the gate independently computes; wrong figures fail louder than none.
      status: RULED #111, ENACTED #111
      ⚠ DO-NOT-RULE: the tier stays BLOCKING. The legal discharge form is the fix, not a warn/block change - do not re-open the tier question.
      evidence: GOOD-MORNING.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: notes/_GAUGE-LOG.md
  ▸ s111-D4 — RULED #111 (2026-08-06, Dave): DOFIRST_INDEX_TK_MAX reversed 800 -> 700. Verbatim: 'A cap raised to clear its own gate is not a cap.' #110's wrap sub raised it 700->800 to clear its own gate; reversed. Index shaved to 681 tape, gate PASSES. Shave the index, never raise the ceiling to clear its own gate.
      status: RULED #111, ENACTED #111
      ⚠ DO-NOT-RULE: 700 is the ceiling. If the index exceeds it, shave the index - do not raise this number again.
      evidence: GOOD-MORNING.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ d0802-P2a — RULED #76 (dream pass 4) (2026-08-02, Dave): c_block comparison branch added to _capture_gate.py chain check (STILL ADVISORY; arming/re-dialling/retiring the tier stays Dave's word alone).
      status: ENACTED #128 2026-08-08. `knowledge/_capture_gate.py` gained the `c_block` comparison branch (`elif bill_of(chain_file) > bill_of(c_block)`), STILL ADVISORY and still a WARN - arming/re-dialling/retiring the tier remains Dave's word alone.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P3 — RULED #76 (dream pass 4) (2026-08-02, Dave): _RUNBOOK-capture-ritual.md:89 amended to carry #28's ruling: next-title at top; rename delivered to CHAT only. Rename half deliberately not gated.
      status: ENACTED #128 2026-08-08. `knowledge/_RUNBOOK-capture-ritual.md:89` now orders the NEXT SESSION TITLE only, and carries #28's amendment inline: the retrospective rename is delivered in CHAT at wrap and never written into GOOD-MORNING.md.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P7 — RULED #76 (dream pass 4) (2026-08-02, Dave): Declare-LAST residual clause: when 2c/2d/2f are skipped, the residual must state the size: stamp is therefore the prior session's and by roughly how much the artefact moved. Structural; survives its dead motivating receipt (P7 DEAD-AND-INVERTED, proposal untouched).
      status: ENACTED #128 2026-08-08. The declare-LAST clause is inscribed at the size-stamp spec in `knowledge/_RUNBOOK-capture-ritual.md`: when 2c/2d/2f are skipped the residual must state the SIZE of the skip - that the stamp is #N-1's and roughly how far the artefact has moved. NO GATE.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ s161-D4 — RULED #161 (2026-08-12, Dave): THE STALE-TOP-ITEM FENCE, BLOCK NOT WARN. A wrap may not certify a 'next top item' (or equivalent owed-work claim) that cites a ruling id whose _rulings.json status already says ENACTED - the #159/#160 defect that carried 's142-D1 wave enactment owed' two sessions past its fact, refuted the whole time by the store the wrap already parses. Conductor recommended block-not-warn (a warn under wrap heat is a warn nobody reads) with a bite test proving the gate can fail, driven on the real #160 wrap text as the red fixture. Dave: 'okay do it', after '2 sessions carried the wrong information, this is a waste of time'.
      status: RULED #161. Enactment delegated same session; conductor replays the gate in-window.
      evidence: chat #161 2026-08-12 (live) - Dave verbatim 'okay do it' on the read-back naming block-not-warn + bite test
      evidence: _DECISION-HISTORY/2026-08-12-160-the-nine-that-were-never-values.md (line 90, the false 'owed' claim) vs knowledge/_rulings.json (s142-D1 status: enacted #143)
  ▸ s161-D1 — RULED #161 (2026-08-12, Dave): G8 CLOSED - RETIRE COMPLETELY. The dormant % band 45/60/63 (BAND_FLOOR/HARD_STOP/MARKED_MAX) stays retired; this CONFIRMS #74-D3 rather than reversing it. Context: Dave first answered 'Pin' from the staged batch; the conductor surfaced that enforcement was already RETIRED at #74-D3 by his own option-select (the G8 state item, opened #86, pointed at retired residue) and gave the owed explanation (the band graded window fill as a %; its purpose carries on in the real-token path amber 160K / working 200K / hard 256K). Dave then ruled, verbatim: 'G8 retire completely'. The ruling history stays preserved per the #74 stratum (notes/_MEMENTO-DECISIONS.md sections 36 and 74); the G8 item closes as already-ruled-retired, now confirmed.
      status: RULED #161 after read-back; closes G8. No code change owed - enforcement was already retired; the state item closes.
      evidence: chat #161 2026-08-12 (live) - staged batch answer 'Pin, but lets return to this because i need an explanation for this', conductor read-back surfacing #74-D3, then Dave verbatim 'G8 retire completely'
      evidence: knowledge/_capture_gate.py:125-137 (the retirement comment block, #74-D3)
  ▸ s188-D1 — RULED #188 (2026-08-16, Dave): PASS-8 P1 RULED: THE GRADING UNIT IS THE HOOK FILE. _gardener.py's grader reads the memory hook FILE (index-line fallback permitted, file first), aligning the grader with the s182-D1 authoring convention already in force. The index stays lean - no proof-tokens required in MEMORY.md lines (boot rent stays flat). CONSEQUENCE ACCEPTED IN THE SAME WORD: the 109-of-122 and 50-of-57 UNPROVABLE figures were measured on the wrong text; they are re-measured after the grader change and the B3 return-with-numbers restarts its count on the honest figures. BUILD QUEUED to #189, not built at #188.
      status: ruled
      evidence: chat #188 2026-08-16 (live) - implications laid out (grade the file / grade the line / both); Dave: '1. Grade the file (your recommendation)'
  ▸ s188-D2 — RULED #188 (2026-08-16, Dave): PASS-8 P2 RULED: NARROW RETRACTION CARVE-OUT, RECEIPT REQUIRED. The 2c carry rule's 'AGES +1, WORDING UNCHANGED' invariant gains exactly one exit: a carried claim's wording may change ONLY to record a retraction, and the edit MUST cite its receipt (the run or commit that proved the claim false), the same way a repo claim cites git log. An edit without a receipt token is refused by the carry gate exactly as today. The carve-out is mutation-tested like any gate before it is trusted. BUILD QUEUED to #189, not built at #188. Pass-8 P3/P4/P5 remain FLOATED, carried to #189 undecided.
      status: ruled
      evidence: chat #188 2026-08-16 (live) - carve-out vs keep-frozen vs drop-invariant laid out with the twice-carried retracted claim as the driving case; Dave: '2. same again, your recommendation - narrow carve-out, receipt required'
  ▸ s188-D3 — RULED #188 (2026-08-16, Dave): SUPERSESSION, EXPLICIT: s188-D1 (grader reads the hook FILE) SUPERSEDES the P1 clause of s183-D1 (the light version: index-line grading + companion count + refusal-string fix), which is RETIRED. s188-D2 (receipt-required retraction carve-out) stands as a STRENGTHENING AMENDMENT to s183-D1's P2 clause, not a reversal. Dave's word: 'I just want the most robust version of this so we don't have to revisit it, the point behind all this is you have full spectrum context, with as little failures as possible.' s183-D1's P3/P4/P5 clauses are UNTOUCHED and remain in force. FINDING RECORDED IN THE SAME WORD: the #187 chain asserted pass-8 P1-P5 were floated/unruled while s183-D1 had held their promotion for four sessions; the conductor believed the chain over the rulings store and re-put settled rulings as options - the retrieval-default class. The rulings store is the authority on 'was this ruled'; the chain is not.
      status: ruled
      evidence: chat #188 2026-08-16 (live) - the s183-D1/s188-D1 delta was asserted to Dave plainly and he picked the robust version
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

