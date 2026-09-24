# #302 A: the callipers stand up on 09 and 12

**Dave, Thu 2026-09-24 07:59 BST:** "can the callipers on slide 09 and 12 be perpendicular to the tray"

**DONE.** On 09 the calliper now stands upright on the tray. The beam runs across the front with the fixed jaw on the left. The outside jaws point up, the graduated face is toward you, and the slug is gripped between the jaws with its axis toward the camera. The rest pose is unchanged at yaw -27 / pitch 20. Slide 12's plate follows automatically through img#cpPrint, and I checked it by eye.

## The stance: two parallels
- The instrument stands on **two plain rest blocks (machinist's parallels)** under the beam's lower edge. One is left of the carriage, at x 22..38. The other is under the far end, at x 118..134. The small inside jaws hang 3 mm clear of the tray.
- **Why:**
  - Standing on the inside-jaw tips puts both supports at the left, around x 0 and x 49, while the beam and depth rod run out to x 184. That would topple, and the tips are slanted points.
  - Standing on the beam's edge means the inside jaws go through the tray.
  - Parallels are what an inspector actually uses to stand a gauge up. It is two boxes, and it reads at once.
- **The tray** keeps its style: a transparent wire box with all 12 edges, classified in 3D. It was resized to suit the standing instrument: depth z -16..36 (it was a 106 mm-wide plate), with the length unchanged.

## What changed (source `notes/_lanes/296/C/v14-plain-before-c.html`, callipers block only)
- **Frame:** `Fc = {x:Fc0.x, y:Fc0.z, z:Fc0.y}`, where Fc0 is the old lying frame at PSI 0. The jaw direction is now up and the face normal points at the camera. Every part keeps its Fc millimetres.
- **Graduated-face deco test:** `m21 > 0` became `dot(Fc.z, VD) > 0`. This is scoped to the callipers, because the same line also exists in the robot arm.
- **Painter's order.** All three frame axes keep one depth sign over the orbit (yaw -52..-2, pitch 8..32): Fc.x +0.03..+0.78, Fc.y (up) +0.14..+0.53 and Fc.z +0.53..+0.99. So a part can only hide what is left of it, below it or behind it. `ord` is now pinned from that rule, in this order:
  - parallels -3
  - inside jaws -2
  - beam (left) -1
  - carriage 0
  - beam (right) 0.5
  - fixed outside jaw 1
  - slug 2
  - slider outside jaw 3
  - wheel / lock / depth rod 4
- **Three fixes that remove the "attachment" faults #299 D had accepted.** None of them changes anything you can see:
  - The beam is split either side of the carriage. Its middle is wholly inside the carriage, and its edges are still carried through dashed.
  - The slider jaw's root is trimmed to the carriage top. That part is wholly inside the carriage.
  - The depth rod sits on the beam face (`ROD_Z = ZB1+ROD_R`) instead of 1.3 mm sunk into it.
- **The two parallels** were added as `bx(...)` at ord -3.
- **Edit scripts:** `notes/_lanes/302/A/edit_a.py`, then `edit_a2.py`. After those, the tray depth was changed by hand from -24..44 to -16..36, to cut the orbit-corner overshoot. The deck was rebuilt with `build_c.py` only.

## Checks
- **Ray-cast painter's-order probe:** `notes/_lanes/302/A/probe_paint_a.py`, which is #299 D's probe with the new parts named. It samples every 2 css px at 1440, at rest and at the 8 orbit corners and edges, with the slider at t = 0 and 6.5.
  - **0 bad samples in all 18 views** (for example 0 / 13,738 at rest). Output: `probe-final.txt`.
  - Before, at rest, it was 417 / 6,646 bad, all from the accepted attachment classes.
- **Full deck at 1600x900** (`shoot_w.py`): **16 renders, 0 rail hits, 0 overflow, 0 errors.**
- **Pixel diff against the pre-edit deck:**
  - Only **09 and 12** change.
  - 13 also differs, at 731..863 x 402..518 on the spinning graph hub. It is harness flicker: two renders of the unedited deck differ in the same place (`shots-before` vs `shots-before-rep`).
- **Source diff:** `notes/_lanes/302/A/source.diff`. Every hunk is at lines 6569..6942, inside the callipers block (6555..7054 before). The deck diff is the same.

## Named, not fixed
- **At the extreme orbit corners, the tray's end runs past the canvas.**
  - At yaw -52 / pitch 32 it runs 29 px past the bottom. At the yaw -2 corners it runs 12 px past the right.
  - #299 D had a 17 px overshoot on the left, and the K 0.42 fit allows this by design.
  - At rest the drawing is fully in frame: box 33..726 x 122..562 of a 759x684 canvas.
  - Fixing it would mean changing the shared fit (centring on the sweep, not the rest), which would move the rest pose. Not done.

## Paths (all under notes/_lanes/302/A/)
- `before-after.png`: 09 and 12, before and after, side by side
- `before-after-zoom.png`: 09's drawing, before and after
- `orbit-corners.png`: rest plus the 4 corners, after; `orbit-corners-before.png` is the same set before
- `shots/` (after), `shots-before/`, `shots-before-rep/`
- `v14-plain-before-c.BEFORE-A.html` (the source backup), `deck.BEFORE-A.html`
- nothing committed; git was not touched

---

# Revision: turned over, floating, tilted (Dave, 08:18 BST)

**Dave:** "spin through 180 degrees so the disk its measuring is pointing down and it doesn't need the supporting blocks, it's fine just floating, maybe give it an angle so the calliper end is raised"

**DONE. In the deck: reading A, the jaw end raised 10 degrees.**

- **Orientation:** the outside jaws and the slug now point down, and the graduated face faces the camera. The fixed jaw is on the **left**.
  - The half-turn about the beam put the face on the back, so the depth axis was mirrored back to the camera.
  - The result is exactly how a real calliper is held and read face-on: jaws down, fixed jaw left, scale along the beam's lower edge, and the thumb wheel under the slider. It reads more naturally than the upright version, which was a mirror image.
- **Floating:** the two rest blocks are gone. The tray is now flat in the world and fitted automatically under the instrument.
  - Its top sits 20 mm below the lowest point of the metal, over the slider's travel.
  - Its ends sit 16 mm and 3 mm past the instrument, and its depth is unchanged.
  - At 12 mm the slider jaw's tip looked as if it touched the tray's back edge at rest, so I opened the gap to 20.
- **Tilt:** `var TILT` in the source. +10 raises the jaw end (reading A); -10 raises the depth-rod end (reading B).
  - I chose A because the jaws are the working end of a calliper. Also, B nearly cancels the view's own slope at rest, so the beam looks almost level and the tilt barely reads.
  - **To swap to B:** `python3 notes/_lanes/302/A/swap_tilt.py B`. It changes that one line and rebuilds with build_c.py; `swap_tilt.py A` swaps back. The B files ready to use: `source.readingB.html` and `deck.readingB.html`.

## Painter's order
- A view ray leaves every point going right, up and toward the camera, so a part can only be hidden by one to its right, above it or in front of it. The draw order follows from that, back to front:
  1. fixed outside jaw
  2. slug
  3. slider's outside jaw
  4. beam, left part
  5. carriage
  6. beam, right part
  7. inside jaws
  8. wheel / lock / rod
- **The small inside jaws** are trimmed at the carriage edge. That part was always hidden inside the carriage.
- **Reading A needs one extra rule.** Near the yaw -2 edge of the orbit, the beam's direction turns slightly away from the camera (Fc.x depth down to -0.057). The chain along the beam then reverses (slider jaw, slug, fixed jaw; beam right, carriage, beam left), so those parts carry a second order used only there.
  - Without it, the probe found 28-73 bad samples at the two yaw -2 corners.

## Checks
- **Ray-cast probe** (`probe_paint_a.py`, every 2 px, rest plus the 8 orbit corners and edges, t = 0 and 6.5):
  - Reading A: **0 bad in 18 of 18 views** (0 / 13,306 at rest). Output: `probe-readingA.txt`.
  - Reading B: **0 bad in 18 of 18.** Output: `probe-readingB.txt`.
- **Full deck at 1600x900:** A (the deck) has **16 renders, 0 rail hits, 0 overflow, 0 errors**. The B deck is the same.
- **Pixel diff against the original pre-#302 deck:** only 09 and 12 change, plus the known flicker on 13's spinning hub.
- **Source diff:** `source-readingA.diff` against `v14-plain-before-c.BEFORE-A.html`. Every hunk is at before-file lines 6569..6916, inside the callipers block (6555..7054).
- **By eye:** 09 and 12's Scrutiny plate at rest, and every orbit corner (`orbit-corners-A.png`, `orbit-corners-B.png`).

## Named, not fixed
- **At the orbit corner yaw -52 / pitch 32, the tray's front corner runs about 50 px past the bottom of the canvas.** At the yaw -2 corners it runs 13 px past the right.
  - The tray now hangs lower (it floats) and the drawing is taller, so the overshoot at that corner grew from 29 px.
  - The rest view is in frame: box 32..727 x 86..598 of 759x684.
  - Fixing it means re-centring the shared fit on the orbit sweep, which moves the rest pose. Not done.

## Files (under notes/_lanes/302/A/)
- `tilt-readings.png`: 09 in reading A and in reading B, plus 12, whole and close up, all labelled
- `v14-plain-before-c.UPRIGHT-A.html` and `deck.UPRIGHT-A.html`: the upright version, backed up
- `edit_b.py` then `edit_b2.py` (the tray gap was changed from 12 to 20 by hand afterwards), `swap_tilt.py`
- `source.readingA.html` / `source.readingB.html`, `deck.readingA.html` / `deck.readingB.html`
- `shots-A/` (the deck), `shots-B/`
- no git, no Project memory
