# Icon-library gaps

Durable log of missing / needed icon assets surfaced during the component review.
Each gap blocks a specific design intent; revisit and wire it up when the asset lands.

| Glyph | Needed for | Status | Notes |
|---|---|---|---|
| `brand-apollo` (crescent) | Masthead brand mark (extreme crescent: white highlight + black shadow) | **PROVISIONAL** (2026-07-16) | Dave asked for a bow-and-arrow brand icon. Authored inline flagged `data-provenance="provisional" data-bespoke` (stroke bow arc + string + arrow). Replace with a real drawn HSBC/Apollo asset later. |
| `menu-search` (combined) | Masthead — collapsed nav affordance + trigger (menu + search overlapping) | **PROVISIONAL** (2026-07-16) | Dave asked for a single combined menu+search glyph ("draw one for now, overlapping"). Authored inline in `Masthead-interactive.html` flagged `data-provenance="provisional" data-bespoke` (hamburger bars + scaled magnifier). Replace with a real HSBC asset when one exists. |
| `download-active` (filled) | Links — icon-link active/pressed state | **OPEN** (2026-06-29) | HSBC library has `download.svg` (line) but **no `-active` filled variant** — 45 other `global-controls` glyphs do have one (e.g. `bookmark` / `bookmark-active`). The dynamic-weight set classifies `download` as active = *heavier stroke* because it's a **line-only** icon (arrow + tray, nothing enclosed to fill). Dave deferred: icon-link active = **label underline** for now. When a filled download glyph exists (authored-interim or official HSBC), add it to the library and wire the line→filled swap on hover/active per the `-active` convention. |

## The `-active` convention (for when these are filled in)
Resting `name.svg` = line/outline glyph; `name-active.svg` = the **filled silhouette** of it
(see `bookmark.svg` vs `bookmark-active.svg`). The icon gate (`_validate_icons.py`) byte-matches every
inline `<svg>` path to a real library file, so any active glyph must be a real asset in `assets/icons/`,
not an inline-authored shape.
