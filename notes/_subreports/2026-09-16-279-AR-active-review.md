# #279 lane AR — the 15-base active review sheet for Dave — P-277-3 instrument
2026-09-16 · lane AR (Fable 5.1) · instrument under `s277-D6` · full report: `notes/_lanes/279/active-review/REPORT.md`

**The one line.** `notes/_lanes/279/active-review/REVIEW-active-2026-09-16.html` puts the 15 icon bases and their 31 "active" drawings (14×2 + 1×3, all derived at build time from `knowledge/_icon_nodes.json`'s `defaultActive` nulls + `activeVariantOf` edges, 46 glyphs inlined at 48px + 16px on light and dark chrome) in front of Dave with one answer per base — the twin, none, or flag-as-its-own-icon with per-drawing checkboxes and a note. Answers persist in localStorage; Export writes `DAVE-EXPORT-active-2026-09-16.json` as `{page, at, exportedAt, answers:{<base>:{choice, twin, flags[], note}}}`. Driver 36/36 green (export shape, round-trip, virgin first load); screenshots light + dark × 1280 + 390 from a never-driven context, checked by eye. Nothing under `knowledge/` touched.

**Closes when** Dave's export from this page is received (and read into rulings by the next lane).
