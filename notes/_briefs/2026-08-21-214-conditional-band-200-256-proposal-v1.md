# The 200–256K conditional band — proposal, with the re-source check done first

*Session #214 · 2026-08-21 · conductor Fable, re-source by conductor in-window (web, four sources). Store row `W-99y`. Companion to `2026-08-21-214-context-territory-strategy-v1.md` (row `W-99x`). This amends Dave's own #58b shape ("do not reach 200,000 · 200,000–256,000 is DANGEROUS · past 256,000 everything goes badly"), so ruling it is his signature alone. No constant moves until he rules.*

---

## Part 1 — The re-source check (what the current published record says)

The repo's stored figures — **93% MRCR v2 recall at 256K, 76% at 1M** — were verified at #56 and turn out to be **Claude Opus 4.6's** numbers. Still accurately quoted; now known to be model-specific. What the August 2026 record says:

**1. The gradient is real and current.** Every 2026 long-context survey confirms it: multi-needle recall degrades past 256K **for every public model**; RULER-style effective-context estimates put frontier models (Claude included) at **200–400K reliable** for multi-fact work against a 1M advertised window. The 256K point remains the last strong measured point on the Anthropic line. Our stored assumption is not stale — it's the current consensus shape.

**2. New and material: recall at scale is VERSION-VOLATILE.** Opus 4.6 scored ~78% on MRCR v2 8-needle at 1M; **Opus 4.7 reportedly dropped to ~32% on the same test** — described as a deliberate trade (long-distance attention traded for agentic/vision gains). A model upgrade can silently halve long-range recall between versions. **A published benchmark describes the model it was run on, not the seat you're on today.** This is the strongest argument yet for the recall probe: it's the only instrument that measures *our* model, *this* week.

**3. This seat's model (Fable 5) at 256K: strong; past 256K: unpublished.** Anthropic's launch copy says Fable 5 "stays focused across millions of tokens" — marketing prose, not a benchmark. The one hard figure found: **91.1 on multi-hop reasoning at 256K (best competing model: 73.7)**. No MRCR-style score for Fable 5 at 512K–1M is published anywhere. So at 256K we're on the strongest long-context model yet measured; beyond 256K we'd be running on a claim.

**4. The standing caveat that shapes the band's conditions:** the HELMET finding, reproduced by the 2026 generation — **synthetic recall does not predict downstream performance.** A model can ace needle-retrieval and still hallucinate summarizing the same haystack. This is precisely why the band must be conditioned on *work type*, not just token count: synthesis (a wrap, a ruling readback) is the downstream task recall benchmarks fail to predict.

**Sources:** [Anthropic — Claude Fable 5 and Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) · [ofox.ai — Real Accuracy Past 200K Tokens (updated 2026-08-17)](https://ofox.ai/blog/long-context-llm-benchmarks-200k-tokens-2026/) · [DataCamp — Fable 5 vs GPT-5.5](https://www.datacamp.com/blog/claude-fable-5-vs-gpt-5-5) · [WentuoAI — Opus 4.7 long-context regression](https://blog.wentuo.ai/en/claude-opus-4-7-long-context-regression-en.html) · [MRCR v2 8-needle leaderboard](https://llm-stats.com/benchmarks/mrcr-v2-(8-needle)) *(third-party figures are the trade press's, not Anthropic's; the leaderboard is the primary for MRCR numbers)*.

**Verdict of the check: the assumptions are real, and the band is better supported today than when #56 sourced it.** 200–256K on Fable 5 is measured-strong territory; 256K stays the wall (unpublished beyond, plus version volatility, plus the synthetic-vs-downstream gap).

---

## Part 2 — The proposed rule (amending #58b, Dave's signature)

**Current shape (#58b, Dave's):** do not reach 200,000 · 200,000–256,000 is dangerous · past 256,000 everything goes badly.

**Proposed shape:** 200,000 stays the *working line* jobs are priced against · **200,000–256,000 becomes a CONDITIONAL band** · 256,000 stays the hard wall, unqualified.

The band's conditions, all three required:

1. **Work-type condition.** In the band, only mechanical, receipt-backed, instrument-verified work is legal: renders with their proofs, gate runs, mechanical edits verified by diff, mining that quotes file:line. **Judgment and inscription work is illegal in the band** — rulings, wrap synthesis, decision readbacks, anything where a silently forgotten fact becomes a confident false inscription. If judgment work remains when FILL crosses 200K, it delegates to a fresh sub or waits for the next session.
2. **Declaration condition.** Crossing 200K is announced in chat at the crossing (one line, the check-in mechanism — a declared gap passes, a silent one fails), and the band entry is recorded at the wrap.
3. **Probe condition (the teeth).** The band stays legal only while a recall probe is green. The probe: the conductor plants 3–5 arbitrary fact-pairs in the window's first third (boot-adjacent), and quizzes itself blind at every check-in past 150K; a wrong or missing answer at any check-in **closes the band for that session** — judgment work stops immediately and the session heads to wrap. Cheap (~a few hundred real per check-in), per-seat, per-model-version — the only instrument that survives a silent model upgrade.

**What this buys:** the 200K line stops being a cliff-edge worry and becomes a gear change. Combined with the companion brief's advisory re-derivation (~190K), the practical shape becomes: **full-judgment territory to ~190K, mechanical territory with a live probe to 256K, wall at 256K.** Against the old working assumption, that is up to ~56K of additional legal (conditioned) territory per session.

---

## Consequences and pitfalls (mandatory — Dave #165)

**(a)** The work-type line will blur in practice — "mechanical" work quietly grows judgment content (a mining sub's summary *is* synthesis). Mitigation: the classification is made *before* entering the band, per remaining item, and anything unclassifiable is judgment by default. **(b)** The probe tests retrieval, not synthesis quality — HELMET says exactly this — so a green probe is *necessary, never sufficient*; that's why judgment work stays illegal in-band even with the probe green. **(c)** Version volatility cuts both ways: a model upgrade could also *improve* recall, but the probe only ever *closes* the band, never widens past 256K — widening beyond the wall would need published measurement on the current model, which doesn't exist. **(d)** Probe facts planted in the first third exercise the boot-distance recall path, but not mid-window recall; a v2 could plant at two depths. **(e)** The third-party MRCR figures (notably the Opus 4.7 regression) are trade-press numbers not verified against Anthropic's own publications; the *shape* (version volatility exists) is what the proposal leans on, not the exact 32.2%. **(f)** This adds a small standing check-in cost past 150K (~hundreds of real per check-in) — priced, accepted, and tiny beside the territory gained.

---

## Decision surface (plain words, each independent)

1. **Adopt the conditional band as ruled shape** — 200–256K legal for mechanical receipt-backed work only, with declaration + live recall probe? *(Recommended yes.)*
2. **256K stays the unqualified wall?** *(Recommended yes — unpublished beyond for this model, and the probe can't license what no measurement supports.)*
3. **Build the recall probe into the check-in** (plant at boot, quiz past 150K, band-closing on failure)? *(Recommended yes — it's also the standing defense against silent model-version regressions, worth having even if you decline the band.)*
