# LANE LS — REPORT — four sketches of the graph as three visible layers, on one page

#280 · 2026-09-16 · lane LS (Opus 5) · **these are sketches, not a build.** Nothing in the explorer
changed to make them: `knowledge/_build_kg_explorer.py`, `knowledge/_kg_explorer.template.html` and
`notes/_KG-EXPLORER.html` were read for their data and left exactly as lane LY shipped them.

## For Dave, in plain prose

You said the layers were shells rather than rows, and that you wanted to see a few ideas rather than
have one built. So there are four, on one page, and each one is a real picture of the real graph —
every dot is a node and every line a relation, taken from the explorer's own draw predicate with
every chip switched on, so what you are looking at is 4,562 nodes and 7,528 relations' worth of
truth rather than a diagram of an idea. Where a sketch would have gone to mud it is sampled, and the
caption says by how much: 1,513 nodes and the 2,702 relations between them, keeping every
Explanation node, every Design-governance node and every node that carries a line across a boundary,
because the crossings are what the picture is for.

**The page:** `notes/_lanes/280/layout-sketches/SKETCHES-2026-09-16.html` — one row per sketch, the
pictures large, two sentences each, then the radio, the keep-as-a-second-view boxes, the note field
and an export button.

The three layers are the same three every time — System (what exists), Design governance (what a
design must do), Explanation (why) — and **The Constitution is never one of them**: it is the ground
disc in the shells, the plate beside the stack in the floors, the arc outside the rings in the
orbits, and the bedrock band in the strata.

## The four, each in its two sentences

**1 · STRATA** — Three bands stacked top to bottom, so a node's layer is simply how high it sits on
one flat stage — and every line that leaves a band is a claim crossing from one kind of knowledge to
another. It is the cheapest of the four: a switch in the page, built and shipped today behind
`LAYOUT · FORCE / STRATA`, with the old force layout still what the page opens with.

**2 · SHELLS** — System is the solid core, Design governance the shell wrapped round it, Explanation
the shell round that, and the Constitution the ground disc all three stand on, so depth rather than
height tells you which layer you are in and a citation from the record reads as a line climbing off
the floor into the core. It costs its own lane: the file already carries a 3D position for every
node, but shells, a plinth, a cutaway and a rotation the mouse can drive are a new way of placing
and drawing them, not a setting.

**3 · FLOORS** — Three translucent plates in an exploded stack, each floor carrying its own view's
force layout laid flat on it, so every layer stays a readable map of itself while the cross-floor
lines show the traffic between them — and the Constitution is a fourth plate standing beside the
building rather than under it. It costs a new projection, the cheaper one: the plates reuse the x
and y the builder already computes, so the work is the isometric and the plate furniture, not a new
layout.

**4 · ORBITS** — The shells seen from above: System at the centre, Design governance the middle ring,
Explanation the outer ring and the Constitution an arc parked outside them, each ring keeping the
order the force layout gave it so neighbours stay neighbours. It costs a switch in the page, the
same class of change as strata — only each node's radius and angle move — and it is the one of the
four that survives at phone width and on paper.

## What was built here

| Where | What |
|---|---|
| `_sketches.py` | The renderer. Loads the KG embedded in `notes/_KG-EXPLORER.html`, takes the drawn node and edge sets from lane LY's `sim.py` (the EX2 §3 re-implementation of the page's own predicate) with every family chip on, samples for legibility, and writes five SVGs + `facts.json` + `shells-live.json`. |
| `_build_page.py` | Inlines those SVGs into `SKETCHES-2026-09-16.html`, with the prose, the radio set, the keep boxes, the note and the export. |
| `sketch-*.svg` | shells (three-quarter, light) · shells (cutaway, light) · shells (dark) · floors (light) · orbits (light). Sketch 1's picture is lane LY's shipped screenshot, referenced at `../layout/shots/kg-117-strata-all-light.png` rather than copied. |
| `shots/` | `page-1280-light.png` (never driven), `page-390-light.png`, `shots.json`, `drive.json`. |

**Where the coordinates come from.** Nothing new is solved. The shells put each node on its view's
sphere by Fibonacci placement, with the Fibonacci index handed out in the order of the node's own
longitude in the builder's 3D force layout; the floors and the Constitution plinth lay each view's
own 2D force layout flat; the orbits keep the cyclic order of the 2D force angle and equalise its
spacing. The palette is the explorer's: node colour by type, line colour by edge family, the four
layer tints from `BANDFAM`.

**Two honest deviations, both because the raw layout is not evenly spread.** (1) The 3D force
directions are clumped, so projecting them straight onto a sphere gives a blot rather than a shell —
hence Fibonacci placement ordered by longitude, which keeps the ordering and gives up the spacing.
(2) The 2D force layout parks whole families in far-off columns (the assets column sits near
x ≈ 7,500 while the rest of System lives under x ≈ 0), so a min–max squash would pile most of a view
into one corner of its plate; the flat placements use percentile rank instead — left is still left,
near is still near, only the spacing is given up. Both are stated in the code and both are one line
to reverse if the real thing is ever built.

## Gates

* **Page errors `[]`** and **console errors `[]`** in a fresh, never-driven 1280×800 light context;
  `Object.keys(localStorage)` is `[]`; all five inline SVGs present, the sketch-1 photograph loaded,
  5 radios and 4 checkboxes, page height 9,852px (`shots/shots.json`).
* **Driven** (`shots/drive.json`): dragging inside the live frame changes the canvas (its data URL
  changes), then radio → shells, keep → strata + orbits, note typed, copy pressed, and the envelope
  read back off the page is exactly
  `{"exportedAt":…,"page":"SKETCHES-2026-09-16","answers":{"layout":{"choice":"shells","keep":["strata","orbits"],"note":"the shells are what I meant"}}}`.
  Page errors `[]` — the first driven run raised one, a rejected `clipboard.writeText` in headless,
  and the handler now swallows it.
* **Phone**: at 390×844 there is no sideways scroll.
* `node --check` on the page's script before the build.
* Disk: `/sessions` at 99% throughout. Nothing downloaded, `knowledge/` never copied, Chromium only
  via `knowledge/_render/seat_env.sh`; scratch lived under `/sessions/…/outputs/ls/` and is removed.
  The 3.5 MB full-page screenshot the first shot run produced was deleted rather than committed.

## Not done, declared

1. **The live canvas is shells only**, and it does not spin by itself — a rotation running at load
   would make the never-driven screenshot non-deterministic. Drag turns it; that is all it does.
2. **No dark version of floors or orbits.** 3D is the crowd-pleaser, so the one dark render went to
   shells, per the brief.
3. **No hit-testing on the sketches.** Nothing is clickable and nothing has a tooltip: they are
   pictures. Dig, search and scrub all live in the explorer and none of them was touched.
4. **The sampling is the honest cost of legibility.** The full 4,562-node draw is in sketch 1's
   photograph, which is not sampled; sketches 2–4 are, and every caption says by how much.

## Shipped

Commit `SHA`. Store row `W-280ls` (owner: dave; closes when Dave's export is received).

---
The three views and THE CONSTITUTION are `s277-D8`.
