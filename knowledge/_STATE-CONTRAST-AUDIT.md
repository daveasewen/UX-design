# State-contrast audit — rendered hover / pressed states (light + dark)
*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**14 text failure(s) across 75 snippet(s).**

**14 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**

## Accordion — ✅ clean

## Account-card — ✅ clean

## Account-selector — ✅ clean

## Action-bar — ✅ clean

## Alert — ⬛ 1 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — a "Review payment details" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Amount-display — ✅ clean

## Amount-input — ✅ clean

## Avatar — ✅ clean

## Badge — ✅ clean

## Banner — ❌ 4 TEXT fail(s) · ⬛ 1 UNMEASURABLE box(es)
- ❌ TEXT [light/pressed] 4.09:1 (need 4.5) — "Confirm it was me"
- ❌ TEXT [light/pressed] 4.09:1 (need 4.5) — "Secure my account"
- ❌ TEXT [dark/pressed] 4.09:1 (need 4.5) — "Confirm it was me"
- ❌ TEXT [dark/pressed] 4.09:1 (need 4.5) — "Secure my account"
- ⬛ UNMEASURABLE (declared hole) — a "See affected services" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Breadcrumbs — ✅ clean

## Button — ✅ clean

## Cards — ✅ clean

## Chart-bar — ✅ clean

## Chart-boxplot — ✅ clean

## Chart-bullet — ✅ clean

## Chart-butterfly-h — ✅ clean

## Chart-butterfly-v — ✅ clean

## Chart-candlestick — ✅ clean

## Chart-combo — ✅ clean

## Chart-donut — ✅ clean

## Chart-histogram — ✅ clean

## Chart-line — ✅ clean

## Chart-pie — ✅ clean

## Chart-scatter — ✅ clean

## Chart-sparkline — ✅ clean

## Chart-stacked-area — ✅ clean

## Confirmation — ✅ clean

## Countdown-timer — ✅ clean

## Data-grid — 2 icon warn(s) · ⬛ 1 UNMEASURABLE box(es)
- 🟡 icon [dark/hover] 1.27:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.27:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — svg — no on-screen box at measurement time (zero-size, or entirely outside the viewport). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Date-picker — 4 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)

## Date-range-picker — 4 icon warn(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)

## Divider — ✅ clean

## Drawer — ✅ clean

## Dropdown — ✅ clean

## Empty-state — ✅ clean

## Eyebrow — ✅ clean

## File-upload — 2 icon warn(s)
- 🟡 icon [dark/hover] 1.11:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.11:1 (need 3.0) (decorative)

## Form-layout — 2 icon warn(s) · ⬛ 1 UNMEASURABLE box(es)
- 🟡 icon [dark/hover] 1.11:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.11:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — span#f-name-tip.tipbody "Match the name on the re" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Headers — ✅ clean

## Hero — ✅ clean

## Icon-button — ⬛ 1 UNMEASURABLE box(es)
- ⬛ UNMEASURABLE (declared hole) — svg — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Input-fields — 4 icon warn(s) · ⬛ 1 UNMEASURABLE box(es)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)
- ⬛ UNMEASURABLE (declared hole) — span#b1tip.tip "Enter the amount you wan" — not present in the hit stack at its own sample point (pointer-events:none, or an overlay above it takes the hit). The paint stack under it cannot be observed, so the pre-2026-08-07 ancestor-only walk ran instead: any ratio reported over this box is that weaker measurement, NOT a hit-stack one. Nothing is invented and nothing is waived (s129-D3).

## Links — ✅ clean

## List-items — ✅ clean

## Loading-indicator — ✅ clean

## Modal-lightbox — ✅ clean

## Modals — ✅ clean

## Navigations — ✅ clean

## Notifications — ✅ clean

## Pagination — ✅ clean

## Popover — ✅ clean

## Progress-tracker — ✅ clean

## Quick-actions — ✅ clean

## Reorder — ✅ clean

## Search-field — ✅ clean

## Secure-entry — ✅ clean

## Segmented-control — ✅ clean

## Selection-controls — ❌ 8 TEXT fail(s) · 6 icon warn(s)
- ❌ TEXT [light/pressed] 3.95:1 (need 4.5) — "Savings"
- ❌ TEXT [light/pressed] 3.95:1 (need 4.5) — "Credit card"
- ❌ TEXT [light/pressed] 3.95:1 (need 4.5) — "90 days"
- ❌ TEXT [light/pressed] 3.95:1 (need 4.5) — "6 months"
- ❌ TEXT [light/pressed] 3.95:1 (need 4.5) — "12 months"
- ❌ TEXT [light/pressed] 3.95:1 (need 4.5) — "✕"
- ❌ TEXT [dark/hover] 3.66:1 (need 4.5) — "Accept terms & conditions"
- ❌ TEXT [dark/pressed] 3.66:1 (need 4.5) — "Accept terms & conditions"
- 🟡 icon [light/hover] 1:1 (need 3.0)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 2.3:1 (need 3.0) (decorative)

## Skeleton-loader — ✅ clean

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

## Tabs — ❌ 2 TEXT fail(s)
- ❌ TEXT [dark/hover] 1:1 (need 4.5) — "2"
- ❌ TEXT [dark/pressed] 1:1 (need 4.5) — "2"

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
**⬛ 14 DECLARED HOLE(s) — UNMEASURABLE, `s129-D3` (Dave, #129).** Each box above is not hit-testable — it has no on-screen geometry, or it opts out of hit testing (`pointer-events:none`), or something over it takes the hit — so the paint stack beneath it CANNOT BE OBSERVED. Every one is listed BY NAME with its measured reason. The pre-2026-08-07 ancestor-only walk still runs over them, so no failure is waived and no threshold moved; but an overlapping sibling would still be missed, and those readings may NOT be quoted as hit-stack measurements. ⛔ Dave ruled DECLARE, not REFUSE: refusing them would have turned ~60 measured records into nothing, and publishing the fallback number as if it were the real one is the invented-number class this gate exists to kill. The count above is RE-READ off this artefact and asserted equal to the number of ⬛ lines on every write — a hole that goes quiet is a failed write, not a clean run.
