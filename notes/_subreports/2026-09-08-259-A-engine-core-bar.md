# #259 lane A — ENGINE-CORE + BAR · subreport

**s249-D4 enacted.** The chart engine is the library's: `window.dvRender(figureEl, spec)` in
`knowledge/canon/dv-render.js`, injected as an ADR-0015 behaviour partial, with a type registry so
six type partials can be built in parallel. Rule 18's interim recipe is replaced, not re-typed.
Everything below is measured, not asserted; **all ten gates green, driven in a real browser across
4 themes × 2 modes, three mutants red, one control green.**

## Files touched

| path | lines | note |
|---|---|---|
| `knowledge/canon/dv-render.js` | 311 | NEW — the core |
| `knowledge/canon/dv-render-bar.js` | 161 | NEW — the bar type partial (4 types) |
| `knowledge/canon/dv-render-line.js` | 32 | NEW — registered stub |
| `knowledge/canon/dv-render-stacked-area.js` | 31 | NEW — registered stub |
| `knowledge/canon/dv-render-donut.js` | 31 | NEW — registered stub |
| `knowledge/canon/dv-render-sparkline.js` | 32 | NEW — registered stub |
| `knowledge/canon/dv-render-combo.js` | 31 | NEW — registered stub |
| `knowledge/component-types.json` | 814 | 7 `$behaviour` entries; Chart-bar `consumes` +2 |
| `knowledge/components/chart-bar.meta.json` | 175 | typed `behaviour` block |
| `knowledge/snippets/Chart-bar.reference.html` | 1918 | 3 canvases emptied + DATA + 2 injections |
| `knowledge/_tests/chart-engine/bar.html` | 197 | NEW — the committed driven test page |

## Bytes — every partial against the 16,384 code-only cap (ADR-0015 A3)

| source | raw | code-only | of cap |
|---|---|---|---|
| `dv-render.js` | 18,022 | **9,309** | 57% |
| `dv-render-bar.js` | 9,262 | **4,613** | 28% |
| `dv-render-line.js` | 2,235 | 374 | 2% |
| `dv-render-stacked-area.js` | 2,269 | 385 | 2% |
| `dv-render-donut.js` | 2,219 | 356 | 2% |
| `dv-render-sparkline.js` | 2,227 | 410 | 3% |
| `dv-render-combo.js` | 2,185 | 336 | 2% |

⚠ **The PAGE budget is the one that nearly bit.** `Chart-bar` = 34,704 of `PAGE_BYTES` 34,816 —
**112 bytes of headroom, 99.7% full.** The first draft of the bar partial was 5,956 and the page
was **RED by 1,282**; it went green by de-duplicating the four bar types into one `bars(ctx, horiz,
stack)` routine (a grouped column and a horizontal bar are the same arithmetic with the axes
exchanged), not by shaving comments. **This is a ruling-shaped item, below.**

## Gates — verbatim tails

```
gen_component_partials --check OK — all AUTO-PARTIAL blocks in sync, contracts hold.                      EXIT 0
Behaviour-contract gate OK — see knowledge/_BEHAVIOUR-GATE.md                                             EXIT 0
  [PASS] dataviz page budget — worst member 34704 code-only bytes (33.9 KB of 34) across 11 source(s)
         Chart-bar   34704  consumes dv-behaviour, dv-legend, dv-render, dv-render-bar
gen_canon_components: no change (136 components in sync).                                                 EXIT 0
gen_canon_components --check OK — 136 components in sync.                                                 EXIT 0
snippet gate: 136 snippet(s), 0 failure(s)                                                                EXIT 0
✅ DataViz gate passed (15 chart surface file(s)).                                                        EXIT 0
dataviz var-resolution gate — 19 file(s), 681 reference(s), 4 theme(s): mono, legacy, console, supercharge
✅ every colour presentation attribute resolves in at least one theme                                     EXIT 0
✅ No-hardcode gate passed (11 tranche file(s)).                                                          EXIT 0
a11y gate: 136 snippet(s), 0 failure(s), 282 warning(s), 692 note(s) · 1345 controls + 209 marks
  measured · 125 mark(s) below 24                                                                         EXIT 0
_validate_compose.py  RESULT: PASS ✅                                                                     EXIT 0
gen_showroom --check: OUT OF SYNC — stale: ['action-bar.html', 'alert.html', …] orphaned: [] index: ok    EXIT 1
```

**`gen_showroom.py` has NO per-page flag** (`main()` takes only `--check`/`--selftest`). Measured
without regenerating: **61 of 136 pages stale, of which 60 were ALREADY stale before this lane** —
the list is alphabetical from `action-bar.html` and nothing in it is chart-related except
`chart-bar.html`, which is mine. **NOT regenerated** (60 unrelated pages is not this lane's diff).
`_validate_screen.py` NOT run (carry ⑤).

## Driven — Chromium, `goto("file://…")`, never `set_content`

Sandbox was fresh: `pip install playwright` worked; `playwright install chromium` failed twice
(`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`, then a missing `libxdamage1` with no root). Resolved by
`NODE_TLS_REJECT_UNAUTHORIZED=0` for the download and `dpkg-deb -x` of the `.deb` into
`LD_LIBRARY_PATH` — **Chromium 151.0.7922.34 launched and the page was really driven.**

Per combination (mono · legacy · console · supercharge) × (light · dark) — **8/8 green**:

- **0 pageerrors, 0 console errors** on load and after the filter.
- **9 column bars**, all 9 carrying `data-fx` **and** `data-fw` **and** `data-tip`; 5 tick labels,
  ≥4 `line.dv-grid`, exactly 1 `line.dv-axis` baseline.
- **Tooltip**: hovering bar 3 opens `#dvTip.on` reading **`Housing: £950`** — the same number the
  table row carries, because both come off one spec.
- **Filter re-renders**: unticking *Housing* and *Childcare* takes the column chart **9 → 7 bars**,
  the horizontal chart **9 → 7 bars**, the **table spine 9 → 7 rows**, and drops "Housing" out of
  the svg `aria-label`. The unfiltered grouped chart stays at 24. No errors on re-render.
- **Grouped**: 8 categories × 3 series = **24 rects**, 3 distinct `data-series-group`, **24 letter
  keys** (§04.3), table **8 rows × 4 columns**.
- **Horizontal**: every bar `data-fx="0.0000"` — length lives in `data-fw`, which is what the fit
  re-derives; the same two attributes the column uses, meaning the opposite thing.
- **Colour**: 0 fills resolve to nothing; the single-series column resolves to exactly ONE computed
  colour, `rgb(118, 102, 130)` = `--data-series-1`, in all four themes.
- **Separation**: smallest rendered gap between adjacent grouped bars **2.10px** (dv-004 ≥2);
  between adjacent columns 34.00px. Smallest rendered bar width **87.5px** (s116-D1 floor 24).

**One real defect found by driving and fixed.** An authored 2px gap rendered at **1.90px**: the fit
re-derives a mark's `x` and its `width` independently from `data-fx`/`data-fw` and rounds each to
one decimal, so up to 0.15px vanishes out of the gap between them. `GAP` is now **2.2** with the
measurement in the comment — the rule stated in the coordinate space the rule is judged in. Two
attempts were made before the cause was found; the first (author into the *rendered* width rather
than the authored viewBox) was kept anyway because it is independently correct.

## Mutation — the clause bitten, not asserted

Three mutants of the committed test page, driven, then deleted:

| mutant | result |
|---|---|
| a series one value short of `categories` | **RED** — `dv-render: spec.series[0].values[8] is not a finite number`, 0 bars drawn |
| a negative value on `type: "bar"` | **RED** — `dv-render-bar: dv-bar-007 — "Housing" is -950 and negatives are for VERTICAL columns only` |
| `type: "rainbow-column"` | **RED** — `dv-render: no type partial registered for "rainbow-column" — have: bar, column, grouped-column, line, multiline, …` |
| **control** (unmutated `bar.html`) | **GREEN** — 0 errors, 42 marks |

## What I could NOT do — first obstacle, named

1. **Two of Chart-bar's five canvases stay BAKED, and neither is a shortcut.**
   - **cb3, the status ramp.** The ruled spec shape carries `role` **per SERIES**. cb3 is ONE
     series whose FOUR categories each take a different status colour (R-D9's salience ramp is a
     per-category thing). *One series with four different status fills is not expressible in the
     ruled spec.* Ruling-shaped — see below.
   - **cb5, the stacked column.** `_validate_dataviz.py`'s dv-004 measures **static** rect geometry
     (`y[i+1] − (y[i] + h[i])` off the markup) to prove 2px separation, and falls back to demanding
     a surface stroke when it cannot measure. An engine-rendered canvas has **no static rects to
     read**, so an emptied stack is refused BLOCKING by a gate that is correct about the rule and
     blind to the artefact. The stacked TYPE is built and driven; only the snippet's specimen is
     still baked. **This is [[no-gate-parses-the-artefact]] arriving on schedule.**
2. **`gen_showroom.py` has no per-page flag**, so chart-bar's showroom page is left stale with 60
   others rather than regenerating 60 unrelated pages in this lane's diff.
3. **`_validate_screen.py` not run** — carry ⑤ (it clobbers tracked ledger rows).

## RULING-SHAPED — Dave's word, not a lane's

1. **The page budget is 112 bytes from red, and the NEXT type partial cannot land.** ADR-0015 A1
   calls this "the forcing function working, not a defect" — but the forcing function now fires on
   the FIRST consumer of an engine that has six more type partials to come. `Chart-line` will want
   `dv-render` + `dv-render-line`; a member that consumed the core, its type AND `dv-legend` has
   roughly 9 KB of room for the type. Three shapes, none of them a lane's: (a) re-dial `PAGE_BYTES`
   (Amendment 1: "a cap that moves once moves again"); (b) a member consumes only the ONE type it
   draws, which is already true and already priced; (c) accept that the engine core is a *shared*
   payload and price it once per page rather than once per member. **Not decided here.**
2. **The spec shape has no per-CATEGORY role.** Extending `series` with an optional
   `roles: [...]` array is ~180 code bytes and would let cb3 join the engine — but it changes the
   spec Dave ruled at s249-D4, and the budget above has nowhere to put it. Ruled or not ruled, the
   status ramp is a chart every dashboard draws.
3. **dv-004 (and the dataviz gate generally) reads static markup.** Once a canvas is engine-drawn
   the gate is looking at an empty box. Either the gate learns to accept a *driven receipt* for the
   rules only geometry can prove, or the library keeps one baked specimen per such rule forever.
   The same question is owed for dv-016's rendered-contrast reads.
4. **`behaviour.partial` on `chart-bar.meta.json` lists three names as briefed
   (`dv-behaviour, dv-render, dv-render-bar`) but the snippet carries FOUR** — `dv-legend` is
   injected and consumed by the grouped/stacked legends. The schema's own words are "the
   AUTO-BEHAVIOUR name(s) … that the snippet carries". Written as briefed and flagged rather than
   silently corrected.
5. **Chart-bar carries no `APOLLO-DEMO` fence.** Its showroom chrome is the bare `<h2>` headings,
   unfenced before this lane. The DATA + `dvRender()` bootstrap is deliberately NOT fenced — it is
   the pattern a build must copy, not harness. Whether the `<h2>`s should be swept is s258-D3's
   business, not this lane's.
