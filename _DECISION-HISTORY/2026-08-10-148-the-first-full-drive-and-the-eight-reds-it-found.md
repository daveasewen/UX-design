# #148 — the first full 110-step drive, and the eight reds it found

provenance: #148 · 2026-08-10
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #148 · ledger: `knowledge/_rulings.json` § `s148-D1` ·
banner: `GOOD-MORNING.md` ★ LATEST #148. This dossier holds the WHY and HOW; the terse records hold
the WHAT. Authored by the delegated OPUS wrap sub from the conductor's relayed record; every claim
below is either verified first-hand by this sub against the artefact, or attributed to the conductor
and marked as relayed. This sub ruled nothing.*

## The arc

#147 closed with one item at the top of the residual and a reason for it that had just been paid in
full: **the 110-step build had never been driven end to end in this sandbox**, and #147 had measured
what that costs — 245 stale RAG values sitting quietly behind a runner that had been dead since #139.
The item was not "run the build for tidiness". It was "the instrument that re-checks everything has
never once been shown to run".

#148 drove it. The drive needed a runner that could survive the sandbox, so the session built one
first; along the way it found and fixed a third instance of the dead-runner family, and closed a
pointer-form gap Dave ruled on directly. Three findings, and the order matters — each one existed
because the previous one made it visible.

## Finding 1 — `s148-D1`: the ledger could not describe its own evidence

`_governs.py` is the gate over `_rulings.json`'s evidence strings. It knew two legal pointer shapes,
and neither of them was the shape the record had actually been using since #135: an annotated
evidence line naming a path inline, and a plain `chat #<n>` reference to where Dave said the words.
The consequence was not a false green — it was worse in a quieter way. Sessions #142 through #147 had
rulings whose evidence fields were **pure prose**, because prose was the only form that would pass,
and prose is the one form no instrument can ever chase.

Dave was given a three-option set and picked **"Fix both now"** — the predicate and the extraction,
not one then the other. Enacted the same window:

- `is_chat_pointer` (`knowledge/_governs.py:110`) makes `chat #<n>` a legal pointer form, with
  selftest clause **6g** biting in both directions — a synthetic positive must pass, and named
  negatives must fail. A predicate that only ever sees true cannot discriminate.
- `PATHISH_RE` (`:107`) extracts path tokens from the annotated dialect, requiring both a dotted
  extension **and** a slash. Clause **6h** bites on three shapes the regex must *not* claim: prose
  with no pointer, an id like `s142-D1` (no slash), and a token address in braces. The legacy
  fast-path is preserved, so nothing previously green moved — that was a design constraint, not a
  happy accident.
- `:369` carries the one line that keeps the two forms from colliding:
  `is_anchor_pointer(e) and not is_chat_pointer(e)` — *the chat form is legal, never an anchor.*

Then the backfill, and this is the part with a discipline attached. `_rulings.json` was amended
**textually**: `s142-D1` (+5 fields), `s143-D1` (+3), `s146-D1` (+2), `s147-D1` (+3), `s147-D2` (+3),
plus five pure-prose evidence strings rewritten into `chat #<n>` form (`s140-D1`, `s140-D2`,
`s141-D1`). 108 → 109 entries, `s148-D1` itself last. Untouched entries were asserted parse-equal —
a serializer round-trip would have reformatted a hand-formatted file and buried the real diff in
noise. Verified by this sub: 109 entries parse, `s148-D1` last, `_governs.py --selftest` reports
*"all bites green"*.

## Finding 2 — a runner that can be driven in pieces without ever lying about it

The 110-step drive could not run as one call: the sandbox reaps anything crossing a tool-call
boundary, and the build needs ~49s against a ~45s wall. The obvious shape — run it in chunks — has an
obvious failure mode, and it is the failure mode this project keeps paying for: **a partial pass that
prints a green verdict.**

So `--range` / `--resume` was built with the refusal first (`knowledge/_build_all.py:791` onward).
State lives at `/var/tmp/_build_all_state.json` (the root fs is 95% full — `/var/tmp` by runbook) and
carries three things across calls: coverage, HEAD, and the **accumulated gate rc**. The verdict is
REFUSED unless coverage is exactly `1..110`, contiguous, at one unchanged HEAD. A chunk that skips a
step is refused; a chunk run after HEAD moves is refused; garbage `--range` is refused. Selftest arm
**(e)** bites each clause with its own mutation control.

The point is structural: a partial run **cannot** print green. It prints *"NO VERDICT until coverage
reaches 110"* and tells you to `--resume`. That is the [[a-crash-is-not-a-fail]] standard applied to
a runner rather than a parser — fail loud and named, never quietly incomplete.

## Finding 3 — the drive itself, and the eight reds

Composed across **6 chunks**, and the verdict verbatim:

> `(composed pass: coverage 1-110 contiguous at HEAD 9524f0189, gate rc carried across chunks)`
> `❌ build gate failed`

**Eight GATE reds:** step 30 text/icon contrast · 36 token-ramp AUTO-TOKENS sync · 45 snippet gate ·
51 showroom sync · 63 state-contrast · 82 dataviz · 105 package delta-audit · 106 delta-audit
selftest.

Three things about that result deserve to survive in the record.

**It supersedes #62's "75/110 green".** That figure was never a full drive; it was a composition of
partial evidence read as a total. The first real measurement disagrees with it, and the first real
measurement wins.

**Step 94's own output was UNCAPTURED** — the tail was cut. It is declared, not assumed green. A step
whose output nobody read is not a step that passed; writing it down as green would be exactly the
confident false inscription this project's whole record discipline exists to prevent.

**⚠ And the finding inside the finding, unruled and left open:** steps **105 and 106 fail with the
IDENTICAL message**. 106 is the *selftest* for 105's delta-audit. If a selftest cannot fail
independently of its subject, it is not testing the subject — it is echoing it
[[mutation-tests-the-clause-not-the-feature]]. Whether that is what is happening here is not
established, and this wrap does not establish it. It goes to #149 as a named question inside the
triage item, and the remedies for all eight reds are Dave's/the conductor's.

## Finding 4 — the dead-runner family, instance 3

`knowledge/_test_git_commit.py` was supposed to be testing the RULED #128/`s130-D3` commit script.
It was scoring **0 of 12 arms** — the tests had drifted out from under the script they name, and
nothing noticed, because nothing ran them. Re-aligned to the actual ruled script: **22/22 arms,
including 3 biting mutation arms**. The script itself was left untouched — the tests were wrong, not
the subject. Verified by this sub: *"ALL GREEN — 22 arms (incl. 3 mutation controls)"*.

That is the third instance of one family in two sessions: #147's 245 stale RAG values behind the dead
`_build_all.py`, #148's step-11 block, and now a test file that could not have failed because nobody
was asking it. The class is [[instrument-without-a-consumer]], and the recurring question it wants
asked is never "is this gate correct?" but **"does the runner run?"**

## What it cost, and the honest gaps

The step-14→64 lane needed playwright, installed session-scoped to `/var/tmp` (984M of browsers; root
fs now 95%, ~505M free — verified by this sub at wrap). ⚠ **The sandbox is fresh next session, so this
is a NOTE, not an asset** — #149 pays for it again if it needs it.

Gauge: boot **54,153** real, inside the 54,859 ±1,178 band — a datapoint, never corrected into the
constant. Check-ins ran at the opener **and inside two lanes**, which is the discipline
[[checkin-at-the-ends-cannot-catch-the-lane]] asks for and which #147 missed. The wrap opened at FILL
**141,708**, UNDER the stop line 150,929. Delegation: 2 Opus build subs plus this Opus wrap sub, with
the binding budget (FILL) named before each.

⚠ **What this sub could NOT re-verify:** the drive's composed verdict itself. `/var/tmp/_build_all_state.json`
no longer exists at wrap time, and a re-drive is six chunks — far outside a wrap's budget. The verdict
above is the conductor's, quoted verbatim as relayed, and it is corroborated only by HEAD `9524f01`
matching the HEAD the verdict names. That is a real limit on this record and it is written here rather
than smoothed over.

## Where it stands

`s148-D1` is ruled and enacted. The chunked runner exists and refuses to lie. The full drive has been
run for the first time, and it is **red in eight places** — which is the point of running it. Nothing
about those eight was ruled here; the triage is #149's top item, and the 105/106 independence question
sits inside it.
