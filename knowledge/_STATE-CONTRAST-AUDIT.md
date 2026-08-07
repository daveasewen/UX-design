# State-contrast audit — rendered hover / pressed states (light + dark)
*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**14 text failure(s) across 75 snippet(s).**

## Accordion — ✅ clean

## Account-card — ✅ clean

## Account-selector — ✅ clean

## Action-bar — ✅ clean

## Alert — ⚠ 2 ancestor-fallback background(s)
- ⚠ ancestor-fallback background (not hit-testable) — a "Review payment details"
- ⚠ ancestor-fallback background (not hit-testable) — a "Update contact details"

## Amount-display — ✅ clean

## Amount-input — ✅ clean

## Avatar — ✅ clean

## Badge — ✅ clean

## Banner — ❌ 4 TEXT fail(s) · ⚠ 1 ancestor-fallback background(s)
- ❌ TEXT [light/pressed] 4.09:1 (need 4.5) — "Confirm it was me"
- ❌ TEXT [light/pressed] 4.09:1 (need 4.5) — "Secure my account"
- ❌ TEXT [dark/pressed] 4.09:1 (need 4.5) — "Confirm it was me"
- ❌ TEXT [dark/pressed] 4.09:1 (need 4.5) — "Secure my account"
- ⚠ ancestor-fallback background (not hit-testable) — a "See affected services"

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

## Data-grid — 2 icon warn(s) · ⚠ 1 ancestor-fallback background(s)
- 🟡 icon [dark/hover] 1.27:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.27:1 (need 3.0) (decorative)
- ⚠ ancestor-fallback background (not hit-testable) — svg

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

## Form-layout — 2 icon warn(s) · ⚠ 1 ancestor-fallback background(s)
- 🟡 icon [dark/hover] 1.11:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.11:1 (need 3.0) (decorative)
- ⚠ ancestor-fallback background (not hit-testable) — span#f-name-tip.tipbody "Match the name on the re"

## Headers — ✅ clean

## Hero — ✅ clean

## Icon-button — ⚠ 1 ancestor-fallback background(s)
- ⚠ ancestor-fallback background (not hit-testable) — svg

## Input-fields — 4 icon warn(s) · ⚠ 1 ancestor-fallback background(s)
- 🟡 icon [dark/hover] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.21:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.34:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.34:1 (need 3.0) (decorative)
- ⚠ ancestor-fallback background (not hit-testable) — span#b1tip.tip "Enter the amount you wan"

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

## Tab-bar — 4 icon warn(s) · ⚠ 3 ancestor-fallback background(s)
- 🟡 icon [light/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1.3:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1.3:1 (need 3.0) (decorative)
- ⚠ ancestor-fallback background (not hit-testable) — svg
- ⚠ ancestor-fallback background (not hit-testable) — svg.ic-fill
- ⚠ ancestor-fallback background (not hit-testable) — svg.ic-line

## Table — ⚠ 5 ancestor-fallback background(s)
- ⚠ ancestor-fallback background (not hit-testable) — th "Account number"
- ⚠ ancestor-fallback background (not hit-testable) — th "Account"
- ⚠ ancestor-fallback background (not hit-testable) — th "Sort code"
- ⚠ ancestor-fallback background (not hit-testable) — th "Type"
- ⚠ ancestor-fallback background (not hit-testable) — th.num "Available balance"

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
**⚠ 15 background(s) took the ANCESTOR-WALK FALLBACK.** Their box is not hit-testable (`pointer-events:none`, or entirely off-screen at measurement time), so the paint stack under it cannot be observed and the pre-2026-08-07 ancestor-only walk ran instead. Those measurements are as good as they always were — and no better: an overlapping sibling would still be missed. Provenance, not a verdict.
