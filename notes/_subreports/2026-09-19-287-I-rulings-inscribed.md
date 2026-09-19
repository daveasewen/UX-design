# #287 LANE I — THE TWO #286 SENTENCES ARE INSCRIBED (s287-D1, s287-D2)

provenance: 287 · 2026-09-19 · lane I · sub Opus 5 (1M)

**VERDICT: DONE.** Both rulings inscribed through the sanctioned writer, `notes/_RULINGS.html`
re-rendered fresh in the same change (the #283 lesson), the stale DRAFT claim in `_seam.py`
amended, `_standing.md`'s header brought onto the ruling. 620 → **622** rulings. No commit made
(a separate lane commits).

---

## 1. WHAT DAVE SAID, AND WHAT MADE IT A RULING

- #286, 2026-09-18, whole reply to a three-item opener: ***"okay go on everything"***
- #286, 2026-09-18, on the shape of a master registration: ***"okay size-on-the-existing-node"***
- #287, 2026-09-19, item 1: ***"inscribe"*** · item 2: ***"keep `sizes` and rebuild."***

⛔ The join is named on the face of `s287-D1`, not smoothed: reading *"go on everything"* as
ratification-**as-written** was the **CONDUCTOR'S** reading at #286. The word that makes it his is
*"inscribe"*, said on 2026-09-19. Same discipline on `s287-D2`: the key name `sizes` was lane R2's
reading of the file's plural vocabulary until *"keep `sizes` and rebuild."* made it his word.

## 2. THE INSCRIPTION — THE SANCTIONED TOOL, NO HAND-EDIT

`knowledge/_inscribe_ruling.py` did both, `--dry-run` first then `--write`. No fallback hand-edit
was needed; the schema is the tool's own `KEYS` (id/ruled/date/by/says/governs/evidence/status).

```
DRY RUN — would insert cleanly, NOTHING WRITTEN: s287-D1 — textual span of 1766 bytes at offset
  882860; file 882865 → 884631 bytes; rulings 620 → 621; reconstruction proof PASSED.
INSCRIBED: s287-D1 — … rulings 620 → 621; reconstruction proof PASSED (all other bytes identical).
DRY RUN — would insert cleanly, NOTHING WRITTEN: s287-D2 — textual span of 1763 bytes at offset
  884626; file 884631 → 886394 bytes; rulings 621 → 622; reconstruction proof PASSED.
INSCRIBED: s287-D2 — … rulings 621 → 622; reconstruction proof PASSED (all other bytes identical).
```

**s287-D1** — the eight standing lines ratified as written, `_standing.md` out of DRAFT, the seam
re-quoting them at its tail, and the 256,000 wording fix in `_gauge_tokens.py` as HIS.
`governs`: `knowledge/_standing.md` · `knowledge/_seam.py` · `knowledge/_gauge_tokens.py`.
`evidence`: the two DAVE-RULINGS files (#286, #287).

**s287-D2** — a per-size master is a **SIZE FIELD on its lockup's existing node** in
`knowledge/_logo_nodes.json` (the actual path, confirmed by grep: `nodes[].sizes`, a map of raw
height `24/28/32/36/40` → master record, merge-on-write), never its own node and never a new kind;
node count does not move — **8 nodes / 33 edges at inscription**, read by `json.load` at this seat.
`governs`: `knowledge/_logo_nodes.json` · `knowledge/assets/logos/_gen_masters.py` ·
`knowledge/_build_kg_explorer.py`.
`evidence`: the two DAVE-RULINGS files + `notes/_subreports/2026-09-18-286-R2-masters-registered-as-sizes.md`.

## 3. THE STALE DRAFT CLAIM — `:44`, NOT `:26`

⛔ **Reported as asked: the sentence is at `knowledge/_seam.py:44`, not `:26`.** The #286 wrap brief
located it at `:26`; this seat measures `:44`, agreeing with `_HANDOFF-137`'s own second reading.
Both readings are published; neither is rewritten.

Only the first clause was amended, and the second half survives verbatim:

```
-⚠ `knowledge/_standing.md` is a DRAFT until Dave approves it; the seam re-quotes, it never inscribes.
+⚠ `knowledge/_standing.md`'s eight standing lines are RATIFIED AS WRITTEN by Dave (`s287-D1`, 2026-09-19
+— the file is no longer a draft); the seam re-quotes, it never inscribes.
```

`_standing.md`'s header no longer calls the ratification the conductor's reading in the present
tense: it now cites `s287-D1` and *"inscribe"*, while **keeping** the record that the #286 reading
**was** the conductor's. The eight lines below the `---` rule are untouched. Nothing else in either
file was changed. `python3 -m py_compile knowledge/_seam.py` passes.

## 4. THE HTML — RE-RENDERED IN THE SAME CHANGE

```
wrote notes/_RULINGS.html  622 rulings  160 sessions  1111483 bytes
  sha256 a3f4ff98249bb301484b899e59b27e1160bd315e9bdc9e8c5ddcf0bb51f70557
--check → FRESH  _RULINGS.html matches _rulings.json sha256 a3f4ff98…
```

## 5. VERIFICATION (json.load at this seat, not taken from tool prose)

```
count: 622
s287-D1: True   s287-D2: True
dupes: none
html s287-D1: 3 occurrences   s287-D2: 4 occurrences
```

`python3 knowledge/_validate_kg.py` → **OK**: *"every ref parses+resolves, every null carries a
note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the
s135-D4 resolutions input was consumed."* (139 metas checked · 90 `ref:null`+`$note` · 82 ruled
verdicts asserted present.) Nothing outside lane scope was fixed.

## 6. EVERY PATH TOUCHED — `git diff --stat`

```
 knowledge/_rulings.json | 35 ++++++++++++++++++++++++
 knowledge/_seam.py      |  3 ++-
 knowledge/_standing.md  |  8 ++++---
 notes/_RULINGS.html     | 57 +++++++++++++++++++++++++++++---------
 4 files changed, 87 insertions(+), 16 deletions(-)
```

⚠ **Two further paths moved as INSTRUMENT SIDE EFFECTS, not lane edits** — appended to by the
tools' own help-gate/logging on invocation, +2 lines each:
`notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl`. Named here so the
committing lane is not surprised by them.

## 7. NOT DONE / STILL OPEN

- ⛔ **No commit** — a separate lane commits, per the brief.
- The forbidden generators (`gen_kg_rules.py`, `land_rests_on.py`, `gen_kg_icons.py`,
  `_build_all.py`) were **not** run.
- `s287-D2` names the KG explorer rebuild as his word; **this lane did not rebuild it** — out of
  scope here, and `knowledge/_build_kg_explorer.py` is untouched. The ruling now governs it, so the
  rebuild is owed by whichever lane holds item 2.
- Item 3 of #287 (*"do it"* — the 58 prose locations calling 256,000 a wall) is **not** this lane's
  and is untouched. Note that the `ruled` text of `s287-D1` states 256,000 is *not a wall for this
  model in Cowork*, so it is already consistent with that correction.
