# State-contrast audit — rendered hover / pressed states (light + dark)
*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**0 text failure(s) across 15 snippet(s).**

**8 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**

## Slider — ✅ clean

## Stat-card — ✅ clean

## Status-indicator — ✅ clean

## Stepper — ✅ clean

## Summary — ✅ clean

## Tab-bar — 4 icon warn(s) · ⬛ 3 UNMEASURABLE box(es)
- 🟡 icon [light/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.3:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.3:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — svg — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — svg.ic-fill — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — svg.ic-line — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Table — ⬛ 5 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — th "Account number" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th "Account" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th "Sort code" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th "Type" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).
- ⬛ UNMEASURABLE (declared hole) — th.num "Available balance" — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Tabs — ✅ clean

## Tags — ✅ clean

## Textarea — ✅ clean

## Time-picker — 2 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)

## Toast — ✅ clean

## Tooltip — ✅ clean

## Video-player — 2 icon warn(s)
- 🟡 icon [light/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)

## View-options — ✅ clean

---
**⬛ 8 DECLARED HOLE(s) — UNMEASURABLE, `s129-D3` (Dave, #129).** Each box above is not hit-testable — it has no on-screen geometry, or it opts out of hit testing (`pointer-events:none`), or something over it takes the hit — so the paint stack beneath it CANNOT BE OBSERVED. Every one is listed BY NAME with its measured reason. The pre-2026-08-07 ancestor-only walk still runs over them, so no failure is waived and no threshold moved; but an overlapping sibling would still be missed, and those readings may NOT be quoted as hit-stack measurements. ⛔ Dave ruled DECLARE, not REFUSE: refusing them would have turned ~60 measured records into nothing, and publishing the fallback number as if it were the real one is the invented-number class this gate exists to kill. The count above is RE-READ off this artefact and asserted equal to the number of ⬛ lines on every write — a hole that goes quiet is a failed write, not a clean run.
