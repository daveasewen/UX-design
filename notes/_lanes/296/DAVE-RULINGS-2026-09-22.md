# #296 — DAVE'S WORDS, VERBATIM, IN ORDER

provenance: 296 · 2026-09-22 · conductor Fable 5.1 · written by the delegated wrap seat from the conductor's wrap brief
status: observed

*Quote these; never paraphrase. Each entry is followed by what was done on it.*

⛔ **NOTHING HERE WAS INSCRIBED.** He never said "inscribe" at #296. `knowledge/_rulings.json` stays **638** (asserted by `json.load` count at the wrap seat). Every ruling-shaped thing below is a **QUESTION PUT** in the `s271-D4` sense, or a design instruction on the deck carried out by eye — not a ruling in the store.

⚠ **Source of these words:** `notes/_lanes/296/WRAP-BRIEF.md` § *Dave's words — VERBATIM, in order*, cut by the conductor at 20:22 BST. Where the brief itself abbreviates a long message (entry 2's ten-step run order, entry 7's fourteen-line eyebrow list), it is reproduced here **exactly as the brief carries it** and marked; the full text is in the chat and in the lane reports named against each entry. No word was supplied by this seat.

---

## 1

> good morning

Opener. The session opened on the deck, as `_HANDOFF-146` § OWED 1 required.

## 2

> okay I need two versions. one sticks with the car-plant analogy and the other is simpler focused on the structure: Observation-dev getting faster, the breakdown from the image I've pasted before(see image). it will follow the 'speed flow' first because its the observation, break it down, explain the experiment with the agentic loops, what was observed at that point, the component library then add the consistency and quality after that story, then the knowledge graph to join it all together. this doesn't have the metaphor, just observation, problem, analysis, experiment, results, response

Followed by his ten-step run order, **as the brief carries it (abbreviated by the conductor)**: 1 cover good · 2 title wrong, *'what you'll see in the next 15-20 minutes'*, chapter titles wrong · 3 initial observation · 4 systemised design (metaphor intro only) · 5 the experiment good · 6 NEW the insight from slide 4 · 7 the breakdown of speed/quality/consistency, *"this confirmed what we always knew and maybe we now have the opportunity to hopefully solve three things"* · 8 was 6 *"the first improvement, the catologue went from 36 to 134"* · 9 was 7 *"The robots needed a shared brain, then about the carplant being a custom shop"* · 10 was 8 *"we say the same brain rechecks the work for QC"*.

**Done:** two v14 decks from v13 — lane **A** the plant deck (`notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plant.html`, his run order) and lane **B** the plain deck (`notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html`, observation → response, no metaphor). The whiteboard image is saved at `notes/_lanes/296/breakdown-whiteboard-dave-2026-09-22.png`. Commit `1351175a`. Reports: `notes/_subreports/2026-09-22-296-A-deck-v14-plant.md`, `notes/_subreports/2026-09-22-296-B-deck-v14-plain.md`.

## 3

> may i ask why these are not in my repo and I have to download them?

> I thought we had resolved the playwright and chromium problem

> can we permanently fix this?

**Done:** the render environment got a BUILDER — `knowledge/_render/ensure_env.sh` (new), `seat_env.sh` defaulting to `outputs/_render-env`, and a ninth stratum in `knowledge/_RUNBOOK-render-verify.md`. Commit `cf97ccc4`. Cause: the two decks had been built in the cloud because `outputs/_render-env-229` had vanished from the mount. He then pasted back the rewritten Project instructions, with the render line added and *"Files written for Dave live in the repo beside their source; give him the path, not a download."*

## 4

> slide 4: There are 5 causes

> slide 5: I don't think this is quite right, the experiment is in the archive folder, it was more like, build from the 36 components, check's the work and output, but plese take a look, there is even a digram I think

**Done:** lane **B2** — slide 4 became five causes; slide 5 became the six-step loop rebuilt from `archive/apollo-pipeline-spec_v0.2_2026-06-20.html`. Report: `notes/_subreports/2026-09-22-296-B2-plain-five-causes-and-the-loop.md`.

## 5 — the rail

> I need an orientation pattern added. can I have a vertical timeline style progress indicator with circles indicating the chapters and smaller filled dots indicating any sub-pages. It should be persistent and not scroll with the slides movement, the possition indicator should grow to be a larger circle with the chapter number inside and the chapter title to the right all the other don't need the titles but I want to see them very tiny in the first version.

> I'm using a a large screen the collision wont happen. Can we have the line go all the way down the screen, and the items up to the top, the circles with the number have a line running through it, can we remove. Can we somehow have the current slide number in the same position by bunching the others up or something, there is more space to play with if we have the line span the entire height, and the circle and title bigger

> okay this is looking cool, lets keep the same spacing for items below that we have when we have the final slide so its all laid out and easy to see and remove the title from the chapters apart from the current one

> don't worry about the gap right now, its looking pretty good, we need a bit more space between the progress points, it's looking a bit congested and the rest of the deck is pretty minimal. Lets just remove it from slide 2, and I think the circle title was better smaller, maybe same size as the eyebrow text on the slides themselves

> okay one last thing for this, I'd really like anything other than the current chapter to be faded so that it looks less congested, lets use a much lighter grey on the white backgrounds and a darker on the dark, lets really make the everything other than the current chapter stand out

> there is a strange jump with the rail from slide 2 to 3 … after this is fixed can you add the same progress indicator to the plant deck too

**Done:** lane **C**, rail v1 → v6 on the plain deck, then the port to the plant deck. Report: `notes/_subreports/2026-09-22-296-C-plain-chapter-rail.md`. ⚠ The plant deck received the rail and the payoff line ONLY — none of the afternoon/evening plain rulings below were ported to it.

## 6 — the payoff line

> And the payoff is 'Automated product design you can bank on' triple pun, very cool even if I say so myself

> get it? its for a bank, you can use the products for banking and 'bank on' means relyable

**Done:** on the close slide of both decks (plain s12: "Apollo / Automated product design you can bank on.").

## 7

> Can you check the order of play chapter slide matches the tracker, they seem to be out of sync.

Followed by his fourteen-line eyebrow list, **as the brief carries it (abbreviated by the conductor)**: 2 'The order of play' · 3 'What we noticed' · 4 'Can we catch up' · 5 'What we tested' · 6 'What we saw' · 7 'The component library' · 8 'Speed, consistency, and quality' · 9 'The knowledge graph', remove Switch cue · 10 'Gates and evals' · 11 'Demo', remove Switch cue · 12 'The main constituents' · 13 'A smart design system' heading 'twelve types of content' · 14 strapline one line, Apollo bold as cover.

**Done:** applied to the plain deck at the conductor's seat (conductor renders `notes/_lanes/296/D*.png`); eyebrows and the order-of-play slide brought into step with the rail.

## 8

> Plain: lets just remove the ask from the index slide, its fine to keep in the rail. slide4: remove 'speed' and 'All · shared with consistency and quality' slide5: remove 'The agent never invents a part…' slide7: 'Switch to the library' remove. I want a new image for proficiency, maybe draughtsmen tools or desk or something, but we'll come back to that if I have time. there is a flash of white on the background of the images, either lave them white or if you can loose the white can I have a keyline around them

**Done:** the removals applied at the conductor's seat; the prints left WHITE with a keyline (the hidden-line white fills cannot be lost). ⬛ The proficiency image is **parked by him** — carried to #297.

## 9 — the map hub, slides 12, 13, 15

> replace all the content with just Apollo, in bold as usual and the strapline 'Smart design system' the 'coming soon' tags replace with 'In progress' slide 15: the eyebrow, replace 'in closing' with 'Smart design system'

> slide 12: replace 'Three things she is made of.' with 'The three main elements of Apollo' slide13: lets boost the size of the centre content a bit.

**Done:** applied to the plain deck at the conductor's seat.

## 10 — the cold brief

> we created a cold start prompt for apollo sider to test on my work machine can you surface it for me

> no thats the really basic one there is another somewhere

**Done:** surfaced `notes/_briefs/2026-09-08-258-cold-run-brief.md` — the FROZEN prompt, verbatim at that brief's lines 13–17 — and `notes/_lanes/288/GRILL-SOURCE-2026-09-18-hsbc-ceo-international-banking.md` (the work-machine grill brief). ⛔ **This STRIKES the `_HANDOFF-139…146` carry "the frozen demo prompt is NOT RECOVERABLE"** — receipt: that brief's lines 13–17 (`s183-D1` / `s188-D2` form; struck in `_CARRIES.md` § `residual → #297` and in `_HANDOFF-147`). ⬛ **He did NOT confirm which of the two is "the cold brief we will be doing the demo with"** — still unnamed, carried to #297.

## 11 — the boss's pass

> how hot are we I have some changes to make from my boss

Then his boss's changes, in his words:

> first thing let's combine observation with problem as one chapter called 'Problem'. ''Agile' was sluggish' 'Agile delivery was stuck in waterfall, including design. Coupled with long delivery cycles, we were meeting too few user needs and delivering them too late.

> Experiment chapter should be renamed 'Research'

> Research and results combined in one chapter just 'Research'. Change response to 'Evaluation' slide 2: 'what we noticed · can we catch up' to 'what we noticed' Slide 3:'So we asked: how do we speed up design?' - 'So we asked: how might we speed up design' slide 4: replace 'can we catch up' with 'what can we improve' replace 'Why is design slow? Five causes' with 'Why does design feel slow?'

> 'So we asked: how might we speed up design?' change to 'can we speed up design with the help of AI' move slide 4, it should be the intro to 'evaluation'

> slide 8: remove the bottom section

> slide6: 'Why does design feel slow?' to: w'e asked: what else is slowing us design?

(applied as "We asked: what else is slowing design?" — the conductor's reading of the typo, declared.)

> switch slide 8 and 9 retitle 'The knowledge graph joins it all together' 'The second: we started to build a knowledge that joined everything together'

(applied with "graph" inserted — declared.)

> Slide 4: 'Built from the 36 components available. the work checked automatically and by a human'

> switch 9 and 10

> the title for 'the build' on the index and the slide should be 'The result'

> move 12 and 13 to after 10

> remove '4,820 nodes · 8,648 edges' from the final slide

> change: 'The same graph rechecks the work' 'Third: the system checks and rechecks it's own work'

> Change 'It confirmed what we always knew — and a chance to solve three things at once' 'In truth it confirmed much of what we already new and gave us the opportunity to solve three things at once'

> do you think we could add another one of our 3d illustrations that has a representation of a knowledge graph the shells construction is probably best it can be a simplfied version, not the full thing, to replace the brain, then we can have another slide with the brain that talks about the designers brain idea after the gates and evals. please make sure the resting angle is the same as the others, the brain needs this correction too, I think we did it in the past but it's not there any more

> slide 13: eyebrow: The working system title: Let's build something

> can we have the callipers in a similar resting position too, and add a few more nodes to the KG illustration.

**Done:** the text changes by the conductor; the drawings by lane **E** — the SHELLS knowledge-graph drawing on s7 (17 → 26 nodes after his second ask), the brain moved to a slide of its own (s7b, "The designer's brain", words DRAFT, not his), the brain's constants brought to its drawing file (−50 / 20 / 33), the callipers' plate PSI −62 → −90 so it runs parallel to the books, gearbox and shells. ⚠ **Lane E rested the shells at the shared −35 / 20, not the brain's −50** — his "the same as the others" read against the brain's own #292 ruling; the brain's angle is carried to #297 as a question put. Commit `c358fc6b`. Report: `notes/_subreports/2026-09-22-296-E-shells-graph-and-the-brain-slide.md`.

## 12

> we must be hot now

> wrap

> opus 5.5 i hope

The wrap. FILL is **UNMEASURED** — `_checkin.py` found no transcript at the conductor's seat or at this one (`--preflight-line 296`: *"no top-level transcript matched `/sessions/*/mnt/.claude/projects/*/*.jsonl` at this seat"*). The conductor's ~185,000 in the brief's header is his own count, DECLARED; no figure is published as a measurement. The wrap ran on Opus 5.5 as he hoped.
