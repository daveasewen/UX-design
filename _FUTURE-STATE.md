# _FUTURE-STATE — the forward ledger

> STANDING: side-quests, feature ideas, and resurrection candidates — the future half of the state
> machine. Read alongside `_LIVE-STATE.md` (what's true now) and `_DECISION-HISTORY/` (how we got here).

*Created 2026-07-18 at Dave's ask during the consolidation review: "how do we store all the ideas for
side-quests, features and ideas that I want to hold onto, so we have a future-state-machine." Division
of labour: **`_LIVE-STATE` keeps in-flight TARGETS (ruled 2026-07-05) and the SPIN-OFF register (ruled
"surface, don't bury")** — this file holds everything forward-looking that is NOT in flight. An idea
graduates OUT of here into `_LIVE-STATE` OPEN/TARGET when work starts. Refresh with the capture ritual.*

**Entry format:** what · why it's held · what it feeds (Apollo phase/mode) · source/provenance pointer ·
status (`idea` / `parked` / `resurrection-candidate` / `graduated→LIVE`).

## Resurrection candidates — experiments to re-evaluate once the factory is built

- **The restyle saga + generate-then-normalise lineage** — the two-pass "generate free → constrain +
  verify" experiments and the ungoverned diagnostic pieces. *Why held:* Dave 2026-07-18: "definitely
  going to revisit all the old ideas and experiments… this one might fit into two of the four modes."
  *Feeds:* **Apollo Create — Creative and Explore modes.** *Source:*
  `_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md` + `knowledge/_fitness-test/register-spread-2026-07-05*/`
  + memory `generation-mechanism-ideas`. *Status:* resurrection-candidate.
- **The §9 tuning questions** (rule-crafting, inference tiering, the three-arm experiment) — parked by
  the 07-10 ruling until the substrate is rich enough. *Why held:* "I can tune a machine if it doesn't
  have all the parts" — the factory comes first, the tuning returns. *Feeds:* Create mode dials /
  register ramp. *Source:* `_DECISION-HISTORY/2026-07-07-s9-root-cause-and-ruling.md` +
  `knowledge/_FINDINGS-s9-session-2026-07-07.md`. *Status:* resurrection-candidate.
- **Masthead design revisit** — shipped as an **MLP** (Dave, 2026-07-18); iteration expected across
  much of what we produce. *Feeds:* Craft phase. *Source:*
  `_DECISION-HISTORY/2026-07-16-masthead-rounds.md`. *Status:* parked.
- **Iteration-machine front-end mock** — vision facade, proves alignment only. *Feeds:* the eventual
  Apollo interface/harness. *Source:* `notes/_VISION-iteration-machine_2026-07-03.html` (carries the
  old looks-language — reconcile before reuse, see `_LIVE-STATE` propagation gap). *Status:* parked.
- **Portfolio-interactions craft pass** — the wow pass on the Reorder testbed; don't gold-plate before
  the ask. *Feeds:* Craft. *Source:* memory `portfolio-interactions-invite`. *Status:* idea.

## Apollo Mono button-colour finessing — parked 2026-07-20 (Dave)

Raised by Dave right after the `button/*` snippet rebind landed (build green 35/35). Both are
COLOUR-only finessing, deliberately parked so we could carry on to component build-out — the rebind's
token wiring is settled; these are value/perception tweaks on top.

- **Primary hover ≈ secondary default (collision).** Dave: *"hover-primary is very similar to the
  secondary button, might be a little confusing."* Confirmed numerically: primary hover flattens to
  ~`#5F5F5F` (stored equiv `#626262`) and **secondary default is `#626262`** — essentially the same
  grey. Two different buttons in two different states read identically. *Fix space:* re-tune the primary
  hover opacity/colour, or shift the secondary default step, so the emphasis hierarchy stays legible.
  *Feeds:* Craft / Apollo Mono. *Status:* parked.
- **"Done" success state — RESOLVED 2026-07-20 (B-D6).** Was on the Legacy teal `#00847F`; now the R-D14
  green fill `rag/success-background` `#5DAC7B`/`#43AD6F` + black label (`text/on-success`). *Status:* done.

## Legacy-colour leakage — gate live, RAG green set to COMPLETE (2026-07-20)

The teal-in-Mono leak (B-D6/R-D17) is now guarded by **`_validate_legacy_leak.py`** (build-blocking; seeded
with the ruled teal `#00847F`). It caught **7** teal-binding surfaces; Button is fixed, the other seven are
**waived with provenance** pending the work below.

- **Complete the R-D14 green set, then rebind the 7 — DONE 2026-07-20 (R-D18).** Dave ruled the green set
  on the live tuner (glyph dark `#4A9568`, tints `#DCEDE3`/`#12291D`, bare role rebased). All seven rebound,
  all gate waivers cleared, teal fully evicted from Mono. *Status:* done.
- **Seed the gate with error/warning/info once ruled — roles now RULED (R-D20, 2026-07-21).** The three sets
  are complete + Mono; 6 Mono snippets swept, Notifications waived (Legacy ref). *Still open:* seed the Legacy
  error/amber/navy hexes into `LEGACY_ONLY_HEXES` (needs a Notifications waiver in the leak gate, since it holds
  them legitimately), and flip `_validate_theme_provenance.py` from advisory to blocking — both gated on the
  broader foreign-hex cleanup (58 hexes / 67 files). *Status:* idea.

## ★ Decision-graph — typed edges over the record corpus (ADR-0007's unbuilt half) — tasked to Fable (2026-07-21, Dave)

*Why held:* today's icon-011↔R-D6↔R-D3 reconciliation was done by hand because decision records cross-reference
in **prose**, not queryable edges — so recall = keyword search (consult) and reconciliation = manual archaeology.
Desk research confirmed this is **already decided** (ADR-0007 temporal decision-graph; slice 1 / staleness gate
built) — the missing half is the edge convention + generator + conflict gate. *What it feeds:* Apollo PM layer /
the `_STATE-MACHINE-TARGET` context machine. *The slice:* (1) typed-edge front-matter on ~35 decision nodes
(4 ledgers + 11 ADRs + REVIEW rules): `refines · supersedes · subsumes · bounds · conflicts-with · verified-by`
+ `status` + `validation` (unaudited→vouched); (2) generator → LIVE/DEAD/OPEN ledger + **reconciliation view**
(auto-surface any conflicts-with edge lacking a resolution) + per-node "what-touches-this" map; (3) **conflict
gate** — A bounds/conflicts B with no recorded resolution → build flags it (icon-011 vs R-D6 would have lit up).
*Rejected alternatives:* replicate-across-records (rot engine — denormalise only in generated views); graph DB
(tool-temptation — text-based KG gets 80%, per ADR-0007 + the July-2026 external scan). *Routing:* **Fable, fresh
cold session** (big/high-stakes/hands-off); guardrails — conflicts it surfaces are **queued for Dave's ruling,
not auto-resolved** (promotion is Dave's); open sub-call (author all edges in one Fable sweep vs stop at spec+gate
and hand edge-authoring to Sonnet) decided *after* the audit. *Source:* `_DECISION-HISTORY/2026-07-21-rag-completion-and-decision-graph.md`;
ADR-0007 + `notes/_STATE-MACHINE-TARGET.md`. *Status:* **tasked — next session.**

## Token schema: explicit nullable placeholder slots for anticipated flex (2026-07-20, Dave)

Dave's direction: *"we always have to think about max flexibility and save all possible values for the
architecture… the value can be a value or null, like placeholders"* — refined to *"probably not every
possible parameter but the ones we need to flex; I envisage a style builder in the future."* So: reserve
**explicit, nullable** slots on tokens for the dimensions we anticipate flexing (per-mode already; per-theme,
per-state mechanism, opacity), where `null` = *"slot declared, value not yet set"* — NOT a blanket dense
schema. *Why it fits us:* the teal leak was a **silently missing** dark green; an explicit `dark: null`
placeholder would make that hole machine-visible and let a gate fail any *live-component-bound* token whose
mode-slot is null. Needs: a clear null semantic (undecided vs intentionally-inherit) + that "no null under a
live binding" gate. *Feeds:* the **style-builder interface** (ADR-0009 — where a user configures mechanism +
values per state within the AA guarantee); pairs with `$extensions.apollo.state`. *Status:* **written up → `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md`**
(direction accepted; null-gate + slot rollout staged, pilot = the RAG green set). *Provenance:* this session.

## Side-quests (captured in `_LIVE-STATE` 07-16, now homed here)

- **Research knowledge-graph** — KG over the research corpus (dataviz desk research, nav catalog,
  masthead model, dossiers) so findings are queryable, not stranded. Harvest later; capture
  KG-friendly as we go. *Feeds:* Discover phase / ADR-0007 direction. *Status:* parked.
- **Swiss HTML viewer for the state ledgers** — a rendered, ideally editable face over
  `_LIVE-STATE`/this file, house style. Pairs with the PM-KG direction. *Status:* parked.
- **DataViz method → colleague presentation** — Dave 2026-07-18: "much of it deserves to be a
  presentation to colleagues." Material: the method dossier + V7 sheet + the vibration rule story.
  *Feeds:* Dispatch/advocacy. *Source:* `_DECISION-HISTORY/2026-07-16-dataviz-v7-arc.md`. *Status:* idea.
- **★ EXPERIMENT — isoluminant sweep across the WHOLE base Apollo palette, across the bands** — Dave,
  2026-07-19, during the RAG-colours review: *"run this across the whole base Apollo colour palette,
  across the bands."* Take the isoluminant band method built for RAG red/green/blue (match OKLCh **L**
  across hues, hue held, chroma capped to gamut, WCAG contrast measured vs white / black / `#1A1A1A`)
  and apply it to **every hue family × step** in `knowledge/tokens/colour.json` — re-cut each colour to
  sit at each band's shared lightness, to see how the full palette behaves under intensity-matching.
  **⚠️ Second axis to measure (Dave surfaced it in the same review): HALATION / bloom.** Intensity-match
  is one dimension; edge-extremity is another — *"thin lines and colour dance, thicker ones bloom… that's
  the halation effect."* Bright/high-step colours on the dark ground bloom (fills) or shimmer (thin
  strokes/text). The sweep should carry a bloom/edge-extremity read alongside contrast, tying to the
  existing edge-extremity advisory gate + the digital-black rationale (`color/black` `$note`, memory
  `attribute-the-diff` / `dark-rag-token-gaps`). *Why held:* Dave said "schedule after this RAG stuff" —
  runs once the RAG bands are ruled (R-D6). *Feeds:* Discover/colour-foundations + the DataViz/RAG
  palette work. *Source:* `reviews/_rag_colours_calc.py` (the sweep engine) + `reviews/RAG-COLOURS-2026-07-19-v1`
  review comments. *Status:* idea — queued next after RAG.

## Spin-outs (public-facing, beyond the internal engine)

- **★ APOLLO LABS — a public a11y / colour-science microtool ("Ally")** — Dave, 2026-07-19, riding off
  the isoluminant + halation work: *"we might just be on the edge of a really cool a11y tool here… spin
  out Apollo Labs as a side project for public consumption, good promotional material for HSBC."* The
  idea: a small public web tool that runs the palette analysis live — paste/import a palette → isoluminant
  band re-cut (match OKLCh L across hues, for CATEGORICAL palettes) **+** **salience-RAMP ordering** (loudness
  descends with hierarchy, for STATUS palettes — Dave 2026-07-19: *"this is good for colour palettes"*, the ramp
  reframe ENRICHES Labs, doesn't retire it) **+** halation / edge-extremity read (bloom on fills, shimmer on thin
  strokes) **+** WCAG contrast per ground. A demonstrable, sharable artefact of serious accessibility
  craft. *Why it matters:* doubles as **HSBC promotional material** (shows the bank leading on digital
  accessibility) and as an external face for the Apollo method. *Feeds:* the **accessibility aspiration**
  (most digitally accessible bank — memory `accessibility-aspiration`, ADR-0004) + Dispatch/advocacy +
  the spin-off-candidates thread (memory `spin-off-candidates`, `capability-gap-and-obsolescence`).
  *Engine already half-built:* `reviews/_rag_colours_calc.py` (isoluminant sweep) — the [[isoluminant sweep
  experiment]] above is the internal precursor; Apollo Labs is its public form. *Guardrail:* portability +
  no licensed-font / brand-confidential leakage before any public release (ties `univers-webfont-blocker`).
  *Status:* idea — spin-out candidate; surfaced mid-RAG, do not gold-plate before the RAG bands land.
  - **★ THE TWO-MODE OKLCh TUNER is the Labs UI prototype (2026-07-19).** Built to settle the RAG light fills:
    `reviews/RAG-LIGHT-FILLS-2026-07-19-v7` — wide saturation + fine lightness sliders **per hue, per mode**, hue
    held, live hex + WCAG contrast + **a ramp-order guard that reds when the hierarchy breaks**, each mode judged
    against its own ground. Dave: *"give me a saturation slider, make it wide so i can fine tune"* → *"i could do
    this for days."* This is exactly Labs' interaction model (paste palette → tune → live a11y read). Also a
    **Layer-2 in-browser control** for the design-time loop generally ([[dataviz-pillar-progress]]). Lesson banked:
    past ~2 colour round-trips, give the eye a live control instead of another static version. Port the OKLCh↔hex +
    contrast + ramp-guard JS from that file as the Labs seed.

## Type / font procurement targets

- **★ Variable Univers cut — target a ~440–460 weight rung** — Dave, 2026-07-19, in the RAG weight rig:
  *"shame there wasn't a weight in between."* The licensed cut is five STATIC weights (100/300/400/500/700 —
  no 600, no 450) and there is no variable-webfont licence, so the 400↔500 gap can't be bridged now. If a
  variable Univers is ever procured, **~450** is the value the halation weight-rule wants for the mid case.
  *Feeds:* the dark-mode weight ruling (R-D7) + brand font procurement. *Ties:* `univers-webfont-blocker`.
  *Status:* idea — needs licence, not ours to force.
- **★ Dual-observer calibration principle (astigmatic vs corrected)** — Dave, 2026-07-19: *"mixed weight
  might be better for me but weird for normally sighted."* Optimising to the most sensitive eye can diverge
  from the typical viewer. The principle: **serve the sensitive observer without breaking the typical one —
  and flag where they diverge.** Directly shapes **Apollo Labs** (report BOTH observers, mark the gap) and
  the weight ruling (polarity as hard token vs soft guideline). *Feeds:* accessibility aspiration + Apollo
  Labs. *Source:* `reviews/RAG-COLOURS-2026-07-19-v4` §W3. *Status:* principle — apply going forward.

## Feature ideas (product, not yet specced)

- **★ Narrative dossiers as a NODE-SET in the decision graph** — Dave, 2026-07-19, right after making the
  dossier a closing-ritual step (1b): *"it might have to be wired into the KB or the state manager or a
  separate graph or something, not sure but it's some kind of set of nodes for sure."* The dossiers
  (`_DECISION-HISTORY/*.md`) are the **why/how layer**: the ledgers/ADRs hold the WHAT (ruling + pin =
  "what" nodes); the dossier holds the reasoning ARC that connects them (why/how = the edges + rationale
  nodes). **Mechanism OPEN** — wire into the KB, the state-manager, or a separate graph; not yet decided.
  Natural fit with **ADR-0007 temporal decision-graph** (memory `pm-knowledge-graph-direction`), the
  **research-KG** side-quest above, and the **graphify** tool (memory `graphify-tool`); the `_capture_gate.py`
  MVP is where the parsing machinery would live. *Feeds:* Discover / PM-KG. *Status:* idea — node-shaped,
  mechanism TBD; harvest dossiers KG-friendly as we write them so the later wiring is cheap.


- **Tiered access to canon commits** — DS-admin → domain-admin → standard; sandbox open to all,
  commits tiered (Dave, 07-05; captured in the derivation-governance amend thread). *Feeds:*
  governance layer. *Status:* idea — set the goal first, the access model falls out.
- **Admin settings surface above the per-mode tier dials** — "non-removable = locked, not hardcoded"
  (Dave, 07-17). *Feeds:* the harness. *Status:* idea.
- **Review-overlay upgrades as product** — row-identity capture (the method debt), image paste,
  dictation, export. *Feeds:* Craft phase — the overlay IS the product surface. *Status:* idea,
  method-debt half already logged in `_LIVE-STATE` OPEN.
  - **NEW (Dave, 2026-07-19): bake the template controls into the overlay** — every review must carry a
    **light/dark toggle** and a **responsive-width slider** by default. Applied by hand in
    `reviews/SMALL-PICKS-DESK-2026-07-19.html` this session; the durable fix is to add both to
    `_review/_review-overlay.html` so `_make_review.py` injects them everywhere (theme toggle needs a
    body-level `.dark`/`data-theme` convention docs opt into). *Status:* idea → do before the next batch of reviews.
  - **★ PRINCIPLE (Dave, 2026-07-20): every review carries a DECISION CONTROL per open choice — the reviewer
    EDITS the choice in place, not a question round-trip.** Dave: *"add a selector and any other controls so I
    can edit the choices rather than us going back and forward, add this as a principle for all review."* So a
    review sheet is a **live editor**: each open question becomes a control (segmented selector / slider / toggle);
    the live specimen, the resolved-token table and the contrast readout all recompute as the control moves; an
    **export block** emits the settled values for the agent to read straight off (no AskUserQuestion loop). This is
    the review-sheet expression of the **μX / in-context edit-mode controls** concept below — the "edit designs" file
    — and generalises [[feedback-live-controller]] from "how-much" feel-dials to *all* open review choices. Controls
    are bounded by the rules (e.g. an "Elevate" hover option is shown **disabled** with the `webf-011` reason, so the
    sheet teaches the constraint while offering the choice). Reference implementation: **`reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v2.html`**
    (segmented selectors for ground/hover/pressed/label + opacity slider + live token table + export). The comment
    overlay stays for anything the controls don't cover. *Feeds:* Craft — the review overlay as product surface.
    *Status:* principle set → fold the generic control-injection into `_make_review.py` / the overlay when the next
    review batch lands; the per-choice control list derives from the decision, the same way the edit-mode inspector
    derives from `<name>.meta.json`.
- **Countdown numeral snap-slider prototype** — a continuous size input (dial 48–200px) that snaps the
  dial to the **4px grid** and the numeral to the nearest **type-ramp rung** (16/20/24/32/40/52). Working
  prototype in `reviews/SMALL-PICKS-DESK-2026-07-19.html` §1 (comment 3). *Why held:* Dave "might be
  interesting to prototype" — generalises to a **responsive-on-grid component** pattern (size once, stay
  on-grid + on-scale at every viewport). *Feeds:* Create/Craft — responsive token binding. *Status:* prototype built, idea for generalisation.
- **RAG colours — settle once and for all (dedicated review)** — Dave 2026-07-19: "we need to settle the
  RAG colours once and for all… a separate review." Ruled values exist (R-D1/R-D3/R-D4 role pairs) but
  three things are OPEN: dark-mode **green** has no ruled value (incumbent #1AA05C fails white text 3.37),
  dark **red/blue as glyph-on-text** fail 4.5 (pass 1.4.11 icons), and the **manifestation** (cell / pill /
  dot / bar) is undecided — the source of the dv-017 confusion. *Feeds:* the RAG token promotion +
  component rebind (after the blast-radius gate). *Source:* `knowledge/_proforma/_RAG-DECISIONS.md`
  R-D1..R-D4 "Still open". *Status:* queued — next review deliverable.
- **Edge-triage interface (Dave, 2026-07-19: "chat might not be the best ux")** — a small purpose-built UI to work
  the compliance graph's **27 unverified `verified_by` edges**, one SC at a time: show the claim (`applies_to`), the
  available axe-core rule (13 are "easy wins"), a verdict (wire a check / already covered by a bespoke gate / bespoke
  needed / n-a), and mark state — persisted back to the graph. The task is per-item, stateful and visual, which is
  exactly what chat is bad at. **This is a sibling of the μX concept** (proximate, task-specific controls; interface >
  chat for repetitive triage) and the natural step-2 after the KG **diagram** (`reviews/KG-COMPLIANCE-DIAGRAM-2026-07-19-v1`,
  built this session — see the gap) → the interface acts on it. *Feeds:* the harness + compliance moat. *Model:* Opus to
  design + decide per-SC; delegate the mechanical check-wiring down; a batched "verify all 27" hands-off pass could be a
  Fable job later (per `MODEL-ROUTING.md` — Fable = big high-trust-at-scale, not iterative triage). *Status:* idea → prototype next if Dave wants.
- **In-context edit-mode controls (Dave's "μX" concept)** — the harness edit mode (post-generation) surfaces a
  component's controls **proximate to the component itself**, as a floating overlay docked to the selected
  component's state — **only** the controls that component exposes, **no sidebar unless absolutely needed**. Dave
  2026-07-19: *"when I select the component very specific controls are surfaced under the actual component selected
  state… the parameters you can change are proximate to the component you are editing."* The panel carries a **grab
  bar** (drag to reposition — the checkered strip in his sketch). This is the real home of the **snap-slider** idea
  above (the review-doc slider was a proxy) and of every per-component control set. *Feeds:* **Apollo Create/Craft —
  the harness interface** (the eventual front-end, cf. iteration-machine mock). *Source:* Dave's sketch +
  message 2026-07-19; prototype at `reviews/EDIT-MODE-UX-PROTOTYPE-2026-07-19-v2.html`. *Status:* prototype built, develop later.
  - **rev 2 (Dave, 2026-07-19): the component is movable too — TWO grab bars.** One grab bar moves the component,
    one moves its controls. Crucially: **no absolute positioning — movement snaps to DOM containers** (the component
    reorders between slots in a layout stack), and **arrow keys ↑ ↓ move it in the stack**. The inspector snaps to a
    dock (below / beside the component) and travels with it. Dave: *"I'd like to be able to move the component too…
    No absolute positioning it should snap to the doms containers and we could use the arrow keys to move it in a
    stack."* Kinship with the **Reorder** component ([[portfolio-interactions-invite]]) — the stack-reorder mechanics transfer.
  - **UNIVERSAL (Dave, 2026-07-19): every component gets this kind of control set** — not just the countdown. In edit
    mode, selecting *any* component surfaces its own proximate controls + the two grab bars (move component in the
    stack · move the controls). The per-component control set is **derived from the component's meta** — its `props` /
    `variants` / sizes ARE the controls (e.g. Button → variant/size/label/icon/state; Tag → variant/size/dismissible;
    Countdown → style/size/max-time). So `components/<name>.meta.json` becomes the source of truth for the edit-mode
    inspector, the same way it already drives the review-spec spread ([[feedback-review-live-variant-spread]]). The
    shared machinery (grab bars, stack reorder, arrow-key move, dock-snap, 4px/ramp snapping) is component-agnostic;
    only the control list changes per meta. *Status:* principle set — build the generic inspector against the meta when the harness UI is specced.
  - **TIERED to the strict↔creative register (Dave, 2026-07-19): the controls exposed depend on the tier.** The several
    tiers that run between **strict** and **creative** each reveal a **different level of controls** — and *only* the
    controls that tier permits. At the **most open extreme, there are essentially no structured controls — just a prompt
    box** for freeform edits; the **tiers below progressively reveal** specific controls (e.g. "just the colour palette"),
    exposing only what's available at that level. Dave: *"at the extreme level there will be no controls really, although
    [there] is a prompt box so you can make edits… in the tiers below it'll reveal say just the colour palette, but only
    the controls that are available to those levels will be exposed."* So the inspector's control set = **(component meta:
    what's possible) ∩ (register tier: what's permitted)** — and at the free end that intersection collapses to the prompt
    box. This is the [[product-shape-flexing-engine]] / [[register-inference-ramp]] governance made visible in the UI: the
    same dials that constrain generation constrain which knobs the user sees. *Feeds:* [[multi-mode-product-vision]] —
    strict / creative / component-dev / explore. **Direction CONFIRMED (Dave, 2026-07-19):** the prompt-only extreme is
    the **most creative / open** end; moving toward strict progressively reveals more structured, permitted controls.
    *Status:* principle captured + confirmed.

- **★ Style-builder interface (Dave, 2026-07-20)** — a UI where a user configures **per-state styling**
  for a component: for each interaction state (default / hover / pressed / disabled) pick the **render
  mechanism** — `colour`, `opacity`, or **both** (Dave: *"we still allow the user to select either or
  both"*) — and the values, all **within the AA guarantee** (the builder only offers passing selections;
  the Mono primary editor already demonstrates this — disabled failing ramp steps + a contrast-clamped
  opacity dial). This is the harness-side home of **ADR-0009** (state styling: colour = universal
  substrate, opacity = optional operational layer). It's a specialisation of the **μX / in-context
  edit-mode inspector** above — the per-state control set derives from the token skeleton
  (`$extensions.apollo.state`) the same way the inspector derives from `<name>.meta.json`; and it inherits
  the **live-controls-in-reviews** discipline ([[feedback-live-controller]]). A fully chromatic mode
  (red default / blue hover / green active) is just an override set the builder edits. Reference editors:
  `reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v4.html` (opacity+colour+AA) and the v5 mechanism-switch
  sheet. *Feeds:* Craft / the harness; the four-theme model (R-D15). *Status:* principle set + ADR-0009
  accepted → build the generic per-state builder when the harness UI is specced; migrate opacity to a
  first-class number token then.
  **→ Widened to a THEME GENERATOR (Dave, 2026-07-21 evening, Phase-0 session):** *"ultimately we will
  build a theme generator from this, maximum flexibility."* The builder's output IS an override set
  (`tokens/themes/*.overrides.json`) — themes are data, the cascade generator renders them, so the
  generator UI = dials over the flex-slot schema. Consequence already enacted: **radius became a semantic
  TIER** (default + control/surface/indicator roles, alias-fallback chain, `layout.json`) because "one
  radius can't be universal — cards differ from buttons"; every future flex dimension should land as
  role-granular slots with a base fallback for the same reason. The alias-aware resolution in
  `gen_theme_cascade.py` (override the base → every role follows; dial a role → it wins) is the
  generator's core resolution semantic, already live.

- ~~**★ Tiered flex at the COMPONENT-TYPE level — ARCHITECTURE SESSION QUEUED**~~ **GRADUATED
  2026-07-21 (same day, late night #3) → RULED as ADR-0013** — component-type tier carries shared
  VALUES and shared RULES (generated partials); one registry; mechanism lands before Phase-2.
  Original record kept below for the audit trail. *(Dave, 2026-07-21 late
  evening; recorded deliberately WITHOUT exploration, his instruction: "lets not explore now but we
  need to record this and explore later").* The same flexibility the semantic radius tier gives
  (default → role) will be needed **per component TYPE** as well: *"I could imagine that segmented
  controls share the same radius"* — i.e. a type-level grouping (e.g. all segmented controls) sitting
  in the **component token tier**, between the semantic role and the individual component binding, so
  a theme (or the generator) can dial a component FAMILY without touching either the global role or
  each component. His framing, verbatim anchors: **"this will be the same for borders and other
  parameters"** (the pattern generalises across flex dimensions — radius, border, and beyond, so the
  eventual shape is *tiered application in the component token level* as a general schema, not a
  radius feature); **"mono doesn't really need this flexibility, but others might, and the generator
  will"** (Mono stays simple — the tier exists for other themes and ABOVE ALL as generator dials; do
  not complicate Mono's own store to serve it). **The semantic roles as built are FINE ("these are
  fine semantically")** — the component-type tier slots UNDER them, it does not replace them.
  *Open architecture questions for that session:* where type-groups live (token schema? meta?
  a `component-type` axis in the 3-tier stack?); fallback order (component → type-group → semantic
  role → default); how the cascade generator + manifests express type membership; interaction with
  ADR-0010 nullable slots + the token-tier gate. *Status:* **GRADUATED — ruled 2026-07-21 late
  night #3 as ADR-0013**; the open questions above are answered there (registry
  `knowledge/component-types.json` · fallback component → type-group → semantic role → default ·
  ratchet-style gate + selftests). Build = the queued clean-room session per ADR-0013 Consequences.

- **Blast-radius gate v2 — cascade-aware.** T-D13's gate matches selectors structurally
  (class/element presence per file) and gates on the file *set*, so a same-count file *swap* inside
  an acknowledged radius passes, and it doesn't reason about real cascade/specificity. The rigorous
  version parses each file's own CSS and detects genuine size/weight COLLISIONS (the `.tag` 14-vs-12
  case) rather than proxying via file membership. *Feeds:* the type-binding guard-rail. *Status:*
  idea — promote once the v1 has bedded in (cf. consult tool's fuzzy→rigorous path).

- ~~**Harmonise specimen-chrome section labels onto `.spec-h`.**~~ **GRADUATED 2026-07-18** — Dave
  ruled full-strength, no muting (opacity dropped); all 9 files now 12px/opacity-1. See T-D13.
- **Reference files don't uniformly `<link>` canon/type.css.** Found during the harmonisation: only
  5 of the touched specimens link the canon sheet; 4 (Avatar, Links, Selection-controls, Tags) are
  self-contained and can't consume canon classes without re-introducing global blast radius. A
  cold-blooded pass could give every reference file a consistent canon link + local override
  discipline. *Feeds:* specimen-doc consistency. *Status:* idea — not urgent; the specimens render
  correctly as-is.

## Standing register elsewhere (pointers, not copies)

- **In-flight targets** — gates-as-a-service · chat-to-KB bot · ingestion done-right: `_LIVE-STATE.md`
  → PLANNED / TARGET STATES.
- **Spin-off / generalisable candidates** — state machine kit · font-audit instrument · real-font
  embedding · cockroach-doc pattern: `_LIVE-STATE.md` → SPIN-OFF section (ruled home).
- **Fable-session candidates** — `notes/_FABLE-BRIEF-consolidation.md` §7 (gate-glob audit, decision
  audit runs, KB structure).

- **★ SPINE COMPACTION — cold-start context bloat (Dave, 2026-07-21 late night #3: "we need to solve
  the bloat of all the context loading up each session").** Measured: orientation costs ~70k (~35% of
  the window) before any work — ~35-40k is the fixed Cowork baseline (bear it), but ~25k is
  `_LIVE-STATE.md` alone (~45k tokens, 633 lines, 8+ PRIOR deltas that never roll off and are mostly
  DUPLICATED in `_DECISION-HISTORY` already). Fix, two parts: **(1) delta retention rule** — LATEST +
  ≤2 priors stay in-file; older deltas relocate to `_DECISION-HISTORY` at capture time (mostly
  deletion; the History pointers already exist) — add to `_RUNBOOK-capture-ritual.md` step 1 + the
  `_capture_gate.py` spec; **(2) cold-read discipline** — a fresh session reads LATEST delta + OPEN
  section only, full file on demand (inscribe in GOOD-MORNING's read-order line). Claws back
  ~15-20k/session. Mechanical, Sonnet-able — fold into the ruling-batch window's enact-queue or run
  as a chore. Related: `memory-compaction-mechanics` (same pattern, repo-side); MEMORY.md index
  (~6k auto-load) is due its own densify pass under the adversarial-densify gate.
