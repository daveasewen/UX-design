# Capture gate report — mode: build
*Generated 2026-08-07 by `_capture_gate.py`. Scope: 81 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 7 found. READ BEFORE RE-DERIVING:
  ▸ gauge-refusal — RULED #79-D1 (2026-08-02, Dave): The gauge must REFUSE rather than guess. MeasurementRefused, paired with a handler that records refusal as a FAILURE — an unmeasurable floor is not a cleared floor.
      status: BUILT #80, mutation-tested x3
      ⚠ NOT SystemExit — count() is a library function inside a 39+-check gate and BaseException would slip _arm()'s except Exception. A precedent is a claim about a CALL SITE, not a repo.
      evidence: _DECISION-HISTORY/2026-08-02-the-79-dossier.md
  ▸ chain-cut — RULED GM-D7-am / #33 (2026-07-28, Dave): _CHAIN.md is the WHOLE read chain. Everything else is retrieval, never a reading list. Do not open GOOD-MORNING.md to 'check'.
      status: ENACTED #33, held 7 consecutive sessions
      ⚠ _gen_chain.py iterates to a FIXED POINT — the footer states the size of the file containing it. Any unit change must re-converge.
      evidence: _DECISION-HISTORY/2026-07-28-cutting-the-eager-read-chain.md
  ▸ ds-021-D1-82 — RULED #82-D1 (2026-08-02, Dave): WIRE measure_tokens() to the native counter AND re-stamp the LIVE budget claims in the SAME pass. Historical readings are NOT re-denominated -- re-denominating history is a false inscription.
      status: RULED #82-D1 (Dave) and ENACTED the same window. measure_tokens() returns (n,'real'); MEASURERS registers _capture_gate.py 'real'; GM size: stamp (45,869) and _CHAIN.md footer (10,830) re-stamped in real tokens and verified against the artefacts. History in notes/_GAUGE-LOG.md and the archived strata was NOT re-denominated -- that would be a false inscription.
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: _DECISION-HISTORY/2026-08-02-the-real-tier.md
      evidence: notes/2026-08-02-81-cross-instrument-gate-blast-radius.md
      evidence: knowledge/_capture_gate.py
  ▸ ds-025 — RULED #109 (2026-08-06, Dave): ds-025 item 1 (the boot floor) is RE-SCOPED, not closed (#109-D3). The boot TOTAL is now measured — 75,899 real (first turn 65,400 ± 1,400, n=5, plus _CHAIN.md 10,499 additive at turn 2) against a previously published 30,499 ± 8,000, a 45,400 under-report. That half is closed. Item 1 now means the DECOMPOSITION of the 56,308 first-turn remainder only (MEMORY.md's 8,470 is already split out and measured); it closes when the 56,308 is split, not before. Dave asked to understand the re-scope before ruling it, and approved the re-scope itself; he has NOT signed off the knowledge/_gauge_tokens.py code change line-by-line, so the code is ENACTED + UNRATIFIED, not a closed loop. Retires the false 'boot never measured in 36 sessions' wording at notes/_MEMENTO-DECISIONS.md:1297, :1399, :1562 (struck through at source, not deleted) and at GOOD-MORNING.md's header + DO-FIRST pointer.
      status: RULED #109 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: _DECISION-HISTORY/2026-08-06-109-boot-floor-measured.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: knowledge/_DS-IMPROVEMENTS.md
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
  ▸ s119-D1 — RULED #119 (2026-08-07, Dave): Type-composites gate wired at tier (b) SHRINK-ONLY RATCHET. Enforce today against any NEW violation; existing debt (1,101, MEASURED at wiring 2026-08-07, not copied from _HANDOFF-118) declared in _type_ratchet.json and may only shrink. Chosen over (a) BLOCKING-now, with the risk named unprompted and accepted: a baseline set to today's count has the shape of 'a cap raised to clear its own gate'; the claimed difference is shrink-only + declared-as-debt.
      status: RULED + ENACTED #119 — ratchet wired, FAIL clause mutation-tested (baseline 1100 vs count 1101 fires)
      ⚠ The ratchet PASS line must keep saying DEBT, not pass. If the baseline is ever edited upward, that is the cap-raised-to-clear-its-own-gate defect by definition.
      evidence: _HANDOFF-118-the-wiring-seam.md
      evidence: knowledge/_type_ratchet.json
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

