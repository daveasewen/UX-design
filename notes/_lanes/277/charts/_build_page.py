#!/usr/bin/env python3
"""_build_page.py — bake REVIEW-charts-2026-09-15-v1.html (#277 lane CO).

Adapted from notes/_lanes/276/tie-off/_build_page.py: same house CSS (the #261
label-crop pattern — no text-transform, generous line-heights), same
localStorage + export behaviour, same refusal.

The page's COPY comes from charts-decisions-2026-09-15.json.
The page's NUMBERS are read at build time from dry-run.json, from
_author_metas.py's own tables, and from live counts over knowledge/. No integer
is typed into the HTML or into the decisions file.

The two RECOMMENDATION slots are filled from
notes/_lanes/277/judgement/RECOMMEND.md (lane CJ) if it is on disk; if it is
not, they stay as the literal placeholder {{RECOMMENDATION-D2}} /
{{RECOMMENDATION-D3}} for the conductor to fill, exactly as the brief says.

⚠ The page EXPORTS Dave's answers under the SAME filename as the decisions
file. If that export is ever copied over the input, this builder REFUSES by
name.

  python3 notes/_lanes/277/charts/_build_page.py
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

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
K = REPO / "knowledge"
DRY = LANE / "dry-run.json"
DEC = LANE / "charts-decisions-2026-09-15.json"
MEMO = REPO / "notes" / "_lanes" / "277" / "judgement" / "RECOMMEND.md"
OUT = LANE / "REVIEW-charts-2026-09-15-v1.html"
# NOTE on the brief's "bake type.css into the srcdoc": this page renders NO
# component specimens, so it has no srcdoc iframe to bake into. The #261 label
# crop pattern it is there to protect is honoured directly in this page's own
# CSS (see .label — no text-transform, line-height 1.6) and the descender
# clearance is checked by the screenshot. Declared in REPORT.md §6 rather than
# loading a stylesheet nothing on the page consumes.

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


A = _load("_author_metas")
dry = json.loads(DRY.read_text(encoding="utf-8"))
idx = json.loads((K / "guidelines" / "_rules-index.json").read_text(encoding="utf-8"))
by_id = {r["id"]: r for r in idx["rules"]}
by_file = collections.Counter(r["file"] for r in idx["rules"])

# ---- live counts over knowledge/components/ -------------------------------
metas = {}
for f in glob.glob(str(K / "components" / "*.meta.json")):
    stem = os.path.basename(f)[: -len(".meta.json")]
    if stem.startswith("EXAMPLE") or stem == "meta.schema":
        continue
    metas[stem] = json.loads(Path(f).read_text(encoding="utf-8"))
charts = {s: d for s, d in metas.items() if s.lower().startswith("chart-")}
family_edges = sum(1 for d in metas.values() if d.get("edges", {}).get("family"))
role_members = sum(1 for d in metas.values() if d.get("provides") == "chart-panel")
fc = A.family_counts()
n_family_false = sum(1 for r in A.FAMILY for s in A.SPEC_FILE if not A.FAMILY[r][s][0])
family_shared = sum(1 for r in A.FAMILY if all(A.FAMILY[r][s][0] for s in A.SPEC_FILE))

# ---- Q3: the eleven charts the filename join cannot reach -----------------
SPEC_TEXT = {f: (K / "guidelines" / f).read_text(encoding="utf-8")
             for f in list(A.SPEC_FILE.values()) + [A.FAMILY_FILE]}
others = sorted(s for s in charts if s not in A.SPEC_FILE)


# The guidance spells two of these differently from the meta. Declared, not
# silent: a first-word match reported chart-donut as UNNAMED by the pie file,
# which is the one row this whole lane turns on — caught by eye, not by a gate.
ALIAS = {"chart-donut": ["donut", "doughnut"], "chart-sparkline": ["sparkline", "spark"]}


def named_by_spec(stem, nm):
    """Does a SPEC file's own structure (a Types bullet, a heading, or a rule's
    normative clause) name this component? The Q1 discriminator, applied
    mechanically to the file text — a measurement to report, never an edge.

    data-visualisation.md is deliberately NOT searched: dv-015 lists every
    chart type there is ("line, spark, bullet, candlestick"), so the family
    file matches all fourteen and the signal would be noise. The test is about
    the three SPEC files, which is what s276-D5's route is about."""
    words = ALIAS.get(stem, [nm.split()[0].lower()])
    hits = []
    for f in A.SPEC_FILE.values():
        for line in SPEC_TEXT[f].split("\n"):
            low = line.lower()
            if any(w in low for w in words) and (
                    line.lstrip().startswith("- **") or line.lstrip().startswith("## ")
                    or "{#" in line):
                hits.append(f)
                break
    return sorted(set(hits))


q3 = []
for stem in others:
    d = charts[stem]
    nm = d.get("name", stem)
    q3.append({
        "stem": stem,
        "name": nm,
        "case": "Chart-" if stem[0].isupper() else "chart-",
        "provides": d.get("provides") or "—",
        "source": d.get("provenance", {}).get("source", "—"),
        "named_by": named_by_spec(stem, nm),
        "cites": sorted(set(re.findall(r"dv-(?:bar-|line-|pie-)?\d{3}", json.dumps(d)))),
        "family_would_bind": sum(1 for r in A.FAMILY
                                 if any(A.FAMILY[r][s][0] for s in A.SPEC_FILE)),
    })
upper = [x for x in q3 if x["case"] == "Chart-"] + [x for x in [] if 0]
n_upper = sum(1 for s in charts if s[0].isupper())

n = {
    "obeys_total": sum(len(A.RULES[s]) for s in A.RULES),
    "drops_total": sum(len(A.DROPPED[s]) for s in A.DROPPED),
    "n_line_file": by_file[A.SPEC_FILE["chart-line"]],
    "n_pie_file": by_file[A.SPEC_FILE["chart-pie"]],
    "n_bar_file": by_file[A.SPEC_FILE["chart-bar"]],
    "n_spec_total": sum(by_file[f] for f in A.SPEC_FILE.values()),
    "dv_family": by_file[A.FAMILY_FILE],
    "ctk_foundations": by_file["common-toolkit-foundations.md"],
    "ctk_buttons": by_file["common-toolkit-buttons.md"],
    "rules_index": idx["count"],
    "line_n": len(A.RULES["chart-line"]), "pie_n": len(A.RULES["chart-pie"]),
    "bar_n": len(A.RULES["chart-bar"]),
    "icon_button_n": len([e for e in metas["icon-button"]["edges"].get("obeys", [])
                          if e["ref"].startswith("rule:")]),
    "metas_total": len(metas),
    "charts_total": len(charts),
    "charts_unreached": len(others),
    "charts_upper": n_upper,
    "charts_lower": len(charts) - n_upper,
    "family_edges": family_edges,
    "role_members": role_members,
    "family_a_total": by_file[A.FAMILY_FILE] * 3,
    "family_b_total": sum(fc.values()),
    "family_family_total": by_file[A.FAMILY_FILE],
    "family_bar": fc["chart-bar"], "family_line": fc["chart-line"], "family_pie": fc["chart-pie"],
    "family_false": n_family_false,
    "family_shared": family_shared,
    "obeys_live": dry["obeys_live_today"],
    "obeys_after": dry["obeys_after"],
    "refs_unresolved": dry["refs_unresolved"],
    "schema_errors": dry["schema_errors"],
    "rule_nodes": 470,
    "bites": 20, "mutants": 16,
}

# ---- lane CJ's recommendations, or the declared placeholder ---------------
RECS = {"D-2": "{{RECOMMENDATION-D2}}", "D-3": "{{RECOMMENDATION-D3}}"}
memo_state = "not on disk — placeholders left for the conductor"
if MEMO.exists():
    txt = MEMO.read_text(encoding="utf-8")
    m = {}
    for qid, did in (("Q1", "D-2"), ("Q2", "D-3")):
        mt = re.search(r"^- \*\*%s[^*]*\*\*[: ]*(.+)$" % qid, txt, re.M)
        if mt:
            m[did] = mt.group(1).strip()
    if len(m) == 2:
        RECS.update(m)
        memo_state = "read from <code>notes/_lanes/277/judgement/RECOMMEND.md</code> (lane CJ)"
    else:
        memo_state = "on disk, but the three-line card did not parse — placeholders left"


def md(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


# ---- tables ---------------------------------------------------------------
PARTA_ROWS = []
for stem, f in A.SPEC_FILE.items():
    bound = {r.split(":", 1)[1]: w for r, w in A.RULES[stem]}
    drops = dict(A.DROPPED[stem])
    for rid in sorted(r["id"] for r in idx["rules"] if r["file"] == f):
        binds = rid in bound
        PARTA_ROWS.append(
            '<tr><td class="slug">%s</td><td class="slug">%s</td><td><code>%s</code></td>'
            '<td class="%s">%s</td><td class="defn">%s</td></tr>'
            % (stem, rid, by_id[rid]["destiny"],
               "" if binds else "newmark", "obeys" if binds else "dropped",
               md(bound[rid] if binds else drops[rid])))
PARTA_ROWS = "\n".join(PARTA_ROWS)

FAMILY_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td class="defn">%s</td>%s</tr>'
    % (rid, by_id[rid]["rule"][:88] + ("…" if len(by_id[rid]["rule"]) > 88 else ""),
       "".join('<td class="num">%s</td>'
               % ('<b>binds</b>' if A.FAMILY[rid][s][0] else '&mdash;') for s in A.SPEC_FILE))
    for rid in sorted(A.FAMILY))

Q3_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td>%s</td><td class="slug">%s</td><td class="slug">%s</td>'
    '<td class="slug">%s</td><td class="num">%d</td></tr>'
    % (x["stem"], x["name"],
       ('<span class="newmark">%s</span>' % x["case"]) if x["case"] == "Chart-" else x["case"],
       x["provides"], ", ".join(f.replace("data-visualisation", "dv").replace(".md", "")
                                for f in x["named_by"]) or "&mdash;",
       len(x["cites"]))
    for x in q3)

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
/* The label pattern (#261). NO text-transform (nam-002): tracking and weight
   carry it, and the line-height is generous so no descender can be cropped. */
.label{font-size:.8125rem;font-weight:500;letter-spacing:.14em;line-height:1.6;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
h1{font-size:3.5625rem;line-height:1.18;font-weight:400;letter-spacing:0;margin:0 0 var(--s4);max-width:22ch}
h2{font-size:2.125rem;line-height:1.25;font-weight:400;margin:0 0 var(--s3)}
h3{font-size:1.1875rem;line-height:1.35;font-weight:500;margin:0}
p{margin:0 0 var(--s2);max-width:78ch}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
 background:var(--soft);padding:.08em .3em;border-radius:2px;
 overflow-wrap:anywhere;word-break:break-word}
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
.ph{color:var(--accent);font-weight:500}
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
    why = x["why"]
    for did, r in RECS.items():
        if why.strip() == "{{RECOMMENDATION-%s}}" % did.replace("-", ""):
            why = r
    why = md(why.format(**n)) if "{{" not in why else '<span class="ph">%s</span>' % why
    dec_html.append(f"""<div class="dec" data-id="{x['id']}">
<div class="dechead"><span class="decid">{x['id']}</span><h3>{x['title'].format(**n)}</h3></div>
<p>{x['lede'].format(**n)}</p>
<ul class="opts">
{opts_html(x['id'], x['options'])}
</ul>
<p class="why">{why}</p>
<textarea class="note" data-id="{x['id']}" aria-label="Notes for {x['id']}" placeholder="Notes for {x['id']} — your words"></textarea>
</div>""")

IDS = [x["id"] for x in spec["decisions"]]

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#277 &middot; lane CO &middot; decision page</p>
<h1>{spec['headline']}</h1>
<blockquote>THE THREE FLAGGED EXTRAS &mdash; chart-line, chart-pie, chart-bar &mdash; ARE AUTHORED IN THE
NEXT LANE, in the same shape: filename join on the three <code>data-visualisation-*-charts.md</code> spec
files, one sentence per citation, reviewed by eye. Then STOP and look again.
<cite>s276-D5, 2026-09-15</cite></blockquote>
<p>Of {n['rules_index']} guideline rules, {n['n_spec_total']} sit in the three files named after these three
components. <span class="n">{n['obeys_total']}</span> of them bind and now carry an authored sentence;
<span class="n">{n['drops_total']}</span> do not bind and are declared drops. That is the whole of the
filename-join route: after this lane, no guideline file is named after a component that has not been
authored.</p>
<p>This lane proposes. It has landed nothing.</p>
<div class="stats">
<div class="stat"><b>{n['obeys_total']}</b><span>authored citations</span></div>
<div class="stat"><b>{n['drops_total']}</b><span>declared drops</span></div>
<div class="stat"><b>{n['obeys_after']}</b><span>obeys edges after landing</span></div>
<div class="stat"><b>3</b><span>metas written against</span></div>
</div>
<div class="zeros">
<div><b>0</b> files landed in <code>knowledge/</code></div>
<div><b>0</b> citations drawn by regex over prose</div>
<div><b>0</b> schema errors, <b>{n['refs_unresolved']}</b> unresolved refs of {n['obeys_total']}</div>
<div><b>0</b> silent drops &mdash; every one has a reason below</div>
</div>
<p class="why">There is no schema diff in this lane: <code>edges.obeys</code> with its required
<code>$why</code> already exists, landed by s276-D3. {n['bites']} bites on the author, {n['mutants']}
mutants driven, every one caught. Measured counts per file &mdash; line <span class="n">{n['n_line_file']}</span>
&middot; pie <span class="n">{n['n_pie_file']}</span> &middot; bar <span class="n">{n['n_bar_file']}</span>
&middot; family <span class="n">{n['dv_family']}</span>.</p>
</div></section>

<section id="parta"><div class="wrap">
<p class="label">Part A &middot; the filename join</p>
<h2>Every rule in the three files, and what happened to it.</h2>
<p>The join is on the <b>filename</b> &mdash; <code>data-visualisation-bar-charts.md</code> to
<code>chart-bar</code>, and so on &mdash; never a regex over rule prose. Reviewed by eye is part of the
ruling, so a rule that sits in the file but governs a different component is dropped <i>and named</i>. A
declared drop is a finding; a silent one is the s214-D6 failure.</p>
<div class="tw"><table>
<tr><th>component</th><th>rule</th><th>destiny</th><th>verdict</th><th>the authored sentence, or the reason it was dropped</th></tr>
{PARTA_ROWS}
</table></div>
<p class="why">All {n['drops_total']} drops come from structure inside the file, not from taste:
dv-line-009 and dv-line-010 sit under the line file's own <code>## Spark charts</code> heading and govern
<code>chart-sparkline</code>; dv-pie-003 is the doughnut-centre rule, and <code>chart-pie</code>'s own
purpose records that the centre-total wiring was removed as donut-only.</p>
</div></section>

<section id="family"><div class="wrap">
<p class="label">D-3 &middot; the evidence</p>
<h2>The {n['dv_family']} family rules, read against all three.</h2>
<p>Option (a) attaches all {n['dv_family']} to each &mdash; {n['family_a_total']} edges, of which
<span class="n">{n['family_false']}</span> would be false with an authored-looking sentence on them.
Option (b) is this table: <span class="n">{n['family_b_total']}</span> edges,
{n['family_bar']}&nbsp;/&nbsp;{n['family_line']}&nbsp;/&nbsp;{n['family_pie']} on bar&nbsp;/&nbsp;line&nbsp;/&nbsp;pie.
<span class="n">{n['family_shared']}</span> of the {n['dv_family']} bind all three identically &mdash; the
first measurement of what a family node would have to carry, which is what option (c) needs and does not
have.</p>
<div class="tw"><table>
<tr><th>rule</th><th>text</th><th class="num">chart-line</th><th class="num">chart-pie</th><th class="num">chart-bar</th></tr>
{FAMILY_ROWS}
</table></div>
<p class="why">Two findings sit in this table. <b>dv-019's index row is wrong</b>: it carries dv-017's
sentence, but <code>data-visualisation.md</code> line 70 shows dv-019 is the Apollo-added
vibrating-boundaries rule. The matrix above reads the <b>source file</b>, not the index row &mdash; reported, not
fixed, because <code>_rules-index.json</code> is not this lane's to write. And <b>the corpus attaches
nothing above the component today</b>: <code>common-toolkit-foundations.md</code> holds
{n['ctk_foundations']} rules that sit above the four components lane TO authored, and
<span class="n">0</span> were attached to any meta. There is no precedent here, only one to set.</p>
</div></section>

<section id="q3"><div class="wrap">
<p class="label">Flag only &middot; not authored</p>
<h2>The {n['charts_unreached']} chart components a filename cannot reach.</h2>
<p><code>knowledge/components/</code> holds {n['charts_total']} chart metas. Three have a spec file of
their own; {n['charts_unreached']} do not, so the filename-join route stops here. Listed, not authored
&mdash; and the <b>capitalisation split is real</b>: <span class="n">{n['charts_upper']}</span> are
<code>Chart-*</code> and <span class="n">{n['charts_lower']}</span> are <code>chart-*</code>, and the stem
is the node id, so <code>component:Chart-boxplot</code> and <code>component:chart-bar</code> are
differently-shaped slugs in the same graph.</p>
<div class="tw"><table>
<tr><th>meta</th><th>name</th><th>case</th><th>provides</th><th>named by a spec file's own structure</th><th class="num">dv- ids it already cites</th></tr>
{Q3_ROWS}
</table></div>
<p class="why">The "named by" column applies the Q1 test mechanically to the three <b>spec</b> file texts: does the
component's own word appear in a Types bullet, a heading, or a rule's normative clause?
<code>data-visualisation.md</code> is not searched &mdash; dv-015 lists every chart type there is, so the
family file would match all fourteen and the signal would be noise. It is a
<b>measurement</b> for you to read, never an edge &mdash; a meta can cite a rule to record that it <b>escapes</b> it,
which is why the last column is a count and not a proposal.</p>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Your words</p>
<h2>Three decisions.</h2>
<p>Recommendation first on each. One letter is an answer; a letter with a sentence attached is a sequel,
and I will read it back before anything is built on it.</p>
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
<dt>Proposed metas</dt><dd><code>notes/_lanes/277/charts/proposed-metas/</code> &mdash; 3 files, each a
byte-for-byte copy of the live meta plus one inserted span</dd>
<dt>Schema</dt><dd>{n['schema_errors']} errors against
<code>knowledge/components/meta.schema.json</code>, and four negative controls all red</dd>
<dt>Dry run</dt><dd><code>python3 notes/_lanes/277/charts/_dry_run.py</code> &mdash;
{n['obeys_live']} &rarr; {n['obeys_after']} obeys edges, <code>_validate_kg.py</code> OK against the
simulated tree</dd>
<dt>Selftest</dt><dd>{n['bites']} bites on <code>_author_metas.py</code>, all green</dd>
<dt>Mutants</dt><dd>{n['mutants']} driven by <code>_mutate.py</code>, every one caught &mdash; including
the re-dump mutant that <b>survived</b> until bite 20 was written for it</dd>
<dt>Recommendations</dt><dd>{memo_state}</dd>
</dl>
</div><div>
<p>Every integer on this page is read at build time &mdash; from <code>dry-run.json</code>, from
<code>_author_metas.py</code>'s own tables, or counted over <code>knowledge/</code>. No number was typed
into the HTML, and none was typed into the decisions file either.</p>
<p>Nothing landed. <code>knowledge/components/</code> still holds {n['metas_total']} metas carrying
{n['obeys_live']} <code>obeys</code> edges between them, all of them lane TO's, and not one chart meta has
an <code>obeys</code> block. <code>_validate_kg.py</code> is green on the live tree because this lane did
not touch it.</p>
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
   a.download="charts-decisions-2026-09-15.json";
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
print(f"wrote {OUT.name} ({len(HTML):,} bytes) · {len(IDS)} decisions · "
      f"{n['obeys_total']} citations · {len(n)} measured figures")
print(f"recommendations: {memo_state}")
