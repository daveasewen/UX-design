# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 119 snippet(s) (95 verified-bespoke). Library glyphs indexed: 746.

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
| 9 | App-shell-multi-column | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 10 | App-shell-side-nav | 12 | 12 | 0 | 0 | yes | ✅ verified |
| 11 | App-shell-top-nav | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 12 | Avatar-group | 1 | 1 | 0 | 0 | — | ✅ verified |
| 13 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 14 | Back-to-top | 1 | 1 | 0 | 0 | — | ✅ verified |
| 15 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 16 | Banner | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 17 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 18 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 19 | Calendar | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 20 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 21 | Carousel | 2 | 2 | 0 | 0 | — | ✅ verified |
| 22 | Cascader | 2 | 1 | 1 | 0 | yes | ✅ verified · 1 bespoke |
| 23 | Chart-bar | 15 | 15 | 0 | 0 | — | ✅ verified |
| 24 | Chart-boxplot | 3 | 3 | 0 | 0 | — | ✅ verified |
| 25 | Chart-bullet | 3 | 3 | 0 | 0 | — | ✅ verified |
| 26 | Chart-butterfly-h | 3 | 3 | 0 | 0 | — | ✅ verified |
| 27 | Chart-butterfly-v | 3 | 3 | 0 | 0 | — | ✅ verified |
| 28 | Chart-candlestick | 3 | 3 | 0 | 0 | — | ✅ verified |
| 29 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 30 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 31 | Chart-histogram | 3 | 3 | 0 | 0 | — | ✅ verified |
| 32 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 33 | Chart-pie | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 34 | Chart-scatter | 2 | 2 | 0 | 0 | — | ✅ verified |
| 35 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 36 | Chart-stacked-area | 6 | 3 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 37 | Combobox | 15 | 4 | 11 | 0 | yes | ✅ verified · 11 bespoke |
| 38 | Command-palette | 6 | 6 | 0 | 0 | — | ✅ verified |
| 39 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 40 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 41 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 42 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 43 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 44 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 45 | Document-row | 4 | 4 | 0 | 0 | — | ✅ verified |
| 46 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 47 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 48 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 49 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 50 | Fab | 1 | 1 | 0 | 0 | — | ✅ verified |
| 51 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 52 | Filter-toolbar-bar | 9 | 3 | 6 | 0 | — | ✅ verified · 6 bespoke |
| 53 | Footer | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 54 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 55 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 56 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 57 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 58 | Image-block | 1 | 1 | 0 | 0 | — | ✅ verified |
| 59 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 60 | Kpi-tile | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 61 | Layout-utilities | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 62 | Limits-meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 63 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 64 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 65 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 66 | Meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 67 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 68 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 69 | Multi-select | 13 | 5 | 8 | 0 | yes | ✅ verified · 8 bespoke |
| 70 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 71 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 72 | Page-header-lockup | 1 | 1 | 0 | 0 | — | ✅ verified |
| 73 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 74 | Payment-card-visual | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 75 | Popconfirm | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 76 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 77 | Progress-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 78 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 79 | Qr-code | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 80 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 81 | Range-slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 82 | Rating | 1 | 1 | 0 | 0 | — | ✅ verified |
| 83 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 84 | Runway-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 85 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 86 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 87 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 88 | Selection-controls | 8 | 0 | 8 | 0 | — | ✅ verified · 8 bespoke |
| 89 | Sidebar-nav | 9 | 9 | 0 | 0 | — | ✅ verified |
| 90 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 91 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 92 | Split-button | 4 | 4 | 0 | 0 | — | ✅ verified |
| 93 | Splitter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 94 | Standing-order-mandate-row | 2 | 2 | 0 | 0 | — | ✅ verified |
| 95 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 96 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 97 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 98 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 99 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 100 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 101 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 102 | Tags-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 103 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 104 | Template-auth | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 105 | Template-create-edit | 7 | 7 | 0 | 0 | yes | ✅ verified |
| 106 | Template-dashboard | 13 | 13 | 0 | 0 | yes | ✅ verified |
| 107 | Template-detail | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 108 | Template-list-index | 25 | 13 | 12 | 0 | yes | ✅ verified · 12 bespoke |
| 109 | Template-wizard | 7 | 7 | 0 | 0 | yes | ✅ verified |
| 110 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 111 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 112 | Timeline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 113 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 114 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 115 | Transaction-row | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 116 | Transfer-list | 11 | 4 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 117 | Tree | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 118 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 119 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
