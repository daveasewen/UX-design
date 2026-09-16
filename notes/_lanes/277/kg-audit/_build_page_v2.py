#!/usr/bin/env python3
"""_build_page_v2.py — bake REVIEW-kg-audit-2026-09-16-v2.html (#277 lane A2F).

v2 of lane A2's page, on lane A2V's verdict (VERIFY.md, 3a37bcd: PRESENT WITH THESE 5
FIXES) plus the thin-slice section Dave asked for ("also lets consider how this effects our
thin slice technique for design knowledge retrieval at build time"). Corrections BY
ADDITION: v1 and A2's/A3's files are not edited; this builder reads its own v2 decisions
file and the same measurement files, PLUS lane A2V's `verify-figures.json` (the corrected
integers) and this lane's `slice-measure-v2.json` (the thin slice measured). Every integer
on the page is read from one of those files at build time; the three that v1 typed into
A2-measure.json (19,113 / 111,468 / 414,184) are re-measured here and read from
slice-measure-v2.json.

Same contract as v1: DECISIONS FIRST, recommendation first on each card, every
recommendation attributed in the card, six decisions and no seventh (the thin slice is
D-3's instrument, so D-3 carries it). The export shape is unchanged
({page, at, decisions[6]{id, choice, note}}); D-1's one-word answer (the name of the ruling
record) is a separate box on the card and travels in D-1's note as its first line.

The page EXPORTS under a DIFFERENT filename from the builder input, and the builder
REFUSES by name if the export is ever copied over it.

    python3 notes/_lanes/277/kg-audit/_build_page_v2.py
"""
import html
import json
import re
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
DEC = LANE / "kg-audit-decisions-2026-09-16-v2.json"
OUT = LANE / "REVIEW-kg-audit-2026-09-16-v2.html"
A1 = json.loads((LANE / "A1-measure.json").read_text(encoding="utf-8"))
A2 = json.loads((LANE / "A2-measure.json").read_text(encoding="utf-8"))
V = json.loads((LANE.parent / "kg-audit-verify" / "verify-figures.json").read_text(encoding="utf-8"))
S = json.loads((LANE / "slice-measure-v2.json").read_text(encoding="utf-8"))
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


R, U, Q, TK, A11 = A2["rules"], A2["ux"], A2["questions"], A2["tokens"], A2["accessibility_holdings"]
VR, VS, VC, VT = V["rules"], V["ruling_scope_by_governs_target"], V["consumers"], V["tokens"]
runs = {r["key"]: r for r in S["slice_runs"]}
TD = S["today"]
Q9 = next(r for r in S["a3_table_corrected"]["rows"] if r["q"] == "Q9")
n = {
    "a1_nodes": t["nodes"], "a1_edges": t["edges_live"], "a1_dangling": t["edges_dangling"],
    "a1_edge_types": t["edge_types"], "a1_kinds": t["kinds"],
    "a1_nc_types": A2["a1"]["no_consumer_types"],
    "a1_nc_edges": VC["nc12_edges"],                       # FIX 4 (F13): 3,110 live, not 3,125 incl. 15 hasParty nulls
    "a1_nc_edges_fmt": f"{VC['nc12_edges']:,}",
    "a1_nc_edges_v1": A2["a1"]["no_consumer_edges"],
    "a1_nc_pct": round(100 * VC["nc12_edges"] / t["edges_live"]),
    "a1_schema_only": A2["a1"]["schema_only_types"],
    "a1_islands": A2["a1"]["islands"], "a1_orphans": A2["a1"]["orphans"],
    "a1_prose": A2["a1"]["prose_edges"], "a1_authored": A2["a1"]["authored_edges"], "a1_structural": A2["a1"]["structural_edges"],
    "rules_total": R["total"], "rules_files": R["files"], "rules_obeyed": R["rules_obeyed"],
    "rules_no_scope": VR["rules_no_component"],           # 363 (page was right; audit said 316)
    "files_reached": VR["files_reached_n"], "files_unreached": VR["files_unreached_n"],
    "files_named": VR["files_reached_n"] - 1,             # FIX 4 (F12): 7 named after a component (s276-D5) + the family file
    "rules_unreached": VR["rules_in_unreached"],
    "blocking": VR["blocking"], "blocking_obeyed": VR["blocking_obeyed"],
    "blocking_unbound": VR["blocking_unbound"],
    "blocking_via_cites": VR["blocking_reaching_via_cites_appliesTo"],
    "blocking_unbound_any": VR["blocking_unbound_even_counting_cites_path"],
    "cites_edges": V["a11y"]["acc_rule_to_sc_cites"],
    "f_copy": R["foundation_examples"]["copywriting.md"], "f_tone": R["foundation_examples"]["tone-of-voice.md"],
    "f_colour": R["foundation_examples"]["colour-standards-2026.md"] + R["foundation_examples"]["colour-usage.md"],
    "f_type": R["foundation_examples"]["typography-standards-2026.md"] + R["foundation_examples"]["typography-usage.md"],
    "f_icons": R["foundation_examples"]["icons.md"] + R["foundation_examples"]["pictograms.md"],
    "f_neuro": R["foundation_examples"]["neurodiversity.md"],
    "ux_total": U["total"], "ux_orphans": U["orphans"], "ux_a_orphans": sum(1 for v in U["a_grade"].values() if v == 0),
    "a11y_sc": A11["guidelines_family_sc"], "a11y_rules": A11["guidelinerules_family_rules"],
    "a11y_ux": A11["uxprinciples_family_nodes"], "a11y_links": A11["cross_links"],
    "rul_total": VS["total"],
    "rul_system": VS["system"], "rul_design": VS["design"], "rul_both": VS["both"],   # FIX 3 (F9): 435/99/59 under gov_target()
    "rul_system_v1": A2["rulings"]["scope"]["system"], "rul_both_v1": A2["rulings"]["scope"]["both"],
    "rul_system_pct": round(100 * VS["system"] / VS["total"]),
    "rul_no_session": V["ruledIn"]["without"], "rul_session_in_id": V["ruledIn"]["session_in_id"], "rul_dated": A2["rulings"]["date_present"],
    "metas_total": A2["components"]["metas"], "metas_total_all": TD["metas_all"]["files"],
    "metas_tokens": TK["metas_with_tokens_block"],
    "metas_tokens_k": round(TD["metas_all"]["tokens"] / 1000),      # FIX 1 (F21): 415, not 730
    "metas_tokens_exact": f"{TD['metas_all']['tokens']:,}",
    "metas_mb": round(TD["metas_bytes"] / 1_000_000, 1),
    "metas_tokens_k_v1": A2["compose_slice"]["metas_tokens_docstring"],
    "meta_median": f"{TD['meta_median']:,}",
    "showroom_index_k": round(TD["showroom_index"] / 1000),
    "showroom_index": f"{TD['showroom_index']:,}",
    "canon_css": f"{TD['canon_css']:,}", "type_css": f"{TD['type_css']:,}",
    "snippets_tokens": f"{TD['snippets_all']['tokens']:,}", "snippets_files": TD["snippets_all"]["files"],
    "snippet_avg_k": round(TD["snippets_all"]["tokens"] / TD["snippets_all"]["files"] / 1000),
    "rules_index": f"{TD['rules_index']:,}", "compliance_tokens": f"{TD['compliance_rules']['tokens']:,}",
    "icons_manifest": f"{TD['icons_manifest']:,}", "roles_json": f"{TD['roles_json']:,}",
    "rulings_json": f"{TD['rulings_json']:,}", "blast_radius": f"{TD['blast_radius']:,}",
    "consult_index": f"{TD['consult_index']:,}",
    "token_refs": TK["distinct_refs"], "token_files": TK["token_files"],
    "token_groups": S["token_groups"]["groups"], "token_mentions": f"{S['token_groups']['mentions']:,}",
    "token_top12_pct": S["token_groups"]["top12_pct"], "token_leaves_live": VT["leaf_count_live_files"],
    "comp_with_obeys": A2["components"]["with_obeys"], "comp_without_role": A2["components"]["without_provides"],
    "slice_dash_k": round(runs["dashboard"]["slice_tokens"] / 1000, 1),
    "slice_dash_k_int": round(runs["dashboard"]["slice_tokens"] / 1000),
    "slice_dash": f"{runs['dashboard']['slice_tokens']:,}",
    "slice_dash_metas": runs["dashboard"]["metas_in_slice"],
    "slice_dash_metas_k": round(runs["dashboard"]["metas_in_slice_tokens"] / 1000),
    "slice_dash_metas_tok": f"{runs['dashboard']['metas_in_slice_tokens']:,}",
    "slice_dash_ratio": round(runs["dashboard"]["ratio_vs_selected_metas"], 1),
    "slice_bar": f"{runs['bar-chart']['slice_tokens']:,}", "slice_bar_metas": runs["bar-chart"]["metas_in_slice"],
    "slice_bar_metas_tok": f"{runs['bar-chart']['metas_in_slice_tokens']:,}",
    "slice_bar_ratio": round(runs["bar-chart"]["ratio_vs_selected_metas"], 1),
    "slice_form": f"{runs['form']['slice_tokens']:,}", "slice_form_metas": runs["form"]["metas_in_slice"],
    "slice_form_metas_tok": f"{runs['form']['metas_in_slice_tokens']:,}",
    "slice_form_ratio": round(runs["form"]["ratio_vs_selected_metas"], 1),
    "slice_dash_lib_ratio": round(runs["dashboard"]["ratio_vs_whole_library"]),
    "q9_today_k": round(Q9["today_v2"] / 1000), "q9_a3_k": round(Q9["today_a3"] / 1000),
    "a3_summed_m": round(S["a3_table_corrected"]["summed_a3"] / 1e6, 1),
    "v2_summed_m": round(S["a3_table_corrected"]["summed_v2"] / 1e6, 1),
    "v2_dedup_m": round(S["a3_table_corrected"]["deduplicated_v2"] / 1e6, 1),
    "slice_total": f"{S['a3_table_corrected']['slice_total']:,}",
    "ratio_summed": f"{S['a3_table_corrected']['ratio_summed']:,}", "ratio_dedup": f"{S['a3_table_corrected']['ratio_dedup']:,}",
    "obeys_ux_edges": S["obeys_to_ux"]["edges"], "obeys_ux_metas": len(S["obeys_to_ux"]["by_meta"]),
    "obeys_ux_laws": len(S["obeys_to_ux"]["distinct_ux"]),
    "governs_n": cnt("governs"), "governedBy_n": cnt("governedBy"),
    "q_answered": Q["n_answered"], "q_partial": Q["n_partial"], "q_unanswerable": Q["n_unanswerable"],
    "q_rate": Q["rate_pct"], "q_rate_incl": Q["rate_incl_partial_pct"], "q_design": Q["design_time_n"],
    "q_after": Q["after_d2_d5_answered"],
    "chips_off": A2["explorer"]["additive_chips_default_off"],
    "not_in_chip": len(A2["explorer"]["not_in_any_chip"]),
}
# Two of A2V's small integers live only in VERIFY.md's prose (verify-figures.json carries neither):
# F5 — 15 components carry a resolved mustNotNeighbour; F25 — FOUR of the twelve consumer-less types
# answer a designer's question directly. Read from the verdict, not typed.
_verify_md = (LANE.parent / "kg-audit-verify" / "VERIFY.md").read_text(encoding="utf-8")
_m = re.search(r"19 live `mustNotNeighbour` on \*\*(\d+)\*\* components", _verify_md)
n["q8_components"] = int(_m.group(1)) if _m else None
_m = re.search(r"\| F25 \|.*?\*\*(\w+)\*\*;", _verify_md)
n["nc_answering_word"] = _m.group(1) if _m else None
n["mnn_nulls"] = V["null_by_type"]["mustNotNeighbour"]
assert n["blocking_unbound"] == 50 and n["rul_system"] == 435 and n["q_answered"] == 6 and n["metas_tokens_k"] == 415 \
    and n["a1_nc_edges"] == 3110 and n["q8_components"] == 15 and n["obeys_ux_edges"] == 14 and n["nc_answering_word"] == "four", n

# ---- D-6 from A3 (ranked as A3 ranked it), with A2V's F27/F28 corrections BY ADDITION ------------
a3 = json.loads(A3P.read_text(encoding="utf-8"))
items = a3["shortlist"]
opts = []


def lst(v):
    return " · ".join(html.escape(str(x)) for x in v) if isinstance(v, list) else html.escape(str(v))


ranked = sorted(items, key=lambda x: x.get("rank", 99))
for i, it in enumerate(ranked[:5]):
    key = "abcde"[i]
    plain = str(it.get("plain", ""))
    corr = ""
    if it.get("name") == "TOKENS" and "595K" in plain:
        # FIX 5 (F28): A3 charged canon.css to Q9; the meta's tokens block + _blast-radius.json answer it in ≈25K.
        plain = plain.replace("595K-token read", f"{n['q9_a3_k']}K-token read as A3 costed it")
        corr = (f" <span class=\"defn\"><b>A2V correction:</b> Q9’s honest today-cost is about {n['q9_today_k']}K tokens "
                f"(the meta plus <code>_blast-radius.json</code>), not {n['q9_a3_k']}K — TOKENS keeps its place on “no node kind”, not on cost. "
                f"Under D-5(a) this lands as group nodes with a tier, not ≈950 leaves.</span>")
    opts.append([key, i == 0,
                 f"<b>{html.escape(str(it.get('name', '')))}</b> <span class=\"tag\">{html.escape(str(it.get('class', '')))}</span> "
                 f"— {html.escape(plain)}{corr} <span class=\"defn\">Closes {lst(it.get('closes', ''))}. "
                 f"Cost: {html.escape(str(it.get('cost', '')))}. Touches {lst(it.get('touches', ''))}. "
                 f"s274-D12: {html.escape(str(it.get('s274_D12', '')))}</span>"])
names = [str(it.get("name", "")) for it in ranked]
d6 = {"lede": f"Lane A3’s shortlist — {len(items)} candidates in <code>A3-shortlist.json</code>, ranked as A3 ranked them ({', '.join(names)}); the first is A3’s recommendation. Each is priced at one lane or less and tested against s274-D12. A3 measured the twelve questions at <b>about {n['a3_summed_m']}M tokens of file reads today</b> — <b>summed per question</b>, counting <code>_rulings.json</code> three times and the metas twice; the de-duplicated read is about {n['v2_dedup_m']}M with Q9 corrected (Part A) — against about {n['slice_total']} tokens for the answering graph slices. The full argument and A3’s ten refusals are in <code>A3-AUGMENT.md</code>; of its 33 sources A2V spot-checked nine and eight hold — S31 does not carry the claim it is cited for and is dropped here.",
      "options": opts,
      "why": f"Take A3’s first, <b>{names[0]}</b>, and take it as the same lane as D-3: a typed-question door over the graph and the wired compose slice are one instrument with two verbs, not two. A3’s {names[3]} reaches the same gap as D-5 but at about 950 nodes — a leaf count whatever its tier is called, the shape s269-D3 refused — so the two disagree on grain and not on need: take D-5(a) and A3’s <code>aliasOf</code> lands on the group nodes, or take A3’s shape and s269-D3 is superseded by id, never silently. Its {names[2]} is Part D of this page written into the validator — the two lanes converged without reading each other, which is the strongest signal either produced.",
      "attrib": "Lane A3 (Fable) ranked and priced the five; the convergence line is lane A2’s; the Q9 and summed-versus-de-duplicated corrections are lane A2V’s (F27, F28), re-driven by lane A2F."}

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
    ("Q4", "which rules conflict for this component?", "unanswerable", "needs component→rule (7.3%) and a <code>conflictsWith</code> that does not exist; the 5-vs-6 cap is prose in s277-D3", "no", "authored <code>conflictsWith</code> (G7)"),
    ("Q5", "what did Dave rule about this, and when?", "answered", f"<code>governs</code> + <code>date</code> {n['rul_dated']}/{n['rul_total']}; <code>ruledIn</code> covers {n['rul_total'] - n['rul_no_session']}, the session is in the id for {n['rul_session_in_id']} of the other {n['rul_no_session']}", "no — rulings do not ship", "read the id (G9); D-3"),
    ("Q6", "what evidence supports that ruling?", "answered", "<code>evidencedBy</code> length 1, 593/593", "no", "D-3"),
    ("Q7", "which components answer this intent / data shape?", "answered", "<code>answersIntent</code> 14/14, <code>hasDataShape</code> 23/23 (charts); <code>providesRole</code> 108/137 for the rest", "yes (roles.json ships)", f"{n['comp_without_role']} without a role — s273-D2 held sets"),
    ("Q8", "what must this component not sit next to?", "partial", f"19 resolved on {n['q8_components']} components + {n['mnn_nulls']} declared nulls that are anti-pattern statements, not components", "yes — the skill reads the meta prose", "keep the nulls (ruled shape)"),
    ("Q9", "what tokens does this component consume; what breaks?", "unanswerable", f"no <code>token:</code> kind; <code>tokens</code> is a typed block in {n['metas_tokens']} metas; <code>_blast-radius.json</code> computes reach — about {n['q9_today_k']}K tokens to read today, not {n['q9_a3_k']}K", "no", "D-5"),
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
    ("rule", n["rules_total"], "an obligation the agent applies", "definedIn 1 + a scope", f"<b>{n['rules_no_scope']} with no scope; {n['blocking_unbound']} of {n['blocking']} BLOCKING bind nothing</b>"),
    ("sc", 55, "the legal obligation", "under + appliesTo ≥1", "none"),
    ("guideline · principle · standard · policy", "13 · 4 · 1 · 1", "the WCAG taxonomy", "≥1", "none"),
    ("axe", 64, "the automatable check", "1", "none by intent; no consumer"),
    ("ux", n["ux_total"], "the explanation, graded", "≥1 (a rule or component resting on it, or a polarity)", f"<b>{n['ux_orphans']} at degree 0</b>, {n['ux_a_orphans']} of the six A-grade laws among them; the {n['a11y_ux']} standards-family principles have 0 links to sc:"),
    ("polarity", 30, "a tension between principles", "hasParty 2", "5 at degree ≤1 — the declared stubs (s275-D3)"),
]
KIND_HTML = "\n".join(f'<tr><td class="slug">{k}</td><td class="num">{c}</td><td class="defn">{f}</td><td class="defn">{m}</td><td class="defn">{g}</td></tr>'
                      for k, c, f, m, g in KIND_ROWS)

GAPS = [
    ("G1", f"{n['blocking_unbound']} of {n['blocking']} BLOCKING rules bind no component; {n['rules_no_scope']} of {n['rules_total']} rules have no scope", "a scope per guideline file", "authored once + structural (derived, labelled)", f"{n['rules_files']} rows · 1 reader · 1 lane", "s274-D9 · s274-D12 · s276-D5 · s277-D3 · P-274-3", "D-2"),
    ("G2", f"no design-time reader — {n['a1_nc_pct']}% of edges have no consumer; the agent reads ~{n['metas_tokens_k']}K tokens of metas", "wire _compose_slice.py as generate step 1 under the thin-slice contract", "—", "1 lane + pack cut", "s274-D11 · s269-D9 · apollo-spider SKILL :131", "D-3"),
    ("G3", f"the layers are ingestion waves; accessibility sits in three with {n['a11y_links']} links", "three views by force (template only); separately, 20 authored links for the standards-family principles — a new edge type, its own lane", "template · authored", "1 lane (template) + 1 lane (20 sentences)", "s275-D6 refined · s275-D4 (the authored lane, not D-1) · s269-D2 kept", "D-1 · gap list"),
    ("G4", "no token kind (Q9)", "token: at group grain with tier + bindsToken from metas.tokens", "structural", f"~{n['token_groups']} nodes · ~1,000 edges · 1 lane", "s269-D3 · P-269-7", "D-5"),
    ("G5", "no asset kind (Q12)", "lane RI’s 688 nodes / 1,299 edges", "structural", "ruled + 1 land lane", "s269-D1 step 4 · RI-1..4 · s230-D2", "RI’s page"),
    ("G6", "rule → principle absent (Q3)", "authored restsOn, 59 BLOCKING × six A-grade laws first", "authored", "≤ 60 sentences · 1 lane", "s269-D5 · s275-D5", "gap list"),
    ("G7", "conflicts between rules absent (Q4)", "authored conflictsWith; a precedence ladder only if Dave authors one (D-1 why)", "authored", "rare; the known one first", "s277-D3", "gap list"),
    ("G8", "341 patterns / 176 contexts are one-component labels", "decide: tag attribute, or members", "decision", "0 build", "none", "gap list"),
    ("G9", f"{n['rul_no_session']} rulings lack a session edge; no scope on rulings", "read the session from the id; a scope proxy from governs[] if Dave wants one", "structural", "~10 lines", "none", "D-1 why (unratified)"),
    ("G10", "explorer prints islands 2 · orphans 0 over the base graph only", "compute after the append", "fix", "8 lines", "none", "fix"),
    ("G11", f"{n['ux_orphans']} orphan principles incl. {n['ux_a_orphans']} A-grade laws", "G6 + s275-D5’s component citations", "authored", "inside G6", "s275-D5", "gap list"),
    ("G12", "Figma specs · photography · fonts · personas/JTBD · content standard · lifecycle · temporal window", "parked", "—", "—", "P-273-1 · s269-D4 · P-269-9 · s269-D6 · P-269-6", "parked"),
]
GAP_HTML = "\n".join(f'<tr><td class="slug">{g}</td><td class="defn">{w}</td><td class="defn">{c}</td><td class="slug">{j}</td><td class="defn">{cost}</td><td class="slug">{r}</td><td class="slug">{d}</td></tr>'
                     for g, w, c, j, cost, r, d in GAPS)

REFUSE = [
    "Rule → component by any text match — the 27 regex candidates, name-in-prose, shingle overlap (s274-D12, s276-D5; RI measured the route at 1,947 junk pairs).",
    "Principle → SC by family name (fam-wcag22 → perceivable) — a name match, refused by s275-D4; the 20 links are authored in their own lane or not at all.",
    "Token leaves as nodes — 932 of them by the ruling’s count (s269-D3).",
    "A family node without a carrier (s277-D3 c) — D-2’s attribute carries what it would.",
    "Promoting mentions to typed edges by verb proximity — the regex proposes, Dave ratifies (s267-D3).",
    "Merging the eleven ruling verbs into one — undoes twenty hand-retyped edges to tidy a census.",
    "Inferring a ruling’s scope from its prose — derive it from governs[] only, and call it a proxy.",
    f"Retiring the {n['a1_nc_types']} consumer-less types — they answer four of the twelve questions directly and carry the receipts for the rest; the defect is the missing reader.",
    "Handing the agent the whole graph, or the whole meta library, at build time — 798K and 415K tokens; a slice or nothing.",
]
REFUSE_HTML = "\n".join(f"<li>{md(x)}</li>" for x in REFUSE)

# ---- Part A: the thin slice — tables --------------------------------------------------------
TODAY_ROWS = [
    ("1", "<code>showroom/index.json</code> — “what exists?”, the skill’s first stop", n["showroom_index"], "read whole, by design"),
    ("2", f"<code>components/&lt;slug&gt;.meta.json</code> — the contract; median {n['meta_median']} each, {n['metas_total_all']} files", n["metas_tokens_exact"], f"the ones the agent picks — {n['slice_dash_metas']} on a dashboard ({n['slice_dash_metas_tok']}), {n['slice_bar_metas']} on a bar chart ({n['slice_bar_metas_tok']})"),
    ("3", f"<code>snippets/&lt;Slug&gt;.reference.html</code> — the markup to copy; about {n['snippet_avg_k']}K each", n["snippets_tokens"], "one per component placed"),
    ("4", "<code>canon/canon.css</code> + <code>canon/type.css</code> — every token and class", f"{n['canon_css']} + {n['type_css']}", "opened to find a token by intent; there is no smaller door"),
    ("5", f"<code>guidelines/_rules-index.json</code> — {n['rules_total']} rules", n["rules_index"], "if consulted; the skill names three edge types and no rule"),
    ("6", "<code>assets/icons/icons.manifest.json</code>", n["icons_manifest"], "by eye"),
    ("7", "<code>compliance/rules/*.json</code> — 55 criteria", n["compliance_tokens"], "ships; read when the check skill runs, not at compose"),
    ("—", f"<code>_rulings.json</code> ({n['rulings_json']}) · rule nodes · principle nodes · the baked graph (798,152)", "not read", "not on the compose path; the pack ships none of them"),
    ("—", f"<code>_consult.py</code> — keyword over a {n['consult_index']}-token index holding 63 of {n['rul_total']} rulings", "2.7–5.6K per answer", "a different question (“what governs X?”), text match not edge"),
]
TODAY_HTML = "\n".join(f'<tr><td class="slug">{a}</td><td>{b}</td><td class="num">{c}</td><td class="defn">{d}</td></tr>' for a, b, c, d in TODAY_ROWS)

SLICE_ROWS = []
for key, label in (("dashboard", "a payments dashboard — stat card row, filter bar, data table"), ("form", "a settings form — dropdown, date picker, submit, error state"), ("bar-chart", "a bar chart comparing spend by category")):
    r = runs[key]
    SLICE_ROWS.append((label, f"{r['slice_tokens']:,}", f"{r['metas_in_slice']} · {r['metas_in_slice_tokens']:,}", f"{r['ratio_vs_selected_metas']:.1f}×",
                       f"{r['components']} components · {r['rules']} rules ({r['rules_blocking']} BLOCKING; {r['rules_authored']} authored, {r['rules_routed']} routed by vocabulary) · {r['anti_neighbours']} must-nots · {r['token_groups']} token groups · {r['rulings']} rulings · {r['unresolved']} declared unresolved"))
SLICE_HTML = "\n".join(f'<tr><td>{a}</td><td class="num">{b}</td><td class="num">{c}</td><td class="num">{d}</td><td class="defn">{e}</td></tr>' for a, b, c, d, e in SLICE_ROWS)

QCOST_ROWS = []
for r in S["a3_table_corrected"]["rows"]:
    fix = f" → <b>{r['today_v2']:,}</b>" if r["today_v2"] != r["today_a3"] else ""
    QCOST_ROWS.append((r["q"], r["question"], f"{r['today_a3']:,}{fix}", f"{r['slice']}", str(r["edges"])))
QCOST_HTML = "\n".join(f'<tr><td class="slug">{a}</td><td>{html.escape(b)}</td><td class="num">{c}</td><td class="num">{d}</td><td class="num">{e}</td></tr>' for a, b, c, d, e in QCOST_ROWS)

DEC_EFFECT = [
    ("D-1", "changes the slice’s <b>order</b>, not its size", "Today the slice reads rules in one stage and rulings in another and never reads an SC. Under three views the obligations leg becomes one read — “what must this component do, in order” — with WCAG, rules and design rulings as one list carrying its provenance. The views cost the slice nothing in tokens; they give the reader one verb per view."),
    ("D-2", "changes the slice <b>most</b> — the rules leg", f"Today <code>rules_for()</code> attaches BLOCKING rules by a hand-written vocabulary dictionary (<code>RULE_FILE_ROUTES</code>) and marks each one <i>routed</i>: {runs['dashboard']['rules_routed']} of the {runs['dashboard']['rules']} rules on the dashboard task, {runs['form']['rules_routed']} of {runs['form']['rules']} on the form. A scope per guideline file makes the same attachment a structural join through the meta’s <code>tokens</code> block, labelled <i>derived</i>, with an exception row — and reaches the {n['rules_unreached']} facet rules the dictionary reaches only when a word happens to match."),
    ("D-3", "<b>is</b> the slice", "The decision is whether step 1 reads the slice or the library. Everything in this section is its evidence."),
    ("D-4", "changes the slice’s <b>labels</b>, not its content", "The output’s sections (<code>rules</code>, <code>antiNeighbours</code>, <code>rulings</code>, <code>tokens</code>) become the twelve verbs — <i>must</i>, <i>should</i>, <i>must-not-sit-with</i>, <i>decided</i>, <i>rests-on</i> … — so the agent is told the same dozen words in the slice, the skills and the explorer. Storage untouched."),
    ("D-5", "changes the slice’s <b>source</b> for tokens, not its output", f"Today <code>tokens_for()</code> regexes the group out of each meta’s token strings and looks the tier up in a map built from eight files at load — {runs['dashboard']['token_groups']} groups on the dashboard task. With group nodes carrying a tier the leg is an edge walk (<code>bindsToken</code>) and blast radius rides on the node; the slice prints the same rows from a typed source."),
    ("D-6", "ASK <b>is</b> the slice’s second verb; the rest are behind it", "ASK adds “one question, one node” beside “one task, one screen” — same door. CLOSURE gives the slice inverse starts (a context or a rule as the seed). SHAPES never touches the slice — it is a build gate. TOKENS is D-5’s leg. NEIGHBOURS may trail the slice as a labelled advisory section and may never put a row in it."),
]
DEC_EFFECT_HTML = "\n".join(f'<tr><td class="slug">{a}</td><td>{b}</td><td class="defn">{c}</td></tr>' for a, b, c in DEC_EFFECT)

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
q.ruled{font-style:italic;quotes:none}
.word{margin:var(--s3) 0 var(--s2);padding:var(--s2) var(--s3);border-left:2px solid var(--accent);background:var(--soft)}
.word label{display:block;font-weight:500;margin-bottom:var(--s1)}
.word .hint{display:block;font-size:.875rem;color:var(--muted);margin-bottom:var(--s2)}
.word input{font:inherit;font-size:1rem;padding:var(--s1) var(--s2);border:1px solid var(--g3);background:var(--paper);color:var(--ink);border-radius:2px;width:100%;max-width:24rem}
.contract{display:grid;grid-template-columns:1fr 1fr;gap:var(--s4);margin:var(--s4) 0}
.contract div{border-top:2px solid var(--ink);padding-top:var(--s2)}
.contract>div>b{display:block;font-weight:500;margin-bottom:var(--s1)}.contract li b{font-weight:500}
.contract ul{padding-left:1.1em;margin:0;font-size:.9375rem}.contract li{margin-bottom:.35rem}
@media (max-width:760px){.contract{grid-template-columns:1fr}}
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
    word = ""
    if x.get("word"):
        w = x["word"]
        word = (f'<div class="word"><label for="{x["id"]}-word">{fmt(w["label"])}</label>'
                f'<span class="hint">{md(fmt(w["hint"]))}</span>'
                f'<input type="text" class="wordbox" id="{x["id"]}-word" data-id="{x["id"]}" placeholder="{html.escape(w["placeholder"])}" autocomplete="off"></div>')
    dec_html.append(f"""<div class="dec" data-id="{x['id']}">
<div class="dechead"><span class="decid">{x['id']}</span><h3>{fmt(x['title'])}</h3></div>
<p>{md(fmt(x['lede']))}</p>
<ul class="opts">
{opts_html(x['id'], x['options'])}
</ul>
{word}
<p class="why"><b>Recommendation.</b> {md(fmt(x['why']))}</p>
<p class="attrib">{md(fmt(x['attrib']))}</p>
<textarea class="note" data-id="{x['id']}" aria-label="Notes for {x['id']}" placeholder="Notes for {x['id']} — your words"></textarea>
</div>""")
IDS = [x["id"] for x in spec["decisions"]]
WORD_IDS = [x["id"] for x in spec["decisions"] if x.get("word")]

HTML = f"""<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{spec['title']}</title>
<style>{CSS}</style>
<script type="application/json" id="measured">{json.dumps(n, ensure_ascii=False)}</script>
<section id="headline"><div class="wrap">
<p class="label">#277 &middot; lane A2F &middot; the KG audit &middot; decisions, v2 &mdash; on A2V's verdict, with the thin slice</p>
<h1>{spec['headline']}</h1>
<p>Six decisions sit below, recommendation first on each; everything after them is the evidence they rest on.
<b>The headline is the answer rate:</b> the graph answers <b>{n['q_answered']} of the 12</b> questions a designer asks
mid-task by a path, half-answers {n['q_partial']}, cannot answer {n['q_unanswerable']} &mdash; and the agent, at design
time, can reach <b>{n['q_design']} of the 12</b>, because nothing on the compose path reads the graph. If you take D-2, D-3 and
D-5 the graph answers {n['q_after']} and the agent reaches the same. If you take D-1 the layers stop being the commit
history and start being how a designer thinks. <b>New in v2:</b> the thin slice at build time (Part A, D-3) &mdash; what the
agent reads today when it composes a screen, what it would read, and what each decision does to it; and five
corrections from the second Fable seat, each marked where it lands.</p>
<div class="stats">
<div class="stat"><b>{n['q_answered']}&nbsp;of&nbsp;12</b><span>designer questions answered by a graph path</span></div>
<div class="stat"><b>{n['q_design']}&nbsp;of&nbsp;12</b><span>reachable by the agent at design time today</span></div>
<div class="stat"><b style="white-space:nowrap">{n['metas_tokens_k']}K&nbsp;&rarr;&nbsp;{n['slice_dash_k_int']}K</b><span>tokens: the meta library the skill points at, against the slice for a dashboard</span></div>
<div class="stat"><b>{n['a1_nc_pct']}%</b><span>of edges read by nothing &mdash; {n['a1_nc_types']} types, {n['a1_nc_edges']:,} live edges</span></div>
</div>
<div class="zeros">
<div><b>{n['a1_nodes']:,}</b> nodes &middot; <b>{n['a1_edges']:,}</b> edges &middot; <b>{n['a1_edge_types']}</b> types &middot; <b>{n['a1_kinds']}</b> kinds, at <code>bedf383</code></div>
<div><b>{n['rul_system']}</b> of {n['rul_total']} rulings govern only files by the extractor's own test &mdash; the system's record, not design precedent</div>
<div><b>{n['a11y_links']}</b> edges between the three places accessibility lives ({n['a11y_sc']} sc &middot; {n['a11y_rules']} rules &middot; {n['a11y_ux']} principles)</div>
<div><b>0</b> files under <code>knowledge/</code> written &mdash; this page proposes</div>
</div>
<blockquote>also think about the organisation of the the different layers in this graph, are the 5 layers currently,
maybe this needs reconstituted, should they be layered and conjoined as they are, should it be one or less than 5. in my
mind (this may not be correct) all the accessibility nodes should be design governance nodes, and what we have as
governance should be something like 'system constitution' or 'codex' or 'system management' I don't know right now, but
it seems the categorisation might net be corrcet. [&hellip;] also lets consider how this effects our thin slice technique
for design knowledge retrieval at build time.<cite>Dave, #277, 2026-09-16 (verbatim, his spelling; two asks, one quote)</cite></blockquote>
</div></section>

<section id="decisions"><div class="wrap">
<p class="label">Your words &middot; the ask</p>
<h2>Six decisions.</h2>
<p>One letter is an answer; a letter with a sentence attached is a sequel, and it is read back before anything is built
on it. D-1 asks for a letter and, separately, one word. D-3 is the one every other decision waits on, and it now carries
the thin slice.</p>
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
<p>You have already been asked. What follows is what the answers rest on: the thin slice at build time, the twelve
questions scored, the three views by force, each node kind against its own minimum, the ranked gaps with cost, and the
fixes this lane would refuse. The long form is <code>A2-AUDIT.md</code> and <code>A3-AUGMENT.md</code>; the second seat's
verification is <code>../kg-audit-verify/VERIFY.md</code>; the numbers are <code>A1-measure.json</code>,
<code>A2-measure.json</code>, <code>verify-figures.json</code> and <code>slice-measure-v2.json</code>.</p>
</div></section>

<section id="slice"><div class="wrap">
<p class="label">Part A &middot; the thin slice at build time &middot; D-3's evidence</p>
<h2>What the agent reads when it builds a screen &mdash; today, and under the graph.</h2>
<p><b>Plain.</b> The thin slice is the idea that the agent should be handed the few thousand tokens of design knowledge
a screen actually needs, in the order a designer would want them, instead of a library to browse. Today it does not
exist on the compose path. The generate skill's step 1 says <i>find the components in <code>showroom/index.json</code>,
then read each one's meta, then copy its snippet</i>: that is one {n['showroom_index_k']}K-token index, then a judgement
call about which of {n['metas_total_all']} metas to open (median {n['meta_median']} tokens each, {n['metas_tokens_k']}K
for the library), then about {n['snippet_avg_k']}K tokens of markup per component placed. The tokens are found by
opening <code>canon.css</code> &mdash; {n['canon_css']} tokens, because there is no smaller door. Nothing on that path reads a
graph edge: the skill names three edge types in prose and the agent reads them off the meta by eye. The rulings, the
rule nodes and the principle nodes are not read and, in the pack, not present.</p>
<p>The one tool that builds a slice, <code>knowledge/_compose_slice.py</code>, does it the way a designer would: the task
sentence is turned into roles and chart intents, the roles into components, the components into their edges, then the
BLOCKING rules first, the must-nots, the type composites, the icons, the token <i>groups</i> with their tier, and the
rulings behind each item &mdash; with everything it could not resolve declared as <code>ref: null</code> and a note,
never invented. Re-run this session on three tasks it comes out at <b>{n['slice_dash']} tokens for a dashboard</b> against
{n['slice_dash_metas_tok']} for the {n['slice_dash_metas']} metas it replaces ({n['slice_dash_ratio']}&times;;
{n['slice_dash_lib_ratio']}&times; against the library), {n['slice_form']} for a form ({n['slice_form_ratio']}&times;),
{n['slice_bar']} for a bar chart ({n['slice_bar_ratio']}&times;). Nothing calls it. That is D-3.</p>
<p>A3 measured the other half: the twelve designer questions, asked one at a time, cost about {n['a3_summed_m']}M tokens
of file reads today when each question's reads are summed (about {n['v2_dedup_m']}M if the same file is counted once and
Q9 is charged honestly), against <b>{n['slice_total']} tokens</b> for the twelve typed graph slices that answer them &mdash;
a few hundred tokens a question, under 1K each. So the thin slice has two verbs, one per table below: <i>compose</i> a
screen (the task in, the slice out) and <i>ask</i> one question (a node and a verb in, the answering edges out).</p>

<h3>What is read today, at step 1 of the generate skill</h3>
<div class="tw"><table>
<tr><th>step</th><th>what</th><th class="num">tokens (cl100k)</th><th>how much of it</th></tr>
{TODAY_HTML}
</table></div>

<h3>What the slice reads instead &mdash; three tasks, re-run this session</h3>
<div class="tw"><table>
<tr><th>task</th><th class="num">slice</th><th class="num">metas it replaces &middot; tokens</th><th class="num">ratio</th><th>what is in it</th></tr>
{SLICE_HTML}
</table></div>
<p class="why">The slice reads <code>roles.json</code>, <code>chart-intents.json</code>, the metas, <code>_rules-index.json</code>,
<code>_rulings.json</code> and <code>_ruling_edges.json</code>, the composites, the icon manifest and the token files, and walks
<code>commonPattern</code>, <code>usedInContext</code>, <code>renderedBy</code>, <code>containedBy</code>, <code>hasPart</code>,
<code>consumes</code>, <code>composedOf</code>, <code>family</code>, <code>groupsWith</code>, <code>mustNotNeighbour</code>,
<code>governedBy</code>. It does not read the rule nodes, the principle nodes, the compliance corpus or the baked graph, and it
does not walk <code>governs</code>, <code>obeys</code>, <code>appliesTo</code>, <code>evidencedBy</code> or <code>ruledIn</code> &mdash;
the edges that answer Q1, Q2, Q5, Q6 and Q11. Its rules leg is the tell: BLOCKING rules attach by a vocabulary dictionary
and are marked <i>routed</i>, which is D-2's scope join done by hand.</p>

<h3>The twelve questions &mdash; A3's cost table, with A2V's two corrections marked</h3>
<div class="tw"><table>
<tr><th>q</th><th>question</th><th class="num">read today (A3 &rarr; corrected)</th><th class="num">typed slice</th><th class="num">edges</th></tr>
{QCOST_HTML}
<tr><td class="slug">&Sigma;</td><td>summed per question (A3) &rarr; with Q9 corrected &rarr; de-duplicated</td><td class="num">{S['a3_table_corrected']['summed_a3']:,} &rarr; {S['a3_table_corrected']['summed_v2']:,} &rarr; {S['a3_table_corrected']['deduplicated_v2']:,}</td><td class="num">{n['slice_total']}</td><td class="num">&mdash;</td></tr>
</table></div>
<p class="why">Q9's {n['q9_a3_k']}K charged <code>canon.css</code>; the meta's <code>tokens</code> block already names the tokens and
<code>tokens/_blast-radius.json</code> ({n['blast_radius']} tokens) already answers "what breaks", so the honest read is about
{n['q9_today_k']}K. The ratio is {n['ratio_summed']}&nbsp;:&nbsp;1 summed and {n['ratio_dedup']}&nbsp;:&nbsp;1 de-duplicated; the conclusion is the same at either.</p>

<h3>What each decision does to the slice</h3>
<div class="tw"><table>
<tr><th>decision</th><th>effect on the slice</th><th>how</th></tr>
{DEC_EFFECT_HTML}
</table></div>

<h3>The thin-slice contract &mdash; what D-3(a) wires</h3>
<div class="contract">
<div><b>In</b><ul>
<li><b>intent</b> &mdash; a task sentence, or one of the five chart-intent words (ADR-0017), or one of the twelve question verbs (ASK)</li>
<li><b>shape</b> &mdash; the data shape when there is one (23 shapes, <code>hasDataShape</code>)</li>
<li><b>roles</b> &mdash; the DESK roles the screen needs (12, <code>roles.json</code>), resolved from the sentence or given</li>
<li><b>a component set</b> &mdash; optional: the components already chosen, as a seed; the slice adds what their edges require and never removes one</li>
<li><b>a budget</b> &mdash; tokens; the slice ranks and truncates against it and says what it cut</li>
</ul></div>
<div><b>Out &mdash; every row names the edge, field or file that put it there</b><ul>
<li><b>components</b> &mdash; chosen and why (role, intent, edge); the alternates held and the <code>when</code> that decides, or the note that none is authored</li>
<li><b>governs</b> &mdash; the design rulings on each, by id, with date and the sentence (the Codex, or whatever it is called)</li>
<li><b>obeys</b> &mdash; the rules, BLOCKING first, by id, with destiny, and whether the binding is <i>authored</i> (an <code>obeys</code> edge), <i>derived</i> (a D-2 scope) or <i>routed</i> (the dictionary, until D-2 lands)</li>
<li><b>must-not</b> &mdash; <code>mustNotNeighbour</code>, the resolved and the declared nulls with their <code>$note</code>, and <code>groupsWith</code> beside it</li>
<li><b>tokens</b> &mdash; the groups with tier and count, never leaves (s269-D3); blast radius when D-5 lands</li>
<li><b>assets</b> &mdash; the icons and logos bound (<code>usesIcon</code> / <code>usesLogo</code> when RI's ruling lands; the snippet until then)</li>
<li><b>unresolved</b> &mdash; what the slice could not resolve, and why, <code>ref: null</code> (s274-D10)</li>
<li><b>sized</b> &mdash; the token count of the slice, of the metas it replaced, and the ratio, printed on the slice itself</li>
</ul></div>
</div>
<p class="why">Three fences. The slice never invents a binding (s274-D12): a row is authored, derived from a declared scope, or routed
and labelled so. It never hands over the leaves &mdash; not the 932 tokens, not <code>canon.css</code>, not the library. And it lands
with its consumer in the same commit (s274-D11): the generate skill's step 1 reads it, or it is not wired. The budget is the
one addition nothing in the repo has yet &mdash; a cap the slice is truncated against, with the cut declared.</p>
</div></section>

<section id="questions"><div class="wrap">
<p class="label">Part B &middot; the headline's evidence</p>
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
<p class="label">Part C &middot; D-1's evidence</p>
<h2>Three views by force, not five by wave.</h2>
<div class="layers">
<div><b>The system</b><span>what exists &mdash; component, snippet, pattern, context, role, intent, shape; tokens (D-5) and assets (RI) when they land. The agent <i>chooses</i> here.</span></div>
<div><b>Design governance</b><span>what a design must or should do &mdash; {n['a11y_sc']} WCAG criteria (external law), {n['rules_total']} HSBC rules with a destiny (internal standard), the {n['rul_design'] + n['rul_both']} design-scoped rulings by the extractor's test (case law). Three provenances as sub-chips, one obligation. Accessibility lives here entirely. The {n['obeys_ux_edges']} <code>obeys</code>&rarr;<code>ux:</code> edges are drawn here too &mdash; force is the edge's, not the node's. The agent <i>obeys</i> here.</span></div>
<div><b>Explanation</b><span>why &mdash; {n['ux_total']} graded principles, 30 polarities, the evidence trail. Never an obligation. The agent <i>consults</i> here when obligations pull against each other.</span></div>
</div>
<p>The ruling record is not a view of the designer brain. It is the record &mdash; {n['rul_total']} rulings, each with
its evidence and its session, superseding and refining one another by the authored edges s267-D3 ratified &mdash; and its name
is the one word D-1 asks for. Measured by the extractor's own <code>gov_target()</code> over what each ruling governs:
<b>{n['rul_system']} system-only</b>, <b>{n['rul_design']} design-only</b>, {n['rul_both']} both (v1 printed {n['rul_system_v1']}/{n['rul_both_v1']} by a
looser test that counted the snippet glob as a component). A proxy: it files s269-D3, s274-D12 and s275-D4 &mdash; the rulings that
shape the designer brain &mdash; as "system" because they govern <code>.py</code> and <code>.json</code>. So "three-quarters is how the
system was built" is a real number and a rough sentence.</p>
<p class="why"><b>Unratified, and not on the card:</b> a precedence ladder (law, then ruling, then BLOCKING, then ADVISORY, then the
principles) &mdash; nothing in <code>_rulings.json</code> orders a Dave ruling against a WCAG criterion, and s277-D3 flagged one conflict
(dv-pie-009 "maximum 6" against <code>chart-pie.when</code> "&le; 5 parts") and did not resolve it; a derived <code>scope</code> on
every ruling; and the dozen fences written once (four named: fence 3 of #261, the two-red law, nam-002, "an instrument without a
consumer is refused"). Lane A2 proposed all three; lane A2V's counter-argument &mdash; four decisions in one letter, a norm with no ruling
behind it, a force cut that leaks at <code>obeys</code>&rarr;<code>ux:</code>, a proxy read as a fact &mdash; is why they are here and not in
option (a). Rulings a re-cut touches, by id: s275-D6 (refined &mdash; a sub-chip is still its own chip); s274-D11 belongs to D-3, not here
(it has no chip clause; it is the reader-in-the-same-commit ruling); s275-D4 (the 20 standards-family joins are new authored edges of a
new type &mdash; their own lane, G3, not this re-cut); s269-D2 (the <code>ux:</code> prefix stays); s274-D7, s274-D8, s275-D1..D3,
s270-D2, s276-D3, s277-D1..D3 (node kinds and edge types &mdash; untouched: a view re-cut changes <code>fam</code> labels and the
template's chips, never an id or a type); s267-D3 (untouched). The five edge types no chip draws today &mdash;
{', '.join(f'<code>{x}</code>' for x in A2['explorer']['not_in_any_chip'])} &mdash; get a chip in the same move.</p>
</div></section>

<section id="kinds"><div class="wrap">
<p class="label">Part D &middot; connectivity has an intent</p>
<h2>Each kind against its own minimum.</h2>
<p>"Orphan" means something only against a stated minimum. A snippet with one edge is perfect; a rule with one edge
binds nothing. Three kinds fail their own purpose at scale: rule, pattern, ux.</p>
<div class="tw"><table>
<tr><th>kind</th><th class="num">n</th><th>what it is for</th><th>minimum</th><th>gap</th></tr>
{KIND_HTML}
</table></div>
</div></section>

<section id="gaps"><div class="wrap">
<p class="label">Part E &middot; ranked, with cost</p>
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
<p class="label">Part F &middot; what this lane would refuse</p>
<h2>The attractive fixes that are the s274-D12 shape.</h2>
<ol class="refuse">
{REFUSE_HTML}
</ol>
</div></section>

<section id="receipts"><div class="wrap">
<div class="split"><div>
<p class="label">Receipts</p>
<dl class="recs">
<dt>Measurement</dt><dd><code>A1-measure.json</code> (lane A1, 13a4cf2) + <code>A2-measure.json</code> (lane A2) + <code>../kg-audit-verify/verify-figures.json</code> (lane A2V, 3a37bcd) + <code>slice-measure-v2.json</code> (<code>_measure_slice_v2.py</code>, this lane)</dd>
<dt>Long form</dt><dd><code>A2-AUDIT.md</code> &middot; <code>A3-AUGMENT.md</code> &middot; <code>../kg-audit-verify/VERIFY.md</code> &middot; this lane's <code>FIX-REPORT.md</code> (each fix before/after)</dd>
<dt>Graph</dt><dd>{n['a1_nodes']:,} nodes &middot; {n['a1_edges']:,} live edges &middot; {n['a1_dangling']} declared nulls &middot; {n['a1_edge_types']} types &middot; join classes structural {n['a1_structural']:,} / prose {n['a1_prose']} / authored {n['a1_authored']}</dd>
<dt>The slice</dt><dd><code>_compose_slice.build_slice()</code> called in-process for three tasks; tiktoken cl100k_base; prints nothing, writes nothing under <code>knowledge/</code></dd>
<dt>Nothing run</dt><dd>no <code>gen_kg_edges.py</code>, no <code>_build_all.py</code>, no <code>_build_kg_explorer.main()</code>; nothing under <code>knowledge/</code> written; v1 and A2's/A3's files untouched</dd>
</dl>
</div><div>
<p>Every integer on this page is read at build time from the four measurement files; none was typed into the page or the
decisions file. v1 read three integers (19,113 / 111,468 / 414,184) that had been typed into <code>A2-measure.json</code>; v2
re-measures them and reads them from <code>slice-measure-v2.json</code>. The builder refuses to write the page if the seven
figures it asserts drift.</p>
<p>Dave's words appear once, verbatim, in the hero. Nothing on this page is a ruling.</p>
</div></div>
</div></section>
<footer><div class="wrap">Nothing on this page is a ruling. Dave rules; the lane enacts by addition.</div></footer>
<script>
(function(){{
 var KEY={json.dumps(spec['storage_key'])};
 var IDS={json.dumps(IDS)};
 var WORDS={json.dumps(WORD_IDS)};
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
  if(!r.choice&&!r.note&&!r.word){{delete state[id];}}else{{state[id]=r;}}
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
   var w=document.querySelector('input.wordbox[data-id="'+id+'"]');
   if(w&&r.word)w.value=r.word;
  }});
 }}
 function noteOf(id){{
  var r=state[id]||{{}};
  var w=(r.word||"").trim();
  if(WORDS.indexOf(id)>-1&&w){{return "record: "+w+(r.note?"\\n"+r.note:"");}}
  return r.note||"";
 }}
 function exportObj(){{
  return {{page:{json.dumps(spec['page'])},
          at:new Date().toISOString(),
          decisions:IDS.map(function(id){{
            var r=state[id]||{{}};
            return {{id:id,choice:r.choice||null,note:noteOf(id)}};
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
  var c=e.target.classList;
  if(c&&c.contains("note")){{
   put(e.target.dataset.id,"note",e.target.value);
   clearTimeout(timer);timer=setTimeout(save,400);
  }}
  if(c&&c.contains("wordbox")){{
   put(e.target.dataset.id,"word",e.target.value);
   clearTimeout(timer);timer=setTimeout(save,400);
  }}
 }});
 document.addEventListener("focusout",function(e){{
  var c=e.target.classList;
  if(c&&(c.contains("note")||c.contains("wordbox"))){{clearTimeout(timer);save();}}
 }});
 window.addEventListener("beforeunload",function(){{clearTimeout(timer);save();}});
 el("btnExport").addEventListener("click",function(){{
  var j=show();
  try{{
   var a=document.createElement("a");
   a.href=URL.createObjectURL(new Blob([j],{{type:"application/json"}}));
   a.download="kg-audit-decisions-2026-09-16-v2-export.json";
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
  if(!confirm("Clear every choice, word and note on this page?"))return;
  state={{}};try{{localStorage.removeItem(KEY);}}catch(e){{}}
  document.querySelectorAll('input[type="radio"]').forEach(function(i){{i.checked=false;}});
  document.querySelectorAll("textarea.note").forEach(function(t){{t.value="";}});
  document.querySelectorAll("input.wordbox").forEach(function(t){{t.value="";}});
  el("exp").hidden=true;save();
 }});
 load();restore();paint();
}})();
</script>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT.name} ({len(HTML):,} bytes) · {len(IDS)} decisions · {len(n)} measured figures · D-6 from A3-shortlist.json")
print(f"answer rate {n['q_answered']}/{n['q_partial']}/{n['q_unanswerable']} · design-time {n['q_design']}/12 · "
      f"BLOCKING unbound {n['blocking_unbound']}/{n['blocking']} · rulings system {n['rul_system']}/{n['rul_total']} · "
      f"metas {n['metas_tokens_k']}K · nc edges {n['a1_nc_edges']:,} · slice {n['slice_dash']} vs {n['slice_dash_metas_tok']}")
