---
name: model-selection-by-phase
description: "Which model for which work — canonically in MODEL-ROUTING.md at repo root; Fable=rationed premium, Opus=default/complex, Sonnet=throughput, Haiku=chores; Mode-2 delegation is DEFAULT-ON (mention each time); /model works in Code not Cowork"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5c3cf432-53ab-4f1e-b8a4-bd0a7442df75
---

**⭐ PROMOTED 2026-07-13 → `MODEL-ROUTING.md` (repo root) is now the canonical routing reference**
(linked from `AGENTS.md` → How to work). This memory is the pointer + the "why."

**Dave's REAL model economy (corrected 2026-07-13 — supersedes the earlier Opus/Sonnet-only read):**
- **Fable = rationed PREMIUM.** His most-trusted model, but dear — reserved for **big, high-stakes,
  hands-off jobs** ("I need to trust this"). Not the daily driver. (Earlier notes had Fable as
  cheap-bulk — WRONG; it's the top-trust tier he can't afford to run often.)
- **Opus 4.8 · high = DEFAULT** for anything complex/judgment (his workhorse).
- **Sonnet = throughput** to an existing plan/runbook (gates, metas, rebinds, ingestion tranches).
- **Haiku = chores** (doc-drift, find/replace, formatting, index bumps).

**The mechanics + SURFACE CAVEAT (his screenshots, 2026-07-13):** no auto-fork — a chat runs ONE
model. **`/model` is a Claude Code slash command; in COWORK it does NOT exist** — the `/` menu there
is a **file/skill picker** (Dave confirmed with screenshots; my earlier "it works, you used it" was
wrong — the transcript logged a switch but Dave can't `/model` in his Cowork UI). So in Cowork, Mode 1
manual switching relies on the app's model selector (if surfaced) — which is awkward. **Therefore
Modes 2 + 3 carry the weight for Dave.** Three modes: (1) session lookup — set model (Code slash / app
selector); (2) **in-session delegation** — keep the session on Opus, delegate chore/throughput to
Haiku/Sonnet **subagents** (Agent tool `model:` param), returning into the same chat, no fork = Dave's
real cost lever; (3) handoff pre-selects the next model in `GOOD-MORNING.md`.

**🟢 RULED (Dave, 2026-07-13): Mode 2 is DEFAULT-ON, mention each time.** Auto-delegate the
mechanical/throughput bits to cheaper subagents unless told otherwise; announce each delegation so
Dave sees the pattern and can pull it back. Needs no manual switch — which is why it's the right
default given `/model` is unavailable in Cowork.

**Rules (in the file):** default-down/escalate-up · model never moves who promotes/vouches (Dave,
`derivation-governance`) · declare+record the model (provenance; model is a real variable — the
Sonnet-vs-Opus spread) · in experiments change one thing at a time · verify with peer-or-stronger ·
fresh context pairs with the Opus "decide" tier.

**Demonstrated 2026-07-13:** delegated the `knowledge/README.md` mechanical drift-fix (32→38 metas,
Sutherland "parked"→unblocked) to a **Haiku** subagent; kept the judgment calls on Opus (the AGENTS
link placement + a "build description is stale, needs real rewrite" escalation banner — because the
10→18-step/gate rewrite is substantive, not string-drift). **Product feedback on record:** slash
commands (esp. `/model`) in Cowork would aid the Code transition — worth flagging to Anthropic.
Relates to [[product-shape-flexing-engine]] (floor/ceiling tiering), [[common-toolkit-survey]]
(meter ruling), [[deep-analysis-report-2026-07-10]].
