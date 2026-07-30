# The cap binds the file — and the spec that got there was right for the wrong reason

```
provenance: session-48 · 2026-07-30
status: observed
```

**Register: OBSERVED — one enactment, three findings, one declined cut.** Session #48, Opus 5, Dave
live, Thu 2026-07-30 morning. Dave's instruction at the opener: *"bite 2 then stop"*, plus one folded
item — the stale Default tier in `MODEL-ROUTING.md`.
**Spine:** `GOOD-MORNING.md` ★ LATEST #48 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #48 ·
**Prior:** `_DECISION-HISTORY/2026-07-30-the-fixed-point-and-the-unnamed-unit.md` (#47, the other
half of open 16). Both-way links per `_DECISION-HISTORY/README.md`.

---

## 1. The job, as inherited — and the one number in it that had already moved

#47 left a specification, not a question. Dave had ruled open 16 as **(a)+(c)**; #47 enacted (c) — the
`_CHAIN.md` size stamp became a fixed point, exact by construction — and left (a) written out in full
in the forward title: re-point the M10 consumer to the FILE figure, import `_gen_chain` lazily,
restate `CHAIN_BUDGET_TK` on the measured wrapper **418**, move the drift pin at `:2282`, leave the
ADVISORY tier alone.

The first thing worth recording is that the brief's own warning fired against the brief. It said
*"MEASURE first — file was 4,878 at #47 and the number moves every wrap."* Measured at `b8b388e`:

```
file 4,604 tape  =  slice 4,187  +  wrapper 417
```

**417, not 418.** Twelve hours, one wrap, one token. Nothing turned on the difference — but the
sequence matters: had I taken 418 from the brief, the restatement would have been keyed to a number
no measurement supported, in a mechanism whose entire subject is unmeasured numbers. The rule
[[measure-dont-convert-units]] states is *measure, don't recall*; this is its cheap case, and the
cheap case is the one that trains the reflex.

## 2. The finding: Dave's spec was correct and its stated cause was not

The spec said, parenthetically, **"import `_gen_chain` LAZILY — circular import"**. That instruction
is right, and following it produces working code. But it is not the reason the obvious implementation
fails, and I would have discovered that the hard way if I had trusted the parenthesis instead of
reading the call graph.

`_gen_chain.build()` calls `cg.read_chain_tk()`. It has to: the fixed point needs the slice as a
strict lower bound to seed from. So the shape the spec's wording invites — teach `read_chain_tk` to
measure the file — is not a circular *import*, it is **unbounded recursion**:

```
read_chain_tk  →  _gen_chain.build  →  read_chain_tk  →  …
```

A lazy import does nothing whatsoever about that. Lazy import solves a different, real problem: the
two modules reference each other, so a module-level `import _gen_chain` inside `_capture_gate` would
close the cycle at import time and break every other consumer of the gate. **Both hazards are real;
they are different hazards, and only one of them was named.**

The resolution was therefore a **separate function**, `chain_file_tk(repo)`, sitting beside
`read_chain_tk` rather than inside it:

- `read_chain_tk` keeps its own honest meaning — the slice, the bytes `chain_parts` cuts.
- `chain_file_tk` measures `_gen_chain.build()`'s whole rendered text — the file a cold session opens.
- Both publish side by side, so the wrapper's size is always **attributable** rather than inferred.

★ **The transferable lesson: a correct instruction can carry an incorrect cause, and the cause is the
part a later session reuses.** Nobody re-derives the instruction — they re-derive the reasoning, on
the next problem that looks similar. An instruction that ships with the wrong "why" is a working fix
and a latent error, and the error surfaces somewhere else entirely.

### Two smaller choices inside the same function, both about refusing

**It measures the render, not the bytes on disk.** Every other figure this gate publishes is derived
live from `GOOD-MORNING.md` and `_LIVE-STATE.md`. A cap read off a stale `_CHAIN.md` would bless the
size of a *previous* session's chain — and staleness already has its own detector in
`_gen_chain --check`, a blocking build step. Measuring the live render leaves no gap and keeps one
source of truth.

**It refuses rather than falling back to the slice.** The tempting error path is
`return read_chain_tk(...)` when the render fails. That returns a number ~400 tape low under a label
that says FILE — **the exact defect open 16 records, reintroduced as an error path.** The consumer's
`UNMEASURED` branch already existed and already says so out loud; the refusal routes there.

## 3. Restating a cap so that nothing happens

`CHAIN_BUDGET_TK` moved `(4500, 6000)` → `(4917, 6417)`: both ends plus the measured 417.

```
old:  slice 4,187  vs warn 4,500   →  PASS, 313 tape of headroom
new:  file  4,604  vs warn 4,917   →  PASS, 313 tape of headroom
```

`bill_of()` is a monotone linear map, so restating both sides preserves **the comparison the consumer
actually makes**, not merely the tape figures. This is the `ds-021` precedent: *restate openly, never
silently tighten.* ★ **The test of a restatement is that it is boring today.** If this edit had also
moved a pass to a warn, it would have been a re-dial wearing a unit change, and the drift pin would
have been the only honest record left in the file.

Two things deliberately did **not** move. The **tier**: still ADVISORY, still agent-derived, still
awaiting Dave — re-pointing a unit is not promotion, and the engine never derives-and-promotes. And
the **417 is pinned as a snapshot, not tracked**. A budget that recomputed the wrapper every wrap
would silently absorb *wrapper growth*, which is precisely the region this check exists to expose
([[gate-inside-the-growth-loop]]).

## 4. The bite that proves it, and the bite that could not have existed before

For four sessions every M10 bite in the selftest passed while the wrapper went unmeasured. Reading
them back, the reason is uniform: **they all ask "did it warn?" and none asks "warned about what
size?"** A failure-only suite cannot see a unit error, because the unit error does not change whether
the check fires — it changes what the check is about.

So the new bite asserts the numbers: a `CHAIN FILE` figure must be published, and it must **exceed**
the slice, since the wrapper only ever adds text. Then — because an untested bite is documentation —
I ran a **control**: monkeypatch `chain_file_tk` back to the slice, re-run the selftest.

```
❌ selftest: M10 UNIT BITE: the FILE figure (60) does not exceed the SLICE (60) …
CONTROL selftest rc = 1
```

The bite runs, and it bites. This is the paired discipline the render runbook asks for and the
DV-D17 lesson taught: an absence-proof needs a detectable-when-present half, or a full revert passes
it. [[instrument-without-a-consumer]] — an instrument ships with its reader.

## 5. What I got wrong, and one cut I refused to make

**The error (one, self-caught).** Post-build reconcile showed `knowledge/_CAPTURE-GATE.md` and
`knowledge/_LIVE-STATE-CHECK.md` dirty. My first reading was that I had caused it and should sweep it
with the commit. The probe that cleared me is the one worth keeping: **does
`_build_live_state.py` import `_capture_gate`?** It does not — `os, re, sys, subprocess, datetime` and
nothing else — and I never touched `_LIVE-STATE.md`. So neither diff can be my edit. It became
**open 21** (§C·4): both reports were committed **stale** at `b8b388e`, with real content drift, and
the 34th in-scope file is the dossier *that same commit added*.

★ That makes four instances of one shape in two sessions: a variable inside generated output that
moves *after* the output is written — **per-edit** (#46's hand stamp), **per-pass** (#47's footer
draft), **per-run** (#47's build-date churn), **per-wrap** (these reports). Open 19 frames its
instance as *"seven files dirty with zero content change"*, which is true of dates and trains the next
session to read all post-build dirt as harmless. These two were not harmless, which is why they got
their own open rather than being folded in.

**The cut I refused.** The chain was 737 tape over its warn on my first draft, and the single fattest
line in it is the `size:` stamp at **685 tape** — a perishable measurement that has accreted four
sessions of narration about the stamp saga. Under GM-D2's own table (*"perishable reading — replaced
at the next wrap, never stacked"*) it is legitimately trimmable. I did not trim it, because trimming
it honestly requires locating a live home for each claim inside it first, and **I did not run that
probe.** Named, priced, and left undone — an honest UNPROVEN, which is a priced TODO, and not a
`HOLE`. It is offered as the cheap win at the top of #49's forward title.

**The retirement I could prove.** #39's job-line notice, 126 tape, sat in the chain announcing that
#39's job line was retired at #44. GM-D2's supersession test: *a notice lives exactly as long as the
text it negates remains on a live surface.* Probe: `JOB LINE` appears once in `GOOD-MORNING.md` —
itself — and zero times in `_LIVE-STATE.md`. Its target was gone; **it should have rolled with its
target four sessions ago.** One standing clause inside it (*behind pace means more windows*) was
carried to the render line first, then the notice went. ★ [[read-chain-cut]]'s corollary, again: the
cheapest chain tape is a claim that stopped being true.

## 6. Both EXIT CHECKS bit — tenth consecutive wrap

**2c, on #46's rolling banner.** Its sharpest line — *"the check ran, returned the disconfirming
answer, and never reached the plan"* — had **no standing home**. Probe named and empty:
`never reached (the|my) plan` · `disconfirming` · `evidence gathered and not consumed` across
`GOOD-MORNING.md`, `_FUTURE-STATE.md`, `_RUNBOOK-context-gauge.md`, `AGENTS.md` → the only hits were
#46's own banner, one wrap from leaving live state. Copied up as **open 22**, and recorded there as
**named, unsolved, unmechanised** — because a name is not a gate, and whether this one earns a
mechanism at all is Dave's call.

**The same banner also carried a claim that was false.** Its context-gauge line blamed a hardcoded
`DEFAULT_WINDOW`. #47 settled that: `:63` is `ap.add_argument("--window", type=int,
default=DEFAULT_WINDOW)` — an overridable default. **Ten consecutive banners named a hardcode that
never existed, each citing the previous one.** Under GM-D2's record-correction test the source must be
struck before the notice may roll, so it was struck in place, by addition, before the roll.
[[assertion-propagation-gap]] — and note which half of that class this is: not a claim that flipped,
but one that was **never true**, which is open 17's unsolved shape.

**2d, on #44's rolling delta.** Its residue — *the naming convention is still UNRULED for `roll_2f`
and the archives* — did have a home, and the home was the problem: it sits **inside open 13, an entry
headed ✅ DISCHARGED**, which a reader scanning for live opens skips. Under #43's scope (*same file ⇒
key it and mark PARTIAL*) open 13 was **re-keyed PARTIAL**. [[present-but-unkeyed-ruling]], found in
the wild rather than in a probe designed for it.

## 7. Verification, and saying whose verdict it is

`_build_all.py` still has no subset flag and its 75 steps still exceed one sandbox call. So I imported
**its STEPS table only** — lines 1–196, the driving loop excluded — and ran 1–25 · 26–50 · 51–75 in
three calls, order preserved. **All 75 steps ran; 0 returned non-zero.**

⚠ That is stronger than #47 could say and it is still **my composition, not the build's verdict.**
Running steps individually is not identical to running them in one process, and the composite exit
code `_build_all.py` would produce remains unobtainable. Also green: the gate selftest (exit 0),
`_gen_chain --selftest` (all bites), `_gen_chain --check` (FRESH).

**Pricing, with the measured half named** (`ds-025`). Disk reads **MEASURED: 30,616 tape** — the
capture-ritual runbook alone is 10,327 of it, which is worth knowing before anyone calls the wrap
cheap. My own writing: 3,625 tape. The baseline remains the gauge's **default 35,000 and is
UNPROVEN**. Band **🟡 AMBER ~51%** at `×1.57`; **~63% 🔴** at #41's measured `2.11×`. ★ **A band was
returned, breaking ten consecutive refusals** — the refusals' stated cause was the thing #47
falsified. That the spread now straddles a band boundary is itself the argument for stopping exactly
where Dave said to.

## 8. Resolved state, and what is still open

**Closed:** open 16 (both halves, (c) at #47 and (a) here). **Unblocked:** open 15 — and its `until:`
clause is now wrong in a way worth noting, since it names `read_chain_tk`, the unit open 16 retired;
corrected by addition, not rewritten. **Done on Dave's word:** open 20 (a).

**Dave's, unruled:** open 21 (stale generated reports) · open 22 (does the never-reached-the-plan class
earn a mechanism?) · open 20 (b) the two amber edges, (c) the unsupported *"Measured, adjustable."* ·
open 19 · open 13's naming convention · open 7, whose only relief is 2f, which is why `ds-022` failed
again this wrap and was **declared, not forged** — the strata stack is now **nine**.
