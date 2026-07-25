# Brief — memory-index compaction (MEMORY.md) — 2026-07-25

*Cut by the Opus "Memento efficiency" window (Amber seam). Self-contained: read this, then do the work
cold. Companion to memory `[[gm-banner-compaction]]` / `[[memory-compaction-mechanics]]` and the ritual.*

## Why this exists
`MEMORY.md` is the index loaded into context **every session**. It hit **20KB**, nearing the **24.4KB
read cap** (a PostToolUse hook fired: "compact to under 17.1KB"). Over the cap → the index won't fully
load → recall silently degrades. This is the memory-side twin of the GOOD-MORNING compaction we just did
on the repo side; Dave: *"get the efficiency work done first — it pays off every run."*

## Goal
Compact `MEMORY.md` to **< 17KB** (target ~17.1KB ceiling), **one line per entry**, losing no durable fact.

## Method (there is a skill for exactly this — use it)
1. **Invoke the `consolidate-memory` skill** (`anthropic-skills:consolidate-memory` — "reflective pass:
   merge duplicates, fix stale facts, prune the index"). It is purpose-built for this. Follow it.
2. Read `MEMORY.md` in full + skim `MEMORY-ARCHIVE.md` (the existing archive) so you know what's already retired.
3. **Tighten each hook to ONE line** — subject + the single sharpest pointer. Where a hook has grown to
   carry ★/⚠ detail (e.g. the context-gauge, theming-DNA, buildout-strategy, four-theme, component-type
   entries are the long ones), **move that detail into the entry's own topic file**, leaving a lean hook.
4. **Roll stale / superseded / historical entries to `MEMORY-ARCHIVE.md`** (it exists; append there).
   **Never delete a topic file** — archived entries stay recall-reachable; only the *index hook* leaves.
5. **Merge near-duplicate feedback entries** if any are genuinely the same rule.
6. Keep the two NOTE lines (current-project-state pointer · ARCHIVE pointer).

## GATE before saving (recall-critical — do not skip)
- **No topic file deleted** (only hooks shorten / move to archive).
- **No `[[link]]` orphaned** — if you rename a slug, fix inbound links.
- **Every kept entry still has its one-line index pointer.**
- **Result < 17KB** and re-reads clean end-to-end.
- Stamp your context-gauge reading (this is authoring; Red-authored ⇒ re-verify).

## Routing
**Cold + Opus.** Recall-critical judgement — the reason it was seamed out of the warm Opus window rather
than done at Amber. Under the proposed budget governor (see the ★LATEST banner / `MODEL-ROUTING.md` if
inscribed), this is textbook **surplus-budget quality work**: high value, deferrable, funded when the
week is under pace.

## Then
Legend **v5.1** is the next build after this (brief:
`notes/_briefs/2026-07-25-legend-v5.1-barrise-and-hitarea-audit-brief.md`). Efficiency first, per Dave.
