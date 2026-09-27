# #304 W4a — the chart engine stops cutting, colliding and stretching

provenance: 304 · Sun 2026-09-27 · seat W4a (Opus 5.5) · mount HEAD `86249459` · nothing committed, no git writes on the mount, no `git status`, no Project memory · every build, regen and survey in a throwaway clone `$HOME/c4a` (full history, 1,636 commits) with a BEFORE worktree `$HOME/c4a-before` at HEAD (both die with the VM) · writes on the mount: the 36 files below (byte-identical to the surveyed clone), `notes/_lanes/304/W4a/`, this report
status: observed — every figure below was printed by a gate, a survey, the W4b harness or a browser measurement at this seat

## The answer

Three of the four fixes are in, each licensed by a ruling that already existed. The fourth, markers, has no ruled number and is written up for Dave, not enacted.

1. **Y-axis labels are no longer cut.** ds-012(b) makes the plot area follow the widest label. That fit is now on by default; before, a canvas had to opt in with `data-pl-fit`.
2. **Category and time labels no longer collide.** The labels are thinned on every fit, measured from each label's own width, keeping the latest period and every n-th label before it.
3. **A ring (donut or pie) is the same size on every load, and its box is the drawing, not the tile.** This is ds-030's "fixed diameter, no proportional scaling". The nondeterminism had one cause: the engine measured the canvas while a width transition was mid-flight.
4. **Markers and letters on dense series: STOPPED.** The behaviour itself has a basis in brand rule dv-line-008. The threshold (12) has none. The option is rendered side by side for Dave.

**Effect on the six cold runs.** The runs were re-staged against the HEAD engine (before) and the W4a engine (after), and every view was measured with W4b's harness (`w4b-2.0`). The same 60 views appear on both sides.

| | before | after |
|---|---|---|
| ink per view | 6.62 | 5.53 |
| cut ink (affected tiles) | 69 | 36 |
| collisions | 56 | 38 |
| dead ink | 79 | 65 |
| raw G8 glyphs cut | 148 | 36 |
| raw G7 text on text | 752 | 225 |
| raw G12 chart lost in its box | 14 | 2 |
| raw G6 dead space | 78 | 64 |

- Nothing went up. No class, on any view of any run, reads higher after than before.
- Size and markers do not move (163 and 30), because neither was in this lane's licence.
- **All 36 cut-ink findings left are the Kpi-tile label crop** that V3 held back for Dave (s261-D4). None is a chart.
- **The ring is now deterministic.** Over 8 fresh loads each, with reduced motion and reached by a nav click (the W4b recipe):
  - v1013-r2 Trade: before, 7 at a 580-wide viewBox and 1 at 1014; after, 8 of 8 at 300x260.
  - v1013-r3 Trade: before, 4 and 4; after, 8 of 8 at 300x260.
- **The tiles shrink.**
  - The v1013-r2 overview's ring tile goes from 1,221 to 356px.
  - cand-r2's ring row goes from 2,807 to 1,076px.

## Rulings read, and what each licenses

- **ds-030 (#103, Dave, RULED).** It reads: "Circular charts (donut, pie) are the exception to fluid-plot scaling - fluid container, fixed-diameter centred plot. figure/container takes 100% width; the circular SVG plot keeps its fixed diameter (no proportional scaling) and is horizontally centred. No distortion, height unchanged."
  - At HEAD, `Template-dashboard-bento`'s JS-on release (`figure.dv-fit-on .dv-svg{width:100%} … {height:auto}`) applied to rings too. So a ring's viewBox was scaled to the tile.
  - That broke the ruling in two ways: a 350px ring (scaled), and a 1,221px tile holding a 200px ring (a box the drawing does not fill).
  - **Licenses fix 3.**
- **DV-D02 / DV-D02-A** (`knowledge/_proforma/_DATAVIZ-DECISIONS.md`:36-55). "Donut / pie graphic — EXCLUDED: compressing a circle distorts it" (DAVE-HEDGED on scaling between breakpoints, deferred to the 12-column work). The fix does not scale a ring at any width, so it stays inside the hedge.
- **ds-012(b) (RULED 2026-07-27, `_DS-IMPROVEMENTS.md`:354-382).** It reads: "the plot area is computed from the widest label, not a fixed number … (a) fixes an instance; (b) fixes the class."
  - Opt-in (`data-pl-fit`) was how it was first shipped; the ruling itself has no opt-in. On 5 of 6 cold overviews the attribute was missing (W3b §2 item 2).
  - Point 3's floor and ceiling constants stay `PROVISIONAL-AWAITING-DAVE`, untouched (0.42 of the width, 2px).
  - **Licenses fix 1.**
- **Label thinning** has no ruling of its own. The basis:
  - W3b §2 item 3 said it needs none.
  - Canon already thins at draw time: candlestick shows first and last past a dozen; histogram uses a stride from an estimated width.
  - dv-010 says nothing may obscure the data.
  - Tension, declared: dv-line-003 (ADVISORY brand rule) asks for "per-category X labels". Every category stays in the table and in every mark's tip (dv-005).
  - The 8px clearance is borrowed from the kit's own label offset (`data-dx="8"` in every partial). It is not ruled.
- **Markers.**
  - dv-line-002 says "Single data set: markers not required".
  - dv-line-008 says "End-line markers + key when markers would obscure small intervals" (ADVISORY; an `edges.obeys` on chart-line, s277-D1 enacted). The behaviour has a basis; the threshold does not.
  - G11's 12 is confirmed. `dv-render-line.js`:56 says "The kit's Batch-8 EASED marker cadence, promoted verbatim from the proforma at twelve points". That is the count the proforma was authored at, not a ruling. `_rulings.json` has no marker threshold; I searched it for marker/tick/every point/twelve.
  - The stacked-area in-fill letter "per band per x" is the reviewed recipe in `Chart-stacked-area.reference.html`:28-29, so one letter per band would be a design change.
  - **→ STOPPED; see the Dave questions.**
- **DV-D13, DV-D10, ds-031** are untouched. The centre is still raw form. The line end-key stays. The legend-offset row stays.

## What changed (36 files; list at `notes/_lanes/304/W4a/changed-files.txt`, patch at `w4a.patch.txt`)

**Sources (5).**

- `knowledge/canon/dv-behaviour.js`
  - `gutterPL` defaults to `[data-fx="0"][text-anchor=end]`: the labels that live in the gutter (value ticks, h-bar categories, bullet names, candlestick ticks). Every engine end-anchored text is one of these (checked by grep). An authored `data-pl-fit` still wins, and `data-pl-fit="none"` opts out (it matches nothing, so the floor stands).
  - New `thinLabels(svg)`, called at the end of `fitOne` on every fit. It groups `.dv-label[text-anchor=middle]` rows by baseline and finds the smallest stride at which the measured boxes clear by 8px, anchored on the last category. It writes `visibility` hidden or visible on each label, so nothing moves and nothing scales. A label in a hidden view measures 0 wide and is skipped.
  - A behaviour-identical refactor paid for the bytes. `Y.f(px)` in `fitY` now replaces a duplicated `PT0/pl0` line in the polyline branch; it is the same formula. **All 27 chart receipts re-drove with every measurement byte-identical**: only the source hashes and the `driven` stamp moved.
- `knowledge/canon/dv-render.js`: the viewBox is written from `ctx.VW`, so a fixed-frame type sets its own frame (+4 bytes).
- `knowledge/canon/dv-render-donut.js`
  - The ring's frame is the canvas's authored numeric `width` (the snippets' 300 and 592 are unchanged), else VH+40.
  - It writes that frame back as `width` and `height`.
  - It no longer reads layout, so it is deterministic by construction.
- `knowledge/snippets/Template-dashboard-bento.reference.html`: one rule, `figure.dv-fit-on[data-dv-type="donut"] .dv-svg,figure.dv-fit-on[data-dv-type="pie"] .dv-svg{width:auto; height:auto;}`. Under that rule the box falls back to the attributes, which was browser-checked: 300x260, not 1000x867.
- `knowledge/canon/canon.css`: regenerated. The diff is that rule, scoped.

**Regenerated by their generators, in the clone (31).**

- 15 snippets re-injected by `gen_component_partials.py`: `Chart-{bar,boxplot,bullet,butterfly-h,butterfly-v,candlestick,combo,donut,histogram,line,pie,scatter,sparkline,stacked-area}` and the template.
- 15 showroom pages from `gen_showroom.py` (the 14 `chart-*` pages and `template-dashboard-bento`).
- `knowledge/_BEHAVIOUR-GATE.md` (`_validate_behaviour.py --write`).
- `knowledge/_tests/chart-engine/_receipts.json`: re-driven in four `--page` batches with `notes/_lanes/304/R3/drive_shim.py`, 27/27 FRESH.

⚠ **Page budget.** The worst member page, Chart-combo, is at 34,704 of 34,816 code-only bytes (100%, 112 bytes of headroom). The first draft of the thinning blew it by 723 bytes. The budget is Dave's number (#96), so the code was compressed and deduplicated rather than the cap moved. The next engine change on the combo page will need a saving first.

## Regen recipe (for the commit seat; nothing needs re-running on the mount)

The mount's 36 bytes are the surveyed bytes: `cmp`-identical to the clone, and every mount copy equalled HEAD before the copy.

On the mount these are green:
- `gen_component_partials --check`
- `gen_canon_components --check` (137)
- `gen_showroom --check` (137 plus the index)
- `_validate_behaviour`
- `_drive_chart_engine --check` (27 FRESH)
- `_validate_dataviz`
- `_validate_descender_clip`
- `_validate_geometry --selftest` (OK with the new template CSS)

If a regen is ever needed, the order is: edit the sources → `python3 knowledge/gen_component_partials.py` → `python3 knowledge/canon/gen_canon_components.py` → `python3 knowledge/gen_showroom.py` → `python3 knowledge/_validate_behaviour.py --write` → re-drive the receipts. The re-drive runs at the seat after `source knowledge/_render/seat_env.sh`:
- `python3 notes/_lanes/304/R3/drive_shim.py --page bar.html … --page combo.html`
- `python3 notes/_lanes/304/R3/drive_shim.py --page donut.html … --page stacked-area.html`
- the same for the 14 `Chart-*.reference.html`, two batches of seven.

Then run the C1 serial as `--check` (`_render_rulings`, blast radius, memento index, mention map, `_gen_chain`, schematic). The step count is unchanged (148), so there is nothing for the `[121]` trap.

## Test it hard: what ran

- **Geometry gate on canon** (W4b's gate, 1440; 13 test pages, 14 chart snippets, the bento template, Legend). BEFORE 11 findings on 29 pages, AFTER the same 11, so 0 new false positives. The 11 are pre-existing: sparkline ×2 pages, the bento's known G10. Files: `g-before.*`, `g-after.*`.
- **The six cold runs, every view.**
  - `restage.py` builds `$HOME/w4a/st/{head,after}`. Each run's pages get the tree's `dv-*.js` in place of their inlined engine blocks (v1013-r2 55 blocks; the cands 16 each), and the tree's `canon.css` and `type.css`. The v1013-r1/r3 pages load their engine by `src`.
  - `R4C_RUNS=$HOME/w4a/runs-{head,after} python3 score.py views --run-id cold-…` then measures them.
  - The comparison is in `compare.json`, built by `compare.py`. It uses the intersection of kept views, because the after run of cand-r2 kept one extra duplicate overview view.
- **Ring determinism.** `probe_vw.py`, `probe_vw2.py` and `probe_vw4.py` give the numbers above.
  - The cause was caught in the act. At the `dvRender` call a `CSSTransition` on `width` (580px to 100%, duration 1e-05s under reduced motion) was running, and the svg read 580 while its row read 1014.
  - One load read 0: a `flex-shrink` transition was in flight.
- **Looked at, 1440, light and dark** (`notes/_lanes/304/W4a/renders/`):
  - `ring-trade-v1013r2-{light,dark}.png`: the pie figure goes from 1014x1173 to 1014x308.
  - `ring-row-{v1013-r2,cand-r2,v1013-r3}-before-after.png`.
  - `axis-candr3-overview-fig0{0,1}-{light,dark}.png`: "00 £m" becomes "6000 £m" and "1000 £m"; 30 colliding dates become every second date, ending 25 Sep.
  - 4x crops `axis-candr3-yaxis-4x-light.png` and `axis-candr3-xlabels-*-4x.png`: glyphs whole in both themes.
- **Survey, all 148 steps**, in the clone at HEAD (BEFORE worktree) and HEAD plus this diff (AFTER), `--include-mutating --resume --timeout 60`, six chunks each (logs in `notes/_lanes/304/W4a/survey/`).
  - Both sides: FAIL `[81] [86] [94] [127] [128] [132] [134] [135] [144]` · could-not-ask `[10] [13] [61] [68] [136]` · timeout `[73]`. That is V3's set.
  - **0 green→red.** Every failure-detail block is identical. `_validate_grid` and `_validate_token_forks` outputs are byte-identical across the trees.
  - The survey re-dirtied none of my 36 files, so the generators are idempotent over these bytes.

## Dave's questions (for Tuesday's page; renders in `notes/_lanes/304/W4a/renders/`)

1. **Dense series: markers and letters.**
   - Render: `DAVE-markers-stacked-area-{light,dark}.png` and `DAVE-markers-multiline-{light,dark}.png`. Today's page is on the left. On the right is a RENDER-ONLY mock: above 12 points, the end marker only, and one letter per band.
   - "Plus a key when markers would obscure small intervals" (dv-line-008) gives the behaviour. The number is yours: 12 is the proforma's authoring count, and G11 declared the same number.
   - The stacked-area letter per point is the reviewed recipe, so one letter per band is your call too.
2. **Does a ring's tile hug its content or fill its row, and does a ring get a narrow column by when-rule?**
   - Render: `DAVE-ring-tile-{v1013-r2,cand-r2}-fill-vs-narrow.png`. A is today after this fix (the tile fills a full-width row; the ring is centred and the legend sits at the row's right edge). B is a RENDER-ONLY mock of a half-width column (the legend drops below the ring).
   - With the ring no longer stretched, hug and fill differ only where a ring shares a row with something taller. On v1013-r3 the ring tile is already the tallest in its row (631px, because the legend wraps below in a 384px column), so hug and fill read the same there.
3. **Seen, not fixed (no ruling; a design call).**
   - The multi-line "Sterling indexed to 100" draws flat on a zero-based axis. The core's zero floor is a bar rule, dv-line-001 makes zero optional for lines, and `fn.zeroBaseline = false` exists but no line type sets it (see `dv-render-line.js`'s own CORE REQUEST). Visible in `DAVE-markers-multiline-*.png`.
   - The line end-keys collide when series end close together: 3 collisions on cand-r3 FX. DV-D10 keeps the end-key "pending Dave's a11y check".
   - The stacked-area first-point letter is half outside its band.
   - In a wide tile, `margin-inline:auto` on the ring svg (ds-030 enactment) pushes the legend to the row's far right.

## Limits

- Everything was measured at the arm64 seat with the HSBC face; x64 CI is predicted from the clone.
- The harness measures 1440 only; the six runs were not measured at 390.
- The cold pages were measured against HEAD's `canon.css`, not their own packs, so that the before/after is attributable. The pack-as-shipped row (W4b's) matches HEAD on every class except G7 on cand-r3 (149 v 144) and G12 on v1013-r3 (3 v 2).
- G12 still fires on 2 views. One is a ring at its ruled 300x260 frame reading 34% against G12's declared 35%. The ring there is exactly ds-030's size, so that is a threshold question, not a defect.
- Thinning hides labels with `visibility`. A page script that also thins (v1013-r2 has its own) is superseded on every fit; the result was measured as 0 collisions both sides.

## `_state` row spec

```json
{"id":"W-304ga","title":"#304 W4a filed report - chart engine: axis-gutter fit on by default (ds-012b), measured label thinning, ring frame fixed and deterministic (ds-030); dense-series markers STOPPED for Dave","home":"notes/_subreports/2026-09-27-304-W4a-chart-engine-ink.md","links":["knowledge/canon/dv-behaviour.js","knowledge/canon/dv-render.js","knowledge/canon/dv-render-donut.js","knowledge/snippets/Template-dashboard-bento.reference.html","knowledge/canon/canon.css","notes/_lanes/304/W4a/compare.json","notes/_lanes/304/W4a/renders/"],"project":"apollo","opened":304,"state":"open","owner":"claude","condition":"stated","body":"s218-D7 filed report, wave four seat W4a (#304). ds-012(b) gutter fit is the default (opt-out data-pl-fit=none); category labels thinned at fit time from measured widths (8px clearance borrowed from the kit's label offset, declared); the ring keeps its authored frame and is no longer stretched by the bento template's fluid release (ds-030) - 8/8 loads 300x260 where HEAD was bistable. Six cold runs, same 60 views, HEAD engine vs W4a: ink/view 6.62 -> 5.53, G8 148 -> 36 (remainder = held-back Kpi-tile), G7 752 -> 225, G12 14 -> 2, nothing up. 148-step clone survey: no green-to-red. 27 receipts re-driven, measurements byte-identical. Page budget now 34,704/34,816. Markers-on-dense-series and tile hug/fill + ring narrow column are Dave's, rendered.","closes_when":"a verifier that built none of it re-runs _drive_chart_engine --check, _validate_behaviour and the W4b views phase on one restaged cold run at the seat, matches its row in compare.json, and files under notes/_subreports/ citing this report; Dave has seen DAVE-markers-* and DAVE-ring-tile-* and said which"}
```
