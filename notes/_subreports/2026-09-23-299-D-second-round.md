# #299-D: Dave's second round on the plain Friday deck

provenance: 299 · 2026-09-23
status: observed
session: #299 · 2026-09-23 · lane D (Opus 5.5, remote-device seat)
brief: the conductor's in-chat brief to lane D. Dave's words, 14:12 BST (verbatim in the brief): "turn 09's callipers a quarter turn so they face you like the others? / Put: 'Built from the 36 components available. The work checked automatically, and then by a human.' on two lines / On: 'We asked: what else is slowing design?' match the typography of the other slides, 'We asked:' in the lighter font / Lets make the KG illustration a bit smaller, 15% say, and make it spin slowly :)"
tokens: UNMEASURED (this lane's message.usage cannot be read from the device seat)

## VERDICT

**DONE, all four items, in three commits that each land alone.** Headings (B, C) → `d5583dee`; callipers (A) → `e3f0de60`; the graph (D) → the third commit (sha in § POST-COMMIT). The source was edited and the deck rebuilt with `build_c.py` each time, never hand-edited; `build_e.py` was not run; `build_c.py` was not touched. Pixel diff, the pre-edit deck against the final deck, all 16 slides plus 11's second state, at 1920x1080 and 1440x900 under reduced motion: **only 04, 06, 09 and 13 change**, and on each only the intended element.

Three things to know:

- ⚠ **04's heading had to come down in size.** The bold line is 1381px wide at 54px, and the column is 1120px. Widening the measure to the column was not enough, so the size cap went from 54px to **43px**, the largest whole px at which it fits (44px wraps to three lines).
- ⚠ **The graph's rest pose is yaw -35 / pitch 20, not -27 / 20.** The hub on 13 draws 08's shells, which rest at the shared -35 / 20. The -27 figure belongs to the brain on 10 and now the callipers on 09. The turn starts from the pose 13 had, -35 / 20.
- **Slide 09 needed one more setting than PSI.** Turned a quarter, the painter's order buried the little lock screw under the carriage, so the carriage's two fittings are now pinned on top. This was checked by ray-casting (A, below).

## The items

The source is `notes/_lanes/296/C/v14-plain-before-c.html`.

### B. 04 "What we tested": the heading on two lines. DONE (commit 1)

- The markup went from `Built from the 36 components available. <b>The work checked automatically, and then by a human.</b>` to `Built from the 36 components available.<br><b>The work checked automatically, and then by a human.</b>`. The words are unchanged, and the break is forced after "available.".
- CSS: `#s5x h2{max-width:21em;font-size:clamp(32px,3.7vw,54px)}` became `#s5x h2{max-width:none;font-size:clamp(32px,3.7vw,43px)}`, with a non-rendered comment.
  - **The measure:** 21em (1134px at 1920, 1118.9px at 1440) went to `none`. The 1120px column (`.inner`) bounds it at both sizes. This is the first step the brief allows, and on its own it is not enough, because the bold line needs 1381.3px at 54px and 1362.5px at 53.28px.
  - **The size:** at 1920 it went from **54px to 43px**, and at 1440 from **53.28px to 43px**. Only the cap moved; the vw slope and the 32px floor are unchanged. Probe `_work/probe_fit.py` forces 44px, which gives 3 lines (753 / 960 / 154px). At 43px it is 2 lines, **736.2px (light) / 1099.9px (bold)** in the 1120px column, at both sizes.
  - Print keeps its own `#s5x h2{font-size:40px}` (1023px at 40px, in the 1136px print column). It was not rendered.
- With the heading down from 3 lines to 2, the steps diagram below sits higher. The slide's content block is centred.

### C. 06 "What can we improve": "We asked:" light. DONE (commit 1)

- `<b>We asked: what else is slowing design?</b>` became `We asked: <b>what else is slowing design?</b>`.
- This is the sibling pattern: a light lead-in and the rest in `<b>`, as on 07 (`The first improvement: <b>…</b>`) and 04. The weights are 300 and 600, the size stays 64px, and the heading stays on 2 lines at both sizes. The words are unchanged, and so is the DOM text.

### A. 09 the callipers: a quarter turn. DONE (commit 2)

- **The quarter turn:** `var PSI = -90*D2R;` became **`var PSI = 0*D2R;`**. This is the separate setting that #299 C named, the callipers' lie on the plate. The rest yaw stays **-27**, and pitch 20, YAW_R, PIT_R and TAU are unchanged. 07 and 08 are untouched.
- **Why 0 and not -180:** at PSI 0 the jaws' depth coefficient is positive, so the jaws come toward the viewer, as they did at -90. The beam runs left to right with the fixed jaw on the left, and the graduated face is up. At -180 the jaws would point away, behind the beam.
- **Result:** the beam, and the plate's long side with it, now run across the front, as the plates on 07, 08 and 10 do (the books lie at PSI -5). At rest, calView gives beam +0.427 and jaws +0.837, where it was -0.837 / +0.427.
- **Painter's order.** Over the orbit (yaw -52..-2, pitch 8..32), the beam's depth coefficient is +0.03..+0.78 and the jaws' is +0.53..+0.99. Each keeps one sign, so the drawing stays monotone in depth, which is the condition in the header.
  - Centroid order then breaks one pair: at PSI 0 the lock screw's centroid falls behind the carriage's, so the carriage's white fill covered it.
  - Fix: the thumb wheel and the lock screw get `ord 1` (source, in `buildGeom`), so they are drawn over the carriage. The sort comment was updated. Pinning the lock alone made a new fault (lock over wheel at pitch 8), and pinning both clears it.
  - **Probe** `_work/probe_paint.py`: every 2 css px, ray-cast against the convex solids. It compares the TRUE front solid with the PAINTED one, at rest and at the 8 orbit corners and edges, with the slider at t = 0 and 6.5 s.
    - PSI -90 (the committed state before, the baseline) has only attachment classes (parts that touch or run into each other: carriage/beam, jaw/carriage, rod/beam, inside-jaw/beam), plus a real fault at the yaw -2 corners: the carriage drawn over the wheel, 37-136 samples.
    - PSI 0 with the pin has the same attachment classes and no carriage-over-wheel. The only new item is a 7-9-sample sliver, the workpiece over the slider jaw, at the yaw -2 corners at t = 0.
    - At rest, the bad samples are 417 of 6646, against 782 of 7781 before.
- **The fit:** the drawing re-fits itself from the orbit sweep (K 0.42), so it is wider and a little smaller.
  - The rest scale went from 3.659 to **3.193** at 1920 and from 3.058 to **2.668** at 1440. At rest the drawing is fully in frame (box 28.5..639.5 of a 668 canvas at 1440).
  - At the two left mouse corners (yaw -52) the plate's far corner goes about 13px past the canvas's LEFT edge. Before, it went 92px past the RIGHT edge (#299 C's pre-existing note), so this is improved but not zero.
- The source has an 8-line non-rendered comment above PSI and a 2-line note on the sort. By eye (1440): the long side faces the viewer, parallel to 10's plate, and the lock screw and wheel sit on the carriage.

### D. 13 "A smart design system": the graph 15% smaller and turning. DONE (commit 3)

- **Where:** only slide 13 (`#s10map`) has "Smart design system" in a card with a drawing (`#hubShl`, in the hub). 16 has the words as a label with no drawing. The hub drawing is a **separate instance** that borrows 08's shells code: its own image, drawn by a nested block in 08's script. So it was split off cleanly.
  - **08's drawing and 12's Knowledge thumbnail (08's print image `shlPrint`) are untouched:** pixel-SAME, and `anatomyState()` is identical.
- **Size:** `HUB_SCALE = 0.85` multiplies the hub's fit scale. The hub box, the card and the words keep their size, and line weights and node size are unchanged (node radius is floored at 2.6px).
  - Measured ink box, before to after: 1920 222x222 → 190x189 (**0.856 / 0.851**), centre 959.5,533.5 → 959.5,533.0. 1440 161x160 → 137x136 (**0.851 / 0.850**), centre 760.0,446.5 → 760.0,446.5.
- **Turn:** `HUB_TURN_S = 60`, seconds per full turn. It sits next to HUB_SCALE, the first line of that block. The drawing turns about its vertical axis at constant speed (no easing) from the rest pose, **yaw -35 / pitch 20**, which is 08's.
  - Every view's extent is the outer shell's circle and the axis, so one fit serves every angle and the drawing never leaves the box or drifts off centre.
  - It is drawn into a canvas over the rest image at the deck's 30 fps, 0.2° a frame.
  - Probe `_work/shoot_spin.py` (1440, motion allowed): 10.7° at +1.8 s, and **90.1° at +15.1 s** (yaw 55.1).
- **When it runs:** only while slide 13 is on screen (IntersectionObserver, 5%) and the tab is visible. It stops when the slide is left and **resumes from the angle it left** (probe: 94.6° away, 94.6° two seconds later, still turning when back).
  - It does not stop on window blur, unlike the other drawings' idle loops, so it keeps turning on a presenter's second screen. That was a choice, not a slip.
- **Reduced motion:** it never starts, and `#hubShl`, the rest pose drawn as an image as before (now at 0.85), shows. A CSS `@media (prefers-reduced-motion: reduce)` rule hides the canvas as well. If the setting changes mid-talk, the turn stops and the rest shows, or it resumes.
- **Print:** `beforeprint` and the print media query stop the turn and show the rest image. `@media print` hides the canvas and shows the image. Probe: under print emulation the canvas is `display:none` and the image `visible`; after print it resumes. Print was not rendered to PDF.
- **Interaction:** the hub never followed the mouse (the orbit belongs to 08's instance), so there is nothing to pause for.
- The probe surface `shlHubState()` now also reports scale, turnS, spinning, shown (turn/rest), phiDeg, yawDeg and reduced.
- **CSS:** 5 rules in the `297-D` style block, after `#s10map .hub .hubkg img`: the canvas's placement, `.spinning` swapping canvas for image, and the print and reduced-motion guards. The DOM gains one element on 13 (the canvas, `aria-hidden`).

## Render checks

Every render ran at the seat, on the mount, one call per viewport: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/299/D/_work/shoot_d.py <deck> <dir> WxH`. `shoot_d.py` is #299 C's `shoot_c.py` with `reduced_motion='reduce'` on the page, so every shot is deterministic. It uses `goto("file://…")`, `executable_path=$RENDER_SHELL`, and the same freezes and pointer block. Diffs use `_work/pdiff_d.py`: the rail band (x<200) and content apart, with the bbox, the count and the largest channel sum.

**Pre-edit deck (`_work/before.html` = HEAD `0e23408e`) against the final deck:**

| slide | 1920x1080 | 1440x900 |
|---|---|---|
| 01-03, 05, 07, 08, 10, 11, 11b, 12, 14, 15, 16 | SAME | SAME, except harness flicker on 14's rail (below) |
| **04** s5x | content DIFF 399-1520 x 238-824 (the heading, and the block moves up) | content DIFF 200-1320 x 150-733. The rail band's single pixel at (199,272) is the heading's "B" antialiasing at x=199 |
| **06** s4p | content DIFF 400-1326 x 375-435 (the heading only) | content DIFF 200-1126 x 285-345 |
| **09** s8 | content DIFF 877-1610 x 365-715 (the drawing only) | content DIFF 713-1326 x 303-597 |
| **13** s10map | content DIFF 848-1072 x 404-664 (the drawing only) | content DIFF 679-841 x 355-541 |

- **Harness flicker:** the rail at x 37-40, 43-45 px, max 24-74/765, on 14 and/or 16. It appears identically between two shots of the **same unedited deck** at 1440 (`before-1440` against `before-1440-rep`: 14 and 16). It is not an edit.
- **Commit by commit, at 1440:** before → commit 1 changes 04 and 06 only. Commit 1 → commit 2 changes 09's content only. Commit 2 → final changes 13's content only. Everything else is the flicker above.
- **DOM facts:**
  - s5x gains 1 element (the `<br>`), and its text differs only by that line break.
  - s10map gains 1 element (the canvas).
  - No other text, count, pagenum or step changed. 06's text is identical.
  - `anatomyState()` is identical. There are 0 page and 0 console errors before and after.
  - The one flagged render, 11b's 4 box items on "Proposal:", is pre-existing and unchanged. There are 0 rail hits.
- **Commit read-back:** the deck in `d5583dee` is byte-identical to `_work/after-type.html`, and the deck in `e3f0de60` to `_work/after-cal.html`.

**Contact sheet: `notes/_lanes/299/D/before-after.png`** (2952x5793, 0.96 MB). It has 04, 06, 09 and 13 before and after at 1440x900, then 13 at rest against 13 about 15 s into the turn, then the graph close up (x2.5) at rest and at a quarter turn. The driver is `_work/sheet_d.py`.

## Commits

All went through `SESSION_N=299 INSTRUMENT_AUTOSTAGE=0 DOC_ROW_ACK="…" bash knowledge/_git_commit.sh --reconciled --quiet=<log> <msgfile> <paths>`, with python-written msgfiles. Line 1 is a plain summary (T3 adds `after #299 2026-09-23 — `).

1. **`d5583dee`** (`d5583deeb8b8a7f119d788fef1a846c692c41e1f`), "two headings on the plain Friday deck set as Dave asked". 2 files, +10 / -6: the source and the deck. Transcript: `notes/_lanes/299/D/_gitcommit-D1.log`.
2. **`e3f0de60`** (`e3f0de60283d759f93c4ae6da0359e315a8fac68`), "slide 09's callipers turned a quarter turn to face the viewer like the other drawings". 2 files, +24 / -8. Transcript: `_gitcommit-D2.log`.
3. The graph, with this report and the contact sheet. See § POST-COMMIT.

- ⚠ **Doc-row gate:** the first attempt at commit 1 was REFUSED, with nothing staged. The unrowed doc is #299 C's report (`notes/_subreports/2026-09-23-299-C-his-last-changes.md`). Every commit then passed with `DOC_ROW_ACK` as a DECLARED gap, because `knowledge/_state.json` is outside this lane's brief. **Owed to the conductor:** rows for #299 C's report and this one.
- Gates otherwise green: reuse, chain fresh, showroom, polarity, mention map, session witness #299. The wrap gate is red but visible (declared not-a-wrap). The same two non-blocking boot-drift ❌ lines as #299 C's (#297's 127,600 reading) appeared, and so did the duplicate-heading ⚠ lines. Neither belongs to this lane.
- **Locks:** git printed `unable to unlink .git/index.lock` once per commit, and the script's own clearing handled it ("locks clear"). `.git/*.lock` and `.git/refs/heads/*.lock` were empty afterwards. Nothing was moved to `_orphan-locks`.
- The premise held: before any edit, the source, the deck and `build_c.py` were byte-identical to HEAD `0e23408e`, and there were no locks. `git status`, `git diff`, `add -A`, `reset` and `checkout` were never run. **Not pushed.**

## UNPROVEN / CLAIMED

- **UNPROVEN:** print-to-PDF of 04 and 13. Print was emulated for 13's state only (canvas hidden, image shown).
- **UNPROVEN:** the turn at 1920 and on a real display over minutes. It was rendered at 1440 for 15 s, and the rate is exact (6°/s measured).
- **CLAIMED:** the painter's-order probe samples every 2 css px at 1440. Faults thinner than 2px could slip between samples.

## PATHS

Changed, committed: `notes/_lanes/296/C/v14-plain-before-c.html` (the source) · `notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html` (rebuilt).
Created, committed: `notes/_lanes/299/D/before-after.png` · this report.
Working files, **not committed**: everything in `notes/_lanes/299/D/_work/`:
- pre-edit copies and states: `before.html`, `source.before.html`, `after-type.html`, `after-cal.html`, `after.html` and `hub-block.before.txt`
- render folders `before-1920`, `before-1440`, `before-1440-rep`, `type-1440`, `cal-1440`, `after-1920`, `after-1440` and `spin-1440`, each with `_facts.json`
- drivers `shoot_d.py`, `pdiff_d.py`, `sheet_d.py`, `probe_type.py`, `probe_fit.py`, `probe_cal.py`, `probe_paint.py` (and its `_variant-*.html`) and `shoot_spin.py`
- edit scripts `edit_type.py`, `edit_cal.py` and `edit_hub.py`
- peeks `peek-*.png`

Also not committed: the msgfiles `notes/_lanes/299/D/_msg-D*.txt` and the transcripts `_gitcommit-D*.log`.

---

## § POST-COMMIT (added AFTER the commit, not in it)

- **Commit 3: `a7b2c9f2`** (`a7b2c9f2107d572be71cf98b2498e12444908d00`), subject `after #299 2026-09-23 — slide 13's knowledge graph 15% smaller and turning slowly, a full turn a minute`. 4 files, +306 / -26: the source, the rebuilt deck, `notes/_lanes/299/D/before-after.png` and this report.
  - Gates: doc-row is a DECLARED GAP, covering this report and #299 C's. Everything else is as for commits 1 and 2, and the run ended with "locks clear".
  - The transcript is `notes/_lanes/299/D/_gitcommit-D3.log` (exit 0).
- **Read-back:** the four paths, plus `build_c.py`, are byte-identical to HEAD. `git log`: `a7b2c9f2` ← `e3f0de60` ← `d5583dee` ← `0e23408e`.
- **Locks:** none stranded. `.git/*.lock` and `.git/refs/heads/*.lock` were empty.
- **Not pushed.**
- **Owed to the conductor:** `_state.json` rows for this report and for #299 C's.
- This tail is itself uncommitted.
