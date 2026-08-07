# Capture gate report — mode: build
*Generated 2026-08-07 by `_capture_gate.py`. Scope: 83 file(s) at/after cutover 2026-07-26.*

## WARN
- ds-021 (C) DECLARED GAP — `knowledge/_context_gauge.py` counts in cl100k and cannot name a REAL tier. REFUSES without tiktoken unless --estimate labels the output (#74). Honest about estimate-vs-nothing; still blind to cl100k-vs-real.
- ds-021 (C) CALIBRATION — `knowledge/_measure_tokenizer.py`. #53's instrument — prints a tape|real|ratio|drift table. ⚠ 0 Python consumers, flagged by #77's periphery inventory, re-probed #81 and STILL zero. It is the reason #80 re-derived a ruling #54 had already made: an instrument ships WITH ITS READER, and a measurement nothing re-reads decays into a rediscovery.

## NOTE
- ⚠ RULINGS ALREADY GOVERN WHAT YOU ARE TOUCHING (files touched this session) — 11 found. READ BEFORE RE-DERIVING:
  ▸ gauge-refusal — RULED #79-D1 (2026-08-02, Dave): The gauge must REFUSE rather than guess. MeasurementRefused, paired with a handler that records refusal as a FAILURE — an unmeasurable floor is not a cleared floor.
      status: BUILT #80, mutation-tested x3
      ⚠ NOT SystemExit — count() is a library function inside a 39+-check gate and BaseException would slip _arm()'s except Exception. A precedent is a claim about a CALL SITE, not a repo.
      evidence: _DECISION-HISTORY/2026-08-02-the-79-dossier.md
  ▸ ds-026 — RULED #99 (2026-08-05, Dave): Charts stick to SOLID canonical palette; opacity primitives (--alpha-04..96, 4% ladder, ties round DOWN) are for STATE CHANGES only, for now. Tints = flexibility, not the default reach. --stack-fill-alpha dial retired.
      status: RULED #99 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      ⚠ EVIDENCE-PROSE moved here #119 (was in evidence, the eleventh-copy defect): ledger notes/_MEMENTO-DECISIONS.md § ★ #99; review pair reviews/OPACITY-PRIMITIVES-2026-08-05-v1.html
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: reviews/OPACITY-PRIMITIVES-2026-08-05-v1.html
  ▸ ds-027 — RULED #100 (2026-08-05, Dave): Candlestick encoding: TWO-STATE semantics (colour = close vs open) with SOLID bodies BOTH directions — the hollow-up shape channel of #96-D1 ① is RETIRED. The OHLC data table is the accessibility fallback (colour-blind/greyscale reading). Four-state prior-close convention REJECTED after live spread. Also standing: chart examples carry realistic density (~40 sessions) and are fully responsive via dv-fit — fixed 580 sizing does not apply.
      status: RULED #100 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: reviews/CANDLESTICK-FOURSTATE-2026-08-05-v1.html
  ▸ ds-031 — RULED #106 (2026-08-05, Dave): Donut/pie legend centring: OPTION A, keep as-is. The ring stays 109px left of true container centre; the offset is legend-footprint-driven ((190+28)/2), CONSTANT at 1180px and 760px, not proportional. Option B (hidden .dv-leg-spacer{min-width:190px} -> 0px) NOT taken.
      status: RULED #106 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: reviews/LEGEND-CENTRING-SPREAD-2026-08-05-v1.html
      evidence: knowledge/_REVIEW-SIGNOFF.md:213
  ▸ ds-032 — RULED #106 (2026-08-05, Dave): --alpha-68 is APPROVED for --pri-hover, but the ruling is scoped to the BUTTON ATOM, not to eight per-component edits. Dave verbatim: 'if these are just all buttons from different components they should all be using the one button atom to build from. So there should be one ruling on buttons alone, the alpha-68 is fine.' PREMISE VERIFIED at #106: all 8 sites map --pri-hover to the identical token button/primary/background/hover and each re-declares the hex locally. NOT ENACTED - Dave ruled the blast radius must be measured first; measured #106 as 58 literal button/primary declarations across 10 of 77 snippet files, with an UNRECONCILED 8-sites vs 9-files unit delta that #107 must close before any sweep.
      status: RULED #106 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: notes/_MEMENTO-DECISIONS.md
      evidence: reviews/PRI-HOVER-MEASUREMENT-2026-08-05-v1.md
      evidence: knowledge/_DS-IMPROVEMENTS.md:1789,1806
  ▸ ds-034 — RULED #108 (2026-08-06, Dave): On the button/primary scope question: measure the other 35 colliding token names BEFORE ruling scope — only 5 of 40 were value-checked (#108-D2). Extends his own #107-D1 'partition first, then rule' one level deeper. CORRECTED BY THIS SAME SESSION'S OWN FINDING (see ds-035): the sweep must test value agreement PER THEME, not globally — a global sweep would have manufactured roughly 35 false findings, because --pri-hover and --sec-hover genuinely resolve to different upstream tokens across .cn-button / .cn-modals / .cn-action-bar BY DESIGN under the four-theme architecture, not by drift. NOT STARTED — #109's first job.
      status: RULED #108 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: outputs/_FINDING-canon-pri-hover-brand-mono-fork-2026-08-06-v1.md
      evidence: outputs/_PARTITION-button-primary-2026-08-06-v1.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ ds-035 — RULED #108 (2026-08-06, Dave): STANDING CONSTRAINT, verbatim (#108-D3): "we have 4 themes, mono, legacy, console, and supercharge. they have a lot of overlap but they also diverge, especially the colour palette of legacy and the others, and the grey ramp for supercharge and the others. I just want the flexibility to have these themes and create more." Plus, explicitly NOT NOW: "I will also be revisiting the grey ramp for mono, i think we've calculated wrong." Governs every future cross-theme token-collision sweep: apparent divergence between themes on the same semantic token name is EXPECTED and must not be treated as a defect by default — see ds-034's corrected per-theme sweep spec.
      status: RULED #108 — status field added #119 in a metadata sweep; enactment state NOT asserted here (UNPROVEN by this sweep) — read the evidence pointers
      evidence: outputs/_FINDING-canon-pri-hover-brand-mono-fork-2026-08-06-v1.md
      evidence: notes/_MEMENTO-DECISIONS.md
  ▸ s114-D3 — RULED #114 (2026-08-06, Dave): Apply the hidden hit-area expander to the 8 sub-24px-floor offenders. Verbatim: 'yes expand the hit area...'. OUTCOME: only 2 were real controls (.fl-tip, .help-btn) and were fixed; the other 6 are DECORATIONS of >=44px parents — a gate-SCOPING defect, not 8 a11y failures. Dave's nuance: chart tooltip trigger-points are a lesser concern, the table fallback always exists, a11y rulings there are more nuanced.
      status: RULED #114, ENACTED #114 (994cd25) — the 2 real controls only
      ⚠ The 6 remaining 'offenders' are PHANTOM. Do not 'fix' them; s114-D5's measurement redesign is what removes them.
      evidence: commit 994cd25
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
  ▸ s116-D2 — RULED #116 (2026-08-06, Dave): The table control is ONE MOLECULE consumed by all charts. Verbatim: 'why is it different? the table button and pop-over should be a molecule consumed by all of teh charts.' The button-in-4 / <details>-in-1 split IS the defect. DIRECTION RULED: all charts converge on the NATIVE <details>/<summary>, confirmed as an HTML/CSS solution ('just to confirm, this is an html/css solution' — answered YES). Edge-clamping, Escape-to-close and focus-move are rebuilt as PROGRESSIVE ENHANCEMENT: works fully without JS, JS improves it.
      status: RULED #116, ENACTED #116 — 21 panels across 13 charts converged onto native <details>/<summary>; `hidden` removed; dv-behaviour.js table module rebuilt as progressive enhancement
      ⚠ MEASURED FINDING under this ruling: .dv-tablepanel ships `hidden` (Chart-bar.reference.html:367) and ONLY dv-behaviour.js removes it — with JS off the table fallback is UNREACHABLE on 4 of 5 charts. That is the justification s116-D1 rests on, so D2's convergence is what makes D1 honest. Do not land D1's 24 floor while the fallback is still JS-gated.
      evidence: notes/_MEMENTO-DECISIONS.md
  ⛔ These are DECIDED. Re-deriving one is the #80 defect; re-opening one is Dave's alone.

