# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 66 snippet(s) (36 verified-bespoke). Library glyphs indexed: 746.

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
| 14 | Chart-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 15 | Chart-donut | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 16 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 17 | Chart-scatter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 18 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 19 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 20 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 21 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 22 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 23 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 24 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 25 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 26 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 27 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 28 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 29 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 30 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 31 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 32 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 33 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 34 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 35 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 36 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 37 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 38 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 39 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 40 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 41 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 42 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 43 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 44 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 45 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 46 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 47 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 48 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 49 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 50 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 51 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 52 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 53 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 54 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 55 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 56 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 57 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 58 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 59 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 60 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 61 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 62 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 63 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 64 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 65 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 66 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
