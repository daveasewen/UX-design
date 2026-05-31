# Error taxonomy (4 types, one routing decision each)

Inherited directly from HDS. The orchestrator classifies every failure into
exactly one type. Misclassification — especially treating malformed input as
transient — is the expensive mistake.

| # | Type | Definition | Recovery |
|---|------|------------|----------|
| 1 | **Transient** | Environmental: timeout, API outage, rate limit. Input was valid, the spoke is capable. | Retry same spoke, same input. Cap at N attempts, then escalate. |
| 2 | **Input validation** | Spoke received malformed/incomplete input (missing or wrong-typed field). | Do **not** retry the failed spoke. Go upstream to find why the field is missing. |
| 3 | **Semantic / business-logic** | Spoke ran fine but the *content* is the problem (off-brief, contradictory, design-system-violating). | Route upstream for new input. Often triggers HITL escalation. |
| 4 | **Policy violation** | Crossed a safety/compliance/brand boundary. | Caught by pre-flight hooks where possible. Reframe input, single retry, then escalate. Never loop. |

## Retry budgets (defaults — confirm per ADR / open question)

| Type | Default budget | On exhaustion |
|------|----------------|---------------|
| Transient | 3 | escalate to HITL |
| Input validation | 0 (no retry) | route upstream |
| Semantic | 1 upstream re-run | escalate to HITL |
| Policy | 1 reframed retry | escalate to human |

## Why hooks for policy (type 4)

A hook fires deterministically; a prompt instruction may not. Compliance- and
brand-critical constraints belong in pre-flight hooks, not (only) in prompts.

## Logging

Every classification, recovery action and escalation is logged with the run id,
step, spoke, error type and the contract validation result — audit-grade, as
required in a regulated context.
