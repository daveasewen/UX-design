# Tranche 7 build spec — "Navigation" (Apollo MONO)

Build ONE self-contained interactive file: `knowledge/_proforma/Tranche-7-interactive.html`. Work in `/tmp/fix`.
MUST pass ALL FOUR: `_check_proforma.py <file>`, `_validate_proforma.py`, `_validate_css_governed.py` (DEF-003 no-JS-motion),
`_validate_no_hardcode.py` (DEF-004 no raw styling px). Loop until all green. Design authority = the catalog at
`knowledge/reviews/NAV-PATTERN-CATALOG-2026-07-15.html` — follow its evidence-backed defaults.

## 0. SCAFFOLD — copy VERBATIM from the tokenised `Tranche-6-interactive.html`
Reuse its whole `<head>` (leading-trim rule; `:root` with ALL tokens `--space-* --bw-* --radius* --btn/--ib/--card/--accent-*`
motion + easings; BOTH `[data-theme]` blocks; base resets; scaffold classes `.top .ctrls .frame section .h .tag .sub .btn .ib
.toast`), the `.top` bar (width slider `#fw` + theme toggle), `.wrap>.frame#frame`, `.toast#toast`, the ENTIRE sprite +
`#icon-manifest`, and the base `<script>` (theme toggle, width slider, showToast, **data-modality** Tab/pointer wiring).
Change only `<title>` + top comment → "Tranche 7 · Navigation".

**HARD RULES (mono):** every styling value a TOKEN — spacing `var(--space-*)`, borders `var(--bw-*)`, radius `var(--radius*)`;
NO raw hex outside `[data-theme]` blocks; NO raw px in padding/margin/gap/border-width/border-radius (DEF-004). NO JS-driven
MOTION — motion via CSS scale/transition tokens only (DEF-003). **JS for BEHAVIOUR is expected and fine** (open/close, focus
management, keyboard handlers, responsive) — just not for animating styles. Real icons only. Sentence-case labels. `@container`
responsive + `@media (prefers-reduced-motion)`.

## 1. NEW REAL ICONS — read the asset files, copy geometry faithfully, fill→currentColor, add `<symbol>` + manifest entry
Add these (READ each SVG under `knowledge/assets/icons/`, take its path/geometry verbatim, set `fill="currentColor"`; declare in `#icon-manifest.icons`):
- `i-menu` → `global-controls/menu.svg` (hamburger)  · `i-home` → `global-controls/home.svg`
- `i-collapse` → `global-controls/collapse.svg`  · `i-expand` → `global-controls/expand.svg`
REUSE from the sprite (already present): `i-chevron-down/-up/-left/-right`, `i-close`, `i-search`, `i-more-h` (menu-more-horizontal), `i-add`.
NEVER invent a glyph; the gate checks every symbol maps to a real asset file.

## 2. THE A11Y SPINE (apply everywhere — from the catalog)
- Site nav uses the **DISCLOSURE** pattern: a real `<button>` with `aria-expanded` (true/false) + `aria-controls="{panelId}"`. **Do NOT** use `role="menu"/"menubar"` for navigation links.
- **Esc** closes any open panel/drawer and **returns focus** to its trigger. Wrap each nav region in `<nav>` with a distinct `aria-label`. Active item gets `aria-current="page"`. Provide a **skip-to-content** link first in the header DOM.
- Keyboard: Tab moves between components; links stay individually tabbable (nav is NOT a single roving-tabindex composite).

## 3. SECTIONS — each `.h` (h2 + `.tag`) + `.sub` + live demo + `.hintline`. Tag atom/molecule/organism. COMPOSE built atoms (reuse, don't reinvent).

### A. Popover + NavToggle — tag: primitive / atom
- `.navtoggle` = `<button class="ib navtoggle">` (reuse `.ib`) OR a text+icon toggle; carries `aria-expanded` + `aria-controls`; icon = `i-menu` or `i-chevron-down` that flips on expand (CSS rotate via a token-driven transition, NOT JS). States: default·hover·active·expanded·focus.
- `.popover` = anchored panel below the trigger (`position:absolute`), tokenised padding/border/radius, subtle CSS reveal (opacity/scale via `--ease`). Dismiss on outside-click + Esc; focus returns to trigger (JS behaviour).
- Demo: a toggle opening a short **disclosure** list of nav links. Show it open in the static demo so it's visible.

### B. Global header — tag: organism  (the composition root)
- `.gheader` = **brand** (`i-home` or wordmark, links to “/”, accessible name “Home”) + **primary** `<nav aria-label="Primary">` of `.navlink`s (exposed) + **utility** `<nav aria-label="Utility">` (search `.ib`, account `.navtoggle`). Skip-link first in DOM.
- `.navlink` atom: default·hover·**current** (`aria-current="page"` + a mono indicator — a 2px bottom bar `var(--bw-md)` in `--ink`, NOT colour)·focus.
- **Responsive via `@container`** (drive with the width slider): WIDE = all links exposed; MEDIUM = **priority+** (show the first N, roll the rest into a “More” `.navtoggle`→popover); NARROW = brand + `i-menu` hamburger `.navtoggle` (labelled) that opens the **Drawer** (section E) holding a `.navacc`.
- Show the three responsive states clearly (static mini-frames or via the slider).

### C. Side nav — tag: organism
- `.sidenav` = `<nav aria-label="Sections">` of `.navitem` (icon + label + `aria-current` + optional group chevron). `.navgroup` = **disclosure** (`.navtoggle` heading + nested `.navitem` list, aria-expanded). A **rail toggle** (`i-collapse`/`i-expand`) switches `.sidenav` ↔ `.sidenav.rail` (labels hidden, icons only). In rail mode each item shows its label as a **tooltip** on hover/focus (REUSE the T4 tooltip) AND keeps an `aria-label`.
- States: item default·hover·current·focus; group collapsed·expanded. Responsive: expanded → rail (medium) → Drawer (narrow).

### D. Mega menu — tag: organism
- A `.navtoggle` (in a mini header context) opens `.megamenu` — a wide panel. Build **three variants**, each shown:
  1. `.megamenu.cols` — 3–4 `.menugroup` (a heading + `<ul>` of `.menulink`).
  2. `.megamenu.featured` — columns + a **FeatureCard** (reuse the T5 `.card` / `.card-link`).
  3. `.megamenu.tabbed` — a left `.tabrail` (REUSE T4 Tabs) switching the right panel’s groups.
- **Disclosure**, not menu role. Panel = grouped links (`<h*>` + `<ul>`), Esc closes + returns focus, **no focus-trap** (it’s navigation). Reveal via CSS. Responsive: collapses to a nested `.navacc` (accordion) — show that note/demo.

### E. Drawer + NavAccordion — tag: organism / molecule
- `.drawer` — generalise the T1 drawer: props via classes `edge-left|edge-right|edge-top|edge-bottom` + `modal`. **Modal** drawer = `role="dialog"` + `aria-modal="true"` + **focus-trap** + Esc-close + **return focus to opener** + background made inert (e.g. `[inert]` or `aria-hidden` on the frame while open). Non-modal = push, no trap. Slide motion via the `--drawer` easing token (CSS only).
- `.navacc` = **NavAccordion**: a nested **disclosure** list (top `.navtoggle` rows expand their child link groups in place) — the MOBILE form of B/C/D. aria-expanded per level.
- Demo: a hamburger `.navtoggle` opening a **left modal `.drawer`** containing a `.navacc` (the mobile nav). This ties the tranche together.

## 4. ATOMS to expose + tag (Dave: catch atoms in the patterns)
`.navlink` · `.navitem` · `.navtoggle` · `.menugroup`/`.menulink` · `.navacc` item — define once, compose across sections.
Reuse (do NOT rebuild): T4 Tabs + Tooltip, T5 Card, T1 IconButton + Drawer motion, T5 Actionbar. Note reuse in comments.

## 5. Hard self-check (loop until all green)
- [ ] Component CSS: zero raw hex outside `[data-theme]`; zero raw px in spacing/border-width/border-radius (all tokens) — DEF-004.
- [ ] No JS-driven motion (motion via CSS/tokens) — DEF-003. `@container` responsive + reduced-motion present.
- [ ] Every `<symbol id>` in `#icon-manifest.icons` → a real asset file (incl. the 4 new). Every `<use href>` resolves. Every `.ib`/toggle has an accessible name.
- [ ] Disclosure buttons carry `aria-expanded` + `aria-controls`; Esc closes + returns focus; `aria-current="page"` on active items; skip-link present; nav landmarks labelled. Modal drawer traps focus + returns it; menus/mega-menu do NOT trap.
- [ ] No JS console errors.
Run `_check_proforma.py` on the file, then `_validate_proforma.py`, `_validate_css_governed.py`, `_validate_no_hardcode.py`; report the final PASS line of each.
