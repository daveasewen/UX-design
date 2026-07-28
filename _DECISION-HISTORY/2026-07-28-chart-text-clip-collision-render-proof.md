# The text-cropping render-proof — four corrections to the instrument before one number could be trusted

provenance: session #29 · 2026-07-28
status: observed

> **Both-way links.** Spine: `_LIVE-STATE.md` ⏱ LATEST DELTA 2026-07-28 #29 · queue: `GOOD-MORNING.md`
> ★ LATEST banner. Brief this discharges: `notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md`
> finding 1. Ledger row: `knowledge/_proforma/_DATAVIZ-DECISIONS.md` § Open/pending · 2026-07-28.
> Artefact: `knowledge/_render/verify_chart_text_render.py`.

## Why this session existed

Dave found four defects by eye on `Chart-scatter.reference.html` after DV-J2 landed. Finding 1 —
*"the 'Savings (£000)' axis title collides with the topmost tick label, and the descender on the 'g'
is clipped"* — was the one he had now seen **twice** and named. He picked it as #29's first job from
three candidates, in plain language, the set explicitly declared incomplete.

The brief's own instruction was the load-bearing one: this is **encoding**, not a spot-fix. Apollo
already holds the rule (ds-005 fixed descender clipping) but `_validate_descender_clip.py` matches on
the CSS property `text-box-edge`, which SVG `<text>` never uses — the gate structurally cannot see an
axis label. The collision half has no gate anywhere. Confirmed by retrieval before designing, not
assumed from the brief.

## The arc — and the shape of it

**Every correction in this session came from one measurement disagreeing with another.** No correction
came from reasoning about the code. That is the whole methodological content of the window, and it is
why the file that came out of it is trustworthy: not because it was carefully written, but because it
was made to argue with a second instrument until they agreed.

### Correction 1 — the em box is not the ink (4.6 units of false precision)

The first measurement used `getBBox()` and reported `'Savings (£000)'` **6.00 units** above the
viewBox ceiling. Building a gate on that number was the obvious next move and would have been wrong:
`getBBox()` on SVG text returns the **em box** (font ascent/descent), not the glyphs.

An independent canvas ink-scan measured the true overrun at **1.38 units**. The em box over-reports by
**4.62** on this very label. A containment check written on `getBBox()` fires 4.6 units early — it
would have failed compliant charts on run 1, which is precisely the false-positive class the brief
warns about by name (*"a gate that encodes a rule without its principled exceptions is not
standardisation — it is a future false positive"*).

Same correction, other direction: `'Monthly income (£000)'` em box said 1.00 below the floor; ink said
**0.62**. And a reported `'150'` RIGHT clip **did not exist at all**.

### Correction 2 — a recovered baseline is an inferred baseline

The proof, once built, reported **TOP by 2.88** where the standalone probe had measured **1.38**. Two
instruments of mine disagreeing is a defect in one of them, so it was chased rather than averaged.

Cause: the proof recovered the text baseline as `getBBox().y + canvas fontBoundingBoxAscent`. On the
licensed cut those are not the same quantity — canvas reports **13.63** where `getBBox`'s ascent is
**15.00** — so every ink box sat 1.37 units off. Replaced with `getStartPositionOfChar(0).y`, which is
the **exact** glyph origin and is not inferred from anything.

### Correction 3 — a canvas re-render does not reproduce SVG layout

The same run invented a `'150'` clip of 1.20 units. Cause: horizontal extents were taken from the
canvas re-render, which does not carry SVG letter-spacing or kerning. Fixed by splitting the
measurement by axis, and the split is now the file's design:

| Quantity | Source | Why |
|---|---|---|
| baseline | `getStartPositionOfChar(0).y` | exact, never inferred |
| horizontal | `getBBox()` | laid-out truth, carries letter-spacing; ~1u wider than ink (side bearings) = **conservative** |
| vertical | canvas ink scan | the one place the em box is catastrophically wrong (15.00 vs 10.38), and the one measurement letter-spacing cannot affect |

After both corrections the proof reproduced the standalone probe **exactly** — `TOP by 1.38`,
collision `13.96 × 3.50`. Agreement between two independently-written instruments is the receipt;
neither one alone was evidence.

### The unplanned finding — `set_content()` silently drops a stylesheet

Chased because the numbers still disagreed. `page.set_content(html)` gives the page a base URL of
`about:blank`, so the snippet's linked `../canon/type.css` **404s silently**:

| | stylesheets | axis-title size | bbox width |
|---|---|---|---|
| `goto("file://…")` | 2 | **14px** | 95.94 |
| `set_content(html)` | 1 | **16px** | 109.64 |

A chart **14% larger than the one that exists**. The trap has teeth because
`document.fonts.check('16px HSBC_MtUnivers_Latin')` returns **true in both cases** — the fontconfig
alias covers the snippet's `--font` *and* type.css's `--uf`, so the standing licensed-cut assertion,
the one guard every render-proof carries, structurally cannot see the difference.

This is `embedded-payload-url-trap` (srcdoc/`set_content` re-base relative URLs; a 404 stylesheet is
silent) with a new and worse instance: previously the failure was a missing stylesheet, here it is a
**plausible but wrong** stylesheet state that passes the existing green-light check.

**Blast radius, measured not assumed:** `knowledge/_render/verify_dv_j2_render.py` (#27, canon) uses
`set_content`. Its assertions were re-run both ways — toggle height 32, hit target 44×44 — and are
**identical**, so its verdict stands. But the toggle's own label rendered 12px vs 13.33px, i.e. it
stands by luck: any type-sensitive assertion added to that file later would silently measure a page
that does not exist. Logged as a runbook debt, not fixed here (Dave's scope ruling).

### Correction 4 — the bite was vacuous

The first `--bite` injected a duplicate label into Chart-scatter and asserted "a COLLIDE appeared".
Chart-scatter **already** collides, so the assertion could not distinguish *detected the injection*
from *was going to fail anyway*. This is the DV-D17 lesson (an absence-only test passes a full revert)
in mirror form, and it landed on the author in the session that quotes it.

Replaced with a **sentinel**: the bite injects a `ZZBITE` label, and the check demands a finding that
**names the sentinel** — a condition that cannot pre-exist.

### The instrument must bite both ways

A proof that only ever reports RED cannot show it is measuring anything. Three states, all run:

| Mode | Result |
|---|---|
| plain | **FAILS** — `CLIP 'Savings (£000)' TOP by 1.38` · `COLLIDE '75' x 'Savings (£000)' 13.96 × 3.50`, both widths, both svgs |
| `--bite` | **detects** — 8 findings naming `ZZBITE`, both a CLIP and a COLLIDE |
| `--control` | **GREEN** — with the fix applied live, every finding clears |

`--control` doubles as the **specification of the remedy without committing one**: re-anchoring the
title to the axis line (`x=2→46`) clears the tick column, and `y=9→11` puts the ink top at +0.62,
inside the ceiling. One move answers both failures. The numbers are the agent's arithmetic; the
geometry is Dave's to rule (derivation governance — the engine never derives-and-promotes).

## What Dave ruled

- **Tolerance stays 0.5 user units** — *"1. but you have to show me, watch the gauge for this though."*
  Shown before it stood: magenta viewBox edge + cyan 0.5 line, magnified. The ceiling line **cuts
  through the caps** of "Savings (£000)"; the floor line merely **kisses the descenders** of "Monthly
  income (£000)". One is a defect, the other is antialiasing. `'Monthly income'` therefore passes, and
  `--control` deliberately does **not** touch it — moving it would be an unruled edit.
- **Land scatter, park the corpus sweep.**
- **Full capture ritual at the Red boundary** rather than deferring inscription.

## What is NOT proven, and must not be read as debt

The `--all` sweep returned **78 findings across 6 charts. They are UNTRUSTED.** Two named blind spots,
both in the instrument:

1. **Ancestor transforms.** `getBBox()` is element-local; it is compared against the **root** viewBox.
   Any intervening `<g transform="…">` makes the comparison meaningless — almost certainly the source
   of Chart-bar's horizontal variant reporting every label "LEFT by 3–17" and Chart-combo's right axis
   "RIGHT by 21.45". Fix: compose `getCTM()` before comparing.
2. **Ancestor visibility.** Hidden-ness is tested on the text node, not its parents. A hidden `<g>` —
   a chart variant, donut's `st.visible[id]` centre-figure — reports as live text and collides with
   the visible set. Signature: `'Leisure' × 'Leisure'`, nodes colliding with themselves.

**A count is not a measurement.** 78 is a count of suspicions from an instrument with two known
defects. The corpus-wide clip/collision debt is **UNMEASURED** and stays that way until both are
fixed. Anyone quoting 78 as a debt figure is repeating the mistake this file exists to record.

## Sandbox note (runbook debt)

Mutations were first applied by writing a sibling temp file, so relative URLs would still resolve.
The mount refuses `unlink()` with EPERM (no `rm`, `mv` only), so every run littered
`knowledge/snippets/` with a file matching the build's own `*.reference.html` glob. Replaced with
**DOM mutation after `goto`** — no temp file, no cleanup, URLs still correct. The stray from the failed
runs was moved out of the glob to repo root as `__tmp_moved.html`; it is untracked and needs one
manual delete.

## Resolved state

- `knowledge/_render/verify_chart_text_render.py` — NEW, three modes, all three run and behaving.
- Finding 1 is **measured and instrumented**, not fixed: the proof reports the defect; the geometric
  remedy is specified by `--control` and awaits Dave's ruling on the numbers.
- Findings 2 (responsive) RULED + GATED in #28 · 3 (titles) RULED-not-buildable · 4 (legend molecule)
  unstarted. **The brief's list is still open** — a fifth surfaced in #28 as predicted, and this
  session added a sixth in substance: the render-proof family's `set_content` exposure.
