# Test brief — SME Payments screen (v2)

*Structured so the generator can tell **fixed** from **flexible**. Five parts: intent + structural licence · the register dial · immutable data · correctness rules · the design system to build on. Figures are welded down; structure is licensed; register is explicit, not an adjective. Enriched with the account / status / category data the model previously had to invent.*

---

## 1 · Intent & structural licence

Build a **Payments** screen for the finance admin of an SME — **Northgate Timber Ltd** — on their business current account. It must let them, at a glance: read today's cash position, understand the month's coverage, action the payments waiting on their approval, and scan what's scheduled ahead.

You are designing a real product screen, not formatting a table. You **may** add the columns, states, groupings and secondary labels a finance admin genuinely needs — an account per payment, a status, payee categories, running context. But:

- never invent, alter, or round a **figure** (see §3);
- **prefer the data in §3** — it already carries account refs, categories and statuses, so you should not need to fabricate anything;
- anything you must still add that isn't given must be **derived** from what is, or visibly marked as sample/placeholder.

## 2 · Register — the dial (pick one, or produce all three)

The one knob for temperature. Do not bury it in adjectives — set it here.

- **Sober** — light surfaces, flat, generous white space; red restrained to accent / destructive only; motion minimal.
- **Balanced** — confident; one bold moment allowed (a dark band or a hero figure); red may lead the primary action; motion subtle.
- **Expressive** — editorial; dark hero, gradients and motion unlocked; red leads.

**Register for this run:** `____________`

## 3 · Immutable data — never alter, round, or invent a figure

**Business:** Northgate Timber Ltd · Business current account `···· 8842` · sort code `··–··–··` *(display masked)*

**Cash position (as of 12 May 2026):** opening £120,000 · inflows today +£11,650 · outflows today −£9,200 · **current balance £122,450** · net movement +£2,450 · est. closing £124,000.

**Coverage:** current balance £122,450 − £49,702 scheduled in May = **£72,748 buffer**. Covered *through May* — state exactly, don't overstate.

**Payments:**

| Date | Payee | Category | Account | Status | Amount |
|---|---|---|---|---|---|
| 15 May 2026 | Amazon Business | Supplier · card & fulfilment | ···· 4021 | Awaiting approval — Sarah Chen, 2 days ago | £4,502 |
| 22 May 2026 | BrightHire Payroll Ltd | Payroll · monthly run | ···· 7730 | Awaiting approval — Sarah Chen, 2 days ago | £45,200 |
| 22 Jul 2026 | HMRC — PAYE | Tax · PAYE / NIC | ···· 0001 | Scheduled | £2,200 |
| 12 Aug 2026 | British Gas Business | Utilities · electricity & gas | ···· 5560 | Scheduled | £4,200 |
| 09 Sep 2026 | Ravenscroft Properties | Rent · quarterly lease | ···· 3318 | Scheduled | £50,200 |

Scheduled total: **£106,302** (must equal the sum of the rows). Two items awaiting approval total **£49,702**.

## 4 · Rules — correctness (must hold)

- the same payee shows the same amount everywhere;
- the coverage statement must equal the maths; the scheduled total must equal the sum of the rows;
- a **high-value** approval (here the £45,200 payroll run) must require a confirmation step — no one-click approve;
- masked account refs show last-4 only; sort codes fully masked; never invent or reveal real digits;
- avoid ALL-CAPS labels (house rule — overrides any styling convention that wants caps);
- **figure fidelity overrides everything**: if the design wants a number, it uses a given figure verbatim.

## 5 · Build on the design system — retrieve, don't recall

Use `knowledge/canon/canon.css` (link it; put `class="canon"` on the root). **Retrieve** brand colour, type, spacing, motion (`--spring` / `--press`) and components (`.cn-*`) from it — do not recall from memory or invent brand values. Where the system lacks something the register needs (e.g. a dark surface for an expressive hero, a data-viz palette), **derive it from the tokens and flag it as a candidate** for promotion — don't invent free-hand.

## 6 · Output

A single self-contained HTML file. If producing the register spread, make the three switchable on one screen — the fixed content (§3) identical across all three; only the register (§2) changes.

---

### What changed from v1, and why

| v1 problem | v2 fix |
|---|---|
| "clean and sober" — voice buried in adjectives, silently set the temperature low | **§2** register is an explicit, defined dial |
| gave figures but not the screen's *shape* → the model invented accounts/statuses to make it usable | **§1 + §3** structural licence + the account/status/category data supplied |
| "don't invent any number" collided with good UI (it forbids the enrichment a real screen needs) | **§4** figure fidelity is absolute; *structure* is licensed and pre-filled, so no fabrication needed |
| red rule stated as a blanket ("destructive only") regardless of intent | **§2** red-forwardness is tied to the register |
| no instruction to use the library → a run could recall/invent the brand | **§5** retrieve-don't-recall, derive-and-flag for gaps |
| judged one output against perfection | **§6** optional register spread — generate the road, then harvest |
