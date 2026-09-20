# 289 · I5 — vernier callipers, line-drawn 3D

`notes/_lanes/289/illustration/callipers.html` (standalone, no libraries).
Shots at device scale 2: `callipers-rest.png`, `callipers-orbit.png`.

## What it is
A vernier calliper lying on the base plate, jaws swung toward the camera,
closed on a plain slug at 35 mm. Beam 150 long, graduated on its upper
face; fixed jaw at x = 0; carriage riding the beam at 25 % with its own
outside and inside jaws, vernier, knurled thumb wheel and lock screw;
depth rod out past the far end.

## The idiom, kept
- `#111` hairline visible edges; per-face back-face test, silhouette +
  hard-crease (0.94) inking; painter's order by centroid depth.
- `#BDBDBD` dashed for exactly two things: the beam's three long edges
  where they run **inside the carriage** — classified against the carriage
  ALONE, so nothing else can come back dashed — and the plate and the
  measuring axis where they pass behind metal.
- `#9B9B9B` dash-dot construction: the measuring axis, one line through
  both outside jaws and the slug.
- ONE red `#DA1A00`: the vernier's **zero line**, a single tick, the
  longest on the slider. Picked over the workpiece by rendering — the slug
  in red pulled the eye off the instrument; the zero line IS the reading.
- White card, yaw 35 / pitch 20 rest, damped orbit (tau 1.0) that stays
  where the mouse left it. `prefers-reduced-motion` verified: `running`
  false, static frame drawn.
- Idle: the slider creeps 0..2.5 mm on a 13 s cycle; the caption reading
  follows it (35.00 → 37.50 mm).

## What the four rounds changed
1. **Plate dominated, instrument lost.** Plate hugged to the object;
   K 0.30 → 0.42 with tighter padding. Scale 1.67 → 2.41.
2. **Didn't read as callipers.** Jaws were boxes and the workpiece was a
   tall block swallowing them. Added `polyP`, a prism over a convex
   polygon, so each jaw is a real tapered profile with a flat measuring
   face; the part became a short cylinder standing clear of the beam, so
   the C of the jaws is unbroken and the scale is never covered by it.
3. **Lie of the instrument.** PSI −62° is the flattest angle that still
   keeps the Fc.x depth coefficient negative across the WHOLE orbit
   (−0.04 at yaw −60), so painter's order by depth stays exact. −45°
   reads better but flips sign at yaw −60 and was rejected.
4. **Striped tube.** The 12-gon rod and 16-gon screw creased on every
   flat at the 0.94 threshold. 24- and 20-gon; rod thinned to r 1.9 and
   dropped onto the beam. Knurl added to the thumb wheel.

## Numbers at rest, 600 × 420
10 primitives, 236 vertices, 69 faces drawn / 69 culled, 203 edges inked.
43 main ticks (short 3 / fifth 5 / tenth 7.5 mm) at **6.44 CSS px** pitch,
11 vernier ticks. Draw box 551 × 186 px, inside the card at both orbit
extremes (min x 0.9). No console or page errors in either shot.

Probes: `calStats() calView() calPose() calRuns() calSetMouse() calSetTime() calStill()`.
