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

---

## ⬛ POST-WRAP ADDENDUM (5b) — BY ADDITION; NOTHING ABOVE IS REWRITTEN

⚠ **This addendum is written by a SECOND delegated wrap seat (Opus 5.5).** The first seat ran the
ritual from 19:24 UTC through the commit and the push, and its hand-back never reached the conductor;
it left no § POST-WRAP (its filed report points to one that did not exist) and no push transcript.
This seat found the wrap already committed and pushed, re-verified both, read CI, and filed 5b.
**Nothing the first seat wrote was rewritten.**

**No ruling landed after the wrap gate ran**, so no ★ LATEST banner addendum is owed and the banner is
untouched. The `s271-D4` re-read of the memory hook's open list strikes nothing: `_rulings.json` reads
**638, newest `s295-D4`**, by `json.load` over `rulings`.

1. ⛔★★ **THE WRAP COMMIT IS `39c6ba81` AND IT WENT ON THE TRUE `--wrap` PATH** — the second wrap
   running. The script's own lines (`outputs/_gitcommit-transcript-296W-b.log`):
   **`capture gate [wrap]: 234 in scope · 0 fail · 40 warn`** then **`— wrap gate GREEN on the wrap
   commit (#74-D1 consumer)`**. **18 files changed, 1,914 insertions, 1,101 deletions** (the script's
   count; `git show --stat` without break-detection reads 1,835 / 1,022 — both published), 6 created.
   ⇒ **The `#243` declared not-a-wrap form was not needed.**
2. ⚠ **ONE refusal was paid before it** (`…-296W-a.log`): the #208 `[110]` mention-map re-stale class —
   the gate regenerated `knowledge/_graph-mention-map.json` and, under P5, staged nothing; re-run with
   the path named. The same refusal #295's wrap met. ✅ **The first-add lock variant did NOT fire on
   this commit**: the script logged git's own `unable to unlink '.git/index.lock'` and still closed
   `✓ done — locks clear`; no `.git/*.lock` existed when this seat opened, and no 296W file sits in
   `notes/_lanes/_orphan-locks/`.
3. **THE ★ LATEST BANNER, measured by the gate's own arm** (`section_spans` → `BANNER_LATEST_RE` →
   `measure_tokens`, bounded by the next ★ PRIOR): **764 tape, 8 substantive lines**, against
   `s241-D2`'s **1,200 tape / 10 lines**. ★ **Under by 436 — the first wrap in four NOT to close at
   exactly the cap.** The deck day had few machine findings; that is the reading, not a claim that the
   cap stopped shaping the record.
4. ⬛ **THE PUSH.** **`8af95161..39c6ba81`**, reflog `update by push` at **19:38:26 UTC**.
   `git ls-remote origin refs/heads/master` = **`39c6ba812de600ca4d707d5058923493b7d9fa72`** = local
   HEAD, **verified independently at this seat**; `git log origin/master..master` empty.
   ⛔ **HOW IT WAS PUSHED IS NOT RECORDED.** There is no push transcript and the first seat's stub
   never arrived. The three other-seat paths (`notes/_dream/_GRADE-DECISIONS.jsonl` ·
   `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` · `notes/_lanes/294/WRAP-MEMORY-HOOK.md`) are
   still dirty, so the sanctioned `--push` arm's dirt gate would have refused on them as at every seat
   since #295 — **that is a reading, not a record; do not cite it as the method.**
5. ⬛★ **CI, READ BACK FOR THE WRAP SHA — run `35775081617`, POLLED TO COMPLETION, verdict taken AFTER
   `render` closed.** `release` ✅ SUCCESS at 19:39:07 · `gates` ⛔ FAILURE at 19:43:41, **steps 5 and
   6** · `render` ✅ SUCCESS at **19:53:26 — 9m45s after `gates`** (the #291/#292 lesson, met an
   **eighth** time).

   ```
   SURVEY: 59 pass · 6 FAIL · 4 COULD-NOT-ASK (self-declared refusals) · 0 unaskable (missing/timed out) · 77 not asked (mutating)
   ```

   **IDENTICAL to #295's wrap read on `d9b7320f`.** The six BY NAME: token blast-radius + graph report
   · capture/provenance selftest (still *"no `pre-flight:` stamp"*) · component-partials sync ·
   memento schematic determinism · memento-package delta-audit selftest · governs matcher selftest.
   ✅ **`read chain determinism check` is GREEN on a second wrap tree.** Step 6 aborts where it always
   does (`help-gate: 264 script(s) scanned, 12 failure(s)`; evidence gate `6 lint · 0 unparsed · 5
   rc/observation mismatch`). ⛔ **Nothing CI reported was repaired.**
6. **THE `s214-D6` CHAIN FIGURE AT 5b.** Before: **7,010 tape (slice 6,155 + 855 wrapper), ratio 21%**.
   After this addendum's ⏱ delta line: **7,606 (slice 6,751 + the same 855), ratio 23%** of a
   `GOOD-MORNING.md` of 33,608 tape. **Inside the `<40%` floor and under the ~10–12K target** — ★ unlike
   #295's 5b, which pushed the chain 1,035 past the target. Both figures reported, no third
   invented; `_gen_chain.py --check` FRESH after regeneration. ⛔ No literal was moved.
7. ⚠ **FILL for #296 stays UNMEASURED.** This seat, too, is a remote-device seat with no `.claude`
   transcript tree; no number is written. The conductor's ~185,000 remains his declaration.

---

## ⬛ #297 FIRST-CHAT ADDENDUM — BY ADDITION; NOTHING ABOVE IS REWRITTEN

*Written 2026-09-22 ~21:45 BST by the first #297 chat (Opus 5.5 conductor, a CLOUD session linked to
Dave's computer). That chat was closed on Dave's word *"fresh"* at ~186,000 fill with no work done beyond
one commit. **No wrap was run. THE NEXT CHAT IS STILL #297** — the chain title stands.*

1. ⛔★★ **WHY #296's FILL WAS UNMEASURED — FOUND.** The conductor now runs in the CLOUD workspace and its
   transcript lives THERE: `/root/.claude/projects/-home-claude/<session-id>.jsonl` (the cloud `Bash` tool,
   not `device_bash`). `_checkin.py` globs `/sessions/*/mnt/.claude/projects/*/*.jsonl` on the device and
   says NO TRANSCRIPT FOUND. **Read it in the cloud shell** by summing `input_tokens +
   cache_creation_input_tokens + cache_read_input_tokens` over `message.usage` (the check-in's own
   `FILL_FIELDS`), one row per distinct `message.id`. That is a hand sum, not a `_checkin.py` run — say so.
   ⚠ #296 almost certainly failed the same way; NOT verified.
2. ⛔★★ **BOOT 127,609 real, first turn** (cache_creation 127,607) against `BOOT_CEILING_TK` **72,768**
   (`s295-D3`) — over by **54,841**. After the opener reads (handoff · chain · index · dave-voice · check-in
   · ensure_env): **168,388**. Third turn: **177,764**. The attribution is UNMEASURED (the system prompt is
   not in the transcript). Dave: *"that boot is massive again, i've switched off the docs."* — the Claude
   Docs connector went off at ~21:33; the cache prefix held through it, so it did NOT reach that chat.
   **The fresh chat's first turn measures his switch-off.**
3. ✅ **`22a6a6a8` — the routing doc names Opus 5.5 as the default for every sub**, on his *"okay can you
   change the routing doc to specify 5.5 as teh defaults for subs"*. `MODEL-ROUTING.md` Default tier
   Opus 5 → Opus 5.5 (`claude-opus-5-5`) plus a by-addition note. **NOT PUSHED.** The Premium line
   (`claude-fable-5` vs Fable 5.1) noticed, not changed.
4. ⬛ **PARKED, HIS WORDS — routing by effort:** *"by most evaluations Opus surpasses Fable now or is very
   similar, so i might be using opus at different effort levels for the routing, we can work on this
   later"*. Not a ruling; not started.
5. ⬛ **THE DECK QUESTION WAS PUT AND NOT ANSWERED.** Recommendation given: the PLAIN deck carries Friday
   (a day of his rulings and his boss's pass; the plant deck a day behind). Ask again at the opener.
6. ⚠ **`git status` stranded `.git/index.lock` twice; both moved to `notes/_lanes/_orphan-locks/*.297-*`**
   (his to delete — the mount refuses `unlink`). `_git_commit.sh` needs `SESSION_N=297` on a non-wrap
   commit, and line 1 of the msgfile WITHOUT the `after #N` prefix (T3 adds it).

---

## ⬛ #297 WRAP — STRIKES ON § OWED, BY ADDITION; NOTHING ABOVE IS REWRITTEN

*Written 2026-09-23 by the #297 delegated wrap seat (Opus 5.5), `s183-D1` / `s188-D2`: each strike names the session that closed it and where the closing is inscribed. The same eight are struck in `_CARRIES.md` § `residual → #298`. The successor handoff is `_HANDOFF-148-the-plain-deck-carries-friday-and-his-eye-ruled-it-slide-by-slide.md`.*

1. ~~Which deck carries~~ — **STRUCK #297: the PLAIN deck.** His *"plain"*, 22:00 BST 2026-09-22, `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md`; every #297 lane worked it (`57e885b0` … `f848330e`).
2. ~~The brain's angle~~ — **STRUCK #297: the shared −35 / 20.** *"1. okay do it"*, same file; enacted by lane A, `57e885b0`. His further pivot pick (A/B/C) is a new item.
3. ~~The brain slide's words are a draft~~ — **STRUCK #297: kept.** *"2. this copy is fine"*, same file.
6. ~~The two placeholder footnotes~~ — **STRUCK #297: removed.** *"4. remove the notes"*, same file; lane A, `57e885b0`.
7. ~~Port the plain rulings to the plant deck~~ — **STRUCK #297: moot.** Its condition failed: the plant deck does not carry (*"plain"*).
8. ~~Which cold brief is the demo's~~ — **STRUCK #297: `notes/_lanes/288/GRILL-SOURCE-2026-09-18-hsbc-ceo-international-banking.md`.** *"5. it's the one we reconstructed from co-pilot … but we'll make changes to it"*, same file. His changes are a new item.
11. ~~Why #296's FILL was unmeasured~~ — **STRUCK #297: found.** The conductor runs in the cloud; its transcript is outside the device glob — § #297 FIRST-CHAT ADDENDUM 1 above, `4fe02e0e`. #296's own figure stays a declared absence.
12. ~~The #296 memory hook~~ — **STRUCK #297: placed.** The Project memory holds `wrap-296-two-decks-for-friday-ruled-by-his-eye-and-his-boss.md` (2026-09-22 20:14:49 UTC) and an updated `index.md` (20:16:14 UTC), listed at the #297 wrap seat.

⛔ **NOT STRUCK:** 4 the catalogue plate · 5 the proficiency image · 9 `notes/_lanes/296/E/_dbg-*.png` · 10 the `_git_commit.sh` first-add lock · 13 everything else in `_CARRIES.md`.
