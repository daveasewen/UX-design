# #167 — the eighteen fails, the scoped palette, and the cap nobody ruled

provenance: 167 · 2026-08-13
status: observed

*Narrative dossier (capture-ritual step 1b) for session #167 — FABLE conductor + OPUS subs + this
OPUS wrap sub, Dave live. **One ruling, Dave's: `s167-D1`.** The terse WHAT lives in
`knowledge/_rulings.json`, the ★ LATEST banner of `GOOD-MORNING.md` and the ⏱ LATEST delta of
`_LIVE-STATE.md`; this file holds the WHY and HOW, including the corrections.*

---

## 1. The carried residual was wrong before it was repaired

#166 handed over residual ① as *"the 15 provenance fails on `s157-D1`…`s163-D1`"*, targeted at the
Friday 2026-08-14 housekeeping session. The first act of #167 was not to fix them but to **re-measure
the premise**, and the premise did not survive: `python3 knowledge/_governs.py --selftest` reported
**18 fails across 10 rulings spanning `s157-D1` → `s166-D1`**, not 15 across seven.

The gap is explained by *when* each number was taken. The 15 was measured at #164, the session that
discovered `_build_all.py` had been dying before step 1 since #158 — so the count was true of the
store **as it stood at #164**, and three further sessions minted rulings into it afterwards. ★ The
carried item aged into a false statement without anyone touching it: a count is a measurement with a
timestamp, and a residual carries the number while dropping the clock
[[premise-ages-faster-than-rule]] [[planning-estimate-is-not-a-measurement]].

The 18 fell into two classes, and the split is what made them ratifiable in one sitting rather than
eighteen:

- **11 missing-field fails** — `governs` / `evidence` / `status` absent on `s157-D1`, `s157-D2`,
  `s158-D1`…`s158-D4`, `s160-D1`.
- **7 form fails** — a field present but not in the legal shape: prose evidence with no `chat #N` /
  `commit <sha>` pointer, plus **one rotted path**.

## 2. Three questions were Dave's, and they were asked as questions

Authoring provenance for someone else's rulings is inventing the very thing the gate checks, so the
three places where the record was genuinely ambiguous were put to him rather than filled in:

1. **The 7 form fails** — ratified as a **batch**, since the repair is mechanical (attach the legal
   pointer that already exists in the record).
2. **`s157-D2`'s `governs` scope** — it could plausibly claim the palette files. Dave ruled it
   **NARROW**: the brief plus `_themes.json` only; **`s158-D4` owns the palette files**. Two rulings
   claiming one artefact would have made the register lie about ownership.
3. **`s160-D1`'s status** — the ruling's own text settled *"do the rename as is"*, i.e. **keep the
   names**, and **no rename commit exists**. So its status is **no-op wording**, not an owed
   enactment. ★ This is the stale-top-item shape the `s161-D4` fence exists for: the honest reading
   came from the ruling's own words, not from a later session's memory of it.

All 18 were then enacted **textually** in `knowledge/_rulings.json`. One draft path was corrected
during inscription — a `governs` entry on `s158-D1` written as `canon/…` where the real path is
`knowledge/canon/…`. It was caught by re-reading, and it is recorded here rather than smoothed,
because a rot-detector fed a mangled path is exactly the conflated repair `_governs.py`'s own #164
fix refused to make [[conflated-fix-guarantees-recurrence]].

**Receipt:** the gate re-run by the conductor — `rc=0`, **0 fails**, entries **137 → 138**, JSON
valid.

## 3. `s167-D1` — palette sharing is SCOPED, not per-theme-individual

Dave reviewed a **live palette-tier visual** and said *"thats all correct"*, then *"all of these
decisions are fine to mint right now"*. The ruling **ratifies the as-built shape** of `s157-D2` /
`s158-D4` rather than changing it:

- **RAG:** legacy owns its own · mono owns its own · **console + supercharge SHARE**.
- **Neutrals:** legacy owns its own grey · **mono + console share the mono ramp** · supercharge owns
  its warm ramp.

Two vocabulary points were settled in the same breath, and they matter because both had been drifting
between surfaces: **status ≡ RAG are interchangeable** (his word), and **"main palette" means the
base semantic tier** (mono `activeBase`).

⚠ **The floated clause is kept in its own register and NOT flattened into the ruling.** Dave floated
that the palette shape *"might not be the final shape"*. That is **floated**, not ruled: a future
reshape is a **NEW ruling**, never a re-opening of this one. `s167-D1` records the clause so the
option stays visibly open without the ratification being read as provisional
[[memento-three-registers]] [[feedback-dont-launder-a-premise-into-a-ruling]].

## 4. The 400-char cap nobody had ruled

#166's residual ⑦ said `_state.json` bodies truncate at 400 characters, with **7 of 37 items sitting
exactly on the cap** — i.e. under-read by construction. The first question was not "remove it?" but
**"who ruled it?"**, because a cap with a ruling behind it is a decision and a cap without one is an
accident.

**Four named probes were run and none matched.** The cap lived at
`knowledge/_migrate_state.py:127` with no ruling id, no ledger line and no ADR. The nearest adjacent
precedent runs the **other way**: `notes/_MEMENTO-DECISIONS.md:438` records the **retirement of a
140-char cap**. ★ Saying the searches were run, and naming them, is what makes the absence a finding
rather than a shrug [[unrun-search-indistinguishable-from-absent-record]].

The repair:

- cap **removed at source**;
- the 7 clipped bodies **re-derived from source by exact-prefix match** — never re-authored — and
  written through `_state.save()`, with a **round-trip byte-identical proof** taken first
  [[serializer-defaults-reformat-the-file]];
- `_state.py` selftest **32/32 green**;
- dashboard regenerated via `gen_dashboard.py` (the sanctioned scoped repair, not `_build_all.py`),
  `--check` **OK**;
- of the diff, **48 lines were pre-existing #166 drift and 250 were this regen** — attributed rather
  than reported as one number [[attribute-the-diff]].

**The consequence was declared, per `s165-D1`, not discovered later:** the dashboard's **PROPOSAL
ranking moved for those 7 rows**, because the effort proxy now reads true body lengths. **Nothing
ratified moved** — the score is a proposal, regenerated every build, never written back. It still
needs Dave's eye at the next dashboard sitting, and it is carried as a residual for that reason.

## 5. The residual discovered while repairing a residual

Every one of the 7 repaired items carried a **stale `home` pointer** into `GOOD-MORNING.md:LN`. Five
of those lines now live in `_GM-ARCHIVE.md` (~1238–1246); two are in the current GM at 101 / 105.

★ **The store's provenance pointers rot as GOOD-MORNING rolls** — the same class as *a dated home is
not a home*, but pointed the other way: here it is a **standing store** pointing INTO a **rolling
surface**, so the ritual that keeps GM cheap is the same ritual that breaks the store's citations.
Untouched and out of scope for this session; carried as a new residual so it is countable rather than
re-discovered.

## 6. T2 — a crash is not a fail

`selftest_growth` raised `ModuleNotFoundError` without `tiktoken` at `_capture_gate.py:5307`
(pre-edit), and the cost was not the arm itself: the raise **killed the whole suite**, so every later
arm was unreachable and the run reported nothing about them at all. ★ A crash and a fail are
different states and only one of them is informative [[a-crash-is-not-a-fail]].

Fixed to a **named refusal in the `MeasurementRefused` idiom**: it states what is missing, what is
**UNPROVEN while it is missing**, and the install recipe. **Mutation-proved in both directions**, and
the full selftest **with** `tiktoken` is `rc=0`, unchanged — the control that the fix did not quietly
alter the measured path [[mutation-tests-the-clause-not-the-feature]].

## 7. What is still open

- The `s165-D4` per-line link ratification — **0 of 37**, and per-line, and **his**.
- `priority_override` / `deadline` / `effort` **values** — schema gated, values unauthored.
- The `_REVIEW-SIGNOFF.md` queue, incl. the 42-verdict controller and the v3 designer-community deck.
- The dashboard **v2** lane (`s165-D6`).
- The new **home-pointer rot** class (§5) and the **moved PROPOSAL ranking** (§4).
- The palette **reshape** option, floated by Dave and left floated (§3).

## 8. Environment, recorded rather than smoothed

Sandbox root ran at **99% full (162M free)**; `TMPDIR=/var/tmp` was needed for `tempfile`. The
obvious reclaim is **~1.7G of stale `/var/tmp/pw-browsers-*` from old sessions** — **left untouched**,
because deleting another session's artefacts on a hunch is not a repair. `tiktoken` recipe that
worked: `pip install tiktoken regex --no-deps --break-system-packages --target /tmp/pylibs` with
`PYTHONPATH=/tmp/pylibs`.

---

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #167 · ledger: `knowledge/_rulings.json` § `s167-D1`
(138 entries, tail) · banner: `GOOD-MORNING.md` ★ LATEST #167.*
