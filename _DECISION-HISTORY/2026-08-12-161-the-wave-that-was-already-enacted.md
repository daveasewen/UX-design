# #161 — the wave that was already enacted, and the two carriers that kept it alive

```
provenance: 161 · 2026-08-12
status: observed
```

*Narrative dossier for session #161 (Wed 2026-08-12). The terse records hold the WHAT —
`GOOD-MORNING.md`'s ★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST delta, `knowledge/_rulings.json`
(`s161-D1` · `s161-D2` · `s161-D3`), `knowledge/_state.json` (G3/G7/G8 closed, G18 opened). This file
holds the WHY and HOW. Both-way links: banner ↔ here; the three rulings ↔ here.*

*Shape of the session: a FABLE conductor, TWO Opus build subs, one Opus wrap sub (this file's author).
Quota at the open: session ~5% · weekly ~60% · Fable ~76%, resets Thu 10:59PM.*

---

## Finding 1 — the top item of the day did not exist

#160's wrap wrote, as `residual → #161` item ①, *"THE `s142-D1` WAVE STARTS ON A CLEAN FOUNDATION"*.
The auto-memory's `three-axis-model` hook said the same thing in different words. Two independent-looking
sources agreed, so the session opened with the wave as its job.

**The wave had been fully enacted at #143** — two sessions before the premise was written down.

The way it was found matters more than the fact. The build sub did **not** grep for a marker and declare
victory; it **re-derived the ruling row by row against the artefact**:

- **113 of 114 rows** carry a `$status` naming `s142-D1`.
- The **per-class counts match the ruling exactly** — C1 = 25 … C12 = 7, plus the 3 surface picks.
- **Every `bind:*` row has binds, and no no-bind row does.**
- ⇒ **delta = 0. Nothing was written.**

The one row that is not covered is **`tooltip.tip`**, which was never ruled. It is **staged for Dave**
and was deliberately not decided here.

### Why the premise survived two sessions

A carried residual line reads **identically** whether its subject is owed or already done. There is no
field in the format for "verified since", and the age bracket — `[0 — NEW TOP]` — measures how long the
*line* has been carried, not whether its *claim* is still true. That is the shape of
[[premise-ages-faster-than-rule]]: the derived rule ("do the wave") was fine; only its premise had
rotted, and nothing re-tests a premise.

The second half is the one worth banking: **the stale premise had TWO carriers.** Correcting only the
wrap residual would have left the memory hook to re-inject it at the next boot, and correcting only the
hook would have left #160's committed text to do the same. The conductor corrected the hook
(`s142-D1` now records **VERIFIED ENACTED at #143**); this wrap kills the residual. Fixing one carrier of
a two-carrier claim is not a fix — it is a delay. [[assertion-propagation-gap]]

### What is honestly still unproven

**Value-level aesthetic verification is Dave's eye, and no rendering was done.** The row-by-row derivation
proves the *bindings* are as ruled. It says nothing about whether the result *looks* right. That leg is
declared, not smoothed, and it is carried as a residual rather than folded into the closure —
a green that cannot see the question is not evidence about it. [[green-tests-cannot-see-scope]]

---

## Finding 2 — #160's declared debt, cleared, and what the re-run actually proved

#160 committed `knowledge/_STATE-CONTRAST-AUDIT.md` as a **4-snippet FILTERED artefact** (−302 lines) and
said so in its own banner: *"do not read it as the whole-tree record until it is re-run."* That declaration
is the reason this session could close it cheaply — the debt was named, not discovered.

The re-run itself hit the documented sandbox wart: **a 178-second call-boundary kill**. The recovery was
to chunk the work through a `/var/tmp` driver that calls the module's **own** `run()` and `render_report()`
rather than re-implementing them, then assert with the module's **own** `verify_report()` — which passed.
Re-implementing the report writer to work around a timeout would have produced an artefact that agreed
with a fresh instrument and with nothing else. [[sandbox-call-boundary-kills]]

Result: **74 → 311 lines, 75 sections.**

- **0 TEXT fails · 0 carrier fails · 0 refusals.**
- 82 declared-seat advisories · **32 icon warns** (worst **1.11:1**, Form-layout dark hover) ·
  15 MARK skips · **15 declared holes** (14 → 15; the new one an Alert hole).

The comparison that carries the finding is against the **#155 whole-tree record**, not against #160's
filtered one: **no new reds**, and **Banner's 8 TEXT fails are now 0**. That is `s149-D1`'s #158 mono-error
enactment confirmed **at scope** — the snippet-level green had already been seen, but a snippet gate cannot
tell you the whole tree agrees with it.

One side effect is disclosed rather than tidied: `knowledge/_graph-mark-observations.jsonl` gained **9
generated lines** during the sweep. The conductor left them to ride the commit. **No policy about that
file was invented** — whether generated observations belong inside a wrap commit is unruled, and it is
carried as an open question rather than settled by whoever happened to notice it.

---

## Finding 3 — three rulings, and one of them is a confirmation wearing a reversal's clothes

All three were Dave's, all after a read-back. `knowledge/_rulings.json` goes **124 → 127**.

### `s161-D1` — G8: retire completely

Dave's first answer, off the staged batch, was **"Pin"**. The conductor then surfaced something the batch
had not carried: the % band's enforcement was **already retired at #74-D3**, by Dave's own earlier
option-select, and the G8 item was pointing at retired residue (`knowledge/_capture_gate.py:125-137`).
It also gave the owed explanation — the band graded window fill as a *percentage*, and its purpose lives
on in the real-token path (amber 160K / working 200K / hard 256K).

Dave then ruled, verbatim: **"G8 retire completely"**.

The ordering is the lesson. A pick made from an incomplete set reads exactly like a ruling — and a ruling
recorded on top of an unsurfaced precedent would have re-litigated #74-D3 without anyone noticing it was
being re-litigated. The correction was to **surface the precedent, then re-ask**, so the outcome is
recorded as a **confirmation** of #74-D3 rather than as a fresh decision that happens to agree with it.
[[feedback-readback-sensation-not-mechanism]] [[invariant-cannot-discriminate-reversal]]

### `s161-D2` — G3: WARN, ratified *provisionally*

Dave: *"warn but lets return to thsi soon, I dont want any loose ends"*, then at read-back *"G3 good"*.

The agent-picked WARN tier (#86) is now his, consistent with #160's exit-code-exempt advisory precedent.
But "provisionally" is a word that evaporates unless something holds it: a provisional ratification with
no successor item is an un-ratification with extra steps. So **G18 was opened** — Dave's, closing when
*"Dave confirms warn as final or flips to block"* — and it carries the return-soon flag.
[[conclusions-are-debt-s129-d5]]

### `s161-D3` — G7: archive order ratified as-is

Dave delegated the pick: *"whatever makes most sense"*. The conductor **recommended** rather than hedged —
ratify as-is, because the convention (strata oldest-first, archives newest-first) is what every existing
archive already does, and the flip would rewrite history files for a symmetry nobody reads. Dave confirmed:
*"G7 ratify as is"*. [[feedback-best-practice-over-convenience]]

Store state after all three: **37 items · 34 live · Dave's 22 → 20**, gate PASS, each closure carrying a
`closed_by` receipt that names its ruling rather than merely asserting closure.

---

## Finding 4 — ENOSPC n=6: the pothole moved from symptom to remedy

Five previous sessions recorded ENOSPC as a recurrence. #161 is the first to change what the runbook
*tells you to do*, and both new facts are the kind that make an obvious remedy fail silently:

1. **Stale `/var/tmp` farms are undeletable across sessions.** They return owned by `nobody:nogroup` under
   the next session's uid mapping. `rm -rf` fails *Permission denied* on every file; `sudo` is blocked.
   You can still **read** them (point `PYTHONPATH` / `PLAYWRIGHT_BROWSERS_PATH` at them) but you can never
   reclaim their space. ⇒ **Do not budget a cleanup step. It cannot succeed.**
2. **`df` "free" lies to a non-root user.** `/` at 98% with ~223 M reported free still ENOSPCs on every
   write — the residue is root-reserved blocks. ⇒ **Treat any reading ≥ ~95% as ZERO free.** (Inodes were
   healthy at 11%; it is blocks, not inodes.)

Working recipe, n=6: always a **fresh session-suffixed target** —
`pip install --no-cache-dir --target /var/tmp/pylibs-s<n>` with `PYTHONPATH` pointed at it, `TMPDIR=/var/tmp`.

Written into `knowledge/_RUNBOOK-render-verify.md` **by addition**; the n=3/n=4/n=5 strata stand as history.
n=5 saw the sandbox reclaim a farm *mid-window*; n=6 sees what it cannot reclaim being orphaned. Same class,
seen from both ends. [[stale-mount-corroborates-a-stale-premise]] [[refusal-names-the-first-obstacle]]

---

## The resolved state, and what is still open

**Resolved:** the `s142-D1` wave is closed as a *job* (enacted #143, verified row-by-row here, delta 0) ·
the whole-tree contrast record is trustworthy again (311 lines, 75 sections, no new reds) · G3, G7 and G8
are closed with receipts · the ENOSPC remedy is inscribed at n=6 · the stale memory hook is corrected.

**Open, and all of it Dave's:** `tooltip.tip` (staged) · G18 (G3's return-soon half) · the value-level
aesthetic leg of the wave (nothing rendered) · 32 icon warns, worst 1.11:1 · 15 declared holes ·
82 declared-seat advisories and 15 MARK skips · whether `_graph-mark-observations.jsonl`'s generated lines
belong in a wrap commit · the 19 LEGACY unconditioned items · and every carry rolled forward on the
`residual → #162` list.

**This wrap ruled nothing.** The three rulings are Dave's, made in-window before this sub opened; no close
condition was invented for any G-item or LEGACY item; no ratified stratum was trimmed; `MEMORY.md` and the
auto-memory were not touched (step 3 is the conductor's, SKIP declared); `_build_all.py` was not run; and
nothing was pushed.
