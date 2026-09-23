# #297 — the plain deck carries Friday, and his eye ruled it slide by slide

provenance: 297 · 2026-09-22
status: observed

*The why and how of session #297, written by the delegated wrap seat (Opus 5.5) on 2026-09-23 from the record: his words (`notes/_lanes/297/DAVE-RULINGS-2026-09-22.md`), the six lane reports (`notes/_subreports/2026-09-22-297-*.md`), the lane commits and the wrap brief (`notes/_lanes/297/WRAP-BRIEF.md`). Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #297. Handoff: `_HANDOFF-148-the-plain-deck-carries-friday-and-his-eye-ruled-it-slide-by-slide.md`. Nothing here was inscribed as a ruling: `_rulings.json` stays 638.*

---

## 1. Two chats, and why the second one exists

The first #297 chat opened on the evening of 2026-09-22 at a boot of 127,609 real tokens — over the `s295-D3` ceiling of 72,768 by more than half again. Dave switched the Claude Docs connector off (*"that boot is massive again, i've switched off the docs"*), changed the routing doc so every sub runs on Opus 5.5 (`22a6a6a8`), parked a thought about routing by effort, and closed the chat with *"fresh"* at ~186,000 before any deck work. That chat's addendum (`4fe02e0e`) also found why #296's gauge had been unreadable: the conductor now runs in the cloud workspace, and its transcript is there, outside the path `_checkin.py` searches on his computer.

The second chat opened at 21:49 BST. Its boot measured **127,600** — nine tokens from the first. **The Docs switch-off changed nothing**, and the reason is visible in the chat itself: the Claude Docs tools are present although his connector panel shows Claude Docs as *not connected*. They arrive by some route the panel does not control. What makes up the 127,600 is not measurable from any seat today, because the system prompt is not in the transcript.

## 2. His answers to #296's five (22:00 BST)

#296 had ended with five questions and a sixth that mattered most — which deck carries Friday. He answered in one message: *"plain"*, then *"1. okay do it · 2. this copy is fine · 3. the brain could be pivoted a little more to the words on this slide · 4. remove the notes · 5. it's the one we reconstructed from co-pilot : GRILL-SOURCE-2026-09-18-hsbc-ceo-international-banking. but we'll make changes to it"*.

Lane A enacted the first four (`57e885b0`): the brain went to the shared −35 / 20 resting angle, the s7b words stayed, the two placeholder footnotes came out. Item 3 was read as a further turn of the brain toward the slide's words, so lane A rendered three readings (`notes/_lanes/297/A/brain-pivot-readings.png`, the shared angle and two further pivots, −27 and −19) for him to pick. **He has not picked.** Lane A also pushed, and CI run `35785910901` read identical to the baseline.

Those answers close eight of `_HANDOFF-147`'s thirteen owed items; the wrap strikes them with receipts rather than deleting them.

## 3. The review, and why it was ideas only

He asked for *"a review on the plain version … don't enact just make me an html doc with your analysis and ideas"*, wearing the copy editor's, publisher's and art director's hats. Lane R had no Agent tool in its seat, so it ran the four hats as four passes in sequence (reports R1–R4) and a conductor pass over them: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain-REVIEW.html`, **37 numbered suggestions, 32 before Friday**. Its verdict: the story holds; the ask is a placeholder; the rail runs into the content at laptop width; the diagrams on 04, 06, 11, 12 and 13 are drawn in a heavier hand than the drawings.

The conductor put only the five that mattered most. His answers (07:52 BST on 09-23) set the rest of the morning: the ask is *"discussing this today"*; the rail gets a margin; the diagrams he would see *"separately first"*; moving 11 after 06 was declined on the story's own logic (*"the story is we worked on speed but that work solved other problems that what slide 11 is about"*); and *"Whats the problem with the sum?"*.

## 4. The sum on 07

The lead said *"125 components, 12 templates, 8 foundations — 101 new"* under a headline that said the catalogue went from 36 to 137. The three figures add to 145. Lane B read the library's own count (`showroom/index.json`): 137 is the components *including* the 12 templates; the 8 foundations sit outside it; 137 − 36 = 101. So the headline was right and the lead was wrong in how it listed the parts. Option A kept 137 and moved the foundations out of the list: *"125 components and 12 templates — 101 new — on 8 foundations, each one in code, …"*. It was not ruled until his *"okay lets get this executed"* at 09:53 — which the conductor read as a yes, and which the wrap seat enacted before the ritual (`81541832`). That is a reading of *"this"*, and the handoff asks him to confirm it.

## 5. Five lanes on his eye (09-23 morning)

Each lane edited only the deck's source and rebuilt the deck with `build_c.py`; none hand-edited the deck, none ran the stale `build_e.py`, and each proved its change with a pixel diff at 1920×1080 and a rail-collision check at 1920×1080 and 1440×900.

- **B** (`cde7107d`) — the dash he wanted gone was the rail title's own 24px red line, not a character. The rail now owns a 200px column; at 1440×900 collisions went from 12 slides to none. The cost is laptop-size headlines: 07 now wraps to three lines and 08 to four. It also drew the five diagram proposals as now-versus-proposed pairs and showed them one at a time.
- **C** (`38be9376`) — *"these are all good"*: the five diagrams went in; 11 lost its red and gained a second state on the next press, highlighting everything tackled except *"Lack of user data and research"*; three causes renamed identically on 06 and 11; governance marked as proposed, not solved.
- **D** (`999cba4a`) — the cover strap in two lines, *"A smart design engine powered by AI"* / *"on brand, on standard, accessible, at speed"*; a new chapter, Evolution, from 07 to 13; 12's titles Components · Knowledge · Judgment, with a new Judgment line that does not repeat its noun; 13's hub became 08's knowledge graph with no tray. The Components line also repeats its noun; an alternative was put to him and is unanswered.
- **E** (`f848330e`) — on 11's second state the tackled causes' text turns red and governance carries a † keyed to the proposal note; 06's standards line now says the standards exist but in too many places, and asking someone is quicker than looking — friction, not blame, as he asked (*"I don't what to call the designers lazy, but there is a bit of that too"*).

## 6. What went wrong, or stays wrong

- **Review pages still reach him as copies.** He asked at 09:07 why review pages come from the cloud and not his repo. The answer given — a `computer://` link to the file in his repo — did not open for him (*"can you surface the file"*, 09:50), and the files went as copies again. No mechanism exists yet.
- **The gauge cannot read the conductor.** Every FILL figure at #297 is a hand sum over the cloud transcript, not a `_checkin.py` run. The wrap seat re-read it the same way and the conductor's figures reproduced to the token.
- **`git status` stranded the index lock again**, in lane D — the hazard every handoff since #295 names.
- **The ask (slide 15) is still a draft**, two days before Friday.

## 7. The resolved state, and what is open

Resolved: the plain deck carries Friday; the brain's angle; the s7b words; the footnotes; the plant port (moot); the demo's brief (named); the rail; the diagrams; 11's second state and its red text; the renames; the cover; the Evolution chapter; 12's titles; 13's hub; 06's standards line; 07's count (on a reading).

Open, his: the ask · the brain's pivot pick · the Components and Judgment lines · the laptop-size headlines · the review's other 32 suggestions · his changes to the demo brief · confirming the 07 line · the catalogue plate · the proficiency image. Open, mechanical: review pages from his repo · `_checkin.py` and cloud transcripts · the boot's attribution · the `git status` lock. All in `_CARRIES.md` § `residual → #298`.
