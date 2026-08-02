# Capture gate report — mode: build
*Generated 2026-08-02 by `_capture_gate.py`. Scope: 61 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_capture_gate.py` counts in cl100k and cannot name a REAL tier. ⛔ THE ds-021 DEFECT ITSELF, and the reason this gate exists. measure_tokens() can return only 'tiktoken cl100k_base' or a bytes ESTIMATE — so measurement_degraded() asks 'is this an estimate?' and cl100k answers 'no, healthy'. THE VOCABULARY HAS NO WORD FOR REAL (#80's root cause, confirmed at source #81). Fixing it is a CODE change and it moves the GM size stamps, ds-025's floor and the amber line — priced, not smuggled into this window.
- ds-021 (C) DECLARED GAP — `knowledge/_checkin.py` counts in cl100k and cannot name a REAL tier. Reports THROUGHPUT in cl100k and says so in its own footer ('⚠ UNIT tape/cl100k. D1 rules this an UNVERIFIED proxy'). Declared, which is why it warns rather than fails.
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 6 found. READ BEFORE RE-DERIVING:
  ▸ ds-021 — RULED #54 (2026-07-30, Dave): ONE unit: REAL Claude tokens. cl100k/tiktoken is a LABELLED estimator and is 'never a unit a cap is stated in'.
      status: RULED #54, ENACTMENT SHAPE (C) ruled #81-D1, enactment IN PROGRESS #81
      ⚠ The three homes were declared UNTOUCHED at #54 and were still untouched at #80. Do not re-derive the ratio; it is measured and ruled.
      evidence: notes/_MEMENTO-DECISIONS.md:1716-1785
      evidence: _DECISION-HISTORY/2026-07-30-the-gauge-re-denomination.md
      evidence: notes/_GAUGE-LOG.md:461
      evidence: knowledge/_DS-IMPROVEMENTS.md:1422
  ▸ ds-021-C — RULED #81-D1 (2026-08-02, Dave): Enactment shape (C) — a CROSS-INSTRUMENT gate — chosen over (A) unit-as-type, (B) one authority, (D) calibrate-and-keep. tape/bill machinery KEPT as labelled legacy, not retired.
      status: BUILT #81
      ⚠ Dave's condition, verbatim: 'be careful, i want rigorousness, check for peripheral effects.' The gate checks VOCABULARY, never the live reading — demanding a REAL reading would refuse an honest offline estimate.
      evidence: notes/2026-08-02-81-cross-instrument-gate-blast-radius.md
  ▸ ds-023 — RULED #31/#34 (2026-07-28, Dave): Pre-flight ceiling: fill + job + wrap < 45 (45 itself FAILS). In-flight stop line = 60 minus the priced wrap. 60 is where the wrap has FINISHED.
      status: ENACTED #34
      ⚠ The escape hatch is the literal string 'RESERVE SPEND — forked to Dave'. Matched literally on purpose: a receipt producible by accident is not a receipt.
      evidence: knowledge/_RUNBOOK-context-gauge.md:178
  ▸ gauge-band — RULED #56 (2026-07-31, Dave): Budget in ABSOLUTE real tokens: amber 160,000 · working 200,000 (Dave's) · hard 256,000 (sourced). The 45/60/63 percentage band was REPLACED, not converted.
      status: RULED #56; the % path is DORMANT in code, retire-or-pin FORKED TO DAVE and still open
      ⚠ Read the band table from the runbook; never recall it. It has been misquoted from memory twice in one day.
      evidence: knowledge/_RUNBOOK-context-gauge.md:27
  ▸ gauge-refusal — RULED #79-D1 (2026-08-02, Dave): The gauge must REFUSE rather than guess. MeasurementRefused, paired with a handler that records refusal as a FAILURE — an unmeasurable floor is not a cleared floor.
      status: BUILT #80, mutation-tested x3
      ⚠ NOT SystemExit — count() is a library function inside a 39+-check gate and BaseException would slip _arm()'s except Exception. A precedent is a claim about a CALL SITE, not a repo.
      evidence: _DECISION-HISTORY/2026-08-02-the-79-dossier.md
  ▸ derivation-governance — RULED ADR-0016 era (2026-07-29, Dave): The engine never derives-and-promotes. Promotion is Dave's alone; a threshold reached must FORK TO DAVE, never self-apply.
      status: STANDING
      ⚠ This is why ratio_status() must SAY something at n>=4 rather than silently firming the constant.
      evidence: knowledge/_DS-IMPROVEMENTS.md
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

