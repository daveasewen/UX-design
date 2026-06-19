# Indicator/accent token dark-mode contrast audit

> Checks if brand red, RAG status, and interactive state tokens' dark values create sufficient contrast on the standard dark surface (#1D1D1D). Minimum threshold: 3:1 (UI component).

**Coverage:** 6/7 indicator tokens pass · 1 below threshold.

## Poor contrast — requires fix

| Token | Dark value | Contrast on #1D1D1D | Threshold |
|---|---|---|---|
| `rag/text/on-light` | `#333333` | **1.33:1** | 3.0:1 |

## All indicator/accent tokens

| Token | Dark value | Contrast on #1D1D1D | Status |
|---|---|---|---|
| `rag/error` | `#DB0011` | 3.23:1 | ✅ OK |
| `rag/information` | `#4587A7` | 4.24:1 | ✅ OK |
| `rag/neutral` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `rag/success` | `#00847F` | 3.7:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `rag/text/on-light` | `#333333` | 1.33:1 | ❌ POOR |
| `rag/warning` | `#FFBB33` | 9.96:1 | ✅ OK |