# 289 · I1 — the brain, in the gearbox's line-drawn 3D style

provenance: Dave, 2026-09-20, on proposal v2 — "I really like the 3d illustration style we
have for the gears, maybe we have a brain in the same style somewhere. maybe a stack of
books too." Books are another lane. Source idiom: the v7.5 gearbox art-direction note in
`notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html` (script ~1303–2133).

**Built** `notes/_lanes/289/illustration/brain.html` — standalone, white card, one `<canvas>`,
plain 2D, no libraries. Shot at 600×420 CSS px, device scale 2: `brain-rest.png`,
`brain-orbit.png`.

## Approach

Three parametric bodies, no mesh. **Cerebrum**: an ellipsoid r(t, ψ) — t occipital→frontal,
ψ around it, ψ=0 the top midline — carrying a shallow sinusoidal sulci displacement (amp
0.058 r, 10 waves along t, tilted 2.2 waves around ψ) so every contour line picks up the
gyral wave, plus a gaussian groove at ψ=0: the longitudinal fissure. **Cerebellum**: a
smaller, flatter ellipsoid below and behind, drawn as ribs — its foliation — and nothing
else. **Brainstem**: a short cylinder, two silhouette lines and an end ellipse, exactly as
the gearbox draws a shaft.

Drawn as contour lines, not wireframe: every sample is kept only where the surface normal
faces the camera (n · grad(depth) > 0), so the far half of each body is simply not inked.
Silhouettes are found where that test changes sign, then taken as the outer radial hull of
the crossings about the projected centre, median-of-three smoothed.

Camera, mouse and colours are the gearbox's verbatim: rest yaw 35 / pitch 20, orbit ±25°
yaw / ±12° pitch, critically damped τ = 1.0 s, stays where the mouse left it; #111 hairline,
#BDBDBD dashed, #9B9B9B dash-dot, one #DA1A00 accent on white. Mounted: a base-plate outline
and one dash-dot axis through the stem. Probes: `brStats()`, `brView()`, `brSetMouse()`.

## Line counts — shipped drawing, at rest

| group | segments |
|---|---|
| cerebrum meridians (17, fissure excluded) | 940 |
| cerebrum silhouette | 154 |
| cerebellum folia (7) + silhouette | 118 + 50 |
| brainstem | 82 |
| **solid total (#111)** | **1 356** |
| hidden, #BDBDBD dashed — the stem behind the cerebellum | 46 |
| construction, #9B9B9B dash-dot — the stem axis | 1 |
| accent, #DA1A00 — the longitudinal fissure | 138 |

For comparison the gearbox runs ~1 700 solid. This is a lighter drawing, deliberately.

## Rejected, and why — all judged by rendering, not by guessing

- **Coronal rings** (`?lat=4`, 1 681 solid — `var-H-lat4.png`). Meridians *and* rings makes a
  segmented melon: the rings read as pumpkin ribs and fight the gyri. Rings alone
  (`var-B-rings.png`) read as a loaf of bread. Shipped meridians alone.
- **17 vs 13 vs 21 meridians** (`var-E`, `var-D`, `var-F`). 13 goes thin over the occiput;
  21 crowds the frontal pole. 17.
- **A pole-cap ring** closing the meridians (`var-A-meridians.png`). Closes the starburst but
  reads as an eyeball stuck on the front. Instead the meridians stop short — harder at the
  frontal pole (0.66 of π/2, it faces the camera) than the occipital (0.88) — and the
  silhouette closes the poles.
- **A deep, narrow fissure** (fd 0.30 / fw 0.20). Seen near edge-on it inked as a dozen
  vertical scratches across the crown. Shallower and wider, 0.17 / 0.30: a valley the red
  line sits in.
- **A second construction axis** down the cerebrum's long axis. It crossed the whole gyral
  field diagonally and read as a scratch on the drawing, not as construction. One axis.
- **Filtering silhouette points before hulling.** Left the bins behind the cerebrum empty and
  the polyline sawed between survivors. The hull is now built from every crossing and
  occlusion is applied per segment.

Trial renders are left beside the page as `var-*.png` (delete is blocked in this sandbox);
they are the density evidence above and nothing else depends on them. No other file touched,
no commit.

---

# Pass two — 2026-09-20

Dave: *"the brain isn't quite right"*, with `DAVE-REF-brain-side-view.png`. He was right —
pass one was an ellipsoid wearing meridians, a melon. It is kept as `brain-v1.html`;
`brain-vs-ref.png` (reference beside render) is how each of the seven rounds was judged.

**The model changed, not the styling.** The cerebrum is a **traced side profile** — 32
control points off the reference, closed centripetal Catmull-Rom — given thickness by a
**signed distance field**: `|l| ≤ WMAX·√(q(2−q))`, `q = min(1, d/DREF)`; flat-sided through
the middle, rolling to zero at the outline. So the **silhouette is the traced profile**,
projected: frontal lobe, occipital bulge and the temporal lobe's front-bottom **notch**
survive every orbit position exactly. The field also copes with that notch, which is
concave — no radial `r(θ)` can, since a ray from any centre crosses it twice.

**Gyri**: ~23 strokes made once in the profile plane — a walk along a line field of arcs
concentric about the Sylvian, wobbled by two-octave noise, tilted per stroke, spaced by an
occupancy grid, 40–120 units, most with one sulcus gap — lifted `+1.2` along the normal and
kept only where that normal faces the camera. One hairline under the red fissure marks the
temporal lobe's upper border; without it the red floated on a wall.

**Kept verbatim:** #111 hairline, #BDBDBD dashed (stem behind the cerebellum), #9B9B9B
dash-dot axis, ONE #DA1A00 accent — the lateral fissure — white card, base plate, damped
orbit τ=1.0 s that stays put. **Rest yaw 20 / pitch 12**, as briefed.

## Rejected, each after a render

- **±25° yaw orbit.** At rest yaw 20 the near edge crosses front-on and the brain flips to
  face the other way. Clamped to ±18 / ±10. The only deviation from the gearbox idiom.
- **A plain sine scallop on the outline.** A brain edge must be lumpy or it reads as a
  bean, but an undetuned sine inks a doily. Shipped: amplitude-modulated, detuned, and
  **damped by local curvature** — a wave deeper than the local radius folds the outline
  into a knot, which tied the temporal notch shut for two rounds.
- **Trusting the crease to hold the silhouette.** It does, except near the poles, where the
  near sheet stands WMAX in front of the rim — ~16 units of sideways shift at yaw 20 — and
  ridges projected *outside* the outline. Cheaper than solving the true horizon: clip every
  surface stroke to the projected rim polygon.
- **RIM = 8 units.** Clear of the edge, but it emptied the thin temporal lobe. RIM = 5;
  the silhouette clip carries the tidiness instead.
- **WOB 1.45 / BIAS 0.5.** Enough wander to kill the concentric swirl, but the strokes went
  uniform — fur, not gyri. 0.9 / 0.26.

At rest: 1 066 solid (260 gyri, 434 outline, 145 folia, 99 cerebellum, 116 stem), 20
hidden, 1 construction, 32 accent. No other file touched, no commit.

---

## Pass three — trace, don't generate

Passes one and two GENERATED a brain. Neither read as one: what says "brain" is not a rule,
it is the particular run of THOSE sulci on THAT outline. Pass three traces the reference.

**Step 1 — trace.** Reference thresholded to ink, skeletonised (skimage), the skeleton walked
into polylines split at junctions, dropped under 12 px, Douglas–Peucker at 1.5 px. The rim
comes separately, as the 8 px iso-contour of the filled silhouette's distance transform — the
centreline of the reference's own heavy outline as ONE closed loop, not the fragments the
skeleton leaves where gyri meet it. Out: 125-point rim, 87 gyri, 31 cerebellar strokes, 4 stem
strokes, and the lateral fissure chained from ten segments running from the temporal notch up
and back. Normalised to cerebrum width 300, origin the cerebrum centroid → `brain-trace.json`;
`brain-trace.png` is that flat, and it is the reference in hairline.

**Step 2 — solid.** Profile plane (a, b), third axis u lateral. Distance field d off the rim on
a 2-unit grid, plus local feature size R = max{ d(q) : |p−q| ≤ d(q) }. Half-thickness
w = WMAX·(R/RREF)^0.75·√(1−(1−d/R)²), WMAX 62. The √ is the elliptical section asked for; the R
term is what one global field could not do — it makes the 20-unit brainstem a rod (R≈10, a
seventh of the cerebrum) with nothing modelled separately. Every stroke sits on the NEAR sheet
at u = +w, inked only where the normal (1, −∂w/∂a, −∂w/∂b) faces the camera, so strokes die
before the rim and the far sheet is never inked. The rim is the u = 0 crease, so the silhouette
IS the trace at every orbit position.

**Idiom kept:** #111 hairline, #BDBDBD hidden (the stem's run up through the body), #9B9B9B
dash-dot (vertical axis, and the solid's horizontal section at b = −78), ONE red #DA1A00 — the
lateral fissure — white card, base plate, damped orbit (tau 1.0 s) that stays put. Rest yaw 15 /
pitch 10, clamped ±20 / ±10. At rest the card is the reference near verbatim; orbiting opens the
section ellipse and slides the gyri off the rim, which is the thickness showing. Trace inlined,
so `brain.html` is standalone. Pass two kept as `brain-v2.html`. No other file, no commit.

## Pass four — the mirror

Dave on pass three: "this has become half a brain in effect, can we just extrapolate the other
half as the mirror image of this." So: pass three copied to `brain-v3.html`, and `brain.html`
made a full solid by reflection about the mid-sagittal plane u = 0.

**The far half is the near half reflected.** Far sheet u = −w(a,b), carrying the SAME traced
strokes at the same (a, b) — which is also the anatomy: the hemispheres are near mirror images.
The red is NOT mirrored; one lateral fissure, near side, one red.

**Hidden line, now real.** A stroke on sheet s has outward normal n_s = (s, −∂w/∂a, −∂w/∂b) and
is inked only where n_s faces the eye AND a march along the view vector does not re-enter the
body (|u| < w inside the rim). That is what keeps the far hemisphere from leaking through, and
what lets it show where it should — through the notch under the temporal lobe and from overhead.

**The outline is solved, not guessed.** On the section normal to the rim the solid is u = ±w(t),
w' → ∞ at t = 0. With Vd = V·(inward normal) the silhouette is w'(t) = s·Vu/Vd, s = sign(Vd) —
one point per rim vertex, continuous, no snapping. Vd → 0 sends t → 0, so the crease IS the
silhouette and the card at rest is still the trace verbatim; a rim turning hard toward the eye
sends the answer onto the FAR sheet, the mirror carrying the outline. Two earlier attempts —
facing-sign on a smoothed grid, then marching squares — both broke the outline into fragments
(worst at the brainstem, where the grid slope and the exact field disagreed); this does not.

**Longitudinal fissure.** The crest of the crease, upper rim at u = 0, #111 hairline, inked
where it is not occluded and has separated from the outline by more than 3 px — so nothing
doubles at rest, it opens as a groove on orbit, and it is the spine in `brain-top.png`.

**Also:** orbit ±25 / ±12 about rest yaw 15 / pitch 10, nothing clamping it; "LATERAL FISSURE"
callout and the grey section ellipse dropped (neither is gearbox idiom). 0.7 ms/frame. Shots
re-rendered at device scale 2: `brain-rest.png`, `brain-orbit.png`, `brain-orbit2.png`,
`brain-top.png`. No other file, no commit.

## Pass five — two hemispheres, one solid each

Dave: the side views are right, the top is not — "two halves in a mirror image". Pass four is
kept as `brain-v4.html`; the fix is the SOLID, not the strokes.

**Each hemisphere is its own solid**, `s·u ∈ [g(a,b), w(a,b)]` — pass four's body with the
midline slab `|u| < g` milled out. The LATERAL sheet stays at `u = ±w`, pass four's surface
untouched, so rest / orbit / orbit2 are unchanged to a hairline (6.5k differing px of 1M,
nearly all of it the new groove). The MEDIAL sheets are the planes `u = ±g`, meeting on the
contour `w = g`, 0.4 units inside the traced rim — the fissure is open right to the outline.
`g` is a FIELD, `6·smoothstep(R)` on local feature size: 6 across cerebrum and cerebellum, 0
on the BRAINSTEM, which stays one cylinder (at `g = 0` the halves close into `|u| < w`). The
fissure being geometry, the synthetic crest line is gone: the groove is the two MEDIAL RIM
EDGES, inked where the march clears both solids — at rest only the crown shows, as a
hairline; pitch over and it opens into the valley.

**The section solve stopped using w'(t) as a proxy.** The exact condition,
`F = Va·∂w/∂a + Vb·∂w/∂b − s·Vu = 0`, is now tracked with the real 2-D gradient. Near the rim
it collapses to pass four's `Vd·w' = s·Vu` (unchanged side views); deep in, where the proxy
was wrong, it finds each hemisphere's lateral CREST instead of fragmenting. One loop per
hemisphere, coincident answers inked once, crest-to-crease jumps left as gaps not chords.
**Rejected:** `±[g, g+2w]` as briefed, and a `1.5w` half-measure — both widen the solid
(ours is half as wide as a real brain) but shift the gyri ~12 px along u. Side views won.
**Also:** "traced · 1:1 profile" removed; `brain-top.png` at pitch **78**, not 70 — at 70 the
270-unit height swamps the 124-unit width and the lobes read as one loaf; `brain-front.png`
added (yaw 80 / pitch 10). No other file, no commit.

## Pass six — width first

Pass five was right in everything but the one thing it named itself — "ours is half as wide as a
real brain" — and kept it thin to leave the side views pixel-identical. Overruled; kept as
`brain-v5.html`.

**Each hemisphere is now the literal half-ellipse of the brief,** `s·u ∈ [g, g + 2w]`: flat
medial face at `u = ±g`, rounded lateral sheet out to `u = ±(g + 2w)`, with `WMAX` halved to 31
so the fattest section is `6 + 2·31 = 68` a side and the pair is **136 across a 300-long
profile** — width 0.45 of length, height ~0.7 of it. Two things fall out with nothing modelled
separately: the cerebellum, whose `d` tops out at ~33 against the cerebrum's 92, comes to **~104
wide**, and the brainstem, `R ≈ 9 < RLO`, keeps `g = 0` and stays **one 19-unit midline
cylinder**. The gyri ride the lateral sheet and move outward with it, which is where they belong.
Housing half-width and the occlusion march's `u` bound follow `2·WMAX + GMAX`.

**Rest re-picked by eye at 10 / 8.** Rendered 8/6, 10/8, 12/6, 12/10 at the new width: 8/6 is flat
but dead, the thickness never announces itself; 12/10 shears the frontal pole and the crown groove
reads as a doubled outline half the length of the skull. At **10 / 8** the near lateral sheet
presents almost square, the outline is the traced profile, the folia stay legible, and the groove
is a single hairline sliver over the crown. Orbit ±25 / ±12 about it, damped, staying put; all
else unchanged. Five shots re-rendered at device scale 2 — `brain-top.png` (pitch 75) now two
lobes ~60 units deep with the groove between; `brain-front.png` (yaw 85) two lobes side by side.
**Rejected:** raising the silhouette jump cut 70 → 110 px, which changed nothing. No other file,
no commit.
