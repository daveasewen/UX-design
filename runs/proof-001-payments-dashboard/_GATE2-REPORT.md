# Gate 2 — assembly-tier report
*Screen: Business Banking · Payments (Route B — Figma Make, fresh generation from the shared prompt) · source: Figma Make code export, transcribed by hand from src/app/App.tsx (625 lines of React)*

**Verdict: ✅ PASS** — 0/6 blocking checks failed, 1/3 advisory flags.

## Blocking gates
- ✅ **DATA-1** — All cross-panel amounts reconcile.
- ✅ **DATA-2** — Stated total £106,302 ≥ shown rows £106,302.
- ✅ **DATA-3** — 'Covered through May' holds: balance £122,450 − scheduled £49,702 = £72,748.
- ✅ **A11Y-1** — All action-tile glyphs >= 3:1.
- ✅ **BRAND-1** — Red reserved for destructive actions.
- ✅ **FLOW-1** — High-value approvals require confirmation.

## Advisory
- ✅ **COPY-1** — Consistent currency format.
- 🟡 **COPY-2** — 7 all-caps labels/banners (readability).
- ✅ **PII-1** — Sort-code masking policy OK.
