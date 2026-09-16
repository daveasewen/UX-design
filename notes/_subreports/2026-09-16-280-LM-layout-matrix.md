# #280 lane LM — the explorer's layout matrix (force · strata · shells × 2D · 3D), explorer 1.18

2026-09-16 · lane LM (Opus 5) · `s280-D1` inscribed first, then built in three commits.

## In plain prose

Dave's word on the four sketches was: keep all of them, plus the original view, in 2D and in 3D, and
keep force the default. That is a MATRIX, not a fifth sketch — three layouts by two dimensions, six
cells, one switch — and it is what `s280-D1` says and what explorer 1.18 is. The four sketches map
onto the matrix without remainder: STRATA-3D is the sketch called FLOORS and SHELLS-2D is the sketch
called ORBITS, so nothing he asked for is missing and nothing new was invented to fill a hole.

Storage is untouched: no node id, no edge type, no file under `knowledge/` changed. What changed is
where the dots are put, and the page's tool row, which now carries both axes — `LAYOUT: force ·
strata · shells` and `2D · 3D` — plus `?layout=` and `?dim=` so any cell can be photographed without
the page ever being clicked.

**Ruling:** `s280-D1` · **Report:** `notes/_lanes/280/layout-matrix/REPORT.md` ·
**Contact sheet:** `notes/_lanes/280/layout-matrix/MATRIX-2026-09-16.html` ·
**Store rows:** `W-280ls` closed (his export received), `W-280lm` opened (closes on his word on the
contact sheet).

## The three new coordinate sets, all baked at build time

| Cell | Keys | Placement |
|---|---|---|
| strata-3D (floors) | `xf,yf,zf` | three plates at y −620 / 0 / +620, 1,500 units square, each carrying its view's own force x,y flattened by PERCENTILE RANK; the Constitution a fourth plate beside at cx +1,950 |
| shells-2D (orbits) | `xo,yo` | annuli 140…560 / 760…1,040 / 1,180…1,360, the Constitution an ARC at 1,560…2,180 over 0.38…4.02 rad; angle = the node's own force angle, order kept, spacing equalised, sub-rings chosen so angular ≈ radial spacing |
| shells-3D | `xs,ys,zs` | Fibonacci placement on spheres r 620 / 1,000 / 1,320, the index in the order of the node's own 3D longitude; the Constitution a sunflower plinth disc at y +1,560, r 1,560; outer shells at 55% / 40% alpha |

`x`, `y`, `x3`, `y3`, `z3` and `y2` are not touched — which is what makes the default provable.

## Findings worth carrying

1. **A "nothing moved" proof has to be like-for-like, and this lane is the second lane in two to hit
   it.** `_rulings.json` moved DURING the lane because the lane itself inscribed `s280-D1` into it,
   so the shipped 1.17 page and the new 1.18 page differ at page defaults by the GHOST edges of the
   new ruling (an edge to a switched-off family is drawn at alpha 0.04, so a data change shows in a
   default screenshot even though nothing of it is "drawn"). The control has to be HEAD's builder run
   against today's data. Lane LY recorded the same class at #280; it is now twice, which makes it a
   habit rather than an accident.
2. **One `base()` is the whole matrix.** Six cells could have been six code paths; instead every cell
   is resolved in ONE function that returns a node's resting triple, and `fit()`, the dig, the
   surface, the search-fly and the two switches all read it. The per-cell gate then has a single
   thing to probe, and the probe is shared by the screenshots and the driven runs — one driver, never
   two.
3. **A spinning 3D view has no canvas-md5 identity gate.** `spin` is on by default, so a 3D cell's
   pixels are a function of when the screenshot fired. The resting-coordinate driver is the honest
   gate for those cells; the md5 gate belongs to the 2D ones.
4. **The 3D cells' furniture has to be world-space, not screen-space.** The plates, the ring annuli
   and the plinth are sampled in world coordinates and projected point by point, so they rotate and
   foreshorten with the graph. A screen-space rectangle would have been cheaper and would have lied
   the moment the cloud turned.

## Declared out

The shells-3D **cutaway toggle** (offered "if cheap" in the brief). It needs a button, a hemisphere
predicate in `dot()` and `pick()`, and its own driven gate; the outer-shell opacity ramp already
delivers what it was for. ~25 lines plus a gate if Dave wants it.
