# #304 W4b — the instruments now see ink

provenance: 304 · Sun 2026-09-27 · seat W4b (Opus 5.5) · nothing committed, no git writes, no Project memory · wrote only `knowledge/_validate_geometry.py`, `knowledge/_tests/geometry/`, `notes/_lanes/304/R4c/harness/` and `notes/_lanes/304/W4b/` (plus seat-local stage copies under `$HOME/r4c/stage/st-*`)

## The answer

The geometry gate's G6 miss on v1013-r2 had one cause, and chasing it turned up two more blind spots of the same kind: the gate could not see the pages the cold runs actually build. All three are fixed at their cause. Each has a lever that puts the old reading back, and the selftest proves each one. Two clauses are new: marks on every point (G11) and a chart lost in its box (G12). The gate stays ADVISORY.

The harness now scores every view of a run. That is ten destinations on all six runs, where the candidates were scored on one view before. It reads text after script has written it, and it tests the theme switch in both directions using the run's own controls. The score is restructured the way W3b asked:
- the four rubric parts are a pass/fail FLOOR;
- INK is the comparable number;
- two judgment rows are printed with their evidence and left blank for Dave.

**The new baseline.** All six runs pass the floor. The legacy /12 sum is now 11–12 on every run, so it is fully saturated, as W3b predicted. On ink the candidate is not better: 7.0 defects per view against v1.0.13's 6.2. The gap is almost all cut ink: 1.9 per view against 0.4, which is the y-axis labels cut at the chart's left edge.

## 1. The G6 miss, reproduced, and its cause

**Reproduced.** The R4b gate on v1013-r2 at 1440 found 0 G6 (`geo-v1013-r2.json`). A dump of the gate's own model (`W4b/dbg_g6.py`) shows why. The ring tile, `section.c-bento__tile.c-bento` at 1062×1221, wears `.c-bento`, so the gate classes it as a GROUP. Its one panel inside, `div.c-bento__tile.stat-card`, is never enumerated as a tile, because the wall walk only collects tiles that sit two or more to a grid.

A one-panel group's panel was never measured. The reference bento wraps even a one-panel row as a group, so every such panel was blind.

**Fixed.** Lone panels are now leaves, and G6 measures them. On v1013-r2 the ring tile reads "259.9px of empty band between content blocks", and G12 reads "the chart's ink covers 21% of its box (ink 433x430 in a 1014x879 box)". W3b's probe said 351px because it released the shell frame; the gate measures the page as shipped. The v1013-r2 page is now a real-page selftest leg: the frozen run is staged beside the v1.0.13 zip in `$TMPDIR`. With lever `X-lone` switched on, its G6 disappears, which reproduces R4b's reading.

**Two more blind spots, found on the same pages.**
- **X-scroll, the app shell.** The cold runs scroll an inner box (`.sh-content`), not the window.
  - G7 clipped every text run to that box's *viewport*, so nothing below the inner fold could ever collide. cand-r3's thirty overlapping axis dates read 0.
  - G8 stopped at any scroll box as "reachable". But content past a scroll box's START edge is not reachable, and every "00 £m" y-label hangs left of the chart's `overflow-x:auto` `.dv-stage`.
  - Now a scroll box clips to its scroll area, from its origin out to its scrollable overflow. Runs unrolled through a scroll box are compared only within that scroll frame. The page's inner scroll boxes are walked before measuring.
- **X-own, a false positive this exposed.** A text run was clipped only by its ancestors, never by its own element, so an ellipsis title's hidden tail "collided" with the tag beside it. That produced 8 false G7 on the snippet references, and 40 on the showroom index once its inner scroll was read. Both are now gone. The clean fixture carries a guard for this case: with `X-own` switched on, the guard fires.

**Also.** Every finite CSS animation is finished before the gate measures, so entry motion cannot be read mid-flight. Every finding now carries `tile`: "T<n>" for a tile, "L<n>" for a lone panel.

## 2. The new clauses

| Clause | Designer rule | Tolerance and why |
|---|---|---|
| G11 marks on every point (minor) | One series of a chart carries a mark of one kind on every one of more than 12 points: point glyphs (grouped by `data-series-group`, else by fill), or one letter key repeated. It counts only when a line or band in the same chart has exactly that many vertices (twice as many for a closed band), so a scatter's points never count. | **12.** No ruling exists (searched `_rulings.json`). The kit's marker proforma was authored at twelve points (`dv-render-line.js`: "promoted verbatim from the proforma at twelve points"), and W3b §3 proposes markers off above about 12. Declared; Dave may move it. |
| G12 chart lost in its box (minor) | A chart (the outermost svg, at least 160×100, not `pAR=none`) whose marks together cover less than 35% of its own box. | **35%.** A ring that fits its box covers about 75%; line and bar charts cover 80% or more. The v1013-r2 ring reads 21%, and cand-r2's rings read 5%. |

Cut ink and label collisions were not missing clauses. G8 and G7 already covered them, and they were blind for the X-scroll reason, so they are repaired rather than duplicated. Dead ink is G6 (including lone panels) plus G12.

## 3. Test it hard: the gate

`python3 knowledge/_validate_geometry.py --selftest` returns **GEOMETRY SELFTEST OK** (`W4b/selftest-geometry.txt`). It covers:
- **Planted clauses:** 13 of 13, each caught on its planted element, including G11 and G12 on new fixture sections.
- **Sub-cases:** 4 of 4 — G6-lone, G7-shell, G8-scroll, G11-letters.
- **Clean fixture:** 0 findings at 1440 and 390.
- **Reference bento:** only its 4 known-true G10 findings.
- **The #288 page:** G1b, G3, G5 and G6 still named.
- **Mutations:** 13 clause switches, each letting exactly its own planted defect through.
- **Cause levers:** 3. `X-lone` and `X-scroll` let exactly their sub-cases through and move nothing else; `X-own` re-opens only its guard.
- **The real v1013-r2 leg:** as described in §1.
- **Determinism:** the selftest run twice gives identical output.

The generator is `notes/_lanes/304/W4b/gen_fixtures.py`, R4b's generator extended; R4b's own copy is left untouched. The own-size fixtures changed only in their header comment.

**Zero false positives from the new clauses.** Each corpus was swept at 1440 with the old gate (the pre-W4b copy) and the new gate, and the results diffed (`W4b/fp/`):
- **Snippet references (137 pages):** 0 findings added. 8 false G7 were removed (the X-own class).
- **Showroom (138 pages):**
  - G11 and G12 add 0 findings.
  - The scroll repair adds 0 G7 and 0 G8.
  - The only movement is on `showroom/index.html`. The inner-scroll walk now loads the catalogue's lazy thumbnails, so two cards now show a "no thumbnail" placeholder. That renamed one existing G6 and added one G6: a 59px band under a card with no image, which is a true reading of the page as scrolled.
- **Own-size:** `--selftest` is OK. Its showroom button and table legs still read 0 findings (`W4b/selftest-own-size.txt`). R4b's 0-FP baseline holds.

## 4. The harness

- **`views` phase** (`harness/views.py`, new).
  - **Discovery:** it clicks each nav item in a fresh context and measures the page where the click left it, so linked files, `?view=` routes, `#/` routes and script-only views are all reached.
  - **Deduplication:** a real link is identified by its URL; a button is identified by its main text.
  - **Measurement:** the gate's own code at 1440×900.
  - **Also read:** rendered text against the profile's words, charts (cut only by hidden/clip ancestors or a scroll box's start edge), and the theme switch in both directions.
  - It is resumable.
- **Drive.** It now tries first the theme control that names the other mode. It used to click "Light" on a light page, which was R4s harness defect 1.
- **Score** (`score.py`, `HARNESS_VERSION w4b-2.0`).
  - FLOOR: each rubric part must reach 2, and the parts are never summed.
  - INK has five classes: dead, cut, collisions, size drift, markers.
    - A unit is an affected tile for the four geometry classes. For size drift it is a *kind* (component, clause and part, with the text stripped), so six legend keys at 16.7px count as one defect.
    - THE comparable number is **defects per view**. Every run is scored on all its views, and lower is better.
    - Per 10 leaf tiles is shown beside it, but not as the headline, because tile counts depend on how a run marks up its tiles (cand-r2 has 31 tiles across 10 views).
  - Worst case per class.
  - Two judgment rows, with evidence, answered "Dave: ______": the overview's headings for the three-question sections, and every ring chart with its tile's share of the content width.
  - `total` is kept and labelled legacy. The `R4C_RUNS` environment variable redirects writes, so a re-score never touches R4c's runs.
- **Tested.**
  - `score.py selftest-views` passes 16 of 16 (`W4b/selftest-views.txt`):
    - each ink class planted > 0 and clean = 0;
    - the ink reading identical when measured twice;
    - three routing shapes (#/, ?view=, script-only) each give 3 views, read the script-written "headroom" (it is not in the source), and switch the theme light → dark → light;
    - a one-way-switch mutant fails.
  - R4c's own `selftest` passes 8 of 8 on the restructured score, run on copies of its fixture runs (`W4b/runs-fx/`).

## 5. The six cold runs re-scored: the new baseline

Harness `w4b-2.0`. The data is `notes/_lanes/304/W4b/runs/compare-six.html` and `.json`, and every run has a `scorecard.html`.

| run | R4c /12 (as run) | R4s like-for-like /12 | views scored, before → now | theme, before → now | floor (new) | legacy sum now | **ink per view** | dead | cut | collisions | size (kinds) | markers | worst dead band | gate score @1440, R4b → W4b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1013-r1 | 9 | 9 | 10 files → 10 | FAIL → PASS | PASS | 11 | **7.3** | 15 | 6 | 19 | 28 | 5 | 469px | 1 → 0 |
| v1013-r2 | 10 | 10 | 10 files → 10 | FAIL → PASS | PASS | 12 | **3.9** | 6 | 0 | 0 | 27 | 6 | 356px (ring covers 7%) | 1 → 1 |
| v1013-r3 | 11 | 11 | 10 files → 10 | FAIL → PASS | PASS | 11 | **7.4** | 24 | 7 | 9 | 29 | 5 | 189px | 1 → 1 |
| cand-r1 | 8 | 10 | 1 → 10 | FAIL → PASS | PASS | 12 | **8.0** | 16 | 18 | 9 | 31 | 6 | 169px | 1 → 0 |
| cand-r2 | 7 | 9 | 1 → 10 | FAIL → PASS | PASS | 11 | **5.2** | 11 | 8 | 7 | 22 | 4 | 367px (ring covers 5%) | 1 → 0 |
| cand-r3 | 9 | 11 | 1 → 10 | FAIL → PASS | PASS | 12 | **7.9** | 7 | 30 | 12 | 26 | 4 | 99px | 1 → 0 |

Group means per view: v1.0.13 against the candidate.

| | v1.0.13 | candidate |
|---|---|---|
| ink, all classes | 6.2 | 7.0 |
| dead | 1.5 | 1.1 |
| cut | 0.4 | 1.9 |
| collisions | 0.9 | 0.9 |
| size | 2.8 | 2.6 |
| markers | 0.5 | 0.5 |

Every run has a series carrying 30 markers on 30 points. v1013-r2 reads 0 collisions because its engine thins alternate date labels (`visibility:hidden`); W3b's probe counted the hidden ones. `rich` is now 3 on all six, because charts are counted over ten views and a chart below a shell's fold no longer counts as clipped (R4s harness defect 4).

**What the new numbers say.** Taking them with W3b's reading:
- The candidate composes, but it carries more cut ink.
- v1013-r2, the stacked single column with thinned labels, is the cleanest page on ink.
- Nothing separates the groups on dead ink, markers or size drift. Those defects are the engine's and canon's, shared by both arms.

## 6. Determinism

The views phase was run twice on all six runs (`runs/` and `runs-rerun/`, compared by `W4b/determinism.py`, output in `determinism.txt`). The result is **PASS**: 60 of 60 views identical in URL and ink, with one exception.

**The exception is the page, not the instrument.** v1013-r3's Trade ring is bistable across loads: 132px on 10 of 12 fresh loads and 200px on 2, each load stable for 3 s (`W4b/probe_ring_bistable.py` / `.txt`). v1013-r2's Trade ring is bistable in the same way: 350px on 6 of 8 loads and 200px on 2. Both runs' dead-ink counts can therefore move by ±1 between renders.

**New engine finding, for the lane that fixes W3b's cause #1.** The ring's diameter depends on load timing.

The v1013-r2 overview's text signature also moved between loads while its ink did not. That is informational only.

## 7. Limits

- Everything was measured at the arm64 seat with the HSBC face, at 1440 only for the views; 390 is still gate-only.
- Own-size references are the repo's HEAD snippets, not each run's pack. That is the same for all six runs.
- G11 recognises dv markup, plus any chart whose line vertex count matches its glyph count.
- G12 counts text inside the svg as ink.
- Discovery depends on the nav selectors, and is capped at 14 views.
- R4b's 26-page baseline was not re-measured with the new gate. Expect lower scores wherever app shells hid collisions and cut labels.

## 8. Changed files (for the commit seat)

- `knowledge/_validate_geometry.py`: G11, G12, three repairs with levers, FINISH_ANIMATIONS_JS, `tile` on every finding, and new selftest legs.
- `knowledge/_tests/geometry/geometry-planted.html`, `geometry-clean.html`: regenerated. `own-size-planted.html`, `own-size-clean.html`: header comment only.
- `notes/_lanes/304/R4c/harness/`:
  - new: `views.py`, `fixtures/fx-views-hash.html`, `fx-views-query.html`, `fx-views-script.html`, `fx-theme-oneway.html`, `fixtures/_nopack/README.txt`;
  - edited: `score.py`, `browser.py`, `selftest.py`.
- `notes/_lanes/304/W4b/`: `gen_fixtures.py` (the fixtures' home now), the patch scripts, probes, `fp/`, `runs/`, `runs-rerun/`, `runs-fx/`, `gate-six/`, selftest logs, `determinism.*`, `probe_ring_bistable.*`.
- **Do NOT stage** `W4b/*.pre-W4b.py.txt`. They are rollback copies.
- `_build_all.py` is untouched, and the step count is unchanged (148).
- The gate's `--build` selftest now unzips the v1.0.13 dist (about 20 MB) into `$TMPDIR` when a browser is present. CI still has no browser, so it declares 77.
- The real-page leg SKIPS, and says so, if `notes/_lanes/304/R4c/cold/v1013-r2/out` is not committed.

## `_state` row spec

```json
{"id":"W-304gb","title":"#304 W4b filed report - the instruments see ink: G6 lone-panel, app-shell scroll and own-clip blind spots repaired with levers; G11 marks-on-every-point and G12 chart-lost-in-box added; harness views phase + floor/ink score; six cold runs re-baselined","home":"notes/_subreports/2026-09-27-304-W4b-instruments-see-ink.md","links":["knowledge/_validate_geometry.py","knowledge/_tests/geometry/geometry-planted.html","notes/_lanes/304/R4c/harness/views.py","notes/_lanes/304/R4c/harness/score.py","notes/_lanes/304/W4b/runs/compare-six.html","notes/_lanes/304/W4b/determinism.txt","notes/_lanes/304/W4b/probe_ring_bistable.txt"],"project":"apollo","opened":304,"state":"open","owner":"claude","condition":"stated","body":"s218-D7 filed report, wave four seat W4b (#304). Geometry gate: 13 clauses, 4 planted sub-cases, 3 cause levers, W3b's v1013-r2 ring tile as a real-page leg; 0 new-clause findings on 137 snippet references and 138 showroom pages. Harness w4b-2.0: every view, rendered text, theme both ways, floor pass/fail + ink per view. New baseline: all six pass the floor; ink per view v1.0.13 6.2 vs candidate 7.0 (cut ink 0.4 vs 1.9). Engine finding: ring diameter is bistable across loads on v1013-r2/r3 Trade. G11 tolerance 12 and G12 35% are declared, not ruled.","closes_when":"a verifier that built neither re-runs the geometry --selftest and score.py selftest-views at the seat, re-scores one cold run and matches its ink row, and files under notes/_subreports/ citing this report; Dave has seen the ink row and said whether the G11 threshold (12) stands"}
```
