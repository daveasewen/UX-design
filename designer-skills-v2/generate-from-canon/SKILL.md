---
name: generate-from-canon
description: Build a screen or component using only the design system — its reviewed components and design tokens — never inventing new ones. Flags anything the system is missing instead of improvising. Use when you want on-brand, accessible UI drafted by construction. Outputs React (preferred) or plain HTML/CSS.
---

# Generate from canon

Draft UI **strictly from the design system**. The one job here is to stop the
common failure of AI design work — quietly *inventing* components, variants or
colours. If it isn't in the system, this skill flags it rather than making it up.

This is the **strict** mode: deliberately faithful, not a creativity play. When
the system is genuinely missing something you need, use `draft-a-new-pattern`.

## Rules (non-negotiable)
1. Use **only** components and variants defined in `knowledge/components/` (one
   `*.meta.json` per component). Missing what you need? Add it to a **Gaps** list
   and stop — never improvise a component or variant.
2. Bind every visual value to a **token by intent** (from `knowledge/tokens/` /
   `knowledge/canon/canon.css`) — never a raw hex or px.
3. **Type via composites:** component text takes a composite class from
   `knowledge/canon/type.css` (`.t-cm-*` component / `.t-ed-*` editorial) — never
   raw font-size/weight/line-height values.
4. **Build against Apollo Mono, the baseline theme** (`knowledge/tokens/themes/`):
   monochrome throughout — colour appears **only** in RAG status + data-vis; the
   only red is `#B92F1E` (status, never action/nav); square corners; sentence case.
5. Honour each component's `antiPatterns` and `relationships`.
6. Cover the relevant **states**: default / hover / pressed / focus / disabled /
   loading / error / empty.
7. **Icons are real assets only** — from `knowledge/assets/icons/` (see the
   manifest); never draw or invent a glyph.
8. Carry **provenance** — note which canon component and tokens each part came from.

## Procedure
1. Read the request. Find the canon components each screen needs — look in
   `knowledge/components/*.meta.json` for the contract, `knowledge/canon/canon.css`
   + `knowledge/canon/type.css` and `knowledge/snippets/` for the reviewed
   markup/CSS.
2. Compose the screen from those pieces; bind tokens; set the states.
3. Anything the system can't supply → list under **Gaps**, don't invent.
4. Produce the output: **React** (wire the real components) preferred, or plain
   **HTML/CSS** using the canon classes/tokens.

## Output
- The code (React or HTML/CSS).
- A short **"used / missing"** note: which canon components + tokens you drew on,
  and any Gaps the system couldn't cover.

> If you have Figma Dev Mode + Code Connect available, pull components/variables
> live; otherwise the `knowledge/` files are the source of truth.

*Experimental — feedback on what's missing is the point.*
