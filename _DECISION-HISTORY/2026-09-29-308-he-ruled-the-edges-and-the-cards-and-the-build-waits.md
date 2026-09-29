# #308 — he ruled the edges, the drift and the cards, and the build waits

provenance: 308 · 2026-09-29
status: observed

*The why and the how of session #308 (Tue 2026-09-29, 08:34 BST to his "yea lets wrap" at 19:44). The what is in `_HANDOFF-159-he-ruled-the-edges-and-the-cards-and-the-build-waits.md` and in `_LIVE-STATE.md`'s ⏱ LATEST delta (spine entry); the rulings are `s308-D1`..`s308-D44` in `knowledge/_rulings.json` (ledger).*

## 1. The picture page, and the note that was the decision

`_HANDOFF-158` put his picture-page answers first. He had answered 15 of 16 at 08:05. One call was ticked "Keep it open" but carried a sentence, which the record's rule treats as the ruling itself: the conductor read it back and he pasted the read-back as his answer at 08:38 (*"threat this as a ruling"*). The tree's chosen mark stops being one rule for every theme and becomes a choice each theme makes. Lane I wrote the fifteen into the record without building anything, so each answer became a tracked row rather than a half-done change.

## 2. Why the edges came before the cards

His 08:43 ask for research into design-system ontologies was about the graph's edges, which had grown to 65 types with no single definition of any of them. Lane O's first answer said nothing worth adopting existed; his 08:48 challenge (*"there are many defined online ubuntu comes to mind too"*) sent it back, and the second round found Canonical's Design System Ontology. That changed three of the nine recommendations, and he re-ruled the whole set on v2 at 12:13. His note on item 7 moved a standing preference: plain Anglo-Saxon words are for product names, and in the register *"Lets do what is neatest"*. Lane E then built the four items that every later one rests on: one register, the ends check, one direction stored, and each type's shape. Building them surfaced five questions the record could not settle (carousel and cards, ten governed-by lines, the ruled-by lines, tab bar, alert and toast); he took all five at 17:07. The first of those, which contains which, turned into the cards-and-tiles question.

## 3. Rebuild, not patch

The old claim tables were red because a checker judged 2026-08 testimony against today's tree. The recommendation was dated notes on the nine rows. He chose to rebuild instead (*"Lets do this properly, I'd rather rebuild than patch"*), and asked for blocking. The conductor listed what blocking would cost and advised one clean advisory CI run first; he took the advice. Lane K's checker now judges each row at the commit that wrote it, and turned out faster than the one it replaced (14 s against 38 s at the seat).

## 4. The drift, diagnosed before it was fixed

His 14:44 *"lets look at the foundations drift after :)"* was answered with a diagnosis page rather than a regeneration. It showed that the committed pages were right about the colour and the generator was right about the logos. The colour reader had read only the first canon block per theme since #288. Fixing it made seven of eight pages regenerate byte-identical, and that proved the fix. The matrix selftest he asked to be blocking was held back, not forced: its two reds are a ruling question (is the #261 nav family a tile group?), and the build does not answer that.

## 5. Cards and tiles, named by him

The carousel question needed definitions, so lane O's third round looked for a standard nomenclature, found none, and proposed Canonical's line (a card is one of a set of like records; a tile is one bento cell holding one thing). He took all five calls, then questioned two words himself. "Holder" was one he *"wouldn't use"*, and he wondered whether "cell" should be reserved. At 19:01 he gave *"yes to both"*: "housing" and "cell" as the grid position only. Container types stay open as his.

## 6. The reds, and why each is now a line

Five reds reached CI and each was fixed within the session. None was a wrong change. Each was a real change that one instrument read differently at the seat and on CI: an anchor that matched ten lines, a regen fed by an uncommitted log line, a comment inside a hashed stylesheet, a generator outside the regen serial, and two checks slower than the survey's 60 s cap. Each is now a "cold seat should know" line in the handoff, because the next session will meet the same seams.

## Resolved, and still open

Resolved: the picture page (15 rulings), the edge definitions and items 1 to 4, the five edge questions, Common as the interface label, the default icons, the claim-table checker (blocking), the colour reader, the logos page, cards and tiles as rulings, "housing" and "cell". Still open: the cards-and-tiles build, container types, edge register items 5 to 9, the matrix selftest's two reds, the twelve picture-page work rows, and everything `_HANDOFF-158` left standing.
