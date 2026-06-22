# Screen spec — Business Banking · Payments dashboard

*Station ① output. The **enforceable** criteria below ARE station ③ (gate 2).*
*Source screen: Figma Make export (Business Banking / Sarah Chen), transcribed to data for gating.*

## The job
A business admin opens Payments to (a) judge whether the business is solvent right now,
(b) approve/reject pending payments, and (c) trust the scheduled-payments picture before money moves.

## Riskiest assumptions (what bites if wrong)
1. The admin trusts the headline reassurance ("you're covered") without re-checking the maths.
2. The admin trusts that an amount shown for a payee is the same everywhere it appears.
3. The admin approves high-value payments from this screen quickly, under time pressure.

Each becomes a checkable criterion.

## Acceptance criteria

### Enforceable → gate 2 (BLOCK — fails the build)
| ID | Criterion |
|----|-----------|
| DATA-1 | The same payee/payment shows the **same amount** in every panel. |
| DATA-2 | A stated total is **≥ the sum of its itemised rows** (and = when all rows are shown). |
| DATA-3 | Any solvency/"covered" reassurance is **derivable from balance − scheduled obligations** for the stated period, including the stated buffer. |
| A11Y-1 | Non-text contrast **≥ 3:1** (WCAG 1.4.11): action-tile glyphs vs tile fill. |
| BRAND-1 | Destructive/error **red is not used for routine actions**. |
| FLOW-1 | A high-value approval (> £10k) **requires a confirmation step**. |

### Advisory → annotate (WARN, non-blocking)
| ID | Criterion |
|----|-----------|
| COPY-1 | One currency format throughout (`£1,234` *or* `1,234 GBP`, not both). |
| COPY-2 | Avoid all-caps for labels/body (readability). |
| PII-1 | Sort-code / account masking policy applied. |

### Taste → human call (never gated)
- Visual hierarchy of the 5 action tiles (rainbow colour carries no meaning).
- Whether a "you're covered" reassurance should appear at all.
- Emphasis of the primary action ("Make a payment").

## The architectural catch (why this matters for the pipeline)
These checks run on the screen as **structured data** (`screen.json`), not the picture. A gate
cannot know BrightHire's two amounts *should* match when they're just two unrelated text layers
in a Figma export. In the live pipeline, **station ② (the generator) must EMIT this structured
model** — one source-of-truth value rendered in many places — or DATA-1/2/3 have nothing to verify.
The hand-transcription from pixels → data here is the contract ② owes ③.
