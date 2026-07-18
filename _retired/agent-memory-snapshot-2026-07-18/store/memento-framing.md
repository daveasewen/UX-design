---
name: memento-framing
description: "Dave's framing — Memento is the operating model for working with AI, and it's why the handoff file is called GOOD-MORNING; the real risk is confident false inscription, not forgetting"
metadata: 
  node_type: memory
  type: project
  originSessionId: a7c41950-9b6a-47ce-ae2a-2f24777a6849
---

**Dave's framing, and the reason the handoff file is called `GOOD-MORNING.md`.** In *Memento*, Leonard has
anterograde amnesia: every morning he reconstitutes himself from a record he built while he still
remembered — Polaroids for working state, **tattoos for the facts he cannot afford to lose**. Dave sees this
as a description of working with AI, not a metaphor for it. Each session starts with no memory and rebuilds
from artefacts.

**The trust hierarchy is the tattoo/Polaroid distinction — use it when deciding where to write something:**
- **Tattoos** — memory files + runbooks. Durable, survive any single rewrite. Rules go here.
- **Polaroids** — `GOOD-MORNING.md`, `_LIVE-STATE.md`. Working state, rewritten constantly.
- **Gone by morning** — the chat itself.

**RULE: never let a durable instruction live only on a Polaroid.** Proved 2026-07-18 — §A's own standing
instruction ("carry this forward every handoff, to orientate a new starter") existed *only* inside
`GOOD-MORNING.md`, so a from-scratch rewrite silently reduced it to the words "Standing section", dropping
the rule and Dave's reason for it. Fixed by also writing it into `_RUNBOOK-capture-ritual.md` step 2.
See [[good-morning-orientation-section]] and [[capture-ritual]].

**The deeper parallel — the real danger is not forgetting, it is CONFIDENT FALSE INSCRIPTION.** Leonard's
tragedy is that he writes a *false* tattoo and then trusts it absolutely, because he cannot remember writing
it. On 2026-07-18 I asserted "38% of the rule corpus is silently missing from the index" with full
confidence. It was wrong — the exclusions were deliberate and Dave-blessed — and I then wrote a second
script to "verify" it that was also broken. Had Dave not pushed back, it would have entered the ledger as
fact and been trusted by every subsequent session, because a future me cannot remember having been wrong.

**Design consequences that follow from this — apply them:**
- **Records carry provenance and confidence, not just content.** Status fields, `$provenance`, who ruled it
  and when (the `_proposals/` holding-pen pattern does this well).
- **Mark what was OBSERVED versus what was INFERRED.** `dv-019`'s 135° hue leg records *"because Dave
  observed the dance on a 146° pair"* — **that sentence is the tattoo, not the number**. A threshold without
  its observation is unfalsifiable by the next session.
- **Inscribe corrections as loudly as the original claim.** If a ledger entry is overturned, the reversal
  goes in the same place with the same prominence — otherwise the confident wrong version wins on re-read.
- **A value without its reason will be misapplied.** `#1A1A1A` ran in production for two weeks with the
  rationale written down nowhere; the hex was findable in ten files and the reason was gone. Hence rule
  `{#col26-021}` — carry the condition with the value, in *every* store (token `$note`, KB prose, Figma
  style description, query bot).

Relates to [[chat-to-kb-bot]] (the query bot is Leonard reading his own tattoos back), [[pm-knowledge-graph-direction]]
and [[procedural-debt-and-method]].
