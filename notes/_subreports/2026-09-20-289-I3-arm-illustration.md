# 289 · I3 — industrial robot arm, line-drawn 3D

`notes/_lanes/289/illustration/arm.html` · renders `arm-rest.png`, `arm-orbit.png` (600×420 card, device scale 2).

## What it is

A six-axis manipulator built as a KINEMATIC CHAIN of convex primitives — N-gon
prisms and boxes — one transform per link, so every joint angle is a parameter:

    J1 base yaw (about b) · J2 shoulder pitch · J3 elbow · J5 wrist pitch · J6 roll

Parts: base plate, bolt flange with four lugs, housing skirt and column, shoulder
axle, bearing boss, upper-arm box beam (L2 = 195), elbow drum, forearm beam
(L3 = 160), wrist drum, roll barrel, palm, two fingers. 17 primitives, 432
vertices, 125 faces drawn / 125 culled, 367 edges inked.

## The three things that made it work

1. **The offset chain is load-bearing, not styling.** J2/J3/J5 are parallel, as on
   any real arm, and each link steps one notch further out along that shared axis.
   That axis keeps a positive depth coefficient (0.877 at rest, >0 across the whole
   orbit range), so painter's order BY PRIMITIVE is exactly chain order — exact,
   not sorted. Within a primitive, faces sort by centroid depth, exact because the
   primitive is convex.
2. **A joint is a cylinder wider than the beam it carries.** v1 had the upper arm
   drawn over its boss and its butt end sticking out below the shoulder like a
   stick leaning on the housing. Fix: draw the beam, then the boss ON it, with the
   boss wider along the joint axis than the beam. The boss swallows the beam end
   exactly and the joint reads as a joint.
3. **Hidden-line for the axes is done in 3D, not in the picture plane.** Books
   clipped against 2D hulls; that has no depth, so an axis stub poking TOWARD the
   camera would be called hidden where it crossed a silhouette. Here a point is
   hidden iff the view ray p + tV, t ≥ 0, meets some primitive — an ordinary slab
   clip against the convex face half-spaces, with a screen-bbox early-out (under
   orthographic projection a solid's shadow projects to its own silhouette).
   Transitions sampled at 44 and bisected 11× to under a pixel.

## Ink, per the idiom

`#111` hairline visible · `#BDBDBD` dashed for the runs that explain the
mechanism only: the five joint axes inside the castings they turn in, the shoulder
axle inside the housing (gearbox-style silhouette pair + far cap), the base plate
behind the machine · `#9B9B9B` dash-dot where those axes are in the open ·
ONE red `#DA1A00`: the elbow's circular joint face rim. `armAxisRuns()` measures
it — J2 open 10.5 px / buried 76.3, J3 10.5 / 43.9, J5 10.5 / 27.7.

Resting yaw 35 / pitch 20, mouse orbit ±25 / ±12, τ = 1.0 s, stays where the mouse
left it. Idle rocks shoulder 3.5° and elbow 4.5° on an 11 s cycle; suppressed under
prefers-reduced-motion (verified: `running:false`, no errors).

## Iterations

v1 arm fell off the shoulder, elbow drum blobby (two near-coincident circles).
v2 re-nested the shoulder, shortened and narrowed the drum. v3 added hub rings to
boss and elbow, lifted the column above the boss, trimmed the J6 stub (61→38 px).
v4 dropped the wrist to 42° to fill the bottom-right and open the gripper.
