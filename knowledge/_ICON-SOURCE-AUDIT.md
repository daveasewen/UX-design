# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 38 snippet(s) (17 verified-bespoke). Library glyphs indexed: 746.

| # | Snippet | paths | library | bespoke | UNKNOWN | declares | status |
|---|---------|------:|--------:|--------:|--------:|:--------:|--------|
| 1 | Accordion | 2 | 2 | 0 | 0 | — | ✅ verified |
| 2 | Account-card | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 3 | Action-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 4 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 5 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 6 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 7 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 8 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 9 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 10 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 11 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 12 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 13 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 14 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 15 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 16 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 17 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 18 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 19 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 20 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 21 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 22 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 23 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 24 | Progress-tracker | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 25 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 26 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 27 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 28 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 29 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 30 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 31 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 32 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 33 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 34 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 35 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 36 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 37 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 38 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
