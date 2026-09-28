# #306 lane T — his check-page answers enacted: 24 closed as answered, 78 reopened, three rulings

provenance: 306 · 2026-09-28 · lane T (Opus 5.5, on the mount via device_bash)
status: observed

Scope: Dave's answers on the check page `notes/_CHECK-306-parked-superseded-2026-09-28-v1.html`, export `notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md` (15:20 BST), applied through the sanctioned writers the way #305 lane H1 parked them (`notes/_lanes/305/H1/store_batch.py`): `_state.load → mutate → _state.check → _state.save`, every change by addition, dry run first. No `git status`, no Project memory, no `_build_all.py`. machinery: 0 instrument / 0 feature (three one-shot lane scripts under `notes/_lanes/306/T/`).

His two calls, verbatim from the export: "Close the 24 already-answered questions?" → "yes" · "Does the call-33 yes settle the two old release rows (W-222, W-272)?" → "yes". And "Keep open" ticked on 78 rows, 14:26 to 15:20 BST. The check answered his 12:59 BST question, verbatim: "can you check these I think some of them have been superseded".

## Counts, before → after (measured, `_state.counts()`)

| measure | before | after |
|---|---|---|
| store items | 942 | 944 (+2 born-closed document rows) |
| live (open) | 490 | 566 |
| Dave's live / mine live | 273 / 217 | 322 / 244 |
| done / dropped / parked | 302 / 1 / 149 | 330 / 1 / 47 |
| rulings | 702 (newest s305-D64) | 705 (newest s306-D3) |
| pinned 75 still live (`s305-D40` arming) | 57 | 61 |

Checks after: `python3 knowledge/_state.py` rc 0, 0 fails (home pointers 0 unresolvable); `_state.py --selftest` 84 bites all green. 107 store ids changed or added, exactly the 102 + W-305hr + W-305n5 + W-305b4 + W-306s + W-306t (diffed against the backup by id, `notes/_lanes/306/T/store_diff.txt`); for every changed row the old body is a prefix of the new one and no field other than `state`, `body` and a new `closed_by` moved.

## What was written

1. The 24 lane S read as SUPERSEDED: parked → done under `s306-D1`. Each body gains a dated paragraph with the answering ruling ids, the record's words as lane S quoted them (`notes/_lanes/306/S/parked-102-check.json`) and lane S's reading; `closed_by` names the ruling. W-222 and W-272 also cite `s306-D2`. The 24: W-99x, W-99y, W-135, W-222, W-247, W-272, W-332, W-349, W-350, W-351, W-352, W-358, W-359, W-368, W-376, W-431, W-434, W-435, W-446, W-452, W-465, W-466, W-467, W-265c.
2. W-305hr: a dated paragraph by addition, saying he has now said which way W-222 and W-272 go (`s306-D2`). Its `closes_when` also needs the 28 kind-6 rulings re-sorted or left; he has not answered that, so it stays open.
3. The 78 ticked "Keep open": parked → open under `s306-D3`, each with a dated paragraph (his tick time, lane S's verdict and, where S found one, what is still open). The #305 park paragraph and tripwire above it stay as history. Five of them (W-510, W-63, W-71, W-72, W-73) were also parked under `s305-D37`; the paragraph says his tick is the later word, and `s305-D37` is not edited.
4. `knowledge/_parked.json` is unchanged. H1 never wrote the 102 into that register: their tripwires live in the row bodies only, and the register holds P-ids alone (34, none for these rows). So there were no entries to remove.
5. W-305n5 closed. Its close, limb by limb: the scan page (`notes/_SCAN-305-parked-questions-2026-09-27-v1.html`, B4, 27efb7b6) and then the #306 check page over the same 102 were put to him; he named 78 by tick and all 78 are reopened.
6. W-305b4 closed. Both B4 pages are committed (27efb7b6, f6aeb264); `_HANDOFF-156` WHAT LANDED records the artifact "Apollo 304 review" at version 7 with the 102 scan added; his export answers all 102. ⚠ Declared: he answered on the #306 check page, not by ticks on B4's scan page itself.
7. Two document rows, born closed under `s305-D40` (`DOC_BIRTH_FROM_SESSION = 306`): W-306s (home `notes/_subreports/2026-09-28-306-S-parked-check.md`) and W-306t (this report). The check page gets no row of its own: #305's precedent is that pages ride in their report row's links (W-305b4 links the two B4 pages; no store row has a page as its home). W-306s links it.
8. Rulings `s306-D1`, `s306-D2`, `s306-D3` inscribed through `knowledge/_inscribe_ruling.py`, dry run then write, reconstruction proof passed each time (`notes/_lanes/306/T/inscribe.log`). Built by `notes/_lanes/306/T/build_entries.py`, which reads his words from the export and never retypes them. ⚠ Shape: the entries carry the eight keys the writer requires (id, ruled, date, by, says, governs, evidence, status). The writer refuses a `watch` key (R1 schema), so none was added. Inscribed as `ruled`; `enacted` is stamped after the commit with `--set-status … --evidence-sha`, as #305 lane L did (`s295-D2`: the sha is the proof).
9. `_CARRIES.md` § residual → #306, item ①: struck in the `s183-D1` form (`~~` round the title, a ⛔ STRUCK note with receipts), the original item following unedited; reconstruction proven (`notes/_lanes/306/T/carry_strike.py`). No " · " in the note, so no new carry item.

## Things to know

- The pinned 75 moved the wrong way on purpose: W-413, W-416, W-417 and W-418 are in the pinned set and he ticked all four "Keep open", so reopening them took the live count from 57 to 61. The regrowth arm is further from arming, not closer; it did not arm.
- Minting the first #306 rows moved the store's "latest session" to 306, so the advisory REGROWTH note now names 65 rows (was 61): rows whose close names a #305 opener or wrap event now count as past. Advisory, not a fail.
- `s305-D32` (the park) and `s305-D33` (the release rows) still read `ruled` in the store. Stamping them is not this lane's brief and was not done.
- Backups: `notes/_lanes/306/T/backup/` (`_state.json.pre-T`, `_rulings.json.pre-T`, `_parked.json.pre-T`, and the § residual → #306 section of `_CARRIES.md` as it stood, `residual-306-pre-T.txt`; `_CARRIES.md` is 37 MB, so only that section was kept).
