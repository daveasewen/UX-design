# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 100 snippet(s) (76 verified-bespoke). Library glyphs indexed: 746.

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
| 9 | Avatar-group | 1 | 1 | 0 | 0 | — | ✅ verified |
| 10 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 11 | Back-to-top | 1 | 1 | 0 | 0 | — | ✅ verified |
| 12 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 13 | Banner | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 14 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 15 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 16 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 17 | Chart-bar | 15 | 15 | 0 | 0 | — | ✅ verified |
| 18 | Chart-boxplot | 3 | 3 | 0 | 0 | — | ✅ verified |
| 19 | Chart-bullet | 3 | 3 | 0 | 0 | — | ✅ verified |
| 20 | Chart-butterfly-h | 3 | 3 | 0 | 0 | — | ✅ verified |
| 21 | Chart-butterfly-v | 3 | 3 | 0 | 0 | — | ✅ verified |
| 22 | Chart-candlestick | 3 | 3 | 0 | 0 | — | ✅ verified |
| 23 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 24 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 25 | Chart-histogram | 3 | 3 | 0 | 0 | — | ✅ verified |
| 26 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 27 | Chart-pie | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 28 | Chart-scatter | 2 | 2 | 0 | 0 | — | ✅ verified |
| 29 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 30 | Chart-stacked-area | 6 | 3 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 31 | Combobox | 15 | 4 | 11 | 0 | yes | ✅ verified · 11 bespoke |
| 32 | Command-palette | 6 | 6 | 0 | 0 | — | ✅ verified |
| 33 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 34 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 35 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 36 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 37 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 38 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 39 | Document-row | 4 | 4 | 0 | 0 | — | ✅ verified |
| 40 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 41 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 42 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 43 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 44 | Fab | 1 | 1 | 0 | 0 | — | ✅ verified |
| 45 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 46 | Footer | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 47 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 48 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 49 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 50 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 51 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 52 | Kpi-tile | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 53 | Layout-utilities | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 54 | Limits-meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 55 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 56 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 57 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 58 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 59 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 60 | Multi-select | 13 | 5 | 8 | 0 | yes | ✅ verified · 8 bespoke |
| 61 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 62 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 63 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 64 | Payment-card-visual | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 65 | Popconfirm | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 66 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 67 | Progress-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 68 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 69 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 70 | Range-slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 71 | Rating | 1 | 1 | 0 | 0 | — | ✅ verified |
| 72 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 73 | Runway-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 74 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 75 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 76 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 77 | Selection-controls | 8 | 0 | 8 | 0 | — | ✅ verified · 8 bespoke |
| 78 | Sidebar-nav | 9 | 9 | 0 | 0 | — | ✅ verified |
| 79 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 80 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 81 | Split-button | 4 | 4 | 0 | 0 | — | ✅ verified |
| 82 | Standing-order-mandate-row | 2 | 2 | 0 | 0 | — | ✅ verified |
| 83 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 84 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 85 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 86 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 87 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 88 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 89 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 90 | Tags-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 91 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 92 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 93 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 94 | Timeline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 95 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 96 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 97 | Transaction-row | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 98 | Transfer-list | 11 | 4 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 99 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 100 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
