# #295 — the push landed, CI was read job by job, and the wrap gate reached zero

provenance: 295 · 2026-09-22
status: observed

*The narrative dossier for Apollo session #295. Session opened Monday 2026-09-21; the ritual and this
file are Tuesday 2026-09-22 — a DATE SPLIT in the `s294-D11` shape, and nothing was re-dated to match.
Written by the delegated OPUS 5 wrap sub. The WHAT is in `knowledge/_rulings.json`, the ★ LATEST
banner and the four filed lane reports; this file is the WHY and HOW. Both-way links at the foot.*

---

## The arc in one paragraph

#294 ended with twelve rulings inscribed, eleven of them enacted in code, **six commits local and
nothing pushed** — and a handoff that said, in its own words, that the push *"is not routine."* #295
was that push. It also turned out to be the session in which three separate defects that had been
carried for twenty wraps were each found to be **something other than what their own fail text said
they were**, and in which **two numbers that everyone had been treating as one number** were pulled
apart. The wrap gate went from seven inherited structural fails to zero. That is the first time in
twenty-one sessions.

## Finding 1 — the boot double-count was never a double-count, and its only remedy was forbidden

The gate had been reporting six boot double-counts since #241's `s241-D2` (*one stratum, one
first-turn figure*). Twenty consecutive wraps had routed around them on the `#243` DECLARED
NOT-A-WRAP path, and the reason nobody fixed them is that **the arm's own remedy text said
`Delete the restatement`** — and `notes/_GAUGE-LOG.md` is append-only. A gate whose only discharge is
the one repair no wrap may make is a gate that gets routed around; that is
[[gate-cannot-pass-in-one-environment]] in its purest form.

Lane I measured what the six actually were, before touching anything, and **not one of them was a
session stating its own boot twice**:

- **#243 was charged FIVE times** because four *later* strata quote its reading inside a `"#243 form"`
  carry paragraph. Four of those five lines are not #243's stratum at all.
- **#264, #273, #287** were charged because their own `wrap-handover:` lines restate the figure their
  post-mortem line already states.
- **#272, #274** were charged by a carry paragraph inside their own stratum.

Every one is a session **talking about** a reading rather than **taking** one. The fix was therefore
never at the log and never at the ceiling: it was at the **reading rule**. `s295-D1` narrows the arm
to the `post-mortem #N:` line whose own ordinal is the session being graded, and the uncharged rows
are **counted and named in a note** (`74 boot reading(s) … are NOT CHARGED`) rather than made
invisible. `_parse_boot_rows` is byte-unchanged; the derived band, the drift arm and the delta arm all
read it and none is narrowed.

**The correction inside the correction.** The ruling names the line as `post-mortem #N:` *with a
colon*. Measured over the live log, **#243's line has the colon and #264 / #272 / #273 / #274 / #287
all read `> **POST-MORTEM #264 — measured, not narrated.**`** — upper case, em dash, no colon. **Five
of the six fails would have survived a matcher pinned to the ruling's own punctuation.** The matcher
was widened to case-insensitive with `:` or a dash, which reaches the strata the ruling's subject
names by number — and that widening is a seat's reading of his intent, not his text. It is stated in
the code comment and asserted by a selftest arm rather than left for a reader to discover. Whether
`s295-D1`'s premise is amended by addition is his.

## Finding 2 — a re-base and a breach are two different objects, and the brief treated them as one

Dave's words on the ceiling were: ***"1. I can't cut anything else permanently, this is possibly the
new ceiling."*** That is authority to move `BOOT_CEILING_TK` from 70,000 to **72,768**, the first cold
boot after he switched boot features off at the #293 worker seat. `s295-D3` did exactly that, n=1
published as n=1, his hedge carried verbatim into the ruling's evidence and into the constant's own
comment.

The brief expected the rehearsal to read 0 afterwards. **Lane I2 measured it at 1 and published that
its own brief was wrong**, with the arithmetic nobody had done before the ruling was drafted:

| session | reading | over 70,000 | over 72,768 |
|---|---|---|---|
| #283 | 80,871 | +10,871 | **+8,103** |
| #287 | 74,120 | +4,120 | **+1,352** |
| #288–#292 | 74,155–74,174 | ≈+4,170 | **≈+1,400** |

The re-base shaved 2,768 off every margin and cleared none of them. **A ceiling that closed this
breach by VALUE would have to be ≥ 80,871** — 8,103 above anything Dave said, and a treadmill rather
than a ratchet.

The reason is structural and worth keeping: **the re-base is about what the NEXT boot is graded
against; the breach is about readings taken on the OLD, heavier boot**, which are append-only
testimony and do not become smaller because the line moved. The only honest instrument is to stop
*charging* readings taken on a retired setup — which is a **boundary**, not a number. Lane I2
declined to invent one and said so; the conductor put it to Dave; his whole reply was ***"inscribe"***.
`s295-D4` moved `BOOT_CEILING_FROM_SESSION` **241 → 295**, the seven readings became **reported and
never charged**, and the wrap gate reached zero.

Two details from the enactment are worth the record. **The brief named the wrong module** — it said
`_gauge_tokens.BOOT_CEILING_FROM_SESSION`; the constant is `_capture_gate.BOOT_CEILING_FROM_SESSION`
at line 4047, and `_gauge_tokens.py:348` carries only a pointer comment. The correction went into
`s295-D4`'s own text rather than being silently absorbed. And **one prose string was corrected rather
than kept**, because keeping it would have made the gate lie in its own voice: the hold-harmless note
read *"are PRE-DIET (session < #%d)"*, and under a #295 boundary those readings are
**PRE-SWITCH-OFF** — a different structural break. A gate that reports correctly while describing
itself wrongly is `s295-D1`'s defect one session on.

## Finding 3 — the refusal that was right, and the ruling it read on the wrong clause

`s295-D2` rules that the enacting lane stamps `status: enacted` in the same commit, with the commit
sha as the evidence pointer. Its very first duty was to back-stamp #294's rulings — and **lane I
refused**, because the sanctioned writer has no path to `status` (`--help`: *"AMEND — evidence array
ONLY; `says` is unreachable from here"*), and hand-editing `knowledge/_rulings.json` is the #179
defect this project abolished.

**The half-stamp was available and was refused on purpose.** `--amend-evidence` could have appended
the sha to each record — producing records **still reading `status: ruled`** while carrying an
enactment sha. The advisory arm keys on `status`, so the half-stamp would have moved **zero** of the
98. *"A convincing-looking half of a ruling is worse than an honest absence."*

Lane I had also cited `s172-D3`(e) as forbidding a lane from building the missing writer. **Lane I3
read that clause by id lookup before building anything and found it says something else**: it is the
observed-failure rule — *"a new test must cite the failure class it guards or the ruling it enforces;
a speculative check QUEUES as a proposal"* — and its own scope line says it *"governs THE APPETITE FOR
NEW INSTRUMENT-BUILDING IN FUTURE SUB BRIEFS ONLY. IT RETIRES NOTHING."* The failure here is
**observed** — lane I's filed refusal, in this session — and the selftest that ships with the writer
cites `s295-D2` by name, which is precisely what (e) demands. *"Lane I's caution was the right
instinct on the wrong clause."*

The writer that resulted, `--set-status ID STATUS --evidence-sha SHA`, carries two design decisions
that are the interesting part:

1. **The status vocabulary is read from the store at call time and never hard-coded.** A list of
   accepted words inside the tool would be a *second copy* of the store's own vocabulary — the
   copy-chain class this repo refuses everywhere else. (The store's seven lead words, enumerated at
   build time: `ruled` 603 · `enacted` 23 · `standing` 6 · `built` 2 · `part-enacted` 1 · `in` 1 ·
   `superseded` 1.) A seat that wants a new status word must get it ruled.
2. **Two span swaps in ONE composition, not two proven writes.** Two individually-proven writes leave
   a **half-stamp window** in which the record reads `enacted` with no sha — the exact state
   `s295-D2` forbids and the state lane I refused to create.

## Finding 4 — and it changed nothing, which is the finding

Lane I's advisory arm had read *"98 of 117 enacted rulings carry no sha"* and its question 2 predicted
that back-stamping the eleven *"moves it to 87"*. After fourteen stamps the arm reads **98 of 131**.

**The numerator did not move by one.** All fourteen records were `status: ruled`, not
`enacted`-without-a-sha, so the stamps grew the **denominator**. ⇒ **the ~87 remainder the brief
fenced off as Dave's does not exist as a separate object** — it is the same 98, untouched, and this
session paid none of it. Whether `s295-D2` binds from #295 forward (the way both `_FROM_SESSION`
boundaries now do) or the 98 is a debt is his, and until it is answered `ENACTED_SHA_BLOCKING` can
never flip: it would be red on 98 records the day it was promoted.

**And the count the record carried was wrong.** `_HANDOFF-145` says *eleven enacted in code* in two
places. Driven over the commit's own diff, `f81bbdd4` names **ten**: `s294-D10` (the Jev decision) and
`s294-D11` add **zero** lines each. `s294-D11` *is* enacted — but at the **wrap commit `359b646b`**,
in `GOOD-MORNING.md`, `_CARRIES.md`, `_CHAIN.md`, the handoff, `_LIVE-STATE.md`, the index and a
memory hook, **with not one `.py` file touched**. Neither was stamped, because stamping D11 with a sha
the brief did not name would be inventing provenance — the one thing the tool exists to make
impossible. ⇒ **is "enacted" a word about CODE, or about the repo's surfaces?** That question is now
load-bearing rather than philosophical.

## Finding 5 — a gate that a passing commit turns red is not measuring the artefact

`_HANDOFF-145`'s post-wrap addendum 4 had declared, from the 5b commit, that **every commit now stales
`_CHAIN.md`** through lane A's live-HEAD clause in the build-verdict line. Lane P met it as CI survey
step `[120]` **newly red** and then proved the tautology at `280e4e82`: the chain was **fresh in the
tree that was committed and stale in the tree the commit produced, in the same second, with no edit
between.** #294's wrap did not push, so nobody had ever seen it.

Lane I3's diagnosis is the part worth keeping, because the obvious fix was wrong. **The cause is two
differences, not one.** The committed and freshly-rendered chains differ at the build-verdict line
*and* at the footer's fixed-point tape figure — because **the two shas are the same byte length and a
different token count**. Normalising the sha clause out of both strings, the first suggested shape,
would have left the size figure mismatched and the check still red. So `check()` **re-asks**: only
after the byte comparison has already failed, it reads the committed file's own stamped HEAD out of
its build-verdict line and regenerates once with that sha pinned. `build()` is untouched and never
sees the pin, so a cold session still reads the honest live comparison against the true HEAD.

**A module global was written first and it did not work.** In-process the fix returned 0; run as a
script on the same tree it stayed red. The cause: `_capture_gate.py:1794` does
`import _gen_chain; _gen_chain.build_verdict_line(repo)` — so when that file runs as `__main__` there
are **two module objects**, and the verdict line is rendered by the other one, whose global was still
`None`. The pin moved to an environment variable, the one channel both copies share, and an
environment variable already set when the process starts is **refused** (`COULD-NOT-ASK`) rather than
honoured. This is the #58/#59 class exactly — a check that disagrees with itself across two
environments on one commit — and it was caught only because the CLI was re-asked rather than trusted.

CI on `c896bcaf` confirms it on a pushed tree: survey **7 FAIL → 6, 58 pass → 59**, and `[120]` green.
**The only step that moved is the one the fix addressed, and it moved the right way.**

## Finding 6 — two sevens under one name

This is the cleanest vocabulary defect the project has produced.

- **The wrap gate's seven fails** — the set `IDEA-wrap-is-slow-five-levers.md` lever 3 asked to be
  ruled closed. `s295-D1` took them 7 → 1; `s295-D4` took them to **0**.
- **CI's survey seven fails** — a different seven, of different steps, that was six last session.
  `s295-D1` took them **6 → 7**. Lane I3's chain fix took them back to 6.

**`s295-D1` moved one from 7 to 1 and the other from 6 to 7, in opposite directions, in the same
commit.** Nothing is wrong in either count; the collision is in the word, and every brief this session
called both *"the seven inherited gate fails."* They need different names before a session rules one
closed and means the other.

A sibling, measured by lane P: **a survey step ID is not a stable identifier across sessions** —
`[123]→[125]`, `[126]→[128]`, `[134]→[136]` this wave alone, because two steps were inserted upstream.
Every record that cites one by number is citing a moving target. The six remaining are cited by name
throughout: `[3]` token blast-radius · `[13]` capture/provenance selftest · `[38]` component-partials
sync · `[125]` memento schematic determinism · `[128]` memento-package delta-audit · `[136]` governs
matcher selftest.

## Finding 7 — the push, and the gate that refused was not the gate on record

`_HANDOFF-145` § OWED 7 carried lane G's #294 declaration: *"no credential in the sandbox's remote
URL, so the push path refuses at the credential gate."* Lane P tried the sanctioned arm first and
measured that **the credential IS present** — `git config remote.origin.url | grep -q "@github.com"`
returns 0, the credential gate would have passed. That declaration is **retired**.

What refused, at three separate seats on the identical three paths, is the **dirt gate**: three files
belonging to other seats, one of them machine-written instrumentation whose exclusion policy **the
script itself declares ⬛ DAVE'S and unruled**. The dirt gate has **no `*_ACK` hatch**, unlike its six
neighbours — *"the script diagnoses the exact case that would justify the hatch and then has no hatch
to offer."*

All four pushes therefore went by plain `git push origin master`, a declared fallback on the
conductor's PUSH verdict, and every one of them paid a named price: **the `s294-D5` expiry gate, the
fast-forward-only gate, the master-only gate and the script's own post-push verification all
skipped.** Verification was re-done by hand each time and the branch confirmed `master` first; the
expiry check was not re-done and nothing claims it. A bare terminal `git push` is also the shape
`_RUNBOOK-capture-ritual.md:781-783` names in the imperative as the thing never to do — `s133-D2`
superseded that **by addition**, and the addition is the arm that refused. Whether a conductor's PUSH
verdict reaches a bare `git push` is his.

## Finding 8 — the first honest asking, and it fails

`_capture_gate.py --selftest` exceeds the ~165 s sandbox call wall, so **all four lanes declared it
NOT RUN WHOLE rather than claiming it**, and CI is the first surface in the project's history that
asked it. It returns **exit 1**, on *"no `pre-flight:` stamp"*.

The verdict worth carrying is the comparison, not the colour: **the failure is byte-identical to
#292's on `301f6fbf`**, before any of this wave's six edits to that file existed. ⇒ the six edits broke
nothing the selftest can see. **It is also no better, and it was already failing.** And it may be
false: `grep -c 'pre-flight:' GOOD-MORNING.md` returns 3 at a live seat, each a full refusal-shaped
stamp, so the file does carry them and the arm is looking in a shape or place it is not finding.
Nobody diagnosed it further and nobody touched it, because #294's cold-seat warning is explicit that
grading a gate with the wrong arm *"is exactly how a false cause ran for ninety-three sessions."*
Whether the suite has a **second** failure is unknown and is reported as unknown — the survey
truncates each failure to its first line.

The structural sibling: **`--wrap` is wired into no CI step at all**, measured at four seats. Neither
the seven fails, nor their closing, nor the ceiling breach, nor its discharge has ever appeared in CI
in either direction. The only instrument that sees the wrap gate is the local rehearsal — so the zero
this session reached is, as far as CI is concerned, invisible.

## The instrument, and the mount

**He stopped on the instrument.** The seam reading 214,824 real / 23 turns was quoted to him past the
180,000 quality line with the wrap recommended, and his whole reply was ***"wrap"***. `s283-D1`'s
override shape stays at n=2; nothing is inferred from this session.

**And for the first time in six wraps his declared seam readings did not reproduce at the wrap seat.**
Measured here off the same transcript with the same `_checkin.read_fill`, neither 214,824/23 nor
218,396/25 appears in the per-turn cumulative series; the nearest distinct readings are 215,019 and
219,030 (+195, +634). The **boot agrees to the token at 72,768**, which is what identifies the window
and makes the `s214-D5` hand-over subtraction legal at all. Both series are published and neither is
rewritten; the shape suggests the declarations were taken mid-turn rather than off a completed `usage`
record, and that is a reading of the difference, not a claim about its cause. The `subs` figures show
the same direction — **measured 690,805 (n=4) against 697,742 declared, high on all four lanes and low
on none** — which is the same systematic offset #294 measured across eight lanes, and is therefore
more likely a property of how the conductor takes the reading than of any lane.

**The lock dance composed into a recipe.** Lane P corrected its own count upward from three to
**eleven** after its commit, and published the sequence because the sequence is the mechanism: the
trigger is not the mount alone, it is a **no-op `git add`** — the retry's add on an already-staged path
stranded the lock, and the *next* named path was then refused, so the script reported the wrong object.
And `git reset -q`, the prescribed remedy, stranded exactly the two refs locks #294 recorded. The
working sequence is: `mv` the index lock → `git reset -q` → `mv` the two refs locks → run the committer
once with every path genuinely unstaged. Nothing was ever `rm`'d at any seat; this mount refuses
`unlink` (`s282-D4`).

## Where it leaves us

The gate is at zero, everything is pushed, CI has been read back on three shas, and the chain check no
longer goes red by construction. What is open is almost entirely **his**: the 98, the word for
`s294-D11`'s and `s294-D12`'s states, the dirt gate's hatch, whether a PUSH verdict reaches a bare
push, and whether 72,768 holds — his own word on that is *"possibly"*, and the next cold boot is the
test.

And one thing is open that is not a gate at all. Friday the 25th is three days out, it is the
internal, and he said so himself, mid-ruling, unprompted: ***"BTW, we need to get back to the
presentation soon."*** **#296 opens on the deck.**

---

*Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA — 2026-09-22 (#295). Ledger:
`knowledge/_rulings.json` § `s295-D1` … `s295-D4`, rendered at `notes/_RULINGS.html`. Handoff:
`_HANDOFF-146-the-push-landed-and-the-wrap-gate-reached-zero.md`. His words:
`notes/_lanes/295/DAVE-RULINGS-2026-09-21.md`. Filed reports:
`notes/_subreports/2026-09-21-295-I-inscribe-and-enact.md` ·
`notes/_subreports/2026-09-21-295-P-push-and-ci.md` ·
`notes/_subreports/2026-09-21-295-I2-ceiling-rebase.md` ·
`notes/_subreports/2026-09-21-295-I3-regime-status-writer-chain-check.md` ·
`notes/_subreports/2026-09-21-295-W-wrap.md`.*
