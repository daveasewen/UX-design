#!/usr/bin/env python3
"""_consult.py — "what governs X?", answered in one step.

Part 2 of the consult read-side tool (reviews/CONSOLIDATION-AUDIT-2026-07-18.html §3).
Reads the generated knowledge/_consult-index.json (built by _build_consult_index.py) plus
the hand-authored knowledge/_consult-lexicon.json, and returns the ranked records that
govern a plain-English query.

Usage:
  python3 knowledge/_consult.py "amber indicator on white"     # ranked answer, one screen
  python3 knowledge/_consult.py "amber indicator on white" --all    # everything that matched
  python3 knowledge/_consult.py "amber indicator on white" --json  # machine-readable
  python3 knowledge/_consult.py --selftest                          # regression check

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
documented in knowledge/_RUNBOOK-consult.md.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(HERE, "_consult-index.json")
LEXICON_PATH = os.path.join(HERE, "_consult-lexicon.json")

STOPWORDS = {
    "the", "and", "for", "with", "on", "of", "a", "an", "in", "to", "is", "are",
    "it", "its", "be", "as", "at", "by", "or", "this", "that", "we", "our",
}

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


def tokenize(s):
    return [t for t in re.split(r"[^a-z0-9]+", s.lower()) if len(t) >= 3 and t not in STOPWORDS]


def expand_query(raw_query, lexicon):
    """Original query tokens, plus lexicon-expanded tokens. Returns (original_set, expanded_only_set)."""
    original = set(tokenize(raw_query))
    expanded = set()
    lc = raw_query.lower()
    for key, val in lexicon.get("synonyms", {}).items():
        if key in lc:
            expanded |= set(tokenize(val))
    expanded -= original
    return original, expanded


def stem_candidates(token):
    """A few cheap candidate substrings for a query token, so 'fonts' still finds 'font-size'
    and 'portability' still finds 'portable'. Not real stemming — substring search is."""
    cands = {token}
    if token.endswith("ing") and len(token) > 5:
        cands.add(token[:-3])
    if token.endswith("es") and len(token) > 4:
        cands.add(token[:-2])
    if token.endswith("s") and len(token) > 3:
        cands.add(token[:-1])
    if len(token) > 6:
        cands.add(token[:6])
    return {c for c in cands if len(c) >= 3}


def record_blob(r):
    return " ".join(str(r.get(k, "")) for k in ("id", "kind", "file", "text", "status")).lower()


def score_record(record, original_tokens, expanded_tokens):
    blob = record_blob(record)
    matched_original = 0
    for t in original_tokens:
        if any(c in blob for c in stem_candidates(t)):
            matched_original += 1
    matched_expanded = 0
    for t in expanded_tokens:
        if any(c in blob for c in stem_candidates(t)):
            matched_expanded += 1
    return matched_original * 2 + matched_expanded


def rule_bucket(rule):
    return "rule-blocking" if rule.get("status") == "BLOCKING" else "rule-advisory"


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
    original, expanded = expand_query(query, lexicon)
    gates = [r for r in index["records"] if r["kind"] == "gate"]
    buckets = {k: [] for k in KIND_ORDER}
    for r in index["records"]:
        if r["kind"] == "rule":
            bucket = rule_bucket(r)
        elif r["kind"] in buckets:
            bucket = r["kind"]
        else:
            # adr / defect records are indexed (future consumers, e.g. a chat surface) but
            # are not one of the six groups this CLI's output is specified to show.
            continue
        s = score_record(r, original, expanded)
        if s <= 0:
            continue
        entry = dict(r)
        entry["_score"] = s
        if r["kind"] == "rule":
            entry["_enforcement"] = enforcement_for_rule(r, gates)
        buckets[bucket].append(entry)
    for k in buckets:
        buckets[k].sort(key=lambda e: (-e["_score"], len(e.get("text", "")), e["id"]))
        if not all_results:
            buckets[k] = buckets[k][: DEFAULT_CAP[k]]
    return buckets, original, expanded


def print_human(buckets, query, original, expanded, all_results):
    print(f'consult: "{query}"')
    if expanded:
        print(f"  lexicon expanded to: {', '.join(sorted(expanded))}")
    total = sum(len(v) for v in buckets.values())
    if total == 0:
        print("  no matches. Consider adding a synonym to knowledge/_consult-lexicon.json"
              " if this is a real miss.")
        return
    for kind in KIND_ORDER:
        rows = buckets[kind]
        if not rows:
            continue
        print(f"\n{KIND_LABEL[kind]} ({len(rows)}{'' if all_results else f'/{DEFAULT_CAP[kind]} shown, --all for more'}):")
        for r in rows:
            head = f"  [{r['id']}] ({r.get('status', 'unknown')}) {r['text'][:140]}"
            print(head)
            if kind in ("rule-blocking", "rule-advisory"):
                print(f"      -> {r['_enforcement']}")
            print(f"      source: {r['file']}")


def build_json(buckets):
    out = {}
    for kind in KIND_ORDER:
        out[KIND_LABEL[kind]] = buckets[kind]
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
        buckets, _, _ = search(query, index, lexicon, all_results=True)
        found = set()
        for rows in buckets.values():
            found |= {r["id"] for r in rows}
        missing = expect_ids - found
        status = "OK" if not missing else "FAIL"
        print(f"[{status}] \"{query}\" — expected {sorted(expect_ids)}, "
              f"missing {sorted(missing) if missing else 'none'}")
        if missing:
            ok = False
    if ok:
        print("selftest OK — all regression queries surfaced their known-answer record(s).")
    else:
        print("selftest FAILED — a known-answer record was not retrieved. Fix the lexicon "
              "or ranking, do not special-case the query string.")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    index = load_json(INDEX_PATH)
    lexicon = load_json(LEXICON_PATH)

    if args and args[0] == "--selftest":
        return run_selftest(index, lexicon)

    if not args:
        print(__doc__)
        return 1

    as_json = "--json" in args
    all_results = "--all" in args
    query_parts = [a for a in args if not a.startswith("--")]
    if not query_parts:
        print("no query given. Usage: python3 knowledge/_consult.py \"<query>\" [--all] [--json]")
        return 1
    query = " ".join(query_parts)

    buckets, original, expanded = search(query, index, lexicon, all_results=all_results)

    if as_json:
        payload = {
            "query": query,
            "lexicon_expansion": sorted(expanded),
            "results": build_json(buckets),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print_human(buckets, query, original, expanded, all_results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
