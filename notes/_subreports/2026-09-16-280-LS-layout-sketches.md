# #280 lane LS — four layout sketches (strata · shells · floors · orbits)

2026-09-16 · lane LS (Opus 5) · sketches for Dave's eye, not a build of the explorer.

## In plain prose

Dave asked to be shown ideas rather than given a build, and said that in his mind the layers were
shells rather than rows or columns. This lane drew four shapes for `s277-D8`'s three views — SYSTEM,
DESIGN GOVERNANCE, EXPLANATION — with THE CONSTITUTION beside them rather than among them, and put
them on one page with a single question at the bottom. Every picture is rendered from the real node
data: the drawn node and edge sets come from the page's own predicate (lane LY's `sim.py`) over the
KG embedded in `notes/_KG-EXPLORER.html`, with every family chip on — 4,562 nodes, 7,528 relations,
1,464 of them crossing a view boundary. Sketches 2–4 are sampled to 1,513 nodes and the 2,702
relations among them for legibility, and every caption states the sample.

**Page:** `notes/_lanes/280/layout-sketches/SKETCHES-2026-09-16.html`
**Report:** `notes/_lanes/280/layout-sketches/REPORT.md`
**Store row:** `W-280ls`, owner dave, closes when his export is received.

## The four

1. **Strata** — lane LY's shipped 2D band layout; its never-driven 1280 screenshot is the picture.
   Cost: a switch in the page, already built.
2. **Shells** — concentric spheres, System the core, the two outer shells at 25%, THE CONSTITUTION a
   dimmed ground disc the shells stand on; rendered as a three-quarter view, a cutaway with the
   front half of the outer two shells removed (1,157 nodes left drawn), a dark three-quarter view,
   and a drag-to-turn canvas. Cost: its own lane.
3. **Floors** — three isometric translucent plates, each carrying its view's own force layout flat,
   with THE CONSTITUTION as a fourth plate beside the stack. Cost: a new projection, the cheap one.
4. **Orbits** — the shells flattened to rings, THE CONSTITUTION an arc outside them. Cost: a switch
   in the page; the only one of the four that survives at phone width and in print.

## Findings worth keeping

1. **The 3D force directions are clumped.** Projecting `x3,y3,z3` straight onto a sphere gives a
   blot, not a shell: the first shells render had DESIGN GOVERNANCE as a single tight knot. The
   sketch uses Fibonacci placement with the index handed out in longitude order — even surface,
   ordering kept, spacing given up. Anyone building the real thing inherits this problem.
2. **The 2D force layout parks families in far-off columns** — the assets column near x ≈ 7,500 while
   the rest of SYSTEM lives under x ≈ 0 — so a min–max normalisation piles most of a view into one
   corner of a plate. Percentile rank was used for every flat placement instead. This is the same
   horizontal-emptiness finding lane LY recorded as EX2 §7.1, seen from the other side.
3. **A rejected `clipboard.writeText` is a page error** in a headless context: the first driven run
   logged one. Any export page in this house that copies to the clipboard needs the promise's
   rejection swallowed, or its "page errors []" gate is a coin toss.
4. **Full-page screenshots of a 9,852px page cost 3.5 MB**, which is not a thing to commit with the
   mount at 99%. The viewport shot plus per-section element shots did the same job for 100 KB.

## Gates run

Page errors `[]` and console errors `[]` never driven at 1280×800 light; `localStorage` empty; the
export envelope proved by driving (`{exportedAt, page, answers:{layout:{choice, keep[], note}}}`);
no sideways scroll at 390×844; `node --check` on the page script. Nothing outside
`notes/_lanes/280/layout-sketches/` changed except the `W-280ls` row in `knowledge/_state.json`,
added with `_state.add()` as the brief directs.
