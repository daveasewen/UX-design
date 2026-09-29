# #309 lane C — the two rulings, the reclass, Metric built properly, the explorer (Opus 5.5)

provenance: 309 · 2026-09-29 · conductor Opus 5.5 (cloud, linked to Dave's computer)
Dave's words: `notes/_lanes/309/DAVE-WORDS-2026-09-29-2137.md` ("1. good" / "2. go", 21:37 BST).

## Where you work
The repo is on Dave's computer, reached ONLY through mcp__remote-devices__device_bash. Every command
starts `cd "$HOME/mnt/Projects--UX-design"`. Each call is a fresh shell, ~170 s cap; split long jobs
into steps that leave files behind. Nothing in the cloud workspace is the repo.
Rendering: every render runs at the seat in ONE call — `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh;
source knowledge/_render/seat_env.sh; python3 <driver>` with executable_path=$RENDER_SHELL. Use `goto("file://…")`,
never `set_content()`. `outputs/308/drive_seat.py` is the wrapper #308 used for `_drive_chart_engine.py` at the seat.

Read first: lane B's report `notes/_subreports/2026-09-29-309-B-cards-and-tiles.md` (the model, the check,
the Metric blast radius), its brief `notes/_lanes/309/B/BRIEF.md` (the traps list applies to you in full),
and `knowledge/_rulings.json` s308-D39..D44.

## Pieces, in order — commit after each
1. INSCRIBE his two answers as s309-D1 and s309-D2 through `knowledge/_inscribe_ruling.py` (entry file,
   `--dry-run`, then `--write`), in lane I's shape (`notes/_subreports/2026-09-29-308-I-inscribe-15.md` line 15):
   `ruled` opens with the answer in capitals; his words verbatim ("good" / "go"); the call's text verbatim
   from the words file; `says` = chat #309 21:37 BST + the words file; `governs` = the rows touched +
   `knowledge/_state.json`; `evidence` = the words file, lane B's report. Answers given in chat, not by
   click — say "in chat", never "by click".
   - s309-D1: tabs, accordion and popover are BLOCKS, not housings.
   - s309-D2: Metric is rebuilt properly — one block, canon and the 27 chart proofs re-run (enacts s308-D42, W-308iu).
2. RECLASS tabs, accordion and popover to kind `block`. The accepts check (`_validate_edges.py --check`)
   must then read 0 refusals on the real tree — that is the clean control lane B could not give. Stamp
   s309-D1 enacted with the commit's sha if the tool's shape allows (lane I used `--set-status … --evidence-sha`).
3. METRIC (s308-D42, s309-D2, W-308iu): stat card and KPI tile become ONE block, Metric; the trend is an
   optional slot; `stat-card` and `kpi-tile` stay as aliases (the pattern lane L used for Common/legacy and
   lane B's alias seats). Change sources and let generators write their outputs — never hand-edit a
   generated file. canon.css changes mean the 27 chart receipts are re-driven (`_drive_chart_engine.py --page …`,
   one page per call if needed) and every receipt reads green again. Designer-pack files: regenerate through
   their own build if one exists; if they are a frozen release, leave them and say so.
   Close condition needs a render WITH and WITHOUT the trend: render both side by side on one PNG at 1440,
   saved beside the source, for Dave to rule by eye. Close W-308iu only when its stated close condition is met.
   Every figure on a rendered page comes from canon, never from a specimen.
   ⛔ Dave's standing fence: "careful of externalities, I don't want to fix something only to break other
   constituent parts." If the merge would break a gate you cannot make green again, STOP, leave the tree at
   the last green commit, and report what broke and why.
4. THE EXPLORER (only if 1–3 are done): `notes/_KG-EXPLORER.html` still shows `role:chart-panel`. Its build
   runs past the shell cap in one call — split it into steps that each finish under ~150 s, or find the
   build's own chunking. Rebuild it so it shows `chart` and the new kinds.

## Scope (s172-D3 (a), verbatim)
"Use the minimum complexity that solves the current task. No abstractions for hypothetical future
needs. No defensive code for scenarios that cannot occur here. Make the changes requested and those
clearly necessary to them — nothing else."
Seams to prove: (2) the accepts check reads 0 refusals on the real tree; (3) all 27 chart receipts green
after the canon change, and the two Metric renders exist. Report `machinery: <n> instrument / <n> feature`.

## Traps (from _HANDOFF-159 and lane B — each has bitten)
- ⛔ NEVER `git status`. After every gate run: `python3 knowledge/_wrap_commit.py unlock --tag 309-C`.
- ⛔ A no-op `git add` strands `.git/index.lock`. Name only paths that differ from HEAD. Under ~30 paths a commit.
- ⛔ Commits ONLY via `knowledge/_git_commit.sh`. Do NOT push.
- ⛔ `gen_kg_sources.py` is not in `_wrap_regen.py`'s serial: after meta changes `--check`, then `--land --ratified s305-D26`.
  After records change, `_wrap_regen.py --checks-only --session 309` names what is stale; run their write forms in its order.
- ⛔ A targeted `_build_survey.py` run appends to `notes/_BUILD-VERDICT-LOG.jsonl`; restore it from HEAD before any regen.
- ⛔ CI's survey caps each step at 60 s. ⛔ Never `git checkout` a shared directory.
- ⛔ Keep each JSON file's own formatting when writing it back.
- Do NOT run `_build_all.py` whole. Do NOT read or write Project memory. Do not ask Dave anything.
- Clear your own leftovers in ignored `outputs/309/C/` at the end (lane B left 95 MB in `outputs/309/B/` — remove that too).

## Report
File `notes/_subreports/2026-09-29-309-C-metric-and-reclass.md` (with a `COUNTS:` line), commit it.
Reply to the conductor in under 250 words: what landed per piece, commit hashes, the seam proofs,
the path of the Metric with/without-trend PNG, what stayed open and why.
