# #260 — CORE REQUESTS, collated and de-duplicated

**⛔ NOTHING HERE IS ENACTED.** This file is the integration lane (I) reading the seven
`*.core-requests.md` files beside it and saying, once, what the four fast-follower lanes
(F1 scatter+histogram · F2 pie+boxplot · F3 bullet+candlestick · F4 butterfly-h/-v) asked the
core for. No line of `knowledge/canon/dv-render.js` — or of `dv-render-donut.js` — was changed
at #260 I. Each request keeps its **reporter count**, because a request three lanes filed
independently is a seam and a request one lane filed is a preference.

The verbatim wording, the measurements and the local workarounds stay in the per-type files
in this directory; this is the index, not a replacement.

---

## A · `dv-render.js` — the engine core

### A1 · Let a type opt out of (or dial down) the cartesian furniture — **5 reporters**
`fn.furniture = false` / `fn.axis = "none"`, with F1 asking for a third position, `'axis'`
(baseline + tick labels, no gridlines).

| reporter | why, in its own terms |
|---|---|
| **#259 donut** (original) | a radial chart pays for gridlines it discards |
| **#259 sparkline** | same discard |
| **F3 bullet** | a **cartesian** type that still wants none: opaque grey bands paint over every gridline, and the promoted component never carried a tick label |
| **F4 butterfly** | the furniture would be **wrong**, not merely unwanted — on a symmetric domain a tick reads `-40` under a wing whose value is 40 |
| **F1 histogram** | the engine-drawn version gained four gridlines and four tick labels **nobody chose**; wants the dial, not the switch |

`ctx.out.length = 0` at the top of a partial is now the shared workaround in donut, sparkline,
bullet and butterfly — four copies of a three-character hack in one group.
**F2 pie re-affirms it without re-filing** (it inherits the donut's cost verbatim).

### A2 · Scope the ZERO CLAMP to the types that own it — **3 reporters (+2 prior)**
`if (lo > 0) { lo = 0; }` runs on the line **after** `fn.domain`, so no type can escape it.
Requested shape, agreed across reporters: `fn.zeroBaseline !== false` (default true, every
bar-family type unchanged), or apply the clamp only in the `else` branch where the engine is
guessing rather than being told.

| reporter | the cost, measured |
|---|---|
| **F3 candlestick** — *"had no third option"* | series 90.41–108.52 against a zero floor occupies the **top 17%** of the plot; every body collapses to a hairline |
| **F2 boxplot** | a distribution (BP 95–180, latency 240–2,100 ms) spends a third to nine tenths of its height on empty space. **Cost recorded, not paid** — the type accepts the clamp |
| **F1 scatter** (implied by A3) | a scatter must scale to its own extent |
| prior: `dv-render-line` (#259) | reported it, left it |
| prior: `dv-render-sparkline` (#259) | filed it, scaled to its own extent |

Every reporter notes the same argument: **dv-bar-009 is a BAR rule** — a bar's length IS its
value; a price is a POSITION on a scale — and `_validate_dataviz.py` already scopes its own
check to `BAR_FAMILY`. Only the engine does not.

### A3 · Let a series value be `null` and mean ABSENT (ragged data) — **3 reporters**
- **F2 boxplot** — the only one where it **blocked a deliverable**: an outlier list is ragged,
  `writeTable` prints a placeholder under a column headed *Outlier*, so
  `Chart-boxplot.reference.html`'s exemplar DATA MOVED (Teams B and D gained real low outliers
  8 and 3, replacing two `—` cells) rather than let the table misstate the data.
- **F1 scatter** — a multi-series scatter must share its x values; the bake plotted three
  segments at three different sets of incomes, which the ruled spec cannot express. Asks for
  `null` in `values` **or** a per-series `x`.
- **F1 histogram / F2 boxplot both note** the general shape: a missing month in a line, a
  category with no reading. ~60 code bytes across `validate`, `writeTable`, `autoLabel`.

⚠ **Spec-shaped as well as core-shaped** — it changes the contract Dave ruled at `s249-D4`.

### A4 · The spec has no NUMERIC X — **1 reporter (F1 scatter), and it is the big one**
Every registered type reads `categories` as a BAND. Requested: `categories` may be numbers, or
the spec grows `x: […]`; the core then owns the x scale (`ctx.xf(n)` beside `ctx.vf(n)`) and
emits axis-2 furniture under a third `fn.axis` value (`'xy'`).
Workaround: ~40 lines inside `dv-render-scatter.js` that would be deleted the day this lands.
**Driven proof it is real**: 7.143–7.167 px per £1k, gaps 43.0–128.9px, against 72.9px even.

### A5 · `valueLabel` beside `categoryLabel` — **1 reporter (F1 histogram)**
The value axis has no name; the series name is doing two jobs ("60 transactions").

### A6 · A type cannot contribute to its own accessible name — **1 reporter (F3 candlestick)**
`autoLabel` enumerates every series × category — **48 phrases for 40 sessions**. Requested:
`fn.label = fn(spec)` alongside `fn.axis`/`fn.domain`, or `ctx.setLabel(s)`.
Workaround **named as unclean**: the partial writes `ctx.spec.label` behind a `__dvLabel` flag,
mutating the caller's spec — *"which nothing forbids and nothing sanctions"*.

### A7 · A re-render never re-runs a type partial — **2 reporters (F1 scatter + F1 histogram)**
`dvRender` dispatches one `resize`, which re-FITS; it never re-RENDERS. Any decision taken from
plot width is frozen at first-render width. Measured: 11 of 20 bin labels at a 1074px plot stay
11 at 654px. Requested: re-call `draw(ctx)` past some width delta, or expose
`dvRender.redraw(figure)`.

### A8 · Furniture BEHIND a partial's own marks — **1 reporter (F3 bullet), not needed today**
One output buffer, pushed in order; a partial that opts out of the core's furniture can only
paint its own furniture ON TOP. Harmless now (a 1px baseline at the left edge). Recorded so the
next lane does not rediscover it.

### A9 · `fitOne` moves rect/text/line/g and **not** `circle`; `fitY` moves `circle` and not `g` — **2 reporters (F1 scatter, F2 boxplot), documentation only**
Two passes, one element, opposite answers. Every point-mark type must wrap glyphs in
`g[data-fx][data-x0]`; today the only way to learn that is to drive a chart and watch the dots
stay put. **One sentence in the core's grammar comment fixes it**; whether the passes should be
made symmetric is bigger.

---

## B · `dv-render-donut.js` — the one request against a type partial

### B1 · Emit radial path coordinates at TWO decimals — **1 reporter (F2 pie), with a driven receipt**
F2 built the fix in a **scratch** copy (local `n2`, 9 call sites), drove the committed
`donut.html` control-and-patched, 4 themes × 2 modes each:

| figure | control (`n1`) | patched (`n2`) | authored |
|---|---|---|---|
| `fig-donut` (ring, inner edge ri = 60) | **2.109px** | **2.194px** | 2.2 |
| `fig-pie` (wedge, at 0.35·ro = 35) | **2.108px** | **2.134px** | 2.2 |

⚠ **The donut's defect IS the rounding; the pie's is NOT** — a pie has no inner edge, so both
the partial and the driver judge it at a **convention**, `0.35 · ro`. See the ruling-shaped list
in the I subreport.
⚠ F2 also says explicitly: **do not** also lower `GAP` from 2.2 — the 0.2 is the *cartesian*
rounding budget and the two mechanisms are independent.

**#260 I re-drove the committed engine at 19:35:36Z and the control numbers reproduce exactly:
`fig-donut` 2.109px and `fig-pie` 2.108px, identical in all 8 combos.** The request is
unenacted and the receipt for it is now in the tree.

---

## C · Filed against a GATE, and DONE by this lane

### C1 · `_validate_dataviz.ENGINE_TEST_PAGE` needs the new snippet→page mappings
Filed by **F1 (scatter, histogram)**; **F3 explicitly said none was owed** for bullet/candlestick
because dv-004's engine branch fires only for donut/pie/stacked; **F4 said the same** for
butterfly. **#260 I mapped all seven anyway** — the map is the reviewer-readable statement of
which snippet is exercised by which page, and a member that is engine-drawn and unmapped is a
member whose receipt nobody can find. Done, with a selftest bite that goes red if a mapping is
dropped or names a page that is not on disk.

---

## D · Explicitly NOT re-filed by a lane (recorded so they are not lost)

- `dv-legend`'s stale value cache after a re-render (#259 lane D request 2) — **still open**.
- `dv-donut-sweep`'s missing re-entry point (#259 lane D request 3) — **still open**.
  F4 declined to re-file either: *"the butterfly emits no `data-tip-value` and no sweep, so this
  lane has no independent evidence to add and re-filing a request twice would only make it look
  like two."*
