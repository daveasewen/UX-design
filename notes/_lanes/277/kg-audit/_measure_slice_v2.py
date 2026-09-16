#!/usr/bin/env python3
"""_measure_slice_v2.py — the THIN SLICE at build time, measured (#277 lane A2F).

Dave: "also lets consider how this effects our thin slice technique for design knowledge
retrieval at build time." The thin slice IS `knowledge/_compose_slice.py` (PROPOSAL, nothing
calls it), the generate skill's step 1 (read showroom/index.json, then the metas it names),
`_consult.py` (keyword over 63 of 593 rulings) and A3's ASK door (proposed).

This script writes ONE file — `slice-measure-v2.json` beside it — and nothing else. It
imports `_compose_slice.build_slice()` in-process (prints nothing, writes nothing under
knowledge/; A2V did the same at 3a37bcd). tiktoken cl100k_base, the same estimator A3 and
A2V used. No generator runs; `_build_kg_explorer.main()` is never called.

    python3 notes/_lanes/277/kg-audit/_measure_slice_v2.py
"""
import glob
import json
import os
import sys
from pathlib import Path

import tiktoken

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"
ENC = tiktoken.get_encoding("cl100k_base")
sys.path.insert(0, str(K))
sys.argv = [sys.argv[0]]  # the help gate reads argv
import _compose_slice as cs  # noqa: E402


def tok(p):
    return len(ENC.encode(Path(p).read_text(encoding="utf-8", errors="replace")))


def tok_glob(pat):
    files = sorted(glob.glob(str(pat)))
    return {"files": len(files), "tokens": sum(tok(f) for f in files)}


# ---- 1. what the agent reads TODAY at step 1 (the generate skill's own "where things live")
today = {
    "showroom_index": tok(REPO / "showroom/index.json"),
    "metas_all": tok_glob(K / "components/*.meta.json"),
    "metas_non_example": {"files": len([f for f in glob.glob(str(K / "components/*.meta.json")) if not os.path.basename(f).startswith("EXAMPLE-")]),
                          "tokens": sum(tok(f) for f in glob.glob(str(K / "components/*.meta.json")) if not os.path.basename(f).startswith("EXAMPLE-"))},
    "metas_bytes": sum(os.path.getsize(f) for f in glob.glob(str(K / "components/*.meta.json"))),
    "canon_css": tok(K / "canon/canon.css"),
    "type_css": tok(K / "canon/type.css"),
    "snippets_all": tok_glob(K / "snippets/*.reference.html"),
    "rules_index": tok(K / "guidelines/_rules-index.json"),
    "compliance_rules": tok_glob(K / "compliance/rules/*.json"),
    "icons_manifest": tok(K / "assets/icons/icons.manifest.json"),
    "roles_json": tok(K / "roles.json"),
    "chart_intents": tok(K / "chart-intents.json"),
    "rulings_json": tok(K / "_rulings.json"),
    "blast_radius": tok(K / "tokens/_blast-radius.json"),
    "consult_index": tok(K / "_consult-index.json"),
    "ux_principle_nodes": tok(K / "_ux_principle_nodes.json"),
}
today["meta_median"] = sorted(tok(f) for f in glob.glob(str(K / "components/*.meta.json")))[len(glob.glob(str(K / "components/*.meta.json"))) // 2]

# ---- 2. the slice, three tasks, in-process ------------------------------------------------
TASKS = [
    ("dashboard", "a payments dashboard screen with a stat card row, a filter bar and a data table"),
    ("bar-chart", "a bar chart comparing spend by category"),
    ("form", "a settings form with a dropdown, a date picker and a submit button, with an error state"),
]
g = cs.load_graph()
runs = []
for key, task in TASKS:
    s = cs.build_slice(task, graph=g)
    m = s["measure"]
    runs.append({
        "key": key, "task": task,
        "slice_tokens": m["slice_tokens"],
        "metas_in_slice": m["metas_in_slice"],
        "metas_in_slice_tokens": m["metas_in_slice_tokens"],
        "ratio_vs_selected_metas": m["ratio_vs_selected_metas"],
        "ratio_vs_whole_library": m["ratio_vs_whole_library"],
        "components": len(s["components"]),
        "rules": len(s["rules"]), "rules_blocking": sum(1 for r in s["rules"] if r["blocking"]),
        "rules_authored": sum(1 for r in s["rules"] if r["confidence"] == "authored"),
        "rules_routed": sum(1 for r in s["rules"] if r["confidence"] == "routed"),
        "anti_neighbours": len(s["antiNeighbours"]),
        "type_composites": len(s["typeComposites"]),
        "icons": len(s["icons"]),
        "token_groups": len(s["tokens"]),
        "token_tiers": sorted({t["tier"] for t in s["tokens"]}),
        "rulings": len(s["rulings"]),
        "unresolved": len(s["unresolved"]),
        "sections_tokens": {k: len(ENC.encode(json.dumps(s[k], ensure_ascii=False)))
                            for k in ("components", "rules", "antiNeighbours", "typeComposites", "icons", "tokens", "rulings", "unresolved")},
    })
library_tokens = runs[0] and cs.measure({"components": []}, g)["library_metas_tokens"]

# ---- 3. what the slice does NOT read today (the stores each decision would add) ----------------
reads = {
    "reads_today": ["roles.json", "chart-intents.json", "components/*.meta.json", "guidelines/_rules-index.json",
                    "_rulings.json", "_ruling_edges.json", "_consult-lexicon.json", "tokens/typography-composites.json",
                    "tokens/semantic-colour.json", "tokens/*.json (tier map)", "component-types.json", "assets/icons/icons.manifest.json"],
    "does_not_read": ["_rule_nodes.json", "_ux_principle_nodes.json", "compliance/rules/*.json (sc, appliesTo)",
                      "tokens/_blast-radius.json", "the baked graph (extract()+extract_extra())"],
    "edge_types_walked": ["commonPattern", "usedInContext", "renderedBy", "containedBy", "hasPart", "consumes",
                          "composedOf", "family", "groupsWith", "mustNotNeighbour", "governedBy"],
    "edge_types_not_walked_that_answer_a_question": ["governs (Q1, 295 → components)", "obeys (Q2/Q4)", "appliesTo (Q11)",
                                                      "evidencedBy (Q6)", "ruledIn (Q5)", "cites (rule → sc)"],
    "rule_leg_routed_not_typed": "rules_for(): BLOCKING rules attach by RULE_FILE_ROUTES vocabulary match, marked confidence:'routed' — this is the D-2 scope join done by hand in a dict",
}

# ---- 4. A3's Q-table, corrected per A2V F27/F28 ------------------------------------------------
a3 = json.loads((LANE / "A3-shortlist.json").read_text(encoding="utf-8"))["measure"]
qrows = []
files_by_q = {  # the file SET each question reads today, for the de-duplicated union (A2V F27)
    "Q1": ["rulings.json", "meta"], "Q2": ["rules-index", "all_metas"], "Q3": ["rules-index", "ux_principle_nodes"],
    "Q4": ["meta", "rules-index", "guidelines_md"], "Q5": ["rulings.json"], "Q6": ["rulings.json"],
    "Q7": ["chart-intents", "roles", "all_metas"], "Q8": ["meta"], "Q9": ["meta", "blast_radius"],
    "Q10": ["meta"], "Q11": ["compliance_rules"], "Q12": ["icons_manifest", "photo_manifest", "snippet"],
}
corpus = dict(a3["corpus_tokens"])
meta_as_a3 = next(q["today_tokens"] for q in a3["questions"] if q["q"] == "Q8")  # "the meta" as A3 costed it (5,286 = its five samples' mean), so Q9's correction sits on A3's own row, as A2V did
corpus.update({"meta": meta_as_a3, "blast_radius": today["blast_radius"], "roles": today["roles_json"],
               "chart-intents": today["chart_intents"],
               # the snippet as A3 costed it inside Q12 (= Q12 today − icons manifest − photo manifest), not typed
               "snippet": next(q["today_tokens"] for q in a3["questions"] if q["q"] == "Q12") - a3["corpus_tokens"]["icons_manifest"] - a3["corpus_tokens"]["photo_manifest"]})
for q in a3["questions"]:
    row = {"q": q["q"], "question": q["question"], "today_a3": q["today_tokens"],
           "slice": q["graph_slice_tokens"], "edges": q["graph_slice_edges"], "verdict": q["graph_answer"]}
    if q["q"] == "Q9":
        row["today_v2"] = meta_as_a3 + today["blast_radius"]
        row["today_v2_note"] = "the meta as A3 costed it (Q8 row) + tokens/_blast-radius.json (A2V F28); A3 charged canon.css 588,102"
    else:
        row["today_v2"] = q["today_tokens"]
    qrows.append(row)
summed_a3 = sum(q["today_tokens"] for q in a3["questions"])
summed_v2 = sum(r["today_v2"] for r in qrows)
union_files = set()
for q, fs in files_by_q.items():
    union_files |= set(fs)
dedup_v2 = sum(corpus[f] for f in union_files)
slice_total = sum(q["graph_slice_tokens"] for q in a3["questions"])

out = {
    "$lane": "A2F", "$issue": 277, "$date": "2026-09-16",
    "$method": "tiktoken cl100k_base 0.14.0; _compose_slice.build_slice() in-process; nothing under knowledge/ written",
    "today": today,
    "library_tokens_compose_slice_measure": library_tokens,
    "slice_runs": runs,
    "slice_reads": reads,
    "a3_table_corrected": {"rows": qrows, "summed_a3": summed_a3, "summed_v2": summed_v2,
                           "deduplicated_v2": dedup_v2, "dedup_files": sorted(union_files),
                           "slice_total": slice_total,
                           "ratio_summed": round(summed_v2 / slice_total), "ratio_dedup": round(dedup_v2 / slice_total)},
    "obeys_to_ux": None,
}
# the 14 obeys→ux edges (s276-D3), by meta — the leak A2V named under D-1 point 3
o2u = {}
for f in sorted(glob.glob(str(K / "components/*.meta.json"))):
    m = json.load(open(f, encoding="utf-8"))
    for e in ((m.get("edges") or {}).get("obeys") or []):
        if isinstance(e, dict) and str(e.get("ref", "")).startswith("ux:"):
            o2u.setdefault(os.path.basename(f)[:-10], []).append(e["ref"])
out["obeys_to_ux"] = {"edges": sum(len(v) for v in o2u.values()), "by_meta": o2u,
                      "distinct_ux": sorted({r for v in o2u.values() for r in v})}
# token group-mentions, A2's own regex (_measure_a2.py:144) — for the "top 12 carry N%" figure A2V quoted
import collections, re  # noqa: E402
groups = collections.Counter()
for f in sorted(glob.glob(str(K / "components/*.meta.json"))):
    t = json.load(open(f, encoding="utf-8")).get("tokens")
    if not t:
        continue
    for ref in set(re.findall(r"\b([a-z][a-z0-9-]*(?:/[a-z0-9-]+)+)\b", json.dumps(t))):
        groups[ref.split("/")[0]] += 1
top12 = sum(n for _, n in groups.most_common(12))
out["token_groups"] = {"groups": len(groups), "mentions": sum(groups.values()), "top12_mentions": top12,
                       "top12_pct": round(100 * top12 / sum(groups.values()))}

(LANE / "slice-measure-v2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("today",)}, indent=1))
for r in runs:
    print(r["key"], r["slice_tokens"], "vs", r["metas_in_slice"], "metas", r["metas_in_slice_tokens"], "ratio", r["ratio_vs_selected_metas"],
          "| rules", r["rules"], "blocking", r["rules_blocking"], "| groups", r["token_groups"], "| rulings", r["rulings"], "| unresolved", r["unresolved"])
print("A3 summed", summed_a3, "→ v2 summed", summed_v2, "dedup", dedup_v2, "slices", slice_total)
print("obeys→ux", out["obeys_to_ux"]["edges"], out["obeys_to_ux"]["by_meta"])
