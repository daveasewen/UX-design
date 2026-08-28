---
name: generate-from-canon
description: Build a screen or component using only the Apollo design system — its 135 reviewed components, its tokens, its type composites and its layout rails — never inventing new ones. Flags anything the system is missing instead of improvising. Use when you want on-brand, accessible UI drafted by construction. Outputs React (preferred) or plain HTML/CSS.
---

# Generate from canon

Draft UI **strictly from the design system**. The one job here is to stop the common
failure of AI design work — quietly *inventing* components, variants or colours. If it
isn't in the system, this skill flags it rather than making it up.

This is the **strict** mode: deliberately faithful, not a creativity play. When the
system is genuinely missing something you need, use `draft-a-new-pattern`.

## Where things live

Four files answer almost every question. Go to them in this order.

| question | file |
|---|---|
| **What exists?** | `showroom/index.json` — 143 entries: 135 components + 8 foundations. Each carries `slug`, `name`, `aliases`, a one-line `blurb`, `level` (element / pattern / block / shell / template), `usage` group, `status` (stable / beta / deprecated), `related`, and its `page`. Search this by aliases and blurb, not by guessing a name. |
| **What does it look like?** | `showroom/<slug>.html` — the live page, every variant and state. `showroom/_thumbs/<slug>.png` for a glance. |
| **What is its contract?** | `knowledge/components/<slug>.meta.json` — `purpose`, `props` (with the token each prop `binds` to), `variants`, `tokens`, `relationships`, `accessibility`, `antiPatterns`, `provenance`. |
| **What is the real markup?** | `knowledge/snippets/<Slug>.reference.html` — the reviewed, gated source. Copy from here. Never re-draw a component from the picture. |

⚠ **Filenames are the index `slug`, but the capitalisation isn't consistent** between the
two folders — `summary` has `components/summary.meta.json` and
`snippets/Summary.reference.html`; `cta-lockup` has `snippets/CTA-lockup.reference.html`.
Match the slug **case-insensitively** (glob it) rather than guessing the case. Every one
of the 135 resolves that way.

Everything else: `knowledge/canon/canon.css` (all tokens, aliases, utilities and all 135
components), `knowledge/canon/type.css` (the type composites),
`knowledge/assets/icons/` (659 glyphs + `icons.manifest.json`),
`knowledge/guidelines/` (59 briefing notes; `_rules-index.json` indexes 470 rules from
them, each tagged BLOCKING / ADVISORY / REVIEW / TASTE),
`showroom/_foundations/` (grids, bento, logos, photography).

## Rules (non-negotiable)

1. **Only what exists.** Every component and variant comes from `showroom/index.json` /
   `knowledge/components/`. Missing what you need? Put it on a **Gaps** list and stop —
   never improvise a component or a variant.
2. **Copy the snippet, don't re-draw it.** Take markup and classes from
   `knowledge/snippets/<Slug>.reference.html`. Hand-rolling a component from its
   screenshot invents defects that the gates then catch as yours.
3. **Bind every visual value to a token by intent** — never a raw hex or px. The names
   live in `knowledge/tokens/*.json` and resolve in `knowledge/canon/canon.css`
   (`primary/background/hover` → `var(--primary-background-hover)`). Spacing, radius and
   border width are tokens too, not just colour: a raw px freezes the thing in every
   theme.
4. **Type via composites.** Component text takes a class from `knowledge/canon/type.css`
   — `.t-cm-*` for component text (button, label, caption, input, figure-1…6,
   chart-label, ctl-12/14/16), `.t-ed-*` for editorial (display-1/2, heading-1…4, body,
   body-small, caption). 31 in all. Never a raw `font-size` / `font-weight` /
   `line-height`.
5. **Pick a theme and say which.** Four ship: **mono** (the baseline), **legacy**,
   **console**, **supercharge**. Set them on the root element:
   `class="canon" data-apollo-theme="mono" data-theme="light"`. The theme registry is
   `knowledge/tokens/themes/_themes.json`, and it records which colours belong to which
   theme. A colour from another theme's set is a leak, not a choice.
6. **Colour is meaning, and the reds are keyed to their background.**
   - Coloured red or green **text** exists in exactly one place: monetary values, always
     next to a symbol (minus, plus, up/down arrow). Nowhere else.
   - Two reds, chosen by the background behind them, not by light/dark mode: the dark red
     `#DA1A00` on **white**, the light red `#F6604C` on **everything else** — dark mode
     and every non-white ground alike.
   - Error checkboxes and radios take the red on the **mark only**. The label keeps
     default ink.
   - In mono, text and glyphs on an error surface take the default dark ink, both modes.
     White-on-error does not exist.
   - Ink itself is a token, not a literal — it resolves per theme (and it is never pure
     black). Bind to it; don't type a hex.
7. **Layout comes from the rails, not from taste.** For bento, grids and the layout
   dials, read **one file**: `knowledge/_render/_bento_edit_rails.json`. It carries every
   dial, its legal option set, the per-theme default, which options may be combined
   (chords) and which exclude each other. Generation ships the defaults — you do not have
   to decide anything up front. If a layout question isn't answered there, it's a Gap.
   Spacing picks from the ruled stops `{1, 2, 4, 16, 24, 40}`, never a free value.
8. **Icons are real assets only** — from `knowledge/assets/icons/`. Never draw a glyph.
   If a shape is genuinely custom, mark it `<svg data-bespoke="why">` so it reads as a
   decision rather than an invention.
9. **Honour `antiPatterns` and `relationships`** from each component's meta —
   `mustNotNeighbour` in particular.
10. **Cover the states**: default / hover / pressed / focus / disabled / loading / error /
    empty, as the component defines them.
11. **Sentence case** for headings and labels. No ALL-CAPS outside acronyms.
12. **Carry provenance** — note which component and which tokens each part came from.

## Procedure

1. **Find.** Search `showroom/index.json` for each thing the screen needs — by alias and
   blurb. Open the showroom page to confirm it's the right thing.
2. **Read the contract.** `knowledge/components/<slug>.meta.json` — variants, states,
   antiPatterns, relationships.
3. **Compose.** Link `knowledge/canon/canon.css` and `knowledge/canon/type.css`. Root
   element (or `<body>`) gets `class="canon"` plus **one** theme attribute:
   `data-theme="light"` or `data-theme="dark"`. That is the whole contract — it is what
   `canon.css` actually selects on, and it is what
   `knowledge/_RUNBOOK-compose-from-canon.md` § Compose a screen says. (`data-mode` is a
   component-level attribute, not a theme one: in `canon.css` it appears only inside
   `.cn-template-auth`, swapping a light/dark logo mark. Do not put it on the root.) Drop each component in as
   its scope class + the snippet's own markup — `<div class="cn-button"><button class="btn
   primary">…</button></div>`. Use the `.c-*` layout utilities. **Your own `<style>` is
   harness only**: no hex, no redefining a `.c-*` or `.cn-*` class. If you're redefining a
   component locally, you've left canon.
   The long version of this is `knowledge/_RUNBOOK-compose-from-canon.md`.
4. **Gaps.** Anything the system can't supply → the Gaps list. Don't invent.
5. **Prove it.** Run the gates on what you built — see the `check-with-gates` skill.
   Composed screens have their own runner:
   `python3 knowledge/_validate_screen.py path/to/your-screen.html`.
   A draft you haven't gated is a claim, not a result.

## Output

- The code (React wiring the real components, or HTML/CSS on the canon classes).
- A short **used / missing** note: components and tokens drawn on, plus any Gaps.
- The gate verdict from step 5, as it actually printed.

> With Figma Dev Mode + Code Connect available you can pull components and variables
> live; otherwise the files above are the source of truth.

*Experimental — feedback on what's missing is the point.*
