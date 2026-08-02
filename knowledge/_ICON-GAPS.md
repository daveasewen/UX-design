# Icon-library gaps

Durable log of missing / needed icon assets surfaced during the component review.
Each gap blocks a specific design intent; revisit and wire it up when the asset lands.

| Glyph | Needed for | Status | Notes |
|---|---|---|---|
| `brand-apollo` (crescent) | Masthead brand mark (extreme crescent: white highlight + black shadow) | ✅ **CLOSED — RULED #86** (2026-08-02) | ~~Dave asked for a bow-and-arrow brand icon~~ **SUPERSEDED by Dave's #86 ruling, verbatim: "the crescent is only a mark for apollo, we use it when we need designs to be anonymous / use the hsbc mark normally."** ⇒ crescent = Apollo/anonymity mark — the masthead use is CORRECT, not a gap; HSBC mark = normal use. Ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #86-D2. Original note, for the record: authored inline flagged `data-provenance="provisional" data-bespoke`. |
| `menu-search` (combined) | Masthead — collapsed nav affordance + trigger (menu + search overlapping) | **PROVISIONAL** (2026-07-16) · **governing record #86** | Dave asked for a single combined menu+search glyph ("draw one for now, overlapping"). Authored inline in `Masthead-interactive.html` flagged `data-provenance="provisional" data-bespoke` (hamburger bars + scaled magnifier). **Standing governing record (`knowledge/_GOVERNING-RECORDS.md` G13b) — closes when Dave approves the glyph.** |
| Spot-illustration / empty-state set | Empty-state (and future first-run / no-results / empty-inbox states) | **OPEN** (2026-07-22, Phase-2 worker B) | NO illustration-scale assets exist anywhere in `assets/icons/` — Empty-state ships text-led with 48px informative glyphs as anchors (worker B's judgment call, receipted). Proper fix = a dedicated spot-illustration set (empty inbox, no results, first-run). Worker B verified every other wave-1 glyph is a byte-matched library asset — this is the lane's only gap. |
| `download-active` (filled) | Links — icon-link active/pressed state | **OPEN** (2026-06-29) | HSBC library has `download.svg` (line) but **no `-active` filled variant** — 45 other `global-controls` glyphs do have one (e.g. `bookmark` / `bookmark-active`). The dynamic-weight set classifies `download` as active = *heavier stroke* because it's a **line-only** icon (arrow + tray, nothing enclosed to fill). Dave deferred: icon-link active = **label underline** for now. When a filled download glyph exists (authored-interim or official HSBC), add it to the library and wire the line→filled swap on hover/active per the `-active` convention. |

## Mislabeled assets (verified by render, 2026-07-17 · T8 footer social strip)

**`assets/icons/social/` base files carry the WRONG platform glyph** — caught only because the
component was render-verified (gates check that the file exists, not that its geometry matches the
name). The correct-named glyph lives in the `-2` sibling:

| File named… | Actually contains | Use this instead for the named platform |
|---|---|---|
| `social-facebook.svg` | **Instagram** glyph | `social-facebook-2.svg` (the real "f") |
| `social-youtube.svg` | **WhatsApp** glyph | `social-youtube-2.svg` (the real ▶) |
| `social-twitter-2.svg` | a chat/@ bubble (not X) | `social-twitter.svg` (the real X) — the base is right here |

**INVERTED `-active` pair (2026-07-17, Tab-bar reconciliation):** `products-and-services/payment.svg` is the
**FILLED** disc and `products-and-services/payment-active.svg` is the **OUTLINE** — backwards from the
`-active` convention (base = line, `-active` = filled silhouette). Anything doing the line→filled swap on this
glyph must wire it **inverted**: line = `payment-active.svg`, filled = `payment.svg`. Worth auditing whether
other `-active` pairs are flipped the same way when the icon-scale work runs (see the SCHEDULED icon/4px-grid
item in `_LIVE-STATE.md`).

`social-linkedin.svg` is correct. **Lesson:** for social/brand glyphs, render-verify the asset before
binding — the filenames are not trustworthy. T8 now uses `-facebook-2` / `-youtube-2` / `-twitter` / `-linkedin`.
Consider renaming the mislabeled base files at source (Dave's call — it's an `assets/` change).

## The `-active` convention (for when these are filled in)
Resting `name.svg` = line/outline glyph; `name-active.svg` = the **filled silhouette** of it
(see `bookmark.svg` vs `bookmark-active.svg`). The icon gate (`_validate_icons.py`) byte-matches every
inline `<svg>` path to a real library file, so any active glyph must be a real asset in `assets/icons/`,
not an inline-authored shape.
