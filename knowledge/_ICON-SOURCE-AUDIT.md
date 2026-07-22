# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 54 snippet(s) (17 verified-bespoke). Library glyphs indexed: 746.

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
| 14 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 15 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 16 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 17 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 18 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 19 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 20 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 21 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 22 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 23 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 24 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 25 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 26 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 27 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 28 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 29 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 30 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 31 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 32 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 33 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 34 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 35 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 36 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 37 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 38 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 39 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 40 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 41 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 42 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 43 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 44 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 45 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 46 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 47 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 48 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 49 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 50 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 51 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 52 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 53 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 54 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
