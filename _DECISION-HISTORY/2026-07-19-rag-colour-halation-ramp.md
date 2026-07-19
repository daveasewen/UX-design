# 2026-07-19 · RAG colour — halation, the salience ramp, and the astigmatism instrument

> Spine entry: `_LIVE-STATE.md` → RAG colours (R-D6…R-D9). Ledger: `knowledge/_proforma/_RAG-DECISIONS.md`.
> RESURRECT: the bloom/dance model + isoluminant/ramp/halation toolkit → **Apollo Labs** (`_FUTURE-STATE`).
> Session review chain: `reviews/RAG-COLOURS-2026-07-19-v1 … v9` (each with its `.REVIEW` overlay).
> Lands whole per the archive rules; corrections get a new banner, never a silent rewrite.

This session began as "settle the RAG dark-mode opens" (v1) and turned into a piece of original
colour-accessibility method. Recording ALL the findings at Dave's request. Grouped by finding, each with
the WHY and where it's enacted.

---

## 1 · Red and yellow are the problem hues; blue and green are stable
Dave (astigmatic calibration): *"blue and green are stable, it's red and yellow that are the problem."*
Grounded in physiology — chromatic aberration is worst at the spectral extremes (long-wavelength red,
short-wavelength blue/violet); astigmatism smears those edges directionally. **Consequence for structure:**
the two "problem" hues each break the uniform pattern for a DIFFERENT reason and each carve out; the stable
pair (green + blue) carries the tuning. Memory: [[colour-stability-red-yellow-problem]].

## 2 · The carve-out structure
- **Red = carve-out for INSTABILITY.** Lever = **depth + white text**, NOT desaturation (desaturation cost
  readability — Dave: "calmer but less readable"). Deeper red raises white-text contrast AND lowers bloom
  together. RULED `#B92F1E`, white text, **mode-stable** (= the light-mode red; light+dark unify). R-D7.
- **Amber = carve-out for LIGHTNESS.** Can't be light enough to be amber and dark enough to contrast →
  black text + a separate darker glyph. `#F0B13A` bg / `#C58900` glyph. R-D3 (prior session).
- **Green + blue = the stable pair**, tuned (see the ramp, §7).

## 3 · Halation is a THIRD design axis (beyond hue and intensity) — R-D6
Two failure modes, both already levered in canon (`color/black` $note: "reduce the extremity of the edge —
the neutral-ground lever [luminance step] · its coloured-ground twin is the saturation ceiling ≤0.72"):
- **BLOOM** (irradiation): a bright feature spills across its edge; light-on-dark reads HEAVIER. Grows with
  bright-side luminance × step. **Visible on thick fields.** Lever = lower the luminance step (the digital-
  black `#1A1A1A` move).
- **DANCE** (chromatic edge instability, "jazz"): saturated colour at a THIN / high-spatial-frequency edge,
  worst when luminance contrast is low. Chromatic channel is low-pass (~4 c/deg). Lever = saturation ceiling.
Dave: *"thin lines and colour dance, thicker ones bloom… that's the halation effect."*

## 4 · Thickness / spatial frequency SELECTS the mode — the bloom/dance model
The new dimension WCAG's flat 4.5 ratio ignores (APCA only approximates via size/weight tables): **stroke
width, as degrees of visual angle, decides whether you get bloom or dance.** First-cut model
`reviews/_rag_bloom_model.py` (v0 heuristic; CSF + chromatic aberration; stroke width → visual angle → CSF
weighting). Sanity holds: white fill = bloom 100, saturated-blue-1px-text = dance 100, and the SAME blue as
a thick fill has dance ≈ 1 — thickness killing the mode, exactly as Dave described. Saturation-cap (chroma
×0.72) drops dance ~28% at ~zero WCAG-contrast cost.

## 5 · Weight polarity, and the light-bleed rule — R-D7
The bright side always blooms into the dark side:
- **Light text on a bright/dark ground** (page, red) → stroke FATTENS → step **down** (400).
- **Dark text on a light fill** (amber, green, blue) → fill blooms inward, THINS the text → step **up** (500).
Model confirms across all grounds. **Also settles the step-down-on-colour hypothesis:** light-bleed
compensation is high on the page (bloom ~29) and small on colour (~2–7) → weight compensation belongs on the
page, not on colour. **RESOLVED to uniform Medium 500** ("medium is best on balance") — the polarity is the
true WHY but the shipped rule is one weight, chosen for simplicity + the dual-observer tension (a mixed split
could read "weird for normally sighted"). Polarity kept as rationale, not a token.

## 6 · The astigmatism calibration instrument + dual-observer principle
Dave: *"this is where my astigmatism is actually a benefit."* Astigmatism = heightened sensitivity to
bloom/dance = a STRICTER test. Calibrating to the most sensitive observer → an accessibility gold-standard.
**Dual-observer principle** (`_FUTURE-STATE`): serve the sensitive observer without breaking the typical one,
and FLAG where they diverge. Shapes Apollo Labs (report both observers) and every future colour call.

## 7 · Status colour is a SALIENCE RAMP, not isoluminant — R-D9 (the session's biggest reframe)
Dave: *"so it's not isoluminance for this, it's actually a ramp."*
- **Categorical / series data → ISOLUMINANT** (match L; no category should dominate — the dataviz rule).
- **Status / hierarchical data → SALIENCE RAMP** (loudness DESCENDS with severity: red › amber › green › blue).
The v7 isoluminant set exposed why: green sat BELOW blue in salience — felt recessive. The ramp fixes it.
**Salience metric** = mean OKLab distance of (fill, text) from the page. Memory:
[[colour-salience-ramp-vs-isoluminant]]. **The emergent salience order matched the semantics for free** —
red/amber (warnings) shout, green/blue (states) are calm — which Dave read as "feature not a bug".

## 8 · Mode-stable RAG
The light-mode RAG values are already near-isoluminant (red/green/blue OKLab L 0.52–0.54, spread 0.024) and
carry their text in both modes → RAG can collapse to ONE set per hue, both modes. Red + amber already
mode-stable by ruling; green/blue's light values work in dark too, closing the long-standing dark-green null
by REUSE (no new value needed) before the ramp re-tuned them. R-D8.

## 9 · Blue is the stubborn hue (open at session end)
Short wavelength + astigmatism = blue edges blur no matter what. Levers that help: **text luminance
contrast** (sharp even when colour blurs → lighter blue + black text, or deep blue + white text) and
**reduced chroma** (less colour edge to smear); a **cyan/teal shift** often focuses better. The tension:
every readability gain makes blue lighter → raises its salience toward green → so green re-seats above it to
hold the ramp. Left OPEN on `reviews/RAG-COLOURS-2026-07-19-v9` for Dave's eye (candidates: light-desat
`#7594C0`, cyan-shift `#5F92B9`, greyer `#89A0C1`, deep-white `#22569F`).

## 10 · Glyph contrast is relative to whether the glyph carries meaning — R-D6
Label-paired glyph → colour is reinforcement → 3:1 non-text floor suffices (a brighter hue is fine).
Meaning-carrying glyph (arrows, colour-only status, bare-number label) → must meet 4.5 text. Refines the
belt-&-braces rule and `{#icon-013}`.

---

## The resolved set at session end (pending final blue pin + red-page flag + §1 manifestation)
| severity | value | text | salience | status |
|---|---|---|---|---|
| breach | `#B92F1E` | white | 56.6 | RULED (R-D7); red-vs-page 2.89 flag, steer keep deep |
| watch | `#F0B13A` / glyph `#C58900` | black | 40.9 | RULED (R-D3) |
| healthy | `#36A467` (re-seats up if blue lightens) | black | 33.1 | ramp-tuned, near-final |
| info (blue) | pending v9 pin | black (or white if deep) | ~32–35 | OPEN — readability |

Weight uniform Medium 500. Marks icon or label-paired (never bare coloured text on dark). Mode-stable.
Chosen "Set 2": red alone in white; green/blue/amber black text.

## Spin-outs / experiments seeded (in `_FUTURE-STATE`)
- **Apollo Labs** — public a11y microtool; engine = isoluminant + salience-ramp + halation, reporting both
  observers. Dave: "this is good for colour palettes" (the ramp enriches Labs, doesn't retire it).
- **Whole-palette isoluminant + halation sweep** — run the method across every hue family/step.
- **Variable Univers ~450 rung** — font-procurement target (no weight between 400 and 500 today).

## Still OPEN
1. Final **blue** value (v9 eyeball). 2. **Red-vs-page 2.89** (keep deep vs lift). 3. **§1 manifestation**
(cell / pill / dot+label / bar). Then enact token promotion behind the blast-radius gate.

---

## SESSION CONTINUED (same day, 2026-07-19 — marked addition, not a rewrite of the above)

*Per the archive rule (lands whole, corrections appended not silently edited). The §9 "blue OPEN" above
resolved later the same session, and a further correction surfaced:*

- **Blue NAILED → `#5F92B9` (cyan-shift), green re-seated → `#43AD6F`; full dark set LOCKED (R-D10).** The
  cyan shift moves blue off the short-wavelength blue that astigmatism blurs worst; green lifts to stay above
  blue in the ramp. Red-vs-page 2.89 flag resolved: keep deep (white text carries the signal).
- **★ R-D11 CORRECTION — status FILLS are NOT mode-stable.** Dave's screenshot of the filled cells on the
  LIGHT page exposed it: the whole set was tuned against the dark page, and **the salience ramp is
  GROUND-RELATIVE — it inverts light↔dark.** On white the light fills (green/blue/amber) wash out
  (fill-vs-white < 3) and the deep-red breach becomes the QUIETEST cell (alarm recedes). So "mode-stable
  fills" (claimed R-D8/R-D10) is WRONG for the fill role. **The dark set stands; the LIGHT-mode fill set is
  reopened** and needs its own ground-aware derivation. The dot+label (glyph-on-page) form may still be
  near-mode-stable (smaller object). This is the lesson of the day's tail: *tune per ground, and prove a
  colour-set on BOTH grounds before calling it mode-stable.*
- **Process:** the narrative dossier itself became a **closing-ritual step (1b)** this session, and the idea of
  wiring dossiers into the decision graph (why/how node-set) was registered (`_FUTURE-STATE`).

---

## SESSION 3 (2026-07-19, later — "RAG light fills: proving per-mode, and a tuner") — marked continuation

*Separate session, appended not merged (archive rule). This is the LIGHT-fill pass R-D11 parked. Ledger: R-D12…R-D14.*

**The arc, and the WHY behind each move:**

1. **The salience metric inverts on white — a real method finding.** Reconstructed the R-D9 salience metric
   (mean OKLab dist of fill+text from page) into `reviews/_rag_light_fills_calc.py`. On white it MIS-RANKS: white
   text sits at zero distance from a white page, so it penalises the very cell (breach) that should shout. ⇒ on
   white, order the ramp by **fill-vs-page + chroma**, not the dark-page salience metric. The metric is
   ground-shaped, not universal.
2. **Amber is the structural blocker — then it isn't.** Amber's identity is lightness, so on white it can't hold a
   fill boundary (1.90) without a border or going brown (R-D3-barred). I built v1/v2 around solving that. **Dave
   killed borders** (*"cant have lines its not part of the aesthetic"* — R-D12 A) and **corrected me on amber**:
   *"amber is fine, it has a label that carries the meaning… we've ruled on this already."* That is R-D6 Ruling A,
   which I'd walked past — the **stale-reading failure mode** the CONSULT step exists to prevent. The deeper reframe
   (Dave: *"its not just about the colour"*): a status cell is a **labelled component**, so fill contrast is a
   **salience/scan lever, not an accessibility floor** — the floor is the label. This reframed everything after.
3. **Black text on the states (R-D12 B)** — Dave: *"black text… reinforces the salience"* (red loud/white, states
   calm/black). Forced green/blue lighter (the R-D4 values were too dark for black text, < AA).
4. **The tuning spiral, and the tuner.** Green "pop"→desaturate, blue purple→lighter→"toward true blue". After
   several round-trips Dave asked for *"a saturation slider, make it wide so i can fine tune"* → built an in-browser
   **OKLCh tuner** (v6), then a **two-mode tuner** (v7) when he said *"we need to adjust on dark too."* Ramp-guard
   reds if green ≤ blue on that ground. Lesson: past a couple of colour round-trips, **give the eye a live control**
   — it's faster and it's a reusable artefact (→ Apollo Labs).
5. **Per-mode PROVEN, not asserted.** Dave floated a mode-stable pair (#5EAE7C/#5898C6); it inverted on white. Then
   *"I want blue… same hue [as dark], changed my mind from the purple."* An exhaustive pair search settled it:
   **the instant green leads blue on white, blue leads on dark** — "louder" is darker on white but lighter on dark,
   so green can't lead on both. R-D11's per-mode claim is now a proof, not a lean.
6. **Locked (R-D14):** light green `#5DAC7B` / blue `#7DABCD` (H241, Option C); dark held at R-D10 (Option C's green
   came down to L0.68 ≈ dark's L0.67, so the modes harmonise without re-cutting dark). Red/amber mode-stable.
   Next: token promotion (Sonnet, blast-radius gate).

**Meta-lesson repeated from Session 1's tail:** *prove a colour set on BOTH grounds* — this time we did, and it
turned an assertion into a proof. And: **check the ruling before designing a solution** (amber, again).
