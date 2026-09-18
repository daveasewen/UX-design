#!/usr/bin/env python3
"""Structured JSON diff of two _logo_nodes.json / _icon_nodes.json snapshots (#286 lane R2).

    python3 jsondiff.py BEFORE.json AFTER.json

Prints a JSON report: nodes added/removed, per-node field changes, edges added/removed
(by an identity that does not depend on list order), top-level keys added/removed/changed.
Reads only. It asserts nothing — the report is the measurement and the lane reads it.
"""
import json
import sys


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def ekey(e):
    return (e.get("s"), e.get("type"), e.get("t"))


def main(a, b):
    A, B = load(a), load(b)
    an = {n["id"]: n for n in A.get("nodes", [])}
    bn = {n["id"]: n for n in B.get("nodes", [])}
    changed = {}
    for i in sorted(set(an) & set(bn)):
        f = {}
        for k in sorted(set(an[i]) | set(bn[i])):
            if an[i].get(k) != bn[i].get(k):
                f[k] = {"was": "ABSENT" if k not in an[i] else an[i][k],
                        "now": "ABSENT" if k not in bn[i] else bn[i][k]}
        if f:
            changed[i] = f
    ae = [ekey(e) for e in A.get("edges", [])]
    be = [ekey(e) for e in B.get("edges", [])]
    top_a = {k: v for k, v in A.items() if k not in ("nodes", "edges")}
    top_b = {k: v for k, v in B.items() if k not in ("nodes", "edges")}
    rep = {
        "node_count": {"before": len(an), "after": len(bn)},
        "nodes_added": sorted(set(bn) - set(an)),
        "nodes_removed": sorted(set(an) - set(bn)),
        "node_fields_changed": {i: sorted(f) for i, f in changed.items()},
        "node_field_change_detail": changed,
        "edge_count": {"before": len(ae), "after": len(be)},
        "edges_added": [list(k) for k in sorted(set(be) - set(ae), key=str)],
        "edges_removed": [list(k) for k in sorted(set(ae) - set(be), key=str)],
        "edge_multiset_identical": sorted(map(str, ae)) == sorted(map(str, be)),
        "top_level_keys_added": sorted(set(top_b) - set(top_a)),
        "top_level_keys_removed": sorted(set(top_a) - set(top_b)),
        "top_level_keys_changed": sorted(k for k in set(top_a) & set(top_b)
                                         if top_a[k] != top_b[k]),
    }
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
