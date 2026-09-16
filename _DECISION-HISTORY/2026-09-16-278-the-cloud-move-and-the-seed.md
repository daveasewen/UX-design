# #278 — the cloud move and the seed

provenance: 278 · 2026-09-16
status: observed

*The WHY and HOW of a session that deliberately did no graph work. Spine entry: `_LIVE-STATE.md`
⏱ LATEST DELTA #278. Ledger: `knowledge/_rulings.json` § `s278-D1`. Handoff:
`_HANDOFF-129-the-cloud-move-and-the-seed.md`. Dave's words verbatim:
`notes/_lanes/278/DAVE-RULINGS-2026-09-16.md`.*

---

## The arc in one line

Dave opened on something he had noticed rather than on the worklist — *"I've noticed that Anthropic
have move the project to the cloud, can you let me know of any implications for this project before
we continue"* — and the whole window went on **measuring** the new environment instead of assuming
it. One open clause got its word on the way out. No lane ran, by design.

## Finding 1 — the move was real, and almost nothing moved

The Cowork memory directory became the claude.ai Project memory (import 2026-09-16 03:14–17Z,
`sources: [cowork-import]`). The tempting answer was "it's a storage change, carry on". The
conductor did not give that answer; he checked, item by item, and the **checking is the finding**:
sandbox (aarch64 Ubuntu 22.04), the FUSE mount, git, push, CI, the delete-guard grant, the chromium
recipe and tiktoken-first are **all unchanged**.

**Why it mattered to check rather than reason.** Dave's own posture named the risk: *"okay as long
as it's safe we have fallen foul of silent and creeping failures in the past"*. A creeping failure
is exactly the one a confident "nothing changed" produces — the claim reads identical whether it was
verified or assumed, and only one of those survives a month.

## Finding 2 — the rule did not change; it got a new place to point at

The recommendation Dave went with (*"okay, i have no choice really, lets do it"*) was: **the repo is
the record, cloud memory is the accelerator**. That is not a new rule. `_RUNBOOK-capture-ritual.md`
step 3 has carried it since 2026-07-18, in the pass that deleted the mirror. What the cloud move
changed is only where the accelerator lives.

**The dead end, recorded because it was tempting.** The obvious response to a store moving is to
write a new policy for it. That would have been a second source of truth for a rule that already had
one home — the exact shape step 3's own "THE MIRROR IS DELETED" ruling exists to prevent. What was
actually owed was one paragraph, by addition, recording the **seat pattern** the move made
structural. That is what this wrap wrote.

## Finding 3 — the boot index did not come across, and that is a measurement not a fault

The cloud store arrived as ~200 flat files and an **empty `index.md`**. The conductor restarted the
index with the #277 ★★★ line, newest-first, in the old `MEMORY.md` shape. The pre-import index is
preserved verbatim in `hook-overflow-2026-09-02-240` and `MEMORY-ARCHIVE`.

Three consequences were named rather than smoothed: the store is **account-wide on READ** and
**Apollo-only on WRITE**; the index file caps at **49,152 B**, so compaction is owed periodically
(the dream pass is its seat); and the forward risk is **one-way** — a re-import could overwrite
cloud-only lines. That last one is harmless *only while the repo holds everything durable*, which is
why the accelerator/record split is load-bearing rather than tidy.

⛔ **And a correction that belongs here because it was believed:** there is **no `MEMORY.md` in the
repo and there never was** — `git ls-files` reads 0. The old one was the Cowork LOCAL index. Every
line of the record that spoke of "`MEMORY.md`" was speaking about a file outside the repo.

## Finding 4 — the seat limit became structural

A delegated wrap sub cannot reach the memory store at all. That was true at #275 and #276 as a
circumstance of where the store sat; after the move it is **structural** — only the conductor's seat
can write it. The pattern that answers it was already proven: the sub writes
`notes/_lanes/<n>/WRAP-MEMORY-HOOK.md`, and the conductor places it at the **next** opener, at a cold
seat, for roughly 4K tokens. `d7b8d72` did exactly that for #277's hook.

**Why this is a runbook line and not a banner line.** It is a rule about how the ritual runs, and a
rule that lives only on a rolling banner is a rule with a death date — the 2c EXIT CHECK exists
because that has already happened. It went into step 3 **by addition**; no existing line was
rewritten.

## Finding 5 — the boot number Dave asked for, answered as a measurement

He asked directly: *"BTW what is the boot measurement it way over the 70K now isnt it?"* The honest
answer was **72,110 real, n=1**, against the `s129-D1` floor of 70,794 — **+1,316**, inside noise
plus a hair. Not "way over".

**What was NOT done, and the restraint is the finding.** A single reading is not a band. The floor
was **not re-based**, `BOOT_FIRSTTURN_TK` was **not touched**, and the n was published as n=1. What
genuinely needs correcting is the floor's *label* — it should read "cloud listing replaces
MEMORY.md" (≈8K either way) — which is a wording fix to a description, not a move of a constant.
Moving a ceiling to fit a measurement is the one thing `s240-D2`/`s241-D1` forbid outright.

## Finding 6 — the clause got its word

`s277-D13` had recorded a question as a question: does the thin slice persist in the session, and
should the graph be an on-demand RAG? The conductor's read-back answered *no and yes*. Dave's word
on it was *"Ill go with you, lets just move on to the other graph work"*.

Inscribed at this wrap as **`s278-D1`**: the thin slice is a **SEED** — composed once at step 1 by
`_compose_slice.py`, after which the session works from its own state — and **ASK is the on-demand
door**, called mid-session when the designer's next prompt needs a node the seed excluded, reading
the Constitution **live** so that a ruling inscribed *after* the seed was composed is still
answerable. Seed and door under one contract; neither replaces the other.

**Why the shape matters.** The alternative — a slice that stays live against the graph — sounds
safer and is strictly worse: it re-pays the 415K-token read `s277-D10` exists to avoid, and it makes
the session's state depend on a file that can move underneath it mid-flight. The seed is cheap and
stable; the door is the escape hatch, and it is the half that reads the Constitution rather than a
snapshot of it.

## What is resolved, and what is still open

**Resolved:** the environment is measured, not assumed · the accelerator/record rule has its new
pointer · the step-3 seat pattern is inscribed · `s277-D13`'s clause is law as `s278-D1`.

**Open, and Dave's:** the `/sessions` disk at 96.6% (nothing in the repo fixes it; the symptom is a
session that will not start) · cloud-index compaction, unscheduled · the one-way re-import risk ·
the boot floor's label · and the whole of #279's first moves, which are #128's, unchanged — land the
icons, then the Constitution wave, with `s278-D1` now an input to the reader lane.
