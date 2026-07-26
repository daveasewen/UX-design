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

## ⏱ LATEST DELTA — 2026-07-26 (Sun evening, OPUS solo self-conducting — ★ THE CAP FORK RULED + the legend model ENACTED on its first member; build 55/55 GREEN, verify 27/27; 🔴 RED ~72% wrap) — "Opened to enact DV-D11/12/13 and hit a wall in the first ten minutes: dv-behaviour.js had 858 bytes of headroom and the model needs ~14,100. Dave ruled the deferred cap fork (§C·2 #18) — SPLIT the source AND re-scope the gate to a per-page budget — then ruled incremental migration. Chart-donut now runs the real model; bar, combo and line follow."

- **★ THE 16KB CAP FORK — RULED (§C·2 #18 CLOSED).** Measured three ways before asking: one file would land at 26,615 B as-written · 22,364 B comment-stripped · 21,327 B even with DV-D12 abandoned. None passed. Dave ruled **split AND re-scope**: `canon/dv-legend.js` joins as a second registered `$behaviour` source, the 16KB per-source cap is renamed to a LEGIBILITY constraint, and a **32KB per-GROUP PAGE budget** (`check_group`/`PAGE_BYTES`) is added so splitting can never buy headroom. Inscribed as **ADR-0015 § Amendment (2026-07-26)**, both beats. WHY/HOW: `_DECISION-HISTORY/2026-07-26-behaviour-cap-fork-and-legend-enactment.md`.
- **★ SAME DEFECT FOUND TWICE:** the "exactly ONE rAF-debounced resize listener" check was also per-source and would have failed dv-legend for carrying ZERO — correct for a source with nothing to reflow. Moved to group level under the same ruling. Gate ships **5 new selftest bites**, including the evasion case (two sources each under 16KB, together over 32KB). Selftest OK.
- **★ MINIFICATION ASKED + DECLINED (Dave, mid-build).** Numbers are real — 28,332 B raw → **9,622 B gzipped**, free at transport — but the cap is a COMPLEXITY forcing function, and minifying shrinks the number without simplifying the thing while letting source sprawl read green. Reference snippets carry the injected block inline and must stay readable; comments are the provenance trail; a minifier adds version-drift to a byte-exact `--check`. Wire-weight belongs in the ADR-0008 adapter layer. Reasoning recorded in the ADR amendment (Rejected, with reasons).
- **★ Chart-donut MIGRATED — the exemplar.** Dual-gesture rows (swatch `role=checkbox` OUTSIDE the isolate label button), typed tips (`data-tip-value`/`data-tip-percent`), sr-only live region, Reset canon-disabled (B-D4). **Verified 27/27** by `knowledge/_verify_dv_legend.js` — the REAL source driven against the REAL snippet in jsdom, incl. Dave's signed-off figures (isolate Housing 950/41%, +Savings 1250/54%), the "nothing ever hides" invariant, additive isolate, the 24%/12% ladder, and rest-to-rest sweep landing exactly on baked geometry.
- **★ TWO MISSES IN THE HANDOFF'S DIVVY, found by grep not by assumption:** (1) **the wave is FOUR members, not three** — `Chart-line` carries a legend (3 rows) and was in no lane; (2) **`.lg` COLLIDES with canon's `.seg.lg`** ("legend" vs "large") — the blast-radius gate caught it on first build; family renamed **`.dv-leg*`**. State classes `.is-ghost`/`.is-faded`/`.is-peek` KEPT — DV-D11 inscribes them verbatim.
- **★ TRANSITIONAL COEXISTENCE (Dave ruled incremental).** The two models are **selector-disjoint** (`button[data-series-toggle]` vs `.dv-legrow`), so members migrate one at a time with every commit working. The old block sits behind a marked TRANSITIONAL header with an executable end condition (`grep -l data-series-toggle knowledge/snippets/Chart-*.reference.html` returns nothing). `dv-legend`'s universal contract is **empty BY DESIGN** meanwhile, hooks riding each migrated member's extraContract, with the promotion instruction written in.
- **⚠ GATES BIT THE RESURRECTED WORK, as the rule says they should:** the signed-off v5.5 CSS failed DEF-005 (`padding:5px 9px`) and the radius gate (`border-radius:2px`). Corrected to **4px/8px** + `var(--border-radius-default)`. **Two small visual deltas from what Dave signed off — flagged for his eye, registered in `_REVIEW-SIGNOFF.md`, not buried.**
- **Build/verify:** `_build_all.py` **55/55 GREEN**; behaviour gate reports per-source 12,682 + 15,650 and page budget **31,268 B (95%)** during transition, **28,332 B (86%)** once the transitional block goes. Library 67. Seed fed (82 nodes / 146 edges).
- **⬛ OPEN, flagged not decided:** (a) `Chart-sparkline` now carries an **inert 15.6KB payload** — injection is group-wide and the registry has no per-member behaviour opt-in; (b) **page budget already at 86%** — the next behaviour addition faces this same fork, by design; (c) `_verify_dv_legend.js` is **unwired** (needs jsdom, not a build dependency) — wire as advisory or vendor?; (d) **graph `--verify` drift**: 5 seed edges unmatched incl. this session's 2 — the parser has **no convention for an ADR AMENDMENT carrying its own node**. Logged, not fudged.
- **🔴 Gauge at authoring: RED ~72% (in-head tally, ESTIMATE ±15%).** ⇒ **NEXT READER RE-VERIFY before building on this:** re-run `_build_all.py` + `node knowledge/_verify_dv_legend.js`, and spot-check the byte figures above.
- **OPEN → NEXT WINDOW:** migrate **Chart-bar** (+ **ds-010**: kill `fill:var(--sc,…)` at `Chart-bar.reference.html:102`), **Chart-combo** (+ DV-D10 axis-proximate lockups), **Chart-line**. Donut is the copy-source. On the last one: delete the transitional block, promote `class="dv-legrow` to the universal contract, drop it from the four extraContracts, re-run the gate (page budget should fall to 86%).

## ⏱ PRIOR DELTA — 2026-07-26 (Sun evening, FABLE solo — ★ LEGEND v5.x SIGNED OFF: v5.4 additive isolate + v5.5 seg coherence BUILT + render-verified → DV-D11/12/13 INSCRIBED + seed fed, build 55/55 GREEN; 🟢 wrap ~35%) — "Opened on the v5.3 defaults; Dave reversed (a) (checkbox now ghosts, nothing ever fully disappears) and re-specced isolate as an ADDITIVE FOCUS MODE; two versioned builds later he signed off v5.5 as the legend model and the three models are inscribed. Next window = the donut+bar+combo wave enacts them into dv-behaviour.js."

- **★ RE-VERIFY FIRST (Amber-authored prior handoff):** cold `_build_all.py` → **55/55 GREEN** (count grew 53→55 with the Memento-lane gate steps — expected); v5.3 claims spot-checked (ghost 12% · hover 24% · `paint(id,level)` · JS `--check` clean) — **held**.
- **★ v5.4 — ADDITIVE ISOLATE (Dave's retune of both v5.3 defaults):** checkbox now ghosts to **12%, not 0%** — TWO render levels only (the three-level ladder is DEAD, both beats in DV-D11); isolate = **additive focus set** (Dave verbatim: *"On isolate mode the checkboxes should be blank, with a border, and the check should add segments in this mode"*) — enter blanks the other boxes, checking ADDS at full; `visible[]` untouched during isolate ⇒ release restores the prior mix by construction; **hover fires in BOTH modes** ("let's try 1") — active-row hover fades other actives to 24%, ghost-row hover **PEEKS** at 24% (`.is-peek`, after `.is-ghost`). **Render-verified 14/14 numeric interaction checks** (opacities + aria states asserted), real HSBC cut, PNGs read.
- **★ v5.5 — SEG NUMERIC COHERENCE (Dave: the seg only changing the centre figure was confusing):** tooltip carries **ONLY the seg-selected number-type** (`data-tip-value`/`data-tip-percent` rewrite; dv-behaviour reads `data-tip` live — no canon re-wire) + the **centre figure follows the LEGEND selection** (isolate Housing → 950/41% · +Savings → 1250/54% · uncheck Other → 1930/83%; percent = share of the grand total). **14/14 render-verified.** ⚠ `aria-label`s keep BOTH forms (deliberate, DV-D13 — confirm at the wave's a11y pass).
- **★ SIGNED OFF + INSCRIBED SAME HOUR (Dave: "good done, love this" on v5.5):** **DV-D11** (legend model, incl. the v5.3→v5.4 reversal inscribed both-beats) · **DV-D12** (trapezoidal sweep easing keyed to segment spans, from v5.2) · **DV-D13** (typed tooltip + selection-following centre) → `_proforma/_DATAVIZ-DECISIONS.md`; **seed fed 81 nodes / 138 edges**, graph regenerated (66 LIVE); `_REVIEW-SIGNOFF.md` legend strand **✅ LOCKED**. WHY/HOW: `_DECISION-HISTORY/2026-07-26-legend-signoff-additive-isolate.md`.
- **OPEN → NEXT WINDOW: the donut+bar+combo WAVE** enacts DV-D11/12/13 into `dv-behaviour.js` + the chart snippets (divvy plan in `GOOD-MORNING`). Riding the wave: **ds-010** (bar `--sc` fill, bar lane) · the DV-D13 aria asymmetry · the DV-D11 seed-uncheck edge. **Hit-area rule + gate rebuild still pending Dave** (separate sign-off, `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`).
- **Build/commit:** only review + record surfaces changed (NO canon/token/snippet edits) → build **55/55**, library **67**. Render env re-staged on the shared mount per `_RUNBOOK-render-verify.md`; two new potholes banked in the dossier §5 (FONTCONFIG_FILE replaces not merges · dv-tip rides pointermove/focusin, test via focus()).
- **🟢 Gauge at authoring: GREEN ~35% (in-head tally, ESTIMATE ±15%).** Clean-budget wrap; full capture ritual this turn.

## ⏱ PRIOR DELTA — 2026-07-25 (Sat night, OPUS solo — Red-handoff re-verified GREEN → donut sweep easing restored (v5.2) + two-step fade redesign (v5.3); both REVIEW CANDIDATES; 🟡 AMBER ~55% wrap at Dave's call) — "Opened as the v5.1 sign-off; became prototype tuning at Dave's direction. Re-verified the Red-authored prior handoff first (`_build_all.py` 53/53 GREEN, claims held), then made two Dave-driven interaction changes, each versioned no-overwrite: v5.2 restored the donut sweep easing that the v3→v5.1 rebuild had silently flattened to linear; v5.3 reworked the fade into two steps. Nothing inscribed — Dave has more changes coming; next window continues on v5.3."

- **★ RED HANDOFF RE-VERIFIED (first action, per the Red-scrutiny rule):** ran `python3 knowledge/_build_all.py` cold → **53/53 GREEN** (a11y · dataviz · integrity all pass). The prior session's "landed" claims (v5.1 bar-key rise, hit-area canon patch) hold. Library still **67**.
- **★ v5.2 — DONUT SWEEP EASING RESTORED — `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.2.html`.** Dave flagged a lost finesse: the radial-sweep intro should ease-IN across the first segment, run LINEAR through the middle, ease-OUT across the last. On-disk v3→v5.1 was plain **linear** (`ang = start+(end−start)·p`) — the finesse dropped in a rebuild. Restored in `sweepDonut` as a **trapezoidal angular-velocity profile keyed to segment spans**: `V=(S+w1+wN)/dur`; accel covers exactly segment-1's width, decel exactly the last's, constant cruise between. ⚠ The real donut's **segment A is 147°** (41% of the circle) → the ease-in is a long ~441ms ramp (>half the 850ms); Dave to judge if that reads sluggish (one-line tunable). **Verified numerically** (node): ang@0=start · ang@dur=end · monotonic · endpoint velocity ≈0 · cruise velocity flat =V. JS `--check` clean. Self-contained rAF (canon-independent).
- **★ v5.3 — TWO-STEP FADE — `reviews/…-v5.3.html` (Dave's ruling).** Hover fade **.18→.24**; ISOLATE now **ghosts the non-focused series to 12%** (`.is-ghost`) instead of hiding them at 0%. To do it cleanly, **isolate became its OWN state layer** (`isolated` var) separate from the checkbox `visible[]` flags → **three render levels: full / ghost(12%) / gone(0%, checkbox-removed)** via a new `paint(id,level)`. Hover suppressed while isolated (isolate owns the dimming); touching a swatch exits isolate mode. **Logic sim 12/12 PASS** (full/ghost/gone truth table across isolate·release·checkbox·reset·guards); JS `--check` clean; CSS levels confirmed present.
- **⬛ TWO DESIGN DEFAULTS — PENDING DAVE'S CONFIRM (I chose, flagged, vetoable):** (a) the **swatch checkbox still fully removes** (0%) — only isolate ghosts to 12% (remove ≠ focus); (b) while isolated **hover doesn't stack**, and **any swatch toggle exits isolate**. Confirm or retune next window.
- **Versions (no-overwrite):** v5.1 (canon-patch baseline) · v5.2 (+sweep) · v5.3 (+two-step fade) all on disk, intact — each carries ONE described delta so Dave can attribute each change.
- **Build/commit:** NO canon/token/snippet edits → build stays **53/53**, library **67**. The start-of-session verify build regenerated `_ADVISORY-SIGNALS.md` + `_LIVE-STATE-CHECK.md` with the known stable-sort wobble (noise) → **restored in place** (sandbox delete-guard blocks `git checkout`; used `git show HEAD:… > …`). Commit = v5.2 + v5.3 + this spine + `GOOD-MORNING` + `_GM-ARCHIVE` roll. Dave pushes via GitHub Desktop (whole stack, incl. the still-unpushed prior stack).
- **🟡 Gauge at authoring: AMBER ~55% (in-head tally, ESTIMATE ±15% — Half-2 broken).** Deliberate wrap at Dave's call (more changes coming). Heat is front-loaded from orientation reads (the ~25k-token `_LIVE-STATE` page + `GOOD-MORNING`); the three iterations since were light.
- **OPEN for the next window:** Dave's next batch of changes on v5.3 → then v5.x SIGN-OFF → inscribe the legend model + the **sweep-easing spec** + the **two-step-fade model** to `_DATAVIZ-DECISIONS`/ADR → the donut+bar+combo wave bakes them into `dv-behaviour.js` (not linear / one-step again).

## ⏱ OLDER DELTAS — rolled to `_LIVE-STATE-ARCHIVE.md` (P1, ruled 2026-07-26)
Verbatim, newest-first, nothing deleted — exact sibling of `_GM-ARCHIVE.md`. Roll rule: this file keeps **LATEST + 2 PRIOR** deltas; the capture ritual rolls the rest (see `knowledge/_RUNBOOK-capture-ritual.md`, step 2d).

> **SPINE DISCIPLINE (ruled 2026-07-18, Fable consolidation session — supersedes the "1044 lines"
> banner):** state lines live here; **narrative longer than ~10 lines goes to `_DECISION-HISTORY/` at
> write time, in the same pass.** Split entries end `History: _DECISION-HISTORY/<file>`. Advisory
> tripwire ~500 lines. Edits to this file are reachability-relevant — run
> `python3 knowledge/_validate_standing_instructions.py` (STAND-002) after touching it.

*Last refreshed: **2026-07-26 ~20:05 BST (from `date`) — "CAP FORK RULED (ADR-0015 § Amendment): dv-legend.js split out + per-group 32KB PAGE budget; Chart-donut migrated to DV-D11/12/13, verify 27/27, build 55/55 GREEN; bar/combo/line to follow behind a selector-disjoint transitional block" (OPUS solo self-conducting, main queue)** · Previous: **2026-07-26 (~19:21 BST, from `date`) — "LEGEND v5.x SIGNED OFF (v5.4 additive isolate + v5.5 seg coherence) → DV-D11/12/13 inscribed + seed fed + register LOCKED" (FABLE solo)** · Previous: **2026-07-26 (~18:19 BST) — "MEMENTO LANE ONLY (weekly-run session): second dream pass RUN + RULED same session" (FABLE conductor + 2 Opus workers)** · Older refresh chain → `_LIVE-STATE-ARCHIVE.md`.*
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
