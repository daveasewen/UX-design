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
