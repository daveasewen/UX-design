# Payments journey — colleague chat prep sheet
*Goal: gather enough to run the payments journey *backwards* through Promenaut and produce a "what would have bitten us after go-live" gap report. ~20–30 min chat.*

**Golden rule:** capture **evidence, not opinion.** Every "we thought / everyone felt" = an *assumption to test*, not a fact. Mark them as you go.

---

## Must-get (the ground truth — don't leave without these)

**1. The observable pain — what's actually going wrong now?**
- Where is it slow / getting reworked / generating complaints or escalations?
- Push for specifics: "slow" → how slow, measured how? Any numbers or artefacts?
> *Buys:* the spine of the whole proof — the real failure the rigor would have caught.

**2. What is everyone actually arguing about?**
- The competing opinions, stated plainly. Who wants what, and why?
> *Buys:* the disagreement usually IS the missing criteria — if 3 people want 3 things, success was never defined.

**3. Was there ever a definition of success?**
- Any target, metric, or "done"? If not — what do people *now* say it should have been?
> *Buys:* the reconstructed spec we test everything against.

---

## Then, if time allows

**4. Who's the customer, and what job does this journey do for them?**
- And who are the 1–2 test customers — how representative are they?
> *Buys:* the JTBD seed; flags if the test base is too narrow to trust.

**5. The unexamined assumptions.**
- "Vibes and instinct" = unstated assumptions. What did everyone just take as given that nobody checked?
> *Buys:* the riskiest-assumptions list — the heart of the gap report.

**6. What signal already exists?**
- Analytics, support tickets, prior versions of the journey, competitor parity.
> *Buys:* kills the "no research" problem — secondary evidence to ingest.

**7. The hard constraints (it's payments — these exist).**
- Regulatory, security, PII / data-masking, existing rails, tech limits.
> *Buys:* the "constitution" — the non-negotiable gates.

**8. Current state.**
- Shipped / in build / to whom? Current scope?
> *Buys:* tells us which intake lane it really sits in (seed / guided JTBD / ingestion).

---

## How it feeds the retrofit
- #1–#3 → reconstruct the spec + show the gap.
- #5–#7 → the riskiest-assumptions list + the gates that got skipped.
- #1 → the "what would have bitten us after go-live" payoff.

*One closing ask for the colleague: can they share any of the artefacts (tickets, analytics, a deck, a thread) so we ingest real material rather than recollection?*
