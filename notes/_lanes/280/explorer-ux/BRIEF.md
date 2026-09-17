# LANE EX3 — BRIEF — explorer 1.19: the legend stops jumping, and every list item gets INSPECT (a modal that shows the record)
#280 · 2026-09-17 · conductor (Fable 5.1) · **model: opus** · bash root `/sessions/intelligent-serene-curie/mnt/UX-design/`

## Dave's words, verbatim (with screenshots of 1.18 dark)
- *"The legend jumps from the side to the bottom when you interact with it."*
- *"Could the have a 'inspect' button on the list items that actually summon the file in a modal."*

## Read first
`notes/_subreports/2026-09-16-279-EX2-explorer-fix.md` §1c/§2 (WHY the legend moves: column while portrait, strip once a family chip makes it landscape) and `notes/_lanes/280/layout-matrix/REPORT.md` (1.18 switch, cells, gates, sim identity method). Files: `knowledge/_kg_explorer.template.html`, `knowledge/_build_kg_explorer.py`.

## 1. The legend does not move by itself
The auto-move is the defect as he experiences it. Rule: the legend's place is STICKY — it stays where it is until the user moves it. Give it a small `⇥ side / ⇣ bottom` toggle in its bar (and remember the choice in `localStorage` under `kg-legend`, next to `kg-theme`). Initial place: side when the shown extent is portrait, bottom when landscape — computed ONCE at load and at a layout/dimension switch only, never on a chip toggle, a dig, or a scrub. `fit()` still uses `usable()` from wherever the legend is. Phone sheet unchanged.

## 2. INSPECT on list items
Every node row in the aside (search results, the dig panel's groups, the path list) gets an `inspect` affordance (a small button at the row's right edge; also `i` on the keyboard for the focused node). It opens a MODAL (not a new page) with: the node's full stored record — every field the embedded KG carries for it, rendered as a definition list, not raw JSON — its edges grouped by type with the verb's wording (`_kg_verbs.json`), and a **File** section: the node's source path (`file` / `governs` / the meta path the builder knows). ⚠ The page is opened from disk (`file://`) and from a server; `fetch()` of the source file works only when served. So: try the fetch; if it succeeds, render the file's contents in the modal (markdown → light rendering; JSON → pretty; CSS → mono); if it fails, show the path with a copy button and say *"open from the repo"* — never a blank or an error. Escape / click-outside closes; focus trapped while open; the modal is the same in all six cells and both themes.
Do NOT embed file contents in the page — the build measures its own size and the size is a gate.

## Gates
Version 1.19; regenerate `notes/_KG-EXPLORER.html` via `python3 knowledge/_build_kg_explorer.py` only. Default canvas md5 identical to 1.18 · LY's sim identity on coordinates · driver: chip toggle ×3, dig, scrub → legend rect unchanged; toggle → moves; reload → remembered; inspect modal opens on a search row, a dig row and a path row, closes on Escape, contents present, fetch-fail path shows the path (run once never-driven from `file://`, once served with a tiny `python3 -m http.server` on a scratch port, killed after) · page errors `[]` · screenshots 1280 light+dark: legend side, legend bottom, modal open (served) and modal fallback (`file://`). `/sessions` at 99%: download NOTHING, never copy `knowledge/`, scratch under `/sessions/intelligent-serene-curie/mnt/outputs/ex3/`, removed at the end.

## Report — `notes/_lanes/280/explorer-ux/REPORT.md` + `notes/_subreports/2026-09-17-280-EX3-explorer-ux.md`; `_state.json` add `W-280ex` (close = Dave has seen the legend stay put and opened a modal). Plain prose first.
Commit via `SESSION_N=280 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…> < /dev/null`, msgfile `/tmp/_msg-280-EX3-$(date +%s).txt`, bare subject `#280 lane EX3: explorer 1.19 — the legend stays put, and INSPECT opens the record in a modal`. Regenerate `_CHAIN.md` if the store row trips the chain gate. Locks → `mv` to `.git/_orphan-locks/`. Never `git stash` / `gen_kg_edges.py` / `_build_all.py`. Do not push. Return: report path, sha, three plain-prose sentences.
