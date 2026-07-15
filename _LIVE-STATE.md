# _LIVE-STATE — what's true now (cold-start spine)

*The supersession ledger for the project: what's **LIVE**, what's **DEAD** (don't build on it),
what's **OPEN**. Read this second, after `GOOD-MORNING.md`, before `knowledge/README.md`.
Per **ADR-0007**. ⚠️ **INTERIM — hand-maintained** until `_build_live_state.py` generates it from
front-matter edges + tombstones. Refresh at end of every session alongside the handoff.*

*Last refreshed: 2026-07-15 (Apollo library taxonomy mono/UI/SC + Apollo mono tokenisation “up to par” — motion tokens done, spacing/border/radius binding in flight, snippet-canon JS pending). Prior: 2026-07-14 (presentations + housekeeping). ⚠️ 07-15 pro-forma token edits landed to disk; commit in progress.*

> ⚠️ **AUDIT STATUS — everything below is RECORDED, not VALIDATED.** Provenance ≠ correctness.
> These entries capture *that* a decision was made and what it supersedes — **not** that it is
> right. Treat every node as **`unaudited`** until a human correctness-audit vouches it (ADR-0007).
> The ledger tells you what's live/dead; it does **not** endorse. Don't mistake a clean node for a
> vetted one.

---

## LIVE — current truth (in force)

- **Project name = Apollo** (2026-07-14). Renamed from *Promenaut* repo-wide (51 files + renames);
  the "Smart Design System" descriptor dropped in favour of **Apollo** (singular preferred; "Apollo
  SDS" acceptable). `archive/` included (kept as part of the one project). Commit be3c364.
- **Red rule = red is the PRIMARY-action accent, used ONCE per screen** (RULED Dave 2026-07-14) —
  **NOT destructive-only.** Destructive/error takes a distinct, non-red treatment. **Supersedes**
  the charter §4 register-tied "red-forward ceiling" (sober=destructive/accent, balanced/expressive=
  red-may-lead) → now universal. `BRAND-1` gate (`runs/proof-001.../gate2_assembly.py`) rewritten:
  blocks red on any non-primary action AND red used >once. **Propagation gap (OPEN):** historical
  fitness-test builds (`knowledge/_fitness-test/sme-payments*.html`) + proof-001 `_GATE2-REPORT.md`
  still state the old rule — regenerate if revived. Memory `apollo-rename-and-red-rule-2026-07-14`. Commit f8e05e5.
- **Designer pack = shipped-ready** (2026-07-14). `designer-skills-v1/` (4 skills + built KB, gitignored);
  handover artifact **`Apollo-designer-skills.zip`**. Delivery via VS Code + GitHub Copilot Agent
  Skills; **no Python for v1**. Intro (`notes/designer-pack-intro-teams.md`) for ~the 20th; hands-on
  the 24th. **Untested:** live-fire on a designer's machine (likely folder-placement) — top release risk.
- **Working model = land to the live repo as-you-go** (RULED 2026-07-14). Deliverables write straight
  to the connected repo via the desktop bridge, NOT cloud scratch; the `/tmp/ux` snapshot is stale —
  don't trust it. Keep GitHub Desktop CLOSED during Claude commits (lock contention). Memory
  `working-model-cloud-vs-device`.
- **Repo restructured for human-readability** (2026-07-14). Root = operating essentials only
  (README · AGENTS · GOOD-MORNING · _LIVE-STATE · MODEL-ROUTING); new `reviews/ notes/ projects/`;
  visual map at `docs/repo-map.html`. Commit 70d38f6.

- **Component library = Apollo pro-forma programme** (STARTED 2026-07-14, in flight). Building the
  *whole* inventory as a lightly-styled **pro-forma** (generate → iterate; styling cascades via
  tokens), then expressing it in MODES: Mode 1 = current HSBC brand (KB tokens as-is); Mode 2 = a new
  **business-line "big sister"** (rounded corners, monochrome, usability-first — colour only where
  meaningful, own type stack + DataViz), captured as a divergence **token mode**, never canon edits.
  ONE component skeleton, N modes — the cascade IS the proof of the factory. Chose **A** (KB-as-base;
  binds by intent so a neutral sub-floor can slide under later). Correctness = a **scramble-test** idea
  (wrong token values → anything that doesn't move is hardcoded). Reviewable build list =
  `reviews/ITINERARY-2026-07-14-apollo-component-library.{html,xlsx}` (124 items: 38 gated / 7 partial /
  79 gaps; 23 P1). IN FLIGHT: proof batch of 6 net-new **atomic** foundations (Icon button, Empty
  state, Skeleton loader, Amount/currency input, Stepper, Drawer) through the gated pipeline to
  validate the pro-forma contract + factory struct-mode. Memory `apollo-component-library-itinerary`. **UPDATE 07-14 eve — TRANCHE 1 DONE** (all 6 as one interactive MONOCHROME file `knowledge/_proforma/Tranche-1-interactive.html`; near-black primary, colour=meaning, real HSBC icons ENFORCED via `_check_proforma.py`; `_PROFORMA-RULES.md` living; artifact `apollo-proforma-tranche-1`). LESSON: a new surface needs its gate wired. **UPDATE 07-14 late — TRANCHES 2–5 DONE + UNIVERSAL GATE PROMOTED** (T2 Toast/Alert/Date-picker/File-upload · T3 Selection-controls · T4 Nav/disclosure · T5 Containers/status, ~19 comps, all gate-green + rendered/inspected; RAG palette RETRIEVED from `tokens/semantic-colour.json`; new `knowledge/_validate_proforma.py` = mode-agnostic universal gate WIRED into `_build_all.py` + a manifest-path-is-real check; verified on Dave's machine 5/5 pass, 39/39 asset paths real; artifacts `apollo-proforma-tranche-2..5`; 6 files landed via bridge for Dave to review+commit+push). MODE rules (monochrome/near-black/square) kept as the subset, NOT gated. Full: [[proforma-programme]].
- **Apollo = THREE libraries** (NAMED Dave 2026-07-15): **Apollo mono** = the monochrome pro-forma
  (unbranded, colour=meaning; the base + the **user-testing** build + Figma-transfer target — Tranches 1–5,
  memory [[apollo-mono]]); **Apollo UI** = a NEW library where **varying radii** live (rounded; the
  usability-first "big-sister" variant — radius is NOT flat here); **Apollo SC** = the **branded** build
  worked on previously. ONE skeleton, expressed as token MODES — radius/colour/motion are mode-overridable
  tokens, never canon edits. (Refines the earlier "Mode 1 brand / Mode 2 big-sister" framing above.)
- **Token governance — getting Apollo mono "up to par"** (Dave 2026-07-15, IN FLIGHT): (a) MOTION = pure
  CSS + tokens, no JS — size-bucketed `--btn/--ib/--card-grow/press` (~1px/side travel) + named `--accent-*`
  pops; `sizeScale()` removed; **DEF-003** gate enforces no JS motion. (b) COLOUR fully tokenised + gated.
  (c) SPACING/BORDER/RADIUS → bind to the KB **`semantic-scale`** (`tokens/spacing.json`+`layout.json`):
  border-width 1/2/4, **radius = a MODE TOKEN** (`--radius:0` in mono; **Apollo UI overrides** with its
  varying radii). Full semantic-responsive spacing map = a **Figma-stage** job (don't rationalise approved
  layouts pre-Figma). (d) REMAINING: snippet-canon JS holdout — `GROW=7/PRESS=9`+`sizeScale` in 4
  `snippets/*.reference.html` (Button/Modals/Quick-actions/Selection-controls) → migrate to CSS tokens.
  A rule + gate (DEF-004: no raw spacing/border px in component CSS) to keep future additions tokenised. Memory [[apollo-mono]]. **Border-width (1/2/4→--bw-*) + radius (MODE token: --radius:0 mono · --radius-round circles · --radius-pill:999px) DONE + written-back 2026-07-15, value-preserving (render-diffed identical).** **SPACING DONE** (all padding/margin/gap → `--space-*`, value-preserving — computed spacing identical on 1,474 elements; + 3 stray `1.5px` field borders → `--bw-1_5`). **DEF-004 no-hardcode gate BUILT + WIRED** (`_validate_no_hardcode.py`, step 21/24; flags raw spacing/radius/border px in component CSS; caught the 1.5px leaks; self-tested) — **full build green 24/24**. Rule 15 + DEF-004 defect entry added. **Remaining: the snippet-canon JS holdout only.**
- **FOUNDATIONAL — no hardcoded styling; everything TOKEN + MODE governed** (RULED Dave 2026-07-15):
  going forward NOTHING is hardcoded — ALL styling (colour, spacing, radius, border, motion, type) is a
  **token**, and the sibling libraries (**Apollo mono/UI/SC**) are governed purely by **MODES** (token-value
  overrides over the ONE skeleton). Goal = **maximally flexible + future-proof**: adding a library = adding a
  mode, never forking components. Enforcement = the planned **DEF-004** gate ("no raw styling value in
  component CSS", wired into `_build_all.py`). NB geometry/component dimensions (widths/heights, CSS-triangle
  arrows) are a separate axis, not "styling" — revisit if we also bind the KB icon/layout size scales.
- **ATOMISE — build at the true atomic level, compose up** (RULED Dave 2026-07-14). Rolled-up
  patterns (e.g. Notifications = inline + toast + global + contextual in one molecule) are a **debt**,
  not the model; going forward build atoms → molecules → organisms per the `meta.schema` category
  ladder, exposing the atoms. Known debt: decompose the existing rolled-up molecules in a later
  refactor. Applies to all new component work.

- **Product = a *flexing* engine** — one governed core, dials per work-type; floor/churn ("vibe")
  vs ceiling/novel ("analysis"). `ADR-0006`.
- **Output modes = a first-class dial** (Dave, 2026-07-05): the engine must produce **two fidelity
  tiers** — (1) **"dumber" portable HTML-component prototypes** (library-agnostic, no build; the
  portability floor) and (2) **build-ready output from a prebuilt library**, with **Sutherland** (the
  HSBC React lib) the intended build target ("build directly using Sutherland"). **Portability =
  NOT married to Sutherland** — dumb-HTML mode, or ingest other libraries, or whatever strategy wins;
  Sutherland is *a* target, not *the* architecture. Note the two-way tie: our **dark-mode work feeds
  back INTO Sutherland** while Sutherland is also our **build target** (same artifact up- and
  downstream); the **Figma library IS Sutherland's working file.** Memories: `output-modes-portability`,
  `sutherland-figma-mapping`. Unaudited node (extends ADR-0006).
- **Register = an inference ramp** (NOT a look): sober = retrieve · balanced = extend ·
  expressive = invent. Charter `_FIXED-FLEX-CHARTER.md` **§9**.
- **§9a — provenance of "reads HSBC"**: brand-ness resolves to named sources (primitives→token
  store · composition→`canon/canon.css` · character→`brand-principles.md` · tone→§4b · red→
  `colour-usage.md`); flag-where-silent is an advisory generation behaviour; residual gestalt =
  human. Brand-source-stop column on the §9 band table. Record:
  `knowledge/_PROVENANCE-inference-levels_2026-07-04.md`.
- **Two harness modes** (§9a): converge/ship = **mode B** advisory brand self-check (ADOPTED) ·
  explore/noodle = **mode A** open human gestalt (OPEN). Mode = a first-class harness dial.
  Memory: `harness-two-modes`.
- **Project memory = temporal decision-graph pattern**, lightweight-first; **this file is the
  cold-start spine.** `ADR-0007`. Memory: `pm-knowledge-graph-direction`.
- **Supersession discipline** (non-negotiable, `AGENTS.md`): any ruling that kills something must
  tombstone the artifact + log the propagation gap in the same pass.
- **Git split** (`AGENTS.md` + memory `git-push-method`; no standalone ADR): Claude commits in terminal + clears
  stale `.git/*.lock`; **Dave pushes via GitHub Desktop only** (never terminal push, never Desktop
  commit, Desktop closed during commits).
- **Build**: `python3 knowledge/_build_all.py` — runs the full gate set (integrity · contrast ·
  snippet · icon-source · a11y · coverage · dark-surface · rules-index); green = internally
  consistent, dark-legible, surfaces not flat-white, snippets match canon. *(Doc-drift: older notes
  say "four gates" — it's ~8; fix on the Tier-B build-gate audit.)*
- **State machine records FUTURE/TARGET states too** (RULED 2026-07-05, Dave; extends `ADR-0007`):
  this ledger carries not just current truth + change history but **where we intend to be** — see the
  `## PLANNED / TARGET STATES` section below. A target = what · why · blockers · source. The
  staleness gate must flag a target whose blockers have cleared but whose status still reads
  "blocked" (the Sutherland failure). This ruling is itself an `unaudited` decision node (extends the
  vouched ADR-0007).

## SUPERSEDED / DEAD — do not build on

- `knowledge/_fitness-test/sme-payments-registers.html` — old **looks-based** register dial
  (surface/accent/motion knobs). → superseded-by charter §9 (2026-07-05). Tombstoned.
- Register-as-"described-look" (dark band / hero / gradient) — → superseded by §9 inference ramp
  (2026-07-03).
- Terminal-only push / "GitHub Desktop retired" (07-02 ruling) — → superseded by the git split
  (07-05).
- `knowledge/_NEXT-SESSION.md` — retired, → superseded by `GOOD-MORNING.md`.

## OPEN — propagation gaps + parked threads

- **⚠️ PROPAGATION GAP (partially closed):** the product vision still speaks the OLD looks-language —
  `ADR-0006` + `notes/_VISION-iteration-machine_2026-07-03.html` say "cool/warm/hot register switch" with
  surface-band moments (the mock even has a `border-radius:10px` cardinal violation) — **still
  open, not yet touched.** One instance of the gap **was** reconciled 2026-07-05:
  `_TEST-BRIEF-v2-sme-payments.md` §2 rewritten from look-language (surfaces/hero/gradients) to §9
  inference-language (retrieve/extend/invent + cardinal/foundational curbs). The vision doc + ADR-0006
  itself remain unreconciled — do that when next in that area.
- **✅ Worked spread — DONE 2026-07-05, TWO instances (Sonnet + Opus re-run).** First
  retrieve/extend/invent spread under the §9 inference definition: SME Payments screen, three bands
  generated in isolated parallel passes. **Sonnet pass:** cardinal curbs held with zero violations;
  foundational curbs diverged monotonically with the register, as predicted. **Dave reviewed the
  actual HTML and found two real gaps**, not just polish: (a) sober used the never-reviewed
  `.c-stat-grid` utility instead of the gate-reviewed `.cn-account-card` for the same data —
  the brief said "retrieve" but had no rule ranking canon artifacts by rigour; (b) expressive
  wasn't bold enough despite nominal MAX-inference licence. Dave also asked whether a
  build→review→correct loop exists (**it didn't**) and proposed testing Opus. **Fixes made same
  session:** (1) `_TEST-BRIEF-v2-sme-payments.md` §2 now states an explicit, mechanical **canon
  rigour tier** — `.cn-*` (gate-reviewed, generated from snippets) always preferred over `.c-*`
  (hand-authored, never reviewed) when one fits; (2) re-ran the full spread on **Opus**. **Opus
  re-run result:** all three bands now retrieve `.cn-account-card`; sober dropped to **zero**
  `.c-*` fallback usage (from relying on it for its centrepiece); expressive reads as a
  substantially bigger compositional swing (needs Dave's eyeball, not just structural grep) — same
  cardinal-curb floor held throughout with zero violations. **Bonus finding:** two independent Opus
  passes caught a real ambiguity in the contract's own §3 wording (conflated "sum of all 5 rows"
  with "scheduled total") that neither Sonnet pass flagged — fixed in the contract. Full writeups:
  `knowledge/_fitness-test/register-spread-2026-07-05/_PROBE-and-selfcheck.md` (Sonnet pass) +
  `register-spread-2026-07-05-opus/_COMPARISON-sonnet-vs-opus.md` (the re-run + comparison).
  Memory: `register-inference-ramp`, `spread-review-gaps-2026-07-05`. **Still not "proven"** — one
  screen, two passes changing two variables at once (rigour-tier rule + model), no rendered visual
  check, and Dave hasn't yet confirmed the Opus expressive band actually reads more exciting. A
  designed build→review→correct loop remains unbuilt (Opus self-corrected mid-pass on one bug, but
  that's not the same as a designed loop).
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
- **Divergence probe — first real run done 2026-07-05** (structural/grep-based, not the full
  novelty-scoring tooling named in §9). See the writeup above. The formal tooling (threshold
  calibration, automated novelty count) is still named-not-built.
- **Named-not-built harness machinery** (§9/§9a): isolated generation · divergence probe · mode-B
  brand self-check · the mode dial.
- **PM-KG MVP** (`ADR-0007`): build `_build_live_state.py` + the staleness gate — own focused
  session.
- **✅ Decision-corpus correctness audit — TIER A CLEAN 2026-07-05 (ADR-0007 §5).** Method:
  `knowledge/_RUNBOOK-decision-audit.md`; ledger: `knowledge/_DECISION-AUDIT.md`. Batches 1–3 run in
  fresh sessions. Batch 1: **ADR-0005 vouch · ADR-0007 vouch · §9/§9a vouch(framing)+defer(proven) ·
  ADR-0006 amend · `derivation-governance` amend.** Batch 2: **ADR-0006 re-audit vouch ·
  `derivation-governance` re-audit split · ADR-0001 vouch · ADR-0002 vouch · ADR-0003 defer ·
  ADR-0004 vouch+rationale-amend.** Batch 3: **charter §4 amend+defer · charter §4b defer ·
  two-harness-modes defer(kept A) · supersession-discipline vouch;** triage **git-split → Tier B ·
  build-gate → Tier B (fast-follower).** **Every Tier A node now has a verdict — the milestone that
  retires the "everything is unaudited" risk for foundational nodes.** Standing OPEN follow-ups:
  §9 proof-obligation · ADR-0003 KG/ingestion · §4 language-strip · TOV content audit ·
  harness-modes exploration. **Next audit work: Tier B opportunistically (feedback/project memories,
  runbook rules) + Tier C by sample/on-touch — NOT the priority; per Dave the next session is the
  seaworthiness planning run.** Never run the audit in a loaded session.
  - **Operational follow-ups from ADR-0004 (07-05, not correctness faults):** (a) **verify current
    EAA / EN 301 549 legal position** (2026-05-31 legal facts are point-in-time); (b) the installed
    `design:accessibility-review` skill audits to **WCAG 2.1 AA** — align to the project's 2.2-AA
    bar; (c) `wcag_version` config param survives only in `archive/harness-v0.1/`, live engine
    hard-targets 2.2. Foundational driver now recorded in ADR-0004: HSBC aspiration = *most digitally
    accessible bank in the world* (bar leads, not complies; ratchets over time).
  - **⚠️ AUDIT-DEFERRED verification (charter §9/§9a) — DO NOT FORGET (Dave, 07-05).** The
    inference-ramp *framing* is vouched, but its *proven/safe* status is **deferred** pending: (a)
    the first worked retrieve/extend/invent spread on one screen — **✅ first instance done
    2026-07-05**, see the worked-spread entry above; (b) the divergence probe + isolated generation
    + mode-B self-check — **✅ first-pass run done 2026-07-05** (isolated generation used for real;
    probe was structural/grep-based, not the full novelty-scoring tooling; mode-B self-check run
    manually against the six principles). **Still not "proven"** — one screen, two spreads now
    (Sonnet + an Opus re-run that fixed two real gaps Dave found on eyeball review), no calibrated
    tooling, no rendered visual check, and Dave hasn't yet confirmed the Opus expressive band reads
    as more exciting. Re-audit §9/§9a's proven status once Dave has reviewed both writeups + all six
    HTML files and, ideally, a second *screen* (not just a second model) with more compositional
    latitude than payments exists, to check the probe isn't just measuring "payments is always
    narrow-road."
  - **Re-audit obligation (two amended nodes).** ADR-0006 (register dial corrected to §9 inference
    ramp) and `derivation-governance` (staged multi-human promotion path) were **amended** in the
    audit; their amended text **re-enters `unaudited`** and must be re-audited in a later batch.
  - **OPEN thread — staged-promotion / extension-library process (from `derivation-governance`
    amend).** Define how inference-born ideas move: holding-pen/sandbox → colleague review →
    "extension library" (separate-but-connected canon) → general canon if broadly useful. Not yet
    worked out; connects to the ADR-0006 compounding-canon promote loop + `gap-pattern-build`.
    **Re-audited 07-05 (batch 2): direction VOUCHED, mechanism DEFERRED — kept OPEN not banked.**
    **FUTURE FEATURE (Dave, 07-05 — capture-only, build once the goal is set):** tiered access to
    canon commits — roles **design-system admin → domain admin → standard**; **sandbox open to
    everyone**, **commits tiered**; **extension libraries readable by all, edit privileges gated by
    domain + commit right**; general-canon promotion still needs the multi-human bar. Set the goal
    first, then the access model falls out of it.
- **⭐ NEW — Harness modes + dials exploration (from two-harness-modes defer, 07-05 batch 3).**
  Kept **Tier A** but **DEFERRED** — abstract/named-not-built, inherits §9a (framing vouched, proven
  deferred). **Dave's reflections to carry:** the harness must be **flexible to a degree** — the modes
  might be a **clean switch, or both** (a simple toggle *plus* an **advanced mode** to tune it); maybe
  even a **"let it rip" mode** (for fun); **finding the use cases is the important part**; approach =
  **research + iterate, start small, expand if needed**; the **dials themselves may need exploration,
  and that exploration may define the settings/toggle**. Own research thread — not the audit. Memory:
  `harness-two-modes`; ledger: `_DECISION-AUDIT.md`.
- **⭐ NEW — Tone-of-voice (TOV) = digital-editorial spin-off + future content audit (from §4b defer, 07-05 batch 3).**
  §4b deferred. Dave's framing: **TOV is genuinely useful for DIGITAL EDITORIAL** and is a **candidate
  spin-off thread** (its own home, separate from the interface engine). For **interfaces it is NOT a
  priority** — the exception is guidance for the **neutral decisions: labelling, language/locale,
  formality**. The wit-licence-per-band mapping can't be vouched without **auditing the actual TOV
  content** (tov-001…051) against the KG — a **possible future thread**, not this audit. Tagged on
  memory `tone-of-voice-ingest`. Ledger: `_DECISION-AUDIT.md` (§4b).
- **⭐ NEW — Charter §4 language-strip (HARD follow-up, from §4 amend+defer, 07-05 batch 3).**
  Audit ruled §4 **amend + defer**: the ramp is governed ONLY by cardinal + foundational curbs +
  inference levels + full compliance, all **retrieved from the KG** — §4's interpretive *language*
  (prose rulings on flatness/red/rounding) is recall-by-adjective (§9/§9a) and must be **stripped**,
  leaving the four curbs only as KG-sourced curb/level derivations. Dave flagged this as a **HARD
  follow-up**, not a quick edit — **do it inside the unified-KG/ingestion thread below, not as a
  standalone charter tweak.** Completeness of the derivations is **deferred** (unprovable until
  ingestion is finished). §4's amended text will re-enter `unaudited`. Ledger: `_DECISION-AUDIT.md`.
- **⭐ NEW — Unified DS knowledge-graph + ingestion, done right (from ADR-0003 defer, 07-05).**
  ADR-0003 was **deferred** (not vouched): Dave reopened the founding instinct that the *whole*
  design-system corpus (component specs, foundations, tokens, snippets, create.hsbc guidelines) is
  **one interlinked graph**. Today that interlink lives only inside the compliance graph. **Root
  cause: ingestion was never completed** (attempted, curtailed). This is a **separate, structured
  work thread with its own audit-grade method** — stated aim: do it correctly this time. Scope:
  map the entity/edge model across the full corpus; decide keep-hybrid / go-unified / **overlay-
  index layer** (leading hypothesis — link across existing stores, don't collapse into one monolith;
  extends `_blast-radius.json` / `graph-index.json`); connect to `graphify-tool` + ADR-0007 infra.
  Memory: `ds-knowledge-graph-revisit`. **Own focused session — not the audit.**
  - **🟠 DESIGN DIRECTION (Dave, 2026-07-10) — from the deep-review KG question; folded into the plan.**
    The compliance "KG" is today an **inverted index, not a graph** (`_build_compliance_kg.py:61–78`:
    self-asserted `relatedSC` arrays flipped into two lookup tables; no SC→SC or component→component
    edges; meta `relationships` never compiled; `query.py` = one-hop dict joins + substring match).
    **Verdict: fine for its current job, wrong for the roadmap** — the layout tier (R4), blast-radius
    reasoning and this ADR-0003 thread all need cross-store *traversal* the index can't do. Chosen
    approach when this thread is taken up:
    (1) **NOT GraphRAG.** GraphRAG *extracts* a graph from unstructured prose for fuzzy sense-making;
        our compliance entities are already structured records with IDs — extraction adds LLM cost +
        noise over clean data. The need is *connection*, not extraction → **overlay-index/property
        graph** over the existing stores (sources of truth stay; edge-layer is derived + regenerable;
        no monolith). Tiny embedded property graph (typed edges in JSON, or Kùzu/DuckDB-PGQ) if real
        path queries are wanted — no RAG machinery.
    (2) **Guideline granularity — not finer text, typed EDGES.** Rules are already ~1-bullet granular;
        don't shatter them. Split only where one rule *bundles* several constraints, so each atom maps
        to exactly one target (the **ACT "atomic vs composite"** distinction). Then add the edge from
        each atomic rule → the token/component/SC/pattern it governs (today those are prose `[REVIEW]`/
        `F1` notes). Connected text, not smaller text, is what multiplies relationships.
    (3) **Import, don't hand-type, the SC↔rule leg.** W3C **ACT Rules Format 1.1** (W3C Rec, Feb 2026)
        + **axe-core** rule metadata already publish rule↔SC machine-readably. Ingest that; hand-curate
        only the **component↔SC** leg (our genuine novelty — exists nowhere else). = report **R6**.
    (4) **Type the edges to give them teeth: `applies_to` (claimed) vs `verified_by` (an executable
        rule exists AND passes).** Turns the graph from bookkeeping into "which compliance claims are
        actually enforced vs merely asserted" — the queryable form of the shallow-a11y-gate finding.
    (5) **Keep the two retrieval needs separate.** The structural compliance graph (above) ≠ the
        advisory "massive-brain designer reads the 462 guideline rules per run" need — *that* one is
        retrieval-over-prose and is the one place a vector/light-graph layer earns its keep. Don't make
        one architecture be both.
    **Sequencing (holds the F5 anti-pattern at bay):** do NOT build now as standalone infra — it rides
    with the **layout/library tier (R4)** + Ingestion **Phase 3**, which are inherently graph-shaped
    and are the natural moment to introduce typed edges (the compliance index becomes one *projection*
    of the overlay). Cheap-now slice if wanted: type the existing edges + import ACT. Unaudited node
    (feeds ADR-0003 when reopened). Report: `reviews/REVIEW-2026-07-10-deep-analysis_rev2.html` §03 gap-3, R4, R6.
- **✅ Seaworthiness plan — DONE 2026-07-05 → `notes/_SEAWORTHINESS-PLAN_2026-07-05.md`.** Curated,
  dependency-aware sequence (not a flat backlog): hull patches (ingestion Phase 0 + capture ritual) →
  **big-rock #1 Ingestion Phase 1** (Sutherland token migration, confirmed unblocked) → **§9 worked
  spread in parallel** → **big-rock #2 PM-KG MVP** (staleness gate) → finish/unify (Phase 2→3→4, with
  the §4 language-strip inside Phase 3). Waiting/parked (D2, toolkit t2, harness-modes, TOV spin-off,
  ADR-0004 ops) kept off the critical path. Capture ritual/gate spec decided in the doc (ritual now,
  gate script alongside PM-KG MVP).
- **✅ Phase 0 (ingestion tracking hygiene) — CLOSED 2026-07-05.** The "39 metas vs 38 in the
  compliance graph" drift flagged in the prior session's KG spot-check was a **false alarm**: 39
  files exist in `components/`, but one (`EXAMPLE-button.meta.json`) is the authoring template,
  correctly excluded by `_build_compliance_kg.py`. Real component count is 38, matching the graph
  exactly. Rebuilt the KG to confirm — `git diff` on `compliance/graph-index.json` and `compliance/rules/`
  was **empty**; the graph was already current. Fixed a latent bug while here: `generated` was a
  hardcoded literal (`"2026-06-18"`) rather than today's date — a miniature of the exact
  "tracking rots silently" failure this plan exists to prevent; now stamps dynamically
  (`datetime.date.today()`). The `_DESIGN-SYSTEM-GAPS.md` correction banner + `_INGESTION-ASSESSMENT_2026-07-05.md`
  as single entry point both confirmed standing. Phase 0 fully closed; Phase 1 (Sutherland token
  migration) is next and is real, unblocked work — unlike this drift.
- **D2 — novel-screen test — THE #1 unlock.** Waiting on a colleague's brief (their brief-v2 +
  own baseline + signed contract *before* generation). `notes/_TEST-PLAN-novel-screen-proof.md`.
- **Toolkit tranche 2** (Dropdowns ×4) — parallel cheap-model workstream. Memory:
  `common-toolkit-survey`.

## PLANNED / TARGET STATES — where we intend to be (for planning, per ADR-0007 extension)

- **🎯 TARGET — Gates-as-a-service → close the agentic loop** (Dave 2026-07-14). Expose Apollo's own
  Python validators (contrast · token-fidelity · a11y · icon-provenance) as **callable tools (an MCP /
  tool interface)** so a host agent runs them **mid-task**, not only in the batch `_build_all.py` CI run.
  *Why:* the validators are the **verifier** — the expensive, differentiated half, already built; wiring
  an agent to call them iteratively (generate → check → fix → re-check) is the **cheap half** that turns
  v1 (skills + KB, one-pass retrieval = *agent-ready*) into *agentic* (self-correcting). Also removes the
  per-designer Python-install blocker. **NOT** the Figma MCP (that's ingestion, already used) and **NOT**
  Sutherland (build target) — this is Apollo's OWN checks as a service. *Blockers/honesty:* the **repair
  loop is "not built"** (deep-analysis architecture diagram); gates verify **declared** obligations only
  ("honesty system, not inspection") — real autonomy may need inspection-mode checks. Connects to the §9
  "generate-free-then-constrain-and-verify" two-pass. Memory `agentic-loop-gates-as-service`. Unaudited —
  an idea recorded today, not a spec.


*The forward-looking dimension of the state machine. Not current truth (that's LIVE) and not a flat
backlog (that's OPEN) — these are intended end-states with a path. Refresh alongside LIVE/DEAD/OPEN.*

- **🔴 SUPERSEDED BY OPEN QUESTION BELOW (2026-07-05, end of session) — Dave's verdict landed,
  and it's not the "converges once gravity-fixed" outcome this target-state assumed.** See the new
  OPEN entry "What does the §9 spread actually reveal?" — this target-state's own diagnosis (craft
  gap → sourced external references → re-run) is no longer the live framing; kept below for the
  historical trail only.
- ~~**🎯 Inference-gravity for the register ramp (expressive craft fix) — ⚠️ BLOCKS external
  review of the §9 spread until resolved (Dave, 2026-07-05).**~~
  - **Target:** the expressive band reads as genuinely exciting/award-calibre digital-product craft
    (motion, depth, interaction choreography) — not just "sober, but bigger" — while the cardinal
    curbs (brand colour retrieved not typed, type, square corners, a11y/safety floor) still hold
    with zero violations, same as the two spreads already run.
  - **Current vs target:** two isolated 3-band spreads run (Sonnet, then Opus) on the same SME
    Payments contract. Both closed the sober retrieval gap (finding 1 — now uses `.cn-account-card`
    via the canon-rigour-tier rule) but **neither closed the expressive excitement gap** — Dave
    judged both against `sme-payments-portfolio.html` (an older, ungoverned "craft piece" with
    hover-lift+shadow/spring easing, radial-gradient hero glow, count-up motion, backdrop-blur
    modal) and found the governed expressive bands still underwhelming by comparison.
  - **Diagnosed cause (this session, confirmed against the actual prompts):** every expressive
    prompt gave *permission* (curbs lifted) but never *direction* — no external creative reference,
    only internal/corporate source material (`canon.css`, `brand-principles.md`,
    `colour-usage.md`). Permission without a target to reach for makes the model recombine what it
    already has rather than invent something new. Full diagnosis: memory
    `spread-review-gaps-2026-07-05`; comparison data: `_COMPARISON-sonnet-vs-opus.md`.
  - **Blockers:** the design tension is resolved in principle — an explicit guardrail now exists
    (pattern only: composition/motion/interaction; never colour/type/logo, which stay retrieved
    from HSBC canon) — but **Dave's eyeball verdict on the actual result is still outstanding.**
  - **Path — steps 1–3 DONE same session, step 4 is next:**
    (1) ✅ defined the inspiration source + guardrail as an explicit "inference gravity" instruction
    (Linear/Stripe/Mercury/Ramp/award-calibre-fintech, each with a named pattern to extract —
    sourced via web search 2026-07-05, not recall); (2) ✅ added it to
    `_TEST-BRIEF-v2-sme-payments.md` §2's expressive bullet, alongside the corrected §3 wording
    (the scheduled/awaiting labelling ambiguity found during the Opus run); (3) ✅ re-ran **only**
    the expressive band on both models as `expressive-v2.html` in each spread folder — grep-verified
    (not just self-reported): motion/animation/transition mentions roughly doubled-to-tripled
    (Sonnet 4→23, Opus 2→15), `backdrop-filter`/blur depth technique appears for the first time in
    either run (0→5 Sonnet, 0→3 Opus), `prefers-reduced-motion` still present in both, zero
    `border-radius` violations, zero brand-colour leaks (every hex is inside a comment citing the
    `var()` it derives from), all figures verbatim including the corrected §3 wording. **(4) NEXT —
    Dave reviews via the updated `register-spread-2026-07-05-compare.html`** (now has an
    "Expressive (v2 — gravity fix)" button per model, plus a direct "Portfolio piece" reference
    button) **against `sme-payments-portfolio.html` specifically for motion/depth/interaction craft.
    This is the actual test — structural counts are a proxy, not the verdict.** (5) once Dave
    confirms, fold the mechanism into charter §9 as a named piece and only then is the §9 spread
    presentable outside this session. **Scope discipline held:** this stayed inside the existing
    "prove-the-core, §9 worked spread" parallel track from `notes/_SEAWORTHINESS-PLAN_2026-07-05.md` —
    did not touch hull patches (done) or reorder Ingestion Phase 1 (still queued, untouched).
  - **Additional diagnostic run, same session (Dave's idea): pure-inference ceiling probe.**
    Two cold Opus passes on the same data, zero brand governance at all (no canon, no curbs, no
    a11y mandate) — with vs without the named influences — to see the true ceiling and isolate
    where the governed version's gaps are. Finding: colour/type/radius gaps are expected (that's
    what the cardinal floor is *for*); the more useful signal is structural — the ungoverned runs
    reached for a genuine organising idea (e.g. "time as the spine") that the governed gravity-fix
    prompt didn't, suggesting the next iteration should ask for a point of view on the data's
    structure, not just borrowed craft patterns. Writeup:
    `register-spread-2026-07-05-diagnostic/_FINDINGS.md`.
  - **Also fixed same session:** a real CSS cascade bug in Opus's `expressive-v2.html` (an
    equal-specificity, later-in-source `.cover > *{position:relative}` rule was silently
    overriding the decorative glow div's `position:absolute`, dropping it into normal flow as a
    520px block and pushing all content down — the "huge black box" Dave flagged from a
    screenshot); and a real comparability bug — three of the ten spread artifacts (Sonnet
    `expressive-v2`, Opus `sober` v1, Opus `balanced` v1) were built as fixed mobile-phone-width
    layouts (390-560px, one with a bottom tab bar) while the rest were desktop-width (900-1240px).
    Normalised all three to a shared desktop container (960px) so the comparison viewer
    (`register-spread-2026-07-05-compare.html`, now also carries the two diagnostic files) is
    genuinely like-for-like. No content/data/curb changes in any of these fixes.
  - **✅ Restyled-ceiling build, same session (Dave: "if we style these using the HSBC
    primitives I'd be pretty happy").** Took `without-influences.html` (Dave's pick — the
    diagnostic piece with the stronger organising idea) and rebuilt its `:root` palette as a
    thin alias layer into canon tokens (accent/warn/info/ok/muted), replaced all three Google
    Fonts with the Univers ramp, squared every corner except the avatar exemption, and
    reinstated the cardinal safety/a11y floor the diagnostic had been told to skip (the
    £45,200 payroll approval was identical to the low-value row — now gated behind a
    confirmation dialog; added focus rings + reduced-motion handling). Kept every
    compositional/motion decision: the "Today's arc" day-timeline and the horizontal
    scheduled-payments timeline (flagged as candidates — no `.cn-*` equivalent exists for
    either). One disclosed deviation: outflow is no longer rendered in red (HSBC's dark-mode
    error token shares the same hex as the brand accent; kept red to the one accent/approval
    job, direction carried by an icon instead). File: `without-influences-hsbc.html`; wired
    into the comparison viewer. Dave confirmed via screenshot that the restyle's structure
    matches what he's judging against — visual verdict on the restyle itself still pending.
  - **✅ Bug found + fixed from that screenshot:** the hero balance number ("122,450") was
    rendering effectively invisible. Root cause was the exact trap canon.css documents at its
    own line 495-496 — my restyle's `:root{ --ink: var(--page); --panel: var(--surface);
    --paper: var(--text); ... }` alias block was a BARE `:root` selector, so every alias
    computed once against `<html>`'s own (light-theme) tokens and inherited that frozen light
    value down, instead of recomputing at `<body data-theme="dark">` the way canon's own
    tokens do. Fixed by matching canon's own selector pattern: `:root, [data-theme="dark"]{...}`.
    Same class of bug as the earlier Opus cascade fix — a real, generalisable lesson (declare
    theme-dependent aliases against the same selector list the tokens they wrap use, never bare
    `:root`). **Still open, not yet fixed or raised for a ruling:** the "Free buffer" gauge
    legend uses the same accent red as "current balance/live" and the approve button — one
    accent doing double duty (live-status AND good/free-status), which may read oddly against
    normal finance-UX convention (red = attention/negative). Flagged for Dave's eye, not
    silently changed.
  - **⚠️ Caught by Dave, not by me:** when asked directly "did you put the restyle through the
    gates or use your own inference?" — the honest answer was **inference, not gates**. No
    `_SCREEN-GATE.md` existed for this file, no validator run showed in the commit history, and
    the file wasn't even named `*.canon.html` (the default glob `_validate_screen.py` scans), so
    the pipeline would have been blind to it either way. Ran `_validate_screen.py` against it for
    real: **FAIL** on first pass — 2 hex refs (`#000`/`#FFF`, only inside explanatory CSS
    comments, reworded to "black"/"white") + 3 UNKNOWN icon paths (hand-drawn stroke arrows for
    inflow/outflow/net-movement direction, a genuine icon-source-rule violation). Fixed by
    swapping in the real library glyphs (`assets/icons/arrows-and-chevrons/arrow-up.svg` /
    `arrow-down.svg`). Re-ran: **PASS**. Lesson for next restyle: run the gate as the LAST step
    before presenting, not as an afterthought prompted by a direct question — a hand-built
    "canon-primitive" restyle is a claim the gate exists specifically to check, not something to
    self-certify.
  - **⚠️ Caught by Dave again, then verified with real numbers, not just fixed on faith:**
    Dave said "this would fail accessibility for a start" after seeing the balance figure fixed.
    Ran the `design:accessibility-review` skill + pulled canon's actual dark-theme hex values and
    computed real WCAG contrast ratios (not the shallow `_validate_screen.py` a11y check, which
    only covers reduced-motion + target-size and gave a false-confidence ✅ earlier — same shape
    of gap as the [[gate-blindspot-state-contrast]] lesson). Found genuine 1.4.3 failures, all in
    my OWN invented tint compositions (not canon's `.cn-*` patterns): rail "current balance" value
    (red text on panel) 3.23:1; gauge "free buffer" label (red text on red-tinted fill) 2.92:1 —
    worse, and even canon's real error-tint token only gets red text to 3.71:1, so red is
    structurally unfit as small/normal-text colour on any dark tint, only as a solid fill with
    reverse text (which is why the buttons pass at 5.2:1); "Scheduled" tag (info/blue text on a
    hand-mixed 12% tint) 3.67:1; scheduled-card date (info/blue on bare panel) 4.24:1, borderline-
    failing. Fixed: the two red instances now use `--paper` (white) text, keeping red as the
    accent/fill only; the two blue instances now sit on canon's REAL `--info-tint` token instead
    of a hand-mixed approximation — verified 4.92:1, passes. Also closed a real modal gap found in
    the same pass: the payroll confirmation dialog had Escape-to-close but no actual keyboard trap
    (Tab could reach the still-exposed-to-AT background) — added Tab-cycling inside the dialog and
    `aria-hidden` on the background wrap while open. Re-ran `_validate_screen.py`: **PASS**.
    **Pattern now twice-confirmed:** a hand-built "canon-primitive" restyle needs its OWN explicit
    verification pass (gate script AND a real contrast check) before presenting — passing the
    existing automated gate is necessary but not sufficient, because that gate doesn't check
    contrast on compositions that aren't `.cn-*` snippets.

- **🎯 Ingestion "done right".** Full detail + phased worklist: **`knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`** (cockroach doc — cold-start-proof, evidence-cited).
  - **Target:** every ingested entity (guideline rule · token · component · snippet · success-
    criterion) addressable in **one interlinked graph or an overlay/index layer** across the existing
    stores; token store **Sutherland-canonical** with the **147 depricate tokens retired**;
    completeness measured as **edge coverage**, not pages processed.
  - **Current vs target:** 3 siloed stores + 1 narrow graph (WCAG↔component only); guidelines 462
    rules (Tier 1 done, Tier 2 tail + 21 legacy open); tokens half-migrated.
  - **Blockers:** **Sutherland export NO LONGER a blocker** (arrived 2026-06-17; the gaps manifest is
    STALE and still says "parked" — Phase 0 fix). Remaining work is ours, not a wait.
  - **Path:** Phase 0 un-stale tracking → Phase 1 execute Sutherland token migration (rebind 147
    depricates → verify → delete; close P1/P3/P4) → Phase 2 finish guidelines capture → Phase 3 build
    the overlay/index graph (ADR-0003 "done right", audit-grade) → Phase 4 wire ingestion coverage
    into this machine as a tracked target.
  - **Phase 3 approach = the 2026-07-10 KG design direction** (see OPEN → "Unified DS knowledge-graph"
    above): overlay/property graph over the existing stores (NOT GraphRAG, NOT a monolith) · atomic-
    where-bundled rules + typed edges (rule→token/component/SC/pattern) · import ACT/axe-core for the
    SC↔rule leg, hand-curate only component↔SC · `applies_to` vs `verified_by` edge types · rides with
    the layout/library tier (R4), not standalone. Cheap-now slice: type existing edges + import ACT.

## SPIN-OFF / GENERALISABLE CANDIDATES — surface, don't bury (Dave, 2026-07-05)

*Tools/methods built here that may generalise to other projects — treat like company spin-offs.
Also the place to surface **whole new projects that emerge mid-chat**. Flag when something proves
reusable; don't force it (most stays local). Memory: `spin-off-candidates`. Revisit in seaworthiness.*

- **🌱 The state machine** (`_LIVE-STATE` + temporal decision-graph/`ADR-0007` + decision-audit
  method) — **Dave's first named candidate.** A portable "how a long-running agent project retains
  state, records supersession, and audits its own decisions" kit.
- Other candidates (unruled): decision-audit runbook + validation-state machine · the fixed/flex
  charter as a brand-true-generation governance pattern · the ingestion→overlay-KG method · the
  review-dossier language-review instrument · verification=enforcement / gate-tiering · the
  "cockroach doc" cold-start-proof pattern.
- Precedent (already ad hoc): `digital-experience-transformation`, `graphify-tool`. The ask is to
  make spin-off **intentional + surfaced**, not accidental.

- **✅ Capture ritual — STOOD UP 2026-07-05 → `knowledge/_RUNBOOK-capture-ritual.md`.** The five-step
  end-of-session sequence (refresh `_LIVE-STATE` → refresh `GOOD-MORNING` → update memory → record
  decision nodes with supersession discipline → commit+push) is now a runbook, not a hope. The
  enforcing `_capture_gate.py` is still deferred to the PM-KG MVP build (spec lives in the runbook);
  until then, the runbook itself **is** the gate — run it by hand every session.

## Entry points

`GOOD-MORNING.md` (latest handoff) → **this file** → `knowledge/README.md` (build) ·
`MEMORY.md` (memory index) · `AGENTS.md` (principles + method) ·
`knowledge/_RUNBOOK-capture-ritual.md` (end-of-session sequence, run every session).
