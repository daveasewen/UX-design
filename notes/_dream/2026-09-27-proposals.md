# Dream pass 14: floated proposals

> **provenance:** `383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367` · **2026-09-27**
> **status: floated.** Nothing here self-promotes. Promotion is Dave's alone, on reading this file
> (derivation-governance, A-D3/D5). Every proposal below carries `status: floated`.
> **Shape A (Cowork), scheduled weekly fire `memento-dream-pass`.** `date` at this seat returned
> `Sun Sep 27 07:14:09 BST 2026`. Pass 13 was 2026-09-20, so this pass is **on time**.
> **HEAD** `3100da99` = `origin/master` (per the dispatch; `git log -1` agrees). The tree was dirty
> at baseline and I left it alone. The dispatch put the dirt down to #304. That is only partly true,
> and kk9 corrects it.

**The spine of this pass.** Pass 13's spine was *"the environment moved and the instruments were not
re-pointed"* (the #278 store move). That lesson was learned for the store and then repeated twice
this week, on two new moves:

- **the hook file changed its shape at #296**, which blinded two parsers (P2);
- **the conductor moved to a cloud seat around #296–#298**, which blinded the pre-flight emitter
  (P5).

The top finding is different in kind. It is a **ruling that was made and then not enacted, while the
thing it was made to stop happened three more times on the most-read file in the project** (P1).
Ranked by prevalence, highest first, as the spec requires.

---

### P1 — `s294-D11` ruled the midnight-wrap stamp so that "the sixth occurrence stops writing a sixth paragraph". It was never enacted: the sixth, seventh and eighth paragraphs were written after it, and the eight lines are now 23.7% of `_CHAIN.md`

- EVIDENCE:
  - **What the ruling was for, quoted from the surface Dave ruled on.** In `notes/_lanes/294/R/review-page.html`,
    item 11 says: *"Ruling it does not change any behaviour — **it stops the sixth occurrence writing a
    sixth paragraph** to re-explain the same thing. My recommendation: Both — … carry the commit date
    on **one header line**, and **let a ruling replace the five explanatory paragraphs with a
    pointer**."* Dave answered *"ill go with all the recommendations"*, and that became `s294-D11`.
  - **It was ruled, not enacted.** `json.load(knowledge/_rulings.json)` gives `s294-D11` a `status` of
    `ruled`. The other ten `s294-D*` records it sits beside carry `ENACTED #294 … commit f81bbdd4`.
  - **The paragraphs did not stop.** `grep -c "WRAP DATE SPLIT" GOOD-MORNING.md` returns **8**, and
    `GOOD-MORNING.md:9`–`:16` are eight `> ⚠ **WRAP DATE SPLIT…` lines. The review page counted
    **5** at `:9`–`:13`. The three added after the ruling, found with `git log -S`:
    - SIXTH at `d9b7320f` (#295 wrap, 2026-09-22);
    - SEVENTH at `c0ad1a85` (2026-09-23);
    - EIGHTH at `efe3bb47` (#303 wrap, 2026-09-26).

    Each of the three cites `s294-D11`'s "shape" in its own text. So each wrap read the ruling as
    permission to add one more line, when the ruling says **one** header line in total.
  - **It is on the cold path.** `_CHAIN.md` is generated from the GM header, and
    `grep -c "WRAP DATE SPLIT" _CHAIN.md` returns **8** (`_CHAIN.md:34`–`:41`). Measured at this seat
    with `cl100k_base`, the eight lines come to **1,845 tape of `_CHAIN.md`'s 7,797**, which is 23.7% of
    the one file a cold session is contracted to read. Boot has sat over `BOOT_CEILING_TK` 72,768 at
    every cloud-seat reading (#297–#301, per #303's gate-open fail line), and Dave's own words at #300
    were *"the boot is huge"*.
  - **Precedent for the class:** `#79-D2` (`notes/_MEMENTO-DECISIONS.md:2803`–`:2808`), *"one of Dave's
    rulings in two places that can drift apart"*. Here the drift is from one line to eight.
- PREVALENCE: 3 of 3 date-split wraps since the ruling added a paragraph, and 0 of 3 used the single
  line the ruling names. There are 8 lines in each of 2 generated/contract files. 1 of 11 `s294-D*`
  rulings is un-enacted, and it is the one on the cold path.
- PROPOSED: **enact `s294-D11` as the page described it. This is enactment, not a new judgement.**
  1. In `GOOD-MORNING.md`'s header, keep **one** rolling `WRAP DATE SPLIT` line, the newest (#303's),
     which each future date-split wrap *replaces* rather than adds to.
  2. Move the seven older lines **verbatim** to `_GM-ARCHIVE.md` under a batch heading, with a one-line
     pointer in their place.
  3. Give it a **named re-checker**: one assert in `_gen_chain.py --check` (or `_capture_gate.py`
     wrap mode) that fails if the header carries more than one `WRAP DATE SPLIT` line.
  4. Stamp `s294-D11` enacted with the sha, under `s295-D2`.

  This is reversible: the archive batch holds every byte. ⚠ The move is a GM header edit, so it
  belongs to the conductor's seat at a wrap, not to a lane.
- status: floated

---

### P2 — The wrap-hook file changed shape at #296, and two instruments that parse it went blind. The B3 grader now silently de-stars all 8 of the newest hooks, and the `s271-D4` open-items re-check reads 4 of the 60 open items those 8 hooks state. The second blindness is declared at every wrap; the first is declared nowhere

- EVIDENCE:
  - **The shape change.** Through #295 each hook carried a `## THE INDEX LINE (for index.md …)`
    section (`notes/_lanes/294/WRAP-MEMORY-HOOK.md:29`, `…/295/…:26`). From #296 on, that section is
    `## FOR THE CONDUCTOR` / `## FOR THE PLACER`, with the index line inside a numbered step
    (`notes/_lanes/303/WRAP-MEMORY-HOOK.md:12`–`:20`: *"**1. Put this line at the TOP of `index.md`**"*).
  - **Blindness 1: the grader drops the stars, and says nothing about it.**
    - `knowledge/_gardener.py:910` matches the section with
      `^##+[^\n]*(?:index|MEMORY\.md)[^\n]{0,24}line\b`, which was measured *"23/23"* on 2026-09-21
      (`:906`–`:909`), the day before the change. No `FOR THE PLACER` heading matches it, so
      `_mirror_headline` falls back to the H1 `# #296 — WRAP MEMORY HOOK`.
    - `:884`–`:885` then derives `marks` and `starred` from that H1. `notes/_dream/_MEMORY-GRADES.json`
      (refreshed 2026-09-27T07:13:35) shows `marks ''` and `starred False` for **every one of
      296…303**.
    - Their real index lines all open `- [★★` (`grep -o '^- \[★*'` over the eight files returns ★★ for
      each).
    - `alert_rule.marks = ['⛔','★★']` and `s179-D1` alerts **only** on starred or blocked entries. So
      the eight newest hooks can never raise a STALE alert. They are FRESH today, which is why nothing
      shows.
    - The sidecar's `unlinked_index_lines` declares the H1 fallback for all nine files (283, 296–303).
      It does **not** say that the fallback strips alert eligibility. `grep -rl "H1-FALLBACK\|headline
      taken from the H1"` over the #29x/#30x records finds no mention.
  - **Blindness 2: the open-items re-check reads almost nothing.** I called
    `_capture_gate.hook_open_items_recheck('.', notes/_lanes/<n>/WRAP-MEMORY-HOOK.md)` read-only at
    this seat, and compared it with the numbered items under each hook's `### OPEN, DAVE'S` heading:

    | hook | 294 | 295 | 296 | 297 | 298 | 299 | 300 | 301 | 302 | 303 |
    |---|---|---|---|---|---|---|---|---|---|---|
    | items stated | 10 | 13 | 9 | 7 | 6 | 8 | 7 | 8 | 7 | 8 |
    | items read by the arm | 10 | 13 | **0** | **0** | **0** | **4** | **0** | **0** | **0** | **0** |

    `HOOK_OPEN_LABEL_RE` (`_capture_gate.py:4696`) needs the label *and a colon on one line*. The
    #296+ heading `### OPEN, DAVE'S — every one a QUESTION PUT …` has no colon.
  - **Declared at every wrap, fixed at none.**
    - #303's hook: *"its parser does not match this file's heading form, **as at #297–#302**"*.
    - The same sentence appears in `notes/_subreports/2026-09-23-{298,299,300}-W-wrap.md`.
    - #295's hook `:266`–`:269` calls it the *"Third blindness in this arm's short life"* and puts a
      ruling-shaped question. That question has no ruling (store 638, newest `s295-D4`).

    This is `[[instrument-without-a-consumer]]` in its declared form: the arm's silence is written
    down eight times and it has contributed nothing at eight wraps.
- PREVALENCE: 8 of the 8 hooks since the change de-starred (0 of 8 declared as such). The re-check
  reads 4 of 60 stated items across #296–#303, against 23 of 23 at #294–#295. There are 2 instruments
  and 1 root.
- PROPOSED: **fix the parsers, and keep the filed hooks as they are** (they are ratified record, and
  the gardener already copes with five historical shapes).
  1. In `knowledge/_gardener.py:910`, widen the section pattern to also accept a
     `FOR THE (PLACER|CONDUCTOR)` section and take its **first fenced block** as the index line.
  2. In `knowledge/_capture_gate.py:4696`, accept a `### OPEN, DAVE'S` **heading** as the label, with
     items being the numbered lines up to the next `###`.
  3. Pin both with one selftest bite each, driven off the **real** `notes/_lanes/303/WRAP-MEMORY-HOOK.md`
     (expect `starred True`, and 8 items read), so the next shape change fails loud.

  The cheaper source-side alternative is to restore the literal `## THE INDEX LINE` heading and an
  `Open, Dave's:` label in the wrap-hook step of `knowledge/_RUNBOOK-capture-ritual.md`. That protects
  new hooks only. The `s271-D4` re-check stays ADVISORY either way: its tier is Dave's.
- status: floated

---

### P3 — `_CHAIN.md:46`, the price line every cold boot reads, still quotes the pre-#301 budget ("working 200,000 · quality-max 256,000") and the pre-#278 `MEMORY.md 8,470` split. Code has said 256,000 and 300,000 since #301, and `s294-D7`'s enactment annotated only one of the two surfaces pass 13 P2 named

- EVIDENCE:
  - `_CHAIN.md:46` (generated from `GOOD-MORNING.md:21`) reads verbatim:
    *"**amber 160,000 (PICKED) · working 200,000 (SOURCED) · quality-max 256,000 (SOURCED)** —
    provenance per `_gauge_tokens.py:63–83`, the authority …"*, and later on the same line:
    *"`MEMORY.md` 8,470 of the first-turn figure is split and measured; **56,308 remains
    unattributed**"*.
  - The authority disagrees:
    `python3 -c "import sys;sys.path.insert(0,'knowledge');import _gauge_tokens as g;print(g.BUDGET_AMBER,g.BUDGET_WORKING,g.BUDGET_HARD)"`
    prints `160000 256000 300000`.
    - `knowledge/_gauge_tokens.py:103`: `BUDGET_WORKING = 256_000  # PICKED by Dave #301`.
    - `:88`: `BUDGET_HARD = 300_000  # PICKED by Dave #301`.
    - The gauge's own runtime string (`:623`–`:624`) already prints *"working PICKED Dave #301, was
      200,000"*.

    So **2 of the 3 figures on the line are wrong**, and the labels are wrong too: they say SOURCED
    where the values are now PICKED.
  - The `8,470` half is pass 13 P2's **first-named surface** (`_CHAIN.md:42` then). `f81bbdd4`'s
    message says *"the 8,470 boot term is re-measured BY ADDITION to 5,413 tape"*, and that is true in
    `knowledge/_gauge_tokens.py:194`–`:227`. `grep -n "5,413" _CHAIN.md` returns nothing. The cold
    reader still gets the retired attribution with no pointer to the re-measure.
  - The pointer `_gauge_tokens.py:63–83` is itself a typed line range. `:63` today is inside a comment
    about the 256,000 *record*, not the triple.
  - Precedent: `#79-D2` (`notes/_MEMENTO-DECISIONS.md:2806`), where the triple is asserted *"by import,
    so there is exactly one authority"*. This line is the second place.
- PREVALENCE: 2 of 3 budget figures and 1 of 1 memory-term attributions on the line are stale. It has
  been read by every cold boot since #301 (#302, #303, #304). 1 of 2 surfaces pass 13 P2 named was
  annotated.
- PROPOSED: **generate it** (the strong `s129-D5` form, the `s294-D8` `_gen_size_stamp.py`
  precedent). Have the wrap's stamp generator write the three budget figures and their PICKED/SOURCED
  labels into `GOOD-MORNING.md:21` from `_gauge_tokens` by import. Replace the `8,470 … 56,308` clause
  with a pointer to the `s294-D7` re-measure block. Weak form, if generation is not wanted: delete
  the figures and leave *"values: `_gauge_tokens.BUDGET_*`, by import"*. No constant moves either way.
  The window lines stay his.
- status: floated

---

### P4 — Two parked items were closed by commits that say so, but the register was never written: `P-276-1` now fires "due" at every dream pass for a file that no longer exists, and `P-293-1` waits on an event nothing fires. Separately, 4 event-less rows match every event, so 6 of the 10 items "due at dream-pass" are not addressed to it

- EVIDENCE:
  - **P-276-1.**
    - `03605215` (#293 lane E1) says: *"PASS 13 P6 — `_validate_lane_ownership.py` comes OFF on
      Dave's own `s276-D6` … MOVED to `_to_delete/…`"*.
    - `ls knowledge/_validate_lane_ownership.py` gives *No such file*, and the `_to_delete/` copy is
      gone too (the `s294-D12` purge arm).
    - `python3 knowledge/_parked.py --due dream-pass` still prints *"⏰ P-276-1 — DID THE LANE-OWNERSHIP
      GUARD EVER FIRE? … changed in 2 commit(s) since 3b9d89b"*. The file-changed trigger counts the
      guard's own deletion as a change, so the row is due at every dream pass indefinitely.
  - **P-293-1** (the 8,470 re-measure, parked by `03605215`).
    - `f81bbdd4`'s message says: *"the 8,470 boot term is re-measured BY ADDITION to 5,413 tape … and
      **P-293-1 is named as unparked**"*.
    - Its register row still reads `status: parked`, trigger `{"kind": "event", "name":
      "cold-boot"}`.
    - `grep -rn 'notice("cold-boot")\|--due cold-boot' knowledge/*.py` finds no caller outside
      `_parked.py`, so nothing will ever surface it. (E1's own report, Q1, says the same: *"nothing
      calls `notice("cold-boot")` today"*.)
  - **The register has not been written since.** `git log --oneline 03605215..HEAD --
    knowledge/_parked.json | wc -l` returns **0** (11 sessions, #294–#304).
  - **The event-less rows.** Four `file-changed` rows carry no `event` key: P-273-1, P-274-1, P-277-1
    and P-277-4. So `--due <any event>` matches them. `--due cold-boot` lists P-270-1, P-273-1,
    P-274-1, P-277-1, P-277-4 and P-293-1, and `--due dream-pass` lists the same four. That is why pass
    13's Method had to explain that seven of its nine "due" items *"are not dream-pass questions at
    all"*.
    - E1 raised this at #293 (Q1: *"narrow `--due` so an event-less `file-changed` row does not match
      every event — … affects four existing items"*).
    - #294's review page filed it as *"the conductor's call, not Dave's"*
      (`notes/_subreports/2026-09-21-294-R-review-page.md:77`), and no conductor has taken it.
- PREVALENCE: 2 of 2 register closures announced in commit messages since 2026-09-21 are not
  reflected in the register. 6 of 10 items due at this pass are not addressed to it (4 event-less, 1
  zombie, plus the standing P-269-4 by design; see kk3). 0 register writes in 11 sessions.
- PROPOSED: two separable, reversible steps.
  - **(a) Enactment:** flip `P-276-1` and `P-293-1` to `status: "enacted"` in `knowledge/_parked.json`,
    citing `03605215` and `f81bbdd4`. The vocabulary exists (`_parked.py:16`: *"enacted" … both keep
    the row; history is data*).
  - **(b) Named re-checker:** in `_parked.evaluate`, when a `file-changed` row's watched path no longer
    exists, print `⚠ WATCHED PATH GONE — close or re-point` instead of `⏰ due`, with one selftest
    bite. This catches the zombie class without changing `--due` semantics.

  Narrowing `--due` for event-less rows is a semantics change to four live items. It is **not**
  proposed here; it stays the conductor's call, as #294 filed it.
- status: floated

---

### P5 — Update to `s294-D9` (pass 9 P1's enactment), not a re-float: the pre-flight emitter built at #293 captured at #294 and #295, then returned `⛔ NOT CAPTURED` at 7 of 7 wraps from #296, because `_checkin.TRANSCRIPT_GLOB` sees only the device mount and the conductor now runs in a cloud seat. Every FILL figure since is a hand sum, and 6 hooks carry the defect as "open, mechanical"

- EVIDENCE:
  - `knowledge/_checkin.py:84`: `TRANSCRIPT_GLOB = "/sessions/*/mnt/.claude/projects/*/*.jsonl"`, with
    one pattern and no alternative.
  - `notes/_GAUGE-LOG.md`, with the pre-flight line per session:
    - `:4014` #294 and `:4048` #295 are `✅ CAPTURED … by knowledge/_checkin.read_fill off
      /sessions/<name>/mnt/.claude/projects/…`;
    - `:4078` #296, `:4103` #297, `:4129` #298, `:4155` #299, `:4181` #300, `:4207` #301 and `:4233`
      #302 all read *"⛔ NOT CAPTURED — UNMEASURED. no top-level transcript matched
      `/sessions/*/mnt/.claude/projects/*/*.jsonl` at this seat"*.
  - **The transcript was readable all along, from the seat that needed it.** `:4157` (#299 post-mortem)
    says: *"the conductor ran in the CLOUD and its transcript is
    `/root/.claude/projects/-home-claude/63d0ecfa-….jsonl`, which the device glob cannot see … Every
    figure here is a HAND SUM of `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`
    per distinct `message.id`, main thread only — the check-in's fields."* The #303 wrap report
    (`notes/_subreports/2026-09-26-303-W-wrap.md`, § WHAT I VERIFIED) read FILL *"first-hand over
    `/root/.claude/projects/-home-claude/2164dd10-….jsonl`"*. So the method is `read_fill`'s own; only
    the path is missing.
  - **Carried, not owned.** `grep -l "cannot see a cloud conductor"` finds the line *"`_checkin.py`
    cannot see a cloud conductor's transcript; FILL is a hand sum"* under OPEN, MECHANICAL in 6 hooks
    (#297, #299–#303).
  - Why it matters beyond tidiness: the `s262-D1` Price-vs-actual hunt, the capture gate's
    boot-ceiling arm and pass 12 P2's FILL overshoot are all now fed by hand-typed sums. That is the
    exact CLAIMED-vs-RUN risk `s294-D9` was ruled to end. ⚠ I could not probe `/root/.claude` from this
    seat (`ls` gives *Permission denied*: I am not the cloud seat). The readability claim rests on the
    #299 and #303 wrap seats' own first-hand reads.
- PREVALENCE: 7 of 7 wraps since the cloud move NOT CAPTURED, against 2 of 2 CAPTURED before it. The
  defect is declared in 6 of the last 7 hooks. It is the same class as pass 13's spine (#278): the
  environment moved and the path was not re-pointed.
- PROPOSED: **re-point by addition.** Make `TRANSCRIPT_GLOB` a tuple:
  1. the device pattern;
  2. `/root/.claude/projects/*/*.jsonl` (main-thread files only; `subagents/` is already excluded by
     depth).

  The newest mtime across both wins, and the refusal names **both** probes. Add one selftest bite
  with a fixture under a temp root. No band, ceiling or literal moves, and no dataset is rewritten:
  the seven hand sums stay as filed.
- status: floated

---

### P6 — The void fence built from pass 13 P1 will declare this pass's own fresh refresh VOID at #305's boot, because the pass refreshes the grades *before* it writes its proposals file and the fence treats any newer proposals file as "a pass has fired since anything was graded". Separately, the fence resolves the now-relative `memory_index` against the working directory, not the repo

- EVIDENCE:
  - The fence, `knowledge/_checkin.py:1414`–`:1419`: `if _newest and _ra and _ra < _newest[0]:
    _void = "it was refreshed …, OLDER than the newest dream pass (…) — at least one pass has fired
    since anything was graded"`. `_newest` is the **mtime** of the newest
    `notes/_dream/*-proposals.md` (`:343`–`:355`).
  - This pass's order, which the dispatch confirms: `_gardener.py --refresh` ran first
    (`_MEMORY-GRADES.json` `refreshed_at: "2026-09-27T07:13:35"`, file mtime `07:13:36 BST`). This
    proposals file is written afterwards, so its mtime is later. That makes `_ra < _newest[0]` true
    from the moment this file exists, and the fence will print `⛔ SIDECAR PRESENT BUT VOID` over grades
    that are minutes old. The replay receipt below is run read-only after writing.
  - **Why it has not fired yet:** at pass 13 the refresh BLOCKED, and the #294 re-point refreshed at
    2026-09-21T17:55:57, *after* the 09-20 file. This is the first pass where refresh and proposals
    ran in the ruled order, so it is the first time the fence can misfire, and it will misfire at
    every pass from now on.
  - **Relative path (thin).** Since `s294-D6` the sidecar's `memory_index` is relative
    (`notes/_lanes/303/WRAP-MEMORY-HOOK.md`). `:1410` tests `os.path.exists(_mi)` against the CWD.
    `_checkin.py` has no `chdir` (`grep -n chdir` returns nothing), and `REPO` is only used elsewhere.
    Run from anywhere but the repo root, it voids with the reason *"the store moved at #278 and nothing
    re-pointed the grader"*, which would be false. All documented invocations run from the root, so
    this has not bitten.
- PREVALENCE: 1 of 1 passes since the re-point where refresh ran before the proposals file. It will
  recur weekly by construction. The relative-path half: 0 observed, 1 latent.
- PROPOSED: **one clause each in `knowledge/_checkin.py`, with a selftest bite each.**
  - Treat the sidecar as fresh if `refreshed_at` falls on or after the **calendar date in the newest
    proposals file's name**, or within the same local day as its mtime. Either keeps the fence's
    purpose (a *later* pass with no refresh still voids).
  - Resolve `_mi` with `os.path.join(REPO, _mi)` when it is not absolute.

  ⚠ Nearest the jj8/kk11 line: the subject is the boot surface's fence, not the dream lane's sequence,
  and I am **not** proposing to reorder the pass.
- status: floated

---

### P7 — Two explicit "the wrap will stage this" promises from #293.1 and #294 have gone unkept for 9 wraps. Three tracked files have sat modified since 2026-09-21/22, and 129 of the 169 untracked paths the dispatch attributed to #304 belong to #297–#303

- EVIDENCE:
  - **#293.1** (session `26ec8b1a`, last turn): *"Added to the J7 note … **The hand-up file already
    lists J7, so the wrap sweeps this edit with it.**"* `git diff --stat` shows
    `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` still **+47 lines** uncommitted, mtime
    2026-09-21 19:31. #294's close narrowed that to *"J7 and the idea notes are left in flight by
    declaration"*, so this one is declared.
  - **#294** (session `c65a1dad`, last turn): *"the hook's receipt is appended but not committed … **#295
    stages it**"*. `notes/_lanes/294/WRAP-MEMORY-HOOK.md` is still **+6 lines** uncommitted, mtime
    2026-09-21 19:36. The diff is the `PLACEMENT RECEIPT` paragraph, which is record. #295's close
    does not mention it.
  - `notes/_subreports/2026-09-22-297-A-plain-deck-brain-and-footnotes.md`: **+23 lines**, mtime
    2026-09-22 22:35, after lane A's commits (`_gitcommit-A2.log` 22:18). I found no declaration.
  - **Untracked, by lane:** `git status --porcelain | grep '^??' | grep -v 304` gives **130** paths:
    - `notes/_lanes/297` **50**, `…/303` **27**, `…/299` **22**, `…/302` **15**, and 5 each for 298,
      300 and 301;
    - plus `notes/_context/`.

    #303's wrap declares its own as *"left, declared"* (shots, work files, eight source backups). The
    `s294-D12` gate covers `_to_delete/` only. Nothing ages lane scratch.
- PREVALENCE: 2 of 2 explicit "will be staged" promises unmet across 9 wraps, 3 tracked files dirty for
  5–6 days, and 130 untracked paths from 7 prior sessions. ⚠ **Thin on harm:** nothing is lost. The
  cost is that every wrap's `uncommitted changes` WARN now carries last week's dirt, and a cold reader
  cannot tell carried dirt from live work (the dispatch could not).
- PROPOSED:
  - **(a) Enactment:** the next wrap stages the three tracked files, which are a placement receipt, a
    Dave-words note and a report addendum, all record.
  - **(b) Named re-checker:** `_capture_gate.py --wrap`'s uncommitted-changes WARN splits out paths
    whose mtime predates the **previous** wrap commit, as `CARRIED DIRT — n wraps old`.

  Whether lane scratch (`_msg-*.txt`, `*.term`, `pre-*.html`) is ignored, purged or aged is Dave's, the
  `s294-D12` shape. It is not proposed here.
- status: floated

---

### P8 (thin) — The memory index keeps its "newest three" rule for wrap lines but not for its own cut receipts: ten `✅ THE CUT WAS PAID` paragraphs have accumulated since #296, and the file grew 6,091 B → 8,985 B in three wraps

- EVIDENCE:
  - Read first-hand this pass, read-only: `memory_read` on the Project's `index.md` gave `version
    34877d8ae0fe`, **8,985 of 49,152 B**, updated 2026-09-26T13:39:56Z. It carries **3 wrap lines**
    (#303, #302, #301, so the rule holds and pass 13 P5 is discharged) and then **10** `✅ THE CUT WAS
    PAID AT #…` paragraphs (#296 opener, #296 wrap, #298, #299 and #300 openers, and the #300, #301,
    #302 and #303 wraps), plus the #285 and #293 standing notes.
  - `notes/_subreports/2026-09-23-300-D-memory-store.md:41` measured `index.md` at **6,091 B** at #300.
    That is +2,894 B over the three wraps since, about 965 B per wrap, and each receipt restates what
    `MEMORY-ARCHIVE-3.md`'s own batch heading already records.
  - ⚠ **Why thin:** under Dave's #300 Project instructions the opener neither reads nor writes memory
    (`notes/_lanes/300/PROJECT-INSTRUCTIONS-v2-LIVE.txt`). I could not establish whether `index.md`'s
    body is in the boot's memory list (lane D measured the list at about 20K real, #300). So the boot
    cost is **unproven**. The monotone growth is proven.
- PREVALENCE: 10 receipts in 8 sessions (#296–#303), 1 per placement. +2,894 B across 3 wraps.
- PROPOSED: **one sentence added to the index's own standing rule:** *"the receipt for a cut moves
  with the line it moved, into the same shard batch"*. Then move the ten receipts verbatim to
  `MEMORY-ARCHIVE-3.md` beside the batches they describe. This is reversible and loses nothing.
  ⚠ Only the conductor's seat writes the store. That makes it the conductor's enactment at a wrap,
  after Dave says he is done.
- status: floated

---

## Checked-clear this pass. For the next pass, do not re-open

- **(kk1) Correction to the dispatch: pass 13's seven are NOT awaiting Dave. All seven were acted on
  within two days.**
  - `03605215` (#293 lane E1) enacted P1's fence, P4's regex (`knowledge/_state.py:126`, now
    `(?:[a-z][a-z0-9]?)?`), P6's guard removal, P7's `DUPLICATE HEADING` emitter, P3's weak form and
    P2's annotation. The conductor sharded the index for P5 (live `index.md` confirms three lines and
    `MEMORY-ARCHIVE-3.md`).
  - Dave then ruled the residues at #294: `s294-D6` (P1 re-point), `s294-D7` (P2 re-measure) and
    `s294-D8` (P3 generate), all `ENACTED … f81bbdd4`.
  - The only residues are the ones this file names: P2's `_CHAIN.md` surface (→ P3 here) and P6's
    parked row (→ P4 here).
- **(kk2) Correction to the dispatch: pass 9's six are not awaiting Dave either.** P3 → `s294-D4`,
  P4 → `s294-D6`, P1 → `s294-D9` (enacted; P5 here is an update to that enactment, not a re-float),
  and P2, P5 and P6 were classed *overtaken* by the #278 move
  (`notes/_subreports/2026-09-21-294-R-review-page.md:67`).
- **(kk3) Gardener, P-269-4 and near-dupes: answered, not re-floated.**
  - Pass 13 P1 is wholly answered: `--refresh` runs against the repo mirror (`population_source:
    repo-mirror (s294-D6)`).
  - STALE 4 (277, 279, 288, 295) are real grades. `AGING 0` is structural and the sidecar says so
    (`limit_can_bite: false`, oldest member 12.4 d vs 30 d).
  - The population's **+10** is exactly #294…#303 joining since the 2026-09-21 refresh (23 → 33), so
    it is expected.
  - `_near_dupes.py`: 22 pairs over 1,047 records. The 1.00 pair has slid to `_GM-ARCHIVE.md:5548` /
    `:6741`, which is the stale-pointer point pass 13 P7 made. P7's re-checker is built and `s273-D4`
    names the watcher.
  - P-269-4 is an `event` row by design, so it will be due at every pass. That is a standing
    instruction, not a zombie, unlike P-276-1 (P4).
- **(kk4) The other due parked items are Dave's and have not rotted:** P-274-1, P-272-1…4, P-273-1,
  P-277-1 and P-277-4. P-277-1's diagnosis still holds today: `_rules-index.json`'s `dv-019` row still
  opens *"Only palette colours in charts …"* and ends `{#dv-017}`. That needs a lane and a Dave choice,
  not a dreamer.
- **(kk5) The boot-ceiling red on the cloud seat and the window moves are HIS, and put.** Boot at
  126,178–128,423 vs `BOOT_CEILING_TK` 72,768 is carried as a question put at #300 Q5 through #303 Q8.
  #303's FILL 402,607 over the 300K hard line (hook) corroborates **pass 12 P2**, which is referenced,
  not re-floated.
- **(kk6) Zero rulings inscribed #296–#303 (store 638) is not a dropped loop.** Each wrap gives the
  reason (*"he did not say 'inscribe'"*, `knowledge/_standing.md:23`).
- **(kk7) Pass 12's (ii4) date-split note is superseded, not re-opened.** (ii4) declined to float the
  stamp question because it was *"carried, aged and his"*. It has since been ruled (`s294-D11`), so P1
  is about enactment, and that is new evidence.
- **(kk8) Pass 13 P3's size stamp is healthy.** `GOOD-MORNING.md:18` is GENERATED by
  `_gen_size_stamp.py` (33,667). Measured at this seat, GM is 34,136 tape at HEAD. The 469 gap is the
  declared 5b tail and the stamp no longer claims "exact".
- **(kk9) Correction to the dispatch's tree attribution.** 169 untracked, of which **39** are #304's
  (`notes/_lanes/304*`, `_REVIEW-304-*`, `_SITTING-304-*`, the 304 subreports and receipts) and **130**
  are #297–#303's plus `notes/_context/` (P7). The 6 modified paths are 2 dream sidecar files
  (dirtied by this pass's refresh, per the dispatch), 1 #304 report, and 3 carried from #293, #294 and
  #297 (P7). `.git/index.lock` gave *"unable to unlink … Operation not permitted"* on my read-only
  `git status`. I left it alone ([[git-lock-mv-not-rm]]).
- **(kk10) What this pass wrote: one file, this one.**
  - **Memory:** `memory_list` and one `memory_read` of the Project's `index.md`, both read-only. No
    memory write.
  - **Read-only runs:** `_parked.py --due dream-pass` and `--due cold-boot`, `_validate_wiring.py`
    (0 failures; `_validate_demo_page.py` exempt by name) and `_near_dupes.py`.
  - **Imported, not run:** `_capture_gate.hook_open_items_recheck` (the function writes nothing) and
    `_gauge_tokens` constants.
  - **Not run:** `_checkin.py` (it appends to counted datasets), `_gardener.py` (the conductor already
    ran `--refresh`) and `_build_all.py`.
  - **Git:** read-only only (`log`, `status`, `show`, `diff --stat`, `ls-files`).
  - `pip install tiktoken` touched the sandbox's Python only, not the repo.
- **(kk11) Out of scope by standing exclusion** (cc6…jj8): the cadence, the conductor sequence, the
  §🔀 row and `_dream/` gating. **P6 sits nearest the line.** Its subject is `_checkin.py`'s boot
  fence, which prints on every session opener, and it explicitly does not propose reordering the pass.
- **(kk12) `_validate_demo_page.py` is exempt by name** (*"wire-or-retire is Dave's, review page
  #293"*), while the #294 page excluded it as *"purpose already ruled — enactment, not judgement"*
  (`s268-D3`). The two surfaces disagree about whose it is. I considered floating it as a dropped loop
  and did **not**: the exemption is the gate's own prescribed remedy, it is visible on every wiring
  run, and it is one item. Noted so the next pass does not rediscover it cold.

---

## Method

**Inputs, in the spec's order.**
1. **The memory index.** `MEMORY.md` no longer exists (the #278 move). I used the repo mirror
   `notes/_lanes/*/WRAP-MEMORY-HOOK*.md` as the spine (33 files, newest `303/`), and this seat *could*
   read the Project cloud store read-only, so the live `index.md` was read first-hand (P8, kk1).
2. `GOOD-MORNING.md` header (lines 1–30, `:9`–`:21`), the `_CHAIN.md` head, `:21` and `:34`–`:46`,
   and `_LIVE-STATE.md` grepped for the pass-13 row.
3. Transcripts.
4. Every checkable claim was spot-checked against the repo before citing.

**Also read:** pass 13's file in full, the checked-clear lists of all 13 prior files (grepped for
this pass's subjects: `WRAP DATE SPLIT` hit only pass 12's ii4, see kk7), `knowledge/_rulings.json`
by field extraction (638 records, `s294-D1…D12` and `s295-D1…D4` read), and `_MEMENTO-DECISIONS.md`
by grep only.

**Sessions: the fidelity ceiling bound harder this week than any before, and it did so structurally.**
`list_sessions` (limit 60) shows nothing newer than **#295**. **#296–#304 are not visible to this
seat at all.** The repo record explains why: from about #296 the conductor ran in a **cloud** seat
(`/root/.claude/projects/-home-claude/…`, `notes/_GAUGE-LOG.md:4157`). So the last ~15 *visible*
sessions were the window:

- read: #295 `a3aa785d` (tail 6), #294 `c65a1dad` (5), #293 `f7975cc0` (4), #293.1 `26ec8b1a` (2),
  #292 `3a8e3a69` (2), and pass 13's own scheduled session `6544529a` (3);
- not re-read: #291 ×2, #289, #288…#282. Pass 13 read them in depth last week and nothing this pass
  turned on them.

For **#296–#303** I read the repo's own copy instead: each `WRAP-MEMORY-HOOK.md`, the
`2026-09-23-{298,299,300}` and `2026-09-24-302` / `2026-09-26-303` wrap reports, and the
`_GAUGE-LOG.md` strata. **#304** has no hook or handoff yet (it appears unwrapped). I did not read
its untracked files beyond counting them (kk9).

**What transcripts contributed: three pieces of speech, no numbers.** #293.1's *"the wrap sweeps this
edit"* and #294's *"#295 stages it"* (P7), and pass 13's close (kk1). Every figure in this file is a
command run here or a line read in the repo.

**Where the ceiling limited a finding.**
- P5's claim that the cloud transcript is readable rests on the #299 and #303 wrap seats' first-hand
  reads. `/root/.claude` is *Permission denied* here.
- P8's boot cost is unproven (stated in P8).
- P2's "declared at every wrap" is from the hooks and wrap reports. I could not see whether the cloud
  chats raised it to Dave in words.

**Replay these** (from the repo root; all read-only):

```
grep -c "WRAP DATE SPLIT" GOOD-MORNING.md _CHAIN.md          # 8 and 8                           — P1
python3 -c "import json;r=json.load(open('knowledge/_rulings.json'))['rulings'];print([v['status'] for v in r if v['id']=='s294-D11'])"   # ['ruled'] — P1
python3 -c "import json;g=json.load(open('notes/_dream/_MEMORY-GRADES.json'));print([(e['id'][:3],e['starred']) for e in g['entries'] if e['id']>='296'])"   # all False — P2
for n in 296 303; do grep -o '^- \[★*' notes/_lanes/$n/WRAP-MEMORY-HOOK.md|head -1; done   # - [★★ twice — P2
python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print(g.hook_open_items_recheck('.','notes/_lanes/303/WRAP-MEMORY-HOOK.md')[1][0][:160])"   # '… · 0 "Open, Dave's" item(s) read' — P2
python3 -c "import sys;sys.path.insert(0,'knowledge');import _gauge_tokens as g;print(g.BUDGET_AMBER,g.BUDGET_WORKING,g.BUDGET_HARD)"   # 160000 256000 300000 — P3
grep -c "working 200,000 (SOURCED)" _CHAIN.md                 # 1 — P3
python3 knowledge/_parked.py --due dream-pass | grep -c "P-276-1"; ls knowledge/_validate_lane_ownership.py   # 1 ; No such file — P4
git log --oneline 03605215..HEAD -- knowledge/_parked.json | wc -l      # 0 — P4
grep -c "pre-flight #29[6-9]:\*\* ⛔ NOT CAPTURED\|pre-flight #30[0-2]:\*\* ⛔ NOT CAPTURED" notes/_GAUGE-LOG.md   # 7 — P5
grep -n '^TRANSCRIPT_GLOB' knowledge/_checkin.py              # :84, one pattern — P5
python3 -c "import os,datetime,sys;sys.path.insert(0,'knowledge');import _checkin as c,json;g=json.load(open('notes/_dream/_MEMORY-GRADES.json'));print(c._grades_refreshed_epoch(g)<c._freshest_proposals_mtime()[0], c._freshest_proposals_mtime()[1])"   # True 2026-09-27-proposals.md — P6
git diff --stat notes/_lanes/294/WRAP-MEMORY-HOOK.md notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md   # +6, +47 — P7
```
