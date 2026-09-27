r = r"""# #305 C2 - the commit seat, wave two: committed 1e107eea, stamps commit on top, nothing pushed

provenance: 305 · 2026-09-27 · C2 (Opus 5.5 sub of the #305 conductor), the only git writer of wave two, at Dave's seat through `device_bash`; no `git status` in any form, no push, no CI read, no Project memory
status: observed (FINAL copy - replaces the interim copy committed in 1e107eea; rides the stamps commit, whose own sha is in the conductor's hand-back, not here)
CITES: `notes/_lanes/305/_COMMON-BRIEF.md` · `_HANDOFF-155-*.md` § THINGS A COLD SEAT SHOULD KNOW · reports 305-H1, H2, K (post-Y2 block), V2 · `notes/_lanes/305/A/CALL-MAP.json` · `notes/_subreports/2026-09-27-305-C1-commit.md` (the model)
machinery: 0 instrument / 0 feature (lane-dir scripts only)

## The answer first

Wave two is committed locally as **`1e107eea2101dfbf7ddf2475ac890ecb8aa68be6`** (134 files, the seven deck checkers recorded as R100 renames). The stamps commit sits on top of it (eleven s305 rulings marked enacted, the rulings page, the chain, the schematic and the explorer regenerated). **Nothing is pushed: origin/master is still `568e2534`**, and the local range above it is X `0ef30746` → Y1 `02d679b3` → Y2 `d3b809a7` → `1e107eea` → the stamps commit. No lock was stranded; none moved. The wrap gate inside the committer read **`242 in scope · 0 fail`**: H2's 130,000 boot ceiling closed the standing boot-ceiling fail, as H2 predicted.

## Before the commit (in order)

1. **State checked, not assumed.** C1's untracked tail had already ridden X (`0ef30746`), so it was not re-named. `knowledge/_graph-mark-observations.jsonl` is CLEAN (X carried it with lane A's 8 and K's 14 lines), so it is not in either commit; the `[131]` schematic-determinism cause C1 found is closed by X, not here.
2. **Store rows minted before the first attempt** (`mint_305c2.py`, `_state.add` + `save`, `check()` ok, 916 → 920): **W-305hr** (H1; `W-305h1..h4` were taken by H1's split rows), **W-305hc** (H2), **W-305v2** (V2), **W-305c2** (this seat). The doc-row gate passed, no `DOC_ROW_ACK`.
3. **Regens** (`step2-regen.log`, all rc 0): `_build_memento_index` first (`_CARRIES.md` changed), then the serial `_render_rulings` → `tokens/_build_blast_radius` (did not move) → `_build_memento_index` → `_build_graph_mention_map` → `_gen_chain` → `_gen_schematic`. `gen_dashboard --check` read OUT OF SYNC after H1's store writes, so `gen_dashboard` was re-run (C1's precedent). Every `--check` FRESH after (`step3-checks.log`). Release-audit `--manifest-check` PASS and frozen-release PASS (3 arms) on the tree before committing.
4. **Every named path checked changed-or-untracked** by `paths_c2.py` (140 of 140), built from the four reports' lists.

## The commits

- **`1e107eea`** `after #305 2026-09-27 — 305 wave two: H1's records diet, H2's lines, ceiling, regrowth switch and CI calls, K's post-Y2 tail, V2's verdict on the zip` — declared not-a-wrap; 89 s, exit 0, `✓ done — locks clear`. `notes/_REHEARSAL-LOG.jsonl` auto-staged by the committer, declared. Transcript `notes/_lanes/305/C2/_gitcommit-C2.{log,term}`.
- **The stamps commit** — `_rulings.json`, `notes/_RULINGS.html`, `_CHAIN.md`, the memento schematic, `notes/_KG-EXPLORER.html` (rebuilt, 151 s, v1.30, 5,485 nodes / 10,573 edges; it bakes each ruling's status, and H1 moved 76 statuses plus these 11), this final report and C2's tail. Every `--check` FRESH after (`step6-checks.log`).

## The stamps (`stamp-dry.log`, `stamp-write.log`)

`_inscribe_ruling.py --set-status <id> "<enacted … note>" --evidence-sha <sha>`, 11/11 dry-run clean, then 11/11 `--write` rc 0. Ids from CALL-MAP, each checked against its `ruled` text; H1's report ids matched CALL-MAP (call n → s305-Dn for 28-41). Each status carries a one-line note of what landed and what, if anything, is still the ruling's own later step.

- **s305-D2** (call 1, the cut) at Y1 **`02d679b3`**. The note says the push and CI read-back are still owed and that V2 reads DO NOT SHIP to the audience.
- **s305-D30** (call 30, the credential helper) at wave one's **`27efb7b6`**. C1's report shows it was done at the seat in wave one; no commit carries it, because it lives in `.git/`. The note says so, and names the push of `568e2534` through the helper and H2's `--push` fix in `1e107eea`.
- **H2's calls at `1e107eea`: s305-D28, D29, D40, D41.** The D29 note keeps the Mac-seat re-measure as the ruling's own later step. The D40 note says births are closed from #306, not #305, and why (H2's reason).
- **H1's fully discharged calls at `1e107eea`: s305-D31 (95/95), D34 (17/17), D35 (14/14), D37, D39.** For D37, 19 of the 20 pages are parked and W-298 was closed under D31. It is not live either way, and the note says so.

**Left ruled on purpose:**
- **s305-D32** (call 32): the parking is done, but putting the scan page to Dave is the conductor's.
- **s305-D33** (call 33): 20 of 22 closed, and W-222 and W-272 are parked instead, because they are also on the call-32 scan.
- **s305-D36** (call 36): 324 of 342 dropped, 18 held on purpose.
- **s305-D38** (call 38): kinds 1-4 and 36 of kind 6 are done; kind 5 and 28 of kind 6 are left. H1 flags s229-D3 as looking BUILT at baf5458e.

Store after: s305 rulings 35 enacted · 21 ruled · 1 standing (57).

## W-305k, the cut row: NOT closed

Its condition is "a cold verifier … has opened the real v1.0.14 zip and filed … , **the three commits are pushed with CI read back**, and s305-D2 is stamped enacted". V2 has filed and D2 is now stamped, but the push and CI read-back are not this seat's job, so the row stays open. Separately, **W-305c1's condition looks met** (its final copy rode X `0ef30746`), but it is still open. Closing it was not in this brief, so it is left for the conductor.

## The regrowth check (s305-D40), live

`python3 knowledge/_state.py` at this seat: **`Regrowth arming (s305-D40): 57 of 75 pinned document rows still live`**. It is not armed. It arms and turns BLOCKING by itself when that reaches 0, and at that point **W-303h, W-304a1, W-304a2, W-304a3 and W-304a4** (outside the pin, closing on #304 events) would be refused unless they are closed or restated in the same batch. The advisory REGROWTH note names 62 live rows.

## Held (not in either commit), by name

- H1: `notes/_lanes/305/H1/backup/{_state.json,_rulings.json,_parked.json}.pre-H1` (revert copies). `residual-305-pre-diet.txt` IS committed, because `_CARRIES.md` cites it.
- H2:
  - `notes/_lanes/305/H2/_stray/`: two extracts another session left in /tmp.
  - `notes/_lanes/305/H2/backup/`: revert copies, held like every lane's backup. It includes copies of the gitignored `knowledge/_tmp/ci29x` scratch.
  - The gitignored `knowledge/_tmp/`.
- K:
  - `notes/_lanes/305/K/{cold,restage,dist,backup}/`.
  - ⚠ **`notes/_lanes/305/K/_gitcommit-Y2.{log,term}` and `_msg-Y2.txt.t3-rendered`**: Y2's own transcripts. No report names them, so they were held under the brief. By the X/Y1/Y2 pattern they are the natural tail of the next commit.
- V2: `notes/_lanes/305/V2/cold/` and `cold13/` (the two unzipped packs, about 96 MB).
- Wave one's holds: B1's `backup/ work/ fix/`, B2's `backup/`, C1's `backup/`, V1's `before/ after/`.
- `_HANDOFF-155`'s other-seat set:
  - `notes/_dream/_MEMORY-GRADES.json` and `_GRADE-DECISIONS.jsonl`
  - `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md`
  - `notes/_lanes/294/WRAP-MEMORY-HOOK.md`
  - `notes/_subreports/2026-09-22-297-A-plain-deck-brain-and-footnotes.md`
  - `notes/_lanes/304/W/_gitcommit-W5b.{log,term}`
  - the untracked `UX-design/`, `notes/_context/`, lane work under `notes/_lanes/265`, `286` and `297`-`304`, `notes/_lanes/304-sq/`, its report and four receipts, `notes/_subreports/assets/2026-09-0{5,6}-*/`
  - #304's `*.pre-W3a.*` and `*.pre-W4b.*` copies

## For the conductor (not repaired; outside this seat's fence)

- **V2's verdict is Dave's call:** the zip is sound but ships s305-D45..D55. Hand nothing over until he rules on s279-D1 against W-305n6. `showroom/_foundations/logos.html` has four broken images.
- **H2's leftovers:**
  - `knowledge/_standing.md:19` still says 180,000.
  - The capture-ritual runbook should say "born done" from #306.
  - s305-D41's text quotes the old step numbers (the current ones are 92, 133 and 134).
- **H1's leftovers:** GOOD-MORNING.md l.34 and `_CHAIN.md` l.59 type 715, but the probe reads 391.

## Paths written by this seat

- `knowledge/_state.json` (4 rows) and `knowledge/_rulings.json` (11 stamps)
- the regen outputs: `_CHAIN.md`, `knowledge/_memento-index.json`, `knowledge/_graph-mention-map.json`, `notes/_RULINGS.html`, `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html`, `dashboard/index.html`, `notes/_KG-EXPLORER.html`
- `notes/_lanes/305/C2/**` and this report
"""
open('notes/_subreports/2026-09-27-305-C2-commit.md','w').write(r)
print(len(r))
