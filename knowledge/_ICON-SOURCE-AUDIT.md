# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*ADVISORY (non-gating). Each snippet's inline `<svg>` path data is matched byte-for-byte against the library. UNKNOWN = not matched — EITHER an invented icon (use the library SVG, ideally a `<symbol>` sprite + `<use>`, and declare it in the token-manifest `icons` block) OR a legitimately bespoke/decorative shape (focus ring, custom mark). A human decides.*

**52 UNKNOWN path(s) across 32 snippet(s).** Library glyphs indexed: 746.

| # | Snippet | paths | library | UNKNOWN | declares icons | status |
|---|---------|------:|--------:|--------:|:--------------:|--------|
| 1 | Accordion | 2 | 0 | 2 | — | ⚠ 2 UNKNOWN path(s) |
| 2 | Avatar | 1 | 0 | 1 | — | ⚠ 1 UNKNOWN path(s) |
| 3 | Badge | 3 | 0 | 3 | — | ⚠ 3 UNKNOWN path(s) |
| 4 | Breadcrumbs | 0 | 0 | 0 | — | — no inline svg paths |
| 5 | Button | 0 | 0 | 0 | — | — no inline svg paths |
| 6 | Cards | 6 | 6 | 0 | — | ✅ all paths trace to the library |
| 7 | Countdown-timer | 0 | 0 | 0 | — | — no inline svg paths |
| 8 | Divider | 0 | 0 | 0 | — | — no inline svg paths |
| 9 | Dropdown | 5 | 0 | 5 | — | ⚠ 5 UNKNOWN path(s) |
| 10 | Headers | 1 | 0 | 1 | — | ⚠ 1 UNKNOWN path(s) |
| 11 | Hero | 1 | 0 | 1 | — | ⚠ 1 UNKNOWN path(s) |
| 12 | Input-fields | 6 | 6 | 0 | yes | ✅ all paths trace to the library |
| 13 | Links | 5 | 5 | 0 | — | ✅ all paths trace to the library |
| 14 | List-items | 0 | 0 | 0 | — | — no inline svg paths |
| 15 | Loading-indicator | 0 | 0 | 0 | — | — no inline svg paths |
| 16 | Modals | 1 | 0 | 1 | — | ⚠ 1 UNKNOWN path(s) |
| 17 | Navigations | 2 | 0 | 2 | — | ⚠ 2 UNKNOWN path(s) |
| 18 | Notifications | 3 | 0 | 3 | — | ⚠ 3 UNKNOWN path(s) |
| 19 | Pagination | 2 | 0 | 2 | — | ⚠ 2 UNKNOWN path(s) |
| 20 | Progress-tracker | 0 | 0 | 0 | — | — no inline svg paths |
| 21 | Quick-actions | 5 | 0 | 5 | — | ⚠ 5 UNKNOWN path(s) |
| 22 | Reorder | 9 | 0 | 9 | — | ⚠ 9 UNKNOWN path(s) |
| 23 | Search-field | 2 | 0 | 2 | — | ⚠ 2 UNKNOWN path(s) |
| 24 | Selection-controls | 7 | 0 | 7 | — | ⚠ 7 UNKNOWN path(s) |
| 25 | Slider | 0 | 0 | 0 | — | — no inline svg paths |
| 26 | Status-indicator | 0 | 0 | 0 | — | — no inline svg paths |
| 27 | Table | 0 | 0 | 0 | — | — no inline svg paths |
| 28 | Tabs | 0 | 0 | 0 | — | — no inline svg paths |
| 29 | Tags | 2 | 0 | 2 | — | ⚠ 2 UNKNOWN path(s) |
| 30 | Tooltip | 1 | 1 | 0 | — | ✅ all paths trace to the library |
| 31 | Video-player | 4 | 0 | 4 | — | ⚠ 4 UNKNOWN path(s) |
| 32 | View-options | 2 | 0 | 2 | — | ⚠ 2 UNKNOWN path(s) |

## UNKNOWN detail

### Accordion — 2 UNKNOWN of 2 path(s)
- `d="M9 12 3 6h12z"`
- `d="M9 12 3 6h12z"`

### Avatar — 1 UNKNOWN of 1 path(s)
- `d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5Zm0 2c-4 0-9 2-9 5v2h18v-2c0-3-5-5-9…"`

### Badge — 3 UNKNOWN of 3 path(s)
- `d="M12 22a2 2 0 0 0 2-2h-4a2 2 0 0 0 2 2Zm6-6V11c0-3-1.6-5.4-4.5-6V4a1.5 …"`
- `d="M12 22a2 2 0 0 0 2-2h-4a2 2 0 0 0 2 2Zm6-6V11c0-3-1.6-5.4-4.5-6V4a1.5 …"`
- `d="M12 22a2 2 0 0 0 2-2h-4a2 2 0 0 0 2 2Zm6-6V11c0-3-1.6-5.4-4.5-6V4a1.5 …"`

### Dropdown — 5 UNKNOWN of 5 path(s)
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`

### Headers — 1 UNKNOWN of 1 path(s)
- `d="M13.85 1 5.85 9l8 8H12.15L4.15 9l8-8H13.85Z"`

### Hero — 1 UNKNOWN of 1 path(s)
- `d="M5 17 5 1l8 8z"`

### Modals — 1 UNKNOWN of 1 path(s)
- `d="M1 1 L13 13 M13 1 L1 13"`

### Navigations — 2 UNKNOWN of 2 path(s)
- `d="M16 16l4 4"`
- `d="M4 20c0-4 4-6 8-6s8 2 8 6"`

### Notifications — 3 UNKNOWN of 3 path(s)
- `d="M8.31 1.68.11 15.8c-.31.53.07 1.2.69 1.2h16.4c.62 0 1-.67.69-1.2L9.69 …"`
- `d="M8.31 1.68.11 15.8c-.31.53.07 1.2.69 1.2h16.4c.62 0 1-.67.69-1.2L9.69 …"`
- `d="M7.22 13.55 3.59 9.92l1.27-1.27 2.36 2.36 5.93-5.93 1.27 1.27-7.2 7.2Z"`

### Pagination — 2 UNKNOWN of 2 path(s)
- `d="M13.85 1 5.85 9l8 8H12.15L4.15 9l8-8H13.85Z"`
- `d="M4.15 17 12.15 9 4.15 1H5.85L13.85 9 5.85 17H4.15Z"`

### Quick-actions — 5 UNKNOWN of 5 path(s)
- `d="M12 3v18M3 12h18"`
- `d="M4 6h16v12H4z"`
- `d="M4 10h16"`
- `d="M12 7v10M9 9.5h4.5a1.5 1.5 0 0 1 0 3H9m1 3h4"`
- `d="M3 11l18-7-7 18-3-7-8-4z"`

### Reorder — 9 UNKNOWN of 9 path(s)
- `d="M6 3h2v2H6V3Zm4 0h2v2h-2V3ZM6 8h2v2H6V8Zm4 0h2v2h-2V8ZM6 13h2v2H6v-2Zm…"`
- `d="M9 4l6 7H3z"`
- `d="M9 14L3 7h12z"`
- `d="M6 3h2v2H6V3Zm4 0h2v2h-2V3ZM6 8h2v2H6V8Zm4 0h2v2h-2V8ZM6 13h2v2H6v-2Zm…"`
- `d="M9 4l6 7H3z"`
- `d="M9 14L3 7h12z"`
- `d="M6 3h2v2H6V3Zm4 0h2v2h-2V3ZM6 8h2v2H6V8Zm4 0h2v2h-2V8ZM6 13h2v2H6v-2Zm…"`
- `d="M9 4l6 7H3z"`
- `d="M9 14L3 7h12z"`

### Search-field — 2 UNKNOWN of 2 path(s)
- `d="M13.5 13.5 L18 18"`
- `d="M1 1 L11 11 M11 1 L1 11"`

### Selection-controls — 7 UNKNOWN of 7 path(s)
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M4 9 L14 9"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M3.5 9.5 L7.5 13.5 L14.5 5"`
- `d="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17.3 5.9 20.7l1.5-6.8L2.2 9l6.9…"`
- `d="M12 2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17.3 5.9 20.7l1.5-6.8L2.2 9l6.9…"`

### Tags — 2 UNKNOWN of 2 path(s)
- `d="M1 1 L11 11 M11 1 L1 11"`
- `d="M1 1 L11 11 M11 1 L1 11"`

### Video-player — 4 UNKNOWN of 4 path(s)
- `d="M8 5v14l11-7z"`
- `d="M8 5v14l11-7z"`
- `d="M4 9v6h4l5 4V5L8 9H4z"`
- `d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"`

### View-options — 2 UNKNOWN of 2 path(s)
- `d="M3 5h18v3H3V5Zm0 5h18v3H3v-3Zm0 5h18v3H3v-3Z"`
- `d="M3 3h8v8H3V3Zm10 0h8v8h-8V3ZM3 13h8v8H3v-8Zm10 0h8v8h-8v-8Z"`

