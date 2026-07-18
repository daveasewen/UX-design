# The §9 question: root cause and the 2026-07-10 ruling

> STANDING: decision-history file — provenance record, never edited after landing.
> **Relocated VERBATIM from `_LIVE-STATE.md` (lines 591–733) on 2026-07-18**, per the ruled
> consolidation (`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`). Spine summary: `_LIVE-STATE.md` → LIVE (generation shape) + OPEN F7.
> **RESURRECT (Dave, 2026-07-18): YES — the experiment chain is valuable for later evaluation.** We pivoted to the factory because it is foundational; the tuning questions return once the machine has all its parts. The 07-10 ruling itself stays LIVE in the spine.

---

- **🔴 OPEN, TOP PRIORITY — "What does the §9 spread actually reveal?" NEEDS A DEDICATED SESSION
  (Dave, end of 2026-07-05). This supersedes the "blocking external review" framing above — the
  gravity-fix + diagnostic + restyle-and-fix sequence all ran, and the result is confusing, not
  converging.** Dave's own words: "the canon works but probably no better than an AI model tied to
  a component library. The layouts tend to be better and the extra 'assumptions' or gap fillers
  seem better when unconstrained... I expected something like: unconstrained with the right
  styling" — i.e. he expected the gravity-fixed *expressive-v2* band to read as roughly
  "unconstrained-quality composition, wearing HSBC tokens," produced directly by the governed
  pipeline. Instead: the governed expressive-v2 bands (both models) still underwhelmed against the
  ungoverned diagnostic pieces on composition/organising-idea/gap-filling; the ungoverned pieces
  had to go through a SEPARATE, manual restyle-and-fix pass (this session's `without-influences-
  hsbc.html` work) to become brand-legitimate — and even that pass needed real bug fixes (a theme-
  alias trap, 3 invented icons, 4 real WCAG contrast failures) the ungoverned model never had to
  care about because it wasn't building inside real constraints. So the "two-step" path (generate
  free → constrain + verify after) visibly works end-to-end, but it is NOT what §9 set out to build
  (one governed pass that's good AND compliant) — and nobody has yet named which of these two
  shapes the engine should actually target.
  - **Two live hypotheses, unranked, Dave to weigh (his own framing as of this message, "its just
    about crafting the rules I guess, i need to read through them"):**
    (1) **Rule-crafting quality** — the gravity instruction (and the register-ramp prompts
    generally) may simply be under-specified/weak, not structurally capped; per
    `register-spread-2026-07-05-diagnostic/_FINDINGS.md`'s own closing line, the ungoverned run's
    real edge was asking for "a point of view on the data's structure," while the governed prompt
    asked to "extract patterns from named products" — a rule-wording gap, fixable by better
    prompting, not a ceiling. Read: `_FIXED-FLEX-CHARTER.md` §9 (the ramp definition) +
    `_TEST-BRIEF-v2-sme-payments.md` §2 (the actual per-band instructions, incl. the gravity block)
    — these are the exact rules Dave means to read through.
    (2) **Structural ceiling — generate-then-normalise.** Memory `generation-mechanism-ideas` Idea 2
    (parked 2026-07-01, Dave: "is this legitimate? yes, plausible") named this almost exactly: run
    ideation from pure inference, then pass the output through a converter/normaliser back onto
    canon. This session accidentally hand-executed that idea once (diagnostic → restyle-and-fix)
    and it worked — which is either the answer (formalise generate-then-normalise as the real
    pipeline shape) or a coincidence that shouldn't be over-read from one screen.
  - **Not yet done, don't assume it's done:** no one has compared "governed single-pass" vs
    "generate-then-normalise two-pass" as a controlled pair on the same screen — everything so far
    is one lineage (unconstrained → hand-restyled) vs a different lineage (governed ramp,
    Sonnet+Opus) that were never actually running the same experiment.
  - **Path:** own dedicated session, per Dave — this is a product-shape/architecture question
    ([[product-shape-flexing-engine]] territory), not a prompt-tuning afternoon. Don't resolve
    inline; start that session by reading this entry + the charter §9 + the test-brief §2 + memory
    `register-inference-ramp` + `generation-mechanism-ideas`.
  - **✅ Prep tooling agreed, same session (Dave: "is there a way we can build a trace to record
    what entities from the knowledge a cold run uses?") — build THIS as part of the dedicated
    session, not separately.** Two-layer design proposed and agreed: (1) a self-reported "sources"
    manifest emitted alongside each cold-run artifact (which guideline rules/tokens/`.cn-*`
    components/named gravity-references it drew on + a one-line reason each); (2) an automatic
    verification pass against the actual artifact — grep for real `.cn-*`/`.c-*` classes, `var(--
    token)` names, and icon path data (extending `_validate_icons.py`'s existing byte-match
    technique) — that flags claimed-but-absent or used-but-unclaimed mismatches. Layer 2 is
    load-bearing, not optional: this exact session already proved a cold run's self-report can
    claim a comment/derivation that isn't actually in the file, so the manifest alone isn't
    trustworthy without the cross-check. Run across the governed spread + gravity-fix + diagnostic
    pieces to get real comparable data on what each lineage actually retrieved vs invented — this
    is the closest thing to a direct empirical answer to the open question above. Reuses existing
    infra rather than new foundations: `_build_xref_index.py` (static token/guideline/component
    map) + the icon-source gate's byte-match method are the components to extend, not rebuild.
  - **✅ BUILT + FIRST EVIDENCE 2026-07-07.** Tools: `knowledge/_trace_knowledge_usage.py`
    (measurement) + `knowledge/_build_trace_dossier.py` (Swiss interactive dossier w/ canvas
    knowledge-graph viz, entity explorer, accordion, rule-adherence layer). Outputs
    `_KNOWLEDGE-USAGE-TRACE.html` / `.md` / `-ENTITIES.json`. Reconstructs retrieved-vs-invented
    from the artifact directly (no self-report needed — sidesteps the unreliable-manifest problem).
    Full record: memory [[knowledge-usage-trace-tool]]. **Result leans H(architecture/rules-design),
    not H(rule-adherence):** governed lineages are provenance-PERFECT (0 invented colours, ~200
    canon token refs, PURE-RETRIEVAL) yet flat → the governed rules are already saturated, so
    tightening application can't be the lever. Diagnostic (best layout, per Dave) is INVENTED (56
    live hex, 219 local vars) AND violates 6 rules/honours 1 → freer layout and rule-honouring pull
    in OPPOSITE directions. **Layout is the crux and the KB does not govern it** — charter line 34:
    "the canon has no template layer — always inferred"; zero `.cn-page/.cn-grid/.cn-layout`; canon
    governs only the *measure* (grid/breakpoints/spacing), and even layout-spacing tokens are
    ~0-retrieved (governed screens hand-author spacing in raw px).
  - **🆕 THIRD HYPOTHESIS ON RECORD (Dave, 2026-07-07): rules WRONG/TOO-TIGHT AT SOURCE.** Not
    mis-applied (H1), not pure architecture ceiling (H2) — constraining composition to reviewed
    human-made create.hsbc components may stifle the layout creativity that is the real
    differentiator. **Next probe Dave flagged: what would a *retrievable* layout/composition layer
    look like (page archetypes as graph nodes)** — the missing governance the trace exposed. Still
    no controlled governed-1-pass vs generate-then-normalise-2-pass run on one screen (the thing).
  - **🎯 ROOT-CAUSED 2026-07-07 → the library-composition-tier gap (H3 refined).** Verified: the
    invention rule (§6 retrieval-first + derive-from-fixed; §9 sober "retrieve and assemble what
    exists") is correct, but the **library stops at organism** — 38 comps = 9 atoms/23 molecules/
    6 organisms, **ZERO templates/shells/page-scaffolds**. So page composition has nothing to
    retrieve → flat layouts are *structurally forced*, not a tuning issue. The layout-governance gap
    and the library-tier gap are the SAME gap. `_COMPONENT-LIBRARY-TARGET.md` already scoped the
    fix (~200–300 catalog incl. Layer-2 shells/templates; "the automation can only compose what
    exists"). **OPEN DECISION F7: build-upfront (`_COMPONENT-LIBRARY-TARGET.md`) vs cluster-compound
    (ADR-0006 pt4 "compounding not completeness"; cluster-promotion = least-proven loop step).**
    Full session record: `knowledge/_FINDINGS-s9-session-2026-07-07.md`. Memories
    [[library-composition-tier-gap]], [[register-inference-ramp]], [[knowledge-usage-trace-tool]].
  - **🟠 COMPONENT-FACTORY DIRECTION + BUILD-OUT PLAN (Dave, 2026-07-10). Reframe firming toward a
    plan — still unaudited, floor-first.** Memory: [[component-library-buildout-plan]].
    Dave's frame: the project became a **compliant component-building machine**; fulfil the brief by
    using it (with **designers always guiding** — human-in-loop, answers bus-factor) to **build the
    library out 38 → ~200-300** (`_COMPONENT-LIBRARY-TARGET.md`). **New facts he supplied:** (a)
    **Sutherland is NOT a rich library to bind to — it's the same sparse ~36, a reflection of the
    Figma library** → there is ONE sparse source reflected in 3 places (Figma↔Sutherland↔canon);
    build it out at source, it feeds all three; the "which library" fork is closed. (b) **Rationale
    = enrich the inference substrate:** more/richer canon → more texture to "semi-innovate" from, so
    even a strict/retrieval run can invent interesting on-brand solutions. (This is a *tune-the-
    inference* move — sits alongside the rule-tuning lead [[ruling-generation-shape-2026-07-10]], and
    it lowers R1's stakes for the FLOOR product: a designer is in the loop + the substrate is richer,
    so autonomous single-pass quality is no longer the go/no-go.) His method: **gap-analysis vs other
    libraries → requirements/spec docs → flesh out the library.**
    **Working plan (agreed direction, sequence mine, for his sign-off):** ① **Housecleaning FIRST**
    (report §08 grooming — fix the 3 lying entry points, tombstone the vision mock, delete 4 dead
    files, archive June cluster, settle gate-count language, commit in-flight work). Rationale: the
    build-out multiplies every artifact ~8× and other designers must be able to read the repo. ②
    **Target** via gap-analysis across THREE tiers (leaf · organism · **page templates/shells** — the
    tier we have ZERO of and the one that actually fixes flat layouts); write specs in the machine's
    own meta.json+snippet format, not prose. ③ **Prove the loop on ONE cluster** (a designer drives
    spec→generate→gate→human-promote→recompose a screen) — tests designer-speed-up + the texture
    hypothesis (measurable, not assumed) + the promotion gate; de-risks 300 before building 300;
    doubles with D2. ④ **Build the template/shell tier + its governance** (new compose gate + layout-
    KG nodes = the generation-KG; "complete library at layout tier" = "build the KG", same move). ⑤
    **Scale compounding** cluster-by-cluster (splits F7: *targeted* build map + *compounding* delivery).
    KG grows as a **byproduct** (each promote adds typed edges). **My caveats (feedback, on record):**
    (1) the load-bearing ~40-50 items are **templates/shells, NOT more leaf components** — prioritise
    the zero-tier or flatness won't move; (2) "designers use the system" is a **product dependency** —
    the tool must be usable by non-Dave ([[robustness-portability]] papercuts: ports, env, no-Univers,
    SSO portal) — Phase ③ will expose it; (3) 260 new components is a multi-month multi-designer
    programme — frame as "build the loop then compound, ship each cluster," not "build 300 then ship."
  - **📄 EXTERNAL DEEP REVIEW 2026-07-10 → `reviews/REVIEW-2026-07-10-deep-analysis.html`** (repo root,
    untracked — commit it; also a desktop artifact). Independent whole-project pass: code-level
    architecture map, git archaeology, experiments/trace re-read, July-2026 field research (v0 DS 2.0 /
    Builder / Bolt = canon-tied generation is now commodity; gates + §9 tiering = ahead of all surveyed;
    RALF/LayoutRAG = retrieval-conditioned layout is published science), grooming inventory (entry-point
    staleness, ~45 archive candidates, tombstones owed). The report *leans* H2+H3; treat that lean as
    analysis input only — superseded on ranking by the ruling below.
  - **🟠 RULING (Dave, 2026-07-10) — direction after reading the review: RULE-TUNING + INFERENCE
    TIERING LEADS; double-pass is a component, not the architecture.** Dave's verdict on the two-pass
    evidence: the restyle/double-pass was "not all that successful" — it produced interesting insights
    and data, but is an interesting hypothesis, no more (this supersedes the earlier "pretty happy"
    reading of `without-influences-hsbc.html`). Way forward = **more experimenting on tuning the rules
    and tiering the inference, with a double pass forming PART of the process** (a stage, e.g.
    normalise/repair after gates — not the pipeline shape). **Future state affirmed: strict mode over a
    full component suite for the "factory"** (floor/churn end) — "arguably we could create this with
    less infrastructure." Consequences: (a) the review's R1 experiment becomes **three arms** on one
    contract — governed single-pass as-is · rule-tuned/re-tiered single-pass (lead hypothesis) ·
    two-pass — rendered, blind-judged; (b) note the empirical hurdle the trace sets for rule-tuning:
    governed output is already PURE-RETRIEVAL, so the tuning that can move the needle is *what the
    rules ask for* (tier definitions, composition licence per band, point-of-view prompts), not
    adherence tightening; (c) connects to OPEN DECISION F7 above (a fuller library tier is the
    strict-mode/factory path). Dave is now in a reading/thinking pass (charter §9, test-brief §2,
    findings doc, the review) — no build work on this thread until he rules again. Memory:
    [[ruling-generation-shape-2026-07-10]]. Unaudited node.
