# Carry-forward — the chart encoding gaps Dave found on the DV-J2 scatter half (2026-07-28)

provenance: session #27 (Opus solo, Dave live) · 2026-07-28
status: floated

> **⚠ THIS LIST IS NOT CLOSED.** Dave's own words on handing it over: *"There maybe more than I've
> stated too."* Anything below is what was caught by eye in one look at one chart. **A later session
> must not read this as a complete specification** — it is a starting set with a known-open tail.
> Treat a fifth finding as expected, not as a surprise.

## Why this file exists

Dave reviewed `Chart-scatter.reference.html` after the DV-J2 scatter half landed (#27, `4283344`)
and found four defects by eye in under a minute. Every one is a **rule Apollo already holds but does
not enforce**. The work is therefore NOT four spot-fixes — it is encoding — and it was deliberately
NOT started in #27 (that window was already Amber and post-wrap; building gates hot is how the
silly-mistakes class lands). Dave: *"I doubt its safe to do the changes and encode them into the
system here."*

**Sequencing argument, and it is the load-bearing one:** the chart-expansion wave is **eight more
charts** (`GOOD-MORNING.md` §C·1(a) STEP 2). Encoding after the wave means fixing nine times;
encoding before means the wave cannot reproduce any of it. This should go in front of the wave.

## The four findings (Dave, by eye, 2026-07-28)

**1 · Cropping + collision on axis text.** The "Savings (£000)" axis title collides with the topmost
tick label ("75"), and the descender on the "g" is clipped. Dave: *"we've fixed this before, need
encoding."* — correct: ds-005 fixed descender clip and `_validate_descender_clip.py` gates it. **But
that gate operates on CSS `text-box-edge`, which SVG `<text>` does not use** — it structurally cannot
see an axis label. The collision half has no gate anywhere.

> **✅ INSTRUMENTED 2026-07-28 #29 — `knowledge/_render/verify_chart_text_render.py`.** MEASURED, both
> widths, licensed cut: `'Savings (£000)'` ink **1.38 units** above the viewBox ceiling ·
> `'75'` × `'Savings (£000)'` ink overlap **13.96 × 3.50**. Bite (sentinel) detects; `--control`
> (the geometric remedy, applied live) goes GREEN — so the proof is not merely stuck red.
> ⚠ **The note above is right about the ink but wrong about the mechanism, and the distinction
> decides the remedy:** the `g` is the ink involved in the *collision*, but it is **not clipped** —
> the clipping happens to the **caps at the opposite edge**. Two defects, one sensation. A fix aimed
> at descenders would have addressed neither. Both beats kept per the Memento discipline.
> ⚠ **Still OPEN:** the defect is measured, not fixed. `--control` SPECIFIES the geometry
> (`x=2→46`, `y=9→11`) — the numbers are Dave's to rule. Corpus-wide debt **UNMEASURED**
> (see the dossier's "what is NOT proven"). Arc + the four instrument corrections:
> `_DECISION-HISTORY/2026-07-28-chart-text-clip-collision-render-proof.md`.

**2 · Charts must be responsive — and the existing rule's exclusion list is itself wrong.**
See § DV-D02 below; this is the biggest item here, because the rule I was about to encode has a
defect in it.

**3 · Every chart needs a title.** Dave: *"this is in the KB, such things need transferred to be
encoded."* Chart-bar carries `<h3 class="dv-title">`; scatter carries none. ⚠ A #27 grep of
`knowledge/guidelines/data-visualisation*.md` found titles named only as a *building block* in a
colour rule (`data-visualisation.md:46`) — **the explicit rule was NOT located.** Do not conclude it
is absent: #27's search was narrow and its budget was short. **Find the KB rule first, quote it, then
gate it.** If it genuinely is not written down, that is itself the finding and it needs Dave's word
before a gate invents a rule.

**4 · The legend does not carry the ruled behaviours, and the composition tier is missing.**
Scatter ships a static `<ul class="dv-legend">`; the DV-D11 dual-gesture model lives in
`canon/dv-legend.js` and is carried by bar/line/combo/donut. Dave's proposal, verbatim: the legend
*"should probably be a separate molecule, same for the controls… The control cluster should probably
be a molecule too with varying contents so parametised or something."*

## ★ DV-D02 — Dave's correction, and why it outranks the rest

The ledger reads: **"Responsive = compress width, never scale proportionally, and TEXT MUST NOT
SCALE… Cartesian charts only; horizontal bar + donut excluded"** (compressing a value axis or a
circle distorts). #27 challenged Dave's "all charts responsive" on the strength of that exclusion
list. **Dave rejected the challenge, and he is the source of the rule.** His words, kept verbatim
because they are hedged and must not be hardened by a later reader:

> *"I think horizontal bars are fine to be fully responsive, donut (graphics) probably not but their
> lockup with the legend will, and I may add breakpoints at some point so that they scale, but thats
> another task when we tackle the 12 column grid and breakpoints."*

**Read carefully, that is three separate things:**

- **(a) h-bar responsive.** DV-D02's exclusion of horizontal bar is **wrong or over-broad**. Status:
  Dave leaning, hedged ("I think") — **NOT YET A FIRM RULING.** Confirm before amending DV-D02.
- **(b) the graphic/lockup split — the conceptually important one.** The donut *graphic* stays
  non-responsive; the donut's *lockup with its legend* is responsive. **Responsiveness applies at
  different levels of a composition**, and DV-D02 today speaks only about plots. This is the same
  seam as finding 4: the chart+legend lockup is a composed object with behaviour of its own.
- **(c) breakpoints/scaling — EXPLICITLY DEFERRED** by Dave to the 12-column-grid + breakpoints task.
  **Do not fold it into this work.** It is named here only so it is not re-discovered as new.

**⚠ Consequence for whoever encodes finding 2: you cannot gate DV-D02 as written.** The rule needs
amending first (at minimum (a), probably (b)), and that is Dave's call, not a lane's. Gating the
current text would enforce a defect — and gate a *correct* future h-bar as a failure.

## ✗ A false inscription made in #27, corrected 2026-07-28 — read this as a worked example

#27 wrote **"FIT not adopted — DV-D02 static, deliberate"** into the DataViz ledger row, the
`GOOD-MORNING.md` banner author-flags and the `_LIVE-STATE.md` delta, and committed all three. **It
was false.** Its source was a CSS comment in scatter (`/* DV-D02 static: fixed geometry, scroll —
text never scales */`) which describes the *safe fallback*, not an exemption. The ledger — the actual
ruling — says cartesian charts are in scope, and scatter is cartesian.

So the agent **inferred a ruling from prose instead of retrieving it**, in the same session it
correctly caught the queue doing the equivalent. Both beats stay in the record per the Memento
discipline, so the reversal can never read as drift. The standing rule it violated is already
written: *trust the spine, don't mine the prose* — retrieval, not recall. The corrections are applied
in place at all three sites.

## Correction 2 — a render-time check is CHEAP, not expensive

#27 argued the collision check "needs a browser, which is why nothing does it", framing it as a more
expensive class of gate. **Dave pushed back and was right.** #27 itself mounted
chromium-headless-shell and ran `knowledge/_render/verify_dv_j2_render.py` green in the same window.
The mechanism for finding 1 is `getBBox()` / `getBoundingClientRect()` on the SVG text nodes inside
the harness that already exists — assert that no two text bounding boxes intersect, and that each
glyph box sits inside its viewBox. **This belongs in the render-proof family, not in a
`_validate_*.py`**, and the runbook for standing the pipeline up is `_RUNBOOK-render-verify.md`.
⚠ Price the sandbox in: it is fresh every session, ~4 calls before a single pixel.

## Proposed shape of the encoding window (NOT ruled — a proposal)

1. **Amend DV-D02 first** — Dave confirms (a) and (b); nothing else can be gated until he has.
2. **Gate the cheap statics** — cartesian chart carries `dv-fit`; every chart carries a title (once
   the KB rule is located and quoted). Each ships a selftest wired into `_build_all.py` and a bite
   proving it can fail — the standing terms for a new gate.
3. **Add the render-time text assertion** — collision + clipping, in the render-proof family.
4. **The composition question is an ADR, taken separately.** ADR-0013 partials + the ADR-0015
   consumes-manifest are already the sharing mechanism, and the manifest is exactly what makes a
   shared legend affordable per chart rather than 16 KB on everyone — so #27's counter-proposal is to
   use the existing machinery rather than mint a new "molecule" tier. **But the genuinely missing
   piece is real:** partials inject a *fixed* block, and Dave is asking for a cluster with *varying
   contents* — a slot/props model the registry has no concept of. That is the same shape as the
   templates/shells zero-tier gap already on the board, and it is a design call.

## Standing reminders for whoever picks this up

- **The list is open** (top of file). Expect a fifth finding.
- Dave's stated preference, in his words: *"I lean to correctness, standardisation with flexibility
  rather than expediency."* A gate that encodes a rule without its principled exceptions is not
  standardisation — it is a future false positive. Encode the exclusions **and their reasons**
  alongside the rule.
- Scatter is not the defect; scatter is the **instrument**. It was the first genuinely new chart
  built after these rules existed, and it broke all four — which measures the gap between what
  Apollo knows and what Apollo enforces. That gap is the actual subject of this brief.
