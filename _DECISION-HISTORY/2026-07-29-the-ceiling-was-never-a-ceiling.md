# The ceiling was never a ceiling — and the gate that enforced it was reading an estimate

provenance: session #36 · 2026-07-29
status: ruled (§1, Dave's, pointer: `notes/_MEMENTO-DECISIONS.md` § ★ #36) + observed (§2–§5, measured this window)

*Session #36, Wed morning, Opus solo, Dave live. A session that enacted no build and is not a
wasted window: it found that the throttle's headline number had been enforcing the opposite of
what Dave meant, and that the gate deciding our wraps degrades silently into an estimator that
under-reports pressure. Both were found by pricing a job, not by building one.*

**Both-way links:** spine → `_LIVE-STATE.md` ⏱ LATEST DELTA 2026-07-29 (#36) · ledger →
`notes/_MEMENTO-DECISIONS.md` § ★ #36 · amends → ds-023 in `knowledge/_RUNBOOK-context-gauge.md`
§ ★★ · prior arc → `2026-07-29-reading-the-usage-series.md` (#35).

---

## 1. The finding that re-shaped the session: 45 was never a block

The window opened by pricing #36's ruled job — enact the #35 offloads plus the deferred register —
at `fill 20 + job 28 + wrap 6 = 54`, and reported it as **failing** the ds-023 pre-flight ceiling of
`fill + job + wrap < 45`. Dave's reply was not a re-dial. It was that the enforcement had never
matched his intent:

> *"I only ever intended the 45% as a warning… it just creates the band, between 45 and 60, that I'd
> prefer the full price with wrap to sit in."*
> *"the full price, front-load + context GM + job + wrap is what must fall to below or about 60,
> straying into 63 occasionally might be fine but rare."*

**The record supports him, and this is the part that matters.** ds-023's own header in
`_RUNBOOK-context-gauge.md` reads:

> *ruled-in-part #31 in Dave's own words, **enforcement picked #31 delegated**, ENACTED + CONFIRMED #34*

Dave ruled the **number**. A delegated agent picked **FAIL** as the enforcement mode. #34 then
sharpened `≤ 45` to `< 45` — correctly, on Dave's word, but that ruling was about *which side of 45
counts*, not about whether 45 should block at all. The blocking-ness was never his.

⇒ **This is the [[gate-narrows-its-own-rule]] class, third appearance, and the most expensive one:
`warn ≠ block`.** The two earlier instances narrowed a rule's *region*. This one inverted its
*direction* — and it did so on the single number every session in this repo prices itself against.

### ★ The gate was failing the target band

Under Dave's reading, `45–60` is where the full price is *supposed* to land. The enacted gate FAILED
at ≥45. So the instrument was not merely stricter than its rule: **it refused the band it existed to
steer sessions into.** Every session since #34 that priced itself honestly into the low 50s — the
intended zone — was either forced to mark a `RESERVE SPEND — forked to Dave` receipt for a spend that
was never over-budget, or to quietly under-price the job to fit. ds-023's own text names the second
outcome as the thing the escape hatch exists to prevent. It was producing it.

**Read back to Dave and confirmed in his own correction** — the first read-back ("45 becomes a WARN,
blocking line ~60") was still wrong in shape: it treated 45 as a threshold to avoid crossing rather
than as the **floor of a preferred band**. He corrected it. That second correction is why the ruling
in the ledger is worded as a band and not as two thresholds.

## 2. The wrap was priced at 6 against a measured 10 — and Dave caught it

The opening price carried `wrap 6`. #35's wrap had been priced at 10 and **still overran**. Nothing
about #36's wrap was cheaper; it was heavier — a worker hand-back to reconcile path-by-path, the
register rows, a new gate function to record.

There was no analysis behind the 6. It was a number that made the total fit.

⇒ **A wrap term is the one term in the stamp with a measured history. Pricing it below the last
measurement requires naming what got cheaper.** Nothing had. Corrected to 10 before the arithmetic
was re-run, and the re-run is what moved the session off enactment entirely.

## 3. ★★ The gate degrades into an estimator that UNDER-reports pressure

The first `--wrap` run this window reported:

> `COMPACTABLE region: 10,939 tape` · warn 8,000 · block 12,000 — *(bytes/3.53 ESTIMATE (tiktoken absent))*

After `pip install tiktoken --break-system-packages`, the same command on the same unchanged file:

> `COMPACTABLE region: 11,353 tape` · warn 8,000 · block 12,000

**A 414-tape swing on the number that decides whether a wrap is allowed to close** — and the swing
runs the wrong way. The estimator does not fail safe; it reports **less** pressure than exists, so a
session in a fresh sandbox sees ~414 tape of **phantom headroom** against a 12,000 block.

The corpus is dense with `★ ⚠ ⛔ ·` and runs at ~3.53 bytes/token where the customary constant is 4 —
the runbook says exactly this, under *"Measure, never convert by rule of thumb."* The fallback honours
the corpus constant and is still wrong, because **a corpus-wide average is not this region's ratio.**
[[measure-dont-convert-units]], now with a number attached: *a count is not a measurement*, and neither
is a conversion.

⚠ **The sandbox is fresh every session and tiktoken is not preinstalled** — the GM header already says
so. What it did not say is that the gate keeps running anyway, labels the degradation in a parenthetical
mid-line, and hands back a plausible number. **A gate that silently substitutes an estimator for its
instrument is [[instrument-without-a-consumer]] inverted: the reader is there, the instrument is not,
and nothing refuses.** Candidate remedy for #37: the size checks REFUSE without tiktoken rather than
estimate — an honest UNKNOWN over a confident approximation. Not ruled; raised.

## 4. GM's offload relief is already spent — the register has nowhere to land

The plan carried into this window assumed the seven offloads would relieve `GOOD-MORNING.md`. **They
will not.** #35's own ledger entry records that the four GM sections (`C2b` `C3` `C4b` `C5`) were
moved *at its wrap, under duress*, after six rounds of trimming each yielding less than the last.

So the standing position, measured this window:

| | tape | |
|---|---|---|
| GM compactable | **11,353** | after #35 spent its relief |
| block | 12,000 | |
| **headroom** | **647** | |

The three remaining offloads (`LS:DEAD` `LS:SPINOFFS` `LS:TARGETS`) and the de-materialised
`LS:LIFECYCLE` all relieve `_LIVE-STATE.md`. **The deferred register lands in `GOOD-MORNING.md` §C.**

⇒ **#36's ruled job spends GM headroom it does not have, while the relief lands in a different file.**
Dave flagged this from his own wrap four hours earlier — it is what forced his six trimming rounds — and
insisted it be planned before a worker starts rather than discovered at the gate. It is now a measured
number in the brief, not an intuition.

## 5. Subagents: right shape, wrong size

The delegation split was drawn from `_RUNBOOK-parallel-conductor.md` rather than reconstructed —
*"a worker never edits shared canon mid-flight; workers write only NEW files at worker-scoped
filenames."* That maps cleanly onto this job: the deferred register is a new file plus a gate function
plus a selftest (worker-safe, and verifiable by **running** it); the offloads edit GM, LS and the
archives (conductor only).

Dave's framing of the same rule, which is the better statement of it:

> **"A sub-agent may do the working, never the judging."**

**But the arithmetic killed it.** The register was priced at 15–18. Dave's own #35 build — five
functions, a probe, 49 bites, two mutation tests — cost about 12. A register plus one gate function is
nearer **8**, and lane overhead is 4–6. Delegation would have saved 2–4 points and bought a hand-back
reconcile in flight, against a GM block sitting 647 tape away.

The pace panel Dave supplied the same morning (all models 69% used, Fable 82%, resets Thu 22:59) reads
**on pace**, which prices the other side: a second context is not free, and the cold-read fee is real.

⇒ **The split stands as the rule. It does not earn its keep on a job this small.** Recorded so the
next session does not re-derive it — and so that "use subagents" is not read as unconditional.

## Resolved state

- **Dave's band is RULED** (§1) and enacted **nowhere** — `_capture_gate.py` still fails at ≥45, and its
  wrap output still prints `≤ 45` while the code enforces `< 45`. Prose staler than its own code, the
  same shape #35 found in `_gm_move.py`. **First job for #37.**
- **No enactment this window, deliberately.** Re-priced at ~35 fill: offloads + honest wrap = ~56, with
  the register pushing ~64. Dave's call, and the throttle working as intended for the third session
  running — the difference being that this time it cut the job *before* the window was hot.
- **Still open, Dave's:** the three LS offloads + `LS:LIFECYCLE` de-materialise + the deferred register,
  with GM headroom planned up front · **the boot has never been measured by any session here** · the M10
  numbers, fourth session untouched · the `{17}`-literal siblings, unswept.

## What I got wrong

1. **Priced a wrap at 6 with no basis, against a measured 10 in the record.** Caught by Dave, not by me.
   The wrap is the one term with a measurement history; using anything else needs a reason.
2. **Read Dave's ruling back in the wrong shape** — "45 becomes a WARN, blocking line ~60" — which turns
   a *preferred band* into two thresholds. He corrected it. Had it been inscribed as read, the ledger
   would have carried a confident, plausible, subtly wrong version of a ruling about the very instrument
   that exists to prevent confident false inscription.
3. **Carried the plan's premise that the offloads relieve GM**, when #35's own ledger entry — one screen
   above where I was reading — records the GM half as already moved. The premise aged in four hours.
   [[premise-ages-faster-than-rule]], same week, same file.
