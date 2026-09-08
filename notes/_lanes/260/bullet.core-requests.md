# Core requests — dv-render.js, from #260 lane F3 (BULLET)

Verbatim, for the core owner. A type lane must not make these itself (the brief's fence, and the
#253 defect's lesson). Each is a WORK-AROUND that already exists inside `dv-render-bullet.js`, so
nothing is blocked on them — they are the difference between a partial that opts out and a partial
that pays for something and throws it away.

## 1. `dvRender` calls `furniture()` unconditionally and offers no switch — SECONDED

This is **dv-render-donut's core request 1, arriving for the third time** (donut #259, sparkline
#259, bullet now). Requested change, verbatim:

> "Let a type partial opt out of the cartesian furniture — honour `fn.axis = "none"` (or
> `fn.furniture = false`) in `dvRender` by skipping the `furniture(ctx, …)` call, the way
> `fn.axis`/`fn.domain` are already honoured. Until then a radial type is silently paying for
> gridlines it throws away."

The bullet is the case that makes it awkward to keep refusing: it is a **cartesian** type with
`fn.axis = "x"`, so it wants the furniture *switch*, not the *radial exception*. It reads against
its qualitative bands, never against gridlines — the promoted component has never carried a tick
label — and the bands are opaque greys, so any gridline the core draws is painted over before it is
seen. `ctx.out.length = 0` at the top of the partial is the third copy of the same three-character
work-around in the same group. **Three consumers is a pattern, not a coincidence.**

## 2. A type partial cannot emit furniture *between* the core's furniture and its own marks

Minor, and only visible once request 1 lands. A bullet's zero baseline is furniture that the TYPE
owns (its x position is `vf(0)`, which only the type knows how to want), so it is pushed after the
marks and therefore paints on top of them. Today that is harmless — the baseline is 1px of
`--baseline` at the left edge, and nothing overlaps it. If a later type needs furniture BEHIND its
marks while still opting out of the core's, `ctx` would need a second buffer (`ctx.back(s)`), or
`furniture()` would need to be callable by the partial rather than only by the core. **Not needed
by anything shipping today; recorded so the next lane does not rediscover it.**
