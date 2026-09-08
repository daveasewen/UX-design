# #260 lane F2 — CORE REQUESTS from the BOXPLOT type (verbatim, for the core owner)

⛔ A type lane must not make these. Filed, not enacted. Lane F2 did not edit
`knowledge/canon/dv-render.js`. Where the core lacked something, the smallest local workaround
lives in `knowledge/canon/dv-render-boxplot.js` and is named in the file's header.

---

## 1 — THE ZERO BASELINE IS FORCED ON **EVERY** TYPE, AND dv-bar-009 IS A **BAR** RULE

`dvRender()` does this unconditionally, after a type's own `fn.domain` has already spoken:

```js
if (lo > 0) { lo = 0; }                      /* dv-bar-009 — the baseline is zero, always */
```

dv-bar-009 says *bar-family*; `_validate_dataviz.py` scopes its own check to `BAR_FAMILY`. A box
plot is not in that family, and neither is a candlestick or a bullet. Forcing zero into a
distribution's domain is not a safety net there, it is lost plot: a box plot of systolic blood
pressure (95–180) or of response latency (240–2,100 ms) spends a third to nine tenths of its height
on empty space below the lowest whisker, and every IQR box collapses toward the top of the frame.

**LOCAL WORKAROUND TAKEN:** none. The type accepts the forced zero because the exemplar's data
starts near zero anyway, and inventing an escape hatch in a type partial would be a type lane
editing core behaviour by the back door. **The cost is recorded, not paid.**

**Requested change, verbatim:** *"Scope the zero floor to the types that own it. Honour an optional
`fn.zeroBaseline` on a registered type function — default `true`, so every type behaves exactly as
it does today — and skip `if (lo > 0) { lo = 0; }` when a type declares `false`. It is the same
shape as `fn.axis` and `fn.domain`, which the core already honours, and it costs about 40 code
bytes. `dv-render-boxplot` would declare `false`; `dv-render-bar` would not. Do NOT solve this by
letting a type override `nice()` — the tick machinery is the core's and should stay there."*

---

## 2 — THE SPEC HAS NO WAY TO SAY "NO VALUE HERE", AND AN OUTLIER LIST IS RAGGED

`validate()` requires `one.values.length === c.length` and every entry to be a finite number. That
is right for a bar and it is the whole difficulty for a box plot: **outliers are a ragged list** —
one category has two, its neighbour has none.

**LOCAL WORKAROUND TAKEN, and it is defensible on its own terms:** any series beyond the fifth is an
*outlier candidate*, and a candidate whose value falls INSIDE `[minimum, maximum]` is not drawn —
because a point within the whiskers is not an outlier. That is a definition, not a sentinel, and it
needs no spec change.

**⚠ WHERE IT LEAKS — the a11y spine.** The core's `writeTable` emits one `<td>` per series per
category, so a placeholder still prints a number under a column headed *Outlier*. A table that
misstates the data is worse than a chart that omits a dot, so the **exemplar's data moved rather
than the table lying**: `Chart-boxplot.reference.html`'s Teams B and D gained REAL low outliers
(8 and 3, replacing the two `—` cells), and the "no outlier for this category" case is exercised on
the committed test page `knowledge/_tests/chart-engine/boxplot.html` instead. That is a visible
change to a ruled exemplar and it is called out in the subreport.

**Requested change, verbatim:** *"Let a series value be `null` and mean ABSENT. `validate()` would
accept `null` alongside a finite number; `writeTable` would emit an em dash for it; a type partial
would skip it. That is the ragged-data shape every statistical type wants (an outlier list, a
missing month in a line, a category with no reading), and today each of them has to invent its own
sentinel — which is how two types end up disagreeing about what an absent value looks like. Roughly
60 code bytes across `validate`, `writeTable` and `autoLabel`. This one is spec-shaped as well as
core-shaped: it changes the contract Dave ruled at s249-D4, so it wants his word, not the core
owner's alone."*

---

## 3 — NOT A REQUEST, A NOTE THE CORE SHOULD KEEP

`fitOne()`'s `[data-fx]` pass moves `rect`, `text`, `line` and `g` — **and not a bare `circle`**.
Any type drawing point marks must therefore wrap them in `g[data-fx][data-x0]`, which is what
`dv-render-boxplot` does for its outlier pair (and what the baked Chart-scatter markup already did).
`fitY()` *does* handle `circle[cy]`, so the two passes are asymmetric on the same element. Worth one
sentence in `dv-render.js`'s grammar comment so the next type lane does not discover it by driving,
the way this one did.
