# Vision note — the engine in a second vehicle
*Parked for revisit. Written 2026-06-29 by Claude + Dave. NOT a roadmap change.*

---

## Status & guardrail (read first)
This is a **horizon-3 "what if," deliberately fenced from the active project.** Apollo's
sequence is unchanged: prove the design-time loop on one real HSBC screen, then define the
target, then build scaffolding. Nothing here competes with that. The question this note
captures is narrow and durable: *could the engine we're building be dropped into a different
vehicle with a different purpose?* Answer: yes — and the cleanest first vehicle is a
**contextual dashboard**, not full GenUI.

## One line
Apollo's IP — gated canon + criteria-as-executable-checks + enforcement — is a generic
**"trust layer for assembled UI."** Pointed at design-time it produces gate-verified prototypes
(what we're building). Pointed at run-time it could assemble a **per-user dashboard** where every
element is provably compliant and the user only ever sees what they're entitled to.

## Two vehicles for the same engine
1. **Broad / aspirational — the GenUI safety substrate.** Everyone ships GenUI as freeform
   *model-emits-UI*. The hard part was never generating an interface; it's generating one you can
   trust — compliant, brand-true, auditable. That trust layer is exactly the kernel we're building.
   Real, but it's a different product and market. Keep as a someday-vision.
2. **Tight / actionable — the contextual dashboard (recommended first vehicle).** Not a fully
   generated experience. A landing surface that **assembles itself per user** from a *certified set
   of cards*, deciding which cards, in what order, with what emphasis, for this person right now.
   The "generation" collapses to **selection + ranking + composition** — an objective problem the
   gates already govern. This is the version worth revisiting first.

## The contextual dashboard, concretely

**Inputs (the user context):**
- **Profile + entitlements** — role and permissions. In banking this is a *hard gate*: you can
  only surface what the user is allowed to see. Maps 1:1 onto our blocking-gate model — entitlement
  becomes a verification check on card eligibility, not a nice-to-have.
- **Company data** — balances, pending payments, approvals queue, limits, exceptions.
- **Comms signals** — email, Teams, Slack: "3 approvals waiting," "client emailed about a payment,"
  surface the relevant card.
- **Chronological triggers** — time-of-day, month-end, cut-off times, scheduled runs:
  "payment run due in 2h," "statement ready."

**What the engine does:** ranks relevance and composes a layout from **gated canon cards** — which
cards, what priority order, what density/emphasis. It does *not* emit pixels or invent components.
Every card is already certified (a11y, contrast, tokens, states). So there is **no taste-call at
run-time** — the taste was spent once, designing the card set. Run-time only does the objective half.

**Why it fits the moat:** "a personalised dashboard where every element is provably compliant and
you can only ever see what you're entitled to" is something freeform GenUI tools structurally cannot
offer. The enforcement layer is the differentiator, and entitlements-as-a-gate is *verification =
enforcement* applied to data visibility — a compliance requirement in banking, not a flourish.

## What it reuses from Apollo (the kernel)
- **Gated canon** → the card/widget library (certified, compliant building blocks).
- **Criteria-as-executable-checks** → run-time eligibility + composition rules (entitlement gates,
  states-completeness, per-card a11y).
- **Enforcement loop** → the dashboard only ever renders gate-passing cards.
- **Tiered checks** → blocking (entitlements, a11y) vs advisory (relevance score).

## What's genuinely new (the "vehicle," not the engine)
- A **user-context model** (profile, entitlements, signals, time).
- **Connectors** — entitlement service, company data, email/Teams/Slack.
- A **relevance / ranking engine** — the actual hard new problem.
- **Run-time-capable gates** — fast, inline, per-instance (today they're an offline batch build).
- A **consent / privacy / audit** layer — heavy in a regulated environment.

## Honest risks
1. **Relevance ranking is its own hard problem.** "What matters to this user now" is easy to get
   noisy or wrong; needs a feedback loop and a sane default order.
2. **Comms integration is a large, sensitive surface** — email/Teams/Slack bring privacy, scope, and
   signal-extraction challenges. Start with entitlements + company data; treat comms as a later add.
3. **Personalised surfaces erode shared mental models.** Far milder for a dashboard than for full
   GenUI, but still real — keep a stable spine and personalise the periphery.
4. **It's a different product than the design tool.** Two-product trap. Stays fenced until the
   design-time loop is proven.

## The one shared investment
The bridge that serves *both* the current project and this vehicle is **making the criteria contract
+ gates run-time-capable** (fast, inline, per-instance, auditable). It's the same `spec.md`-as-checks
artifact, pointed at a live instance instead of a design variant. If we ever build that for other
reasons, this vehicle gets much cheaper — worth noting when we spec the harness tier-contract.

## Revisit when…
- The design-time loop is proven on one real HSBC screen (current locked priority), **and**
- a real stakeholder need for a role-based landing/dashboard surfaces, **or**
- the run-time-capable-gates investment gets made anyway.

Until then: parked, captured, not competing.
