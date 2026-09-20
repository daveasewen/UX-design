# Brief — deck v10 — three more drawings in, the five-up anatomy — #289 — 2026-09-20

Source: `notes/_DEMO-SLIDES-apollo-2026-09-20-v9.html` (12 slides; gearbox `#gb` on s4, books `#bk` on s6, brain `#br` on s7,
each an IIFE with an IntersectionObserver and a print `snap()`; read the D1 report `notes/_subreports/2026-09-20-289-D1-deck-v9.md`
for how they were ported). Output `notes/_DEMO-SLIDES-apollo-2026-09-20-v10.html`. Do not touch v9. No commit.

Dave's words for this pass (`notes/_lanes/289/DAVE-RULINGS-2026-09-20.md`, last four sections): "callipers are good" ·
"two robots spaced apart on either side of a conveyor belt" · "I'm seeing the visual metaphors as parts of the system whereas
we are also describing the parts of the metaphor … no harm in exploring both … the 5 explain more fully what the constituents
are" · "lets see it, we can refine any drawings later". His five: 1 Knowledge: books · 2 Proficiency: brain · 3 Parts: gears ·
4 Tools: arm · 5 Process: the line.

## Changes
1. **s5 The robots** gets the LINE SCENE: port `notes/_lanes/289/illustration/line.html` as canvas `#ln` + `#lnPrint`, in the
   same `.draw` card layout as s4/s6/s7 (type left, drawing right). Slide goes from grey text-only to the drawn layout (white).
2. **s8 The inspector** gets the CALLIPERS: port `notes/_lanes/289/illustration/callipers.html` as `#cp` + `#cpPrint`, same
   layout. Drop the "d = 35.00 mm" caption and any scale bar. Slide goes from dark to the drawn layout (white).
3. **s10 What she is made of** becomes the FIVE-UP ANATOMY: h2 "Five things she is made of." Five cells in a row (extend
   `.grid4` → a `.grid5` rule, ≤ 8 lines of CSS), each cell a SMALL STATIC baked image of the drawing (use each drawing's
   resting-frame snap: the deck already bakes gb/bk/br at print time — instead bake ALL FIVE once on load into small
   `<img>`s ~200px wide; the arm needs porting too as `#am` for this purpose, it can live off-screen in a hidden canvas) with
   the label + one line under each: **Parts** — gears — "the inventory: 137 components in code" · **Knowledge** — books —
   "standards, accessibility, rulings, governance, usage, theory — one graph" · **Proficiency** — brain — "the judgement to
   compose from it" · **Tools** — arm — "the host agent, in the editor designers already have" · **Process** — the line —
   "runbooks: how a build is generated, retrieved and reviewed". Foot: "Three roles in the story — the inventory, the assembly
   engineer, the inspector — and this is what the engineer is made of."
   If baking five canvases on load is too slow or fragile, fall back to five small live canvases that draw once (no idle,
   no orbit) — say which you did.
4. **s2 The strip** — cut to the five chapters Dave says aloud: 1 Why now · 2 The line · 3 The robots · 4 What we built
   (inventory · engineer · inspector) · 5 The build and the ask. One row.
5. Renumber nothing else; 12 slides stay 12. Keep every `rv d1…d5`. Print: the new canvases bake like the others.

## Verify
Render with playwright (`export LD_LIBRARY_PATH=$HOME/.local/lib`), 1440×810, every slide to
`notes/_lanes/289/deck/render-v10/sNN.png`; zero page errors, zero overflow; LOOK at s2, s5, s8, s10 — the canvases drawn,
the five-up legible. Print screenshots of s5, s8, s10. Report `notes/_subreports/2026-09-20-289-D2-deck-v10.md` (<50 lines).
Reply with an 8-line summary.
