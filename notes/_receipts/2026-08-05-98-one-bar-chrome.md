# #98 — ONE-BAR page chrome + snippet control purge (Dave's #97-D1, enacted; #98-D1 ruled this window)

**Ruling #98-D1 (Dave, this window):** purge lands in the SOURCES — the library is his sole
interface from now on, snippets become pure canon. Replay moves INTO the one bar, disabled
where inapplicable. (a) one pane RULED · (b) Replay stays, in-bar RULED · (c) settled as
source-clean after survey evidence (unguarded `themeToggle` listeners made the generator-strip
variant JS-hazardous; sources-clean removes the hazard class entirely).

## What changed
- **75/75 snippet sources cleaned** (Sonnet sub, conductor-verified): `.demo-controls` blocks,
  theme/width/replay wiring, dead CSS. −931/+171 lines. Entangled files hand-edited — real
  state controls KEPT (Data-grid/Table seg, Drawer/Modal `#open`, Toast spawns, List-items
  `#dense`, Skeleton `#resolveDemo` + replacement focus-visible rule). Segmented-control's
  unrelated `.demo-controls` class renamed `.section-head-row`.
- **`gen_showroom.py`:** PAGE_TMPL = ONE bar (title · meta · theme seg · Light/Dark seg ·
  width · ↻ Replay · Open ↗), no ← Library, ONE pane/iframe; generic in-bar replay
  (re-toggles `.dv-animate`/`figure.dv` in the pane; `disabled` where payload has no
  `dv-animate`). INDEX_TMPL viewbar REMOVED (flag ① answered by #97-D1). Selftest +4 bites
  (no back-CTA · one iframe · replay+open in bar · no viewbar) = 10.
- Regen 76 files, `--check` in sync, snippet gate 75/0.

## Render-proof (runbook recipe, staged mount `outputs/_render-env`)
44 asserts × 2 widths (1440/760), ALL PASS, shots READ: one header bar · no back-CTA · pane
carries NO demo-controls · HSBC face true in pane · dark toggle reaches pane body[data-theme]
+ frame ground · replay cycles dv-animate (population 5 stable) · width slider drives iframe ·
deep-link `#theme&m&w` · replay disabled on Button · **console errors [] on both pages —
the strip left no orphaned JS**.

## Residuals, declared
1. **Confirmation.reference.html lost its replay** — its motion is a display-toggle on
   `.confirm`, not `dv-animate`, so the bar's Replay is disabled there. Fix would be migrating
   its motion to the dv-animate idiom (canon behaviour change — Dave's call).
2. ~~Index header theme seg~~ — **RULED + ENACTED in-window (Dave, screenshot): REMOVED.**
   Index header is now title + count only; theme lives solely on the page bar. Selftest bite
   6e pins it; render re-proven (0 segs on index, nav + `#c=` deep-link intact, 0 errors).
3. At narrow embed widths the one bar wraps to two rows inside the iframe — cosmetic.
4. Horizontal-bar y-labels clip at 800px pane width — pre-existing snippet behaviour, not
   introduced by this change.
5. `knowledge/snippets/Segmented-control.reference.html.bak` (0 bytes, sub's sed artefact) —
   sandbox blocks unlink; excluded from commit, delete by hand.
