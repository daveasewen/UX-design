# #153 — the phantom fill, and the refusal that named the wrong obstacle

provenance: session #153 · 2026-08-11
status: observed

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #153 · `GOOD-MORNING.md` ★ LATEST #153.
Ledger: `knowledge/_rulings.json` § `s152-D1` (Dave's ruling, made #152; this session ENACTED it).
Floated register: `_FUTURE-STATE.md` § ⬛ FLOATED #153 — `s153-D1`.
Predecessor arc: `_DECISION-HISTORY/2026-08-11-152-the-star-that-was-never-dark-and-the-gate-that-measured-a-phantom.md`
— that session FOUND the defect; this one FIXED it and then failed to prove the fix.*

---

## The arc in one line

`s152-D1` was enacted in full — fix, declaration, fixtures, arms, mutation control — and **not one
browser-driven arm was ever run**, because the sandbox has no browser and CI does not run this gate
either. The session's real product is therefore two things: a fix that is honestly labelled
**ENACTED, NOT VERIFIED**, and a finding about how gates lie while telling the truth.

---

## Finding 1 — the fix keys on PAINTED, not on the colour black

#152 measured the defect: `_validate_state_contrast.py`'s MARK leg computed
`ratio(inner-fill, the SHAPE's own computed fill)`, and an `<svg>` with no `fill` attribute computes
to the **UA-default black** — a colour nothing on screen wears. `#333` against that phantom is
**1.662 exactly**, and light "passed" at 21:1 against the same phantom, which is precisely why it
never read as an instrument fault.

The obvious remedy — *skip when the fill is black* — was **available and wrong**, and rejecting it
is the interesting part of this finding. Black is a legitimate design value. A genuine black roundel
with a `#333` mark on it is a **real** contrast failure and must keep failing. Keying the skip on the
colour would have converted a false red into a **false green**, which is strictly worse: a false red
gets argued with, a false green gets shipped.

So the clause keys on **painted**, not on black. Inside the `<svg>` branch of MEASURE
(`:336`–`:355`), `bodyPaints` asks whether *some descendant shape actually wears the fill the svg
declares* — a descendant matching
`path,circle,rect,ellipse,line,polyline,polygon,use,text,tspan`, not inside
`defs,clipPath,mask,symbol,marker,pattern` (those are not rendered in place), not hidden, not
`display:none`, not `opacity:0`. If nothing wears it, the comparison is skipped.

**The dead-end that shaped the implementation.** The natural way to compare two colours in this file
is `parse()` — it is what every other leg uses. Using it here would have meant parsing *every*
descendant's fill, and `parse()` **refuses** on anything it cannot read. That would have **minted
refusals this change was never ruled to create**: the gate's refusal count would have moved for
reasons that had nothing to do with `s152-D1`, and the diff would have stopped being attributable
[[attribute-the-diff]]. The presence test therefore compares **computed strings** — both sides come
from `getComputedStyle`, so both are normalised identically and the comparison is exact — and
`parse()` is left doing exactly the job it did before.

**How we know the clause discriminates.** `mark_real_black_roundel_still_fails` is a fixture whose
shape fill computes to *the same* `rgb(0,0,0)` as the phantom, but is genuinely worn by a
`<circle>`. Without that fixture, "skip the phantom" and "skip everything black" are
indistinguishable — and so are "fix it" and "delete it". The mutation control closes the other side:
cut `if(fg&&bodyPaints){` back to `if(fg){` and the **1.66 must reappear**. An arm asserting only
silence cannot tell a fix from a deletion.

## Finding 2 — the skip is declared, and the declaration is designed to move no ratified count

A skipped measurement that is invisible is indistinguishable from a measurement that passed. So the
skip emits a record (`kind:'markskip'`, carrying where/fill/reason) and a report line under its own
`MARKSKIP_PREFIX` at `:512`.

The **deliberate** part: that prefix is **not** one of the counted prefixes. `HOLE_PREFIX`,
`CARRIER_FAIL_PREFIX` and `CARRIER_ERR_PREFIX` all feed counts Dave has ratified, and
`verify_report` asserts those counts against the body on every write. Folding a skip into either
bucket would have moved a ratified figure as a side effect of a bug fix. A skip is neither a failure
nor a hole; it is an advisory receipt whose whole job is that a reader can see the leg did not run,
and argue with it. `verify_report`'s three counter contracts are untouched — the entire diff
(+127/−5) **removes only two lines**.

## Finding 3 — the fix has a runner; the proof does not

This was checked rather than assumed, because [[instrument-without-a-consumer]] has now cost several
sessions. `_build_all.py:255` runs the gate and `:261` runs `--selftest`, both read first-hand. So
the **fix** is not an orphan.

Then the proof was attempted, and it could not run:

- `--selftest` exits **rc=2** with a named refusal —
  `StateContrastSelftestError: chromium would not launch … libXdamage.so.1: cannot open shared
  object file`. The system library is missing, there is no root (dpkg lock), and the disk is **97%
  full / 360M free**.
- **CI does not run it either.** `.github/workflows/gates.yml:20`–`:22` says so explicitly: the
  render-dependent checks are excluded because they need a browser engine.

⇒ `s152-D1` is **ENACTED, NOT VERIFIED**, and the arms that would verify it have **no runner in the
sandbox or in CI** — only Dave's local render path. This is a sharper instance of the
instrument-without-a-consumer class than the ones that named it: previously a *gate* had no runner.
Here **the fix has a consumer and the proof does not**, which is a shape the class did not yet
describe.

**And so the two Selection-controls star reds stay KNOWN-FALSE and DECLARED.** They clear when the
arms are *driven*, not when the code is *written*. The gate refusing loudly is it working as
designed — and a refusal is not a pass.

## Finding 4 — a refusal names the FIRST obstacle, not the BINDING one

This one is new, it was found while trying to verify Finding 3, and it generalises.

The same command was run twice. Both times **rc=2**. Both times an honest, named refusal. **The two
names were different:**

| run | named refusal | true about the disk? |
|---|---|---|
| `python3 …--selftest` | *"the 'playwright' module is not installed"* | **NO** |
| `PYTHONPATH=/var/tmp/pysite …--selftest` | *"chromium would not launch … `libXdamage.so.1`"* | yes |

Playwright **1.62.0 is installed**, at `/var/tmp/pysite`; the browsers are cached at
`/var/tmp/pw-browsers`. The first message is false about the environment. Nothing is wrong with the
gate — it reported, accurately, the first thing that stopped it. The cause is the harness: **bash
calls carry no environment across a call boundary**, so a `--target=` install survives on disk while
the *path to it* does not survive [[sandbox-call-boundary-kills]].

The consequence is the finding: **a session that ran only the first form would have inscribed a
true-sounding falsehood about its own environment, sourced from an honest gate** — and "playwright
is not installed" is exactly the kind of environment claim that gets repeated for months
([[unmatched-grep-is-not-an-absence]] is the same family: the probe's shape decided the answer).
⇒ **When a refusal names an obstacle, check whether it is the binding one before inscribing it.**

**A by-product worth keeping:** 18 **pure** arms run and pass in-sandbox today (`grep -c "^  ok "`
= 18, in both runs). That is first-hand corroboration that residual ② — a pure arm placed before
`got = _measure_fixtures()` — would run today with no browser. It is cheap, and it was skipped only
for budget. Note the asymmetry that makes it worth writing down: those 18 greens exist, but
`--selftest` is rc=2 overall, so **nothing reports them as a pass**.

## Finding 5 — a failed write plus a successful read looks exactly like a successful run

Found by the conductor, inscribed here because it is a class, not an incident.

A redirect to `/var/tmp/st.out` hit permission-denied. `tail` then read **a leftover file from an
earlier session**, whose `"selftest OK — 25 arms"` line was very nearly reported as this run's
result. It was caught only because the arm names for `s151-D1`'s carriers were **absent** from it —
i.e. by a *content* check, not by anything about the pipeline.

The shape: the write failed, the read succeeded, and the shell's exit status did not connect them.
Both halves behaved correctly in isolation. Relatives: [[ritual-output-is-not-evidence]] (verify
against the target, never a banner) and [[stale-mount-corroborates-a-stale-premise]] (a stale source
agrees with you). The remedy applied, and re-applied by the wrap sub on **both** of its own runs:
**write to a path this session owns, and print mtime-vs-now beside the verdict.** Both runs above
show mtime equal to `now`, which is why their rc=2 can be trusted to be *this* session's.

## Finding 6 — what was deliberately NOT done

- **The icon leg shares the phantom.** `kind:'icon'` at the same site uses the same phantom `fg`. It
  is WARN-only and **outside `s152-D1`'s ruled scope**, so it was not fixed and is not ruled. Named
  as a residual so it is checkable rather than re-discovered [[gate-glob-scope-rule]].
- **`s153-D1` is FLOATED, not ruled.** Dave picked *"mirror the two-red law"* from an option set and
  the conductor reflected it back; **he did not confirm**. The SHAPE (a background-keyed fork) is
  what he indicated. ⛔ The two values are **not** ruled and must not be invented — deriving a green
  pair from `s151-D1`'s red pair would be exactly the laundering this record exists to prevent
  [[feedback-dont-launder-a-premise-into-a-ruling]]. It is recorded in `_FUTURE-STATE.md` and
  **deliberately not** in `knowledge/_rulings.json`, where an entry is a ruling by definition.
- **The ENOSPC datapoint was recorded, not promoted.** `TMPDIR=/var/tmp pip install <pkg>
  --break-system-packages --target=/var/tmp/pysite` succeeded where the default prefix died on
  ENOSPC. That is now n=2. The runbook rule was **not** rewritten; two datapoints are a pattern
  worth naming and not yet a rule [[planning-estimate-is-not-a-measurement]].

---

## Resolved state, and what is still open

**Resolved:** the MARK leg no longer measures a phantom; the skip is declared and moves no ratified
count; three fixtures and four arms plus a guarded mutation control exist in the file; the fix has a
confirmed runner.

**Open, and the order is the residual's:**

1. **VERIFY `s152-D1`** — drive the arms on Dave's local render path, or find a browser-free proof.
2. **The pure arm for `render_report`'s markskip line** — runs in-sandbox today, needs no browser.
3. **The icon leg** — same phantom, WARN-only, unfixed by decision.
4. **`s153-D1`** — awaiting Dave's confirmation; values unruled.

**The honest summary of this session:** it produced a fix it could not test, and said so in every
place a reader will look.
