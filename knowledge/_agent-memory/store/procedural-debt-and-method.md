---
name: procedural-debt-and-method
description: "Durable principles from the Open Skills reflection — verification=enforcement, keep convergent/divergent separate, write the method down; next-session backlog lives in _NEXT-SESSION.md"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b984ef19-8715-4451-a36d-b781e96d0089
---

From a 2026-06-19 reflection on the "Open Skills" video, Dave wants these to **stick** across sessions (he flagged them at end of a long day and said "this has to stick").

**Why:** today's work was a live instance of the video's diagnosis — we have strong artifacts but the *procedure* isn't written down.

**How to apply:**
1. **Verification = enforcement, not a nudge.** Our build gates withhold "done" by exiting non-zero (proven: inject a defect → red; restore → green). Strictly stronger than a prose "please verify". Keep any new definition-of-done **executable**, not markdown intent. See [[gated-snippets-and-motion]].
2. **Keep the convergent/divergent line bright.** Gate canon; **never gate exploration** (`_fitness-test/`). Codifying divergent work early kills the surprise that produces ideas (the icon fake-weight trick only existed because motion was still loose). Maps to the two-tier canon/exploration model.
3. **Procedural debt is real and accruing.** Highest-leverage next move = **write the method down as runbooks** ("build a gated component", "reconcile a dark token group") — it currently lives only in-session. Also owed: a consolidation/GC pass (findings scattered across snippets, four `_*.md` docs, meta notes, chat). Don't add more docs — consolidate.

**Next session:** start by reading `UX-design/knowledge/_NEXT-SESSION.md` and **clarifying direction together** (priority deliberately unset). The work has mixed convergent build + divergent exploration; decide the split before building. Related: [[brand-refresh-direction]].
