# LANE IX — BRIEF — icons (666) then logos (12): the measured shape, no decisions
#277 · 2026-09-15 · prep for `s269-D1` STEP 4 · written by the conductor · **model: opus** · READ-ONLY, NO REVIEW PAGE

## Why you exist
`s269-D1` step 4 is **icons then logos**. Dave deferred it at #276 with *"maybe we just tie off these loose ends first."* Quota is not binding this week and his decision load is. So this lane spends tokens, **not his attention**: you produce the measured shape and the costed options so that when he says go, the build lane is one word away.

⛔ **You produce NO review page and NO decisions for Dave.** One file: `notes/_lanes/277/icons/FINDINGS.md`. Nothing lands. Nothing under `knowledge/` is written.

## Read first
1. `notes/_lanes/269/kg-gaps/A-inventory.json` — the `assets — icons` and `assets — logos` families. Their `how_measured` commands are your baseline: **re-run every one and report whether the figure still holds** (it was measured 2026-09-14; the tree has moved).
2. `notes/_lanes/274/` and `notes/_lanes/275/` REPORT.md — the RK/RL lane shape steps 2 and 3 used (propose → verify → land). Your options must fit that shape.
3. `knowledge/assets/icons/icons.manifest.json` · `_README.md` · `dynamic-weight/icon-weight-decisions.json` · `knowledge/tokens/icon-scale.json`.
4. `knowledge/assets/logos/` (12 SVGs + `_export-logos.py`) and `knowledge/guidelines/logos.md` if it exists.
5. `knowledge/_build_kg_explorer.py` — how nodes/edges are extracted and what a new kind costs there.
6. Rulings `s212-D9` (icons, superseded-by) and `s230-D2` (logos — Dave verbatim: *"use this as teh default logo \"masterbrand-light-colour\""* / *"use this for dark mode masterbrand-dark-colour"*).

## What to measure — icons
- 666 manifested SVGs across 10 groups (Misc 24 · Social 7 · Touch 10 · Informative 131 · Volume/audio 16 · Media 104 · Arrows/chevrons 24 · Products/services 208 · Global controls 122 · Status 20). **Confirm or correct every one of those figures.**
- The `active` flag pairing: how many icons have an `-active` twin, how many are orphaned either way. ⚠ #264 repaired glyph twins and derived 8 `-active` glyphs — check the manifest agrees with what shipped.
- `fillMode == "currentColor"`: how many, and which colour tokens they would inherit. Zero token nodes exist in the graph today — so say plainly what `icon→token (themedBy)` would require FIRST.
- How many of the 138 component metas actually name an icon, and whether that mention is joinable (a slug? prose only?). **This is the crux: `icon→component (usedBy)` is worth little if the join is a regex over prose** — that is the exact route `s274-D12` and `s276-D5` refused. Say honestly whether a defensible join exists, and if it does not, say that the edge cannot be built yet.

## What to measure — logos
- The 3 × 2 × 2 grid (masterbrand | masterbrand-identifier | hexagon × light|dark × colour|mono). Confirm all 12 and the filename regularity.
- `s230-D2` already states the default edge in his own words. Say exactly which two of the twelve it names and what the remaining ten would be bound by.
- How many metas mention a logo, and whether app-shell / header / footer are joinable by anything other than prose.

## FINDINGS.md must contain, in this order
1. **The corrected inventory** — every A-inventory figure re-run, with the command and the delta (or "unchanged").
2. **Node kinds, costed** — for icons: `icon` (666) vs `iconGroup` (10) vs both; for logos: `logo` (12). For each: nodes added, explorer impact, whether `_validate_kg.py`'s grammar needs extending and how much (it was extended by ADDITION at #276 — mirror that).
3. **Edge kinds, ranked by defensibility** — for each candidate edge: the join it rests on, whether that join is structural (manifest field, filename) or prose (a regex — then say REFUSED and why), and the count it would produce. **Rank by whether it can be authored, not by how many edges it makes.**
4. **The blockers** — anything that must exist first (token nodes for `themedBy`; a fonts manifest; a guideline doc). Name each and say whose it is.
5. **A proposed two-lane plan** — what an RK-shape propose lane would do and what its review page would ask Dave, in **≤ 4 decisions**, drafted as one-liners. This is a DRAFT for the conductor, not a page.
6. **Gauge at close** and every gate line you ran.

## Gates
`python3 knowledge/_validate_kg.py` must be OK (you changed nothing) · `git status` shows changes ONLY under `notes/_lanes/277/icons/`.

## Cautions
Never `git stash` · never `gen_kg_edges.py` · never `_build_all.py` · textual span only · stale `.git/index.lock` → `mv` to `.git/_orphan-locks/` · commit serially, other lanes are running in this wave · one commit at the end, `#277 2026-09-15 — lane IX: …`, with `--numstat` in the report.
