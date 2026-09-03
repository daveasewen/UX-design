# `#242`-`P` — `W-387`: the polarity receipt (`s240-D3`) built — an R1 row **or** a ruling id, one pointer per node; six controls green, escapes still 4

session: `#242` · 2026-09-03
window: Fable conductor, lane P (build lane; exit gate = the gate's own `--selftest` + lane F's green controls + lane V's `escaped-repro.txt`)
sub index: `P`
brief: `notes/_briefs/2026-09-03-242-lane-P-polarity-receipt-build-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`. SHAPE: ~30 tool calls · 2 repo files edited (1 schema re-cut + pinned, 1 gate) · 11 new selftest arms (125 → 136, 0 failures) · 3 driver scripts filed · 4 evidence transcripts · 0 git commands · 0 writes to `polarities.json`, `principles.json`, `stubs.json`, `_generated/`, the store, the spine or memory · seat `eager-wizardly-lovelace`.

## VERDICT

`s240-D3` is ENACTED and every region of the brief is **DONE** short of V2, which is not mine to run. The receipt is now **one pointer per node**: `sources` (a frozen R1 register row, unchanged) **or** `$seed` (the `knowledge/_rulings.json` id that created a node born after R1); a retired node keeps its row and carries `retiredBy`, and drops out of the derivation. All three refusals the brief named are RED BY NAME and driven **both ways** at the CLI and in `--selftest`: (a) a `$seed`/`retiredBy` naming an id absent from the store → **R1-DANGLING**; (b) a node with two receipts, or with none → **S-SOURCE**; (c) a retired node still named under `_generated/` → **R4-RETIRED-GENERATED** (a new R4 sub-form, declared). The `SCHEMA_SHA256` pin moved in the same change (`42f84503…` → `c2c165ac…`) and its break arm — touch the schema, leave the pin — is red by name. `sources` left the schema's `required`, but **nothing loosened**: the floor moved into code (`check_receipt`), and the "NEITHER receipt" arm proves the deleted key is still a refusal (the #239 `S-SCHEMA` arm was re-cut to `S-SOURCE`). Lane F's **seven green controls all have a GREEN form**: 120 and 235 unchanged; 100 · 225 · 248 · 326 go green the moment the node's receipt is the ruling id instead of an oracle it invented (their Q3 refusal is CORRECT and stays — driven literally, still red, on purpose); 321 goes green once the 30 rows are **RETIRED rather than DELETED**, which is exactly the legal form `#239-F` RULING-SHAPED 4 said was missing. V's `escaped-repro.txt` re-drives **48 rows · CAUGHT 44 · ESCAPED 4** — the same four UNRULED rows (241 · 243 · 245 · 301), not one more. `polarities.json` is **byte-untouched** (sha256 `02d56dc4…`, P's receipt) and so are `principles.json`, `stubs.json` and all three generated files: the derivation did not move, and the live tree is GREEN with no `--write`. One real defect was found and fixed mid-lane (finding 4), and one filed-asset trap was found that will bite V2 if it is not read first (finding 6).

COUNTS: findings `9` · ruling-shaped `8` · UNPROVEN `5`

BRIEF COUNTS: selftest arms `136` (red 119/119 by name · green 15 · 77 2 · **new #242 arms 11** · failures 0) · mutation arms driven both ways `6 pairs` (pin · `$seed` · `retiredBy` · two receipts · no receipt · retired leak) · green controls `7/7 have a green form` (2 unchanged · 4 green under `$seed` · 1 green under `retiredBy`) · escaped-repro `48 re-driven · CAUGHT 44 · ESCAPED 4` (RULED 0 · PROMISED 0 · **UNRULED 4**) · live `--check` `GREEN` · `polarities.json` `BYTE-UNTOUCHED` · data rows edited `0`

**BEFORE → AFTER: `SCHEMA_SHA256 42f84503… → c2c165ac…` · `selftest 125 → 136 arms` · `SCHEMA_FLOORS 47 → 53` · `green controls 1/7 green → 7/7 have a green form` · `ESCAPED 4 → 4`.**

## What was done

**Ground.** `#239`-F's report (all sections, `green-controls-recut.txt`), `#238`-V's harness scripts as filed, `_validate_polarities.py` end to end at the regions the ruling touches (the pin/floors, `check_polarities`, `check_quotes_verbatim`, `derive`, `freshness`, `gate`, the writer, the selftest frame), `polarity.schema.json`, and the four wave scripts' literal shapes for controls 100 · 225 · 235 · 248 · 321 · 326. `s240-D3` was read from the brief (verbatim) and its id verified present in `knowledge/_rulings.json` (333 rulings; `s240-D1/D2/D3` all present).

**1 · `knowledge/brain/schema/polarity.schema.json`** — `required` drops `sources` (the receipt may now be `$seed`); two new properties, each `type: string` + the ASCII id `pattern` + `maxWords: 1`:
- `$seed` — the birth receipt of a node born after R1, described as the ALTERNATIVE to `sources`, never its companion;
- `retiredBy` — the retirement receipt; the node keeps its row and drops out of everything generated.
The root `description` carries the receipt rule in words; `x-refusals` gains `R4-RETIRED-GENERATED`, widens `R1` to cover a receipt id, and widens `S-SOURCE` to cover both/neither. sha256 `c2c165ac126d878d8cb9d8548ac1fba2d765724667bf410dfbcca611372243e4` = the new pin.

**2 · `knowledge/_validate_polarities.py`** (`git diff --numstat`: +233 / −12; the schema is +18 / −6):
- `SCHEMA_SHA256` moved to `c2c165ac…` **in the same change as the schema** (finding 2).
- `SCHEMA_FLOORS` 47 → 53: the root `required` superset drops `sources`; the root `properties` key set gains `$seed` and `retiredBy`; six new floors pin both new properties' `type`, `pattern` and `maxWords`. A schema edit that deletes `$seed` is `SCHEMA-LOOSENED` (arm 111).
- **`check_receipt()`** (new) — the one-pointer law, asked per node BEFORE the source pointers so "no receipt" is named as itself and not as an absent key. Both → `S-SOURCE`; neither → `S-SOURCE`; a `$seed`/`retiredBy` id not in the store → `R1-DANGLING`.
- **`retired_map()` / `live_nodes()`** (new) — the drop-out set and the derivation's view.
- **`derive()`** — takes `live_nodes(...)`: a retired node produces no status row, no edge, no defaults line. The drop-out happens at the ONE place all three files are derived, so "everything generated" needs no per-file rule. Nothing about the retired set is written into the bodies, so with zero retired nodes the three files are byte-identical to `#239`'s.
- **`generated_node_ids()`** (new) + **`freshness()`** — `R4-RETIRED-GENERATED` when a retired id is named as a ROW of a generated file. Read structurally (`rows[].id`, `edges[].polarity`, the declaration's row lines), never by scanning raw text — see finding 4.
- `gate()` banner — `rows N (live N · retired N)` and a `receipts (s240-D3):` line counting R1-row receipts, `$seed` receipts and retirements.
- The `unclaimed` refusal's remedy text now names retirement as the legal form instead of "no legal form yet (Dave's)".
- Module docstring: a `#242 LANE P` block stating the receipt rule and the "retirement is ADDITIVE" reading; `R4` roster updated.
- Selftest: 11 new arms (below) + one re-cut (`S sources missing`, `S-SCHEMA` → `S-SOURCE`), and the summary line now counts `new #242 (s240-D3 receipt) arms`.

**3 · The mutation arms — every refusal driven BOTH WAYS** (`assets/…/mutation-arms.txt` for the CLI transcript, `selftest.txt` for the same arms inside `--selftest`):

| # | arm | expect | verdict |
|---|---|---|---|
| 99 | BREAK: schema `title` edited, `SCHEMA_SHA256` NOT moved | red | `SCHEMA-PIN-MISMATCH` — "sha256 `ddd06384…` is not the pinned `c2c165ac…`" |
| 104 | GREEN: a NEW polarity `pl-31` with `$seed: s240-D3` and no `sources` | green | rc 0 (`--write`) |
| 105 | BREAK: `$seed: s999-D9` | red | `R1-DANGLING` — "`pl-31.$seed 's999-D9'` is not a knowledge/_rulings.json id" |
| 106 | BREAK: `pl-01` carries its R1 `sources` **and** a `$seed` | red | `S-SOURCE` — "carries BOTH … THE RECEIPT IS ONE POINTER PER NODE" |
| 107 | BREAK: a node with NEITHER receipt | red | `S-SOURCE` — "`pl-32`: carries NO receipt" |
| 88 | BREAK (re-cut): `sources` key deleted from `pl-01` | red | `S-SOURCE` (was `S-SCHEMA` at #239 — the floor moved, it did not vanish) |
| 108 | GREEN: `pl-30` retired by a real ruling id, `--write` | green | rc 0 |
| 109 | BREAK: `pl-30` retired, `_generated/` not re-derived | red | `R4-RETIRED-GENERATED` **+** `STALE-GENERATED` |
| 110 | BREAK: `retiredBy: s999-D9` | red | `R1-DANGLING` |
| 111 | BREAK: `$seed` deleted from the SCHEMA's `properties` | red | `SCHEMA-LOOSENED` + `SCHEMA-PIN-MISMATCH` |
| 112 | GREEN: `pl-02` retired — its id is quoted in the derivation's STATIC prose | green | rc 0 (the fix in finding 4) |
| 113 | GREEN: DROP-OUT PROOF — `--check` names the leak · `--write` re-derives · the row SURVIVES in `polarities.json` and is in NONE of the three generated files | green | rc 0, `still_in = []`, `kept_row = True` |
| 114 | GREEN: `--add-polarity` of a brand-new `$seed` node (dry-run then `--write`), 31 rows, gate green after | green | rc 0 — `#239`-F green control (e), which had no legal form |

**4 · Lane F's seven green controls, re-driven** (`assets/…/six-controls-s240-D3.txt`) — each LITERALLY as V wrote it and in its `s240-D3` legal form:

| control | literal, under the built gate | `s240-D3` legal form | verdict |
|---|---|---|---|
| 120 links-empty-array | **GREEN** | — | unchanged |
| 100 row31, fictional source path | RED `S-SOURCE` (correct: the node named its own oracle) | the same new node with `$seed` | **GREEN** |
| 225 `sources.path=/etc/hostname` | RED `S-ID`+`S-SOURCE` (correct) | one legal receipt; the two-receipt variant is RED `S-SOURCE` by design | **GREEN** |
| 235 orphan stub | RED `R3-JUDGEMENT-FIELD` (correct: phrase not verbatim) | `#239`-F (a): orphan stub, phrase verbatim from R1 | **GREEN** (unchanged by `s240-D3`) |
| 248 all-stub node, path `x` | RED `S-SOURCE` (correct) | the same all-stub node with `$seed` | **GREEN** |
| 321 writer into an EMPTY array | RED `S-SOURCE` (correct: 30 frozen rows unclaimed) | the 30 rows **RETIRED**, `--write`, then the writer appends the `$seed` node | **GREEN** — 31 rows kept, 0 retired ids in `_generated/` |
| 326 writer on a 2-space file | RED `S-SOURCE` (correct: the entry cited `selftest`) | the same entry with `$seed`, same 2-space file | **GREEN**, 31 rows |

**5 · V's `escaped-repro.txt`, re-driven** — `assets/…/escaped-now-caught.txt`: `TOTAL: 48 rows re-driven · CAUGHT 44 · still ESCAPED 4 (RULED 0 · PROMISED 0 · UNRULED 4)`; `RULED 16/16` · `PROMISED 26/26` · `UNRULED 2/6` with `241 · 243 · 245 · 301` still escaping — lane F's exact figure. **ESCAPED did not rise.**

**6 · `polarities.json`: BYTE-UNTOUCHED.** sha256 `02d56dc4bca8be53ee5d6e83778bc104c0b2624ee0900bab3e2bbdad5f531c1b` (P's / F's receipt). `principles.json` `c0165ace…` and `stubs.json` `a7d3e274…` likewise; `_generated/` does not appear in `git status`. **No data row was edited and none needed to be** — every green control was reached by a receipt-shaped change, not a data change.

**Written** (repo-relative): `knowledge/_validate_polarities.py` · `knowledge/brain/schema/polarity.schema.json` · this report · `notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt/` (3 drivers + 5 transcripts + `_seam_block.sh` + `_superseded/`). Nothing else. `git status` also shows `knowledge/_graph-mark-observations.jsonl`, `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` modified and `knowledge/_boot_decompose.py` + the two lane-F files untracked — **none of those is this lane's**; they were in the tree when I arrived or belong to lane F / session hooks, and I did not touch them.

## Findings

1. **The receipt widens without loosening anything.** `sources` leaves the schema's `required` (probe: `required` is now `["id","parties","mediating_variable","links"]`), but arm 88 shows deleting the key is still rc 1 — `S-SOURCE`, "carries NO receipt" — and arm 107 shows a fresh node without either receipt is refused. The floor moved from the schema into `check_receipt()`, which is the same trade `#239` made for the five refusals (Q2 (c)).
2. **The pin moved with the schema, and the break arm proves it is a pin.** `42f845036705db1b…` → `c2c165ac126d878d…`. Probe: `mutation-arms.txt` PIN section — a `title`-only edit with the constant left alone is `⛔ REFUSED (SCHEMA-PIN-MISMATCH) — schema/polarity.schema.json sha256 ddd063848e206361… is not the pinned c2c165ac126d878d…`.
3. **The drop-out is enforced at the generator, not per file.** `derive()` is the single place all three generated files are built, so `live_nodes()` there is the whole of "drops out of everything generated from the KG". Probe: arm 113 — `pl-30` retired, `--write`, then `polarities.json` still carries `pl-30` while `generated_node_ids()` over all three files returns a set without it (29 rows in `polarity-status.json`, down from 30).
4. **DEFECT FOUND AND FIXED MID-LANE: a raw-text leak scan reads the derivation's own prose as a leak.** My first `R4-RETIRED-GENERATED` implementation searched the generated files' TEXT for each retired id. `polarity-status.json` carries a static `delta_vs_237T.cause` string that names `pl-22` and `pl-02` in prose, so retiring all 30 rows and running `--write` stayed rc 1 forever — the gate refused a correctly derived file. Probe: the first run of `_drive_six_controls.py`, `321 s240-D3 step 1 … rc=1 RED R4-RETIRED-GENERATED · retired ids leaking into _generated/ = ['pl-02','pl-22']`. Fix: `generated_node_ids()` reads `rows[].id`, `edges[].polarity` and the declaration's row lines — the file's DATA positions, never its prose. A hand edit that pastes an id elsewhere is already `content_sha256`'s job. Arm 112 is the standing control (retire `pl-02` specifically and go green). **This is the class `#242`'s reader should carry forward: a text scan over a generated file cannot tell a derived row from a quoted example.**
5. **The six FALSE-RED controls are green in their `s240-D3` form; they are NOT green literally, and that is correct.** Four of them (100 · 225 · 248 · 326) were red because the node named its own quote oracle — `#239`'s Q3, which `s240-D3` does not touch. Driving them literally still refuses `S-SOURCE`, and making them pass literally would re-open V's escapes 100/225/248/324. What `s240-D3` supplies is the legal receipt they lacked; with it, each goes green (probe: `six-controls-s240-D3.txt`, every line marked `OK`). If Dave meant the LITERAL control shapes must pass, that is RULING-SHAPED 1 below — but it would be a regression, and I did not build it.
6. **TRAP FOR V2: the `_seam_block.sh` filed in `#239`'s assets is V's `#238` block, not the block lane F edited.** Re-driving `escaped-repro.txt` from the filed assets alone reports `D2 ESCAPED` (rc 0, "NO DECLARED LINE") and a total of `ESCAPED 5` — a FALSE escape, because the filed copy has no `POLARITY_BRAIN_DIR` redirect declaration and no tree's-own-home re-gate, which live only in `knowledge/_git_commit.sh:301-333`. Probe: my second run of `_escaped_now_caught.py` (`D2 PROMISED ESCAPED (b) POLARITY_BRAIN_DIR=<clean copy> rc=0 names=[]`). Extracting the block fresh from `_git_commit.sh` makes `D2` CAUGHT and the total `ESCAPED 4`. The re-extracted block is filed beside this report as `_seam_block.sh`; `#239`'s asset was left untouched (ADR-0017, write-once). Absent this file, V2 will read a regression that is not there. A third false escape (`D1`, rc 127) came from simply not copying any `_seam_block.sh` into the run root — the harness needs `brain-real`, `standalone/`, `_graveyard/` and `_seam_block.sh` seeded before it runs.
7. **A `$seed` node has no source row, so `#239`'s Q5/Q3 verbatim checks do not reach it.** `hays` is empty for such a node, so its `note` and `mediating_variable` are bounded only by `maxWords` (15 / 25) and are not checked verbatim against anything; any quote on one of its links is `R3-QUOTE-NOT-VERBATIM` ("cannot be verified"), which means **a `$seed` node cannot carry a `resolvedBy` at all** (a resolvedBy needs a verified quote, `R3-QUOTE-MISSING` if absent). Probe: `check_quotes_verbatim()` at the `if not hays:` branch, and arm 104's node carries `links: []` for exactly this reason. This is the conservative side and is RULING-SHAPED 2/3.
8. **A retired node is still fully validated.** It keeps its R1 `sources` claim (so the bijection is unaffected — retiring is not deleting), its parties must still resolve, its links must still be live and its quotes still verbatim. Only the DERIVATION ignores it. Probe: arm 108 retires `pl-30` and the gate still reports `parties`/`links` counts over all 30 rows; arm 110 shows a bad `retiredBy` on a retired node is still rc 1.
9. **The live tree is green and the derivation did not move.** `live-check.txt`: `rows 30 (live 30 · retired 0)` · `receipts (s240-D3): ONE pointer per node — R1 register row 30 · $seed ruling id 0 · retiredBy 0` · `schema pinned c2c165ac126d… + 53 floors` · all three generated files "content byte-identical" at P's clock `2026-09-02T15:18:55Z`. No `--write` on the live tree was needed or run.

## RULING-SHAPED QUESTIONS

⛔ **MANDATORY SECTION.** Nothing below is decided. Each is Dave's.

1. **Did "the six false-red controls become legal under it" mean their LITERAL shapes?** As built, each control's `s240-D3` legal form is green and the literal shape stays red because the node names an oracle it invented (`#239` Q3). (a) as built — the Q3 refusal stands and the receipt is the thing that widened; (b) also allow a node to cite an arbitrary `sources.path`, which re-opens V's escapes 100 · 225 · 248 · 324. Recommend (a); (b) is a regression and was not built.
2. **What is the quote oracle for a `$seed` node?** Today: none, so it may carry no quote and therefore no `resolvedBy`. (a) leave it — a node born of a ruling states no quotes (~0 lines, as built); (b) the haystack becomes the seeding ruling's own prose in `knowledge/_rulings.json` (~8 lines, and a second oracle is the Q3 question `#239`-F RULING-SHAPED 4 (a) already put to you); (c) the quote must be verbatim in the ruling named by the LINK, not the seed. Recommend (b) when the first `$seed` node needs a `resolvedBy`; not before.
3. **Are `note` / `mediating_variable` on a `$seed` node free text?** Today yes, bounded only by `maxWords` (finding 7). Options: (a) as built; (b) verbatim against the seeding ruling's prose (same machinery as 2 (b)). Recommend deciding 2 and 3 together.
4. **Is `retiredBy` a SECOND receipt, or additive?** Built as ADDITIVE: exactly one of `{sources, $seed}` is the birth receipt, and `retiredBy` may sit beside either. The strict reading of "the receipt is one pointer per node" would refuse a retired `$seed` node. Recommend as built — retirement is a different event from birth.
5. **Must a `$seed` / `retiredBy` ruling be LIVE?** Built as PRESENCE only (the id is in `knowledge/_rulings.json`). `#239`'s Q1 refuses a `resolvedBy` to a not-live ruling; a receipt arguably names history and should survive supersession. Recommend as built; the tighter side costs 2 lines.
6. **`R4-RETIRED-GENERATED` is a NEW sub-form name** — `#239`-F RULING-SHAPED 5's class (a roster change). It is listed in the schema's `x-refusals` and the gate's docstring, and no prior harness expects a different name for this case. Alternative: fold it into `STALE-GENERATED` and lose the "why". Recommend as built.
7. **Should `stubs.json` entries get a `$seed` too?** `s240-D3` says "a polarity's receipt", so stubs were left alone: a stub's phrase must still be verbatim in the frozen R1 register, which means a stub born after R1 has no legal form. Control 235's legal analogue is green only because a verbatim phrase exists. Price: the same two floors + `check_stubs` (~10 lines). Not built — it is outside the ruling's words.
8. **`#239`-F's RULING-SHAPED items 1–9 are all still carried**, in particular Q9 (the four contested migration rows and the 6·4·20 sort, untouched here) and the 4 UNRULED escapes (`241 · 243 · 245 · 301` — `W-374`), which this lane did not touch and which the brief forbade touching.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** V2 itself — the brief's close condition ends "and V2 has run against the built gate", and V2 is the conductor's lane. Everything up to it is driven here. Price: one V2 lane.
- **UNPROVEN:** `knowledge/_test_git_commit.py --selftest` (the seam harness, 44 arms) on the current tree — it spawns `git` inside its fixture, which this lane may not do. The seam block was NOT edited by this lane (`_git_commit.sh` does not appear in `git status`), so the risk is inherited, not new. Price: one git-capable run, ~7 s.
- **UNPROVEN:** the build LOOP's routing of rc 1 from step [141] through `main()` — driven here only through the build's subprocess form inside `escaped-now-caught.txt` (row D1: `B(build form)=1`), never through a real `--range` run (forbidden: it writes chunk state). Price: the conductor's CI run. `_build_all.py` was not run at all, per the fence.
- **UNPROVEN:** that no OTHER consumer reads `knowledge/brain/polarities.json` and would need the retired filter. Probe run: a repo-wide grep for `polarities.json` / `brain/_generated` outside `knowledge/brain/` returns `_validate_polarities.py`, `_build_all.py`, `_git_commit.sh` (all of which go through this gate) plus `_state.json`, `_rulings.json`, `_memento-index.json` and `_tmp/wrap*` (prose mentions, not readers). That is a grep, not a proof that a future consumer will filter. Price: one `--probe` of the pack manifest, ~2 min.
- **CLAIMED:** that the three `.jsonl` files and `_boot_decompose.py` showing in `git status` are not this lane's — asserted from what this lane wrote (2 repo files + its own asset directory), not from a `git stash`-and-compare. Re-read costs one `git diff` per file at the conductor's seat.

## PITFALLS (consequences replayed — owner per row)

| | risk | what is built against it | owner |
|---|---|---|---|
| 1 | A schema edit is STILL a two-file commit (schema + `SCHEMA_SHA256`) — now with 53 floors, so more edits trip it | arm 99 + the refusal names the constant and the file | whoever edits the schema |
| 2 | Re-driving `escaped-repro.txt` from `#239`'s FILED assets reports a false `D2 ESCAPED` (finding 6) | the re-extracted `_seam_block.sh` is filed beside this report; extract from `_git_commit.sh` if in doubt | V2 / anyone re-running the harness |
| 3 | A text scan over a generated file reads the static `delta_vs_237T` prose as a leak (finding 4) | `generated_node_ids()` reads rows, not text; arm 112 is the standing control | whoever extends the generated files |
| 4 | A `$seed` node's `note` / `mediating_variable` are unverified free text bounded only by word count | finding 7 + RULING-SHAPED 2/3; `maxWords` still bites | Dave |
| 5 | A `$seed` node cannot carry a `resolvedBy` today — the first one that needs to will be refused `R3-QUOTE-MISSING`/`NOT-VERBATIM` | the refusal text says the quote cannot be verified; RULING-SHAPED 2 prices the fix | Dave |
| 6 | "Retire" and "delete" look alike to an author; deleting still orphans a frozen row | the `S-SOURCE` unclaimed refusal now NAMES retirement as the legal form instead of saying there is none | whoever removes a polarity |
| 7 | `--check` on a retired-but-not-re-derived home prints TWO names (`R4-RETIRED-GENERATED` + `STALE-GENERATED`); a reader may treat the second as the cause | the retired name is printed first and carries the remedy | reader |
| 8 | The selftest is now 136 arms and copies the home ~136 times under `/dev/shm` (~6 s) | unchanged `finally` cleanup (V finding 16) | sandbox hygiene |

## Evidence

`notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt/` —
`mutation-arms.txt` (**the both-ways proof**: 6 green controls + 7 break arms at the CLI, each with its command, rc and red-by-name line) · `_drive_arms.py` (its generator) · `six-controls-s240-D3.txt` (lane F's seven green controls, LITERAL vs `s240-D3` legal form, every line `OK`) · `_drive_six_controls.py` (its generator) · `escaped-now-caught.txt` (V's 48 rows re-driven standalone in V's order — `CAUGHT 44 · ESCAPED 4`) · `_escaped_now_caught.py` (lane F's generator, re-seated on 3 constants — `REPO`, `F`, `OUT_DIRS`) · `_escaped-run.log` (its stdout) · `_seam_block.sh` (the block re-extracted from `knowledge/_git_commit.sh:301-333` — finding 6; `#239`'s filed copy is the pre-fix one and was left untouched) · `selftest.txt` (136 arms, 0 failures) · `live-check.txt` (the live tree, GREEN) · `_superseded/` (one intermediate selftest log the mount would not let me remove).

REPLAY-THESE: `assets/…/six-controls-s240-D3.txt` (~0.6K — the seven controls, literal vs legal, and why four literals stay correctly red) · finding 6 + `assets/…/_seam_block.sh` (~0.3K — **read this before V2 runs**, or V2 reads a false `D2` escape) · finding 4 (~0.3K — the raw-text leak-scan defect and the class it belongs to) · RULING-SHAPED 1–3 (~0.5K — the literal-controls reading, and the quote oracle a `$seed` node does not have) · `assets/…/escaped-now-caught.txt` TOTAL block (~0.2K — `CAUGHT 44 · ESCAPED 4`, the four UNRULED unchanged)

---

## #242 lane P2 addendum — 2026-09-03

*(APPEND-ONLY. Lane P's text above is untouched. Lane P2 is a three-fix window against V2's findings 3 and 4 plus `ds-021`; it rules nothing, commits nothing, and left `polarities.json` / `principles.json` / `stubs.json` byte-untouched — `polarities.json` still `sha256 02d56dc4bca8be53…`, and `knowledge/brain/_generated/` is absent from `git status`, so the three generated files are byte-identical to HEAD.)*

### Fix 1 — THE LEAK (V2 finding 3): `delta_vs_237T.cause` is DERIVED, and the leak check reads every BYTE

**What was wrong.** `delta_vs_237T.cause` was a hardcoded string literal in `derive()` naming `pl-22` and `pl-02` whether or not they were live, and the leak check read only the derived ROWS. Retire all 30 nodes, re-derive, and the gate went GREEN while `polarity-status.json` still contained `pl-02` and `pl-22` — and lane P's arm 112 certified that as correct.

**What changed** (`knowledge/_validate_polarities.py`): `DELTA_CLAUSES` / `DELTA_FIGURE` (module constants) + `delta_cause(rows_by_id)` — each clause is keyed by the node it is about and is emitted ONLY while that node still has a derived row; the r1 id in it is a LOOKUP against the row, not a re-typed literal. `derive()` calls it. `id_in_raw_text()` is new and `freshness()` now refuses a retired id ANYWHERE in a generated file's bytes, naming WHICH position leaked (`as a derived ROW` vs `in its text (not as a row — a leak a row-only check cannot see)`).

⚠ **BYTE-NEUTRAL, and that is the probe.** With both nodes live the joined text is byte-identical to the literal it replaced, so `--check` on the live tree stays GREEN with all three files `content byte-identical` and nothing under `_generated/` moves. This is a de-hardcoding, not a content edit.

**Driven both ways** (temp copy under `/dev/shm`, real brain copied, `POLARITY_BRAIN_DIR` redirect):

```
# retire pl-02 in a copy of knowledge/brain, then:
python3 knowledge/_validate_polarities.py --check   # rc 1 — R4-RETIRED-GENERATED ×3 (+ STALE ×3)
python3 knowledge/_validate_polarities.py --write   # rc 0
python3 knowledge/_validate_polarities.py --check   # rc 0
# RAW grep of EVERY file under _generated/ for the retired id:
#   defaults-declaration.txt: 'pl-02' present=False
#   polarity-edges.json:      'pl-02' present=False
#   polarity-status.json:     'pl-02' present=False   ← the leak, closed
# pl-02 KEEPS its row in polarities.json: True
```

RED BY NAME: `⛔ REFUSED (R4-RETIRED-GENERATED) — _generated/polarity-status.json still names 'pl-02' as a derived ROW, a node RETIRED by ruling 's240-D3' — a retired node keeps its row in polarities.json and DROPS OUT of everything generated from the KG (s240-D3)`.

**Arm 112 RE-POINTED** — it was a GREEN control asserting "a prose mention is NOT a leak"; it is now a BREAK ARM, and it drives both halves in one arm: retire `pl-02` → `--write` → its id is gone from every BYTE of all three files; then replant it in the derivation's PROSE ONLY with a self-consistent `content_sha256`, where the ROW check is provably blind (`row_blind=True`) → the gate still refuses **`R4-RETIRED-GENERATED` BY NAME**, rc 1.

**MUTATION TEST (the arm bites the clause, not the feature).** Restore the hardcoded literal (`delta_cause` emits regardless of the live set) and re-run: `112  FAIL … arms 137 · red arms 121 (went red by name 120/121) · failures 1`. File restored byte-exact afterwards (sha256 `8725e67b27fe42df…` before and after).

### Fix 2 — THE FLOOR (V2 finding 4): the WIDENING is floored, not just its refusals

**What was wrong.** `SCHEMA_FLOORS`' `required` entry is a `superset` check, so putting `"sources"` back into the schema's `required` reads as a TIGHTENING, passes `SCHEMA-LOOSENED` even with the pin honestly moved, and silently makes every `$seed` node illegal.

**What changed**: a new floor kind **`excludes`** (`required` carries NONE of these) + the pin `("", "required", "excludes", ["sources"])`, and the floor is APPLIED REGARDLESS — `sources` is stripped back out of the effective schema so the legal `$seed` node beside it still passes. Floors 53 → 54.

**Command / arm** (`s240-D3 FLOOR ARM`, arm 113 — the pin is moved HONESTLY to the mutant's sha, exactly what a real two-file schema edit does, so this is a floor check on the SCHEMA TEXT and not on the pin):

```
python3 knowledge/_validate_polarities.py --selftest   # arm 113
```

RED BY NAME: `⛔ REFUSED (SCHEMA-LOOSENED) — schema.required: ['sources'] is back in required, which the pinned floor EXCLUDES (#242 lane P2, s240-D3) — it reads as a tightening, but it legislates away the RECEIPT WIDENING Dave ruled … A schema may only tighten a REFUSAL, never a PERMISSION; the floor is applied regardless`. The arm also asserts `SCHEMA-PIN-MISMATCH` is NOT in the names (the pin was moved, so only the floor bit — V2's separation) and `S-SCHEMA` is NOT in the names (the floor was applied, so the `$seed` node survived).

**MUTATION TEST.** Delete the `excludes` floor entry and re-run: `113  FAIL … rc=1 names=['S-SCHEMA'] :: ⛔ REFUSED (S-SCHEMA) — pl-31.sources: required key 'sources' is missing` — V2's finding-4 consequence, reproduced exactly. `failures 1`. File restored byte-exact.

⚠ **DECLARED, not decided:** the refusal keeps the existing name `SCHEMA-LOOSENED` for a change that is technically a tightening. A new vocabulary word for it would be a naming decision, which this lane has no mandate to take — the detail line says plainly which direction was breached. Dave's, if he wants a distinct name.

### Fix 3 — `ds-021`: `_boot_decompose.py` registered

**What was wrong.** Lane F's new measurer counts `cl100k` and was not in `MEASURERS`, so the wrap gate FAILED on it (the ds-021 (C) birth-catch, working as designed).

**What changed** (`knowledge/_capture_gate.py`): registered `'_boot_decompose.py': ('estimate-only', …)` with the WHY — it counts cl100k TAPE over the DISK-RESIDENT boot inputs; a REAL boot figure comes only from `message.usage`, which it never sees (it takes the real total as `--real N` and prints the harness remainder as `<real> − Σ(ours, tape)` labelled ESTIMATED-BY-SUBTRACTION). Its tape figures are never summed with or scaled to a `real` measurement.

```
python3 knowledge/_capture_gate.py --wrap 2>&1 | grep -c "FAIL ds-021"   #  1  →  0
```

It now sits in the DECLARED-GAP warn list beside `_boot_remeasure.py` and `_context_gauge.py`, which is the honest resting place for an estimate-only measurer.

### Selftest, run last (the fence's closing act)

```
TMPDIR=/dev/shm python3 knowledge/_validate_polarities.py --selftest
arms 137 · red arms 121 (went red by name 121/121) · green arms 14 · no-fire/77 arms 2 ·
new #239 arms 72 · new #242 (s240-D3 receipt) arms 12 · failures 0
✓ selftest OK — control green; every refusal arm red by its name; nothing written on refusal
```

136 → **137 arms** (one green control replaced by two break arms), `#242` arms 11 → 12, **failures 0**. Live tree: `python3 knowledge/_validate_polarities.py --check` → rc 0, GREEN, all three generated files `content byte-identical`.

### Fence

No rulings. `polarities.json` / `principles.json` / `stubs.json` byte-untouched. No store / GM / `_LIVE-STATE` / `_CARRIES` / memory edits. No commit, no push, no `_build_all.py`. Every temp copy lived under `/dev/shm` and is gone. Changed paths: `knowledge/_validate_polarities.py` · `knowledge/_capture_gate.py` · this file (appended).

**STILL OPEN — not this lane's to take:** V2's RULING-SHAPED 1 asked *whether* "drops out of everything generated" means every row or every byte. Lane P2 was briefed to build the every-byte reading and did; **Dave has not confirmed it**, and the `SCHEMA-LOOSENED` naming above is the second open item. V2's RULING-SHAPED 3 (the six false-red controls) and 4 (`$seed` naming a superseded id), and lane P's own 1–8, are untouched and still carried.
