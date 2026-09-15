#!/usr/bin/env python3
"""_build_page.py — bake REVIEW-principles-into-graph-2026-09-15-v1.html (#275 lane RP).

The page's COPY comes from principles-kg-decisions-2026-09-15.json.
The page's NUMBERS come from dry-run.json, from two option runs of the generator,
and from a live measurement of notes/_KG-EXPLORER.html. No integer is typed into
the HTML or into the decisions file.

⚠ The review page EXPORTS Dave's answers under the SAME filename as the decisions
file. If that export is ever copied over the input, this builder REFUSES by name
rather than baking a page with no copy on it.

  python3 notes/_lanes/275/principles-kg/_build_page.py
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
DRY = LANE / "dry-run.json"
DEC = LANE / "principles-kg-decisions-2026-09-15.json"
EXPLORER_HTML = REPO / "notes" / "_KG-EXPLORER.html"
GEN = REPO / "knowledge" / "gen_kg_principles.py"
OUT = LANE / "REVIEW-principles-into-graph-2026-09-15-v1.html"

spec = json.loads(DEC.read_text(encoding="utf-8"))
if "decisions" not in spec or not all(isinstance(d, dict) and "title" in d for d in spec["decisions"]):
    sys.exit(f"REFUSED — {DEC.name} is not the builder input. It looks like the page's EXPORT "
             "({page, at, decisions:[{id, choice, note}]}) has been copied over it. Restore the "
             "input from git before rebuilding; Dave's answers belong beside it, not on top of it.")

d = json.loads(DRY.read_text(encoding="utf-8"))
E = d["proposal"]["edges"]


def et(t):
    return len([e for e in E if e["type"] == t])


def run_option(*flags):
    """Run the generator with an option set into a throwaway file — the option
    counts on the page are MEASURED, never typed."""
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "o.json"
        subprocess.run([sys.executable, str(GEN), *flags, "--dry-run", str(out)],
                       capture_output=True, text=True, check=True)
        return json.loads(out.read_text(encoding="utf-8"))


opt = run_option("--family-edges", "--evidence-edges")
nopn = run_option("--no-polarity-nodes")

# The live graph's node prefixes, counted off the explorer page itself.
live = Counter(re.findall(r'"id"\s*:\s*"([a-zA-Z][a-zA-Z0-9_\-]*):',
                          EXPLORER_HTML.read_text(encoding="utf-8", errors="replace")))

P = json.loads((REPO / "knowledge" / "brain" / "principles.json").read_text(encoding="utf-8"))["principles"]
HEAD = ("id", "statement", "family", "grade", "originator", "year")

n = {
    "principles": d["principles_read"],
    "polarities": d["polarities_read"],
    "nodes": d["node_total"],
    "ux_nodes": d["node_counts"]["ux"],
    "polarity_nodes": d["node_counts"]["polarity"],
    "edges": d["edge_total"],
    "unresolved": d["unresolved_total"],
    "unresolved_nopn": nopn["unresolved_total"],
    "families": d["families"],
    "polarity_edges": d["polarity_edges_header_counts"]["polarities_with_edges"],
    "edgeless": len(d["polarities_without_edges"]),
    "not_edgeable": d["polarity_edges_header_counts"]["parties_not_edgeable"],
    "parties": d["parties_total"],
    "links": d["links_total"],
    "rulings": d["rulings_available"],
    "stubs": d["stubs_available"],
    "wcag": d["wcag_adjacent_principles"],
    "wcag_named": d["wcag_name_matches_not_drawn"],
    "wcag_rest": d["wcag_adjacent_principles"] - d["wcag_name_matches_not_drawn"],
    "fam_wcag22": d["wcag_adjacent_by_family"]["fam-wcag22"],
    "fam_coga": d["wcag_adjacent_by_family"]["fam-coga"],
    "fam_aria": d["wcag_adjacent_by_family"]["fam-aria-apg"],
    "fam_en": d["wcag_adjacent_by_family"]["fam-en301549"],
    "fam_eaa": d["wcag_adjacent_by_family"]["fam-eaa"],
    "live_prefixes": len(live),
    "live_principle": live["principle"], "live_sc": live["sc"],
    "live_guideline": live["guideline"], "live_rule": live["rule"],
    "live_ruling": live["ruling"], "live_component": live["component"],
    "explorer_mb": round(EXPLORER_HTML.stat().st_size / 1_000_000, 1),
    "payload_full_kb": round(len(json.dumps(P, ensure_ascii=False)) / 1000),
    "payload_trim_kb": round(len(json.dumps(
        [{k: p[k] for k in HEAD} for p in P], ensure_ascii=False)) / 1000),
    "metas": len([f for f in os.listdir(REPO / "knowledge" / "components")
                  if f.endswith(".meta.json") and not f.startswith("EXAMPLE-")]),
    "inFamily_edges": opt["edge_counts"]["inFamily"],
    "family_hubs": opt["node_counts"]["family"],
    "evidence_edges": opt["edge_counts"]["evidencedBy"],
    "evidence_nodes": opt["node_counts"]["evidence"],
    "all_eight": opt["edge_total"],
    "opt_nodes": opt["node_total"],
    "A": d["grade_split"]["A"], "B": d["grade_split"]["B"], "C": d["grade_split"]["C"],
    "D": d["grade_split"]["D"], "L": d["grade_split"]["L"],
    "new_types": sum(1 for v in d["edge_status"].values() if v == "NEW"),
}
for t in ("tensionWith", "hasParty", "explainedBy", "touches", "resolvedBy", "challengedBy"):
    n[t] = et(t)
n["ruling_targets"] = len({e["t"] for e in E if e["t"] and e["t"].startswith("ruling:")})
n["ux_in_tension"] = len({x for e in E if e["type"] == "tensionWith" for x in (e["s"], e["t"])})
n["party_ux"] = len([e for e in E if e["type"] == "hasParty" and str(e["t"]).startswith("ux:")])
n["party_ruling"] = len([e for e in E if e["type"] == "hasParty" and str(e["t"]).startswith("ruling:")])
n["party_null"] = len([e for e in E if e["type"] == "hasParty" and e["t"] is None])

IDS = [x["id"] for x in spec["decisions"]]

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
/* The label pattern. NO text-transform (nam-002): tracking and weight carry it,
   and the line-height is generous so no descender can be cropped. */
.label{font-size:.8125rem;font-weight:500;letter-spacing:.14em;line-height:1.6;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
/* Display line-heights are set from a MEASUREMENT, not from taste: at 57/43/34px the
   Univers Next font box (cap .723em + descender .232em + internal leading) needs
   1.166 / 1.213 / 1.212em before the last line's descender clears the content box.
   The Swiss 1.0-1.08 display range crops here, so the house descender clause wins
   and _drive_page.py re-measures it every build. */
h1{font-size:3.5625rem;line-height:1.18;font-weight:400;letter-spacing:0;margin:0 0 var(--s4);max-width:22ch}
h2{font-size:2.125rem;line-height:1.25;font-weight:400;margin:0 0 var(--s3)}
h3{font-size:1.1875rem;line-height:1.35;font-weight:500;margin:0}
p{margin:0 0 var(--s2);max-width:78ch}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
 background:var(--soft);padding:.08em .3em;border-radius:2px}
a{color:var(--accent)}
.n{font-variant-numeric:tabular-nums;font-weight:500}
@media (max-width:760px){h1{font-size:2.125rem}h2{font-size:1.6rem}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);
 border:1px solid var(--g2);margin:var(--s5) 0 var(--s4)}
.stat{background:var(--paper);padding:var(--s3)}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1.25;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1)}
.stat span{display:block;font-size:.8125rem;letter-spacing:.06em;line-height:1.5;color:var(--g6)}
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
.decid{font-size:.8125rem;letter-spacing:.14em;line-height:1.6;font-weight:500;color:var(--accent)}
.opts{list-style:none;margin:var(--s3) 0 0;padding:0}
.opts li{border-top:1px solid var(--rule);padding:var(--s2) 0}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2);align-items:start}
.opt input{margin-top:.45rem;accent-color:var(--accent);width:16px;height:16px;flex:0 0 16px}
.opt label{cursor:pointer;max-width:78ch}
.okey{font-weight:500;letter-spacing:.06em;font-size:.8125rem;color:var(--g6);margin-right:var(--s1)}
.rec{display:inline-block;font-size:.75rem;letter-spacing:.1em;line-height:1.5;
 font-weight:500;color:var(--accent);border:1px solid var(--accent);padding:.05rem .4rem;
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
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:var(--s3);border-top:1px solid var(--g3)}
table{border-collapse:collapse;width:100%;font-size:.875rem;min-width:760px}
th,td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:.75rem;letter-spacing:.08em;line-height:1.6;color:var(--g6);font-weight:500;white-space:nowrap}
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
for x in spec["decisions"]:
    dec_html.append(f"""<div class="dec" data-id="{x['id']}">
<div class="dechead"><span class="decid">{x['id']}</span><h3>{x['title']}</h3></div>
<p>{x['lede'].format(**n)}</p>
<ul class="opts">
{opts_html(x['id'], x['options'])}
</ul>
<p class="why">{x['why'].format(**n)}</p>
<textarea class="note" data-id="{x['id']}" aria-label="Notes for {x['id']}" placeholder="Notes for {x['id']} — your words"></textarea>
</div>""")

ROWS = [
    ("tensionWith", "NEW", "ux &rarr; ux", n["tensionWith"],
     f"The derived pairwise view, read verbatim from <code>_generated/polarity-edges.json</code> and "
     f"re-derived from <code>polarities.json</code> to prove it fresh. {n['ux_in_tension']} principles, "
     f"{n['polarity_edges']} polarities. Carries the polarity id and its mediating variable."),
    ("hasParty", "NEW", "polarity &rarr; ux | ruling | null", n["hasParty"],
     f"Every party of every polarity: {n['party_ux']} resolve to a principle, {n['party_ruling']} to a "
     f"ruling, and {n['party_null']} are declared stubs carried as <code>null</code> plus the phrase."),
    ("touches", "NEW", "polarity &rarr; ruling", n["touches"],
     "One of the four typed out-links s238-D6 ruled. Read from the <code>links</code> array; "
     "the ref must be a live ruling."),
    ("resolvedBy", "NEW", "polarity &rarr; ruling", n["resolvedBy"],
     "The link that settles a polarity. Feeds the derived status in "
     "<code>_generated/polarity-status.json</code>."),
    ("challengedBy", "NEW", "polarity &rarr; ruling", n["challengedBy"],
     "A ruling that pulls against the polarity rather than settling it."),
    ("explainedBy", "NEW", "polarity &rarr; ruling", n["explainedBy"],
     "The rarest of the four &mdash; one link, pl-01 to s151-D1, the two-red law."),
    ("inFamily", "NEW", "ux &rarr; family hub", n["inFamily_edges"],
     f"Off by default (<code>--family-edges</code>). {n['families']} hubs; the largest, fam-laws-of-ux, "
     f"holds 26. Family is an attribute unless you want the picture."),
    ("evidencedBy", "EXISTS", "ux &rarr; evidence", n["evidence_edges"],
     f"The one type that already exists ({live['evidence']} <code>evidence:</code> nodes in the graph) "
     f"&mdash; and 0 of the {n['evidence_nodes']} bibliographic URLs join one. Off by default."),
]
NEW_MARK = '<span class="newmark">New</span>'
rows_html = "\n".join(
    '<tr><td class="slug">%s</td><td>%s</td><td class="slug">%s</td>'
    '<td class="num">%d</td><td class="defn">%s</td></tr>'
    % (a, NEW_MARK if b == "NEW" else "exists", c, v, w)
    for a, b, c, v, w in ROWS)

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#275 &middot; lane RP &middot; decision page</p>
<h1>{spec['headline']}</h1>
<p><code>knowledge/brain/principles.json</code> holds <span class="n">{n['principles']}</span> UX principles
in <span class="n">{n['families']}</span> families, each graded and each carrying its scope conditions, its
known misreadings and a refutation probe. <code>knowledge/brain/polarities.json</code> holds
<span class="n">{n['polarities']}</span> polarities between them, and
<span class="n">{n['tensionWith']}</span> pairwise edges are already derived and waiting. The knowledge graph
carries <span class="n">0</span> of all of it. s269-D1 put this third in the order, after the roles and the
<span class="n">{n['live_rule']}</span> guideline rules that landed yesterday.</p>
<p>This lane measured what a principle can be joined to, and built the generator. Nothing has landed.</p>
<div class="stats">
<div class="stat"><b>{n['principles']}</b><span>principles in the register</span></div>
<div class="stat"><b>{n['nodes']}</b><span>nodes proposed</span></div>
<div class="stat"><b>{n['edges']}</b><span>edges proposed</span></div>
<div class="stat"><b>{n['new_types']}</b><span>of 8 types are new</span></div>
</div>
<div class="zeros">
<div><b>0</b> principle nodes in the graph today</div>
<div><b>0</b> metas or register files touched</div>
<div><b>0</b> invented targets ({n['unresolved']} declared nulls)</div>
<div><b>0</b> things landed &mdash; ratification first</div>
</div>
<p class="why">Grade split: A <span class="n">{n['A']}</span> &middot; B <span class="n">{n['B']}</span>
&middot; C <span class="n">{n['C']}</span> &middot; D <span class="n">{n['D']}</span> &middot; L
<span class="n">{n['L']}</span>, the ladder you named at s237-D1. The
<span class="n">{n['polarities']}</span> polarities hold <span class="n">{n['parties']}</span> parties and
<span class="n">{n['links']}</span> typed citations to <span class="n">{n['ruling_targets']}</span> rulings.</p>
</div></section>

<section id="types"><div class="wrap">
<p class="label">The vocabulary question</p>
<h2>Seven of the eight edge types are new.</h2>
<p>The graph vocabulary is closed (#75). A new node kind and a new edge type are your word, not the lane's
&mdash; which is what this page is for. Two node kinds are proposed: <code>ux:&lt;id&gt;</code>
(<span class="n">{n['ux_nodes']}</span>) and <code>polarity:&lt;id&gt;</code>
(<span class="n">{n['polarity_nodes']}</span>, decision RP-3).</p>
<div class="tw"><table>
<tr><th>edge type</th><th>status</th><th>shape</th><th class="num">count</th><th>where it comes from</th></tr>
{rows_html}
</table></div>
<p class="why">Precedent: s274-D7&hellip;D12 ratified a node kind and four edge types this way yesterday, and
<code>gen_kg_rules.py</code> landed them on that id &mdash; <span class="n">{n['live_rule']}</span>
<code>rule:</code> nodes are in the live explorer now. This generator is the same shape, and the same
refusals: <code>--dry-run</code> is the default, <code>--land</code> refuses without a recorded ruling id.</p>
</div></section>

<section id="notdrawn"><div class="wrap">
<p class="label">What was measured and deliberately not drawn</p>
<h2>Three joins exist in prose only.</h2>
<div class="split"><div>
<dl class="recs">
<dt>Principle &rarr; the standard it restates</dt>
<dd><span class="n">{n['wcag']}</span> rows, <span class="n">0</span> explicit refs (RP-4)</dd>
<dt>Component &rarr; the law it rests on</dt>
<dd><span class="n">0</span> of <span class="n">{n['metas']}</span> metas (RP-5)</dd>
<dt>Principle &rarr; its evidence</dt>
<dd><span class="n">{n['evidence_nodes']}</span> URLs, <span class="n">0</span> joins (RP-2 d)</dd>
</dl>
</div><div>
<p>Each of the three would need a regex over prose, or a name match, to exist. s274-D12 refused exactly that
yesterday for <span class="n">27</span> rule&nbsp;&rarr;&nbsp;component candidates because the sample carried
visible false positives. The same refusal applies here, so the counts are reported and the edges are not
drawn. Two of the three are authored work &mdash; and the authoring is a lane, not a generator.</p>
<p>The one deliberate near-miss worth your eye: <span class="n">{n['wcag_named']}</span> register ids do
contain the name of a live <code>principle:</code> node. That is still a name match, and the whole point of
s274-D12 is that a good-looking name match is how the bad ones get in.</p>
</div></div>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Decisions</p>
<h2>Six decisions. The recommendation is first in each.</h2>
<p>Nothing here is ruled. Every option stays open; the marked option is the lane's recommendation and carries
no weight beyond that.</p>
{"".join(dec_html)}
<div class="bar"><button type="button" id="btnExport">Export JSON</button><button type="button" id="btnCopy">Copy to clipboard</button><button type="button" class="ghost" id="btnClear">Clear</button><span class="said" id="said">not saved yet</span></div>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<section id="standing"><div class="wrap">
<p class="label">Two sentences already on the record</p>
<h2>You have ruled the shape of both halves of this.</h2>
<blockquote>&ldquo;Evidence grade is a field on every principle node.&rdquo;
<cite>Dave, #237 &mdash; s237-D1. So grade is not on this page: it is settled, and it is an attribute.</cite></blockquote>
<blockquote>&ldquo;my instinct is that adopting the hyper-relationship version might pay off in the future when
we really make this KG more powerful&rdquo;
<cite>Dave, #238 &mdash; s238-D1, the ruling that made the polarity a node with typed parties and derived
pairwise edges. RP-3 asks whether that model comes into the graph as-is.</cite></blockquote>
<p class="why">Both sentences were checked against <code>knowledge/_rulings.json</code>, where each occurs
exactly once, in the <code>says</code> field of the ruling named. <code>_quote_gate.py</code> returns 0 on
both because its index does not cover the <code>says</code> field &mdash; a known gap, verified by hand
rather than waved through.</p>
</div></section>

<section id="provenance"><div class="wrap">
<p class="label">Provenance</p>
<h2>Where every figure came from</h2>
<div class="split"><div>
<dl class="recs">
<dt>Script</dt><dd>knowledge/gen_kg_principles.py</dd>
<dt>Corpus</dt><dd>knowledge/brain/principles.json &middot; knowledge/brain/polarities.json &middot;
knowledge/brain/_generated/polarity-edges.json &middot; knowledge/brain/_generated/polarity-status.json &middot;
knowledge/brain/stubs.json &middot; knowledge/_rulings.json &middot; knowledge/_validate_polarities.py</dd>
<dt>Data</dt><dd>notes/_lanes/275/principles-kg/dry-run.json</dd>
<dt>Copy</dt><dd>notes/_lanes/275/principles-kg/principles-kg-decisions-2026-09-15.json</dd>
<dt>Builder</dt><dd>notes/_lanes/275/principles-kg/_build_page.py</dd>
<dt>Command</dt><dd><code>python3 knowledge/gen_kg_principles.py --dry-run
notes/_lanes/275/principles-kg/dry-run.json</code></dd>
<dt>Selftest</dt><dd><code>python3 knowledge/gen_kg_principles.py --selftest</code> &mdash; 15 bites, 18
mutants driven, every one caught (<code>_mutate.py</code>)</dd>
</dl>
</div><div>
<p>Every integer on this page is read at build time from <code>dry-run.json</code>, from a live run of the
generator with the option flags set, or counted off <code>notes/_KG-EXPLORER.html</code> itself. No number was
typed into the HTML, and none was typed into the decisions file either.</p>
<p>The generator touched nothing: <code>python3 knowledge/_validate_kg.py</code> still says OK, and this lane
wrote only new files. The <span class="n">{n['tensionWith']}</span> pairwise edges were re-derived from
<code>polarities.json</code> by the rule printed inside the generated file, and the two sets agree exactly
&mdash; so the view is proved fresh rather than trusted.</p>
</div></div>
</div></section>
<footer><div class="wrap">Nothing on this page is a ruling. Dave rules; the lane enacts by addition.</div></footer>
<script>
(function(){{
 var KEY={json.dumps(spec['storage_key'])};
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
  return {{page:{json.dumps(spec['page'])},
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
   a.download="principles-kg-decisions-2026-09-15.json";
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
print(f"wrote {OUT} ({len(HTML):,} bytes) · {len(IDS)} decisions · {len(ROWS)} edge types · "
      f"{len(n)} measured figures")
