# Dream pass 9 — floated proposals

provenance: `local_9f1a0cfa-70f4-44ab-a8c9-eb6c51538bf6` · 2026-08-23
status: floated

*I PROPOSE ONLY. Nothing here self-promotes; promotion is Dave's alone on reading this file
(derivation-governance). Every RULED row in `notes/_MEMENTO-DECISIONS.md` and every checked-clear item
at the end of EVERY prior proposals file — pass 3's prose list, pass 4's (q)–(w), pass 5's (x)–(bb),
pass 6's (cc1)–(cc6), pass 7's (dd1)–(dd7), pass 8's (ee1)–(ee7) — was read before hunting. **Proposals
from passes 6/7/8 that are still FLOATED are referenced where new evidence bears on them, never
re-floated.** Standing exclusion held: dream-lane mechanics (cadence, conductor sequence, §🔀 row) are
barred from floating (cc6/dd7/ee7 precedent) — see (ff7).*

★ **Shape A (Cowork), scheduled Sunday 07:10 fire, ON TIME** (prior pass 8 = 2026-08-16). Live tree
verified before measuring: `git log --oneline -1` → `1e59273 #216`, matching the dispatch.

Ranked by prevalence, highest first.

---

### P1 — The pre-flight half of the price-vs-actual dataset has been `⛔ NOT CAPTURED` for **27 consecutive sessions**, and the refusal reason it repeats — *"a sub cannot measure the CONDUCTOR's window"* — is falsified **four lines below itself** by the `s214-D5` hand-over field, which now carries the conductor's window as a measured number

- EVIDENCE:
  - **The run, counted not recalled.** `notes/_GAUGE-LOG.md`, last captured pre-flight is **`:1862`
    `pre-flight #189: boot 56,432 (disk 56,432 measured...)`**. From **`:1871` (#190)** to **`:2209`
    (#215)** every single block reads `⛔ NOT CAPTURED — UNMEASURED`, and #216's block (in
    `knowledge/_memento-index.json:162`, the GM copy — the gauge log lags by one by design, dd2)
    makes **27**. `grep -n "pre-flight #" notes/_GAUGE-LOG.md | grep -c "NOT CAPTURED"` → **96**
    across the whole file; the tail-30 slice is 26 of 26 with #216 the 27th.
  - **The refusal, verbatim, at `notes/_GAUGE-LOG.md:2209`:** *"⛔ NOT CAPTURED — UNMEASURED. Reason
    unchanged from #199…#214 (sixteen consecutive): this is a DELEGATED wrap sub, and **a sub cannot
    measure the CONDUCTOR's window at ITS opener**; every term would be a guess wearing a number's
    authority."*
  - ⛔ **And at `notes/_GAUGE-LOG.md:2213`, four lines later, in the same block:**
    *"**wrap-handover: brief-cut 271,145 real (conductor)** · sub-cut 274,588 real (first-hand) ·
    delta 3,443 real."* The conductor's window IS measured and IS handed to the sub — that is exactly
    what `s214-D5` half 1 was ordered built for. The same pairing appears one session earlier at
    `:2189` (refusal) and `:2193` (`brief-cut 315,136 real (conductor)`). **The premise the refusal
    rests on stopped being true at #214 and the sentence has been copied forward twice since.**
    [[premise-ages-faster-than-rule]]; *stale twice ⇒ generate, don't re-stamp* (`_CHAIN.md:54`).
  - **The hand-typed counter is also wrong, and derivably so.** The block says *"sixteen consecutive"*
    (anchored on #199 and never re-derived); the run actually starts at **#190**, so the true figure
    at #215 is **26**. Same class as pass 5's P2 and pass 7's P1 — an ordinal nothing parses — but a
    *different surface*, and named here only as corroboration, not as a re-float.
  - **What it costs.** Price-vs-actual drift is a **standing dreamer hunt, added at #21 as Dave's own
    pick** (`.claude/agents/dreamer.md:52–54`: *"`notes/_GAUGE-LOG.md` is a dataset now: hunt sessions
    whose pre-flight price and closed band diverge REPEATEDLY"*). With one column empty for 27
    sessions the hunt is **structurally un-runnable** — as it was for me this morning. Pass 4's P1
    made `⛔ NOT CAPTURED` a *legal, honest* form, and it is; what nobody re-checked is that the
    honest refusal became a permanent one.
- PREVALENCE: **27 of 27** sessions since #190; the falsifying counter-evidence present in **2 of 2**
  blocks that carry a `wrap-handover` line (#214, #215). 15 transcripts read, 5 gauge-log strata read
  in full.
- PROPOSED: the **generate-it** triage (`s129-D5`). One line in the wrap-sub brief template
  (`knowledge/_RUNBOOK-capture-ritual.md`, which `s214-D5` already made the home of the hand-over
  field): *the `pre-flight #N` boot term is taken from the conductor's brief-cut figure on the
  hand-over line, attributed to the conductor, or declared absent with the reason re-derived this
  session — the #199 reason string may not be copied.* Smallest reversible step; touches one template
  line and no constant. ⛔ Explicitly NOT proposed: changing any gauge figure, or making this a gate.
- status: floated

---

### P2 — `s188-D1` moved the grading unit from the `MEMORY.md` index line to the hook **FILE**, but memory maintenance still writes the newest fact to the **index line** — so three hooks now carry their live claim only in the half the grader no longer reads, and one of them is graded `AGING` at 34 days for a claim Dave restated **yesterday**

- EVIDENCE:
  - **The unit moved.** This pass's `--refresh` receipt, verbatim:
    *"probe source : hook FILE 94 · index-line FALLBACK 25 · pinned 0 **(s188-D1: the grading UNIT is
    the hook FILE, file first)**"*. That is pass 8's P1 enacted, and it worked — `UNPROVABLE` fell
    **111 → 25** and `FRESH` rose **12 → 78**.
  - **The maintenance surface did not move with it.** A sweep of all 119 linked hooks (index line vs
    hook-file body, comparing the highest `#NNN` session number each mentions) returns **3 hooks whose
    index line cites a session the hook FILE never mentions**:
    - `feedback-gate-dont-patch.md` — index line **`MEMORY.md:93`**: *"#215 Dave: **'always real fixes
      never patches, they just get lost'**"*. The hook file mentions **no session ≥ 200 and no
      2026-08 date at all**; `ls -l` gives mtime **2026-07-19 01:19**.
    - `conditional-band-and-recall-probe-214.md` — index cites **#216**, file stops at **#214**.
    - `memory-compaction-mechanics.md` — index cites **#214**, file stops at **#153**.
  - **The consequence, on the grader's own output.** `notes/_dream/_MEMORY-GRADES.json` grades
    `feedback-gate-dont-patch.md` **`AGING`** with the why-string *"…but the claim itself has not been
    touched in 34 days"* — computed at `knowledge/_gardener.py:940`, `os.path.getmtime(target)`, where
    `target` is the hook FILE. **The claim was touched yesterday; the file was not.** The grade is
    mechanically correct and substantively false, which is the worst shape a grade can take.
  - **This is the pass's one `--changed yes` row.** The AGING grade is what sent me to that file; the
    divergence is what I found. Logged honestly:
    `python3 knowledge/_gardener.py --grade-decision feedback-gate-dont-patch.md --changed yes --note "…"`
    → *"logged: decision on feedback-gate-dont-patch.md (changed=yes)"*.
- PREVALENCE: **3 of 119** linked hooks by the mechanical sweep; **1 of 3** already producing a wrong
  grade. Structural rather than widespread — but it is a *new* failure mode created by `s188-D1`, one
  cycle old, and it will grow with every index-line-only edit.
- PROPOSED: a **named re-checker** (`s129-D5` triage 2), not a rule and not a compaction. Add one
  advisory arm to `knowledge/_gardener.py --refresh`: *for each hook, if the index line names a higher
  `#NNN` than the hook file does, print it as `INDEX-AHEAD` beside the grade* — it is the same
  regex sweep run above, ~15 lines, and it fails loud rather than quietly ageing the file.
  ⛔ Explicitly NOT proposed: editing any of the three hooks (memory writes are Dave's/the ritual's),
  and NOT `GRADE_AGING_DAYS`, which stays Dave's at the B3 review.
- status: floated

---

### P3 — `s183-D1` deferred the AGING half of the B3 return-with-numbers by five cycles on the stated ground that *"`GRADE_AGING_DAYS = 30` cannot move a single entry inside a 7-day window"* — on cycle **one** it moved **13**, and AGING went 1 → 16

- EVIDENCE:
  - **The deferral, verbatim,** `knowledge/_RUNBOOK-dream-pass.md:92–96`: *"the return-with-numbers
    reports after the FIRST cycle on the COST half (which has data now) and **after FIVE cycles on the
    AGING half, because `GRADE_AGING_DAYS = 30` cannot move a single entry inside a 7-day window** —
    one cycle of AGING evidence would be no signal read as no decay."*
  - **Cycle one, measured this morning.** `python3 knowledge/_gardener.py --refresh` receipt:
    *"hooks graded : 119 FRESH 78 · **AGING 16** · STALE 0 · UNPROVABLE 25 … **grade changes : 13**
    (model-selection-by-phase.md: FRESH → AGING; feedback-route-by-default.md: FRESH → AGING;
    feedback-parallel-conductor.md: FRESH → AGING; feedback-worktree-reconcile-trail.md: FRESH →
    AGING; feedback-header-wins-over-audit.md: FRESH → AGING)"*. Pass 8's receipt (quoted at ee1) read
    *"AGING 1 … grade changes 0"*. Sidecar why-strings put the crossers at **32, 33, 35, 39 days** —
    entries that were already 25–32 days old when the window opened and crossed 30 inside it.
  - ⚠ **The honest caveat, which cuts both ways.** Part of the jump is `s188-D1` re-basing the corpus
    (index-line → hook FILE), so this is not a clean like-for-like week. But the *mechanism* the
    deferral denied — an entry crossing 30 days inside a 7-day window — is demonstrated at
    `knowledge/_gardener.py:940` and by four dated why-strings. The premise is falsified even if the
    magnitude is inflated.
  - ⚠ **And a second caveat that matters more than the first.** `age_days` is
    `(now - os.path.getmtime(hook_file)) / 86400`. AGING is a pure wall-clock function of **file edit
    recency**, monotonic and unbounded: with the memory store rarely rewritten, every FRESH entry
    becomes AGING on a fixed schedule whether or not its claim decayed, and P2 shows the mtime can be
    wrong about editing too. **Five more cycles will produce a decay curve of edit recency, not of
    claim truth** — which is a defensible thing to measure, but Dave should be told it is what he is
    being shown.
- PREVALENCE: **13 of 119** entries flipped in one cycle; **1 of 1** cycles observed since the window
  opened. The falsified premise is a single sentence in one runbook.
- PROPOSED: amend the **review plan only** — bring the AGING half's return forward from five cycles to
  **two** (`knowledge/_RUNBOOK-dream-pass.md:92–96`), so the second cycle either confirms or kills the
  `s188-D1`-re-base explanation, and carry the mtime caveat into the B3 brief §7 as a stated property
  of the grade. ⛔ `GRADE_AGING_DAYS` is UNTOUCHED and stays Dave's, exactly as `s183-D1` fenced it.
  Note this reports on a RULED row rather than re-floating pass 8's P5 (which `s183-D1` closed) — the
  line I drew is at (ff7).
- status: floated

---

### P4 — The B3 **cost half's** return date is **today** — the first cycle closed at 07:10 this morning — and the numbers are ready, unreported, and lopsided: **139 machine rows / 14,835 real tokens** against **0 human decision rows** in the window

- EVIDENCE:
  - **The return date, verbatim,** `knowledge/_RUNBOOK-dream-pass.md:92–94`: *"the return-with-numbers
    reports **after the FIRST cycle on the COST half (which has data now)**."* The window opened
    `2026-08-16T06:10:28Z` (`GRADE_WINDOW_OPEN`, generated, restated in the sidecar schema block); the
    first cycle closed at this pass's 07:10 fire. **Nothing triggers the report** — no gate, no
    check-in line, no queue row names it; it exists only in the runbook sentence above.
  - **The cost half, computed from `notes/_dream/_GRADE-DECISIONS.jsonl` (154 rows total):**
    **139 rows at ≥ window_open**, all `kind: alert`, **14,835 real tokens**, mean **106.7**
    (136 rows × 105 + 3 × 185). Per day: 08-16 **28** · 08-17 18 · 08-18 13 · 08-19 **46** · 08-20 9 ·
    08-21 10 · 08-22 14 · 08-23 1. The refresh receipt agrees: *"countable rows : 139 of 154 at >=
    window_open 2026-08-16T06:10:28Z (**alert 139 · decision 0**)"*.
  - ⚠ **A number the ruling's own model does not predict.** `s179-D1`'s cost note prices the surface at
    *"header + one alert line = 105 real tokens"* — read as a per-session cost. 139 printings across 8
    days is **~17 per day, up to 46 in one day**: the surface prints on every `_checkin.py` run, and
    the check-in is mandatory at the opener *and at every lane seam*. **The per-session mental model
    understates the real spend by roughly an order of magnitude.** 14,835 real tokens is ~9% of the
    150,929 advisory — one week, one surface.
  - **The human half is 0 by construction, and this pass is the first row.** The only `decision` row in
    the file predates the window (`at 2026-08-15T13:31:40`) and carries its own
    `drive_note: "#180 BUILD DRIVE … EXCLUDE from the B3 return-with-numbers"`. `s183-D1` made *one
    row per pass* the remedy — which caps the human dataset at **~7 rows a year against ~7,000 machine
    rows**. Three honest rows logged this morning (P2's `--changed yes`, plus `--changed no` on
    `git-push-method.md` and `conditional-band-and-recall-probe-214.md`); ⛔ none synthesised.
- PREVALENCE: **1 of 1** cycles — but it is *the* cycle the ruling named, and it is due now. Dataset
  read in full (154 rows).
- PROPOSED: put the cost half on Dave's desk at the **next** conductor's report with the four numbers
  above, and — because a return date with no re-checker is the debt `s129-D5` names — **stamp the
  runbook sentence with the generated instant it is due**, i.e. have `--refresh` print
  `⚠ RETURN DUE (cost half): first cycle closed <date>` once the window is ≥ 7 days old, so the
  obligation announces itself instead of waiting to be remembered. ⛔ Not proposed: retiring the alert
  surface, or changing what it prints — that is the review's call.
- status: floated

---

### P5 — `git-push-method.md`'s `description:` frontmatter — the field that renders in search results — still publishes *"Dave pushes via GitHub Desktop **ONLY**; never push from terminal"*, **39 days and three rulings** after that rule was retired; `s177-D1` fixed this exact class by patching **three named files** instead of gating the condition

- EVIDENCE:
  - **The stale text, verbatim,** `.auto-memory/git-push-method.md:3`: *"RULED 2026-07-05 (supersedes
    07-02 terminal-only): single-writer git — Claude commits in terminal (+ clears stale locks),
    **Dave pushes via GitHub Desktop ONLY; never push from terminal** (hangs on creds)… CLOUD-MODE lock
    fix added 2026-07-14."*
  - **What is actually in force.** `s207-D1` (`knowledge/_rulings.json`, status *"RULED #207 … memory
    hook git-push-method updated at ritual step 3"*): *"PUSH AT THE CONDUCTOR'S JUDGMENT — the
    on-Dave's-word half of the push split is retired."* Preceded by `s133-D2` (agent push, gated) and
    `s203-D1` (authority delegated to the conductor's seat). **The hook's BODY carries all of it** —
    `## ★★ 2026-08-19 (#203)` at `:102` and `## ★★ 2026-08-19 (#207)` at `:114` — and the `MEMORY.md`
    index line is correct too. **Only the `description:` is wrong**, and it is the half that renders.
  - **Nine terminal pushes at #215 alone**, per its own wrap block, plus two at #216 (`175246f`,
    `1e59273`) — so the retired sentence is contradicted by the last two sessions' commit history.
  - **The class was patched, not gated.** `s177-D1` (`says`, verbatim): *"P3 — the three stale boot
    figures in the memory corpus are corrected at the compaction pass: **boot-floor-measured-109**
    description restated…, **boot-measurable-via-usage** description drops its frozen parenthetical
    figure, **budget-vs-quota-vocabulary** replaces frozen arithmetic…"* — three named files, no
    condition. Dave's own words on this shape, `MEMORY.md:93`: *"#215 Dave: 'always real fixes never
    patches, they just get lost'"* [[feedback-gate-dont-patch]] [[conflated-fix-guarantees-recurrence]].
    This is instance **4**.
  - **A mechanical sweep of all 119 hooks** (description's newest date vs body's newest date) returns
    **12 candidates**; reading them, exactly **1** — this one — has a description that *contradicts a
    ruling in force*. `sandbox-html-rendering.md`, the only other flagged file with a correction
    keyword, has a current description (`#143`) and is clean.
  - **This is the pass's most useful `--changed no` row.** The grader calls this hook **`FRESH`** —
    *"all 3 paths named in the hook FILE resolve"*. FRESH here means *the backticks point at real
    files*, not *the claim is true*. Logged as a nil return with that note, per `s183-D1`.
- PREVALENCE: **1 of 119** hooks live today (mechanical sweep, whole store); **4th instance** of a
  class ruled on at pass 7. Thin as a count, load-bearing as a subject — it governs pushing.
- PROPOSED: two smallest steps, separable. **(a)** Restate the `description:` to the in-force rule at
  the next compaction pass, preserving the 07-05 text in the body as history (the `s177-D1` P3 shape,
  which worked). **(b)** The real fix Dave asked for: one advisory arm in
  `knowledge/_gardener.py --refresh` — *if a hook's body contains a `CORRECTED`/`SUPERSEDED`/`RETIRED`
  section dated later than every date in its own `description:`, print `DESC-BEHIND`* — the sweep
  above, ~12 lines, catching instance 5 before it is written. ⛔ Not proposed: any edit to memory by
  this pass (I write nothing outside `notes/_dream/`).
- status: floated

---

### P6 — A ruling of Dave's — `s217-D1` — exists **only** in an uncommitted working tree, no committed surface knows it happened, and the sole instrument that looks at the tree is a wrap-time **bare count** that never names what is in it (and never runs at all when a session does not wrap)

- EVIDENCE:
  - **The ruling is real and it is uncommitted.** `git diff knowledge/_rulings.json` → `1 file
    changed, 15 insertions(+)`; a set-difference of the working copy against `HEAD:knowledge/_rulings.json`
    gives **new ids: `['s217-D1']`, removed: none, total now 236**. Its text:
    *"W-93 PHOTOGRAPHY PIPELINE: HYBRID — ORIGINALS NON-REPO, COMMITTED MANIFEST + WEB-SIZED
    DERIVATIVES OF USED PHOTOS ONLY … by: Dave"*, evidence *"chat #217 2026-08-22 — Dave: 'So option
    one for now but ultimately Apollo will need an image store…'"*.
  - **No committed surface carries it.** `GOOD-MORNING.md`'s ★ LATEST is still *"2026-08-22 … **#216**
    … ONE RULING INSCRIBED: `s216-D1`"*; `_CHAIN.md:56` is `residual → #217`; `_LIVE-STATE.md`'s last
    refresh is *"2026-08-22 … #216 wrap"*. A cold reader has no way to learn `s217-D1` exists.
  - **And the first cold reader got it wrong — this pass's own dispatch.** It described the dirty tree
    as *"36 modified + 21 untracked paths (**#216 leftovers**)"*. `git status --porcelain` returns
    **37 M + 21 ??**, and **every one of the 21 untracked paths is `217`-named or `217`-produced** —
    `notes/_briefs/2026-08-22-217-{bento-tuner,foundations-bento,logos-library,photography-manifest}-brief.md`,
    `notes/_briefs/2026-08-22-217-s217-D1-entry.json`, `knowledge/_render/gen_foundations_217.py`,
    `knowledge/_render/verify_bento_tuner_217.py`, `knowledge/assets/photography-web/`. The transcript
    of #217 ends with *"say the word when you want the wrap — there's a fair amount of working tree to
    commit."* **The provenance of Dave's ruling was mis-attributed by one session inside 24 hours,
    because nothing in the repo could correct it.** ⚠ This is not a wrap failure — #217 is paused, not
    lapsed, and the wrap is Dave's word to give.
  - **What is watching, and what it can see.** `knowledge/_capture_gate.py:4146–4150` is the only
    `git status --porcelain` call in the instrument set (`_checkin.py` and `_inscribe_ruling.py` have
    none). It emits one **warn**: `f"git: {n} uncommitted path(s) — commit before close (step 5)"`.
    A bare integer — it cannot distinguish *58 paths, one of which is a Dave ruling* from *58 paths of
    known dirty-at-baseline instrumentation appends* (pass 6's P2 population, still floated). And it
    lives in `--wrap`, the one moment an unwrapped session never reaches [[a-crash-is-not-a-fail]].
  - ⚠ **Why the exposure is not theoretical here.** `knowledge/_RUNBOOK-git-commit.md` § Gotchas:
    *"★ `git checkout -- <path>` CANNOT RESTORE A FILE ON THIS MOUNT (measured #139)."* On this mount
    a mistaken clean is not reversible.
- PREVALENCE: **1 of 1** — live at this moment, and the mis-attribution is **2 of 2** cold readers who
  touched it (the dispatch, and me before I ran the diff). Thin as a count; the receipts are exact and
  the window is open right now.
- PROPOSED: the **generate-it** triage. Give the existing warn a content-aware sibling in
  `knowledge/_capture_gate.py` and, more usefully, in `knowledge/_checkin.py` (which runs mid-window,
  where the fix is cheap — the #92 earlier-gate argument applied to a different term): *if
  `knowledge/_rulings.json` is dirty, name it and print the ruling ids the working copy has that
  `HEAD` does not* — the exact set-difference run above, ~20 lines, no new file, no ruling touched.
  ⛔ Not proposed by this pass, and deliberately: committing anything, staging anything, or touching
  `s217-D1`. **The conductor may wish to tell Dave the ruling is uncommitted before anything else
  happens to that tree.**
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(ff1) The ~190,000 advisory contradiction is FOUND, CARRIED and correctly refused — do not report
  it as a finding.** Three surfaces disagree today: `MEMORY.md:8` says *"s214-D4 n=2 MET — ~190K
  advisory ARMS at #216 OPENER"*, `_LIVE-STATE.md:84` says *"THE ADVISORY LINE IS RE-DERIVED AND
  STAGED, **NOT IN FORCE** … ⛔ `150,929` still stands"*, and `_gauge_tokens.py:144/:164` still name
  150,929. I had this half-written as a proposal before reading `_CHAIN.md:56`, which carries it as
  **new carry ⑤**, verbatim: *"⛔ **THE ~190,000 ADVISORY IS ANNOUNCED BUT UNINSCRIBED, AND THE RECORD
  STILL SAYS 150,929 [NEW — 0]** … This seat neither armed nor discharged it — a wrap sub moving an
  advisory would be laundering a premise into a ruling. #217's opener inscribes it or lets it lapse."*
  That is the discipline working exactly as [[feedback-dont-launder-a-premise-into-a-ruling]] rules.
  **A ruling awaiting Dave, not a record defect.**
- **(ff2) The CI read-back queue is owed, aged and homed — not a dropped loop.** #213 (*"the two owed
  CI read-backs"*), #214 (*"owed to the #215 opener, declared"*), #215, #216 (*"no auth from any seat
  today — covers both pushes"*). It is carried at `_CHAIN.md:56` as carries ⑥ and ⑦ with age brackets,
  and it **has** been discharged at least once (**CI #413 GREEN on `e645df2`**, read back by the
  conductor at #215, quoted in four places). An obligation that is met sometimes and carried with its
  age the rest of the time is the system working; `#401/#402` remain the aged head of the queue.
- **(ff3) The lane register still says charts while the forward title says logos + photography — and
  the wrap was RIGHT not to move it.** `_CHAIN.md:56` carry ⑨ names it in full and gives the reason:
  `knowledge/_lanes.json` is checked against §C·1 by a BLOCKING gate, so repointing it from a wrap
  sub's seat would be editing Dave's standing worklist. Named, owned, deliberately unrepaired.
- **(ff4) The dirty tree is DECLARED, and I neither cleaned, staged nor reverted any of it.** 37
  modified + 21 untracked at open. The three instrumentation appends among them
  (`notes/_REHEARSAL-LOG.jsonl`, `knowledge/_graph-mark-observations.jsonl`,
  `notes/_dream/_GRADE-DECISIONS.jsonl`) are **pass 6's P2, still floated** — referenced, not
  re-floated. ⛔ I did not touch `.git/index.lock` (the known unlink wart, [[git-lock-mv-not-rm]]).
- **(ff5) Pass 8's P1 was enacted and the enactment is visible and large.** `s188-D1` moved the
  grading unit to the hook FILE; this pass's receipt reads *"probe source : hook FILE 94 · index-line
  FALLBACK 25"*, and UNPROVABLE fell **111 → 25** while FRESH rose **12 → 78**. Recorded as evidence
  that the fix landed. P2 above is a *new* consequence of that move, not a re-float of P1.
- **(ff6) What this pass wrote, stated plainly.** **Three files, all mandated by the dispatch and the
  runbook's § B3, and nothing else.** (1) this proposals file — the pass's only *finding* output;
  (2) `notes/_dream/_MEMORY-GRADES.json`, restamped by the mandated
  `python3 knowledge/_gardener.py --refresh`; (3) `notes/_dream/_GRADE-DECISIONS.jsonl`, appended with
  **one `--refresh` alert row + three honest `--grade-decision` rows** (1 × `changed=yes`,
  2 × `changed=no`; ⛔ none synthesised, `s183-D1`). *(Pass 8's ee6 declared a tension between "only
  write the proposals file" and "run the refresh arm"; this pass's dispatch resolved it mechanically
  in advance — the restamp and the decision rows are named as mandated instrument outputs, so there is
  no tension left to declare.)* **No memory file, no canon, no ledger, no git operation of any kind.**
- **(ff7) Out of scope by standing exclusion, and where I drew the line.** Dream-lane mechanics remain
  barred (cc6/dd7/ee7): I did **not** float the cadence, the conductor sequence, or the lane's §🔀 row.
  ⚠ **P3 and P4 sit nearest that line.** Their *subject* is the B3 review plan — a dataset and a return
  date that `s182-D1`/`s183-D1` bind Dave to review — not the lane's schedule; P4 reports on the
  window the lane's fire *opened*, which is ground truth, not a proposal about firing. ⚠ **P3 also
  reports on a RULED row** (`s183-D1`'s amended return date). I am not re-floating pass 8's P5, which
  that ruling closed; I am reporting that the ruled deferral's own stated premise is falsified by the
  first cycle of data it was waiting for. If Dave reads that as re-opening settled ground, the honest
  answer is to drop P3 and keep the mtime caveat.

---

## Method

**Read, in the dreamer spec's order.** `MEMORY.md` (index, hooks only — 119 linked entries) ·
`GOOD-MORNING.md` header + ★ LATEST banner (skimmed under truncation; the file's lines are
single-paragraph and exceed one tool result) · `_LIVE-STATE.md` header, § OPEN and the `#216` delta
zone · `_CHAIN.md` (`:34`–`:95`, including the whole `residual → #217` line) · `.claude/agents/dreamer.md`
in full · `knowledge/_RUNBOOK-dream-pass.md` in full, § "The B3 refresh arm" twice ·
`notes/_MEMENTO-DECISIONS.md` heading/RULED spine · **every prior proposals file's checked-clear list
in full** (pass 3's prose block, (q)–(w), (x)–(bb), (cc1)–(cc6), (dd1)–(dd7), (ee1)–(ee7)) and every
prior `### P<n>` heading, so that floated-but-unruled proposals could be referenced rather than
re-floated.

**Transcripts: 15 read** (Shape A, `list_sessions` → `read_transcript`), #217 back to #203 — five in
detail (#217, #216, #215, #214, #213), the rest by title and closing report. **Fidelity ceiling, and
where it bound:** tool calls appear as names only, with no arguments or results, so **not one figure in
this file comes from a transcript**. Transcripts were used only to locate claims; every number here was
re-derived against the repo. Where the ceiling bit hardest: I could not see *which* files #217 wrote,
only that it wrote some — P6's file list comes from `git status` and the `217`-naming, not from the
session.

**Live-tree check before measuring:** `git log --oneline -1` → `1e59273 #216`, matching the dispatch's
stated HEAD.

**Commands a conductor can re-run, verbatim** (all read-only except the two mandated arms):
- `git log --oneline -1` → `1e59273 #216`
- `git status --porcelain | awk '{print $1}' | sort | uniq -c` → `21 ??`, `37 M`
- `git diff --stat knowledge/_rulings.json` → `1 file changed, 15 insertions(+)`; set-difference vs
  `git show HEAD:knowledge/_rulings.json` → `new ids: ['s217-D1']`, `total now 236`
- `grep -n "pre-flight #" notes/_GAUGE-LOG.md | grep -c "NOT CAPTURED"` → `96`; last non-`NOT CAPTURED`
  is `:1862` (#189); `:1871`…`:2209` is the unbroken run
- `sed -n '2209p;2213p' notes/_GAUGE-LOG.md` → the refusal and the conductor's measured brief-cut,
  four lines apart
- `python3 knowledge/_gardener.py --refresh` → `119 hooks · FRESH 78 · AGING 16 · STALE 0 ·
  UNPROVABLE 25 · grade changes 13 · probe source hook FILE 94 / index-line FALLBACK 25 ·
  countable rows 139 of 154 at >= 2026-08-16T06:10:28Z (alert 139 · decision 0)`
- in-window cost, over `notes/_dream/_GRADE-DECISIONS.jsonl`: `139` rows, `14,835` tokens, mean `106.7`
- `sed -n '940p' knowledge/_gardener.py` → `age_days = (now - os.path.getmtime(target)) / 86400.0`
- `sed -n '4146,4150p' knowledge/_capture_gate.py` → the bare-count `git:` warn
- `sed -n '3p' .auto-memory/git-push-method.md` → the retired `description:`
- `ls -l .auto-memory/feedback-gate-dont-patch.md` → mtime `2026-07-19 01:19`, vs `MEMORY.md:93`
  citing `#215`
- the two mechanical memory sweeps in P2 and P5 are ~15-line Python over `.auto-memory/`, reproduced
  in the proposals above in enough detail to retype.

**Nothing here self-promotes.** Six proposals, all `status: floated`; promotion is Dave's alone.
