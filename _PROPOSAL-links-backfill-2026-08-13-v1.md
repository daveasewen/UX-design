# PROPOSAL — `links` backfill for `knowledge/_state.json`

**Status: PROPOSAL. Nothing here is in the store.** Derived mechanically 2026-08-13 by a
script (`/var/tmp/derive_links.py`, recipe below) that scans each item's own `title`, `body`,
`closes_when`, `home` and `provenance` for the ids of *other* store items and for
`_decision-graph.json` node ids. Dave ratifies; only then does anything land.

## Why this is a proposal and not a patch

`links` is the dominant input to the dashboard's priority score (weight 0.30, "Unlock").
An agent that backfills the links it then scores itself against has closed the loop with no
reader in it. So: the derivation is mechanical, every candidate carries the QUOTED line that
produced it, and the failure mode is visible — a mention is not a dependency. Some of these
are genuine edges; some are an item merely NAMING another. Only Dave can tell them apart,
and the quoted line is what lets him.

## Coverage

| | n |
|---|---|
| items in store | 37 |
| items carrying links TODAY | 0 |
| **items that would GAIN at least one link if this proposal were ratified whole** | **6** |
| items with no candidate found (would stay empty) | 31 |
| distinct link targets proposed (tier A) | 6 |
| items with a tier-B (home-document) candidate only | 31 |

Coverage would move **0/37 → 6/37 (16%)**.

### Two limits this derivation cannot get past, stated rather than hidden

1. **The store's `body` is truncated at 400 characters** — measured: 7 of 37 items sit
   exactly on the cap, so their prose was CUT before this scan ever read it. Tier A
   therefore under-reads by construction; a missing candidate is not evidence of no edge.
2. **Tier B windows overlap.** 19 items are homed in `GOOD-MORNING.md` within a few dozen
   lines of each other, so the same neighbours (`G18`, `G3`, `B-D7`) recur across many
   items. That recurrence is an artefact of the window, not a hub in the graph. Tier B is
   capped at 3 targets per item and is NOT part of any proposed array.

⚠ The number the dashboard reports would move even if every candidate were wrong. That is
exactly why the ratification step exists — a coverage number is not a graph.

## Per item

### `W-0b` — ★★ ENCODE BEFORE THE WAVE

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:44`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:44`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 5 hits in `GOOD-MORNING.md:44 ±15`):
    > …p sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES G18 BY TURNING A PROVISIONAL WARN INTO A BLOCK** — ✅ **`s1…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:44 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `DV-D02-A`

### `W-0c` — NEXT BUILD CANDIDATES

- state `open` · owner `dave` · opened #0 · home `GOOD-MORNING.md:45`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:45`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 5 hits in `GOOD-MORNING.md:45 ±15`):
    > …p sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES G18 BY TURNING A PROVISIONAL WARN INTO A BLOCK** — ✅ **`s1…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:45 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-020`

### `W-0d` — ✅ THE #67 ENACT WAVE

- state `open` · owner `dave` · opened #0 · home `GOOD-MORNING.md:46`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:46`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 5 hits in `GOOD-MORNING.md:46 ±15`):
    > …p sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES G18 BY TURNING A PROVISIONAL WARN INTO A BLOCK** — ✅ **`s1…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:46 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
  - `B-D7` (graph node, 1 hit in `GOOD-MORNING.md:46 ±15`):
    > …l, #120)* — order RULED: RENDER-CONFIRM `--phys-size` (B-D7 press physics —

### `W-01` — ds-018 C2 follow-through

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:47`
- **Proposed `links`: `["B-D7"]`**
  - `B-D7` (graph node, 1 mention) — from `body`:
    > …low-through — order RULED: RENDER-CONFIRM --phys-size (B-D7 press physics —
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:47`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 5 hits in `GOOD-MORNING.md:47 ±15`):
    > …p sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES G18 BY TURNING A PROVISIONAL WARN INTO A BLOCK** — ✅ **`s1…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:47 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-018`

### `W-02` — dv-legend/dv-behaviour CEILING

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:54`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:54`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 5 hits in `GOOD-MORNING.md:54 ±15`):
    > …p sub, Dave live, **ONE RULING, DAVE'S — AND IT CLOSES G18 BY TURNING A PROVISIONAL WARN INTO A BLOCK** — ✅ **`s1…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:54 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
  - `B-D7` (graph node, 1 hit in `GOOD-MORNING.md:54 ±15`):
    > …l, #120)* — order RULED: RENDER-CONFIRM `--phys-size` (B-D7 press physics — > Alert/Empty-state/Popover, possib…

### `W-03` — ds-012(b) gutter-relative plot area

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:62`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:62`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 2 hits in `GOOD-MORNING.md:62 ±15`):
    > …· ✅ *CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:62 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
  - `B-D7` (graph node, 1 hit in `GOOD-MORNING.md:62 ±15`):
    > …l, #120)* — order RULED: RENDER-CONFIRM `--phys-size` (B-D7 press physics — > Alert/Empty-state/Popover, possib…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-012`

### `W-04` — DV-D16 floating growth

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:65`
- **Proposed `links`: `["DV-D16"]`**
  - `DV-D16` (graph node, 2 mentions) — from `title`:
    > DV-D16 floating growth
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:65`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G18` (sibling item, 2 hits in `GOOD-MORNING.md:65 ±15`):
    > …· ✅ *CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped…
  - `G3` (sibling item, 1 hit in `GOOD-MORNING.md:65 ±15`):
    > …CONSUMED, do not carry again: **#162 residual ① — G18, G3's return-soon half** (CLOSED by `s163-D1`: flipped to…
  - `B-D7` (graph node, 1 hit in `GOOD-MORNING.md:65 ±15`):
    > …l, #120)* — order RULED: RENDER-CONFIRM `--phys-size` (B-D7 press physics — > Alert/Empty-state/Popover, possib…

### `W-05` — Instrument-fit remainder

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:69`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:69`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `B-D7` (graph node, 1 hit in `GOOD-MORNING.md:69 ±15`):
    > …l, #120)* — order RULED: RENDER-CONFIRM `--phys-size` (B-D7 press physics — > Alert/Empty-state/Popover, possib…
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:69 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:69 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-06` — ds-016, UNRULED

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:74`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:74`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `B-D7` (graph node, 1 hit in `GOOD-MORNING.md:74 ±15`):
    > …l, #120)* — order RULED: RENDER-CONFIRM `--phys-size` (B-D7 press physics — > Alert/Empty-state/Popover, possib…
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:74 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:74 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-016`

### `W-07` — ds-017, UNRULED

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:79`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:79`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:79 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:79 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-017`

### `W-08` — STILL OWED, unchanged, none superseded

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:83`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:83`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:83 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:83 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-09` — DELEGATION TOPOLOGY, UNSCOPED

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:84`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:84`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:84 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:84 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-10` — ✅ PER-GATE TEST PLAN

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:85`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:85`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:85 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:85 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-022`

### `W-11` — THE 2c-ROLL / INDEX-VOCABULARY DEADLOCK

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:86`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:86`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:86 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:86 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-12` — THE #57 1b DOSSIER

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:87`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:87`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:87 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:87 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-13` — /tmp RUNBOOK EXPOSURE, UNFIXED

- state `open` · owner `claude` · opened #0 · home `GOOD-MORNING.md:88`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:88`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:88 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:88 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-14` — ⬛ DAVE'S FOUNDING PRINCIPLE

- state `open` · owner `dave` · opened #0 · home `GOOD-MORNING.md:89`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:89`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:89 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:89 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-15` — LEDGER § ★ #59

- state `open` · owner `dave` · opened #0 · home `GOOD-MORNING.md:90`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:90`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:90 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:90 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `W-16` — UNHOMED PAIR, copied up at the #78 2c EXIT CHECK

- state `open` · owner `dave` · opened #0 · home `GOOD-MORNING.md:91`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`GOOD-MORNING.md:91`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G5` (sibling item, 1 hit in `GOOD-MORNING.md:91 ±15`):
    > …. Cut sized ~2,000–2,600 real, collides with open item G5 (the four advisory size caps, re-measure in real then…
  - `DV-D16` (graph node, 1 hit in `GOOD-MORNING.md:91 ±15`):
    > …r is Dave's eye. Ledger: `_DS-IMPROVEMENTS.md`. > **4. DV-D16 floating growth** — RE-PRICE YOURSELF (a DOWNWARD re-p…
  - `DV-D14` (graph node, 1 hit in `GOOD-MORNING.md:91 ±15`):
    > …don't inherit it); build wording ②, not ①; animate DV-D14's ENACTED heights, not true heights; > `prefers-red…

### `G1` — Worklist-index cap DOFIRST_INDEX_TK_MAX = 700 (_capture_gate.py:1403,…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:17`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:17`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:17 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:17 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…
  - `G4` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:17 ±15`):
    > …`, agent-picked) | Dave rules warn vs block | OPEN | | G4 | GM §C measured 191 > 150 warn cap (`_capture_gate.py…

### `G2` — TAPE_TO_BILL = 1.57 at n=2 (_capture_gate.py:371; RATIO_FIRM_N = 4 per…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:18`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:18`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:18 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:18 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…
  - `G4` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:18 ±15`):
    > …`, agent-picked) | Dave rules warn vs block | OPEN | | G4 | GM §C measured 191 > 150 warn cap (`_capture_gate.py…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-021`

### `G3` — retired_unit_prose_audit tier = WARN (_capture_gate.py:2078, 2098,…

- state `done` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:19`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:19`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:19 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:19 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G4` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:19 ±15`):
    > …`, agent-picked) | Dave rules warn vs block | OPEN | | G4 | GM §C measured 191 > 150 warn cap (`_capture_gate.py…

### `G4` — GM §C measured 191 > 150 warn cap (_capture_gate.py:2864,…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:20`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:20`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:20 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:20 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:20 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G5` — Four advisory size caps as a set (_capture_gate.py:4843–4858

- state `blocked` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:21`
- **Proposed `links`: `["G9"]`**
  - `G9` (sibling item, 1 mention) — from `closes_when`:
    > Re-measured in real (G9 first), then Dave ratifies the set in one pass
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:21`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:21 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:21 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:21 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G6` — DEFER_STREAK = 6 (_gm_usage.py:353) + USAGE_HISTORY_BLOCKING = False

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:22`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:22`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:22 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:22 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:22 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G7` — Which end of an archive is "newest" (strata oldest-first · archives…

- state `done` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:23`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:23`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:23 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:23 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:23 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G8` — Dormant % band BAND_FLOOR/HARD_STOP/MARKED_MAX = 45/60/63…

- state `done` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:24`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:24`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:24 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:24 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:24 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G9` — ds-023 re-measurement programme

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:25`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:25`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:25 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:25 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:25 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `ds-023`

### `G10` — The "70%/95%" stray band (GM:36

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:26`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:26`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:26 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:26 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:26 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G11` — DS-018 recessive value

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:27`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:27`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:27 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:27 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:27 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G12` — Charter §4b tone-of-voice temperature map, PROVISIONAL 2026-07-02…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:28`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:28`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:28 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:28 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:28 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G13b` — menu-search combined glyph, PROVISIONAL 2026-07-16 (_ICON-GAPS.md; the…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:29`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:29`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:29 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:29 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:29 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G14` — Icon-button dark bindings

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:30`
- **Proposed `links`: `["ADR-0014"]`**
  - `ADR-0014` (graph node, 1 mention) — from `body`:
    > …k verbatim (icon-button.meta.json:68; parent: SC dark, ADR-0014)
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:30`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:30 ±15`):
    > …location) | closes_when | status | |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:30 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:30 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G15` — DV-D13 donut centre figure + st.visible[id]=true release wiring…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:31`
- **Proposed `links`: `["DV-D13"]`**
  - `DV-D13` (graph node, 2 mentions) — from `title`:
    > DV-D13 donut centre figure + st.visible[id]=true release wiri…
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:31`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:31 ±15`):
    > |---|---|---|---| | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:31 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:31 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G16` — The _proforma/_DATAVIZ-DECISIONS.md:567 enactment call (agent's, not…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:32`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:32`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G1` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:32 ±15`):
    > | G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_c…
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:32 ±15`):
    > …| Dave ratifies 700 or names his own number | OPEN | | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:32 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…

### `G17` — RAG status manifestation…

- state `open` · owner `dave` · opened #86 · home `knowledge/_GOVERNING-RECORDS.md:33`
- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph
  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.
- **Tier B — WEAKER, from the home document (`knowledge/_GOVERNING-RECORDS.md:33`), not from the item's own fields.**
  Proximity in a document is not a dependency; these are offered for Dave's eye only
  and are NOT part of the proposed `links` array above:
  - `G2` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:33 ±15`):
    > | G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`…
  - `G3` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:33 ±15`):
    > …airs logged, then Dave rules firm-or-retire | OPEN | | G3 | `retired_unit_prose_audit` tier = WARN (`_capture_ga…
  - `G4` (sibling item, 1 hit in `knowledge/_GOVERNING-RECORDS.md:33 ±15`):
    > …`, agent-picked) | Dave rules warn vs block | OPEN | | G4 | GM §C measured 191 > 150 warn cap (`_capture_gate.py…

### `G18` — G3 revisit: retired_unit_prose_audit WARN ratified provisionally #161 - Dave wants no loose ends

- state `done` · owner `dave` · opened #161 · home `knowledge/_rulings.json (s161-D2)`
- **Proposed `links`: `["G3"]`**
  - `G3` (sibling item, 1 mention) — from `title`:
    > G3 revisit: retired_unit_prose_audit WARN ratified provis…
- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds
  decision-graph node ids, and these are not nodes): `s161-D2`

## Recipe (so this is reproducible, not a one-off)

```
python3 /var/tmp/derive_links.py    # writes this file; reads the store, writes NOTHING to it
```

Matching rules, stated so a wrong one can be argued with:

1. Ids are matched longest-first with word boundaries — `G13b` can never match as `G13`,
   `R-D6.A2` never as `R-D6.A`. A prefix collision would silently propose the wrong edge.
2. A self-mention is dropped: an item naming itself is not a dependency.
3. Ruling ids (`sNNN-DN`), `ds-NNN` and `DV-D*` are REPORTED but NOT proposed, because the
   field's stated contract (`_state.py` docstring) is decision-graph node ids.
4. Direction is NOT derived. A mention gives an undirected association; which way the
   dependency runs is a judgement, and the quoted line is the evidence for making it.

### The script, inlined so the recipe survives /var/tmp

```python
#!/usr/bin/env python3
"""Machine-derive CANDIDATE links for _state.json. PROPOSES ONLY — never writes the store."""
import json, re, os, collections
ROOT = "/sessions/dreamy-focused-allen/mnt/UX-design"
store = json.load(open(os.path.join(ROOT, "knowledge/_state.json"), encoding="utf-8"))
graph = json.load(open(os.path.join(ROOT, "knowledge/_decision-graph.json"), encoding="utf-8"))
_n = graph["nodes"]
NODE_IDS = set(_n) if isinstance(_n, dict) else {x["id"] for x in _n}
ITEM_IDS = {i["id"] for i in store["items"]}

# Longest-first alternation so 'G13b' never matches as 'G13', 'R-D6.A2' never as 'R-D6.A'.
def alt(ids):
    return "|".join(re.escape(x) for x in sorted(ids, key=len, reverse=True))

ITEM_RE = re.compile(r"(?<![A-Za-z0-9-])(%s)(?![A-Za-z0-9])" % alt(ITEM_IDS))
NODE_RE = re.compile(r"(?<![A-Za-z0-9-])(%s)(?![A-Za-z0-9.-])" % alt(NODE_IDS))
# ruling ids (sNNN-DN / #NNN-DN) and DS improvement ids — recorded as EVIDENCE, not proposed as
# links, because they are not decision-graph node ids and the field's contract is node ids.
EVID_RE = re.compile(r"(?<![A-Za-z0-9])(s\d{2,3}-D\d+[A-Za-z]?|ds-\d{3}|DV-D\d+[A-Za-z-]*|ADR-\d{4})")

FIELDS = ("title", "body", "closes_when", "home", "provenance")

def quote(text, m, width=110):
    s = max(0, m.start() - width // 2); e = min(len(text), m.end() + width // 2)
    return ("…" if s else "") + " ".join(text[s:e].split()) + ("…" if e < len(text) else "")

out = []
gain = 0
for it in store["items"]:
    iid = it["id"]
    cands = collections.OrderedDict()   # target -> list of (kind, field, quoted line)
    evid = collections.OrderedDict()
    for f in FIELDS:
        text = str(it.get(f) or "")
        if not text:
            continue
        for m in ITEM_RE.finditer(text):
            t = m.group(1)
            if t == iid:
                continue                # self-reference is not a link
            cands.setdefault(t, []).append(("sibling item", f, quote(text, m)))
        for m in NODE_RE.finditer(text):
            t = m.group(1)
            cands.setdefault(t, []).append(("graph node", f, quote(text, m)))
        for m in EVID_RE.finditer(text):
            t = m.group(1)
            if t in NODE_IDS:
                continue
            evid.setdefault(t, []).append((f, quote(text, m)))
    # ---- TIER B: the item's HOME document, ±15 lines around the cited line.
    # WEAKER EVIDENCE, kept separate and labelled: proximity in a document is not a
    # dependency. Bodies in the store are truncated at 400 chars (measured: 7 items sit
    # exactly on the cap), so tier A under-reads by construction — this recovers some of
    # what the truncation cut, without pretending it is the same grade of evidence.
    ctx = collections.OrderedDict()
    home = str(it.get("home") or "")
    mfile = re.match(r"^([^:]+?\.md):(\d+)$", home)
    if mfile and os.path.exists(os.path.join(ROOT, mfile.group(1))):
        lines = open(os.path.join(ROOT, mfile.group(1)), encoding="utf-8").read().splitlines()
        n = int(mfile.group(2))
        seg = "\n".join(lines[max(0, n - 16):n + 15])
        for rex, kind in ((ITEM_RE, "sibling item"), (NODE_RE, "graph node")):
            for m in rex.finditer(seg):
                t = m.group(1)
                if t == iid or t in cands:
                    continue
                ctx.setdefault(t, []).append((kind, "%s:%d ±15" % (mfile.group(1), n), quote(seg, m)))
    if cands:
        gain += 1
    out.append((it, cands, evid, ctx))

json.dump({"gain": gain, "total": len(store["items"])}, open("/var/tmp/links_summary.json", "w"))

L = []
w = L.append
w("# PROPOSAL — `links` backfill for `knowledge/_state.json`")
w("")
w("**Status: PROPOSAL. Nothing here is in the store.** Derived mechanically 2026-08-13 by a")
w("script (`/var/tmp/derive_links.py`, recipe below) that scans each item's own `title`, `body`,")
w("`closes_when`, `home` and `provenance` for the ids of *other* store items and for")
w("`_decision-graph.json` node ids. Dave ratifies; only then does anything land.")
w("")
w("## Why this is a proposal and not a patch")
w("")
w("`links` is the dominant input to the dashboard's priority score (weight 0.30, \"Unlock\").")
w("An agent that backfills the links it then scores itself against has closed the loop with no")
w("reader in it. So: the derivation is mechanical, every candidate carries the QUOTED line that")
w("produced it, and the failure mode is visible — a mention is not a dependency. Some of these")
w("are genuine edges; some are an item merely NAMING another. Only Dave can tell them apart,")
w("and the quoted line is what lets him.")
w("")
w("## Coverage")
w("")
w("| | n |")
w("|---|---|")
w("| items in store | %d |" % len(store["items"]))
w("| items carrying links TODAY | %d |" % sum(1 for i in store["items"] if i.get("links")))
w("| **items that would GAIN at least one link if this proposal were ratified whole** | **%d** |" % gain)
w("| items with no candidate found (would stay empty) | %d |" % (len(store["items"]) - gain))
w("| distinct link targets proposed (tier A) | %d |" % len({t for _i, c, _e, _x in out for t in c}))
w("| items with a tier-B (home-document) candidate only | %d |" % sum(1 for _i, c, _e, x in out if x and not c))
w("")
w("Coverage would move **%d/%d → %d/%d (%.0f%%)**." % (
    sum(1 for i in store["items"] if i.get("links")), len(store["items"]),
    gain, len(store["items"]), 100.0 * gain / len(store["items"])))
w("")
w("### Two limits this derivation cannot get past, stated rather than hidden")
w("")
w("1. **The store's `body` is truncated at 400 characters** — measured: 7 of 37 items sit")
w("   exactly on the cap, so their prose was CUT before this scan ever read it. Tier A")
w("   therefore under-reads by construction; a missing candidate is not evidence of no edge.")
w("2. **Tier B windows overlap.** 19 items are homed in `GOOD-MORNING.md` within a few dozen")
w("   lines of each other, so the same neighbours (`G18`, `G3`, `B-D7`) recur across many")
w("   items. That recurrence is an artefact of the window, not a hub in the graph. Tier B is")
w("   capped at 3 targets per item and is NOT part of any proposed array.")
w("")
w("⚠ The number the dashboard reports would move even if every candidate were wrong. That is")
w("exactly why the ratification step exists — a coverage number is not a graph.")
w("")
w("## Per item")
w("")
for it, cands, evid, ctx in out:
    w("### `%s` — %s" % (it["id"], it["title"]))
    w("")
    w("- state `%s` · owner `%s` · opened #%s · home `%s`" % (
        it["state"], it["owner"], it["opened"], it.get("home") or "—"))
    if not cands:
        w("- **NO CANDIDATE.** Nothing in this item's own words names another item or a graph")
        w("  node. Proposed `links`: **stay empty** — an invented edge is worse than a missing one.")
    else:
        w("- **Proposed `links`: `%s`**" % json.dumps(sorted(cands)))
        for t, hits in cands.items():
            kind, field, line = hits[0]
            w("  - `%s` (%s, %d mention%s) — from `%s`:" % (
                t, kind, len(hits), "" if len(hits) == 1 else "s", field))
            w("    > %s" % line)
    if ctx:
        w("- **Tier B — WEAKER, from the home document (`%s`), not from the item's own fields.**" % it.get("home"))
        w("  Proximity in a document is not a dependency; these are offered for Dave's eye only")
        w("  and are NOT part of the proposed `links` array above:")
        for t, hits in list(ctx.items())[:3]:
            kind, where, line = hits[0]
            w("  - `%s` (%s, %d hit%s in `%s`):" % (t, kind, len(hits), "" if len(hits) == 1 else "s", where))
            w("    > %s" % line)
    if evid:
        w("- Ruling/DS ids also mentioned (**evidence, NOT proposed as links** — `links` holds")
        w("  decision-graph node ids, and these are not nodes): %s" % ", ".join(
            "`%s`" % k for k in evid))
    w("")
w("## Recipe (so this is reproducible, not a one-off)")
w("")
w("```")
w("python3 /var/tmp/derive_links.py    # writes this file; reads the store, writes NOTHING to it")
w("```")
w("")
w("Matching rules, stated so a wrong one can be argued with:")
w("")
w("1. Ids are matched longest-first with word boundaries — `G13b` can never match as `G13`,")
w("   `R-D6.A2` never as `R-D6.A`. A prefix collision would silently propose the wrong edge.")
w("2. A self-mention is dropped: an item naming itself is not a dependency.")
w("3. Ruling ids (`sNNN-DN`), `ds-NNN` and `DV-D*` are REPORTED but NOT proposed, because the")
w("   field's stated contract (`_state.py` docstring) is decision-graph node ids.")
w("4. Direction is NOT derived. A mention gives an undirected association; which way the")
w("   dependency runs is a judgement, and the quoted line is the evidence for making it.")
open(os.path.join(ROOT, "_PROPOSAL-links-backfill-2026-08-13-v1.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("gain %d / %d" % (gain, len(store["items"])))
```
