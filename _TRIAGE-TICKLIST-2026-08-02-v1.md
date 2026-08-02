# Bankruptcy triage tick-list · #86 · 2026-08-02

**Tick a GOVERNING item to accept its `closes_when`; strike it to redraft. INERT items archive as one block unless you pull one out.**

---

## ⛔ THE INVENTORY THE HANDOFF GAVE ME WAS NOT REAL — measured first, per [[premise-ages-faster-than-rule]]

The handoff said **118 markers** (`UNRULED` 67 · `FORKED` 24 · `awaiting Dave` 11 · `PROVISIONAL` 16) in GM + ledger. **No probe reproduces those numbers** — not line counts (31 in those two files), not occurrences (31), not case-insensitive (53), not repo-wide (231 lines, incl. archives the bankruptcy doesn't touch). Consolidated to real ITEMS across all live homes (GM, ledger, LS, code, standing knowledge docs — archives and dated records excluded):

> **MEASURED SPLIT: 16 GOVERNING (+1 borderline) / ~22 named INERT + 3 unexpanded question-batches.**
> The prediction's numerator **survives** (~15 predicted, 16 measured — and it was predicted).
> The denominator **dies**: there is no 85-strong INERT pile; the "~100 queued decisions" never existed.
> **The bankruptcy ruling survives, but it is a smaller event than #85 sold it as.**

**Method, declared:** code items verified at the call site; prose items verified at the marker line + context only. `?` = not verified to call-site depth.

---

## GOVERNING — live code/values running on a provisional choice. Archiving = silently permanent.

| ✓ | # | live value, in force today | drafted `closes_when` |
|---|---|---|---|
| ☐ | G1 | `DOFIRST_INDEX_TK_MAX = 700` — agent-picked #82 over measured 531 (`_capture_gate.py:1403`) | Dave ratifies 700 or names his own |
| ☐ | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`:371`, `RATIO_FIRM_N = 4` already pinned) | 4 measured pairs logged → Dave rules firm-or-retire |
| ☐ | G3 | retired-unit prose gate runs WARN not FAIL — tier agent-picked (`:2078`) | Dave rules WARN vs FAIL |
| ☐ | G4 | §C over warn cap (191 > 150), fires every run; remedy unruled (`:2864`) | Dave picks OFFLOAD / TRIM / KEEP |
| ☐ | G5 | advisory cap set: `CORPUS_BUDGET 36000` · chain pair (4917, 6417) · banner fallback · §A 4500 — all agent-derived, all in the OLD unit (`:4843–4858`) | re-measured in real (G9 first), then Dave ratifies the set |
| ☐ | G6 | `DEFER_STREAK = 6` + `USAGE_HISTORY_BLOCKING = False` — advisory, agent-proposed #35 (`_gm_usage.py:353`) | Dave rules the streak + per-candidate OFFLOAD/TRIM/KEEP |
| ☐ | G7 | `roll_2f`/archives "which end is newest" — rolls run on an unruled convention (`:268`, ledger:687) | Dave names the newest-end convention (one sentence) |
| ☐ | G8 | % band 45/60/63 DORMANT in code — retire-or-pin FORKED since #58 (`:135–137`) | Dave says retire or pin |
| ☐ | G9 | **ds-023, the CLASS:** every ceiling stated in tape is now graded against real ⇒ ~1.55× tighter than whoever set it intended (G1 was one instance) | Dave rules the re-measure-and-restamp programme |
| ☐ | G10 | "70%/95%" third band — unprovenanced, FENCED live in GM:36 | Dave rules provenance or strikes it |
| ☐ | G11 | DS-018 recessive value — four candidates, components render with one today (`_DS-IMPROVEMENTS.md:939`) | Dave picks the recessive value |
| ☐ | G12 | Charter §4b register temperature — PROVISIONAL since 07-02, used at build time (`_FIXED-FLEX-CHARTER.md:55`) | tov-016 review lands or Dave ratifies §4b |
| ☐ | G13 | two PROVISIONAL masthead icons live since 07-16 — crescent where Dave asked **bow-and-arrow** (`_ICON-GAPS.md:8–9`) | Dave approves final glyphs |
| ☐ | G14 | icon-button dark bindings reuse Button's verbatim — PROVISIONAL; SC dark still awaits Dave (`icon-button.meta.json:68`) | Dave rules SC dark |
| ☐ | G15 | DV-D13 centre-figure + `st.visible[id]=true` — agent's call, live in showroom (`_REVIEW-SIGNOFF.md`) | Dave's eye at sign-off |
| ☐ | G16 | DATAVIZ "one enactment call is the agent's, not Dave's" (`_DATAVIZ-DECISIONS.md:567`) | Dave ratifies or reverses the call |
| ☐ | G17? | RAG status manifestation — canon pick A / A+B / A+B+C open since 07-19 (`_LIVE-STATE.md:387`); whether a provisional manifestation renders live is **unverified** | Dave's canon pick |

---

## ⚠ A THIRD PILE THE TWO CLASSES DON'T COVER — the asymmetry you asked #85 to explain, now with bodies

**RULED-BUT-UNENACTED.** Archiving these doesn't make a provisional value permanent — it **silently un-does a ruling of yours**. Bankruptcy must not touch them:

- Molecules pack — **RULED #66, enacts still pending** (`_REVIEW-SIGNOFF.md`)
- Radius/corner tuner — your explicit *"return SOON, don't let me forget"*; archiving it does exactly the forgetting
- #84-D1 — ruled, instrument doesn't yet serve it; successor named for re-open anyway

---

## INERT — open questions, nobody blocked, no live value. Archive as ONE block; return by name with a `closes_when`.

ds-016 *(borderline — a blind index is live behaviour, but no provisional value)* · ds-017 · six `_decision-graph.json` edge types (#71) · cross-instrument claim check *(already opener item (a))* · pre-flight presence gate *(opener (b))* · "Caps bind on `bill`" rot-or-record *(opener (d))* · `_produces_real_tier()` propagation *(g)* · `_measure_tokenizer.py` 0 consumers *(h)* · `_FUTURE-STATE.md` two proposals (by their own text) · `_DS-IMPROVEMENTS.md` :768 floated + :801 remedies · msgfile blank-line-2 fold · grouped-column redesign *(blocked on your reference images)* · chart text clip/collision remedy · TYPE Q1 (provisional pending trim check) · D3 scatter re-look *(#72 — you asked to SEE it again)* · COMBO-LINE-INVERT R-B/R-C · donut + chart-bar "awaiting eye" *(possibly superseded by #79 sign-off — verify before archiving, two padding deltas were the open part)*

**Unexpanded, declared:** three ledger question-batches (ledger:553 ×3, :1281 ×5, :2053 ×3) — not read to item depth this session; they go into the archive block with a flag, not a classification.

---

## Residuals, declared

1. Boot half UNMEASURED (ds-025 stands) — the pricing above is conversation-half only.
2. I read `_CHAIN.md` (~13K real) before finding the handoff that forbade it — **the chain's "YOU ARE #85" outranked the handoff for a cold session; the handoff shape needs a claim on the boot path or it loses to the chain every time.** Finding for the rebuild.
3. G17 and the two "awaiting eye" entries carry `?` — not verified to call-site depth.
