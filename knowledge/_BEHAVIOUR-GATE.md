# Behaviour-contract gate (ADR-0015)

Per source ≤16KB (legibility) · per member page ≤34KB (page weight) · no polling/network · ONE rAF-debounced resize per GROUP · DEF-003 boundary · members carry no external script src.

**Unit: CODE-ONLY bytes** — `//` and `/* */` comments and blank lines are stripped at measure time (ADR-0015 Amendment 3, Dave #250 2026-09-06, option (e)). Source files are never modified. The caps did not move. Page figures sum each member's `consumes` declaration (Amendment 2), so the group's number is the WORST member page. A behaviour the registry marks `shared: true` (the engine core `dv-render`) is priced ONCE PER PAGE and excluded from member figures (Amendment 4, Dave #260 2026-09-08, `s260-D1`).

- **dataviz/dv-behaviour** — `knowledge/canon/dv-behaviour.js` · **13590 code-only bytes** (13.3 KB of 16 KB) · 24503 raw, 10913 comment/blank · 18 member(s)
- **dataviz/dv-legend** — `knowledge/canon/dv-legend.js` · **7760 code-only bytes** (7.6 KB of 16 KB) · 15255 raw, 7495 comment/blank · 18 member(s)
- **dataviz/dv-donut-sweep** — `knowledge/canon/dv-donut-sweep.js` · **3889 code-only bytes** (3.8 KB of 16 KB) · 5511 raw, 1622 comment/blank · 18 member(s)
- **dataviz/dp08-anchor** — `knowledge/canon/dp08-anchor.js` · **1821 code-only bytes** (1.8 KB of 16 KB) · 3884 raw, 2063 comment/blank · 18 member(s)
- **dataviz/dv-render** — `knowledge/canon/dv-render.js` · **11056 code-only bytes** (10.8 KB of 16 KB) · 24127 raw, 13071 comment/blank · 18 member(s)
- **dataviz/dv-render-bar** — `knowledge/canon/dv-render-bar.js` · **4613 code-only bytes** (4.5 KB of 16 KB) · 9262 raw, 4649 comment/blank · 18 member(s)
- **dataviz/dv-render-line** — `knowledge/canon/dv-render-line.js` · **3648 code-only bytes** (3.6 KB of 16 KB) · 9795 raw, 6147 comment/blank · 18 member(s)
- **dataviz/dv-render-stacked-area** — `knowledge/canon/dv-render-stacked-area.js` · **4583 code-only bytes** (4.5 KB of 16 KB) · 12253 raw, 7670 comment/blank · 18 member(s)
- **dataviz/dv-render-donut** — `knowledge/canon/dv-render-donut.js` · **4185 code-only bytes** (4.1 KB of 16 KB) · 11670 raw, 7485 comment/blank · 18 member(s)
- **dataviz/dv-render-sparkline** — `knowledge/canon/dv-render-sparkline.js` · **3235 code-only bytes** (3.2 KB of 16 KB) · 9852 raw, 6617 comment/blank · 18 member(s)
- **dataviz/dv-render-combo** — `knowledge/canon/dv-render-combo.js` · **5198 code-only bytes** (5.1 KB of 16 KB) · 11625 raw, 6427 comment/blank · 18 member(s)
- **dataviz/dv-render-scatter** — `knowledge/canon/dv-render-scatter.js` · **4148 code-only bytes** (4.1 KB of 16 KB) · 10020 raw, 5872 comment/blank · 18 member(s)
- **dataviz/dv-render-histogram** — `knowledge/canon/dv-render-histogram.js` · **2218 code-only bytes** (2.2 KB of 16 KB) · 6670 raw, 4452 comment/blank · 18 member(s)
- **dataviz/dv-render-boxplot** — `knowledge/canon/dv-render-boxplot.js` · **4336 code-only bytes** (4.2 KB of 16 KB) · 9882 raw, 5546 comment/blank · 18 member(s)
- **dataviz/dv-render-bullet** — `knowledge/canon/dv-render-bullet.js` · **4443 code-only bytes** (4.3 KB of 16 KB) · 10582 raw, 6139 comment/blank · 18 member(s)
- **dataviz/dv-render-candlestick** — `knowledge/canon/dv-render-candlestick.js` · **4872 code-only bytes** (4.8 KB of 16 KB) · 10765 raw, 5893 comment/blank · 18 member(s)
- **dataviz/dv-render-butterfly** — `knowledge/canon/dv-render-butterfly.js` · **4711 code-only bytes** (4.6 KB of 16 KB) · 10795 raw, 6084 comment/blank · 18 member(s)
- **click-or-tab/click-or-tab** — `knowledge/canon/click-or-tab.js` · **493 code-only bytes** (0.5 KB of 16 KB) · 1892 raw, 1399 comment/blank · 30 member(s)

- **click-or-tab — page budget (worst member):** 493 code-only bytes (0.5 KB of 34 KB, 1%) across 1 source(s)
    - `Amount-input` — 493 bytes · consumes click-or-tab
    - `Calendar` — 493 bytes · consumes click-or-tab
    - `Combobox` — 493 bytes · consumes click-or-tab
    - `Data-grid` — 493 bytes · consumes click-or-tab
    - `Date-picker` — 493 bytes · consumes click-or-tab
    - `Date-range-picker` — 493 bytes · consumes click-or-tab
    - `File-upload` — 493 bytes · consumes click-or-tab
    - `Filter-toolbar-bar` — 493 bytes · consumes click-or-tab
    - `Form-layout` — 493 bytes · consumes click-or-tab
    - `Input-fields` — 493 bytes · consumes click-or-tab
    - `Multi-select` — 493 bytes · consumes click-or-tab
    - `Secure-entry` — 493 bytes · consumes click-or-tab
    - `Stepper` — 493 bytes · consumes click-or-tab
    - `Tags-input` — 493 bytes · consumes click-or-tab
    - `Template-auth` — 493 bytes · consumes click-or-tab
    - `Template-confirmation` — 493 bytes · consumes click-or-tab
    - `Template-create-edit` — 493 bytes · consumes click-or-tab
    - `Template-dashboard` — 493 bytes · consumes click-or-tab
    - `Template-dashboard-bento` — 493 bytes · consumes click-or-tab
    - `Template-detail` — 493 bytes · consumes click-or-tab
    - `Template-empty` — 493 bytes · consumes click-or-tab
    - `Template-error` — 493 bytes · consumes click-or-tab
    - `Template-list-index` — 493 bytes · consumes click-or-tab
    - `Template-report` — 493 bytes · consumes click-or-tab
    - `Template-settings` — 493 bytes · consumes click-or-tab
    - `Template-wizard` — 493 bytes · consumes click-or-tab
    - `Textarea` — 493 bytes · consumes click-or-tab
    - `Time-picker` — 493 bytes · consumes click-or-tab
    - `Tree` — 493 bytes · consumes click-or-tab
    - `Video-player` — 493 bytes · consumes click-or-tab
- **dataviz — page budget (worst member):** 34809 code-only bytes (34.0 KB of 34 KB, 100%) across 17 source(s)
    - shared, priced ONCE PER PAGE (s260-D1, A4): dv-render — 11056 code-only bytes, NOT charged to member figures
    - `Chart-combo` — 34809 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-bar, dv-render-line, dv-render-combo
    - `Chart-donut` — 29424 bytes · consumes dv-behaviour, dv-legend, dv-donut-sweep, dv-render, dv-render-donut
    - `Chart-butterfly-h` — 26061 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-butterfly
    - `Chart-butterfly-v` — 26061 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-butterfly
    - `Chart-bar` — 25963 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-bar
    - `Chart-stacked-area` — 25933 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-stacked-area
    - `Chart-pie` — 25535 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-donut
    - `Chart-scatter` — 25498 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-scatter
    - `Chart-line` — 24998 bytes · consumes dv-behaviour, dv-legend, dv-render, dv-render-line
    - `Template-report` — 21851 bytes · consumes dv-behaviour, dv-render, dv-render-bar, dv-render-line
    - `Chart-candlestick` — 18462 bytes · consumes dv-behaviour, dv-render, dv-render-candlestick
    - `Template-dashboard` — 18203 bytes · consumes dv-behaviour, dv-render, dv-render-bar
    - `Chart-bullet` — 18033 bytes · consumes dv-behaviour, dv-render, dv-render-bullet
    - `Chart-boxplot` — 17926 bytes · consumes dv-behaviour, dv-render, dv-render-boxplot
    - `Chart-sparkline` — 16825 bytes · consumes dv-behaviour, dv-render, dv-render-sparkline
    - `Chart-histogram` — 15808 bytes · consumes dv-behaviour, dv-render, dv-render-histogram
    - `Template-dashboard-bento` — 15411 bytes · consumes dv-behaviour, dp08-anchor
    - `Legend` — 7760 bytes · consumes dv-legend

## ✓ PASS — every behaviour source honours the contract.
