# Good morning, Dave ☕

> **RENAME THE WRAPPED CHAT →** `Apollo — "we are losing decisions": ds-013 caught by Dave's eye (srcdoc killed type.css in ALL 49 showroom panes, every gate green throughout) · legend wave CLOSED (combo + line, 100/100) · the enactment register RULED — 🔴 Red ~92% wrap`
> **TITLE THE NEXT CHAT →** `Apollo — ADR-0016 P2: write the ruled-vs-RENDERED proofs, starting with the two Dave found (dv-004 separation · alpha-key contrast). FOUR CALLS ARE HIS AND GATE THE WORK — read §DO-FIRST before writing any code`
> *(Titles are LABELS — role comes from Dave's opener line. The wave = the parallel model: Opus conducts, workers per lane, DIVVY in §DO-FIRST. Gauge bands: Green<45 / Amber 45–60 / Red≥60.)*


> ## ★ LATEST — 2026-07-27 (Mon **later** morning, OPUS solo self-conducting, effort MAX — ★ **ADR-0016 BUILT: `_ENACTMENT-REGISTER.md` — 3 of 76 rulings (4%) are PROVEN** · **ds-014 DISCHARGED by render: 2 lost decisions, 2 artefacts** · **dv-004 proven blind on 3 chart types**; build **57/57 GREEN**; 🔴 RED ~92% wrap): **Dave read the brief and said "as you advise". So: the discriminator first, then the build he ruled. The discriminator settled all four flags in one pass — and the root cause of one of them generalised into the number the register now reports.**
> - **★ ds-014 SETTLED — MEASURED, at 1180 and 760, licensed cut, snippet BESIDE showroom pane.** **#2 stacked segment spacing — LOST:** gap **0.0–0.1px** on all 4 columns × 3 boundaries, `stroke:none`, against a **BLOCKING dv-004 that requires ≥2px**. **#3 stacked alpha-key contrast — LOST:** keys render **`#1A1A1A` (`--ink`)**, not the `var(--page)` their markup declares — `text.dv-barkey{fill:var(--ink)}` beats the SVG presentation attribute — giving **3.31 / 3.46 / 3.78:1** at 12px/700 against AA's 4.5:1; white measures ≈5:1 and passes. **#1 + #4 — ARTEFACTS:** donut centre value **dx +0.00 / dy −2.00**, ring offset **0.00**, identical in both artefacts at both widths. ds-013 was the whole story.
> - **★ WHY #2 SHIPPED GREEN — and it is bigger than one chart.** `_validate_dataviz.py` guards dv-004 with `if dtype in ("donut","pie","stacked")`; the figure declares **`stacked-column`**. **The gate never looked.** ⚠ **PROVEN BY BITE in a scratch copy** — adding that one string makes it fail: `✗ dv-004: stacked-column segment lacks a >=2px surface-coloured separating stroke.` **Three blind values in the corpus** (`stacked-column`, `grouped-column`, `scatter`, all zero mentions in the gate) ⇒ **dv-004, dv-bar-009 and dv-line-011 are inert on those types.**
> - **★ THE REGISTER — P1 SHIPPED, P3 WIRED ADVISORY (step 56/57).** `_build_enactment_register.py` harvests every ruling from the four ledgers + all ADRs: **PROVEN 3 · CLAIMED 20 · UNPROVEN 53 · NOT-GATEABLE 0**. **The four-verdict scheme is the contribution, and CLAIMED is the point** — a check names the ruling but nothing proves the check can FAIL. **ds-013 lived in CLAIMED for weeks.** Advisory deliberately: *a gate that fails 53 rows on day one gets switched off, and a switched-off gate is how we got here.*
> - **★ THE REFRAME, and it is the thing to carry.** Dave is not noticing four regressions. **He is noticing the visible edge of 73 rulings that nothing checks** — with his eyes, because that is currently the only instrument we have.
> - **⚠ TWO SELF-INFLICTED ERRORS, both caught, both inscribed.** ADR-0016's draft said *75/52* — written before the generator ran; **the register harvests ADRs, so it counts itself**: measured **76/53**. Same class as Correction 2 of 07-26. And the probe's first donut pass used `querySelector('svg')`, which returns the **toolbar copy icon** — it reported a 16px-wide "chart canvas". **The probe committed the exact error it was written to detect.**
> - **🔴 RED ~92% (Dave's calibration; I had said 85%, and called that Amber) — AND THE GAUGE ITSELF FAILED TWICE, which is the finding.** ⚠ **I labelled it "Amber" at an already-understated 85%. Our own bands are Green<45 / Amber 45–60 / Red≥60 — 85 is deep RED**, and the mislabel went into this banner, `_LIVE-STATE` and the summary Dave read. **A false reading of the instrument built to catch false readings.** Second failure, Dave's: **the gauge was only consulted at WRAP.** It has to be estimated **BEFORE committing to a big job**, so the cost is priced when it can still change the plan. ⇒ **Both now ruled into `_RUNBOOK-context-gauge.md` as the PRE-FLIGHT step + a band table you read, never recall.** ⇒ **Next reader RE-VERIFIES this banner's prose before building on it** — it was written at ~92%.
>
> ## ★ PRIOR — 2026-07-27 (Mon morning, OPUS solo self-conducting, effort MAX — ★ **THE LEGEND WAVE IS CLOSED** (combo + line migrated, 100/100, transitional block deleted) **+ ds-013: `srcdoc` had killed `type.css` in ALL 49 showroom panes**; build 56/56 GREEN; commit `ba336dc`; 🔴 RED ~80% wrap): **Dave opened with a bug report, not a lane: *"the labeling on the donut and bars, they are all too big apart from the reset button, we had an independent scale for labels that seems to have been lost."* He was exactly right, and the cause was three tiers below the charts.**
> - **★ ds-013 — THE SHOWROOM HAS BEEN RENDERING UNCOMPOSED TYPE, LIBRARY-WIDE.** `gen_showroom.py` hands each snippet to its pane iframe as **`srcdoc`**, and a srcdoc document inherits the **parent's** base URL. So every snippet's own `<link href="../canon/type.css">` — correct from `knowledge/snippets/` — re-resolved against `showroom/` to a path that does not exist. **type.css 404'd in all 49 panes that link it**; every `.t-cm-*` composite AND selector binding in it was inert. Measured, licensed cut: legend label **16px/400 → 12px/500**, letter key **→ 12px/700**. **Reset was the only correct label in the pane because its CSS hard-codes `font-size:12px`** — precisely the asymmetry Dave described.
> - **★ NOT a lane-① regression — OBSERVED, not assumed.** The PRE-migration snippet (`git show 7401daf~1`) renders **13.333px** under the same unreachable-type.css condition (the `<button>` UA default). The outage predates the wave; DV-D11's `.dv-leg-item{font:inherit}` swapped that default for the inherited **16px** and cost the key its 700 weight, which is what pushed it past Dave's threshold.
> - **★ FIXED + GATED, not patched.** `rebase_payload_urls()` re-points payload URLs; **a rebased URL whose target is missing FAILS THE BUILD**. Selftest (6 bites) wired as build step 56. ⚠ One bite pins the anti-fix: an injected `<base href>` would also re-base fragment URLs and break **every icon sprite** in the library. **My own selftest caught a real defect in my own fix** (query/fragment suffixes were being dropped) before it shipped.
> - **★ LANES ②③ DONE — the wave is COMPLETE.** Chart-combo (2 series) + Chart-line (3 series) on DV-D11. **Combo keeps a circle swatch** for its line series — two mark types on one plot makes shape a real channel (bar's were dropped because all its marks are rects); **line earns the full circle/square/diamond set**. ⚠ **Non-obvious, unnamed by the divvy:** the diamond's `rotate(45deg)` also rotates its 44px hit-area `::before`, so the target stood on its corner — **counter-rotated**, and proved by `elementFromPoint` probes at both widths.
> - **★ THE VERIFY SUITE WAS LYING BY CONSTRUCTION.** `_verify_dv_legend_members.js` had baked in **bar's three series** (`const [a,b,c] = L.ids`) and the **literal name "Current"** — so it crashed on a 2-series member and would have "passed" any member whose series happened to be called Current. Generalised to per-N invariants, names read off the markup. **54 → 100 checks; bar's 54 unchanged in number, wording and meaning.**
> - **★ TRANSITION CLOSED** (`_check_legend_migration.py` exit 0): transitional block deleted (`dv-behaviour.js` 15,771 → **13,004 B**), dead `.dv-legend*`/`.dv-legbtn*`/`.dv-quiet` CSS deleted from all four members. **Page budget 31,490 → 28,723 B (88%).** ⚠ **The handoff predicted 85% / 27,768 B. 88% is the MEASURED number** — recorded as measured, per Saturday's Correction 2.
> - **★ A PROMOTION TRIED AND REVERSED — the more useful fact.** Promoting `class="dv-legrow` to dv-legend's universal contract (as the old note instructed) **failed the build, correctly**: Chart-sparkline and Chart-scatter are members of the dataviz behaviour **GROUP** but carry no legend. **The group is broader than the capability** ⇒ the universal contract stays empty, now permanently and for a better reason. Real fix = the already-logged per-member behaviour opt-in (schema change, **Dave's call**).
> - **⬛ OWED, and it is the next session: 49 showroom panes now render CANON type for the first time and NOBODY HAS LOOKED.** Registered in `_REVIEW-SIGNOFF.md`. Dave chose "lanes now, sweep after"; the window went to the lanes. **Build the sweep as a NUMERIC assertion, not an eyeball pass** (§DO-FIRST).
> - **🔴 RED ~80% (ESTIMATE ±15%)** ⇒ **next reader RE-VERIFIES before building** — and re-verify the PROSE, not just the gates: that is where all three of Saturday's errors lived, and this banner was written hotter than that one.
>
> *(Compaction 2c — keep ★ LATEST + 1 PRIOR, roll the rest. Older banners (the 07-22→24 chart-wave + ADR arc, the 07-25 AM v4 + midday→PM v5 + PM Memento-efficiency + PM#2 memory/routing-governor banners) are in `_GM-ARCHIVE.md` (Batches 1–6), verbatim, newest-first; durable narrative in `_DECISION-HISTORY/` + `notes/`.)*

---

*Briefing — refreshed 2026-07-27 ~08:30 BST (date from `date`), session "ADR-0016 built — the
enactment register (4% PROVEN) + ds-014 settled by render" (Opus 5 solo self-conducting, effort
MAX). §A = orientation · §B = session · §C = queue.*

## ⬛ DO THIS FIRST

> **✅ CLOSED, do not re-open.** The legend wave (all four members on DV-D11, `_check_legend_migration.py`
> exit 0, page budget 88%). **ds-014's discriminator — it RAN**, and all four of Dave's flags are
> settled with measurements in `knowledge/_DS-IMPROVEMENTS.md`. **ADR-0016 P1 + P3-advisory.**
> Nothing here is owed twice.
>
> **★★★ DO FIRST — PUT THE FOUR CALLS TO DAVE. They gate everything else in this section, and
> three of them cannot be answered by an agent (derivation governance).**
> The discriminator turned Dave's four flags into **two lost decisions and two artefacts**, and
> then the register turned the root cause of one into a corpus-wide number. What is owed now is
> not investigation — it is **his ruling**:
> - **(a) dv-004 on stacked columns.** Measured separation **0.0–0.1px**, `stroke:none`; the rule
>   is BLOCKING and requires **≥2px**. Fix by a 2px surface-coloured stroke (the donut's existing
>   mechanism) or by a geometry gap? **Both change the chart's look.**
> - **(b) The alpha keys (A/B/C on the segments).** They render **`#1A1A1A`** because
>   `text.dv-barkey{fill:var(--ink)}` (snippet L127 · canon.css L3434) overrides the `var(--page)`
>   in their own markup. **3.31 / 3.46 / 3.78:1** at 12px/700 vs AA's 4.5:1. White measures ≈5:1
>   and passes, and the D-Q2 ledger line already says white — so this may be pure restoration.
>   ⚠ It collides with **type26-013 (white type is red-only)**, which the ledger flagged and never
>   resolved. **That collision is the actual decision.**
> - **(c) Widening the gate's dtype vocabulary is mechanical — but it turns (a) into a RED BUILD.**
>   So it lands *with* (a)'s answer, never before it. Do not "tidy" it early.
> - **(d) NEW, un-ruled, not on his list:** `.dv-donut-row` is `flex-start`, so the ring+legend
>   cluster pins left and whitespace grows with viewport (**−114px at 600 → −534px at 1440** from
>   figure centre). No ruling covers donut cluster alignment. Flagged only — do not fix it.
>
> **★★★ THEN — ADR-0016 P2: THE PROOFS. This is the build, and (a)+(b) are its first two.**
> `docs/decisions/ADR-0016-enactment-proof-register.md` is accepted; `knowledge/_ENACTMENT-REGISTER.md`
> is generated every build (step 56/57, **advisory**). Today's reading: **PROVEN 3 · CLAIMED 20 ·
> UNPROVEN 53 · NOT-GATEABLE 0, of 76.**
> **The non-obvious part of P2, and the reason CLAIMED exists:** a proof that reads the ledger and
> compares it to another document proves nothing — that is what we already had. **Read the RULED
> value out of the source of truth and assert the RENDERED value** in a real browser with the
> licensed face. `_sweep_type_enactment.py` is the pattern; `_RUNBOOK-render-verify.md` is the recipe.
> ⚠ **Every P2 proof ships with a bite that proves the proof can FAIL.** Non-negotiable, and it has
> now caught a real defect three sessions running:
> - `_sweep_type_enactment.py` reported a cheerful "0 deviations" while it could not read the
>   stylesheet at all (**that is how ds-013 survived weeks**).
> - `_verify_dv_legend_members.js` would have passed any member whose series was named "Current".
> - **This session, twice.** dv-004 passed a chart with 0.0px separation because its branch tests
>   `"stacked"` and the figure says `"stacked-column"` — **proven by bite in a scratch copy: adding
>   that one string makes the gate fail correctly.** And *my own probe* first measured the donut with
>   `querySelector('svg')`, which returns the **toolbar copy icon** — it reported a 16px-wide "chart".
>   **The probe committed the exact error it was written to detect. Assume yours will too.**
>
> **★★ THE SCOPE-BLINDNESS LANE — three chart types are ungoverned right now.**
> `stacked-column`, `grouped-column` and `scatter` appear **zero** times in `_validate_dataviz.py`
> ⇒ **dv-004, dv-bar-009 and dv-line-011 are all inert on them.** The register audits this
> automatically for `data-dv-type`. **Generalising that audit to other gate vocabularies is high-value
> and nobody has looked** — it is the cheapest way to find the next ds-013.
>
> **★★ STILL OWED, unchanged and NOT superseded by any of the above:**
> **(i) The showroom type sweep.** `knowledge/_sweep_type_enactment.py` ran once: **800
> composite-bound elements across 67 panes, 22 deviations in 27 panes** — the pattern is **WEIGHT,
> not size**. Worst pane stepper (3); also amount-input · date-picker · date-range-picker · drawer ·
> empty-state. Results in `knowledge/_type-sweep-2026-07-27.json`. ⚠ It needs
> `--allow-file-access-from-files` or it reads ZERO composites and reports a cheerful "0 deviations".
> **This is a P2 proof in all but name — fold it into the register rather than running it as a
> one-off.**
> **(ii) §C·2's RULING BATCH (15 + 17–22)** — has not moved in days, gates §C·1(c). **Fable is the
> model for that session** (open judgment).
> **(iii) The hit-area rule + gate rebuild** — read `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`
> FIRST. Chart-line's 45°-rotated diamond swatch (whose hit target rotated with it) is a live case:
> a markup-driven hit-area gate must understand transforms.
> **(iv) Radius/corner tuner (§C·1d)** — v1+v2 BUILT + render-verified
> (`reviews/RADIUS-CORNER-TUNER-2026-07-24-v*.html`); owed = the TWEAKS + ruling the numbers with
> Dave ("return soon, don't let me forget"). **Do NOT rebuild from scratch.**
>
> **MODEL + EFFORT (Dave ruled 2026-07-26, still current):** conductor = **Opus 5, effort MAX** ·
> mechanical lanes = **Sonnet, default** · **Fable reserved** for open-judgment sessions (the ruling
> batch · the hit-area gate). P2 is **script-then-judge**: any model can write a proof; **every
> deviation it finds is Dave's call, not the agent's.**
>
> *Standing: every handoff carries both names (top) + a DIVVY PLAN. **Render-verify re-proven from
> scratch AGAIN 2026-07-27** — runbook held, but bank one NEW pothole: staged on the shared mount,
> `playwright install` fails at **`EPERM rmdir '__dirlock'`**, not at host-validation. Same reading —
> **check the cache, proceed** (`chromium_headless_shell-*` was present and worked). Prior potholes
> still true: `/tmp` NOT writable (use the outputs mount) · FONTCONFIG_FILE replaces not merges ·
> the two-alias fontconfig is required · **render the SNIPPET for canon truth and the SHOWROOM PAGE
> for what Dave looks at** — since ds-013 they finally agree, and a probe's job is to prove that,
> not assume it.*

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

> ⚠ **STALE BELOW — do not read it as current (2026-07-27, later morning).** The two most recent
> sessions are summarised only in the ★ LATEST + ★ PRIOR banners at the top of this file, which are
> authoritative. This section still narrates the 07-26 lane ① window. **The narrative for
> ADR-0016 / ds-014 lives in `docs/decisions/ADR-0016-enactment-proof-register.md` (§ Provenance
> carries every measurement) and `knowledge/_DS-IMPROVEMENTS.md` ds-014.** Rewriting §B was
> deliberately not attempted at Amber — the banner + DO-FIRST carry the session, and a hot rewrite
> of a long narrative section is exactly what produced 07-26's three corrections.

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

> **COMMIT STATE (refreshed 2026-07-26 ~20:0x BST, cap-fork + donut-migration session).** ONE commit:
> `canon/dv-legend.js` (new) · `canon/dv-behaviour.js` (legend isolated behind a TRANSITIONAL block) ·
> `_validate_behaviour.py` (check_group + PAGE_BYTES + 5 bites) · `component-types.json` (dv-legend
> registered, donut hooks migrated, the old deferral marked RULED) · `Chart-donut.reference.html`
> (migrated) + 4 members' marker pairs · regenerated `canon.css`/showroom/`_BEHAVIOUR-GATE.md` ·
> `_verify_dv_legend.js` (new, 27/27) · ADR-0015 § Amendment · seed + graph · `_REVIEW-SIGNOFF.md` ·
> `_LIVE-STATE` + `_GM-ARCHIVE` + `_LIVE-STATE-ARCHIVE` rolls · this file · the dossier.
> **Build 55/55 GREEN · behaviour gate green (page budget 31,268 B = 95% during transition) · library 67.**
> **Context gauge at authoring: 🔴 RED ~72% (ESTIMATE)** — Red-authored ⇒ next reader re-verifies before
> building on it. Dave pushes via GitHub Desktop (whole stack, Desktop closed while Claude commits).
