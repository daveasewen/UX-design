#!/usr/bin/env python3
"""_build_page.py — bake REVIEW-kg-audit-2026-09-16-v1.html (#277 lane A2).

Adapted from notes/_lanes/277/page/_build_page.py (lane CP's, not touched).
Same contract: DECISIONS FIRST, recommendation first on each card, every
recommendation attributed in the card, every integer read at build time —
from A1-measure.json (lane A1, 13a4cf2) and A2-measure.json (this lane's
_measure_a2.py) — none typed into the HTML or the decisions file.

D-6 ("which augmentation first") is fed from A3-shortlist.json if lane A3 has
written it; otherwise the card is a MARKED placeholder that says so.

The page EXPORTS Dave's answers under a DIFFERENT filename from the builder
input, and the builder REFUSES by name if the export is ever copied over it.

    python3 notes/_lanes/277/kg-audit/_build_page.py
"""
import html
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
DEC = LANE / "kg-audit-decisions-2026-09-16-v1.json"
OUT = LANE / "REVIEW-kg-audit-2026-09-16-v1.html"
A1 = json.loads((LANE / "A1-measure.json").read_text(encoding="utf-8"))
A2 = json.loads((LANE / "A2-measure.json").read_text(encoding="utf-8"))
A3P = LANE / "A3-shortlist.json"

spec = json.loads(DEC.read_text(encoding="utf-8"))
if "decisions" not in spec or not all(isinstance(d, dict) and "title" in d for d in spec["decisions"]):
    sys.exit(f"REFUSED — {DEC.name} is not the builder input; it looks like the page's export "
             "was copied over it. Restore the input from git before rebuilding.")

# ---- numbers ---------------------------------------------------------------------
t = A1["totals"]
census = A1["item4_edge_type_census"]
ctypes = census.get("types") or census.get("census") or census
if isinstance(ctypes, dict):
    ctypes = [dict(v, type=k) if isinstance(v, dict) else {"type": k, "n": v} for k, v in ctypes.items()]


def cnt(name):
    for r in ctypes:
        if r.get("type") == name:
            return r.get("n") or r.get("count") or r.get("edges")
    return None


R, U, Q, TK, RUL, A11 = A2["rules"], A2["ux"], A2["questions"], A2["tokens"], A2["rulings"], A2["accessibility_holdings"]
n = {
    "a1_nodes": t["nodes"], "a1_edges": t["edges_live"], "a1_dangling": t["edges_dangling"],
    "a1_edge_types": t["edge_types"], "a1_kinds": t["kinds"],
    "a1_nc_types": A2["a1"]["no_consumer_types"], "a1_nc_edges": A2["a1"]["no_consumer_edges"],
    "a1_nc_pct": round(100 * A2["a1"]["no_consumer_edges"] / t["edges_live"]),
    "a1_schema_only": A2["a1"]["schema_only_types"],
    "a1_islands": A2["a1"]["islands"], "a1_orphans": A2["a1"]["orphans"],
    "a1_prose": A2["a1"]["prose_edges"], "a1_authored": A2["a1"]["authored_edges"], "a1_structural": A2["a1"]["structural_edges"],
    "rules_total": R["total"], "rules_files": R["files"], "rules_obeyed": R["rules_obeyed"],
    "files_reached": len(R["files_reached_by_obeys"]), "files_unreached": R["files_not_reached"],
    "rules_unreached": R["rules_in_unreached_files"],
    "blocking": R["blocking"], "blocking_obeyed": R["blocking_obeyed"],
    "blocking_unbound": R["blocking"] - R["blocking_obeyed"],
    "f_copy": R["foundation_examples"]["copywriting.md"], "f_tone": R["foundation_examples"]["tone-of-voice.md"],
    "f_colour": R["foundation_examples"]["colour-standards-2026.md"] + R["foundation_examples"]["colour-usage.md"],
    "f_type": R["foundation_examples"]["typography-standards-2026.md"] + R["foundation_examples"]["typography-usage.md"],
    "f_icons": R["foundation_examples"]["icons.md"] + R["foundation_examples"]["pictograms.md"],
    "f_neuro": R["foundation_examples"]["neurodiversity.md"],
    "ux_total": U["total"], "ux_orphans": U["orphans"], "ux_a_orphans": sum(1 for v in U["a_grade"].values() if v == 0),
    "a11y_sc": A11["guidelines_family_sc"], "a11y_rules": A11["guidelinerules_family_rules"],
    "a11y_ux": A11["uxprinciples_family_nodes"], "a11y_links": A11["cross_links"],
    "rul_total": RUL["total"], "rul_system": RUL["scope"]["system"], "rul_design": RUL["scope"]["design"],
    "rul_both": RUL["scope"]["both"], "rul_system_pct": round(100 * RUL["scope"]["system"] / RUL["total"]),
    "rul_no_session": RUL["without_ruledIn"], "rul_session_in_id": RUL["session_in_id"], "rul_dated": RUL["date_present"],
    "metas_total": A2["components"]["metas"], "metas_tokens": TK["metas_with_tokens_block"],
    "token_refs": TK["distinct_refs"], "token_files": TK["token_files"],
    "comp_with_obeys": A2["components"]["with_obeys"], "comp_without_role": A2["components"]["without_provides"],
    "metas_tokens_k": A2["compose_slice"]["metas_tokens_docstring"],
    "slice_tokens": f"{A2['compose_slice']['slice_tokens']:,}", "slice_replaced": f"{A2['compose_slice']['metas_replaced_tokens']:,}",
    "governs_n": cnt("governs"), "governedBy_n": cnt("governedBy"),
    "q_answered": Q["n_answered"], "q_partial": Q["n_partial"], "q_unanswerable": Q["n_unanswerable"],
    "q_rate": Q["rate_pct"], "q_rate_incl": Q["rate_incl_partial_pct"], "q_design": Q["design_time_n"],
    "q_after": Q["after_d2_d5_answered"],
    "chips_off": A2["explorer"]["additive_chips_default_off"],
    "not_in_chip": len(A2["explorer"]["not_in_any_chip"]),
}
assert n["blocking_unbound"] == 50 and n["rul_system"] == 432 and n["q_answered"] == 6, n

# ---- D-6 from A3, or a marked placeholder ------------------------------------------
if A3P.exists():
    a3 = json.loads(A3P.read_text(encoding="utf-8"))
    items = a3 if isinstance(a3, list) else a3.get("shortlist") or a3.get("items") or []
    opts = []

    def lst(v):
        return " · ".join(html.escape(str(x)) for x in v) if isinstance(v, list) else html.escape(str(v))

    ranked = sorted(items, key=lambda x: x.get("rank", 99))
    for i, it in enumerate(ranked[:5]):
        key = "abcde"[i]
        opts.append([key, i == 0,
                     f"<b>{html.escape(str(it.get('name', '')))}</b> <span class=\"tag\">{html.escape(str(it.get('class', '')))}</span> "
                     f"— {html.escape(str(it.get('plain', '')))} <span class=\"defn\">Closes {lst(it.get('closes', ''))}. "
                     f"Cost: {html.escape(str(it.get('cost', '')))}. Touches {lst(it.get('touches', ''))}. "
                     f"s274-D12: {html.escape(str(it.get('s274_D12', '')))}</span>"])
    names = [str(it.get("name", "")) for it in ranked]
    d6 = {"lede": f"Lane A3’s shortlist &mdash; {len(items)} candidates in <code>A3-shortlist.json</code>, ranked as A3 ranked them ({', '.join(names)}); the first is A3’s recommendation. Each is priced at one lane or less and tested against s274-D12. The full argument and A3's ten refusals are in <code>A3-AUGMENT.md</code>.",
          "options": opts,
          "why": f"Take A3’s first, <b>{names[0]}</b>, and take it as the same lane as D-3: a typed-question door over the graph and the wired compose slice are one instrument with two verbs, not two. A3’s {names[3] if len(names) > 3 else ''} reaches the same gap as D-5 but at about 950 nodes — the leaf grain s269-D3 refused — so the two disagree on grain and not on need: take D-5(a) and A3’s <code>aliasOf</code> lands on the tier nodes, or take A3’s shape and s269-D3 is superseded by id, never silently. Its {names[2] if len(names) > 2 else ''} is Part C of this page written into the validator — the two lanes converged without reading each other, which is the strongest signal either produced.",
          "attrib": "Lane A3 (Fable) ranked and priced the five; the convergence line is lane A2’s.", "placeholder": False}
else:
    d6 = {"lede": "<span class=\"ph\">PLACEHOLDER — lane A3 had not written <code>A3-shortlist.json</code> when this page was built.</span> A3 is surveying what is orthogonal, lateral or meta — community summaries, inferred inverse and transitive edges, temporal validity (P-269-6), hypergraph rulings, an embedding index, shape validation, provenance, the token graph, agent-memory architectures — and pricing each against the s274-D12 test. When its shortlist lands the conductor rebuilds this page and the options below become A3’s ranked five.",
          "options": [["a", False, "<span class=\"ph\">A3’s first choice — not yet written.</span>"],
                      ["b", False, "<span class=\"ph\">A3’s second — not yet written.</span>"]],
          "why": "No recommendation until A3 reports. A2’s one word on the question: anything that manufactures plausible-but-unratified edges is advisory at most (s274-D12), and the augmentation that pays first is the one that lowers the query-time token cost of the twelve questions, because that is the cost the agent actually pays.",
          "attrib": "Placeholder written by lane A2; the slot is lane A3’s.", "placeholder": True}

for d in spec["decisions"]:
    if d["id"] == "D-6":
        d["lede"], d["options"], d["why"], d["attrib"] = d6["lede"], d6["options"], d6["why"], d6["attrib"]


def md(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def fmt(s):
    return s.format(**n) if "{" in s else s


# ---- evidence tables --------------------------------------------------------------------
QROWS = [
    ("Q1", "what governs this component?", "answered", "<code>governs</code> ruling→component, length 1, 107 of 137; the 30 without are true absences", "partial — 28 <code>governedBy</code> ship; the 295 <code>governs</code> do not", "D-3"),
    ("Q2", "which components does this rule bind?", "partial", f"<code>obeys</code> on {n['comp_with_obeys']} metas, {n['files_reached']} of {n['rules_files']} files; the facet files cannot be expressed", "no", "D-2"),
    ("Q3", "what principle underlies this rule, and its grade?", "unanswerable", "rule→ux 0 of 470; no edge type in either direction", "no", "authored <code>restsOn</code> (G6)"),
    ("Q4", "which rules conflict for this component?", "unanswerable", "needs component→rule (7.3%) and a <code>conflictsWith</code> that does not exist; the 5-vs-6 cap is prose in s277-D3", "no", "authored <code>conflictsWith</code> + the Constitution (G7)"),
    ("Q5", "what did Dave rule about this, and when?", "answered", f"<code>governs</code> + <code>date</code> {n['rul_dated']}/{n['rul_total']}; <code>ruledIn</code> covers {n['rul_total'] - n['rul_no_session']}, the session is in the id for {n['rul_session_in_id']} of the other {n['rul_no_session']}", "no — rulings do not ship", "read the id (G9); D-3"),
    ("Q6", "what evidence supports that ruling?", "answered", "<code>evidencedBy</code> length 1, 593/593", "no", "D-3"),
    ("Q7", "which components answer this intent / data shape?", "answered", "<code>answersIntent</code> 14/14, <code>hasDataShape</code> 23/23 (charts); <code>providesRole</code> 108/137 for the rest", "yes (roles.json ships)", f"{n['comp_without_role']} without a role — s273-D2 held sets"),
    ("Q8", "what must this component not sit next to?", "partial", "19 resolved on 17 components + 51 declared nulls that are anti-pattern statements, not components", "yes — the skill reads the meta prose", "keep the nulls (ruled shape)"),
    ("Q9", "what tokens does this component consume; what breaks?", "unanswerable", f"no <code>token:</code> kind; <code>tokens</code> is a typed block in {n['metas_tokens']} metas", "no", "D-5"),
    ("Q10", "which pattern / context is this used in?", "answered", "length 1, 100% / 99.3% — but 341 of 380 patterns and 176 of 222 contexts are one-component labels", "yes (metas)", "G8 — a pattern of one is a tag"),
    ("Q11", "what is the WCAG / accessible-name obligation?", "answered", "<code>appliesTo</code> 134/137 + the meta’s <code>accessibility.relatedSC</code> block", "yes (compliance ships)", "—"),
    ("Q12", "what icon / logo / photo may I use?", "unanswerable", "no asset kind; lane RI proposes 688 nodes / 1,299 edges (5520d43), unruled; photography ruled s269-D4, unbuilt", "partial (manifest ships, unlinked)", "RI’s page; then photography"),
]
QROWS_HTML = "\n".join(
    f'<tr><td class="slug">{q}</td><td>{md(txt)}</td><td class="v-{v}">{v}</td><td class="defn">{path}</td><td class="defn">{dt}</td><td class="defn">{close}</td></tr>'
    for q, txt, v, path, dt, close in QROWS)

KIND_ROWS = [
    ("component", 137, "the thing chosen", "renderedBy 1 · usedInContext ≥1 · providesRole ≥1 · ≥1 obligation", f"0 at degree 0; {n['comp_without_role']} without a role; {137 - n['comp_with_obeys']} without an obeys"),
    ("snippet", 137, "the render", "1", "none — 87 at degree 1 is correct"),
    ("pattern", 380, "a composition of ≥2 components", "≥2 in-edges", "<b>341 at degree 1</b> — labels, not patterns"),
    ("context", 222, "where a component lives", "≥2 in-edges", "<b>176 at degree 1</b>"),
    ("role · intent · shape", "12 · 14 · 23", "the DESK address (s270-D2)", "≥1 provider", "none"),
    ("ruling", n["rul_total"], "a decision cited by id", "governs ≥1 · evidencedBy ≥1 · a session", f"{n['rul_no_session']} without a session edge ({n['rul_session_in_id']} recoverable from the id); no scope"),
    ("evidence", 886, "the receipt", "1", "none by intent; ids are the evidence string"),
    ("artefact", 618, "a governed file", "1", "none; the guideline-file artefacts are the natural scope hub for D-2"),
    ("session", 92, "when", "≥1", "none"),
    ("rule", n["rules_total"], "an obligation the agent applies", "definedIn 1 + a scope", f"<b>{n['rules_total'] - n['rules_obeyed']} with no scope; {n['blocking_unbound']} of {n['blocking']} BLOCKING bind nothing</b>"),
    ("sc", 55, "the legal obligation", "under + appliesTo ≥1", "none"),
    ("guideline · principle · standard · policy", "13 · 4 · 1 · 1", "the WCAG taxonomy", "≥1", "none"),
    ("axe", 64, "the automatable check", "1", "none by intent; no consumer"),
    ("ux", n["ux_total"], "the explanation, graded", "≥1 (a rule or component resting on it, or a polarity)", f"<b>{n['ux_orphans']} at degree 0</b>, {n['ux_a_orphans']} of the six A-grade laws among them; the {n['a11y_ux']} standards-family principles have 0 links to sc:"),
    ("polarity", 30, "a tension between principles", "hasParty 2", "5 at degree ≤1 — the declared stubs (s275-D3)"),
]
KIND_HTML = "\n".join(f'<tr><td class="slug">{k}</td><td class="num">{c}</td><td class="defn">{f}</td><td class="defn">{m}</td><td class="defn">{g}</td></tr>'
                      for k, c, f, m, g in KIND_ROWS)

GAPS = [
    ("G1", f"{n['blocking_unbound']} of {n['blocking']} BLOCKING rules bind no component; {n['rules_total'] - n['rules_obeyed']} of {n['rules_total']} rules have no scope", "a scope per guideline file", "authored once + structural", f"{n['rules_files']} rows · 1 reader · 1 lane", "s274-D9 · s274-D12 · s276-D5 · s277-D3 · P-274-3", "D-2"),
    ("G2", f"no design-time reader — {n['a1_nc_pct']}% of edges have no consumer; the agent reads ~{n['metas_tokens_k']}K tokens of metas", "wire _compose_slice.py as generate step 1", "—", "1 lane + pack cut", "s274-D11 · s269-D9 · apollo-spider SKILL :130", "D-3"),
    ("G3", f"the layers are ingestion waves; accessibility sits in three with {n['a11y_links']} links", "three views by force; scope on rulings; 20 authored links", "template + authored", "1 lane", "s274-D11 · s275-D6 · s275-D4 · s269-D2 kept", "D-1"),
    ("G4", "no token kind (Q9)", "token: at tier grain + bindsToken from metas.tokens", "structural", "10–20 nodes · ~1,000 edges · 1 lane", "s269-D3 · P-269-7", "D-5"),
    ("G5", "no asset kind (Q12)", "lane RI’s 688 nodes / 1,299 edges", "structural", "ruled + 1 land lane", "s269-D1 step 4 · RI-1..4 · s230-D2", "RI’s page"),
    ("G6", "rule → principle absent (Q3)", "authored restsOn, 59 BLOCKING × six A-grade laws first", "authored", "≤ 60 sentences · 1 lane", "s269-D5 · s275-D5", "gap list"),
    ("G7", "conflicts between rules absent (Q4)", "authored conflictsWith + the Constitution", "authored", "rare; the known one first", "s277-D3", "gap list"),
    ("G8", "341 patterns / 176 contexts are one-component labels", "decide: tag attribute, or members", "decision", "0 build", "none", "gap list"),
    ("G9", f"{n['rul_no_session']} rulings lack a session edge; no scope on rulings", "read the session from the id; derive scope from governs[]", "structural", "~10 lines", "none", "inside D-1"),
    ("G10", "explorer prints islands 2 · orphans 0 over the base graph only", "compute after the append", "fix", "8 lines", "none", "fix"),
    ("G11", f"{n['ux_orphans']} orphan principles incl. {n['ux_a_orphans']} A-grade laws", "G6 + s275-D5’s component citations", "authored", "inside G6", "s275-D5", "gap list"),
    ("G12", "Figma specs · photography · fonts · personas/JTBD · content standard · lifecycle · temporal window", "parked", "—", "—", "P-273-1 · s269-D4 · P-269-9 · s269-D6 · P-269-6", "parked"),
]
GAP_HTML = "\n".join(f'<tr><td class="slug">{g}</td><td class="defn">{w}</td><td class="defn">{c}</td><td class="slug">{j}</td><td class="defn">{cost}</td><td class="slug">{r}</td><td class="slug">{d}</td></tr>'
                     for g, w, c, j, cost, r, d in GAPS)

REFUSE = [
    "Rule → component by any text match — the 27 regex candidates, name-in-prose, shingle overlap (s274-D12, s276-D5; RI measured the route at 1,947 junk pairs).",
    "Principle → SC by family name (fam-wcag22 → perceivable) — a name match, refused by s275-D4; the 20 links are authored under D-1 or not at all.",
    "Token leaves as nodes — 932 of them (s269-D3).",
    "A family node without a carrier (s277-D3 c) — D-2’s attribute carries what it would.",
    "Promoting mentions to typed edges by verb proximity — the regex proposes, Dave ratifies (s267-D3).",
    "Merging the eleven ruling verbs into one — undoes twenty hand-retyped edges to tidy a census.",
    "Inferring a ruling’s scope from its prose — derive it from governs[] only.",
    f"Retiring the {n['a1_nc_types']} consumer-less types — they answer five of the twelve questions; the defect is the missing reader.",
]
REFUSE_HTML = "\n".join(f"<li>{md(x)}</li>" for x in REFUSE)

CSS = (REPO / "notes/_lanes/277/page/_build_page.py").read_text(encoding="utf-8")
CSS = CSS[CSS.index('CSS = """') + 9: CSS.index('"""\n\n\ndef opts_html')]
CSS += """
.v-answered{color:var(--ink);font-weight:500}.v-partial{color:var(--g7)}.v-unanswerable{color:var(--accent);font-weight:500}
.layers{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s3);margin:var(--s4) 0}
.layers div{border-top:2px solid var(--ink);padding-top:var(--s2)}
.layers b{display:block;font-weight:500;margin-bottom:var(--s1)}
.layers span{font-size:.875rem;color:var(--muted)}
@media (max-width:760px){.layers{grid-template-columns:1fr}}
ol.refuse{padding-left:1.2em;max-width:78ch}ol.refuse li{margin-bottom:var(--s1);font-size:.9375rem}
"""


def opts_html(did, opts):
    out = []
    for key, rec, text in opts:
        oid = f"{did}-{key}"
        rec_html = '<span class="rec">Recommended</span>' if rec else ""
        out.append(f'<li><div class="opt"><input type="radio" name="{did}" id="{oid}" value="{key}">'
                   f'<label for="{oid}"><span class="okey">({key})</span>{rec_html}{fmt(text)}</label></div></li>')
    out.append(f'<li><div class="opt"><input type="radio" name="{did}" id="{did}-none" value="">'
               f'<label for="{did}-none"><span class="okey">(&mdash;)</span>No choice yet &mdash; clear this decision.</label></div></li>')
    return "\n".join(out)


dec_html = []
for x in spec["decisions"]:
    dec_html.append(f"""<div class="dec" data-id="{x['id']}">
<div class="dechead"><span class="decid">{x['id']}</span><h3>{fmt(x['title'])}</h3></div>
<p>{md(fmt(x['lede']))}</p>
<ul class="opts">
{opts_html(x['id'], x['options'])}
</ul>
<p class="why"><b>Recommendation.</b> {md(fmt(x['why']))}</p>
<p class="attrib">{md(fmt(x['attrib']))}</p>
<textarea class="note" data-id="{x['id']}" aria-label="Notes for {x['id']}" placeholder="Notes for {x['id']} — your words"></textarea>
</div>""")
IDS = [x["id"] for x in spec["decisions"]]

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#277 &middot; lane A2 &middot; the KG audit &middot; decisions, v1</p>
<h1>{spec['headline']}</h1>
<p>Six decisions sit below, recommendation first on each; everything after them is the evidence they rest on.
<b>The headline is the answer rate:</b> the graph answers <b>{n['q_answered']} of the 12</b> questions a designer asks
mid-task by a path, half-answers {n['q_partial']}, cannot answer {n['q_unanswerable']} &mdash; and the agent, at design
time, can reach <b>{n['q_design']} of the 12</b>, because nothing on the compose path reads the graph. If you take D-2, D-3 and
D-5 the graph answers {n['q_after']} and the agent reaches the same. If you take D-1 the layers stop being the commit
history and start being how a designer thinks.</p>
<div class="stats">
<div class="stat"><b>{n['q_answered']}&nbsp;of&nbsp;12</b><span>designer questions answered by a graph path</span></div>
<div class="stat"><b>{n['q_design']}&nbsp;of&nbsp;12</b><span>reachable by the agent at design time today</span></div>
<div class="stat"><b>{n['blocking_unbound']}&nbsp;of&nbsp;{n['blocking']}</b><span>BLOCKING HSBC rules that bind no component</span></div>
<div class="stat"><b>{n['a1_nc_pct']}%</b><span>of edges read by nothing &mdash; {n['a1_nc_types']} types, {n['a1_nc_edges']:,} edges</span></div>
</div>
<div class="zeros">
<div><b>{n['a1_nodes']:,}</b> nodes &middot; <b>{n['a1_edges']:,}</b> edges &middot; <b>{n['a1_edge_types']}</b> types &middot; <b>{n['a1_kinds']}</b> kinds, at <code>bedf383</code></div>
<div><b>{n['rul_system']}</b> of {n['rul_total']} rulings govern only files &mdash; the system's own record, not design precedent</div>
<div><b>{n['a11y_links']}</b> edges between the three places accessibility lives ({n['a11y_sc']} sc &middot; {n['a11y_rules']} rules &middot; {n['a11y_ux']} principles)</div>
<div><b>0</b> files under <code>knowledge/</code> written &mdash; this page proposes</div>
</div>
<blockquote>also think about the organisation of the the different layers in this graph, are the 5 layers currently,
maybe this needs reconstituted, should they be layered and conjoined as they are, should it be one or less than 5. in my
mind (this may not be correct) all the accessibility nodes should be design governance nodes, and what we have as
governance should be something like 'system constitution' or 'codex' or 'system management' I don't know right now, but
it seems the categorisation might net be corrcet.<cite>Dave, #277, 2026-09-16 (verbatim, his spelling)</cite></blockquote>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Your words &middot; the ask</p>
<h2>Six decisions.</h2>
<p>One letter is an answer; a letter with a sentence attached is a sequel, and it is read back before anything is built
on it. D-1 carries the most weight and D-3 is the one every other decision waits on.</p>
{"".join(dec_html)}
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
<p>You have already been asked. What follows is what the answers rest on: the twelve questions scored, the three
layers by force, each node kind against its own minimum, the ranked gaps with cost, and the fixes this lane would
refuse. The long form is <code>notes/_lanes/277/kg-audit/A2-AUDIT.md</code>; the numbers are
<code>A1-measure.json</code> and <code>A2-measure.json</code>.</p>
</div></section>

<section id="questions"><div class="wrap">
<p class="label">Part A &middot; the headline's evidence</p>
<h2>The twelve questions a designer asks mid-task.</h2>
<p>Scored twice: can the graph answer it by a path (A1's reachability seeds, judged), and can the agent reach that
answer at design time today (the compose skill reads the metas; the pack ships <code>_rulings.json</code> empty and
does not ship the rule or principle nodes).</p>
<div class="tw"><table>
<tr><th>q</th><th>the question</th><th>graph</th><th>path &middot; coverage</th><th>design time today</th><th>what closes it</th></tr>
{QROWS_HTML}
</table></div>
<p class="why">Answer rate <b>{n['q_answered']} / {n['q_partial']} / {n['q_unanswerable']}</b> &mdash; {n['q_rate']}% answered,
{n['q_rate_incl']}% counting partial. With RI landed and Q5 read from the id: 7 / 2 / 3. With D-2 and D-5: {n['q_after']} / 1 / 2.</p>
</div></section>

<section id="layers"><div class="wrap">
<p class="label">Part B &middot; D-1's evidence</p>
<h2>Three layers by force, not five by wave.</h2>
<div class="layers">
<div><b>The system</b><span>what exists &mdash; component, snippet, pattern, context, role, intent, shape; tokens (D-5) and assets (RI) when they land. The agent <i>chooses</i> here.</span></div>
<div><b>Design governance</b><span>what a design must or should do &mdash; {n['a11y_sc']} WCAG criteria (external law), {n['rules_total']} HSBC rules with a destiny (internal standard), the {n['rul_design'] + n['rul_both']} design-scoped rulings (case law). Three provenances as sub-chips, one precedence ladder. Accessibility lives here entirely. The agent <i>obeys</i> here.</span></div>
<div><b>Explanation</b><span>why &mdash; {n['ux_total']} graded principles, 30 polarities, the evidence trail. Never an obligation. The agent <i>consults</i> here when obligations pull against each other.</span></div>
</div>
<p>The ruling record is not a layer of the designer brain. It is the <b>Codex</b> &mdash; {n['rul_total']} rulings, each with
its evidence and its session, superseding and refining one another by the authored edges s267-D3 ratified. Measured over
what each ruling governs: <b>{n['rul_system']} system-only</b>, <b>{n['rul_design']} design-only</b>, {n['rul_both']} both. A derived
<code>scope</code> on each ruling puts the design ones inside the governance view and leaves the system ones where the
conductor reads them. The <b>Constitution</b> is the dozen fences everything else defers to &mdash; fence 3 of #261, the two-red
law, nam-002, "an instrument without a consumer is refused" &mdash; and the precedence ladder: law, then ruling, then BLOCKING,
then ADVISORY, then the principles behind them. It does not exist as a document today.</p>
<p class="why">Rulings a re-cut touches, by id: s274-D11 and s275-D6 (the "behind its own chip" clauses become sub-chips of
Design governance; the reader-in-the-same-commit clauses stand); s275-D4 (the named lane it defers the joins to is this
lane); s269-D2 (the <code>ux:</code> prefix stays); s274-D7, s274-D8, s275-D1..D3, s270-D2, s276-D3, s277-D1..D3 (node kinds
and edge types &mdash; untouched: a view re-cut changes <code>fam</code> labels and the template's chips, never an id or a
type); s267-D3 (untouched). The five edge types no chip draws today &mdash; {', '.join(f'<code>{x}</code>' for x in A2['explorer']['not_in_any_chip'])} &mdash;
get a chip in the same move.</p>
</div></section>

<section id="kinds"><div class="wrap">
<p class="label">Part C &middot; connectivity has an intent</p>
<h2>Each kind against its own minimum.</h2>
<p>"Orphan" means something only against a stated minimum. A snippet with one edge is perfect; a rule with one edge
binds nothing. Three kinds fail their own purpose at scale: rule, pattern, ux.</p>
<div class="tw"><table>
<tr><th>kind</th><th class="num">n</th><th>what it is for</th><th>minimum</th><th>gap</th></tr>
{KIND_HTML}
</table></div>
</div></section>

<section id="gaps"><div class="wrap">
<p class="label">Part D &middot; ranked, with cost</p>
<h2>The gaps, in the order they change a 30-second decision.</h2>
<div class="tw"><table>
<tr><th>#</th><th>gap</th><th>closes with</th><th>join</th><th>cost</th><th>touches</th><th>where</th></tr>
{GAP_HTML}
</table></div>
<p class="why">The 105 dangling edges are not on this list: every one carries a sentence and the shape is ruled
(s270-D2, s274-D10, s275-D2). Fifty-one are anti-pattern statements, twenty-two are events, eight are sub-parts, fifteen
are declared stubs, two are true anaphora a human resolves in a minute. The prose tier ({n['a1_prose']} edges) stays: <code>mentions</code>
dashed and advisory, <code>cites</code> solid and labelled a parsed citation.</p>
</div></section>

<section id="refuse"><div class="wrap">
<p class="label">Part E &middot; what this lane would refuse</p>
<h2>The attractive fixes that are the s274-D12 shape.</h2>
<ol class="refuse">
{REFUSE_HTML}
</ol>
</div></section>

<section id="receipts"><div class="wrap">
<div class="split"><div>
<p class="label">Receipts</p>
<dl class="recs">
<dt>Measurement</dt><dd><code>A1-measure.json</code> (lane A1, 13a4cf2) + <code>A2-measure.json</code> (<code>_measure_a2.py</code>, this lane)</dd>
<dt>Long form</dt><dd><code>A2-AUDIT.md</code> &mdash; nine sections, plain prose first, then the technical prose, then one line</dd>
<dt>Graph</dt><dd>{n['a1_nodes']:,} nodes &middot; {n['a1_edges']:,} live edges &middot; {n['a1_dangling']} declared nulls &middot; {n['a1_edge_types']} types &middot; join classes structural {n['a1_structural']:,} / prose {n['a1_prose']} / authored {n['a1_authored']}</dd>
<dt>Nothing run</dt><dd>no <code>gen_kg_edges.py</code>, no <code>_build_all.py</code>, no <code>_build_kg_explorer.main()</code>; nothing under <code>knowledge/</code> written</dd>
<dt>D-6</dt><dd>{'fed from A3-shortlist.json' if not d6['placeholder'] else 'a marked placeholder &mdash; A3 had not reported at build time'}</dd>
</dl>
</div><div>
<p>Every integer on this page is read at build time from the two measurement files; none was typed into the page or
the decisions file, and the builder refuses to write the page if the three figures it asserts drift.</p>
<p>Dave's words appear once, verbatim, in the hero. Nothing on this page is a ruling.</p>
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
   a.download="kg-audit-decisions-2026-09-16-v1.json";
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
print(f"wrote {OUT.name} ({len(HTML):,} bytes) · {len(IDS)} decisions · {len(n)} measured figures · "
      f"D-6 {'from A3-shortlist.json' if not d6['placeholder'] else 'PLACEHOLDER'}")
print(f"answer rate {n['q_answered']}/{n['q_partial']}/{n['q_unanswerable']} · design-time {n['q_design']}/12 · "
      f"BLOCKING unbound {n['blocking_unbound']}/{n['blocking']} · rulings system {n['rul_system']}/{n['rul_total']}")
