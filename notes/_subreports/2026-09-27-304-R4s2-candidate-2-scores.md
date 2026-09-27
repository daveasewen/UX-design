# #304 R4s2 — candidate 2 scored on every view

provenance: 304 · Sun 2026-09-27 · scoring seat R4s2 (Opus 5.5) · repo HEAD 3100da99 · nothing committed, no git calls, no Project memory · writes only this report, `notes/_REVIEW-304-candidate-2-2026-09-27-v1.html` and `notes/_lanes/304/R4s2/` (plus seat-local stages `$HOME/r4c/stage/cold-cand2-*`, `$HOME/r4s2/st/c2canon/`) · the frozen cold-run outputs were not touched
status: observed — every figure was printed by the W4b harness, a gate or a probe at the seat; every screenshot named below was looked at

**Review page for Dave:** `notes/_REVIEW-304-candidate-2-2026-09-27-v1.html`

## The answer

Candidate 2 carries less ink and looks better; most of the gain is the chart engine, which lifts the old pages equally. Ink per view (W4b harness `w4b-2.0`, all ten views, lower is better): cand2-r1 4.7, cand2-r2 4.4, cand2-r3 6.2, mean **5.10**. The six earlier runs as shipped (W4b baseline) 6.62; the same six re-rendered on candidate 2's own engine, canon and type **5.53** (v1.0.13 5.43, candidate 1 5.63) — identical, class for class and run for run, to W4a's re-render, so wave three and four's canon moved nothing on those pages. Setting aside the Kpi-tile label crop (held for Dave, s261-D4) and a harness false positive (grid rows hidden in the grid's own scroll box), the groups read v1.0.13 5.30, candidate 1 4.27, candidate 2 3.73, with candidate 2's runs tight at 3.6–3.9. Small, consistent, three runs a side. All nine runs pass the floor.

By eye (full-length 1440 light and dark, looked at): cand2-r3 is the best overview of the nine — half-width chart pairs, finding-titled charts, no left-cut axes, no stretched rings, thinned dates. Shared with v1.0.13 and still first to the eye: 30 markers on every 30-point line (and stacked-area letters on cand2-r2), dark-mode chart tiles without edges, the 640px shell, shrunk legend buttons, the KPI descender crop, labels now cut at the right-hand end.

**Recommendation, for Dave's decision:** cut v1.0.14 from candidate 2 on Tuesday, after two gate-code fixes that change no rendered page (receipt gate masks APOLLO-DEMO spans; icon-source check masks script bodies), so no new cold run. This departs from R4s's four-fix condition: one of the four landed (Common 24px, measured 24px on all runs); the other three (KPI crop, full-height shell, chart receipt address) each wait on Dave and are in v1.0.13 already.

## Which comparison is like for like

- **(c) the six restaged on the candidate-2 pack's engine+canon+type** (`restage_c2.py`, W4a's method; pack bytes = HEAD 3100da99): like for like on what a page renders with. 5.53.
- **(b) W4a's patched engine**: like for like on the engine, but HEAD 86249459 canon (pre waves three/four). Reads identical to (c).
- **(a) W4b baseline**: old engine, old canon. Not like for like.
- **Build time is like for like in no set**: cand2 agents built with the new engine, canon and the candidate-2 skill in front of them; the six were built on v1.0.13 / candidate 1 and are only re-drawn. (c) → cand2 is authoring plus run-to-run chance.

## Scores (ink per view; class counts over ten views)

| run | (a) as shipped | (b) W4a | (c)/as built | adjusted | dead | cut | coll | size | markers |
|---|---|---|---|---|---|---|---|---|---|
| v1013-r1 | 7.3 | 6.2 | 6.2 | 5.8 | 15 | 0 | 14 | 28 | 5 |
| v1013-r2 | 3.9 | 3.7 | 3.7 | 3.7 | 4 | 0 | 0 | 27 | 6 |
| v1013-r3 | 7.4 | 6.4 | 6.4 | 6.4 | 21 | 0 | 9 | 29 | 5 |
| cand-r1 | 8.0 | 5.8 | 5.8 | 4.8 | 11 | 9 | 1 | 31 | 6 |
| cand-r2 | 5.2 | 4.0 | 4.0 | 3.4 | 7 | 3 | 4 | 22 | 4 |
| cand-r3 | 7.9 | 7.1 | 7.1 | 4.6 | 7 | 24 | 10 | 26 | 4 |
| cand2-r1 | — | — | 4.7 | 3.7 | 8 | 5 | 7 | 23 | 4 |
| cand2-r2 | — | — | 4.4 | 3.6 | 5 | 3 | 5 | 31 | 0 |
| cand2-r3 | — | — | 6.2 | 3.9 | 10 | 23 | 0 | 25 | 4 |

Means: v1.0.13 6.20 / 5.43 / 5.43 / 5.30 · candidate 1 7.03 / 5.63 / 5.63 / 4.27 · candidate 2 — / — / 5.10 / 3.73. Per class, candidate 2: dead 0.77, cut 1.03 (all Kpi crop), collisions 0.40 (10 of 12 grid false positive), size 2.63, markers 0.27. Adjusted = minus views whose sampled collisions all name the grid pager/hint/range and whose sampled cuts are all `kpi-lbl` (heuristic on ≤3 samples per class per view, declared). Harness ext (overview): geometry score 1 on all three; direct gates on all ten pages: own-size 82 / 104 / 146 findings, every one a chart part (legend buttons, sparkline table cells). Judgment rows printed on the page with evidence, answered "Dave: ______".

## Defects the runs reported, verified

1. **Dark: grey section and tiles both #1F1F1F** — confirmed on all three (`shots/shots.json`). `[data-theme="dark"]` sets `--surface-subtle` and `--surface-raised` both #1F1F1F (`canon.css`:845–846, generated tokens); `_bento_edit_rails.json` page_rail resolved dark grey = white for every theme, and has no `common` entry. v1013-r3 and cand-r3 set their ground to #1A1A1A by hand. **Dave's call** (which dark ground), then canon/rails.
2. **Side-nav 640px** — confirmed (`canon.css`:5678, 4697, 5148); cand2-r1/r2 640 as shipped; cand2-r3 skipped `.sh`, its nav pane stops ~730px. **Component** (full-viewport form) + skill wording.
3. **Receipt gate counts the fenced demo script** — confirmed: `_validate_receipt.inline_scripts()` skips AUTO-BEHAVIOUR spans but not APOLLO-DEMO (DEMO_FENCE_RE at :199 unused there); Data-grid `#script[1]` = the 1,447 B fenced switcher (snippet :1140–1166). FAIL:BEHAVIOUR-NOT-LOADED on grid pages of all three runs. **Pack tooling, no ruling** — pre-cut fix.
   **Wrong chart script** — confirmed: mint `behaviour_address()` → `dv-behaviour.js`, metas → `dv-render.js`; FAIL:BEHAVIOUR-ADDRESS-DISAGREES on every chart region of cand2-r3 (r2 re-minted around it). **Dave's one line, then tooling** (R4s (b), still open).
4. **text-box-trim shrinks legend buttons** — confirmed and located: the shell's and bento's per-scope leading-trim rule (`canon.css`:5668, 17643: `:where(.cn-x) :where(button, span, li, …)`) trims the two spans inside each nested legend button → 16.7px; removing trim on those spans restores 20px (`probe_size.py`). **Canon generator** (`gen_canon_components` scoping has no lower boundary at a nested `cn-` scope), no ruling. This is the size class, ~2.6/view in every group.
5. **KPI tiles 4px taller in the bento** — confirmed, same class: `:where(.cn-template-dashboard-bento) .spark-inline{height:44px}` (17942) outranks Kpi-tile's 40px (13102); tile 159.1 v 155.1. **Canon generator**, no ruling.
6. **Icon-source false positive** — confirmed on cand2-r2: `_validate_screen.gate_icons()` scans raw HTML incl. script bodies; inlined `dv-render.js` has "<svg" at :245/:258, read as `d="M' + p.join(' L') + ' Z…"`. **Pack tooling, no ruling** — pre-cut fix.

## Found here

- **Right-edge chart label cut** in every set (2–4 per run): last value tick / last category runs 5–19px past `.dv-stage` (`overflow-x:auto`) end edge (`probe_edge.py`, `edge-runs*.json`; seen on cand2-r2 "Middle East and Afric", "1500 £"). **Engine** (right-end twin of ds-012(b)); G8 blind because it treats a scroll box's end edge as reachable.
- **Harness/gate: rows hidden by a data grid's own scroll box counted as G7 collisions** with the pager and hint (`probe_grid.py`, `probe/grid-cand2-r1-payments.png`: no overlap on screen). Nested scroll frames; W4b's X-scroll repair compares within the outer frame.
- Run-level slips (not canon): "raised NaN Sep" (cand2-r1), "−2781.4% down" (cand2-r2), donut totals without a unit.

## Limits

1440 only for views; 390 is gate-only (overview). Three runs a side. Adjusted column is sample-based. Shots release the shell frame (declared, R4s RELEASE css). The earlier six are re-drawn, not re-built.

## Files

- `notes/_REVIEW-304-candidate-2-2026-09-27-v1.html` (builder `notes/_lanes/304/R4s2/build_review.py`; house CSS from the R4s review, overlay verbatim from the Apollo-MCP proposal v2 with CFG swapped; QA renders `R4s2/qa/`, no page errors, no horizontal scroll at 1440 or 390)
- `notes/_lanes/304/R4s2/`: `score_one.sh`, `runs/cold-cand2-r{1,2,3}/`, `restage_c2.py`, `mkruns_c2.py`, `views_c2.sh`, `runs-c2canon/`, `gates/` (geometry 1440/390 + own-size 1440, all pages), `ink-sets.json`, `shots.py` + `shots/`, `probe_grid.py`, `probe_size.py`, `probe_edge.py`, `edge-runs.json`, `edge-runs-c2canon.json`, `probe/`
- Do not stage: `R4s2/qa/*.png` if QA renders are not wanted in the tree.

## `_state` row spec

```json
{"id": "W-304s2", "title": "#304 R4s2 filed report - candidate 2 scored on every view: ink 5.10/view vs the six on the same engine+canon 5.53 (v1013 5.43, cand1 5.63), 6.62 as shipped; adjusted 3.73 vs 4.27 vs 5.30; six reported defects verified and classified, two found; recommend cut v1.0.14 from candidate 2 plus two gate-code fixes", "home": "notes/_subreports/2026-09-27-304-R4s2-candidate-2-scores.md", "links": ["notes/_REVIEW-304-candidate-2-2026-09-27-v1.html", "notes/_lanes/304/R4s2/ink-sets.json", "notes/_lanes/304/R4s2/runs/", "notes/_lanes/304/R4s2/runs-c2canon/", "notes/_lanes/304/R4s2/gates/", "notes/_lanes/304/R4s2/shots/", "notes/_lanes/304/R4s2/probe_edge.py", "notes/_lanes/304/R4s2/probe_grid.py", "notes/_lanes/304/R4s2/probe_size.py"], "project": "apollo", "opened": 304, "state": "open", "owner": "claude", "condition": "stated", "body": "s218-D7 filed report, scoring seat R4s2 (#304). W4b harness w4b-2.0 on cand2-r1..r3 (all views, floor PASS x3). Like-for-like on render bytes = the six earlier runs restaged on the candidate-2 pack engine/canon/type (= HEAD 3100da99), which read identical to W4a's re-render class for class. Verified: dark grey ground = tile #1F1F1F (tokens canon.css:845-846; Dave's call); side-nav 640px (component); receipt gate counts APOLLO-DEMO fenced Data-grid script (_validate_receipt.inline_scripts; tooling); chart receipt address mint vs meta (Dave's line, then tooling); legend 16.7px = outer-scope leading-trim rule bleeding into nested chart legend spans (canon generator); KPI +4px = bento .spark-inline 44px outranks Kpi-tile 40px (same scope-bleed class); icon-source FP = gate_icons scans script bodies (tooling). New: right-edge chart label cut past .dv-stage end edge in every set (engine; G8 blind to end-edge); harness counts rows hidden in a data grid's own scroll box as collisions (nested scroll frames). Recommendation: cut v1.0.14 from candidate 2 Tuesday after the two gate-code fixes (no page change, no new cold run).", "closes_when": "Dave has seen the review page and answered the cut decision; a verifier that built none of it re-runs score.py views on one cand2 run with R4C_RUNS redirected and matches its ink row in ink-sets.json, and files under notes/_subreports/ citing this report"}
```
