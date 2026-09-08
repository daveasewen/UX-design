# Core requests — dv-render.js, from #260 lane F3 (CANDLESTICK)

Verbatim, for the core owner. A type lane must not make these itself. Both are worked around inside
`dv-render-candlestick.js`, so nothing is blocked — but request 1 is now on its **third** reporter
and is the only one of the three that could not simply be lived with.

## 1. ⛔ THE ZERO CLAMP RUNS AFTER `fn.domain`, SO NO TYPE CAN ESCAPE IT

`dv-render.js`, in `dvRender()`:

```js
if (typeof draw.domain === 'function') { v = draw.domain(spec); lo = v[0]; hi = v[1]; }
else { …min/max of every value… }
if (lo > 0) { lo = 0; }                      /* dv-bar-009 — the baseline is zero, always */
```

Requested change, verbatim:

> "Honour a type's own domain. `fn.domain` is the seam a type uses to say what its value axis
> means, and the zero clamp on the line after it silently overrules every answer it can give. Make
> the clamp a property of the TYPE, not of the engine — `fn.zeroBaseline !== false` (default true,
> so every bar-family type is unchanged) — or apply the clamp only in the `else` branch, where the
> engine is guessing rather than being told. dv-bar-009 is a BAR rule: a bar's length IS its value,
> so it must start at zero. A price is a POSITION on a scale, and a candlestick, a line and a
> scatter all have to be free to scale to their own extent."

**MEASURED, not asserted.** The promoted Chart-candlestick series runs 90.41 → 108.52. Against the
partial's own scale the ticks are 90 / 95 / 100 / 105 / 110 and the candles fill the 216px plot;
against the core's zero-floored scale the same data occupies the top **17%** of the box and every
body collapses to a hairline. Driven in Chromium, 8/8 theme × mode combinations, with the partial's
own scale.

**THIS IS THE THIRD REPORT OF ONE DEFECT.** `dv-render-line.js` reported it and left it alone (its
zero-based line matched the promoted snippet, so nothing regressed). `dv-render-sparkline.js` filed
it and scaled to its own extent instead. This lane had no third option: there is no honest
candlestick with a zero baseline. Each work-around costs the same ~14 lines — the type computes
`nice(lo, hi, 4)` itself, discards `ctx.out`, and re-emits gridlines, tick labels and the baseline
against the scale it actually drew — and each copy is a place the three can drift apart.

## 2. The accessible name is the core's and a type cannot contribute to it

`autoLabel(spec)` enumerates every series × category, capped at 12 categories. For a candlestick
that is **48 phrases** ("Open S1 101.25, High S1 102.06, Low S1 99.75, Close S1 100.59, Open S2 …")
— truthful, and not a sentence anyone can listen to. ds-027's promised summary is the range, the
open and the close. Requested change, verbatim:

> "Let a type partial own its accessible name. Either honour `fn.label = fn(spec)` alongside
> `fn.axis` and `fn.domain` — the core keeps `spec.label` as the author's override and falls back
> to `autoLabel` when neither exists — or expose `ctx.setLabel(s)` on the context. A type knows what
> its own chart says; the core only knows what numbers are in it."

**Work-around in place, and it is not clean:** the partial writes `ctx.spec.label` and marks it with
a `__dvLabel` flag so an author-supplied label survives and the partial's own sentence refreshes on
every re-render. It mutates the caller's spec object, which nothing forbids and nothing sanctions.

Driven result with the work-around, mono/light and the other seven combinations identically:

> "Share price, open high low close, forty sessions, pounds. Ranges from a low of 90.41 to a high of
> 108.52, opening 101.25 and closing 106.16 across 40 sessions."
