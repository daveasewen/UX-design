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

---

## AMENDMENT #153-A — post-wrap, after commit `c5b406f`

*Addition only. Everything above stands unaltered as the record of what #153 believed and why*
[[header-wins-over-audit]]. *This addendum corrects it; it does not replace it. Written by a separate
OPUS amendment sub, which re-verified first-hand every claim it inscribes.*

**The honest summary was wrong in its most important word.** #153 did not produce a fix it *could
not* test. It produced a fix it *did not* test, because it stopped at the first obstacle it hit and
called that obstacle the environment.

### 1 · The environmental fence was false

The wrap inscribed *"chromium would not launch … `libXdamage.so.1: cannot open shared object file`
… no root"* as an environmental fact. It is not one, and the repo already said so:

- `knowledge/_RUNBOOK-render-verify.md:181` stages exactly those libs with **`apt-get download`**.
- `:186` says, in as many words: *"(`apt-get download` needs no root and no `apt-get update`.)"*
- The lib farm **was already on disk the whole time** —
  `/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu/libXdamage.so.1`, in a directory dated
  **Aug 8 15:21**, three days before #153.
- `:36` names the exact error committed: *"(`PLAYWRIGHT_BROWSERS_PATH` alone) was NOT sufficient this
  time; the full working env, all four."*

The conductor set `PLAYWRIGHT_BROWSERS_PATH`, hit the lib error, tried `apt-get install` (root,
refused), and declared a fence — **without opening the runbook that answers it.** Dave said
*"I think theres a runbook for chromium and playwright"* and the fence dissolved in one call.

*(Precision, verified here: the brief relayed the farm as `/var/tmp/chromelibs`. At that level there
are only `.deb` files; the extracted `.so`s sit one `root/usr/lib/aarch64-linux-gnu` deeper — which
is the exact `LD_LIBRARY_PATH` the runbook prints at `:44`. A correction to the path, not to the
finding.)*

### 2 · This is the third instance of one class, and Dave caught it twice with the same sentence

- **#123** declared a render gap on *"chromium is TLS-blocked in-sandbox"*.
- **#124** carried that forward **as fact**, and Dave stopped it with *"and there is a runbook for
  chromium and playwright"* — his words are inscribed at that runbook's **`:131`**, and the original
  ask at **`:5`**.
- **#153** did it again, and Dave caught it again, with almost the same sentence.

Each refusal was sincere, loud and named. Each named the **first** obstacle rather than the
**binding** one. **This recurrence is the finding of #153-A — more than the fix is**
[[feedback-read-the-runbook]] [[refusal-names-the-first-obstacle]].

### 3 · What the runbook's env actually produced

With `PYTHONPATH=/var/tmp/pysite` · `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers` ·
`LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu` · `TMPDIR=/var/tmp` ·
`PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`:

- `python3 _validate_state_contrast.py --selftest` → **rc=0, `"selftest OK — 57 arms"`, zero bites**
  (`grep -c '^  ok '` = 57). **Re-driven first-hand by this sub, not relayed.**
- All five `s152-D1` arms green, **including `arm_removing_the_skip_brings_the_phantom_back`** — the
  mutation control that cuts `if(fg&&bodyPaints){` out of MEASURE and demands the 1.662 return
  [[mutation-tests-the-clause-not-the-feature]].
- `V.run(['Selection-controls'])` driven live: **MARK text failures 0** (was 2) · other text
  failures **0**. The two star reds are **measured clear**, not merely declared known-false.

⇒ **`s152-D1` is ENACTED *and* VERIFIED.**

### 4 · An arm bit on its first real run, and the bite was the arm's

`arm_browser_phantom_shape_fill_is_skipped_and_declared` asserted the reason string *"no painted fill
at all"*. The branch that actually fires is the **declared-but-unworn** one, because an `<svg>` with
no `fill` attribute computes to **`rgb(0, 0, 0)`** — which is **not `none`** — so `shapeFillStr` is
truthy. The remedy asserts the phantom colour explicitly plus *"no descendant shape paints"*, so the
arm can no longer pass against the other branch by accident.

**The mechanism was right and the expectation was wrong.** An arm that bites and names its own
assertion is the arm working [[a-crash-is-not-a-fail]].

### 5 · A unit correction, caught in this pass

The figure relayed as *"28 declared MARK SKIPs"* is the **raw** record count. Re-measured:
`Selection-controls` yields **42 raw records → 28 raw `markskip`s → 4 UNIQUE lines** after
`render_report`'s own de-duplication key. **The report prints 4.** Both numbers are true of different
things, and naming which is which is the whole discipline [[measure-dont-convert-units]].

**An observation that rules nothing:** 28 raw (4 unique) skips on *one* snippet says the MARK leg was
only ever measuring anything real on **genuine roundels** — its former red count **overstated its
reach**. `s152-D1`'s open item (*whether any other of the 75 snippets hits the class*) stays open and
unmeasured.

### 6 · The blocker that replaces the false one — and it is measured

`knowledge/_STATE-CONTRAST-AUDIT.md` was **not** corrupted and **not** rewritten: verified at
**2026-08-11 15:38:59 / 2,364 bytes / 21 lines**, byte-identical before and after every drive
(`run()` measures, `main()` writes, `:1206`). It is therefore **known-stale** — it still prints the
two reds that no longer reproduce.

Regenerating it is blocked, but narrowly and for a different reason than #153 gave:

- A full sweep **exceeds the ~178 s tool-call cap** (the conductor's run was killed at 177,998 ms).
- ⚠ **The brief said "38 snippets" and that is wrong.** Measured:
  `knowledge/snippets/*.reference.html` = **75** — the same figure `s152-D1`'s own open item already
  uses.
- Timed here on a 3-snippet drive: **49.5 s ⇒ 16.5 s/snippet ⇒ ~1,237 s (~20.6 min) for 75** —
  roughly **7× the cap**, not marginally over.

⇒ The audit needs **chunking in the shape of `_build_all.py --range/--resume`**
[[sandbox-call-boundary-kills]]. **The browser is fine; the call boundary is the limit** — and unlike
the fence it replaces, this one is measured.

### 7 · Correcting #153's own residual ①

It said the arms have *"no runner in the sandbox OR in CI"*. **They do run in the sandbox.** What
remains true is that **CI still excludes them**: `.github/workflows/gates.yml:20`–`:22`, re-read
first-hand — *"The render-dependent checks … are NOT run here — they need a browser engine."*

⬛ **A proposal for #154, and explicitly not a decision:** a CI render job is now cheap, because
`gates.yml` runs on `ubuntu-latest`, which **has root**, where `playwright install --with-deps
chromium` works with none of the lib-farm choreography. **Dave's call, not this sub's.**

### 8 · What this amendment did not do

**It ruled nothing.** `s153-D1` (green/success-ink) stays **FLOATED, awaiting Dave's confirmation** —
the shape only; **the two values are not ruled and were not invented**, and it stays in
`_FUTURE-STATE.md` and deliberately out of `knowledge/_rulings.json`. The icon-leg phantom residual
stays **declared and unfixed**. All **22** of Dave's open G-items and every ratified stratum are
untouched: **add, never trim.** **Not pushed.**

**The honest summary of the amendment:** the session's own verdict on itself was the last thing that
needed checking, and it did not survive the check.
