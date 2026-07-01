# Component gaps

Durable log of component SCOPE not yet built. We promote the reviewed baseline now and build the rest when prioritised.

| Component | Have (promoted) | Missing / to add | Logged |
|---|---|---|---|
| Modals | Dialog box (confirm/alert) — promoted as a dialog | **True modals** + **lightboxes**, for **desktop and mobile** — more variants exist in the HSBC Figma library (file `mI8hvIkV98nquoqWzKh5Kn`). Build these as their own gated snippets/variants. | 2026-06-29 (Dave) |
| Confirmation / success | Mobile success screen — animated, vertically centred (gated `.cn-confirmation`) | **Desktop variant** — wider / dialog-style layout (not full-bleed centred). Build as a variant once the desktop pattern is defined. | 2026-06-30 (Dave) |

## Token / system gaps (SME-Payments fitness tests, 2026-06-30)

Exposed by the portfolio run — the canon was silent in exactly the places it had to invent. Governance: `_FIXED-FLEX-CHARTER.md`.

| Gap | What's missing | Derive from | Logged |
|---|---|---|---|
| **Inverse / hero surface** | no light-mode dark-band role — the portfolio invented charcoals (`#0E1014`…) when canon dark values already exist | promote a semantic `inverse/surface` ramp from the existing dark-theme values (`#1D1D1D` / `#000000` / `#212121` / `#404040`) | 2026-06-30 |
| **Data-viz palette + chart primitives** | no chart components, no named data series — the waterfall / runway / proportional bars were invented | brand red + canon teal (`rag/success`) + neutrals; add a small named data-series scale | 2026-06-30 |
| **Register / craft tokens** | `--spring` / `--press` exist but are component-scoped (the portfolio re-invented its easings); no global elevation / gradient ramp for an *expressive* register | surface motion tokens globally; define an elevation + gradient ramp gated to the expressive register (pending the flatness decision in the charter) | 2026-06-30 |
