# Runbook — compose a screen from canon (the composition layer)

**Problem this solves** (proven in the payments-journey + SME walks): canon snippets were
standalone reference HTML. Assembling a screen meant hand-re-coding each component, which
drifted — the list-item title/sub stacking bug came back, and the button lost its calibrated
scale-physics (`scale(1.02/.97)` instead of canon's `1.04/.95`). There was no shared token +
component layer to compose from.

**The fix:** one importable stylesheet — `knowledge/canon/canon.css` — that every screen
*and* every snippet consumes. Composition becomes objective **selection + layout**; a composed
screen cannot silently drift because it has no component CSS of its own.

---

## What's in `canon/canon.css` (4 layers, top → bottom)

1. **AUTO-GENERATED TOKENS** — `:root` + `[data-theme="dark"]`, 343 vars + 116 dark overrides.
   Generated from `knowledge/tokens/*.json` by `gen_canon_tokens.py`; names trace 1:1 to token
   paths (`primary/background/hover` → `--primary-background-hover`). **Never hand-edit between
   the AUTO markers** — re-run the generator. This is the anti-drift spine.
2. **SEMANTIC ALIASES** — short ergonomic roles → semantic tokens (`--surface` →
   `var(--tertiary-background-default)`, `--focus` → `var(--focus-ring)`, …). This is the layer
   each snippet used to re-invent by hand; it lives **once** here now. Add an alias rather than
   re-deriving a colour in a component.
3. **BASE + LAYOUT UTILITIES** — `.canon` root, `.c-stack-*`, `.c-row`, `.c-grid`, `.c-screen`
   phone frame, plus the gap-report missing patterns: `.c-actionbar` (sticky), `.c-summary`
   (key/value), `.c-stat-grid`, `.c-account-card`, bottom `.c-tabbar`, `.c-choice-row`.
4. **AUTO-GENERATED COMPONENTS** — all 32, **generated from the reviewed snippets** by
   `canon/gen_canon_components.py`. Each component is carried **verbatim** (every rule, state,
   reduced-motion block AND every decision comment — handled a11y findings, contrast reasoning,
   non-colour press signals, `driftAllow` reasons), with its theme colours rewritten to token
   refs and its CSS scoped under `.cn-<component>` (e.g. `.cn-button`, `.cn-list-items`). A header
   comment per component carries its Aria contract, atom reuses, and known findings. The snippets
   are the source of truth (they are the final reviewed components); **never hand-edit between the
   AUTO-COMPONENTS markers** — edit the snippet and regenerate, so review decisions can't be lost.

## Compose a screen

1. Root element gets `class="canon"`, and **two** attributes on it (or `<body>`): the theme,
   `data-apollo-theme="common|console|supercharge"`, and the mode, `data-theme="light|dark"`.
   They are different dials — canon selects on both. `data-theme` cannot carry a theme, so a
   root with `data-theme` alone is a **mono** build (mono is the attribute-less baseline; every
   radius token is `0` there). `legacy` is the older key for `common` and still resolves
   (`s227-D8`), but new work emits `common`.
2. `<link rel="stylesheet" href="../canon/canon.css">`.
3. Drop in each component as **its scope class + the snippet's own markup**, e.g.
   `<div class="cn-button"><button class="btn primary full">…</button></div>` or
   `<div class="cn-list-items"><ul class="list"><li><button class="row">…</button></li></ul></div>`.
   Use the `.c-*` utilities + gap patterns for layout (`.c-stack-*`, `.c-actionbar`, `.c-summary`,
   `.c-account-card`, `.c-tabbar`, `.c-choice-row`). **The screen's own `<style>` is harness only —
   no `#hex`, no `.c-*`/`.cn-*` redefinitions.**
4. Worked example: `_fitness-test/payments-journey.canon.html` — same journey as the drifted
   `payments-journey.html`, but its hand-written CSS dropped from **117 lines → ~20** (harness
   only), 0 rogue hex, every component the gated original.

## Two inscribed lessons (from the 2026-07-05 restyle saga — history:
`_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md`; inscribed 2026-07-18 by ruling)

- **Theme-dependent alias blocks use the SAME selector list as the tokens they wrap — never a bare
  `:root`.** A bare `:root{ --ink: var(--page); }` computes once against `<html>`'s light values and
  inherits the frozen result under `[data-theme="dark"]`. Match canon's own pattern:
  `:root, [data-theme="dark"]{ … }`. This bug rendered a hero figure invisible and canon.css
  documents the trap at its own alias layer — check there before writing aliases.
- **A hand-built "canon-primitive" screen is a CLAIM the gate exists to check — run the gate as the
  LAST step before presenting, never when asked.** The restyle passed "on inference" until Dave asked
  directly; the real run then failed on hex refs + 3 unknown icon paths, and a follow-up contrast
  pass found four genuine 1.4.3 failures the shallow check missed. Gate + a real contrast check on
  any composition that is not a `.cn-*` snippet.

## Gate it — run the composed screen through the WHOLE pipeline, not a hand audit

```
python3 knowledge/_validate_screen.py --render        # all *.canon.html through every applicable gate
```
`_validate_screen.py` runs, on each composed screen, the SAME gates the snippets pass — so a
deviation fails the build instead of waiting for a human to spot it:
- **compose** (`_validate_compose`): 0 rogue hex, no `.c-*`/`.cn-*` redefinition, every class resolves,
  no native/`accent-color` control reinvention.
- **icon-source** (`_validate_icons`): every inline `<svg>` path must byte-match the `assets/icons`
  library (or be `data-bespoke`); shape-only icons flagged. (This is what caught the hand-drawn tab-bar
  icons after the radio + notification icon fixes.)
- **a11y** (`_validate_a11y`): reduced-motion present if it animates; target-size.
- **state-contrast** (`_validate_state_contrast`, `--render`): renders every screen × light/dark, drives
  real hover/pressed on each interactive element, checks computed contrast (the gate that closed the
  Cards 9/9 blind spot).
Writes `_SCREEN-GATE.md`. The token-level gates (`_validate_dark_surfaces`, `_validate_coverage`) run on
the token/meta layer upstream — canon inherits them, so they don't need re-running per screen.
`_validate_compose.py` alone still works for a quick structural-only check.

## Regenerate canon (the two generators — canon.css is generated, not hand-kept)

```
python3 canon/gen_canon_tokens.py        # tokens/*.json      -> AUTO-GENERATED TOKENS block
python3 canon/gen_canon_components.py     # snippets/*.html    -> AUTO-COMPONENTS block
python3 _validate_compose.py              # gate
```
Both rewrite only their AUTO block; the hand-authored aliases / utilities / gap patterns in
between are preserved. Idempotent.

## Add / change a component

Edit the **snippet** (`snippets/<Name>.reference.html`) — it's the reviewed source of truth and
stays covered by `_validate_snippets.py` (token-fidelity + a11y) and `_validate_icons.py`. Then
run `gen_canon_components.py`. Never hand-edit the component inside canon.css. New patterns that
aren't a snippet yet (account card, summary, stat grid…) live in the hand-authored
JOURNEY/SCREEN PATTERNS block as `.c-*`.

---

## Known follow-ups (deliberately not done this session)

- **Icon-source gate on composed screens** — `payments-journey.canon.html` uses inline SVG paths
  (like the original fitness-test). To bring composed screens under `_validate_icons.py`, wire the
  `assets/icons/` sprite (`<symbol>` + `<use>`) instead of inline paths.
- **Dark RAG token gaps** (`[[dark-rag-token-gaps]]`) — canon faithfully mirrors them
  (`--rag-information` dark = `#4587A7`, the illustration-blue leak that fails contrast). Fix
  belongs in `tokens/semantic-colour.json`, then re-run the generators.
- **Promote gap patterns to snippets** — the `.c-*` JOURNEY/SCREEN patterns aren't gated yet; once
  reviewed, give each a snippet so it generates into the `.cn-*` layer like the rest.
