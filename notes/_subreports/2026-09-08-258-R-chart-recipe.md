# 258 lane R — one data-driven chart recipe (rule 18)

**Landed:** `apollo-spider/skills/generate-from-canon/SKILL.md` lines 191–238 — new **rule 18
"Charts from data — the interim recipe"**, immediately after rule 17, before `## Procedure`.
28 lines of prose + a 15-line JS example. Marked interim: *"A library engine replaces this in
v1.0.9"*. No snippet, meta, canon or `_screen-gate` file touched.

## The grammar, quoted from `knowledge/canon/dv-behaviour.js`

`fitOne()` re-derives every x as `PL + data-fx × plotW` after re-pinning the viewBox 1:1
(`svg.setAttribute('viewBox','0 0 '+W+' '+H)` — DV-D02, text never scales). Per element:

| element | attributes it must carry |
|---|---|
| `rect` | `data-fx` (+ `data-fw` for width) |
| `line` | `data-fx` + `data-fx2` |
| `text` | `data-fx` + `data-dx` |
| `polyline` / `path` | `data-fxs` + `data-ys` (space-separated) |
| `g` | `data-fx` + `data-x0` (emitted as a translate) |
| size-preserving glyph | `class="dv-mk"` (the VFIT mark contract) |
| the svg itself | `data-pl/-pr/-pt/-pb/-h/-h-min` (kit defaults 46/12/14/30/260/200) |

y is **not** authored: `fitY()` caches `data-fy` / `data-fh` / `data-fy1` / `data-fy2` /
`data-fys` / `data-pts0` on first fit as plot fractions.
Tooltip = `data-tip` only — `dvTip` is created by the script and driven by ONE delegated
`pointermove` + `focusin`/`focusout` at `document`; `tipAt` re-homes it into
`src.closest('[class*=cn-chart-]')`. The ONE resize listener is rAF-debounced and calls
`fitCharts(); placeSegs();` — so `dispatchEvent(new Event('resize'))` is the only re-fit hook
a renderer can call. That is exactly what cold run 5 does (`arm-A-blind/dashboard.html:1202`,
`renderAll()` → *"dv-behaviour re-fits the freshly emitted columns"*).

## The trap the cold runs did NOT know

`canon.css` namespaces every `.dv-*` rule as `:where(.cn-chart-bar) …` — the svg box
(`.dv-svg{width:580px;height:260px}`, line 7318), the grow keyframes (7337–7338), the tip
(`.dv-tip{position:fixed…}`, 7544). The v4 and v5 cold runs emitted correct `data-fx`/`data-fw`
geometry but wrapped it in nothing (`grep -c cn-chart dashboard.html` → **0**), so the bars
never animated and the tip was an unstyled div. The series *fills* survived only because
`--data-series-1…5` are also declared on the two `:root` theme blocks (canon.css 401 / 786).
Rule 18 trap (a) records this; traps (b) theme attrs on `<html>` and (c) delegate to a static
ancestor carry forward from cold runs 5 and 3.

## Proof — recipe-only test page, driven

`/tmp/r258/chart-recipe-test.html`, 78 lines, written from rule 18 as published (skeleton,
attribute table and the JS example copied out of the rule; the dashboards were not re-opened).
Rendered headless with `LD_LIBRARY_PATH=$HOME/.local/chromelibs
PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1 python3 drive.py`.

| check | result |
|---|---|
| pageerrors / console errors | **0** |
| bars animate | heights at t=60ms `22.8 / 3.2 / 0` → at rest `95.5 / 40.9 / 216.0` |
| tooltip on hover | `#dvTip` `.on`, text `Groceries: 420`, `position:fixed`, parent `.cn-chart-bar` |
| re-render after a data change | `[95.5, 40.9, 216, 59.1, 47.7, 68.2]` → `[23.9, 10.2, 216, 14.8, 12.1, 17.1]`; entry animation re-fires (t=60ms `4.3 / 0.19 / 0`) |
| fit engine engaged | `data-fy="0.5579" data-fh="0.4421"` cached by `fitY`; viewBox re-pinned `0 0 1152 260`; bar width 102→61px on a 1200→760 viewport |

The recipe passed **unchanged**. One correction was made to the *test*, not the rule: the first
data change scaled every category by the same factor, and a max-normalised chart is invariant
under that — a proportional change is not a change. The second run filters one category and
moves five of six bars.
