# Dream pass — 2026-08-02

provenance: local_cfa295ea-b60e-46f9-9918-13bcccab96c6 · 2026-08-02
status: floated

*Fourth pass. Covers the new ground since the 2026-07-28 pass (which reached #21): sessions
**#22 → #76**, five days. Nothing here is promoted; promotion is Dave's alone. Every proposal
carries at least one receipt, and where evidence is thin it says so.*

⚠ **This pass had `git` and read-only shell; the three prior passes did not.** The 2026-07-28 pass
recorded that having no git blunted two hunts and that "a pass with git can settle it in one
command." Two of the findings below (P2's trajectory, P5's two-edits-no-change) exist only because
the history was readable. All token figures are **tiktoken cl100k, measured on the artefact**, not
recalled — `tiktoken` had to be installed into the sandbox first (the every-session seam #73's (g)
self-heals at the commit seam only).

---

### P1 — The `boot` term of the pre-flight price has FOUR live accounts and no adjudication; two published totals dropped a measured ~52K term

- EVIDENCE:
  - **RULED and measured:** `notes/_MEMENTO-DECISIONS.md:2253` — *"#60-D3 — MEASURED: boot = 61,775,
    closed by reproduction. Three independent readings: 61,582 (#58b), 61,812 (#59), 61,775 (#60).
    Spread 240."*
  - **Still standing in the read-chain corpus:** `GOOD-MORNING.md:477` — *"`_gauge_tokens.py` boot
    model re-derive (prints 28,619 ± 8,000; **MEASURED constant is 61,775**)"*. So the shipped tool
    prints a third figure and the owed re-derive is already an open item.
  - **The form the runbook rules:** `knowledge/_RUNBOOK-context-gauge.md:34` —
    `pre-flight #NN: boot N (disk N measured · harness ~N est ±N, ds-025)`. The harness half is
    required to be **estimated and named**, not dropped.
  - **Practice through #67 (honest):** `notes/_GAUGE-LOG.md:668, 676, 683, 697` — #63/#64/#65/#67 all
    read *"boot 61,775 QUOTED (standing constant … Cowork window, own boot unmeasurable from inside
    — declared gap)"*. That is the quote-with-declared-gap form working.
  - **The switch, unrecorded:** `notes/_GAUGE-LOG.md:704` (#68) — *"boot 10,000 est (chain-only;
    harness unobservable (Cowork, ds-025))"*; `:712` (#69) — *"boot 10,000 est"*. Then #74 —
    *"boot unobservable (no opener stamp — harness half `ds-025`)"*; #72/#73/#75 — `⛔ NOT CAPTURED`.
  - **The arithmetic is load-bearing.** #68 published `10,000 + 118,000 + 40,000 = 168,000 of
    200,000 — AMBER at the line`. On the ruled constant the same three terms give **219,775** — over
    Dave's working line. #69 published the identical 168,000 and its post-mortem records the job
    overrunning to *"~190,000 est"*; on the ruled constant that is ~242,000.
  - **Probe for a retirement record, named so it is not an unmatched-grep-as-absence:** `grep` of
    every `boot`-bearing line in `notes/_MEMENTO-DECISIONS.md` for
    `retire|struck|supersede|no longer|re-scope|rescope|chain-only|chain only|10,000` — **0 hits.**
    No ruling, no correction-at-source, no `~~strikethrough~~` retires #60-D3.
  - ⚠ **Note what is NOT being claimed.** `"chain-only boot HELD"` (GAUGE-LOG `:707, :715, :726, :733`)
    is a true and useful *section-usage* observation — GM was never read whole. The defect is that a
    reading-behaviour observation was substituted into the *price* slot, where the harness half then
    silently costs zero.
- PREVALENCE: **8 of the last 9 sessions with strata (#68–#75) do not carry the ruled boot term**;
  2 of them (#68, #69) published a total computed on the substituted one. 39 `pre-flight #N` /
  `consult-receipts #N` strata read across `notes/_GAUGE-LOG.md` + `GOOD-MORNING.md`.
- PROPOSED: **not a fix — a one-line adjudication from Dave**, homed where the form lives
  (`knowledge/_RUNBOOK-context-gauge.md`, the pre-flight form block at `:34`). Three candidates, his
  pick: **(a)** the ruled 61,775, quoted with a declared gap (the #63–#67 practice); **(b)** disk-only,
  with the harness NAMED as unpriced on the same line so the total cannot read as complete; **(c)**
  `⛔ NOT CAPTURED — UNMEASURED` (already legal since #73's (h)). Whichever he takes, the same word
  goes on `GOOD-MORNING.md:477` and beside #60-D3's ledger row. **Strike nothing** — #60-D3 is his
  ruling and it is not an agent's move to retire it.
- status: floated

---

### P2 — The read chain has crossed its advisory BLOCK-CANDIDATE, and the gate that reports it cannot tell warn from block

- EVIDENCE:
  - **Measured at HEAD `18048db`, tiktoken cl100k: `_CHAIN.md` = 7,480 tape.** (It matches the file's
    own fixed-point footer exactly, so the stamp is sound — the number is not the defect.)
  - `knowledge/_capture_gate.py:647` — `CHAIN_BUDGET_TK = (4917, 6417)  # (warn, BLOCK-CANDIDATE)`.
    7,480 is **+2,563 over warn and +1,063 over the block-candidate.**
  - **The gate cannot say so.** `_capture_gate.py:1683–1698` has one comparison,
    `elif bill_of(chain_file) > bill_of(c_warn):`, and `c_block` appears **only** at `:1683`
    (unpacking), `:1695` and `:1696` (inside the f-string). `grep -n "c_block"` returns those three
    lines and nothing else. A chain at 4,918 and a chain at 7,480 produce the identical warn, with
    the block-candidate printed as decoration.
  - **The standing declaration has been outgrown.** `GOOD-MORNING.md:401–404` — *"⛔ DECLARED #55,
    AWAITING DAVE — **THE READ CHAIN SITS OVER ITS ADVISORY WARN** … the chain has been over the
    warn since before #55 opened"*, with *"Inherited at +495; #55 added +210 net"* (≈5,600). That
    declaration is correctly shaped — it names the band and refuses to quote a moving figure — but
    its **severity claim is now one threshold behind the artefact**, and no session has said so.
  - **The trajectory, measured across 57 commits touching `_CHAIN.md` since 2026-07-30:** the floor
    oscillates and wraps pull it down — `86b0cad` (#73 wrap) **5,148**, `ec46a4e` (#74 wrap) **5,248**.
    It crossed the block-candidate three times mid-session and returned under at each wrap
    (`e7df94d` 6,866 · `f70f602` 7,184 · `514f4bd` 7,256). **#75 skipped the 2c/2d/2f rolls, so
    7,480 is the first block-candidate breach ever left standing at a wrap-end state.** This is
    consistent with the memory hook that the floor is discipline-controllable, and it is the first
    datum showing what a skipped roll costs the *next* session's boot.
  - **A third-generation stale figure in the contract block.** `GOOD-MORNING.md:93` — *"⚠ **MEASURED
    #38: 4,585 tape — OVER M10's 4,500 warn.** This block quoted `3,410 tk` from #33 and had been
    stale five sessions."* The 4,585 is now itself 2,895 tape adrift, in the same sentence that
    records the previous instance of exactly this. `GOOD-MORNING.md:401` already demonstrates the
    correct shape one page later: *"Run `chain_file_tk('.')` for the figure — it MOVES, and writing
    it here would falsify it."*
- PREVALENCE: 3 of 3 standing sites carry the un-escalated statement (gate constant, GM:401
  declaration, GM:93 contract block); 57 commits measured.
- PROPOSED: two separable smallest steps, **neither of which arms anything** — arming, re-dialling
  and retiring the tier all remain Dave's word alone.
  1. `_capture_gate.py:1690` — add a branch comparing against `c_block`, still advisory, so the
     escalation is *nameable* at the wrap. An advisory that cannot distinguish its own two thresholds
     is an instrument without a reader.
  2. `GOOD-MORNING.md:93` — replace the `MEASURED #38: 4,585 tape` figure with the
     `chain_file_tk('.')` pointer that `:401` already uses. Same file, same session, proven shape.
- status: floated

---

### P3 — `_RUNBOOK-capture-ritual.md:89` is an instruction Dave SUPERSEDED at #28, still standing in the required-structure list — and #71 already reasoned from it

- EVIDENCE:
  - `knowledge/_RUNBOOK-capture-ritual.md:87–89`, step 2 (*"Write/refresh `GOOD-MORNING.md`" …
    "**Required structure, in order:**"*) — *"**The two names first** (see step 4b) — rename + next
    title, at the very top."*
  - `knowledge/_RUNBOOK-capture-ritual.md:418–423`, step 4b — *"**RENAME THIS SESSION → …** —
    **DELIVERED IN CHAT AT WRAP, never written into `GOOD-MORNING.md`.** ⚠️ **AMENDED — ruled Dave
    #28, 2026-07-28 (post-wrap addendum, step 5b), superseding the both-names-at-the-top instruction
    above.** … it was billing cold-start tokens to every future session to carry an instruction only
    the outgoing one could act on. **ENACTED here #30**."*
  - **The enactment was partial.** 4b was amended and the practice is correct — `grep -n "RENAME THIS
    SESSION" GOOD-MORNING.md` returns **nothing**, and `TITLE THE NEXT CHAT` is at `GOOD-MORNING.md:15`,
    exactly where #28 puts it. **Only the sentence at `:89` was left behind**, inside the numbered list
    a wrap reads top-to-bottom.
  - **It has already been acted on.** Transcript *"Apollo - #71: scatter responsive + the wrap that
    never ran"* (2026-08-01), after Dave asked *"can I get a title for thsi chat"*: *"Answered by the
    repo: the step is still there in full … `_RUNBOOK-capture-ritual.md` step **4b**, added
    2026-07-18 on your instruction, and **line 89 is explicit**: 'The two names first (see step 4b) —
    rename + next title, at the very top.' Not at the end. Not on request."* #71 quoted the
    superseded line as the live authority and did not see the amendment sixteen lines further on.
  - **The delivery itself is also lapsing, separately.** #70 and #71 both closed with neither name
    and Dave had to ask twice (*"can I have a title for this window"*, *"can I get a title for thsi
    chat"*); **#75's closing message carries no `RENAME THIS SESSION` line at all** (it gives only
    *"Next chat title's already set"*). #72/#73/#74 delivered it. Probe:
    `grep -rn "RENAME THIS SESSION|rename" knowledge/_capture_gate.py knowledge/_gen_chain.py knowledge/_gm_move.py`
    = **empty** — still ungated, as #71 diagnosed and explicitly assigned (*"It's the first small
    thing #72 should add"*). Four sessions later, nothing.
- PREVALENCE: 1 superseded line, 1 session already reasoning from it; rename delivery missing in
  **3 of the last 6 wraps** (#70, #71, #75), 2 of which Dave prompted. 15 transcripts read.
- PROPOSED: **one line, addition-then-cut, in that order.** Amend `_RUNBOOK-capture-ritual.md:89` to
  read *"The NEXT-SESSION title first — at the very top (see step 4b; the rename goes to CHAT only,
  ruled #28)"*. This is a record correction of an already-ruled amendment, not a new ruling —
  reference #28, do not re-decide it. **Do not** bundle a rename gate into the same motion: the
  rename has no artefact and #71's own note that it *"only ever lives in chat, which is exactly why
  it's the half that goes missing"* is the thing that needs Dave's judgment, separately.
- status: floated

---

### P4 — The consult-receipt honest negative is a stable 54% lapse across 39 sessions with no downward trend, and nothing consumes the rate

- EVIDENCE: 39 `consult-receipts #N` lines across `notes/_GAUGE-LOG.md` and `GOOD-MORNING.md`.
  **21 are `none`**: #30 #31 #33 #38 #40 #41 #42 #44 #46 #47 #50 #51 #54 #56 #58 #59 #60 #65 #68 #72
  #73. Several label themselves — *"a LAPSE, declared, not a ruled skip"* (#54, #56, #58, #68),
  *"the third in six sessions"* (#42), *"`_memento_search.py` was not called once this window"*
  (#44, #46), *"Third consecutive honest negative"* (#73). In the last ten with a line (#59–#74),
  six are `none`.
- ⚠ **This is NOT the trigger-index proposal.** That remedy is #72's, it is standing in GM §C·2, and
  it is on Dave's #76 list as item (f) — untouched here. The finding is about the *instrument*: the
  honest-negative form was built so a zero could be recorded truthfully, and it has succeeded at that
  for 39 sessions while the behaviour it measures has not moved. The rate is currently obtainable
  only by grepping 39 strata, which is why no session has ever quoted it.
- PREVALENCE: 21 of 39.
- PROPOSED: the cheapest possible consumer, and nothing else — extend the stratum's own format to
  carry the running count: `consult-receipts #N: none — Nth of M sessions`. Roughly 8 tape a wrap,
  written where the lapse is being recorded, so the rate is legible at the moment of writing instead
  of by archaeology. Whether that rate then justifies Dave's trigger index is *his* open item and is
  deliberately not pre-empted here.
- status: floated

---

### P5 — `_git_commit.sh --reconciled` promises a per-path reconcile the script cannot perform; flagged twice on one day, and two later edits to the file left it

- EVIDENCE:
  - `knowledge/_git_commit.sh:12` — *"`--reconciled`   you have run `git status --short` and can name
    WHY every dirty path exists (runbook step 0.5 — the script cannot do this judgment for you)"*.
  - `knowledge/_git_commit.sh:112` — `git add -A 2>/dev/null`. That is the only staging call.
  - Transcript *"Apollo - #70"* (2026-08-01): *"**`--reconciled` is an assertion, not a reconcile.** I
    told the script I'd accounted for every dirty path; I hadn't. That single unverified claim is what
    pulled another worker's uncorrected draft into my commit. … **`_git_commit.sh:68` is `git add -A`**
    — so the script *cannot* honour the per-path reconcile its own guard demands. The guard asks for
    something the mechanism can't do, which is why passing the flag felt sufficient. … **That's a
    ruling for you, not me.**"* (The line number has since moved to `:112`; the statement is unchanged.)
  - Transcript *"Research with receipts"* (same day, parallel worker): *"Working tree also has two
    unrelated modified files … **reconcile each path explicitly rather than `git add -A`**."*
  - Memory hook `worktree-reconcile-trail`: *"shared dirty tree → reconcile every path (**never blind
    `git add -A`**)"* — the memory forbids the only thing the mechanism does.
  - **git receipt:** `_git_commit.sh` has been edited twice since #70 — `8d176a1` (#73 (g), tiktoken
    self-heal) and `c27d7b1` (#74-D1, the wrap-gate WARN/`--wrap` split). Both landed *at the commit
    seam*; neither touched `:112`.
  - **Live today:** this pass ran against a tree carrying five uncommitted #76 files. The next
    `_git_commit.sh` run on that tree stages all of them regardless of what `--reconciled` asserted —
    the exact shape that bit at #70.
- PREVALENCE: 2 independent flags in one day + 1 memory hook, against 2 subsequent edits to the same
  file and 0 changes to the mechanism. 15 transcripts read.
- PROPOSED: **Dave's ruling, two options, do not do both.** Either (a) the script accepts paths
  (`git add -- "$@"`) so `--reconciled` means what it says, or (b) `--reconciled`'s implied promise is
  dropped and the flag is renamed to what it actually is (an acknowledgement, not a reconcile).
  Whichever he picks, the memory hook and `:12`'s wording move with it. This is a guard of his; an
  agent quietly changing what a safety flag means is the class this repo exists to stop.
- status: floated

---

### P6 — Three of a tracked worker receipt's four forks have no standing home

- EVIDENCE: `notes/_receipts/2026-08-01-worker-kg-cookbook-vs-decision-graph.md` (tracked, in git)
  closes with four forks. **One landed:** the six unruled edge types reached the #74/#75 GM banner and
  were closed at #75-D1 (`b1ca391`). **Three did not:** the two-fetch staleness control, the *"fog"*
  row in the charter, and the `MEMORY.md` index-drift gate — which the worker itself called *"the only
  one worth money today"*. The two-fetch control was named twice, independently: the *"Memento desk
  research"* session reached the same conclusion from its own failure (*"Three endpoints agreeing was
  one reading, not three … Two fetches, and it would have caught this at the start"*), and #70's
  closing message relayed all three to the conductor.
  **Probes, named:** `grep -rn` for `two-fetch`, `staleness control`, `fog`, `index-drift` across
  `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_FUTURE-STATE.md`, `notes/_MEMENTO-DECISIONS.md`,
  `knowledge/_FIXED-FLEX-CHARTER.md` — **0 hits each**. `MEMORY.md` matches exist but none is the
  drift gate (`GOOD-MORNING.md:371` is the #56 compaction; `_FUTURE-STATE.md:235` a trim idea; `:300`
  subagent memory).
- ⚠ **Declared limit:** this is *not* a lost artefact — the receipt is committed and reachable. It is
  three forks with no standing home, which is precisely the class #76's own step-2d EXIT CHECK caught
  hours ago for the inert proforma `data-pl/pr/h` attributes, and homed by addition to
  `_FUTURE-STATE.md`. Evidence for *whether they are worth doing* is thin — the worker's own
  assessment is the only ranking that exists.
- PREVALENCE: 3 of 4 forks homeless; named by 2 sessions; 5 standing surfaces probed, 0 hits.
- PROPOSED: one `_FUTURE-STATE.md` entry — the same motion #76 just performed, same format
  (`status: parked`, `[born #76 · guards · until]`), naming all three with the receipt path as source.
  Addition only; nothing is ruled, nothing is prioritised, and the entry is what lets a later pass
  cut them honestly.
- status: floated

---

### P7 — GM's `size:` stamp is 9–10% below the artefact and #75's residual, which named four other gaps, did not name it

- EVIDENCE: `GOOD-MORNING.md:9` — *"**size:** GM **24.9K tape** · §A **4.4K tape (EXEMPT)** · corpus
  **42.4K tape** · **measured #74, AT THE WRAP'S END (declare-LAST)**"*. Measured at HEAD `18048db`,
  tiktoken cl100k: **GM 27,269 · LS 18,948 · corpus 46,217** — the stamp is **+2,369 (+9.5%)** and
  **+3,817 (+9.0%)** adrift. Against `CORPUS_BUDGET_TK = 36000` the artefact is 10,217 over its warn
  while the stamp reports 6,400 over. #75's residual (`_CHAIN.md:53`) names the skipped 2c/2d/2f
  rolls, the missing 1b dossier, the 2f `HOLE #75` and the unmeasured gauge — and stops there.
  The same shape four sessions earlier, transcript *"Apollo - #71"*: *"GM's header size-stamp still
  ends at #69 — extending it needs a real tiktoken pass, so it flagged it rather than hand-estimating."*
- ⚠ **Honest scope:** the stamp is labelled *"measured #74"*, so this is a dated figure, not a false
  inscription, and it sits inside the read chain where every cold session meets it first. The
  proposal is about the *residual*, not the stamp.
- PREVALENCE: 2 of 15 transcripts (#71, #75); both left the figure in the chain.
- PROPOSED: one clause in the declare-LAST step of `knowledge/_RUNBOOK-capture-ritual.md` — when
  2c/2d/2f are skipped, the residual must also state that the `size:` stamp is therefore #N−1's and
  by roughly how much the artefact has since moved. One sentence, no gate, and it composes with
  #73's *declare LAST, re-read the declaration against the artefact* rather than adding a new rule.
- status: floated

---

## Licensed re-checks (the two the conductor declared, and only these two)

**(n) — M10's advisory tier. The prior receipt's contradiction is explained: it compared a live
figure against a RETIRED threshold.** The 28,000 in *"chain 30,306 tk, threshold 28,000 — trigger has
not fired"* is the **2026-07-27 M-set number against the GM+LS-whole referent**, which Dave's #33
read-chain cut retired. `_capture_gate.py:608–616` records this in terms: *"⚠ **THE PROMOTION TRIGGER
IS DISARMED, DELIBERATELY, AND THIS IS DAVE'S CALL TO RE-MAKE.** … Re-pointing satisfies that
instantly — 3,410 < 28,000 — but it is satisfied **by redefinition, not by achievement**."* The live
consumer is `CHAIN_BUDGET_TK = (4917, 6417)` against the whole `_CHAIN.md` file (`:647`, re-pointed a
second time at #48). So the prior pass's sentence was not self-contradictory so much as **unit-mixed**
— two numbers from two referents on one line. ⇒ **Not clear, and now superseded by P2**: measured
today, the live comparison is **7,480 vs (4,917 / 6,417)**, over both. The 28,000 trigger remains
correctly disarmed and is not re-floated here.

**(p) — lane order. SETTLED, and the hunt is currently vacuous.** `knowledge/_lanes.json` records
`lane-1-memento: landed` (*"LANDED 2026-07-28 #25"*) and `lane-2-apollo-charts: active` (*"born
blocked, UNBLOCKED #25"*). git receipt: `_lanes.json` has **four commits, all on 2026-07-28**
(`847d82b` → `59148f3` → `80a5a57` → `4283344`) and none since. So lane 2 was blocked only within
2026-07-28, between `847d82b` and `59148f3` — a window of hours inside a single day, and lane 1's own
landing commit is the one that unblocked it. **Since #25 no lane has been in state `blocked`, so no
work since #22 can have violated a block; the lane-order hunt has nothing to bite on and will stay
that way until a lane is blocked again.** `lane_routing_check` is BLOCKING and the GM §C·1 routing
line agrees with the records, so drift would have failed loud. ⇒ **Checked-clear, and now proven
rather than observed.**
⚠ One thing the settling turned up, declared and *deliberately not floated* — `_lanes.json`'s
`lane-dream-pass` sequence still carries *"M12 — first UNATTENDED Sun 08-02 07:10 fire"* as
`state: queued`, and that fire is what produced this file. It is inside the standing scope exclusion
(dream-lane mechanics), so it is named here for whoever wraps and nothing more.

---

## Method

**Sessions read (15, Shape A / Cowork, `list_sessions` → `read_transcript`).** #75 · #74 · #73 · #72 ·
#71 · #70 · #69 · #68 · #67 · #66 · #65 · *"Research with receipts"* (the #70 parallel worker) ·
*"Memento desk research"* · *"Mem-test – Good morning"*. Closing turns read in full for each; #66–#75
are the sessions carrying wrap claims, and those are the ones the hunts needed.

**Skipped, and why.** **#76** — it is **RUNNING** as this pass executes (76 assistant turns at the
time of reading; latest turn concerns the dv-legend split forking to Dave). Only the one-line progress
summary was taken; a full read of a live session would have paired a partial account with a settled
one, which is the pairing [[wrap-skipped-chain-certifies-wrong-session]] warns against. **#76 is
therefore the one session in this window whose claims are NOT tested here.** *"Mem-test – Good
morning"* was read and carries no material — it is a two-turn plugin smoke test. Sessions **#22–#64**
were not read: A-D2 sets the transcript window at ~15 and this pass honoured it. Those sessions are
covered only through their repo artefacts (`notes/_GAUGE-LOG.md` strata, `_GM-ARCHIVE.md`,
`notes/_MEMENTO-DECISIONS.md`), which is why P1 and P4 are built on strata rather than transcripts.

**Where the fidelity ceiling bit.** Turn-level only: tool calls appear as bare names — `(called
mcp__workspace__bash)`, `(called Edit)` — with no arguments and no results. Three consequences, named:
(1) **openers are not reachable** at a useful `limit`, since `read_transcript` returns the most recent
N messages, so every pre-flight figure in P1 comes from the committed stratum rather than from the
chat where it was declared; (2) **no transcript claim could be checked against what a session actually
ran** — every "landed / green / measured" claim in this file was re-verified against `git log`,
`git show` or a live measurement instead, which is the spec's own instruction and, this pass, was
cheap because git was available; (3) **prices spoken in chat and never stamped are invisible**, which
is exactly the population P1 is about, so P1's prevalence is a floor, not a ceiling.

**Ceilings that did NOT bite this pass.** The prior two passes recorded that the absence of git
blunted them. This pass had read-only shell and used it for: the 57-commit `_CHAIN.md` trajectory
(P2), the two-edits-no-change receipt on `_git_commit.sh` (P5), the four-commit `_lanes.json` history
that settled (p), and every token figure quoted. `tiktoken` is absent from a fresh sandbox and had to
be installed before any measurement — the same seam #73's (g) heals at the commit seam only.

**Governance.** One file written: this one. No edits anywhere else, no git write operation of any
kind. The working tree's five modified files (`GOOD-MORNING.md`, `_LIVE-STATE.md`, `_GM-ARCHIVE.md`,
`_LIVE-STATE-ARCHIVE.md`, `_FUTURE-STATE.md` — #76's in-flight 2c/2d rolls plus its EXIT-CHECK
copy-up) were read as evidence and left byte-for-byte untouched.

**On the missing `dreamer` agent-type pin** (the one in-scope exception). Repo side is intact:
`.claude/agents/dreamer.md` exists, is well-formed, and its frontmatter pins
`tools: Read, Grep, Glob, Write, ToolSearch`. The visible cause is not in the repo — this session's
working directory is the Cowork scratch dir
(`…/local_cfa295ea-…/outputs`) with `/Users/daviewen/Documents/Claude/Projects/UX-design` attached
only as an *additional* working directory, and project-scoped agent discovery keys off the primary
cwd. The conductor already knows; the tool restriction was held as discipline throughout.

---

## Checked-clear this pass — for the next pass, do not re-open

- **(q) `notes/_receipts/` resumed and is tracked.** Pass 2's item (i) noted receipts stopping at
  2026-07-24. They resumed: 07-28, 07-29 (×4), 07-31, and two on 08-01, all in `git ls-files`.
  The parallel-session rule held; the gap simply closed.
- **(r) The `_CHAIN.md` size stamp is exact.** Its footer claims 7,480 tape; measured 7,480. The
  fixed point built at `62b6e1e` still converges. P2 is about the *budget comparison*, not the stamp.
- **(s) `_lanes.json` agrees with GM §C·1 and with itself.** Schema invariant *"a lane whose blockers
  all landed MUST NOT stay blocked"* holds — lane-2 lists `blocked_by: [lane-1-memento]` and is
  `active` because lane 1 is `landed`. `lane_routing_check` is BLOCKING; no drift.
- **(t) The wrap gate's `--wrap` arm is a real consumer.** #75's own COMMIT STATE records it blocking
  that wrap on 3 fails and being right (*"a declared gap passes only where the gap is REAL"*), and
  #74's wrap commit proved the green path. [[instrument-without-a-consumer]] is discharged for this
  gate; do not re-float it.
- **(u) The `DV-D18`-names-two-rulings collision is FOUND, DECLARED and correctly homed** — #75's
  banner and `_LIVE-STATE.md` delta both carry it, and it is item (d) on Dave's #76 list. Leaving it
  unfixed is deliberate (renumbering his ruling is not an agent's move). Not a record defect to
  re-report; a ruling awaiting him.
- **(v) #76's dirty tree is a wrap in flight, not a lapse.** The five modified files are 2c/2d rolls
  plus a `_FUTURE-STATE.md` copy-up the step-2d EXIT CHECK required before the #72 delta could move.
  Named per the runbook. A future pass finding this committed should read it as the ritual working.
- **(w) `_capture_gate.py`'s `ABS_TERM_RE` / #58 crash class is homed in code** (`:763–801`) with the
  `','`-return failure recorded verbatim. #68's chat-only note about a `~` breaking the absolute-form
  match is covered by that block; no separate home is owed.
