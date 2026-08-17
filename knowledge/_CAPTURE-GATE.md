# Capture gate report — mode: build
*Generated 2026-08-17 by `_capture_gate.py`. Scope: 149 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 7 found. READ BEFORE RE-DERIVING:
  ▸ gauge-refusal — RULED #79-D1 (2026-08-02, Dave): The gauge must REFUSE rather than guess. MeasurementRefused, paired with a handler that records refusal as a FAILURE - an unmeasurable floor is not a cleared floor.
      status: BUILT #80, mutation-tested x3
      ⚠ NOT SystemExit - count() is a library function inside a 39+-check gate and BaseException would slip _arm()'s except Exception. A precedent is a claim about a CALL SITE, not a repo.
      evidence: _DECISION-HISTORY/2026-08-02-the-79-dossier.md
  ▸ s115-D1 — RULED #115 (2026-08-06, Dave): Open graph-engineering candidates 1 + 3 + the MARK-HALF of 2 now, deferring #115's titled lane (D5 checker redesign, D2 citation gate). Verbatim: 'no lets get these done now.'
      status: RULED #115, ENACTED #115 (9b47152, 6a16633)
      ⚠ Display-only by construction: no ranking change (3 queries x 2 doors byte-identical vs HEAD with marks stripped). DEMOTION is NOT part of this ruling. Deviation declared: steps 1+3 share one commit because the sandbox delete-guard blocks the mv-aside.
      evidence: commit 9b47152
      evidence: commit 6a16633
      evidence: notes/_briefs/2026-08-06-graph-candidates-pricing-brief.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s146-D1 — RULED #146 (2026-08-10, Dave): BUILD THE ADDRESS-RESOLVE GATE AND WIRE THE ORPHANS - Dave's word ('do it please') on the stated recommendation: ONE gate for the 'stopped matching, stopped failing' class, not four per-site patches. Enacted same window: (1) knowledge/_validate_binds_resolve.py - manifest presence (75/75 absolute), manifest var resolution through gen_snippet_tokens.resolve (the ONE router, s121-D1 lesson), and meta binds address existence across declared stores (41 distinct addresses, 102 total; icon.* sizes live in icon-scale.json and alpha in opacity.json - 6 addresses no prior instrument could see). 5 selftest bites plus TWO real-corpus mutation drives (renamed rung -> red; renamed manifest id -> red; both restored byte-identical). (2) THE LAYERED-ORPHAN REPAIR: _build_all.py had aborted at check_routes() since #139 (four STEPS entries with no ROUTE_ROWS row), which is WHY _validate_binds_ratchet.py and _validate_dtcg.py (#141) sat as unwired orphans for 5 sessions - the wiring gate lives inside the runner that refused to start. Routes repaired (110 steps), all three gates wired, wiring gate 35/35.
      status: ENACTED #146. Readback owed: 'do it' was read as ratifying the one-gate design; Dave may strike. NOTE the gate proves addresses point at SOMETHING, not the RIGHT thing - binding correctness stays with the BINDS-AUTHORING-VERDICTS record.
      evidence: knowledge/_validate_binds_resolve.py
      evidence: _DECISION-HISTORY/2026-08-10-146-two-thirds-of-a-shape-and-the-runner-that-died-quietly.md
      evidence: chat #146 (live) - Dave: 'do it please'
  ▸ s148-D1 — RULED #148 (2026-08-10, Dave): CLEAR THE STEP-11 BLOCK BOTH WAYS - picked from a three-option set ('Fix both now', the recommendation): (a) give live-chat provenance a LEGAL pointer form in _governs.py ('chat #<n> ...', the #119 commit-form precedent, [[honest-refusal-needs-a-legal-form]]) instead of letting the anchor predicate claim the word 'chat' as a path; (b) BACKFILL governs/evidence/status on the schema-drifted rulings (s142-D1 x5, s143-D1 x3, s146-D1 x2, s147-D1 x3, s147-D2 x3 missing fields; s135-D3/s143-D1/s144-D1/s145-D1 chat-evidence misclassified as anchors) from their own records, inferred fields MARKED as backfilled. Found by the #148 full _build_all.py drive at step 11 - a dead-runner casualty, second family after #147's 245 RAG values.
      status: ENACTED #148: legal form + selftest clause 6g (positive + three negative controls); entries backfilled textually, untouched entries asserted parse-equal.
      evidence: knowledge/_governs.py
      evidence: chat #148 (live) - Dave's pick from the three-option set
  ▸ s161-D4 — RULED #161 (2026-08-12, Dave): THE STALE-TOP-ITEM FENCE, BLOCK NOT WARN. A wrap may not certify a 'next top item' (or equivalent owed-work claim) that cites a ruling id whose _rulings.json status already says ENACTED - the #159/#160 defect that carried 's142-D1 wave enactment owed' two sessions past its fact, refuted the whole time by the store the wrap already parses. Conductor recommended block-not-warn (a warn under wrap heat is a warn nobody reads) with a bite test proving the gate can fail, driven on the real #160 wrap text as the red fixture. Dave: 'okay do it', after '2 sessions carried the wrong information, this is a waste of time'.
      status: RULED #161. Enactment delegated same session; conductor replays the gate in-window.
      evidence: chat #161 2026-08-12 (live) - Dave verbatim 'okay do it' on the read-back naming block-not-warn + bite test
      evidence: _DECISION-HISTORY/2026-08-12-160-the-nine-that-were-never-values.md (line 90, the false 'owed' claim) vs knowledge/_rulings.json (s142-D1 status: enacted #143)
  ▸ s191-D3 — RULED Dataviz var-resolution gate promoted to BLOCKING; DV-J2b record clash reconciled by annotation (2026-08-17, Dave): Two settlements in one word ('just get tehm done', approving the recommendations as put). (a) The dataviz var-resolution gate (knowledge/_gate_dataviz_vars.py, built #190 e568dcf-adjacent as the #184 priced candidate) is promoted from ADVISORY to BLOCKING in _build_all.py — a chart colour var() resolving in no theme renders silent black past thirteen gates and is never intentional; its selftest row rides to ABORT. Glob width and ds-number remain as picked. (b) The DV-J2b redundant-record clash (GOOD-MORNING.md + knowledge/_state.json W-0c both claiming FOLDED+ENACTED #67 against s182-D2's deletion) is reconciled BY ANNOTATION: the old lines are marked OVERTAKEN with s182-D2 named as the operative closure — ratified record annotated, never erased.
      status: ruled
      evidence: chat #191 2026-08-17 (live) - Claude: '1. Var-gate: block? 2. Record clash: annotate?' Dave: 'just get tehm done and then we'll wrap if you have space'
  ▸ s193-D1 — RULED #193 (2026-08-17, Dave): MAKE THE GATES ROCK SOLID BY FIXING THE CLASS, NEVER PATCHING (his words: 'whatever fixes this without patching, lets wire it all properly' / 'okay I want this rock solid'). Two decisions taken on explicit yes: (a) _inscribe_ruling.py gains a SANCTIONED --amend-evidence mode carrying the same byte-reconstruction proof as append (evidence array ONLY, `says` unreachable by construction), and the s176-D2/s178-D1 + s175-D1/s176-D1 evidence entries are legalized with factual pointers, nothing retyped; (b) the memento-package VERBATIM SET re-sync is authorized ONCE for #193 (his #64 release boundary) — explicitly NOT a standing rule. Companion enactments the same session under the same word: the COULD-NOT-ASK third verdict (exit 77 + self-naming first line, _could_not_ask.py) wired across tier/reach-dependent gates and read by _build_survey.py and _build_all.py.
      status: RULED + ENACTED #193
      evidence: chat #193 2026-08-17 (live) - the two AskUserQuestion answers ('Yes, build it' / 'Yes, sync now') and the standing words quoted in says
      evidence: commit d44f023 - COULD-NOT-ASK wired as a third verdict across the tier-dependent gates
      evidence: commit f773cc2 - --amend-evidence built + s176-D2/s178-D1 legalized; memento-package re-synced (authorized once)
      evidence: commit 711bfd1 - the remaining 5 provenance reds legalized; capture gate 0 reds
      evidence: commit 27f5342 - the two defects the wiring shipped with fixed (recursion hang; checkout-cannot-hold refusal)
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

