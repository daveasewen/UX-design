# 2026-08-07 · #118 — The wiring seam: a proof case that was false, and the class behind it

```
provenance: 118 · 2026-08-07
status: observed
```

> **Both-way links.** Spine: `_LIVE-STATE.md` ⏱ LATEST DELTA #118 · `GOOD-MORNING.md` ★ LATEST #118.
> Standing homes: `GOOD-MORNING.md` §C·2 (the open question, verbatim) · §C·4 (the four orphans + the
> wiring-gate spec). Measurements: `notes/_GAUGE-LOG.md` § #118 additions.
> Primary sources, written in-window by the conductor and committed with this file:
> **`_TRIAGE-118-bucket-sort-v1.md`** (the sort Dave asked to see before I acted) and
> **`_HANDOFF-118-the-wiring-seam.md`** (the forward plan).
>
> ⚠ **PROVENANCE OF THIS DOSSIER, STATED PLAINLY.** It was written at the wrap by a **delegated Opus
> sub that was not in the conductor's window.** The arc below is reconstructed from those two
> in-window artefacts plus first-hand measurement of the repo at wrap time — **not from lived
> reasoning.** Where a figure is this sub's own measurement it says so; everything else is quoted.

---

## Why this session existed

Dave had asked for a decision-backlog triage **twice** — at #57, and again at #117 with
*"this has to happen."* #117 produced an inventory of 17 open items with a first-guess bucket
attached to each, and a claim: **"roughly half this list was never Dave's."** #118 was opened to
prove or refute that claim, and Dave's own opener set the method:

> *"Show me the bucket sort before you act."*

That instruction is the reason the session has a defensible finding rather than a tidy one. The sort
was produced as a **floated** artefact with nothing enacted, and the one item that could not be
sorted without his word was carried to him as a question rather than absorbed as a decision.

## Finding 1 — the sort holds, and the counter-evidence is stated beside it

Of the 17 inventoried items: **8 are (B) mis-escalated — Claude's to take back · 1 is (C) stale ·
bucket (D) is Claude's work entirely** ⇒ **8 remain genuinely Dave's, and 2 of those are blocked on
Claude, not on him.** The #117 claim **holds**.

**And the same file states what weakens it:** *"I sorted 9 of the 17 on their nature without probing
them."* Every one of those went to A or B on a judgement call. That admission is not decoration —
finding 2 is the proof that such a judgement can be wrong in three directions at once, which is
exactly why #119 is instructed to probe before enacting any unprobed row.

## Finding 2 — the proof case was false, and it was false in three different directions

`_HANDOFF-117` had named `_validate_type_composites.py` as bucket D's specimen:
*"The gate has never been built… three months of knowledge, zero enforcement."*

Driving it produced the opposite of every claim on file:

| Claim on the record | What driving it showed |
|---|---|
| "the gate has never been built" | **Built 2026-07-18** — `knowledge/_validate_type_composites.py`, 10,602 bytes |
| implied: it does not work | `--selftest` → **OK**; three checks (TYPE-001/002/003), Dave's own 2026-07-17 scope ruling encoded |
| implied: it cannot fail | true exit code **1** — **1,101 violations across 90 of 90 files** (81 real component snippets, 9 demo) |
| `MEMORY.md`: *"the gate is a TODO, NOT built"* | **FALSE** |
| #117: archived the hook *claiming a gate enforced it* | **FALSE, the other way** |

⇒ **Three records described one file's state wrongly, in three different directions, for three
weeks, and nobody ran it.**

**The gate is not missing. It is UNWIRED** — no reference to it exists in `_build_all.py`, while
twenty-odd sibling validators sit in that list.

★ This **sharpens** bucket D rather than refuting it. #117's diagnosis was *knowledge does not
throttle behaviour*. The truth is more specific and worse: **the gate was written, and writing it
changed nothing, because it was never connected to a consumer.** Building the instrument was never
the hard part — **wiring it was, and wiring is the one step with no gate on it.**
[[instrument-without-a-consumer]] · [[premise-ages-faster-than-rule]]

## Finding 3 — it generalised to a class, and only *driving* the class told us anything

A count of orphaned validators was cheap: **29 `_validate_*.py` on disk, 25 wired, four orphaned.**
The count was also almost useless, because **each of the four failed for a different reason**:

| Validator | Written | `--selftest` | Live run | Diagnosis |
|---|---|---|---|---|
| `_validate_compose.py` | 2026-08-05 | rc=0 PASS | rc=0 PASS | ✅ **Pure oversight.** Green, harmless, two days old — wire it, zero risk |
| `_validate_type_composites.py` | 2026-07-18 | rc=0 OK | **rc=1**, 1,101 violations / 90 files | ✅ Works, fails **honestly**. Real debt. **Tier is Dave's** |
| `_validate_screen.py` | 2026-06-29 | rc=1 CRASH | rc=1 CRASH | ⛔ **ROTTED** — `ValueError: too many values to unpack (expected 3)`; a data shape moved under it |
| `_validate_state_contrast.py` | 2026-07-03 | rc=1 CRASH | rc=1 CRASH | ⚠ `ModuleNotFoundError: playwright` — **environmental, not logical** |

★★ **The lesson, and it is the reason #119 is forbidden from sorting these off the table above:**
one oversight, one rotted, one environmental, one real, and **no count could have separated them.**
[[green-tests-cannot-see-scope]] · [[a-crash-is-not-a-fail]]

⚠ A near-miss worth keeping: the type gate was almost mis-read as *"reports FAIL but exits 0"*,
because `$?` after a pipe is the **pipe's** exit code. Capture rc with no pipe, or use `PIPESTATUS`.

## The one question that was NOT answered, and why it was not absorbed

Wiring the type gate is mechanical. **Choosing its tier is not.** As put to Dave:

> **(a) BLOCKING now** — honest; the build goes red immediately on 1,101 violations, and nothing
> else ships until they are fixed.
> **(b) SHRINK-ONLY RATCHET at 1,101** — enforcing today against any new violation, with the
> existing debt declared and drawn down.

**Claude recommended (b) — and named the argument against its own recommendation, unprompted:**
*a baseline set to today's count has exactly the shape of "a cap raised to clear its own gate."*
The claimed difference is that it may **only shrink** and is declared as debt rather than absorbed
as a pass. **If Dave does not buy that distinction, (b) is not defensible and (a) is what is left.**

**He did not rule, and the question stays his.** It is recorded verbatim at `GOOD-MORNING.md` §C·2,
and neither the conductor nor this wrap sub answered it. ⚠ If (b) is ever ruled, the baseline must
be **re-measured at the moment of wiring** — `1101` is a measurement with a date on it
[[measure-dont-convert-units]] · [[feedback-dont-launder-a-premise-into-a-ruling]].

## The dead end, and it is the session's second seam

**#118's opener told Dave two things that were false:** that #117's work was *"committed nowhere"*,
and that **8 structural fails** stood. Both were false — #117 had been committed at **`675a626`**
(Aug 6, 21:30), the chain routed to #118, and structural fails were **0**.

**Cause: the mount served `_CHAIN.md` at its 20:03 state while disk held 21:30.** The handoff's
premise and the stale file **agreed with each other**, and that agreement read as corroboration.

★★★ **A stale mount looks like a quiet repo, and two stale sources corroborating each other feel
like verification.** Corrected in-session, unprompted.

⬛ **This seam is spec'd nowhere and may have no gate available.** #118 named two seams — the wiring
seam and the stale-mount seam — and built neither. The wiring gate is spec'd and buildable. The
stale-mount seam is not, yet. **If #119 cannot gate it, the honest move is to say so plainly and
retire it, rather than carry it forward as a reproach.**

## Resolved state at the end of #118

- ✅ The triage **ran** and is floated, not enacted: `_TRIAGE-118-bucket-sort-v1.md`.
- ✅ The #117 claim **holds**; the counter-evidence (9 unprobed rows) is declared beside it.
- ✅ #117's compaction-figure contradiction is **settled on disk** — measured at this wrap:
  `MEMORY.md` **19,088 bytes · 107 entries · mtime 2026-08-06 20:53**, i.e. still #117's own write
  ⇒ `_HANDOFF-117` was right and `notes/_GAUGE-LOG.md`'s post-mortem was wrong (18,367 / −12.1% /
  105). **Corrected by ADDITION; #117's lines left verbatim** [[assertion-propagation-gap]].
- ⛔ **Nothing was enacted from the sort**, and **no orphaned validator was wired.**
- ⛔ **Nothing on the DO-NOT-RULE list was touched**, no cap was raised to clear its own gate, and no
  error bar was widened. The pre-existing 32.9-vs-32 red in `_validate_behaviour.py` is left RED.

## What is still open

1. **Build the wiring gate** — the seam is *the moment a `_validate_*.py` lands on disk without an
   entry in `_build_all.py`*. It must ship with its own bite-test and be **wired in the same pass**;
   a wiring gate that is itself unwired is a joke that writes itself. Mutation-test **detection and
   remediation separately** [[mutation-tests-the-clause-not-the-feature]].
2. **Wire `_validate_compose.py`** (green, zero risk), then the other three per their diagnosis —
   **re-driven, never sorted off the table above.**
3. **The type gate's tier — Dave's, open.**
4. **The stale-mount seam** — gate it, or retire it and say so.
5. The rest of bucket B, tabulated with its verified state in `_HANDOFF-118-the-wiring-seam.md` § ③.
