# LANE FO — BRIEF — WHO OWNS A DOUBLE-NAMED FILE: inscribe s281-D2 (the guideline family owns it; the builder declares the tie), fix the builder, light the 24. INSCRIBE + WIRE.
#281 · 2026-09-17 · conductor (Fable 5.1) · **model: opus** · bash root `/sessions/nifty-exciting-cerf/mnt/UX-design/`

## Dave's word, verbatim
Decisions export 11:58Z, `notes/_lanes/281/orphan-plan/DAVE-EXPORT-DECISIONS-2026-09-17.json`, q2 = (a), no note, not overruled. Option text ruled on, `DECISIONS-2026-09-17.html` #q2: **"The guideline family owns it; the builder declares the tie instead of resolving it by read order."** Earlier, orphan plan 11:02Z: `rules-in-the-constitution` = ruling.

## Read first (retrieval)
`notes/_lanes/280/orphan-census/REPORT.md` (set 06 / finding 3: three artefact nodes decide the fate of 24 rules; files `knowledge/guidelines/data-visualisation.md` 15 · `accessibility-interaction-design.md` 6 · `naming.md` 3) · `knowledge/_build_kg_explorer.py` at 1.21 — find WHERE a file's artefact node is minted and which pass wins when a ruling's `artefacts` and the rule index both name it (the census says governance runs first; verify, do not repeat) · `s277-D8` for the family vocabulary (governance / guidelines / guidelinerules keys do not move) · `notes/_subreports/2026-09-17-281-CM-chip-map.md` (1.21 base; note lane PH may be bumping the explorer to 1.22 in parallel — take the version that is in HEAD when you commit and say which).

## Do
1. **Inscribe `s281-D2`** in `knowledge/_rulings.json` by textual span (insert only, `N  0` numstat): id `s281-D2`, date 2026-09-17, by Dave, `says` = export ref + q2 (a) + the option sentence verbatim, `ruled` = a file under `knowledge/guidelines/` named by both a ruling's artefacts and the rule index is a GUIDELINE-family node; the builder DECLARES the tie (both claimants recorded on the node, e.g. `claimedBy: [governance, guidelinerules]`) and assigns family by what the file is, never by pass order; a ruling naming it still draws its artefact line to it. `governs` = the builder. `status` ruled.
2. **Fix the builder**: family by file kind + declared tie. General, not a three-file patch — any future double-named file follows the same rule. Say in the report how many files are tied today (expect 3) and list them.
3. **Explorer bump** (1.22 or 1.23 depending on PH): VERSION note. The tie should be readable in the node's INSPECT record.
4. **Prove it.** Census re-run: `rules-in-the-constitution` 24 → 0 at every-chip-on (Constitution off); no other set moves. Coordinate sets byte-identical if no node is added or removed (none should be — the same three artefact nodes, re-homed); if the layout moves, say why. `_validate_kg.py` green; page errors `[]`, served; 1280 light shot.

## Gates
Files: `knowledge/_rulings.json` (span insert), `knowledge/_build_kg_explorer.py`, `notes/_KG-EXPLORER.html`, `notes/_lanes/281/file-owner/`, the filed report, `_state.json` row if asked. **Do not touch `obeys`/`held`, the principles family, or lane PH's files. If PH has committed before you, rebuild on its HEAD.** `/sessions` 99%: scratch under `/sessions/nifty-exciting-cerf/mnt/outputs/fo/`, removed at the end. Never `git stash` / `gen_kg_edges.py` / `_build_all.py`. Locks → `mv` to `.git/_orphan-locks/`, never `rm`. If the working tree is mid-commit from another lane, wait and retry — do not force.

## Report — `notes/_subreports/2026-09-17-281-FO-file-owner.md`, evidence under `notes/_lanes/281/file-owner/`. Plain prose first. COUNTS · ruling-shaped · UNPROVEN · REPLAY-THESE.
Commit via `SESSION_N=281 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…> < /dev/null`, msgfile `/tmp/_msg-281-FO-$(date +%s).txt`, subject `#281 lane FO: the double-named file — s281-D2 inscribed, N files tied, 24 dark rules → M`. Do not push. Return ONLY a stub.
