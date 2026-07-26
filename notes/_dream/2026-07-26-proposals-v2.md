# Dream pass — proposals, 2026-07-26 (v2, second pass)

provenance: local_bc312468-9e33-4bc1-8977-284ce74b70af · 2026-07-26
status: floated

*Shape A (Cowork) second dream pass of the day, per `notes/_MEMENTO-DECISIONS.md` A-D2/A-D4 and the
steering spec `.claude/agents/dreamer.md`. Versioned `-v2` per spec rule 2 — the morning's
`2026-07-26-proposals.md` exists and has already been RULED, so nothing here overwrites it.*

**Nothing here self-promotes.** Every proposal is `status: floated`; promotion is Dave's alone
(derivation-governance). Ranked by prevalence, highest first. Where evidence is thin it says so.

**Deliberately NOT re-floated:** P1–P8 and S-D1–S-D3 (ruled + enacted today, ledger rows in
`notes/_MEMENTO-DECISIONS.md`), their enactments, the four items the morning pass recorded as
"hunted and found CLEAR", and the dream-lane's own freshly-ruled mechanics. This pass hunts the
**main Apollo queue and the generated-artifact layer**, which the morning pass reached only in
passing.

---

### P1 — The compaction rolls have made six numbered "DEFERRED TO DAVE" chart decisions unreachable from either live spine file, and left the banner's own cross-reference pointing at nothing

- EVIDENCE:
  - The 2026-07-24 chart-wave banner, now in `_GM-ARCHIVE.md:32`, reads: *"**⚠ DEFERRED TO DAVE
    (numbered, all recorded — see `_LIVE-STATE` top):** (1) DATAVIZ SIGN-OFF … (2) Q2 combo home
    (new snippet vs Chart-bar variant) · (3) sweep hook / 16KB cap fork · (4) COMBO-LINE-INVERT
    R-B/R-C · (5) Chart-scatter Layer-2 · (6) brush/range-select spec · (7) JS-off seg wart"*.
  - Grepped every one against both live spine files today. Counts (`GOOD-MORNING.md` /
    `_LIVE-STATE.md`): "Q2 combo" **0 / 0** · "combo home" **0 / 0** · "COMBO-LINE-INVERT" **0 / 0** ·
    "scatter Layer-2" **0 / 0** · "range-select" **0 / 0** · "seg wart" **0 / 0** · "16KB" **0 / 1**.
    All seven are present in `_GM-ARCHIVE.md` and/or `_LIVE-STATE-ARCHIVE.md`. Item (1), the DATAVIZ
    SIGN-OFF, **is** carried live — because it happens to sit in the standing §C·2 block
    (`GOOD-MORNING.md:327`). It is the one of the seven that had a standing home.
  - A repo-wide grep for the distinctive strings ("JS-off seg wart", "brush/range-select",
    "COMBO-LINE-INVERT") finds them only in: the two archives, `notes/_briefs/2026-07-24-*`,
    `notes/_receipts/2026-07-24-*`, `_DECISION-HISTORY/2026-07-24-*`, and ADR-0014. Every one of
    those is a *dated* artefact — none is a live queue a cold session reads.
  - The pointer itself is now false: the banner says *"see `_LIVE-STATE` top"*, and `_LIVE-STATE.md`
    today holds exactly **3** delta sections (LATEST + 2 PRIOR, all 2026-07-25/26), none of which
    mentions the seven. `GOOD-MORNING.md` holds exactly **2** banners.
  - This is the same failure ds-010 exhibited — the case the morning pass caught as P5 and Dave ruled
    accept-enact-now. P5 fixed the **instance** (one line restored to GM DO-FIRST). The **mechanism**
    is unchanged, and it has six more victims already on the floor.
  - Not an argument against compaction: GM 2c and the new `_LIVE-STATE` 2d are both correct and both
    preserve content verbatim. What neither has is an **exit check** — a rolled banner can carry a
    ⚠/⬛ Dave-owed item out of live state, and nothing notices.
- PREVALENCE: 6 of the 7 numbered deferrals, verified absent from both live spine files (2 files ×
  7 strings checked); 1 prior instance already ruled (ds-010/P5); 0 of the 6 appear in any live
  standing register.
- PROPOSED: smallest reversible step — add the six to the standing **`GOOD-MORNING.md` §C·2** block
  where the DATAVIZ SIGN-OFF already lives (they are the same kind of object, from the same banner,
  and §C·2 is why (1) survived). Then make the compaction steps carry an exit check: in
  `_RUNBOOK-capture-ritual.md` steps 2c/2d, before a banner or delta rolls to its archive, any
  ⚠/⬛/"AWAITING"/"OPEN CALL" line inside it must already appear in a standing section — else copy it
  up first. This is gate-shaped, not prose-shaped: `_validate_standing_instructions.py` already does
  reachability for STAND-002, so the check has a home if Dave wants it to bite.
- status: floated

---

### P2 — Four generated reports are non-deterministic by construction; the "stable-sort wobble" everyone works around is seven unsorted `set()` iterations, and I reproduced it three times in six runs

- EVIDENCE:
  - Named as known noise in four places, twice with a manual workaround attached:
    `GOOD-MORNING.md:12` — *"The verify-build's stable-sort noise (`_ADVISORY-SIGNALS`,
    `_LIVE-STATE-CHECK`) restored in place (sandbox delete-guard blocks `git checkout` → used
    `git show HEAD:… >`)"*; `_LIVE-STATE.md:27` (same event, same dance); `GOOD-MORNING.md:384`
    carries it as a §C·4 enact-queue item — *"advisory-signals emitter stable sort (ordering
    wobble…)"*; `GOOD-MORNING.md:421` — *"`_ADVISORY-SIGNALS.md` ordering wobble left uncommitted"*.
  - **Reproduced this pass.** Ran `_validate_advisory.py` six times with `PYTHONHASHSEED=random`:
    two distinct outputs, 3 runs each (md5 `6f9c115d…` ×3, `f2cca70b…` ×3). The whole diff is one
    line moving one position:
    `- **unmasked-digits** — sort-code shape "40-12-26" …` swapping with its neighbour in
    Form-layout. *(The file was restored to HEAD immediately — `git diff HEAD` is clean; I wrote
    nothing outside this proposals file.)*
  - **Root cause located, exactly.** `knowledge/_validate_advisory.py:141`, `:157`, `:159` iterate
    `for m in set(...)`. Every *other* check in the same function uses `sorted(set(...))` —
    `:163`, `:167`, `:176`, `:196` — so this is an omission, not a design choice.
  - **Same class, three more scripts, including the second file named in the complaint:**
    `knowledge/_build_live_state.py:298` and `:353` (`for base in set(dead_files)`,
    `for adr in set(ADR_RE.findall(...))`) — that script is the emitter of `_LIVE-STATE-CHECK.md`;
    `knowledge/_validate_snippets.py:213`; `knowledge/_build_trace_dossier.py:378`. Seven sites,
    four files.
  - Cost is not cosmetic. It makes a *deterministic* build print a false diff, which means the
    reconcile step (`_RUNBOOK-git-commit.md` step 0.5 — "account for every dirty path") is trained
    every session to wave through two known-noisy paths. That is exactly the habit the reconcile rule
    exists to prevent, and it has already produced one recorded "left uncommitted" outcome (`:421`).
- PREVALENCE: named in 4 spine lines across 2 files; reproduced live 3 of 6 runs; 7 code sites in 4
  scripts, all in generated-report emitters.
- PROPOSED: wrap the seven iterations in `sorted(...)` — a one-word edit each, no behaviour change,
  no report content change (only ordering becomes fixed). Then close the §C·4 line at
  `GOOD-MORNING.md:384` and drop the "known wobble" caveats at `:12`/`:421` and `_LIVE-STATE.md:27`;
  the deletions are the tell that it really landed. Optional hardening if Dave wants it gated: a
  build step that runs one emitter twice under `PYTHONHASHSEED=random` and fails on a diff — the
  same bite-test shape used elsewhere.
- status: floated

---

### P3 — Twenty advisory accessibility signals have not moved in eleven commits; three of them were wired with an explicit promotion condition that has now sat unmet for 23 days

- EVIDENCE:
  - **The number is frozen.** `_ADVISORY-SIGNALS.md` has read **"20 signal(s)"** in every one of the
    last 11 commits that touched it — 2026-07-22 (`16c8b84`) through 2026-07-25 (`9a16365`); the
    commit before that read 18. Not one signal has been cleared in the window, through the whole
    Phase-2 wave, the chart wave and the legend work.
  - **Three carry a written promotion condition, all still unmet.** `knowledge/_validate_advisory.py`
    documents each at wiring (Dave ruling 2026-07-03, advisory-first per ADR-0005 §5):
    - G role-suffix (avd-006) — *"4 live canon signals at ruling time (Cards 'Example link'); fix at
      the Cards revisit, then promote."* Still 2 signals today (Cards + canon-gallery).
    - H skip-link (acd-003, **SC 2.4.1 — Level A**) — *"ALL 5 screens signal at wiring time — real
      gap."* Still **5 of 5** today. `knowledge/guidelines/accessibility-client-side-dev.md:27`
      records the same ruling: *"all 5 composed screens signal at wiring — real gap, fix at the
      composition touch"*.
    - N inputmode/autocomplete (acd-025, SC 1.3.5) — *"FIRES on canon email inputs at wiring time —
      evidence banked for the Input-fields supercharge."* Still 8 signals (4 in Input-fields, 4
      mirrored in the gallery).
  - **The conditions are honest, and that is the trap.** `git log -- knowledge/_fitness-test/` shows
    the composed screens have not been touched since the Apollo rename — so H's *"fix at the
    composition touch"* has genuinely never triggered. A condition whose trigger never fires is
    indistinguishable, from the record's point of view, from a closed item.
  - **Nothing tracks any of it.** Greps for "advisory" across `GOOD-MORNING.md`, `_LIVE-STATE.md`,
    `_FUTURE-STATE.md` return only the *stable-sort noise* mentions (P2's subject) — not one line
    about the signals themselves. `knowledge/_DS-IMPROVEMENTS.md`, the designated home for known DS
    debt, has no entry for any of the three.
  - Weight, in this project's own terms: the foundational aspiration is *most digitally accessible
    bank, WCAG 2.2 AA as the floor* (ADR-0004). H is a **Level A** criterion failing on every
    composed screen the engine has ever produced, sitting in a generated report that no live document
    points at.
- PREVALENCE: 20 signals unchanged across 11 commits / 4 days; 3 promotion conditions unmet for 23
  days; 0 mentions in 3 spine files and 0 entries in the DS-debt register.
- PROPOSED: do not fix the signals here — that is design work and Dave's call. Do the **tracking**
  fix, which is the cheap half: open one `ds-0NN` entry in `knowledge/_DS-IMPROVEMENTS.md` naming the
  three conditional promotions, their trigger events (Cards revisit · composition touch ·
  Input-fields supercharge) and their current counts, so the debt is registered where debt lives
  rather than only inside a generated report. If Dave wants the trigger to actually fire, the
  smallest version is a line in the Input-fields / Cards entries of the build-out queue saying "clears
  advisory G/N when it lands".
- status: floated

---

### P4 — `_REVIEW-SIGNOFF.md` is the durable sign-off tracker and has not been fed since 2026-07-21, while at least four review artefacts have queued up behind Dave

- EVIDENCE:
  - The file is explicitly the running list: `knowledge/_REVIEW-SIGNOFF.md:8` — *"⬛ PENDING — FULL
    CONSOLIDATED REVIEW (Apollo Mono baseline)… Running list of what it must cover"*, and it does
    the job well for older items (it carries the DataViz sign-off, Tranche-9, the Video-player
    fast-follower with probe values). Memory hook `full-review-pending` names it as the backlog.
  - mtime **2026-07-21 21:59** — five days and roughly a dozen commits ago.
  - What has queued since, none of it in the file (grep for "legend", "tuner", "v5", "donut",
    "combo", "sparkline" → **0 hits**):
    1. Legend v5 / v5.1 / v5.2 / v5.3 — four review candidates in `reviews/` (v5.3 written
       2026-07-25 20:14), all "not canon till Dave signs off".
    2. Radius/corner tuner v1 + v2 (`reviews/RADIUS-CORNER-TUNER-2026-07-24-v*.html`) — the ★★ item,
       whose GM status line was corrected by P7 this evening.
    3. The data-marks-exempt rule + a11y gate rebuild — `notes/_briefs/2026-07-25-hit-area-rule-and-gate-proposal.md`,
       marked "⬛ PENDING SIGN-OFF" in both spine files.
    4. The five chart panes in `showroom/` (chart-bar/line/donut/combo/sparkline, regenerated
       2026-07-25 18:11) — memory hook `dataviz-pillar-progress` says sign-off = Dave eyeballs the
       five panes.
  - So the queue lives in banner prose (which compacts — see P1) while the register built to hold it
    goes stale. The two failures compound: the register is the natural landing place for exactly the
    items P1 shows being evicted.
- PREVALENCE: 1 register untouched 5 days vs 4 distinct pending sign-off strands, each verified as a
  file on disk; 0 of the 4 named in the register.
- PROPOSED: append the four to the "Running list of what it must cover" block in
  `knowledge/_REVIEW-SIGNOFF.md`, each as one line with its artefact path — no restructuring, no new
  file. Then make the capture ritual's step 1 mention it: when a session leaves a review artefact
  awaiting Dave, the artefact path goes in the register, not only in the banner. Pairs with P1's exit
  check; either alone helps, both together close the loop.
- status: floated

---

### P5 — An owed revision has been blocked for three consecutive sessions on a source document that only ever existed as a chat upload (thin, but cheap to close forever)

- EVIDENCE:
  - Carried unchanged in three consecutive lane status lines: `_LIVE-STATE.md:16` — *"Owed:
    convergence-note `-v2` (still blocked on re-attach of
    `2026-07-26-convergence-anthropic-dreaming.md`)"*; `:17` — *"Owed unchanged: convergence `-v2`
    (blocked on re-attach)"*; `:18` — same phrase again.
  - The reason is stated plainly in `notes/2026-07-26-memento-dream-pass-scope.md:211` — *"NOT done.
    The source note wasn't re-attached and revising it from the [summary] …"* — and at `:23`.
  - Repo check: `find . -iname "*convergence*"` returns exactly one file,
    `notes/2026-07-26-memento-dreaming-convergence-and-buildable.md` (the *review* of the note).
    The note under review is **not in the repo at all**; it exists only as an upload, and
    `notes/2026-07-26-memento-dreaming-convergence-and-buildable.md:16` records it as
    *"(uploaded)"*.
  - **The counter-example is in the same window**, which is what makes this cheap: the Lamin Mukta
    talk transcript *was* saved into the repo (`lamish-context-engineering-transcript.md`, tracked,
    committed in `dfdc857`) and consequently nothing that depends on it is blocked. Same session
    family, same kind of source, opposite outcome, opposite consequence.
  - Why it matters beyond one note: the project's doctrine is retrieval-not-recall and
    receipts-in-the-repo. A cited source that lives only in a chat window is, by that doctrine, an
    un-retrievable citation — and here it has already cost three sessions the same deferral.
- PREVALENCE: **thin on impact, firm on evidence** — 1 blocked deliverable, but the blocker is
  restated verbatim in 3 consecutive session statuses + 2 note lines, and the repo confirms the file's
  absence. Listed because the fix is one sentence, not because it is urgent.
- PROPOSED: two lines, both small. (a) Dave re-attaches the note once, and the session **saves it into
  `notes/`** before working on it — after which `-v2` is unblocked forever. (b) Add one clause to
  `_RUNBOOK-capture-ritual.md` step 1: *any uploaded document the record will cite gets written into
  the repo in the same session* — the `lamish-…` transcript is the worked precedent to point at.
- status: floated

---

## Method

**Pass shape.** Shape A (Cowork), second pass of 2026-07-26, dispatched with the morning pass already
ruled. Because that pass had mined the transcript set thoroughly and its findings were enacted hours
earlier, this pass deliberately inverted the weighting: **repo-first forensics** (generated reports,
validators, registers, archives, git history) with transcripts used to date and corroborate, rather
than transcript-first. Every proposal above rests on a repo receipt I produced this pass; none rests
on a transcript claim alone.

**Read / measured (repo, this pass):** `.claude/agents/dreamer.md` · `notes/_MEMENTO-DECISIONS.md` ·
`notes/_dream/2026-07-26-proposals.md` (incl. its checked-clear list) · `GOOD-MORNING.md` (section
map + targeted reads) · `_LIVE-STATE.md` (heads + greps) · `_GM-ARCHIVE.md` · `_LIVE-STATE-ARCHIVE.md`
· `_FUTURE-STATE.md` (greps) · `knowledge/_REVIEW-SIGNOFF.md` · `knowledge/_ADVISORY-SIGNALS.md`
(+ 12 commits of its history) · `knowledge/_validate_advisory.py` · `knowledge/_build_live_state.py` ·
`knowledge/_validate_snippets.py` · `knowledge/_build_trace_dossier.py` ·
`knowledge/_A11Y-GATE.md` · `knowledge/_INTEGRITY-REPORT.md` · `knowledge/_DS-IMPROVEMENTS.md` ·
`knowledge/guidelines/accessibility-client-side-dev.md` · `knowledge/guidelines/_INGESTION-QUEUE.md` ·
`knowledge/_RUNBOOK-git-commit.md` · `knowledge/_RUNBOOK-capture-ritual.md` (step map) ·
`knowledge/_git_commit.sh` · `notes/_receipts/` listing · `reviews/` + `showroom/` listings · git log,
`origin/master` state, `.git` lock behaviour.

**Two live experiments, both cleaned up.**
1. *Determinism* (P2): six runs of `_validate_advisory.py` under `PYTHONHASHSEED=random`, outputs
   compared by md5 → two variants. `knowledge/_ADVISORY-SIGNALS.md` restored from HEAD immediately
   (`git show HEAD:… >`, the documented dance); `git diff HEAD` verified clean afterwards. **This
   proposals file is the only file this pass leaves changed.**
2. *Lock behaviour* (recorded clear, below): moved `.git/index.lock` aside, ran read-only
   `git status` and `git log` — the lock reappears every time.

**Transcripts.** The window is the last 15 by `list_sessions`; it has slid by two since the morning
pass (adding the two lane sessions `local_3ff44b84` and `local_85ecbae4`, dropping `local_0bd78738`
and `local_7f87d96d`). I read **4 directly this pass** — `local_3ff44b84` (ruling session),
`local_17b416e1` (orchestration survey), `local_c0ed56c7` (v5.3 → LinkedIn), `local_09f53927`
(v5.2/v5.3) — and relied on the morning pass's full 15/15 read for the rest, treating its
transcript-derived claims as leads to verify rather than evidence to reuse. That is a deliberate
budget choice given how recently the same set was mined; it is also this file's main honesty caveat:
**the transcript layer is under-sampled by this pass, so a transcript-only finding could have been
missed.** The known Shape A ceiling (turn-level only; tool calls as bare names, no arguments or
results) applies unchanged, and the recency bias the morning pass documented applies to my four reads
too.

**Scope exclusions, per dispatch.** Nothing here proposes on the dream lane's own mechanics
(`dreamer.md`, `_capture_gate.py`, the weekly task, `notes/_dream/` gating) — those were ruled and
enacted hours ago and are not drift. Nothing re-floats P1–P8 or S-D1–S-D3.

**Hunted and found CLEAR — recorded so the next pass doesn't re-open them:**
- *Stale `.git` locks look like a recurring mystery.* They are not: the sandbox delete-guard blocks
  `unlink`, so **any** git command — including read-only `git status` — leaves a fresh `index.lock`.
  Verified live (moved the lock aside; `git status` recreated it immediately). The record already says
  this correctly at `knowledge/_RUNBOOK-git-commit.md:3–6`, and `_git_commit.sh` (P2 of the morning
  pass) now clears them mechanically. Nothing owed.
- *"Push owed / unpushed stack" appears in several live lines.* Checked: `origin/master` = `9dd3920`
  = HEAD, `git rev-list --count origin/master..HEAD` = **0**. Everything is pushed. The remaining
  mentions sit inside dated banners describing the state at *that* session's start, which is what a
  dated record is for (`feedback-header-wins-over-audit`). Not a correction.
- *`GOOD-MORNING.md:12` and `_LIVE-STATE.md:27` still say "53/53 GREEN" while the build now has 55
  steps.* Both are inside dated 2026-07-25 banners and were true when written; the morning pass's P4
  already de-hardcoded the standing §A count. Historical, not stale.
- *`_INTEGRITY-REPORT.md` shows 4 warnings.* Read them: four unresolvable token paths
  (`icon/arrow`, `padding/arrow`, `text/ticks`, `overlay/background-blur`) in Hero / Line chart /
  Modals metas. Report is PASS with 0 errors and the warnings are labelled best-effort by design.
  Left alone deliberately — flagging them would be inventing a finding out of a gate working
  correctly.
- *`notes/_receipts/` stops at 2026-07-24.* Looked like ritual drift; it is not. Receipts are a
  **parallel-session** artefact (`feedback-parallel-conductor`), and every session since has been solo.
  Correct by rule.
- *The decision-audit backlog (`_RUNBOOK-decision-audit.md`, memory `decision-audit-method`).* Checked
  whether the "designed, not run" claim had rotted. It has not — the runbook is unchanged since
  2026-07-05 and the audit genuinely has not been run. Known and honestly recorded; a real backlog,
  but not a record defect, and re-stating it would be noise rather than a finding.

**Shape of the findings.** The morning pass concluded that its eight were nearly all *propagation
gaps* — known, written, correct facts that fail to bite. These five are one layer down and mostly a
different failure: **the generated and registered layer is not read**. Two of the five (P1, P4) are
items falling out of the live spine because the registers built to hold them are not fed; two (P2, P3)
are machine-generated reports that no live document points at, so their contents — a reproducible
non-determinism and twenty unmoved accessibility signals — have simply never been looked at; P5 is a
citation that left the repo entirely. If the morning pass's lesson was *make the rule mechanical*,
this pass's is the complement: **a generated artifact that nothing points at is not evidence, it is
storage.**
