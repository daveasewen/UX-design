# Worker receipt — the {17}-literal sweep — 2026-07-29 (#39 window, worker lane)

```
provenance: worker-17-literal-sweep · 2026-07-29
status: observed
```

**Lane:** `worker-17-literal-sweep` · **Role: WORKER.** No git — a conductor reconciles and commits.
**Brief:** none written. Dave's opener, verbatim: *"Okay. Let's just start picking off some small
things to try and make some progress."* followed by *"I want your role to be worker"* and
*"have you written anything? can you leave receipts if you have"*.
**Model:** Opus 5 (`claude-opus-5`, per session env). **Stamp:** 2026-07-29 (sandbox `date`).
**Target:** `GOOD-MORNING.md` §C·4 — *"⚠ THE `{17}`-LITERAL CLASS … a selftest reporting a number it
does not compute; instance fixed, **siblings UNSWEPT**"* [born #35 · until: swept or ruled otherwise].

---

## ⚠ Context gauge — STATED, THEN CORRECTED. Read the correction, not the number.

At the time I reported it I said **"~37,400 tape / ~58,755 bill / ~29 pts — Green on the measured
half."** The tape figure is measured and stands. **The band does not.**

`~29 pts` divides by `DEFAULT_WINDOW = 200_000`. **I did not verify that denominator**, and the
worker lane one file over — `notes/_receipts/2026-07-29-context-degradation-worker.md`, which I found
only while looking up *this* receipt's format — had already declined to name a band for exactly that
reason: Anthropic's published window for Opus 5 is **1M**, which would put the same tape at **~7.5%**.
Three bands apart, same session.

**So: tape ~37,400 measured (disk half). Band ⛔ UNSTATED — the denominator is unset.** Naming
🟢 GREEN off an unverified constant is the [[measuring-tool-must-not-guess]] failure, *UNKNOWN never
defaulted*, and I committed it in prose before catching it here. **Of the 37,400, ~10,200 is #37's
boot figures inherited rather than re-measured by me, and the harness half is unreachable (`ds-025`).**

⇒ **This is a second, independent session arriving at the same finding, one lane apart, hours apart.**
It bears on Dave's open **#2** (ds-025's remedy) and on open **#5** (that lane's 339-line note, still
unread). Surfaced, not promoted — a floated item is not authority.

---

## What was actually done

| # | File | Was | Now | Live-wrong? |
|---|---|---|---|---|
| 1 | `knowledge/_gen_lanes.py:250` | literal `19 bites` in an f-string | `{len(ran)}`, incremented in `bite()` | **No — latent.** The last bite sits inside `if lanes:`, so a records-fail path would have over-reported 19-for-18 |
| 2 | `knowledge/gen_showroom.py:474` | literal `6 bites` | `%d` from `len(ran)` | **No — latent.** ⚠ 2 of the 6 checks are `try/except` gates, **not** `bite()` calls; counting `bite()` alone would have **under-reported 6 as 4**, so both gates register explicitly |
| 3 | `knowledge/_validate_edge_extremity.py:241` | literal `weight floor 500@12-16 / 300@20+` | derived by probing `min_weight_for()` | **YES — LIVE-WRONG.** The function has always returned `500` for sizes **12–19**. The summary under-stated the band by three sizes and had done since it was written |

**Method:** AST scan of every `*.py` in `knowledge/` for functions named `*selftest*` containing
`print()` calls whose **literal** text parts carry digits — structure, not substring, per the
`BANNER_SESSION_RE` lesson (#37). 10 candidates returned; 7 dismissed on inspection as ordinals
(`bite 1`, `bite 2`), record IDs (`R-D3`, `lane-1-memento`), session refs (`#32`) or literal
*expectations* printed against computed actuals (`expected 1` — that is how a bite is supposed to
read). 3 were real. **The sweep is complete for this file set.**

## Evidence — every fix mutation-proven, then restored

| Mutation | Expected | Observed |
|---|---|---|
| delete one `bite()` from `_gen_lanes` selftest | `18 bites` | `18 bites` ✅ |
| delete the `ran.append` for gate 5 in `gen_showroom` | `5 bites` | `5 bites` ✅ |
| move the weight boundary `size < 20` → `size < 18` | summary follows | `500@12-17 / 300@18+` ✅ |
| **restore all three** | `19` / `6` / `500@12-19` | all three ✅ |

Backups taken to `/tmp` before each mutation and copied back; final state re-run and green.
**I did NOT run `_build_all.py`** — one foreground ≤45s call, and the conductor's to spend.
`gen_showroom.py` is in the build path, so **that run is a precondition to landing this.**

---

## ⬛ FORKED UP — judgment, not a worker's. Two.

**1. `_validate_edge_extremity.py:42` — `WEIGHT_FLOOR = [(12, 500), (20, 300)]` is read by nothing.**
Repo-wide grep: one hit, its own definition. The live rule is `min_weight_for()` at line 78; the gate
calls the function (line 172). The constant is caps-named, sits with the tuned dials (`SAT_CEILING`,
`LIGHT_FG_LUM`) and carries a comment stating the rule — so it is **the obvious place to re-dial the
halation weight floor, and editing it would change nothing, silently, with the build still green.**
The [[instrument-without-a-consumer]] shape. It is also what let fix #3 above stay wrong: three
statements of one rule, one inert, and the disagreement had nowhere to surface.
Two fixes, and they mean different things — **(a) delete it** (function is the rule; one source of
truth; cheapest, and where I lean) or **(b) wire it** (`min_weight_for` reads the constant; the rule
becomes data and re-dialling is a data edit; more in keeping with retrieval-not-recall, but a
refactor of a live gate). **(b) is a statement about where rules live ⇒ derivation governance.**
⚠ **Deliberately NOT minted as a `ds-` item:** taking a number while another lane is live risks two
lanes claiming the same one. Proposed for the conductor to number.

**2. GM §C·4 enact-queue — `consult "5/5 shown" denominator (separable, do regardless)` is STALE.**
Already closed by the O2′ rework. Live run: `rulings (5 of 40 shown — --all for more)` · `advisory
rules (5 of 61 …)` · `open items (3 of 29 …)` — true totals, not the cap. Both `_consult.py:22` and
`_search_core.py:27` carry in-code notes recording it closed. **Needs striking at wrap.**
⚠ Cost is small but real and I paid it: I selected it *because* it read as the cheapest item on the
board, then spent the survey to find it done. Same family as `HOLE #35` — **the record disagreeing
with the world in the direction that wastes a session's opening moves.**
**Not edited by me:** GM is the wrap ritual's file and a second lane of Dave's is live.

---

## Tree state — explicit paths, nothing staged

```
M knowledge/_gen_lanes.py
M knowledge/_validate_edge_extremity.py
M knowledge/gen_showroom.py
```

⚠ **Never `git add -A` here** — a second lane of Dave's is live. Stage these three by name.

**One further mutation of shared state, flagged at the time:** I moved a stranded
`.git/index.lock` to `_to_delete/index.lock.<epoch>` at ~10:34 (the sandbox cannot unlink inside
`.git`; `mv` is the runbook's remedy). Tree was clean and `git status` returned nothing, so I read it
as stranded from #38's wrap — **but with another lane live I cannot prove it was not theirs,
mid-operation.** If a lane hit a git error around 10:34, that is me.

## What I did NOT do

- **No commits.** Worker lane; a conductor reconciles.
- **No edit to `GOOD-MORNING.md`, `_LIVE-STATE.md`, or any ledger** — wrap-ritual surfaces, live lane.
- **No `ds-` number minted** (see fork 1).
- **No `_build_all.py` run** (see Evidence).
- **No adjudication of Dave's six opens** — all his; none touched.

## Record corrections observed this window (verified, not assumed)

- **Tree is clean and PUSHED.** `HEAD` = `origin/master` = `f72a910`; `git reflog show origin/master`
  reads `update by push`. `_LIVE-STATE.md`'s LATEST delta says *"TREE STATE. Local, unpushed"* —
  true when written, **false now.**
- **`_capture_gate.py` no longer prints `≤ 45` while enforcing `< 45`** (the #36 complaint). #37's
  band enactment is live: `BAND_FLOOR/HARD_STOP/MARKED_MAX = (45, 60, 63)`, and the message
  interpolates the constants. **That §C·4 line is spent.**
