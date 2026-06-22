# Shared spec — A/B test · Business Banking Payments screen

*Station ① · the single input given to **both** generators (your canon composer + Figma Make).*
*Source of truth for every figure: `dataset.json`.*

## Scope — deliberately tight (read this)
**ONE screen, ONE job.** This is the *experiment*, so the spec is narrow on purpose: a clean, controlled
A/B beats a sprawling brief. Breadth — a multi-JTBD requirements doc that spawns several screens — is the
*demo* step, and it comes **after** the mechanism is proven on one screen. Widening now would just add noise
to the comparison (and contradicts your own "don't boil the ocean / minimum viable target" guardrail).

## The job-to-be-done
"As an SME finance admin, before any money moves, I need to confirm the business is solvent and
approve/reject pending payments with confidence — without re-checking the figures myself."

## What the screen must show
Cash position (opening · current · net movement · est. closing · inflows/outflows) · a solvency/coverage
statement · pending approvals · upcoming scheduled payments **with a stated total** · recent transactions.
**Every figure comes from `dataset.json` and must not be altered, rounded, or invented.**

## Acceptance criteria

### Enforceable → gate 2 (BLOCK — fails the build)
| ID | Criterion |
|----|-----------|
| DATA-1 | The same payee shows the **same amount** in every panel. |
| DATA-2 | The stated "upcoming total" **= the sum** of the listed rows. |
| DATA-3 | The coverage statement is **derivable from balance − scheduled obligations** for the period (incl. buffer). |
| DATA-4 | **Fidelity:** every figure matches `dataset.json` — nothing invented or rounded away. *(new vs proof-001; needs the dataset — gate 2 to be extended, or checked by hand for v1.)* |
| A11Y-1 | Non-text contrast **≥ 3:1** (1.4.11) on action glyphs / status. |
| BRAND-1 | **Red reserved** for destructive actions only. |
| FLOW-1 | High-value approval (> £10k) **requires a confirmation step**. |

### Advisory (WARN)
COPY-1 one currency format · COPY-2 no all-caps labels · PII-1 mask sort codes/accounts.

### Taste (human, never gated)
Visual hierarchy · emphasis of the primary action · whether to show a coverage banner at all.

## States to handle
loading · error (failed/rejected approval) · empty (no upcoming payments) · very long payee name · zero-fee.

---

## How to run the A/B
1. **Route A — composer (canon):** assemble the screen using **only** gated canon (snippets + tokens) + this
   spec; emit `route-A.screen.json`. Gate runs on it natively.
2. **Route B — Figma Make:** paste `figma-make-prompt.md` into a **blank** Figma Make (a generation, not a
   restyle of the old image); export; transcribe the result to `route-B.screen.json`. *(It emits pixels, not
   data — that transcription step is itself a finding: only one route is checkable by construction.)*
3. **Gate both:** `python3 ../proof-001-payments-dashboard/gate2_assembly.py route-A.screen.json` (and `-B`).
4. **Compare:** blocking pass/fail per route + the checkability asymmetry + a human taste pass on survivors.
   Write up in the Tabs fitness-test A/B format.

**Fairness guardrails:** identical information to both · gate checks must be standards-justifiable, not
composer-shaped · n=1 is a demo — repeat across a few specs before claiming a measured win.
