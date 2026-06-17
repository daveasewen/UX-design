# Token ingestion — gaps & edits log

Running record of issues found while ingesting the HSBC Common Toolkit **"Gaps and edits"** branch (Figma fileKey `Cgbtrmfp15ruNFkIAClpkI`) into the DTCG token store. Each item is for Dave to confirm; nothing is edited in Figma without sign-off.

## Breakpoints, grids and scales (page `471:15986`, web guide `13967:90189`)

1. **Deprecated duplicate border token.** ✅ DONE — Dave deleted `non-interactive (depricate)/border/on-light/neutral-3`. Canon never included it.

### ⚠️ Broader issue: a "host" of `depricate` variables across the file
There are many variables under a misspelled `depricate` namespace, not just the border one. The connector can only see variables bound to a queried node, so it can't list them all. **Bulk fix (Dave):** search "depricate" in Figma's Variables panel and delete the matches. **Claude:** will log every `depricate` variable encountered per Foundations page below as a running hit-list. Canon (the DTCG store) excludes all deprecated aliases by default.

Deprecated variables seen so far:
- `non-interactive (depricate)/border/on-light/neutral-3` (#d7d8d6) — deleted ✅

2. **"Scales applied differently" note.** ✅ EXPLAINED (Dave): this is the type scale — it changes across breakpoints. Not an error. Confirm exact per-scale values on the Font scales page.

3. **Type-size differences across breakpoints/files.** ✅ EXPLAINED (Dave): expected — `scale-1/2/3` are responsive type+space scales, so a step like `font-4` resolves to different px per breakpoint (e.g. 24 vs 19). Reconcile exact values when ingesting Font scales and tokens.

4. **Separate margin token.** ✅ DONE (Dave: yes, may change). `layout.json` now splits `grid.main` and `grid.flyout`, each with separate `gutter` and `margin` per breakpoint. Main margin mirrors gutter (single source value); flyout margins are 0 until Large then 40.

## Font scales and tokens (page frame `46048:7963`)

5. **TScale vs grid-scale breakpoint mismatch.** ✅ DECISION (Dave): the **TScale mapping ending at 1600+ is authoritative** — TScale:1 = 320–959, TScale:2 = 960–1599, TScale:3 = 1600+. The Breakpoints page's "scale (font and space)" column (scale-1 320–759 / scale-2 760–1279 / scale-3 1280+) is the older mapping and should be reconciled to match. **Open edit:** update the Breakpoints page scale ranges to the TScale ranges (or confirm intentional difference).

6. **Per-TScale type sizes were in images.** ✅ RESOLVED via OCR (specimen node 46048:10725). Full 7-size × 3-TScale table now in `typography.json`. The connector's resolved variable mode was TScale:3.

7. **Missing `font-3`/`font-6`/`font-7`.** ✅ RESOLVED via OCR — all seven steps (font-1…font-7) captured. font-N = specimen S-N.

8. **`font-4 = 24` here vs `19` in accordion.** ✅ EXPLAINED — 24 is TScale:3, 19 is TScale:1 (confirmed by the table). Component metadata should reference the type step (e.g. font-5) rather than a fixed px, since px varies by TScale.

9. **New token found: `layout/web/margin = 16px`** (added to `layout.json`), alongside `layout/web/gutter = 40px`.

10. **RAG status colours seen** (for the Colour tokens page): `colour/rag/green #00847f`, `green-tint #e5f2f2`, `red #a8000b`, `red-tint #f9f2f3`; plus `rag/icon/success/container #00847f`, `rag/border/error/default #a8000b`. Will formalise on the Colour tokens page.

_Add subsequent pages below as they are ingested._
