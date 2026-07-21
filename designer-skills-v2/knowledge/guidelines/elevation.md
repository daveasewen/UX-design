---
title: Elevation
source: HSBC Common Toolkit (MCP) — "Gaps and edits" branch, Foundations › Elevation page (node 873:34991)
type: foundation-guidance
captured: 2026-06-17
related_tokens: elevation.json (decorative blur 8 / functional blur 16; X/Y/spread per scale)
external_ref: create.hsbc/Guidelines/Foundations/Elevation.html
note: No new tokens on this page — values are in elevation.json. Dark-mode elevation reverses (higher levels get LIGHTER) — see dark-mode.md.
---

# Elevation

Elevation is a visual indication of depth or distance. It's applied when elements or patterns sit on top of one another. To show different levels we use **overlays and shadows**.

Elevation orientates and focuses the user. It's applied **consistently** across each element/pattern (e.g. all snackbars share one elevation, all partial modals share another).

## Types
Two elevation types (token values in `elevation.json`):
- **Decorative** — shadow blur `8`.
- **Functional** — shadow blur `16`.
(Both: X/Y/spread per scale. Don't use both types at once on the same element — see Usage.)

## Usage
- ✅ **Do** use shadows or overlays to focus user attention on higher levels of content.
- ❌ **Don't** display both types of elevation at the same time on a specific element or pattern.
- ✅ **Do** show elevation when the element/pattern sits above level 0 (for example, browser tooltips).
- ❌ **Don't** use shadows (inner or outer) for purely aesthetic decoration.

(The page includes two further do/don't examples not transcribed here; re-pull node 873:34991 → 46029:157227 / 46029:157363 if needed.)

## Behaviour
Elevation is shown on a system of **levels**, with specific patterns assigned to specific levels (level 0 = base content; higher levels = overlays/modals/tooltips etc.).

Elevation can be **triggered**:
- **on appearance** — when an element or pattern on a higher level appears on screen;
- **on scroll** — when level 0 is scrolled underneath elements/patterns.

Footnotes from the levels table:
- *\* Elements/patterns contained within these do not display further elevation.*
- *\*\* Conditional — if a page has just loaded with no scrollable content, no shadow is displayed; if the page is scrollable, a shadow appears.*

## Dark mode
The shadow/overlay model is less effective on dark backgrounds. In dark mode the effect **reverses**: indicate higher levels by making the surface **lighter**, not darker. See `dark-mode.md` (Elevation / Lighter background surfaces).
