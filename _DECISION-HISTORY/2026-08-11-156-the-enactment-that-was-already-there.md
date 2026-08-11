# #156 — the enactment that was already there, and the disk that was not ours to clear

```
provenance: 156 · 2026-08-11
status: observed
```

*Both-way links: `GOOD-MORNING.md` ★ LATEST #156 banner · `_LIVE-STATE.md` ⏱ LATEST DELTA #156 ·
`knowledge/_rulings.json` § `s155-D1` (status tail, ENACTMENT MEASURED #156) · prior arc:
`_DECISION-HISTORY/2026-08-11-155-green-mirrors-red-and-the-audit-that-finally-ran.md`.*

---

## Why this session existed

`s155-D1` was ruled at #155 and amended the same window (#155-A): green/success ink mirrors the
two-red law, the values resolved **by reference to `s144-D1`** — `#137F3C`-on-white / `#66CC8D`-else —
scope **MONO ONLY**. The forward title said "the two green values"; by the time the session opened,
the values were no longer the question. What was open was **enactment**, and nobody had measured
whether enactment was owed at all.

## Finding 1 — the cheap item first, and it was genuinely one line

`knowledge/_tests/test_gates.py`'s docstring said the render-dependent gates' *"un-testedness in CI
is a known gap, not a green light"*. That became false the moment #155's CI `render` job landed —
the assertion-propagation class, named on #155's own banner as *"#156's cheapest item"*. The
docstring now names the job and what each half of it does: `--selftest` **BLOCKING**, the full sweep
**ADVISORY** while the Banner 8 stay open. `ast.parse` clean.

⚠ **And the suite itself could not be run here.** See finding 3 — that is a fence, not a pass.

## Finding 2 — the enactment was a SURVEY, and the survey found it already seated

The instinct at the top of the session was to build: mint a `--success-atom` alias, fork the theme
files, wire a seat. Every one of those would have been wrong, and the measurement is why:

- **(a) the values were already minted at #145** — `knowledge/tokens/semantic-colour.json`,
  `rag/success-ink`. The ruling did not need them created.
- **(b) `knowledge/canon/canon.css` already emits the fork** — `--rag-success-ink: #137F3C` in the
  light block (`:309`) and `#66CC8D` in the dark block (`:664`), the **same mode-block pattern** as
  `--rag-error-ink`. The shape `s155-D1` rules is the shape the file already has.
- **(c) MONO-ONLY holds STRUCTURALLY, not by luck** — no theme override file names either `-ink`
  rung, and the inheritance shape is identical for red and green. There is no green-specific
  fall-through to declare [[fall-through-class-declare-what-you-mean]].
- **(d) there is NO atom seat** — no component carries a success state, so no `--success-atom` alias
  was added. An alias with no consumer is an
  [[instrument-without-a-consumer]]; minting one to make the enactment *look* complete would have
  been the defect this repo has a hook for.
- **(e) the one ruled green-TEXT seat has no binding site.** The ruling's rider is *coloured text only
  on monetary values carrying a symbol*. The monetary component is `amount-display`, and its
  `meta.json` `sign` prop is an enum of **`["none", "negative"]`** — there is no `"positive"` value to
  bind. So the ruled seat cannot be enacted without an enum addition, and **an enum addition is a
  ruling**. Carried unchanged from #143 finding 5; it is Dave's.

**The arc, and it is the transferable part:** an enactment lane that opens by measuring what is
already seated can close as a survey. The failure mode it avoids is the opposite — building a seat to
discharge a residual, and inscribing "ENACTED" over an instrument nothing consumes.

Recorded **by textual addition** in `s155-D1`'s `status` (the file carries mixed `\u` escaping, so a
serializer round-trip is impossible [[serializer-defaults-reformat-the-file]]); 116 entries, priors
asserted parse-equal before the write.

## Finding 3 — a disk fence, dated, verified three ways, and NOT a permanent limitation

`knowledge/_tests/test_gates.py` needs two ~153 MB tree copies. `/` had ~338 M free. The space is
held by **~1.7 GB of stale, nobody-owned `/var/tmp/pw-browsers-s131/`, `-s136/`, `-129` and
`pwenv-s131`** left by prior sessions. Three probes, all run, none inferred:

1. `rm -rf` on them → **Permission denied** (not ours to delete).
2. `sudo` → broken: `/etc/sudo.conf` owned by uid 65534.
3. `/dev/shm` → too small to host the copies.

⇒ **the suite's runner this session is CI, not the sandbox.** ⚠ Written deliberately as a
**per-session fence dated 2026-08-11**, not as a standing environmental fact: a fresh sandbox next
session most likely clears it, and this repo has three recorded instances of a true-when-written
environmental claim aging into a false one that nothing chased
[[assertion-propagation-gap]] [[refusal-names-the-first-obstacle]].

## Finding 4 — the FILL blowout had one nameable cause

Two `shutil.Error` ENOSPC dumps printed whole copytree error trees into the transcript: **~65K FILL**
for output nobody read. The lesson is mechanical, not moral: **quiet or tail every command that can
emit a copytree error tree** (`2>&1 | tail -20`). Wrap-open landed at FILL **141,154** against the
stop line **150,929** — the wrap opened **AT the line, late, not early**, and the two dumps are the
reason. #155's wrap opened at 113,634 for the same shaped session.

## What is resolved, and what is still open

**Resolved:** the stale `test_gates.py` claim · the enactment question for `s155-D1` — measured, not
assumed, and the answer is *already seated everywhere a seat exists*.

**Open, and none of it is this session's:** the `amount-display` `sign` `"positive"` enum value
(**Dave's** — the only remaining `s155-D1` residual) · whether the CI sweep step ever flips to
blocking (**Dave's**, and only when the Banner 8 land) · the Banner-8 hover-wash · the icon-leg
phantom · every G-item · every `_FUTURE-STATE.md` priority · any green fork for legacy / console /
supercharge (explicitly **not governed** by `s155-D1`).
