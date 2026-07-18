---
name: robustness-portability
description: "Portability/robustness bar — engine owns the plumbing; AND (07-15) the LIBRARY is CSS+token-governed, JS behaviour-only, so it's portable + Figma-transferable"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6d4d256-65cf-4438-9588-8f44138e09e2
---

**`knowledge/_ROBUSTNESS-PORTABILITY.md`** (drafted 2026-07-01). Dave's hard requirement: the synthesis engine is meant to be **portable** (used by non-us people on their own machines) — if they trip on plumbing before reaching the value, the governance is moot.

- **Principle:** the tool OWNS the plumbing; the user never sees a port, cache flag, segfault, lock file, or URL scheme. Zero-config is the product, not a nicety.
- **The visual-QA loop (render→critique→fix→re-render) is a CORE pipeline stage — the CRAFT gate** (governance gets the vocabulary right; the QA loop gets the finish right — different jobs, see [[fixed-flex-charter]]). It must be OWNED: bundled tested renderer (deps baked, can't segfault), auto fresh-fetch (no cache-bust), bounded timeout+retry (never silently hang), no user server/ports, and the loop AUTOMATED so the machine catches craft misses (padding, collisions) before the human.
- **Papercuts to engineer away** (all hit this session as duct tape): manual local server · single-thread deadlock · `?v=N` cache-busting · `file://` blocked · sandbox chromium segfault (exit 139) · extension "document idle" 45s hang · git index-lock · missing brand font. Each = a support ticket.
- **Why it matters:** the governance model is sound; the fragility is all ENVIRONMENTAL. A portable product must make the ground solid + invisible or people bounce off the tooling first.
- Current duct-tape recipe (what to replace) is in [[sandbox-html-rendering]]. See [[fixed-flex-charter]] [[promenaut-product-vision]] [[procedural-debt-and-method]].

---

**⭐ LIBRARY portability principle (RULED Dave 2026-07-15) — CSS + tokens govern styling; JS is behaviour-only.**
Distinct from the *engine* portability above: this is about the *component library* being portable. Dave:
"as little JS as possible; **CSS and tokens should govern everything — motion, spacing, etc.** (within reason);
this library must be portable — I thought it might be good to **transfer it to Figma when it's complete**."
- **Rule:** motion, spacing, radii, colour → CSS + design tokens, never computed in JS. JS only for genuine
  **behaviour** (open/close, validation, focus) and data-driven values (progress width, ring offset).
- **Why:** portability + a clean **Figma hand-off** — tokens → Figma variables, CSS structure → components/
  auto-layout; **JS logic does not transfer** to Figma at all. The more we hold the CSS-first line, the more the
  Figma transfer is a real option rather than a rebuild.
- **Trigger + worked example:** the button `sizeScale()` JS (measured each button's width to compute a constant-px
  scale) had scattered across files + silently missed JS-generated buttons. Replaced with pure-CSS **scale-factor
  tokens** (`--btn-grow`/`--btn-press` for buttons, `--ib-grow`/`--ib-press` for icon-buttons, size-scoped to
  ~2px). Gated as **DEF-003** (`_validate_css_governed.py`). See [[interaction-motion-experiment]], the rule 14 in
  `_proforma/_PROFORMA-RULES.md`, and the "pro-forma as house standard for HTML docs" direction [[type-rule-sentence-case]].
- **NB — the JS-motion sprawl is bigger than the pro-forma:** the gated snippet canon (Button/Modals/Quick-actions/
  Selection-controls + canon.css + ~8 fitness-tests) still hardcodes `GROW=7` in JS — a focused CSS-migration pass is owed there.
