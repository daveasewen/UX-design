---
name: spin-off-candidates
description: "PATTERN (Dave, 2026-07-05): tools/methods we build to fix problems in UX-design should be generalised + spun off as their own projects (like company spin-offs); surface emergent projects when they appear in chat; the state machine is Dave's first named candidate"
metadata:
  node_type: memory
  type: project
  originSessionId: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367
---

**STATED 2026-07-05 (Dave — capture-only thought).** We keep building tools + methodologies to solve
local problems, and several are **general-purpose** — they'd serve other projects. Treat them like a
company's **spin-offs**: recognise when something local is actually reusable, and surface it as its own
thing rather than burying it inside UX-design. Corollary: **whole new projects sometimes emerge mid-chat**
— we need to *surface* those deliberately (name them, give them a home) instead of losing them to the
conversation.

**Dave's first named candidate: the state machine** (`_LIVE-STATE.md` + the temporal decision-graph /
ADR-0007 + the decision-audit method) — a portable "how a long-running agent project retains state,
records supersession, and audits its own decisions" kit.

**Other likely candidates (my read, not ruled):** the decision-audit runbook + validation-state machine
([[decision-audit-method]]); the fixed/flex charter as a brand-true-generation governance pattern
([[fixed-flex-charter]]); the ingestion → overlay-KG method ([[ds-knowledge-graph-revisit]]); the
review-dossier language-review instrument ([[process-doc-language-review]]); verification=enforcement /
gate-tiering; the "cockroach doc" cold-start-proof pattern.

**Precedent — this already happens ad hoc:** [[digital-experience-transformation]] (a strategy strand
spun off UX-design) and [[graphify-tool]]. The ask is to make it **intentional + surfaced**, not
accidental.

**How to apply:** when a tool/method proves it generalises, flag it as a spin-off candidate (don't force
it — most things stay local). Surface emergent projects the moment they appear. Keep the running register
in `_LIVE-STATE` (SPIN-OFF / GENERALISABLE section). Connects to [[output-modes-portability]]
(portability = the same "don't marry it to HSBC" instinct at the product level) and
[[robustness-portability]]. Revisit in the seaworthiness run — some may deserve their own thread.
