# 289 · I2 — A stack of books, in the gearbox's hand

Built: `notes/_lanes/289/illustration/books.html` (standalone, white card,
one canvas, no libraries). Shots: `books-rest.png`, `books-orbit.png`
(same folder, device scale 2, card cropped at 600×420 CSS px).

## What it is

Seven hardback volumes on a base plate. Each volume is three stacked
prisms — bottom board, text block, top board — extruded in b from a plan
footprint: a rectangle with a **rounded spine** (a sampled circular bulge)
on the +a side. The boards use the full footprint, the text block the same
footprint inset by 3.4 on fore edge, head and tail, so the boards stand
**proud** on three sides and the spine stays one continuous curve. The
page block is a set of lighter (#C6C6C6) hairlines at constant b on every
visible text-block face that is not the spine — leaf edges, which a closed
book shows on the fore edge *and* on head and tail. At the resting yaw the
head is what faces us, so that is where they land. Each volume is yawed
1.5–5.5° about the vertical and nudged a unit or two in plan.

Projection, spring, mouse and palette are lifted from the s3 gearbox:
yaw 35 / pitch 20 at rest, ±25 / ±12 on the mouse, critically damped
τ = 1.0 s, **stays where the mouse left it**. #111 hairline, #BDBDBD
hidden, #9B9B9B dash-dot construction, one #DA1A00 accent — the **top
volume's spine**, the only red on the card. Probes: `bkStats()`,
`bkView()`, `bkSetMouse(x,y)`, `bkStill()`.

Hidden line is done three ways, all computed:
1. **Per face.** A plan face's normal is ±b, so the test is `m21` alone; a
   side face's normal lives in (a,u), so it is `m20·na + m22·nu > 0`.
   42 of 273 faces are culled at rest; back faces are never emitted.
2. **Between prisms.** Painter's order: fill white, then stroke. The view
   always looks *down* (pitch stays in 8…32°), so a lower prism can never
   overlap a higher one from in front — prism order is exact between
   prisms, centroid depth settles faces within one, which is exact
   because a prism is convex.
3. **Lines that pass behind the stack.** Each base-plate and axis segment
   is clipped (Cyrus–Beck) against the convex hull of every volume's
   projected outline; clear runs ink solid / dash-dot, occluded runs ink
   #BDBDBD dashed on top of the fills. That is the only dash here.

## Rejected, and why

- **Dashing the volumes' own hidden edges.** A stack of slabs hides almost
  nothing informative — only its own underside. 570 dashes that say
  "boxes have bottoms" is the wireframe look v7.5 cut. Dashes were spent
  on the plate and the axes instead, where they say the stack is *on*
  something.
- **A separate spine arc for the text block.** First build sampled the
  bulge over the text block's own (inset) depth, so board and text arcs
  diverged and the spine read as a peeling flap. The text block now
  samples the *board's* curve over its own sub-range: one spine surface.
- **Stroking every face boundary.** Inked the arc's tessellation creases
  and the spine read as a radiator. A vertical crease is now stroked only
  where the footprint changes kind or where it is the silhouette — the
  gearbox's `hard[]` rule.
- **Sorting all faces by centroid depth alone.** Large near-horizontal
  board faces jumped ahead of tall side faces and left strays across the
  page hatch; prism-major order fixed it (verified with a per-volume
  colour render).
- **±9° yaw and ±8% footprint spread.** Read as a fanned pile, not a
  stack; halved.
- **Callouts.** The gearbox needs them (12T/30T); a book does not. One
  mono block, `n = 7 vol`, tied to the ink box.

## Pass two — the spine is straight

Dave, on the first render: *"notice the curve on the books — these edges
should be straight."* Right — the rounded spine was a brief mistake. The
footprint is now a **plain rectangle**: four corners, four straight edges,
nothing sampled; `BULGE` / `NARC` / `arcA` are gone and every book is a
rectangular box, the spine a flat face like the other three. Pass one kept
as `books-v1.html`.

Everything else holds: proud boards, page-edge hairlines, both hidden-line
passes, base plate, axes, damped orbit. The red accent is now the top
volume's **spine edge** — two verticals and the two long edges, one
rectangle outline; the board/text creases inside that face stay black, so
it reads as an outline and not a ladder. Re-shot at device scale 2: 63
faces drawn, 42 culled, 38 page lines, 7 hulls, no console errors.
