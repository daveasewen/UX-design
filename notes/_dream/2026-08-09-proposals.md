# Dream pass 6 — floated proposals

provenance: local_38462ae9-34cb-4dba-a48e-fa7b69c92894 · 2026-08-09
status: floated

*Shape A (Cowork), scheduled Sunday 07:10 fire — the lane's first pass that was neither manual nor
overdue. Five proposals, ranked by prevalence. **Nothing here is ruled, promoted or enacted**;
promotion is Dave's alone (derivation-governance). Every prior pass's RULED rows and checked-clear
items were read before hunting and are not re-opened — where a finding touches the same class as an
earlier one, it says so and says what is new.*

---

### P1 — **Twenty-one of the ninety-six rulings in the store carry an identical status string frozen at a #119 metadata sweep — and at least one of them says "unknown" in the field designed to answer the question while its own `says` field states the answer**

- EVIDENCE:
  - `knowledge/_rulings.json` — **21 records** carry the byte-identical status
    *"RULED #<n> - status field added #119 in a metadata sweep; enactment state NOT asserted here
    (UNPROVEN by this sweep) - read the evidence pointers"*. Grep count: 21 occurrences of
    `enactment state NOT asserted here (UNPROVEN by this sweep)`; total records in the file: **96**
    (`"id":` count). The affected span is `#96` → `#110`.
  - **The self-contradicting record.** `ds-033` (`_rulings.json:446–459`):
    `says` = *"…**NOT ENACTED**: the literal at type.css:180 (`[data-theme="dark"]{background:#111;color:#fff}`)
    still reads #111 — the ruling is recorded, the code has not been changed."*
    `status` = *"RULED #108 - … enactment state NOT asserted here (UNPROVEN by this sweep)…"*.
    **The record knows and the status field says it does not.**
  - **Verified live today, not inherited:** `knowledge/canon/type.css:180` still reads
    `[data-theme="dark"]{background:#111;color:#fff;}`. Ruled #108 (2026-08-06); unenacted at #136.
    `GOOD-MORNING.md` DO-FIRST item 19 carries the same fact in prose — so the project holds
    *known-unenacted* in one register and *unknown* in the register a reader queries.
  - **The string is republished, not inert.** `knowledge/_governs.py:209` prints
    `status: {r.get('status', 'unstated')}` verbatim, and `:289` carries `status` in its field list —
    so any consult/governs reader asking "is this enacted?" is handed the 17-session-old sweep text.
  - **Nothing re-checks it.** No gate greps for the sweep string; the sweep is dated to #119 and the
    chain is at #136 — seventeen sessions with no re-assertion and no expiry.
- ⚠ **Not a re-float, and the boundary matters.** Pass 5's P1 (RULED `s128-D1`) was about six rulings
  **absent from** `_rulings.json`; this is about rulings **present in it whose status field is
  permanently agnostic**. Pass 3's P2 (RULED, enacted #22) was about the enactment register's
  *corpus coverage*. Different object each time. ⚠ Also note the spec's own steer — *UNPROVEN is
  honest, target CLAIMED first*. This is floated **not** because UNPROVEN is dishonest but because
  an UNPROVEN with no price, no re-checker and no expiry is exactly the debt `s129-D5` names, and
  `ds-033` proves at least one of the 21 is answerable from material already in the same record.
- PREVALENCE: **21 of 96 records (22%)** in one file · 1 demonstrated self-contradiction · 1
  repo-verified live literal · 1 consumer that republishes the string · 17 sessions unchanged.
- PROPOSED: **one of the three `s129-D5` triage options — the named re-checker, as the smallest.**
  Add a check to `knowledge/_governs.py --selftest` (or `_capture_gate.py --wrap`, whichever Dave
  prefers as the home) that counts records whose `status` still contains the `#119 metadata sweep`
  string and reports the count at every wrap, so 21 silent unknowns become one visible, moving
  number. ⛔ Do **not** bulk-rewrite the 21 statuses to "ENACTED" — that manufactures the exact
  CLAIMED class ADR-0016 forbids. `ds-033` specifically can be closed from its own `says` field, but
  closing it is a ruling, not an agent's move. Touches: `knowledge/_governs.py`,
  `knowledge/_rulings.json` (read-only for the check).
- status: floated

---

### P2 — **The instruments that verify a commit write to a tracked file, so verifying after committing dirties the tree — and since `s133-D2` that residue does not just look untidy, it makes the ruled push path refuse**

- EVIDENCE:
  - **The mechanism, read off the script, not recalled.** `knowledge/_git_commit.sh` runs
    `python3 knowledge/_capture_gate.py --wrap` at **:153/:157** and stages at **:300–316**. Both
    `_capture_gate.py` and `_checkin.py` append a record to `notes/_REHEARSAL-LOG.jsonl` on every
    run (memory hook `feedback-context-gauge`: check-in = `knowledge/_checkin.py`). A gate run
    *inside* the script is therefore captured by the later staging; **anything run after the commit
    is not.**
  - **The new teeth.** `_git_commit.sh:38` — `[ -z "$(git status --short)" ] || { echo "✗ push
    refused: tree not clean — commit first (s133-D2)"; exit 1; }`. Verifying a commit after making
    it now *blocks the push that `s133-D2` exists to allow*. The class predates #133; the refusal
    does not.
  - **Nine instances across the transcript window**, each declared and none repaired:
    #115 (`notes/_MEMENTO-DECISIONS.md:4537` — *"the +1 `notes/_REHEARSAL-LOG.jsonl` lines inside
    `9b47152`/`ce0cc7f`"*) · #123 (*"the two rehearsal-log lines went in as `0eacf2d`"*) · #124
    (*"that post-wrap gate-confirmation dirtying the rehearsal log has now happened **twice** — it's
    a class, carried as an observation, **not ruled**"*) · #125 (diagnosed in full, and Dave's own
    screenshot was the receipt: *"commit has 300 lines, disk has 301"*) · #128 (*"tree clean except
    the flagged jsonl"*, then *"the jsonl residue committed knowingly (13 lines by now)"*) · #129
    (*"one rehearsal-log line rolls dirty into #130"*) · #134 (*"tree clean but for my own
    verification run's rehearsal-log append — declared, left for #135's sweep"*) · #135 (the push
    stack names *"the rehearsal-log append"* as one of its four commits) · **and this dispatch**,
    which records the tree dirty with `notes/_REHEARSAL-LOG.jsonl` at fire time.
  - **The remedy was priced and then lost.** #125 rolled it as a priced item — *"move the log write
    ahead of the staging seam, or exclude the log from the clean-tree assertion and stop claiming
    something the wrap can't know"*. It appears in **no** carry list today: greps of `_LIVE-STATE.md`
    and `GOOD-MORNING.md` for `REHEARSAL-LOG` return only the #104 unattributed-path line
    (`_LIVE-STATE.md:923`, where the log is listed as *accounted for*) and gauge-log strata. Neither
    the GM DO-FIRST worklist nor `_LIVE-STATE` § OPEN carries it. **Eleven sessions, priced once,
    homed nowhere.**
- PREVALENCE: **9 sessions of 15 read** · 1 priced remedy dropped from every carry list · 2 script
  line ranges that create the loop · 1 live instance at this pass's own dispatch.
- PROPOSED: **exclude `notes/_REHEARSAL-LOG.jsonl` from the `--push` clean-tree assertion at
  `knowledge/_git_commit.sh:38`** — the one tracked file the verification instruments themselves
  write, named explicitly so the exclusion cannot silently widen. Smallest and fully reversible
  (one line). Two alternatives exist and are Dave's to prefer instead: move the append after the
  staging seam (fixes the ordering, larger blast radius), or stop tracking the log (loses the
  rehearsal record's history). ⛔ Do not blanket-relax the clean-tree gate — its refusal is doing
  its job on every other path.
- status: floated

---

### P3 — **`_RUNBOOK-git-commit.md` still says "GitHub Desktop only (never terminal push)" three sessions after Claude began pushing from the terminal on Dave's word — and the staleness was flagged as owed at #128 and has not been touched since**

- EVIDENCE:
  - `knowledge/_RUNBOOK-git-commit.md:7` — *"Companion to memory `git-push-method`; **git split =
    Claude commits, Dave pushes via GitHub Desktop**."*
  - `knowledge/_RUNBOOK-git-commit.md:99` — *"**GitHub Desktop only** (never terminal push — it hangs
    on credentials)."* Greps of the file for `--push` return **0 hits**.
  - **What is actually live.** `s133-D2` (`notes/_MEMENTO-DECISIONS.md:5684–5690`): *"GATED PUSH:
    CLAUDE MAY PUSH ON DAVE'S WORD, MASTER, FF-ONLY, VERIFIED"*, `--push` mode added to
    `knowledge/_git_commit.sh:35–40` as *"the ONLY push path"*. **Exercised twice, first-hand:**
    #133 (*"Pushed and verified — remote master == local `98f1f19`"*) and #135 (*"Pushed and
    verified — remote master == local `81c3371`, four commits up"*).
  - **The memory index and the runbook now disagree.** Hook `git-push-method` already carries
    *"★ s133-D2: push via `_git_commit.sh --push` on Dave's explicit word only"*. The runbook that
    the hook names as its companion says the opposite. Per the Memento trust hierarchy that is the
    wrong way round: the **tattoo** is stale and the **Polaroid** is current.
  - **It was flagged and dropped.** #128's closing message, item ③ of "three small things left
    yours": *"`_RUNBOOK-git-commit.md` still describes the old call form — left for you or the next
    wrap rather than edited unasked."* Eight sessions (#129–#136); the file still describes the old
    call form, and `s133-D2` has since added a second contradiction on top of the first.
- ⚠ **Same class as pass 4's P3 (RULED, enacted), different artefact.** That one was
  `_RUNBOOK-capture-ritual.md:89`. This is the recurrence of the class in the runbook that memory
  flags as the most-reconstructed-from-memory of all (`feedback-read-the-runbook`: *"recurred #133
  AND inside the #134 wrap sub"*). Stating it as a recurrence, not a re-float.
- PREVALENCE: **2 stale clauses in 1 runbook** · 0 mentions of the live call form · 1 explicit
  hand-off of the item at #128 · 8 sessions untouched · 2 first-hand contradicting pushes.
- PROPOSED: **amend `knowledge/_RUNBOOK-git-commit.md` by addition** — one clause at `:99` recording
  that `bash knowledge/_git_commit.sh --push` is the ruled terminal path (`s133-D2`: master ·
  ff-only · verified · Dave's explicit word), Desktop remaining legal per the ledger's own
  *"SUPERSEDES … BY ADDITION — Desktop remains"*; and update `:7`'s one-line summary and the `:27`
  call-form block to name `--push` alongside `--reconciled`. ⛔ Never trim the Desktop text —
  `feedback-header-wins-over-audit` and the ledger both keep it in force.
- status: floated

---

### P4 — **The push credential's shape is inscribed in two standing places as "this repo, Contents r/w, 90d" — the session that installed it said on the record that the token in force is broader than that, nothing re-checks either the scope or the expiry, and the script's own refusal message instructs pasting a live credential into chat**

- EVIDENCE:
  - **The inscribed premise, twice.** `notes/_MEMENTO-DECISIONS.md:5688` — *"Auth: fine-grained PAT
    (this repo, Contents r/w, 90d expiry) in the remote URL on his disk."*
    `knowledge/_git_commit.sh:39` — *"Dave: fine-grained PAT (this repo, Contents r/w, 90d) → **paste
    to Claude** → `git config remote.origin.url https://<TOKEN>@github.com/daveasewen/UX-design.git`"*.
  - **What #133 recorded about the credential actually installed** (its own words, on the record):
    *"this one is broader than the ruled shape (single repo, 90 days); it works, but narrowing it
    when convenient keeps the blast radius small."* Dave's preceding message offered it as
    *"god access"*. So the standing premise describes a credential that is not the one in force —
    the `s129-D5` **environment-premise** medium, the seventh of the seven media.
  - **Nothing re-checks either half.** `_git_commit.sh:38–39` tests only that the remote URL contains
    `@github.com`; it cannot see scope, and it cannot see expiry. A 90-day token minted 2026-08-08
    expires around **2026-11-06**, at which point the ruled push path fails with a message that
    still describes a token nobody re-issued. No date is stamped anywhere.
  - **The instruction is the mechanism.** *"paste to Claude"* is what produced **three live PATs in
    the #133 transcript** (two superseded, one in force). Two were flagged for revocation in-session
    and Dave replied *"done"* — chat-only, unverifiable from the repo.
  - ✅ **Checked, and clean:** a repo-wide grep for `github_pat_` / `ghp_…` returns **0 files**. No
    credential material has leaked into any tracked or untracked file. This proposal is about the
    standing instruction and the stale premise, **not** about a leak.
- PREVALENCE: **2 standing repo assertions** contradicted by **1 first-hand session statement** · 1
  unstamped expiry with a computable date · 3 credentials transited chat in 1 session · 0 leaked
  bytes in the repo.
- PROPOSED: **two one-line amendments, both by addition, both reversible, neither of them a ruling.**
  (a) Stamp the ledger's Auth line at `notes/_MEMENTO-DECISIONS.md:5688` with what is actually in
  force **and an expiry date** — the `s129-D5` "expiry" triage option, so that quoting the line after
  that date is a declared defect rather than a silent one. (b) Re-word `knowledge/_git_commit.sh:39`
  so the refusal tells Dave to run the `git config remote.origin.url` line **himself**, rather than
  to paste the token to Claude — the credential then never transits the chat and the gate behaves
  identically. ⛔ Whether to narrow the token's scope is **Dave's security call and is not proposed
  here**; only the record's accuracy and the instruction's shape are.
- status: floated

---

### P5 — **A `--all-dirty` escape hatch that a sub added to the commit script on its own initiative — never Dave's words — has been awaiting his one-word verdict since #128 and has fallen out of every carry list (thin)**

- EVIDENCE:
  - **It exists and is live:** `knowledge/_git_commit.sh:15` (usage), `:57` (`--all-dirty) ALLDIRTY=1`),
    `:303`, `:311`.
  - **Its provenance is declared, and it is not Dave's.** #128's closing message: *"The sub added an
    `--all-dirty` escape hatch to the commit script (**its construction, not your words**) — say the
    word if you want it gone."* At the same session's end all three open items were said to *"roll
    to #129"*.
  - **What it is an escape hatch *from*.** `_git_commit.sh:19` — *"`git add -A` RETIRED — ruled Dave
    2026-08-02 (dream pass 4, P5 'ACCEPTED, option (a)'), enacted"* — and `:300` *"EXPLICIT-PATH
    STAGING … `git add -A` is gone"*. The hatch restores stage-everything behaviour under a new
    name; it does echo each path first, which is a real mitigation, and the ruling's own status text
    discloses it (`_rulings.json:1287`, `_CAPTURE-GATE.md:78`).
  - **The loop dropped.** The disclosure lives inside a ruling's status string; the **open question
    to Dave** lives nowhere. It is absent from the GM DO-FIRST worklist, from `_LIVE-STATE` § OPEN,
    and from every residual list #129 → #135.
- ⚠ **Thin, and labelled thin:** the hatch is disclosed, mitigated by its echo, and has caused no
  observed harm in eight sessions. What is floated is the **dropped question**, not the code.
- PREVALENCE: 1 feature · 4 code sites · 1 question put once · 8 sessions with no mention in any
  carry list.
- PROPOSED: **one line in `_LIVE-STATE.md` § OPEN** homing the question ("`--all-dirty`: sub-authored
  #128, keep or remove — Dave's word"), so it is answerable rather than invisible. ⛔ Do not remove
  the flag unasked — it was disclosed at birth and removing agent-added machinery without his word
  is the same overreach in the other direction.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(cc1) No credential material is in the repo.** A whole-tree grep for `github_pat_` and `ghp_…`
  returns **0 files**, including untracked ones visible to the file tools. The three PATs pasted at
  #133 exist only in that session's transcript. P4 is about the record and the instruction; there is
  no leak to hunt.
- **(cc2) Pass 5's P3 prediction is now MOOT at its stated mechanism, and closing it is the useful
  answer.** P3 predicted `notes/_dream/…-proposals.md` being swept into an unrelated commit by
  `git add -A`. That call is **retired**: `knowledge/_git_commit.sh:19` records the retirement and
  `:300–316` implements explicit-path staging. The mechanism the prediction rested on is gone.
  A future sweep would now require someone to type `--all-dirty` (which is P5's object). Pass 5's P3
  was floated thin and never ruled — it should be read as **overtaken**, not as still-open.
- **(cc3) The #125 playwright/TLS contradiction is homed, not lost.** `_LIVE-STATE.md` § OPEN carries
  *"⚠⚠ CONTRADICTION — TWO FIRST-HAND SANDBOX READINGS OF THE PLAYWRIGHT DOWNLOAD (born #125)"*, and
  memory carries a second datapoint from #134 (pip ENOSPC at a fixed cutoff despite free disk). Two
  first-hand readings recorded with no winner picked is the discipline working.
- **(cc4) "RULED NOT ENACTED" is not, by itself, drift.** `s135-D1` and `s135-D4` are both stamped
  RULED NOT ENACTED **and** carried as residual items ① and ④ with age brackets. That pairing is the
  system working exactly as `s128-D2` intended. P1 above is about rulings whose enactment state is
  recorded as *unknown*, which is a different failure.
- **(cc5) The zero-byte `.git/index.lock` on the mount is a known, recorded wart** (memory hook
  `git-lock-mv-not-rm`; named first-hand at #132 and #135, git working anyway both times). Not a
  finding.
- **(cc6) Out of scope by standing exclusion, recorded so it is not mistaken for an oversight:** the
  generated lanes index still shows `M12 — first UNATTENDED Sun 08-02 07:10 fire … queued` while
  `notes/_dream/2026-08-02-proposals.md` exists. That is **dream-lane mechanics**, which this pass is
  barred from floating. Noted, deliberately not proposed.

---

## Method

**Shape A (Cowork).** Dispatched 2026-08-09 by the scheduled Sunday 07:10 fire; date supplied by the
conductor from the host's `date`, not recalled. Conductor session
`local_38462ae9-34cb-4dba-a48e-fa7b69c92894`. Repo root `/Users/daviewen/Documents/Claude/Projects/UX-design`.

**Read, in spec order:** `MEMORY.md` memory index (hooks only, as injected context) ·
`.claude/agents/dreamer.md` (the steering spec, in full) · `GOOD-MORNING.md` header + ★ LATEST + ★
PRIOR banners + the DO-FIRST worklist and POINTERS block · `_LIVE-STATE.md` lines 1–106 (header,
LANES, §🔀 dream-lane rows, ⏱ LATEST and PRIOR deltas) plus a section-head index of the rest ·
**all five prior proposals files** (every heading, pass 4's and pass 5's checked-clear lists in full,
pass 5's P3 body and Method in full) before hunting anything. Targeted repo forensics:
`knowledge/_rulings.json` (status census + `ds-033` record), `knowledge/_governs.py` (status
consumers), `knowledge/canon/type.css:180` (the live literal), `knowledge/_git_commit.sh` (push mode,
gate/stage ordering, staging retirement, `--all-dirty`), `knowledge/_RUNBOOK-git-commit.md`,
`notes/_MEMENTO-DECISIONS.md` (§ `s133-D2`, rehearsal-log occurrences), `knowledge/_CAPTURE-GATE.md`,
plus whole-tree greps for `github_pat_`/`ghp_…` and for `REHEARSAL-LOG` homing.

**Transcripts — 15 read, 0 skipped.** #136 `local_d4febbac` · #135 `local_2cf6d771` · #134
`local_366080a7` · #133 `local_47c7b4cf` · #132 `local_5aca6a78` · #131 `local_4a0e07e0` · #130
`local_010e8021` · #129 `local_b0b574eb` · #128 `local_a590b514` · #127 `local_326fddf1` · #126
`local_d0e4102e` · #125 `local_d7cef1dd` · #124 `local_bb329f45` · #123 `local_02439cd1` · #122
`local_f3dee276`. Each read tail-first at a message limit sized to the session (45 for the live #136,
40 → 10 for older ones), which is where the wrap receipts and Dave's rulings sit. ⚠ **This is the
first pass to actually read the window** — pass 5 read one transcript of fifteen and said so; the
chat-only class it could not hunt is where P2's #124/#125 receipts and P4's #133 receipts come from,
and neither would have been findable from repo artefacts alone.

**Where the fidelity ceiling bit.** The known Shape A ceiling — turn-level only, tool calls as bare
names with no arguments or results — meant that **every** transcript claim used above was re-verified
against the repo before being cited: the script line numbers in P2 and P3, the runbook clauses in P3,
the `--all-dirty` sites in P5, the `ds-033` record and the `type.css:180` literal in P1, and the
absence of any credential bytes in P4. Two things the ceiling cost this pass, stated rather than
disguised: (1) I could not see *which* paths any session staged, only that `_git_commit.sh` was
called — so P2's nine instances rest on the sessions' own prose plus the repo mechanism, not on
observed diffs; (2) I have no shell and no git, so no claim here rests on `git log`, on a gate run, or
on any measurement I could not make with a file tool. Where a number is quoted it is a grep count or
a line read, and it says which.

**Prevalence discipline.** Every `N of M` above counts files, records, grep hits or named sessions —
never an impression. P5 is labelled thin on its face and ranked last for that reason.
