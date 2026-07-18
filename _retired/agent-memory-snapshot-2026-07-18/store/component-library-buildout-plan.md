---
name: component-library-buildout-plan
description: "Dave's 2026-07-10 component-factory direction + the working build-out plan (housecleaning → gap-analysis target → prove-one-cluster → template tier → compound). Floor-first; unaudited; supersedes report §07 sequencing where they differ."
type: project
---
**Reframe firmed into a direction (Dave, 2026-07-10) — floor-first, still unaudited.** The project
became a **compliant component-building machine**; fulfil the brief by using it — **with designers
always guiding** (human-in-loop; answers the bus-factor-1 worry) — to build the library out from
**38 → ~200-300** (already scoped in `knowledge/_COMPONENT-LIBRARY-TARGET.md`; see also
[[library-composition-tier-gap]]).

**New facts Dave supplied (change earlier analysis):**
- **Sutherland is NOT a rich library to bind to** — it's the same **sparse ~36**, a *reflection of
  the Figma library*. So there is ONE sparse source reflected in three places (Figma ↔ Sutherland ↔
  our canon); build it out **at source** and it feeds all three. → the "which library — own vs
  Sutherland" fork from the deep review is **closed**.
- **Rationale = enrich the inference substrate.** More/richer canon → more *texture* to
  "semi-innovate" from, so even a **strict/retrieval run** can invent interesting on-brand solutions
  to new requirements. This is a **tune-the-inference move** (substrate, not prompt) that sits
  alongside the rule-tuning lead ([[ruling-generation-shape-2026-07-10]]). It also **lowers R1's
  stakes for the FLOOR product**: with a designer in the loop AND a richer substrate, autonomous
  single-pass quality is no longer the go/no-go — R1 becomes a tuning question, not a gate.
- **Method Dave proposed:** gap-analysis vs other libraries → requirements/spec docs → flesh out.

**Working plan (direction agreed; sequence is Claude's, for Dave's sign-off):**
1. **Housecleaning FIRST** (report §08 grooming): fix the 3 lying entry points (knowledge/README
   "32/four gates/Sutherland parked"; GOOD-MORNING trace-as-pending; _LIVE-STATE ADR-0006 gap),
   tombstone `_VISION-iteration-machine`, delete the 4 dead files, archive the June cluster, settle
   gate-count language, commit in-flight work. **Why first (not just tidy):** the build-out
   multiplies every artifact ~8× (300 comps = metas/snippets/gate-runs/KG-nodes), and **other
   designers must be able to read the repo** — a newcomer reading the current README is misled day 1.
2. **Target via gap-analysis across THREE tiers** — leaf · organism · **page templates/shells** (the
   tier we have ZERO of and the one that actually fixes flat layouts; harvest page patterns from
   GOV.UK/USWDS/Polaris/Carbon). Write specs in the **machine's own meta.json + snippet-contract
   format**, not prose, so a spec is directly buildable + gateable.
3. **Prove the loop on ONE cluster** before committing to 300 — a designer drives
   spec→generate→gate→**human-promote**→recompose a screen. Tests three claims at once: (a) does the
   machine actually speed a *designer* up; (b) does higher-tier canon measurably reduce flatness on
   recompose (**the texture hypothesis — measured, not assumed**); (c) does human promotion hold as
   the quality gate. De-risks 300 before building 300; doubles with **D2**.
4. **Build the template/shell tier + its governance** — needs a real compose/hierarchy/responsive
   gate (today's compose/screen gates are shallow + out-of-build) + layout-KG nodes. "Complete the
   library at the layout tier" = "build the generation-KG" — **same move**.
5. **Scale compounding**, cluster-by-cluster (splits F7 build-vs-compound: *targeted* build MAP from
   the gap-analysis + *compounding* DELIVERY, value each cluster). KG grows as a **byproduct** —
   each promote adds its typed edges (see [[ds-knowledge-graph-revisit]] for the overlay/property-
   graph approach: NOT GraphRAG; import ACT/axe-core for the SC↔rule leg; applies_to vs verified_by).

**Claude's caveats on record (feedback, not affirmation — Dave asked for critique):**
1. The load-bearing ~40-50 items are **templates/shells, NOT more leaf components** — prioritise the
   zero-tier or flat layouts won't move (this is the [[library-composition-tier-gap]] finding: the
   06-24 payments-journey proof already showed complete components ≠ a shippable screen).
2. "**Designers use the system**" is a **product dependency** — the tool must be usable by non-Dave
   ([[robustness-portability]] papercuts: ports, env fragility, no-Univers-font fallback, SSO portal).
   Phase 3 will expose it; budget for it.
3. 260 new components is a **multi-month, multi-designer programme** even with the machine — frame as
   "build the loop, then compound, ship each cluster," not "build 300 then ship." Prioritise D2's
   journey first, then highest-texture families, then templates.

**How to apply:** housecleaning is the agreed immediate next action (Claude to run the safe/reversible
parts on Dave's go, hold deletes for his nod). Full record in `_LIVE-STATE` OPEN. Pairs with
[[library-composition-tier-gap]], [[product-shape-flexing-engine]], [[ruling-generation-shape-2026-07-10]],
[[deep-analysis-report-2026-07-10]] (§07 R4).
