# Worker receipt — Chart wave lane ① (Chart-bar + Chart-scatter)

*2026-07-24 · WORKER, chart-revisit fan-out lane ① · brief `notes/_briefs/2026-07-24-chart-wave-lane1-bar-scatter.md` ·
baseline HEAD `fa29858` (verified `git log --oneline -1` at lane start) · **NO GIT — conductor commits the ONE reconcile.***
*Model note: divvy ratified this lane at **Fable·medium**; this window ran on **Opus** (knob is Dave's at window-open) — flagged, no behavioural difference to the deliverable.*
*Fences honoured: no writes to GOOD-MORNING / _LIVE-STATE / _FUTURE-STATE / briefs / ledger spines / `dv-behaviour.js` / `_build_all.py` / `MIGRATED_SNIPPETS`/`CATEGORIES`.*

## 🟠 Context gauge at authoring: AMBER→RED ~68% (ESTIMATE ±15%)
Heavy reading ballast (GOOD-MORNING + _LIVE-STATE + exemplar receipt + full Chart-line pattern + Chart-bar) plus a full generate→build→verify cycle. Red-leaning ⇒ **conductor: re-verify the build-state + registry claims below before trusting.** Deliberate cut: Chart-bar landed COMPLETE + verified; Chart-scatter + proforma-fit deferred with precise specs rather than half-built (see §Deferred).

---

## Outcome — Chart-bar landed COMPLETE end-to-end; every Chart-bar gate GREEN

`knowledge/snippets/Chart-bar.reference.html` rebuilt to the full Layer-2 (Chart-line exemplar bar),
with **D-Q3 (grouped + stacked promote)**, **DV-D09 (h-bar → series-3)**, **DV-D07 + DV-D08 rebind**, and the
**menu 3/4 sort toggle**. 5 figures. The Layer-2 machinery is ported **verbatim** from the render-verified
Chart-line exemplar (same `dv-behaviour`, same control CSS, same fit hooks) — only the bar geometry is new,
and that is covered by the deterministic parity check below.

### Files landed (worker-owned, per fences)
- **`knowledge/snippets/Chart-bar.reference.html`** — REWRITTEN (558 lines). Figures:
  1. **Column, single-series, SORTABLE** — original/ascending/descending as **baked `data-dv-view` variant groups** (geometry generation-time), switched by a **seg that CONSUMES the Segmented-control atom** (`.seg.sm`, sliding `.ind` driven by `dv-behaviour`'s `moveSeg`); the **table mirrors the active order** via three baked `<tbody data-dv-view>` variants (`setView` toggles them too). + title, popover, fit, table-popover, CSV.
  2. **Horizontal bar, single-series** — **DV-D09 ENACTED**: default fill `data/series/3` (`#577C78`); column stays `series-1`. Value axis + gridlines ride the fit (horizontal-scaling per Batch-3 #6). + Layer-2.
  3. **Status — R-D9 salience ramp** (direct-labelled) + Layer-2.
  4. **Grouped column, multi-series (D-Q3)** — 3 series × 4 quarters; legend-as-filter + isolate (shift/dbl-click) + highlight; shaped+lettered swatches (circle A · square B · diamond C) mirroring **on-chart `.t-cm-chart-key` (12/700, ink)** letters above each sub-bar; AA hollow off-state.
  5. **Stacked column, multi-series (D-Q3)** — same series; in-segment letter keys (page-ink on fills); legend-as-filter.
  - **DV-D07 ENACTED**: axis/grid rebound to the two-channel roles `--data-axis`/`--axis-alpha` + `--data-grid`/`--grid-alpha` (supersedes the promotion-time `text/default@0.6` + `@per-mode-alpha` house treatment — the homeless-greys gap the wave-2 receipt flagged).
  - **DV-D08 ENACTED**: `.t-cm-chart-label`/`-value` 12/500 · `.t-cm-chart-key` 12/700 (supersedes `t-cm-legal`/`t-cm-caption`, 11→12).
  - **AUTO-BEHAVIOUR markers present but EMPTY** — membership is a conductor serial (see §Conductor serials). Every behaviour HOOK is in the markup (`data-tip`, fit fractions, `.dv-tbl-toggle`+`.dv-tablepanel`, `data-series-toggle`).
- **`knowledge/components/chart-bar.meta.json`** — refreshed (purpose/props/variants/tokens/motion/responsive/a11y/antiPatterns/tokenValidation) to the Layer-2 + new figures + rulings. Schema-valid (coverage gate 67/67, integrity schema 66/67 — the 1 invalid is lane ③'s combo, not this).
- **`knowledge/canon/_type-bindings.json`** — added `Chart-bar.reference.html` to the `.seg button` and `.seg.sm button` blast-radius file sets (the mechanical accompaniment to consuming the atom — exactly as Chart-line was registered; `moveSeg` targets `.seg`, so the sort switch must use the real atom, not a local clone). **Conductor: review this diff** (2 files' `files` arrays; I re-serialised the JSON with indent=2 — if the repo's canonical format differs, regenerate). Only MY file was added; Chart-donut (lane ②) still escapes — theirs to register.
- Regenerated (deterministic): `showroom/chart-bar.html` (+ `index.html`); `knowledge/canon/canon.css` (see §Shared-tree note — it was STALE at lane start; `gen_theme_cascade.py` brought it back in sync).

## Verification
- **DataViz gate**: `Chart-bar` **5 charts, 0 blocking, 50 advisory** — the 50 are the decorative gridline reads (`#E1E1E1` 1.31:1 L / `#484848` 1.90:1 D across 5 figures), DV-D07 working as ruled (1.4.11-exempt, advisory by design; no grid contrastPair declared).
- **Deterministic geometry + fit parity** (mechanical, no browser): **52 bars across 5 figures** — every baked `x`/`width` reconciles with its `data-fx`/`data-fw` fraction (±0.6), all in plot bounds. **chart↔table value parity: 52/52 tips** appear in their figure's table. CLEAN.
- **Full build gates** green for Chart-bar: snippet · a11y (0 fail) · coverage (67/67) · radius (0 strict) · **census unmoved** (0 press-shaped locals; quiet controls, not B-D7) · type-blast (registered, 0 escaped for Chart-bar).
- **RENDER-VERIFY: OWED (environmental blocker, not a refusal).** The sandbox **home directory rotates between bash calls** (`relaxed-compassionate-meitner` ↔ `youthful-wonderful-franklin`), so the Playwright `chromium-headless-shell` binary (downloaded successfully, 110 MB) and the pip module install under a home that does not persist to the next call — no browser survives to render. Per the standing "render-verify OWED" precedent. **Compensating evidence is strong**: (a) all mechanical gates green, (b) geometry/parity deterministically proven, (c) the ENTIRE interaction layer + control CSS is the byte-for-byte exemplar machinery, already render-verified at 2 widths + dark + HC + filtered + JS-off on 2026-07-23. Residual visual risk is isolated to bar-specific layout (grouped/stacked spacing, hollow legend off-state, seg-slide on the sort switch). An injected render copy is staged at `outputs/chart-bar-render.html` for whoever has a working browser. **Gate for close: Dave eyeballs `showroom/chart-bar.html`.**

---

## ★ CONDUCTOR SERIALS — hand-offs (I did NOT touch `component-types.json` or `dv-behaviour.js`)

### 1. Register Chart-bar as a dataviz member + the PER-CAPABILITY CONTRACT SPLIT (the wave note's "observed need", now observed)
The current `dataviz` `$behaviour.dv-behaviour.requires.declarations` demands `data-fxs="` — a **polyline-only** hook. Bar's fit rides **rects** (`data-fx`+`data-fw`), so bar legitimately lacks `data-fxs`. This is exactly the split the exemplar receipt predicted ("if a member legitimately lacks a hook … split the behaviour contract per-capability THEN, from observed need, not now"). **Now observed.** Minimal fix — make `data-fxs="` line-family-only:

```jsonc
// component-type/dataviz/$members  — add:
"Chart-bar": { "selector": "figure.dv" }

// component-type/dataviz/$behaviour/dv-behaviour/requires/declarations
// → keep the UNIVERSAL core (every member has these):
["data-tip=\"", "class=\"dv-tbl-toggle", "class=\"dv-tablepanel"]
// → move data-fxs (polyline fit) + data-series-toggle (multi-series legend) to a
//    per-member "extraDeclarations" (or a line/scatter-family sub-contract):
//      Chart-line/Chart-scatter: + "data-fxs=\""
//      Chart-bar (grouped/stacked present in-file): + "data-series-toggle=\""
```
Chart-bar's file-level check passes the universal core AND carries `data-series-toggle` (grouped/stacked); the ONLY thing blocking it today is the universal `data-fxs`. After the split, run `gen_component_partials.py` to inject `dv-behaviour` into Chart-bar's empty markers. (Same split unblocks lane ②'s donut/sparkline and lane ③'s combo — sparkline has no legend, donut no polyline, etc.)

### 2. `.seg` blast-radius — I registered Chart-bar; **lane ② Chart-donut still needs it** (`_type-bindings.json`, `.seg button` + `.seg.sm button`).

---

## Shared-tree note (for the reconcile)
This working tree already held **other lanes' uncommitted work** at lane start (lane ② Chart-donut/-sparkline modified; lane ③ Chart-combo added) and a **stale `canon.css`** (out of sync with tokens — pre-existing, not from me; `gen_theme_cascade.py` regenerated it, +377 lines, deterministic). The **only two build blockers now are both sibling-lane**, NOT Chart-bar:
1. **lane ③** `Chart-combo.meta.json` — 2 schema errors: `accessibility.relatedSC` required (missing) + `provenance.source` `"net-new-design"` not in the enum `['figma','code','both','gap-report','proforma-promotion']`.
2. **lane ②** `Chart-donut` `.seg` blast-radius unregistered.
With those two fixed, the build returns to green (Chart-bar contributes zero failures).

---

## Deferred (deliberate cut at the gauge — precise continuation)

### Chart-scatter → full Layer-2 (brief item 5) — NOT rebuilt
The existing `Chart-scatter.reference.html` (Layer-1, 286 lines, DataViz gate PASS 0/0) is **safe in place** — nothing broken, just not yet Layer-2. Continuation spec (a fresh window, ~half a Fable budget):
- Port the same Layer-2 as Chart-bar/line (popover · fit · table-popover · CSV · title · H-stack head). Two quantitative axes → both-axis gridlines + numeric ticks ride the fit (`data-fx` on vertical gridlines/x-ticks; points are `<g class="dv-marker" data-fx data-x0>` translated by fit like the line's markers).
- **Enlarged marker family** (exemplar canon, SUPERSEDES kit): circle r**5.5** · square **11** · diamond **±6.5**; page-stroke 2.5.
- Segment letters (A/B/C) stay; add `.dv-stage` right-padding if the end letters clip (line precedent).
- Legend-as-filter for the 3 segments (shaped+lettered swatches, hollow off-state).
- Register as a dataviz member with the per-capability split above (scatter HAS `data-fxs`? no — points are `<g>`, not polylines; so scatter is like bar for the polyline hook — it needs the split too, and its own point-translate fit already matches `dv-behaviour`'s `g[data-fx]` branch).

### B4 — proforma scatter fit wiring (brief item 6) — NOT done
The "one permitted proforma edit" (`_proforma/DataViz-interactive.html` scatter section only: add `data-fx`/`data-x0` to the scatter points + `data-fx`/`data-fx2` to its gridlines so the gold-standard file meets its own fit bar). Bounded, independent of the snippet. Deferred with the scatter snippet.

### Menu item 8 — BRUSH / RANGE-SELECT (brief item 7: SPEC ONLY — the ruling requires it designed before build). **Spec below; do NOT build.**

---

## ★ BRUSH / RANGE-SELECT — keyboard design spec (menu 8, scatter + line)

**Intent.** Drag a region on the plot to select a subset — read an aggregate, filter, or (later) zoom. Dave ruled all 11 menu items IN (2026-07-23); item 8 "needs its keyboard design before build."

**Pointer model.** Pointer-down on the plot canvas begins a selection rectangle (scatter: 2D box; line: a 1D x-range band spanning full height). Drag sizes it; release commits. Inside = emphasised; outside = `.dv-quiet` (data-layer dim only — never controls). A small readout (`role="status"`, `.t-cm-chart-value`) shows "n points · X a–b · Y c–d". A "Clear selection" button restores.

**Keyboard model (the required design).**
- The plot gains ONE focusable overlay: `<g class="dv-brush" role="application" tabindex="0" aria-label="Range select. Arrow keys move the active edge; Shift with arrows resizes; Tab switches edge; Enter commits; Escape clears.">`. `role="application"` is deliberate (arrow keys are the tool's own, not page scroll) and scoped to this node only.
- Two anchors: **start** and **end** (active one indicated visually + `aria-current`). **Arrow keys** move the active anchor one **step** — step = one data increment on the categorical/dominant axis, a fixed px (e.g. 8) on the free axis. **Shift+Arrow** resizes (moves the active edge, other edge fixed). **Tab** (while the overlay holds focus, trapped) switches the active anchor; **Enter** commits the selection; **Escape** clears and returns the overlay to the neutral state.
- **`aria-live="polite"`** region announces bounds + count on every change ("Selecting 6 points, X 40 to 60, Y 20 to 45") — debounced to key-up so rapid arrowing doesn't flood.
- **Reduced-motion**: no animated sweep; selection rect appears/updates instantly.
- **Progressive enhancement** (ADR-0015): no-JS = no brush overlay; the baked chart + table are the fallback. **DEF-003**: geometry only — no scale-physics, no `transform:scale`.
- **Perf** (ADR-0015 contract): the brush reuses the ONE rAF-debounced frame; pointer math on `pointermove` is delegated (document-level), no per-point listeners.

**OPEN for Dave (design rulings — spec only, do not settle):**
1. Default action on commit — **FILTER** (hide outside), **HIGHLIGHT** (dim outside, keep visible), or **READ-ONLY** (just the aggregate readout)? Recommend HIGHLIGHT + readout (least destructive; filter is a separate explicit toggle).
2. **Zoom-on-commit**? (rescale axes to the selection) — powerful but couples to the fit system's fixed domain; recommend deferring to the planned Apollo edit-mode.
3. Line 1D-band vs scatter 2D-box — confirm both, or line gets a simpler x-range only.

---

## Open Qs / for the conductor
- `_type-bindings.json` reserialised indent=2 — confirm canonical format.
- The 50 Chart-bar gridline advisories are permanent-by-design (DV-D07); if the report noise bothers, a decorative-class suppression is a conductor call (same standing item as the line's 16).
- Stacked-column legend FILTER hiding a middle series leaves a visual gap in the stack (segments don't reflow) — receipted as a known reference caveat; a reflow-on-filter is a design decision, not built.
- Sort-view `<tbody data-dv-view>` mirroring: verified the `setView` selector (`[data-dv-view~="name"]`) matches `<tbody>` groups — behaviour toggles them with the bars. (Confirm on render.)
