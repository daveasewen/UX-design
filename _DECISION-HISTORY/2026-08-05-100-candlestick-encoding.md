# #100 — Candlestick encoding: the four-state convention Dave brought, and rejected by his own eye

provenance: happy-ecstatic-edison #100 · 2026-08-05
status: ruled → knowledge/_rulings.json ds-027 · ledger notes/_MEMENTO-DECISIONS.md § ★ #100

## The arc

**1 · Dave opened with the richer convention.** He brought a reference table (hollow-candle semantics
from real trading charts, with a TradingView SPY screenshot): colour = close vs *prior* close, fill =
close vs *open* — four states. He'd already reasoned the accessibility consequence himself: *"we might
have to rely on the table this time as the fallback"* — i.e. he saw that spending the fill channel on a
second data axis breaks the shape-mirrors-colour redundancy of #96-D1 ①. He also asked for realistic
density ("usually there is a lot in these types of chart") and, mid-build, re-stated the standing rule:
*"all these charts should be fully responsive, so the 580 sizing doesn't really apply."*

**2 · The reversal was flagged before building.** Adopting four-state would reverse Dave's own #96-D1 ①
(hollow-up as the non-colour redundancy channel). Rather than launder his soft "we might have to" into a
ruling, the options were put to him plainly; he picked **four-state as a VARIANT** — a live spread, he
rules by eye — and ~40 candles in the canon frame.

**3 · The spread had to be made judgeable.** First seeded dataset produced only 4/40 candles that
differed between the two encodings (gap-opens are what create the divergent states, and the walk had
almost none). Caught by looking at the render, not by any gate — then pinned as a gate:
`ASSERT-diverge ≥ 8` plus every state ≥ 4 examples, so the generator can never again emit a spread too
weak to judge. Seed search (100→103) found a passing dataset. This is the session's transferable lesson:
**a decision spread has its own quality bar — the variants must visibly diverge — and that bar is
assertable.**

**4 · Dave ruled against the convention he brought.** Seeing both live: *"variant a, we can just go
solid on the blocks, we're using the table as the fallback position for Ally."* Two-state semantics
(colour = close vs open), **solid bodies both directions** — which retires the hollow-up channel
entirely, going further than either variant on display. The OHLC table (+ per-candle aria-labels)
carries accessibility. The four-state key stays in the review doc as the record of what was considered.

**5 · Enactment rolled on the stop line.** Check-in at the enactment seam: FILL 143,566 vs stop
150,929. The canon-snippet rewrite is a serial loop (edit → validate → regen → render) — exactly the
#95/#99 blow mechanism — so the wrap opened *before* the loop, and #101 inherits it whole:
solid `.dv-up`, 40-session dataset (seed 103), `data-fx`/`data-x0`/`data-fw` wiring (today's canon
candles have no `data-fx` — they don't reflow at all), manifest + header comments reciting ds-027,
then gates + showroom regen + render-verify.

## Resolved / open

Resolved: ds-027 (encoding + solid + table fallback + density/responsive standing word).
Open → #101: the enactment above · bullet flex-height · Confirmation Replay idiom · 125/49 corpus
fork · #97 flag ② · `--pri-hover` stored equivalents at retired 0.70.

Links: spine `_LIVE-STATE.md` ⏱ #100 · ledger § ★ #100 · spread
`reviews/CANDLESTICK-FOURSTATE-2026-08-05-v1.html` (+ `gen_candlestick_fourstate.py`, seed 103).
