# Route B gap log — building Tabs from the KB only

Recorded live while building `route-b-tabs-kb-only.html` from the knowledge base alone (meta, token stores, compliance, guidelines). Locked **before** the unconstrained Route A build, so nothing here is hindsight. Severity: 🔴 blocked me / had to invent · 🟡 underspecified, guessed · 🟢 KB strength.

## 🟢 What the KB got right (the wins)

1. **It caught its own design-system defect and shipped the fix.** `tabs.meta.json` flags P3 explicitly (selected indicator bound to the `color/primary` primitive, loses dark mode) AND the `tabs/*` mode-aware group actually exists in `semantic-colour.json` (`tabs/active` #DB0011→#FFFFFF, `tabs/standard-border`, `tabs/overflow-border`, `tabs/background`, `tabs/overflow-background`). So I could build it *correctly* — using `tabs/*` — guided by the meta. This is the system working as intended.
2. **Accessibility semantics were concrete and usable.** `role=tablist/tab/tabpanel`, `aria-selected`, roving tabindex, arrow keys, the "don't rely on red alone" anti-pattern, and the 6 WCAG SCs — enough to build a correct interaction + ARIA layer without guessing.
3. **Colour tokens resolved cleanly** with light/dark values, and the deprecated-token rebinds were named (`interactive(depricate)/on-light/surface/primary` → `tabs/background`).
4. **The 44px target** was explicitly stated (a11y.targetArea + 2.5.8) — the one dimension the KB actually pins.

## 🔴 Had to invent — KB silent

1. **Focus-ring spec — nothing, anywhere.** The KB cites 2.4.7 Focus Visible and 2.4.11 Focus Not Obscured but never defines what an HSBC focus indicator *is* — no thickness, colour, offset, or style token. I invented a 2px outline. For an accessibility-led system this is the most serious gap: the component is graded against focus criteria the KB gives no way to satisfy concretely.
2. **All component dimensions.** The meta specifies zero geometry: tab height (used 44px target as a proxy), internal padding (guessed `padding/fixed/medium` 16px), indicator thickness (guessed `border-width/large` 4px), track thickness (guessed `border-width/small` 1px), gap between tabs (guessed 0). None of these mappings are in the KB.
3. **Motion / transitions.** No motion guidance exists in the KB at all (no motion guideline was ingested). Invented 120ms ease for hover/selection.

## 🟡 Underspecified — guessed

4. **`font-weight: medium` is an unmapped string token** (`{"medium":"medium"}`), not a numeric weight — guessed CSS 500.
5. **`letter-spacing/font-5` is empty (`{}`)** in the store — omitted.
6. **`border-radius/default` has a null value** — couldn't use it; assumed square (0).
7. **Font family is proprietary** ("Univers Next for HSBC") with no web fallback stack specified — guessed Arial/Helvetica/sans-serif.
8. **Tab activation model** (automatic-follows-focus vs manual Enter/Space) not specified — chose ARIA-APG default (automatic).
9. **Overflow dropdown is underspecified.** The meta names it (trigger + menu of hidden tabs) and its tokens, but not the breakpoint/width that triggers overflow, how many tabs collapse, menu item height/sizing, or keyboard model for the menu. Built a basic version.
10. **`selected-first/middle/last` states** are listed as props but not explained (presumably indicator positioning at the bar edges) — inferred.

## 🟡 KB may be wrong / smells

11. **Dark-mode tab surface resolves to pure white.** `tabs/background` and `tabs/overflow-background` are `#FFFFFF` in **both** light and dark. With `background/default` dark = `#000000`, that paints a white tab bar on a black page in dark mode. `dark-mode.md` only gives generic "raise = lighter surface" elevation guidance — nothing tab-specific — so the KB can't tell me whether this is an intentional light island or a token-data error. Strong smell; flagged in the dark-mode audit's "flat" list.
12. **`tabs/*` group is incomplete.** It has active/background/border/overflow but **no hover or pressed surface tokens**, so interactive states still fall back to `tertiary/background/hover|pressed` — which are themselves flat white in dark mode. So even a "correct" full rewire to `tabs/*` leaves hover/pressed non-adapting in dark mode.
13. **Guideline mismatch.** `horizontal-scroll.md` is mapped to Tabs (xref) for overflow, but it's actually **carousel** guidance (hub nav, hero cards, credit-card carousel) — it does not cover the tab-overflow-dropdown pattern. The mapping is misleading; the only real overflow guidance is the meta's one-liner.

## Headline

The KB was **strong on correctness scaffolding** (tokens, ARIA, the SC list, and — impressively — its own defect + the fix) but **silent on everything that makes a component look and feel finished**: focus indicator, all geometry, motion, type detail. A coded result is *possible* and *accessible in structure*, but its visual quality is almost entirely my invention, not the KB's. That's the core finding to test against Route A.
