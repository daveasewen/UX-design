# Focus indicators (keyboard focus visibility)

> **Status: CANON — signed off by Dave 2026-06-20.** The HSBC Common Toolkit Figma library carries **no canonical focus primitive** — searched 2026-06-19 (`focus`, `outline`, `ring`): no variable exists, and the closest matches (`form/border/active`, `border/strong`, the `bottom stroke/active` effect) are general-purpose, not a focus ring. In the React/CSS layer focus is handled with `:focus-visible` outlines rather than a token. This document defines a system-wide standard so that generators stop **inventing** a focus ring per component (the Tabs fitness test, 2026-06-19, found Route B had no focus design at all and Route A had to guess one). The ring colour, width, and offset below are now the agreed standard; revisit only if the design/accessibility team introduce a native Figma focus primitive.

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

## Technique — accessible without being clumsy

The default browser outline reads as clumsy. Use `:focus-visible` (so the indicator shows for keyboard/programmatic focus, not mouse clicks) and replace the default ring with a considered treatment — but **never** `outline: none` without a visible replacement. All three patterns below satisfy 2.4.7 / 2.4.11 / 2.4.13 when they keep **≥3:1 contrast** against what's immediately behind them and are **at least as thick as the element's own border emphasis**. Match the pattern to the component:

- **Text inputs → two-tone border / thickened stroke.** Use the field's own anatomy: on `:focus-visible`, thicken the bottom-stroke (or border) in the field's **own active colour** (`form/border/active`) — a coloured/blue ring is not required and is often busier. Keep it ≥3:1 and distinct from the error stroke. Example: `input:focus-visible { outline: none; box-shadow: inset 0 -3px 0 var(--form-border-active); }` (`focus/ring` may be used where a component has no strong border colour of its own.)
- **Links → underline / border shift.** A thick branded underline directly under the text: `a:focus-visible { outline: none; box-shadow: inset 0 -4px 0 var(--focus-ring); }`
- **Buttons & other controls → floating outline.** A ring just outside the perimeter, matching the control's corner radius: `button:focus-visible { outline: none; box-shadow: 0 0 0 3px var(--focus-ring); }` (or `outline: 2px solid var(--focus-ring); outline-offset: 2px`).

Whichever pattern, the indicator must enclose or sit adjacent to the element so it's unmissable, and must not be clipped by overflow/sticky containers (2.4.11).

## Per-component application

A component's meta expresses its focus intent in the `tokens` block (bind `focus/ring`) and, where the geometry differs from the default, in its `dimensions` block. Components must not redefine the colour, width, or offset locally — the point of the standard is one ring across the system.

## Provenance

- WCAG basis: `guidelines/digital-accessibility-standards.md`, `components/_ACCESSIBILITY-CONFORMANCE.md` (2.4.7, 2.4.11, 2.4.13).
- Origin: `knowledge/_FITNESS-TEST-tabs.md` fix #2 (2026-06-19).
- Confidence: `asserted` — signed off by Dave 2026-06-20 (was `review`; see `_CONFIDENCE.md`). The ring colour/width/offset are agreed canon; no native Figma primitive exists to supersede them.
