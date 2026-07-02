# Good morning, Dave ☕

*Session briefing — written end of 2026-07-02, evening session ("the window day" — north-star mock + Fable-window sprint). Previous briefing (critical regroup, same date) superseded; its open items carried below.*

## The session in one line

The north-star mock got built and immediately started paying: two of its nine gaps closed
same-day, GOV.UK proved the engine generalises, you ratified the four curbs, the advisory
tier went live and caught real defects, the guidance-ingestion workstream opened (supporting
palette + four data-vis guideline pages, enforcement-tagged) — and when I overstepped into
the token store, the process caught it and we invented the holding pen.

## What changed in the repo

1. **North-star mock (the "define just enough target" artifact):**
   `_VISION-northstar-front-end_2026-07-02.html` — six regions, every one receipted
   built/named/gap; three switchable layouts (your pick **frame + stages** is default);
   blocked ≠ discarded (repair + harvest exits on the killed variant); gap list G1–G9 at
   the bottom. G-statuses updated live as the day closed them.
2. **GOV.UK second-system run — decision #4 CLOSED, same day, under timebox:**
   `second-system-govuk/` — 5 gated components from public code source; snippet gate 5/5
   (one patch: themes declared per system), a11y gate 5/5 (zero modifications); 9 findings
   (F1–F9) in `_FINDINGS.md`. Verdict: **the engine generalises; HSBC coupling is shallow
   and enumerable.** The gate bit GOV.UK's known yellow-focus weakness (F7) and my own
   recall drift (F8).
3. **Charter §4: RATIFIED (you):** flatness fixed sober/balanced, expressive-only unlock
   via derived ramp (+ data-chart carve-out — see 7); inverse/surface promoted as a role;
   red may lead in balanced+expressive; radius square in ALL registers (rounded system =
   future variant, not a register privilege). Parked: register reach over spacing/layout.
4. **G2 partially closed:** `knowledge/_RUNBOOK-criteria-contract.md` +
   `runs/contract-001-sme-payments/contract.json` (hand-compiled, `agreedBy: null` —
   honours its own rule). The compiler is the remaining half.
5. **G5 live:** `_validate_advisory.py` — 3 prose rules executable at the advisory tier
   (all-caps house rule, placeholder-as-only-name, unmasked digit runs); bite-tested 6/6
   (`_tests/test_advisory.py`, in CI); build is now **16 steps** (advisory at #6, non-gating).
   First run: 19 signals, incl. **a real unmasked sort code in `Table.reference.html`**.
6. **Token governance — the day's most important lesson:** I minted 10 derived tokens into
   the live store (review-tagged); you caught it. Now: `tokens/_proposals/` is the holding
   pen — **outside the resolving stores; a tag is not a fence, the store boundary is the
   fence** (recorded in `_PROMOTION-QUEUE.md`). Store restored; build green without them.
7. **Ingested (your supplies, both penned/recorded with provenance):**
   - **Supporting palette** — 50 values, 10 families, from your create.hsbc session →
     `tokens/_proposals/supporting-palette.proposals.json` (contrast receipts per value;
     supersedes my derived data series, which stay as format spec).
   - **Data-vis guidance, 4 pages** → `guidelines/data-visualisation.md` + the bar / pie /
     line companions — first guidelines of the engine era, every rule tagged with its
     enforcement destiny (blocking-derivable / advisory-derivable / taste). Gate-candidate
     hard rules captured: bar zero-baseline (mandatory) vs line zero-baseline (optional!),
     pie 6-slice cap, slices sum-to-total, straight lines only, no negative values on
     horizontal bars, spark aspect ratios. Charter carve-out recorded: **chart fills stay
     flat in ALL registers.** Your call: ingestion is a standing workstream — the site is
     rich with this (queued targets in `_NEXT-SESSION.md` §2a).
8. **Robustness papercut logged:** sandbox screenshot compositor rendered a correct white
   DOM as a dark PNG — trust-chain rule added to `_ROBUSTNESS-PORTABILITY.md` (G8 input).

## On your desk (fastest first)

- **V7 — charting series pick (~20s):** open `_fitness-test/v7-series-assignment-AB.html`.
  Standing recommendation: **B + usage rule** (≤2 data sets → series-1+3 complementary pair;
  ordered → family ramp). Queue entry has the full receipt.
- **Table sort-code fix (~1 min):** `Table.reference.html` shows `40-12-08` unmasked —
  charter §2 violation, propagates to the gallery. One-line fix; canon, so your approve.
- **All-caps scope ruling:** house rule vs 17 uppercase signals across the HSBC canon —
  canon-wide (migration) or brief-scoped (check reads the contract)? Advisory, no urgency.
- **V6 — inverse/surface + expressive ramp proposals** (holding pen, swatches at
  `_fitness-test/v6-token-proposals.html`).
- **Colleague chase** — calibration materials (still the #1 unlock; jumps every queue).
- **Token provenance (ADR-0005 open item)** — now also carries the supporting palette
  (login-walled source) and the two-machine question.

## The window (Fable metered from the 7th)

Judgment-dense work stays in the window: calibration (if materials land), G2 compiler spec,
more guideline ingestion (targets queued in `_NEXT-SESSION.md` §2a). Plumbing (G6 diff,
G8 render harness, G9 promote-on-win, G1 ingestion) is deliberately post-window — the gap
entries are their briefs. The metering itself = the ADR-0005 portability test: tighten
runbooks before the 7th, then a cold, cheaper operator runs the engine and the gates score it.

## Waiting elsewhere (don't pick up unless Dave says so)

Calibration project materials (colleague) · Q3 primary customer call (after calibration).
