# 2026-09-22 · #296 · Lane B2 — PLAIN deck: five causes (s4p) and the experiment loop (s5x)

## VERDICT
Both rulings applied in place to `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (471,651 → 475,614 B). 0 page errors, 0 console errors, 0 overflowing cards; checked by eye (s2, s4p, s5x, s5r). The diff from the saved copy is five hunks, all inside s4p, s5x and their scoped `#s4p`/`#s5x` rules in the `data-lane="296-B"` style block (and its print line). Everything else is byte-identical: scripts, inlined assets, brain constants, other slides, footers. s2 is untouched ("agentic loops" still fits the loop, so I left it).

## WHAT CHANGED
**s4p, Ruling 1.** Headline "Why is design slow? **Five causes.**" Five cells in one row, **grouped 2 + 3**, the way the whiteboard's Speed arrow splits: a red-ruled "SPEED" band over 01–02 and a black-ruled "ALL · SHARED WITH CONSISTENCY AND QUALITY" band over 03–05. The cells follow the grid4 idiom (red index, bold h3, grey sentence). Foot: "From the whiteboard: Current problems → Speed, which runs into its own group and into All."

**s5x, Ruling 2.** The v0.2 spec diagram rebuilt slide-native in HTML/CSS (no image, no spec styles). Six boxes in a row, 1 Intake → 2 Criteria contract → 3 Generate × N → 4 Objective gates → 5 Taste + test → 6 Prototype, joined by arrows. The fill logic is copied from the spec: 2 and 4 black, 5 accent red, the rest grey. The regenerate loop is a red dashed line from under step 4 back up into step 3, with an arrowhead, labelled "fail a gate → regenerate". Measured: the loop ends sit exactly on the centres of columns 3 and 4 (624.5 / 815.5 px). Headline "Built only from the 36 components. **Then the work, and the output, checked.**" Lead "The agent never invents a part. Anything missing is raised as a gap — never improvised." Step 4 is tagged "checks the work" and step 5 "checks the output", which ties the loop to Dave's gist. Footer kept verbatim.

Builder (idempotent; rebuilds from the saved copy): `notes/_lanes/296/B2/build_b2.py`. Driver: `notes/_lanes/296/B2/shoot.py`.

## VERBATIM vs PARAPHRASE
| Text | Source | Status |
|---|---|---|
| Governance process · 2 stage process (Figma + Code library) · Small component library · Lack of design standards and accessibility knowledge · Low/variable skills | whiteboard | verbatim |
| "Speed", "All" group names | whiteboard | verbatim; "· shared with consistency and quality" is lane gloss |
| "It is a queue. Every component waits its turn for review." / "Every component is designed twice: once in Figma, once in code." | lane B | kept as-is |
| 03 "Too few parts, so designers draw the rest from scratch." | — | **B2 paraphrase** |
| 04 "With no written rules, each decision is made again, and accessibility is fixed late." | — | **B2 paraphrase** |
| 05 "How good and how fast the work is depends on who picks it up." | — | **B2 paraphrase** |
| "Why is design slow? Five causes." | Dave's ruling | in his sense |
| Step names 1 · Intake … 6 · Prototype, "Generate × N", "from canon only", "→ the gates", "Kill the broken", "Contrast · a11y · tokens · states", "Human + users … the winner", "handoff spec", "fail gate → regenerate" | spec v0.2 diagram | verbatim or near-verbatim ("fail a gate", "pick" lower-case) |
| Step bodies 1, 2, 3, 6 ("The brief, its jobs and assumptions." / "Success and failure written as executable checks." / "N variants, built from the 36 components only." / "Tuned, with a handoff spec.") | spec v0.2 diagram | condensed paraphrase |
| Lead "never invents a part … raised as a gap — never improvised" | spec v0.1 ("never invents components or variants"; "raised as open_gaps — never improvised") | paraphrase, last words verbatim |
| Headline "Built only from the 36 components. Then the work, and the output, checked." | Dave's ruling + spec v0.1 "built only from the component library" | paraphrase |
| "checks the work" / "checks the output" tags | Dave's ruling | **B2 mapping** (gates = work, taste + test = output) |
| Footer "June–July 2026: one brief, two arms …" | v13/v14 | verbatim |

## RENDER RECEIPTS
Seat render (ensure_env OK, seat_env OK), 1440×900 @2x, 2.5 s waits. Errors: new file 0, before-copy 0. Slide heights 900/900. Overflow probe on the five cells, their h3s, the six steps and their paragraphs: none. All six steps are 171 px tall. Pagenums 02, 04, 05, 06 / 15.
PNGs in `notes/_lanes/296/B2/`: `s2.png`, `s4p.png`, `s5x.png`, `s5r.png`, `before-s4p.png`, `before-s5x.png`, `before-after-s4p.png`, `before-after-s5x.png`, `measured.json`. Before copy: `v14-plain-before-b2.html`.
Checked by eye: no clipped descenders; cell 04 (four-line h3) fits; loop arrow legible. On the first render the step headers were uneven and the loop line was hidden under its label. I fixed both and re-rendered.

## UNPROVEN
- "36" is Dave's number (it matches s6 "from 36 to 137"). Neither spec file states 36.
- The v0.2 spec is a *design* of the loop. I have not checked that the June–July two-arm runs executed every one of the six steps, in particular 2 (criteria contract) and 5 (human + users).
- The three new cause sentences are my reading, not Dave's.
- Fonts fall back from Univers Next at the seat.

## QUESTIONS FOR DAVE
1. Are the three new sentences under Small component library, Lack of design standards… and Low/variable skills said the way you would say them?
2. Slide 5: did the experiment run all six steps (including the criteria contract and the human + users pick), or should the slide show only 3 → 4 → regenerate?
3. The agenda (slide 2) still calls chapter 4 "agentic loops". Keep it, or change it to something like "built from 36 parts"?
