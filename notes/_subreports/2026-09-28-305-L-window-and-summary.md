# #305 L — the window (s305-D62), the wrap summary (s305-D63), and his boot line on W-305w

provenance: 305 · 2026-09-28 · L (Opus 5.5 sub of the #305 conductor), post-wrap, at Dave's seat through `device_bash`; no `git status` in any form, no Project memory, `_build_all.py` not run
status: observed (this copy rides the stamp commit; the push, `ls-remote` and CI read-back are added below BY ADDITION after the push, and that addendum is NOT committed — it is the next commit seat's tail, as C4's and D1's were)
CITES: `notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md` · `_HANDOFF-156-he-took-the-sitting-v1014-was-cut-and-ci-went-green.md` (cold-seat facts; OWED item 9) · `notes/_subreports/2026-09-27-305-H2-code.md` (the homes) · `notes/_subreports/2026-09-28-305-W-wrap.md` (W's tail) · `notes/_lanes/305/C4/` (the commit-seat method)
machinery: 0 instrument / 0 feature (constants, pins, fixtures and prose moved; nothing new built)

## VERDICT

DONE. Two rulings inscribed and enacted, his boot line added to the store by addition, two commits, pushed, CI read back (see the addendum). **Rulings 699 → 701.**

COUNTS: rulings 2 · constants moved 4 · pins driven 4 · files edited 8 · ruling-shaped 2 · UNPROVEN 1

## His words (Mon 2026-09-28 11:41 BST, verbatim; `notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md`)

> lt's turn the summary into shorter bullets just outlining decisions, outputs and problems, less verbose.

> Lets make the window 320 including a wrap, 320 is a bright amber and 350 as the limit.

> it doesnt seem like there is much we can do about the boot, its just tinkering around the edges

## 1 · The window — `s305-D62`, enacted at `5058d963`

Inscribed through `_inscribe_ruling.py` (dry run clean, then `--write`, reconstruction proof passed), quoting his second line verbatim in `ruled` and `says`, with the conductor's reading stated in `ruled` as the reading. It names `s305-D28` as superseded; `s305-D28` is byte-unchanged. Evidence: `chat #305 2026-09-28 (live)` and the anchor `DAVE-WORDS-2026-09-28-1141.md#The window`; the stamp added `commit 5058d963`.

**Every constant moved, old → new** (`knowledge/_gauge_tokens.py`, the one home; every consumer reads it):

| constant | old | new | what it is |
|---|---|---|---|
| `BUDGET_WORKING` | 256,000 | **320,000** | the working window, **wrap included** |
| `BUDGET_HARD` | 300,000 | **350,000** | the limit; still the only blocking tier |
| `STOP_LINE_TK` | 236,000 | **300,000** | where the wrap starts, so it lands inside 320,000 (advisory) |
| `TOLERATED_TK` | 276,000 | **320,000** | the bright-amber line (advisory) |
| `BUDGET_AMBER` | 160,000 | 160,000 | not named by his words; unmoved |
| `BOOT_CEILING_TK` | 130,000 | 130,000 | `s305-D29`; unmoved |

`band_for(320,000)` reads AMBER and RED starts strictly above it, which matches "320 is a bright amber". Each constant carries the ruling and its old value; the #301 / `s305-D28` comments beneath are kept as their record.

**The other homes, in lockstep:**
- `knowledge/_capture_gate.py`: the triple pin `(160_000, 256_000, 300_000)` → `(160_000, 320_000, 350_000)`; the stop/tolerance pin `(236_000, 276_000)` → `(300_000, 320_000)`; the 12 pre-flight fixtures priced `of 256,000` now read `of 320,000` (the gate fails any stamp not priced at the live working line), and the three over-the-line fixtures were lifted so they still test what they claim (266,897 → 336,897 twice, over working and under hard; 316,897 → 366,897, past hard); `_WALL` (the declared-breach vocabulary of the FILL-ceiling arm) learns `320,000|320000`, keeping 200,000 and 256,000; the three messages that name the line's authority now cite `s305-D62`; two header addenda.
- `knowledge/_checkin.py`: the three citation strings `s305-D28` → `s305-D62`.
- `knowledge/_seam.py`: the docstring's verdict table (300,000 / 320,000 / 350,000, and the working window including the wrap).
- `knowledge/_RUNBOOK-context-gauge.md`: the single copy of the bands (the `s305-D28` line) has its band list struck through with a pointer, and a new ⬛ `s305-D62` line under it states the bands in force; the stop-line section gets one crossing-out line under H2's.
- ⛔ **`knowledge/_standing.md:19` NOT edited.** It still reads *"180,000 FILL is the QUALITY line and stands; working 256,000 and hard 300,000 are not walls in Cowork (#284)…"*. It is Dave's ratified text (`s287-D1`) and the seam re-quotes it every run; it is his to amend. `s305-D62`'s `ruled` names it.

**Every pin driven to a named refusal once** (in-process, the constant set back to its old value, then restored; `notes/_lanes/305/L/pins-driven.log`):
- control: `selftest_preflight_tokens()` 0 failures.
- `BUDGET_WORKING` → 256,000: the triple pin fires by name (`budget = (160000, 256000, 350000), ruled (160,000 at #56 · 320,000 / 350,000 by s305-D62 …`), and seven fixtures fail with *"pre-flight prices against 320,000, but the ruled working budget is 256,000"*.
- `BUDGET_HARD` → 300,000: the triple pin fires; the marked-overrun fixture fails past the quality-max line; the #53 floor guard names the ordering (`amber 160,000 < working 320,000 < quality-max 300,000 must hold`).
- `STOP_LINE_TK` → 236,000: `stop/tolerance = (236000, 320000), ruled (300,000, 320,000) by s305-D62 …`.
- `TOLERATED_TK` → 276,000: `stop/tolerance = (300000, 276000), ruled (300,000, 320,000) by s305-D62 …`.
- restored: 0 failures.

**Selftests, all green:** `_gauge_tokens.py --selftest` OK · `_seam.py --selftest` 15 arms · `_capture_gate.py --selftest` rc 0 in 141 s, "all failure classes bite; green control passes" (`cg-selftest.log`) · `_checkin.py --selftest-compaction` 5/5, `--selftest-disk` ran · `stop_line_consistency()` 0 fails · `fill_working_ceiling_check()` 0 issues (the declared #268/#269/#282 breaches still read DECLARED against 320,000) · `_governs.py --selftest` all bites green. ⚠ `_checkin.py --selftest-block` needs a session transcript and this seat has none (the seat condition H2 named).

## 2 · The wrap summary — `s305-D63`, enacted at `5058d963`

Inscribed the same way, quoting his first line verbatim. It replaces the #250 practice (a plain-prose narrative of five to seven paragraphs after every wrap).

**Where the ritual asked for the narrative:** nowhere in the repo. `knowledge/_RUNBOOK-capture-ritual.md` never carried the #250 practice (searched for narrative, plain prose, paragraph, summary across the runbooks, `_CHAIN.md` and the #297–#305 wrap briefs; the only "narrative" is step 1b, the dossier, which is a different thing and is unchanged). It lived in Project memory (`plain-prose-wrap-summary-250.md`, not read here by the brief) and in the conductor's launch message to the wrap seat. So the change is by addition: **step 5c** after 5b, stating the new form, with the old practice written and struck through beside it and a pointer to `s305-D63`. The heading's step list is left as written. `ds-023`'s required strings are untouched (`stop_line_consistency` 0 fails).

⚠ **For the conductor:** the Project memory file `plain-prose-wrap-summary-250.md` still says to give the prose narrative; it is the conductor's to update when the note is placed. The next wrap brief should ask for `SUMMARY-BULLETS.md`, not `NARRATIVE.md`.

**#305's summary in the new form:** `notes/_lanes/305/W/SUMMARY-BULLETS.md`, 19 bullets (7 decisions · 5 outputs · 7 problems), drawn from `NARRATIVE.md` and `_HANDOFF-156`; `NARRATIVE.md` is kept.

## 3 · The boot — not a ruling

His third line states a view, not a decision, so it was not inscribed. **The row:** `W-305w` (the #305 wrap row). Its `closes_when` names *"whether --wrap is the wrap path again"*, which is OWED item 9's question (cut the boot, move the ceiling again, or keep the declared path); carry ⑮ in `_CARRIES.md` names no row. His words were added to its `body` by addition through `_state.py` (`load` → append → `check()` ok → `save`; `notes/_lanes/305/L/state_boot_line.py`): the old body is the new body's prefix; the row stays open. ⚠ **Related, not touched:** `W-305n3` (his call-29 comment, *"we need to make this more efficient somehow"*) is the boot-efficiency thread; his line reads as an answer to it too. Whether it closes or parks `W-305n3` is his.

## The commits

- **Before commit 1:** `W-305l` minted for this report (`mint_305l.py`, `check()` ok, 940 → 941); regen serial in order, all rc 0 (`step2-regen.log`); `gen_kg_titles --check` STALE → `--write` (701 rulings titled); `gen_dashboard --check` OUT OF SYNC → re-run → OK; release audit `--manifest-check` PASS (a5b00c14), package delta 0 failures, frozen `--check` PASS, `knowledge/_graph-mark-observations.jsonl` clean (`step3-checks.log`, `step4-titles-dashboard.log`). Every named path checked changed-or-untracked (`paths_l.py`, 46 of 46).
- **Commit 1 `5058d963`** — 47 files (46 named + the auto-staged `notes/_REHEARSAL-LOG.jsonl`), +16,529 / −1,183. Declared not-a-wrap; `SESSION_N=305 … --reconciled --quiet`; exit 0 in 86 s, `✓ done — locks clear`, doc rows present, one door run. The wrap gate inside it: `243 in scope · 1 fail · 325 warn`, the one fail the known boot-ceiling breach (#304 131,130 > 130,000), visible and not blocking. Transcripts `_gitcommit-L1.{log,term}`. Carries W's tail: `_gitcommit-W5b.{log,term}` final copies, `_4c-hygiene.log`, `_ci-gates-W5b.log`, `_ci-runs-eb2630bb.txt`, `_push-W5b-plain.log`, `step6-parse-5b.txt`.
- **The stamps:** `s305-D62` and `s305-D63` `ruled` → `enacted` at `5058d963` through `--set-status … --evidence-sha`, dry run first (`stamp-dry.log`, `stamp-write.log`).
- **Commit 2 (the stamp commit)** carries the two stamps, the serial re-run (all rc 0; `_RULINGS.html` moved; titles and dashboard `--check` OK — `step6-stamp-regen.log`), the KG explorer rebuilt after the stamp so it bakes D62 and D63 as enacted (`_build_kg_explorer.py`, 154 s, v1.30, 5,544 nodes / 10,667 edges, islands 2, orphans 0 — `step7-explorer.log`), this report's final copy and the lane tail. Its sha is in the addendum.

## Held (not committed), by name

`notes/_lanes/305/L/backup/` (eight pre-edit copies) · the other-seat set named in `_HANDOFF-156` (`notes/_dream/_GRADE-DECISIONS.jsonl`, `_MEMORY-GRADES.json`, `notes/_lanes/293/J7-…`, `notes/_lanes/294/WRAP-MEMORY-HOOK.md`, `notes/_lanes/304/W/_gitcommit-W5b.{log,term}`, `notes/_subreports/2026-09-22-297-A-…`, `notes/_subreports/2026-09-26-304sq-A1-animation-storyboard.md`, the other lanes' untracked scratch).

## What I did wrong, declared

- `tiktoken` was missing at the seat (4c removes `~/.local`), so the first selftest run failed on UNMEASURABLE; installed with `pip install tiktoken --break-system-packages` and re-run. No file changed between.

## RULING-SHAPED QUESTIONS

1. ⬛ **`knowledge/_standing.md:19`** still states 180,000 / 256,000 / 300,000. Amend it to the `s305-D62` lines? His text; the seam quotes it every run. (Carried on `W-305hc`.)
2. ⬛ **Does his boot line close or park `W-305n3`**, and is it his answer to OWED item 9 ("keep the declared path")? Not assumed.

### UNPROVEN

1. That the `_checkin.py` block reading uses the new lines on a live transcript — `--selftest-block` cannot run at this seat (no transcript); the constants it reads are proven by the gauge and gate selftests.

## Changed paths (exact)

Commit 1 (`5058d963`): `knowledge/_rulings.json` · `knowledge/_state.json` · `knowledge/_gauge_tokens.py` · `knowledge/_capture_gate.py` · `knowledge/_checkin.py` · `knowledge/_seam.py` · `knowledge/_RUNBOOK-context-gauge.md` · `knowledge/_RUNBOOK-capture-ritual.md` · `_CHAIN.md` · `dashboard/index.html` · `knowledge/_memento-index.json` · `knowledge/_node_titles.json` · `notes/_RULINGS.html` · `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html` · this report (interim) · `notes/_lanes/305/W/SUMMARY-BULLETS.md` · W's seven tail files · `notes/_lanes/305/L/**` (no `backup/`) · auto-staged `notes/_REHEARSAL-LOG.jsonl`.

Commit 2: `knowledge/_rulings.json` (the two stamps) · the serial outputs that moved · `notes/_KG-EXPLORER.html` · `knowledge/_node_titles.json` / `dashboard/index.html` if moved · this report · `notes/_lanes/305/L/**` tail.

## Addendum, by addition (after the push; this addendum itself is NOT committed — it is the next commit seat's tail, with `_push-L-plain.log`, `_gitcommit-L2.{log,term}`, `_msg-L2.txt.t3-rendered`, `_ci-runs-db708760.txt`, `_ci-gates-L.log`, `_ci-gates-L-summary.txt`, `step6-parse.txt`)

- **The stamp commit is `db708760e8e782ab33cdaed8018d508c1a757f63`**: 18 files (17 named + the auto-staged `notes/_REHEARSAL-LOG.jsonl`), +2,974 / −27; declared not-a-wrap, exit 0 in 81 s, `✓ done — locks clear`; the wrap gate read the same one fail (`243 in scope · 1 fail · 324 warn`, the boot ceiling). Transcripts `_gitcommit-L2.{log,term}`.
- **The push: `eb2630bb..db708760`** (both commits), plain `git push origin master`, rc 0, through the credential helper. Branch `master` checked; the live remote read `eb2630bb` by `ls-remote`, an ancestor of HEAD, so a fast-forward. **`git ls-remote origin refs/heads/master` = `db708760e8e782ab33cdaed8018d508c1a757f63` = local HEAD.** `_push-L-plain.log` (URL without credentials). No lock stranded by either commit or the push.
- **CI, read to completion, verdict taken after `render` closed:** run **`36413311980`** on `db708760` (the head; `5058d963` rode the same push and has no run of its own) — `release` ✅ 11:03:57Z · `gates` ✅ 11:12:54Z · `render` ✅ 11:17:27Z. **ALL GREEN.**
  - Step 5: `SURVEY: 69 pass · 0 FAIL · 6 COULD-NOT-ASK · 0 unaskable · 79 not asked (mutating)`.
  - Step 6: 0 gate red; advisory `[140] [141] [150]`; could-not-ask `[10] [13] [61] [68] [73] [74] [142] [147] [148] [153] [154]` — **identical by name to W's runs `36404496114` and `36406448995`.**
  - The evidence step red-and-continued at `6 lint · 0 unparsed · 4 rc/observation mismatch` (W1-5, WIRE-14, WIRE-20, WIRE-21) — identical to W's 5b run `36406448995`. ⛔ Nothing was repaired.
- **`W-305l` stays open:** its close condition is this final copy committed; this addendum is the next commit seat's tail.

---

# ROUND TWO — the boot ceiling (s305-D64) and the wrap redesign scheduled (by addition; nothing above is rewritten)

status: observed (this section rides the round-two commits; its push and CI read-back are added below it by addition after the push)

## His words (verbatim; appended by addition to `notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md` § The wrap and § Yes both)

The conductor, 12:21 BST: *"yes to both, the boot ceiling at 135,000 and the wrap redesign as #306's second job, after your 102 ticks?"* — Dave: *"yes both"*. His 11:41 line on the wrap: *"can we parallelise the wrap at all to make it quicker, don't we have a plan to make the wrap better too, we had duplicate- -writes all over the place."*

## 1 · `s305-D64` — the boot ceiling is 135,000

Inscribed through `_inscribe_ruling.py` (dry run clean, then write; 701 → 702), quoting the question and his answer verbatim. `ruled` names `s305-D29` as superseded (not edited) and gives the conductor's reason: the cloud seat boots at about 131,000, mostly tools and the system prompt, which he cannot control; his 11:41 boot line quoted; the ceiling stays a tripwire for a real jump; shrink-only resumes from 135,000.

**Constant moved:** `BOOT_CEILING_TK` **130,000 → 135,000** (`knowledge/_gauge_tokens.py`; the D29 comment above it kept). **Every home:** arm E of `_gauge_tokens.py --selftest` (the equality pin 130,000 → 135,000 and the direction check "ABOVE 135,000", both citing D64); `_capture_gate.py` reads the constant at check time, so only its boot-drift note's citation moved (`s305-D29 until the Mac seat` → `s305-D64`); a ⬛ `s305-D64` line added under the band table of `knowledge/_RUNBOOK-context-gauge.md`. No other literal 130,000 pins the ceiling (searched `knowledge/**/*.py|md|sh`).

**The pin driven to a named refusal** (a copy of the module in `/dev/shm`, the constant sed-edited, run with `PYTHONPATH=knowledge`; `pin-d64-driven.log`): at 130,000 → `[E s294-D7/s305-D64] BOOT_CEILING_TK = 130,000, not 135,000 …`, 1 named failure; at 140,000 → the same plus `[E s305-D64] BOOT_CEILING_TK = 140,000 is ABOVE the 135,000 s305-D64 set …`, 2 named failures; the live file green.

**The wrap gate's boot-ceiling arm** (`boot_constant_drift_check`, in-process against the live `notes/_GAUGE-LOG.md`; `boot-arm-D64.log`): **0 fails** at 135,000 — derived band 127,826 ±1,742 over #298–#304, newest #304 **131,130**, under the ceiling. Control at 130,000: 1 fail, `CEILING BREACH … #304 131,130`. #305's **131,040** is not in the gauge log yet (it joins at the next 2f roll); it is 3,960 under 135,000. The gate's reading inside the committer is in the commit section below.

**Selftests:** `_gauge_tokens.py --selftest` OK · `_seam.py --selftest` 15 arms · `_governs.py --selftest` green · `_capture_gate.py --selftest` rc 0 (130 s). ⚠ **Declared:** the first capture-gate selftest run FAILED on my own evidence anchor — `DAVE-WORDS…#The boot` matched two lines once I had appended "The boot-ceiling half…" to the file. I reworded my own uncommitted line ("Its first half, the ceiling at 135,000, …"); the anchor is unique again and every selftest is green. Nothing inscribed was amended.

## 2 · The wrap redesign — #306's second job (scheduling, not a ruling)

- **`_HANDOFF-156` OWED item 2, inserted by addition** after the 102 (the items below keep their written numbers; the new item says to read them as 3–11). It quotes the question, "yes both" and his 11:41 wrap line, and sets out the plan from `notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md`: lever 1 one story written once as the handoff with the banner, delta, dossier, wrap report and memory hook generated from it (the duplicate writes he named); lever 5 three seats in parallel (story / mechanics / commit-push-CI); lever 3 mostly done (the boot-ceiling fail ended with D64). A post-wrap addendum at the handoff's foot records D62–D64, marks the cold-seat window bullet stale, and strikes OWED item 9 by his words.
- **Store row `W-305wr` minted** through `_state.py` (`add` + `check()` ok, 941 → 942): home the five-levers file, owner claude, closes when a wrap has run on the redesign (handoff written once, the other views generated, the three seats in parallel) with its receipt filed, or Dave re-schedules or parks it with a tripwire.

## 3 · `W-305w` — NOT closed, and why

Its `closes_when` asks for FIVE things: the 102, `s212-D1`/`s256-D1`, the ring and the threads, the `s279-D1`/`W-305n6` collision, and whether `--wrap` is the wrap path again. `s305-D64` answers only the fifth. The other four are still his, so closing it would strike four open questions without a receipt. Recorded instead, by addition in its body: the fifth is answered by `s305-D64`, with the gate reading. (`W-305n3`, his boot-efficiency and wrap thread, is still not touched; `W-305wr` links it.)
