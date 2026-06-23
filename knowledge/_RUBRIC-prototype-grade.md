# Prototype-grade rubric — the "Tabs-bar standard"

*The yardstick for refining every reference snippet to demo-grade. Exemplar: `snippets/Tabs.reference.html`.*
*Why: high-res, component-compliant prototypes we can assemble **in the absence of Figma Make** — and the finesse that feeds Sutherland. The gates verify; this rubric is what we refine **toward**.*

## The 10 dimensions (what makes Tabs the exemplar)
| # | Dimension | What it means | Signal (auto) |
|---|-----------|---------------|---------------|
| 1 | **Token-faithful** | every colour is a resolved canon token; embedded `#token-manifest` maps var → token; `_validate_snippets.py` gates drift | `token-manifest` |
| 2 | **Dual theming, live** | light + dark, both token-faithful, working theme toggle + transition | `data-theme="dark"` |
| 3 | **Full state set** | default · hover · active/pressed · selected · disabled · focus, each styled | ≥4 state selectors |
| 4 | **Designed focus** | `focus/ring` token, `:focus-visible`, distinct from selection | `:focus-visible` |
| 5 | **Motion + reduced-motion** | canon motion tokens; `@media (prefers-reduced-motion)` escape hatch | `prefers-reduced-motion` |
| 6 | **Complete AT** | ARIA roles/attrs, keyboard model (arrows/Home/End/Esc), roving tabindex, ≥44px targets | role + aria- + keydown |
| 7 | **Explicit geometry** | heights/padding/widths/gaps from the meta `dimensions` block, not guessed | *manual* |
| 8 | **Real behaviour** | a working component (selection, menus, resize), not a static picture | `addEventListener` |
| 9 | **Edge & content states** | overflow, empty, loading, error, long-string handled where relevant | *manual* |
| 10 | **Brand compliance** | square corners (`border-radius:0`); no type-weight jump on selection; angular | `border-radius:0` |
| 11 | **Responsive / reflow** | adapts to available width — overflow collapses, works down to 320px (WCAG 1.4.10), no fixed-width lock | `ResizeObserver` / `@media` / `matchMedia` |

> **Dim 11 was added 2026-06-21 after Dave caught the exemplar itself lacking it** — the canon Tabs showed an overflow *menu* but never actually collapsed tabs into it. A reference that doesn't reflow isn't prototype-grade. Worked fix: `_fitness-test/tabs-responsive.html` (priority+ overflow via ResizeObserver, selected tab always kept visible).

> **Decided 2026-06-22 (option A) — passive atoms vs the AT signal.** The `AT(aria+kbd)` signal used to require a `keydown`/`keyup` handler, which assumes interactivity. Passive atoms (Status-indicator, Divider, Badge, Loading-indicator) are non-interactive **by design** — a keyboard handler would violate their own anti-patterns. **Resolution:** a component's meta may set `"interactive": false`; the scorer then credits AT for being exposed via `role`/`aria-live`/`aria-label` (4.1.3 / 1.4.1) instead of a keyboard handler. A passive component that exposes *nothing* still scores 0, so the bar stays meaningful — it measures the AT each component actually needs, rather than excluding the dimension. Effect: Status-indicator 8.5→9.0; Divider 5.0→6.0; Loading-indicator 5.5→6.0; Badge 6.0→7.0.

> **PENDING — decision B candidate (native-keyboard AT), flagged 2026-06-22.** The `AT(interactive)` signal demands a JS `keydown`/`keyup` handler, which UNDER-CREDITS components whose interactivity is NATIVE (`<a>` / `<button>` / native inputs) — they're fully keyboard-operable WITHOUT a JS handler (a `keydown` on a native `<a>` is redundant / an anti-pattern). This bit Selection-controls (native checkbox/radio/switch) and Cards (whole-card native `<a>` link). **BAND-AID used so far:** add a genuinely keyboard-driven sub-pattern so a real `keydown` exists (SC → chips radiogroup; Cards → selectable-card radiogroup). **ROOT-CAUSE FIX (make deliberately, like decision A):** credit AT for components keyboard-operable via native semantics + visible focus, not only a JS handler — guarded so a control exposing nothing still scores 0. Decide **before the native-link components (Links, Breadcrumbs, Pagination, Navigations)**, where bolting on a variant stops being honest.

## The bar
**Prototype-grade** = dimensions 1–6 + 8 + 10 + 11 fully met, and 7 + 9 reviewed for that component's relevant cases. Tabs is the reference; everything else is scored against it in `_PROTOTYPE-GRADE-AUDIT.md`.

## The refine loop (how to take a snippet to standard)
The agreed loop (from the strategy flag — convergent rubric, divergent taste, kept separate):
1. **Start from canon** — the current gated snippet + its meta (tokens, dimensions, a11y, anti-patterns).
2. **Generate 3–4 unconstrained variants** at the exploration tier (`_fitness-test/`, never gated) on meaningful axes — density, motion character, hierarchy.
3. **Dual critique** — score each against this rubric (convergent) + a taste pass (divergent); keep the line bright.
4. **Refine + promote the winner** into the gated snippet; update the meta; `python3 _build_all.py` must stay green.
5. **Re-audit** — the score should rise. That re-score is the progress metric, not another document.

## Priority toward the demo
Demo target = the **payments journey** (dashboard → make-a-payment → confirmation). Refine the components that journey needs first — see the ★ rows in `_PROTOTYPE-GRADE-AUDIT.md`.

*Scorer: `_build_prototype_grade_audit.py` → `_PROTOTYPE-GRADE-AUDIT.md` (advisory, non-gating).*
