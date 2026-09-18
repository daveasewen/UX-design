# #286 lane S — the standing file comes out of DRAFT

**Lane:** S (standing ratified) · **Session:** #286 · **Date:** 2026-09-18 · **Conductor:** Fable 5.1
**Working files:** `notes/_lanes/286/S/` (seam-BEFORE.txt, seam-AFTER.txt, close_w285sc.py)

Every claim below was run or read in-window. Nothing was committed or pushed. None of the four
fenced generators was run.

---

## 1. The rulings file

`notes/_lanes/286/DAVE-RULINGS-2026-09-18.md` — NEW, built to the shape of
`notes/_lanes/285/DAVE-RULINGS-2026-09-18.md` (read first: verbatim-quote bullets, a ⚠ marker
where a conductor's reading is separated from Dave's words, and a `## Still his` tail).

It records:

- The conductor's opener, which named **three** of Dave's open items — (1) the eight standing
  lines' wording, (2) how the accepted masters get registered, the `gen_kg_icons.py` fence,
  (3) the 256,000 wording fix in the gauge — plus the question of whether one cold-boot reading
  was enough.
- Dave's **whole reply**, verbatim: *"okay go on everything"*.
- **Explicitly**, that this is his word on **all three items** and on **running `gen_kg_icons.py`**
  (item 2 is the fence; standing line 2 names that generator as fenced on his word).
- **Explicitly**, that the conductor's READING of those six words — ratification of the eight
  lines *as written* — is **the conductor's, not Dave's sentence**. He did not say "as written",
  did not quote a line, did not say "ratified".

## 2. `knowledge/_standing.md` out of DRAFT

Header replaced only. The DRAFT block

> ⚠ **DRAFT — Dave's approval pending; nothing here is inscribed by this file.** …

became a ratified header naming #286, 2026-09-18, Dave's words *"okay go on everything"*, the
receipt path `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md`, and the re-quotes-never-inscribes rule.

**The eight lines were not touched.** Proof, from `git diff --unified=0 knowledge/_standing.md`:
every `+`/`-` line is inside the header block above the `---` rule; not one of the eight
constraint lines appears on either side of the diff.

`git diff --stat`:

```
 knowledge/_standing.md | 11 ++++++++---
 knowledge/_state.json  |  9 ++++++---
 2 files changed, 14 insertions(+), 6 deletions(-)
```

(`knowledge/_gauge_tokens.py`, `notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl`
are also dirty in the tree — **not this lane's**; the gauge file is #286 item 3's lane.)

### The seam, after the change

`python3 knowledge/_seam.py` → rc=0. Its STANDING block:

```
STANDING
Everything is delegated: the conductor orchestrates and judges; lane work done in-seat is a lapse (#57 / s204-D1, restated #284).
The four generators that undo hand-authored state — gen_kg_rules.py, land_rests_on.py, gen_kg_icons.py, _build_all.py single-process — never run without Dave's word (H-135 open 11).
Commits only through knowledge/_git_commit.sh, as a lane by default; push is the conductor's call with a CI read-back (H-135 move 3).
180,000 FILL is the QUALITY line and stands; 256,000 is not a wall for this model in Cowork (Dave's correction, #284).
Strike nothing from a carry without a receipt (s183-D1 / s188-D2).
Dave rules from plain prose and visuals, never ID codes; render readings side by side for a visual ruling (#66-D5, s172-D1).
Every sub files its full report at notes/_subreports/ (s218-D7).
A ruling is Dave's word inscribed; a proposal, a lane's finding or his enthusiasm is not one (s271-D4).
STANDING 8 lines · 246 cl100k
```

**8 lines · 246 cl100k — unchanged.** Measured, not asserted: the seam was run BEFORE the edit into
`notes/_lanes/286/S/seam-BEFORE.txt` and AFTER into `seam-AFTER.txt`, and
`diff <(sed -n '/^STANDING$/,$p' BEFORE) <(… AFTER)` returned **empty — IDENTICAL**.

Why the count could not move: `_seam.standing_lines()` (`_seam.py:100`) drops *everything up to and
including the first `\n---\n`* and prints every non-empty, non-`#` line after it. The edit is
entirely above that rule, so the printed body is byte-identical by construction — and the diff
confirms it rather than resting on the reading.

`python3 knowledge/_seam.py --selftest` → **`seam selftest: 7 arms, all GREEN`**, including the
STANDING arms (block present, block last, ≤ the 300 cl100k tail ceiling).

`python3 knowledge/_seam.py --help` is not a distinct surface — `_seam.py` has no `--help` that
differs from its docstring header; the block above is from the live run.

## 3. `W-285sc` closed through the store's own writer

**There is no `--close` CLI.** Measured: `python3 knowledge/_state.py --help` prints the module
docstring; `_state.py.__main__` (`:911`) handles only `--selftest` and otherwise **reports**
(`check()` + `counts()`). The module's write surface is the API — `load()` → mutate → `check()` →
`save()` — and `add()` is its only wrapper, which only adds. That load/mutate/check/save shape is
the sanctioned close every prior lane used (`notes/_lanes/276/W/carry277.py`,
`knowledge/_tmp/wrap241/mk_rows.py`). `_state.json` was **not** hand-edited.

The writer script is `notes/_lanes/286/S/close_w285sc.py` (dry-run by default, `--write` to save).
It ran dry first:

- `PRE check ok=True fails=0 notes=4` — the store was green before the change, so nothing below is
  a pre-existing failure attributed to this lane.
- `POST check ok=True fails=0` — the BLOCKING gate at `_state.py:478` (a row in `done` with no
  non-empty `closed_by` FAILS) passed.
- `save() would reorder items: False` — the `_sort_key` re-sort in `save()` is a no-op here, so the
  JSON diff is the row and nothing else. Confirmed by `git diff knowledge/_state.json`: 9 lines
  changed, all inside the `W-285sc` object.

**No refusal.** The writer did not refuse at any point.

### The row, after

- `state`: `open` → **`done`**
- `closed_by` (the receipt, verbatim as stored):

> #286 2026-09-18 — close condition met: Dave ruled the wording at #286. His words, verbatim:
> "okay go on everything", answered to a three-item opener whose item 1 was the eight standing
> lines. knowledge/_standing.md is out of DRAFT — header replaced, the eight lines byte-identical
> (git diff touches header only); the seam still prints STANDING 8 lines · 246 cl100k, unchanged.
> Receipt: notes/_lanes/286/DAVE-RULINGS-2026-09-18.md, which records that reading his six words as
> ratification-as-written is the CONDUCTOR'S reading, not Dave's sentence. No s286- ruling was
> inscribed in _rulings.json by this lane — inscribing is a separate act (s271-D4).

- `links` gained `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md` and
  `notes/_subreports/2026-09-18-286-S-standing-ratified.md` (the three existing links kept —
  nothing struck).
- `closes_when`, `title`, `home`, `owner`, `opened`, `project`, `condition`: **untouched**.

Store after, from `python3 knowledge/_state.py` (rc=0):

```
items 695 · live 589 · conditioned 681 · UNCONDITIONED 14
  by state: {'open': 589, 'blocked': 0, 'ruled': 0, 'done': 86, 'dropped': 0, 'parked': 20}
  live by owner: {'dave': 305, 'claude': 284}
```

(The 4 notes printed are the standing DECLARED-DEBT / coverage / project-split notes, unchanged by
this lane.)

## 4. No ruling inscribed

`knowledge/_rulings.json` was **not touched** — `git status --porcelain knowledge/_rulings.json` is
empty, and a key scan returns **no `s286-` keys at all**.

⬛ **Stated for the record: the ratification of `knowledge/_standing.md` is RECORDED (rulings file +
file header + closed store row) but NO `s286-` ruling was inscribed by this lane.** Inscribing is a
separate act — `s271-D4`, which is itself one of the eight lines: *"A ruling is Dave's word
inscribed; a proposal, a lane's finding or his enthusiasm is not one."*

## 5. Ruling-shaped things left open

1. **Whether an `s286-` ruling should be inscribed for the ratification** — this lane deliberately
   did not. If the conductor wants the standing wording to exist as an inscribed ruling and not
   only as a ratified file, that is a separate act with its own lane.
2. **⚠ STALE PROSE, found and NOT changed:** `knowledge/_seam.py:26` still reads
   *"⚠ `knowledge/_standing.md` is a DRAFT until Dave approves it; the seam re-quotes, it never
   inscribes."* — the first clause is now false. It is docstring only (no code path prints
   "DRAFT"), so nothing the seam emits is wrong; but the file that re-quotes the standing lines
   describes them as a draft. Left for the conductor: `_seam.py` was outside this lane's brief and
   its selftest is the thing that would carry the change.
3. **Item 2 of the opener — the master registration** — Dave's *"okay go on everything"* releases
   the `gen_kg_icons.py` fence (recorded in the rulings file), but **HOW** the masters enter
   `_logo_nodes.json` is still unshaped. #285's own rulings file left that as "still his".
   **This lane ran no generator.**
4. **Item 3 — the 256,000 wording fix in the gauge** — `knowledge/_gauge_tokens.py` is dirty in the
   tree; another lane's. Not verified here.

## Compliance

- No commit, no push.
- `gen_kg_rules.py`, `land_rests_on.py`, `gen_kg_icons.py`, `_build_all.py`: **not run**.
- Nothing struck without a receipt — the only removal anywhere is the DRAFT header block, whose
  receipt is Dave's words plus `notes/_lanes/286/DAVE-RULINGS-2026-09-18.md`.
- All working files under `notes/_lanes/286/S/`; `/tmp` not used.
