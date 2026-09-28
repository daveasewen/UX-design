# #306 wrap — summary (s305-D63)

**Decisions**
- 24 parked questions closed as answered; 78 kept open by his ticks (s306-D1..D3, enacted).
- Wrap redesign ruled whole: story once with all views generated, three seats, summary at the push, carries by change (s306-D4..D9).
- Eleven bloat limits adopted, each by its phase (s306-D10). Rulings 702 → 712.

**Outputs**
- Phase 1 (six wrap tools, 079740c5) and phase 2 (one CI wait, 0afaca91) built; this wrap ran on them.
- Proof: 0 scripts (target 0), 1 move file + the 5b (target 1 + 5b), 1 rebuild for the wrap (target 1).
- Wrap commit 5234ce41 on the --wrap path (gate 244 in scope, 0 fail), pushed 17:11 UTC: 17.6 min from launch (#305: about 59 to the summary).
- CI: 079740c5 GREEN (run 36453625640); wrap 5234ce41 GREEN (run 36456434157). Summary at 32 min from launch.
- Handoff _HANDOFF-157 (11,008 B, under the 25,270 ceiling). Next: `Apollo - #307: the 78 reopened questions, how he wants them worked`.

**Problems**
- Fill 321,077 at launch, over the 320,000 limit by 1,077 (hand sum by _wrap_facts.py).
- Two hand steps: `_gen_titles.py` is missing from _wrap_regen.py; `{{SECTION_SIZES}}` doubled a `> ` (docstring gap).
- The gate and git reset still strand locks: 4 unlock runs this wrap (14 lock files), all moved, none deleted.
- The 5b needs its own regen (the delta line feeds _CHAIN.md), so rebuilds are 2 in all.
