# #260 lane F2 — CORE REQUESTS from the PIE type (verbatim, for the core owner)

⛔ A type lane must not make these. Filed, not enacted. Lane F2 edited neither
`knowledge/canon/dv-render.js` nor `knowledge/canon/dv-render-donut.js`.

---

## 1 — RADIAL PATH COORDINATES MUST BE EMITTED AT TWO DECIMALS (the 2.109 defect, cause proven)

**The finding (lane A, #260):** the driven receipt records the donut's dv-004 separation as
**2.109px** and the pie's as **2.108px**, against an authored `GAP = 2.2`. The attributed cause was
`U.n1()` rounding radial path coordinates to one decimal in `dv-render-donut.js`.

**MEASURED, not asserted — and the attribution is only PARTLY right.** I built the fix in a scratch
copy of `dv-render-donut.js` (a local `n2(v) = (Math.round(v*100)/100).toFixed(2)` used by `pt()`
and by the three radius literals in `arc()`; nine call sites, no core change, no other edit) and
drove the **committed** `donut.html` twice through `_drive_chart_engine.py`'s own `drive()` —
control and patched, 4 themes × 2 modes each, into a scratch receipts path:

| figure | control (`n1`, one decimal) | patched (`n2`, two decimals) | authored |
|---|---|---|---|
| `fig-donut` (ring, measured at the inner edge ri = 60) | **2.109px** | **2.194px** | 2.2 |
| `fig-pie` (wedge, measured at 0.35·ro = 35) | **2.108px** | **2.134px** | 2.2 |

Identical in all 8 combinations, 0 pageerrors, 5 arcs, filter still re-renders 5 → 3.

**So the DONUT defect is exactly the rounding**: 2.109 → 2.194, residual 0.006px = the remaining
two-decimal budget. **The PIE's is not** — see request 2.

**Requested change, verbatim:** *"In `knowledge/canon/dv-render-donut.js`, emit radial path
coordinates at TWO decimals, not one. Add a local `function n2(v) { return (Math.round(v * 100) /
100).toFixed(2); }` beside the existing `n1` alias and use it in `pt()` and for the three radius
literals inside `arc()` — leave `n1` on the data-\* attributes and the annotation geometry, where a
tenth is plenty. The cost is +9 code bytes and the measured gain is 0.085px of dv-004 headroom, from
2.109 to 2.194 against an authored 2.2. Do it in the donut file rather than in the core: the core's
`n1` is also what dv-behaviour's fit re-rounds to a tenth on cartesian marks, so widening it there
would spend bytes on a pass that throws the extra digit away. If a second radial type ever needs
it, promote `n2` to `dvRender.util` then — not before."*

⚠ Do **not** also lower `GAP` from 2.2. The 0.2 is the *cartesian* rounding budget the core comment
documents; on a radial path the two-decimal emission is what buys the same safety, and the two
mechanisms are independent.

---

## 2 — dv-004 ON A PIE IS MEASURED AT A CONVENTION, AND THE CONVENTION IS THE NUMBER

`_drive_chart_engine.py` measures a ring at its inner edge (`rmin`, the narrow one — correct) and a
pie at **`0.35 · ro`**, "the engine's own reference radius for a pie", because a pie has no inner
edge. That is why the pie barely moved above: **its recorded figure is dominated by the reference
radius, not by rounding.**

The honest geometry: two adjacent wedges are two rays from one centre separated by `gap` radians.
Their separation is `r · gap` and it goes to **ZERO at the apex**. There is no radius at which a pie
satisfies "2px everywhere"; `0.35 · ro` is a convention that both the partial (`ctx.GAP / (ri || ro
* 0.35)`) and the driver happen to share.

**This is not a request to change the driver** — the driver is gate-adjacent and fenced from a type
lane. It is a request that the core owner (or Dave) says which of these the library means:

- (a) dv-004 on a pie is judged at a **named reference radius**, and that radius is written down
  once — today it is a magic `0.35` in two files that agree by luck, not by contract; or
- (b) dv-004 does not apply to a wedge at all (the rule is about *adjacent filled blocks* of
  comparable width), and the pie is scoped out of the rule the way boxplot already is.

**Ruling-shaped, not a lane's.** Recorded here because the pie is the member that makes it visible.

---

## 3 — RE-AFFIRMED FROM #259 (lane D), still open, NOT re-filed as new

`dvRender` still calls `furniture()` unconditionally and `dv-render-donut` still opens with
`ctx.out.length = 0` to throw away gridlines it never wanted. Chart-pie inherits that cost verbatim.
Lane D's wording stands: *"honour `fn.axis = "none"` (or `fn.furniture = false`) in `dvRender` by
skipping the `furniture(ctx, …)` call, the way `fn.axis`/`fn.domain` are already honoured."*
