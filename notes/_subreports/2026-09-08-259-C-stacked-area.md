# #259 lane C — STACKED-AREA type partial · subreport

`dvRender.types["stacked-area"]` is built. The snippet's canvas ships EMPTY and is drawn by
`dvRender(figure, spec)`; nothing in `dv-render.js`, `dv-render-bar.js` or `component-types.json`
was touched. **All my gates green, driven in a real browser across 4 themes × 2 modes (8/8), three
mutants red, one control green.**

## Files touched

| path | lines | note |
|---|---|---|
| `knowledge/canon/dv-render-stacked-area.js` | 161 | stub → BUILT (1 type: `stacked-area`) |
| `knowledge/snippets/Chart-stacked-area.reference.html` | 971 → 1500 | canvas emptied · 2 AUTO-BEHAVIOUR pairs added + injected · DATA + engine call |
| `knowledge/components/chart-stacked-area.meta.json` | +11 | typed `behaviour` block |
| `knowledge/_tests/chart-engine/stacked-area.html` | 137 | NEW — committed driven test page |

## Bytes

| source | raw | code-only | of cap |
|---|---|---|---|
| `dv-render-stacked-area.js` | 10,285 | **4,248** | 26% of 16,384 |

**PAGE: `Chart-stacked-area` = 34,339 of 34,816 — GREEN, 477 bytes of headroom (98.6% full).**
Consumes `dv-behaviour (13,048) + dv-legend (7,734) + dv-render (9,309) + mine (4,248)`. The budget
left exactly **4,725 bytes** for a type partial and this one fits, but only just — see RULING-SHAPED.

## Rulings quoted

- **dv-2px-separation** (#96, Dave, standing dataviz canon): *"2px separation rule for adjacent
  blocks is STANDING dataviz canon (histogram bars, stacked bands, any adjacent filled blocks)."*
  Enacted with REAL GEOMETRY — `ctx.GAP` (2.2) cut off the TOP of every band that has a band above
  it, the same "cut the block BELOW the join" convention `dv-render-bar` uses, so the TOP band still
  reads the true total. Canon's `.dv-band{stroke:var(--page); stroke-width:2}` supplies the ruled
  surface stroke as well, so BOTH mechanisms are present. **Measured 2.20px, every band pair, every
  category, at 1280px AND at 760px.**
- **ds-026** (#99, Dave): *"Charts stick to SOLID canonical palette; opacity primitives … are for
  STATE CHANGES only … `--stack-fill-alpha` dial retired."* Colour is `ctx.fill(i)` only — a
  `var(--data-series-N)` or `var(--status-*)` token, no tint, no alpha, no dial.
- **ds-030** (#103, Dave): *"ALL charts are fully horizontally responsive … no fixed px width."*
  Every x is a fraction (`data-fxs` / `data-fx`); driven: markers move 123.3 → 97.3px on a
  1280 → 760 viewport change.
- **s248-D2** (#248, Dave): *"the chart fills its tile's width AND height, and the aspect ratio need
  not be constant … fit re-positions, never scales."* y is authored in the `data-h` space and cached
  by `fitY` as a plot fraction, so a taller tile re-scales the stack. ⚠ `canon.css` pins
  `:where(.cn-chart-stacked-area) .dv-svg{height:260px}` and `figure.dv-fit-on` releases only
  `width`, so the HEIGHT half of s248-D2 is inert for this scope — a CSS fact, not a partial fact.
- **DEF-003** (CSS-governed motion, `knowledge/_CSS-GOVERNED-GATE.md`): entry motion stays CSS —
  the canon `.dv-animate .dv-band{animation:…dvFade}` rules. This file writes no transform, no
  scale, no timing; every number it emits is an SVG geometry attribute derived from the data.

## dv-004 — how it actually grades my snippet (asked for explicitly; NOT exempted)

`_validate_dataviz.py` line 33 states the rule as *"dv-004 >=2px separation — gapless surfaces
(donut/stacked segments) carry a surface-coloured stroke >=2px"*, with a second, mechanism-neutral
branch added when Dave ruled the geometry route on 2026-07-27.

**It never fires on this snippet.** Two independent reasons, both measured in the source:

1. `if dtype in ("donut", "pie", "stacked")` — and `DTYPE_CANON` folds `stacked-column` and
   `stacked-bar` into `stacked` but has **no entry for `stacked-area`**, which is its own member of
   `KNOWN_DTYPES`. So `dtype == "stacked-area"` and the whole dv-004 block is skipped.
2. Even if it were reached, `_rect_stack_gap` reads `x` / `y` / `height` off `<rect>`s and returns
   `(None, "segments are not measurable rects")` for paths; the fallback then demands a
   surface-coloured stroke **in the markup**, and an engine-rendered canvas ships no marks at all.

So the bar lane's finding generalises and gets worse here: dv-004 is blind to engine-rendered
canvases **and** blind to this dtype even when it is baked. The rule is enacted and MEASURED (2.20px,
driven, below); the gate simply does not grade it. Gate verdict for the file is
`[PASS] snippets/Chart-stacked-area.reference.html (1 charts, 0 blocking, 0 advisory)` — a pass that
is silent on the rule, not a pass that checked it. `[[no-gate-parses-the-artefact]]`, again.

## Gates — verbatim tails (10 commanded)

```
gen_component_partials --check   OUT OF SYNC: Chart-combo (dv-render, dv-render-bar,
  dv-render-line, dv-render-combo), Chart-line (behaviour-manifest)          EXIT 1  ← NOT MINE
  (no Chart-stacked-area line in the failure list; my two pairs inject clean)
_validate_behaviour.py           X dataviz (page budget): worst member page Chart-combo loads
  43518 code-only bytes > 34816                                             EXIT 1  ← NOT MINE
  Chart-stacked-area — 34339 bytes · consumes dv-behaviour, dv-legend, dv-render,
  dv-render-stacked-area                                                    (GREEN, mine)
gen_canon_components.py          generated 136 components -> .cn-<scope>                   EXIT 0
gen_canon_components.py --check  OK — 136 components in sync.                              EXIT 0
_validate_snippets.py            snippet gate: 136 snippet(s), 0 failure(s)                EXIT 0
_validate_dataviz.py             [PASS] snippets/Chart-stacked-area.reference.html
                                 (1 charts, 0 blocking, 0 advisory)
                                 ❌ DataViz gate FAILED — DV-D02-A on data-dv-type="spark"  EXIT 1 ← NOT MINE
_gate_dataviz_vars.py            ✅ every colour presentation attribute resolves in at
                                 least one theme (15 files, 532 refs, 4 themes)            EXIT 0
_validate_no_hardcode.py         ✅ No-hardcode gate passed (11 tranche file(s)).           EXIT 0
_validate_a11y.py                a11y gate: 136 snippet(s), 0 failure(s), 198 warning(s)   EXIT 0
_validate_compose.py             RESULT: PASS ✅                                            EXIT 0
gen_showroom.py --check          OUT OF SYNC — 66 stale, 6 of them chart-*                 EXIT 1
```

**`gen_showroom.py` has no per-page flag** (`main()` takes only `--check`/`--selftest`) and its
printer truncates the stale list to 6; re-run with the slice removed, the true count is **66 stale,
of which 6 are chart pages (`chart-bar`, `chart-combo`, `chart-donut`, `chart-line`,
`chart-sparkline`, `chart-stacked-area`) — one per #259 lane — and 60 are pre-existing.**
NOT regenerated: 60 unrelated pages is not this lane's diff. `_validate_screen.py` and
`_build_all.py` not run (fenced by the brief).

## Driven — Chromium 151, `goto("file://…")`, never `set_content`

Sandbox had playwright + a chromium download but no `libXdamage.so.1`; resolved with
`LD_LIBRARY_PATH=/tmp/pwlibs/usr/lib/aarch64-linux-gnu` (the .deb the #259 core lane already
extracted). Chromium really launched; every number below is read out of the live DOM.

**Per combination (mono · legacy · console · supercharge) × (light · dark) — 8/8 identical, 8/8 green:**

| assertion | value |
|---|---|
| pageerrors / console errors | **0 / 0** |
| `path.dv-band` | **3**, all 3 with `data-fxs` + `data-ys` + `data-tip` + `tabindex="0"` + `role="img"` + `aria-label` |
| curve commands in any `d` | **none** (dv-line-011: M and L only) |
| `g.dv-marker` | **30** (10 categories × 3 series), all 30 with `data-fx` **and** `data-x0` |
| marker centre vs its band's first vertex | **0.00px** — the `data-x0` proof |
| `polyline.dv-band-line` / `text.dv-barkey` / `text.dv-label` | 3 / 30 / 10 |
| gridlines / baseline / tick labels | 4 / 1 / 4 |
| table spine | **10 rows × 4 header cells**, rewritten by the engine |
| band fills resolving to nothing | **0** — 3 distinct colours, `rgb(118,102,130)` / `rgb(164,92,58)` / `rgb(87,124,120)` |
| band-line strokes / marker fills | same 3 colours (no dead `var()` anywhere) |
| **dv-2px-separation, smallest clear ground between adjacent bands** | **2.20px** at 1280px **and 2.20px at 760px** |

**Tooltip.** Hovering marker 12 opens `#dvTip.on` reading **`B · Savings · Q3 24: 80`**, and that
marker's own `aria-label` is `B, Savings, Q3 24: 80` — the same number the table row carries,
because both come off one spec.

**Resize re-fits.** First four marker x at 1280px = `123.3, 238.3, 353.3, 468.3`; at 760px =
`97.3, 160.3, 223.3, 286.3`. Separation held at 2.20px through the reflow.

**Filter re-renders (rule 14).** Unticking *Q1 24* and *Q2 26*: markers **30 → 24**, category
labels **10 → 8**, **table spine 10 → 8 rows**, and the svg `aria-label` now opens
"… Current Q2 24 45, …" (Q1 24 gone). 0 errors on re-render.

**The SNIPPET itself, driven separately** (`Chart-stacked-area.reference.html`, self-contained,
injected copies only): 0 pageerrors, 3 bands, 30 markers, 30 letter keys, 10 labels, table
**10 rows × 4 cols** rewritten by the engine, 3 legend rows. Clicking the legend's *Savings* name
isolates it — the other two bands take `is-ghost`, which works because the engine emits
`class="dv-band dv-series"` (dv-legend's delegated click targets `.dv-series[data-series-group]`;
the baked exemplar's bands carried `dv-band` alone and were not clickable).

## Mutation — the clauses bitten, not asserted

Four copies driven, then deleted:

| mutant | result |
|---|---|
| `if (lifted) { hi += ctx.GAP; }` → `+= 0` | **RED** — smallest band separation **0.00px** (dv-2px-separation gone). The gap is the clause, and removing it is visible in the rendered geometry. |
| `data-x0` dropped from the marker `<g>` | **RED** — first marker's centre lands **103.5px** off its band's first vertex (fitOne writes `translate(x − x0)` and the child's `cx` is added on top) |
| a negative value in a series | **RED** — `dv-render-stacked-area: "Savings" is -80 at "Q3 24" — a stacked area has no signed band (the total would stop being the silhouette); use type "column" for signed data`; **0 bands drawn** |
| **control** (unmutated) | **GREEN** — 0 errors, 3 bands, 30 markers, 2.20px |

## What I could NOT do — first obstacle, named

1. **The `Total` column is gone from the table spine.** `writeTable()` in `dv-render.js` owns the
   spine and emits category + one column per series; the baked recipe's computed `Total` column (and
   its `.dv-total` CSS, which is now unused) is not re-emitted. I did not touch the core. **Core
   request, below.**
2. **The height half of s248-D2 is inert for this scope** — `canon.css` pins the plot svg to
   `height:260px` inside `.cn-chart-stacked-area` and `figure.dv-fit-on` releases only `width`, so
   `fitHeight`'s "the box must FOLLOW the viewBox" probe fails and returns `data-h`. Fixing that is a
   canon.css change outside my files.
3. **No `APOLLO-DEMO` fence exists in this snippet** (s258-D3). Its showroom chrome is the two bare
   `<h2>` headings, unfenced before this lane, exactly as lane A found on Chart-bar. The DATA +
   `dvRender()` bootstrap is deliberately NOT fenced — it is the pattern a build copies, not harness.
4. **The `<svg>` gained `data-pt="14" data-pb="30" data-h-min="200"`** — the engine's defaults, made
   explicit so the frame is readable. Flagged rather than left implicit.

## Core requests — verbatim, for the conductor

> **`dv-render.js` `writeTable()` should support an optional TOTAL column.** A stacked chart's table
> answer is incomplete without the stack total — the baked Chart-stacked-area spine carried
> `<th scope="col" class="dv-total">Total</th>` and a `<td class="dv-total">` per row, and the CSS
> for it still ships. Suggested shape: `spec.total = true` (or the type partial hanging
> `fn.total = true`), emitting one extra header cell and one extra `<td>` per row carrying the raw
> sum. ~140 code bytes in the core. I did NOT edit the core; the snippet ships without it and the
> `.dv-total` rule is currently dead CSS.

> **`fitOne()`'s `<g>` branch should fail loud, not silently double.** A `<g data-fx>` with no
> `data-x0` gets `translate(x − 0)` written onto it while its children keep their authored `cx`, so
> the mark lands at roughly twice the distance from the gutter. **The baked exemplar this lane
> replaced shipped exactly that defect** (`knowledge/snippets/Chart-stacked-area.reference.html`
> before this change: twelve `<g class="dv-marker" data-fx="…">` with no `data-x0`), and it was
> invisible because nothing measured it. Either default `data-x0` to the child's own `cx`, or throw.

## RULING-SHAPED — Dave's word, not a lane's

1. **The page budget is 477 bytes from red on the SECOND consumer of the engine.** Lane A reported
   112 bytes on Chart-bar; this lane lands at 477 on Chart-stacked-area, and the gate is already RED
   on `Chart-combo` (43,518 — it consumes bar + line + combo on top of the core) and on
   `Chart-donut` (37,787). The engine's whole design is one shared core + n small type partials, and
   the page budget prices the core **once per member** as if it were that member's own payload.
   Three shapes, none of them a lane's: (a) re-dial `PAGE_BYTES`; (b) price the shared engine core
   ONCE per page rather than once per member; (c) accept that a multi-type member (combo) cannot
   exist under this budget. **Not decided here.**
2. **`_validate_dataviz.py` does not know `stacked-area` is a stack.** `DTYPE_CANON` folds
   `stacked-column` and `stacked-bar` into `stacked`; `stacked-area` is a separate `KNOWN_DTYPES`
   member and therefore skips dv-004 entirely — including when the figure was fully baked, i.e. it
   has been skipping it since the component landed at #95. Adding `"stacked-area": "stacked"` to
   `DTYPE_CANON` would fold it in, but `_rect_stack_gap` cannot measure paths, so the fold would
   convert a silent skip into a blocking demand for a markup stroke on an EMPTY canvas. Both halves
   are the same question lane A raised: **does a gate accept a DRIVEN receipt for the rules only
   rendered geometry can prove?** I did not touch the gate.
3. **`behaviour.partial` — I listed FOUR names; Chart-bar's meta lists three.** The schema says
   `partial` is "the AUTO-BEHAVIOUR name(s) … that the snippet carries", and this snippet carries
   `dv-behaviour, dv-legend, dv-render, dv-render-stacked-area`. Lane A wrote three as briefed and
   flagged the omission of `dv-legend` as ruling-shaped; I read the schema and wrote four. **The two
   metas now disagree in shape.** One of us is wrong and it is one ruling, not two.
