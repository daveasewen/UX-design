# Note — the boot has three bands, and the middle one has switches

provenance: 293, Jev side-quest worker seat (Fable 5.1) · 2026-09-21 · analysis + one action by Dave

## Dave's words, verbatim

> there must be a way to make this boot smaller, i keep being told it can't be but I just have an
> instinct we are missing something

> but for a long time the boot hovered at around 50k how can this be?

> okay, so most of the boot is actually out of our control unless they are 'dismissible'

> it's fine, i understand this much better now, I've switched off what I think we can ditch

## The series — MEASURED, from `notes/_GAUGE-LOG.md`'s own boot samples

| sessions | boot | reading |
|---|---|---|
| #111 → #132 (early–mid Aug) | 54–55k, flat | the plateau after the #112 remedy — "the 50k he remembers" |
| #214 → #226 (22–28 Aug) | 61.6k → 66.8k → 69.6k → 75.7k → 79k | **+24k in one week; nothing of ours grew that much** |
| #227 → #293 | 74–79k, flat | new plateau; this seat's turn-1 `cache_creation_input_tokens` = **74,220** |

## What the #242 decomposition missed

`_boot_decompose.py` measured what we OWN (≈8k: MEMORY stub, skills roster, MCP blocks, deferred
tool names, agent list) and called the remainder "harness, estimated by subtraction, never a
measurement". It never asked whether the harness has switches. The 22–28 Aug step coincides with
Cowork feature blocks arriving in the harness — visible in this seat's own context: the Artifact tool
schema, the memory filesystem guidance + five tools, the Claude Docs connector, the visualise widget,
scheduled tasks, Chrome / built-in browser / computer-use blocks.

## Three bands (the middle one is ESTIMATE from what this seat could see, not measured)

1. **Fixed ≈ 50k** — Anthropic's base prompt, core tool schemas, Cowork instructions. Not ours.
2. **Dismissible ≈ 15–20k** — feature blocks tied to a toggle in Cowork settings / plugin panel /
   connectors: Chrome extension, computer use, Docs connector, visualise, scheduled tasks, plugins,
   possibly memory. Figma vanishing mid-session at #233 proved a toggle moves the number.
3. **Ours ≈ 8k** — handoff, chain, skills roster, project instructions. Already dieted; ~3k left.

## Action taken — by Dave, at this seat, 2026-09-21

He switched off "what I think we can ditch". **Mid-session evidence that at least one switch took:
the Claude Docs connector disconnected from this seat while the session was live.** Which others he
turned off is his panel's record, not this seat's.

## What the next cold boot must do — the measurement

Read turn-1 `cache_creation_input_tokens` from the session transcript (`_checkin.read_fill`) and
publish it beside 74,220. If it walked toward 55k, the middle band is real and its size is now
MEASURED. Then, if he wants the decomposition: re-enable one feature per session and read the delta.
⛔ Boot ceiling stays SHRINK-ONLY at 70,000 — never raise the literal; this is the first real chance
to get under it since #220.

## Ruling-shaped question — QUESTION PUT

Memory is the largest dismissible block this seat could see (~5k) and is also the project
accelerator; `index.md` is at zero headroom regardless. Off for Apollo sessions, or kept? His.
