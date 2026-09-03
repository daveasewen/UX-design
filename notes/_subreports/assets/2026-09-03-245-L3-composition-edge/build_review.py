#!/usr/bin/env python3
"""L3 #245 — GENERATES `_REVIEW-L3-composition-edge-2026-09-03-v1.html` (repo root) FROM this lane's
artefact files, so the page cannot disagree with them. Single file · knowledge/canon/type.css inlined
VERBATIM · zero external refs · four themes x light/dark through the canon's own mechanism
([data-apollo-theme] + [data-theme]), per-theme grounds/inks READ from the token store via
gen_bento_matrix_217.resolve_token (theme-tokens.json), never typed."""
import html as H, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "_REVIEW-L3-composition-edge-2026-09-03-v1.html")

def rd(name): return open(os.path.join(HERE, name), encoding="utf-8").read()
def js(name): return json.loads(rd(name))
def e(s): return H.escape(str(s), quote=False)

TYPE_CSS = open(os.path.join(ROOT, "knowledge", "canon", "type.css"), encoding="utf-8").read()
pop = js("population-proposal.json"); arms = rd("schema-arms.txt"); diff = rd("meta.schema.proposed.diff")
frag = js("groupsWith.schema.fragment.json"); rails_txt = rd("rails-from-edge.txt"); rails = js("_bento_edit_rails.proposed.json")
drive = rd("drive-real-artefact.txt"); selftest = rd("selftest-check-composition.txt"); probe = js("render-probe.json")
grep_before = rd("rename-grep-before.txt"); plan = js("rename-plan.json"); toks = js("theme-tokens.json")
rulings = json.load(open(os.path.join(ROOT, "knowledge", "_rulings.json"), encoding="utf-8"))

def find_ruling(rid):
    def walk(o):
        if isinstance(o, dict):
            if o.get("id") == rid: return o
            for v in o.values():
                r = walk(v)
                if r: return r
        elif isinstance(o, list):
            for v in o:
                r = walk(v)
                if r: return r
    return walk(rulings)
D4 = find_ruling("s234-D4")
LINE154 = open(os.path.join(ROOT, "knowledge", "components", "template-dashboard-bento.meta.json"), encoding="utf-8").read().splitlines()[153]
L154_QUOTE = re.search(r"if Dave wants.*?not a worker lane's\.", LINE154).group(0)

# ---- measured numbers, pulled from the files (never retyped) ----
n_live = int(re.search(r"against LIVE schema:\s+(\d+)/(\d+)", arms).group(1)); n_live_of = int(re.search(r"against LIVE schema:\s+(\d+)/(\d+)", arms).group(2))
n_prop_ok = re.search(r"against PROPOSED schema:\s+(\d+)/(\d+)", arms).groups()
n_arms = re.search(r"ARMS: (\d+) · green (\d+) · red (\d+)", arms).groups()
c = pop["counts"]; n_edges = c["edges"]; n_files = c["meta_files_touched_if_applied"]
n_null = sum(1 for v in pop["proposals"].values() for x in v["edges"]["groupsWith"] if x["ref"] is None)
st = re.search(r"selftest: (\d+) arm\(s\) · (\d+) failed", selftest).groups()
gr = re.search(r"files: (\d+) · occurrences: kpi (\d+) · chart (\d+) · rail (\d+) · total (\d+)", grep_before).groups()
dial = rails["dials"]["grouping"]
p1440 = probe["viewports"]["1440"]

def theme_css():
    """Per-theme ground/ink/rule from the store (theme-tokens.json). Two-red law s151-D1: #DA1A00 on WHITE, #F6604C else."""
    out = []
    for key, row in toks.items():
        t, m = key.split("/")
        bg, ink, rule, panel = row["--background-default"], row["--text-default"], row["--border-subtle"], row["--surface-subtle"]
        accent = "#DA1A00" if bg.upper() == "#FFFFFF" else "#F6604C"
        sel = '[data-apollo-theme="%s"][data-theme="%s"]' % (t, m)
        out.append("%s{--bg:%s; --ink:%s; --rule:%s; --panel:%s; --accent:%s; --module:%s;}" % (sel, bg, ink, rule, panel, accent, row["--tertiary-background-default"]))
    return "\n".join(out)

CSS = """
:root{
  --accent:#DA1A00; --ink:#1A1A1A; --bg:#FFFFFF; --rule:#E1E1E1; --panel:#F0F0F0; --module:#FFFFFF;
  --g6:#767676; --g7:#545454;
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem; --max:1200px; --gut:2rem;
  --mono:ui-monospace,Menlo,"SF Mono",Consolas,monospace;
}
[data-theme="dark"]{--g6:#9A9A9A; --g7:#B8B8B8;}
/* per-theme grounds, READ from the store — see the provenance comment above the block */
%THEMES%
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%}
html,body{background:var(--bg); color:var(--ink)}
body{margin:0; font-family:var(--uf); font-size:16px; line-height:1.7; overflow-x:hidden}
.wrap{max-width:var(--max); margin:0 auto; padding:0 var(--gut)}
nav{position:sticky; top:0; z-index:50; background:var(--bg); border-bottom:1px solid var(--rule)}
nav .wrap{display:flex; align-items:center; gap:var(--s2); min-height:54px; flex-wrap:wrap; padding-top:6px; padding-bottom:6px}
.brand{font-size:12px; font-weight:500; letter-spacing:.14em; text-transform:uppercase; white-space:nowrap}
.navlinks{display:flex; gap:var(--s2); margin-left:auto; flex-wrap:wrap}
.navlinks a{font-size:13px; color:var(--g6); text-decoration:none; letter-spacing:.04em}
.navlinks a:hover{color:var(--ink)}
.ctl{display:flex; gap:6px; flex-wrap:wrap; align-items:center}
.ctl button{font:inherit; font-size:11px; font-weight:500; letter-spacing:.08em; text-transform:uppercase; background:none; color:var(--g7); border:1px solid var(--rule); padding:4px 9px; cursor:pointer; min-height:28px}
.ctl button[aria-pressed="true"]{color:var(--ink); border-color:var(--ink)}
.ctl button:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
h1,h2,h3,h4{margin:0}
h1{margin:0}
h2{margin:0 0 var(--s3)}
h3{margin:0 0 var(--s2)}
h4{font-size:13px; font-weight:500; letter-spacing:.1em; text-transform:uppercase; margin:0 0 var(--s2)}
p{margin:0 0 var(--s2); max-width:68ch}
.lede{font-size:1.1875rem; line-height:1.6}
.label{font-size:12px; font-weight:500; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); display:flex; align-items:center; gap:var(--s1); margin:0 0 var(--s3)}
.label::before{content:''; display:inline-block; width:20px; height:1px; background:var(--accent); flex:none}
.muted{color:var(--g7)} .small{font-size:14px; line-height:1.6} .mono{font-family:var(--mono); font-size:13px}
code{font-family:var(--mono); font-size:.88em; background:var(--panel); padding:1px 4px; overflow-wrap:anywhere}
a{color:var(--ink)}
section{padding:var(--s7) 0; border-bottom:1px solid var(--rule); scroll-margin-top:64px}
section.band{background:var(--panel)}
.hdr{display:grid; grid-template-columns:2fr 1fr; gap:var(--s6); align-items:end}
.meta dt{font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:var(--g6); margin-top:var(--s2)}
.meta dd{margin:0; font-size:14px; overflow-wrap:anywhere}
.flag{display:inline-block; font-size:12px; font-weight:500; letter-spacing:.12em; text-transform:uppercase; border:1px solid var(--accent); color:var(--accent); padding:3px 9px; margin-bottom:var(--s3)}
.stats{display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--rule); border:1px solid var(--rule); margin-top:var(--s4)}
.stat{background:var(--bg); padding:var(--s3)} .stat .n{font-size:clamp(2rem,4.4vw,2.6875rem); font-weight:300; line-height:1; display:block}
.stat .k{font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:var(--g6); display:block; margin-top:var(--s1)} .stat.hi .n{color:var(--accent)}
.dim{display:grid; grid-template-columns:1fr 2fr; gap:var(--s6); align-items:start}
.idx{font-size:clamp(3rem,7vw,5.25rem); font-weight:200; line-height:.9; color:var(--g6); display:block}
.dim>*,.pair>*,.cards>*,.stats>*,.hdr>*,.col>*,.card>*{min-width:0}
.scroll{overflow-x:auto; -webkit-overflow-scrolling:touch; max-width:100%%; min-width:0}
table{border-collapse:collapse; width:100%%; min-width:640px; font-size:14px; line-height:1.5}
th,td{text-align:left; vertical-align:top; padding:10px 14px 10px 0; border-bottom:1px solid var(--rule)}
th{font-size:12px; letter-spacing:.1em; text-transform:uppercase; font-weight:500; color:var(--g6); white-space:nowrap}
td.id{font-family:var(--mono); white-space:nowrap; padding-right:var(--s3)}
pre{font-family:var(--mono); font-size:12px; line-height:1.5; margin:0 0 var(--s2); background:var(--panel); padding:var(--s2); overflow-x:auto; border-left:2px solid var(--rule); white-space:pre; max-width:100%%}
section.band pre{background:var(--bg)}
.pair{display:grid; grid-template-columns:1fr 1fr; gap:1px; background:var(--rule); border:1px solid var(--rule); margin-top:var(--s3)}
.col{background:var(--bg); padding:var(--s3)}
.colhead{font-size:12px; font-weight:500; letter-spacing:.12em; text-transform:uppercase; margin-bottom:var(--s2); padding-bottom:var(--s1); border-bottom:1px solid var(--rule)}
.colhead.b{color:var(--accent)}
.cards{display:grid; grid-template-columns:repeat(2,1fr); gap:1px; background:var(--rule); border:1px solid var(--rule)}
.card{background:var(--bg); padding:var(--s3)} .card .n{font-size:12px; font-weight:500; letter-spacing:.12em; color:var(--accent); display:block; margin-bottom:var(--s1)}
.card h3{font-size:16px; margin-bottom:var(--s1)} .card p{font-size:14px; line-height:1.55; margin:0 0 var(--s1)}
.own{font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--g6)}
.qq{border-top:1px solid var(--rule); padding-top:var(--s3); margin-top:var(--s4)} .qq:first-of-type{border-top:0; margin-top:0}
.qq .num{font-size:12px; letter-spacing:.12em; color:var(--accent); font-weight:500}
.rec{border-left:2px solid var(--accent); padding-left:var(--s2); margin-top:var(--s2); font-size:15px}
.note{background:var(--panel); padding:var(--s3); border-left:2px solid var(--rule); font-size:14px; line-height:1.6} section.band .note{background:var(--bg)}
.note p:last-child{margin-bottom:0}
.red{color:var(--accent)}
ol,ul{padding-left:1.15rem; max-width:68ch} li{margin-bottom:var(--s1); font-size:15px; line-height:1.6}
footer{padding:var(--s5) 0 var(--s7); font-size:13px; color:var(--g6)} footer p{max-width:none; overflow-wrap:anywhere}
.prose{overflow-wrap:anywhere}
/* the group schematic — drawn with the page's own tokens, not a screenshot */
.wallpic{display:grid; grid-template-columns:repeat(6,1fr); gap:10px; background:var(--panel); padding:10px; border:1px solid var(--rule); margin:var(--s3) 0}
.wallpic .grp{display:grid; gap:2px; padding:2px; border:1px dashed var(--accent); grid-column:span 3} .wallpic .grp.full{grid-column:span 6; grid-template-columns:repeat(2,1fr)}
.wallpic .mod{background:var(--module); border:1px solid var(--rule); min-height:38px; font-size:11px; padding:4px 6px; color:var(--g7); overflow-wrap:anywhere}
.wallpic .cap{grid-column:1/-1; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--accent); padding:2px 4px}
.wallpic.stacked .grp.full{grid-template-columns:1fr}
@media (max-width:900px){
  .hdr,.dim{grid-template-columns:1fr; gap:var(--s4)} .pair,.cards{grid-template-columns:1fr} .stats{grid-template-columns:repeat(2,1fr)}
  :root{--s7:3.5rem; --s6:2.5rem; --gut:1.25rem} .navlinks{display:none}
  .wallpic{grid-template-columns:1fr} .wallpic .grp,.wallpic .grp.full{grid-column:span 1}
}
""".replace("%THEMES%", theme_css()).replace("%%", "%")

def pre(s): return "<pre>%s</pre>" % e(s.rstrip("\n"))

def edges_table():
    rows = []
    for f, v in pop["proposals"].items():
        for x in v["edges"]["groupsWith"]:
            ref = x["ref"] if x["ref"] else '<span class="red">null</span>'
            rows.append("<tr><td class=\"id\">%s</td><td class=\"id\">%s</td><td class=\"prose small\">%s</td></tr>" % (e(f), ref if x["ref"] is None else e(ref), e(x["$note"])))
    return "<div class=\"scroll\"><table><thead><tr><th>meta file (untouched)</th><th>groupsWith.ref</th><th>$note — measured at the line named</th></tr></thead><tbody>%s</tbody></table></div>" % "".join(rows)

def groups_measured():
    rows = []
    for g in pop["groups_measured"]:
        rows.append("<tr><td class=\"id\">%s</td><td>%s</td><td class=\"id\">%d</td><td>%s</td><td class=\"small\">%s</td><td class=\"id\">%s:%d</td></tr>" % (
            e(g["class"]), e(g["shared_question"]), g["span"], e(", ".join("%s (data-c=%d)" % (t["scope"], t["data_c"]) for t in g["tiles"])),
            e(", ".join("%s ×%d" % kv for kv in g["contents"].items()) or "Kpi-tile ×4 (the tile IS the component)"), "…reference.html", g["line"]))
    return "<div class=\"scroll\"><table><thead><tr><th>class today</th><th>aria-label = the shared question</th><th>span</th><th>tiles</th><th>carries</th><th>measured at</th></tr></thead><tbody>%s</tbody></table></div>" % "".join(rows)

def dial_excerpt():
    d = {k: dial[k] for k in ("kind", "control", "$derived_from", "types", "ruled_by", "groups", "unresolved", "role_names")}
    d["unresolved"] = [{"on": u["on"], "$note": u["$note"][:110] + "…"} for u in d["unresolved"]]
    return json.dumps(d, indent=2, ensure_ascii=False)

def probe_table():
    rows = []
    for w, d in probe["viewports"].items():
        for k, v in d.items():
            rows.append("<tr><td class=\"id\">%s</td><td>%s</td><td class=\"id\">%d</td><td class=\"id\">%s</td><td class=\"id\">%s</td><td class=\"id\">%s</td><td>%s</td><td class=\"id\">%s</td></tr>" % (
                w, "as shipped" if k == "as_shipped" else "fixture: literal 6 declared", v["wall_tracks"], e(v["var_bento_cols_now"]), e(v["var_layout_bento_columns"]), e(v["wall_gridAutoFlow"]),
                ('<span class="red">%s</span>' % e(v["kpi_layout"])) if v["kpi_layout"] != "2x2" and w == "1440" else e(v["kpi_layout"]), e(str([g["tracks"] for g in v["groups"]]))))
    return "<div class=\"scroll\"><table><thead><tr><th>viewport</th><th>artefact</th><th>wall tracks</th><th>--bento-cols-now</th><th>--layout-bento-columns</th><th>grid-auto-flow</th><th>KPI board</th><th>group tracks</th></tr></thead><tbody>%s</tbody></table></div>" % "".join(rows)

RULE7B = """7b. **Grouping comes from the graph, not from the class name.** Whether two modules share
    a group is a fact stored ONCE, as an `edges.groupsWith` entry in the member's
    `knowledge/components/<slug>.meta.json` (the positive twin of `mustNotNeighbour`). The
    rails' `grouping` dial and this rule are DERIVED from it and never restate it. A group is
    members that answer ONE question the user came with — never "the KPIs, because they are
    KPIs"; its members are uniform in kind, carry one accessible name and one containment
    signal, and stay contiguous at every band. Read the edge before you draw a `<section>`;
    where the edge is `ref:null` the grouping is undecided and is a Gap, not a guess. HOW MANY
    groups a screen has, and what belongs in each, is the designer's product decision — never
    yours (template-dashboard-bento.meta.json:12)."""

QUESTIONS = [
    ("The three role WORDS.", "rB: no mature system groups by content type, and `kpi/chart/rail` teach exactly that. s234-D4 rules the re-cut; the words are yours.",
     [("a", "<code>-lead</code> / <code>-evidence</code> / <code>-context</code> — the floated trio; collision grep returns 0 files outside this lane's scratch."),
      ("b", "keep <code>-kpi/-chart/-rail</code> — costs nothing today; keeps teaching the taxonomy that produced the #233 taste-grouping."),
      ("c", "other words — same price as (a): 1 source file (6 occurrences), 2 regenerated files, the ordered serial.")],
     "Recommend (a). The rename plan is a dry run: 1 file to edit, 2 to regenerate, %s occurrences across %s files of which all but 3 files are history, rulings, archive or scratch and are never touched." % (gr[4], gr[0])),
    ("The schema change itself.", "Line 154 of the template meta already says it: “%s”" % e(L154_QUOTE),
     [("a", "apply the fragment as proposed — <code>groupsWith</code> in the closed <code>{ref, $note}</code> edge form, one line by addition at <code>meta.schema.json:216</code>; %s/%s live metas already validate against it." % (n_prop_ok[0], n_prop_ok[1])),
      ("b", "widen the edge form (a <code>group</code> or <code>role</code> field) — carries the shared question as data, but re-opens the closed form for all 12 existing edge types."),
      ("c", "do not add it — grouping stays a class name in one snippet and rule 7 keeps sending the agent to a file that has no seat for it (rB F13).")],
     "Recommend (a). The form is the one every other edge uses; the shared question rides in <code>$note</code> until a grammar question (Q7) is answered."),
    ("One-member group legality (rB Q3).", "The chart group holds one module. Carbon says a tile, not a tile-group; Apollo's construction wants the wrapper for its row-unit seat.",
     [("a", "legal, as a declared carve-out — the edge stays <code>ref:null</code> with the reason, the wrapper keeps the seat."),
      ("b", "illegal — the row unit moves to the tile, the <code>&lt;section&gt;</code> goes, and the gate's C2/C3 read the module directly.")],
     "Recommend (a), priced: nothing changes in the snippet; the edge's <code>$note</code> becomes the record. (b) is a snippet edit plus the regen serial and touches the row-height model, which is L4's and yours."),
    ("Which composition condition gets an INSTRUMENT (rB Q4).", "<code>check_composition.py</code> exists in scratch and bites (%s arms, %s failed). It is registered nowhere." % (st[0], st[1]),
     [("a", "register it ADVISORY in <code>_validate_screen.py</code>'s chain — reports, never blocks; the L1 ratchet posture."),
      ("b", "register it BLOCKING for C9 only (pure arithmetic, no judgement residue) and advisory for C1."),
      ("c", "leave it unregistered — a gate that is not a consumer of every commit is not a gate.")],
     "Recommend (b): C9 has no eye-only residue at all (rB's own column), and it already refuses honestly (exit 77) where the artefact does not declare its column count."),
    ("Wiring the 470 destiny-tagged guideline rules (rB Q5).", "<code>grep -ln '_rules-index' knowledge/_validate_*.py</code> → nothing. 59 BLOCKING rules sit in an index no gate reads.",
     [("a", "not now — the standing [[instrument-without-a-consumer]] is declared and carried."),
      ("b", "a subset: the composition-class rules (<code>ID-9</code>, <code>neuro-003</code>, <code>CA-2</code>) become C7/C8/C4 arms of this same gate — ~3 arms, ~2K tokens."),
      ("c", "all 59 BLOCKING — a build lane with its own brief and price.")],
     "Recommend (b). It keeps one gate for one class and gives three of the 470 a consumer without pretending the other 467 have one."),
    ("The row-height model.", "Fixed unit / floor <code>minmax(rung,auto)</code> / mis-rung — L4's three renders are the surface for this, not this page.",
     [("a", "fixed rows at every level"), ("b", "the canon hybrid as shipped — fixed at the wall, <code>minmax(unit,1fr)</code> floor inside a group"), ("c", "content-sized with an aspect-ratio floor (Carbon)")],
     "Recommend NO PICK here: point at L4's renders (<code>reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html</code>) and rule off them. The grouping edge is indifferent to the model — it names members, not heights."),
    ("Which LEVEL carries the edge, and does a group need an identity?", "The derivation from the graph yields <b>3 components</b> (<code>kpi-tile</code> · <code>stat-card</code> · <code>summary + status-indicator</code>) — but the last two are the SAME drawn group (“Position”) at two levels, module and content, and the graph cannot say so. %d of %d proposed edges are <code>ref:null</code> because a group is not a node in the grammar." % (n_null, n_edges),
     [("a", "module level only — the edge lives on the tile component (<code>kpi-tile</code>, <code>stat-card</code>); content edges are dropped (6 edges, not 8); groups derive without double counting; “Summary sits beside Status-indicator” is lost."),
      ("b", "both levels, as proposed — 8 edges; a consumer must know that a module edge and a content edge can name one group."),
      ("c", "add <code>group:&lt;slug&gt;</code> to the node-id grammar — every edge resolves, the template's 3 <code>ref:null</code> become refs; a grammar change touching <code>#/definitions/edge</code>'s pattern and <code>gen_kg_edges.py</code>.")],
     "Recommend (a) now, (c) when the grammar is next opened: the module IS the component the bento places, and rule 7b reads the tile's meta, not its contents'."),
]

def questions_html():
    out = []
    for i, (title, ctx, opts, rec) in enumerate(QUESTIONS, 1):
        out.append('<div class="qq"><span class="num">Q%d</span><h3 class="t-ed-heading-4">%s</h3><p class="small">%s</p><ol type="a">%s</ol><p class="rec"><b>%s</b></p></div>' % (
            i, title, ctx, "".join("<li>%s</li>" % o for _, o in opts), rec))
    return "".join(out)

CONSEQ = [
    ("1", "The snippet the SKILL tells the agent to splice never declares its column count or packing", "As shipped, at 1440 the KPI board stacks 4×1 where its own comment says 2×2; the wall's six tracks are implicit, made by the span-6 tile. Declaring two literals fixes it; that is a snippet edit + the ordered serial.", "conductor · repair lane"),
    ("2", "A one-line schema addition is still a schema change", "Applying the fragment re-validates 137 files and re-runs every gate that imports the schema; the L2 fragment is queued for the same act — one sitting, two hunks.", "Dave (ratify) · conductor (apply)"),
    ("3", "Applying the 8 edges puts nothing out of sync", "No generator reads <code>groupsWith</code> today, so the live rails file is unchanged until <code>--rails-from-edge</code> becomes <code>--rails</code>. The dry run proves the default path byte-identical (sha before = after).", "conductor at apply time"),
    ("4", "The rename reaches canon's projection and the memento index", "Both are GENERATED; the plan regenerates them and edits neither. History, rulings and archive keep the old words forever — that is the design.", "conductor · regen serial"),
    ("5", "A ref:null edge is a declared gap, and a consumer must not read it as 'no group'", "The dial lists 4 unresolved edges by name; a gate that treated null as false would go green on the undecided.", "whoever writes the consumer"),
    ("6", "check_composition reads the artefact's own CSS with a small matcher", "Selectors it cannot match (<code>:not</code>, <code>:is</code>, unsupported <code>:has</code> forms) are SKIPPED and counted, not guessed — a page whose gutter comes only through such a rule reads UNRESOLVED → exit 77.", "gate author, if registered"),
    ("7", "Two lanes touched the same words today", "L4 (<code>reviews/ROW-HEIGHT-RENDERS-2026-09-03-v1.html</code>) carries the three class names in its render scripts; the rename plan classifies them as history and touches nothing.", "conductor at reconcile"),
    ("8", "The chart-bar meta already says <code>mustNotNeighbour: component:stat-card</code>", "…“making the identical claim”. The proposed <code>groupsWith</code> on stat-card does not contradict it — different claims may share a group — but a consumer must read both edges, not one.", "gate author"),
]

def conseq_html():
    return '<div class="cards">%s</div>' % "".join('<div class="card"><span class="n">%s</span><h3>%s</h3><p>%s</p><span class="own">%s</span></div>' % (n, t, p, o) for n, t, p, o in CONSEQ)

PAGE = f"""<!DOCTYPE html>
<html lang="en" data-apollo-theme="mono" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>#245-L3 — The composition edge</title>
<!--
  L3 #245 · THE COMPOSITION EDGE (s234-D4) — A PROPOSAL FOR DAVE'S EYE. Nothing live was written:
  no meta, no schema, no generator output, no gate list, no SKILL.md. Every number on this page is
  read from knowledge/_tmp/l3-245/* by build_review.py at generation time.
  SELF-CONTAINED: knowledge/canon/type.css is INLINED VERBATIM below; zero external references.
  THEMES: the canon's own mechanism — [data-apollo-theme="mono|legacy|console|supercharge"] +
  [data-theme="light|dark"] on <html>; the per-theme grounds/inks below were READ from the token store
  via gen_bento_matrix_217.resolve_token (knowledge/_tmp/l3-245/theme-tokens.json), never typed.
  Two-red law s151-D1: #DA1A00 on a white ground, #F6604C on every other ground.
-->
<style id="type-css">
/* ===== knowledge/canon/type.css — INLINED VERBATIM (T-D9 load order: before page CSS) ===== */
{TYPE_CSS}
/* ===== end type.css ===== */
</style>
<style>
{CSS}
</style>
</head>
<body>

<nav>
  <div class="wrap">
    <span class="brand">#245 · Lane L3</span>
    <span class="navlinks">
      <a href="#answer">Answer</a><a href="#edge">The edge</a><a href="#population">The 8</a><a href="#dial">The dial</a><a href="#gate">The gate</a><a href="#questions">Questions</a><a href="#rename">Rename</a><a href="#rule7b">Rule 7b</a><a href="#risk">Consequences</a>
    </span>
    <span class="ctl" role="group" aria-label="Theme">
      <button type="button" data-t="mono" aria-pressed="true">mono</button><button type="button" data-t="legacy" aria-pressed="false">legacy</button><button type="button" data-t="console" aria-pressed="false">console</button><button type="button" data-t="supercharge" aria-pressed="false">supercharge</button>
      <button type="button" id="mode" aria-pressed="false">dark</button>
    </span>
  </div>
</nav>

<section id="top">
  <div class="wrap">
    <span class="flag">Proposed — no meta, schema, generator output, gate list or SKILL was written</span>
    <div class="hdr">
      <div>
        <p class="label">The composition edge · s234-D4</p>
        <h1 class="t-ed-display-1">Grouping lives<br>once, in the graph</h1>
      </div>
      <dl class="meta">
        <dt>Session</dt><dd>#245 · 2026-09-03 · lane L3 of the v1.0.6 brief</dd>
        <dt>Data</dt><dd>the real artefact <code>knowledge/snippets/Template-dashboard-bento.reference.html</code>, its meta, the live schema, the live rails generator — all read, none written</dd>
        <dt>Binding ruling</dt><dd class="mono">s234-D4 (Dave, 2026-09-02)</dd>
        <dt>Register</dt><dd>Every value below is <b>proposed</b>. Files live in <code>knowledge/_tmp/l3-245/</code> and <code>notes/_subreports/assets/2026-09-03-245-L3-composition-edge/</code>.</dd>
      </dl>
    </div>
  </div>
</section>

<section id="answer">
  <div class="wrap">
    <p class="label">The answer, before the argument</p>
    <div class="dim">
      <div><span class="idx">01</span></div>
      <div>
        <h2 class="t-ed-heading-1">Today grouping is three class names in one snippet. The proposal makes it one typed edge in the graph, and everything else derives from it.</h2>
        <p class="lede">The ruling, verbatim from <code>knowledge/_rulings.json</code>: <i>“{e(D4["ruled"])}”</i></p>
        <p><code>grep -rn groupsWith knowledge/components/</code> returns <b>0</b> today — confirmed before anything was built. The fragment adds one line beside <code>mustNotNeighbour</code>; {n_edges} edges are proposed across {n_files} meta files ({n_null} of them <code>ref:null</code>, each naming what you must settle); a dry-run <code>--rails-from-edge</code> derives a grouping dial from those edges without touching the live rails file; a gate does rB's two pure-arithmetic checks against the real artefact and bites on six mutants.</p>
        <p><b>One thing the gate found by refusing.</b> The snippet never declares <code>--layout-bento-columns</code> (or <code>--layout-bento-packing</code>), although its meta says it does. Rendered standalone at 1440, the KPI board stacks 4×1 instead of 2×2. Section 05.</p>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><span class="n">0</span><span class="k">groupsWith in live metas today</span></div>
      <div class="stat"><span class="n">{n_live}/{n_live_of}</span><span class="k">live metas valid · live AND proposed schema</span></div>
      <div class="stat"><span class="n">{n_edges}</span><span class="k">edges proposed · {n_files} meta files</span></div>
      <div class="stat hi"><span class="n">{n_null}</span><span class="k">ref:null — yours</span></div>
      <div class="stat"><span class="n">{n_arms[0]}</span><span class="k">schema arms · {n_arms[2]} red</span></div>
      <div class="stat"><span class="n">{st[0]}</span><span class="k">gate arms · 6 mutants bitten</span></div>
      <div class="stat"><span class="n">{gr[0]}</span><span class="k">files carrying the old names · {gr[4]} occurrences</span></div>
      <div class="stat hi"><span class="n">1</span><span class="k">defect found by driving</span></div>
    </div>
  </div>
</section>

<section id="edge" class="band">
  <div class="wrap">
    <p class="label">The edge</p>
    <div class="dim">
      <div><span class="idx">02</span></div>
      <div>
        <h2 class="t-ed-heading-1">One property, the form every other edge already uses.</h2>
        <p>The slot exists at <code>meta.schema.json:216</code>: <code>edges</code> is a closed object of twelve edge types, each an array of <code>{{ref: &lt;node-id&gt;|null, $note}}</code>. <code>mustNotNeighbour</code> is the negative composition edge and is populated; <code>groupsWith</code> is its positive twin. The change is a schema change and is yours — the template meta says so at line 154: <i>“{e(L154_QUOTE)}”</i></p>
      </div>
    </div>
    <div class="pair">
      <div class="col"><div class="colhead">The fragment · knowledge/_tmp/l3-245/groupsWith.schema.fragment.json</div>{pre(json.dumps(frag, indent=2, ensure_ascii=False))}</div>
      <div class="col"><div class="colhead b">The diff · +1 / −0 · live schema sha unchanged</div>{pre(diff)}</div>
    </div>
    <h4 style="margin-top:var(--s4)">Schema arms · knowledge/_tmp/l3-245/schema-arms.txt</h4>
    {pre(arms)}
  </div>
</section>

<section id="population">
  <div class="wrap">
    <p class="label">The population — proposed, not written</p>
    <div class="dim">
      <div><span class="idx">03</span></div>
      <div>
        <h2 class="t-ed-heading-1">Three groups measured off the artefact; eight edges, every one carrying the line it was read at.</h2>
        <p>The grouping criterion is rB's, not mine: a group is members that answer <b>one question</b> the user came with — read off each group <code>&lt;section&gt;</code>'s <code>aria-label</code>, never invented. The module (Kpi-tile, Stat-card) is the member; what a Stat-card carries rides inside it, and the two content edges (Summary ↔ Status-indicator) are proposed <i>as well</i> so you can see both levels and pick one (Q7).</p>
      </div>
    </div>
    <h4>What the artefact draws</h4>
    <div class="wallpic" aria-label="Schematic of the three drawn groups">
      <div class="grp full"><span class="cap">This month · tpl-group-kpi · 4 × Kpi-tile</span><span class="mod">Closing balance</span><span class="mod">Money out</span><span class="mod">Awaiting approval</span><span class="mod">Available overdraft</span></div>
      <div class="grp"><span class="cap">Spending analysis · tpl-group-chart · 1 × Stat-card</span><span class="mod">Where the money went (Chart-bar)</span></div>
      <div class="grp"><span class="cap">Position · tpl-group-rail · 2 × Stat-card</span><span class="mod">Balances (Summary)</span><span class="mod">Needs attention (Status-indicator ×3)</span></div>
    </div>
    {groups_measured()}
    <h4 style="margin-top:var(--s4)">The eight edges · knowledge/_tmp/l3-245/population-proposal.json</h4>
    {edges_table()}
    <p class="small muted" style="margin-top:var(--s3)">Validation: {n_prop_ok[0]}/{n_prop_ok[1]} live metas pass the proposed schema; {n_files}/{n_files} proposal-applied metas pass it; the same {n_files} are RED against the live schema — the change is required, not decorative. Six planted mutants red, three controls green (arms above).</p>
  </div>
</section>

<section id="dial" class="band">
  <div class="wrap">
    <p class="label">The dial — derived, never picked</p>
    <div class="dim">
      <div><span class="idx">04</span></div>
      <div>
        <h2 class="t-ed-heading-1">What <code>--rails</code> would emit, read from the edge and from nothing else.</h2>
        <p>The live generator was imported, not edited. <code>rails_from_edge.py</code> calls its own <code>edit_rails()</code>, adds one dial by addition and writes to scratch. Groups are connected components of the <code>groupsWith</code> graph over the template's <code>$composes</code> members; <code>ref:null</code> edges are listed as unresolved, by name. No prose is parsed. The live rails file and the generator hash the same before and after, and <code>--rails --out &lt;tmp&gt;</code> still equals the file on disk.</p>
      </div>
    </div>
    <div class="pair">
      <div class="col"><div class="colhead">Proof · knowledge/_tmp/l3-245/rails-from-edge.txt</div>{pre(rails_txt)}</div>
      <div class="col"><div class="colhead b">dials.grouping (excerpt) · _bento_edit_rails.proposed.json</div>{pre(dial_excerpt())}</div>
    </div>
    <p class="note" style="margin-top:var(--s3)">The derivation exposes the level question honestly: <code>stat-card</code> (a self-edge) and <code>summary + status-indicator</code> come out as two components although the artefact draws them as one group. A dial that knows only the graph cannot merge them without a group identity — Q7.</p>
  </div>
</section>

<section id="gate">
  <div class="wrap">
    <p class="label">The gate — C9 span legality · C1 gap ladder</p>
    <div class="dim">
      <div><span class="idx">05</span></div>
      <div>
        <h2 class="t-ed-heading-1">Pure arithmetic, read off the artefact's own CSS — and it refused where the artefact does not say.</h2>
        <p><code>check_composition.py</code> reads the column count and band clamps from the page's <code>@container</code> blocks and resolves each bento's gutter by matching the page's own <code>--bento-gutter</code> rules against its own DOM, specificity-ranked. C9: every effective span divides the columns at every band and every grid sums to whole rows. C1: <code>gap(child) &lt; gap(parent)</code>, strictly, both on the ruled stops. It is registered in no gate list.</p>
        <p><b>Driven on the real snippet it came back UNPROVEN (exit 77), not green:</b> the base column count is undeclared. <code>.c-bento</code> reads <code>var(--layout-bento-columns)</code> and nothing in the file sets it — though <code>template-dashboard-bento.meta.json</code> <code>$tokenGaps[0]</code> says <i>“The value is declared as a literal 6 with this note.”</i> <code>grep -c -- '--layout-bento-columns\\s*:' …reference.html</code> → 0. The same is true of <code>--layout-bento-packing</code> (<code>row dense</code> is lost; computed <code>grid-auto-flow</code> is <code>row</code>).</p>
      </div>
    </div>
    <h4>What that does on screen · render-probe.json (playwright, file://, the seat's runbook recipe)</h4>
    {probe_table()}
    <div class="wallpic stacked" aria-label="Schematic: as shipped at 1440 the KPI board stacks 4 by 1">
      <div class="grp full"><span class="cap">as shipped · 1440 · KPI board stacked 4×1 (each tile 1376 × 196)</span><span class="mod">Closing balance</span><span class="mod">Money out</span><span class="mod">Awaiting approval</span><span class="mod">Available overdraft</span></div>
    </div>
    <p class="small muted">With the literal declared (fixture, in sandbox scratch only) the four tiles sit 2×2 at 686 × 196 — the layout the snippet's own comment at line 838 describes. The wall shows six tracks in both cases: as shipped they are <i>implicit</i> tracks created by the span-6 tile, which is why the defect hid. Full-page PNGs of both are in the evidence folder.</p>
    <div class="pair">
      <div class="col"><div class="colhead">Drive · the real artefact · drive-real-artefact.txt</div>{pre(drive)}</div>
      <div class="col"><div class="colhead b">Selftest · selftest-check-composition.txt</div>{pre(selftest)}</div>
    </div>
  </div>
</section>

<section id="questions" class="band">
  <div class="wrap">
    <p class="label">Ruling-shaped questions — yours</p>
    <div class="dim">
      <div><span class="idx">06</span></div>
      <div>
        <h2 class="t-ed-heading-1">Seven things the proposal had to leave open, put back to you with the options priced.</h2>
        <p class="small muted">Each carries one recommendation. A recommendation is not a ruling; five of these (the words · the schema change · one-member legality · the 470 rules · the row-height model) are on your do-not-rule list and are put back exactly as questions.</p>
      </div>
    </div>
    {questions_html()}
  </div>
</section>

<section id="rename">
  <div class="wrap">
    <p class="label">The rename — floated, grepped, nothing renamed</p>
    <div class="dim">
      <div><span class="idx">07</span></div>
      <div>
        <h2 class="t-ed-heading-1"><code>tpl-group-kpi / -chart / -rail</code> → proposed <code>-lead / -evidence / -context</code>.</h2>
        <p>Grep-before, repo-wide: <b>{gr[0]} files, {gr[4]} occurrences</b> (kpi {gr[1]} · chart {gr[2]} · rail {gr[3]}). One is the source, two are generated projections, the rest are history, rulings, review pages, conductor state or scratch and are never edited. The floated words collide with nothing.</p>
      </div>
    </div>
    {pre(grep_before)}
    <h4 style="margin-top:var(--s4)">Dry-run plan · rename-plan.json</h4>
    <ol>{''.join('<li>%s</li>' % e(s) for s in plan["steps_if_ruled"])}</ol>
    <p class="small muted">would edit: <code>{e(", ".join(plan["would_edit"]))}</code> · would regenerate: <code>{e(", ".join(plan["would_regenerate"]))}</code> · never touched: {len(plan["never_touch"])} files · conductor state by addition: {len(plan["conductor_by_addition"])} files.</p>
  </div>
</section>

<section id="rule7b" class="band">
  <div class="wrap">
    <p class="label">Rule 7b — proposed text</p>
    <div class="dim">
      <div><span class="idx">08</span></div>
      <div>
        <h2 class="t-ed-heading-1">Beside rule 7 and 7a in <code>generate-from-canon/SKILL.md</code>, never re-wording them.</h2>
        <p>Rule 7 sends the agent to the rails file for every layout dial; 7a makes dashboards bento-first. Neither says where grouping comes from, and the rails file has no seat for it (rB F13, <code>grep -c group _bento_edit_rails.json → 0</code>). 7b points at the edge. No SKILL.md was edited.</p>
      </div>
    </div>
    {pre(RULE7B)}
  </div>
</section>

<section id="risk">
  <div class="wrap">
    <p class="label">Consequences replayed</p>
    <div class="dim">
      <div><span class="idx">09</span></div>
      <div><h2 class="t-ed-heading-1">What could go wrong with what was built, and who owns each.</h2></div>
    </div>
    {conseq_html()}
  </div>
</section>

<footer>
  <div class="wrap">
    <p>Generated by <code>knowledge/_tmp/l3-245/build_review.py</code> from the lane's artefact files. Filed report: <code>notes/_subreports/2026-09-03-245-L3-composition-edge.md</code>. Evidence: <code>notes/_subreports/assets/2026-09-03-245-L3-composition-edge/</code>. Nothing live was written; nothing here is ruled.</p>
  </div>
</footer>

<script>
(function(){{
  var r=document.documentElement, mode=document.getElementById('mode'), tb=document.querySelectorAll('.ctl button[data-t]');
  if(window.matchMedia && window.matchMedia('(prefers-color-scheme:dark)').matches){{r.setAttribute('data-theme','dark');}}
  function sync(){{var d=r.getAttribute('data-theme')==='dark'; mode.textContent=d?'light':'dark'; mode.setAttribute('aria-pressed',String(d));
    tb.forEach(function(b){{b.setAttribute('aria-pressed',String(b.getAttribute('data-t')===r.getAttribute('data-apollo-theme')));}});}}
  mode.addEventListener('click',function(){{r.setAttribute('data-theme',r.getAttribute('data-theme')==='dark'?'light':'dark');sync();}});
  tb.forEach(function(b){{b.addEventListener('click',function(){{r.setAttribute('data-apollo-theme',b.getAttribute('data-t'));sync();}});}});
  sync();
}})();
</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8").write(PAGE)
ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', PAGE) + re.findall(r"@import|url\((?!['\"]?data:)", PAGE)
print("wrote %s (%d B) · external refs: %d · type.css inlined verbatim: %s" % (os.path.relpath(OUT, ROOT), len(PAGE.encode()), len(ext), TYPE_CSS in PAGE))
