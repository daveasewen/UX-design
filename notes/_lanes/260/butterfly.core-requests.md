# #260 lane F4 (butterfly-h + butterfly-v) — core requests for `knowledge/canon/dv-render.js`

Filed, not made. This lane wrote the smallest local workaround in its own partial and did not
touch the core.

## 1. SECONDING dv-render-donut's request: let a type opt out of the cartesian furniture

`dvRender` calls `furniture(ctx, …)` unconditionally before `draw(ctx)`, and there is no switch.
`dv-render-donut` opens with `ctx.out.length = 0` to throw away furniture the core has already
pushed; **`dv-render-butterfly` now does exactly the same thing, for a different reason, which is
the point** — two independent types have now paid for the same discard, so it is a seam and not a
donut quirk.

Requested change, verbatim (unchanged from #259 lane D, so the two requests merge rather than
compete): *"Let a type partial opt out of the cartesian furniture — honour `fn.axis = "none"` (or
`fn.furniture = false`) in `dvRender` by skipping the `furniture(ctx, …)` call, the way `fn.axis` /
`fn.domain` are already honoured."*

**Why the butterfly needs it, and it is NOT the donut's reason.** A butterfly's domain is symmetric
(`[-M, +M]`) so that both wings share one scale. The core's furniture then labels the lower/left
half of the axis with NEGATIVE numbers — a tick reading `-40` under a wing whose value is 40. The
donut discards furniture it does not need; the butterfly discards furniture that would be **wrong**.
Both reference implementations also draw no gridlines at all by ds-020 declaration, gated green at
#95, so the discard is not a redesign either.

## 2. NEW: the core has no way to say "this axis is a MAGNITUDE, not a signed value"

The narrower shape of request 1, and the one that would let a butterfly keep the core's furniture
instead of re-emitting its own. `furniture()` formats every tick with `ctx.fmt(t)`, and `ctx.fmt`
is fixed by the core before `draw(ctx)` runs, so a type partial cannot intercept it.

Requested change, verbatim: *"Let a type partial supply a tick formatter — honour
`fn.tickFormat = fn(spec, value)` (defaulting to the core's `fmt`) so a type whose domain is a
mirrored MAGNITUDE can label a tick with `|value|`. Today the only way to get honest tick labels on
a symmetric domain is to discard the furniture and re-emit it, which is 600 bytes of duplication per
such type and a second place for the axis grammar to drift."*

Not urgent for this lane — butterfly draws no ticks at all, by ruling — but it is the difference
between "no value axis by design" and "no value axis because the engine cannot label one".

## 3. NOT re-filed

dv-legend's stale value cache after a re-render (#259 lane D request 2) and dv-donut-sweep's
missing re-entry point (request 3) both still stand. Neither is re-filed here: the butterfly emits
no `data-tip-value` and no sweep, so this lane has no independent evidence to add and re-filing a
request twice would only make it look like two.
