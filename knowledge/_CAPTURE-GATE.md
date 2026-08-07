# Capture gate report — mode: build
*Generated 2026-08-07 by `_capture_gate.py`. Scope: 82 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 16 found. READ BEFORE RE-DERIVING:
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
  ▸ ds-021-D1-82 — RULED #82-D1 (2026-08-02, Dave): WIRE measure_tokens() to the native counter AND re-stamp the LIVE budget claims in the SAME pass. Historical readings are NOT re-denominated -- re-denominating history is a false inscription.
      status: RULED #82-D1 (Dave) and ENACTED the same window. measure_tokens() returns (n,'real'); MEASURERS registers _capture_gate.py 'real'; GM size: stamp (45,869) and _CHAIN.md footer (10,830) re-stamped in real tokens and verified against the artefacts. History in notes/_GAUGE-LOG.md and the archived strata was NOT re-denominated -- that would be a false inscription.
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: _DECISION-HISTORY/2026-08-02-the-real-tier.md
      evidence: notes/2026-08-02-81-cross-instrument-gate-blast-radius.md
      evidence: knowledge/_capture_gate.py
  ▸ gauge-log-one-writer — RULED #96 (2026-08-05, Dave): ONE WRITER: only roll_2f creates gauge-log session sections; wraps never hand-write them. Collisions are marked exceptions by addition.
      status: RULED #96 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ ds-034 — RULED #108 (2026-08-06, Dave): On the button/primary scope question: measure the other 35 colliding token names BEFORE ruling scope — only 5 of 40 were value-checked (#108-D2). Extends his own #107-D1 'partition first, then rule' one level deeper. CORRECTED BY THIS SAME SESSION'S OWN FINDING (see ds-035): the sweep must test value agreement PER THEME, not globally — a global sweep would have manufactured roughly 35 false findings, because --pri-hover and --sec-hover genuinely resolve to different upstream tokens across .cn-button / .cn-modals / .cn-action-bar BY DESIGN under the four-theme architecture, not by drift. NOT STARTED — #109's first job.
      status: RULED #108 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: outputs/_FINDING-canon-pri-hover-brand-mono-fork-2026-08-06-v1.md
      evidence: outputs/_PARTITION-button-primary-2026-08-06-v1.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ ds-035 — RULED #108 (2026-08-06, Dave): STANDING CONSTRAINT, verbatim (#108-D3): "we have 4 themes, mono, legacy, console, and supercharge. they have a lot of overlap but they also diverge, especially the colour palette of legacy and the others, and the grey ramp for supercharge and the others. I just want the flexibility to have these themes and create more." Plus, explicitly NOT NOW: "I will also be revisiting the grey ramp for mono, i think we've calculated wrong." Governs every future cross-theme token-collision sweep: apparent divergence between themes on the same semantic token name is EXPECTED and must not be treated as a defect by default — see ds-034's corrected per-theme sweep spec.
      status: RULED #108 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: outputs/_FINDING-canon-pri-hover-brand-mono-fork-2026-08-06-v1.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s110-D1 — RULED #110 (2026-08-06, Dave): Open the four-phase boot-rent plan (ds-036); P1 delegated to a Sonnet sub. Chosen over P2-first, over cranking the design queue, and over research candidates 1+2.
      status: RULED #110 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: GOOD-MORNING.md
      evidence: _LIVE-STATE.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s110-D3 — RULED #110 (2026-08-06, Dave): P3 — gate the boot floor. Chosen over banking P2's small win and over closing the boot lane, taken AFTER the P1 finding re-priced P2 downward (five MCP servers already gone, remaining candidates worth only 2-4% of the 75,899 floor). Governs knowledge/_capture_gate.py::boot_constant_drift_check(), BOOT_DRIFT_BLOCKING and BOOT_DRIFT_WINDOW.
      status: RULED #110 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: GOOD-MORNING.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: notes/_GAUGE-LOG.md
  ▸ s111-D1 — RULED #111 (2026-08-06, Dave): BOOT_DRIFT_BLOCKING stays BLOCKING; the defect was the missing legal discharge, not the tier. Verbatim: 'Keep it BLOCKING, but the gate as built has no legal discharge — that's the defect, not the tier … the gate bites SILENCE, not reality … No session should ever be blocked with no honest way forward.' A declaration only discharges if its mean/constant/error-bar/delta MATCH what the gate independently computes; wrong figures fail louder than none.
      status: RULED #111, ENACTED #111
      ⚠ DO-NOT-RULE: the tier stays BLOCKING. The legal discharge form is the fix, not a warn/block change — do not re-open the tier question.
      evidence: GOOD-MORNING.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: notes/_GAUGE-LOG.md
  ▸ s111-D4 — RULED #111 (2026-08-06, Dave): DOFIRST_INDEX_TK_MAX reversed 800 → 700. Verbatim: 'A cap raised to clear its own gate is not a cap.' #110's wrap sub raised it 700→800 to clear its own gate; reversed. Index shaved to 681 tape, gate PASSES. Shave the index, never raise the ceiling to clear its own gate.
      status: RULED #111, ENACTED #111
      ⚠ DO-NOT-RULE: 700 is the ceiling. If the index exceeds it, shave the index — do not raise this number again.
      evidence: GOOD-MORNING.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s115-D1 — RULED #115 (2026-08-06, Dave): Open graph-engineering candidates 1 + 3 + the MARK-HALF of 2 now, deferring #115's titled lane (D5 checker redesign, D2 citation gate). Verbatim: 'no lets get these done now.'
      status: RULED #115, ENACTED #115 (9b47152, 6a16633)
      ⚠ Display-only by construction: no ranking change (3 queries x 2 doors byte-identical vs HEAD with marks stripped). DEMOTION is NOT part of this ruling. Deviation declared: steps 1+3 share one commit because the sandbox delete-guard blocks the mv-aside.
      evidence: commit 9b47152
      evidence: commit 6a16633
      evidence: notes/_briefs/2026-08-06-graph-candidates-pricing-brief.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s115-D2 — RULED #115 (2026-08-06, Dave): The mark observation window must be INSTRUMENTED, never human-remembered. Verbatim: 'so I should be looking out for these manually?... do I have to write these down on a postit or something??'
      status: RULED #115, ENACTED #115 (ce0cc7f) — the WINDOW is open, the verdict is not in
      ⚠ DEMOTION (pricing brief item 4) is NOT RULED and NOT SCHEDULED: it is decided on `_graph_edges.py --tally` evidence, and the ruling is Dave's. The mark's semantic: a result MENTIONS a superseded node; it is not itself dead.
      evidence: commit ce0cc7f
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: _DECISION-HISTORY/2026-08-06-115-graph-candidates-and-the-observation-window.md
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

