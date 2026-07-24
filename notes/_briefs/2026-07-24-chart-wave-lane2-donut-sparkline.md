# Wave lane ② — Chart-donut + Chart-sparkline (chart-revisit fan-out)

*Cut 2026-07-24 by the conductor. Model/effort per the ratified divvy: **Fable · medium**. Role from
Dave's opener. **Read first, in order:** `GOOD-MORNING.md` → `snippets/Chart-line.reference.html`
(THE pattern) → `notes/_receipts/2026-07-23-chart-line-exemplar-worker.md` (SIX refinements + state
model + a11y constraint = CANON) → `_DATAVIZ-DECISIONS.md` DV-D05/07/08 · ADR-0015 · type26-013.*

## Scope

1. **Chart-donut → full Layer-2:** popover on segments (`data-tip`, focusable per the exemplar's
   marker pattern) · table-view popover · optional title · H-stack head · legend-as-filter/isolate/
   highlight with shaped+lettered swatches + AA hollow off-state. **Radial sweep entry motion
   RETURNS** — it is data-driven geometry, explicitly allowed under ADR-0015/DEF-003; port the
   proforma's rAF sweep + `data-seq` label sequencing into a dv-behaviour hook (RECEIPT the hook
   need — the source edit is the conductor's serial).
2. **Menu item 5 (ruled in): value ⇄ % toggle** — baked variant groups (`data-dv-view` idiom);
   centre total + direct labels + table all mirror the active mode.
3. **Variants:** spider + direct both stay (D-Q2 default = STILL OPEN, don't pick); letters-on-
   segments stays HELD (type26-013 white-type — do not resurrect).
4. **Chart-sparkline → compact Layer-2:** popover + fit; NO legend machinery (single series); the
   inline-44px KPI specimen stays passive (Stat-card seam untouched, B-Q6 open). JS-off = baked
   sparkline exactly as now.
5. **DV-D08 rebind both files:** labels→`t-cm-chart-label` · values→`t-cm-chart-value` · any keys→
   `t-cm-chart-key`; centre total stays `t-cm-figure-3` (24/500 — above the ladder, per the
   exemplar's title precedent).

## Watch: per-capability behaviour split

The registry hook contract is currently the LINE set. If donut/sparkline need materially different
hook shapes (sweep, arc popover anchoring), do NOT force-fit — receipt the observed need and the
proposed split; the conductor restructures the registry serially (accretion from OBSERVED need,
ADR-0013 ruling 3).

## Fences (three lanes live)

**Yours:** `snippets/Chart-donut.reference.html` · `snippets/Chart-sparkline.reference.html` ·
their metas · receipt `notes/_receipts/2026-07-24-wave-lane2-donut-sparkline.md`.
**NOT yours:** `component-types.json` · `dv-behaviour.js` (needs → receipt) · `_build_all` ·
registries · spine · proforma · git.

## Bar checklist

As lane ①: serial builds · gate 0 blocking · parity scripts (segment arcs↔table esp. after the %
toggle) · render-verify ≥2 widths + dark + HC + filtered + JS-off · census/radius/coverage green ·
controls never dim-only (exemplar recipe verbatim; constraint OPEN pending Dave's adviser).
