# _LIVE-STATE — what's true now (cold-start spine)

*The supersession ledger for the project: what's **LIVE**, what's **DEAD** (don't build on it), what's
**OPEN**, plus in-flight **TARGETS**. Read this second, after `GOOD-MORNING.md`, before
`knowledge/README.md`. Per **ADR-0007**. ⚠️ **INTERIM — hand-maintained** until `_build_live_state.py`
generates it from front-matter edges + tombstones. Refresh at end of every session alongside the
handoff — and **stamp the date from `date`, never from the session's own belief** (the T-D12 handoff
mis-dated itself a day forward; commit timestamps caught it).*

*Siblings: **`_FUTURE-STATE.md`** — side-quests, feature ideas, resurrection candidates (the forward
half of the state machine, Dave's ask 2026-07-18) · **`_DECISION-HISTORY/`** — dated per-thread
narrative, relocated verbatim (how we got here; see its README for the rules + RESURRECT tags).*

## 🔀 SPIN-OFF LANE — Memento dream-pass (registered 2026-07-26, per the spin-off rule; runs COLD from its own record, deliberately OUTSIDE the GM queue — the lane itself dogfoods §4.2's cold-read thesis)
Entry point: `notes/2026-07-26-memento-dream-pass-scope-v2.md` (three shapes: Cowork · Claude Code · VS Code+Copilot) → v1 same date (§4.1 fields+gate, tooling verification) → `notes/2026-07-26-memento-dreaming-convergence-and-buildable.md` (the record).
**Status (2026-07-26, later session): D1–D4′ RULED + §4.1 BUILT.** Rulings + why: `notes/_MEMENTO-DECISIONS.md` (D1a repo-side · D2 five values · D3 one script · D4′ §4.1→A→C→B; D5/D6 pencilled). Built: `knowledge/_capture_gate.py` (build/wrap/selftest modes) wired blocking into `_build_all.py`; runbook steps 1b/2/3 + gate section amended; cutover `notes/2026-07-26-provenance-cutover.md`; three lane notes field-retrofitted. **NEXT for this lane: Shape A** — scheduled Cowork task emitting `notes/_dream/…-proposals.md` (scope v1 §4). Owed: convergence-note `-v2` (still blocked on re-attach of `2026-07-26-convergence-anthropic-dreaming.md`) · Dave's D6 access check before any Shape C build. Prior commits `dfdc857` + `f140fee` + `d22f29f` (f140fee/d22f29f unpushed as of this session's start — Desktop push owed).
**Status (2026-07-26 evening, Shape A session): SHAPE A BUILT + FIRST DREAM PASS RUN — 8 floated proposals await Dave.** A-D1–A-D4 RULED (ledger, explicit option-select): manual-first-then-schedule · weekly/last-~15 (config only — task NOT created, earns itself on this file) · D5 ENACTED `.claude/agents/dreamer.md` (steering spec, single source for Shapes A/B/C; dot-path blocked to file tools → written via shell) · proposals home `notes/_dream/` — verified OUTSIDE `_capture_gate.py`'s glob, fields by discipline (A-D4). First pass: ONE cold Opus dreamer subagent, 15/15 transcripts read (turn-level ceiling held), evidence repo-verified → `notes/_dream/2026-07-26-proposals.md` (298 lines, 8 proposals ranked by prevalence; conductor spot-checked 3/3: P1 `_LIVE-STATE` 855 lines/205,561 B exact · P3 render-verify runbook untouched since 07-23, greps 0 · P5 ds-010 live at `Chart-bar.reference.html:102`, GM count 0). Dreamer also recorded a checked-clear list so the next pass doesn't re-open settled ground. NEXT: **Dave READS the proposals file** — promotion his alone (derivation-governance) → on his say-so the weekly task is created per A-D2. Owed unchanged: convergence `-v2` (blocked on re-attach) · D6 before any Shape C. Prior lane commits verified pushed at session start (`06e48ef` = origin/master).
**Status (2026-07-26 evening, ruling session): DAVE RULED THE DREAM — P1–P5+P7+P8 accept-enact-now (ENACTED), P6 deferred to its own session (parked `_FUTURE-STATE.md`), rejections: none; S-D1 schedule EARNED (`memento-dream-pass` weekly, Sun 07:10, per A-D2) · S-D2 lane flag (`--wrap --lane`) + S-D3 stdout-only wrap BUILT + bite-tested — both wrap-gate warts CLOSED.** Full rulings + WHY + enactment receipt: `notes/_MEMENTO-DECISIONS.md`. Headline enactments on main-queue surfaces (by ruling, per proposal): `_LIVE-STATE-ARCHIVE.md` (this file 205KB→62KB, ritual step 2d) · `knowledge/_git_commit.sh` + runbook · render-verify runbook fold · GM count/tuner/ds-010 lines · `_FUTURE-STATE` corrections. **Lane is now STEADY-STATE: the weekly task dreams; Dave rules; sessions enact.** Owed unchanged: convergence `-v2` (blocked on re-attach) · D6 before any Shape C. ⚠ `ec4c2f3` was UNPUSHED at this session's start — push the whole stack via Desktop.
**Status (2026-07-26 evening, weekly-run session): SECOND DREAM PASS RUN + RULED SAME SESSION — V2-P1–P4 ENACTED, V2-P5 HELD.** Pass ran cold per the lane checklist (Fable conductor + 1 Opus dreamer, repo-first forensics); 5 proposals → `notes/_dream/2026-07-26-proposals-v2.md` (commit `d777aaa`, 4/4 conductor spot-checks held). Dave ruled in plain language same session: V2-P1 six 07-24 chart deferrals RESTORED to GM §C·2 as **17–22** + compaction EXIT CHECK in ritual 2c/2d · V2-P2 emitter determinism FIXED (7 `sorted()` sites, 4 scripts; advisory 6/6 identical under random hash, §C·4 line closed; dated-banner mentions left historical) · V2-P3 ds-011 logged (G/H/N advisory promotions + triggers, incl. WCAG 2.4.1 Level A ×5 screens) · V2-P4 `_REVIEW-SIGNOFF.md` fed 4 strands (legend v5.x · tuner v1+v2 · hit-area rule brief · 5 chart panes) + ritual step-1 feed-the-register clause. **V2-P5(a) ENACTED same session — Dave re-attached the note; saved verbatim to `notes/2026-07-26-convergence-anthropic-dreaming.md` (+fields, gate 0 fail); the three-session blocker is DEAD.** V2-P5(b) (runbook save-uploads clause) pencilled, awaits his word. Ledger rows V2-P1–P5 in `notes/_MEMENTO-DECISIONS.md`. Build 55/55 GREEN post-enactment. **Continuation same session (Dave: "love your work continue"): V2-P5(b) ENACTED (save-cited-uploads clause, ritual step 1; read as the yes, vetoable) + convergence `-v2` WRITTEN** — `notes/2026-07-26-convergence-anthropic-dreaming-v2.md` (Opus worker + Fable 4/4 spot-check incl. independent transcript grep; supersedes v1 in-part, v1 stays as filed; §3-verification fixes + databases-Q&A recorded OWED in its §7). **Lane's owed list now: D6 (Dave, before Shape C) + `-v2`'s own §7 leftovers only.** **S-D4 (same evening): conductor sequence inscribed → `knowledge/_RUNBOOK-dream-pass.md`; Cowork skill `dream-pass` + the weekly task prompt are thin pointers to it — "run dream pass" is now the whole invocation.**

## ⏱ LATEST DELTA — 2026-07-27 (Mon **later morning #4**, OPUS solo self-conducting, effort MAX — ★ **CALLS (1)(2)(3)(5) RULED BY DAVE; the 465-rule INSTRUMENT-FIT pass is BUILT, RUN and WIRED** · ★ **ds-016 — 7 LIVE GATES CITE RULES THE INDEX CANNOT SEE: 698 anchors declared, 465 indexed, 265 invisible — `aid-009` among them** · build **60/60 GREEN**; 🔴 RED ~72% at ritual) — "He said 'most robust methods', so the tool was built so it could not guess. Then bite 1 failed on its first run and the failure was the finding: the rule the a11y gate enforces is not in the rules index at all."

- **★ CALL (3) DELIVERED — `knowledge/_build_instrument_fit.py`, the instrument ladder at corpus scale.** I0 STATIC (source bytes) → I1 DOM (parsed tree) → I2 RENDER (computed/composited/geometric) → I3 EYE (judgment, never a defect). **Sits ON TOP of ADR-0016:** the register asks *is there a check and can it fail*; this asks *can it observe the property at all*. Generated `_INSTRUMENT-FIT.md` + `_instrument-fit.json`, **11 bites**, wired **advisory** as build steps 58 (selftest) + 59 (report) per the P3 posture.
- **★ MEASURED: 465 rules — UNDER-INSTRUMENTED 12 · UNGATED 165 · UNTAGGED 279 · EYE-ONLY 4 · FIT 5.** ⚠ **The limit is stated first, not buried: 279 of 465 (60%) are UNTAGGED**, so **12 is a FLOOR, not an answer.** Deliberately NOT fixed by widening patterns until the report went quiet — that is anti-false-fix #2 in the tool's own header, and it would convert a measured finding into a tuned one. **Two of the 12 are BLOCKING and both are contrast rules with STATIC gates:** `dv-016` (chart titles/axis/gridlines) and `icon-011` (*"icons require 4.5:1 in all instances"*). **Contrast is a COMPOSITED property** — a static parse reads the declared hex, not what lands on screen. Same class as ds-010 · ds-013 · DV-D15, now four proven instances.
- **★ ds-016 — THE FINDING NOBODY WENT LOOKING FOR, and it is ds-015 INVERTED.** Bite 1 asserted the ds-015 ground truth and returned `None`: **`aid-009` is not in `_rules-index.json`.** Chasing it: `guidelines/*.md` declares **698** rule anchors; the index holds the **465** carrying an enforcement-destiny tag; the other **265 are invisible** to the index, `_consult.py`, the enactment register and this pass — and **7 of them are cited by a live gate as its authority** (`aca-003` · `aca-004` · **`aid-009`** · `aid-020` · `avd-006` · `axs-003` · `nam-001`). `aid-009` is Dave's 2026-07-03 hit-area ruling, named 5× by `_validate_a11y.py`; **its anchor line simply never got a destiny tag.** Mirror image in the same family: **`icon-005` (BLOCKING, 44×44 target) IS indexed and NO gate names it.** ⇒ There the gate couldn't see the component; **here the INDEX can't see the rule** — markup correct, lookup fails, nothing reports it. ⚠ **The 265 are excluded BY DESIGN, not by bug; the defect is the SILENCE.** LOGGED not fixed — the remedy is call (4)'s discussion, unruled.
- **⚠ THE BITES CAUGHT THREE DEFECTS IN MY OWN TOOL, ALL ON FIRST RUN.** (1) A crude bare-word probe read **three** gates as RENDER — `_validate_proforma.py`, `_validate_token_tiers.py`, `_validate_type_composites.py` — matching the word **chrome**, as in *mono*chrome and *demo-*chrome. ⚠ **Wrong direction: it makes gates look STRONGER than they are**, which in a fitness audit buys silence. (2) `icon-005` came out **FIT** with `_build_instrument_fit.py` itself as the evidence — **a register that NAMES a rule was counting as a check that ENFORCES it**; fixed with `NOT_A_GATE` (this file + `_build_enactment_register.py`, same exposure). (3) bite 1's failure ⇒ ds-016. **Third session running for "assume your probe is wrong in the direction that reads as green".**
- **★ CALL (2) RULED — ADOPTION-TIME AND SWEEP ARE COMPLEMENTARY (Dave: *"You're right about 2 they are complimentary"*).** He asked to be corrected; **his lean was right, the framing was the thing that needed correcting.** Adoption-time captures intent from whoever knows *why* — **counted** data, not inferred — but is blind to everything already shipped (**64 of 67 snippets already carry the `::before` expander; it would find zero**), and a *missing* declaration is silence. Sweep is retroactive and needs no cooperation — **proven the same day, it found the 7 dangling citations laid down months apart** — but reports late and **its own coverage is unmeasured** (blind to 265 rules, can't classify 279 more; nothing revealed that until a second check was built). ⇒ **The only way to detect a MISSING declaration is to sweep for it**, so the sweep is what makes adoption-time enforceable. Held shape: **adoption-time forcing function + a sweep narrowed to one job, finding undeclared adoptions.**
- **Evidence:** build `python3 knowledge/_build_all.py` **60/60 GREEN exit 0** · 2026-07-27 · selftest `_build_instrument_fit.py --selftest` **11/11** · 2026-07-27 · register `knowledge/_INSTRUMENT-FIT.md` (465 rules) · 2026-07-27 · capture gate **13 in scope / 0 fail / 0 warn** · 2026-07-27 · defect `knowledge/_DS-IMPROVEMENTS.md` **ds-016** · ideas `_FUTURE-STATE.md` § KG forcing-function **Exploration beat 2** · dossier `_DECISION-HISTORY/2026-07-27-the-index-cannot-see-the-rule.md`.
- **⬛ STILL DAVE'S:** **(4)** consult enforcement column — *"I lean fix, but this probably needs a discussion"*, **NOT ruled**; the `5/5 shown` denominator is separable + trivial and was **NOT done** (Red budget). **(5)** `CTRL` vocabulary sweep — **ruled YES, NOT started.** **NEW:** invest in the pattern table (279 UNTAGGED)? · ds-016's three remedies (fail-loud / tag the 7 / both).
- **🔴 Gauge: RED ~72% at ritual (ESTIMATE ±15%).** Read off the band table. Pre-flight was stated before the build and ran ~10 points over — the miss was ds-016, an unplanned finding chased mid-job. **Wrap reserved in advance per the three-term rule.**

## ⏱ PRIOR DELTA — 2026-07-27 (Mon **later morning #3**, OPUS solo self-conducting, effort MAX — ★ **KG FORCING-FUNCTION: EXPLORATION BEAT 1 — Dave reframed it TWICE and both reframes beat the four held angles** · ★ **ds-015: `aid-009`'s hit-area check EXEMPTS every component that adopts the hit-area mechanism — 7 of 67 snippets are actually measured, gate says "0 failures"** · **PRE-FLIGHT now has THREE terms** · build **58/58 GREEN**; 🟡 AMBER ~58%, nothing built by design) — "He asked to explore, not build, so I explored. The consult's own instrument turned out to be guessing; then Dave read the exhibit and said 'maybe we are checking the wrong thing', which was righter than my exhibit — the rule is negated by the very mechanism that satisfies it."

- **★ THE HEADLINE, and it is Dave's: INSTRUMENT FIT IS A THIRD AXIS.** Angle (1) of the FLOATED idea (*compare what a rule SAYS against what its gate DEMANDS*) **would NOT have caught `aid-009`.** The rule names *"a minimum 44×44px target area"*; the gate calls its check *"target size"* — **the vocabulary matches; the narrowing is in the INSTRUMENT.** A static regex observes a *declared box*; the rule is about a *target*. They stop tracking each other the moment the property is expressed through a mechanism (expander · token · transform) — and **the gate goes QUIET, not RED.** ⇒ **Sits ON TOP of ADR-0016, not inside it:** PROVEN/CLAIMED/UNPROVEN ask *"is there a check and can it fail?"*; this asks *"is it looking at the right thing?"* — **a check can be PROVEN and still measure a proxy that doesn't track its rule.** dv-004 was the *narrowing* case; `aid-009` is the *instrument* case, and it is larger.
- **★ ds-015 — ADOPTING THE CORRECT MECHANISM IS WHAT REMOVES A COMPONENT FROM THE CHECK.** `_validate_a11y.py` does not mis-measure the `::before` expander; it **`continue`s**, deferring to a "render axis" that **does not exist** (the hit-area gate is still PENDING DAVE SIGN-OFF). **MEASURED: 67 snippets · 1,869 selectors skipped by the `CTRL` vocabulary · 14 eligible · 7 exempted · 7 actually measured.** Verdict **0 failures, exit 0**; 64 of 67 snippets use `::before`. **The diamond proves it three times** (`.dv-leg-sw.sw-diamond`, 8×8 + `rotate(45deg)`): out of `CTRL` scope · expander is `min-width:var(--hit,44px)` and the regex reads literal `(\d+)px` · `::before` → exempt. ⚠ And its real defect is a **transform** consequence — **no static box measurement can see that in principle**; `elementFromPoint` caught it by hand in the legend wave.
- **★ DAVE'S SECOND REFRAME — the propagation defect, and the strongest angle yet.** *"we are relying too much on my memory here, the hit mechanism should have triggered something that cascaded this elsewhere."* Adoption is a LOCAL CSS decision with a GLOBAL governance consequence and **nothing carried it** — no registry entry, no re-check, no flag. Sibling of the assertion-propagation gap, but worse: **the gate never fires at all, because the adoption IS the exemption.** ⇒ **The trigger should be ADOPTION-TIME, not sweep-time.** Cheapest cut: make claiming the exemption require naming the rule it exempts from, and let the register harvest it — **an exemption that must declare itself is one you can count.**
- **⚠ THE CONSULT'S OWN INSTRUMENT IS GUESSING — two defects, bite-tested.** (1) `rulings (5/5 shown, --all for more)` is **shown/CAP, not shown/total** — `:200` truncates, `:217` counts the truncated list, the true population is discarded before printing. True totals **28 · 38 · 54**; agent sees **17–22%** of the material, and **BLOCKING rules truncate too** (5 of 16). (2) `enforcement_for_rule()` decides gated-ness by **keyword overlap between rule text and gate text/glob** — it never opens the gate. **54 BLOCKING rules · consult claims a gate for 25 · 10 of those are named in no `.py` file at all.** ⚠ Stated then and now: that proves **unverified**, not **unenforced**. In fairness the docstring is candid ("possibly gated by", "answered per-query") — **it is a good hint; the defect appears only when Dave's proposal promotes the hint to an authority.**
- **★ PRE-FLIGHT NOW HAS THREE TERMS (Dave: *"remember that it self consumes tockens too"* + *"encode a pre-flight mechanism rather than loosing it in this chat"*).** The rule was already inscribed, so it was NOT re-litigated — what was missing is the **meta-cost**. ⇒ `_RUNBOOK-context-gauge.md`: **"A pre-flight estimate that does not include the wrap is not a pre-flight estimate" — `fill + job + WRAP (~5%) = projected band`, always three terms.** Consequences: **reserve the wrap BEFORE starting the job** (at Amber the question is never *"can I fit this job?"* but *"can I fit this job AND the ritual?"*) · instruments obey their own bands — **except reading the band table.** Evidence: last session priced its render job right (53%, held) then ran **the ritual unpriced**, 58→63, band corrected at close. **Applied to itself same window: the instrument-tagging build was CUT, not started.**
- **✅ ENACTED — two, both reversible, neither pre-empting a ruling.** `_validate_a11y.py`'s silent `continue` now **warns** (6→13 warnings, 0 failures) with an **anti-false-fix block**: do NOT delete the exemption and fail those selectors — they are **unmeasured**, not non-compliant, and a static parse cannot tell the difference. Plus the runbook clause above. **Nothing else built — his instruction was explore, not build.**
- **⚠ CORRECTED THE HANDOFF'S OWN PROSE IN THE FIRST TWO MINUTES.** The ★ LATEST banner said register **PROVEN 4 / UNPROVEN 52 of 76**; the generated file reads **54 of 78** — DV-D14+DV-D15 were inscribed and the register harvested them. **The RED ~63% stamp told the next reader to re-verify the prose, and it worked.** Also verified rather than inherited: **no chat-rename tool exists** (searched loaded + deferred; `session_info` is read-only) — the runbook's step-4b claim stands, re-verified.
- **Evidence:** build `_build_all.py` **58/58 GREEN exit 0** · 2026-07-27 · a11y gate **67 snippets / 0 fail / 13 warn** · 2026-07-27 · corpus scan reproducing the gate's own `CTRL`/`DECOR` regexes · 2026-07-27 · consult bite-test 3 queries default-vs-`--all` · 2026-07-27 · defect `knowledge/_DS-IMPROVEMENTS.md` **ds-015** · ideas `_FUTURE-STATE.md` § KG forcing-function **Exploration beat 1** · dossier `_DECISION-HISTORY/2026-07-27-the-instrument-cannot-see-the-property.md`.
- **⬛ FIVE CALLS ARE DAVE'S** (all in ds-015 + `_FUTURE-STATE`): (1) instrument-fit = third register axis or its own check? (2) trigger adoption-time or sweep-time? (3) run the 465-rule instrument-tagging pass? (4) fix or REMOVE the consult's enforcement column — a wrong "gated by" is worse than none; the `5/5` denominator is trivial and separable. (5) **`CTRL` is an UNSWEPT vocabulary** — the `dv-vocab` pattern applies directly and has been run nowhere but dataviz.
- **🟡 Gauge at authoring: AMBER ~58% (ESTIMATE ±15%), wrap reserved at ~5% per the new three-term rule.** Read off the band table. Nothing was built past Amber, deliberately.

## ⏱ PRIOR DELTA — 2026-07-27 (Mon **later morning #2**, OPUS solo self-conducting, effort MAX — ★ **ds-014 CALLS (a)+(b) RULED BY DAVE, ENACTED AND PROVEN BY RENDER** · ★ **the gate had NARROWED ITS OWN RULE — dv-004's text is mechanism-neutral, its gate demanded a stroke** · **`dv-vocab` NEW BLOCKING: unknown chart types can no longer skip silently** · build **58/58 GREEN**; register **PROVEN 3→4, UNPROVEN 53→52**; 🟡 AMBER ~58% wrap) — "Dave declined my recommendation and asked why I'd made it. Checking cost one grep and he was right — the donut's stroke mechanism doesn't transfer to a plot with gridlines behind it. Chasing *why* I'd recommended it found the real defect: the gate had quietly narrowed a mechanism-neutral rule into one mechanism, so it wasn't just failing to catch the error, it was the source of it."

- **★ DV-D14 — dv-004 is satisfied by GEOMETRY on gridded plots (Dave's ruling, against my recommendation).** I proposed the donut's 2px `stroke="var(--page)"`. Dave: *"I prefer the geometry the border will obscure gridlines, may I know why you recommend borders?"* **He was right and the check took one grep: `cb5` carries 5 full-width `.dv-grid` lines behind the columns; the donut carries none.** An SVG stroke straddles its path, so 2px puts 1px OUTSIDE each rect — painting over every gridline down both sides of all 4 columns. ⇒ **A surface-coloured stroke only simulates separation when the thing behind it IS the surface.** Enacted **variant A, both ends pinned**: baseline `y=230` and each stack top stay TRUE, the 4px comes out of segment heights. **Accepted cost, stated at ruling time: segments understate 2.0–2.6%, worst on the shortest column.**
- **★ THE FINDING THAT OUTRANKS THE CHART — the gate had narrowed the rule.** dv-004's text is **mechanism-NEUTRAL** (*"minimum 2px separation between colour blocks"*); `_validate_dataviz.py` enforced *"must carry a surface-coloured stroke >=2px"*. Both directions bite: a chart satisfying dv-004 by real geometry **would have FAILED**, and **an agent reading the gate to learn what compliance looks like gets the wrong answer** — which is exactly what happened to me. Dave supplied the governing fact from the KG (*"the gap is only 2px minimum, this is in the dataviz specifications in the KG"*) and then named the class himself → **held as FLOATED in `_FUTURE-STATE.md`** (his exploration, do not build ahead of it). ⚠ Caution recorded there: the consult prints `rulings (5/5 shown, --all for more)` — **it TRUNCATES**, so a forcing function built on it would be a CLAIMED gate with extra steps.
- **★ DV-D15 — `data/text/on-series` MINTED (Dave's promotion).** The keys had declared `var(--page)`: white today only because of where the neutral ramp sits — **a coincidence, not an intent**. New role → `color/grey/white`, **pinned in BOTH modes**, modelled on `rag/text/on-dark`; **deliberately NO alpha channel** (DV-D07 computes contrast from the composite, so an alpha slot is a route to passing on the hex and failing on screen). **type26-013 does NOT collide** — checked, not assumed: *"black/dark-grey on light · white/light-grey on dark"* covers it; the white-only clause is specific to RED grounds.
- **★ THE VOCABULARY HAD FORKED — fixed structurally, not by enumeration.** The corpus carries **both `stacked` and `stacked-column`, both `grouped` and `grouped-column`**, plus `scatter`. Adding three strings would have guaranteed a repeat ⇒ **`DTYPE_CANON` normalises once at read time** + **`dv-vocab` (NEW, BLOCKING) fails the build on any dtype the gate has never heard of**, naming the rules that would have skipped it. Scope-blindness audit: 3 blind values → **"none detected"**. **The dataviz selftest is now WIRED into the build** — it existed and ran only by hand, which is precisely why nothing ever proved dv-004 could fail. 9 new bites, incl. one reproducing the exact ds-014 figure.
- **⚠ A THIRD SILENT-FALLBACK, and it happened AFTER the build went green.** Token minted, generated into `canon.css`, build 58/58 — **and the keys still rendered BLACK at 3.99:1.** The snippet carries a LOCAL MIRROR of the token list for standalone preview and didn't declare the new var; **`fill:var(--undefined)` falls back to the SVG initial value, black, in silence.** Third instance of one class, three different mechanisms: ds-010 (author CSS beat `fill=`) · ds-013 (404 stylesheet) · this. **Through-line: a lookup that misses and reports nothing — and in all three the markup is CORRECT, so no static gate reaches it.**
- **★ PROVEN BY RENDER — `knowledge/_verify_dv_stacked_enactment.py` (NEW, the ADR-0016 P2 proof).** Licensed cut, **snippet AND showroom pane, 1180 AND 760, all four agreeing**: separation **2.00px** on all 8 boundaries; keys white at **5.26 / 5.04 / 4.61:1** vs AA 4.5. ⚠ **The prior handoff predicted "≈5:1"; MEASURED worst case is 4.61:1** (series-3, margin **0.11**) — recorded as measured. **Series-3 cannot be lightened without breaking AA.**
- **⚠ THE PROBE COMMITTED THE ERROR IT WAS WRITTEN TO DETECT — third session running.** First run reported *"no stacked-column figure"* for the showroom; the honest reading was not "the showroom is broken" but **"I queried the top document and the panes are `srcdoc` iframes"**. Last session's probe used `querySelector('svg')` and got the toolbar copy icon. **Standing lesson, earned three times: assume your probe is wrong in the direction that reads as green.**
- **⬛ (d) donut cluster alignment — PARKED on Dave's ruling.** Logged in `_DS-IMPROVEMENTS.md`, deliberately NOT fixed; rule it in a session where he can see it live.
- **Evidence:** build `_build_all.py` **58/58 GREEN exit 0** · 2026-07-27 · gate selftest **22/22** incl. 9 new · 2026-07-27 · render proof `_verify_dv_stacked_enactment.py` **ALL ASSERTIONS PASS**, 4 contexts · 2026-07-27 · register `knowledge/_ENACTMENT-REGISTER.md` PROVEN 4 / CLAIMED 20 / UNPROVEN 52 of 76 · 2026-07-27 · ledger DV-D14 + DV-D15 · dossier `_DECISION-HISTORY/2026-07-27-the-gate-that-narrowed-its-own-rule.md`.
- **🔴 Gauge at ritual close: RED ~63% (ESTIMATE ±15%) — CORRECTED.** Banner authored at a true AMBER ~58%; the ritual cost ~5% more, crossing the Red≥60 line. Read off the band table, not recalled. **AMBER ~58%** — wrapped deliberately at Dave's "wrap up" rather than starting the remaining 52 P2 proofs hot. **Pre-flight was stated before the render job, per the new rule, and held.**

## ⏱ OLDER DELTAS — rolled to `_LIVE-STATE-ARCHIVE.md` (P1, ruled 2026-07-26)
Verbatim, newest-first, nothing deleted — exact sibling of `_GM-ARCHIVE.md`. Roll rule: this file keeps **LATEST + 2 PRIOR** deltas; the capture ritual rolls the rest (see `knowledge/_RUNBOOK-capture-ritual.md`, step 2d).

> **SPINE DISCIPLINE (ruled 2026-07-18, Fable consolidation session — supersedes the "1044 lines"
> banner):** state lines live here; **narrative longer than ~10 lines goes to `_DECISION-HISTORY/` at
> write time, in the same pass.** Split entries end `History: _DECISION-HISTORY/<file>`. Advisory
> tripwire ~500 lines. Edits to this file are reachability-relevant — run
> `python3 knowledge/_validate_standing_instructions.py` (STAND-002) after touching it.

*Last refreshed: **2026-07-27 ~10:55 BST (from `date`) — "Instrument fit at corpus scale: calls (1)(2)(3)(5) ruled; the 465-rule pass BUILT+RUN+WIRED (12 under-instrumented, 2 BLOCKING contrast rules, 279 UNTAGGED = a floor not an answer); ds-016 — 7 live gates cite rules the index cannot see, aid-009 among them; adoption-time and sweep ruled COMPLEMENTARY; build 60/60 GREEN" (OPUS solo self-conducting, effort MAX, main queue)** · Previous: **2026-07-27 ~10:30 BST — "KG forcing-function EXPLORATION BEAT 1: INSTRUMENT FIT is a third axis + the trigger should be ADOPTION-TIME; ds-015; PRE-FLIGHT now three terms; 58/58" (OPUS solo self-conducting)** · Previous: **2026-07-27 ~09:30 BST — "ds-014 calls (a)+(b) RULED, ENACTED and PROVEN BY RENDER; dv-004's gate had NARROWED its own rule; dv-vocab NEW BLOCKING; 58/58" (OPUS solo self-conducting)** · Older refresh chain → `_LIVE-STATE-ARCHIVE.md`.*
1104 → ~450 lines per the classification Dave ruled via markup (11 pins) on
`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`. Nothing deleted: ~580 lines relocated verbatim to
`_DECISION-HISTORY/`, duplicates reduced to pointers, two entries removed on their own recorded
instructions. Prior refresh: T-D12 ruling, commit `9fb1381`.*

## 🕓 OPEN — Latin Univers **WEBFONT**: waiting on brand (raised 2026-07-18, reframed same week)

> **DOWNGRADED from ⛔ BLOCKING to 🕓 WAITING.** Dave: *"the license will be renewed soon, it may well
> have been already, the webfont needed Ultralight added, I think this is only procedural, and low
> risk."* **The commercial judgement is his and recorded as made — do not re-litigate it.**

**Split the question in two. Only one half is about risk.**

**(1) LICENCE — procedural, pending, low-risk. Owner: BRAND, chased by Dave.** The renewal is in
flight; the delta is a *weight* (**Ultralight**) being added. Write **"renewal pending; Dave assesses
the gap as procedural and low-risk"** — never "we have no licence".

**(2) ASSETS — unchanged, and NOT a risk question.** Verified by inventory: **zero Latin
`.woff`/`.woff2` files exist in the repo** (five script packs present; Latin has none). A favourable
licence does not deliver files — shareable real-face material stays blocked until the pack physically
lands, because there is nothing to embed.

**✅ DISTRIBUTION — CLOSED, ruled "leave".** The four tracked files embedding base64 woff2 stay. No
`git rm --cached`, no BFG, no history rewrite. Repo is private (confirmed by Dave) and shared only to
HSBC employees — every recipient sits inside HSBC's own licence. Interim control retained:
`reviews/*CONTACT*.html` gitignored; share OUTSIDE HSBC as PDF only.

**WHAT CLEARS THIS:** (1) **files land** — `HSBC_MtUnivers_Latin-*.woff/.woff2` in
`knowledge/assets/fonts/` (this alone unblocks shareable material); (2) **brand confirms whether
Ultralight is in scope** — ⚠️ not a detail: the packs ship Th/Lt/Rg/Md/Bd ≡ 100/300/400/500/700, so
Ultralight is a **sixth weight below Thin → a change to the canon ramp → a TYPE RULING, not an asset
drop.** Expect it; don't discover it in a diff.

**Provenance corrections, kept loud (full record: `knowledge/_proforma/_TYPE-DECISIONS.md`
§ Blockers 1):** I struck this blocker as "false" and Dave caught it. And
`WebfontUserGuide-2024.pdf` is **generic Monotype guidance, not an entitlement record** — "we hold no
Latin webfont" rests on absence of files, not on any document.

## LIVE — current truth (in force)

### ⭐ TYPE and BOX are SEPARATE — T-D12, RULED + VERIFIED across 21 files (2026-07-18)
- **Two lists, two questions.** `.t-cm-<size>` = TYPE (family, size, weight, **`line-height:1`**) —
  **safe to bind anywhere.** `.t-cm-slot` = BOX (`display:inline-flex`, `align-items`, `min-height`,
  cap-trim) — **opt-in**, bound ONLY where the element already declares a flex display.
- **`--slot` carries the slot height on the type composite.** A custom property is inert unless read,
  so a type-only binding has no box consequence. That is what makes the two lists independent.
- **`line-height` is TYPE, not BOX** — Component tier *is* "single-line at line-height 1". This was
  not the question the queue asked and it is the one that decided the batch: with line-height in the
  box, type-only bindings silently DROPPED the `/1` the old shorthand carried.
- **Cap-trim reaches elements that lacked it, and the shift is ACCEPTED** — refusing it would leave
  two classes of button in canon.
- **The slot test stays conservative.** "Already declares flex" is the OBSERVED condition `.btn` met,
  not a theory. **Slotting anything else is a per-component decision with its own diff, never a
  mechanical sweep.** Widening it is a ruling.
- Evidence: 13/21 pixel-identical, 0 page-height changes, real HSBC Univers. Ledger:
  `_proforma/_TYPE-DECISIONS.md` **T-D12**; sheet `reviews/TYPE-BOX-SPLIT-2026-07-18.html`.
  Validation state: **unaudited**.
- **METHOD, reusable:** the `NO_SNAP=1` isolation control in `apply_type_bind.py` separated diffs the
  binding CAUSED from diffs T-D10 INTENDED. **A diff you cannot attribute is not evidence.** Reach for
  a control before reaching for a verdict.

### Type binding — RULED + PROVEN on one component (2026-07-18)
- **Mechanism = (d) selector-list extension, HAND-MAINTAINED.** A component binds by being appended
  to its composite's selector list in `canon/type.css`. Plain CSS: no generator, no build step, no
  markup change. `type-bindings.json` + orphan gate = an OPTIONAL later upgrade, **explicitly
  deferred — do not build**. Ledger: `_proforma/_TYPE-DECISIONS.md` T-D9.
- **`.t-cm` is variant D.** Cap-trim sits on the **ELEMENT**; the former required `.txt` child is
  **GONE**. `inline-flex` + `align-items:center` centres the cap box in a taller slot — an
  `inline-block` variant TOP-ALIGNS and is wrong. Observed in real HSBC Univers. Supersedes the
  07-17 composite.
- **⚠️ LOAD ORDER IS LOAD-BEARING.** `.t-cm-button` and `.btn` are both specificity 0-1-0 → source
  order decides. **`type.css` must load BEFORE component CSS.** Not yet gated.
- **Delivery = `<link>`, NOT inlining.** The portable unit is the PROJECT, not the file (Dave: *"the
  entire project must be portable… a package, pulled from a repo"*). The 49-file inline sweep was
  solving a problem that does not exist.
- **`type.css` is HAND-AUTHORED.** The "generated" header was false provenance; removed.
- **Bound so far: `.btn` (selector-list) + Countdown `.num` (CLASS).** **T-D14 (2026-07-19):** new rung
  `.t-cm-figure-3` (24px/500) added to the ramp; the countdown numeral is the **first composite bound in
  MARKUP** — via a class on the element, because bare `.num` can't go global (collides with `.cn-table td.num`).
  Zero-visual-change (500 = shipped value). **ASSERT-003 retired** (clears_when met). ⚠️ **The BULK binding
  mechanism for the remaining ~338 stays OPEN** — this was one collision-forced case, NOT a general ruling. Ledger: T-D14.
- **Unchanged from 07-17:** CSS cap-trim · 4px slot · slot min `ceil(cap + 2·descender)` snapped to
  4px · descender guard baked INTO the slot · stacks use `gap`, **never padding**.

### RAG — amber SOLVED, background/glyph split (2026-07-18)
- **Two tokens per hue: `background` (fills) + `glyph` (icons, arrows, text).** Red/green/blue hold
  the SAME value in both roles; **only amber diverges**. Ledger: `_proforma/_RAG-DECISIONS.md`.
- **`amber/background` = `#F0B13A`** — ink on it 9.16. **`amber/graphic` = `#C58900`** — 3.02 on
  white, 6.25 on `#111`; required by `{#dv-016}` (≥3:1 series fills, blocking).
- **Rule 1 — amber is always paired with black text. Rule 2 — amber is not a DIRECTIONAL delta
  colour**; it remains valid for status and tolerance.
- **White is the RAG text colour universally; dark-text variant DROPPED** (R-D1) — amber the sole
  exception, always was.
- **`#000000` retained in the KB as brand source of truth**; `#1A1A1A` = digital black for screens;
  `#1D1D1D` dropped; `#333333` canon, stays.
- **Incumbent RAG values NOT deleted** — retired into a future legacy theme. Tombstone, keep.
- **R-D4 (2026-07-18): matting rungs RULED — green + blue matted 15%** (`#2B7E4F` / `#306EC6`),
  red as-is, one level across both. **Role tokens PROMOTED** into `semantic-colour.json` as
  `rag/<hue>-background` + `rag/<hue>-glyph` (additive; incumbents untouched; zero components
  rebound yet — rebinding waits for the blast-radius gate). Green promoted **light-only**: the
  contrast gate refused the known-failing incumbent dark (3.37) — dark leaf lands with the
  dark-green ruling. Gate model gained `RULED_PAIR_EXCLUSIONS` (white text × amber fill is
  forbidden by rule 1, so the audit no longer tests it). Ledger: R-D4.
- **★ DARK SET LOCKED (2026-07-19, R-D5…R-D11).** Full arc: `_DECISION-HISTORY/2026-07-19-rag-colour-halation-ramp.md`.
  Dark-mode RAG (mode-stable for red/amber; per §note below for green/blue): **breach `#B92F1E` white ·
  watch `#F0B13A`/`#C58900` black · healthy `#43AD6F` black · info `#5F92B9` black** (cyan-shifted for
  astigmatic legibility). Weight uniform Medium 500. Marks icon/label-paired (never bare coloured text on
  dark). **Red = carve-out (deep+white, instability); amber = carve-out (lightness); green+blue = the
  isoluminant→RAMP-tuned pair.** Key rulings: R-D6 (halation = 3rd axis: bloom vs dance, thickness selects
  the mode; glyph-contrast-by-role) · R-D7 (red locked, weight polarity→uniform 500) · R-D9 (status colour
  is a SALIENCE RAMP, not isoluminant — loudness descends with severity) · R-D10 (set locked).
- **✅ LIGHT FILLS LOCKED (2026-07-19, R-D12…R-D14) — full set now reconciled.** R-D11 (fills are ground-relative)
  RESOLVED: **light green `#5DAC7B` · light blue `#7DABCD`** (H241, black text); dark stays R-D10 (`#43AD6F`/`#5F92B9`);
  red `#B92F1E`/white + amber `#F0B13A`/`#C58900` mode-stable. **NO lines** (R-D12 A, aesthetic); **black text on states**
  (R-D12 B). **Fill contrast = salience lever, NOT a floor** — the LABEL carries meaning (R-D6), so amber-soft-on-white is
  ruled fine (I over-raised it; Dave corrected). **★ Per-mode PROVEN, not asserted:** exhaustive search shows no single
  green/blue keeps green›blue on both grounds (loud=darker on white, lighter on dark). Reconciled table + arc: ledger
  R-D12…R-D14; sign-off `reviews/RAG-LIGHT-FILLS-2026-07-19-v9-LOCKED`; derivation `reviews/_rag_light_fills_calc.py`;
  ★ **two-mode in-browser TUNER** (v6→v7, OKLCh, ramp-guard) = Apollo Labs / Layer-2 controls candidate.
- **✅ FILLS PROMOTED (2026-07-19, this session).** R-D14 fills written to `semantic-colour.json` `*-background`
  + propagated to `canon.css`: light `#5DAC7B`/`#7DABCD`, dark `#43AD6F`/`#5F92B9`, breach `#B92F1E` now mode-stable,
  watch `#F0B13A`. `rag/text` polarity (white on breach, black on states — `type26-013`+R-D12 B) enacted via the
  **existing `RULED_PAIR_EXCLUSIONS`** (white×green/blue forbidden, like amber). Build green. **NOT rebound** — components
  render RAG as dots (glyphs, bind incumbents, R-D6 fine) + chips (tints); the `-background` fills await the §1
  manifestation pick. **Both amber rules still unenforced (gate owed).**
- **★ FOUR-THEME ARCHITECTURE — R-D15 (2026-07-19).** ONE token store + ONE baseline library, toggling **4 themes:
  Apollo Legacy · Mono · Console (UI) · Supercharge (SC)**. Components bind theme-agnostic roles; theme override sets
  supply the hex. **Apollo Legacy** alone carries the teals AND the HSBC brand `color/grey/100–800`. **The baseline we
  build now = Apollo Mono, "very mono": monochrome throughout, colour ONLY in RAG + data-vis.** Broader colour/theming
  build PARKED ("deal with colours later"). Ledger R-D15; memory `four-theme-architecture`.
- **★ Apollo Mono grey ramp = `color/mono/1…15`** (2026-07-19, R-D15). Dual-end brightness curve (γ=1.7, 15 stable
  index steps, black→white), packing resolution to both ends, thinning mid-greys; `#1A1A1A` = `mono/4`. Keys are index
  (theme-remappable); per-step brightness in the token `$description`. In `colour.json` + canon; build green. Tuner:
  `reviews/APOLLO-MONO-GREY-CURVE-2026-07-19-v2.html`. **Grey-tint standing check** (memory `feedback-grey-tint-check`):
  surface greys (`#333`=`grey/800`, `#767676`=`grey/600`) before changing — Dave usually rules black, but confirm.
- **★ Amount-display — P1 atom BUILT + gated (2026-07-19).** Money-format primitive: currency-before-no-space
  (copy-025), tabular figures, U+2212 sign, redacted privacy state. Snippet + `amount-display.meta.json` + review;
  monochrome (directional colour deferred to the colour workstream). Added figure rungs **`.t-cm-figure-4/5/6`**
  (32/16/14, all tabular) to `canon/type.css`; atom is fully composite-bound (no raw font). COMMITTED (conductor).
- **★ Digital black `#1A1A1A` = the new `#000`** (Dave 2026-07-19) — GENERAL, not just the reverse-text halation
  case. Swept all 38 components' dark grounds + `background/default` dark → `#1A1A1A` (shadows/overlays stay pure
  `#000`). COMMITTED. Expands [[neutral-blacks]]'s conditional framing; `#1A1A1A` = `mono/4`.
- **★ R-D16 — Mono semantic greys seated on `color/mono/*` — RULED, enactment PENDING.** Dave ruled on
  `reviews/APOLLO-MONO-SEMANTIC-GREYS-2026-07-19-v1`: text ink → `mono/4 #1A1A1A` (**★ SUPERSEDES `col25-011`**
  for Mono — Grey-8 stays Legacy) · **DROP** secondary text grey (hierarchy = weight/size, "very mono") ·
  `#767676`→`mono/8 #808080` · tinted `#D7D8D6`→`mono/12 #E1E1E1` · mechanical maps approved. **Enactment
  (Sonnet, queued):** write token values + sync the 38 component declarations + regen `canon.css` + re-gate;
  annotate `col25-011`/`colour-usage.md` with the Mono override. Ledger `_proforma/_RAG-DECISIONS.md` R-D16.

- **Project name = Apollo** (renamed from *Promenaut* repo-wide 2026-07-14; "Apollo" singular
  preferred, "Apollo SDS" acceptable). History: `_DECISION-HISTORY/2026-07-14-rename-and-restructure.md`.
- **Red rule = red is the PRIMARY-action accent, used ONCE per screen** (RULED Dave 2026-07-14) —
  **NOT destructive-only.** Destructive/error takes a distinct, non-red treatment. Supersedes the
  charter §4 register-tied ceiling → now universal. `BRAND-1` gate rewritten accordingly.
  **Propagation gap (OPEN):** historical fitness-test builds + proof-001 `_GATE2-REPORT.md` still
  state the old rule — regenerate if revived. Memory `apollo-rename-and-red-rule-2026-07-14`.
- **Designer pack = shipped-ready** (2026-07-14). `designer-skills-v1/` (4 skills + built KB,
  gitignored); handover artifact **`Apollo-designer-skills.zip`**. Delivery via VS Code + Copilot
  Agent Skills; no Python for v1. Intro ~the 20th; hands-on the 24th. **Untested:** live-fire on a
  designer's machine — top release risk.
- **Working model = land to the live repo as-you-go** (RULED 2026-07-14). Deliverables write straight
  to the connected repo; the `/tmp/ux` snapshot is stale — don't trust it. GitHub Desktop CLOSED
  during Claude commits. Memory `working-model-cloud-vs-device`.
- **Repo restructured for human-readability** (2026-07-14) — root = operating essentials; visual map
  `docs/repo-map.html`. History: `_DECISION-HISTORY/2026-07-14-rename-and-restructure.md`.

- **Component library = Apollo pro-forma programme, in flight.** ONE component skeleton, N modes —
  **Apollo mono** (monochrome base; *"pro-forma" = Apollo mono*) · **Apollo UI** (branded HSBC) ·
  **Apollo SC** (prior branded — "keep the ideas, don't copy the solutions"). **FOUNDATIONAL RULING
  (Dave 2026-07-15):** no hardcoded styling — everything tokenised, sibling libraries governed by
  MODES; enforced by DEF-003 (no JS motion) + DEF-004 (no raw px) in `_build_all.py`.
  **Tranches T1–T8 built + gated** in `knowledge/_proforma/` (interactive one-file-per-tranche);
  rules live in `_PROFORMA-RULES.md` (16 rules, incl. rule 16: every component ships Swiss dossier +
  KB model doc). Reviewable build list =
  `reviews/ITINERARY-2026-07-14-apollo-component-library.{html,xlsx}` (124 items; ~50 real base gaps;
  extend-not-restart). Memory [[proforma-programme]].
  History: `_DECISION-HISTORY/2026-07-15-proforma-tranche-arc.md`.
- **TYPE-TOKEN SYSTEM = PROMOTED TO CANON + grid enforced library-wide** (2026-07-17, Dave "crack
  on"): (1) primitives → `tokens/typography.json` + composites → `tokens/typography-composites.json`,
  `type.css` settled; (2) HSBC-general incumbent type+spacing parked as sibling sets — Apollo = the
  proposed HSBC standard, governed by modes; (3) **DEF-005** grid gate wired; (4) retrofit — 230
  off-grid snaps across canon.css + 38 snippets + 9 tranches; (5) vertical-stack rule drafted;
  (6) arrow asset RETIRED; (7) DEF-005 expanded to 50 files, all PASS. Rulings + WHY in
  `knowledge/_proforma/_TYPE-DECISIONS.md`.
  History: `_DECISION-HISTORY/2026-07-17-type-token-build.md`.
- **ATOMISE — build at the true atomic level, compose up** (RULED Dave 2026-07-14). Rolled-up
  patterns are a **debt**, not the model; build atoms → molecules → organisms per the `meta.schema`
  ladder. Known debt: decompose existing rolled-up molecules later. Applies to all new work.

- **Apollo product spine = "lovable on rails" · four phases** (Dave 2026-07-17; labels provisional,
  shape is the vision). **1 · Discover** (ingest/research; chat-to-KB bot likely here) ·
  **2 · Create** (being built now; four modes: **Strict** "Factory" · **Creative** · **Component
  Dev** · **Explore**) · **3 · Craft** (the review doc + comment overlay IS this phase) ·
  **4 · Dispatch** (hand to engineering; may fold away). **The four Create modes = TIERED LEVELS OF
  ADHERENCE** to the rails, guardrails progressively removed, per-tier sub-settings. **a11y (WCAG
  2.2 AA) IS the single non-removable floor** across every mode (per FOUNDATIONAL
  `accessibility-aspiration`) — "non-removable" = LOCKED, not HARDCODED: an **admin access layer**
  tunes every setting incl. the floor. **Apollo = the MOONSHOT** (name rationale). Memory
  `apollo-product-framing`. Unaudited — a framing, not a spec.
- **Product = a *flexing* engine** — one governed core, dials per work-type; floor/churn vs
  ceiling/novel. `ADR-0006`.
- **Output modes = a first-class dial** (Dave 2026-07-05): two fidelity tiers — portable dumb-HTML
  prototypes + build-ready from a prebuilt library, with **Sutherland** *a* target, not *the*
  architecture. Two-way tie: dark-mode work feeds INTO Sutherland; the Figma library IS Sutherland's
  working file. Memories `output-modes-portability`, `sutherland-figma-mapping`. Unaudited.
- **Register = an inference ramp** (NOT a look): sober = retrieve · balanced = extend · expressive =
  invent. Charter `_FIXED-FLEX-CHARTER.md` **§9**.
- **§9a — provenance of "reads HSBC"**: brand-ness resolves to named sources; flag-where-silent is
  advisory; residual gestalt = human. Record: `knowledge/_PROVENANCE-inference-levels_2026-07-04.md`.
- **Two harness modes** (§9a): converge/ship = mode B ADOPTED · explore/noodle = mode A OPEN. Memory
  `harness-two-modes`.
- **Project memory = temporal decision-graph pattern; this file is the cold-start spine.** `ADR-0007`.
- **Supersession discipline · git split · data hygiene** — canonical in `AGENTS.md` (tombstone +
  propagation log in the same pass; Claude commits in terminal, Dave pushes via GitHub Desktop only).
- **Build** — `python3 knowledge/_build_all.py` is the one command; the gate list lives in the script
  and in `GOOD-MORNING.md` §A. (This entry previously carried a third, drifted copy of the list.)
- **State machine records FUTURE/TARGET states too** (RULED 2026-07-05, extends ADR-0007): targets
  carry what · why · blockers · source; the staleness gate must flag a target whose blockers cleared.
  **Extended 2026-07-18:** the forward half now has its own home — **`_FUTURE-STATE.md`** (side-quests,
  ideas, resurrection candidates); in-flight TARGETS stay below. Unaudited node.

## DECISION-NODE LIFECYCLE — generated from the decision graph (ADR-0007 part 2)

<!-- AUTO-DECISION-LIFECYCLE START — do NOT hand-edit between these markers.
     Generated by `knowledge/_build_live_state.py` from `knowledge/_decision-graph.json`
     (which `_build_decision_graph.py` produces from the audited seed + inscribed edges).
     To change what appears here, change the ledgers/ADRs and re-run `_build_all.py`.
     Consistency only, never validity (ADR-0007 §5): a clean ledger is not a vouched one. -->

**82 decision nodes — 67 LIVE · 6 AMENDED · 8 DEAD · 1 OPEN.** Full typed edges + what-touches-this map: `knowledge/_DECISION-GRAPH.md`.

**☠ DEAD — do not build on (8):**
- **DV:DOSSIER.chevron** · DataViz dossier chevron-on-stacked claim — superseded by DV-D04
- **DV:DOSSIER.s07** · DataViz dossier §07 one-file-per-component — superseded by DV-D01
- **R-D8** · Green/blue Band A; dark set closes — superseded by R-D9, R-D10
- **R-D13** · Light fills locked (first pass); dark reopened — superseded by R-D14
- **T-D7** · Binding mechanism: measure before ruling — superseded by T-D8
- **T-D11** · /1 batch attempted, failing, reverted — superseded by T-D12
- **TYPE:2026-07-17:composite-txt-child** · 07-17 composite with required .txt child — superseded by T-D9
- **TYPE:2026-07-18:badge-A8000B** · #A8000B badge ruling (same-day superseded) — superseded by TYPE:2026-07-18:sat-ceiling

**◐ AMENDED — live, but a specific claim is dead (6):**
- **ADR-0006** · Flexing engine product shape — dead claim(s): cool-warm-hot register framing
- **R-D1** · RAG promotion round one — dead claim(s): dark red #CC4333 as the status-fill red; the vaguer 'future legacy theme' phrasing
- **R-D2** · Background/glyph split + matting — dead claim(s): role-uniformity
- **R-D3** · Amber solved
- **R-D4** · Matting rungs + first token promotion — dead claim(s): green/blue rung values for light fills
- **R-D10** · Dark set locked — dead claim(s): fills are mode-stable

**○ OPEN / proposed (1):**
- **T-D5** · Tracking rule IF sheets survive

**✓ LIVE (67)** — in force; titles in `_DECISION-GRAPH.md` §②:
  ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0007, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0014, ADR-0015, ADR-0015-A1, B-D1, B-D2, B-D3, B-D4, B-D5, B-D6, B-D7, CHARTER.S9, DEF-003, DEF-005, DEF-006, DV-D01, DV-D02, DV-D03, DV-D04, DV-D05, DV-D06, DV-D07, DV-D08, DV-D09, DV-D10, DV-D11, DV-D12, DV-D13, R-D5, R-D6.A, R-D6.A2, R-D6.B, R-D7, R-D9, R-D11, R-D12.A, R-D12.B, R-D14, R-D15, R-D16, R-D17, R-D18, R-D19, R-D20, R-D21, T-D1, T-D2, T-D3, T-D4, T-D6, T-D8, T-D9, T-D10, T-D12, T-D13, T-D14, TYPE:2026-07-18:sat-ceiling

<!-- AUTO-DECISION-LIFECYCLE END -->

## SUPERSEDED / DEAD — do not build on

- `knowledge/_fitness-test/sme-payments-registers.html` — old looks-based register dial → superseded
  by charter §9 (2026-07-05). Tombstoned.
- Register-as-"described-look" — → superseded by §9 inference ramp (2026-07-03).
- Terminal-only push (07-02) — → superseded by the git split (07-05).
- `knowledge/_NEXT-SESSION.md` — retired → `GOOD-MORNING.md`.
- **`knowledge/_agent-memory/store/` — the memory mirror — DELETED 2026-07-18 (RULED Dave, via
  consolidation review pin 11).** It had become the third source of truth its own README forbids
  (115 stored vs 110 live, five ghosts, knowingly stale by three more). Final dated snapshot:
  **`_retired/agent-memory-snapshot-2026-07-18/`** (tombstone-bannered, non-authoritative, never
  refreshed). Capture-ritual step 3 amended: durable content is INSCRIBED properly (rules →
  guidelines/runbooks · checkable facts → assertions · rulings → ledgers), never photocopied.
  Propagation: runbook rewritten; snapshot README carries the tombstone; memory `capture-ritual`
  updated.
- **The "stale-reading pattern" spine note (07-18) — tombstoned 2026-07-18**, superseded by the
  **consult mechanism** (ruled via consolidation review pin 10): problem-domain index + pre-flight
  receipt, spec at `reviews/CONSOLIDATION-AUDIT-2026-07-18.html` §3, landing as
  `knowledge/_consult.py` + `_RUNBOOK-consult.md`. The bite-rule ("check the KB and the gates BEFORE
  designing") lives in `GOOD-MORNING.md` §A until the tool makes it mechanical.

## OPEN — propagation gaps + parked threads

### ✅ CLOSED (2026-07-19) — `gen_rules_index.py` truncation fixed
The `chunk[:500]` cap in `rule_text()` was cutting 11+ rules mid-sentence in `_RECONCILIATION.md` and making
their tails unsearchable in `_consult.py` (`icon-015` alone lost ~2300 chars). **Fix: cap removed** — the
walk-back already bounds `rule_text` to one bullet/paragraph, so full text now flows to both consumers.
Verified independently by the rules-index worker (465 rules intact, longest icon-015=2833, old-cap
fingerprint gone). Provenance comment in the generator so a cold session won't "restore" the cap. Receipt:
`notes/_receipts/2026-07-19-worker-rules-index-truncation.md`.

### ✅ CLOSED (2026-07-18) — the binding mechanism's BLAST RADIUS now has a gate
`_validate_type_blast_radius.py` (blocking, wired into `_build_all.py`) + registry
`canon/_type-bindings.json`. Bites on any UNREGISTERED / ESCAPED / UNWAIVED-BARE appended selector;
current debt registered + waived so it lands green. Full ruling + v1 limits: **T-D13** in
`_proforma/_TYPE-DECISIONS.md`. Residual DEBT to burn down (non-`/1` batch): namespace `h2` (25
files) then the scoped-element set — tracked there, not here.

### 🟠 OPEN — the non-`/1` batch, and why DEF-006 stays unwired
**61 non-`/1` font shorthands remain in `snippets/`**; the bulk of the remaining **690 TYPE-002** sit
in the pro-forma tranches, carrying line-heights 1.1–1.6 — binding REPLACES them with canon and
**things move**. Needs its own reviewed batch with T-D12's before/after pixel discipline.
**DEF-006 is 780 → 729 and stays UNWIRED until this lands** — wiring it earlier trains everyone to
ignore a red build.

### Awaiting Dave — small, no analysis needed
- ~~Matting rung for green + blue~~ — **RULED R-D4 (2026-07-18): both matted 15%** (`#2B7E4F` /
  `#306EC6`), red as-is; role tokens promoted (see LIVE → RAG). Rung came from a direct readback —
  the pin export named the hue, not the row (the overlay row-identity debt biting again).
- ~~**`{#dv-017}`(a) CONTRADICTION**~~ **RESOLVED R-D5 (2026-07-19): split the clause** — directional deltas
  red/green ONLY; RAG status a separate concern (R-D3). Enacted in `data-visualisation.md`.
- ~~**★ RAG light-mode FILLS — REOPENED (R-D11)**~~ **RESOLVED + LOCKED 2026-07-19 (R-D14).** Light green `#5DAC7B` /
  blue `#7DABCD` (H241), dark stays R-D10; per-mode proven. See LIVE → RAG. **Only open piece: the token promotion**
  (`rag/*` per-mode + rebind behind the blast-radius gate) — Sonnet-appropriate, deferred.
- **§1 RAG manifestation — OPEN.** Which forms are canon: Status-indicator dot+label (existing canon) · filled
  cell/badge · bar/edge; tags+pills EXCLUDED by canon (ctkt). Decision sheet built
  (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`), awaiting Dave's canon pick (A / A+B / A+B+C). Then a
  Sonnet build: rebind Status-indicator to R-D10, spec cell/bar as gated components (cells need more vertical padding).
- ~~**`.tag` COLLISION**~~ **RESOLVED 2026-07-18.** Was three things under one name: the tag component
  (14px), a smaller reuse (12px), and a masthead descriptor `.h .tag`. Ruled (Dave): tag atom = 3
  variants (dismissible/bordered/plain) × 2 sizes (`.tag`/`.tag--sm`), `.tag--plain` for borderless;
  colour/RAG deferred. Masthead descriptor renamed `.h .tag` → `.h .subtitle` (specimen chrome, not a
  component). Live Tags descender clip fixed via ds-005. Specimen: `reviews/TAG-COMPONENT-2026-07-18`.
  **ds-005 now GATED + CLOSED (07-19):** `_validate_descender_clip.py` (step 27/34) forces
  `text-box-edge:text text` on every truncating label; the button follow-on audit found `.btn`/`.cta`/`.qbtn`
  CLEAN (they never truncate — null result), the real debt was 7 labels in Tranche-2/3/4/7/8 + Masthead
  `.dd-title`/`.navitem-tx`, all fixed zero-waivers. Removing an override now reds the build.
- ~~**`.num` at 24px**~~ **RULED T-D14 (2026-07-19):** added `.t-cm-figure-3` (24/500) to the ramp;
  countdown numeral bound via class; build green (34 steps). Multi-size 20/24/32 lands with countdown size variants.
- **Family A (reverse on near-black), 12 decls** — held at 500. Re-specimen on a FULL dark surface.

### Gates owed — rules that exist but do not bite
- **Amber rules 1 + 2** (R-D3) · **type.css load order** · **DEF-006** (see above) · dark-mode green
  `#1AA05C` 3.37 · dark-mode red/blue as TEXT glyphs on `#111` (3.97 / 4.15).

### ⚠️ METHOD DEBT — the review overlay loses row identity
Three sheets needed three different disambiguation routes; one (RAG-MATTING) is unresolvable. **The
overlay should capture which row a comment is pinned to.** A PRODUCT fix, not a process workaround —
registered against the review-layer-as-product thread (and `_FUTURE-STATE.md` feature ideas).

- **🔴 GAP (2026-07-17, measured) — the library does NOT use the canon type ramp.** Type was promoted
  and the *grid* retrofit ran, but components were never rebound: **0 of 50** files reference a
  `.t-cm-*`/`.t-ed-*` composite; raw font declarations remain everywhere (canon.css 113, T8 43, T1
  25, T6 23…). **THE TYPE RETROFIT (sibling to the grid retrofit) — NOT STARTED:** (1) components
  link/inline `type.css`; (2) rebind every text declaration — Component for single-line, Editorial
  for wrapping prose (the N1 caveat decides); (3) snap off-ramp sizes; (4) wire
  `_validate_type_composites.py` into the build (Dave: *"we need to hard wire this"*).
  ⚠️ `canon.css` is GENERATED from snippets between the AUTO markers — edit snippets and regenerate,
  never hand-retype. Scope ≈ the grid retrofit; needs a fresh session.
- **✅ Icon SOURCE canvas normalised to 18×18** (2026-07-17, ruled option A — fix the assets, we own
  the library). Library now **652 × 18×18** + 6 deliberate non-square utility marks; build green;
  renders identical. History: `_DECISION-HISTORY/2026-07-17-type-token-build.md`.
- **🔵 SCHEDULED (Dave 2026-07-17) — ICON SCALE onto the 4px grid** (step 0 above done). Icon render
  sizes were never snapped and DEF-005's square-exemption can't see them. Measured: ~56 usages
  on-grid, **~50 OFF** (18px ×20, 14px ×14, 22px ×7, 26/34/11/15/10 tail). **The work:**
  (1) sanctioned icon scale on 4px = **12/16/20/24/32/36/40/44** (36·40·44 added by Dave — 44 = WCAG
  target-size floor); rule the mapping per off-grid size **against renders, not on paper** (Dave's
  call — optical weight); (2) **tie icon box → the type grid-slot** (icon beside a label takes the
  SAME slot — the rule that makes the scale self-evident); (3) source-artwork caveat: the ~71
  non-square assets need a `preserveAspectRatio`/pad-to-square ruling; (4) gate it — narrow DEF-005's
  exemption or add `_validate_icon_scale.py`; (5) retrofit the ~50, re-render. NOT started.

- **🟢 RULE 16 (2026-07-16) — component documentation is part of "done":** Swiss dossier in
  `reviews/` + graph-connected KB model doc in `_proforma/` (typed `relations:`). FIRM going forward.
  Exemplar: the Masthead pair. **Backlog (Dave "we might have to go back"):** retrofit docs for
  T1–T7; stand up the Swiss component catalog ("nicer Storybook") as their shared home.
- **🟡 PARKED — round-one DataViz kit BUILT + reviewed, "good enough for now", NOT signed off**
  (RULED Dave 2026-07-16). Gate-first: `_validate_dataviz.py` (9 blocking + 5 advisory) wired; whole
  kit on `knowledge/_proforma/DataViz-interactive.html`; **nine review rounds enacted** — ledger
  `knowledge/_proforma/_DATAVIZ-DECISIONS.md` (read before touching charts). **REVISIT target, not
  DONE:** Dave will add Layer-2 interaction controls (filtering, chart titles…) and finish sign-off.
  Interactivity never render-checked in a browser by Dave — needs his in-browser pass. Staleness:
  flip to DONE only on his sign-off.
- **DataViz foundations — RATIFIED + PROMOTED (2026-07-16):** method dossier ratified (semantic SVG +
  tokens + CSS motion + hidden-table spine; canvas rejected); **V7 promoted into
  `semantic-colour.json`**: `data/series/1–5` (C, mode-stable) · `data/series-high-contrast/1–5` (A,
  per-chart rebind) · `data/delta/{gain,loss,neutral,warning}` (D2, value-split pairs); **`{#dv-019}`
  recorded** (scoped gain/loss exception + the vibrating-boundaries rule, thresholds 1.25 / 135° /
  0.5 adopted advisory — quantified because Dave OBSERVED the dance on a 146° pair); suggestion
  ranges stay `proposed` in `tokens/_proposals/dataviz-ranges.proposals.json`. **NEXT = round-one kit
  revisit** per the parked entry above. Dossier: `reviews/DATAVIZ-METHOD-2026-07-16.html`.
  History (the rev 1→3 arc): `_DECISION-HISTORY/2026-07-16-dataviz-v7-arc.md`. Presentation
  candidate: see `_FUTURE-STATE.md`.
- **🟢 Masthead — SHIPPED as an MLP** (review complete, Dave "done at last", 2026-07-16; MLP status
  ruled 2026-07-18). `knowledge/_proforma/Masthead-interactive.html`: one `.masthead`, 3 recipes
  (L1 exposed · L1 + mega · Trigger mega), drill-down drawer variant, all gates green. Supersedes the
  T7 `gheader` + `mm-masthead` demos. Two provisional glyphs (`i-brand-apollo` crescent,
  `i-menu-search`) await real assets — `knowledge/_ICON-GAPS.md`. Design revisit possible later.
  History (six review rounds): `_DECISION-HISTORY/2026-07-16-masthead-rounds.md`.
- **⚠️ PROPAGATION GAP (partially closed):** `ADR-0006` + `notes/_VISION-iteration-machine_2026-07-03.html`
  still speak the OLD looks-language ("cool/warm/hot register switch"; the mock has a
  `border-radius:10px` cardinal violation). `_TEST-BRIEF-v2` §2 was reconciled 07-05; the vision doc
  + ADR-0006 remain open — do when next in that area.

- **Worked spread — DONE 2026-07-05, two instances (Sonnet + Opus re-run).** First
  retrieve/extend/invent spread; cardinal curbs held; Dave found two real gaps, fixed same session
  (canon rigour tier `.cn-*` > `.c-*`; Opus re-run). Writeups in
  `knowledge/_fitness-test/register-spread-2026-07-05*/`. Still not "proven" — one screen.
  History: `_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md`.
- **🟠 GENERATION SHAPE — RULED (Dave, 2026-07-10): rule-tuning + inference tiering LEAD; the
  double-pass is a component, not the architecture.** The two-pass restyle was "not all that
  successful" — an interesting hypothesis, no more. Future state affirmed: **strict mode over a full
  component suite for the "factory"**. The trace tool (`knowledge/_trace_knowledge_usage.py`) showed
  governed output is already PURE-RETRIEVAL — tuning must change *what the rules ask for*, not
  adherence. **ROOT CAUSE of flat layouts: the library stops at organism — ZERO templates/shells** —
  the layout-governance gap and the library-tier gap are the SAME gap ([[library-composition-tier-gap]]).
  **OPEN DECISION F7:** build-upfront vs cluster-compound. **Working plan (agreed direction):**
  housecleaning → gap-analysis targets across three tiers (templates/shells = the load-bearing zero
  tier) → prove the loop on ONE cluster → build the template tier + compose gate → scale compounding.
  Full chain + all three hypotheses: `_DECISION-HISTORY/2026-07-07-s9-root-cause-and-ruling.md` +
  `knowledge/_FINDINGS-s9-session-2026-07-07.md`. Deep review:
  `reviews/REVIEW-2026-07-10-deep-analysis_rev2.html`. Memory [[ruling-generation-shape-2026-07-10]].
  **RESURRECT:** the experiment lineage is future evaluation material once the factory has all its
  parts (Dave, 2026-07-18) — registered in `_FUTURE-STATE.md`.
- **Named-not-built harness machinery** (§9/§9a): isolated generation · divergence probe (formal
  tooling) · mode-B brand self-check · the mode dial.
- **PM-KG MVP** (`ADR-0007`): `_build_live_state.py` + the staleness gate + `_capture_gate.py` — own
  focused session.
- **✅ Decision-corpus audit — TIER A CLEAN 2026-07-05** (ADR-0007 §5; method
  `_RUNBOOK-decision-audit.md`; ledger `_DECISION-AUDIT.md` — per-batch verdicts live there).
  Milestone: every Tier A node has a verdict — retires the "everything is unaudited" risk for
  foundational nodes. **Standing follow-ups:** §9 proof-obligation · ADR-0003 KG/ingestion · §4
  language-strip · TOV content audit · harness-modes exploration · re-audit the two amended nodes
  (ADR-0006, `derivation-governance` — amended text re-enters `unaudited`) · staged-promotion /
  extension-library process (direction VOUCHED, mechanism DEFERRED; tiered-access feature idea →
  `_FUTURE-STATE.md`). Next: Tier B opportunistically, Tier C by sample/on-touch. Never in a loaded
  session.
- **⭐ Harness modes + dials exploration** (from the 07-05 defer): flexible to a degree — clean
  switch or toggle + advanced mode, maybe "let it rip"; **finding the use cases is the important
  part**; research + iterate, start small. Own thread. Memory `harness-two-modes`.
- **⭐ TOV = digital-editorial spin-off + future content audit** (§4b defer): genuinely useful for
  DIGITAL EDITORIAL — candidate spin-off; for interfaces NOT a priority except neutral decisions
  (labelling, locale, formality). Memory `tone-of-voice-ingest`.
- **⭐ Charter §4 language-strip (HARD follow-up):** strip §4's interpretive prose
  (recall-by-adjective), leaving the four curbs as KG-sourced derivations — **do inside the
  unified-KG/ingestion thread, not standalone.** Amended text re-enters `unaudited`.
- **⭐ Unified DS knowledge-graph + ingestion, done right** (from ADR-0003 defer). The whole corpus is
  one interlinked graph; today that lives only in the compliance index. **Design direction (Dave,
  2026-07-10):** the compliance "KG" is an inverted index, fine for its job, wrong for the roadmap.
  When taken up: (1) **NOT GraphRAG** — overlay/property graph over existing stores, edge layer
  derived + regenerable, no monolith; (2) granularity = typed EDGES, not finer text (split only
  bundled rules — ACT atomic-vs-composite); (3) **import** the SC↔rule leg (ACT Rules Format 1.1 +
  axe-core metadata), hand-curate only component↔SC (our genuine novelty); (4) type edges
  `applies_to` vs `verified_by` — the queryable form of "enforced vs asserted"; (5) keep structural
  graph separate from advisory retrieval-over-prose. **Sequencing:** rides with the layout/library
  tier (R4) + Ingestion Phase 3 — not standalone infra. Cheap-now slice: type existing edges + import
  ACT. Memory `ds-knowledge-graph-revisit`. Unaudited.
- **Seaworthiness plan — DONE 2026-07-05** → `notes/_SEAWORTHINESS-PLAN_2026-07-05.md` (the
  dependency-aware sequence; partly overtaken by the pro-forma pivot). Phase 0 ingestion-tracking
  hygiene CLOSED same date. History: `_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md`.
- **D2 — novel-screen test — THE #1 unlock.** Waiting on a colleague's brief (their brief-v2 + own
  baseline + signed contract *before* generation). `notes/_TEST-PLAN-novel-screen-proof.md`.
- **Toolkit tranche 2** (Dropdowns ×4) — parallel cheap-model workstream. Memory
  `common-toolkit-survey`.

## PLANNED / TARGET STATES — in-flight targets (per the ADR-0007 extension)

*Intended end-states with a path. Ideas not yet in flight live in **`_FUTURE-STATE.md`**.*

- **🎯 Full consolidated review page (Apollo Mono baseline)** — Dave reviews the whole Mono baseline in **ONE
  big review page when the build-out is "done"**, not piecemeal (*"I just need to get this nailed"*, 2026-07-19).
  Running backlog + method: `knowledge/_REVIEW-SIGNOFF.md` top block. Covers T1–T9 as they render post-tokenise,
  the tokenise deltas (divider `#3A3A3A→#808080` · blue focus · near-white primary), and the open decisions
  (mono primary-action token · success mono-vs-teal · focus blue-vs-mono) + DataViz sign-off + T9 first review.
  Memory `full-review-pending`.

- **🎯 Gates-as-a-service → close the agentic loop** (Dave 2026-07-14). Expose Apollo's validators as
  callable tools (MCP) so a host agent runs them mid-task (generate → check → fix → re-check) — the
  verifier is the expensive, differentiated half, already built. Removes the per-designer Python
  blocker. *Honesty:* the repair loop is not built; gates verify DECLARED obligations only. Memory
  `agentic-loop-gates-as-service`. Unaudited.
- **🎯 Chat-to-the-KB bot** (Dave 2026-07-17). Conversational agent over the Apollo KB (canon ·
  criteria · rulings · decision graph) for designers/devs/stakeholders. Open: retrieval grounding +
  citations, scope, surface, guardrails. **The consult index (2026-07-18) is its seed — same index,
  read side built once, used twice.** Memory `chat-to-kb-bot`. Unaudited.
- **🎯 Ingestion "done right"** — full detail: `knowledge/_INGESTION-ASSESSMENT_2026-07-05.md`
  (cockroach doc). Target: every ingested entity addressable in one overlay graph; tokens
  Sutherland-canonical, 147 deprecates retired; completeness = edge coverage. Sutherland export is NO
  LONGER a blocker (arrived 06-17). Path: Phase 1 token migration → Phase 2 finish guidelines →
  Phase 3 overlay graph (= the 07-10 KG design direction above) → Phase 4 wire coverage into this
  machine.

## SPIN-OFF / GENERALISABLE CANDIDATES — surface, don't bury (Dave, 2026-07-05)

*Tools/methods that may generalise — treat like company spin-offs. Surface mid-chat; don't force it.
Memory `spin-off-candidates`. Sibling register for ideas/side-quests: `_FUTURE-STATE.md`.*

- **🌱 The state machine** (`_LIVE-STATE` + `_FUTURE-STATE` + `_DECISION-HISTORY` + decision-audit
  method) — **Dave's first named candidate.** A portable "how a long-running agent project retains
  state, records supersession, and audits its own decisions" kit.
- **🌱 The FONT AUDIT instrument** (2026-07-18, `reviews/gen_univers_dossier.py` + fontTools passes):
  answers "is this face tight or loose relative to its own stroke weight; is our commissioned cut
  actually stock?" with numbers. Settled in ten minutes a weeks-open question and relocated a defect
  to the foundry (ds-004). Unruled; embedded in a dossier generator, would need extracting.
- **🌱 REAL-FONT EMBEDDING for review sheets** (2026-07-18, `embed_fonts()` in
  `gen_tracking_contact_sheet.py`): base64 woff2 inlining so specimens render in the brand face
  anywhere. Retired the "judge on your screen" caveat. **Candidate to fold into `_make_review.py`.**
- Other candidates (unruled): decision-audit runbook · fixed/flex charter pattern ·
  ingestion→overlay-KG method · review-dossier language-review instrument ·
  verification=enforcement gate-tiering · the cockroach-doc pattern. Precedent:
  `digital-experience-transformation`, `graphify-tool`.

- **Capture ritual** — canonical at `knowledge/_RUNBOOK-capture-ritual.md`; run every session, no
  exceptions. The enforcing `_capture_gate.py` is deferred to the PM-KG MVP.
