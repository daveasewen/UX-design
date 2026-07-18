---
name: composition-layer-canon-css
description: The composition layer that fixes canon drift — shared knowledge/canon/canon.css; built + proven 2026-06-29
metadata: 
  node_type: memory
  type: project
  originSessionId: 19e99480-a06a-4f32-bf97-2b677a7876a2
---

LOCKED 2026-06-29 (Dave chose: **shared canon.css**, and proof scope **"extract all 32 first"**).
Fixes the composition gap proven in [[payments-journey-proof]]: snippets were standalone HTML, so
assembling a screen meant hand-re-coding each component → drift (list-item `__body` stacking bug;
button lost calibrated scale-physics, drifted to `scale(1.02/.97)` vs canon `1.04/.95`).

**Built — `knowledge/canon/canon.css` (4 layers, ~934 lines):**
1. AUTO-GENERATED token spine — `:root` + `[data-theme=dark]`, 343 vars + 116 dark, generated from
   `tokens/*.json` by `canon/gen_canon_tokens.py` (idempotent; rewrites only between AUTO markers,
   preserves hand layers). Names trace 1:1 to token paths. The anti-drift principle applied to the
   layer itself — the spine is generated, never hand-copied.
2. SEMANTIC ALIASES — the single reconciliation of the per-snippet local vocab (`--surface` →
   `var(--tertiary-background-default)` = #FFF/#1D1D1D raised; `--focus` → `--focus-ring`; rag; ink).
   Snippets each re-invented this by hand; now defined ONCE.
3. BASE + UTILITIES + JOURNEY/SCREEN PATTERNS (hand) — `.canon`, `.c-stack/row/grid/screen`, +
   gap-report missing patterns: `.c-actionbar`(sticky), `.c-summary`(k/v), `.c-stat-grid`,
   `.c-account-card`, `.c-tabbar`, `.c-choice-row`, `.c-eyebrow`.
4. AUTO-COMPONENTS — all 32 **GENERATED from the reviewed snippets** by `canon/gen_canon_components.py`,
   carried VERBATIM (every rule/state/reduced-motion + every decision comment) with theme colours→token
   refs, scoped `.cn-<component>`. Header per component carries Aria + atom-reuses + knownFindings +
   driftAllow reasons. **CORRECTION (same session):** my first pass HAND-retyped components and stripped
   comments → lost ~137 review decisions (Dave caught it). Fixed by generating from snippets instead:
   decision comments 37→**196**, all vars resolve. Snippets stay source-of-truth; canon regenerates.
   **2nd bug Dave caught (visual):** generator emitted `--X: var(--X)` when a snippet's local var name
   == the token css-var name (e.g. `--text-reverse`) → circular → button label lost contrast (dark on
   red). Fixed: skip the scope redef, let the global :root token provide it (flips in dark). 0 circular
   now. Motion was NOT lost — `.btn` rules are byte-identical to the snippet; full-width CTAs just don't
   hover-grow by canon's own `.btn.full:hover{transform:none}` rule (non-full measured scale 1.058 on
   hover). **3rd bug (dark mode, render-found):** aliases declared only on `:root` got substituted with
   LIGHT token values at :root and inherited down, so dark theme set on `<body>` didn't flip body text /
   gap-pattern colours (header title #333 on black). Fixed by declaring the alias block on
   `:root, [data-theme="light"], [data-theme="dark"]` so it re-resolves at whichever element carries the
   theme (works html OR body). RENDER UNBLOCKED (visual verification now possible — DO IT for UI work):
   playwright chromium via PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1 + local libXdamage.so.1
   (apt-get download libxdamage1 → dpkg-deb -x → LD_LIBRARY_PATH=outputs/libs). All 4 screens × light/dark
   verified clean.

**Proof:** `_fitness-test/payments-journey.canon.html` — same journey as drifted `payments-journey.html`
but hand CSS dropped **117 → ~20 lines** (harness only), 0 rogue hex/redefines, every component the gated
original (`.cn-*` scope + snippet markup). Gate + inner-class resolution PASS. Drift-points (list `__body`
stacking, button `1.04/.95` scale-physics) now live once in canon → can't silently recur.

**Gate (the composition TIER above the per-component rubric, called for in the proof):**
`knowledge/_validate_compose.py` — canon vars resolve + braces + spine markers; each `*.canon.html`
has 0 hex / 0 redefines / all `.c-*` resolve. **PASS.** Writes `_COMPOSE-AUDIT.md`.

**Migration path:** when Sutherland lands, `.c-*` classes map to React components via node IDs
([[code-binding-hub-spoke]]); canon.css is the Sutherland-independent layer that works today. Feeds
[[vision-contextual-dashboard]].

**4th decision-loss (Dave caught, cross-checked Figma node 45132-326648):** the journey's from-account
picker used my hand-authored gap-pattern `.c-choice-row` with a NATIVE `<input type=radio>` + `accent-color:red`
— reinventing the reviewed radio (which is grey `form/border/default` → ink `secondary/background/default`
dot, animated; NO red). The generated `.cn-selection-controls` radio was faithful; composition bypassed it.
Fixed: `.c-choice-row` is now LAYOUT-ONLY and composes the real `.cn-selection-controls .radio/.dot`;
added compose-gate check #7 (fail on `accent-color` / native radio-checkbox not built from cn-selection-controls).
**Root cause of ALL four losses = hand-authoring in the composition path** (hand-retype, generator bugs,
gap patterns). Generated `.cn-*` components are faithful; rule going forward: compose reviewed `.cn-*` for
anything that has a snippet, gap patterns are layout-only + must compose canon atoms for controls, and
**always render + visually verify** (static checks missed contrast/dark/radio — all visual). Remaining gap
patterns (account-card, summary, tab bar, confirmation/success, eyebrow) are un-reviewed placeholders →
review them into snippets so they generate into `.cn-*` too.

**Composition-fidelity audit (2026-06-29, Dave's method "go through the rest like the radio"):** diff each
journey component's MARKUP against its snippet's canonical markup (`strip <body>`, grep the component's
classes). Assume snippets are correct. Found the journey had dropped a11y/structure decisions during
composition: list rows missing `type=button` + avatar `role=img`/`aria-label` + `.trail` wrapper; progress
tracker missing `role=progressbar`+aria-value* + `aria-live` count + count-before-track order; input fields
used `<label class=lbl>` instead of `<div class=lbl><label for>` + help-text below instead of above +
missing `aria-describedby`; notification missing `role=status`; status chip dot missing `aria-hidden` +
label not in `<span>`. All fixed + re-rendered light/dark + gate PASS. Tags/links/buttons already faithful.
Method to REUSE for the rest of the journey/other screens. **5th loss (Dave caught — the notification):**
journey HAND-DREW the info icon (pale currentColor disk) instead of the library glyph; reviewed component
uses a `<symbol>` sprite + `<use href="#ic-info"/>` (solid accent disk + `--mark` knockout). ALL the journey's
icons were hand-approximated (back chevron, kebab, arrow ≠ exact `chevron-left`/`menu-more-vertical`/`arrow-right`
library paths → would fail `_validate_icons.py`). Fixed: added the reviewed sprite (ic-error/warning/success/
info/close + chevron-left/more/arrow-right, VERBATIM library paths) once per screen, wired notification (+dismiss
button), success icon, header back/more, arrow link via `<use>`. Only hand-drawn left = the 3 bottom-tab-bar
icons (`.c-tabbar` gap pattern, un-reviewed). RULE: never hand-draw an icon — `<use>` the library sprite.
**Dave's key steer: stop hand-auditing — RUN THE SCREEN THROUGH ALL THE GATES (the pipeline is built to
check many things).** Built `knowledge/_validate_screen.py [--render]`: runs each `*.canon.html` through the
SAME gates the snippets pass — compose + icon-source (`_validate_icons`) + a11y (`_validate_a11y`) +
rendered state-contrast (`_validate_state_contrast.audit_page` over every screen×light/dark driving real
hover/pressed). It immediately caught the 3 hand-drawn tab-bar icons; fixed with library glyphs
(home/card/add-payment). Journey now PASSES all four. Token-level gates (dark-surfaces, coverage) run
upstream on tokens/meta — canon inherits them. Run with the chromium env workaround (PLAYWRIGHT_SKIP_… +
LD_LIBRARY_PATH=outputs/libs). Writes `_SCREEN-GATE.md`.
Remaining un-reviewed gap patterns (account-card, summary, tab bar, confirmation, eyebrow) still to be reviewed into snippets.

Two generators: `canon/gen_canon_tokens.py` (tokens) + `canon/gen_canon_components.py` (components);
hand layers between the AUTO blocks are preserved. Runbook = `_RUNBOOK-compose-from-canon.md`.
**Known follow-ups (NOT done, by choice):** (1) wire `assets/icons/` sprite into composed screens for
the icon HARD gate ([[icon-source-rule]]) — journey still uses inline SVG; (2) dark RAG fix in source
tokens — canon faithfully MIRRORS the `#4587A7` leak ([[dark-rag-token-gaps]]); (3) promote the `.c-*`
gap patterns to gated snippets so they generate into `.cn-*` too.
Relates to [[pipeline-mental-model]] (this is the "harness/materials" composition layer made concrete).
