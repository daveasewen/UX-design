# Behaviour-contract gate (ADR-0015)

Per source ≤16KB (legibility) · per member page ≤34KB (page weight) · no polling/network · ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.

**Unit: CODE-ONLY bytes** — `//` and `/* */` comments and blank lines are stripped at measure time (ADR-0015 Amendment 3, Dave #250 2026-09-06, option (e)). Source files are never modified. The caps did not move. Page figures sum each member's `consumes` declaration (Amendment 2), so the group's number is the WORST member page.

- **dataviz/dv-behaviour** — `knowledge/canon/dv-behaviour.js` · **13048 code-only bytes** (12.7 KB of 16 KB) · 19768 raw, 6720 comment/blank · 15 member(s)
- **dataviz/dv-legend** — `knowledge/canon/dv-legend.js` · **7734 code-only bytes** (7.6 KB of 16 KB) · 15131 raw, 7397 comment/blank · 15 member(s)
- **dataviz/dv-donut-sweep** — `knowledge/canon/dv-donut-sweep.js` · **3889 code-only bytes** (3.8 KB of 16 KB) · 5511 raw, 1622 comment/blank · 15 member(s)
- **dataviz/dp08-anchor** — `knowledge/canon/dp08-anchor.js` · **1821 code-only bytes** (1.8 KB of 16 KB) · 3884 raw, 2063 comment/blank · 15 member(s)

- **dataviz — page budget (worst member):** 24671 code-only bytes (24.1 KB of 34 KB, 71%) across 4 source(s)
    - `Chart-donut` — 24671 bytes · consumes dv-behaviour, dv-legend, dv-donut-sweep
    - `Chart-bar` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-butterfly-h` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-butterfly-v` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-combo` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-line` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-pie` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-scatter` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-stacked-area` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Template-dashboard-bento` — 14869 bytes · consumes dv-behaviour, dp08-anchor
    - `Chart-boxplot` — 13048 bytes · consumes dv-behaviour
    - `Chart-bullet` — 13048 bytes · consumes dv-behaviour
    - `Chart-candlestick` — 13048 bytes · consumes dv-behaviour
    - `Chart-histogram` — 13048 bytes · consumes dv-behaviour
    - `Chart-sparkline` — 13048 bytes · consumes dv-behaviour

## ✓ PASS — every behaviour source honours the contract.
