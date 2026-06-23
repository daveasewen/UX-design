# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*ADVISORY (non-gating). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Limitation: only `<path d>` is checked; pure `<circle>`/`<rect>` icons (e.g. a 3-dot kebab) are not yet caught.*

**0 UNKNOWN path(s)** across 32 snippet(s) (15 verified-bespoke). Library glyphs indexed: 746.

| # | Snippet | paths | library | bespoke | UNKNOWN | declares | status |
|---|---------|------:|--------:|--------:|--------:|:--------:|--------|
| 1 | Accordion | 2 | 2 | 0 | 0 | — | ✅ verified |
| 2 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 3 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 4 | Breadcrumbs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 5 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 6 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 7 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 8 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 9 | Dropdown | 5 | 0 | 5 | 0 | — | ✅ verified · 5 bespoke |
| 10 | Headers | 1 | 1 | 0 | 0 | — | ✅ verified |
| 11 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 12 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 13 | Links | 5 | 5 | 0 | 0 | — | ✅ verified |
| 14 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 15 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 16 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 17 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 18 | Notifications | 3 | 0 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 19 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 20 | Progress-tracker | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 21 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 22 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 23 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 24 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 25 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 26 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 27 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 28 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 29 | Tags | 2 | 2 | 0 | 0 | — | ✅ verified |
| 30 | Tooltip | 1 | 1 | 0 | 0 | — | ✅ verified |
| 31 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 32 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
