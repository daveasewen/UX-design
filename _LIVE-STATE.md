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

*Last refreshed: 2026-08-08 (Sat from `date` — **#129 wrap**: **FIVE RULINGS, ALL DAVE'S, ALL ENACTED IN-WINDOW.** **`s129-D1` THE BOOT FLOOR IS RE-BASED 75,899 -> 54,859** (`BOOT_FIRSTTURN_TK` 65,400 -> 54,859, `BOOT_FIRSTTURN_ERR` 1,400 -> 1,178; published floor 81,335 -> 70,794, room for job + wrap 118,665 -> 129,206) on **seven consecutive same-unit same-moment measurements** (#111 55,733 - #113 54,038 - #117 54,807 - #118 54,404 - #125 53,681 - #126 53,997 - #127 54,375, n=7 spread 2,052); **the ruled figure is Dave's n=3 54,859, NOT the n=7 mean 54,434**, and both are inscribed on purpose; **NOTHING ELSE MOVED** - stop line 150,929 and the 160,000/200,000/256,000 walls untouched. ⛔ **A SECOND DEFECT FOUND WHILE ENACTING, SAME CLASS:** `_capture_gate._parse_boot_samples()` matched **case-sensitively** while every post-mortem since #125 opens with the word *Boot* - **three sessions of the evidence the re-base rests on were invisible to the gate that grades the constant**, and it did not refuse, it silently counted fewer; fixed with `re.I`, parsed samples **28 -> 31**, and **both readings published** (old parser + new constant FAILS, fixed parser PASSES) so the fix cannot be mistaken for the finding. **`s129-D2`**: `_build_all.py`'s state-contrast caveat is now **GENERATED** (`state_contrast_caveat()` + selftest arm (d)) - closing #127's ⑧, the string that had gone false a third time and was left as evidence rather than re-stamped; `--selftest` **PASS, 102 steps**. **`s129-D3`**: the **15 un-hit-testable boxes are DECLARED as named holes**; `_validate_state_contrast.py` arms **19 -> 25, rc=0**; audit regenerated, holes **15 -> 14**, and **the delta was ATTRIBUTED to the browser build by a `git show HEAD` control x3**, not claimed; **the 4 REAL failures are byte-identical and still red**. **`s129-D4`**: **ASCII in the machine store, glyphs in the prose** - `_rulings.json` 0 non-ASCII, 15 glyphs mapped, round-trip byte-verified before writing, `_governs --selftest` **30 -> 30 with an empty diff**. **★★ `s129-D5` (Dave, mid-turn, ratifying the conductor's 5-whys):** *"verified is a property of a MOMENT, not the artefact; every inscribed conclusion is DEBT with three options: generate / named re-checker / expiry"* - root: **the system stores CONCLUSIONS where it should store GENERATORS**; enacted as the standing hunt **"Conclusions that could be queries"** in `.claude/agents/dreamer.md`, recorded in the ledger and in `_rulings.json` (**77 ids**). ✅ **THE BROWSER-DOWNLOAD QUESTION, OWED SINCE #126, IS ADJUDICATED FIRST-HAND: the download WORKS** (exit 0, 340M `chromium_headless_shell-1234` at `/var/tmp/pw-browsers-129`); **TLS-blocked did not reproduce**, and **both #125 subs were reading the environment, not the network** - **ENOSPC on the 98%-full shared `/sessions` volume presents as "Download failure, code=1"** and **`/tmp` is SHARED ACROSS SESSIONS** (a foreign session's stale `pwdl.log` was served as this run's evidence); `_RUNBOOK-render-verify.md` amended **BY ADDITION**, no dated stratum edited. ⚠ **NEW AND DAVE'S, REPORTED NOT REPAIRED: both #128 commits certify the WRONG SESSION** - `d74552e` and `ed4ce3a` carry #127's subject while `d74552e`'s own body asserts *"this message's first line deliberately begins with '#128'"*; either the msgfile's first line was wrong or the subject assert did not bite, **NOT diagnosed further**. ⛔ **WHAT WE GOT WRONG:** the first download probe read a **foreign session's `/tmp` log as its own evidence** (caught by the ENOSPC diff); the first write of `s129-D5` into `_rulings.json` used an **invented schema**, taking `_governs` failures **30 -> 67**, caught **by running the gate** and rewritten to the store's real shape; and the enactment sub first reported *"TLS-blocked on 3 CDNs"* because it ran `playwright install` **without opening the render runbook** - corrected in-window, wrong reading left visible. ⚙ ⛔ **NO #129 BOOT SAMPLE AND NO FILL SERIES EXIST** - the conductor could not read its own `message.usage`; **nothing is substituted**, the eighth datapoint is OWED, and the quota panel was **not re-read (UNKNOWN)**. Delegation: **2 OPUS subs**.)*  *Last refreshed: 2026-08-08 (Sat from `date` — **dream pass 5, lane step 7b** (Seam ①, ruled #128): the pass RAN — manual, **overdue from #127** where it was raised and rolled rather than started. 3 proposals → `notes/_dream/2026-08-08-proposals.md`, commit `6836c5a`; **P1 and P2 RULED BY DAVE THE SAME SESSION**, and P1 was extended live from *register the six* to **enact all seven 08-02 items now**. Enactment receipts: this session's commit. §🔀 below carries the lane row.)*    *Last refreshed: 2026-08-07 (Fri from `date` — **#127 wrap**: **THE MEMENTO SCHEMATIC v2 IS BUILT AND GENERATED**, at the third attempt — `knowledge/_gen_schematic.py` (~1,058 lines) → `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html`, **seven panels** (the six subsystems chain · store · search · marks · gates · package, plus a self panel), **39 rows, every figure read off disk at generation time**, inline SVG, no CDN, build-step counts taken from **`_gen_chain._steps_in` — the function itself, never a copy** (one slicer, `s125-D1`); **each panel computes its own *what re-checks this*** from `STEPS` × `ROUTE_ROWS` and renders a red **NOTHING RE-CHECKS THIS** where the answer is none. **v1 KEPT and TOMBSTONED (+29/−0, purely additive, stale figures untouched)** — Dave's #125 disposition enacted. **WIRED 98 → 102 STEPS on Dave's call**: 3 schematic rows + **1 contrast-selftest row** (⚠ **four wired, not the three quoted to him** — the fourth added under the file's own precedent *"a selftest not in STEPS is a gate that does not run"*, declared in chat); ★★ **`s125-D1` demonstrated itself a THIRD time, live** — the published build figure moved **98 → 102** and the never-verified shortfall **23 → 27** with **nothing typed**. **`_governs.py` RED REPAIRED STRUCTURALLY — and the standing record of that defect was FALSE IN BOTH HALVES**: `s121-D1` points at **bare `canon.css`** (the record silently added the `knowledge/canon/` prefix, hiding a path **never resolvable from repo root — the entry was BORN RED at #121**) and **line 5548 DOES exist** (`--alpha-84: 0.84;`), so **a repair driven off that sentence would have gone GREEN pointing at an unrelated token**; the real construct (RAG roundel policy) had drifted **5548 → 6451**. Fix = anchor pointer `<path>#<literal>` (**+135/−0**, line number **derived at read time and stored nowhere**), `_rulings.json` ±2 lines round-trip byte-verified, **7 mutation bites all RED as designed**, `_governs --selftest` **32 → 30**. ⚠ **STILL RED, honestly: `_capture_gate.py --selftest` rc=1 — the gate reports only `fs[0]`, so *one rotten pointer* was never one: 30 remain** (class B 18 = `s122-D1…D5`/`s123-D1…D4`/`s124-D1` missing `evidence`/`status`, **filling them means asserting what Dave ruled**; class C 12 = `s125-D1/D2/D3` prose-in-`evidence`; **+11 legacy `<path>:<int>` green and unverifiable**) — **all Dave's**. **BOTH `_validate_state_contrast.py` DEFECTS FIXED with the boundary proven**: `effBg` **modelled the paint stack as the ancestor chain when painting is a z-ordered geometry of boxes** (now composites the browser's own hit stack), `out[3]` was **a derived summary written into a positional slot the loop above owns** (now an insert; the eaten `Accordion` heading is back, the zero-snippet crash is a named refusal); **TEXT failures 46 → 14 — exactly the 32 named false failures removed, ZERO added — and all 4 REAL failures survive with identical ratios, still red, nothing waived**; **confirmed by a second instrument sharing no code** (screenshot pixels **21.0:1** where the gate said 1:1); audit regenerated **14 / 75 snippets** with stated and real counts **asserted equal on every write** (coverage 38 → 75 closes *stale by 37*); **8 mutation bites, byte-exact restore after each**, incl. **M5**, which reddens a "fix" that stops failing by ceasing to report. ⚠ **The sub was wrong TWICE and measurement caught both** (element `opacity` invented 12 failures; refusing un-hit-testable boxes turned 60 records into holes) — visible only because it captured the whole corpus instead of the headline; **the declare-vs-refuse call on the remaining 15 boxes is DAVE'S**. ⛔ **A claim gone false a THIRD time in a THIRD place, deliberately NOT re-stamped**: `_build_all.py`'s comment was corrected, but its `ROUTE_ROWS` **remedy string still carries the `s125-D3` parse caveat fixed at #125** (0 parse refusals measured across all 75 snippets) — **left as EVIDENCE, remedy raised to Dave**, because *stale twice ⇒ GENERATE, don't re-stamp*. ⛔ **THE DREAM PASS was raised by Dave mid-session and NOT RUN** — it did not fit the window and was **rolled to #128 as item ①**, deliberately, rather than started and abandoned. ⛔ **WHAT WE GOT WRONG: the opener's budget arithmetic** — it treated **150,929 as the ceiling and subtracted the wrap AGAIN**, reporting ~30K of job room against a real **79,012**; Dave: *"150,929 is the line at which it is recommended you start the wrap, not the limit"*. ★ **A reserve on a reserve — the exact defect named in `_gauge_tokens.py`'s own comments eleven lines above the quoted constant** — and **it materially affected a decision** (the delegation pick), so the pick was declared **re-openable**. Inscribed by ADDITION in `_RUNBOOK-context-gauge.md`; **no constant moved.** ✅ **GREEN:** `_build_all.py --selftest` **PASS, 102 steps** · `_validate_wiring.py` **30/30, 0 exempt, 0 failures** · `_gen_schematic.py --check` FRESH · `_gen_schematic --selftest` · `_gen_chain --selftest` · `_validate_state_contrast --selftest` rc=0, 19 arms. **UNPROVEN, priced:** a single-process full contrast run (~400s vs the ~178s call kill) — CI delivers it. ⚙ **boot 54,375 real** — the **SIXTH datapoint below the published 75,899 floor**; ⛔ **recorded, NOT re-based — the re-base is Dave's and remains untaken**. FILL 71,917 → 90,537 → 111,360 → **135,896** vs wrap-open **150,929**, **wrap DELEGATED at 135,896 — roll, not ride**. ✅ **Quota panel GIVEN: session 14% · all-models 13% · Fable 17%**, with the WINDOW named as the binding constraint.)*    *Last refreshed: 2026-08-07 (Fri from `date` — **#126 wrap**: **`s125-D1` RULED #125, ENACTED #126** — the chain banner's build-step count is now a **GENERATED figure**. `knowledge/_gen_chain.py` gained `BUILD_VERDICT_MARK`, `VERDICT_SHA = "18c7789"`, `BuildStepCountError`, `_steps_in()` (AST), `build_steps_now()`, `build_steps_at()` and `build_verdict_line()`; `knowledge/_capture_gate.py`'s `chain_parts()` gained a **20-line purely-additive block (0 deleted lines)** that splices the rendered verdict at the build-verdict marker, and `GOOD-MORNING.md`'s 371-char typed segment became that 17-char marker after its narrative was homed. **`_CHAIN.md` now reads *"75 of 98 steps green (#62, `18c7789`) — 23 steps have NEVER been in a green verdict"*, both counts read from an AST at each end and the shortfall COMPUTED.** ⛔ **THE SCHEMATIC WAS NOT BUILT — the window ran out, exactly as at #125**; the title is a LABEL, not a deliverable claim. **THREE decisions inside the enactment, all declared:** (a) **TWO numbers, not one** — publishing only the live count would have manufactured *"ALL 98 STEPS ASKED AND GREEN (#62)"*, a sentence nobody ever measured, produced by the very fix meant to stop manufactured claims; (b) **the SPLICE lives in `_capture_gate.chain_parts`, not `_gen_chain`**, because `chain_parts` is THE ONE SLICER — `read_chain_tk` measures exactly what it returns and `_gen_chain` writes exactly what it returns, so a downstream injection would be WRITTEN BUT NOT MEASURED (#41's second-consumer drift); the AST READER is in `_gen_chain.py` as ruled and only the splice moved — **an implementation reconciliation, NOT a re-ruling, flagged for Dave**; (c) **`VERDICT_SHA` is typed on purpose** — it names a fixed historical event and cannot go stale the way a COUNT does. ★★ **THE PREMISE DEMONSTRATED ITSELF INSIDE ONE DAY:** #125 measured `len(STEPS)` = 97, #126 measured **98** — `s125-D2`'s wiring added a step between the probe and the enactment, so the figure went stale again in under 24 hours. ★★ **NEW FINDING: 23 build steps have NEVER been inside any green verdict.** **Evidence:** 98 steps / 98 distinct labels on disk, 75 / 75 at `18c7789`, 1:1 at both ends · **mutation battery 12 bites 0 fail** (a new step moves 98→99 and the gap 23→24 · renaming `STEPS` REFUSES BY NAME and publishes NO count · a non-literal `STEPS` refuses · an unreachable `VERDICT_SHA` declares the COVERAGE unmeasured while still publishing the live count · a duplicated label is surfaced, not counted as growth), `_build_all.py` restored **byte-exact (sha256)** after every mutation · **5 permanent bites WIRED into `_gen_chain.selftest()`**, the load-bearing one re-deriving `len(STEPS)` from disk at test time and asserting the chain publishes THAT. **GREEN rc=0:** `_gen_chain --selftest` · `_gen_chain --check` FRESH · `_validate_wiring.py` 30/30/0 exempt/0 failures · `_build_all.py --selftest` PASS 98 steps · `check_budgets()` **0 blocking failures**. ⚠ **The `_capture_gate.py --selftest` red is `_governs.py`'s `s121-D1` pointer rot (`canon.css:5548` absent) — PRE-EXISTING and NOT this session's**, attribution checked against `git status`; recorded as a standing open item, not fixed. ⚙ Gauge: **boot 53,997 real** — the **FIFTH datapoint below the published 75,899 floor**, consistent with the post-break n=3 mean 54,859; ⛔ **recorded, NOT re-based — the re-base is Dave's and remains untaken**. FILL 74,120 → **135,735** vs stop line **150,929**, **wrap DELEGATED at 135,735 — roll, not ride**, and the schematic was not started for exactly that reason; throughput 175,569 real. ⚠ **Dave's quota panel was ASKED FOR at the opener and NOT GIVEN — recorded UNKNOWN, never estimated.**)*  
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

## ⏱ LATEST DELTA — 2026-08-08 (Sat **#129**, FABLE conductor, Dave live, ONE window + 2 OPUS subs — ✅ **FIVE RULINGS, ALL DAVE'S, ALL ENACTED IN-WINDOW** · ★★★ **THE BOOT FLOOR IS RE-BASED 75,899 → 54,859, AND THE PARSER THAT GRADES IT COULD NOT SEE THREE OF THE SEVEN MEASUREMENTS** · ★★ **`s129-D5`: VERIFIED IS A PROPERTY OF A MOMENT, NOT OF THE ARTEFACT** · ⚠ **BOTH #128 COMMITS CERTIFY THE WRONG SESSION — FOUND, NOT REPAIRED**)

**Landed (evidence per claim):** **⚠ READ THE SHAPE FIRST — the session opened on work that was already done.** Dream pass ① (owed from #127, carried into #128) was found COMPLETE at boot — `6836c5a`, 07:57 — and a #128 session had then **enacted all six 2026-08-02 dream-pass rulings** (`d74552e` 08:20, `ed4ce3a` 09:08). **P1 was overtaken by events inside two hours**, which is itself the `s129-D5` finding in miniature: the proposal was a CONCLUSION about repo state, written the night before, with nothing re-checking it. The window went to five rulings instead.

- **① `s129-D1` — THE BOOT FLOOR RE-BASED, 75,899 → 54,859.** `_gauge_tokens.BOOT_FIRSTTURN_TK` **65,400 → 54,859** and `BOOT_FIRSTTURN_ERR` **1,400 → 1,178**; the published floor (first turn + measured `_CHAIN.md`) moves **81,335 → 70,794**, room for job + wrap **118,665 → 129,206**. **Evidence, n=7, same unit and same moment each time:** #111 55,733 · #113 54,038 · #117 54,807 · #118 54,404 · #125 53,681 · #126 53,997 · #127 54,375 (spread 2,052). **#111-D2** (*don't fit a constant across a structural break*) is **SPENT, not overruled** — the break sits between #109 and #111 and the post-break series has been a plateau since #117. ⚠ **The ruled figure is NOT the n=7 mean (54,434); it is Dave's n=3 figure 54,859**, and both are inscribed in the source on purpose so that a future session "correcting" the constant to the mean is visibly doing the thing this project keeps un-doing. ⛔ **NOTHING ELSE MOVED**: stop line 150,929, `BUDGET_AMBER` 160,000, `BUDGET_WORKING` 200,000, `BUDGET_HARD` 256,000 — a cheaper boot moves the ROOM, never the LINE.
- **⛔ ①b A SECOND DEFECT, FOUND WHILE ENACTING, SAME CLASS AS THE RULING.** `_capture_gate._parse_boot_samples()` matched **case-sensitively**, and every post-mortem since #125 opens its sentence with the word — *"**Boot 53,681 real**"*. Those lines **did not parse, did not REFUSE, and were not counted**: three sessions of the evidence the re-base rests on were invisible to the gate that grades the constant. Fixed with `re.I` (one flag, both the match and the refusal probe); parsed samples **28 → 31**. ⚠ **The parser fix and the re-base landed in the same pass and the fix moves the gate's own window, so BOTH readings are published:** old parser + new constant **FAILS** (window mean 56,078, delta +1,219 — the window still straddles the break), fixed parser **PASSES** (mean 54,325, delta −533). The constant was **not fitted to the window**; 54,859 clears the bar by 645.
- **② `s129-D2` — THE STATE-CONTRAST CAVEAT IS GENERATED, NOT RE-STAMPED.** `_build_all.py` gained `state_contrast_caveat()` and selftest arm **(d)**. This closes #127's ⑧ — the remedy string that had gone false a **third** time and was deliberately left as evidence rather than hand-corrected a fourth. **`--selftest` PASS, 102 steps**, replayed by the conductor.
- **③ `s129-D3` — THE 15 UN-HIT-TESTABLE BOXES ARE DECLARED AS NAMED HOLES.** #127's declare-vs-refuse fork, taken by Dave. `_validate_state_contrast.py` selftest arms **19 → 25, rc=0** (replayed by the conductor with the browser at `/var/tmp/pw-browsers-129` and `LD_LIBRARY_PATH=$HOME/.local/chromelibs/root/usr/lib/aarch64-linux-gnu`, **re-exported per call** — nothing survives a tool-call boundary). Audit regenerated: holes **15 → 14**. ★ **The delta was ATTRIBUTED rather than claimed:** a `git show HEAD` control run ×3 puts the one-hole change on the **browser build**, not on `s129-D3`'s emit condition, whose logic is unchanged apart from the added `reason`. ⛔ **The 4 REAL failures are byte-identical and still red.**
- **④ `s129-D4` — ASCII IN THE MACHINE STORE, GLYPHS IN THE PROSE.** `_rulings.json` now holds **0 non-ASCII**; 15 glyphs mapped; the file was **round-tripped and byte-verified before writing** so the diff carries the semantic change and nothing else; `_governs.py --selftest` **30 → 30 with an empty diff** — the store changed and the verdict did not, which is the assertion worth making.
- **★★ ⑤ `s129-D5` — "VERIFIED" IS A PROPERTY OF A MOMENT, NOT OF THE ARTEFACT.** Dave, mid-turn, ratifying the conductor's 5-whys in his own words: *"verified is a property of a MOMENT, not the artefact; every inscribed conclusion is DEBT with three options: generate / named re-checker / expiry."* ★ **The 5-whys root: the system stores CONCLUSIONS where it should store GENERATORS.** Seven media are now on the record — prose · a comment · a return value · a pointer · the record of a defect itself · **a commit subject** (⑦ below) · **the sandbox environment** (⑥ below). Enacted as a **standing hunt, "Conclusions that could be queries"**, in `.claude/agents/dreamer.md`; recorded at `notes/_MEMENTO-DECISIONS.md` § `s129-D5` and in `knowledge/_rulings.json` (**77 ids**).
- **⑥ THE BROWSER-DOWNLOAD CONTRADICTION IS ADJUDICATED — OWED SINCE #126, RE-OWED AT #127 AND #128.** Settled **first-hand by the conductor, not by picking a side of the #125 record**: the download **WORKS** — exit 0, **340M `chromium_headless_shell-1234`** at `/var/tmp/pw-browsers-129`; **TLS-blocked did not reproduce.** ★ **Both #125 subs were reading the environment, not the network.** Two real culprits, both environmental and both now named: **(a) ENOSPC on the 98%-full SHARED `/sessions` volume presents as *"Download failure, code=1"*** — set `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/…` and run `df -h $HOME` before blaming the network; **(b) `/tmp` is SHARED ACROSS SESSIONS**, and a foreign session's stale `pwdl.log` was served as this run's evidence — use unique log paths under `$HOME`. `knowledge/_RUNBOOK-render-verify.md` amended **BY ADDITION**, dated 2026-08-08 stratum at the head; **no dated stratum was edited or deleted**, because the file already held both readings stratified by date and quoting one stratum is not reading the file.
- **⚠ ⑦ NEW, DAVE'S, REPORTED AND NOT REPAIRED — BOTH #128 COMMITS CERTIFY THE WRONG SESSION.** `d74552e` and `ed4ce3a` both carry the subject *"after #127 2026-08-07 — ✅ THE SCHEMATIC v2 LANDED…"* — #127's banner text — while `d74552e`'s **own message body asserts** *"this message's first line deliberately begins with '#128'"*. **That claim is false as committed.** Two candidate causes, neither eliminated: the msgfile's first line was genuinely wrong (in which case the #124 subject assert did exactly its job and faithfully certified a wrong line), or **the assert did not bite**. ⛔ **NOT diagnosed further and NOT repaired — Dave's, and it is #130's opening item.** ★ Note the class: the body's claim about its own first line was a **conclusion inscribed at write time with nothing re-checking it at commit time** — `s129-D5`, in the git log.
- **⛔ WHAT THE CONDUCTOR GOT WRONG — three, all caught in-window, all left visible.** **(a)** the first download probe **read a foreign session's `/tmp` log as its own evidence**, and it was caught only because the ENOSPC diff did not fit; **(b)** the first write of `s129-D5` into `_rulings.json` used an **invented schema** — no `ruled`/`by`/`says`/`governs`, and a string `evidence` that the validator iterated as characters — taking `_governs` failures **30 → 67**; caught **by running the gate rather than by reading the diff**, rewritten to the store's real shape, back to **30**; **(c)** the enactment sub's first report said *"TLS-blocked on 3 CDNs"* because it ran `playwright install` **without opening the render runbook** — corrected in-window, and the wrong reading is **left visible in its records**, not tidied away.
- **✅ GREEN (conductor replay, not sub testimony):** `_build_all.py --selftest` **PASS, 102 steps** · `_validate_state_contrast.py --selftest` **rc=0, 25 arms** · `_governs.py --selftest` **30** · `_rulings.json` **0 non-ASCII, 77 ids** · boot constant **54,859 live**. **RED, honestly:** `_capture_gate.py --selftest` **rc=1** (30 pointer entries — **Dave's**) · state-contrast gate **rc=1** on the 4 REAL failures (**Dave's**).
- **⚙ Gauge:** ⛔ **NO #129 BOOT SAMPLE EXISTS.** The conductor could not read its own first-turn `message.usage` this session, and **nothing is substituted** — the eighth datapoint is OWED and is recorded as such in `notes/_GAUGE-LOG.md` § #129. The **WINDOW** budget was the binding constraint and was named as such; ⚠ **the quota panel was not re-read — UNKNOWN, never estimated.** Delegation: **2 OPUS subs** (enactment ~192K, plus this wrap).
- **Dave's opens UNCHANGED:** P1 confirm-to-open · G4 ratify · recorder-constants refresh · the 3 chart-meta provenance-enum edits. **CLOSED and removed from the opens:** the boot-floor re-base (`s129-D1`) · declare-vs-refuse on the 15 boxes (`s129-D3`).
- **→ #130** *(ages in sessions, per the #128 P2 ruling)*: ⬛ ① **the #128 wrong-subject autopsy [0]** · ⬛ ② **the 30 pointer entries [2]** · ⬛ ③ **the 4 REAL contrast failures [4]** · ⬛ ④ **dream-pass P2 [1] — half answered** · ⬛ ⑤ **dream-pass P3 [1] — largely closed** · ⬛ ⑥ **carried (FIFTEENTH roll)**: fall-through class [6] · `s116-D4`/`D5` [13] · `s114-D2` [15] · stale-mount seam [≥15] · P4 chain trim [19] · `89-D2` [40] · `ds-032` [≥20] · `ds-025` [20] · boot-rent plan [19] · G4 ratify [≥16] · P1 confirm-to-open [19] · 3 chart-meta provenance-enum edits [9].

## ⏱ PRIOR DELTA — 2026-08-07 (Fri **#127**, OPUS conductor, Dave live, ONE window + 3 OPUS subs — ✅ **THE MEMENTO SCHEMATIC v2 IS BUILT AND GENERATED, AFTER ROLLING TWICE** · ✅ **THE BUILD WENT 98 → 102 STEPS ON DAVE'S CALL** · ✅ **BOTH `_validate_state_contrast.py` DEFECTS FIXED — TEXT FAILURES 46 → 14 WITH THE BOUNDARY PROVEN AND NOTHING WAIVED** · ★★ **`_governs.py` REPAIRED STRUCTURALLY — AND THE STANDING RECORD OF THAT DEFECT WAS FALSE IN BOTH HALVES** · ★★ **`s125-D1` DEMONSTRATED ITSELF A THIRD TIME, LIVE, WITH NOTHING TYPED**)

**Landed (evidence per claim):** the session title `Apollo - #127: the schematic v2` names a lane that **actually landed this time**, at the third attempt. Three OPUS subs ran under an OPUS conductor in ONE window; the wrap was delegated at FILL 135,896 against a wrap-open line of 150,929 — **rolled, not ridden.**

- **① ✅ THE SCHEMATIC v2 — GENERATED, NOT DRAWN.** New `knowledge/_gen_schematic.py` (~1,058 lines) produces `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html`: **seven panels** — the six subsystems (chain · store · search · marks · gates · package) plus a **self panel** — **39 rows, every figure read off disk at generation time**, inline SVG, no CDN. Build-step counts come from **`_gen_chain._steps_in`, the function itself and never a copy** (one slicer, `s125-D1`). ★ **Each panel computes its own *"what re-checks this"*** from `STEPS` × `ROUTE_ROWS` and renders a red **NOTHING RE-CHECKS THIS** where the answer is none. **v1 (`reviews/MEMENTO-SCHEMATIC-2026-07-26-v1.html`) KEPT and TOMBSTONED — +29/−0, purely additive, its stale figures deliberately untouched**, which is Dave's #125 disposition enacted verbatim. *(evidence: `knowledge/_gen_schematic.py` · `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html` · 2026-08-07)*
- **② ✅ WIRED — 98 → 102 STEPS, DAVE'S CALL AT THE OPENER.** Three schematic rows (build · `--check` · `--selftest`) **plus one contrast-selftest row** in `_build_all.py`'s `STEPS` and `ROUTE_ROWS`. **The schematic's own red self-warning flipped to 0 occurrences automatically** once the rows existed. ⚠ **FOUR rows were wired, not the THREE quoted to Dave**: the fourth is the contrast selftest, added under the file's own stated precedent — *"a selftest not in STEPS is a gate that does not run"* — and **declared to him in chat, not buried in the diff.** *(evidence: `knowledge/_build_all.py` · `_build_all.py --selftest` PASS, 102 steps · 2026-08-07)*
- **★★ ③ `s125-D1` DEMONSTRATED ITSELF A THIRD TIME, LIVE.** Wiring those rows moved the chain's published build figure **98 → 102** and the never-verified shortfall **23 → 27**, **with nothing typed by anyone.** Yesterday's ruling paid for itself again inside 24 hours — the third demonstration in three consecutive sessions.
- **④ ✅ `_governs.py` RED — REPAIRED STRUCTURALLY, AND THE STANDING RECORD WAS WRONG.** `_LIVE-STATE.md:457` stated that `s121-D1` points at `knowledge/canon/canon.css:5548` and that *"that line does not exist"*. **BOTH HALVES ARE FALSE.** The ruling points at **bare `canon.css`** — the record silently added the prefix, and that is what hid the real defect: a path **never resolvable from repo root**, so the entry was **BORN RED at #121**. And **line 5548 does exist**; today it reads `--alpha-84: 0.84;`. ⚠ **A repair driven off that sentence would have gone GREEN pointing at an unrelated token.** The construct the ruling actually cites — the RAG roundel policy — had drifted **5548 → 6451**, 903 lines in 5 sessions. **Fix:** a new anchor-pointer form `<path>#<literal>` in `knowledge/_governs.py` (**+135/−0, purely additive**) — `is_anchor_pointer()`, `resolve_anchor()`, wired into `render()` and `selftest()` — with the **line number derived at read time and stored nowhere** (the `_steps_in` shape). `_rulings.json` **±2 lines, round-trip byte-verified, no serializer reformat**. **7 mutation bites, all RED as designed, every restore sha256 byte-exact.** `_governs --selftest` **32 → 30** failures. *(evidence: `knowledge/_governs.py` · `knowledge/_rulings.json` · 2026-08-07)*
- **⚠ ⑤ STILL RED, HONESTLY — AND "ONE ROTTEN POINTER" WAS NEVER ONE.** `_capture_gate.py --selftest` is **rc=1**. The gate reports only `fs[0]`; with `s121-D1` repaired, **30 entries remain** — **class B (18)**: `s122-D1…D5`, `s123-D1…D4`, `s124-D1` missing `evidence`/`status`, and **filling those means asserting what Dave ruled**; **class C (12)**: `s125-D1/D2/D3`, where `evidence` was used as a prose field. **A further 11 entries still use `<path>:<int>` — green, unverifiable, and currently invisible to the gate.** ⛔ **ALL NOT FIXED. All Dave's.**
- **⑥ ✅ THE TWO `_validate_state_contrast.py` DEFECTS — FIXED, WITH THE BOUNDARY PROVEN.** **The `effBg` class was the MODEL, not the walk:** it modelled the paint stack as the ancestor chain **when painting is a z-ordered geometry of boxes**, so it was blind by construction to an absolutely-positioned sibling; it now composites the browser's own hit stack (`elementsFromPoint`, paint order, src-over). **The `out[3]` class was a derived summary written into a positional slot the loop above owns** — now an insert; the eaten `Accordion` heading is back and the zero-snippet `IndexError` is a named refusal. Added `verify_report()` (`StateContrastReportError`), `--selftest` (**19 arms**), `--help`, and named refusals for unknown args and for a filter matching nothing. ★ **THE BOUNDARY: TEXT failures 46 → 14 — exactly the 32 named false failures removed (Segmented-control ×12 · Charts ×16 · View-options ×4), ZERO added.** **All 4 REAL failures survive with identical ratios, still red**: Banner `.abtn:active` **4.09:1** ×4 · Selection-controls **3.95:1** ×6 + **3.66:1** ×2 · Tabs dark **1.00:1** ×2 — **nothing waived, nothing re-thresholded.** **Independently confirmed by a second instrument sharing no code**: screenshot pixels read **21.0:1** where the gate had said 1:1. `_STATE-CONTRAST-AUDIT.md` regenerated — **14 failures / 75 snippets, stated count and real count asserted equal by the script on every write**; coverage **38 → 75** closes the *"stale by 37"*. **8 mutation bites, one clause each, byte-exact restore after every one**, including **M5, the boundary guard: a "fix" that stops failing by ceasing to report goes RED.** *(evidence: `knowledge/_validate_state_contrast.py` · `knowledge/_STATE-CONTRAST-AUDIT.md` · 2026-08-07)*
- **⚠ ⑦ THE SUB'S FIRST IMPLEMENTATION WAS WRONG TWICE, AND MEASUREMENT CAUGHT BOTH.** Ignoring element `opacity` **invented 12 failures**; refusing un-hit-testable boxes turned **60 measured records into holes**. ★ **Both were visible only because it captured the whole corpus instead of trusting the headline.** ⬛ **The declare-vs-refuse posture on the 15 remaining un-hit-testable boxes is DAVE'S** (§ OPEN).
- **⚠ ⑧ A CLAIM GONE FALSE FOR THE THIRD TIME, IN A THIRD PLACE — AND DELIBERATELY NOT RE-STAMPED.** `_build_all.py`'s state-contrast comment, already hand-corrected once at #125 for going false inside its own session, **went false again** (it still described the 32 as *"deliberately unfixed"*). **And its gate remedy string at `ROUTE_ROWS` still carries the `s125-D3` parse caveat, which was FIXED at #125** — #127 measured **0 parse refusals across all 75 snippets**, before and after. ⛔ **The conductor corrected the comment but explicitly REFUSED to hand-correct the remedy a third time, leaving it as EVIDENCE with the remedy raised to Dave**: the standing rule is *stale twice ⇒ GENERATE, don't re-stamp*, and a third hand-correction is the move `s125-D1` exists to forbid.
- **⛔ ⑨ THE DREAM PASS WAS MISSED AND IS ROLLING.** Dave raised it mid-session. It did not fit the window — **a sub's report alone costs more FILL than remained before the wrap-open line** — so it was **rolled to #128 as the FIRST item, deliberately, rather than started and abandoned.** Recorded as **OVERDUE**.
- **⛔ ⑩ WHAT WE GOT WRONG — THE BUDGET ARITHMETIC AT THE OPENER.** It treated **150,929 as the ceiling and then subtracted the wrap AGAIN**, reporting ~30K of job room when the real figure was **79,012**. Dave corrected it: *"150,929 is the line at which it is recommended you start the wrap, not the limit"* — 200,000 is working, 256,000 is the absolute hard stop, and 150,929 is derived as `wall − wrap`. ★ **A RESERVE ON A RESERVE — the exact defect named in `_gauge_tokens.py`'s own comments eleven lines above the constant that was quoted.** ⚠ **It materially affected a decision**: Dave chose to delegate the schematic against an understated budget. **The delegation succeeded, but the stated reason was wrong and the pick was declared re-openable, not settled.** ✅ Inscribed **by ADDITION** at `knowledge/_RUNBOOK-context-gauge.md` § The Red trigger; **no constant was moved.**
- **✅ GREEN, verified by the conductor directly:** `_build_all.py --selftest` **PASS, 102 steps** · `_validate_wiring.py` **30/30, 0 exempt, 0 failures** · `_gen_schematic.py --check` **FRESH** · `_gen_schematic.py --selftest` all bites · `_gen_chain.py --selftest` all bites · `_validate_state_contrast.py --selftest` **rc=0, 19 arms**. **RED, honestly:** `_capture_gate.py --selftest` rc=1 (the 30 pointer entries) · the state-contrast gate rc=1 on Dave's 4 real failures. **UNPROVEN, priced:** a single-process full contrast run (~400s against the host's ~178s call kill) — CI delivers it.
- **⚙ gauge:** **boot 54,375 real** (`message.usage`, first turn) — ⚠ **the SIXTH datapoint below the published 75,899 floor**, consistent with the post-break n=3 mean of 54,859. ⛔ **RECORDED, NOT re-based — the re-base is DAVE'S and remains UNTAKEN.** FILL check-ins **71,917 → 90,537 → 111,360 → 135,896** against wrap-open **150,929**; **the wrap was DELEGATED at 135,896 — roll, not ride.** ✅ **Quota panel GIVEN**: session **14%** · weekly all-models **13%** · weekly Fable **17%** — and the **window budget was named as the binding constraint, not quota.** **3 OPUS subs; delegation cost ~18.6K FILL for a full build.**
- **⛔ DO-NOT-RULE — respected in full, carried verbatim:** `G1`–`G17` · floor **75,899** and the re-base · recorder constants · **v1 pack sync (#114)** · mono grey ramp · SC dark · `G8` · type-ratchet debt **1,101 (may only shrink)** · the **19 `LEGACY_IDS`** items · **32.9-vs-32 RED** · `ds-025` · `ds-032` · the boot-rent plan · the fall-through-class remedy · the UNPROVEN msgfile attribution · **the 4 REAL contrast failures** · **the render-runbook contradiction** · **`G4`** (its §C warn was printed and proceeded past — warn ≠ block, and **the cap was NOT moved**) · **new this session: the 15 un-hit-testable boxes · the class B/C pointer repairs · generate-vs-re-stamp · the ⛔/★-vs-ASCII glyph question.** **This wrap ruled nothing, changed no value, and edited no gate, threshold or fence.**
- **Dave's opens UNCHANGED:** P1 confirm-to-open · G4 ratify · recorder-constants refresh · the 3 chart-meta provenance-enum edits.
- **→ #128:** ⬛ ① **THE DREAM PASS — OVERDUE** · ⬛ ② **`_capture_gate` 30 pointer entries** · ⬛ ③ **declare-vs-refuse, 15 boxes — DAVE'S** · ⬛ ④ **the 4 REAL contrast failures — DAVE'S** · ⬛ ⑤ **generate-vs-re-stamp — DAVE'S** · ⬛ ⑥ **⛔/★-vs-ASCII — DAVE'S** · ⬛ ⑦ **the boot-floor re-base, SIXTH below-floor reading — DAVE'S** · ⬛ ⑧ **`_LIVE-STATE.md:457` misdiagnosis — CORRECTED BY ADDITION at this wrap, verify it** · ⬛ ⑨ **carried:** fall-through class · `s116-D4`/`D5` · `s114-D2` · stale-mount seam · P4 chain trim · 89-D2 · `ds-032` · `ds-025` · boot-rent plan · G4 ratify · P1 confirm-to-open · the 3 chart-meta provenance-enum edits (**FOURTEENTH roll**).


## ⏱ PRIOR DELTA — 2026-08-07 (Fri **#126**, OPUS conductor, Dave live, ONE window, no subs until the wrap — ✅ **`s125-D1` RULED #125, ENACTED #126: THE CHAIN BANNER'S BUILD-STEP COUNT IS NOW A GENERATED FIGURE** · ⛔ **THE SCHEMATIC WAS *NOT* BUILT — THE WINDOW RAN OUT, EXACTLY AS AT #125** · ★★ **THE RULING'S PREMISE DEMONSTRATED ITSELF INSIDE ONE DAY: THE FIGURE WENT STALE AGAIN IN UNDER 24 HOURS** · ★★ **A NEW FINDING, NOT A RESTATEMENT: 23 BUILD STEPS HAVE NEVER BEEN INSIDE ANY GREEN VERDICT**)

**Landed (evidence per claim):** **⚠ READ THE SHAPE FIRST — the session title is `Apollo - #126: enact s125-D1, then draw the schematic` and ONE of those two halves landed.** Dave confirmed that lane at the opener by explicit option-select (*"Title lane as written"*). **THE SCHEMATIC WAS NOT BUILT**; the window ran out and the wrap was delegated at FILL 135,735 rather than ridden. **The title is a LABEL, not a deliverable claim** [[feedback-dont-launder-a-premise-into-a-ruling]].

- **① ✅ `s125-D1` — RULED #125, ENACTED #126. The build-step count is GENERATED, never typed.** `knowledge/_gen_chain.py` gained `BUILD_VERDICT_MARK`, `VERDICT_SHA = "18c7789"`, `BuildStepCountError`, `_steps_in()` (AST), `build_steps_now()`, `build_steps_at()` and `build_verdict_line()`. `knowledge/_capture_gate.py`'s `chain_parts()` gained a **20-line PURELY ADDITIVE block (0 deleted lines)** that splices the rendered verdict where the build-verdict marker appears. `GOOD-MORNING.md` line 10's **371-char typed segment was replaced by the 17-char marker** — its narrative was homed at § OPEN and `notes/_MEMENTO-DECISIONS.md` § ★ #125 **before** the cut, and the full reasoning now lives as comments in `_gen_chain.py` [[home-by-addition-then-cut]]. **`_CHAIN.md` now reads: *"⛔ BUILD VERDICT: 75 of 98 steps green (#62, `18c7789`) — 23 steps have NEVER been in a green verdict. Both counts GENERATED from `_build_all.py`'s AST at each end; the shortfall is computed (`s125-D1`)."***
- **② THREE DECISIONS TAKEN INSIDE THE ENACTMENT, ALL DECLARED.** **(a) TWO numbers, not one.** Substituting only the live count would have published *"ALL 98 STEPS ASKED AND GREEN (#62)"* — **a sentence nobody ever measured, manufactured by the very fix meant to stop manufactured claims.** So BOTH ends are read from an AST (working tree **98**; `git show 18c7789:knowledge/_build_all.py` **75**) and the **23-step shortfall is COMPUTED**. **(b) The SPLICE lives in `_capture_gate.chain_parts`, not `_gen_chain`, although the ruling names `_gen_chain`** — `chain_parts` is **THE ONE SLICER**: `read_chain_tk` measures exactly what it returns and `_gen_chain` writes exactly what it returns, so text injected downstream would be **WRITTEN BUT NOT MEASURED**, the #41 second-consumer drift. The **AST READER is in `_gen_chain.py` as ruled**; only the splice moved — identical reason to why `dofirst_index` is composed in the slicer. ⚠ **This is an IMPLEMENTATION RECONCILIATION, NOT A RE-RULING, and it is flagged as visible to Dave** [[instruction-right-cause-wrong]]. **(c) `VERDICT_SHA` is typed ON PURPOSE** — it names a fixed historical event, so it cannot go stale the way a COUNT does; everything derived from it is measured.
- **★★ ③ THE PREMISE DEMONSTRATED ITSELF INSIDE ONE DAY — the sharpest evidence the session produced.** #125 measured `len(STEPS)` = **97**; #126 measured **98**. `s125-D2`'s wiring of `_validate_state_contrast.py` added a step **between the probe and the enactment**. ⇒ **the figure went stale again in under 24 hours**, which is precisely the reason Dave chose a generator over a third re-stamp [[no-gate-parses-the-artefact]].
- **★★ ④ A NEW FINDING, NOT A RESTATEMENT: 23 BUILD STEPS HAVE NEVER BEEN INSIDE ANY GREEN VERDICT.** The `#62` green verdict covers the 75 steps that existed at `18c7789`; disk holds 98. The gap was invisible while the figure was a single typed number, and it only became statable once **both** ends were measured.
- **⑤ EVIDENCE, ALL RE-RUN THIS SESSION.** `len(STEPS)` = **98**, **98 distinct labels** (AST); at `18c7789` = **75**, **75 distinct labels** — 1:1 at both ends. **MUTATION BATTERY: 12 bites, 0 fail** — adding a step moves the published figure **98→99** and the gap **23→24** · renaming `STEPS` **REFUSES BY NAME and publishes NO count** · a non-literal `STEPS` refuses · an **unreachable `VERDICT_SHA` declares the COVERAGE unmeasured while still publishing the live count** · a duplicated label is **surfaced rather than counted as growth**. `_build_all.py` was restored **byte-exact (sha256 verified)** after every mutation.
- **⑥ ✅ FIVE PERMANENT BITES WIRED into `_gen_chain.selftest()`** (already a registered build step). **The load-bearing one RE-DERIVES `len(STEPS)` from disk at test time and asserts the chain publishes THAT** — it is the direct answer to *"what re-checks this?"*, the question `s125-D1` exists to force [[a-new-tier-silently-bypasses-its-tests]]. ★★ **AND THE BITES BIT THIS WRAP, ON ITS OWN PROSE:** the marker-leak bite went RED because this banner and this delta, as first written, **spelled the build-verdict marker literally** while describing the enactment — and a MENTION inside chain-resident text is indistinguishable to a cold reader from a **FAILED SUBSTITUTION** [[gate-must-quote-what-it-forbids]]. ⛔ **The gate was right; the prose was the defect. The prose was rewritten and the bite was NOT touched, scoped or exempted** — an instrument driven on real data, failing, on the day it was built [[green-tests-cannot-see-scope]].
- **⑦ GREEN, all rc=0:** `_gen_chain.py --selftest` **all bites pass** · `_gen_chain.py --check` **FRESH** · `_validate_wiring.py` **30 on disk / 30 wired / 0 exempt / 0 failures** · `_build_all.py --selftest` **PASS, 98 steps** · `check_budgets()` **0 blocking failures** (warns are the standing set: §C 164 vs cap 150 = `G4`, the `ds-021` `tk`-vs-`tape` stamp-unit warn, the advisory size caps).
- **⚠ ⑧ ATTRIBUTION CHECKED, AND THE RED IS NOT MINE.** `_capture_gate.py --selftest` is RED on `_governs.py`: ruling **`s121-D1` points at `canon.css:5548`, which does not exist**. **PRE-EXISTING** — `_governs.py` and `canon.css` are untouched in `git status`, and this session's `_capture_gate.py` diff is **20 lines, 0 deletions, gated behind a marker-presence test**. ⛔ **Recorded as a standing open item; NOT fixed** [[attribute-the-diff]].
- **⚙ gauge:** **boot 53,997 real** (`message.usage`, first turn) — ⚠ **the FIFTH datapoint below the published 75,899 floor**, consistent with the post-break n=3 mean of 54,859. ⛔ **RECORDED, NOT re-based — the re-base is DAVE'S and remains UNTAKEN** [[boot-floor-measured-109]]. FILL check-ins **74,120 → 135,735** against the stop line **150,929**; **the wrap was DELEGATED at 135,735 — roll, not ride**, and **the schematic was not started for exactly that reason** [[stop-line-repriced-93]]. Conversation-half throughput at the seam **175,569 real**. ⚠ **Dave's quota panel was ASKED FOR at the opener and NOT GIVEN — recorded as UNKNOWN, never estimated** [[quota-panel-has-three-numbers]] [[feedback-measuring-tool-must-not-guess]].
- **⛔ DO-NOT-RULE — respected in full, carried verbatim:** `G1`–`G17` · floor **75,899** and the re-base · recorder constants · **v1 pack sync (#114)** · mono grey ramp · SC dark · `G8` · type-ratchet debt **1,101 (may only shrink)** · the **19 `LEGACY_IDS`** items · **32.9-vs-32 RED** · `ds-025` · `ds-032` · boot-rent plan · attribution re-probe · the fall-through-class remedy · the UNPROVEN msgfile attribution · **the 4 REAL contrast failures** · **the render-runbook contradiction** · **the `_governs.py`/`s121-D1` red**. **This wrap ruled nothing, changed no value, and edited no gate, threshold or fence** — including `G4`, whose §C 164-vs-150 warn the mover printed and proceeded past (warn ≠ block); **the cap was NOT moved.**
- **Dave's opens UNCHANGED:** P1 confirm-to-open · G4 ratify · recorder-constants refresh · the 3 chart-meta provenance-enum edits.
- **→ #127:** ⬛ ① **THE SCHEMATIC v2** — generated, six subsystems, v1 (`reviews/MEMENTO-SCHEMATIC-2026-07-26-v1.html`) KEPT + TOMBSTONED; **Dave's #125 pick, now rolled TWICE** · ⬛ ② **`effBg` SIBLING BLINDNESS** (32 false failures) · ⬛ ③ **`out[3]` OVERWRITE** + `_STATE-CONTRAST-AUDIT.md` stale by 37 + the `IndexError` on zero snippets + no `--selftest` flag · ⬛ ④ **THE RENDER-RUNBOOK CONTRADICTION — RE-VERIFY, owed at #126 and NOT DONE; now owed at #127** · ⬛ ⑤ **THE 4 REAL CONTRAST FAILURES — DAVE'S** · ⬛ ⑥ **NEW: `_governs.py` selftest RED** (`s121-D1` pointer rot, `canon.css:5548` absent) — found #126 by attribution control, not fixed · ⬛ ⑦ carried: fall-through class still has no gate · `s116-D4`/`s116-D5` · `s114-D2` · stale-mount seam · P4 chain trim · 89-D2 · `ds-032` · `ds-025` · boot-rent plan · attribution re-probe (**THIRTEENTH roll**).


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
