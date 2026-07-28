# WORKER BRIEF — §A subdivision (the `gm:A` door is one atom)

**Cut:** 2026-07-28 (Tue evening), session #33, Opus conducting, Dave live.
**Lane:** `worker-a-subdivision` · **Role: WORKER.** No git. Receipt only.
**Conductor:** #33 (the session that cut this brief). It holds the write-lock on
`GOOD-MORNING.md` and `knowledge/_capture_gate.py`. **Do not touch either file.**

---

## Why you exist (read this, don't reconstruct)

#32 ruled, and Dave confirmed at #33's opener, that the **eager read chain (GM-D7-am) gets cut**:
the read contract had every session spend ~33K tk *before any question was asked*, so the working
255-record retrieval door could not save a token the contract had already spent. New chain =
header + ★ LATEST banner + `_LIVE-STATE` latest delta. **§A and §C stay in the file** and become
retrieval-on-demand via `knowledge/_memento_search.py`.

**#33 then measured the door and found a hole.** `--fetch gm:A` returns **15,869 bytes / 4,208 tk
cl100k — the entire §A, all or nothing.** §C is already granular (C1/C2/C2b/C3/C4/C4b/C5, 84–1,435
tk each) so §C's door is fine. §A's is not.

⇒ **A coarse door is not retrieval.** As it stands the cut moves §A from *paid every window* to
*paid in full on the first §A-shaped question* — "where does X live", "what are the four themes",
"what's the build command". Those are the commonest questions there are. **Your job closes that
hole, and without it the cut delivers a fraction of what it looks like it delivers.**

---

## The job

**Subdivide `§A` into its natural subsections so the door can serve one fact without serving all
of them.**

§A's subsections today are `##`-level headings inside the `# §A · ORIENTATION` region:

| subsection | rough size |
|---|---|
| the Memento framing blockquote + STANDING SECTION note (the §A preamble) | ~700 tk |
| `## What Apollo is` | ~180 tk |
| `## ★ ONE token store · ONE baseline library · FOUR themes` | ~640 tk |
| `## Where things live` | ~830 tk |
| `## The one command that matters` | ~90 tk |
| `## Rules that actually bite` | ~800 tk |
| `## Standing instructions for the agent` | ~430 tk |
| `## The other standing documents` | ~380 tk |
| `## Parallel-session model` | ~150 tk |
| `## Renders — REAL FONT, in-sandbox` | ~150 tk |
| `## How we work` | ~130 tk |

*(Sizes are #33's estimates from the section total — **measure them yourself**, don't inherit
them. A count is not a measurement.)*

### Where the mechanism actually lives

Do not guess at this — #33 traced it for you:

- `knowledge/_build_memento_index.py::parse_gm_ls` (line ~116) builds the `gm:*` / `ls:*` records.
- It does **not** use the generic `parse_sections` H2 splitter. It delegates to
  **`knowledge/_gm_usage.py`** — `GM_VOCAB`, `LS_VOCAB`, `split_sections(lines, vocab,
  unknown_check=...)`.
- So the section vocabulary is `_gm_usage.py`'s, and **that is your primary file.**
- `split_sections` has an `unknown_check` that **errors on unrecognised sections** — this is
  correct dv-004 shape (normalise once, fail loud on unknown, never enumerate). **Keep it.**
  Your change must not weaken it into silence.

### Your files (the fence)

**MAY EDIT:** `knowledge/_gm_usage.py` · `knowledge/_build_memento_index.py` and their selftests.
**MUST NOT EDIT:** `GOOD-MORNING.md` · `knowledge/_capture_gate.py` · `_LIVE-STATE.md` · anything
in `_GM-ARCHIVE.md` / `_LIVE-STATE-ARCHIVE.md`.

⚠ **The conductor is editing prose inside `GOOD-MORNING.md` in the same wall-clock window.** It has
undertaken not to add or remove any `##` heading there, so your vocab work and its prose work
cannot collide. **If you find yourself needing a heading added to GOOD-MORNING.md, STOP and say so
in the receipt — do not add it.**

---

## Constraints that will bite you if you skip them

1. **Backward compatibility of `gm:A`.** Something must still answer `--fetch gm:A`. Either keep a
   parent record or make the door resolve `gm:A` to a listing of its children — **your call, but
   state which you chose and why in the receipt.** A dangling id that used to work is a retrieval
   regression, and retrieval regressions are how #32 lost two sessions.
2. **`_gm_usage.py` also carries the section-usage instrument** (`PRIOR` referenced-never-consumed
   8/8, `C2b`/`C3`/`C4b`/`C5` unused 5 sessions running). **That instrument is #34's job, not
   yours.** If subdividing §A changes the shape of what usage reports, note it — don't fix it.
3. **Selftests are BUILD STEPS.** Every changed gate ships a selftest and wires it.
4. **★ Paired bites — the positive one is load-bearing.** Prove your splitter reports the RIGHT
   subsections on a good file *and* refuses a malformed one. A failure-only suite survives a revert
   that deletes the whole comparison. This is #32's lesson, learned the expensive way.
5. **Run the build, in ONE foreground ≤45s call:** `python3 knowledge/_build_all.py`. It must exit
   **0**. It was **red for two sessions and two wraps committed over it** — do not become the
   third. `nothing survives a tool-call boundary` in this sandbox; background jobs get reaped.
6. **The index is rebuilt LAST** (ritual step 2g). `_capture_gate.py::index_freshness_check` is
   BLOCKING and compares CONTENT, never mtime.
7. **`tiktoken` is NOT preinstalled** — `pip install tiktoken --break-system-packages`. Measure in
   **cl100k**, and **name the unit on every token number** (ds-021: charged ≈ ×1.55, provisional).

---

## Definition of done

- §A serves per-subsection records through `_memento_search.py` (search finds them; `--fetch <id>`
  returns one subsection, not the whole of §A).
- Measured before/after, both units: cost of a §A-shaped question then vs now.
- `python3 knowledge/_build_all.py` exits 0, with your selftest wired in as a step.
- Paired bites, positive one included, demonstrably failing when they should.
- **Receipt at `notes/_receipts/2026-07-28-a-subdivision-worker.md`** — header carries your
  context-gauge reading (scrutiny indicator, not a quality score), the measurements, the
  backward-compat decision you made, and anything you found that you did not fix.

**No git. The conductor reconciles and commits.** Reconcile every path — never a blind
`git add -A` with a worker live.

---

## If you find something

STOP, re-price, and fork to Dave — do not absorb it silently. #30, #31 and #32 all exceeded their
own projections; the ceiling has never once held. An unplanned finding is exactly where that
happens.
