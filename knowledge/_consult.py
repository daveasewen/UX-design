#!/usr/bin/env python3
"""_consult.py — "what governs X?", answered in one step. THE DS-DECISIONS DOOR.

Part 2 of the consult read-side tool (reviews/CONSOLIDATION-AUDIT-2026-07-18.html §3).
Since O2′ (#25, ruled Dave 2026-07-28) this file is a THIN DOOR over the shared engine
`knowledge/_search_core.py` — matching, ranking, honest denominators and the two-stage
fetch contract live THERE (one copy; the Memento door `_memento_search.py` imports the
same spine). This door owns: the DS corpus (knowledge/_consult-index.json, built by
_build_consult_index.py), the six output groups, and the enforcement column.

Usage:
  python3 knowledge/_consult.py "amber indicator on white"          # stage 1: ranked refs
  python3 knowledge/_consult.py "amber indicator on white" --all    # no per-group cap
  python3 knowledge/_consult.py "amber indicator on white" --json   # machine-readable
  python3 knowledge/_consult.py --fetch R-D3                        # stage 2: full record verbatim
  python3 knowledge/_consult.py --selftest                          # regression check

Two-stage (O2′): stage 1 shows each record's head (first 140 chars) as a REF — that is a
pointer, not the record; stage 2 `--fetch <id>` prints the indexed text IN FULL. The old
single-stage output truncated at 140 chars with no way back — the KG-float complaint;
fetch retires it. Group headers now quote the true matched TOTAL, never the cap
(the §C·4 "5/5 shown" wart, closed here).

Matching = keyword over text + a small hand-authored synonym lexicon
(knowledge/_consult-lexicon.json) that grows one line each time a real query misses —
curation is part of the job, not a one-off seed.

Groups, in this fixed order: rulings, blocking rules, advisory rules, assertions, open
items, gates. Every RULE record also carries an enforcement column: "gated by <script>
over <bite>" (or "possibly gated by..." on a fuzzy file/topic match) if a gate record's
text/glob plausibly covers the rule's source file, else "asserted only — no gate bites"
— the gate-glob-coverage question, answered per-query instead of as a separate campaign.

Advisory tier (AGENTS principle 5): this tool does not gate anything today. The pre-flight
protocol (run a consult before designing; paste the receipt into the review sheet/meta) is
documented in knowledge/_RUNBOOK-consult.md — and since #25 the wrap stratum carries a
`consult-receipts` line (ADVISORY probe, format in _search_core.py).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _search_core as core
import _graph_edges  # #115 steps 1+3: ADVISORY edge attachment, display-only

INDEX_PATH = os.path.join(HERE, "_consult-index.json")
LEXICON_PATH = os.path.join(HERE, "_consult-lexicon.json")

KIND_ORDER = ["ruling", "rule-blocking", "rule-advisory", "assertion", "open-item", "gate"]
KIND_LABEL = {
    "ruling": "rulings",
    "rule-blocking": "blocking rules",
    "rule-advisory": "advisory rules",
    "assertion": "assertions",
    "open-item": "open items",
    "gate": "gates",
}
DEFAULT_CAP = {
    "ruling": 5, "rule-blocking": 5, "rule-advisory": 5,
    "assertion": 5, "open-item": 3, "gate": 5,
}

# Small code-level bridge for the enforcement-column fuzzy match, kept separate from the
# user-facing lexicon (that one expands SEARCH queries; this one bridges gate-script jargon
# to guideline-file topic words, e.g. the a11y gate's short name vs "accessibility").
TOPIC_BRIDGE = {
    "a11y": {"accessibility"}, "accessibility": {"a11y"},
    "dataviz": {"visualisation", "visualization", "data"},
    "data": {"dataviz"},
    "css": {"styling", "style"},
    "proforma": {"pro-forma"},
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def bucket_for(record):
    if record["kind"] == "rule":
        return "rule-blocking" if record.get("status") == "BLOCKING" else "rule-advisory"
    if record["kind"] in KIND_ORDER:
        return record["kind"]
    # adr / defect records are indexed (future consumers, e.g. a chat surface) but
    # are not one of the six groups this CLI's output is specified to show.
    return None


# Generic enough that a shared occurrence says nothing about topical overlap (every gate's
# docstring says "gate", most files live under a "standards"/"guidelines" doc, etc.)
GENERIC_TOPIC_WORDS = {
    "assets", "asset", "standards", "standard", "general", "common", "guide", "guides",
    "guideline", "guidelines", "rules", "rule", "design", "token", "tokens", "component",
    "components", "usage", "content", "digital", "knowledge", "validate", "gate", "gates",
    "html", "file", "files", "reference",
}


def _is_topic_word(w):
    # len>=4, not purely numeric (years collide), not too generic to mean anything
    return len(w) >= 4 and not w.isdigit() and w not in GENERIC_TOPIC_WORDS


def gate_keywords(gate):
    text = " ".join([gate.get("id", ""), gate.get("text", ""), gate.get("bite") or ""])
    words = set(w for w in re.split(r"[^a-z0-9]+", text.lower()) if _is_topic_word(w))
    bridged = set(words)
    for w in words:
        bridged |= TOPIC_BRIDGE.get(w, set())
    return bridged


def rule_keywords(rule):
    stem = os.path.splitext(os.path.basename(rule.get("file", "")))[0].lower()
    words = set(w for w in re.split(r"[-_]", stem) if _is_topic_word(w))
    bridged = set(words)
    for w in words:
        bridged |= TOPIC_BRIDGE.get(w, set())
    return bridged


def enforcement_for_rule(rule, gates):
    rkeys = rule_keywords(rule)
    if not rkeys:
        return "asserted only — no gate bites"
    fuzzy = None
    for g in sorted(gates, key=lambda x: x["id"]):
        gkeys = gate_keywords(g)
        if rkeys & gkeys:
            return f"gated by {g['id']} over {g.get('bite') or 'unknown'}"
        if fuzzy is None:
            for rk in rkeys:
                for gk in gkeys:
                    if (rk in gk or gk in rk) and rk != gk:
                        fuzzy = f"possibly gated by {g['id']} over {g.get('bite') or 'unknown'} (fuzzy: {rk}~{gk})"
                        break
                if fuzzy:
                    break
    return fuzzy or "asserted only — no gate bites"


def search(query, index, lexicon, all_results=False):
    gates = [r for r in index["records"] if r["kind"] == "gate"]

    def decorate(entry):
        if entry["kind"] == "rule":
            entry["_enforcement"] = enforcement_for_rule(entry, gates)
        # #115 step 1 (ADVISORY): ~79/635 DS-door records ARE graph nodes directly
        # (ADR-*/R-D*/DV-D*/T-D* ids match `_decision-graph.json` node ids one-for-one) —
        # `_graph_edges.nodes_for_record` finds those via direct id match, same call as
        # the Memento door's mention-map lookup. Adds keys only, never re-scores/-sorts.
        entry["_graph_neighbours"] = _graph_edges.neighbour_lines(entry)
        # #115 step 3 (MARK-ONLY, separate function/hunk from step 1 above).
        entry["_graph_superseded"] = _graph_edges.superseded_lines(entry)

    buckets, totals, original, expanded = core.search(
        index["records"], query, lexicon, bucket_for, DEFAULT_CAP,
        all_results=all_results, decorate=decorate)
    return buckets, totals, original, expanded


def print_human(buckets, totals, query, expanded, all_results):
    print(f'consult: "{query}"')
    if expanded:
        print(f"  lexicon expanded to: {', '.join(sorted(expanded))}")
    total = sum(len(v) for v in buckets.values())
    if total == 0:
        print("  no matches. Consider adding a synonym to knowledge/_consult-lexicon.json"
              " if this is a real miss.")
        return
    if not _graph_edges.available():
        print(f"  ({_graph_edges.unavailable_notice()})")
    for kind in KIND_ORDER:
        rows = buckets.get(kind, [])
        if not rows:
            continue
        print("\n" + core.group_header(KIND_LABEL[kind], len(rows), totals.get(kind, len(rows)),
                                       all_results))
        for r in rows:
            head = f"  [{r['id']}] ({r.get('status', 'unknown')}) {r['text'][:140]}"
            print(head)
            if kind in ("rule-blocking", "rule-advisory"):
                print(f"      -> {r['_enforcement']}")
            print(f"      source: {r['file']}  (stage 2: --fetch {r['id']})")
            # #115 step 3 (MARK-ONLY) before step 1's neighbour lines
            for line in r.get("_graph_superseded", []):
                print(f"      {line}")
            # #115 step 1 (ADVISORY)
            for line in r.get("_graph_neighbours", []):
                print(f"      {line}")
            # #115 observation recorder — DISPLAYED marks only; loud on write failure.
            notice = _graph_edges.record_observation("consult", query, r)
            if notice:
                print(f"      {notice}")


def print_fetch(index, record_id):
    record, err = core.fetch(index["records"], record_id)
    if err:
        print(err)
        return 1
    print(f"[{record['id']}] kind={record['kind']} status={record.get('status', 'unknown')}")
    print(f"source: {record['file']}")
    print()
    print(record.get("text", "").rstrip())
    return 0


def build_json(buckets):
    out = {}
    for kind in KIND_ORDER:
        out[KIND_LABEL[kind]] = buckets.get(kind, [])
    return out


# ------------------------------------------------------------------ selftest
SELFTEST_CASES = [
    ("amber glyph contrast white", {"R-D3", "avd-001"}),
    ("inline fonts portability", {"T-D9"}),
    ("univers sandbox render", {"ASSERT-002", "ASSERT-006"}),
]


def run_selftest(index, lexicon):
    ok = True
    for query, expect_ids in SELFTEST_CASES:
        buckets, _, _, _ = search(query, index, lexicon, all_results=True)
        found = set()
        for rows in buckets.values():
            found |= {r["id"] for r in rows}
        missing = expect_ids - found
        status = "OK" if not missing else "FAIL"
        print(f"[{status}] \"{query}\" — expected {sorted(expect_ids)}, "
              f"missing {sorted(missing) if missing else 'none'}")
        if missing:
            ok = False
    # O2′ bites: the two-stage fetch, both directions
    record, err = core.fetch(index["records"], "R-D3")
    hit = record is not None and err is None and record.get("text")
    print(f"[{'OK' if hit else 'FAIL'}] --fetch R-D3 returns the full record (stage 2 hit)")
    ok = ok and bool(hit)
    record, err = core.fetch(index["records"], "NO-SUCH-ID-XYZ")
    refused = record is None and err and "REFUSING" in err
    print(f"[{'OK' if refused else 'FAIL'}] --fetch unknown id REFUSES (fail-loud)")
    ok = ok and bool(refused)
    # #115 steps 1+3: same edge-attachment bites as the Memento door, on synthetic
    # state so they can FAIL independent of disk state. Real state saved/restored.
    saved = dict(_graph_edges._state)
    try:
        _graph_edges._state.update({
            "loaded": True,
            "graph": {"nodes": {"ADR-X": {}, "ADR-Y": {}},
                      "edges": [{"from": "ADR-Y", "type": "supersedes", "to": "ADR-X"}]},
            "reverse": {},
        })
        no_mention = _graph_edges.neighbour_lines({"id": "some-other-id"})
        bite_a = no_mention == []
        print(f"[{'OK' if bite_a else 'FAIL'}] edge attach: record with no mention gets no attachment")
        ok = ok and bite_a
        # DS door: direct id match — a record whose id IS a graph node
        hit_lines = _graph_edges.neighbour_lines({"id": "ADR-X"})
        bite_b = "⌁ ADR-X superseded-by ADR-Y" in hit_lines
        print(f"[{'OK' if bite_b else 'FAIL'}] edge attach: injected fabricated edge appears via direct id match")
        ok = ok and bite_b
        mark_lines = _graph_edges.superseded_lines({"id": "ADR-X"})
        bite_c = mark_lines == ["⛔ SUPERSEDED by ADR-Y"]
        print(f"[{'OK' if bite_c else 'FAIL'}] step 3 mark: target-of-supersedes record gets the ⛔ line")
        ok = ok and bite_c
    finally:
        _graph_edges._state.clear()
        _graph_edges._state.update(saved)
    if ok:
        print("selftest OK — all regression queries surfaced their known-answer record(s).")
    else:
        print("selftest FAILED — a known-answer record was not retrieved. Fix the lexicon "
              "or ranking, do not special-case the query string.")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    index = core.load_records_or_refuse(INDEX_PATH, "consult (DS door)")
    lexicon = load_json(LEXICON_PATH)

    if args and args[0] == "--selftest":
        return run_selftest(index, lexicon)

    if "--fetch" in args:
        i = args.index("--fetch")
        if i + 1 >= len(args):
            print("--fetch needs a record id. Usage: python3 knowledge/_consult.py --fetch <id>")
            return 1
        return print_fetch(index, args[i + 1])

    if not args:
        print(__doc__)
        return 1

    as_json = "--json" in args
    all_results = "--all" in args
    query_parts = [a for a in args if not a.startswith("--")]
    if not query_parts:
        print("no query given. Usage: python3 knowledge/_consult.py \"<query>\" "
              "[--all] [--json] | --fetch <id>")
        return 1
    query = " ".join(query_parts)

    buckets, totals, original, expanded = search(query, index, lexicon, all_results=all_results)

    if as_json:
        payload = {
            "query": query,
            "lexicon_expansion": sorted(expanded),
            "totals": {KIND_LABEL[k]: v for k, v in totals.items()},
            "results": build_json(buckets),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print_human(buckets, totals, query, expanded, all_results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
