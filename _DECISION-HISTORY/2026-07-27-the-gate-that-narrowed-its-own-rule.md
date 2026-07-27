# 2026-07-27 — The gate that narrowed its own rule

```
provenance: local_f9387db0-49bb-4d2d-8f53-7944f0adcb1a · 2026-07-27
status: ruled → knowledge/_proforma/_DATAVIZ-DECISIONS.md (DV-D14, DV-D15)
```

*Session: ds-014 calls (a)+(b) put to Dave, ruled, enacted and PROVEN BY RENDER. Opus 5 solo
self-conducting, effort MAX. Build 57/57 → 58/58 GREEN. Spine entry: `_LIVE-STATE.md` ⏱ LATEST
2026-07-27 (later-morning #2). Ledger: DV-D14 + DV-D15. Defect record: `knowledge/_DS-IMPROVEMENTS.md`
ds-014 (calls a+b, ENACTED block). Forward idea: `_FUTURE-STATE.md` § forcing the KG into the decision loop.*

---

## Why this session is worth a dossier

The WHAT is small: a stacked bar chart got 2px of separation and its letter keys went white. The WHY
is not. **Three times in this session a check said green while the thing it checked was wrong**, and
each time the mechanism was different. The value here is the pattern, not the chart.

---

## 1 · The recommendation that was wrong, and how it got made

ds-014 call (a) asked how to create dv-004's required separation on the stacked column. I recommended
**a 2px surface-coloured stroke**, reasoning: the donut already does exactly this, it's proven, and it
leaves the data-to-pixel mapping untouched.

Dave declined it and asked why:

> *"I prefer the geometry the border will obscure gridlines, may I know why you recommend borders?"*

**He was right, and the check took one grep.** `cb5` carries **five full-width `.dv-grid` lines behind
the columns**. The donut carries **none** — it sits on plain page. An SVG stroke straddles its path, so
a 2px stroke puts 1px *outside* each rect: a page-coloured band painted over every gridline down both
sides of all four columns.

**The generalisable form:** *a surface-coloured stroke only simulates separation when the thing behind
it IS the surface.* The donut's mechanism isn't wrong — its **ground** is uniform and cb5's is not. I
transferred a precedent without checking what it was standing on.

⚠ **The failure was procedural, not analytical.** CONSULT-before-designing is a STANDING rule. I did
not run it before recommending. Had I, I'd have read dv-004's actual text in the first minute.

## 2 · What the consult actually said — the real finding

Running it (late) returned:

> `[dv-004] (BLOCKING) Colour separation: don't rely on colour to separate values — **minimum 2px
> separation between colour blocks.**`

**Mechanism-neutral.** No stroke. No mention of one. But `_validate_dataviz.py` enforced it as:

> `dv-004  >=2px separation — gapless surfaces (donut/stacked segments) carry a surface-coloured stroke >=2px`

⇒ **The gate had narrowed a mechanism-neutral rule into a single mechanism, and nothing compared the
two.** The consequences run both ways, and the second is the nasty one:

1. A chart satisfying dv-004 with **real geometry would have FAILED** the gate — a false negative on a
   correct implementation.
2. **An agent reading the gate to find out what compliance looks like gets the wrong answer** — which is
   precisely what happened to me. The gate wasn't just failing to catch the error; **it was the source of it.**

Dave named the fix direction before I'd finished writing it up:

> *"btw the gap is only 2px minimum, this is in the dataviz specifications in the KG"*

and then, unprompted, the class:

> *"we may create something that will force decisions to check that KG in such situations… the KG is a
> valuable resource and shouldn't be ignored, thats what it is there for"*

Held in `_FUTURE-STATE.md` as **floated, not ruled** — he explicitly asked to explore benefits, method
and implications together. The sharpest angle recorded there: **a check comparing what a rule SAYS
against what its gate DEMANDS** — the exact mirror of ADR-0016. The register asks *"is this ruling
live?"*; this asks *"is the gate still enforcing the rule, or its own paraphrase of it?"*

⚠ **And a caution against building it naively:** today's consult printed `rulings (5/5 shown, --all for
more)`. **It truncates by default.** A forcing function built on a truncating query is a CLAIMED gate
with extra steps — the ds-013 shape exactly. Its own recall needs bite-testing before anything leans on it.

## 3 · The vocabulary had forked, and enumeration would have papered over it

The register's scope-blindness audit named three blind values. Counting the corpus directly showed
something worse: **the vocabulary had forked without anyone noticing.** Both `stacked` *and*
`stacked-column`. Both `grouped` *and* `grouped-column`. Plus `scatter`, never taught to the gate at all.

Adding three strings to a tuple would have fixed today and guaranteed a repeat. Instead:

- **`DTYPE_CANON`** normalises synonyms **once, at read time**, not at five separate branches;
- **`dv-vocab` (NEW, BLOCKING)** — any `data-dv-type` the gate has never heard of now **fails the build**,
  naming the rules that would otherwise have skipped it in silence.

**That converts the whole class from silent-skip to build-failure**, which is the only version that
survives the next person adding a chart type. Scope-blindness audit now reports *"No scope-blind
vocabulary values detected."*

## 4 · The third silent failure — and it happened AFTER everything was green

Call (b): mint `data/text/on-series` (Dave's promotion), rebind cb5's keys, split the blanket CSS rule
by ground. Token minted, generated into `canon.css` (`--data-text-on-series: #FFFFFF`, both modes),
markup rebound, **build 58/58 green**.

**The keys still rendered BLACK. 3.99:1.**

The snippet is standalone-previewable and carries a **local mirror** of the token list in its own
`[data-theme]` blocks — and that mirror didn't declare the new var. **`fill:var(--undefined)` does not
fall back to the previous value; it falls back to the SVG initial value, black, in silence.**

Third instance of one class in this file's history, each with a different mechanism:

| | mechanism | detected by |
|---|---|---|
| **ds-010** | author CSS beat each rect's `fill=` attribute | render |
| **ds-013** | 404 stylesheet — `srcdoc` re-based the URL | Dave's eye |
| **today** | `var()` on an undeclared property → silent black | render probe |

**The through-line: a lookup that misses and reports nothing.** No gate we have catches any of the three,
because in every case the *markup is correct* — the resolution is what fails.

## 5 · The probe committed the error it was written to detect. Again.

`_verify_dv_stacked_enactment.py` is the ADR-0016 **P2 proof** for both rulings: read the ruled value,
assert the **rendered** value in the licensed cut, across snippet × showroom × 1180 × 760.

Its first run reported **`"no stacked-column figure"` for the showroom** — and the honest reading was
*not* "the showroom is broken". The showroom delivers snippets into pane **iframes via `srcdoc`** (the
ds-013 mechanism), so the figure is never in the top document. **I had queried only the top document.**

Last session's probe used `querySelector('svg')` and got the **toolbar copy icon**, reporting a 16px-wide
"chart canvas". Different bug, identical class: **looking at the wrong document and believing the answer.**
Third session running. The loop over `page.frames` now carries a comment saying so.

**Standing lesson, earned three times: assume your probe is wrong in the direction that reads as green.**

## 6 · What was measured, and one correction to the record

Licensed cut, snippet **and** showroom pane, 1180 **and** 760 — all four agreeing:

| assertion | ruled | rendered |
|---|---|---|
| dv-004 separation | ≥2px | **2.00px**, all 8 boundaries |
| key A on `rgb(118,102,130)` | ≥4.5:1 | **5.26:1** |
| key B on `rgb(164,92,58)` | ≥4.5:1 | **5.04:1** |
| key C on `rgb(87,124,120)` | ≥4.5:1 | **4.61:1** |

⚠ **Correction to the prior handoff:** it predicted *"white measures ≈5:1"*. **Measured worst case is
4.61:1** — series-3, margin **0.11** over AA. Recorded as measured, per 07-26's Correction 2.
**Series-3 cannot be lightened without breaking AA here**, and nothing but this proof would catch it.

## 7 · Resolved state, and what is still open

**Resolved:** DV-D14 + DV-D15 inscribed · cb5 re-geometried (variant A) · `data/text/on-series` minted ·
dv-004 accepts both mechanisms · `dv-vocab` blocking · 9 new bites · **the dataviz selftest WIRED into
the build** (it existed and ran only by hand — which is exactly why nothing ever proved dv-004 could
fail) · build **58/58** · register **PROVEN 3→4, UNPROVEN 53→52**.

**Open:**
- **(d) donut cluster alignment — PARKED on Dave's ruling.** Logged, deliberately not fixed.
- **52 UNPROVEN rulings** — the P2 programme. Today proved two; the method is now demonstrated twice.
- **Dave's forcing-function idea** — needs the exploration session he asked for. **Do not build ahead of it.**
- **The 49 showroom panes** still owed an eyeball since ds-013 (`_REVIEW-SIGNOFF.md`).

**A note on how the two rulings were reached, because it is the reusable part:** both came from Dave
*pushing back on a recommendation and supplying a fact from the KG*. Neither was an agent derivation
he approved. The record should keep it that way round.
