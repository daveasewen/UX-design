---
name: sds-quick-edit-interface
description: North-star idea — a lightweight visual edit interface for the Smart Design System so users make quick edits directly instead of spending agent tokens on basic changes.
metadata: 
  node_type: memory
  type: project
  originSessionId: bee457ea-aa66-4840-aa48-576912c2badb
---

**The goal (north star).** Build a lightweight **visual edit interface for the Smart Design System (SDS / Promenaut)** that lets a user make quick, direct edits — copy changes, re-arranging/restructuring layout, small tweaks — through a UI, *rather than "wringing out tokens" on basic edits*. The motive: don't spend LLM/agent turns on trivial changes; give the user direct agency for the small stuff and reserve the agent for real work.

**Seed / prototype (2026-06-29).** Explored this idea on the narrative deck at `digital-experience-transformation/polished/Transformation-Story_edit.html`. It has two modes — **Edit text** (inline contenteditable) and **Arrange** (click to select → click/Enter to drill deeper → Esc up → drag or arrow-key nudge to move) — plus draggable sticky notes, autosave to localStorage, and Export-to-markdown so edits/notes flow back to me.

**Status.** Dave's verdict = *"not quite right"* — parked (his call, to avoid distraction). When picked up: ask what's off about the interaction model (granularity? how restructuring/re-flowing works? the select-and-drill feel?) before iterating. Relates to [[swiss-design-system]].

**Slide 3 status.** Restructured to 2 columns (from→to) × 3 keyline rows — role shift / measurement shift / human→SDS handoff, each with a context line. **Synced into the master deck `Transformation-Story_v1.html` on 2026-06-29** (Dave approved "good for now"). Still TODO if consistency wanted: the operating-model HTML page (`Operating-Model-and-Roles.html`) and doc still carry the older 4-item shifts framing (Bottleneck/Value/Quality/Compliance) — could be reconciled to the 3-typed-shifts version.
