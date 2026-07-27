# Good morning, Dave ☕

> **RENAME THE WRAPPED CHAT →** `Apollo — "maybe we are checking the wrong thing": Dave found that the hit-area MECHANISM switches off the hit-area RULE — 7 of 67 snippets measured, gate green · INSTRUMENT FIT is a third axis above ADR-0016 · the trigger should be ADOPTION-TIME · pre-flight now has three terms · 58/58 · 🟡 Amber ~58%`
> **TITLE THE NEXT CHAT →** `Apollo — instrument fit at corpus scale: tag all 465 rules with the instrument their property needs, then rank every gate that is weaker than its rule. Dave has FIVE open calls waiting in §DO-FIRST — read them before building`
> *(Titles are LABELS — role comes from Dave's opener line. The wave = the parallel model: Opus conducts, workers per lane, DIVVY in §DO-FIRST. Gauge bands: Green<45 / Amber 45–60 / Red≥60.)*


> ## ★ LATEST — 2026-07-27 (Mon **later morning #3**, OPUS solo self-conducting, effort MAX — ★ **KG FORCING-FUNCTION, EXPLORATION BEAT 1: Dave reframed it TWICE and both reframes beat all four held angles** · ★ **ds-015 — `aid-009` EXEMPTS every component that adopts the hit-area mechanism: 7 of 67 snippets are actually measured and the gate reports "0 failures"** · **PRE-FLIGHT now has THREE terms** · build **58/58 GREEN** · 🟡 AMBER ~58%, **nothing built by design**): **He asked me to explore, not build. So the session's output is two findings and one sentence of his that outranks both.**
> - **★ INSTRUMENT FIT IS A THIRD AXIS — and the held angle (1) would have MISSED it.** Angle (1) is *compare what a rule SAYS against what its gate DEMANDS*. `aid-009` says *"a minimum 44×44px target area"*; the gate calls its check *"target size"* — **the vocabulary MATCHES. The narrowing is in the INSTRUMENT, not the words.** A static regex sees a *declared box*; the rule is about a *target*, and the two decouple the moment the property is carried by a mechanism (expander · token · transform) — at which point **the gate goes QUIET, not RED.** ⇒ Ask of every rule: **"what property does this name, and can this gate's instrument observe it at all?"** (static parse → DOM → render+hit-test → eye). ⇒ **This sits ON TOP of ADR-0016:** PROVEN/CLAIMED/UNPROVEN ask *is there a check and can it fail*; this asks *is it looking at the right thing* — **a check can be PROVEN and still measure a proxy that doesn't track its rule.**
> - **★ ds-015 — DOING THE RIGHT THING IS WHAT MAKES YOU INVISIBLE.** `_validate_a11y.py` doesn't mis-measure the `::before` expander, it **`continue`s** — deferring to a "render axis" that **does not exist**. **MEASURED: 67 snippets · 1,869 selectors skipped by the `CTRL` vocabulary · 14 eligible · 7 exempted · 7 measured.** 64 of 67 snippets use `::before`. **The diamond fails three ways at once** (out of `CTRL` scope · expander is `min-width:var(--hit,44px)` vs a literal-`px` regex · `::before`→exempt) — and its real defect is a **transform**, which **no static box measurement can see in principle.** ⚠ **This proves the CHECK is blind, NOT that the components fail.**
> - **★ DAVE'S SECOND REFRAME, and it is the best angle on the whole idea.** *"we are relying too much on my memory here, the hit mechanism should have triggered something that cascaded this elsewhere."* Adoption = a LOCAL CSS decision with a GLOBAL governance consequence, and **nothing carried it.** ⇒ **The trigger should be ADOPTION-TIME, not sweep-time.** Cheapest cut: make claiming the exemption **name the rule it exempts from**, and let the register harvest it — **an exemption that must declare itself is one you can count.**
> - **⚠ THE CONSULT'S OWN INSTRUMENT IS GUESSING (bite-tested, two defects).** `rulings (5/5 shown)` is **shown/CAP not shown/total** (`:200` truncates, `:217` counts the truncated list) — true totals **28 · 38 · 54**, agent sees **17–22%**, and **BLOCKING truncates too (5 of 16)**. And `enforcement_for_rule()` decides gated-ness by **keyword overlap**, never opening the gate: **54 BLOCKING rules · 25 claimed gated · 10 named in no `.py` at all.** ⚠ That proves **unverified**, not unenforced. Its docstring is candid — **it's a good hint; the defect only bites when Dave's proposal promotes the hint to an authority.**
> - **★ PRE-FLIGHT NOW HAS THREE TERMS** (Dave: *"it self consumes tockens too"* + *"encode a pre-flight mechanism rather than loosing it in this chat"*). Already-inscribed rule NOT re-litigated; what was missing is the **meta-cost** ⇒ **"A pre-flight estimate that does not include the wrap is not a pre-flight estimate" — `fill + job + WRAP (~5%)`, always three terms.** Reserve the wrap BEFORE the job. Evidence: last session priced its render job right (53%, held), ran **the ritual unpriced**, 58→63. **Applied to itself: the instrument-tagging build was CUT, not started.**
> - **⚠ THE HANDOFF'S OWN PROSE WAS STALE, caught in two minutes.** Banner said register **4/52 of 76**; generated file reads **4/54 of 78** (DV-D14+D15 harvested). **The RED ~63% stamp told the next reader to re-verify the prose. It worked — keep stamping.** Also re-verified, not inherited: **no chat-rename tool exists.**
>
> ## ★ PRIOR — 2026-07-27 (Mon **later morning #2**, OPUS solo self-conducting, effort MAX — ★ **ds-014 calls (a)+(b) RULED BY DAVE, ENACTED, PROVEN BY RENDER** · ★ **dv-004's GATE HAD NARROWED ITS OWN RULE** · **`dv-vocab` NEW BLOCKING — unknown chart types can no longer skip in silence** · build **58/58 GREEN** · register **PROVEN 3→4** · 🟡 AMBER ~58% wrap): **Dave declined my recommendation and asked why I had made it. Answering that took one grep and cost me the argument — then found a defect bigger than the chart.**
> - **★ DV-D14 — GEOMETRY, not a stroke, and Dave was right on the evidence.** I recommended the donut's 2px `stroke="var(--page)"`. He said: *"I prefer the geometry the border will obscure gridlines, may I know why you recommend borders?"* **`cb5` carries 5 full-width `.dv-grid` lines behind the columns; the donut carries NONE.** An SVG stroke straddles its path — 2px puts 1px OUTSIDE each rect, painting over every gridline down both sides of all 4 columns. ⇒ **A surface-coloured stroke only simulates separation when the thing behind it IS the surface.** Enacted **variant A, both ends pinned**; accepted cost, stated before it landed: **segments understate 2.0–2.6%**, worst on the shortest column.
> - **★ THE FINDING THAT OUTRANKS THE CHART.** dv-004's text is **mechanism-NEUTRAL** — *"minimum 2px separation between colour blocks"*. Its gate demanded *"a surface-coloured stroke >=2px"*. **So a chart satisfying dv-004 by real geometry would have FAILED — and an agent reading the gate to learn what compliance looks like gets the WRONG ANSWER.** The gate was not merely failing to catch my error; **it was the source of it.** Now accepts either mechanism; unmeasurable geometry still demands the stroke (fails safe).
> - **★ DAVE NAMED THE CLASS HIMSELF — and it is FLOATED, not ruled.** *"we may create something that will force decisions to check that KG… the KG is a valuable resource and shouldn't be ignored, thats what it is there for."* Held in `_FUTURE-STATE.md` with four angles; sharpest is **a check comparing what a rule SAYS against what its gate DEMANDS** — the exact mirror of ADR-0016. ⚠ **Do NOT build ahead of the exploration session he asked for.** Caution recorded: the consult prints `rulings (5/5 shown, --all for more)` — **it TRUNCATES**, so a forcing function built on it is a CLAIMED gate with extra steps.
> - **★ DV-D15 — `data/text/on-series` MINTED (his promotion).** Keys had declared `var(--page)`: white today **only because of where the neutral ramp sits — a coincidence, not an intent**. New role → `color/grey/white`, pinned BOTH modes, modelled on `rag/text/on-dark`; **deliberately NO alpha channel** (DV-D07 computes contrast from the composite). **type26-013 does NOT collide** — checked, not assumed: its white-only clause is specific to RED grounds.
> - **★ THE VOCABULARY HAD FORKED — fixed structurally.** Corpus carries **both `stacked` and `stacked-column`, both `grouped` and `grouped-column`**, plus `scatter`. Enumerating three strings would have guaranteed a repeat ⇒ **`DTYPE_CANON` normalises once at read time** + **`dv-vocab` FAILS THE BUILD on any unknown dtype**. Scope-blindness audit: **3 blind values → "none detected"**. **Selftest WIRED into the build** — it existed and ran only by hand, which is exactly why nothing ever proved dv-004 could fail. **9 new bites**, one reproducing the ds-014 figure verbatim.
> - **⚠ A THIRD SILENT-FALLBACK — and it landed AFTER the build went green.** Token minted, generated into `canon.css`, **58/58 — and the keys still rendered BLACK at 3.99:1.** The snippet carries a LOCAL MIRROR of the token list for standalone preview and never declared the new var; **`fill:var(--undefined)` falls back to the SVG initial value, black, silently.** Three instances, three mechanisms: **ds-010** (author CSS beat `fill=`) · **ds-013** (404 stylesheet) · **this**. **Through-line: a lookup that misses and reports nothing — and in all three the MARKUP IS CORRECT, so no static gate reaches it.**
> - **★ PROVEN BY RENDER — `_verify_dv_stacked_enactment.py` (NEW, the P2 proof).** Licensed cut, **snippet AND showroom pane, 1180 AND 760, all four agreeing**: separation **2.00px** on all 8 boundaries · keys white **5.26 / 5.04 / 4.61:1** vs AA 4.5. ⚠ **The prior handoff predicted "≈5:1". MEASURED worst is 4.61:1** (series-3, margin **0.11**) ⇒ **series-3 cannot be lightened without breaking AA.**
> - **⚠ THE PROBE MADE THE ERROR IT WAS WRITTEN TO DETECT — third session running.** It reported *"no stacked-column figure"* for the showroom; the honest reading was **"I queried the top document and the panes are `srcdoc` iframes"**, not "the showroom is broken". Last session: `querySelector('svg')` → the toolbar copy icon. **Assume your probe is wrong in the direction that reads as green.**
> - **🟡 AMBER ~58% — and the PRE-FLIGHT rule worked.** Priced the render job before starting it (*"fill ~38% + ~15% = ~53% Amber"*) and it held. Wrapped on Dave's word rather than starting the remaining 52 proofs hot.
>
> *(Compaction 2c — keep ★ LATEST + 1 PRIOR, roll the rest. Older banners (the 07-22→24 chart-wave + ADR arc, the 07-25 AM v4 + midday→PM v5 + PM Memento-efficiency + PM#2 memory/routing-governor banners) are in `_GM-ARCHIVE.md` (Batches 1–6), verbatim, newest-first; durable narrative in `_DECISION-HISTORY/` + `notes/`.)*

---

*Briefing — refreshed 2026-07-27 ~10:30 BST (date from `date`), session "the instrument cannot see
the property — KG exploration beat 1 + ds-015" (Opus 5 solo self-conducting, effort MAX).
§A = orientation · §B = session · §C = queue.*

## ⬛ DO THIS FIRST

> **✅ CLOSED, do not re-open.** ds-014 calls (a)(b)(c) — RULED, ENACTED, RENDER-PROVEN. The legend wave,
> ds-013, ADR-0016 P1/P3-advisory all stay closed. **Nothing here is owed twice.**
>
> **★★★ FIVE CALLS ARE DAVE'S, and they gate the next build. Put them to him BEFORE starting.**
> All five came out of exploration beat 1 (`_FUTURE-STATE.md` § *forcing the KG into the decision loop*
> → **Exploration beat 1**; evidence in `knowledge/_DS-IMPROVEMENTS.md` **ds-015**):
> 1. Does **INSTRUMENT FIT** join the enactment register as a **third axis**, or stand as its own check?
> 2. Is the trigger **ADOPTION-TIME** or sweep-time? *(His idea; the adoption-time shape is the strongest
>    thing anyone has proposed for the forcing function — an exemption that must name the rule it exempts
>    from is an exemption you can count.)*
> 3. Run the **465-rule instrument-tagging pass**? Mechanical, ranks the whole corpus. **NOT started —
>    deliberately, it is a build and the window was capped.** This is the natural DO-FIRST once he rules.
> 4. **Fix or REMOVE the consult's enforcement column.** A wrong `gated by` is worse than no column. The
>    `5/5 shown` denominator is a separate, trivial fix — **do that one regardless.**
> 5. **`CTRL` in `_validate_a11y.py` is an UNSWEPT VOCABULARY.** `dv-vocab` closed this class for dataviz
>    only. 1,869 selectors currently skip. **Same pattern, already proven, applies directly.**
>
> **★★★ IF HE RULES "GO" ON #3 — the method is now demonstrated THREE times.** ADR-0016 P2 exemplars:
> `knowledge/_sweep_type_enactment.py` (corpus sweep) · `knowledge/_verify_dv_stacked_enactment.py`
> (**the better model** — ruled value vs RENDERED value across snippet × showroom × two widths).
> ⚠ **Every proof ships with a bite proving the proof can FAIL.** Non-negotiable; it has caught a real
> defect **five sessions running.**
> **Register reads PROVEN 4 · CLAIMED 20 · UNPROVEN 54 of 78** *(re-read the generated file, do not trust
> this line — it moved twice today as rulings were harvested).* **Target CLAIMED first** — an UNPROVEN row
> is honest about being unchecked; a CLAIMED row lies.
>
> **★★ STILL OWED, unchanged and NOT superseded:**
> **(i) The showroom type sweep + the 49-pane eyeball** — `_sweep_type_enactment.py` ran once: **800
> composite-bound elements, 22 deviations in 27 panes**, pattern is **WEIGHT not size**
> (`knowledge/_type-sweep-2026-07-27.json`). ⚠ Needs `--allow-file-access-from-files` or it reads ZERO and
> reports a cheerful "0 deviations". **Fold into the register as a P2 proof, don't re-run as a one-off.**
> **(ii) §C·2's RULING BATCH (15 + 17–22)** — unmoved for days, gates §C·1(c). **Fable is the model.**
> **(iii) The hit-area rule + gate** — read `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`
> FIRST. ⚠ **This is no longer a backlog item: ds-015 proves it is the NAMED RECEIVER for an exemption
> that is already shipping in 7 components.** The diamond's counter-rotation is the live case — a
> markup-driven gate must understand transforms, and a static one cannot.
> **(iv) Radius/corner tuner (§C·1d)** — v1+v2 BUILT + render-verified; owed = TWEAKS + ruling the numbers
> with Dave ("return soon, don't let me forget"). **Do NOT rebuild from scratch.**
> **(v) `showroom/chart-bar.html` cb5 rendered but UNSEEN by Dave** — 2.0–2.6% segment understatement,
> ink→white key flip, and **series-3 sits at 4.61:1, 0.11 over AA** (constrains any re-tune of that hue).
> **(vi) ds-014 (d) — donut cluster alignment, PARKED on his ruling** (`.dv-donut-row` is `flex-start`;
> −114px at 600 → −534px at 1440). Logged not fixed, deliberately — rule it where he can see it live.
> *(Carried up by the 2c EXIT CHECK so banner compaction can't lose it.)*
>
> **MODEL + EFFORT (Dave ruled 2026-07-26, still current):** conductor = **Opus 5, effort MAX** ·
> mechanical lanes = **Sonnet** · **Fable reserved** for open-judgment (the ruling batch · the hit-area
> gate). P2 is **script-then-judge**: any model writes a proof; **every deviation it finds is Dave's call.**
>
> **⚠ THE PRE-FLIGHT RULE CHANGED TODAY — read it before pricing anything.** `_RUNBOOK-context-gauge.md`:
> **"A pre-flight estimate that does not include the wrap is not a pre-flight estimate."**
> `fill + job + WRAP (~5%) = projected band` — **always three terms.** At Amber the honest question is never
> *"can I fit this job?"* but ***"can I fit this job AND the ritual?"*** Instruments (task list, consult,
> gauge check, ritual) are **not free** — but **never economise on READING the band table**; that omission
> has produced a wrong band twice and costs a `grep`.
>
> **⚠ THE LESSON THIS SESSION EARNED: the recommendation went through the CONSULT first, unprompted, and
> that is the whole remedy from this morning's arc working.** Cheap, and it is what stopped a second wrong
> recommendation. *(Full arc: `_DECISION-HISTORY/2026-07-27-the-instrument-cannot-see-the-property.md`.)*
>
> *Standing: every handoff carries both names (top) + a DIVVY PLAN. Known potholes all still true: the
> installer's non-zero exit is HOST-VALIDATION not download refusal (**check the cache, proceed**) ·
> `/tmp` NOT writable (use the outputs mount) · FONTCONFIG two-alias block required · **render the SNIPPET
> for canon truth and the SHOWROOM PAGE for what Dave looks at**, and the showroom's panes are `srcdoc`
> IFRAMES — query `page.frames`, not the top document. **Assume your probe is wrong in the direction that
> reads as green** (four sessions running).*

*Read: **§A Orientation** (skip if you're in context) → **§B This session** → **§C Queue**.
Then `_LIVE-STATE.md` → the decision files it points to.*

---

# §A · ORIENTATION — the whole project in one page

> **Why this file is called GOOD-MORNING** *(Dave's framing — keep it, it explains the architecture)*
> **Memento.** Leonard has anterograde amnesia: every morning he reconstitutes himself from a record he
> built when he still remembered — Polaroids for working state, **tattoos for the facts he cannot afford
> to lose**. That is this project's operating model, not a metaphor for it. A session starts with no
> memory and rebuilds from artefacts.
>
> **The trust hierarchy is the tattoo/Polaroid distinction:** repo rules + runbooks + ledgers = tattoos
> (durable, survive any single rewrite) · `GOOD-MORNING` + `_LIVE-STATE` = Polaroids (working state,
> rewritten often) · the chat = gone by morning. **Never let a durable rule live only on a Polaroid.**
> *(Live example, 2026-07-22: this file said the tabs ruling was "NOT yet inscribed" — the ledger already
> carried R-D23 AND R-D24. The ledger was right. Read the ledger.)*
>
> **The real danger is not forgetting — it is confident false inscription.** Records carry provenance
> and confidence, not just content. Corrections get inscribed as loudly as the original claim. **Mark
> what was OBSERVED versus what was INFERRED.** The ritual stamps dates from `date`, never from belief.
> *(2026-07-22 afternoon instance: B-D7 was ruled in TWO beats — "shared 4%", reversed within the hour
> to pixel-true. BOTH are in the ledger, so the reversal can never read as agent drift.)*
>
> **The SECOND failure mode costs more: a stale READING of our own rules.** ⇒ **Before designing anything,
> CONSULT: `python3 knowledge/_consult.py "<what you're about to design>"`** (rules · rulings · assertions ·
> gates + where each bites). Runbook: `knowledge/_RUNBOOK-consult.md`. *(ds-009 CLOSED 2026-07-22: the
> corpus is now DISCOVERED — every `_proforma/_*-DECISIONS.md` indexes or the build fails.)*

> **STANDING SECTION — carry it into every handoff, from 2026-07-17 on.** At Dave's request:
> *"orientate a new starter — wider context helps."* New-starter style: assume the reader has no context.
> **Update it when the shape of the project changes, not every session — but never drop it, and never
> shorten it to a label.** *(Also step 2 of `_RUNBOOK-capture-ritual.md`; reachability-gated by
> `_validate_standing_instructions.py`.)*

## What Apollo is
A **governed design-system engine** for agentic UI generation. The bet: *generation is a commodity* — the value
is the layer around any generator. Two principles run through everything:
- **Retrieval, not recall.** Brand values are retrieved from token stores, so generated work can't drift off-brand.
  **Since ADR-0013 (built 2026-07-22) retrieval reaches RULES too:** organisms consume atoms' rule-blocks
  as generated partials — never re-type a sub-atom.
- **Verification = enforcement.** Judgment is encoded as **blocking gates**; "done" is withheld until they pass.
  If a rule isn't gated, assume it will be broken.

Tagline: **"lovable on rails."** Four phases: **Discover** → **Create** (what's being built now) → **Craft**
(the review-overlay docs ARE this) → **Dispatch**.

## ★ ONE token store · ONE baseline library · FOUR themes (R-D15 → ADR-0011 → ADR-0014 → ★ ADR-0013)
*Themes are **override sets at the semantic tier**; since ADR-0014 they carry **their own neutral primitive
ramps** through the **neutral DNA tier** (semantic roles alias `color/neutral/1–15`, never `color/mono/*`
directly; indices are SEMANTIC POSITIONS — SC remaps its anchor). **State mechanism is a THEME PROPERTY**
(registry `stateMechanism` + blocking snap gate). **★ Since ADR-0013, MOTION is a theme dial too (B-D7):**
`motion/press/{travel,darken}` — Mono carries the movement (pixel-true 2px), **Console inherits it**,
**Legacy + Supercharge zero it** (colour-only state feedback); tuning = a token edit, zero JS.
**Sibling pairs:** {Mono, Console} share neutrals/opacity/status/dataviz — Console FENCED (colour;
motion is inherited-not-fenced, flag if it should join); {Legacy, Supercharge} = structural siblings.*
The four themes (Dave's canonical order):
- **Apollo Legacy** — faithful reproduction of the existing HSBC system: brand red `#DB0011`, teals,
  `color/grey/*`. **AA-EXEMPT as-built (R-D24)**; explicit per-path overrides, no DNA tier, **no press movement**.
- **★ Apollo Mono** — the baseline we build NOW. "Very mono": colour ONLY in RAG status + dataviz.
  Neutral scale = `color/mono/1–15`; only red `#B92F1E` (status/RAG/dataviz). Carries the B-D7 press physics.
- **Apollo Console** — branded HSBC library. **LOCKED ≡ Mono** on neutrals/opacity/status/dataviz (fence);
  inherits Mono's motion; live divergence = rounded corners (radius overrides, values provisional).
- **Apollo Supercharge** — brand-uplift. **OWN warm ramp** `color/warm/1–15` (OBSERVED, Figma pull);
  states = COLOUR; **no press movement**; dark mode = provisional-agent, awaiting Dave.

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores — the retrieval source
    colour.json       primitives: mono/1-15 · neutral/1-15 (DNA tier) · warm/1-15 (SC) · grey/* (Legacy)
    semantic-colour.json  roles alias color/neutral/* + rag/* + component tiers + $extensions.apollo.state
    motion.json       durations · easings · ★ press/{travel,darken} (B-D7 — the theme-dialable physics)
    themes/           the four override sets + _themes.json registry (stateMechanism · neutralRamp ·
                      siblingPairs · console fencedPaths · ★ Legacy/SC motion kills)
  ★ component-types.json  THE ADR-0013 REGISTRY — one file, both halves: component-type/<group>/<param>
                      tokens ($alias→semantic + cached $value) + $members (selector map) + $partials
                      (source atom · rootSelector · requires/matchValues/declarations · $manifestBinds)
  snippets/           64 gated reference components = CANON (40 + Phase-2's 24). Atoms carry
                      PARTIAL blocks; consumers carry generated AUTO-PARTIAL blocks (provenance-
                      commented, sync-gated). Multi-control members = :is() selector lists (wave-1
                      convention); mixed sizes = local --phys-size override
  ★ gen_component_partials.py  injects partials into consumers; --check = build gate; selftest 8 bites
  ★ _validate_partials.py      the re-implementation RATCHET (strict on members · census = accretion
                      worklist) → _PARTIALS-GATE.md
  canon/              canon.css (token spine · components · AUTO-THEMES cascade) + type.css (HAND-AUTHORED)
                      + generators (gen_canon_tokens · gen_theme_cascade · ★ gen_canon_components — now
                      IN the build: regenerate-always + determinism --check, ADR-0013 ruling 4)
  guidelines/         the rules, each {#id} + destiny tag; _rules-index.json (generated)
  _proforma/          Apollo Mono tranches T1–T9 + the decisions ledgers (near-canonical per ruling 3)
  _consult.py         "what governs X?" — RUN IT before designing (corpus now DISCOVERED, ds-009 closed)
  _validate_*.py      the gates — incl. _validate_state_snap.py (ADR-0014) + ★ _validate_partials.py
  gen_showroom.py     generates showroom/ — never hand-edit showroom
showroom/             THE LIBRARY, browsable: 64 harness pages + index w/ live count (#theme=… all four)
reviews/              review sheets — ★ AWAITING DAVE: SC-DARK-MODE-2026-07-22-v1(.REVIEW).html
notes/_receipts/      worker-receipt dir · notes/_briefs/ conductor briefs
_LIVE-STATE.md        LIVE / DEAD / OPEN / TARGETS — read second, always
_GM-ARCHIVE.md        rolled-off GOOD-MORNING banners (verbatim, newest-first) — compaction, step 2c
_FUTURE-STATE.md      side-quests, ideas, RESURRECTION candidates
_DECISION-HISTORY/    dated narrative — ★ 2026-07-22: the ADR-0014 arc AND the ADR-0013/B-D7 arc
```

## The one command that matters
```
python3 knowledge/_build_all.py     # ★ the blocking build — it prints its own [i/N] step count;
                                    #   exits non-zero on any failure (count not hardcoded here: it rots — P4, 2026-07-26)
```

## Rules that actually bite (core + this session's)
- **CONSULT before designing** — then **survey before build**. *(This session the survey found Icon-button's
  physics was a REVIEWED refinement, not drift — which became B-D7.)*
- **★ ADR-0013 (BUILT): never re-type a sub-atom.** A registered partial's rule may exist ONLY in the
  atom's PARTIAL block or a generated AUTO-PARTIAL block — the ratchet gate blocks members' local
  re-implementations; the census lists everyone else's (accrete from OBSERVED duplication, ruling 3).
  Joining a family = markers + required vars + manifest binds + registry entry, and the generator
  fails loud on any missing piece.
- **★ B-D7: press physics is pixel-true and theme-dialable.** Travel/darken are TOKENS
  (`motion/press/*` → group caches); `--phys-size` is LOCAL geometry (buttons 120, icon 44); Legacy/SC
  zero the dial. **No JS in physics — ever** (Dave's constraint; DEF-003 posture). Tuning = token edit.
- **ADR-0014: semantic neutrals alias `color/neutral/*`, NEVER `color/mono/*` directly** · whites are
  classified (substrate → `neutral/15`; absolute → `color/white`, pinned).
- **ADR-0014: opacity states must SNAP** (`_validate_state_snap.py`, blocking, 7 checks incl. the
  text-state AA floor — inactive ≠ disabled).
- **Selftests are BUILD STEPS** — every new gate ships one AND wires it (partials + ratchet did).
- **Resurrect-verbatim is NOT gate-exempt** — the 273d18c~1 stepper's 13px/3px hit the grid gate on
  re-entry; corrected 12px/4px. Old reviewed artefacts re-enter through the same door as new work.
- **Grey-tint standing check** · **type26-013 (BLOCKING): white type is red-only** · **R-D6 glyph
  contrast by ROLE** · **`LEGACY_THEME_EXEMPTIONS`** (R-D24 — EXEMPTED, never passed).
- **canon.css** — generated only between AUTO markers; type.css HAND-AUTHORED. *(The ruling-4 gap is
  CLOSED: snippet RULE-text now self-heals into canon every build.)*
- **Every selector appended to `canon/type.css` is GLOBAL** — register in `_type-bindings.json` or the
  blast-radius gate fails.
- **Icons: real assets only** · **4px grid** · **sentence case** · **square corners in Mono** (radius =
  ROLE tokens, per-theme) · **weights: 100/300/400/500/700 only, NO 600.**
- **Derivation governance** — the engine never derives-and-promotes. **Promotion is Dave's alone.**
  *(SC dark values agent-derived → AWAIT him; B-D7's enacted values are HIS ruling, verbatim-quoted.)*
- **Spine discipline** — state lines in `_LIVE-STATE`; narrative >10 lines → `_DECISION-HISTORY/`.
- **Inscription prose is PARSER-VISIBLE** — no node names in ADR-header parentheticals (phantom edges).

## Standing instructions for the agent
- **Announce the model/routing split at the START of every substantive task** (`MODEL-ROUTING.md`).
- **Surface the chat names at BOTH ends — the small reliable thing Dave leans on, and it gets dropped
  (Dave flagged 2026-07-25).** At session START, offer the last handoff's "TITLE THE NEXT CHAT" as a
  ready-to-paste **"Rename this chat: …"**; at WRAP, put BOTH names at the top of `GOOD-MORNING.md`
  (ritual step 4b). Claude cannot rename chats itself — a name left unsurfaced is a label lost.
- **Verify before asking** (read repo / run gates) — including your own flags. **Reflect back before
  recording** a ruling — and when a ruling REVERSES, inscribe both beats (B-D7 is the model).
- **Decision-heavy / material-referring choices ship as review HTML** (`knowledge/_review/_make_review.py`
  — NOT at knowledge/ root). Architecture calls = the ADR-0012/0013/0014 model: options + firm
  recommendations in-chat, Dave rules by number, inscribe same hour, **feed the graph seed same hour**.
- **Surface spin-off candidates**; register ideas in `_FUTURE-STATE.md`. **Run the capture ritual
  unasked**; **stamp dates from `date`**. **Memory accelerates; the repo is the record.**
- **Stamp the context-gauge reading on every handoff artefact** — creator in `GOOD-MORNING` commit-state,
  workers in their receipt header — as a SCRUTINY indicator on that artefact (Red-authored ⇒ next reader
  re-verifies before trusting; not a quality score). Canon: `_RUNBOOK-context-gauge.md` § authoring-time stamp.

## The other standing documents (REACHABILITY-GATED by `_validate_standing_instructions.py` STAND-002 — keep every one referenced here)
`_STANDARDS.md` (★ the standards hub) · `AGENTS.md` · `MODEL-ROUTING.md` · `_FUTURE-STATE.md` · `_DECISION-HISTORY/README.md` ·
`knowledge/_proforma/_PROFORMA-RULES.md` · `knowledge/_proforma/_TYPE-DECISIONS.md` (T-D1…T-D14) ·
`knowledge/_proforma/_RAG-DECISIONS.md` (R-D1…R-D25) ·
`knowledge/_STYLE-PROVENANCE.md` · `knowledge/_proforma/_DATAVIZ-DECISIONS.md` ·
`docs/decisions/ADR-0012-decision-graph-edge-convention.md` (seed `notes/_decision-graph-seed-2026-07-21.json` —
★ 124/124 zero mismatch after B-D7; feed it EVERY inscription, or `--verify` drifts silent) ·
`docs/decisions/ADR-0013-component-type-tier-composition.md` (★ BUILT 2026-07-22 — Consequences updated) ·
`docs/decisions/ADR-0014-per-theme-neutral-primitives-state-snap.md` ·
`knowledge/_proforma/_BUTTON-DECISIONS.md` (B-D1…★ **B-D7**; in the CONSULT corpus since ds-009 closed) ·
`docs/decisions/ADR-0009-state-styling-architecture.md` · `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` · `docs/decisions/ADR-0011-four-theme-token-architecture.md` ·
`knowledge/_DS-IMPROVEMENTS.md` (ds-007 open · ds-008 ✅ · ds-009 ✅) · `knowledge/_ICON-GAPS.md` · `knowledge/_ASSERTIONS.md` +
`knowledge/_assertions.json` · `knowledge/guidelines/_rules-index.json` · ★ `knowledge/component-types.json` (the ADR-0013 registry) ·
`knowledge/_PARTIALS-GATE.md` (the ratchet report — census = Phase-2's accretion worklist). **Runbooks** indexed by `knowledge/_RUNBOOKS.md`.
*(This list was dropped in a rewrite once and STAND-002 red-flagged it — do not prune it.)*

## Parallel-session model (PROVEN 2026-07-21)
On "read good morning", role is picked (Worker / Conductor / Solo) — **from Dave's opener line ONLY;
titles are labels.** ONE conductor = single writer for shared state; workers emit receipts to
`notes/_receipts/`, no git. Conductor reconciles the shared tree before committing (never blind
`git add -A` with workers live). Every handoff carries a **DIVVY PLAN**. Workers can absorb live Dave
rulings mid-flight — receipt verbatim.

## Renders — REAL FONT, in-sandbox
**→ `knowledge/_RUNBOOK-render-verify.md` (stood up 2026-07-23, Dave's ask) — read it, don't
reconstruct.** Pipeline VERIFIED WORKING 2026-07-23: headless-shell download + libs + real-HSBC-cut
render all green (the 07-22 "download refused" reads as the installer's EXPECTED host-validation
exit — the runbook explains). Render-verify for ADR-0014 + ADR-0013 is now UNBLOCKED, still OWED
until actually run + seen. HTML is what Dave reviews; PNGs are agent self-verification only.

## How we work
- **Review loop:** every doc ships **clean source + REVIEW copy** (`knowledge/_review/_make_review.py <file>`).
- **Live tuners beat static versions past ~2 colour round-trips.** Sheets read canon.css LIVE, never retype.
- **Dave commits via GitHub Desktop.** Claude commits in-sandbox per `_RUNBOOK-git-commit.md` — run it,
  don't improvise. `unable to unlink … *.lock` warnings = the delete-guard, not failure; judge by HEAD.
- **Comms:** exec summary + numbered next steps first, detail below.

---

# §B · THIS SESSION

> ⚠ **STALE BELOW — do not read it as current (2026-07-27, later morning #3).** The three most recent
> sessions are summarised only in the ★ LATEST + ★ PRIOR banners at the top of this file, which are
> authoritative. This section still narrates the 07-26 lane ① window. **The narratives you actually
> want:** this session → `_DECISION-HISTORY/2026-07-27-the-instrument-cannot-see-the-property.md`
> (the KG exploration arc: the consult's two defects, Dave's two reframes, why held angle (1) would have
> missed `aid-009`, and the three-term pre-flight) · prior → `_DECISION-HISTORY/2026-07-27-the-gate-that-narrowed-its-own-rule.md`
> (the full arc: why the recommendation was wrong, the gate-narrowed-its-own-rule finding, the forked
> vocabulary, the third silent-fallback, and the probe repeating the wrong-document error) · rulings →
> `knowledge/_proforma/_DATAVIZ-DECISIONS.md` **DV-D14 + DV-D15** · defect record →
> `knowledge/_DS-IMPROVEMENTS.md` ds-014 (ENACTED block) · the register build →
> `docs/decisions/ADR-0016-enactment-proof-register.md`. Rewriting §B was again deliberately not
> attempted — the banner + DO-FIRST + the dossier carry the session, and a hot rewrite of a long
> narrative section is exactly what produced 07-26's three corrections.

> ⓘ Most recent = **legend wave lane ①** (2026-07-26 evening, Opus 5 solo self-conducting, effort MAX).
> The ★ LATEST banner is its summary; the narrative WHY/HOW — why the re-verify mattered more than the
> lane, the correction to my own correction on the grep, the two non-obvious calls the divvy didn't
> name — is `_DECISION-HISTORY/2026-07-26-legend-wave-lane-1-and-three-record-corrections.md`.
> **Evidence per claim** (`<source> · <date>`): build `_build_all.py` 55/55 GREEN · 2026-07-26 ·
> members `node knowledge/_verify_dv_legend_members.js` 54/54 · 2026-07-26 · exemplar
> `node knowledge/_verify_dv_legend.js` 27/27 · 2026-07-26 · migration state
> `python3 knowledge/_check_legend_migration.py` → donut ✅ bar ✅, combo + line remain · 2026-07-26 ·
> ds-010 closure = computed-fill read at 1180 + 760 in the licensed cut, font assert passed ·
> 2026-07-26 · ds-012 = per-label `getBBox()`, 6 of 6 clipped, worst 16.8px · 2026-07-26 ·
> byte figures = `knowledge/_BEHAVIOUR-GATE.md` + `wc -c` · 2026-07-26 · commit `aabe617`.
> **What I got wrong:** my first framing said a grep "cannot" discriminate the migration state —
> building the replacement disproved it (`data-series-toggle="` works today, on punctuation luck).
> Corrected in the script's docstring, the dv-behaviour comment, the dossier and the banner.
> The two older narratives below are retained for context.
>
> ⓘ (prior) the **bar-audit → CONDUCTOR window** (the
> narrative WHY lives in `_DECISION-HISTORY/2026-07-23-bar-audit-and-conductor-absorbs.md` — audit
> method, the contaminated-Q8-framing lesson, the base64-payload iframe borrow, the rulings arc,
> the two-lane reconcile incl. the `a2acc9e` mid-conduct note). Evidence per claim: audit sheet
> `reviews/BAR-CHART-AUDIT-2026-07-23-v1.REVIEW.html` (rendered 1400+840) · ledger DV-D08/09 +
> seed 76/130 (`f887efd`) · sidequest receipt + its commit (`db1ed1b`) · builds 51/51 at baseline
> AND post-inscription. The detailed narrative below is the **PRIOR Phase-2 waves** session,
> retained for context.

## (prior) 2026-07-22 evening — "Phase-2, BOTH waves: one conductor, five worker windows"

*The record lives in the receipts (5 worker + 2 conductor-reconcile, `notes/_receipts/2026-07-22-
phase2-*`) — no separate dossier; the receipts ARE the narrative, judgment calls included.*

- **✅ 24 components in one day** (W1: A-forms 4 + B-feedback 10 · W2: A-continuation 5 — **forms
  brief COMPLETE 9/9** — + C Data-grid + D Charts 4). Library 40→64, registry 4→18 members,
  radius 45-strict, **census 32→32 across everything**, 51/51 green at every reconcile. Firsts:
  calendar panel (Date-picker, composed from surveyed parts) · determinate progress bar
  (File-upload, ink-on-neutral) · Charts = the parked kit PROMOTED (provisional-agent, sign-off
  yours). Conventions minted: `:is()` multi-control members · local `--phys-size` on mixed sizes ·
  `proforma-promotion` provenance class · dataviz gate wired to chart snippets (new-surface rule).
- **✅ The protocol COMPOUNDS:** wave-1 absorb completed 7 lanes' contracts by hand (they fire only
  on registration — fails-loud proven); wave-2 workers READ that lesson and pre-landed contracts →
  both wave-2 absorbs injected clean first try. Fences held all day; A's wave-2 breach flag =
  misread of MY mid-wave absorb of C (resolved + inscribed in the wave-2 reconcile receipt —
  the name-every-path reflex worked, the inference didn't).
- **✅ Dave's in-flight asks handled by the hot-clause:** showroom header count SHIPPED (live 64) ·
  card thumbnails NOTED (`_FUTURE-STATE`, `#bare`-mode shape) · theme "outage" diagnosed as
  wrong-file + payload-is-base64 (pages were correct; Legacy's small delta on data components =
  architecture, not bug).
- **🐛 Wrong/caught:** Drawer close 44→36 (file beat receipt) · my pkill self-match (twice-class,
  receipted for the runbook) · one stale-cascade red per wave (my own serial edits, regen healed).
  **Owed:** render-verify (headless-shell, standing).

---

# §C · QUEUE

## 1. ★ NEXT STRANDS (pick one per window; role from the opener line)
**(a) ★ CHART-EXPANSION PROGRAMME — prove-one-then-wave (Dave ruled 2026-07-22, this session).**
**STEP 1 (next window, solo — DO THIS FIRST):** build the **scatter** exemplar END-TO-END — proforma
section in `_proforma/DataViz-interactive.html` (DV-D01) + promoted `snippets/Chart-scatter.reference.html`
(composites-only type, role-token radius, dataviz tokens, controls toolbar + legend + `<table>` spine) +
its `.meta` + registration (`MIGRATED_SNIPPETS` radius-strict · `CATEGORIES` "Charts") + regen
cascade+showroom → build green (dataviz gate globs `Chart-*` automatically). Hand to Dave to eyeball the
LOCK-UP before fanning out. **STEP 2 (wave) — DIVVY PLAN, the other 8 as fenced worker lanes** (NEW snippet
files + receipts only, no git): **lane 1** butterfly-h + butterfly-v + histogram (bar-family geometry) ·
**lane 2** box plot + bullet + candlestick (statistical/gauge; candlestick up/down = `data/delta/gain·loss`) ·
**lane 3** pie (donut-family, dv-pie-009 ≤6, D-Q2 labelling) + stacked area (line-family) + **promote**
grouped/stacked bars (D-Q3). Conductor = serial set (registry · MIGRATED_SNIPPETS · CATEGORIES · spine ·
ONE commit). **Heatmap NOT in scope — parked** (`_FUTURE-STATE` ★). Model: Sonnet/Fable workers, Opus conducts.
**(b) Wave 3 fan-out (component library)** — ~26 itinerary gaps remain (`reviews/ITINERARY-2026-07-14…`);
conductor surveys + cuts lane briefs (wave-1/2 = the pattern; candidates: navigation/menu family + P2 depth).
Serial set as always (registry · MIGRATED_SNIPPETS · CATEGORIES · spine · git = conductor only, ONE commit).
**(c) Templates+shells clean-room (Layer-2, the load-bearing gap)** — solo Fable ADR-style session.
Best AFTER the ruling batch: field-family, stepper-fold and delta-seam answers shape it.
**(d) Enact window (cheap)** — absorb §C·2 rulings as token/registry edits + §C·4; new candidates: mint
`data/axis`+`data/grid` (per ★ DV-D07 two-channel) · R-D9 ramp promotion · field-family group build if ruled ·
Stat-card `spark` slot · **★★ the live radius/corner tuner (Dave: return SOON).**
**(e) ★ ROUTING SIDE-QUEST — ✅ DONE + RATIFIED SAME DAY (2026-07-23 evening).** All 13 proposals
RATIFIED by Dave and #6–12 ENACTED in-session (his override): sheet
`reviews/ROUTING-AUDIT-2026-07-23-v1.REVIEW.html` · receipt
`notes/_receipts/2026-07-23-routing-sidequest-audit.md` (ruling verbatim). **#12 SUPERSEDES the
07-13 Mode-2 default-on** (delegation now DELIBERATE; MODEL-ROUTING tombstoned, memory hooks
updated). #13 = the calm-banner trial riding THIS handoff's top — Dave judges by eye. Residue in
§C·4: none owed beyond the trial verdict.

## 2. ★ DAVE: THE RULING BATCH — 15 REMAIN of 16 (D-Q3 = #14 RULED 2026-07-23, promote in the
wave; Q8/B2 also RESOLVED → DV-D08) + the ★ DATAVIZ SIGN-OFF (rule by number; all retro-propagate). **The sign-off first:** D promoted the PARKED kit verbatim into
Chart-bar/line/donut/sparkline — your review flips them provisional-agent→canon (open-014).
**New this wave, 8–16:**
8. **(A-Q5)** Calendar day-cells + Stepper done-dots carry NO press physics (judged selection
   targets / structural markers, the Tabs class) — confirm, or extend the family.
9. **(A-Q6)** File-upload built the library's FIRST determinate progress bar (ink-on-neutral,
   R-D22 spirit) — accretion candidate when a second consumer appears.
10. **(A-Q7)** Stepper consumes Progress-tracker's visuals by copy — fold to one snippet, or
    accrete a stepper-visuals partial at a third consumer?
11. **(A-Q8)** Date-range = restart-on-earlier-pick (inscribed as reference behaviour) — flag if
    the HSBC source says swap-endpoints.
12. **(D-Q1)** Line markers: Background fill (promoted default, theme-adaptive) vs White — the
    kit toggle never ruled.
13. **(D-Q2)** Donut labelling default: spider vs direct; letters-on-segments HELD (white letters
    on series fills — type26-013).
14. ~~**(D-Q3)** Promote the kit's grouped/stacked bars next wave?~~ **✅ RULED 2026-07-23 (audit
    B1): PROMOTE, wave bar lane** — ledger line under DV-D09's block; the Batch-1 #3
    grouped-LAYOUT open (reference images) is separate and stays open.
15. **(D-Q4)** Status-watch amber light-mode = 3.02:1 vs page — the R-D3 graphic floor with zero
    margin. Comfortable for charts, or lift?
16. **(D-Q5)** TWO delta conventions now live (charts `data/delta/gain·loss` vs Stat-card's R-D5
    rag arrows) — one canon convention, or a deliberate chart/card split?

**17–22 — RESTORED from the rolled 07-24 chart-wave banner (dream-pass v2 P1, ruled 2026-07-26):
the banner's compaction to `_GM-ARCHIVE.md:32` carried these out of live state; copied back
verbatim-in-substance. Same ruling mechanics as 8–16.**
17. **Q2 combo home** — new snippet vs Chart-bar variant.
18. ~~**Sweep hook / 16KB cap fork** — amend cap vs modularise.~~ **✅ RULED 2026-07-26: SPLIT *and* RE-SCOPE** — `dv-legend.js` is a second source; 16KB stays per-source (legibility) and a **32KB per-GROUP PAGE budget** was added so a split can't buy headroom. Inscribed **ADR-0015 § Amendment**; the sweep is no longer baked-static (DV-D12 runs).
19. **COMBO-LINE-INVERT R-B/R-C** — R-A casing DAVE-SEEN-PROVISIONAL.
20. **Chart-scatter Layer-2** — deferred, stays Layer-1 safe.
21. **Brush/range-select spec** — menu 8, designed not built.
22. **JS-off seg wart** — shared w/ Chart-line, atom-level fix.

## 2b. WAVE-1 RULINGS 1–7 (unchanged, rule with the above)
1. **Form-label weight** — the `.t-cm-label` composite renders 400; gated Input-fields labels are
   16/500. Rule 400 (Input-fields migrates later) or mint a 500 form-label composite (one type.css
   line + binding).
2. **`input-error` null slot** — the ADR-0010 slot you anticipated is NOT declared; all four form
   components bind semantic `rag/error` directly. Declare the null slot?
3. **Toast dark glyphs** — coloured shapes on the ELEVATED NEUTRAL ground (all ≥3.55); the
   white-shape dark ruling was made on TINTED grounds. Confirm or extend.
4. **Modal family fold** — Modal-lightbox extends Modals as a separate snippet; fold into one
   modal-family snippet later, or keep split + a dialog-mechanics partial when a group accretes?
5. **Figure vouch** — figure-4/5/6 composites still "PREPARED, awaiting vouch"; vouching flips
   Amount-display candidate→canon + hardens Stat-card's value type.
6. **★ Field-family accretion** (ADR-0013 ruling 3, cross-lane OBSERVED duplication — the
   wave's standout): field chrome (hover fill · focus black border + 4px stroke · error stroke)
   now consumed by copy across ≥7 files (Input-fields, Dropdown, Search-field + A's four +
   Account-selector). Accrete `field-family` as registry group #2 next wave?
7. **Showroom Overlays split** — B proposes Overlays (Drawer/Popover/Lightbox/Modals/Tooltip) +
   Data-display buckets; wave 1 filed into existing buckets. Re-bucket?
   *(Minor, flag-if-wrong: conductor decided the mixed-size idiom = local `--phys-size` override,
   inscribed in the registry; Secure-entry holds figure-3/24 in its 40px narrow cells (A-Q3);
   fl-summary ≈ Alert filed to the dedup pass (A-Q4); linked Stat-card variant awaits the
   press/link posture question (B-Q6).)*

## 3. ★ THE STANDING EYEBALL SET (NON-BLOCKING — your "foundations first" ruling; pin-comments
now live in every showroom pane, so it's async)
**(a) B-D7 motion:** Button/Modals presses calm down · Progress-tracker scale press + dots↔line
collapse through 520px · Icon-button identical · `#theme=legacy`/`#theme=supercharge` = colour-only.
**(b)** SC dark sheet `reviews/SC-DARK-MODE-2026-07-22-v1.REVIEW.html` + 4 held whites + Console
radius px + bigplay. **(c) NEW from Phase-2:** all 24 new components across 4 themes × light/dark — the Charts 4 double
as the dataviz sign-off (§C·2).

## 4. Enact-queue (cheap, post-rulings)
**★ NEW 2026-07-27 (from exploration beat 1) — carried here by the 2c EXIT CHECK so compaction can't lose them:**
**consult `5/5 shown` denominator** — trivial, separable from the enforcement-column question, do it regardless ·
**`CTRL` vocabulary sweep** in `_validate_a11y.py` (`dv-vocab` pattern, 1,869 selectors skip today) ·
**ds-014 (d) donut cluster alignment** — PARKED on Dave, logged not fixed (`.dv-donut-row` `flex-start`) ·
**ds-015's exemption warnings** are advisory by design — they become the hit-area gate's worklist when it lands.
**★ NEW 2026-07-26 (from lane ①) — carried up here by the 2c EXIT CHECK, so they survive banner compaction:**
**DV-D13 aria asymmetry** — the legend's `aria-label`s deliberately keep BOTH the value and percent forms
(a screen-reader user shouldn't lose data to a toggle they may never perceive). Flagged at inscription,
**confirm at the wave's a11y pass** · **`_check_legend_migration.py`** is the authorisation to delete the
transitional block (exit 0) — the old grep in the handoff could never fire · **ds-012** h-bar labels clipped
16.8px, Dave's call on fix shape (`_DS-IMPROVEMENTS.md`) · **the swatch-shape delta** on Chart-bar, reversible
on request (`_REVIEW-SIGNOFF.md`).
**★ NEW 2026-07-26 (from the cap-fork session):** wire **BOTH** verify suites — `_verify_dv_legend.js` (donut exemplar, 27/27) and `_verify_dv_legend_members.js` (members, 54/54) — as advisory build steps, or vendor their jsdom dependency (today: `npm i jsdom` into `/tmp`, unwired; two suites now, so the prize is bigger) · decide `Chart-sparkline`'s **inert 15.6KB payload** (needs per-member behaviour opt-in in the registry — schema change) · give the graph parser a convention for an **ADR-amendment node** (`--verify` shows 5 unmatched seed edges) · F1 Legacy icon/default white · F2 Legacy `rag/error-tint` · tag-atom radius reconcile · F5 Dropdown's
6 locals · designer-pack v2.1 re-bake · **DV-D09 enact** (h-bar → series-3; bar lane) · **pro-forma dedup pass (ruling 3 — now also carries wave-1's
fl-summary≈Alert + B's observation that Tranche-1/2 hold earlier empty-state/toast sketches)** ·
composite motion tokens (would retire the matchValues pin) · enact whatever §C·2/§C·3 rulings change ·
consider `--verify` blocking.

## 4b. ★ QUEUED: button-states finesse pass (Dave 2026-07-22, "not now — follow up") *(was §C·3b — the wave-1 briefs/receipts + prior deltas point here under that number)*
Full brief in `_FUTURE-STATE.md` §button-states-finesse. Headlines: **Legacy state-mechanism fidelity
question** (as-built may be OPACITY, we render colours — VERIFY against source, don't flip on
recollection; "Legacy shouldn't change" = the design is frozen, our reproduction of it can be
corrected) · **Mono+Console pressed = darker pressed fill** (ties to the open tertiary/quaternary
pressed-token gap; B-D7's softer darken makes this more visible) · **SC keeps the opacity option
open, probably won't change** · **loader ATOM for all loading states** (registry group candidate #2;
Button's `.spin` = first consumer). Theme posture, Dave: Legacy frozen; Mono/SC/Console all in
design development. Natural shape: one session = fidelity check + pressed-tint tuner (review HTML,
rule live) + loader accretion.

## 5. Parked (unchanged)
Legacy hex seeding + provenance-gate flip · Console/Supercharge chromatic palettes · T9 review ·
Sutherland field test · full-review backlog (`_REVIEW-SIGNOFF.md`) · `_FUTURE-STATE` items ·
spot-illustration/empty-state icon set (`_ICON-GAPS.md`, wave-1's only gap).

> **COMMIT STATE (refreshed 2026-07-27 ~10:35 BST from `date`, KG exploration beat 1 + ds-015).**
> ONE commit: `_FUTURE-STATE.md` (**Exploration beat 1** — Dave's two reframes verbatim, instrument-fit as
> a third axis, adoption-time trigger, 3 open questions) · `knowledge/_DS-IMPROVEMENTS.md` (**ds-015 NEW**
> — the exemption, the measurements, the diamond's three blindnesses, severity caveat + anti-false-fix) ·
> `knowledge/_validate_a11y.py` (**the silent `continue` now WARNS** + a 17-line anti-false-fix provenance
> block) · `knowledge/_RUNBOOK-context-gauge.md` (**PRE-FLIGHT is THREE terms** + instrument cost rows) ·
> `_DECISION-HISTORY/2026-07-27-the-instrument-cannot-see-the-property.md` (**NEW dossier**) ·
> regenerated `knowledge/_A11Y-GATE.md` + `_consult-index.json` · `_LIVE-STATE` + `_GM-ARCHIVE` (Batch 7)
> + `_LIVE-STATE-ARCHIVE` rolls · this file.
> **Build 58/58 GREEN (exit 0) · a11y gate 67 snippets / 0 fail / 13 warn (was 6 — the 7 new are the
> exemptions declaring themselves) · STAND-002 PASS, 26 standing docs reachable.**
> **NOTHING WAS BUILT — his instruction was explore, not build.** Both enactments are reversible and
> neither pre-empts a ruling.
> **Context gauge at authoring: 🟡 AMBER ~58% + ~5% wrap ⇒ 🔴 RED ~63% at close (ESTIMATE ±15%).** Read off
> the band table, and **priced in advance this time** — the three-term rule was written mid-session and
> immediately applied to itself: the instrument-tagging build was CUT rather than started, and the ritual
> was reserved before the last job began. ⇒ **Next reader: the ★ LATEST banner and §DO-FIRST were authored
> in Amber and are the trustworthy part; this block was written at the Red boundary — re-verify the PROSE,
> which is what no gate sees.** *(That instruction earned its keep today: it is how this session caught the
> previous handoff quoting a register figure that had already moved.)*
> Dave pushes via GitHub Desktop (whole stack, Desktop closed while Claude commits).
