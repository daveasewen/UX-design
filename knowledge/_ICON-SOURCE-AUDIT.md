# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 64 snippet(s) (36 verified-bespoke). Library glyphs indexed: 746.

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
| 16 | Chart-line | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 17 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 18 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 19 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 20 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 21 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 22 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 23 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 24 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 25 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 26 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 27 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 28 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 29 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 30 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 31 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 32 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 33 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 34 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 35 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 36 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 37 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 38 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 39 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 40 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 41 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 42 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 43 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 44 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 45 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 46 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 47 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 48 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 49 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 50 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 51 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 52 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 53 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 54 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 55 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 56 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 57 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 58 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 59 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 60 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 61 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 62 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 63 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 64 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
