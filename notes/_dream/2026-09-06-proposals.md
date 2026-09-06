# Dream pass 11 — floated proposals

provenance: `77f284ff-44c3-44a6-a11e-be7b8bd7fcf3` · 2026-09-06
status: floated

*I PROPOSE ONLY. Nothing here self-promotes; promotion is Dave's alone on reading this file
(derivation-governance). Every RULED row in `knowledge/_rulings.json` / `notes/_MEMENTO-DECISIONS.md`
and every checked-clear item at the end of EVERY prior proposals file — pass 1's (a)–(d), pass 2's
(a)–(f), pass 3's (a)–(e), pass 4's (n),(p),(q)–(w), pass 5's (x)–(bb), pass 6's (cc1)–(cc6), pass 7's
(dd1)–(dd7), pass 8's (ee1)–(ee7), pass 9's (ff1)–(ff7), pass 10's (gg1)–(gg9) — was read before
hunting. **Proposals from passes 6–10 that are still FLOATED are referenced where new evidence bears
on them, never re-floated** (see hh1, hh2, hh3). Standing exclusion held: dream-lane mechanics
(cadence, conductor sequence, the lane's §🔀 row, `_dream/` gating) are barred from floating —
cc6/dd7/ee7/ff7/gg9 precedent, see (hh8).*

★ **Shape A (Cowork), scheduled Sunday 07:10 fire, ON TIME** (pass 10 = 2026-08-30). Date from the
host env line, corroborated mechanically by `notes/_dream/_MEMORY-GRADES.json`
`"refreshed_at": "2026-09-06T07:16:57"` — the conductor's B3 refresh arm, run before I was dispatched.

⚠ **ONE CEILING TO DECLARE UP FRONT, because it shaped what I could measure.** This seat has **no
Bash** (the dreamer spec's tool list is Read · Grep · Glob · Write · ToolSearch). Passes 9 and 10
derived their figures with `python3` one-liners; **every number below is derived with `Grep` counts
and `Read`, and every one is reproducible with a single `rg` invocation quoted in § Method.** Where
that bound me is stated at (hh6) — in particular `_CARRIES.md` and `knowledge/_REVIEW-SIGNOFF.md`
hold single lines long enough that `Grep` refuses to print them, so I made no claim about either.

Ranked by prevalence, highest first.

---

### P1 — #242's memory-index diet cut the B3 grader's population from **122 hooks to 33** and nothing declared it: the instrument that answers *"is any starred memory claim stale?"* now reads **33 of the 140 hooks Dave's own store still names**, and the 107 it stopped reading sit one file away, in the exact syntax its parser already accepts

- EVIDENCE:
  - **The population, both ends, from the instrument's own output.** `notes/_dream/_MEMORY-GRADES.json`
    today: `"hooks_seen": 33`, `"counts": {"FRESH": 23, "AGING": 3, "STALE": 3, "UNPROVABLE": 4}`
    (`:30`–`:36`). Pass 10's own receipt, quoted at its (gg5): *"FRESH 63 · AGING 33 · STALE 0 ·
    UNPROVABLE 26 over **122** hooks"*. **122 → 33 in one cycle, a 73% cut.**
  - **Why.** `knowledge/_gardener.py::parse_memory_index` (`:702`–`:730`) builds the whole graded
    population from lines of `MEMORY.md` matching `_HOOK_RE` (`:695`). `MEMORY.md` was reduced to a
    ⛔/★★★-tier STUB at #242 on Dave's *"yes"*; it now carries **33** such lines — counted, not
    recalled. **Nothing else is a source.** There is no directory walk, no orphan arm.
  - **The 107 are not lost — they are one file away, and they are already gradeable.**
    `MEMORY.md:2` names their home in its own words: *"EVERY other hook, verbatim, by name:
    [hook-overflow-2026-09-03-242]… read it when a hook is NAMED, never at boot"*. That file carries
    **107 lines in the exact `_HOOK_RE` shape** (`^-\s+\[title\](slug.md)`). The grader could read it
    tomorrow without a regex change.
  - ⛔ **And the cut is already hiding a real STALE, which is the receipt that makes this more than
    bookkeeping.** Commit `7f8801f` (#241) deleted `knowledge/_measure_tokenizer.py` — verified
    absent: `Glob knowledge/_measure_tokenizer*` → no files. **Four** hook files in the store name it.
    **Three** are inside the 33 and all three graded **STALE** this morning
    (`diet-measured-and-ritual-cut-241.md`, `tape-unit-is-not-real-tokens.md`,
    `retrieval-default-hides-the-ruling.md` — `_MEMORY-GRADES.json:207`, `:512`, `:553`). The
    **fourth**, `tape-is-openai-not-claude.md`, is outside the 33 **and outside the overflow file too**,
    and its body says: *"Instrument: `knowledge/_measure_tokenizer.py` — **RE-RUN IT, never quote this
    number**"*. **A hook that orders a re-run of a deleted file, graded by nothing.**
  - **The blast radius was declared for the sibling cut and missed for this one.** #241's own lane
    report named the `_measure_tokenizer` consequence exactly right —
    `notes/_subreports/2026-09-02-241-lane-E-diet-apply.md:297`: *"D4's one non-import consumer is real
    and will register … **That grade will drop at the next dream pass.**"* — and `_capture_gate.py:524`
    repeats it in code. The memory-stub row of the same diet table
    (`notes/_subreports/2026-09-03-242-lane-F-boot-offload.md:47`) declares only the *retrieval*
    consequence: *"tier-B/C hooks stop firing **UNPROMPTED**; they survive only as look-up-BY-NAME"*.
    **True, and not the whole cost:** they also stopped being *graded*. No `_DECISION-HISTORY` file for
    #242 or #243 mentions the grader at all (grepped: 0 hits for `gardener|MEMORY-GRADES|grader`).
  - **The sidecar even has a slot for this warning and it is empty.** `_MEMORY-GRADES.json:5` carries a
    hand-written incomparability notice for the *previous* re-base: *"⚠ The counts in this file after
    2026-08-16 are NOT comparable with the ones before it."* There is **no such line for #242**, so the
    B3 return-with-numbers dataset Dave is bound to review now spans two silent re-bases, one declared.
  - ⚠ **The instrument refuses an EMPTY population and waves through a SHRUNKEN one.**
    `_gardener.py:706`–`:710` blocks when the index is missing, with the reason spelled out: *"An empty
    grade set here would read as 'nothing is stale', which is the exact false-confidence B3 exists to
    remove."* **The same sentence is true of a 73% cut** and no arm asserts it.
- PREVALENCE: **107 of 140** hooks the store still names are ungraded (33 graded + 107 in the overflow
  = 140); **1 of 1** graded populations affected; **1 of 4** files carrying a provably-dead path is
  invisible to the grader today. Whole index and whole overflow read mechanically, not sampled.
- PROPOSED: the **named re-checker** triage (`s129-D5` #2), smallest form first. **(a)** One advisory
  arm in `knowledge/_gardener.py --refresh`: *print `POPULATION CHANGED: N hooks this run vs M last
  run` whenever `hooks_seen` moves by more than a threshold, and refuse silently succeeding on a
  shrink* — the same posture `:706` already takes for zero, applied to the slope. **(b)** Separately,
  and Dave's call because it changes what B3 measures: have `parse_memory_index` also read the
  overflow file `MEMORY.md:2` already names, so the graded set matches the store rather than the boot
  diet. ⛔ Explicitly NOT proposed: reverting the #242 stub (it is Dave's ruling and it bought real
  boot tokens), editing any hook, or touching `GRADE_AGING_DAYS` / the alert surface — both stay
  Dave's at the B3 review.
- status: floated

---

### P2 — The same parser grades **one hook per line** and drops any second link on that line **without declaring it**, four lines above a comment that promises the opposite: **5 starred hooks in the live index are ungraded and unlisted**, and the same shape would drop **13 more** the moment P1's remedy lands

- EVIDENCE:
  - **The regex, verbatim,** `knowledge/_gardener.py:695`:
    `_HOOK_RE = re.compile(r"^-\s+\[(?P<title>[^\]]+)\]\((?P<slug>[^)\s]+\.md)\)(?P<rest>.*)$")` —
    `.match()`, one capture, and everything after the first link falls into `rest`, which is used for
    nothing. `parse_memory_index` (`:716`–`:719`) appends to `unlinked` **only when the line matches
    nothing at all**, with the comment *"# DECLARED, never silently dropped"*.
  - **A line with two hooks matches, so it is never declared — and there are five of them.**
    `MEMORY.md` lines **16, 17, 19, 21, 27**. Counted mechanically: **33** lines match `_HOOK_RE`;
    **5** of those 33 carry a second `[…](….md)` on the same line.
  - **The five hooks that are consequently ungraded, by name** — each verified absent from the 33
    `"id"` fields in `notes/_dream/_MEMORY-GRADES.json`:
    `boot-floor-measured-109.md` (line 16, *"★★★ Boot band = s208-D1 constant"*) ·
    `fill-reader-enacted-91.md` (17, *"★★★ FILL ≠ THROUGHPUT"*) ·
    `do-not-rule-list-cannot-fence-a-generator.md` (19, ⛔★★) ·
    `delegated-wrap-rename-relay.md` (21, ⛔★) ·
    `refusal-names-the-first-obstacle.md` (27, ★★★).
    **Every one is starred or blocked**, i.e. every one is in the exact subset `s179-D1` scoped alerts
    to. Four of the five are named in the boot-critical band/gauge cluster.
  - **And the declaration that would have caught it names the wrong three lines.**
    `_MEMORY-GRADES.json:37`–`:41`, `"unlinked_index_lines"`, lists lines **1, 2 and 36** — the prose
    lines. The five half-read lines appear nowhere. So the file's honest-register discipline is intact
    for the case the author thought of and blind to the case they did not.
  - **The scale if P1 is fixed.** The overflow file carries **107** `_HOOK_RE` lines, of which **13**
    carry a second link. Restoring the population without fixing the regex would restore 107 of 120
    and drop 13 silently — instance 2 of a class fixed at instance 1
    [[conflated-fix-guarantees-recurrence]]. **Fix them in one motion or the second fix gets lost.**
- PREVALENCE: **5 of 38** hook references in the live index (33 first-on-line + 5 second-on-line) are
  read by nothing; **5 of 5** are starred; **13 more** latent in the overflow (**18 of 145** across
  both files). Both files read whole.
- PROPOSED: a **one-line change with an arm**, not a convention. Replace `.match()` with a
  `finditer` over the line in `parse_memory_index` (`knowledge/_gardener.py:716`) so every link on a
  line becomes a hook — **and add one selftest arm that plants a two-link index line and asserts two
  graded entries**, which is the arm that would have caught this
  [[mutation-tests-the-clause-not-the-feature]]. ⛔ Explicitly NOT proposed: reformatting `MEMORY.md`
  onto one-hook-per-line (that is Dave's store and the ⛔/★★★ stub's line budget is his), or changing
  `ALERT_MARKS` / the alert surface.
- status: floated

---

### P3 — A delegated wrap sub declared an epistemic limit of **its own seat** as a property of the artefact — *"`_tools/` … provenance unknown"* — and the record has since published that phrase **11 times across 7 surfaces including the generated retrieval index**, while the session **two before** names the directory, its build command and its purpose in plain chat

- EVIDENCE:
  - **The claim, as it is published.** `_LIVE-STATE.md:14`: *"Strays DECLARED, not committed: `_tools/`
    (untracked at the opener, **provenance unknown**, 92 KB)"*; restated at `:76`:
    *"**`_tools/` NOT committed — 92 KB, untracked at the opener, provenance unknown, a stray**"*.
  - **Where it has spread, counted:** **11 occurrences across 7 files** —
    `_LIVE-STATE.md` ×2 · `_CHAIN.md:76` · `GOOD-MORNING.md:484` · `_CARRIES.md:52` ·
    `notes/_briefs/2026-09-05-247-delegated-wrap-brief.md:20` · `knowledge/_memento-index.json` ×5.
    The index copy means **retrieval will serve it**, which is the surface
    [[read-chain-is-where-staleness-is-free]] names as the worst home for a claim that ages.
  - ⛔ **The provenance is in the record, one session earlier.** #246's transcript
    (*"Apollo - #246: the library dictates…"*) has this seat writing, in chat, to Dave:
    *"cd ~/Documents/Claude/Projects/UX-design/_tools/Caffeinate — chmod +x build.sh && ./build.sh &&
    open Caffeinate.app"*, then *"Paste any error back and **I'll fix the source**"*, then handling
    `xcode-select` follow-ups. The artefact corroborates it: `_tools/Caffeinate/main.swift:1`–`:2` is
    *"Caffeinate — a one-file macOS menu bar toggle for /usr/bin/caffeinate. Build: cd _tools/Caffeinate
    && ./build.sh"* — the same two-line instruction. **This is not an unattributable stray; it is #246's
    working file for Dave's own machine.**
  - **The mechanism, and it is structural rather than careless.** The declaration was written by #247's
    **delegated wrap sub**, whose brief is `notes/_briefs/2026-09-05-247-delegated-wrap-brief.md`. A
    wrap sub cannot see the conductor's chat, let alone the *previous* session's chat — the same
    ceiling `notes/_GAUGE-LOG.md` has been refusing the pre-flight boot term over for 27+ sessions
    (pass 9's P1, referenced at hh1, not re-floated). **The honest form is "provenance not established
    from this seat"; the form that got inscribed is "provenance unknown", which is a claim about the
    world.** That is the [[feedback-dont-launder-a-premise-into-a-ruling]] shape one notch down: a
    seat's blind spot laundered into a repo fact.
  - ⚠ **Honest caveat, stated rather than smoothed.** The Shape-A ceiling means I can see #246's chat
    but not its tool arguments, so I cannot prove the *bytes* were written by #246 rather than by Dave
    on his side during that session. **What is proven is the negative that matters:** the record
    contains a specific, dated, path-exact account of what `_tools/Caffeinate` is and who was working
    on it, so *"provenance unknown"* is false as published, whichever hand wrote the file.
- PREVALENCE: **11 sites across 7 surfaces**, carried **3 consecutive sessions** (#246 → #247 → #248);
  **1 of 3** declared strays affected (`knowledge/_screen-gate/dashboard.md` and the `.git/index.lock`
  are declared without a provenance claim, correctly). Grep run over the whole repo.
- PROPOSED: two smallest steps, separable. **(a)** At the next 2c/2d roll, restate the six live copies
  as *"provenance: #246 (Caffeinate menu-bar toggle, `main.swift:1`) — untracked by choice, 92 KB"*,
  and leave the archived copies as dated history (ADR-0017). **(b)** The re-checker, and it is the one
  worth having: **one line in the delegated-wrap brief template**
  (`knowledge/_RUNBOOK-capture-ritual.md`, already the home of the `s214-D5` hand-over field) —
  *a stray may be declared UNCOMMITTED from any seat, but it may only be declared UNKNOWN after a
  `grep -rn "<path>"` over `notes/`, `_DECISION-HISTORY/` and the last two sessions' briefs returns
  nothing; otherwise write "not established from this seat".* ⛔ Not proposed: committing `_tools/`,
  deleting it, or `.gitignore`-ing it — what happens to Dave's own build tool is Dave's.
- status: floated

---

### P4 — `knowledge/_SCREEN-GATE.md` says *"this index is rebuilt from that directory on every run"* and *"9 subject(s) on record"*; the directory holds **10**, and the missing one is `dashboard.md` — the gate record for the project's **current declared focus**

- EVIDENCE:
  - **The index's own promise,** `knowledge/_SCREEN-GATE.md:3`–`:4`: *"One file per subject under
    `_screen-gate/`; this index is rebuilt from that directory on every run, so gating one screen never
    erases another (#230 T5)."* Its last line (`:16`) is *"9 subject(s) on record."* and it lists 9.
  - **The directory holds 10.** `Glob knowledge/_screen-gate/*` returns
    `canon-gallery.canon.md` · `international-banking-dashboard.regen-v1.md` ·
    `international-banking-dashboard.regen-v2-receipt.md` · `nio-dash-console-v1.canon.md` ·
    `nio-dash-console-v2.canon.md` · `payments-journey.canon.md` · `sme-payments-desktop.canon.md` ·
    `sme-payments-swiss.canon.md` · `sme-payments.canon.md` · **`dashboard.md`**. The first nine are the
    nine rows; `dashboard.md` appears in no row.
  - **The rebuilder is real and it is a build step.** `knowledge/_validate_screen.py::write_index`
    (`:134`–`:147`) globs `_screen-gate/*.md` and rewrites the index — *"Rebuild `_SCREEN-GATE.md` from
    what is ON DISK — the whole population, not this run's"* — and `_validate_screen.py` is wired at
    `knowledge/_build_all.py:292`. So the index is not wrong by design; **it is simply older than the
    subject**, and `_build_all.py` is fenced from running in this sandbox (`_CHAIN.md` STATE line), so
    nothing has re-run it since `dashboard.md` appeared.
  - ⚠ **The half that makes it worth a proposal rather than a chore, and I mark the CI leg as
    inference because I cannot run CI from here.** `dashboard.md` is **untracked** (declared in the
    #247 wrap: *"NOT staged by the brief's fence: `_tools/` (92 KB) · `knowledge/_screen-gate/dashboard.md`
    (7.9 KB)"*, `notes/_subreports/2026-09-05-247-wrap.md:111`). A tracked generated file whose content
    is derived from a directory containing an untracked member **cannot agree between this machine and a
    fresh clone**: locally the next build writes 10 rows, in CI it writes 9 and matches. The index is
    therefore green in the only place that checks it and stale in the only place that is read.
  - **Subject matters.** `MEMORY.md:4` records #246's focus verbatim: *"#246 DASHBOARDS ONE-SHOTABLE IS
    THE FOCUS"*. The one subject the composed-screen gate's index does not name is the one the last
    three sessions were about.
- PREVALENCE: **1 of 10** subjects missing; **1 of 1** index; **2 sessions** (#247, #248) with the
  subject file on disk and unnamed. Thin as a count — floated because the mechanism (a tracked build
  output derived from untracked input) is general and the file is the gate's public record.
- PROPOSED: the smallest step is **not** "re-run the gate" (it needs a render sandbox and the fenced
  build). It is **(a)** decide `dashboard.md`'s status — commit it as a subject, or move it out of
  `_screen-gate/` if it is a draft; either resolves the divergence at the source, and both are Dave's
  because they say whether dashboards are permanent gate subjects (the open question already recorded
  at `notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/build_review.py:423`). **(b)** The
  re-checker: one arm in `write_index()` that refuses when a file it is about to index is untracked —
  *"a generated index may not be built from state a clone cannot see"* — ~5 lines, no new file.
  ⛔ Not proposed: hand-editing `_SCREEN-GATE.md` (it is generated), or running `_build_all.py`.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(hh1) Pass 9's P1, P4, P5 and pass 10's P1–P4 are all still FLOATED and are referenced above,
  never re-floated.** Specifically: the `⛔ NOT CAPTURED` pre-flight streak (pass 9 P1) is cited in P3
  only as the *shape* of a seat-limit inscribed as a fact; the B3 cost half (pass 9 P4) is the dataset
  P1 talks about and I did **not** re-float it — I note only, as ground truth, that the conductor's
  refresh receipt this morning reads **283 countable rows of 298 (alert 279 · decision 4)**, i.e. the
  machine:human ratio pass 9 P4 named has gone from 139:0 to 279:4; and pass 10's P1 (sub-report
  contract parses) is the class the dispatch's *"twelve #248 sub-reports uncited / no parseable COUNTS
  / REPLAY-THESE / RSQ"* finding belongs to — **same class, same remedy, not new in kind, not
  re-floated.**
- **(hh2) Pass 10's P3 is UNCHANGED in substance and the new evidence STRENGTHENS it without being a
  new finding.** `_CHAIN.md` STATE now reads *"BUILD VERDICT: **75 of 142** steps green (#62,
  `18c7789`) — **67** steps have NEVER been in a green verdict"*, against pass 10's quoted *75 of 140 …
  65*. **The two COUNTS regenerated (140 → 142, 65 → 67) and the ANCHOR did not** — which is precisely
  P3's argument that `VERDICT_SHA` is the un-regenerated half. Reported as corroboration of a floated
  proposal; **not re-floated**.
- **(hh3) The uncommitted `s248-D1…D4` are pass 9's P6 class, and the class is OPEN-BY-INSTANCE, not
  re-opened by me.** Verified: `knowledge/_rulings.json` carries `"id": "s248-D1"` … `"s248-D4"` at
  `:6157`, `:6173`, `:6189`, `:6206` in the working tree, and the dispatch declares the file modified
  and uncommitted. Pass 10's (gg1) closed the *#217 instance*; the *proposal* — a content-aware sibling
  to the bare `git: N uncommitted path(s)` warn, in `_checkin.py` where it runs mid-window — was never
  ruled and is unchanged. **This is instance 2 of exactly the exposure it predicted, which is evidence
  for it, not a new proposal.** Same for `knowledge/_screen-gate/dashboard.md` and `_tools/`.
- **(hh4) I nearly published a false finding about DO-FIRST item 18, and the correction is the
  record.** `_CHAIN.md`'s presence index names 28 items and **18 is absent from the sequence**
  (`0b,0c,0d,1…17,19…26`), while #247's residual ⑤ NOT DONE lists *"cold test · `[18]` · 4px audit"* —
  which reads as an owed DO-FIRST item that the index's *"Every open item is named"* claim has lost.
  **It is not.** The index is faithful: `GOOD-MORNING.md` carries exactly **28** lines matching
  `DOFIRST_ITEM_RE` (`^>\s*\*\*(\d+[a-z]?)\.`) and **zero** matching `^> \*\*18\.`; the old item 18
  (*"MEMORY COMPACTION OWED (#104)"*) is archived at `_GM-ARCHIVE.md:3358`. `[18]` in the residual is a
  **DP principle number**, proved by `notes/_briefs/2026-09-05-247-delegated-wrap-brief.md:18`:
  *"NEXT: **W2 — Bento rhythm** (DP-14 15 16 **18**…)"*. Two identical tokens, two vocabularies
  [[vocabulary-collision-switch-202]]. Recorded so the next pass does not spend the same hour.
- **(hh5) `_measure_tokenizer.py`'s deletion left ZERO executable orphans — the #241 cut was clean, and
  I checked because P1 depends on the opposite half.** `grep -rn "_measure_tokenizer"` returns **116
  hits across 31 files** and **not one is an import or a call**: `knowledge/_capture_gate.py:513`–`:529`
  is the retired registry entry (comment), `:5825` a comment, `knowledge/_governs.py:28` and
  `apollo-spider/gumdrop/_governs.py:28` quote it as the cautionary tale, the rest is `notes/`,
  archives, `_rulings.json` and the retrieval index. The probe #241 named for exactly this
  (`_capture_gate.py:520`, *"THE PROBE, NAMED, so the deletion is falsifiable"*) **passes today**. The
  memory-hook fallout is P1's subject; the code is clean.
- **(hh6) Where the no-Bash ceiling bound, stated rather than smoothed.** `Grep` refuses to print lines
  above its length guard, and three surfaces are written as single enormous lines: `_CARRIES.md`
  (4.5 MB; the `residual → #248` carry list is one line), `knowledge/_REVIEW-SIGNOFF.md` (its 2026-09
  rows) and much of `knowledge/_memento-index.json`. **I therefore made no claim about the carry
  list's contents, the sign-off tracker's freshness, or the retrieval index's rows** — bounded-context
  `-o` patterns recovered the `provenance unknown` sites in P3, and nothing further. A conductor with a
  shell should re-run P3's count as `rg -c "provenance unknown"` and P1's as
  `rg -c '^-\s+\[[^]]+\]\([^) ]+\.md\)' MEMORY.md hook-overflow-2026-09-03-242.md`.
- **(hh7) What this pass wrote, stated plainly. ONE file — this one.** The conductor ran the B3 refresh
  arm before I was dispatched (`"refreshed_at": "2026-09-06T07:16:57"`), so ee6's tension is resolved
  mechanically and there is none left to declare. I logged **no** `--grade-decision` rows, ran **no**
  `_gardener.py` arm, ran **no** `_checkin.py`, and performed **no** git operation of any kind — this
  seat has no Bash, so that is a property of the tool set, not a promise. The tree is DIRTY at baseline
  with #248's unwrapped session (5 modified + 4 untracked groups, exactly as the dispatch declared) and
  **I neither cleaned, staged nor reverted any of it**; I did not touch `.git/index.lock`
  [[git-lock-mv-not-rm]]. No memory file, no canon, no ledger, no `notes/` file but this one.
- **(hh8) Out of scope by standing exclusion, and where I drew the line.** Dream-lane mechanics remain
  barred (cc6/dd7/ee7/ff7/gg9): I did **not** float the cadence, the conductor sequence, the lane's §🔀
  row, or `_dream/` gating. ⚠ **P1 and P2 sit nearest that line and I judge them clear of it, but the
  judgment is Dave's, so here is the reasoning:** their subject is `knowledge/_gardener.py`, the memory
  grader, and the B3 review dataset — an instrument and a dataset that `s179-D1`/`s182-D1`/`s183-D1`
  bind Dave to review. The dream lane is the thing that *fires* the refresh arm; it is not the arm.
  ⚠ **If Dave reads P1(b) — "grade the overflow too" — as re-scoping the B3 review rather than
  repairing it, the honest answer is to keep P1(a), the population alarm, and drop P1(b).**

---

## Method

**Read, in the dreamer spec's order.** `.claude/agents/dreamer.md` in full, first ·
`MEMORY.md` in full (37 lines, the #242 ⛔/★★★ stub) · `_CHAIN.md:1`–`:60` (header, STATE block,
★ LATEST banner, `residual → #248` pointer, presence index) · `_LIVE-STATE.md` and `GOOD-MORNING.md`
by bounded pattern only — see (hh6) · `notes/_dream/_MEMORY-GRADES.json` (header + all 33 entry ids +
the three STALE why-strings) · **pass 9's and pass 10's proposals files in full, and every prior pass's
`### P<n>` headings and checked-clear bullets** by a single ripgrep sweep over `notes/_dream/*.md`
(pass 1's (a)–(d) … pass 8's (ee1)–(ee7)), so floated-but-unruled proposals could be referenced rather
than re-floated · `knowledge/_gardener.py` §§ constants, `parse_memory_index`, `_HOOK_RE`, the alert
rule · `knowledge/_capture_gate.py:504`–`:544` (the MEASURERS registry + the retired entry),
`:1527`–`:1610` and `:3857`–`:3869` (the DO-FIRST presence index and its gate) ·
`knowledge/_validate_screen.py:118`–`:162` · `knowledge/_SCREEN-GATE.md` in full ·
`notes/_subreports/2026-09-02-241-lane-E-diet-apply.md` § (d) and
`notes/_subreports/2026-09-03-242-lane-F-boot-offload.md` § the diet table ·
`hook-overflow-2026-09-03-242.md` and `tape-is-openai-not-claude.md` in the memory store.

**Transcripts: 15 in the window, 3 read in detail, 12 by title.** Shape A, `list_sessions` →
`read_transcript`, covering **#248 back to #234**. Read in detail: **#248** (`local_1e494a0d`),
**#247** (`local_dde85b56`), **#246** (`local_99430bc7`). The remaining twelve (#245 … #234) were taken
by title and closing report only, and **no figure in this file comes from any of them**.
⛔ **Skipped and declared:** none — pass 10's own session is outside the 15-session window, so the
circularity that forced pass 10's skip did not arise.
**Fidelity ceiling, and where it bit:** tool calls appear as names with no arguments or results, so
**not one number in this file comes from a transcript**. Transcripts located claims; every figure was
re-derived against the repo. Where it bit hardest is **P3** — #246's chat proves the record *contains*
`_tools/Caffeinate`'s account, but the ceiling means I cannot see which tool wrote the bytes, which is
why P3's caveat is stated in the proposal rather than in this section.

**Baseline check before measuring** (read-only, and the only kind available to this seat):
`Glob notes/_dream/*.md` → newest was `2026-08-30-proposals.md`, so this filename is free and no `-vN`
was needed. Dirty-tree contents spot-verified where they mattered: `s248-D1…D4` present in
`knowledge/_rulings.json`, `knowledge/_screen-gate/dashboard.md` present on disk, `_tools/Caffeinate/`
present with 5 files.

**Commands a conductor can re-run, verbatim** (all read-only; nothing below writes). Paths relative to
the repo root except where the memory store is named:
- `python3 -c "import json;d=json.load(open('notes/_dream/_MEMORY-GRADES.json'));print(d['hooks_seen'],d['counts'],d['unlinked_index_lines'])"`
  → `33 {'FRESH':23,'AGING':3,'STALE':3,'UNPROVABLE':4} ['1: …','2: …','36: …']`
- in the memory store: `rg -c '^-\s+\[[^]]+\]\([^) ]+\.md\)' MEMORY.md` → **33** ·
  the same pattern on `hook-overflow-2026-09-03-242.md` → **107**
- second-link count, both files:
  `rg -c '^-\s+\[[^]]+\]\([^) ]+\.md\).*\[[^]]+\]\([^) ]+\.md\)'` → **5** (MEMORY.md) · **13** (overflow)
- `sed -n '695p;702,730p' knowledge/_gardener.py` → `_HOOK_RE`, the `unlinked` append and its
  *"DECLARED, never silently dropped"* comment; `sed -n '706,710p'` → the empty-index refusal
- in the memory store: `rg -l '_measure_tokenizer' .` → **4 files**; in the repo:
  `ls knowledge/_measure_tokenizer.py` → No such file; `rg -c '_measure_tokenizer' -g '*.py' knowledge/`
  → comments only (`_capture_gate.py`, `_governs.py`)
- `rg -c 'provenance unknown' .` → **11 across 7 files**; `rg -n 'provenance unknown' _LIVE-STATE.md`
  → `:14`, `:76`
- `sed -n '1,2p' _tools/Caffeinate/main.swift` → the same build command #246 gave Dave in chat
- `ls knowledge/_screen-gate/ | wc -l` → **10**; `tail -1 knowledge/_SCREEN-GATE.md` →
  `9 subject(s) on record.`; `rg -c 'dashboard' knowledge/_SCREEN-GATE.md` → **2** (both the
  `international-banking-dashboard` rows; no `dashboard.md` row)
- `rg -c '^>\s*\*\*[0-9]+[a-z]?\.' GOOD-MORNING.md` → **28**; `rg -c '^> \*\*18\.' GOOD-MORNING.md`
  → **0**; `sed -n '3358p' _GM-ARCHIVE.md` → the archived item 18
- `rg -n '"s248-D' knowledge/_rulings.json` → `:6157 :6173 :6189 :6206`
- `sed -n '297,300p' notes/_subreports/2026-09-02-241-lane-E-diet-apply.md` → *"That grade will drop at
  the next dream pass"*; `sed -n '47p' notes/_subreports/2026-09-03-242-lane-F-boot-offload.md` → the
  memory-stub row of the diet table
- `sed -n '111p' notes/_subreports/2026-09-05-247-wrap.md` → the unstaged-strays declaration

**Nothing here self-promotes.** Four proposals, all `status: floated`; promotion is Dave's alone.
