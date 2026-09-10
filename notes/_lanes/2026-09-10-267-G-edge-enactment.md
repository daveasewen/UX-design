# #267 lane G — enactment of s267-D3 (the 78 ratified ruling edges)

Ruling: `s267-D3` (knowledge/_rulings.json, last entry — NOT edited by this lane).
Input: `notes/_lanes/2026-09-10-267-E-edge-judgement.md` + `notes/_lanes/267/E/edge-recs.json`.

## DONE

**1 — authored store** `b858080`
- `knowledge/_ruling_edges.json` — 48 authored ruling→ruling edges + 31 `ratified_plain_mentions`.
- `knowledge/_gen_ruling_edges_from_recs.py` — the derivation, kept and re-takeable
  (`--print` reports without writing). Applies `dir` (one REVERSE, rec #40 → s172-D3 bounds
  s181-D1), takes `type` as ratified, retypes the nine Q1 rows to `supersedesClause`, and
  scans EVERY ruling for authored supersession FIELDS.
- Q1 nine: recs #5 #19 #34 #42 #52 #55 #64 #69 #70. The ruling's list and the lane-E list on
  `reviews/EDGE-JUDGEMENT-267-2026-09-10-v1.html:68` are IDENTICAL — no disagreement to report.
- Q2: rec #42 rewritten to the ACTOR — `s188-D1 → s183-D1`, with s188-D3 carried in `evidence`.
  Rec #41 stays a plain mention (lane E's REJECT). **Rec #19 is NOT rewritten**: the review page
  raised s162-D1 as the possible actor, but the store's own `s142-D1.superseded_note_s168_D1`
  field names s168-D1 as the closer, so actor and recorder are the same node. Declared, not hidden.
- The two edges lane E found missing are both present and both DERIVED, not typed:
  `s171-D1 → s129-D1` from the field scan (`source: "store-field:superseded_by"` — the only
  field-sourced row, printed as such by the script), and `s188-D1 → s183-D1` as the Q2 rewrite.

**2 — generator** `b5c54d2` · `knowledge/_build_kg_explorer.py` v1.9 → **v1.10**
- `:92` `ruling_edges()` reads the store; `:210-220` emits all 48 as `authored=True, derived=False`
  → SOLID. `supersedesClause` is a declared type: template `:159-165` FAMILY + READ entries,
  drawn in the SAME governance red as `supersedes` but DOTTED `[1.5,2.5]` (template `:266`).
  **Named choice:** dashed `[4,3]` is already the derived signal and must stay reserved, and the
  TWO-RED LAW (s151-D1) forbids inventing a third red — so the clause variant is a dot pattern,
  not a colour. The dig panel tags the group `RATIFIED S267-D3`.
- `:87` defect 1 — right boundary + inflection set `(?:s|es|d|ed|ing)?\b(?!\.[a-z])`.
- `:243-247` defect 2 — the ±80 window is clamped to the neighbouring mention ids.
- `:249` defect 3a — nearest verb wins, not dict order. `:255-259` defect 3b — a verb reading
  AFTER the mention proposes `t->s`.
- `:237` — the proposal loop skips any pair the store carries (authored `s/t` or `from_pair`) and
  emits no proposal on a `ratified_plain_mentions` pair.
- **Bite** `knowledge/_bite_kg_edge_proposal.py` — 15 cases, all green, driving the REAL
  `VERB_RX`/`MENTION_RX` and window arithmetic: "enactment", "override sets", "overrides.json",
  "NARROWEST", "correctly", "refinement" NOT verbs; "supersedes", "retired", "narrows",
  "enacting" ARE; a verb reaches only the FIRST id of a four-id list; both directions.
  MUTATION-PROVEN: restore the left-boundary-only regex and exactly the six noun/adverb cases turn red.

**3 — rebuild + drive** `ed1f930`
- `notes/_KG-EXPLORER.html`: nodes **2794 → 2794**, edges **4845 → 4845** — 48 derived `mentions`
  replaced one-for-one by 48 authored edges (mentions 284 → 236). Authored ruling edges drawn: **48**
  (extends 16 · supersedesClause 9 · enacts 6 · confirms 5 · refines 4 · supersedes 3 · narrows 2 ·
  bounds 1 · corrects 1 · retires 1).
- **PROPOSED after the fix: 0** (was 78). Report line: `PROPOSED TOTAL 0 (pairs already judged by
  s267-D3: 48 suppressed as authored, 31 ratified plain mentions)`.
- Playwright over `file://` (never `set_content`), headless Chromium 151:
  **0 console errors**; in-page probe `EDGES.filter(e=>e.ratified==='s267-D3').length === 48`,
  `supersedesClause 9`, `proposedType 0`; dig on `s151-D1` = 24 relations with its authored edge
  read back from the panel as `enacts IS ENACTED BY RATIFIED S267-D3 · 1 · s151-D2`.
  Script `notes/_kg-sweeps/267-G/drive_267_G.py`, receipt `drive-267-G.json`, screenshots
  `notes/_kg-sweeps/267-G/s151-D1-dig-v110.png` and `-dark.png`.

## NOT DONE (by rule, not by omission)

- **`notes/_PROPOSED-267-ruling-edges.html` NOT WRITTEN.** The generator proposes **0** new edges
  after the fix — every proposal it used to make is on a pair s267-D3 has already judged. Nothing
  to put on a page. This is the intended outcome, not a failure.
- `knowledge/gen_kg_edges.py` NOT touched and NOT run (⛔ lane-E RSQ 2 from #265 is unruled).
- No `_rulings.json` edit, no `_build_all.py`, no push, no stash.

## SEAM — two edge-type vocabularies now exist

`knowledge/gen_kg_edges.py` carries its own `DECLARED_EDGE_TYPES` for the COMPONENT graph; this
lane's `supersedesClause` was added to `_build_kg_explorer.py` + its template only. The two stores
are separate and neither validates the other, so a ruling-edge type is legal in the explorer and
unknown to `gen_kg_edges.py`. Left as found, per the fence. Whoever unrules RSQ 2 owns reconciling them.

## LIMITS DECLARED IN THE SOURCE (not swept under)

1. A regex has no part of speech: a bare infinitive ("supersede") is now missed, and a plural noun
   spelled like a verb ("the overrides") still hits — only the file-extension form is excluded.
2. The direction test reads only word ORDER. Passive voice and parenthetical citation
   ("CORRECTED BY … (see X)", lane E rec #1's shape) still read `s->t`, and a THIRD ruling named as
   the actor (rec #41's shape) is not detected at all — that case needs a human, as it got one here.
3. Lane E's defect 5 is only half addressed: the authored FIELDS are now read, but `MENTION_RX`
   still misses the `#NNN-DN` and `/D3` shorthand forms. Not in this lane's brief; still open.

## TOKENS (ESTIMATED)

Lane FILL ≈ **62K** — brief + ruling + lane-E file ≈ 9K, recs/store inspection ≈ 8K, generator +
template reading ≈ 14K, edits and build/drive output ≈ 16K, chromium install churn ≈ 5K, this
file ≈ 10K. Not measured via `message.usage` from inside the lane.

## RED

- `/sessions` was at **98% full (244M free)** — `playwright install chromium` failed ENOSPC into
  `~/.cache`, and needed `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw` (on `/`, 1.4G free) plus
  `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` to download at all. The
  `chromium-in-sandbox-recipe` hook needs both of those added, or the next lane loses the same
  ~10 minutes.
