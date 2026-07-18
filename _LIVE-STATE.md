# _LIVE-STATE — what's true now (cold-start spine)

*The supersession ledger for the project: what's **LIVE**, what's **DEAD** (don't build on it),
what's **OPEN**. Read this second, after `GOOD-MORNING.md`, before `knowledge/README.md`.
Per **ADR-0007**. ⚠️ **INTERIM — hand-maintained** until `_build_live_state.py` generates it from
front-matter edges + tombstones. Refresh at end of every session alongside the handoff.*

*Last refreshed: **2026-07-19 (session "Splitting type from box")**. **RULED — T-D12:** TYPE and BOX
are SEPARATE selector lists. `.t-cm-<size>` carries family/size/weight/**line-height:1** (safe
anywhere); `.t-cm-slot` carries display/align/min-height/cap-trim (**opt-in**, only where the element
already declares a flex display). Slot height travels as `--slot`, inert unless read. All three
questions ruled as recommended (Dave: *"cool lets go with all your recommendations"*).
**VERIFIED, NOT ARGUED:** 13/21 pixel-identical, **zero page-height changes**, real HSBC Univers;
6 of 8 residuals isolated as T-D10's intended weight snap via a `NO_SNAP` control, the other 2 are
accepted cap-trim (geometry probe: only `min-height` changed). **CLOSES T-D11.**
**TWO SELF-INFLICTED DEFECTS, neither caught by a gate:** a `COLLISION_HOLD` honoured in planning
was violated in the write (global `str.replace` stripped `.tag`, which shares declaration text with
`.chip`); and the slot list patched 1 of 3 `.t-cm-slot` occurrences, so a slotted selector could get
the box WITHOUT the trim. Both fixed. **DEF-006: 780 → 729**, still deliberately unwired.
**LICENCE THREAD CLOSED + REFRAMED** — see the OPEN/BLOCKING section immediately below.
**Commit `9fb1381`.***

> ⚠️ **THIS FILE IS 1044 LINES AND HAS NEVER SHRUNK.** It is the cold-start spine and it has grown
> past what a cold agent can actually read — which defeats the purpose it exists for. Consolidation
> is scoped as the **Fable session**; see `notes/_FABLE-BRIEF-consolidation.md`. **Do not add to this
> file without asking whether something can come out.**

## 🕓 OPEN — Latin Univers **WEBFONT**: waiting on brand (raised 2026-07-18, **reframed 2026-07-19**)

> **DOWNGRADED from ⛔ BLOCKING to 🕓 WAITING.** Dave, 2026-07-19: *"the license will be renewed soon,
> it may well have been already, the webfont needed Ultralight added, I think this is only procedural,
> and low risk."* **The commercial judgement is his and it is recorded as made — do not re-litigate it.**

**Split the question in two. Only one half is about risk.**

**(1) LICENCE — procedural, pending, low-risk. Owner: BRAND, chased by Dave.** The renewal is in
flight and the delta is a *weight* (**Ultralight**) being added, which implies a renewal line-item
rather than an entitlement that never existed. Stop writing "we have no licence"; write **"renewal
pending; Dave assesses the gap as procedural and low-risk."**

**(2) ASSETS — unchanged, and NOT a risk question.** Verified by inventory 2026-07-19: **zero Latin
`.woff`/`.woff2` files exist in the repo.** Five script packs present (Arabic, Japanese Tazugane,
Chinese ×2, Armenian — Th/Lt/Rg/Md/Bd each); Latin has none. **A favourable licence does not deliver
files.** Shareable real-face material stays blocked until the pack physically lands — not because it
is forbidden, but because there is nothing to embed.

**✅ DISTRIBUTION QUESTION — CLOSED, ruled "leave".** The four tracked files embedding base64 woff2
(`TYPE-SPECIMEN-2026-07-17`, `TYPE-COMPOSITES-2026-07-17`, plain + REVIEW, at `24accd0`) stay as they
are. **No `git rm --cached`, no BFG purge, no history rewrite.** Repo is private (confirmed by Dave,
upgrading it from an unauthenticated-404 inference) and Dave 2026-07-19: *"anything in the repo will
only be shared to other HSBC employees anyway"* — every recipient sits inside HSBC's own licence.
**Interim control retained:** `reviews/*CONTACT*.html` gitignored; share OUTSIDE HSBC as PDF only.

**⚠️ PROVENANCE CORRECTION.** `WebfontUserGuide-2024.pdf` is **generic Monotype usage guidance with
no entitlement schedule** (723 lines; no mention of Latin, Ultralight, or entitlements). It cannot
settle the question either way. "We hold no Latin webfont" has always rested on **absence of files**,
not on any document — I had been citing the PDF as if it were the licence record. **It is not one.**
The entitlement record sits with brand/procurement and we have never seen it.

**WHAT EXACTLY CLEARS THIS** *(a blocker must name its own clearing artefact — this one did not)*:
1. **Files land** — `HSBC_MtUnivers_Latin-*.woff` + `.woff2` in `knowledge/assets/fonts/`. This alone
   unblocks shareable real-face material.
2. **Brand confirms scope** — whether **Ultralight** is included. **Not a detail:** the script packs
   ship Th/Lt/Rg/Md/Bd ≡ 100/300/400/500/700, so an Ultralight sits BELOW Thin and is a **sixth
   weight** — a change to the canon ramp, therefore a **TYPE RULING, not an asset drop.** Expect it;
   do not discover it in a diff. (`{#type26-*}` weights rule, memory `type-body-weight-rule`.)

**⚠️ Provenance note:** I struck this blocker earlier the same day as "false", having found the *desktop*
set and not read which licence class the blocker named. Dave caught it. Full correction + the superseded
text are in `knowledge/_proforma/_TYPE-DECISIONS.md` § Blockers 1.

## LIVE — current truth (in force)

### ⭐ TYPE and BOX are SEPARATE — T-D12, RULED + VERIFIED across 21 files (2026-07-19)
- **Two lists, two questions.** `.t-cm-<size>` = TYPE (family, size, weight, **`line-height:1`**) —
  **safe to bind anywhere.** `.t-cm-slot` = BOX (`display:inline-flex`, `align-items`, `min-height`,
  cap-trim) — **opt-in**, bound ONLY where the element already declares a flex display.
- **`--slot` carries the slot height on the type composite.** A custom property is inert unless read,
  so a type-only binding has no box consequence. That is what makes the two lists independent.
- **`line-height` is TYPE, not BOX** — Component tier *is* "single-line at line-height 1". This was
  not the question the queue asked and it is the one that decided the batch: with line-height in the
  box, type-only bindings silently DROPPED the `/1` the old shorthand carried.
- **Cap-trim reaches elements that lacked it, and the shift is ACCEPTED** — refusing it would leave
  two classes of button in canon (trimmed in `Button.reference`, untrimmed in `Confirmation`).
- **The slot test stays conservative.** "Already declares flex" is the OBSERVED condition `.btn` met,
  not a theory. **Slotting anything else is a per-component decision with its own diff, never a
  mechanical sweep.** Widening it is a ruling.
- Evidence: 13/21 pixel-identical, 0 page-height changes, real HSBC Univers. Ledger:
  `_proforma/_TYPE-DECISIONS.md` **T-D12**; sheet `reviews/TYPE-BOX-SPLIT-2026-07-18.html`.
  Validation state: **unaudited** (per `_RUNBOOK-decision-audit.md` — never self-promoted).
- **METHOD, reusable:** the `NO_SNAP=1` isolation control in `apply_type_bind.py` separated diffs the
  binding CAUSED from diffs T-D10 INTENDED — turning "8 files differ" into "6 intended, 2 to rule on".
  **A diff you cannot attribute is not evidence.** Pixel count alone would have condemned a correct
  change. Reach for a control before reaching for a verdict.

### Type binding — RULED + PROVEN on one component (2026-07-18)
- **Mechanism = (d) selector-list extension, HAND-MAINTAINED.** A component binds by being appended
  to its composite's selector list in `canon/type.css`. Plain CSS: no generator, no build step, no
  markup change. `type-bindings.json` + orphan gate = an OPTIONAL later upgrade, **explicitly
  deferred — do not build**. Ledger: `_proforma/_TYPE-DECISIONS.md` T-D9.
- **`.t-cm` is variant D.** Cap-trim sits on the **ELEMENT**; the former required `.txt` child is
  **GONE**. `inline-flex` + `align-items:center` is what centres the cap box in a taller slot — an
  `inline-block` variant TOP-ALIGNS and is wrong. Observed in real HSBC Univers
  (`reviews/trimtest.html`, `outputs/trimtest2.png`). Supersedes the 07-17 composite.
- **⚠️ LOAD ORDER IS LOAD-BEARING.** `.t-cm-button` and `.btn` are both specificity 0-1-0 → source
  order decides. **`type.css` must load BEFORE component CSS.** Not yet gated.
- **Delivery = `<link>`, NOT inlining.** The portable unit is the PROJECT, not the file (Dave:
  *"the entire project must be portable… a package, pulled from a repo"*). The 49-file inline sweep
  was solving a problem that does not exist.
- **`type.css` is HAND-AUTHORED.** The "generated 2026-07-17" header was false provenance; removed.
- **Bound so far: `.btn` only**, pixel-diff verified as a no-op.
- **Unchanged from 07-17:** CSS cap-trim · 4px slot · slot min `ceil(cap + 2·descender)` snapped to
  4px · descender guard baked INTO the slot · stacks use `gap` slot-edge to slot-edge, **never
  padding**. **No `padding` property is authored anywhere.**

### RAG — amber SOLVED, background/glyph split (2026-07-18)
- **Two tokens per hue: `background` (fills) + `glyph` (icons, arrows, text).** Red/green/blue hold
  the SAME value in both roles; **only amber diverges**. Ledger: `_proforma/_RAG-DECISIONS.md`.
- **`amber/background` = `#F0B13A`** (L 0.800, C 0.147, H 79.5°) — ink on it 9.16.
- **`amber/graphic` = `#C58900`** (L 0.673) — 3.02 on white, 6.25 on `#111`. **Required by
  `{#dv-016}`** (≥3:1 series fills, blocking): the light amber is 1.90 and cannot be a chart colour.
- **Rule 1 — amber is always paired with black text. Rule 2 — amber is not a DIRECTIONAL delta
  colour**; it remains valid for status and tolerance (RAG health, watch, within-tolerance variance).
- **White is the RAG text colour universally; the dark-text variant is DROPPED** (R-D1) — amber is
  the sole exception and always was.
- **`#000000` retained in the KB as brand source of truth** (query-bot rationale); `#1A1A1A` is the
  digital black for screens; `#1D1D1D` dropped; `#333333` canon, stays.
- **Incumbent RAG values are NOT deleted** — retired into a future legacy theme. Tombstone, keep.
- **⚠️ NOT YET GATED.** Both amber rules are mechanically checkable and unenforced.

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
  validate the pro-forma contract + factory struct-mode. Memory `apollo-component-library-itinerary`. **UPDATE 07-14 eve — TRANCHE 1 DONE** (all 6 as one interactive MONOCHROME file `knowledge/_proforma/Tranche-1-interactive.html`; near-black primary, colour=meaning, real HSBC icons ENFORCED via `_check_proforma.py`; `_PROFORMA-RULES.md` living; artifact `apollo-proforma-tranche-1`). LESSON: a new surface needs its gate wired. Full: [[proforma-programme]].
  **UPDATE 2026-07-15 — library NAMED "Apollo mono" + Tranches 1–7 all built & gated.** Dave named this monochrome
  base **Apollo mono** (unbranded user-testing + Figma target), one of a THREE-library taxonomy governed by MODES:
  **Apollo mono** (here) · **Apollo UI** (new branded, varying radii) · **Apollo SC** (prior branded — "keep the ideas,
  don't copy the solutions"). **FOUNDATIONAL RULING (Dave):** *"we shouldn't hard code any styling going forward, must be
  tokenised and all the sibling libraries should be governed by modes — very flexible and future-proof."* Now enforced.
  **T6 (text entry & forms)** built + review-fixed with Dave (border-as-state-channel; uniform 51px field height every state;
  real error triangle; no size/layout jumps). **T7 (navigation)** built from a deep-research nav catalog
  (`reviews/NAV-PATTERN-CATALOG-2026-07-15.html` + artifact) — Popover/NavToggle · GlobalHeader · SideNav · MegaMenu
  (cols/featured/tabbed) · Drawer+NavAccordion; disclosure a11y spine; artifact `apollo-tranche-7-navigation`.
  **FULLY TOKENISED** (colour · motion via CSS scale tokens, JS motion removed incl. snippet canon · spacing `--space-*` ·
  border `--bw-sm/md/lg/1_5` · radius mode-token). **FOUR gates in `_build_all.py`:** universal `_validate_proforma.py` ·
  **DEF-003** `_validate_css_governed.py` (no JS motion) · **DEF-004** `_validate_no_hardcode.py` (no raw px in
  spacing/border/radius — caught real 1.5px leaks). DEF taxonomy 001 state-cluster / 002 glyph / 003 motion / 004 styling.
  **SCHEDULED TARGET (blocked on Dave's Figma):** type-token system = 3 responsive scales × 9 sizes + line-heights, 4px-grid →
  2 labelling-style sets (editorial + UI); same Figma file carries new colour tokens for all 3 modes; restore placeholder
  leading-trim (fixes off-grid 51px field). NOTED: legacy-libraries build-out. NEXT = Tranche 8 (BottomTabBar · InPageNav ·
  FooterNav · RelatedLinks · Stepper) OR type-tokens on Figma arrival. Full: [[proforma-programme]], [[nav-pattern-catalog]], [[apollo-mono]].
- **TYPE-TOKEN SYSTEM = PROMOTED TO CANON + grid enforced library-wide** (2026-07-17, Dave "crack on"). Whole
  arc landed this session: (1) **promoted** reconciled primitives → `tokens/typography.json` + composites →
  `tokens/typography-composites.json`, `type.css` settled; (2) **HSBC-general incumbent** type+spacing parked as
  sibling sets (`_typography-hsbc-general.json`, `_spacing-hsbc-general.json`) — Apollo = the proposed HSBC
  standard, governed by modes ("preserve old as legacy"); (3) **DEF-005** grid gate wired into `_build_all.py`;
  (4) **retrofit** — 230 off-grid snaps (preserve-density ties, hairlines exempt) across canon.css + 38 snippets
  + 9 tranches; spacing padding/responsive snapped; (5) **vertical-stack rule** drafted (slots already contain
  the descender → pure 4px rhythm); (6) **arrow asset RETIRED** — `padding/arrow` + `icon/arrow/font-N` were
  unused legacy fixed-px chevron; live components use em-scaled flex-centred chevron; parked + 3 metas rebound;
  (7) **DEF-005 EXPANDED** — gate now block-aware + HTML-safe, exempts hairline(1/3)/negative/square, gates **50
  files** (type.css + canon.css + snippets + tranches), all PASS. **Build green (26 steps).** Renders verified
  in-sandbox. Review sheet `reviews/GRID-RETROFIT-2026-07-17.html`. ALL rulings + WHY in
  `knowledge/_proforma/_TYPE-DECISIONS.md`. **OPEN:** webfont — Latin desktop OTF/TTF in
  `knowledge/assets/fonts/_desktop/`, product still needs the create.hsbc webfont licence renewed — **external dependency, outside Dave's control**, logged as a standing product-path blocker (not an action item).
  Historical build detail below:
- **TYPE-TOKEN SYSTEM = built, proposals await promotion** (2026-07-17). From Figma *Digital Supercharge 0.5*
  (`scale-1`, node 2320-70342) reconciled with repo `typography.json`. **Primitives** (reconciled + 4px-normalised,
  weights confirmed 250/300/350/400/500/700 from the Latin desktop instances, display sizes font-00/font-0 added —
  scale-2/3 INFERRED) → `tokens/_proposals/typography-reconciled-2026-07-17.json`. **Composites** = TWO sets
  **Editorial** (full line-height) + **Component** (cap-trim + 4px grid-slot) → `tokens/_proposals/typography-composites-2026-07-17.json`
  + working mixin `knowledge/canon/type.css`. Key mechanism: Component text is **cap-trimmed** then **seated in a
  4px grid-slot** (slot = `ceil(cap+2·descender)`→4px = line-height token AND descender-guard); metrics measured
  (cap 0.723em, USE_TYPO_METRICS off → 1.3em natural box). **Gate** `knowledge/_validate_grid.py` (4n + 2px half-step;
  1px=borders only; font-size/letter/border/radius exempt) — passes selftest + type.css. RULINGS + WHY all in
  `knowledge/_proforma/_TYPE-DECISIONS.md` (D1–D6, N1, V1, body-weight brand rule, grid subdivisions). **Naming:**
  role names + font-N alias (D1); sets = Editorial vs Component (D3, "get people off Figma onto Apollo"); highlight→
  **emphasis** (D5); `-V2` = dark-mode weight step-up (V1). **BRAND RULE:** no light/ultra on body sizes (min regular);
  see memory [[type-body-weight-rule]]. OPEN: promote proposals→canon (Dave's sign-off; canon promotion = Dave only);
  wire grid gate as DEF-005 (task #8); vertical-stack spacing rule (task #7); retrofit ~123 off-grid values in canon.css
  + 69 across tranches — fix source snippets+tokens, regenerate (task #9); investigate arrow-padding 5/6/7 asset;
  webfont: Latin desktop OTF/TTF in `knowledge/assets/fonts/_desktop/` (product still needs webfont licence renewed).
- **ATOMISE — build at the true atomic level, compose up** (RULED Dave 2026-07-14). Rolled-up
  patterns (e.g. Notifications = inline + toast + global + contextual in one molecule) are a **debt**,
  not the model; going forward build atoms → molecules → organisms per the `meta.schema` category
  ladder, exposing the atoms. Known debt: decompose the existing rolled-up molecules in a later
  refactor. Applies to all new component work.

- **Apollo product spine = "lovable on rails" · four phases** (Dave 2026-07-17, new framing — labels
  provisional, shape is the vision). Tagline **"lovable on rails"** = generative freedom bound to
  brand/a11y/governance **rails**. Four phases the final harness rolls every feature into:
  **1 · Apollo Discover** (ingest · research · analyse — KB intake; chat-to-KB bot likely here) ·
  **2 · Apollo Create** (generation, being built now; four modes: **Strict** = assembly-line "Factory
  mode" from the sponsor deck · **Creative** · **Component Dev** · **Explore** = free noodling) ·
  **3 · Apollo Craft** (review · edit · craft — the review doc + comment overlay IS this phase) ·
  **4 · Apollo Dispatch** (hand a package to engineering; may fold away if integrated rather than a
  discrete handoff — ties to Sutherland build target). Subsumes prior mode thinking: the four Create
  modes = `multi-mode-product-vision`; converge-ship vs explore-noodle = `harness-two-modes`; one
  `product-shape-flexing-engine` underneath. Memory `apollo-product-framing`. Unaudited — a framing, not a spec.
  **REFINEMENT (Dave 2026-07-17): the four Create modes = TIERED LEVELS OF ADHERENCE** to the rails
  (a11y · standards · canon components · KB guidance), guardrails **progressively removed along the tiers**
  (Strict = all gates blocking + canon-only → … → Explore = most off), with **per-tier sub-settings**. "Lovable
  on rails" = a dial, not a fixed track; it's the `fixed-flex-charter` + `register-inference-ramp` made an
  explicit per-mode governance control. **RESOLVED (Dave 2026-07-17): a11y (WCAG 2.2 AA) IS the single
  non-removable floor** — holds across every mode incl. Explore, no tier dial can drop it (per FOUNDATIONAL
  `accessibility-aspiration`); likely joined by other locked foundations (e.g. colour palette, TBD).
  **Nuance: "non-removable" = LOCKED, not HARDCODED** — an **admin access layer tunes every setting incl. the
  floor** (new product concept: an admin settings surface above the per-mode tier dials), keeping nothing truly
  hardcoded. **Name rationale: Apollo = the MOONSHOT** (after the Apollo programme) — the ambition behind the name.
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

### ✅ CLOSED 2026-07-19 — the type/box split. Ruled as **T-D12**; see LIVE above.
*(This entry was "NEXT SESSION STARTS HERE". Kept as a tombstone for one refresh so the transition is
visible, then delete it — flagged for the consolidation session.)*

### 🔴 OPEN — the binding mechanism's BLAST RADIUS has no gate (raised 2026-07-19, T-D12 §5)
**The selector-list mechanism puts bare, unscoped selectors into a globally-linked stylesheet.**
`h2`, `.label`, `.status`, `.time`, `.chip` are now global rules in `canon/type.css`, applying to
**every** snippet that links it. It holds today only because component CSS loads second and wins at
equal specificity — i.e. **load order is doing safety-critical work across ~460 selectors with no
gate on it.** The `.tag` collision is the first instance and will not be the last.
- **This does NOT reopen T-D9.** The mechanism is ruled; what is missing is its guard-rail.
- **Sequencing view (mine, for Dave):** this wants a gate **BEFORE** the remaining 690 TYPE-002 are
  bound, not after. The next batch is where the blast radius stops being tolerable.
- Candidate check: every selector appended to a composite list must be either namespaced or proven
  unique across all gated files; flag any bare element selector (`h2`) outright.

### 🟠 OPEN — the non-`/1` batch, and why DEF-006 stays unwired
**61 non-`/1` font shorthands remain in `snippets/`**; the bulk of the remaining **690 TYPE-002**
sit in the pro-forma tranches. These carry unitless line-heights of **1.1–1.6**, so binding REPLACES
them with the canon value and **things move**. That is not mechanical and needs its own reviewed
batch with the same before/after pixel discipline as T-D12.
**DEF-006 is 780 → 729 and stays UNWIRED until this lands** — wiring it earlier turns the build red
on known, unruled work, which trains everyone to ignore a red build.

### Awaiting Dave — small, no analysis needed
- **Matting rung for green + blue** — `as now` / `−15%` / `−28%` / `−40%`. Contrast is near-identical
  across steps by design, so there is **no numerical tell — do NOT guess**. Sheet:
  `reviews/RAG-MATTING-2026-07-18.html`.
- **`{#dv-017}`(a) CONTRADICTION** — permits **red/green** for delta indicators while naming
  **"RAG-style cells"** as an indicator form; RAG includes amber by definition. The rule permits a
  palette it also excludes. Surfaced by Dave's finance challenge 2026-07-18.
- **`.tag` COLLISION** — 14px in its canonical `Tags.reference`, 12px in `Account-card` and
  `List-items` where the source comment says it is *reusing that atom*. One selector cannot join two
  composites. Ruling: one atom at one size, or an explicit `.tag--sm`.
- **`.num` at 24px/400** — no Component composite exists at 24px (ramp: 12/14/16/20/32/40/52). Add a
  rung, or snap to 20 or 32.
- **Family A (reverse on near-black), 12 decls** — held at 500. To revisit, re-specimen on a FULL
  dark surface, not a chip.

### Gates owed — rules that exist but do not bite
- **Amber rules 1 + 2** (R-D3) — checkable, unbuilt.
- **type.css load order** — checkable, unbuilt.
- **DEF-006** — still not wired.
- Dark-mode green `#1AA05C` 3.37 · dark-mode red/blue as TEXT glyphs on `#111` (3.97 / 4.15).

### ⚠️ METHOD DEBT — the review overlay loses row identity
Three sheets this session needed **three different** disambiguation routes: pin POSITION (T-D10),
ARITHMETIC (R-D1), and NEITHER (RAG-MATTING — unresolvable, still open). **The overlay should
capture which row a comment is pinned to.** This is a PRODUCT fix to the overlay, not a process
workaround. Register against the review-layer-as-product-feature thread.

### ⚠️ THE PATTERN THAT COST THE MOST TIME TODAY — for the consolidation session
Three times I designed a solution to a problem the system had **already answered**: the ochre glyph
(1.4.1 waiver was canon in 5 snippets) · the 49-file inline sweep (portability was never tested) ·
"no Univers in-sandbox" (fonts have been in the repo). **Not stale facts — a stale READING of our
own rules.** `_validate_assertions.py` catches facts that flip; nothing catches a rule we forgot we
had. **Check the KB and the gates BEFORE designing.**

- **🔴 GAP FOUND (2026-07-17, measured) — the library does NOT use the canon type ramp.** Type was *promoted
  to canon* on 07-17 and the *grid* retrofit ran — but components were **never rebound to the composites**.
  The grid retrofit snapped **dimensions**; it did not change how **text** is specified. Measured today:
  **0 of 50** component files reference a `.t-cm-*` / `.t-ed-*` composite, **0** link or inline `canon/type.css`,
  and raw font declarations remain everywhere — **canon.css 113**, Tranche-8 43, Tranche-1 25, Tranche-6 23, etc.
  (Contrast: **grid IS done + enforced** — DEF-005 passes across 51 files.) The only things using canon type
  metrics today are the two reconciled candidates in `knowledge/_review/`, and even they inline the values
  rather than the classes. **THE TYPE RETROFIT (sibling to the grid retrofit) — NOT STARTED:**
  1. Components link/inline `type.css` instead of redefining fonts.
  2. Rebind every text declaration to a composite: **Component** (`.t-cm-*`, cap-trim + 4px slot) for
     single-line labels; **Editorial** (`.t-ed-*`, 4px line-heights) for wrapping prose. (Multi-line Component
     text drifts off-grid — the N1 caveat — so the single-line/wrapping split is the deciding rule.)
  3. Snap off-ramp sizes (plenty of 11/13/15/19px that isn't on the 12/14/16/20/24… ramp).
  4. Wire **`_validate_type_composites.py`** into `_build_all.py` so it's enforced like DEF-005 — Dave
     2026-07-17: *"everything we produce should use these font rules … we need to hard wire this."*
  ⚠️ **`canon.css` is GENERATED from the reviewed snippets — edit the snippets and regenerate, never hand-retype**
  (hand-retyping loses decisions). Scope ≈ the grid retrofit; needs a fresh session, not a tail-end one.
- **✅ STEP 0 DONE (2026-07-17) — icon SOURCE canvas normalised to 18×18.** RULED Dave: **normalise the source
  assets** ("the errors happened either by the author or during ingest, they should definitely be aligned") —
  i.e. option A, we own this library, not emit-time patching. **69 files** were off-canvas (35× `19×18`,
  28× `18×19`, 6× `19×19`); measured with real path bboxes (`svgelements`), not a number-scrape:
  **53 had artwork already inside 0–18 → lossless viewBox retag** (these had been rendering ~5% SMALL, since a
  19-unit canvas scale-to-fits into a square box); **16 genuinely exceeded 18 → uniform scale-to-fit wrapper**
  `<g transform="scale(k)">` (k=0.947 for the six true 19×19 — lending/-active, overdraft, pay-company,
  premier-privileges-active, sell; k≈0.994–0.999 for ten rounding-noise cases) — **the wrapper preserves the
  original path data byte-intact** for provenance/diffing. **EXCLUDED (deliberate non-square utility marks,
  left alone):** `handle.svg`, `arrow-{up,down}-low`, `arrow-{left,right}-narrow` (`8×16`/`18×9`/`18×7`).
  Library now **652 × 18×18** + those 6. Only **3 glyphs were inlined downstream** (social-linkedin,
  social-youtube-2, stamp-active) — their `<symbol viewBox>` updated in Tranche-8 + the reconciled candidate.
  **Full build green (26/26) incl. the icon gate; before/after renders identical (no clip, no distortion).**
- **🔵 SCHEDULED (Dave 2026-07-17) — ICON SCALE onto the 4px grid** (step 0 above is its prerequisite, now done).
  Type + spacing were snapped to 4px this session; **icon RENDER sizes were not**, and the grid gate can't see them: `_validate_grid.py` deliberately
  **exempts a height that equals a width** in the same rule ("intrinsic square size … governed by icon-scale,
  not layout"), so every icon box escapes DEF-005. **Measured today across `canon.css` + 38 snippets + 9
  tranches:** ~56 icon usages are already on-grid (20px ×22, 16px ×22, 24px ×8, 12px ×4) and **~50 are OFF**
  — **18px ×20**, **14px ×14**, 22px ×7, 26px ×3, 34px ×2, 11px ×2, 15px ×1, 10px ×1. Roughly half the library.
  **The work:**
  1. **Define the sanctioned icon scale** on 4px — **12 / 16 / 20 / 24 / 32 / 36 / 40 / 44** (36·40·44 added by
     Dave 2026-07-17 — 44 matches the WCAG target-size floor, so an icon can fill a full touch target) — and rule the mapping
     for each off-grid size (18→16 or 20? 14→12 or 16? 22→20 or 24? 26→24, 34→32, 11→12, 15→16, 10→12).
     Dave's call; sizes affect optical weight, so decide against renders, not on paper.
  2. **Tie icon box → the type grid-slot.** A Component label sits in a 4px slot (16px label → 20px slot);
     an icon beside it should take the SAME slot so icon+label rows land on-grid by construction. This is
     the clean rule that makes the scale self-evident rather than arbitrary.
  3. **Source-artwork caveat (found today):** the asset library is drawn on an **18-unit canvas** — 786 files
     are `18×18`, but **~71 are NON-SQUARE** (`19×18` ×35, `18×19` ×28, `19×19` ×6, plus `8×16`/`18×9`/`18×7`).
     Vector scaling to a 16/20/24 box is fine, but the non-square ones will letterbox or distort in a square
     box — need a `preserveAspectRatio` / pad-to-square ruling. (Same family of asset defects as the mislabelled
     glyphs in `knowledge/_ICON-GAPS.md`.)
  4. **Gate it (verification = enforcement):** either narrow DEF-005's square exemption for icons, or add
     **`_validate_icon_scale.py`** allowing only the sanctioned sizes, wired into `_build_all.py`.
  5. **Retrofit** the ~50 off-grid usages, then re-render to confirm no optical regressions.
  Sequenced with the other enforcement work: component index + duplicate-guard + type-composite gate
  (see the type/reuse rules). NOT started.

- **🟢 NEW RULE + backlog (2026-07-16) — component documentation is part of "done".** Every component now
  ships with a two-part doc: a reviewable **Swiss dossier** in `reviews/` + a graph-connected **KB model doc**
  in `knowledge/_proforma/` (typed `relations:` edges). Codified as **`_PROFORMA-RULES` rule 16** (FIRM going
  forward). First exemplar pair: `reviews/MASTHEAD-MODEL-2026-07-16.html` + `knowledge/_proforma/_MASTHEAD-MODEL.md`
  (the switchable-masthead model — PROPOSED, labels open, see its §06 / Open decisions). **FUTURE TASK (state
  machine, backlog — Dave "we might have to go back"):** retrofit dossier+KB-model docs for Tranches 1–7, and
  stand up the Swiss-aesthetic HTML **component catalog** ("nicer Storybook") as their shared home. Not committed
  — sequenced after current build work.
- **🟡 PARKED — round-one DataViz kit BUILT + reviewed, "good enough for now", NOT signed off (RULED Dave 2026-07-16).**
  Gate-first build complete: `_validate_dataviz.py` (9 blocking + 5 advisory, `--selftest`) wired into `_build_all.py`
  step 22; whole kit on ONE file `knowledge/_proforma/DataViz-interactive.html` (KPI · column/bar/grouped/stacked ·
  line/multi/spark · donut ×3 label variants) via generator `knowledge/_review/_gen_dataviz_charts.py`; build green
  25/25. **NINE review rounds enacted** — full ruling+WHY ledger at **`knowledge/_proforma/_DATAVIZ-DECISIONS.md`**
  (read it before touching charts). Committed `c0d8db6`, `baf1f7b`, `f10b082`, `f93c2cc`, `de8cbcb` (Dave pushes via Desktop).
  **Dave's ruling:** move on now, but this is a **REVISIT target, not DONE** — he will come back to add **more controls
  (filtering, chart titles, and other Layer-2 interaction controls)** and finish sign-off. Interactivity so far
  (theme/contrast/width-slider/table-drawer/series-toggle/tooltip/variant-tabs/marker-toggle) is verified by gate +
  `node --check` only — **never render-checked in a browser** (sandbox has no browser); needs Dave's in-browser pass.
  Staleness gate: flip this to DONE only when Dave signs off after the revisit. Prior research history below is retained.
- **🟠 OPEN (2026-07-16) — DataViz is the next big pillar (Dave's pick), in research.** Desk research DONE
  → `reviews/DATAVIZ-DESK-RESEARCH-2026-07-16.html` (+ review pair): digital + finance charting, cited; feeds a
  method dossier. KB already carries the HSBC rules (`guidelines/data-visualisation.md` + bar/pie/line companions:
  flat-fills-only/no-gradient/no-3D, ≥3:1 building blocks, palette-only, ≥2px block gap, per-type rules) and the
  **"supercharge" = supporting palette** (10 families × 5 steps, in `colour.json`; `tokens/_proposals/supporting-palette.proposals.json`).
  **Approach RECOMMENDED:** CSS-first **custom SVG + token layer** (reject canvas — can't tokenise/inspect/a11y),
  table-as-source for simple types, D3-scale/Observable-Plot for hard maths only, CSS-only motion. **RULINGS (Dave
  2026-07-16, from the dossier review):** (1) red/green gain-loss "not precious" — the never-red/green orthodoxy is
  overblown; USE it, pair with sign/arrow/position — but ⚠ this needs the HSBC KB **no-red-in-charts** rule
  ({#dv-017}) EXPLICITLY OVERRIDDEN (flagged, not yet done); (2) **texture sparingly + stylishly** — one chevron-style
  pattern max per chart, still flat; (3) **legends OK but with an alphabetic signifier** (bars A·B·C, legend shows
  colour+letter+name). **OPEN/NEXT:** method dossier · **V7 series-assignment** (which palette family/step = series-N
  per mode — unblock with real renders, respect per-mode `indicatorOK`) · **variant-complete inventory** (Dave: bar →
  butterfly/tornado/segmented/vertical-horizontal/waterfall… enumerate ALL sub-variants) · round-one kit
  (KPI stat card · line/spark · bar/column/stacked · donut). Tasks #13–16.
  **UPDATE 2026-07-16 eve — method dossier DRAFTED + V7 RENDERED, both awaiting Dave's markup.**
  (1) **Method dossier** → `reviews/DATAVIZ-METHOD-2026-07-16.html` (+ .REVIEW pair) + KB model doc
  `knowledge/_proforma/_DATAVIZ-METHOD.md` (typed relations, per rule 16): approach restated for RATIFICATION
  (semantic SVG + tokens + CSS motion + visually-hidden-table spine; canvas rejected), vocabulary model
  (family→type→variant; designers pick recipes), **variant-complete inventory (41 items, tiers R1/R2/M/X)**,
  the four rulings enacted incl. a DRAFT scoped override for gain/loss red (touches **col26-012** — the actual
  no-red-with-supporting-palette rule, NOT dv-017 as previously cited — plus the 07-14 red-once-per-screen rule:
  deltas = data semantics, not actions), gate mapping (new `_validate_dataviz.py` + indicator-contrast extension;
  gate lands WITH the first chart), round-one kit spec + build order. **8 numbered decisions in §08.**
  (2) **V7 decision sheet** → `reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html` (+ .REVIEW pair; generator
  `knowledge/_review/_gen_series_renders.py`): candidates **A** hue-spread mid-step (light=dark-families step 3,
  dark=light-families step 2; recommended) / **B** strong-step 1 / **C** mode-stable dual-legal (surfaces the
  **dv-014 ↔ col26-017 scope tension**), × both real surface tokens × 4 chart types, receipts RECOMPUTED from hex
  (all agree with proposals file); + delta options (1: RAG tokens, needs override — `rag/error/dark` IS #DB0011,
  4.02:1 = the ds-002 signature, OK for ≥3:1 indicators / 2: in-palette pair, no override). Render-verified in-sandbox
  (playwright headless-shell, memory recipe), 0 console errors; full build green after. **NOTHING PROMOTED —
  derivation-governance holds; V7 stays Dave's judgment gate.** NEXT = Dave marks up both REVIEW copies →
  enact picks (semantic-colour.json `data/series-N` + override wording into the guideline) → build round-one kit.
  **UPDATE 2026-07-16 late — Dave's markup ENACTED (sheet now REV 2) + range-mode architecture set.**
  RULED via markup (readback pending confirm): **C = DEFAULT** series assignment (mode-stable; resolves dv-014
  scope = ACROSS the theme switch; col26-017 divergence recorded consciously) · **A = HIGH-CONTRAST ALTERNATE**
  via a per-chart switch (`data-contrast` / `data-range` — token rebind, no chart forks) · B retired to the record.
  **Deltas REBUILT** per markup: rev-1 options (RAG reuse / raw palette pairs) retired; new values DERIVED from
  palette anchors (most-red burnt-orange/1 + most-green forest-green/1 + blue neutral midnight + amber sun-yellow),
  hue pulled to convention, lightness SOLVED against real surfaces; three options **D1 quiet / D2 convention-forward
  (rec) / D3 CVD-split** await pick; amber asymmetric (3:1 light graphic-grade / 6.5:1 dark). **Ranges direction
  (Dave, follow-ups):** we can CREATE ranges (colour-theory harmonies + "scientific" criteria), categorised by
  INTENT (harmony-led · contrast-led first two); range selection = a future **edit-mode harness dial**, so ranges
  LIVE IN TOKENS — enacted as generated holding pen `tokens/_proposals/dataviz-ranges.proposals.json` (range/default=C,
  range/high-contrast=A, 5 generated suggestions tagged by intent, delta d1–d3; statuses picked-pending-confirm /
  proposed; generator emits it alongside the sheet). Sheet §06 = the suggestion strips. Method dossier §05 synced.
  REMAINING PICKS: confirm C/A readback · delta D1/D2/D3 · promote-or-park §06 ranges. Then round-one kit.
  **UPDATE 2026-07-16 night — second markup batch (7 items) + the vibrating-boundaries article ENACTED (sheet REV 3).**
  🟢 **NEW RULE (Dave, via Tuts+ "Vibrating boundaries" article): avoid vibrating boundaries** — adjacent
  saturated near-complementary equal-value pairs shimmer; a11y hazard (astigmatism, sensory processing; equal-value
  pairs also vanish for CVD). QUANTIFIED: all 3 legs = risk (pair value-ratio <1.25 + hue-sep ≥135° + both HSL
  sats ≥0.5; hue leg set at 135° because Dave OBSERVED the dance on a 146° pair). Enacted as: vibration receipts on
  every candidate/delta/range (sheet + tokens `$vibration`) · advisory adjacent-pair check specced for
  `_validate_dataviz.py` (dossier §06 row; skip pairs separated by a dv-004 gap — the gap IS the classic defence) ·
  dossier ruling §04.5 (Apollo-added rule, not ingested-HSBC). **DELTAS: D2 = PICKED** (Dave), dark red/green
  "danced" → value-split BOTH pairs (receipts caught light mode had the same triple; light loss deepened 6.0:1,
  dark gain 6.2:1/loss 4.4:1 + dark red desat 0.60) — all pairs now ≤ moderate; **D1 kept-option** (same split);
  D3 retired-record (mechanism absorbed into the fix). **RANGES: palette-native ONLY** (Dave: "we can't invent
  anything — only safe in the RAG" = deltas are the sole derived-colour zone): all suggestion ranges rebuilt from
  existing palette primitives ($token paths carried), WIDENED across family step-ramps 1→5 (also the vibration
  defence); CVD-diverging range RETIRED (existing guideline rules = the mitigation). Sheet/tokens/dossier all
  regenerated; build green. REMAINING: confirm the rev-3 readback · promote-or-park ranges · confirm vibration
  thresholds (1.25/135°/0.5) as the gate's advisory start. Then round-one kit.
  **✅ UPDATE 2026-07-16 close — V7 CONFIRMED + ENACTED (Dave: "happy with my initial selection with your
  adjustments").** PROMOTED into `semantic-colour.json`: **`data/series/1–5`** (C, mode-stable, same hex both
  modes, $alias→supporting primitives) · **`data/series-high-contrast/1–5`** (A, per-chart rebind) ·
  **`data/delta/{gain,loss,neutral,warning}`** (D2, value-split pairs; derived — no primitive alias, $note carries
  anchors). **Override + new rule RECORDED in the guidelines as `{#dv-019}`** (`data-visualisation.md`, cross-ref
  annotation at col26-012 in `colour-standards-2026.md`): scoped gain/loss exception (delta indicators only, never
  series fills; doesn't count against red-once-per-screen) + the vibrating-boundaries rule (Apollo-added,
  advisory-derivable) — the rules-index gate rejected `{#dv-019-apollo}` (ID grammar = must end in the number),
  renamed to `{#dv-019}`, now indexed. Statuses flipped to `confirmed-2026-07-16` in
  `dataviz-ranges.proposals.json` + the sheet; `supporting-palette.proposals.json` $README marked V7 RESOLVED
  (semantic side = receipts now). Suggestion ranges stay `proposed`. Vibration thresholds = adopted as the
  advisory start. Full `_build_all.py` GREEN. **NEXT = round-one kit** (KPI card → bar/column → line → donut)
  against the live tokens, `_validate_dataviz.py` (incl. vibration check) landing WITH the first chart; dossier
  §08 items 1/5/6/7/8 (approach ratify, tiers, maths helper, chevron timing, gate plan) still open for markup.
  **✅ UPDATE 2026-07-16 final — METHOD DOSSIER RATIFIED (Dave's markup, 4 items).** §01 approach RATIFIED
  (semantic SVG + tokens + CSS motion + hidden-table spine; canvas rejected — now the build method) · §05
  confirmed · §06 gate plan APPROVED · §07 kit spec APPROVED (settles chevron-in-R1). Tiers (§03 boundaries) +
  maths helper (hand-rolled first) stand as DEFAULTS, unmarked — movable before they bite. Dossier §08 updated
  to resolved-status; KB model doc status updated. **DataViz has NO open blockers: next session = build the
  round-one kit** (KPI card → bar/column → line → donut, gate-first). Committed `966f0d1` (tokens batch) —
  this ratification batch needs its own commit.
- **🔵 FUTURE SIDEQUEST (2026-07-16, Dave) — knowledge graph of ALL our research.** Build a KG over the
  research corpus we keep generating (dataviz desk-research + method, masthead/nav pattern research, the model
  dossiers, framework scans, etc.) so findings are queryable + reusable, not stranded in one-off dossiers.
  **Harvest later** — for now, just capture research as we go in a KG-friendly way. Folds into the existing
  PM/DS knowledge-graph direction (ADR-0007 temporal decision-graph; typed edges; `_GRAPH-REPORT`/graphify) —
  the research corpus becomes another node/edge source alongside decisions + components. First inputs already on
  disk: `reviews/DATAVIZ-DESK-RESEARCH-2026-07-16.html`, `reviews/NAV-PATTERN-CATALOG-2026-07-15.html`,
  `reviews/MASTHEAD-MODEL-2026-07-16.html` + their KB docs. Memory `pm-knowledge-graph-direction` / `ds-knowledge-graph-revisit`.
- **🔵 FUTURE SIDEQUEST (2026-07-16, Dave) — Swiss HTML viewer for this ledger.** Build a well-structured
  Swiss-styled HTML view of `_LIVE-STATE.md` so Dave can inspect it (and ideally **edit / add** entries) rather
  than reading raw markdown. Editable = needs write-back (bigger). Same house style as the pattern catalog /
  masthead dossier. Not started — parked as a state-machine future task. Pairs with the PM-KG direction
  (a rendered face over the ledger). Also: TLS-CA playwright render recipe now captured in memory
  `sandbox-html-rendering` (full chrome renders in-sandbox again with local-extracted libs).
- **🟢 BUILT + LIVE (2026-07-16) — unified Masthead shipped, all gates green.**
  `knowledge/_proforma/Masthead-interactive.html`: ONE `.masthead` driven by `data-mode`
  (`minimal/exposed/exposed-mega/trigger`) + modifiers (`data-prominence primary|index`, `data-affordance
  burger|menu-search`, `data-search/-account on|off`) + a **switch row** that reconfigures the one live
  instance across the **5 recipes** (`App-minimal · L1 exposed · L1 + mega · Trigger mega · Dashboard-index`).
  **Folds in + SUPERSEDES the T7 `gheader` + `mm-masthead` demos** (they can be retired from Tranche-7).
  CSS-only motion (mega grid-reveal), search-finesse working (bar search icon hides when the panel carries
  search), priority+ → hamburger→modal-drawer responsive, disclosure a11y (aria-expanded/controls, ink
  underbar current, Esc-return, focus-trapped drawer). **All 4 pro-forma gates PASS + full `_build_all.py`
  (24 steps) green**; render-verified all 5 recipes + responsive, 0 console errors. Labels as signed off
  (D1 kept provisional · D2 Shell + optional footer → T8 · D3 recipe names). Docs: model dossier
  `reviews/MASTHEAD-MODEL-2026-07-16.html` + KB `_MASTHEAD-MODEL.md` (rule 16 pair); component review copy
  `knowledge/_review/Masthead-interactive-REVIEW.html`. **REVIEW ROUND 1 APPLIED (Dave, 2026-07-16):**
  dropped App-minimal (responsive covers it; app builds get their own components later) + the axis controls;
  merged Dashboard-index → **Trigger mega** (now 3 recipes: L1 exposed · L1 + mega · Trigger mega); trigger +
  account moved to the RIGHT; bar search + narrow hamburger now collapse into ONE drawn **combined
  menu-search glyph** (`i-menu-search`, flagged `provisional`/`bespoke`, logged to `_ICON-GAPS.md` — replace
  with a real HSBC asset later); removed the "All products" button (exposed-mega L1 links open the mega
  themselves); frame is bottom-border-only + account dropdown no longer clipped. All 4 gates + full
  `_build_all.py` still green; re-rendered all 3 recipes + narrow, 0 errors. **REVIEW ROUND 2 APPLIED
  (Dave, 2026-07-16):** (a) **bow+arrow brand mark** (`i-brand-apollo`, provisional/bespoke — Apollo the archer);
  (b) desktop trigger shows **separate menu + search** icons that **combine into the one menu-search glyph on
  mobile**; (c) **NEW drill-down side-nav drawer variant** (`.drawer.drilldown` — horizontal push nav, each
  submenu a full panel with title + back button, reflecting the mega IA; modal focus-trap scoped to the active
  level via `inert`; CSS-only slide) opened by the mobile combined glyph — the simple `.navacc` accordion
  variant is RETAINED in Tranche 7 (Dave: keep both); (d) masthead **underline** moved to `.masthead-bar` so it
  shows in every mode. 2 provisional glyphs logged to `_ICON-GAPS.md`. All 4 gates + full board green; rendered
  desktop/narrow/drill-down push+back, 0 errors.
  **REVIEW COMPLETE (Dave, 2026-07-16 — "done at last") after ~6 rounds.** Final state: **3 recipes**
  (App-minimal + the axis controls dropped; Dashboard-index merged into Trigger mega); **brand = extreme
  crescent** `i-brand-apollo` (provisional; picked from a 2-option render — bow-arrow & moon-craters rejected);
  desktop = separate menu+search, **combine into one menu-search glyph on mobile → drill-down drawer**; search
  finesse tied to **mega-open state** (bar search present, goes TRANSPARENT — not display:none, so no jump —
  when the mega is invoked); mega search = white bg + clear-on-active; masthead **underbar on `.masthead-bar`**;
  nav labels **wrapped in `<span>`** so leading-trim applies inside the flex `<a>` (memory
  `leading-trim-label-decision` gotcha #4); **all-caps purged** (`.dd-group-h`); brand icon↔wordmark gap 4px.
  Provisional icons `i-brand-apollo` (crescent) + `i-menu-search` await real assets (`_ICON-GAPS.md`).
  **NEXT** = Tranche 8 (+ Shell/footer template tier) or the type-token system on Figma arrival.
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

- **🎯 TARGET — chat-to-the-KB bot in the final system** (Dave 2026-07-17, quick capture). Ship a
  conversational agent, part of the delivered product, that users (designers/devs/stakeholders) can
  **chat to the design-system knowledge base** — ask what a token/component/rule is, why a decision was
  made, how to use something — answered from the Apollo KB (canon · criteria · rulings · the decision
  graph), not general knowledge. *Why:* the KB is already the source of truth; a retrieval-grounded chat
  surface makes it self-serve and is a natural sibling to gates-as-a-service (same KB, read side vs
  enforce side). *Open/unspecified:* retrieval grounding + provenance/citations, scope (read-only Q&A
  vs can-it-generate), surface (in-catalog / Slack / IDE), guardrails against invented answers. Idea
  recorded today, not a spec. Memory `chat-to-kb-bot`. Unaudited.


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

- **🌱 NEW 2026-07-18 — the FONT AUDIT instrument** (`reviews/gen_univers_dossier.py` + the
  fontTools measurement passes behind it). Given any two font files it answers, with numbers rather
  than opinion: *is this face tight or loose relative to its own stroke weight?* (sidebearing ÷ stem,
  normalised to 1000 UPM, comparable across designs) · *how does spacing behave across the weight
  range?* · *is our commissioned cut actually the same as the stock family?* (glyph-by-glyph advance,
  LSB/RSB, and kerning-pair comparison) · *what are the real vertical metrics and therefore the
  natural line box?*
  **Why it generalises:** every brand with a commissioned type cut has the "is ours the same as
  stock, and where does published guidance stop applying?" question, and almost nobody can answer it.
  Here it settled in ten minutes a question that had been open for weeks, and **relocated a defect
  from HSBC to the foundry** (ds-004). It also produced the session's most load-bearing measurement —
  the SB/stem collapse across weights — which no amount of reading would have surfaced.
  **Status:** unruled candidate. Currently embedded in a dossier generator; would need extracting.

- **🌱 NEW 2026-07-18 — REAL-FONT EMBEDDING for review sheets** (`embed_fonts()` in
  `gen_tracking_contact_sheet.py`). Inlines the licensed face as base64 woff2 (~300KB for five
  weights) so a specimen renders in the actual brand type in any browser, with no install and no
  broken relative paths when the file moves.
  **Why it matters beyond convenience:** it **retired a caveat that had been attached to every
  specimen sheet in this project** — "sandbox has no Univers, judge on your screen". Type decisions
  judged in a fallback face are not type decisions. **Candidate to fold into `_make_review.py`** so
  every future sheet gets it automatically rather than by remembering.
  **Status:** unruled candidate; working, and the obvious next step is promotion into the review
  pipeline.

- **✅ Capture ritual — STOOD UP 2026-07-05 → `knowledge/_RUNBOOK-capture-ritual.md`.** The five-step
  end-of-session sequence (refresh `_LIVE-STATE` → refresh `GOOD-MORNING` → update memory → record
  decision nodes with supersession discipline → commit+push) is now a runbook, not a hope. The
  enforcing `_capture_gate.py` is still deferred to the PM-KG MVP build (spec lives in the runbook);
  until then, the runbook itself **is** the gate — run it by hand every session.

## Entry points

`GOOD-MORNING.md` (latest handoff) → **this file** → `knowledge/README.md` (build) ·
`MEMORY.md` (memory index) · `AGENTS.md` (principles + method) ·
`knowledge/_RUNBOOK-capture-ritual.md` (end-of-session sequence, run every session).
