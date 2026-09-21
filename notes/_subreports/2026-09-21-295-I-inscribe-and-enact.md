# 295 · I — two rulings inscribed on his word and both enacted in code: `s295-D1`, `s295-D2`, store 634 → 636, gate 7 → 1

session: `#295` · 2026-09-21 · lane `I` · model Opus 5 (1M) · conductor Fable 5.1
job: INSCRIBE `s295-D1` and `s295-D2`, ENACT both in `knowledge/_capture_gate.py`, commit. No push.

COUNTS: findings `11` · ruling-shaped `5` · UNPROVEN `3`

His word, verbatim, and it is the whole authority for this lane:

> `inscribe`

given after two recommendations were put to him in chat, themselves answering his

> `1. i need to see them`
> `2. I don't know the answer to this`

⛔ **THE HEADLINE RESULT IS A NUMBER AND ITS OPPOSITE.** `s295-D1` took the wrap gate from **7
structural fails to 1** — measured at both ends, both readings published below — and the ONE that
remains is the boot **CEILING BREACH**, which this lane did not touch, did not weaken and could not
have closed: its remedy is to cut the boot, and the literal is Dave's alone.

⛔ **AND ONE THING WAS REFUSED RATHER THAN IMPROVISED: the eleven of #294 ARE NOT BACK-STAMPED.**
The sanctioned writer has no path to `status`. See § THE REFUSAL THAT MATTERS.

---

## COUNTS — `json.load`, IDS AND COUNTS ONLY, NO RECORD PRINTED

| | |
|---|---|
| `rulings` before | **634** |
| `rulings` after | **636** |
| new ids, in the order they were put to him | `s295-D1` `s295-D2` |
| the 634 pre-existing records | **compared object-by-object against a pre-inscription copy: IDENTICAL** |
| `_README` (20 keys) | **compared: IDENTICAL** · top-level key order identical |
| `git diff --numstat` | **33 insertions, 0 deletions** — a pure append |

The two spans, as the tool printed them:

```
s295-D1  1964 B @ 916629   file 916,634 → 918,598 bytes
s295-D2  2314 B @ 918593   file 918,598 → 920,912 bytes
```

Both lines read `reconstruction proof PASSED (all other bytes identical)`.

⛔ **NOTHING WAS HAND-EDITED.** Both went in through `knowledge/_inscribe_ruling.py --write`, one
entry per invocation. **Rehearsed twice before the live file was touched:** each entry `--dry-run`'d
individually against `knowledge/_tmp/rulings-pre-295.json`, then the two-in-sequence run played
end-to-end against a second copy and checked (`634 → 636`, ids in order, the 634-record prefix
`==`) BEFORE the live write.

`python3 knowledge/_inscribe_ruling.py --selftest` ran **GREEN before** the writes and the store
parses green after. `_governs.py --selftest`: **the same four pre-existing `s282-*` fails and no
others** — `grep -c s295` over its whole output reads **0**, so neither new record appears in any
fail, note or `⬛ DECLARED` line. R1…R6 all passed at arrival.

## THE TWO, ONE LINE EACH

| id | what it rules | his word |
|---|---|---|
| `s295-D1` | the boot double-count arm reads the `post-mortem #N:` line and **nothing else**; the log is append-only and is not edited; the **ceiling is unchanged and the breach stands** | inscribe |
| `s295-D2` | the **enacting lane** stamps `status: enacted` in the **same commit**, the **commit sha is the proof**, and the wrap checks it — **ADVISORY at first** | inscribe |

⚠ **`s295-D1` IS NARROWER THAN THE PROPOSAL IT ANSWERS, AND THE RULING SAYS SO IN ITS OWN TEXT.**
Lever 3 of `notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md` asked for **all seven** inherited
fails to be ruled CLOSED as history, **"no code"**. What he was actually shown, and what he ruled,
was **two problems**: six double-counts closed by a **code narrowing**, and the ceiling breach left
standing. Six, not seven; code, not no-code. Recorded inside the ruling rather than smoothed.

---

## (a) `s295-D1` ENACTED — `knowledge/_capture_gate.py`, ONE ARM, NO CONSTANT MOVED

⛔★★ **THE DEFECT WAS NEVER WHAT THE FAIL TEXT SAID IT WAS. NOT ONE of the six was a session
stating its own boot twice.** Measured before the edit, from the live log:

- **#243 was charged FIVE times** because four *later* strata quote its reading inside a
  `"#243 form"` **carry paragraph** (`⛔ THREE BLOCKING GATE REFUSALS ARE CARRIED IN THE #243 FORM…`).
  Four of those five lines are not #243's stratum at all.
- **#264, #273, #287** were charged because their `wrap-handover: brief-cut …` / delta lines restate
  the figure the post-mortem line already stated.
- **#272, #274** were charged by a carry paragraph in their own stratum.

Every one is a session **talking about** a reading, not **taking** one. And the arm's own remedy text
said *"Delete the restatement"* — **the one repair no wrap may make**, because `notes/_GAUGE-LOG.md`
is append-only. A gate whose only discharge is forbidden is a gate that gets routed around
[[gate-cannot-pass-in-one-environment]]: twenty consecutive wraps took the #243 path past it.

**THE EDIT, AND ITS BLAST RADIUS:**

- new `BOOT_POST_MORTEM_LINE_RE` + `_is_post_mortem_row(row)` — a reading counts toward the
  double-count only if it sits on a post-mortem line **whose own ordinal is the session being
  graded**.
- `boot_stratum_double_count_check` grades `[r for r in rows if _is_post_mortem_row(r)]`.
- the fail text now says **`⛔ THE LOG IS APPEND-ONLY: do not edit a written stratum`** and points
  the fix at the stratum being written now.
- the uncharged rows are **counted and named in a note** — `74 boot reading(s) … are NOT CHARGED` —
  never made invisible.

⛔ **`_parse_boot_rows` IS BYTE-UNCHANGED.** The derived band, the drift arm and the delta arm all
read it and **none of them is narrowed**. `BOOT_CEILING_TK` untouched. `BOOT_DOUBLE_COUNT_FROM_SESSION`
still **241** — the ruling narrows WHAT IS READ and moves no boundary, and the selftest asserts that.

⚠ **A PREMISE IN THE BRIEF (AND IN THE RULING'S OWN LETTER) IS TOO TIDY, AND IT IS PUBLISHED RATHER
THAN SMOOTHED.** The ruling names the line as `post-mortem #N:` **with a colon**. Measured over the
live log: **#243's line reads `> **post-mortem #243:**` but #264 / #272 / #273 / #274 / #287 all
read `> **POST-MORTEM #264 — measured, not narrated.**` — upper case, EM DASH, no colon.** Five of
the six fails would have **survived** a matcher pinned to the ruling's own punctuation. The matcher
is therefore case-insensitive and admits `:` or a dash, which **widens the ruling's letter to reach
the strata the ruling's subject names by number** — and that widening is stated in the code comment
and asserted by selftest arm (4), not left for a reader to discover.

⚠ **ONE SIDE EFFECT, DECLARED:** the old `legacy` note (pre-#241 ordinals carrying more than one
reading) now prints **nothing**, because under the narrowed reading **no** pre-#241 ordinal carries
two post-mortem lines. The information did not vanish — the `NOT CHARGED` note counts the same rows
— but a reader watching for the old wording will not find it. Selftest arm (5) keeps the pre-#241
hold-harmless honest with its own fixture.

### the selftest — `selftest_boot_double_count_narrowing()`, six arms, each naming its control

| arm | fixture | must |
|---|---|---|
| 1 | post-mortem line alone | **PASS** (the control for 3) |
| 2 | figure repeated in a `wrap-handover` line · in a `#243 form` carry paragraph · both | **PASS** + leave a `NOT CHARGED` note |
| 3 | **two** `post-mortem #250` lines, one session | **FAIL**, and the fail must say `APPEND-ONLY` |
| 4 | the live log's real `POST-MORTEM #N — …` shape | **PASS** |
| 5 | `BOOT_DOUBLE_COUNT_FROM_SESSION == 241` · a pre-#241 double | boundary unmoved · ungraded |

⛔ **PROVEN TO BE ABLE TO FAIL, BY MUTATION, IN MEMORY ONLY** — a selftest nobody has seen go red is
a decoration:

```
M1 un-narrowed   (_is_post_mortem_row → True)  → 4 failures  (arm 2 fires first)
M2 over-narrowed (_is_post_mortem_row → False) → 1 failure   (arm 3: "the narrowing ate the defect")
controls green again: 0
```

## (b) `s295-D2` ENACTED — the ADVISORY arm, beside the other advisory arms

`enacted_sha_pointer_check(repo)` + `ENACTED_SHA_BLOCKING = False` + `ENACTED_STATUS_RE` /
`ENACTED_SHA_RE`, wired into `wrap_checks` in the `(fails if … else warns)` shape the other advisory
arms use, immediately before `fill_working_ceiling_check`.

⛔ **ADVISORY BY THE RULING'S OWN WORDS**, and the reason is measured, not timid — **its first live
reading is the argument for why it could not have blocked today**:

> `s295-D2 ENACTED WITHOUT A SHA: 98 of 117 ruling(s) with 'status: enacted' carry NO sha-shaped
> evidence pointer`

**117 ENACTED records of 636; 19 carry a sha, 98 do not.** A blocking arm would have been red on the
day it was built, on 295 sessions of records written before the convention existed. The count prints
every wrap so the promotion argument can be made on numbers. **Promotion is Dave's word.**

⚠ **WHAT IT DOES NOT CHECK, SAID OUT LOUD IN THE CODE:** that the sha is real, reachable, or the
commit that did the enacting. It asserts the **SHAPE**. A shaped-but-wrong pointer is a smaller lie
than no pointer, and `git cat-file` per pointer needs a repo the gate may be run outside of.

### the selftest — `selftest_enacted_sha_pointer()`, six arms

control (enacted **with** a sha → silent) · the bite (enacted, no sha → raised **by id**) · scope
(a `ruled` record is not charged) · prose is not a sha · **an unreadable store reads UNMEASURED, never
green** [[a-crash-is-not-a-fail]] · `ENACTED_SHA_BLOCKING` is False.

⛔ **PROVEN TO BE ABLE TO FAIL, BY MUTATION:**

```
M3 status-re dead     → 3 failures
M4 sha-re too loose   → 2 failures
M5 promoted to BLOCKING → 1 failure ("promotion is Dave's word, not a seat's")
controls green again: 0
```

## ⚙ THE TEST I RAN, AND THE ONE I DID NOT — SAID PLAINLY

⛔ **`python3 knowledge/_capture_gate.py --selftest` WAS NOT RUN WHOLE.** The brief declares it
exceeds the sandbox call wall at ~165 s and instructs the narrowest possible probe; that instruction
was obeyed. What ran instead: **the two new arm functions called directly in-process**, both
returning `0` failures, **plus the five mutation probes above**, plus `boot_stratum_double_count_check`
driven against the live repo. ⚠ **This is not the suite passing**, and the first honest asking of the
whole suite is CI — which is behind the still-unpushed commits (`_HANDOFF-145` § OWED 1). **Declared,
not claimed.**

## ⛔ THE GATE — 7 → 1, BOTH READINGS MEASURED, NEITHER DECLARED

**BEFORE.** Taken by loading `git show HEAD:knowledge/_capture_gate.py` as its own module and
driving its `wrap_checks('.', 2026-09-21, lane=False)` **against the 634-record pre-inscription
store** — i.e. the tree exactly as #295 inherited it — then restoring the live store and proving it
byte-identical with `cmp`:

> **FAILS 7 · WARNS 358** — the CEILING BREACH + `#243` ×5 · `#264` · `#272` · `#273` · `#274` · `#287`

**AFTER.** `python3 knowledge/_checkin.py --window 200000 --no-block`:

> `rehearsal [wrap-gate, early]: 1 STRUCTURAL fail(s) — fix NOW, cheap · 0 heals-at-wrap · 365 warn(s)`

The one remaining, in full and untouched:

> `⛔ STRUCTURAL boot-drift CEILING BREACH: _gauge_tokens.BOOT_CEILING_TK = 70,000 and 7 post-diet
> reading(s) EXCEED it — #283 80,871 · #287 74,120 · #288 74,174 · #289 74,174 · #290 74,165 ·
> #291 74,155 · #292 74,170.`

⚠ **THE INTERMEDIATE READING IS PUBLISHED TOO, BECAUSE IT WAS MINE:** between the inscription and
the page re-render the rehearsal read **2** — the second was `s263-D10 RULINGS PAGE STALE`, caused
by this lane's own inscription. Cleared as § REFUSALS records. **No gate was weakened, none acked.**

## ⛔⛔ THE REFUSAL THAT MATTERS — THE ELEVEN ARE **NOT** BACK-STAMPED

`s295-D2` rules that the eleven #294 rulings enacted in code are back-stamped `status: enacted` with
`f81bbdd4`. **NOTHING WAS STAMPED. The tool has no path to `status`, and hand-editing
`knowledge/_rulings.json` is the #179 defect this project abolished.** Measured, not assumed:

- `--help` on the sanctioned writer: *"AMEND (sanctioned #193, **evidence array ONLY** — `says` is
  unreachable from here)"*.
- `grep -n status knowledge/_inscribe_ruling.py` → **five hits, none of them a writer**: the R1
  docstring, the `KEYS` tuple, a type-check loop, a selftest fixture value, a selftest deletion.
- `argparse` has `--entry --rulings --dry-run --write --selftest --amend-evidence --id`. **No
  `--status`, no `--amend-status`.**

⛔ **THE HALF-STAMP WAS AVAILABLE AND WAS REFUSED.** `--amend-evidence` *could* have appended
`commit f81bbdd4 …` to each of the eleven. That would have produced eleven records **still reading
`status: ruled`** while carrying an enactment sha — a record that claims nothing and points at a
commit, and the new advisory arm keys on `status`, so the half-stamp would have moved **zero** of the
98. **A convincing-looking half of a ruling is worse than an honest absence.** Brief's instruction
obeyed to the letter: *report it as a refusal and stamp nothing.*

⇒ **`s295-D2` IS RULED AND ITS GATE IS BUILT, AND ITS BACK-STAMP IS OWED TO A WRITER THAT DOES NOT
EXIST.** The eleven, named so the next seat need not re-derive them from the handoff: `s294-D1`
`s294-D2` `s294-D3` `s294-D4` `s294-D5` `s294-D6` `s294-D7` `s294-D8` `s294-D9` `s294-D11` `s294-D12`.
**Not in that set, and why:** `s294-D10` is the **Jev decision** — a decision, not code
(`_HANDOFF-145` § 3 names *eleven* enacted across lanes A, B and G and calls D10 out separately).
⚠ `s294-D12` is a **third state the field has no word for**: enacted in code AND discharged in fact,
by Dave's own hands. It is in the eleven for its code half only, and `_HANDOFF-145` § OWED 3 flags
the same gap.

⛔ **`s295-D2` ITSELF IS `status: ruled`, NOT `enacted`,** although this lane enacted it — for the
same reason. The ruling's own first duty cannot be discharged by the ruling's own enactment lane.

## `notes/_RULINGS.html` — RE-RENDERED, AS THE GATE DEMANDED IN ITS OWN WORDS

The brief was right that this would go red and it did, at the rehearsal between the two steps:

> `⛔ STRUCTURAL s263-D10 RULINGS PAGE STALE — STALE _RULINGS.html embeds 9401d3c1… but
> _rulings.json is now 6d009d8b…`

Remedy run **exactly as the gate wrote it, in that order**: `_render_rulings.py` →
`wrote notes/_RULINGS.html  636 rulings  162 sessions  1,152,406 bytes  sha256 6d009d8b…`, then
`--check` → `FRESH _RULINGS.html matches _rulings.json sha256 6d009d8b…`.

## THE DOC ROW

`W-295i`, minted through `_state.add()` before staging, with a **true** close condition (the arm
refuses without one, and inventing one is the smaller cousin of inventing his ruling).

## THE COMMIT — `95cb58dd`, ONE REFUSAL PAID

`95cb58dd` — **9 files changed, 718 insertions, 20 deletions**, 2 created.

```
SESSION_N=295 bash knowledge/_git_commit.sh --reconciled \
  knowledge/_tmp/msg-295-I-inscribe-enact-2001.txt <9 named paths>
```

Staged: `knowledge/_rulings.json` · `knowledge/_capture_gate.py` · `knowledge/_state.json` ·
`_CHAIN.md` · `notes/_RULINGS.html` · `notes/_lanes/295/DAVE-RULINGS-2026-09-21.md` ·
`notes/_subreports/2026-09-21-295-I-inscribe-and-enact.md` · and the two machine appends
`notes/_REHEARSAL-LOG.jsonl` · `notes/_dream/_GRADE-DECISIONS.jsonl`.
**Paths named individually; `add -A` was never used. NOTHING IS PUSHED** — no remote consulted,
no `git ls-remote`, no CI claimed. Fresh msgfile under a unique name in the gitignored
`knowledge/_tmp/`, line 1 with **no** `after #N` prefix (the script adds it, and asserted exactly
one).

**The gate at the commit seam, DECLARED not-a-wrap (`#74-D1`), red visible not blocking:**

> `capture gate [wrap]: 232 in scope · 1 fail · 366 warn`

**Doc-row gate: population 547 · staged-in-THIS-commit 1 · unrowed 0 · ✅ PASS.**

### ⛔ REFUSALS PAID — TWO, VERBATIM, NEITHER ARGUED WITH, NEITHER ACKED

**1 · `s263-D10` — the rulings page, caught by the rehearsal between the two steps.** Quoted in
full in § `notes/_RULINGS.html` above. **Real, and caused by this lane.** Remedy run exactly as the
gate wrote it.

**2 · THE STEP-0.5 RECONCILE GATE REFUSED THE FIRST COMMIT ATTEMPT:**

> `✗ refusing to stage: run 'git status --short', account for EVERY dirty path (step 0.5), then
> re-run with --reconciled.`

**Accounted for, and the two unstaged paths are deliberately not mine:**
`notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md` — **another worker's LIVE file**, left
uncommitted by declaration at #294 (`_HANDOFF-145` § OWED 13: *"in-flight is not a stray (#70)"*) —
and `notes/_lanes/294/WRAP-MEMORY-HOOK.md`, **owed to the conductor** (§ OWED 14). Staging either
would mean minting a doc row on another seat's behalf and freezing work still moving. The script's
own line: `⚠ 2 dirty path(s) NOT staged — deliberate under explicit-path staging`.

### THE LOCKS — TWO RENAMED ON-DEVICE, ZERO `rm`'d

`.git/index.lock` (0 bytes) existed at the pre-commit check and was `mv`'d to
`notes/_lanes/_orphan-locks/stale-index.lock-295-I-2000`; a second respawned before the retry and
went to `stale-index.lock-295-I-<HHMMSS>`. `.git/HEAD.lock` and `.git/refs/heads/master.lock` were
**absent at both checks**. ⛔ **Nothing was ever `rm`'d** — this mount refuses `unlink`
(`s282-D4`), and the script's own
`warning: unable to unlink … Operation not permitted` is git failing to clean up after itself, not
a foreign lock. The script closed on `✓ done — locks clear`.

---

## RULING-SHAPED QUESTIONS

1. ⛔ **WHO BUILDS THE `status` WRITER, AND DOES IT BELONG IN `_inscribe_ruling.py`?** `s295-D2`
   cannot be discharged without one, and the only sanctioned writer reaches the evidence array only.
   A `--set-status --id <id> --sha <sha>` path with the same reconstruction proof is the obvious
   shape; **building it is a new instrument in the same breath as the finding that motivates it,
   which `s172-D3(e)` forbids.** So: next session, with its own brief?
2. ⛔ **THE 98.** `s295-D2`'s arm reads **98 of 117 ENACTED records carry no sha.** Back-stamping the
   eleven of #294 moves it to 87. Is the remaining 87 a **backlog to be paid**, or does the ruling
   bind **from #295 forward** the way `BOOT_DOUBLE_COUNT_FROM_SESSION` and `BOOT_CEILING_FROM_SESSION`
   both do? **Nothing was assumed and no `_FROM_SESSION` boundary was invented here.**
3. ⛔ **`s294-D12`'s THIRD STATE STILL HAS NO WORD.** Enacted in code AND discharged in fact by his
   hands. `status` has `ruled` / `enacted`; a record that is both, or that is discharged rather than
   coded, cannot say so. Second session running this has been named.
4. ⚠ **WHEN DOES `ENACTED_SHA_BLOCKING` FLIP?** Written ADVISORY by the ruling's words. The number
   it would be argued on now prints every wrap. **Dave's word, and nobody should promote it quietly.**
5. ⚠ **THE RULING'S LITERAL `post-mortem #N:` DOES NOT MATCH FIVE OF THE SIX STRATA IT CLOSES.**
   The matcher was widened to case-insensitive with `:` or a dash, and that widening is a seat's
   reading of his intent, not his text. **Amend `s295-D1`'s premise by addition, or let the code
   comment carry the correction?** (Same shape as `_HANDOFF-145` § OWED 4.)

### counts

- rulings inscribed **2** · store **634 → 636** · records reformatted **0** · gates weakened **0** ·
  gates acked **0** · constants moved **0**
- rulings **back-stamped 0 of 11** — the sanctioned writer has no `status` path; **refusal, not an
  oversight**
- gate: **7 structural fails → 1** (measured at both ends) · warns 358 → 365 (the new advisory arm
  is one of them)
- selftest arms added **2**, arms inside them **12**, **each proven able to fail** by 5 mutation
  probes
- validators run **6**: `_inscribe_ruling --selftest` (green) · `_governs --selftest` (4
  pre-existing `s282-*` fails, **0 `s295-*`**) · `_render_rulings --check` (stale → regenerated →
  fresh) · `_gen_chain --check` · the two new arms direct · `_checkin --window 200000 --no-block`
- ⛔ **`_capture_gate.py --selftest` NOT RUN WHOLE** — call wall; narrowest probe run instead and
  **declared**, not claimed
- doc rows minted **1** (`W-295i`, population 772 → 773) · commits **2** (`95cb58dd`, + this report completed) · pushes **0** · locks `rm`'d **0** · locks renamed on-device **2**
- refusals paid **2**: `s263-D10` stale rulings page (mine, cleared by re-render) · the step-0.5 reconcile gate (2 dirty paths belonging to other seats, accounted for and deliberately unstaged)

### UNPROVEN, named rather than implied

1. **The whole capture-gate suite.** Only the two new arms and their mutations were driven.
2. **CI on any of it.** Seven commits are local and unpushed; no CI run exists and none is claimed.
3. **That `f81bbdd4` is the right sha for all eleven.** Taken from `_HANDOFF-145` and #294 lane I's
   report; **not verified by `git show` per ruling at this seat**, and moot while the stamp is refused.

## RULING-SHAPED QUESTIONS — WHAT I FOUND WRONG IN MY OWN BRIEF

Said plainly rather than smoothed, as instructed:

1. ⛔ **"copy the exact form from #294 lane I's report" — #294 lane I's report DOES NOT CARRY the
   three `s218-D7` machine-read lines.** Driven with the gate's own three regexes over all eight
   `2026-09-21-294-*` reports: `notes/_subreports/2026-09-21-294-I-inscribe.md` matches
   `SUBREPORT_QUESTIONS_RE` **False**, `SUBREPORT_REPLAY_RE` **False**, `SUBREPORT_COUNTS_RE`
   **False** — it carries `### counts`, `### replay these` and a prose heading instead. The form was
   copied from `2026-09-21-294-B-enact-d2-d3-d9-d12.md`, which matches all three.
   ⚠ That is lane B's own gate catching a sibling lane retroactively, and it is exactly the
   population `s294-D2` was ruled about.
2. ⚠ **The ruling's `post-mortem #N:` literal.** Five of the six strata it closes do not use a colon.
   Detailed in § (a).
3. ⚠ **"expect 1 — the ceiling breach only" was right, but only after a second step.** The reading
   immediately after inscription was **2**; the `s263-D10` page re-render the brief mentioned as an
   aside is **load-bearing**, not optional.

REPLAY-THESE: `python3 knowledge/_inscribe_ruling.py --selftest` · `python3 knowledge/_governs.py --selftest` · `python3 knowledge/_render_rulings.py --check` · `python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print(g.selftest_boot_double_count_narrowing(), g.selftest_enacted_sha_pointer())"` · `python3 -c "import json;r=json.load(open('knowledge/_rulings.json'))['rulings'];print(len(r),[x['id'] for x in r[-2:]])"` · `python3 knowledge/_checkin.py --window 200000 --no-block`
