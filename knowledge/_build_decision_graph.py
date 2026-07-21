#!/usr/bin/env python3
"""
Decision-graph generator + conflict gate (ADR-0012, proposed; extends ADR-0007 slice 1).

WHY: rulings cross-reference in prose, so reconciliation was manual archaeology (the icon-011
R-D6/R-D3 case, 2026-07-21). This walks TYPED edges and generates the views ADR-0007 designed:
a LIVE/AMENDED/DEAD/OPEN ledger, a reconciliation view (unresolved conflicts surface on their
own), and a per-node "what touches this" map.

SOURCES (in order):
  1. notes/_decision-graph-seed-2026-07-21.json  — the audited seed (judgment half, Fable session)
  2. (post-inscription) inline `Edges:` lines in ledgers + ADR headers + DV front-matter — the
     parser hook exists (`parse_inline_edges`) but inscription waits on ADR-0012 acceptance.

EDGE GRAMMAR (ADR-0012 §2/§3): type(target[, k=v…]) with types
  supersedes · refines · subsumes · bounds · conflicts-with · diverges-from · verified-by · relates
Aliases normalised here, never rewritten in source: Extends->refines, gated_by->verified-by,
governs->bounds, Relates->relates.

GATE SEMANTICS (ADR-0012 §6 — anti-laundering per ADR-0007 §5: consistency, never validity):
  --strict exits non-zero on: conflicts-with lacking `resolution` · resolution=open ·
  a structural-edge target that resolves to no known node/rule/anchor.
  `resolution=queued` NEVER fails the gate — queued conflicts are DAVE'S to rule (routing rule 2);
  they are surfaced loudly in the reconciliation view instead. diverges-from is intentional by
  definition and is listed, never flagged.

Writes knowledge/_DECISION-GRAPH.md + knowledge/_decision-graph.json.
Run:  python3 knowledge/_build_decision_graph.py [--strict] [--selftest]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "notes", "_decision-graph-seed-2026-07-21.json")
OUT_MD = os.path.join(HERE, "_DECISION-GRAPH.md")
OUT_JSON = os.path.join(HERE, "_decision-graph.json")

STRUCTURAL = {"supersedes", "refines", "subsumes", "bounds", "conflicts-with", "diverges-from"}
EVIDENCE = {"verified-by"}
WEAK = {"relates"}
ALIASES = {"extends": "refines", "gated_by": "verified-by", "governs": "bounds"}
# targets that are legitimate endpoints without being seed nodes: guideline rules, files, methods
RULE_ID = re.compile(r"^[a-z]{2,6}\d{0,2}[a-z]?-\d{3}$")  # icon-011, col25-011, type26-013, dv-016, ctkb-015 …
FILEISH = re.compile(r"[/.]")


def load_seed():
    with open(SEED, encoding="utf-8") as f:
        seed = json.load(f)
    edges = []
    for e in seed.get("edges", []):
        e = dict(e)
        e["type"] = ALIASES.get(e["type"], e["type"])
        edges.append(e)
    return seed.get("nodes", {}), edges, seed.get("errata", [])


def parse_inline_edges():
    """Post-inscription hook: parse `Edges: type(target, k=v) · …` lines from ledgers/ADRs.
    Returns [] until inscription lands (ADR-0012 acceptance gates it). Kept so the interface
    is stable and the inscription diff can be verified against the seed."""
    return []


def classify(nodes, edges):
    """Lifecycle rollup: DEAD = whole-node supersedes inbound; AMENDED = claim-scoped supersedes
    inbound (invalidated-not-deleted); explicit node status wins where it says superseded."""
    inbound = {}
    for e in edges:
        inbound.setdefault(e.get("to"), []).append(e)
    state = {}
    for nid, meta in nodes.items():
        st = meta.get("status", "accepted")
        dead_hit = [e for e in inbound.get(nid, []) if e["type"] == "supersedes" and not e.get("claim")]
        claim_hits = [e for e in inbound.get(nid, []) if e["type"] == "supersedes" and e.get("claim")]
        if st == "superseded" or dead_hit:
            state[nid] = "DEAD"
        elif claim_hits or st == "amended":
            state[nid] = "AMENDED"
        elif st == "proposed":
            state[nid] = "OPEN"
        else:
            state[nid] = "LIVE"
    return state, inbound


def check(nodes, edges):
    """Gate findings: (severity, code, msg). severity ⚠ fails --strict; i is report-only."""
    findings = []
    known = set(nodes)
    for e in edges:
        t, to = e["type"], e.get("to", "")
        if t in STRUCTURAL and to not in known and not RULE_ID.match(to) and not FILEISH.search(to):
            # unresolvable structural target — allow named anchors ("X:Y" / "CHARTER.*") and
            # descriptive endpoints only for conflicts-with (the tension may be with a practice)
            if ":" not in to and "." not in to and t != "conflicts-with":
                findings.append(("⚠", "orphan-target",
                                 f"{e['from']} —{t}→ `{to}`: target resolves to no known node/rule/anchor."))
        if t == "conflicts-with":
            res = e.get("resolution")
            if not res:
                findings.append(("⚠", "conflict-unresolved",
                                 f"{e['from']} conflicts-with {to}: NO resolution recorded."))
            elif res == "open":
                findings.append(("⚠", "conflict-open",
                                 f"{e['from']} conflicts-with {to}: resolution=open."))
            elif res == "queued":
                findings.append(("i", "conflict-queued",
                                 f"{e['from']} conflicts-with {to} — QUEUED FOR DAVE: {e.get('claim', e.get('note', ''))[:100]}"))
    return findings


def what_touches(nodes, edges):
    adj = {}
    for e in edges:
        adj.setdefault(e["from"], {"out": [], "in": []})["out"].append(e)
        if e.get("to") in nodes:
            adj.setdefault(e["to"], {"out": [], "in": []})["in"].append(e)
    return adj


def fmt_edge(e, direction="out"):
    q = []
    for k in ("scope", "claim", "resolution", "reason", "ref"):
        if e.get(k):
            q.append(f"{k}={e[k]}")
    qs = f" ({'; '.join(q)})" if q else ""
    if direction == "out":
        return f"—{e['type']}→ {e.get('to')}{qs}"
    return f"{e['from']} —{e['type']}→{qs}"


def main():
    nodes, edges, errata = load_seed()
    edges += parse_inline_edges()
    state, inbound = classify(nodes, edges)
    findings = check(nodes, edges)
    adj = what_touches(nodes, edges)
    warns = [f for f in findings if f[0] == "⚠"]
    queued = [f for f in findings if f[1] == "conflict-queued"]
    diverges = [e for e in edges if e["type"] == "diverges-from"]

    by_state = {}
    for nid, st in state.items():
        by_state.setdefault(st, []).append(nid)

    L = ["# Decision graph — generated views (ADR-0012)", "",
         "*GENERATED by `_build_decision_graph.py` from the audited seed "
         "(`notes/_decision-graph-seed-2026-07-21.json`) — do not hand-edit. Consistency only, "
         "never validity (ADR-0007 §5): a clean graph is not a vouched one.*", "",
         f"**{len(nodes)} nodes · {len(edges)} edges · {len(warns)} gate warning(s) · "
         f"{len(queued)} conflict(s) queued for Dave · {len(diverges)} recorded deliberate divergence(s).**", ""]

    L.append("## ① Reconciliation view — conflicts + divergences")
    L.append("")
    if queued:
        L.append("### ★ QUEUED FOR DAVE (never auto-resolved)")
        for _, _, msg in queued:
            L.append(f"- 🟡 {msg}")
        L.append("")
    open_c = [f for f in findings if f[1] in ("conflict-unresolved", "conflict-open")]
    if open_c:
        L.append("### ⚠ UNRESOLVED (gate fails on these in --strict)")
        for _, _, msg in open_c:
            L.append(f"- ⚠ {msg}")
        L.append("")
    resolved = [e for e in edges if e["type"] == "conflicts-with" and e.get("resolution") in ("ruled", "interim", "deferred", "parked")]
    L.append(f"### Registered tensions with a recorded resolution ({len(resolved)})")
    for e in resolved:
        L.append(f"- {e['from']} ↔ {e['to']} — **{e['resolution']}**"
                 + (f" (ref: {e['ref']})" if e.get("ref") else "")
                 + (f" — {e.get('note','')[:90]}" if e.get("note") else ""))
    L.append("")
    L.append(f"### Deliberate divergences (intentional — the gate never flags these)")
    for e in diverges:
        L.append(f"- {e['from']} ⇹ {e['to']} — {e.get('reason','')[:140]}")
    L.append("")

    L.append("## ② Lifecycle ledger")
    L.append("")
    for st, label in (("LIVE", "LIVE"), ("AMENDED", "AMENDED — live with a dead claim (invalidated, not deleted)"),
                      ("DEAD", "DEAD — do not build on"), ("OPEN", "OPEN / proposed")):
        ids = sorted(by_state.get(st, []))
        if not ids:
            continue
        L.append(f"### {label} ({len(ids)})")
        for nid in ids:
            n = nodes[nid]
            extra = ""
            if st == "AMENDED":
                claims = [e.get("claim") for e in inbound.get(nid, []) if e["type"] == "supersedes" and e.get("claim")]
                if claims:
                    extra = f" — dead claim(s): {'; '.join(c for c in claims if c)}"
            if st == "DEAD":
                sups = [e["from"] for e in inbound.get(nid, []) if e["type"] == "supersedes"]
                if sups:
                    extra = f" — superseded by {', '.join(sups)}"
            L.append(f"- **{nid}** · {n.get('title','')}{extra}")
        L.append("")

    L.append("## ③ What-touches-this map (per node, inbound + outbound)")
    L.append("")
    for nid in sorted(adj, key=lambda x: (x.split("-")[0], x)):
        a = adj[nid]
        if not a["in"] and not a["out"]:
            continue
        L.append(f"**{nid}**")
        for e in a["out"]:
            L.append(f"  - {fmt_edge(e,'out')}")
        for e in a["in"]:
            L.append(f"  - ← {fmt_edge(e,'in')}")
        L.append("")

    L.append("## ④ Validation rollup (human-only; never derived)")
    vc = {}
    for nid, n in nodes.items():
        vc[n.get("validation", "unaudited")] = vc.get(n.get("validation", "unaudited"), 0) + 1
    L.append("")
    L.append(" · ".join(f"**{k}**: {v}" for k, v in sorted(vc.items())))
    if errata:
        L.append("")
        L.append("## ⑤ Errata (fix at next capture)")
        for e in errata:
            L.append(f"- **{e['id']}** — {e['what']}")
    L.append("")

    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L))
    json.dump({"nodes": nodes, "edges": edges, "state": state,
               "findings": [{"sev": s, "code": c, "msg": m} for s, c, m in findings]},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)

    print(f"decision graph: {len(nodes)} nodes, {len(edges)} edges -> {os.path.relpath(OUT_MD, ROOT)}")
    print(f"  states: " + " · ".join(f"{k} {len(v)}" for k, v in sorted(by_state.items())))
    for sev, code, msg in findings:
        print(f"  {sev} [{code}] {msg[:110]}")
    return len(warns)


def selftest():
    """Bite-test: an open conflict and an orphan structural target must each fail strict."""
    nodes = {"A": {"title": "a"}, "B": {"title": "b"}}
    bad1 = [{"from": "A", "type": "conflicts-with", "to": "B"}]                    # no resolution
    bad2 = [{"from": "A", "type": "conflicts-with", "to": "B", "resolution": "open"}]
    bad3 = [{"from": "A", "type": "supersedes", "to": "GHOST"}]                    # orphan target
    ok = [{"from": "A", "type": "conflicts-with", "to": "B", "resolution": "queued"},
          {"from": "A", "type": "diverges-from", "to": "B", "reason": "intentional"}]
    for name, es, want in (("unresolved", bad1, True), ("open", bad2, True),
                           ("orphan", bad3, True), ("queued+diverge", ok, False)):
        warns = [f for f in check(nodes, es) if f[0] == "⚠"]
        fired = bool(warns)
        assert fired == want, f"selftest {name}: expected fire={want}, got {fired}"
        print(f"  selftest {name}: {'fires' if fired else 'green'} ✓")
    print("selftest PASS — gate bites on unresolved/open/orphan; queued + diverges-from stay green")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    warns = main()
    sys.exit(warns if "--strict" in sys.argv else 0)
