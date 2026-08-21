# Context-territory strategy — how much window the delegated wrap buys, and what else expands the room

*Session #214 · 2026-08-21 · conductor Fable, mining by one Opus sub (139,796 sub tokens, n=1 — QUOTA, never window FILL). Store row `W-99x`. Every figure below was spot-checked against its named source line before inscription; units named on every figure (real = `message.usage` Claude tokens; FILL = resident context, never summed with throughput or quota).*

**Decisions in this brief are Dave's. Nothing here moves a constant, a line, or a band. His `s208-D1` rider is honoured by construction: the boot-reduction option is priced beside the re-base options, in Part 4.**

---

## Part 1 — What the delegated wrap already buys (the answer to the morning's question)

The wrap has been delegated to an Opus sub every session since ~#199. What that is worth, from the record:

An **in-window wrap costs 42,434 · 44,211 · 49,071 real** (n=3, measured #59/#91/#94, `notes/_GAUGE-LOG.md:637/:871/:903`). The set has been frozen since #94 — the re-price was declined as unrecoverable — and the ritual has grown considerably since, so the true in-window cost today is *at least* this band and plausibly higher.

A **delegated wrap costs the conductor only the hand-over**. The nearest measurements: hand-over deltas of **9,948 (#207) · 3,622 (#208) · 8,665 (#209) real** (the window movement between the conductor's declared brief cut and the wrap sub's first-hand cut, `_GAUGE-LOG.md:2086/:2100/:2113`), and the one measured delegation round-trip in the record — **~6,300 real conductor cost against 293,169 sub tokens, ~46:1 leverage** (#60, a *work* sub, n=1, upper-bound brief-out ~4,259 + partial report-in ~2,000, `_GM-ARCHIVE.md:3211`).

**So the measured gain is roughly 35,000–45,000 real of window per session** — the wrap band minus a ~5–10K hand-over. Against today's geometry (boot 61,633, advisory room ~88K), that is **about half again as much job room as an in-window wrap would leave**.

The price is quota, not window: **one delegated wrap measured 452,623 quota tokens** (#110, n=1, `_GAUGE-LOG.md:1038`). At today's panel (All models 11% · Fable 12%, both reset Thu 10:59 PM) quota is the slack resource and this trade is correct. When quota binds, the #110 precedent stands: the wrap runs inline and the old arithmetic returns.

**The honest gap:** no conductor-side delegated-wrap cost *field* exists in the gauge log — the #212 banner says so in terms (`GOOD-MORNING.md:50`), and the nine mined figures are whole-session FILL at mixed moments (three of the nine are the wrap sub's own cut, with the conductor's lower declared cut sitting beside them in the same log block). The 35–45K gain above is therefore a *derivation from adjacent measurements*, not a first-class measurement. Part 3 prices the fix.

---

## Part 2 — The larger prize: the advisory line is priced for a ritual we no longer run

The advisory stop line is arithmetic: **150,929 = 200,000 − 49,071** — the working line minus the *largest in-window wrap ever measured* (`_GAUGE-LOG.md:1000`; "the FORMULA is the ruling, the number is not" — `_gauge_tokens.py:77-83`). It contains no boot term and no delegation term.

With the wrap delegated by default, the −49,071 term is charging for a cost the conductor no longer pays. `s190-D2` already ruled the semantics (150,929 advisory; **200,000 is the binding squeeze cutoff**; "a conductor between 150,929 and 200,000 has legal room" — `_rulings.json:3214`). The formula, re-run with the delegated ritual's own numbers:

> **advisory = 200,000 − hand-over reserve (measured 3,622–9,948, n=3) ≈ 190,000**

**Option A (recommended): re-derive the advisory line as ~190,000, conditional on delegated wrap.** Gain: **+39,071 real of ruled job room per session**, from Dave's own formula with a measured term swapped for a measured term. Condition attached: if quota binds and the wrap must run inline, the line reverts to the old arithmetic that day. This is not goal-moving — the ritual changed; the formula is unchanged.

**Option B (recommend against, stated fairly): re-base the working/hard lines to the seat.** The evidence *for*: five delegated-era conductors ran FILL past every line and healthy — **515,335 (#209) · 369,000 (#210) · 305,137 (#211) · 237,361 (#212) · 226,539 (#213)**, all real, the #209 calibration-gap finding ("this seat's window is larger than the repo's gauge constants assume," `_GAUGE-LOG.md:2113`), plus 13 earlier crossings recorded as caused overruns. The evidence *against*: **256,000 is SOURCED, not picked — 93% MRCR v2 recall at 256K, falling to 76% at 1M** (`_gauge_tokens.py:55-59`), and Dave's own #58b shape stands: *do not reach 200,000 · 200,000–256,000 is dangerous · past 256,000 everything goes badly.* "Ran healthy" is the absence of a crash, measured; recall degradation is silent and no gate can see it. Trading a published benchmark for five anecdotes is the wrong direction of evidence. **If Dave wants this door opened, the honest precondition is a recall probe** (plant N facts early, probe them late, per-session) — priced in Part 3 as optional.

**One instrument observation, semantics UNVERIFIED and declared as such:** this seat's harness surfaces a remaining-token figure to the conductor at every turn — it read **~15.0M at today's boot**. Whether that is a context window or a session budget is unknown; it is named here only because the record's own gap list says "what this seat's true window actually is — none measures the denominator," and this is the first candidate instrument anyone has pointed at. Reading it costs nothing; interpreting it needs a probe, not a guess.

---

## Part 3 — Instruments to build (small, and they feed every decision above)

1. **Conductor-side delegated-wrap cost field** in the gauge-log wrap template: brief-out (`cache_creation` of the launching turn) + hand-over delta (conductor's declared cut vs wrap sub's first-hand cut — both moments are already being written; the field just subtracts them) + replay cost. A template/runbook edit, no code. After 2–3 wraps the Part-1 derivation becomes a measurement.
2. **Per-session boot re-measure script** (~15 lines, tiktoken over the mounted boot inputs) — already suggested verbatim in `_DS-IMPROVEMENTS.md:1789-1791`: the disk-resident half of boot is "a variable this programme shrinks, and nobody has ever watched it move." Also discharges the 72-session-old warning at `_gauge_tokens.py:104`.
3. *(Optional, only if Option B is ever live)* **Recall probe**: plant/probe fact pairs across the window, score per session. Not priced further unless wanted.

---

## Part 4 — The boot-reduction option, priced beside the re-base (the `s208-D1` rider, satisfied)

Boot is drifting up while the lines hold still: constant 56,749 ± 1,154; drift declared at #213 (6-sample mean 57,907, +1,157; the two newest boots, 63,258 and 61,605, are both OUT of band; today's read 61,633). The decomposition (pinned to the #109-era measurement, itself due a re-measure — instrument 2 above): MEMORY.md 8,800 · attributed harness items 15,660 · unattributed residual 40,648 · plus `_CHAIN.md` additive at turn 2.

**The single biggest lever: `_CHAIN.md` has doubled — 10,499 → 21,323 real** (its own generated footer, the one home). The chain *is* the ★ LATEST banner plus header; the growth is banner girth. A banner-discipline clause in the wrap brief (target the chain back toward its ~10–12K era) **recovers ~9–10K real at every session's turn 2** — no deletion of record, since everything rolls to the archive verbatim anyway. This was the #110 plan's P4, never started, and its target has doubled while it waited.

Second lever: **MEMORY.md compaction** (measured share 8,800 real; compaction is already owed at this opener as deferred wrap step 3) — worth an estimated 2–4K, by the established trim-hooks-to-overflow-files mechanics, never deletion. Third, for completeness: the MCP boot-rent trim was measured at ~1,500–3,000 and deprioritized by Dave's own no-sticking-plasters standard (#110-D3); it stays parked.

**Priced together: ~11–14K real per session back, against the +39K of Option A** — territory expands from both ends.

---

## Consequences and pitfalls (mandatory — Dave #165)

**(a) Option A removes early-warning margin for the day the wrap can't delegate.** Quota outage or a binding week forces an inline wrap; at FILL 190K the wrap then finishes at ~235–240K, inside Dave's "dangerous" band. Mitigation is the condition written into the option: quota-bound day ⇒ old line, announced at the opener, not discovered at the wrap. **(b) The hand-over reserve rests on n=3.** If the reserve is undersized the overshoot lands in exactly the band Option A spends. Instrument 1 fixes this within 2–3 wraps; a prudent sequencing is to build the field first and let the re-base proposal arrive with n≥5. **(c) The in-window band itself is stale (n=3, pre-#111 ritual).** Everything derived from 49,071 — including today's 150,929 — inherits that staleness in both directions. **(d) Recall loss past 256K would be invisible.** No gate, no instrument, no symptom until a wrong answer surfaces with confidence — the exact "confident false inscription" the whole Memento system exists to prevent. This is why Option B is recommended against without a probe. **(e) Quota inversion is standing.** A sub is free in budget and 5–10× in quota; every expansion lever here leans harder on delegation, so the strategy's own premise (quota slack) must be re-read from the panel at every opener — the panel is perishable and has three numbers. **(f) The chain trim is a wrap-brief behaviour change** — the same seam where a delegated sub once ruled Dave's open item; the clause must say *shorter*, never *decide what to drop* — roll-to-archive already preserves everything.

---

## The decision surface (plain words)

1. **Re-derive the advisory line to ~190,000 while wraps are delegated, with the quota-bind reversion condition?** Recommended yes — after instrument 1 has 2–3 wraps of data, if you prefer the cautious sequencing.
2. **Leave the 200K working and 256K hard lines exactly where your #58b sourcing put them?** Recommended yes. (The seat-evidence door stays closed unless you want a recall probe built first.)
3. **Build the two small instruments (wrap-cost field, boot re-measure script)?** Recommended yes — both are template-sized.
4. **Enact the boot-reduction pair (chain/banner discipline clause + MEMORY.md compaction)?** Recommended yes — this is the rider's option, priced at ~11–14K/session recovered.
