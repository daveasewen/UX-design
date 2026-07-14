# Indicator/accent token dark-mode contrast audit

> Brand red, RAG status, interactive-state, and border tokens tested at **3:1** (WCAG 1.4.11) against the worst-case (lightest) dark surface resolved from the store — page default `#000000` + raised island `#1D1D1D`. `on-light` tokens excluded (light-only). Border tokens included since 2026-07-14 (1.4.11 explicitly covers UI-component boundaries). `*/disabled` tokens excluded — WCAG 1.4.11 itself exempts inactive components.

**Result:** 16 pass · 0 allowed exception(s) · **15 gating failure(s)** · 5 skipped (light-only).

## ❌ Gating failures — these FAIL the build

| Token | Dark value | Surface | Contrast | Need |
|---|---|---|---|---|
| `border/strong` | `#656565` | `#1D1D1D` (page/raised) | **2.89:1** | 3.0:1 |
| `border/subtle` | `#404040` | `#1D1D1D` (page/raised) | **1.63:1** | 3.0:1 |
| `data-vis/border/on-dark/baseline-2` | `#333333` | `#1D1D1D` (page/raised) | **1.33:1** | 3.0:1 |
| `data-vis/border/on-dark/gridline` | `#333333` | `#1D1D1D` (page/raised) | **1.33:1** | 3.0:1 |
| `divider/border/break` | `#212121` | `#1D1D1D` (page/raised) | **1.05:1** | 3.0:1 |
| `divider/border/section` | `#404040` | `#1D1D1D` (page/raised) | **1.63:1** | 3.0:1 |
| `divider/border/subsection` | `#212121` | `#1D1D1D` (page/raised) | **1.05:1** | 3.0:1 |
| `divider/border/subsectionInset` | `#212121` | `#1D1D1D` (page/raised) | **1.05:1** | 3.0:1 |
| `form/border/default` | `#656565` | `#1D1D1D` (page/raised) | **2.89:1** | 3.0:1 |
| `form/border/pressed` | `#656565` | `#1D1D1D` (page/raised) | **2.89:1** | 3.0:1 |
| `primary/border/hover` | `#BA1110` | `#1D1D1D` (page/raised) | **2.55:1** | 3.0:1 |
| `table/border` | `#404040` | `#1D1D1D` (page/raised) | **1.63:1** | 3.0:1 |
| `tabs/overflow-border` | `#474747` | `#1D1D1D` (page/raised) | **1.81:1** | 3.0:1 |
| `tabs/standard-border` | `#474747` | `#1D1D1D` (page/raised) | **1.81:1** | 3.0:1 |
| `tooltip/border` | `#404040` | `#1D1D1D` (page/raised) | **1.63:1** | 3.0:1 |

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
| `border/strong` | `#656565` | `#1D1D1D` | 2.89:1 | ❌ POOR |
| `border/subtle` | `#404040` | `#1D1D1D` | 1.63:1 | ❌ POOR |
| `data-vis/border/on-dark/baseline-1` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-2` | `#333333` | `#1D1D1D` | 1.33:1 | ❌ POOR |
| `data-vis/border/on-dark/gridline` | `#333333` | `#1D1D1D` | 1.33:1 | ❌ POOR |
| `data-vis/border/on-dark/indicator` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `divider/border/break` | `#212121` | `#1D1D1D` | 1.05:1 | ❌ POOR |
| `divider/border/section` | `#404040` | `#1D1D1D` | 1.63:1 | ❌ POOR |
| `divider/border/subsection` | `#212121` | `#1D1D1D` | 1.05:1 | ❌ POOR |
| `divider/border/subsectionInset` | `#212121` | `#1D1D1D` | 1.05:1 | ❌ POOR |
| `elevation/border` | `#767676` | `#1D1D1D` | 3.71:1 | ✅ OK |
| `form/border/active` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `form/border/default` | `#656565` | `#1D1D1D` | 2.89:1 | ❌ POOR |
| `form/border/pressed` | `#656565` | `#1D1D1D` | 2.89:1 | ❌ POOR |
| `primary/border/default` | `#DB0011` | `#1D1D1D` | 3.23:1 | ✅ OK |
| `primary/border/hover` | `#BA1110` | `#1D1D1D` | 2.55:1 | ❌ POOR |
| `primary/border/pressed` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/error` | `#DB0011` | `#1D1D1D` | 3.23:1 | ✅ OK |
| `rag/information` | `#4587A7` | `#1D1D1D` | 4.24:1 | ✅ OK |
| `rag/neutral` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/success` | `#00847F` | `#1D1D1D` | 3.7:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/warning` | `#FFBB33` | `#1D1D1D` | 9.96:1 | ✅ OK |
| `secondary/border/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `secondary/border/hover` | `#EDEDED` | `#1D1D1D` | 14.4:1 | ✅ OK |
| `secondary/border/pressed` | `#D7D8D6` | `#1D1D1D` | 11.79:1 | ✅ OK |
| `table/border` | `#404040` | `#1D1D1D` | 1.63:1 | ❌ POOR |
| `tabs/overflow-border` | `#474747` | `#1D1D1D` | 1.81:1 | ❌ POOR |
| `tabs/standard-border` | `#474747` | `#1D1D1D` | 1.81:1 | ❌ POOR |
| `tertiary/border/default` | `#767676` | `#1D1D1D` | 3.71:1 | ✅ OK |
| `tooltip/border` | `#404040` | `#1D1D1D` | 1.63:1 | ❌ POOR |