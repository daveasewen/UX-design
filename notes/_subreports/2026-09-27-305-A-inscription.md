# #305 A — the inscription seat: Dave's 2026-09-27 sitting inscribed as s305-D1..D56, six threads minted, Friday recorded

provenance: 305 · 2026-09-27 · lane A (Opus 5.5 sub of the #305 conductor), at Dave's seat through `device_bash`; no git write, no git status, no Project memory, no regen serial
status: observed
CITES: `notes/_lanes/305/_COMMON-BRIEF.md` · `notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md` (his export, 14:53 BST) · `notes/_SITTING-304-tuesday-2026-09-29-v1.html` (committed at 52049781) · #304 reports C2, C4, C5, C6, F5, V3, V4, V5, W4a, W5a, W5c, J, R3, R4b, M, R5 · the six `notes/_DECIDE-304-*` pages
machinery: 0 instrument / 0 feature (two one-off scripts in the lane dir, nothing wired)

## The answer first

`knowledge/_rulings.json` went **638 → 694** rulings (json.load over `rulings`), ids **`s305-D1`..`s305-D56`**, all 56 through `knowledge/_inscribe_ruling.py` — each dry-run first (56/56 clean), then `--write` one at a time (56/56 rc 0, reconstruction proof PASSED every time; log `notes/_lanes/305/A/inscribe.log`). `git diff --numstat`: **972 insertions, 0 deletions**. After the writes: `_governs.py --selftest` all bites green; `_inscribe_ruling.py --selftest` all arms green; every anchor pointer resolves to exactly one line; every commit pointer resolves (`git cat-file`); no pointer aims into a rolling file (R6). Six new store rows **W-305n1..W-305n6** through `_state.add` + `_state.save` (899 → 905 items, `check()` ok, diff +102/−0). Friday recorded verbatim. `CALL-MAP.json` written for every call.

## Numbering

`s305-D1` = the standing rule (his 13:59 BST words). Then one ruling per ANSWERED call in page order: calls 1–26 = D2–D27; **call 27 = nothing inscribed** (comment only); calls 28–41 = D28–D41; 41b = D42, 41c = D43, 41e = D44; calls 42–53 = D45–D56. Call 6 is one ruling, as the page asked. `notes/_lanes/305/A/CALL-MAP.json` is the lookup (call → id, status, needs_build, one-line what-to-build).

## Status by call

- **standing** (lead word already in the store): D1.
- **enacted, ratifying what is already in the tree** (5): call 3 = D4 @ `4be130e5` (both gates built advisory, steps 147–148, exit 77; confirmed advisory at HEAD in `_build_all.py` and both gates' `sys.exit(77)`) · call 6 = D7 @ `3100da99` (thinning, declared without a ruling in that commit's body) + `52049781` (right-hand twin) · call 13 = D14 @ `4be130e5` (s245-D10 stamped at aaf3bb7e) · call 41c = D43 @ `52049781` (today's trim, F5's narrowing, V5 verified) · call 53 = D56 @ `52049781` (1,203 derived titles). Each carries a `commit <sha> - …` pointer, so `s295-D2`'s enacted-sha check counts them proven. ⚠ Calls 3 and 41c are beyond the brief's example list: both decide "keep what is in the tree", the tree already holds it, and the receipts are clean, so they follow the brief's rule for ratifying calls.
- **ruled** (everything else, 50).

## Where the brief's reading and the page differed — flagged, not smoothed

1. **Call 41e is NOT "as built".** The page's recommendation (which his "yes" takes) is code ALONE on the canvas, title kept in search / panel / INSPECT, and title the 49 bare labels. Wave five built code AND title on the canvas. So D44 is `ruled`, needs_build: one template line in the explorer + three more kinds in `gen_kg_titles.py`.
2. **Call 52 is NOT built.** Seat J ran a 50-edge probe; the hand-run sweep script under `notes/` that the ruling adopts does not exist yet ("What runs next … A sweep script under notes"). D55 is `ruled`, needs_build.
3. **Supersessions named in `ruled`, earlier entries untouched:** D28 crosses out the figures of `s271-D1`, `s272-D93`, `s260-D2`; D29 supersedes `s295-D3` until the Mac seat (shrink-only of `s240-D2`/`s241-D1` resumes from the Mac-seat reading); D39 supersedes `s135-D3` (retired) and parks `s114-D2`, `s246-D3`; D26 amends `s269-D6` (lifecycle a field, content standard parked) and discharges `s269-D1`'s step-5 clause; D10 amends `s219-D1`'s shipped default within `s219-D3`'s rails (the when-rules page's reading); D3 moves the roster the manifest holds at 58 (`s223-D6` lineage) to 60. D48 (Launchpad) and D50 (October) cross out the PROPOSAL's "Apollo Live" and "now" — the proposal is not a ruling, so no store id is superseded.
4. Call 45's answer and call 47's/50's hedges are quoted whole, newlines and hedges kept.

## Still Dave's after this sitting (not decided by any yes)

Call 27 (visuals owed, W-305n4) · call 18's four clashes for his eye (data grid, lightbox, stepper, tab bar) · call 26's token name (#145 precedent) · call 24's rule wording · call 10's grey by eye at the wrap · call 38's two green values for the eight no-trace stamps · call 3's re-look after one cold run · the three comment threads W-305n1/n2/n3 · the Friday surprise W-305n6.

## New store rows (all `project: apollo`, `opened: 305`, `state: open`, `condition: stated`)

| id | owner | thread | home |
|---|---|---|---|
| W-305n1 | dave | call 6 comment — labelling rules for complex charts (5 columns, 3 labels, two keys) | export `#06 · Thinning the category` |
| W-305n2 | dave | call 8 comment — donut not responsive but not fixed; 4px-grid bands at build, editable in edit mode | export `#08 · A ring` |
| W-305n3 | dave | call 29 comment — boot efficiency, and return to improving the wrap | export `#29 · The boot ceiling` |
| W-305n4 | claude | call 27 — visuals owed before he can rule | export `#27 · Two things the skill lane widened` |
| W-305n5 | claude | call 32 — surface the 102 parked questions for his scan | export `#32 · Park 102 ruling-shaped questions` |
| W-305n6 | dave | Friday — the Launchpad PoC is a surprise; nothing on shared material | `notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md` |

Ids use the `n` suffix because `W-305` already exists (a #229 row); `ID_RE` allows two suffix characters.

## ⚠ For the commit seat — these MUST ride the same commit

The new rulings' evidence and the new rows' homes point at files that are **not yet tracked**: `notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md` (55 anchor pointers + 5 homes), `notes/_lanes/305/_COMMON-BRIEF.md` (8 anchor pointers), `notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md` (W-305n6's home). Committed without them, `_governs.py --selftest` (step [13]) and `_state.check_homes` go red in CI. `_render_rulings.py` and the regen serial were NOT run (commit seat's). Build lanes that enact a `ruled` s305 entry stamp it with `_inscribe_ruling.py --set-status <id> enacted --evidence-sha <sha>` per `s295-D2`.

## Measured, and how

Counts by `json.load` over `rulings` before (638) and after (694); diff by `git --no-optional-locks diff --numstat`; anchors by `_governs.resolve_anchor` (0 ambiguous, 0 absent); commits by `git --no-optional-locks cat-file -e`; store by `_state.check()` and a load/save round-trip proven byte-identical before writing, with an mtime guard against a concurrent writer. Times in `says` are the export's saved stamps, read as BST per the common brief (13:59–14:53 BST).

## Paths written (exact)

- `knowledge/_rulings.json` (M, via `_inscribe_ruling.py --write` only)
- `knowledge/_state.json` (M, via `_state.add` + `_state.save` only)
- `notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md` (new)
- `notes/_lanes/305/A/OWNS.txt`, `notes/_lanes/305/A/CALL-MAP.json`, `notes/_lanes/305/A/build_entries.py`, `notes/_lanes/305/A/mint_threads.py`, `notes/_lanes/305/A/inscribe.log`, `notes/_lanes/305/A/sitting-page-text.txt` (new)
- `notes/_lanes/305/A/entries/s305-D1.json` … `s305-D56.json` (56 new)
- `notes/_subreports/2026-09-27-305-A-inscription.md` (this report, new)

## Follow-up (conductor's second brief, same rules)

1. **`s305-D57` — call 27, both halves as ONE ruling**, from `notes/_lanes/305/DAVE-RULINGS-2026-09-27-call-27.md` (half A "yes" 16:04 BST, half B "yes" 16:05 BST, both quoted verbatim; the sitting comment "I need to visuals for this" quoted too). **Status enacted @ `4be130e5`**: rule 3a (width named) and procedure step 1 (seed: ask the graph, the reader) were built into `apollo-spider/skills/generate-from-canon/SKILL.md` by R4a in #304 wave two (`git log -S` finds both at 4be130e5) and read the same at HEAD; the wave's [121] red was the chain step count, green at 86249459. B1's uncommitted SKILL.md line (the shell's `is-full` form) is call 11 / `s305-D12`, not this ruling. Count **694 → 695**. Dry-run then `--write`, rc 0.
2. **W-305n4 closed** through the store's own writer (`state: done` + `closed_by` receipt citing the page and his two answers; `check()` ok; mtime guard). Script `notes/_lanes/305/A/close_w305n4.py`. Its close condition (page filed under notes/, call 27 ruled from it) is met.
3. **Evidence amends, `--amend-evidence` only** (`ruled`, `says`, `governs` untouched — governs is unreachable from the sanctioned writer, so the verifier's governs corrections are carried as evidence pointers and declared as such): `s305-D13` (+4: the `.nv-count` homes Navigations, Sidebar-nav, Tab-bar, and V1), `s305-D26` (+2: `gen_kg_sources.py`, `_source_nodes.json`), `s305-D9` (+1: F2 — his yes took hug + a narrow column by rule; NO legend placement is built or decided), `s305-D25` (+1: F3 — the wording in the three metas is R4a's draft awaiting his word), `s305-D11` (+1: F1 — scoped to Common; the conductor asked B1 to keep the other three themes as they were). Every new line's path tokens exist; `_governs.py --selftest` all bites green after.
4. **CALL-MAP.json** call 27 → `s305-D57`, enacted, needs_build false.

Store after: `_rulings.json` diff vs HEAD 1,005 insertions / 0 deletions; `_state.json` 105 / 0.

Follow-up paths written: `knowledge/_rulings.json` (M), `knowledge/_state.json` (M), `notes/_lanes/305/A/CALL-MAP.json` (M), `notes/_lanes/305/A/inscribe.log` (M), `notes/_lanes/305/A/followup_call27.py` (new), `notes/_lanes/305/A/close_w305n4.py` (new), `notes/_lanes/305/A/entries/s305-D57.json` (new), `notes/_lanes/305/A/entries/amend-s305-D13.json`, `amend-s305-D26.json`, `amend-s305-D9.json`, `amend-s305-D25.json`, `amend-s305-D11.json` (new), this report (M). ⚠ Must ride the same commit: `notes/_lanes/305/DAVE-RULINGS-2026-09-27-call-27.md` (two anchors in D57) and `notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html` (evidence path, W-305n4 link), plus `notes/_subreports/2026-09-27-305-V1-verifier-wave-one.md` (evidence path in five amends).
