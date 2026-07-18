---
name: nav-pattern-catalog
description: "Nav research catalog DONE 2026-07-15 (reviews/NAV-PATTERN-CATALOG-2026-07-15.html + artifact). Tranche 7 (nav) BUILT + gated 2026-07-15 = Popover/NavToggle, GlobalHeader, SideNav, MegaMenu (3 variants), Drawer+NavAccordion. Tranche 8 still proposed."
metadata:
  node_type: memory
  type: project
---

**Apollo Navigation Pattern Catalog — built 2026-07-15** (Dave asked for comprehensive nav research while he finds the
Figma files). Deliverable: `reviews/NAV-PATTERN-CATALOG-2026-07-15.html` + desktop artifact `apollo-nav-pattern-catalog`.
Built from a **deep-research** workflow (26 sources, 117 claims → 24 verified adversarially; NN/g · W3C ARIA APG · Baymard ·
IBM Carbon · Shopify Polaris · Material 3) synthesised with design-system craft into an Apollo-oriented reference.

**Coverage (all families Dave listed + more):** A primary/global (top bar: exposed / burger-only / hybrid; utility nav) ·
B menus (mega-menu variants: multi-column/featured/tabbed/image-led/mixed; dropdown; fly-out=discouraged; split button) ·
C side/vertical (persistent/collapsible/tree/icon-rail) · D overlay (drawer/off-canvas, sheet, popover) · E in-page
(anchor/scroll-spy, sub-nav, tabs-as-nav) · F wayfinding (breadcrumb, pagination, back-to-top, step/wizard) · G contextual
("you may also be interested in", related, footer/fat-footer, sitemap) · H mobile (bottom tab bar, hamburger+accordion,
priority+/more, sticky action bar). Each: definition · use/avoid · variants · responsive · a11y · pitfalls · Apollo component.
Plus a **responsive-transformation matrix** (mobile patterns are mostly responsive STATES of desktop organisms) and a
**single a11y model**.

**Key verified evidence (drives defaults):**
- **Exposed beats hidden** — NN/g: hiding nav cut discoverability >20%, slowed tasks ~39% desktop / ~15% mobile; labelled
  combination pattern 89% vs 44% usage. ⇒ default EXPOSED top-level; collapse only when needed and LABEL the toggle.
- **Click not hover** to open submenus (touch/keyboard); hover-intent timing (~0.1s in / 0.5s out) if hover added.
- **Disclosure pattern, NOT menu/menubar**, for site nav (button + aria-expanded + aria-controls; Esc closes+returns focus);
  menu/menubar roles are for application command menus. Two-tier keyboard (Tab between, arrows within). (Refuted: general nav
  is NOT a single roving-tabindex composite.)
- **Mega menu over cascading fly-outs**; **real destinations at top level**, not under generic umbrellas.
- Caveat: NN/g figures are ~2016 browse/e-commerce; direction robust but validate against HSBC analytics for authenticated flows.

**✅ TRANCHE 7 BUILT + GATED — 2026-07-15** (Dave: "It looks great, and I think you should just build it").
`knowledge/_proforma/Tranche-7-interactive.html` + artifact `apollo-tranche-7-navigation`. Built via Sonnet from
`_TRANCHE-7-SPEC.md`; all FOUR gates green (`_check_proforma` + universal + DEF-003 CSS-governed + DEF-004 no-hardcode);
44/44 real icons. **5 sections, atoms tagged:**
1. **Popover + NavToggle** (primitive/atom) — disclosure toggle (aria-expanded/-controls), CSS-reveal popover, outside-click + Esc dismiss, focus returns to trigger.
2. **GlobalHeader** (organism) — brand + Primary `<nav>` of `.navlink`s (current = `aria-current="page"` + 2px `--bw-md` ink underbar, NOT colour) + Utility nav; `@container` responsive wide→priority+→hamburger.
3. **SideNav** (organism) — `.navitem` list + `.navgroup` disclosures + rail toggle (`i-collapse`/`i-expand`) → icon-only rail with tooltip labels (reuses T4 Tooltip).
4. **MegaMenu** (organism) — three variants shown: `.cols` (columns), `.featured` (columns + FeatureCard, reuses T5 Card via mono-tokenised `.mm-feature`), `.tabbed` (T4 Tabs switching panel). Disclosure, no focus-trap.
5. **Drawer + NavAccordion** (organism/molecule) — generalised T1 drawer with edge-*/modal classes; MODAL = role=dialog + aria-modal + focus-trap + Esc-close + return-focus + inert bg; `.navacc` nested disclosure = the mobile form of 2–4.
**4 new real icons** added (geometry copied from assets): `i-menu` `i-home` `i-collapse` `i-expand`. Generic `makeDisclosure`
JS helper drives all toggles (behaviour only, no JS motion). Fixed a build defect: the featured-card markup used `.card-link`
classes with no CSS → browser-default blue/concatenated render; fixed with mono-tokenised `.mm-feature` styling.

**Tranche 8** (proposed, later) = BottomTabBar+More · InPageNav/scroll-spy · FooterNav · RelatedLinks/Cards · Journey **Stepper**.

**Notes:** the nav tranche is heavily a COMPOSITION exercise (reuses IconButton, Tooltip, Tabs, Breadcrumb, Pagination,
Segmented, Card, Badge, Drawer, Actionbar) — a strong proof of the pro-forma "compose, don't re-invent" claim. All will inherit
the Figma type/colour tokens ([[type-system-tokens]]) when they land. Fits ATOMISE + no-hardcode/mode-governed ([[apollo-mono]]).
See [[proforma-programme]], [[apollo-component-library-itinerary]].
