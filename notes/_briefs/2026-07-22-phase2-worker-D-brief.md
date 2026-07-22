# Phase-2 Worker D brief — CHARTS / DATA-VIZ KIT lane (itinerary row 53, lane-sized on its own)

*Cut by the wave-1 conductor session, 2026-07-22 (date from `date`), per the wave-2 divvy
(`GOOD-MORNING.md` §C·1). WORKER per `knowledge/_RUNBOOK-parallel-conductor.md`: NEW files only,
NO git, NO shared-registry/handoff writes. Receipt at the end. Model: Fable. Role comes from
Dave's opener line only.*

## The lane

**Charts / data-viz kit** — itinerary row 53, P1: "Bar / line / donut / sparkline. Fitness tests
invented these." This lane is a PROMOTION, not an invention: the kit already exists and has been
through 9 review rounds — your job is to graduate it into gated reference snippets.

## Survey debt (this lane lives or dies on retrieval — the kit is PARKED, not signed off)

- `python3 knowledge/_consult.py "dataviz chart colour categorical status"` first.
- **`knowledge/_proforma/DataViz-interactive.html` IS the kit** (built + 9 rounds, PARKED
  "good enough" — Dave has NOT signed it off). Promote its reviewed values/shapes as OBSERVED
  retrieval; every promotion is still provisional-agent until his sign-off — say so in each
  snippet header + your receipt. Do NOT edit the pro-forma file (fence; tranches are
  near-canonical, ruling 3 — the queued dedup pass reconciles them toward canon, not you).
- **`_proforma/_DATAVIZ-DECISIONS.md` + `_DATAVIZ-METHOD.md`** — the ruled ground. Colour rules
  that BITE here: **R-D9 categorical = ISOLUMINANT · STATUS = salience RAMP (red › amber › green ›
  blue)** · R-D5 deltas red/green only, the GLYPH wears the colour (3:1 labelled-glyph floor,
  R-D6 A′) · R-D3 amber carve-out (always black text) · R-D7 mode-stable red `#B92F1E` ·
  halation bloom/dance axis (R-D6) for thin strokes on dark. Mono: colour ONLY in RAG + dataviz.
- Sibling prior art: Worker B's `snippets/Stat-card` (delta arrows — consume its conventions) ·
  `snippets/Amount-display` (figure composites — note the figure-4/5/6 vouch is OPEN, B-Q5;
  bind the composites, flag the dependency) · `snippets/Table` (if you ship a chart-with-table
  spread). Legends/axis labels: `.t-cm-*` composites only.

## Worklist (ordered; cut line in the receipt)

| # | Snippet | Notes |
|---|---|---|
| 1 | **Bar chart** | Vertical + horizontal; categorical (isoluminant) + status (ramp) series variants. |
| 2 | **Line chart** | Multi-series; halation-aware stroke weights on dark; markers = real glyphs or pure CSS shapes. |
| 3 | **Donut / proportion** | Incl. single-value "progress ring" variant IF the kit has one (it's display, not the loader atom — that stays queued §C·4b). |
| 4 | **Sparkline** | Inline scale; pairs with Stat-card — receipt the composition seam. |

One snippet per chart type (`Chart-bar.reference.html` etc.) + meta each, OR one `Charts-kit`
snippet with the full spread if the kit's structure argues for it — your call, justify in the
receipt. SVG/CSS only, zero JS for static renders (interactive demos may use minimal inline JS
in the demo controls ONLY, like Drawer's — the specimens themselves stay static).

## Rules (identical to wave 1)

Theme-blind semantic bindings via `#token-manifest` (dataviz roles from `semantic-colour.json` —
never `color/mono/*` direct, never hexes) · radius roles · composites-only type · 4px grid ·
sentence case · no 600 weight · white type red-only · real icons only · AA + R-D6 glyph-contrast
by ROLE · full variant spread incl. dark (halation check per `_DATAVIZ-DECISIONS.md`) · empty +
no-data states (consume Worker B's Empty-state pattern by reference) · `_build_all.py` green
before each next snippet. Pressables (legend toggles, if promoted): the ADR-0013 partials
protocol — empty marker pair + `--phys-size` + `--spring`/`--press` byte-equal to Button +
`transform var(--spring)` in the control transition (contracts fire on registration — land them
now), `$members` JSON in receipt. Category proposal: likely a NEW "Charts" bucket — propose,
don't edit `gen_showroom.py`.

## Do NOT

Edit any `_proforma/` file · any existing snippet · `component-types.json` / `_validate_radius.py`
/ `gen_showroom.py` · tokens (dataviz token gaps → receipt; promotion is Dave's) · mint a loader
atom · touch git or handoff files.

## Receipt (mandatory, last act)

`notes/_receipts/<date from date>-phase2-worker-D-charts.md` — landed + cut line · what was
promoted from the kit vs newly judged (mark each PROVISIONAL-AGENT pending Dave's dataviz
sign-off) · `$members` JSON · MIGRATED_SNIPPETS basenames · category proposal · icon/token gaps ·
open questions · NO commits made.
