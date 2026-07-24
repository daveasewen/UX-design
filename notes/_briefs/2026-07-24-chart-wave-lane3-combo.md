# Wave lane ③ — Chart-combo: bar + line overlay, dual axis (net-new)

*Cut 2026-07-24 by the conductor. Model/effort per the ratified divvy: **Fable · high** — this is
the wave's one real design problem. Role from Dave's opener. **Read first, in order:**
`GOOD-MORNING.md` → `snippets/Chart-line.reference.html` + `snippets/Chart-bar.reference.html`
(you are composing their languages) → `notes/_receipts/2026-07-23-chart-line-exemplar-worker.md`
(SIX refinements + state model = CANON) → `_DATAVIZ-DECISIONS.md` DV-D05/07/08 + dv-bar-009 +
dv-line-011 → the 2026-07-23 revisit brief §combo.*

## The ask (Dave, verbatim from the programme): "we've completely missed the bar with line overlay"

Design + build `snippets/Chart-combo.reference.html` — bars on the PRIMARY axis + a line on a
SECONDARY axis (reference data shape: monthly volume bars + a running-average or margin-% line).
**Q2 (new snippet vs Chart-bar variant) is technically Dave's — the standing recommendation is a
new snippet; build it that way and flag loudly in the receipt so his ruling can still fold it.**

## Design decisions you own (each receipted with rationale + alternatives)

1. **Secondary-axis grammar** — right-edge ticks in `data/axis` (DV-D07 role); how the two scales
   are labelled apart (unit suffix in the tick text vs axis titles) — propose, pick, receipt.
2. **Series assignment** — bars vs line from `data/series/*` with the ≥3:1 floor BOTH modes;
   the line must read against bars it CROSSES (test at intersections, not just page ground).
3. **Zero-baseline** — dv-bar-009 binds the BAR axis; the line's secondary axis may float —
   state the posture explicitly (this becomes the combo precedent).
4. **dv-line-011** straight segments; line markers = the ENLARGED family (r5.5, page-stroke 2.5);
   line-end letter key if multi-line.
5. **Table spine** — one `<table>` carrying both series with unit columns; parity scripted.

## Layer-2 (all exemplar canon)

Popover (tips name the unit: "Mar: 420 units" / "Mar: 4.2%") · fit · table-view popover · optional
title · H-stack head · legend filter/isolate/highlight (two entries, shaped swatches, hollow
off-state) · seg-view + per-view additive overlays IF you add a scale view (optional — a
monthly⇄cumulative view is a natural fit; per-view overlay copies per the exemplar state model).

## Fences (three lanes live)

**Yours:** `snippets/Chart-combo.reference.html` (NEW) · `components/chart-combo.meta.json` (NEW) ·
receipt `notes/_receipts/2026-07-24-wave-lane3-combo.md`.
**NOT yours:** `component-types.json` (membership via receipt) · `dv-behaviour.js` (hook needs →
receipt) · `_build_all` · `MIGRATED_SNIPPETS`/`CATEGORIES` (registration = conductor serial —
NOTE: your snippet is UNREGISTERED until absorb, so run the DataViz gate by import as worker-D did,
and say so in the receipt) · spine · proforma · git.

## Bar checklist

As the other lanes, plus: intersection-contrast proof (line over bar fills, both modes) ·
dual-axis tick parity (both scales recompute correctly under fit) · render-verify ≥2 widths +
dark + HC + filtered + JS-off · controls never dim-only (constraint OPEN; exemplar recipe verbatim).
