# Dream pass 12 — floated proposals

provenance: `local_ed8e4d52-5c5e-4b62-8a05-6a9addcf0960` · 2026-09-13
status: floated

*I PROPOSE ONLY. Nothing here self-promotes; promotion is Dave's alone on reading this file
(derivation-governance). Every RULED row in `knowledge/_rulings.json` (453 ids, through `s268-D8`)
and `notes/_MEMENTO-DECISIONS.md`, and every checked-clear item at the end of EVERY prior proposals
file — pass 1's (a)–(d) … pass 11's (hh1)–(hh8) — was read before hunting. **Proposals from passes
6–11 that are still FLOATED are referenced where new evidence bears on them, never re-floated** (see
ii1, ii2, ii3). Standing exclusion held: dream-lane mechanics (cadence, conductor sequence, the
lane's §🔀 row, `_dream/` gating) are barred from floating — cc6/dd7/ee7/ff7/gg9/hh8 precedent, see
(ii8).*

★ **Shape A (Cowork), scheduled Sunday 07:10 fire, ON TIME** (pass 11 = 2026-09-06). Date from `date`
on the host (`Sun Sep 13 07:12:39 BST 2026`), corroborated mechanically by
`notes/_dream/_MEMORY-GRADES.json` `"refreshed_at": "2026-09-13T07:11:34"` — the conductor's B3
refresh arm, run before I was dispatched.

⚠ **Ground truth at this seat, stated before any finding.** Tree clean but for
`notes/_dream/_MEMORY-GRADES.json` (the B3 arm's own sidecar — I did not touch it); HEAD =
origin/master = `b6b63db`, nothing unpushed. **#268 is UNWRAPPED** — 30 commits across 2026-09-11
and 2026-09-12, and the spine's ★ LATEST banner is still #267. That is a wrap not yet run, not
ritual drift, and I have not treated it as a finding (ii4).

⚙ **This seat HAS a shell**, unlike pass 11's (hh6). Every number below is reproducible with a
command quoted in § Method.

Ranked by prevalence, highest first.

---

### P1 — The stop line has **three live values in four authorities**, and the one the live instrument actually reports is **scraped by regex out of last session's wrap prose**: `_checkin.py` reads `_CHAIN.md`, whose only matching string today sits inside #267's *breach narrative* and says **180,000 unconditionally** — while the runbook that GOOD-MORNING calls the band table's ONLY copy still says **~190,000**, Dave's own `s260-D2` says **180,000 delegated / 150,929 inline**, and the ★★★ memory hook says **150,929**

- EVIDENCE:
  - **The ruling.** `knowledge/_rulings.json` `s260-D2` (2026-09-08, `"by": "Dave"`):
    *"When the wrap is DELEGATED the advisory start-wrap-by line is 180,000 real; when the wrap runs
    INLINE the advisory stays 150,929."* Its `"governs"` field names
    **`knowledge/_checkin.py` · `knowledge/_gauge_tokens.py` · `notes/_GAUGE-LOG.md`**.
  - ⛔ **Neither named instrument contains either number.**
    `grep -n '180_000\|180,000\|180000\|DELEGAT' knowledge/_checkin.py knowledge/_gauge_tokens.py`
    → **0 hits**. `grep -rln 's260-D2' --include='*.py' knowledge/ apollo-spider/` → **0 files**;
    the same over `knowledge/_RUNBOOK*.md` → **0 files**. The ruling lives in `_rulings.json` and in
    rolling prose, and in nothing that runs.
  - **How the live figure is obtained — a regex over a Polaroid.** `knowledge/_checkin.py:320`
    `CHAIN_STOP_RE = re.compile(r"stop line\s*\**\s*([\d][\d,]*)")`; `:410`–`:421` sets the `STOP`
    field from the FIRST match in `_CHAIN.md`, with the comment *"⛔ Never a literal typed here: a
    constant invented by this script would be a stop line nobody ruled"*; `:425`–`:437`
    (`derive_budget`) prints `⛔ PAST the stop line by N`. **`_CHAIN.md` is GENERATED** from GM's
    header + ★ LATEST banner and LS's ⏱ LATEST DELTA (GM header, line 2–3).
  - **What it matches today — exactly one string, and it is a sentence about a breach.**
    `_CHAIN.md:92` reads *"…past the `s260-D2` delegated **stop line 180,000** — and first-hand at
    THIS seat `_checkin.py` reads 201,554 real…"*. Run the script's own regex over the file: **1
    match, `180,000`**. So the number every seam check-in in every session — delegated or inline —
    is measured against is a figure quoted inside #267's post-mortem narrative.
  - **It is a by-product of the roll, and it has flipped once already.** Walking the last 18 commits
    that touched `_CHAIN.md`: `150,929` alone from 2026-09-07 (`b15b7d9`) through 2026-09-08
    (`7647aaf`), **both** numbers at `fe17820` (09-09), and **`180,000` alone** from `79a2604`
    (09-09) to HEAD — **six committed rolls**, i.e. every session since #263 has had the DELEGATED
    figure reported to it unconditionally. `s260-D2`'s inline half is un-representable in a
    one-number scrape.
  - ⛔ **The third value, in the file GM says is the only authority.**
    `knowledge/_RUNBOOK-context-gauge.md:357` — *"### ★★ THE `s214-D4` CONDITIONAL ADVISORY —
    **~190,000** on delegated-wrap days (ARMED #217)"*, `:369` — *"In force on a delegated-wrap
    session: advisory **~190,000**"*, and the section's own clause `:376`–`:378`: *"Generated
    consumers lag by design … **the figure in force is the one this section states for the session
    type**"*. `GOOD-MORNING.md:111` points at this file as *"the band table's ONLY copy; grep it,
    never recall it."* **`190,000` appears 3 times in it; `180,000` appears 0 times; `s260-D2`
    appears 0 times.** The ruling that superseded it did not reach it, and the ruling's `governs`
    list does not name it.
  - **The fourth, in the boot-loaded memory stub.** `MEMORY.md:28` publishes
    *"★★★ Stop line 150,929 ADVISORY; WALL 200K"* → `stop-line-repriced-93.md`, whose body carries
    150,929 / 200,000 / 256,000 and ends *"No constant was moved."* It names `s190-D2` and `#127`
    and **not** `s260-D2`. `notes/_dream/_MEMORY-GRADES.json` grades it **FRESH**, because the probe
    is *"all 5 paths named in the hook FILE resolve"* — paths, not claims (see P4).
  - ⚠ **Honest limit.** The three values are not all wrong in the same direction and I am not ruling
    which is right: `s260-D2` is the newest and is Dave's, so I read 180,000/150,929 as in force —
    but that is a reading, and which authority wins is his.
- PREVALENCE: **4 authorities, 3 distinct values** for one figure · the divergence is **5 days and
  8 sessions old** (`s260-D2` 2026-09-08 → #268) · the live scrape has been the delegated-only value
  for **6 committed `_CHAIN.md` rolls** · **0** of the 3 files the ruling names as governed contain
  it. All counts mechanical, whole files.
- PROPOSED: the **generate-it** triage (`s129-D5` #1), smallest form. **(a)** Put the pair where the
  script can see it: two constants in `knowledge/_gauge_tokens.py`
  (`STOP_INLINE = 150_929`, `STOP_DELEGATED = 180_000`, both citing `s260-D2`), and have
  `_checkin.py` prefer them, keeping `CHAIN_STOP_RE` only as the declared fallback — this is what
  `:410`'s own comment asks for and the opposite of inventing a number. **(b)** One line in
  `knowledge/_RUNBOOK-context-gauge.md:357`–`:371` recording that `s260-D2` superseded `s214-D4`'s
  ~190,000 with 180,000 (by ADDITION, ADR-0017 — do not erase the armed-at-#217 record).
  ⛔ Explicitly NOT proposed: moving 200,000 or 256,000, re-dialling either advisory, or editing
  `_CHAIN.md` (it is generated). Which number is authoritative stays Dave's — (a) and (b) only make
  the answer he already gave reachable by the machine.
- status: floated

---

### P2 — A **717-token** boot overshoot is a named, blocking, mutation-tested gate arm with its own discharge grammar; a **104,364-token** FILL overshoot is a sentence. The working ceiling was passed in **3 of the last 4 sessions that measured FILL**, every breach was honestly written down, and the string `FILL` appears in `_capture_gate.py` exactly **twice — both times as a label**

- EVIDENCE:
  - **The breaches, from the log and the chain, not from prose about them.**
    `notes/_GAUGE-LOG.md:3206` (#264): *"FILL: **214,299 real** DECLARED by the conductor at the
    brief cut (96 turns) · 221,197 real measured first-hand"*, *"34,299 OVER the `s260-D2` delegated
    stop line of 180,000 and 21,197 over the 200,000 working ceiling"*. `:3248` (#266):
    *"FILL: **304,364 real** … **THIS IS A BREACH AND IT IS RECORDED AS ONE: 124,364 OVER** the …
    180,000 and **104,364 OVER the 200,000 working ceiling**"*. `_CHAIN.md:92` (#267):
    *"`_checkin.py` reads **201,554 real** over 75 turns, which is **also past the 200,000 working
    wall**"*.
  - **Nothing grades any of them.** `grep -c 'FILL' knowledge/_capture_gate.py` → **2**, and both
    are inert: `:2674` is a comment about QUOTA-vs-FILL vocabulary and `:2809` is
    `TESTIMONY_LABELS = ("META", "ERRORS", "PRE-FLIGHT", "PAIR", "CLOSED", "BAND", "FILL", "OUTCOME")`
    — a label tuple. **No arm parses a measured FILL, and none compares one to `BUDGET_WORKING`.**
  - **The budget arms that DO exist grade a PREDICTION, never a measurement.**
    `_capture_gate.py:1349`–`:1387` is the pre-flight band: `stop_at = gauge.BUDGET_WORKING −
    terms["wrap"]`, `if total > gauge.BUDGET_HARD` … `elif total > gauge.BUDGET_WORKING` — where
    `total` is the *estimate* parsed out of the pre-flight string. A session may therefore price
    itself green and close 104,364 over, and every gate stays green.
  - ⛔ **The asymmetry, measured against the sibling term.** Boot has
    `BOOT_CEILING_TK = 70_000` (`knowledge/_gauge_tokens.py:227`, `s241-D1`, shrink-only), a
    breach-detection arm, a declared-discharge grammar (`_capture_gate.py:3966`–`:4002`,
    `s244-D1`), and a per-breach discharge check (`:4347`–`:4368`). #267's boot was **70,717 —
    717 over** and that is written up as a third consecutive breach in the ★ LATEST banner. **The
    same banner records FILL 201,554 against a 200,000 wall in the next clause, with no arm behind
    it.** The cheaper number is the enforced one.
  - **The wall is Dave's own, in his words**, quoted in the memory store
    (`stop-line-repriced-93.md`): *"the cut off that you have to squeeze the wrap is 200k not 150
    you have space"* — inscribed as `s190-D2`.
  - ⚠ **Thin where it is thin, and declared.** `notes/_GAUGE-LOG.md` blocks for **#261** and **#262**
    carry **no FILL figure at all**, so the series has two holes; and the log lags the chain by one
    session by design ((dd2), so #267's block is not there yet). I therefore say **3 of the last 4
    sessions that produced a reading**, not "3 of the last 4 sessions".
- PREVALENCE: **7** log blocks since the ruling (#260…#266); **5** carry a declared conductor FILL,
  **2** carry none; **2 of those 5** are past the 200,000 working wall, **+#267** from the chain =
  **3 of the last 4 readings**; **6 of 11** readings since #250 are past the 150,929 advisory.
  **0** gate arms over any of it, against **~100 lines** of machinery for the boot term.
- PROPOSED: the **named re-checker** triage (`s129-D5` #2), advisory first, and deliberately smaller
  than the boot machinery. **(a)** One arm in `knowledge/_capture_gate.py`'s wrap checks that parses
  the `post-mortem #N:` block's declared FILL — the figure `s241-D2` already requires be stated once
  — and **WARNS, named, when it exceeds `gauge.BUDGET_WORKING`**, with the same declared-discharge
  posture `s244-D1` gave the boot ceiling (a breach that is DECLARED in the block passes; a silent
  one fails). **(b)** Separately, and Dave's because it is a tier decision: whether that arm should
  ever block. ⛔ Explicitly NOT proposed: moving 200,000 or 256,000, restricting delegation, or
  making the pre-flight estimate binding.
- status: floated

---

### P3 — The record corrects a date conflation in capital letters — *"THERE ARE THREE DATES, NOT ONE … NEVER CONFLATE THEM AGAIN"* — and then inscribes two of the three as **relative phrases with no anchor**: *"the small demo is NEXT WEEK"* and *"David Rice is ~2 WEEKS OUT"*, now published at **10 sites across 5 surfaces** including the generated retrieval index and the boot-loaded memory stub, while the only absolute date of the three is both **past and overtaken**

- EVIDENCE:
  - **The sentence, `_CHAIN.md:72`** (and identically in `_LIVE-STATE.md` and `GOOD-MORNING.md`'s
    ★ LATEST): *"⛔★★★ **THE OPENER'S PREMISE WAS WRONG AND DAVE CORRECTED IT — THERE ARE THREE
    DATES, NOT ONE.** **v1.0.9 releases Friday 2026-09-11** · **the small demo is NEXT WEEK** ·
    **David Rice is ~2 WEEKS OUT**. … **NEVER CONFLATE THEM AGAIN.**"*
  - **Where it is published:** `_CHAIN.md` 2 lines · `_LIVE-STATE.md` 2 · `GOOD-MORNING.md` 1 ·
    `knowledge/_memento-index.json` 4 — **9 sites in the repo**, plus `MEMORY.md:3` in the memory
    store (*"⛔ v1.0.9 Fri / small demo NEXT week / Rice in ~2 weeks — three dates, never conflate"*)
    = **10 across 5 surfaces**. The index copy means retrieval serves it
    [[read-chain-is-where-staleness-is-free]].
  - **The arithmetic that makes it a defect rather than a nit.** The sentence was written
    2026-09-10. Read that day, *"next week"* = w/c 2026-09-14 and *"~2 weeks"* ≈ 2026-09-24. Read
    **today** (2026-09-13) it still resolves roughly right; read at the next wrap-but-one it
    resolves a week later, **and nothing in the string says which Thursday it was written on**.
    The chain is the one surface a cold session is contracted to read and the one surface that rolls.
  - **The absolute member of the trio is already false as a plan.** *"v1.0.9 releases Friday
    2026-09-11"* — by that Friday, `apollo-spider/dist/` had gained **v1.0.11** (`cacaa19`),
    **v1.0.12** (`e68920d`) and **v1.0.13** (`117b33c`), all dated 2026-09-11, on top of v1.0.10
    (`de8ed57`, 09-10). So the banner's one checkable date describes a release plan that three
    later releases overtook **on the day itself**, and the spine has not been rolled since.
  - **The class already bit once, in this exact sentence.** Its own text records that **#266
    collapsed all three dates into "Friday"**, which is what the correction exists to prevent —
    *"a release deadline … doing duty for a rehearsal deadline and an audience deadline at once."*
    The remedy chosen was prose emphasis, and prose emphasis does not carry an anchor date.
  - ⚠ **Honest limit:** I did not find any absolute date for either the small demo or the Rice
    session anywhere in the repo (`grep -o 'Rice[^.]\{0,90\}' _CHAIN.md` returns only *"Rice ~2
    WEEKS"* / *"Rice is ~2 WEEKS OUT"*; the run-of-show page carries authoring dates only). **If
    Dave has told anyone a calendar date, it is not in the record**, and that absence is the
    finding's sharpest edge — the demo is the project's declared focus.
- PREVALENCE: **10 sites / 5 surfaces**, carried unchanged for **3 days and 1 session** (#267 →
  #268, unwrapped); **2 of 3** dates are relative; **1 of 3** absolute and overtaken; **0** absolute
  dates for the two that matter. Grep over the whole tree, `_tmp` and `dist` excluded.
- PROPOSED: the **expiry-stamp** triage (`s129-D5` #3), one sentence, at the next 2c/2d roll — restate
  the trio **as at its own authoring date**: *"as at 2026-09-10: v1.0.9 Fri 2026-09-11 (SUPERSEDED —
  v1.0.13 shipped the same day) · small demo w/c 2026-09-14 · David Rice ≈ 2026-09-24, DATE NOT
  CONFIRMED BY DAVE"*. Two of those three are derivations from his relative words and must be
  labelled as such, not promoted to fact. **And the one thing only Dave can close: the actual date
  of the small demo and of the Rice session** — if he gives them, they belong in
  `notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html`'s header, not in a rolling banner.
  ⛔ Not proposed: inventing either date, or editing `knowledge/_memento-index.json` (generated).
- status: floated

---

### P4 — The wrap ritual writes the session's memory hook **before** Dave answers the session's last questions, so the hook's *"Open, Dave's"* list can be false within minutes — and it was: **2 of the 3 open items** in the most recent ★★★ hook are closed in the repo, one of them by a ruling inscribed **5 minutes 38 seconds** after the hook file was written — and the grader calls the file **FRESH**, because it grades whether paths resolve, not whether claims are true

- EVIDENCE:
  - **The hook, as it is published.**
    `v1010-released-edges-ratified-kg-sphere-267.md:25` in the memory store: *"**Open, Dave's:**
    lane N changed `_validate_compose.py:87` to read `var(--x, fallback)` as resolved — **a gate
    change without a ruling, flagged**; SC dig with default families = 0 neighbours (auto-switch?);
    v1.0.10 canon regen not in the zip → v1.0.11"*. `MEMORY.md:3` repeats the first item in the
    boot-loaded ⛔/★★★ stub: *"gate change at `_validate_compose.py:87` unruled"*.
  - ⛔ **Item 1 was ruled the same evening.** `knowledge/_rulings.json` `s267-D4`: *"`_validate_compose.py`
    reads `var(--x, <fallback>)` as RESOLVED … Lane N's change at `_validate_compose.py:87` (commit
    `57ddff1`) **STANDS**"*, `"says"`: *Dave at #267 … **"1 push 2 accepst"***. Inscribed at
    `ceef5b9`, **2026-09-10 21:26:49**. The hook file's mtime is **2026-09-10 21:21** — the ruling
    landed **5m38s later**, and the repo spine says so in three places
    (`_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md` all carry *"`s267-D4`: `var(--x, fallback)`
    RESOLVED"*).
  - **Item 3 is closed too.** *"canon regen not in the zip → v1.0.11"*: v1.0.10's packed
    `canon/canon.css` hashes `b5e66eb545e0…`, **v1.0.11's `f37a65d77ccf…`**, v1.0.13's
    `05098f99941a…` — **byte-identical to the repo's `knowledge/canon/canon.css` today** (same
    sha; `nv-item` present 59 times, the #267 regen's own probe). The fast follower shipped on
    2026-09-11. **Item 2 (SC dig, default families = 0 neighbours) I could not close** and report as
    still open.
  - **The mechanism is the ritual's ORDER, not carelessness — and the transcript shows it plainly.**
    In #267 the conductor's closing turn says *"**Memory hook written.** Wrap lane brief will
    name…"* **in the same message** that puts the two questions to Dave (*"1. Push? 2. One unruled
    gate change to accept or revert"*). Dave's answer — *"1 push / 2 accepst"* — is the **next**
    turn. The ★ LATEST banners record this order as a virtue: *"✅ MEMORY DONE at his seat"* (#267
    ⑥), *"✅ MEMORY DONE at conductor's seat"* (#266 ⑥). **A record written before the answer cannot
    contain the answer.**
  - **And nothing downstream can see it.** `notes/_dream/_MEMORY-GRADES.json` grades this file
    **FRESH**, why-string: *"all 7 paths named in the hook FILE resolve (probe: os.path.exists +
    repo basename index)"*. The grading unit is `s188-D1`'s — the hook FILE's backticked repo paths.
    **Every path in a hook whose claims have all been overtaken still resolves**, so the grade is
    structurally incapable of falling for this failure mode. That is not a bug in `s188-D1`; it is
    the boundary of what it measures, and nothing measures the other side.
  - ⚠ **Thin where it is thin.** **59** files in the memory store carry an
    `unruled|not ruled|ruling owed|awaits his` string — a candidate population, **not** a measured
    defect rate. I verified **exactly one file exhaustively** (3 items, 2 closed). Do not read 59 as
    59 defects.
- PREVALENCE: **2 of 3** open items false in **1 of 1** hook checked exhaustively — the **newest**
  ★★★ hook, inside the 52-hook graded population and inside `s179-D1`'s alert scope; **1 of 1**
  grading probe blind to the class by construction; **59** files carry a same-shaped claim,
  unsampled.
- PROPOSED: **give it a named re-checker** (`s129-D5` #2), and the cheapest possible one, because the
  write order is Dave's to change and I am not proposing that. **(a)** One line in
  `knowledge/_RUNBOOK-capture-ritual.md`'s memory step, in the same register as the dream-11 P3(b)
  clause already sitting at `:450`: *an "Open, Dave's" item written before his answer must be
  written as a QUESTION PUT (`"put to Dave at the wrap call"`), never as a state of the world; and
  the wrap's final step re-reads that list against `_rulings.json` and strikes what the session's own
  rulings closed.* **(b)** Alternatively, and simpler if he prefers one move to a rule: **write the
  hook after the last ruling**, which is a one-step reorder of the ritual — his call, and the
  reason I am not proposing it as the primary is that the current order is what makes the hook
  survive a wrap that runs out of window. ⛔ Explicitly NOT proposed: editing any memory file (this
  seat cannot write to the store), changing `GRADE_AGING_DAYS`, the alert surface, or `s188-D1`'s
  grading unit.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(ii1) Pass 11's P2 and P4 are ENACTED, P1 is HALF-enacted, and I re-floated none of them.**
  **P2 landed at #256:** `knowledge/_gardener.py:705`–`:709` now carries the comment *"dream-11 P2
  (enacted #256)"* and `_HOOK_LINK_RE`; `parse_memory_index:733` iterates **every** link on a line.
  **P1(a) landed:** `_MEMORY-GRADES.json` carries a `"population"` block —
  `{"prev": 33, "now": 52, "delta": 19, "threshold": 5, "line": "POPULATION CHANGED: 52 hooks this
  run vs 33 last run (+19, threshold ±5)"}` — and it **fired this morning**, exactly as proposed.
  **P1(b) (grade the overflow file too) did not land** and remains Dave's, as pass 11 said. **P4 is
  discharged:** `knowledge/_SCREEN-GATE.md`'s last line now reads *"10 subject(s) on record."* and
  `ls knowledge/_screen-gate/ | wc -l` → **10**.
- **(ii2) Pass 11's P3 got its PROSPECTIVE half and not its retrospective half, and the claim has
  grown 11 → 71 occurrences. Reported as corroboration; NOT re-floated.** P3(b) is in the runbook
  verbatim, `knowledge/_RUNBOOK-capture-ritual.md:450`–`:457`: *"⛔ **A STRAY'S PROVENANCE IS A SEAT
  LIMIT UNTIL IT IS SEARCHED** (dream-11 P3(b), #256)"*. P3(a) — restating the live copies — did
  not happen, and `grep -ro 'provenance unknown'` (excluding `_tmp/`, `_to_delete/`, `dist/`) now
  returns **71 occurrences across 7 files**: `knowledge/_memento-index.json` **40** ·
  `_CARRIES.md` **21** · `notes/_GAUGE-LOG.md` 3 · `_LIVE-STATE-ARCHIVE.md` 3 · `_LIVE-STATE.md` 2 ·
  one brief · the runbook's own quotation of it. ⚠ **The mechanism worth Dave's eye is the 21:** the
  carry list re-publishes the sentence on every roll, so a false claim's footprint grows linearly
  with sessions. That is pass 11's P3 with a bigger number, which is why it is here and not above.
- **(ii3) Pass 6's P1 is UNCHANGED — still exactly 21 — and pass 9's P1 is UNCHANGED at #266.**
  `knowledge/_rulings.json` today: **453** rulings, **183** distinct `status` strings, **21** still
  carrying the #119 metadata-sweep sentence verbatim and **250** the plain `"ruled"`. And the
  pre-flight `⛔ NOT CAPTURED` streak reaches **#266** (`notes/_GAUGE-LOG.md:3246`), **160**
  occurrences in the file. Both referenced, neither re-floated.
- **(ii4) #268 is unwrapped and that is not a finding.** 30 commits `ee864de…b6b63db` across
  2026-09-11 and 2026-09-12, tree clean, HEAD = origin/master. The session's own last turn offers
  *"or 'wrap' and I'll close #268"*, so the wrap is pending, not skipped. ⚠ What IS worth Dave's
  eye, and is already his by the three WRAP DATE SPLIT banners at `GOOD-MORNING.md:9`–`:11`: **#268
  is the first session to span two calendar days of WORK** (not merely a midnight-spanning wrap), so
  #241's ruling-shaped question — what a date-split wrap should stamp — will arrive at its next wrap
  in a fourth shape. I am not floating it: it is carried, aged and his.
- **(ii5) I nearly filed a false finding about the release zips, and the correction is the record.**
  `git ls-files apollo-spider/dist | tail -5` appears to stop at v1.0.9, which reads as "v1.0.10–13
  are untracked". **It is lexicographic sorting** — `v1.0.10`…`v1.0.13` sort before `v1.0.2`. All
  four are committed (`git show --stat cacaa19|e68920d|117b33c|de8ed57` each shows the blob added)
  under the deliberate `.gitignore:49` exception. Recorded so the next pass does not spend the
  same ten minutes.
- **(ii6) The dispatch's own extract is in the repo, and it is not mine.**
  `_to_delete/_dream12-do-not-refloat.md` exists (the conductor's copy of the do-not-re-float list);
  `_to_delete/` is gitignored at `.gitignore:34`, so it does not dirty the tree. Declared so it is
  not read later as an artefact of this pass.
- **(ii7) What this pass wrote, stated plainly. ONE file — this one.** The conductor ran the B3
  refresh arm before I was dispatched (`"refreshed_at": "2026-09-13T07:11:34"`, population 33→52,
  FRESH 33 · AGING 10 · STALE 2 · UNPROVABLE 7), leaving `notes/_dream/_MEMORY-GRADES.json`
  modified; **I did not touch it, stage it, or revert it.** I logged no `--grade-decision` rows,
  ran no `_gardener.py` arm, no `_checkin.py`, no `_build_all.py`, no `gen_kg_edges.py`, and **no
  git operation of any kind** — every command in § Method is read-only. I wrote **no** memory file
  (this seat cannot write to the store), no canon, no ledger, no `notes/` file but this one. The one
  script I executed, `_capture_gate._carry_items`, was imported read-only to confirm the carry probe
  (ii-adjacent: it returns **412**, exactly the banner's figure).
- **(ii8) Out of scope by standing exclusion, and where I drew the line.** Dream-lane mechanics
  remain barred (cc6/dd7/ee7/ff7/gg9/hh8): I did **not** float the cadence, the conductor sequence,
  the lane's §🔀 row, or `_dream/` gating. ⚠ **P4 sits nearest that line and I judge it clear of it:**
  its subject is the WRAP ritual's memory step and the B3 grader's probe, both of which exist
  independently of this lane — but P4(a) touches `_RUNBOOK-capture-ritual.md`, which the dream lane
  also reads, so the judgment is flagged rather than assumed.

---

## Method

**Read, in the dreamer spec's order.** `.claude/agents/dreamer.md` in full, first ·
`MEMORY.md` (the #242 ⛔/★★★ stub, 47 lines) and the hooks it names where a claim was in question
(`stop-line-repriced-93.md`, `v1010-released-edges-ratified-kg-sphere-267.md`) ·
`GOOD-MORNING.md:1`–`:180` (header, STATE block, ★ LATEST + ★ PRIOR banners, DO THIS FIRST, the
POINTERS block, §A's opening) · `_LIVE-STATE.md` by section heads, the 🛤 LANES block (`:23`–`:66`),
the ⏱ LATEST/PRIOR DELTA heads and the § OPEN headings (`:440`–`:1200`) — the file has single lines
long enough to blow a tool-result budget, so bounded greps were used inside it and that is declared,
not smoothed · `notes/_dream/2026-09-06-proposals.md` in full and every prior pass's `### P<n>`
headings by one ripgrep sweep over `notes/_dream/*.md` · `knowledge/_rulings.json` (453 rows, parsed
with `json`) · `knowledge/_gardener.py` §§ `_HOOK_RE`/`_HOOK_LINK_RE`/`parse_memory_index` ·
`knowledge/_checkin.py:296`–`:437` · `knowledge/_gauge_tokens.py:63`–`:230` ·
`knowledge/_capture_gate.py:1322`–`:1492`, `:2674`–`:2809`, `:3966`–`:4002`, `:4347`–`:4368` ·
`knowledge/_RUNBOOK-context-gauge.md:355`–`:380` · `knowledge/_RUNBOOK-capture-ritual.md:440`–`:460` ·
`knowledge/_validate_compose.py:75`–`:99` · `notes/_GAUGE-LOG.md` §§ #250–#266 ·
`notes/_subreports/2026-09-11-268-cold-run-9.md` head.

**Transcripts: 15 in the window, 2 read, 13 by title.** Shape A, `list_sessions` (25 returned) →
`read_transcript`, window **#268 back to #254** as dispatched. Read: **#268**
(`local_d7264a85`, most recent ~30 turns) and **#267** (`local_14d6f549`, closing 12 turns). The
other thirteen (#266 … #254) were taken **by title only**. ⛔ **Skipped and declared:** nothing in
the window; the two dream-pass sessions in the list (`local_dcd2f425` "Memento dream pass" and
`local_0f07123a` "#253-B sidequest") are outside the numbered window and were not read.
**Fidelity ceiling, and where it bit:** tool calls appear as names with no arguments or results, so
**not one number in this file comes from a transcript.** Transcripts supplied two things only, both
quoted rather than counted: #267's closing turn (P4's write-order mechanism, and Dave's *"1 push /
2 accepst"*) and #268's last turn (*"or 'wrap' and I'll close #268"*, ii4). Every figure was
re-derived against the repo.

**Commands a conductor can re-run, verbatim** (all read-only; nothing below writes):

- `python3 -c "import json;rows=json.load(open('knowledge/_rulings.json'))['rulings'];print(len(rows));print([r['ruled'] for r in rows if r['id']=='s260-D2'])"`
  → 453, and the 180,000/150,929 text
- `grep -n '180_000\|180,000\|180000\|DELEGAT' knowledge/_checkin.py knowledge/_gauge_tokens.py` → **0**
- `grep -rln 's260-D2' --include='*.py' knowledge/ apollo-spider/` → **0** ·
  `grep -rln 's260-D2' knowledge/_RUNBOOK*.md` → **0**
- `python3 -c "import re;print([m.group(0) for m in re.finditer(r'stop line\s*\**\s*([\d][\d,]*)',open('_CHAIN.md').read())])"`
  → `['stop line 180,000']` (one match, at `_CHAIN.md:92`)
- `for c in $(git log --pretty=%h -18 -- _CHAIN.md); do git show $c:_CHAIN.md | grep -o 'stop line[ *]*[0-9][0-9,]*'; done`
  → 150,929 until `7647aaf` (09-08) · both at `fe17820` · 180,000 only from `79a2604` (09-09)
- `grep -c '190,000' knowledge/_RUNBOOK-context-gauge.md` → **3**;
  `grep -c '180,000' knowledge/_RUNBOOK-context-gauge.md` → **0**; `sed -n '357,378p'` for the section
- `grep -c 'FILL' knowledge/_capture_gate.py` → **2**; `grep -n 'FILL' knowledge/_capture_gate.py`
  → `:2674` (comment) and `:2809` (`TESTIMONY_LABELS`)
- `sed -n '3206p;3248p' notes/_GAUGE-LOG.md` → #264's 214,299 and #266's 304,364 breach lines;
  `sed -n '92p' _CHAIN.md` → #267's 201,554
- `grep -n 'BOOT_CEILING_TK' knowledge/_gauge_tokens.py` → `:227` `= 70_000`;
  `sed -n '3966,4002p;4347,4368p' knowledge/_capture_gate.py` → the breach/discharge machinery
- `grep -ro 'NEXT WEEK\|2 WEEKS OUT\|next week' _CHAIN.md _LIVE-STATE.md GOOD-MORNING.md knowledge/_memento-index.json | cut -d: -f1 | sort | uniq -c`
  → `_CHAIN.md` 2 · `_LIVE-STATE.md` 2 · `GOOD-MORNING.md` 1 · index 4; `sed -n '72p' _CHAIN.md`
  → the three-dates sentence
- `git log --oneline --all -- apollo-spider/dist | head -4` → v1.0.13 `117b33c` · v1.0.12 `e68920d` ·
  v1.0.11 `cacaa19` · v1.0.10 `de8ed57`
- `for v in 10 11 13; do unzip -p apollo-spider/dist/Apollo-Spider-v1.0.$v.zip '*canon/canon.css' | shasum; done; shasum knowledge/canon/canon.css`
  → `b5e66eb…` · `f37a65d…` · `05098f9…` = repo
- `git log -1 --date=iso --pretty='%h %ad' ceef5b9` → `2026-09-10 21:26:49`;
  `ls -l <memory-store>/v1010-released-edges-ratified-kg-sphere-267.md` → mtime `Sep 10 21:21`
- `python3 -c "import json;d=json.load(open('notes/_dream/_MEMORY-GRADES.json'));print(d['refreshed_at'],d['hooks_seen'],d['counts'],d['population'])"`
  → `2026-09-13T07:11:34 52 {'FRESH':33,'AGING':10,'STALE':2,'UNPROVABLE':7}` + the POPULATION
  CHANGED line
- `grep -ro 'provenance unknown' . | grep -v '_tmp\|_to_delete\|/dist/' | cut -d: -f1 | sort | uniq -c`
  → 71 across 7 files; `sed -n '450,457p' knowledge/_RUNBOOK-capture-ritual.md` → the P3(b) clause
- `python3 -c "import json,collections;rows=json.load(open('knowledge/_rulings.json'))['rulings'];c=collections.Counter(r.get('status') for r in rows);print(len(c),sum(v for k,v in c.items() if k and 'metadata sweep' in k),c['ruled'])"`
  → `183 21 250`
- `PYTHONPATH=knowledge python3 -c "import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#268:**' in l][0])))"`
  → **412**, the banner's figure

**Baseline check before measuring:** `ls notes/_dream/2026-09-13*` → no such file, so this filename
is free and no `-vN` was needed. `git status --short` → one modified path,
`notes/_dream/_MEMORY-GRADES.json`, the conductor's B3 sidecar; `git log --oneline -1` → `b6b63db`,
level with `origin/master`.

**Nothing here self-promotes.** Four proposals, all `status: floated`; promotion is Dave's alone.
