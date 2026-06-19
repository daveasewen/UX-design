# Text/icon token dark-mode contrast audit

> Checks if all text, icon, and label tokens' dark values create sufficient contrast on the standard dark surface (#1D1D1D, HSBC dark-mode/600). Text needs 4.5:1 (AA), icons/UI need 3:1 (AA).

**Coverage:** 7/10 text/icon tokens pass · 3 below threshold.

## Poor contrast — requires fix

| Token | Dark value | Contrast on #1D1D1D | Threshold | Context |
|---|---|---|---|---|
| `rag/text/on-light` | `#333333` | **1.33:1** | 4.5:1 | text |
| `tertiary/text/disabled` | `#767676` | **3.71:1** | 4.5:1 | text |
| `text/disabled` | `#767676` | **3.71:1** | 4.5:1 | text |

## All text/icon tokens

| Token | Dark value | Contrast on #1D1D1D | Threshold | Status |
|---|---|---|---|---|
| `icon/default` | `#FFFFFF` | 16.86:1 | 3.0:1 | ✅ OK |
| `icon/default-reverse` | `#FFFFFF` | 16.86:1 | 3.0:1 | ✅ OK |
| `icon/disabled` | `#767676` | 3.71:1 | 3.0:1 | ✅ OK |
| `rag/text/on-dark` | `#FFFFFF` | 16.86:1 | 4.5:1 | ✅ OK |
| `rag/text/on-light` | `#333333` | 1.33:1 | 4.5:1 | ❌ POOR |
| `tertiary/text/disabled` | `#767676` | 3.71:1 | 4.5:1 | ❌ POOR |
| `tertiary/text/pressed` | `#FFFFFF` | 16.86:1 | 4.5:1 | ✅ OK |
| `text/default` | `#FFFFFF` | 16.86:1 | 4.5:1 | ✅ OK |
| `text/disabled` | `#767676` | 3.71:1 | 4.5:1 | ❌ POOR |
| `text/reverse` | `#FFFFFF` | 16.86:1 | 4.5:1 | ✅ OK |