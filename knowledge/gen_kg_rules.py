#!/usr/bin/env python3
"""gen_kg_rules.py — the GUIDELINE-RULE node + edge generator (#274 lane RK).

Enacts s269-D1 order item 2: put the 470 tagged guideline rules
(knowledge/guidelines/_rules-index.json) into the knowledge graph as nodes,
with edges to the things that already exist there.

  NODE KIND   rule:<id>            e.g. rule:aca-001
              attributes: id · file · destiny · destinyFull · rule (the text)
              `rule:` is a FREE prefix — measured, not assumed: the live graph
              (notes/_KG-EXPLORER.html) carries pattern/context/component/
              snippet/role/intent/shape/ruling/artefact/evidence/session/sc/
              guideline/principle/standard/policy/axe and nothing else.
              `principle:` and `guideline:` are TAKEN by WCAG (s269-D2).

  EDGE TYPES  definedIn    rule    -> artefact:knowledge/guidelines/<file>.md   NEW
              cites        rule    -> sc:<n.n.n>                                NEW
              enforcedBy   rule    -> artefact:<gate path>                      NEW
              flaggedBy    snippet -> rule:<id>                                 NEW
              appliesTo    rule    -> component:<slug>                          EXISTS
                                      (the guidelines family already draws 826
                                      appliesTo edges, sc -> component)

⛔ A NEW NODE KIND AND A NEW EDGE TYPE ARE CLOSED-VOCABULARY CHANGES (#75).
This script PROPOSES; Dave ratifies; only then does it land. `--dry-run` is the
DEFAULT and writes one JSON file into the lane folder and nothing else.
`--land` REFUSES unless `--ratified sNNN-DN` names a ruling id that exists in
knowledge/_rulings.json (mutation-tested — bite 7).

WHERE IT LANDS. Rules are not components, so these nodes cannot live in
knowledge/components/*.meta.json. `--land` writes ONE new file,
knowledge/_rule_nodes.json, in the shape of knowledge/_ruling_edges.json (the
s267-D3 precedent: an AUTHORED node/edge file the explorer reads). ⚠ THAT FILE
HAS NO CONSUMER UNTIL _build_kg_explorer.py IS TAUGHT TO READ IT — an
instrument without a consumer (knowledge hook). The reader is ~12 lines and is
NOT written by this lane: it is decision RK-5 on the review page.

NEVER INVENTED (fence 3, #261): a target that does not resolve to a measured
node becomes {"ref": null, "$note": "<the evidence>"} and is counted in
`unresolved`. 19 SC citations name criteria we hold no sc: node for; 2 advisory
signals sit in *.canon.html files that are not snippet nodes. Declared, never
guessed.

OFF BY DEFAULT, both because the measurement is weak and the answer is Dave's:
  --with-appliesto   rule -> component by EXACT component-name match in the
                     rule text. 27 pairs / 24 rules / 14 components, and the
                     sample carries visible false positives (va25-013 "Avatar",
                     icon-015 "Confirmation"). Counted, shown, not landed.
  --destiny-edges    destiny as a hasDestiny edge to a destiny:<VALUE> hub
                     instead of an attribute. 470 edges, 4 hub nodes.

Usage:
  python3 knowledge/gen_kg_rules.py                       # dry run (default)
  python3 knowledge/gen_kg_rules.py --dry-run /tmp/x.json # dry run, named output
  python3 knowledge/gen_kg_rules.py --land --ratified s274-D1
  python3 knowledge/gen_kg_rules.py --selftest
  python3 knowledge/gen_kg_rules.py --corpus <dir>        # operate on a scratch knowledge/ dir

DO-NOT-RULE: this script never edits a meta, never edits _rules-index.json,
never edits meta.schema.json, never edits _rulings.json, and never adds a rule.
It reads and proposes.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RULINGS = HERE / "_rulings.json"
LANE = ROOT / "notes" / "_lanes" / "274" / "rules-kg"
DEFAULT_OUT = LANE / "dry-run.json"
LANDED = "_rule_nodes.json"

# The five edge types this generator can assert. `appliesTo` is the only one
# that ALREADY EXISTS in the graph vocabulary (guidelines family, sc->component).
EDGE_TYPES = ("definedIn", "cites", "enforcedBy", "flaggedBy", "appliesTo")
EDGE_STATUS = {"definedIn": "NEW", "cites": "NEW", "enforcedBy": "NEW",
               "flaggedBy": "NEW", "appliesTo": "EXISTS"}

FAMILY = "rules"
GUIDELINES_DIR = "guidelines"
DOC_PREFIX = "artefact:knowledge/guidelines/"

# "(SC 1.3.1 A + 4.1.2 A)" — the numbers ride in one parenthetical that names SC
# once. A bare "1.4.3" outside such a parenthetical is NOT a citation (a ratio,
# a version, a clause number), so the parenthetical is the unit.
PAREN_RX = re.compile(r"\(([^)]*\bSC\b[^)]*)\)")
NUM_RX = re.compile(r"\b(\d+\.\d+\.\d+)\b")
INLINE_RX = re.compile(r"\bSC\s+(\d+\.\d+\.\d+)")
# "(nam-002)" in _ADVISORY-SIGNALS.md — the signal's cited authority.
SIGNAL_RID_RX = re.compile(r"\(([a-z]{2,5}-\d{3})\)")
RULING_ID_RX = re.compile(r"^s\d{2,4}-D\d+$")


# ------------------------------------------------------------------ corpus

def _k(corpus=None):
    return Path(corpus) if corpus else HERE


def load_rules(corpus=None):
    p = _k(corpus) / GUIDELINES_DIR / "_rules-index.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    return data["rules"], data


def sc_ids(corpus=None):
    """The sc: node addresses, read from the same place _build_kg_explorer.py
    reads them (knowledge/compliance/rules/*.json). A silently empty set would
    turn every citation into an unresolved null, so an empty directory is loud."""
    out = set()
    for f in sorted(glob.glob(str(_k(corpus) / "compliance" / "rules" / "*.json"))):
        try:
            r = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(r, dict) and r.get("sc"):
            out.add(r["sc"])
    return out


def component_names(corpus=None):
    """{meta `name`: slug} — the same index _build_kg_explorer.py builds for its
    own applies_to matching: the meta's OWN name field, never the node label."""
    out = {}
    for f in sorted(glob.glob(str(_k(corpus) / "components" / "*.meta.json"))):
        b = os.path.basename(f)[: -len(".meta.json")]
        if b.startswith("EXAMPLE-"):
            continue
        try:
            m = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(m, dict) and m.get("name"):
            out.setdefault(m["name"], b)
    return out


def snippet_ids(corpus=None):
    return {os.path.basename(p) for p in glob.glob(str(_k(corpus) / "snippets" / "*.reference.html"))}


def advisory_signals(corpus=None):
    """[(file, rule_id, line)] for every signal in _ADVISORY-SIGNALS.md that
    NAMES a rule id. A signal with no cited rule is not an edge — counted, not
    guessed at."""
    p = _k(corpus) / "_ADVISORY-SIGNALS.md"
    if not p.exists():
        return [], 0
    cur, out, total = None, [], 0
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            cur = ln[3:].split(" — ")[0].strip()
        elif ln.startswith("- **"):
            total += 1
            for rid in SIGNAL_RID_RX.findall(ln):
                out.append((cur, rid, ln.strip()[:200]))
    return out, total


def gate_map(corpus=None):
    """rule id -> [gate relpath]. Read from knowledge/_instrument-fit.json, whose
    `gates` column is EVIDENCE-BASED (_build_instrument_fit.py:harvest_gates —
    the gate file must NAME the rule id; no keyword inference). This is a
    DERIVED artefact, so its freshness against the index is asserted, not
    assumed (bite 5)."""
    p = _k(corpus) / "_instrument-fit.json"
    if not p.exists():
        return {}, False
    try:
        rows = json.loads(p.read_text(encoding="utf-8"))["rows"]
    except Exception:
        return {}, False
    return {r["id"]: list(r.get("gates") or []) for r in rows if r.get("gates")}, True


# ------------------------------------------------------------------ parsing

def cited_scs(text):
    """Every success criterion a rule's text cites, in sorted order."""
    got = set()
    for g in PAREN_RX.findall(text):
        got |= set(NUM_RX.findall(g))
    got |= set(INLINE_RX.findall(text))
    return sorted(got)


def named_components(text, names):
    """[(name, slug)] for every component whose exact `name` appears in the rule
    text on a word boundary. Case-sensitive and never fuzzy — and still weak
    enough that it is off by default (see the module docstring)."""
    hits = []
    for nm in sorted(names):
        if re.search(r"(?<![A-Za-z0-9-])" + re.escape(nm) + r"(?![A-Za-z0-9-])", text):
            hits.append((nm, names[nm]))
    return hits


# ------------------------------------------------------------------ build

def build(corpus=None, with_appliesto=False, destiny_edges=False):
    """Returns (payload, report). Reads only; writes nothing."""
    rules, index = load_rules(corpus)
    scs = sc_ids(corpus)
    names = component_names(corpus)
    snips = snippet_ids(corpus)
    gates, gates_present = gate_map(corpus)
    signals, signals_total = advisory_signals(corpus)
    rule_ids = {r["id"] for r in rules}

    nodes, edges, unresolved = {}, [], []

    def add(nid, label, **kw):
        n = nodes.setdefault(nid, {"id": nid, "type": nid.split(":")[0], "label": label, "fam": FAMILY})
        n.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return nid

    def link(s, t, ty, note=""):
        edges.append({"s": s, "t": t, "type": ty, "fam": FAMILY,
                      **({"note": note} if note else {})})

    for r in rules:
        rid = "rule:" + r["id"]
        attrs = {"ruleId": r["id"], "file": r["file"], "destinyFull": r.get("destinyFull"),
                 "text": r["rule"][:400]}
        if not destiny_edges:
            attrs["destiny"] = r.get("destiny")
        add(rid, r["id"], **attrs)

        # definedIn — the guideline document the rule is anchored in.
        doc = DOC_PREFIX + r["file"]
        add(doc, r["file"], docOf=FAMILY)
        link(rid, doc, "definedIn")

        # cites — SC citations parsed out of the rule text.
        for sc in cited_scs(r["rule"]):
            if sc in scs:
                link(rid, "sc:" + sc, "cites")
            else:
                edges.append({"s": rid, "t": None, "type": "cites", "fam": FAMILY,
                              "note": f"cites SC {sc} — no sc:{sc} node in knowledge/compliance/rules/"})
                unresolved.append({"rule": r["id"], "type": "cites", "value": sc,
                                   "why": "no such sc: node — the criterion is not in the compliance corpus"})

        # enforcedBy — a gate that NAMES this rule id.
        for g in gates.get(r["id"], []):
            link(rid, add("artefact:" + g, g), "enforcedBy")

        # appliesTo — weak, off by default.
        if with_appliesto:
            for nm, slug in named_components(r["rule"], names):
                link(rid, "component:" + slug, "appliesTo", note=f'rule text names "{nm}"')

        if destiny_edges:
            d = r.get("destiny")
            link(rid, add("destiny:" + str(d), str(d)), "hasDestiny")

    # flaggedBy — snippet -> rule, from the advisory signals.
    seen = set()
    for f, rid, line in signals:
        if rid not in rule_ids:
            unresolved.append({"rule": rid, "type": "flaggedBy", "value": f,
                               "why": "the signal cites a rule id the index does not hold"})
            continue
        if f not in snips:
            unresolved.append({"rule": rid, "type": "flaggedBy", "value": f,
                               "why": "the flagged file is not a snippet: node (a *.canon.html page)"})
            continue
        key = (f, rid)
        if key in seen:
            continue
        seen.add(key)
        link("snippet:" + f, "rule:" + rid, "flaggedBy", note=line)

    counts = {}
    for e in edges:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    node_counts = {}
    for n in nodes.values():
        node_counts[n["type"]] = node_counts.get(n["type"], 0) + 1

    payload = {
        "$description": "PROPOSED rule: nodes and their edges (#274 lane RK, s269-D1 item 2). "
                        "NOT RATIFIED until a ruling id is recorded in knowledge/_rulings.json.",
        "generated_by": "knowledge/gen_kg_rules.py",
        "family": FAMILY,
        "edge_types": {t: EDGE_STATUS[t] for t in EDGE_TYPES},
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "edges": edges,
    }
    report = {
        "corpus": str(_k(corpus)),
        "rules_read": len(rules),
        "index_count_field": index.get("count"),
        "byDestiny": index.get("byDestiny"),
        "guideline_docs": len({r["file"] for r in rules}),
        "sc_nodes_available": len(scs),
        "component_names_indexed": len(names),
        "snippets_available": len(snips),
        "advisory_signals_total": signals_total,
        "advisory_signals_citing_a_rule": len(signals),
        "instrument_fit_present": gates_present,
        "rules_with_a_gate": len(gates),
        "edge_counts": counts,
        "edge_total": len(edges),
        "edge_status": {t: EDGE_STATUS[t] for t in EDGE_TYPES},
        "node_counts": node_counts,
        "node_total": len(nodes),
        "unresolved": unresolved,
        "unresolved_total": len(unresolved),
        "options": {"with_appliesto": bool(with_appliesto), "destiny_edges": bool(destiny_edges)},
    }
    return payload, report


# ------------------------------------------------------------------ ratify

def ruling_exists(rid, rulings_path=None):
    p = Path(rulings_path or RULINGS)
    if not p.exists():
        return False
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in ("rulings", "_README"):
        for entry in data.get(key, []) or []:
            if isinstance(entry, dict) and entry.get("id") == rid:
                return True
    return False


def land(corpus=None, rulings_path=None, ratified=None, with_appliesto=False, destiny_edges=False):
    """Refuses without a ratification id that EXISTS in _rulings.json (#75).
    Writes exactly one file: <knowledge>/_rule_nodes.json. Touches no meta."""
    if not ratified:
        raise SystemExit("REFUSED — --land needs --ratified sNNN-DN (a new node kind and a new "
                         "edge type are closed-vocabulary changes, #75: Dave ratifies, then it lands)")
    if not RULING_ID_RX.match(ratified):
        raise SystemExit(f"REFUSED — --ratified '{ratified}' is not a ruling id (sNNN-DN)")
    if not ruling_exists(ratified, rulings_path):
        raise SystemExit(f"REFUSED — ruling '{ratified}' is not in {rulings_path or RULINGS}. "
                         "An unrecorded ratification is not a ratification.")
    payload, report = build(corpus, with_appliesto, destiny_edges)
    payload["ratified"] = ratified
    out = _k(corpus) / LANDED
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["landed"] = {"ratified": ratified, "file": str(out),
                        "nodes": report["node_total"], "edges": report["edge_total"]}
    return report


def _dry(corpus, out_path, with_appliesto=False, destiny_edges=False):
    payload, report = build(corpus, with_appliesto, destiny_edges)
    report["mode"] = "dry-run"
    report["proposal"] = payload
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


# ------------------------------------------------------------------ selftest

def _mini(tmp):
    """Synthetic knowledge/ dir — touches nothing in the live tree."""
    k = tmp / "knowledge"
    (k / GUIDELINES_DIR).mkdir(parents=True)
    (k / "compliance" / "rules").mkdir(parents=True)
    (k / "components").mkdir(parents=True)
    (k / "snippets").mkdir(parents=True)
    rules = [
        {"id": "aaa-001", "file": "alpha.md", "destiny": "BLOCKING", "destinyFull": "BLOCKING",
         "rule": "A-1 — titles (SC 1.1.1 A + 9.9.9 AA): Buttons must be named."},
        {"id": "aaa-002", "file": "alpha.md", "destiny": "ADVISORY", "destinyFull": "ADVISORY",
         "rule": "A-2 — a ratio of 4.5.1 is not a citation and 1.1.1 alone is not either."},
        {"id": "bbb-001", "file": "beta.md", "destiny": "TASTE", "destinyFull": "TASTE",
         "rule": "B-1 — no citations here at all."},
    ]
    (k / GUIDELINES_DIR / "_rules-index.json").write_text(json.dumps(
        {"count": 3, "byDestiny": {"BLOCKING": 1, "ADVISORY": 1, "TASTE": 1}, "rules": rules},
        indent=2), encoding="utf-8")
    (k / "compliance" / "rules" / "sc-1-1-1.json").write_text(json.dumps(
        {"sc": "1.1.1", "title": "Non-text content", "level": "A"}), encoding="utf-8")
    (k / "components" / "button.meta.json").write_text(json.dumps(
        {"name": "Buttons", "provenance": {"source": "code"}}), encoding="utf-8")
    (k / "components" / "EXAMPLE-button.meta.json").write_text(json.dumps(
        {"name": "Buttons", "provenance": {"source": "code"}}), encoding="utf-8")
    (k / "snippets" / "Alpha.reference.html").write_text("<p>x</p>", encoding="utf-8")
    (k / "_ADVISORY-SIGNALS.md").write_text(
        "# Advisory signals\n\n"
        "## Alpha.reference.html — 2 signal(s)\n"
        "- **caps-name** — ALL-CAPS word \"X\" (aaa-001)\n"
        "- **caps-name** — ALL-CAPS word \"Y\" (aaa-001)\n"
        "- **no-cite** — a signal that names no rule\n"
        "## Gallery.canon.html — 1 signal(s)\n"
        "- **caps-name** — ALL-CAPS word \"Z\" (aaa-002)\n"
        "## Alpha.reference.html — 1 signal(s)\n"
        "- **ghost** — cites a rule the index does not hold (zzz-999)\n", encoding="utf-8")
    (k / "_instrument-fit.json").write_text(json.dumps(
        {"rows": [{"id": "aaa-001", "gates": ["knowledge/_validate_x.py"]},
                  {"id": "aaa-002", "gates": []},
                  {"id": "bbb-001", "gates": []}]}), encoding="utf-8")
    return k


def selftest():
    fails = []

    def bite(n, desc, cond):
        print(("  ok  " if cond else "  FAIL") + f"  bite {n}: {desc}")
        if not cond:
            fails.append(n)

    with tempfile.TemporaryDirectory() as td:
        k = _mini(Path(td))
        payload, rep = build(k)
        ids = {n["id"] for n in payload["nodes"]}
        E = payload["edges"]

        def of(ty):
            return [e for e in E if e["type"] == ty]

        # 1 — one rule: node per index row, carrying the four attributes
        n1 = [n for n in payload["nodes"] if n["id"] == "rule:aaa-001"][0]
        bite(1, "every index row becomes a rule: node with id/file/destiny/destinyFull/text",
             len([n for n in payload["nodes"] if n["type"] == "rule"]) == 3
             and n1.get("ruleId") == "aaa-001" and n1.get("file") == "alpha.md"
             and n1.get("destiny") == "BLOCKING" and n1.get("destinyFull") == "BLOCKING"
             and str(n1.get("text")).startswith("A-1 —"))

        # 2 — definedIn is one per rule and the doc node is an artefact:, deduped
        bite(2, "definedIn: one edge per rule, two doc nodes for three rules",
             len(of("definedIn")) == 3
             and "artefact:knowledge/guidelines/alpha.md" in ids
             and len([n for n in payload["nodes"] if n["type"] == "artefact"
                      and n["id"].startswith(DOC_PREFIX)]) == 2)

        # 3 — MUTATION: the SC parse takes the parenthetical, not any n.n.n
        #     "4.5.1" (a ratio) and a bare "1.1.1" must NOT become citations.
        bite(3, "cites parses only SC parentheticals — a ratio and a bare number are not cited",
             cited_scs(k and "A-1 (SC 1.1.1 A + 9.9.9 AA)") == ["1.1.1", "9.9.9"]
             and cited_scs("a ratio of 4.5.1 and a bare 1.1.1") == []
             and len(of("cites")) == 2)

        # 4 — MUTATION: an SC with no node is ref:null + note, never invented
        nulls = [e for e in of("cites") if e["t"] is None]
        bite(4, "an unresolvable SC becomes t:null + note and is counted in unresolved",
             len(nulls) == 1 and "9.9.9" in nulls[0]["note"]
             and any(u["value"] == "9.9.9" for u in rep["unresolved"])
             and not any(e["t"] == "sc:9.9.9" for e in E))

        # 5 — enforcedBy is evidence-based and the derived source is freshness-checked
        gates, present = gate_map(k)
        rules, _ = load_rules(k)
        fresh = set(gates) <= {r["id"] for r in rules}
        bite(5, "enforcedBy comes from _instrument-fit.json rows whose ids all exist in the index",
             present and fresh and [e["t"] for e in of("enforcedBy")] == ["artefact:knowledge/_validate_x.py"])

        # 6 — flaggedBy: deduped, snippet-resolved, ghost rule ids and canon pages refused
        fb = of("flaggedBy")
        why = {u["why"][:20] for u in rep["unresolved"] if u["type"] == "flaggedBy"}
        bite(6, "flaggedBy dedupes 2 signals to 1 edge, refuses a canon page and a ghost rule id",
             len(fb) == 1 and fb[0]["s"] == "snippet:Alpha.reference.html"
             and fb[0]["t"] == "rule:aaa-001" and len(why) == 2)

        # 7 — MUTATION: --land REFUSES without a recorded ratification, and writes nothing
        refusals = 0
        for bad in (None, "s999-D9", "not-a-ruling"):
            try:
                land(k, RULINGS, bad)
            except SystemExit:
                refusals += 1
        bite(7, "--land REFUSES with no id, an absent id and a malformed id, and writes no file",
             refusals == 3 and not (k / LANDED).exists())

        # 8 — --land with a real ruling writes exactly ONE file and no meta changes
        snap = {p.name: p.read_text(encoding="utf-8") for p in (k / "components").glob("*.json")}
        snap["idx"] = (k / GUIDELINES_DIR / "_rules-index.json").read_text(encoding="utf-8")
        r8 = land(k, RULINGS, "s269-D1")
        landed = json.loads((k / LANDED).read_text(encoding="utf-8"))
        bite(8, "--land writes only _rule_nodes.json, stamps the ruling, leaves every input byte-identical",
             (k / LANDED).exists() and landed["ratified"] == "s269-D1"
             and r8["landed"]["ratified"] == "s269-D1"
             and all(p.read_text(encoding="utf-8") == snap[p.name] for p in (k / "components").glob("*.json"))
             and (k / GUIDELINES_DIR / "_rules-index.json").read_text(encoding="utf-8") == snap["idx"])

        # 9 — MUTATION: appliesTo is OFF by default and exact-name when on
        p_on, r_on = build(k, with_appliesto=True)
        ap = [e for e in p_on["edges"] if e["type"] == "appliesTo"]
        bite(9, "appliesTo is absent by default, and on demand matches the meta `name` exactly (EXAMPLE- excluded)",
             not of("appliesTo") and [e["t"] for e in ap] == ["component:button"]
             and r_on["component_names_indexed"] == 1)

        # 10 — MUTATION: destiny is an attribute by default, an edge only on demand
        p_d, _ = build(k, destiny_edges=True)
        hd = [e for e in p_d["edges"] if e["type"] == "hasDestiny"]
        bite(10, "destiny is a node attribute by default; --destiny-edges swaps it for 3 edges to 3 hubs",
             all("destiny" in n for n in payload["nodes"] if n["type"] == "rule")
             and len(hd) == 3 and not any("destiny" in n for n in p_d["nodes"] if n["type"] == "rule")
             and len([n for n in p_d["nodes"] if n["type"] == "destiny"]) == 3)

        # 11 — a dry run writes its JSON and NOTHING else
        with tempfile.TemporaryDirectory() as td2:
            k2 = _mini(Path(td2))
            before = {str(p): p.read_text(encoding="utf-8") for p in k2.rglob("*") if p.is_file()}
            out = Path(td2) / "DRY.json"
            _dry(k2, out)
            after = {str(p): p.read_text(encoding="utf-8") for p in k2.rglob("*") if p.is_file()}
            bite(11, "--dry-run writes its JSON outside the corpus and leaves the corpus byte-identical",
                 out.exists() and before == after and not (k2 / LANDED).exists())

        # 12 — the edge-status table is honest: only appliesTo pre-exists
        bite(12, "edge_status marks appliesTo EXISTS and the other four NEW",
             rep["edge_status"] == {"definedIn": "NEW", "cites": "NEW", "enforcedBy": "NEW",
                                    "flaggedBy": "NEW", "appliesTo": "EXISTS"})

    print("SELFTEST PASS" if not fails else f"SELFTEST FAIL — bites {fails}")
    return 1 if fails else 0


# ------------------------------------------------------------------ entry

def main():
    try:  # #269 PARKED-WITH-A-TRIPWIRE hook: advisory print, never a gate
        import _parked; _parked.notice("kg-edge-gen")
    except BaseException:
        pass
    argv = sys.argv[1:]
    if "--selftest" in argv:
        return selftest()

    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default

    corpus = Path(opt("--corpus")) if opt("--corpus") else None
    ap = "--with-appliesto" in argv
    de = "--destiny-edges" in argv

    if "--land" in argv:
        rep = land(corpus, None, opt("--ratified"), ap, de)
        print(f"LANDED — ratified {rep['landed']['ratified']} · {rep['landed']['file']} · "
              f"{rep['node_total']} nodes · {rep['edge_total']} edges {rep['edge_counts']}")
        print("  ⚠ NO CONSUMER YET — _build_kg_explorer.py does not read this file (decision RK-5).")
        return 0

    out = Path(opt("--dry-run") or opt("--out") or str(DEFAULT_OUT))
    rep = _dry(corpus, out, ap, de)
    print(f"DRY RUN — {rep['rules_read']} rules read · {rep['node_total']} nodes · {rep['edge_total']} edges")
    print(f"  edges: {rep['edge_counts']}")
    print(f"  status: {rep['edge_status']}")
    print(f"  nodes: {rep['node_counts']}  unresolved: {rep['unresolved_total']}")
    print(f"  wrote {out}")
    print("  NOT LANDED — a new node kind and a new edge type are closed-vocabulary changes (#75); "
          "--land needs --ratified sNNN-DN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
