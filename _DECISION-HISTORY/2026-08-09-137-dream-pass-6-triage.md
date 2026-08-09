# #137 — dream pass 6 triage: the instruments were dirtying the tree they measure

```
provenance: wrap-sub #137 · 2026-08-09
status: ruled (pointer: knowledge/_rulings.json § s137-D1)
```

Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#137) · Banner: `GOOD-MORNING.md` ★ LATEST #137 ·
Ledger: `knowledge/_rulings.json` (`s137-D1`) · Source artefact:
`notes/_dream/2026-08-09-proposals.md` (commit `0219075`) · Predecessor arc:
`_DECISION-HISTORY/2026-08-09-136-three-axis-model.md`.

⚠ **Written by the wrap sub from the conductor's session facts and from first-hand re-runs of the
measurements against the repo** — the drives quoted below were re-executed by this sub where they
were cheap to re-execute (`_governs.selftest()`, the `--file` probe, the round-trip assertion), and
are marked as such. The `s137-D1` three-way drive is the conductor's, reported not re-run;
declared, not laundered as first-hand.

---

## Why this session existed

It did not exist for a reason anyone chose. **Dream pass 6 fired on its scheduled Sunday 07:10 slot
and committed `0219075`** — 273 lines, `notes/_dream/2026-08-09-proposals.md`, five floated
proposals P1–P5 — and #137 opened to find the largest piece of new work in the tree waiting for it.

**It was found by a boot-time `git log`, not by any gate.** #136's wrap banner was generated at
15:40 on the same day; a commit made at 07:10 that morning is invisible to it, because a wrap banner
describes what its own session did. So the #137 residual list — the thing the session is supposed to
read to know what is waiting — did not contain the largest item waiting.

Dave named the remedy in one sentence: *"at wrap, `git log` since boot; any foreign commit gets
named in the banner — that closes this class permanently. A scheduled lane that commits mid-session
will happen again."* **It is FLOATED, not ruled** — recorded in `_LIVE-STATE.md` § OPEN, deliberately
not enacted this session, however obviously good it is. Enacting a wrap step because it is obviously
good is how a delegated wrap ends up ruling its own principal's open item.

---

## Finding 1 — the premises were re-verified before anything was decided, and that was the cheap half

The dreamer runs cold and **has no shell**. Every one of its five proposals rests on a premise about
the repo that it could not itself check. All five were re-verified first-hand at #137 against the
working tree, before any of them was discussed as a candidate. **All five hold.**

That is the boring result, and it is the one worth writing down: the pass was worth reading precisely
because its premises survived contact. The interesting failure is in Finding 4, where the dreamer's
*checked-clear* item did not survive.

---

## Finding 2 — `s137-D1`: the verification instruments were dirtying the tree they verify

**The defect, in its own terms.** `_capture_gate.py --wrap` and `_checkin.py` both append to
`notes/_REHEARSAL-LOG.jsonl`, which is a **tracked** file. `_git_commit.sh` runs the gate at `:153/157`
and stages at `:300–316`, so a run *inside* the script is captured and **anything run after the commit
is not**. Since `s133-D2` the `--push` path asserts a clean tree at `:38` — so *verifying a commit
after making it* left the tree dirty and refused the very push `s133-D2` exists to allow.

**Confirmed first-hand at #137, not inherited:** this session's own opening `_checkin.py` left
` M notes/_REHEARSAL-LOG.jsonl` in `git status` before any other work had been done.

**The archaeology is the part that stings.** The remedy had been priced ONCE, at #125 — *"move the
log write ahead of the staging seam, or exclude the log from the clean-tree assertion"* — and then
appeared in **no carry list for eleven sessions**. Greps of `_LIVE-STATE.md` and `GOOD-MORNING.md`
for `REHEARSAL-LOG` returned only the #104 unattributed-path line. It took a scheduled dream pass,
running cold with no memory of any of those eleven sessions, to put it back on the board.

**Dave's ruling**, picked over two named alternatives (move the append after the staging seam; stop
tracking the log): the clean-tree assertion excludes **exactly one named file**, written out in full
so the exclusion cannot silently widen. Enacted at `knowledge/_git_commit.sh:43-44`. The refusal now
also **prints the dirty paths**, which it did not before — a gate that refuses without naming what it
refused on is a gate you learn to ignore.

**Driven three ways on the artefact's own bytes**, because a ruling about a guard that is asserted
rather than driven is a preference:

| leg | setup | result |
|---|---|---|
| A | real tree, real dirt | rc=1, lists `_LIVE-STATE.md` + `_git_commit.sh` + 3 untracked font files, **does not list the log** |
| B | scratch tree, only the log dirty | rc=0 |
| C | mutation: log **and** one other file dirty | rc=1 — **exclusion proven NARROW** |

`bash -n` clean. ⚠ **NOT DRIVEN: the end-to-end `--push`, because driving it means pushing, and that
needs Dave's word.** UNPROVEN BY CHOICE, declared here and in the ledger rather than quietly omitted.

---

## Finding 3 — the false green, and why it is the method finding of the session

**The first test of `s137-D1` passed and had tested nothing.**

Inserting a 6-line comment block shifted the line numbers. The probe had been written as
`sed -n '40,41p'` and the enacted guard now lived at `43,44` — so it extracted two **comment** lines
and `eval`'d them. **`eval` of comments exits 0.** It printed `GUARD PASSED`.

It was caught in-window, owned to Dave, and redone against the real line numbers. Nothing false was
reported. But the shape is the one this project keeps meeting: *a green that cannot fail is an
assertion* — [[green-tests-cannot-see-scope]]. The specific lesson to carry is narrower and more
useful than the slogan: **an offset probe re-anchors itself the moment you edit the file, and the
edit that shifts it is usually the edit you are testing.** Address the guard by content, not by line
number, or re-derive the line numbers after the write.

⚠ **Second-order, same session:** twice, `$?` was read **after a pipe** and returned the *pipe's*
exit code rather than the command's. That is the #130 defect, recurring, in a session that was
explicitly hunting for false greens.

---

## Finding 4 — the artefact recording the all-clear is what falsifies it

Dream pass 6's item **(cc1)** states that a whole-tree grep for `github_pat_` / `ghp_…` returns
**0 files**, and files it as checked-clear for future passes.

**Re-run at #137, the same grep returns two files:** `notes/_dream/2026-08-09-proposals.md` (lines
156, 205, 249) — and `knowledge/_memento-index.json`, which indexed it.

✅ **There is no leak.** Every hit is the string inside backticks in the dreamer's own prose *about*
the grep. cc1's **verdict** — no credential material in the repo — is re-verified and **STANDS**;
only its count is stale.

The finding is the structure, not the count: **the document that records the all-clear is the thing
that breaks it, and the retrieval index then republishes the false line to anyone who asks.** It is
USE vs MENTION with no scope — the same defect as [[gate-must-quote-what-it-forbids]]. Any credential
gate written to this grep will now fire forever on a file containing no credential, and the honest
response to a permanently-red gate is to stop reading it. A secret scanner has to exclude quoted
mentions, or match the token *shape* rather than the prefix.

---

## Finding 5 — fontconfig writes into the repo it scans, and two remedies collided to put it there

Three untracked files, all stamped **2026-08-08 22:57** — #136's render-verify run — sat in
`knowledge/assets/fonts/_desktop/TTF/`: `.uuid` (36 bytes, one UUID), `.uuid.LCK` and
`.uuid.TMP-NpSPVs` (2 bytes each: an orphaned lock and an atomic-write temp from a process that died
before cleanup). Fontconfig writes a `.uuid` marker into a scanned font directory to give it a stable
cache identity.

**Cleaned at #137** — all three moved to `_to_delete/_fontconfig_strays/`; the tree now has zero
untracked paths and the 10 tracked `.ttf` files were never touched.

**The cause is two of this project's own fixes colliding.** The OLD render recipe copied the TTFs to
`~/.fonts`, so fontconfig scribbled *outside* the repo. #136's ENOSPC fix removed that copy to save
disk and pointed `FONTCONFIG_FILE`'s `<dir>` **straight at the repo's TTF directory**
(`_RUNBOOK-render-verify.md:42,46`) — which saved the disk and moved fontconfig's writes *inside the
tree*, where they trip `s133-D2`'s clean-tree gate.

★ **This is the same class as `s137-D1`: an instrument writing into the tree it measures. Two
independent instances in one session makes it a class, not a coincidence.**

**Dave's instruction, verbatim:** *"Just make sure its tidy and fixed, no patches or hacks solve it
permanently please."* The permanent fix is designed and priced in `_LIVE-STATE.md` § OPEN — a
`/var/tmp` **symlink farm** (`ln -s` each repo `.ttf` into `/var/tmp/fonts-<session>/`), which costs
~0 bytes and therefore **preserves the ENOSPC constraint that forced #136's change rather than
reopening it**. It is **NOT enacted and NOT proven**: the proof is a real render run (~4 sandbox
calls) confirming the face still renders at 1180+480 and that no `.uuid*` appears under
`knowledge/assets/` afterwards. #137 had **18,402 real** of job room at the decision point, which does
not fit a render lane plus a wrap. Recorded rather than rushed. ⛔ And explicitly **not** gitignored —
an ignore rule hides an instrument that is still writing where it must not.

---

## Finding 6 — found by the wrap: `_capture_gate.py --selftest` had been red for three sessions

This one was not in the session's plan; the wrap found it while checking its own preconditions.

`python3 knowledge/_capture_gate.py --selftest` exits **rc=1** with **1,739** failures, all of the
form *"ruling `s137-D1` points at `p` which does not exist"*. `knowledge/_rulings.json` stores
`evidence` — and, from #136, `governs` — as a **string** on six records, where `_governs.py:294`
iterates the field as a **list of pointers**. Iterating a string yields characters, so the checker
walked ratified prose one letter at a time. 92 of 98 records use lists: the checker is right, the
data is wrong.

★ **The real defect is that nothing runs the check at wrap.** `_capture_gate.py --wrap` does not call
`_governs.selftest()`. Its only consumer is `--selftest`, wired into `_build_all.py`, which is
sandbox-impossible (~49s against the ~45s call kill) and therefore never runs here.
[[instrument-without-a-consumer]] — and three consecutive wraps committed over a red gate that none of
them could see.

⚠ **Attributed with a control rather than assumed:** the selftest is red against **HEAD's**
`_rulings.json` as well, so **#135 introduced the class**; #136 and #137 widened it. This wrap did not
cause it and did not inherit a clean gate either.

**Repaired by addition — nothing trimmed, no ratified byte changed.** Every string field was wrapped
in a single-element list, and `s137-D1`'s real path `knowledge/_git_commit.sh` was **prepended** to
its `governs` list. **1,739 → 7.** The prepend was **driven both directions**, because a trigger index
that cannot trigger is the one failure the file exists to prevent:
`_governs.py --file knowledge/_git_commit.sh` surfaced **only `d0802-P5`** before, and **`d0802-P5` +
`s137-D1`** after.

⬛ **The 7 residual failures were deliberately left.** Every one is prose in an `evidence` field where
a resolvable pointer is required — `s135-D4`'s is a real path made unresolvable by its own
parenthetical; `s135-D3`'s is `chat #135; …`, not a path at all. Clearing them means **trimming
ratified ruling records on five inherited entries**, and *add-never-trim* outranks a green. The file's
own `_README` already says which way that repair should go: *"THIS FILE IS A POINTER INDEX, NEVER A
SECOND COPY OF CANON."*

⛔ **And the durable half:** repairing six records repairs six records. **Nothing parses
`_rulings.json` in its consumer's grammar** — no check asserts at write time that `evidence`/`governs`
are lists of resolvable pointers, which is why a malformed record shipped three times running
([[no-gate-parses-the-artefact]]). A wrap-mode call to `_governs.selftest()` would have caught all
three the day they landed. It is one line — and it is Dave's to license, because it converts a
currently-silent condition into a blocking one.

---

## Finding 7 — the serializer guard fired, and that is the sixth time

The first attempt to write `_rulings.json` used `ensure_ascii=False`. The round-trip check **refused
before writing**: the file stores em-dashes escaped, so every such line would have been silently
rewritten and the diff would have been unreadable.

Held ×6 now. The measured recipe is three knobs and all three matter:
`json.dumps(d, indent=1)` · `ensure_ascii` **left at its default** · **no trailing newline** ·
and the assertion `json.dumps(json.loads(raw), indent=1) == raw` run on the **unchanged** file
*before* any edit. This wrap ran that assertion first and it passed byte-identical at 136,663 bytes;
only then was the shape repair applied.

---

## What is resolved, and what is still open

**Resolved:** `s137-D1`, ruled and enacted and driven. The fontconfig strays, cleaned. The
`_rulings.json` field shape, repaired by addition. The false green, caught and redone.

**Open, and none of it is this wrap's:**

- **Dream pass 6 P1, P3, P4, P5** — all still Dave's, all unruled. Only P2 became `s137-D1`.
- **The fontconfig permanent fix** — designed and priced, not enacted, not proven. Needs a real
  render run. ⛔ Not to be closed by a gitignore.
- **The wrap-step candidate** (`git log` since boot; foreign commits named in the banner) — Dave's
  words, **floated, not ruled**.
- **The 7 residual `_governs` pointers**, plus the missing write-time parser for `_rulings.json`.
- **Three readbacks still owed and untouched this session:** clause-A copy refinement (#136,
  floated) · #67-D2 reconciliation (Dave said "cool", not ruled) · mono no-border extension (carried
  since #134, age 2).
- **The 16 tier-map rows** — controller built at #136, still awaiting Dave's eye.

---

*Both-way links: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#137) and § OPEN (four entries born #137) ·
`GOOD-MORNING.md` ★ LATEST #137 · `knowledge/_rulings.json` § `s137-D1` ·
`notes/_dream/2026-08-09-proposals.md` (`0219075`) · `notes/_GAUGE-LOG.md` § #137.*
