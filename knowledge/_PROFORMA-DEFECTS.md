# Apollo pro-forma — recurring-defect tracker

Stood up 2026-07-14 (Dave: *"we need to track this error, it keeps happening"*). Log recurring
defects here so a fix isn't just a one-off — each entry names the **root cause** and the **prevention**
(the gate that stops it recurring). A defect isn't "closed" until its prevention exists.

Format: `ID · title · symptom · root cause · fix · prevention (gate) · status`.

---

## DEF-001 — interactive-atom motion diverges from the canonical Button scale-physics
- **Symptom (Dave, T5 card):** buttons "don't scale up" on hover; "the wrong hover and pressed state on
  the button atom… it keeps happening."
- **Root cause:** the pro-forma **scaffold** `.btn` put the hover-grow only on `.btn.pri`, at a flat 2px,
  not width-derived — while the canon (`snippets/Button.reference.html`, motion promoted 2026-06-22)
  applies it to **every** variant via `.btn:hover{transform:scale(var(--hs))}` with a **width-derived
  7px grow / 9px press + brightness(.85)**, set by a `sizeScale()` JS so absolute motion is constant at
  any size. Ghost/secondary buttons therefore never grew. Systemic (shared scaffold → recurs everywhere).
- **Fix (2026-07-14):** scaffold `.btn`/`.ib` re-bound to the canonical scale-physics verbatim + the
  `sizeScale()` JS added (also covers `.card-link`). One central change → every tranche corrected.
- **Prevention (TODO — the "state-cluster gate"):** a check that pro-forma interactive atoms bind to the
  shared cluster — flag any bespoke `transform:scale()` hover on `.btn/.ib/.card-link/.av` that isn't the
  canonical `var(--hs)/var(--ps)`. Until built, this file is the guard.
- **Status:** FIXED at the scaffold level (propagates to T2–T5). Gate = TODO.

## DEF-002 — glyph invisible on a same-value surface (checkbox tick "no tick")
- **Symptom (Dave, T3):** checked checkbox shows no tick.
- **Root cause:** the tick `<symbol>` path is `fill="currentColor"`; on the checked box `currentColor`
  resolved to `--ink` (dark) sitting on the `--pri` (near-black) fill = dark-on-dark, invisible. A CSS
  `fill:` on the wrapping svg does NOT override the path's own `fill="currentColor"`.
- **Fix (2026-07-14):** set the box `color:var(--icon-rev)` when `:checked`/`:indeterminate` so
  `currentColor` becomes the reversed (light) colour; tick + dash now read on the fill.
- **Prevention (TODO — the "glyph-presence gate", already proposed in `_PROFORMA-RULES.md` rule 7):**
  a render-based check that every glyph is ≥~1.3:1 against its own surface in every state incl. disabled.
- **Status:** FIXED (T3). Glyph-presence gate = TODO (build it; then this class can't recur silently).

---

*Both preventions are on the same theme as [[proforma-programme]]: a rule is only a guarantee once it's
gated. Build DEF-001's state-cluster gate and DEF-002's glyph-presence gate next time the gate work is open.*

## DEF-003 — styling (motion) computed in JS instead of CSS + tokens
- **Symptom (Dave, 2026-07-15):** the button scale-physics (`sizeScale()`) was JS — it had to run, re-run
  on resize, and reach every button, so it scattered across files and silently missed the JS-generated
  pagination/banner buttons; the 7px magnitude was hardcoded in JS in 4 snippets + fitness-tests too.
- **Root cause:** motion was built JS-first. Dave's principle: "as little JS as possible; CSS + tokens
  govern everything — motion, spacing, etc." (portability + a future Figma transfer, where JS doesn't map).
- **Fix (2026-07-15):** removed `sizeScale()`; motion is now pure-CSS scale-factor tokens `--btn-grow`/
  `--btn-press` (buttons) + `--ib-grow`/`--ib-press` (icon-buttons), applied directly in CSS. All 5 tranches migrated.
- **Prevention (BUILT — `_validate_css_governed.py`, wired into `_build_all.py`):** flags `sizeScale`, JS
  setting `--hs`/`--ps`, or `.style.transform = scale`. Self-tested (catches an injected `sizeScale`). Behaviour/data JS is not flagged.
- **Status:** FIXED + GATED (pro-forma). TODO: the gated snippet canon (Button/Modals/Quick-actions/Selection-controls + canon.css) still uses the JS `GROW=7` — migrate in a focused pass ([[interaction-motion-experiment]]).
