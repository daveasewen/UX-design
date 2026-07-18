# Indicator/accent token dark-mode contrast audit

> Brand red, RAG status, interactive-state, and border tokens tested at **3:1** (WCAG 1.4.11) against the worst-case (lightest) dark surface resolved from the store — page default `#000000` + raised island `#1D1D1D`. `on-light` tokens excluded (light-only). Border tokens included since 2026-07-14 (1.4.11 explicitly covers UI-component boundaries). `*/disabled` tokens excluded — WCAG 1.4.11 itself exempts inactive components.

**Result:** 34 pass · 0 allowed exception(s) · **0 gating failure(s)** · 5 skipped (light-only).

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
| `border/strong` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `border/subtle` | `#707070` | `#1D1D1D` | 3.4:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-1` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-2` | `#6C6C6C` | `#1D1D1D` | 3.21:1 | ✅ OK |
| `data-vis/border/on-dark/gridline` | `#6C6C6C` | `#1D1D1D` | 3.21:1 | ✅ OK |
| `data-vis/border/on-dark/indicator` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `divider/border/break` | `#696969` | `#1D1D1D` | 3.07:1 | ✅ OK |
| `divider/border/section` | `#707070` | `#1D1D1D` | 3.4:1 | ✅ OK |
| `divider/border/subsection` | `#696969` | `#1D1D1D` | 3.07:1 | ✅ OK |
| `divider/border/subsectionInset` | `#696969` | `#1D1D1D` | 3.07:1 | ✅ OK |
| `elevation/border` | `#767676` | `#1D1D1D` | 3.71:1 | ✅ OK |
| `form/border/active` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `form/border/default` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `form/border/pressed` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `primary/border/default` | `#DB0011` | `#1D1D1D` | 3.23:1 | ✅ OK |
| `primary/border/hover` | `#D61412` | `#1D1D1D` | 3.19:1 | ✅ OK |
| `primary/border/pressed` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/error` | `#DB0011` | `#1D1D1D` | 3.23:1 | ✅ OK |
| `rag/error-glyph` | `#CC4333` | `#1D1D1D` | 3.55:1 | ✅ OK |
| `rag/information` | `#4587A7` | `#1D1D1D` | 4.24:1 | ✅ OK |
| `rag/information-glyph` | `#2674DC` | `#1D1D1D` | 3.7:1 | ✅ OK |
| `rag/neutral` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/success` | `#00847F` | `#1D1D1D` | 3.7:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#2674DC` | 4.55:1 | ✅ OK |
| `rag/warning` | `#FFBB33` | `#1D1D1D` | 9.96:1 | ✅ OK |
| `rag/warning-glyph` | `#C58900` | `#1D1D1D` | 5.58:1 | ✅ OK |
| `secondary/border/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `secondary/border/hover` | `#EDEDED` | `#1D1D1D` | 14.4:1 | ✅ OK |
| `secondary/border/pressed` | `#D7D8D6` | `#1D1D1D` | 11.79:1 | ✅ OK |
| `table/border` | `#707070` | `#1D1D1D` | 3.4:1 | ✅ OK |
| `tabs/overflow-border` | `#787878` | `#1D1D1D` | 3.82:1 | ✅ OK |
| `tabs/standard-border` | `#787878` | `#1D1D1D` | 3.82:1 | ✅ OK |
| `tertiary/border/default` | `#767676` | `#1D1D1D` | 3.71:1 | ✅ OK |
| `tooltip/border` | `#707070` | `#1D1D1D` | 3.4:1 | ✅ OK |