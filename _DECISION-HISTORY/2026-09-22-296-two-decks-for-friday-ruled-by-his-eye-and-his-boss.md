# 2026-09-22 · #296 — two decks for Friday, ruled all day by his eye, and his boss had the last word

provenance: 296 · 2026-09-22
status: observed

*Session narrative dossier (ritual step 1b). The WHAT lives in the ★ LATEST banner of `GOOD-MORNING.md`, the ⏱ LATEST delta of `_LIVE-STATE.md`, `_HANDOFF-147-two-decks-for-friday-ruled-by-his-eye-and-his-boss.md` and the lane reports; this file holds the WHY and the HOW. Written by the delegated wrap seat (Opus 5.5) from the conductor's wrap brief (`notes/_lanes/296/WRAP-BRIEF.md`), the five lane reports and the three commits. His words, verbatim and in order: `notes/_lanes/296/DAVE-RULINGS-2026-09-22.md`.*

⛔ **No ruling was inscribed at #296.** `knowledge/_rulings.json` reads **638** before and after. Every design decision below is his instruction on a deck, carried out by eye — not a record in the store.

⛔ **The session's FILL is UNMEASURED.** No transcript was found at any seat. Nothing in this file is a gauge reading.

---

## 1 · Why the session was the deck, and why there were two

`_HANDOFF-146` put the presentation first: Friday 2026-09-25 is three days out and it is the internal, and at #295 he had asked for it himself (*"we need to get back to the presentation soon"*). He opened #296 by asking for **two** decks, not one: one keeps the car-plant analogy; the other drops the metaphor and follows the structure of the story itself — *"observation, problem, analysis, experiment, results, response"*. The reasoning is his: the plain deck follows the "speed flow" first, *"because its the observation"*, and only then adds consistency and quality, with the knowledge graph *"to join it all together"*.

**How:** both decks were cut from v13 in parallel lanes (A plant, B plain), each by an idempotent builder that asserts its anchors, so the v13 deck is untouched and each v14 can be rebuilt from its saved source. Lane A kept everything from the brain script to the end of the file byte-identical; lane B grep-proved that no plant vocabulary survived in the slide markup.

## 2 · The render environment got a builder, because the decks came back as downloads

The first two decks were built in the cloud, because `outputs/_render-env-229` had vanished from the mount and the seat "had no Playwright". He asked why they were not in his repo, and then: *"can we permanently fix this?"* The fix was structural rather than another rescue: `knowledge/_render/ensure_env.sh` BUILDS or repairs the environment on the mount at any seat, idempotently, and `seat_env.sh` points at `outputs/_render-env` by default. He then wrote the rule into the Project instructions himself: *"Files written for Dave live in the repo beside their source; give him the path, not a download."* Commit `cf97ccc4`. **Why this matters beyond the day:** a render that depends on a directory surviving on the mount fails silently the day it does not; a builder that runs at every boot turns a vanished directory into a slow first call.

## 3 · The plain deck, ruled by eye all day

The pattern of the day was a tight loop: a render at his seat, his words, a small change, another render. Three threads ran through it.

- **The content (lane B2).** He corrected slide 4 to *"There are 5 causes"* and sent slide 5 back to the archive: the experiment was not what the deck described, it was *"build from the 36 components, check's the work and output"*, and there was a diagram. Lane B2 rebuilt the six-step loop from `archive/apollo-pipeline-spec_v0.2_2026-06-20.html` natively on the slide. **Why:** the deck's claim about the experiment has to match the record of the experiment; the archive held the diagram and the deck had drifted from it.
- **The rail (lane C, six versions).** He asked for an orientation pattern — a vertical, persistent progress indicator, circles for chapters, dots for sub-pages, the current chapter large with its number and title. Each version answered one of his sentences: full-height line and a fixed current position (v2); even spacing and titles only on the current chapter (v3); more air, gone from slide 2, a title at eyebrow size (v4); everything but the current chapter faded, lighter on white and darker on dark (v5); the jump between slides 2 and 3 fixed (v6); then the same rail on the plant deck. **How:** the deck became GENERATED — `build_c.py` builds it from a source file — so every later edit went to the source, never to the deck.
- **The words.** The payoff line is his and he was pleased with it: *"Automated product design you can bank on"* — a triple pun for a bank. The eyebrows were brought into step with the rail on his fourteen-line list; the index lost the ask; the prints were left white with a keyline, because the hidden-line drawings' white fills cannot be removed.

## 4 · The cold brief that "could not be recovered" was in the repo

He asked for the cold-start prompt *"to test on my work machine"*, and then for *"another somewhere"* when the first was too basic. Two were surfaced: the frozen prompt in `notes/_briefs/2026-09-08-258-cold-run-brief.md` (lines 13–17) and the work-machine grill brief `notes/_lanes/288/GRILL-SOURCE-2026-09-18-hsbc-ceo-international-banking.md`. **The finding is the first one:** since #288, eight handoffs had carried *"the frozen demo prompt is NOT RECOVERABLE"*. It was in a brief the #288 search had named. It is struck with that receipt. **Why this is worth a paragraph:** an unrun or mis-scoped search reads exactly like an absent record, and the carry survived eight wraps because nothing re-tested it [[unrun-search-indistinguishable-from-absent-record]]. What is NOT settled is which of the two is *"the cold brief we will be doing the demo with"*; he did not say.

## 5 · The boss's pass

In the evening he brought changes from his boss, and the story's shape changed: observation and problem became one chapter, **Problem** (*"'Agile' was sluggish"*); experiment became **Research**, and results folded into it; response became **Evaluation**, opened by the five-causes slide (*"We asked: what else is slowing design?"*); "the build" became **The result**, on a slide now reading *"The working system / Let's build something."* Two of his words were read by the conductor and the readings are declared: *"w'e asked: what else is slowing us design?"* became "We asked: what else is slowing design?", and "a knowledge that joined everything together" had "graph" inserted.

**The drawings (lane E).** He asked for a 3D knowledge-graph drawing from the shells construction to replace the brain, and a slide of its own for the brain after gates and evals, with the brain's rest angle corrected *"the same as the others"*. Lane E drew three nested shells (then 26 nodes and 26 edges on his second ask), moved the brain to s7b, brought the deck's brain constants up to its drawing file, and turned the callipers' plate a quarter turn (PSI −62 → −90) so it runs parallel to the books, gearbox and shells. **The tension the lane named rather than hid:** his #292 ruling set the brain alone at −50 / 20 / 33, while every other drawing rests at −35 / 20. "The same as the others" and "the brain's own ruled angle" cannot both be true. The lane rested the shells at the shared angle and left the brain at −50; the conductor recommended the shared angle. It is his to rule.

Commit `c358fc6b`. ⛔ **It went by plain `git commit -F`**, declared: `_git_commit.sh` refused four times because its OWN first auto-stage of `notes/_REHEARSAL-LOG.jsonl` stranded the index lock, and every named path after it was refused. This is a new variant of the #295 lock class, where a no-op re-add was the trigger. It is recorded and not repaired.

## 6 · What was deliberately NOT done

- **The plant deck was NOT brought up to date.** It has the rail and the payoff line only. Porting a day of rulings to a deck that may not be shown would be work spent on a guess; whether it carries is his call.
- **The brain slide's words were NOT treated as his.** They are a draft.
- **The catalogue plate (PSI −5) was NOT squared**, though it is now the only drawing off the shared angle. One constant; unruled.
- **Nothing was inscribed**, because he did not say "inscribe".

## 7 · Resolved state and what is open

**Resolved:** two v14 decks exist; the plain deck is 16 slides in Problem · Research · Evaluation · The result · The ask, GENERATED from `notes/_lanes/296/C/v14-plain-before-c.html` by `notes/_lanes/296/C/build_c.py`; the render environment rebuilds itself; the frozen prompt is found.

**Open, and his:** which deck carries on Friday · the brain's angle · the brain slide's words · the catalogue plate · the proficiency image (parked by him) · the two footnotes flagged twice · which cold brief is the demo's. **Open, and mechanical:** the `_git_commit.sh` first-add lock variant; the transcript that no seat could find. All carried in `_CARRIES.md` § `residual → #297`.

---

*Links: banner and stratum `GOOD-MORNING.md` (#296) · delta `_LIVE-STATE.md` (#296) · handoff `_HANDOFF-147-two-decks-for-friday-ruled-by-his-eye-and-his-boss.md` · wrap report `notes/_subreports/2026-09-22-296-W-wrap.md` · lane reports `notes/_subreports/2026-09-22-296-{A,B,B2,C,E}-*.md`.*
