# A11y gate — _validate_a11y.py

**67 snippet(s)** · **0 failure(s)** · **13 warning(s)**

Gating: reduced-motion (2.3.3) · target size <24 floor (2.5.8, aid-009 ruling 2026-07-03). Reported: target size 24–43 vs the 44×44 HSBC default (aid-009).

Library bar (aqa-003, ruled 2026-07-03): the canon is LIBRARY-GRADE — guideline and recommendation tiers bind it, not just standards.

## Alert
- 🟡 warn — `.alert .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Banner
- 🟡 warn — `.banner .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Data-grid
- 🟡 warn — `.fchip .x` is 24×24px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Drawer
- 🟡 warn — `.sheet .close` is 36×36px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Headers
- 🟡 warn — `.content-header button` is 40×40px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Modals
- 🟡 warn — `.dialog .close` is 36×36px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Popover
- 🟡 warn — `.pop .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Reorder
- 🟡 warn — `.handle` is 32×32px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out
- 🟡 warn — `.moves button` is 30×30px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Search-field
- 🟡 warn — `.clear` is 24×24px (<44 HSBC default, aid-009) — enlarge, expand hit area, or claim a 2.5.8 exception out

## Selection-controls
- 🟡 warn — `.chip .x` is 18×18px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Toast
- 🟡 warn — `.toast .x` is 24×24px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

## Tooltip
- 🟡 warn — `.trigger` is 22×22px — EXEMPT via a ::before hit-area expander, NOT MEASURED (aid-009, ds-015). Static CSS cannot size the expander; the render-axis hit-area gate owes this one.

