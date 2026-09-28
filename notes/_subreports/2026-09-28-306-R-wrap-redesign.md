# #306-R — the wrap redesign: measured, designed, put to Dave on one page

session: `#306` · 2026-09-28
window: lane R (design lane, Opus 5.5, at Dave's seat through device bash, read-only except the files named below)
sub index: `R`
brief: the conductor's launch message (verbatim in the conductor's transcript); the plan it builds on is `notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md`
provenance: 306 · 2026-09-28
status: observed
tokens: UNMEASURED — this seat cannot read its own transcript while it is still growing

## VERDICT

DONE. The last three wraps (#303, #304, #305) are measured from their own logs and git, the duplicate writes of the #305 wrap are mapped by grep over what it actually wrote, and the redesign is on a decision page for Dave: `notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html`. Six calls are put, each with a recommendation. The page was render-checked at 1440 and 390, in light and dark: 0 page errors, 0 horizontal overflow, and the chips and Copy as text both work. The headline is that half of every wrap is waiting on CI twice, and each key fact is hand-written in about seven places. Nothing was built, ruled, committed or pushed.

COUNTS: findings `7` · ruling-shaped `6` · UNPROVEN `3`

## What was done

1. **Measured** (`notes/_lanes/306/R/wraptimes.py`, `prose_size.py`). Launch times are the conductor-transcript times each W report quotes. Every other time is a file mtime at the seat, in UTC, or a git commit time.

| minutes | #303 | #304 | #305 |
|---|---|---|---|
| launch → first gate written | 4.2 | 6.5 | 5.0 |
| first gate → first push | 14.2 | 18.1 | 20.9 |
| CI wait on the wrap commit | 14.6 | 16.5 | 15.2 |
| 5b follow-up (write + commit + push) | 3.4 | 3.8 | 3.7 |
| CI wait on the 5b commit | 9.4 | 14.9 | 14.0 |
| **total, launch → last CI read** | **45.8** | **59.8** | **58.8** (+1.7 to 4c) |
| of which CI waits | 24.0 | 31.4 | 29.2 |

Launches: #303 12:47:24Z (W report line 27) · #304 11:16:59Z (line 28) · #305 09:09:46Z (line 24). Commits: 2 each (#303 also had one refused run at the mention-map gate). Gate runs at the seat: 4 each (open, pre-wrap, inside each commit). Regen logs: not logged, 3, 5. `_gm_move` ops files: 6, 6, 9 (#305's extra three were re-work after the pre-commit gate: fix-ceiling, fix-banner, s214b). One-off `_work` scripts written: 8 (280 lines), 9 (319), 11 (394), and 4 to 5 of them say "Modelled on" the last wrap's. Hand-written prose added: 92,289 · 93,520 · 107,459 chars (≈26K · 26K · 30K tokens at 3.53 chars/token). Carried-items copy-forward: 794,487 · 803,996 · 368,624 chars. Record files in the wrap commits, with other lanes' tails left out: 16 · 17 · 18.

2. **Mapped the duplicate writes** (`dupmap.py` → `dupmap.json`, `dupgroup.py` → `dupgroup.json`). This counts the ADDED lines of `81bce363` + `eb2630bb` per file, plus `SUMMARY-BULLETS.md` and the two commit messages. Staging vehicles (`_ops-*.json`, `delta_305.txt`, `stratum_305.txt`, `signoff_row.txt`) are dropped because they are copied into GM, LS and the sign-off list. `WRAP-BRIEF.md` is the conductor's input. GM archive, LS archive and the gauge log are moves of earlier sessions' text. 27 facts were tested: the mean is **7.1 hand-written homes per fact**, and 24 of 27 are in 5 or more. Top: v1.0.14 in 12; rulings total 699, the newest ruling id and the headline in 10; the boot-ceiling breach, the next beat, the fill at the wrap, "set in ink" and Launchpad in 9. `_CHAIN.md` and the titles receipt are the only generated homes.

3. **Mapped the steps.** Judgment (needs prose): 1 (delta prose), 1b (dossier), 2 (banner), the handoff, the W report, the carries' new items and strikes' receipts, 3 (memory note), 5c (summary). Mechanics (already scripted or scriptable): 2c, 2d, 2e, 2f (`_gm_move.py` + `_roll_state.py`), carries aging, state rows (`_state.py`), 2g index, 4b titles, 4d rulings page, the size stamp, the gate, 5 commit and push, the CI read-back, 5b, 4c. Must serialise: views after both sources exist; 2g after every GM/LS edit; the gate before the commit; 5b after CI; 4c last. Everything else can run beside the prose.

4. **Designed** (on the page, section "The design"): two source files, each with one writer. `notes/_lanes/<n>/W/STORY.md` is markdown with tagged sections, written by the story seat. `FACTS.json` holds measured figures and is written by the mechanics seat. A new `_wrap_views.py` generates the handoff, dossier, W report, banner, delta, summary, memory note, commit message and state-row titles. The per-wrap scripts become permanent tools: `_wrap_facts.py`, `_wrap_ops.py`, `_wrap_carries.py`, `_wrap_rows.py`, `_ci_readback.py`. There are three seats (story, mechanics, commit) that join only at the commit. The gate gets a blocking "views are fresh" arm, the same class as `index_freshness_check` and `rulings_page_freshness_check`. The generated W report still carries the `s218-D7` lines, a state row and a path citation. The design has six phases, each proven on one real wrap with before-and-after measurements.

5. **Wrote the page** at `notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html`, built by `notes/_lanes/306/R/build_page.py` from `page_body.html`, `page_script.js` and `_chrome.css`. The chrome is copied from `notes/_CHECK-306-parked-superseded-2026-09-28-v1.html`. It has one inline SVG, no images, no external links and no `target=_blank`.

6. **Render-checked** with `notes/_lanes/306/R/render.py`, using `file://` goto and `$RENDER_SHELL`. Results are in `renders/render-check.json`, with screenshots `page-{1440,390}-{light,dark}.png` and `svg-*.png`, and an export sample in `export-sample.md`. All four renders: errors 0, scrollWidth = clientWidth, 0 off-edge boxes. At 390: 3 chips clicked → 3 on, "3 of 6 calls", the export carries the question text verbatim with the answer's chip text and the recommendation, the words box exports, Copy shows "Copied", and the state persists across reload.

## Findings

1. **Half of every wrap is waiting on CI twice**: 24.0 of 45.8, 31.4 of 59.8, and 29.2 of 58.8 minutes. The second wait (9 to 15 minutes) checks the 5b commit, which only records the first commit's result. Probe: `wraptimes.py`.
2. **Dave's summary comes after the whole run.** The summary is written after 5b and 4c. At #305, `SUMMARY-BULLETS.md` has mtime 10:51Z, against a launch at 09:09Z.
3. **Each key fact is hand-written in about seven places** (mean 7.1 over 27 facts). Probe: `dupgroup.py`.
4. **The three long narrations share no sentence.** The handoff, the W report and the dossier have 0 shared sentences over 60 characters in any pair. They are re-told, not copied, which is where drift comes from. Probe: an inline difflib check over the three #305 files.
5. **The memory body is written three times verbatim**: `memory_body_305.md` appears 100% inside `memory_file_305.md` and 100% inside `WRAP-MEMORY-HOOK.md`. That is ≈20K chars per wrap.
6. **`_CARRIES.md` is 37,018,756 bytes with 82 sections.** Each wrap appends a full copy of the previous section with ages +1: residual → #306 is 369,557 chars, and → #304 was 794,484.
7. **The wrap seat re-authors 8 to 11 scripts every wrap**, "modelled on" the last wrap's (`build_ops`, `carries`, `mint`, `names`, `ci`, `cilog`, `step6parse`, the commit shells). After renumbering, 54 of 56 lines of `build_ops` differ between #304 and #305, because the prose is embedded in the script.

## RULING-SHAPED QUESTIONS

Put to Dave on the page, each with the recommendation first. None is answered here.

1. Write the session's story once, and generate every other view from it, the handoff included? (a, recommended: story plus measured figures, all views generated · b: the handoff stays hand-written and is the story · c: no)
2. May a generated wrap report count as the filed report every seat owes? (yes, recommended; `s218-D7`, the plan's question 2)
3. Run the wrap as three seats at once, for story, mechanics and commit, joined only at the commit? (yes, recommended)
4. Give you the summary as soon as the wrap is pushed, and stop waiting on CI for the small follow-up commit? (a, recommended: the next opener reads the follow-up's CI · b: summary at push, still wait · c: as today)
5. Stop copying the whole carried-items list forward every wrap: write only what changed, and generate the full list when it's read? (yes, recommended · not now)
6. May the seam check add your words and the running tally to the story draft during the session? (yes, in a later phase, recommended; the plan's question 3)

### UNPROVEN, named rather than implied

1. **The wrap seat's own token cost for #303, #304 and #305.** None recorded it. The last reading is #292: 115,674 tokens, plus 85,536 for a second commit seat (HANDOFF-143, via the #293 plan). Price: phase 1 writes it into `FACTS.json` from the seat's transcript after the hand-back.
2. **Every "after" figure on the page is an estimate**: launch to push ≈13 to 15 minutes, to the summary ≈15, to done ≈30 to 32, prose ≈35K chars. They are derived from the measured split, not from a run. Price: one real wrap per phase.
3. **The time before launch** (the conductor writing the brief) **and after** (memory placement, the summary in chat) is not measured. #305's brief mtime is 09:09:21Z against Dave's message at about 09:08Z.

REPLAY-THESE: `python3 notes/_lanes/306/R/wraptimes.py` · `python3 notes/_lanes/306/R/dupmap.py && python3 notes/_lanes/306/R/dupgroup.py` · `python3 notes/_lanes/306/R/prose_size.py` · `python3 notes/_lanes/306/R/build_page.py` · render: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/306/R/render.py`
