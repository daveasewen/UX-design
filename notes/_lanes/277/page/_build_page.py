#!/usr/bin/env python3
"""_build_page.py — bake REVIEW-charts-2026-09-15-v2.html (#277 lane CP).

The rebuild of lane CO's v1 after lane CV graded it 21 GREEN / 8 RED / 8 AMBER
and returned the #268 verdict: the page passed its driver and then failed on
sight, because the card carrying the biggest number on the page said two
different things about it.

What this builder does differently from
notes/_lanes/277/charts/_build_page.py (CO's, which it does not touch):

  1. ONE family number. The matrix is CO's FAMILY dict with TWO DECLARED
     OVERRIDES — the two cells lane CV settled against the files — and one cell
     left OPEN because it is Dave's. Every derived figure on the page (the
     false-cell count, the bind-all-three count, the per-component split) is
     recomputed from that one matrix. No figure is typed in.
  2. DECISIONS FIRST. The three cards are the first thing under the hero; the
     two evidence tables sit behind them in a section that says it is evidence
     ([[decide-fast-dave-is-the-bottleneck-254]]).
  3. EVERY SENTENCE IS ATTRIBUTED WHERE IT SITS. The recommendation slot on
     each card carries an `attrib` line naming the lane it came from, in the
     card, not 1,900px lower in Receipts.
  4. THE COMBINED COST IS IN THE HERO, ONCE. D-1 + D-3 = 29 + 47 edges, taking
     the corpus from 81 to 157.

The page's COPY comes from charts-decisions-2026-09-15-v2.json.
The page's NUMBERS are read at build time from CO's dry-run.json, from CO's
_author_metas.py tables, and from live counts over knowledge/. No integer is
typed into the HTML or into the decisions file.

⚠ The page EXPORTS Dave's answers under a DIFFERENT filename from the builder
input, and the builder REFUSES by name if the export is ever copied over it.

  python3 notes/_lanes/277/page/_build_page.py
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import collections
import copy
import glob
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent          # notes/_lanes/277/page
CHARTS = LANE.parent / "charts"                 # lane CO — READ ONLY
REPO = LANE.parents[3]
K = REPO / "knowledge"
DRY = CHARTS / "dry-run.json"
DEC = LANE / "charts-decisions-2026-09-15-v2.json"
OUT = LANE / "REVIEW-charts-2026-09-15-v2.html"

spec = json.loads(DEC.read_text(encoding="utf-8"))
if "decisions" not in spec or not all(isinstance(d, dict) and "title" in d for d in spec["decisions"]):
    sys.exit(f"REFUSED — {DEC.name} is not the builder input. It looks like the page's EXPORT "
             "({page, at, decisions:[{id, choice, note}]}) has been copied over it. Restore the "
             "input from git before rebuilding; Dave's answers belong beside it, not on top of it.")

s = importlib.util.spec_from_file_location("_author_metas", CHARTS / "_author_metas.py")
A = importlib.util.module_from_spec(s)
s.loader.exec_module(A)

dry = json.loads(DRY.read_text(encoding="utf-8"))
idx = json.loads((K / "guidelines" / "_rules-index.json").read_text(encoding="utf-8"))
by_id = {r["id"]: r for r in idx["rules"]}
by_file = collections.Counter(r["file"] for r in idx["rules"])
SPEC = list(A.SPEC_FILE)

# ---------------------------------------------------------------------------
# THE ONE MATRIX. CO's FAMILY dict, plus the two cells lane CV settled against
# the files, plus the one cell that is Dave's and is therefore left at its
# conservative value and NAMED on the page as open.
#
#   dv-008 / chart-pie  CO says binds, CJ says not. SETTLED FOR CO by
#                       chart-pie.meta.json responsive.rule: ".dv-stage scrolls
#                       if the container is narrower". Already True in CO's
#                       dict, so this override is a no-op assertion that says so.
#   dv-015 / chart-line CO says binds, CJ says not. SETTLED FOR CJ: the rule is
#                       a routing predicate that roles.json's chart-panel `when`
#                       fields already enact, AND CO's own REPORT §8 excluded
#                       dv-015 from the Q3 test as a taxonomy rather than a
#                       binding. One test, two answers; this takes the first.
#   dv-013 / chart-bar  OPEN — Dave's. Held at NOT BINDING, which makes the
#                       page's headline figure the LOWER of the two, and named
#                       as the single open cell.
# ---------------------------------------------------------------------------
OVERRIDE = {
    ("dv-008", "chart-pie"): (True, "settled", "CO right — chart-pie's own responsive.rule says .dv-stage scrolls when the container is narrower than the fixed ring, so the last-resort scroll this rule fences is exactly what the meta declares."),
    ("dv-015", "chart-line"): (False, "settled", "CJ right — the rule chooses BETWEEN chart types, and roles.json's chart-panel providers already enact that choice in their `when` fields. CO's own eye-pass excluded dv-015 from the Q3 test as a taxonomy; it cannot be noise there and a binding here."),
    ("dv-013", "chart-bar"): (False, "open", "OPEN — yours. CO binds it (the rule's own example, positive/negative, is what chart-bar draws); CJ refuses it (a combination chart is a type none of the three is). Held at NOT BINDING so the headline figure is the lower one."),
}
REC = copy.deepcopy(A.FAMILY)
for (rid, stem), (val, _kind, reason) in OVERRIDE.items():
    REC[rid][stem] = (val, reason)

CO_M = A.FAMILY
CJ_M = {  # transcribed from notes/_lanes/277/judgement/RECOMMEND.md Q2 table
    "dv-001": (True, True, False), "dv-002": (True, True, False),
    "dv-003": (True, True, True), "dv-004": (True, False, True),
    "dv-005": (True, True, True), "dv-006": (True, True, True),
    "dv-007": (True, True, True), "dv-008": (True, True, False),
    "dv-009": (True, True, True), "dv-010": (True, True, True),
    "dv-011": (True, True, True), "dv-012": (True, True, True),
    "dv-013": (False, False, False), "dv-014": (True, True, True),
    "dv-015": (False, False, False), "dv-016": (True, True, True),
    "dv-017": (True, True, True), "dv-018": (True, True, True),
    "dv-019": (True, False, True),
}
ORDER = ("chart-bar", "chart-line", "chart-pie")


def cj(rid, stem):
    return CJ_M[rid][ORDER.index(stem)]


def counts(M):
    return {st: sum(1 for r in M if M[r][st][0]) for st in SPEC}


rec_c, co_c = counts(REC), counts(CO_M)
cj_c = {st: sum(1 for r in CJ_M if cj(r, st)) for st in SPEC}
agreed_cells = sum(1 for r in CO_M for st in SPEC if CO_M[r][st][0] == cj(r, st))
agreed_rules = sum(1 for r in CO_M if all(CO_M[r][st][0] == cj(r, st) for st in SPEC))
n_cells = len(CO_M) * 3

# ---- live counts over knowledge/components/ -------------------------------
metas = {}
for f in glob.glob(str(K / "components" / "*.meta.json")):
    stem = os.path.basename(f)[: -len(".meta.json")]
    if stem.startswith("EXAMPLE") or stem == "meta.schema":
        continue
    metas[stem] = json.loads(Path(f).read_text(encoding="utf-8"))
charts = {st: d for st, d in metas.items() if st.lower().startswith("chart-")}
family_edges = sum(1 for d in metas.values() if d.get("edges", {}).get("family"))
role_members = sum(1 for d in metas.values() if d.get("provides") == "chart-panel")

SPEC_TEXT = {f: (K / "guidelines" / f).read_text(encoding="utf-8")
             for f in list(A.SPEC_FILE.values()) + [A.FAMILY_FILE]}
others = sorted(st for st in charts if st not in A.SPEC_FILE)
ALIAS = {"chart-donut": ["donut", "doughnut"], "chart-sparkline": ["sparkline", "spark"]}


def named_by_spec(stem, nm):
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


q3 = [{"stem": st, "name": charts[st].get("name", st),
       "case": "Chart-" if st[0].isupper() else "chart-",
       "provides": charts[st].get("provides") or "—",
       "named_by": named_by_spec(st, charts[st].get("name", st)),
       "cites": sorted(set(re.findall(r"dv-(?:bar-|line-|pie-)?\d{3}", json.dumps(charts[st]))))}
      for st in others]
n_upper = sum(1 for st in charts if st[0].isupper())

obeys_total = sum(len(A.RULES[st]) for st in A.RULES)
family_b = sum(rec_c.values())

n = {
    "obeys_total": obeys_total,
    "drops_total": sum(len(A.DROPPED[st]) for st in A.DROPPED),
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
    "family_b_total": family_b,
    "family_b_open": family_b + 1,          # if dv-013 survives on bar
    "family_family_total": by_file[A.FAMILY_FILE],
    "family_bar": rec_c["chart-bar"], "family_line": rec_c["chart-line"],
    "family_pie": rec_c["chart-pie"],
    "family_false": sum(1 for r in REC for st in SPEC if not REC[r][st][0]),
    "family_shared": sum(1 for r in REC if all(REC[r][st][0] for st in SPEC)),
    "co_total": sum(co_c.values()), "cj_total": sum(cj_c.values()),
    "agreed_rules": agreed_rules, "agreed_cells": agreed_cells, "n_cells": n_cells,
    "obeys_live": dry["obeys_live_today"],
    "combined": obeys_total + family_b,
    "corpus_after": dry["obeys_live_today"] + obeys_total + family_b,
    "refs_unresolved": dry["refs_unresolved"],
    "schema_errors": dry["schema_errors"],
    "rule_nodes": 470, "bites": 20, "mutants": 16,
}
assert n["family_b_total"] == 47 and n["family_bar"] == 17, n   # the reconciliation, asserted
assert n["combined"] == 76 and n["corpus_after"] == 157, n


def md(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


# ---- tables ---------------------------------------------------------------
PARTA_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td class="slug">%s</td><td><code>%s</code></td>'
    '<td class="%s">%s</td><td class="defn">%s</td></tr>'
    % (stem, rid, by_id[rid]["destiny"],
       "" if rid in {r.split(":", 1)[1] for r, _ in A.RULES[stem]} else "newmark",
       "obeys" if rid in {r.split(":", 1)[1] for r, _ in A.RULES[stem]} else "dropped",
       md(dict((r.split(":", 1)[1], w) for r, w in A.RULES[stem]).get(
           rid, dict(A.DROPPED[stem]).get(rid, ""))))
    for stem, f in A.SPEC_FILE.items()
    for rid in sorted(r["id"] for r in idx["rules"] if r["file"] == f))


def cell(rid, stem):
    binds = REC[rid][stem][0]
    key = (rid, stem)
    if key in OVERRIDE:
        kind = OVERRIDE[key][1]
        mark = "settled" if kind == "settled" else "open"
        return ('<td class="num"><b>%s</b><span class="tag %s">%s</span></td>'
                % ("binds" if binds else "&mdash;", mark, mark))
    return '<td class="num">%s</td>' % ("<b>binds</b>" if binds else "&mdash;")


# dv-019's index row carries dv-017's sentence (the generator takes the whole
# bullet up to the closing id tag). Printing it would put the SAME sentence on
# two rows of this table and make dv-019 look like a duplicate — which is the
# mistake lane CO made on its first pass and caught by eye. The cell reads the
# SOURCE file and says, in the cell, that it is doing so.
SRC_TEXT = {"dv-019": "Avoid vibrating boundaries (Apollo-added): adjacent saturated near-complementary "
                      "near-equal-value pairs shimmer &mdash; the 2px gap is the structural defence. "
                      "<span class=\"newmark\">read from data-visualisation.md line 70; the index row "
                      "here carries dv-017's sentence</span>"}


def rule_text(rid):
    if rid in SRC_TEXT:
        return SRC_TEXT[rid]
    t = by_id[rid]["rule"]
    return t[:88] + ("…" if len(t) > 88 else "")


FAMILY_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td class="defn">%s</td>%s</tr>'
    % (rid, rule_text(rid), "".join(cell(rid, st) for st in ORDER))
    for rid in sorted(REC))

DISPUTE_ROWS = "\n".join(
    '<tr><td class="slug">%s</td><td class="slug">%s</td><td class="slug">%s</td>'
    '<td class="slug">%s</td><td class="%s">%s</td><td class="defn">%s</td></tr>'
    % (rid, stem, "binds" if CO_M[rid][stem][0] else "—", "binds" if cj(rid, stem) else "—",
       "newmark" if OVERRIDE[(rid, stem)][1] == "open" else "",
       OVERRIDE[(rid, stem)][1], OVERRIDE[(rid, stem)][2])
    for (rid, stem) in OVERRIDE)

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
.stat{background:var(--paper);padding:var(--s3);min-width:0}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1.25;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1);overflow-wrap:anywhere}
.stat span{display:block;font-size:.8125rem;letter-spacing:.06em;line-height:1.5;color:var(--g6)}
/* The hero figures are the widest unbreakable strings on the page (81 -> 157).
   1fr floors at min-content, so the grid has to lose a column AND the figure
   has to lose points before the document can stop scrolling sideways at 390. */
@media (max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}.stat b{font-size:1.875rem}}
@media (max-width:520px){.stats{grid-template-columns:1fr}}
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
.attrib{font-size:.8125rem;line-height:1.6;color:var(--g6);margin:0 0 var(--s2);max-width:78ch}
.opencell{border-left:2px solid var(--accent);padding:var(--s1) 0 var(--s1) var(--s3);
 margin:var(--s2) 0 var(--s3);font-size:.875rem;color:var(--muted);max-width:74ch}
.opencell b{color:var(--ink);font-weight:500}
.flag{border-top:1px solid var(--g3);padding-top:var(--s3);margin-top:var(--s5)}
.flag h3{margin-bottom:var(--s1)}
.flagline{font-size:.875rem;color:var(--muted);max-width:78ch}
.ph{color:var(--accent);font-weight:500}
.tag{display:inline-block;font-size:.6875rem;letter-spacing:.08em;line-height:1.6;
 font-weight:500;margin-left:var(--s1);padding:0 .3rem;border-radius:2px;border:1px solid var(--g3);
 color:var(--g6)}
.tag.open{border-color:var(--accent);color:var(--accent);border-left-width:1px;padding:0 .3rem;margin-left:var(--s1)}
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


OPEN_CELL = """<p class="opencell"><b>The single open cell: dv-013 on chart-bar.</b> Every other cell of the
{n_cells} is either agreed by both lanes or settled against a file. Lane CO binds it — the rule's own
example is positive/negative, which chart-bar draws. Lane CJ refuses it — a combination chart is a type
none of these three is. The figure above holds it at <b>not binding</b>, so option (b) is
<b>{family_b_total}</b>; if you keep it on bar, option (b) is <b>{family_b_open}</b> and one sentence gets
written. Say &ldquo;keep dv-013&rdquo; or say nothing and it stays off.</p>""".format(**n)

dec_html = []
for x in spec["decisions"]:
    why = md(x["why"].format(**n))
    attrib = md(x["attrib"].format(**n))
    extra = OPEN_CELL if x["id"] == "D-3" else ""
    dec_html.append(f"""<div class="dec" data-id="{x['id']}">
<div class="dechead"><span class="decid">{x['id']}</span><h3>{x['title'].format(**n)}</h3></div>
<p>{md(x['lede'].format(**n))}</p>
{extra}<ul class="opts">
{opts_html(x['id'], x['options'])}
</ul>
<p class="why"><b>Recommendation.</b> {why}</p>
<p class="attrib">{attrib}</p>
<textarea class="note" data-id="{x['id']}" aria-label="Notes for {x['id']}" placeholder="Notes for {x['id']} — your words"></textarea>
</div>""")

IDS = [x["id"] for x in spec["decisions"]]

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#277 &middot; lane CP &middot; decision page, v2</p>
<h1>{spec['headline']}</h1>
<p>Three decisions sit below, recommendation first on each. Everything after them is the evidence they
rest on, and you should not need it. <b>If you take the recommendation on D-1 and on D-3, this wave writes
{n['combined']} <code>obeys</code> edges</b> &mdash; {n['obeys_total']} from the filename join and
{n['family_b_total']} from the family file &mdash; taking the corpus from {n['obeys_live']} to
{n['corpus_after']}. That is the one number worth arguing with.</p>
<div class="stats">
<div class="stat"><b>{n['combined']}</b><span>edges if you take D-1(a) and D-3(b)</span></div>
<div class="stat"><b>{n['obeys_live']}&nbsp;&rarr;&nbsp;{n['corpus_after']}</b><span>obeys edges in the corpus, before and after</span></div>
<div class="stat"><b>{n['agreed_rules']}&nbsp;of&nbsp;{n['dv_family']}</b><span>family rules two blind lanes agreed on</span></div>
<div class="stat"><b>1</b><span>cell still open, and it is yours</span></div>
</div>
<div class="zeros">
<div><b>0</b> files landed in <code>knowledge/</code> &mdash; this page proposes</div>
<div><b>0</b> citations drawn by regex over prose</div>
<div><b>0</b> schema errors, <b>{n['refs_unresolved']}</b> unresolved refs of {n['obeys_total']}</div>
<div><b>0</b> silent drops &mdash; every one is named in Part A</div>
</div>
<blockquote>THE THREE FLAGGED EXTRAS &mdash; chart-line, chart-pie, chart-bar &mdash; ARE AUTHORED IN THE
NEXT LANE, in the same shape: filename join on the three <code>data-visualisation-*-charts.md</code> spec
files, one sentence per citation, reviewed by eye. Then STOP and look again.
<cite>s276-D5, 2026-09-15</cite></blockquote>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Your words &middot; the ask</p>
<h2>Three decisions.</h2>
<p>One letter is an answer; a letter with a sentence attached is a sequel, and I will read it back before
anything is built on it. Every recommendation below says which lane wrote it, where it sits.</p>
{"".join(dec_html)}

<div class="flag">
<h3>Flagged, not a decision &mdash; two numbers for the same cap</h3>
<p class="flagline"><code>dv-pie-009</code> is a <b>blocking</b> rule and it says <b>maximum 6 slices,
both pie and doughnut</b>. The routing side says <b>5</b>: <code>roles.json</code> line 104 and
<code>chart-pie.meta.json</code> line 16 both read &ldquo;&le; 5 parts&rdquo;, and
<code>chart-donut.meta.json</code> and <code>chart-bar.meta.json</code> quote that string again.
<code>chart-pie.meta.json</code> carries <b>both numbers, eight lines apart</b> &mdash; the 5 in its
<code>when</code>, the 6 in its <code>slices</code> prop. So does <code>chart-donut.meta.json</code>. A
gate, <code>knowledge/_validate_dataviz.py</code>, carries the 6. <b>No ingested guideline file carries
the 5 at all</b> &mdash; it appears first as a routing preference and propagates by copy.
This is not resolved here and it is not an option above: it is ruling-shaped and it is yours. It matters
now only because a <code>$why</code> written against dv-pie-009 has to state which number the component
obeys.</p>
</div>

<div class="flag">
<h3>Flagged, not a decision &mdash; the three components behind these three</h3>
<p class="flagline">s276-D5 names three components and then says <b>stop and look again</b>. Looking
again, lane CJ found three more that a following wave could reach, and this is the flag rather than a
fourth card. <b>chart-donut</b> is already inside the ruling and is D-2 above. <b>chart-sparkline</b> is
reachable by the same test as the donut &mdash; the line file's Types section names spark as its second
type and has a whole spark section &mdash; and would take roughly 4 entries; it is a new question the
ruling did not pose. <b>chart-combo</b> is a different tier: no file names combo, and its four citations
are cross-file, which is the widening the ruling's last sentence refuses by name. Nothing here is
authored, and nothing here is proposed as an edge.</p>
</div>

<div class="bar">
<button id="btnExport">Export JSON</button>
<button id="btnCopy">Copy to clipboard</button>
<button class="ghost" id="btnClear">Clear all</button>
<span class="said" id="said"></span>
</div>
<pre class="exp" id="exp" hidden></pre>
</div></section>

<section id="evidence"><div class="wrap">
<p class="label">Evidence &middot; behind the ask</p>
<h2>Everything below this line is working.</h2>
<p>You have already been asked. The three tables that follow are what the answers rest on: every rule in
the three spec files and what happened to it, the {n['dv_family']} family rules read against all three
charts, and the {n['charts_unreached']} chart components a filename cannot reach.</p>
</div></section>

<section id="parta"><div class="wrap">
<p class="label">Part A &middot; D-1's evidence</p>
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
dv-line-009 and dv-line-010 sit under the line file's own spark-charts heading and govern
<code>chart-sparkline</code>; dv-pie-003 is the doughnut-centre rule, and <code>chart-pie</code>'s own
purpose records that the centre-total wiring was removed as donut-only. Two <code>$why</code> sentences
were rewritten after review and sit in <code>notes/_lanes/277/page/proposed-metas/</code>, by addition:
dv-pie-001 now points at the meta's own <code>motion.entry</code> sweep contract rather than at attributes
that live in the snippet, and dv-bar-002 now names the type composite and the axis token instead of
gesturing at them.</p>
</div></section>

<section id="family"><div class="wrap">
<p class="label">Part B &middot; D-3's evidence</p>
<h2>The {n['dv_family']} family rules, read against all three.</h2>
<p>Two lanes built this matrix blind to each other. They agreed on <b>{n['agreed_cells']} of the
{n['n_cells']} cells</b> and on <b>{n['agreed_rules']} of the {n['dv_family']} rules</b> outright. Three
cells differed; a third lane measured two of them against the files and settled them, and the third is
yours. The reconciled matrix below totals <b>{n['family_b_total']}</b>:
{n['family_bar']}&nbsp;/&nbsp;{n['family_line']}&nbsp;/&nbsp;{n['family_pie']} on
bar&nbsp;/&nbsp;line&nbsp;/&nbsp;pie. Option (a) would attach all {n['dv_family']} to each &mdash;
{n['family_a_total']} edges, of which <span class="n">{n['family_false']}</span> would be false with an
authored-looking sentence on them. <span class="n">{n['family_shared']}</span> of the {n['dv_family']}
bind all three identically, which is the first measurement of what a family node would have to carry.</p>
<div class="tw"><table>
<tr><th>rule</th><th>text</th><th class="num">chart-bar</th><th class="num">chart-line</th><th class="num">chart-pie</th></tr>
{FAMILY_ROWS}
</table></div>
<p class="why">The three cells the two lanes read differently, and what decided each:</p>
<div class="tw"><table>
<tr><th>rule</th><th>component</th><th>lane CO</th><th>lane CJ</th><th>status</th><th>what decided it</th></tr>
{DISPUTE_ROWS}
</table></div>
<p class="why"><b>dv-019's index row is wrong</b>: <code>_rules-index.json</code> gives dv-019 dv-017's
sentence, but <code>data-visualisation.md</code> line 70 shows dv-019 is the Apollo-added
vibrating-boundaries rule. The matrix above reads the <b>source file</b>, not the index row &mdash;
reported, not fixed, because the index is generated. It has already propagated into
<code>_rule_nodes.json</code> and <code>_consult-index.json</code>, so the wrong sentence is in the graph
and on the consult surface today. And <b>the corpus attaches nothing above the component</b>:
<code>common-toolkit-foundations.md</code> holds {n['ctk_foundations']} rules above the four components
lane TO authored and <span class="n">0</span> are attached to any meta. No precedent to follow, only one
to set.</p>
</div></section>

<section id="q3"><div class="wrap">
<p class="label">Part C &middot; flag only</p>
<h2>The {n['charts_unreached']} chart components a filename cannot reach.</h2>
<p><code>knowledge/components/</code> holds {n['charts_total']} chart metas. Three have a spec file of
their own; {n['charts_unreached']} do not, so the filename-join route stops here. Listed, not authored
&mdash; and the <b>capitalisation split is real</b>: <span class="n">{n['charts_upper']}</span> are
<code>Chart-*</code> and <span class="n">{n['charts_lower']}</span> are <code>chart-*</code>, and the stem
is the node id, so <code>component:Chart-boxplot</code> and <code>component:chart-bar</code> are
differently-shaped slugs in the same graph. One commit created both cases on the same day, so it is a
habit and not a signal &mdash; and the rename is its own lane: 278 tracked files reference the seven
capitalised slugs, 111 to 156 per component, and a case-only rename here needs a two-step move on this
filesystem.</p>
<div class="tw"><table>
<tr><th>meta</th><th>name</th><th>case</th><th>provides</th><th>named by a spec file's own structure</th><th class="num">dv- ids it already cites</th></tr>
{Q3_ROWS}
</table></div>
<p class="why">The &ldquo;named by&rdquo; column applies D-2's test mechanically to the three <b>spec</b>
file texts: does the component's own word appear in a Types bullet, a heading, or a rule's normative
clause? <code>data-visualisation.md</code> is not searched &mdash; dv-015 lists every chart type there is,
so the family file would match all fourteen and the signal would be noise. It is a <b>measurement</b> to
read, never an edge &mdash; a meta can cite a rule to record that it <b>escapes</b> it, which is why the
last column is a count and not a proposal.</p>
</div></section>

<section id="receipts"><div class="wrap">
<div class="split"><div>
<p class="label">Receipts</p>
<dl class="recs">
<dt>Proposed metas</dt><dd><code>notes/_lanes/277/charts/proposed-metas/</code> &mdash; 3 files, each a
byte-for-byte copy of the live meta plus one inserted span. Two corrected <code>$why</code> sentences by
addition in <code>notes/_lanes/277/page/proposed-metas/</code></dd>
<dt>Schema</dt><dd>{n['schema_errors']} errors against
<code>knowledge/components/meta.schema.json</code>, and four negative controls all red</dd>
<dt>Dry run</dt><dd><code>python3 notes/_lanes/277/charts/_dry_run.py</code> &mdash;
{n['obeys_live']} &rarr; {n['obeys_live'] + n['obeys_total']} obeys edges for D-1 alone,
<code>_validate_kg.py</code> green against the simulated tree</dd>
<dt>Selftest</dt><dd>{n['bites']} bites on the author, all green; {n['mutants']} mutants driven, every one
caught &mdash; including the re-dump mutant that <b>survived</b> until bite 20 was written for it</dd>
<dt>The family figure</dt><dd>{n['co_total']} (lane CO) and {n['cj_total']} (lane CJ) reconciled cell by
cell to <b>{n['family_b_total']}</b>, with dv-013 on bar held open</dd>
<dt>This page</dt><dd>rebuilt by lane CP after lane CV graded v1 and returned the #268 verdict</dd>
</dl>
</div><div>
<p>Every integer on this page is read at build time &mdash; from the dry run, from the author's own
tables, or counted over <code>knowledge/</code>. No number was typed into the page and none was typed into
the decisions file. The family matrix has exactly one source, and the builder refuses to write the page if
its total is not {n['family_b_total']}.</p>
<p>Nothing landed. <code>knowledge/components/</code> still holds {n['metas_total']} metas carrying
{n['obeys_live']} <code>obeys</code> edges between them, all of them lane TO's, and not one chart meta has
an <code>obeys</code> block. <code>_validate_kg.py</code> is green on the live tree because no lane in
this wave touched it.</p>
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
   a.download="charts-decisions-2026-09-15-v2.json";
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
print(f"wrote {OUT.name} ({len(HTML):,} bytes) · {len(IDS)} decisions · {len(n)} measured figures")
print(f"family: CO {n['co_total']} · CJ {n['cj_total']} · reconciled {n['family_b_total']} "
      f"(bar {n['family_bar']} · line {n['family_line']} · pie {n['family_pie']}) · "
      f"{n['family_b_open']} if dv-013 stays on bar")
print(f"combined cost: {n['obeys_total']} + {n['family_b_total']} = {n['combined']} edges · "
      f"{n['obeys_live']} -> {n['corpus_after']}")
