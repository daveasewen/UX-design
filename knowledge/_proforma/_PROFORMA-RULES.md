# Apollo pro-forma — rules (living)

The small, cascadable rule-set the **pro-forma base** is built to. Kept growing as we discover rules
during the build (Dave: "let's build these rules as we go along, they will be used later"). Modes
(HSBC-brand, business-line) layer ON TOP of these — they never edit the base, they override tokens.

Status: WORKING DRAFT — started 2026-07-14 during Tranche 1. Confirm/adjust with Dave before it hardens.

---

## Base rules (the monochrome floor)

1. **Monochrome by default.** Primary / high-emphasis actions = **near-black `#1A1A1A`** (light) /
   near-white (dark). No brand red at the base. Dark inverts to near-white so emphasis is preserved.
2. **Colour = meaning only.** Colour is reserved for **status** (RAG: error / warning / success / info)
   and **data-viz**. Everything structural — actions, chrome, borders, text — is greyscale.
   - **Rationale (Dave 2026-07-14): red already means destruction + warning**, so it cannot also serve
     as a brand-primary accent without clashing. That clash is *why* the base is monochrome and red is
     pushed into meaning-only (and into the HSBC-brand mode as an explicit, owned choice).
   - In Tranche 1 the only hue anywhere is the amount-input error — which proves the rule at a glance.
3. **Token discipline.** Every visual value binds to a token **by intent** — never a hardcoded hex/rgb.
   Enforced by the **no-hardcode / scramble** check (scramble the token values → anything that doesn't
   move is a leak). All colour lives in the theme token blocks only.
4. **Square corners at the base.** Rounded corners are a **business-line mode** divergence, not the base.

## Interaction rules

5. **Every component carries live interactive states**, not just static state chips: real
   `:hover` / `:active` / `:focus-visible` **and** behaviour (drawer opens/closes, stepper navigates,
   skeleton loads, amount formats, toggles toggle). Seeing states in isolation is fine; the review
   surface must let you *interact*.
6. **Motion is subtle.** Hover = **+2px**, press = **−2px** (on the component's target size); press may
   add a small brightness recede. All motion honours `prefers-reduced-motion`.
7. **Glyph presence.** An icon glyph must be distinguishable from its own surface in **every** state
   incl. disabled (never bind a glyph to a token equal to its surface). Enforced by the proposed
   `glyph-presence` gate (~1.3:1 floor, distinct from the 3:1 non-text-contrast gate).
8. **Icons: real assets only — never invent silently.** Every glyph is built from a real file in
   `knowledge/assets/icons/` (sprite + `#icon-manifest` mapping each glyph → its source path). If a
   genuinely-needed glyph is **missing** from the library, an invented placeholder is allowed **only if
   flagged `provisional`** (`data-provenance="provisional"` on the symbol + logged to `_ICON-GAPS.md`)
   so a real one gets commissioned. Silent invention is a FAIL. (Rule tightened after invented glyphs
   slipped into an early tranche — see enforcement note below.)

## Responsive rules

8. **Responsive behaviour is required and must be demonstrable.** Components reflow to their container
   (container queries, not viewport), verified down to 320px. The review surface carries a **width
   slider** so reflow is visible without resizing. Canonical reflows: action bars **stack + go
   full-width, primary promoted to top** on narrow; dense rows scroll or stack; overlays cap width.

## Accessibility floor (non-negotiable, inherited from the KB)

9. WCAG **2.2 AA** floor: contrast, **44×44** targets, visible focus, programmatic name/role/value,
   status announced, colour never the sole carrier of meaning.

## Modes layer on top (do NOT edit the base)

- **HSBC-brand mode:** re-adds red as the primary accent + the "red used once per screen" rule +
  brand type. Red here is an owned, explicit brand choice — the base stays monochrome.
- **Business-line ("big sister") mode:** rounded corners + its own type stack + its own data-viz set;
  still monochrome-utilitarian, colour-for-meaning.
- Each mode is a **token override set** composed with light/dark — same component skeleton, different skin.

## Enforcement (rules must be gated, not hoped for)

Apollo's existing hard gates (`_validate_icons.py` = no invented icons, contrast, a11y, snippet,
coverage…) run inside `knowledge/_build_all.py` — but that only covers the **gated pipeline**
(`snippets/` + `components/*.meta.json`). The **pro-forma tranche files are a new surface** upstream of
that pipeline, so the existing gates never ran on them — which is how invented glyphs slipped through
2026-07-14. Fix: **`_check_proforma.py`** runs the same class of checks on every tranche file
(no unflagged invented icons · no hardcoded colour outside theme blocks · all `<use>` refs resolve ·
every icon-only button named) and MUST be green before a tranche is shown. Run it on every regenerate.
At promotion, the per-component split also runs the full `_build_all.py` gate set.

## Process (how we build + review)

- **A tranche = one self-contained interactive file** (light/dark toggle + width slider) as the
  **review surface**. Build + review a whole tranche in one file.
- **Split to per-component gated snippets at promotion** — when a tranche graduates into the gated
  set, each component becomes its own `snippets/<Name>.reference.html` + `meta.json` and runs the
  `_build_all.py` gates (incl. the new no-hardcode + glyph-presence checks) + the icon-asset rebase.
- Pro-forma WIP lives in `knowledge/_proforma/`; nothing touches the gated 38 until promoted.

---

*Open to confirm with Dave: near-black shade (#1A1A1A), and whether any of the above should move from
"rule" to "hard gate" now vs at promotion.*
