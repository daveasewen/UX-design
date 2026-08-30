# Dream pass 10 — floated proposals

provenance: `local_85a77eb9-9ba0-4dbf-afa6-94788367d4ce` · 2026-08-30
status: floated

*I PROPOSE ONLY. Nothing here self-promotes; promotion is Dave's alone on reading this file
(derivation-governance). Every RULED row in `notes/_MEMENTO-DECISIONS.md` and every checked-clear item
at the end of EVERY prior proposals file — pass 3's prose list, pass 4's (q)–(w), pass 5's (x)–(bb),
pass 6's (cc1)–(cc6), pass 7's (dd1)–(dd7), pass 8's (ee1)–(ee7), pass 9's (ff1)–(ff7) — was read
before hunting. **Proposals from passes 6/7/8/9 that are still FLOATED are referenced where new
evidence bears on them, never re-floated** (see gg4, gg5). Standing exclusion held: dream-lane
mechanics (cadence, conductor sequence, the lane's §🔀 row, `_dream/` gating) are barred from floating
— cc6/dd7/ee7/ff7 precedent, see (gg9).*

★ **Shape A (Cowork), scheduled Sunday 07:10 fire.** Date taken from the host: `date` → `Sun Aug 30
07:26:09 BST 2026`, corroborated mechanically by `notes/_dream/_MEMORY-GRADES.json`
`"refreshed_at": "2026-08-30T07:12:03"`. Live tree verified before measuring: `git log --oneline -1`
→ `48df9c6`, matching the dispatch; 4 modified paths, exactly the declared baseline.

Ranked by prevalence, highest first.

---

### P1 — `s218-D7`'s three PARSED contract lines are invisible to their own parser in most filed reports, and the rate got **worse** after #221 fixed one of the three: of the **15 reports filed since that fix**, only **3** have a parseable `COUNTS:`, **3** a parseable `REPLAY-THESE:`, and **4** a parseable `RULING-SHAPED QUESTIONS` heading

- EVIDENCE:
  - **What the ruling requires.** `knowledge/_rulings.json` § `s218-D7`, verbatim: *"the FILE is sole
    authority; **stub figures are parsed from it, never retyped** … **Stub carries a priced
    REPLAY-THESE line so deferral is declared.**"* The runbook restates it at
    `knowledge/_RUNBOOK-capture-ritual.md:666`: the check *"PARSES each report's `COUNTS:` /
    `REPLAY-THESE:` lines"*. The skeleton calls the COUNTS line *"PARSED, not prose"* and the
    REPLAY line *"also PARSED"* (`notes/_subreports/_TEMPLATE.md:47`, `:86`).
  - **The three parsers**, `knowledge/_capture_gate.py:4652–4656` — `SUBREPORT_COUNTS_RE`,
    `SUBREPORT_REPLAY_RE` (`^REPLAY-THESE:\s*(\S.*)$`), `SUBREPORT_QUESTIONS_RE`
    (`^#{1,6}\s*RULING-SHAPED QUESTIONS\s*$`).
  - **Measured this morning over the whole population** (64 filed reports, `_TEMPLATE.md` excluded,
    the gate's own regexes imported and applied):

    | line | parses | present in the text but unparseable | absent entirely |
    |---|---|---|---|
    | `COUNTS:` | **28** | 27 | 9 |
    | `REPLAY-THESE:` | **21** | 39 | 4 |
    | `RULING-SHAPED QUESTIONS` | **26** | 35 | 3 |

    ⚠ I nearly published *"43 reports have no REPLAY-THESE line"*. A loose search says **60 of 64**
    carry the words. The defect is **decoration and shape**, not omission
    [[unmatched-grep-is-not-an-absence]].
  - **The failure mode, exactly.** The newest reports have migrated from a FIELD LINE to a SECTION
    HEADING: `notes/_subreports/2026-08-29-225-ci-reds-forensics.md:490` → `## REPLAY-THESE`;
    `:575` → `## RULING-SHAPED (named, NOT ruled — ⬛ these are Dave's / the conductor's)`;
    `notes/_subreports/2026-08-29-224-tier1-portback.md:261` → `## REPLAY-THESE`;
    `notes/_subreports/2026-08-28-223-d8-enact-and-bake.md:525` → `## 8. REPLAY-THESE`.
    A heading has no `<path> (~N tk)` items, so **the priced half — the half that makes a deferral
    DECLARED rather than silent — is gone**, not merely unparsed. And
    `notes/_subreports/2026-08-29-225-gumdrop-gate-widening.md:7` writes
    `COUNTS: findings 8 / ruling-shaped 4 / UNPROVEN 2` — slashes, a **fourth** form.
  - ⛔ **And this is the same disease #221 already diagnosed and fixed on ONE of the three.**
    `_capture_gate.py:4631–4640`, verbatim: *"THE GATE AND ITS OWN TEMPLATE DISAGREED, AND THE
    TEMPLATE IS THE INSTRUCTION … MEASURED at #221 across `notes/_subreports/`: **37 of 44** filed
    reports carrying a COUNTS line failed the parse … Fixed on the GATE, not on 37 reports"*, taking
    the parse *"from 13/44 to 24/44"*. **The two sibling regexes on the lines either side of it were
    never re-measured and never widened.** Instance 2 and 3 of a class fixed at instance 1
    [[conflated-fix-guarantees-recurrence]]; Dave's own words on the shape, `MEMORY.md:93`:
    *"always real fixes never patches, they just get lost"* [[feedback-gate-dont-patch]].
  - **It is going backwards, not forwards.** Of the **15** reports filed on or after 2026-08-28 —
    i.e. every report written *since* the #221 widening landed — `COUNTS:` parses **3**,
    `REPLAY-THESE:` parses **3**, the questions heading parses **4**. The corpus rate is 44% / 33% /
    41%; the post-fix rate is 20% / 20% / 27%.
- PREVALENCE: **36 of 64 · 43 of 64 · 38 of 64** filed reports fail the three parses; **12 of 15 ·
  12 of 15 · 11 of 15** among reports filed since the fix. Whole population read mechanically, not
  sampled.
- PROPOSED: the **#221 remedy applied to its two siblings, and nothing else** — widen
  `SUBREPORT_REPLAY_RE` and `SUBREPORT_QUESTIONS_RE` at `knowledge/_capture_gate.py:4655–4656` to
  accept the same ordinary decoration the COUNTS pattern already accepts (leading `#`/`**`,
  a numbered heading prefix), **and re-measure the parse rate in the same motion** so the figure is
  known rather than assumed. ⛔ Explicitly NOT proposed: loosening the *vocabulary* or the field
  order (the #221 comment refuses that deliberately and I inherit the refusal); editing any of the 64
  filed reports (they are dated history, ADR-0017); flipping `SUBREPORT_CITE_BLOCKING`, which is
  Dave's word. ⚠ **Read P2 before pricing this one** — the check that would report the number
  currently has an empty population.
- status: floated

---

### P2 — The constant that answers *"when was the last wrap?"* matches the prefix its own commit script documents as the **NON-WRAP** shape, so it selects the newest commit of any kind: it matches **129 of the last 150 commits**, only 11 of which mention a wrap — and right now it hands both of its consumers an **empty population**

- EVIDENCE:
  - **The two shapes, from the authority.** `knowledge/_git_commit.sh:138–139`, verbatim: *"The prefix
    T3 generates has TWO legal shapes: `after #<n> <date> — ` **(non-wrap)** and `#<n> <date> — `
    **(wrap)**."*
  - **The detector.** `knowledge/_capture_gate.py:4657`:
    `WRAP_COMMIT_SUBJECT_RE = re.compile(r"^after\s+#\d+\b")` — the non-wrap shape, named for the wrap
    one. Its refusal string (`:4712`) tells the reader the same thing: *"no commit whose subject opens
    `after #<n>`"*.
  - **Specificity, counted not recalled.** Over `git log -n 150 --format='%s'`: **129** subjects start
    `after #N`, of which **11** mention "wrap"; 21 start `#N`, of which 0 mention "wrap". The regex is
    satisfied by 86% of all commits.
  - **The live consequence, run from this seat just now:**
    `_last_wrap_commit('.')` → `('48df9c67…', 'after #225 2026-08-29 — #225: Gumdrop arm 5 (advisory)
    + two filed sub-reports rowed W-269/W-270')` — an ordinary work commit — and
    `_changed_since('.', <that sha>, 'notes/_subreports')` → **`[]`**. The `s218-D7` citation check's
    population is empty. **A check that cannot fail** [[instrument-without-a-consumer]].
  - **Two consumers, both blinded the same way.** `subreport_citation_check` (`:4710`) and
    `regen_serial_check` (`:4386`) — the latter is the start point for the ordered regen serial that
    [[regen-serial-set-is-ordered]] records as having cost *"~6 CI reds"* at #210.
  - ⛔ **And its selftest is green because the fixture uses the two shapes correctly.**
    `_capture_gate.py:8354–8356` plants exactly `commit("#217 2026-08-24 — work")` then
    `commit("after #217 2026-08-24 — capture ritual")` — the documented mapping, which the live log
    inverts. The arm proves the CLAUSE ("a subject starting `after #` is found") and never the
    FEATURE ("the last WRAP is found in a real log") [[mutation-tests-the-clause-not-the-feature]],
    [[green-tests-cannot-see-scope]].
  - ⚠ **Honest complication, stated rather than smoothed.** Real wrap commits use BOTH shapes —
    `cbe69e6 after #224 … — the #224 wrap — …` and `540f2cd #217 … — ★★ PHOTOGRAPHY, LOGOS …`. So the
    regex is not wrong *about wraps*; it is **not specific**, and non-specificity is what makes it
    always return the newest commit. Any fix has to key on something other than the prefix.
- PREVALENCE: **1 constant · 2 of 2 consumers · 129 of 150 commits match · population `[]` today.**
  Thin as a count of lines; it is the reason P1's degradation was never reported.
- PROPOSED: the **generate-it** triage (`s129-D5`). Have `_last_wrap_commit` key on a mark the wrap
  itself owns rather than a prefix both kinds share — the wrap commit is the one that moves
  `GOOD-MORNING.md`'s ★ LATEST banner, so `git log --format=… -- GOOD-MORNING.md` plus the existing
  subject match is a two-line change at `knowledge/_capture_gate.py:4669–4678` — **and add one arm to
  `selftest_subreport_citation` that plants a work commit AFTER the wrap commit**, which is the arm
  that would have caught this. ⛔ Not proposed: changing the commit-subject convention (T3's shapes
  are ruled and three other gates count them), or touching `_git_commit.sh`.
- status: floated

---

### P3 — The most-read sentence in the project still says **"75 of 140 steps green (#62) — 65 steps have NEVER been in a green verdict"**, six sessions after this project's own committed record declared that exact figure an artefact: *"`126/128` build steps green DRIVEN INDIVIDUALLY — the 75/128 'record' was a tiktoken-less-sandbox artefact"*

- EVIDENCE:
  - **What every cold session reads.** `_CHAIN.md` STATE line, generated:
    *"⛔ **BUILD VERDICT: 75 of 140 steps green (#62, `18c7789`) — 65 steps have NEVER been in a green
    verdict.** Both counts GENERATED from `_build_all.py`'s AST at each end; the shortfall is computed
    (`s125-D1`)."* Re-derived from this seat: `_gen_chain.build_verdict_line()` returns that string
    verbatim today.
  - **The correction, committed, in the project's own words.** `_GM-ARCHIVE.md:123` (#218 seam 1,
    `adb5130`): *"★ **`126/128` build steps green DRIVEN INDIVIDUALLY — the 75/128 'record' was a
    tiktoken-less-sandbox artefact**, which is why [[sandbox-call-boundary-kills]] says install
    tiktoken first or the reds are noise."* Same sentence in the wrap brief that produced it,
    `notes/_briefs/2026-08-25-218-closing-wrap-brief.md:30`.
  - **A second, independent contradiction.** `notes/_briefs/2026-08-22-215-wrap-brief.md:32`:
    *"**CI: #413 GREEN on `e645df2` — read back in chat, first green in twenty runs.**"* Measured from
    this seat: `_gen_chain.build_steps_at('e645df2')` → **128 steps**. A green CI run at a
    128-step commit cannot leave 65 steps never-green.
  - **Why it cannot self-correct.** `knowledge/_gen_chain.py:280` is `VERDICT_SHA = "18c7789"`, with
    its own defence at `:277–279`: *"⚠ This SHA is typed, and that is deliberate: it names a fixed
    historical event, **so it cannot go stale the way a COUNT does**."* True of the *event* — and the
    published sentence is not the event, it is the CONCLUSION *"no later green verdict exists"*, which
    is exactly the kind of claim that ages. **Nothing re-checks it.** The `--selftest` bites around it
    assert the counts are AST-derived and that the marker does not leak; none asserts the anchor is
    still the latest.
  - **Three published surfaces, one constant.** `_gen_chain.py` (the chain banner + `GOOD-MORNING.md`
    via the `{{BUILD_VERDICT}}` splice at `_capture_gate.py:1637–1645`); `_gen_schematic.py:354–360`,
    which imports the same constant; and the rendered page —
    `reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html:143`: *"steps the last green verdict actually covered
    — 75 of 128 — 53 steps have NEVER been in a green verdict (#62 …)"*.
  - The class is `s125-D1`'s own: *"a claim that was true when written, went false, and nothing
    re-checks it"* [[no-gate-parses-the-artefact]]. `s125-D1` generated the two COUNTS and left the
    ANCHOR typed; this is the same defect one level up. *Stale twice ⇒ generate, never re-stamp*
    (`_CHAIN.md`).
- PREVALENCE: **1 constant · 2 generators · 3 published surfaces · every cold read, every session.**
  The falsifying receipt is **6 sessions old** and lives in `_GM-ARCHIVE.md` — retrieval surface,
  where no cold session will meet it [[read-chain-is-where-staleness-is-free]].
- PROPOSED: one of the three `s129-D5` triages, Dave's pick, and I recommend **(a)**.
  **(a) Generate it** — derive the anchor from the newest commit with a recorded green verdict rather
  than typing it, or, if no such record is machine-readable, **(b) stamp it with an expiry** — have
  `build_verdict_line()` refuse (the module's existing UNMEASURED posture, which is already written
  and tested) once the anchor is older than N sessions, rather than restating a superseded figure.
  **(c)** at minimum, re-point `VERDICT_SHA` to `adb5130` and carry the `126/128` reading, which is a
  one-line change but leaves the class open. ⛔ Not proposed: changing `s125-D1`, changing what the
  counts measure, or running `_build_all.py` (the chain forbids partial runs and the sandbox cannot
  complete one).
- status: floated

---

### P4 — `s223-D3` ruled that the version-naming ruling is **not** the ratification — *"His fresh word for v1.0.2 itself is NOT this entry"* — and v1.0.3's ratify gate is keyed to exactly such an entry: the store now derives **"RATIFIED … satisfied by the store, not by prose"** from a #224 ruling made **the day before** Dave's word, while the word itself survives only as a Python comment

- EVIDENCE:
  - **The rule.** `knowledge/_rulings.json` § `s223-D3` (Dave, 2026-08-28), verbatim: *"Dave rules the
    fix: each cut requires his fresh word — a ruling naming this cut's version in the store — before
    the manifest may read RATIFIED. **His fresh word for v1.0.2 itself is NOT this entry**; it is
    given only after his eye on the release page."*
  - **How v1.0.2 satisfied it — two rulings, not one.** `s223-D2` named the version; `s223-D7` was the
    word, and its evidence field says so: *"chat #223 2026-08-28 — Dave selected **'Bake it — word
    given'** after the release page and receipt."*
  - **How v1.0.3 satisfies it — one ruling, and it is the naming one.**
    `knowledge/_release/_gen_pack_manifest.py:612`: `"v1.0.3": "s224-D1",`. `s224-D1` is the #224
    tier-1 port-back ruling; its evidence is *"chat #224 2026-08-29 — Dave: 'as you recommend, would
    this be 1.03?' then 'yes' on the `s224-D1` read-back."* **There is no `s225-D*` anything** — the
    store's newest id is `s224-D2` (276 entries).
  - **Where his actual ratify word lives.** Only in `_gen_pack_manifest.py:612–615`, as a code
    comment: *"#225, Dave's word 'Ratify — bake it' (2026-08-29), given at the opener"* — corroborated
    by the #225 transcript's closing report (*"v1.0.3 ratified → baked → checked → ledger cut"*), which
    is the Shape-A ceiling tier, not a receipt.
  - **What the machine now publishes.** `ratification_status()` (`:626–643`) checks only that the
    keyed id exists with `status == "ruled"`. `knowledge/_release/_pack_manifest.json` therefore reads
    *"status": "**RATIFIED — s224-D1 names v1.0.3 in the store; s219-D4(2) satisfied by the store, not
    by prose**"*. The satisfaction is in fact **prose plus a hand-typed key**; `s219-D4(2)` is
    *"release = his word"*, and his word is the one thing the store does not hold.
  - ✅ **What did NOT go wrong, said plainly.** The gate HELD: `git log -S '"v1.0.3": "s224-D1"'` →
    the key entered at `1e028a1` (#225, *after* the word), while `git log -S 's224-D1' --
    knowledge/_rulings.json` → the ruling entered at `333deee` (#224). The #224 wrap explicitly
    recorded `status PROPOSED — no ruling is keyed to v1.0.3 yet`. Dave really did ratify; the defect
    is **that the store cannot show it**, and the ordering guarantee now rests on whoever types the
    key rather than on the record.
- PREVALENCE: **1 of 3 keyed versions** (`v1.0.0`→`s219-D10` and `v1.0.2`→`s223-D7` are both genuine
  ratify rulings with the word in their evidence; `v1.0.3`→`s224-D1` is not). Thin as a count,
  load-bearing as a subject — it governs what ships to designers.
- PROPOSED: two smallest steps, separable and both Dave's. **(a)** Inscribe his #225 word as its own
  entry via `_inscribe_ruling.py` (the only legal writer) and re-key `RATIFY_IDS["v1.0.3"]` to it —
  one store row, one line, the `s223-D2`/`s223-D7` shape that already worked. **(b)** The re-checker:
  one arm in `ratification_status()` that refuses when the keyed ruling's own `evidence` names an
  earlier session than the cut it ratifies — the ordering `s223-D3` exists to guarantee, asserted
  instead of assumed. ⛔ Not proposed: unbaking, re-cutting, or changing the v1.0.3 zip; nothing about
  the release is wrong, only its provenance.
- status: floated

---

## Checked-clear this pass — for the next pass, do not re-open

- **(gg1) Pass 9's P6 is CLOSED and the closure is visible.** `s217-D1` is committed —
  `git log -S 's217-D1' -- knowledge/_rulings.json` names `540f2cd` (#217), `61302a3` (#218) and
  `d0a5551` (#220); the working tree no longer carries `knowledge/_rulings.json` at all, and the store
  stands at 276 entries. The uncommitted-ruling window pass 9 found open is shut.
- **(gg2) The dirty tree is DECLARED and I neither cleaned, staged nor reverted any of it.** Exactly
  the four modified paths the dispatch named: `knowledge/_probe/session-225.json`,
  `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`,
  `notes/_dream/_MEMORY-GRADES.json`. The instrumentation appends among them remain **pass 6's P2,
  still floated** — referenced, not re-floated. ⛔ I did not touch `.git/index.lock`; every `git`
  call from the sandbox printed `unable to unlink … Operation not permitted`, the known wart
  [[git-lock-mv-not-rm]], and I left it alone.
- **(gg3) I hunted for orphaned instruments and the register already owns them all.**
  `python3 knowledge/_validate_wiring.py` → *"50 gate script(s) on disk · 48 wired · 2 exempt by name ·
  0 failure(s)"*, naming `_gate_pack_imports.py` and `_validate_descender_computed.py` as declared
  exemptions and `_gate_harness_stubs.py` as a verified arm. `_gate_doc_rows.py` looked orphaned on a
  first sweep (absent from `_build_all.py` and `gates.yml`) and is not: it is wired at the commit seam,
  `knowledge/_git_commit.sh:282` and `:604`. Driven: *"population 153 · unrowed 0 · ✅ PASS"* — the
  #185 forgotten-document class is green today.
- **(gg4) The pre-flight `⛔ NOT CAPTURED` streak is pass 9's P1, still floated — referenced, not
  re-floated.** `notes/_GAUGE-LOG.md:2401` (#223) reads *"twenty-fifth consecutive"*; 105 of the file's
  `pre-flight #` blocks now carry the refusal. New only as corroboration: the hand-typed ordinal has
  now **skipped a number** — `:2309` (#219) says *"twenty consecutive"*, `:2331` (#220) says
  *"twenty-second consecutive"*. Same ordinal class already named at passes 5, 7 and 9; not a
  proposal.
- **(gg5) The AGING half's SECOND cycle has landed, and it is the evidence pass 9's P3 asked for —
  reported, not re-floated.** `notes/_dream/_MEMORY-GRADES.json` after this pass's conductor-run
  refresh: **FRESH 63 · AGING 33 · STALE 0 · UNPROVABLE 26** over **122** hooks, against pass 9's
  *FRESH 78 · AGING 16 · STALE 0 · UNPROVABLE 25* over 119. AGING has gone **1 → 16 → 33** in three
  cycles. P3's caveat holds and is now measured twice: `age_days` is
  `(now - os.path.getmtime(hook_file)) / 86400` (`knowledge/_gardener.py:940`), so this is a decay
  curve of **file edit recency**, not of claim truth. ⚠ Also worth Dave's eye at the B3 review, and
  NOT floated as a proposal because it is the review's own subject: `ALERT_LIST_GRADES = ("STALE",)`
  (`_gardener.py:154`) is the only arm that names a hook, and STALE has been **0 in all three
  cycles** — the alert has never once listed anything.
- **(gg6) I measured the `provenance:` field-line convention and I am NOT floating it — the gate's
  glob is narrower than the class, and per [[gate-glob-scope-rule]] the rule may not be wider.** Of
  257 dated documents under `notes/`, `notes/_briefs/`, `notes/_receipts/`, `notes/_subreports/` and
  `_DECISION-HISTORY/` since 2026-08-15, **51** carry a `provenance:` line and **5** carry a session
  id. But `_capture_gate.py:1111` globs `notes/*.md` and `_DECISION-HISTORY/*.md` only, and the
  sub-report skeleton deliberately prescribes a different header (`session: #NNN` + `brief:` +
  `tokens:`). The subdirectories are honestly ungated, exactly as A-D4 reasoned about `_dream/`.
  Declared thin, dropped.
- **(gg7) #225 is UNTITLED in the session list, and I am recording it as ground truth rather than
  floating it.** `list_sessions` returns it as **"Good morning"**, while `_CHAIN.md:22` says
  *"**YOU ARE #225. TITLE THIS CHAT →** `Apollo - #225: ratify and bake v1.0.3`"* and the line's own
  parenthetical calls the chat half *"ungateable"*. The cost was real and it was mine: #225 is the
  session that ratified and baked v1.0.3, and I identified it only by reading it. Not floated —
  the remedy is a keystroke of Dave's, not a reversible repo step. ⚠ Related and also not a finding:
  **#225 has not wrapped.** It is PAUSED with three decisions on Dave's desk (chain-ratio remedy,
  the Gumdrop version story, the push), which is the #217 precedent at pass 9's P6 — *paused, not
  lapsed* — and the six unpushed commits are his call, not drift.
- **(gg8) What this pass wrote, stated plainly. ONE file — this one.** The dispatch had the conductor
  run the B3 refresh arm before I was dispatched (`"refreshed_at": "2026-08-30T07:12:03"`, and the
  grade-decision row is his), so ee6's tension is resolved mechanically and there is none left to
  declare. I logged **no** `--grade-decision` rows, ran **no** `_gardener.py` arm, ran **no**
  `_checkin.py` (it appends to the counted dataset), and performed **no** git operation of any kind —
  no add, no commit, no push, no checkout, no clean. Every `git` command I ran was read-only
  (`log`, `status`, `show`, `diff --stat`). No memory file, no canon, no ledger.
- **(gg9) Out of scope by standing exclusion, and where I drew the line.** Dream-lane mechanics remain
  barred (cc6/dd7/ee7/ff7): I did **not** float the cadence, the conductor sequence, the lane's §🔀
  row, or `_dream/` gating. ⚠ **P1 and P2 sit nearest that line and I judge them clear of it:** their
  subject is `s218-D7`, the *sub-report* contract that governs every delegated lane in the project,
  and `_capture_gate.py`, which is the capture ritual's gate — neither is the dream lane. ⚠ **gg5's
  second half reports on the B3 review's own subject** and is therefore filed here as an observation
  for Dave's sitting, not as a proposal.

---

## Method

**Read, in the dreamer spec's order.** `MEMORY.md` (index, hooks only — 122 entries at this pass's
count) · `GOOD-MORNING.md` header, ★ LATEST banner and the `residual → #225` line ·
`_LIVE-STATE.md` header and refresh line · `_CHAIN.md` (the header, the STATE block, and the
81,536-character residual line sliced by character range — Read cannot open it, so it was read via
`python3` slicing) · `.claude/agents/dreamer.md` in full · `notes/_MEMENTO-DECISIONS.md` heading and
RULED spine (the file is 544KB / 6,106 lines; Read refuses it whole) · **every prior proposals file's
checked-clear list and every prior `### P<n>` heading** (pass 3's prose block, (q)–(w), (x)–(bb),
(cc1)–(cc6), (dd1)–(dd7), (ee1)–(ee7), (ff1)–(ff7)), so floated-but-unruled proposals could be
referenced rather than re-floated · `notes/_subreports/_TEMPLATE.md` in full ·
`knowledge/_RUNBOOK-capture-ritual.md` § filed sub-reports.

**Transcripts: 15 in the window, 14 read, 1 skipped-and-declared.** Shape A, `list_sessions` →
`read_transcript`, covering #225 back to #214 plus the two #218 worker windows and pass 9's own lane
session. Five read in detail (#225, #224, #223, #222, #221), the rest by title and closing report.
⛔ **Skipped and declared:** `local_9f1a0cfa` *"Memento dream pass"* — pass 9's own session; reading a
dream pass to write a dream pass is circular, and its output is the file I read instead.
**Fidelity ceiling, and where it bound:** tool calls appear as names only, with no arguments or
results, so **not one figure in this file comes from a transcript**. Transcripts located claims;
every number was re-derived against the repo. Where it bit hardest: **#225 is untitled** (gg7), so the
window's most consequential session had to be identified by reading it rather than by its label; and
Dave's v1.0.3 ratify word (P4) is visible to me only at transcript tier, which is precisely why its
absence from the store matters.

**Live-tree check before measuring:** `git log --oneline -1` → `48df9c6`, matching the dispatch;
`git status --porcelain` → 4 ` M` lines, the declared baseline, unchanged at close.

**Commands a conductor can re-run, verbatim** (all read-only; nothing below writes):
- `python3 -c "import sys;sys.path.insert(0,'knowledge');import _gen_chain as gc;print(gc.build_verdict_line());print(gc.VERDICT_SHA, gc.build_steps_at('e645df2'), gc.build_steps_now())"`
  → the `75 of 140` sentence · `18c7789` · `(128, 128, None)` · `(140, 140, None)`
- `sed -n '123p' _GM-ARCHIVE.md | grep -o '126/128[^*]*'` → the #218 artefact correction
- `sed -n '32p' notes/_briefs/2026-08-22-215-wrap-brief.md` → `CI: #413 GREEN on e645df2`
- `sed -n '280p' knowledge/_gen_chain.py` → `VERDICT_SHA = "18c7789"`; `sed -n '354,360p' knowledge/_gen_schematic.py` → the second consumer
- `python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as c;print(c._last_wrap_commit('.'));print(c._changed_since('.', c._last_wrap_commit('.')[0], 'notes/_subreports'))"`
  → `('48df9c67…', 'after #225 … Gumdrop arm 5 …')` and `[]`
- `sed -n '4657p' knowledge/_capture_gate.py` → `WRAP_COMMIT_SUBJECT_RE = re.compile(r"^after\s+#\d+\b")`; `sed -n '138,139p' knowledge/_git_commit.sh` → the two documented shapes
- `git log -n 150 --format='%s' | grep -c '^after #'` → `129`; `git log -n 150 --format='%s' | grep '^after #' | grep -ci wrap` → `11`
- the three-regex sweep over `notes/_subreports/*.md` (imports `SUBREPORT_COUNTS_RE` /
  `SUBREPORT_REPLAY_RE` / `SUBREPORT_QUESTIONS_RE` from `_capture_gate` and applies them to all 64
  filed reports) → `COUNTS 28 · REPLAY 21 · QUESTIONS 26`; restricted to basenames `>= 2026-08-28`
  (n=15) → `3 · 3 · 4`
- `sed -n '490p;575p' notes/_subreports/2026-08-29-225-ci-reds-forensics.md` · `sed -n '7p' notes/_subreports/2026-08-29-225-gumdrop-gate-widening.md` → the heading form and the slash form
- `git log --oneline -S '"v1.0.3": "s224-D1"' -- knowledge/_release/_gen_pack_manifest.py` → `1e028a1`;
  `git log --oneline -S 's224-D1' -- knowledge/_rulings.json` → `333deee`
- `python3 -c "import json;d=json.load(open('knowledge/_release/_pack_manifest.json'));print(d['status'])"` → the `RATIFIED — s224-D1 …` string
- `python3 knowledge/_validate_wiring.py` · `python3 knowledge/_gate_doc_rows.py` → both green, quoted at gg3
- `python3 -c "import json;print(json.load(open('notes/_dream/_MEMORY-GRADES.json'))['counts'])"` → `{'FRESH': 63, 'AGING': 33, 'STALE': 0, 'UNPROVABLE': 26}`

**Nothing here self-promotes.** Four proposals, all `status: floated`; promotion is Dave's alone.
