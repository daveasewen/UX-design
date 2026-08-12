#!/usr/bin/env python3
"""_build_graph_mention_map.py — the join `_decision-graph.json` and `_memento-index.json`
lack (#115 graph-candidates-pricing-brief, step 0).

`_decision-graph.json` node ids (100: `ADR-*`, `R-D*`, `TYPE:*`, `DV:*`, …) have ZERO
overlap with `_memento-index.json` record ids (575, `gm:*` / ledger ids / …) — edges
cannot be joined by id. Records DO mention node ids in body text, so this builds the
missing join: node-id -> [record ids whose blob mentions it], by literal (case-
insensitive) substring search of each node id against the record blob (mirrors
`_search_core.record_blob`, field-for-field). This build step reads corpus JSONs
directly rather than importing the door/spine modules — same posture as the other
build/_build_*.py scripts.

Fail-loud contract (ds-016 class, repo convention): a missing input file REFUSES,
loud and named — never a silent empty map.

Usage:
  python3 knowledge/_build_graph_mention_map.py             # write the map
  python3 knowledge/_build_graph_mention_map.py --check     # determinism / staleness gate
  python3 knowledge/_build_graph_mention_map.py --selftest  # bites: hit, miss, refusal
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(HERE, "_decision-graph.json")
INDEX_PATH = os.path.join(HERE, "_memento-index.json")
OUT_PATH = os.path.join(HERE, "_graph-mention-map.json")


def record_blob(r):
    """Mirrors `_search_core.record_blob` — same field set, same lowering. Duplicated
    (not imported) deliberately: this build step reads corpus JSONs directly like its
    siblings, no import of a door/spine module at build time."""
    return " ".join(str(r.get(k, "")) for k in ("id", "kind", "file", "head", "text", "status")).lower()


def load_graph_nodes(path=GRAPH_PATH):
    if not os.path.exists(path):
        raise SystemExit(f"graph mention map: REFUSING — decision-graph missing at {path} "
                         f"(run knowledge/_build_decision_graph.py first).")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    nodes = data.get("nodes")
    if not nodes:
        raise SystemExit(f"graph mention map: REFUSING — {path} holds ZERO nodes; "
                         f"a graph with nothing to join is broken, not quiet.")
    return nodes


def load_memento_records(path=INDEX_PATH):
    if not os.path.exists(path):
        raise SystemExit(f"graph mention map: REFUSING — memento index missing at {path} "
                         f"(run knowledge/_build_memento_index.py first).")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    records = data.get("records")
    if not records:
        raise SystemExit(f"graph mention map: REFUSING — {path} holds ZERO records; "
                         f"REFUSING to build a mention map over nothing.")
    return records


def build_map(node_ids, records):
    """node-id -> sorted list of record ids whose blob contains the node id as a literal
    (case-insensitive) substring. Deterministic: node ids and hit lists both sorted."""
    blobs = [(r["id"], record_blob(r)) for r in records]
    out = {}
    for nid in node_ids:
        needle = nid.lower()
        hits = sorted(rid for rid, blob in blobs if needle in blob)
        if hits:
            out[nid] = hits
    return out


def render(mention_map):
    payload = {
        "$generated_by": "knowledge/_build_graph_mention_map.py — never hand-edit; "
                         "regenerated every build (#115 step 0)",
        "map": mention_map,
    }
    return json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


def build():
    nodes = load_graph_nodes()
    records = load_memento_records()
    node_ids = sorted(nodes.keys())
    mention_map = build_map(node_ids, records)
    return mention_map, node_ids


# ------------------------------------------------------------------ selftest
def selftest():
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    # synthetic hit: a record whose blob literally contains the node id
    node_ids = ["ADR-0005", "ADR-9999-NOWHERE"]
    records = [
        {"id": "gm:X", "kind": "gm-section", "file": "f.md", "head": "h",
         "text": "see ADR-0005 for the ruling", "status": ""},
        {"id": "gm:Y", "kind": "gm-section", "file": "f.md", "head": "h",
         "text": "unrelated text entirely", "status": ""},
    ]
    m = build_map(node_ids, records)
    bite("synthetic hit: ADR-0005 mentioned in gm:X is found",
         m.get("ADR-0005") == ["gm:X"])
    # synthetic miss: a node id that appears nowhere gets no entry
    bite("synthetic miss: unmentioned node id has no key",
         "ADR-9999-NOWHERE" not in m)
    # case-insensitivity
    m2 = build_map(["adr-0005"], [{"id": "gm:Z", "kind": "x", "file": "f", "head": "h",
                                    "text": "ADR-0005 in caps", "status": ""}])
    bite("case-insensitive match", m2.get("adr-0005") == ["gm:Z"])
    # refusal on missing graph input
    try:
        load_graph_nodes(os.path.join("/nonexistent", "_no-graph.json"))
        bite("missing graph input REFUSES", False)
    except SystemExit as e:
        bite("missing graph input REFUSES", "REFUSING" in str(e))
    # refusal on missing memento index input
    try:
        load_memento_records(os.path.join("/nonexistent", "_no-index.json"))
        bite("missing memento index input REFUSES", False)
    except SystemExit as e:
        bite("missing memento index input REFUSES", "REFUSING" in str(e))
    # refusal on empty records (a broken parser, not a quiet corpus)
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"records": []}, f)
        empty_path = f.name
    try:
        load_memento_records(empty_path)
        bite("empty memento index REFUSES", False)
    except SystemExit as e:
        bite("empty memento index REFUSES", "REFUSING" in str(e))
    finally:
        os.unlink(empty_path)

    if fails:
        print(f"selftest FAILED — {len(fails)} bite(s): {fails}")
        return 1
    print("selftest OK — hit, miss, case-insensitivity and both input refusals all bite.")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    mention_map, node_ids = build()
    text = render(mention_map)
    if "--check" in sys.argv:
        if not os.path.exists(OUT_PATH):
            print("graph mention map --check: map file missing — run the build")
            return 1
        with open(OUT_PATH, encoding="utf-8") as f:
            on_disk = f.read()
        if on_disk != text:
            print("graph mention map --check: STALE — regenerate (the map on disk does not "
                  "match the corpus; never hand-edit it)")
            return 1
        print(f"graph mention map --check: current ({len(mention_map)} of {len(node_ids)} "
              f"node(s) mentioned)")
        return 0
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    total_hits = sum(len(v) for v in mention_map.values())
    print(f"graph mention map: {len(mention_map)} of {len(node_ids)} node(s) mentioned, "
          f"{total_hits} record hit(s) total -> {os.path.relpath(OUT_PATH, HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
