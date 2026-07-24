# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 67 snippet(s) (36 verified-bespoke). Library glyphs indexed: 746.

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
| 15 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 16 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 17 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 18 | Chart-scatter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 19 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 20 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 21 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 22 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 23 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 24 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 25 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 26 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 27 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 28 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 29 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 30 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 31 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 32 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 33 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 34 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 35 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 36 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 37 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 38 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 39 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 40 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 41 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 42 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 43 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 44 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 45 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 46 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 47 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 48 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 49 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 50 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 51 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 52 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 53 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 54 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 55 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 56 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 57 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 58 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 59 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 60 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 61 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 62 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 63 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 64 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 65 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 66 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 67 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
