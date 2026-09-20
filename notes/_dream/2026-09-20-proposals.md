# Dream pass 13 — floated proposals

> **provenance:** `383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367` · **2026-09-20**
> **status: floated** — nothing here self-promotes. Promotion is Dave's alone, on reading this file
> (derivation-governance, A-D3/D5). Every proposal below carries `status: floated`.
> **shape A (Cowork), SCHEDULED weekly fire `memento-dream-pass`.** ⚠ **DECLARED, NOT EXPLAINED: the
> fire landed at ~11:27 BST, not the ruled 07:10.** `date` at this seat returned
> `Sun Sep 20 11:30:50 BST 2026`. Pass 12 was 2026-09-13, so this pass is **ON TIME within the week**
> and late within the day. The cadence itself is barred from this pass's floating (see jj8) — this
> line records the fact and stops.
> **HEAD** `3e69b316` = `origin/master`, nothing unpushed. Tree DIRTY at baseline with #289's
> unwrapped session, LEFT AND FLAGGED by the conductor; I neither cleaned, staged nor reverted any
> of it (jj4).

**The spine of this pass.** Five of the seven findings below have one root: **the memory store moved
at #278 (2026-09-16) from the sandbox-mounted `.auto-memory/MEMORY.md` to claude.ai Project cloud
memory, and not one instrument that read the old store was re-pointed, re-measured or fenced.** The
move was deliberate and well-handled in the chat; what did not happen is the *instrument* half. P1
and P2 are the two live consequences. They are ranked by prevalence, highest first, as the spec
requires.

---

### P1 — The B3 memory grader has been dead since the #278 store move, and the boot surface has gone on printing STALE alerts from a 2026-09-13 sidecar graded over 52 hooks in a store that no longer exists — 42 rows of it, logged into the very dataset the B3 review is owed

- EVIDENCE:
  - `python3 knowledge/_gardener.py --refresh`, run at this seat, rc≠0, verbatim:
    *"⛔ GARDENER BLOCKED — nothing filed. P8/B3 — the memory index does not resolve, so NOTHING
    can be graded. expected : `/sessions/vigilant-gracious-rubin/mnt/.auto-memory/MEMORY.md`
    REFUSING TO GUESS another index."* The refusal is **correct and well-built** — that is not the
    defect.
  - The defect is the CONSUMER. `notes/_dream/_MEMORY-GRADES.json` still carries
    `"refreshed_at": "2026-09-13T07:11:34"`, `"hooks_seen": 52`,
    `"memory_index": "/sessions/busy-festive-davinci/mnt/.auto-memory/MEMORY.md"`.
  - `knowledge/_checkin.py:1259`–`:1301` has exactly **one** fence, and it is `if not _gdoc:`
    (*"⛔ NO SIDECAR … Grades are UNKNOWN, not clean"*) — **absent** is fenced, **stale** is not, and
    **"my provenance path does not resolve"** is not. A present-but-dead sidecar takes the green
    path: it prints `GRADES B3 sidecar, refreshed 2026-09-13 …` and then the alert lines, or else
    the line *"✅ no starred/blocked entry is STALE — an honest silence"*. That silence is no longer
    honest; it is a reading of a store the project stopped using four days ago.
  - What it prints today, reproduced read-only via `_gardener.render_grade_alerts` (I did **not** run
    `_checkin.py` — it appends to the counted dataset): **3 lines**, two `⛔ STALE` hooks
    (`retrieval-default-hides-the-ruling.md`, `tape-unit-is-not-real-tokens.md`) and one surface-control
    line `· 7 UNPROVABLE · 10 AGING (of 52 starred/blocked entries)`.
  - `notes/_dream/_GRADE-DECISIONS.jsonl`: **89** alert rows carry
    `"refreshed_at": "2026-09-13T07:11:34"`, first `2026-09-13T07:33:38`, last `2026-09-19T10:54:38`;
    **42 of them are at or after 2026-09-16**, the move. Every one of those 42 measures the token
    cost of a surface that is reporting on a dead store — and `s183-D1` counts them into the B3
    return-with-numbers. The machine half of that dataset is now being padded by an instrument that
    knows nothing.
- PREVALENCE: 42 of the 43 `_GRADE-DECISIONS.jsonl` rows written since 2026-09-16 (the 43rd is the
  conductor's one honest `--grade-decision` row today). Across sessions: every boot from #278 to #289.
  3 of 3 surfaces involved are wrong in the same direction — the sidecar's `refreshed_at`, its
  `memory_index`, and `_checkin.py`'s missing fence.
- PROPOSED: **the smallest reversible step is one fence, not a re-point.** In `knowledge/_checkin.py`
  (the `if not _gdoc:` branch, `:1263`), add a sibling arm: if `_gdoc["memory_index"]` does not
  resolve on disk **or** `refreshed_at` is older than the last scheduled dream-pass fire, print the
  UNKNOWN-not-clean line instead of the counts, and log the row with `"kind": "alert-void"` so the
  B3 dataset can tell a real measurement from a dead one. *(Re-pointing `_gardener.py` at the cloud
  store is a bigger question and is NOT proposed here — only the conductor's seat can read that
  store, so the grader may have no legal seat at all any more. That is ruling-shaped and Dave's.)*
- status: floated

---

### P2 — The boot decomposition the read chain publishes still attributes 8,470 real tokens to `MEMORY.md`, a file that no longer exists at any path; #278's conductor said on the record it would be re-measured, and across five boot readings since, nobody has — while boot went UP

- EVIDENCE:
  - `_CHAIN.md:42` — the ONE file a cold session is contracted to read — still says verbatim:
    *"`MEMORY.md` **8,470** of the first-turn figure is split and measured; **56,308** remains
    unattributed — that is what `ds-025` item 1 now means."*
  - `knowledge/_gauge_tokens.py:161` carries the same term in the floor table
    (*"MEMORY.md 8,470 MEASURED (#109, tokenised off the mounted auto-memory)"*), and `:443` — inside
    the string the gauge **prints at runtime as its own provenance** — still says the derived floor
    *"Covers system prompt + tool schemas + deferred-tool list + MCP instructions + **MEMORY.md** +
    CLAUDE.md"*.
  - The file is gone. At this seat: `ls ../.auto-memory` → *"No such file or directory"*;
    `ls MEMORY.md` → *"No such file or directory"*.
  - The re-measure was PROMISED, in the session that caused it. #278's transcript, the conductor's
    own words: *"Two consequences I will put in the #279 handoff: **the boot floor drops by the
    missing 8,470 (it is a measurement, so the constant is re-measured, not edited)**, and the
    runbook's 'auto-memory' wording at step 3 becomes 'Project instructions + cloud memory'."*
    Eleven sessions later neither has happened.
  - And the arithmetic went the other way, which is what makes this more than tidiness. Post-move
    first-turn readings, from `notes/_GAUGE-LOG.md` and the GM banners: **#284 80,882 · #285 80,863 ·
    #286 73,832 · #287 74,120 · #288 74,174** — five readings, all over `BOOT_CEILING_TK = 70_000`,
    the record calling them the 9th/10th/11th/12th/13th post-diet readings over it. The whole 7,031
    fall at #286 was attributed to **one** named variable (Dave blocking the Browser connector's 17
    tools) and the record says so carefully. **Nobody noticed that a second, larger term had already
    silently left the boot at #278 and the figure did not fall by it.** Either the 8,470 was never
    really in the first-turn cost, or something else absorbed it; the published decomposition cannot
    be right in both halves, and it is quoted at every cold start.
  - ⚠ `ds-025` item 1 *is* the decomposition question, so this is not a new subject — but `ds-025`
    asks about the **56,308 unattributed** remainder. The defect here is the **8,470 attributed**
    half, which the record treats as settled.
- PREVALENCE: live in 2 of 2 chain surfaces (`_CHAIN.md:42` and `GOOD-MORNING.md`'s § header, the
  same sentence) plus the gauge's runtime provenance string; unchanged across 11 sessions and 5 boot
  readings since the move.
- PROPOSED: **stamp it with an expiry and name the re-checker — do not edit the constant.** The
  literal is `s241-D1` SHRINK-ONLY and moving it is Dave's alone. The reversible step is in
  `knowledge/_gauge_tokens.py`: annotate the `MEMORY.md 8,470` line and the `:443` `fmethod` string
  by ADDITION with *"⛔ THE STORE MOVED AT #278 — this term is UNRE-MEASURED since; the figure is a
  pre-#278 measurement, not a current one"*, and mint the promised re-measure as a parked item with
  a due event (`knowledge/_parked.py`), so the promise has a consumer instead of living in one
  session's chat. #278's own second consequence — the runbook's *"auto-memory"* wording at
  `_RUNBOOK-capture-ritual.md` step 3 — rides the same fix.
- status: floated

---

### P3 — `GOOD-MORNING.md`'s `size:` stamp calls its own figure "exact" and has understated the generated figure at 6 of the last 7 wrap commits, by a gap that is growing — and at #288 the two series disagree in SIGN, so the wrap's published conclusion ("GM is −322 tape") is the opposite of what the file did

- EVIDENCE: both numbers are `cl100k_base` over the whole file, so they are the same unit and
  directly comparable. The stamp is hand-taken at the wrap; `_CHAIN.md`'s figure is GENERATED by
  `knowledge/_gen_chain.py` (`_UNIT_WORDS` at `:188`) from the file in the same commit. Per commit,
  `stamp` vs `chain`:

  | commit | session | stamp ("exact") | generated | gap |
  |---|---|---|---|---|
  | `e292b14b` | #282 wrap | 34,681 | 34,907 | −226 |
  | `160961f8` | #283 wrap | 34,869 | 35,109 | −240 |
  | `9a97e006` | #284 wrap | 34,845 | 34,845 | **0** ✅ |
  | `d2ae9c73` | #285 wrap | 35,028 | 35,211 | −183 |
  | `febbefe2` | #286 wrap | 35,503 | 35,966 | −463 |
  | `04dbeab1` | #287 wrap | 35,238 | 35,634 | −396 |
  | `71b3363c` | #288 wrap | 34,916 | 35,644 | **−728** |
  | `45d130c2` | #288 5b | 34,916 | 36,089 | −1,173 |

  And a live measure at this seat confirms the generated half is the true one:
  `tiktoken.get_encoding("cl100k_base")` over `GOOD-MORNING.md` at HEAD = **36,089**, to the token.
  - **The sign inversion.** #288's banner reasons from the stamp series: *"AND THIS TIME THE ROLLS
    DID NOT PAY FOR THEIR REPLACEMENT, ON EITHER FILE: against #287's stamp (35,238 …) GM is −322
    tape"*, and builds a cause on it (*"#288 DISCHARGED almost nothing and ACCRUED seventeen
    carries"*). Wrap commit to wrap commit, the file went **35,634 → 35,644, i.e. +10**; 5b to 5b,
    **35,846 → 36,089, i.e. +243**. The stamp says GM shrank; GM grew.
  - ⚠ **This is PARTLY declared and I am saying where the declaration stops.** The stamp's own text
    says 5b lands after it and *"the stamp is NOT re-taken"*, and 3.2% is inside its 10% grading
    tolerance. So the GAP is disclosed. What is **not** disclosed is (a) that the word **"exact"** is
    false of the file as committed — no measurement of `GOOD-MORNING.md` will ever return 34,916 —
    and (b) that the session-over-session DELTA computed from two stamps can and did come out with
    the wrong sign, which no tolerance covers.
  - The remedy already exists **in the same sentence**, for the neighbouring term: *"⛔ the chain's
    own size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer"*.
- PREVALENCE: 6 of 7 wrap commits since #282 understate; 1 of 7 is exact; the gap grows 226 → 728
  across the run. 1 of 1 published GM deltas this week has the wrong sign.
- PROPOSED: **generate it — the strong form of the `s129-D5` triage, and the #45 precedent applied to
  the GM term.** Delete the `GM **34.9K tape** (34,916 exact …)` figure from `GOOD-MORNING.md`'s
  `size:` line and replace it with the same pointer the chain figure already gets (*"its ONE home is
  `_CHAIN.md`'s generated header"*), so the wrap's delta is computed between two generated readings
  or not at all. If Dave would rather keep a stamp, the weak form is to drop the word **"exact"** and
  have `_gen_chain.py --check` fail when the stamp and the generated figure disagree by more than the
  5b tail. *(#50 is the precedent for the class: "the fattest line in the chain claimed its own size,
  and the claim had drifted 18%".)*
- status: floated

---

### P4 — `_state.py`'s row-id regex forbids a digit in a lane suffix, so every digit-named lane (W2, C2, R2 …) is refused registration under its own name and renamed to a form that no longer names it — five times in four consecutive sessions, and the document register now carries ids that do not match the lane directories on disk

- EVIDENCE:
  - `knowledge/_state.py:117` — `ID_RE = re.compile(r"^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$")`.
    The suffix class is `[a-z]{0,2}`: no digit may follow the session number.
  - The refusal, quoted verbatim in the #287 wrap report
    (`notes/_subreports/2026-09-19-287-W2-wrap.md:206`–`:209`):
    *"Writing this report's own row as `W-287w2` was **REFUSED by `_state.add`** — verbatim:
    'REFUSED: W-287w2: id does not match `^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$`' … The row
    is `W-287ww`. **#285 met it twice (`W-285lm2`, `W-285c2`) and #286 once (`W-286r2`)**"*, and
    `notes/_subreports/2026-09-19-288-W2-wrap.md:204`: *"This report's row is **`W-288ww`** — the
    `W-287w2` shape that `_state.add` refused at #287"*.
  - The #287 conductor surfaced it to Dave in chat as a live wart: *"Doc-row regex refused `W-287w2`
    → `W-287ww`, fourth instance."*
  - The consequence is in the store. `knowledge/_state.json` carries `"id": "W-287ww"` and
    `"id": "W-288ww"` — while the lanes on disk are `notes/_lanes/287/W2/` and
    `notes/_lanes/288/W2/`. The register that answers *"which lane filed which document"* names a
    lane that does not exist, and the true lane has no row under its own name. Digit-suffixed lanes
    are the NORM here, not an edge case: #288 alone ran `B`, `P`, `T`, `W2`; #289's untracked
    subreports are `G1`, `G2`, `G3`, `H1`, `H2`.
  - ⚠ This is **not** pass 10's P1 (`s218-D7` sub-report parse contract). That is about report
    *headings*; this is the registry's own id grammar refusing a legal lane name.
- PREVALENCE: 5 refusals across 4 consecutive sessions (#285 ×2, #286 ×1, #287 ×1, #288 ×1) —
  4 of the last 5 sessions that filed a wrap report.
- PROPOSED: widen the suffix class in `knowledge/_state.py:117` to `[a-z][a-z0-9]?` (or
  `[a-z0-9]{0,2}`), which admits `W-287w2` and `W-285lm2` while still refusing a bare-digit suffix
  that could collide with the session number, and add the two shapes to whatever selftest guards that
  regex. One-line, reversible, and it removes the rename step that is currently making the register
  lie. ⚠ The five existing renamed rows are RATIFIED RECORD; **repointing them is not proposed** —
  that is an edit to filed history and is Dave's, if he wants it at all.
- status: floated

---

### P5 — The memory index's own cut rule has been suspended for three consecutive wraps and the index now carries SIX wrap lines against a rule of three, because `MEMORY-ARCHIVE.md` has 162 bytes of headroom; it was raised at #285, #286, #287 and #288 and routed to "the dream pass" each time — so here it is, with the honest note that this seat cannot read the store

- EVIDENCE:
  - The index's own `description:`, quoted verbatim by the conductor's export
    (`_to_delete/_dream13-project-memory-index.md`): *"the index keeps the NEWEST THREE wrap lines
    only (cut at #285) and older ones move verbatim to MEMORY-ARCHIVE — ⛔ **SUSPENDED AT #286, #287
    and AGAIN AT #288, which carries SIX lines** … because MEMORY-ARCHIVE is at 48,990 of its
    49,152 B cap and the lines that should have moved would not fit and were not truncated"*.
  - Four consecutive sessions raised it to Dave and four consecutive sessions routed it away.
    #285: *"**The memory archive is full** (48,990 of 49,152 bytes), so the next index cut has
    nowhere to go. A second archive file, or a trim of the oldest lines — your call when it comes
    up, not today."* #286: *"One thing refused by arithmetic: the memory archive has 162 bytes of
    headroom … **That's a dream-pass question.**"* #287: *"the memory index now carries five wrap
    lines because the archive is full."* #288: *"archive cut still blocked at 162 B headroom, index
    carries six lines."* The index trailer says it in as many words: *"what to do about the archive
    is Dave's — **the dream pass is its seat**."*
  - The growth is monotone and mechanical: 3 (ruled) → 4 (#286) → 5 (#287) → 6 (#288) → 7 at the
    next wrap. Nothing has been truncated and nothing has been lost, which is the discipline working;
    what is drifting is that a RULED invariant of the boot surface is now false by four lines and the
    falsification is recorded only in the `description:` field that announces the invariant.
  - ⚠ **FIDELITY CEILING, STATED NOT SMOOTHED:** this seat cannot read claude.ai Project cloud
    memory. Every byte figure above is the conductor's export or a transcript quote — **second-hand,
    and I did not verify one of them.** The cross-session ROUTING (four sessions, four deferrals) is
    first-hand from the transcripts and is the part I stand behind.
- PREVALENCE: 4 of the last 4 sessions raised it; 3 of 3 wraps since #285 suspended the cut; the
  overflow is 6 lines against a ruled 3.
- PROPOSED: **the smallest reversible step is not a trim — it is a second archive file.** Deleting or
  truncating archived wrap lines destroys record; adding `MEMORY-ARCHIVE-2.md` (or whatever the store
  permits) and pointing the index's cut at it costs nothing and is undoable. What is genuinely Dave's
  and is NOT proposed here: whether wrap lines should be archived at all now that the repo carries
  `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md` for every one of them — the archive may be a copy of
  something the repo already holds, which would make this a deletion question rather than a capacity
  one. ⚠ Only the conductor's seat can write that store, so whichever way he rules, the enactment is
  not a lane's.
- status: floated

---

### P6 — P-276-1 cannot be answered in the terms it was parked in: the lane-ownership guard's tripwire could never have fired, because nothing has ever run the guard — and it is now one of TWO orphans the wiring gate fails on, up from zero at pass 10

- EVIDENCE:
  - P-276-1 (`python3 knowledge/_parked.py --due dream-pass`, due today) says the guard *"comes OFF
    at the next dream pass if its tripwire never fired"* and names the evidence as *"the guard file
    itself plus `notes/_REHEARSAL-LOG.jsonl` — any run that printed an offending staged path"*.
  - **There are no runs.** `python3 knowledge/_validate_wiring.py` at this seat:
    *"⛔ ORPHAN: `_validate_lane_ownership.py` exists on disk and NOTHING RUNS IT — no
    `_build_all.STEPS` entry, no `_git_commit.sh` invocation, no `gates.yml` step, not an arm of a
    wired script, and no named exemption."* Confirmed independently: `grep -c lane_ownership` returns
    **0** for each of `knowledge/_git_commit.sh`, `knowledge/_build_all.py`,
    `.github/workflows/gates.yml`, `knowledge/_checkin.py`, `knowledge/_seam.py`.
  - `grep -c 'lane_ownership' notes/_REHEARSAL-LOG.jsonl` → **0** across 2,994 lines. The guard does
    not write to that log at all, so the parked item's stated evidence source could never have
    carried the answer either way.
  - So the removal condition is satisfied **vacuously**, and that is a materially different fact from
    the one the ruling anticipated. `s276-D6` was written expecting an observation window; there was
    no window. The guard is a 78-line file with a working `--selftest` that has never been asked a
    real question.
  - **And the orphan count has moved.** Pass 10's (gg3) recorded *"50 gate script(s) on disk · 48
    wired · 2 exempt by name · **0 failure(s)**"*. Today: *"58 gate script(s) on disk (50
    `_validate_*` · 8 `_gate_*`) · 53 wired · 3 exempt by name · **2 failure(s)**"* — the second
    orphan is `_validate_demo_page.py`, born at `08e315dc` (#268, 2026-09-11, *"the pre-bake gate
    that drives the run-of-show's own page from the staged pack"*), which has been unwired for nine
    sessions. The gate that catches orphans is working; its output has had no consumer.
- PREVALENCE: 2 orphans of 58 gate scripts (0 of 50 at pass 10, nine sessions ago); 0 of 2,994
  rehearsal-log lines name the guard; 0 of 5 wiring surfaces invoke it.
- PROPOSED: two separable steps, both reversible, neither of which I have taken.
  **(a)** Report P-276-1 to Dave as **ANSWERED NEGATIVE BY CONSTRUCTION** rather than as "the
  tripwire did not fire", and let him rule the deletion on that corrected premise — it bears directly
  on his own words in the parked item (*"I don't think this is durable, feels like we're patching
  just to get it done"*), because an unwired patch is the strongest form of his objection.
  **(b)** Whatever he rules on the guard, `_validate_demo_page.py` needs the gate's own prescribed
  remedy — *"wire it or exempt it BY NAME with a reason and a date"* — and the wiring gate's 2
  failures should be carried with an age like any other red, so a third orphan is visible before it
  is nine sessions old. ⛔ **I did not delete the guard.** The spec is PROPOSE-only and the parked
  item says so too.
- status: floated

---

### P7 — P-269-4's near-duplicate list is due, and its headline finding is not only still true but has MOVED: the byte-identical `_GM-ARCHIVE.md` heading has slid from 4940/6133 to 5295/6488, the retrieval index mints a second record for it, and `_near_dupes.py` is wired to nothing and consumed by nobody

- EVIDENCE:
  - `python3 knowledge/_near_dupes.py` at this seat: *"NEAR-DUPES ADVISORY — 22 pair(s) at ≥ 0.5
    overlap across 1000 record(s)"*, top pair **`1.00`**:
    `gm-archive:4b-queued-button-states-finesse-pass-dave-2026-07-22-not-now` ·
    `…-not-now-2`, at `_GM-ARCHIVE.md:5295` · `_GM-ARCHIVE.md:6488`.
  - Byte-identical, verified: both lines are
    *"## 4b. ★ QUEUED: button-states finesse pass (Dave 2026-07-22, "not now — follow up") *(was
    §C·3b — the wave-1 briefs/receipts + prior deltas point here under that number)*"*, 171
    characters each, `a == b` → `EQUAL`.
  - P-269-4 recorded the pair at birth (#269, 2026-09-13) as *"`_GM-ARCHIVE.md:4940` = `:6133`"*.
    A week of rolls has moved both line numbers by ~355 and the duplicate is untouched — which is the
    point: the parked item's own pointer is already stale, exactly the class `s129-D5` names.
  - **It is not one heading, it is a block.** The `### ⬛ OFFLOADED #35 — §C·2b · §C·3 · §C·4b · §C·5,
    VERBATIM, on Dave's ruling` block at `:5294` re-inscribes four headings that the #16 roll had
    already archived at `:6391` (`2b. WAVE-1 RULINGS 1–7`), `:6414` (`3. ★ THE STANDING EYEBALL SET`),
    `:6488` (`4b`) and `:6499` (`5. Parked`). Both copies were legal when written; the archive now
    holds two snapshots of one section set.
  - **The retrieval surface carries the duplication.** `knowledge/_memento-index.json` holds 2,255
    records, of which the four above appear twice with the indexer's silent `-2` collision suffix.
    `_memento_search.py` is the contracted first move (*"retrieval FIRST"*, GM header), so a search
    for that queue item returns two records for one fact and nothing tells the reader which.
  - **And the instrument has no consumer.** `_near_dupes.py` is not a `_validate_*` or `_gate_*`
    script, so `_validate_wiring.py` does not even look for it; it appears in no build step, no
    commit-seam call and no CI job. It exists because a parked item asks the dream pass to run it by
    hand, once a week. [[instrument-without-a-consumer]].
- PREVALENCE: 1 exact pair of 1,000 records scanned (22 pairs ≥0.5); 4 duplicated headings in one
  offload block; 1 of 1 dream passes has ever run it.
- PROPOSED: pick one of the three `s129-D5` triage forms and stop carrying the pair as prose.
  The cheapest is **give it a named re-checker**: have the indexer DECLARE a collision instead of
  silently appending `-2` — one line in the id-minting path that emits
  `⚠ DUPLICATE HEADING: <id> at <a> and <b>` — so the duplicate is visible at build time and the
  pointer never needs re-typing. ⛔ **Deleting either copy is NOT proposed**: the #35 block says
  *"VERBATIM, on Dave's ruling"*, so removing it is an edit to ratified record. ⚠ **Thin on impact,
  and I am saying so:** this is an archive, the cost is a retrieval nuisance, not a wrong answer.
  It is here because P-269-4 is due today and this is its honest discharge.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(jj1) Pass 12's P2 (the FILL overshoot with no gate) is UNCHANGED and is referenced, never
  re-floated — but the new evidence is worth Dave's eye because a remedy was BORN since.**
  `s283-D1` gave the project `python3 knowledge/_seam.py` before and after every lane, ADVISORY, and
  #283's own transcript says it worked: *"The seam check stopped its own session at the stop line …
  first time in four sessions."* Five sessions on, FILL closes read **#284 217,359 · #285 197,852 ·
  #286 162,555 · #287 181,277 · #288 197,234** — past the 180,000 quality line in **4 of 5**, by
  17,234 at #288. An advisory check that fires and is then walked past is exactly pass 12's P2 with
  a mechanism attached. **Reported as corroboration for a floated proposal; not a new finding.**
- **(jj2) The six inherited gate fails in the `#243` form, now at the FOURTEENTH consecutive wrap,
  are DECLARED every time and correctly owned — do not report them as a discovery.** #281 called it
  the seventh, #283 the ninth, #287 the thirteenth, #288 the fourteenth; CI fails the same two
  `gates` steps (*"Survey the COMMITTED tree"* + *"Knowledge build"*) on every sha. The hand-typed
  ordinal that counts them is pass 10's (gg4) class and is not re-floated. ⚠ The **new** red — #288's
  `release` job failing at step 12 (`build-designer-pack.sh --selftest`, stale chart receipts needing
  a render seat) — was read back in chat the same evening, named as *"#289's first mechanical job,
  before any lane"*, and is the discipline working at full speed.
- **(jj3) Pass 8's (ee2) ruled the sidecar's `memory_index` field "a per-session mount path, NOT a
  finding", and I am NOT overturning that — P1 is a different fact and here is the line.** (ee2) was
  right that the path varies per session forever. P1 does not say the path CHANGED; it says the path
  no longer resolves **at any mount**, because the file it points at was retired from the project at
  #278. A varying pointer is provenance; a pointer to a retired file is a dead premise. If Dave reads
  P1 as re-opening (ee2), the honest answer is to keep the `_checkin.py` fence and drop the
  `memory_index` half of it.
- **(jj4) The dirty tree is #289's unwrapped session, declared by the dispatch, and I neither cleaned,
  staged nor reverted any of it.** One correction to the dispatch's own ground truth, recorded so it
  is not read later as drift: the dispatch named **4** modified paths; there are **5**. The fifth is
  `notes/_dream/_GRADE-DECISIONS.jsonl`, dirtied by the conductor's own `--grade-decision` row at
  `2026-09-20T11:29:34` — i.e. by the dispatch's own preparation, minutes before I was launched.
  Those instrumentation appends remain **pass 6's P2, still floated**, referenced not re-floated.
  ⛔ I did not touch `.git/index.lock`; every `git` call from this sandbox printed
  *"unable to unlink … Operation not permitted"*, the known wart [[git-lock-mv-not-rm]], and I left
  it alone.
- **(jj5) A second dispatch ground-truth correction, and it matters because it would have hidden the
  finding.** The dispatch states that `_near_dupes.py`'s *"top pairs are 2026-08-20 fan-out briefs at
  0.66"*. The tool's actual first line of output is a **1.00** pair, and the 0.66 brief pairs are
  eighth and ninth. Had I taken the dispatch's summary rather than running the tool, P7 would not
  exist. Recorded as the reason the spec says to verify claims against the repo.
- **(jj6) The newest handoff at root is `_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-named.md`**
  (`ls -t _HANDOFF-*.md | head -1`), matching the index, not the `_HANDOFF-87-bankruptcy` shape the
  dispatch floated as a guess. HEAD `3e69b316` = `origin/master`; rulings stand at **622**
  (`json.load(knowledge/_rulings.json)["rulings"]`), `s288-*` does not exist, and #288's banner claim
  *"`_rulings.json` STAYS 622"* is TRUE. Spot-checked and true, so not findings:
  `knowledge/canon/gen_bento_role_vars.py` is **289 lines**; `notes/_STRAND-MAP-2026-09-19.html` has
  **13** `<section`; `_CHAIN.md` says `YOU ARE #289`.
- **(jj7) What this pass wrote, stated plainly. ONE file — this one.** I ran
  `python3 knowledge/_gardener.py --refresh` because § B3 mandates it; **it BLOCKED and filed
  nothing**, which is P1's central receipt, and `git status --porcelain` confirms
  `notes/_dream/_MEMORY-GRADES.json` is **not** modified — so (ee6)'s old tension between "only write
  the proposals file" and "run the refresh arm" resolved itself this time by the arm refusing. I
  logged **no** `--grade-decision` rows, ran **no** `_checkin.py` (it appends to the counted dataset —
  the alert lines in P1 were rendered read-only via `_gardener.render_grade_alerts`), ran **no**
  `_build_all.py`, and performed **no git operation of any kind** — every `git` call in § Method is
  read-only (`log`, `status`, `show`). No memory file (this seat cannot write the Project store), no
  canon, no ledger, no `notes/` file but this one.
- **(jj8) Out of scope by standing exclusion, and where I drew the line.** Dream-lane mechanics remain
  barred (cc6/dd7/ee7/ff7/gg9/hh8/ii8): I did **not** float the cadence, the conductor sequence, the
  lane's §🔀 row, or `_dream/` gating — **including the 11:27 fire time**, which the header records as
  a fact and nothing more. ⚠ **P1 sits nearest the line and the judgment is flagged rather than
  assumed:** its subject is `knowledge/_gardener.py` and `knowledge/_checkin.py`'s BOOT surface —
  an instrument and a fence that exist on every session opener, not only on dream mornings. The dream
  lane is the thing that *fires* the refresh arm; it is not the arm, and it is not the boot print.
  ⚠ **P5 sits second-nearest:** the index's trailer names the dream pass as the archive's seat, so
  reporting on it is answering a question routed here, not proposing anything about the lane itself.

---

## Method

**Inputs, in the spec's order.** (1) The memory index — **not read directly: this seat cannot reach
claude.ai Project cloud memory.** I used the conductor's verbatim export,
`_to_delete/_dream13-project-memory-index.md` (gitignored, 19 lines), and every claim I take from it
is marked second-hand in the proposal that uses it (P5 is the only one that leans on it). (2)
`GOOD-MORNING.md` header + ★ LATEST/★ PRIOR banners (first 60 lines), `_CHAIN.md` head and `:42`.
(3) Fifteen sessions from `list_sessions`, read via `read_transcript`.
(4) Every checkable transcript claim spot-checked against the repo before citing.

**Sessions read (15, newest first):** #289 `b0af391c` · #288 `00c8b0c5` · #287 `09972043` · #286
`5b51ad79` · #285 `c0e3326a` · #284 `b7971c45` · #283 `09fe83d9` · #282 `7bcb5189` · #281 `046f6737` ·
#280 `07ecdda5` · #279 `51523b86` · #278 `edbf71a9` · #277 `3674aa74` · #276 `7b06d46e` · #275
`51c72040`. **Depth was graded, not uniform:** the last-10-message tail for #289/#288/#287, the
last 6 for #286/#285, 3–4 for #284…#281, and the last 2 for #280…#275. **Nothing was skipped for
convenience**; #280's and #276's transcripts are two messages long in their entirety, and for the
older five I cross-read the repo's own copy of the session (`_HANDOFF-*`, `notes/_lanes/27*/`,
`knowledge/_parked.json`) rather than resting on the tail. ⚠ **A tail is not a session:** for
#284…#275 I can vouch only for what the closing turns say, and I have not treated silence in those
tails as evidence of anything.
**One thing the older tails did settle, and it strengthens P6:** #275's close reports the collision
that caused the lane-ownership guard in the first place — *"two of your sessions were open on this
repo at once. The #274 chat committed into #275's lane folder and replaced a file the lane was
using"* — so the guard was built for a real, observed event and then wired to nothing.

**Where the fidelity ceiling bound, stated rather than smoothed.** Shape A gives turn-level text
only — tool calls appear as bare names (`(called mcp__workspace__bash)`, `(called Agent)`) with no
arguments and no results. So **not one number in this file comes from a transcript**: every figure is
either a command I ran at this seat or a line I read in the repo. The transcripts contributed
exactly three things, all of them *speech*: #278's promise to re-measure the boot floor (P2), #287's
chat mention of the doc-row refusal (P4), and the four-session routing of the archive question (P5).
Where a transcript asserted a number I wanted — #288's FILL, #286's boot — I quote the repo's copy
(`notes/_GAUGE-LOG.md`, the GM banner) and say so.

**Commands run, all read-only, all reproducible.** From `/…/UX-design`:

```
date ; git log --oneline -1 ; git status --short ; ls -t _HANDOFF-*.md | head -1
python3 knowledge/_parked.py --due dream-pass
python3 knowledge/_gardener.py --refresh            # BLOCKED, filed nothing — P1's receipt
python3 knowledge/_validate_wiring.py               # 2 ORPHANs — P6
python3 knowledge/_near_dupes.py                    # 22 pairs, top 1.00 — P7
grep -c 'lane_ownership' notes/_REHEARSAL-LOG.jsonl                       # 0
grep -n 'W-\[0-9\]{1,3}' knowledge/*.py                                     # _state.py:117 — P4
grep -o '"id": "W-28[5-9][a-z]*"' knowledge/_state.json | sort | uniq -c
python3 -c "import tiktoken;print(len(tiktoken.get_encoding('cl100k_base').encode(open('GOOD-MORNING.md').read())))"   # 36089 — P3
for c in $(git log --format=%h -12 -- GOOD-MORNING.md); do \
  git show $c:GOOD-MORNING.md | grep -o '([0-9,]* exact' | head -1 ; \
  git show $c:_CHAIN.md | grep -o 'It is [0-9,]* tape' | head -1 ; done                # P3's table
python3 -c "import json;[...]"   # _GRADE-DECISIONS.jsonl row counts — P1
python3 -c "import sys;sys.path.insert(0,'knowledge');import _gardener as g;\
            print(g.render_grade_alerts(json.load(open('notes/_dream/_MEMORY-GRADES.json'))))"   # read-only alert render
ls ../.auto-memory ; ls MEMORY.md                                          # both absent — P2
```

**What I deliberately did not hunt.** The `s218-D7` sub-report contract parses (pass 10's P1 class,
cleared at hh1), the `⛔ NOT CAPTURED` pre-flight streak (pass 9's P1), the `#119` metadata-sweep
status strings (pass 6's P1), the `provenance unknown` footprint (pass 11's P3, corroborated at ii2)
and the three dirty instrumentation logs (pass 6's P2) — all still floated, all referenced where new
evidence bore on them, none re-floated. The 622 RULED ids, the twelve prior passes' `### P<n>`
headings and the ledger's `##` spine were read from `_to_delete/_dream13-do-not-refloat.md` **before**
hunting, as the dispatch required.

**Parked items due at this pass, discharged or not.** Of the nine, **P-276-1** is answered in P6 and
**P-269-4** in P7. The other seven — P-274-1, P-272-1, P-272-2, P-272-4, P-273-1, P-277-1, P-277-4 —
are **not** dream-pass questions at all: every one names Dave as the owner of the decision and a lane
as the owner of the work. I read all nine, confirmed none has silently rotted (each still points at a
file that exists and a question that is still open), and **I am deliberately not converting any of
them into a proposal** — a parked item waiting on Dave is the parking system working, not a dropped
loop. P-277-1's diagnosis in particular (the `dv-019` row carrying `dv-017`'s sentence, propagated to
`_rule_nodes.json` and `_consult-index.json`) is fully written up in the parked entry and needs a
lane, not a dreamer.
