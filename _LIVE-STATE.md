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

*Last refreshed: 2026-09-09 (Wed from `date` — **#265 wrap**. ✅ **NO DATE SPLIT: the session, its ritual and its commits are all 2026-09-09** — the three standing WRAP DATE SPLIT notices belong to #241, #248 and #261 and nothing was re-dated here, because nothing needed to be. One evening, conductor **Fable**, **FOUR OPUS 5 LANES** (**B** the `s263-D10` bite arm · **C** three inherited reds · **D** the first real browser drive of `_PROPOSED-263.html` · **E** the fourth red, `_validate_kg.py`) plus **TWO blind OPUS drivers** for the `/goal` bite-test and this OPUS 5 wrap sub, DELEGATED wrap. ⛔ **DAVE WENT TO BED MID-SESSION — *"lets crack on we have lots of tokens to use, we have spare budget and Im going to bed soon"* — SO THIS SEAT RULED NOTHING AND EVERY OPEN QUESTION STAYS OPEN IN HIS NAME.** ★★★ **THE HEADLINE IS A NARROWING, NOT A PASS: `s262-D5`'s `/goal` CLAUSE BITES ON *HOLD* AND ON NOTHING ELSE.** `knowledge/_bite_goal.py` emits an INTACT `apollo-spider/cold-start/COPILOT-BOOT.md` and a MUTATED copy with option 3's five-line `/goal` span stripped (the strip is ASSERTED, not assumed), plus a 4-turn scenario; two Opus lanes, blind to each other and to the repo, each played the assistant from ONE boot. Grades: **INTACT GREEN 2/2 · MUTATED RED 1/2**, and the single discriminating arm is **G2 — holding the goal against a drift**: with the clause, T2's *"just build me a transactions list"* was checked against *make rent* **by name** and re-shaped into two priced options; without it the list was simply built and the drift was absorbed, never named. ⛔ **G1 — confirm before build — passed in BOTH arms and is therefore NOT this clause's**: it belongs to rule 7a's bento question, and deleting the `/goal` clause would not move it. ⛔ **G3 — report against the goal — is UN-REGEXABLE**: both T4s name the goal, and only a reader can tell *"Against the goal — the answer reads at a glance, not yet"* from *"Where we are: 1. Goal stated 2. Page built"*. ★★★ **TWO RULINGS, DAVE'S, INSCRIBED — `knowledge/_rulings.json` entries 440–441, the store 439 → 441, both parsing with `by` Dave · `date` 2026-09-09.** **`s265-D1`** ***"1. okay make it stand alone"*** — the bite-test is a **STANDALONE instrument, not a `test_gates.py` CASE**, run by a lane with a live driver at every change to `COPILOT-BOOT.md` option 3, its transcripts and grades filed as subreport assets; it does not join CASES while the sandbox has no scriptable driver (`claude -p` → `terminal_reason: api_error`), because **a case that cannot run in one environment is refused as a gate** [[gate-cannot-pass-in-one-environment]]. **`s265-D2`** ***"2. okay yes"*** — G3 is graded **RUBRIC-ONLY**, a reader grades T4, and the regex arm is **ADVISORY and never counted**. ★★★ **AND THE OTHER HALF OF THE DAY WAS FOUR OPUS LANES PAYING DOWN INHERITED RED, ALL OF IT WORK NO ONE HAD TO RULE.** ✅ **Lane B** gave `s263-D10`'s `rulings_page_freshness_check` the **registered bite arm it was born without** — `selftest_rulings_freshness()` wired into `_selftest_body()`, plus `case_capture_gate_rulings_arm()` in `knowledge/_tests/test_gates.py`; four bites, and **the CLAUSE is what is graded**: three separate FAIL-OPEN edits (`if rc != 0:` → `if False:`, a blocking→advisory `fails`→`notes` demotion, an early return) each turned the arm RED while an unmutated control stayed GREEN in the same process, and the `_tests/` registration was driven both directions. ⛔ **A `CASES` row could not hold it and the reason is structural** — the check is a *function* inside `wrap_checks()` with no exit code, and it is REPO-scoped (`knowledge/_rulings.json` **and** `notes/_RULINGS.html`) while `fresh_copy` copies `knowledge/` alone; that is written into the code so the next reader does not retry it. **No copytree was taken: peak scratch under 3 MB** (`67b1879`). ✅ **Lane C** closed two of three inherited reds: **`_validate_icons.py` is GREEN** (5 UNKNOWN → 0 — Legend's five `<svg class="dv-svg">` **chart canvases were never icons**; they gained the byte-identical `data-bespoke=` reason the fourteen chart snippets already carry), and **`knowledge/components/footer.meta.json` is SCHEMA-VALID for the first time since #261** (`edges.composes` — **an invented edge type with no consumer anywhere** — → `edges.consumes` plus the `$consumes` source array the generator name-matches, and `provenance.source: "redesign"` → `"gap-report"`, *restored* from `git show 6e6271f`, not chosen). `_build_integrity.py` went **16 → 14** errors, schema **132/137 → 133/137**; ⛔ **the fourteen that stand are ONE family and none is mechanical** — four #261-era metas authored richer shapes than `meta.schema.json` permits, and every repair is a schema decision (`a88673e`). ✅ **Lane E** took the **fourth red lane C found standing beside the three**: `_validate_kg.py` **13 → 5**. Seven `pattern:`/`context:` nodes were registered with entries **copied BYTE-FOR-BYTE from a clean scratch regeneration's own output**, and Legend's hand-slugged `context:small-multiples` was repointed to `context:dashboard-rows-of-small-multiples` — the id the generator derives from that meta's own prose, because registering the short id would have meant **inventing a node the machinery does not know** (`087e058`). ⛔ **AND LANE E MEASURED THE REASON `gen_kg_edges.py` MUST NOT BE RE-RUN: a clean regeneration REWRITES EIGHT METAS AND DELETES AUTHORED CONTENT** — Filter-toolbar-bar's `composedOf`/`delegatesTo`/`drivesConsumer`/`$contract` blocks (the `s258-D1` contract, ~40 lines), Legend's `containedBy` and `governedBy` edges, the tail of Footer's `$note`; the diff is **441 lines** and is filed. `s245-D7` is the ruled mechanism that protects authored edges and its carry list is **one name**. ⇒ **the generator is FENCED until Dave rules the carry list.** ✅ **Lane D drove `notes/_PROPOSED-263.html` in a real browser for the FIRST time** — the page Dave ruled eleven defaults off at #263 had never been rendered. Chromium ran headless off `_RUNBOOK-render-verify.md`'s class fix, re-run from scratch because the VM had been rebuilt. **The interaction core is sound and OBSERVED, not construed:** the `localStorage` round-trip survives a reload with ruling AND note intact, `#tallyN` and `#sRuled` track together through 0 → 3 → 11 → clear, the export block's `NOT RULED` line is exact at 11/8/0, all 33 `button.rb` measure **44.0px** at both 760 and 375, there is no horizontal scroll, and **the console is completely silent across five contexts**. ⛔ **Two real defects fell out, both in the theme layer, and the page was NOT edited**: the sticky control bar's own targets are **34.2px** (`label.tog` 35.0, the `#decide` checkbox **13×13**) under the 44px floor the ruling rows hold, and the `[data-theme="dark"]` block at line 196 is a **DEAD ARM** — invisible on `<html>` (two byte-identical PNGs are the receipt) and, forced on `<body>`, it half-paints and leaves `accent` at `#DA1A00` on near-black, a **TWO-RED-LAW `s151-D1` violation the `prefers-color-scheme` path does not have** (`d3a2297`). ⚙ **GAUGE:** the conductor DECLARED **147,425 real FILL** at the brief cut — **32,575 UNDER** the `s260-D2` delegated stop line of 180,000, ⇒ **this wrap is delegated because DAVE IS ASLEEP and the conductor's seat stays for the read-back, not because the line was crossed**; first-hand at this seat his transcript reads **148,308 real over 47 turns**. ⛔ **BOOT 70,260 real, MEASURED at his opener — 260 OVER the 70,000 shrink-only literal, and it is RECORDED AS A BREACH**: eight consecutive under-ceiling readings end here, the literal is shrink-only by `s240-D2`/`s241-D1`, and the gate's refusal (still standing on #255's 70,127) is recorded in the #243 form rather than routed around, for a **nineteenth** wrap running. ✅ **A `subs` LINE IS WRITTEN THIS TIME AND IT IS MEASURED, NOT ESTIMATED** — five lanes' Agent `usage`: drivers 48,453 + 49,700 · B 117,210 · C 148,627 · D 80,597 · E 115,314; ⛔ **this wrap seat's own spend is UNREADABLE from inside itself and NO number is written for it** — an UNKNOWN is never turned into a number. ⛔ **AND ONE OPERATIONAL FINDING FOR THE RECORD: the "stale `.git/index.lock`" WAS NEVER STALE.** The Cowork sandbox was refusing **all unlinks** until `allow_cowork_file_delete` was granted mid-session; git's own lockfiles and `tmp_obj_*` survived every commit because nothing could remove them. Granted, cleared — and the diagnosis that had stood for two sessions was wrong about the cause. ⛔ **MEMORY (ritual step 3) WAS NOT WRITTEN AT THIS SEAT — A SEAT LIMIT, DECLARED NOT SKIPPED, FOR THE FIFTH CONSECUTIVE DELEGATED WRAP (#261 … #265)**; ⚠ for the second wrap running the brief announced it in front and **the conductor wrote the memory hook itself before delegating**. ⬛ **STILL HIS AND UNTOUCHED:** the **four ungraded `-active` glyphs** on `notes/_REVIEW-264-active-glyphs-2.html` · **`global-money`**, which needs drawing, not deriving · **THIRTEEN lane ruling-shaped questions** (B:2 · C:5 · D:3 · E:3), every one priced with a recommendation and none ruled · the two `_PROPOSED-263.html` defects · whether a **gate report should be refused at commit when its own tree ≠ HEAD** (#263, age 2) · **#241's midnight-wrap question, age 23** · and what ritual step 3 should say about a delegated seat, now with five datapoints. Gauge, declared skips (each with its size) and not-done: the ⏱ LATEST DELTA below. **`_CARRIES.md` § `## residual → #266` is the carry set (`s225-D2`); the banner carries the pointer and the probeable count.**)  Previous: 2026-09-09 (Wed from `date` — **#264 wrap**. ✅ **NO DATE SPLIT: the session, its ritual and its commits are all 2026-09-09** — the three standing WRAP DATE SPLIT notices belong to #241, #248 and #261 and nothing was re-dated here, because nothing needed to be. One evening, **19:26 → 20:30**, conductor **Fable**, **no subs but this OPUS 5 wrap sub**, DELEGATED wrap. ⛔ **THE SESSION OPENED ON TWO CARRIES AND BOTH WERE WRONG, WHICH IS THE DAY'S FIRST FINDING.** Dave's first sentence — *"I thought this was ruled"* — is correct: **`s263-D1`'s `governs` names `knowledge/snippets/Stat-card.reference.html`** and the P-01 recommendation he ACCEPTed says verbatim **"Stat card moves with it, always"**, so the Stat card arrow seat was settled at #263 and **no ruling is owed**; the carry is STRUCK with that receipt. And the sidebar `chart` glyph was **never hand-baked** — all **twelve** `<symbol>`s in `Sidebar-nav.reference.html` are byte-identical to `knowledge/assets/icons/` files by path data; the defect was **PAIRING** (Spending rested on `data-chart` and went current on `insight-active`, a bulb; Transfers rested on `balance-transfer`, which has no `-active` twin in the library at all, and went current on `transfer-active`). ★★★ **THREE RULINGS, DAVE'S, INSCRIBED — `knowledge/_rulings.json` entries 437–439, the store 436 → 439, each parsing with `by` Dave · `date` 2026-09-09.** `s264-D1` ***"Spending A"*** → `data-chart`/`data-chart-active` · `s264-D2` ***"Transfer D"*** → `transfer`/`transfer-active`, scope Sidebar-nav only (`9bfacb9`) · `s264-D3` ***"Good try btw, maybe shelve the rejected ones for further work. keep teh others, good experiment we can return to it later."*** — the derived-glyph experiment is kept and **eight twins enter the library**, five are rejected with his thirteen grades verbatim in the ruling (`c7247c2`). ✅ **THE PAIRING DEFECT WAS GENERALISED INTO A GATE ARM RATHER THAN FIXED TWICE** — Dave: *"1. okay fix them 2. do it"*. `knowledge/_validate_icons.py` now resolves every `.ic-line`/`.ic-fill` pair to library slugs and **MIS-TWINNED is BLOCKING** (a line glyph with no twin is reported, not failed); bite-test **`twin`** (`mut_mistwinned_icon`) is registered in `knowledge/_tests/test_gates.py` and was driven **RED → GREEN in-process** on one 93 MB copy; it found a **THIRD** case immediately — Tab-bar's Insights row carried `insight` in **both** slots, now `insight-active` (`s262-D3`) — and four App-shell/Command-palette snippets moved `balance-transfer` → `transfer` at rest (`3d7def7`). ★★★ **EIGHT `-active` GLYPHS WERE DERIVED FROM THEIR LINE GLYPHS BY SKIA PATH OPS AND ARE IN THE LIBRARY:** cheque, finances, document-report, newspaper, device-mobile, online-banking, presentation, add-circle — written as `<slug>-active.svg` with a **`$derived`** annotation in `icons.manifest.json` (`$total` **658 → 666**; the icon gate's glyph count **750 → 758**, its 5 UNKNOWN Legend icons pre-existing and untouched). ⚠ **The method was calibrated against TEN human-drawn pairs before it was shown to him** — 7 within tolerance, and the three misses (card, alert, insight) are designer edits no rule recovers (`3722f26`, `c7247c2`). ★★★ **THE SECOND PASS FOUND THE CLASS, AND THEN THE ONE GLYPH THE CLASS DOES NOT CONTAIN** — Dave: *"have another go"*. His five rejections are ONE class (two bodies with an overlap exclusion), and rebuilding the silhouette as the holes of the exterior of the line ink unioned with a grown front silhouette makes **balance-transfer, tax, workspace and digital-statements fill**; ⛔ **`global-money` is ONE CONNECTED INK PIECE** — the arrows touch the meridians, so there is no second body to find and it is a **drawing** problem, not a derivation one (`5e97c90`). Dave, closing: ***"no time for this now, but we can return to it another time because we are getting somewhere"*** ⇒ the four stay **UNGRADED** on `notes/_REVIEW-264-active-glyphs-2.html`, nothing further entered the library, and that sentence was appended to `s264-D3`'s `evidence` rather than left in chat. ⚙ **GAUGE:** the conductor DECLARED **214,299 real FILL** at the brief cut (96 turns) — **34,299 OVER** the `s260-D2` delegated stop line of 180,000 and over the 200,000 working ceiling, which is why this wrap is delegated; first-hand at this seat his transcript reads **221,197 real over 101 turns**, minutes apart, both standing. ✅ **Boot 69,955 real, MEASURED at his opener — no hole this session** — 45 UNDER the 70,000 shrink-only literal, an eighth consecutive under-ceiling reading, ⛔ **and the arm still refuses on #255's standing 70,127**, so the commit is made in the #243 form for an eighteenth wrap running. Throughput **612,089** (conductor) / **624,066** (this seat), cl100k-estimate. ⛔ **NO `subs` LINE IS WRITTEN** — the only sub was this wrap seat, whose own spend is not readable from inside itself, and an UNKNOWN is never turned into a number. ⛔ **MEMORY (ritual step 3) WAS NOT WRITTEN AT THIS SEAT — A SEAT LIMIT, DECLARED NOT SKIPPED, FOR THE FOURTH CONSECUTIVE DELEGATED WRAP (#261, #262, #263, #264)**; ⚠ the difference this time is that the brief declared it off-limits and **the conductor wrote the memory hook itself before delegating**. ⬛ **STILL HIS AND UNTOUCHED:** the **`/goal` bite-test**, ruled *"do it"* at this session's opener and **NOT STARTED** · the **four ungraded** derived twins and whether **`global-money`** gets drawn · whether a **gate report should be refused at commit when its own tree ≠ HEAD** (#263, age 1) · **#241's midnight-wrap question, age 22** · what to do about ritual step 3 at a delegated seat · and **three pre-existing reds on a pristine repo** (footer's two schema reds · `_validate_icons.py`'s 5 UNKNOWN Legend icons · `_build_integrity.py`), none caused here and none repaired here. Gauge, declared skips (each with its size) and not-done: the ⏱ LATEST DELTA below. **`_CARRIES.md` § `## residual → #265` is the carry set (`s225-D2`); the banner carries the pointer and the probeable count.**)  Previous: 2026-09-09 (Wed from `date` — **#263 wrap**. ✅ **NO DATE SPLIT: the session, its ritual and its commits are all 2026-09-09** — the three standing WRAP DATE SPLIT notices belong to #241, #248 and #261 and nothing was re-dated here, because nothing needed to be. Conductor **Fable** (declared in the wrap brief) + **THREE OPUS 5 SUBS** (**P** the review page for the eleven proposed defaults, **E** the D7/D10 enactment, **A** the D11 enactment) with **lane C run at the conductor's own seat** (the chart-engine re-drive), plus this OPUS 5 wrap sub, DELEGATED wrap. ⛔ **THE CONDUCTOR'S FILL WAS NOT MEASURED AT THE WRAP CUT** — the brief declares an **ESTIMATE ~65–75K real** and marks it as one, because no `message.usage` was read at that seat; ⚠ **an estimate is not converted into a measurement here.** **THROUGHPUT at the wrap seam: 167,102 cl100k-estimate declared by the conductor, 171,698 measured first-hand at this seat**, and ⛔ `_checkin.py`'s BUDGET line here reads **FILL 155,332 real over 74 turns, boot 69,687**, which disagrees with his own estimate by roughly 2× and is **recorded rather than reconciled** — this seat cannot prove from inside itself which window that transcript belongs to. ★★★ **THIRTEEN RULINGS, DAVE'S, INSCRIBED — `knowledge/_rulings.json` entries 424–436, the store 423 → 436, each parsing with `by` Dave · `date` 2026-09-09 · `status` ruled.** `s263-D1` … `s263-D11` rule the **eleven PROPOSED defaults** that the #261 conductor had defaulted and #262 had left standing — **eight straight ACCEPTs**, and the three that came back `LATER` ruled on his own sentences: `s263-D7` the doormat is a **"dormant variant"** of Footer (which also discharges `s261-D3`'s *"for now"* hedge) · `s263-D8` the chart legend **stays 44px** (*"Is this teh legend for charts? if so leave it at 44 it works fine"* → *"accept"* once confirmed) · `s263-D9` `data-dv-controls` **contract-only** (*"an interesting idea to wire one legend to multiple charts but not required at this stage"*). Then `s263-D12` *"whatever is the best standard solution"* — `variants[].status` becomes a first-class enum `active|dormant|deprecated` — and `s263-D13` **"yes"**. ★★★ **THE DAY: A DEFAULTED LIST GOT A SURFACE AND THE SURFACE GOT ELEVEN ANSWERS IN ONE PASS** — `notes/_PROPOSED-263.html` (lane P) carries each recommendation verbatim beside what the code actually does, an Accept/Reject/Later row and an export block whose `NOT RULED (n):` line is what let the wrap see what was still open; ⛔ **the lane ruled nothing itself, and the page was never driven in a browser and never published** (hosted publish refused). ⛔ **AND ONE OF THE ELEVEN RULINGS EXPOSED A GATE THAT WAS GRADING NOTHING:** `s263-D11` retired `_validate_snippets.py`'s source-text `requiredAria` arm in favour of the DOM-driven arm in `_validate_dataviz.py`, and that arm was reading **STALE on all 27 pages** because `knowledge/canon/type.css` moved at `4cc4204` (#261 F2) after the receipts were driven at `0420197`. ★ **`knowledge/_DATAVIZ-GATE.md`, committed at `81ce08f`, reads PASS / 0 STALE from a tree that did not match HEAD** — the #253 pattern in a new venue, ruling-shaped and HIS. ✅ **THE RE-DRIVE IS A MEASUREMENT:** Chromium 151 installed without root, **27 pages × 8 combos** re-driven at `521a751`, **0 differing measured fields** ⇒ **v1.0.9's charts are retroactively clean** and the dataviz gate is GREEN. ✅ **THE TENTH RELEASE GATE (`s263-D13`, `5050b33`):** `--release` now runs a **write-nothing `--receipts-fresh`** check after `require_clean` and REFUSES over stale driven receipts — selftest drives the mutant RED and the control GREEN, and the frozen/audit/CI gates still PASS. ✅ **`s263-D10` IS LIVE AND RAN FOR THE FIRST TIME AT THIS WRAP** — `rulings_page_freshness_check()` is BLOCKING inside `wrap_checks()`, calling the renderer's own `check()` in-process, and runbook **step 4d** is new; ⛔ **it has NO registered bite-test arm**, declared at birth. ⛔ **MEMORY (ritual step 3) WAS NOT WRITTEN AT THIS SEAT AND THE REASON IS A SEAT LIMIT, NOT A SKIP** — the store's path is outside both directories this wrap sub's file tools accept and invisible to the shell; the conductor writes memory itself. ⛔ **THIS IS THE THIRD CONSECUTIVE DELEGATED WRAP AT WHICH THAT HAS HAPPENED (#261, #262, #263), WHICH IS A PATTERN RATHER THAN AN INCIDENT**, and what to do about it is Dave's. ⬛ **STILL HIS AND UNTOUCHED:** the Stat card arrow seat (⚠ `s263-D1`'s `governs` names `Stat-card.reference.html` and the conductor reads it as settled — ⛔ **Dave has not said so**) · `/goal` untested · the sidebar `chart` glyph · #241's midnight-wrap question at age 21 · and **three pre-existing reds on a pristine repo** (footer's two schema reds · `_validate_icons.py`'s 5 UNKNOWN Legend icons · `_build_integrity.py`'s 17 errors / 25 warnings), none caused here and none repaired here. Gauge, declared skips (each with its size) and not-done: the ⏱ LATEST DELTA below. **`_CARRIES.md` § `## residual → #264` is the carry set (`s225-D2`); the banner carries the pointer and the probeable count.**)  *Last refreshed (#262, trimmed at the #265 wrap): #262's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #265, in the same section as its ⏱ delta block. Nothing was deleted — moved.*  *Last refreshed (#261, trimmed at the #264 wrap): #261's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #264, in the same section as its ⏱ delta block. Nothing was deleted — moved.*  *Last refreshed (#260, trimmed at the #263 wrap): #260's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #263, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#259, trimmed at the #262 wrap): #259's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #262, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#258, trimmed at the #261 wrap): #258's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #261, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#257, trimmed at the #260 wrap): #257's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-08 #260, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#256, trimmed at the #259 wrap): #256's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-08 #259, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#255, trimmed at the #258 wrap): #255's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-08 #258, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#254, trimmed at the #257 wrap): #254's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-08 #257, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#253, trimmed at the #256 wrap): #253's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-08 #256, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#252, trimmed at the #255 wrap): #252's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-07 #255, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#251, trimmed at the #254 wrap): #251's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-07 #254, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#250, trimmed at the #253 wrap): #250's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-07 #253, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#249, trimmed at the #252 wrap): #249's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-07 #252, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#248, trimmed at the #251 wrap): #248's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-06 #251, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#247, trimmed at the #250 wrap): #247's `Previous:` chain segment — carried inside the dream-pass-11 wrapper line — was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-06 #250, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#246, trimmed at the #249 wrap): #246's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-06 #249, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#245, trimmed at the #248 wrap): #245's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-05 #248, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#244, trimmed at the #247 wrap): #244's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-05 #247, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#243, trimmed at the #246 wrap): #243's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-05 #246, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#242, trimmed at the #245 wrap): #242's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-03 #245, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#241, trimmed at the #244 wrap): #241's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-03 #244, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#240, trimmed at the #243 wrap): #240's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-03 #243, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#239, trimmed at the #242 wrap): #239's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-03 #242, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#238, trimmed at the #241 wrap): #238's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #241, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#237, trimmed at the #240 wrap): #237's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #240, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#236, trimmed at the #239 wrap): #236's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #239, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#235, trimmed at the #238 wrap): #235's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #238, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#234, trimmed at the #237 wrap): #234's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #237, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#233, trimmed at the #236 wrap): #233's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #236, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#232, trimmed at the #235 wrap): #232's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #235, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#231, trimmed at the #234 wrap): #231's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-02 #234, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#230, trimmed at the #233 wrap): #230's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-01 #233, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#229, trimmed at the #232 wrap): #229's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-01 #232, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#228, trimmed at the #231 wrap): #228's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-01 #231, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#227, trimmed at the #230 wrap): #227's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-31 #230, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#226, trimmed at the #229 wrap): #226's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-31 #229, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#225, trimmed at the #228 wrap): #225's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-31 #228, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#224, trimmed at the #227 wrap): #224's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-31 #227, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#223, trimmed at the #226 wrap): #223's `Previous:` chain segment was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-30 #226, in the same section as its ⏱ delta block. Nothing was deleted — moved.* *Last refreshed (#221 and earlier — 2d boundary, trimmed at the #225 wrap): #222's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-30 #225; #221's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-29 #224; #220's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-28 #223; #219's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-28 #222; #218's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-28 #221; #217's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-27 #220; #216's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-26 #219; #215's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-24 #218; #214's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-24 #217; #213's full summary moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-08-22 #216; #212's was moved at the #215 wrap to § Rolled 2026-08-22 #215; #211 at the #214 wrap to § Rolled 2026-08-21 #214; #210 and earlier at the #213 wrap to § Rolled 2026-08-21 #213, which carries the #210 → #184 chain and, inside it, the pre-existing pointer to § Rolled 2026-08-16 #186 … § Rolled 2026-08-11 #156 for #182 and earlier. Nothing was deleted — moved.*
*(⚠ **MOVED INTO THE HEADER ZONE, #35.** The wrap gate's `"Last refreshed" is not today` check reads only the first 40 lines — where this line did not live. It had been passing on dates inside the LANES section, so on #34 it could not have failed even with a stale stamp. Moved so the check tests what it is named after.)*

*(⚠ **WRAP DATE SPLIT — THE SESSION RAN 2026-09-02, THE COMMIT LANDED 2026-09-03, AND BOTH DATES STAND.** #241's capture ritual was authored on 2026-09-02 and steps 1→4c completed that night; the commit did **not** land, and this wrap sub finished step 5 the following morning. ⛔ **Nothing was re-dated:** the `Last refreshed` stamp above, every `## Batch 2026-09-02 #241` / `§ Rolled 2026-09-02 #241` archive key, the 1b dossier and the filed sub-report filenames all carry the SESSION's date, because moving them to match the commit would be exactly the T-D12 false inscription this file's own header block warns about, running the other way. This line carries the COMMIT date so the wrap gate's `"Last refreshed" is not today` check grades a **true statement** rather than a back-dated one — the check exists to catch an unrefreshed handoff, and this handoff was refreshed. ⬛ **RULING-SHAPED, DAVE'S: what a wrap that spans midnight should stamp.** Provenance: 241 · 2026-09-03 · status: observed.)*

*(⚠ **WRAP DATE SPLIT, SECOND OCCURRENCE — THE SESSION RAN 2026-09-05, THE RITUAL AND ITS COMMIT RAN 2026-09-06, AND BOTH DATES STAND.** #248's conductor cut the wrap brief at 183,983 real FILL on the evening of 2026-09-05 and the delegated wrap sub ran every step the next morning. ⛔ **Nothing was re-dated:** the ★ LATEST banner heading, the ⏱ delta heading, every `## Batch 2026-09-05 #248` / `§ Rolled 2026-09-05 #248` archive key, the `#### 2026-09-05 #248` stratum, the 1b dossier and the filed sub-report filenames all carry the SESSION's date (`_DECISION-HISTORY/2026-09-05-248-…`; the wrap report alone is `notes/_subreports/2026-09-06-248-wrap.md` because it was WRITTEN on the 6th). The `Last refreshed` stamp above carries the COMMIT date so the wrap gate's `"Last refreshed" is not today` check grades a **true statement**, exactly as #241's did. ⬛ **#241's RULING-SHAPED question — what a wrap that spans midnight should stamp — is STILL DAVE'S, age 7, and this is its second instance; the #241 paragraph above stands verbatim, by ADDITION.** Provenance: 248 · 2026-09-06 · status: observed.)*

*(⛔ **`_seam_block.sh` — THE CURRENT COPY IS LANE P'S:** `notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt/_seam_block.sh`. The copies filed under `notes/_subreports/assets/2026-09-02-239-F-polarity-fix/` and `.../2026-09-02-238-V-polarity-verifier/` are **pre-fix #238 blocks — DATED HISTORY (ADR-0017 / `s192-D1`), NOT to be edited and NOT to be reached for**. V2 confirmed the staleness at #242. Pointer written #244; carry ⑤.)*

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
- ▶ §C·1 strands (a)–(d) — chart expansion · wave 3 · templates/shells · enact window — active · receipt ACTIVATED #244 (2026-09-03) — the queue line read `queued` while waves 3–6 had all LANDED (#209 · #210 · #218), which is what made #242's opener recommend "charts wave 3" again: the assertion-propagation class, fourth recurrence, carried as ⑥ from #242/#243 and NOT fixable by a wrap sub. WORK IN FLIGHT AT #244: lane A — the nav/menu family, §C·1 chart-expansion wave 3; lane B — the radius tuner. Receipts land in notes/_subreports/2026-09-03-244-lane-A-*.md and -lane-B-*.md. ⚠ ACTIVE means in flight, not shipped — the step lands only when its strands (a)–(d) carry their own receipts. Records carry STATE; the WHY stays in notes/_MEMENTO-DECISIONS.md.
- ⏹ until: born blocked, UNBLOCKED #25 (lane 1 landed) — lands when DV-J1/DV-J2 + the §C·1 strands ship (keys minted #26, Dave: J = Job; was ex-M4a/ex-M4b) · receipts: knowledge/_proforma/_DATAVIZ-DECISIONS.md § Open/pending · GOOD-MORNING.md §C·1(a)–(d)

**ACTIVE — `lane-3-bento` · Bento + library (photography · logos · Foundations)** *(born #218 · 2026-08-24 — MINTED AT THE OPENER on Dave's word ('the bento lane still needs work'); the work has been live since #211 (photography arrival, W-93) through the #216/#217 builds, and #216/#217 both named the register's silence)*
- ✅ #216/#217 builds — photography ruled HYBRID + manifest/derivatives (s217-D1), bento minted to canon with roles + squaring pass (s217-D2/D3/D7), Foundations tier filled, matrix explorer — landed · receipt knowledge/_rulings.json § s217-D1…s217-D8 · knowledge/_state.json W-108…W-126 · notes/_briefs/2026-08-23-217-bento-research-v1.md
- ▶ Dave's sitting over the bento decision surface — W-119 canon demo · W-124 roles + keyline trial · W-125 gallery span-vs-justified · W-126 matrix explorer + s217-D5 P1–P5 — active
- ⏳ enact wave for the sitting's rulings (scoped after the sitting, not before) — queued
- ⏳ photography KG mapping — W-109, node identity first (Dave's) — queued
- ⏹ until: lands when the bento decision surface is ruled (W-119 · W-124 · W-125 · W-126 + the five s217-D5 open points) and the resulting rulings are enacted; the photography KG mapping (W-109) lands or is parked · receipts: knowledge/_REVIEW-SIGNOFF.md · knowledge/_rulings.json · knowledge/_DS-IMPROVEMENTS.md ds-044…ds-058

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
**Status (2026-08-23, dream pass 9): SCHEDULED Sun 07:10 fire, ON TIME (pass 8 = 08-16). 6 proposals FLOATED, 0 ruled (Dave absent — a scheduled run cannot rule): P1 pre-flight `⛔ NOT CAPTURED` 27 consecutive sessions while the s214-D5 hand-over field measures the conductor's window four lines below · P2 s188-D1 grading-unit split (3 hooks' live claim only in the index line the grader no longer reads) · P3 s183-D1's AGING-deferral premise falsified cycle one (AGING 1→16) · P4 B3 cost-half return date fell TODAY, 139 alert rows / 14,835 tokens vs 0 decision rows · P5 `git-push-method.md` description publishes the retired Desktop-only rule 39 days on · P6 **s217-D1 exists ONLY in the uncommitted tree**. Output `notes/_dream/2026-08-23-proposals.md` — ⛔ **UNCOMMITTED, HELD DELIBERATELY**: the commit gate demands a regenerated `_CHAIN.md`, but `_CHAIN.md` is dirty with #217's unwrapped edits and staging it would sweep/overwrite in-flight work (mechanical rule: never sweep; P6's own warning). Commit owed once #217 wraps. Dreamer = Opus pinned, conductor = Fable (scheduled session's model); spot-checks 5 exact + 2 chased-and-named (dreamer's "all 21 untracked are 217-named" is false literally — 14 are photography/logos paths — true in substance; its "_MEMORY-GRADES.json already dirty at baseline" was wrong, the refresh made it 37 M). 7 checked-clear (ff1–ff7). ⚠ Pass 8 (08-16) never wrote its step-7b row here — this is the first §🔀 row since pass 7. ⚠ Baseline dirt = #217's unwrapped photography/logos session, LEFT AND FLAGGED. Boot 53,477 real — BELOW the s208-D1 band by 2,118, declared.**
**Status (2026-08-15, dream pass 7): SCHEDULED fire, ⚠ a day EARLY (Sat 08:13 vs the ruled Sun 07:10 — declared, not reconciled). Not overdue (pass 6 = 08-09). 4 proposals FLOATED, 0 ruled (Dave absent — a scheduled run cannot rule): P1 STANDING-CARRY line `GOOD-MORNING.md:438` untouched 56 sessions with split ordinals ("SEVENTH" vs "twelfth") · P2 the ~26K GM-boot overspend went measured→measured→UNMEASURABLE at #176 (no boot-read declaration required anywhere) · P3 three memory files publish boot figures outside the ruled `s171-D1` band on the retrieval surface (one description says 75,899 vs constant 56,158 ±849) · P4 enacting a ruling breaks its predecessor's provenance anchor by construction (2 of 157 today, one per re-base forever). Output `notes/_dream/2026-08-15-proposals.md`, commit `69fba90`. Dreamer = Opus pinned, conductor = Fable; spot-checks 4/4 held (one `git log -L` "exactly one commit" imprecision chased — the trace lists 3, the latest touch e3174d1 #120 is the substance, benign). 7 checked-clear (dd1–dd7) incl. pass-6 P1 re-measured (still exactly 21 sweep strings, store now 157). ⚠ The 2026-08-09 pass's P1–P5 are STILL FLOATED awaiting Dave — now nine proposals on the table across two files. ⚠ `notes/_REHEARSAL-LOG.jsonl` was dirty at commit time (the gate-run append, pass-6 P2's class) — left out of the lane commit and flagged per the mechanical rule. Commit carries `after #176` — the lane-numbering seam from pass 6 remains unruled.
**Status (2026-09-06, dream pass 11): SCHEDULED Sun 07:10 fire, ON TIME (pass 10 = 08-30 ran on time but ⚠ never wrote its §🔀 row here — this is the first row since pass 9). 4 proposals FLOATED, 0 ruled (Dave absent — a scheduled run cannot rule; all four await his eye).** Dreamer = Opus pinned (dispatched as general-purpose/opus — the `dreamer` agent type is not registered in the scheduled harness, spec read+followed by prompt), conductor = Fable (scheduled session's own model), spot-checks **4/4 held** (grades sidecar `hooks_seen` 33 / 23·3·3·4 re-read · index one-link 33 + overflow 107, two-link 5 + 13 re-grepped · `provenance unknown` re-counted 11 hits — the dreamer's "7 files" is **6** (`_LIVE-STATE` ×2 · `_CHAIN` · `GOOD-MORNING` · `_CARRIES` · #247 wrap brief · `_memento-index.json` ×5), plus 13 in git-ignored `knowledge/_tmp/wrap247/`, benign · `_screen-gate/` 10 files vs `_SCREEN-GATE.md` "9 subject(s)" re-run). Output `notes/_dream/2026-09-06-proposals.md`, commit `2319d2a` — **P1** (#242's index diet cut the B3 grader population 122→33 undeclared; 107 hooks in the overflow file ungraded, 5 of them starred) · **P2** (the index parser grades one hook per line and silently drops a second link — 5 live, 13 latent) · **P3** (a delegated wrap sub's own blind spot, "`_tools/` … provenance unknown", inscribed 11× incl. the retrieval index while `_tools/Caffeinate/main.swift:1–2` carries the build command #246 gave Dave) · **P4** (`_SCREEN-GATE.md` says 9 subjects, directory holds 10, missing = `dashboard.md`, the current focus; thin as a count, floated for the mechanism). 6 checked-clear (hh1–hh6; hh4 records a near-false finding about DP `[18]`, hh6 that `_CARRIES.md`/`_REVIEW-SIGNOFF.md` were unreadable to a Bash-less seat). B3 refresh ran: 33 graded, FRESH 23 · AGING 3 · STALE 3 · UNPROVABLE 4, 5 grade changes; the 3 STALE hooks all name `knowledge/_measure_tokenizer.py`, deleted at `7f8801f` (#241). One `--grade-decision` row logged (changed=yes). ⚠ Baseline dirt = #248's UNWRAPPED W2-rhythm session (5 modified incl. `_rulings.json` +65 with `s248-D1…D4`, 11 untracked) — LEFT AND FLAGGED, not swept; showroom gate passed with `SHOWROOM_ACK` naming #248's uncommitted bento edit as the cause. ⚠ `origin/master` 4dc12b6 vs HEAD now 3 ahead (deb172a, 04099a8, 2319d2a) — Dave pushes. ⚠ `_checkin.py` refused first: tiktoken absent in the scheduled sandbox (installed in-session). Boot 57,157 real.


## ⏱ LATEST DELTA — 2026-09-09 (Wed from `date`) (**#265**, one evening, conductor **Fable** + **4 OPUS 5 LANES** (B, C, D, E) + **2 blind OPUS drivers** + this OPUS 5 wrap sub — ★★★ **THE `/goal` CLAUSE BITES ON HOLD AND ON NOTHING ELSE, AND FOUR LANES PAID DOWN INHERITED RED**)

*(WHY/HOW: `_DECISION-HISTORY/2026-09-09-265-goal-bite.md` — why a mutation test that goes RED is a NARROWING rather than a pass, how three of four inherited reds were repairable from the repo's own history without a single authored word, and why the KG generator is now fenced by a measurement rather than by caution. Filed reports: `notes/_subreports/2026-09-09-265-G-goal-bite-test.md` · `notes/_subreports/2026-09-09-265-B-d10-bite-arm.md` · `notes/_subreports/2026-09-09-265-C-three-reds.md` · `notes/_subreports/2026-09-09-265-D-drive-proposed-263.md` · `notes/_subreports/2026-09-09-265-E-kg-red.md` · `notes/_subreports/2026-09-09-265-W-wrap.md`.)*

- ✅ **NO DATE SPLIT — THE SESSION, ITS RITUAL AND ITS COMMITS ARE ALL 2026-09-09**, confirmed from `date` at this seat. The three standing WRAP DATE SPLIT notices belong to #241, #248 and #261; nothing was re-dated here because nothing needed to be. #241's ruling-shaped question — what a midnight-spanning wrap should stamp — is **still Dave's, now at age 23**.
- ⛔ **DAVE RULED TWICE AND THEN WENT TO BED, AND THAT IS WHY THIS WRAP IS DELEGATED.** His words: *"lets crack on we have lots of tokens to use, we have spare budget and Im going to bed soon"*. The conductor's FILL at the brief cut was **147,425 real — 32,575 UNDER the `s260-D2` delegated stop line 180,000** ⇒ **the line was not crossed; the seat is held open for his read-back.** ⛔ **This seat RULED NOTHING, graded no glyph, and left thirteen lane ruling-shaped questions open in his name.**
- ★★★ **THE `/goal` BITE-TEST IS A NARROWING, NOT A PASS — AND THE NARROWING IS THE FINDING.** `knowledge/_bite_goal.py` (`--emit DIR [--mutate]` / `--grade transcript.json`) cuts option 3's five-line `/goal` span out of `apollo-spider/cold-start/COPILOT-BOOT.md` **with an assertion that it is gone**, and two Opus lanes — blind to each other and to the repo — each played the assistant from ONE boot through a 4-turn scenario. **INTACT GREEN 2/2 · MUTATED RED 1/2.** ⇒ **the clause is load-bearing on exactly one arm: G2, holding the goal against a drift.** Intact T2: *"One check against the goal, then I'll do as you say … It does not answer 'will I make rent this month' at a glance"* → two priced options. Mutated T2: *"The shape I'd build: the answer on top, the list under it … Say go and I'll build it."* — the drift absorbed, never named as one. ⛔ **G1 (confirm before build) passed in BOTH arms** — both T1s end *"Dashboard bento — is that right?"*, which is **rule 7a's**, not `s262-D5`'s; it stays counted because the ruling says so, but **it does not discriminate**. ⛔ **G3 (report against the goal) is UN-REGEXABLE and the transcripts show why**: intact T4 opens *"Against the goal — … The answer reads at a glance — not yet"* (met / not-met), mutated T4 opens *"Where we are: 1. Goal stated 2. Page built …"* (a done-list that happens to name the goal). A reader tells them apart in one glance; `GOAL_TERMS` cannot. ★ **[[no-gate-parses-the-artefact]] holds even for a transcript — halfway.**
- ★★★ **TWO RULINGS, DAVE'S, INSCRIBED — `knowledge/_rulings.json` entries 440–441, the store 439 → 441, both parsing with `by` Dave · `date` 2026-09-09 · `status` ruled.** **`s265-D1`** — ***"1. okay make it stand alone"***: the bite-test is a **STANDALONE instrument**, run by a lane with a live driver at every change to `COPILOT-BOOT.md` option 3, transcripts and grades filed as subreport assets; **it does not join `test_gates.py`'s CASES** while the sandbox has no scriptable driver (`claude -p` → `terminal_reason: api_error`, one probe, not diagnosed), because a case that cannot run in one environment is refused as a gate. **`s265-D2`** — ***"2. okay yes"***: `s262-D5`'s third clause is graded **RUBRIC-ONLY**, a reader grades T4, and the G3 regex arm is **ADVISORY and never counted**, with the reason written into the source beside it. `16922b5`.
- ✅ **`s263-D10` HAS THE REGISTERED BITE ARM IT WAS BORN WITHOUT, AND THE ARM GRADES THE CLAUSE.** Lane B added `selftest_rulings_freshness()` to `knowledge/_capture_gate.py` (wired into `_selftest_body()` beside its sibling `selftest_index_freshness`) and `case_capture_gate_rulings_arm()` to `knowledge/_tests/test_gates.py`, called from `main()` — **75 + 27 insertions, 0 deletions, nothing existing edited**. Four bites: the out-loud SKIP · the never-generated page · **a GREEN control that must also say `FRESH`** · the defect itself. **Three FAIL-OPEN mutants were applied to copies and every one turned the arm RED** — `if rc != 0:` → `if False:`, a silent `fails.append(…STALE…)` → `notes.append(…)` blocking→advisory demotion, and an early `return fails, notes` (which killed **all four** bites) — while an unmutated control loaded through the identical importlib path in the same process returned `[]`. ⛔ **A `CASES` row CANNOT hold this check and the reason is structural, now written into the code so no one retries it**: it is a *function* inside `wrap_checks()` with no exit code (`python3 knowledge/_capture_gate.py` bare is `REFUSED (write-gate)`), and it is REPO-scoped — it reads `knowledge/_rulings.json` **and** `notes/_RULINGS.html`, while `fresh_copy` copies `knowledge/` alone. ✅ **No copytree anywhere: peak scratch under 3 MB, and the mount reads 33% used / 309 G free — the 89% in the brief was the Mac disk, not this one.** `67b1879`.
- ✅ **TWO INHERITED REDS CLOSED, AND BOTH REPAIRS CAME OUT OF THE REPO'S OWN HISTORY RATHER THAN OUT OF A LANE'S JUDGEMENT.** `python3 knowledge/_validate_icons.py` is **GREEN (5 UNKNOWN → 0)**: Legend's five `<svg class="dv-svg">` elements are **bar-chart canvases, not icons** — `<rect class="dv-series">` + `<line class="dv-baseline">`, two specimens and three small multiples — and they gained the `data-bespoke="chart canvas — dataviz geometry, not an icon…"` reason string **copied byte-for-byte** from the fourteen chart snippets. `knowledge/components/footer.meta.json` is **SCHEMA-VALID for the first time since #261**: `edges.composes` was **an invented edge type with no consumer anywhere in `knowledge/*.py`** — silently invisible to the KG rather than merely non-validating — and became `edges.consumes` (the typed key fifteen sibling metas use) plus the `$consumes` array `gen_kg_edges.py:322` name-matches, without which the next regeneration would drop the edge again; `provenance.source: "redesign"` → `"gap-report"` was **RESTORED from `git show 6e6271f`**, not chosen. `_build_integrity.py`: **16 → 14** errors, schema **132/137 → 133/137**. `a88673e`.
- ⛔ **THE FOURTEEN INTEGRITY ERRORS THAT STAND ARE ONE CAUSE — #261-ERA METAS OUTRAN `meta.schema.json` — AND EVERY REPAIR IS A SCHEMA DECISION, SO NONE WAS TAKEN.** Four shapes, censused over the corpus: `stateModel` authored as a rich object in **4** metas where the schema says `enum: simple|full` (111 absent · 23 string · 4 dict) · `with[]` as bare strings (Data grid ×6) and a `when` clause (Legend) with no seat · four edge types with no schema seat (`drivesConsumer`, `composedOf`, `delegatesTo`, `$contract`) · `relationships.composes` + `$composes-verbatim` in a closed object. ⚠ **`edges` is the ONE object in the schema with `additionalProperties:false` and NO `^\$` patternProperties**, which is why a `$`-sigil key reds there and nowhere else — recorded because it makes the "demote to a sigil" repair unavailable inside `edges` specifically. **No ruling governs any of it**: 441 rulings grepped for `footer|provenance|redesign|meta\.schema` — `s263-D7`/`s263-D12` govern footer's dormant variant only.
- ✅ **THE FOURTH RED — `_validate_kg.py` 13 → 5 — AND THE FIVE THAT STAND ARE A FENCE, NOT A BACKLOG.** Lane C found it standing beside the three; lane E classified all 13 by cause and repaired 8 **without wording anything**: seven `pattern:`/`context:` nodes registered with `id`/`label`/`sources` **copied entry-for-entry from a clean scratch regeneration's own output** (`_nodes-pattern.json` 375 → 381, `_nodes-context.json` 218 → 220, serialisation byte-verified against the generator's writer), and Legend's hand-slugged `context:small-multiples` **repointed** to `context:dashboard-rows-of-small-multiples` — the id the generator derives from that meta's own `relationships.livesInside` — because **nothing in the corpus produces the short id, so registering it would have meant inventing a node**. ⛔ **The freshness red is a STALE JOIN KEY, not a stale corpus**: `gen_kg_edges.py:load_resolutions` keys every PROMOTE on an **exact `$note` string**, and #258 rewrote the prose that note is derived from; the #135 verdict itself is unchanged and still correct. `087e058`.
- ⛔★★★ **`gen_kg_edges.py` IS FENCED BY A MEASUREMENT: A CLEAN REGENERATION TODAY REWRITES EIGHT METAS AND DELETES AUTHORED CONTENT.** The diff is **441 lines** and is filed (`probe-regeneration-would-rewrite-8-metas.diff`): it deletes Filter-toolbar-bar's `composedOf` / `delegatesTo` / `drivesConsumer` / `$contract` blocks in full — the `s258-D1` event+attribute contract, ~40 lines — Legend's `containedBy` and `governedBy` edges (`ruling:s151-D1`, `s248-D3`, `s258-D1`), and the tail of Footer's `context:template-dashboard` `$note`; the rest is field-ORDER churn from `splice_edges` putting `edges` last. **`s245-D7` is the ruled mechanism that protects authored edges from exactly this, and its carry list is `DECLARED_EDGE_TYPES = ("groupsWith",)` — ONE entry, so nothing else survives.** ⇒ **do not run the generator before lane E's RSQ 2 is ruled.** The registries were advanced by **ADDITION ONLY** for the same reason: a regeneration would REMOVE `context:page-above-a-table-or-list-items-region`, which `filter-toolbar-bar.meta.json:151` live-references.
- ★★★ **`notes/_PROPOSED-263.html` WAS DRIVEN IN A REAL BROWSER FOR THE FIRST TIME — THE PAGE ELEVEN RULINGS WERE MADE OFF HAD NEVER BEEN RENDERED.** Chromium headless in the sandbox off `_RUNBOOK-render-verify.md`; ⚠ **every path the runbook names as reusable was GONE (VM rebuild)** — `/var/tmp/pylibs`, `/var/tmp/pw-browsers-220`, `~/.cache/ms-playwright`, `<MOUNT>/outputs/syslibs` — so the class fix was re-run from scratch and it worked, exit 0, `ldd | grep -c "not found"` → **0** after one rootless `libxdamage1` deb. **Five contexts, and the interaction core is OBSERVED:** `localStorage` round-trip survives `reload()` with ruling AND note intact (`{"P-01":{"v":"ACCEPT","note":"ink seat, confirmed"},…}`) · click-again-to-unset decrements 3→2→3 · `#tallyN` and `#sRuled` stay in sync through 0 → 3 → 11 → clear · the export block's `NOT RULED` line is exact at **11 / 8 / none** · all **33** `button.rb` measure **44.0 × 243.3** at 760 and **44.0 × 115.0** at 375, one distinct size, no outlier · `scrollWidth == clientWidth` at both widths · **the console is completely silent — zero logs, zero warnings, zero page errors, across all five contexts.** `d3a2297`.
- ⛔ **AND TWO REAL DEFECTS FELL OUT OF THAT DRIVE, BOTH IN THE THEME LAYER, AND THE PAGE WAS NOT EDITED.** **(a)** The sticky control bar does not hold the floor its own ruling rows hold: `#exportBtn`/`#clearBtn` measure **34.2px**, `label.tog` **35.0**, the `#decide` checkbox **13×13** — at BOTH 760 and 375, because the `@media (max-width:760px)` block at lines 314–320 grows `button.rb` and never touches `.bar button,.bar label.tog`. **(b)** The `[data-theme="dark"]` block at line 196 is a **DEAD ARM**: there is no toggle, theming is `prefers-color-scheme` only and on that path it is **CORRECT** (`#DA1A00` light / `#F6604C` dark — TWO-RED LAW `s151-D1` held at 1280 and 375); but the block redefines **no custom properties**, so forced on `<html>` it is invisible (the two PNGs are **byte-identical, 81,705 B both — that identity IS the finding**) and forced on `<body>` it yields a dark ground with **`accent` still `#DA1A00`** — a TWO-RED-LAW violation the working path does not have — with the bar, the quote panel and the output panel still light-painted. ⚠ **The file also declares two different darks: `#1A1A1A` at line 196 against `#0C0C0C` at line 224.** All three are D's RSQ 1–3.
- ⚙ **GAUGE — TWO OBJECTS, REPORTED SEPARATELY, NEVER SUMMED OR CONVERTED** [[measure-dont-convert-units]]. **FILL** is resident context (`message.usage`); **THROUGHPUT** is the cumulative log. ✅ **NO HOLE — `tiktoken` was installed at the conductor's opener.** The conductor **DECLARED 147,425 real** at the brief cut — **32,575 UNDER** the `s260-D2` delegated line of 180,000 ⇒ **the delegation is because Dave is asleep, not because a line was crossed.** First-hand at this seat, `knowledge/_checkin.py` reads his transcript at **148,308 real over 47 turns**; `s214-D5`: **brief-cut 147,425 · sub-cut 148,308 · delta 883 · replay unobservable (conductor-side, post-wrap)** — the second consecutive wrap at which the hand-over is fully measured. ⛔ **BOOT 70,260 real, MEASURED — 260 OVER the 70,000 shrink-only literal, RECORDED AS A BREACH**, ending eight consecutive under-ceiling readings (#264 read 69,955). ⛔ **The literal is SHRINK-ONLY (`s240-D2`/`s241-D1`): the remedy is to cut the boot, never to raise the number, raising it is Dave's word alone, and it is not a price a wrap may pay to unblock itself** [[gate-must-quote-what-it-forbids]]. The gate's standing refusal is still #255's **70,127**; the commit is made in the **#243 form** with the refusal RECORDED, the **nineteenth** wrap running.
- ✅ **A `subs` LINE IS WRITTEN, AND EVERY FIGURE IN IT IS A MEASUREMENT** — Agent `usage`, REAL Claude tokens, **QUOTA not FILL**, never added to the block's fill numbers and never graded against the stop line: the two `/goal` drivers **48,453** + **49,700**, lane **B 117,210**, lane **C 148,627**, lane **D 80,597**, lane **E 115,314** — `subs 560,101 tokens (n=6)`. ⛔ **THIS WRAP SEAT'S OWN SPEND IS NOT IN THAT FIGURE AND NO NUMBER IS WRITTEN FOR IT** — a sub cannot read its own `message.usage` from inside itself, and an UNKNOWN is never turned into a number [[feedback-measuring-tool-must-not-guess]].
- ⛔ **THE "STALE `.git/index.lock`" WAS NEVER STALE, AND THE DIAGNOSIS THAT STOOD FOR TWO SESSIONS WAS WRONG ABOUT THE CAUSE.** The Cowork sandbox was refusing **all unlinks** until `allow_cowork_file_delete` was granted, so git's own lockfiles and its `tmp_obj_*` objects survived every commit — not because a process died holding one, but because nothing on this mount could remove any file. Granted mid-session; cleared. ★ **The carried item that says a stale lock "can only be MOVED, and Dave deletes it Mac-side" now has a second, truer half: the permission is grantable from inside.**
- ⚠ **DECLARED SKIPS AT THIS WRAP, EACH WITH ITS SIZE** (declare-last, and the size is the point): **2e = 0 dated strata rolled** — `## ⬛ DO THIS FIRST` measures **10,140 real / 78 raw lines**, inside the 120-warn / 180-block band, and nothing in it aged past LATEST+1 · **2c RAN** (the #263 banner → `_GM-ARCHIVE.md` § Batch 2026-09-09 #265) · **2d RAN** (the #262 ⏱ delta + its `Previous:` chain segment, VERBATIM → `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #265) · **2f RAN** (the `#### 2026-09-09 #264` stratum → `notes/_GAUGE-LOG.md` + `_GM-ARCHIVE.md`) · **MEMORY = 0 bytes at this seat (SEAT LIMIT, FIFTH CONSECUTIVE; the conductor wrote the hook before delegating)** · **`_CARRIES.md` never read whole — 11.4 MB (11,996,718 B, MEASURED at this seat after the section landed), worked line-wise through `_capture_gate._carry_items()`** · **BOOT MEASURED 70,260 real — no hole, and a BREACH** · full `knowledge/_tests/test_gates.py` **NOT RUN** at this seat (lane B drove its own new case in-process and took no copytree) · `_capture_gate.py --selftest` **NOT re-driven whole** (it exceeds the sandbox call wall — the fifth consecutive wrap to declare it) · no `_build_all.py`, no `_validate_screen.py`, no retrieval query, no recall plant, **no Artifact publish** — refused in Cowork since #263.
- ⬛ **STILL HIS, CARRIED FORWARD — RULING-SHAPED AND NOT RULED HERE:** the **four ungraded `-active` glyphs** (balance-transfer, tax, workspace, digital-statements) on `notes/_REVIEW-264-active-glyphs-2.html`, the conductor's PROPOSED lead for #266 · **`global-money`**, which is one connected ink piece and needs DRAWING, not deriving · **THIRTEEN lane ruling-shaped questions — B:2 · C:5 · D:3 · E:3** — every one filed with its options priced and a recommendation, and **not one ruled**, because Dave was asleep · the **two `_PROPOSED-263.html` defects**, one CSS line each and both ruling-shaped · **`DECLARED_EDGE_TYPES`**, which fences the KG generator until he answers · whether a **gate report should be refused at commit when its own tree ≠ HEAD** (#263, age 2) · **#241's midnight-wrap question, age 23** · and **ritual step 3 at a delegated seat**, now with five datapoints. ⛔ **This seat ruled nothing.** **`_CARRIES.md` § `## residual → #266` is the carry set (`s225-D2`, probe 396); the banner carries the pointer and the probeable count.**

## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#264**, one evening 19:26 → 20:30, conductor **Fable**, no subs but this OPUS 5 wrap sub — ★★★ **TWO GLYPH TWINS RULED, A MIS-TWINNING GATE ARM, AND EIGHT DERIVED `-active` GLYPHS ENTERED THE LIBRARY**)

*(WHY/HOW: `_DECISION-HISTORY/2026-09-09-264-glyph-twins-and-derived-actives.md` — why two of the session's three opening carries were WRONG rather than open, how a pairing defect was generalised into a blocking gate arm instead of being fixed twice, and what the second derivation pass proved about the one glyph that still refuses. Filed report: `notes/_subreports/2026-09-09-264-W-wrap.md`.)*

- ✅ **NO DATE SPLIT — THE SESSION, ITS RITUAL AND ITS COMMITS ARE ALL 2026-09-09.** The three standing WRAP DATE SPLIT notices belong to #241, #248 and #261; nothing was re-dated here because nothing needed to be. #241's ruling-shaped question — what a midnight-spanning wrap should stamp — is **still Dave's, now at age 22**.
- ⛔ **THE SESSION OPENED ON TWO CARRIES AND BOTH WERE WRONG, WHICH IS THE DAY'S FIRST FINDING.** **(1) The Stat card arrow seat was NOT open.** Dave, first sentence: *"I thought this was ruled"* — and he is right: `s263-D1`'s `governs` names `knowledge/snippets/Stat-card.reference.html`, and the P-01 recommendation he ACCEPTed says verbatim **"Stat card moves with it, always."** ⇒ **no ruling owed; the carry is STRUCK.** The #263 wrap read that same `governs`, wrote *"a `governs` list is a scope, not an answer"*, carried it anyway, and the #264 opener repeated it. ★ **A carry that survives a wrap on the strength of the wrap's own doubt is worth one grep of the ruling it doubts.** **(2) The sidebar `chart` glyph was NOT hand-baked.** All **twelve** `<symbol>`s in `Sidebar-nav.reference.html` are **byte-identical to `knowledge/assets/icons/` files by path data**. The defect was **PAIRING**: Spending rested on `data-chart` and went current on `insight-active` (a bulb — a different concept); Transfers rested on `balance-transfer` (which has **no `-active` twin in the library at all**) and went current on `transfer-active`, so the shape changed on selection. **STRUCK, with the repair as its receipt.**
- ★★★ **THREE RULINGS, DAVE'S, INSCRIBED — `knowledge/_rulings.json` entries 437–439, the store 436 → 439, each parsing with `by` Dave · `date` 2026-09-09** (`_inscribe_ruling.py`, reconstruction proof passed on each). **`s264-D1`** — Sidebar-nav's Spending row wears `data-chart` / `data-chart-active`; his words, off `notes/_REVIEW-264-sidebar-glyph.html` (options A `data-chart`, B `insight`, C `dashboard`): ***"Spending A"***. **`s264-D2`** — Transfers wears `transfer` / `transfer-active` (options D the transfer pair, E as built): ***"Transfer D"***; scope is Sidebar-nav, and the four App-shell / Command-palette snippets are a carry, not ruled there. **`s264-D3`** — the derived-glyph experiment is KEPT and eight twins enter the library: ***"Good try btw, maybe shelve the rejected ones for further work. keep teh others, good experiment we can return to it later."***, then ***"Add the ones I said yes to to the library / the rejected ones we can work on later"***, with the thirteen grades verbatim in the ruling — including ***"balance-transfer → neither — the whole card should be filled not just the top, but the overlap exclusion are need to be kept"***, ***"tax → neither — the document icon half should be filled, if you look at teh document icon as a guide"***, ***"workspace → neither — we have to fill teh otehr part of teh icon too"***, ***"digital-statements → neither — need both parts filled"*** and ***"global-money → neither — thsi is quite ahard one to get right"***. Commits `9bfacb9` (D1/D2) and `c7247c2` (D3).
- ★★★ **THE PAIRING DEFECT WAS GENERALISED INTO A GATE ARM RATHER THAN FIXED TWICE — Dave: *"1. okay fix them 2. do it"*.** `knowledge/_validate_icons.py` grew a **TWIN ARM**: every `.ic-line` / `.ic-fill` pair in a snippet is resolved to library slugs, the fill must be the line's `-active` or `-active-badge`, and **MIS-TWINNED is BLOCKING**; a line glyph with no twin in the library is **reported, not failed** (that is `balance-transfer`'s state, and it is a fact about the library, not a defect in the page). Bite-test **`twin`** (`mut_mistwinned_icon`) is registered in `knowledge/_tests/test_gates.py` and was driven **RED → GREEN in-process** on **one 93 MB copy**, because the suite's own harness copytrees ≈5 GB and ENOSPCs at 89% disk. ✅ **The arm found a THIRD case on its first run that the eye had missed** — Tab-bar's Insights row carried `insight` in **both** slots, so its "current" state was the line glyph; now `insight-active` (`s262-D3`). Four app-shell/palette snippets moved `balance-transfer` → `transfer` at rest in the same commit. `3d7def7`.
- ★★★ **THE EXPERIMENT — Dave: *"go, lets see whatcha got"* — DERIVED A FILLED TWIN FROM A LINE GLYPH BY GEOMETRY, AND IT IS CALIBRATED, NOT ASSERTED.** Skia path ops (`skia-python`, its `libEGL`/`libGL`/`libglvnd`/`libGLX`/`libOpenGL` extracted without root the `chromium-in-sandbox-recipe` way): **S** = silhouette (contours filled and unioned) · **B** = S − erode(S, 1.25) · **I** = L − B · **A1** = S − I · **A2** = S − silhouette(I). ⚠ **Calibrated against TEN human-drawn pairs before it was shown to him — 7 within tolerance, and the three misses are DESIGNER EDITS no rule recovers** (card, alert, insight), with `settings` needing A2. Thirteen orphans went to `notes/_REVIEW-264-active-glyphs.html` (`notes/_lanes/264-active-gen.py`, `264-active-page.py`, `3722f26`) and **nothing entered the library before he graded them**.
- ✅ **EIGHT DERIVED TWINS ARE IN THE LIBRARY, AND THE MANIFEST SAYS THEY ARE DERIVED.** `cheque` · `finances` · `document-report` · `newspaper` · `device-mobile` · `online-banking` · `presentation` · `add-circle`, written as `<slug>-active.svg` with a **`$derived`** annotation in `knowledge/assets/icons/icons.manifest.json` (textual insertion; `$counts` + `$total` **658 → 666**; the icon gate's glyph total **750 → 758**, and the **5 Legend UNKNOWN** icons it still reports are pre-existing and untouched). ⛔ **A generated twin is not a Figma export and the manifest is not allowed to pretend otherwise** — that is what `$derived` is for. `c7247c2`.
- ★★★ **THE SECOND PASS FOUND THE CLASS, AND THEN FOUND THE ONE GLYPH THE CLASS DOES NOT CONTAIN — Dave: *"have another go"*.** His five rejections were **ONE CLASS**: two-body icons with an overlap exclusion, where the derivation fills only the front body because the rear body's contour is not closed on its own. `notes/_lanes/264-active-gen2.py` rebuilds the silhouette as **the holes of the EXTERIOR of (L ∪ grow(frontSil, gap 1.0))**, finds fronts as **rings whose sealing GAINS area** (>3 px², raster-counted at 16× **for classification only**), and morphologically closes open bodies. **`balance-transfer`, `tax`, `workspace` and `digital-statements` now fill.** ⛔ **`global-money` is ONE CONNECTED INK PIECE — the arrows touch the meridians, so there is no second body to find; it is a DRAWING problem, not a derivation problem.** Page `notes/_REVIEW-264-active-glyphs-2.html`, `5e97c90`. Dave, closing: ***"no time for this now, but we can return to it another time because we are getting somewhere"*** ⇒ **the four stay UNGRADED, nothing further entered the library, and that sentence was appended to `s264-D3`'s `evidence` (`--amend-evidence`)** rather than being left in chat.
- ⚙ **GAUGE — TWO OBJECTS, REPORTED SEPARATELY, NEVER SUMMED OR CONVERTED** [[measure-dont-convert-units]]. **FILL** is resident context (`message.usage`); **THROUGHPUT** is the cumulative log. ✅ **NO HOLE THIS SESSION — `tiktoken` was installed at the opener and again at this seat.** The conductor **DECLARED 214,299 real FILL** at the brief cut (peak, 96 turns) — **34,299 OVER the `s260-D2` delegated **stop line 180,000**** and over the 200,000 working ceiling, ⇒ **this wrap is DELEGATED and that is the reason.** First-hand at this seat, `knowledge/_checkin.py` reads his transcript at **221,197 real over 101 turns**; the two readings are minutes apart, both stand, and neither is the other. **Boot 69,955 real**, measured at the conductor's opener — **45 UNDER** the 70,000 shrink-only literal, an **eighth consecutive under-ceiling reading**. Throughput **612,089** (conductor) / **624,066** (this seat), cl100k-estimate. ⛔ **NO `subs` LINE IS WRITTEN AND THAT IS THE CONTRACT, NOT AN OMISSION** — the only sub was this wrap seat, whose own spend is not readable from inside itself, and an UNKNOWN is never turned into a number [[feedback-measuring-tool-must-not-guess]].
- ✅ **THE BOOT-CEILING ARM STILL REFUSES, AND IT IS STILL RIGHT TO.** `_gauge_tokens.BOOT_CEILING_TK` = 70,000 and **#255's 70,127 is the one post-diet reading above it** — a standing breach this session did not cause and may not clear. `s240-D2`/`s241-D1` make the literal **shrink-only**: the remedy is to cut the boot, never to raise the number, and raising it is Dave's word alone and is **not a price a wrap may pay to unblock itself** [[gate-must-quote-what-it-forbids]]. The commit is therefore made in the **#243 form**, with the refusal RECORDED rather than routed around — the **eighteenth** wrap running.
- ⛔ **NOT DONE / NOT CLAIMED AT THIS WRAP SEAT.** **MEMORY (ritual step 3) — a SEAT LIMIT, DECLARED NOT SKIPPED, for the FOURTH consecutive delegated wrap (#261, #262, #263, #264)**; ⚠ **the difference this time is that the brief declared it off-limits and the conductor wrote the hook BEFORE delegating**, so the step was covered rather than merely declared. ⛔ **The full `knowledge/_tests/test_gates.py` suite is still unrun on this disk** (only the `icon` and `twin` cases were driven, in-process). ⛔ **Three pre-existing reds stand unchanged and none was caused or repaired here** — `knowledge/components/footer.meta.json`'s two schema reds · `_validate_icons.py`'s 5 UNKNOWN Legend icons · `_build_integrity.py`. ⛔ **No Artifact publish was attempted** — it was REFUSED in Cowork at #263 and the file is the surface.
- ⚠ **DECLARED SKIPS AT THIS WRAP, EACH WITH ITS SIZE** (declare-last, and the size is the point): **2e = 0 dated strata rolled** — `## ⬛ DO THIS FIRST` measures **10,140 real / 109 raw lines**, inside the 120-warn / 180-block band, and nothing in it aged past LATEST+1 · **2c RAN** (the #262 banner → `_GM-ARCHIVE.md` § Batch 2026-09-09 #264) · **2d RAN** (the #261 ⏱ delta + its `Previous:` chain segment, VERBATIM → `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #264) · **2f RAN** (the `#### 2026-09-09 #263` stratum → `notes/_GAUGE-LOG.md` + `_GM-ARCHIVE.md`) · **MEMORY = 0 bytes at this seat (SEAT LIMIT, conductor wrote the hook)** · **`_CARRIES.md` never read whole — **11.0 MB** (11528723 B, MEASURED — an 11.1 estimate stood here for the length of one wrap and is corrected**), worked line-wise through `_capture_gate._carry_items()` · no `_build_all.py` (SANDBOX-IMPOSSIBLE) · no `knowledge/_validate_screen.py` · **full `test_gates.py` not run** (disk 89%, ≈93 MB per copy) · `notes/_PROPOSED-263.html` **still never driven in a browser** · **no retrieval query, no recall plant** · **no Artifact publish** (refused in Cowork at #263).
- ⬛ **STILL HIS, CARRIED FORWARD — RULING-SHAPED AND NOT RULED HERE:** the **`/goal` bite-test**, ruled *"do it"* at the #264 opener and **NOT STARTED** — the proposed first item of #265 · the **four ungraded derived twins** on `notes/_REVIEW-264-active-glyphs-2.html` (balance-transfer, tax, workspace, digital-statements) and **whether `global-money` gets DRAWN** · whether a **gate report should be refused at commit when its own tree ≠ HEAD** (#263's finding, age 1) · **#241's midnight-wrap question, age 22** · what to do about **ritual step 3 at a delegated seat**, now with four datapoints. ⛔ **This seat ruled nothing and graded no glyph.** **`_CARRIES.md` § `## residual → #265` is the carry set (`s225-D2`); the banner carries the pointer and the probeable count.**

## ⏱ PRIOR DELTA — 2026-09-09 (Wed from `date`) (**#263**, one day, conductor **Fable** + **3 OPUS 5 SUBS** (P, E, A) + this OPUS 5 wrap sub, with lane C run at the conductor's own seat — ★★★ **THE ELEVEN PROPOSED DEFAULTS WERE RULED IN ONE PASS, AND A GATE THAT WAS GRADING NOTHING BECAME THE TENTH RELEASE GATE**)

*(WHY/HOW: `_DECISION-HISTORY/2026-09-09-263-eleven-defaults-and-the-tenth-gate.md` — why a defaulted recommendation has no natural moment to come back, and how one of the eleven rulings exposed a gate that was blocking on stale evidence. Filed report: `notes/_subreports/2026-09-09-263-W-wrap.md`. Lane fragments: `notes/_lanes/263-P-proposed-review.md` · `notes/_lanes/263-E-enact-d7-d10.md` · `notes/_lanes/263-A-enact-d11.md` · `notes/_lanes/263-C-redrive-chart-engine.md`.)*

- ★★★ **THIRTEEN RULINGS, DAVE'S, INSCRIBED — `knowledge/_rulings.json` entries 424–436, the store 423 → 436, each parsing with `by` Dave · `date` 2026-09-09 · `status` ruled.** `s263-D1` … `s263-D11` rule the **eleven PROPOSED defaults** the #261 conductor had defaulted and #262 had left standing: **P-01** the delta glyph ink seat *(governs `Kpi-tile.reference.html` AND `Stat-card.reference.html`)* · **P-02** group-row by type · **P-03** disabled-column alpha · **P-04** adopting `data-apollo-filter-*` · **P-05** the 1400px collapse · **P-06** keeping the Tab-bar name · **P-07** the doormat · **P-08** the 44px legend seat · **P-09** `data-dv-controls` · **P-10** `--check` as a wrap gate · **P-11** retiring the source-text aria arm. **EIGHT ARE STRAIGHT ACCEPTS.** ★ **THE THREE THAT CAME BACK `LATER` WERE RULED ON HIS OWN SENTENCES:** `s263-D7` — *"[p]ark — keep the doormat as a dormant variant of Footer so it stays one component"*, then, asked what to call the state, **"dormant variant"** ⇒ the doormat is neither retired nor live, and `s261-D3`'s *"App footer **for now**"* hedge is discharged · `s263-D8` — *"Is this teh legend for charts? if so leave it at 44 it works fine"* → **"accept"** once it was confirmed as the chart legend, so **the 44px seat stands** · `s263-D9` — *"accept contract-only, it's an interesting idea to wire one legend to multiple charts but not required at this stage"*, an acceptance with its scope cut to the contract and the wider idea parked **in his own words**. Then two more, both arising from enactment rather than from a plan: `s263-D12` — *"whatever is the best standard solution"* — and `s263-D13` — **"yes"**.

- ★★★ **THE DAY: A DEFAULTED LIST GOT A SURFACE, AND THE SURFACE GOT ELEVEN ANSWERS IN ONE PASS.** Lane P built `notes/_PROPOSED-263.html` (50,906 B; generator kept as `notes/_lanes/263-P-build.py`, so the page is regenerable and not hand-edited): eleven cards, each with the **verbatim recommendation**, the reason given, **what the code does today**, the alternative, and an Accept / Reject / Later row with a note field — plus an **export block** rendering one line per ruled item **and a `NOT RULED (n):` line**, which is what let the wrap see what was still open. ⛔ **The lane ruled NOTHING — every row shipped empty and no default was pre-selected.** ⚠ **AND THE PAGE WAS NEVER DRIVEN IN A BROWSER AND NEVER PUBLISHED** (hosted publish refused — the approval card could not be answered from the seat), so the surface Dave read was the file; its behaviour is proved by construction, not by observation.

- ⛔ **A GATE THAT `s263-D11` HAD JUST MADE LOAD-BEARING WAS GRADING NOTHING, AND THE PROOF WAS IN A COMMITTED GREEN REPORT.** `s263-D11` deletes `_validate_snippets.py`'s source-text `requiredAria` arm (with its bite-test — a bite-test for a retired arm is a guaranteed RED — and four docs corrected), leaving the **DOM-driven** arm in `_validate_dataviz.py` as the one gate. Lane A then found **every driven receipt in the repo STALE**: `knowledge/canon/type.css` moved at **`4cc4204`** (#261 lane F2, 10:58) *after* `knowledge/_tests/chart-engine/_receipts.json` was driven at 09:54 (`0420197`, hash `295b2867…`), so `_validate_dataviz.py` read **STALE on all 27 pages** and the new one-gate was **blocking-on-stale**. ★ **AND `knowledge/_DATAVIZ-GATE.md`, committed at `81ce08f` (12:56), reads PASS / 0 STALE — a report written from a tree that did not match HEAD**, the #253 two-lanes-wiping pattern in a new venue. Nothing in the repo compares a committed gate report against the commit it rides on. **Ruling-shaped, HIS, and carried.**

- ✅ **THE RE-DRIVE WAS A MEASUREMENT, NOT A REASSURANCE.** Chromium 151 was installed in the sandbox **without root** — playwright plus `libXdamage.so.1` extracted from the arm64 deb into `~/.local/lib` under `LD_LIBRARY_PATH` — and `knowledge/_drive_chart_engine.py` re-drove **27 pages × 8 theme×mode combos** at **`521a751`**. Result: **0 differing measured fields** against the 09:54 receipts — marks, rows, contrast, rogue hex, gradients, curve and aria all identical, same Chromium build. ⇒ **the type.css change moved nothing a chart measures, and v1.0.9's charts are retroactively clean.** `_validate_dataviz.py` → `✅ DataViz gate passed (15 chart surface file(s))`, 0 STALE, 0 blocking; `requiredAria [driven]` reads n/n present in all 8 combos on every page. ⚠ The STALE arm was proved live **by observation** — it fired on the real tree before the re-drive, and lane A had already driven its RED on a mutant receipt.

- ★★★ **THE TENTH RELEASE GATE (`s263-D13`, `5050b33`).** The dataviz gate was **not** among the nine release gates, which is exactly why nothing caught the staleness at the v1.0.9 cut. Asked whether it should join, Dave said **"yes"**. The enactment is deliberately narrow: `apollo-spider/build-designer-pack.sh --release` now runs a **`--receipts-fresh`** check **after `require_clean`**, **write-nothing** — it REFUSES over stale driven receipts rather than re-driving them, because a release that silently re-drives its own evidence is a release grading its own homework. The selftest drives the **mutant RED and the real control GREEN**; the frozen, audit and CI gates still PASS.

- ✅ **`s263-D12` IS A SCHEMA RULING THAT NOBODY PLANNED, AND IT EXISTS BECAUSE A LANE DECLARED ITS DEVIATION INSTEAD OF HIDING IT.** Enacting D7, lane E found `knowledge/components/meta.schema.json` defines `variants[].items` with `"additionalProperties": false` and `patternProperties {"^\\$": {}}`, so a bare `status` key drove the meta validator RED (measured verbatim before anything was changed). The lane took the legal `$status` route **and said so**. Put to Dave, the answer was *"whatever is the best standard solution"* ⇒ **`variants[].status` is now a first-class enum `active | dormant | deprecated`** and the footer's doormat carries `status: "dormant"` (`27f0f46`). ★ **The `$`-prefix convention is for one-off annotations; a state three components will want is not a one-off.**

- ✅ **`s263-D10` IS ENACTED AND RAN FOR THE FIRST TIME AT THIS WRAP.** `rulings_page_freshness_check(repo)` is wired **first inside `_capture_gate.py::wrap_checks()`, BLOCKING**, calling the renderer's own `check()` **in-process** (no subprocess — the sandbox call-boundary lesson), so one implementation of the freshness rule exists; runbook **step 4d** is new, between 4c and 5, and the step list in its header now reads `… 4, 4b, 4c, 4d, 5, 5b`. The RED arm was driven by hand at lane E. ⛔ **There is NO registered bite-test for it in `knowledge/_tests/`** — declared at birth, carried, not discovered later [[instrument-without-a-consumer]].

- ⚙ **GAUGE — TWO OBJECTS, REPORTED SEPARATELY, NEVER SUMMED OR CONVERTED** [[measure-dont-convert-units]]. ⛔ **The conductor's FILL was NOT MEASURED at the wrap cut** — the brief declares an **ESTIMATE ~65–75K real** and marks it as one, because no `message.usage` was read at that seat. **THROUGHPUT at the wrap seam: 167,102 cl100k-estimate declared by the conductor · 171,698 measured first-hand at this seat** (a moving number read minutes apart; both stand). ⛔ **AND `_checkin.py`'s BUDGET line at this seat reads FILL 155,332 real over 74 turns, boot 69,687, which disagrees with the conductor's own estimate by roughly 2× — RECORDED, NOT RECONCILED**, because this seat cannot prove from inside itself which window that transcript belongs to. **subs 306,253 tokens (n=3)** — P **99,889** · E **117,998** · A **88,366** — **QUOTA, never window FILL**, and never graded against the stop line. ⚠ **THE `s260-D2` DELEGATED stop line 180,000 real STANDS AND CANNOT BE GRADED THIS SESSION** — the FILL it grades was not measured, so the line exists and the reading does not; ⛔ **an ESTIMATE is not put in its place** [[feedback-measuring-tool-must-not-guess]]. **Boot: NOT MEASURED** (no `tiktoken` at the opener; installed after the fact) ⇒ the boot-band series takes a **HOLE for #263** rather than an invented number, and the `--wrap` gate form is **REFUSED for the seventeenth wrap running** on #255's 70,127.

- ⚠ **DECLARED SKIPS AT THIS WRAP, EACH WITH ITS SIZE** (declare-last, and the size is the point): **2e = 0 dated strata rolled**, `## ⬛ DO THIS FIRST` at **10,140 real / 109 raw lines** inside the 120-warn band · **2c/2d/2f ALL RAN CLEAN** (#261 banner 11 ln · #260 ⏱ delta 15 ln + its 2,708-character chain segment · the #262 stratum 14 ln → `notes/_GAUGE-LOG.md` + 2 ln → `_GM-ARCHIVE.md`) · **MEMORY = 0 bytes at this seat, a SEAT LIMIT and the THIRD consecutive one** · **`_CARRIES.md` never read whole — 10.6 MB** · **BOOT not measured** · **`notes/_PROPOSED-263.html` never driven, never published** · no `_build_all.py`, no `_validate_screen.py`, `test_gates.py` NOT RUNNABLE (ENOSPC), no recall plant, no retrieval query.

- ⬛ **STILL HIS, CARRIED FORWARD — RULING-SHAPED AND NOT RULED HERE:** the **Stat card arrow seat** (⚠ `s263-D1`'s `governs` names `Stat-card.reference.html` and the conductor reads P-01's *"Stat card moves with it"* as settling it — ⛔ **Dave has not said so and this seat did not ask him**) · **`/goal` untested** — nothing tests that the pack HOLDS a goal across a session · the **sidebar `chart` line glyph**, hand-baked with its filled twin named `insight-active` · **whether a gate report should be refused at commit when its own tree does not match HEAD** · **#241's midnight-wrap question, now at age 21** · and the **three pre-existing reds** on a pristine repo (footer's two schema reds · `_validate_icons.py`'s 5 UNKNOWN Legend icons · `_build_integrity.py`'s 17 errors / 25 warnings), none caused here and none repaired here. **`_CARRIES.md` § `## residual → #264` is the carry set (`s225-D2`): 524 aged · 6 new · 1 STRUCK**, probe **387**; the banner carries the pointer and the count.

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

**102 decision nodes — 84 LIVE · 9 AMENDED · 8 DEAD · 1 OPEN.** Full typed edges + what-touches-this map: `knowledge/_DECISION-GRAPH.md`.

**☠ DEAD — do not build on (8):**
- **DV:DOSSIER.chevron** · DataViz dossier chevron-on-stacked claim — superseded by DV-D04
- **DV:DOSSIER.s07** · DataViz dossier §07 one-file-per-component — superseded by DV-D01
- **R-D8** · Green/blue Band A; dark set closes — superseded by R-D9, R-D10
- **R-D13** · Light fills locked (first pass); dark reopened — superseded by R-D14
- **T-D7** · Binding mechanism: measure before ruling — superseded by T-D8
- **T-D11** · /1 batch attempted, failing, reverted — superseded by T-D12
- **TYPE:2026-07-17:composite-txt-child** · 07-17 composite with required .txt child — superseded by T-D9
- **TYPE:2026-07-18:badge-A8000B** · #A8000B badge ruling (same-day superseded) — superseded by TYPE:2026-07-18:sat-ceiling

**◐ AMENDED — live, but a specific claim is dead (9):**
- **ADR-0006** · Flexing engine product shape — dead claim(s): cool-warm-hot register framing
- **ADR-0015** · Behaviour partials: dataviz interaction layer as generated JS — dead claim(s): size-clause-and-one-source-posture; group-wide-injection-becomes-manifest-gated; size-clause-unit-becomes-code-only
- **ADR-0015-A1** · Behaviour sources may be MANY; the 16KB cap becomes per-source legibility plus a 32KB per-group page budget — dead claim(s): page-budget-value-32-reads-34-and-sum-becomes-per-member
- **ADR-0015-A2** · Consumes-manifest: behaviour injection is universal by default, narrowed by a member's positive declaration, fail-loud both ways (TENTATIVE, revisit open) — dead claim(s): budgets-are-no-longer-untouched-consumes-now-drives-the-page-sum
- **R-D1** · RAG promotion round one — dead claim(s): dark red #CC4333 as the status-fill red; the vaguer 'future legacy theme' phrasing
- **R-D2** · Background/glyph split + matting — dead claim(s): role-uniformity
- **R-D3** · Amber solved
- **R-D4** · Matting rungs + first token promotion — dead claim(s): green/blue rung values for light fills
- **R-D10** · Dark set locked — dead claim(s): fills are mode-stable

**○ OPEN / proposed (1):**
- **T-D5** · Tracking rule IF sheets survive

**✓ LIVE (84)** — in force; titles in `_DECISION-GRAPH.md` §②:
  ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0007, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0012-A1, ADR-0013, ADR-0014, ADR-0015-A3, ADR-0016, ADR-0017, B-D1, B-D2, B-D3, B-D4, B-D5, B-D6, B-D7, CHARTER.S9, DEF-003, DEF-005, DEF-006, DV-D01, DV-D02, DV-D03, DV-D04, DV-D05, DV-D06, DV-D07, DV-D08, DV-D09, DV-D10, DV-D11, DV-D12, DV-D13, DV-D14, DV-D15, DV-D16, DV-D17, DV-D18, DV-D19, DV-D20, R-D5, R-D6, R-D6.A, R-D6.A2, R-D6.B, R-D7, R-D9, R-D11, R-D12, R-D12.A, R-D12.B, R-D14, R-D15, R-D16, R-D17, R-D18, R-D19, R-D20, R-D21, R-D22, R-D23, R-D24, R-D25, T-D1, T-D2, T-D3, T-D4, T-D6, T-D8, T-D9, T-D10, T-D12, T-D13, T-D14, T-D15, TYPE:2026-07-18:sat-ceiling

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
⚠ **COUNT RE-BASED #205 2026-08-19 (Dave: "do it"): 76 → 92 metas** (dir entries 96; growth = the #196–#204 component waves incl. the six `s204-D1` P2 components). `ASSERT-009` re-based 77→92 in `knowledge/_assertions.json` — it caught the drift by ABORTing a chore sub's `_build_all` at the veracity gate, which is the assertion doing its job. The #131 measurement prose above is kept verbatim as history. ⚠ The old "77 repo-wide" framing is retired: repo-wide `*.meta.json` is now 176 (snippet metas), a different population. The remedy question below is UNCHANGED and still Dave's.
[born #131 · guards: the 92 `knowledge/components/*.meta.json` files + the count itself (ASSERT-009, re-based #205) · until: Dave picks (a), (b) or (c)]

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
