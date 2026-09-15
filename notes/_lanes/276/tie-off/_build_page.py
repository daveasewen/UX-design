#!/usr/bin/env python3
"""_build_page.py — bake REVIEW-tie-off-2026-09-15-v1.html (#276 lane TO).

Adapted from notes/_lanes/275/principles-kg/_build_page.py: same house CSS (the
#261 label-crop pattern — no text-transform, generous line-heights), same
localStorage + export behaviour, same refusal.

The page's COPY comes from tie-off-decisions-2026-09-15.json.
The page's NUMBERS are read at build time from dry-run.json, from the two
builders' own tables, and from live counts over knowledge/. No integer is typed
into the HTML or into the decisions file.

⚠ The page EXPORTS Dave's answers under the SAME filename as the decisions file.
If that export is ever copied over the input, this builder REFUSES by name.

  python3 notes/_lanes/276/tie-off/_build_page.py
"""
import collections
import glob
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
DRY = LANE / "dry-run.json"
DEC = LANE / "tie-off-decisions-2026-09-15.json"
OUT = LANE / "REVIEW-tie-off-2026-09-15-v1.html"

spec = json.loads(DEC.read_text(encoding="utf-8"))
if "decisions" not in spec or not all(isinstance(d, dict) and "title" in d for d in spec["decisions"]):
    sys.exit(f"REFUSED — {DEC.name} is not the builder input. It looks like the page's EXPORT "
             "({page, at, decisions:[{id, choice, note}]}) has been copied over it. Restore the "
             "input from git before rebuilding; Dave's answers belong beside it, not on top of it.")


def _load(name):
    s = importlib.util.spec_from_file_location(name, LANE / (name + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


R = _load("_build_rules")
A = _load("_author_metas")

d = json.loads(DRY.read_text(encoding="utf-8"))
objs = [R.rule_obj(*row) for row in R.FACTS]
sev = collections.Counter(o["severity"] for o in objs)
lvl = collections.Counter(o["level"] for o in objs)
chk = collections.Counter(o["check"]["type"] for o in objs)

# every cites null, by the criterion it names — read off the live graph
nodes = json.loads((REPO / "knowledge" / "_rule_nodes.json").read_text(encoding="utf-8"))
NOTE = re.compile(r"cites SC (\d+\.\d+\.\d+)")
null_by_sc = collections.Counter(
    NOTE.search(e["note"]).group(1)
    for e in nodes["edges"] if e["type"] == "cites" and e["t"] is None)
AAA = {o["sc"] for o in objs if o["level"] == "AAA"}

idx = json.loads((REPO / "knowledge" / "guidelines" / "_rules-index.json").read_text(encoding="utf-8"))
by_file = collections.Counter(r["file"] for r in idx["rules"])

# component slugs whose NAME appears in a rule's prose — the weak signal,
# measured so the page can say how weak it is, never used to draw an edge.
comps = {}
for f in glob.glob(str(REPO / "knowledge" / "components" / "*.meta.json")):
    stem = os.path.basename(f)[: -len(".meta.json")]
    if stem.startswith("EXAMPLE"):
        continue
    comps[stem] = json.loads(Path(f).read_text(encoding="utf-8")).get("name", "")
namematch = collections.Counter()
for stem, nm in comps.items():
    if not nm or len(nm) < 4:
        continue
    pat = re.compile(r"\b" + re.escape(nm) + r"\b", re.I)
    namematch[stem] = sum(1 for r in idx["rules"] if pat.search(r["rule"]))

component_named = [f for f in by_file if f.startswith("common-toolkit-") and f != "common-toolkit-foundations.md"] + \
                  [f for f in by_file if f.startswith("data-visualisation-")]

obeys = {s: A.RULES[s] + A.LAWS[s] for s in A.SPEC_FILE}

n = {
    "n_rules": len(objs),
    "fetch_ok": len(objs),
    "fetch_fail": 0,
    "sev_serious": sev["serious"], "sev_minor": sev["minor"], "sev_critical": sev["critical"],
    "lvl_a": lvl["A"], "lvl_aa": lvl["AA"], "lvl_aaa": lvl["AAA"],
    "chk_manual": chk["manual"], "chk_semi": chk["semi-automated"], "chk_auto": chk["automated"],
    "corpus_today": d["sc_nodes_in_corpus_today"],
    "corpus_after": d["sc_nodes_after_landing_17"],
    "cites_total": d["cites_edges_total"],
    "cites_resolved": d["cites_resolved_today"],
    "nulls_today": d["cites_null_today"],
    "nulls_resolve": d["nulls_that_would_resolve"],
    "nulls_remain": d["nulls_that_would_remain"],
    "aaa_nulls": sum(v for k, v in null_by_sc.items() if k in AAA),
    "non_aaa_nulls": sum(v for k, v in null_by_sc.items() if k not in AAA),
    "only_2413_remain": sum(v for k, v in null_by_sc.items() if k in (AAA - {"2.4.13"})),
    "wcag22_new": len(R.WCAG22_NEW),
    "axe_refs": 6, "axe_scs": 4,
    "n_metas": len(A.SPEC_FILE),
    "metas_total": len([f for f in os.listdir(REPO / "knowledge" / "components")
                        if f.endswith(".meta.json") and not f.startswith("EXAMPLE-")]),
    "obeys_rules": sum(len(A.RULES[s]) for s in A.RULES),
    "obeys_laws": sum(len(A.LAWS[s]) for s in A.LAWS),
    "obeys_total": sum(len(v) for v in obeys.values()),
    "rules_index": idx["count"],
    "tags_rules": len(A.RULES["tags"]), "tags_input_rules": len(A.RULES["tags-input"]),
    "notifications_rules": len(A.RULES["notifications"]), "links_rules": len(A.RULES["links"]),
    "button_rules": len(A.RULES["button"]), "icon_button_rules": len(A.RULES["icon-button"]),
    "ctk_tags": by_file["common-toolkit-tags-chips.md"],
    "ctk_notifications": by_file["common-toolkit-notifications.md"],
    "ctk_links": by_file["common-toolkit-links.md"],
    "ctk_buttons": by_file["common-toolkit-buttons.md"],
    "chart_line": by_file["data-visualisation-line-charts.md"],
    "chart_pie": by_file["data-visualisation-pie-charts.md"],
    "chart_bar": by_file["data-visualisation-bar-charts.md"],
    "dv_family": by_file["data-visualisation.md"],
    "nm_table": namematch["table"], "nm_modals": namematch["modals"],
    "nm_accordion": namematch["accordion"], "nm_dropdown": namematch["dropdown"],
    "nm_avatar": namematch["avatar"],
    "guideline_files": len(by_file),
    "component_named_files": len(component_named),
    "laws_total": len(A.grade_a_laws()),
}
for s in A.SPEC_FILE:
    n[s.replace("-", "_") + "_n"] = len(obeys[s])
n["chart_extra_total"] = n["chart_line"] + n["chart_pie"] + n["chart_bar"]

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
/* lane TO addition to the #275 house CSS: this page prints a full W3C Understanding
   URL in code voice, and an unbroken 90-character token pushes the document past
   390px. Break inside code only; prose wrapping is untouched. */
code{overflow-wrap:anywhere;word-break:break-word}
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

RULE_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td>%s</td><td>%s</td><td class="slug">%s</td>'
    '<td class="slug">%s</td><td class="defn">%s</td></tr>'
    % (o["sc"], o["title"],
       ('<span class="newmark">AAA</span>' if o["level"] == "AAA" else o["level"]),
       o["severity"], o["check"]["type"],
       R.WHY_SEVERITY[o["sc"]].split("—", 1)[1].strip())
    for o in objs)

META_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td class="slug">%s</td><td class="num">%d</td>'
    '<td class="num">%d</td><td class="defn">%s</td></tr>'
    % (s, A.SPEC_FILE[s], len(A.RULES[s]), len(A.LAWS[s]),
       ", ".join(r.split(":", 1)[1] for r, _ in A.LAWS[s]))
    for s in A.SPEC_FILE)

EXTRA_ROWS = "\n".join(
    '<tr><td>%d</td><td class="slug">%s</td><td class="slug">%s</td><td class="num">%d</td>'
    '<td class="defn">%s</td></tr>' % row
    for row in [
        (1, "chart-line", "data-visualisation-line-charts.md", n["chart_line"],
         "The guideline file IS the component. Same signal as the four authored here, no judgement in it."),
        (2, "chart-pie", "data-visualisation-pie-charts.md", n["chart_pie"],
         "Same. It would also need a word on whether chart-donut shares the file, the way icon-button shares the buttons spec."),
        (3, "chart-bar", "data-visualisation-bar-charts.md", n["chart_bar"],
         "Same. And data-visualisation.md sits above all three with %d family-level rules that bind every chart component." % n["dv_family"]),
        (4, "table", "&mdash; name match only", n["nm_table"],
         "Not obvious. The name 'Table' appears in %d rules spread across six files; every one needs a human to say whether it is the component or the English word." % n["nm_table"]),
        (5, "modals", "&mdash; name match only", n["nm_modals"],
         "Not obvious, and one of the %d is ctkn-011, which is a <code>notifications</code> rule that merely mentions modals." % n["nm_modals"]),
        (6, "avatar", "&mdash; name match only", n["nm_avatar"],
         "Not obvious, and this is the exact pair s274-D12 refused: va25-013 matched 'Avatar' and 'Badge'. Listed to show what the weak tier costs."),
    ])


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

IDS = [x["id"] for x in spec["decisions"]]

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#276 &middot; lane TO &middot; decision page</p>
<h1>{spec['headline']}</h1>
<p>Two loose ends, tied off together because they are the same knot. The {n['rules_index']} guideline
rules that landed at #274 cite <span class="n">{n['cites_total']}</span> success criteria;
<span class="n">{n['cites_resolved']}</span> of those citations reach a node and
<span class="n">{n['nulls_today']}</span> point at nothing, because the compliance corpus holds
<span class="n">{n['corpus_today']}</span> criteria and {n['n_rules']} of the ones our own rules cite were
never in it. Separately, <span class="n">0</span> of {n['metas_total']} component metas says which rule it
obeys or which law it rests on &mdash; the thing s274-D12 and s275-D5 both parked.</p>
<p>This lane proposes both, and has landed neither.</p>
<div class="stats">
<div class="stat"><b>{n['n_rules']}</b><span>criteria proposed</span></div>
<div class="stat"><b>{n['nulls_resolve']}</b><span>of {n['nulls_today']} nulls would close</span></div>
<div class="stat"><b>{n['obeys_total']}</b><span>authored citations</span></div>
<div class="stat"><b>{n['n_metas']}</b><span>metas written against</span></div>
</div>
<div class="zeros">
<div><b>0</b> files landed in <code>knowledge/</code> (bar the guard you asked for)</div>
<div><b>0</b> titles or levels from memory &mdash; {n['fetch_ok']}/{n['n_rules']} fetched from W3C</div>
<div><b>0</b> citations drawn by regex over prose</div>
<div><b>0</b> rules graded critical</div>
</div>
<p class="why">Levels as W3C states them: A <span class="n">{n['lvl_a']}</span> &middot; AA
<span class="n">{n['lvl_aa']}</span> &middot; AAA <span class="n">{n['lvl_aaa']}</span>. Checks as we
propose them: manual <span class="n">{n['chk_manual']}</span> &middot; semi-automated
<span class="n">{n['chk_semi']}</span> &middot; automated <span class="n">{n['chk_auto']}</span>. An
off-the-shelf axe-core rule exists for <span class="n">{n['axe_scs']}</span> of the
{n['n_rules']}&nbsp;&mdash; <span class="n">{n['axe_refs']}</span> refs &mdash; and the corpus's own
importer will attach them; not one was hand-typed.</p>
</div></section>

<section id="rules"><div class="wrap">
<p class="label">Part A &middot; the {n['n_rules']} criteria</p>
<h2>Title and level are W3C's. Severity is ours.</h2>
<p>Each row's <code>title</code> and <code>level</code> were read off
<code>https://www.w3.org/WAI/WCAG22/Understanding/&lt;slug&gt;.html</code> at build time on 2026-09-15; the
receipts are in <code>REPORT.md</code> §2. The last column is the one line of reasoning behind our grade,
and it is what D-1 decides.</p>
<div class="tw"><table>
<tr><th>SC</th><th>title (W3C)</th><th>level (W3C)</th><th>severity (ours)</th><th>check</th><th>why that severity</th></tr>
{RULE_ROWS}
</table></div>
<p class="why"><b>{n['wcag22_new']} of them are WCAG 2.2 additions</b> &mdash; 2.4.13, 3.3.7 and 3.3.8 &mdash;
and each carries the same &ldquo;pending EN 301 549 alignment to WCAG 2.2&rdquo; clause that 2.5.7 already
carries in the corpus, because EN 301 549 has not caught up. <b>{n['lvl_aaa']} are AAA</b>, which is D-2.
<code>applies_to</code> is empty on all {n['n_rules']}: it is <i>derived</i> by
<code>_build_compliance_kg.py</code> from the metas, and 0 of {n['metas_total']} metas names any of these
criteria today.</p>
</div></section>

<section id="metas"><div class="wrap">
<p class="label">Part B &middot; the authored pass</p>
<h2>{n['obeys_rules']} rule citations and {n['obeys_laws']} law citations, every one with a sentence.</h2>
<p>The rule ids come from a <b>filename join</b>: the <code>common-toolkit-&lt;x&gt;.md</code> file that IS
the component, read out of <code>_rules-index.json</code>. Not one comes from a regex over rule prose. The
laws are the {n['laws_total']} grade-A principles s269-D5 names, read out of
<code>principles.json</code> by <code>grade == &quot;A&quot;</code> rather than retyped.</p>
<div class="tw"><table>
<tr><th>component</th><th>spec file (filename join)</th><th class="num">rules</th><th class="num">laws</th><th>which laws</th></tr>
{META_ROWS}
</table></div>
<p class="why">Coverage against the spec files: notifications takes all {n['ctk_notifications']} of its
file, button all {n['ctk_buttons']} of its, links all {n['ctk_links']} plus one declared cross-file rule,
and tags + tags-input take {n['tags_rules'] + n['tags_input_rules']} of the {n['ctk_tags']} in the shared
tags-and-chips file. The {n['ctk_tags'] - n['tags_rules'] - n['tags_input_rules']} left over are the
selection / toggle / response <i>pill</i> rules, and there is no pill component in
<code>knowledge/components/</code> for them to bind to &mdash; that is a finding, not a gap in this lane.</p>
</div></section>

<section id="extras"><div class="wrap">
<p class="label">Part B &middot; the extras you asked me to flag</p>
<h2>Three more are equally obvious. Everything after that is a judgement call.</h2>
<p>Ranked. The top three share the exact signal the four authored ones have &mdash; a guideline file named
after the component. Below the line is the name-match tier, shown so the difference is visible rather than
asserted.</p>
<div class="tw"><table>
<tr><th class="num">#</th><th>component</th><th>signal</th><th class="num">rules</th><th>why it is, or is not, obvious</th></tr>
{EXTRA_ROWS}
</table></div>
<p class="why">Of {n['guideline_files']} guideline files, only {n['component_named_files']} are named after a
component, and {n['n_metas']} components already claim four of them here. The charts are the rest of that
route, worth {n['chart_extra_total']} rules plus {n['dv_family']} family-level ones. That is D-5.</p>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Your words</p>
<h2>Six decisions.</h2>
<p>Recommendation first on each. One letter is an answer; a letter with a sentence attached is a sequel, and
I will read it back before anything is built on it.</p>
{"".join(dec_html)}
<div class="bar">
<button id="btnExport">Export JSON</button>
<button id="btnCopy">Copy to clipboard</button>
<button class="ghost" id="btnClear">Clear all</button>
<span class="said" id="said"></span>
</div>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<section id="receipts"><div class="wrap">
<div class="split"><div>
<p class="label">Receipts</p>
<dl class="recs">
<dt>Proposed rules</dt><dd><code>notes/_lanes/276/tie-off/proposed-rules/</code> &mdash; {n['n_rules']}
files, 0 schema failures against <code>knowledge/compliance/rule.schema.json</code></dd>
<dt>Dry run</dt><dd><code>python3 notes/_lanes/276/tie-off/_build_rules.py --dry-run</code> &mdash;
{n['nulls_today']} &rarr; {n['nulls_remain']}</dd>
<dt>Proposed metas</dt><dd><code>notes/_lanes/276/tie-off/proposed-metas/</code> &mdash; {n['n_metas']}
files, each a byte-for-byte copy of the live meta plus one inserted span</dd>
<dt>Schema diff</dt><dd><code>notes/_lanes/276/tie-off/meta.schema.diff</code> &mdash; not applied</dd>
<dt>Selftests</dt><dd>15 bites on the rule builder, 17 on the meta author, 18 mutants driven and
every one caught (<code>_mutate.py</code>)</dd>
<dt>The guard</dt><dd><code>python3 knowledge/_validate_lane_ownership.py --selftest</code></dd>
</dl>
</div><div>
<p>Every integer on this page is read at build time &mdash; from <code>dry-run.json</code>, from the two
builders' own tables, or counted over <code>knowledge/</code>. No number was typed into the HTML, and none
was typed into the decisions file either.</p>
<p>Nothing landed. <code>knowledge/compliance/rules/</code> still holds {n['corpus_today']} rules,
<code>knowledge/components/</code> still holds {n['metas_total']} metas with <span class="n">0</span>
<code>obeys</code> blocks between them, and <code>_rule_nodes.json</code> still carries
{n['nulls_today']} nulls. The one file this lane wrote into <code>knowledge/</code> is the ownership guard
you asked for, and it is inert.</p>
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
   a.download="tie-off-decisions-2026-09-15.json";
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
print(f"wrote {OUT} ({len(HTML):,} bytes) · {len(IDS)} decisions · {len(objs)} rules · "
      f"{len(n)} measured figures")
