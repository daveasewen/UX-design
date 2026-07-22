# 2026-07-22 — Chart-expansion scoping · Console corner architecture · heatmap park

*Opus solo, evening. Opened as "good morning"; became a scoping + tactical session — a chart-expansion
programme, a corner-radius architecture moment, and a heatmap design exploration that concluded "this
needs a tool, not a snippet." No fan-out ran; deliberately wrapped at Amber for a clean build seam.
Spine entry: `_LIVE-STATE.md` LATEST 2026-07-22 (evening, Opus). Forward pointers: `_FUTURE-STATE.md`
★★ tuner + ★ heatmaps.*

## Arc 1 — DataViz labels were below the ramp floor (quick win)
Dave: "make all the labels the lowest size on the font ramp, ~12px, medium weight." The chart-label
SVG text (`dv-label`/`dv-axis`/`dv-val`/`dv-key-el`/`dv-direct`) sat at a hardcoded **11px** — *below*
the KB ramp whose floor is `--fs-7: 12px`. The tell was the off-ramp size, so the fix is a **snap to the
ramp token**, not a literal: `font: 500 var(--fs-7)/1`. DV-D05 alignment. **Consequence flagged, not
hidden:** this flattened three deliberate emphasis weights — values (600), on-chart keys (700),
direct-amount (600) — all to 500. Left legend text at 12/400 (chrome). Reversible; awaiting Dave's nod
on restoring the emphasis.

## Arc 2 — Heatmap colour: the reasoning that ended in "build a tool"
Dave asked the real question directly: "can't we interpolate — what range, black→red→yellow→white?"
The read that emerged:
- **Yes, interpolate — in OKLab (perceptual), not sRGB.** sRGB interpolation muddies the mid-band; OKLab
  keeps equal data steps looking equal. Built a live tuner to prove it: `reviews/HEATMAP-RAMP-2026-07-22-v1.html`.
- **The property that carries the data is monotonic LIGHTNESS**, not hue. Heatmap cells are large filled
  areas → they sit in the luminance-driven **bloom** regime, not the thin-line **dance** regime
  ([[halation-bloom-dance-model]]). Monotonic lightness also means greyscale-safe + colourblind-safe.
- **On black→red→yellow→white specifically:** it's the classic incandescent ramp — maximum
  discriminability, but it runs straight through Dave's two *least-stable* hues (red + yellow,
  [[colour-stability-red-yellow-problem]]) and is a lot of chroma for "very mono." Verdict: keep it as an
  **opt-in high-contrast variant**, not the default. Default = **warm-mono** (warm off-white → `#B92F1E`
  → near-black): a heat cue, one hue family, monotonic lightness.
- **Why it can't be a snippet (Dave's conclusion, and the important one):** a heatmap is *two* unbounded
  problems at once — data dimensionality (5×5 … 100×100, so no single static lock-up) and **continuous
  colour** (can't be pre-baked into flat DTCG tokens the way categorical-series + RAG are). Both point at
  a **live, code-driven interpolation tool** for when Apollo gets an interface. So heatmaps are **PARKED**
  with the intention logged; the tuner is the proof-of-mechanism seed. A new sequential `data/heat/*`
  token **class** (a third dataviz colour class, distinct from categorical-isoluminant and status-salience)
  is deferred with it.

## Arc 3 — Console corners: a misstep, its correction, and the architecture answer
Dave: "can Console have 4px corners, just to try it." I set `border-radius/default`→4 **and** flattened
`surface` 12→4 — i.e. uniform 4. Dave caught it looking at the Console bar chart: "no rounded corners on
the bars… you've made all the corners 4, that's not what I want — we should be tuning corners for every
component type; buttons and cards already differ. Is this architectural?"

Two findings, both verified in the repo before answering (verify-before-asking + attribute-the-diff):
1. **The bars were never the problem.** `rect.dv-series` binds *no* radius (no `rx`, no `border-radius`;
   CSS `border-radius` doesn't apply to SVG rects anyway). Only Chart-bar's dashed **empty-state frame**
   takes a theme radius (`surface`). So the 4px change couldn't and didn't round the bars — they're
   square in every theme, which is *correct* for dataviz (rounding a bar distorts the datum).
2. **The real mistake was mine, not the architecture's:** I moved two independent dials together. Per-type
   corner tuning already exists in **two tiers** — the semantic ROLE tier (`control`/`surface`/`indicator`,
   the reason buttons≠cards) and the **ADR-0013 component-type tier** (finer per-type dials, the same
   registry that holds the motion press tokens; unused for radius only because the three roles have covered
   every case so far). So: **not an architectural hole — an unpopulated slot plus a uniform-dial error.**
   Fix: restored Console to control/indicator = 4, surface = 12 (buttons 4 / cards 12 / bars square).

**The lesson that generated a forward task:** corners want to be tuned *per type, by eye* — which is why
Dave asked for, and I logged (★★, "don't let me forget"), a **live radius/corner tuner**. If corner-per-type
tuning starts recurring, that's the accretion signal to mint component-type radius groups (like field-family).
An explicit `data-mark` radius=0 token is the clean move IF charts ever need themeable corners.

## Arc 4 — Programme scope + how we'll run it
Mapped Dave's wish-list against the proforma: grouped/stacked bars already exist (→ promote, = D-Q3); 8
net-new after parking heatmaps (butterfly ×2, scatter, histogram, box, pie, stacked area, bullet,
candlestick). Deliverable per type = the lock-up (chart + controls + legend + table spine) projected across
4 themes × light/dark. **Run mode ruled: prove-one-then-wave** — exemplar = **scatter**, built end-to-end
next window for Dave to eyeball the lock-up, then fan out the rest as worker lanes (DV-D01 pipeline:
explore in `DataViz-interactive.html` → promote to `Chart-*.reference.html`).

## Resolved state / still open
**Resolved:** labels snapped (emphasis-restore pending Dave); Console corners fixed + provisional; heatmaps
parked with tool intention + seed tuner; tuner idea durably logged; programme scoped; build green 51/51.
**Open (unchanged):** the 16-Q ruling batch + dataviz sign-off (`GOOD-MORNING` §C·2). **Next:** scatter
exemplar, fresh full-budget window.
