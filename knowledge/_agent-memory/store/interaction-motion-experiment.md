---
name: interaction-motion-experiment
description: "Scale-physics. RULED: motion is SUBTLE, pure-CSS scale tokens (NO JS; DEF-003), and SIZE-BUCKETED so travel ≈1px/side at every surface width (07-15)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 452a0a17-6e63-4feb-ad8c-b23dfebbbd1b
---

Scale-physics motion = **attract on hover** (grow toward the cursor) + **depress on press** (recede + slight brightness). Scale only — NO shadow, NO translate (brand stays flat/angular). Chosen over 3D-depress (translate + inset shadow) which clashes with the brand.

**State (2026-06-22):** IN CANON on Button (`snippets/Button.reference.html`); experimental on Selection-controls. NOT universal — apply CASE-BY-CASE (discrete free-standing controls grow+depress; layout-bound elements like tabs/rows/links don't). A dedicated MOTION-REFINEMENT pass was owed.

---

**RULED 2026-07-15 (Dave) — motion is SUBTLE, and governed by pure CSS tokens (NO JS).** Two rulings, same day:

1. **Subtler is canon.** Reviewing the pro-forma, the `.btn` buttons grew 7px (the Button.reference/DEF-001
   width-derived magnitude) vs the icon buttons' ~2px. Dave: "the subtler interactions are better, make it canon
   for all." → dial everything to the icon-button subtlety (~2px). Supersedes the 7px magnitude.

2. **CSS + tokens, no JS (the important one).** The subtlety was first done with a `sizeScale()` JS helper
   (measured each button's width → set `--hs`/`--ps` for a constant-px scale). Dave flagged this as the root
   problem: "**as little JS as possible; CSS and tokens should govern everything**… this library must be portable…
   transfer it to Figma when complete." → **`sizeScale()` REMOVED entirely.** Motion is now pure-CSS **scale-factor
   tokens**, applied directly (`transform:scale(var(--btn-grow))`).

**Enforcement:** **DEF-003** gate — `knowledge/_validate_css_governed.py`, wired into `_build_all.py`; flags
`sizeScale`, JS setting `--hs`/`--ps`, or `.style.transform=scale`. Self-tested. Rule 14 in `_PROFORMA-RULES.md`.
See [[robustness-portability]] (CSS-first / Figma principle), [[type-rule-sentence-case]] (pro-forma = house standard).

---

**REFINED 2026-07-15 (Dave) — SIZE-BUCKETED tokens so absolute travel is ~1px/side at ANY surface width.**
Follow-up to ruling #2's accepted trade-off ("CSS scale is a percentage, so absolute px varies with width"). Dave,
re a Stack Overflow link on pixel-scaling + "could we have an enclosing element that crops": I explained pure CSS
**can't** read an element's rendered width into `calc()`, so true constant-px needs JS (banned) — and crucially the
**same limit exists in Figma** (prototypes scale by %, variables can't read node width), so staying proportional keeps
the library and its future Figma twin in lockstep. Dave: **"I think there's value in [bucketing]… there are cards
that scale as well, and I'd like it to be as consistent as possible."**

The fix = **size-scoped token buckets**, one per surface-size class, each factor = `1 ± 2/W` for ~1px/side travel:
- `--ib-grow: 1.045; --ib-press: 0.955;` — small controls (~44px): `.ib`, `.pg-num`. Unchanged (already right).
- `--btn-grow: 1.02; --btn-press: 0.98;` — buttons (~120px): `.btn`, `.pb-action`. Unchanged.
- `--card-grow: 1.007; --card-press: 0.993;` — **NEW**, large surfaces (~275px): `.card-link`.

**Root cause it fixed:** the card *borrowed* `--btn-grow` (1.02) but a `.card` is a `minmax(262px,1fr)` grid track
(~277px rendered) vs a button's ~75–120px, so it lunged **~2.77px/side** — ~2.5–3× the buttons. That was the
inconsistency Dave saw. Render-measured proof (T5, headless): card **2.77 → 0.97px/side**; icon 0.81; button 0.76
(a `.sm`) up to ~1.2–1.5 (default). Now all in a tight ~1px band. Gate-green (universal + DEF-003), written to all 5
tranches on-device.

**Chosen** "match buttons ~1px" over "slight extra lift ~1.5px" (`--card-grow`≈1.011) — the card already has its
subtle shadow to carry elevation, so scale just needs to match. Reversible = one token value if review wants more lift.

**Fixed-size accents are OUT of scope by design** (checkbox tick, radio dot, chip ×, avatar, date cells, segmented):
their size is *known/fixed*, so their pixel travel is already constant by construction — the checkbox even uses the
exact pure-CSS constant-px idiom `scale(calc(1 + 1.5/20))` on its 20px box. Bucketing only matters for **auto-width**
surfaces (buttons, cards) whose width CSS can't read.

**TODO (holdout):** the gated snippet canon — Button/Modals/Quick-actions/Selection-controls + generated `canon.css`
+ ~8 fitness-tests — still uses the JS `GROW=7`. A focused CSS-migration pass through that pipeline is owed
(bigger than it looks; the pro-forma is the go-forward standard so it can be scheduled deliberately).

Related: [[gated-snippets-and-motion]], [[component-review-program]], [[robustness-portability]].
