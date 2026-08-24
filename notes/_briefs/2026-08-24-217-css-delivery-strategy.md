# CSS delivery strategy — compiled sizes, subset mints, critical inlining (#217 post-wrap, 2026-08-24)

**Status: MEASURED SIMULATION + priced techniques. Nothing here is ruled.** The s216-D1 mint step is ruled-but-unbuilt; every figure below was measured on the real `knowledge/canon/canon.css` at 27,270 lines (commit era `e6a1fe5`, #217) by simulating the mint: comments stripped, other themes' cascade removed, subsets cut by component selector bucket. Re-measure before quoting these against a future canon — the file grows.

## 1 · Compiled size, one theme, light + dark included (Dave's question)

| artefact | raw | gzip (over the wire) |
|---|---|---|
| authoring canon.css (4 themes, annotated) | 1,749,626 B | ~306 KB |
| — annotation comments (mint strips) | 472,019 B | — |
| — other-themes AUTO-THEMES cascade | 215,762 B (console 46K · legacy 58K · SC 107K) | — |
| **compiled single theme, dev-ready** | **~1,067,000 B** | **~116 KB** |
| minified (whitespace only) | 1,046,442 B | ~113 KB (−2%, not worth much) |
| type.css add-on | 11,675 B | — |

Per-theme size difference is negligible: a compile swaps values in place. ~116 KB gz is heavier than Bootstrap (~25 KB) but ordinary for a full product DS with a chart layer; it is one cached file.

## 2 · Site-scoped subset mints (the big lever)

The weight is concentrated: template shells ~207 KB + charts ~142 KB + app chrome ~90 KB of the 1.06 MB. A page that doesn't use them shouldn't pay for them.

| mint | raw | gzip | cut |
|---|---|---|---|
| full suite | 1,065 KB | ~116 KB | — |
| **brochureware site** (foundations + type + ~20 marketing components + bento) | **140 KB** | **~20 KB** | −83% |
| app/dashboard (adds charts, tables, app chrome, filters) | 454 KB | ~47 KB | −60% |

Mechanism already exists in embryo: each component's `#token-manifest` maps var→token, so the generator knows what a page consumes. A "site mint" = the s216-D1 mint with a component list as input. **Priced, not built; adopting it is Dave's.**

## 3 · Critical CSS inlining (honest assessment)

Works by inlining above-the-fold rules in the HTML so first paint doesn't wait on a stylesheet fetch. Real gains only on cold visits over slow networks, and they scale with the size deferred — deferring a 20 KB site mint buys ~100–300ms on mobile, imperceptible on fast connections. **The trap: inlined CSS cannot be cached** — every page re-ships it; returning visitors get slower under aggressive inlining.

**The pragmatic ladder for an Apollo-minted site:**
1. Scoped site mint first (does most of the work — see §2).
2. Inline only the true skeleton: tokens, type, grounds, first-viewport shell — target 2–4 KB.
3. `<link rel="preload">` the linked remainder so it's in flight immediately; let it cache.
4. The generator can COMPUTE critical CSS per page (it knows which components sit above the fold) — most sites guess; ours wouldn't. Priced, not built.

## 4 · Fonts beat CSS for perceived load

The licensed cut arriving late (flash of fallback / invisible text) is more visible than 200ms of stylesheet. Decide alongside any inlining work: a `font-display` policy + preloading the 2–3 actually-used weights likely buys more perceived speed than any CSS chunking. Unruled.

## Retrieval hooks
compiled css size · theme publish size · site mint · subset mint · tree-shaking · critical css · inline css · perceived load · font-display · preload · gzip sizes · s216-D1 publish tier
