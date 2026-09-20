# 289 · I6 — The parts catalogue (open book), line-drawn 3D

**Ruling answered.** Dave: "The inventory slide should be an open book, like a catalogue."
**Built.** `notes/_lanes/289/illustration/catalogue.html` — standalone, white card, one canvas, 600×420.
**Renders.** `catalogue-rest.png`, `catalogue-orbit.png` (playwright, device scale 2).

## The object
A thick hardback lying open on the base plate. One book frame `Fb` (world turned PSI = −5° about the
vertical, x across, y along the spine, z up). Each half gets its own frame — `FR = Fb` rotated +5°
about `Fb.y`, `FL = Fb` turned 180° then rotated +5° — so **both halves are modelled with identical
local geometry**, x from 0 at the spine to 100 at the fore-edge, each 5° up from flat. That is the V.

Per half: a **board** (box, 6-unit square/overhang); a **page block** — a convex wedge prism, section
`(0,TB) (Wp,TB) (Wp,TB+13) (0,TB+17)` in the x–z plane, thicker at the spine, extruded head to tail;
and the **top page**, which is *not* a solid but a swept surface `zPage(x) = zLin(x) + 5.6·(1−x/26)²`
— a cylinder segment at the gutter flattening to the block's own plane by x = 26. A narrow spine box
bridges the boards; a ribbon lies askew on the right half and drapes over the fore-edge.

## The catalogue content
3 columns × 4 rows of plain rectangles per page, each with a short caption rule under it, no letters.
**Every card edge is sampled on the page surface**, so the gutter column visibly bows with the curl
instead of floating over it. At 600×420 a card is ~45 × 29 CSS px — crisp, and the only thing on the
page competing with it is three #C6C6C6 rulings near the gutter, which is deliberate.

## Idiom compliance
- **#111 hairline** visible ink; hidden line, not wireframe. Per-face back-face test, silhouette /
  hard-crease edges only, painter's order by centroid depth, fill white then stroke — the arm's and
  callipers' method verbatim, `polyP` included.
- **#BDBDBD dashed** for runs that *explain*: the base plate behind the book (5 runs), and each
  board's far long edge carried straight on under its own page block (1 run) — ray-vs-primitive slab
  clip, transitions bisected to sub-pixel.
- **#9B9B9B dash-dot**: the spine axis, sited at board level so it is genuinely buried in the blocks
  and comes back dashed there. The axis is drawn, not asserted.
- **#C6C6C6**: page edges on the fore-edge and on head and tail (books.html convention).
- **ONE red #DA1A00**: the outline of the top-left card on the right-hand page.
- Yaw 35 / pitch 20 rest, ±25 / ±12 damped orbit, tau 1.0 s, stays where the mouse left it. No idle.

## Iterations (5 looks)
1. PSI = −36 put the spine straight at the camera; the book read flat. 2. Re-sited to −12; good, but
head/tail page hatching was on the wrong cap (capLo is the *near* end) and the gutter was 68 units of
blank — fixed, Lg 34→26. 3. Ribbon at 4.6 units wide read as a page rule — remade as a filled,
askew strip that occludes the print under it. 4. PSI = +15 fixed the orbit but cramped the rest view.
5. PSI = −5 settled it: the resting 3/4 is open, and the flat pose now sits outside the reachable
orbit except at the extreme right-mouse corner.

Probes: `catStats()`, `catView()`, `catRuns()`, `catSetMouse(x,y)`, `catStill()`.
5 primitives, 40 vertices, 15 faces drawn / 15 culled, 45 edges inked.
