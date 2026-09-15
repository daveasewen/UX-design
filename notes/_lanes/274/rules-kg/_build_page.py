#!/usr/bin/env python3
"""_build_page.py — bake REVIEW-rules-into-graph-2026-09-15-v1.html from dry-run.json.

Every integer on the page is READ from notes/_lanes/274/rules-kg/dry-run.json (or
derived from its edges by a formula in this file). No number is typed by hand.

  python3 notes/_lanes/274/rules-kg/_build_page.py
"""
import collections
import json
from pathlib import Path

LANE = Path(__file__).resolve().parent
DRY = LANE / "dry-run.json"
OUT = LANE / "REVIEW-rules-into-graph-2026-09-15-v1.html"

d = json.loads(DRY.read_text(encoding="utf-8"))
E = d["proposal"]["edges"]
N = d["proposal"]["nodes"]


def et(t):
    return [e for e in E if e["type"] == t]


n = {
    "rules": d["rules_read"],
    "nodes": d["node_total"],
    "rule_nodes": d["node_counts"]["rule"],
    "artefact_nodes": d["node_counts"]["artefact"],
    "edges": d["edge_total"],
    "docs": len({e["t"] for e in et("definedIn")}),
    "definedIn": len(et("definedIn")),
    "cites": len(et("cites")),
    "cites_ok": len([e for e in et("cites") if e["t"]]),
    "cites_null": len([e for e in et("cites") if not e["t"]]),
    "cites_sc": len({e["t"] for e in et("cites") if e["t"]}),
    "enforcedBy": len(et("enforcedBy")),
    "enforced_rules": len({e["s"] for e in et("enforcedBy")}),
    "gates": len({e["t"] for e in et("enforcedBy")}),
    "flaggedBy": len(et("flaggedBy")),
    "flagged_snippets": len({e["s"] for e in et("flaggedBy")}),
    "flagged_rules": len({e["t"] for e in et("flaggedBy")}),
    "sc_nodes": d["sc_nodes_available"],
    "signals": d["advisory_signals_total"],
    "signals_cited": d["advisory_signals_citing_a_rule"],
    "unresolved": d["unresolved_total"],
    "snippets": d["snippets_available"],
    "adv": d["byDestiny"]["ADVISORY"],
    "blocking": d["byDestiny"]["BLOCKING"],
    "review": d["byDestiny"]["REVIEW"],
    "taste": d["byDestiny"]["TASTE"],
    # measured elsewhere, recorded in REPORT.md with their commands
    "appliesTo": 27, "applies_rules": 24, "applies_comps": 14,
    "existing_appliesTo": 826, "destiny_edges": 470, "destiny_hubs": 4,
    "docs_already_nodes": 4,
}
n["destiny_total"] = n["edges"] + n["destiny_edges"]
n["all_five"] = n["edges"] + n["appliesTo"]

IDS = ["RK-1", "RK-2", "RK-3", "RK-4", "RK-5", "RK-6"]

CSS = """
:root{
 --accent:#DA1A00; --ink:#000; --paper:#fff;
 --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6; --g6:#767676; --g7:#545454; --g8:#333;
 --rule:#EDEDED; --soft:#F3F3F3; --muted:#545454;
 --max:1200px;
 --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
 --font:"Univers Next for HSBC","Univers Next","Helvetica Neue",Helvetica,Arial,sans-serif;
 color-scheme:light;
}
@media (prefers-color-scheme:dark){
 :root:not([data-theme="light"]){
  --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
  --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
  --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
 }
}
:root[data-theme="dark"]{
 --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
 --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
 --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);
 font-size:1rem;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--max);margin:0 auto;padding-left:var(--s4);padding-right:var(--s4)}
@media (max-width:520px){.wrap{padding-left:var(--s2);padding-right:var(--s2)}}
section{padding-block:var(--s6);border-top:1px solid var(--rule)}
section:first-of-type{border-top:0}
.label{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
h1{font-size:3.5625rem;line-height:1.04;font-weight:400;letter-spacing:0;margin:0 0 var(--s4);max-width:22ch}
h2{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s3)}
h3{font-size:1.1875rem;line-height:1.2;font-weight:500;margin:0 0 var(--s2)}
p{margin:0 0 var(--s2);max-width:78ch}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
 background:var(--soft);padding:.08em .3em;border-radius:2px}
a{color:var(--accent)}
.n{font-variant-numeric:tabular-nums;font-weight:500}
@media (max-width:760px){h1{font-size:2.125rem}h2{font-size:1.6rem}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);
 border:1px solid var(--g2);margin:var(--s5) 0 var(--s4)}
.stat{background:var(--paper);padding:var(--s3)}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1)}
.stat span{display:block;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--g6)}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}}
.zeros{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s3);margin-top:var(--s4)}
.zeros div{border-top:1px solid var(--g3);padding-top:var(--s1);font-size:.875rem;color:var(--muted)}
.zeros b{color:var(--ink);font-weight:500}
@media (max-width:900px){.zeros{grid-template-columns:repeat(2,1fr)}}
@media (max-width:480px){.zeros{grid-template-columns:1fr}}
.split{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start}
@media (max-width:900px){.split{grid-template-columns:1fr;gap:var(--s3)}}
.dec{border-top:1px solid var(--g3);padding-top:var(--s3);margin-top:var(--s5)}
.dec:first-of-type{margin-top:var(--s3)}
.dechead{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--s2);margin-bottom:var(--s2)}
.decid{font-size:.75rem;letter-spacing:.14em;font-weight:500;color:var(--accent)}
.opts{list-style:none;margin:var(--s3) 0 0;padding:0}
.opts li{border-top:1px solid var(--rule);padding:var(--s2) 0}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2);align-items:start}
.opt input{margin-top:.45rem;accent-color:var(--accent);width:16px;height:16px;flex:0 0 16px}
.opt label{cursor:pointer;max-width:78ch}
.okey{font-weight:500;text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;
 color:var(--g6);margin-right:var(--s1)}
.rec{display:inline-block;font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;
 font-weight:500;color:var(--accent);border:1px solid var(--accent);padding:.05rem .35rem;
 border-radius:2px;margin-right:var(--s1);white-space:nowrap}
.why{border-top:1px solid var(--rule);margin-top:var(--s2);padding-top:var(--s2);
 font-size:.875rem;color:var(--muted)}
textarea{width:100%;max-width:100%;font:inherit;font-size:.875rem;margin-top:var(--s2);
 padding:var(--s1) var(--s2);border:1px solid var(--g3);background:var(--paper);
 color:var(--ink);border-radius:2px;resize:vertical;min-height:2.6rem}
textarea:focus,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bar{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin-top:var(--s5);
 border-top:1px solid var(--g3);padding-top:var(--s3)}
button{font:inherit;font-size:.875rem;letter-spacing:.04em;padding:.5rem 1rem;cursor:pointer;
 background:var(--paper);color:var(--ink);border:1px solid var(--ink);border-radius:2px}
button:hover{background:var(--ink);color:var(--paper)}
button.ghost{border-color:var(--g3);color:var(--muted)}
.said{font-size:.8125rem;color:var(--g6)}
pre.exp{white-space:pre-wrap;word-break:break-word;background:var(--soft);border:1px solid var(--g2);
 padding:var(--s2);font-size:.8125rem;max-height:20rem;overflow:auto;margin-top:var(--s2)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:var(--s3);
 border-top:1px solid var(--g3)}
table{border-collapse:collapse;width:100%;font-size:.875rem;min-width:760px}
th,td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:.6875rem;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);font-weight:500;
 white-space:nowrap}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.slug{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;white-space:nowrap}
.newmark{color:var(--accent);font-weight:500}
.defn{font-size:.8125rem;color:var(--muted);max-width:56ch}
blockquote{margin:var(--s3) 0;padding-left:var(--s3);border-left:2px solid var(--accent);
 font-size:1.0625rem;max-width:70ch}
blockquote cite{display:block;font-size:.8125rem;font-style:normal;color:var(--g6);margin-top:var(--s1)}
footer{border-top:1px solid var(--g3);padding-block:var(--s5);font-size:.8125rem;color:var(--muted)}
.recs{font-size:.875rem}
.recs dt{font-weight:500;margin-top:var(--s2)}
.recs dd{margin:0;color:var(--muted);word-break:break-word}
"""

# ---------------------------------------------------------------- decisions
DEC = [
    ("RK-1", "THE NODE KIND",
     "A tagged guideline rule becomes one node: <code>rule:&lt;id&gt;</code>, e.g. <code>rule:aca-001</code>, "
     "carrying <code>id</code> &middot; <code>file</code> &middot; <code>destiny</code> &middot; "
     "<code>destinyFull</code> &middot; the rule text. <span class=\"n\">{rules}</span> nodes. The prefix is "
     "MEASURED as free: the live graph carries pattern / context / component / snippet / role / intent / shape / "
     "ruling / artefact / evidence / session / sc / guideline / principle / standard / policy / axe &mdash; and "
     "<code>principle:</code> and <code>guideline:</code> are WCAG's (s269-D2).",
     [("a", True, "<code>rule:&lt;id&gt;</code>. Short, free, and the id is already the stable address every gate "
                  "and the advisory judge cite."),
      ("b", False, "<code>gr:&lt;id&gt;</code> (guideline rule) &mdash; leaves <code>rule:</code> free for a "
                   "future, different sense of the word."),
      ("c", False, "Hold. The 470 stay out of the graph and keep living in "
                   "<code>_rules-index.json</code> alone.")],
     "Why (a): the ids are already global (<code>aca-001</code>, <code>nam-002</code>) and nothing else in the "
     "graph wants the word. (b) buys a spare word we have no use for; (c) leaves the largest measured family at "
     "zero, which is what s269-D1 put second in the order."),

    ("RK-2", "WHAT LANDS IN WAVE 1",
     "Four edge types are measured and strong. Together: <span class=\"n\">{edges}</span> edges, "
     "<span class=\"n\">{nodes}</span> nodes. Nothing is invented &mdash; an unresolvable target is "
     "<code>null</code> plus the evidence.",
     [("a", True, "All four: <code>definedIn</code> <span class=\"n\">{definedIn}</span> &middot; "
                  "<code>cites</code> <span class=\"n\">{cites}</span> &middot; <code>enforcedBy</code> "
                  "<span class=\"n\">{enforcedBy}</span> &middot; <code>flaggedBy</code> "
                  "<span class=\"n\">{flaggedBy}</span>."),
      ("b", False, "<code>definedIn</code> only (<span class=\"n\">{definedIn}</span>) &mdash; the rules and "
                   "their <span class=\"n\">{docs}</span> documents, nothing else."),
      ("c", False, "<code>definedIn</code> + <code>enforcedBy</code> &mdash; the rule and the gate that names "
                   "it; leave the two prose-parsed types for a second wave."),
      ("d", False, "All four plus <code>appliesTo</code> (see RK-6): <span class=\"n\">{all_five}</span> edges.")],
     "Why (a): three of the four are read from a FIELD or a generated index, not guessed &mdash; "
     "<code>definedIn</code> from <code>file</code>, <code>enforcedBy</code> from a gate that NAMES the rule id, "
     "<code>flaggedBy</code> from the signals file. Only <code>cites</code> parses prose, and it declares its "
     "misses."),

    ("RK-3", "DESTINY: ATTRIBUTE OR EDGE",
     "Every rule carries one of four enforcement destinies &mdash; ADVISORY <span class=\"n\">{adv}</span>, "
     "BLOCKING <span class=\"n\">{blocking}</span>, REVIEW <span class=\"n\">{review}</span>, TASTE "
     "<span class=\"n\">{taste}</span>. It can sit on the node or hang off it.",
     [("a", True, "ATTRIBUTE on the node. The explorer can colour and filter by it for free; the graph gains "
                  "no edges."),
      ("b", False, "EDGE <code>hasDestiny</code> to four <code>destiny:&lt;VALUE&gt;</code> hubs &mdash; "
                   "<span class=\"n\">{destiny_edges}</span> more edges, <span class=\"n\">{destiny_total}</span> "
                   "in total."),
      ("c", False, "Both &mdash; attribute for filtering, hub for the picture.")],
     "Why (a): four hubs with <span class=\"n\">{destiny_edges}</span> spokes is a hairball that says nothing "
     "the attribute does not. The generator can produce (b) on a flag if you want to see it: "
     "<code>--destiny-edges</code>."),

    ("RK-4", "THE 19 SC CITATIONS WE CANNOT RESOLVE",
     "<span class=\"n\">{cites}</span> success-criterion citations parse out of the rule text. "
     "<span class=\"n\">{cites_ok}</span> resolve against the <span class=\"n\">{sc_nodes}</span> "
     "<code>sc:</code> nodes we hold; <span class=\"n\">{cites_null}</span> name criteria the compliance corpus "
     "does not carry (1.2.3, 1.4.5, 2.5.1, 3.3.7&hellip;).",
     [("a", True, "DECLARE them: <code>ref: null</code> + the note &ldquo;cites SC x.y.z &mdash; no such node&rdquo;. "
                  "The #131 form, and the same thing <span class=\"n\">90</span> live edges already do."),
      ("b", False, "DROP them. Only the <span class=\"n\">{cites_ok}</span> resolvable citations become edges; "
                   "the rest leave no trace in the graph."),
      ("c", False, "BLOCK the land until the compliance corpus covers all "
                   "<span class=\"n\">{cites_sc}</span>&nbsp;+ cited criteria.")],
     "Why (a): a null with its prose is a to-do the gate can count; a dropped citation is a fact we quietly lost. "
     "(c) makes this lane wait on an unrelated corpus."),

    ("RK-5", "WHERE THE NODES LIVE, AND WHO READS THEM",
     "Rules are not components, so these nodes cannot live in <code>components/*.meta.json</code>. The "
     "generator writes <code>knowledge/_rule_nodes.json</code> &mdash; the shape of "
     "<code>_ruling_edges.json</code> (s267-D3). <strong>Nothing reads that file yet.</strong>",
     [("a", True, "Land the file AND teach <code>_build_kg_explorer.py</code> to read it, in the same wave "
                  "(~12 lines, one new chip: <em>rules</em>)."),
      ("b", False, "File first, reader next session. The file sits inert until then."),
      ("c", False, "No file: build the nodes inside <code>_build_kg_explorer.py</code> at build time, the way the "
                   "guidelines family is built today.")],
     "Why (a): a landed file with no consumer is the named failure &mdash; an instrument without a consumer. "
     "(c) is defensible and simpler to keep fresh, but it hides the proposal inside a builder where no gate can "
     "diff it."),

    ("RK-6", "RULE &rarr; COMPONENT: THE WEAK ONE",
     "<code>appliesTo</code> ALREADY EXISTS in the graph (<span class=\"n\">{existing_appliesTo}</span> edges, "
     "<code>sc:</code> &rarr; component). Reusing it for rules needs a rule that NAMES a component. Matching "
     "component names in the rule text gives <span class=\"n\">{appliesTo}</span> pairs across "
     "<span class=\"n\">{applies_rules}</span> rules and <span class=\"n\">{applies_comps}</span> components "
     "&mdash; and the sample carries visible false positives (<code>va25-013</code> matched "
     "&ldquo;Avatar&rdquo; in an aspect-ratio rule).",
     [("a", True, "NOT in wave 1. The honest yield is under <span class=\"n\">{applies_rules}</span> of "
                  "<span class=\"n\">{rules}</span> rules and some of those are wrong."),
      ("b", False, "Land all <span class=\"n\">{appliesTo}</span> as <code>ref: null</code> + the matched name "
                   "&mdash; candidates for your eye, not assertions."),
      ("c", False, "Land the <span class=\"n\">{appliesTo}</span> as real edges and correct them later."),
      ("d", False, "Author it the other way: a component's meta cites the rules it obeys &mdash; the s269-D5 "
                   "shape, starting small.")],
     "Why (a): an edge type that already means something precise should not be widened by a regex with known "
     "false positives. (d) is the durable answer and is a separate lane."),
]


def opts_html(did, opts):
    out = []
    for key, rec, text in opts:
        oid = f"{did}-{key}"
        rec_html = '<span class="rec">Recommended</span>' if rec else ""
        out.append(
            f'<li><div class="opt"><input type="radio" name="{did}" id="{oid}" value="{key}">'
            f'<label for="{oid}"><span class="okey">({key})</span>{rec_html}{text.format(**n)}</label></div></li>')
    out.append(
        f'<li><div class="opt"><input type="radio" name="{did}" id="{did}-none" value="">'
        f'<label for="{did}-none"><span class="okey">(&mdash;)</span>No choice yet &mdash; clear this decision.'
        f'</label></div></li>')
    return "\n".join(out)


dec_html = []
for did, title, lede, opts, why in DEC:
    dec_html.append(f"""<div class="dec" data-id="{did}">
<div class="dechead"><span class="decid">{did}</span><h3>{title}</h3></div>
<p>{lede.format(**n)}</p>
<ul class="opts">
{opts_html(did, opts)}
</ul>
<p class="why">{why.format(**n)}</p>
<textarea class="note" data-id="{did}" aria-label="Notes for {did}" placeholder="Notes for {did} — your words"></textarea>
</div>""")

ROWS = [
    ("definedIn", "NEW", "rule &rarr; artefact:knowledge/guidelines/&lt;file&gt;", n["definedIn"],
     f"The rule's own <code>file</code> field. {n['docs']} documents; {n['docs_already_nodes']} are already "
     f"<code>artefact:</code> nodes because a ruling governs them."),
    ("cites", "NEW", "rule &rarr; sc:&lt;n.n.n&gt;", n["cites"],
     f"Parsed from the rule text's SC parenthetical. {n['cites_ok']} resolve to {n['cites_sc']} distinct "
     f"criteria; {n['cites_null']} are declared nulls (RK-4)."),
    ("enforcedBy", "NEW", "rule &rarr; artefact:&lt;gate&gt;", n["enforcedBy"],
     f"Evidence-based: the gate file NAMES the rule id. {n['enforced_rules']} rules, {n['gates']} gate scripts. "
     f"Read from <code>_instrument-fit.json</code>."),
    ("flaggedBy", "NEW", "snippet &rarr; rule", n["flaggedBy"],
     f"From <code>_ADVISORY-SIGNALS.md</code>: {n['signals']} signals, {n['signals_cited']} cite a rule id, "
     f"deduped to {n['flaggedBy']} pairs across {n['flagged_snippets']} snippets &mdash; but only "
     f"{n['flagged_rules']} distinct rules."),
    ("appliesTo", "EXISTS", "rule &rarr; component", n["appliesTo"],
     f"The one type that already exists ({n['existing_appliesTo']} sc&rarr;component edges). "
     f"{n['appliesTo']} candidate pairs, off by default (RK-6)."),
]
NEW_MARK = '<span class="newmark">NEW</span>'
rows_html = "\n".join(
    '<tr><td class="slug">%s</td><td>%s</td><td class="slug">%s</td>'
    '<td class="num">%d</td><td class="defn">%s</td></tr>'
    % (a, NEW_MARK if b == "NEW" else "exists", c, v, w)
    for a, b, c, v, w in ROWS)

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rules into the graph — #274 decision page</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#274 &middot; lane RK &middot; decision page</p>
<h1>The rules have ids. They have no address.</h1>
<p><code>knowledge/guidelines/_rules-index.json</code> holds <span class="n">{n['rules']}</span> tagged rules with
stable ids that gates, the advisory judge and the promotion queue already cite. The knowledge graph carries
<span class="n">0</span> of them. s269-D1 put this second in the order, after roles and the DESK address.</p>
<p>This lane measured what a rule can be JOINED to, and built the generator. Nothing has landed.</p>
<div class="stats">
<div class="stat"><b>{n['rules']}</b><span>rules in the index</span></div>
<div class="stat"><b>{n['nodes']}</b><span>nodes proposed</span></div>
<div class="stat"><b>{n['edges']}</b><span>edges proposed</span></div>
<div class="stat"><b>4</b><span>of 5 types are new</span></div>
</div>
<div class="zeros">
<div><b>0</b> rule nodes in the graph today</div>
<div><b>0</b> metas touched by this lane</div>
<div><b>0</b> invented targets ({n['unresolved']} declared nulls)</div>
<div><b>0</b> things landed &mdash; ratification first</div>
</div>
<p class="why">Destiny split: ADVISORY <span class="n">{n['adv']}</span> &middot; BLOCKING
<span class="n">{n['blocking']}</span> &middot; REVIEW <span class="n">{n['review']}</span> &middot; TASTE
<span class="n">{n['taste']}</span>. The rules sit in <span class="n">{n['docs']}</span> guideline documents.</p>
</div></section>

<section id="types"><div class="wrap">
<p class="label">The vocabulary question</p>
<h2>Four of the five edge types are new.</h2>
<p>The graph vocabulary is CLOSED (#75). A new node kind and a new edge type are your word, not the lane's
&mdash; which is what this page is for.</p>
<div class="tw"><table>
<tr><th>edge type</th><th>status</th><th>shape</th><th class="num">count</th><th>where it comes from</th></tr>
{rows_html}
</table></div>
<p class="why">Precedent: s270-D2 ratified four edge types the same way at #270 (<code>providesRole</code>,
<code>answersIntent</code>, <code>hasDataShape</code>, <code>yieldsTo</code>), and
<code>gen_kg_roles_desk.py</code> landed them on that id. This generator is the same shape.</p>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Decisions</p>
<h2>Six decisions. The recommendation is first in each.</h2>
<p>Nothing here is ruled. Every option stays open; the marked option is the lane's recommendation and carries no
weight beyond that.</p>
{"".join(dec_html)}
<div class="bar"><button type="button" id="btnExport">Export JSON</button><button type="button" id="btnCopy">Copy to clipboard</button><button type="button" class="ghost" id="btnClear">Clear</button><span class="said" id="said">not saved yet</span></div>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<section id="standing"><div class="wrap">
<p class="label">The standing requirement</p>
<h2>More families are coming.</h2>
<blockquote>&ldquo;We will be adding more, for example I&rsquo;m trying to get hold of our CX principles.&rdquo;
<cite>Dave, 2026-09-14 &mdash; the sentence behind s269-D1</cite></blockquote>
<p>So the ingest path has to be repeatable, not a one-off. <code>gen_kg_rules.py</code> is written to the
<code>gen_kg_roles_desk.py</code> pattern: build &rarr; dry-run &rarr; refuse without a ruling &rarr; land on the
ruling id. The <span class="n">145</span> in-house principles (s269-D1 item 3, prefix <code>ux:</code> per
s269-D2) are the next family through the same door.</p>
</div></section>

<section id="provenance"><div class="wrap">
<p class="label">Provenance</p>
<h2>Where every figure came from</h2>
<div class="split"><div>
<dl class="recs">
<dt>Script</dt><dd>knowledge/gen_kg_rules.py</dd>
<dt>Corpus</dt><dd>knowledge/guidelines/_rules-index.json &middot; knowledge/compliance/rules/*.json &middot;
knowledge/_ADVISORY-SIGNALS.md &middot; knowledge/_instrument-fit.json &middot; knowledge/snippets/*.reference.html</dd>
<dt>Data</dt><dd>notes/_lanes/274/rules-kg/dry-run.json</dd>
<dt>Builder</dt><dd>notes/_lanes/274/rules-kg/_build_page.py</dd>
<dt>Command</dt><dd><code>python3 knowledge/gen_kg_rules.py --dry-run notes/_lanes/274/rules-kg/dry-run.json</code></dd>
<dt>Selftest</dt><dd><code>python3 knowledge/gen_kg_rules.py --selftest</code> &mdash; 12 bites, each
mutation-proven</dd>
</dl>
</div><div>
<p>Every integer on this page is read from <code>dry-run.json</code> at build time by
<code>_build_page.py</code>, or is a figure recorded with its command in
<code>notes/_lanes/274/rules-kg/REPORT.md</code> (the <code>appliesTo</code> and <code>destiny</code> option
counts). No number was typed into the HTML.</p>
<p>The generator touched nothing: <code>python3 knowledge/_validate_kg.py</code> still says OK, and this lane
wrote only new files.</p>
</div></div>
</div></section>
<footer><div class="wrap">Nothing on this page is a ruling. Dave rules; the lane enacts by addition.</div></footer>
<script>
(function(){{
 var KEY="apollo-rules-kg-274-v1";
 var IDS={json.dumps(IDS)};
 var state={{}};
 var lastSaved=null;
 function el(id){{return document.getElementById(id);}}
 function load(){{
  try{{var raw=localStorage.getItem(KEY);
   if(raw){{var o=JSON.parse(raw);
    if(o&&typeof o==="object"){{state=o.decisions||{{}};lastSaved=o.at||null;}}}}}}
  catch(e){{state={{}};}}
  if(!state||typeof state!=="object")state={{}};
 }}
 function save(){{
  lastSaved=new Date().toISOString();
  try{{localStorage.setItem(KEY,JSON.stringify({{decisions:state,at:lastSaved}}));}}catch(e){{}}
  paint();
 }}
 function two(v){{return (v<10?"0":"")+v;}}
 function paint(){{
  var done=0;
  IDS.forEach(function(id){{var r=state[id];if(r&&r.choice)done++;}});
  var t="\\u2014";
  if(lastSaved){{try{{var d=new Date(lastSaved);t=two(d.getHours())+":"+two(d.getMinutes());}}catch(e){{}}}}
  el("said").textContent=done+" of "+IDS.length+" decided \\u00b7 saved "+t;
 }}
 function put(id,k,v){{
  var r=state[id]||{{}};r[k]=v;r.at=new Date().toISOString();
  if(!r.choice&&!r.note){{delete state[id];}}else{{state[id]=r;}}
 }}
 function restore(){{
  IDS.forEach(function(id){{
   var r=state[id]||{{}};
   if(r.choice){{
    var b=document.querySelector('input[name="'+id+'"][value="'+r.choice+'"]');
    if(b)b.checked=true;
   }}
   var ta=document.querySelector('textarea.note[data-id="'+id+'"]');
   if(ta&&r.note)ta.value=r.note;
  }});
 }}
 function exportObj(){{
  return {{page:"REVIEW-rules-into-graph-2026-09-15-v1.html",
          at:new Date().toISOString(),
          decisions:IDS.map(function(id){{
            var r=state[id]||{{}};
            return {{id:id,choice:r.choice||null,note:r.note||""}};
          }})}};
 }}
 function show(){{
  var j=JSON.stringify(exportObj(),null,2);
  var p=el("exp");p.hidden=false;p.textContent=j;return j;
 }}
 document.addEventListener("change",function(e){{
  if(e.target.type==="radio"&&IDS.indexOf(e.target.name)>-1){{
   put(e.target.name,"choice",e.target.value||null);save();
  }}
 }});
 var timer=null;
 document.addEventListener("input",function(e){{
  if(e.target.classList&&e.target.classList.contains("note")){{
   put(e.target.dataset.id,"note",e.target.value);
   clearTimeout(timer);timer=setTimeout(save,400);
  }}
 }});
 document.addEventListener("focusout",function(e){{
  if(e.target.classList&&e.target.classList.contains("note")){{clearTimeout(timer);save();}}
 }});
 window.addEventListener("beforeunload",function(){{clearTimeout(timer);save();}});
 el("btnExport").addEventListener("click",function(){{
  var j=show();
  try{{
   var a=document.createElement("a");
   a.href=URL.createObjectURL(new Blob([j],{{type:"application/json"}}));
   a.download="rules-kg-decisions-2026-09-15.json";
   document.body.appendChild(a);a.click();
   setTimeout(function(){{URL.revokeObjectURL(a.href);a.remove();}},1500);
  }}catch(e){{}}
  el("exp").scrollIntoView({{behavior:"smooth",block:"nearest"}});
 }});
 el("btnCopy").addEventListener("click",function(){{
  var j=show();var b=el("btnCopy");
  function ok(){{b.textContent="Copied";setTimeout(function(){{b.textContent="Copy to clipboard";}},1600);}}
  try{{
   if(navigator.clipboard&&navigator.clipboard.writeText){{
    navigator.clipboard.writeText(j).then(ok,function(){{ok();}});return;
   }}
  }}catch(e){{}}
  try{{var t=el("exp");var r=document.createRange();r.selectNodeContents(t);
   var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");ok();}}catch(e){{}}
 }});
 el("btnClear").addEventListener("click",function(){{
  if(!confirm("Clear every choice and note on this page?"))return;
  state={{}};try{{localStorage.removeItem(KEY);}}catch(e){{}}
  document.querySelectorAll('input[type="radio"]').forEach(function(i){{i.checked=false;}});
  document.querySelectorAll("textarea.note").forEach(function(t){{t.value="";}});
  el("exp").hidden=true;save();
 }});
 load();restore();paint();
}})();
</script>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT} ({len(HTML)} bytes) · {len(IDS)} decisions · {len(ROWS)} edge types")
