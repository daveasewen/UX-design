# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 75 snippet(s) (50 verified-bespoke). Library glyphs indexed: 746.

| # | Snippet | paths | library | bespoke | UNKNOWN | declares | status |
|---|---------|------:|--------:|--------:|--------:|:--------:|--------|
| 1 | Accordion | 2 | 2 | 0 | 0 | — | ✅ verified |
| 2 | Account-card | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 3 | Account-selector | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 4 | Action-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 5 | Alert | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 6 | Amount-display | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 7 | Amount-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 8 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 9 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 10 | Banner | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 11 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 12 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 13 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 14 | Chart-bar | 15 | 15 | 0 | 0 | — | ✅ verified |
| 15 | Chart-boxplot | 3 | 3 | 0 | 0 | — | ✅ verified |
| 16 | Chart-bullet | 3 | 3 | 0 | 0 | — | ✅ verified |
| 17 | Chart-butterfly-h | 3 | 3 | 0 | 0 | — | ✅ verified |
| 18 | Chart-butterfly-v | 3 | 3 | 0 | 0 | — | ✅ verified |
| 19 | Chart-candlestick | 3 | 3 | 0 | 0 | — | ✅ verified |
| 20 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 21 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 22 | Chart-histogram | 3 | 3 | 0 | 0 | — | ✅ verified |
| 23 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 24 | Chart-pie | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 25 | Chart-scatter | 2 | 2 | 0 | 0 | — | ✅ verified |
| 26 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 27 | Chart-stacked-area | 6 | 3 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 28 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 29 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 30 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 31 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 32 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 33 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 34 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 35 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 36 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 37 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 38 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 39 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 40 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 41 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 42 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 43 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 44 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 45 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 46 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 47 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 48 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 49 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 50 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 51 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 52 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 53 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 54 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 55 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 56 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 57 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 58 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 59 | Selection-controls | 8 | 0 | 8 | 0 | — | ✅ verified · 8 bespoke |
| 60 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 61 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 62 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 63 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 64 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 65 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 66 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 67 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 68 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 69 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 70 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 71 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 72 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 73 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 74 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 75 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
