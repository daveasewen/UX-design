# #309 lane B — build the cards and tiles (Opus 5.5)

provenance: 309 · 2026-09-29 · conductor Opus 5.5 (cloud, linked to Dave's computer)
Dave's word to start: "go" (20:50 BST), on the conductor's opener naming pieces 1–5 below.

## Where you work
The repo is on Dave's computer, reached ONLY through the device shell tool
(mcp__remote-devices__device_bash). Every command starts `cd "$HOME/mnt/Projects--UX-design"`.
Each call is a fresh shell with a ~170 s cap; nothing survives between calls except files.
Nothing in the cloud workspace is the repo.

## The job — the rulings are the spec; quote them, never paraphrase
Read first: `knowledge/_rulings.json` ids s308-D34, s308-D39..D44 (verbatim text),
`notes/_lanes/308/DAVE-RULINGS-2026-09-29-1856-cards-and-tiles.md`,
`notes/_subreports/2026-09-29-308-O-ontology-research.md` § Round 3,
`notes/_RESEARCH-308-cards-tiles-containers-2026-09-29-v1.html` (the proposals he took),
`notes/_subreports/2026-09-29-308-E-edge-register.md` (where the edge register and ends check live),
`notes/_subreports/2026-09-29-308-L-common-and-icons.md` (the alias pattern: id kept, interfaces print the new name).
Work rows in the store (`python3 knowledge/_state.py`): W-308ir, W-308is, W-308it, W-308iu, W-308iv.

1. W-308ir (s308-D39, s308-D44) — the definitions and the five kinds: layout, HOUSING (not "holder"),
   record, block, part. Card = one of a set of like records; tile = one bento cell, surfaced, holding
   one thing. "Cell" = the grid position only (where it sits, what it spans); no surface, not a part.
   Every component meta declares one kind.
2. W-308is (s308-D40) — "accepts": each container's slots say which kinds they accept; the check refuses
   any containedBy line the parent does not accept. ADVISORY FIRST (warns, does not block), like every new check.
3. W-308it (s308-D41) — container = the register's umbrella word, never a component name except the layout
   utility; surface = a property (ground, border or none); panel = a region of the screen frame only;
   the chart-panel ROLE is renamed chart (check `knowledge/roles.json`, s252-D1, and its readers).
4. W-308iu (s308-D42) — stat card and KPI tile become one block, Metric, trend an optional slot, old
   names kept as aliases. ⛔ PROBE THE SCALE FIRST. If the merge ripples into `knowledge/canon/canon.css`,
   generated pages or render receipts, STOP piece 4, and report the blast radius in plain words
   (files, receipts, pages) — Dave said at #308 "you can still argue the other way if I'm not
   understanding the scale". Pieces 1, 2, 3 and 5 do not wait on it.
5. W-308iv (s308-D43) — the four nesting limits: a card never holds a layout, a housing or another record;
   a tile holds exactly one thing and never sits directly in a tile (nest through a bento); a carousel's
   slides all hold the same kind — these three REFUSE (advisory in the first run, per D40). A lone card
   is a tile — this one WARNS.
Then re-express s308-D34 (a carousel holds cards) as accepts rules, so the pair becomes derived.
Close each W-row through `_state.py`'s close gate only when its close condition is met; leave open what isn't.
Do NOT touch W-308iw (container types: section/division/sector) — that is Dave's word, not yet given.

## Scope (s172-D3 (a), verbatim)
"Use the minimum complexity that solves the current task. No abstractions for hypothetical future
needs. No defensive code for scenarios that cannot occur here. Make the changes requested and those
clearly necessary to them — nothing else."
Seam to prove: the accepts check refuses once, by name, on a real bad containedBy line (a mutant), and
passes on the real tree (control). One level deep. No checker for the checker.
Report `machinery: <n> instrument / <n> feature` lines.

## Traps on this mount (from _HANDOFF-159 — each has bitten)
- ⛔ NEVER run `git status`. After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 309-B`.
- ⛔ A no-op `git add` strands `.git/index.lock`. Name only paths that differ from HEAD.
- ⛔ Commits ONLY via `knowledge/_git_commit.sh`. Keep a commit under ~30 paths (~2 s a path to stage).
  Do NOT push — the conductor pushes and reads CI back.
- ⛔ `knowledge/canon/canon.css` is pinned by the 27 chart receipts — even a comment change needs
  `_drive_chart_engine.py --page …` re-driven. Avoid touching it; if you must, say so first in your report.
- ⛔ `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes run `--check`, then
  `--land --ratified s305-D26`. Mind the regen serial order (memory: regen-serial-set-is-ordered).
- ⛔ A targeted `_build_survey.py` run appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD
  before any chain/schematic regen.
- ⛔ CI's survey caps every step at 60 s — a new check must fit, timed at the seat.
- ⛔ Never `git checkout` a shared directory; scope any revert to files you own.
- ⛔ Writing JSON back with library defaults reformats the whole file — keep the file's own formatting.
- Do NOT run `_build_all.py` whole. Do NOT read or write Project memory.

## Report
File `notes/_subreports/2026-09-29-309-B-cards-and-tiles.md` (with a `COUNTS:` line), commit it.
Return to the conductor, in under 250 words: what landed per piece (1–5 + D34), commit hashes, the seam
proof (refusal name + control), what stayed open and why, and piece 4's blast radius if you stopped it.
