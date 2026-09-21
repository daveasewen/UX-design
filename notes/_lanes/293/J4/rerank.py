#!/usr/bin/env python3
"""rerank.py — lane 293/J4. Does a Jev Score re-rank beat lexical order on the Memento door?

WHAT THIS IS
A MEASURING INSTRUMENT, not a wiring. Nothing in the repo imports this file and nothing
should: `knowledge/_memento_search.py` is untouched by lane J4 and re-ranking is a
PROPOSAL, not a change. This script exists so the proposal can be argued from numbers.

THE SHAPE (docs.typesafe.ai/cookbooks/rerank_typesafe.md)
  1. FAST SEARCH — `_search_core.search()` via the Memento door's own bucket/cap policy.
     Lexical token overlap, stem candidates, lexicon expansion; score = 2x original-token
     hits + expanded-token hits. That is the shortlist: top-20, in the door's own display
     order (see WHAT "RANK" MEANS below).
  2. RE-RANK — ONE request per query. `state = {query, candidates:[{i, text}]}`; one Score
     question per candidate, 4 concrete levels. Re-sort by expected score, ties broken by
     the lexical rank that came in.

DEVIATION FROM THE COOKBOOK, DECLARED. The cookbook runs one Noul per (query, candidate)
pair — 30 requests per query — and its own closing note says a real application would ask
several questions about the same pair in one call (`/cookbooks/parallel_questions`,
`/patterns/fan-out`). This lane's live budget is one request per query, so the 20
candidates become 20 parallel Score questions in one request. Score rather than Noul
because the brief specified a 4-level ladder; the primitive doc
(`/primitives/score.md`) confirms parallel Scores in one request are evaluated
independently and cost only the extra question tokens. UNMEASURED CONSEQUENCE: all 20
candidates share one `state`, so a candidate is no longer judged in isolation the way the
cookbook's per-pair calls judge it. Whether that helps or hurts was not tested here.

WHAT "RANK" MEANS — stated, because the door has no single ranked list. `_memento_search.py`
prints PER-BUCKET lists (lane records, GM sections, ledger sections, ...), each capped
separately by `DEFAULT_CAP`. The baseline used here is THE ORDER A SESSION ACTUALLY READS:
the door's own capped output, buckets concatenated in `KIND_ORDER`, first 20 lines. Caps
are left ON, so the shortlist is what the door would really hand over — 31 rows at most,
usually fewer.

A GLOBAL variant (`--global`) is also available: every bucket flattened, caps off, sorted
by the engine's own key `(-_score, len(text), id)`. It is a HARSHER baseline that the door
never displays, and it was measured separately because the two disagree sharply — see the
subreport. Every rank number carries the mode it was measured in.

CAP: 20 candidates, 600 chars of text each. A record longer than 600 chars is judged on
its first 600. Truncation is counted and reported, never silent.

ORACLE RULE (knowledge/_jev.py): no key, no route -> JevUnavailable is an ABSENCE, not a
fail. This script prints the lexical baseline and exits 0 in that case.

Run:
    python3 notes/_lanes/293/J4/rerank.py --dry     # lexical baseline only, no network
    python3 notes/_lanes/293/J4/rerank.py           # live: one request per fixture query
"""
import json
import os
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
KNOW = os.path.join(REPO, "knowledge")
sys.path.insert(0, KNOW)

import _memento_search as door          # noqa: E402
import _search_core as core             # noqa: E402
import _jev                             # noqa: E402

FIXTURE = os.path.join(HERE, "fixture.jsonl")
OUT_JSON_FMT = os.path.join(HERE, "rerank-raw%s.json")
TOP_N = 20
TEXT_CAP = 600

LEVELS = [
    "Unrelated to the query: the candidate is about a different subject entirely.",
    "Shares words or vocabulary with the query but does not address what it asks.",
    "Partially answers the query: touches the subject, but is not the record the query "
    "is looking for.",
    "Directly answers the query: this is the record the query is asking for, and reading "
    "it settles the question.",
]


def load_fixture():
    rows = []
    with open(FIXTURE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("scored") is False or not r.get("correct_id"):
                continue
            rows.append(r)
    return rows


def lexical_topn(query, index, lexicon, n=TOP_N, global_mode=False):
    """The shortlist, in the order the door hands it over. See WHAT "RANK" MEANS above."""
    buckets, _totals, _orig, _exp = core.search(
        index["records"], query, lexicon, door.bucket_for, door.DEFAULT_CAP,
        all_results=global_mode, decorate=None)
    total = sum(len(v) for v in buckets.values())
    if global_mode:
        flat = [e for rows in buckets.values() for e in rows]
        flat.sort(key=lambda e: (-e["_score"], len(e.get("text", "")), e["id"]))
    else:
        flat = [e for kind in door.KIND_ORDER for e in buckets.get(kind, [])]
    return flat[:n], total


def candidate_text(rec):
    head = (rec.get("head") or "").strip()
    body = (rec.get("text") or "").strip()
    blob = (head + "\n" + body).strip() if head and not body.startswith(head) else (body or head)
    return blob[:TEXT_CAP], len(blob) > TEXT_CAP


def build_request(query, cands):
    state = {
        "query": query,
        "candidates": [{"i": i, "text": candidate_text(c)[0]} for i, c in enumerate(cands)],
    }
    questions = {}
    for i in range(len(cands)):
        questions["c%02d" % i] = _jev.score(
            "How well does the candidate passage at candidates[%d].text answer the "
            "search query in `query`?" % i, LEVELS)
    return state, questions


def rank_of(ids, correct):
    return ids.index(correct) + 1 if correct in ids else None


def mrr(ranks):
    """Absent-from-shortlist contributes 0 — the standard convention, stated not hidden."""
    return sum(0.0 if r is None else 1.0 / r for r in ranks) / len(ranks) if ranks else 0.0


def hits_at(ranks, k):
    return sum(1 for r in ranks if r is not None and r <= k)


def main():
    dry = "--dry" in sys.argv
    global_mode = "--global" in sys.argv
    index = core.load_records_or_refuse(door.INDEX_PATH, "293-J4 rerank probe")
    lexicon = door.load_lexicon()
    rows = load_fixture()

    if not dry and not _jev.available():
        print("no oracle (no TYPESAFE_API_KEY) — printing the lexical baseline only. "
              "An absence is not a fail.")
        dry = True

    results = []
    t_all = time.perf_counter()
    for row in rows:
        q, correct = row["query"], row["correct_id"]
        cands, total = lexical_topn(q, index, lexicon, global_mode=global_mode)
        ids = [c["id"] for c in cands]
        before = rank_of(ids, correct)
        rec = {"query": q, "correct_id": correct, "matched_total": total,
               "mode": "global" if global_mode else "door-display",
               "n_candidates": len(cands), "rank_before": before,
               "truncated": sum(1 for c in cands if candidate_text(c)[1]),
               "lexical_ids": ids}
        if not dry and cands:
            state, questions = build_request(q, cands)
            try:
                resp = _jev.ask(state, questions,
                                note="293-J4 memento re-rank probe: %r" % q)
            except _jev.JevError as exc:
                print("  retry after %s (error_type=%s)" % (exc.status, exc.error_type))
                time.sleep(2)
                resp = _jev.ask(state, questions,
                                note="293-J4 memento re-rank probe (retry): %r" % q)
            answers = resp.get("answers", {})
            scored = []
            for i, cid in enumerate(ids):
                a = answers.get("c%02d" % i, {})
                scored.append((a.get("score", 0.0), a.get("confidence"), i, cid))
            order = sorted(scored, key=lambda t: (-t[0], t[2]))
            after_ids = [t[3] for t in order]
            rec.update({
                "rank_after": rank_of(after_ids, correct),
                "latency_ms": resp.get("_latency_ms"),
                "request_id": resp.get("_request_id"),
                "model": resp.get("model"),
                "usage": resp.get("usage"),
                "scores": {cid: {"score": s, "confidence": c} for s, c, _i, cid in scored},
                "reranked_ids": after_ids,
            })
            print("  %-52s before=%s after=%s  %sms" % (q[:52], before, rec["rank_after"],
                                                        rec["latency_ms"]))
        else:
            print("  %-52s before=%s (matched %d)" % (q[:52], before, total))
        results.append(rec)

    wall = time.perf_counter() - t_all
    b = [r["rank_before"] for r in results]
    print("\nn = %d   absent from lexical top-%d: %d"
          % (len(results), TOP_N, sum(1 for r in b if r is None)))
    print("BEFORE  MRR %.3f  hits@1 %d  hits@3 %d" % (mrr(b), hits_at(b, 1), hits_at(b, 3)))
    if not dry:
        a = [r["rank_after"] for r in results]
        lat = [r["latency_ms"] for r in results if r.get("latency_ms")]
        print("AFTER   MRR %.3f  hits@1 %d  hits@3 %d" % (mrr(a), hits_at(a, 1), hits_at(a, 3)))
        print("latency mean %.1f ms  median %.1f  min %.1f  max %.1f  (n=%d)"
              % (statistics.mean(lat), statistics.median(lat), min(lat), max(lat), len(lat)))
        it = sum((r.get("usage") or {}).get("input_tokens", 0) for r in results)
        ot = sum((r.get("usage") or {}).get("output_tokens", 0) for r in results)
        print("tokens: %d input / %d output over %d requests" % (it, ot, len(lat)))
    print("total wall %.1f s" % wall)
    out_json = OUT_JSON_FMT % ("-global" if global_mode else "")
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump({"mode": "global" if global_mode else "door-display", "top_n": TOP_N, "text_cap": TEXT_CAP, "levels": LEVELS,
                   "dry": dry, "wall_s": round(wall, 1), "results": results},
                  fh, indent=2, ensure_ascii=False)
    print("raw -> %s" % os.path.relpath(out_json, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
