# #243 lane Q — the six controls become permanent named arms (s243-D1)

Session #243 · 2026-09-03 · enacts `s243-D1` · sources: `notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt/_drive_six_controls.py` + `six-controls-s240-D3.txt` (read whole, shapes ported verbatim, nothing reinvented) · raw logs: `notes/_subreports/assets/2026-09-03-243-lane-Q-six-controls/`

## HEADLINE

`knowledge/_validate_polarities.py --selftest` went from **137 arms / 0 failures** to **148 arms / 0 failures**: eleven new arms labelled `(#243 s243-D1)`, six GREEN (the s240-D3 legal form of controls 100, 225, 235, 248, 321, 326) and five RED (the literal shape of 100, 235, 248, 321, 326, each refused by the name lane P recorded). 225's literal shape was already the named red arm `V225` (S-ID + S-SOURCE) and its two-receipts shape the existing `s240-D3 BREAK ARM: BOTH receipts` (S-SOURCE) — neither is duplicated; the new 225 green arm names both as its pair. `--check` GREEN before and after. Every green arm was mutation-tested RED BY NAME (three mutations); the two writer/stub red arms (235, 321) were driven GREEN by removing their refusal clause (two mutations); the three S-SOURCE red arms (100/248/326) could NOT be driven green even with three clauses removed — they fall through to S-SHAPE and then R3-JUDGEMENT-FIELD, and the arms still FAIL because the name moved (detail under MUTATION ARMS). `polarities.json`, `principles.json`, `stubs.json` and all three files under `_generated/` are BYTE-UNTOUCHED (sha256 identical before/after). Selftest wall time 5.9 s (no timeout issue).

## WHAT WAS DONE

File changed: `knowledge/_validate_polarities.py` only (+144 / −1): a header paragraph `#243 LANE Q`, a `writer_arm()` helper (same contract as `arm()`, but the driver is `add_entry(..., write=True)` — the entry point V's 321/326 attacked), the eleven arms after the `s240-D3 ADD-POLARITY` block, and one summary count `new #243 (s243-D1 six controls) arms N`. Two of my labels first contained `(#239`, which inflated the older `new #239 arms` count 72→74; reworded, it is 72 again.

Per control — arm number in the selftest table, label (abridged), expected, actual, rc:

| # | control | expected | actual | rc | refusal name |
|---|---------|----------|--------|----|--------------|
| 116 | **100 LITERAL** — V's 31st row (pr-fitts/pr-hick) cites fictional `notes/nowhere.json`, `--write` | red | PASS (red by name, nothing written) | 1 | S-SOURCE |
| 117 | **100 LEGAL** — the SAME row, `$seed` = s240-D3 in place of `sources`, `--write` | green | PASS | 0 | — |
| 118 | **225 LEGAL** — new node (pl-33) names ONE receipt (`$seed`), `--write`; paired with `V225` (arm 52, literal `/etc/hostname`: S-ID + S-SOURCE) and `BOTH receipts` (arm 106: S-SOURCE) | green | PASS | 0 | — |
| 119 | **235 LITERAL** — orphan stub, INVENTED phrase `'an orphan phrase'` | red | PASS | 1 | R3-JUDGEMENT-FIELD |
| 120 | **235 LEGAL** (lane F's #239 form (a)) — orphan stub, phrase VERBATIM from the first R1 row (`'tn-01 pr-jakobs-law (work like'`, read from the register at run time) | green | PASS | 0 | — |
| 121 | **248 LITERAL** — all-stub node cites source path `'x'`, `--write` | red | PASS (nothing written) | 1 | S-SOURCE |
| 122 | **248 LEGAL** — the SAME all-stub node with `$seed`, `--write` | green | PASS | 0 | — |
| 123 | **321 LITERAL** — all 30 rows DELETED, then the writer appends a `$seed` node | red | PASS (file untouched) | 1 | S-SOURCE |
| 124 | **321 LEGAL** — all 30 rows RETIRED (`retiredBy` = s240-D3) + `--write` green, then the writer appends the `$seed` node: 31 rows kept, no retired id in any ROW or BYTE under `_generated/` | green | PASS | 0 | — |
| 125 | **326 LITERAL** — file re-indented to 2 spaces, writer's entry cites `'selftest'` | red | PASS (file untouched) | 1 | S-SOURCE |
| 126 | **326 LEGAL** — the SAME 2-space file, the SAME entry with `$seed`: writer green, 31 rows, gate green after | green | PASS | 0 | — |

Notes on fidelity to lane P:
- Lane P's 100-legal used row-0 parties (its `seed_node()`), which is byte-for-byte the existing generic `s240-D3 GREEN CONTROL`. I ported the pair so it differs in EXACTLY the receipt: V's own `NEW31` (pr-fitts/pr-hick) with `sources` swapped for `$seed`. Same for 248 (`ALLSTUB` → `ALLSTUB_SEED`) and 326 (`GOOD` → `GOOD_SEED`), as lane P did.
- 321 LEGAL carries lane P's drop-out proof (row-level `generated_node_ids`) and adds the byte-level scan (`id_in_raw_text`) lane P2 introduced; both empty.
- 120 (links-empty-array) was never red and needs no pair; not added.
- Selftest table lines 116–126 verbatim: `notes/_subreports/assets/2026-09-03-243-lane-Q-six-controls/selftest-after.txt`.

## MUTATION ARMS

Each mutation was applied to `knowledge/_validate_polarities.py`, the selftest run, and the file restored from a saved copy; sha256 of the restored file matched the saved copy after every run (`a8b11b1dcb0b65f1…`). Full output: `mutation-green-arms.txt`, `mutation-red-arms.txt` in the assets dir.

### Green arms → RED BY NAME

**G1 — the driver drops `$seed` handling** (`check_receipt`: `has_seed = False`). Every `$seed` green arm, old and new, goes red S-SOURCE "carries NO receipt":

```
=== MUTATION G1 — driver DROPS $seed handling (check_receipt: has_seed forced False)
104  FAIL    green      1  -      s240-D3 GREEN CONTROL: a NEW polarity born after R1 carries `$seed` = a real ruling id and NO `sources` — the legal form #239-F RULING-SHAPED 4 was missing (#242 lane P)
           ⛔ REFUSED (S-SOURCE) — pl-31: carries NO receipt — every polarity traces to something Dave ruled (s240-D3): name the frozen R1 row in `sources` or, for a node born after R1, the knowledge/_rulings.json id that created it in `$seed`
106  FAIL    red        0  -      s240-D3 BREAK ARM: BOTH receipts on one node — its R1 `sources` AND a `$seed` (the receipt is ONE POINTER PER NODE) (#242)
115  FAIL    green      0  yes    s240-D3 ADD-POLARITY (#242): a BRAND-NEW polarity with a `$seed` receipt is accepted by the writer (dry-run then --write), 31 rows, gate green after — #239-F green control (e), which had no legal form
117  FAIL    green      1  -      100 LEGAL (#243 s243-D1): the SAME 31st row with `$seed` = s240-D3 in place of `sources` — --write green
           ⛔ REFUSED (S-SOURCE) — pl-31: carries NO receipt — …
118  FAIL    green      1  -      225 LEGAL (#243 s243-D1): a new node names ONE legal receipt (`$seed` = s240-D3) — --write green; PAIRED with V225 … and the s240-D3 BOTH-receipts break arm …
           ⛔ REFUSED (S-SOURCE) — pl-33: carries NO receipt — …
122  FAIL    green      1  -      248 LEGAL (#243 s243-D1): the SAME all-stub node with `$seed` = s240-D3 — --write green
           ⛔ REFUSED (S-SOURCE) — pl-40: carries NO receipt — …
124  FAIL    green      1  -      321 LEGAL (#243 s243-D1): all 30 rows RETIRED (`retiredBy` = s240-D3) and --write green, then the writer appends the `$seed` node — 31 rows KEPT in polarities.json, no retired id in any row or byte under _generated/
           ⛔ REFUSED (S-SOURCE) — pl-90: carries NO receipt — …
126  FAIL    green      1  -      326 LEGAL (#243 s243-D1): the SAME 2-space file, the SAME entry with `$seed` = s240-D3 — writer green, 31 rows, gate green after
           ⛔ REFUSED (S-SOURCE) — pl-90: carries NO receipt — …
arms 148 · red arms 126 (went red by name 125/126) · green arms 20 · no-fire/77 arms 2 · new #239 arms 72 · new #242 (s240-D3 receipt) arms 12 · new #243 (s243-D1 six controls) arms 11 · failures 8
```

**G2 — 100 LEGAL's `$seed` pointed at a fictional ruling id** (`NEW31_SEED["$seed"] = "s999-D9"`). Exactly one arm fails, by name:

```
=== MUTATION G2 — 100 LEGAL $seed pointed at a FICTIONAL ruling id s999-D9
117  FAIL    green      1  -      100 LEGAL (#243 s243-D1): the SAME 31st row with `$seed` = s240-D3 in place of `sources` — --write green
           ⛔ REFUSED (R1-DANGLING) — pl-31.$seed 's999-D9' is not a knowledge/_rulings.json id — the receipt names a ruling that does not exist (s240-D3); a receipt that points at nothing is a judgement wearing an id
arms 148 · … · failures 1
```

**G3 — the derivation stops dropping retired nodes** (`live_nodes()` returns every row). 321 LEGAL's prep `--write` regenerates WITH the retired ids and the arm goes red R4-RETIRED-GENERATED, alongside the #242 retirement arms:

```
=== MUTATION G3 — derivation STOPS dropping retired nodes (live_nodes returns every row)
108  FAIL    green      1  -      s240-D3 GREEN CONTROL: a node RETIRED by a real ruling id — it KEEPS its row and the derivation is re-run without it (#242)
109  FAIL    red        1  -      s240-D3 BREAK ARM: a RETIRED node whose id still appears under _generated/ — R4-RETIRED-GENERATED by name, not just STALE (#242)
112  FAIL    red        1  yes    s240-D3 LEAK ARM (#242 lane P2, V2 finding 3): …
114  FAIL    green      1  yes    s240-D3 DROP-OUT PROOF (#242): pl-30 retired → …
124  FAIL    green      1  -      321 LEGAL (#243 s243-D1): all 30 rows RETIRED (`retiredBy` = s240-D3) and --write green, then the writer appends the `$seed` node — 31 rows KEPT in polarities.json, no retired id in any row or byte under _generated/
         :: (R4-RETIRED-GENERATED) — _generated/defaults-declaration.txt still names 'pl-30' as a derived ROW, a node RETIRED by ruling 's240-D3' — a retired node keeps its row in polarities.json and DROPS OUT of everything generated from the KG (s240-D3); run: python3 knowledge/_validate_polarities.py --write
arms 148 · red arms 126 (went red by name 124/126) · … · failures 5
```

### Red arms → GREEN when the literal-shape refusal is removed

**R1 — the stub-phrase VERBATIM clause removed** (`check_stubs`: `if register_text is not None and phrase not in register_text:` → `if False:`). 235 LITERAL goes GREEN (rc 0) and the arm FAILS, as does V234:

```
=== MUTATION R1 — the stub-phrase VERBATIM clause removed (check_stubs)
 35  FAIL    red        0  -      V234 R3 stub phrase that is a 15-word verdict — not verbatim in the register (#239 Q5)
119  FAIL    red        0  -      235 LITERAL (#243 s243-D1): an orphan stub whose phrase is INVENTED ('an orphan phrase') — not verbatim in the R1 register; R3-JUDGEMENT-FIELD
arms 148 · red arms 126 (went red by name 124/126) · … · failures 2
```

**R2 — the "frozen rows claimed by no node" clause removed** (`if unclaimed and not any(...)` → `if False:`). 321 LITERAL goes GREEN (rc 0 — the writer appends into the emptied array and regenerates) and the arm FAILS. V244 (the `--check` form of the same attack) also fails, but stays rc 1 under some other name — the writer path is the one that goes fully green:

```
=== MUTATION R2 — the 'frozen rows claimed by no node' clause removed
 51  FAIL    red        1  -      V244 S-SOURCE all 30 rows deleted — 30 frozen rows claimed by no node (#239 Q3)
123  FAIL    red        0  -      321 LITERAL (#243 s243-D1): all 30 rows DELETED, then the writer appends a `$seed` node — 30 frozen rows claimed by no node; S-SOURCE, file untouched
arms 148 · red arms 126 (went red by name 124/126) · … · failures 2
```

**R3 — 100 / 248 / 326 LITERAL (S-SOURCE) CANNOT be driven green; here is precisely why.** Three successive mutations:

- R3a — the source ALLOW-LIST clause alone removed: all three stay red S-SOURCE via the next clause (`elif s["id"] not in rows_by_id`); only V222 fails. `failures 1`.
- R3b — allow-list AND row-exists clauses removed: the row-text lookup `hays.append(row_texts[s["id"]])` raises `KeyError` on the fictional id, and the Q7 catch-all names it S-SHAPE. All three arms FAIL because the name moved (S-SOURCE → S-SHAPE), not because they went green:

```
116  FAIL    red        1  -      100 LITERAL (#243 s243-D1): …
        rc=1 named=False (names=['S-SHAPE'] wanted=['S-SOURCE']) crashed=False untouched=True :: ⛔ POLARITY GATE REFUSED — 1 refusal(s) … (nothing written):
           ⛔ REFUSED (S-SHAPE) — the gate could not finish reading …/arm116: KeyError: 'tn-31' (at _validate_polarities.py:973 in check_polarities) — an input of a shape this gate does not read; a crash is not a fail, so it is named here
121  FAIL … KeyError: 'y' …      125  FAIL … KeyError: 'x' …
arms 148 · red arms 126 (went red by name 116/126) · … · failures 10
```

- R3c — both clauses removed AND the lookup guarded (`row_texts.get(s["id"], "")`): still rc 1 — the node's `mediating_variable` is now checked verbatim against an EMPTY source row and refused R3-JUDGEMENT-FIELD (Q5):

```
=== MUTATION R3c — allow-list + row-exists clauses removed AND the row-text lookup guarded
116  FAIL    red        1  -      100 LITERAL (#243 s243-D1): …
        rc=1 named=False (names=['R3-JUDGEMENT-FIELD'] wanted=['S-SOURCE']) … ⛔ REFUSED (R3-JUDGEMENT-FIELD) — pl-31.mediating_variable 'target count' is not a verbatim substring of the node's source row — descriptive text the register does not say is a judgement (Q5, #239)
121  FAIL … 125  FAIL … · failures 6
```

So the literal shape of 100/248/326 is refused in depth: Q3 allow-list → Q3 row-exists → Q7 catch-all → Q5 verbatim. Removing the named refusal makes the arm FAIL (which is the property a mutation test wants) but never makes the gate GREEN. The arms are therefore proven to detect the removal of their refusal; the "would turn green" half is UNPROVEN for these three, for the stated structural reason (see UNPROVEN).

## UNTOUCHED SURFACES

sha256 before == after, measured (before: opener of this lane; after: post-edit, post-mutation, post-restore):

```
02d56dc4bca8be53ee5d6e83778bc104c0b2624ee0900bab3e2bbdad5f531c1b  knowledge/brain/polarities.json
c0165ace59d3364dbc8610b02808ee7b610402764c8af2441cc73c3cce53bc96  knowledge/brain/principles.json
a7d3e274d65a009772e8a716757412aba229d36aefc8f3e0b851e0bbadc8e9c7  knowledge/brain/stubs.json
a9c7d831d5ce7f855e5bae907b16cea2277008dfc3194d0cca6bb27df6675762  knowledge/brain/_generated/defaults-declaration.txt
a2cb79a0560ee2680fb309410136ddbc17431d0cd286e59cdcf35b27a7460fcd  knowledge/brain/_generated/polarity-edges.json
cf823c23357835d0c83eb4b7a47050cc2d419eed930dc20961442e32e0232afc  knowledge/brain/_generated/polarity-status.json
```

`git diff --stat`: `knowledge/_validate_polarities.py | 145 +++++++++++++++++++++++++++++++++++++-` (1 file changed, 144 insertions(+), 1 deletion(-)). Also new, untracked: `notes/_subreports/assets/2026-09-03-243-lane-Q-six-controls/` (6 log files) and this report. The other entries in `git status` (`knowledge/_rulings.json`, `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`, `_REVIEW-six-controls-reading-2026-09-03-v1.html`, `knowledge/_probe/session-243.json`) were already modified/untracked when this lane opened and were not touched by it.

## UNPROVEN

- **"Removing the refusal turns 100/248/326 LITERAL green"** — could not be driven. Three clauses removed (allow-list, row-exists, row-text lookup) and the gate still refuses, by a different name each time (S-SHAPE, then R3-JUDGEMENT-FIELD). Driving them green would mean disabling Q5's verbatim check as well, i.e. a fourth clause in a different rule; at that point the mutation no longer tests "the literal-shape refusal", it tests the gate as a whole. The arms DO fail under every one of these mutations, which is what protects them. Named, not estimated.
- A 225 red arm that is BOTH labelled "225" and distinct from `V225` / the `BOTH receipts` arm does not exist, by choice (no duplicates per the brief). If the conductor wants the number on the red side too, the change is a one-word relabel of two existing arms — not done here because those arms belong to #239/#242 and their counts key on their labels.

## RULING-SHAPED

None found. Everything driven sits inside `s243-D1` as ruled (option (a)); the four unruled escapes 241/243/245/301 (`W-374`) were not touched, as the ruling puts them out of scope.

## COUNTS

arms 137 → 148 · failures 0 · new #243 arms 11 · --check GREEN · polarities.json BYTE-UNTOUCHED

## Q2 ADDENDUM — 2026-09-03

Lane Q2 · fixes V3's four findings (`notes/_subreports/2026-09-03-243-V3-six-controls-verifier.md`) in `knowledge/_validate_polarities.py` ONLY · the body above is left as written; this section corrects it · every mutation below ran on a MIRROR copy (`knowledge/` essentials + the two `notes/_subreports/assets/` inputs the gate reads), the repo file's sha checked unchanged after each run · raw logs prefixed `q2-` and the driver `_mutate_q2.py` in `notes/_subreports/assets/2026-09-03-243-lane-Q-six-controls/`.

Baseline at open: `--selftest` 148 arms / 0 failures, `--check` GREEN (`q2-selftest-before.txt`, `q2-check-before.txt`). After: **150 arms / 0 failures**, `--check` GREEN (`q2-selftest-after.txt`, `q2-check-after.txt`). Because two arms were added at 225, every arm number from 118 on is +2 against the body of this report and V3's table: 235 LITERAL/LEGAL are now 121/122, 248 are 123/124, 321 are 125/126, 326 are 127/128.

### F1 (MEDIUM) — FIXED. 100/248/326 LITERAL now pin the Q3 allow-list CLAUSE, not just the family name

The arm frame had no detail assertion (`arm()` took `must_name` / `must_not` only; `writer_arm()` took `must_name`), so one was added — the smallest extension: an optional `must_detail` substring that a red arm must find in the gate's output, on top of the name.

- `arm()` signature line 1816 (+ docstring 1817–1820); the check lines 1842–1845: `detailed = (must_detail is None) or (must_detail in out)` folded into `ok`, and `detailed=… (must_detail=…)` printed in the failure note.
- `writer_arm()` signature line 2420; the check lines 2458–2461, same shape.
- `ALLOW_CLAUSE = "is not on the source allow-list"` at line 2405 (comment 2401–2404) — the detail text of the clause s243-D1 says stands ("a node may not name its own oracle").
- 100 LITERAL line 2474, 248 LITERAL line 2528, 326 LITERAL line 2558: `must_detail=ALLOW_CLAUSE`. (The new 225 LITERAL, line 2493, carries it too.)

No existing arm passes `must_detail`, so none changes behaviour (150/0 at rest, and the #239/#242 counters stay 72/12).

**R3a re-driven** (the allow-list clause alone removed: `if s["path"] not in SOURCE_ALLOW:` → `if False:`), on the Q2 script, verbatim from `q2-mutation-R3a-after.txt`:

```
=== MUTATION R3a the source ALLOW-LIST clause alone removed (Q3: 'a node may not name its own oracle')
 43  FAIL    red        1  -      V222 R3 paraphrase + source pointer broken (path → nowhere): UNVERIFIABLE is refused (#239 Q3)
116  FAIL    red        1  yes    100 LITERAL (#243 s243-D1): V's 31st row (pr-fitts/pr-hick) cites a FICTIONAL R1 path notes/nowhere.json — …
   rc=1 named=True (names=['S-SOURCE'] wanted=['S-SOURCE']) detailed=False (must_detail='is not on the source allow-list') crashed=False untouched=True :: …
   ⛔ REFUSED (S-SOURCE) — pl-31.sources[0].id 'tn-31' is not a row of notes/nowhere.json
118  FAIL    red        1  yes    225 LITERAL (#243 s243-D1): a NEW node pl-33 whose ONLY receipt is the foreign path /etc/hostname …
   rc=1 named=True (names=['S-ID', 'S-SOURCE'] wanted=['S-ID', 'S-SOURCE']) detailed=False (must_detail='is not on the source allow-list') …
123  FAIL    red        1  yes    248 LITERAL (#243 s243-D1): a node whose BOTH parties are declared stubs cites source path 'x' — …
   rc=1 named=True (names=['S-SOURCE'] wanted=['S-SOURCE']) detailed=False (must_detail='is not on the source allow-list') crashed=False untouched=True :: …
   ⛔ REFUSED (S-SOURCE) — pl-40.sources[0].id 'y' is not a row of x
127  FAIL    red        1  yes    326 LITERAL (#243 s243-D1): polarities.json re-indented to 2 spaces, the writer's entry cites 'selftest' as its source — …
   rc=1 named=True (names=['S-SOURCE'] wanted=['S-SOURCE']) detailed=False (must_detail='is not on the source allow-list') crashed=False untouched=True :: …
   ⛔ REFUSED (S-SOURCE) — pl-90.sources[0].id 'x' is not a row of selftest
arms 150 · red arms 128 (went red by name 123/128) · green arms 20 · no-fire/77 arms 2 · new #239 arms 72 · new #242 (s240-D3 receipt) arms 12 · new #243 (s243-D1 six controls) arms 13 · failures 5
✗ selftest FAILED — 5 arm(s)
restored mirror sha 96cdfb4414608662 == gold 96cdfb4414608662 | repo sha 96cdfb4414608662 (repo unchanged: True )
```

All three (116, 123, 127) now FAIL under R3a — the gate still says `S-SOURCE`, but from the row-exists clause, and `detailed=False` names that. Contrast, the SAME mutation on lane Q's script (`q2-mutation-laneQ-contrast.txt`): `failures 1` (V222 only) — 116/121/125 PASS, as V3 found. At rest all three PASS (`q2-selftest-after.txt`).

### F2 (HIGH) — FIXED. 235 LEGAL's phrase comes from the R1 FILE and lies inside ONE field

Lines 2502–2522. `_r1_row0 = json.loads(read_text(os.path.join(REPO, R1_TENSIONS_REL)))["tensions"][0]` — the file, as lane P read it — and `_verbatim4 = " ".join(_r1_row0["the_pull"].split()[:4])` = `'Familiarity says converge on'`, the first four words of row 0's `the_pull`. `load_register()` is no longer called by the arm. The arm's mutate step `_orphan_verbatim_stub()` (2509–2516) first checks, live, that the phrase is a substring of EXACTLY one string field of row 0 (`["the_pull"]`) and of the file's bytes; if not, it raises and the arm fails as "mutation setup crashed". The label now says "read from the R1 FILE".

Mutations, all on the mirror (`q2-mutation-M4-after.txt`, `q2-mutation-M4d-after.txt`, `q2-mutation-laneQ-contrast.txt`):

**M4b (V3's, verbatim — `load_register` PREPENDS `FABRICATED ` to every row text).** Q2 arm 122: PASS green, label `('Familiarity says converge on')` — the phrase did NOT move with the haystack. Lane Q's arm 120 under the same mutation: PASS green, label `('FABRICATED tn-01 pr-jakobs-…')` — the phrase followed the mutation, which is the tautology. This is the discriminating pair. **The brief expected arm 122 to go RED under M4b; it does not, and it should not:** a prefix does not remove an interior register phrase from the haystack, so a non-tautological in-field phrase is, correctly, still verbatim. Only a phrase anchored at the very start of the join (i.e. the cross-field `id`+`side_a` phrase F2 removes) can be dislodged by a prefix. So the red proof is M4d:

**M4d (Q2's — the STUB haystack alone, `all_rows_text` at line ~909, built WITHOUT R1 row 0; nothing else touched):**
```
=== MUTATION M4d the STUB haystack alone (all_rows_text, Q5's check_stubs input) is built WITHOUT R1 row 0 — …
122  FAIL    green      1  -      235 LEGAL (#243 s243-D1), lane F's #239 form (a): an orphan stub — declared, never used — whose phrase is VERBATIM from ONE field of the first R1 row, read from the R1 FILE ('Familiarity says converge on') — green
   ⛔ REFUSED (R3-JUDGEMENT-FIELD) — stubs[15]: phrase 'Familiarity says converge on' is not VERBATIM in the frozen R1 register — a stub is a phrase the register already says (s238-D1); a phrase nothing can check is a judgement (Q5, #239)
arms 150 · red arms 128 (went red by name 128/128) · green arms 20 · … · new #243 (s243-D1 six controls) arms 13 · failures 1
✗ selftest FAILED — 1 arm(s)
```
Exactly one arm fails — 235 LEGAL, red `R3-JUDGEMENT-FIELD` by name, on ITS phrase — and the 15 real stubs stay green. The arm's oracle is the file: when the gate stops saying what the file says, the arm goes red.

**M4c (V3's — fields joined with `' \n '`):** `failures 0`, arm 122 PASS green (`q2-mutation-M4-after.txt`). The phrase survives a per-field tightening of Q5, as required.

**M4b2 (haystack REPLACED with `FABRICATED <id>`) — run, then discarded as CONFOUNDED:** `row_texts` also feeds Q5's `mediating_variable`/`note` verbatim checks, so 31 arms fail including the CONTROL; arm 122's own refusal lines are about pl-30, not the stub. Not evidence either way; kept in the log for honesty only.

### F3 (LOW) — FIXED. 225 now has three arms of its own on ONE node

Lines 2477–2500. Lane Q's 225 LEGAL (`seed_node(id="pl-33")` = arm 104 under another id) is gone. In its place `FOREIGN33` — pl-33, parties pr-steering/pr-klm (a pair no other arm uses), receipt `[{"path": "/etc/hostname", "id": "x"}]`, V225's foreign receipt verbatim — driven three ways, six-controls-s240-D3.txt § [225]'s three drives on one node:

| # | arm | expect | at rest | must_name | must_detail |
|---|---|---|---|---|---|
| 118 | 225 LITERAL — pl-33 whose ONLY receipt is `/etc/hostname`, `--write` | red | PASS, rc 1, nothing written | S-ID + S-SOURCE | `is not on the source allow-list` |
| 119 | 225 TWO RECEIPTS — the same pl-33 with the foreign `sources` AND `$seed` | red | PASS, rc 1, nothing written | S-SOURCE | `carries BOTH` |
| 120 | 225 LEGAL — the same pl-33 reduced to ONE legal receipt (`$seed`) | green | PASS, rc 0 | — | — |

V225 (arm 52: row 0 + a SECOND foreign receipt) and arm 106 (row 0's R1 row + `$seed`) are untouched; the new pair differs from them in the node (a new one, not row 0) and from 100 LITERAL in the receipt (an absolute path outside the repo vs a fictional repo-relative one — same clause, different escape). Driven (`q2-mutation-G1-M5-after.txt`, `q2-mutation-M5-after.txt`):

- **G1** (lane Q's: `has_seed` forced False): 120 goes red `S-SOURCE — pl-33: carries NO receipt` (FAIL, as every `$seed` green arm does), and 119 FAILS with `detailed=False (must_detail='carries BOTH')` — the BOTH clause no longer fires and the family name alone (still `S-SOURCE`, from the allow-list) would have masked it. `failures 9` = lane Q's 8 + arm 119.
- **M5** (the BOTH-receipts clause disabled: `if has_src and has_seed:` → `if False:`): `failures 2` — arm 106 (rc 0, went green) and arm 119 (`detailed=False`, S-SOURCE still named by the allow-list clause). Exactly the two BOTH-receipts arms, nothing else.
- **R3a** (above): 118 FAILS with `detailed=False`; 119 and 120 PASS.

### F4 (LOW) — headline correction

The `## HEADLINE` and `### Red arms → GREEN…` R3 paragraph above frame the R3a result as robustness ("could NOT be driven green … refused in depth"). The precise statement is: **100/248/326 LITERAL did not FAIL under R3a — fixed at Q2 by F1.** With the allow-list clause alone removed, the three arms PASSED on lane Q's script (`failures 1`, V222 only) because they asserted the family name `S-SOURCE`, which the row-exists clause also carries; they now FAIL under R3a (`failures 5`: V222 + 116 + 118 + 123 + 127, all `detailed=False`), and PASS at rest. The UNPROVEN bullet "Removing the refusal turns 100/248/326 LITERAL green — could not be driven" stands as a property of the gate (four clauses sit behind the literal shape); what changed is that the arms now prove WHICH clause fires, not only that the family does.

### UNTOUCHED SURFACES (Q2)

sha256 before Q2's first edit == after its last run, all six equal the values in the body:
```
02d56dc4bca8be53ee5d6e83778bc104c0b2624ee0900bab3e2bbdad5f531c1b  knowledge/brain/polarities.json
c0165ace59d3364dbc8610b02808ee7b610402764c8af2441cc73c3cce53bc96  knowledge/brain/principles.json
a7d3e274d65a009772e8a716757412aba229d36aefc8f3e0b851e0bbadc8e9c7  knowledge/brain/stubs.json
a9c7d831d5ce7f855e5bae907b16cea2277008dfc3194d0cca6bb27df6675762  knowledge/brain/_generated/defaults-declaration.txt
a2cb79a0560ee2680fb309410136ddbc17431d0cd286e59cdcf35b27a7460fcd  knowledge/brain/_generated/polarity-edges.json
cf823c23357835d0c83eb4b7a47050cc2d419eed930dc20961442e32e0232afc  knowledge/brain/_generated/polarity-status.json
```
`knowledge/_validate_polarities.py` sha `a8b11b1d…` (lane Q) → `96cdfb441460866216c1832a082c7a9178ee045ce41cc9dccaa76e733d8345ea` (Q2); every mutation ran on the mirror and the repo sha was re-read unchanged after each. `git diff --stat` for the script vs HEAD: `193 +++…-` (189 insertions, 4 deletions; lane Q's 144/1 included). Files changed by Q2: `knowledge/_validate_polarities.py`, this report (append only), and the `q2-*` logs + `_mutate_q2.py` under `notes/_subreports/assets/2026-09-03-243-lane-Q-six-controls/`. No `_build_all.py`, no commit; `_rulings.json` / `_REHEARSAL-LOG.jsonl` / `_GRADE-DECISIONS.jsonl` in `git status` were already modified before lane Q opened and were not touched.

### UNPROVEN (Q2)

- "Arm 122 goes RED under V3's M4b" — could not be driven and is not a property a correct in-field phrase can have (a prefix leaves interior text in place); M4d is the red proof, and M4b's contribution is the unchanged label against lane Q's `FABRICATED …` one.
- M4b2 is confounded (above) and proves nothing about arm 122.

### RULING-SHAPED (Q2)

None new. V3's one item (whether Q5's haystack should be per-field verbatim) is untouched by F2 — the arm no longer depends on the cross-field join either way — and remains Dave's, as V3 framed it.

### COUNTS (Q2)

arms 148 → 150 · failures 0 · new #243 arms 13 · --check GREEN · brain files BYTE-UNTOUCHED
