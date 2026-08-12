# Build brief — the named-palette tier (s157-D2, ruled #157, build at #158)

**Ruling:** `knowledge/_rulings.json` § s157-D2. **Mechanism precedent:** ADR-0014 (neutral DNA
tier) — extend it, do not invent a parallel one. **Do not re-derive:** everything below was
measured in-window at #157.

## The ruled sharing matrix (Dave, #157, confirmed against the #122 RAG controller)

| family    | legacy | mono | console | supercharge |
|-----------|--------|------|---------|-------------|
| grey ramp | own    | ── shared ── ↔ console | | own |
| RAG       | own (s122-D1/D5, SETTLED-ASSERTED) | own (s122-D2) | ── shared (s122-D3, fence lifted s122-D4) ── | |

## Measured state (#157, first-hand)

- Console + supercharge `overrides/rag/*`: **12 of 16 keys hex-identical duplicates**; only the
  4 `-tint` keys differ, LEGITIMATELY (tints derive from different grounds — keep per-theme).
- Legacy rag overrides: own values, `$notes` ratified — ADD, never trim.
- Mono rag lives in base `semantic-colour.json` (no override file names it).
- No theme overrides `rag/success-ink` / `rag/error-ink` — the -ink rungs are MONO ONLY by
  ruling (s151-D1 / s155-D1) and fall through silently today. Dave's eye caught this at #157.
- Theme cascade: `gen_theme_cascade.snippet_theme_css()` re-projects only vars a theme
  overrides — the fall-through class is structural, one gate short.

## The build (shape ruled; mechanics to price first at #158)

1. Palette sets as first-class token files: `knowledge/tokens/palettes/rag/{mono,legacy,console-supercharge}.json`
   — **names are placeholders, Dave rules them**. Values SOURCED from existing files, never retyped by hand.
2. `_themes.json` registry declares consumption per family: `ragPalette:`, `neutralRamp:`
   (ADR-0011 anticipated `neutralRamp`). Grey-ramp declarations per the matrix above.
3. Shared-by-reference projection. Tints stay per-theme derived.
4. **The gate is the point** [[gate-inside-the-growth-loop]]: every theme names a palette per
   family; no theme file hand-carries a palette-owned value; parse in the consumer's grammar
   (resolve against the JSON, not grep). Wire a consumer — `_build_all.py` step + CI — or it is
   an instrument without a consumer.
5. `amount-display` `--success-ink` then resolves via the palette (snippet currently carries
   raw hex in its two `[data-theme]` blocks — swap to the projected var once the tier exists).

## DO-NOT-RULE (the builder decides none of these)

- Palette names — Dave's.
- In-place-verify vs generate for the ratified override files — price both, Dave picks.
- Any green fork for non-mono themes' -ink rungs — NOT governed; do not invent.
- The 15 token-split exceptions, promotion of any derivation — Dave only.

## Open from s157-D1 (same lane, carried)

- Mono green seat APPROVED in-window ("for mono it's perfect").
- `none` → unbound delta stands unvetoed.
- No gate resolves meta `binds` addresses against the colour spine (#145 finding) — the palette
  gate above is the natural home; consider closing both with one instrument.
