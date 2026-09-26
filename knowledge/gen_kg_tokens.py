#!/usr/bin/env python3
"""gen_kg_tokens.py — the TOKEN-GROUP node + `bindsToken` edge generator (#304 R3, enacts s277-D12).

s277-D12 (Dave, 2026-09-16, audit D-5 option a, his 'go' on the read-back): "TOKENS ENTER THE GRAPH
AT GROUP GRAIN WITH THEIR TIER (audit D-5 option a), as _compose_slice.py already reads them (~128
groups, the top 12 carrying 70% of references), with a structural `bindsToken` from the metas' typed
`tokens` block — honouring s269-D3's 'TIER GRAIN — semantic versus primitive — and NEVER as 932 leaf
nodes'". Option (a) on the page he ticked (notes/_lanes/277/kg-audit/REVIEW-kg-audit-2026-09-16-v2.html):
"The token group ... as the token: node, each carrying its tier (semantic · component-type ·
foundation · primitive) as an attribute; bindsToken minted structurally from each meta's tokens block;
blast radius carried from _blast-radius.json as an attribute. ... no sentence authored."

  NODE KIND   token:<group>   e.g. token:text, token:border-radius
              attributes: tier + source (READ from _compose_slice._token_tier_map — ONE reader, so
              the graph and the slice cannot disagree on a group's tier), blast (distinct components
              reaching any member of the group in tokens/_blast-radius.json) and blastTop (up to four
              members with their own blast). Every group the tier map knows becomes a node, bound or
              not — an unbound group is a measured orphan, never dropped.
  EDGE TYPE   bindsToken      component:<slug> -> token:<group>
              one edge per (component, group), from _compose_slice._meta_token_groups() over the
              meta's `tokens` block (the same TOKEN_PATH_RX walk the slice uses); `paths` carries the
              member paths the meta names, sorted. STRUCTURAL: no prose is read beyond the path parse.

NEVER INVENTED: a path in a meta whose group the store does not define (e.g. "font-5/medium") gets
no edge and no node; it is COUNTED in `$unresolved` with up to eight examples.
NOT HERE: leaf tokens (s269-D3 refused them), aliasOf (A3's option, not ruled), typography
composites (the slice's fifth tier "composite" is not in D-5(a)'s four), the npm-registry sequel
(P-277-5, parked, his to time).

MODES
  (default) --dry-run   compute and print the counts; writes nothing
  --land --ratified sNNN-DN   write knowledge/_token_nodes.json; REFUSES unless the id is in
                              knowledge/_rulings.json
  --check               recompute and compare with the landed file (content, not mtime); rc 1 on drift
  --selftest            mutation bites (see selftest())
"""
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import glob, json, os, re, sys, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_NAME = "_token_nodes.json"
FAMILY = "tokens"
RULING_ID_RX = re.compile(r"^s\d{2,3}-D\d{1,3}$")
TIERS = ("semantic", "component-type", "foundation", "primitive")   # D-5(a)'s four, in its order


def _slice(root):
    sys.path.insert(0, root)
    import _compose_slice as C   # read-only: two functions, one graph load
    return C


def compute(root=HERE):
    C = _slice(root)
    g = C.load_graph(root)
    tiers = g["token_tiers"]                                   # group -> (tier, source)
    bad = sorted(t for t, _ in tiers.values() if t not in TIERS)
    if bad:
        raise SystemExit("REFUSED — the slice's tier map carries a tier D-5(a) does not name: %s" % bad)
    br_path = os.path.join(root, "tokens", "_blast-radius.json")
    br = json.load(open(br_path, encoding="utf-8")) if os.path.exists(br_path) else {}
    reach, member_blast = {}, {}
    for row in br.get("ranking", []):
        tok = row.get("token") or ""
        grp = tok.split("/")[0]
        reach.setdefault(grp, set()).update(row.get("components") or [])
        member_blast.setdefault(grp, []).append((row.get("blast", 0), tok))
    nodes = []
    for grp in sorted(tiers):
        tier, src = tiers[grp]
        top = sorted(member_blast.get(grp, []), key=lambda x: (-x[0], x[1]))[:4]
        n = {"id": "token:" + grp, "type": "token", "label": grp, "fam": FAMILY,
             "tier": tier, "source": src, "blast": len(reach.get(grp, ()))}
        if top:
            n["blastTop"] = [{"token": t, "blast": b} for b, t in top]
        nodes.append(n)
    known = {n["id"] for n in nodes}
    edges, unresolved, metas_read, metas_bound = [], {}, 0, 0
    for f in sorted(glob.glob(os.path.join(root, "components", "*.meta.json"))):
        slug = os.path.basename(f)[:-10]
        if slug.startswith("EXAMPLE-"):
            continue
        try:
            m = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(m, dict) or not m.get("tokens"):
            continue
        metas_read += 1
        groups = C._meta_token_groups(m, g)
        # the paths per group, and the paths whose group the store does not define (counted, not edged)
        paths = {}
        for v in _walk(m.get("tokens")):
            for p in C.TOKEN_PATH_RX.findall(v.lower()):
                grp = p.split("/")[0]
                if grp in tiers:
                    paths.setdefault(grp, set()).add(p)
                else:
                    unresolved.setdefault(grp, set()).add(slug)
        if groups:
            metas_bound += 1
        for grp in sorted(groups):
            t = "token:" + grp
            if t not in known:
                continue
            edges.append({"s": "component:" + slug, "t": t, "type": "bindsToken", "fam": FAMILY,
                          "paths": sorted(paths.get(grp, ()))})
    doc = {
        "$description": None,   # set by land()
        "family": FAMILY,
        "$ruled": {"s277-D12": "tokens at GROUP grain with their TIER, bindsToken from the metas' typed tokens block (audit D-5 option a); s269-D3: never as leaf nodes"},
        "$measured": {"groups": len(nodes), "groupsBound": len({e["t"] for e in edges}),
                      "bindsToken": len(edges), "metasWithTokens": metas_read, "metasBinding": metas_bound,
                      "byTier": {t: sum(1 for n in nodes if n["tier"] == t) for t in TIERS},
                      "blastSource": "tokens/_blast-radius.json (generated %s)" % br.get("generated")},
        "$unresolved": {"$what": "path groups named in a meta's tokens block that NO token file defines — no node, no edge, counted (never invented)",
                        "groups": len(unresolved),
                        "examples": {k: sorted(v)[:3] for k, v in sorted(unresolved.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:8]}},
        "nodes": nodes, "edges": edges}
    return doc


def _walk(v):
    if isinstance(v, dict):
        for k, x in v.items():
            yield str(k)
            yield from _walk(x)
    elif isinstance(v, list):
        for x in v:
            yield from _walk(x)
    elif v is not None:
        yield str(v)


def ruling_exists(rid, root=HERE):
    try:
        d = json.load(open(os.path.join(root, "_rulings.json"), encoding="utf-8"))
    except Exception:
        return False
    return any(isinstance(r, dict) and r.get("id") == rid for r in d.get("rulings", []))


def describe(ratified):
    return ("RATIFIED _token_nodes.json under %s (#304 R3). token:<group> nodes at GROUP grain with their "
            "tier + bindsToken component->token edges, both STRUCTURAL (no sentence authored). Regenerate "
            "with `python3 knowledge/gen_kg_tokens.py --land --ratified %s`; never hand-edit. `--check` "
            "compares a fresh compute with this file." % (ratified, ratified))


def serial(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def land(ratified, root=HERE):
    if not ratified:
        raise SystemExit("REFUSED — --land needs --ratified sNNN-DN (a new node kind and a new edge type are closed-vocabulary changes, #75)")
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
        print("gen_kg_tokens --check: %s ABSENT — nothing landed" % OUT_NAME); return 1
    have = json.load(open(out, encoding="utf-8"))
    doc = compute(root)
    doc["$description"] = describe(have.get("ratified"))
    doc["ratified"] = have.get("ratified")
    if serial(doc) != serial(have):
        print("gen_kg_tokens --check: STALE — %s differs from a fresh compute. Run: python3 knowledge/gen_kg_tokens.py --land --ratified %s"
              % (OUT_NAME, have.get("ratified"))); return 1
    m = have["$measured"]
    print("gen_kg_tokens --check OK — %d token: groups (%d bound) · %d bindsToken · in sync" % (m["groups"], m["groupsBound"], m["bindsToken"]))
    return 0


def selftest():
    fails, n = [], 0
    def bite(i, what, ok):
        nonlocal n; n += 1
        print("  %s bite %d — %s" % ("OK  " if ok else "FAIL", i, what))
        if not ok: fails.append(i)
    tmp = tempfile.mkdtemp(prefix="kgtok-")
    try:
        # a scratch copy of exactly the inputs the reader opens (the slice loads its graph from `root`)
        shutil.copytree(HERE, os.path.join(tmp, "k"), ignore=shutil.ignore_patterns(
            "_tmp", "__pycache__", "_render", "compliance", "assets", "_release", "*.png", "*.zip"))
        k = os.path.join(tmp, "k")
        base = compute(k)
        ids = {nd["id"] for nd in base["nodes"]}
        bite(1, "every node is token:<group> at group grain — no leaf id carries a '/'",
             all(i.startswith("token:") and "/" not in i for i in ids))
        bite(2, "every node's tier is one of D-5(a)'s four", all(nd["tier"] in TIERS for nd in base["nodes"]))
        bite(3, "every bindsToken runs component: -> a token: node that exists", all(
            e["s"].startswith("component:") and e["t"] in ids and e["type"] == "bindsToken" for e in base["edges"]))
        bite(4, "no (component, group) pair twice", len({(e["s"], e["t"]) for e in base["edges"]}) == len(base["edges"]))
        # 5 — MUTATION: a meta that names a new path in a KNOWN group gains exactly that edge
        mp = sorted(glob.glob(os.path.join(k, "components", "*.meta.json")))
        victim = next(p for p in mp if "EXAMPLE-" not in p and json.load(open(p)).get("tokens"))
        slug = os.path.basename(victim)[:-10]
        vm = json.load(open(victim))
        known_unbound = sorted(i.split(":", 1)[1] for i in ids
                               if not any(e["s"] == "component:" + slug and e["t"] == i for e in base["edges"]))
        grp = known_unbound[0]
        vm["tokens"]["$r3plant"] = grp + "/planted-member"
        json.dump(vm, open(victim, "w"))
        after = compute(k)
        new = [e for e in after["edges"] if e["s"] == "component:" + slug and e["t"] == "token:" + grp]
        bite(5, "MUTATION: planting %s/… in %s mints ONE bindsToken to token:%s" % (grp, slug, grp),
             len(after["edges"]) == len(base["edges"]) + 1 and len(new) == 1)
        # 6 — MUTATION: a path in an UNKNOWN group is counted unresolved, never edged, never a node
        vm["tokens"]["$r3plant"] = "zzplanted/member"
        json.dump(vm, open(victim, "w"))
        after = compute(k)
        bite(6, "MUTATION: an unknown group 'zzplanted' adds no node and no edge, and IS counted unresolved",
             len(after["edges"]) == len(base["edges"]) and "token:zzplanted" not in {nd["id"] for nd in after["nodes"]}
             and after["$unresolved"]["groups"] == base["$unresolved"]["groups"] + 1)
        # 7 — --land refuses without a recorded ratification and writes nothing
        out = os.path.join(k, OUT_NAME)
        if os.path.exists(out): os.remove(out)
        refused = 0
        for bad in (None, "nonsense", "s999-D99"):
            try: land(bad, k)
            except SystemExit: refused += 1
        bite(7, "MUTATION: --land REFUSES with no id, a malformed id and an absent id, and writes no file",
             refused == 3 and not os.path.exists(out))
        # 8 — --check catches a landed file that drifted
        json.dump(vm, open(victim, "w"))                       # keep the zz plant: compute differs from…
        vm["tokens"].pop("$r3plant"); json.dump(vm, open(victim, "w"))
        land("s277-D12", k)
        rc_fresh = check(k)
        vm["tokens"]["$r3plant"] = grp + "/planted-member"; json.dump(vm, open(victim, "w"))
        rc_stale = check(k)
        bite(8, "MUTATION: --check is 0 on a fresh landing and 1 after a meta moves under it", rc_fresh == 0 and rc_stale == 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("gen_kg_tokens selftest: %d bite(s), %d fail(s)" % (n, len(fails)))
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
        print("LANDED %s under %s — %d token: groups (%d bound) · %d bindsToken · %d unresolved group(s)"
              % (os.path.relpath(out, os.path.dirname(HERE)), rid, m["groups"], m["groupsBound"], m["bindsToken"], doc["$unresolved"]["groups"]))
        return 0
    doc = compute()
    m = doc["$measured"]
    print("DRY RUN (writes nothing) — %d token: groups %s · %d bound · %d bindsToken from %d metas · %d unresolved group(s)"
          % (m["groups"], m["byTier"], m["groupsBound"], m["bindsToken"], m["metasWithTokens"], doc["$unresolved"]["groups"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
