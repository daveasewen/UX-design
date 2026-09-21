# 293 · J4 — can a Jev re-rank fix Memento retrieval? Measured: no lift at n = 14.

**Verdict: FLAT. Do not wire it on this evidence.** Fourteen real queries, one live
request each, MRR 0.173 → 0.187, hits@1 1/14 → 1/14, hits@3 3/14 → 2/14. Four rows
improved, four degraded, three unchanged, three unmovable. At n = 14 one query is worth
~0.07 of MRR, so the whole delta is smaller than one row. **And the headline finding is
not about the re-ranker at all: for 4 of 14 real queries the record the session actually
fetched was never on the shortlist** — Jev cannot rescue what lexical never surfaced.

Full table, aggregate, exact request JSON, score distribution:
`notes/_lanes/293/J4/rerank-results.md`. Fixture: `notes/_lanes/293/J4/fixture.jsonl`.
Script: `notes/_lanes/293/J4/rerank.py` (measuring instrument — nothing imports it,
nothing should).

## 1. Where the fixture came from — Dave gave none, so it is transcript-mined

**Stated first because it bounds everything below.** Dave supplied no queries. The brief's
first source, the session transcripts under `.claude/projects/session/`, yielded **zero**
usable pairs: the only `_memento_search.py` strings in this session's transcripts are
echoes of the module's own docstring from reading the file, not invocations. So the
fixture comes from the repo's own record of real invocations:

**`consult-receipts` strata.** `_search_core.py` defines the line format
(`> **consult-receipts #N:** "query" → id · id`) and `_capture_gate.py::consult_receipt_probe`
enforces it. 357 such lines exist across `notes/_GAUGE-LOG.md`, `_GM-ARCHIVE.md`,
`GOOD-MORNING.md` and lane strata; 63 carry a payload rather than an honest negative. Each
is a real session writing down the query it typed and the records it got.

Ground truth was taken in two grades, recorded per row in `provenance`:

- **10 rows — fetch-backed.** The receipt explicitly says the session `--fetch`ed that
  record (`"(fetched)"`, `"(fetched verbatim)"`, `--fetch <id>`). This is the brief's
  "the record the session ended up fetching right after", as close as this repo records it.
  Three of these receipts elide the id (`ledger:93-…`); the id was resolved by unique
  prefix against `knowledge/_memento-index.json` and the resolution is noted in the row.
- **4 rows — sole-id.** The receipt returned exactly one record for that query and no
  other. Weaker: it is what the door surfaced, not provably what was read.

One row was mined and then **excluded from scoring**: `"trigger index"`
(`notes/_GAUGE-LOG.md:794`), **documented miss #1** — the ds-021 / #80 / #81 failure the
trigger-index README in `knowledge/_rulings.json` `_README` records. The receipt is
explicit that the query "returned THIS WEEK'S BANNERS and not one of the ten homes of the
ruling it was about". It is kept in the fixture with `correct_id: null` because **a
re-rank cannot touch it**: the right answer (the trigger index itself) is not a record in
the memento corpus at all, so no candidate could ever carry it. Same for
`"ds-021 ds-022 ds-023 throttle dual unit mover fold stop line"` (#34) — its receipt says
the ledger's ds- entries were not indexed and needed `awk`. Those two misses are a
**corpus** defect, not a **ranking** defect, and re-ranking is the wrong instrument for
them. That is a finding, not a gap in this lane.

One slug moved since its receipt was written: `band table amber threshold remaining
budget` → the receipt's `runbook:context-gauge:…-and-this-is-the-only-cop`, re-pinned to
the current index's `…-gm-d9`. Same record, same pin `_memento_search.py::SELFTEST_CASES`
carries.

## 2. Commands (redacted — the key is never printed, quoted or logged)

```
grep -h "_memento_search.py" .claude/projects/session/*.jsonl \
     .claude/projects/session/*/subagents/*.jsonl      # 18 hits, all docstring echoes, 0 real queries
python3 -  # mine `consult-receipts` payloads from **/*.md, validate ids against _memento-index.json
python3 notes/_lanes/293/J4/rerank.py --dry            # lexical baseline, door-display order, no network
python3 notes/_lanes/293/J4/rerank.py --dry --global   # lexical baseline, caps off, no network
python3 notes/_lanes/293/J4/rerank.py                  # LIVE: 14 requests, one per query
```

The key lives in `.env.local` and is handled only by `knowledge/_jev.py`. All fourteen
calls appended receipts to `knowledge/_jev-receipts.jsonl` with request ids, questions as
sent, answers as returned and measured latency. No file outside
`notes/_lanes/293/J4/` and `notes/_subreports/` was created or modified; the receipts file
is appended by the adapter itself.

## 3. The design, and where it departs from the cookbook

The rerank cookbook (`docs.typesafe.ai/cookbooks/rerank_typesafe.md`) runs **one Noul per
(query, candidate) pair** — 30 requests per query on CLERC — and closes by saying a real
application would ask several questions about one pair in a single call. This lane's live
budget is **one request per query**, so the 20 candidates became **20 parallel Score
questions in one request**, which `docs.typesafe.ai/primitives/score.md` confirms are
evaluated independently for a few extra question tokens. Score rather than Noul because
the brief specified the 4-level ladder.

**The J3 lesson held:** `state` is the real evidence. Memento candidates are already text,
so nothing was described — `state = {query, candidates:[{i, text≤600}]}`, the record body
itself. That is the advantage J3 lost to `html_to_state`, and it was kept here. The cost
is truncation: 266 of the 280 candidates were cut at 600 chars, counted per row in the
table, never silent.

## 4. What this does NOT prove

- **The fixture is transcript-mined, not Dave-given.** Every query is real, but the
  "correct" answer is what a session named in its receipt. On `ds-018` Jev's new rank-1,
  `ledger:121-2026-08-07-ds-018-ruled-enacted-s121-d1`, is arguably a BETTER answer than
  the receipt's `gm:C2` banner — and the metric scores it as a 5-place degradation.
  At least one of fourteen rows punishes the re-ranker for possibly being right.
- **n = 14. Confidence is low and is stated as low.** The cookbook's own result used 40
  queries, and its lift (5% → 18% top-1) is the scale of effect this fixture is too small
  to resolve either way.
- **The candidate cap is 20 and the text cap is 600 chars.** A longer window, or the
  cookbook's one-request-per-pair isolation, was not tested. All 20 candidates shared one
  `state`, which the cookbook's design deliberately avoids; whether that helps or hurts is
  unmeasured.
- **"Rank" had to be invented.** The door prints per-bucket capped groups and has no
  single ranked list. Two baselines were measured — the door's display order (headline)
  and a caps-off global flatten — and they disagree sharply (4 vs 8 absent correct ids).
  A production re-rank would have to decide which order it is re-ranking, and that
  decision is not made here.
- **Nothing about accuracy in general.** Fourteen Score ladders on one corpus, one day,
  one model version (`jev-1.13.0`). No repeat runs, so answer stability is unmeasured.

## 5. PROPOSAL ONLY — how a re-rank could sit behind a flag. Not a change.

**For the conductor to rule. `knowledge/_memento_search.py` was not touched by this lane
and must not be touched on this evidence.** If it is ever ruled in, the shape that fits
the existing contracts is:

`_memento_search.py` gains one opt-in flag, `--rerank`, default OFF, and nothing else
changes. On the flag: after `search()` returns its buckets, the door branches on
`_jev.available()` **first** — no key, no route, `JevUnavailable` ⇒ print exactly what it
prints today and say in one line that the oracle was absent. That is the oracle rule from
`_jev.py`, and it is the whole reason the flag can be safe: an absent oracle must degrade
to today's behaviour, never to an error and never to an empty result. On success the door
re-orders the ALREADY-CAPPED display rows and prints the Jev score beside each id, so the
reader can see what moved and why; the pre-rank position stays printed next to it. The
re-rank must never change bucket membership, never change `totals`, and never change what
`--fetch` resolves — the same absolute constraint `_decorate_edges` already lives under
(`#115`: decorate only ADDS keys, never touches `_score`). Cost is one request, ~7.3K
input tokens and ~0.9 s per query, which is a real tax on a cold session's first lookup
and is the reason the flag is off by default.

**But the measurement argues against building it yet.** The two documented misses this
lane went looking for — `"trigger index"` and the ds-021 ledger entries — are records the
corpus did not hold or did not index. Four more of the fourteen queries failed the same
way: the right record was never on the shortlist. **A re-ranker cannot add a candidate.**
On this evidence the cheaper and better-aimed work is on RECALL — what the index holds and
what the lexicon expands — not on the order of what lexical already found. If a re-rank
is revisited, it should be after a fixture of 40+ pairs exists and after the shortlist is
shown to contain the right answer most of the time, which is the precondition the cookbook
itself operates under (100% of its golds were in the top 30).
