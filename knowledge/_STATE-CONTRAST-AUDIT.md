# State-contrast audit — rendered hover / pressed states (light + dark)

*Drives each interactive element's real hover/pressed states and measures computed foreground vs effective background. TEXT < 4.5 (large < 3.0) FAILS; svg ICONS < 3.0 WARN (many decorative). Disabled controls skipped (WCAG-exempt). Closes the declared-pairs blind spot (Dave, 2026-06-22).*

**FIRST FULL SWEEP — 2026-07-03, all 38 snippets** (render path revived in-sandbox: libXdamage user-space + skip-validate env, see `_ROBUSTNESS-PORTABILITY.md`; run in 13 batches — background jobs die-with-parent in this sandbox, single-call time cap).

**6 TEXT failure line(s) · 20 icon warn(s) · 26 interactive sections (12 snippets have no interactive elements).**

TRIAGE (2026-07-03):
- **Selection-controls — REAL (2 fails):** 'Accept terms & conditions' label 4.02:1 in light hover+pressed. Converges with copy-022 (same row needs 'terms and conditions' wording) → ONE component touch, Dave's eyes required (locked component).
- **View-options — MEASUREMENT ARTIFACT (4 fails, verified by screenshot):** light-hover renders black pill + white label, clearly legible; the gate's effective-background walk misses the absolutely-positioned sliding indicator (.ind) beneath the label. GATE BUG docketed: z-layer-aware background resolution needed; Tab-bar B (same mechanism) passed — verify why when fixing.
- Icon warns are the known judgment class (decorative marks, knockouts) — no action this pass.

## Account-card — ✅ clean

## Action-bar — ✅ clean

## Badge — ✅ clean

## Breadcrumbs — ✅ clean

## Button — ✅ clean

## Confirmation — ✅ clean

## Countdown-timer — ✅ clean

## Dropdown — ✅ clean

## Eyebrow — ✅ clean

## Hero — ✅ clean

## Input-fields — ✅ clean · 4 icon warn(s)
- 🟡 icon [light/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1:1 (need 3.0) (decorative)
- 🟡 icon [light/hover] 1.3:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1.3:1 (need 3.0) (decorative)

## List-items — ✅ clean

## Loading-indicator — ✅ clean

## Navigations — ✅ clean

## Notifications — ✅ clean

## Progress-tracker — ✅ clean

## Quick-actions — ✅ clean

## Search-field — ✅ clean

## Selection-controls — ❌ 2 TEXT fail(s) · 6 icon warn(s)
- ❌ TEXT [light/hover] 4.02:1 (need 4.5) — "Accept terms & conditions"
- ❌ TEXT [light/pressed] 4.02:1 (need 4.5) — "Accept terms & conditions"
- 🟡 icon [light/hover] 1:1 (need 3.0)
- 🟡 icon [light/pressed] 1.3:1 (need 3.0)
- 🟡 icon [light/hover] 1.3:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 2.26:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1:1 (need 3.0)
- 🟡 icon [dark/pressed] 1:1 (need 3.0) (decorative)

## Status-indicator — ✅ clean

## Summary — ✅ clean
- 🟡 icon [light/hover] 1.33:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1.33:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1:1 (need 3.0) (decorative)

## Table — ✅ clean

## Tabs — ✅ clean

## Tooltip — ✅ clean

## Video-player — ✅ clean · 2 icon warn(s)
- 🟡 icon [dark/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1:1 (need 3.0) (decorative)

## View-options — ❌ 4 TEXT fail(s) · 4 icon warn(s)
- ❌ TEXT [light/hover] 1.33:1 (need 4.5) — "List"
- ❌ TEXT [light/pressed] 1.33:1 (need 4.5) — "List"
- ❌ TEXT [dark/hover] 1:1 (need 4.5) — "List"
- ❌ TEXT [dark/pressed] 1:1 (need 4.5) — "List"
- 🟡 icon [light/hover] 1.33:1 (need 3.0) (decorative)
- 🟡 icon [light/pressed] 1.33:1 (need 3.0) (decorative)
- 🟡 icon [dark/hover] 1:1 (need 3.0) (decorative)
- 🟡 icon [dark/pressed] 1:1 (need 3.0) (decorative)
