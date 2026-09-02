# #239 — LANE F: FIX the polarity gate against V's 48 escapes, then re-drive V's harness as the exit gate

Read `notes/_briefs/2026-09-02-239-COMMON-lane-rules.md` first (it points at #238's COMMON — read that too). Then, in this order:
1. `notes/_subreports/2026-09-02-238-V-polarity-verifier.md` — ALL sections, especially ESCAPED, CRASH/MISNAMED, RULING-SHAPED Q1–Q10, PITFALLS row 8.
2. `notes/_subreports/assets/2026-09-02-238-V-polarity-verifier/escaped-repro.txt` (90 lines) — **this is the proof standard**, not P's arm table.
3. `notes/_subreports/2026-09-02-238-P-polarity-gate.md` + `notes/_briefs/2026-09-02-238-P-polarity-gate-brief.md` — what the builder claims and why.
4. Rulings `s238-D1`, `D3`, `D5`, `D6`, `D7` from `knowledge/_rulings.json` (probe in #238 COMMON).
5. The code: `knowledge/_validate_polarities.py`, `knowledge/brain/` (`polarities.json`, `stubs.json`, `schema/`, `_generated/`), the `POLARITY GATE — s238-D7` block in `knowledge/_git_commit.sh`, and steps 141/142 in `knowledge/_build_all.py` (read the step FUNCTIONS; never run the whole build).

## THE JOB
Make every one of V's 48 ESCAPED rows a NAMED refusal (rc≠0, nothing written) at ALL THREE doors — `--check`/`--write` CLI, the `_build_all.py` step function, the `_git_commit.sh` seam block — and turn the 10 CRASH rows into named refusals and the 3 MISNAMED into correctly named ones. Order: **RULED 16 first**, then PROMISED 26, then CRASH 10 + MISNAMED 3, then UNRULED 6 (see DO-NOT-RULE).

**Fix by CLASS, not by row** (V pitfall 8; Dave #215 "real fixes never patches"). V's Q1–Q8 are already written as classes. Take V's RECOMMENDED answer on each as the DERIVED DEFAULT — the conservative side, per `s238-D3`/`s238-D5` — and declare every default you took in the report:
- **Q1 (what is "live" for R1):** build **(b)** now — a `resolvedBy` whose target ruling's status text carries OPEN / PARKED / DEFERRED / FORKED / "supersedes" is refused. **(c)** (a machine `state` field via `_inscribe_ruling.py`) is NOT yours — it touches the store's only writer; float it as a priced proposal.
- **Q2 (schema pinned):** build **(c)** — the five refusals' floors (`minItems 2`, the four link types, `additionalProperties false` at every level, `maxWords 15`) live in code AND the gate refuses a schema that loosens any of them. Add **(b)** the sha pin only if it costs under 20 lines; otherwise float it.
- **Q3 (quote oracle):** **(b)** — `sources[].path` restricted to the frozen R1 register or a ruled allow-list; a `resolvedBy` without a VERIFIED quote is refused; `touches` may stay quote-free.
- **Q4 (clock):** yes — ISO-8601 UTC, refuse a future clock (skew ≤ 1 h) and one older than the R1 asset's date.
- **Q5 (free text):** yes — `note` verbatim-checked like `quote`; `mediating_variable` `maxWords 25` (FLOATED figure — declare it); `sources[].id/path` patterned; every string refused if it carries a Cf-category character (closes 22, 231, 328 as a class).
- **Q6 (directory):** yes — list dotfiles, list `schema/` contents (exactly one schema), refuse `*.tmp`, refuse `__pycache__` under the home.
- **Q7 (crash → named refusal):** yes — a catch-all around `gate()` naming the exception class and JSON path as `S-SHAPE`; decode `utf-8` with a named `S-PARSE`; hash-guard the set memberships. A crash is not a fail — it must become one, by name.
- **Q8 (the two hatches):** both — the seam unsets `POLARITY_BRAIN_DIR` OR prints a DECLARED `— polarity gate: REDIRECTED to …` line; the build treats rc 77 as ABORT when `knowledge/` is present, COULD-NOT-ASK only when it is not.

For every class fix, ADD arms to `--selftest` so the builder's own test covers what V found — but the self-test is NOT the proof (it proves the clause). The proof is below.

## EXIT GATE — V's harness, re-driven (Dave: "do both")
On copies under `/sessions/keen-serene-johnson/mnt/outputs/f239/`, re-run V's own instruments unchanged except for the two seat constants at the top of `_v_attack.py` (V pitfall 2): `_v_attack.py`, `_wave1.py` … `_wave4.py`, `_seam_block.sh` from `notes/_subreports/assets/2026-09-02-238-V-polarity-verifier/`. **Copy them to your assets dir first; the originals are dated history — never edit them.** Then:
- every row in `escaped-repro.txt` → CAUGHT, by name, at all three doors (paste each standalone command's new output into `assets/…/escaped-now-caught.txt`, same 90-line order);
- CRASH 10 → named refusals; MISNAMED 3 → the right name;
- V's 7 green controls still GREEN; live `--check` on the real tree GREEN; the three derived views still byte-deterministic (V's determinism probe);
- P's `--selftest` green with your new arms counted;
- `bash knowledge/_git_commit.sh --selftest` still passes its 14 bites (you may run the SELFTEST; you may not commit);
- `python3 knowledge/_validate_wiring.py` — report its verdict; its pre-existing red on `_validate_receipt.py` (P finding 14) is OUT OF SCOPE, do not fix it, name it.
A row that still escapes is reported as ESCAPED with its command, never smoothed.

## DO-NOT-RULE (Dave's; report, never decide)
- **Q9** the four contested migration rows (tn-02, tn-27, tn-29, tn-22) and the sort (6·4·20 vs 6·3·21 vs 6·9·15) — touch NO row in `polarities.json` beyond what a class fix forces, and if a class fix forces one, STOP and report it as ruling-shaped instead.
- **Q10** the `watch` note on `s238-D6` — conductor's.
- **Q1 (c)** the machine `state` field in the store.
- The **UNRULED 6** — fix only where a class fix above catches them for free; otherwise list each with a proposed default and its price.
- The four ask-whens, the 20 open polarities' conservative side, pl-02 / pl-29, P's Q1/Q2/Q6 — all carried, none yours.
- Any constant, band, floor, or roster; any file outside `knowledge/_validate_polarities.py`, `knowledge/brain/schema/`, `knowledge/brain/_generated/` (regenerated only by `--write`), the seam block in `_git_commit.sh`, steps 141/142 in `_build_all.py`, and your report + assets. If a fix needs another file, STOP and report the price.

## COUNTS (report grammar, same as V's so the two files diff)
**attacks n · caught n · ESCAPED n (RULED n · PROMISED n · UNRULED n) · CRASH n · MISNAMED n · green controls n/7 · live --check green/red · determinism ok/fail · selftest arms n (red n/n) · new arms n · commit-script selftest n/14 · wiring verdict · UNPROVEN n.** Then a **BEFORE → AFTER** line: `48 → n ESCAPED · 10 → n CRASH · 3 → n MISNAMED`.

## FILING
`X = F`, slug `polarity-fix`. Report sections per `_TEMPLATE.md` plus: **DEFAULTS TAKEN** (every Q1–Q8 choice, the side it bent to, one line each — `s238-D5`), **STILL ESCAPING** (if any, with commands), **RULING-SHAPED** (Q9/Q10/Q1c + anything a class fix forced you to stop on), **PITFALLS** (owner per row), **REPLAY-THESE** (≤7 lines, sized). Stub back to chat ≤12 lines: report path · the BEFORE → AFTER line · COUNTS · REPLAY-THESE · UNPROVEN list · files touched (paths only).
