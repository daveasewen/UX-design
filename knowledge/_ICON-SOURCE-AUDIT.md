# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**0 UNKNOWN path(s)** across 39 snippet(s) (17 verified-bespoke). Library glyphs indexed: 746.

| # | Snippet | paths | library | bespoke | UNKNOWN | declares | status |
|---|---------|------:|--------:|--------:|--------:|:--------:|--------|
| 1 | Accordion | 2 | 2 | 0 | 0 | — | ✅ verified |
| 2 | Account-card | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 3 | Action-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 4 | Amount-display | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 5 | Avatar | 1 | 1 | 0 | 0 | — | ✅ verified |
| 6 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 7 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 8 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 9 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 10 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 11 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 12 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 13 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 14 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 15 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 16 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 17 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 18 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 19 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 20 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 21 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 22 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 23 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 24 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 25 | Progress-tracker | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 26 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 27 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 28 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 29 | Selection-controls | 7 | 0 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 30 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 31 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 32 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 33 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 34 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 35 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 36 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 37 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 38 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 39 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

*(none — every inline path is library-matched or marked bespoke)*
