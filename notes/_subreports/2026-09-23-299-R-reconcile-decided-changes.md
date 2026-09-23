# #299 lane R — reconcile: which of his decided copy and diagram-style changes on the plain deck are not yet enacted

provenance: 299 · 2026-09-23
status: observed

lane: R (Opus 5.5, remote-device seat, READ-ONLY) · tokens: context ~209,000 at the report-writing turn — a hand sum (input + cache_creation + cache_read of the last message) over this sub's cloud transcript, not a `_checkin.py` reading

## VERDICT

**Almost everything he decided is in the deck.** 42 decided changes found · **40 ENACTED · 2 PARTLY · 0 NOT ENACTED**. Both gaps are copy, one line each, in the one source file. No decided diagram-style change is outstanding.

1. **06, cause 04's description lost "accessibility".** He asked for it at 08:38; lane C put it in; lane E's friction rewrite (answering his 09:15/09:18 notes) replaced the whole line and dropped it. "Pushed for time" is not said either.
2. **02, the order of play no longer matches the rail.** It lists "what she is made of" under The result, but slide 12 now sits in Evolution; Evolution's descriptor names only the library, the graph and the gates.

OPEN (not decided): 8 named items + 26 review suggestions he never answered.

## Premise checks

- **Source and deck agree.** `build_c.build()` run on the source into `/dev/shm/r299-deck.html`, then `cmp` against `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html`: **IDENTICAL** (523,318 bytes).
- **Working tree = HEAD** for all three files (sha1 of `git show HEAD:<path>` vs the file): source `be49fbc7668d` · deck `f2ea392e6e72` · `build_c.py` `f7176053b9c0`. HEAD `4c9b4040`.
- Only `git log` and `git show` were run — no `git status`, `diff`, `add`, `reset`. Nothing rendered. Nothing edited but this report. The `build_c` import ran with `sys.dont_write_bytecode` (the `__pycache__` in `notes/_lanes/296/C/` is dated 10:52, #298 lane B's).
- **Line numbers** are in the SOURCE `notes/_lanes/296/C/v14-plain-before-c.html` unless named; the deck carries the same text (byte-identical build).
- **Where his words are:** W296 = `notes/_lanes/296/DAVE-RULINGS-2026-09-22.md` · W297 = `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` · W298 = `notes/_lanes/298/DAVE-WORDS-AND-BOOT-FINDING-2026-09-23.md`. ⚠ W296 entries 2 and 7 are the #296 conductor's abbreviation of two long messages (that file says so at its line 10); quoted as that file carries them.

---

## 1 · PARTLY — the work still to do

### P1 · Slide 06 — cause 04's description · COPY · PARTLY

His words:
- W297:61 — "06: 'Lack of design standards....' to 'Lack of standards knowledge' and add accessibility etc in the description.."
- W297:112 — "one note on 04 on slide six, the standards are available, so they are written down. we need to succinctly say they are multiple sources and designers would rather"
- W297:116–117 — "...ask someone, they certainly don't want to read, and they are pushed for time, the problem isn't that they are not available the problem is that there are frictions. I don't what to call the designers lazy, but there is a bit of that too"

**In:** the title rename (`38be9376`) and the friction line (`f848330e`), source :508 — "Standards exist, but in too many places; asking someone is quicker than looking it up."
**Missing:** "accessibility". Lane C's line carried it ("Design, accessibility and content standards are not written down, so each decision is made again."). His 09:15 note corrected "not written down"; it did not withdraw accessibility. Lane E's rewrite dropped it. "Pushed for time" is only implied by "quicker".

**Edit** (source :508; the words are drafts for his pick, not his):
- old: `<p>Standards exist, but in too many places; asking someone is quicker than looking it&nbsp;up.</p>`
- new A (minimal — adds only what he asked): `<p>Design and accessibility standards exist, but in too many places; asking someone is quicker than looking it&nbsp;up.</p>`
- new B (tighter; carries "pushed for time"): `<p>Design and accessibility standards exist, but in many places; pushed for time, designers ask rather than&nbsp;read.</p>`
- ⚠ The current line is 87 characters and 4 lines at 1920 and 1440; its four siblings run 2–3. A is ~112 characters (likely 5 lines), B ~100. Render 06 at both sizes. The same cause on 11 is a name only (:600) — nothing to change there.

### P2 · Slide 02 — the order of play no longer matches the rail · COPY · PARTLY

His words:
- W296:72 — "Can you check the order of play chapter slide matches the tracker, they seem to be out of sync."
- W297:93 — "I want a new chapter called evolution after evaluation, that stars with slide 07"
- W298:35 — "the running order is fine, we just need to enact the changes I've decided, the only real change is the new chapter Evolution after Evaluation."

**In:** Evolution is on 02 (`999cba4a`, :447), and the rail runs Evolution 07–13 (`build_c.py:210`).
**Out of sync:**
- :448 reads The result — "demo · what she is made of". "What she is made of" is slide 12, which is in Evolution now; The result is 14 alone. And "she" came off 12 at his word — W296:88 "slide 12: replace 'Three things she is made of.' with 'The three main elements of Apollo'".
- :447 reads Evolution — "the library · the graph · the gates", for a chapter that also holds the brain (10), the three problems (11), the elements (12) and the map (13).

**Edit** (drafts — the rule is his, these words are not; they are the review's suggestion 20):
- :447 old `<em>the library &middot; the graph &middot; the gates</em>` → new `<em>the library &middot; the graph &middot; the gates &middot; the brain</em>`
- :448 old `<em>demo &middot; what she is made of</em>` → new `<em>the live demo</em>`
- ⚠ 02 is five near-equal columns (`minmax(max-content,1fr)`, about 192–218px each at 1440 per #297 lane D). A longer Evolution line may crowd it at 1440. Render 02 at both sizes.

*(No item is wholly NOT ENACTED.)*

---

## 2 · DECIDED AND ENACTED — receipts

Commits: `1351175a` (#296 two decks + the rail, lane C; the loop and five causes, lane B2) · `c358fc6b` (#296 boss's pass, eyebrows, removals, drawings — the #296 conductor's text changes went in here) · `57e885b0` `cde7107d` `38be9376` `999cba4a` `f848330e` `81541832` (#297) · `f54562e2` (#298).

| # | slide | type | his words (file:line) | where now | commit | status |
|---|---|---|---|---|---|---|
| 1 | 02 | COPY | W296:24 (abbreviated) "2 title wrong, *'what you'll see in the next 15-20 minutes'*" | :442 "What you'll see in the next 15–20 minutes." | 1351175a / c358fc6b | ENACTED |
| 2 | 02 | COPY | W296:80 "lets just remove the ask from the index slide, its fine to keep in the rail" | :444–448, no ask | c358fc6b | ENACTED |
| 3 | 02 | COPY | W296:110 "slide 2: 'what we noticed · can we catch up' to 'what we noticed'" | :444 | c358fc6b | ENACTED |
| 4 | chapters | COPY | W296:106 "let's combine observation with problem as one chapter called 'Problem'" · W296:108 "Experiment chapter should be renamed 'Research'" · W296:110 "Research and results combined in one chapter just 'Research'. Change response to 'Evaluation'" · W296:128 "the title for 'the build' on the index and the slide should be 'The result'" | 02 :444–448; rail `build_c.py:206–213` | c358fc6b | ENACTED |
| 5 | eyebrows | COPY | W296:74 his fourteen-line eyebrow list (abbreviated) | 02 :440 · 03 :457 · 04 :471 · 05 :492 · 07 :519 · 08 :538 · 09 :557 · 11 :589 · 12 :610 · 13 :641–642 "A smart design system" / "Twelve types of content." (its 04 and 11 lines superseded by rows 12 and 20) | c358fc6b | ENACTED |
| 6 | 03 | COPY | W296:106 "''Agile' was sluggish' 'Agile delivery was stuck in waterfall, including design. Coupled with long delivery cycles, we were meeting too few user needs and delivering them too late." | :458–459 | c358fc6b | ENACTED |
| 7 | 03 | COPY | W296:112 "'So we asked: how might we speed up design?' change to 'can we speed up design with the help of AI'" | :460 | c358fc6b | ENACTED |
| 8 | 04 | COPY | W296:124 "Slide 4: 'Built from the 36 components available. the work checked automatically and by a human'" | :472 | c358fc6b | ENACTED |
| 9 | 04 | COPY + DIAGRAM | W296:42 "it was more like, build from the 36 components, check's the work and output" | the loop :474–483 ("checks the work", "checks the output") | 1351175a | ENACTED |
| 10 | 05 | COPY | W296:80 "slide5: remove 'The agent never invents a part…'" | absent from the source | c358fc6b | ENACTED |
| 11 | 06 | COPY | W296:40 "slide 4: There are 5 causes" | :504–510 | 1351175a | ENACTED |
| 12 | 06 | COPY | W296:110 "slide 4: replace 'can we catch up' with 'what can we improve'" · W296:116 "slide6: 'Why does design feel slow?' to: w'e asked: what else is slowing us design?" | :502 "What can we improve" · :503 "We asked: what else is slowing design?" (typo reading declared at W296:118) | c358fc6b | ENACTED |
| 13 | 07 | COPY | W296:80 "slide7: 'Switch to the library' remove" (+ W296:74, the Switch cues on the graph and demo slides) | 0 hits for "Switch to" in the source | c358fc6b | ENACTED |
| 14 | 08 | COPY | W296:120 "switch slide 8 and 9 retitle 'The knowledge graph joins it all together' 'The second: we started to build a knowledge that joined everything together'" | :539 ("graph" inserted, declared W296:122) | c358fc6b | ENACTED |
| 15 | 09 | COPY | W296:134 "change: 'The same graph rechecks the work' 'Third: the system checks and rechecks it's own work'" | :558 ("its") | c358fc6b | ENACTED |
| 16 | 11 | COPY | W296:136 "Change 'It confirmed what we always knew — and a chance to solve three things at once' 'In truth it confirmed much of what we already new and gave us the opportunity to solve three things at once'" | :590 ("knew") | c358fc6b | ENACTED |
| 17 | 12 | COPY | W296:88 "slide 12: replace 'Three things she is made of.' with 'The three main elements of Apollo'" | :611 | c358fc6b | ENACTED |
| 18 | 13 | COPY | W296:86 "replace all the content with just Apollo, in bold as usual and the strapline 'Smart design system' the 'coming soon' tags replace with 'In progress'" | hub :756–758 · badges :660, :741 | c358fc6b | ENACTED |
| 19 | 13 | DIAGRAM-STYLE | W296:88 "slide13: lets boost the size of the centre content a bit." | at 1920 the hub's words keep #296's sizes (58 / 17). ⚠ At 1440 #297 lane D scales them to ~43 / 14 so the drawing fits (its declared deviation 1) | c358fc6b · 999cba4a | ENACTED (watch at 1440) |
| 20 | 14 | COPY | W296:140 "slide 13: eyebrow: The working system title: Let's build something" | :768–769 | c358fc6b | ENACTED |
| 21 | 16 | COPY | W296:64 "And the payoff is 'Automated product design you can bank on'" · W296:86 "slide 15: the eyebrow, replace 'in closing' with 'Smart design system'" · W296:132 "remove '4,820 nodes · 8,648 edges' from the final slide" · W296:74 "14 strapline one line, Apollo bold as cover" | :980–982; no count on 16; `white-space:nowrap` :8413; weight 600 :8414 | 1351175a / c358fc6b | ENACTED |
| 22 | rail | STYLE | W296:48–58 (v1–v6: circles and dots; full-height line; only the current title; more space; "remove it from slide 2"; "anything other than the current chapter to be faded") | `build_c.py` STYLE v1–v6 · `hideOn:['s1','s2']` :98 · fade :62–64 | 1351175a | ENACTED |
| 23 | 12 | DIAGRAM-STYLE | W296:80 "there is a flash of white on the background of the images, either lave them white or if you can loose the white can I have a keyline around them" | :8420 `.grid5 .pic` white + 1px keyline | c358fc6b | ENACTED |
| 24 | 08 · 09 · 10 | DIAGRAM-STYLE | W296:138 "…add another one of our 3d illustrations that has a representation of a knowledge graph … to replace the brain, then we can have another slide with the brain … please make sure the resting angle is the same as the others…" · W296:142 "can we have the callipers in a similar resting position too, and add a few more nodes to the KG illustration." | the shells graph on 08 (26 nodes); the brain on 10; the shared −35 / 20 (:1952, :2733, :3804, :5042, …); callipers PSI −90 | c358fc6b | ENACTED |
| 25 | 10 (+ 12's plate) | DIAGRAM-STYLE | W297:16 "1. okay do it" · W297:18 "3. the brain could be pivoted a little more to the words on this slide" · W298:32 "B" | :3404 `YAW0 = -27`, `PIT0 = 20` | 57e885b0 → f54562e2 | ENACTED |
| 26 | 10 | COPY (keep) | W297:17 "2. this copy is fine" | :575–577 unchanged | — | ENACTED (kept) |
| 27 | 06 · 13 | COPY | W297:19 "4. remove the notes" | 0 hits for "From the whiteboard" and "Placeholder: not yet ruled" | 57e885b0 | ENACTED |
| 28 | rail | STYLE | W297:41 "2. lets remove the m-dash from the titles to get a little more space and give it a rail." | `build_c.py:54` (dash gone) · :68–78 (`--rail-w:200px` column) | cde7107d | ENACTED — ⚠ read as the RAIL title's dash; the slides' eyebrow dash (`.label::before`) is untouched. If he meant the eyebrows, that is a different change. |
| 29 | 04 06 11 12 13 | DIAGRAM-STYLE | W297:42 "3. Okay let me see them separately first" → W297:57 "these are all good" | `<style data-lane="297-C">` :8422–8504 + script :8505; 04's boxes :8433; 12's plates are 07's catalogue, 08's graph, 10's brain (:8371); 13's paths hidden (:8492) | 38be9376 | ENACTED |
| 30 | 11 | DIAGRAM-STYLE | W297:57 "lets remove the red from three problems slide, on the box, on speed, and remove addressed first." | heads ink :8454; no "Addressed first" in the source | 38be9376 | ENACTED |
| 31 | 11 | DIAGRAM-STYLE | W297:58 "insert a new state triggered like the next slide advancement where everything we have tackled is highlighted" · W297:108 "I think we just make the text red on slide 11" | `data-steps="2"` :587 · state-2 red text :8480 | 38be9376 · f848330e | ENACTED |
| 32 | 11 | DIAGRAM-STYLE + COPY | W297:59 "Governance need an indicator that it it isn't solved but we have a proposal i.e. sign of the system not the outputs, or at least a fast-track." · W297:108 "and just add a reference mark to the governance text" | :598–599 dagger + "Proposal: sign off the system, not the outputs — or at least a fast-track." | f848330e | ENACTED |
| 33 | 11 | COPY | W297:58 "except lack of 'User data and research' - rename to this." | :601 "Lack of user data and research" | 38be9376 | ENACTED |
| 34 | 06 · 11 | COPY | W297:61 "'Lack of design standards....' to 'Lack of standards knowledge'" · W297:63 "'Governance process' to 'Manual, linear governance process'." · W297:65 "'Low/variable skills' to 'Highly variable design skills'" | 06 :505, :508, :509 · 11 :598, :600 | 38be9376 | ENACTED |
| 35 | 06 | COPY | see P1 | :508 | 38be9376 · f848330e | **PARTLY** |
| 36 | 13 | DIAGRAM-STYLE | W297:76 "can we have the KG graphic in the middle of the diagram from 08 on 13 in the middle;, try and keep the text and remove the tray for this one" | :755 `img#hubShl`; `<style data-lane="297-D">` :8569 | 999cba4a | ENACTED |
| 37 | 12 | COPY | W297:80–81 "Lets have the titles as / Components - Knowledge - Judgment" | :613–615 | 999cba4a | ENACTED |
| 38 | 12 | COPY | W297:83 "the description for Judgement will need different copy, I don't want to repeat the noun" · W298:26 "this is fine" | :615 "The brain: what to build, and how to compose it." | 999cba4a | ENACTED |
| 39 | 01 | COPY | W297:87–89 "cover slide, change the strap to: / A smart design engine powered by AI / on, brand, on standard, accessible, at speed" | :428 (stray comma after "on" dropped; no full stop, as typed) | 999cba4a | ENACTED |
| 40 | rail · 02 | COPY / STRUCTURE | W297:93 "I want a new chapter called evolution after evaluation, that stars with slide 07" · W298:35 | `build_c.py:206–213` · 02 :446–447 | 999cba4a | ENACTED |
| 41 | 07 | COPY | W297:44 "5. Whats the problem with the sum?" · W297:132 "okay lets get this executed" (read as yes) · W298:28 "do it" | :521 "125 components and 12 templates — 101 new — on 8 foundations, …" | 81541832 | ENACTED |
| 42 | 02 | COPY | see P2 | :447–448 | 999cba4a | **PARTLY** |

---

## 3 · OPEN — not decided

| # | what | his latest words (file:line) |
|---|---|---|
| O1 | **The ask, slide 15.** The red stamp "Draft — the ask slot is Dave's and is not ruled" (:966), the third-person line (:968) and the draft foot are still on it. Review 29. | W297:40 "1. were discussing this today" — nothing since (W298:30 is the conductor's note that no answer came). |
| O2 | **07 and 08 headlines at laptop size** (3 and 4 lines at 1440×900 since the rail took its column). | W298:27 "lets get the structure right and then we'll deal with polish". The structure is now settled (W298:35), so this may be next. |
| O3 | **His changes to the demo brief** (`notes/_lanes/288/GRILL-SOURCE-2026-09-18-hsbc-ceo-international-banking.md`); 14's lead :770 would follow it (review 31). | W297:20 "but we'll make changes to it" · W298:29 "we'll do that last" |
| O4 | **Judgment or judgement.** 12's title says "Judgment" (:615); 10's headline :576, 10's lead :577 and 12's foot :617 say "judgement". Flagged by #297 lane D; never put to him. | His message uses both: W297:81 "Judgment", W297:83 "Judgement". |
| O5 | **Lane E's alternative line for 06** — "The standards are written, but scattered — and pressed for time, designers ask rather than read." Never put to him. It lands wherever P1 lands. | none |
| O6 | **A new image for Proficiency.** Probably moot: 12's third plate is now the brain (row 29). | W296:80 "I want a new image for proficiency, maybe draughtsmen tools or desk or something, but we'll come back to that if I have time." |
| O7 | **The catalogue plate on 07 is off the shared angle** (PSI −5). Put at #296 (`notes/_subreports/2026-09-22-296-E-shells-graph-and-the-brain-slide.md:80`) and #297 (W297:6, item 3). | His answer to item 3 turned the brain, not the plate: W297:18 "3. the brain could be pivoted a little more to the words on this slide". Unruled. |
| O8 | **Moving 11 up after 06 (review 30) and the map to a backup (review 33).** Closed as not-now by his running-order words; listed so no lane moves slides. | W297:43 "I'm not opposed to this but they are very similar slides, the contents and messaging would have to change, otherwise we are just presenting two very similar content with no really differentiation, feels messy, also remember the story is we worked on speed but that work solved other problems that what slide 11 is about." · W298:35 "the running order is fine" |

**O9 — the review's suggestions he never answered** (`notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain-REVIEW.html`; his only words on it are W297:30, the ask for the review; only 1–5, 8, 17, 29 and 30 were put to him, W297:36). 26 of 37, by number:

- **Copy (14):** 18 the 07 and 08 footnotes read as a workbench (:522 "Source: showroom/index.json, read 2026-09-22. Growing." · :542 "4,820 nodes · 8,648 edges · explorer builder 1.27, 2026-09-19."; 13's paths are already hidden, row 29) · 19 jargon — 04 "a11y", "from canon only", "Kill the broken.", "Generate × N", "both on Opus"; 05 "agents"; 08 "rulings", "retrieved at build time"; 09 "Gates and evals" [his]; 13 "Every ruling inscribed with its receipt.", "Governed components, each with a meta and a build." · 20 02's descriptors (= P2) · 21 the cover eyebrow "Apollo · design-system engine" → "Smart design system" (his phrase) · 22 "catalogue" [his] vs "library" (its Proficiency half is done, row 37) · 23 "The first improvement: / The second: / Third: / Fourth:" [his] → "First: / Second: …" · 24 04 "The work checked…" [his] → "The work was checked…" · 25 11 "In truth it confirmed…" [his] → "In truth, the answers confirmed…" · 26 "2 stage process (Figma + Code library)" → "Two-stage process (Figma + code library)" (its "Low/variable" half is superseded, row 34) · 27 11's serial comma [his]; 12's "main" twice [his] · 28 14's foot "Live and unedited, with the recording as the fallback." off the slide · 31 14 names the brief (tied to O3) · 32 12's foot accounts for the gates · 34 one number ready for "how much faster?"
- **Type and style (6):** 9 hide the rail on the close (`build_c.py` `hideOn`, add `'s12'`) · 10 no one-word last lines in headlines · 11 three headline sizes, not five · 12 07's weights matched to 08–10 · 13 "Apollo" 132px on both cover and close · 37 hide "↓ / space to advance" on the cover
- **After Friday, by the review's own label (4):** 7 11's shared band · 14 one left edge · 15 one top line · 16 the typeface
- **On the day (2):** 35 the 15–20 minute promise · 36 rehearse once on the room's screen and carry a PDF
- **Already done by other means (8):** 1–5 (row 29) · 6 (row 29 — 12's plates are the three drawings) · 8 (row 28) · 17 (row 41). **29, 30, 33** are O1 and O8.

---

## 4 · In the deck but NOT his words — lane choices he has not named

- 02, Evaluation's descriptor "what else is slowing design" (#297 lane D, from 06's headline).
- 06, cause 04's whole line (#297 lane E's drafting of his 09:15 / 09:18 notes) — P1.
- 06, the 2px red rule over "Small component library" (#297 lane B's addition; inside his "these are all good").
- 11, "Shared by all three" (lane B, from the review).
- 11, the note's wording "Proposal: sign off the system, not the outputs — or at least a fast-track." (the conductor's reading of "sign of").
- 12, the foot "Components, knowledge and the judgement to compose from them." ("Parts" → "Components", lane D).
- 13, the hub's words scale down at 1440 (lane D) — row 19.

---

## 5 · PROPOSED LANES

**One lane.** Why:

1. **Both gaps are one-line copy edits in one file** — source :447–448 and :508. No diagram, CSS or builder change is outstanding.
2. **The deck is generated wholesale.** `build_c.py` rewrites the whole deck from that one source on every run. Two lanes editing it at once would race: each rebuild overwrites the other's, and each lane's pixel-diff baseline would be the other's half-done state.
3. **Both need his pick of words first** — P1's A or B, P2's two descriptors. Put them to him in plain words in chat; then ONE lane: edit the source → `python3 notes/_lanes/296/C/build_c.py` (never `build_e.py`) → render 02 and 06 at 1920×1080 and 1440×900 on the mount (the recipe in `_HANDOFF-149` § THE PLAIN DECK) → pixel-diff all 16 plus 11's second state → one commit through `knowledge/_git_commit.sh` with `SESSION_N=299`.
4. **If he rules on OPEN items in the same answer**, fold the copy ones into the SAME lane (same file). Review 9 (hide the rail on the close) is one word in `build_c.py` and can ride the same build. Anything larger — headline sizes, the laptop headlines, the ask's layout — goes to a second lane that starts only AFTER the first has committed. Serial, never parallel, for the race in 2.

---

## Receipts

- **Read:** W296 · W297 · W298 (in full) · `_HANDOFF-147` § HIS WORDS · `_HANDOFF-148` · `_HANDOFF-149` · `notes/_lanes/296/WRAP-BRIEF.md` (lines 20–60) · `notes/_lanes/298/WRAP-BRIEF.md` (grep) · `notes/_subreports/2026-09-22-297-{A,B,C,D,E,R,R3}-*.md` · the review page's text (python strip of script/style/svg/data URIs to `/tmp/review.txt` on the device, outside the repo; 349 lines, read whole) · `_CARRIES.md` § `residual → #299` (grep).
- **Not read in full:** #297 R1, R2, R4, W · #298 A, B, W · the #296 lane reports (grep only).
- **git:** `log --oneline -20` · `show --stat` of 999cba4a f848330e 81541832 f54562e2 38be9376 cde7107d 57e885b0 c358fc6b · `show HEAD:<path>` for the three blob hashes · `show 1351175a:<deck>` to confirm the strings the #296 removals took out.
- **Scratch outside the repo:** `/dev/shm/r299-deck.html` (the proof build) and `/tmp/review.txt`.
- **Deviations:** none from the brief.
