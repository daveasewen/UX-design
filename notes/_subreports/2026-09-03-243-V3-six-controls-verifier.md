# #243 V3 — verifier of lane Q's six controls (s243-D1)

Session #243 · 2026-09-03 · verifies `notes/_subreports/2026-09-03-243-lane-Q-six-controls.md` · read-only on the repo; every mutation was driven on a MIRROR copy (`knowledge/` essentials + the two `notes/_subreports/assets/` inputs the gate reads) so the repo file was never touched · raw logs: `notes/_subreports/assets/2026-09-03-243-V3-six-controls-verifier/`

## VERDICT

**SATISFIED WITH FINDINGS** — every number lane Q claimed re-measures exactly (137 → 148 arms, 0 failures, `--check` GREEN, six brain files byte-identical) and each of the five red arms fires exactly one refusal, by the right name, for the right clause; but one green arm (235 LEGAL) is TAUTOLOGICAL — its "verbatim" phrase is taken from the gate's own `load_register()` output rather than from the R1 file, so it stays green when the haystack is fabricated (M4b, 148/148 pass) — and the three S-SOURCE red arms (100/248/326 LITERAL) do not detect removal of the very clause the ruling names (Q3 allow-list; lane Q's own R3a log shows them PASSING under that mutation).

## COUNTS (re-measured, this seat)

| measure | lane Q claimed | V3 measured | source |
|---|---|---|---|
| arms, HEAD script (`git show HEAD:…`) run in the mirror | 137 | **137** · red 121 (121/121 by name) · green 14 · failures 0 | `selftest-HEAD.txt` |
| arms, working script, run IN THE REPO | 148 | **148** · red 126 (126/126 by name) · green 20 · no-fire/77 2 · #239 72 · #242 12 · #243 11 · failures 0 · rc 0 | `selftest.txt` |
| arms, working script, run in the mirror | — | 148 / 0 — table identical to the in-repo run modulo tmp dir names (diff empty) | `selftest-mirror` (diffed, not kept) |
| selftest wall | 5.9 s | 6.6 s | this seat |
| `--check` | GREEN | **GREEN**, rc 0, three `_generated/` files "content byte-identical" | `check.txt` |
| `knowledge/_validate_polarities.py` sha256 | `a8b11b1dcb0b65f1…` | `a8b11b1dcb0b65f1b304ceb920971bc55890808b415c1130b0a831b2525d9a18` before, after every mutation, and at close | — |
| `git diff --stat` for the script | +144 / −1 | `145 +++…-` (144 insertions, 1 deletion); the other three modified files and untracked entries pre-date lane Q | — |

## PER-ARM TABLE

Refusal text per red arm re-driven through the CLI (`--write --brain COPY` / `--add-polarity … --write --brain COPY`), `red-arms-verbatim.txt`. "Shape matches control" is judged against `_drive_six_controls.py` (lane P).

| # | arm | shape matches lane P's control? | tautology risk? | refusal name right? |
|---|---|---|---|---|
| 116 | 100 LITERAL | YES — `NEW31` byte-equal to lane P's, appended, `gate(write=True)` | n/a (red) | YES — one refusal, `S-SOURCE`, detail "`pl-31.sources[0].path 'notes/nowhere.json' is not on the source allow-list … a node may not name its own oracle (Q3, #239)`". BUT the arm asserts only the family name; under lane Q's own R3a (allow-list clause removed) it PASSES via the row-exists clause — see Finding 1 |
| 117 | 100 LEGAL | DEVIATES, disclosed — lane P used `seed_node()` (row-0 parties = pr-jakobs-law/pr-von-restorff); lane Q used V's pr-fitts/pr-hick so the pair differs in exactly the receipt. Better pairing than lane P's, not "verbatim" | LOW — goes red under G1 (`$seed` handling dropped) and G2 (fictional id); under my M5 (NEITHER-receipt accepted) it stays green, correctly, since it carries a receipt | n/a (green) |
| 118 | 225 LEGAL | YES — `seed_node(id="pl-33")`, as lane P | HIGH in the sense of REDUNDANCY — identical to arm 104 (`s240-D3 GREEN CONTROL`, `seed_node()` = pl-31) except the id string. Under every mutation run (G1, M1–M5) 118 and 104 move together; 118 adds no discriminating power. Inherited from lane P — see Finding 3 | n/a |
| 119 | 235 LITERAL | YES — `{"id":"st-orphan-phrase","phrase":"an orphan phrase"}`, `--check` | n/a | YES — one refusal, `R3-JUDGEMENT-FIELD`, "`stubs[15]: phrase 'an orphan phrase' is not VERBATIM in the frozen R1 register`" |
| 120 | 235 LEGAL | NO — lane P read the R1 FILE (`json.loads(open(R1))["tensions"][0]`) as an oracle independent of the gate; lane Q reads `load_register()[1]`, i.e. THE GATE'S OWN HAYSTACK, and takes its first four tokens. The phrase `'tn-01 pr-jakobs-law (work like'` spans two register fields (`id` + `side_a`) and is NOT a substring of the R1 file's bytes nor of any single field (measured: both False) | **TAUTOLOGICAL** — M4b (haystack prefixed with `FABRICATED `): phrase becomes `'FABRICATED tn-01 pr-jakobs-law (work'`, which appears in no file, and the arm stays GREEN (148/148). M4c (fields joined with `' \n '`, whitespace only): the arm goes RED `R3-JUDGEMENT-FIELD` while all 15 real stubs stay green — the arm pins a join artefact, not a register phrase. See Finding 2 | n/a |
| 121 | 248 LITERAL | YES — `ALLSTUB` byte-equal, appended, `write=True` | n/a | YES — one refusal, `S-SOURCE`, "`pl-40.sources[0].path 'x' is not on the source allow-list`". Same family-name caveat as 116 (Finding 1) |
| 122 | 248 LEGAL | YES — `ALLSTUB_SEED`, as lane P | LOW — red under G1 (lane Q) | n/a |
| 123 | 321 LITERAL | YES — rows emptied, `add_entry(GOOD_SEED, write=True)`; entry point is the writer, as V attacked | n/a | YES — one refusal, `S-SOURCE`, "`frozen row(s) ['tn-01', …] (30) are claimed by no node`" + "File untouched". Under M3 (writer ignores the gate) it FAILS on `untouched=False` — the byte check is live |
| 124 | 321 LEGAL | YES — lane P's two steps (retire all + `--write`, then writer) + lane P2's byte scan; `_rc321 == [0]`, 31 rows, `leaks_rows=[] leaks_bytes=[]` | LOW — red under G3 (lane Q). Under my M2 (`retired_map()` empty) it stays GREEN: derivation still drops retired rows via `live_nodes()`, so no leak exists to miss; arms 109/112/114 catch M2 instead. Correct behaviour, not a gap | n/a |
| 125 | 326 LITERAL | YES — 2-space re-indent, `add_entry(GOOD)`; `compose_append` succeeded on the 2-space file (the refusal is the gate's, not the composer's) | n/a | YES — one refusal, `S-SOURCE`, "`pl-90.sources[0].path 'selftest' is not on the source allow-list`". Family-name caveat (Finding 1). Under M3 it FAILS on `untouched=False` |
| 126 | 326 LEGAL | YES — 2-space file, `GOOD_SEED`, 31 rows, gate green after | LOW — red under G1 (lane Q) | n/a |

Label/count hygiene: none of the eleven labels contains `(#239` or `#242`, so the older counters stay 72 and 12 (equal to HEAD) — no double counting.

## MUTATIONS (V3's own; none in lane Q's logs)

Each applied to the mirror copy of the script, `--selftest` run, the file restored from the repo bytes; mirror sha `a8b11b1dcb0b65f1` == repo sha after every run (`mutations.txt`, `mutations-M4bc.txt`). Output verbatim, trimmed to FAIL rows and the summary line.

**M1 — `check_receipt` ACCEPTS a `$seed` absent from the store** (`for key in ("$seed", "retiredBy")` → `("retiredBy",)`):
```
105  FAIL    red        1  -      s240-D3 BREAK ARM: `$seed` names s999-D9, absent from knowledge/_rulings.json (#242)
arms 148 · red arms 126 (went red by name 125/126) · … · new #243 (s243-D1 six controls) arms 11 · failures 1
```
Caught by arm 105 (#242) only. None of the 11 new arms move — expected: their `$seed` is real. The dangling-id property is guarded by #242's arm, not by s243-D1's.

**M2 — `retired_map()` returns EMPTY:**
```
109  FAIL    red        1  -      s240-D3 BREAK ARM: a RETIRED node whose id still appears under _generated/ — R4-RETIRED-GENERATED by name, not just STALE (#242)
112  FAIL    red        1  -      s240-D3 LEAK ARM (#242 lane P2, V2 finding 3): pl-02 retired → --write and its id is gone from every BYTE of all three generated files; …
114  FAIL    green      0  yes    s240-D3 DROP-OUT PROOF (#242): pl-30 retired → --check names R4-RETIRED-GENERATED · --write regenerates · …
arms 148 · … · failures 3
```
Caught by 109/112/114 (#242). 321 LEGAL (124) stays green — `live_nodes()` still drops retired rows, so the generated files carry no leak for the post-check to find. Not a gap.

**M3 — the WRITER skips the gate's verdict** (`add_entry`: `if rc != 0 and not only_stale:` → `if False:`):
```
123  FAIL    red        1  yes    321 LITERAL (#243 s243-D1): all 30 rows DELETED, then the writer appends a `$seed` node — …
125  FAIL    red        1  yes    326 LITERAL (#243 s243-D1): polarities.json re-indented to 2 spaces, the writer's entry cites 'selftest' as its source — …
138  FAIL    red        1  yes    ADD-POLARITY: an entry with a typed status is REFUSED by name, nothing written
139  FAIL    red        1  yes    V324 ADD-POLARITY: an entry whose quote has no reachable source is REFUSED (S-SOURCE + R3-QUOTE-NOT-VERBATIM), nothing written (#239 Q3)
140  FAIL    green      0  yes    ADD-STUB: a verbatim phrase appended textually; …
arms 148 · red arms 126 (went red by name 122/126) · … · failures 5
   rc=1 named=True (names=['S-SOURCE'] wanted=['S-SOURCE']) crashed=False untouched=False :: …
   WROTE /dev/shm/polarity-selftest-…/arm125/polarities.json; regenerating the derived files:
```
Both new writer red arms (123, 125) FAIL — the post-write gate still says S-SOURCE (rc 1, named) but the file WAS written (`untouched=False`). `writer_arm()`'s byte check is the clause that catches it. Good.

**M4 — Q5 haystack joined per field with NUL:** confounded — because 235 LEGAL builds its phrase FROM `load_register()`, the phrase itself acquired the NUL and was refused `S-FORMAT-CHAR` (`failures 1`). This is what led to M4b/M4c.

**M4b — `load_register` PREPENDS `FABRICATED ` to every row's text** (the haystack no longer matches the R1 file):
```
arms 148 · red arms 126 (went red by name 126/126) · green arms 20 · … · new #243 (s243-D1 six controls) arms 11 · failures 0
✓ selftest OK — control green; every refusal arm red by its name; nothing written on refusal
```
NOTHING fails. 235 LEGAL's phrase is now `'FABRICATED tn-01 pr-jakobs-law (work'` — in no file on disk — and the arm is green. The arm's oracle is the code under test.

**M4c — row fields joined with `' \n '` instead of `' '`** (whitespace only; a phrase may not span two fields):
```
120  FAIL    green      1  -      235 LEGAL (#243 s243-D1), lane F's #239 form (a): an orphan stub — … ('tn-01 pr-jakobs-law (work like') — green
   ⛔ REFUSED (R3-JUDGEMENT-FIELD) — stubs[15]: phrase 'tn-01 pr-jakobs-law (work like' is not VERBATIM in the frozen R1 register — …
arms 148 · … · failures 1
```
Only 235 LEGAL fails; the 15 real stubs all pass — the real store does not depend on cross-field phrases, only this arm does.

**M5 — `check_receipt` silently accepts NEITHER receipt** (tautology probe for the `$seed` green arms):
```
107  FAIL    red        1  -      s240-D3 BREAK ARM: NEITHER receipt — a node with no `sources` and no `$seed` (#242)
arms 148 · … · failures 1
```
Caught by 107 (#242). The five `$seed` green arms stay green, correctly.

## UNTOUCHED SURFACES

sha256 at this seat (before my first run and after my last; `git status` lists none of these as modified, so they also equal HEAD) — all six EQUAL lane Q's recorded values:

```
02d56dc4bca8be53ee5d6e83778bc104c0b2624ee0900bab3e2bbdad5f531c1b  knowledge/brain/polarities.json
c0165ace59d3364dbc8610b02808ee7b610402764c8af2441cc73c3cce53bc96  knowledge/brain/principles.json
a7d3e274d65a009772e8a716757412aba229d36aefc8f3e0b851e0bbadc8e9c7  knowledge/brain/stubs.json
a9c7d831d5ce7f855e5bae907b16cea2277008dfc3194d0cca6bb27df6675762  knowledge/brain/_generated/defaults-declaration.txt
a2cb79a0560ee2680fb309410136ddbc17431d0cd286e59cdcf35b27a7460fcd  knowledge/brain/_generated/polarity-edges.json
cf823c23357835d0c83eb4b7a47050cc2d419eed930dc20961442e32e0232afc  knowledge/brain/_generated/polarity-status.json
```
`knowledge/brain/_generated/` holds exactly those three files. `knowledge/_validate_polarities.py` sha `a8b11b1d…9a18` unchanged throughout (mutations ran on the mirror). No `_build_all.py`, no commit, no edit to the gate.

## FINDINGS

1. **MEDIUM — 100/248/326 LITERAL (arms 116, 121, 125; `knowledge/_validate_polarities.py` lines 2460–2462, 2485–2487, 2515–2516) do not protect the clause the ruling names.** Each asserts only the family name `S-SOURCE`, a name shared by seven clauses (register missing/unparseable/no list · BOTH receipts · NO receipt · allow-list · row-exists · row claimed twice · rows unclaimed). Lane Q's own R3a log (`mutation-red-arms.txt` lines 9–11): with the Q3 allow-list clause alone removed — the sentence "a node may not name its own oracle" that s243-D1 says STANDS — arms 116/121/125 all PASS (`failures 1`, V222 only). The report's headline ("could NOT be driven green … refused in depth") presents this coverage gap as robustness. Fix shape: `arm()`/`writer_arm()` take a `must_detail` substring (e.g. `"not on the source allow-list"`) for these three; mechanical, no ruling needed. Verbatim refusal text at `red-arms-verbatim.txt` shows the correct clause does fire today.

2. **HIGH — 235 LEGAL (arm 120; lines 2478–2483) is tautological.** `_verbatim4 = " ".join(next(iter(load_register()[1].values())).split()[:4])` — the arm's phrase is the first four tokens of the gate's OWN haystack, not of the R1 file. Consequences, all measured: (a) the phrase `'tn-01 pr-jakobs-law (work like'` is in neither the R1 file's bytes nor any single field (it straddles `id` and `side_a`; it exists only because `load_register()` space-joins a row's values); (b) M4b — fabricate the haystack and the arm stays green, 148/148; (c) M4c — a whitespace-only per-field join reds this arm and nothing else. Lane P's driver read the R1 FILE directly and so was NOT tautological; the port replaced the independent oracle with the code under test, which contradicts the report's "shapes ported verbatim". Fix shape: read `notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json` in the arm and take four consecutive words from INSIDE one field (e.g. `side_a`: `"work like everything else"`); the arm then proves a register phrase is accepted and survives a per-field tightening of Q5.

3. **LOW — 225 LEGAL (arm 118; lines 2466–2471) is arm 104 with a different id string.** `seed_node(id="pl-33")` vs `seed_node()` (pl-31): same parties, same `mediating_variable`, same receipt, same `write=True`. In every mutation run here and in lane Q's G1, 104 and 118 move together. Inherited from lane P's `225-legal`; the "225" control is therefore present in the selftest by label only — its red side lives in V225/arm 106, its green side duplicates 104. If the pair is to carry weight, the green form should be the literal's own shape with the receipt swapped (row 0 with `sources` replaced by `$seed`, which is the s240-D3 "one pointer" form) — that is the 100-style pairing lane Q applied elsewhere.

4. **LOW — report framing.** `## HEADLINE` says "the three S-SOURCE red arms (100/248/326) could NOT be driven green"; the precise statement is "under R3a they did not FAIL" (see Finding 1). Everything else in the report re-measures exactly.

5. **INFO — the M2 result is a correct non-catch, not a gap.** `retired_map()` returning empty is caught by #242's 109/112/114; 321 LEGAL stays green because `live_nodes()` still drops retired rows and the post-check scans the generated bytes, which are then clean. No action.

## LANE Q'S TWO UNPROVEN ITEMS

- **"Removing the refusal turns 100/248/326 LITERAL green — could not be driven."** Real property of the gate (four clauses stand behind the literal shapes) AND a gap in arm design: because the arms assert the family name, the first-line clause (allow-list) can be deleted without any of the three arms noticing (Finding 1). The right UNPROVEN framing is "these arms prove S-SOURCE fires; they do not prove WHICH clause fires."
- **"No 225 red arm distinct from V225 / BOTH receipts, by choice."** Real and acceptable on the red side (no duplicates). On the green side the choice was not carried through: 225 LEGAL IS a duplicate of arm 104 (Finding 3). Net: control 225 has no arm of its own on either side.

## RULING-SHAPED

One item, Dave's to decide, verbatim: **Q5's verbatim haystack joins each register row's fields with a single space, so a stub phrase that straddles two fields (e.g. `'tn-01 pr-jakobs-law (work like'` = `id` + `side_a`) passes as "verbatim in the frozen R1 register". The 15 real stubs do not rely on this (M4c: per-field join leaves all 15 green); only arm 120 does. Tightening Q5 to per-field verbatim is a change to a refusal's scope — it is not needed to fix Finding 2 (the arm can pick an in-field phrase without it), so nothing here blocks on it.**

Nothing else is ruling-shaped; s243-D1 option (a) is enacted as ruled.
