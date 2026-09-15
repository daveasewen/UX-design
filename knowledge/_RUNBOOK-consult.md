# Runbook — consult (the read-side query tool)

STANDING: run `python3 knowledge/_consult.py "<your question>"` before designing anything —
paste the receipt (query + retrieved record ids) into the work's review sheet or meta.

*(This doc must be reachable from `GOOD-MORNING.md` for the standing-instructions reachability
gate to see it — that wiring is the parent session's job, not this one's; see the build note
at the bottom.)*

## What this is

The knowledge base is superbly ID'd — 465 rules, T-D/R-D/DV-D rulings, ASSERT-00x, DEF-00x,
ADRs, gates — but until now it lived in nine-plus stores with grep as the only join. A rule
that is written, correct and unretrieved is indistinguishable from one that does not exist.
`_consult.py` is the query surface: "what governs X?", answered in one step, with an
enforcement column (gated vs asserted-only) so the gate-glob-coverage question is answered
per-query instead of as a separate audit campaign.

Full design intent: `reviews/CONSOLIDATION-AUDIT-2026-07-18.html` §3.

## The two files

- `knowledge/_build_consult_index.py` — generator. Reads the rules index, the three
  `_proforma/*-DECISIONS.md` ledgers, `_assertions.json`, every `_validate_*.py` gate,
  `docs/decisions/ADR-*.md`, `_DS-IMPROVEMENTS.md` + `_ICON-GAPS.md`, and `_LIVE-STATE.md`'s
  `## OPEN` section. Writes `knowledge/_consult-index.json`. Wired into `_build_all.py` as a
  generator step — it reruns on every build, so the index cannot silently go stale.
- `knowledge/_consult.py` — the query. Tokenises the question, expands it through the lexicon,
  keyword-matches over every indexed record, and prints ranked results grouped as: rulings,
  blocking rules, advisory rules, assertions, open items, gates. Every rule result carries an
  enforcement line — `gated by <script> over <bite>` (or `possibly gated by...` on a fuzzy
  match) or `asserted only — no gate bites`.

## Usage

```
python3 knowledge/_consult.py "amber indicator on white"      # ranked answer, one screen
python3 knowledge/_consult.py "amber indicator on white" --all    # no per-section cap
python3 knowledge/_consult.py "amber indicator on white" --json   # machine-readable
python3 knowledge/_consult.py --selftest                          # regression check, exits 1 on miss
```

## The pre-flight protocol

Before designing a solution to a problem in this repo's domain — a colour choice, a spacing
rule, a type decision, an accessibility question — **run a consult first.** Several 07-18
failures (the ochre glyph, the 49-file inline-fonts sweep, "no Univers in-sandbox") were the
same shape: a problem the system had already answered, solved again from scratch because
nothing made the existing answer askable. Paste the receipt — the query string and the
retrieved record ids — into the work's review sheet or meta. This makes "did you check first"
a one-line, checkable fact instead of a trust exercise.

## Tier: advisory, for now

This enters at the **advisory tier** (AGENTS principle 5) — it does not fail any build today.
The promotion path to blocking is a presence-check gate (a validate-consult script, not yet built: new/changed
review sheets and metas must carry a consult receipt) once the tool has earned trust by being
bite-tested in real use. Do not build that gate pre-emptively; earn it first.

## The lexicon — grow on miss

`knowledge/_consult-lexicon.json` is hand-authored, not generated, and deliberately seeded
rather than exhaustive (~30 entries at build time). People ask questions in their own words
("ochre", "padding", "bold", "colour-blind", "storybook"); the index carries the KB's own
vocabulary ("amber", "gap", "weight", "CVD", "catalog"). When a real query returns nothing
useful because the asker's word doesn't match the KB's word, **add one line to the lexicon
and move on** — this is the intended maintenance model, not a gap to eventually close with a
bigger seed list. Curation is part of the job.

## The selftest — what "working" means

`--selftest` replays three known-answer regression queries and exits 1 if any expected record
id is missing from the results:

| query | must surface |
|---|---|
| `amber glyph contrast white` | `R-D3` (the amber ruling, `_RAG-DECISIONS.md`) and `avd-001` (VD-1 — colour is never the only carrier of meaning, SC 1.4.1 A; chosen as the "1.4.1 / colour alone / waiver" rule — see the build note in the delivering session's report for why this id and not another candidate such as `icon-013`) |
| `inline fonts portability` | `T-D9` (binding mechanism ruling — the delivery/link-not-inlining consequence lives in its body) |
| `univers sandbox render` | `ASSERT-002` and `ASSERT-006` (the desktop-Univers-present assertions) |

Run it after touching the lexicon, the ranking logic, or any of the source files the index
generator reads. It is wired into `_build_all.py` as an advisory step — it reports but does
not fail the full build (promotion to blocking follows the same path as the tool itself).

## Build wiring

`_build_consult_index.py` runs as a generator step in `_build_all.py` (rebuilds the index
every time). `_consult.py --selftest` runs immediately after as an advisory step (reports,
does not abort the build). See `_build_all.py`'s `STEPS` list for the exact position.

## O2′ (#25, ruled 2026-07-28) — the spine split: ONE engine, TWO doors

Dave's direction (ledger `notes/_MEMENTO-DECISIONS.md` § Memento-before-Apollo, enacted #25,
option-select ×3 all recommended): the search functionality is MODULAR — a core engine plus
corpus doors, two-stage retrieval throughout.

- `knowledge/_search_core.py` — the engine: matching, ranking, honest denominators, the
  two-stage fetch contract, and the `consult-receipts` line format (one copy; the wrap
  probe imports it). `--selftest` bites.
- `knowledge/_consult.py` — the DS door (this runbook's original subject). Interface
  unchanged, plus **`--fetch <id>`** (stage 2: the full record verbatim — retires the
  140-char truncation) and honest group headers (`5 of 41 shown`, never the cap as the
  denominator).
- `knowledge/_memento_search.py` — the Memento door: GM/LS sections · both archives ·
  the Memento ledger · gauge blocks · briefs · dream proposals · the memento runbooks ·
  lane records. Index `_memento-index.json` via `_build_memento_index.py` (regenerates
  every build; closed contracts REFUSE unknown structure, ds-016 class; archives are
  deliberately OPEN-form — moved content carries arbitrary headings, measured #25).
  Same lexicon file as the DS door — one curation point.

  ⛔ **AND THE INDEX THE QUOTE GATE SEARCHES COVERS NEITHER `notes/_lanes/` NOR THE `says`
  FIELD OF `knowledge/_rulings.json` — SO A 0 FROM `knowledge/_quote_gate.py` IS A STATEMENT
  ABOUT THE INDEX, NEVER ABOUT THE QUOTE.** *(Homed here BY ADDITION at the #276 wrap's 2f
  EXIT CHECK, from the lesson the #275 stratum carried into an append-only dated home before
  it rolled; measured four wraps running — #273 **0/13**, #274 **0/9**, #275 **2/4**, #276
  **see this session's stratum** — which is what makes it a class and not an anecdote.
  provenance: 276 · 2026-09-15 · status: observed.)* Dave's words arrive in a lane file
  (`notes/_lanes/<N>/DAVE-RULINGS-<date>.md`) and are inscribed into a ruling's `says`, and
  `_build_memento_index.py` reads neither surface. ⇒ **When the gate returns 0, verify the
  sentence as an EXACT SUBSTRING of the lane file and SAY WHICH FILE you checked** — never
  present the 0 as a refusal of the quote, and never drop the check silently.
  ⚠ **Widening the index to cover those two surfaces is UNBUILT AND UNRULED**, priced at one
  lane; it is Dave's call, and until he takes it the verification above is held by hand.

**Two-stage protocol (the ruled shape):** stage 1 returns REFS (ids + one-line heads +
file:line) — cheap to read; stage 2 `--fetch <id>` prints the record VERBATIM. Spend
tokens on the records you need, not on the corpus.

**Consult receipts (the KG forcing function, #25):** the wrap stratum carries a
`consult-receipts` line — the window's queries with their retrieved ids, or the honest
negative `none — <why>`. FORM-checked by `_capture_gate.py::consult_receipt_probe`,
ADVISORY at birth; promotion to BLOCKING is Dave's word. Ritual runbook step 2f has the
one-line contract.

## n-gram doors (#269, 2026-09-13) — ADVISORY, read-only, NOT in the pack

Research `_RESEARCH-ngram-lookups-2026-09-13-v1.html`; Dave's word *"as long as it's safe and
you test the usual dependencies and externalities lets go for it"*. Three files, all in
`knowledge/`, none shipped (`_search_core.py` / `_memento_search.py` are pinned byte-identical
to the memento-package by `_validate_package_delta.py`, so nothing here touches them):

- `knowledge/_ngram.py` — the library: word bigrams (`phrase_score`), character-trigram
  vocabulary (`Vocabulary.nearest` — "ratifed" → "ratified"), word shingles + Jaccard.
  `--selftest` bites (11).
- `knowledge/_quote_gate.py "<phrase>"` — **are these his words, verbatim?** FOUND with
  id · file:line, or NOT FOUND with the nearest real phrase (longest run of words in common)
  and a *did you mean* for any word the record has never used. `--file <page>` checks every
  quoted span of 4+ words in a page. Marker `QUOTE-GATE ADVISORY`; exit 0 unless `--strict`.
  Probed at birth: *"six month project…"* 0 hits, *"6 month project…"* 2 — the paraphrase
  the gate exists to catch.
- `knowledge/_near_dupes.py` — **which records say the same thing twice?** 8-word shingle
  overlap over the archive kinds (+ briefs, dreams); pairs ≥ 0.5 Jaccard, best first, as
  candidates for the dream pass. At birth: 22 pairs, one at 1.00 (a GM-archive section
  archived twice, `_GM-ARCHIVE.md:4940` and `:6133`).

⛔ **Open, Dave's:** (1) whether the quote gate becomes a STEP in the capture ritual (today it
is a door anyone may call); (2) phrase-aware RANKING inside `_memento_search.py` — a pack
change, therefore a release; (3) `_quote_gate.py` cannot see the memory hooks
(`memory/*.md` are not indexed) — *"keep them if they are cheap"* is a miss for that reason.
