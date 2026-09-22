# #297 lane A — the plain deck carries Friday: the brain on the shared angle, two footnotes out, three pivot readings for Dave

provenance: 297 · 2026-09-22 · lane A (Opus 5.5, remote-device seat)
status: observed

Dave's words are filed at `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` (step 0, text as briefed):
*"plain"* · *"1. okay do it"* · *"2. this copy is fine"* · *"3. the brain could be pivoted a little more to the words on this slide"* · *"4. remove the notes"*.

## VERDICT

**DONE.** The plain deck is changed three ways, all as Dave ruled. The brain rests at the shared −35 / 20. The s7b words are unchanged. The two placeholder footnotes are out: the whiteboard line on slide 06 and the map's placeholder line. The catalogue plate is untouched. Across all 16 slides, pixel changes are confined to 06, 10, 12 and 13, and the DOM confirms only the two footnotes were removed. The three pivot readings are on one sheet for Dave to pick. The deck carries A until he does. **Two things to know:** the brief's "s6" for the whiteboard footnote pointed at the wrong slide, so I removed it from 06 / 16 (`s4p`), which matches Dave's words. And on slide 06 the chapter rail's title now overlaps the headline, which already happens on three other slides. I did not patch it.

COUNTS: findings 6 · ruling-shaped 2 · UNPROVEN 2

## WHAT LANDED

1. **The brain is on the shared angle.** In the source `notes/_lanes/296/C/v14-plain-before-c.html`, the brain's `YAW0` went from −50 to **−35**. `PIT0` stays at 20. Books, gearbox, shells and callipers all rest at −35 / 20, so the brain's plate now runs parallel to theirs: plate edges at **13.47° / 26.03°** on screen, down from 16.01° / 22.18° at −50 (the same projection formula lane E used).
   - **AOV 33 is kept.** It is the brain's plate overhang, a length that pads the housing box along the brain's front-to-back axis (`box(-HALF, HALF, AMIN-AOV+PADF, AMAX+AOV-PADF, …)`). It is not an angle, and none of the other drawings has a matching constant, so there was nothing to match it to.
   - **Where the angle lives:** in the source HTML, which is the only file `build_c.py` reads. The standalone drawing file `notes/_lanes/289/illustration/brain.html` is not pulled into the build, and I did not touch it.
   - **Slide 12 (s10, "The three main elements") follows automatically.** Its Proficiency cell copies the brain's baked print (`an3` ← `brPrint`), so it now shows the −35 pose too. That is by construction, not a defect.
2. **The s7b words are unchanged.** The deck has **no visible DRAFT marker** on s7b: the DOM shows zero `.draft` elements, and the slide text is word for word what it was before. So I changed nothing visible. ⚠ **Declared:** the s7b HTML *comment* in the source (not rendered) said "Headline and lead are DRAFT FOR DAVE'S WORDS" and "rest angle −50 / 20 / 33". I rewrote it to record the new angle and his "this copy is fine", so the next seat does not raise the words again. No visible text changed.
3. **Two footnotes are out**, each removed as one `<p class="foot">` element:
   - **Slide 6** (`s4p`, "We asked: what else is slowing design?", pagenum 06 / 16): *"From the whiteboard: Current problems → Speed, which runs into its own group and into All."*
   - **The map slide** (`s10map`, "Twelve types of content.", 13 / 16): *"Ten of the twelve stand in the repository today … Placeholder: not yet ruled."*
   - ⚠ **DEPARTURE FROM THE BRIEF, declared.** The brief put the whiteboard footnote on "s6, the library 36→137 slide". That slide is **07 / 16** on the deck's own counter, and its only footnote is a source line (*"Source: showroom/index.json, read 2026-09-22. Growing."*), not a whiteboard note. The only whiteboard footnote in the deck is on **06 / 16**, and its id is `s4p`. Dave was asked about "slide 6's whiteboard" footnote, and the handoff's OWED item 6 says the same, so I removed the s4p footnote. **s6's source line is untouched.**
   - The now-unused CSS rules `#s4p .foot` and `#s10map .foot` stay in place. They are dormant and harmless.
4. **The catalogue plate (PSI −5) is not touched.**
5. **The deck was rebuilt** with `notes/_lanes/296/C/build_c.py` and never hand-edited. `build_e.py` was not run.

## THE PREMISE PROBE (before any edit)

- I imported `build_c.build()` and ran it on the **unedited** source into `/dev/shm`. The output was **byte-identical** to the committed deck (500,375 bytes). The deck, the source and `build_c.py` on disk were each byte-identical to `HEAD` (4fe02e0e). There were no `.git/*.lock` files.
- After the edits, the source went from 487,976 to 488,139 characters and the rebuilt deck is 500,538 bytes. The deck's diff against HEAD is **15 changed lines**, all of them from the four source edits.

## PIXEL DIFF — all 16 slides, before vs after (1440×900 at 2×)

The render harness is `notes/_lanes/297/A/shoot.py`, with the pixel comparison in `cmp.py`. Both are working files and uncommitted. The harness blocks `pointermove` and `mousemove` at the window's capture phase, which is harness-only and stops headless Chromium's stray (0,0) event from swinging the drawings. It freezes the callipers with `calSetTime(0)`+`calStill()`, freezes the cover graph with `kgPause(true)`+`kgStill()`, and parks the brain and shells with `brSet(0,0)` / `shlSet(0,0)`. **Before trusting it, I shot the unedited deck twice: all 16 slides came out SAME.** Without those freezes, s1, s2 and s8 differed from one run to the next.

| slide | result |
|---|---|
| 01 s1 · 02 s2 · 03 s3 · 04 s5x · 05 s5r | SAME |
| **06 s4p** | DIFF (the footnote is gone and the block re-centres) |
| 07 s6 · 08 s7 · 09 s8 | SAME |
| **10 s7b** | DIFF (the brain at −35), bbox 1348–2594 × 326–1471 px, i.e. the drawing only |
| 11 s6b | SAME |
| **12 s10** | DIFF (the brain thumbnail only), bbox 1990–2382 × 622–983 px |
| **13 s10map** | DIFF (the footnote is gone and the map grows into the space) |
| 14 s9 · 15 s11 · 16 s12 | SAME |

**DOM check:** section order, pagenums (01/16 … 16/16) and heights (all 900) are unchanged. s4p lost exactly one `<p>` (27 → 26 elements) and s10map lost exactly one `<p>` (107 → 106). In both cases the only text removed is the footnote. Every other slide has the same element count, tags and text. There were 0 page errors and 0 console errors before and after. All three anatomy prints arrive.

**By eye** (the after PNGs, read at this seat): the s7b brain is fully in frame and nothing is clipped. s10map shows no gap, because its grid grows into the space. ⚠ **s4p: with the footnote gone, the slide's content re-centres ≈42 CSS px lower (read off the two renders), and the rail's current-chapter title "EVALUATION" now overlaps the headline's second line ("design?").** Before the change it sat just clear of it. **This is not new in kind.** The committed deck already has the same rail-title-over-headline collision on 07 s6, 08 s7 and 11 s6b (lane E noted s6 and s7). Removing the footnote adds 06 to that list. I **did not** patch it. A one-slide spacer would hide one instance of a rail-placement problem that also affects three other slides. That fix belongs to the rail (its `anchor` 0.38) and is Dave's call. Picture: `notes/_lanes/297/A/after/06-s4p.png`.

## THE THREE PIVOT READINGS — for Dave to pick; the deck carries A

Sheet: **`notes/_lanes/297/A/brain-pivot-readings.png`** (4512×1130). Full slides: `notes/_lanes/297/A/s7b-reading-A.png`, `-B.png`, `-C.png` (2880×1800 each).

**Which way is "toward the words":** the words are on the left. The brain's frontal pole points left and its back faces the viewer. Screen-x of the forward axis is −cos(yaw), so a **larger (less negative) YAW0** swings the front round toward the left and the words, and opens the brain into a truer side profile. The −50 → −35 change already turned it that way, and B and C carry on. A more negative YAW0 would turn it away from the words. This is confirmed by eye on the sheet.

| reading | the one constant (source, the brain's camera block) | extra yaw | brain's plate edges on screen |
|---|---|---|---|
| **A** (committed) | `var YAW0 = -35*Math.PI/180, PIT0 = 20*Math.PI/180;` | 0 | 13.47° / 26.03°, parallel to the others |
| **B** | `var YAW0 = -27*Math.PI/180, PIT0 = 20*Math.PI/180;` | **+8°** | 9.89° / 33.87° |
| **C** | `var YAW0 = -19*Math.PI/180, PIT0 = 20*Math.PI/180;` | **+16°** | 6.72° / 44.81° |

- **A pick is one constant.** Edit that one `YAW0` literal in `notes/_lanes/296/C/v14-plain-before-c.html` (the brain's line, just below the `#297 A` comment) and run `python3 notes/_lanes/296/C/build_c.py`. The comment above the line already names A / B / C.
- ⚠ **The trade-off Dave should see:** the brain's plate turns with the brain. **B and C take its plate off the shared parallel** that item 1 just set. B's plate edges (9.89° / 33.87°) match what the callipers had at PSI −62, the position lane E squared up at #296. Keeping the plate parallel while turning only the brain would need a new brain-only turn inside the plate frame (a PSI-like constant). That is not built.
- All three readings keep the brain fully in frame (the fit is re-derived from the orbit sweep at each YAW0). The orbit is ±25° yaw, so under the mouse C reaches +6°, just past pure profile.

## PATHS

Created: `notes/_lanes/297/DAVE-RULINGS-2026-09-22.md` · `notes/_lanes/297/A/brain-pivot-readings.png` · `notes/_lanes/297/A/s7b-reading-A.png` · `notes/_lanes/297/A/s7b-reading-B.png` · `notes/_lanes/297/A/s7b-reading-C.png` · this report.
Changed: `notes/_lanes/296/C/v14-plain-before-c.html` (the source) · `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt).
Working files, **not committed**: `notes/_lanes/297/A/before/` and `after/` (16 PNGs + `_facts.json` each) · `notes/_lanes/297/A/_work/` (the B/C variant sources, decks and renders) · `notes/_lanes/297/A/shoot.py`, `cmp.py`, `sheet.py` (the drivers, kept out so CI's help-gate population is not changed) · `notes/_lanes/297/A/v14-plain-before-c.pre-297A.html` (the source before this lane; HEAD holds it too) · `notes/_lanes/297/A/_railband-check.png`, `_s10-an3-before-after.png` (look-checks) · the msgfile.

## FINDINGS (each with its probe above)

1. The brief's "s6" for the whiteboard footnote pointed at the wrong slide. The only whiteboard footnote is on `s4p` (06 / 16). Probe: `grep -n 'class="foot'` over the source, plus the pagenums.
2. On s4p, the chapter rail's title now overlaps the headline, the same collision already on 07, 08 and 11. Probe: `after/06-s4p.png` against `before/06-s4p.png`.
3. Slide 12's brain thumbnail follows the brain by construction (`an3` ← `brPrint`). Probe: the pixel-diff bbox, plus `anatomyState()`.
4. s7b has no visible DRAFT marker. Probe: 0 `.draft` elements in the DOM facts.
5. Without freezes, the harness is not deterministic on s1, s2 and s8. It is SAME on all 16 slides once the callipers and the cover graph are frozen and the pointer events are blocked. Probe: two shots of the unedited deck.
6. Readings B and C take the brain's plate off the shared parallel: 9.89° / 33.87° and 6.72° / 44.81°. Probe: the projection formula lane E used.

## UNPROVEN / CLAIMED

- **UNPROVEN:** print (Cmd-P) was not rendered. The brain's baked print is the same frame as the canvas at rest, but I did not look at a printed page. Price: one print-to-PDF render.
- **UNPROVEN:** only 1440×900 was rendered. The rail-title overlap on 06 may read differently at other viewport heights, because the rail anchors at 0.38 of the height. Price: one render matrix.

## RULING-SHAPED QUESTIONS

1. The brain now sits at the same angle as the other drawings (A). Would you like it turned a little further toward the words: B (+8°) or C (+16°)? Either one takes its plate slightly off parallel with the others.
2. With the footnote gone from slide 6, the "Evaluation" chapter label on the left now runs into the headline, as it already does on slides 7, 8 and 11. Should the chapter label move, or should it be left as it is?

REPLAY-THESE: none — the stub carries everything.
