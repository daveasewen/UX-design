# #303 lane P: "the press", the looping line drawing for slide 16 (s12)

Phase 1 only: a standalone prototype. The source and the generated deck were not touched.

## What was built
- **Prototype:** `notes/_lanes/303/P/press.html`. This is slide s12 at 1440×900: a dark ground, with the s12 text (label "Smart design system", h1 "Apollo", the close-line) in a `.type` column on the left and the canvas `#pr` in a `.draw` column on the right. It uses the same 38fr/58fr grid, gap and draw height as s4–s8.
- **The drawing:** hairline ink on black, with no fills except the ground. It has the callipers' wire-box tray and one stack of sheets standing in a slot cut in the tray top. A web page (16:10, a thin slab) is made on a stand floating over the front of the stack, tilted back 64° like the catalogue's book, so it reads face-on. When it has been checked, it lies down about its bottom edge onto the stack.
- **The page parts:** each one drops in along the page normal and snaps into place with a slight overshoot and a quick fade-in. In order: a header bar (logo square and three nav rules), four KPI tiles (a figure and a caption rule each), a chart (axes and one line) and a table (a column rule and six row rules). Part outlines are ink `#EDEDED`. The detail inside them is grey `#9B9B9B`, so the layout reads first.
- **The check:** one red rule, `--accent-dark` `#F6604C` (the two-red law: the dark-card red), 1.8 px, sweeps the finished page from top to bottom once. It is the only red in the drawing.
- **The stack:** sheets sit slightly askew (a deterministic jitter per sheet: ±1.2 across, ±1 deep, ±0.35°). The jitter fades out as a sheet goes down, so the press squares them up. The top sheet shows the previous page's parts.
- **The press:** after each landing the whole stack sinks one sheet into the tray. It stands 8 high just after a landing and 7 before the next. The part of the stack inside the tray is a hidden run, dashed in the hidden grey `#545454` (its near uprights and near floor edges). The sheet at the bottom passes into the slot and out of the drawing.
- **Hidden lines:** the callipers' method is lifted nearly verbatim (convex boxes, back-face test, painter's order with a ground fill, silhouette and hard-crease ink, and the tray and slot edges classified in 3D by view-ray slab clip, with buried runs dashed `[5,4]`).
- **Sway:** the callipers' cursor-follow is ported verbatim (±25° yaw, ±12° pitch, critically damped, tau 1.0 s, stays where the mouse leaves it). It draws at 30 fps only while `#s12` is in view (IntersectionObserver). Under reduced motion it shows one still frame, t = 4.2 (the page made, before the check).
- **Print:** `#prPrint` is baked from that 4.2 still, following the same `snap()` pattern as `cpPrint`.
- **Controls (prototype only):** `?t=<seconds>` freezes the clock, so stills are deterministic. `&mx=&my=` (from -1 to 1) sets the sway. Probe functions: `prSetTime(t)`, `prStats()`, `prFit()`, `prCycle`.

## Cycle timing (T = 8.0 s, seamless)
| s | what happens |
|---|---|
| 0.00–1.10 | a blank sheet comes down 46 units onto the stand, fading in over the first 0.55 s |
| 1.25 | the header drops in (each part flies for 0.55 s) |
| 1.75 / 1.95 / 2.15 / 2.35 | the four KPI tiles |
| 2.85 | the chart |
| 3.45 | the table (the page is complete at 4.0) |
| 4.40–5.40 | the red check sweeps top to bottom |
| 5.70–7.10 | the page lies down onto the stack (rotates 64° to 0°, eased) |
| 7.10–7.70 | the press: the stack sinks one sheet |
| 7.70–8.00 | rest |

The seam is checked by pixel diff (`seam.py`): the canvas at t = 7.999 and t = 8.000 differs in 0 pixels by more than 40/255, so there is no visible restart. Sheet identity is `cycle - j`, so the askew offsets travel with each sheet across the seam.

## View angle and where it comes from
- Rest pose: yaw -27° / pitch 20°, with sway YAW_R 25°, PIT_R 12° and TAU 1.0. Taken from the callipers: `notes/_lanes/296/C/v14-plain-before-c.html:6772` (`var YAW0 = -27*D2R, PIT0 = 20*D2R, YAW_R = 25*D2R, PIT_R = 12*D2R, TAU = 1.0;`). That is the brain's rest pose that Dave ruled at #298 B (`:3482`) and applied to the callipers at #299 C ("the illustration need to have it's resting state match the others, reference the change we made to the brain").
- **Not matched:** the catalogue `#ct` (`:8168`) and the shells `#shl` (`:3882`) still rest at yaw -35.
- `setView`, `springStep`, `updateView`, `prepare`, `rayHits` and `splitLine` are the callipers' (`:6772–6960`). The projection convention is the same: world [x, y, z], y toward the camera, z up.
- **Fit:** the callipers' K = 0.42 blend of rest and orbit boxes, plus one change. The press is width-bound at rest but its height over the sway is not, so the scale is capped to the whole orbit's height and centred on it. This costs about 3% of scale at 1440×900. Without it, the tray's near corner left the canvas by 16 px at the pitch-down corner of the sway. The orbit corners are checked in `frames/orbit-corners.png` (all within the canvas).

## Frames
- `notes/_lanes/303/P/frames/sheet.png`: the contact sheet, 3×2.
- `1-blank.png` (0.55 s), `2-parts-half.png` (2.3), `3-complete.png` (4.2), `4-red-sweep.png` (4.95), `5-to-stack.png` (6.5), `6-press.png` (7.45).
- `orbit-corners.png`: the sway extremes at 4.2 and 6.4.
- `ref_s6.png` and `ref_s8.png`: the deck's catalogue and callipers slides, rendered for reference only.
- Drivers are in the same folder: `shoot.py [t:name ...]`, `seam.py`, `corners.py`, `fit.py`, `shoot_ref.py`.

## Design rounds
1. **First layout:** the page was made on a stand to the left and slid to a stack on the right. It read correctly, but the scene was 2:1 in a near-square column, so the drawing was small and the stack was a thin sliver.
2. **Moved the stand over the stack:** the page now lies down onto the stack instead of travelling to it. The drawing is about 1.7× larger. The stand was lifted 8 units so the page's bottom edge clears the stack top. The jitter was reduced, and the moving dashed sheet lines inside the tray were cut to the bank's outline (they were too dense).
3. **Fixed the clipping** at the sway extreme (see Fit above), and thickened the red from 1.6 px to 1.8 px.

## What I could not do or judge
- **Type:** the seat has no Univers Next, so type was judged only as fallback Helvetica. The h1 at 124px and the close-line fit the 38fr column at 1440 (two lines).
- **Motion:** I judged motion from stills plus the seam diff only. I did not watch it play. The pacing (the 8 s cycle, 0.55 s snaps, the 1.4 s lie-down) needs Dave's eye on a real screen.
- **Hidden lines:** the painter's order is not ray-cast verified the way #302 A was. It is simple here (stack bottom-up, then page, then parts, with the part in flight last), and nothing visibly wrong showed in the frames or at the orbit corners.
- **Where the prototype departs from the brief:** the stack is not literally "growing to 8 then reset". It is always fed at the top and pressed out at the bottom (7→8→7), which is what makes it seamless. The page is also composed tilted on a stand above the stack, not flat on the tray. Flat at pitch 20°, a page foreshortens to about 30% and does not read as a web page.

## Phase 2: how to put it into the source's s12 (`notes/_lanes/296/C/v14-plain-before-c.html`, then `python3 notes/_lanes/296/C/build_c.py`)
1. **HTML** (the s12 section, `:1055–1062`): wrap the label, h1 and close-line in `<div class="type">…</div>`. After it, add `<div class="draw rv d2"><canvas id="pr"></canvas><img id="prPrint" alt=""></div>`. Keep `.pagenum`. There are no id collisions: the source has no `id="pr"`, `prPrint` or `pr*` globals, and nothing reads `location.search`.
2. **CSS:** put the block marked `/* PHASE 2 ADDITION */` from press.html into the s12 `<style data-lane="G3">` block (`:1064–1070`). That covers `#s12 .inner` grid, `.type`, `.draw`, `canvas`, `#prPrint`, the `max-width:900px` rule and the `@media print` rule (the print block is canvas hidden, img shown, `.draw` 560px). Alternatively, add `#s12` to the selector lists at `:258–280` and `:402–405`.
3. **JS:** copy the one IIFE from press.html (`/* 16 · THE PRESS */` down to the closing `})();`) into a new `<script data-lane="303-P">` before `</body>` (`:8784`, after the `297-C` script at `:8699`). Before pasting, either delete the query-string lines (`var Q = …`, `frozen = …Q.t…`, the `Q.mx` line) and set `frozen = null`, or rename them to a `prt` key so a deck URL can never freeze slide 16. The `prFit` probe can be dropped. The IntersectionObserver already targets `s12`.
4. **Check after building:** render the generated deck's s12 at 1440×900 at a few `prSetTime(t)` values, and confirm the other slides are byte-identical outside the s12 region.

## Phase 2: integrated into s12 (Dave approved, with three changes)
**Backup:** `notes/_lanes/303/v14-plain-before-c.pre-P2.html` (`cp -p`, taken before any edit).
**Edits:** every edit is an exact single-match replace with `assert count==1`, scripted in `notes/_lanes/303/P/integrate_p2.py`. One more edit added the `prStill` probe. The deck was rebuilt with `python3 notes/_lanes/296/C/build_c.py`.

### The three changes Dave asked for
1. **The red rule stays inside the page.** It now runs from the page's left edge to its right edge on the printed face (no ±7 overhang). It is also clipped to the face's own outline with `ctx.clip()`, so it can never draw outside the page. This is fixed in both press.html and the source.
2. **Apollo is always bold.** Added `#s12 h1{font-weight:600;}`, the cover wordmark's weight. It is scoped to s12 and verified as computed fontWeight 600.
3. **The strapline breaks where Dave said.** It now reads `Automated product design<br>you can bank on.` The text is otherwise identical, and it renders as 2 lines.

### What changed in the source
- **HTML (s12 only):** the label, h1 and close-line are wrapped in `<div class="type">`. Added `<div class="draw rv d2"><canvas id="pr"></canvas><img id="prPrint" alt=""></div>`. The pagenum is unchanged.
- **CSS:** one new block, `<style data-lane="303-P">`, right after the G3 style block. It holds the s12 two-column grid, `.draw`, canvas, `#prPrint`, the max-width:900px rule, the print rule (canvas hidden, print still shown) and the bold h1.
- **JS:** one new block, `<script data-lane="303-P">`, before `</body>`. It is the prototype's IIFE with the query-string freeze removed, so a deck URL can never freeze slide 16. The IntersectionObserver on `#s12` means the loop runs only while s12 is on screen. `#prPrint` is baked from the t = 4.2 rest still (on `beforeprint`, and once at 1.2 s), like cpPrint.
- **Probes:** `prSetTime(t)` freezes the clock and renders; `prStill()` resets the sway to rest (the callipers' calStill); `prRun()` resumes; `prStats()`.

### Verification (one render call per run, seat recipe; `verify_p2.py`)
- **Deck health:** 0 page errors, 16 `.slide`, pagenums "01 / 16" to "16 / 16" unchanged.
- **s12 type:** h1 computed fontWeight "600"; close-line 2 lines, innerText "Automated product design\nyou can bank on."
- **The loop:** it starts when s12 scrolls into view. The clock read 2.45 s after 2.5 s on screen.
- **Stills (s12 at 1440×900, after `prStill()`):**
  - `frames/p2-parts.png` (t 2.3, 4 parts in)
  - `frames/p2-check.png` (t 4.95, the red check, clipped to the page)
  - `frames/p2-lie-down.png` (t 6.5)
  - `frames/p2-check-canvas.png` (the canvas alone at 4.95)
  - `frames/p2-live.png` (the free-running loop at about 2.5 s)
- **Headless sway:** in the first verify run, the headless browser had pushed the sway to its corner (yaw about -52°). The live loop reacts to pointer events, exactly like the callipers, so p2-live.png may show some sway. The frozen stills are taken after `prStill()`, at the rest pose (yaw -27 / pitch 20).
- **In the deck:** the draw column is 648 px wide, not the prototype's 737, because the deck's slide padding leaves room for the chapter rail. The fit rescales automatically and nothing clips.
- **Source diff against the backup:** only the 3 s12 lines are replaced; everything else is added (the s12 wrapper, the CSS block and the script block). No other slide was touched.

## Phase 3: the scan follows the page's relief (Dave: "can the scan be a little slower and look like its going over the topology of the page rather than being a straight line, so it shows the raised edges of the components")
**Backup:** `notes/_lanes/303/v14-plain-before-c.pre-P3.html` (`cp -p`).
**Edits:** exact single-match replaces, all inside the `303-P` script block, scripted in `integrate_p3.py` and `integrate_p3b.py`. The same replaces were applied to `press.html`. The deck was rebuilt with `build_c.py`.

### What changed
- **Raised parts:** the header, KPI tiles, chart panel and table are now shallow raised slabs, 4.5 units high instead of 1.1. Their side edges are in the same hairline ink as everything else. The relief shows as a thin strip on each part's right and lower side, and the page still reads as a web page.
- **The scan is now a profile line**, like a laser line over a surface. It runs flat on the page, steps up at each part's edge, runs across its top and steps down its far edge. It is still clipped to the page outline.
- **The scan now runs down the page and sweeps left to right** (it used to run across the page and sweep top to bottom). I changed direction after looking at the first attempt. From this camera angle, "up off the page" lands almost exactly along a line running across the page, so the steps folded back onto the line itself and no relief showed. A line running down the page shows every step as a clear sideways jog.
- **Slower:** the scan now takes 1.9 s instead of 1.0 s. The cycle is 9.0 s instead of 8.0 s. The beats after the scan moved later by 0.9 s but keep their own pace:
  - scan 4.40–6.30
  - lie-down 6.60–8.00
  - press 8.00–8.60
  - rest 8.60–9.00

### Verification (`verify_p3.py`, one call)
- **Deck health:** 0 page errors, 16 `.slide`, pagenums 01 to 16 unchanged, `prCycle` = 9.
- **s12 type:** h1 weight 600, strapline 2 lines, loop running.
- **Seam:** the canvas at t = 8.999 vs t = 9.000, and at 17.999 vs 18.000, differs in 0 pixels by more than 40/255.
- **Scope:** the diff against the P3 backup is confined to the `303-P` script block.

### Stills (rest pose via `prStill()`)
In `notes/_lanes/303/P/frames/`:
- `p3-relief.png` (4.2)
- `p3-scan-a.png` (4.85), `p3-scan-b.png` (5.35), `p3-scan-c.png` (5.85): three moments mid-scan
- `p3-lie-down.png` (7.3)
- `p3-press.png` (8.3)
- `p3-sheet.png`: contact sheet of the six
- `p3-zoom-a.png`, `p3-zoom-b.png`, `p3-zoom-c.png`: the canvas at 2×

I checked crops of the 2× shots: the red begins and ends exactly on the page outline and jogs at every part edge.
