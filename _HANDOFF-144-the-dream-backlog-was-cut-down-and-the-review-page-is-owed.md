# HANDOFF #144 — #293 → #294 — THE DREAM BACKLOG WAS CUT DOWN AND THE REVIEW PAGE IS OWED

provenance: 293 · 2026-09-21
status: observed

*Written by the delegated OPUS 5 wrap sub at the close of #293 (conductor Fable 5.1). Every figure
here was MEASURED at this seat unless it says otherwise; where a measurement disagrees with the
brief's declaration, both readings are published and neither is rewritten.*

✅ **NO DATE SPLIT.** The session opened Monday **2026-09-21**; all four lanes ran that day and **all
three commits carry it** — `03605215` · `c0e9242e` · this wrap's own. `date` at this seat read
`Mon Sep 21 15:00:44 BST 2026`. **No DATE-SPLIT line was added to `GOOD-MORNING.md`'s header** (#292's
own ritual ran earlier the same day), and the five that stand were not touched. ⛔ #241's
ruling-shaped question — what a midnight-spanning wrap should stamp — is untouched and still Dave's,
now at **age 52**.

⛔★★ **NO RULING WAS INSCRIBED. `knowledge/_rulings.json` STAYS AT 622** — verified here by
`json.load` over the `rulings` list, **id and count only, never a printed record**, with **no `s293-`
id present**, the newest three still reading `s283-D1` · `s287-D1` · `s287-D2`. **He did not say
*"inscribe"* today.** Everything ruling-shaped below is a **QUESTION PUT** (`s271-D4`), never a state
of the world.

---

## ⛔ READ FIRST, IN THIS ORDER

1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.
2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta). **11,669 tape**
   (slice 10,817 + the generator's 852 wrapper). ⚠ Inside the `s214-D6` ~10–12K target, **up 1,955
   on #292's 9,714 — and the BANNER slice went DOWN (5,133 against 5,301), so the growth is all in
   the ⏱ delta**, which `s241-D2` makes the sole home for gauge, declared-skip and correction
   detail. This wrap published four corrections in full rather than smoothing any of them.
3. ⛔ **It does NOT replace `_HANDOFF-130`…`-143`.** Every open item on those fourteen still stands
   **except ONE struck here with a receipt** — see § THE ONE STRIKE.
4. `notes/_lanes/293/DAVE-RULINGS-2026-09-21.md` — his four entries, verbatim, in order, with what
   was done on each. **Quote them; never paraphrase.**
5. `_CARRIES.md` § `residual → #294` when you need the bodies — **627 probeable items**. Do not read
   it at boot; fetch the section (`_memento_search.py` → `--fetch carries:residual-294`).

---

## ⛔⛔ DAVE'S WORDS — FOUR ENTRIES VERBATIM, AND THE FOURTH IS ONE WORD

> Good Morning! we should probably look at the latest dream pass, in fact some previous ones may not have been enacted

> okay lets get these cut these down, I don't like all these loose ends, lets get the no-brainers done first. Give me a plan to get this of our desk. then wen they are cut down lets get a new review page with anything that needs mu judgement on it excluding anything settled

> go

> wrap

*(Mid-session, and it is not a ruling: he asked* **"activity seems to have stopped?"** *while lane E1
ran long. It was answered in chat and nothing followed from it.)*

⚠ **A FIFTH ASK — the Jev research that became lane J — IS ON THE RECORD WITHOUT A QUOTATION, because none is reachable from this seat.** The wrap brief did not carry it; the identification is the conductor's own memory note (§ THINGS A COLD SEAT SHOULD KNOW), which is a paraphrase and is quoted as one. **#294 should recover his verbatim line into `notes/_lanes/293/DAVE-RULINGS-2026-09-21.md`.**

**Read:** entry 2 carries an **ordering constraint** — no-brainers first, *then* a review page, and
the page excludes anything settled. Running them together produces exactly the surface he was
complaining about. Entry 4 is the whole of his reply to a seam reading outside tolerance.

---

## WHAT LANDED — TWO COMMITS BEFORE THIS WRAP'S, ALL 2026-09-21

| sha | what |
|---|---|
| `03605215` | **lane E1** — the dream lane's backlog enacted, eight items, each with a selftest that can fail |
| `c0e9242e` | **this ritual's step-0 commit** — lane DA's audit, his rulings file, the `W-293da` doc row, `_CHAIN.md` regenerated |

⚠ **AND THE WRAP COMMIT CARRIES LANE J's TWO FILES AND LANE J2's THREE**, identified mid-ritual — see § THINGS A COLD SEAT SHOULD KNOW.

⛔ **NOTHING IS PUSHED.** `git ls-remote` was not consulted for a comparison because there is nothing
to compare: **the push verdict is *"not pushed — conductor's judgement"***, by the brief's own
instruction, and **no CI run exists on any of the three shas.** None is claimed.

**1 — THE AUDIT: 39 PROPOSALS, AND MOST OF THEM WERE ALREADY DONE.** Lane **DA** (Opus, depth 1,
READ-ONLY on git, and deliberately NOT running `_checkin.py` because that arm appends to two counted
datasets and an audit must not move the population it audits) searched four ruling surfaces — all 622
records in `knowledge/_rulings.json` by field extraction, `notes/_MEMENTO-DECISIONS.md`, every
`notes/_lanes/*/DAVE-RULINGS-*.md`, `_DECISION-HISTORY/*dream*` — with one liveness probe per
proposal. **22 ruled+enacted · 1 RULED-AND-NOT-ENACTED · 13 never ruled and still live · 3
overtaken.**
★ **AND IT CORRECTED THE BRIEF'S PREMISE FROM PRIMARY SOURCES.** Each proposals file states its own
number in its first line: `2026-08-09` is **pass 6**; `2026-08-08` calls itself the *"Fifth pass"*.
**Published mapping: 08-08 = 5 · 08-09 = 6 · 08-15 = 7 · 08-16 = 8 · 08-23 = 9 · 08-30 = 10 · 09-06 =
11 · 09-13 = 12 · 09-20 = 13.** An audit that inherits a wrong index produces a confident, wrong
census, so this is the finding the rest of it rests on.
⬛ **THE LARGEST GAP: PASS 9 WAS NEVER PUT TO DAVE AT ALL** — six proposals, no disposition ruling in
any of the four surfaces, three still live at 29 days. Previously unwritten anywhere.
Deliverable: `notes/_lanes/293/DA/dream-enactment-audit.html`.

**2 — THE ENACTMENT: 8 OF 8, 0 BLOCKED, NO CONSTANT MOVED.** Lane **E1** (Opus, depth 1), commit
`03605215`: the lane-ownership guard OFF under `s276-D6` (**moved**, never `rm`'d) with its sibling
orphan exempted by name, taking `_validate_wiring.py` from **2 failures to 0** · a staleness/void
fence on the B3 grades sidecar, both clauses tripping independently, the row still logged as
`"kind": "alert-void"` so the B3 return can count it but cannot mistake it for a measurement ·
`_state.py`'s `ID_RE` widened, selftest **57 → 66** bites · the memento indexer **DECLARING** id
collisions instead of silently suffixing, firing **6** times on the real corpus against the 4 the
pass named · the `8,470` boot-floor term annotated BY ADDITION with the re-measure parked as
`P-293-1` · *"exact"* dropped from the `size:` stamp · ★ **the `s186-D2` #119-sweep re-checker BUILT
after 36 days** and wired into `_capture_gate.run()` · and the pre-flight generator.
⛔ `STOP_LINE_TK`, `BOOT_CEILING_TK`, `BUDGET_HARD` and the `8,470` term are **byte-unchanged**.

**3 — THERE WAS NEVER A GENERATOR FOR THE PRE-FLIGHT LINE, AND THAT IS THE SESSION'S SHARPEST
RESULT.** Every `⛔ NOT CAPTURED` in `notes/_GAUGE-LOG.md` was **hand-typed** into a
`knowledge/_tmp/wrap<n>/stratum*.py`, each copying the last with the ordinal bumped — the literal
phrase is *"Reason unchanged from #199…#<n-1>"* — for **93 consecutive sessions, #199 → #291, 185
occurrences.** The stated reason (*"a sub cannot read its own `message.usage`"*) was **answering a
question nobody asked**: the line wants the CONDUCTOR'S window, readable from a sub seat all along,
and several of those strata say `_checkin.py` WAS run on it *in the paragraph that refuses*.
✅ **The arm ran at this wrap and returned a CAPTURED measurement** — `python3
knowledge/_checkin.py --preflight-line 293`, which appends to no log (both counted datasets
byte-identical across the call, by construction) — published verbatim in the #293 stratum.
⛔★★ **AND THE STAMP IS STILL A REFUSAL, WHICH IS THE HONEST OUTCOME AND A FINDING THIS WRAP OWES
#294 BY NAME.** `preflight_line()` returns **the SPEND** (the conductor's FILL at the call);
`GOOD-MORNING.md`'s pre-flight stamp, by `_capture_gate.check_preflight`, wants **the PRICE**
(`boot N + job N est + wrap N est = N of 200,000 — BAND`, Dave #56). **Two different objects**, so
the generated line is neither the absolute form nor a legal refusal and **pasting it into GM takes
the wrap RED** — measured here, at the first wrap to use the arm. ⇒ **The GM stamp is the #73 legal
refusal with a cause that is TRUE of #293 — *the session was never priced at its opener, so there
is no estimate for the stamp to carry* — a different sentence from the 93-session copy, whose
stated cause was false.** ⬛ **Whether the stamp's form widens to admit a measured CAPTURED line, or
`--preflight-line` grows a second emitter for the priced form, is ruling-shaped and HIS.** A wrap
does not change a gate's contract to make its own commit green.

**4 — THE MEMORY CEILING IS DISCHARGED BY A SHARD AND A STANDING RULE.** Done **in the conductor's
seat**, because only that seat can reach the store (#278). `MEMORY-ARCHIVE-2.md` opened at **35,063
B**; the **#283 → #289 wrap lines** and the **#286–#291 suspension notes** moved **VERBATIM**;
`index.md` rewritten to the newest three (#292 · #291 · #290) and now **15,605 B of 49,152**; the
frontmatter `description` corrected — the one #292 recorded as wrong and uncorrectable at zero
headroom; and the rule inscribed in the index: ★ **open the next shard, never truncate, never
suspend.** `MEMORY-ARCHIVE.md` untouched at **48,990 B**.

---

## ⛔ FOUR LANES — TWO VERIFIED, TWO NOT

DA · E1 · **J** · **J2**. ✅ **Verified at this seat rather than taken on trust:** DA's and E1's sub-transcripts
carry `"model":"opus"`, `"spawnDepth":1` and `"agentType":"general-purpose"` in their own
`.meta.json`, and so does this wrap sub's. ⛔ **LANES J AND J2 HAVE NO TRANSCRIPT AND NO `.meta.json` IN THIS
SESSION's `subagents/` DIRECTORY, so their model, their depth and their token cost are UNVERIFIED AT
THIS SEAT AND ARE NOT ESTIMATED.** ⚠ **A THIRD LANE — J — ALSO RAN AND HAS NO TRANSCRIPT IN THIS SESSION's `subagents/` DIRECTORY**, which is how it was first mis-read as a stray; it is identified, committed and corrected at § THINGS A COLD SEAT SHOULD KNOW.

⛔ **The delegation rule `s204-D1` was obeyed.** Move 2 was done in seat and that is a **SEAT LIMIT,
not a departure**: a sub cannot reach the memory store at all. **The sentence that rules `s204-D1` is
STILL uninscribed**, for a fifth consecutive session of obedience.

---

## ★★★ THE INSTRUMENT WAS OBEYED, NOT OVERRIDDEN — AND THE n DOES NOT MOVE

At **FILL 222,464 real / 22 turns** the seam check read **OUTSIDE the 220,000 tolerance**. It was
quoted to him with the wrap recommended over a third override. **His reply, verbatim and entire:
*"wrap"*.**

⇒ **#283, #290 and #293 stopped ON the instrument. #291 and #292 each overrode it exactly once with a
note and then obeyed.** ⛔ **`s283-D1`'s override shape STAYS AT n=2. This session adds nothing to it
and no rule is invented from it here.** The cost is real and is carried rather than minimised: **the
review page he asked for in the same breath as the no-brainers was one lane away and is not built.**

---

## ⚙ THE NUMBERS, MEASURED AT THIS SEAT

**The conductor's window** — `_checkin.read_fill` **imported rather than re-implemented**, against
`.claude/projects/session/a691e928-52e5-4d5e-89c2-09ffedcd0387.jsonl`, the session's TOP-LEVEL
transcript (the three subs being `subagents/agent-*.jsonl` beneath it):

> **FILL 224,335 real / 24 turns · peak 224,335 · boot 74,204 · 0 compaction records · 0 drops**

✅ **EVERY ONE of the conductor's four declared seam readings reproduces EXACTLY at this seat — zero
difference on all four:** `153,108 / 10` · `156,242 / 12` · `172,905 / 19` · `222,464 / 22`.

> **wrap-handover: brief-cut 222,464 · sub-cut 224,335 · delta 1,871 · replay unobservable
> (conductor-side, post-wrap)**

✅ The subtraction is **legal**: both terms read the same window, and the four agreements to the token
are the identification. **1,871 is the second-smallest hand-over on record**, after #292's 954.

⛔ **4,335 past the 220,000 tolerance and 44,335 past the 180,000 quality line — BOTH DECLARED. The
256,000 hard figure is CLEAR by 31,665 and no literal was moved.**

**`subs`** — **MEASURED 398,836 (n=2, of FOUR lanes that ran)** against **NO DECLARATION**: DA **169,242** · E1 **229,594**; ⛔ **lanes J and J2 are UNMEASURABLE here — no transcript exists at this seat for either — and the gap is declared, never filled with a guess.**
⛔ **The conductor declared no sub figure for #293, so nothing is reconciled and the absence is
STATED rather than defaulted to a zero.** ⚠ This wrap sub's own window is excluded — a seat cannot
read its own final price — the same exclusion #292's n=9 made, so the figures are comparable.

**Boot 74,204** is over `BOOT_CEILING_TK` 70,000 — **SHRINK-ONLY, cut the boot, never raise the
literal.** **34 tokens above #292's 74,170**; the last six readings spread fifty-three tokens.

---

## ⛔ THE GATES — SEVEN IN, SEVEN OUT, ALL INHERITED

The step-0 commit's gate read **EIGHT**. ⚠ **The eighth was NOT inherited: the retrieval index was
STALE, which is step 2g's job and this ritual's own to close.** It was closed, and the
seven-inherited figure is published beside the eight rather than in place of it.

Every one of the seven is another session's append-only testimony in `notes/_GAUGE-LOG.md`: the
**boot-drift CEILING BREACH** and **six boot double-counts** (#243 ×5, #264, #272, #273, #274, #287).
⛔ **A wrap may not repair an inherited gate fail.** Both of this ritual's commits take the `#243`
DECLARED NOT-A-WRAP path — **the NINETEENTH consecutive wrap.**

✅ **NEW: the `s186-D2` #119-sweep re-checker fired inside `_capture_gate.run()` for the first time**
and returned *"21 frozen 'UNPROVEN by this sweep' status string(s) — unchanged. Counted, never
rewritten; refuses only on growth."*

⛔★★ **AND A DECLARED HOLE, CARRIED FROM LANE E1 VERBATIM RATHER THAN RE-RUN:
`python3 knowledge/_capture_gate.py --selftest` EXCEEDED THE SANDBOX CALL WALL AT 165 s AT THAT SEAT
AND IS UNASKED THERE** — in the session that changed the file. This wrap ran the gate **live** through
`_git_commit.sh`, but **a live arm firing is not the selftest passing**, and the first surface that
will ask it honestly is CI — which is gated behind the unpushed commits.

---

## ✅ THE COMMIT PATH — ONE REFUSAL, AND IT WAS THE RIGHT ONE

⛔ **This ritual opened with lane DA's work uncommitted, so it made a commit of its own BEFORE the
wrap commit — `c0e9242e`, runbook step 0.** Every dirty path was named and staged explicitly,
including the three machine appends `knowledge/_graph-mark-observations.jsonl`,
`notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl`.

✅ **THE DOC-ROW GATE WAS ANTICIPATED RATHER THAN MET, A SECOND SESSION RUNNING:** `W-293da` was
minted through `_state.add()` and `_CHAIN.md` regenerated **before** the first commit attempt, so it
passed post-staging on the first run — against #289's, #290's and #291's three-refusal runs.

⚠ **ONE REFUSAL WAS PAID AND IT WAS NOT THAT GATE: `s130-D3` refused a non-wrap commit with no
`SESSION_N`** — *"a subject is generated from a current-session source or not at all; a stale on-disk
banner is never inherited"* — and **nothing was staged by the refused run**. Re-run as
`SESSION_N=293`, exit 0. **Write this down: a mid-session commit needs `SESSION_N=<n>`.**

⛔★★ **A STALE `.git/index.lock` WAS FOUND AT THE OPEN** (0 bytes, 14:56, stranded by lane E1's
commit) **AND WAS `mv`'d ASIDE, NEVER `rm`'d** [[git-lock-mv-not-rm]] — to
`/sessions/keen-wizardly-maxwell/stale-index.lock-293-wrap`, outside the repo. The per-session delete
grant was active and was never needed. **No lock was stranded at this seat.**

---

## THE ONE STRIKE, AND WHAT WAS DELIBERATELY NOT STRUCK

✅ **STRUCK — #292's OWED ITEM 12, *"INDEX SHARDING (his pick, not started) and the memory archive's
162 B — now joined by `index.md` at ZERO"*** (`s183-D1` strike form, `s188-D2` receipt).
**Receipt: the conductor-seat acts of Move 2** — `MEMORY-ARCHIVE-2.md` at 35,063 B, the #283→#289
lines and the #286–#291 notes moved VERBATIM, `index.md` at **15,605 B of 49,152**, the description
corrected, the standing rule inscribed. **The session that proved the claim false is #293 and the
correction is inscribed in the store itself**, mirrored into the repo at the ⏱ LATEST DELTA, the ★
LATEST banner ④ and `_CARRIES.md` § `residual → #294` ⑥.
⚠ **THE FORM WAS CHECKED BEFORE THE STRIKE, NOT AFTER IT, AND THE READING IS PUBLISHED:** `s188-D2`
asks for **a locatable inscription**, not specifically for a commit sha, and the **seat limit here is
structural** (#278 — only the conductor can write that store), so requiring a sha would make anything
memory-side **permanently unstrikable**. ⇒ **A conductor-seat act IS a receipt under that form in
this case.** Whether it is in general is ruling-shaped and is carried as a question.

⛔ **NOT STRUCK — #292's OWED ITEM 13, *"DREAM PASS 13's SEVEN PROPOSALS, still unruled
(`dcf17ade`)"*, AND THE PRECISION IS THE POINT.** Six of the seven were **ENACTED** by lane E1 — P1,
P2, P3 (weak form), P4, P6, P7 — and the seventh, **P3's strong form, is carried to the review page**.
⛔ **NOT ONE OF THEM WAS RULED.** `s183-D1` strikes a **headline** and never a clause; the headline
says *still unruled*, which is true of all seven. They were enacted as **no-brainers** on his *"lets
get the no-brainers done first"* — an instruction to clear a backlog, not a ruling on seven
proposals. *"A strike that is wrong is worse than an item that is merely stale"* (`s271-D4`).

⛔ **NOTHING ELSE WAS STRUCK.**

---

## ⛔★★ THE BANNER CAP CLOSED AT ZERO HEADROOM — A FIRST

The ★ LATEST banner was drafted at **1,252 tape** and shortened **ELEVEN** times to land at **EXACTLY
1,200 of the `s241-D2` cap of 1,200, over 9 of 10 substantive lines — ZERO tokens of headroom**,
against #292's two. Eleven ruling-shaped carries are represented on it by five bullets, by the same
merging #292 resorted to for ten.

⇒ **#292's complaint is not withdrawn and is now literal: the cap has stopped constraining girth and
started shaping the record, and the next wrap in this idiom has no room at all.** Reported, not
appealed — **the cap is Dave's.** [[gate-inside-the-growth-loop]]

---

## ⬛ OWED TO #294, IN ORDER

1. ⛔★★ **MOVE 3 — THE JUDGEMENT-ONLY REVIEW PAGE. HIS WORDS, AND IT IS THE FIRST JOB.** Each item
   with **a recommendation and a one-word rule**; it **REPLACES `notes/_lanes/293/DA/dream-enactment-audit.html`
   as the ruling surface** (the audit is the evidence, the page is where he rules); **everything
   settled is excluded**. The five: **(a) pass 10's three unruled findings** — on a digest page since
   #226, never raised again, all three live, and P3 has DRIFTED (`build_verdict_line()` now reads
   *"75 of 144 steps green … 69 have NEVER been in a green verdict"*) — ⚠ **`s125-D1`'s `watch` field
   forbids the obvious hand-fix BY NAME.** **(b) the B3 grader: re-point it at the store's new home
   first, or run the review on the data that exists?** Both returns are overdue and the instrument is
   dead (`_gardener.py --refresh --dry-run` → `⛔ GARDENER BLOCKED … REFUSING TO GUESS`). **(c) pass
   9's staleness constant** `GRADE_AGING_DAYS = 30`, provisional, never ruled. **(d)
   generate-vs-stamp on the `size:` figure** — P3's strong form; the weak form landed. **(e) pass 6
   P4's stamped token-scope expiry, ~2026-11-06**, about six weeks out, the scope never proposed.
2. ⬛ **EVERYTHING #292 OWED THAT #293 DID NOT TOUCH**, each at its true age in `_CARRIES.md` §
   `residual → #294`: **his v12/v13 notes** (the read is DONE, the output owed, the four D2 flags and
   the dark robots slide gated on them) · **the deck's brain still at PASS SIX** (v13 inlines `YAW0
   10` / `PIT0 8` / `AOV 12` against the drawing file's `−50 / 20 / 33`) · **the workers' finessing —
   *"we'll work on that together"*, NOT a lane brief** · **the dashboard review, and WHICH cold
   brief** (unnamed to the record; the frozen demo prompt was declared NOT RECOVERABLE at #288) ·
   **lane B3's plate question** (plate to −50 as shipped, or held at the cogs' −35 with the brain
   turning 11.6° in its own axes; and does `AOV` widen past 33?) · **the two hidden-line flaws lane
   B2 named** · **lane C's runner question** (wire `_drive_chart_engine.py --check` — blocking or
   advisory?) · **lane H's two** · **lane D's nine** (chief among them whether **DP-01…29** become
   the standard) · **the deck's counter** (thirteen cards, twelve reading `NN / 12`, one `10A / 12`).
   ⛔ **FRIDAY THE 25TH IS NOW FOUR DAYS OUT, AND IT IS THE INTERNAL.**
3. ⛔ **THE PUSH, AND A CI READ-BACK JOB BY JOB.** `03605215` + `c0e9242e` + this wrap's commit are
   **LOCAL**. ⚠ **This one is not routine:** lane E1 changed `_capture_gate.py`, `_checkin.py`,
   `_state.py`, `_governs.py` and `_build_memento_index.py`, and **the capture gate's own selftest is
   UNASKED at every seat this session had** — CI is the first honest asking.
4. **LANE E1's SIX and LANE DA's NINE ruling-shaped questions**, bodies in the two filed reports and
   headlines at `_CARRIES.md` § `residual → #294` ⑧ and ⑨.
5. **LANE J's JEV BRIEF NEEDS A DECISION PUT BACK TO HIM** — researched, committed here, never returned to him; his stated constraint is **optional improvement, never a hard dependency**, and his verbatim words are **not on the record** and should be recovered. See below.

---

## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING

- ⛔★★ **A THIRD LANE — J — RAN THIS SESSION, AND THIS SEAT's FIRST READING OF IT WAS WRONG. THE CORRECTION IS PUBLISHED, NOT SMOOTHED.**
  `notes/_lanes/293/J/jev-integration-brief.html` (26,473 B) and
  `notes/_subreports/2026-09-21-293-J-jev-research.md` appeared at **15:01–15:03**, after this
  wrap's step-0 commit had staged its paths. **Not in the wrap brief · no sub transcript for a lane J
  in this session's `subagents/` directory (three exist: DA, E1, this wrap sub) · `grep -rn -i
  "jev\|typesafe"` over `notes/`, `_DECISION-HISTORY/`, `GOOD-MORNING.md` and `_CARRIES.md` returned
  nothing** — so they were first written up as a stray of *provenance not established from this seat*.
  ⛔ **THE SEARCH THAT DISPROVED IT IS THE ONE dream-11 P3(b) DOES NOT NAME: THE MEMORY STORE.**
  `/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/areas/jev-integration.md`, written
  **2026-09-21T14:10:16Z**, version `6aab740ecb06`, says in its own body: *"wants research on
  integrating Jev into the Apollo projects, driven from Cowork (2026-09-21, session #293 **lane J**;
  brief at `notes/_lanes/293/J/`)"*. ⇒ **LANE J IS #293's AND IT IS HIS ASK.** Both files are
  **committed by this wrap** with the doc row `W-293j`.
  ⬛ **STILL OWED, AND IT IS A QUESTION PUT:** the same memory line records **a Jev dependency would
  not work for anyone without the API, so it must be an OPTIONAL improvement and never a hard
  dependency**, and that **he has a TypeSafe/Jev invite and the API key *"shouldn't be a problem"***.
  **The brief has not been put back to him for a decision.** ⚠ **His Jev words are NOT available
  verbatim at this seat** — the wrap brief did not carry them and the memory line is the conductor's
  paraphrase — so `notes/_lanes/293/DAVE-RULINGS-2026-09-21.md` records the ask with its provenance
  and **invents no quotation**; **#294 should recover the verbatim line.**
  ★ **GENERAL, AND WORTH MORE THAN THE FILE: since #278 the memory store is a FOURTH provenance
  surface, reachable only from a seat that can read it, and a negative over three of four surfaces is
  not a negative.**
- ⛔★★ **A FOURTH LANE — J2 — LANDED AT 15:25–15:27, WHILE THIS RITUAL WAS CLOSING, AND IS CARRIED
  RATHER THAN LEFT.** `knowledge/_jev.py` (29,019 B), `knowledge/_jev-receipts.jsonl` (2 lines) and
  `notes/_subreports/2026-09-21-293-J2-jev-adapter.md` — **the Jev adapter, built and fired twice
  live**, in house style. Doc row `W-293j2`. ⛔ **Like lane J it has no transcript and no
  `.meta.json` at this seat.** ⛔ **Its own report names the hole in it: `_jev.py` is AN INSTRUMENT
  WITH NO CALLER** — nothing in `_build_all.py` calls it, its author says nothing should until a
  retrieval experiment runs on a known-answer fixture, **the Score rubric is UNFALSIFIED at n=2
  (it has only ever returned its top level)**, accuracy is entirely unmeasured and `html_to_state`
  is declared lossy in its own CANNOT block [[instrument-without-a-consumer]]. ✅ Both lanes' files
  were **stable at stage time** and a commit removes nothing, so carrying them was the
  non-destructive choice.
- ⚠★★ **A FIFTH LANE — J3 — WAS STILL RUNNING WHEN THIS WRAP COMMITTED AND IS DELIBERATELY LEFT
  OUT.** `notes/_lanes/293/J3/` — two fixture pages, `probe.py`, `questions-as-sent.json`,
  `probe-results.md` — written **15:35–15:36, seconds before staging**, with **no filed sub-report
  yet and no `_state.json` row**. ⛔ **IN-FLIGHT IS NOT A STRAY AND ITS ABSENCE IS NOT A DROP:**
  committing a file another worker is still writing is the **#70** defect, and a later commit loses
  nothing. **Commit it at #294's opener with a doc row, once its report exists.**
- ⛔ **`_git_commit.sh`: a MID-SESSION commit needs `SESSION_N=<n>`** — `s130-D3` refuses without it,
  and correctly. **Plus: a FRESH msgfile with a FRESH name and NO `after #N …` prefix on line 1** —
  the script adds it. ✅ Both paid at #293.
- ⛔ **MINT THE DOC ROWS AND REGENERATE `_CHAIN.md` *BEFORE* THE FIRST COMMIT ATTEMPT.** Two sessions
  running now, and it is why the doc-row gate has cost zero refusals since #291.
- ⛔ **A STALE `.git/index.lock` IS `mv`'d ASIDE, NEVER `rm`'d** [[git-lock-mv-not-rm]]. One was found
  at #293's open, stranded by a lane commit. Restore a file with `git show <sha>:<path> > <path>`.
- **`pip install tiktoken --break-system-packages` FIRST** in a cold sandbox, and **again after**
  `_gate_scratch_hygiene.py --clean --wrap`, which removes `~/.local/lib`. **Fourth consecutive wrap
  to meet it.**
- **The sub-transcripts are readable from a sandbox seat** at
  `/sessions/*/mnt/.claude/projects/session/<id>.jsonl` and `…/<id>/subagents/agent-*.jsonl`, each
  with a `.meta.json` naming model, `spawnDepth` and description. ★ **And the CONDUCTOR'S top-level
  transcript is readable from a sub seat too — that is the whole of dream pass 9 P1, and the reason
  93 sessions of `⛔ NOT CAPTURED` were avoidable.** `python3 knowledge/_checkin.py --preflight-line <N>`.
- **`knowledge/_graph-mark-observations.jsonl`, `notes/_REHEARSAL-LOG.jsonl` and
  `notes/_dream/_GRADE-DECISIONS.jsonl` are machine appends** — committed with the work and NAMED in
  the body, never swept in silently.
- ⚠ **`_to_delete/` is still an accumulating squatter that `4c` does not reach**, now joined by
  `_to_delete/_s276-D6-lane-ownership-guard/`. What to do about it is his.
- ⚠ **The `size:` stamp is THIS session's own measurement** (GM 35,336 / LS 69,151 / corpus 104,645,
  iterated to a fixed point). ⛔ **The DECLARED post-stamp drift closed at GM 37,065 (4.89%) and LS
  70,164 (1.46%)** against a 10% grading tolerance, because the `s214-D6` chain figure, the
  stratum fills **and two mid-ritual corrections** all land after the stamp, by the #241 rule. The
  stamp was deliberately NOT re-taken for them — saying so is cheaper and truer than a second
  reading nobody can reconcile.

---

*Filed report: `notes/_subreports/2026-09-21-293-W-wrap.md`. Dossier:
`_DECISION-HISTORY/2026-09-21-293-the-dream-backlog-was-cut-down-and-the-review-page-is-owed.md`.
Memory hook: `notes/_lanes/293/WRAP-MEMORY-HOOK.md`. His words:
`notes/_lanes/293/DAVE-RULINGS-2026-09-21.md`. Lane reports:
`notes/_subreports/2026-09-21-293-DA-dream-enactment-audit.md` ·
`notes/_subreports/2026-09-21-293-E1-dream-enactment.md`.*
