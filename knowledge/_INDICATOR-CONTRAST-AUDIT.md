# Indicator/accent token dark-mode contrast audit

> Checks if brand red, RAG status, and interactive state tokens' dark values create sufficient contrast on the standard dark surface (#1D1D1D). Minimum threshold: 3:1 (UI component).

**Coverage:** 19/29 indicator tokens pass · 10 below threshold.

## Poor contrast — requires fix

| Token | Dark value | Contrast on #1D1D1D | Threshold |
|---|---|---|---|
| `data-vis/surface/primary` | `#000000` | **1.25:1** | 3.0:1 |
| `rag/error` | `#A8000B` | **2.14:1** | 3.0:1 |
| `rag/error-tint` | `#260005` | **1.15:1** | 3.0:1 |
| `rag/information` | `#305A85` | **2.35:1** | 3.0:1 |
| `rag/information-tint` | `#000D1B` | **1.16:1** | 3.0:1 |
| `rag/success-tint` | `#001615` | **1.11:1** | 3.0:1 |
| `rag/text/on-light` | `#333333` | **1.33:1** | 3.0:1 |
| `rag/warning-tint` | `#221701` | **1.05:1** | 3.0:1 |
| `tertiary/background/active` | `#1D1D1D` | **1.0:1** | 3.0:1 |
| `tertiary/background/pressed` | `#1D1D1D` | **1.0:1** | 3.0:1 |

## All indicator/accent tokens

| Token | Dark value | Contrast on #1D1D1D | Status |
|---|---|---|---|
| `data-vis/surface/primary` | `#000000` | 1.25:1 | ❌ POOR |
| `form/background/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/border/active` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/border/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `rag/error` | `#A8000B` | 2.14:1 | ❌ POOR |
| `rag/error-tint` | `#260005` | 1.15:1 | ❌ POOR |
| `rag/information` | `#305A85` | 2.35:1 | ❌ POOR |
| `rag/information-tint` | `#000D1B` | 1.16:1 | ❌ POOR |
| `rag/neutral` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `rag/success` | `#00847F` | 3.7:1 | ✅ OK |
| `rag/success-tint` | `#001615` | 1.11:1 | ❌ POOR |
| `rag/text/on-dark` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `rag/text/on-light` | `#333333` | 1.33:1 | ❌ POOR |
| `rag/warning` | `#FFBB33` | 9.96:1 | ✅ OK |
| `rag/warning-tint` | `#221701` | 1.05:1 | ❌ POOR |
| `secondary/background/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/border/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `tabs/active` | `#DB0011` | 3.23:1 | ✅ OK |
| `tertiary/background/active` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tertiary/background/pressed` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tertiary/text/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |