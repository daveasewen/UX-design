# Behaviour-contract gate (ADR-0015)

Per source ≤16KB (legibility) · per member page ≤34KB (page weight) · no polling/network · ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.

**Unit: CODE-ONLY bytes** — `//` and `/* */` comments and blank lines are stripped at measure time (ADR-0015 Amendment 3, Dave #250 2026-09-06, option (e)). Source files are never modified. The caps did not move. Page figures sum each member's `consumes` declaration (Amendment 2), so the group's number is the WORST member page.

- **dataviz/dv-behaviour** — `knowledge/canon/dv-behaviour.js` · **13048 code-only bytes** (12.7 KB of 16 KB) · 19768 raw, 6720 comment/blank · 15 member(s)
- **dataviz/dv-legend** — `knowledge/canon/dv-legend.js` · **7734 code-only bytes** (7.6 KB of 16 KB) · 15131 raw, 7397 comment/blank · 15 member(s)
- **dataviz/dv-donut-sweep** — `knowledge/canon/dv-donut-sweep.js` · **3889 code-only bytes** (3.8 KB of 16 KB) · 5511 raw, 1622 comment/blank · 15 member(s)
- **dataviz/dp08-anchor** — `knowledge/canon/dp08-anchor.js` · **1821 code-only bytes** (1.8 KB of 16 KB) · 3884 raw, 2063 comment/blank · 15 member(s)
- **dataviz/dv-render** — `knowledge/canon/dv-render.js` · **9309 code-only bytes** (9.1 KB of 16 KB) · 18022 raw, 8713 comment/blank · 15 member(s)
- **dataviz/dv-render-bar** — `knowledge/canon/dv-render-bar.js` · **4613 code-only bytes** (4.5 KB of 16 KB) · 9262 raw, 4649 comment/blank · 15 member(s)
- **dataviz/dv-render-line** — `knowledge/canon/dv-render-line.js` · **374 code-only bytes** (0.4 KB of 16 KB) · 2235 raw, 1861 comment/blank · 15 member(s)
- **dataviz/dv-render-stacked-area** — `knowledge/canon/dv-render-stacked-area.js` · **385 code-only bytes** (0.4 KB of 16 KB) · 2269 raw, 1884 comment/blank · 15 member(s)
- **dataviz/dv-render-donut** — `knowledge/canon/dv-render-donut.js` · **356 code-only bytes** (0.3 KB of 16 KB) · 2219 raw, 1863 comment/blank · 15 member(s)
- **dataviz/dv-render-sparkline** — `knowledge/canon/dv-render-sparkline.js` · **410 code-only bytes** (0.4 KB of 16 KB) · 2227 raw, 1817 comment/blank · 15 member(s)
- **dataviz/dv-render-combo** — `knowledge/canon/dv-render-combo.js` · **336 code-only bytes** (0.3 KB of 16 KB) · 2185 raw, 1849 comment/blank · 15 member(s)

- **dataviz — page budget (worst member):** 35414 code-only bytes (34.6 KB of 34 KB, 102%) across 11 source(s)
    - `Chart-combo` — 35414 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-bar, dv-render-line, dv-render-combo
    - `Chart-bar` — 34704 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-bar
    - `Chart-donut` — 34336 bytes · consumes dv-behaviour, dv-legend, dv-donut-sweep, dv-render, dv-render-donut
    - `Chart-stacked-area` — 30476 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-stacked-area
    - `Chart-line` — 30465 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-line
    - `Chart-sparkline` — 22767 bytes · consumes dv-behaviour, dv-render, dv-render-sparkline
    - `Chart-butterfly-h` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-butterfly-v` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-pie` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Chart-scatter` — 20782 bytes · consumes dv-behaviour, dv-legend
    - `Template-dashboard-bento` — 14869 bytes · consumes dv-behaviour, dp08-anchor
    - `Chart-boxplot` — 13048 bytes · consumes dv-behaviour
    - `Chart-bullet` — 13048 bytes · consumes dv-behaviour
    - `Chart-candlestick` — 13048 bytes · consumes dv-behaviour
    - `Chart-histogram` — 13048 bytes · consumes dv-behaviour

## ✗ FAILURES
- dataviz (page budget): worst member page Chart-combo loads 35414 code-only bytes > 34816 (ADR-0015 page budget — splitting a source does not buy headroom)
