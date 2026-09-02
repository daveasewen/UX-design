# #240 — THE BOOT BAND: derive it, ratchet it, shrink first (FLOATED at #239; Dave: "we need to get this fixed soon")

**Status:** RULING-SHAPED, Dave's. Pasted by Dave into #239 mid-turn (a proposal from another seat's wrap); #239 had no window budget for it (FILL 168,576 real past the 150,929 advisory when it arrived) and filed it here unchanged in substance. **First beat of #240: Dave rules the shape, then it goes to ONE lane.**

## THE CLASS (his framing, kept)
The `s208-D1` band (`BOOT_FIRSTTURN_TK` 56,749 ± 1,154 → 55,595–57,903 in `knowledge/_gauge_tokens.py`) is a TYPED constant that a MEASURED number keeps walking away from: #234 75,206 · #235 75,294 · #236 75,198 · #237 76,915 · #238 75,336 · #239 75,619 (all first-turn `message.usage`, read from `notes/_GAUGE-LOG.md` + `_checkin.py`). Every wrap either declares the gap or asks for a re-base. That is the copy-chain class one level up — the thing `s234-D1…D6` (generation chain, never copy chain) ruled out everywhere else.

## THE PROPOSAL — three parts, ORDER MATTERS
1. **Derive the band, never type it.** The gate reads the last n=7 first-turn `message.usage` figures from the gauge log and computes median ± measured spread at check time. A step change beyond the spread goes red; slow drift never needs a re-base because there is no constant to re-base. *(the class fix)*
2. **Keep ONE absolute number as a shrink-only ratchet.** A rolling band alone is a thermometer that follows the fever. One ceiling stays typed, Dave's to move, and boot may only go DOWN past it — the type-composites debt ratchet, re-used. *(what catches bloat)*
3. **Shrink first** — already RULED as `s228-D6` (shrink-then-rebase) and the `s208-D1` rider. `MEMORY.md` alone has gone 8,470 → ~20,700 bytes; each per-session ToolSearch load is ~1,200 real. Cut those BEFORE anything is derived, or the derived band just ratifies the bloat.

## UNPROVEN, NAMED (carried from the paste, not verified at #239)
- Whether the drift gate fires in CI or only in the wrap gate — nobody opened its code; it surfaced as a declared WARN at a wrap, never a CI red. Price: grep `_gauge_tokens.py` + `_capture_gate.py` for the band check, one call.
- Whether "76,125 mean, +19,376, fourth session running" in the paste is #238's or another seat's reading — #239's own first-hand figure is 75,619.

## WHAT THE LANE WOULD TOUCH (price, for the ruling)
`knowledge/_gauge_tokens.py` (band → derived function + one typed ceiling), `_capture_gate.py` / `_checkin.py` wherever the band is compared, `notes/_GAUGE-LOG.md` read path (n=7 window), a selftest arm per behaviour (step change red · slow drift green · ceiling ratchet refuses a rise), the runbook stratum. Est. one Opus lane, ~19K conductor return. The MEMORY.md shrink is a SEPARATE chore (memory-compaction pass, conductor's seat — memory is outside the repo and outside any lane's reach).

## DO-NOT-RULE for the lane
The ceiling's VALUE (Dave's) · n=7 vs another window (propose, don't pick silently) · retiring the dormant 45/60/63 % band (`G8`, Dave's) · anything that moves the stop line, wall or advisory.

**Recommendation to Dave (one clause):** rule all three as written — part 3 is already his ruling, parts 1–2 are the same shape as `s234` and the composites ratchet, both already his.
