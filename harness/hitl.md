# Human-in-the-loop (HITL) gate framework

HITL gates are **designed components**, not error handlers. They sit exactly
where automated judgment is unreliable, and they are where senior design
judgment — the scarce, defensible input — stays in the loop.

## Gate anatomy

Every gate declares:

- **Trigger** — the condition that invokes it.
- **Decision surface** — what the human sees (a compact, reviewable artifact, not raw state).
- **Allowed actions** — the finite set of human responses.
- **Return path** — where the run continues for each action.
- **Owner** — who is accountable (role, not person, for portability).

## Gate types

### Craft gate (automated, scored)
Not a HITL gate. The **Critic** spoke scores output against defined criteria
(design-system conformance, token usage, contract integrity). Emits `pass: bool`
+ structured recommendations. The orchestrator routes on `pass`.

### Taste gate (HITL — the design lead)
The human/encoded-judgment gate. Analogue of HDS's Chief Editor. Refers to
`taste.md` (encoded preferences + past decisions). Question: *is this worth
shipping — does it meet our standard, not just our rules?* Escalates to a human
when the encoded judgment is insufficient.

### Approval gates (HITL)
- **Gate A — Brief approved.** Trigger: framing spoke produces brief + success criteria. Action: approve / redirect. Return: generator, or back to framing.
- **Gate B — Final approval.** Trigger: handoff artifact assembled. Action: approve / flag issues. Return: handoff if cosmetic; upstream spoke if deeper.

## Design rule

A system that tries to automate a judgment it cannot reliably make produces
*confidently wrong* output. Prefer an explicit gate over a fragile automation.

## `taste.md`

Human-authored, human-owned. Updated by the design lead, informed by escalation
patterns (which decisions the system kept punting). It is the north star that
prevents drift from the design identity across runs. See
`harness/state/memory.md` for how it relates to the learning store.
