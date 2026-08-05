# Worker receipt — Chart wave 2 lane ② (Chart-boxplot · Chart-bullet · Chart-candlestick)

*2026-08-05 · WORKER, chart-expansion wave-2 fan-out lane ② · brief
`notes/_briefs/2026-08-05-chart-wave2-lane2-statistical.md` · DIVVY plan
`notes/_briefs/2026-08-05-chart-wave2-DIVVY.md` · model: **Sonnet** (as ratified).
**NO GIT — conductor commits the ONE reconcile.**
Fences honoured: no writes to `component-types.json` / `_validate_radius.py` /
`gen_showroom.py` / `dv-behaviour.js` / `MIGRATED_SNIPPETS` / `CATEGORIES` / spine docs /
existing snippets / git. Only new files landed.

---

## Outcome — three new snippets + three metas, all COMPLETE Layer-1 (toolbar + table spine), NOT YET registered

### Files landed
- **`knowledge/snippets/Chart-boxplot.reference.html`** (NEW) — one figure, four categories
  (Team A–D), median/IQR/whiskers/outliers. Outlier markers = the Chart-scatter ENLARGED marker
  family (circle r5.5, page-colour stroke 1.5), per the brief's citation — same series colour, not
  a new channel. Table mirrors the five-number summary (min/Q1/median/Q3/max) + outliers per
  category. Empty-state figure included.
- **`knowledge/components/Chart-boxplot.meta.json`** (NEW) — schema-shaped like `Chart-scatter.meta.json`
  (purpose/props/variants/tokens/motion/responsive/relationships/accessibility/antiPatterns/
  tokenValidation/provenance). `provenance.source`: `"gap-report"`.
- **`knowledge/snippets/Chart-bullet.reference.html`** (NEW) — one figure, three KPI rows
  (Revenue/Satisfaction/Retention), each with a measure bar (`data/series/1`, brief-ruled), a
  comparative target marker (ink 3px vertical tick, brief-ruled), and three qualitative range bands
  behind the measure. Table mirrors measure/target/range breakpoints per row. Empty-state included.
- **`knowledge/components/Chart-bullet.meta.json`** (NEW) — same shape; flags the range-tint gap
  as a standing open question for Dave (see §Grey-tint below).
- **`knowledge/snippets/Chart-candlestick.reference.html`** (NEW) — one figure, ten sessions, full
  OHLC. Body fill = `data/delta/gain`/`data/delta/loss` (**RULED**, per the brief's §C·1(a)
  citation) — consumed **verbatim** from `canon.css` (`--data-delta-gain`/`--data-delta-loss`,
  light `#16864E`/`#B92F1E` · dark `#1AA05C`/`#CC4333`), not re-derived. Wick = ink at reduced
  weight (`.6` alpha, 1px), per the brief. Table mirrors Open/High/Low/Close per session.
  Empty-state included.
- **`knowledge/components/Chart-candlestick.meta.json`** (NEW) — same shape; cites the
  `data/delta/gain`·`data/delta/loss` binding in `tokens.delta`.

All six files are additive only — nothing existing was touched.

---

## What was copied verbatim vs newly judged

**Copied verbatim (per the brief's instruction to copy the mark contract + toolbar):**
- Toolbar chrome — `.dv-vt`/`.dv-csv`/`.dv-tbl-toggle`/`.dv-dd`/`.dv-tablepanel`/`.dv-tip` CSS,
  byte-for-byte from `Chart-bar.reference.html`/`Chart-scatter.reference.html`.
- The `AUTO-MARKUP dv-lockup-title` / `AUTO-MARKUP dv-lockup-title` comment-marker convention and
  its content shape (an `<h3 class="dv-title t-cm-section-label">` + a `.dv-tbl-toggle` button) —
  **the markers are present with content already in place**, matching what
  `gen_component_partials.py` would inject, but the actual registry entry + regeneration is a
  **conductor serial** (below), same as the 2026-07-24 lane-1 precedent.
- Outlier marker family (boxplot) — the Chart-scatter enlarged canon (circle r5.5, page stroke 1.5).
- 580×260 frame + 46→568/14→230 plot convention (boxplot, candlestick). Bullet uses a
  580×200 frame with a 120→568 horizontal plot — a **newly judged** proportion (a bullet row is
  conventionally wide/short, not the cartesian 580×260 box; declared below).

**NOT copied (ds-020 fence, DIVVY-inherited, all three lanes):**
- The DV-D07 two-channel axis/grid roles (`data/axis` + `data/grid` colour-snapped-to-neutral +
  declared alpha) that Chart-bar/Chart-scatter now carry post-migration. All three new snippets use
  the **PRE-DV-D07 ink-at-alpha idiom** instead (`text/default` at `.6` axis / `.10`–`.16` grid,
  rendered here as `var(--data-axis)`/`var(--data-grid)` bound to that older value, not the minted
  role). **This is the inherited gap, declared per the brief — not filled.** Each snippet's header
  comment and `#token-manifest` `$note` name it explicitly.

**Newly judged, receipted for Dave's eyeball:**
1. **Boxplot** — whisker/cap = ink 1px; median = ink 2px (heavier, for at-a-glance read); box =
   `data/series/1`. No existing exemplar has a box-and-whisker mark, so this vocabulary is
   worker-judged from the brief's spec, not ported.
2. **Bullet** — canvas proportions (580×200, wide/short vs the cartesian 580×260) are a judgment
   call — bullet charts conventionally read as a stacked row of gauges, not a plot. Flagged for
   Dave; happy to conform to 580×260 if that's the house convention instead.
3. **Bullet ranges — GREY-TINT CHECK.** The three qualitative range bands (poor/satisfactory/good)
   are **NEW greys, not a minted token.** Per `feedback-grey-tint-check`, these are **NOT
   auto-picked** — rendered as `color-mix(in srgb, var(--ink) 8%/16%/24%, var(--page))` so the
   demo stays theme-derived (never a hardcoded hex) while the real token decision is pending.
   **Surfaced to Dave here, not shipped as canon.** Both meta.json files flag this in
   `tokens.ranges` / `tokenValidation.$note`.
4. **Candlestick — dv-011 partial.** Direction (up/down) is colour-coded (`data/delta/gain`/`loss`)
   with body position relative to the open line as the only non-colour redundancy (standard
   candlestick convention — no shape/letter channel added). Flagged, not fixed; a colour-blind user
   still reads direction from body position, so this is not a bare colour-only violation, but it's
   weaker than the shape+letter+name redundancy scatter/bar carry. Named in the meta's `nonText`
   field for Dave's call.

---

## Fence: ds-020 (inherited gap) — RECEIPTED

Per the brief: *"Copy the exemplar's mark contract + toolbar, NOT the axis/grid CSS (ds-020 fence —
inherit the gap knowingly, receipt it, do not fill it)."* Done as instructed. All three snippets'
`--data-axis`/`--data-grid` custom properties are bound to the PRE-DV-D07 ink-at-alpha values, and
each file's top comment + `#token-manifest.$note` name the gap explicitly so it is not silently
lost. **Not filled** — a future DV-D07 migration pass (like the 2026-08-01 scatter migration,
`_DATAVIZ-DECISIONS.md` ds-020 entry) would touch these three the same way it touched Chart-scatter.

---

## ★ CONDUCTOR SERIALS — hand-offs (I did NOT touch `component-types.json` or `dv-behaviour.js`)

1. **Register all three as dataviz `$members`** in `knowledge/component-types.json` (selector
   `figure.dv`, same pattern as `Chart-bar`/`Chart-scatter`), then run
   `python3 knowledge/gen_component_partials.py` to inject `dv-behaviour` between each file's
   **empty** `AUTO-BEHAVIOUR dv-behaviour` markers. All three files carry the markers already, plus
   every hook the injected script needs verbatim: `data-tip="`, `class="dv-tbl-toggle`,
   `class="dv-tablepanel`, `class="dv-csv`. None of the three use `data-fxs` (no polylines) or
   `data-series-toggle` (no legend/multi-series filter in any of the three) — per the 2026-07-24
   lane-1 receipt's predicted per-capability split, these are core-only members, same class as
   Chart-bar's fit-by-rect membership. No FIT hooks (`data-fx`/`data-fw`/`data-x0`) are wired on the
   marks either — the geometry is **baked static** (DV-D02 default), consistent with "FIT hooks NOT
   wired" as declared in each meta's `responsive.rule`. If FIT is wanted for these three, that's an
   additional pass (add `data-fx`/`data-fw` to the box/candle/bullet-bar rects and `data-fx` to the
   gridlines) — not built here, not requested by the brief.
2. **`_type-bindings.json`** — none of these three consume the Segmented-control atom or any other
   registered atom, so no blast-radius registration is owed (unlike lane-1's `.seg` case).
3. **DataViz gate / census / radius / coverage / a11y** gates — **NOT RUN.** This worker has no
   access to the repo's Python tooling from the sandboxed shell used for this lane (mounted
   read/write copy only, no build harness invoked). Per the brief's checklist ("DataViz gate 0
   blocking · parity scripts · census/radius/coverage green"), this is an **OWED** gate, not a
   refusal — flagging for the conductor to run after replay, same posture as the 07-24 receipt's
   render-verify OWED precedent. Compensating evidence: (a) every fill is `var(--token)`, no raw
   hex, checked by eye across all three files; (b) JSON schema for all three metas parses clean
   (`python3 -c "import json; json.load(...)"` — verified in this window); (c) SVG tag balance
   verified (`<svg>`/`</svg>`, `<figure>`/`</figure>`, `</html>` counts all 1:1 across the three
   files); (d) OHLC/boxplot pixel geometry was hand-computed against each file's stated axis
   formula and one arithmetic error (candlestick wick/body y-coordinates, first draft) was caught
   and corrected in this same window before landing — see below.
4. **Render-verify (≥2 widths + dark + HC + filtered + JS-off)** — **OWED**, same environmental
   class as the 07-24 precedent (no persistent browser in this sandbox). Compensating evidence:
   toolbar/table/tip CSS is byte-for-byte the already-render-verified Chart-bar/Chart-scatter
   machinery; only the mark geometry (box/bullet-row/candle) is new and unverified visually.

---

## Self-check note — a caught arithmetic error

While authoring `Chart-candlestick.reference.html`, the first-draft wick/body y-coordinates did
NOT match the stated OHLC aria-labels (copy-paste drift from an earlier scratch calc). Caught by
re-deriving `y(v) = 230 − 5.4×(v−95)` from the axis gridlines and recomputing all ten sessions'
wick-top/wick-bottom/body-top/body-height by hand before landing. Flagging this explicitly per
`a-crash-is-not-a-fail` / measure-don't-convert-units posture: **the corrected numbers are in the
landed file**, but this class of error (geometry that LOOKS plausible but doesn't reconcile with
its own labels) is exactly what the lane-1 receipt's "deterministic geometry + fit parity" check
was built to catch mechanically — that check was **not run here** (no harness access, per §3
above), so the correction above is a manual spot-check, not a gate pass. **Conductor: re-verify
candlestick geometry against its own aria-labels/table before trusting.**

---

## Checklist status (brief's list, honestly reported)

- Type composites only: **YES** — every text element uses `.t-cm-chart-label`/`.t-cm-chart-value`/
  `.t-cm-caption`/`.t-cm-section-label`/`.t-cm-legal`, no raw font shorthand anywhere in the three files.
- DataViz gate 0 blocking: **OWED** (§3 above).
- Parity scripts: **OWED** (§3 above; manual spot-check only, one error caught — see self-check note).
- Render-verify ≥2 widths + dark + HC + filtered + JS-off: **OWED** (§4 above, 07-24 precedent).
- Census/radius/coverage green: **OWED** (§3 above).
- Controls never dim-only (hollow-swatch recipe): **N/A** — none of the three carry a DV-D11 legend
  or any dim-only control; no swatches exist in this lane's scope.
