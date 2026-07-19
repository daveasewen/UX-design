# Text/icon token dark-mode contrast audit

> Each text/icon token is tested against the **worst-case (lightest) dark surface it can sit on**, resolved from the store — page default `#1A1A1A` + raised island `#1D1D1D`, or the token's own group surfaces. `on-light` tokens are excluded (light-only). Disabled-state tokens are allowlisted (reported, not gated). Text needs 4.5:1, icons/UI need 3:1.

**Result:** 8 pass · 2 allowed exception(s) · **0 gating failure(s)** · 2 skipped (light-only).

## Allowed exceptions (reported, not gated)

| Token | Dark value | Surface | Contrast | Reason |
|---|---|---|---|---|
| `tertiary/text/disabled` | `#808080` | `#484848` | 2.32:1 | Disabled text — exempt from WCAG 1.4.3 (inactive UI component). |
| `text/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | Disabled text — exempt from WCAG 1.4.3 (inactive UI component). |

## Skipped — light-mode-only tokens

| Token | Reason |
|---|---|
| `rag/text/on-light` | light-mode-only (on-light); excluded from dark audit |
| `text/on-inverse` | sits on an inverting surface (secondary/pressed buttons), not the page; validated per-component via snippet contrast pairs |

## All audited text/icon tokens

| Token | Dark value | Surface | Contrast | Status |
|---|---|---|---|---|
| `icon/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/default-reverse` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#B92F1E` | 6.02:1 | ✅ OK |
| `tertiary/text/disabled` | `#808080` | `#484848` | 2.32:1 | 🟡 ALLOWED |
| `tertiary/text/pressed` | `#FFFFFF` | `#484848` | 9.15:1 | ✅ OK |
| `text/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `text/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | 🟡 ALLOWED |
| `text/reverse` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `text/secondary` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |