# Focus indicators (keyboard focus visibility)

> **Status: INFERRED standard, tagged `review`.** The HSBC Common Toolkit Figma library carries **no canonical focus primitive** — searched 2026-06-19 (`focus`, `outline`, `ring`): no variable exists, and the closest matches (`form/border/active`, `border/strong`, the `bottom stroke/active` effect) are general-purpose, not a focus ring. In the React/CSS layer focus is handled with `:focus-visible` outlines rather than a token. This document defines a system-wide standard so that generators stop **inventing** a focus ring per component (the Tabs fitness test, 2026-06-19, found Route B had no focus design at all and Route A had to guess one). Confirm the values with the design/accessibility team before treating as canon.

## Why this exists

Every interactive component in the toolkit is graded against **WCAG 2.2 AA 2.4.7 Focus Visible**, **2.4.11 Focus Not Obscured (Minimum)**, and **2.4.13 Focus Appearance**, yet the knowledge base defined no focus colour, width, or offset. A focus indicator is not optional craft — it is a conformance obligation. This gap is **systemic: it affects all 32 components**, not just Tabs.

## The standard

**Tokens**

- **Ring colour** — `focus/ring` (`tokens/semantic-colour.json`), mode-aware: light `#305A85` (`color/blue/600`), dark `#4587A7` (`color/blue/400`). Grounded in the system's existing information-blue ramp rather than an invented hex.
- **Ring width** — `layout/focus/ring-width` = `2px` (equals `border-width/medium`).
- **Ring offset** — `layout/focus/ring-offset` = `2px`.

**Rules**

- Render the ring with `:focus-visible` (keyboard/programmatic focus), **not** `:focus` — do not show the ring on mouse click.
- The ring is a **2px solid outline** in `focus/ring`, offset `2px` from the element edge so it stays clear of the component fill.
- **Never** remove the outline (`outline: none` / `outline: 0`) without rendering an equally visible replacement. This is the single most common 2.4.7 failure.
- The ring must clear **3:1 non-text contrast (1.4.11)** against *both* the component surface and any adjacent colour. Verified for this token: **light 7.17:1** on `#FFFFFF`, **dark 4.24:1** on `#1D1D1D` — both pass.
- Focus order and the ring must not be **clipped or hidden** by overflow containers, sticky headers, or scroll regions (2.4.11). For components inside scrolling overflow (e.g. Tabs overflow menu), ensure the focused item scrolls into view with its ring intact.
- The ring is **independent of selection/active state colour**. Selected-but-not-focused and focused-but-not-selected must be visually distinguishable (do not reuse the brand-red selected indicator as the focus ring).

## Per-component application

A component's meta expresses its focus intent in the `tokens` block (bind `focus/ring`) and, where the geometry differs from the default, in its `dimensions` block. Components must not redefine the colour, width, or offset locally — the point of the standard is one ring across the system.

## Provenance

- WCAG basis: `guidelines/digital-accessibility-standards.md`, `components/_ACCESSIBILITY-CONFORMANCE.md` (2.4.7, 2.4.11, 2.4.13).
- Origin: `knowledge/_FITNESS-TEST-tabs.md` fix #2 (2026-06-19).
- Confidence: `review` — see `_CONFIDENCE.md`. Pending design-team confirmation of the ring colour/width/offset.
