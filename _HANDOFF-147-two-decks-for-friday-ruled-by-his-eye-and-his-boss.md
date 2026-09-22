# HANDOFF #147 — #296 → #297 — TWO DECKS FOR FRIDAY, RULED ALL DAY BY HIS EYE, AND HIS BOSS HAD THE LAST WORD

provenance: 296 · 2026-09-22
status: observed

*Written by the delegated OPUS 5.5 wrap seat at the close of #296 (conductor Fable 5.1). Every figure
here was measured at this seat unless it says otherwise. Where the brief declared something this
seat could not measure, it is published as a declaration and never as a reading.*

✅ **ONE DAY, NO DATE SPLIT.** The session, all five lanes, the three session commits and this ritual
are all **2026-09-22** (`date` at this seat: `Tue Sep 22 19:24:12 UTC 2026`, 20:24 BST). Nothing was
re-dated, and no date-split header line was added to `GOOD-MORNING.md`.

⛔ **NOTHING WAS INSCRIBED. `knowledge/_rulings.json` READS 638**, checked here by `json.load` over the
`rulings` list (id and count only): the newest is still `s295-D4`. He never said "inscribe". Every
ruling-shaped thing at #296 is a **question put** (`s271-D4`) or a design instruction on a deck.

⛔ **THE FILL IS UNMEASURED.** `_checkin.py` found no transcript at the conductor's seat or at this one.
The conductor's **~185,000** at the brief's cut is his own count, **declared**. No band is claimed.

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-146`.** Every open item on those still stands **except the
   TWO struck here with receipts** — see § THE STRIKES.
4. `notes/_lanes/296/DAVE-RULINGS-2026-09-22.md` — his words, verbatim, in order, with what was done on
   each. **Quote them; never paraphrase.**
5. `_CARRIES.md` § `residual → #297` when you need the bodies — **654 probeable items, 12 new, 2 struck**.
   Do not read it at boot; fetch the section (`_memento_search.py` → `--fetch carries:residual-297`).
6. The five lane reports `notes/_subreports/2026-09-22-296-{A,B,B2,C,E}-*.md` and this wrap's
   `notes/_subreports/2026-09-22-296-W-wrap.md`.

---

## ⛔⛔ HIS WORDS

Twelve entries — too long to repeat here, and repeating them would be a second copy that can drift.
They are in `notes/_lanes/296/DAVE-RULINGS-2026-09-22.md`, in order. The four that decide #297:

> okay I need two versions. one sticks with the car-plant analogy and the other is simpler focused on the structure … this doesn't have the metaphor, just observation, problem, analysis, experiment, results, response

> And the payoff is 'Automated product design you can bank on' triple pun, very cool even if I say so myself

> how hot are we I have some changes to make from my boss

> we must be hot now

⚠ **He did NOT say which deck he will show on Friday**, and he did NOT say which cold brief is the demo's.

---

## WHAT LANDED — THREE SESSION COMMITS, UNPUSHED AT THE WRAP'S OPEN

**`cf97ccc4` — the render environment got a BUILDER.** `knowledge/_render/ensure_env.sh` (new) builds or
repairs `outputs/_render-env` on the mount at any seat; `seat_env.sh` points there by default; a ninth
stratum in `knowledge/_RUNBOOK-render-verify.md`. Cause: the first two decks were built in the cloud
because `outputs/_render-env-229` had vanished from the mount, and he asked *"can we permanently fix
this?"*

**`1351175a` — two v14 decks.** Lane **A**: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plant.html`, the
car-plant analogy in his run order. Lane **B**: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html`,
no metaphor. Lane **B2**: five causes and the archive spec's six-step loop on the plain deck. Lane
**C**: the chapter rail, v1 → v6, then ported to the plant deck with the payoff line.

**`c358fc6b` — his boss's pass and lane E.** The plain deck became Problem · Research · Evaluation · The
result · The ask. Lane **E**: the SHELLS knowledge-graph drawing (26 nodes / 26 edges), the brain on a
slide of its own (s7b, words DRAFT), the brain's constants brought to its drawing file (−50 / 20 / 33),
the callipers' plate turned PSI −62 → −90 to match the shared angle. ⛔ **Committed by plain `git commit
-F`, declared** — see § THINGS A COLD SEAT SHOULD KNOW.

⛔ **THE PLANT DECK IS A DAY BEHIND.** It got the rail and the payoff line only. None of the afternoon or
evening rulings reached it.

---

## THE PLAIN DECK AS IT STANDS — AND HOW TO EDIT IT

`notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html`, 16 slides, **GENERATED** by
`notes/_lanes/296/C/build_c.py` from the SOURCE `notes/_lanes/296/C/v14-plain-before-c.html`.
⛔ **Edit the source, never the deck. Do NOT run `notes/_lanes/296/E/build_e.py`** — its source is stale;
it would drop the conductor's s9 change and all of lane E's second pass.

DOM order: s1 cover · s2 order of play · s3 Problem *"'Agile' was sluggish."* · s5x Research (the
six-step loop) · s5r what we saw · s4p Evaluation opener *"We asked: what else is slowing design?"* ·
s6 library 36→137 · s7 graph (the SHELLS drawing) · s8 gates *"Third: the system checks and rechecks its
own work."* · s7b the designer's brain (DRAFT words) · s6b breakdown · s10 three elements · s10map map
(hub *Apollo / Smart design system*) · s9 *"The working system / Let's build something."* · s11 the ask
(untouched) · s12 close *"Apollo / Automated product design you can bank on."*

Rail: **Problem** s3 · **Research** s5x[s5r] · **Evaluation** s4p[s6 s7 s8 s7b s6b s10 s10map] · **The
result** s9 · **The ask** s11[s12].

---

## THE STRIKES — BY ADDITION, WITH RECEIPTS (`s183-D1` / `s188-D2`)

1. ⛔ **`_HANDOFF-139…146` — *"the frozen demo prompt is NOT RECOVERABLE"* — STRUCK. THE CLAIM WAS
   FALSE.** Receipt: `notes/_briefs/2026-09-08-258-cold-run-brief.md` lines 13–17 carry it verbatim,
   under `## THE PROMPT (verbatim, FROZEN — do not improve it)`. Surfaced to him at #296. Struck in
   `_CARRIES.md` § `residual → #297` on the ⚠ ⑪ carry. [[unrun-search-indistinguishable-from-absent-record]]
2. ⛔ **`_HANDOFF-146` § OWED 1 — THE PRESENTATION, #296 OPENS ON THE DECK — THE HEADLINE IS STRUCK BY
   ACT.** Receipt: the two v14 decks, a day of his rulings, commits `cf97ccc4` · `1351175a` ·
   `c358fc6b`. ⚠ **The clauses are NOT struck:** the v12/v13 notes (superseded by today's, which is
   not the same as discharged), the workers' finessing to be done *"together"*, and the dashboard
   review.

⛔ **NOT STRUCK, deliberately:** the dashboard-review carry (④ in the #296 set) — the prompt being found
does not tell us which brief is the demo's. *"A strike that is wrong is worse than an item that is
merely stale."*

---

## ⬛ OWED TO #297, IN ORDER

1. ⬛★★★ **FRIDAY 2026-09-25 IS THREE DAYS OUT — WHICH DECK CARRIES?** The plain deck is the one he
   worked all day; the plant deck is a day behind. **He has not said. Ask at the opener.**
2. ⬛ **The brain's angle** — its own −50 / 20 / 33 (his #292 ruling, the brain alone) or the shared
   −35 / 20 (books, gearbox, shells, callipers). His to rule; the conductor recommended the shared
   angle. Put to him at the wrap call.
3. ⬛ **The brain slide's words (s7b) are a DRAFT, not his.**
4. ⬛ **The catalogue plate** — PSI −5, plate 11.17° / 30.64°, now the only drawing off the shared
   angle. One constant. Unruled.
5. ⬛ **The proficiency image** (draughtsman's tools or a desk) — parked by him.
6. ⬛ **The map slide's placeholder footnote and slide 6's whiteboard footnote** — flagged twice,
   unruled.
7. ⬛ **Port today's plain rulings to the plant deck — only if the plant deck carries.**
8. ⬛ **Which cold brief is the demo's** — still unnamed. Candidates:
   `notes/_briefs/2026-09-08-258-cold-run-brief.md` and
   `notes/_lanes/288/GRILL-SOURCE-2026-09-18-hsbc-ceo-international-banking.md`.
9. ⬛ **`notes/_lanes/296/E/_dbg-*.png` are his to delete** (this mount refuses `unlink`).
10. ⬛ **The `_git_commit.sh` first-add lock variant needs a mechanism, not a workaround.**
11. ⬛ **#296's FILL is UNMEASURED at every seat.** Whether the transcript path moved or the seat changed
    is not diagnosed.
12. ⬛ **The memory hook is owed to the conductor** — `notes/_lanes/296/WRAP-MEMORY-HOOK.md`, § FOR THE
    CONDUCTOR.
13. ⬛ **Everything in `_CARRIES.md` § `residual → #297` that #296 did not touch**, each at its true
    age — including every item `_HANDOFF-146` § OWED 2–14 named (the 98, `s294-D11`/`D12`, the push
    arm's hatch, the selftest's CI fail, `--wrap` in no CI step, and the rest).

---

## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING

- ⛔★★ **`_git_commit.sh` CAN STRAND THE INDEX LOCK ON ITS OWN FIRST ADD.** At #296 the script's
  auto-stage of `notes/_REHEARSAL-LOG.jsonl` stranded `.git/index.lock`, and every named path after it
  was refused; four refusals, then `c358fc6b` went by plain `git commit -F`, declared (transcripts
  `outputs/_gitcommit-transcript-17901042*.log` · `…43*` · `…44*`). The #295 recipe still applies
  between attempts: **`mv` the index lock → `git reset -q` → `mv` the refs locks (`HEAD.lock`,
  `refs/heads/master.lock`, `ORIG_HEAD.lock`) → run the committer ONCE with every path unstaged.**
  ⛔ **Never `rm`: this mount refuses `unlink`.** `git status` alone strands one; one was already
  stranded at this wrap's open.
- ⛔ **THE PLAIN DECK IS GENERATED.** Edit `notes/_lanes/296/C/v14-plain-before-c.html` and run
  `build_c.py`. Never hand-edit the deck. Never run `build_e.py`.
- ⛔ **RENDERS RUN AT DAVE'S SEAT, ON THE MOUNT, IN ONE CALL:** `export TMPDIR=/dev/shm; bash
  knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 <driver>` with
  `executable_path=$RENDER_SHELL`. Files for Dave live in the repo beside their source; give him the
  path.
- ⛔ **NO TRANSCRIPT WAS FOUND AT ANY SEAT AT #296.** If `_checkin.py` finds none at #297's boot either,
  write the absence — never a number.
- ⛔ **`_state.add()` refuses a row whose `home` does not exist** — create the file first. **Mint the doc
  rows and regenerate `_CHAIN.md` BEFORE the first commit attempt.**
- ⛔ **THE `_gm_move.py` OPS FILE IS A MSGFILE:** unique name, session-owned path, `os.path.exists` + a
  size floor asserted in the writing process. **THE SHELL EATS BACKTICKS** — write files with quoted
  heredocs or python, never through an unquoted shell string.
- **`pip install tiktoken --break-system-packages` FIRST**, and again after
  `_gate_scratch_hygiene.py --clean --wrap`.
- ⚠ **Three other-seat paths stay dirty by declaration** (`notes/_dream/_GRADE-DECISIONS.jsonl` ·
  `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` · `notes/_lanes/294/WRAP-MEMORY-HOOK.md`); they
  have refused the sanctioned push arm at every seat since #295.

---

*Filed report: `notes/_subreports/2026-09-22-296-W-wrap.md`. Dossier:
`_DECISION-HISTORY/2026-09-22-296-two-decks-for-friday-ruled-by-his-eye-and-his-boss.md`. Memory hook:
`notes/_lanes/296/WRAP-MEMORY-HOOK.md`. His words: `notes/_lanes/296/DAVE-RULINGS-2026-09-22.md`. Lane
reports: `notes/_subreports/2026-09-22-296-A-deck-v14-plant.md` ·
`notes/_subreports/2026-09-22-296-B-deck-v14-plain.md` ·
`notes/_subreports/2026-09-22-296-B2-plain-five-causes-and-the-loop.md` ·
`notes/_subreports/2026-09-22-296-C-plain-chapter-rail.md` ·
`notes/_subreports/2026-09-22-296-E-shells-graph-and-the-brain-slide.md`.*
