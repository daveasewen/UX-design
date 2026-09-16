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
1. **Seed — ask the graph, do not read the library** (`s277-D10`, `s278-D1`). Run the
   reader once and work from the slice it returns:
   ```
   python3 knowledge/_compose_slice.py "<the request>" --out seed.json --explain
   ```
   Typed inputs sharpen it: `--roles page-frame,record-list --intent comparison
   --components button,table --shape "parts-of-whole" --budget 20000`. The seed's
   fields are the contract — `components` · `governs` (rulings) · `obeys`
   (authored / derived / routed, BLOCKING first) · `mustNot` (incl. `ref:null`) ·
   `tokens` (group + tier) · `assets` (icons / logos) · `unresolved` · `sized` — and
   a field that is `null` says why in `$nulls`. Open a meta only for a component the
   seed names (`components[].meta`), and the snippet it names (`components[].snippet`);
   `knowledge/canon/canon.css` + `type.css` are what you LINK, not what you read.
   The seed is composed ONCE; the session works from it. When a later prompt needs a
   node the seed excluded — or a ruling inscribed after it — use the ASK door, which
   reads the Constitution live and answers one of the 12 designer questions in ≤1K
   tokens:
   ```
   python3 knowledge/_compose_slice.py --ask "what governs component:button?" --seed seed.json
   ```
   (governs · binds · principle · conflicts · ruled · evidence · answers · avoid ·
   tokens · usedIn · wcag · assets — `python3 knowledge/_compose_slice.py --help`
   lists them.) A refusal names its first obstacle; do not work around it.
   **Fallback, declared, not default:** only if `knowledge/_compose_slice.py` is not
   in the pack you were given, read `knowledge/components/*.meta.json` for the
   contract as before — and write `step 1: metas-read fallback (no reader in pack)`
   in the used / missing note so the run says which door it used.
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
