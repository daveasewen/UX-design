# Text/icon token dark-mode contrast audit

> Each text/icon token is tested against the **worst-case (lightest) dark surface it can sit on**, resolved from the store — page default `#1A1A1A` + raised island `#1D1D1D`, or the token's own group surfaces. `on-light` tokens are excluded (light-only). Disabled-state tokens are allowlisted (reported, not gated). Text needs 4.5:1, icons/UI need 3:1.

**Result:** 17 pass · 4 allowed exception(s) · **0 gating failure(s)** · 5 skipped (light-only).

## Allowed exceptions (reported, not gated)

| Token | Dark value | Surface | Contrast | Reason |
|---|---|---|---|---|
| `button/secondary/label/disabled` | `#808080` | `#B7B7B7` | 1.97:1 | Disabled button label — exempt from WCAG 1.4.3 (inactive UI component). |
| `tertiary/text/disabled` | `#808080` | `#484848` | 2.32:1 | Disabled text — exempt from WCAG 1.4.3 (inactive UI component). |
| `text/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | Disabled text — exempt from WCAG 1.4.3 (inactive UI component). |
| `text/on-disabled` | `#808080` | `#1D1D1D` | 4.27:1 | Disabled label ink — visible ghost, exempt from WCAG 1.4.3 (inactive UI component). |

## Skipped — light-mode-only tokens

| Token | Reason |
|---|---|
| `icon/on-inverse` | sits on an inverting surface (secondary/pressed buttons), not the page; validated per-component via snippet contrast pairs |
| `rag/text/on-light` | light-mode-only (on-light); excluded from dark audit |
| `text/on-action` | sits ONLY on surface/action (button/secondary fill), never the page/raised ground; validated per-component via button/secondary/label/default (10.47:1 dark) — same shape as text/on-inverse above |
| `text/on-inverse` | sits on an inverting surface (secondary/pressed buttons), not the page; validated per-component via snippet contrast pairs |
| `text/on-success` | sits ONLY on rag/success-background (the R-D14 green success fill), never the page/raised ground; validated per-component via the Button success contrast pair (black on green = 7.65:1 light / 7.45:1 dark) — same shape as text/on-action above |

## All audited text/icon tokens

| Token | Dark value | Surface | Contrast | Status |
|---|---|---|---|---|
| `button/primary/icon/default` | `#333333` | `#FFFFFF` | 12.63:1 | ✅ OK |
| `button/primary/label/default` | `#333333` | `#FFFFFF` | 12.63:1 | ✅ OK |
| `button/primary/label/disabled` | `#808080` | `#FFFFFF` | 3.95:1 | ✅ OK |
| `button/quaternary/label/default` | `#FFFFFF` | `#232323` | 15.72:1 | ✅ OK |
| `button/quaternary/label/disabled` | `#808080` | `#232323` | 3.98:1 | ✅ OK |
| `button/secondary/label/default` | `#000000` | `#B7B7B7` | 10.47:1 | ✅ OK |
| `button/secondary/label/disabled` | `#808080` | `#B7B7B7` | 1.97:1 | 🟡 ALLOWED |
| `button/tertiary/label/default` | `#FFFFFF` | `#232323` | 15.72:1 | ✅ OK |
| `button/tertiary/label/disabled` | `#808080` | `#232323` | 3.98:1 | ✅ OK |
| `data/text/on-series` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/default-reverse` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#B92F1E` | 6.02:1 | ✅ OK |
| `tertiary/text/disabled` | `#808080` | `#484848` | 2.32:1 | 🟡 ALLOWED |
| `tertiary/text/pressed` | `#FFFFFF` | `#484848` | 9.15:1 | ✅ OK |
| `text/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `text/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | 🟡 ALLOWED |
| `text/on-disabled` | `#808080` | `#1D1D1D` | 4.27:1 | 🟡 ALLOWED |
| `text/reverse` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `text/secondary` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |