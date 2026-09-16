# LANE LM — REPORT — the explorer's LAYOUT MATRIX: force · strata · shells, each in 2D and 3D, force the default

#280 · 2026-09-16 · lane LM (Opus 5) · **the ruling was inscribed FIRST (`s280-D1`, commit `53a91bd`), then built in three commits** so partial progress survived. Explorer **v1.18**.

## For Dave, in plain prose

You asked for all four sketches plus the original view, in 2D and 3D, with force still the default.
That is what this is. The tool row now carries **two switches instead of one** — `LAYOUT: force ·
strata · shells` and, beside it, `2D · 3D` (the old 3D button, now the matrix's second axis) — and
the six pictures they make are all real, all the same graph, all the same relations. Nothing about
what the graph SAYS changed: no node id, no edge type, no file under `knowledge/` moved. Only where
the dots are put.

**The page still opens exactly as it did.** Force · 2D is the default, and its canvas is pixel for
pixel the 1.17 you already have (§3). Every other cell is one click, or one URL flag, away.

**The contact sheet:** `notes/_lanes/280/layout-matrix/MATRIX-2026-09-16.html` — the six cells in a
3×2 grid, layout by row, dimension by column, one sentence each, nothing to answer. It is for
looking.

### The six cells, one sentence each

1. **Force · 2D** *(the default)* — The graph as it has always stood: one red hub of components with
   the families fanning out around it, the shape found by the force itself and nothing placed by hand.
2. **Force · 3D** — The same cloud lifted off the page and turned, so the depth between the clusters
   is visible and the hub reads as a solid centre rather than a blot.
3. **Strata · 2D** *(sketch 1, shipped at 1.17)* — Three horizontal bands with the Constitution as
   bedrock below them, so a node's layer is simply how high it sits, and every line crossing a
   boundary is a claim leaving one kind of knowledge for another.
4. **Strata · 3D** *(the sketch called FLOORS)* — The same three layers as translucent plates in an
   exploded stack, each floor carrying its own view's map laid flat on it, with the Constitution a
   fourth plate standing beside the building rather than under it.
5. **Shells · 2D** *(the sketch called ORBITS)* — The layers seen from above as concentric rings —
   System the core, Design governance the middle ring, Explanation the outer one, the Constitution an
   arc parked outside them — the one cell that survives at phone width and on paper.
6. **Shells · 3D** *(sketch 2)* — System as a solid core sphere inside two dimmed shells, standing on
   the Constitution's plinth disc, so a ruling's citation reads as a line climbing off the floor into
   the core.

The picture that earns the round is `shots/kg-118-shells-3d-all-light.png`: every chip on, the black
ruling cloud lying on the plinth, and a red bundle of citations climbing off it into the core.

## 1. The ruling, inscribed first

`s280-D1`, by `knowledge/_inscribe_ruling.py` — dry-run, then `--write`. `git diff --numstat
knowledge/_rulings.json` = **19 insertions, 0 deletions**; the module's own reconstruction proof
PASSED (removing the inserted span gives back the original bytes). `notes/_RULINGS.html` re-rendered
the module's own way (`_render_rulings.py`), `--check` reports **FRESH**. Entry kept at
`notes/_lanes/280/layout-matrix/entry-s280-D1.json`.

**One deviation from the brief, declared.** The brief asked for "the two exports" as evidence. Only
one export exists on disk — the sketches export of 20:30Z. His two earlier sentences are recorded in
`notes/_lanes/280/PACE-2026-09-16.md`, so that file is the second evidence pointer (and it was
committed with the ruling, so the pointer cannot rot). The `says` field carries all three of his
sentences verbatim.

## 2. What was built

| Where | What |
|---|---|
| `knowledge/_build_kg_explorer.py` | `prank()` · `floors()` → `xf,yf,zf` · `_ring_place()` + `orbits()` → `xo,yo` · `shells3d()` → `xs,ys,zs`, plus `plates` / `rings` / `shells` blocks in the data. VERSION → **1.18**. `+141 / −2`. |
| `knowledge/_kg_explorer.template.html` | The matrix itself: `LAYOUT` over three values and `three` as the second axis, `?layout=` + `?dim=`, `base()` as the ONE place a cell is resolved, `fit()` reading the live coordinate set and each cell's own furniture, `drawPlates()`, `drawRings()`, `drawShells()`, the outer-shell opacity ramp, cross-layer edge weighting in every non-force cell, `setDim()`, and the layout button cycling. `+115 / −20`. |
| `notes/_KG-EXPLORER.html` | regenerated the module's own way — `python3 knowledge/_build_kg_explorer.py`, nothing else. |
| `notes/_lanes/280/layout-matrix/` | `shots.py` (the screenshots + the per-cell driver probe), `drive.py` (the driven gate + the switch walk), `_build_matrix.py` → `MATRIX-2026-09-16.html`, `shots/` (21 PNG + `shots.json` + `drive.json`). |

**Where each cell's coordinates come from, stated plainly.**

* **Strata-3D (floors).** Three plates at `y −620 / 0 / +620`, each 1,500 world units square; a node
  keeps its own view's force layout, flattened onto the plate by PERCENTILE RANK on each axis (lane
  LS's finding: the force layout parks the assets column near x ≈ 7,500, so a min–max squash would
  pile a whole view into one corner — left stays left, the spacing is given up). The Constitution is
  a fourth plate at `cx +1,950`, `y +310` — beside the building, dimmed, drawn only with its chip.
* **Shells-2D (orbits).** Ring radii System 140…560, Design governance 760…1,040, Explanation
  1,180…1,360, the Constitution an ARC at 1,560…2,180 spanning 0.38…4.02 rad. The angle is the
  node's own force angle `atan2(y,x)`: the cyclic order survives, the spacing is equalised. Each ring
  is sub-divided into as many concentric rows as makes its angular and radial spacing about equal
  (System 18, Design governance 5, Explanation 2, the Constitution 14).
* **Shells-3D.** One sphere per view — System r 620, Design governance r 1,000, Explanation r 1,320 —
  laid out by Fibonacci placement with the index handed out in the order of the node's own longitude
  in the 3D force layout (LS's second finding: the raw 3D directions are clumped, so projecting them
  straight onto a sphere gives a blot). The Constitution is a sunflower disc — the plinth — at
  `y +1,560`, radius 1,560. Outer shells are drawn at 55% (design) and 40% (explain) of their alpha
  so the core reads through them.

## 3. Gate — the default is 1.17, to the pixel

The control is a **like-for-like rebuild**, lane LY's §3 method: HEAD-at-lane-start's builder and
template (`git show 53a91bd:…`), run against **today's** data with only its ROOT and its template
path redirected. It has to be like-for-like because `_rulings.json` moved DURING this lane — this
lane inscribed `s280-D1` into it — so a naive "1.17 file vs 1.18 file" diff would read as if the
layout had moved things it did not.

`sim.py` (lane LY's re-implementation of the page's own draw predicate) over both pages:

| chips | nodes | relations | drawn-node set | drawn-edge set | x,y of every drawn node | x3,y3,z3,deg |
|---|---|---|---|---|---|---|
| page defaults | 1050 = 1050 | 1,642 = 1,642 | 1001, same set | 1,175, same set | **0 moved** | **0 moved** |
| + assets | 1738 = 1738 | 2,945 = 2,945 | 1689, same set | 2,462, same set | **0 moved** | **0 moved** |
| + Constitution | 3217 = 3217 | 4,910 = 4,910 | 3168, same set | 4,432, same set | **0 moved** | **0 moved** |
| every chip on | 4618 = 4618 | 8,086 = 8,086 | 4569, same set | 7,535, same set | **0 moved** | **0 moved** |

Over the WHOLE node list, not only the drawn set: of 4,630 nodes, **0** have a different `x`, `y`,
`x3`, `y3`, `z3`, `y2`, `view`, `deg`, `born` or `died`; the edge list and the `bands` block are
byte-identical.

**Canvas identity.** Control page and 1.18, both at page defaults, both light, both 1280×800, fresh
contexts: `cv.toDataURL()` md5 **`716028a29c…` = `716028a29c…`**. The shipped default of 1.18 is 1.17.

## 4. Gate — the per-cell driver: every node inside its own layer

One probe, used by BOTH the screenshots and the driven runs (`shots.py: PROBE`), reads each node's
resting place through the page's own `base()` and measures how far outside its layer it is.
**Tolerance 1.0 world unit** (every placement is baked and rounded to 0.1, so the real figure is the
rounding). Per cell: strata-2D against its band's `[y0,y1]`; strata-3D against its plate's height and
its ±750 square; shells-2D against its ring's `[r0,r1]` and, for the Constitution, its arc; shells-3D
against `| |p| − r |`, and for the Constitution against the plinth's height and radius.

**Result: 0 nodes out of layer, 0 nodes with no layer, in every cell** — in all 16 never-driven
screenshot contexts and at all 10 steps of all six driven passes. The worst distance seen anywhere is
**0.07** world units (shells-3D, the rounding).

## 5. Gate — driven, per cell (`shots/drive.json`)

Each of the six cells, in its own fresh context, opened by URL flag and then driven: Constitution
chip on → off · dig `component:button` (panel renders) · Escape · scrub 12 days back and home ·
search "button" → fly → focus · Escape. The driver invariant is re-checked after every move.
**All six cells: 10 steps, 0 out-of-layer steps, page errors `[]`.** Dig, scrub, legend, search and
fly work in every cell — no cell has to be declared partial.

The **switch walk**, one context, never reloaded: force-2D → force-3D → strata-2D → strata-3D →
shells-2D → shells-3D → back to force-2D. The button pair reads correctly at each stop, 0 out of
layer at each stop, and at home **every node is back at its `oy`** (`maxOffsetFromForce` = 0). Page
errors `[]`.

## 6. Screenshots — `notes/_lanes/280/layout-matrix/shots/`

21 PNG, each in a **fresh `browser.new_context`**, colour scheme emulated, the cell chosen by URL
flag rather than by a click, with `Object.keys(localStorage) == ['kg-theme']` and page errors `[]`
recorded for every one. Twelve at 1280×800 (the six cells, light and dark), three at 390×844 (the
three 2D cells, light — the 3D cells are not offered at phone width as a photograph because they
rotate), three extras with every chip on (strata-3D, shells-2D, shells-3D), the like-for-like
control, and the contact sheet at 1280 and 390.

What I saw, by eye. **Force-2D/3D** — unchanged, and the 3D cloud still the crowd-pleaser.
**Strata-3D** — the exploded stack reads immediately as a building: EXPLANATION's plate empty at the
defaults (its chip is off, which is the truth), DESIGN GOVERNANCE's plate empty likewise, SYSTEM's
plate carrying the red component map, and with every chip on the plates fill and the cross-plate
lines become the traffic between floors. **Shells-2D** — a target: the red hub as the solid core,
the rings drawn as annuli in their own tints, the Constitution's arc outside, and at 390 it still
reads. **Shells-3D** — with every chip on this is the best picture the graph has produced: the black
ruling cloud lying flat on the plinth, the core sphere dense and legible through the two dimmed
shells, and the citation bundle climbing off the floor into it.

## 7. Not done, or done differently, with size

1. **The shells-3D CUTAWAY toggle is DECLARED OUT.** The brief offered it "if cheap". It is not
   free — it needs a button, a hemisphere predicate in `dot()` and `pick()`, and its own driven gate
   — and the opacity ramp already does the job it was for (the core reads through the outer shells).
   ~25 lines plus a gate if it is wanted.
2. **The 3D cells spin by default**, as they have since v1.0 (`spin` is on). Their canvas md5 is
   therefore not a meaningful identity gate — it happened to be stable across runs here, but nothing
   guarantees it. The driver check, which reads resting coordinates, is the gate for those cells.
3. **The dimension switch SNAPS**, like the layout switch: positions are set straight to the new
   set and the stage re-fits, so a screenshot is the real thing as soon as the page settles. Before
   1.18 the 3D button tweened. A tween that re-fits mid-flight is a non-deterministic screenshot.
4. **The ghost layer is dropped in every non-force cell**, not only in strata (1.17's rule, widened):
   an edge to a switched-off family is a long diagonal smear across plates or shells that reads as
   traffic which is not in fact drawn. In force it is untouched.
5. **Off-layer node ghosts are still drawn** at alpha 0.05 wherever their cell puts them — in
   strata-3D and shells-2D that is a faint cloud outside the fitted picture (the Constitution's
   plate/arc with its chip off). It is 1.16's behaviour, not new, and switching its chip on brings it
   into the picture properly.
6. **Phone width: 2D only.** The three 2D cells are photographed at 390 and have no sideways scroll;
   the 3D cells work there but are not offered as a still.
7. **Equal plate sizes, equal ring bands.** Explanation (171 nodes) gets the same plate and the same
   ring thickness as System (1,750), so it is sparse. Sizing a layer to its content is a few lines in
   `floors()` / `orbits()` if Dave prefers it — the same declared gap as 1.17's equal band heights.
8. **The `bands`, `plates`, `rings` and `shells` blocks are four blocks, not one.** They could be one
   `layers` block with a per-cell geometry; four blocks kept the 1.17 strata code untouched, which is
   what made the pixel-identity proof cheap.

## 8. Gates run

* `node --check` on the template's script before every build (three times).
* `python3 knowledge/_validate_kg.py` and `python3 knowledge/_validate_lane_ownership.py` — appended
  below with the shipped sha.
* `_state.check()` green after closing `W-280ls` and adding `W-280lm`.
* Disk: `/sessions` at 99% throughout. Nothing was downloaded, `knowledge/` was never copied, and
  Chromium came from `knowledge/_render/seat_env.sh` only. Scratch lived in
  `/sessions/intelligent-serene-curie/mnt/outputs/lm/` (the 1.17 control page and its patched
  builder, ~7 MB) and is removed at the end.

## 9. Shipped

* `53a91bd` — `s280-D1` inscribed (the ruling, `_RULINGS.html`, the entry, the export and the pace note).
* `b5df9c9` — explorer **1.18a**: strata-3D (floors) and the two-axis switch.
* `eddf87a` — explorer **1.18b**: shells-2D (orbits).
* `c3805ec` — explorer **1.18**: shells-3D, the contact sheet, the report, the subreport and the store rows
  (`W-280ls` closed with a receipt naming Dave's export file; `W-280lm` and `W-280lf` opened).

`_validate_kg.py` rc 0 ("OK — every ref parses+resolves, every null carries a note, every meta has
provenance, edges match schema, gen_kg_edges.py is idempotent-clean"); `_validate_lane_ownership.py`
"LANE OWNERSHIP: OK — no staged path under another session's lane (this is #280)";
`_render_rulings.py --check` FRESH; `_gen_chain.py` regenerated (the store row tripped the chain gate).
Nothing pushed.
