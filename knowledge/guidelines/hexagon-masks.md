---
title: Hexagon masks (creative hexagons)
source: HSBC Common Toolkit (MCP) — "Gaps and edits" branch, Foundations › Hexagon masks page (node 960:26374)
type: foundation-guidance
captured: 2026-06-17
external_ref: https://create.hsbc/foundations-and-identity/Creative-hexagons.html
note: Sticker sheet; detailed usage/types/placement on create.hsbc. No design tokens. Mask shapes can be exported as assets on request (see "Assets" below).
related_assets: knowledge/assets/hexagons/ (not yet exported)
---

# Hexagon masks (creative hexagons)

The HSBC hexagon used as a **creative device to mask/crop imagery**. Full usage, types and placement rules live on create.hsbc → [Creative hexagons](https://create.hsbc/foundations-and-identity/Creative-hexagons.html).

> **Usage constraint (from the component):** the hexagon mask is "**only to be used to mask image shapes**" — it crops imagery into the hexagon silhouette; it's not a container/background fill.

## Types
- **Iconic Hexagon** — the full/closed hexagon device (500×250 artwork).
- **Open Hexagon** — the open hexagon variant (500×250). Documented purpose: "Hexagon mask".
- **Cropped Hexagon** — partial hexagon crops for masking imagery into standard image ratios.

## Cropped Hexagon variants
Each crop comes in 5 aspect ratios, each with **top / middle / bottom** positions and **left / right** sides (6 versions per ratio → 30 masks). Reference width 295px:

| Ratio | Example size (w×h) |
|---|---|
| 1:1 | 295 × 295 |
| 4:3 | 295 × 221 |
| 16:9 | 295 × 166 |
| 21:9 | 295 × 126 |
| 3:1 | 295 × 98 |

The mask is applied as an **alpha mask** over an image (CSS `mask-image` / Figma mask), so the underlying photo shows through the hexagon-cropped shape.

## Assets (optional export)
The mask shapes (Iconic, Open, and the 30 Cropped variants) can be exported to `knowledge/assets/hexagons/` as SVG using the same REST pattern as `_export-icons.py` / `_export-logos.py` (needs a `file_content:read` token). Useful for brand-accurate image cropping in prototypes — export on request. Per the icons sourcing rule, treat as internal prototype assets.
