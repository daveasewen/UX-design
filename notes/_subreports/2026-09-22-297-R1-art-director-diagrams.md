# #297 lane R1 — art director: the diagrams on 04, 06, 11, 12, 13

provenance: 297 · 2026-09-22 · lane R (review conductor ran the R1 pass itself — no Agent tool at this seat)
status: observed — analysis and ideas only; the deck was not changed
deck: `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` at HEAD `57e885b0` (blob `c68c6640…`, identical to the working tree when measured)
renders read: `notes/_lanes/297/A/after/*.png` (1440×900 @2×, taken 21:10–21:11 BST after the deck's last write at 21:10:36)
measured: `notes/_lanes/297/R/_measure.json` (Playwright computed styles, 1440×900, 1680×1050, 1920×1080) · drawings' line specs read from the canvas source
sketches: `notes/_lanes/297/R/sketch/P*.png` — the proposals injected as CSS/DOM at render time only (deck blob unchanged after the run)

## Verdict

The five diagrams are drawn by three different hands. 06, 12 and 13 already sit close to the drawings on 07–10 (hairlines, white, square, quiet). **04 and 11 are the outliers**: filled black and red header bands, filled grey chips with white type, 1.5–3px rules, solid grey arrowheads. Aligning them is mostly subtraction.

## Inventory — measured at 1440×900 (CSS px)

| | 04 the loop | 06 five causes | 11 three problems | 12 three elements | 13 the map | 07–10 drawings |
|---|---|---|---|---|---|---|
| Line weight | box 1.5px (computes 1px at 1×, 1.5 at 2×); connector 1.5px; loop 2px dashed | none | bus 1.25px; card top rules **3px**; list dividers 1px | grid top 1px; cell dividers 1px; plate keyline 1px | grid gaps 1px; ticks 1×16px | **1px** ink; hidden 1px dashed 5/4; centre 1px dash-dot 9/3/2/3; red node 1.4px |
| Line colour | boxes #D7D8D6; connectors #545454; loop #DA1A00 | — | bus #9B9B9B; rules #DA1A00 / #333 / #767676; dividers #EDEDED | #D7D8D6 top; **#EDEDED on #F3F3F3 (1.03:1, invisible)** | #D7D8D6 gaps; ticks #000 (#9B9B9B on "in progress") | ink #111; hidden #BDBDBD; centre #9B9B9B |
| Arrows | solid triangle 7×10px #545454 (red into step 5); loop head 12×10 red | — | none (bus + drops) | — | stems, no heads | — |
| Containers | white, square; **filled header bands**: #EDEDED ×3, #000 ×2, #DA1A00 ×1 | none — open columns on white | white cards, no side keyline; **filled chips** #DA1A00 / #333 / #767676, white type | white plates in grey cells | white tiles; "in progress" #F3F3F3 + 45% opacity | white ground, plinth |
| Corners | 0 | — | 0 | 0 | 0 | — |
| Label type | 11.5 / 600 / caps / 1.15px | index 12 / 500 / 1.68px | chips 13 / 600 / caps / 1.3px; group labels 11 / 500 / caps / 1.54px | index 12 / 500 / 1.68px | index 9.5 / 400 / 1.33px #9B9B9B; badge 8.5 mono; paths 8.5 mono | gear tooth labels, mono, baked |
| Title | (band is the title) | 22 / 600 | — | 18 / 600 | 15 / **500**, Title Case | — |
| Body | 15.84 / 400 #333 | 16.56 / 400 #545454 | 15 / 400 #000 | 13 / 400 #545454 | 11.5 / 400 #333 | — |
| Numbering | "1 · Intake" inline | "01" own line, red | none | "01" own line, red | "01" own line, grey 9.5px | — |
| Red means | the human step, the two checks, the loop | numbering | Speed | numbering | the hub rule | **the one part to look at** |
| Ground | grey #F3F3F3 | white | grey | grey | grey | white |

**Where they disagree:** five stroke weights (1, 1.25, 1.5, 2, 3px) · five line colours · three arrow kinds · two diagrams with filled blocks, three without · red means four different things (step, speed, numbering, hub) · five label specs · three title sizes (22, 18, 15) · five body sizes (16.56, 15.84, 15, 13, 11.5) · three numbering formats.

**A slip found on the way:** 04's black and red boxes were meant to carry black/red borders (`#s5x .blk{border-color:var(--black)}`, `.red{…accent}`) but lose on specificity to `#s5x .steps li{border:1.5px solid var(--g3)}` (0,1,1,0 < 0,1,1,1). Computed border-top-color on steps 2, 4 and 5 is rgb(215,216,214). The black and red bands sit in grey boxes.

## One grammar — borrowed from the drawings

1. **Line.** 1px. Ink #111 for flow and connection; #D7D8D6 for containers and dividers. The only heavier line: a 2px top rule marking a group head.
2. **Dash.** Dashed 5/4 means "goes back" or "not yet" — the drawings' hidden line. The loop on 04; the in-progress tiles on 13.
3. **Arrow.** One head: solid, 6×8px, in the line's colour, only where something flows (04). Elsewhere stems without heads (11's drops, 13's ticks).
4. **Container.** White, square, 1px #D7D8D6 keyline. No filled bands, no white type on colour.
5. **Type.** Labels = the eyebrow spec (12 / 500 / caps / .14em). Numbers "01" in the label spec, #767676. Titles 18 / 600, sentence case. Body 16 / 400 #333, line-height 1.45. Notes 12 / 500 #767676.
6. **Red.** One red idea per diagram, marking the thing to look at — the job red does in every drawing (the red page, the red path, the red jaw line, the red fissure). Never numbering, never a fill.
7. **Ground.** Diagrams on grey with white containers; drawings on white. 06 has no containers and stays white.

## Per slide — keep / change

**04 the loop** — keep six boxes in one row, the loop underneath, the notes. Change: header bands → label over a 1px rule, "01 Intake" with the number grey; boxes 1px #D7D8D6; connectors 1px ink, 6×8 heads; red on the two checks only (2px red top rule on steps 04 and 05, their red notes) and the loop at 1.5px dashed 5/4; italic grey notes → roman. Body 15.84 → 16.
**11 the three problems** — keep three heads, the bus, three cards. Change: chips → labels (Speed in red, the others ink); bus 1.25px #9B9B9B → 1px ink; card rules 3px → 2px (ink; red for Speed); 1px keyline round each card; drop the in-card SPEED and QUALITY labels (the heads already say it); "All · shared by all three" → "Shared by all three"; the tick moves under "Small component library" and reads "Addressed first". List 15 → 16.
**13 the map** — keep the 4×4 frame, the hub, clockwise numbering, the inward ticks (they already are the grammar's stems). Change: delete the twelve file paths (8.5px monospace); index 9.5px #9B9B9B (2.85:1) → 12 / 500 #767676; titles 15/500 Title Case → 16/600 sentence case; descriptions 11.5 → 13; "in progress" → white tile with a dashed 5/4 inset keyline, full-strength type, the badge in the label spec (today 45% opacity ≈ 3:1).
**06 five causes** — keep five open columns, no boxes. Change: titles 22 → 18 and one title block height, so all five descriptions start on one line (titles wrap 2/3/2/4/1 lines today, descriptions start at four heights); a 1px #D7D8D6 rule over each column; numbers grey.
**12 three elements** — keep three plates, numbers, titles. Change now: numbers grey; cell dividers #EDEDED → #D7D8D6. Change later: plates show the three drawings the audience has just seen — catalogue (07), graph (08), brain (10) — at one scale. Today plate 01 (gearbox) and plate 02 (books) appear nowhere else, and the brain print (737×684) is contained at 0.317 against 0.517 for the 600×420 prints, i.e. drawn at 61% of the others' scale, with hairlines to match. The gearbox's tooth labels render ≈5px tall.
**Later, 11** — "Shared by all three" belongs under all three heads, as a full-width band, not in the column under Consistency (Consistency has no causes of its own, so it reads as "All").

## Sketches

- Rendered: `notes/_lanes/297/R/sketch/P04-s5x.png`, `P06-s4p.png`, `P11-s6b.png`, `P12-s10.png`, `P13-s10map.png` (1440×900 @2×; CSS/DOM injected at render time by `notes/_lanes/297/R/sketch_render.py`).
- Drawn: two SVG sketches (04 and 11, current vs proposed) and a grammar sheet live inline in the review HTML, labelled SKETCH.
