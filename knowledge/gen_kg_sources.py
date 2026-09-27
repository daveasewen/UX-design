#!/usr/bin/env python3
"""gen_kg_sources.py — the graph's step 5: where a part is SET, where its BEHAVIOUR comes from, where its
geometry was CAPTURED, and what its slots ACCEPT (#305, the sitting's call 25; s269-D1 item 5).

s269-D1 ordered the KG-gap proposal's steps 1-5 and said "each step still PROPOSES its schema diff and
Dave ratifies it, because a new edge type is a vocabulary change (#75)". Steps 1-4 each had their
ratification; step 5 had none until the sitting of 27 September 2026, call 25, Dave: "yes" — on the
recommendation "yes to the four edge types; lifecycle status as a field, not a kind; content standard
parked" (notes/_SITTING-304-tuesday-2026-09-29-v1.html). The proposal's rows
(_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html) are the spec:

  EDGE TYPE          FROM → TO                                    READ FROM (the meta, nothing else)
  setIn              component → typestyle:<class>                every `.t-cm-*` / `.t-ed-*` / `.t-hp-*` class the
                                                                  meta names, resolved against the composites
                                                                  canon/type.css defines (`refs` = times named)
  behaviourFrom      component → file:<path> | snippet:<file>     behaviour.script + behaviour.partial (a partial
                                                                  name resolves to knowledge/canon/<name>.js; a
                                                                  `<snippet>#script` is the snippet's own script,
                                                                  `inline: true`)
  capturedFrom       component → figma:<file:node> | snippet: |   provenance.figma_node and provenance.code_path
                     file:<path>
  acceptsCapability  component → capability:<name>                slots.<slot>.accepts.capability (`slots` names them)

  NODE KINDS (new, family `sources`): typestyle:<class> (attribute `file`), file:<repo path> (a repo file
  that is not a snippet), figma:<fileKey:node>, capability:<name> (minted from the metas' own accepts
  values: no capability registry exists, and s140-D2 made the metas the home of a slot's contract).
  `snippet:` targets are the base graph's own nodes, never restated.

NEVER INVENTED: a class no composite defines, a partial with no file, or a code path that does not
exist gets no edge and no node; it is COUNTED in `$unresolved` with examples.
NOT HERE: lifecycle status (a FIELD on variants since #263, s263-D12 — no node kind), content standard
(parked: ours is prose, no source to map), providesCapability (no source: only the accepts half exists).

MODES
  (default)                   compute and print the counts; writes nothing
  --land --ratified sNNN-DN   write knowledge/_source_nodes.json; REFUSES unless the id is in _rulings.json
  --check                     recompute and compare with the landed file (content, not mtime); rc 1 on drift
  --selftest                  mutation bites
"""
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_NAME = "_source_nodes.json"
FAMILY = "sources"
EDGE_TYPES = ("setIn", "behaviourFrom", "capturedFrom", "acceptsCapability")
RULING_ID_RX = re.compile(r"^s\d{2,3}-D\d{1,3}$")
CLASS_RX = re.compile(r"\.(t-(?:cm|ed|hp)-[a-z0-9-]+)")
TYPE_CSS = os.path.join("canon", "type.css")


def _metas(root):
    for f in sorted(glob.glob(os.path.join(root, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith("EXAMPLE-"):
            continue
        try:
            raw = open(f, encoding="utf-8").read(); m = json.loads(raw)
        except Exception:
            continue
        if isinstance(m, dict):
            yield slug, raw, m


def _as_list(v):
    return v if isinstance(v, list) else ([v] if v else [])


def compute(root=HERE):
    repo = os.path.dirname(root)
    css = open(os.path.join(root, TYPE_CSS), encoding="utf-8").read()
    defined = lambda cls: re.search(r"\." + re.escape(cls) + r"(?![a-z0-9-])", css) is not None
    nodes, edges, unresolved = {}, [], {"setIn": {}, "behaviourFrom": {}, "capturedFrom": {}}
    per_type_metas = {t: set() for t in EDGE_TYPES}

    def node(nid, label, **kw):
        if nid.startswith("snippet:"):
            return nid                                               # the base graph's own node — never restated
        n = nodes.setdefault(nid, {"id": nid, "type": nid.split(":", 1)[0], "label": label, "fam": FAMILY})
        n.update({k: v for k, v in kw.items() if v is not None})
        return nid

    def miss(t, key, slug):
        unresolved[t].setdefault(key, set()).add(slug)

    def file_target(path):
        p = path.split("#", 1)[0].strip()
        if not p or not os.path.exists(os.path.join(repo, p)):
            return None
        if p.startswith("knowledge/snippets/") and p.endswith(".reference.html"):
            return "snippet:" + os.path.basename(p)
        return node("file:" + p, os.path.basename(p), path=p)

    for slug, raw, m in _metas(root):
        cid = "component:" + slug
        # setIn — the type composites the meta names
        counts = {}
        for cls in CLASS_RX.findall(raw):
            counts[cls] = counts.get(cls, 0) + 1
        for cls in sorted(counts):
            if not defined(cls):
                miss("setIn", cls, slug); continue
            edges.append({"s": cid, "t": node("typestyle:" + cls, "." + cls, file="knowledge/" + TYPE_CSS),
                          "type": "setIn", "fam": FAMILY, "refs": counts[cls]})
            per_type_metas["setIn"].add(slug)
        # behaviourFrom — the script and the partials
        b = m.get("behaviour") if isinstance(m.get("behaviour"), dict) else {}
        tgt = {}
        for sp in _as_list(b.get("script")):
            t = file_target(str(sp))
            if t is None:
                miss("behaviourFrom", str(sp), slug); continue
            tgt.setdefault(t, set()).add("script")
            if "#" in str(sp):
                tgt[t].add("inline")
        for pn in _as_list(b.get("partial")):
            t = file_target("knowledge/canon/%s.js" % pn)
            if t is None:
                miss("behaviourFrom", str(pn), slug); continue
            tgt.setdefault(t, set()).add("partial")
        for t in sorted(tgt):
            e = {"s": cid, "t": t, "type": "behaviourFrom", "fam": FAMILY, "via": sorted(tgt[t] - {"inline"})}
            if "inline" in tgt[t]:
                e["inline"] = True
            edges.append(e); per_type_metas["behaviourFrom"].add(slug)
        # capturedFrom — the Figma node and the code path
        p = m.get("provenance") if isinstance(m.get("provenance"), dict) else {}
        cap = []
        for fnode in _as_list(p.get("figma_node")):
            fnode = str(fnode).strip()
            if fnode:
                cap.append((node("figma:" + fnode, fnode), "figma_node"))
        for cp in [x.strip() for v in _as_list(p.get("code_path")) for x in str(v).split(",")]:   # one string may list several
            t = file_target(cp)
            if t is None:
                miss("capturedFrom", cp, slug); continue
            cap.append((t, "code_path"))
        for t, via in cap:
            edges.append({"s": cid, "t": t, "type": "capturedFrom", "fam": FAMILY, "via": via})
            per_type_metas["capturedFrom"].add(slug)
        # acceptsCapability — what each slot legally takes
        slots = m.get("slots")
        items = slots.items() if isinstance(slots, dict) else ((str(i), s) for i, s in enumerate(slots or []))
        acc = {}
        for sname, sd in items:
            if not isinstance(sd, dict) or not isinstance(sd.get("accepts"), dict):
                continue
            for c in _as_list(sd["accepts"].get("capability")):
                acc.setdefault(str(c), set()).add(sd.get("name", sname) if isinstance(slots, list) else sname)
        for c in sorted(acc):
            edges.append({"s": cid, "t": node("capability:" + c, c), "type": "acceptsCapability", "fam": FAMILY,
                          "slots": sorted(acc[c])})
            per_type_metas["acceptsCapability"].add(slug)

    nlist = [nodes[k] for k in sorted(nodes)]
    by_kind = {}
    for n in nlist:
        by_kind[n["type"]] = by_kind.get(n["type"], 0) + 1
    doc = {
        "$description": None,   # set by land()
        "family": FAMILY,
        "$ruled": {"s269-D1": "item 5, the edge types setIn / behaviourFrom / capturedFrom / acceptsCapability, each step PROPOSES its schema diff and Dave ratifies it",
                   "call 25 of the sitting (2026-09-27)": "Dave: \"yes\" — yes to the four edge types; lifecycle status as a field, not a kind; content standard parked"},
        "$measured": {"nodes": len(nlist), "nodesByKind": by_kind, "edges": len(edges),
                      "edgesByType": {t: sum(1 for e in edges if e["type"] == t) for t in EDGE_TYPES},
                      "metasByType": {t: len(per_type_metas[t]) for t in EDGE_TYPES}},
        "$unresolved": {"$what": "names in a meta that resolve to nothing that exists — no node, no edge, counted (never invented)",
                        **{t: {"count": len(v), "examples": {k: sorted(s)[:3] for k, s in sorted(v.items())[:8]}}
                           for t, v in unresolved.items()}},
        "nodes": nlist, "edges": edges}
    return doc


def ruling_exists(rid, root=HERE):
    try:
        d = json.load(open(os.path.join(root, "_rulings.json"), encoding="utf-8"))
    except Exception:
        return False
    return any(isinstance(r, dict) and r.get("id") == rid for r in d.get("rulings", []))


def describe(ratified):
    return ("RATIFIED _source_nodes.json under %s (#305, the sitting's call 25; s269-D1 item 5). typestyle: / file: / "
            "figma: / capability: nodes and the setIn / behaviourFrom / capturedFrom / acceptsCapability edges, all "
            "STRUCTURAL, read from the metas (no sentence authored). Regenerate with `python3 knowledge/gen_kg_sources.py "
            "--land --ratified %s`; never hand-edit. `--check` compares a fresh compute with this file." % (ratified, ratified))


def serial(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def land(ratified, root=HERE):
    if not ratified:
        raise SystemExit("REFUSED — --land needs --ratified sNNN-DN (a new edge type is a closed-vocabulary change, #75)")
    if not RULING_ID_RX.match(ratified):
        raise SystemExit("REFUSED — --ratified '%s' is not a ruling id (sNNN-DN)" % ratified)
    if not ruling_exists(ratified, root):
        raise SystemExit("REFUSED — ruling '%s' is not in knowledge/_rulings.json" % ratified)
    doc = compute(root)
    doc["$description"] = describe(ratified)
    doc["ratified"] = ratified
    out = os.path.join(root, OUT_NAME)
    open(out, "w", encoding="utf-8").write(serial(doc))
    return out, doc


def check(root=HERE):
    out = os.path.join(root, OUT_NAME)
    if not os.path.exists(out):
        print("gen_kg_sources --check: %s ABSENT — nothing landed" % OUT_NAME); return 1
    have = json.load(open(out, encoding="utf-8"))
    doc = compute(root)
    doc["$description"] = describe(have.get("ratified"))
    doc["ratified"] = have.get("ratified")
    if serial(doc) != serial(have):
        print("gen_kg_sources --check: STALE — %s differs from a fresh compute. Run: python3 knowledge/gen_kg_sources.py --land --ratified %s"
              % (OUT_NAME, have.get("ratified"))); return 1
    m = have["$measured"]
    print("gen_kg_sources --check OK — %d nodes · %d edges %s · in sync" % (m["nodes"], m["edges"], m["edgesByType"]))
    return 0


def selftest():
    fails, n = [], 0
    def bite(i, what, ok):
        nonlocal n; n += 1
        print("  %s bite %d — %s" % ("OK  " if ok else "FAIL", i, what))
        if not ok: fails.append(i)
    tmp = tempfile.mkdtemp(prefix="kgsrc-")
    try:
        # a scratch repo holding exactly what compute() opens: knowledge/{components,canon/type.css,_rulings.json},
        # the canon scripts and the snippets it resolves paths against
        k = os.path.join(tmp, "knowledge")
        shutil.copytree(os.path.join(HERE, "components"), os.path.join(k, "components"))
        shutil.copytree(os.path.join(HERE, "canon"), os.path.join(k, "canon"), ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(os.path.join(HERE, "snippets"), os.path.join(k, "snippets"), ignore=shutil.ignore_patterns("*.png"))
        shutil.copy(os.path.join(HERE, "_rulings.json"), k)
        if os.path.isdir(os.path.join(HERE, "_proforma")):
            shutil.copytree(os.path.join(HERE, "_proforma"), os.path.join(k, "_proforma"))
        base = compute(k)
        ids = {nd["id"] for nd in base["nodes"]}
        bite(1, "every edge is one of the four types and runs component: -> a node this file mints or a base snippet:",
             all(e["type"] in EDGE_TYPES and e["s"].startswith("component:") and (e["t"] in ids or e["t"].startswith("snippet:"))
                 for e in base["edges"]))
        bite(2, "every node is one of the four new kinds and carries the family", all(
            nd["type"] in ("typestyle", "file", "figma", "capability") and nd["fam"] == FAMILY for nd in base["nodes"]))
        bite(3, "no (component, target, type) triple twice", len({(e["s"], e["t"], e["type"]) for e in base["edges"]}) == len(base["edges"]))
        bite(4, "all four edge types are present on the live corpus", all(base["$measured"]["edgesByType"][t] > 0 for t in EDGE_TYPES))
        # 5 — MUTATION: a meta naming a defined composite it did not name before gains exactly one setIn
        victim = os.path.join(k, "components", "button.meta.json")
        vm = json.load(open(victim))
        have = {e["t"] for e in base["edges"] if e["s"] == "component:button" and e["type"] == "setIn"}
        plant = next(c for c in ("t-ed-display-1", "t-ed-display-2", "t-ed-heading-1") if "typestyle:" + c not in have)
        vm["$b2plant"] = "set in ." + plant
        json.dump(vm, open(victim, "w"))
        after = compute(k)
        bite(5, "MUTATION: naming .%s in button mints ONE setIn" % plant,
             after["$measured"]["edgesByType"]["setIn"] == base["$measured"]["edgesByType"]["setIn"] + 1)
        # 6 — MUTATION: an undefined composite is counted unresolved, never edged, never a node
        vm["$b2plant"] = "set in .t-cm-zzplanted"
        json.dump(vm, open(victim, "w"))
        after = compute(k)
        bite(6, "MUTATION: .t-cm-zzplanted adds no node and no edge, and IS counted unresolved",
             after["$measured"]["edges"] == base["$measured"]["edges"] and "typestyle:t-cm-zzplanted" not in {x["id"] for x in after["nodes"]}
             and after["$unresolved"]["setIn"]["count"] == base["$unresolved"]["setIn"]["count"] + 1)
        # 7 — MUTATION: a slot's new capability mints its node and one acceptsCapability
        vm.pop("$b2plant")
        vm.setdefault("slots", {})["b2plant"] = {"accepts": {"capability": ["zz-planted-capability"]}}
        json.dump(vm, open(victim, "w"))
        after = compute(k)
        bite(7, "MUTATION: a planted slot capability mints capability:zz-planted-capability and one edge",
             "capability:zz-planted-capability" in {x["id"] for x in after["nodes"]}
             and after["$measured"]["edgesByType"]["acceptsCapability"] == base["$measured"]["edgesByType"]["acceptsCapability"] + 1)
        # 8 — --land refuses without a recorded ratification and writes nothing
        out = os.path.join(k, OUT_NAME)
        refused = 0
        for bad in (None, "nonsense", "s999-D99"):
            try: land(bad, k)
            except SystemExit: refused += 1
        bite(8, "MUTATION: --land REFUSES with no id, a malformed id and an absent id, and writes no file",
             refused == 3 and not os.path.exists(out))
        # 9 — --check is 0 fresh and 1 after a meta moves
        vm["slots"].pop("b2plant"); json.dump(vm, open(victim, "w"))
        land("s269-D1", k)
        rc_fresh = check(k)
        vm["$b2plant"] = "set in ." + plant; json.dump(vm, open(victim, "w"))
        rc_stale = check(k)
        bite(9, "MUTATION: --check is 0 on a fresh landing and 1 after a meta moves under it", rc_fresh == 0 and rc_stale == 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("gen_kg_sources selftest: %d bite(s), %d fail(s)" % (n, len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--check" in argv:
        return check()
    if "--land" in argv:
        rid = argv[argv.index("--ratified") + 1] if "--ratified" in argv and argv.index("--ratified") + 1 < len(argv) else None
        out, doc = land(rid)
        m = doc["$measured"]
        print("LANDED %s under %s — %d nodes %s · %d edges %s" % (os.path.relpath(out, os.path.dirname(HERE)), rid,
              m["nodes"], m["nodesByKind"], m["edges"], m["edgesByType"]))
        return 0
    doc = compute()
    m = doc["$measured"]
    print("DRY RUN (writes nothing) — %d nodes %s · %d edges %s · metas %s · unresolved %s" % (
        m["nodes"], m["nodesByKind"], m["edges"], m["edgesByType"], m["metasByType"],
        {t: v["count"] for t, v in doc["$unresolved"].items() if not t.startswith("$")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
