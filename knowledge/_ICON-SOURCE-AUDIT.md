# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 135 snippet(s) (97 verified-bespoke). Library glyphs indexed: 750.

| # | Snippet | paths | library | bespoke | UNKNOWN | declares | status |
|---|---------|------:|--------:|--------:|--------:|:--------:|--------|
| 1 | Accordion | 2 | 2 | 0 | 0 | — | ✅ verified |
| 2 | Account-card | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 3 | Account-selector | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 4 | Action-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 5 | Alert | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 6 | Amount-display | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 7 | Amount-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 8 | Anchor-nav | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 9 | App-shell-doormat | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 10 | App-shell-focused | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 11 | App-shell-multi-column | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 12 | App-shell-nav-rail | 7 | 7 | 0 | 0 | — | ✅ verified |
| 13 | App-shell-side-nav | 12 | 12 | 0 | 0 | yes | ✅ verified |
| 14 | App-shell-split | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 15 | App-shell-top-nav | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 16 | Avatar-group | 1 | 1 | 0 | 0 | — | ✅ verified |
| 17 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 18 | Back-to-top | 1 | 1 | 0 | 0 | — | ✅ verified |
| 19 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 20 | Banner | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 21 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 22 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 23 | CTA-lockup | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 24 | Calendar | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 25 | Card-header-lockup | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 26 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 27 | Carousel | 2 | 2 | 0 | 0 | — | ✅ verified |
| 28 | Cascader | 2 | 1 | 1 | 0 | yes | ✅ verified · 1 bespoke |
| 29 | Chart-bar | 15 | 15 | 0 | 0 | — | ✅ verified |
| 30 | Chart-boxplot | 3 | 3 | 0 | 0 | — | ✅ verified |
| 31 | Chart-bullet | 3 | 3 | 0 | 0 | — | ✅ verified |
| 32 | Chart-butterfly-h | 3 | 3 | 0 | 0 | — | ✅ verified |
| 33 | Chart-butterfly-v | 3 | 3 | 0 | 0 | — | ✅ verified |
| 34 | Chart-candlestick | 3 | 3 | 0 | 0 | — | ✅ verified |
| 35 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 36 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 37 | Chart-histogram | 3 | 3 | 0 | 0 | — | ✅ verified |
| 38 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 39 | Chart-pie | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 40 | Chart-scatter | 2 | 2 | 0 | 0 | — | ✅ verified |
| 41 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 42 | Chart-stacked-area | 6 | 3 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 43 | Combobox | 15 | 4 | 11 | 0 | yes | ✅ verified · 11 bespoke |
| 44 | Command-palette | 6 | 6 | 0 | 0 | — | ✅ verified |
| 45 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 46 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 47 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 48 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 49 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 50 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 51 | Document-row | 4 | 4 | 0 | 0 | — | ✅ verified |
| 52 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 53 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 54 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 55 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 56 | Fab | 1 | 1 | 0 | 0 | — | ✅ verified |
| 57 | Feature-grid-lockup | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 58 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 59 | Filter-toolbar-bar | 9 | 3 | 6 | 0 | — | ✅ verified · 6 bespoke |
| 60 | Footer-doormat-lockup | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 61 | Footer | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 62 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 63 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 64 | Hero-variants | 3 | 3 | 0 | 0 | — | ✅ verified |
| 65 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 66 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 67 | Image-block | 1 | 1 | 0 | 0 | — | ✅ verified |
| 68 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 69 | Kpi-tile | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 70 | Layout-utilities | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 71 | Limits-meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 72 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 73 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 74 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 75 | Meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 76 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 77 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 78 | Multi-select | 13 | 5 | 8 | 0 | yes | ✅ verified · 8 bespoke |
| 79 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 80 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 81 | Page-header-lockup | 1 | 1 | 0 | 0 | — | ✅ verified |
| 82 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 83 | Payment-card-visual | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 84 | Popconfirm | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 85 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 86 | Progress-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 87 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 88 | Qr-code | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 89 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 90 | Range-slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 91 | Rating | 1 | 1 | 0 | 0 | — | ✅ verified |
| 92 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 93 | Runway-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 94 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 95 | Section-heading-lockup | 1 | 1 | 0 | 0 | — | ✅ verified |
| 96 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 97 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 98 | Selection-controls | 8 | 0 | 8 | 0 | — | ✅ verified · 8 bespoke |
| 99 | Sidebar-nav | 9 | 9 | 0 | 0 | — | ✅ verified |
| 100 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 101 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 102 | Split-button | 4 | 4 | 0 | 0 | — | ✅ verified |
| 103 | Splitter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 104 | Standing-order-mandate-row | 2 | 2 | 0 | 0 | — | ✅ verified |
| 105 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 106 | Stats-band-lockup | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 107 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 108 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 109 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 110 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 111 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 112 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 113 | Tags-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 114 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 115 | Template-auth | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 116 | Template-confirmation | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 117 | Template-create-edit | 7 | 7 | 0 | 0 | yes | ✅ verified |
| 118 | Template-dashboard | 13 | 13 | 0 | 0 | yes | ✅ verified |
| 119 | Template-detail | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 120 | Template-empty | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 121 | Template-error | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 122 | Template-list-index | 25 | 13 | 12 | 0 | yes | ✅ verified · 12 bespoke |
| 123 | Template-report | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 124 | Template-settings | 6 | 4 | 2 | 0 | yes | ✅ verified · 2 bespoke |
| 125 | Template-wizard | 7 | 7 | 0 | 0 | yes | ✅ verified |
| 126 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 127 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 128 | Timeline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 129 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 130 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 131 | Transaction-row | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 132 | Transfer-list | 11 | 4 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 133 | Tree | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 134 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 135 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
