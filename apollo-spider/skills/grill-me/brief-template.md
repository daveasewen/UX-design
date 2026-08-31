# Grill brief — <task name>

Date: <YYYY-MM-DD>
Task: <one line: what is being designed, and for whom>

| # | question | answer |
|---|---|---|
| 1 | Theme | <Mono / Common / Console / Supercharge> |
| 2 | Light, dark or both | <both / light only / dark only> |
| 3 | Density and width | <comfortable or compact · target width> |
| 4 | Brand assets | <what, and where they are — or "none" / "not yet"> |
| 5 | Data | <real (where it is) / placeholder> |
| 6 | Fixed and off-limits | <accessibility and other commitments · what the system must not do> |

Skipped: <list the question numbers skipped, or "none">
Defaults used: <e.g. "Q1 skipped — proceeding with Mono, announced 2026-08-30", or "none">

Notes: <anything the designer said that doesn't fit a row — keep their words>

---

Filled example:

# Grill brief — payments dashboard

Date: 2026-08-30
Task: Treasury overview dashboard for corporate international banking, internal users.

| # | question | answer |
|---|---|---|
| 1 | Theme | **skipped — proceeding with Mono, announced 2026-08-30. Every corner square by design.** |
| 2 | Light, dark or both | Both |
| 3 | Density and width | Compact; wide desktop, people have it open all day |
| 4 | Brand assets | Logo in `assets/brand/`; no photography |
| 5 | Data | Real — 12 payments in `data/payments.csv` |
| 6 | Fixed and off-limits | Keyboard-only must work end to end. Don't invent components; don't animate the figures |

Skipped: 1
Defaults used: Q1 skipped — Mono, announced before the build started

Notes: Amounts stay in their own currency, no conversion in the row.
