---
session: 309
headline: metric was built, and the checks run before the push
one_sentence: THE CARDS AND TILES AND METRIC WERE BUILT, THE ARROW TOOK THE RAG INK, AND A LANE NOW SEES CI'S WHOLE VERDICT BEFORE THE PUSH
opened_word: Good Morning!
wrap_word: i think we need to wrap
wrap_word_context: just after *"how hot are you"*
conductor: Opus 5.5, a CLOUD session linked to Dave's computer
wrap_seat: delegated, Opus 5.5
lanes: Opus 5.5 lanes B, C, E, D, F, G
first_beat: READ THE `CI owed:` LINE AT THE FOOT, THEN PUT THE ARROW TO HIM
next_title: Apollo - #310: the arrow, the dark ground and the loose ends
words_files: notes/_lanes/309/DAVE-WORDS-2026-09-29-2137.md · notes/_lanes/309/DAVE-WORDS-2026-09-30-0707.md · notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md
lane_reports: notes/_subreports/2026-09-29-309-{B,C}-*.md · notes/_subreports/2026-09-30-309-{D,E,F,G}-*.md
prior_handoff_struck: 1
---

## @words
- Tue 20:47 — Good Morning!
- Tue 20:50 — go *(build the cards and tiles)*
- Tue 21:37 — 1. good / 2. go *(tabs, accordion and popover are blocks; Metric rebuilt properly)*
- Wed 07:07 — 1. Moving to metric is probably a good idea but the arrow must be the the right RAG ink / 2. We'll recut towards the end of the week / 3. I'm worried that the checks weren't made can we investigate, im sure we can find a work-around / 4. Please delete
- Wed 10:24 — Can I have a review doc rather than pngs. there are a few comments I want to make
- Wed 11:04 — export `notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md`: 3. *"1. the filters are stacking vertically here 2. theres no tile colour in dark mode, if there is I cant see it, the background should be the darkest grey and the tiles black. Anyway this is something we need to decide separatly."* · 5. *"the sparkline has become an area chart, but weird, and I though we had a rule for the minimum items in a stat bar. where has tall that blank space come from on the after"* · 6a *"Let a metric say up is bad (not the recommendation)"* · 6b *"Full ink, as ruled (the recommendation)"* · 6c *"Yes (the recommendation)"* · 2 *"not answered"*
- Wed 13:08 — how hot are you
- Wed 13:08 — i think we need to wrap

## @rulings
- `s309-D1` — *"1. good"* (21:37) — tabs, accordion and popover are blocks, not housings; the accepts check reads 110 of 110 — ENACTED
- `s309-D2` — *"2. go"* (21:37) — Metric rebuilt properly as one block, the KPI tile its reference, the stat card and the KPI tile its alias seats — ENACTED
- `s309-D3` — *"Moving to metric is probably a good idea but the arrow must be the the right RAG ink"* (07:07) — the stat card pages move to Metric with the arrow on the ink seat, in the right RAG ink — ENACTED
- `s309-D4` — *"We'll recut towards the end of the week"* (07:07) — the designer pack is re-cut towards the end of the week — RULED
- `s309-D5` — his 11:04 export, call 6a *"Let a metric say up is bad (not the recommendation)"* — a metric may say "up is bad", NOT the recommendation — ENACTED
- `s309-D6` — his 11:04 export, call 6b *"Full ink, as ruled (the recommendation)"* — Metric's no-change mark at full ink — ENACTED
- `s309-D7` — his 11:04 export, call 6c *"Yes (the recommendation)"* — every lane runs the pre-push check, Worker checklist step 5 — ENACTED

## @summary
### decisions
- {d.rulings_summary}: tabs, accordion and popover are blocks; Metric rebuilt properly; the stat card pages move to Metric with the arrow in the right RAG ink; the pack is re-cut towards the end of the week; a metric may say "up is bad"; the no-change mark at full ink; every lane runs the pre-push check.
### outputs
- Built: the cards-and-tiles model (the accepts check at 110 of 110), Metric as one block (stat card and KPI tile kept as its other names), four pages moved onto it in the ruled ink, and a check a lane can run to see CI's whole verdict before a push (Worker checklist step 5).
### problems
- Two CI reds in the session, each from a lane skipping a mechanical step. Both were fixed the same day.
- Your review page couldn't be published into the shared review artifact (a permission check refused it). How review pages reach you now is still open.
- Still yours: the arrow's shape, which metrics are "up is bad", the dark-mode ground and tiles, and the container types.
- The session ran to {facts.fill.now:,}, past the stop and limit lines but under the hard line.

## @did
### THE CARDS AND TILES, BUILT
20:50 BST, *"go"*: lane B built the five kinds (layout, housing, record, block, part), the advisory accepts check inside `_validate_edges.py --check`, container, surface and panel with chart-panel renamed chart, and the four limits; the carousel ruling is now derived (`94ba3c73`..`bba80abd`). It stopped Metric on scale (canon.css 193 mentions, pinned by the 27 chart receipts). 21:37, *"1. good"* / *"2. go"*: tabs, accordion and popover are blocks (`s309-D1`, 110 of 110 accepted) and Metric rebuilt properly (`s309-D2`); lane C built it, one block with the trend an optional slot and stat-card and kpi-tile as aliases, the 27 receipts re-driven green, the explorer v1.35 (`4b64f0e8`..`f197743e`).

The opener read #308's owed CI on `{facts.ci.owed.sha8}`: {facts.ci.owed.verdict}. Lane B's five kinds went onto every meta; W-308ir, W-308is, W-308it, W-308iv closed; its 5 refusals all came from classing tabs, accordion and popover as housings. Lane C renamed the KPI tile's vocabulary, generated `.cn-kpi-tile` as an alias, moved no measurement, and closed W-308iu.
### THE ARROW AND THE CHECKS
07:07, *"1. Moving to metric is probably a good idea but the arrow must be the the right RAG ink"* and *"2. We'll recut towards the end of the week"*: `s309-D3`, `s309-D4`; lane D moved the banking demo, progress dashboard, receipt test and FAB overlay onto Metric, the arrow on the ink seat in all four themes (`06062e9f`..`893028e1`). *"3. I'm worried that the checks weren't made can we investigate, im sure we can find a work-around"*: lane E sliced state-contrast at the seat (8 slices, byte-identical to CI's audit), gave hit-area `$RENDER_SHELL`, and a `/tmp`-clone survey that asks all 167 steps and caught lane C's red on `528e8318` (`b690a19b`). *"4. Please delete"*: the leftovers `outputs/309/{B,C}` went.

The ink: rise #137F3C light / #66CC8D dark, fall #DA1A00 / #F6604C (lane D's drawing at `d6d570bf`); the full state-contrast audit regenerated (it had covered only 3 snippets since lane C). The survey counts any step that is not `--check`/`--selftest` as mutating and never asks it, so [10] was asked only by CI after the push; the slices take about 4.3 min; the clone survey with `--include-mutating` in four chunks gives CI's whole blocking verdict (about 7 min, 12 with the sweep). The deleted leftovers were 141 MB, on the delete permission he granted at the prompt.
### HIS REVIEW PAGE, AND THE TWO REDS
10:24, *"Can I have a review doc rather than pngs. there are a few comments I want to make"*: lane F built `notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html` (`6e7af8c5`); the artifact publish was refused, he opened it from Finder. 11:04 export: 6a *"Let a metric say up is bad (not the recommendation)"* (`s309-D5`), 6b full ink (`s309-D6`), 6c yes (`s309-D7`); the arrow's shape not answered. Lane G built `upIsBad` and the full-ink mark, fixed the receipt sparkline the move had stretched (`e649da06`), and wrote the pre-push routine into the Worker checklist; three looks pre-date the move (W-309g3, W-309g4) and the dark ground is his (W-309g2).

Publishing into the artifact "Apollo 304 review" was refused by a permission check (rebuilding the artifact's index from a read of it); the page lives in the repo only. The `upIsBad` setting (class `up-is-bad`, `7e58f84a`) is on no live page; the routine is step 5 of the Worker checklist in `knowledge/_RUNBOOK-parallel-conductor.md`; the sparkline had been stretched across 1,360 px; lane G's range is `d1c0f8b7`..`99ba4a6e`. The looks: the filters (W-309g3), the receipt page's chart script and splice (W-309g4), the one-tile group (W-309g4). The reds: `528e8318` ([10], ASSERT-009 138 → 139 for `metric.meta.json`, lane C's skipped re-base; the conductor re-based it, `054aee4b`) and `99ba4a6e` ([131], lane G's regen left `knowledge/_graph-mark-observations.jsonl` uncommitted; the conductor committed it, `fc203264`, read by this seat).

## @problems
- ⚠ Red on `528e8318` ([10], ASSERT-009 138 → 139 for metric.meta.json; re-based `054aee4b`, green) and on `99ba4a6e` ([131], lane G's regen left `knowledge/_graph-mark-observations.jsonl` uncommitted; `fc203264`).
- ⚠ His review page could not be published into the artifact "Apollo 304 review"; he opened it from Finder.

## @owed
- ★★★ dave: **the arrow: keep Metric's thin line arrow, or bring the filled triangle back, in the RAG ink?** — His review page item 2, unanswered. The ink is `s309-D3`'s; only the shape is open. The thin arrow stands meanwhile.
- ★★ dave: **which live metrics are "up is bad"?** — The option exists (`s309-D5`, `upIsBad`); no page uses it. The banking demo's "Net FX exposure" is the live example lane D named.
- ★★ dave: **dark mode: the ground the darkest grey and the tiles black? (W-309g2)** — His words: *"the background should be the darkest grey and the tiles black. Anyway this is something we need to decide separatly."*
- ⬛ mine: **mine, small: can the three older looks be fixed?** — The banking demo's filters onto one row (`.ftb-row` → `.ftb-primary`, W-309g3). The receipt page: load the chart script and fix the splice markers that drop a rule each (W-309g4). The one-tile stat group against the minimum of two is his call (W-309g4).
- ⬛ dave: **the designer pack re-cut towards the end of the week (`s309-D4`), and the container types (W-308iw)?** — Metric, the kinds and the logos fix (W-305v2) ride the re-cut. Container types: section, division, sector, panel. Then everything still standing on `_HANDOFF-159` OWED items 3 to 6 (the edge register items 5 to 9 and W-308ie; the bento-matrix selftest's two reds; the picture-page rows; the older carries).
- ⬛ standing: **everything still standing on `_HANDOFF-159` OWED items 3 to 6** (carried)
- ⬛ mine: **the review surface: how should review pages reach him now the publish step is refused?** — The #309 page is not in the artifact.
- ⬛ found: **found and not acted on** — hit-area has never run in CI (its words say the render job runs it; `gates.yml` does not); `knowledge/_HIT-AREA-ADVISORY.md` dates from 2026-08-19 (77 snippets against today's 137); the stat card's own drawing still exists (showroom, gallery, the frozen #227 retrieval pair).

## @new
- ⬛ **THE ARROW — KEEP METRIC'S THIN LINE ARROW, OR BRING THE FILLED TRIANGLE BACK, IN THE RAG INK?** [DAVE'S] — item 2 of his review page (`notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html`) came back "Chose: not answered" in his 11:04 export (`notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md`). The ink is settled (`s309-D3`: rise #137F3C light and #66CC8D dark, fall #DA1A00 light and #F6604C dark, all four themes); the shape is not. The thin arrow stands meanwhile.
- ⬛ **WHICH LIVE METRICS ARE "UP IS BAD"?** [DAVE'S] — his 11:04 click on call 6a, "Let a metric say up is bad (not the recommendation)", is `s309-D5`. Lane G built the one optional setting (`upIsBad` in the meta, class `up-is-bad` on the tile, `7e58f84a`); no live page sets it. The banking demo's "Net FX exposure" falling and shown red is the live example lane D named.
- ⬛ **DARK MODE — THE GROUND AND THE TILE COLOUR** [DAVE'S] — his 11:04 note on the banking demo, verbatim: *"theres no tile colour in dark mode, if there is I cant see it, the background should be the darkest grey and the tiles black. Anyway this is something we need to decide separatly."* Row W-309g2. Nothing built.
- ⬛ **THE THREE LOOKS THAT PRE-DATE THE MOVE — THE FILTERS, THE RECEIPT PAGE'S CHART AND SPLICE, THE ONE-TILE GROUP** — lane G (`notes/_subreports/2026-09-30-309-G-review-answers.md`): the banking demo's filter row still wears `.ftb-row`, which canon no longer styles, so the four filters stack (W-309g3; renaming it `.ftb-primary` alone puts them on one line). The receipt page does not load the chart script and its splice markers are HTML comments inside `<style>`, so each drops the rule after it (W-309g4). The one-tile stat group against the meta's minimum of two per group is his call (W-309g4).
- ⬛ **THE DESIGNER PACK RE-CUT, TOWARDS THE END OF THE WEEK** [DAVE'S] — his 07:07 words, *"We'll recut towards the end of the week"*, are `s309-D4`. The frozen pack still names Kpi-tile and carries no kinds; the logos fix (W-305v2) also rides the next cut. No row was minted for the re-cut.
- ⬛ **THE REVIEW SURFACE — HOW DO REVIEW PAGES REACH HIM NOW?** — lane F's page was built in the repo, but publishing it into the artifact "Apollo 304 review" was refused by a permission check (rebuilding the artifact's index from a read of it). He opened it from Finder and answered it. The next review page needs a route that is not refused.
- ⬛ **FOUND AND NOT ACTED ON — HIT-AREA HAS NEVER RUN IN CI, ITS ADVISORY IS FROM AUGUST, THE STAT CARD'S DRAWING STILL EXISTS** — lane E: `_validate_hit_area.py` says CI's render job runs it blocking, but `gates.yml` never names it; its only CI run is `_build_all.py` step 68 in the gates job, which has no browser, so it has refused 77 on every run. `knowledge/_HIT-AREA-ADVISORY.md` dates from 2026-08-19 (77 snippets; today's sweep 137). Lane D kept `Stat-card.reference.html` and `.cn-stat-card` for its showroom page, gallery section and the frozen #227 retrieval pair.

## @struck
- **① BUILD THE CARDS AND TILES — THE DEFINITIONS AND THE FIVE KINDS, "ACCEPTS", METRIC, THE FOUR NESTING LIMITS** — BUILT — Lane B built the definitions and the five kinds, the advisory "accepts" check in `_validate_edges.py --check`, container, surface and panel with chart-panel renamed chart, the four limits, and the carousel ruling re-expressed as accepts rules (`94ba3c73`..`bba80abd`; rows W-308ir, W-308is, W-308it, W-308iv closed). His 21:37 "1. good" / "2. go" made tabs, accordion and popover blocks (`s309-D1`, `daf855ac`, 110 of 110 lines accepted) and Metric a proper rebuild (`s309-D2`): lane C built it, one block with the trend an optional slot and stat-card and kpi-tile as aliases, the 27 chart receipts re-driven (`879f9aae`, `ccb917c4`, `f197743e`; W-308iu closed). Container types stay his, carried as their own item.

## @rows
- note W-305wr — the fourth wrap on the phase-1 tools, and the first DATE SPLIT on them (--date 2026-09-30 --session-date 2026-09-29 --date-split). Counts in notes/_subreports/2026-09-30-309-W-wrap.md. Phases 3 to 6 remain. The row stays open.
- note W-305v2 — his 07:07 words 'We'll recut towards the end of the week' are s309-D4; the logos fix and Metric ride that cut. The row stays open for the zip.

## @cold
- ⛔★★ **THE PRE-PUSH ROUTINE IS NOW WORKER CHECKLIST STEP 5 (`s309-D7`):** a `/tmp` clone, the chunked survey 1:12, 13:55, 56:140, 141:167 with `--include-mutating`, `test_gates`, `_validate_evidence`, and the sliced state-contrast sweep when snippets or canon change. Do not survey on the mount for this: it never asks the writer gates.
- ⛔★ **ADDING OR REMOVING A COMPONENT META ⇒ RE-BASE ASSERT-009 IN THE SAME CHANGE** (`notes/_lanes/309/cond/assert009_rebase.py`). Red on `528e8318`.
- ⛔★ **A REGEN THAT APPENDS TO `knowledge/_graph-mark-observations.jsonl` MUST COMMIT IT WITH THE SCHEMATIC**, or CI's [131] reads stale. Red twice now (#308 lane I's rule, #309 `99ba4a6e`).
- ⛔★★ **NEVER RUN `git status`.** After every gate run, `python3 knowledge/_wrap_commit.py unlock --tag <n>-<seat>`. A no-op `git add` strands `.git/index.lock` on this mount.
- ⚠ **THE COMMIT GATE REFUSES A REPORT WITH NO STORE ROW.** Lane F's passed on `DOC_ROW_ACK`; W-309f1 was added after.
- ⚠ **THE ARTIFACT PUBLISH OF THE REVIEW INDEX WAS REFUSED BY A PERMISSION CHECK THIS SESSION.** Owed item 7.
- ⚠ **A carry item must not hold a bracketed number like `[68]`:** `_carry_items` reads it as the item's age and counts a `[NEW — 0]` item early. This wrap wrote one, caught it, and reworded it (429, not 430).
- ⛔ **Window lines (`s305-D62`, `s305-D64`):** stop {d.stop_line:,} · limit {d.limit_line:,} · hard {d.hard_line:,} · `BOOT_CEILING_TK` {d.boot_ceiling:,}. This session crossed the stop at {d.stop_crossed_local} Wed and the limit at {d.limit_crossed_local}.

## @why
### 1. The build, and where it stopped honestly
`_HANDOFF-159` put the cards and tiles first, and his "go" at 20:50 sent lane B to build all six of #308's calls in one pass. Five landed as data and a check: every meta now names its kind, and the accepts check derives "a carousel holds cards" rather than storing it. Two things were left for him rather than forced. First, the accepts check refused five lines on the real tree, all because lane B had classed tabs, accordion and popover as housings. It did not bend the kinds to make the tree pass; it put the call to him. Second, Metric (merging the stat card and the KPI tile) turned out not to be a metas-only change: 193 mentions in canon.css, which the 27 chart receipts pin. Lane B stopped on the probe, as its brief told it to, and put the scale to him. At 21:37 he answered both in two words each: *"1. good"* / *"2. go"*.
### 2. Why Metric was rebuilt, not aliased
The cheaper path was two names for one block. The conductor's call, which he took, was that this is the patch he said at #308 he did not want. Lane C made the KPI tile the one reference, because it was the superset (the stat card's parts plus the trend and target slots), renamed its vocabulary, and kept the old names only as alias seats and a generated canon alias, so nothing drawn on them moved. The stat card's own drawing was kept untouched, because three live pages were built on it and moving them would move the arrow's colour. That was a look change, so it was his to see first.
### 3. The arrow's ink: canon already had the answer
His 07:07 line, *"the arrow must be the the right RAG ink"*, sounded like a new decision. Lane D found it was an old one, never applied to the stat card: `s263-D1` puts the delta glyph on the ink seat, `s182-D3` says it follows the red and green inks for all themes, and the two-red law and its green mirror give the four values. The stat card had kept the fill seat, with per-theme overrides, one of which (#66CC8D on white) read at 1.98:1. Moving the pages onto Metric applied the ruled ink everywhere. Lane D also said what canon does NOT allow: the colour follows direction, never the metric's sense. That became call 6a on his page, and he chose against the recommendation. A metric may now say up is bad (`s309-D5`).
### 4. The checks that weren't made
Late on Tuesday the conductor told him two checks could not run in full on his computer. His answer, *"I'm worried that the checks weren't made"*, was right, and lane E found the exact reason: the survey only asks steps whose arguments are `--check` or `--selftest`, so the assertion gate that went red on `528e8318` was asked by nobody before the push. The fix was not to make the survey braver on the real tree. It was a throwaway clone on the VM's own disk, where every step can run without touching the mount. The two slow or blind checks were fixed where they were weak: state-contrast in slices merged to a byte-identical audit, and hit-area reading the seat's browser path. He then made the routine a rule for every lane (`s309-D7`).
### 5. The review page, and a door that closed
He asked for a review page rather than PNGs so he could comment. The page was built the usual way, but publishing it into the shared artifact was refused by a permission check. He opened it from Finder and answered it, so the work was not blocked, but the route review pages have used since #304 did not work this session. His comments found four looks; lane G traced each one before touching it. Only one (the stretched sparkline) came from the move, and only that one was fixed. The other three were older and became rows.
### 6. The two reds, and why each is now a line
Both reds came from a lane leaving a mechanical step for someone else: a new meta without the ASSERT-009 re-base, and a regen whose appended observations file was not committed with the schematic. Each is now a line in the handoff's cold-seat list. The first is exactly what the new pre-push routine catches; lane E proved that on the red commit itself.
### Resolved, and still open
Resolved: the cards-and-tiles model, Metric, the ink, the full-ink no-change mark, the up-is-bad setting, the pre-push routine, `s309-D1`..`D7`. Open, and his: the arrow's shape, which metrics are up-is-bad, the dark ground and tiles, the one-tile group, the re-cut at the end of the week, the container types, and the route for review pages.

## @findings
- **A bracketed number inside a carry item is read as its age.** `_capture_gate._carry_items` found `[68]` (a build step number) in this wrap's new item ⑦ and counted that `[NEW — 0]` item a wrap early: 430 instead of 429. This seat reworded "step [68]" to "step 68" in the new section and in `new.txt` (one hand step; the item is this wrap's own text, written minutes before). The general fix is phase 3's: read the age only from the bracket right after the title.
- **`_CARRIES.md` is 38 MB** (38,169,086 bytes before this roll; the roll added 382,860 characters). Every roll copies the whole previous list forward. Not changed; stated for phase 5 (`s306-D8`).

## @questions
None new from this seat. The OWED list in `_HANDOFF-160` carries his.

## @unproven
None.

## @skips
THE FOURTH WRAP ON THE REDESIGN'S TOOLS, THE FIRST DATE SPLIT ON THEM: every figure from `_wrap_facts.py`, one move file from `_wrap_ops.py --date 2026-09-30 --session-date 2026-09-29 --date-split` (plus the 5b, 13 ops in `_ops-309W.json`), carries by `_wrap_carries.py`, rows by `_wrap_rows.py`, one regen by `_wrap_regen.py --run --session 309`, the commit by `_wrap_commit.py`, CI by `_ci_readback.py`; counts in `notes/_subreports/2026-09-30-309-W-wrap.md`. The six lane transcripts were copied with the conductor's; this seat's own transcript (`agent-a464a5fb2d18d0bc9.jsonl`) was not. The brief typed {facts.fill.now:,} for the fill ("{facts.fill.now:,} at 12:08Z"); the brief and the hand sum agree. 2c, 2d, 2f, 2g ALL RAN by the move file. 2d's `Previous:` trim and 2e moved nothing. The `size:` stamp is THIS wrap's, GENERATED by `_gen_size_stamp.py --write`. Step 3 is a SEAT LIMIT BY THE BRIEF: payloads in `notes/_lanes/309/W/_work/`, the note `notes/_lanes/309/WRAP-MEMORY-HOOK.md`. Other-seat dirty paths are carried by name in the wrap report; the transcripts in `knowledge/_tmp/wrap309/` are gitignored and never committed.

## @section_usage
GM HDR:R LATEST:C PRIOR:R DOFIRST:U A:U C1:U C2:U C4:U STRATA:C · LS HDR:C LANES:U SPIN:U DELTAS:C WEBFONT:U LIVE:U LIFECYCLE:U DEAD:U OPEN:U TARGETS:U SPINOFFS:U

## @tally
