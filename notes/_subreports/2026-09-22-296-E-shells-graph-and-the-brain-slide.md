# #296 lane E — the shells graph on the graph slide, and the brain on a slide of its own

Dave, verbatim: *"do you think we could add another one of our 3d illustrations that has a representation of a knowledge graph the shells construction is probably best it can be a simplfied version, not the full thing, to replace the brain, then we can have another slide with the brain that talks about the designers brain idea after the gates and evals."* / *"please make sure the resting angle is the same as the others, the brain needs this correction too, I think we did it in the past but it's not there any more"*

## WHAT LANDED

- **s7 (the knowledge graph)**: the brain is out of the drawing slot. A new drawing is in: **three nested shells** (the core, the middle and the outer layer, as in Dave's shells model of the explorer's three layers, `graph-layers-are-shells-280`). Each shell has its outline, its equator and one meridian. There are **17 nodes** (4 on the core, 6 on the middle, 7 on the outer) and **17 edges**. One chain (core to middle to outer) and its end node are in the accent red. It sits on a square plate with the books' construction cross and a vertical dash-dot axis. Every ring, edge and node that falls behind the picture plane through the centre is drawn in the deck's hidden grey dash (`#BDBDBD`, `[5,4]`), which is the same convention the books and the gearbox use. The ink is `#111` at 1 px and the red is `#DA1A00` at 1.4 px, the same as the others. The drawing animates to the mouse like the others (YAW_R 25 / PIT_R 12 / TAU 1.0), and a print is baked to `#shlPrint` at 1.2 s. It is a new IIFE modelled on the brain's scaffold (canvas `#shl`).
- **s7b (new, "The designer's brain")**: a light slide in the Evaluation chapter. It comes after gates and evals (s8) and before the breakdown (s6b). The brain canvas and print moved here unchanged, except that its rest angle is now corrected. Its animation observer now watches `s7b`. It inherits every CSS rule `#s7` has, including print.
- **The brain's correction**: the deck's copy had three constants three passes behind the drawing file. The drawing file is `notes/_lanes/289/illustration/brain.html` (pass nine, #292 B3, L474, and pass eight, L374). The copy now carries its values: **YAW0 10 → −50, PIT0 8 → 20, AOV 12 → 33**. Nothing else in the brain changed. Slide 12 (the constituents slide, previously s10) picks this up automatically, because its Proficiency cell pulls `brPrint`.
- **Pagenums** are now `NN / 16` by DOM order. The rail's Evaluation subs are `s6 s7 s8 s7b s6b s10 s10map`, set in `notes/_lanes/296/C/build_c.py`.
- **Edit path, as briefed**: the edits are in the SOURCE `notes/_lanes/296/C/v14-plain-before-c.html`, made by `notes/_lanes/296/E/build_e.py`. That script is idempotent and rebuilds from `notes/_lanes/296/E/v14-plain-before-e.html`, which is the pre-E source saved first. `build_c.py` was then run to generate the deck. The generated deck was never hand-edited. The shells IIFE lives on its own at `notes/_lanes/296/E/shells-iife.js`. The pre-E builder was saved as `notes/_lanes/296/E/build_c-before-e.py`.

## ⚠ ONE DEPARTURE FROM THE BRIEF — the shells rest at −35 / 20, not −50 / 20 / 33

The brief asked for the shells at −50 / 20 / 33 **and** for their plate to run parallel to the books' and the gearbox's plates. Both cannot be true. The books and the gearbox, like 7 of the deck's 8 drawings, rest at **−35 / 20**. Only the brain rests at −50, and that was Dave's own ruling on the brain alone (B3: *"this is the right angle"*). A plate at −50 does not run parallel to a plate at −35. AOV is the brain's own plate-overhang constant and means nothing for a sphere. I followed Dave's words ("the same as the others") and the brief's parallel test, so the shells use −35 / 20 with the books' camera code verbatim. Switching to −50 means changing one constant in `shells-iife.js` and re-running the two builders.

## RECEIPTS (`notes/_lanes/296/E/measured.json`)

| | YAW0 | PIT0 | plate | plate edges on screen (a-edge / u-edge) |
|---|---|---|---|---|
| gearbox (deck `gb`) | −35 | 20 | 404×172×14 | 13.47° / 26.03° off horizontal |
| books (deck `bk`) | −35 | 20 | ≈318×266×11 | 13.47° / 26.03° |
| **shells (new)** | **−35** | **20** | 320×320×12 | **13.47° / 26.03° — parallel** |
| brain (corrected) | **−50** | **20** (AOV **33**) | 366×156×12 | 22.18° / 16.01° — Dave's B3 ruling, not parallel |

These angles come from the shared projection, `atan2(sin(pit)·sin(yaw), cos(yaw))`. The `YAW0` / `PIT0` literals were read back from the built source: nine drawings, eight at −35/20 and the brain at −50/20. I checked them by eye in `drawings-four-up.png` (shells, brain, books, gearbox, all as baked prints). The shells, books and gearbox plates run parallel. The brain's plate is steeper.

- Shells: `shlState()` reports 17 nodes, 17 edges, 2 red edges, 1 red node, 6 rings and 3 outlines. At rest, 10 nodes are in front and 7 behind. No red segment falls on the hidden side. Canvas 737×684 at 1440×900, SC 1.39. The ink box sits inside the canvas, with no clipping.
- Errors: **0** page errors and **0** console errors across the whole deck.
- **All 16 sections are 900 px high.** Pagenums run 01/16 … 16/16 in DOM order `s1 s2 s3 s5x s5r s4p s6 s7 s8 s7b s6b s10 s10map s9 s11 s12`.
- `anatomyState()`: an1 = gbPrint (900×630), an2 = bkPrint (1200×840), an3 = brPrint (1474×1368, now from the s7b slot). All three arrive. Slide 12's brain shows the −50/20 pose with the plate behind the back of the brain.
- PNGs are in `notes/_lanes/296/E/`: `s6 s7 s8 s7b s6b s10 .png` (1440×900 at 2×), `contact-s6-s6b.png`, `shells-print.png` and `brain-print.png` (the two drawings as baked at 2×), `books-print.png`, `gearbox-print.png`, `drawings-four-up.png`. Driver: `notes/_lanes/296/E/shoot.py`.

## VERBATIM vs DRAFT

- Verbatim / structural: the eyebrow "The designer's brain" (from the brief), the placement, the drawing, and the angle.
- **DRAFT FOR DAVE'S WORDS**, headline: "Fourth: **a designer's judgement, built into the system.**"
- **DRAFT FOR DAVE'S WORDS**, lead: "The parts and the knowledge are not enough on their own — the brain is the judgement to compose from them, the way an experienced designer would."
- There is no footer figure, as briefed.

## UNPROVEN / NOTICED

- **The render harness can drift the drawings.** Headless Chromium fires a pointermove at (0,0) after a scroll, so any drawing on screen swings to its orbit limit (yaw −25, pitch +12). One early shot of s7b showed this. The final shots park the view with `brSet(0,0)` and `shlSet(0,0)` and centre the mouse. On the real screen, the drawings follow Dave's mouse as they always have. I did not test print (Cmd-P). The CSS for print mirrors #s7's rules.
- The shells are not a data view. They are an illustration of the three layers, with no link to the real graph's counts.
- On the shells drawing, two outer nodes sit close to the plate's back corner. This is minor, and I left it for Dave's eye.
- **Pre-existing, not from this lane**: the chapter rail's current-chapter title ("EVALUATION") overlaps the headline's first line on s6 and s7. The overlap is visible in `s7.png`.
- Housekeeping: `notes/_lanes/296/E/_dbg-*.png` are debug frames. The sandbox refused `rm`, so they can be deleted.

## QUESTIONS FOR DAVE

1. The graph slide now shows three nested shells with a small graph threaded through them, and one red path running from the core out to the edge. Does it read as the knowledge graph to you?
2. The shells sit at the same angle as the books and the gears, and all three plates run parallel. The brain sits at the angle you picked for it last time, which is turned a little further. Should the brain's plate also line up with the others?
3. The new brain slide's headline and line are my placeholders: "Fourth: a designer's judgement, built into the system." What would you like it to say?

## § e2 — the callipers' resting position, and more nodes on the shells

Dave, verbatim: *"can we have the callipers in a similar resting position too, and add a few more nodes to the KG illustration."*

Edit path: I edited the CURRENT source `notes/_lanes/296/C/v14-plain-before-c.html` in place. It already had the conductor's s9 change ("The working system" / "Let's build something."), which is still in the built deck. Before editing I saved it as `notes/_lanes/296/E/v14-plain-before-e2.html`. Then I ran `build_c.py`. I did not re-run `build_e.py`, which now builds from a stale source (see the note below).

**1 · The callipers were the odd one out, though not by their camera.** Their camera constants already matched the others: YAW0 −35 / PIT0 20 / YAW_R 25 / PIT_R 12 / TAU 1.0, with the same `setView`. The difference is that the whole instrument and its plate are built in a frame turned **PSI = −62°** about the vertical. That put the plate's edges at **9.89° / 33.87°** on screen, against the books' and the gearbox's **13.47° / 26.03°**.
- Change: **PSI −62 → −90**. This is a quarter turn, the nearest square angle, and it lands the plate edges exactly on **13.47° / 26.03°**, parallel to the books, gearbox and shells. I checked this in `e2-four-up.png`.
- Why −90 and not 0: the callipers' header derives a monotone-depth window. It needs Fc.x depth < 0 and Fc.y depth > 0 over the whole orbit (yaw −60..−10, pitch 8..32), and that holds for PSI of roughly −100..−60. −90 is inside it, so the painter's order stays exact. 0 or 180 would fall outside it and break the occlusion. The jaws still swing toward the camera and the graduated face is still up (`e2-s8.png`).
- A comment block above the constant records this, and the header line now reads "PSI = −90 deg (#296 E2; was −62)". The camera constants are untouched.
- Noticed and not touched: the catalogue on s6 has the same construction at **PSI −5°**, which puts its plate at **11.17° / 30.64°**. That is close to parallel but not exact. Squaring it to 0 is a one-constant change if Dave wants it.

**2 · The shells: 17 → 26 nodes, 17 → 26 edges.**
- The core, middle and outer shells now have **5 / 9 / 12** nodes.
- The 26 edges are: 2 within the core, 8 from the core to the middle, 4 within the middle, and 12 from the middle to the outer shell.
- There is still **one red chain**, core → middle → outer, made of 2 red edges and the 1 red end node. None of it is hidden.
- The rule for the back half is unchanged: whatever lies behind the centre plane is drawn in the hidden grey dash.
- At rest, **16 nodes are in front and 10 behind**. That is 62 / 38, against 59 / 41 before.
- The nodes that sat on the plate's back corner were moved: middle [−40, 100] → [−20, 110] and outer [−12, 70] → [−4, 78]. Two others were moved round the back to keep the front/behind balance.
- `notes/_lanes/296/E/shells-iife.js` carries the same geometry.

**Receipts** (`notes/_lanes/296/E/e2-measured.json`): **0 errors**. **All 16 sections are 900 px** high, with pagenums 01/16 … 16/16. The constituents slide pulls all three prints. Renders are `e2-s7.png`, `e2-s8.png` and `e2-four-up.png` (shells · brain · books · callipers, the baked prints), plus the individual prints `e2-shlPrint.png`, `e2-brPrint.png`, `e2-bkPrint.png` and `e2-cpPrint.png`. The driver is `notes/_lanes/296/E/shoot_e2.py`.

**Note:** `notes/_lanes/296/E/build_e.py` now builds from a stale source. Do not re-run it, because it would drop the conductor's s9 change and all of e2.

**Question for Dave:** the catalogue drawing on the component-library slide is also turned slightly off the others (5°). Should it be squared up too?
