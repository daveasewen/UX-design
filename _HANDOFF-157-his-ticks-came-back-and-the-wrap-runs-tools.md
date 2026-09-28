# HANDOFF #157 — #306 → #307 — HIS TICKS CAME BACK, AND THE WRAP RUNS TOOLS

provenance: 306 · 2026-09-28
status: observed

*Written by the delegated OPUS 5.5 wrap seat at the close of #306 (conductor Opus 5.5, a CLOUD session linked to Dave's computer). Every figure is from `notes/_lanes/306/W/FACTS.json` (`_wrap_facts.py`) unless it says otherwise; the lanes' figures are the lanes'.*

✅ **ONE DAY, NO DATE SPLIT.** Opened Monday 2026-09-28 12:55 BST (`_HANDOFF-156`, first beat the 102 parked questions); the wrap was launched at 17:54 BST on the stop line.

⛔ **`knowledge/_rulings.json` READS 712**, newest `s306-D10` (702 at the opener). `s306-D1`..`D3` enacted (the parked check); `s306-D4`..`D10` ruled (the wrap redesign). His words are verbatim in his exports — **quote them; never paraphrase.**

⛔★ **#307'S FIRST BEAT: THE 78 REOPENED QUESTIONS.** He ticked "Keep open" on 78 of the 102; they are live rows again. Ask him how he wants them worked (a sitting page by theme?) before building anything.

⛔ **THE FILL IS A HAND SUM BY `_wrap_facts.py`**, over the conductor's cloud transcript `/root/.claude/projects/-home-claude/5e5935fe-28be-545e-a6fe-beb6756b4b36.jsonl`, copied to the gitignored `knowledge/_tmp/wrap306/`: **boot 131,492** (under the 135,000 ceiling by 3,508) · 160,000 at 13:00 · **300,000 at 16:59** · 320,000 at 17:53 (the brief) · **321,077 at the wrap launch**, over the 320,000 limit (`s305-D62`) by 1,077. The conductor's own sum, 318,882 at 17:50, is reproduced exactly by the tool. subs 2,376,328 real (n=9, quota, never added).

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-156`.** Every open item on those still stands **except the ones struck with receipts** — this wrap strikes `_HANDOFF-156` OWED item 1 (the 102 ticks) by addition at its foot, and two carries in `_CARRIES.md` § `residual → #307`.
4. **His two exports:** `notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md` (15:20) · `notes/_lanes/306/DAVE-RULINGS-2026-09-28-wrap-redesign.md` (16:01). His 16:58 words: `notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md`.
5. `_CARRIES.md` § `residual → #307` when you need the bodies. Fetch the section; do not read it at boot.
6. The lane reports, when the work needs them: `notes/_subreports/2026-09-28-306-{S-parked-check,T-parked-enact,R-wrap-redesign,U-rulings-and-bloat,V-limits-and-phase2,W1-phase1-tools}.md` · this wrap's `notes/_subreports/2026-09-28-306-W-wrap.md`.

---

## ⛔⛔ HIS WORDS

> 12:59 — can you check these I think some of them have been superseded

> 14:16 — please surface the file

> 15:39 — 1. go 2. go

> 16:01 (the redesign export) — lets go with all the recommendations, one thing to check is whether this bloats anything else, we used to have a running tally I think but it bloated the boot

> 16:58 — go on both

"1. go" was the push of the session's work; "2. go" the wrap redesign put on a page. "go on both" was to the conductor's two asks: adopt the eleven limits, and build phases 1 and 2 now so tonight's wrap is their first proof.

---

## WHAT THE SESSION FOUND

- **24 of the 102 parked questions were already answered by later rulings** (lane S, four Opus readers, every row read against `_rulings.json`): 24 answered, 34 partly, 10 unsure, 34 live. He closed the 24 and kept the other 78 open, all of them, including the 34 partly answered.
- **The regen serial in `_HANDOFF-156` was missing a step.** It omitted `knowledge/gen_kg_titles.py`, so the first push went red on CI step [88], KG node titles stale. The conductor fixed it (`fe243c6c`, `notes/_lanes/306/P/`); `_wrap_regen.py` now carries it as step 5 of 8.
- **Where the wrap's time goes** (lane R, #303–#305): 46 to 60 minutes a wrap, about half waiting on CI twice; each fact hand-written in about 7.1 places; `_CARRIES.md` 37 MB, because the whole list is copied forward every wrap.
- **The bloat check** (lane U, his 16:01 question): phases 1, 2 and 5 add nothing to the boot, and phase 5 shrinks the repo. Phases 3 and 6 can grow the boot through the generated handoff, and phase 6 the window through the seam. Both are the July shape; the eleven guards are adopted as `s306-D10`.

## WHAT LANDED

| Commit | CI run | What |
|---|---|---|
| `138d45fe` · `dcb76d81` | `36437656013` RED | T: `s306-D1`..`D3`, 24 closed, 78 reopened, `W-222`/`W-272` settled |
| `fe243c6c` | `36439579304` ✅ | P (conductor): KG node titles regenerated |
| `3b4cae5d` | `36443037064` ✅ | U: `s306-D4`..`D9` ruled, the bloat check |
| `0afaca91` | — | V: `s306-D10`, phase 2 (`_ci_readback.py`, the runbook order, `ci_owed_check`) |
| `079740c5` | `36453625640` (§ POST-WRAP) | W1: phase 1, six wrap tools, `_build_all.py` steps 156–161 |
| *the wrap* | § POST-WRAP | this ritual, on the new tools |

Pushed `80d4198d..dcb76d81`, then `..fe243c6c`, `..3b4cae5d`, `..079740c5`, each on his 15:39 "go". The check page went into the artifact **"Apollo 304 review"** (`https://claude.ai/artifact/1PpLec2QecFEjdnDAXYCw5`), versions 8 and 9; the artifact is not in git.

**The six redesign rulings, in plain words:** the wrap writes the story once, plus measured figures, and every other view is generated from it, the handoff included (`s306-D4`); a generated wrap report counts as the filed report (`s306-D5`); the wrap runs as three seats, story, mechanics and commit, joined at the commit (`s306-D6`); his summary goes out as soon as the wrap is pushed, and the next opener reads the follow-up's CI (`s306-D7`); the carried list stops being copied forward, only what changed is written (`s306-D8`); later, the seam adds his words and the tally to the draft during the session (`s306-D9`). The six phases: 1 tools (built), 2 the one-wait order (built), 3 one story and generated views, 4 three seats, 5 carries by change, 6 the seam draft.

---

## ⬛ OWED TO #307, IN ORDER — EACH WRITTEN AS THE QUESTION IT IS

1. ⬛★★★ **The 78 reopened questions are live again, 34 of them partly answered. How does he want them worked: a sitting page by theme?** `s306-D3`; lane S's verdicts per row in `notes/_lanes/306/S/parked-102-check.json`.
2. ⬛★★ **The redesign continues: phase 3 next (one story, all views generated, the handoff ceiling at 25,270 B and 8,106 cl100k), then 4, 5 and 6. Did tonight's wrap prove phases 1 and 2?** The counts against the targets are in the wrap report and in § POST-WRAP below. If proven, `s306-D4` phase 1 and `s306-D7` move to `enacted` at #307 with this wrap's receipt. Row `W-305wr` stays open.
3. ⬛ **The suggested sentence for his Project instructions, step 1 — does he want to add it?** Lane V, verbatim: *"In the same shell call, also run python3 knowledge/_ci_readback.py --owed; it prints only a short CI summary for the commit the last wrap pushed without waiting, and a red there is the session's first beat."* His text; nothing is edited for him.
4. ⬛ **`_CHAIN.md` is over its advisory warn (7,906 against 7,700 at #305's 5b), and the handoff is not counted in the boot figure** (lane U). Both are phase-3 limits under `s306-D10`.
5. ⬛ **Everything still standing on `_HANDOFF-156` OWED items 2–10 that this session did not strike**, each at its true age: re-sort `s212-D1`/`s256-D1` · the ring against the donut meta · the five new threads · the two token names · the rails half of call 9 · the logos page's four broken images · the Launchpad PoC and the pack's reader group · the dream pass on a live tree, the HSBC face, the callipers, `_HANDOFF-152`'s list, the 180,000 line in `_standing.md`. ⚠ **The wrap redesign (its item 2) is now UNDER WAY, not struck; `W-305wr` stays open.** Item 9 (the boot ceiling) was struck by lane L (`s305-D64`); this wrap struck its two carries.

---

## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING

- ⛔★★ **THE WRAP RUNS TOOLS NOW** (`knowledge/_RUNBOOK-capture-ritual.md`, the PHASE 1 block near the top and "★ THE ORDER AFTER THE COMMIT"): `_wrap_facts.py` · `_wrap_ops.py` → `_gm_move.py` · `_wrap_carries.py` · `_wrap_rows.py` · `_wrap_regen.py` · `_wrap_commit.py` · `_ci_readback.py`. Write no script in `_work/`.
- ⛔ **`{{SECTION_SIZES}}` and `{{ROLL_STATE}}` each become a WHOLE line that already starts `> `** — write the placeholder bare on its line, never `> {{…}}` (this wrap did, and hand-fixed the doubled `> >`; recorded as a phase-1 defect).
- ⛔★★ **NEVER RUN `git status`.** The wrap gate strands `.git/index.lock` on this mount, and `git reset -q` strands `HEAD.lock` and `refs/heads/master.lock`: after EVERY gate run, `python3 knowledge/_wrap_commit.py unlock --tag <n>-<seat>` (moves them to `notes/_lanes/_orphan-locks/`, never `rm`).
- ⛔ **The regen serial is `_wrap_regen.py --run`, ONCE, after the last edit.** It has eight steps, `gen_kg_titles.py` included, `gen_dashboard.py` last. `_memento_search.py` appends to `knowledge/_graph-mark-observations.jsonl`; `--paths-out` puts it in the commit.
- ⛔ **`_gen_titles.py --session N` (step 4b) is NOT in that serial yet**, though the PHASE 1 table says it is: run it after the banner is placed, or the wrap gate fails TITLE GENERATION (found at this wrap).
- ⛔★ **THE PUSH TOKEN IS BEHIND A GET-ONLY CREDENTIAL HELPER** (`.git/apollo-credentials`, `s305-D30`); `_ci_readback.py` reads it through `git credential fill` and never prints it. It expires 6 November.
- ⛔★ **THE REPO `daveasewen/UX-design` IS PUBLIC.** Every push publishes. Push only on his word; he gave it for this session's work at 15:39.
- ⚠ **`_build_all.py` HAS 161 STEPS** (155 `_ci_readback.py` selftest, 156–161 the six wrap tools, appended last; no step number moved).
- ⚠ **`_CARRIES.md` still grows about 370 KB a wrap** (this roll added 371,634 characters) until phase 5 (`s306-D8`, limit 10 of `s306-D10`: at most 20,000 B a wrap).
- ⛔ **Window lines (`s305-D62`, `s305-D64`):** stop 300,000 · limit 320,000 · hard 350,000 · `BOOT_CEILING_TK` 135,000.
- ⛔ **Project memory: none at the opener, none while the chat is live.** The note is placed only after he says he is done.
- ⛔ **`device_bash` kills background jobs when the call returns** — run gates in the foreground with the longest timeout.
- ⚠ **Other-seat paths stay dirty by declaration:** the list in `_HANDOFF-156`, plus W1's untracked `notes/_lanes/306/W1/_gitcommit-W1.log` and `.term`. The conductor's transcripts in `knowledge/_tmp/wrap306/` are gitignored.

---

*Filed report: `notes/_subreports/2026-09-28-306-W-wrap.md`. Dossier: `_DECISION-HISTORY/2026-09-28-306-his-ticks-came-back-and-the-wrap-runs-tools.md`. Memory hook: `notes/_lanes/306/WRAP-MEMORY-HOOK.md`. Figures: `notes/_lanes/306/W/FACTS.json`.*

*Title the next chat:* `Apollo - #307: the 78 reopened questions, how he wants them worked`

---

## ⬛ POST-WRAP ADDENDUM (5b) — BY ADDITION; NOTHING ABOVE IS REWRITTEN

**No ruling landed after the wrap gate ran**, so no banner addendum is owed. The `s271-D4` re-read strikes nothing: `_rulings.json` reads **712, newest `s306-D10`**.

1. ⛔★ **THE WRAP COMMIT IS `5234ce41`, ON THE `--wrap` PATH.** Gate before it: `244 in scope · 0 fail · 341 warn`. 43 paths, every one checked changed or untracked first; `✓ done — locks clear`, exit 0. Log `notes/_lanes/306/W/_gitcommit-W.log`.
2. **THE PUSH: `079740c5..5234ce41`**, plain `git push origin master` through the credential helper; fast-forward checked first; `git ls-remote` = local HEAD. 17:11:58 UTC, **17.6 minutes from the launch** (16:54:23 UTC).
3. ⬛★ **CI, READ BACK BY `_ci_readback.py` — THE ONE WAIT.** `079740c5` run `36453625640` **ALL GREEN** (release, gates, render). The wrap commit `5234ce41` run `36456434157` **ALL GREEN** (release 17:12:48 · gates 17:19:40 · render 17:26:30 UTC). Summaries `notes/_lanes/306/W/_ci-runs-079740c5.txt`, `_ci-runs-5234ce41.txt`. The summary went to Dave at 17:26 UTC, **32 minutes from the launch** (about 59 at #305).
4. **THE PHASE 1 AND 2 PROOF, AGAINST THE TARGETS:** scripts written **0** (target 0; three inline one-off edits, no file) · move files **1 + the 5b** (target 1 + the 5b) · rebuilds **1 for the wrap** (target 1), **plus 1 for this 5b**, because the 5b line lands in the ⏱ delta that `_CHAIN.md` slices · hand steps **2** (`_gen_titles.py` missing from the serial; a doubled `> ` from the placeholder). Detail in `notes/_subreports/2026-09-28-306-W-wrap.md` § POST-COMMIT. Whether this counts as proven is his (OWED item 2).
5. **Locks: 14 lock files moved in four `unlock` runs (the fourth after the 5b gate)** (the gate's `index.lock` each time, plus `HEAD.lock`, `ORIG_HEAD.lock` and `refs/heads/master.lock` from the reset), all in `notes/_lanes/_orphan-locks/` with `306-W` in their names. The committer held none.
6. **`_CHAIN.md` after the wrap's regen: 7,371 cl100k (slice 6,519 + 852), UNDER the 7,700 warn; after this 5b's regen 7,670 (slice 6,818 + 852), still under by 30** — OWED item 4's first half is not true at this wrap, only close; the handoff-not-counted half stands.
7. ⛔ **MEMORY — NOT WRITTEN BY THIS SEAT.** Payloads in `notes/_lanes/306/W/_work/`; the note `notes/_lanes/306/WRAP-MEMORY-HOOK.md`.
8. ⚠ **STEP 4c runs LAST, after the 5b commit and push.**

CI owed: this addendum's own commit — read by the next opener with python3 knowledge/_ci_readback.py --owed
