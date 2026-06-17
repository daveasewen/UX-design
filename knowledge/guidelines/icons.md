---
title: Icons
source: HSBC Common Toolkit (MCP) — "Gaps and edits" branch, Foundations › Icons page (node 2107:29115)
type: foundation-guidance
captured: 2026-06-17
related_tokens: icon-scale.json (sizes: xsmall 12 / small 18 / medium 24 / large 36; arrow dims), semantic-colour.json (icon/* colours)
related_assets: knowledge/assets/icons/ (exported SVG catalogue + icons.manifest.json)
external_ref: create.hsbc (most up-to-date icons); UI Centre (official SVG download for development)
note: No new tokens on this page. Icon SIZES are in icon-scale.json; icon COLOURS in semantic-colour.json (icon/*).
---

# Icons

## ⚠️ Sourcing rule (important)
Per HSBC guidance: **"Do not export SVGs from the HSBC Icon Library file or from artwork files. Download the SVGs from the UI Centre for sharing with development."** The most up-to-date icons live on **create.hsbc**; most are also in the HSBC Icon Library shipped with the toolkit.

**Implication for this project:** the SVGs we export from Figma (`knowledge/assets/icons/`, via `_export-icons.py`) are for **internal knowledge-base prototyping only**. For anything handed to development, source icons from the **UI Centre**, not from our Figma export.

## HSBC icon library
The icon set is organised into groups (see the Export board): Miscellaneous, Social, Touch, Informative, Volume and audio, Media, Arrows and chevrons, Products and services, Global controls, Status Icons.

## Default and active states
- In their **default** state, icons are depicted by simple lines.
- In their **active** state, they have a **solid fill**.
- **Not all icons have active states.**
- Icons should appear in the **active** state when a user interacts with or selects them (e.g. selecting a tooltip or a navigation section). The only exceptions are covered in the states and Notifications section.

(This is why the catalogue contains `… Active` variants; the manifest flags them with `active: true`.)

## Badges
A badge is attached to a UI element to inform the user of new activity and direct them to find out more — e.g. a badge by the inbox link when a new message arrives.

## Thicker weight icons
A few icons need to be used smaller than the standard recommended sizes. These are designed on the same 18×18px grid but with a **thicker 1.8px line weight**, so they can scale down without the line breaking up. Examples include thicker versions of chevrons and some state icons.

## Sizing & colour (tokens)
- **Sizes** (`icon-scale.json`): `xsmall` 12px, `small` 18px, `medium` 24px, `large` 36px; plus per-font arrow icon dimensions.
- **Colour** (`semantic-colour.json` → `icon/*`): e.g. `icon/default` (#333333 light / #FFFFFF dark), `icon/disabled`, `icon/default-reverse`. Monochrome icons in the exported catalogue use `currentColor` so they inherit these.
