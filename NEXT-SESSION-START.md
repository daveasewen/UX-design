# Session-starter prompt — paste this into a fresh chat

> Copy everything in the block below into a new conversation to bootstrap it cleanly.

---

We're continuing the **Promenaut** design-to-code knowledge-base project (HSBC Common Toolkit). Before doing anything, read `MEMORY.md` and these files in the `UX-design` folder for context: `GOOD-MORNING.md`, `knowledge/_FITNESS-TEST-tabs.md`, and `knowledge/README.md`. Don't re-derive what's already recorded.

**Where we are:** the knowledge base is a strong correctness/provenance/migration-safety layer but can't yet drive *shippable* output. We proved this by building Tabs twice (KB-only vs unconstrained) — the KB-only build is **broken in dark mode** (white-on-white, fails WCAG), and our integrity gate passed it anyway. Full findings + an 8-item fix backlog are in `knowledge/_FITNESS-TEST-tabs.md`. Fix #4 (motion tokens) is already done.

**Confirmed last session:** the Figma connector **can write variable values** via `use_figma` (Plugin API, `figma.variables.setValueForMode()`); auth is good (david.ewen@emeal.nttdata.com, Full/expert on HSBC Enterprise). Writing to Figma still requires: canonical values (not demo hexes), the "Gaps and edits" branch, and my explicit go-ahead per change — and the first write must be a single reversible test variable.

**Today's priorities, in order:**
1. **Reconcile the corrected Tabs dark values** to real HSBC dark primitives (`neutral-dark-mode` / `rag-dark` in the colour stores) — replace my Route A demo hexes with canon, and stage the corrected `tabs/*` dark values. (Dark indicator decision already made: **core red `#DB0011`**, which passes 1.4.11 at 3.46:1 on the dark surface.)
2. **Fix #1** — correct the flat/wrong `tabs/*` dark token values, and make `_build_dark_mode_audit.py` **contrast-aware** (today it rates a token "clean" if it merely *has* a dark value, even when wrong).
3. **Fix #2** — add a focus-indicator standard (a `focus/*` token + `guidelines/focus-indicators.md`); systemic, affects all 32 components.
4. **Fix #3** — add a geometry/dimensions block to the meta schema (metas carry colours but no measurements).
5. Then **re-run the Tabs fitness test** and check the Route A–B gap has shrunk — that re-run is the progress metric, not another derived view.

**Working rhythm (from memory):** proactively flag reflection checkpoints; watch for the "productivity bubble" (building instead of proving value); after each step run `python3 knowledge/_build_all.py` (the gate); commit via GitHub Desktop on my prompt; and write a `GOOD-MORNING.md` briefing when we wrap.

Start by reading the context files, then give me a short plan for tackling priority #1 before doing it.

---
