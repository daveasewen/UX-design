# Cross-cutting inputs — BA & PO

Business Analyst and Product Owner are modelled as **input providers and gate
participants**, not generative design pipelines. They shape what the pipelines
work on and authorise key gates.

## Business Analyst (BA)

| Provides | Into | As |
|---|---|---|
| Functional/non-functional requirements | framing (UX design) | `requirements` input |
| Acceptance criteria | craft + final gates | gate criteria |
| Process & data constraints | generator, handoff | constraints input |

## Product Owner (PO)

| Provides | Into | As |
|---|---|---|
| Priorities & scope | framing, prioritisation | scope input |
| Success metrics | framing, final approval | success criteria |
| Sign-off authority | Gate A (brief), Gate B (final) | HITL approver |

## Modelling note

Represent BA/PO contributions as **typed inputs** and **gate roles** in the
contracts, so a human or an upstream agent can fill them interchangeably. This
keeps the harness flexible: if BA/PO work later becomes its own pipeline, it
plugs in without changing downstream disciplines.
