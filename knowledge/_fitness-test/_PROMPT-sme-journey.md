# Prompt — SME Payments full journey (canon styling)

Build a 3-screen business-banking Payments JOURNEY for an SME finance admin (Northwind Trading Ltd),
in HSBC Common Toolkit style, mobile. Use the canon components and the STANDARD HSBC palette — brand
red is the normal primary-action colour (no special red restriction). Square corners, generous white
space, sentence-case labels, mask sort codes and account numbers. Use exactly these figures — do not
change, round, or invent any number. Same payee shows the same amount everywhere; any stated total must
equal the sum of its rows; any "covered" / projected-balance statement must match the maths.

## Screen 1 — Overview (the finance admin's contextual dashboard)
CASH POSITION (as of 12 May 2026): opening £120,000 · inflows today +£11,650 · outflows today −£9,200 ·
current balance £122,450 · net movement +£2,450 · est. closing £124,000.
COVERAGE: current balance £122,450 minus May scheduled payments £49,702 leaves a £72,748 buffer —
covered through May (state it accurately; don't overstate).
TRIGGERED CARD — the unexpected, contextually-surfaced item; surface it prominently near the top:
"Two large payments clear the same week." On 22 May, BrightHire Payroll Ltd £45,200 and Amazon Business
£4,502 both settle (£49,702 that week), taking the balance to £72,748. It is covered — flag the
concentration, don't alarm. Give the admin a way to act (e.g. review that week).
PENDING APPROVAL (2): Amazon Business £4,502 (Sarah Chen, 2d ago) · BrightHire Payroll Ltd £45,200
(Sarah Chen, 2d ago).
UPCOMING PAYMENTS — 5 scheduled, £106,302 total: 15 May Amazon Business £4,502 · 22 May BrightHire
Payroll Ltd £45,200 · 22 Jul HMRC — PAYE £2,200 · 12 Aug British Gas Business £4,200 ·
09 Sep Ravenscroft Properties £50,200.

## Screen 2 — Review & approve (BrightHire Payroll Ltd £45,200)
From: Current account ···4821 · Payee: BrightHire Payroll Ltd (account masked) · Amount £45,200 ·
Scheduled 22 May 2026 · Reference: May payroll.
Show the projected impact: current balance £122,450 minus £45,200 leaves £77,250 available after this
payment. A high-value approval MUST require an explicit confirmation step (no one-click approve).

## Screen 3 — Confirmation / receipt
Payment approved. £45,200 to BrightHire Payroll Ltd, scheduled 22 May 2026, from Current account ···4821,
reference "May payroll". Approved by the admin on 12 May 2026. Offer next actions: done · view upcoming
payments.

## Rules
- Canon HSBC styling (brand red = standard primary action) · square corners · generous white space ·
  sentence-case labels (no ALL-CAPS).
- Mask all sort codes / account numbers (···nnnn).
- Same payee = same amount everywhere · every stated total = the sum of its rows · every coverage /
  projected-balance line must match the maths.
- Derived figures (must equal): May buffer £122,450 − £49,702 = £72,748 · after BrightHire
  £122,450 − £45,200 = £77,250 · upcoming total = £106,302 · concentration 22 May = £45,200 + £4,502 = £49,702.
- Figures are FIXED as above — do not change, round, or invent any number.
