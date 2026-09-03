#!/usr/bin/env python3
"""L3 #245 — the groupsWith POPULATION PROPOSAL for the bento template and its group members.

⛔ Writes NO live meta. Reads knowledge/snippets/Template-dashboard-bento.reference.html (the REAL
artefact) to MEASURE the groups and their members, then writes:
  knowledge/_tmp/l3-245/population-proposal.json   {file -> {edges:{groupsWith:[...]}}, provenance}
  knowledge/_tmp/l3-245/schema-arms.txt            live 136/136 (LIVE + PROPOSED schema) · proposals N/N
                                                   (PROPOSED) · proposals RED under LIVE (the change is
                                                   needed) · planted mutants red · controls green
Grouping criterion is rB's, not mine: a group = members that answer ONE question the user came with;
the shared question is read off each group <section>'s aria-label, never invented.
"""
import copy, glob, json, os, re, sys
import jsonschema

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
COMP = os.path.join(ROOT, "knowledge", "components")
SNIP = os.path.join(ROOT, "knowledge", "snippets", "Template-dashboard-bento.reference.html")
OUT = os.path.dirname(os.path.abspath(__file__))
LIVE_SCHEMA = os.path.join(COMP, "meta.schema.json")
PROP_SCHEMA = os.path.join(OUT, "meta.schema.proposed.json")

CONTENT_MARKERS = {           # what a stat-card MODULE carries, by the class the snippet uses
    "chart-bar": r'class="dv"[^>]*data-dv-type="column"',
    "summary": r'<dl class="summary"',
    "status-indicator": r'class="status (?:warn|err|inf|ok)"',
}


def strip_comments(html):
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def measure_groups():
    html = open(SNIP, encoding="utf-8").read()
    lines = html.splitlines()
    body = strip_comments(html[html.index('<main class="tpl-page"'):html.index("</main>")])
    groups = []
    for m in re.finditer(r'<section class="([^"]*\btpl-group-([a-z]+)\b[^"]*)"[^>]*?data-c="(\d)"'
                         r'[^>]*?aria-label="([^"]*)"', body):
        seg = body[m.end(): body.index("</section>", m.end())]
        tiles = re.findall(r'<div class="c-bento__tile ([a-z-]+)[^"]*"[^>]*?data-c="(\d)"', seg)
        contents = [k for k, rx in CONTENT_MARKERS.items() if re.search(rx, seg)]
        counts = {k: len(re.findall(rx, seg)) for k, rx in CONTENT_MARKERS.items() if re.search(rx, seg)}
        # line numbers of the <section> in the real file, for the $note
        needle = 'tpl-group-%s"' % m.group(2)
        ln = next(i + 1 for i, l in enumerate(lines) if needle in l and "<section" in l)
        groups.append({
            "class": "tpl-group-" + m.group(2), "role_word_today": m.group(2),
            "shared_question": m.group(4), "span": int(m.group(3)), "line": ln,
            "tiles": [{"scope": t[0], "data_c": int(t[1])} for t in tiles],
            "tile_scopes": sorted(set(t[0] for t in tiles)),
            "contents": counts,
        })
    return groups


def proposals(groups):
    """The edges, one dict per meta file. Every $note carries the line it was measured at."""
    g = {x["class"]: x for x in groups}
    kpi, chart, rail = g["tpl-group-kpi"], g["tpl-group-chart"], g["tpl-group-rail"]
    assert kpi["tile_scopes"] == ["kpi-tile"] and len(kpi["tiles"]) == 4
    assert chart["tile_scopes"] == ["stat-card"] and len(chart["tiles"]) == 1 and chart["contents"] == {"chart-bar": 1}
    assert rail["tile_scopes"] == ["stat-card"] and len(rail["tiles"]) == 2 and set(rail["contents"]) == {"summary", "status-indicator"}
    S = "knowledge/snippets/Template-dashboard-bento.reference.html"
    P = {}
    P["kpi-tile"] = [{
        "ref": "component:kpi-tile",
        "$note": "PROPOSED #245 L3. Group '%s' (%s:%d): FOUR Kpi-tiles answer one question - how did "
                 "this month go. Uniform in kind (rB C2), so the edge is a SELF-edge: a KPI groups "
                 "with the other KPIs of its period, never with a chart because it is 'a KPI'."
                 % (kpi["shared_question"], S, kpi["line"])}]
    P["stat-card"] = [{
        "ref": "component:stat-card",
        "$note": "PROPOSED #245 L3. Group '%s' (%s:%d): TWO Stat-card modules (Balances - Needs "
                 "attention) stacked, one question - where do I stand. MEASURED: the MODULE is the "
                 "group member; what it carries (Summary, Status-indicator) rides inside it."
                 % (rail["shared_question"], S, rail["line"])}]
    P["chart-bar"] = [{
        "ref": None,
        "$note": "PROPOSED #245 L3. Group '%s' (%s:%d) holds ONE module - a Stat-card carrying "
                 "Chart-bar's column specimen. One member is a tile, not a group, under Carbon's "
                 "framing (rB Q3, Dave's - NOT ruled here). ref:null because there is no partner to "
                 "point at until he says whether a one-member group is legal."
                 % (chart["shared_question"], S, chart["line"])}]
    P["summary"] = [{
        "ref": "component:status-indicator",
        "$note": "PROPOSED #245 L3. Inside group '%s' (%s:%d): Balances (Summary) beside Needs "
                 "attention (Status-indicator chips) - the same question, where do I stand."
                 % (rail["shared_question"], S, rail["line"])}]
    P["status-indicator"] = [{
        "ref": "component:summary",
        "$note": "PROPOSED #245 L3. The mirror of summary.edges.groupsWith -> component:summary, "
                 "same group '%s' (%s:%d). Symmetric by proposal; whether the edge is stored once or "
                 "twice is a question, not a ruling." % (rail["shared_question"], S, rail["line"])}]
    P["template-dashboard-bento"] = [{
        "ref": None,
        "$note": "PROPOSED #245 L3. Group '%s' (%s:%d) - members %s; shared question read off the "
                 "section's aria-label. ref:null: a GROUP is not a node in the edge grammar "
                 "(component|pattern|context|snippet|ruling) and this lane does not invent a "
                 "'group:' prefix - Dave's eye. Today's class: %s."
                 % (x["shared_question"], S, x["line"],
                    " + ".join("component:" + c for c in (["kpi-tile"] if x["class"] == "tpl-group-kpi"
                                                         else sorted(x["contents"]))),
                    x["class"])} for x in (kpi, chart, rail)]
    return P


def validator(path):
    s = json.load(open(path, encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(s)
    return jsonschema.Draft7Validator(s)


def valid(V, doc):
    return not list(V.iter_errors(doc))


def main():
    groups = measure_groups()
    P = proposals(groups)
    live_v, prop_v = validator(LIVE_SCHEMA), validator(PROP_SCHEMA)
    metas = sorted(f for f in glob.glob(os.path.join(COMP, "*.meta.json"))
                   if not os.path.basename(f).startswith("EXAMPLE"))
    example = [f for f in glob.glob(os.path.join(COMP, "*.meta.json")) if os.path.basename(f).startswith("EXAMPLE")]
    lines, arms = [], []

    def arm(name, cond):
        arms.append((name, cond)); lines.append("%s  %s" % ("GREEN" if cond else "RED  ", name))

    # 1 · live metas, both schemas
    ok_live = sum(valid(live_v, json.load(open(f))) for f in metas)
    ok_prop = sum(valid(prop_v, json.load(open(f))) for f in metas)
    lines.append("live metas (EXAMPLE-* excluded, %d file(s) so excluded): %d" % (len(example), len(metas)))
    lines.append("  against LIVE schema:     %d/%d valid" % (ok_live, len(metas)))
    lines.append("  against PROPOSED schema: %d/%d valid" % (ok_prop, len(metas)))
    lines.append("  EXAMPLE-button.meta.json against LIVE schema: %s (pre-existing, not this lane's)"
                 % ("valid" if valid(live_v, json.load(open(example[0]))) else "RED - 'tokenValidation' is a required property"))
    arm("A · every live meta validates against the PROPOSED schema (by addition)", ok_prop == len(metas) == ok_live)
    # 2 · proposals applied in memory
    applied, n_edges = {}, 0
    for stem, edges in P.items():
        m = json.load(open(os.path.join(COMP, stem + ".meta.json"), encoding="utf-8"))
        m2 = copy.deepcopy(m)
        m2.setdefault("edges", {})["groupsWith"] = edges
        applied[stem] = m2; n_edges += len(edges)
    ok_applied = sum(valid(prop_v, m) for m in applied.values())
    red_live = sum(not valid(live_v, m) for m in applied.values())
    lines.append("proposals: %d meta file(s), %d groupsWith edge(s) (ref set %d · ref:null %d)"
                 % (len(P), n_edges, sum(e["ref"] is not None for es in P.values() for e in es),
                    sum(e["ref"] is None for es in P.values() for e in es)))
    arm("B · %d/%d proposal-applied metas validate against the PROPOSED schema" % (ok_applied, len(applied)), ok_applied == len(applied))
    arm("C · %d/%d proposal-applied metas are RED against the LIVE schema (edges is additionalProperties:false - the change IS required)" % (red_live, len(applied)), red_live == len(applied))
    # 3 · every non-null ref resolves to a meta file that exists
    refs = [e["ref"] for es in P.values() for e in es if e["ref"]]
    resolves = all(os.path.exists(os.path.join(COMP, r.split(":", 1)[1] + ".meta.json")) for r in refs)
    arm("D · %d non-null refs resolve to an existing knowledge/components/<stem>.meta.json" % len(refs), resolves)
    # 4 · mutants (each must be RED under the PROPOSED schema)
    base = applied["kpi-tile"]
    def mut(fn):
        m = copy.deepcopy(base); fn(m); return not valid(prop_v, m)
    arm("M1 · ref 'group:this-month' (not in the node-id grammar) is RED", mut(lambda m: m["edges"]["groupsWith"][0].__setitem__("ref", "group:this-month")))
    arm("M2 · an extra key 'role' on the edge is RED (edge form is closed)", mut(lambda m: m["edges"]["groupsWith"][0].__setitem__("role", "lead")))
    arm("M3 · an edge without 'ref' is RED", mut(lambda m: m["edges"]["groupsWith"][0].pop("ref")))
    arm("M4 · groupsWith as a bare string is RED", mut(lambda m: m["edges"].__setitem__("groupsWith", "kpi-tile")))
    arm("M5 · numeric $note is RED", mut(lambda m: m["edges"]["groupsWith"][0].__setitem__("$note", 7)))
    arm("M6 · a misspelt 'groupWith' key is RED", mut(lambda m: m["edges"].__setitem__("groupWith", m["edges"].pop("groupsWith"))))
    def ctl(fn):
        m = copy.deepcopy(base); fn(m); return valid(prop_v, m)
    arm("K1 · control: ref:null + $note is GREEN", ctl(lambda m: m["edges"]["groupsWith"][0].__setitem__("ref", None)))
    arm("K2 · control: empty groupsWith [] is GREEN", ctl(lambda m: m["edges"].__setitem__("groupsWith", [])))
    arm("K3 · control: edge with ref only (no $note) is GREEN", ctl(lambda m: m["edges"]["groupsWith"][0].pop("$note")))
    reds = [n for n, c in arms if not c]
    lines.append("ARMS: %d · green %d · red %d" % (len(arms), len(arms) - len(reds), len(reds)))
    txt = "\n".join(lines) + "\n"
    open(os.path.join(OUT, "schema-arms.txt"), "w", encoding="utf-8").write(txt)
    doc = {
        "$what": "PROPOSED groupsWith edges for the bento template and its group members. NOT applied to any live meta.",
        "$ruling": "s234-D4",
        "$measured_from": "knowledge/snippets/Template-dashboard-bento.reference.html (comments stripped, <main> only)",
        "$schema": "knowledge/_tmp/l3-245/meta.schema.proposed.json",
        "groups_measured": groups,
        "proposals": {stem + ".meta.json": {"edges": {"groupsWith": edges}} for stem, edges in P.items()},
        "counts": {"groups": len(groups), "tiles": sum(len(g["tiles"]) for g in groups),
                   "member_metas": len(P) - 1, "meta_files_touched_if_applied": len(P), "edges": n_edges},
    }
    open(os.path.join(OUT, "population-proposal.json"), "w", encoding="utf-8").write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(txt)
    return 1 if reds else 0


if __name__ == "__main__":
    sys.exit(main())
