# Capture gate report — mode: build
*Generated 2026-08-08 by `_capture_gate.py`. Scope: 92 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 15 found. READ BEFORE RE-DERIVING:
  ▸ ds-021 — RULED #54 (2026-07-30, Dave): ONE unit: REAL Claude tokens. cl100k/tiktoken is a LABELLED estimator and is 'never a unit a cap is stated in'.
      status: RULED #54, ENACTMENT SHAPE (C) ruled #81-D1, enactment IN PROGRESS #81
      ⚠ The three homes were declared UNTOUCHED at #54 and were still untouched at #80. Do not re-derive the ratio; it is measured and ruled.
      evidence: notes/_MEMENTO-DECISIONS.md:1782 — COLLAPSE TO REAL TOKENS, KEEP THE PRICE/BUDGET ANALOGY
      evidence: _DECISION-HISTORY/2026-07-30-the-gauge-re-denomination.md
      evidence: notes/_GAUGE-LOG.md:461 — aggregate over five registers
      evidence: knowledge/_DS-IMPROVEMENTS.md:1422 — observed on two files in one
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
  ▸ s115-D2 — RULED #115 (2026-08-06, Dave): The mark observation window must be INSTRUMENTED, never human-remembered. Verbatim: 'so I should be looking out for these manually?... do I have to write these down on a postit or something??'
      status: RULED #115, ENACTED #115 (ce0cc7f) - the WINDOW is open, the verdict is not in
      ⚠ DEMOTION (pricing brief item 4) is NOT RULED and NOT SCHEDULED: it is decided on `_graph_edges.py --tally` evidence, and the ruling is Dave's. The mark's semantic: a result MENTIONS a superseded node; it is not itself dead.
      evidence: commit ce0cc7f
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: _DECISION-HISTORY/2026-08-06-115-graph-candidates-and-the-observation-window.md
  ▸ d0802-P2a — RULED #76 (dream pass 4) (2026-08-02, Dave): c_block comparison branch added to _capture_gate.py chain check (STILL ADVISORY; arming/re-dialling/retiring the tier stays Dave's word alone).
      status: ENACTED #128 2026-08-08. `knowledge/_capture_gate.py` gained the `c_block` comparison branch (`elif bill_of(chain_file) > bill_of(c_block)`), STILL ADVISORY and still a WARN - arming/re-dialling/retiring the tier remains Dave's word alone.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P5 — RULED #76 (dream pass 4) (2026-08-02, Dave): _git_commit.sh takes explicit paths so --reconciled means what it says (option (a)); git add -A retired as the only staging call.
      status: ENACTED #128 2026-08-08. `knowledge/_git_commit.sh` stages EXPLICIT PATHS named on the command line; `git add -A` is retired. A `--all-dirty` escape hatch echoes every path it stages. Enacted together with seam (2): `--cleanup=verbatim` and a post-commit subject-identity assert that FAILS LOUD.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

