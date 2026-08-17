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

*Last refreshed: 2026-08-17 (Mon from `date` — **#193 wrap**: FABLE conductor + 5 OPUS build subs + this OPUS wrap sub, DELEGATED wrap, **ONE RULING, DAVE'S — `s193-D1` (fix the CLASS, never patch: the sanctioned `--amend-evidence` mode + the once-only memento-package re-sync)**, inscribed by the CONDUCTOR via `_inscribe_ruling.py` (179→180) — ⛔ **this wrap sub wrote NOTHING into `knowledge/_rulings.json`; it CARRIES the conductor's uncommitted inscription.** ✅ **THE COULD-NOT-ASK THIRD VERDICT WIRED** (`d44f023`): exit 77 + a self-naming line across `[59]`/`[71]`/`[109]`/`[112]`/`[113]`, survey counts refusals NON-BLOCKING, `_build_all` taught 77=continue (`48f545e`). ✅ **`--amend-evidence` BUILT + THE PROVENANCE REDS LEGALIZED** (`f773cc2` delta-audit 8→0, `711bfd1` `_governs` reds 11→0); the memento-package re-sync AUTHORIZED ONCE (#64 boundary). ★ **THE DELIVERABLE — THE CI READ-BACK: survey GREEN, render job GREEN, and the chained Knowledge-build RAN THROUGH ALL 120 STEPS for the first time in the repo's history**, reporting the STANDING 44 never-green step debt instead of dying at step 8; ⛔ full build green is a PROGRAMME, not this session's claim. ✅ **THE WIRING'S OWN TWO DEFECTS FIXED** (`27f5342`): unbounded recursion in the state-contrast selftest (40s+ → 0.045s refusal) + the checkout-cannot-hold refusal keyed on `git check-ignore`, mutation-proven both directions. ✅ **THREE HELP-GATE OFFENDERS + TWO #174 DEBTS** exposed by that first chained run (`3eca292`/`7b335ef`/`165f17b`, ASSERT-009 76→77 metas `5e552d5`, KG edge gate `b83d792`, schematic caption geometry `23519bb`/`86c85b8`, index+schematic fixed point `b123372`/`8f41ed2`). ⚙ boot **56,722 real** (in band) · **FILL at wrap-open 215,597 real** — PAST the 150,929 ADVISORY by 64,668 and past the 200,000 working line, **wall 256,000 binding**; **subs 496,124 tokens (n=5, MEASURED)**, this wrap sub's own spend EXCLUDED and unknowable. Effort band **L**. ⚙ QUOTA, RELAYED: All **31%** · Fable **40%**, resetting Thu 10:59PM — ⛔ crank NOT taken. ⬛ STILL DAVE'S: the **standing-44 build-step triage** · the **ds-034/ds-035 gitignored-evidence homing** · the ds-0NN chart-intent reconciliation (⛔ NEVER OPENED this session, on his word) · the `_GRADE-DECISIONS.jsonl` policy · the var-gate's glob width + ds-number · the three remaining `W-31` choices · `STALE_AFTER_SESSIONS` · `BASELINE_DATE` · `CARRY_GATE_BLOCKING` · the trend card (FLOATED) · the `#174` adjudication · all `G`-items · the 19 unconditioned legacy close conditions · the quota crank. ⛔ NOT PUSHED.)*  *Last refreshed: 2026-08-17 (Mon from `date` — **#192 wrap**: FABLE conductor + 1 OPUS build sub + this OPUS wrap sub, DELEGATED wrap, **ONE RULING, DAVE'S — `s192-D1` (WRITE-ONCE promoted to an ADR: live facts get ONE home plus addresses, history frozen)**, inscribed by the CONDUCTOR via `_inscribe_ruling.py` (178→179) — ⛔ **this wrap did NOT write `knowledge/_rulings.json`.** Home: **`docs/decisions/ADR-0017-write-once-live-facts.md`** (`a171e3c`). ✅ **SIDECAR SCHEMA v1→v2 for `rechecked_at_session`** (`4d517cf`, the session's titled item): selftest green, **verdicts UNCHANGED — STILL-UNENACTED 1 · UNPROBEABLE 19 · WEAK-MATCH 1**. ⚠ **THE FINDING — THE BLIND-HARNESS CLASS RECURRED** (`c1991e5`): the `s191-D1` showroom gate went in unstubbed at #191, so at #192's open all **14 commit-path arms were CRASHING and the crashes were read as results**; healed and now **GATED** by `knowledge/_gate_harness_stubs.py`, built consumer-first with a `W-33` row via `_state.add()`, mutation-proven both directions, harness **26→30 arms all green**. ✅ **PARKED-CANDIDATE RECEIPTS** (`b9c72c6`): ds-0NN chart-intent PARKED + WRITE-ONCE floated, ⛔ nothing ruled by that commit. ⚙ **INSTRUMENTATION APPEND DECLARED** (`adcc364`) — the `_GRADE-DECISIONS.jsonl` policy remains DAVE'S. ✅ **PUSHED ON DAVE'S WORD** (*"psh"*) via `bash knowledge/_git_commit.sh --push`; remote verified **`adcc364`** ⇒ the CI read-back of the first BLOCKING-var-gate chained build is now a LIVE debt. ⚙ boot **56,750 real** (in band) · FILL at wrap-open **~125,000 DERIVED** from a relayed room figure of **~26,000** to the **150,929 ADVISORY** (wall **200,000**, `s190-D2`) — ⛔ a delegated sub cannot measure the conductor's window, declared, never invented · **subs 86,140 tokens (n=1, MEASURED)**; this wrap sub's own spend EXCLUDED and unknowable. Effort band **M**. ⚙ QUOTA, RELAYED: All **30%** · Fable **38%**, resetting Thu 10:59PM — ⛔ crank decision NOT taken. ⬛ STILL DAVE'S: the ds-0NN candidate's scope + first consumer · the `_GRADE-DECISIONS.jsonl` policy · the var-gate's glob width + ds-number · the three remaining `W-31` choices · `STALE_AFTER_SESSIONS` · `BASELINE_DATE` · `CARRY_GATE_BLOCKING` · the trend card (FLOATED) · the `#174` adjudication · all `G`-items · the 19 unconditioned legacy close conditions · the quota crank. ✅ PUSHED.)*  *Last refreshed: 2026-08-17 (Mon from `date` — **#191 wrap**: FABLE conductor + 2 OPUS build subs + this OPUS wrap sub, DELEGATED wrap, **THREE RULINGS, DAVE'S — `s191-D1` (the showroom sync gate BLOCKS at the commit seam, `SHOWROOM_ACK` the declared hatch) · `s191-D2` (HOME-OR-DECLARE: a hook's artefact is homed in-repo or its non-repo home is DECLARED and graded as such) · `s191-D3` (the dataviz var-gate is a GATE, not an advisory)**, all three inscribed by the CONDUCTOR via `_inscribe_ruling.py` (175→178) — ⛔ **this wrap did NOT write `knowledge/_rulings.json`.** ✅ **DV-J1 DISCHARGED, NOT BUILT** (`7c95f9c`): the scope was already closed by DV-J2 (#27) + `s182-D2`; the real residue was the **showroom serving deleted markup FOUR RULINGS STALE** — `gen_showroom` regenerated 5 pages, gates green. Same commit: the **119-sweep boot consumer** in `_checkin.py` driven FRESH/EXPIRED/UNKNOWN-AGE/NO-SIDECAR, **4 declare-dirt harness arms**, and ★ **THE FINDING — the commit harness had been BLIND since #188** (the unstubbed doc-row gate made every commit-path arm a crash read as a result); healed, **26 arms green**. ✅ **SHOWROOM SYNC GATE** (`165fe11`): BLOCKING at the commit seam, driven both ways — a planted stale page REFUSED with nothing staged. ✅ **HOME-OR-DECLARE ENACTED** (`8a89b75`): `render.py` HOMED at `knowledge/_render/render.py` (runbook copies, never retypes); the NON-REPO adjacent marker taught to `_gardener.py`, mutation arm **g13** bites both ways; real-store refresh flipped **both STALE hooks FRESH honestly** — store **FRESH 96 · AGING 4 · STALE 0 · UNPROVABLE 27**; DV-J1 row set landed with a **two-halves receipt on Dave's word**, lanes regenerated. ✅ **VAR-GATE PROMOTED** (`9eaed64`): ADVISORY → GATE in both `_build_all.py` tables, the `#166` labels moved together as JOIN KEYS, `check_routes` selftest green **119**; the **DV-J2b record clash annotated OVERTAKEN** in `GOOD-MORNING.md` + `knowledge/_state.json` naming **`s182-D2`** as the operative closure (added, never trimmed); one hash typo in the inscribed ruling fixed textually PRE-commit, declared. ⚙ boot **56,496** (in band) · FILL at wrap-open **167,166** — PAST the **150,929 ADVISORY** by 16,237, **DECLARED**, with legal room to the **200,000** wall (`s190-D2`) · **subs 226,216 tokens (n=2, MEASURED)** — 107,228 + 118,988; this wrap sub's own spend EXCLUDED and unknowable from inside. Effort band **M**. ⬛ STILL DAVE'S: the var-gate's **glob width + ds-number** · the three remaining `W-31` builder choices · the sidecar schema bump for `rechecked_at_session` · `STALE_AFTER_SESSIONS = 15` · `BASELINE_DATE` · `CARRY_GATE_BLOCKING` · the trend card (FLOATED) · all `G`-items · the 19 unconditioned legacy close conditions · the quota crank. ⛔ NOT PUSHED.)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#190 wrap**: FABLE conductor + 3 OPUS subs + this OPUS wrap sub, DELEGATED wrap, **TWO RULINGS, DAVE'S — `s190-D1` (`STEP_STATES` widened with `superseded`; a superseded step whose receipt names no `sN-DN` is REFUSED) · `s190-D2` (the 150,929 line is ADVISORY wrap-open; **200,000 BINDS**)**, both inscribed by the CONDUCTOR via `_inscribe_ruling.py` — ⛔ **this wrap did NOT write `knowledge/_rulings.json`.** ✅ **B3 GRADER FIXED** (`1e8005b`): memory-store indexing + a token-adjacent use-vs-mention negation guard; 23 selftests green; store **FRESH 94 · AGING 4 · STALE 2 · UNPROVABLE 27**, both STALE honest. ✅ **`STEP_STATES` WIDENED** (`fc3015a`): DV-J2b row aligned, lanes regenerated, NEXT pointer now **DV-J1** — an Opus sub had REFUSED DV-J2b as superseded (`s182-D2`, `27b421a`), the #185 trap recurring. ✅ **MEMENTO PHASE 2 CLOSED** (`13d389d`): `W-19`/`W-20`/`W-22`/`W-24`/`W-27` closed with receipts, each VERIFIED AND DRIVEN; store live 39 → 34. ✅ **THE DATAVIZ VAR-RESOLUTION GATE BUILT** (`e568dcf`): `knowledge/_gate_dataviz_vars.py`, 4 themes + alias chains, 8 plant-then-detect arms; REAL DRIVE 15 files · 688 refs · **0 dead**; ADVISORY in `_build_all.py` steps 93/94. ⚠ **REDUNDANT-RECORD HYGIENE ITEM FLAGGED, UNTOUCHED**: `GOOD-MORNING.md:52` + `knowledge/_state.json:34` both claim *"DV-J2b FOLDED+ENACTED #67"* — DAVE'S EYE. ⚙ boot **56,424** (in band) · FILL at wrap-open **141,685** vs the ADVISORY **150,929** (wall **200,000**, `s190-D2`) · **subs 224,206 tokens (n=3, MEASURED)**; this wrap sub's own spend EXCLUDED and unknowable. ⬛ The four `W-31` choices · `CARRY_GATE_BLOCKING` · the var-gate's severity/glob/ds-number · the trend card (FLOATED) · `W-22`/`W-24` policy · the `#174` adjudication remain DAVE'S. ⛔ NOT PUSHED.)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#189 wrap**: FABLE conductor + one OPUS build sub + one SONNET trace sub + this OPUS wrap sub, ⛔ **NO RULINGS — no `s189-D*` exists; `knowledge/_rulings.json` was NOT written this session.** ✅ **`W-31` BUILT (`s188-D1`)** — `knowledge/_gardener.py` grades the hook FILE with a declared index-line fallback; 16 mutation bites; suffix-match fix for the #180 false-STALE class; `hook_file_probe_companion` deleted per `s188-D3`. **RE-MEASURED live: FRESH 93 · AGING 4 · STALE 3 · UNPROVABLE 27** (was 14/1/0/112 on the wrong text) — the honest B3 figures. ✅ **`W-32` BUILT (`s188-D2`)** — the 2c carry gate in `knowledge/_capture_gate.py` (`retraction_receipt` + `carry_wording_check`, wired in `wrap_checks`, BLOCKING), mutation-proven 3 directions, driven on 10 real archived wraps: **11 un-receipted rewordings** found. ✅ **`W-28`/`W-29`/`W-30` TRACED AND CLOSED** with receipts; `s178-D1`(a)'s receipt is wrap commit `2d2ff44`. ⚙ boot **56,432** (in band) · FILL at wrap-open **~115,309** vs stop **150,929** ⇒ room **~35,620**, UNDER the 42–49K wrap band ⇒ **this wrap is DELEGATED**. **subs 222,532 tokens (n=2, measured)** (QUOTA, never fill; this wrap sub's own spend declared separately in chat). ⬛ **FOUR `W-31` builder choices + `CARRY_GATE_BLOCKING` are PICKED, NOT RULED — DAVE'S EYE OWED.** ⛔ NOT PUSHED.)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#188 wrap**: FABLE conductor, IN-WINDOW wrap, Dave LIVE, **THREE RULINGS — `s188-D1` (grader reads the hook FILE) · `s188-D2` (retraction carve-out, receipt required) · `s188-D3` (supersession explicit: D1 retires `s183-D1` P1; D2 strengthens its P2; P3/P4/P5 in force)**, all via `_inscribe_ruling.py`, 170→173. ✅ Lane B landed (one Opus sub, 106,202 tk n=1): `W-19` compaction declared line mutation-proven · `W-22` instrumentation dirt DECLARED, policy Dave's · `W-24` refusal reworded + expiry stamp, token-scope byte-identical. ✅ Lane C landed: `_gate_doc_rows.py` proven-able-to-fail on the real pre-row store, WIRED blocking into `_git_commit.sh`, live finding 3 unrowed s176 briefs → `W-28`–`W-30`; store 53. ★ FINDING: the chain called pass-8 unruled while `s183-D1` held it — the rulings store is the authority. ⚙ boot 56,303 · FILL at wrap-open 133,776 vs stop 150,929 ⇒ room 17,153; in-window on room-to-WORKING 66,224. ⚠ 2c/2d rolls + dossier DECLARED SKIPPED with sizes (see ⏱ LATEST). ⛔ NOT PUSHED.)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#187 wrap**: FABLE conductor, IN-WINDOW wrap, Dave LIVE, ⛔ **NO RULINGS**. ★ Phase 2 opened: rows `W-19`–`W-27` via `_state.add()`; lane divvy inscribed (`W-27`); `W-25` CLOSED VERIFIED-MOOT (enacted #178 — stale promotion premise, pass-8 P2 class); `W-21` BUILT (`_recheck_119_sweep.py`, mutation-proven; 1 STILL-UNENACTED / 19 UNPROBEABLE DECLARED); `W-23` ENACTED (`--push` call form added, 0→3 mentions); `W-26` registers the compaction brief. Pass-8 P1–P5 floated, Dave's. ⚙ boot 56,271 · FILL at wrap-open 144,361 vs stop 150,929 ⇒ room 6,568; in-window on room-to-WORKING 55,639. ⛔ NOT PUSHED.)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#186 wrap**: FABLE conductor, IN-WINDOW wrap, Dave LIVE throughout, **TWO RULINGS, DAVE'S — `s186-D1` (compaction five questions: Q1 ratified · Q2 ruled+inscribed in `_RUNBOOK-context-gauge.md` · Q3/Q4 parked with triggers · Q5 ruled as a Phase 2 row) and `s186-D2` (pass 6 P1–P4 promoted · P5 KEEP · pass 7 P1 promoted)**, both via `_inscribe_ruling.py`, 168→170. ✅ **`W-18` CLOSED** via `_state`'s own writer (check OK, diff 3 lines); `W-17` open, condition ratified. ✅ **Memory step 3 RAN** — #184 items found already present (stale carry); the #185 forgotten-document hook WRITTEN. ⚙ boot 56,163 · FILL at wrap-open 125,280 vs stop 150,929; in-window on the budget arithmetic, no subs. ⛔ **NOT PUSHED.**)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#185 wrap**: FABLE conductor + this OPUS wrap sub, Dave LIVE throughout, ⛔ **NO RULINGS — `knowledge/_rulings.json` NOT WRITTEN, NOT OPENED FOR EDIT; no `s185-D*` exists.** ✅ **THE DREAM-PASS SEAM IS BUILT AND COMMITTED** — `knowledge/_checkin.py` prints a DREAM block at boot (newest proposals file by mtime+header + a git-log enact probe, three branches), **mutation-proven** (the pass-9 probe returns empty). Evidence: commit `ccc3d45` · 2026-08-16. ⚠ **CAUSE, OWNED IN CHAT BY THE CONDUCTOR:** the #185 opener reported the dream pass unverified while the fired-at-06:10Z evidence was on the check-in's own GRADES line — [[refusal-names-the-first-obstacle]]. ✅ **DREAM PASS 8 CONFIRMED:** fired **06:10Z on schedule** (the FIRST scheduled pass; the B3 counting window is OPEN); P1–P5 all promoted `s183-D1` and enacted at commit `eaaee37` 13:11. **Nothing from pass 8 is outstanding.** Backlog: **pass 6 P1–P5 floated · pass 7 P1 deferred**. ✅ **DV-J2b FOUND SUPERSEDED BEFORE ANY BUILD** — the lane queue (2026-07-28) vs `s182-D2` (#182); **the queue is the defect**, and `knowledge/_lanes.json` is amended by this wrap (state `superseded`, receipt appended). ⛔ **No sparkline code was touched.** ★ **TWO FORGOTTEN DOCUMENTS SURFACED BY DAVE:** `_MEMENTO-REBUILD-PROPOSAL-2026-08-02-v1.md` (parts 1–3 built — state store + generated chain; **parts 4–5 NOT done**: GM still **71,928 real**, boot **56,069** vs the promised ~2K) and `_BRIEF-compaction-strategy-2026-08-15-v1.html` (**five §06 questions never surfaced**). **NEITHER HAD A STORE ROW — the forgotten-document class, named.** ✅ **THE MEMENTO CLOSE-OUT PLAN IS APPROVED** (Dave, verbatim: *"okay sounds good … go for it"*) — inscribed by this wrap as `notes/_briefs/2026-08-16-memento-closeout-plan.md` (**status: standing**, ⛔ NOT ruled) plus **two new store rows `W-17`/`W-18`**, both with `closes_when`, added via `_state.add()` (the gate's own writer). #186 opens at **Phase 1**. ✅ **COMMIT-RUNBOOK LESSON INSCRIBED:** a msgfile headline carried its own session prefix and the subject **doubled**; amended from a fresh msgfile (`ccc3d45` is the amended result) ⇒ `knowledge/_RUNBOOK-git-commit.md` step 3 now forbids it. ⚙ **GAUGE (relayed):** **FILL 112,533 real at the wrap-open decision** (BUDGET line, `message.usage`) vs stop **150,929** — the wrap was delegated on the budget-binds rule. Context gauge at authoring: 🔴 ~75% (ESTIMATE). ⛔ **NOT RULED / NOT TOUCHED:** every pass 6 P1–P5 · pass 7 P1 · the five compaction questions · the trend card · every colour value · `knowledge/_rulings.json` · memory files (the conductor's) · `knowledge/_build_all.py` · ⛔ **NOT PUSHED.**)*  *Last refreshed: 2026-08-16 (Sun from `date` — **#184 wrap**: FABLE conductor + **TWO OPUS build subs** + this OPUS wrap sub, Dave LIVE throughout, **THREE RULINGS, DAVE'S — `s184-D1` · `s184-D2` · `s184-D3`**, all three inscribed via `knowledge/_inscribe_ruling.py`, the only sanctioned writer. ⬛ **`s184-D1`: *"the line should be responsive to its enclosure by default"*** — readback *"this is all correct"*; ⛔ the **4px height-snap was NOT picked** and stays OPEN DIRECTION; heights 64/44 UNCHANGED. ⬛ **`s184-D2`: the MONO-ONLY riders of `s151-D1`/`s149-D1` do NOT restrict the sparkline's semantic stroke keying — `s182-D3`'s all-four-themes reading STANDS**, riders not re-stamped. ⬛ **`s184-D3`: breach/watch/healthy/info → negative/monitor/positive/neutral**, chart-consumer alias layer only, `rag-*` untouched; the `neutral` double-meaning was surfaced and knowingly accepted. ✅ **BOTH ENACTED AND BOTH RENDER-PROVEN:** the sparkline goes `width:100%` with the JS-gated release DELETED (+55/−12) behind a NEW `knowledge/_render/verify_sparkline_responsive.py` that **caught two mutations four gates waved through**; the rename is **equal +/− across four files with HEAD-vs-tree PNGs BYTE-IDENTICAL (115,915 B, sha256 `5da382519c1bc905…`)**. ★ **FINDING: a dangling dataviz var renders SILENT BLACK past all thirteen gates** — appended to `_DS-IMPROVEMENTS.md` as *"chart var-resolution gate"*. ⚠ **The `#174` adjudication has a delivered plain description + three options and NO PICK — description ≠ decision.** ⚙ **GAUGE (relayed):** boot **56,013 real** INSIDE the `s171-D1` band · FILL at wrap-open **110,497 real** (floor, late by one step) vs stop **150,929** ⇒ room **40,432** · job window ≈ **54,484 real** · **`subs 149,889 tokens (n=2)`** (QUOTA, never fill). ⛔ **MEMORY step 3 NOT RUN — the store is unreachable from a delegated wrap sub (read-only in bash, outside the file tools' connected folders); the owed additions are itemised on the residual.** ⛔ **NOT PUSHED.** Dossier: `_DECISION-HISTORY/2026-08-16-184-the-responsive-sparkline-and-the-status-rename.md`.)*  * the `#168`/`#168-A` `canon.css` comment: **PREMISE EXPIRED**, already deleted by the generator and committed at **`76b024c`** (#174), recoverable verbatim at `git show 76b024c^:knowledge/canon/canon.css` **lines 4123–4133**, and restoring it would **re-insert superseded hexes** ⇒ ⬛ **DAVE'S adjudication of the #174 deletion**; both `gen_canon_components.py --check` and `gen_theme_cascade.py --check` are **rc=1 today**. **(2)** the `--status-*` fall-through: **DAVE'S EYE by the record's own words**, and `_LIVE-STATE-ARCHIVE.md:112` records the edit as **already shipped at #174** ⇒ what is open is his eye on a **shipped** change. **(3)** the `#158` preamble port to the 8 package copies: **RE-PRICED — a verbatim port BREAKS all eight** (`ModuleNotFoundError: _helpgate` does not ship); the real close is a **RELEASE change** (ship `_helpgate.py` + `KNOWN_FILES` at `_validate_package_delta.py:85-86` + `_MACHINERY-MANIFEST.md` + a dist rebuild) ⇒ ⬛ **DAVE'S WORD**; `_validate_package_delta.py` **rc=1, 8 failures, 6 lines each** at that point. ✅ **BUILD SUB B (queued checks lane, 129,227 tokens) BUILT BOTH.** **(i) THE `[112]`/`[107]` READ-CHAIN GATE:** `knowledge/_gen_chain.py` **+137 lines** — `stamped_tier()` plus a **COULD-NOT-ASK clause in `check()` BEFORE the byte compare**, exiting non-STALE when the **reachable** tier ≠ the **stamped** tier with **both tiers named**; an unreadable stamp is also COULD-NOT-ASK; `write()` untouched so offline generation still works; **11 new selftest bites**, and the **mutation arms mutate the STAMP** (forcing the fallback would be unreachable where the defect lives). `.github/workflows/gates.yml` **+43** — `fetch-depth: 0` on both checkouts and **the lying comment corrected with the mechanism written out**. Remedy **quoted** from `notes/_receipts/2026-08-14-s173-ci-triage.md` (*"(c) is the recommendation… ~8–12K"* + *"fetch-depth: 0… ~2K"*). **Driven end-to-end: HEAD's copy said STALE, the new code says COULD-NOT-ASK, same tree, same env.** **(ii) THE EVIDENCE-FORMAT ENFORCEMENT CHECK** (`s177-D1`'s rolling-file rule): `knowledge/_governs.py` **+62** (`ROLLING_FILES` + `rolling_target()`, the ruling's own three files enumerated) and `knowledge/_inscribe_ruling.py` **+68** — **refusal `R6`**, 8 selftest arms; **driven on `s171-D1`'s real evidence string → rc=3 REFUSED**, the cured form accepted, `_rulings.json` md5 **`0f9490e7…` unchanged**; ⛔ **deliberately NOT wired into `_governs --selftest`/render** so the **11 ratified fails do not turn red** (byte-identical selftest output proven). ⚠ **The *"PRICED"* claim in `s177-D1` has NO number on the record anywhere — DECLARED, not invented.** ✅ **CONDUCTOR VERIFIED, OWN RUNS, UNPIPED:** `_gen_chain.py --selftest` rc=0 all bites · `--check` rc=0 **FRESH** · `_inscribe_ruling.py --selftest` rc=0 all arms · `_rulings.json` md5 **`0f9490e7bf6876bfef2fd11eed2cf506` unchanged**. ⚠ **ONE PITFALL CAUGHT LIVE:** a `/tmp` redirect Permission-denied made a selftest read rc=1 — **the redirect's rc, not the test's**; re-run clean [[a-crash-is-not-a-fail]]. ⚠ **RESIDUALS NEW THIS SESSION:** the **survey bucket is NOT wired** (no exit-code protocol for could-not-ask exists; `[107]` still lands in the survey FAIL column in CI; close ≈ **4–6K PICKED** + a ruling on the protocol, **Dave's**) · **`[113]` package delta grew 6 → 143 lines** on `_gen_chain.py`'s two package copies — **deliberate, a package is a RELEASE**; 2 of the 8 delta findings are now this session's · ⚠ **UNPROVEN: real CI** — both fixes proven **locally only**; price = next push + run read-back ~2K, and ⛔ **push is Dave's word, NOT taken**. ⚙ **GAUGE (relayed):** boot **55,945 real** INSIDE the `s171-D1` band per `knowledge/_gauge_tokens.py` · **FILL at wrap-open 116,441 real — a FLOOR, late by one step — vs stop 150,929 ⇒ room 34,488, UNDER the 42–49K wrap price**, which is why this wrap is delegated · job window ≈ **60,496 real** · **`subs 210,070 tokens (n=2)`** (QUOTA, never fill; this wrap sub's own spend EXCLUDED and unknowable). ✅ **MEMORY step 3 RAN — the conductor's, in-window:** `banner-brackets-are-ages.md` NEW + its `MEMORY.md` index line; **declared, not claimed**. ⛔ **NOT RULED/NOT TOUCHED:** ⚠ **the scaling call at tuner v2 was NOT TAKEN — Dave went out; it remains #184's natural opener, DAVE'S EYE, wording unchanged** · the MONO-ONLY rider reconciliation · the trend card (floated) · every colour value (`s151-D1`/`s149-D1`/`s155-D1`/`s182-D3`) · the compaction five questions · `knowledge/_rulings.json` · memory files (the conductor's) · `knowledge/_build_all.py` (**NOT RUN — `#166` labels are JOIN KEYS**) · **scheduled tasks** (the first scheduled dream-pass fires **2026-08-16 07:10**, untouched) · the 11 ratified `_governs` fails · ⛔ **NOT PUSHED**. Dossier: `_DECISION-HISTORY/2026-08-16-183-the-brackets-were-ages-and-both-checks-landed.md`.)*  *Last refreshed (#182 and earlier, rolled #179–#186 — 2d boundary): full text moved to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-16 #186, § Rolled 2026-08-16 #185, § Rolled 2026-08-16 #184, § Rolled 2026-08-16 #183, § Rolled 2026-08-15 #182, § Rolled 2026-08-15 #181, § Rolled 2026-08-15 #180, § Rolled 2026-08-15 #179, § Rolled 2026-08-15 #178, § Rolled 2026-08-15 #177, § Rolled 2026-08-15 #176, § Rolled 2026-08-14 #175, § Rolled 2026-08-14 #174, § Rolled 2026-08-14 #173, § Rolled 2026-08-14 #172, § Rolled 2026-08-14 #171, § Rolled 2026-08-14 #170, § Rolled 2026-08-13 #169, § Rolled 2026-08-13 #168, § Rolled 2026-08-13 #167, § Rolled 2026-08-12 #164, § Rolled 2026-08-12 #163, § Rolled 2026-08-12 #162, § Rolled 2026-08-12 #161, § Rolled 2026-08-12 #160, § Rolled 2026-08-12 #159, § Rolled 2026-08-12 #158, § Rolled 2026-08-12 #157 and § Rolled 2026-08-11 #156.*
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
- ⛔ DV-J2b — sparkline toggle markup + CSS (JS already injected, dormant) — superseded · receipt State word aligned #190 under s190-D1 (enum widened; the #185 'queued-but-superseded' trap is dead). knowledge/_proforma/_DATAVIZ-DECISIONS.md § Open/pending (split from DV-J2 by Dave's ruling #27 — scatter half only, to keep the diff attributable) · SUPERSEDED s182-D2 (#182): sparkline is an atom alone; table CTA moved to the future trend-card component (floated, not ruled). Successors: trend-card composition (needs Dave's word) or sparkline colour/height-snap at the tuner.
- ✅ DV-J1 — table-idiom unification (was ex-M4a) — landed · receipt LANDED BY TWO HALVES, Dave's word #191 ('call it landed, with a receipt naming both halves'): scatter half fixed under DV-J2 (#27); sparkline half DELETED by s182-D2 ('the sparkline is an atom alone') — outcome verified mechanically #191: 21 markup <summary> across 13 chart snippets, 0 off-idiom (corrected probe, markup-anchored); stale showroom surface regenerated 7c95f9c
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
**Status (2026-08-15, dream pass 7): SCHEDULED fire, ⚠ a day EARLY (Sat 08:13 vs the ruled Sun 07:10 — declared, not reconciled). Not overdue (pass 6 = 08-09). 4 proposals FLOATED, 0 ruled (Dave absent — a scheduled run cannot rule): P1 STANDING-CARRY line `GOOD-MORNING.md:438` untouched 56 sessions with split ordinals ("SEVENTH" vs "twelfth") · P2 the ~26K GM-boot overspend went measured→measured→UNMEASURABLE at #176 (no boot-read declaration required anywhere) · P3 three memory files publish boot figures outside the ruled `s171-D1` band on the retrieval surface (one description says 75,899 vs constant 56,158 ±849) · P4 enacting a ruling breaks its predecessor's provenance anchor by construction (2 of 157 today, one per re-base forever). Output `notes/_dream/2026-08-15-proposals.md`, commit `69fba90`. Dreamer = Opus pinned, conductor = Fable; spot-checks 4/4 held (one `git log -L` "exactly one commit" imprecision chased — the trace lists 3, the latest touch e3174d1 #120 is the substance, benign). 7 checked-clear (dd1–dd7) incl. pass-6 P1 re-measured (still exactly 21 sweep strings, store now 157). ⚠ The 2026-08-09 pass's P1–P5 are STILL FLOATED awaiting Dave — now nine proposals on the table across two files. ⚠ `notes/_REHEARSAL-LOG.jsonl` was dirty at commit time (the gate-run append, pass-6 P2's class) — left out of the lane commit and flagged per the mechanical rule. Commit carries `after #176` — the lane-numbering seam from pass 6 remains unruled.


## ⏱ LATEST DELTA — 2026-08-17 (Mon from `date`) (**#193**, FABLE conductor + 5 OPUS build subs + this OPUS wrap sub, DELEGATED wrap, **ONE RULING, DAVE'S — `s193-D1`**)

**Landed (evidence per claim; sixteen work commits — `d4bf842` · `d9923cb` · `d44f023` · `f773cc2` · `711bfd1` · `27f5342` · `3eca292` · `7b335ef` · `165f17b` · `5e552d5` · `b123372` · `8f41ed2` · `48f545e` · `23519bb` · `86c85b8` · `b83d792` — ALL PUSHED except this wrap's own commit, which additionally carries the conductor's uncommitted `s193-D1` inscription):**

- ⬛ **`s193-D1` RULED AND ENACTED — FIX THE CLASS, NEVER PATCH** — Dave's words: *"whatever fixes this without patching, lets wire it all properly"* and *"okay I want this rock solid"*. Two decisions on an explicit yes: **(a)** `knowledge/_inscribe_ruling.py` gains a SANCTIONED **`--amend-evidence`** mode with the same byte-reconstruction proof as append — **evidence array ONLY, `says` unreachable BY CONSTRUCTION** — and the `s176-D2`/`s178-D1` + `s175-D1`/`s176-D1` evidence entries are legalized with factual pointers, **nothing retyped** (`f773cc2`, delta-audit **8 → 0**; `711bfd1` closes the remaining five, capture-gate `_governs` reds **11 → 0**); **(b)** the memento-package VERBATIM SET re-sync is **AUTHORIZED ONCE for #193** (the #64 release boundary), ⛔ **explicitly NOT a standing rule**. Inscribed by the CONDUCTOR via `_inscribe_ruling.py` (rulings 179→180) — ⛔ **this wrap sub wrote NOTHING into `knowledge/_rulings.json`; it CARRIES the conductor's inscription in its commit.**
- ✅ **THE COULD-NOT-ASK THIRD VERDICT IS WIRED (`d44f023`)** — `knowledge/_could_not_ask.py`: **exit 77 + a self-naming first line**, across the tier/reach-dependent gates **`[59]` `[71]` `[109]` `[112]` `[113]`**; `_build_survey.py` counts refusals **NON-BLOCKING**, `_build_all.py` was taught **77 = continue** (`48f545e`, where the assertion gate joined the class: RootUnreachable 77 vs unknown-root FAIL, **M2 intact**).
- ★ **THE DELIVERABLE — THE CI READ-BACK, AND THE FIRST FULL 120-STEP CHAINED BUILD IN THE REPO'S HISTORY** — survey **GREEN** (0 FAIL, honest ⊘ refusals) · render job **GREEN** (the recursion fix proven at browser tier) · and the chained Knowledge-build, which had been **dying at step 8**, now **RUNS ALL 120 STEPS** and reports the **STANDING 44 never-green step debt** (e.g. `[34]` text/icon contrast audit, red locally too; the wrap-ritual arms in the capture gate). ⛔ **FULL BUILD GREEN IS A PROGRAMME, NOT A CLAIM OF THIS SESSION.**
- ⚠ **THE WIRING'S OWN TWO DEFECTS, FOUND AND FIXED (`27f5342`)** — **(i)** the state-contrast selftest had **UNBOUNDED RECURSION** (a planted-playwright child spawned grandchildren; **40s+ → a 0.045s refusal**) · **(ii)** the capture-gate checkout-cannot-hold refusal is now keyed on **`git check-ignore`**. **Mutation-proven both directions.**
- ✅ **THREE HELP-GATE OFFENDERS AND TWO #174 DEBTS, ALL EXPOSED BY THE FIRST CHAINED RUN** — help-gate wired into `render.py`, `_recheck_119_sweep.py`, `_gate_doc_rows.py` (`3eca292`/`7b335ef`/`165f17b`) · **ASSERT-009 re-measured 76 → 77 metas** (`5e552d5`; the 77th is `progress-bar.meta.json`, rot **four sessions** old) · the **KG edge gate healed** and progress-bar joined the KG (`b83d792`) · schematic caption geometry **class-fixed** for the tape tier, compact unit `cl100k EST`, both spellings read (`23519bb`/`86c85b8`) · the memento index + schematic reconciled to a **fixed point** (`b123372`/`8f41ed2` — the "index LAST" lesson paid twice in one session).
- ⚙ **INSTRUMENTATION APPEND, DECLARED (`d9923cb`)** — ⛔ **the `_GRADE-DECISIONS.jsonl` exclude / commit / relocate POLICY remains DAVE'S** (dream pass 6 P2); the append is declared, not decided. ⚙ **DECLARED: sub 3's first commit SUBJECT-DOUBLED** (the `#185` class) and was repaired in-session by the documented amend-from-a-fresh-msgfile remedy.
- ⚙ **GAUGE.** boot **56,722 real** (in band) · **FILL at wrap-open 215,597 real** — the conductor's OWN `_checkin.py` measurement, relayed: **PAST the 150,929 ADVISORY by 64,668 and past the 200,000 working line, with the 256,000 wall BINDING** · **subs 496,124 tokens (n=5, MEASURED)** — 60,653 · 150,840 · 120,592 · 66,654 · 97,385; ⛔ this wrap sub's own spend is **EXCLUDED and unknowable from inside**. Effort band **L**. ⚙ **QUOTA PANEL, RELAYED ONLY:** All **31%** · Fable **40%**, resetting Thu 10:59PM — ⛔ **the crank was NOT taken** (one window, more delegation).
- ⛔ **NOT RULED / NOT TOUCHED:** the **standing-44 build-step triage** (DAVE'S READING) · the **ds-034/ds-035 gitignored-evidence homing** (HOME-OR-DECLARE, `s191-D2`, DAVE'S) · the **ds-0NN chart-intent reconciliation** (⛔ **never opened this session — the CI lane consumed it on Dave's word**; still owed on its own terms) · the `_GRADE-DECISIONS.jsonl` policy · the var-gate's **glob width and ds-number** · the three remaining `W-31` builder choices · `STALE_AFTER_SESSIONS = 15` · `BASELINE_DATE` · `CARRY_GATE_BLOCKING` · the trend card (**FLOATED — never re-put as an option**) · the `#174` adjudication · every colour value · all `G`-items · the 19 unconditioned legacy close conditions · quota crank decisions · **memory step 3 NOT RUN from this seat** (a delegated wrap sub cannot reach the store) · ⛔ **NOT PUSHED — push is Dave's word and the conductor relays it.**

## ⏱ PRIOR DELTA — 2026-08-17 (Mon from `date`) (**#192**, FABLE conductor + 1 OPUS build sub + this OPUS wrap sub, DELEGATED wrap, **ONE RULING, DAVE'S — `s192-D1`**)

**Landed (evidence per claim; the five work commits are `b9c72c6` · `4d517cf` · `c1991e5` · `a171e3c` · `adcc364`, in that order, and ALL ARE PUSHED — remote verified at `adcc364`):**

- ⬛ **`s192-D1` RULED AND ENACTED — WRITE-ONCE IS ADR-0017 (`a171e3c`)** — Dave's words: *"promote WRITE-ONCE to an ADR, but lets get this fixed very soon, it's foundational"*. Home: **`docs/decisions/ADR-0017-write-once-live-facts.md`**. The principle: **live facts get ONE home plus addresses; history is frozen**; the `ds-0NN` block stands as the period record, not as a second live copy. Inscribed by the CONDUCTOR via `knowledge/_inscribe_ruling.py` (rulings 178→179) — ⛔ **this wrap did NOT write `knowledge/_rulings.json`.** ★ Floated at `b9c72c6` and RULED the same session: the accrete-from-duplication rule holds new work immediately.
- ⚠ **THE FINDING, AND IT IS A RECURRENCE: THE COMMIT HARNESS WENT BLIND A SECOND TIME (`c1991e5`)** — the `s191-D1` showroom gate went into `_git_commit.sh` **unstubbed at #191**, so at #192's open **all 14 commit-path arms were crashing and the crashes were read as results**. Healed, and this time **GATED**: `knowledge/_gate_harness_stubs.py`, built **consumer-first**, `W-33` row created through `_state.add()` at creation, **mutation-proven both directions**, harness **26 → 30 arms, all green**. ★ The class has now recurred TWICE (doc-row #188, showroom #191) [[a-crash-is-not-a-fail]] [[forgotten-document-class]].
- ✅ **THE SESSION'S TITLED ITEM LANDED — SIDECAR SCHEMA v1 → v2 FOR `rechecked_at_session` (`4d517cf`)** — selftest green; **verdicts UNCHANGED: STILL-UNENACTED 1 · UNPROBEABLE 19 · WEAK-MATCH 1**. A schema bump that moved no verdict is reported as exactly that.
- ✅ **THE OTHER-LANE PARKED-CANDIDATE RECEIPTS COMMITTED AS-IS (`b9c72c6`)** — the ds-0NN chart-intent candidate **PARKED** (scope + first consumer owed on its own terms) and WRITE-ONCE **floated**; ⛔ nothing ruled by that commit.
- ⚙ **INSTRUMENTATION APPEND, DECLARED (`adcc364`)** — one line into `notes/_dream/_GRADE-DECISIONS.jsonl` from the pre-push check-in. ⛔ **The exclude / commit / relocate POLICY for that file remains DAVE'S** (dream pass 6 P2).
- ✅ **PUSHED ON DAVE'S WORD (*"psh"*)** via the ruled call form `bash knowledge/_git_commit.sh --push` (`s133-D2`, the ONLY push path); remote verified equal to **`adcc364`**. ⇒ the **CI read-back of the first BLOCKING-var-gate chained build is now a live debt**, not a hypothetical.
- ⚙ **GAUGE.** boot **56,750 real** (in band) · **FILL at wrap-open: RELAYED AS ROOM — ~26,000 to the 150,929 ADVISORY** (⇒ ~125,000 FILL), wall **200,000** binding (`s190-D2`). ⛔ A delegated wrap sub cannot measure the conductor's window; the FILL figure is the arithmetic complement of a relayed room figure and is DECLARED as such, never presented as an independent measurement · **subs 86,140 tokens (n=1, MEASURED)** — the Opus build sub; this wrap sub's own spend is EXCLUDED and unknowable from inside. Effort band **M**. ⚙ **QUOTA PANEL, RELAYED ONLY:** All **30%** · Fable **38%**, resetting Thu 10:59PM — Fable was the hot budget; ⛔ **the crank decision is DAVE'S and was not taken.**
- ⛔ **NOT RULED / NOT TOUCHED:** the ds-0NN chart-intent candidate's scope + first consumer · the `_GRADE-DECISIONS.jsonl` policy · the var-gate's **glob width and ds-number** · the three remaining `W-31` builder choices · `STALE_AFTER_SESSIONS = 15` · `BASELINE_DATE` · `CARRY_GATE_BLOCKING` · the trend card (**FLOATED — never re-put as an option**) · the `#174` adjudication · every colour value · all `G`-items · the 19 unconditioned legacy close conditions · quota crank decisions · `knowledge/_rulings.json` (**not written by this wrap**) · memory files (**step 3 ran at the CONDUCTOR's seat: the write-once hook flipped floated→canon + its `MEMORY.md` index line; a wrap sub cannot reach the store**).

## ⏱ PRIOR DELTA — 2026-08-17 (Mon from `date`) (**#191**, FABLE conductor + 2 OPUS build subs + this OPUS wrap sub, DELEGATED wrap, **THREE RULINGS, DAVE'S — `s191-D1` · `s191-D2` · `s191-D3`**)

**Landed (evidence per claim; the four work commits are `7c95f9c` · `165fe11` · `8a89b75` · `9eaed64`, in that order):**

- ✅ **DV-J1 DISCHARGED, NOT BUILT (`7c95f9c`)** — the queued scope was already closed by **DV-J2 (#27)** and **`s182-D2`**; what was actually left was the **showroom serving deleted markup FOUR RULINGS STALE**. `gen_showroom` regenerated **5 pages**, gates green. Dave ruled the disposal in his own words — *"your recommendation is good : call it landed, with a receipt naming both halves"* — so the row is **LANDED with a two-halves receipt**, not quietly closed.
- ⚠ **THE FINDING: THE COMMIT HARNESS HAS BEEN BLIND SINCE #188 (`7c95f9c`)** — the doc-row gate went into `_git_commit.sh` unstubbed, so **every commit-path arm in `_test_git_commit.py` was crashing and the crash was being read as a result**. Healed; **26 arms green**, including **4 new declare-dirt arms**. ★ A harness that cannot fail is an assertion [[a-crash-is-not-a-fail]].
- ✅ **THE 119-SWEEP BOOT CONSUMER WIRED (`7c95f9c`)** — `_checkin.py` now reads the sidecar and was **driven through all four states**: FRESH · EXPIRED · UNKNOWN-AGE · NO-SIDECAR. Closes #187's ⑥(c) carry [[instrument-without-a-consumer]].
- ⬛ **`s191-D1` RULED AND ENACTED (`165fe11`)** — the **showroom sync gate is BLOCKING at the commit seam**, with `SHOWROOM_ACK` as the declared hatch. **Driven both ways**: a planted stale page was REFUSED **with nothing staged**.
- ⬛ **`s191-D2` RULED — HOME-OR-DECLARE (`8a89b75`)** — `render.py` is **HOMED in-repo** at `knowledge/_render/render.py` and the runbook **copies, never retypes**; the **NON-REPO adjacent marker** is taught to `knowledge/_gardener.py` (mutation arm **g13**, bites both ways). Real-store refresh: **both STALE hooks flipped FRESH honestly** — store **FRESH 96 · AGING 4 · STALE 0 · UNPROVABLE 27**. The DV-J1 row set landed with the two-halves receipt; lanes regenerated. ★ This **consumes the third of the four `W-31` builder choices** — it was a RULE, not a patch, exactly as #189 said.
- ⬛ **`s191-D3` RULED — THE VAR-GATE IS A GATE (`9eaed64`)** — ADVISORY → BLOCKING in **both** `_build_all.py` tables, the `#166` labels moved **together, as join keys**, `check_routes` selftest green at **119**. The same commit **annotates the DV-J2b record clash OVERTAKEN** in `GOOD-MORNING.md` and `knowledge/_state.json`, naming **`s182-D2` as the operative closure** — **added, never trimmed**; two closure stories are reconciled by annotation, not by erasure [[feedback-header-wins-over-audit]]. ⚠ **DECLARED: one hash typo inside the inscribed ruling was repaired TEXTUALLY, pre-commit.**
- ⚙ **GAUGE.** boot **56,496 real** (in band) · FILL at wrap-open **167,166** — **PAST the 150,929 ADVISORY by 16,237, DECLARED**, with legal room to the **200,000** wall (`s190-D2`: the advisory is a wrap-open line, the wall BINDS) · **subs 226,216 tokens (n=2, MEASURED)** — DV-J1 107,228 + residuals 118,988; this wrap sub's own spend is EXCLUDED and unknowable from inside. Effort band **M**. ⚙ **QUOTA PANEL, RELAYED ONLY:** All **29%** · Fable **36%**, both resetting Thu 11PM — Fable was the hot budget, which is why the work ran as two Opus build subs and the wrap is delegated. ⛔ **The crank decision is DAVE'S and was not taken.**
- ⛔ **NOT RULED / NOT TOUCHED:** the var-gate's **glob width and ds-number** · the three remaining `W-31` builder choices (all-must-resolve · the 185 surface · `grading_unit`) · the sidecar schema bump for `rechecked_at_session` · `STALE_AFTER_SESSIONS = 15` · `BASELINE_DATE` · `CARRY_GATE_BLOCKING` · the trend card (**FLOATED — never re-put as an option**) · the `#174` adjudication · every colour value · all `G`-items · the 19 unconditioned legacy close conditions · quota crank decisions · `knowledge/_rulings.json` (**not written by this wrap — `s191-D1`/`D2`/`D3` were inscribed by the conductor**) · memory files (**step 3 ran at the CONDUCTOR's seat: the new `non-repo-home-or-declare.md` hook + its `MEMORY.md` index line; a wrap sub cannot reach the store**) · ⛔ **NOT PUSHED — Dave's word was not given.**

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

**101 decision nodes — 85 LIVE · 7 AMENDED · 8 DEAD · 1 OPEN.** Full typed edges + what-touches-this map: `knowledge/_DECISION-GRAPH.md`.

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

**✓ LIVE (85)** — in force; titles in `_DECISION-GRAPH.md` §②:
  ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0007, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0012-A1, ADR-0013, ADR-0014, ADR-0015-A1, ADR-0015-A2, ADR-0016, ADR-0017, B-D1, B-D2, B-D3, B-D4, B-D5, B-D6, B-D7, CHARTER.S9, DEF-003, DEF-005, DEF-006, DV-D01, DV-D02, DV-D03, DV-D04, DV-D05, DV-D06, DV-D07, DV-D08, DV-D09, DV-D10, DV-D11, DV-D12, DV-D13, DV-D14, DV-D15, DV-D16, DV-D17, DV-D18, DV-D19, DV-D20, R-D5, R-D6, R-D6.A, R-D6.A2, R-D6.B, R-D7, R-D9, R-D11, R-D12, R-D12.A, R-D12.B, R-D14, R-D15, R-D16, R-D17, R-D18, R-D19, R-D20, R-D21, R-D22, R-D23, R-D24, R-D25, T-D1, T-D2, T-D3, T-D4, T-D6, T-D8, T-D9, T-D10, T-D12, T-D13, T-D14, T-D15, TYPE:2026-07-18:sat-ceiling

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
✅ **P5 HALF CLOSED #186 — `s186-D2` (Dave): KEEP.** The `--all-dirty` hatch stands; the #128 question is answered. The (1) tracked-log half remains open, Dave's three ways.
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
- **The BOOT-RENT PLAN (P2)** and **the ATTRIBUTION RE-PROBE** — ⛔ **DAVE'S, twelfth roll at #125.** ✅ *BY ADDITION #178: the re-probe is DISCHARGED (`s178-D1`(b)) — its consumers were the boot re-bases (`s129-D1`, `s171-D1`) and the #112-D1 recorder, all delivered; the frozen roll-counter here was stale at write (record shows THIRTEENTH at #127, then the item left the list at #128 unclosed). The BOOT-RENT PLAN half of this line is untouched.*
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
