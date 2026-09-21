# 293 · J4 — Jev re-rank over the Memento door: results

**14 live requests, no retries fired, budget 15.** Model requested `jev-latest`; model
answered `jev-1.13.0` on all fourteen. Fixture: `fixture.jsonl` (15 rows, 14 scoreable),
mined from `consult-receipts` lines in the repo's own gauge log and GM archive — **Dave
gave no queries; every one of these is a query a real session actually typed**, and the
correct id is the record that session named as fetched (or the sole id its receipt
returned). Provenance per row is in the fixture.

## What "rank" means here — read this before the table

`_memento_search.py` has **no single ranked list**. It prints per-bucket groups (lane
records, GM sections, ledger sections, …), each capped separately by `DEFAULT_CAP`. So
"rank" had to be defined, and it is defined two ways, both measured:

- **door-display** (the headline): the order a session actually reads — the door's own
  capped output, buckets concatenated in `KIND_ORDER`, first 20 rows. This is the
  shortlist the re-ranker was given.
- **global** (`--dry --global`, no requests spent): every bucket flattened, caps off,
  sorted by the engine's own key `(-_score, len(text), id)`. A harsher baseline the door
  never shows. Reported in its own column because the two disagree sharply.

## Per-query table

`before` / `after` = 1-based rank of `correct_id` in the door-display top-20, before and
after the Jev re-rank. `global` = rank in the caps-off flattened order. `trunc` = how many
of the 20 candidates were cut at 600 chars.

| query | correct_id | before | after | Δ | global | trunc | latency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scatter exemplar chart expansion step 1` | `ledger:two-lanes-the-m-set-splits-chart-jobs-lose-their-m-codes-202` | 11 | 10 | +1 | **absent** | 16 | 909.3 ms |
| `#93 stratum wrap point 49,071` | `ledger:93-the-stop-line-re-priced-and-the-premise-that-died-twice-2` | 10 | **1** | **+9** | 1 | 19 | 874.8 ms |
| `66-D6 A2 permanent strict sparkline sheds scatter key connects` | `ledger:66-2026-08-01-the-voice-pass-discharged-as-is` | 10 | 17 | **−7** | 6 | 20 | 920.5 ms |
| `0c next build candidates` | `gm:DOFIRST` | 3 | 4 | −1 | **absent** | 19 | 965.6 ms |
| `opacity primitives 4% spread` | `ledger:98-2026-08-05-one-bar-enacted-snippet-sources-become-pure-ca` | 7 | 4 | +3 | 4 | 20 | 881.4 ms |
| `125/49 corpus fork` | `ls:DELTAS` | **absent** | **absent** | — | **absent** | 20 | 1000.1 ms |
| `capture ritual sequence` | `runbook:capture-ritual:HDR` | 14 | 17 | −3 | 1 | 17 | 895.7 ms |
| `compose-audit --sc inline-scope` | `gm:PRIOR` | 5 | 5 | — | **absent** | 18 | 915.6 ms |
| `DV-D19 legend specimen rebuild real canon` | `gm:PRIOR` | **absent** | **absent** | — | **absent** | 20 | 918.4 ms |
| `184 memory owed two-red mono blind gate` | `gm:PRIOR` | **absent** | **absent** | — | **absent** | 20 | 935.3 ms |
| `band table amber threshold remaining budget` | `runbook:context-gauge:the-floor-is-measured-never-assumed-gm-d9` | **absent** | **absent** | — | **absent** | 20 | 917.1 ms |
| `lane routing check blocking records` | `lane:lane-1-memento` | 3 | 3 | — | **absent** | 19 | 942.3 ms |
| `batch #30` | `gm-archive:batch-2026-07-27-17-rolled-by-the-wrap-of-the-memento-harden` | 18 | **5** | **+13** | 6 | 18 | 914.5 ms |
| `ds-018` | `gm:C2` | **1** | 6 | **−5** | 12 | 20 | 888.9 ms |

## Aggregate — measured, n = 14, confidence LOW

| | MRR | hits@1 | hits@3 | correct id absent from the top-20 |
| --- | --- | --- | --- | --- |
| **lexical (door-display)** | **0.173** | **1 / 14** | **3 / 14** | **4 / 14** |
| **+ Jev re-rank** | **0.187** | **1 / 14** | **2 / 14** | 4 / 14 (unchanged — a re-rank cannot add a candidate) |
| lexical (global, caps off) | 0.190 | 2 / 14 | 2 / 14 | 8 / 14 |

MRR counts an absent correct id as 0 — the standard convention, stated rather than hidden.
The global row is a BASELINE ONLY; no requests were spent re-ranking it.

**The honest reading: flat.** MRR moves +0.014 on n = 14. Four rows improved (one by 13
places, one by 9), four degraded, three were unchanged and three could not move because
the correct record was never on the shortlist. At this n a single row is worth ~0.07 of
MRR, so the change is inside the noise of one query. This measures **no useful lift and no
useful harm** — it does not measure that re-ranking cannot help.

## Cost and time — measured

| | |
| --- | --- |
| requests | **14** (budget 15; no typed error, no retry fired) |
| tokens | **102,106 input / 4,256 output** — 7,293 input per request |
| latency | mean **920.0 ms**, median 916.4, min 874.8, max 1000.1 |
| total wall | **14.0 s** for all fourteen, run serially |
| cost | **not reported by the API.** At the rerank cookbook's *declared* jev-1.12 price of $0.042 / 1M input tokens this is ≈ **$0.0043** for the whole run — a declared figure carried over from the vendor's cookbook, not a measured one. |

**Latency against the record.** J2 measured 693.5 ms mean (n=2), J3 594.6 ms (n=3), both
on single-digit question counts. J4's 920.0 ms (n=14) carries **twenty Score questions and
~7.3K input tokens per request**; TypeSafe's declared band is 70–500 ms. Nineteen live
calls to date, every one of them above the top of the declared band.

## The exact request, for one query

Query `ds-018`. `state` is the real evidence, never a description of it (the J3 lesson):
the candidates ARE the record text, capped at 600 chars each.

State shape (candidate 0 shown in full; 19 more follow, same shape):

```json
{
  "query": "ds-018",
  "candidates": [
    {
      "i": 0,
      "text": "## 2. ★ DAVE: THE RULING BATCH — 15 REMAIN of 16 (D-Q3 ✅ #14; Q8/B2 → DV-D08) + the ★ DATAVIZ\nSIGN-OFF (rule by number; all retro-propagate). **Sign-off first:** D promoted the PARKED kit verbatim\ninto Chart-bar/line/donut/sparkline — your review flips them provisional-agent→canon (open-014).\n*(Your three chart flags, #6 — filed same minute per ds-017: verbatim + read-backs in\n`_DATAVIZ-DECISIONS.md` § Batch 10 + `_DS-IMPROVEMENTS.md` § ds-018. 23–25 below = state lines only.)*\n**✅ CLOSED-AGGREGATE, rolled #38 (2e closure-tombstone term = LATEST+2; all ruled #14–#27, guards = ledger closed-lin"
    },
    { "i": 1, "text": "…" }
  ]
}
```

Candidate ids in shortlist order: `gm:C2` · `gm:DOFIRST` ·
`ledger:121-2026-08-07-ds-018-ruled-enacted-s121-d1` ·
`ledger:86-2026-08-02-sun-triage-bankruptcy-session-declared-budget` ·
`ledger:212-the-triage-sitting-twelve-rulings-and-dave-s-desk-goes-4` ·
`gauge:2026-08-07-121` · `gauge:2026-08-16-187` · `gauge:2026-08-17-191` · … (20 total).

`questions` — twenty of these, `c00`…`c19`, identical but for the index:

```json
{
  "c00": {
    "type": "score",
    "instructions": "How well does the candidate passage at candidates[0].text answer the search query in `query`?",
    "criteria": [
      "Unrelated to the query: the candidate is about a different subject entirely.",
      "Shares words or vocabulary with the query but does not address what it asks.",
      "Partially answers the query: touches the subject, but is not the record the query is looking for.",
      "Directly answers the query: this is the record the query is asking for, and reading it settles the question."
    ]
  },
  "c01": { "type": "score", "instructions": "How well does the candidate passage at candidates[1].text answer the search query in `query`?", "criteria": [ "…same four levels…" ] }
}
```

## What the scores looked like

280 Score answers over the 14 requests. Mean 1.05 on the 0–3 ladder; rounded distribution
**0: 55 · 1: 166 · 2: 52 · 3: 7**. **No ties at the top of any shortlist** — every query got
a strict ordering, so the tie-break on lexical rank never fired. Mean per-query confidence
ranged 0.28 (`compose-audit --sc inline-scope`) to 0.68. The ladder is doing real work: it
is not collapsing to one level the way J3's `absence_honesty` collapsed at the P/M
boundary.

## The one that is worth arguing about

`ds-018` is the biggest single degradation (1 → 6) and it is the row where the FIXTURE is
most open to challenge. Jev put
`ledger:121-2026-08-07-ds-018-ruled-enacted-s121-d1` first, at 2.97 with the mass on
level 3 — a ledger section whose title says ds-018 was ruled and enacted. The fixture's
correct answer is `gm:C2`, because that is what session #131's receipt named. **Both are
defensible and the ledger record is arguably the better answer**, but the fixture scores
against what the session fetched, not against what a reader would now prefer, so this
counts as a degradation. Stated, not smoothed: on at least one of fourteen rows the metric
is punishing the re-ranker for an answer that may be right.

Raw: `rerank-raw.json` (door-display, live) · `rerank-raw-global.json` (global, dry).
Receipts for all 14 calls, with request ids and questions as sent:
`knowledge/_jev-receipts.jsonl`.
