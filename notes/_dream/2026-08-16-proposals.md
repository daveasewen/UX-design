# Dream pass 8 — floated proposals

provenance: `local_93b978c2-c995-422d-a418-58872bb61d93` · 2026-08-16
status: floated

*I PROPOSE ONLY. Nothing here self-promotes; promotion is Dave's alone on reading this file
(derivation-governance). Every RULED row in `notes/_MEMENTO-DECISIONS.md` and every checked-clear item
at the end of EVERY prior proposals file — pass 3's, pass 4's (q)–(w), pass 5's (x)–(bb), pass 6's
(cc1)–(cc6), pass 7's (dd1)–(dd7) — was read before hunting. **Pass 6's P1–P5 and pass 7's P1 are
STILL FLOATED and are NOT re-floated here**; where new evidence bears on one it is referenced, not
duplicated. (Pass 7's P2/P3/P4 were promoted and enacted at `s177-D1`; P1 was DEFERRED there.)*

★ **This is the FIRST SCHEDULED pass — `memento-dream-pass`, Sun 07:10, fired on time
(`lastRunAt 2026-08-16T06:10:28Z`, verified by a live `list_scheduled_tasks`).** By `s182-D1` CALL 4
that fact is not incidental: **it is the event that opens the B3 return-with-numbers counting window.**
P4 below is about what that window found on its first morning.

Ranked by prevalence, highest first.

---

### P1 — The grades instrument decides "is this hook probeable?" by reading the ONE-LINE `MEMORY.md` index entry, while `s182-D1`'s newly-in-force authoring convention tells authors to put the probeable token in the hook FILE — so the two hooks written since the ruling both comply and both grade UNPROVABLE, and the "109 of 122 judgment-shaped" figure the ruling accepted was measured on the wrong text

- EVIDENCE:
  - **The convention, in force since #182.** `s182-D1` CALL 1, `knowledge/_rulings.json`:
    *"IMMEDIATELY IN FORCE: the probe-shaped-hooks AUTHORING CONVENTION — a new memory hook that makes
    a mechanical claim must carry the backticked path or quotable line that makes it probeable."*
    Restated verbatim in the hook that carries it, `b3-review-ruled-182.md`:
    *"⛔ AUTHORING CONVENTION, IN FORCE NOW — when writing any memory **hook** that makes a mechanical
    claim, include the backticked path or quotable line that makes it probeable."*
  - **What the grader actually reads.** `knowledge/_gardener.py`, `derive_probe(hook: str, root: str)`
    at **:735**, called with `s` — and `s` is set at **:706** as `line.strip()` while iterating
    `open(MEMORY.md).read().splitlines()`. The same loop stamps `"hook_sha": _sha(s)` (**:721**) and
    `"index_line": i`. **The unit of grading is the index LINE, never the hook file.** The refusal
    string at **:750** then says *"no backticked repo path **in the hook**"* — the word "hook" meaning
    the index line to the machine and the file to the author.
  - **Two hooks have been written since the ruling. Both obey it. Both grade UNPROVABLE.**
    - `banner-brackets-are-ages.md` (written #183) body: *"**Probe:** walk `_GM-ARCHIVE.md` backwards
      — the 'THREE REAL DEFECTS' item reads `[45]·[50]·[113]` at birth…"* — a backticked repo path,
      a named probe, an explicitly mechanical claim. Sidecar verdict, this pass:
      `"grade": "UNPROVABLE", "why": "no backticked repo path in the hook"`, `"probe_ran": false`.
    - `b3-review-ruled-182.md` — the hook that PUBLISHES the convention — carries backticked
      `knowledge/_gardener.py` and `knowledge/_rulings.json` in its body. Same verdict, same string.
    - Their `MEMORY.md` index lines carry no backticked path, which is why. Neither author was wrong;
      the surface they were told to write into is not the surface that is read.
  - **The measurement, re-run and decomposed this pass** (`--refresh` receipt of 2026-08-16T07:12:05):
    **124 hooks — FRESH 12 · AGING 1 · STALE 0 · UNPROVABLE 111**, grade changes **0**. Of those 111,
    reading the hook FILE bodies (frontmatter stripped) with `_gardener.py`'s own `looks_like_path()`:
    - **25** carry **exactly one** path-like backticked token ⇒ under the grader's *existing*
      `path-present` rule these flip immediately, no new probe kind, no ruling.
    - **60** carry **more than one** ⇒ `kind: none` by the AMBIGUOUS rule, which is a defensible
      refusal but a different one from *"no mechanical claim exists"*.
    - **26 — and only 26 — carry none at all.** Separately, **69 of the 111** name at least one
      backticked path that **resolves to a real file in the repo today**.
  - ⚠ **What that does to the ruling's premise, stated carefully.** `s182-D1` CALL 1 parked probe
    commissioning behind the first-cycle numbers, and its hook reasons *"~80 hooks are judgment-shaped
    forever."* On the corpus's own text the genuinely path-free population is **26**, not ~80. ⛔ I am
    **not** claiming 85 probes exist — a backticked path is necessary, not sufficient, and several of
    the 69 point at rolling files (`GOOD-MORNING.md`, `_CHAIN.md`) where a presence probe would be
    near-meaningless. **69 and 25 are upper bounds on the addressable subset, and they are labelled as
    such.** The finding is that the number Dave ruled against was produced by grading a different
    string from the one the ruling asks authors to write.
- PREVALENCE: **2 of 2** hooks authored since the convention came into force comply with it and grade
  UNPROVABLE anyway (100%) · **85 of 111** UNPROVABLE bodies carry a path-like token, **25** of them
  unambiguously · **1** code path (`_gardener.py:706 → :735`) is the whole mechanism · **1** ruling
  (`s182-D1` CALL 1) and **1** carried residual (⑤, age `[4]`) rest on the figure.
- PROPOSED: **the smallest step is a measurement, not a build, and it is deliberately not a new
  instrument** (`s172-D3` fences appetite). Add a `--refresh` **companion count**, printed on the
  receipt beside the existing census: *"of N UNPROVABLE, K have exactly one resolvable backticked path
  in the hook FILE"* — read-only, no grade changes, no schema change, and it turns the disputed premise
  into a number Dave can rule on at the return-with-numbers. ⛔ **Do NOT switch the grader to read hook
  files unasked** — that would silently re-grade the corpus underneath a ruling Dave has just made, and
  the re-grade is exactly what CALL 1 parked. If he wants the stronger form, the two separable calls
  are: (a) **the grading unit** — index line or hook file, which is a *definition*, his; (b) whether
  the AMBIGUOUS-resolves-upward rule should prefer the **first** path over refusing, which is a
  behaviour change and should carry its own mutation arm. ★ The cheapest wording fix costs one string:
  `_gardener.py:750`'s *"in the hook"* → *"in the MEMORY.md index line"*, so the refusal stops
  describing a file it never opened [[gate-must-quote-what-it-forbids]].
- status: floated

---

### P2 — A claim Dave personally caught and corrected at #182 was carried forward verbatim into #183's residual list — twice — because the 2c carry rule's own invariant is "AGES +1, WORDING UNCHANGED", and an unchanged wording cannot record a retraction

- EVIDENCE:
  - **The correction, inscribed in four places at #182.** `GOOD-MORNING.md:36` — *"⓪ THE FIRST FACT IS
    A CORRECTION TO OUR OWN RECORD, AND IT IS WRITTEN FIRST BECAUSE IT WAS CARRIED TWICE AS TRUTH. The
    #181 banner said the Monday dream-pass slot was 'RULED BUT STILL UNSCHEDULED' … **BOTH WERE FALSE**
    … **Dave caught it.**"* Also `_LIVE-STATE.md:69`, `knowledge/_REVIEW-SIGNOFF.md:279`, and
    `s182-D1`'s evidence array, which is where the class rule was deliberately homed:
    ★ *"any claim that something is UNSCHEDULED must cite a scheduler-list RUN, exactly as a repo claim
    cites `git log`."*
  - **The retracted claim is live in `_CHAIN.md`'s `residual → #184` list today, in two items:**
    - *"★ ⑥ THE RETURN-WITH-NUMBERS IS A STANDING DEBT … `[4]` — ⛔ **The first scheduled pass has not
      run, because the weekly Monday slot below is still unscheduled.**"*
    - *"⚙ **THE WEEKLY MONDAY SCHEDULE IS RULED BUT NOT SCHEDULED `[4]`** — it waits on controller
      adoption, by the ruling's own words."*
  - **Ground truth, run this pass, per the class rule's own standard.** `list_scheduled_tasks` →
    exactly one task: `memento-dream-pass` · *"At 07:10 AM, only on Sunday"* · `cron 0 7 * * 0` ·
    `enabled: true` · `lastRunAt 2026-08-16T06:10:28.795Z` · `nextRunAt 2026-08-23`. The slot is not
    Monday, it is not unscheduled, and it ran — **it is what dispatched this pass.**
  - **The same banner contradicts itself.** `_CHAIN.md` ⓪ (#183's own words): *"⚠ **The first SCHEDULED
    dream-pass therefore fires later THIS SAME DAY, 2026-08-16 07:10**"*. One banner, both claims.
  - **The mechanism is named in the list itself**, and that is what makes this a class rather than a
    slip: *"**PRIOR CARRIES, AGES +1, WORDING UNCHANGED** *(2c EXIT CHECK … nothing orphaned)*"*. The
    exit check verifies **presence** — that no item was dropped — and it has no test for **truth**. A
    correction is the one event that must change wording, and the invariant forbids it
    [[invariant-cannot-discriminate-reversal]].
  - ⚠ **This has now propagated across four wraps** (#181 asserted it · #182 retracted it · #183
    re-published it · it stands at age `[4]` for #184), and the retraction never reached the carry list
    because the correction was written to GM's ⓪ block and to `_LIVE-STATE.md`, which are different
    surfaces from the residual list. Pass 7's P1 found the *stale-ordinal* half of this class outside
    the `s161-D4` fence; this is a **different and worse half — a fact the fence does cover in form,
    carried at a correct age, whose content Dave has already overturned** [[gate-glob-scope-rule]].
- PREVALENCE: **2 items** in one live `residual → #184` list state a retracted claim · **1** internal
  self-contradiction within the same banner · **4 sessions** of propagation (#181→#184) · **4 record
  sites** carry the correction and **0** of them reached the carry list · **1** live scheduler read
  settles it in one call.
- PROPOSED: **one clause in `knowledge/_RUNBOOK-capture-ritual.md` step 2c, and it is a carve-out from
  an existing rule rather than a new rule** — *"WORDING UNCHANGED holds for every carry EXCEPT one
  whose claim was corrected or retracted since it was written; a retracted carry is struck with its
  retraction named (session + where the correction is inscribed), never re-typed."* Then strike the two
  items above. ⛔ **Do not simply delete them** — `feedback-header-wins-over-audit`: the honest form is
  *struck with the receipt*, because a silently vanished item is indistinguishable from a dropped one,
  which is precisely what the 2c EXIT CHECK exists to prevent. ★ If Dave wants the mechanical form
  instead of the prose one, the cheapest is a **named re-checker** (`s129-D5`): the exit check already
  cross-checks `residual → #N` claims against `_rulings.json` under `s161-D4` — extend the same pass to
  flag any carry whose text appears in a GM ⓪ **CORRECTION** block. Touches:
  `knowledge/_RUNBOOK-capture-ritual.md` step 2c · `GOOD-MORNING.md`'s next residual roll.
- status: floated

---

### P3 — The `residual → #N` list is the most-read carry surface in the project and nothing parses it, so #183's list carries seven colliding circled numerals, one item recorded twice at two different ages, and an orphaned sentence fragment with an unmatched bracket — all three defects also present one session earlier

- EVIDENCE (all from `_CHAIN.md`'s `residual → #184` block, 11,697 chars, parsed this pass):
  - **Seven numeral collisions in one list.** ① ② ③ ④ ⑤ ⑥ ⑦ each appear **twice**, ⑤ and ⑥ **three
    times** — the session's own eight new items are numbered ①–⑧ and the carried block from #182 was
    copied in with **its** ①–⑦ intact, then two more ⑤/⑥ items follow. A reader told "see ⑤" has three
    candidates.
  - **One item appears twice with two different ages.** *"⬛ ① THE SCALING CALL AT TUNER v2 IS STILL
    DAVE'S EYE AND IS #184's NATURAL OPENER **[1 — DAVE'S]**"* and, 6,000 characters later, *"⬛ ① THE
    SCALING CALL AT TUNER v2: DAVE'S EYE, AND #183's NATURAL OPENER **[2 — DAVE'S]**"*. Same
    deliverable, same file `reviews/SPARKLINE-ATOM-TUNER-2026-08-15-v2.html`, same 31,509 B, same
    "scaling is the ONLY open decision" sentence — **one item, two ages, one list.** Since the age is
    what `s128-D2` uses to date an item and what `banner-brackets-are-ages` teaches readers to convert
    to an origin session, the item now resolves to two different origins.
  - **An orphaned fragment carried as if it were an item.** Between two ⬛ items:
    *"· **alert surface cost in real tokens). ·**"* — a dangling clause with an unmatched closing
    parenthesis, no marker glyph, no age bracket. It is the tail of ⑥'s parenthetical, split off when
    the block was copied.
  - **Not new to #183 — the same three defects are in `GOOD-MORNING.md:51`'s `residual → #183` list**
    (⑤ and ⑥ colliding with the session's own ①–⑦; the identical *"alert surface cost in real
    tokens)."* fragment). **Two consecutive sessions, hand-copied, unparsed.**
  - **Why nothing catches it.** `s161-D4`'s fence cross-checks each `residual → #N` **claim** against
    `_rulings.json` status and reported *0 fails* at #176 — it reads claims, not list structure. The
    generated line beneath (*"residual (GENERATED #183): 2c OK (banners 2/2) · 2d OK (deltas 3/3) · 2f
    OK (strata 1, log #182)"*) counts **banners and strata**, never items. The list is the one
    high-traffic artefact with no parser in its consumer's grammar
    [[no-gate-parses-the-artefact]].
- PREVALENCE: **7 colliding numerals · 1 duplicated item with 2 ages · 1 malformed fragment**, in
  **2 of 2** consecutive residual lists inspected · **0** of the 3 existing checks over this surface
  (`s161-D4`, 2c EXIT CHECK, the generated `residual` line) can see any of them.
- PROPOSED: **a parser, and the smallest useful one is a counter, not a validator** — one function in
  the existing 2c tooling that splits the `residual → #N` list on ` · `, and reports three numbers at
  wrap: **items · duplicate marker glyphs · segments with no age bracket**. Advisory first (report,
  never block — `gate-narrows-its-own-rule`), so its first live run measures the real population before
  anything is made to fail. ⛔ **Do not renumber the carried block by hand** — the collision is a symptom
  of copying a numbered set into another numbered set, so the durable fix is that **carried items lose
  their circled numerals and keep only their age bracket**, which is the field `s128-D2` actually
  defines. ★ If Dave prefers zero new machinery, the prose-only version is one line in step 2c: *"the
  circled numerals number THIS session's new items only; carried items are identified by age."*
  Touches: `knowledge/_RUNBOOK-capture-ritual.md` step 2c · whichever module owns the 2c roll.
- status: floated

---

### P4 — The B3 return-with-numbers counting window opened at 07:10 this morning by `s182-D1` CALL 4, and on its first morning the human half of the dataset is empty by construction while the cost half contains 1,050 real tokens of rows the ruling excludes but nothing marks

- EVIDENCE:
  - **The window, and that it is now open.** `s182-D1` CALL 4: *"the return-with-numbers counting
    window opens at the FIRST SCHEDULED dream-pass (2026-08-16 07:10); the 2026-08-15 manual pass does
    NOT count."* `list_scheduled_tasks`: `lastRunAt 2026-08-16T06:10:28Z` — **it fired; this is that
    pass.**
  - **The dataset has two halves and only one is populated.** `notes/_dream/_GRADE-DECISIONS.jsonl`,
    15 rows: **14 `kind: alert`** (the cost half) and **1 `kind: decision`** (the human half — *"how
    often a grade changed a retrieval decision"*). That one decision row is
    `{"entry": "boot-floor-measured-109.md", "changed_retrieval": false, "session": "#180"}` and it
    carries the exclusion note. ⇒ **countable human datapoints at window open: 0.**
  - **The exclusion is a hand-typed free-text field, and it covers 4 of the 14 rows.** Four alert rows
    carry `drive_note: "#180 BUILD DRIVE … EXCLUDE from the B3 return-with-numbers; the counting window
    opens at the first scheduled dream-pass cycle"`. The other **10 carry nothing** — yet their
    timestamps run `2026-08-15T13:30:24` → `2026-08-16T00:33:02`, **all before 07:10 today**, so by the
    ruling all ten are outside the window too. Summed naively they contribute **1,050 real tokens**
    (10 × 105) to a cost figure that should currently read **0**. Nothing in the file derives
    countability from the ruled boundary; the boundary exists only in prose.
  - **Every alert row stamps a census that was already stale when it was written.** All 14 carry
    `counts: {FRESH 12, AGING 1, STALE 0, UNPROVABLE 109}` and `refreshed_at: 2026-08-15T13:29:47` —
    because `_checkin.py` reads the sidecar and only `--refresh` rewrites it, and `--refresh` runs once
    per dream pass. Today's refresh moves it to **111 of 124**. The cost log therefore records the
    grade census of *a week ago* against *today's* spend.
  - **Nothing prompts the human half.** `--grade-decision <entry-id> --changed yes|no` is a manual flag;
    `knowledge/_RUNBOOK-dream-pass.md` § B3 describes it (*"the other half … is human and is never
    inferred"*) but **no step in the conductor sequence or the dreamer spec asks for it**. An
    instrument whose input nobody is asked for returns empty at review
    [[instrument-without-a-consumer]].
- PREVALENCE: **1 of 2** dataset halves populated at window open · **10 of 14** cost rows unmarked but
  out-of-window (1,050 real tokens) · **14 of 14** rows stamping a superseded census · **0 of 9** steps
  in the dream-pass conductor sequence mention `--grade-decision` · **1 week** to the next scheduled
  pass, so whatever shape this file has by 08-23 is the shape the review reads.
- PROPOSED: **two small separable steps, both reversible, neither a new instrument.**
  (a) **Generate the boundary instead of noting it** (`s129-D5`'s strong option): write the ruled
  window-open timestamp **once** into `notes/_dream/_MEMORY-GRADES.json`'s schema block (it already
  carries `ruled_by` and the `s182-D1` provenance), and have the receipt report *countable* rows as
  `at >= window_open` — so the exclusion stops depending on whoever remembered to type a `drive_note`.
  (b) **Add one line to `knowledge/_RUNBOOK-dream-pass.md` § B3 and to the dreamer's Method
  obligations:** every pass records at least one `--grade-decision` row for the grades it actually
  consulted, *including a `--changed no`* — a nil return is a datapoint and an absent return is not.
  ⛔ **Do not backfill or synthesise decision rows** — the human half is worth exactly what it is, and
  inventing it would manufacture the CLAIMED class ADR-0016 forbids. ⚠ Consequence, stated: on today's
  evidence the review due after this cycle will read *"cost: measured; effect: no data"* — which is a
  legitimate answer to bring Dave, but only if it is brought as a **finding** rather than discovered at
  the review.
- status: floated

---

### P5 — The `AGING` grade cannot change inside the observation window that is supposed to derive it: the threshold is 30 days, the return-with-numbers is due after one weekly cycle, and this pass measured exactly zero grade changes

- EVIDENCE:
  - `knowledge/_gardener.py:144` — `GRADE_AGING_DAYS = 30` with the comment
    *"PROVISIONAL: probe passes but the claim itself hasn't been touched"*; `:815` is the only
    transition (`if age_days > aging_days: return AGING`).
  - `s182-D1` CALL 2: *"the 30-day AGING threshold stays an EXPLICIT PLACEHOLDER, picked not derived;
    **derive from cycle data**."* And `_gardener.py:133` restates it in the schema block.
  - The cycle is **weekly** (`cron 0 7 * * 0`), and `s179-D1`'s fork returns *"after one full
    dream-pass cycle"* — **7 days against a 30-day threshold**. Four cycles must pass before the
    threshold can move a single entry that was not already over it.
  - **Measured, not argued:** today's `--refresh` receipt reports **`grade changes : 0`** over the full
    week since the sidecar was created, with the population at FRESH 12 · AGING 1 · STALE 0 ·
    UNPROVABLE 111. The AGING census has been **1** at every reading.
  - ⚠ The three-way interaction is what makes it structural rather than slow: **111 of 124 entries are
    UNPROVABLE and cannot grade at all**, **STALE has never been non-zero**, and **AGING is gated 30
    days out** — so the first cycle's dataset is, by the instrument's own construction, almost
    guaranteed to be *no signal*, which is indistinguishable from *no decay*
    [[unrun-search-indistinguishable-from-absent-record]].
- PREVALENCE: **1 constant · 1 ruling clause that depends on it · 1 measured cycle with 0 changes ·
  4 cycles minimum before the constant can produce its own evidence.** Thin on breadth by design —
  it is one number — and it is ranked last for that reason; it is included because it is cheap to
  settle and expensive to discover at the review.
- PROPOSED: **name the mismatch to Dave and give him the two forms, do not pick one.** (a) **Move the
  return date, not the constant** — the return-with-numbers reports after the first cycle *on the cost
  half* (which has data now) and after **five** cycles on the AGING half, so the placeholder gets a
  window it can actually be derived in; or (b) **lower `GRADE_AGING_DAYS` for the observation period
  only**, declared as an instrumentation setting with an expiry date, so at least one transition is
  observable — the `s129-D5` **expiry** option. ⛔ **Not proposed: deriving the threshold from an empty
  cycle**, which would dress a picked number as a measured one
  [[planning-estimate-is-not-a-measurement]]. Touches: `knowledge/_gardener.py:144` (only under (b),
  and only with Dave's word — the constant is inside a ruling's PROVISIONAL schema).
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(ee1) The B3 refresh arm RAN, and its receipt is reproduced here rather than summarised.**
  `python3 knowledge/_gardener.py --refresh`, rc=0: *124 hooks graded — FRESH 12 · AGING 1 · STALE 0 ·
  UNPROVABLE 111 · unlinked lines 4 DECLARED, not graded · grade changes 0 · alert surface 1 line.*
  The sidecar `notes/_dream/_MEMORY-GRADES.json` was rewritten by that run — **that is the arm's
  intended output, and it is the ONE file besides this one that this pass changed** (see ee6). The
  diff is a restamp: `refreshed_at`, `memory_index` (the session's own mount path), `hooks_seen`
  122 → 124, `UNPROVABLE` 109 → 111, and three shifted `unlinked_index_lines` offsets. **No grade
  flipped.** The two new hooks are `banner-brackets-are-ages.md` and `b3-review-ruled-182.md`, both
  UNPROVABLE — which is P1's receipt, not a separate finding.
- **(ee2) The `memory_index` path inside the sidecar is a per-session mount path, and it is NOT a
  finding.** It moved from `/sessions/relaxed-wonderful-bardeen/…` to
  `/sessions/nifty-youthful-albattani/…`. Cowork mounts are session-scoped, so this field will differ
  on every single refresh forever. Checked deliberately because it *looks* like drift; it is the
  sandbox working. A future pass should read it as provenance, not as a pointer.
- **(ee3) The gauge-log 2f lag, the `_governs` evidence-format fails, and the `[107]` CI gate are all
  correctly homed and are not re-reported.** Pass 7 cleared the first two at (dd2)/(dd1); the third has
  moved *forward* since — #183 built the COULD-NOT-ASK clause and `fetch-depth: 0`, and carried its own
  honest residual that **real CI is UNPROVEN and the survey bucket is unwired**. That is the discipline
  working, and it is Dave's push, not a defect.
- **(ee4) The instrumentation files that dirty the tree — `notes/_REHEARSAL-LOG.jsonl`,
  `knowledge/_graph-mark-observations.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` — are pass 6's P2,
  STILL FLOATED, and are referenced not re-floated.** #183's banner ⑧ names all three as
  *"dirty-at-baseline instrumentation appends (declared; their POLICY remains an open residual)"*.
  New datapoint recorded here for Dave's eventual ruling on that P2: the population is now **three**
  files, not one, and the third of them is the dataset a ruling depends on (P4).
- **(ee5) Pass 7's P1 is UNCHANGED in substance and is not re-floated — but one half of it was
  enacted and the enactment is visible.** `GOOD-MORNING.md:10`'s stale "EIGHTH session running"
  ordinal is **gone**, replaced by *"(the session-count ordinal is DELETED per `s178-D1` enacting
  dream-P1 — stale twice ⇒ generate, never re-stamp)"*. The STANDING CARRY half remains deferred per
  `s177-D1` pending the liveness check. P2 above is a *different* half of the same family and says so.
- **(ee6) What this pass wrote, stated plainly and without smoothing.** **Two files:** this proposals
  file (the pass's only *finding* output) and `notes/_dream/_MEMORY-GRADES.json` (the B3 refresh arm's
  own output, mandated by `knowledge/_RUNBOOK-dream-pass.md` § B3 — *"Every pass runs
  `python3 knowledge/_gardener.py --refresh`"*). ⚠ **The dispatch said "the proposals file is your only
  write" AND "run the refresh arm"; those two instructions are in tension and I am declaring the
  tension rather than resolving it silently.** I did **not** revert the sidecar, because reverting
  would discard the mandated refresh. **Nothing else was touched:** no memory file, no canon, no
  ledger, no git operation of any kind. `git status --porcelain` at close shows exactly
  `M notes/_dream/_MEMORY-GRADES.json` plus this new file. The `.git/index.lock` that git warns about
  is the known unlink-permission wart (`git-lock-mv-not-rm`); ⛔ I did not touch it.
- **(ee7) Out of scope by standing exclusion, recorded so it is not mistaken for an oversight:**
  dream-lane mechanics remain barred from this pass's floating (pass 6 cc6, pass 7 dd7). ⚠ **P2 and P4
  sit near that line and I am naming where I drew it:** P2's *subject* is the 2c carry rule, and the
  scheduler only supplies the ground truth that settles it; P4's *subject* is a dataset that `s182-D1`
  binds Dave to review, not the lane's cadence. **What I deliberately did NOT float:** the lane's §🔀
  status row in `_LIVE-STATE.md`, the cadence itself, and the conductor sequence's own steps.

---

## Method

**Shape A (Cowork), pass 8 — the FIRST SCHEDULED fire under `s182-D1` CALL 4.** Session
`local_93b978c2-c995-422d-a418-58872bb61d93`, date **2026-08-16** from the host's `date`
(`Sun Aug 16 07:10 BST 2026`), not recalled. Repo root
`/Users/daviewen/Documents/Claude/Projects/UX-design`; the sandbox mount is
`/sessions/nifty-youthful-albattani/mnt/UX-design`, verified to be the **live** tree and not a stale
copy before anything was measured (`git log --oneline -3` → `56fd68a` #183 · `27b421a` #182 ·
`5a9f6ba` #181) [[stale-mount-corroborates-a-stale-premise]].

**Read, in spec order:** `MEMORY.md` memory index (hooks only, as injected context) ·
`.claude/agents/dreamer.md` in full · `knowledge/_RUNBOOK-dream-pass.md` in full including § B3 ·
`_CHAIN.md` in full (118 lines — it carries the #183 banner, the whole `residual → #184` list, and the
generated residual line) · `GOOD-MORNING.md` and `_LIVE-STATE.md` **by targeted line reads and greps
only** — ⛔ deliberately NOT opened top-to-bottom, since a conductor doing exactly that is pass 7's P2
and is a live carried residual · **all seven prior proposals files**: every `### P` heading, every
`status:` line, and every checked-clear list ((q)–(w), (x)–(bb), (cc1)–(cc6), (dd1)–(dd7), and pass 3's
prose-form list) **before** hunting anything.

**Repo forensics run this pass, each named with what it produced:**
`python3 knowledge/_gardener.py --refresh` (the mandated B3 arm; receipt at ee1) ·
`notes/_dream/_MEMORY-GRADES.json` parsed — 124 entries, per-entry `grade`/`probe`/`why` read ·
`notes/_dream/_GRADE-DECISIONS.jsonl` parsed — 15 rows, split by `kind`, summed by `tokens`, checked
for `drive_note` and against the ruled window boundary · `knowledge/_rulings.json` parsed — **164
rulings** (up from 157 at pass 7); `s182-D1`/`-D2`/`-D3` read verbatim ·
`knowledge/_gardener.py` read at `:130–150`, `:700–760`, `:800–820` (the index-line loop, `derive_probe`,
the AGING transition) · **an independent re-measurement of the UNPROVABLE population against the hook
FILE bodies**, using `_gardener.py`'s own imported `looks_like_path()` rather than a re-implementation,
frontmatter stripped — 25 / 60 / 26 split, 69 resolving · `_CHAIN.md`'s residual block parsed
programmatically for circled numerals and age brackets · repo-wide greps for `Monday` across `.md`
and `.py` · `git log`/`git status` (read-only).

**One live external probe, and it is the receipt P2 turns on:** `list_scheduled_tasks` — one task,
`memento-dream-pass`, Sun 07:10, enabled, `lastRunAt 2026-08-16T06:10:28Z`. Run precisely because
`s182-D1`'s own class rule demands it: *any "X is unscheduled" claim must cite a scheduler-list RUN.*

**Experiments and their cleanup.** One: `notes/_dream/_MEMORY-GRADES.json` was copied to
`/tmp/grades-before.json` before the refresh so the diff could be attributed
[[attribute-the-diff]]. `/tmp` is outside the repo; nothing to clean in the tree. No other file was
created, moved or deleted. No mutation was applied to any source file — **P1 is reported from reading
the code path and re-running the grader's own predicate, not from mutating it**, and that limit is
stated rather than dressed: I have **not** proven that switching the grading unit would produce 25
working probes, only that 25 entries satisfy the existing rule's precondition on a surface the grader
does not read.

**Transcripts — 15 in the window, 1 read, 14 skipped, and the trade is stated not smoothed.**
`list_sessions` returned 20; the Apollo window is **#166–#182** plus a "General message" session
(`local_88e298a0`, most recent) and the pass-7 dream session (`local_4191e490`). ⚠ **#183 has no
listed session of its own** under an Apollo title, though its commit `56fd68a` is in the log — so the
session that produced the artefacts P2 and P3 are built from is **not in the transcript window at
all**. I read `local_ce099fb9` (#182) only, for the B3 ruling's live shape. The other fourteen were not
read at turn level, for pass 7's stated reason: the Shape A ceiling gives tool **names** without
arguments or results, so every checkable claim must be re-verified in the repo regardless — and this
pass's five proposals are each built on a measurement I made myself this morning. ⚠ **The cost of that
trade, named: a repeated verbal instruction from Dave across #166–#183 that left no artefact would not
have been caught.** That is this pass's largest blind spot, and it is the same one pass 7 declared.

**Where the ceiling bit.** P1's subject — whether the author of a hook understood "the hook" to mean
the file or the index line — is a matter of intent that no transcript at this fidelity could settle.
I resolved it from **artefacts instead**: both post-ruling hooks put the backticked path in the file
body and neither put one in the index line, which is what an author following the written convention
would do. Stated as an inference from two artefacts, not as a claim about anyone's reasoning.

**Prevalence discipline.** Every `N of M` above is a count of files, JSON records, grep hits, parsed
list segments or timestamped rows produced by a command run this pass. P5 is labelled thin on its face
and ranked last for that reason. Where a number is an upper bound (P1's 69 and 25) it says so in the
proposal body, not only here.
