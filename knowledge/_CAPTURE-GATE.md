# Capture gate report — mode: build
*Generated 2026-08-15 by `_capture_gate.py`. Scope: 138 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 22 found. READ BEFORE RE-DERIVING:
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
  ▸ chain-cut — RULED GM-D7-am / #33 (2026-07-28, Dave): _CHAIN.md is the WHOLE read chain. Everything else is retrieval, never a reading list. Do not open GOOD-MORNING.md to 'check'.
      status: ENACTED #33, held 7 consecutive sessions
      ⚠ _gen_chain.py iterates to a FIXED POINT - the footer states the size of the file containing it. Any unit change must re-converge.
      evidence: _DECISION-HISTORY/2026-07-28-cutting-the-eager-read-chain.md
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
  ▸ ds-025 — RULED #109 (2026-08-06, Dave): ds-025 item 1 (the boot floor) is RE-SCOPED, not closed (#109-D3). The boot TOTAL is now measured - 75,899 real (first turn 65,400 +/- 1,400, n=5, plus _CHAIN.md 10,499 additive at turn 2) against a previously published 30,499 +/- 8,000, a 45,400 under-report. That half is closed. Item 1 now means the DECOMPOSITION of the 56,308 first-turn remainder only (MEMORY.md's 8,470 is already split out and measured); it closes when the 56,308 is split, not before. Dave asked to understand the re-scope before ruling it, and approved the re-scope itself; he has NOT signed off the knowledge/_gauge_tokens.py code change line-by-line, so the code is ENACTED + UNRATIFIED, not a closed loop. Retires the false 'boot never measured in 36 sessions' wording at notes/_MEMENTO-DECISIONS.md:1297, :1399, :1562 (struck through at source, not deleted) and at GOOD-MORNING.md's header + DO-FIRST pointer.
      status: RULED #109 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: _DECISION-HISTORY/2026-08-06-109-boot-floor-measured.md
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: knowledge/_DS-IMPROVEMENTS.md
  ▸ ds-036 — RULED #109 (2026-08-06, Dave): STANDING CONSTRAINT, verbatim (#109-D4): "Lets fix this properly, no patches no sticking plasters." Governs the four-phase #110 follow-on to the boot-floor finding: P1 split the 56,308 first-turn remainder by tokenising what is actually on disk (skill frontmatter, CLAUDE.md, plugin manifests), Cowork system prompt falls out as the residual by subtraction - collapses from a multi-session throwaway-boot project to a one-pass morning; P2 cut unearning boot rent - seven MCP servers load unauthenticated (Asana, Atlassian, Intercom, Linear, Notion, Slack, Figma) plus a duplicate second Figma server, each drop needs Dave's call + a re-measure; P3 gate it - a boot-ceiling gate that fails loud on drift, the mechanical form of this ruling; P4 the _CHAIN.md corpus-trim option, correctly priced at 14% of the floor. Priced and awaiting Dave's confirm to open #110, not yet running.
      status: RULED #109 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: _DECISION-HISTORY/2026-08-06-109-boot-floor-measured.md
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
  ▸ d0802-P2b — RULED #76 (dream pass 4) (2026-08-02, Dave): GOOD-MORNING.md hardcoded chain figure (4,585 tape prose block) replaced with the chain_file_tk('.') pointer form the same file already uses.
      status: ENACTED #128 2026-08-08. `GOOD-MORNING.md:125` no longer carries a figure: the prose now points at `chain_file_tk('.')` and says the figure MOVES, the form the same file uses at :427.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P4 — RULED #76 (dream pass 4) (2026-08-02, Dave): consult-receipts stratum line carries the running 'Nth of M' count (~8 tape/wrap).
      status: ENACTED #128 2026-08-08. The running-count form is inscribed at the ONE copy of the consult-receipt form, `knowledge/_search_core.py` (the file the gate's probe imports): the stratum line carries `#N (Nth of M)`.
      evidence: notes/_MEMENTO-DECISIONS.md:3373 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ s148-D1 — RULED #148 (2026-08-10, Dave): CLEAR THE STEP-11 BLOCK BOTH WAYS - picked from a three-option set ('Fix both now', the recommendation): (a) give live-chat provenance a LEGAL pointer form in _governs.py ('chat #<n> ...', the #119 commit-form precedent, [[honest-refusal-needs-a-legal-form]]) instead of letting the anchor predicate claim the word 'chat' as a path; (b) BACKFILL governs/evidence/status on the schema-drifted rulings (s142-D1 x5, s143-D1 x3, s146-D1 x2, s147-D1 x3, s147-D2 x3 missing fields; s135-D3/s143-D1/s144-D1/s145-D1 chat-evidence misclassified as anchors) from their own records, inferred fields MARKED as backfilled. Found by the #148 full _build_all.py drive at step 11 - a dead-runner casualty, second family after #147's 245 RAG values.
      status: ENACTED #148: legal form + selftest clause 6g (positive + three negative controls); entries backfilled textually, untouched entries asserted parse-equal.
      evidence: knowledge/_governs.py
      evidence: chat #148 (live) - Dave's pick from the three-option set
  ▸ s161-D4 — RULED #161 (2026-08-12, Dave): THE STALE-TOP-ITEM FENCE, BLOCK NOT WARN. A wrap may not certify a 'next top item' (or equivalent owed-work claim) that cites a ruling id whose _rulings.json status already says ENACTED - the #159/#160 defect that carried 's142-D1 wave enactment owed' two sessions past its fact, refuted the whole time by the store the wrap already parses. Conductor recommended block-not-warn (a warn under wrap heat is a warn nobody reads) with a bite test proving the gate can fail, driven on the real #160 wrap text as the red fixture. Dave: 'okay do it', after '2 sessions carried the wrong information, this is a waste of time'.
      status: RULED #161. Enactment delegated same session; conductor replays the gate in-window.
      evidence: chat #161 2026-08-12 (live) - Dave verbatim 'okay do it' on the read-back naming block-not-warn + bite test
      evidence: _DECISION-HISTORY/2026-08-12-160-the-nine-that-were-never-values.md (line 90, the false 'owed' claim) vs knowledge/_rulings.json (s142-D1 status: enacted #143)
  ▸ s161-D1 — RULED #161 (2026-08-12, Dave): G8 CLOSED - RETIRE COMPLETELY. The dormant % band 45/60/63 (BAND_FLOOR/HARD_STOP/MARKED_MAX) stays retired; this CONFIRMS #74-D3 rather than reversing it. Context: Dave first answered 'Pin' from the staged batch; the conductor surfaced that enforcement was already RETIRED at #74-D3 by his own option-select (the G8 state item, opened #86, pointed at retired residue) and gave the owed explanation (the band graded window fill as a %; its purpose carries on in the real-token path amber 160K / working 200K / hard 256K). Dave then ruled, verbatim: 'G8 retire completely'. The ruling history stays preserved per the #74 stratum (notes/_MEMENTO-DECISIONS.md sections 36 and 74); the G8 item closes as already-ruled-retired, now confirmed.
      status: RULED #161 after read-back; closes G8. No code change owed - enforcement was already retired; the state item closes.
      evidence: chat #161 2026-08-12 (live) - staged batch answer 'Pin, but lets return to this because i need an explanation for this', conductor read-back surfacing #74-D3, then Dave verbatim 'G8 retire completely'
      evidence: knowledge/_capture_gate.py:125-137 (the retirement comment block, #74-D3)
  ▸ s168-D3 — RULED #168 (2026-08-13, Dave): SUB-SPEND ACCOUNTING, OPTION 2 - Dave: 'I like both... lets do option 2'. (a) A gauge-log block MAY carry ONE optional line `subs <N> tokens (n=<count>)`. ABSENT IS LEGAL AND NEVER DEFAULTED. The word `job` is FORBIDDEN on that line - containment, not style: gen_dashboard.py's _JOB_RE sweeps the whole file and a `job`-spelled subs line would move an S/M/L band edge silently. Guarded by _capture_gate.py::gauge_log_subs_line, 12 arms, SUBS_LINE_BLOCKING=True - the TIER is a DECLARED CHOICE, not part of the ruling, and a downgrade is Dave's. Runbook section added at _RUNBOOK-capture-ritual.md step 2f. (b) EFFORT-SWITCH AGENT DEFINITIONS: .claude/agents/opus-deep.md (effort: max) and .claude/agents/opus-fast.md (effort: low). NOTE: they were NOT registered mid-session - first live use is #169.
      status: RULED #168 AND ENACTED IN-WINDOW for (a) - gate live and BLOCKING, runbook section written, first real subs line written by the #168 wrap. (b) BUILT NOT REGISTERED - agent defs exist on disk; first live use #169.
      evidence: chat #168 2026-08-13 (live) - Dave: 'I like both... lets do option 2'; FIRM
      evidence: knowledge/_capture_gate.py::gauge_log_subs_line - 12 arms, proven against _JOB_RE
      evidence: knowledge/_RUNBOOK-capture-ritual.md
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

