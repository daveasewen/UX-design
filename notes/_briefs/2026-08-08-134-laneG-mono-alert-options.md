# Mono alert tint-only options — s134 laneG

**Controller:** `reviews/MONO-ALERT-OPTIONS-2026-08-08-s134-v1.html` — self-contained, no deps. DO-NOT-RULE respected: no canon/token/snippet/chain/GM/rulings edits, no commits.

## Canon symbol check
`knowledge/snippets/Alert.reference.html` `#al-error/-warning/-success/-info` symbols are **CANON**, not hand-rolled:
- `#al-error` path is byte-identical to `knowledge/assets/icons/status-icons/error.svg`'s outer path (same coordinates).
- `#al-warning/-success/-info` match `warning-solid.svg` / `success-solid.svg` / `information-solid.svg` geometry (18×18 grid, same inner-glyph paths), redrawn as `<symbol>` so `style="fill:var(--mark)"` can theme the inner mark — the flat status-icon SVGs hard-code fill instead.
No `_ICON-GAPS.md` entries flag any of the four alert glyphs. Controller reuses the Alert.reference.html sprite verbatim.

## Spine values used (sole source: `knowledge/tokens/semantic-colour.json`)
Roundel shape = `rag/*-background` (mode-invariant, s122-D2): error `#F6604C`, warning `#E0A61F`, success `#66CC8D`, info `#78A7E8`.
Tint = `rag/*-tint` (s123-D3 composited): error `#FDD9D4`/`#60302A`, warning `#F6E6C0`/`#614C1C`, success `#D4F1DF`/`#32533F`, info `#DFEAF9`/`#38475C` (light/dark).

## Contrast table (glyph-on-shape, the gated leg)
| status | shape | #1A1A1A | #000000 | #FFFFFF |
|---|---|---|---|---|
| error | #F6604C | 5.55:1 | 6.70:1 | 3.14:1 fail |
| warning | #E0A61F | 7.99:1 | 9.64:1 | 2.18:1 fail |
| success | #66CC8D | 8.77:1 | 10.59:1 | 1.98:1 fail |
| information | #78A7E8 | 7.04:1 | 8.49:1 | 2.47:1 fail |

All four pass ≥4.5 with #1A1A1A or #000000; white glyph fails on all four (shapes too light) — controller flags this live if selected.
