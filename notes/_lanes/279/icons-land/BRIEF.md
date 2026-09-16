# LANE IL — BRIEF — land the icons: A3/A4 pre-land fixes, open the door, `--land --ratified s277-D4`
#279 · 2026-09-16 · enacting `s277-D4..D7` · written by the conductor (Fable 5.1) · **model: opus** · LAND, then a Fable verify lane reads the live tree

## Rulings (read them whole in `knowledge/_rulings.json`: `s277-D4`, `s277-D5`, `s277-D6`, `s277-D7`, and `s278-D1` for context only)
- **D4**: three node kinds — `icon:` (666) · `iconGroup:` (10) · `logo:` (12) = 688 nodes, behind an `assets` chip OFF by default, landed by `gen_kg_icons.py --land --ratified` on THIS id. Declared nulls carried, never dropped.
- **D5**: `usesIcon` from the geometry byte-match (371 / 105 / 81); `usesLogo` 18, `inGroup` 666, `ruledBy` 8, `defaultFor` 2. `themedBy` DECLINED. The prose/slug-as-word route REFUSED.
- **D6**: the 15 bases with 2–3 actives carry **NO `activeVariantOf`**; each of the 31 is a declared null. Dave reviews the 15 manually (`P-277-3`, parked). Do not invent a twin.
- **D7**: all 12 logos enter; the two `s230-D2` names carry `defaultFor`; the 10 unbound lockups carry a declared-null `governedBy` each.

## The generator and its verdicts
- `notes/_lanes/277/icons-propose/gen_kg_icons.py` — read its docstring (lines 1–80) and `land()` (~line 690) before touching anything. `RATIFIES = ()` at line 172 is the door.
- `notes/_lanes/277/icons-verify/VERIFY.md` — Fable's verify. **A3 and A4 are pre-land conditions on you** (lines 54–60):
  - **A3**: the `defaultFor` residue null (`app-shell-nav-rail`) is found by a substring-over-English test (`for slug in sorted(metas): if slug.lower() in low and slug not in bound`). Anchor it on the ruling's own clause instead — `s230-D2`'s `says` literally reads "App-shell-nav-rail deliberately NOT rebound" — or declare the residue by name against `s230-D2`. Then **add a bite** proving a second substring slug does NOT produce a null.
  - **A4**: `meta.schema.diff` bakes live integers (758, 371, 105, 81, 102, 835, 18, "Measured live") into schema description text that would go stale on the first regeneration. Keep the four limits, drop the counts (or mark them "at 5520d43"). Fix the diff AND whatever in the generator emits it.
- The generator's own `--selftest` (17 bites) and `_mutate.py` (25 mutants) must stay green after your edits; A3's new bite makes it 18.

## Steps, in order
1. Copy nothing. Edit `gen_kg_icons.py` in place under `notes/_lanes/277/icons-propose/` (it is the record of the proposal; the land is its next commit) — A3, A4, then `RATIFIES = ("s277-D4", "s277-D5", "s277-D6", "s277-D7")`. Update the docstring lines that say the door is shut (62–64, 170, 694, 975, 1112, and the bite-12/bite-17 assertions that assume `RATIFIES == ()` — rewrite those bites so they test the door with the allowlist OPEN: refuse for no id / malformed / unrecorded / a live id NOT in the list, land for `s277-D4`).
2. `--selftest` → 18/18. `_mutate.py` → 0 survivors (add a mutant for the A3 anchor).
3. `--dry-run` into scratch; assert `_icon_nodes.json` / `_logo_nodes.json` byte-identical to the committed proposal copies EXCEPT where A3/A4 legitimately change bytes — name every differing byte in the report.
4. `python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --land --ratified s277-D4` → writes `knowledge/_icon_nodes.json` and `knowledge/_logo_nodes.json`. Counts assert: 688 nodes (666/10/12), 1,299 edges (666/234/371/18/2/8), 32 declared nulls, 0 `activeVariantOf`, 0 `themedBy`.
5. `python3 knowledge/_validate_kg.py` (or whatever the tree's KG validator is — find it, do not guess) on the live tree. If the validator does not yet know the three kinds, that is the **grammar +3 kinds by addition** — add them by textual addition, never rewriting an existing kind, and say so.
6. **Explorer chip: NOT this lane.** Do not touch `knowledge/_build_kg_explorer.py` or `_KG-EXPLORER.html`. Report what the chip lane will need (the two node files' shape, the edge names, the family key you would use — `assets` is taken? check `RULE_FAM`'s note at line 113).
7. `git status` must show changes ONLY under `notes/_lanes/277/icons-propose/`, `notes/_lanes/279/icons-land/`, `knowledge/_icon_nodes.json`, `knowledge/_logo_nodes.json`, and the grammar file if step 5 needed it. Anything else dirty that you did not touch (`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` are already dirty — leave them unstaged).

## Report — `notes/_lanes/279/icons-land/REPORT.md` + a copy at `notes/_subreports/2026-09-16-279-IL-icons-land.md`
Every gate line verbatim · the A3 mechanism you chose and the bite that proves it · the A4 bytes dropped · counts · the byte-diff of step 3 · what the chip lane needs · `git diff --numstat` **re-read from the SHIPPED sha** after the commit. One commit via `SESSION_N=279 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…>` — a FRESH msgfile per attempt (`/tmp/_msg-279-IL-$(date +%s).txt`), subject line bare, NO "after #279" prefix (the script adds it). Subject: `#279 lane IL: icons landed — s277-D4..D7, A3/A4 pre-land fixes, 688 nodes / 1,299 edges`.
Never `git stash` · never `gen_kg_edges.py` · never `_build_all.py` · never `_build_kg_explorer.main()` · stale `.git/index.lock` → `mv` to `.git/_orphan-locks/`, never `rm` · `pip install tiktoken --break-system-packages` if any gate asks for it · paths in bash are under `/sessions/laughing-elegant-feynman/mnt/UX-design/`.
