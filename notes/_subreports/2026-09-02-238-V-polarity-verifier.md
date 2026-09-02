# `#238`-`V` — the polarity gate, tested to failure: three doors agree, and 48 hostile rows walk through all three

session: `#238` · 2026-09-02
window: Fable conductor, lane V (adversarial verifier, `s172-D3` depth cap 1 — report, never fix)
sub index: `V`
brief: `notes/_briefs/2026-09-02-238-V-polarity-verifier-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`. SHAPE: ~45 tool calls · 1 harness (`_v_attack.py`) + 4 wave scripts written · 111 attacks driven (97 harness arms × 3 doors + `--write` + 3 doors again; 10 writer-door probes; 2 door-asymmetry probes; 2 argv probes) · `--selftest` run 7 times (live + 6 mutants) · T's `_derive_sort.py` re-seated and re-run · 0 git commands · 0 writes under `knowledge/` · 0 edits to dated history · seat `wonderful-adoring-euler`, all copies under `/sessions/wonderful-adoring-euler/mnt/outputs/v238/`.

## VERDICT

Lane P's own claims hold at this seat: the live tree is **green** (`--check` rc 0, 0.096 s), the live `--selftest` reproduces **55 arms, 45/45 red by name**, the three derived views are **deterministic** (two `--write` runs at different clocks, one with `_generated/` absent, are byte-identical with the clock stripped and equal to the live tree), and the three real doors — CLI, the `_build_all.py` STEPS entry in its own subprocess form, the `_git_commit.sh` block run with `fail()` — **agreed with each other on rc and refusal name on 96 of 96 arms, never wrote a byte on refusal, and an accepting `--write` never touched a home file**. What P's self-test cannot see is what it was not built to look for, and there is a lot of it: of **100 attacks that a correct gate should refuse, 39 were caught by name, 48 ESCAPED, 10 CRASHED (a traceback, no name — at every door the build's remedy and the seam's `fail` text still say "the refusal is NAMED above"), 3 were red under the wrong name.** The escapes fall into eight classes, and the headline four are structural rather than typos: **(1)** R1's "live registers" is one field — `superseded_by`, present on 1 of 328 store rows — so a `resolvedBy` to a ruling superseded in prose, PARKED, or "still open" resolves and *closes the polarity*; **(2)** the quote-verbatim guard trusts an oracle the node names itself, so a paraphrase passes by breaking the pointer, repointing it at `_rulings.json`, or at the node's own file, and an empty / one-word / absent quote closes a row as `resolved`; **(3)** the schema file is an unguarded loosening surface — six loosenings pass `--check` (one of them, `sources[]` extra keys, passes `--selftest` too), and because the seam runs only `--check`, five of them commit cleanly and abort the *next* build at [142]; **(4)** refusal 3 stops at `additionalProperties`: a 14-word verdict in `note`, 300 words in `mediating_variable` or `sources[].id`, a 15-word verdict as a stub phrase, and a zero-width-space join that makes 44 words count as one all pass. Plus: the clock is unvalidated (`generated_at: banana` is "fresh"), the closed home has six open edges (dotfiles, `.tmp` leftovers, anything under `schema/`, `__pycache__`), `POLARITY_BRAIN_DIR` is a *silent* hatch at the seam beside the spelled `POLARITY_ACK`, an absent home is rc 77 and the build *continues*, and `--dry-run --write` writes. The migration is a declared per-row table (the L-rules are labels), and my own reading disagrees on 3 of 21 links (tn-02, tn-27, tn-29) and on the rule-letter for the one row that moves the sort (tn-22); under my reading tn-27 re-opens and the sort is T's 6·3·21. The 6·9·15 in `s238-D6` is explained and **proven by recount**: it is every non-obligation row whose `apollo_touch` names any ruling id, all read as resolved. Regions of the brief: **all five DONE**; nothing fixed (depth cap 1).

COUNTS: findings `18` · ruling-shaped `10` · UNPROVEN `6`

BRIEF COUNTS: attacks `111` driven (harness 97 · writer 10 · doors 2 · argv 2; 4 void: 1 setup crash, 2 misfires, 1 non-test) · expect-red `100` · caught `39` · **ESCAPED `48`** (RULED 16 · PROMISED 26 · UNRULED 6) · CRASH `10` · MISNAMED `3` · green controls `7/7` · migration disagreements `3` (+1 rule-letter) · determinism `OK` · live --check `GREEN` · UNPROVEN `6`

## ESCAPED — the headline, first (every row: `assets/…/escaped-repro.txt` carries the standalone command)

Grades: **RULED** defeats the letter of a ruled refusal or property · **PROMISED** defeats a promise the gate, schema or P's report makes that no ruling states · **UNRULED** nothing ruled — an observation with an owner. The decisive door for a home mutation is `--write` (it either accepts and re-derives, or refuses by name); for a generated-file or stray-file mutation it is `--check` as-is.

| # | grade | what passed all three doors | root |
|---|---|---|---|
| 30 | RULED | `resolvedBy s200-D2` — superseded by `s200-D3` in **prose** ("supersedes s200-D2's theme scope"), no `superseded_by` field → pl-03 derives `resolved`, sort 6·4·20 → 6·5·19 | R1 reads one field; the store's `status` is free prose |
| 31 | RULED | `resolvedBy gauge-band` — status "retire-or-pin FORKED TO DAVE and still open" → `resolved` | same |
| 32 | RULED | `resolvedBy s182-D1` — status PARKED → `resolved` | same |
| 110 | RULED | schema `parties.minItems` 2→1 + pl-01 with one party → green; caught **one build later** by [142] arms 32+37 | no pin on the schema; seam runs `--check` only |
| 111 | RULED | schema `type.enum` + `relatedTo` + a `relatedTo` link (the fifth type `s238-D6` does not rule) → green; [142] arm 14 catches next build | same |
| 112 | RULED | schema `parties.items.additionalProperties: true` + `why` on a party → green; [142] arm 21 next build | same |
| 310 | RULED | schema `sources.items.additionalProperties: true` + `judgement` on a source → **`--check` green AND `--selftest` green (55/55)** — a TOTAL escape | no arm probes `sources[]` |
| 210 | RULED | `.edges.json` (an authored edge list) at the brain top | `check_home_dir` skips names starting with `.` |
| 211 | RULED | `_generated/.authored-edges.json` | same |
| 212 | RULED | `_generated/.polarity-edges.json.tmp` — a half-written file from an interrupted `--write` | same |
| 213 | RULED | `schema/edges.json` (an authored edge list) | `schema/` is in `ALLOWED_TOP`; its contents are never listed |
| 216 | RULED | `__pycache__/edges.json` | skipped by name |
| 230 | RULED | `note`: "Jakob must always win in Apollo because Dave rules by eye and prefers familiarity" (14 words) | `note` is bounded, never verbatim-checked (the schema calls it "a verbatim gloss") |
| 231 | RULED | `note`: 44 visible words joined by U+200B → `words()` = 1 | `str.split()` does not split on Cf characters |
| 232 | RULED | `mediating_variable`: a 300-word verdict | `minLength 1`, no `maxWords` |
| 233 | RULED | `sources[0].id`: a 300-word verdict on pl-04 | `minLength 1`, no bound; pl-04 has no quotes so nothing is even UNVERIFIED |
| 22 | PROMISED | a stub whose phrase is one U+200B (visually empty) | `.strip()` does not strip U+200B |
| 328 | PROMISED | the same stub through `--add-stub --write` → written | same, at the writer |
| 234 | PROMISED | a stub phrase that is a 15-word verdict, declared as a party | a "verbatim phrase" nothing can check |
| 70 | PROMISED | `generated_at` 2099-01-01 on all three derived files → "fresh" | the sha excludes the clock; `--check` re-derives AT the on-disk clock, so any string is its own oracle |
| 71 | PROMISED | `generated_at: banana` → "fresh (generated_at banana, content byte-identical)" | no shape check on the clock |
| 82 | PROMISED | `$migration.verdicts = {"pl-01": "Jakob wins in Apollo …"}` | `$migration` / `$description` are allowed keys with unvalidated content |
| 83 | PROMISED | `$description` replaced by 500 words of verdict | same |
| 93 | PROMISED | `sources[0].id` = `tn-0１` (fullwidth 1) → pl-01's quote "UNVERIFIED (declared, not passed)" beside "✓ GREEN", rc 0 | a broken pointer launders every quote on the node |
| 222 | PROMISED | P arm 23's paraphrase + `sources.path` → nowhere → UNVERIFIED, green | same |
| 311 | PROMISED | schema `sources.minItems` 0 + `sources: []` + the paraphrase → green; [142] arm 23 next build | same + no pin |
| 220 | PROMISED | `sources` → `knowledge/_rulings.json` # `s238-D7`, quote = 13 words *of the ruling* → "verified" | the node names its own oracle |
| 300 | PROMISED | `sources` → `knowledge/brain/polarities.json` # `pl-01`, quote = 8 words of its own `mediating_variable` → "verified" | same |
| 223 | PROMISED | `resolvedBy s116-D1` with `quote: ""` → verified (`"" in anything`); pl-01 → `resolved` | an empty receipt closes a row |
| 224 | PROMISED | `resolvedBy s116-D1` with `quote: "the"` → verified; pl-01 → `resolved` | a one-word receipt |
| 400 | PROMISED | `resolvedBy s116-D1` with no quote at all → pl-01 → `resolved` | `quote` is optional; only the migration brief demanded one |
| 324 | PROMISED | `--add-polarity --write` of an entry whose quote has no reachable source → "1 UNVERIFIED (declared, not passed)" and **written** | the writer runs the same gate |
| 401 | PROMISED | pl-04's `sources[0].id` → `tn-02` → `polarity-status.json` copies tn-02's `factory_default` / `ask_when` onto pl-04 | `r1_id` is taken from a forgeable pointer |
| 312 | PROMISED | schema `note.maxWords` 500 + a 64-word note → green; [142] arm 20 next build | no pin |
| 214 | PROMISED | `schema/polarity.schema.v2.json` — a second schema beside the first | `schema/` unlisted |
| 246 | PROMISED | `$migration.sha256` = 64 zeros | the receipt is decorative — nothing verifies it |
| 247 | PROMISED | `$migration.from` = a path that does not exist | same |
| 403 | PROMISED | `polarities.json` replaced by a symlink to a file outside the home → every door green | the gate reads through; a commit would carry the symlink |
| D1 | PROMISED | the home ABSENT (`POLARITY_BRAIN_DIR=/nowhere`): CLI rc 77 · **build: "COULD-NOT-ASK — declared refusal, build continues"** · seam: blocked (`\|\| fail`) | 77 was designed for shipped packs; in the source repo a deleted `knowledge/brain/` is a mutation |
| D2 | PROMISED | the seam block with `POLARITY_BRAIN_DIR=<a clean copy>` while the tree's `knowledge/brain/` is dirty → "— polarity gate green"; no DECLARED-GAP line; the only trace is the gate's own `home <path>` line | a silent hatch beside the spelled `POLARITY_ACK` (declared passes, silent fails) |
| A1 | PROMISED | `--add-polarity FILE --dry-run --write` → **writes** | `FLAGS` is a membership test for conflicts (#208 class) |
| A2 | PROMISED | `--check --write` → **writes** `_generated/` | same |
| 301 | UNRULED | `principles.json`: `pr-wcag-1-4-3` grade L→C → pl-15 leaves settled-by-obligation, sort 6·4·20 → 5·5·20, no refusal | the register is unguarded; s237-D2 is defeated by a letter |
| 241 | UNRULED | a principle's `statement` rewritten | P's "seeded byte-for-byte" is a receipt of a moment, not a gate |
| 243 | UNRULED | pl-16: `resolvedBy s116-D1` AND `challengedBy s116-D1` | a contradiction no ruling refuses |
| 244 | UNRULED | all 30 rows deleted → 0·0·0 after `--write` | no floor on the row count |
| 245 | UNRULED | all 21 links deleted → 6·0·24 after `--write` | the migration receipt is decorative |
| 402 | UNRULED | pl-01's body duplicated under `pl-31` → edges 22 → 23 | no dedupe of bodies |

## CRASH (red by traceback, not by name) and MISNAMED

| # | input | traceback site (`knowledge/_validate_polarities.py`) |
|---|---|---|
| 44 | party `role: {"side": "a"}` | `roles = {p.get("role") …}` line 402 — `TypeError: unhashable type: 'dict'` |
| 202 | link `type: ["touches"]` | `if key in seen_links` line 463 — unhashable list in the tuple |
| 203 | party `ref: ["pr-fitts"]` | `party_refs = {p.get("ref") …}` line 456 |
| 204 | stub `id: ["st-x"]` | `if s.get("id") in seen_ids` line 325 |
| 250 | `sources: [{"id": "tn-01"}]` (no `path`) on a node with a quote | `_source_row_text` → `os.path.join(REPO, None)` line 505 |
| 251 | `sources[0].path: 5` | same |
| 252 | one non-UTF-8 byte in `polarities.json` | `read_text` → `UnicodeDecodeError` (not `S-PARSE`) |
| 256 | schema `properties: []` | `schema_keywords_supported` → `'list' object has no attribute 'items'` line 190 |
| 257 | schema `id.pattern: "^pl-["` | `re.search` → `re.error` |
| 217 | `_generated` is a FILE | `--check` names `MISSING-GENERATED` (fine); **`--write` crashes** at `os.makedirs` line 816 |

Every crash is rc 1 at all three doors, so nothing bad is committed — but the build prints the GATE remedy ("The refusal is NAMED in the output above") and the seam prints "the refusal is NAMED directly above", and nothing is. Probe: `assets/…/wave3.txt` last block; `assets/…/doors/44-*.txt`.

MISNAMED (red, wrong name): **200** a bare-string link `"s116-D1"` and **201** `type: null` → `S-SCHEMA`, not `R2-UNTYPED` — the most natural untyped link is not named as one; **42** `role: null` → `S-SCHEMA`, not `S-ROLE`. Two of my own arms misfired and are void (114: my 39-word "quote" was not verbatim so `R3-QUOTE-NOT-VERBATIM` fired first — replaced by 312; 221: 22 words tripped `R3-QUOTE-TOO-LONG` first — replaced by 300).

## What was done

**1 · Every refusal through the REAL entry points.** `_v_attack.py` drives each hostile row, on a copy, through **A** `--check --brain <copy>`, **B** the `_build_all.py` STEPS entry in the build's own `[sys.executable, path] + extra_args` form with `POLARITY_BRAIN_DIR` and `route(label)` for the remedy (never the build), **C** the `# ── POLARITY GATE — s238-D7` block extracted verbatim from `_git_commit.sh` and run in a throwaway bash with `fail()` defined (never a commit); then **W** `--write` on a second copy (the decisive door for a home mutation); then A/B/C again on the post-write copy. Tree hashes before/after at every door. Result: **A/B/C agree on rc and on the printed refusal names on 96/96 arms; every refusing door left every byte; every accepting `--write` left the three home files** (`assets/…/TOTALS.txt`). The doors are faithful to `gate()`; the findings are all in `gate()`.

**2 · Hostile rows.** The brief's twelve, each with variants (wave 1, 45 arms), then my own (wave 2, 43; wave 3, 5 + the writer door + the two asymmetries; wave 4, 4 + argv + cleanup + the live selftest). Tables: `assets/…/wave1..4.txt`; per-arm transcripts `assets/…/doors/`.

**3 · The migration table** re-derived from the frozen text with my own reading and diffed row by row: `assets/…/migration-diff.txt`.

**4 · The sort.** T's `_derive_sort.py` re-seated (the `dreamy-relaxed-noether` path substituted, `ASSETS` redirected) and re-run: **whole-file equal to the filed `tension-sort.json`**; side by side with the gate's `polarity-status.json`: they differ on exactly **tn-22**; and a recount from the frozen rows reproduces `s238-D6`'s 6·9·15 exactly (`assets/…/sort-side-by-side.txt`).

**5 · The generated views.** Determinism (`assets/…/determinism.txt`), live `--check` (`assets/…/live-check.txt`), live `--selftest` (`assets/…/live-selftest.txt`).

**Written** (repo-relative): this report · `notes/_subreports/assets/2026-09-02-238-V-polarity-verifier/` (29 files + `doors/` 108 transcripts, ~600 KB of content — see pitfall 4). Nothing under `knowledge/` touched; no git; no edit to any dated file.

## Findings

1. **The three doors are one door.** On 96/96 arms A, B and C returned the same rc and printed the same refusal names; on 0 arms did a `--check` door change a byte; on 0 refused `--write`s did a byte change. P's finding 8 holds. Probe: `assets/…/TOTALS.txt` lines 2–5 (computed from the per-arm JSON, not retyped).
2. **R1's "live" is one field.** `_rulings.json` carries `superseded_by` on **1** of 328 rows (`s129-D1`); four rows say "superseded" in prose (`s123-D3`, `s133-D2`, `s168-D4`, `s200-D3` naming `s200-D2`), one is "still open" (`gauge-band`), three are PARKED. The gate's R1-SUPERSEDED reads only the field, so a `resolvedBy` to any of the others resolves — and **`derive()` counts it**: pl-03 flips to `resolved` on `s200-D2`, `gauge-band` and `s182-D1` alike (arms 30–32; `assets/…/doors/30-*.txt`, `polarity-status.json` in each `brain-w`). Root cause is the store's vocabulary (status is free prose), not a typo in the gate.
3. **The clock is a string nobody reads.** `content_sha256` excludes `generated_at`; `--check` re-derives *at the on-disk clock*, so `2099-01-01…` and `banana` are both "fresh (…, content byte-identical)" (arms 70–71). s238-D3's "with a clock" is satisfied by any text in the slot.
4. **The quote guard trusts an oracle the node names itself.** `check_quotes_verbatim` looks up `sources[].path/id` *from the node*: break the pointer (93, 222, 311) and every quote is "UNVERIFIED (declared, not passed)" while the last line says "✓ polarity gate GREEN" and rc is 0; repoint it at `_rulings.json` (220) or at `polarities.json` itself (300) and a quote of the *wrong text* is "verified". An empty quote (223), `"the"` (224) or no quote (400) on a `resolvedBy` closes pl-01 as `resolved`. The writer accepts and writes an unverifiable quote (324). P's finding 10 ("the gate checks they are") holds only when the author is honest about the pointer.
5. **Refusal 3 stops at `additionalProperties`.** Four fields on the node carry free text: `note` (≤15 words, never verbatim-checked though the schema calls it "a verbatim gloss": 230), `mediating_variable` (no `maxWords`: 232), `sources[].id/path` (no bound: 233), and a stub's `phrase` (234). `words()` counts `str.split()` tokens, and U+200B is not whitespace, so 44 visible words count as one (231) and one U+200B is a "non-empty" phrase (22, 328). `$description` and `$migration` are exempt keys with unvalidated content (82, 83).
6. **The schema is an unguarded loosening surface — P's "bite the bite" seen from the other side.** No sha pins it; the code's own node-level R3/R5 check is the only guard that does not read it (113 was caught for exactly that reason). Six loosenings pass `--check` (110, 111, 112, 310, 311, 312). Because [142] `--selftest` copies the (loosened) real home, five of them make an existing arm stop firing and the selftest goes red — **at the next build, ABORT; the seam runs `--check` alone, so the commit lands** (`assets/…/selftest-110-*.txt` … `selftest-312-*.txt`, `wave3.txt`). **310** (`sources[]` extra keys) overlaps no arm: `--check` green, `--selftest` 55/55 green — total.
7. **Six open edges on the closed directory.** Top-level dotfiles (210 — a literal authored `.edges.json`), dotfiles inside `_generated/` (211), a `.tmp` from an interrupted `--write` (212 — the writer's own temp name), anything under `schema/` (213 a literal authored edge list, 214 a second schema), `__pycache__` (216). A real subdirectory IS caught (215, `R4-STRAY-FILE`).
8. **Ten crashes are red without a name** (table above). The pattern: set-membership on `role`/`ref`/`type`/`id` runs *before* the schema verdict is read; `_source_row_text` joins a `None` path; `read_text` has no decode guard; two schema mutations reach code that assumes shape. Rc 1 everywhere, so nothing commits — but "a crash is not a fail": the build's GATE remedy and the seam's `fail` text both assert a name that is not there.
9. **Three misnamings**, all red: a bare-string link and a `null` type are `S-SCHEMA` not `R2-UNTYPED` (200, 201); a `null` role is `S-SCHEMA` not `S-ROLE` (42). The five ruled refusal names are promised in `x-refusals`; the most natural untyped link does not get one.
10. **Door asymmetries.** (D1) `POLARITY_BRAIN_DIR=/nowhere` → CLI 77 → `_build_all.main()` prints "COULD-NOT-ASK (exit 77) — declared refusal, build continues"; the seam blocks. The 77 verdict was built for shipped packs (P finding 11); in the source repo, a deleted `knowledge/brain/` is a mutation the build walks past. (D2) The seam line honours `POLARITY_BRAIN_DIR`; on a fake-repo stand-in whose `knowledge/brain/` carries a typed status, the block goes red with no env and **green** with `POLARITY_BRAIN_DIR=<clean copy>` — no "DECLARED GAP" line, the only trace is the gate's own `home /…/brain-real` line (`assets/…/door-asymmetry-seam-redirect.txt`). (D3) `.git/hooks` has no live hook: a raw `git commit` never meets the seam — class-wide for every gate in `_git_commit.sh`, named here because `s238-D7` says "every commit".
11. **Argv contradictions write.** `--add-polarity FILE --dry-run --write` writes the file; `--check --write` regenerates (`assets/…/wave4.txt`). `FLAGS` refuses unknown tokens (#208) but not contradictory known ones.
12. **The migration is a declared table; three of 21 links read differently to me, and the one row that moves the sort is licensed by an inference the printed rule does not describe.** `_migrate_tensions.py:159` says the links are "declared per row"; L1–L5 are labels. My reading (`assets/…/migration-diff.txt`): **tn-02** `explainedBy` (the same "IS / is exactly this trade" shape P typed `explainedBy` on tn-01; T read `resolvedBy` — three readings on one row); **tn-27** `touches` — "Dave already leans this way" is a lean, the touch says the rubric "must be split" (future), and `s234-D6` itself rules a path-taking gate with a provenance receipt, one instance of the lean, not the ranking-vs-judgement split; under this reading tn-27 re-opens and the sort is **6·3·21**; **tn-29** `resolvedBy` — the same verb ("adopt") on the same ruling (`s234-D3`) that P typed `resolvedBy` on tn-16; **tn-22** type agreed, but L1 reads "a ruling id cited in `how_it_resolves`" and `s217-D8` appears only in `apollo_touch` (P's own provenance field admits `how_it_resolves+apollo_touch`).
13. **The sort gap is explained and proven.** Obligation rows = {tn-15, 16, 19, 20, 25, 29}; the non-obligation rows whose `apollo_touch` names *any* ruling id = {tn-01, 02, 07, 08, 11, 14, 17, 22, 27} = 9 → **6·9·15 is exactly "every touch id closes"**, T finding 2's sensitivity figure. The typed reading closes {tn-07, 17, 22, 27} → 6·4·20; the five it leaves open are tn-01 (explainedBy), tn-02 (contested), tn-08 (the touch says the rule "does not" exist), tn-11 and tn-14 (challenges) — four clearly wrong to close, one contested, which is T's "four". `s238-D6`'s ruled text carries the naive figure in its parenthetical. Probe: `assets/…/sort-side-by-side.txt`.
14. **T's sort reproduces; determinism OK; live tree green; live selftest reproduces.** `_derive_sort.py` re-seated → whole-file equal to the filed `tension-sort.json`; gate vs T differ on tn-22 only. Two `--write`s (one creating `_generated/` from nothing) → three files byte-identical with the clock stripped and equal to the live tree. `--check` rc 0 in 0.096 s. `--selftest` on the live home: "arms 55 · red arms 45 (went red by name 45/45)".
15. **The register is unguarded** (observations, nothing ruled): a grade letter L→C on `pr-wcag-1-4-3` moves pl-15 out of settled-by-obligation with no refusal (301: 6·4·20 → 5·5·20); a statement rewrite passes (241); `$migration.sha256`/`from` are never checked (246, 247); all rows or all links can be wiped (244, 245); a symlink is read through (403).
16. **P's pitfall 9 is wrong in one clause.** "the tempdir is removed on every path" — the `shutil.rmtree` is not in a `finally`; `--selftest --brain <absent>` tracebacks and leaves `/dev/shm/polarity-selftest-*` (`assets/…/wave4.txt`; I removed the one it left).
17. **The selftest's superseded arm is hostage to the store.** It needs ≥1 `superseded_by` row (there is exactly one); if that row is ever tidied the arm reports "UNPROVEN, not passed" as a FAIL and [142] ABORTS the build.
18. **The writer's proof is half tautological.** `add_entry`'s reconstruction check compares `new_text[:at] + new_text[at+len(span):]` to `original` — true by construction, since `compose_append` built `new_text` as exactly that; the independent prefix/suffix proof exists only in selftest arm 46. The round-trip proof is real and caught a nested key named `polarities` under `$migration` (329, refused, untouched). A 2-space-indented file is accepted and left mixed-format (326).

## RULING-SHAPED QUESTIONS

⛔ **MANDATORY SECTION.** Nothing below is decided. Each is Dave's. Depth cap 1: these are the prices, not the fixes.

1. **What is "live" for R1?** (a) `superseded_by` only, as built; (b) also refuse a `resolvedBy` whose target's `status` text carries OPEN / PARKED / DEFERRED / "supersedes"; (c) the store carries a machine `state` field written only by `_inscribe_ruling.py`, and R1 reads that. Recommend **(c) as the permanent fix paired with (b) as the tactical one** (Dave #228: tactical + permanent PAIRED, owner named — the store's writer).
2. **Should the schema be pinned?** (a) leave it the consumer's grammar, unguarded, as built; (b) the gate pins its sha and a schema edit must move the pin in the same commit; (c) the five refusals' floors (`minItems 2`, the four types, `additionalProperties false` at every level, `maxWords 15`) live in code AND the gate refuses a schema that disagrees. Recommend **(c)** — it keeps P's "bite the bite" (the schema still drives the check) and closes the loosening class at the seam, not one build later.
3. **Close the quote oracle?** (a) as built; (b) `sources[].path` restricted to the frozen R1 register (or a ruled allow-list), and a `resolvedBy` without a *verified* quote refused; `touches` may stay quote-free. Recommend **(b)** — a `resolvedBy` moves the sort; an unreceipted one is a typed status by another door.
4. **Check the clock?** parse ISO-8601 UTC, refuse a future clock (skew ≤ 1 h) and one older than the R1 asset's date. Recommend yes — five lines.
5. **Bound and verify the free text.** `note` verbatim-checked like `quote` (the schema already says "verbatim gloss"); `mediating_variable` `maxWords` (25?); `sources[].id/path` patterned; `$description`/`$migration` shape-fixed; and every string refused if it carries a Cf-category character (closes 22, 231, 328 as a class). Recommend all five.
6. **Close the directory.** List dotfiles, list `schema/` contents (exactly one schema), refuse `*.tmp`, refuse `__pycache__` under the home. Recommend yes.
7. **Crash → named refusal.** A catch-all around `gate()` that names the exception class and the JSON path as `S-SHAPE`; decode as `utf-8` with a named `S-PARSE`; hash-guard the set memberships. Recommend yes — the seam and build text currently promise a name.
8. **The two hatches.** `_git_commit.sh` unsets `POLARITY_BRAIN_DIR` (or prints "— polarity gate: REDIRECTED to $POLARITY_BRAIN_DIR" as a declared line); and the build treats rc 77 as ABORT when `knowledge/` itself is present (source repo), COULD-NOT-ASK only when it is not (shipped pack). Recommend both.
9. **The four contested migration rows** — tn-02 (touches / explainedBy / resolvedBy), tn-27 (resolvedBy vs touches; re-opens the row), tn-29 (touches vs resolvedBy), tn-22 (the rule's letter). Dave's eye on four quotes; P's Q3/Q4 already hold two of them.
10. **`s238-D6`'s parenthetical carries the naive figure** ("moves the sort 6-3-21 to 6-9-15"). ADR-0017 freezes history; a `watch` note on the row via `_inscribe_ruling.py` is the conductor's call.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** whether the seam's `--check` on the WORKTREE can disagree with what the commit carries (staging order in `_git_commit.sh`; d0802-P5 stages explicit paths) — not driven, no git here. Price: one dry run at a seat that may run git, ~5 min.
- **UNPROVEN:** whether raw `git commit` is ever used in practice (no hook; the runbook mandates the script) — a process fact, not a repo fact. Price: Dave's word.
- **UNPROVEN:** CI's behaviour on rc 77 for [141] — read from `_build_all.py` lines 1352–1358, not driven. Price: the conductor's CI run.
- **UNPROVEN:** which of the four contested migration rows Dave would rule — his eye (Q9).
- **UNPROVEN:** that `jsonschema` (P's independent reader) would also accept 310's loosened schema — by construction it must (it reads the same file), not re-run. Price: one `_probe_independent.py` run on the mutant, ~1 min.
- **UNPROVEN:** the migration's other 17 links beyond my four disagreements are *right* — I agree with them, which is a second reading, not a proof. Price: none available; a third reader.
- **CLAIMED:** the fake-repo stand-in for D2 is faithful to the tree — the seam block is the verbatim extract and the helper modules are byte copies, but it is a stand-in. Re-read costs one run of `_wave3.py`.

## PITFALLS (consequences replayed, Dave #165 — owner per row)

| | risk | what is built against it | owner |
|---|---|---|---|
| 1 | "48 ESCAPED" read as 48 defects — 6 are UNRULED observations and 26 defeat promises rather than rulings | the grade column on every row; the RULED set is 16 and listed by number in `escaped-repro.txt` | conductor's stub |
| 2 | The wave scripts hardcode `REPO` and `V` for this seat (lane T finding 11 class) | both constants sit at the top of `_v_attack.py`; nothing else is seat-bound | whoever re-runs |
| 3 | The arms left ~30 MB of copies under `/sessions/…/outputs/v238/` and the mount refuses `rm` (graveyard dirs accumulate) | scratch, outside the repo; `_graveyard/` is the declared dumping ground | sandbox hygiene |
| 4 | The `doors/` transcripts are elided (boilerplate RULE lines) and CAUGHT arms are 4-line stubs — because the mount refuses deletes and the full set was 1.2 MB | every elision is marked in the file; `live-check.txt` carries the RULE lines once; the scripts regenerate everything in ~1 min | reader |
| 5 | My reading of the four link types uses the schema's seated semantics; if P's Q1 re-words two of them, tn-02/tn-29 move | the diff quotes the semantics it used at its head | Dave / P Q1 |
| 6 | The harness drives the seam block with `POLARITY_BRAIN_DIR` set on every arm — the very hatch D2 names | the arms prove `gate()` through the door; D2 proves the door itself on a stand-in with no env | reader |
| 7 | `--selftest` was run 7 times, once on the LIVE home — it copies to `/dev/shm` and removes them on the rc-0 path; the crash-path probe left one dir | removed in the same call; finding 16 records the class | me (done) |
| 8 | A fix lane that closes the RULED 16 one by one will re-open this class (Dave #215: "real fixes never patches") | Q1–Q8 are written as classes, not rows; Q2 and Q5 each close a whole column of the table | the fix lane's brief |

## Evidence

`notes/_subreports/assets/2026-09-02-238-V-polarity-verifier/` —
`_v_attack.py` (the harness: three doors + write door, verdict rules in the docstring) · `_wave1.py` … `_wave4.py` (every arm as code; re-seat two constants and re-run) · `_seam_block.sh` (the seam block as extracted and wrapped) · `wave1.txt` … `wave4.txt` (the verdict tables) · `TOTALS.txt` (counts and door-agreement, computed from the JSON dumps) · `escaped-repro.txt` (the 48 ESCAPED rows, graded, each with a standalone command) · `doors/` (108 per-arm transcripts: full for ESCAPED / CRASH / MISNAMED / green / writer arms, 4-line stubs for CAUGHT, RULE lines elided everywhere — declared) · `migration-diff.txt` (task 3, 21 links row by row) · `sort-side-by-side.txt` + `derive-sort-rerun-this-seat.txt` + `_derive_sort_reseated.py` (task 4) · `determinism.txt` + `determinism-det{1,2}-write.txt` · `live-check.txt` · `live-selftest.txt` · `selftest-110…312-*.txt` (the build's [142] on the six accepted schema mutants: five red one build later, 310 green) · `door-asymmetry-77.txt` · `door-asymmetry-seam-redirect.txt`.

REPLAY-THESE: `assets/…/escaped-repro.txt` (~3.5K — the 48 rows graded, RULED 16 first; the only place the whole set stands with commands) · findings 2, 4, 6 (~0.9K — the three structural classes: one-field "live", the self-named oracle, the unpinned schema) · finding 12 + `assets/…/migration-diff.txt` rows tn-22 and tn-27 (~0.6K — the rule-letter gap on the sort-moving row, and the row that re-opens) · finding 10 D2 + `assets/…/door-asymmetry-seam-redirect.txt` (~0.4K — the silent hatch) · RULING-SHAPED Q1, Q2, Q3 (~0.5K — the three that shape the fix lane) · the CRASH table (~0.4K — ten inputs, line numbers)
