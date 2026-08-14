# Text/icon token dark-mode contrast audit

> Each text/icon token is tested against the **worst-case (lightest) dark surface it can sit on**, resolved from the store — page default `#1A1A1A` + raised island `#1D1D1D`, or the token's own group surfaces. Since **s170** a state-suffixed ink (e.g. `.../label/default`) is paired only with its OWN state's ground — worst-case across states is a fall-back, not the rule. `on-light` tokens are excluded (light-only). Disabled-state tokens are allowlisted (reported, not gated). Text needs 4.5:1, icons/UI need 3:1.

**Result:** 17 pass · 5 allowed exception(s) · **1 gating failure(s)** · 5 skipped (light-only).

**Per-theme (s169 grounds + s170 overrides):** 9 pair(s) regraded where a theme moves the ground or the ink · **1 gating failure(s)** · 0 R-D24 exempted.

## Per-theme palette-resolved pairs (s157-D2 palette tier)

> The base pass above reads the semantic store, i.e. the activeBase theme (**apollo-mono**). Grounds owned by the palette tier are re-resolved here per theme via `tokens/themes/_themes.json` → `ragPalette`, and INKS are re-resolved per theme via that theme's `overrideSet` (s170). Only pairs whose ground or ink MOVES are listed; the `Moved` column says which. `❌` rows gate the build exactly as base failures do; `EXEMPTED` = a Legacy pair matched in R-D24's table.

| Theme | Palette | Token | Moved | Ink (base → theme) | Ground (base → theme) | Contrast | Need | Status |
|---|---|---|---|---|---|---|---|---|
| **Apollo Legacy** (`apollo-legacy`) | `palettes/rag/legacy.json` | `button/primary/icon/default` | ground | `#333333` | `button/primary/background/default` `#FAFAFA` → `#DB0011` | **2.42:1** | 3.0:1 | ❌ POOR |
| **Apollo Legacy** (`apollo-legacy`) | `palettes/rag/legacy.json` | `button/primary/label/default` | ink+ground | `#333333` → `#FFFFFF` | `button/primary/background/default` `#FAFAFA` → `#DB0011` | **5.22:1** | 3.0:1 | ✅ OK |
| **Apollo Legacy** (`apollo-legacy`) | `palettes/rag/legacy.json` | `rag/text/on-dark` | ground | `#FFFFFF` | `rag/error-background` `#F6604C` → `#A8000B` | **7.87:1** | 4.5:1 | ✅ OK |
| **Apollo Legacy** (`apollo-legacy`) | `palettes/rag/legacy.json` | `rag/text/on-information` | ink+ground | `#1A1A1A` → `#FFFFFF` | `rag/error-background` `#F6604C` → `#A8000B` | **7.87:1** | 4.5:1 | ✅ OK |
| **Apollo Legacy** (`apollo-legacy`) | `palettes/rag/legacy.json` | `text/secondary` | ink | `#FFFFFF` → `#9B9B9B` | page/raised `#1D1D1D` | **6.07:1** | 4.5:1 | ✅ OK |
| **Apollo Console** (`apollo-console`) | `palettes/rag/console-supercharge.json` | `rag/text/on-dark` | ground | `#FFFFFF` | `rag/error-background` `#F6604C` → `#B92F1E` | **6.02:1** | 4.5:1 | ✅ OK |
| **Apollo Console** (`apollo-console`) | `palettes/rag/console-supercharge.json` | `rag/text/on-information` | ink+ground | `#1A1A1A` → `#FFFFFF` | `rag/error-background` `#F6604C` → `#B92F1E` | **6.02:1** | 4.5:1 | ✅ OK |
| **Apollo Supercharge** (`apollo-supercharge`) | `palettes/rag/console-supercharge.json` | `rag/text/on-dark` | ground | `#FFFFFF` | `rag/error-background` `#F6604C` → `#B92F1E` | **6.02:1** | 4.5:1 | ✅ OK |
| **Apollo Supercharge** (`apollo-supercharge`) | `palettes/rag/console-supercharge.json` | `rag/text/on-information` | ink+ground | `#1A1A1A` → `#FFFFFF` | `rag/error-background` `#F6604C` → `#B92F1E` | **6.02:1** | 4.5:1 | ✅ OK |

## ❌ Gating failures — these FAIL the build

| Token | Dark value | Surface | Contrast | Need | Context |
|---|---|---|---|---|---|
| `rag/text/on-dark` | `#FFFFFF` | `#F6604C` (rag) | **3.14:1** | 4.5:1 | text |

## Allowed exceptions (reported, not gated)

| Token | Dark value | Surface | Contrast | Reason |
|---|---|---|---|---|
| `button/primary/label/disabled` | `#808080` | `#484848` | 2.32:1 | Disabled button label — exempt from WCAG 1.4.3 (inactive UI component). |
| `button/secondary/label/disabled` | `#808080` | `#484848` | 2.32:1 | Disabled button label — exempt from WCAG 1.4.3 (inactive UI component). |
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
| `button/primary/icon/default` | `#333333` | `#FAFAFA` | 12.1:1 | ✅ OK |
| `button/primary/label/default` | `#333333` | `#FAFAFA` | 12.1:1 | ✅ OK |
| `button/primary/label/disabled` | `#808080` | `#484848` | 2.32:1 | 🟡 ALLOWED |
| `button/quaternary/label/default` | `#FFFFFF` | `#232323` | 15.72:1 | ✅ OK |
| `button/quaternary/label/disabled` | `#808080` | `#232323` | 3.98:1 | ✅ OK |
| `button/secondary/label/default` | `#000000` | `#808080` | 5.32:1 | ✅ OK |
| `button/secondary/label/disabled` | `#808080` | `#484848` | 2.32:1 | 🟡 ALLOWED |
| `button/tertiary/label/default` | `#FFFFFF` | `#232323` | 15.72:1 | ✅ OK |
| `button/tertiary/label/disabled` | `#808080` | `#232323` | 3.98:1 | ✅ OK |
| `data/control/label-disabled/color` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `data/text/on-series` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/default-reverse` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `icon/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | `#F6604C` | 3.14:1 | ❌ POOR |
| `rag/text/on-information` | `#1A1A1A` | `#F6604C` | 5.55:1 | ✅ OK |
| `tertiary/text/disabled` | `#808080` | `#484848` | 2.32:1 | 🟡 ALLOWED |
| `tertiary/text/pressed` | `#FFFFFF` | `#1A1A1A` | 17.4:1 | ✅ OK |
| `text/default` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `text/disabled` | `#808080` | `#1D1D1D` | 4.27:1 | 🟡 ALLOWED |
| `text/on-disabled` | `#808080` | `#1D1D1D` | 4.27:1 | 🟡 ALLOWED |
| `text/reverse` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |
| `text/secondary` | `#FFFFFF` | `#1D1D1D` | 16.86:1 | ✅ OK |