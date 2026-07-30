# The fixed point and the unnamed unit — how open 16 turned out to be unimplementable as ruled

```
provenance: session-47 · 2026-07-30
status: observed
```

**Register: OBSERVED — findings + one Dave ruling, enacted in part.** Session #47, Opus 5, Dave live
(Wed evening 2026-07-29 → Thu morning 2026-07-30, one window across the date boundary).
**Spine:** `GOOD-MORNING.md` ★ LATEST #47 · **Ledger:** `notes/_MEMENTO-DECISIONS.md` § ★ #47 ·
**Commit:** `62b6e1e`. Both-way links per `_DECISION-HISTORY/README.md`.

---

## 1. The opener found the queue's top item already stale, by 2×

#46 recorded `_CHAIN.md` at **+182 over its own 4,500 warn** and parked the remedy (open 16) for a
Fable window. Measuring at HEAD before pricing anything gave **4,860 tape — +360**. The progression:

| commit | `_CHAIN.md` FILE |
|---|---|
| `f811069` (#44) | 4,719 |
| `d3d9a16` (#45) | 4,682 |
| `5f55a22` (#46) | 4,860 |

⇒ **#46's own final edits added +178 after it stamped the number.** Its open-16 row was wrong at the
moment it was written. This is the third instance of the thing #46 itself named in the GM header —
*"the gap between stamping and finishing is where every one of these dies"* — and the first time the
gap has been measured across a commit boundary rather than caught pre-commit.

**Why it matters beyond the number:** the row was not stale in the ordinary sense of ageing. It was
false on arrival. Nothing in the corpus chases that class — [[assertion-propagation-gap]] fires on a
FLIP, and this never flipped. It is exactly **open 17**, found in the wild one session after open 17
was homed as an abstraction.

## 2. A withdrawal: the gauge denominator is homed, and I nearly filed a duplicate

Dave chose a small read-only bite: settle whether **open 2** (`ds-025`'s remedy) already covers the
context gauge's hardcoded window. My hypothesis was that it did not, and that the ten consecutive
band refusals pointed at an unhomed defect worth a new open.

**Half right, and the wrong half was the actionable one.**

- ✅ Open 2 does NOT cover it. `ds-025`'s three numbers are **boot · bill · fill** — all numerators.
  A denominator is out of scope.
- ⛔ But it IS homed, in three places: `_FUTURE-STATE.md:742`, and two lane receipts
  (`lane-a-region-measurement.md:246` calls it *"the only definition"*,
  `lane-b-six-opens-assembled.md:45`). **None of them is §C** — the roster a wrap actually reads —
  which is why ten banners have re-declared it as if fresh.
- ⛔ **The word "hardcodes" was wrong for ten sessions.** `_context_gauge.py:63` reads
  `ap.add_argument("--window", type=int, default=DEFAULT_WINDOW)`. It is an **overridable default**.
  Ten banners described a flag-settable default in language that made the refusal sound structural.
- ⬛ **The remedy has been written since 2026-07-29**, in open 5's floated note, P4:
  *"`_context_gauge.py` takes `--model`, and the thinking-retention behaviour is a per-model constant
  in the script, not an assumption."* Open 5 is `status: floated`, **UNREAD BY ANY SESSION** — four
  now — under Dave's firm #38 condition *"we must return to it when we get this fixed."*

**The lesson is not "the fix was missing."** The fix was written, filed, and pointed at. The problem
is that §C cannot see receipts or floated notes, so a documented remedy and an undocumented one look
identical from the roster. ⇒ **A finding filed only in a receipt is filed in a dated home, and dated
homes do not count** — the same rule 2c's EXIT CHECK already applies to banners, never applied to
the receipts the banners point at.

**Three things surfaced on the way, all forked, none touched:**

1. `MODEL-ROUTING.md` is stale in its default tier — names *"Opus 4.8 · high"* as Default–complex;
   this session is `claude-opus-5`. **I announced my own routing off that table at the opener.**
2. `_context_gauge.py` carries `AMBER_AT = 0.50`; `_capture_gate.py:79` carries Dave's ruled
   `((45,"GREEN"),(60,"AMBER"),…)`. #37 enacted the recalibration in the gate and left the gauge
   behind. **Two instruments, two amber edges.**
3. `DEFAULT_WINDOW` and `DEFAULT_BASELINE` both sit under the comment **`"Measured, adjustable."`**
   `ds-025` item 1 records the boot was never measured in 36 sessions, and #37's disk half
   (17,810 tape) matches neither constant. Whether either was ever measured is UNPROVEN; what is
   certain is the annotation is unsupported by the record. **Open 17's class, second specimen.**

## 3. Open 16 was not implementable as ruled — and the reason was in #46's own prose

Dave ruled **(a) cap the file + (c) name the unit**. Pricing the enactment surfaced a blocker:

`_gen_chain.py::build()` calls `read_chain_tk()` to produce the FOOTER, and **the footer contains
the figure**. So "measure the file" needs the file, which needs the footer, which needs the number.
**Circular.**

#46 had written the diagnosis without recognising it as one: *"a self-referential delta cannot be
written before the edit that changes it."* It appears in the GM header as a lament about hand-editing
a stamp. It is in fact a proof that the ruled shape could not be built.

⇒ **The wrapper had gone unmeasured for three sessions because measuring it was structurally
impossible, not because nobody looked.** Every session that "should have caught it" was up against a
circularity none of them named.

### The resolution: a fixed point

Render with a provisional figure → measure the whole rendered text → re-render with the true figure
→ **assert convergence**. Seeded from the slice, which is a strict lower bound (the wrapper only
adds). Converges in **2 passes**. If it oscillates, it **REFUSES** — both ends of a 2-cycle are
false, and a stamp picked from one end is the "cheerful zero" class wearing a plausible number.

**What this buys that a rule could not:** the stamp becomes **exact by construction**. #46 broke its
own size stamp twice in one session by hand and caught it pre-commit both times. A fixed point has
no gap between stamping and finishing, because there is no hand in it. This is the concrete case for
Dave's #47 direction — *"more machinery is what we are after, we should be translating as much prose
as we can"* — recorded as [[translate-prose-into-machinery]].

## 4. Three errors, all self-caught, one by the instrument being built

1. **The first footer draft cost +107 tape on every future cold read.** It explained the ruling, the
   unit change and the history — inside the file. The fix growing the region it exists to govern
   ([[gate-inside-the-growth-loop]]). Trimmed to **+18**. ★ **Visible only because the fixed point
   now reports slice and wrapper separately** — the instrument caught its own author within ten
   minutes of existing. The rule is now a comment in the source: **the `.py` is read by maintainers
   by choice; the `.md` is charged to every cold session forever — be generous here, miserly there.**
2. **The first version stamped the PASS COUNT into the footer.** That changes the rendered text on
   every pass, so the measured thing moves with the measurement and convergence is never guaranteed.
   Caught before running. Rule now in source: **the only per-pass variable in the rendered text is
   the figure itself.**
3. **I called the build "hanging"** off two runs stopping at an identical 364 log lines. That was an
   inference from a coincidence. Step 74 run alone is **exit 0 in 10s**. Withdrawn —
   [[measuring-tool-must-not-guess]], applied to my own diagnosis.

## 5. The build no longer fits in one sandbox call — and nobody could have noticed

**Measured:** 75 steps; steps 1–73 consume ~40s; the 45s tool cap kills the run at 364 log lines,
`EXIT=124`, reproduced at both 40s and 43s. `_build_all.py` has **no subset flag**.

⇒ **No session can obtain the build's own composite exit code any more.** Verified here in segments,
and the composition is mine, not the build's verdict:

- steps 1–73 — reached step 73 with no abort line; `_build_all.py:290` `sys.exit`s on any gating
  failure, so reaching 73 **proves** none of 1–73 gate-failed;
- steps 69–71 (this change) — generate ✅ · determinism check ✅ · selftest ✅;
- step 74 exit 0 (10s) · step 75 exit 0 (*"PASS, 0 errors, 4 warnings, schema valid 67/67"*);
- the `❌ FAIL` lines in the log are a **declared-ADVISORY** gate (C2 property-resolves, ruled
  BLOCKING but shipping advisory until its backlog clears, remedy explicitly Dave's) plus four
  deliberate bad-date/bad-status fixtures.

**So the honest claim is "all 75 accounted for, none gate-failing" — not "75/75 exit 0".** The banner
has been saying the stronger thing. [[ritual-output-is-not-evidence]]: a build verdict quoted from a
previous run is a banner, not evidence.

## 6. The same bug in a second costume, found by the reconcile

Step 0.5 turned up seven dirty files beyond the two I edited. Every one was a **pure date stamp**,
`2026-07-29` → `2026-07-30`, zero content change — the build ran either side of midnight.

Those artefacts stamp the **build date** into generated content, so the repo throws a false diff on
any day the build runs. **That is this morning's footer bug with a longer period:** a per-RUN
variable inside generated output, where the footer had a per-PASS one. Per-pass broke convergence;
per-run breaks the diff. Both make a generated file disagree with itself for reasons that have
nothing to do with what it describes.

Raised, not ruled — whether a generated artefact may carry a date at all is Dave's.

---

## Resolved state

- ✅ **Open 16 (c) ENACTED** — `62b6e1e`. Fixed-point stamp, unit named, three bites re-pointed.
  Measured: **file 4,878 tape = slice 4,460 + wrapper 418**, fixed point in 2 passes.
- ⛔ **Open 16 (a) NOT enacted.** `CHAIN_BUDGET_TK` and the M10 consumer still measure the slice.
  The cap does not yet bind the file. **Open 15 stays blocked behind it.**
- ✅ **Open 2 question settled** — the denominator is homed, in receipts §C cannot see.
- ⛔ **2f still blocked** (open 7); `ds-022` FAILS at this wrap, DECLARED, no forged `HOLE`.
  Strata stack **EIGHT**.

## Still open

Bite 2 (open 16 (a)) is specified and priced: re-point the M10 consumer to the file figure, restate
`CHAIN_BUDGET_TK` on the measured 418 so today's verdict is arithmetically unchanged (`ds-021`
precedent, `_capture_gate.py:344` — restate, never silently tighten), update the drift pin at
`:2282`, keep ADVISORY/awaiting-Dave status untouched.

New candidates raised this session, all Dave's: the build's call budget · date stamps in generated
artefacts · `MODEL-ROUTING.md`'s stale default tier · the two amber edges · the unsupported
`"Measured, adjustable."` annotations.
