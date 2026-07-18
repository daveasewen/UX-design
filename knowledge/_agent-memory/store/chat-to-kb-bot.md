---
name: chat-to-kb-bot
description: TARGET — ship a chat-to-the-KB bot in the final product; users converse with the design-system knowledge base
metadata: 
  node_type: memory
  type: project
  originSessionId: 092f2ec3-f158-4442-b33b-7b5302f0d3f6
---

TARGET (Dave 2026-07-17, quick capture): the final Apollo system should include a **conversational bot users can chat to the design-system KB** — ask what a token/component/rule is, why a decision was made, how to use something — answered from the Apollo knowledge base (canon · criteria · rulings · decision graph), grounded in retrieval, not general model knowledge.

**Why:** the KB is already the source of truth; a chat surface makes it self-serve. Natural sibling to [[agentic-loop-gates-as-service]] — same KB, read/Q&A side vs enforce/verify side.

**Open (unspecified, not a spec yet):** retrieval grounding + provenance/citations; scope (read-only Q&A vs can it also generate/compose); surface (in the component catalog / Slack / IDE); guardrails against invented answers. Recorded in `_LIVE-STATE.md` PLANNED/TARGET section. Relates to [[multi-mode-product-vision]], [[pm-knowledge-graph-direction]].
