# Test brief — SME Payments screen (v2)

*Structured so the generator can tell **fixed** from **flexible**. Five parts: intent + structural licence · the register dial · immutable data · correctness rules · the design system to build on. Figures are welded down; structure is licensed; register is explicit, not an adjective. Enriched with the account / status / category data the model previously had to invent.*

---

## 1 · Intent & structural licence

Build a **Payments** screen for the finance admin of an SME — **Northgate Timber Ltd** — on their business current account. It must let them, at a glance: read today's cash position, understand the month's coverage, action the payments waiting on their approval, and scan what's scheduled ahead.

You are designing a real product screen, not formatting a table. You **may** add the columns, states, groupings and secondary labels a finance admin genuinely needs — an account per payment, a status, payee categories, running context. But:

- never invent, alter, or round a **figure** (see §3);
- **prefer the data in §3** — it already carries account refs, categories and statuses, so you should not need to fabricate anything;
- anything you must still add that isn't given must be **derived** from what is, or visibly marked as sample/placeholder.

## 2 · Register — the inference dial (produce all three)

> **⚠️ Reconciled 2026-07-05 to charter §9.** This section previously described register as a
> *look* (surfaces / hero / gradients) — the exact propagation gap logged OPEN in `_LIVE-STATE.md`
> ("vision still speaks the OLD looks-language"). Register is **not a look; it is the level of
> inference you are licensed to use.** The visual outcome is a *consequence* of the inference level,
> never the instruction itself. See `_FIXED-FLEX-CHARTER.md` §9/§9a for the full ramp.

Register sets which curbs are in force. **Cardinal curbs never lift, at any band:** brand colour
(retrieved, never typed), type (Univers + ramp), corner radius (square — no rounding, no exceptions
on this screen), the a11y floor (AA contrast, focus ring, target size, reduced-motion), the safety
patterns (§4 below — high-value confirm, masked refs), and the data-chart-flat carve-out.
**Foundational curbs move with the band** (flatness/elevation, composition & density, motion amount,
red-forwardness).

- **Sober** *(retrieve — inference OFF)*. All curbs held, cardinal + foundational. Retrieve and
  assemble what already exists in `canon/canon.css`; invent only if forced, and if you do, derive
  it from a canon primitive and flag it as a candidate — never type a brand value from memory.
  Brand-source stop: token store + `canon/canon.css` (`.cn-*`) only.
  **Canon rigour tier (mechanical, not adjectival — check this order every time):**
  1. **`.cn-*` components** (auto-generated from `knowledge/snippets/*.reference.html` — gate-
     reviewed, the single source of truth for that pattern) — **always prefer these** when one
     fits the data shape, even approximately.
  2. **`.c-*` classes** (the hand-authored alias/utility/gap-pattern layer — never gate-reviewed,
     built to patch compositional gaps) — use **only** when no `.cn-*` component fits.
  3. Raw tokens/semantic aliases only, composed by hand — **last resort**, and the composition
     itself becomes a flagged candidate.
  Before using any `.c-*` class, name in a comment *which* `.cn-*` components you checked and
  ruled out, and why. Skipping a fitting `.cn-*` component in favour of a `.c-*` utility is a
  retrieval failure at every register, not a register-appropriate choice — sober means *don't
  invent*, not *pick the least-reviewed available option*.
- **Balanced** *(extend — inference ON but bounded)*. Cardinal + foundational curbs still both
  hold, but you may **extend**: compose more confidently, allow one deliberate emphasis moment,
  let red lead the primary action — provided every brand-bearing choice still traces to a named
  source (cardinals from the token store, composition from canon, character from
  `guidelines/brand-principles.md`, red-forwardness from `guidelines/colour-usage.md`). Flag
  anywhere the knowledge base is silent rather than inventing from a prior.
- **Expressive** *(invent — MAX inference, cardinal curbs only)*. Foundational curbs release —
  composition, density, motion, and red-forwardness are yours to invent. **Cardinal curbs still
  never lift** — square corners, retrieved brand colour, type, and the full a11y/safety floor are
  non-negotiable even here. Anything new must be derived from a cardinal and flagged (§6 of the
  charter), never recalled free-hand. This is "hot but leashed," not an ungated free-for-all.

**Machinery for this run (§9):** generate **each band in isolation** — a cold, independent pass
that does not see the other two bands or any prior SME-Payments variant in
`knowledge/_fitness-test/`. After all three land, run the **divergence probe**: measure how far
apart the bands actually are: are they properly clustering/diverging, or did they collapse toward a
shared mean? Payments is a cardinal-heavy, safety-critical screen, so some convergence across bands
is *expected*, not a failed spread — the probe is screen-relative, not a fixed distance target.

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

**Total across all 5 rows: £106,302** (awaiting-approval + scheduled combined — this is "the sum of
the rows" the coverage figure above is calculated against). Two items **awaiting approval** total
**£49,702**; the three **already-scheduled** items (HMRC, British Gas, Ravenscroft) total
**£56,600**. £49,702 + £56,600 = £106,302 — all three figures are consistent, but don't call
£106,302 the "scheduled total" on-screen; it's the whole table's total. **⚠️ Corrected 2026-07-05:**
the original wording ("Scheduled total: £106,302") conflated "all 5 rows" with "scheduled" (2 of the
5 rows are awaiting-approval, not scheduled) — two independent Opus generation passes caught this
ambiguity where the earlier Sonnet passes did not; fixed here so it can't mislabel on-screen again.

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

**One self-contained HTML file per band — three files, not one switchable screen.** (Superseded
2026-07-05: the old single-file-with-a-toggle instruction let one pass anchor on itself across
bands, defeating the isolation the divergence probe depends on.) Each file is produced from **this
same signed contract**, in a cold pass that cannot see the other two bands. The fixed content (§3
data, §4 rules) must be identical across all three; only what §2 licenses may change.

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
