---
name: kb-distillation-at-deploy
description: "EXPLORE before deploy — the deployed build engine may not need the live KB; distil it into something more efficient, while the KB stays the dev-time + chat source of truth"
metadata: 
  node_type: memory
  type: project
  originSessionId: 092f2ec3-f158-4442-b33b-7b5302f0d3f6
---

Consideration (Dave 2026-07-17, "worth noting", explore before deploy): ultimately the **build/generation engine at deploy time may NOT need the full live KB** — all of it could be **distilled into something more efficient** (e.g. compiled rules, baked gates/tokens, a tuned model — mechanism TBD).

**But the KB does not retire.** It stays load-bearing for: (a) the [[chat-to-kb-bot]] (chatting to the smart design system), and (b) further development work on Apollo itself. So this is a **"distil the build engine for efficiency" question, not a "throw the KB away" one** — the KB remains the dev-time + read-side source of truth; only the deployed generation path might run on a compiled/distilled artifact.

**How to apply:** a pre-deploy architecture fork to explore, not decided. Keep the KB as source of truth during development; design so a distilled deploy artifact can be *generated from* it without the two diverging. Relates to [[capability-gap-and-obsolescence]] (invest in transferable structure), [[pipeline-mental-model]], [[apollo-product-framing]] (Discover/Create feed the engine; chat = Discover-side read).
