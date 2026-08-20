# Icon-source audit — inline SVG paths vs the HSBC library (`assets/icons/`)

*GATE (build-failing as of 2026-06-24). Each inline `<svg>` path is matched to the library. **library** = byte-matches a real glyph · **bespoke** = inside `<svg data-bespoke="reason">`, a deliberately custom shape (control glyph / animated / focus mark), verified · **UNKNOWN** = neither (possibly invented → use the library SVG, or mark it `data-bespoke`). Shape-only icons (`<circle>`/`<rect>`/`<ellipse>`/`<polygon>` with no `<path>`, e.g. a 3-dot kebab) are now flagged too.*

**15 UNKNOWN path(s)** across 108 snippet(s) (77 verified-bespoke). Library glyphs indexed: 746.

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
| 11 | Back-to-top | 1 | 1 | 0 | 0 | — | ✅ verified |
| 12 | Badge | 3 | 3 | 0 | 0 | — | ✅ verified |
| 13 | Banner | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 14 | Breadcrumbs | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 15 | Button | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 16 | Calendar | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 17 | Cards | 6 | 6 | 0 | 0 | — | ✅ verified |
| 18 | Carousel | 11 | 0 | 0 | 11 | — | ⚠ 11 UNKNOWN |
| 19 | Cascader | 2 | 1 | 1 | 0 | yes | ✅ verified · 1 bespoke |
| 20 | Chart-bar | 15 | 15 | 0 | 0 | — | ✅ verified |
| 21 | Chart-boxplot | 3 | 3 | 0 | 0 | — | ✅ verified |
| 22 | Chart-bullet | 3 | 3 | 0 | 0 | — | ✅ verified |
| 23 | Chart-butterfly-h | 3 | 3 | 0 | 0 | — | ✅ verified |
| 24 | Chart-butterfly-v | 3 | 3 | 0 | 0 | — | ✅ verified |
| 25 | Chart-candlestick | 3 | 3 | 0 | 0 | — | ✅ verified |
| 26 | Chart-combo | 3 | 3 | 0 | 0 | — | ✅ verified |
| 27 | Chart-donut | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 28 | Chart-histogram | 3 | 3 | 0 | 0 | — | ✅ verified |
| 29 | Chart-line | 6 | 6 | 0 | 0 | — | ✅ verified |
| 30 | Chart-pie | 16 | 6 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 31 | Chart-scatter | 2 | 2 | 0 | 0 | — | ✅ verified |
| 32 | Chart-sparkline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 33 | Chart-stacked-area | 6 | 3 | 3 | 0 | — | ✅ verified · 3 bespoke |
| 34 | Combobox | 15 | 4 | 11 | 0 | yes | ✅ verified · 11 bespoke |
| 35 | Command-palette | 6 | 6 | 0 | 0 | — | ✅ verified |
| 36 | Confirmation | 1 | 1 | 0 | 0 | — | ✅ verified |
| 37 | Countdown-timer | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 38 | Data-grid | 13 | 9 | 4 | 0 | yes | ✅ verified · 4 bespoke |
| 39 | Date-picker | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 40 | Date-range-picker | 10 | 10 | 0 | 0 | yes | ✅ verified |
| 41 | Divider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 42 | Document-row | 4 | 4 | 0 | 0 | — | ✅ verified |
| 43 | Drawer | 2 | 2 | 0 | 0 | — | ✅ verified |
| 44 | Dropdown | 10 | 0 | 10 | 0 | — | ✅ verified · 10 bespoke |
| 45 | Empty-state | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 46 | Eyebrow | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 47 | Fab | 1 | 1 | 0 | 0 | — | ✅ verified |
| 48 | File-upload | 8 | 8 | 0 | 0 | yes | ✅ verified |
| 49 | Footer | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 50 | Form-layout | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 51 | Headers | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 52 | Hero | 1 | 1 | 0 | 0 | — | ✅ verified |
| 53 | Icon-button | 5 | 5 | 0 | 0 | — | ✅ verified |
| 54 | Image-block | 5 | 1 | 0 | 4 | — | ⚠ 4 UNKNOWN |
| 55 | Input-fields | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 56 | Kpi-tile | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 57 | Layout-utilities | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 58 | Limits-meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 59 | Links | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 60 | List-items | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 61 | Loading-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 62 | Meter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 63 | Modal-lightbox | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 64 | Modals | 1 | 1 | 0 | 0 | — | ✅ verified |
| 65 | Multi-select | 13 | 5 | 8 | 0 | yes | ✅ verified · 8 bespoke |
| 66 | Navigations | 2 | 2 | 0 | 0 | — | ✅ verified |
| 67 | Notifications | 9 | 9 | 0 | 0 | yes | ✅ verified |
| 68 | Pagination | 2 | 2 | 0 | 0 | — | ✅ verified |
| 69 | Payment-card-visual | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 70 | Popconfirm | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 71 | Popover | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 72 | Progress-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 73 | Progress-tracker | 1 | 1 | 0 | 0 | — | ✅ verified |
| 74 | Qr-code | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 75 | Quick-actions | 4 | 4 | 0 | 0 | — | ✅ verified |
| 76 | Range-slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 77 | Rating | 1 | 1 | 0 | 0 | — | ✅ verified |
| 78 | Reorder | 18 | 18 | 0 | 0 | — | ✅ verified |
| 79 | Runway-bar | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 80 | Search-field | 2 | 2 | 0 | 0 | — | ✅ verified |
| 81 | Secure-entry | 5 | 5 | 0 | 0 | yes | ✅ verified |
| 82 | Segmented-control | 2 | 2 | 0 | 0 | — | ✅ verified |
| 83 | Selection-controls | 8 | 0 | 8 | 0 | — | ✅ verified · 8 bespoke |
| 84 | Sidebar-nav | 9 | 9 | 0 | 0 | — | ✅ verified |
| 85 | Skeleton-loader | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 86 | Slider | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 87 | Split-button | 4 | 4 | 0 | 0 | — | ✅ verified |
| 88 | Splitter | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 89 | Standing-order-mandate-row | 2 | 2 | 0 | 0 | — | ✅ verified |
| 90 | Stat-card | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 91 | Status-indicator | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 92 | Stepper | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 93 | Summary | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 94 | Tab-bar | 11 | 11 | 0 | 0 | yes | ✅ verified |
| 95 | Table | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 96 | Tabs | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 97 | Tags-input | 4 | 4 | 0 | 0 | yes | ✅ verified |
| 98 | Tags | 1 | 1 | 0 | 0 | yes | ✅ verified |
| 99 | Textarea | 3 | 3 | 0 | 0 | yes | ✅ verified |
| 100 | Time-picker | 9 | 4 | 5 | 0 | yes | ✅ verified · 5 bespoke |
| 101 | Timeline | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 102 | Toast | 6 | 6 | 0 | 0 | yes | ✅ verified |
| 103 | Tooltip | 3 | 3 | 0 | 0 | — | ✅ verified |
| 104 | Transaction-row | 0 | 0 | 0 | 0 | — | — no inline svg paths |
| 105 | Transfer-list | 11 | 4 | 7 | 0 | — | ✅ verified · 7 bespoke |
| 106 | Tree | 2 | 2 | 0 | 0 | yes | ✅ verified |
| 107 | Video-player | 4 | 4 | 0 | 0 | — | ✅ verified |
| 108 | View-options | 2 | 2 | 0 | 0 | — | ✅ verified |

## UNKNOWN detail

### Carousel — 11 UNKNOWN of 11 path(s)
- `d="(shape-only icon: <svg><rect> with a diagonal corner mark, captioned i…"`
- `d="(shape-only icon: <svg class="ph" viewBox="0 0 400 220" preserveAspect…"`
- `d="(shape-only icon: <svg class="ph" viewBox="0 0 400 220" preserveAspect…"`
- `d="M11 15L5 9L11 3"`
- `d="M7 3L13 9L7 15"`
- `d="(shape-only icon: <svg class="ph" viewBox="0 0 300 220" preserveAspect…"`
- `d="(shape-only icon: <svg class="ph" viewBox="0 0 300 220" preserveAspect…"`
- `d="(shape-only icon: <svg class="ph" viewBox="0 0 300 220" preserveAspect…"`
- `d="(shape-only icon: <svg class="ph" viewBox="0 0 300 220" preserveAspect…"`
- `d="M11 15L5 9L11 3"`
- `d="M7 3L13 9L7 15"`

### Image-block — 4 UNKNOWN of 5 path(s)
- `d="(shape-only icon: <svg> carries role="img" + a descriptive aria-label …"`
- `d="(shape-only icon: <svg viewBox="0 0 400 300" preserveAspectRatio="none…"`
- `d="(shape-only icon: <svg viewBox="0 0 300 300" preserveAspectRatio="none…"`
- `d="(shape-only icon: <svg viewBox="0 0 300 400" preserveAspectRatio="none…"`

