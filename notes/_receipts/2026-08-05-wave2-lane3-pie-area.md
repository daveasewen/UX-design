# Worker receipt — Chart wave-2 lane ③ (Chart-pie + Chart-stacked-area)

*2026-08-05 · WORKER, chart-expansion wave-2 fan-out lane ③ · brief `notes/_briefs/2026-08-05-chart-wave2-lane3-pie-area.md` ·
DIVVY `notes/_briefs/2026-08-05-chart-wave2-DIVVY.md` · **NO GIT — conductor commits the ONE reconcile.***
*Model: Sonnet, as divvied.*
*Fences honoured: no writes to `component-types.json`, `dv-behaviour.js`, `_validate_radius.py`, `gen_showroom.py`, `MIGRATED_SNIPPETS`/`CATEGORIES`, spine docs, existing snippets (donut/line untouched), or git.*
*STALE queue item skipped, per brief instruction: "promote grouped/stacked bars (D-Q3)" already LANDED 2026-07-24 (`Chart-bar.reference.html:39`) — not rebuilt. Two items only, as scoped.*

## Outcome — both new members landed

### Files created (worker-owned, per fences)
1. **`knowledge/snippets/Chart-pie.reference.html`** (new, ~430 lines) — ported from `Chart-donut.reference.html` (2026-07-24 exemplar copy-source, itself named by the brief). Two figures + empty state:
   - **Spider + legend** and **direct labels** variants, both carried over unchanged from the donut (D-Q2 default stays OPEN — cited, not re-decided, matching donut posture).
   - **ri dropped to 0** — segment `d` paths recomputed as `M cx,cy L edge A ro ro 0 large 1 edge Z` (full wedges, no ring hole). Same `cx`/`cy`/`ro`/`a1`/`a2` as the donut, computed with a one-off Python script for precision (not hand-eyeballed) — so every leader, label, legend row and table cell is **byte-identical in position** to the donut's, only the fill geometry differs.
   - **Centre total + DV-D13 selection-follow wiring REMOVED** — donut-only per the brief; no `data-total` display, though `data-total="2320"` stays on the figure element for parity/dv-pie-010 bookkeeping even with nothing rendering it.
   - dv-pie-009 (≤6 slices) — 5 segments, same data as the donut.
   - Legend-as-filter (DV-D11 dual-gesture), value ⇄ % segmented toggle, table-view popover, CSV — all copied verbatim (CSS byte-identical to the donut's).
   - **AUTO-MARKUP/AUTO-BEHAVIOUR markers pre-landed EMPTY** — same standing worker fence as every prior wave (Chart-bar's lane-① receipt, Chart-donut's own lane-② landing). Registration is the conductor's serial.
2. **`knowledge/snippets/Chart-stacked-area.reference.html`** (new, ~380 lines) — line-family frame/toolbar ported from `Chart-line.reference.html` (2026-07-23 exemplar); stacking recipe ported from `Chart-bar.reference.html`'s **already-landed** stacked-column figure (D-Q3, 2026-07-24 — consumed here, not re-promoted). One figure (3 series × 4 quarters) + empty state:
   - **Three cumulative bands** as closed SVG polygons (top boundary forward, bottom boundary back), fills bound to `data/series/1-3` at a flat `--stack-fill-alpha` (default 1) — a **receipted CSS dial, not a minted token** (brief: "receipt any tint you need but do NOT mint one").
   - **Top-edge strokes** — one straight-segment polyline per band boundary (dv-line-011 compliant), stroke = the series token.
   - **Vertex markers** — line exemplar's BACKGROUND mode (series fill + page stroke r4.2), tip/aria-label carry the **per-series** value at that point (not the cumulative band height).
   - **In-fill letter keys** — follow the stacked-column recipe exactly: one `.t-cm-chart-key` letter per band per quarter, bound to `--data-text-on-series` (`data/text/on-series`, minted 2026-07-27 for Chart-bar — **reused, not re-minted**), positioned at each band's vertical midpoint.
   - **Table mirrors per-series values AND a computed Total column** (140/153/168/190 — sums verified by hand against the three series columns, same numbers as Chart-bar's stacked-column table so the two members describe the same underlying dataset).
   - Legend-as-filter, plain swatches (not the line's shaped-swatch set — receipted rationale in-file: band identity is the in-fill letter, matching Chart-bar's stacked-column legend, not Chart-line's per-point marker-shape legend).
   - **AUTO-MARKUP/AUTO-BEHAVIOUR markers pre-landed EMPTY.**
3. **`knowledge/components/chart-pie.meta.json`** (new) — full schema (purpose/props/variants/tokens/motion/responsive/accessibility/antiPatterns/tokenValidation/provenance), modelled on `chart-donut.meta.json`'s shape. `tokenValidation.result` marked **UNPROVEN** (see below), not PASS.
4. **`knowledge/components/chart-stacked-area.meta.json`** (new) — same shape, modelled on `chart-line.meta.json` + the stacked-column notes in `chart-bar.meta.json`. Also **UNPROVEN**.
5. **This receipt.**

Both JSON meta files validated with `python3 -c "json.load(...)"` — parse clean. Both HTML files tag-balance checked (`<figure>`/`</figure>` and `<svg>`/`</svg>` counts match: pie 2/2 figures, 8/8 svgs including demo-control icons; stacked-area 1/1 figure, 4/4 svgs).

## ⚠ Deviations from a full landing — declared, not silent

- **No DataViz/contrast gate run.** This worker window has no access to the gate runner (`_validate_dataviz.py` / the contrast-pair script) or a browser for render-verify. Both `tokenValidation.result` fields are marked **UNPROVEN**, explicitly NOT copy-pasted as PASS, with a note that the bound tokens are the SAME ones already measured clean on Chart-donut/Chart-line/Chart-bar (series 1–5, data/axis, data/grid, data/text/on-series) — so the risk is geometry/structure, not token contrast. **Conductor: run the same gate pass done for lanes ① and ② before promoting past PROVISIONAL.**
- **render-verify: OWED**, same standing precedent as the 07-24 lane-① receipt (no persistent browser in this worker's environment). Compensating evidence: (a) both files are structurally verbatim ports of already render-verified exemplars (donut for pie's chrome; line + bar-stacked for stacked-area's chrome), (b) pie's segment geometry was computed with a script, not eyeballed, (c) stacked-area's band/marker/key coordinates were derived arithmetically from Chart-bar's own already-shipped stacked-column rect positions (same dataset, same y-scale), not invented. **Gate for close: Dave eyeballs both in `showroom/` once regenerated.**
- **census/radius/coverage/parity scripts** — not run (no tool access in this window). Structurally these files use only existing composite classes (`.t-cm-chart-*`, `.seg`, `.dv-leg*`, `.dv-tbl-toggle` etc.) and no raw font shorthand or hex fills outside CSS custom properties, so a clean run is expected but **UNVERIFIED, not claimed**.

## ds-020 fence — inherited, receipted (per instruction, not filled)

- **Chart-pie**: checked and found **N/A** — the donut/pie pattern carries **no axis or gridline CSS at all** (it's a ring, not a Cartesian frame), so there is nothing under that fence to inherit for this file. Noted in both the file header and the meta's `$survey` so it isn't mistaken for a silent skip.
- **Chart-stacked-area**: the fence **applies and is inherited knowingly**. `.dv-grid`, `line.dv-axis`/`text.dv-axis` are copied byte-for-byte from `Chart-line.reference.html` — not re-derived, not re-audited by this lane. Flagged in the file's header comment and in the meta's `$survey`/`tokens.axis` fields.

## ★ CONDUCTOR SERIALS — hand-offs (did NOT touch `component-types.json` or `dv-behaviour.js`)

### 1. Register both as `dataviz` `$members`
```jsonc
// component-type/dataviz/$members — add:
"Chart-pie": { "selector": "figure.dv" }
"Chart-stacked-area": { "selector": "figure.dv" }
```
Then `python3 knowledge/gen_component_partials.py` to inject `dv-behaviour` into both files' empty AUTO-MARKUP/AUTO-BEHAVIOUR markers.

### 2. Chart-pie's sweep-hook variant
The donut's sweep hook (still itself a conductor serial, per its own receipt — never built) targets `data-cx/-cy/-ro/-ri/-a1/-a2`. Chart-pie's segments carry the same five attributes **minus `data-ri`** (full wedges have no inner radius). Whoever builds the sweep hook needs a `data-ri` presence check (falls back to `ri=0`) or a small pie-specific branch. Flagged in-file (segment path comment).

### 3. Chart-stacked-area's fit-hook gap
The existing `dv-behaviour` `fitOne()` selector set (per the Chart-bar lane-① receipt's per-capability contract split) knows rects (`data-fx`+`data-fw`) and polylines (`data-fxs`). It does **not** yet know `.dv-band` (filled polygon path) or `.dv-band-line` (top-edge polyline sharing `data-fx` semantics differently than a bar). Until extended, this chart is JS-off-fixed-width (580×260 + scroll) — the same static answer every member has pre-fit, not a regression, but flagged so the fit doesn't silently no-op once registered. `data-fx` fractions ARE present on every other element (grid/axis/markers/keys/labels) for when this lands.

### 4. `.seg` / toolbar blast-radius
Chart-pie consumes `.seg`/`.seg.sm` (value ⇄ % toggle) same as the donut — if `_type-bindings.json`'s blast-radius file set still isn't fully reconciled from lanes ① / ②, this file needs adding too. Chart-stacked-area does NOT use `.seg` (no view-mode toggle), so it doesn't need that particular registration.

## Open Qs / for the conductor
- Chart-stacked-area's legend-filter-hides-a-middle-band caveat (bands don't reflow) is the same known gap Chart-bar's stacked-column receipt already flagged — not re-solved here, just inherited and re-noted so it isn't lost when the two members are compared side by side.
- `--stack-fill-alpha` is a new CSS custom property, not a token — flagged per the "receipt any tint you need but do NOT mint one" instruction; if the conductor wants it removed (flat 1 with no dial) that's a one-line trim, not a re-architecture.
- Neither file was added to `_type-bindings.json`'s blast-radius sets (serial file, not touched) — the `.seg`/`.seg.sm` consumption above is the one that needs it (Chart-pie only).
