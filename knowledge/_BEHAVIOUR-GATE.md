# Behaviour-contract gate (ADR-0015)

Per source ≤16KB (legibility) · per member page ≤34KB (page weight) · no polling/network · ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.

**Unit: CODE-ONLY bytes** — `//` and `/* */` comments and blank lines are stripped at measure time (ADR-0015 Amendment 3, Dave #250 2026-09-06, option (e)). Source files are never modified. The caps did not move. Page figures sum each member's `consumes` declaration (Amendment 2), so the group's number is the WORST member page. A behaviour the registry marks `shared: true` (the engine core `dv-render`) is priced ONCE PER PAGE and excluded from member figures (Amendment 4, Dave #260 2026-09-08, `s260-D1`).

- **dataviz/dv-behaviour** — `knowledge/canon/dv-behaviour.js` · **13048 code-only bytes** (12.7 KB of 16 KB) · 19768 raw, 6720 comment/blank · 16 member(s)
- **dataviz/dv-legend** — `knowledge/canon/dv-legend.js` · **7734 code-only bytes** (7.6 KB of 16 KB) · 15131 raw, 7397 comment/blank · 16 member(s)
- **dataviz/dv-donut-sweep** — `knowledge/canon/dv-donut-sweep.js` · **3889 code-only bytes** (3.8 KB of 16 KB) · 5511 raw, 1622 comment/blank · 16 member(s)
- **dataviz/dp08-anchor** — `knowledge/canon/dp08-anchor.js` · **1821 code-only bytes** (1.8 KB of 16 KB) · 3884 raw, 2063 comment/blank · 16 member(s)
- **dataviz/dv-render** — `knowledge/canon/dv-render.js` · **9502 code-only bytes** (9.3 KB of 16 KB) · 20148 raw, 10646 comment/blank · 16 member(s)
- **dataviz/dv-render-bar** — `knowledge/canon/dv-render-bar.js` · **4613 code-only bytes** (4.5 KB of 16 KB) · 9262 raw, 4649 comment/blank · 16 member(s)
- **dataviz/dv-render-line** — `knowledge/canon/dv-render-line.js` · **3616 code-only bytes** (3.5 KB of 16 KB) · 9187 raw, 5571 comment/blank · 16 member(s)
- **dataviz/dv-render-stacked-area** — `knowledge/canon/dv-render-stacked-area.js` · **4248 code-only bytes** (4.1 KB of 16 KB) · 10285 raw, 6037 comment/blank · 16 member(s)
- **dataviz/dv-render-donut** — `knowledge/canon/dv-render-donut.js` · **3875 code-only bytes** (3.8 KB of 16 KB) · 9731 raw, 5856 comment/blank · 16 member(s)
- **dataviz/dv-render-sparkline** — `knowledge/canon/dv-render-sparkline.js` · **3235 code-only bytes** (3.2 KB of 16 KB) · 9852 raw, 6617 comment/blank · 16 member(s)
- **dataviz/dv-render-combo** — `knowledge/canon/dv-render-combo.js` · **5198 code-only bytes** (5.1 KB of 16 KB) · 11625 raw, 6427 comment/blank · 16 member(s)
- **dataviz/dv-render-scatter** — `knowledge/canon/dv-render-scatter.js` · **4148 code-only bytes** (4.1 KB of 16 KB) · 10020 raw, 5872 comment/blank · 16 member(s)
- **dataviz/dv-render-histogram** — `knowledge/canon/dv-render-histogram.js` · **2218 code-only bytes** (2.2 KB of 16 KB) · 6670 raw, 4452 comment/blank · 16 member(s)
- **dataviz/dv-render-boxplot** — `knowledge/canon/dv-render-boxplot.js` · **4336 code-only bytes** (4.2 KB of 16 KB) · 9882 raw, 5546 comment/blank · 16 member(s)
- **dataviz/dv-render-bullet** — `knowledge/canon/dv-render-bullet.js` · **4443 code-only bytes** (4.3 KB of 16 KB) · 10582 raw, 6139 comment/blank · 16 member(s)
- **dataviz/dv-render-candlestick** — `knowledge/canon/dv-render-candlestick.js` · **4872 code-only bytes** (4.8 KB of 16 KB) · 10765 raw, 5893 comment/blank · 16 member(s)
- **dataviz/dv-render-butterfly** — `knowledge/canon/dv-render-butterfly.js` · **4711 code-only bytes** (4.6 KB of 16 KB) · 10795 raw, 6084 comment/blank · 16 member(s)

- **dataviz — page budget (worst member):** 34209 code-only bytes (33.4 KB of 34 KB, 98%) across 17 source(s)
    - shared, priced ONCE PER PAGE (s260-D1, A4): dv-render — 9502 code-only bytes, NOT charged to member figures
    - `Chart-combo` — 34209 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-bar, dv-render-line, dv-render-combo
    - `Chart-donut` — 28546 bytes · consumes dv-behaviour, dv-legend, dv-donut-sweep, dv-render, dv-render-donut
    - `Chart-butterfly-h` — 25493 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-butterfly
    - `Chart-butterfly-v` — 25493 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-butterfly
    - `Chart-bar` — 25395 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-bar
    - `Chart-stacked-area` — 25030 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-stacked-area
    - `Chart-scatter` — 24930 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-scatter
    - `Chart-pie` — 24657 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-donut
    - `Chart-line` — 24398 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-line
    - `Chart-candlestick` — 17920 bytes · consumes dv-behaviour, dv-render, dv-render-candlestick
    - `Chart-bullet` — 17491 bytes · consumes dv-behaviour, dv-render, dv-render-bullet
    - `Chart-boxplot` — 17384 bytes · consumes dv-behaviour, dv-render, dv-render-boxplot
    - `Chart-sparkline` — 16283 bytes · consumes dv-behaviour, dv-render, dv-render-sparkline
    - `Chart-histogram` — 15266 bytes · consumes dv-behaviour, dv-render, dv-render-histogram
    - `Template-dashboard-bento` — 14869 bytes · consumes dv-behaviour, dp08-anchor
    - `Legend` — 7734 bytes · consumes dv-legend

## ✓ PASS — every behaviour source honours the contract.
