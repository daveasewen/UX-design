# Surface token dark-mode contrast audit

> Checks if all background/surface/border tokens create sufficient contrast on the standard dark surface (#1D1D1D, HSBC dark-mode/600). Minimum threshold: 3:1 (UI component).

**Coverage:** 41/59 surface tokens pass · 18 below threshold.

## Poor contrast — requires fix

| Token | Dark value | Contrast on #1D1D1D | Threshold |
|---|---|---|---|
| `background/default` | `#000000` | **1.25:1** | 3.0:1 |
| `data-vis/border/on-dark/baseline-2` | `#333333` | **1.33:1** | 3.0:1 |
| `data-vis/border/on-dark/gridline` | `#333333` | **1.33:1** | 3.0:1 |
| `data-vis/border/on-light/baseline-2` | `#333333` | **1.33:1** | 3.0:1 |
| `data-vis/border/on-light/gridline` | `#333333` | **1.33:1** | 3.0:1 |
| `data-vis/surface/primary` | `#000000` | **1.25:1** | 3.0:1 |
| `data-vis/surface/secondary` | `#000000` | **1.25:1** | 3.0:1 |
| `tabs/background` | `#1D1D1D` | **1.0:1** | 3.0:1 |
| `tabs/overflow-background` | `#1D1D1D` | **1.0:1** | 3.0:1 |
| `tabs/overflow-border` | `#474747` | **1.81:1** | 3.0:1 |
| `tabs/standard-border` | `#474747` | **1.81:1** | 3.0:1 |
| `tertiary/background/active` | `#1D1D1D` | **1.0:1** | 3.0:1 |
| `tertiary/background/default` | `#1D1D1D` | **1.0:1** | 3.0:1 |
| `tertiary/background/disabled` | `#333333` | **1.33:1** | 3.0:1 |
| `tertiary/background/hover` | `#474747` | **1.81:1** | 3.0:1 |
| `tertiary/background/pressed` | `#1D1D1D` | **1.0:1** | 3.0:1 |
| `tertiary/border/default` | `#474747` | **1.81:1** | 3.0:1 |
| `tertiary/border/disabled` | `#333333` | **1.33:1** | 3.0:1 |

## All surface tokens

| Token | Dark value | Contrast on #1D1D1D | Status |
|---|---|---|---|
| `background/default` | `#000000` | 1.25:1 | ❌ POOR |
| `border/strong` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `border/subtle` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-1` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `data-vis/border/on-dark/baseline-2` | `#333333` | 1.33:1 | ❌ POOR |
| `data-vis/border/on-dark/gridline` | `#333333` | 1.33:1 | ❌ POOR |
| `data-vis/border/on-dark/indicator` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `data-vis/border/on-light/baseline-1` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `data-vis/border/on-light/baseline-2` | `#333333` | 1.33:1 | ❌ POOR |
| `data-vis/border/on-light/gridline` | `#333333` | 1.33:1 | ❌ POOR |
| `data-vis/border/on-light/indicator` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `data-vis/surface/primary` | `#000000` | 1.25:1 | ❌ POOR |
| `data-vis/surface/secondary` | `#000000` | 1.25:1 | ❌ POOR |
| `divider/border/break` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `divider/border/section` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `divider/border/subsection` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `divider/border/subsectionInset` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `elevation/border` | `#767676` | 3.71:1 | ✅ OK |
| `form/background/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/background/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/background/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/border/active` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/border/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/border/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `form/border/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/background/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `primary/border/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `scrollbar/background` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/background/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/background/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/background/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/background/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/border/default` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/border/disabled` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/border/hover` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `secondary/border/pressed` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `table/border` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `table/column/background` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `table/header/background` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `tabs/background` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tabs/overflow-background` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tabs/overflow-border` | `#474747` | 1.81:1 | ❌ POOR |
| `tabs/standard-border` | `#474747` | 1.81:1 | ❌ POOR |
| `tertiary/background/active` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tertiary/background/default` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tertiary/background/disabled` | `#333333` | 1.33:1 | ❌ POOR |
| `tertiary/background/hover` | `#474747` | 1.81:1 | ❌ POOR |
| `tertiary/background/pressed` | `#1D1D1D` | 1.0:1 | ❌ POOR |
| `tertiary/border/default` | `#474747` | 1.81:1 | ❌ POOR |
| `tertiary/border/disabled` | `#333333` | 1.33:1 | ❌ POOR |
| `timer/background` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `tooltip/background` | `#FFFFFF` | 16.86:1 | ✅ OK |
| `tooltip/border` | `#FFFFFF` | 16.86:1 | ✅ OK |