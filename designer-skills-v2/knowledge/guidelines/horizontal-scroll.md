---
title: Horizontal scroll design (carousels)
source: HSBC Common Toolkit (MCP) — "Gaps and edits" branch, node 2298:160129
type: pattern-guidance
captured: 2026-06-17
note: A UX/accessibility PATTERN page (not a single component, no bound tokens). Covers accessible horizontal-scroll / carousel patterns with three worked examples. get_metadata failed (HTTP2) on this node; captured via screenshot OCR.
---

# Horizontal scroll design

Horizontal scroll can be an effective way to showcase a large amount of content while keeping a clean, organised interface — but it must be implemented thoughtfully. Designing to the accessibility standards ensures all users, regardless of ability, have a comparable experience and can navigate the horizontal scroll effectively. This includes (but is not limited to) **tab sequence, voice navigation, keyboard navigation, and screen-reader compatibility**.

> These statements aid accessible design; they inform the accessibility requirements rather than constrain the design.

## Core principle (applies to all horizontal-scroll patterns)
- **Visually, users must be able to navigate to the next and previous items** in the horizontal scroll component (not swipe-only — provide visible controls / keyboard + screen-reader access).
- **Users must be able to know which item they are currently on.**
- **All calls to action must have sufficient colour contrast.**

## 1. Hub Navigation
- For hub navigation you **don't need to show the total item count**.
- Users must still know which item they're on.
- **Option 1 — entry point ("limited links visible"):** highlight the most important page links outside the menu. Limit to **three or four** depending on label length. If developers code adaptive overflow (by screen size, label length, or font size), more links can be shown.
- **Option 1 — open ("full takeover"):** a full takeover for additional links/features; include **all** links ideally, or the four main ones if necessary.

## 2. Hero content cards
- The **"View all" button is not applicable** for cards — regardless of how many cards a person has, put them in the **carousel**. This component won't experience overflow.
- **Option 1A — arrows + pips/pagination (forward/backward carousel):** swipe with a thumb or navigate with arrows. Left arrow disabled on the first slide, right arrow disabled on the last; navigation is left/right only. No "View all" needed given the page's dynamic nature.
- **Option 1B — arrows + pips/pagination (circular carousel):** swipe or use arrows; arrows are **not** disabled — the carousel loops circularly.

## 3. Credit card carousel
- Cards associated with a person's accounts; again, **"View all" is not applicable** — add them to the carousel.
- All CTAs need sufficient colour contrast.
- **With and without arrow navigation:**
  - **Option 1 (primary) — pagination with arrows:** pagination must **always** include arrows for navigation.
  - **Option 2 — pips alone (no arrows):** each pip's **target area ≥ 44×44px**; sufficient colour contrast between pip and background; **selected vs deselected distinguished by more than colour** (also shape/size).
- **One-item change:** pressing the right arrow shifts the carousel by **one item at a time** (one enters on the right as one leaves on the left). **Recommendation: no more than 5 content cards in a carousel.**
- A "do not use pagination …" caveat appears on this section alongside the pagination options — REVIEW exact wording/scope (possibly "don't use pips-only pagination for this case").
