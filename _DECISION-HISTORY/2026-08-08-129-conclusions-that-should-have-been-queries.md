# #129 — conclusions that should have been queries

```
provenance: 129 · 2026-08-08
status: observed
```

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST DELTA #129 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #129
(rulings `s129-D1`…`s129-D5`) · **Banner:** `GOOD-MORNING.md` ★ LATEST #129 · **Measurements:**
`notes/_GAUGE-LOG.md` § `#### 2026-08-08 #129`.
Both-way links per `_DECISION-HISTORY/README.md`.

---

## Why this dossier exists

Five rulings landed in one window. Four of them are the *same sentence* wearing four costumes, and the
fifth is Dave naming the sentence out loud. The ledger holds the WHAT — the constants, the arms, the ids.
This file holds the WHY: how a session that opened to do one thing discovered that thing was already done,
what it found while looking, and the 5-whys that turned four separate repairs into one standing hunt.

---

## Finding 1 — the session opened on work that was already finished, twice over

The brief was dream-pass item ①, owed from #127 and carried into #128. The first act of the window was to
check `git log` rather than to trust the residual that named it. Three commits, all timestamped that
morning, changed the plan:

- `6836c5a` (07:57) — **the dream pass had already run**, producing `notes/_dream/2026-08-08-proposals.md`
  with three proposals.
- `d74552e` (08:20) and `ed4ce3a` (09:08) — a #128 session had then **enacted all six of Dave's
  2026-08-02 dream-pass rulings**, which is exactly what proposal P1 existed to argue for.

So **P1 was overtaken by events within two hours of being written.** P1's evidence was not wrong when it
was gathered; it had simply stopped being true, and nothing in the proposals file could notice. That is
worth pausing on, because it is the same shape as everything else in this session: *a proposal is a
conclusion about repo state with no re-checker attached.*

The correction was cheap because the premise was verified against a source with a different clock — `git
log`, not the carried residual — which is the standing lesson from the stale-mount seam. Had the session
executed the brief as written, it would have spent a window re-enacting six enacted rulings and reported
success.

What survived of the pass: **P2 and P3**, both in reduced form, both verified rather than re-asserted. P2's
age-bracket half turned out to be **already ruled and already enacted** into
`_RUNBOOK-capture-ritual.md` § 2c by #128 — and #129's own residual is the first to use the format. Its
other half stands: the ordinal that counts the rolls (*"FIFTEENTH roll"*) is still hand-typed prose that
nothing reads. P3 predicted this file's siblings being swept into an unrelated commit by `git add -A`;
the probe found the mechanism **gone** — `_git_commit.sh:257` now stages only explicitly named paths,
d0802-P5 enacted at #128 — leaving a smaller, real residue: `notes/_dream/` is still outside the gate glob
by ruling (A-D4), so nothing checks the lane's output; it simply can no longer be swept in by accident.

★ Note the discipline that mattered more than either answer: **both were re-measured at the wrap instead of
being copied forward.** A carry that is re-stated without being re-checked is how an item survives fifteen
rolls unchanged.

---

## Finding 2 — the boot floor, re-based at last, and the parser that could not see its own evidence

`s129-D1`. The published floor of 75,899 had been contradicted by **seven consecutive measurements** taken
in the same unit and at the same moment — #111 55,733 · #113 54,038 · #117 54,807 · #118 54,404 · #125
53,681 · #126 53,997 · #127 54,375, n=7, spread 2,052. Every one of those sessions recorded the datapoint
and every one of them declined to act on it, correctly: *a measurement disagreeing with a published constant
is evidence, not authority*, and the re-base was Dave's to take. He took it.

`BOOT_FIRSTTURN_TK` moved **65,400 → 54,859**, `BOOT_FIRSTTURN_ERR` **1,400 → 1,178**; the published floor
moves **81,335 → 70,794** and the room for job + wrap **118,665 → 129,206**. Nothing else moved — the
wrap-open line at 150,929 and the 160,000 / 200,000 / 256,000 walls are untouched, because a cheaper boot
moves the ROOM and never the LINE.

Two things about this ruling are worth inscribing beyond the number:

**(a) The ruled figure is deliberately not the best fit.** Dave picked **54,859** — the n=3 post-break mean
he was shown at #117 — while the n=7 mean is **54,434**. Both are now in `_gauge_tokens.py` on purpose. The
ruled figure is a RULING; the n=7 mean is EVIDENCE. A future session that "tidies" the constant to 54,434
by hand will be visibly doing the thing this project keeps having to un-do, and the two numbers sitting
side by side are what make that visible.

**(b) A second defect surfaced while enacting, and it was the same class as the ruling.**
`_capture_gate._parse_boot_samples()` matched **case-sensitively**, and every post-mortem since #125 opens
its sentence with the word: *"**Boot 53,681 real**"*. Those lines did not parse — and, worse, **did not
refuse**. They were silently counted as absent. Three sessions of the very evidence the re-base rests on
were invisible to the gate that grades the constant. The fix is one flag (`re.I`, applied to both the match
and the refusal probe); parsed samples went **28 → 31**.

That fix moves the gate's own window, which makes the shape dangerous: a remedy landing in the same pass as
the thing it grades. So **both readings were published rather than one**: with the old parser and the new
constant the gate **FAILS** (window mean 56,078, delta +1,219 — the window still straddles the #109/#111
structural break); with the fixed parser it **PASSES** (mean 54,325, delta −533). The constant was not
fitted to the window; 54,859 clears the bar by 645. Nobody has to take the enacting sub's word for which
change did the work, which is the only honest way to land a fix and its own test together.

**And an honest hole, declared:** *no #129 boot sample exists.* The conductor could not read its own
first-turn `message.usage` this session. The eighth datapoint is **owed** and nothing was substituted for
it — a re-base session with no measurement of its own is an irony, but an invented number would be worse.

---

## Finding 3 — the browser-download contradiction, and why both subs were right about what they saw

Owed since #126, re-owed at #127, re-owed again at #128. Two #125 subs had produced **opposite first-hand
readings** of the same operation: one saw the playwright browser download **succeed** and then throw
`EPERM … rmdir '__dirlock'`; the other saw it **TLS-blocked on all three CDNs**. Three sessions declined to
adjudicate, and the record correctly refused to flatten them — but three consecutive declines is not a
quiet win for either sub.

#129 settled it the only way it could be settled: **by running it, first-hand, as the conductor.** The
download **works** — exit 0, a 340M `chromium_headless_shell-1234` landed at `/var/tmp/pw-browsers-129`.
TLS-blocked did not reproduce.

The interesting part is not the verdict; it is that **neither sub was hallucinating.** Both were reading
the environment and calling it the network:

- **ENOSPC on the 98%-full shared `/sessions` volume presents as *"Download failure, code=1"*.** The
  remedy is a browser path outside the shared volume (`PLAYWRIGHT_BROWSERS_PATH=/var/tmp/…`) and a
  `df -h $HOME` before anyone blames a CDN.
- **`/tmp` is SHARED ACROSS SESSIONS.** This bit #129's own first probe: a foreign session's stale
  `pwdl.log` was read as this run's evidence. It was caught only because the ENOSPC diff did not fit the
  log's story. The remedy is unique log paths under `$HOME`.

`_RUNBOOK-render-verify.md` was amended **by addition** — a dated 2026-08-08 stratum at the head — and no
dated stratum was edited or deleted. The file already held both #125 readings stratified by date; quoting
one stratum is not reading the file, and overwriting one would have destroyed the evidence that made this
adjudication checkable.

★ **The sandbox environment is therefore a medium of the same class as prose and comments:** a fence about
the environment, true when written, with nothing that re-checks it.

---

## Finding 4 — generate, declare, and ASCII: three small rulings that are one sentence

- **`s129-D2` — generate, don't re-stamp.** `_build_all.py`'s state-contrast caveat had gone false a
  **third** time by #127, and #127 deliberately left it un-corrected as evidence rather than hand-fixing it
  a fourth. Dave ruled GENERATE. It is now `state_contrast_caveat()`, with selftest arm (d); `--selftest`
  PASS at 102 steps.
- **`s129-D3` — declare, don't refuse.** The 15 un-hit-testable boxes become **named holes**. Arms went
  19 → 25, rc=0; the audit regenerated with holes 15 → 14. ★ **That one-hole delta was attributed rather
  than claimed** — a `git show HEAD` control run three times puts it on the browser build, not on
  `s129-D3`'s emit condition, whose logic is unchanged apart from the added `reason`. The four REAL
  failures are byte-identical and still red; nothing was waived.
- **`s129-D4` — ASCII in the machine store, glyphs in the prose.** `_rulings.json` now holds 0 non-ASCII
  with 15 glyphs mapped, round-tripped and byte-verified before writing so the diff carries the semantic
  change and nothing else. `_governs --selftest` **30 → 30, diff empty** — the store changed and the
  verdict did not, which is the assertion worth making. Scope is the machine store only; prose surfaces
  keep their glyphs by the same ruling.

Read separately these are three chores. Read together they are three different answers to one question:
*what re-checks this?* Generate it, or declare the hole, or normalise the store so the checker can read it.

---

## Finding 5 — the 5-whys, and Dave's sentence

Late in the window the conductor ran a 5-whys on why the same class kept recurring. The chain, compressed:

1. Why did the caveat go false three times? Because it was typed.
2. Why was typing it acceptable? Because it was true when typed.
3. Why did nothing catch it going false? Because nothing re-reads a comment.
4. Why is that the norm? Because the record stores the *answer*, which is cheap to write and free to read.
5. **Why is that wrong? Because the answer has an expiry date and the record does not carry one.**

⇒ **The root: the system stores CONCLUSIONS where it should store GENERATORS.**

Dave ratified it mid-turn, in his own words, and this is `s129-D5`:

> *"verified is a property of a MOMENT, not the artefact; every inscribed conclusion is DEBT with three
> options: generate / named re-checker / expiry."*

The media on the record now number **seven**, and #129 added two of them:

| # | medium | where it was caught |
|---|---|---|
| 1 | **prose** | #125 — *"the 75"*, disk said 98 |
| 2 | **a comment** | #125 — an exemption's reason, disproven on its own date |
| 3 | **a return value** | #125 — `parse()` fabricating `{"ratio":1}` |
| 4 | **a pointer** | #126 — `_governs.py` red |
| 5 | **the record of a defect itself** | #127 — `_LIVE-STATE.md:457`, false in both halves |
| 6 | **a commit subject** | **#129** — both #128 commits, Finding 6 |
| 7 | **the sandbox environment** | **#129** — the playwright fence, Finding 3 |

Enacted minimally and by addition: the standing hunt **"Conclusions that could be queries"** in
`.claude/agents/dreamer.md`; recorded at `notes/_MEMENTO-DECISIONS.md` § `s129-D5` and in
`knowledge/_rulings.json` (77 ids). **No gate, no threshold and no expiry term was set** — the three
options are Dave's vocabulary for choosing a remedy per item, not a policy a wrap may apply on his behalf.

---

## Finding 6 — both #128 commits certify the wrong session (reported, not repaired)

`git log --format='%h %s'` shows `d74552e` and `ed4ce3a` — #128's two enactment commits — both carrying the
subject *"after #127 2026-08-07 — ✅ THE SCHEMATIC v2 LANDED…"*, which is **#127's banner text**. Meanwhile
`d74552e`'s **own message body asserts** *"this message's first line deliberately begins with '#128'"*.

That claim is **false as committed**, and there are exactly two candidate causes, neither eliminated:

- **(a)** the msgfile's first line was genuinely wrong, in which case the #124 subject assert did exactly
  its job and **faithfully certified a wrong line** — sound gate, bad input; or
- **(b)** the assert did not bite on this path, in which case every subject since #124 is uncertified.

The difference matters enormously and cannot be settled by staring at the log. **#129 did not diagnose it
further and did not repair it** — it is Dave's, and it is #130's opening item. A repair improvised at a wrap
is exactly how an unenforced convention becomes a fact.

★ The class is this session's own ruling, sitting in the git log: the body's claim about its own first line
was a **conclusion inscribed at write time with nothing re-checking it at commit time**.

⚠ **A live regression check ran at this very wrap.** #129's msgfile first line begins `#129 2026-08-08 — `,
and the post-commit subject was verified equal to it. So whatever failed at #128 did not recur at #129.
**That is one datapoint, not a diagnosis** — an invariant that passes cannot discriminate a reversal.

---

## What the conductor got wrong

Three, all caught in-window, all left visible rather than tidied:

1. **The first download probe read a foreign session's `/tmp` log as its own evidence.** Caught only
   because the ENOSPC diff did not fit. This is the finding from Finding 3 biting its own investigation.
2. **The first write of `s129-D5` into `_rulings.json` used an invented schema** — no `ruled`/`by`/`says`/
   `governs`, and a string `evidence` that the validator iterated character by character. `_governs`
   failures went **30 → 67**. It was caught **by running the gate**, not by reading the diff, and rewritten
   to the store's real shape, back to 30. A store has a grammar; guessing it produces a file that looks
   right and parses wrong.
3. **The enactment sub first reported "TLS-blocked on 3 CDNs"** because it ran `playwright install`
   *without opening the render runbook*. Corrected in-window; **the wrong reading is left visible in its
   records**, because a report that quietly matches the final answer is not a record of how the answer
   was reached.

---

## Resolved state, and what is still open

**Closed by this session:** the boot-floor re-base (`s129-D1`) · generate-vs-re-stamp (`s129-D2`) ·
declare-vs-refuse on the 15 boxes (`s129-D3`) · glyphs-vs-ASCII in the store (`s129-D4`) · the
browser-download contradiction, owed since #126 · the overdue dream pass (closed at #128, discovered here).

**Green, conductor-replayed, not sub testimony:** `_build_all.py --selftest` PASS 102 steps ·
`_validate_state_contrast.py --selftest` rc=0, 25 arms · `_governs.py --selftest` 30 · `_rulings.json`
0 non-ASCII, 77 ids · boot constant 54,859 live.

**Red, honestly:** `_capture_gate.py --selftest` rc=1 — the 30 pointer entries, Dave's, because filling
class B/C means asserting what he ruled · the state-contrast gate, red on the four REAL failures, Dave's.

**Open, and each is someone's named call:** the #128 wrong-subject autopsy (Dave's, new) · the 30 pointer
entries (Dave's) · the four REAL contrast failures (Dave's) · dream-pass P2's hand-typed ordinal ·
dream-pass P3's ungated `notes/_dream/` glob (A-D4) · and the carried set, on its fifteenth roll, now
written with ages so that a cold reader can tell a hand-off from a fossil.

**Unmeasured, declared:** #129 has no boot sample and no fill series at all. It is a hole in the throttle
dataset with a post-mortem attached, which is the honest shape rather than a tidy one.
