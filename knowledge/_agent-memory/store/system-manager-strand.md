---
name: system-manager-strand
description: "The \"system-manager\" workstream in the UX-design (Promenaut) repo — governance/evolution of the design system, kept separate from the build pipeline."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f4692a8-384f-450c-8b44-61918e03e217
---

Dave opened a separate, ongoing strand (started 2026-06-22) about the **continual development of the design system itself** — how it changes over time, who decides, how decisions are captured and rolled out. It lives in `UX-design/system-manager/` and is **deliberately isolated**: not wired into AGENTS.md, the harness, or any pipeline. Treat it as a design space; proposals graduate to real only by an explicit edit to the harness/ADRs.

First subject: **capturing design decisions** (`system-manager/01-capturing-design-decisions.md`). The proposal extends the repo's existing decision spine (ADRs, promotion queue, canon/memory/`taste.md` split, HITL gates, the `_XREF-INDEX` blast-radius map) rather than inventing new machinery. Core model: a Design Decision Record + 6-stage lifecycle (Propose→Discuss→Decide→Build→Tell→Check); AI drafts, a human ratifies; decide once / build many; a few decide / most are informed; centralised ratification + federated execution.

Four open decisions are Dave's to make (governance model, where DDRs live, who the deciders are, meeting-trigger threshold). A boss-facing pitch of this exists at `system-manager/capturing-decisions-proposal.html`.
