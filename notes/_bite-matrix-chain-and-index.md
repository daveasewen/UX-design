provenance: #63 conductor, in-window · status: DRAFT — not ratified
evidence: mutations run live this session (#63, 2026-07-31) during the CI-survey wiring; quoted verbatim below

# Bite matrix — `_gen_chain.py` + `_build_memento_index.py` (gates 2 and 3 of 5, DO-FIRST 10)

Format per DO-FIRST 10: CLAIMS · BITES · MUTATION-RED · CANNOT-SEE. These two are built
in-window rather than by sub because their decisive mutations were already run and quoted
today while wiring CI (`816f726`) — a sub would have re-proven the proven.

---

## Gate 2 — `knowledge/_gen_chain.py` (391 lines; enumerated from source this session)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 1 | `_capture_gate` import failure → refuse with reason, chain NOT generated (l.151-154) | none (pragma: no cover) | UNPROVEN — would require breaking the sibling module on the live tree | — |
| 2 | Degraded instrument (tiktoken absent/estimate fallback) → MEASUREMENT REFUSAL, distinct from STALE and MISSING, before any measuring (l.156-166) | selftest #59 bites: "--check on a degraded instrument still exits non-zero" (l.347) + post-refusal tree untouched (l.361) | **PROVEN LIVE #63** — fresh sandbox pre-`pip install tiktoken`, clean tree: `✗ _CHAIN.md check FAILED — the token measurer is running on the ESTIMATE fallback, not the real tiktoken encoder…` (survey [70], exit 1). After install, same tree: `1 pass · 0 FAIL`. | Gates tiktoken PRESENCE; a present-but-wrong encoding (drift in cl100k itself) would measure confidently. |
| 3 | GOOD-MORNING.md missing → refuse (l.168-170) | selftest "--check FAILS when the file is missing entirely" (l.369) | — | — |
| 4 | Banner/parse failure (`chain_parts` returns None) → refuse, never a confident blank (l.175-177) | selftest "no ★ LATEST banner ⇒ REFUSE, never emit a confident blank" (l.370) | — | Refusal fires on parse FAILURE; a banner that parses but was written wrong (false content, right shape) flows through faithfully. |
| 5 | Every published figure MEASURED, never counted (l.185-187); footer figure must reach a fixed point; 2-cycle oscillation → REFUSE both ends (l.207-216); non-settling in MAX passes → refuse (l.218-219) | none in shipped selftest for the oscillation arm | UNPROVEN — forcing a 2-cycle needs a footer whose rendered width flips with the figure; not constructible without editing the module | A converged stamp proves the file self-measures truly, not that the SLICE is the intended slice — banner selection is `chain_parts`' contract, unexamined here. |
| 6 | `write()` refuses to write anything on build refusal (l.222-226) | covered via claim-2 selftest (tree untouched after refusal, l.361) | — | — |
| 7 | `check()` compares CONTENT, never mtime (l.239-246); MISSING file → red (l.252-253); STALE file → red with the cold-session-reads-a-previous-record wording (l.257-261) | selftest "--check FAILS on a hand-edited file (the stale-record class)" (l.367) | **PROVEN LIVE #63** — one-word typo hand-edited into `_CHAIN.md`, clean tree otherwise: `❌ [70] read chain determinism check — stale _CHAIN.md serves a PREVIO… exit 1` → `SURVEY: 0 pass · 1 FAIL`. Reverted; control re-green. | **Fresh ≠ true.** The check proves disk byte-matches what GM/LS generate NOW; garbage in GM yields a faithfully fresh chain of garbage. And run AFTER `write()` in the same pass it can never fail — the #60-D4 tautology, now closed at the CI seam by `816f726` (survey asks [70] before the build), still open for any local build-then-check run. |

## Gate 3 — `knowledge/_build_memento_index.py` (466 lines; contract tiers enumerated from source)

| # | CLAIMS | BITES | MUTATION-RED | CANNOT-SEE |
|---|---|---|---|---|
| 1 | Closed forms REFUSE on the unknown, never enumerate-and-skip (l.11-17): malformed `#### ` in the gauge log refuses (l.204) | selftest "gauge: malformed `#### ` REFUSES" (l.323) + "near-miss META spelling STILL REFUSES" (l.349) | — | Closed-contract refusal is per DECLARED file; a new source file added to the corpus but never declared is invisible, not refused (presence of sources is the build list's contract, not this parser's). |
| 2 | Zero gauge blocks / zero records from a source class / glob matching zero files → refuse, never index around a hole (l.208, 256, 290) | selftest l.327 ("zero blocks REFUSES"), l.355 ("META-only file REFUSES"), l.370 ("missing declared source REFUSES") | — | — |
| 3 | Open forms (archive `## ` headings) split but never refuse on heading content (l.358-363) | selftest "archive: open split — moved `## ` headings become records, no refusal" (l.363) | — | By design nothing validates moved-content headings — a mangled archive heading indexes as a mangled record, silently. |
| 4 | Deterministic output: collision suffixing + slugs stable (l.373, 375) | selftest both lines | — | — |
| 5 | `--check`: determinism check, content-compare against the committed JSON (O2′ #25; usage l.43) — a stale committed index goes red | none needed beyond the shipped determinism bites (l.307-375 suite green in CI) | **PROVEN LIVE #63** — single whitespace injected into `knowledge/_memento-index.json`: `❌ [66] memento index determinism check (O2′ #25) exit 1` → `SURVEY: 0 pass · 1 FAIL`. Restored from backup; tree byte-clean after. | Same tautology class as the chain: [65] regenerates, [66] checks — inside one `_build_all.py` pass [66] cannot fail (#60-D4, located to `:160-161`). Closed at the CI seam by `816f726`; still open locally. ⚠ Scope note, declared: the `--check` implementation body (beyond l.375) was not line-enumerated this pass — its bite is proven by mutation, its internals are cited from the O2′ pattern, not read. |

---

## Standing findings across gates 2+3

- **Both decisive staleness checks now run against the COMMITTED tree in CI before any
  regeneration** (`816f726`) — the #60-D4 seam is closed where it bit. Local
  build-then-check remains tautological by construction; the survey (`--range`) is the
  local method.
- **Fresh ≠ true, twice over:** both gates verify derived-artifact consistency with
  sources, never source truth. A false banner or mangled archive heading propagates
  with full gate blessing. The gates upstream of the record (capture gate, gate 4) are
  where truth-shaped checks live — which is why its matrix is next.
