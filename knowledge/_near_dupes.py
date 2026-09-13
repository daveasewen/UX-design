#!/usr/bin/env python3
"""_near_dupes.py — THE NEAR-DUPLICATE DOOR: "which records say the same thing twice?"
(#269, ADVISORY — a candidate list for the dream pass, never a merge).

WHY (research `_RESEARCH-ngram-lookups-2026-09-13-v1.html` use 4; Dave's "go for it"
2026-09-13): the weekly dream pass reads the archives by eye to find what to consolidate.
Word-shingle overlap finds the candidates by measurement — probed at #269: 22 pairs above
0.5 Jaccard among GM/LS archive sections and briefs, e.g. three consecutive GM batches
(08-28 / 08-29 / 08-30) at 0.56–0.58.

WHAT IT DOES: for the chosen record kinds, builds k-word shingles (default 8) over each
record's text and prints every pair whose Jaccard overlap is ≥ the threshold, best first,
with both ids, file:line and the overlap. Pairs are CANDIDATES — whether two records are
one record is the dream pass's proposal and Dave's ruling. This door NEVER writes.

Defaults are the archive kinds because that is where consolidation lives; `--kinds all`
sweeps everything (slower: pairs grow with the square of the record count).

Usage:
  python3 knowledge/_near_dupes.py                                    # archives + briefs, ≥0.5
  python3 knowledge/_near_dupes.py --threshold 0.35 --kinds brief,dream
  python3 knowledge/_near_dupes.py --kinds all --json
  python3 knowledge/_near_dupes.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _search_core as core
import _ngram as ng

INDEX_PATH = os.path.join(HERE, "_memento-index.json")
MARK = "NEAR-DUPES ADVISORY"
DEFAULT_KINDS = ("gm-archive-section", "ls-archive-section", "brief", "dream")


def find_pairs(records, threshold=0.5, k=8, min_shingles=3):
    """[(jaccard, rec_a, rec_b)] best first. Records with fewer than `min_shingles`
    shingles are skipped — a two-line record is 'similar' to everything and to nothing."""
    sh = []
    for r in records:
        s = ng.shingles(str(r.get("text", "")), k)
        if len(s) >= min_shingles:
            sh.append((r, s))
    # inverted index shingle → record positions, so we only compare pairs that share one
    post = {}
    for i, (_, s) in enumerate(sh):
        for g in s:
            post.setdefault(g, []).append(i)
    seen = set()
    out = []
    for g, ids in post.items():
        if len(ids) < 2:
            continue
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                a, b = ids[x], ids[y]
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                j = ng.jaccard(sh[a][1], sh[b][1])
                if j >= threshold:
                    out.append((round(j, 2), sh[a][0], sh[b][0]))
    out.sort(key=lambda t: (-t[0], t[1]["id"], t[2]["id"]))
    return out


def report(pairs, scanned, threshold, as_json=False):
    if as_json:
        print(json.dumps({"marker": MARK, "threshold": threshold, "scanned": scanned,
                          "pairs": [{"jaccard": j, "a": a["id"], "b": b["id"],
                                     "a_at": f"{a.get('file')}:{a.get('line')}",
                                     "b_at": f"{b.get('file')}:{b.get('line')}"} for j, a, b in pairs]},
                         indent=2, ensure_ascii=False))
        return
    print(f"{MARK} — {len(pairs)} pair(s) at ≥ {threshold} overlap across {scanned} record(s)")
    for j, a, b in pairs:
        print(f"  {j:.2f}  {a['id']}  ·  {b['id']}\n        {a.get('file')}:{a.get('line')}  ·  {b.get('file')}:{b.get('line')}")


def selftest():
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    base = "one two three four five six seven eight nine ten eleven twelve"
    recs = [
        {"id": "A", "file": "a.md", "line": 1, "text": base},
        {"id": "B", "file": "b.md", "line": 2, "text": base + " thirteen"},
        {"id": "C", "file": "c.md", "line": 3, "text": "an entirely different sentence about amber and descenders and lanes"},
        {"id": "D", "file": "d.md", "line": 4, "text": "too short"},
    ]
    pairs = find_pairs(recs, threshold=0.5, k=4)
    bite("A and B (one appended word) are a pair", [(a["id"], b["id"]) for _, a, b in pairs] == [("A", "B")])
    bite("C pairs with nothing", not any("C" in (a["id"], b["id"]) for _, a, b in pairs))
    bite("a record under min_shingles is skipped, not matched", not any("D" in (a["id"], b["id"]) for _, a, b in pairs))
    bite("mutation: threshold 0.99 finds nothing", find_pairs(recs, threshold=0.99, k=4) == [])
    src = open(__file__, encoding="utf-8").read().split("def selftest")[0]
    bite("door has no write path", '"w"' not in src and "'w'" not in src)
    print("near-dupes selftest:", "FAIL " + ", ".join(fails) if fails else "OK")
    return 1 if fails else 0


def main():
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    threshold, kinds, as_json, k = 0.5, DEFAULT_KINDS, "--json" in argv, 8
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--threshold":
            i += 1; threshold = float(argv[i])
        elif a == "--kinds":
            i += 1; kinds = None if argv[i] == "all" else tuple(argv[i].split(","))
        elif a == "--k":
            i += 1; k = int(argv[i])
        elif a == "--json":
            pass
        else:
            raise SystemExit(f"near-dupes: unknown argument {a} — see --help")
        i += 1
    records = core.load_records_or_refuse(INDEX_PATH, "near-dupes")["records"]
    chosen = [r for r in records if kinds is None or r.get("kind") in kinds]
    if not chosen:
        raise SystemExit(f"near-dupes: no records of kind(s) {kinds} — kinds in the index: "
                         f"{sorted(set(r.get('kind') for r in records))}")
    report(find_pairs(chosen, threshold, k), len(chosen), threshold, as_json)


if __name__ == "__main__":
    main()
