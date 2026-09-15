# HANDOFF #124 — #273 → #274 — THE ADDRESS AND THE REGISTRY

> ⚠ **This file is NEWER than `_CHAIN.md` and OUTRANKS it** (and `_HANDOFF-123`). Written by the #273 conductor (Fable) at FILL ≈191,000 real — past the 180,000 working line, INSIDE the ~220,000 tolerated band (`s272-D93`, arm enacted this session) — BEFORE the delegated wrap. Every claim is a receipt.

## ⛔ READ FIRST, IN THIS ORDER
1. This file. 2. `_CHAIN.md`. 3. `python3 knowledge/_parked.py --check`. ★ Stale-mount check: `git log --oneline -3` vs `ls -la --time-style=full-iso _CHAIN.md`. ★ `pip install tiktoken --break-system-packages` before `_checkin.py` (refused to guess without it).

## ⛔⛔ DAVE'S — VERBATIM. Source: `notes/_lanes/273/DAVE-RULINGS-2026-09-15.md` (every sentence, in order)
- *"1. advisory arm"* → **`s272-D93` ENACTED** `4294b60`: `gauge.TOLERATED_TK = 220_000`; `STOP_LINE_TK` 180,000 UNCHANGED; `_checkin.py` says TOLERATED between them, PAST TOLERANCE above. Driven at 170/195/220/230K.
- *"i cant get access to the common library specs right now, we'll have to park it."* → **P-273-1** (`_parked.json`, fires on `knowledge/guidelines` commit).
- *"lets turn to the 'What the knowledge graph is missing' work, the roles drift. The sidequests can wait. If the list vs card blocks anything lets do that too"* · mid-turn: *"Id really like to get this nailed then go back to the presentation: _PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html"*
- Roles-drift export (`notes/_lanes/273/roles-drift/roles-drift-decisions-2026-09-15.json`): RD-1 **a** · RD-2 **a** · RD-4 **a** → **`s273-D1..D3`**; RD-3 null, note: *"I need to understand the implications of this, maybe closing the list was a bad idea, I have a feeling this will reoccur, lets explore"*
- RD-3 after the three-shape exploration: *"1. is thsi a candidate for an N-gram? probably over engineering"* → **`s273-D4`** REGISTRY not whitelist; no new instrument.

## ⛔ NOT RULED — DO NOT RULE
LC-1..LC-4 on `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html` (the line · the shapes · account-card · …) — P-272-1's owner is Dave · the `example` key on the 13 new when-fields entries (26 legacy entries lack it — declared, his) · the 4 near-dupe pairs (`records`/`rows` · `entry`/`content` · `exits`/`destinations` · `steps`/`parts`) · the `data-grid` 6 `with`-slug reds (#261) · the `input` sub-roles (27 providers, `$extension`) · P-272-2..4 · everything in handoff-123's list not named here.

## WHAT #273 DID — RECEIPTS (6 commits, LOCAL; `git rev-list --count @{u}..HEAD` = 10 incl. #272's 5; push = his word)
1. `4294b60` s272-D93 advisory arm. 2. `7cf3caa` `knowledge/_roles_drift.py` (selftest 12/12) + `notes/_REVIEW-roles-drift-2026-09-15-v1.html` (lane RD, Opus, 137K+100K sub) + P-273-1. **Declared red found here:** `_validate_roles_resolve.py` FAIL(6)→FAIL(20) at `b46ea90` — #272's 15 inscribed `when`s used 13 field names outside `when-fields.json`; `_validate_kg.py OK` had been claimed, the resolver was not run.
3. `0d98a34` **s273-D1 ENACTED** — `_enact_s273_d1_address.py` wrote `provides` onto 84 metas by textual span (reconstruction-proven per file); drift 108/108, 0 silent, 0 roles at zero; `gen_kg_roles_desk.py --land --ratified s270-D2` → providesRole 24→108, 207 edges, 85 metas; explorer regen. ⚠ Chart-boxplot's yieldsTo `$note` regenerated and dropped a hand-added span.cols sentence (generator-owned field — if that sentence mattered it belongs on the meta).
4. `783a8d9` **s273-D3 ENACTED** — lane LC (Opus, 196K sub): `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html`. 13 systems, 0 draw the line on field count; predicates found: surface · record-level actions · same-shape set; GOV.UK summary card = the one list-card precedent; LC-1 (a) needs ONE new field `actions`. Lane corrected my brief: `cards` provides `arrangement`; only `account-card` is `$not-a-provider`.
5. `5f0c97f` **s273-D4 ENACTED** — lane WR (Opus, 86K sub): 13 names defined in `when-fields.json` by textual span, `$description` amended by addition; resolver FAIL(20)→FAIL(6). `_near_dupes.py` cannot read a JSON without code — NOT built.
6. `_KG-EXPLORER.html` regenerated in 3.

## #274 — FIRST MOVES
0. Opener: has he pushed (10 local)? Then the four LC decisions are on the page — one-word each.
1. **THE PRESENTATION** (his mid-turn ask): `notes/_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html` — re-read it against what has landed since it was written: roles (12) are IN the graph (s270-D2 + s273-D1, 108 edges), the DESK address edges are in, the 13 families' zero-counts are stale for at least roles. Regenerate its numbers from the graph, do not hand-correct.
2. **s273-D2 authoring pass two** — 49 silent providers, 8 roles (headline-metric & chart-panel have none), one Opus lane per role, verifier same wave, `when` in the registry grammar (a lane may ADD a name with definition + example, listed in its report — s273-D4). `record-list` waits on LC-1; `input` waits on sub-roles. ≈19K conductor FILL per lane — budget 3–4 lanes per session.
3. `_roles_drift.py` is the drift gate now: run it before any claim about roles.
**Cautions:** `model: opus` every lane · verifier same wave · `_checkin.py` every ~10 turns · screenshot + text diff before presenting · textual span only · never `git stash` · never `gen_kg_edges.py` · `git --work-tree=… checkout` UPDATES THE INDEX (I did it once, reset with `git reset -q -- <paths>`; use `git archive | tar` for a historical copy) · `_numbers_check.py` in lane RD has a void-tag slicer defect (declared).

## STRUCTURAL REDS AT THE SEAM (wrap heals or declares)
Memento index stale (#272's 19 notes + today's) → 2g · boot 81,419 = NINTH breach, his · `/sessions` disk 96% (825 MB dead-session scratch, unremovable from inside) · `_REHEARSAL-LOG.jsonl` / `_GRADE-DECISIONS.jsonl` dirty (instrument-written) · MEMORY.md over cap (stub rule) · resolver FAIL(6) = #261 data-grid, not new.
**Gauge:** boot 81,419 real · FILL 191,386 real at the last check-in (≈100 turns) · subs: RD 137K + 101K · LC 196K · WR 86K = 520K delegated (n=4).
