# #261 — six dashboard components, a driver scope closed, and an opening premise that was false

provenance: 261 · 2026-09-09
status: observed

> ⚠ **WRAP DATE SPLIT — SESSION OPENED 2026-09-08 EVENING, RITUAL AND COMMIT 2026-09-09.** The third
> occurrence of the #241/#248 shape. ⛔ **Nothing was re-dated to match the commit.** The R and D3
> lanes' commits carry 2026-09-08 22:11–22:44; every later commit carries 2026-09-09. The nine
> `s261-D*` rulings are dated **2026-09-09**, the session's COMMIT date, and each carries in its own
> `evidence` the sentence that says so — the hour of each ruling was not recorded at this seat, so
> the date is not a claim about the hour.

Both-way links: `_LIVE-STATE.md` § ⏱ LATEST DELTA #261 · `GOOD-MORNING.md` § ★ LATEST #261 ·
`knowledge/_rulings.json` § `s261-D1`…`s261-D9` · `_CARRIES.md` § `## residual → #262`.

---

## 1 — The session opened on a premise that was false, and the opener proved it rather than inheriting it

#260's handoff titled the chat *"the push — sixteen commits including a shipped release stand local"*.
The opener ran `git ls-remote` and found **origin at `7647aaf`**, which is exactly where #260's own
ritual commit landed — so the sixteen commits were not unpushed at all; the chain title was stale.

★ **The lesson is the one this repo keeps re-earning and did not have to pay for again: a repo-state
claim is verified against `git log` / a real remote read, never against a banner** — the standing
line in the chain header. What it cost here was one command. What it would have cost is a session
opened on a job that did not exist.

⚠ **And the carry survives its own correction, in a corrected form.** The push is still owed and is
still Dave's (`s133-D2`) — it is just **37 commits** now, not sixteen, because #261 added them.

## 2 — The day's shape: a nine-lane design wave under one sentence of scope

Dave's opener scoped v1.0.9 in his own words — *"we need to work on some of the components that we'll
be using for dashboards… ideate… pick up some backlog items"*, then *"I also want to tackle the nav
and footer design"* (`s261-D1`). That is a **scope**, not a specification, and it is why the wave was
seated as ideation lanes rather than as build tickets: nothing downstream could be written as an
acceptance criterion because the criterion was going to be **his eye**.

Two lanes ran the evening before the wave — **R** (his rulings page) and **D3** (the driver scope
#260 owed) — and seven ran the next morning: **K** KPI tile · **G** grid header · **F** filter
toolbar · **N** nav family · **Ft** footer · **L** legend · **M** the six mechanical carries, with
**C** on the collated core requests and **V** verifying the whole wave cold.

★ **The wave was then REVIEWED, and the review is the actual product of the day.** Dave came back on
five of the six components in his own sentences, and each one became a revision lane the same
morning: K2/K3, G2/G3, F2, N2, Ft2. **Six of his eight review rulings are corrections of things a
lane chose and he did not want** — the original KPI text layout, the spark line's end dot, the
column-header end bars, the odd black edges, the smaller segmented control, the top-nav's selected
background, the tab bar's non-island form. ⇒ **the lanes' taste was the thing under test, and it
lost more often than it won.** That is not a defect in the wave; it is what an ideation wave is for.

## 3 — The correction he made to his own record

`s261-D7` carries a sentence no gate could ever have produced: *"I ruled that entire lock-up was
mutually exclusive, I've changed my mind about the menu button."*

The 2026-06-30 tab-bar sign-off row in `knowledge/_REVIEW-SIGNOFF.md` put **Menu in the exclusive
group**. That row has stood for seventy days. It is **not rewritten** — supersession discipline says
the old text stays verbatim and the correction is written beside it — so the row now carries a struck
clause naming `s261-D7`, and the same word closes the **ISLANDS marked for REVISIT** flag the row has
also carried since the day it was written, because restoring the original segmented island *is* the
answer to the revisit.

★ **The general shape: the record's job is to make a reversal cheap to make and impossible to hide.**
A record that could only be appended to would have made him argue with his own past ruling; a record
that could be edited would have made the reversal invisible. Struck-with-a-receipt is the only form
that does both.

## 4 — D3: the fail-open venues were PROVED red, not assumed

`s260-D3` made driven receipts the gate for engine-drawn charts, and #260's wrap declared the
**scope** of that driver unfinished: dv-004 was measured on one page, butterfly-v's baseline join was
provable and ungated, `dv-016`/`dv-017`/`dv-009`/`line-011` were vacuous on a canvas, and
`requiredAria` passed on a JS string literal.

The lane did the thing this repo has learned to insist on and did it **first**: it built
`knowledge/_tests/chart-engine/_probe_fail_open.py`, which copies a shipped snippet, mutates its
inlined engine so the **rendered DOM** breaks the rule, proves the break in Chromium, then runs the
gate over the copy. **All six venues were GREEN before the fix and RED after it** — the premise was
measured rather than believed [[mutation-tests-the-clause-not-the-feature]].

The closing matrix reads **86 driven / 81 static / 48 n-a / 0 unanswered**, and receipts are bound to
`self_sha256`. ⬛ **One finding is ruling-shaped and is NOT a defect the lane could fix:
`requiredDeclarations` is not a live gate at all** — a fifth venue of [[no-gate-parses-the-artefact]],
handed to Dave rather than quietly wired.

## 5 — V found what parallel lanes do to each other, and it was attribution, not loss

The verifier drove eight gates green on the integrated tree and confirmed the two reds
(`_validate_kg`'s PROMOTE edge, `_validate_type_composites` at 1083/88) are **INHERITED** — driven on
a worktree at `7647aaf` to prove it, and type-composites actually **improved** (base 1087/90).

Five mechanical claims were driven and then **mutated**, every mutation restored with
`git show HEAD:<path> >`. ⛔ **`git checkout` was never used** — the #253 lesson, where two lanes
wiped each other with it.

★ **The cross-lane finding: `_git_commit.sh --reconciled` cross-stages parallel lanes.** `0903bb6`
carries Ft's subject and 26 of **K's** files; `5691d09` carries K's subject and three other lanes'
`_state.json` rows. **Nothing was lost** — every lane's meta, snippet and showroom page resolves at
HEAD — but the history misattributes, and a reader reconstructing who built what from `git log` would
be wrong. ⇒ **serial commits only until that is fixed**, and it is carried.

## 6 — C corrected a count the previous wrap had typed

#260's delta said **seven** collated core requests. C found **eleven**: five landed (C1–C5), five
deferred, one already done. ⚠ **The number in a handoff is a claim like any other**, and this one was
under by four.

C's second finding is the more interesting one and it is **ruling-shaped, recorded, not acted on**:
`s260-D1`'s `shared` exclusion means `_validate_behaviour` drops the engine core from the member page
sum outright (`w not in shared`), so **engine growth is currently FREE against `PAGE_BYTES` as the
gate measures it** — Chart-combo read 34,209 before the lane's +470 bytes of engine and 34,209 after,
and it *could not have moved*. The browser still loads every byte. ⇒ **the 607 bytes of headroom the
brief priced were never at risk, and the budget the ruling protects is now measuring something
slightly different from what it is understood to measure.** Dave's.

## 7 — The rulings page, built and then scoped in the same session

Lane R built the carried item four sessions old: a generator, not a page —
`knowledge/_render_rulings.py` → `notes/_RULINGS.html`, 408 rulings, filterable, self-contained, with
`--check` for freshness. Built as a generator precisely so it cannot rot.

Dave's response was not what four sessions of carrying it had assumed: *"what do I do with this doc? …
this is a lot and will impede our progress."*

★ **`s261-D9` is therefore a SCOPE, not a retirement.** The page is **reference** — a surface to look
a ruling *up* in — and never a reading list; only weight-bearing rulings are surfaced to him. ⇒ the
thing that was owed was not the page. It was **an answer to "which of these still has weight"**, and
building the complete surface made that question visible by answering the wrong one first.
⚠ This is the same finding as [[decide-fast-dave-is-the-bottleneck]] arriving from a new direction:
**his reading time is the scarce resource, and a complete artefact spends it.**

## 8 — What is still open, and why none of it was decided here

⬛ **Eleven lane recommendations were DEFAULTED BY THE CONDUCTOR and are carried as PROPOSED, never
inscribed** — the delta glyph ink seat, group-row by type, disabled-column alpha, adopting
`data-apollo-filter-*`, the 1400px collapse, keeping the Tab-bar name, retiring the doormat, the 44px
legend seat, `data-dv-controls` as contract-only, `--check` as a wrap gate, and retiring the aria arm.
A lane's recommendation that a conductor defaults to is **a decision that was made without him**, and
writing it into the ledger would make it look like his. It is not.

⬛ **Three weight-bearing questions were PUT to him and are UNANSWERED**: whether the tile affordance
is a link or a button; the 24px dense floor against *"44 everywhere"*; and the nav current-location
colour in Supercharge dark. ⬛ **Plus the Stat card arrow seat** — `s261-D4` answered the arrow
question for the KPI tile and the same question on Stat card was never asked.

★ **The reason they are listed rather than resolved is the do-not-rule discipline**
[[sub-ruled-daves-open-item-110]]: a wrap that answers an open question of Dave's has not tidied the
record, it has forged a ruling.

## Resolved state at the close

Six dashboard components landed and were reviewed; five were revised on his words the same morning.
Nine rulings inscribed `s261-D1`…`s261-D9`. The driver scope `s260-D3` owed is **closed**. v1.0.9 is
**not cut** — nothing was bumped or baked, and that is a state rather than a plan. **37 commits stand
local and unpushed, and the push is his.**
