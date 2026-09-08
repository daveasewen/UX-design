# #260 lane F3 — BULLET + CANDLESTICK type partials · subreport

**s259-D1's fast follower, two of eight.** `knowledge/canon/dv-render-bullet.js` and
`knowledge/canon/dv-render-candlestick.js` register `bullet` and `candlestick` on the dv-render
type registry; both promoted components now ship an **EMPTY** canvas drawn by
`dvRender(figure, spec)`. **8 of 8 theme × mode combinations green on both driven test pages, zero
page errors anywhere, six mutants red with named errors, two controls green** — and both SNIPPETS
were driven end-to-end as well, not just the test pages.

**No red is owed to Dave from this lane.** Both page budgets are half empty (s260-D1's shared-core
pricing is why), dv-004 does not bind either type, and every gate that can see these two files is
green. Three items are RULING-SHAPED and one core defect now has its **third** reporter.

## Files touched

| path | note |
|---|---|
| `knowledge/canon/dv-render-bullet.js` | **NEW** — the bullet type partial |
| `knowledge/canon/dv-render-candlestick.js` | **NEW** — the candlestick type partial |
| `knowledge/_tests/chart-engine/bullet.html` | **NEW** — committed driven test page |
| `knowledge/_tests/chart-engine/candlestick.html` | **NEW** — committed driven test page |
| `knowledge/snippets/Chart-bullet.reference.html` | canvas emptied + DATA + 2 marker pairs + behaviour-manifest |
| `knowledge/snippets/Chart-candlestick.reference.html` | canvas emptied + DATA + 2 marker pairs + behaviour-manifest |
| `knowledge/components/Chart-bullet.meta.json` | typed `behaviour` block added |
| `knowledge/components/Chart-candlestick.meta.json` | typed `behaviour` block added |
| `knowledge/_tmp/260/bullet.registry.json` · `candlestick.registry.json` | registry fragments (lane may not edit the registry) |
| `knowledge/_tmp/260/bullet.core-requests.md` · `candlestick.core-requests.md` | core requests, verbatim |

**Nothing else.** `component-types.json`, `dv-render.js`, `_receipts.json`, every gate, canon.css
and the other six types' files are untouched. `_drive_chart_engine.py` was IMPORTED by a scratch
driver (`drive()` called directly, output to `/tmp/f3/receipts-scratch.json`) so the committed
receipts file was never written — the integration lane re-drives.

## Bytes — measured with `_validate_behaviour.code_only`

| source | raw | code-only | of the 16,384 per-source cap |
|---|---|---|---|
| `dv-render-bullet.js` | 10,582 | **4,443** | 27% |
| `dv-render-candlestick.js` | 10,765 | **4,872** | 30% |

**Page budget (`PAGE_BYTES` 34,816), computed the way `_validate_behaviour.check_group` computes
it** — `dv-render` carries `"shared": true` (s260-D1, ADR-0015 A4) and is priced once per PAGE, so
it is NOT in either member's sum; neither member consumes `dv-legend`:

| member | consumes | page figure | of cap |
|---|---|---|---|
| `Chart-bullet` | dv-behaviour + dv-render(shared) + dv-render-bullet | 13,048 + 4,443 = **17,491** | **50.2%** |
| `Chart-candlestick` | dv-behaviour + dv-render(shared) + dv-render-candlestick | 13,048 + 4,872 = **17,920** | **51.5%** |

Lane A's #259 ruling-shaped item 1 and lane D's 2,971-byte overrun are both **discharged for these
two types by s260-D1** — the member that nearly killed the bar and did kill the donut is a
half-full page once the engine core is priced once. Recorded because the discharge is the ruling
working, not a coincidence.

## THE SPEC — what each type does with the ruled shape

**Candlestick takes the s249-D4 spec UNEXTENDED.** OHLC is four numbers per period and `series` is
already "n named arrays, one value per category", so the four price points ARE four series, named
and ordered: `open, high, low, close`. That is not a convenience — it is why the accessibility
answer survives the move intact. The **core's own `writeTable`** emits
`Session | Open | High | Low | Close`, column for column the table the promoted snippet baked by
hand, and ds-027 (Dave, #100) makes that table THE accessibility fallback, not a decoration.
Driven: 40 rows, 5 columns, `S1 | 101.25 | 102.06 | 99.75 | 100.59`.

**Bullet needs ONE extension and it is declared, not smuggled.** `spec.ranges` — the qualitative
breakpoints. A bullet without its bands is a horizontal bar; the bands are the whole reason the
component beats stat-card and kpi-tile in its own `when` clause ("when the BENCHMARK … is the
point"). The core's `validate()` neither knows nor rejects extra keys, so the partial validates
`ranges` **itself**, loudly and by name, exactly as the core validates what it owns. RULING-SHAPED,
below.

## Rulings enacted, and how each was PROVEN

- **#96-D1 ② — row pitch 60px, `H = 80 + (rowCount−1)·60`.** Enacted, not re-typed: `PITCH = 60` is
  a constant in the partial, and the canvas authors `data-pt="4" data-pb="16"` so that
  `plotH = H − 20 = 60 × rowCount` **exactly** and the band arithmetic needs no special case. The
  pitch is **capped, never stretched** (`Math.min`), which is the ruling's own sentence ("a single
  row keeps the SAME 60px band/appearance"). **Driven: pitch measured 60.000px in all 8
  combinations, band rect 32px, measure bar 16px, target tick 48px — the baked numbers to the
  pixel. After filtering a KPI out: 2 rows, pitch STILL 60.000px, band still 32px.**
- **#96-D1 ③ — canon greys, minted nothing.** `--dv-range-1/2/3`. A **fourth** breakpoint throws by
  name, because a fourth token does not exist. Driven: the three bands resolve to
  `rgb(237,237,237)` / `rgb(215,216,214)` / `rgb(183,183,183)` = `--color-grey-200/300/400`.
- **#96-D1 ③ z-order (bands → bar → marker).** In SVG that is DOM order and nothing else, so the
  push order IS the z-order. Driven — the first row's children, in order:
  `dv-label`, `dv-range-1`, `dv-range-2`, `dv-range-3`, `dv-series dv-measure`, `dv-target`.
- **brief-ruled: measure = data/series/1, marker = ink.** The measure rect carries
  `fill="var(--data-series-1)"` as a presentation attribute **so the dataviz gate can read it** —
  it reads `fill` off `.dv-series` — while canon.css's `.dv-measure{fill:…}` wins at paint time and
  binds the SAME token, so the two cannot disagree. Driven: one computed fill, `rgb(118,102,130)`,
  in all four themes.
- **ds-027 (#100) — SOLID two-state, colour = close vs open ONLY.** Driven: 40 bodies, **24 up / 16
  down**, every one a real fill (`solid: true`, 0 dead `var()`s), two distinct colours per mode —
  light `rgb(22,134,78)` / `rgb(185,47,30)`, dark `rgb(26,160,92)` / `rgb(204,67,51)` =
  `--data-delta-gain` / `--data-delta-loss`. The #96-D1 ① hollow-up channel stays retired and this
  partial cannot bring it back: there is no stroke-only branch in it.
- **DV-D02 / DV-D02-A — compress, never scale.** Both types are cartesian, so both canvases keep
  `dv-fit`. Driven at 1180 → 760: **bullet** viewBox `1132 → 712`, bar width `820 → 475.6`, row
  height **16px unchanged**, label type **12px unchanged**. **Candlestick** viewBox `1132 → 712`,
  candle 40's group re-translates `translate(-0.0,0) → translate(-414.8,0)`, body width **16.600px
  unchanged**, wick **1px unchanged**, axis type **12px unchanged**.
- **rule 14 — the filter re-renders and the a11y answer follows.** Bullet 3 → 2 marks, table 3 → 2
  rows, and the svg `aria-label` drops "Satisfaction". Candlestick 40 → 30 marks, table 40 → 30
  rows. All 8 combinations, both pages.
- **DEF-003 — CSS-only motion.** Every number either partial writes is an SVG attribute derived
  from the data; entry is `.dv-animate .dv-row` / `.dv-animate g.dv-candle` on an authored
  `animation-delay`. No JS geometry animation, no scale physics.
- **dv-017 / DEF-004.** Every colour emitted is a `var()` token. `_gate_dataviz_vars`: 360
  references, 4 themes, all resolve.

## Gates — verbatim tails

```
_validate_dataviz     [PASS] snippets/Chart-bullet.reference.html       (1 charts, 0 blocking, 0 advisory)   GREEN
                      [PASS] snippets/Chart-candlestick.reference.html  (1 charts, 0 blocking, 0 advisory)   GREEN
                      ✅ DataViz gate passed (15 chart surface file(s)).                                     EXIT 0
_validate_behaviour   Behaviour-contract gate OK — see knowledge/_BEHAVIOUR-GATE.md                          EXIT 0
_validate_snippets    snippet gate: 136 snippet(s), 2 failure(s) — Chart-boxplot, Chart-scatter   NOT MINE (other lanes)
_gate_dataviz_vars    ✅ every colour presentation attribute resolves in at least one theme                  EXIT 0
_validate_no_hardcode ✅ No-hardcode gate passed (11 tranche file(s)).                                       EXIT 0
_validate_a11y        136 snippet(s), 0 failure(s), 181 warning(s) · 68 marks measured                       EXIT 0
_validate_compose     RESULT: PASS ✅                                                                        EXIT 0
gen_showroom --check  OUT OF SYNC — stale: chart-boxplot/-bullet/-butterfly-h/-butterfly-v/-candlestick/
                      -histogram · orphaned: [] · index: ok                                   NOT REGENERATED
gen_component_partials --check
                      X dataviz/dv-render: Chart-bullet does not consume this behaviour but carries its
                        AUTO-BEHAVIOUR markers …                                   EXPECTED — registry fragment
```

**`gen_component_partials --check` is EXPECTED-RED and the redness was falsified, not asserted.**
The registry cannot know `dv-render-bullet` / `dv-render-candlestick` until the integration lane
applies the fragments, so every member of this wave (all four lanes) reports "does not consume this
behaviour but carries its AUTO-BEHAVIOUR markers". Re-run with `load_registry` monkey-patched to
apply **this lane's two fragments verbatim**: **zero failures and zero out-of-sync for Chart-bullet
and Chart-candlestick.** Out-of-sync being empty is the load-bearing half — it means the
hand-injected `dv-render` + type-partial blocks AND the derived `#behaviour-manifest` blocks are
**byte-exact** with what the generator will produce, so the integration lane's `--write` is a no-op
on these four files.

`gen_canon_components.py` **does not exist in this tree** (it is named in #259's lane-A report; the
file is not there now) — not run, named rather than skipped silently. `gen_showroom.py` still has
no per-page flag, and the six stale pages are one per new engine type across all four lanes, so
regenerating is the integration lane's call, not a type lane's. `_validate_screen.py` not run
(carry ⑤).

## Driven — Chromium 151.0.7922.34, `goto("file://…")`, never `set_content`

Playwright was already installed; `LD_LIBRARY_PATH` into `/tmp/pwlibs/root` (the #259 lane-A/D
`dpkg-deb -x` workaround) was still in place. Viewport 1180×900, `reduced_motion: reduce`,
`device_scale_factor: 1`, per (mono · legacy · console · supercharge) × (light · dark).

**`bullet.html` — 8/8 identical, 8/8 green.** 0 pageerrors, 0 console errors. 3 rows / 3 measure
bars / **9 range rects** / 3 target ticks; every measure carries `data-fx` AND `data-fw`. Zero
baseline at x = 120 = the authored gutter. Tooltip on hover of row 2 opens `#dvTip.on` reading
**`Satisfaction: 58 of 100, target 70`** — the same numbers that row's table cells carry, because
both come off one spec. 0 dead fills.

**`candlestick.html` — 8/8 identical, 8/8 green.** 0 pageerrors, 0 console errors. **40 candle
groups, 40 wicks, 40 bodies**, every group carrying `data-fx` AND `data-x0` (the translate grammar,
so nothing inside a candle is ever re-scaled). Tooltip on hover of candle 3: **`S3: open 97.52,
high 99.4, low 97.3, close 98.42`**. **The value axis is NOT zero-floored: ticks read 90 / 95 / 100
/ 105 / 110** — the same five gridlines the promoted bake carried, arrived at independently by
`nice(90.41, 108.52, 4)`.

**The SNIPPETS themselves, driven the same way (light + dark).** `Chart-bullet.reference.html`:
0 errors, 3 marks, table 3 rows, tooltip `Revenue: 82 of 100, target 75`, viewBox `0 0 1208 200`.
`Chart-candlestick.reference.html`: 0 errors, 40 marks, table 40 rows × 5 columns, tooltip
`S1: open 101.25, high 102.06, low 99.75, close 100.59`, gain/loss both resolving per mode. **The
injected copies work, not just the `<script src>` test pages.**

## Geometry agreement with the promoted bake — measured, not eyeballed

The candlestick partial reproduces the baked snippet's numbers because it derives them the same
way, not because they were copied. At the authored 580×260 frame: Y(90) = 230.0, Y(95) = 176.0,
Y(100) = 122.0, Y(105) = 68.0, Y(110) = 14.0 — the bake's five gridlines exactly. Session 1: wick
99.75 → 124.7 (bake 99.8 → 124.7), body top 108.5, height 7.1, x 48.5, width 8.1 — **the bake's
values to one decimal.** Same for the bullet: band 32, bar 16, tick 48, pitch 60.

## Mutation — the clause bitten, not asserted

Six mutants of the two committed test pages, driven, then deleted (`__mutant.html` removed):

| mutant | result |
|---|---|
| bullet: FOUR range breakpoints | **RED** — `spec.ranges has 4 breakpoints — #96-D1 ③ mints THREE qualitative tints (--dv-range-1/2/3) and a fourth band would bind a token that does not exist`, 0 marks |
| bullet: ranges not ascending (`[60,40,100]`) | **RED** — `spec.ranges must ascend from zero — ranges[1] is 40 and the band before it ends at 60`, 0 marks |
| bullet: a THIRD series | **RED** — `a bullet row is ONE measure against AT MOST ONE target — got 3 series. Expected [measure] or [measure, target]; use type "bar" for a multi-series horizontal comparison`, 0 marks |
| candlestick: High/Low series SWAPPED | **RED** — `spec.series[1].name is "Low" — position 1 of a candlestick spec is "high" (open, high, low, close, in that order)`, 0 marks |
| candlestick: a HIGH below the close | **RED** — `"S1" has high 99 below open 101.25 / close 100.59 / low 99.75 — the HIGH is the session's highest price, always`, 0 marks |
| candlestick: THREE series | **RED** — `OHLC is FOUR series — open, high, low, close, in that order. Got 3: Open, High, Low`, 0 marks |
| **control** — unmutated `bullet.html` | **GREEN** — 0 errors, 3 marks |
| **control** — unmutated `candlestick.html` | **GREEN** — 0 errors, 40 marks |

The high/low swap is the one worth noting: **positional-only validation would have drawn a chart
that is wrong in a way nothing can see.** Naming the four series and checking the OHLC invariant is
the difference between a partial that renders and a partial that refuses.

## Core requests — verbatim, for the core owner (filed in full in `knowledge/_tmp/260/*.core-requests.md`)

1. **⛔ THE ZERO CLAMP RUNS AFTER `fn.domain`, SO NO TYPE CAN ESCAPE IT — THIRD REPORTER.**
   `if (lo > 0) { lo = 0; }` sits on the line after the `fn.domain` call. dv-render-line reported it
   and left it; dv-render-sparkline filed it and scaled to its own extent; **this lane had no third
   option — there is no honest candlestick with a zero baseline.** Measured: the promoted series
   90.41–108.52 against a zero floor occupies the **top 17%** of the plot and every body collapses
   to a hairline. Requested verbatim: *"Honour a type's own domain. Make the clamp a property of the
   TYPE, not of the engine — `fn.zeroBaseline !== false` (default true, so every bar-family type is
   unchanged) — or apply the clamp only in the `else` branch, where the engine is guessing rather
   than being told. dv-bar-009 is a BAR rule: a bar's length IS its value. A price is a POSITION on
   a scale."* Each work-around costs ~14 lines and each copy is a place three partials can drift.
2. **`dvRender` calls `furniture()` unconditionally — SECONDED, third consumer.** donut's core
   request 1, verbatim, now with a **cartesian** claimant: a bullet has `fn.axis = "x"` and still
   wants no gridlines (opaque grey bands paint over them and the promoted component never carried a
   tick label). `ctx.out.length = 0` is the third copy of the same three-character work-around in
   one group. **Three consumers is a pattern, not a coincidence.**
3. **The accessible name is the core's and a type cannot contribute to it.** `autoLabel` enumerates
   every series × category — **48 phrases** for 40 sessions. Requested verbatim: *"honour
   `fn.label = fn(spec)` alongside `fn.axis` and `fn.domain`, or expose `ctx.setLabel(s)`."*
   Worked around by writing `ctx.spec.label` behind a `__dvLabel` flag — it mutates the caller's
   spec, which nothing forbids and nothing sanctions. Result driven:
   *"Share price, open high low close, forty sessions, pounds. Ranges from a low of 90.41 to a high
   of 108.52, opening 101.25 and closing 106.16 across 40 sessions."*
4. **Minor, recorded so the next lane does not rediscover it:** a partial that opts out of the
   core's furniture has no way to emit furniture BEHIND its own marks (one output buffer, pushed in
   order). Harmless today — the bullet's baseline is 1px at the left edge and overlaps nothing.

## RULING-SHAPED — Dave's word, not a lane's

1. **`ranges` is an EXTENSION to the s249-D4 spec, and a bullet cannot exist without it.** The spec
   Dave ruled is `{type, categories, series, format, unit, caption, categoryLabel, label}`. A
   bullet's qualitative bands are per-CHART, not per-series and not per-category, so they fit none
   of those fields. The partial reads `spec.ranges` and validates it itself; the core neither knows
   nor rejects it. Two shapes, neither a lane's: **(a)** the ruled spec grows an optional `ranges`
   (≈0 core bytes — the core already ignores unknown keys, so this is a documentation change and a
   line in the core's header comment), or **(b)** the extension stays the type's private business
   and the header comment is where it is declared, which is what shipped. **This is the same shape
   as lane A's per-CATEGORY `role` question (#259, its item 2) and it should be answered once for
   both, not twice differently.**
2. **The engine's `<table>` spine narrows the bullet from six columns to three, and it does it
   silently between JS-off and JS-on.** MEASURED: the authored table carries
   `KPI | Measure | Target | Poor to | Satisfactory to | Good to`; after `dvRender` runs it carries
   `KPI | Measure | Target`. The three breakpoint columns are present with JS OFF and absent with JS
   ON. **This is dv-render-donut's item 4 (the dropped value ⇄ percent column) with a different
   noun** — `writeTable` emits `Category | <series name>…` and has no notion of a column that is
   not a series. Either the spec grows a way to say "these columns too", or engine-drawn figures
   accept a narrower table than the bake had, and it is written down. The authored six-column table
   was KEPT rather than trimmed to match, so nothing regresses with JS off.
3. **`_validate_snippets`'s `requiredAria` check is satisfied by a JS STRING LITERAL.** Both
   components declare `role="img"` in their token manifest's `requiredAria`. After the canvas was
   emptied there is no `role="img"` in either file's MARKUP — the gate passes because the *injected
   partial's source code* contains `' role="img" aria-label="'`. The claim is TRUE (driven: every
   measure bar and every candle body carries `role="img"` + `aria-label` at runtime) but the gate is
   green **for the wrong reason**, and would stay green if the attribute were deleted from the
   emitted markup and left in a comment. **[[no-gate-parses-the-artefact]], third venue** — after
   dv-004 on the donut and dv-004 on the stacked column. s260-D3 gave dv-004 a driven-receipt route;
   `requiredAria` has none, and now needs one or an explicit exemption for engine-drawn canvases.
4. **`data-domain-min="0"` was REMOVED from the candlestick figure**, because the domain is not
   zero-based and declaring it so was a claim the chart does not make. `dv-bar-009` only fires on
   `BAR_FAMILY` so nothing was gated on it. Named because deleting a declared attribute is the kind
   of edit that should be noticed, not discovered.

## What I could NOT do — first obstacle, named

1. **The registry is not mine.** `component-types.json` needs one `$behaviour` entry and one
   `consumes` line per type; both are in `knowledge/_tmp/260/*.registry.json`, and the monkey-patched
   run above proves they are the only two things standing between this lane and a green
   `gen_component_partials --check`.
2. **`_receipts.json` is not mine and `_drive_chart_engine.py` has no `--out`.** Driven through a
   scratch importer instead; the integration lane must re-drive `bullet.html` and `candlestick.html`
   for the committed receipt. **Neither type NEEDS one:** dv-004's engine-drawn branch fires only
   for `donut`/`pie`/`stacked`, and neither of these is one — so `ENGINE_TEST_PAGE` (a gate, and
   fenced) needs **no** new entry today. Noted in the candlestick fragment so a later change that
   brings a gapless surface to either type knows the mapping it then owes.
3. **`gen_showroom.py` has no per-page flag** and six pages are stale across four lanes.
4. **The candlestick's period labels are the bake's answer, not a better one.** Past twelve
   sessions only the first and last are drawn (forty tick labels collide into a grey smear). A real
   date axis with a thinning rule is a bigger job than a type partial and was not attempted.
5. **s116-D1's 24px floor is NOT met by a candle body** (~8px at 580, ~16.6px at 1132) and cannot
   be while ds-027's standing density rule asks for forty sessions. Receipted sub-24 **by design**,
   the same posture Chart-scatter's markers carry — named in the partial's header rather than
   quietly ignored.
