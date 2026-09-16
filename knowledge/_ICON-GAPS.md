# Icon-library gaps

Durable log of missing / needed icon assets surfaced during the component review.
Each gap blocks a specific design intent; revisit and wire it up when the asset lands.

| Glyph | Needed for | Status | Notes |
|---|---|---|---|
| `brand-apollo` (crescent) | Masthead brand mark (extreme crescent: white highlight + black shadow) | ✅ **CLOSED — RULED #86** (2026-08-02) | ~~Dave asked for a bow-and-arrow brand icon~~ **SUPERSEDED by Dave's #86 ruling, verbatim: "the crescent is only a mark for apollo, we use it when we need designs to be anonymous / use the hsbc mark normally."** ⇒ crescent = Apollo/anonymity mark — the masthead use is CORRECT, not a gap; HSBC mark = normal use. Ledger: `notes/_MEMENTO-DECISIONS.md` § ★ #86-D2. Original note, for the record: authored inline flagged `data-provenance="provisional" data-bespoke`. |
| `menu-search` (combined) | Masthead — collapsed nav affordance + trigger (menu + search overlapping) | **PROVISIONAL** (2026-07-16) · **governing record #86** | Dave asked for a single combined menu+search glyph ("draw one for now, overlapping"). Authored inline in `Masthead-interactive.html` flagged `data-provenance="provisional" data-bespoke` (hamburger bars + scaled magnifier). **Standing governing record (`knowledge/_GOVERNING-RECORDS.md` G13b) — closes when Dave approves the glyph.** ⚠ #212: the DESIGNED glyph arrived (Figma Neo-net v02.0 node 2785:97115, Dave: "try this"); exported, cleaned to `assets/icons/menu-search.svg`, swapped into `Masthead-interactive.html` as PROPOSED (`data-provenance="figma-export …"`); his eye owed on the live masthead before APPROVED. |
| Spot-illustration / empty-state set | Empty-state (and future first-run / no-results / empty-inbox states) | **OPEN** (2026-07-22, Phase-2 worker B) | NO illustration-scale assets exist anywhere in `assets/icons/` — Empty-state ships text-led with 48px informative glyphs as anchors (worker B's judgment call, receipted). Proper fix = a dedicated spot-illustration set (empty inbox, no results, first-run). Worker B verified every other wave-1 glyph is a byte-matched library asset — this is the lane's only gap. |
| `download-active` (filled) | Links — icon-link active/pressed state | **OPEN** (2026-06-29) | HSBC library has `download.svg` (line) but **no `-active` filled variant** — 45 other `global-controls` glyphs do have one (e.g. `bookmark` / `bookmark-active`). The dynamic-weight set classifies `download` as active = *heavier stroke* because it's a **line-only** icon (arrow + tray, nothing enclosed to fill). Dave deferred: icon-link active = **label underline** for now. When a filled download glyph exists (authored-interim or official HSBC), add it to the library and wire the line→filled swap on hover/active per the `-active` convention. |
| `folder` / hierarchy set (folder, folder-open) | Tree (wave-4 #210) — node glyphs for hierarchy/disclosure views | **OPEN** (2026-08-20, wave-4 Lane A) | Lane A probed `assets/icons/` and found NO folder or hierarchy glyph anywhere; Tree ships with chevron twisties + text-led nodes (no invented glyph, per the byte-match discipline). Proper fix = folder / folder-open pair (+ `-active` per convention). Receipt: `notes/_receipts/2026-08-20-210-wave4-laneA-calendar-tree.md`. |
| `grip` / drag-handle (resize) | Splitter (wave-4 #210) — divider affordance; future reorder/drag uses | **OPEN** (2026-08-20, wave-4 Lane B) | Lane B probed for grip/drag/handle/resize names — 0 hits. Splitter ships with a CSS-drawn dot-pair divider flagged demo-chrome, no invented library-style glyph. Proper fix = grip-vertical / grip-horizontal pair. Receipt: `notes/_receipts/2026-08-20-210-wave4-laneB-cascader-splitter-qrcode.md`. |

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

## The drawings Dave says are their own icon (2026-09-16, his review of the 15 multi-active bases)

Dave looked at every base that came out of the export with two or three drawings all named “… Active” and said, drawing by drawing, which one is the twin and which is a different icon wearing an active name. A drawing in this table is **not** the active state of its base: it is its own icon, it needs an inactive version drawn, and the name it carries came from the exporter's collision counter, not from a designer.

His export: `notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json` (2026-09-16T15:55:41.531Z). The words in the last column are his, verbatim.

| Drawing | Base it was exported under | The twin he named | His words |
|---|---|---|---|
| `alert-active-2` | `alert` | `alert-active` | alert-active-2 is incorrectly labeled |
| `contact-chat-ai-active` | `contact-chat-ai` | `contact-chat-ai-active-2` | contact-chat-ai-active is incorrectly labeled |
| `dentist-active` | `dentist` | `dentist-active-2` | dentist-active - wrong label<br>dentist-active-3 - wrong label |
| `dentist-active-3` | `dentist` | `dentist-active-2` | dentist-active - wrong label<br>dentist-active-3 - wrong label |
| `laboratory-active-2` | `laboratory` | `laboratory-active` | laboratory-active-2 - mislabeled |
| `renew-active` | `renew` | `renew-active-2` | renew-active - mislabeled |
| `user-staff-active` | `user-staff` | `user-staff-active-2` | user-staff-active - mislabeled |
| `voice-active-2` | `voice` | `voice-active` | voice-active-2 - mislabeled |
| `withdraw-overpayment-active` | `withdraw-overpayment` | `withdraw-overpayment-active-2` | withdraw-overpayment-active - mislabeled |

**6 rows of his review are not on this list yet** — `electricity`, `employee-banking-solution`, `financial-health-check`, `jade-lifestyle`, `reward`, `traditional-chinese-medicine`. On each of those his tick and his note say different things, or he wrote that he was not certain, so nothing was written down from them and the question is back with him on `notes/_lanes/280/inscribe-active/ASK-2026-09-16.html`. The drawings they name join this table when he answers.

## The `-active` convention (for when these are filled in)
Resting `name.svg` = line/outline glyph; `name-active.svg` = the **filled silhouette** of it
(see `bookmark.svg` vs `bookmark-active.svg`). The icon gate (`_validate_icons.py`) byte-matches every
inline `<svg>` path to a real library file, so any active glyph must be a real asset in `assets/icons/`,
not an inline-authored shape.
