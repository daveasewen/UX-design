# Dream pass — 2026-08-08

provenance: local_a590b514-eb6a-4b64-a637-48445c1521db · 2026-08-08
status: floated

*Fifth pass. The prior pass (2026-08-02) covered through **#76**; the chain is now at **#127** and this
file is written for **#128**. **Fifty-one sessions of uncovered ground against a fifteen-transcript
window** — the coverage gap is stated plainly in § Method and it is the largest ceiling this pass
carries. Nothing here is promoted; promotion is Dave's alone. Every proposal carries at least one
receipt read this pass, and where evidence is thin or second-hand it says so.*

⚠ **This pass had NO shell and NO git** — `Read`/`Grep`/`Glob`/`Write`/`ToolSearch` only, per the
spec's frontmatter and the dispatch's restatement. So there is **no commit history, no file mtime and
no token measurement** in this file. Every figure below is either **quoted from an artefact** or
**counted by grep**. Where the 2026-08-02 pass could settle a question with `git log`, this one
declares it open instead.

---

### P1 — **All six of Dave's 2026-08-02 dream-pass rulings are unenacted at #127 — and not one of them exists in `_rulings.json`, so the instrument that tracks enactment is structurally blind to them**

- EVIDENCE — the ruling, then the artefact, one pair per item. Dave's words are at
  `notes/_MEMENTO-DECISIONS.md:3373` — *"I'll go with all your recommendations"*, after a full prose
  read-back of all seven (P1 was withdrawn by its author, so **six** bind).
  - **P2 half (a) — `c_block` comparison branch. NOT ENACTED.** Ruled *"add a `c_block` comparison
    branch (STILL ADVISORY)"* (`:3375`). Exhaustive probe re-run this pass:
    `grep -n "c_block" knowledge/_capture_gate.py` → **exactly 3 hits — `:2234` (unpacking), `:2246`
    and `:2247` (inside the same f-string)**. `_capture_gate.py:2243` is still the single comparison,
    `elif bill_of(chain_file) > bill_of(c_warn):`. **Identical to the shape the pass described six
    days ago; the only change is the line numbers.**
  - **P2 half (b) — `GOOD-MORNING.md`'s hardcoded chain figure. NOT ENACTED, and it has rotted
    further.** Ruled *"replace `GOOD-MORNING.md:93`'s hardcoded `4,585` with the `chain_file_tk('.')`
    pointer `:401` already uses"*. The line has moved to **`GOOD-MORNING.md:125`** and reads
    verbatim: *"⚠ **MEASURED #38: 4,585 tape — OVER M10's 4,500 warn.** This block quoted `3,410 tk`
    from #33 and had been stale five sessions."* ★ **The correct shape is still present in the same
    file** — `GOOD-MORNING.md:427` carries *"run `chain_file_tk('.')` — the figure MOVES"*. So the
    file demonstrates the remedy 302 lines below the defect, exactly as it did at #75.
    ⚠ **And the figure is now stale in its UNIT as well as its value**: `_CHAIN.md`'s generated
    footer reads *"15,935 real — the unit is THE WHOLE FILE"*, while `:125` quotes **4,585 tape**
    against a **4,500 tape** warn. A sentence whose own subject was re-denominated (#82-D1, real
    tokens, measured never converted) now reads as if the chain were 85 over its warn.
  - **P3 — `_RUNBOOK-capture-ritual.md:89`. NOT ENACTED.** Ruled *"amend `:89` to carry #28's
    ruling"*. `grep -n "two names first" knowledge/_RUNBOOK-capture-ritual.md` → **`:89` —
    "- **The two names first** (see step 4b) — rename + next title, at the very top."** **Byte-identical
    to the line the #90 re-check already found unchanged** (`:3420`, *"verbatim unchanged"*). Two
    independent verifications, 37 sessions apart, same result.
  - **P4 — the running count in the `consult-receipts` stratum. NOT ENACTED.** Ruled *"add the running
    count to the stratum line (~8 tape/wrap)"*. All `consult-receipts #N` lines in
    `notes/_GAUGE-LOG.md` read this pass: **not one carries an `Nth of M` count**, up to and
    including the newest, `:1209` (#126) — *"none — **and it is a LAPSE, not a ruled skip**"*, a fully
    written honest negative with no rate in it. The form Dave ruled has never once been written.
  - **P5 — `_git_commit.sh` takes explicit paths. NOT ENACTED.** Ruled *"option (a) — the script
    takes explicit paths so `--reconciled` means what it says"*. `grep -n "git add" knowledge/_git_commit.sh`
    → **`:227  git add -A 2>/dev/null`**, still the only staging call; `:12` still promises
    *"you have run `git status --short` and can name WHY every dirty path exists"*. The line has now
    travelled **`:112` → `:220` → `:227`** across three independent readings (#75, #89, today) while
    the mechanism never moved.
  - **P6 — one `_FUTURE-STATE.md` entry homing the three orphaned forks. NOT ENACTED.** Ruled
    *"addition only"*. Probe re-run against the destination the ruling itself names:
    `grep -n "two-fetch|staleness control|index-drift|fog" _FUTURE-STATE.md` → **0 hits, all four
    terms.** Identical to the #90 re-check (`:3439`), which recorded the same zero and called it
    *"ruled-not-enacted"*. **Thirty-eight sessions later it is still zero.**
  - **P7 — the declare-LAST residual clause. NOT ENACTED.** Ruled *"one clause in declare-LAST"*
    (the clause is structural and survives P7's dead numbers — `:3448` is explicit that *"the
    proposal is untouched and must not die with its evidence"*).
    `grep -n "declare.LAST|2c/2d/2f are skipped|#N−1" knowledge/_RUNBOOK-capture-ritual.md` →
    **0 hits.**
- **⇒ THE STRUCTURAL HALF, WHICH IS THE PART WORTH DAVE'S TIME.** `knowledge/_rulings.json` is the
  store `_governs.py` reads, and #127 spent real effort repairing its pointer forms (30 red entries,
  `_LIVE-STATE.md:457`, the anchor-pointer build). **Its 65 `"id"` entries are `ds-*` plus
  `s110-D1` onward. There is no ruling id below `s110` and none for any dream-pass P-item** —
  `grep -n "dream" knowledge/_rulings.json` → **0 hits**. So the six rulings above are not
  *late*; they are **not in the system that would notice they were late.** This is precisely the
  two-tier hypothesis the #89 correction declared and could not test (`:3371` — *"P2/P3/P4/P5/P7 are
  UNTESTED against this hypothesis. It is a strong hypothesis, not a class."*). **Tested now, on all
  six: it holds on all six.**
- **⇒ AND THE LANE'S OWN CHARTER SENTENCE NAMES THE MISSING STEP.** `_LIVE-STATE.md:38` —
  *"steady-state by design: the weekly task dreams; Dave rules; sessions enact"*. The first two
  clauses have run five times. **The third has a measured record of 0 for 6.**
- ⚠ **What this is NOT.** It is not a re-float: no remedy above is re-argued, re-scoped or
  re-recommended, and P7's dead receipt is not resurrected. It is the *"Claimed-ENACTED vs RUN"*
  hunt run over Dave's own accepted set, which is on the spec's hunt list.
- ⚠ **Declared limit.** Without git I cannot say *when* between #76 and #127 each was last touched,
  only that each is un-enacted **today**. The 51-session gap is real and this proposal does not
  pretend to close it.
- PREVALENCE: **6 of 6 rulings unenacted · 6 of 6 absent from `_rulings.json`** (65 ids read) ·
  2 of them independently re-verified as unchanged by the #90 re-check, 37–38 sessions ago ·
  8 files probed.
- PROPOSED: **one addition, no remedy touched.** Give the six an entry apiece in
  `knowledge/_rulings.json` under the id form already in use — `d0802-P2`…`d0802-P7` (or whatever
  prefix Dave prefers; the *form* is the ask, not the string) — each carrying `date: 2026-08-02`,
  Dave's ruling text, `status: ruled`, `enacted: false`, and an anchor pointer to
  `notes/_MEMENTO-DECISIONS.md#I'll go with all your recommendations`. **That is the whole
  proposal.** It enacts none of the six, re-opens none of them, and changes no gate — it makes them
  *visible to the instrument that already exists*, so a later session can close them without a
  dream pass having to re-find them. ⚠ **Do NOT bundle any of the six remedies into the same
  motion** — several are Dave's guards (`_git_commit.sh` especially) and this pass has no shell to
  verify a change with. ⛔ **And note the round-trip hazard:** `_rulings.json` is the file whose
  serializer produced a 2,310-line diff from a one-field edit at #126 — assert byte-identical on an
  unchanged round-trip before writing.
- status: floated

---

### P2 — **The residual's carry list has rolled FOURTEEN times, eight of its items are unchanged since the TENTH roll, and the ordinal that counts them is hand-typed prose that nothing reads**

- EVIDENCE:
  - `_CHAIN.md:62` (live, for #128) — *"⬛ **⑨ carried (FOURTEENTH roll):** fall-through class ·
    `s116-D4`/`D5` · `s114-D2` · stale-mount seam · P4 chain trim · 89-D2 · `ds-032` · `ds-025` ·
    boot-rent plan · G4 ratify · P1 confirm-to-open · 3 chart-meta provenance-enum edits."*
  - `_GM-ARCHIVE.md:66` (the #124 wrap) — *"⬛ **③ carried: `s116-D4`/`s116-D5` · `s114-D2` ·
    stale-mount seam · P4 chain trim · 89-D2 enactment · `ds-032` · `ds-025` · boot-rent plan ·
    attribution re-probe (**TENTH roll**)."* Independently corroborated in a second file:
    `_LIVE-STATE-ARCHIVE.md:35`, same list, same **TENTH roll**.
  - **Diffed by hand: eight items are identical across the two** — `s116-D4` · `s116-D5` ·
    `s114-D2` · stale-mount seam · P4 chain trim · 89-D2 · `ds-032` · `ds-025` · boot-rent plan
    (nine, counting `s116-D4`/`D5` separately). **The counter advanced TENTH → FOURTEENTH; the
    content did not.** One item left the list (attribution re-probe, closed at #124 per the memory
    index) and three joined (G4 ratify · P1 confirm-to-open · the 3 chart-meta enum edits) — so the
    list is **growing net**, not draining.
  - **The oldest entries date the drift.** `_LIVE-STATE.md:393` — *"**`s116-D4` / `s116-D5`** — ruled
    #116, unenacted."* That is **eleven sessions**. `89-D2` is on the memory index as
    *"⬛★★ #89-D2 RULED-NOT-ENACTED — lives only in `_MEMENTO-DECISIONS.md`; the store's count ≠
    Dave's open rulings"* — **thirty-eight sessions**, and its hook already says the store cannot
    see it, which is P1's finding arriving from a second direction.
  - **The counter is in the AUTHORED half, not the generated half.** The two residual lines sit
    adjacent: `_CHAIN.md:61` is stamped *"residual (**GENERATED #127**) … — `_roll_state.py`"*, and
    `_CHAIN.md:62` — the carry list and its ordinal — is not. `_roll_state.py`'s own docstring
    (`:5`) scopes it to *"ONE canonical line — the roll-residual"* for **2c/2d/2f**; `grep -n "roll"`
    across that file returns nothing that reads a carry list. ⇒ **`FOURTEENTH` is a word a human
    increments, and no gate, selftest or build step consumes it.**
  - ★ **This is the exact failure mode flagged AT the ruling that created the newest of these
    clauses.** `notes/_MEMENTO-DECISIONS.md:3380`, appended by Dave's own P7 acceptance: *"⚠ Flagged
    at ruling: this is the 3rd–4th 'declare it in the residual' clause. **Watch the residual becoming
    where things go to be declared and then forgotten.**"* Six days on, the residual carries fourteen
    rolls of items nobody has closed. **The prediction was written down, and it came true in the same
    file that recorded it.**
- ⚠ **Honest scope.** Every one of these items is genuinely declared — none is hidden, and the
  discipline of naming them at each wrap is working exactly as designed. The finding is that
  **declaring is the only thing that happens to them**, and the one number that would make the
  duration legible (`FOURTEENTH`) is prose.
- PREVALENCE: **14 rolls; 8–9 items identical across the 4-session span TENTH→FOURTEENTH**, verified
  in 3 files (`_CHAIN.md`, `_GM-ARCHIVE.md`, `_LIVE-STATE-ARCHIVE.md`) · 2 items dated to #116 and
  #89 from the live spine and the memory index.
- PROPOSED: **the cheapest possible consumer, and nothing else** — extend the carry line's own format
  to carry each item's *age*, not just the list's ordinal:
  `carried (14th roll): s116-D4 [11] · 89-D2 [38] · …`, the bracket being sessions-since-ruled.
  Roughly one line at the wrap, written where the carry is being written, so the duration is legible
  at the moment of authorship instead of by archaeology across three archives. ⛔ **Explicitly NOT
  proposed:** any threshold, any gate, any auto-escalation, and any judgment about which items should
  close. **Whether a 38-roll item should be closed, re-scoped or archived is Dave's alone** — several
  are on his DO-NOT-RULE list verbatim (`ds-025`, `ds-032`, the boot-rent plan, G4). This makes the
  number visible; it does not act on it. *(If P1's `_rulings.json` entries land, the ages become
  derivable rather than typed — the two compose, and that ordering is the better one.)*
- status: floated

---

### P3 — **This file will be swept into an unrelated session's commit by `git add -A`, for the second consecutive dream pass, and the mechanism that does it is the one Dave already ruled fixed (thin — a prediction, not yet a defect)**

- EVIDENCE:
  - **It happened last time, to this file's predecessor.** `notes/_MEMENTO-DECISIONS.md:3416` —
    *"`notes/_dream/2026-08-02-proposals.md` is **tracked** — swept into `72bc5d5` (*"#76-D1/#76-D2:
    the DV-D12 split, the DV-D18 collision…"*), **a commit with nothing to do with this lane**, by
    `git add -A`. The dream pass's only sanctioned output was committed by an unrelated session that
    never knew it existed."*
  - **The mechanism is unchanged** — `knowledge/_git_commit.sh:227`, `git add -A 2>/dev/null`, the
    only staging call (P1's fifth bullet; same probe).
  - **The lane's output is deliberately ungated**, so nothing else can catch it: `A-D4`
    (`notes/_MEMENTO-DECISIONS.md:19`) — *"`_dream/` stays OUTSIDE the gate glob until it earns its
    own gate … `_capture_gate.py` glob = `notes/*.md` → the subdir is honestly ungated"*.
  - **And #128 is a session that will commit.** `_CHAIN.md:21` names it, and the residual hands it
    nine items; whatever else it does, its wrap runs `_git_commit.sh`.
- ⚠ **THIN, and labelled thin.** This is a *prediction from an unchanged mechanism plus one prior
  instance*, not a measured defect — I have no git and cannot check whether this file is already
  tracked, nor whether the tree is dirty right now. **If #128's wrap commit turns out to name this
  file in a subject about something else, the prediction is confirmed; if #128 commits it
  deliberately, nothing happened.** It is floated at this weight and no higher.
- ⚠ **It is not a re-float of P5.** P5's remedy is ruled and already covered as one of P1's six; this
  is the narrower observation that **the lane's own output is the recurring victim**, which is a fact
  about the dream pass rather than about the script.
- PREVALENCE: 1 prior instance, directly quoted · 1 unchanged mechanism · 3 supporting receipts.
  **Thin by construction.**
- PROPOSED: **one sentence in the dispatch, not in any file** — whoever conducts #128 should name
  `notes/_dream/2026-08-08-proposals.md` explicitly in the wrap's reconcile step, so that if it is
  committed it is committed *knowingly*, in a subject that mentions it. **No code, no gate, no
  ruling.** ⛔ Do **not** add `notes/_dream/` to the gate glob to solve this — `A-D4` is Dave's and
  the subdir being ungated is deliberate.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(x) `CHAIN_BUDGET_TK` being denominated in a retired unit is ALREADY DAVE'S, with an id.**
  `_capture_gate.py:1044` still reads `CHAIN_BUDGET_TK = (4917, 6417)` in **tape**, while the chain's
  own footer reports **15,935 real**. That is not an unnoticed drift — it is `G5` in the generated
  worklist (`_CHAIN.md:113`): *"Four advisory size caps as a set — closes when: Re-measured in real
  (G9 first), then Dave ratifies the set in one pass"*, and the memory index carries it as
  *"⛔ CEILINGS still in TAPE — measure both sides in the ceiling's unit; G5 owns re-denomination."*
  **Correctly homed, correctly owned, do not report it as a finding.** *(P1 cites the GM:125 prose
  only, which is a different object: a hand-authored sentence Dave ruled should be replaced.)*
- **(y) The `_capture_gate.py` 30 pointer entries and the 11 invisible `<path>:<int>` entries are
  DECLARED, NOT MISSED.** `_CHAIN.md:51` and `_LIVE-STATE.md` § OPEN both carry them in full, with
  the honest note that *"a form that cannot fail is not a passing form"* and *"ALL NOT FIXED — Dave's"*.
  This is a red gate being reported red. Not a record defect.
- **(z) `_build_all.py`'s thrice-stale remedy string was left un-re-stamped ON PURPOSE.**
  `_CHAIN.md:54` — *"The comment was corrected; the remedy was NOT — left as EVIDENCE, question
  raised to Dave, because *stale twice ⇒ GENERATE, don't re-stamp*."* A future pass finding a false
  string there should read it as the rule working, not as rot.
- **(aa) The build figure `102 steps / 27 never-green` is GENERATED at both ends** (`s125-D1`,
  `_gen_chain._steps_in`), and demonstrated itself moving 98→102 with nothing typed. The
  never-in-a-green-verdict shortfall is real and declared; it is not a stale claim.
- **(bb) The `size:` stamp at `_CHAIN.md:34` is dated, unit-correct and points rather than restates
  for the chain figure** — *"THE READ-CHAIN FIGURE IS DELIBERATELY ABSENT — its ONE home is
  `_CHAIN.md`'s own generated footer"*. This is P7's remedy shape already present for the chain term.
  ⚠ Whether the GM/LS halves (50,542 / 58,731, *"measured 2026-08-07 #127"*) are still accurate could
  **not** be checked this pass — no tokenizer, no shell. **Unmeasured, not clear** — flagged here so
  the next pass with a shell measures it rather than assuming either way.

---

## Method

**Shape A (Cowork).** Dispatched 2026-08-08 (date supplied by the conductor from the host's `date`,
not recalled), session `local_a590b514-eb6a-4b64-a637-48445c1521db`.

**⛔ THE COVERAGE GAP, STATED FIRST BECAUSE IT IS THE BIGGEST THING ABOUT THIS PASS.** The prior pass
covered through **#76**. The chain is at **#127**. **Fifty-one sessions are uncovered**, and the
transcript window is fifteen — so **at best 15 of 51 sessions (29%) are reachable by transcript, and
the other 36 are reachable only through repo artefacts.** Every proposal above is therefore built on
**repo forensics**, and each states what it can and cannot claim about *when* something drifted.
⚠ **A finding that lives only in a #77–#112 chat and left no artefact is invisible to this pass.**

**Read (repo, this pass, in spec order):** `MEMORY.md` index (hooks only, as injected context) ·
`.claude/agents/dreamer.md` · `_CHAIN.md` **in full** (the whole contract; GM and `_LIVE-STATE.md`
were deliberately NOT opened whole — `_CHAIN.md:10` forbids exactly that reflex, and both were
reached by targeted grep instead) · all four prior proposals files (headings + Method + every
checked-clear list, before hunting) · `notes/_MEMENTO-DECISIONS.md` **§ 3355–3475 only** (the pass-4
entry, its same-window correction, and the #90 three-verdict re-check — the file is 461 KB and
cannot be read whole by a file tool) · `knowledge/_capture_gate.py` (targeted) ·
`knowledge/_git_commit.sh` (targeted) · `knowledge/_RUNBOOK-capture-ritual.md` (targeted) ·
`knowledge/_rulings.json` (id census) · `knowledge/_roll_state.py` (targeted) ·
`notes/_GAUGE-LOG.md` (all `consult-receipts` strata) · `GOOD-MORNING.md`, `_LIVE-STATE.md`,
`_GM-ARCHIVE.md`, `_LIVE-STATE-ARCHIVE.md`, `_FUTURE-STATE.md` (grep only).

**Transcripts — 1 read, 14 NOT read, and this is a real shortfall, not a choice I am dressing up.**
`list_sessions` (limit 20) returned #127 → #109 plus one stub. I read **`local_326fddf1` (#127)**,
final turns only. **The other fourteen were not read.** Two honest reasons, in order of weight:
(1) **#127's wrap is available in higher fidelity as an artefact** — `_CHAIN.md:44–88` and
`_LIVE-STATE.md`'s LATEST DELTA carry the whole banner with evidence-per-claim, which is strictly
better than a turn-level transcript; the same is true of #109–#126 via `_GM-ARCHIVE.md` and
`_LIVE-STATE-ARCHIVE.md`. (2) **Cost:** these sessions' closing messages are very long, and a
fifteen-transcript read at a useful `limit` would have consumed the window this file needed.
⚠ **The consequence, named:** *chat-only material — a ruling spoken and never inscribed — is the one
class this pass could not hunt*, and it is precisely the class the #89 two-tier hypothesis is about.
**A pass with more room should read the fourteen.** I have not padded any prevalence figure to
disguise this: every `N of M` above counts files or grep hits, never transcripts.

**Where the fidelity ceiling bit.** The known Shape A ceiling (turn-level; tool calls as bare names,
no arguments or results) applies to the one transcript read, and nothing in this file rests on it —
#127's transcript is cited nowhere as evidence; it was read as a cross-check and it agreed with the
repo.

**Where the NO-SHELL ceiling bit — three named consequences.** The 2026-08-02 pass had read-only
shell and recorded that two of its findings existed only because git was readable. This pass had
neither. (1) **No commit history**, so P1 can say "unenacted today" but not "unenacted since when",
and P3 cannot check whether this file is already tracked. (2) **No tokenizer**, so every size claim
above is *quoted from an artefact's own stamp*, never measured — which is why the GM/LS `size:`
halves are recorded in (bb) as **unmeasured rather than clear**. (3) **No `git status`**, so I do not
know the working tree's state and have made no claim about it — [[stale-mount-corroborates-a-stale-premise]]
was the #89 failure and the honest response to having no clock is to make no dated claim at all.
⚠ **One reconcile I COULD run, and did:** `MEMORY.md`'s highest session hook (**#127**) vs
`_CHAIN.md`'s *"YOU ARE #128"* — **consistent.** The two numbers agree, so the mount is not stale in
the #89 sense. That is the control the #89 correction invented, run before the first finding.

**Do-not-re-float discipline.** All four prior proposals files were read (headings, Methods, and the
2026-08-02 checked-clear list (q)–(w)) **before** any hunting, along with the ledger's pass-4 entry,
its correction, and the #90 P4/P6/P7 re-check. **Nothing above re-argues a ruled remedy.** P1 reports
*non-enactment of rulings*, which the spec lists as a hunt (Claimed-ENACTED vs RUN / dropped loops);
P2 is a new object (the carry list, which no prior pass examined); P3 is labelled thin and is scoped
to the lane's own output rather than to P5's mechanism. The P-set collision recorded at `:3450` is
noted and this file's P-numbers are **deliberately not reused from either set** — cite them as
*"2026-08-08 P1/P2/P3"* or they will collide with the other two live sets.

**Scope exclusions honoured.** Dream-lane mechanics (schedule, fire cadence, the lane-wrap-gate seam)
are the standing exclusion and nothing above proposes on them — ⚠ though one observation is named and
**deliberately not floated**: `_CHAIN.md:55` records the dream pass as **OVERDUE** at #127, while
`S-D1`'s schedule is weekly-Sunday and the last pass was Sunday 2026-08-02. Either the weekly task
has stopped firing or "overdue" is the wrong word. **That is lane mechanics; it is named here for
whoever wraps and nothing more.**

**Governance.** **One file written: this one.** `notes/_dream/2026-08-08-proposals.md` did not exist
(`Glob notes/_dream/*` returned exactly the four prior files), so it is plain-dated, not versioned.
No edits anywhere else — not memory, not notes, not canon, no git, no scratch files, nothing to clean
up. Every proposal carries `status: floated`. **Nothing here promotes itself.**
