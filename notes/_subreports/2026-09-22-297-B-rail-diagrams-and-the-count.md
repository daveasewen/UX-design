# #297 lane B — the rail gets its own space and loses its dash; five diagram proposals, one at a time; the count on 07

provenance: 297 · 2026-09-22 (session date; work done Wed 2026-09-23 ~07:55–09:00 BST) · lane B (Opus 5.5, remote-device seat)
status: observed
tokens: UNMEASURED — this seat has no `message.usage` read

Dave's words are filed by addition at `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (step 0, as briefed), with the conductor's reading beneath them:
*"2. lets remove the m-dash from the titles to get a little more space and give it a rail."* · *"3. Okay let me see them separately first"* · *"5. Whats the problem with the sum?"*

## VERDICT

**DONE, three parts.**
1. **The rail (enacted).** The dash was the rail title's own drawn dash, not a character. It has gone from the rail title. The rail now owns a 200px column, and no slide's content enters it. Collisions: **1440×900 12 of 14 → 0** · **1920×1080 0 → 0**. At 1920, nothing but the rail title moved. At 1440 the content steps right of the rail. Two things there: 07's headline gains a line, and so does 08's.
2. **Five diagram proposals (not enacted).** One PNG per slide, "Now" on the left and "Proposed" on the right, with the changes listed underneath. A viewer shows them one at a time. The deck and its source carry none of it.
3. **The count (probe only, nothing changed).** The headline is right: 137 is the library's own component count, and it includes the 12 templates. The lead is what is wrong. It lists 8 foundations inside the breakdown of 137, and foundations sit outside that count, which is why the three figures add up to 145. Two corrected lines are below.

## 1 · The rail

**Where the dash was.** The rail's title is built by `notes/_lanes/296/C/build_c.py` (its STYLE block). The dash was `#chrail .cr-t::before`: a 24px, 1px accent line plus an 8px gap. It copied the slides' eyebrow pattern (`.label::before`). There is no em-dash character in the chapter names ('Problem', 'Research', 'Evaluation', 'The result', 'The ask'). Both `::before` rules are removed. **The eyebrow dash on the slides (`.label::before`) is untouched**, since he said "the titles" and the ruling reads it as the rail.
Result: the title starts at 72px instead of 104px. The widest title, "EVALUATION", now ends at 163px instead of 195px.

**The rail's own space.** Rules added to the same STYLE block, v7, commented in place:
- `:root{--rail-w:200px}`. This is the rail's right edge (163px) plus a 32px (`--s4`) gutter, rounded up.
- `.slide` left padding is at least `--rail-w`. The right padding matches `--rail-w` while the 1120 column can still centre, and gives way (never below 6vw) when it cannot. So **at 1920 the content does not move**, and at 1440 the 1120 column steps right to x=200 instead of shrinking. The headline type is unchanged.
- The drawing cards (`#s6 #s7 #s8 #s7b`, and `#s4 #s5` for parity) use the same rule on their 1360 grid.
- The map (`#s10map`) uses the same rule, keeping its own 72px minimum. Below 1520 wide its bottom padding becomes 72px. Without that, once the map stepped right, its bottom-right corner came 1px from the page number at 1440 (it was 26.6px before this change; now 25px).
- `#s1` keeps `padding:0` (its ID rule wins, and the rail is hidden there).

**The source HTML is unchanged.** Both the dash and the column live in the builder, because the rail does. Rebuilt with `python3 notes/_lanes/296/C/build_c.py`. The rebuild was proven idempotent against the committed deck before the edit (byte-identical). `build_e.py` was not run. The deck was not hand-edited.

**Collisions, by bounding box** (`notes/_lanes/297/B/rail_check.py`). This checks every visible rail element (the line, each circle and dot, the title's box) against every content element (text line boxes, img/canvas/svg, any painted box or pseudo-content), all 16 slides:

| viewport | before | after | smallest clearance after |
|---|---|---|---|
| 1440×900 | **12 of 14** visible-rail slides: 03 04 05 06 07 08 11 12 13 14 15 16 (09, 10 miss by 3.7 / 5.1px) | **0** | 37px (06–14), 47.9 (04, 05), 57.5 (03), 65.5 (15, 16) |
| 1920×1080 | 0 | **0** | 117px (07–10, was 85), 237px elsewhere (was 205) |

The rail is hidden on 01 and 02 (no collisions there either way). This matches R2's count (12 of 14 at 1440, none at 1920).

**Pixel diff at 1920×1080**, all 16 slides against the pre-change render (`notes/_lanes/297/A/cmp.py`):
- **01 and 02 are the same.**
- **03–16 changed only in the rail title band** (x 72–193, y 405–414, 419–658 px per slide), where the title moved left by the dash's 32px.
- There was anti-aliasing noise of at most 5 levels at one rail dot on 03 and 09.
- **No content pixel moved at 1920.**

**At 1440×900, what now looks different.** I looked at the after renders of 06, 07, 10, 11 and 13 in full, and 02, 04, 08 and 12 on a sheet:
- Standard slides: the content starts at x=200 (was 160) and is still 1120 wide. The right margin is 120.
- Drawing cards: the column is 1153.6 wide (was 1267), from x=200. **07's headline goes from 2 lines to 3** ("…went from 36 / to 137."). **08's goes from 3 to 4.** All other headline and body line counts are unchanged, measured on all 16. The drawings on 07–10 are drawn about 9% narrower.
- 13's map sits 25px clear of the page number.
- No clipped text and no overlap anywhere.
- The two extra headline lines are the only thing that reads worse, and only at 1440. At 1920 there is no change.

## 2 · The five diagrams, one at a time (proposals only)

- Viewer: `notes/_lanes/297/B/diagrams-one-at-a-time.html`. One pair per screen, Previous / Next and the arrow keys, the slide number and the change list beside it. Clicking the picture shows it at full size. It keeps its place in the URL (#04 … #13). Checked in Chromium at 1440 and at 390 wide (no sideways scroll), with no page errors.
- Pairs: `notes/_lanes/297/B/diagram-04.png`, `-06`, `-11`, `-12`, `-13`. Each is 3040px wide: Now | Proposed at 1440×900, plus the change list underneath.
- How they were made: `notes/_lanes/297/B/proposals/propose.py` writes a COPY, `proposals/deck-proposed.html` (the rebuilt deck plus ONE style and ONE script, `data-lane="297-B-proposal"`). It renders "now" from the deck itself and "proposed" from the copy. **The deck and its source carry no proposal CSS or JS.** Both renders include the Step-1 rail.

**The grammar used** is R1's (`notes/_subreports/2026-09-22-297-R1-art-director-diagrams.md`), pushed toward the drawings on 08 and 10. There is one deviation from R1: **the things (steps, cards, the map's frame) are outlined in the drawings' 1px ink #111**, not R1's #D7D8D6. In the render, grey keylines read as interface cards, while ink rectangles read as the drawings: the catalogue on 07 is ink rectangles with one red. The dividers, and the frames round pictures, stay #D7D8D6.
The other rules, all R1's:
- a dashed 5/4 line means "goes back" or "not yet";
- one solid 6×8 arrowhead, used for flow only;
- no filled bands, and no white type on colour;
- labels 12/500/caps/.14em;
- numbers in grey;
- one red idea per diagram, drawn as a line, never as a fill.

| slide | gist of the proposal |
|---|---|
| 04 the loop | The filled black, grey and red header bands go. The steps become white ink-hairline boxes numbered 01–06 in grey. Red marks the checking only: 04 and 05 outlined in red, and the way back from a failed gate as a red dashed hairline. The italic notes stand upright. |
| 06 five causes | An ink hairline over each column, still with no boxes. Numbers in grey. Titles 22 → 18 at one height, so all five descriptions start on one line. One 2px red rule over "Small component library", the cause tackled first, as a thread into 07. **This is a lane addition, not R1's, and Dave can refuse it on its own.** |
| 11 three problems | The chips become plain labels (Speed red, the others ink). The bus is one ink line. The cards are outlined in ink, Speed's in red. The repeated in-card labels go. "Shared by all three". The tick moves under "Small component library" and reads "Addressed first". |
| 12 three elements | The plates show 07's catalogue, 08's graph and 10's brain, cropped to their ink and drawn at ONE scale (0.40). A gamma is applied so the hairlines stay ink at that scale. The gearbox and the books appear nowhere else in the deck. Numbers grey, the invisible cell lines drawn in #D7D8D6, descriptions at 16. This is **R1's "change later"**, brought forward to be seen. |
| 13 the map | The twelve file paths go. The type comes up to the deck's sizes (grey 12 numbers, bold 16 sentence-case titles, 13 descriptions). "In progress" tiles become white with a grey dashed inset line instead of 45% type on grey. The outer frame is ink, the grid inside grey. The red rule under Apollo stays the only red. |

I looked at every PNG (and each proposed render at 1:1). Each proposal reads as the same hand as the drawings: ink hairlines, one red, dashes for not-yet or going back. It is not just a thinner version of today's. What is kept: the six-in-a-row plus the loop (04), open columns (06), the heads, bus and three cards (11), three plates (12), and the 4×4 frame, hub and inward ticks (13). What was not done: the copy changes R1's sketch carried (e.g. 13's "Every ruling inscribed with its receipt."), headline sizes, and 11's full-width "Shared" band.

## 3 · The count on 07 (probe only; the deck is unchanged)

**What 07 says:** "the catalogue went from 36 to 137. 125 components, 12 templates, 8 foundations — 101 new". Footnote: `showroom/index.json, read 2026-09-22`.

**What the file says** (`showroom/index.json`, generated 2026-09-09 by `knowledge/_render/gen_library_214.py`, #261):
- `$component_count` **137**. By level: element 76 + pattern 33 + block 9 + shell 7 = **125**, plus template **12**.
- `$foundation_count` **8**. These are flagged `foundation: true` and are separate: photography, logos, bento, bento rails and four grids.
- `$count` **145** = 137 + 8, i.e. every entry.
- It is current. The 138 `knowledge/components/*.meta.json` on disk are the 137 plus `EXAMPLE-button` (the schema example), matched case-insensitively.

**So:**
- 137 does **not** count foundations, and 125 + 12 = 137 exactly.
- "101 new" is 137 − 36, arithmetic, not a counted list of new entries.
- The lead's three figures sum to 145. **The headline is right. The lead is the sentence that is wrong**, because it puts the foundations inside a breakdown of 137.

**What 36 was.** It is Dave's own figure: "the original library had only 36 components" (`notes/_lanes/289/DAVE-RULINGS-2026-09-19.md:96`; his 04 line "Built from the 36 components available", `notes/_lanes/296/DAVE-RULINGS-2026-09-22.md:124`).
- It counted components only. At that time the index had no template or foundation levels. The index history starts on 2026-08-22 with 135 entries and no foundations; foundations were added from 2026-08-24.
- The record itself has 32 reviewed (2026-06-20), ~38 at the build-out proposal, and 40 gated canon (2026-07-21), as #289 lane H2 found (`notes/_subreports/2026-09-19-289-H2-library-buildout-story.md:10`). "36" is his recollection and is left as his word.
- So **36 → 137 is like for like**, components as the library counts them. 36 → 145 is not.

**Two corrected lines, for him to pick (neither applied):**
- **A (keep 137; recommended):** the headline stays "…the catalogue went from 36 to 137." The lead becomes: "125 components and 12 templates — 101 new — on 8 foundations, each one in code, built to our design and accessibility standards." Slide 12's "The library: 137 components in code." still agrees.
- **B (count everything, 145):** the headline becomes "…the catalogue went from 36 to 145." The lead becomes: "125 components, 12 templates, 8 foundations — 109 new — each one in code, built to our design and accessibility standards." This also needs slide 12 to change ("137 components" → "145 parts"). **Caveat:** it is not like for like, because the 36 counted no foundations.

## Deviations
- **The builder changed, not the source.** `notes/_lanes/296/C/build_c.py` carries both rail changes. `v14-plain-before-c.html` is byte-unchanged.
- **The map rule.** One more rule than "give the rail space" strictly needs: the `#s10map` bottom padding below 1520 wide. Without it, the change would have created a new near-touch on 13.
- **Ink containers.** The proposals outline their containers in ink, not R1's #D7D8D6 (the reason is given above). 06's red rule is the lane's own addition.
- **The date split.** Filenames keep the session date 2026-09-22. The rulings entry is dated 2026-09-23 07:52 BST.

## Files
- Changed: `notes/_lanes/296/C/build_c.py` · `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt) · `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (appended)
- New: `notes/_lanes/297/B/diagram-04.png`, `-06.png`, `-11.png`, `-12.png`, `-13.png` · `notes/_lanes/297/B/diagrams-one-at-a-time.html` · `notes/_lanes/297/B/rail_check.py` · `notes/_lanes/297/B/proposals/propose.py` · this report
- Working, not committed: `notes/_lanes/297/B/_work/` (before and after renders at both sizes, collision JSONs, the pre-edit deck and builder) · `notes/_lanes/297/B/proposals/` (`deck-proposed.html`, `_shots/`, `_compose/`)
