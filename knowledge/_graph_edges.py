#!/usr/bin/env python3
"""_graph_edges.py — ADVISORY edge-attachment helper for the search doors (#115
graph-candidates-pricing-brief, steps 1 + 3). Display-only: every function here either
returns lines to APPEND to a result entry, or nothing. Nothing in this module touches
`score_record`, sort order, bucket membership, or caps — that is the brief's ABSOLUTE
CONSTRAINT for step 1, and step 3 (MARK-ONLY) inherits it.

Two distinct, separately-committable concerns live in this one small file (kept as two
functions rather than two files because both need the same lazy graph/mention-map load —
splitting the load would duplicate the degrade-loudly contract):

  STEP 1 (candidate 1, ADVISORY) — `neighbour_lines(entry)`: for a result whose id is a
  graph node (direct match, e.g. the DS door's `ADR-*`/`R-D*`/`DV-D*` records) OR is
  MENTIONED by a graph node (via the mention map built by
  `_build_graph_mention_map.py` — the join `_decision-graph.json` node ids and
  `_memento-index.json` record ids lack, 0/575 overlap), list that node's
  supersedes/refines/bounds neighbours, both directions, with direction+type shown.

  STEP 3 (candidate 2, MARK-ONLY) — `superseded_lines(entry)`: same node lookup, but
  only surfaces `⛔ SUPERSEDED by <node>` when the mentioned/matched node is the TARGET
  of a `supersedes` edge. NO ranking change, NO demotion — demotion is a later,
  separately-ruled step (#115 order item 4).

The edge-type vocabulary is CLOSED (#75) — this module CONSUMES `supersedes` /
`refines` / `bounds` from `_decision-graph.json`'s edge list; it never invents a type.

Degrade LOUDLY, never silently (repo convention, ds-016 class): if the mention map or
the decision graph is missing on disk, `available()` returns False and callers must
print `unavailable_notice()` once — they must NOT attach nothing and say nothing.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(HERE, "_decision-graph.json")
MENTION_MAP_PATH = os.path.join(HERE, "_graph-mention-map.json")

# Closed set (#75) — the only edge types step 1 ever surfaces as "neighbours".
NEIGHBOUR_TYPES = {"supersedes", "refines", "bounds"}
_REVERSE_LABEL = {
    "supersedes": "superseded-by",
    "refines": "refined-by",
    "bounds": "bounded-by",
}

_state = {"loaded": False, "graph": None, "reverse": None}


def _load(graph_path=GRAPH_PATH, mention_map_path=MENTION_MAP_PATH):
    """Lazy, memoised. Missing input -> graph stays None (degrade, never crash the
    door: an advisory seam must not be able to take retrieval down)."""
    if _state["loaded"]:
        return
    _state["loaded"] = True
    if not os.path.exists(graph_path) or not os.path.exists(mention_map_path):
        return
    with open(graph_path, encoding="utf-8") as f:
        graph = json.load(f)
    with open(mention_map_path, encoding="utf-8") as f:
        mention_map = json.load(f).get("map", {})
    reverse = {}
    for node_id, record_ids in mention_map.items():
        for rid in record_ids:
            reverse.setdefault(rid, []).append(node_id)
    _state["graph"] = graph
    _state["reverse"] = reverse


def _reset_for_test():
    """Test-only: forces the next call to re-run `_load()`. Used by selftests that
    inject synthetic paths/data, and to restore real state afterwards."""
    _state["loaded"] = False
    _state["graph"] = None
    _state["reverse"] = None


def available():
    _load()
    return _state["graph"] is not None


def unavailable_notice():
    return ("edge attachments unavailable — run "
            "_build_graph_mention_map.py")


def nodes_for_record(record_id):
    """Every graph node id relevant to this record: mention-map hits (record's blob
    mentions the node) UNION a direct id match (the record's own id IS a node id —
    true for ~79/635 DS-door records whose ids already are ADR-*/R-D*/DV-D* etc.)."""
    _load()
    graph, reverse = _state["graph"], _state["reverse"]
    if graph is None:
        return []
    out = set(reverse.get(record_id, []))
    if record_id in graph.get("nodes", {}):
        out.add(record_id)
    return sorted(out)


# ---------------------------------------------------------------- step 1 (ADVISORY)
def neighbour_lines(entry):
    """#115 step 1: supersedes/refines/bounds neighbours of every graph node this
    record matches, both directions, as display-only lines. [] if none or the graph
    is unavailable (caller handles the unavailable-notice separately)."""
    node_ids = nodes_for_record(entry.get("id"))  # triggers _load()
    graph = _state["graph"]
    if not node_ids or graph is None:
        return []
    edges = graph.get("edges", [])
    seen, lines = set(), []
    for nid in node_ids:
        for e in edges:
            etype = e.get("type")
            if etype not in NEIGHBOUR_TYPES:
                continue
            if e.get("from") == nid and e.get("to"):
                line = f"⌁ {nid} {etype} {e['to']}"
            elif e.get("to") == nid and e.get("from"):
                line = f"⌁ {nid} {_REVERSE_LABEL[etype]} {e['from']}"
            else:
                continue
            if line not in seen:
                seen.add(line)
                lines.append(line)
    return lines


# ---------------------------------------------------------------- step 3 (MARK-ONLY)
def superseded_lines(entry):
    """#115 step 3: `⛔ SUPERSEDED by <node>` for every graph node this record matches
    that is the TARGET of a `supersedes` edge. MARK ONLY — caller must never use this
    to reorder, cap, or demote; that is item 4 of the brief's order, not opened here."""
    node_ids = nodes_for_record(entry.get("id"))  # triggers _load()
    graph = _state["graph"]
    if not node_ids or graph is None:
        return []
    edges = graph.get("edges", [])
    supersessors = {}
    for e in edges:
        if e.get("type") == "supersedes" and e.get("to") and e.get("from"):
            supersessors.setdefault(e["to"], []).append(e["from"])
    seen, lines = set(), []
    for nid in node_ids:
        for by in sorted(set(supersessors.get(nid, []))):
            line = f"⛔ SUPERSEDED by {by}"
            if line not in seen:
                seen.add(line)
                lines.append(line)
    return lines
