---
name: library-composition-tier-gap
description: "Root cause of underwhelming layouts (verified 2026-07-07): the invention rule = retrieve/derive-from-existing, but the library stops at organism (38 comps, 0 templates/shells), so page composition has nothing to retrieve; ~200-300 catalog already scoped; build-vs-compound is the open decision"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b86f842-66c3-4882-b0d1-4f5299d1a517
---

**VERIFIED 2026-07-07 (§9 session). Dave's diagnosis, checked correct.** The §9-spread "flat
layouts" trace to a **library-completeness gap at the composition tier**, not to bad rules or bad
rule-application.

**The rule (verbatim, charter `_FIXED-FLEX-CHARTER.md` §6 + §9):** invention is bounded to
existing material — §6 "Retrieval-first: query the graph for a component/token that fits *before*
generating" + "Derive from fixed: a new value must be *derived from* a brand primitive… not
invented free-hand"; §9 sober = "retrieve and assemble what exists; invent only if forced, then
derive-from-canon." So at sober/balanced the engine can only compose from what the library holds.

**The library (`_XREF-INDEX.json`):** 38 components = **9 atoms · 23 molecules · 6 organisms.
ZERO templates / shells / page-scaffolds** — the ladder stops at organism; no `.cn-page/.cn-grid/
.cn-layout` class exists. So page-level composition has **nothing to retrieve** → layout is always
hand-inferred from thin parts → underwhelming layouts are *structurally forced* at the strict end.
This is the same gap as [[register-inference-ramp]]'s F4 "layout has no retrievable governance,"
seen from the library side. It also explains why the unconstrained diagnostic won on layout: it
freely invented the missing tier.

**Already scoped (`knowledge/_COMPONENT-LIBRARY-TARGET.md`):** base ~38 → ~75–85 + a **Layer 2 of
~40–50 shells/templates/lock-ups** → a **"200–300+ item catalog"** (matches Dave's "~300 including
templates and shells" recollection). Its own line: "the automation can only compose what exists, so
the inventory is the prerequisite for the machine."

**OPEN DECISION — build-upfront vs compound (unresolved).** `_COMPONENT-LIBRARY-TARGET.md` frames
the catalog as a program to build. **ADR-0006 pt 4** pushes back — "compounding canon, not
completeness… chasing a complete library is the alphabetical treadmill" — answering with the
**cluster promote-loop** (each novel lock-up → gated canon the moment invented once). They agree the
template/shell TIER must exist; they differ on how to fill it. ADR-0006 flags cluster-level
promotion as the **least-proven** part of the loop (tokens+motion promoted, never a whole lock-up).

**How to apply:** when picking the §9/layout next step, treat "add a retrievable composition/shell
tier" as the lever — either build Layer 2 or prove cluster-promotion. Pairs with
[[product-shape-flexing-engine]] (flex ceiling needs the upstream), [[ds-knowledge-graph-revisit]]
(shells as graph nodes = whole-corpus KG territory), [[knowledge-usage-trace-tool]] (add a
composition-tier probe: is any retrieved unit above organism?). Full record:
`knowledge/_FINDINGS-s9-session-2026-07-07.md` (F6/F7).