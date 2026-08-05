# Receipt — #97 showroom side tree nav (Dave's job, from #96 OWED)

**What:** `showroom/index.html` button sea → side tree nav. Generator-only change
(`knowledge/gen_showroom.py`: INDEX_TMPL + section-builder); regenerated, never hand-edited.

**Shape (proposed by Claude, awaiting Dave's eye — NOT ruled):**
- Left nav 260px: `<details open>` per category (native expand/collapse), component links with
  per-item meta in `title`, count per category.
- Right pane: intro on landing; picking a component loads its page in an inline iframe with a
  viewbar (component name + "Open page ↗").
- Deep link `#c=<slug>&theme=<t>`; theme seg carries into the frame src; aria-current on the
  selected link, ancestor category auto-opens.
- ≤760px collapses to single column.

**Proofs (all green, run 2026-08-05):**
- `gen_showroom.py --selftest` 6 bites OK · regen 75 pages + index · `--check` in sync.
- Render-verified in-sandbox (runbook recipe, shared-mount staging), widths 1180 + 700,
  `document.fonts.check('16px HSBC_MtUnivers_Latin')` true at both.
- Numeric asserts: nav width 260 · 75 links / 7 categories · iframe display none→block on click ·
  hash `#c=chart-candlestick&theme=mono` · aria-current tracks · theme switch rewrites frame src to
  `#theme=legacy` · deep-link `#c=button&theme=legacy` restores selection · 700px grid = `700px`
  (single column).
- Shots read: `outputs/index-1180-landing.png`, `index-1180-selected.png`, `index-700.png`.

**Flags for Dave:**
1. Doubled chrome in preview: the embedded page keeps its own header (← Library, theme seg, width
   slider) under the new viewbar. Kept for the width slider; rule if it should be suppressed in
   iframe context.
2. Residual, declared: at 700px an oversized gap sits between the stacked tree and the intro —
   cosmetic; desktop is the review surface; unfixed.

**Untouched:** component pages, snippets, categories map, review overlay routing.
