# Dream pass — proposals, 2026-07-26

provenance: local_85ecbae4-fa2f-4313-b9ba-fcecf9f27f88 · 2026-07-26
status: floated

*Shape A (Cowork) first dream pass, per `notes/_MEMENTO-DECISIONS.md` A-D1/A-D2/A-D4 and the steering
spec `.claude/agents/dreamer.md`. Read COLD: repo spine + the last 15 session transcripts.*

**Nothing here self-promotes.** Every proposal is `status: floated`; promotion is Dave's alone, on
reading this file (derivation-governance). Proposals are ranked by prevalence, highest first.
Where evidence is thin it says so.

---

### P1 — `_LIVE-STATE.md` has no compaction rule and no archive sibling; it is now the single largest cold-start cost in the project

- EVIDENCE:
  - Repo, measured this pass: `_LIVE-STATE.md` = **205,561 bytes / 855 lines / 32 `PRIOR DELTA`
    sections**, oldest dated 2026-07-19. It **exceeds a single `Read` call** (29,872 tokens vs the
    25,000 cap) — I could not read it whole; I had to head-read plus grep.
  - `_LIVE-STATE.md:354` is a **single unbroken paragraph** chaining ~20 session summaries via
    `Previous: … Previous: … Previous:` back to 2026-07-18. One line, several thousand tokens.
  - The cost is named in the record, repeatedly: `_LIVE-STATE.md:26` — *"Heat is front-loaded from
    orientation reads (the ~25k-token `_LIVE-STATE` page + `GOOD-MORNING`)"*; `GOOD-MORNING.md:13` —
    *"heat front-loaded from orientation reads"*.
  - The comparison is the point: **GOOD-MORNING has a compaction rule** (ritual step 2c, keep ★LATEST
    + 1 PRIOR) **and an archive** (`_GM-ARCHIVE.md`, 34KB, in use). **MEMORY.md has a size cap**
    (~17.1KB, hook fires when tripped — session "Memento efficiency" and session "memory-index
    compaction" both acted on it). `_LIVE-STATE` has **neither** — no cap, no archive file, no ritual step.
  - Both compaction sessions explicitly stepped over it: session "memory-index compaction …" —
    *"`_LIVE-STATE` was deliberately left untouched — no design-system state changed this window"*;
    session "Memento efficiency: GM −35% …" — *"`_LIVE-STATE` I left untouched — nothing in the
    design-system state changed this session"*. Both reasons are sound per-session and jointly
    guarantee the file only ever grows.
  - Corroborating waste: the session titled *"Apollo — legend v5.3: Dave's next changes …"* paid the
    full cold-start orientation (GM + `_LIVE-STATE` + a cold `_build_all.py` re-verify) and then did
    **zero Apollo work** — the window went to LinkedIn profile copy. The orientation was bought and
    not used.
- PREVALENCE: 3 of 15 transcripts name the orientation read as the gauge cost; 2 of 15 explicitly
  decline to compact this file; verified directly against the repo (size, delta count, missing archive).
- PROPOSED: smallest reversible step — create **`_LIVE-STATE-ARCHIVE.md`** as the exact sibling of
  `_GM-ARCHIVE.md` (verbatim, newest-first, batched), roll every `PRIOR DELTA` older than the **last
  three** into it, and split the `:354` `Previous:` chain at the same boundary. Then add the roll as a
  numbered step in `_RUNBOOK-capture-ritual.md` beside the existing 2c so it self-maintains. No content
  is deleted — this is the move already proven twice on GOOD-MORNING.
- status: floated

---

### P2 — `_RUNBOOK-git-commit.md` was reconstructed from memory rather than read in 3 of the 5 commit-running sessions, and each time the lock step failed first

- EVIDENCE:
  - **Improvised (hit the failure, then recovered):**
    - *"Apollo — legend v5 + popover fix + 44px hit-area"* — Dave caught it, and the agent conceded
      verbatim: *"That's the rot — I reconstructed the commit from memory, mis-read the lock as
      Desktop when it's the sandbox delete-guard, and should've opened the runbook first."*
    - *"Apollo — legend FEEL ruled … v4"* — *"The sandbox's delete-guard won't let `rm` remove the
      stale `index.lock`. My notes say the sandbox can move what it can't delete — trying `mv`."*
    - *"Apollo — legend v5.1 bar-key RISE …"* — *"A stale `.git/index.lock` … is blocking the commit.
      `rm` won't work here, but a rename should."* Then a second lock (`HEAD.lock`) blocked the
      follow-up commit in the same session.
  - **Followed the runbook (no failure):** *"Apollo — legend v5.2 … v5.3"* — *"Runbook loaded — the
    mv-not-rm lock dance. Step 0 + 0.5: clear any inherited lock"*; and *"Memento — D1–D4′ RULED …"* —
    *"Runbook followed to the letter — clear · account · stage · clear · commit · clear."*
  - The runbook already anticipates all three failures. `knowledge/_RUNBOOK-git-commit.md:11` —
    *"Clear locks BEFORE staging as well as after — the sequence is clear · stage · clear · commit ·
    clear"*, with a dated self-correction at `:13` (*"Corrected 2026-07-18 after step 1 failed on a
    12-minute-old stale lock"*). Step 0 at `:15–19` is exactly the `mv`-aside loop each session
    re-derived under pressure.
  - The memory rule exists too (`feedback-read-the-runbook`: *procedural tasks → READ+FOLLOW the
    runbook, don't reconstruct from memory*). So this is not a missing rule — it is a rule that does
    not bite.
- PREVALENCE: 3 of 5 commit-running transcripts (of 15 read) improvised; 2 of 5 complied. Failure
  correlates with wrap-time heat — all three misses were Amber/Red wraps.
- PROPOSED: per `feedback-gate-dont-patch` (*recurring cross-file fix → GATE the condition*), do not
  add another prose reminder. Make step 0 **mechanical**: a tiny `knowledge/_git_commit.sh` that runs
  clear · stage · clear · commit · clear and refuses to stage while any `.git/*.lock` exists, with the
  runbook reduced to "run this script". A hot agent can call one script; it demonstrably cannot be
  relied on to recall a five-beat sequence.
- status: floated

---

### P3 — The render-verify shared-mount workaround exists only on the Polaroids; the runbook that owns it is untouched since 2026-07-23

- EVIDENCE:
  - Owed in writing, twice: `GOOD-MORNING.md:19` — *"Render beat sandbox instance-flapping by staging
    the browser on the shared mount (fold into `_RUNBOOK-render-verify.md`)"*; `_LIVE-STATE.md:36` —
    *"staging Playwright + browser + libs + fonts on the shared mount (`PLAYWRIGHT_BROWSERS_PATH`
    etc.). Fold into `_RUNBOOK-render-verify.md`."* GM's standing DO-FIRST block repeats it a third time.
  - Repo check: `knowledge/_RUNBOOK-render-verify.md` **mtime 2026-07-23 16:09**, and greps for
    `PLAYWRIGHT_BROWSERS_PATH`, `shared mount`, `instance-flap`, `flapping` return **zero matches**.
    The fold has not happened.
  - A second render fact is in the same position — `_LIVE-STATE.md:71` banks that the fontconfig alias
    must cover **both** font strings (`"Univers Next for HSBC"` *and* `"Univers Next HSBC"`), *"the
    second was missing and chart composite text falls back without it"* — also not in the runbook.
  - This directly contradicts the project's own doctrine, stated in `GOOD-MORNING.md` §A: **"Never let
    a durable rule live only on a Polaroid."** Both these facts are load-bearing for a pipeline that
    was blocked for days, and both live only on files that get rewritten every session.
- PREVALENCE: asserted-as-owed in 2 spine files + 1 transcript; unfulfilled across the 3 sessions since.
- PROPOSED: fold both recipes (shared-mount env staging; the two-string fontconfig alias) into
  `_RUNBOOK-render-verify.md` as a short "sandbox environment" section, then **delete the reminders**
  from `GOOD-MORNING` and `_LIVE-STATE` — the deletion is the tell that the fold really happened, and
  it pays into P1.
- status: floated

---

### P4 — Counts in prose have rotted; two are now wrong, and one of the wrong ones is load-bearing in the Memento strategy

- EVIDENCE:
  - **Orientation count, wrong.** `GOOD-MORNING.md:164`, in the standing §A block headed *"The one
    command that matters"*, reads *"★ 51 steps (45→51 …)"*. Measured this pass: `_build_all.py`'s
    `STEPS` list has **55 entries**. It was already wrong at 53 (the figure the 07-25 banners quote)
    before `_capture_gate.py` added two more on 07-26. This line sits in the section every cold start reads.
  - **Strategy claim, wrong and conflated.** *"53 blocking gates"* appears three times in the Memento
    corpus — `notes/2026-07-26-memento-dreaming-convergence-and-buildable.md:39` and `:156`, and
    `notes/2026-07-26-memento-dream-pass-scope.md:202`. Repo reality: **27** `_validate_*.py` gate
    scripts; **55** build steps, of which ~31 are gate-ish. So 53 is neither the gate count nor the
    current step count — it is a step count from a past week, relabelled as gates.
  - This matters more than a typo because the number carries an argument. The convergence note's
    strongest claim — *"That is a fitness function… a generic memory dreamer has no ground truth to
    score against"* — is quantified with it, and it was repeated verbatim in-session (*"You have 53
    blocking gates and a build that exits non-zero"*). The **claim survives**; the number should not
    be recalled.
  - Same shape as the `assertion-propagation-gap` hook: the gate fires on FLIP, so a line that is
    merely *out of date* is never chased.
- PREVALENCE: 2 distinct rotted counts across 4 files (1 spine file + 3 notes), echoed in 2 of 15
  transcripts.
- PROPOSED: two small moves. (a) In `GOOD-MORNING.md:164`, **drop the hardcoded step count** — the
  command prints `[i/N]` itself, so the prose should say "the blocking build" and stop asserting a
  number that cannot be gated. (b) Correct the three Memento occurrences to a sourced form
  ("27 blocking validators inside a 55-step build that exits non-zero, as of 2026-07-26") so the
  argument keeps its teeth without depending on recall.
- status: floated

---

### P5 — ds-010 is a live, confirmed canon rendering defect that has fallen out of the handoff entirely

- EVIDENCE:
  - Still present in canon, verified this pass: `knowledge/snippets/Chart-bar.reference.html:102` —
    `rect.dv-series{fill:var(--sc,var(--data-series-1));}`. Unchanged since diagnosis.
  - Still OPEN in the register: `knowledge/_DS-IMPROVEMENTS.md:231` — *"**OPEN** — surfaced to Dave
    2026-07-24"*. Effect per that entry: grouped, stacked, horizontal (DV-D09 teal) **and** the status
    chart (R-D9 ramp) all render series-1 purple; *"The `fill` attributes — and with them DV-D09 …
    and the R-D9 status salience ramp — are dead in render."*
  - Tracking has stopped. `grep -c ds-010 GOOD-MORNING.md` = **0** — it appears nowhere in the live
    handoff, not in DO-THIS-FIRST, not in §C. Its last mention in `_LIVE-STATE` is the **07-25 morning**
    delta (`:63`, *"STILL DAVE'S OPEN CALL — ds-010"*); the three later sessions' wraps do not carry it.
  - It was raised as a decision for Dave in 2 transcripts (07-24 discovery; 07-25 v4 session) and then
    goes silent — not closed, not ruled, just no longer mentioned.
  - Why it is worth chasing rather than leaving to the wave: it is a **one-line fix** (drop the
    declaration), the gates cannot see it (`dv-016` checks declared tokens, not the CSS-collapsed
    render), and the chart wave it was deferred into has itself been blocked behind legend sign-off
    since 07-24.
- PREVALENCE: 2 of 15 transcripts raise it, 0 of the 5 most recent carry it; confirmed live in the
  repo on 2 files.
- PROPOSED: re-surface one line in `GOOD-MORNING` §C (or DO-THIS-FIRST) restating the open call —
  *fold into the bar lane, or fix now as a one-liner + rebuild* — so it is decided rather than
  forgotten. This is a tracking fix, not a design change; the fix itself stays Dave's call.
- status: floated

---

### P6 — The context gauge's measuring half has been broken since ~07-21, and the recalibrated bands are now narrower than the instrument's own stated error

- EVIDENCE:
  - Every handoff stamps the caveat rather than a measurement: **11 occurrences** of
    `ESTIMATE ±15%` across the two spine files (`_LIVE-STATE.md` ×8, `GOOD-MORNING.md` ×3), each
    reading *"in-head tally, ESTIMATE ±15% — Half-2 broken"*. `Half-2` appears **13 times** across the
    corpus including two worker receipts.
  - The runbook records the breakage honestly — `knowledge/_RUNBOOK-context-gauge.md:77` — *"Until
    rebuilt, Half 1 (the in-head tally) governs; a Half-2 reading that disagrees with the tally by >2×
    is presumed wrong, not reassuring."* The engine `knowledge/_context_gauge.py` exists but is dated
    2026-07-21 and is not being used. **This one is correctly tattooed** — the record is not at fault;
    the rebuild is simply never scheduled.
  - The sharp edge: Dave recalibrated the bands on 2026-07-25 to **Green <45 · Amber 45–60 · Red ≥60**.
    The Amber band is **15 points wide**; the instrument's stated error is **±15%**. A reading of
    "Amber ~55%" is consistent with anything from Green to Red. Yet the bands now drive real
    behaviour — the runbook's Amber tier blocks starting a new build artefact, fires the spine flush,
    and triggers the wrap.
  - Observed cost of the imprecision in this window's set: two sessions wrapped at ~55–58% Amber with
    work left mid-flight, while one authored a full session at 🔴 ~70% and stamped
    *"NEXT READER RE-VERIFY"* — the next reader duly spent a cold `_build_all.py` run re-verifying
    claims that all held.
- PREVALENCE: stamped in 11 places across both spine files and in ~7 of 15 transcripts' wrap lines —
  the single most repeated caveat in the corpus.
- PROPOSED: one of two, Dave's call. (a) **Rebuild Half-2** — a real token count against the session
  transcript, so the band is measured not guessed; or (b) if the rebuild is not worth it, **widen or
  re-shape the bands** so they are coarser than the instrument's error (e.g. two states, "keep going"
  / "wrap now"), which is the honest expression of a ±15% instrument. Either way, stop paying the
  cost of a three-band precision the tally cannot deliver.
- status: floated

---

### P7 — GOOD-MORNING says the radius/corner tuner is "still owed" while two built versions sit in `reviews/`

- EVIDENCE:
  - `GOOD-MORNING.md:54` — *"**★★ Radius/corner tuner (§C·1d) — still owed:** 'return soon, don't let
    me forget.'"* Read cold, that says nothing exists.
  - Repo: **`reviews/RADIUS-CORNER-TUNER-2026-07-24-v1.html`** *and*
    **`reviews/RADIUS-CORNER-TUNER-2026-07-24-v2.html`** both exist.
  - `_LIVE-STATE.md:129` describes v1 in detail (*"dials `border-radius` control/surface/indicator per
    theme in 2px steps, preview updates live, reads canon.css … render-verified Mono(square)/
    Console(round)"*) and records what is **actually** outstanding: *"Tuner TWEAKS deferred (Dave:
    'we'll do the tuner after')."*
  - So the owed item is *tweaks + settling the numbers with Dave*, not *build a tuner*. The GM line
    understates progress in the direction that risks the most expensive error — a fresh cold session
    rebuilding from scratch something already render-verified. Note `_FUTURE-STATE.md:73` still frames
    it as the original ask too.
- PREVALENCE: 1 spine file states it wrongly, contradicted by 2 artefacts on disk + 1 `_LIVE-STATE`
  line; the ★★ item is carried in every handoff in the set.
- PROPOSED: amend `GOOD-MORNING.md:54` to name the state precisely — *"v1+v2 built and render-verified
  (`reviews/RADIUS-CORNER-TUNER-2026-07-24-v*.html`); **owed = the tweaks + ruling the numbers with
  Dave**"* — and mirror the same correction at `_FUTURE-STATE.md:73`. Cheap, and it protects a
  ★★ item Dave asked twice not to lose.
- status: floated

---

### P8 — `_to_delete/` is accreting and its "empty it host-side" note has never closed (thin)

- EVIDENCE: `_to_delete/` holds **24 entries** — a `.DS_Store` from 07-18, eight `_commit-msg*.txt`
  drafts spanning 07-19→07-21, `_assert_test/`, `_dense_test/`, `binned-review-docs/`, and
  `_stale_locks/` containing `index.lock`, `HEAD.lock`, `maintenance.lock` plus three dated
  `HEAD.lock.*` files from today. Flagged once, in the session *"Memento — three-shape dream-pass
  scope"*: *"The sandbox left stale `.git` lock debris moved into `_to_delete/` — worth emptying
  host-side sometime."* Never mentioned again.
- PREVALENCE: **thin** — 1 of 15 transcripts. Confirmed harmless: `_to_delete/` is gitignored
  (`.gitignore:25`), so nothing leaks into the repo. Listed for completeness, not urgency.
- PROPOSED: a one-line host-side `rm -rf _to_delete/*` when Dave is next at the machine (the sandbox
  cannot do it — that is the whole reason the directory exists). Optionally add the sweep as an
  optional last step of `_RUNBOOK-git-commit.md`. Low value; drop it if it costs a decision.
- status: floated

---

## Method

**Read (repo, this pass):** `.claude/agents/dreamer.md` (steering spec) · `GOOD-MORNING.md` (whole) ·
`_LIVE-STATE.md` (**head-read + grep only — see below**) · `notes/_MEMENTO-DECISIONS.md` ·
`knowledge/_DS-IMPROVEMENTS.md` (ds-010 entry) · `knowledge/_RUNBOOK-git-commit.md` ·
`knowledge/_RUNBOOK-context-gauge.md` · `knowledge/_RUNBOOK-render-verify.md` (grep) ·
`knowledge/_build_all.py` (STEPS parsed) · `knowledge/_capture_gate.py` (glob) ·
`knowledge/snippets/Chart-bar.reference.html` (line 102) · `_FUTURE-STATE.md` (grep) · `reviews/` listing.

**MEMORY.md — not readable by me.** The memory store lives **outside the repo**, so it is not on any
path my file tools can reach and it is invisible to `_build_all.py` (this is D1's finding, and the
reason the capture gate is repo-side only). Honest disclosure: the memory **index hooks** were
nonetheless present in my injected session context, so I could see hook titles and one-line summaries
and have cited them by name (`feedback-read-the-runbook`, `feedback-gate-dont-patch`,
`assertion-propagation-gap`, `gm-banner-compaction`). I could **not** open any individual memory file,
so no proposal here touches memory content, and none proposes a memory edit.

**Transcripts — all 15 read, none skipped.** In dispatch order: `local_e607b66f` (D1–D4′ + §4.1 built) ·
`local_57114829` (three-shape scope) · `local_00712f30` (Anthropic dreaming verified) · `local_09dcece9`
(LinkedIn outreach drafting) · `local_5fb45415` (talk-transcript cleanup) · `local_c0ed56c7` (legend
v5.3 → LinkedIn profile) · `local_17b416e1` (orchestration survey) · `local_09f53927` (v5.2/v5.3) ·
`local_5b43f513` (v5.1) · `local_6b9eb611` (memory-index compaction) · `local_28ddf8aa` (Memento
efficiency) · `local_fe7e4c97` (v5 + popover fix) · `local_268214b5` (legend FEEL → v4) ·
`local_0bd78738` (v3 + ds-010) · `local_7f87d96d` (O1 dark-in-light).

**Fidelity ceilings, and where they bit.**
1. *Turn-level only* (the known Shape A ceiling, not a defect): tool calls appear as bare names —
   `(called Edit)`, `(called mcp__workspace__bash)` — with **no arguments and no results**. So I can
   see *that* a session edited a file, never *what* it wrote. Every checkable claim in this file was
   therefore verified against repo state instead of taken from a transcript; where a proposal rests on
   a transcript quote, it is a quote of the agent's own prose, not of a tool payload.
2. *Recency bias:* `read_transcript` returns the **most recent** N messages, so I read session **ends**
   — wrap claims, handoff summaries, gauge stamps. That over-samples exactly the material most likely
   to be self-congratulatory, and under-samples mid-session work. Two mitigations: I only cited wrap
   claims that I could check in the repo, and the strongest finding (P2) comes from a session where
   the wrap **admits** the failure. Accepted, per dispatch.
3. *Read cap:* `_LIVE-STATE.md` could not be read whole — that limitation is itself P1's primary receipt.

**Hunted and found CLEAR — recorded so the next pass doesn't re-open them:**
- *GOOD-MORNING carries no Memento-lane entry.* Looked like drift; it is **ruled**. `_LIVE-STATE.md:14`
  registers the lane and states it runs *"deliberately OUTSIDE the GM queue"*; the lane is the first
  section of the file that is read second. Reachable by design. Not a finding.
- *GM's ★LATEST is 07-25 while two 07-26 sessions exist.* Same ruling — the 07-26 work is lane-only, and
  `_LIVE-STATE.md:354` explicitly stamps *"main Apollo queue UNTOUCHED this session."* Not staleness.
- *The gauge's "Half-2 broken" caveat.* Checked whether it lived only on Polaroids (the P3 shape).
  It does not — `_RUNBOOK-context-gauge.md:77` carries it properly. P6 is about the **unscheduled
  rebuild**, not a record defect.
- *`notes/_dream/` being ungated.* Confirmed deliberate and correctly scoped: `_capture_gate.py:74`
  globs `notes/*.md` and `_DECISION-HISTORY/*.md` only, so this subdirectory is genuinely outside it —
  exactly as A-D4 states, per the gate-glob-scope rule. This file carries its fields by discipline, not
  by enforcement, and says so.

**Shape of the findings.** Six of the eight are the *same failure*, which is worth naming: a rule or
fact that is **known, written, and correct** fails to bite — the git runbook (P2), the render recipe
owed to its runbook (P3), counts that no gate can check (P4), an open defect nobody re-states (P5), a
broken instrument nobody schedules (P6), a status line nobody refreshes (P7). None is a knowledge gap.
All are propagation gaps. That is consistent with `assertion-propagation-gap`, and it suggests the
highest-leverage response is mechanical (P2's script, P4's derived counts, P1's ritual step) rather
than another written rule.
