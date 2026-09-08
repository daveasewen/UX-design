# #260 lane F1 — SCATTER + HISTOGRAM type partials · subreport

**Both types are built, both snippets are re-pointed at the engine, and both were driven in a real
Chromium across 4 themes × 2 modes — 8/8 green each, zero page errors, zero console errors, eight
mutants red and two controls green.** `s259-D1`'s fast follower, two of its eight types.

Neither type needed the core changed and neither needed a literal raised: `dv-render-scatter` is
**4,148** code-only bytes of a 16,384 cap and `dv-render-histogram` is **2,218**; the two member
pages land at **24,930** and **15,266** of the 34,816 page budget — the first #260 members with
real headroom, because `s260-D1` had already made the engine core a shared payload.

**One red in the tree is MINE and it is the un-merged registry, not a defect** — see *Gates*.

## Files created / edited

| path | what |
|---|---|
| `knowledge/canon/dv-render-scatter.js` | **NEW** — 162 lines, registers `dvRender.types.scatter` |
| `knowledge/canon/dv-render-histogram.js` | **NEW** — 106 lines, registers `dvRender.types.histogram` |
| `knowledge/_tests/chart-engine/scatter.html` | **NEW** — the committed driven test page (2 canvases + legend) |
| `knowledge/_tests/chart-engine/histogram.html` | **NEW** — the committed driven test page (2 canvases) |
| `knowledge/snippets/Chart-scatter.reference.html` | both canvases EMPTIED; ids added; DATA + `dvRender()` bootstrap; 2 marker pairs; **`dv-legend` block MOVED below the bootstrap** |
| `knowledge/snippets/Chart-histogram.reference.html` | canvas EMPTIED; id added; DATA + `dvRender()` bootstrap; 2 marker pairs |
| `knowledge/components/Chart-scatter.meta.json` | typed `behaviour` block (+10 lines, no reformatting) |
| `knowledge/components/Chart-histogram.meta.json` | typed `behaviour` block + the stale baked-pixel `bins` note corrected |
| `knowledge/_tmp/260/{scatter,histogram}.registry.json` | the `$behaviour` entry + `consumes` for the integration lane |
| `knowledge/_tmp/260/{scatter,histogram}.core-requests.md` | 4 + 3 requests, verbatim |

⛔ Not touched: `component-types.json`, `dv-render.js`, `_receipts.json`, any gate, `canon.css`,
any other type's files, GOOD-MORNING/_LIVE-STATE/_CARRIES/_rulings/memory.

## Bytes — measured with `_validate_behaviour.code_only`, not estimated

| source | raw | code-only | of the 16,384 cap |
|---|---|---|---|
| `dv-render-scatter.js` | 10,020 | **4,148** | 25% |
| `dv-render-histogram.js` | 6,670 | **2,218** | 14% |

| member page | sum | of PAGE_BYTES 34,816 |
|---|---|---|
| **Chart-scatter** = dv-behaviour 13,048 + dv-legend 7,734 + dv-render-scatter 4,148 | **24,930** | 71.6% |
| **Chart-histogram** = dv-behaviour 13,048 + dv-render-histogram 2,218 | **15,266** | 43.8% |

The shared core `dv-render` (9,309) is excluded per **ADR-0015 Amendment 4 / `s260-D1`**. Both
figures are the gate's own, printed by `_validate_behaviour.py` run against a scratch tree with the
registry fragments merged: `[PASS] dataviz page budget — worst member 34209 … Chart-scatter 24930 …
Chart-histogram 15266`. The worst member is still Chart-combo, not mine.

## What each type actually does

**SCATTER — the numeric x axis is the whole difficulty.** Every other registered type reads
`spec.categories` as a BAND: n equal slots, order only. A scatter's x is a MEASUREMENT — 28→35 has
to be a visibly shorter step than 122→140 or the chart is a dot plot with sorted labels. The ruled
spec (s249-D4) has no numeric x, so the partial **parses a number out of each category** and, when
every one parses, builds its own x scale off `dvRender.util.nice` and emits the second axis
(vertical gridlines, x tick labels, left axis rule) itself; when any category is not a number it
falls back to band centres and draws an honest ordinal dot plot. **That is a LOCAL WORKAROUND for a
missing core field and it is filed as core request 1, not presented as the design.** Points are
`g.dv-marker[data-fx][data-x0]` wrapping a glyph and an invisible `circle.dv-hit` r=12 — the group
wrapper because `fitOne()` branches on TAG and has no `circle` branch (the #72 discharge shape), the
hit circle because AA 2.5.8 wants 24px around a 9px mark and the interactive attributes belong on
the target. §04.3: four shapes (circle/square/diamond/triangle) by series index, each `.dv-mk` so
the fit moves the glyph instead of stretching it.

**HISTOGRAM — contiguity is the type.** `band = plotW / bins` and the mark IS the whole band, edge
to edge, because the variable underneath is continuous and a gutter would assert a range with no
data in it. **There is deliberately NO geometric dv-004 gap:** `#96-D3` already met the 2px rule on
this type with a page-coloured 2px stroke in canon.css precisely because histogram bars touch, and
`_validate_dataviz.py` scopes dv-004 to donut/pie/stacked and never reads this type. Cutting a gap
would destroy the thing the chart exists to show; the partial says so at the seam. Two loud
refusals: a second series throws (a histogram is one distribution — `grouped-column` and
`stacked-column` already exist) and a negative frequency throws (dv-bar-009). Bin labels thin
themselves when the band cannot afford them.

## Driven — Chromium 151.0.7922.34, `goto("file://…")`, never `set_content`

Sandbox lacked `libXdamage.so.1`, the same obstacle lanes A and D hit at #259, resolved the same
way (`apt-get download libxdamage1` → `dpkg-deb -x` → `LD_LIBRARY_PATH`). Viewport 1180×900,
`reduced_motion=reduce`, `device_scale_factor=1`.

**⛔ NOTHING WAS WRITTEN TO `knowledge/_tests/chart-engine/_receipts.json`.** The committed driver
has no `--out`, so it was imported and its `RECEIPTS` constant re-pointed at `/tmp` before
`drive()` was called; the repo file is untouched and the integration lane records the real receipt.

### `scatter.html` — 8/8 identical, 8/8 green

- **0 pageerrors, 0 console errors** on load, on hover, after the filter and after the resize.
- **12 markers**, all 12 carrying `data-fx` **and** `data-x0`; **12 hit circles**, every one
  measuring **24.0px** across and carrying `data-tip` + `tabindex="0"` + `aria-label`.
- **THE NUMERIC AXIS, MEASURED.** Rendered point centres give a slope of **7.143 – 7.167 px per
  £1k across all 12 points** (constant to 0.3%), with adjacent gaps from **43.0px to 128.9px**
  where an evenly spaced band axis would have put every gap at **72.9px**. This is the assertion
  the type stands or falls on and it is measured, not asserted.
- **Ticks**: y `0 · 20 · 40 · 60`, x `0 · 50 · 100 · 150` — the same ticks the baked specimen
  shipped, now derived. Axis titles read back as `Monthly income (£000)` and `Savings (£000)`.
- **Tooltip**: hovering point 4 opens `#dvTip.on` reading **`Monthly income (£000) 55 · Savings
  (£000) 14`** — both coordinates, the same numbers the table row carries.
- **Filter re-renders (rule 14)**: unticking two income bands takes the plot **12 → 10 markers**
  and the **table spine 12 → 10 rows**, and drops those incomes out of the svg `aria-label`.
- **§04.3**: the segment figure draws **7 circles + 7 squares + 7 diamonds**, three distinct
  `data-series-group` values and three distinct computed fills — `rgb(118,102,130)`,
  `rgb(164,92,58)`, `rgb(87,124,120)` = `--data-series-1…3` — in all four themes. **0 dead fills.**
- **Resize** 1180 → 760: viewBox **`0 0 1132 260` → `0 0 712 260`** (the plot compresses, it does
  not scale), glyph `r` stays **4.5** and tick text stays **12px** — DV-D02, the cartesian
  assertion and the inverse of the donut's.

### `histogram.html` — 8/8 identical, 8/8 green

- **0 pageerrors, 0 console errors**; **8 bins**, all 8 carrying `data-fx` **and** `data-fw` **and**
  `data-tip` **and** `tabindex="0"`.
- **CONTIGUITY, MEASURED**: the gap between every adjacent pair of bins is **0.0px** (worst
  **−0.1px**, which is the one-decimal rounding of `n1()` making neighbours overlap by a tenth,
  never separate), and the bins **tile the plot exactly** — 1074.1px of bins across a 1074.0px
  plot at 1132 wide, and 654.0 of 654.0 at 712 wide.
- **dv-004's mechanism is present and correct**: `stroke-width 2px`, stroke colour
  `rgb(255,255,255)` in mono/light and `rgb(26,26,26)` in dark, `rgb(247,246,244)` in
  supercharge/light — the page colour per theme, which is what #96-D3 asked for.
- **Tooltip**: hovering bin 3 opens `#dvTip.on` reading **`£100–150: 45 transactions`**.
- **Filter re-renders**: **8 → 6 bins** and **8 → 6 table rows**, aria-label follows.
- **LABEL THINNING fires**: the 20-bin canvas labels **11 of 20** at a 1074px plot; the 8-bin
  canvas labels all 8. **0 dead fills**; one series, one fill, `rgb(118,102,130)`.
- **Resize** 1180 → 760: viewBox **1132 → 712**, text stays 12px, bins re-derive from
  `data-fx`/`data-fw` and stay contiguous at the new width.

### The SNIPPETS themselves, driven (scratch tree with the registry merged and partials injected)

- `Chart-histogram.reference.html`: **0 errors, 8 bins, 8 table rows rewritten from the spec, bins
  contiguous (−0.1…0.0px), one live fill.**
- `Chart-scatter.reference.html`: **0 errors, 12 + 21 marks, 12 + 7 table rows, three live fills**,
  and **DV-D11 works on engine-drawn marks** — unchecking the first legend swatch sets
  `aria-checked="false"` and dims **14 elements** (7 glyphs + their 7 marker groups). That is the
  #259 donut lesson enacted: the snippet injects `dv-render` + the type partial ABOVE the
  `dvRender()` bootstrap and `dv-legend` BELOW it, because `dv-legend.rec()` caches every mark once
  at parse time and would otherwise cache an empty canvas.

## Mutation — the clause bitten, not asserted

Every mutant is a copy of the committed page rewritten into `/tmp` with absolute `src` paths (the
repo is never written), driven, then discarded.

| mutant | result |
|---|---|
| **control** `scatter.html` | **GREEN** — 0 errors, 12 markers, gaps 43.0–128.9px |
| scatter: one category is `'about 28'` (not a number) | **RED** — the axis collapses to band centres, gaps **89.4–89.6px**, i.e. even. The numeric assertion discriminates. |
| scatter: a series one value short of `categories` | **RED** — `dv-render: spec.series[0].values[11] is not a finite number`, 0 marks |
| scatter: `dv-fit` stripped from canvas 1 | **RED on resize** — viewBox stays `1132` while the control tracks to `712`. ⚠ It is **green on load**, because the ENGINE pins the viewBox itself at render; #72's original "pinned at 580" signature no longer discriminates until the plot is resized. Named below. |
| scatter: `data-x0` forced to 0 | **RED** — every point is displaced by the fit, gaps double to 86–257.8px |
| **control** `histogram.html` | **GREEN** — 0 errors, 8 + 20 bins, gaps 0.0px |
| histogram: a second series | **RED** — `dv-render-histogram: a histogram is ONE distribution, got 2 series — use type "grouped-column" or "stacked-column" for more` |
| histogram: a negative frequency | **RED** — `dv-render-histogram: bin "£100–150" has frequency -45 — a count cannot be negative (dv-bar-009, the axis starts at zero)` |
| histogram: `type: 'histogramme'` | **RED** — `dv-render: no type partial registered for "histogramme" — have: histogram` |
| histogram: a 2.2px gap cut out of `data-fw` | **RED** — bins separate by **2.1–2.2px** against the control's 0.0. Contiguity is a real assertion, not a description. |

## Gates — verbatim, run on the REAL tree unless marked

```
_validate_dataviz     ✅ DataViz gate passed (15 chart surface file(s))                   EXIT 0
                      [PASS] Chart-scatter.reference.html    (2 charts, 0 blocking, 0 advisory)
                      [PASS] Chart-histogram.reference.html  (1 charts, 0 blocking, 0 advisory)
_validate_snippets    ❌ Chart-scatter.reference.html: required ARIA missing: role="img"   MINE — below
_validate_a11y        136 snippet(s), 0 failure(s) · no scatter/histogram finding          GREEN
_validate_no_hardcode ✅ No-hardcode gate passed (11 tranche file(s))                       GREEN
_gate_dataviz_vars    ✅ every colour presentation attribute resolves in at least one theme GREEN
_validate_compose     RESULT: PASS ✅                                                       GREEN
gen_canon_components  --check OK — 136 components in sync                                   GREEN
_validate_behaviour   [PASS] page budget — Chart-scatter 24930 · Chart-histogram 15266   SCRATCH TREE
gen_component_partials both marker pairs FILL, snippet gate then 0 failures                SCRATCH TREE
```

**The one red is the un-merged registry and it clears on integration.** `_validate_snippets` reads
`requiredAria` off each snippet's own manifest by substring; `Chart-scatter`'s list includes
`role="img"`, which the baked points used to carry in the markup and the engine now emits at
runtime. **Proven, not assumed:** a scratch copy of `knowledge/` with the two registry fragments
merged and `gen_component_partials.py` run reports **`snippet gate: 136 snippet(s), 0 failure(s)`**
— the injected `dv-render-scatter` source contains the literal `role="img"`, so the requirement is
met once the blocks are filled. The two `_validate_behaviour`/`gen_component_partials` rows above
come from that same scratch tree, because the real one cannot be green until a lane that is allowed
to edit `component-types.json` merges the fragments.

⚠ **`_validate_screen.py` and `_build_all.py` NOT run** (carry ⑤ / fenced). `gen_showroom.py` NOT
run — it has no per-page flag and regenerating it would put other lanes' pages in this diff.

## Integration lane — the three things this lane could not do itself

1. **Merge `knowledge/_tmp/260/{scatter,histogram}.registry.json`** into
   `component-type.dataviz` (`$behaviour` entry + the member's `consumes`).
2. **Run `python3 knowledge/gen_component_partials.py`** — it fills the four empty AUTO-BEHAVIOUR
   marker pairs the two snippets now carry. Until then both snippets are engine-less and
   `_validate_snippets` is red on the one line above.
3. **Re-drive `python3 knowledge/_drive_chart_engine.py`** so `_receipts.json` covers the two new
   pages. Both pages drive clean under the committed driver **today** — 8/8 combos, 0 errors, the
   filter moving marks AND rows in every combo — the numbers were simply written to `/tmp`.

## Core requests filed — verbatim in `knowledge/_tmp/260/`

`scatter.core-requests.md`: (1) **the spec has no numeric x** — let `categories` be numbers, or add
`x: […]`, and let the core own the second axis under a third `fn.axis` value; (2) **a multi-series
scatter must share its x values** — allow `null` in `values`, or a per-series `x`, because the
specimen this replaces plotted three segments at three different sets of incomes; (3)
`_validate_dataviz.ENGINE_TEST_PAGE` needs the two new snippet→page mappings (a gate is not a type
lane's file); (4) **a re-render never re-runs a type partial**, so any decision made from the plot
width is frozen at first-render width.

`histogram.core-requests.md`: (1) **the spec has no `valueLabel`** — the frequency axis has no name
and the series name is doing two jobs; (2) **the core draws furniture this type did not have** —
`fn.furniture = false | 'axis'`, the dial the donut lane asked for the OFF end of; (3) the
re-render request above, restated with its measurement.

## What I could NOT do — first obstacle, named

1. **The scatter's three segments no longer plot at their own x values.** The ruled spec makes
   every series share `categories`, so the snippet's segment figure was re-authored onto seven
   SHARED income bands. The chart is correct and honest; it is a **different sampling** from the
   bake, and it is core request 2.
2. **Neither snippet keeps a baked specimen, so both are 100% engine-drawn.** Lanes A and D each
   kept one baked canvas to hold a static rule up. Neither of my types owes a statically-measured
   rule (dv-004 is scoped to donut/pie/stacked; the histogram's separation is a canon.css stroke),
   so nothing was preserved for a gate's benefit — but it does mean `dv-016`'s rendered-contrast
   read now sees **no series fills at all** in these two snippets, and passes by having nothing to
   grade. That is a silence, not a pass.
3. **The histogram gained gridlines and value tick labels nobody asked for** — the core's
   `furniture()` is unconditional. Core request 2 above; not fixed locally, because the fix is a
   core flag and a type lane must not write one.
4. **Label thinning does not survive a resize.** Measured: 11 of 20 labels at a 1074px plot stay 11
   at 654px. The core dispatches a re-FIT, never a re-RENDER.
5. **`gen_showroom.py` has no per-page flag**, so the two showroom pages are left as they are
   rather than regenerating unrelated pages into this lane's diff.

## RULING-SHAPED — Dave's word, not a lane's

1. **`role="img"` now passes a gate for the wrong reason.** `_validate_snippets` requires the
   literal `role="img"` in the snippet, and after injection it finds it — **inside the engine's
   JavaScript source**, not in any markup a browser will render before JS runs. The gate is a
   substring search and cannot tell the difference. This is
   [[no-gate-parses-the-artefact]] arriving in a THIRD gate (after dv-004's static geometry at
   #259 and dv-016's contrast reads), and this time it fails OPEN rather than closed, which is the
   worse direction. `s260-D3` gave dv-004 a driven-receipt route; the same question is now owed for
   `requiredAria`. **Not decided here, and nothing was weakened to make it pass.**
2. **The #72 dv-fit mutation signature has been silently retired by the engine.** The scatter's
   fit was discharged at #72 with a mutation that read "strip `dv-fit` ⇒ viewBox stays PINNED at
   580". Measured today: with the engine drawing, stripping `dv-fit` leaves the chart **correct on
   load** (the engine pins the viewBox to the rendered width itself) and only wrong **after a
   resize**. Any future test that repeats #72's assertion at load time will pass a broken chart.
   Either the engine should stop setting the viewBox when the canvas carries no `dv-fit`, or the
   discharge's mutation needs restating in terms of a resize. This lane's driven check does the
   resize; nothing else in the repo does.
3. **The spec still has no numeric x, and this is the second type to strain it.** Lane A's
   ruling-shaped item 2 was "no per-CATEGORY role"; this is "no per-point x". Both are the same
   shape: `{categories, series[].values}` is a BAND grammar, and two of the fourteen chart types in
   the library are not band charts. Whether the spec grows a second numeric axis or the library
   accepts that scatter-like types own their own x read is Dave's, not a lane's. The workaround
   here is ~40 lines and it is driven and green — but it is 40 lines that would be deleted the day
   the core grows the field.
4. **A histogram cannot honour s116-D1.** A bin's width IS its band; there is no gutter to spend
   and no way to lift a mark to a 24px hit target without breaking contiguity. Twenty bins in a
   654px plot gives **32.7px** bins, which is fine; forty would give 16.4px and the type would be
   shipping sub-target hit areas with no lever to pull. Either a histogram is exempt from the 24px
   floor (the mark is data geometry, and the a11y gate already exempts data marks from the 44px
   rule for the same reason), or the type needs a maximum bin count. Today it is neither.
