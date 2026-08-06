# A11y gate — _validate_a11y.py

**75 snippet(s)** · **6 failure(s)** · **33 warning(s)**

Gating: reduced-motion (2.3.3) · target size <24 floor (2.5.8, aid-009 ruling 2026-07-03). Reported: target size 24–43 vs the 44×44 HSBC default (aid-009).

Library bar (aqa-003, ruled 2026-07-03): the canon is LIBRARY-GRADE — guideline and recommendation tiers bind it, not just standards.

## Account-selector
- 🔴 FAIL — `.as-trigger .chev` is 16×16px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)

## Alert
- 🟡 warn — `.alert .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Avatar
- 🟡 warn — `.avatar.sm` is 32×32px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Banner
- 🟡 warn — `.banner .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Cards
- 🔴 FAIL — `.card.opt .radio` is 22×22px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)

## Chart-bar
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-butterfly-h
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-butterfly-v
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-combo
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-donut
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-line
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.
- 🟡 warn — `.dv-leg-sw.sw-diamond` is 8×8px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-pie
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-scatter
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Chart-stacked-area
- 🟡 warn — `.dv-leg-sw` is 12×12px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Data-grid
- 🔴 FAIL — `.sort .ic` is 16×16px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)
- 🟡 warn — `.dgs-clear` is 24×24px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out
- 🟡 warn — `.fchip .x` is 24×24px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Date-picker
- 🟡 warn — `.dp-box .tail-btn` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Date-range-picker
- 🟡 warn — `.dr-box .tail-btn` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Drawer
- 🟡 warn — `.sheet .close` is 36×36px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Dropdown
- 🔴 FAIL — `.opt .tick` is 16×16px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)

## File-upload
- 🔴 FAIL — `.fu-remove .icn` is 14×14px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)
- 🟡 warn — `.fu-remove` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Form-layout
- 🟡 warn — `.fl-tip` is 18×18px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Headers
- 🟡 warn — `.content-header button` is 40×40px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Input-fields
- 🟡 warn — `.help-btn` is 18×18px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.
- 🟡 warn — `.box .tail-btn` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Modals
- 🟡 warn — `.dialog .close` is 36×36px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Popover
- 🟡 warn — `.pop .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Reorder
- 🟡 warn — `.handle` is 32×32px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out
- 🟡 warn — `.moves button` is 30×30px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Search-field
- 🟡 warn — `.clear` is 24×24px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Secure-entry
- 🟡 warn — `.se-cell` is 40×48px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Selection-controls
- 🟡 warn — `.chip .x` is 18×18px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Time-picker
- 🔴 FAIL — `.tp-opt .tick` is 16×16px (<24 floor, 2.5.8) — add a ::before hit-area expander or enlarge (aid-009)
- 🟡 warn — `.tp-box .tail-btn` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Toast
- 🟡 warn — `.toast .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Tooltip
- 🟡 warn — `.trigger` is 22×22px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

