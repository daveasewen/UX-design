# Runbook — converting the HSBC catalogue to dynamic-weight icons

Method for porting the HSBC icon catalogue (`knowledge/assets/icons/<group>/`, filled SVGs) into
the dynamic-weight outline system, one group at a time. Keep this current as groups land.

## State model (how "appropriate states" maps)
- **default** → outline, variable stroke weight (our standard render).
- **active** → solid fill of the same silhouette (HSBC convention; confirmed on `bookmark`).
  Driven by `state="active"` on `<dyn-icon>` — no separate icon name.
- **badge** → a notification dot, added via the `badge` attribute (recolour with `--dyn-badge`).
  HSBC's `* Badge` / `* Active Badge` files collapse into this toggle.
- **solid-only** icons (e.g. carets) never have a weight — listed in the `SOLID` set.

### Holed icons (active fill)
Filling works automatically for single closed paths (bookmark, star, heart, caret). Icons whose
filled silhouette needs a punched hole (gear centre, an "i" knocked out of a disc) are TWO elements,
so a plain fill can't subtract. For those, add a single combined path to `ACTIVE_PATHS[name]`
(outer + inner subpath, `fill-rule:evenodd`). Do this per-icon as groups require it.

## Collapse / skip rules (why 658 files ≠ 658 icons)
- **`-thick` variants** → dropped. Thickness is the weight axis now (1 chevron, not chevron + chevron-thick).
- **`* Active` files** → become `state="active"`, not new names.
- **`* Badge` / `* Active Badge`** → become the `badge` toggle.
- **Proportional variants** (`-low`, `-narrow`) → skipped by default; add on request.
- **Social (7)** → brand logos (Facebook/LinkedIn/Twitter/YouTube). SKIP — trademarked, not weight-suited.
- **Status Icons (20)** → fixed multi-colour semantic marks; keep colour-fixed (outline equivalents
  already exist: check-circle, x-circle, alert-triangle, etc.).
- **Multi-colour glyphs** (manifest `fillMode` ≠ `currentColor`) → flag; redraw mono or skip.

## Per-group process
1. List the group from `icons.manifest.json`; strip `-thick`, fold `Active`/`Badge` into state/badge.
2. Redraw each base icon as a 24×24 outline path (round caps/joins), HSBC glyph as visual reference.
   Add `ACTIVE_PATHS` / `SOLID` entries where needed.
3. Add to `dynamic-icons.js` under a clearly-commented group section.
4. **Verify**: headless-render a sheet of the new icons at a couple of weights + any states; eyeball
   every glyph; confirm no empties / console errors before marking the group done.
5. Update the coverage tracker below + the README icon list.

## Coverage tracker
| Group (manifest)        | Source files | Converted | Status |
|-------------------------|-------------:|-----------|--------|
| Core / common UI set    | — | 64 | ✅ done (not a single HSBC group; close, search, settings, user, mail, file…) |
| Arrows and chevrons     | 24 | 12 | ✅ done (4 single + 4 double chevrons, 4 carets; `-thick` collapsed) |
| Global controls         | 121 | 0 | ⬜ next — has 46 active states |
| Touch                   | 10 | 0 | ⬜ todo (gestures, no states) |
| Volume and audio        | 16 | 0 | ⬜ todo (partial overlap: play/pause/stop/volume/mute done) |
| Media                   | 99 | 0 | ⬜ todo (28 active) |
| Informative             | 131 | 0 | ⬜ todo (58 active) |
| Miscellaneous           | 24 | 0 | ⬜ todo (HSBC-specific product glyphs) |
| Products and services   | 206 | 0 | ⬜ todo (87 active; large, bespoke) |
| Status Icons            | 20 | — | ⏭ keep colour-fixed (outline equivalents exist) |
| Social                  | 7 | — | ⏭ skip (brand logos) |
