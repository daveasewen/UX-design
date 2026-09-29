# #308 lane L — "Common is legacy" and the default icons

COUNTS: rulings 1 (s308-D25, store 814 → 815, stamped enacted at 8fc6df3c) / rows noted 1 (W-308i1) / doc rows minted 1 (W-308l1, born closed) / defaultActive in the graph 1 → 15 of 15 (14 drawn lines + 1 declared null; 0 → 14 lines) / undeclared skips 14 → 0 / surfaces relabelled 146 pages (137 showroom + index + 8 foundations) + canon.css comment + 2 reports / guard arms 6 (gen_showroom) + 3 (_validate_edges) / commits 965257d3, 8fc6df3c, and this report's / pushed no

Dave's words: notes/_lanes/308/DAVE-WORDS-2026-09-29-1208.md (committed in 965257d3). Item 1: "Common is legacy - its how we should label it in any interfaces, we can rename or alias it, whatever is the best solutio". Item 2: "Okay, is this simple to fix?"

## Job 1 — Common is the label, legacy is the id

**Id vs label, in one sentence:** the theme keeps the id `legacy` (`apollo-legacy`) everywhere it is an identifier, and the registry's display `label` is now "Apollo Common", which every interface reads and prints as "Common" — an alias, because a rename would move hundreds of files and rewrite old records, and s227-D8 already holds the rename as its own lane.

**The one home.** It already existed: `label` on each theme in `knowledge/tokens/themes/_themes.json`, read through `gen_theme_cascade.load_themes()`. Changed "Apollo Legacy" → "Apollo Common" and added a `$labelNote` beside it (the ruling, the reason, what reads it). The `attrAliases: ["common"]` of s227-D8(a) is untouched.

**Which interfaces print a theme name to a person — measured, not assumed:**

| surface | printed the theme name? | change |
|---|---|---|
| showroom component pages (137) — also the pack's theme picker, all in the pack manifest | yes: picker button "Legacy", the note "Legacy re-binds N", "Apollo Legacy: N var(s) re-bound" | the button and note already read `label`; the "re-binds" line was hand-typed and now reads it. Regenerated. |
| showroom/index.html (gen_library_214) | yes: picker button | already reads `label`. Regenerated (also picks up a committed chart-bar JS count it was behind on). |
| showroom/_foundations/*.html (gen_foundations_217), 8 pages | yes: hand-typed picker "Legacy" | generator now reads `label` (`theme_btns()`); the 8 pages got that one line (see below). |
| knowledge/_render/apollo-fab.js (view-time overlay) | yes, already "Common" since #227 | none; the guard covers it. |
| KG explorer | no picker; the word appears only inside ruling and history records | none (history). |
| dashboard | no picker; only in ruling titles | none (history). |
| review-page builders (knowledge/_review/, _make_review.py) | no theme names | none. The dated `_render/gen_*_217.py` / `gen_review_213*.py` write old pages under reviews/ — history, untouched. |
| reports a person reads: _TEXT-CONTRAST-AUDIT.md/.json, _THEME-PROVENANCE-GATE.md | yes, from `label` | regenerated; they now read "Apollo Common (`apollo-legacy`)". |
| canon.css AUTO-THEMES comment | yes, from `label` | regenerated; one comment line, same byte length, selector still `[data-apollo-theme="legacy"]`. |

**The guard.** `gen_showroom.py --check` (the showroom sync gate, BLOCKING in `_build_all.py`) now also scans every live picker — `showroom/*.html`, `showroom/_foundations/*.html`, `dashboard/index.html`, `knowledge/_render/apollo-fab.js` — and refuses any theme control whose printed name is not the registry label (less "Apollo "). Selftest arms 8–8f: the registry says Common; a bare "Legacy" button goes red; a foundations-style `data-theme-attr` button printing the id goes red; the label and a light/dark button pass; an overlay THEMES row printing the id goes red; the live pickers are clean today. Proven on the real HEAD~ files: the pre-change accordion page and bento page each give one fault.

**Ruling and row.** s308-D25 inscribed with `_inscribe_ruling.py` (dry run, then write; reconstruction passed; receipt `notes/_lanes/308/L/inscribe.write.txt`), entry `notes/_lanes/308/L/entries/s308-D25.json`, then stamped enacted with 8fc6df3c. W-308i1 noted by addition (`notes/_lanes/308/L/rows.json`): "Common" in s308-D2 means `legacy`, so the chosen mark is red in Supercharge and Legacy/Common, black in Console and Mono.

## Job 2 — the default icons

- `knowledge/_build_kg_explorer.py` 1.32: `defaultActive` joins `ASSET_DRAWN`. Built graph: 15 defaultActive = 14 lines (both ends present) + 1 declared null (icon:jade-lifestyle, his "open"); 1.31 had 0 lines + that null. In the page: 14 drawn with the assets chip on, 0 at defaults (the assets chip loads off, as every asset line).
- The class: every pass that reads an edge and does not link it now calls `_skip()`, which tallies by "<pass> <type>" in `rep['skipped_by']`; `main()` prints the tally ("skipped edges by type: none" today); `SKIP_DECLARED` (empty) is where a deliberate skip is named with its reason.
- `knowledge/_validate_edges.py --coverage` (BLOCKING) gains SKIPPED-UNDECLARED. Selftest 17 of 17 pass, including arms 14–16. Mutant: with defaultActive taken back out of ASSET_DRAWN in memory, coverage refuses "asset defaultActive (14 edge(s) read from storage and not linked)". `--check` 11,486 of 11,486 pass; `--coverage` OK, skipped on read 0.
- `knowledge/_edge_register.json` defaultActive row: note, verb line, `$measured` 15 / nulls 1 / to icon 14 (no drift line). `knowledge/_kg_verbs.json` defaultActive: note rewritten, nulls 15 → 1.
- `_compose_slice.py --selftest`: the same 6 reds lane E recorded (46, 57, 60, 62, 71, 73), none new; bite 45 (live reader agrees with the explorer) still passes.

## Renders (at the seat, file://, RENDER_SHELL)

- `notes/_lanes/308/L/L-tree-common.png` — showroom Tree page, Common pressed, note "12 token(s) · Common re-binds 2".
- `notes/_lanes/308/L/L-index-common.png` — the library index (the pack's picker), Common pressed.
- `notes/_lanes/308/L/L-bento-common.png` — foundations Bento page, COMMON pressed, `data-apollo-theme="legacy"` on the page.
- `notes/_lanes/308/L/L-kg-explorer-defaultActive.png` — explorer 1.32, assets on, dug on icon:alert: the defaultActive line to alert-active is drawn.
Drivers: `notes/_lanes/308/L/render_L.py`, `render_kg_L.py`.

## Things Dave should see

- The foundations generator (`gen_foundations_217.py`) was already out of sync with its pages before this lane: logos.html would drop from 12 to 8 variants, and five pages' Supercharge caption fallback would change from `#312C26` (warm) to `#313131` (grey) — that one looks like a regression in what the generator now resolves. It is not in CI. I did not regenerate those pages; each got only its picker line, which matches what the generator now emits.
- The showroom picker lists Common first (registry order: legacy is order 1). Unchanged; only the name moved.

## Verification

`gen_showroom --check` OK and `--selftest` 22 bites OK; `gen_library_214 --check` OK; `gen_theme_cascade --check`/`--selftest` OK; palette-tier, state-snap, dataviz-vars, bento-role-vars OK; `_wrap_regen --checks-only --session 308` fresh except `_gen_titles` (refuses until the wrap, as expected). `notes/_BUILD-VERDICT-LOG.jsonl` was clean at every commit.
