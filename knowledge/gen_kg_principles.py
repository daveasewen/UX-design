#!/usr/bin/env python3
"""gen_kg_principles.py — the UX-PRINCIPLE + POLARITY node/edge generator (#275 lane RP).

Enacts s269-D1 order item 3: put the 145 in-house UX principles
(knowledge/brain/principles.json) and the 30 polarities
(knowledge/brain/polarities.json + _generated/polarity-edges.json) into the
knowledge graph as nodes, with edges to the things that already exist there.

  NODE KINDS  ux:<id>        e.g. ux:pr-fitts                                145
              attributes: the twelve register fields VERBATIM (statement is
              the #236-R1 lane's own words, <=25 words, carried whole and
              never truncated) plus gradeName, read from the s237-D1 map in
              knowledge/_validate_polarities.py (never typed in here).
              `ux:` is the prefix s269-D2 RULED, and it is MEASURED free:
              notes/_KG-EXPLORER.html carries evidence/artefact/ruling/rule/
              pattern/context/component/snippet/session/axe/sc/shape/intent/
              role/guideline/principle/standard/policy and nothing else.
              `principle:` and `guideline:` are WCAG's (s269-D2).

              polarity:<id>  e.g. polarity:pl-01                              30
              attributes: mediatingVariable, statusDerived, r1Id.
              DEFAULT ON, `--no-polarity-nodes` builds the alternative. This
              is decision RP-3 and it is Dave's, not the lane's.

  EDGE TYPES  tensionWith    ux       -> ux                                NEW  22
              hasParty       polarity -> ux | ruling | null                NEW  68
              explainedBy    polarity -> ruling                            NEW   1
              touches        polarity -> ruling                            NEW   9
              resolvedBy     polarity -> ruling                            NEW   7
              challengedBy   polarity -> ruling                            NEW   4
              inFamily       ux       -> family:<id>    (--family-edges)    NEW 145
              evidencedBy    ux       -> evidence:<url> (--evidence-edges) EXISTS

  All six default types are MEASURED absent from the live graph. `evidencedBy`
  is the one that already exists (1,228 edges, governance family) — and 0 of
  the 53 distinct bibliographic URLs in the register match a live evidence:
  node, so reusing the word would make `evidence:` mean two things at once
  (the #202 vocabulary-collision class). Off by default; counted, shown.

  The FOUR typed polarity links are four types because s238-D6 ruled the link
  typed and the generator refusing an untyped one: the typed link IS the
  citation. Collapsing them to one `polarityLink` carrying a `linkType`
  attribute is option (c) on RP-2 and is not taken silently.

⛔ A NEW NODE KIND AND A NEW EDGE TYPE ARE CLOSED-VOCABULARY CHANGES (#75).
This script PROPOSES; Dave ratifies; only then does it land. `--dry-run` is the
DEFAULT and writes one JSON file into the lane folder and nothing else.
`--land` REFUSES unless `--ratified sNNN-DN` names a ruling id that exists in
knowledge/_rulings.json (mutation-tested — bite 10).

WHERE IT LANDS. `--land` writes ONE new file, knowledge/_ux_principle_nodes.json,
in the shape of knowledge/_rule_nodes.json (the s274-D11 precedent: an authored
node/edge file the explorer reads behind its own chip). Whether the explorer
READER lands in the same commit is decision RP-6. This script MEASURES the
answer rather than asserting it: it greps _build_kg_explorer.py for its own
landed filename and prints what it found.

NEVER INVENTED (fence 3, #261): a target that does not resolve to a measured
node becomes {"t": null, "$note": "<the evidence>"} and is counted in
`unresolved`. 15 polarity parties are declared stubs (a phrase, not a register
row — knowledge/brain/stubs.json) and carry the verbatim phrase in the note;
12 polarities produce no tensionWith edge at all and are declared, not dropped.

⛔ NO WCAG JOIN IS DRAWN. 20 principles sit in WCAG-adjacent families
(fam-wcag22 11 · fam-coga 6 · fam-aria-apg 1 · fam-en301549 1 · fam-eaa 1) and
the graph already holds principle:1..4, 38 sc:, 12 guideline:, standard: and
policy: nodes. NO FIELD in principles.json names any of them — measured, all
twelve fields — so the only route is regex on a name, which s274-D12 refused
for 27 rule->component candidates. The count is reported; the edge is not
drawn. That is decision RP-4.

OFF BY DEFAULT:
  --family-edges     family as an inFamily edge to a family:<id> hub instead
                     of an attribute. 145 edges, 32 hubs. GRADE is NOT offered
                     as an edge: s237-D1 already ruled it "a field on every
                     principle node".
  --evidence-edges   ux -> evidence:<url>, 134 edges, 53 new evidence: nodes,
                     0 of which join a live one.
  --no-polarity-nodes  the RP-3 alternative: no polarity: nodes, tensionWith
                     only, and the 21 typed ruling links declared lost.

Usage:
  python3 knowledge/gen_kg_principles.py                        # dry run (default)
  python3 knowledge/gen_kg_principles.py --dry-run /tmp/x.json  # dry run, named output
  python3 knowledge/gen_kg_principles.py --land --ratified s275-D1
  python3 knowledge/gen_kg_principles.py --selftest
  python3 knowledge/gen_kg_principles.py --corpus <dir>         # a scratch knowledge/ dir

DO-NOT-RULE: this script never edits principles.json, polarities.json, any
generated brain artefact, any meta, meta.schema.json, _rulings.json,
_build_kg_explorer.py or _rules-index.json, and never adds a principle. It
reads and proposes.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import itertools
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RULINGS = HERE / "_rulings.json"
LANE = ROOT / "notes" / "_lanes" / "275" / "principles-kg"
DEFAULT_OUT = LANE / "dry-run.json"
LANDED = "_ux_principle_nodes.json"
EXPLORER = HERE / "_build_kg_explorer.py"

FAMILY = "uxprinciples"
UX = "ux:"
POL = "polarity:"

# The four typed polarity out-links (s238-D6) plus the three structural types.
LINK_TYPES = ("explainedBy", "touches", "resolvedBy", "challengedBy")
EDGE_TYPES = ("tensionWith", "hasParty") + LINK_TYPES + ("inFamily", "evidencedBy")
# MEASURED against notes/_KG-EXPLORER.html, not assumed: only evidencedBy pre-exists.
EDGE_STATUS = {t: "NEW" for t in EDGE_TYPES}
EDGE_STATUS["evidencedBy"] = "EXISTS"

RULING_ID_RX = re.compile(r"^s\d{2,4}-D\d+$")
URL_RX = re.compile(r"https?://[^\s)]+")
# s237-D1's grade names live in ONE place. Read them, never retype them.
GRADE_NAMES_RX = re.compile(r"^GRADE_NAMES\s*=\s*(\{[^}]*\})", re.M)
# The five families whose rows restate a standard the graph already carries.
WCAG_ADJACENT = ("fam-wcag22", "fam-coga", "fam-aria-apg", "fam-en301549", "fam-eaa")
# The six A-grade laws s269-D5 names. Measured against the metas; never drawn here.
SIX_LAWS = ("pr-fitts", "pr-hick", "pr-steering", "pr-klm",
            "pr-speed-accuracy", "pr-graphical-perception")
# The twelve register fields, carried verbatim. `id` becomes uxId (the node owns `id`).
FIELDS = ("statement", "family", "originator", "year", "grade", "grade_alt",
          "grade_reason", "evidence", "scope_conditions", "known_misreadings",
          "refutation_probe")


# ------------------------------------------------------------------ corpus

def _k(corpus=None):
    return Path(corpus) if corpus else HERE


def load_principles(corpus=None):
    d = json.loads((_k(corpus) / "brain" / "principles.json").read_text(encoding="utf-8"))
    return d["principles"], d


def load_polarities(corpus=None):
    d = json.loads((_k(corpus) / "brain" / "polarities.json").read_text(encoding="utf-8"))
    return d["polarities"], d


def load_polarity_edges(corpus=None):
    """The DERIVED pairwise view (s238-D1: derived, never authored). Returns
    (edges, header). A missing file is loud, not an empty success."""
    p = _k(corpus) / "brain" / "_generated" / "polarity-edges.json"
    if not p.exists():
        return [], {}
    d = json.loads(p.read_text(encoding="utf-8"))
    return d.get("edges", []), d


def load_status(corpus=None):
    p = _k(corpus) / "brain" / "_generated" / "polarity-status.json"
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {r["id"]: r for r in d.get("rows", []) if isinstance(r, dict) and r.get("id")}


def load_stubs(corpus=None):
    p = _k(corpus) / "brain" / "stubs.json"
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {s["id"]: s.get("phrase", "") for s in d.get("stubs", []) if s.get("id")}


def ruling_ids(corpus=None, rulings_path=None):
    """The ruling: node addresses, read from the same place _build_kg_explorer.py
    reads them. An empty set would turn every typed link into a null, so it is
    asserted non-empty by bite 5 rather than trusted."""
    p = Path(rulings_path) if rulings_path else (_k(corpus) / "_rulings.json")
    if not p.exists():
        return set()
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return set()
    return {r["id"] for r in d.get("rulings", []) if isinstance(r, dict) and r.get("id")}


def grade_names(corpus=None):
    """s237-D1's ladder names, READ from knowledge/_validate_polarities.py's
    GRADE_NAMES constant. Dave named these; the lane does not retype them, and
    if the constant is gone the attribute is omitted rather than guessed."""
    p = _k(corpus) / "_validate_polarities.py"
    if not p.exists():
        return {}, False
    m = GRADE_NAMES_RX.search(p.read_text(encoding="utf-8"))
    if not m:
        return {}, False
    try:
        return json.loads(m.group(1).replace("'", '"')), True
    except Exception:
        return {}, False


def explorer_reads(name=LANDED, path=None):
    """Does _build_kg_explorer.py name our landed file? MEASURED at run time —
    gen_kg_rules.py's hard-coded 'NO CONSUMER YET' line went stale the moment
    explorer v1.11 learned to read _rule_nodes.json."""
    p = Path(path) if path else EXPLORER
    if not p.exists():
        return None
    return name in p.read_text(encoding="utf-8")


# ------------------------------------------------------------------ derivation

def derive_pairs(polarities, principle_ids):
    """Re-derive the pairwise view from polarities.json by the rule printed in
    polarity-edges.json: for each polarity, each unordered pair of parties on
    DIFFERENT sides whose refs BOTH resolve to a principles.json row -> one
    edge. Used to PROVE the generated file is fresh (bite 2), not to replace it."""
    out = set()
    for p in polarities:
        parties = [pa for pa in p.get("parties", []) if pa.get("ref") in principle_ids]
        for a, b in itertools.combinations(parties, 2):
            if a.get("role") != b.get("role"):
                out.add((p["id"], frozenset((a["ref"], b["ref"]))))
    return out


# ------------------------------------------------------------------ build

def build(corpus=None, family_edges=False, evidence_edges=False,
          polarity_nodes=True, rulings_path=None):
    """Returns (payload, report). Reads only; writes nothing."""
    principles, preg = load_principles(corpus)
    polarities, _ = load_polarities(corpus)
    pedges, pheader = load_polarity_edges(corpus)
    status = load_status(corpus)
    stubs = load_stubs(corpus)
    rids = ruling_ids(corpus, rulings_path)
    gnames, gnames_found = grade_names(corpus)

    pids = {p["id"] for p in principles}
    nodes, edges, unresolved = {}, [], []

    def add(nid, label, **kw):
        n = nodes.setdefault(nid, {"id": nid, "type": nid.split(":")[0], "label": label, "fam": FAMILY})
        n.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return nid

    def link(s, t, ty, note="", **kw):
        e = {"s": s, "t": t, "type": ty, "fam": FAMILY}
        e.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        if note:
            e["note"] = note
        edges.append(e)

    def declare(s, ty, why, note=""):
        """A target we cannot resolve: t:null + the evidence, counted. NEVER a guess."""
        edges.append({"s": s, "t": None, "type": ty, "fam": FAMILY, "note": note or why})
        unresolved.append({"source": s, "type": ty, "why": why, "note": note or why})

    # ---- ux: nodes -------------------------------------------------------
    for p in principles:
        attrs = {"uxId": p["id"]}
        for f in FIELDS:
            if f == "family" and family_edges:
                continue                      # the fact moves to the edge, never both
            attrs[f] = p.get(f)
        if gnames_found and p.get("grade") in gnames:
            attrs["gradeName"] = gnames[p["grade"]]
        add(UX + p["id"], p["id"], **attrs)
        if family_edges:
            link(UX + p["id"], add("family:" + str(p["family"]), str(p["family"])), "inFamily")
        if evidence_edges:
            m = URL_RX.search(str(p.get("evidence") or ""))
            if m:
                u = m.group(0).rstrip(").,;")
                link(UX + p["id"], add("evidence:" + u, u), "evidencedBy")
            else:
                declare(UX + p["id"], "evidencedBy",
                        "the evidence field carries no URL (NOT FETCHED / UNPROVEN)",
                        note=str(p.get("evidence"))[:200])

    # ---- tensionWith — the DERIVED pairwise view, read verbatim ----------
    derived = derive_pairs(polarities, pids)
    from_file = {(e["polarity"], frozenset((e["from"], e["to"]))) for e in pedges}
    fresh = derived == from_file
    for e in pedges:
        if e["from"] not in pids or e["to"] not in pids:
            declare(UX + str(e["from"]), "tensionWith",
                    "an endpoint of the generated pair is not a principles.json row",
                    note=f"{e['polarity']}: {e['from']} -> {e['to']}")
            continue
        link(UX + e["from"], UX + e["to"], "tensionWith",
             polarity=e["polarity"], mediatingVariable=e.get("mediating_variable"),
             fromKind=e.get("from_kind"), toKind=e.get("to_kind"))

    # ---- polarity: nodes, their parties and their typed ruling links -----
    with_edges = {e["polarity"] for e in pedges}
    for p in polarities:
        pid = POL + p["id"]
        if polarity_nodes:
            st = status.get(p["id"], {})
            add(pid, p["id"], polarityId=p["id"],
                mediatingVariable=p.get("mediating_variable"),
                statusDerived=st.get("status_derived"), r1Id=st.get("r1_id"),
                partyCount=len(p.get("parties") or []))
        if p["id"] not in with_edges:
            unresolved.append({
                "source": pid, "type": "tensionWith",
                "why": "no pair of parties on different sides both resolve to a register row "
                       "(237-T finding 3) — the polarity is declared, never dropped",
                "note": "; ".join(f"{pa.get('role')}={pa.get('ref')}" for pa in p.get("parties") or [])})

        for pa in p.get("parties") or []:
            ref, note = pa.get("ref"), (pa.get("note") or "")
            tag = f"{pa.get('role')} — {note}".strip(" —")
            if not polarity_nodes:
                continue
            if ref in pids:
                link(pid, UX + ref, "hasParty", note=tag, role=pa.get("role"))
            elif ref in rids:
                link(pid, "ruling:" + ref, "hasParty", note=tag, role=pa.get("role"))
            elif ref in stubs:
                declare(pid, "hasParty",
                        "the party is a DECLARED STUB — a phrase, not a register row (s238-D1)",
                        note=f'{ref}: "{stubs[ref]}"')
            else:
                declare(pid, "hasParty",
                        "the party ref resolves to no principle, ruling or declared stub",
                        note=f"{ref} ({pa.get('role')})")

        for l in p.get("links") or []:
            ty, ref = l.get("type"), l.get("ref")
            if ty not in LINK_TYPES:          # s238-D6: the generator refuses an untyped link
                unresolved.append({"source": pid, "type": str(ty), "why":
                                   "link type is not one of the four s238-D6 types — refused",
                                   "note": json.dumps(l, ensure_ascii=False)[:200]})
                continue
            if not polarity_nodes:
                unresolved.append({"source": pid, "type": ty, "why":
                                   "--no-polarity-nodes: the link has no source node, so it is LOST",
                                   "note": f"{ty} -> {ref}"})
                continue
            if ref in rids:
                link(pid, "ruling:" + ref, ty, note=(l.get("quote") or "")[:300])
            else:
                declare(pid, ty, "the link names a ruling id _rulings.json does not hold",
                        note=f"{ty} -> {ref}")

    # ---- what we deliberately did NOT draw --------------------------------
    wcag = [p["id"] for p in principles if p.get("family") in WCAG_ADJACENT]
    named = [p["id"] for p in principles
             if any(w in p["id"] for w in ("perceivable", "operable", "understandable", "robust"))]

    counts, node_counts = {}, {}
    for e in edges:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    for n in nodes.values():
        node_counts[n["type"]] = node_counts.get(n["type"], 0) + 1

    payload = {
        "$description": "PROPOSED ux: principle nodes, polarity: nodes and their edges "
                        "(#275 lane RP, s269-D1 item 3). NOT RATIFIED until a ruling id is "
                        "recorded in knowledge/_rulings.json.",
        "generated_by": "knowledge/gen_kg_principles.py",
        "family": FAMILY,
        "edge_types": {t: EDGE_STATUS[t] for t in EDGE_TYPES},
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "edges": edges,
    }
    report = {
        "corpus": str(_k(corpus)),
        "principles_read": len(principles),
        "register_lane": preg.get("lane"),
        "grade_split": {g: sum(1 for p in principles if p.get("grade") == g)
                        for g in sorted({p.get("grade") for p in principles})},
        "grade_names_found": gnames_found,
        "families": len({p.get("family") for p in principles}),
        "polarities_read": len(polarities),
        "polarity_edges_in_file": len(pedges),
        "polarity_edges_header_counts": pheader.get("counts"),
        "pairwise_view_is_fresh": fresh,
        "pairwise_rederived": len(derived),
        "polarities_without_edges": sorted(p["id"] for p in polarities if p["id"] not in with_edges),
        "parties_total": sum(len(p.get("parties") or []) for p in polarities),
        "links_total": sum(len(p.get("links") or []) for p in polarities),
        "link_types": {t: sum(1 for p in polarities for l in (p.get("links") or [])
                              if l.get("type") == t) for t in LINK_TYPES},
        "rulings_available": len(rids),
        "stubs_available": len(stubs),
        "wcag_adjacent_principles": len(wcag),
        "wcag_adjacent_by_family": {f: sum(1 for p in principles if p.get("family") == f)
                                    for f in WCAG_ADJACENT},
        "wcag_name_matches_not_drawn": len(named),
        "six_laws": list(SIX_LAWS),
        "edge_counts": counts,
        "edge_total": len(edges),
        "edge_status": {t: EDGE_STATUS[t] for t in EDGE_TYPES},
        "node_counts": node_counts,
        "node_total": len(nodes),
        "unresolved": unresolved,
        "unresolved_total": len(unresolved),
        "explorer_reads_landed_file": explorer_reads(),
        "options": {"family_edges": bool(family_edges), "evidence_edges": bool(evidence_edges),
                    "polarity_nodes": bool(polarity_nodes)},
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


def land(corpus=None, rulings_path=None, ratified=None, family_edges=False,
         evidence_edges=False, polarity_nodes=True):
    """Refuses without a ratification id that EXISTS in _rulings.json (#75).
    Writes exactly one file: <knowledge>/_ux_principle_nodes.json."""
    if not ratified:
        raise SystemExit("REFUSED — --land needs --ratified sNNN-DN (a new node kind and a new "
                         "edge type are closed-vocabulary changes, #75: Dave ratifies, then it lands)")
    if not RULING_ID_RX.match(ratified):
        raise SystemExit(f"REFUSED — --ratified '{ratified}' is not a ruling id (sNNN-DN)")
    if not ruling_exists(ratified, rulings_path):
        raise SystemExit(f"REFUSED — ruling '{ratified}' is not in {rulings_path or RULINGS}. "
                         "An unrecorded ratification is not a ratification.")
    payload, report = build(corpus, family_edges, evidence_edges, polarity_nodes, rulings_path)
    payload["ratified"] = ratified
    # #275 fence (commit ef1213b): a LANDED file must NAME its ruling and must not
    # carry the dry run's "PROPOSED ... NOT RATIFIED" text.
    payload["$description"] = (f"RATIFIED ux: principle nodes, polarity: nodes and their edges "
                               f"under {ratified} (#275 lane RP; s269-D1 item 3, s269-D2 the "
                               f"prefix). Regenerate with `gen_kg_principles.py --land "
                               f"--ratified {ratified}`; never hand-edit.")
    out = _k(corpus) / LANDED
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["landed"] = {"ratified": ratified, "file": str(out),
                        "nodes": report["node_total"], "edges": report["edge_total"]}
    return report


def _dry(corpus, out_path, family_edges=False, evidence_edges=False, polarity_nodes=True):
    payload, report = build(corpus, family_edges, evidence_edges, polarity_nodes)
    report["mode"] = "dry-run"
    report["proposal"] = payload
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


# ------------------------------------------------------------------ selftest

def _mini(tmp):
    """Synthetic knowledge/ dir — touches nothing in the live tree.

    pr-a / pr-b are a real pair; pr-l is an obligation (grade L); st-x is a
    declared stub; s269-D1 is a live ruling and s999-D9 is not. pl-03 is the
    237-T finding 4 shape — two principles on the SAME side, which must derive
    NO edge; without it a generator that ignored the rule would look correct.
    Statements are deliberately LONG so that any truncation is visible."""
    k = tmp / "knowledge"
    (k / "brain" / "_generated").mkdir(parents=True)
    P = [
        {"id": "pr-a", "statement": "A" * 500, "family": "fam-one", "originator": "X", "year": 1954,
         "grade": "A", "grade_alt": None, "grade_reason": None, "evidence": "Ev A — https://ex.test/a (fetched)",
         "scope_conditions": "sc-a", "known_misreadings": "km-a", "refutation_probe": "rp-a"},
        {"id": "pr-b", "statement": "B" * 500, "family": "fam-two", "originator": "Y", "year": 1994,
         "grade": "C", "grade_alt": "B", "grade_reason": "why", "evidence": "NOT FETCHED",
         "scope_conditions": "sc-b", "known_misreadings": "km-b", "refutation_probe": "rp-b"},
        {"id": "pr-l", "statement": "L" * 500, "family": "fam-wcag22", "originator": "W3C", "year": 2023,
         "grade": "L", "grade_alt": None, "grade_reason": None, "evidence": "https://ex.test/l (fetched)",
         "scope_conditions": "sc-l", "known_misreadings": "km-l", "refutation_probe": "rp-l"},
        {"id": "pr-wcag-perceivable", "statement": "P" * 500, "family": "fam-wcag22", "originator": "W3C",
         "year": 2023, "grade": "L", "grade_alt": None, "grade_reason": None,
         "evidence": "https://ex.test/p (fetched)", "scope_conditions": "sc-p",
         "known_misreadings": "km-p", "refutation_probe": "rp-p"},
    ]
    (k / "brain" / "principles.json").write_text(json.dumps(
        {"$description": "mini", "lane": "test", "principles": P}, indent=2), encoding="utf-8")
    POLS = [
        {"id": "pl-01",
         "parties": [{"ref": "pr-a", "role": "side_a", "note": "one"},
                     {"ref": "pr-b", "role": "side_b", "note": "two"},
                     {"ref": "st-x", "role": "side_b", "note": None},
                     {"ref": "s269-D1", "role": "side_b", "note": "a ruling party"}],
         "mediating_variable": "MV-1",
         "links": [{"type": "explainedBy", "ref": "s269-D1", "quote": "q"},
                   {"type": "resolvedBy", "ref": "s999-D9", "quote": "ghost"},
                   {"type": "invented", "ref": "s269-D1"}],
         "sources": [{"path": "x", "id": "tn-01"}]},
        {"id": "pl-02",
         "parties": [{"ref": "pr-a", "role": "side_a"}, {"ref": "st-x", "role": "side_b"}],
         "mediating_variable": "MV-2", "links": [], "sources": [{"path": "x", "id": "tn-02"}]},
        {"id": "pl-03",      # 237-T finding 4: two principles on ONE side derive NO edge
         "parties": [{"ref": "pr-a", "role": "side_b"}, {"ref": "pr-b", "role": "side_b"}],
         "mediating_variable": "MV-3", "links": [], "sources": [{"path": "x", "id": "tn-03"}]},
    ]
    (k / "brain" / "polarities.json").write_text(json.dumps(
        {"$description": "mini", "$migration": {}, "polarities": POLS}, indent=2), encoding="utf-8")
    (k / "brain" / "_generated" / "polarity-edges.json").write_text(json.dumps(
        {"$header": "GENERATED", "rule": "see the live file", "counts": {"edges": 1},
         "edges": [{"polarity": "pl-01", "from": "pr-a", "to": "pr-b",
                    "from_kind": "principle", "to_kind": "principle",
                    "mediating_variable": "MV-1"}]}, indent=2), encoding="utf-8")
    (k / "brain" / "_generated" / "polarity-status.json").write_text(json.dumps(
        {"rows": [{"id": "pl-01", "r1_id": "tn-01", "status_derived": "resolved", "parties": []},
                  {"id": "pl-02", "r1_id": "tn-02", "status_derived": "open", "parties": []},
                  {"id": "pl-03", "r1_id": "tn-03", "status_derived": "open", "parties": []}]},
        indent=2), encoding="utf-8")
    (k / "brain" / "stubs.json").write_text(json.dumps(
        {"stubs": [{"id": "st-x", "phrase": "a phrase, not a row"}]}, indent=2), encoding="utf-8")
    (k / "_validate_polarities.py").write_text(
        'GRADE_NAMES = {"A": "REPLICATED", "B": "STUDIED", "C": "PRACTISED", '
        '"D": "DEBUNKED", "L": "OBLIGATION"}\n', encoding="utf-8")
    return k


def selftest():
    fails = []

    def bite(n, desc, cond):
        print(("  ok  " if cond else "  FAIL") + f"  bite {n}: {desc}")
        if not cond:
            fails.append(n)

    with tempfile.TemporaryDirectory() as td:
        k = _mini(Path(td))
        payload, rep = build(k, rulings_path=RULINGS)
        ids = {n["id"] for n in payload["nodes"]}
        E = payload["edges"]

        def of(ty):
            return [e for e in E if e["type"] == ty]

        # 1 — every register row becomes a ux: node carrying the twelve fields VERBATIM.
        #     Equality is against the SOURCE ROW read back off disk, so any truncation
        #     or rename is caught whatever the field's length (M1).
        src = {p["id"]: p for p in json.loads(
            (k / "brain" / "principles.json").read_text(encoding="utf-8"))["principles"]}
        a = [n for n in payload["nodes"] if n["id"] == "ux:pr-a"][0]
        b = [n for n in payload["nodes"] if n["id"] == "ux:pr-b"][0]
        bite(1, "every register row becomes a ux: node whose twelve fields equal the source row byte for byte",
             len([n for n in payload["nodes"] if n["type"] == "ux"]) == 4
             and a.get("uxId") == "pr-a"
             and all(n.get(f) == src[n["uxId"]].get(f)
                     for n in payload["nodes"] if n["type"] == "ux" for f in FIELDS
                     if src[n["uxId"]].get(f) is not None)
             and a.get("statement") == src["pr-a"]["statement"] and len(a.get("statement") or "") == 500
             and a.get("family") == "fam-one" and a.get("year") == 1954 and a.get("grade") == "A"
             and b.get("grade_alt") == "B" and b.get("grade_reason") == "why")

        # 2 — MUTATION: the pairwise view is READ, and PROVED fresh by re-derivation.
        #     pl-03 is the 237-T finding 4 shape: two principles on the SAME side. A
        #     derivation that ignored the different-sides rule would invent that pair,
        #     the re-derivation would stop agreeing with the file, and this goes RED (M2).
        bite(2, "tensionWith is read from polarity-edges.json, and re-derivation (same-side pairs refused) agrees",
             rep["pairwise_view_is_fresh"] is True and rep["pairwise_rederived"] == 1
             and len(of("tensionWith")) == 1
             and of("tensionWith")[0]["s"] == "ux:pr-a" and of("tensionWith")[0]["t"] == "ux:pr-b"
             and derive_pairs(json.loads((k / "brain" / "polarities.json").read_text())["polarities"],
                              {"pr-a"}) == set())

        # 3 — the tensionWith edge CARRIES the polarity and its mediating variable
        t = of("tensionWith")[0]
        bite(3, "tensionWith carries polarity id + mediatingVariable + fromKind/toKind as edge attributes",
             t.get("polarity") == "pl-01" and t.get("mediatingVariable") == "MV-1"
             and t.get("fromKind") == "principle" and t.get("toKind") == "principle")

        # 4 — MUTATION: the four s238-D6 types are four DISTINCT edge types; an untyped link is refused
        bite(4, "the typed links become four distinct edge types and a 5th, untyped, link is REFUSED",
             len(of("explainedBy")) == 1 and of("explainedBy")[0]["t"] == "ruling:s269-D1"
             and not of("invented")
             and any(u["type"] == "invented" and "s238-D6" in u["why"] for u in rep["unresolved"]))

        # 5 — MUTATION: a link naming a ruling we do not hold is t:null + note, never invented
        gh = [e for e in of("resolvedBy") if e["t"] is None]
        bite(5, "a link to an unheld ruling becomes t:null + note, counted, and no ruling: node is invented",
             len(rep["rulings_available"] and gh) == 1 and "s999-D9" in gh[0]["note"]
             and "ruling:s999-D9" not in ids and rep["rulings_available"] > 0
             and any("s999-D9" in u["note"] for u in rep["unresolved"]))

        # 6 — hasParty resolves three ways: ux, ruling, and a DECLARED STUB as t:null + the phrase
        hp = of("hasParty")
        stub = [e for e in hp if e["t"] is None]
        bite(6, "hasParty resolves to ux: and ruling:, and a declared stub is t:null carrying the phrase verbatim",
             sorted({e["t"] for e in hp if e["t"]}) == ["ruling:s269-D1", "ux:pr-a", "ux:pr-b"]
             and len(stub) == 2 and all('"a phrase, not a row"' in e["note"] for e in stub)
             and not any(i.startswith("stub:") for i in ids))

        # 7 — an edgeless polarity is DECLARED, not dropped, and still gets its node
        bite(7, "a polarity with no derivable pair is declared in unresolved and still becomes a node",
             rep["polarities_without_edges"] == ["pl-02", "pl-03"]
             and {"polarity:pl-02", "polarity:pl-03"} <= ids
             and len([u for u in rep["unresolved"] if u["type"] == "tensionWith"]) == 2
             and any(u["source"] == "polarity:pl-03" and u["type"] == "tensionWith"
                     for u in rep["unresolved"]))

        # 8 — MUTATION: --no-polarity-nodes drops the nodes AND declares the 21 links LOST
        p_np, r_np = build(k, polarity_nodes=False, rulings_path=RULINGS)
        bite(8, "--no-polarity-nodes removes polarity: nodes and every edge sourced at one, and declares the loss",
             not any(n["id"].startswith(POL) for n in p_np["nodes"])
             and not [e for e in p_np["edges"] if str(e["s"]).startswith(POL)]
             and len([e for e in p_np["edges"] if e["type"] == "tensionWith"]) == 1
             and any("LOST" in u["why"] for u in r_np["unresolved"]))

        # 9 — MUTATION: family is an attribute by default; --family-edges swaps it. Grade NEVER moves (s237-D1)
        p_f, _ = build(k, family_edges=True, rulings_path=RULINGS)
        inf = [e for e in p_f["edges"] if e["type"] == "inFamily"]
        bite(9, "family is an attribute by default, an inFamily edge only on demand; grade stays a field (s237-D1)",
             all("family" in n for n in payload["nodes"] if n["type"] == "ux")
             and not of("inFamily") and len(inf) == 4
             and len([n for n in p_f["nodes"] if n["type"] == "family"]) == 3
             and not any("family" in n for n in p_f["nodes"] if n["type"] == "ux")
             and all(n.get("grade") for n in p_f["nodes"] if n["type"] == "ux")
             and not [e for e in p_f["edges"] if e["type"] == "hasGrade"])

        # 10 — MUTATION: --land REFUSES without a recorded ratification, and writes nothing
        refusals = 0
        for bad in (None, "s999-D9", "not-a-ruling"):
            try:
                land(k, RULINGS, bad)
            except SystemExit:
                refusals += 1
        bite(10, "--land REFUSES with no id, an absent id and a malformed id, and writes no file",
             refusals == 3 and not (k / LANDED).exists())

        # 11 — --land writes ONE file, NAMES the ruling, drops the PROPOSED text, changes no input
        snap = {str(p): p.read_text(encoding="utf-8") for p in k.rglob("*") if p.is_file()}
        r11 = land(k, RULINGS, "s269-D1")
        landed = json.loads((k / LANDED).read_text(encoding="utf-8"))
        after = {str(p): p.read_text(encoding="utf-8") for p in k.rglob("*")
                 if p.is_file() and p.name != LANDED}
        bite(11, "--land writes only the landed file, NAMES the ruling in $description, leaves inputs byte-identical",
             landed["ratified"] == "s269-D1" and r11["landed"]["ratified"] == "s269-D1"
             and "s269-D1" in landed["$description"]
             and "PROPOSED" not in landed["$description"] and "NOT RATIFIED" not in landed["$description"]
             and after == snap)

        # 12 — a dry run writes its JSON and NOTHING else
        with tempfile.TemporaryDirectory() as td2:
            k2 = _mini(Path(td2))
            before = {str(p): p.read_text(encoding="utf-8") for p in k2.rglob("*") if p.is_file()}
            out = Path(td2) / "DRY.json"
            _dry(k2, out)
            now = {str(p): p.read_text(encoding="utf-8") for p in k2.rglob("*") if p.is_file()}
            bite(12, "--dry-run writes its JSON outside the corpus and leaves the corpus byte-identical",
                 out.exists() and before == now and not (k2 / LANDED).exists())

        # 13 — the edge-status table is honest: only evidencedBy pre-exists
        bite(13, "edge_status marks evidencedBy EXISTS and the other seven NEW",
             rep["edge_status"]["evidencedBy"] == "EXISTS"
             and sorted(t for t, s in rep["edge_status"].items() if s == "NEW")
             == ["challengedBy", "explainedBy", "hasParty", "inFamily", "resolvedBy",
                 "tensionWith", "touches"])

        # 14 — MUTATION: NO WCAG join is drawn, not even for the row whose id NAMES a live
        #      principle: node. s274-D12 refused 27 regex candidates; this refuses 1 of 1.
        bite(14, "no edge targets principle:/sc:/guideline:/standard:/policy: — the WCAG join is not drawn",
             rep["wcag_adjacent_principles"] == 2 and rep["wcag_name_matches_not_drawn"] == 1
             and "ux:pr-wcag-perceivable" in ids
             and not [e for e in E if str(e.get("t") or "").split(":")[0]
                      in ("principle", "sc", "guideline", "standard", "policy")])

        # 15 — grade names are READ from the s237-D1 constant, never retyped, and absent if it is
        (k / "_validate_polarities.py").write_text("# no constant here\n", encoding="utf-8")
        p_ng, r_ng = build(k, rulings_path=RULINGS)
        bite(15, "gradeName is read from _validate_polarities.py's s237-D1 map and omitted when it is gone",
             rep["grade_names_found"] is True
             and [n for n in payload["nodes"] if n["id"] == "ux:pr-a"][0]["gradeName"] == "REPLICATED"
             and r_ng["grade_names_found"] is False
             and not any("gradeName" in n for n in p_ng["nodes"] if n["type"] == "ux"))

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
    fe = "--family-edges" in argv
    ee = "--evidence-edges" in argv
    pn = "--no-polarity-nodes" not in argv

    if "--land" in argv:
        rep = land(corpus, None, opt("--ratified"), fe, ee, pn)
        print(f"LANDED — ratified {rep['landed']['ratified']} · {rep['landed']['file']} · "
              f"{rep['node_total']} nodes · {rep['edge_total']} edges {rep['edge_counts']}")
        reads = rep["explorer_reads_landed_file"]
        print(f"  consumer: _build_kg_explorer.py names {LANDED}? "
              f"{'YES' if reads else 'NO — an instrument without a consumer (decision RP-6)'}"
              f"{' (measured at run time)' if reads is not None else ' — explorer not found'}")
        return 0

    out = Path(opt("--dry-run") or opt("--out") or str(DEFAULT_OUT))
    rep = _dry(corpus, out, fe, ee, pn)
    print(f"DRY RUN — {rep['principles_read']} principles · {rep['polarities_read']} polarities · "
          f"{rep['node_total']} nodes · {rep['edge_total']} edges")
    print(f"  edges: {rep['edge_counts']}")
    print(f"  status: {rep['edge_status']}")
    print(f"  nodes: {rep['node_counts']}  unresolved: {rep['unresolved_total']}")
    print(f"  pairwise view fresh (re-derived from polarities.json): {rep['pairwise_view_is_fresh']}")
    print(f"  explorer reads {LANDED}: {rep['explorer_reads_landed_file']}")
    print(f"  wrote {out}")
    print("  NOT LANDED — a new node kind and a new edge type are closed-vocabulary changes (#75); "
          "--land needs --ratified sNNN-DN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
