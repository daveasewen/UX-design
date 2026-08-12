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

*Last refreshed: 2026-08-12 (Wed from `date` — **#164 wrap**: FABLE conductor + TWO OPUS build subs + this OPUS wrap sub, Dave live, **ONE RULING, DAVE'S — AND THE FINDING IS A GATE THAT COULD NOT RUN**. ⛔→✅ **`_build_all.py` HAS BEEN DYING BEFORE STEP 1 SINCE #158** — the two **help-gate STEPS added at #158** had **NO `ROUTE_ROWS` rows**, so the first route lookup aborted the build above step 1; two `ABORT` rows added (**`3ef22c7`**) and the build then reached **step 13**. ⛔ **CONSEQUENCE: STEP 13's PROVENANCE GATE HAS NOT RUN FOR FIVE SESSIONS — `_governs.py --selftest` RED, 15 REAL FAILS** on rulings **`s157-D1`…`s163-D1`** in `knowledge/_rulings.json` (missing `governs`/`evidence`/`status`, or prose evidence with no `chat #N`/`commit` pointer), **re-driven by this sub, not relayed**. ★ **instrument-without-a-consumer: the gate did not fail because it could not run.** ⛔ **NOT FIXED HERE — authoring those values is inventing provenance; Dave-side, target Friday 2026-08-14.** ✅ **A 16th FAIL WAS A FALSE POSITIVE, FIXED AT SOURCE:** `PATHISH_RE` truncated dotted stems (`Tooltip.reference.html` → `.reference`), fixture-driven fix, **16 → 15** (`3ef22c7`). ✅ **SHOWROOM RE-SYNCED** — 6 pages stale since the #158 banner/badge-ink enactment; `gen_showroom.py --check` **rc=0, 75 pages + index**, re-driven here. ✅ **THREE BRIEFS INSCRIBED *AND PUSHED*:** borrowed-instruments **v1+v2** (`434c455`, **RULED-TO-EXPLORE**, enactment **parked for Friday**, five Dave-gates open) and the **progress dashboard** (`7543b48`) — **RULED A PRIORITY BY DAVE**: *"this is a priority after the side quest, it will really help me"*, build **2026-08-13** after his sidequest, **Mono components + the `swiss-design-system` aesthetic**, panels his eye. ✅ **42-VERDICT CONTROLLER BUILT + RENDER-VERIFIED** — `reviews/pri-hover-verdicts-42-v1.html`: 42 cards · 0 console errors · live hover · localStorage · export well-formed · **zero pre-selected inputs**. ⚠ **SCOPE DECLARED: the 42 are the WHOLE #139 token-fork ledger, of which `--pri-hover` is ONE card — the filename undersells it; ⛔ NOT renamed (Dave's), queued in `knowledge/_REVIEW-SIGNOFF.md`.** ⛔ **MSGFILE-PREFIX CLASS, INSTANCE 9** — `ac5ecac` carried a DOUBLED prefix, amended from a FRESH `printf` msgfile before push. ⚠ **T2 DECLARED, NOT FIXED:** `selftest_growth` **CRASHES** instead of failing NAMED without `tiktoken` (`_capture_gate.py:5307`) — crash-vs-named-FAIL is **unruled**. ⚠ **T3:** sandbox disk ~full; session-suffixed `--target` recipe stands, **no runbook amended**. ⚙ **DELEGATION:** Dave — **use OPUS subs liberally, quota is plentiful**; binding budget **NAMED: QUOTA for the subs, FILL in-window**; ⛔ no Sonnet subs. ⚙ **GAUGE: NOT MEASURED BY THIS SUB AND NOT RELAYED — no figure was handed over, so NONE is inscribed; an UNKNOWN is never defaulted.** ⛔ **THIS WRAP RULED NOTHING** — no provenance value authored, no verdict picked or reordered, no file renamed, T2's design untouched, **no ruling id minted for the dashboard priority** (promotion is Dave's alone); every G-item, LEGACY item, icon warn, declared hole, palette value, non-mono fork, the CI blocking flip, the `_gen_titles.py` exception and every `_FUTURE-STATE.md` priority are **his and untouched**; **no ratified stratum trimmed — ADD, never trim**; MEMORY step 3 is the conductor's (**SKIP declared**); `_build_all.py` **NOT RUN by this wrap**. ⛔ **THE WRAP COMMIT IS LOCAL — NOT PUSHED.** Dossier: `_DECISION-HISTORY/2026-08-12-164-the-gate-that-could-not-run.md`.)*  *Last refreshed: 2026-08-12 (Wed from `date` — **#163 wrap**: FABLE conductor + this OPUS wrap sub, Dave live, **ONE RULING, DAVE'S — G18 CLOSED BY FLIPPING A PROVISIONAL WARN TO BLOCK**. ✅ **`s163-D1`: `retired_unit_prose_audit` FLIPPED TO BLOCK** — superseding `s161-D2`'s provisional WARN **through its own close condition** (*"Dave confirms warn as final or flips to block"*); Dave picked **"Flip to block (Recommended)"** from a staged choice after read-back. ✅ **ENACTED IN THE SAME WINDOW, all three legs read off disk here:** (1) the **`duct tape` homonym fixed in `RETIRED_PROSE_WORDS_RE`** with `(?<!duct )(?<!duct-)` lookbehinds — **word-sense only, no unit prose exempted** (the #84-named regex defect, **2 of the 5 live hits**); (2) the **remaining 3 hits cleared BY DECLARATION, never by rephrasing** — `knowledge/_BANKRUPTCY-ARCHIVE.md` #87 batch (historical marker) and `knowledge/_DS-IMPROVEMENTS.md` **ds-021** (SUPERSEDED marker — the **#84-named true positive**, 2 hits); (3) the audit **WIRED BLOCKING** in `_capture_gate.py`'s md sweep, with a comment block recording **the discharge of both #84 parking conditions** — ending 79 sessions of parked/unwired state. ✅ **VERIFICATION RE-DRIVEN BY THIS SUB, NOT RELAYED:** planted hit ⇒ **1 FAIL**, removed ⇒ **0**; the **`duct tape`/`duct-tape` control EXEMPT in both runs**; `selftest_retired_unit_prose()` **PASS (empty failure list)**; **live tree 0 fails / 0 warns**; `_capture_gate.py --wrap` **rc=0 — 121 in scope · 0 fail · 15 warn**, run BEFORE any edit. ✅ **RECORD:** `knowledge/_rulings.json` **129 → 130** (tail `s163-D1`, **re-parsed here**); `knowledge/_state.json` **G18 → `done`** with a `closed_by` receipt naming the ruling. ⚠ **SCOPE CARRIED UNSOFTENED:** the audit catches **STALE INDEXES, not FALSE CLAIMS**; the retired **percentage band is OUT OF SCOPE pending ds-023**; **the cross-instrument claim check remains the open successor — DAVE'S**. ⚙ **GAUGE (relayed by the conductor, not re-measured here):** boot **55,309** real, inside the **54,859 ±1,178** band — a datapoint, never corrected into the constant; **FILL at wrap-open ~111,310** vs stop **150,929** ⇒ the wrap opened **EARLY, ~39.6K of room against a 42–49K price**. Delegation: **this OPUS wrap sub only**, binding budget **NAMED: QUOTA for the sub**; ⛔ no Sonnet subs. ⚠ **ENOSPC: NO NEW FACT** — the `--target /var/tmp/pylibs-s163w` recipe held first time and no ENOSPC was observed, so ⛔ **no runbook amended**. ⛔ **THIS WRAP RULED NOTHING** — `s163-D1` is **DAVE'S**; **no close condition invented for anything**; every remaining G-item and LEGACY close condition, the 19 LEGACY unconditioned items, the 32 icon warns and 15 declared holes, `_graph-mark-observations.jsonl` policy, palette values, non-mono forks, promotions, the CI blocking flip, the `_gen_titles.py` write-gate exception, the cross-instrument claim check successor and every `_FUTURE-STATE.md` priority are **his and untouched**; **no ratified stratum trimmed — ADD, never trim**; MEMORY step 3 is the conductor's (**SKIP declared**); `_build_all.py` **NOT RUN**. ⛔ **THE WRAP COMMIT IS LOCAL — NOT PUSHED.** Dossier: `_DECISION-HISTORY/2026-08-12-163-the-provisional-warn-that-closed-through-its-own-condition.md`.)*  *Last refreshed: 2026-08-12 (Wed from `date` — **#162 wrap**: FABLE conductor + this OPUS wrap sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES THE WAVE**. ✅ **`s162-D1`: `tooltip.tip` (enum `top|bottom`, default `top`) RULED `no-bind:structural-param`, class C11 — ON SIGHT**, off `reviews/REVIEW-tooltip-tip-s162.html` (both edges, light + dark, snippet CSS verbatim) plus the finding that **the reviewed snippet is SPACE-AWARE and flips at runtime**. Dave verbatim: ***"so yes, the tooltip should flip if there is no space to display it in the same way as it moves from the edge to accommodate the message"*** → after read-back ***"this a behavior that will be constant across all themes, i don't think this needs tokenizing"***; ★ **read-back confirmed BEFORE recording**. ✅ **THE `s142-D1` WAVE IS CLOSED 114/114** — `knowledge/_rulings.json` **128 → 129** (tail `s162-D1`, **re-parsed here**), `knowledge/components/tooltip.meta.json`'s `tip` row gained its **`$status`**, read back off disk. ✅ **GATES RE-DRIVEN, NOT RELAYED:** `_validate_snippets.py` **rc=0 (75/0)** · `_validate_binds_resolve.py` **rc=0** (75 snippets · 958 vars · 102 binds addresses · 75/75 canon blocks · 0 fails) · `_validate_palette_tier.py` **rc=0**. ✅ **COMMITTED *AND PUSHED ON DAVE'S WORD* — `0fa5f8f`**, tree clean after push. ⛔ **MSGFILE-PREFIX CLASS INSTANCE 8:** the first T3 invocation **REFUSED** (`--all-dirty` missing) and the retry **reused the MUTATED msgfile** ⇒ doubled prefix (`6e0ed57`), amended clean from a fresh `printf` while unpushed — ★ **a refused invocation is still an invocation**; hook corrected by the conductor, ⛔ this sub did not touch `MEMORY.md`. ⚠ **A CARRIED REPO-STATE CLAIM WAS STALE:** #161's *"wraps `6726a2a`+`ee091ef` NOT pushed"* — the remote already had them (ahead-count **1** pre-commit); recorded as a measurement, **no gate invented**. ⚠ **ENOSPC n=7 RE-MEASURED:** `/` at **97%**, `rm` still blocked for foreign-owned `/var/tmp` dirs; the #161 `--target /var/tmp/pylibs-s162` recipe **held** — ⛔ **no runbook amendment, n=7 added no new fact**. ⬛ **G18 EXPLAINED, NOT RULED — HIS:** 5 live hits measured, flip-to-block RECOMMENDED, **no ruling taken**. ⛔ **THE WAVE'S VALUE-LEVEL AESTHETIC LEG REMAINS UNPROVEN** — only **tooltip** was rendered; the other 113 rows are unseen and only Dave's eye can close them. ⚙ **GAUGE (relayed):** boot **55,337** real, inside the **54,859 ±1,178** band — a datapoint, never corrected into the constant; **FILL at wrap-open 141,920** vs stop **150,929** ⇒ **the wrap opened LATE, ~9K of room against a 42–49K price — declared, not smoothed**. Delegation: **this OPUS wrap sub only**, binding budget **NAMED: QUOTA for the sub**; ⛔ no Sonnet subs. ⛔ **THIS WRAP RULED NOTHING** — no close condition invented for any G-item or LEGACY item; G18, the 19 LEGACY unconditioned items, the icon warns and declared holes, `_graph-mark-observations.jsonl` policy, palette values, non-mono forks, promotions, the CI blocking flip and every `_FUTURE-STATE.md` priority are **his and untouched**; **no ratified stratum trimmed — ADD, never trim**; MEMORY step 3 is the conductor's (**SKIP declared**); `_build_all.py` **NOT RUN**. ⚠ **THE WRAP COMMIT IS LOCAL — NOT PUSHED.** Dossier: `_DECISION-HISTORY/2026-08-12-162-the-last-unruled-row-and-the-flip-that-was-already-there.md`.)*    *Last refreshed (#161 and earlier, rolled #164 — 2d boundary): full text moved to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-12 #164, § Rolled 2026-08-12 #163, § Rolled 2026-08-12 #162, § Rolled 2026-08-12 #161, § Rolled 2026-08-12 #160, § Rolled 2026-08-12 #159, § Rolled 2026-08-12 #158, § Rolled 2026-08-12 #157 and § Rolled 2026-08-11 #156.*
*(⚠ **MOVED INTO THE HEADER ZONE, #35.** The wrap gate's `"Last refreshed" is not today` check reads only the first 40 lines — where this line did not live. It had been passing on dates inside the LANES section, so on #34 it could not have failed even with a stale stamp. Moved so the check tests what it is named after.)*

## 🛤 LANES — generated index (records: `knowledge/_lanes.json` · generator: `knowledge/_gen_lanes.py` · O1′ pilot, ruled #24)

*Data carries STATE, prose carries WHY — the WHY lives in `notes/_MEMENTO-DECISIONS.md`. The GM §C·1 eager ROUTING line is checked against the records at wrap (BLOCKING). Never hand-edit between the markers.*

<!-- AUTO-LANES START — generated by knowledge/_gen_lanes.py from knowledge/_lanes.json; never hand-edit between these markers. -->
**LANDED — `lane-1-memento` · Memento** *(born #19 · 2026-07-28 (standing priority, Dave) · two-lanes #20)*
- ✅ M5 — hardened GM/LS mover `_gm_move.py` — landed · receipt notes/_MEMENTO-DECISIONS.md § ★ M5 ENACTED (#21)
- ✅ wrap-ritual section-usage instrumentation `_gm_usage.py` + probe — landed · receipt notes/_MEMENTO-DECISIONS.md § ★ #23
- ✅ O1′ — LS schema + generated index/view (lanes = pilot case) — landed · receipt notes/_MEMENTO-DECISIONS.md § ★ #24
- ✅ O2′ — modular memento-search + gates — landed · receipt notes/_MEMENTO-DECISIONS.md § ★ #25
- ⏹ until: LANDED 2026-07-28 #25 — O2′ enacted (core + two doors + gates); lane-2-apollo-charts unblocked · receipts: notes/_MEMENTO-DECISIONS.md

**ACTIVE — `lane-2-apollo-charts` · Apollo charts** *(born #20 · 2026-07-28 (M-codes retired at the split) · blocked_by: lane-1-memento)*
- ✅ DV-J2 — chart-table-toggle accretion, SCATTER HALF (was ex-M4b) — landed · receipt knowledge/_proforma/_DATAVIZ-DECISIONS.md § Open/pending (#27 — first NARROW consumes declaration live: 13,251 B in, dv-legend's 16,271 B refused; 4-way mutation control; render-proven knowledge/_render/verify_dv_j2_render.py)
- ⏳ DV-J2b — sparkline toggle markup + CSS (JS already injected, dormant) — queued · receipt knowledge/_proforma/_DATAVIZ-DECISIONS.md § Open/pending (split from DV-J2 by Dave's ruling #27 — scatter half only, to keep the diff attributable)
- ⏳ DV-J1 — table-idiom unification (was ex-M4a) — queued
- ⏳ §C·1 strands (a)–(d) — chart expansion · wave 3 · templates/shells · enact window — queued
- ⏹ until: born blocked, UNBLOCKED #25 (lane 1 landed) — lands when DV-J1/DV-J2 + the §C·1 strands ship (keys minted #26, Dave: J = Job; was ex-M4a/ex-M4b) · receipts: knowledge/_proforma/_DATAVIZ-DECISIONS.md § Open/pending · GOOD-MORNING.md §C·1(a)–(d)

**STEADY — `lane-dream-pass` · Memento dream-pass (spin-off)** *(born 2026-07-26 (S-D1 schedule EARNED — weekly Sun 07:10) · wraps: `--wrap --lane`)*
- ⏳ M12 — first UNATTENDED Sun 08-02 07:10 fire (nobody watches it; that is the point) — queued
- ⏹ until: steady-state by design: the weekly task dreams; Dave rules; sessions enact · receipts: notes/_MEMENTO-DECISIONS.md · _LIVE-STATE.md §🔀
<!-- AUTO-LANES END -->

## 🔀 SPIN-OFF LANE — Memento dream-pass (registered 2026-07-26, per the spin-off rule; runs COLD from its own record, deliberately OUTSIDE the GM queue — the lane itself dogfoods §4.2's cold-read thesis)
Entry point: `notes/2026-07-26-memento-dream-pass-scope-v2.md` (three shapes: Cowork · Claude Code · VS Code+Copilot) → v1 same date (§4.1 fields+gate, tooling verification) → `notes/2026-07-26-memento-dreaming-convergence-and-buildable.md` (the record).
**Status (2026-07-26, later session): D1–D4′ RULED + §4.1 BUILT.** Rulings + why: `notes/_MEMENTO-DECISIONS.md` (D1a repo-side · D2 five values · D3 one script · D4′ §4.1→A→C→B; D5/D6 pencilled). Built: `knowledge/_capture_gate.py` (build/wrap/selftest modes) wired blocking into `_build_all.py`; runbook steps 1b/2/3 + gate section amended; cutover `notes/2026-07-26-provenance-cutover.md`; three lane notes field-retrofitted. **NEXT for this lane: Shape A** — scheduled Cowork task emitting `notes/_dream/…-proposals.md` (scope v1 §4). Owed: convergence-note `-v2` (still blocked on re-attach of `2026-07-26-convergence-anthropic-dreaming.md`) · Dave's D6 access check before any Shape C build. Prior commits `dfdc857` + `f140fee` + `d22f29f` (f140fee/d22f29f unpushed as of this session's start — Desktop push owed).
**Status (2026-07-26 evening, Shape A session): SHAPE A BUILT + FIRST DREAM PASS RUN — 8 floated proposals await Dave.** A-D1–A-D4 RULED (ledger, explicit option-select): manual-first-then-schedule · weekly/last-~15 (config only — task NOT created, earns itself on this file) · D5 ENACTED `.claude/agents/dreamer.md` (steering spec, single source for Shapes A/B/C; dot-path blocked to file tools → written via shell) · proposals home `notes/_dream/` — verified OUTSIDE `_capture_gate.py`'s glob, fields by discipline (A-D4). First pass: ONE cold Opus dreamer subagent, 15/15 transcripts read (turn-level ceiling held), evidence repo-verified → `notes/_dream/2026-07-26-proposals.md` (298 lines, 8 proposals ranked by prevalence; conductor spot-checked 3/3: P1 `_LIVE-STATE` 855 lines/205,561 B exact · P3 render-verify runbook untouched since 07-23, greps 0 · P5 ds-010 live at `Chart-bar.reference.html:102`, GM count 0). Dreamer also recorded a checked-clear list so the next pass doesn't re-open settled ground. NEXT: **Dave READS the proposals file** — promotion his alone (derivation-governance) → on his say-so the weekly task is created per A-D2. Owed unchanged: convergence `-v2` (blocked on re-attach) · D6 before any Shape C. Prior lane commits verified pushed at session start (`06e48ef` = origin/master).
**Status (2026-07-26 evening, ruling session): DAVE RULED THE DREAM — P1–P5+P7+P8 accept-enact-now (ENACTED), P6 deferred to its own session (parked `_FUTURE-STATE.md`), rejections: none; S-D1 schedule EARNED (`memento-dream-pass` weekly, Sun 07:10, per A-D2) · S-D2 lane flag (`--wrap --lane`) + S-D3 stdout-only wrap BUILT + bite-tested — both wrap-gate warts CLOSED.** Full rulings + WHY + enactment receipt: `notes/_MEMENTO-DECISIONS.md`. Headline enactments on main-queue surfaces (by ruling, per proposal): `_LIVE-STATE-ARCHIVE.md` (this file 205KB→62KB, ritual step 2d) · `knowledge/_git_commit.sh` + runbook · render-verify runbook fold · GM count/tuner/ds-010 lines · `_FUTURE-STATE` corrections. **Lane is now STEADY-STATE: the weekly task dreams; Dave rules; sessions enact.** Owed unchanged: convergence `-v2` (blocked on re-attach) · D6 before any Shape C. ⚠ `ec4c2f3` was UNPUSHED at this session's start — push the whole stack via Desktop.
**Status (2026-07-26 evening, weekly-run session): SECOND DREAM PASS RUN + RULED SAME SESSION — V2-P1–P4 ENACTED, V2-P5 HELD.** Pass ran cold per the lane checklist (Fable conductor + 1 Opus dreamer, repo-first forensics); 5 proposals → `notes/_dream/2026-07-26-proposals-v2.md` (commit `d777aaa`, 4/4 conductor spot-checks held). Dave ruled in plain language same session: V2-P1 six 07-24 chart deferrals RESTORED to GM §C·2 as **17–22** + compaction EXIT CHECK in ritual 2c/2d · V2-P2 emitter determinism FIXED (7 `sorted()` sites, 4 scripts; advisory 6/6 identical under random hash, §C·4 line closed; dated-banner mentions left historical) · V2-P3 ds-011 logged (G/H/N advisory promotions + triggers, incl. WCAG 2.4.1 Level A ×5 screens) · V2-P4 `_REVIEW-SIGNOFF.md` fed 4 strands (legend v5.x · tuner v1+v2 · hit-area rule brief · 5 chart panes) + ritual step-1 feed-the-register clause. **V2-P5(a) ENACTED same session — Dave re-attached the note; saved verbatim to `notes/2026-07-26-convergence-anthropic-dreaming.md` (+fields, gate 0 fail); the three-session blocker is DEAD.** V2-P5(b) (runbook save-uploads clause) pencilled, awaits his word. Ledger rows V2-P1–P5 in `notes/_MEMENTO-DECISIONS.md`. Build 55/55 GREEN post-enactment. **Continuation same session (Dave: "love your work continue"): V2-P5(b) ENACTED (save-cited-uploads clause, ritual step 1; read as the yes, vetoable) + convergence `-v2` WRITTEN** — `notes/2026-07-26-convergence-anthropic-dreaming-v2.md` (Opus worker + Fable 4/4 spot-check incl. independent transcript grep; supersedes v1 in-part, v1 stays as filed; §3-verification fixes + databases-Q&A recorded OWED in its §7). **Lane's owed list — CORRECTED 2026-07-28 #22 (dream-pass-3 P4a; the 07-26 'only' was false within a day): the ledger `notes/_MEMENTO-DECISIONS.md` is the owed list's home, never this line — at correction time it held: M12's first unattended Sunday fire (08-02 07:10; M11 CLOSED #21 `0ee1634`) · D6 (Dave, before Shape C) · `-v2`'s §7 leftovers · the #21 dreamer hunt-list follow-ons.** **S-D4 (same evening): conductor sequence inscribed → `knowledge/_RUNBOOK-dream-pass.md`; Cowork skill `dream-pass` + the weekly task prompt are thin pointers to it — "run dream pass" is now the whole invocation.**
**Status (2026-08-08, dream pass 5 — the lane's first §🔀 row since 2026-07-26, and that gap is the finding): PASS 5 RAN MANUALLY, OVERDUE FROM #127. 3 proposals; P1 + P2 RULED SAME SESSION; ALL SEVEN 2026-08-02 ITEMS RULED ENACT-NOW.** Run shape: **manual**, not the scheduled fire — it was raised by Dave mid-#127, did not fit that window, and was **rolled to #128 as item ①** rather than started and abandoned. Dreamer = Opus pinned, conductor = Fable, spot-checks **4/4 held**. Output `notes/_dream/2026-08-08-proposals.md`, commit `6836c5a` — **P1** (all six 2026-08-02 dream-pass rulings unenacted at #127 **and none of them present in `_rulings.json`**, so the instrument that tracks enactment was structurally blind to them) · **P2** (residual carry rolled 14×, no age on any carried item) · **P3** (this file's own sweep risk); 5 checked-clear. **Dave ruled P1 and P2 the same session, and extended P1 live** from *register the six for visibility* to **enact all seven 08-02 items now** (`s128-D1`); P2 ruled as an age-bracket FORMAT, no threshold and no gate (`s128-D2`); and two seams were ruled alongside — **this very step** (`s128-D3`, the lane writes its status here between commit and gate, `knowledge/_RUNBOOK-dream-pass.md` step 7b) and the commit script's `--cleanup=verbatim` + subject assert (`s128-D4`, raised by pass 5's own first commit losing its message to a '#'-leading first line). Rulings + WHY: `notes/_MEMENTO-DECISIONS.md` § #128; registrations `d0802-P2a…P7` in `knowledge/_rulings.json`. **Lane state: steady, and the third clause of its charter — *sessions enact* — has a receipt for the first time in 52 sessions.**
**Status (2026-08-09, dream pass 6 — the lane's FIRST on-time scheduled fire): SCHEDULED Sun 07:10, NOT overdue. 5 proposals FLOATED, 0 ruled (Dave absent — a scheduled run cannot rule; all five await his eye).** Dreamer = Opus pinned, conductor = Fable (scheduled session's own model), spot-checks **4/4 held** (P1's 21/96 frozen strings re-counted exact · `type.css:180` `#111` quoted · `_git_commit.sh` dirty-tree push-refusal + tracked `_REHEARSAL-LOG.jsonl` re-verified · runbook `:7/:99` Desktop-only lines + 0 `--push` hits re-grepped; the dreamer's cc1 "0 files" chased to 1 benign mention-not-use hit — its own file quoting the search pattern, no credential bytes, `real-token` regex 0). Output `notes/_dream/2026-08-09-proposals.md`, commit `0219075` — **P1** (21/96 rulings carry a status string frozen at the #119 sweep; `_governs.py:209` republishes it) · **P2** (verify-after-commit dirties the tree and `s133-D2`'s clean-tree gate then refuses `--push`; 9 sessions) · **P3** (`_RUNBOOK-git-commit.md` still rules "GitHub Desktop only" three sessions after `s133-D2` made terminal push the ruled path — pass-4 P3's class recurring in a different artefact) · **P4** (PAT expiry ~2026-11-06 unstamped, nothing re-checks scope, `:39` instructs the credential transit chat) · **P5, thin** (the `--all-dirty` escape hatch awaits Dave's one-word verdict since #128, on no carry list); 6 checked-clear (cc1–cc6, incl. pass-5 thin-P3 OVERTAKEN — `git add -A` retired, explicit-path staging live). This pass read 15/15 transcripts (pass 5 read 1 of 15 — declared there). ⚠ **SEAM FOUND, DAVE'S: the lane has no session-number vocabulary** — T3 (s130-D3) refuses non-wrap commits without `SESSION_N`; the witness passes only for 136, so the lane commit carries `after #136` while `_CHAIN.md` reserves the #136 title for the resolutions-input enactment session — [[honest-refusal-needs-a-legal-form]], his call whether lane runs take a number or T3 grows a lane form. First scheduled fire whose file was committed BY the lane itself (08-02's was swept by #76's `add -A` — the defect s128-D4 retired).


## ⏱ LATEST DELTA — 2026-08-12 (Wed **#164**, FABLE conductor + TWO OPUS build subs + this OPUS wrap sub, Dave live, **ONE RULING, DAVE'S — AND THE FINDING IS A GATE THAT COULD NOT RUN** — ⛔→✅ **THE BUILD DIED BEFORE STEP 1 SINCE #158; STEP 13's PROVENANCE GATE IS RED WITH 15 REAL FAILS** · ✅ **THREE BRIEFS PUSHED** · ✅ **SHOWROOM RE-SYNCED** · ⬛ **THE 15 ARE DAVE'S, TARGET FRIDAY**)

**Landed (evidence per claim, verified first-hand by this wrap sub unless marked RELAYED):**

- ⛔→✅ **THE BUILD'S ROUTE TABLE WAS MISSING THE #158 STEPS.** Two `ROUTE_ROWS` rows (both `ABORT`) added in **`3ef22c7`** — `_build_all.py` then reached **step 13** for the first time since #158. ★ A new step bypassed the table that governs steps; the symptom read as an environment fault.
- ⛔ **STEP 13 IS RED — 15 REAL PROVENANCE FAILS, FIVE SESSIONS OF UNGATED RULINGS.** `_governs.py --selftest` re-driven here: **15 FAIL lines** on `s157-D1`…`s163-D1` (missing `governs`/`evidence`/`status`, or prose evidence with no `chat #N`/`commit` pointer). ⛔ **Untouched — authoring them is inventing provenance. Dave-side, target Friday 2026-08-14.**
- ✅ **A 16th FAIL WAS FALSE AND FIXED AT SOURCE.** `PATHISH_RE` truncated dotted stems (`Tooltip.reference.html`); fixture-driven fix, **16 → 15** (`3ef22c7`). ⛔ The pointer was correct; the extractor was not.
- ✅ **SHOWROOM RE-SYNCED** — 6 pages stale post-#158; `gen_showroom.py --check` **rc=0 (75 pages + index)**, re-driven here.
- ✅ **THREE BRIEFS INSCRIBED AND PUSHED** — `434c455` (borrowed-instruments v1+v2, **RULED-TO-EXPLORE**, enactment parked for Friday, five Dave-gates open) · `7543b48` (progress dashboard, **RULED A PRIORITY BY DAVE**, build 2026-08-13 after his sidequest, Mono + `swiss-design-system`, panels his eye).
- ✅ **42-VERDICT CONTROLLER BUILT + RENDER-VERIFIED** — `reviews/pri-hover-verdicts-42-v1.html`, **zero pre-selected inputs**; queued in `knowledge/_REVIEW-SIGNOFF.md`. ⚠ **The 42 are the whole #139 token-fork ledger; the filename undersells it — ⛔ NOT renamed, that is Dave's.**
- ⛔ **MSGFILE-PREFIX CLASS, INSTANCE 9** (`ac5ecac`, doubled prefix, amended from a fresh `printf` msgfile before push). Nothing gates it.
- ⚠ **T2 / T3 DECLARED, NOT FIXED:** `selftest_growth` **crashes** instead of failing named without `tiktoken` (`_capture_gate.py:5307`, unruled) · sandbox disk ~full, session-suffixed `--target` recipe stands, **no runbook amended**.
- ⚙ **DELEGATION + GAUGE.** Dave: **use OPUS subs liberally, quota is plentiful**; binding budget **NAMED — QUOTA for the subs**; ⛔ no Sonnet subs. **GAUGE: NOT MEASURED BY THIS SUB AND NOT RELAYED — none inscribed; UNKNOWN is never defaulted.**
- ⛔ **THIS WRAP RULED NOTHING** — and **no ruling id was minted for the dashboard priority**; promotion is Dave's alone.
- ✅ **POST-WRAP ADDENDUM (after `7cfa5b7`, NOT an amend of it) — THE DECK LANE IS ATTRIBUTED.** The two PRESENTATION files the wrap left untracked as **unattributable** (a correct refusal, and it stands as written) came from a **Cowork worker lane, `tender-stoic-clarke`, Dave's, role declared retrospectively**. Evidence: **`notes/_receipts/2026-08-12-tender-stoic-clarke-designer-community-deck.md`**. Handed up **v1 · v2 · v3 + the receipt**, nothing committed; **v3 is the deck for the 2026-08-13 designer community call**, now queued in `knowledge/_REVIEW-SIGNOFF.md` **awaiting Dave's eye**, ⚠ **not render-verified** (playwright absent in that sandbox). Pointer/state/owner: `GOOD-MORNING.md` §C·4 post-wrap addendum block. ⛔ **Deck NOT edited · v1/v2 NOT deleted · the four Dave statements inside it (75→135→300 · autonomous low-risk production · edit mode + brief builder · separate products) are FLOATED/OBSERVED ONLY — no ledger, no ADR, no ruling id.** ⛔ **Nothing settled at wrap was touched, including the 15 provenance fails.**

Dossier: `_DECISION-HISTORY/2026-08-12-164-the-gate-that-could-not-run.md`.

## ⏱ PRIOR DELTA — 2026-08-12 (Wed **#163**, FABLE conductor + this OPUS wrap sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES G18 THROUGH ITS OWN CONDITION** — ✅ **`s163-D1`: `retired_unit_prose_audit` FLIPPED TO BLOCK, WIRED, BOTH #84 PARKING CONDITIONS DISCHARGED** · ✅ **RULED · ENACTED · RE-DRIVEN IN ONE WINDOW** · ⚠ **SCOPE: STALE INDEXES, NOT FALSE CLAIMS**)

**Landed (evidence per claim, verified first-hand by this wrap sub unless marked RELAYED):**

- ✅ **`s163-D1` RULED BY DAVE — G18 CLOSED.** The flip supersedes `s161-D2`'s provisional WARN **per that ruling's own close condition** (*"Dave confirms warn as final or flips to block"*); Dave picked **"Flip to block (Recommended)"** from a staged choice after a read-back. `knowledge/_rulings.json` **129 → 130**, tail `s163-D1` — **re-parsed here (JSON round-trip; body read in full)**.
- ✅ **THE HOMONYM IS FIXED AT THE REGEX, WORD-SENSE ONLY.** `RETIRED_PROSE_WORDS_RE` = `(?<!duct )(?<!duct-)\b(tape|bill)\b` — **diff read off disk**. **2 of the 5 live hits**, named at #84 as *"a REGEX defect … cheaply fixable"*. ⛔ **Bare `tape` still matches everywhere else** — proven by the control, not by the comment.
- ✅ **THE OTHER 3 HITS WERE CLEARED BY DECLARATION, NEVER BY REPHRASING.** `knowledge/_BANKRUPTCY-ARCHIVE.md` (the #87 batch — historical marker) and `knowledge/_DS-IMPROVEMENTS.md` **ds-021** (SUPERSEDED marker; the **#84-named true positive**, 2 hits). ★ **Re-denominating dated text would destroy the record the audit exists to protect** — the audit pins WHERE the words appear, never HOW a sentence is phrased.
- ✅ **THE AUDIT IS WIRED AND BLOCKING.** `f, w = retired_unit_prose_audit(repo)` + `fails += f` in `_capture_gate.py`'s md sweep, beside a comment block recording **the discharge of both #84 parking conditions**. ★ **An unwired gate cannot fail and is not an achievement** [[instrument-without-a-consumer]].
- ✅ **VERIFICATION RE-DRIVEN HERE, INCLUDING THE CONTROL.** Planted undeclared `tape` line ⇒ **1 FAIL** (quoting file · line · region · both remedies); removed ⇒ **0**; **`duct tape`/`duct-tape` control EXEMPT in both runs**; `selftest_retired_unit_prose()` **PASS**; **live tree 0 fails / 0 warns**; `_capture_gate.py --wrap` **rc=0 (121 in scope · 0 fail · 15 warn)** run BEFORE any edit [[mutation-tests-the-clause-not-the-feature]].
- ✅ **THE STATE STORE CARRIES THE CLOSURE WITH A RECEIPT.** `knowledge/_state.json` **G18 → `done`**, `closed_by` = *"s163-D1 (Dave, #163) - flipped to block; audit wired blocking, hits cleared by declaration, homonym fixed in regex"* — **read back off disk**.
- ⚠ **THE SCOPE CAVEAT IS CARRIED UNSOFTENED:** **STALE INDEXES, NOT FALSE CLAIMS**; the percentage band is **OUT OF SCOPE pending ds-023**; **the cross-instrument claim check remains the open successor and is DAVE'S** [[gate-must-quote-what-it-forbids]].
- ⚙ **GAUGE (RELAYED by the conductor, not re-measured by this sub):** boot **55,309** real, inside the **54,859 ±1,178** band — a datapoint, never corrected into the constant; **FILL at wrap-open ~111,310** vs stop **150,929** ⇒ **EARLY, ~39.6K of room against a 42–49K price**. Delegation: **this OPUS wrap sub only**; binding budget **NAMED — QUOTA**. ⛔ No Sonnet subs. ⚠ **QUOTA NOT RE-POLLED** — the panel figure on the record is dated, not current.
- ⛔ **THIS WRAP RULED NOTHING** — `s163-D1` is **DAVE'S**; no close condition invented for anything; every remaining G-item and LEGACY close condition, the 19 LEGACY unconditioned items, the icon warns and declared holes, `_graph-mark-observations.jsonl` policy, palette values, non-mono forks, promotions, the CI blocking flip, the `_gen_titles.py` write-gate exception and the cross-instrument claim check successor are **his and untouched**; **no ratified stratum trimmed — ADD, never trim**; MEMORY step 3 **SKIPPED (the conductor's)**; `_build_all.py` **NOT RUN**; ⛔ **NOT PUSHED**.

Dossier: `_DECISION-HISTORY/2026-08-12-163-the-provisional-warn-that-closed-through-its-own-condition.md`.

## ⏱ PRIOR DELTA — 2026-08-12 (Wed **#162**, FABLE conductor + this OPUS wrap sub, Dave live, **ONE RULING, DAVE'S, AND IT CLOSES THE WAVE** — ✅ **`s162-D1`: `tooltip.tip` RULED `no-bind:structural-param` ON SIGHT** · ✅ **THE `s142-D1` WAVE CLOSES 114/114** · ✅ **RULED · ENACTED · VERIFIED *AND PUSHED* — `0fa5f8f`** · ⛔ **MSGFILE-PREFIX CLASS INSTANCE 8** · ⚠ **A CARRIED "NOT PUSHED" CLAIM WAS STALE** · ⚠ **ENOSPC n=7**)

**Landed (evidence per claim, verified first-hand by this wrap sub unless marked RELAYED):**

- ✅ **`s162-D1` RULED BY DAVE, ON SIGHT.** `tooltip.tip` (enum `top|bottom`, default `top`) → **`no-bind:structural-param`**, class **C11**. Instrument: `reviews/REVIEW-tooltip-tip-s162.html` (**both edges, light + dark, snippet CSS verbatim**, confirmed on disk here) plus the finding that **the reviewed snippet is SPACE-AWARE and flips at runtime**. Dave verbatim: ***"so yes, the tooltip should flip if there is no space to display it in the same way as it moves from the edge to accommodate the message"*** → after read-back ***"this a behavior that will be constant across all themes, i don't think this needs tokenizing"***. ★ **Read-back confirmed BEFORE recording.**
- ✅ **THE `s142-D1` WAVE IS CLOSED 114/114.** `knowledge/_rulings.json` **128 → 129**, tail `s162-D1` — **re-parsed here (JSON round-trip)**; `knowledge/components/tooltip.meta.json`'s `tip` row carries its **`$status`**, read back off disk.
- ✅ **GATES RE-DRIVEN, NOT RELAYED.** `_validate_snippets.py` **rc=0 (75/0)** · `_validate_binds_resolve.py` **rc=0** (75 snippets · 958 vars · 102 binds addresses · 75/75 canon blocks · 0 fails) · `_validate_palette_tier.py` **rc=0** (4 themes · 3 palettes · 38 declared keys · 75 metas · 75 manifests).
- ✅ **PUSHED ON DAVE'S WORD — `0fa5f8f`**, *"after #162 2026-08-12 — s162-D1: tooltip.tip ruled no-bind:structural-param — the s142-D1 wave closes 114/114"*; tree clean after push, verified here.
- ⛔ **MSGFILE-PREFIX CLASS, INSTANCE 8 — AND THE TRIGGER WAS A REFUSAL.** The first T3 invocation refused (`--all-dirty` missing); the retry **reused the MUTATED msgfile** ⇒ doubled prefix (`6e0ed57`), amended clean from a fresh `printf` while unpushed. ★ **A refused invocation is still an invocation — it already mutated the file.** Hook corrected by the conductor; ⛔ this sub did not touch `MEMORY.md`.
- ⚠ **A CARRIED REPO-STATE CLAIM WAS STALE:** #161's *"wraps `6726a2a`+`ee091ef` NOT pushed"* — **the remote already had them** (ahead-count **1** pre-commit). Recorded as a measurement; **no gate invented.**
- ⚠ **ENOSPC n=7, RE-MEASURED NOT INHERITED:** `/` at **97%**, `rm` still permission-blocked for foreign-owned `/var/tmp` dirs. The #161 recipe **held** — tiktoken via `--target /var/tmp/pylibs-s162`. ⛔ **No runbook amendment: n=7 produced no new fact.**
- ⬛ **G18 EXPLAINED, NOT RULED — STAYS DAVE'S.** 5 live hits measured (`_BANKRUPTCY-AR…` ×1 · `_DS-IMPROVEMENTS` ×2 · `_ROBUSTNESS-PO…` ×2), flip-to-block **RECOMMENDED**; **no ruling taken, no close condition invented.**
- ⛔ **THE WAVE'S VALUE-LEVEL AESTHETIC LEG REMAINS UNPROVEN.** Only **tooltip** was rendered and seen; **the other 113 rows are unseen and only Dave's eye can close them.**
- ⚙ **GAUGE (RELAYED by the conductor, not re-measured by this sub):** boot **55,337** real, inside the **54,859 ±1,178** band — a datapoint, never corrected into the constant. **FILL at wrap-open 141,920** vs stop **150,929** ⇒ **the wrap opened LATE, ~9K of room against a 42–49K price — declared, not smoothed.** Delegation: **this OPUS wrap sub only**, binding budget **NAMED: QUOTA for the sub**; ⛔ no Sonnet subs.
- ⛔ **THIS WRAP RULED NOTHING** — `s162-D1` is **DAVE'S**; no close condition invented for any G-item or LEGACY item; G18, the 19 LEGACY unconditioned items, the icon warns and declared holes, `_graph-mark-observations.jsonl` policy, palette values, non-mono forks, promotions, the CI blocking flip and every `_FUTURE-STATE.md` priority are **his and untouched**; **no ratified stratum trimmed — ADD, never trim**; MEMORY step 3 is the conductor's (**SKIP declared**); `_build_all.py` **NOT RUN**. ⚠ **The WRAP commit is LOCAL — NOT PUSHED.**

Dossier: `_DECISION-HISTORY/2026-08-12-162-the-last-unruled-row-and-the-flip-that-was-already-there.md`.

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
- **White is the RAG text colour universally; dark-text variant DROPPED** (R-D1, claim carried live
  by R-D7/R-D15 — cite those; R-D1 itself is superseded · s124 tally SAVE) — amber the sole
  exception, always was.
- **`#000000` retained in the KB as brand source of truth**; `#1A1A1A` = digital black for screens;
  `#1D1D1D` dropped; `#333333` canon, stays.
- **Incumbent RAG values NOT deleted** — retired into a future legacy theme. Tombstone, keep.
- **R-D4 (2026-07-18): matting rungs RULED — green + blue matted 15%** (`#2B7E4F` / `#306EC6` —
  ⚠ SUPERSEDED as fill values (R-D12.B): light later RESOLVED `#5DAC7B`/`#7DABCD`, dark stays
  R-D10's `#43AD6F`/`#5F92B9`, see below · s124 tally SAVE),
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
  ★ **REINFORCED #108-D3 (Dave, verbatim, `ds-035`):** *"we have 4 themes, mono, legacy, console, and supercharge. they have a lot of overlap but they also diverge, especially the colour palette of legacy and the others, and the grey ramp for supercharge and the others. I just want the flexibility to have these themes and create more."* Plus, explicitly NOT NOW: *"I will also be revisiting the grey ramp for mono, i think we've calculated wrong."* → governs every cross-theme token-collision sweep: divergence between themes on the SAME token name is expected, not a defect by default (see the `--pri-hover` finding, `outputs/_FINDING-canon-pri-hover-brand-mono-fork-2026-08-06-v1.md`).
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

**100 decision nodes — 84 LIVE · 7 AMENDED · 8 DEAD · 1 OPEN.** Full typed edges + what-touches-this map: `knowledge/_DECISION-GRAPH.md`.

**☠ DEAD — do not build on (8):**
- **DV:DOSSIER.chevron** · DataViz dossier chevron-on-stacked claim — superseded by DV-D04
- **DV:DOSSIER.s07** · DataViz dossier §07 one-file-per-component — superseded by DV-D01
- **R-D8** · Green/blue Band A; dark set closes — superseded by R-D9, R-D10
- **R-D13** · Light fills locked (first pass); dark reopened — superseded by R-D14
- **T-D7** · Binding mechanism: measure before ruling — superseded by T-D8
- **T-D11** · /1 batch attempted, failing, reverted — superseded by T-D12
- **TYPE:2026-07-17:composite-txt-child** · 07-17 composite with required .txt child — superseded by T-D9
- **TYPE:2026-07-18:badge-A8000B** · #A8000B badge ruling (same-day superseded) — superseded by TYPE:2026-07-18:sat-ceiling

**◐ AMENDED — live, but a specific claim is dead (7):**
- **ADR-0006** · Flexing engine product shape — dead claim(s): cool-warm-hot register framing
- **ADR-0015** · Behaviour partials: dataviz interaction layer as generated JS — dead claim(s): size-clause-and-one-source-posture; group-wide-injection-becomes-manifest-gated
- **R-D1** · RAG promotion round one — dead claim(s): dark red #CC4333 as the status-fill red; the vaguer 'future legacy theme' phrasing
- **R-D2** · Background/glyph split + matting — dead claim(s): role-uniformity
- **R-D3** · Amber solved
- **R-D4** · Matting rungs + first token promotion — dead claim(s): green/blue rung values for light fills
- **R-D10** · Dark set locked — dead claim(s): fills are mode-stable

**○ OPEN / proposed (1):**
- **T-D5** · Tracking rule IF sheets survive

**✓ LIVE (84)** — in force; titles in `_DECISION-GRAPH.md` §②:
  ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0007, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0012-A1, ADR-0013, ADR-0014, ADR-0015-A1, ADR-0015-A2, ADR-0016, B-D1, B-D2, B-D3, B-D4, B-D5, B-D6, B-D7, CHARTER.S9, DEF-003, DEF-005, DEF-006, DV-D01, DV-D02, DV-D03, DV-D04, DV-D05, DV-D06, DV-D07, DV-D08, DV-D09, DV-D10, DV-D11, DV-D12, DV-D13, DV-D14, DV-D15, DV-D16, DV-D17, DV-D18, DV-D19, DV-D20, R-D5, R-D6, R-D6.A, R-D6.A2, R-D6.B, R-D7, R-D9, R-D11, R-D12, R-D12.A, R-D12.B, R-D14, R-D15, R-D16, R-D17, R-D18, R-D19, R-D20, R-D21, R-D22, R-D23, R-D24, R-D25, T-D1, T-D2, T-D3, T-D4, T-D6, T-D8, T-D9, T-D10, T-D12, T-D13, T-D14, T-D15, TYPE:2026-07-18:sat-ceiling

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

### ✅ #138 — THE CAUSE IS FIXED: THE `/var/tmp` SYMLINK FARM, DRIVEN THREE WAYS + A REAL RENDER — COLD-SANDBOX CASE UNPROVEN, NOT CLOSED

**Closes the #137 entry below except one declared gap. The record below is kept verbatim.**

Fontconfig's `<dir>` now points at `/var/tmp/fonts-<session>/` — a symlink farm (`ln -s` each repo `.ttf`
into it) — instead of the repo's own TTF directory, so its `.uuid`/`.uuid.LCK`/`.uuid.TMP-*` marker
lands in `/var/tmp`, never in the tree it scans. ~5 KB of links, so it **preserves the ENOSPC
constraint** that forced #136's change rather than reopening it. Enacted in
`knowledge/_RUNBOOK-render-verify.md` as a new `§ SYMLINK FARM (#138)` block, addition-only; #129's
and #136's blocks stand as history, with the `<dir>`→repo element on `:42`/`:46` marked SUPERSEDED.

**Premise reproduced first-hand before any fix:** `fc-cache` against the OLD (`<dir>`=repo) conf wrote
the same three stray names #136 left (`.TMP` suffix random — #136 `NpSPVs`, #138 `SpeXCi`).
**Driven three ways, with a mutation that discriminates:** (A) farm conf, clean dir → **0** repo
strays · (B) mutation, ONLY `<dir>` swapped back to the repo, everything else identical → **3** strays
(the test CAN fail) · (C) after cleanup → **0**. **A real render run** (`showroom/chart-bar.html`,
`goto file://`, 1180+480) confirms the face still renders: `HSBC_MtUnivers_Latin` / `Univers Next
HSBC` / `Univers Next for HSBC` all measure **347**, matching each other and NOT the DejaVu (375) or
nonexistent-face (301) controls. Repo strays after the render: **0**.

★ **The method finding, and it recurs: the FIRST probe was a false green** — `FONTCONFIG_FILE`
*replaces* the system config, and the conf had no `<include>` of `/etc/fonts/fonts.conf`, so only 10
faces (all HSBC, of 394 on the box) were visible and every request fell back to the only faces
present — **345 for every face measured, including one that does not exist.** A page can render
entirely in the HSBC cut and look correct even when its fallback is broken, which means #136-era
renders "verified" pages that could never have shown a fallback bug. The `<include>` line is now
mandatory and documented; `document.fonts.check()` returned `true` in BOTH the broken and working
configs and is recorded as worthless for this purpose. Same class as #137's `sed`-grabbed-comment
false green [[green-tests-cannot-see-scope]] — two sessions running.

✅ **The class is now gated, not just documented:** `instrument_stray_check()`, new in
`knowledge/_capture_gate.py`, called from `wrap_checks()` — pass 1 respects `.gitignore` (measured:
`knowledge/assets` carries 60 untracked-but-ignored paths, so ignoring `.gitignore` wholesale would
fire every wrap), pass 2 re-checks WITHOUT `--exclude-standard`, filtered to
`INSTRUMENT_SIGNATURES=(".uuid",)`, so a `.gitignore` entry cannot blind it. Driven four ways: clean
tree silent · planted `.uuid`+`.uuid.LCK` FAILS, classified structural · the SAME files then
gitignored STILL fails · a non-signature untracked file fails via pass 1. Lives at the wrap seam
deliberately, not `_build_all.py` (sandbox-impossible, ~49s vs the ~45s call kill).

⬛ **NOT CLOSED — declared, not hidden: the farm is UNPROVEN in a COLD sandbox.** #138 re-used
`/var/tmp` staging left by #129/#131/#136 (`pw-browsers-*`, `pylibs`, `chromelibs` all survived);
runbook steps 1–4 (download + libs) were never re-run against an empty `/var/tmp`. Carried to #139 as
residual ①. ⚠ **Two potholes hit and documented in the same lane:** ENOSPC n=4 (`/sessions` 100% full,
18 M free at boot, same shape as #129/#136) and a cross-filesystem `mv` (repo→`/var/tmp` fails,
different filesystem — same-mount `mv` to `_to_delete/` works), the second CAUGHT BY the new gate, an
unplanned live demonstration. Dave's instruction on gate scope, verbatim: *"i just want a solid
fix"* — enacted on that instruction; **not minted as a ruling**, promotion is his alone.
[born #138 · guards: `_RUNBOOK-render-verify.md` § SYMLINK FARM (#138) + `_capture_gate.py::instrument_stray_check` · until: driven in a cold sandbox]

### ⛔ NEW #137 — FONTCONFIG WRITES INTO THE REPO IT SCANS — DAVE: *"no patches or hacks, solve it permanently"* (born #137, **CLEANED, CAUSE NOT YET FIXED — #138's FIRST MOVE**)

**Measured, not inherited.** Three untracked files sat in `knowledge/assets/fonts/_desktop/TTF/`, all stamped
**2026-08-08 22:57** (#136's render-verify run, minutes after the tier-map controller was built): `.uuid`
(36 bytes, one UUID — `cc93ecdf-bc0f-473f-bb7c-b825f28a20bc`), `.uuid.LCK` and `.uuid.TMP-NpSPVs` (2 bytes each,
an orphaned lock and atomic-write temp from a process that died before cleanup). Fontconfig writes a `.uuid`
marker into a scanned font directory to give that directory a stable identity for its cache.
✅ **CLEANED #137** — all three moved to `_to_delete/_fontconfig_strays/` (gitignored, `.gitignore:25`); the
10 tracked `.ttf` files were never touched and the tree now has **zero untracked paths**.

⛔ **THE CAUSE IS UNFIXED AND THE CLEANUP IS NOT THE FIX** — they regenerate on the next render run.
**Two of this project's own remedies collided:** the OLD render recipe copied the TTFs to `~/.fonts`, so
fontconfig scribbled *outside* the repo. #136's ENOSPC fix removed the copy to save disk and pointed
`FONTCONFIG_FILE`'s `<dir>` **straight at the repo's TTF directory** (`_RUNBOOK-render-verify.md:42,46`) — which
saved the disk and moved fontconfig's writes *inside the tree*. The dirt then trips `s133-D2`'s clean-tree gate
and refuses the push. ★ **Same class as `s137-D1`/dream-P2: an instrument writing into the tree it measures.
Two independent instances in one session makes it a class, not a coincidence.**

⬛ **THE PERMANENT FIX, DESIGNED AND PRICED, NOT ENACTED — Dave's standing instruction is that it be permanent,
so it must be DRIVEN, not asserted:** point `FONTCONFIG_FILE`'s `<dir>` at a **`/var/tmp` symlink farm**
(`ln -s` each repo `.ttf` into `/var/tmp/fonts-<session>/`) rather than at the repo path. Symlinks cost ~0 bytes,
so the ENOSPC constraint that forced the #136 change is **preserved, not reopened**; fontconfig writes its
`.uuid` into `/var/tmp` where it belongs; the repo is never written. Then amend `_RUNBOOK-render-verify.md:42,46`
**by addition**. ⚠ **UNPROVEN — the proof is a real render run (~4 sandbox calls) confirming (a) the face still
renders at 1180+480 and (b) no `.uuid*` appears under `knowledge/assets/` afterwards.** #137 had 18,402 real of
job room at the decision point, which does not fit a render lane plus a wrap; recorded rather than rushed.
⛔ **Do NOT "fix" this by gitignoring `.uuid*` — Dave explicitly refused a patch.** An ignore rule hides an
instrument that is still writing where it must not.
[born #137 · guards: `_RUNBOOK-render-verify.md:42,46` + the absence of `.uuid*` under `knowledge/assets/` · until: the symlink-farm recipe is driven green and the runbook amended]

### ⬛ NEW #137 — WRAP-STEP CANDIDATE, DAVE'S WORDS: `git log` SINCE BOOT, FOREIGN COMMITS NAMED IN THE BANNER (born #137, **FLOATED, NOT RULED**)

**Dave, #137, verbatim:** *"at wrap, `git log` since boot; any foreign commit gets named in the banner — that closes
this class permanently. A scheduled lane that commits mid-session will happen again."*
**The class it closes:** a session's wrap banner describes only what that session did, so a commit made by anyone
else inside the window — a scheduled dream lane, a parallel conductor — is invisible to the record the next
session reads. **Demonstrated live this session:** dream pass 6 fired on its 07:10 schedule and committed
`0219075` (273 lines, `notes/_dream/2026-08-09-proposals.md`); #136's wrap banner, generated at 15:40, cannot
name it, and the #137 residual list therefore does not contain the single largest piece of new work waiting.
It was found by a boot-time `git log`, not by any gate.
⛔ **FLOATED, NOT RULED — this is a candidate Dave asked to be noted, not an instruction to enact.** Enactment
would add a step to the wrap ritual (`_RUNBOOK-capture-ritual.md`) and a check to `_capture_gate.py --wrap`;
neither is priced here. ★ Note the shape: it is a **generate-don't-inherit** remedy of the same family as the
T3 chain fix — the banner would compute foreignness from `git log`, never from what the session remembers doing.
[born #137 · guards: the wrap banner's completeness claim · until: Dave rules the wrap step in or out]

### ⬛ NEW #137 — TWO DREAM-PASS ITEMS THAT FELL OUT OF EVERY CARRY LIST — RE-HOMED HERE SO THEY ARE ANSWERABLE (born #137, dream pass 6 P2 + P5)

**Both were raised once, priced or asked, and then appeared in no residual list for eight-to-eleven sessions.
Homing them is the whole point of this entry; neither is ruled and neither is enacted.**

**(1) P2 — the verification instruments dirty the tree, and since `s133-D2` that blocks the ruled push.**
`_capture_gate.py --wrap` and `_checkin.py` both append to `notes/_REHEARSAL-LOG.jsonl`; `_git_commit.sh:153/157`
runs the gate and stages at `:300–316`, so a run *inside* the script is captured and **anything run after the
commit is not**. `_git_commit.sh:38` then refuses to push on a dirty tree. ✅ **CONFIRMED FIRST-HAND #137, not
inherited:** this session's own opening `_checkin.py` left ` M notes/_REHEARSAL-LOG.jsonl` in `git status`
before any other work was done. The remedy was priced once at #125 — *"move the log write ahead of the staging
seam, or exclude the log from the clean-tree assertion"* — and greps of `_LIVE-STATE.md` and `GOOD-MORNING.md`
for `REHEARSAL-LOG` return only the #104 unattributed-path line. **Eleven sessions, priced once, homed nowhere
— until this line.** ⬛ **Dave's, three ways:** name the log in the `:38` exclusion (one line, reversible) ·
move the append after the staging seam (larger blast radius) · stop tracking the log (loses its history).
⛔ Do not blanket-relax the clean-tree gate — it is doing its job on every other path.

**(2) P5 — the `--all-dirty` escape hatch is still awaiting the one-word verdict asked at #128.**
Live at `_git_commit.sh:15` (usage), `:50`, `:57`, `:302`, `:303`, `:311` — verified #137. A sub added it on its
own initiative and #128 disclosed exactly that: *"its construction, not your words — say the word if you want it
gone."* It restores stage-everything behaviour under a new name, after Dave retired `git add -A` at dream pass 4;
it does echo every path first, which is a real mitigation, and no harm has been observed in eight sessions.
**What is open is the dropped question, not the code.** ⛔ Do not remove it unasked — removing agent-added
machinery without his word is the same overreach as adding it was.
[born #137 · guards: `_git_commit.sh:38` and the `--all-dirty` sites · until: Dave rules each of the two]

### ⚠ NEW #137 — THE DREAM ARTEFACT BROKE ITS OWN CHECKED-CLEAR GREP, AND THE INDEX REPUBLISHES IT (born #137, MEASURED)

Dream pass 6's item **(cc1)** states *"a whole-tree grep for `github_pat_` and `ghp_…` returns **0 files**"* and
files it as checked-clear for future passes. **Re-run at #137, the same grep returns two files:**
`notes/_dream/2026-08-09-proposals.md` (lines 156, 205, 249) and `knowledge/_memento-index.json`, which indexed it.
✅ **There is no leak, and the finding is not that there is one** — all matches are the string inside backticks in
the dreamer's own prose *about* the grep. **The finding is that the artefact recording the all-clear is what
falsifies it**, and the index then serves the false line to anyone who retrieves it.
★ **Class: USE vs MENTION with no scope** — the same defect as `gate-must-quote-what-it-forbids`. Any credential
gate written to this grep will now fire forever on a file containing no credential, and the honest response to a
permanently-red gate is to stop reading it. **A secret-scanner must exclude quoted/backticked mentions, or scan
for the token *shape* rather than the prefix.** ⬛ Not proposed as a build here; recorded so the next pass does
not inherit cc1 as true. ⚠ **cc1's verdict — no credential material in the repo — is itself RE-VERIFIED and
STANDS.** Only its grep count is stale.
[born #137 · guards: `notes/_dream/2026-08-09-proposals.md` + cc1's claim · until: a scanner exists with USE/MENTION scope, or Dave strikes it]

### ⚠ NEW #137 — `_capture_gate.py --selftest` HAS BEEN RED SINCE #135 AND NO WRAP COULD SEE IT (born #137, **MEASURED BY THE #137 WRAP; SHAPE REPAIRED, 7 RESIDUAL ARE DAVE'S**)

**What was measured, on the artefact's own bytes:** `python3 knowledge/_capture_gate.py --selftest` exits **rc=1** with **1,739**
failures, every one of the form *"ruling `s137-D1` points at `p` which does not exist"*. Cause: `knowledge/_rulings.json` stores
`evidence` — and, from #136, `governs` — as a **STRING** on six records (`s135-D1`…`s135-D4`, `s136-D1`, `s137-D1`) where
`_governs.py:294` iterates the field as a **LIST of pointers**. Iterating a string yields characters, so the checker walked the prose
one letter at a time and reported each letter as a rotten pointer. **92 of 98 records use lists; the string is the anomaly, the
checker is right and the data is wrong.**

★ **THE REAL DEFECT IS NOT THE SHAPE — IT IS THAT NOTHING RUNS THE CHECK AT WRAP.** `_capture_gate.py --wrap` does **not** call
`_governs.selftest()`; the only consumer is `_capture_gate.py --selftest`, wired into `_build_all.py`, which is **sandbox-impossible**
(~49s vs the ~45s call kill) and therefore never runs here. So the red was invisible to #135, #136 and #137's wraps alike and all
three committed over it — [[instrument-without-a-consumer]], in the gate family that exists to prevent exactly this.
⚠ **ATTRIBUTED WITH A CONTROL, not assumed:** the selftest is RED against **HEAD's** `_rulings.json` as well, so **#135 introduced
the class** and #136/#137 widened it. #137 did not cause it and did not inherit a clean gate either.

✅ **SHAPE REPAIRED #137, BY ADDITION — no ratified byte was trimmed.** Every string field was wrapped in a single-element list
(the prose preserved verbatim), and `s137-D1`'s real path `knowledge/_git_commit.sh` was **PREPENDED** to its `governs` list.
**1,739 → 7 failures.** ★ The prepend was **driven both directions**, because a trigger index that cannot trigger is the one thing
this file exists to prevent: `_governs.py --file knowledge/_git_commit.sh` surfaced **only `d0802-P5`** before, and
**`d0802-P5` + `s137-D1`** after. *(`governs` entries are never existence-checked, so keeping the original prose as a second entry
is inert — that is why the addition costs nothing.)*

⬛ **THE 7 RESIDUAL FAILURES ARE NOT A WRAP SUB'S TO CLEAR, and that is the whole reason this entry exists.** Each is prose sitting
in an `evidence` field where a resolvable pointer is required — e.g. `s135-D4`'s `notes/_briefs/2026-08-08-135-laneA-kg-apply.md
(structural proof + exceptions ledger)`, a real path made unresolvable by its own parenthetical; `s135-D3`'s is `chat #135; …`,
which is not a path at all and also trips the anchor positive control. **Clearing them means TRIMMING ratified ruling records on
five inherited entries, and *add-never-trim* outranks a green.** The repair is cheap but it is a judgment call about ratified text:
split each string into resolvable pointers and relocate the parentheticals to `says` or to the dossier. **The file's own `_README`
already says which way it should go** — *"THIS FILE IS A POINTER INDEX, NEVER A SECOND COPY OF CANON"*.
★ **THE PRECEDENT WAS SEARCHED FOR BEFORE THIS REPAIR WAS KEPT, AND IT LICENSES EXACTLY THIS SHAPE OF FIX.**
§ OPEN `### ⬛ NEW #126 — _governs.py SELFTEST IS RED` records the same gate red for a different cause, and #126's
wrap refused to touch it: *"a wrap that fixes what it happened to trip over is a wrap that ruled its own scope."*
**#127 then repaired it — STRUCTURALLY and PURELY ADDITIVELY (+135/−0), re-pointing NOTHING** — and that is the
line this wrap held to: the container type was corrected by addition, and the six CONTENT decisions (which pointer
is the right one) were left untouched and are named above. ⚠ **If the conductor or Dave reads the line differently,
the repair is one `git checkout knowledge/_rulings.json` away from reverted** — it changed no ratified byte, which
is precisely what makes it cheap to undo.
⛔ **And the gate-don't-patch half, which is the durable finding:** repairing six records fixes six records. **Nothing parses
`_rulings.json` in its consumer's grammar** — no check asserts that `evidence`/`governs` are lists of resolvable pointers at write
time, which is why a malformed record shipped three times running. [[no-gate-parses-the-artefact]]. A wrap-mode call to
`_governs.selftest()` would have caught all three the day they landed; it is one line, and it is Dave's to license because it
turns a currently-silent condition into a BLOCKING one.
[born #137 · guards: `knowledge/_rulings.json` evidence/governs shape + the absence of any wrap-mode consumer for `_governs.selftest()` · until: the 7 pointers are authored into legal form and a parser gates the field at write time]

### ⬛ NEW #130 — THE ENACTMENT LANE: `s130-D4` / `D5` / `D6` + TABS + LEGACY REVERSED TEXT (born #130, RULED, **NOT ENACTED**)

**State:** RULED by Dave #130, recorded in `knowledge/_rulings.json` and `notes/_MEMENTO-DECISIONS.md` § ★★ #130
with the honest status *RULED #130 / NOT ENACTED*. **No value moved in any token file.** **Owner: Dave** — the
enactment licence is his word.
**Method (pointer, not body):** values half → `knowledge/tokens/*.json`; consumption half → the snippet corpus via
`gen_canon_components.py` + regen + gate replay. The full measured grid lives in
`reviews/CONTRAST-CONTROLLER-2026-08-08-v3.html`.
⚠ **Owed at enactment, not now:** legacy success `#00847F` + white sits **at** the 4.5 boundary and must be
**measured**, not assumed; legacy info moves toward `#4F77B0` per the `s122-D3` map.
⛔ **Dark mode:** Dave ratified *"(a) ~8%, (b) all three"*, but **two of the three already invert via the cascade**
and **the banner wash MUST NOT** (RAG fills are mode-invariant by his own `s122-D1/D2/D3`). **No machinery was
added and the discrepancy was declared back to him** — an enactor must not quietly add the third.

✅ **AMENDED BY ADDITION #131 — the LEGACY-REVERSED-TEXT half of this item is DONE.** `s131-D1` (Dave, #131)
ruled and enacted the legacy RAG fills from his own Figma values — error `#A8000B` · warning `#FFBB33` ·
success `#00847F` · information `#305A85`, white text **and** marks on error/success/information, amber the
sole dark-ink exception — which **supersedes the `#4F77B0` direction named above** and closes the
*"exact values owed at enactment"* clause. ⛔ **The REST of this item is UNTOUCHED: `s130-D4` / `D5` / `D6`
and tabs are still RULED-NOT-ENACTED.** Do not read the half as the whole. Evidence: `knowledge/_rulings.json`
§ `s131-D1` · `reviews/LEGACY-RAG-BANNERS-2026-08-08-s131-v1.html` · `gen_theme_cascade --check` rc=0 201/206.
[born #131 · guards: the `#4F77B0` and *"values owed"* text above · until: `s130-D4`/`D5`/`D6` are enacted]

### ⛔ NEW #131 — THE COMPONENT-SPEC KG IS IN NO INDEX AND NO CHECKLIST (born #131, REPORTED NOT REPAIRED, REMEDY IS DAVE'S)

**What was measured:** `knowledge/components/*.meta.json` — **76** (⚠ **MEASURED at the wrap and it corrected this session's own figure: the brief and every first draft said 78 — 78 is the DIRECTORY's entry count; 76 are metas, plus `meta.schema.json` and `_ACCESSIBILITY-CONFORMANCE.md`; 77 repo-wide, one lives at `knowledge/_proforma/icon-button.meta.json`. Registered as `ASSERT-009` so the count is re-tested, not repeated**) of component specification carrying
**token claims in prose** — is **NOT in the memento index**, and **no enactment checklist names it**.
`banner.meta.json` sat **stale against `s131-D1`** through the entire values-and-consumption enactment and was
surfaced **by Dave's own question**, not by any gate. It was then amended by addition (three claims) and
re-validated — the *file* is current; the *class* is not fixed.
**Class:** identical to #130's *"true when written, gone false, nothing re-checks it"* — the **fifth medium**.
⬛ **OWNER: DAVE — three options, none taken here:**
- **(a)** add the metas to the memento index (retrieval surfaces them; nothing checks them);
- **(b)** a **parse-gate** on meta token-claims — parse in the consumer's grammar, the strongest option;
- **(c)** an enactment-checklist line — cheapest, weakest; a convention with no gate is a preference.
⚠ **Dave's attached question, recorded so it is not lost: how IS the design KG used, indexed and checked?**
Honest answer as of #131: **used by hand · indexed nowhere · checked by nothing.** Narrative:
`_DECISION-HISTORY/2026-08-08-131-the-legacy-rag-fills-and-the-design-kg-nothing-checks.md` § Finding 3.
[born #131 · guards: the 76 `knowledge/components/*.meta.json` files + the count itself (ASSERT-009) · until: Dave picks (a), (b) or (c)]

### ⬛ NEW #131 — CONSOLE/SC LIGHTER INFORMATION BLUE: DIRECTION ONLY, NO VALUE (born #131)

✅ **CLOSED #132 — `s132-D1` (Dave, off the controller): fill `#5A85C1`, mark INK, RULED AND ENACTED END-TO-END; see `knowledge/_rulings.json` § `s132-D1` and the ⏱ LATEST delta.** The block below stands as history of the open state. [born #131 · closed #132 · guards: `_rulings.json` § `s132-D1` · until: rolls per 2d term]

`s131-D1` explicitly does **not** carry a console/SC information value — its own `watch` field says so:
*"console/SC lighter info blue is DIRECTION ONLY, no value picked — do not enact it under this ruling."*
**A controller is owed** (Dave rules from live controllers fast and in his own words). ⛔ **Nothing may be
enacted for console/SC under `s131-D1`.** Note also that this does **not** close the console/SC
**information-REST** contrast worklist items — those stay in the 4-REAL register below.
[born #131 · guards: `_rulings.json` § `s131-D1`.watch · until: Dave rules a console/SC value from a controller]

### ⚠ NEW #131 — A CONTROL THAT COULD NOT RUN: THE 156 VALIDATOR FAILS ARE ATTRIBUTED BY CONTENT (born #131)

`_validate_snippets.py` reports **156 ❌**. The intended `git stash` control **returned rc=1** — the known
zero-byte `.git/index.lock` on the mount — so **the with/without-diff control DID NOT RUN**. Attribution fell
back to **content**: no fail line names the minted slot `rag/text/on-information`; the **12 Banner fails are the
pre-existing #130 drift family** (mono base vs legacy-reference hexes) and this diff touches none of their
value-pairs. ⛔ **This is an honest UNPROVEN, priced as a TODO — not a pass.** The 156 are **reported, not
repaired** (repair is outside this session's licence).
[born #131 · guards: any later claim that #131 left the validator unchanged · until: a control runs, or Dave rules the 156]

### ⬛ DAVE'S — THE ERROR-MARK IMAGE CONFIRM (born #130, NOT RULED)

Dave sent an image that **did not arrive**. The conductor's provisional reading — *white shape, red glyph*, both
legs **6.02** — is recorded as **provisional** and is **not a ruling**. The mono `--mark-error` companion options
were measured: `#FFFFFF` **6.02** · `#F0F0F0` **5.28**. **Owner: Dave**; nothing may be enacted from the
provisional reading.

### ⬛ DAVE'S — MARK-vs-FILL 3.0 GATE: BUILD IT, OR PUT IT ON THE WORKLIST (born #130)

Asked at #130 and **not answered**. **Owner: Dave.**

### ⬛ NEW #130 — TWO RATIFIED WORKLIST ITEMS (born #130)

Ratified by Dave as **named worklist items**, not as rulings: **(a)** console + SC **information REST** contrast
failures, **3.81 / 4.13** · **(b)** legacy **success washed**. Both fold into the enactment lane above; neither is
enacted.

### ⬛ NEW #130 — `_validate_state_contrast.py --selftest` IS ENVIRONMENT-DEPENDENT AND SILENT ABOUT IT (born #130)

**Measured:** rc=**2** at **18** arms without `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-129`; rc=**0** at
**25** arms with it. It does **not** say which world it ran in. ★ **A selftest whose arm count depends on the
environment and does not declare it publishes a green that means two different things.** **Remedy proposed, NOT
built: a named refusal** [[honest-refusal-needs-a-legal-form]]. **Owner: Dave** (a refusal is a gate behaviour).

### ⛔⛔ NEW #130 — AN ANCHOR AIMED AT A ROLLING STACK IS GUARANTEED TO ROT (born #130, NOT RULED)

`s130-D2` repointed `s129-D1`'s rotten anchor at `GOOD-MORNING.md#### 2026-08-08 #129`, and **this ritual's own
step-2f roll then moved that stratum into `notes/_GAUGE-LOG.md`** — breaking the pointer for the **second
consecutive wrap**. ★ **The ritual itself is the thing that moves the target.** Repointed at the **append-only**
gauge log (a durable target); `_governs --selftest` rc=0 restored; **declared a MOVE, not a rot.**
⛔ **The general remedy — never anchor at a roll-eligible region, or have the mover repoint what it moves — is
NOT ruled here. Owner: Dave.**

### ⛔ NEW #130 — THE STATE-CONTRAST AUDIT'S BANNER 4.09 MEASURED THE WRONG BUTTON (born #130, NOT REPAIRED)

The 4.09 reading is the **chromed ghost** (`.abtn`, `knowledge/canon/canon.css:3959`), **not** the quaternary Dave
says ships. Under the true quaternary the **pressed failure DISAPPEARS (15.27)** and the failure **MIGRATES TO
REST** — **8 of 48 readings**, because `--button-quaternary-label-default` resolves to `--text-default`, page ink
on a RAG fill. ⛔ **The audit file and the snippet corpus were NOT touched: the snippet button-style question is
DAVE'S.** Related, recorded not acted on: canon and snippets **already disagree on error red**
(`#B92F1E`/`#CC4333` inline vs store `#F6604C`, which lives in `semantic-colour.json` and in no live component);
canon declares **no banner-scoped quaternary** and quaternary has **no pressed token** (hover == pressed), so the
press is **inexpressible** until `s130-D4` is enacted.

### ⬛ THE CARRIED SET — the residual list that has rolled every session, HOMED #125 by the EXIT CHECK
⚠ **This list has lived ONLY on the rolling banner/delta residual line for twelve sessions.** A banner is
a Polaroid: the moment its delta rolls, the item is unreachable from live state. The EXIT CHECK exists to
catch exactly this and it has been catching pieces of this list one at a time; **homing the whole set is
cheaper than homing it again next wrap.** ⛔ **Nothing here is ruled, re-scoped or closed by this wrap —
this is a POINTER block, and every method body stays at its pointer.**
- **`s116-D4` / `s116-D5`** — ruled #116, unenacted. → `knowledge/_rulings.json` · ledger § ★ #116.
- **`s114-D2`** — the adoption-time CITATION GATE, four binding conditions. → `GOOD-MORNING.md` §C·4,
  `#114`'s ruled-and-unbuilt set, item ③ (the one item of that set still open).
- **The STALE-MOUNT SEAM** — a mount can corroborate a stale premise; verify at boot against a source
  with a DIFFERENT CLOCK (`git log` vs mtime). Remedy unruled. → `_RUNBOOK-context-gauge.md`.
- **P4 — the `_CHAIN.md` trim.** Phase 4 of the #110 roll, priced at 14% of the boot floor, **not** the
  main event. ⚠ **P-SET COLLISION: two different P-sets share the numbers P4/P6/P7 and their statuses are
  OPPOSITE** — always name which set. → `notes/_MEMENTO-DECISIONS.md`:4049 ff.
- **`89-D2` — RULED, NOT ENACTED.** It lives **only** in `notes/_MEMENTO-DECISIONS.md`; the ruling store's
  count does not include it, so *"how many open rulings"* answered from the store is short by this one.
- **`ds-032`** · **`ds-025`** (boot-floor attribution; re-scoped #109) → `knowledge/_DS-IMPROVEMENTS.md`.
- **The BOOT-RENT PLAN (P2)** and **the ATTRIBUTION RE-PROBE** — ⛔ **DAVE'S, twelfth roll at #125.**
- **The FALL-THROUGH CLASS has no gate** (born #123) — see its own block below.
[born ≤#114 · homed #125 · guards: this block · until: each is enacted or ruled]

### ⬛ DAVE'S — P1 · G4 · the RECORDER CONSTANTS: three opens that had NO standing home (HOMED #125 by the EXIT CHECK)
⚠ **Copied up here at #125's wrap, and the reason is this session's own finding.** These three have
been carried as *"Dave's opens UNCHANGED"* on every banner since #113–#120, and #124's banner asserted
their standing home was *"`_LIVE-STATE.md` § OPEN"*. **That claim was never true** — only the chart-meta
enum edits were ever homed there. A pointer to a home that does not exist is the same class the whole of
#125 was spent on: a claim that reads as authoritative and that nothing re-checks. Homed, not ruled.
- **P1 — the boot-attribution split, AWAITING DAVE'S CONFIRM TO OPEN.** Phase 1 of the four-phase #110
  roll (`notes/_MEMENTO-DECISIONS.md`:4049): split the **56,308 unattributed** of the first-turn boot by
  tokenising what is actually on disk (skill frontmatter, `CLAUDE.md`, plugin manifests), the Cowork
  system prompt falling out as the residual by subtraction. P2 boot-rent · P3 boot-ceiling gate ·
  P4 `_CHAIN.md`'s 10,499 are the rest of that roll. ⛔ **Priced, seen by Dave, NOT opened — his word.**
- **G4 — GM §C over its warn cap.** `notes/_MEMENTO-DECISIONS.md`:3040: *"GM §C 191 > 150 warn cap →
  closes when Dave picks OFFLOAD / TRIM / KEEP."* ⛔ **The pick is Dave's; the cap is not to be moved.**
- **The conductor-surface RECORDER CONSTANTS — 3 MEASURABLY STALE, refresh is DAVE'S.**
  `knowledge/_surface_recorder.py` (RULED #112-D1, built #113) grades against real-token constants that
  the measurements have since drifted away from; the gate DECLARES the drift rather than hiding it
  (`_capture_gate.py` boot-drift line), which is the whole bar. ⛔ **Only Dave's ruling closes it.**
[born ≤#113 · homed #125 · guards: this block · until: Dave rules each]

### ⬛ DAVE'S — the 4 REAL state-contrast failures surfaced by `s125-D3` (born #125)
`s125-D3` taught `parse()` to read `color(srgb …)` and to REFUSE unreadable syntax by name; **20 false
failures vanished and 4 REAL ones appeared.** ⛔ **These are DAVE'S to rule — this wrap did not fix,
close or waive any of them, and no threshold was touched.**
- **Banner `.abtn:active` — 4.09:1, needs 4.5. LIGHT *and* DARK.** `knowledge/canon/canon.css:3963` /
  `:3975`. NEW, surfaced only because the parse refusal stopped fabricating a pass.
- **Pre-existing, also REAL:** Tabs ×2 DARK at **1.00:1** — `.cn-tabs .ovcount`, `canon.css:2496`, a
  genuine token collision (white on white in dark) · Selection-controls ×8 (light/pressed **3.95:1** ×6,
  dark **3.66:1**).
[born #125 · guards: this block · until: Dave rules the four]

### ✅ ENACTED #126 — `s125-D1`: the chain banner's build-step count is a GENERATED figure (born #125, enacted #126)
**Dave ruled** at #125 that the build-step count in the chain banner stops being a typed number and becomes a
**GENERATED figure** — `knowledge/_gen_chain.py` reads `len(STEPS)` out of `knowledge/_build_all.py`'s
AST at generation time. He chose this **over a third re-stamp**, explicitly. ✅ **ENACTED #126.**
`_gen_chain.py` carries `BUILD_VERDICT_MARK` · `VERDICT_SHA = "18c7789"` · `BuildStepCountError` ·
`_steps_in()` (AST) · `build_steps_now()` · `build_steps_at()` · `build_verdict_line()`; the **splice** is a
20-line purely-additive block in `_capture_gate.chain_parts()` — **the one slicer**, because `read_chain_tk`
measures exactly what it returns and `_gen_chain` writes exactly what it returns, so a downstream injection
would be **written but not measured** (#41's second-consumer drift). ⚠ **That placement differs from the
ruling's literal wording (`_gen_chain`) and is declared as an IMPLEMENTATION RECONCILIATION, not a
re-ruling — flagged for Dave's eye** [[instruction-right-cause-wrong]]. **BOTH ends are measured and the
shortfall is computed**, because publishing only the live count would have manufactured *"ALL 98 STEPS
ASKED AND GREEN"*, a sentence nobody measured. ★ **The premise proved itself inside one day: 97 at #125's
probe, 98 at #126's enactment** — `s125-D2` added a step in between. **12 mutation bites 0 fail · 5
permanent bites wired into `_gen_chain.selftest()`, the load-bearing one re-deriving `len(STEPS)` from disk.**
⬛ **The 23-step shortfall it exposed is a SEPARATE open item — see the block below.**
Ledger: `knowledge/_rulings.json` (`s125-D1`, status + `enacted`) · `notes/_MEMENTO-DECISIONS.md` § ★ #125 / § ★ #126.
[born #125 · enacted #126 · guards: `_gen_chain.selftest()`'s 5 bites + `--check` as a build step · until: closed — kept 2 sessions per the tombstone term]

### ⬛ NEW #126 — 23 BUILD STEPS HAVE NEVER BEEN INSIDE ANY GREEN VERDICT
Surfaced by `s125-D1`'s enactment and **statable only because both ends are now measured**: the `#62` green
verdict covers the **75** steps that existed at `18c7789`; disk holds **98**. ⇒ **23 steps have never been
asked inside a green single-process build.** ⚠ **This is a FINDING, not a failure** — it says nothing about
whether those 23 steps pass; it says the published verdict has never covered them. A full single-process
`_build_all.py` run is sandbox-impossible (~49s vs the ~45s call kill), so **closing this belongs to CI**.
⛔ **Nothing here is ruled, waived or scheduled by this wrap.**
[born #126 · guards: this block + the generated `_CHAIN.md` verdict line · until: a green verdict covers all 98, or Dave rules the chase closed]

### ⬛ NEW #126 — `_governs.py` SELFTEST IS RED: `s121-D1` POINTER ROT (`canon.css:5548` absent)
`knowledge/_capture_gate.py --selftest` fails inside `_governs.py`: the ruling **`s121-D1` points at
`knowledge/canon/canon.css:5548`, and that line does not exist.** ⚠ **PRE-EXISTING, and the attribution was
CHECKED rather than assumed** — `_governs.py` and `canon.css` are untouched in `git status`, and #126's
`_capture_gate.py` diff is 20 lines with **0 deletions**, gated behind a marker-presence test
[[attribute-the-diff]]. ★ It is the same class the whole of #125 was spent on, in a fourth medium: **a
POINTER that was true when written and nothing re-checks it** [[no-gate-parses-the-artefact]].
⛔ **Found #126 by an attribution control, deliberately NOT fixed — the repair is someone's to rule, and a
wrap that fixes what it happened to trip over is a wrap that ruled its own scope.**
[born #126 · guards: this block · until: the pointer is re-anchored or Dave rules it]
⛔ **CORRECTED #127 — AND THE CORRECTION IS THE FINDING: BOTH HALVES OF THE BLOCK ABOVE ARE FALSE.**
The block above states that `s121-D1` points at `knowledge/canon/canon.css:5548` and that *"that line does
not exist"*. **MEASURED #127 — both halves wrong.** (a) `_rulings.json` points at **bare `canon.css`**; the
record above **silently added the `knowledge/canon/` prefix**, and that is what hid the real defect — a path
**never resolvable from repo root**, so the entry was **BORN RED at #121**, not rotted into red. (b) Line
**5548 DOES exist** — today it reads `--alpha-84: 0.84;`. ⚠ **A repair driven off that sentence would have
gone GREEN pointing at an unrelated token.** The construct the ruling actually cites (the RAG roundel policy)
had drifted **5548 → 6451**: 903 lines in 5 sessions.
✅ **REPAIRED STRUCTURALLY, NOT RE-POINTED.** `knowledge/_governs.py` gained the anchor-pointer form
`<path>#<literal>` — `is_anchor_pointer()`, `resolve_anchor()`, wired into `render()` and `selftest()`,
**+135/−0 purely additive** — with the **line number derived at read time and stored nowhere** (the
`_steps_in` shape) [[no-gate-parses-the-artefact]]. `_rulings.json` **±2 lines, round-trip byte-verified, no
serializer reformat** [[serializer-defaults-reformat-the-file]]. **7 mutation bites, all RED as designed,
every restore sha256 byte-exact.** `_governs --selftest` **32 → 30** failures.
⚠ **The wrong text above is KEPT VERBATIM, not edited** — a record correction that deletes the false claim
destroys the evidence that the claim was believed, and this one was believed for a whole session.
[born #126 · CORRECTED #127 · guards: the two false halves above · until: #128 verifies this correction]

### ⬛ THE MEMENTO SCHEMATIC — v2 GENERATED, v1 KEPT AND TOMBSTONED (born #125, NEITHER DONE)
**A schematic already exists and nothing pointed at it:** `reviews/MEMENTO-SCHEMATIC-2026-07-26-v1.html`
(commit `f783008`), **hand-authored, referenced by NO generator.** It states *"27 blocking validators in a
55-step build"*; disk today is **30 validators, 98 steps**. It also draws a **different subject** — the
dream-pass lane — not the six subsystems #125 was asked for. **Dave's disposition: v2 GENERATED (so it
cannot drift), v1 KEPT and TOMBSTONED.** ⛔ **Neither has happened; both roll to #127 — the SECOND roll.**
⚠ The v1 file is still live and still asserts the stale figures — that is instance 1 of the through-line in a
second medium. ⛔ **#126 opened with this as half its named lane and never reached it**: the window ran out at
FILL 135,735 and the wrap was delegated rather than ridden. ★ **Two consecutive sessions have now been titled
partly for this and not built it** — that is a pricing finding, not a motivation one: **the schematic has never
been given a window of its own.**
[born #125 · rolled ×2 (#126, #127) · guards: this block · until: v2 lands and v1 carries its tombstone]
✅ **CLOSED #127 — BOTH HALVES LANDED, THIRD TIME ASKED.** `knowledge/_gen_schematic.py` (~1,058 lines) →
`reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html`: **seven panels** (the six subsystems — chain · store ·
search · marks · gates · package — plus a self panel), **39 rows, every figure read off disk at generation
time**, inline SVG, no CDN. Build-step counts come from `_gen_chain._steps_in` — **the function itself,
never a copy** (ONE slicer, `s125-D1`). ★ **Each panel COMPUTES its own "what re-checks this"** from `STEPS`
× `ROUTE_ROWS` and renders a red **NOTHING RE-CHECKS THIS** where the answer is none — **it fired that about
ITSELF until the wiring landed** (§ 98 → 102 below). **v1 KEPT and TOMBSTONED — +29/−0, purely additive, its
stale figures deliberately untouched**: Dave's #125 disposition, enacted verbatim. Wired into `_build_all.py`
as three steps (build · `--check` · `--selftest`) each with its `ROUTE_ROWS` row.
⚠ **v2 IS A REVIEW ARTEFACT AWAITING DAVE** — registered in `knowledge/_REVIEW-SIGNOFF.md` at this wrap.
[born #125 · rolled ×2 · CLOSED #127 · guards: `_gen_schematic.py --check` (wired, blocking) · until: n/a]

### ★★ OPEN, NO GATE — TWO `_validate_state_contrast.py` DEFECTS, FOUND AND DELIBERATELY NOT FIXED (born #125)
Found while proving `s125-D3`, scoped OUT of it on purpose so the ruling's mutation test proved one
clause and not a bundle [[mutation-tests-the-clause-not-the-feature]].
- **`effBg` walks ANCESTORS ONLY.** It cannot see an absolutely-positioned **SIBLING** that paints the
  selected pill, so it measures the wrong background ⇒ **32 FALSE failures**: Segmented-control ×12 ·
  Charts ×16 · View-options ×4. **Real rendering is fine.** Distinct from `s125-D3`, which was a *parse*
  defect; this is a *geometry* defect.
- **`out[3] = <headline>` OVERWRITES instead of inserting** — it eats the first snippet's heading. The
  committed `knowledge/_STATE-CONTRAST-AUDIT.md` claims *"across 38 snippet(s)"* and contains **37**;
  `Accordion` was eaten. ⚠ **AND, measured at this wrap: with ZERO snippets in scope the same line raises
  `IndexError: list assignment index out of range`** — the defect is not only an overwrite, it is a crash.
  ⚠ **Also observed at this wrap: `_validate_state_contrast.py` has NO `--selftest` flag and silently
  treats an unknown argument as a snippet-name FILTER** — an unknown that is defaulted rather than named
  [[measuring-tool-must-not-guess]]. **Not fixed, not ruled — recorded.**
- ⚠ **The artefact is STALE by 37:** `_STATE-CONTRAST-AUDIT.md` covers 38 snippets; `knowledge/snippets/`
  holds **75** `*.reference.html` (measured at this wrap). It has not been regenerated.
[born #125 · guards: this block · until: each is fixed or ruled]
✅ **FIXED #127 — BOTH, WITH THE BOUNDARY PROVEN AND NOTHING WAIVED.**
- **`effBg` — the class was not "ancestors only", it was the MODEL.** It modelled the paint stack as the
  ancestor chain **when painting is a z-ordered geometry of boxes**; ancestors are a subset, so it was
  **blind by construction** to an absolutely-positioned sibling. It now composites the browser's own hit
  stack (`elementsFromPoint`, paint order, src-over).
- **`out[3]` — a derived summary written into a positional slot the loop above owns.** Now an INSERT. The
  eaten `Accordion` heading is back, and the zero-snippet `IndexError` is a **named refusal**. Added
  `verify_report()` (`StateContrastReportError`), `--selftest` (**19 arms**), `--help`, and named refusals
  for an unknown argument and for a filter that matches nothing [[measuring-tool-must-not-guess]].
- ★ **THE BOUNDARY, PROVEN — TEXT failures 46 → 14: exactly the 32 NAMED false failures removed**
  (Segmented-control ×12 · Charts ×16 · View-options ×4), **ZERO added**. **All 4 REAL failures survive with
  IDENTICAL ratios** — Banner `.abtn:active` **4.09:1** ×4 · Selection-controls **3.95:1** ×6 + **3.66:1** ×2 ·
  Tabs dark **1.00:1** ×2 — **still red, nothing waived, nothing re-thresholded.** **Independently confirmed
  by a second instrument sharing no code**: screenshot pixels read **21.0:1** where the gate had said 1:1.
- ✅ **`_STATE-CONTRAST-AUDIT.md` REGENERATED — 14 failures / 75 snippets**, and the **stated count and the
  real count are asserted equal by the script on every write**. Coverage **38 → 75**, which makes the
  *"stale by 37"* bullet above **HISTORICAL**.
- **8 mutation bites, one clause each, byte-exact restore after every one** — including **M5, the boundary
  guard: a "fix" that stops failing by ceasing to report goes RED** [[green-tests-cannot-see-scope]].
[born #125 · FIXED #127 · guards: the 19 selftest arms, now a wired build step · until: n/a]

### ⬛ DAVE'S — DECLARE-vs-REFUSE on the 15 UN-HIT-TESTABLE BOXES (born #127)
> ✅ **CLOSED #129 — `s129-D3`, Dave's call: DECLARE, as named holes.** `_validate_state_contrast.py` selftest arms **19 → 25, rc=0** (conductor-replayed); the audit was regenerated and holes moved **15 → 14**, ⚠ **and that one-hole delta was ATTRIBUTED, not claimed** — a `git show HEAD` control run ×3 puts it on the browser build, not on `s129-D3`'s emit condition, whose logic is unchanged apart from the added `reason` [[attribute-the-diff]]. ⛔ **The 4 REAL failures are byte-identical and still red — nothing was waived.** *(evidence: `knowledge/_validate_state_contrast.py` · `knowledge/_STATE-CONTRAST-AUDIT.md` · 2026-08-08)*

⚠ **The sub's first implementation was WRONG TWICE, and measurement caught both**: ignoring element
`opacity` **invented 12 failures**; **refusing** un-hit-testable boxes turned **60 measured records into
holes**. ★ **Both were visible only because it captured the WHOLE corpus instead of trusting the headline**
[[green-tests-cannot-see-scope]]. **15 boxes remain that `elementsFromPoint` cannot hit** (off-screen,
zero-area, or fully occluded at probe time). The shipped build **DECLARES** them rather than refusing them.
⛔ **Which posture is right — DECLARE (a stated approximation) or REFUSE (a named hole) — is DAVE'S.**
[born #127 · guards: this block · until: Dave rules the posture]

### ✅ CLOSED #130 — `_capture_gate.py --selftest` IS GREEN: the 30 pointer entries are repaired (born #127, closed #130 under `s130-D1`+`s130-D2`)

**`_governs --selftest` 32 FAILs → rc=0 · `_capture_gate --selftest` rc=0 — GREEN FOR THE FIRST TIME SINCE #121.** Class B filled from Dave's ratified records (10 drafts, all ratified); class C reshaped to `#127` anchors; **9 legacy pointers converted, NOT the recorded 11 — delta declared, the stale `+11` at line 75 deliberately NOT corrected.** ⚠ The #129 boot measured **32**, not the published 30: the two extra were `s129-D1`'s own anchor, **born red** at the #129 wrap's 2f roll. **The record below is kept verbatim.**

### ⬛ NEW #127 — `_capture_gate.py --selftest` IS STILL RED: 30 POINTER ENTRIES, NOT ONE
⛔ **HONEST STATE: `_capture_gate.py --selftest` rc=1.** The #126 record above called this *"one rotten
pointer"*; **the gate reports only `fs[0]`**, so "one" was never the count. With `s121-D1` repaired,
**30 remain**, in three classes:
- **class B (18)** — `s122-D1…D5`, `s123-D1…D4`, `s124-D1`: missing `evidence` / `status`. ⛔ **Filling these
  means asserting what Dave ruled.** Not a mechanical repair, and HIS.
- **class C (12)** — `s125-D1` / `s125-D2` / `s125-D3`, where `evidence` was used as a PROSE field.
  Mechanical in shape, but it re-writes ruling records.
- **+11 further entries still use the old `<path>:<int>` form — green, unverifiable, and currently
  INVISIBLE to the gate.** ★ **A form that cannot fail is not a passing form.**
⛔ **ALL NOT FIXED at #127. Recorded, left.**
[born #127 · guards: this block · until: Dave rules class B and licenses the class-C + legacy repairs]

### ⬛ DAVE'S — GENERATE-vs-RE-STAMP the `_build_all.py` COMMENT *and* THE REMEDY STRING (born #127)
> ✅ **CLOSED #129 — `s129-D2`, Dave's call: GENERATE.** `_build_all.py` gained `state_contrast_caveat()` and selftest arm **(d)**; the caveat is now computed rather than typed, which is the only disposition the class permits after a claim has gone false three times. **`--selftest` PASS, 102 steps**, conductor-replayed. *(evidence: `knowledge/_build_all.py` · 2026-08-08)*

The state-contrast comment in `knowledge/_build_all.py` **went false for the second time in two consecutive
sessions**, inside the file that enforces the rule against exactly this. ⚠ **And a THIRD instance sits
beside it**: the gate's `ROUTE_ROWS` **remedy string still carries the `s125-D3` parse caveat, which was
FIXED at #125** — #127 measured **0 parse refusals across all 75 snippets**, before and after.
⛔ **The comment was corrected; the remedy was DELIBERATELY NOT hand-corrected a third time.** It is left in
place **as EVIDENCE**, with the decision raised to Dave: the standing remedy for a claim that rots twice is
***GENERATE it, do not re-stamp it*** (`s125-D1`'s precedent), and a third hand-correction is the exact move
that ruling exists to forbid [[no-gate-parses-the-artefact]] [[gate-dont-patch]].
[born #127 · guards: this block + the comment stratum in `_build_all.py` STEPS · until: Dave rules generate-vs-re-stamp]

### ⬛ DAVE'S — ⛔/★ GLYPHS vs ASCII IN GENERATED REVIEW ARTEFACTS (born #127)
> ✅ **CLOSED #129 — `s129-D4`, Dave's call: ASCII in the MACHINE STORE, glyphs in the PROSE.** `knowledge/_rulings.json` now holds **0 non-ASCII**, 15 glyphs mapped; the file was **round-tripped and byte-verified before writing** so the diff carries the semantic change and nothing else [[serializer-defaults-reformat-the-file]]; `_governs.py --selftest` **30 → 30 with an empty diff** — the store changed and the verdict did not. ⚠ **Scope: the MACHINE STORE. Prose surfaces (this file, GM, the ledgers) keep their glyphs by the same ruling** — do not read this as a repo-wide ASCII rule. *(evidence: `knowledge/_rulings.json` · `knowledge/_governs.py` · 2026-08-08)*

Raised by the schematic build: the generated HTML carries the same ⛔/★/⚠ vocabulary the written record uses.
It is a legibility and house-style call about **generated artefacts**, not about the record. ⛔ **UNRULED —
Dave's.**
[born #127 · guards: this block · until: Dave rules]

### ⬛ OVERDUE #127 — THE DREAM PASS, RAISED BY DAVE AND NOT RUN
> ✅ **CLOSED — AND IT WAS ALREADY CLOSED BEFORE #129 OPENED.** The pass RAN at #128 (`6836c5a`, 07:57 — `notes/_dream/2026-08-08-proposals.md`, 3 proposals), and a #128 session then **enacted all six 2026-08-02 rulings** (`d74552e` 08:20, `ed4ce3a` 09:08), so **dream-pass P1 was overtaken by events within two hours of being written.** ★ **#129 discovered this at boot by checking `git log` rather than by trusting the carried residual** [[premise-ages-faster-than-rule]] — and the shape of the miss is the session's own finding: **a proposal is a CONCLUSION about repo state with nothing re-checking it** (`s129-D5`). ⬛ **P2 and P3 remain, in reduced form — see the two new blocks below.**

Dave raised the dream pass **mid-session at #127**. It did not fit the window: **a sub's report alone costs
more FILL than remained before the wrap-open line**. ⛔ **Rolled to #128 as the FIRST item, deliberately,
rather than started and abandoned** [[stop-line-repriced-93]]. ★ Recorded as **OVERDUE**, not as a queue
item — it is the only thing on the #128 list that **Dave asked for out loud and did not get**.
[born #127 · guards: this block · until: the pass runs]

### ⛔ NEW #127 — THE OPENER'S BUDGET ARITHMETIC WAS WRONG: A RESERVE ON A RESERVE
The #127 opener treated **150,929 as the ceiling and then subtracted the wrap AGAIN**, reporting **~30K** of
job room when the real figure was **79,012**. **Dave caught it**, verbatim: *"150,929 is the line at which it
is recommended you start the wrap, not the limit"* — **200,000 is working, 256,000 is the absolute hard stop,
and 150,929 is DERIVED as `wall − wrap`.** ★ **This is a RESERVE ON A RESERVE — the exact defect named in
`_gauge_tokens.py`'s own comments, eleven lines above the constant that was quoted** [[read-chain-is-where-staleness-is-free]].
⚠ **IT MATERIALLY AFFECTED A DECISION:** Dave chose to delegate the schematic against an **understated**
budget. The delegation succeeded, **but the stated reason was wrong, and the pick was declared RE-OPENABLE,
not settled.** ✅ **Inscribed by ADDITION** at `knowledge/_RUNBOOK-context-gauge.md` § The Red trigger —
**no constant was moved and no cap was touched.**
[born #127 · guards: this block + the runbook addition · until: a wrap-open computes job room as `stop line − current FILL` and says so]

### ⚠⚠ CONTRADICTION — TWO FIRST-HAND SANDBOX READINGS OF THE PLAYWRIGHT DOWNLOAD (born #125)
> ✅ **ADJUDICATED #129 — owed since #126, re-owed at #127 and #128, and settled by the conductor's OWN first-hand run rather than by picking a side of the record.** **The download WORKS: exit 0, a 340M `chromium_headless_shell-1234` landed at `/var/tmp/pw-browsers-129`. TLS-blocked did NOT reproduce.** ★ **Neither sub was wrong about what it saw; both were reading the ENVIRONMENT and calling it the network.** Two real culprits, both now named in the runbook: **(a) ENOSPC on the 98%-full SHARED `/sessions` volume presents as *"Download failure, code=1"*** — set `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/…` and run `df -h $HOME` before blaming the network; **(b) `/tmp` is SHARED ACROSS SESSIONS**, and a foreign session's stale `pwdl.log` was served to #129's own first probe as its evidence — use unique log paths under `$HOME`. `knowledge/_RUNBOOK-render-verify.md` amended **BY ADDITION**, a dated 2026-08-08 stratum at the head; ⛔ **no dated stratum was edited or deleted** — the file already held both readings stratified by date, and quoting one stratum is not reading the file. ⚠ **THE SANDBOX IS THE SEVENTH MEDIUM of the `s129-D5` class:** a fence about the environment, true when written, with nothing that re-checks it. *(evidence: `knowledge/_RUNBOOK-render-verify.md` · 2026-08-08)*

⛔ **RECORDED, NOT ADJUDICATED. No winner was picked, nothing was averaged, and
`knowledge/_RUNBOOK-render-verify.md` was NOT edited on either basis.** Two Opus subs, same session,
same sandbox family, opposite observations — both first-hand:
- **Sub 1:** the `_validate_state_contrast.py` exemption reason (*"`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`
  on all 3 CDNs"*) **was never true** — it observed the **download SUCCEED**, with the installer then
  throwing `EPERM … rmdir '__dirlock'`. **A failure message AFTER a success** — a shape
  `_RUNBOOK-render-verify.md` explicitly banks.
- **Sub 2:** playwright's node downloader **IS** TLS-blocked on all 3 CDNs, and `NODE_EXTRA_CA_CERTS`
  does **not** fix it, while `curl` reaches the same URLs fine. It installed chromium **by hand** to
  `/tmp/pw-browsers` (needs `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers`,
  `LD_LIBRARY_PATH=/tmp/extralibs/usr/lib/aarch64-linux-gnu`).
- **Third datapoint, this wrap, and it adjudicates NOTHING:** sub 2's hand-installed browser was still
  present at `/tmp/pw-browsers` and a real chromium launched from it, while playwright's own default path
  `~/.cache/ms-playwright/` did not exist. **This says the workaround persists; it says nothing about
  whether the downloader is blocked**, because no download was attempted at this wrap.
⇒ **`_RUNBOOK-render-verify.md` needs a RE-VERIFY** — a fresh, deliberate download attempt whose
result is written down. ⚠ **Until then, do not carry either reading forward as a fact**: a fence
inherited as a fact is a premise, and premises age faster than rules [[premise-ages-faster-than-rule]].
⛔ **OWED AT #126 AND NOT DONE — NOW OWED AT #127.** #126 spent its window on `s125-D1` and stopped at the
stop line; **no download was attempted, no reading was adjudicated, and `_RUNBOOK-render-verify.md` is still
NOT edited.** ⚠ **Both readings remain recorded verbatim above and neither has been promoted** — a second
session declining to adjudicate is not a quiet win for either sub.
⛔ **STILL NOT DONE AT #127 — now owed at #128.** #127 spent its window on the schematic, the
wiring, `_governs.py` and the two contrast defects; **the re-verify was not started.** ★ A second
session declining to adjudicate is not a quiet win for either sub.
[born #125 · re-owed #127 · guards: this block · until: a session re-verifies the runbook end to end]

### ✅ CLOSED #130 — the #128 WRONG-SUBJECT DEFECT IS FIXED AT ITS CAUSE (`s130-D3`, Dave's pick from three)

**T3 GENERATES, NEVER INHERITS.** Non-wrap commits never read the banner (subject = `SESSION_N` witness + `date` + the msgfile's own first line; **REFUSES** without `SESSION_N` or on an empty first line); `--wrap` **asserts the banner's `#N` == `SESSION_N` and REFUSES on mismatch**. **5 mutation arms verified**, subject-fold blank line intact, `bash -n` clean. ⚠ **The two #128 commits themselves are NOT rewritten** — history stands, per the standing no-rewrite ruling. **The record below is kept verbatim.**

### ⚠⚠ NEW #129 — DAVE'S: BOTH #128 COMMITS CERTIFY THE WRONG SESSION (found, NOT diagnosed, NOT repaired)
**The fact, checkable in one command.** `git log --format='%h %s'` shows `d74552e` and `ed4ce3a` (both
2026-08-08, both #128's enactment of the six 2026-08-02 dream-pass rulings) carrying the subject
*"after #127 2026-08-07 — ✅ **THE SCHEMATIC v2 LANDED…**"* — **#127's banner text** — while `d74552e`'s
**own message body asserts** *"this message's first line deliberately begins with '#128'"*. **That claim
is false as committed.**
**Two candidate causes, NEITHER eliminated, and the difference matters:**
- **(a) the msgfile's first line was genuinely wrong**, in which case the `#124` subject assert did
  exactly its job and **faithfully certified a wrong line** — the gate is sound and the input was not; or
- **(b) the assert did not bite**, in which case the gate built at #124 is not running on this path and
  every subject since is uncertified.
⛔ **NOT diagnosed further and NOT repaired at #129 — this is DAVE'S**, and it is #130's opening item.
★ **The class is this session's own ruling in the git log:** the body's claim about its own first line was
a **conclusion inscribed at write time with nothing re-checking it at commit time** (`s129-D5`); a subject
line is the **sixth medium** on that list. ⚠ **A live regression check ran at #129's own wrap** — this
session's msgfile first line begins `#129 2026-08-08 — ` and the post-commit subject was verified equal to
it — **so whatever failed at #128 did not recur at #129; that is one datapoint, not a diagnosis**
[[a-skipped-wrap-makes-the-chain-certify-the-wrong-session]] [[invariant-cannot-discriminate-reversal]].
> ★★★ **DIAGNOSED AT THIS SAME WRAP — AND THE DIAGNOSIS COST ONE FALSE CLAIM, STRUCK HERE AT ITS SOURCE.**
> The two candidate causes above were written before the wrap committed. **The wrap then reproduced the
> defect on its own first commit (`29b4c2e`), which is how the mechanism was found:**
> - `knowledge/_git_commit.sh`'s **T3 block (#77-D2) REPLACES the msgfile's first line** with a headline
>   **derived from `GOOD-MORNING.md`'s ★ LATEST banner** — the msgfile's own line 1 is discarded, by design.
> - **#78-D3 prefixes `"after "`** to that headline **on any commit not run with `--wrap`**.
> ⇒ **a non-wrap commit inherits whatever banner happens to be on disk.** #128 wrote no banner at all, so
> both of its commits inherited **#127's**. **Neither candidate cause above is right as stated:** the
> msgfile's first line was never consulted, and the assert did not fail to bite — **it compares the
> REWRITTEN msgfile to the commit subject, so it is TRUE and USELESS for this question.**
> ⛔ **STRUCK: this session's own banner briefly claimed *"post-commit subject verified equal to msgfile
> line 1"*.** That was written before the commit ran and **was false the moment it was written** — the
> exact class `s129-D5` names, committed by the session that ruled it [[assertion-propagation-gap]].
> ⛔ **STILL NOT FIXED, AND STILL DAVE'S.** The mechanism is DESIGNED behaviour (#77-D2 + #78-D3), not a
> bug: the remedy — whether T3 should refuse when the banner's session number disagrees with `SESSION_N`,
> whether the assert should compare the ORIGINAL line 1, or neither — is a ruling, not a repair.
> ✅ **#129's real wrap commit was re-run as `SESSION_N=129 … --wrap`**, which takes the unprefixed path.
[born #129 · guards: this block · until: Dave rules the autopsy]

### ⬛ CARRIED, REDUCED #129 — dream-pass P2 (the residual's ordinal) and P3 (the sweep risk)
⚠ **Both were verified at #129's wrap rather than re-asserted from the proposals file, and both moved —
so they are carried in their REDUCED form, not their original one.**
- **P2 — HALF ANSWERED.** The half about **AGE** is ruled and enacted: #128's P2 ruling put
  *"every carried item is written with its AGE in sessions"* into `_RUNBOOK-capture-ritual.md` § 2c
  (FORMAT ONLY — no threshold, no cap, no gate; the age is REPORTED, never acted on), and **#129's
  residual is the first to use it**. ⬛ **The other half stands:** the ordinal that counts the rolls
  (*"FIFTEENTH roll"*) is still **hand-typed prose that nothing reads or checks** — `_roll_state.py`
  generates the 2c/2d/2f residual line but not the carry ordinal. **A count nobody can re-derive is a
  conclusion, not a measurement** [[measure-dont-convert-units]].
- **P3 — LARGELY CLOSED, and the closure was verified not assumed.** The predicted sweep mechanism is
  **gone**: `knowledge/_git_commit.sh` no longer contains `git add -A` (retired by d0802-P5, enacted #128);
  the only staging call is now `git add -- "$_p"` at `:257`, over paths named explicitly by the caller.
  ⬛ **The residue is real but smaller:** `notes/_dream/` is still **outside the gate glob by ruling**
  (A-D4), so nothing checks the lane's output — it simply can no longer be swept in by accident.
[born #128 · reduced #129 · guards: this block · until: the ordinal is generated / A-D4 is revisited]

### ★★ STANDING #129 — `s129-D5`: VERIFIED IS A PROPERTY OF A MOMENT, NOT OF THE ARTEFACT
**Dave's words, mid-turn, ratifying the conductor's 5-whys:** *"verified is a property of a MOMENT, not
the artefact; every inscribed conclusion is DEBT with three options: generate / named re-checker / expiry."*
★ **The root the 5-whys reached: the system stores CONCLUSIONS where it should store GENERATORS.** The
media on the record, seven and counting — **prose** (#125's *"the 75"*) · **a comment** (an exemption's
reason) · **a return value** (`parse()` faking `{"ratio":1}`) · **a pointer** (`_governs.py`) · **the
record of a defect itself** (`_LIVE-STATE.md:457`, false in both halves) · **a commit subject** (#128,
block above) · **the sandbox environment** (the playwright fence, block above).
**Enacted, minimally and by addition:** the standing hunt **"Conclusions that could be queries"** in
`.claude/agents/dreamer.md`; recorded at `notes/_MEMENTO-DECISIONS.md` § `s129-D5` and in
`knowledge/_rulings.json` (**77 ids**). ⛔ **NO gate, NO threshold, NO expiry term was set** — the three
options are Dave's vocabulary for choosing a remedy per item, not a policy this wrap may apply on his behalf.
[born #129 · guards: this block + the dreamer hunt · until: Dave scopes a remedy tier]

### ⬛ DAVE'S — the 3 chart-meta PROVENANCE-ENUM edits (born #120, HOMED #123 by the EXIT CHECK)
⚠ **Copied up here at #123's wrap because it had NO standing home** — it lived only on the #120
delta and the rolling banners, and #120's delta rolls at this wrap (ritual 2c/2d EXIT CHECK).
#120's build repair set `"provenance": "worker-composition" → "code"` in three chart `meta.json`
files (`Chart-histogram`, `Chart-butterfly-v`, `Chart-butterfly-h`), keeping the worker context in
each `$note`. The integrity gate is PASS on it. **It is a judgment call, flagged for Dave's eye and
never ratified** — three sessions running it has been carried as "unchanged" without a home.
[born #120 · homed #123 · guards: this block · until: Dave looks at the three enums]

### ✅ CLOSED #123 — the SIX parked consequences of the #122 mark-map pass (born #122, closed #123)
**ALL SIX ARE CLOSED**, by four rulings taken with the rendered artefact in front of Dave:
`s123-D1`…`s123-D4` (`knowledge/_rulings.json` entries 58–61) plus the **v6 controller sign-off**
(*"mega"* — `knowledge/_REVIEW-SIGNOFF.md`, which closes consequence 6 and was the licence for the
rest). Arc: `_DECISION-HISTORY/2026-08-07-123-rag-world-signoff-and-tint-opacities.md`.
1 → `s123-D1` legacy warn/info backgrounds **RESTORED** `#F0B13A`/`#7DABCD`, declared in legacy's
overrides · 2 → `s123-D2` `ownsHexes` **REFRESHED**, provenance re-run **37 UNCHANGED** (so none of
the 37 was an artefact of the stale map) · 3 → `s123-D4` SC badge shift **RATIFIED** (*"SC badge is
fine"*) · 4 → the **4.56** white-on-teal legacy success leg **ACCEPTED with the v6 pass** · 5 →
`s123-D3` tint scope **RULED + ENACTED IN FULL** (legacy+SC solid · mono+console tuned opacities;
**AMENDS ds-026** — alpha is no longer state-changes-only, Dave ratified *"this is fine"*) · 6 →
**DRIVEN VISUALLY**, v6 SIGNED OFF.
⛔ **Do not re-open.** [born #122 · closed #123 · guards: `_rulings.json` 58–61 + `_REVIEW-SIGNOFF.md`
+ this line · until: term elapses at #125]

### ✅ CLOSED #124 — the memento-package DELTA-AUDIT RE-BASELINE (born #120, blocked on #64/#114, closed #124)
**The word was TAKEN and then SUPERSEDED SAME SESSION BY ITS OWN ENACTMENT.** Dave first ruled **WAIT** —
the package red stands until the #115 tally is judged, *then* sync. The tally was distilled
(`reviews/outputs/graph-mark-tally-digest-v1.html`) and **judged the same session** (*"i've gone with all
your recommendations"*), so the close condition fell inside the window and the sync ran: memento-package
copies of `_memento_search.py` re-synced · **`_graph_edges.py` ADDED to `VERBATIM_SET` + both copies + both
manifests**. ⚠ **The sync ALONE left a DEAD IMPORT — delta-audit GREEN, artefact BROKEN.** That is the
`no-gate-parses-the-artefact` class (#122) recurring in a different medium, and it was **caught by an
import-closure probe, not by the audit**. **Final: delta-audit 0 failures · validator selftest green ·
package import PROVEN.** ⛔ **This closes the RE-BASELINE only — the separate `v1` designer-skills pack
sync question (#114) is UNTOUCHED and remains Dave's.** [born #120 · closed #124 · guards: `_rulings.json` +
this line + the delta-audit run · until: term elapses at #126]

### ✅ CLOSED #124 — the #115 GRAPH PROGRAMME, in full (`s124-D1`)
**`_rulings.json` entry 62. DEMOTE IS RETIRED: the graph-mark stays MARK-ONLY, permanently** — a display
label, never a ranking lever. Ratified by Dave on Claude's recommendation with **measured** evidence: the
s124 tally found **76 of 79 marks were noise**, so the mark cannot discriminate mention-as-history from
mention-as-authority, and a demote built on it would mostly bury healthy records. ★ The arc is the point:
**instrumented (#115) → tallied (#115/#124) → judged by Dave (#124) → ruled (#124)** — the observation
window existed so this ruling would have provenance instead of recollection. Closes candidates-brief
**item 4**, the last open item of the programme. ⚠ **Probe pollution was DECLARED on the digest's own card
face:** ~half the raw marks were #124's own queries; every judged card had clean sightings.
⛔ **Do not re-open and do not extend the ruling beyond what it says.** [born #115 · closed #124 · guards:
`_rulings.json` `s124-D1` + `_REVIEW-SIGNOFF.md` + this line · until: term elapses at #126]

### ✅ GATED #124 — the 83,000-character COMMIT SUBJECT (born #78 as an unruled finding, gated #124)
Commit **`0eacf2d` is PUSHED and carries an ~83,000-character subject**; its msgfile body was JSONL with
**no blank line after the headline**, and git's `%s` folds everything up to the first blank. **Dave RULED:
gate and harden, KEEP THE HISTORY — no rewrite, no force-push.** ⇒ **`0eacf2d`'s subject STAYS in the log,
by ruling**; truncate git-log reads rather than trying to repair them. Enacted: `_git_commit.sh` **T3
inserts the blank separator** · a **post-commit 200-char subject cap fails loud** · `_test_git_commit.py`
carries `subject_fold_blank_line_inserted_124` + `MUTATION_blank_insert_removed_bites_124`, **22 arms
green**. ★ **The finding had been DOCUMENTED since #78 — in the harness's own comment, as *"not a script
defect"* — and never gated. A documented-but-ungated hazard is a scheduled defect.**
⛔ **RESIDUAL, UNPROVEN AND DECLARED NOT CHASED, and it is nobody's to close silently:** **how JSONL got
into that msgfile is unattributed.** It is not a gap in the gate — the gate now bites regardless of cause —
but the cause is unknown and is recorded as unknown [[a-crash-is-not-a-fail]].
[born #78 · gated #124 · guards: `_git_commit.sh` T3 + the 200-cap + 2 harness arms + this line ·
until: the attribution is measured or Dave rules the chase closed]

### ★★ OPEN, NO GATE — the ACCIDENTAL FALL-THROUGH class (born #123, standing)
**When a base value moves, every theme that MEANT the old value must declare it.** Inheritance is
indistinguishable from agreement until the base changes — at which point a theme that was merely
quiet gets silently re-ruled by someone else's decision. **Three instances, two sessions:** legacy
warn/info backgrounds (#122, ruled back at `s123-D1`) · legacy `rag/error-tint` undeclared (#123) ·
supercharge tints undeclared (#123). The last two were found **while enacting the remedy for the
first**, and both would have silently inherited mono's new values. All three are closed by explicit
declaration; **the CLASS is not.** ⚠ **No gate looks for an undeclared theme value whose base is
about to move** — this is `ds-039`'s cousin: not a gate that failed, a state nothing inspects.
Remedy UNRULED, unpriced. [born #123 · guards: this block · until: a gate ships or Dave rules it closed]

*(historical, kept as the record of what was parked — every item above is now closed)*
The five rulings `s122-D1`…`s122-D5` are CLOSED. These are their **mechanical consequences**,
none of them ruled, none of them decided by the session that produced them. Full arc:
`_DECISION-HISTORY/2026-08-07-mark-map-pass-and-the-half-dead-canon.md`.
1. **Legacy warning/information BACKGROUNDS fell through to the new mono values** — `#E0A61F` /
   `#78A7E8` (were `#F0B13A` / `#7DABCD`). Never declared in `apollo-legacy.overrides.json`, so
   never ruled. **UNRULED — his call whether legacy declares its own.**
2. **`_themes.json` `ownsHexes` is STALE** — *"`#B92F1E` is Mono's only red"* is false as of
   `s122-D3` (console/supercharge error). ⚠ The theme-provenance advisory's **37** are measured
   against that stale map, so the figure is not comparable across the boundary.
3. **Supercharge `badge/` + `tabs/badge/background` shifted to `#B92F1E`** via store alias edges —
   a mechanical consequence of `s122-D3`, **Dave's eye owed.**
4. **Legacy success white-on-teal mark leg = 4.56** — the weakest leg in the new world, over the
   4.5 bar. Recorded, not flagged as a defect.
5. **`*-tint` pairs remain UNRULED for mode-invariance** — the declared scope residual of `s122-D1`.
6. **NOT DRIVEN VISUALLY:** nobody has eyeballed rendered marks on the new fills.
   `reviews/outputs/mark-map-controller-v6.html` is in `knowledge/_REVIEW-SIGNOFF.md` awaiting him.
   ⚠ Both of #122's real findings came from Dave's eye, not from the 19+ green gates — this is not
   a formality (see `ds-039`).
[born #122 · guards: this block + `_REVIEW-SIGNOFF.md` + `ds-038`/`ds-039` · until: Dave rules each]

### ✅ FIXED #123 — `gen_canon_tokens.py` no longer destroys the hand-authored TOKENS atoms
The canon `TOKENS alpha` / `marks` / `mark-carriers` atoms sit inside AUTO markers with **no store
origin**, so a `gen_canon_tokens.py` run rewrote the AUTO span and took them out (`s121-D1` defect,
born #121, restated #122). **FIXED #123:** the generator now **harvests the hand-authored atoms
before the rewrite and re-injects them after**, and refuses with a named `AtomPreserveError` if one
would be dropped. Evidence: 3-bite selftest (`harvest · preserve · refusal`) re-run at this wrap —
`gen_canon_tokens selftest OK`; **driven twice on the real file, idempotent, atoms 3/3**.
⛔ **What we got wrong, same session:** the first version's own header comment matched its
marker-count regex (`TOKENS <name> START`) and would have raised a **spurious refusal on the NEXT
regen** — a false alarm shaped exactly like the defect it guards. Tightened to the `===== TOKENS`
form before it shipped. *An instrument whose own documentation is inside its own search space will
eventually measure itself.*
[born #121 · restated #122 · FIXED #123 · guards: the selftest + this line · until: term elapses at #125]

### ✅ RULED #108 — `type.css:180` dark-mode specificity collision, ink = `#1A1A1A`, NOT YET ENACTED
`knowledge/canon/type.css:180` ships `[data-theme="dark"]{background:#111;color:#fff}`. Its
attribute-selector specificity (0-1-0) beats any component's plain `body{background:var(--page)}`
(0-0-1), so **every dark-mode pane renders `rgb(17,17,17)` instead of the declared `#1A1A1A`**
even though `--page` resolves correctly. Observed live (real Dark button) on
`showroom/confirmation.html` and `showroom/chart-donut.html`; pre-existing, not introduced at #104.
**RULED #108 (Dave, by eye, `ds-033`): ink = `#1A1A1A`.** `type.css` NOT yet touched — the ruling
is recorded, the code change is not made. [born #104 · ruled #108 · guards: this line + GM DO-FIRST 19 + `ds-033` · until: enacted]

### ⚠ UNATTRIBUTED PATH, working-tree — #104
`_RESEARCH-graph-engineering-2026-08-05-v1.html` (39,447 bytes, repo root, untracked, mtime 20:09)
appeared during the #104 window and **no sub reported writing it**. **NOT staged, not committed.**
Every other untracked/modified path this window is accounted for (the chain-diet brief, the two
`reviews/PRI-HOVER-MEASUREMENT-*` files, `reviews/LEGEND-CENTRING-SPREAD-*`, `gen_showroom.py`'s
two one-line fixes, the 75 regenerated `showroom/*.html`, `notes/_REHEARSAL-LOG.jsonl`'s appends).
This one file is not — flagged, awaiting Dave, do not stage until claimed. [born #104 · guards:
this line · until: attributed or Dave rules it]

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
  Sonnet build: rebind Status-indicator to the R-D10 dark set **as amended by R-D11** (R-D10's
  mode-stability claim is dead — a build citing R-D10 alone re-enacts it · s124 tally SAVE), spec
  cell/bar as gated components (cells need more vertical padding).
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
