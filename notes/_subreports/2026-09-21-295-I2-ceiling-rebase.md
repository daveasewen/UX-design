# 295 · I2 — the boot ceiling is re-based on Dave's word: `s295-D3` inscribed (636 → 637), `BOOT_CEILING_TK` 70,000 → 72,768 — AND THE BREACH DID NOT CLOSE

session: `#295` · 2026-09-21 · lane `I2` · model Opus 5 (1M) · conductor Fable 5.1
job: INSCRIBE `s295-D3`, ENACT the literal in `knowledge/_gauge_tokens.py`, commit, PUSH, read CI.

COUNTS: findings `9` · ruling-shaped `4` · UNPROVEN `3`

His word, verbatim, and it is the whole authority for this lane:

> `1. I can't cut anything else permanently, this is possibly the new ceiling`

---

## ⛔★★ THE HEADLINE IS THE BRIEF'S OWN EXPECTATION BEING WRONG, AND IT IS MEASURED

**The brief said: *"publish the REHEARSAL fail count (lane I left it at 1 — the ceiling breach;
expect 0 now — measure it)."* MEASURED: IT IS STILL 1. THE RE-BASE DID NOT CLOSE THE BREACH.**

The gate's own line after the enactment, verbatim and unedited:

> `⛔ STRUCTURAL boot-drift CEILING BREACH: `_gauge_tokens.BOOT_CEILING_TK` = 72,768 and 7
> post-diet reading(s) EXCEED it — #283 80,871 · #287 74,120 · #288 74,174 · #289 74,174 ·
> #290 74,165 · #291 74,155 · #292 74,170.`

**THE ARITHMETIC NOBODY DID BEFORE THE RULING WAS DRAFTED.** The ceiling moved UP by 2,768. The
breaching readings sit between 74,120 and 80,871. **The smallest of them, #287, is 74,120 —
1,352 tokens ABOVE the new ceiling.** Margins before and after, per reading:

| session | reading | over 70,000 | over 72,768 |
|---|---|---|---|
| #283 | 80,871 | +10,871 | **+8,103** |
| #287 | 74,120 | +4,120 | **+1,352** |
| #288 | 74,174 | +4,174 | **+1,406** |
| #289 | 74,174 | +4,174 | **+1,406** |
| #290 | 74,165 | +4,165 | **+1,397** |
| #291 | 74,155 | +4,155 | **+1,387** |
| #292 | 74,170 | +4,170 | **+1,402** |

⇒ **The re-base shaved 2,768 off every margin and cleared NONE of them.** A ceiling that closed
this breach would have to be **≥ 80,871** — the #283 reading — which is 8,103 above anything Dave
said and would not be an honest shrink-only ratchet in any case.

⇒ ★★ **THE RE-BASE AND THE BREACH ARE TWO DIFFERENT OBJECTS AND THE BRIEF TREATED THEM AS ONE.**
The re-base is about **what the NEXT boot is graded against**. The breach is about **readings
taken on the OLD, heavier boot**, which are append-only testimony and do not become smaller
because the line moved. **The only thing that would drop them out of the gate is moving
`BOOT_CEILING_FROM_SESSION` — a REGIME BOUNDARY — and `s295-D3` explicitly does not touch it and
this lane did not invent one.** That is a ruling-shaped question, below, not a seat's to answer.

⚠ **AND THE GATE NAMES SEVEN WHERE THE BRIEF NAMED NINE.** The brief's evidence lists nine
post-diet readings over 70,000, adding `#293 74,204` and `#294 74,656`. **The gate's live reading
names SEVEN and neither #293 nor #294 is among them.** Both figures are carried into the ruling's
text as the brief gave them; the discrepancy is **published, not reconciled** — the two later
readings are evidently not yet in the parsed post-diet sample set, and diagnosing why would mean
grading the log parser, which no part of this lane's authority covers.

---

## THE INSCRIPTION — `json.load`, COUNTS AND IDS ONLY, NO RECORD PRINTED

| | |
|---|---|
| `rulings` before | **636** |
| `rulings` after | **637** |
| new id | `s295-D3` |
| the 636 pre-existing records | **compared object-by-object against a pre-inscription copy: IDENTICAL** |
| `_README` | **compared: IDENTICAL** · top-level key order identical |
| `git diff --numstat` | **18 insertions, 0 deletions** — a pure append |

The tool's own span line, verbatim:

```
INSCRIBED: s295-D3 — textual span of 2623 bytes at offset 920907; file 920912 → 923535 bytes;
rulings 636 → 637; reconstruction proof PASSED (all other bytes identical).
```

⛔ **NOTHING WAS HAND-EDITED.** `knowledge/_inscribe_ruling.py --write`, one entry, one
invocation. **Rehearsed twice against copies before the live file was touched:** a `--dry-run`
against `knowledge/_tmp/rulings-pre-295-I2.json`, then a full `--write` played end to end against
a SECOND copy (`rulings-rehearse-I2.json`) and checked — `636 → 637`, id `s295-D3`, the 636-record
prefix `==`, `_README` `==`, key order `==` — **before** the live write. Both copies live in the
gitignored `knowledge/_tmp/`.

⚠ **AN EVIDENCE POINTER WAS REFUSED BEFORE IT WAS WRITTEN, BY MEASUREMENT.** The obvious pointer
for a boot-reading ruling is `notes/_GAUGE-LOG.md`. **Measured:** `_governs.ROLLING_FILES` is
`['GOOD-MORNING.md', '_LIVE-STATE.md', 'notes/_GAUGE-LOG.md']` — the gauge log **ROLLS**, so under
`R6`/`s177-D1` it is INVALID ON ARRIVAL as an evidence pointer. The four pointers used instead:
the lane file, the two #295 subreports, and `knowledge/_gauge_tokens.py`.

---

## THE ENACTMENT — ONE LITERAL, AND THE THREE PLACES THAT WOULD HAVE DISAGREED WITH IT

**`knowledge/_gauge_tokens.py:325`, the one line:**

```
BOOT_CEILING_TK = 70_000       # `s241-D1`, SHRINK-ONLY. Measured first post-diet boot: 69,092.
⇒
BOOT_CEILING_TK = 72_768       # `s295-D3`, SHRINK-ONLY from here. Dave's word, n=1, #295 turn 1.
                               # (was 70_000 — `s241-D1`, first post-diet boot 69,092 at #241.)
```

**The provenance comment is BY ADDITION, 23 lines above it**, and it says both halves out loud:
where 70,000 came from (`s240-D2` defined the ceiling as the first post-#240-diet boot, `s241-D1`
fixed its value from the 69,092 reading at #241, it held 54 sessions, and the nine breach readings
were taken against it and stay over it forever in the append-only log) and where 72,768 comes from
(`s295-D3`, the first cold boot after Dave switched boot features off at the #293 worker seat,
`_checkin.py` FILL 89,108 real / 2 turns at the #295 conductor's seat, **n=1 published as n=1**).
**His hedge is in the comment verbatim**, with the recommendation it answered.

### THE GREP — WHAT ELSE SAYS 70,000, AND WHAT WAS AND WAS NOT TOUCHED

Swept `--include=*.py --include=*.sh --include=*.yml --include=*.yaml --include=*.js` for
`70_000` / `70,000` / `70000`. **Three live-code hits mattered. Fourteen were records and are
NOT edited.**

| where | what | verdict |
|---|---|---|
| `knowledge/_gauge_tokens.py:325` | **the literal** | ⬛ **CHANGED — the ruling** |
| `knowledge/_gauge_tokens.py:307` | prose comment *"one boot over 70,000 fails by name"* | ⬛ **CHANGED to name `BOOT_CEILING_TK`** — a prose copy of a moving number is the copy-chain class this module refuses elsewhere; the correction says so in place |
| `knowledge/_gauge_tokens.py:837` | **selftest arm E pinned `("BOOT_CEILING_TK", 70_000)`** | ⬛ **CHANGED — it would have gone RED on the true tree** |
| `knowledge/_capture_gate.py:4035` | comment *"`s241-D1` fixes its value at 70,000"* | ⬛ **CORRECTED BY ADDITION, original sentence kept** — it is the true history of the number the breach readings were graded against |
| `knowledge/_capture_gate.py:7004` | fixture `"job 70,000 est"` | ✅ **NOT TOUCHED — not the ceiling.** It is a pre-flight JOB estimate in a `#58` crash-regression fixture. A blind sweep would have corrupted a mutation-tested fixture |
| `knowledge/_release/_gen_pack_manifest.py` ×3 | `1700000000` | ✅ **NOT TOUCHED** — epoch timestamps, matched only because `70000` is a substring |
| `notes/_lanes/283…287/**` ×14 | banner/carry/ops scripts of past wraps | ✅ **NOT TOUCHED — these are RECORDS.** They are past sessions' rendered testimony about the ceiling AS IT THEN STOOD, and editing them would rewrite history to agree with today |

⛔ **`_capture_gate.py` READS THE CONSTANT, IT DOES NOT COPY IT.** Measured: `gt.BOOT_CEILING_TK`
is read at check time at `:4896`, `:9793`, `:10106`; the fail text at `:5029`/`:10143` interpolates
it. **No second copy of the value exists in the gate**, which is why one literal was enough.

### THE SELFTEST ARM THAT WOULD HAVE LIED, AND WHY IT WAS RE-PINNED RATHER THAN LOOSENED

⛔★ **`_gauge_tokens.selftest()` arm E — `"E s294-D7 re-measure published by addition; no constant
moved"` — HARD-PINNED `BOOT_CEILING_TK == 70_000`.** Left alone it would have gone red on a tree
where Dave's own ruling had been enacted correctly: **a selftest failing the truth.**

⛔ **IT WAS NOT DELETED AND NOT LOOSENED TO `is not None`.** It is **re-pinned to 72_768**, so a
seat that moves the ceiling again *without his word* trips it exactly as before — and a **second
assertion was added beside it**, because shrink-only is the half an equality check cannot see:

```
if name == "BOOT_CEILING_TK" and isinstance(got, int) and got > 72_768:
    failures.append("[E s295-D3] BOOT_CEILING_TK = … is ABOVE the re-based 72,768 —
                     SHRINK-ONLY means it may go DOWN and NEVER UP. A breach is REPORTED,
                     not absorbed by raising this line.")
```

⛔ **PROVEN ABLE TO FAIL, BY MUTATION, IN MEMORY ONLY:**

```
M1  BOOT_CEILING_TK ← 70,000 (the old literal)      → rc=1, 1 err  (the re-pin bites)
M2  BOOT_CEILING_TK ← 80,000 (raised, illegal)      → rc=1, 2 errs (the re-pin AND the direction arm)
M3  BOOT_CEILING_TK ← 60,000 (lowered, LEGAL)       → rc=1, 1 err  ★ see below
control                                              → rc=0
```

⚠★ **M3 IS A FINDING ABOUT THE ARM, PUBLISHED RATHER THAN SMOOTHED: a LEGAL shrink — exactly what
`s241-D1` and `s295-D3` both permit Dave to do — ALSO trips the equality arm.** That is inherited
from `s294-D7`'s design (it pins an exact value to prove D7 moved nothing), not introduced here.
⇒ **Consequence, stated so nobody rediscovers it at 2 a.m.: the next time Dave lowers the ceiling,
this pin must move in the SAME commit.** Loosening it to `<= 72_768` was available and **was
refused**: that would delete `s294-D7`'s "no constant moved" guarantee to buy convenience.

---

## ⛔ THE GATE — 1 → 2 → 1, EVERY READING MEASURED

| when | rehearsal reading |
|---|---|
| **at open (inherited)** | **1** — ⚠ **NOT RE-MEASURED AT THIS SEAT, DECLARED.** Taken from lane I's filed close. This lane's first `_checkin.py` run happened AFTER the inscription, so no independent before-reading exists and none is claimed |
| **after the inscription, before the re-render** | **2** — the second is `s263-D10 RULINGS PAGE STALE`, **caused by this lane** |
| **after `_render_rulings.py`** | **1** — the ceiling breach, unchanged, quoted in full at the top |

```
rehearsal [wrap-gate, early]: 1 STRUCTURAL fail(s) — fix NOW, cheap · 0 heals-at-wrap ·
367 warn(s) (was 367 at the last logged run)
```

**No gate was weakened, none was acked, and the one that remains is the one this lane's own ruling
was supposed to close and did not.**

### `notes/_RULINGS.html` — RE-RENDERED (`s263-D10`), AS THE GATE WROTE THE REMEDY

```
wrote notes/_RULINGS.html  637 rulings  162 sessions  1,155,466 bytes  sha256 bbe3860a…
FRESH _RULINGS.html matches _rulings.json sha256 bbe3860a…
```

### THE SELFTESTS RUN, AND THE ONE NOT RUN WHOLE

⛔ **`python3 knowledge/_capture_gate.py --selftest` WAS NOT RUN WHOLE** — the brief and
`_HANDOFF-145` both put it past the sandbox call wall. **The narrowest possible probe was run
instead: the three arms that actually read `BOOT_CEILING_TK`, called directly in-process.**

```
selftest_boot_delta_parse            -> []   (0 failures)
selftest_boot_ceiling_discharge      -> []   (0 failures)
selftest_boot_double_count_narrowing -> []   (0 failures)   ← lane I's new arm, still green
```

✅ **`python3 knowledge/_gauge_tokens.py --selftest` RAN WHOLE AND GREEN, in 0.20 s** — the
brief's call-wall warning belongs to `_capture_gate.py`, not to this module, and that is measured
rather than assumed. ✅ `py_compile` on both edited files.

---

## THE DOC ROW, THE CHAIN, THE COMMITS

`W-295i2`, minted through `_state.add()` before staging with a **true** close condition — the arm
refuses without one, and inventing one is the smaller cousin of inventing his ruling.

`_CHAIN.md` regenerated before the commit attempt, per the brief. ⚠ **It goes stale again the
instant the commit exists** — lane P proved that at `280e4e82` (§ FOR THE NEXT SEAT: *"the chain
was fresh in the tree that was committed and stale in the tree the commit produced, in the same
second, with no edit between"*). **Not repaired here; it is structurally unfinishable.**

<!-- COMMIT-SHAS -->

### THE LOCKS — `mv`'D, NEVER `rm`'D

⛔ **ONE WAS ALREADY STRANDED AT THE OPEN, BEFORE THIS LANE RAN ANY GIT COMMAND** — the third
consecutive session this has been measured. Every lock this lane met was moved to
`notes/_lanes/_orphan-locks/stale-index.lock-295-I2-<HHMM>`. **Nothing was `rm`'d** — this mount
refuses `unlink` (`s282-D4`).

---

## RULING-SHAPED QUESTIONS

1. ⛔★★ **THE RE-BASE DID NOT CLOSE THE BREACH, AND CLOSING IT NEEDS A REGIME BOUNDARY, NOT A
   NUMBER.** Seven readings of 74,1xx–80,871 sit over 72,768 exactly as they sat over 70,000.
   `BOOT_CEILING_FROM_SESSION` is still **241**. ⇒ **Are the post-switch-off boots a THIRD REGIME
   with their own `_FROM_SESSION` (the way the post-diet boots got one at #241), or do the old
   readings stand red forever as testimony?** Both are defensible; **neither is a seat's to pick**,
   and `s295-D3` says so in its own text rather than quietly moving the boundary.
2. ⛔ **THE HEDGE NEEDS A MECHANISM OR IT IS DECORATION.** He said *"possibly"*. The ruling records
   it and says the next cold boots are the test — but **nothing in the code knows that 72,768 is
   provisional.** ⇒ Does a re-base on `n=1` get a **confirmation clause** (e.g. re-open for his
   word if the next two cold boots disagree by more than the nineteen-token spread the previous
   setup showed), or is a hedge always prose only?
3. ⚠ **SEVEN OR NINE?** The brief's evidence names nine post-diet readings over 70,000; the gate
   names seven and excludes `#293 74,204` and `#294 74,656`. **Both are in the record now and
   neither was rewritten.** ⇒ Is the gate's sample set short two readings, or is the brief's list
   counting figures the parser correctly declines? **A ruling built on a count nobody reconciled
   is the `s295-D1` `post-mortem #N:` defect again, one session later.**
4. ⚠ **AN EXACT-VALUE PIN AND A SHRINK-ONLY LITERAL ARE IN TENSION, FOREVER.** `s294-D7`'s arm E
   pins the ceiling to an exact number; `s295-D3` guarantees Dave may lower it whenever he likes.
   **Every future legal shrink is a two-file edit or a red selftest.** ⇒ Should arm E test
   *direction* (`<= the last ruled value`) with the ruled value carried in a named constant, or is
   the friction the point?

### counts

- rulings inscribed **1** · store **636 → 637** · records reformatted **0** · pure append proven
  by object comparison of all 636 predecessors
- constants moved **1** — `BOOT_CEILING_TK` 70,000 → 72,768, **on Dave's word and nothing else**
- gate: **1 → 2 → 1** structural fails (all three readings measured) · warns **367**, unchanged ·
  gates weakened **0** · gates acked **0**
- live-code sites corrected **4** (1 literal, 2 comments, 1 selftest pin) · records left alone **14**
- selftest assertions added **1** (the shrink-only direction arm) · **mutation probes 3, all bit**
- validators run **5**: `_inscribe_ruling --dry-run` + rehearsal `--write` on copies ·
  `_gauge_tokens --selftest` (whole, green) · three gate arms direct (green) ·
  `_render_rulings --check` (stale → regenerated → fresh) · `_checkin --window 200000 --no-block`
- ⛔ **`_capture_gate.py --selftest` NOT RUN WHOLE** — call wall; narrowest probe run and **declared**

### UNPROVEN, named rather than implied

1. **THE 72,768 READING ITSELF.** It is the conductor's turn-1 `_checkin.py` figure, taken at a
   seat this lane cannot re-enter. **n=1, not independently re-measured here, and the ruling says
   n=1 in its own text.**
2. **THE WHOLE CAPTURE-GATE SUITE.** Three arms were driven; the rest is CI's to ask.
3. **THAT 72,768 HOLDS.** His own word on it is *"possibly"*. **The next cold boot is the test and
   it has not happened.**

REPLAY-THESE: `python3 -c "import sys;sys.path.insert(0,'knowledge');import _gauge_tokens as g;print(g.BOOT_CEILING_TK)"` (expect **72768**) · `python3 knowledge/_gauge_tokens.py --selftest` (expect green, ~0.2 s) · `python3 -c "import json;r=json.load(open('knowledge/_rulings.json'))['rulings'];print(len(r),r[-1]['id'])"` (expect **637 s295-D3**) · `python3 knowledge/_render_rulings.py --check` (expect FRESH, sha256 `bbe3860a…`) · `python3 -c "import sys;sys.path.insert(0,'knowledge');import _capture_gate as g;print(g.selftest_boot_ceiling_discharge(), g.selftest_boot_delta_parse())"` (expect two empty lists) · `python3 knowledge/_checkin.py --window 200000 --no-block` (expect **1 STRUCTURAL fail — the CEILING BREACH, still, at 72,768**)
