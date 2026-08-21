# Capture gate report — mode: build
*Generated 2026-08-21 by `_capture_gate.py`. Scope: 166 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 39 found. READ BEFORE RE-DERIVING:
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
  ▸ s110-D1 — RULED #110 (2026-08-06, Dave): Open the four-phase boot-rent plan (ds-036); P1 delegated to a Sonnet sub. Chosen over P2-first, over cranking the design queue, and over research candidates 1+2.
      status: RULED #110 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: GOOD-MORNING.md
      evidence: _LIVE-STATE.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s110-D2 — RULED #110 (2026-08-06, Dave): Posture: crank, delegate hard.
      status: RULED #110 - status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) - read the evidence pointers
      evidence: GOOD-MORNING.md
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
      evidence: notes/_MEMENTO-DECISIONS.md:3568 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P2b — RULED #76 (dream pass 4) (2026-08-02, Dave): GOOD-MORNING.md hardcoded chain figure (4,585 tape prose block) replaced with the chain_file_tk('.') pointer form the same file already uses.
      status: ENACTED #128 2026-08-08. `GOOD-MORNING.md:125` no longer carries a figure: the prose now points at `chain_file_tk('.')` and says the figure MOVES, the form the same file uses at :427.
      evidence: notes/_MEMENTO-DECISIONS.md:3568 — I'll go with all your recommendations
      evidence: notes/_dream/2026-08-08-proposals.md
  ▸ d0802-P4 — RULED #76 (dream pass 4) (2026-08-02, Dave): consult-receipts stratum line carries the running 'Nth of M' count (~8 tape/wrap).
      status: ENACTED #128 2026-08-08. The running-count form is inscribed at the ONE copy of the consult-receipt form, `knowledge/_search_core.py` (the file the gate's probe imports): the stratum line carries `#N (Nth of M)`.
      evidence: notes/_MEMENTO-DECISIONS.md:3568 — I'll go with all your recommendations
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
  ▸ s186-D2 — RULED #186 (2026-08-16, Dave): DREAM-PASS BACKLOG SETTLED (Phase 1 sitting). Pass 6 P1-P4 PROMOTED as priced Phase 2 enactment rows: P1 re-checker counting the 21 frozen '#119 sweep' status strings at wrap (no bulk rewrite - that manufactures the CLAIMED class ADR-0016 forbids); P2 the verify-after-commit-dirties-tree fix; P3's two remaining stale Desktop-only lines in _RUNBOOK-git-commit.md amended by addition (the substance was already corrected #141; Desktop stays legal); P4 expiry stamp on the ledger's PAT line (~2026-11-06) + reword the refusal so the credential never transits chat (token scope stays Dave's security call, unproposed). P5 RULED: KEEP the --all-dirty hatch - disclosed at birth, echo-mitigated, no observed harm; the #128 open question closes as kept. Pass 7 P1 PROMOTED to Phase 2: liveness check of the four STANDING CARRY items FIRST, then fold into the fenced residual list; the two bare ordinals (GM:10, GM:438) are DELETED, never re-stamped. Also ratified in the same word: the W-17 and W-18 close conditions as written at #185; W-18's condition is satisfied by s186-D1 and W-18 closes.
      status: ruled
      evidence: chat #186 2026-08-16 (live) - Dave picked promote-all-four / keep / promote-to-Phase-2, then ratified the full readback including both close conditions: 'Firm - ratify all'
  ▸ s188-D2 — RULED #188 (2026-08-16, Dave): PASS-8 P2 RULED: NARROW RETRACTION CARVE-OUT, RECEIPT REQUIRED. The 2c carry rule's 'AGES +1, WORDING UNCHANGED' invariant gains exactly one exit: a carried claim's wording may change ONLY to record a retraction, and the edit MUST cite its receipt (the run or commit that proved the claim false), the same way a repo claim cites git log. An edit without a receipt token is refused by the carry gate exactly as today. The carve-out is mutation-tested like any gate before it is trusted. BUILD QUEUED to #189, not built at #188. Pass-8 P3/P4/P5 remain FLOATED, carried to #189 undecided.
      status: ruled
      evidence: chat #188 2026-08-16 (live) - carve-out vs keep-frozen vs drop-invariant laid out with the twice-carried retracted claim as the driving case; Dave: '2. same again, your recommendation - narrow carve-out, receipt required'
  ▸ s188-D3 — RULED #188 (2026-08-16, Dave): SUPERSESSION, EXPLICIT: s188-D1 (grader reads the hook FILE) SUPERSEDES the P1 clause of s183-D1 (the light version: index-line grading + companion count + refusal-string fix), which is RETIRED. s188-D2 (receipt-required retraction carve-out) stands as a STRENGTHENING AMENDMENT to s183-D1's P2 clause, not a reversal. Dave's word: 'I just want the most robust version of this so we don't have to revisit it, the point behind all this is you have full spectrum context, with as little failures as possible.' s183-D1's P3/P4/P5 clauses are UNTOUCHED and remain in force. FINDING RECORDED IN THE SAME WORD: the #187 chain asserted pass-8 P1-P5 were floated/unruled while s183-D1 had held their promotion for four sessions; the conductor believed the chain over the rulings store and re-put settled rulings as options - the retrieval-default class. The rulings store is the authority on 'was this ruled'; the chain is not.
      status: ruled
      evidence: chat #188 2026-08-16 (live) - the s183-D1/s188-D1 delta was asserted to Dave plainly and he picked the robust version
  ▸ s190-D2 — RULED #190 (2026-08-16, Dave): STOP-LINE SEMANTICS CLARIFIED: the 150,929 stop line is the ADVISORY start-wrap-by figure, not the wall. Dave's word: 'the cut off that you have to squeeze the wrap is 200k not 150 you have space' (#190, live, correcting a conductor reading the advisory as the binding cutoff). The binding squeeze cutoff for a wrap is the 200,000 working cap (the #56 band); 150,929 remains the line at which a wrap should OPEN. A conductor at FILL between 150,929 and 200,000 has legal room to finish a wrap and should not panic-delegate or truncate on the advisory alone.
      status: ruled
      evidence: chat #190 2026-08-16 (live) - Dave: 'do a little job and wrap, the cut off that you have to squeeze the wrap is 200k not 150 you have space'
  ▸ s191-D3 — RULED Dataviz var-resolution gate promoted to BLOCKING; DV-J2b record clash reconciled by annotation (2026-08-17, Dave): Two settlements in one word ('just get tehm done', approving the recommendations as put). (a) The dataviz var-resolution gate (knowledge/_gate_dataviz_vars.py, built #190 e568dcf-adjacent as the #184 priced candidate) is promoted from ADVISORY to BLOCKING in _build_all.py — a chart colour var() resolving in no theme renders silent black past thirteen gates and is never intentional; its selftest row rides to ABORT. Glob width and ds-number remain as picked. (b) The DV-J2b redundant-record clash (GOOD-MORNING.md + knowledge/_state.json W-0c both claiming FOLDED+ENACTED #67 against s182-D2's deletion) is reconciled BY ANNOTATION: the old lines are marked OVERTAKEN with s182-D2 named as the operative closure — ratified record annotated, never erased.
      status: ruled
      evidence: chat #191 2026-08-17 (live) - Claude: '1. Var-gate: block? 2. Record clash: annotate?' Dave: 'just get tehm done and then we'll wrap if you have space'
  ▸ s212-D2 — RULED RAG STATUS MANIFESTATION - CANON IS A+B+C (G17 closes) (2026-08-21, Dave): The RAG status canon pick, open since 2026-07-19, is A+B+C - all three manifestations are canon. Judged on the live render iframed in the REVIEW-212 rule-now page, which answers the #86 caveat that the live render was unverified. Enactment (wiring the pick into canon) is queued as its own store row.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'A+B+C - G17 RAG status manifestation'
      evidence: reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1.REVIEW.html - the artefact judged live
  ▸ s212-D3 — RULED TONE-OF-VOICE TEMPERATURE MAP RATIFIED AS-IS (G12 closes) (2026-08-21, Dave): Charter section 4b's temperature map (expressive = wit ON surface-scoped / balanced = subtle headline-only / sober = zero wit warmth stays; locale a parameter on any band, clarity outranks it) moves PROVISIONAL -> RATIFIED, unchanged, after seven weeks live without friction. The PROVISIONAL stamp in the charter and guidelines may be updated to RATIFIED with this ruling as provenance.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'RATIFY AS-IS - G12 tone-of-voice temperature map'
  ▸ s212-D4 — RULED THE STRAY 70%/95% BAND IS STRUCK (G10 closes) (2026-08-21, Dave): The '70%/95%' band in GOOD-MORNING.md matching no ruled banding system, with no provenance repo-wide and already FENCED, is STRUCK on Dave's word. The line is removed at source with this ruling as provenance; the two-red law, gauge bands and every ruled banding system are untouched.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'STRIKE - G10 stray 70%/95% band'
  ▸ s212-D5 — RULED THREE CONSTANTS RATIFIED AS-IS AND PARKED AS A SET (G1+G2+G6) (2026-08-21, Dave): DOFIRST_INDEX_TK_MAX=700 (G1), TAPE_TO_BILL=1.57-at-n=2-provisional-until-4-pairs (G2), DEFER_STREAK=6 with USAGE_HISTORY_BLOCKING=False (G6) are ratified at their current values and their rows PARKED. The park is conditional: any of the three returns to Dave's desk the first time a gate fails on it, with the live failure attached. G2's own firm-or-retire-at-n=4 rule survives the park unchanged.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'RATIFY+PARK ALL THREE - G1+G2+G6 three low-risk constants as a set'
  ▸ s212-D6 — RULED SECTION-C REMEDY IS OFFLOAD (G4) (2026-08-21, Dave): GM section C's over-cap state (about 185 charged lines vs 150 warn) is remedied by OFFLOAD, chosen over TRIM and KEEP: bodies move into conditioned store rows, section C keeps one pointer line per item, nothing is deleted, the home-by-addition-then-cut probe runs per moved body. The 150 cap itself is NOT re-dialled by this ruling. Enactment is Claude's, queued as its own store row; G4 closes when section C measures back under its warn cap.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'OFFLOAD - G4 GM section-C over its 150-line cap'
  ▸ s212-D7 — RULED THE ds-023 RE-MEASUREMENT PROGRAMME RUNS, DELEGATED (G9; G5 waits on it) (2026-08-21, Dave): G9's programme is ruled RUN: every old-unit ceiling is re-measured on its artefact in real tokens and restamped with provenance - measured, never converted. Delegated to a sub; the restamped numbers return to Dave for the G5 set-ratification in one pass, per G5's own close condition. Nothing is ratified by this ruling; it authorises the measurement.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'RUN IT (delegate) - G9 re-measurement programme (unblocks G5)'
  ▸ s212-D8 — RULED ICON-BUTTON DARK BINDINGS PARKED UNDER THE SC-DARK PARENT (G14) (2026-08-21, Dave): G14 is parked under its parent question - SC dark (ADR-0014, awaiting Dave). Icon-button keeps reusing Button's on-light/on-dark verbatim until the SC-dark sitting rules the family; G14 un-parks into that sitting automatically.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'PARK UNDER SC-DARK - G14 icon-button dark bindings'
  ▸ s212-D9 — RULED MENU-SEARCH COMBINED GLYPH APPROVED - the Figma Neo-net export replaces the provisional (G13b closes) (2026-08-21, Dave): The designed combined menu+search glyph (Figma Neo-net v02.0 Brand dev 06, node 2785:97115) supersedes the provisional bespoke glyph that had run since 2026-07-16. Dave supplied the node ('This was always a placeholder until it was designed properly. try this' + URL) and approved the placed swap ('good'). Library asset: knowledge/assets/icons/menu-search.svg (background stripped, currentColor, geometry untouched); consumer: Masthead-interactive.html symbol i-menu-search, provenance attribute carries the figma-export trail.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'try this' + Figma URL node 2785-97115, then 'good' on the placed swap
      evidence: knowledge/assets/icons/menu-search.svg - the cleaned export with provenance comment
  ▸ s212-D10 — RULED THE FOUNDING PRINCIPLE IS SETTLED - the six-beat ladder, model-free, a guiding principle not a manifesto (W-14 closes) (2026-08-21, Dave): The founding principle's wording is the ruled six-beat ladder in Dave's own method words: RETRIEVE - RESEARCH - ANALYSE - PLAN - PROBE - TEST (his 'we research, we analyse, we probe, we test' plus the #62 PLAN and desk-research extensions, shaped at #63-D1). His framing at adoption, near-verbatim: the principle is a GUIDING PRINCIPLE, not a manifesto or rule; MODEL-ROUTING.md is the instruction/adapter layer beneath it. The principle deliberately names no model - the three-layer architecture (invariant/knowledge/adapter, his own 2026-07-23 research) holds per the #212 currency check, so the invariant stays model-free by design. Adopted conditionally on that check ('do the research first... then we'll go with your recommendation') and the condition resolved HOLDS. The routing-table amendments the check proposed (P1-P10, two behavioural: P4 classifier-destination rewrite, P8 the Opus-5-verification-vs-canon-rule-5 conflict) are SEPARATE and await Dave's by-number rulings.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'do the research first to see if anything has changed then we'll go with your recommendation. Guess the shape of it is the principle is a guiding principle not a manifesto or rule and the other routing becomes the instruction layer'
      evidence: notes/_briefs/2026-08-21-212-routing-currency-check-v1.md - the check: holds with 10 amendments, architecture untouched
      evidence: notes/2026-07-23-fable-routing-research-dave.md - the three-layer source, Dave's own research
  ▸ s212-D11 — RULED THE G5 CAP SET IS RATIFIED AT THE MEASURED RESTAMPS - real unit, one pass (G5 closes) (2026-08-21, Dave): The four old-unit advisory caps are restamped in REAL tokens at the G9 programme's measured proposals, ratified as a set: CORPUS_BUDGET_TK 36000 -> 55700 · chain-region pair (4917, 6417) -> (7700, 10000) · BANNER_BUDGET_FALLBACK_TK (4000, 5000) -> (6400, 7800) · SECTION_A_WARN_TK 4500 -> 7200. Derivation was restatement not re-dial: REAL(artefact at its ruling) x (cap / cl100k at its ruling), baselines reproduced exactly before proposing. Consequences carried with the ruling: the corpus and chain caps remain genuinely breached by real growth after restamp (3.3x and ~2x) - the restamp makes the unit honest, it does not silence those warnings; section A's warn clears because it was a pure unit artefact. Riders NOT ruled here, still Dave's: the bill_of() 1.57x overstatement repair, and the re-PICK of SIZE_BUDGET compactable 8000 + TITLE_CAP_TAPE 120 (picked-never-measured, no restamp possible).
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'okay lets do it' on the presented restamp table
      evidence: notes/_receipts/2026-08-21-212-g9-ds023-remeasurement.md - the measurement, baselines reproduced exactly
  ▸ s212-D12 — RULED MODEL-ROUTING CURRENCY AMENDMENTS P1-P7 + P9 + P10 TAKEN; P8 STAYS OPEN (2026-08-21, Dave): Nine of the ten numbered amendments from the #212 routing currency check are taken as ruled text corrections to MODEL-ROUTING.md: P1 (Fable pinned claude-fable-5, usage credits named as the ration mechanism) · P2 (Default cell cited+dated) · P3 (Sonnet/Haiku strings pinned, Haiku retirement watch >= 2026-10-15) · P4 (fallback-aware routing rewritten - Opus 5 is no longer a classifier-free destination) · P5 (five published classifier categories replace 'security-adjacent') · P6 (effort = five-rung ladder, official page) · P7 (mid-session anti-pattern broadened to model-and-effort) · P9 (Mode 2 doc corroboration) · P10 (tokenizer-overhead line corrected - Fable premium is 2x per token, nothing more). P8 - the Opus-5 remove-verification guidance vs canon verification rule 5 and the #204 adversarial-verifier topology - is DELIBERATELY NOT RULED: three readings stand in the report and the pick is Dave's.
      status: ruled
      evidence: chat #212 2026-08-21 - Dave: 'okay lets do it' on the presented amendment list, P8 explicitly presented as unpicked
      evidence: notes/_briefs/2026-08-21-212-routing-currency-check-v1.md - the dated check, every claim sourced
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

