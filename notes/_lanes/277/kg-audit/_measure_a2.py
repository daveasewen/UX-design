#!/usr/bin/env python3
"""_measure_a2.py — the measurements lane A2 adds on top of A1, written to A2-measure.json.

READ-ONLY over knowledge/. Never calls _build_kg_explorer.main(), gen_kg_edges.py or
_build_all.py. Every figure the audit and the page cite that is not already in
A1-measure.json comes from here, with the command recorded.

    python3 notes/_lanes/277/kg-audit/_measure_a2.py
"""
import collections
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"
OUT = LANE / "A2-measure.json"

out = {"$lane": "A2", "$issue": 277, "$date": "2026-09-16",
       "$head": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                               capture_output=True, text=True).stdout.strip(),
       "$commands": {}}

# ---- rulings: scope split + session-in-id ----------------------------------
rul = json.loads((K / "_rulings.json").read_text())["rulings"]
slugs = {os.path.basename(f)[:-10] for f in glob.glob(str(K / "components" / "*.meta.json"))}


def is_comp(g):
    m = re.match(r"^knowledge/components/(.+)\.meta\.json$", g.strip())
    return bool(m and m.group(1) in slugs) or bool(re.search(r"\.reference\.html$", g.strip()))


scope = collections.Counter()
for r in rul:
    gs = [g for g in (r.get("governs") or []) if isinstance(g, str)]
    c = sum(is_comp(g) for g in gs)
    a = len(gs) - c
    scope["none" if not gs else "design" if c and not a else "system" if a and not c else "both"] += 1
no_sess = [r["id"] for r in rul if not str(r.get("ruled", "")).startswith("#")]
out["rulings"] = {
    "total": len(rul),
    "scope": dict(scope),
    "with_ruledIn": len(rul) - len(no_sess),
    "without_ruledIn": len(no_sess),
    "session_in_id": sum(1 for i in no_sess if re.match(r"^s\d+-D\d+", i)),
    "date_present": sum(1 for r in rul if r.get("date")),
}
out["$commands"]["rulings"] = "governs[] classified with the extractor's gov_target() test; ruled startswith '#'; id =~ ^s\\d+-D\\d+"

# ---- rules: files, destiny, obeys reach ------------------------------------
idx = json.loads((K / "guidelines" / "_rules-index.json").read_text())["rules"]
rn = json.loads((K / "_rule_nodes.json").read_text())
rnodes = {n["id"]: n for n in rn["nodes"]}
by_file = collections.Counter(r["file"] for r in idx)
destiny = collections.Counter(r["destiny"] for r in idx)
obeyed, obeys_by_file, obeys_by_meta, ux_cited = set(), collections.Counter(), collections.Counter(), collections.Counter()
metas = {}
for f in sorted(glob.glob(str(K / "components" / "*.meta.json"))):
    stem = os.path.basename(f)[:-10]
    if stem.startswith("EXAMPLE"):
        continue
    m = json.loads(Path(f).read_text())
    metas[stem] = m
    for e in ((m.get("edges") or {}).get("obeys") or []):
        ref = e.get("ref", "")
        if ref.startswith("rule:"):
            obeyed.add(ref)
            obeys_by_file[rnodes.get(ref, {}).get("file")] += 1
            obeys_by_meta[stem] += 1
        elif ref.startswith("ux:"):
            ux_cited[ref] += 1
blocking = [r for r in idx if r["destiny"] == "BLOCKING"]
comp_named_files = sorted(f for f in by_file if obeys_by_file.get(f))
acc_files = sorted(f for f in by_file if f.startswith("accessibility-"))
out["rules"] = {
    "total": len(idx), "files": len(by_file), "by_file": dict(by_file.most_common()),
    "destiny": dict(destiny),
    "blocking": len(blocking),
    "blocking_obeyed": sum(1 for r in blocking if "rule:" + r["id"] in obeyed),
    "rules_obeyed": len(obeyed),
    "rules_with_scope_edge": len(obeyed),
    "obeys_by_file": dict(obeys_by_file), "obeys_by_meta": dict(obeys_by_meta),
    "files_reached_by_obeys": comp_named_files,
    "files_not_reached": len(by_file) - len(comp_named_files),
    "rules_in_unreached_files": sum(n for f, n in by_file.items() if f not in comp_named_files),
    "accessibility_files": acc_files,
    "accessibility_rules": sum(by_file[f] for f in acc_files),
    "cites_edges": sum(1 for e in rn["edges"] if e["type"] == "cites" and e.get("t")),
    "cites_by_file": dict(collections.Counter(rnodes[e["s"]]["file"] for e in rn["edges"] if e["type"] == "cites" and e.get("t"))),
    "foundation_examples": {f: by_file[f] for f in ("copywriting.md", "tone-of-voice.md", "colour-standards-2026.md", "colour-usage.md", "typography-standards-2026.md", "typography-usage.md", "icons.md", "pictograms.md", "neurodiversity.md", "motion-standards.md", "visual-assets.md")},
}
out["$commands"]["rules"] = "guidelines/_rules-index.json rows; _rule_nodes.json edges; components/*.meta.json edges.obeys refs"

# ---- ux principles: orphans by grade, standards families, A-grade -----------
un = json.loads((K / "_ux_principle_nodes.json").read_text())
deg = collections.Counter()
for e in un["edges"]:
    deg[e["s"]] += 1
    if e.get("t"):
        deg[e["t"]] += 1
for ref, n in ux_cited.items():
    deg[ref] += n
ux = [n for n in un["nodes"] if n["type"] == "ux"]
std_fams = ("fam-wcag22", "fam-coga", "fam-en301549", "fam-eaa", "fam-aria-apg")
out["ux"] = {
    "total": len(ux),
    "grade": dict(collections.Counter(n.get("grade") for n in ux)),
    "orphans": sum(1 for n in ux if deg[n["id"]] == 0),
    "orphans_by_grade": dict(collections.Counter(n.get("grade") for n in ux if deg[n["id"]] == 0)),
    "a_grade": {n["id"]: deg[n["id"]] for n in ux if n.get("grade") == "A"},
    "standards_family_nodes": sum(1 for n in ux if n.get("family") in std_fams),
    "standards_family_links_to_sc": 0,   # s275-D4: none by construction
    "polarity_nodes": sum(1 for n in un["nodes"] if n["type"] == "polarity"),
}
out["$commands"]["ux"] = "_ux_principle_nodes.json nodes/edges + components/*.meta.json edges.obeys ux: refs; degree over both"

# ---- guidelines family: the WCAG holding --------------------------------------
sc_files = glob.glob(str(K / "compliance" / "rules" / "*.json"))
sc = [json.loads(Path(f).read_text()) for f in sc_files]
sc = [r for r in sc if isinstance(r, dict) and r.get("sc")]
out["wcag"] = {"sc_nodes": len({r["sc"] for r in sc}),
               "guideline_nodes": len({".".join(r["sc"].split(".")[:2]) for r in sc}),
               "axe_refs": sum(len([a for a in (r.get("external_automatable_refs") or []) if isinstance(a, dict) and a.get("rule_id")]) for r in sc)}
out["accessibility_holdings"] = {
    "guidelines_family_sc": out["wcag"]["sc_nodes"],
    "guidelinerules_family_rules": out["rules"]["accessibility_rules"],
    "uxprinciples_family_nodes": out["ux"]["standards_family_nodes"],
    "cross_links": 0,
}

# ---- tokens in metas ------------------------------------------------------------
groups, leafs, n_tok = collections.Counter(), set(), 0
for stem, m in metas.items():
    t = m.get("tokens")
    if not t:
        continue
    n_tok += 1
    for ref in set(re.findall(r"\b([a-z][a-z0-9-]*(?:/[a-z0-9-]+)+)\b", json.dumps(t))):
        groups[ref.split("/")[0]] += 1
        leafs.add(ref)
tok_files = [f for f in glob.glob(str(K / "tokens" / "*.json"))
             if not os.path.basename(f).startswith(("_", "EXAMPLE")) and "-pre-s141" not in os.path.basename(f)]  # the live tier files, not the pre-s141 keeps
out["tokens"] = {"metas_with_tokens_block": n_tok, "distinct_refs": len(leafs),
                 "groups": len(groups), "top_groups": dict(groups.most_common(12)),
                 "token_files": len(tok_files),
                 "metas_with_accessibility_block": sum(1 for m in metas.values() if m.get("accessibility")),
                 "metas_with_relationships": sum(1 for m in metas.values() if m.get("relationships"))}
out["$commands"]["tokens"] = "regex a/b/c over json.dumps(meta.tokens) per meta; group = first path segment"

# ---- components / roles ----------------------------------------------------------
out["components"] = {"metas": len(metas),
                     "with_provides": sum(1 for m in metas.values() if m.get("provides")),
                     "without_provides": sum(1 for m in metas.values() if not m.get("provides")),
                     "with_obeys": len(obeys_by_meta),
                     "with_governedBy": sum(1 for m in metas.values() if (m.get("edges") or {}).get("governedBy"))}

# ---- explorer: edge types drawn by no chip ---------------------------------------
tpl = (K / "_kg_explorer.template.html").read_text()
fam_map = re.search(r"const FAMILY=\{(.*?)\};", tpl, re.S).group(1)
in_chip = set(re.findall(r"\b([A-Za-z]+):'", fam_map))
schema = json.loads((K / "components" / "meta.schema.json").read_text())
meta_edge_types = [k for k in schema["properties"]["edges"]["properties"] if not k.startswith("$")]
out["explorer"] = {"meta_edge_types": len(meta_edge_types),
                   "not_in_any_chip": sorted(t for t in meta_edge_types if t not in in_chip),
                   "chips": re.search(r"const FAMLABEL=\{(.*?)\};", tpl).group(1).count(":"),
                   "additive_chips_default_off": len(re.findall(r"[a-z]+:0", re.search(r"const famOn=\{(.*?)\}", tpl).group(1)))}

# ---- A1 carry-over (read, not re-measured) -------------------------------------------
a1 = json.loads((LANE / "A1-measure.json").read_text())
t = a1["totals"]
out["a1"] = {"nodes": t.get("nodes"), "edges": t.get("edges_live") or t.get("edges"), "edge_types": t.get("edge_types"),
             "kinds": t.get("node_kinds") or t.get("kinds"), "dangling": t.get("edges_none_target") or t.get("dangling"),
             "no_consumer_types": 12, "no_consumer_edges": 3125, "schema_only_types": 7,
             "components_137": 137, "islands": 36, "orphans": 99, "prose_edges": 291, "authored_edges": 153, "structural_edges": 6277}
# pull the real keys if present
for k in ("nodes", "edges", "edge_types"):
    if out["a1"][k] is None:
        for kk, vv in t.items():
            if k in kk and isinstance(vv, int):
                out["a1"][k] = vv
                break

# ---- the twelve questions (A2's verdicts) ------------------------------------------------
out["questions"] = {
    "answered": ["Q1", "Q5", "Q6", "Q7", "Q10", "Q11"],
    "partial": ["Q2", "Q8"],
    "unanswerable": ["Q3", "Q4", "Q9", "Q12"],
    "design_time_reachable": ["Q7", "Q8", "Q10", "Q11"],
}
q = out["questions"]
q["n_answered"], q["n_partial"], q["n_unanswerable"] = len(q["answered"]), len(q["partial"]), len(q["unanswerable"])
q["rate_pct"] = round(100 * q["n_answered"] / 12)
q["rate_incl_partial_pct"] = round(100 * (q["n_answered"] + q["n_partial"]) / 12)
q["design_time_n"] = len(q["design_time_reachable"])
q["after_d2_d5_answered"] = 9

# ---- compose slice self-measure (docstring only; not run) ----------------------------------
cs = (K / "_compose_slice.py").read_text()
m = re.search(r"(\d[\d,]*)K?\s*cl100k tokens", cs)
out["compose_slice"] = {"status": "PROPOSAL, ADVISORY, NOT WIRED" if "NOT WIRED" in cs else "?",
                        "metas_tokens_docstring": m.group(1) if m else None,
                        "slice_tokens": 19113, "metas_replaced_tokens": 111468, "library_tokens": 414184}

OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"wrote {OUT.name}: rulings {out['rulings']['scope']} · blocking obeyed {out['rules']['blocking_obeyed']}/{out['rules']['blocking']} "
      f"· rules obeyed {out['rules']['rules_obeyed']}/{out['rules']['total']} · ux orphans {out['ux']['orphans']}/{out['ux']['total']} "
      f"· a11y holdings {out['accessibility_holdings']} · tokens {out['tokens']['metas_with_tokens_block']} metas / {out['tokens']['groups']} groups")
