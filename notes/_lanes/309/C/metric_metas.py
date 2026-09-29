"""#309 lane C - the Metric meta and the two alias seats (s308-D42, s309-D2).
metric.meta.json is built from kpi-tile.meta.json (the superset: the stat card's anatomy plus the
two optional slots), with the class vocabulary renamed as in the snippet and the stat card's
relationships, count and anti-patterns folded in. stat-card.meta.json and kpi-tile.meta.json become
thin alias seats (aliasOf component:metric, the s210-D5 seat: no spec, at most 14 keys). The prior
bytes of both are in git history at daf855ac. Run once."""
import json, re
C = "knowledge/components/"
kpi = json.load(open(C + "kpi-tile.meta.json", encoding="utf-8"))
st = json.load(open(C + "stat-card.meta.json", encoding="utf-8"))
TOK = r"(?<![A-Za-z0-9/_-])"
def ren(o):
    s = json.dumps(o, ensure_ascii=False)
    s = re.sub(TOK + r"kpi-tile(?![A-Za-z0-9_]|\.meta|\.reference)", "metric", s)
    s = re.sub(TOK + r"kpi-(?=[a-z])", "metric-", s)
    return json.loads(s)
RULE = ("s308-D42 (Dave, #308, by click): 'One block, Metric, with the trend as an optional slot; old names kept "
        "as aliases'. s309-D2 (Dave, #309, in chat, 21:37 BST): 'go', to 'Metric: rebuild it properly, one lane, "
        "canon and the 27 chart proofs re-run.'")
m = {}
m["name"] = "Metric"
m["category"] = "molecule"
m["kind"] = "block"
m["$status"] = ("RULED " + RULE + " Built #309 lane C from the KPI tile, the superset; Dave's eye owed on the "
                "with/without-trend render (notes/_lanes/309/C/metric-with-without-trend.png).")
m["purpose"] = ("One headline number as one block: label, value, delta and comparison period, with two optional "
                "slots - the TREND (the Chart-sparkline atom at its inline scale) and a hue-free target row. "
                "Without a series the trend slot is left out: that is the reading the stat card was. With a "
                "series the tile also shows HOW the number moved: the reading the KPI tile was. One tile, one "
                "claim; a board is a grid of these.")
m["$aliases"] = ("component:stat-card (the without-trend reading) and component:kpi-tile (the with-trend "
                 "reading) are alias seats of this meta (aliasOf, the s210-D5 seat). They hold no spec.")
for k in ("provides", "answers"):
    m[k] = kpi[k]
m["shape"] = st["shape"]
m["span"] = {"cols": {"min": st["span"]["cols"]["min"], "max": kpi["span"]["cols"]["max"]}}
m["priority"] = st["priority"]
m["when"] = ("shape = one-measure × value-and-delta AND delta != none — the default of the role: label · value · "
             "delta · period, one block (s308-D42). The trend slot is filled only when a series exists to show "
             "(s247-D3 / DP-08: no series, no spark); yields to Chart-bullet (when: \"a target or performance band "
             "is the point, not the delta\") and to runway-bar (when: \"the number is 'money vs what is already "
             "scheduled'\").")
m["with"] = kpi["with"]
m["$merged"] = ("#309 lane C, on " + RULE + " The KPI tile was the superset (the stat card's anatomy verbatim plus "
                "the spark and target slots, a state model and two affordance rivals), so its spec is this meta's "
                "spec, with its class vocabulary renamed kpi-* -> metric-*. From the stat card: its relationships, "
                "its span floor (2 columns), its priority (60, the role's default) and its group count. The stat "
                "card's arrow sat on the FILL seat (rag/success / rag/error); Metric's arrow is on the INK seat, as "
                "Dave ruled for the tile at #261 K3 ('We need to use the dark versions of the colours on the "
                "arrows') - the KPI tile's own header had said the stat card must follow. Both prior metas are in "
                "git history at daf855ac. Before #309: " + kpi["$floated"])
for k in ("props", "variants", "slots", "tokens"):
    m[k] = ren(kpi[k])
m["slots"]["spark"]["$status"] = "THE TREND - an optional slot (s308-D42); heights 28 compact / 40 default / 56 hero (#261)"
m["slots"]["target"]["$status"] = "optional; drawn #261, Dave's eye owed"
m["relationships"] = {
    "livesInside": kpi["relationships"]["livesInside"] + st["relationships"]["livesInside"],
    "mustNotNeighbour": st["relationships"]["mustNotNeighbour"],
    "commonPatterns": kpi["relationships"]["commonPatterns"] + st["relationships"]["commonPatterns"],
}
for k in ("accessibility",):
    m[k] = ren(kpi[k])
m["antiPatterns"] = ren(kpi["antiPatterns"]) + [a for a in st["antiPatterns"] if a not in kpi["antiPatterns"]]
m["tokenValidation"] = ren(kpi["tokenValidation"])
m["provenance"] = dict(ren(kpi["provenance"]))
m["provenance"]["code_path"] = "knowledge/snippets/Metric.reference.html"
m["provenance"]["$note"] = ("#309 lane C: snippets/Kpi-tile.reference.html renamed to Metric.reference.html (git mv) "
                            "and its vocabulary renamed; the drawing is unchanged. Before: " + kpi["provenance"]["$note"])
for k in ("interactive", "stateModel", "responsive", "dimensions"):
    m[k] = ren(kpi[k])
m["count"] = kpi["count"] + st["count"]
m["edges"] = ren(kpi["edges"])
m["edges"]["renderedBy"] = [{"ref": "snippet:Metric.reference.html"}]

def alias(src, reading, why, extra_purpose):
    a = {}
    a["name"] = src["name"]
    a["category"] = src["category"]
    a["kind"] = src["kind"]
    a["purpose"] = (src["name"].upper() + " IS AN ALIAS OF METRIC - the " + reading + " reading. " + extra_purpose +
                    " The geometry, tokens, states and full spec live ONCE, in metric.meta.json; this record "
                    "keeps the old slug a findable, selectable identity (" + RULE + ").")
    a["aliasOf"] = {"component": "component:metric", "reading": reading, "why": why}
    a["relationships"] = src["relationships"]
    a["provenance"] = {"source": src["provenance"].get("source", "gap-report"),
                       "figma_node": src["provenance"].get("figma_node", ""),
                       "code_path": "knowledge/snippets/Metric.reference.html"}
    a["$aliasRecord"] = ("ENACTED #309 lane C per s308-D42 and s309-D2. This file WAS the full " + src["name"] +
                         " spec; every fact it held is in metric.meta.json or superseded there (see its $merged), "
                         "and the prior bytes are in git history at daf855ac. The alias seat holds no spec, by "
                         "the s210-D5 size fence in meta.schema.json.")
    a["$relationshipsRetained"] = ("Kept as they were: they are KG wiring, not spec (the s210-D5 precedent, "
                                   "progress-bar.meta.json), so the lines that name this slug keep resolving.")
    a["edges"] = src["edges"]
    return a

sc = alias(st, "without trend",
           "A Metric whose trend slot is empty: the number and whether it moved against one prior period. "
           "Pick it when the reader needs the figure, not the shape of its history.",
           "A Metric with no series.")
sc["$snippetDisposition"] = ("snippets/Stat-card.reference.html is KEPT, byte-untouched: pages built before the "
                             "merge carry .cn-stat-card and its markup - the #227 banking demo "
                             "(dashboards/international-banking-dashboard.canon.html, measured by "
                             "_validate_geometry.py and _validate_own_size.py), the provenance-receipt tests and "
                             "the progress dashboard. Moving them onto Metric's markup changes how they look (the "
                             "arrow moves to the ink seat), which is Dave's to see; until then canon keeps its "
                             "block and the showroom its page.")
kt = alias(kpi, "with trend",
           "A Metric with its trend slot filled: the number, how it moved, and the SHAPE of the movement over "
           "twelve points. Pick it when the reader needs to see how the number moved.",
           "A Metric with a series in its trend slot.")
kt["$snippetDisposition"] = ("snippets/Kpi-tile.reference.html is now snippets/Metric.reference.html (git mv, #309); "
                             "its canon scope .cn-kpi-tile is now .cn-metric, and showroom/kpi-tile.html is "
                             "showroom/metric.html.")
for a in (sc, kt):
    assert len(a) <= 14, len(a)
def dump(p, o):
    open(p, "w", encoding="utf-8").write(json.dumps(o, indent=2, ensure_ascii=False) + "\n")
dump(C + "metric.meta.json", m)
dump(C + "stat-card.meta.json", sc)
dump(C + "kpi-tile.meta.json", kt)
print("metric keys", len(m), "stat-card", len(sc), "kpi-tile", len(kt))
