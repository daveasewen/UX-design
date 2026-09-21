# 295 · I3 — the regime boundary moves on his word and the wrap gate reaches **ZERO**; the `status` writer is built and the **98 did not move**; `_gen_chain.py --check` stops being red by construction

session: `#295` · 2026-09-21 · lane `I3` · model Opus 5 (1M) · conductor Fable 5.1
job: INSCRIBE + ENACT `s295-D4` · BUILD the `--set-status` writer and back-stamp · FIX `_gen_chain.py --check`. Commit, push, read CI.

COUNTS: findings `12` · ruling-shaped `5` · UNPROVEN `4`

His whole word, verbatim, and it is the entire authority for Part 1:

> `inscribe`

given on the conductor's put, quoted from `notes/_lanes/295/DAVE-RULINGS-2026-09-21.md`:

> `the gate has a count-from-session line, still set to #241; moving it to #295 says the
> post-switch-off boots are a new regime; the old readings are history`

---

## ⛔★★ THREE HEADLINES, AND TWO OF THEM ARE A BRIEF OR A SIBLING LANE BEING WRONG

1. ★★ **THE WRAP GATE READS `0` STRUCTURAL FAILS.** Lane I took it 7 → 1. Lane I2's re-base left
   it at 1. `s295-D4` closed the last one. **Measured at both ends, both readings published below.**
2. ⛔★★ **THE BACK-STAMP DID NOT MOVE THE 98, AND LANE I's Q2 PREDICTED IT WOULD.** Lane I's advisory
   arm read *"98 of 117 enacted rulings carry no sha"* and its question 2 said back-stamping the
   eleven *"moves it to 87"*. **Measured after fourteen stamps: `98 of 131`. The numerator did not
   move by one.** All fourteen were `status: ruled`, not `enacted`-without-a-sha, so the stamps grew
   the **DENOMINATOR** and left the backlog exactly where it was. ⇒ **the ~87 the brief fenced off
   as Dave's does not exist; the 98 is the same 98 it always was.**
3. ⛔★★ **`f81bbdd4` ENACTED TEN #294 RULINGS IN CODE, NOT ELEVEN — AND THE HANDOFF SAYS ELEVEN IN
   TWO PLACES.** See § THE COUNT THAT WAS WRONG.

⚠ **AND THE BRIEF NAMED THE WRONG MODULE FOR PART 1's CONSTANT.** It said
`_gauge_tokens.BOOT_CEILING_FROM_SESSION`. **Measured by grep before anything was edited: the
constant is `_capture_gate.BOOT_CEILING_FROM_SESSION`, line 4047**, and `_gauge_tokens.py:348`
carries only a comment pointing at it. The correction is written into `s295-D4`'s own text rather
than silently absorbed.

---

# PART 1 — `s295-D4` INSCRIBED AND ENACTED

## THE INSCRIPTION — `json.load`, COUNTS AND IDS ONLY, NO RECORD PRINTED

| | |
|---|---|
| `rulings` before | **637** |
| `rulings` after | **638** |
| new id | `s295-D4` |
| the 637 pre-existing records | **compared object-by-object against a pre-inscription copy: IDENTICAL** |
| `_README` | **compared: IDENTICAL** · top-level key order identical |
| `git diff --numstat` | **18 insertions, 0 deletions** — a pure append |

The tool's own span line, verbatim:

```
INSCRIBED: s295-D4 — textual span of 2864 bytes at offset 923530; file 923535 → 926399 bytes;
rulings 637 → 638; reconstruction proof PASSED (all other bytes identical).
```

⛔ **NOTHING WAS HAND-EDITED.** `knowledge/_inscribe_ruling.py --write`, one entry, one invocation.
**Rehearsed TWICE against copies in the gitignored `knowledge/_tmp/` before the live file was
touched:** a `--dry-run`, then a full `--write` played end to end against a SECOND copy and checked
(`637 → 638`, id `s295-D4`, the 637-record prefix `==`, `_README` `==`, key order `==`).
`--selftest` ran **GREEN before** the write.

## THE ENACTMENT — ONE LITERAL, AND THE WORD THAT WOULD HAVE BECOME A LIE

```
BOOT_CEILING_FROM_SESSION = 241
⇒
BOOT_CEILING_FROM_SESSION = 295        # `s295-D4`, Dave's word. (was 241 — `s240-D2`, the #240 diet.)
```

**The provenance is BY ADDITION.** The #241 paragraph above it stays **word for word** — it is the
true history of the FIRST boundary — and a #295 paragraph sits beside it carrying the measured
break (his switch-off at the #293 worker seat), the first post-switch-off reading (72,768 at #295
turn 1), and the arithmetic below.

⛔★ **ONE PROSE STRING WAS CORRECTED RATHER THAN KEPT, BECAUSE KEEPING IT WOULD HAVE MADE THE GATE
LIE IN ITS OWN VOICE.** The hold-harmless note read *"are PRE-DIET (session < #%d)"*. Under a #295
boundary those readings are **PRE-SWITCH-OFF**, a different structural break. The note now names
**both** boundaries so a reader can tell which regime a reading belongs to. ⚠ A gate that reports
correctly while describing itself wrongly is the `s295-D1` `post-mortem #N:` defect one session on.

### WHY A BOUNDARY AND NOT A NUMBER — THE ARITHMETIC, RE-MEASURED AT THIS SEAT

| session | reading | over 72,768 |
|---|---|---|
| #283 | 80,871 | **+8,103** |
| #287 | 74,120 | **+1,352** ← the smallest margin |
| #288 | 74,174 | **+1,406** |
| #289 | 74,174 | **+1,406** |
| #290 | 74,165 | **+1,397** |
| #291 | 74,155 | **+1,387** |
| #292 | 74,170 | **+1,402** |

⇒ **A ceiling that closed this breach by VALUE would have to be ≥ 80,871** — 8,103 above anything
Dave said, and a treadmill rather than a ratchet. All seven **PREDATE the switch-off**. ⇒ the honest
instrument is to stop **CHARGING** readings taken on a retired setup, which is a **BOUNDARY**.

⛔ **WHAT DID NOT MOVE:** `BOOT_CEILING_TK` stays **72,768** and stays shrink-only.
`BOOT_DOUBLE_COUNT_FROM_SESSION` stays **241** — a different question, and a selftest arm asserts it
did not ride along.

### ⛔ THE GATE — MEASURED AT BOTH ENDS, NEITHER DECLARED

**BEFORE**, taken by loading `git show HEAD:knowledge/_capture_gate.py` as its own module and
driving its `boot_constant_drift_check` against this tree:

> **1 fail** — `boot-drift CEILING BREACH: _gauge_tokens.BOOT_CEILING_TK = 72,768 and 7 post-diet
> reading(s) EXCEED it — #283 80,871 · #287 74,120 · #288 74,174 · #289 74,174 · #290 74,165 ·
> #291 74,155 · #292 74,170.`

**AFTER**, the live gate: **0 fails**, and all seven **NAMED** in the note:

> `boot-drift: 7 reading(s) in the window sit above the ceiling but were taken BEFORE the current
> regime boundary (session < #295) and are NOT graded against it — #283 80,871 · #287 74,120 ·
> #288 74,174 · #289 74,174 · #290 74,165 · #291 74,155 · #292 74,170. …Those readings are
> REPORTED and never CHARGED…`

**THE FULL REHEARSAL, `python3 knowledge/_checkin.py --window 200000 --no-block`:**

| when | reading |
|---|---|
| at open (lane I2's filed close, **not re-measured at this seat, declared**) | **1** |
| after the inscription, before the re-render | **1** — but a DIFFERENT fail: `s263-D10 RULINGS PAGE STALE`, **caused by this lane** |
| after `_render_rulings.py` | ★★ **0 STRUCTURAL fails** |

```
rehearsal [wrap-gate, early]: 0 STRUCTURAL fail(s) — fix NOW, cheap · 0 heals-at-wrap · 368 warn(s)
```

⚠ **THE INTERMEDIATE READING IS PUBLISHED BECAUSE IT WAS MINE** — the count stayed at 1 across the
enactment and it would have been easy to report "still 1". **It was a different fail.** The
`s263-D10` re-render is **load-bearing, not an aside** — the third consecutive lane to find that.

### THE SELFTEST PIN — ADDED, EXACT, AND REFUSING BOTH DIRECTIONS

⚠ **THERE WAS NO EXISTING PIN TO RE-PIN.** Measured: no selftest anywhere asserted
`BOOT_CEILING_FROM_SESSION`'s value; the two fixtures that mention it DERIVE from it
(`base = 300 + …` / `500 + …`) and moved harmlessly. So a pin was **added**, in
`selftest_boot_ceiling_discharge`, in lane I2's shape:

⛔ **EXACT, NOT DIRECTIONAL, AND THE REASON IS NOT TIMIDITY.** Raising this boundary **DISCHARGES A
LIVE BREACH BY HIDING ITS READING** — the loudest possible way to absorb a failure without paying
it. Lowering it **re-charges readings his word ruled HISTORY.** Neither is a seat's, so both are
refused. ⚠ **The price is named in the comment:** the next time Dave moves this boundary, the pin
moves in the same commit. **Loosening it to a direction test was available and was REFUSED.**

⛔ **PROVEN ABLE TO FAIL, BY MUTATION, IN MEMORY ONLY:**

```
M1 boundary back to 241 (the old regime)        → 1 failure
M2 boundary raised to 400 (hides live breaches) → 1 failure
M3 boundary lowered to 100                      → 1 failure
M4 double-count boundary dragged to 295         → 1 failure  (the sibling arm)
controls green again: 0
```

---

# PART 2 — THE `status` WRITER

## ⛔ `s172-D3`(e) WAS READ BEFORE ANYTHING WAS BUILT, BY ID LOOKUP, AND IT DOES NOT FORBID THIS

Lane I cited it as forbidding a lane from adding the writer. **Read at this seat from
`knowledge/_rulings.json`**, clause (e) is the **OBSERVED-FAILURE RULE**:

> *"a new test must cite the failure class it guards or the ruling it enforces; a speculative check
> QUEUES as a proposal and is never built"*

and the ruling's own scope line is explicit:

> *"this template governs THE APPETITE FOR NEW INSTRUMENT-BUILDING IN FUTURE SUB BRIEFS ONLY. IT
> RETIRES NOTHING."*

⇒ ⛔ **IT FENCES SPECULATIVE CHECKS, NOT A WRITER A RATIFIED RULING CANNOT BE DISCHARGED WITHOUT.**
The failure is **OBSERVED** — lane I's filed refusal, in this session — and the selftest that ships
with the writer **cites `s295-D2` by name**, which is precisely what (e) demands. **The conductor's
reading is confirmed by the ruling's own text, and lane I's caution was the right instinct on the
wrong clause.**

## `--set-status ID STATUS --evidence-sha SHA`

Same proof discipline as `--amend-evidence`, seven refusals:

| | |
|---|---|
| **S1 TARGET** | the id must exist **exactly once** (shares `_entry_span` with amend) |
| **S2 VOCABULARY** | the new status's **LEAD WORD** must be one already present in the store |
| **S3 SHA** | `enacted` **REQUIRES** a 7–40 lowercase-hex sha |
| **S4 TEXTUAL** | **TWO span swaps in ONE composition**, proven by reconstruction |
| **S4b BOUNDARY** | both spans asserted to be exactly the quoted string / exactly the `[...]` array, and asserted **non-overlapping** |
| **S5 SCOPE** | exactly ONE ruling differs, only in `status`/`evidence` |
| **S6 CHANGES** | a no-op stamp is refused |

⛔★ **THE VOCABULARY IS READ FROM THE STORE AT CALL TIME AND IS NEVER HARD-CODED IN THE TOOL.** A
list of accepted words in this file would be a **SECOND COPY** of the store's own vocabulary — the
copy-chain class this repo refuses everywhere else, and the exact shape lane I2 corrected in
`_gauge_tokens.py`. Enumerated at build time, the store's seven lead words: **`ruled` (603) ·
`enacted` (23) · `standing` (6) · `built` (2) · `part-enacted` (1) · `in` (1) · `superseded` (1)**.
**Nothing was invented.** A seat that wants a new status word must get it ruled.

⛔ **ONE COMPOSITION, NOT TWO WRITES, AND THAT IS THE WHOLE ARGUMENT FOR THE EXTRA COMPLEXITY.** Two
individually-proven writes leave a **HALF-STAMP WINDOW** in which the record reads `enacted` with no
sha — **the exact state `s295-D2` forbids, and the state lane I refused to create on purpose.**

⚠ **DECLARED LIMIT, IN THE CODE:** S3 checks the sha's **SHAPE**. That the commit exists, is
reachable, or did the enacting is **NOT checked** — `git cat-file` needs a repo the tool may run
outside of. Same limit the gate's advisory arm already declares.

### THE SELFTEST — `selftest_set_status()`, SEVEN ARMS, WIRED INTO `--selftest`

vocabulary refuses an invented word · `enacted` refused with **six** malformed shas and with none ·
the control lands byte-exact touching **two fields of one record** · no-op refused · unknown id
refused · **a reformatting composer caught** · **a span one byte too wide caught** (the #294
`armA1c` class, to which S4 is structurally blind).

⛔ **PROVEN ABLE TO FAIL, BY MUTATION, IN MEMORY ONLY:**

```
M1 the vocabulary gate dead                         → 3 failures
M2 the `enacted` sha requirement dropped            → 7 failures
M3 the sha shape loosened to `.*`                   → 5 failures
M4 the composer widened so it also edits `says`     → 1 failure
controls green again: 0
```

⚠ **M4 FIRST CAME BACK AS A TRACEBACK, NOT A RED ARM, AND THAT WAS FIXED RATHER THAN ACCEPTED.**
The control call is now wrapped so a refused control is reported as a named failure —
**a crash is not a fail** [[a-crash-is-not-a-fail]].

## ⛔★★ THE COUNT THAT WAS WRONG — TEN, NOT ELEVEN

`_HANDOFF-145` § 3's heading reads *"ELEVEN ENACTED IN CODE, THREE LANES, ONE COMMIT"* and its OWED
item 3 repeats *"Eleven are enacted in code"*. Lane I named eleven: `s294-D1`…`D9`, `D11`, `D12`.

**DRIVEN OVER THE COMMIT ITSELF** — `git show f81bbdd4 | grep '^+'`, counted per id:

| id | added lines naming it in `f81bbdd4` |
|---|---|
| `s294-D1` `D2` `D3` `D4` `D5` `D6` `D7` `D8` `D9` `D12` | 24 · 78 · 24 · 26 · 20 · 46 · 22 · 20 · 21 · 77 |
| **`s294-D10`** | ⛔ **0** |
| **`s294-D11`** | ⛔ **0** |

⇒ **TEN.** `f81bbdd4`'s own commit message names exactly those ten, lane by lane (A: D1+D8 · B:
D2+D3+D9+D12 · G: D4+D5+D6+D7). `s294-D10` is the Jev decision — a decision, not code, as lane I
said. **`s294-D11` IS enacted — but at the WRAP commit `359b646b`**, and its thirteen added lines
land in `GOOD-MORNING.md`, `_CARRIES.md`, `_CHAIN.md`, the handoff, `_LIVE-STATE.md`,
`_memento-index.json` and a wrap memory hook. ⛔ **NOT ONE `.py` FILE.**

⇒ ⛔ **`s294-D11` IS NOT STAMPED HERE, AND THAT IS A REFUSAL.** It is enacted in the **RITUAL
SURFACES**, not in code, and `f81bbdd4` is not its sha. **Stamping it with a sha the brief did not
name would be inventing provenance, which is the one thing this tool exists to make impossible.**

## THE STAMPS — FOURTEEN

`s294-D1` `D2` `D3` `D4` `D5` `D6` `D7` `D8` `D9` `D12` → **`f81bbdd4`** · `s295-D1` `s295-D2` →
**`95cb58dd`** · `s295-D3` → **`0d487352`** · `s295-D4` → **`ac6b3810`** (this lane's own Part-1
commit, which is why Part 1 committed first).

`s294-D12` carries **the third state in its own status text**: enacted in code AND discharged in
fact by Dave's hands. **Third session running that this state has been named and the field still
has no word for it.**

**PROVEN AFTER THE FACT by `json.load` against the `HEAD` blob:** count `638 → 638` · `_README`
identical · key order identical · **EXACTLY 14 records differ and they are EXACTLY the plan** · **no
record changed outside `status`/`evidence`.**

## ⛔ THE ADVISORY ARM'S NEW READING — AND IT IS THE FINDING

```
s295-D2 ENACTED-SHA: 131 ruling(s) read ENACTED of 638 in the store; 33 carry a sha-shaped
evidence pointer, 98 do not.
```

**Before: 98 of 117. After: 98 of 131.** ⇒ ★★ **BACK-STAMPING FOURTEEN `ruled` RECORDS AS `enacted`
CANNOT REDUCE A COUNT OF `enacted`-RECORDS-WITHOUT-A-SHA. It can only grow the denominator.** Lane
I's Q2 arithmetic (*"moves it to 87"*) assumed the eleven were already `enacted`. **They were all
`ruled`.** ⛔ **The ~87 backlog the brief fenced as Dave's does not exist as a separate object — it
is the same 98, untouched, and this lane back-stamped none of it.**

---

# PART 3 — `_gen_chain.py --check` STOPS BEING RED BY CONSTRUCTION

Lane P's Q3, proven at `280e4e82`: *"the chain was fresh in the tree that was committed and stale in
the tree the commit produced, in the same second, with no edit between."*

## ⛔★ THE CAUSE IS TWO DIFFERENCES, NOT ONE, AND "IT'S JUST THE SHA" WOULD HAVE BEEN THE WRONG FIX

**Measured, by diffing the committed `_CHAIN.md` against a fresh render:**

```
@@ -41 +41 @@   the build-verdict line — `HEAD is ac6b3810` vs `HEAD is ac55c7b2`
@@ -113 +113 @@ *(Chain ends. **10,480 tape …   vs   **10,481 tape …
```

⇒ ★ **THE TWO SHAS ARE THE SAME BYTE LENGTH AND A DIFFERENT TOKEN COUNT**, so they shift the
footer's fixed-point tape figure by one. **Normalising the sha clause out of both strings — the
brief's first suggested shape — would have left the size figure mismatched and the check still
red.** That is why the fix **re-ASKS** instead of normalising.

## THE FIX — RE-ASK AT THE SHA THE COMMITTED CHAIN WAS GENERATED AT

`check()` now, **only when the byte comparison already failed**, reads the committed file's own
stamped HEAD out of its build-verdict line (`CHAIN_HEAD_RE`), and if it differs from the fresh
render's, **regenerates once with that sha pinned** and compares against THAT.

⛔ **WHAT IS NOT WEAKENED, AND IT IS THE CONSTRAINT THE BRIEF SET:** `build()` is **untouched** and
never sees the pin, so **the chain a cold session reads still carries the honest live comparison** —
*"that run is at X, HEAD is Y"* — against the TRUE HEAD. And `--check`'s own green message **names
both shas** rather than going quiet.

⛔★★ **A MODULE GLOBAL WAS WRITTEN FIRST AND IT DID NOT WORK, AND THE REASON IS WORTH KEEPING.**
In-process the fix returned 0; run as a script on the SAME TREE it stayed red. **Cause measured:
`_capture_gate.py:1794` does `import _gen_chain; _gen_chain.build_verdict_line(repo)` — so when this
file runs as `__main__` it is TWO module objects, and the verdict line is rendered by the OTHER one,
whose global was still `None`.** ⇒ the pin moved to an **environment variable**, the one channel
both copies share. ⚠ **This is the #58/#59 class exactly: a check that disagrees with itself across
two environments on one commit.** It was caught because the CLI was re-asked rather than trusted.

⛔ **AND THE ENVIRONMENT MAY NOT PIN THE VERDICT.** A var already set when the process **started**
is `check()`'s own scratch channel being driven from outside: it **REFUSES** (`COULD-NOT-ASK`),
never passes. Selftested.

### THE SELFTEST — FIVE NEW BITES, AND THE FIXTURE IS THE REAL SITUATION

The chain is **GENERATED with the pin set to another sha**, so the fixture is internally consistent
at that sha — tape figure included — and then asked with the pin gone.

⚠ **THE FIRST VERSION OF THESE ARMS PASSED WHILE PROVING NOTHING, AND THE PLANT ASSERTIONS EXIST
BECAUSE OF IT.** Without `notes/_BUILD-VERDICT-LOG.jsonl` **and** `knowledge/_build_all.py` in the
fixture tree the verdict line takes its NOT-DERIVABLE branch, which carries **no HEAD clause at
all** — so the pin had nothing to change and `check()` was reaching the ordinary FRESH path. **Both
files are now copied in, and two bites assert the plant actually planted.**

⛔ **PROVEN ABLE TO FAIL, BY MUTATION — BOTH DIRECTIONS, AS THE BRIEF REQUIRED:**

```
M1 the re-ask laundered (any difference passes once a pin exists)  → 1 bite red:
     "REAL content staleness is STILL RED even when HEAD has also advanced"
M2 the re-ask removed entirely (the pre-#295 behaviour restored)   → 3 bites red:
     GREEN-on-HEAD-advance · names both shas · the FRESH qualifier
M3 the pre-set-environment guard removed                           → 2 bites red
```

## ⛔ THE PROOF THE BRIEF ASKED FOR — GREEN ON THE COMMITTED TREE, NO REGENERATION

See § THE COMMITS for the run and its verbatim output.

---

## THE COMMITS

Three, as briefed. `ac6b3810` (Part 1) · `ac55c7b2` (Part 2) · this one (Part 3 + report).
All through `SESSION_N=295 bash knowledge/_git_commit.sh --reconciled <msgfile> <named paths>`.
**Paths named individually; `add -A` was never used.** Fresh msgfile under a unique name in the
gitignored `knowledge/_tmp/`, line 1 with **no** `after #N` prefix (the script adds it and asserted
exactly one each time).

⚠ **THREE DIRTY PATHS DELIBERATELY NOT STAGED AT EVERY COMMIT, AND THEY ARE NOT THIS LANE'S** —
`notes/_dream/_GRADE-DECISIONS.jsonl` (machine instrumentation whose policy the script itself
declares ⬛ DAVE'S and unruled) · `notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` ·
`notes/_lanes/294/WRAP-MEMORY-HOOK.md` (both left uncommitted by declaration at #294,
`_HANDOFF-145` § OWED 13/14). **All three were dirty before this lane ran any command.**

**Doc row `W-295i3`**, minted through `_state.add()` before staging with a **true** close condition
(population **775 → 776**). ⚠ **The report file had to be created as a DECLARED PLACEHOLDER first,
because `_state.add()` refuses a row whose `home` does not exist on disk** — a small ordering fact
no report has recorded and the next lane will meet.

## ⛔ REFUSALS PAID

1. ⛔★ **THE SHELL ATE THE BACKTICKS ON THE FIRST STAMP RUN.** The fourteen stamps were driven
   through a generated shell script; **command substitution stripped every backticked term from all
   fourteen status strings.** Caught by reading the tool's own echo, not by a gate. **Restored from
   the `HEAD` blob — proven byte-identical to the pre-stamp snapshot with `cmp`, and the live file
   proven equal to the blob after — and every stamp re-run through `subprocess` with an argv LIST
   and no shell.** ⛔ **Nothing was hand-edited at any point and no partial state was committed.**
   ⚠ `git checkout` could NOT do the restore: this mount refuses `unlink` (`s282-D4`), so the blob
   was written back through python.
2. ⛔ **`s263-D10` STALE RULINGS PAGE, TWICE — MINE BOTH TIMES.** Cleared by `_render_rulings.py`
   exactly as the gate wrote the remedy, after Part 1 (638 rulings, sha256 `550d7e9b…`) and again
   after the stamps (sha256 `96ee3fce…`), each verified `--check` FRESH.
3. ⛔ **`s294-D11` NOT STAMPED** — enacted in the ritual surfaces, not in code; `f81bbdd4` is not
   its sha and no sha was invented. See § THE COUNT THAT WAS WRONG.
4. ⛔ **THE ~87 BACKLOG NOT BACK-STAMPED** — fenced by the brief and Dave's per lane I Q2, and
   measured here to be the whole 98 rather than a remainder.
5. ⛔ **`_capture_gate.py --selftest` NOT RUN WHOLE** — the sandbox call wall, third consecutive
   lane. The narrowest probe was run instead: the four boot arms called directly in-process, plus
   the four mutation probes. **DECLARED, not claimed.**

## THE LOCKS — `mv`'D, NEVER `rm`'D

Every `.git/index.lock` met at this seat was moved on-device to
`notes/_lanes/_orphan-locks/stale-index.lock-295-I3-<HHMMSS>`. ⛔ **Nothing was ever `rm`'d** — this
mount refuses `unlink` (`s282-D4`). ⚠ **One was already stranded at the open, before this lane ran
any git command — the fourth consecutive session this has been measured.** `git status` alone, and
`git checkout` on a refused unlink, both strand one.

---

## RULING-SHAPED QUESTIONS

1. ⛔★★ **THE 98 IS NOT A BACKLOG WITH A REMAINDER — IT IS ALL OF IT, AND NOTHING THIS SESSION DID
   TOUCHED IT.** `s295-D2`'s arm now reads 98 of 131. ⇒ **Does the ruling bind FROM #295 FORWARD**,
   the way `BOOT_CEILING_FROM_SESSION` and `BOOT_DOUBLE_COUNT_FROM_SESSION` both now do — in which
   case the arm should carry its own `_FROM_SESSION` and stop counting 295 sessions of records
   written before the convention existed — **or is the 98 a debt to be paid?** ⛔ **No boundary was
   invented here.** ⚠ Until it is answered, `ENACTED_SHA_BLOCKING` can never flip: it would be red
   on 98 records on the day it was promoted.
2. ⛔★★ **`s294-D11` NEEDS A SHA AND THE ONE THE HANDOFF IMPLIES IS WRONG.** It is enacted at the
   WRAP commit `359b646b`, in ritual surfaces, with no `.py` file touched. ⇒ **Is "enacted" a word
   about CODE, or about the repo's surfaces?** If the latter, D11 stamps with `359b646b` and the
   handoff's "eleven" becomes true by a different route. If the former, D11 stays `ruled` and
   **two filed records say eleven where the commit says ten.**
3. ⛔ **`s294-D12`'s THIRD STATE STILL HAS NO WORD** — enacted in code AND discharged in fact by his
   hands. **Third session running this has been named.** This lane put the fact in the record's own
   status prose because there was nowhere else to put it; **that is a workaround, not an answer.**
4. ⚠ **THE EXACT PIN ON `BOOT_CEILING_FROM_SESSION` IS IN PERMANENT TENSION WITH HIS FREEDOM TO
   MOVE IT** — the same tension lane I2 named for `_gauge_tokens` arm E, now at a second constant.
   ⇒ **Should the ruled value live in ONE named place that both the constant and its pin read, or
   is the two-file friction the point?** Two lanes have now paid it.
5. ⚠ **`--check`'s GREEN IS NOW A THIRD VERDICT IN PROSE BUT NOT IN ITS EXIT CODE.** "FRESH at the
   commit it was generated at" exits **0**, the same as a true FRESH. ⇒ **Should a HEAD-only advance
   have its own machine-readable code** the way `COULD-NOT-ASK` (77) does, so CI can tell "matches
   a fresh render" from "matches the render at its own commit"? **The distinction is real and only
   the prose carries it.**

### counts

- rulings inscribed **1** · store **637 → 638** · records reformatted **0** · pure append proven by
  object comparison of all 637 predecessors
- rulings **back-stamped 14** · **status writer BUILT** (lane I's refusal discharged) · constants
  moved **1** (`BOOT_CEILING_FROM_SESSION` 241 → 295, on Dave's word and nothing else)
- gate: **1 → 0** structural fails, both ends measured · warns 368 · gates weakened **0** · gates
  acked **0**
- selftest arms added **3** (the boundary pin pair, `selftest_set_status`, the chain HEAD-advance
  block) · bites inside them **18** · **mutation probes 11, every one bit**
- validators run **7**: `_inscribe_ruling --selftest` (whole, green) · `_gauge_tokens --selftest`
  (whole, green, 0.2 s) · `_governs --selftest` (the same four pre-existing `s282-*` fails, **0
  `s295-D4`**) · `_render_rulings --check` (×2, stale → regenerated → FRESH) · `_gen_chain
  --selftest` (whole, all bites pass) · `_gen_chain --check` · `_checkin --window 200000 --no-block`
- ⛔ **`_capture_gate.py --selftest` NOT RUN WHOLE** — call wall; narrowest probe run and **declared**
- doc rows minted **1** (`W-295i3`, 775 → 776) · commits **3** · locks `rm`'d **0**

### UNPROVEN, named rather than implied

1. **THE WHOLE CAPTURE-GATE SUITE.** Four arms were driven; the rest is CI's to ask.
2. **THAT `f81bbdd4` IS THE RIGHT SHA FOR ALL TEN.** Taken from the commit's own diff and its own
   message — **which is stronger than lane I's inherited claim** — but not verified by reading each
   ruling's enacting code at this seat.
3. **THAT 72,768 HOLDS.** His own word on it is *"possibly"*, and **the first post-#295 cold boot —
   now the FIRST reading the ceiling will actually be judged on — has not happened.**
4. **THAT `--check` STAYS GREEN ACROSS A WRAP.** Proven here across three ordinary commits. A wrap
   rewrites `GOOD-MORNING.md` and `_LIVE-STATE.md`, which is REAL content drift and correctly red
   until regenerated — **the fix does not and must not change that.**

REPLAY-THESE: `python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print(g.BOOT_CEILING_FROM_SESSION, g.BOOT_DOUBLE_COUNT_FROM_SESSION)"` (expect **295 241**) · `python3 -c "import json;r=json.load(open('knowledge/_rulings.json'))['rulings'];print(len(r),r[-1]['id'])"` (expect **638 s295-D4**) · `python3 knowledge/_inscribe_ruling.py --selftest` (expect green, SET-STATUS arms named in the line) · `python3 knowledge/_gen_chain.py --selftest` (expect **all bites pass**) · `python3 knowledge/_gen_chain.py --check` (expect **exit 0** — FRESH, or FRESH-at-its-own-commit if HEAD has advanced) · `python3 knowledge/_render_rulings.py --check` (expect FRESH) · `python3 knowledge/_checkin.py --window 200000 --no-block` (expect **0 STRUCTURAL fails**) · `python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print([x[:90] for x in g.enacted_sha_pointer_check('.')[1] if 'ENACTED-SHA' in x])"` (expect **131 enacted, 33 with a sha, 98 without**)

---

## ⬛ POST-COMMIT ADDENDUM (4) — BY ADDITION; NOTHING ABOVE IS REWRITTEN

⚠ **THIS IS A FOURTH COMMIT AND THE BRIEF ASKED FOR THREE.** The brief allowed *"fewer if the
script's contract forces it"* and not more. **It is declared rather than absorbed: a commit cannot
read its own CI** (lane P's termination, met again), so the choice was a report that says nothing
about CI or one more commit that says what CI said. **The push happened at commit three; this commit
carries only prose.** ★ **And it is itself a proof of Part 3: this commit advances HEAD past the
chain's own commit and `--check` stays green.**

## ⛔ THE PROOF PART 3 OWED — GREEN ON THE COMMITTED TREE, NO REGENERATION

Run immediately after `c896bcaf` with a clean tree (bar the three other-seat paths), with **no
`_gen_chain.py` run in between**:

```
HEAD is now: c896bcaf
  ✅ _CHAIN.md is FRESH at the commit it was generated at (`ac55c7b2`) — HEAD has since advanced to
     `c896bcaf`, and the ONLY difference is the build-verdict line's live-HEAD clause and the tape
     figure it shifts. Content matches GOOD-MORNING.md / _LIVE-STATE.md as they now stand
exit=0
```

⇒ ★★ **THE CHAIN WAS GENERATED AT `ac55c7b2`, TWO COMMITS BACK, AND `--check` IS GREEN.** Under the
old behaviour this tree was red by construction.

## ⬛ THE PUSH — THE SANCTIONED ARM WAS TRIED FIRST, IT REFUSED, AND THE FALLBACK IS DECLARED

⛔ **`bash knowledge/_git_commit.sh --push` WAS RUN FIRST AND REFUSED AT THE DIRT GATE — lane P's and
lane I2's finding reproduced a third time, on the identical three paths:**

```
✗ push refused: tree not clean — commit first (s133-D2; rehearsal log excluded per s137-D1). Dirty paths:
 M notes/_dream/_GRADE-DECISIONS.jsonl
 M notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md
 M notes/_lanes/294/WRAP-MEMORY-HOOK.md
```

⛔ **THE PUSH THEREFORE WENT BY PLAIN `git push origin master`, A DECLARED FALLBACK AND NOT THE
SANCTIONED PATH.** The brief authorised it explicitly and the conductor's verdict is PUSH. **The
price is named rather than implied: the `s294-D5` expiry gate, the fast-forward-only gate, the
master-only gate and the script's own post-push verification ALL SKIPPED.** Branch was confirmed
`master` before the push and the verification was re-done by hand; **the expiry check was NOT
re-done and nothing here claims it.**

```
   89f09db9..c896bcaf  master -> master
git rev-parse HEAD            → c896bcafbacb725833ffb7f59c5f49666f27eff4
git ls-remote origin master   → c896bcafbacb725833ffb7f59c5f49666f27eff4   ✅ EQUAL
```

⛔ **The remote URL and its token were never printed: every line that touched them is `sed`-redacted.**

## ⬛ CI, READ BACK FOR `c896bcaf`

**RUN `35652886287` · workflow `gates` · created 2026-09-21T20:43:54Z · POLLED TO COMPLETION ·
RUN CONCLUSION: FAILURE.**

| job | colour | failing steps |
|---|---|---|
| `gates` | ⛔ **FAILURE** | **5** `Survey the COMMITTED tree` · **6** `Knowledge build` |
| `release` | ✅ **SUCCESS** | none |
| `render` | ✅ **SUCCESS** | none |

⚠ **`render` stayed `in_progress` for roughly eight minutes after `gates` and `release` had closed.
The verdict above is the one taken AFTER it finished** — the #291/#292 lesson, met a fifth time.

### ★★ THE ONE THING THIS LANE WENT TO CI TO LEARN, AND IT IS THE ANSWER IT WANTED

```
#295 lane P  (d30aebe1):  SURVEY: 58 pass · 7 FAIL · 4 COULD-NOT-ASK · 0 unaskable · 77 not asked
#295 lane I2 (0d487352):  SURVEY: 58 pass · 7 FAIL · 4 COULD-NOT-ASK · 0 unaskable · 77 not asked
#295 lane I3 (c896bcaf):  SURVEY: 59 pass · 6 FAIL · 4 COULD-NOT-ASK · 0 unaskable · 77 not asked
```

★★ **`[120] read chain determinism check` IS GREEN IN CI, verbatim from the run log:**

```
  ✅ [120] read chain determinism check — stale _CHAIN.md serves a PREVIO…
```

⇒ ⛔ **THE ONLY STEP THAT MOVED IS THE ONE PART 3 FIXED, AND IT MOVED THE RIGHT WAY.** 7 → 6 fails,
58 → 59 passes. **It is the step lane P found NEWLY RED on `d30aebe1` and called red on every pushed
tree by construction; it is green on a pushed tree now.**

**THE SIX THAT REMAIN, BY NAME** (never by number — lane P measured that survey step IDs move
between sessions): `[3]` token blast-radius · `[13]` capture/provenance selftest · `[38]`
component-partials sync · `[125]` memento schematic determinism · `[128]` memento-package
delta-audit · `[136]` governs matcher selftest. ⛔ **All six inherited, identical to lane P's and
lane I2's set minus `[120]`.**

⇒ ⛔ **AND THE REST OF THIS LANE BROKE NOTHING CI CAN SEE.** `[13]` is `_capture_gate.py --selftest`,
which this lane edited (the boundary constant, the note text, the new pin arms) — **still exit 1 on
the same `pre-flight:` stamp arm, no worse and no better.** `_inscribe_ruling.py` gained a whole new
write path and `[9]`'s help-gate selftest and step 6's script scan both still count the same 12
failures on the same 12 files. Step 6 aborts where it always did:

```
help-gate: 264 script(s) scanned, 12 failure(s) — a script that can write before it reads argv is
the #157 gen_showroom defect
```

⛔★ **THE ZERO IS INVISIBLE TO CI, AND THAT IS WORTH SAYING OUT LOUD.** The wrap gate reading `0`
structural fails — this lane's first headline — **does not appear in CI at all**:
`_capture_gate.py --wrap` is wired into no CI step, lane P and lane I2 both measured that, and it
holds here. **The only instrument that sees the zero is the local rehearsal.**

⛔ **NOTHING CI REPORTED WAS REPAIRED** — the brief fences it.
