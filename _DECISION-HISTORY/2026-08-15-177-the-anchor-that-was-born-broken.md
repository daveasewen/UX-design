# #177 — the dream-pass disposition, and the anchor that was born broken

```
provenance: s177 · 2026-08-15
status: ruled — knowledge/_rulings.json § s177-D1
```

*Spine entries: `GOOD-MORNING.md` ★ LATEST #177 · `_LIVE-STATE.md` ⏱ LATEST DELTA #177.
Ledger: `knowledge/_rulings.json` § `s177-D1` (157 → 158).
Both-way: those entries cite this session; this dossier cites them.*

⚠ **THE SESSION IS NOT ABOUT ITS OWN TITLE, AND THAT IS WRITTEN DOWN FIRST.** #177 opened as
*"the token-fork ledger baseline is red and unruled"*. The ledger was never touched. At the wrap
decision Dave said, verbatim, ***"okey lets wrap and defer to the next session"*** — so the namesake
is **deferred by his explicit word** and is the **top residual item for #178, his**. A session whose
title and content diverge is normal here (the rename beat exists for exactly that); a session whose
title implies work that was silently *not* done is how a stale premise gets inherited, which is why
this paragraph is at the top rather than in the residual.

---

## Why the dream pass got ruled in one sitting

Dream-pass 7 had already run before this session (commit `69fba90`, a scheduled fire a day early —
Sat 08:13 against the ruled Sun 07:10; declared in the lane row, not reconciled). It left **four
floated proposals and zero rulings**, because a scheduled unattended pass cannot rule.

The conductor reviewed all four in full, then gave **one recommendation with its externalities
stated** rather than four separate asks. Dave's ruling came back in one line:

> *"I'll go with your recommendation, be careful I don't wa[n]t it to break other parts of the system"*

That second clause is the same fence as `s172-D3`'s — his standing worry is **blast radius**, not
scope. It is why every enactment below is by **addition** or by a **textual, byte-verified** edit,
and why P1 was deferred rather than taken along with the rest.

**The disposition, as ruled:**

| proposal | disposition |
|---|---|
| **P1** — fold the four STANDING CARRY items, delete the two bare ordinals | **DEFERRED** — gated on a liveness check of all four items first |
| **P2** — a required `boot reads:` field in the wrap-sub brief | **PROMOTED + ENACTED** |
| **P3** — three stale boot figures in the memory corpus | **PROMOTED + ENACTED** |
| **P4a** — `_governs.py` skips anchors on superseded rulings | **PROMOTED + ENACTED, mutation-proven** |
| **P4b** — retire `s171-D1`'s born-broken evidence anchor | **DEFERRED at the ruling, then SIGNED and ENACTED the same session** |

**P1's deferral is the interesting one.** The proposal was to fold four long-carried items into a
fenced STANDING CARRY block. The objection that carried the day: **fold a zombie into a fenced list
and it gains fence-protected immortality.** The liveness check has to happen *before* the fold, not
after — otherwise the fold is the thing that makes the check never happen.

---

## P2 — the field that measures the conductor, and its first live drive

The measured problem: the conductor's `GOOD-MORNING.md` boot-read is the one **repeatedly-measured
~26K process cost** in the record (#173, #175). At #176 it became **unmeasurable** — nothing in the
brief template required the conductor to declare what it opened, so the wrap could only carry the
item **UNMEASURED**, which reads identically to "clean"
[[unrun-search-indistinguishable-from-absent-record]].

The remedy is prose, not machinery: one required line in every wrap-sub brief.

```
boot reads: <files the conductor opened at boot, or NONE>
```

**A declared gap passes; a silent one fails.** A brief missing the line is a template violation the
wrap sub *can* see and must name in its report. The expiry alternative — strike the item after it
reads UNMEASURED twice more — was **REJECTED at ruling**, on the ground that expiring an unmeasured
cost rewards the silence.

★ **This wrap is the field's first live drive, and it worked.** The brief carried:
`boot reads: _CHAIN.md (head, targeted bash reads) — GOOD-MORNING.md was NOT opened`. So the item
that was UNMEASURED at #176 is **measured at #177**, and the answer is that the overspend **did not
recur**. That is a check earning its place on its first run, which is rarer than it should be.

---

## P3 — three numbers that had frozen

Three boot figures in the memory corpus had gone stale, in two different ways: **descriptions** that
quoted a number instead of naming its source, and **frozen arithmetic** that would silently be wrong
the next time the constant moved. The fix took option **(c) — form, not number**: the descriptions
now point at `knowledge/_gauge_tokens.py` (read the file, never a hook figure) and the arithmetic is
written as a **formula**.

The consequence stated plainly at the proposal, and worth keeping: this is the **third** re-base
(#109 → `s129-D1` → `s171-D1`). A fourth will rot any figure left in prose. Form-not-number is the
only shape of the three that survives it.

A **memory compaction pass** ran alongside: `MEMORY.md` **22.0K → 18.2K**, detail relocated to
`hook-overflow-2026-08-15.md`, **11 settled entries** to `MEMORY-ARCHIVE.md`.

⚠ **Memory lives outside the repo.** There is no diff to point at, and no gate can see it. The fact
is recorded here and in the spine because the repo is the record and memory is the accelerator
[[memory-md-is-in-the-mount]].

---

## P4a — a gate that was failing on rulings that no longer apply

`_governs.py --selftest` had been carrying anchor failures on **superseded** rulings — entries whose
evidence pointers were correct when written and became unresolvable when the ruling they belong to
was superseded. Re-pointing them would be an edit to ratified record. Leaving them makes the selftest
a number nobody can read.

The enacted shape: `_governs.py` **skips anchor resolution on a superseded ruling, and prints that it
skipped** (sections 5 and 6a). `s129-D1` gained `superseded_by: s171-D1` by textual insert.

**The skip prints on purpose.** A silent skip is a free pass — the same shape as `ABSENT` vs `HOLE`
in the gauge log: a check that goes quiet when it declines to look cannot be told apart from one that
looked and passed.

**Mutation proof, one level, per `s172-D3`(c):** a **live** ruling was mislabelled superseded in the
working file; the print fired, the fail count moved, and the file was restored **byte-identically**
(`cmp`-verified). The check can fail, and it was proved once — not re-proved by a second instrument.

**Machinery price:** ~16 instrument lines in `_governs.py`, **0 feature lines elsewhere**.

---

## P4b — the anchor that was never going to resolve

`s171-D1`'s `evidence[0]` read:

> `notes/_GAUGE-LOG.md#boot-drift DECLARED #170 - series 55,337 / 55,309 / 56,170 / 56,326 / 56,527 / 56,693`

It had failed for **six consecutive sessions**, and each session read the failure as **rot** — a
pointer that used to work and had drifted. It never worked. The target line in `_GAUGE-LOG.md`
separates its series with **`·`**, not `` / ``, and carries no `- series` fragment. The anchor was
**born broken**: it was written to describe a line that did not exist in that form on the day it was
written.

★ **The general form, and the reason it is worth a section:** *a pointer that has never resolved and
a pointer that has rotted look identical from the failure side.* Six sessions each spent a moment
deciding it was rot, and none of them checked the target. The distinguishing evidence — the target
line's actual shape — was one grep away the whole time.

The remedy is **retirement, not repair**. Repointing it would invent provenance the entry never had.
The replacement is a **chat-form retirement note that preserves the original string verbatim**, so
the record still shows exactly what was claimed and why it could not hold. Dave signed it later the
same session: ***"okay do P4b"***.

⚠ **One conductor error, caught before it hardened.** The first draft of that note falsely claimed
`commit 6d5db13` sat in the entry's remaining evidence. It did not. Caught and fixed **before** the
inscription landed — which is the only kind of catch that is cheap.

**And the standing rule that came out of it, which is the durable half of P4:**

> **An evidence pointer into a file the capture ritual ROLLS** — `GOOD-MORNING.md` banners,
> `notes/_GAUGE-LOG.md` strata, `_LIVE-STATE.md` deltas — **is invalid on arrival.** Point at the
> commit or the chat; those do not roll.

An enforcement check for that rule was **QUEUED, not built** — `s172-D3`(e): a new instrument is
never built in the same breath as the finding that motivates it.

---

## The count that moved, and the rc that lied

`_governs.py --selftest` went **14 → 10 fails** across the session: `s129-D1`'s two false reds
retired by P4a, `s171-D1`'s two by P4b.

⛔ **The remaining 10 are not ours to fix.** They are the `s175`/`s176` evidence-format nits sitting
on **ratified record**. Repairing them is an edit to text Dave ratified, and it is his call.

**The finding underneath:** the dream-pass report had recorded *"14 FAILs, rc=0"*. The fail count was
right; **the rc was wrong.** The source returns `1 if fails else 0` (~line 529), so rc was **1**. The
report's zero came from reading `$?` **after a pipe** — the pipeline's status, not the script's. Same
class as the #174 friction-9 catch, and the correction is inscribed at
`notes/_dream/2026-08-15-proposals.md` § Method rather than only being noticed here.

⚠ **A second, smaller wart, declared rather than smoothed:** a control `git stash` misfired
mid-verification (the sandbox lock wart). That datapoint is **declared VOID**. Nothing was lost —
the content was verified by other means — but a datapoint taken from a misfired control is not a
datapoint, and calling it one is how a measurement becomes a fact.

---

## What was ruled outside the repo

Dave amended a standing memory rule the same session: the **#153 no-Sonnet-subs** rule now permits
**Sonnet when VERY appropriate**, routed per `MODEL-ROUTING.md`. ⛔ **Inscription work stays Opus+.**
Recorded here because memory is not the record — the repo is.

---

## Resolved state, and what is still open

**Resolved:** `s177-D1` inscribed and parse-verified (`_rulings.json` 157 → 158, textual tail
insert). P2, P3, P4a and P4b all enacted, P4a mutation-proven. The `_governs` false-red count is down
by four and every one of those four is retired for a stated reason rather than repointed.

**Open, and the order they matter in:**

1. ⬛ **The token-fork ledger baseline** — deferred by Dave's explicit word to #178. Top item, his.
2. ⚠ **P1** — the STANDING CARRY fold, gated on the four-item liveness check.
3. ⬛ **The 10 `_governs` evidence-format fails** — ratified record, Dave's.
4. ⚙ **The quota crank-up window** (~08-16/17, his word at #176) — ask at the #178 opener.

**And the session's own honest number:** FILL at wrap-open was **196,684** against a stop line of
**150,929** — an **overrun of ~45.8K**, declared, not smoothed. The wrap opened at Dave's word
immediately after the overrun was measured and reported to him. Boot came in at **57,430 real**
against the `s171-D1` band ceiling of **57,007** — **~423 above**, a datapoint left outside its band
rather than corrected into it, and not used to re-base anything.
