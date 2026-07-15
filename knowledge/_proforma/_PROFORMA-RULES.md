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

**⭐ PROMOTED 2026-07-14 (Dave asked):** the UNIVERSAL subset is now a real build gate. New
`knowledge/_validate_proforma.py` = a **mode-agnostic** gate wired into `knowledge/_build_all.py`
(step "pro-forma universal gate"). It auto-discovers every `_proforma/*.html` carrying an
`#icon-manifest` and enforces: real-icons-only · no-hardcode-colour · refs-resolve · icon-buttons-named
**+ a STRENGTHENED check that every manifest path resolves to a real asset file** (closes the
"fabricated path behind a real-looking manifest entry" hole `_check_proforma` left). So the pro-forma
surface is now gated on every `python3 knowledge/_build_all.py`, not just by hand. **MODE rules
(monochrome / near-black / colour=meaning / square) are deliberately NOT in this gate** — they are the
monochrome-base subset (this file); the main pipeline also carries brand-mode components that
legitimately re-add colour. `_check_proforma.py` stays as the single-file dev tool.

## Process (how we build + review)

- **A tranche = one self-contained interactive file** (light/dark toggle + width slider) as the
  **review surface**. Build + review a whole tranche in one file.
- **Split to per-component gated snippets at promotion** — when a tranche graduates into the gated
  set, each component becomes its own `snippets/<Name>.reference.html` + `meta.json` and runs the
  `_build_all.py` gates (incl. the new no-hardcode + glyph-presence checks) + the icon-asset rebase.
- Pro-forma WIP lives in `knowledge/_proforma/`; nothing touches the gated 38 until promoted.

---

## UPDATE 2026-07-14 — Tranches 2–5 built + RAG palette retrieved

**Tranches 2–5 built** as interactive monochrome files in `knowledge/_proforma/` (all gate-green,
rendered + inspected; verified on-device 5/5 pass incl. asset-path check):
- **T2** Toast · Alert/callout · Date picker · File upload
- **T3** Checkbox (tri-state) · Radio · Switch · Segmented · custom Select/listbox
- **T4** Tabs · Breadcrumb · Pagination · Accordion · Tooltip
- **T5** Card · Badge/Tag · Progress (bar/ring) · Avatar · Banner

**RAG palette — RETRIEVED from `tokens/semantic-colour.json` (not recalled)**, both themes, now in the
shared scaffold token blocks: `--err` #A8000B/#DB0011 · `--warn` #FFBB33 · `--success` #00847F ·
`--info` #305A85/#4587A7 (+ `-t` tints). **Accessible status pattern (LOCKED):** amber fails as text
(1.69:1 on white) → **status text stays ink; the RAG hue appears only on the status icon + a left accent
bar + a tint background; colour is never the sole carrier** (icon + label always present).

**Canon-pack method:** a shared **scaffold** (token blocks + base CSS + a 39-glyph sprite EXTRACTED from
the real asset files + manifest + `splice.py`) is filled by each tranche at three markers only, so
tokens/sprite/manifest can't drift. Control glyphs render `currentColor`; the 4 status badges keep their
real brand fills (colour = meaning).

*Open to confirm with Dave: (a) near-black shade (#1A1A1A); (b) two finesse taste-calls — T4 tooltip
info-badge (one blue dot) and T2 upload completed-bar going teal (both defensible as colour=meaning);
(c) whether a MODE-rule gate (monochrome/square) is wanted, or mode rules stay rules-not-gates.*

---

## UPDATE 2026-07-14 (review pass) — new rules from Dave's feedback

10. **ROUNDEL CARVE-OUT (Dave 2026-07-14).** The square-corners base rule (rule 4) has a carve-out:
    **circular atoms — Badge, Avatar, status pins/dots, and standard circular atoms — are EXEMPT and may be
    `border-radius:50%`.** Tags/chips are **NOT** exempt (they stay square — confirmed against `snippets/Tags.reference.html`,
    which says the same). Radio dots, switch thumbs, progress rings were already circular and are fine.

11. **COMMON INTERACTIVE STATE CLUSTER (Dave 2026-07-14).** Every interactive atom binds to the ONE canonical
    Button scale-physics — width-derived `--hs`/`--ps` (grow 7px hover / recede 9px + `brightness(.85)` press),
    set by `sizeScale()`; focus ring; disabled stays put; reduced-motion disables it. Buttons, icon-buttons, the
    clickable card, and stacked avatars all use it — **never a bespoke hover or a translate-based lift.** The
    scaffold `.btn`/`.ib` now carry it centrally. Recurrence is tracked as **DEF-001** in `_PROFORMA-DEFECTS.md`.

12. **GLYPH PRESENCE (reinforced — DEF-002).** A glyph must read against its own surface in EVERY state incl.
    disabled; never let a glyph's colour equal its surface. A CSS `fill:` on the wrapping `<svg>` does NOT override
    a `<symbol>` path's own `fill="currentColor"` — control the box's `color` instead. Build the glyph-presence
    gate (rule 7) to catch this class automatically.

13. **REUSE CALIBRATION (Dave 2026-07-14).** Reuse so prior work isn't wasted — but **deliberate, never the
    default.** Distinguish reusing the **decisions** (motion, a11y, state model, variants someone already reasoned
    through — mine these freely, incl. the brand-agnostic work in brand-mode snippets) from reusing the **artifact**
    (the snippet, brand skin and all — risky: it's brand-mode + may carry rolled-up/ATOMISE debt). Default = pull the
    decisions, rebuild clean for the monochrome base; bind to the artifact only where it genuinely fits. **Declare
    per component whether you're *mining* an existing snippet or *building fresh*, so Dave can veto either.**

North star (Dave 2026-07-14): make the pro-forma **as technically robust and flexible as possible** — everything is
reviewable and expected to take several passes; token-bound-by-intent so modes cascade with no re-code; fix once,
propagate (the button-motion fix is the exemplar). Robustness (gates, tracker) makes the flexibility safe to lean on.

## UPDATE 2026-07-15 — styling is CSS + token governed (portability / Figma)

14. **CSS + TOKENS GOVERN STYLING; JS IS BEHAVIOUR-ONLY (Dave 2026-07-15).** As little JS as possible:
    **motion, spacing, radii, colour** are governed by CSS + design tokens — never computed in JS. JS is
    for genuine **behaviour** (open/close, validation, focus management) and data-driven values (a progress
    width, a ring offset). *Why:* the library must be **portable**, and the target is a clean **Figma
    transfer** (tokens → Figma variables, CSS structure → components/auto-layout; JS logic does not
    transfer). Worked example — **motion**: the old `sizeScale()` JS (measuring each button's width to
    compute a constant-px scale) is replaced by pure-CSS scale-factor tokens — `--btn-grow`/`--btn-press`
    for buttons, `--ib-grow`/`--ib-press` for icon-buttons (size-scoped so each reads ~2px). Trade-off
    accepted (Dave, "within reason"): CSS scale is a percentage, so absolute px varies a little with width.
    Enforced by **DEF-003** (`_validate_css_governed.py`, wired into `_build_all.py`): flags `sizeScale`,
    JS setting `--hs`/`--ps`, or `.style.transform = scale`.
