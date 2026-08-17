# Indicator/accent token dark-mode contrast audit

> Brand red, RAG status, interactive-state, and border tokens tested at **3:1** (WCAG 1.4.11) against the worst-case (lightest) dark surface resolved from the store — page default `#1A1A1A` + raised island `#1D1D1D`. `on-light` tokens excluded (light-only). Border tokens included since 2026-07-14 (1.4.11 explicitly covers UI-component boundaries). `*/disabled` tokens excluded — WCAG 1.4.11 itself exempts inactive components.

**Result:** 46 pass · 0 allowed exception(s) · **0 gating failure(s)** · 5 skipped (light-only).

## Skipped — light-mode-only tokens

| Token | Reason |
|---|---|
| `data-vis/border/on-light/baseline-1` | light-mode-only (on-light); excluded from dark audit |
| `data-vis/border/on-light/baseline-2` | light-mode-only (on-light); excluded from dark audit |
| `data-vis/border/on-light/gridline` | light-mode-only (on-light); excluded from dark audit |
| `data-vis/border/on-light/indicator` | light-mode-only (on-light); excluded from dark audit |
| `rag/text/on-light` | light-mode-only (on-light); excluded from dark audit |

## All audited indicator/accent tokens

| Token | Dark value | Surface | Contrast | Status |
|---|---|---|---|---|
| `border/action-strong` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `border/strong` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `border/subtle` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `button/primary/icon/default` | `#333333` | `#FFFFFF` | 12.63:1 | ✅ OK |
| `button/primary/label/default` | `#333333` | `#FFFFFF` | 12.63:1 | ✅ OK |
| `button/tertiary/border/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-1` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-2` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `data-vis/border/on-dark/gridline` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `data-vis/border/on-dark/indicator` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `divider/border/break` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `divider/border/section` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `divider/border/subsection` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `divider/border/subsectionInset` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `elevation/border` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `form/border/active` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `form/border/default` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `form/border/pressed` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `primary/border/default` | `#DB0011` | `#1D1D1D` | 3.23:1 | ✅ OK |
| `primary/border/hover` | `#D61412` | `#1D1D1D` | 3.19:1 | ✅ OK |
| `primary/border/pressed` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/error` | `#F6604C` | `#1D1D1D` | 5.38:1 | ✅ OK |
| `rag/error-glyph` | `#F6604C` | `#1D1D1D` | 5.38:1 | ✅ OK |
| `rag/error-graphic` | `#CC4333` | `#1D1D1D` | 3.55:1 | ✅ OK |
| `rag/error-ink` | `#F6604C` | `#1D1D1D` | 5.38:1 | ✅ OK |
| `rag/information` | `#78A7E8` | `#1D1D1D` | 6.82:1 | ✅ OK |
| `rag/information-glyph` | `#78A7E8` | `#1D1D1D` | 6.82:1 | ✅ OK |
| `rag/information-graphic` | `#2674DC` | `#1D1D1D` | 3.7:1 | ✅ OK |
| `rag/neutral` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/success` | `#66CC8D` | `#1D1D1D` | 8.5:1 | ✅ OK |
| `rag/success-glyph` | `#66CC8D` | `#1D1D1D` | 8.5:1 | ✅ OK |
| `rag/success-graphic` | `#4A9568` | `#1D1D1D` | 4.65:1 | ✅ OK |
| `rag/success-ink` | `#66CC8D` | `#1D1D1D` | 8.5:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#F6604C` | 3.14:1 | ✅ OK |
| `rag/text/on-information` | `#1A1A1A` | `#F6604C` | 5.55:1 | ✅ OK |
| `rag/warning` | `#E0A61F` | `#1D1D1D` | 7.74:1 | ✅ OK |
| `rag/warning-glyph` | `#E0A61F` | `#1D1D1D` | 7.74:1 | ✅ OK |
| `rag/warning-graphic` | `#C58900` | `#1D1D1D` | 5.58:1 | ✅ OK |
| `secondary/border/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `secondary/border/hover` | `#F0F0F0` | `#1D1D1D` | 14.79:1 | ✅ OK |
| `secondary/border/pressed` | `#E1E1E1` | `#1D1D1D` | 12.89:1 | ✅ OK |
| `table/border` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `tabs/overflow-border` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `tabs/standard-border` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `tertiary/border/default` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `tooltip/border` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |