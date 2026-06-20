# Brand refresh — direction (FUTURE / EXPERIMENTAL)

> **Status: not active. Do NOT apply to the component canon, tokens, or gated reference snippets.**
> This is a forward-looking design direction for an in-progress HSBC brand refresh. Per Dave (2026-06-19):
> bag it now for continuity, but use it **only as experimentation when we reach full compositions and
> journeys** — never on individual components yet. A *refresh, not a reset* — see the consistency principle.
> Deliberately kept OUT of `guidelines/` so it is not picked up by the component RAG/generation layer.
> Pair with the **Swiss-design skill** when playing with these at the composition level.

## The cheat-sheet (8 principles)

1. **Typography should be elegant** — larger and thinner; considered, with clear hierarchy. Fewer weights, simpler usage rules.
2. **Boxes within boxes** — avoid boxy designs (the "HSBC of old" feel). Consider removing frames; make components full-width with generous internal padding.
3. **Refined asset selection** — photography complements the layout, doesn't complicate it. Use icons sparingly (avoid icon overload — consider text instead). Pictograms must carry specific meaning; no visual assets for their own sake.
4. **A blurred background isn't "supercharge"** — a blur alone doesn't make a design supercharged; layout, spacing and type hierarchy still have to do the work.
5. **Flexibility is key** — the foundations are fixed, but components and layout should flex to customer and business needs.
6. **Breathing space** — give elements room to be heard; generous spacing where appropriate; use negative space to lead the eye.
7. **Logical, tactile interactions (CD)** — interactions mimic the real world: buttons feel pressed; things move the way they would in 3D space.
8. **Consistency remains a constant** — this is a refresh, not a reset; the experience stays consistent across the entire HSBC eco-system (internal and external).

## Candidate direction — icon weight system (outline icons)
From the Tags cross work (2026-06-19): an icon's **line weight can mirror the adjacent font weight**, so
icons read as members of the type family, held **constant across sizes** via `vector-effect:non-scaling-stroke`
(one variable `--is` drives both the type weight and the icon stroke). Proof of concept:
`_fitness-test/icon-weight-system.html`. **Requires icons drawn as single centerline STROKES.** Verified 2026-06-19: the HSBC set is **0/658 stroked —
every icon is `fill`**, including the outline-STYLE ones (their "outline" is a thin *filled ring*, not a stroke).
So the weight system is NOT a CSS switch on the current artwork — there's no `stroke-width` to vary. Routes:
(a) re-author icons as true centerline strokes (then stroke-width + non-scaling-stroke work as in the demo), or
(b) ship per-weight icon artwork (light→bold versions) — both icon-LIBRARY decisions; or
(c) **FAKE it on the existing filled icons via an in/out stroke** (Dave's idea, prototype `_fitness-test/icon-fake-weight.html`):
    add a stroke to the filled path — `stroke:currentColor` (icon colour) extends the fill → heavier; `stroke:<bg colour>`
    erodes it → lighter; width sets the amount. Needs NO re-authoring. CAVEATS: the "lighter" (bg-colour) stroke only
    works over a SOLID, KNOWN background (breaks over imagery/gradients); strokes are edge-centred (~half-effective,
    both contours of compound icons thicken); sub-pixel strokes anti-alias differently per browser. FIX for the bold-end faceting (Dave): the
    icon runs edge-to-edge in its viewBox, so a heavy stroke spills past the box and gets clipped (flattens curves
    into facets) — scale the icon DOWN within its container (~80%, `transform-box:fill-box; transform:scale(.8)`)
    so the outward stroke has room. Strong candidate for a CSS-only weight axis where backgrounds are controlled. Fits refresh principles
1 (elegant/thinner type) + 3 (refined, sparing icon use). NB: default icons are outline-style, active = solid —
use the outline (non-`*-active`/`*-solid`) file for default states (fixed in Tooltip 2026-06-19).

## How this intersects what we've built
- The **motion themes** draft (`_MOTION-THEMES.md`) — especially "Tactile / press physics" — already aligns with principle 7; that's a natural bridge when we experiment.
- Principles 2 + 6 (de-frame, full-width, breathing space) are **composition/layout** moves, not component-token moves — which is exactly why they're scoped to compositions/journeys, not the current component work.
- When the refresh formally lands it will likely touch tokens (type scale, spacing) and component framing; revisit the gated references + tokens then, not before.
