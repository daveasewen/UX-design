# Session-starter prompt — paste this into a fresh chat

> Copy everything in the block below into a new conversation to bootstrap it cleanly.

---

We're continuing the HSBC Common Toolkit component-refinement work (Promenaut).
Before anything, read MEMORY.md and these files in the UX-design folder:
GOOD-MORNING.md, knowledge/_RUBRIC-prototype-grade.md, knowledge/_PROTOTYPE-GRADE-AUDIT.md.
Don't re-derive what's already recorded.

WHERE WE ARE: the assembly-tier gate suite is built and proven (runs/proof-001, runs/proof-002).
The component-review program has started: Tabs is promoted (responsive, 9/9, build green);
Cards is rebuilt to the real library types (action/link/media + the canonical arrow-link atom
+ the real card-details icon) and sits blessed in knowledge/_fitness-test/cards-responsive.html,
ready to promote.

TODAY'S PRIORITY — keep working the component reviews. Bring each journey component to the
Tabs-bar standard, then promote it:
  1. Promote Cards properly: write its meta for the 3 types, switch static cards to <article>,
     then `cd knowledge && python3 _build_all.py` must be green.
  2. Then List-items (transaction rows), then Status-indicator, Table, Modals, Notifications…
     (★ priority rows in _PROTOTYPE-GRADE-AUDIT.md).

THE METHOD (per component): refine in _fitness-test/ (exploration, never gated) → I review it
visually → promote into the gated snippets/*.reference.html → rebuild green. Pull the real
component from the Common Toolkit Figma (fileKey mI8hvIkV98nquoqWzKh5Kn, use get_design_context /
get_screenshot) and real icons from knowledge/assets/icons; reuse canonical atoms (e.g. the Links
arrow-link). KEEP CANON SIMPLE — conservative motion, no animation cleverness (the Tabs lesson).

WORKING RHYTHM: present files for my visual review; nothing enters canon without my go-ahead;
green build = done; flag reflection checkpoints; write a GOOD-MORNING.md when we wrap; commit on
my prompt with a paste-ready git summary.

PARKED (don't get distracted): the Figma dark-mode port (task #19) — components first.

Start by reading the context files and confirming the build is green, then promote Cards.

---
