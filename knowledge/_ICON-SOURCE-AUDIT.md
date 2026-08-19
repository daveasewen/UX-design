# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 85 snippet(s) (69 verified-bespoke). Library glyphs indexed: 746.

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
| 11 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 12 | Banner | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 13 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 14 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 15 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 16 | Chart-bar | 15 | 15 | 0 | 0 | — | ✅ verified |
| 17 | Chart-boxplot | 3 | 3 | 0 | 0 | — | ✅ verified |
| 18 | Chart-bullet | 3 | 3 | 0 | 0 | — | ✅ verified |
| 19 | Chart-butterfly-h | 3 | 3 | 0 | 0 | — | ✅ verified |
| 20 | Chart-butterfly-v | 3 | 3 | 0 | 0 | — | ✅ verified |
| 21 | Chart-candlestick | 3 | 3 | 0 | 0 | — | ✅ verified |
| 22 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 23 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 24 | Chart-histogram | 3 | 3 | 0 | 0 | — | ✅ verified |
| 25 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 26 | Chart-pie | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 27 | Chart-scatter | 2 | 2 | 0 | 0 | — | ✅ verified |
| 28 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 29 | Chart-stacked-area | 6 | 3 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 30 | Combobox | 15 | 4 | 11 | 0 | yes | ✅ verified · 11 bespoke |
| 31 | Command-palette | 6 | 6 | 0 | 0 | — | ✅ verified |
| 32 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 33 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 34 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 35 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 36 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 37 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 38 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 39 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 40 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 41 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 42 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 43 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 44 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 45 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 46 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 47 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 48 | Kpi-tile | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 49 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 50 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 51 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 52 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 53 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 54 | Multi-select | 13 | 5 | 8 | 0 | yes | ✅ verified · 8 bespoke |
| 55 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 56 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 57 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 58 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 59 | Progress-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 60 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 61 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 62 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 63 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 64 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 65 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 66 | Selection-controls | 8 | 0 | 8 | 0 | — | ✅ verified · 8 bespoke |
| 67 | Sidebar-nav | 9 | 9 | 0 | 0 | — | ✅ verified |
| 68 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 69 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 70 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 71 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 72 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 73 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 74 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 75 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 76 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 77 | Tags-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 78 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 79 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 80 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 81 | Timeline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 82 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 83 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 84 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 85 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
