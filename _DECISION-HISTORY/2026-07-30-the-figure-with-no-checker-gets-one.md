# The figure with no checker gets one — and its own control found the machine that had been minting the defect

```
provenance: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367 · 2026-07-30
status: observed
```

**Session #49 · Opus solo · Dave live · "bite 3 only, then stop" by instruction.**
Spine entry: `GOOD-MORNING.md` ★ LATEST #49 · rulings + WHY: `notes/_MEMENTO-DECISIONS.md` § ★ #49.
Predecessor: `_DECISION-HISTORY/2026-07-30-the-cap-binds-the-file.md` (#48, closed open 16).

---

## 1. The job, and why it was finally doable

Open 15 was born at **#45**, homeless until **#46** copied it up by EXIT CHECK, and **blocked** on
open 16 for four sessions because nobody could say what the assertion should compare *against*.
#48 closed open 16 — the cap binds the FILE via `chain_file_tk` — which answered the blocking
question. Dave's opener priced the window at 23% of shared quota over twelve hours and picked
**bite 3 only**.

The defect, restated from #45's own probe: `_capture_gate.py`'s `SIZE_TK_RE` validates the **GM**
figure and nothing else. Every other `chain`-near-`stamp` string in the file was a test fixture.
So the one number the entire #33 read-chain cut exists to govern was the one figure in the stamp
with nothing behind it — [[gate-narrows-its-own-rule]] and [[instrument-without-a-consumer]]
meeting on a single line.

## 2. The design decision: ban PRESENCE, not drift — and the reason is a timing argument

The obvious enactment is a drift check: find the hand chain figure, compare it to `chain_file_tk`,
fail if it has moved more than `SIZE_TOLERANCE`. I did not build that, and the reason is worth
recording because it is not a preference.

**A drift check on a hand copy passes at the moment of writing.** A wrap that re-adds the figure
copies a number that is *true when it copies it* — so the check goes green for the session that
performs the retired act, and only bites the session that inherits it. That is a cap firing after
the writing, which [[gate-inside-the-growth-loop]] measured can only ever be paid in live record.
Banning presence fails the wrap that does it, while undoing it is still free — one deletion.

It also matches what is already ruled: #45 **retired** the hand copy and pointed at the generated
one in `_CHAIN.md`'s footer; #48's banner says it "MUST NEVER BE RE-ADDED". Enforcing a retirement
is not deriving-and-promoting. **What IS mine is the TIER** — `fail` rather than `warn` — and the
gate message says so in its own text, and forks it to Dave.

**The refusal still reports the measurement.** A gate that only forbids teaches the next session
nothing about where the truth lives, so the message carries the live `chain_file_tk` figure, the
drift, and the footer's address. And when `chain_file_tk` refuses, the ban still stands and the
message says UNMEASURED with the reason — never the slice, which is ~400 tape low and is open 16's
defect reintroduced as an error path.

## 3. Scope: the ban stops at the stamp, and a control holds it there

`GOOD-MORNING.md:488` really does carry `the CHAIN only (**~4.1K tape**` — inside a dated stratum,
as a **true** record of what one session's boot cost. A repo-wide ban would forge a defect out of
correct history. So the check reads the `size:` stamp only, and the suite carries a **scope control**
that asserts the same string, in a stratum, passes clean. Report the measurement, never prescribe
the region.

The regex was not invented. Every form it must catch was pulled from `git log` on `GOOD-MORNING.md`:
`chain **4.4K tape` (#44) · `chain 3.56K tape` (#39) · `chain 34.7K tk` (#30, legacy unit) ·
`_CHAIN.md **4.6K tape`. It was tested against four must-miss strings first — including the live
stamp's own `417-tape` wrapper prose and `chain 4,065 → 4,400` — before a line of the check existed.

## 4. ★★ THE FINDING — the positive control caught the machine that had been minting the defect

House rule is that the positive control leads: prove the check does not fire on everything, or it
becomes noise and is routed around within a wrap. Mine fired. So did the scope control. Both on the
**green** fixture.

The cause: **`_gm_fixture`, the generator behind every entry in `BUDGET_FIXTURES`, had been stamping
`chain {tk}K tape` into its default stamp since #34** — and stamping it *wrong*, putting the GM
figure under a `chain` label. So for fifteen sessions the green control that licenses every budget
fixture in this file had been asserting that a stamp carrying a hand chain figure is **correct**.

★ **The lesson is about the shape of #45's probe, not about #45.** #45 surveyed occurrences and
found three fixture sites — `:1844`, `:1846`, `:2050` — and concluded they were all fixtures and
therefore harmless. The **generator** that mints them on every default fixture was not among them,
because it does not contain the string; it *composes* it at runtime from an f-string. A survey of
occurrences cannot see the thing producing the occurrences. Sibling of
[[unmatched-grep-is-not-an-absence]] one level up: a complete list of matches is not a complete list
of sources.

★ And the mechanism that found it was **the control, not my reading**. I read `_gm_fixture` before
editing it and did not notice; the bite noticed within seconds of first running. This is the third
consecutive session where a control caught something care did not.

Two expected-fail fixtures (`BUDGET_FIXTURES` "STALE" and "no K") also said `chain`. The new ban
would not have turned them red — they already expect a fail — it would have made them fail for a
reason **their own names do not state**, which is how a suite quietly stops meaning what it says.
Both re-labelled `corpus`.

## 5. Verification, and what I did NOT run

- **Gate selftest: 0 failures**, rc=0. `_gen_chain --selftest` green · `--check` **FRESH**.
- **CONTROL 1 (the bite bites).** Neuter `CHAIN_STAMP_RE` to a never-matching pattern ⇒
  `selftest_growth` returns **4 open-15 failures**; restore ⇒ **0**. A green suite is not a proof.
- **CONTROL 2 (scope holds).** The real GM:488 string, injected into a fixture's **stratum**,
  produces **0** chain-ban fails — while the regex still matches the string in isolation, asserted
  in the same bite so the control cannot quietly stop controlling anything.
- **Live repo, `--wrap`:** no chain-figure fail. Two fails, both **pre-existing and declared** —
  strata stack and `ds-022`, the standing consequence of 2f being blocked on open 7.

⛔ **I DID NOT RUN THE 75-STEP BUILD, and the reason is a falsified premise, not a shortcut.**
#48 recorded "steps 1–73 consume ~40s". **It did not reproduce**: steps **1–25 alone** exceeded the
44s sandbox call cap. Rather than binary-search the segment size at ~40s a call on a 23%-quota day,
I verified by **call graph**, which is a stronger argument for a change confined to one file:

- `check_budgets`, `_gm_fixture`, `BUDGET_FIXTURES`, `CHAIN_STAMP_RE` — **grepped repo-wide**; the
  only consumer outside `_capture_gate.py` is `_gm_move.py:462`, which reuses `_gm_fixture`.
- So `_gm_move.py --selftest` was run, not import-smoked: **green**.
- Build steps that invoke the changed file — 51 (`_capture_gate.py`), 52 (`--selftest`), 174/176/178
  (`_gen_chain.py`, `--check`, `--selftest`) — **all rc=0**.
- The four other importers (`_gm_usage`, `_search_core`, `_gen_lanes`, `_gm_move`) — selftests rc=0.

★ **Say it plainly: "every consumer of the changed surfaces was run" is MY composition and a
different claim from "the build is green."** I have not made the second claim.

## 6. Errors

**1, self-caught, and it cost nothing.** I reached for `git stash push` to compare fail-sets
before/after my edit, on a question the record had **already answered** — the chain's own banner
says `ds-022` FAILS every wrap while 2f is blocked. The stash did not take (a stranded
`.git/index.lock`), the working tree was never disturbed, and the comparison was unnecessary in the
first place. ★ The near-miss is the familiar one: I went to *measure* a thing the record already
*stated*, and the safest version of that mistake is still a mistake, because it put a
history-rewriting command next to a dirty tree to answer a question retrieval had answered.
[[feedback-verify-before-asking]] has a mirror — **verify against the record before reaching for a
probe that can damage it.**

## 7. A perishable number that moved

#48's `size:` line says the chain "LANDED ~1% OVER WARN". **Measured now: `_CHAIN.md` is 5,159 tape
against the 4,917 warn — +242, or +4.9%.** Not a contradiction of #48 (its own later edits are in
that figure) but the same shape #44 named: a claim about a moving number, stamped once and read
forever. It is ADVISORY and I did not act on it; it is reported so the next session prices from a
measurement rather than from a banner.

## 8. Resolved state, and what is still open

**Closed:** **open 15**, after four sessions — born #45, homeless until #46, blocked until #48.
`guards: SIZE_TK_RE` is now true rather than aspirational.

**Dave's, unruled, untouched by this window:** open 21 (stale generated reports) · 22 (does the
never-reached-the-plan class earn a mechanism?) · 20 (b)/(c) · 19 · 7 (whose block is why `ds-022`
failed again, **declared, not forged** — the strata stack is now **TEN**) · 13 · 14 · 17 · 18 ·
9/10/11/12.

**Mine, offered and declined-as-unproven by #48, still unclaimed:** the `size:` stamp line is 685
tape, the fattest in the chain. Trimming it honestly needs each claim's live home located first.
Not attempted here — Dave's instruction was bite 3 only.

**New, and it is a tier question rather than a defect:** the chain-figure ban ships at **FAIL**.
That tier is agent-picked. The gate says so in its own message; the engine never derives-and-promotes.
