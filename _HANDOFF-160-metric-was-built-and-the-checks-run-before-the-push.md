# HANDOFF #160 — #309 → #310 — METRIC WAS BUILT, THE ARROW TOOK THE RAG INK, AND THE CHECKS RUN BEFORE THE PUSH

provenance: 309 · 2026-09-29
status: observed

*Written by the delegated OPUS 5.5 wrap seat at the close of #309 (conductor Opus 5.5, a CLOUD session linked to Dave's computer). Every figure is from `notes/_lanes/309/W/FACTS.json` (`_wrap_facts.py`) unless it says otherwise; the lanes' figures are the lanes'.*

⛔ **DATE SPLIT, THE ELEVENTH ON THIS RUN (`s294-D11`'s shape, nothing re-dated).** Opened Tuesday 2026-09-29 20:47 BST (`_HANDOFF-159`, chat "Good Morning!"); lanes B and C ran that night; resumed Wednesday 2026-09-30 07:07 BST; his words at 13:08 BST, verbatim: *"i think we need to wrap"* (just after *"how hot are you"*). The ritual is Wednesday.

⛔ **`knowledge/_rulings.json` READS 841**, newest `s309-D7` (834 at the opener). Every one of `s309-D1`..`D7` is his, from a chat line or his review export, kept verbatim in `notes/_lanes/309/DAVE-*.md`. **Quote them; never paraphrase.**

⛔★ **#310'S FIRST BEAT: READ THE `CI owed:` LINE AT THE FOOT, THEN PUT THE ARROW TO HIM.** His review page's item 2 (thin line arrow or the filled triangle back, in the RAG ink) came back "not answered". The ink is ruled (`s309-D3`); the shape is not. The thin arrow stands meanwhile.

⛔ **THE FILL IS A HAND SUM BY `_wrap_facts.py`**, over the conductor's cloud transcript `/root/.claude/projects/-home-claude/c90b4000-f5d3-5ec7-b472-e34bacefa744.jsonl`, copied to the gitignored `knowledge/_tmp/wrap309/`: **boot 133,692** (under the 135,000 ceiling by 1,308) · 160,000 at 20:50 Tue · **300,000 at 10:39 Wed** · 320,000 at 11:48 · **326,997 at his "i think we need to wrap"** (13:08), under the hard 350,000 (`s305-D62`) by 23,003; the brief's typed figure agrees · 336,396 at the launch of this seat. subs 1,780,076 real (n=6, quota, never added).

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-159`.** Every open item on those still stands **except the ones struck with receipts**: this wrap strikes `_HANDOFF-159` OWED item 1 (build the cards and tiles), in `_CARRIES.md` § `residual → #310` and by addition at the foot of `_HANDOFF-159`.
4. **His words:** `notes/_lanes/309/DAVE-WORDS-2026-09-29-2137.md` · `notes/_lanes/309/DAVE-WORDS-2026-09-30-0707.md` · `notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md`.
5. `_CARRIES.md` § `residual → #310` when you need the bodies. Fetch the section; do not read it at boot.
6. The lane reports, when the work needs them: `notes/_subreports/2026-09-29-309-{B,C}-*.md` · `notes/_subreports/2026-09-30-309-{D,E,F,G}-*.md` · this wrap's `notes/_subreports/2026-09-30-309-W-wrap.md`.

---

## ⛔⛔ HIS WORDS (chat lines; the exports are in the files above)

> Tue 20:47 — Good Morning!

> Tue 20:50 — go *(build the cards and tiles)*

> Tue 21:37 — 1. good
> 2. go *(tabs, accordion and popover are blocks; Metric rebuilt properly)*

> Wed 07:07 — 1. Moving to metric is probably a good idea but the arrow must be the the right RAG ink
> 2. We'll recut towards the end of the week
> 3. I'm worried that the checks weren't made can we investigate, im sure we can find a work-around
> 4. Please delete

> Wed 10:24 — Can I have a review doc rather than pngs. there are a few comments I want to make

> Wed 11:04 — (his review-page export, `DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md`) 3. *"1. the filters are stacking vertically here 2. theres no tile colour in dark mode, if there is I cant see it, the background should be the darkest grey and the tiles black. Anyway this is something we need to decide separatly."* · 5. *"the sparkline has become an area chart, but weird, and I though we had a rule for the minimum items in a stat bar. where has tall that blank space come from on the after"* · 6a "Let a metric say up is bad (not the recommendation)" · 6b "Full ink, as ruled (the recommendation)" · 6c "Yes (the recommendation)" · 2 "not answered"

> Wed 13:08 — how hot are you

> Wed 13:08 — i think we need to wrap

---

## WHAT THE SESSION DID

- **The opener.** #308's owed CI read was green on `3457115c`.
- **The cards and tiles, built (lane B, `94ba3c73`..`bba80abd`).** Five kinds (layout, housing, record, block, part) on every meta; the advisory accepts check inside `_validate_edges.py --check`; container, surface and panel defined, the chart-panel role renamed chart; the four limits; the carousel-holds-cards ruling now derived. W-308ir, is, it, iv closed. Lane B stopped Metric on scale (canon.css 193 mentions, pinned by the 27 chart receipts) and found 5 refusals, all from classing tabs, accordion and popover as housings.
- **His 21:37 answers (lane C, `4b64f0e8`..`f197743e`).** `s309-D1`: tabs, accordion, popover are blocks, the check reads 110 of 110. `s309-D2`: Metric as one block (the KPI tile's reference renamed, the trend an optional slot), stat-card and kpi-tile as alias seats, `.cn-kpi-tile` generated as an alias, the 27 chart receipts re-driven with no measurement moved, the explorer rebuilt at v1.35. W-308iu closed.
- **CI red on `528e8318`** ([10], ASSERT-009 138 → 139 for `metric.meta.json`); lane C skipped the re-base. The conductor re-based it (`054aee4b`); green.
- **His 07:07 worry about the checks (lane E, `b690a19b`).** The survey counts any step that is not `--check`/`--selftest` as mutating and never asks it, so [10] was asked only by CI after the push. Now: state-contrast runs in 8 slices at the seat (about 4.3 min, the merged audit byte-identical to CI's); hit-area reads `$RENDER_SHELL` first; a `/tmp` clone surveyed with `--include-mutating` in four chunks gives CI's whole blocking verdict (about 7 min, 12 with the sweep) and caught the `528e8318` red. His "Please delete": `outputs/309/{B,C}` (141 MB) went, on the delete permission he granted at the prompt.
- **His 07:07 items 1 and 2 (lane D, `06062e9f`..`893028e1`).** `s309-D3`: the banking demo, the progress dashboard, the receipt test and the FAB overlay moved onto Metric, the arrow on the ink seat (rise #137F3C light / #66CC8D dark, fall #DA1A00 / #F6604C, all four themes). `s309-D4`: the designer pack is re-cut towards the end of the week. The full state-contrast audit regenerated (it covered only 3 snippets since lane C).
- **His review page (lane F, `6e7af8c5`):** `notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html`. ⚠ Publishing it into the artifact "Apollo 304 review" was REFUSED by a permission check (rebuilding the artifact's index from a read of it); the page lives in the repo only and he opened it from Finder.
- **His 11:04 export (lane G, `d1c0f8b7`..`99ba4a6e`).** `s309-D5` (a metric may say "up is bad", NOT the recommendation): the optional `upIsBad` setting, on no live page. `s309-D6`: the no-change mark at full ink. `s309-D7`: every lane runs the pre-push check, now step 5 of the Worker checklist in `knowledge/_RUNBOOK-parallel-conductor.md`. The receipt sparkline the move had stretched across 1,360 px is fixed (`e649da06`). Three looks pre-date the move and are rows: the filters (W-309g3), the receipt page's chart script and splice (W-309g4), the one-tile group (W-309g4). The dark ground is his (W-309g2).
- **CI red on `99ba4a6e`** ([131] schematic stale): lane G's regen left `knowledge/_graph-mark-observations.jsonl` uncommitted. The conductor committed it (`fc203264`); its CI is read in § POST-WRAP.

| Range | What |
|---|---|
| `3457115c..fc203264` | 23 commits, all pushed (`notes/_lanes/309/W/COMMITS.txt`) |
| *the wrap* | § POST-WRAP |

---

## ⬛ OWED TO #310, IN ORDER — EACH WRITTEN AS THE QUESTION IT IS

1. ⬛★★★ **The arrow: keep Metric's thin line arrow, or bring the filled triangle back, in the RAG ink?** His review page item 2, unanswered. The ink is `s309-D3`'s; only the shape is open. The thin arrow stands meanwhile.
2. ⬛★★ **Which live metrics are "up is bad"?** The option exists (`s309-D5`, `upIsBad`); no page uses it. The banking demo's "Net FX exposure" is the live example lane D named.
3. ⬛★★ **Dark mode: what ground and tile colour?** W-309g2, his words: *"the background should be the darkest grey and the tiles black. Anyway this is something we need to decide separatly."*
4. ⬛ **Mine, small: can the three older looks be fixed?** The banking demo's filters onto one row (`.ftb-row` → `.ftb-primary`, W-309g3). The receipt page: load the chart script and fix the splice markers that drop a rule each (W-309g4). The one-tile stat group against the minimum of two is his call (W-309g4).
5. ⬛ **The designer pack re-cut, towards the end of the week (`s309-D4`):** Metric, the kinds and the logos fix (W-305v2) ride it.
6. ⬛ **Container types: does he want section, division, sector, panel?** W-308iw. Then everything still standing on `_HANDOFF-159` OWED items 3 to 6 (the edge register items 5 to 9 and W-308ie; the bento-matrix selftest's two reds; the picture-page rows; the older carries).
7. ⬛ **The review surface: how should review pages reach him now the publish step is refused?** The #309 page is not in the artifact.
8. ⬛ **Found and not acted on:** hit-area has never run in CI (its words say the render job runs it; `gates.yml` does not); `knowledge/_HIT-AREA-ADVISORY.md` dates from 2026-08-19 (77 snippets against today's 137); the stat card's own drawing still exists (showroom, gallery, the frozen #227 retrieval pair).

---

## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING

- ⛔★★ **THE PRE-PUSH ROUTINE IS NOW WORKER CHECKLIST STEP 5 (`s309-D7`):** a `/tmp` clone, the chunked survey 1:12, 13:55, 56:140, 141:167 with `--include-mutating`, `test_gates`, `_validate_evidence`, and the sliced state-contrast sweep when snippets or canon change. Do not survey on the mount for this: it never asks the writer gates.
- ⛔★ **ADDING OR REMOVING A COMPONENT META ⇒ RE-BASE ASSERT-009 IN THE SAME CHANGE** (`notes/_lanes/309/cond/assert009_rebase.py`). Red on `528e8318`.
- ⛔★ **A REGEN THAT APPENDS TO `knowledge/_graph-mark-observations.jsonl` MUST COMMIT IT WITH THE SCHEMATIC**, or CI's [131] reads stale. Red twice now (#308 lane I's rule, #309 `99ba4a6e`).
- ⛔ **`device_bash` DEFAULTS TO A 120 s TIMEOUT.** Pass `timeout_ms` (up to 178000) on a commit, or it is killed before it lands.
- ⛔★★ **NEVER RUN `git status`.** After every gate run, `python3 knowledge/_wrap_commit.py unlock --tag <n>-<seat>`. A no-op `git add` strands `.git/index.lock` on this mount.
- ⚠ **THE COMMIT GATE REFUSES A REPORT WITH NO STORE ROW.** Lane F's passed on `DOC_ROW_ACK`; W-309f1 was added after.
- ⚠ **THE ARTIFACT PUBLISH OF THE REVIEW INDEX WAS REFUSED BY A PERMISSION CHECK THIS SESSION.** Owed item 7.
- ⚠ **A carry item must not hold a bracketed number like `[68]`:** `_carry_items` reads it as the item's age and counts a `[NEW — 0]` item early. This wrap wrote one, caught it, and reworded it (429, not 430).
- ⛔ **Window lines (`s305-D62`, `s305-D64`):** stop 300,000 · limit 320,000 · hard 350,000 · `BOOT_CEILING_TK` 135,000. This session crossed the stop at 10:39 Wed and the limit at 11:48.
- ⛔ **Project memory: none at the opener, none while the chat is live.** The note is placed only after he says he is done.
- ⚠ **Other-seat paths stay dirty by declaration** (the W report names them); the transcripts in `knowledge/_tmp/wrap309/` are gitignored.

---

*Filed report: `notes/_subreports/2026-09-30-309-W-wrap.md`. Dossier: `_DECISION-HISTORY/2026-09-29-309-metric-was-built-and-the-checks-run-before-the-push.md`. Memory hook: `notes/_lanes/309/WRAP-MEMORY-HOOK.md`. Figures: `notes/_lanes/309/W/FACTS.json`.*

*Title the next chat:* `Apollo - #310: the arrow, the dark ground and the loose ends`

---

## ⬛ POST-WRAP ADDENDUM (5b) — BY ADDITION; NOTHING ABOVE IS REWRITTEN

**No ruling landed after the wrap gate ran**, so no banner addendum is owed. The `s271-D4` re-read strikes nothing: `_rulings.json` reads **841, newest `s309-D7`**.

1. ✅ **CI IS GREEN.** `b973f27a` run `36715837052`, all three jobs (release, gates, render), read by `_ci_readback.py` at 12:51 UTC (`notes/_lanes/309/W/_ci-runs-b973f27a.txt`). The wrap commit `2e90d6d5` has no run of its own: CI runs on a push's tip.
2. ✅ **THE OWED READ ON `fc203264` IS GREEN:** run `36713414485`, all three jobs, the render job finishing 12:27:57 UTC (`notes/_lanes/309/W/_ci-runs-fc203264.txt`). The [131] red on `99ba4a6e` is closed.
3. ⛔ **THE WRAP COMMIT IS `2e90d6d5`, ON THE `--wrap` PATH** (gate `247 in scope · 0 fail · 49 warn`), 19 paths plus the auto-staged rehearsal log, in one run of 114 s. **`b973f27a` carries the seat's 33 files** under `notes/_lanes/309/W/`, split off on the #308 lesson (keep a `--wrap` run under about 30 paths). Both passed first time.
4. **THE PUSH: `fc203264..b973f27a`**, plain `git push origin master`, fast-forward checked first, `git ls-remote` = local HEAD, at 12:36:20 UTC, **22.1 minutes from the launch** (12:14:17 UTC); the summary went at the CI read, **36.9 minutes**.
5. **Phase-1 counts:** scripts written **0** · move files **1 + the 5b** · rebuilds **1 for the wrap, 1 for this 5b** · hand steps **1** (one carry item reworded, W report § 3) · commits **2 for the wrap**.
6. ⚠ **`_CHAIN.md` IS 7,947 cl100k, OVER THE 7,700 WARN** (`CHAIN_BUDGET_TK`, `s212-D11`) by 247, under the 10,000 fail. The date-split line and the longer delta are the growth. Stated, not trimmed.
7. ⚠ **The next title.** `GOOD-MORNING.md` carries the brief's `Apollo - #310: the arrow, the dark ground and the loose ends`. `_gen_titles.py` derived `Apollo - #310: the arrow — thin line or filled triangle, in the rag ink?`. Declared, not reconciled. The retrospective rename it derived for this chat: `Apollo - #309: metric was built, the arrow took the rag ink, and the checks run before the push`.
8. ⛔ **MEMORY — NOT WRITTEN BY THIS SEAT.** Payloads are in `notes/_lanes/309/W/_work/`; the note is at `notes/_lanes/309/WRAP-MEMORY-HOOK.md`.
9. ⚠ **STEP 4c runs LAST, after the 5b commit and push.**

CI owed: this addendum's own commit — read by the next opener with python3 knowledge/_ci_readback.py --owed
