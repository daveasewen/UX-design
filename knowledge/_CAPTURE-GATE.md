# Capture gate report — mode: build
*Generated 2026-08-17 by `_capture_gate.py`. Scope: 146 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 8 found. READ BEFORE RE-DERIVING:
  ▸ chain-cut — RULED GM-D7-am / #33 (2026-07-28, Dave): _CHAIN.md is the WHOLE read chain. Everything else is retrieval, never a reading list. Do not open GOOD-MORNING.md to 'check'.
      status: ENACTED #33, held 7 consecutive sessions
      ⚠ _gen_chain.py iterates to a FIXED POINT - the footer states the size of the file containing it. Any unit change must re-converge.
      evidence: _DECISION-HISTORY/2026-07-28-cutting-the-eager-read-chain.md
  ▸ ds-021-D1-82 — RULED #82-D1 (2026-08-02, Dave): WIRE measure_tokens() to the native counter AND re-stamp the LIVE budget claims in the SAME pass. Historical readings are NOT re-denominated -- re-denominating history is a false inscription.
      status: RULED #82-D1 (Dave) and ENACTED the same window. measure_tokens() returns (n,'real'); MEASURERS registers _capture_gate.py 'real'; GM size: stamp (45,869) and _CHAIN.md footer (10,830) re-stamped in real tokens and verified against the artefacts. History in notes/_GAUGE-LOG.md and the archived strata was NOT re-denominated -- that would be a false inscription.
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: _DECISION-HISTORY/2026-08-02-the-real-tier.md
      evidence: notes/2026-08-02-81-cross-instrument-gate-blast-radius.md
      evidence: knowledge/_capture_gate.py
  ▸ gauge-log-one-writer — RULED #96 (2026-08-05, Dave): ONE WRITER: only roll_2f creates gauge-log session sections; wraps never hand-write them. Collisions are marked exceptions by addition.
      status: RULED #96 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ ds-025 — RULED #109 (2026-08-06, Dave): ds-025 item 1 (the boot floor) is RE-SCOPED, not closed (#109-D3). The boot TOTAL is now measured - 75,899 real (first turn 65,400 +/- 1,400, n=5, plus _CHAIN.md 10,499 additive at turn 2) against a previously published 30,499 +/- 8,000, a 45,400 under-report. That half is closed. Item 1 now means the DECOMPOSITION of the 56,308 first-turn remainder only (MEMORY.md's 8,470 is already split out and measured); it closes when the 56,308 is split, not before. Dave asked to understand the re-scope before ruling it, and approved the re-scope itself; he has NOT signed off the knowledge/_gauge_tokens.py code change line-by-line, so the code is ENACTED + UNRATIFIED, not a closed loop. Retires the false 'boot never measured in 36 sessions' wording at notes/_MEMENTO-DECISIONS.md:1297, :1399, :1562 (struck through at source, not deleted) and at GOOD-MORNING.md's header + DO-FIRST pointer.
      status: RULED #109 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: _DECISION-HISTORY/2026-08-06-109-boot-floor-measured.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: knowledge/_DS-IMPROVEMENTS.md
  ▸ d0802-P2b — RULED #76 (dream pass 4) (2026-08-02, Dave): GOOD-MORNING.md hardcoded chain figure (4,585 tape prose block) replaced with the chain_file_tk('.') pointer form the same file already uses.
      status: ENACTED #128 2026-08-08. `GOOD-MORNING.md:125` no longer carries a figure: the prose now points at `chain_file_tk('.')` and says the figure MOVES, the form the same file uses at :427.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P4 — RULED #76 (dream pass 4) (2026-08-02, Dave): consult-receipts stratum line carries the running 'Nth of M' count (~8 tape/wrap).
      status: ENACTED #128 2026-08-08. The running-count form is inscribed at the ONE copy of the consult-receipt form, `knowledge/_search_core.py` (the file the gate's probe imports): the stratum line carries `#N (Nth of M)`.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ s168-D3 — RULED #168 (2026-08-13, Dave): SUB-SPEND ACCOUNTING, OPTION 2 - Dave: 'I like both... lets do option 2'. (a) A gauge-log block MAY carry ONE optional line `subs <N> tokens (n=<count>)`. ABSENT IS LEGAL AND NEVER DEFAULTED. The word `job` is FORBIDDEN on that line - containment, not style: gen_dashboard.py's _JOB_RE sweeps the whole file and a `job`-spelled subs line would move an S/M/L band edge silently. Guarded by _capture_gate.py::gauge_log_subs_line, 12 arms, SUBS_LINE_BLOCKING=True - the TIER is a DECLARED CHOICE, not part of the ruling, and a downgrade is Dave's. Runbook section added at _RUNBOOK-capture-ritual.md step 2f. (b) EFFORT-SWITCH AGENT DEFINITIONS: .claude/agents/opus-deep.md (effort: max) and .claude/agents/opus-fast.md (effort: low). NOTE: they were NOT registered mid-session - first live use is #169.
      status: RULED #168 AND ENACTED IN-WINDOW for (a) - gate live and BLOCKING, runbook section written, first real subs line written by the #168 wrap. (b) BUILT NOT REGISTERED - agent defs exist on disk; first live use #169.
      evidence: chat #168 2026-08-13 (live) - Dave: 'I like both... lets do option 2'; FIRM
      evidence: knowledge/_capture_gate.py::gauge_log_subs_line - 12 arms, proven against _JOB_RE
      evidence: knowledge/_RUNBOOK-capture-ritual.md
  ▸ s186-D2 — RULED #186 (2026-08-16, Dave): DREAM-PASS BACKLOG SETTLED (Phase 1 sitting). Pass 6 P1-P4 PROMOTED as priced Phase 2 enactment rows: P1 re-checker counting the 21 frozen '#119 sweep' status strings at wrap (no bulk rewrite - that manufactures the CLAIMED class ADR-0016 forbids); P2 the verify-after-commit-dirties-tree fix; P3's two remaining stale Desktop-only lines in _RUNBOOK-git-commit.md amended by addition (the substance was already corrected #141; Desktop stays legal); P4 expiry stamp on the ledger's PAT line (~2026-11-06) + reword the refusal so the credential never transits chat (token scope stays Dave's security call, unproposed). P5 RULED: KEEP the --all-dirty hatch - disclosed at birth, echo-mitigated, no observed harm; the #128 open question closes as kept. Pass 7 P1 PROMOTED to Phase 2: liveness check of the four STANDING CARRY items FIRST, then fold into the fenced residual list; the two bare ordinals (GM:10, GM:438) are DELETED, never re-stamped. Also ratified in the same word: the W-17 and W-18 close conditions as written at #185; W-18's condition is satisfied by s186-D1 and W-18 closes.
      status: ruled
      evidence: chat #186 2026-08-16 (live) - Dave picked promote-all-four / keep / promote-to-Phase-2, then ratified the full readback including both close conditions: 'Firm - ratify all'
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

