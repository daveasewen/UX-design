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
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(HERE, "_decision-graph.json")
MENTION_MAP_PATH = os.path.join(HERE, "_graph-mention-map.json")
OBSERVATIONS_PATH = os.path.join(HERE, "_graph-mark-observations.jsonl")

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


# ------------------------------------------------- observation recorder (#115 step-4 evidence)
def record_observation(door, query, entry, path=OBSERVATIONS_PATH):
    """Append one JSONL line per DISPLAYED result that carried a ⌁/⛔ mark — called by
    the doors' print loops (post-cap: it records what Dave/a session actually SAW, not
    what decorate computed and never showed). This is the instrument for the mark
    observation window: demote (brief item 4) gets ruled on this log's save-vs-noise
    tally, not on anyone's recollection.

    Returns None on success, or a LOUD one-line notice string the caller must print —
    a silent write failure would make the window blind while looking instrumented
    [measuring-tool-must-not-guess]. Never raises into the door: an advisory recorder
    must not take retrieval down."""
    neigh = entry.get("_graph_neighbours") or []
    sup = entry.get("_graph_superseded") or []
    if not neigh and not sup:
        return None
    import datetime
    rec = {
        "date": datetime.date.today().isoformat(),
        "door": door,
        "query": query,
        "record": entry.get("id"),
        "neighbour_lines": len(neigh),
        "superseded_by": sorted({l.rsplit(" ", 1)[-1] for l in sup}),
    }
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
        return None
    except OSError as e:
        return (f"⚠ mark observation NOT recorded ({e}) — the observation window is "
                f"blind for this query; declared, not silent")


def tally(path=OBSERVATIONS_PATH):
    """The recorder's reader (an instrument ships WITH its reader). Prints marks fired,
    by record and by query, superseded-marks separated — the shape the demote ruling
    needs. Refuses loudly on a missing/empty log rather than printing a zero that could
    read as 'no marks fired'."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print(f"tally REFUSED: {os.path.basename(path)} is missing or empty — either no "
              f"door has run since the recorder landed, or the recorder is broken. "
              f"An empty window is a claim that needs that distinction made, not a zero.")
        return 1
    rows = []
    with open(path, encoding="utf-8") as f:
        for i, ln in enumerate(f, 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                rows.append(json.loads(ln))
            except json.JSONDecodeError as e:
                print(f"tally REFUSED: line {i} unparseable ({e}) — fix the log, never skip")
                return 1
    marked = [r for r in rows if r.get("superseded_by")]
    print(f"mark observations: {len(rows)} displayed result(s) carried marks, "
          f"{len(marked)} carried a ⛔ SUPERSEDED mark, "
          f"{len({r['query'] for r in rows})} distinct query(ies), "
          f"{len({r['record'] for r in rows})} distinct record(s)")
    by_rec = {}
    for r in marked:
        by_rec.setdefault(r["record"], []).append(r)
    for rid, rs in sorted(by_rec.items(), key=lambda kv: -len(kv[1])):
        bys = sorted({b for r in rs for b in r["superseded_by"]})
        qs = sorted({r["query"] for r in rs})
        print(f"  ⛔ [{rid}] ×{len(rs)} — superseded-by {', '.join(bys)} — "
              f"queries: {', '.join(qs[:4])}{' …' if len(qs) > 4 else ''}")
    if not marked:
        print("  (no ⛔ marks displayed yet — only ⌁ neighbour attachments)")
    print("verdict material, not a verdict: save-vs-noise is judged per record above "
          "— a ledger record ABOUT a supersession is noise; a live-looking ruling that "
          "IS superseded is a save.")
    return 0


def _recorder_selftest():
    """Bites that can FAIL: a mark writes a line; a no-mark entry writes nothing; a
    write failure returns a LOUD notice, never raises; tally refuses an empty log."""
    import tempfile
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "obs.jsonl")
        marked = {"id": "X-1", "_graph_neighbours": ["⌁ a refines b"],
                  "_graph_superseded": ["⛔ SUPERSEDED by ADR-9"]}
        unmarked = {"id": "X-2", "_graph_neighbours": [], "_graph_superseded": []}
        bite("recorder: marked entry returns None (success)",
             record_observation("memento", "q", marked, path=p) is None)
        bite("recorder: line landed and parses with superseded_by",
             json.loads(open(p).read().strip())["superseded_by"] == ["ADR-9"])
        n_before = os.path.getsize(p)
        bite("recorder: unmarked entry writes NOTHING",
             record_observation("memento", "q", unmarked, path=p) is None
             and os.path.getsize(p) == n_before)
        notice = record_observation("memento", "q", marked,
                                    path=os.path.join(td, "no-such-dir", "obs.jsonl"))
        bite("recorder: write failure returns a LOUD notice, no raise",
             notice is not None and "NOT recorded" in notice)
        bite("tally: refuses a missing log", tally(os.path.join(td, "absent.jsonl")) == 1)
        bite("tally: reads the real shape", tally(p) == 0)
    if fails:
        print(f"recorder selftest FAILED — {fails}")
        return 1
    print("recorder selftest OK — writes, skips, fails loud, and the reader reads.")
    return 0


if __name__ == "__main__":
    if "--tally" in sys.argv:
        sys.exit(tally())
    if "--selftest" in sys.argv:
        sys.exit(_recorder_selftest())
    print(__doc__)
    sys.exit(0)
