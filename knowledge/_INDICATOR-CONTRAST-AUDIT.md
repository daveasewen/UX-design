# Indicator/accent token dark-mode contrast audit

> Brand red, RAG status, and interactive-state tokens tested at **3:1** (WCAG 1.4.11) against the worst-case (lightest) dark surface resolved from the store — page default `#000000` + raised island `#1D1D1D`. `on-light` tokens excluded (light-only).

**Result:** 6 pass · 0 allowed exception(s) · **0 gating failure(s)** · 1 skipped (light-only).

## Skipped — light-mode-only tokens

| Token | Reason |
|---|---|
| `rag/text/on-light` | light-mode-only (on-light); excluded from dark audit |

## All audited indicator/accent tokens

| Token | Dark value | Surface | Contrast | Status |
|---|---|---|---|---|
| `rag/error` | `#DB0011` | `#1D1D1D` | 3.23:1 | ✅ OK |
| `rag/information` | `#4587A7` | `#1D1D1D` | 4.24:1 | ✅ OK |
| `rag/neutral` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/success` | `#00847F` | `#1D1D1D` | 3.7:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `rag/warning` | `#FFBB33` | `#1D1D1D` | 9.96:1 | ✅ OK |