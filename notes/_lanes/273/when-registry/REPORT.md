# REPORT — #273 lane WR: s273-D4 enacted — `when` is a REGISTRY, and the 13 names are defined

Written: `knowledge/when-fields.json` (textual span, two spans) + this lane folder. No commits. No ruling.

---

## 1. The 13 definitions, as written

Each carries `definition` + `kind` (the existing entry shape) **plus `example`** — s273-D4 requires
"one definition sentence + one example clause", and no existing entry had a place to put one, so
`example` is a new third sibling carrying the REAL clause, read off the meta.
*Flagging that as the one shape deviation for Dave: the 26 legacy entries are untouched and still
carry two keys only.*

| name | kind | definition | example (the real clause) |
|---|---|---|---|
| `baseline` | number | where the value axis of the bars starts (`0` = every column is measured from zero, so the bar heights are comparable) | `baseline = 0` |
| `primaryNavigation` | enum | whether the frame carries primary navigation (`absent` = it deliberately carries none) | `primaryNavigation = absent` |
| `breadcrumbs` | enum | whether the frame carries a breadcrumb trail (`absent` = it deliberately carries none) | `breadcrumbs = absent` |
| `search` | enum | whether the frame carries a search affordance (`absent` = it deliberately carries none) | `search = absent` |
| `exits` | count | how many deliberate ways out of the frame the person is given | `exits = 1` |
| `job.count` | count | how many jobs the frame is asked to hold at once | `job.count = 1` |
| `entry` | enum | what the person is asked to type into the control (`free text` = words they compose themselves, not a value chosen from a fixed list) | `entry = free text` |
| `full` | enum | what a FULL reading of the meter means (`BLOCKED, not done` = the cap is spent and the next action is refused) | `full = BLOCKED, not done` |
| `position` | enum | where in a flow the page sits | `position = end of an instruction` |
| `order` | enum | the fixed order the page's blocks are read in, where that order is the design argument | `order = message, then FACTS, then actions, then what-happens-next` |
| `cause` | enum | what failed (`404` the address is wrong, `500` something failed at our end) | `cause in (404, 500)` |
| `steps` | count | how many ordered steps the task is broken into | `steps >= 2` |
| `records` | count | how many already-happened records the reading carries | `records >= 2` |

`entry` appears on **two** metas (`input-fields`, `textarea`) — ONE definition covers both: both gates
open `entry = free text`; what separates them is the *prose* clause after it (one line vs more than
one line), which is not a field claim and is not parsed.

Sources: the clause itself (`_roles_drift.py --json` → `illegal_when_clauses`) and each meta's own
`purpose`/`when` prose in `knowledge/components/*.meta.json`. Nothing invented, no gate rewritten.

## 2. `$description` amended BY ADDITION

One paragraph appended inside the existing `$description` string, after s254-D2's paragraph, which is
untouched (the proof shows the old string is a strict PREFIX of the new one). It says: the list is a
REGISTRY under s273-D4; a lane may add a name by addition with a definition sentence and an example
clause, listed in its report; the resolver still refuses an undefined name (the #254 typo defence
stands); Dave sees additions at wrap; synonym drift is watched by the existing `_near_dupes.py`.

## 3. Proof — textual span, the `_inscribe_ruling.py` way

`notes/_lanes/273/when-registry/_proof.py` (run it with no argument for a dry run):

```
[OK] R2  removing both inserted spans gives back the ORIGINAL BYTES
[OK] A3a the result PARSES
[OK] A3b parsed diff in `fields` = EXACTLY +13 keys (13 added, 0 removed, 0 changed)
[OK] A3c the ONLY other change is `$description`, APPEND-ONLY (old string is a prefix): ['$description']
[OK] A3d every added name carries a definition sentence AND an example clause (s273-D4)
  bytes 5151 -> 7857   span1 521 at 634   span2 2185 at 5665
WROTE .../knowledge/when-fields.json
```

`git diff --stat` on the target: `knowledge/when-fields.json | 17 +++++++++++++++--` — two lines
touched, nothing reformatted. The file was never `json.dump`ed.

## 4. Near-dupe door

**`_near_dupes.py` cannot take a JSON of records without a code change** — its `main()` loads records
only from `knowledge/_memento-index.json` and filters by `kind`; there is no `--file` / stdin path.
Per the brief I stopped there: `_near_dupes.py` is unmodified and nothing new was built.
(Side note, not a request: its `min_shingles=3` at `k=8` would in any case skip one-sentence
definitions shorter than ~10 words.)

### Near-dupe candidates for Dave — spotted by reading, NOT merged, NOT renamed

| new name | existing name | why it is arguably the same thing |
|---|---|---|
| `records` | `rows` | "how many records the reading carries" vs "how many rows the reading carries" — near-identical wording; `records` is time-ordered history, `rows` is tabular, but the field claim reads the same |
| `entry` | `content` | `content` = "what an arrangement is being asked to hold"; `entry` = what the person is asked to type. Same question at two scales (arrangement vs control) |
| `exits` | `destinations` | both COUNT ways off the page; `destinations` is navigation targets, `exits` is deliberate ways out of a focused frame |
| `steps` | `parts` | both count the pieces a whole splits into; `steps` is ordered and enforced, `parts` is a composition |

## 5. Gates — verbatim

```
RESULT: FAIL (6)
```
(`_validate_roles_resolve.py`, was `FAIL (20)`. The 6 remaining are the `data-grid` `with` entries
without a slug, #261 — not this lane's, left alone.)

```
_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.
```

```
  `when`: roles.json 81/108 · metas 38/137 · metas whose gate uses a field OUTSIDE when-fields.json: 0
```

## 6. First obstacle

**The entry shape had no seat for an example clause.** The 26 existing entries carry `definition` +
`kind` only, while s273-D4 requires a definition sentence *and* an example clause. The brief said to
match the existing siblings exactly; matching exactly would have dropped half the ruling. I kept both
existing keys and added `example` as a third, and I am naming it here rather than deciding it —
if Dave wants the example out of the file, `_proof.py` regenerates the span without it.
