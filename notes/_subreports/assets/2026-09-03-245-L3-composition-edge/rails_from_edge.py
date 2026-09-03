#!/usr/bin/env python3
"""L3 #245 — `--rails-from-edge` DRY RUN: how gen_bento_matrix_217.py --rails WOULD emit a grouping
dial DERIVED FROM the groupsWith edge (s234-D4: one home in the KG, consumers derive).

⛔ The live generator is NOT modified and its live output is NOT rewritten. This script IMPORTS the
generator's own edit_rails() (the same objects --rails serialises), adds ONE derived dial, and writes
  knowledge/_tmp/l3-245/_bento_edit_rails.proposed.json
  knowledge/_tmp/l3-245/rails-from-edge.txt        the proof transcript (hashes before/after, diff size)
The edge is read from the PROPOSAL (population-proposal.json), applied in memory over the live metas
— never from a live meta, because no live meta carries the edge today (grep -rn groupsWith -> 0).
"""
import copy, glob, hashlib, json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
KNOW = os.path.join(ROOT, "knowledge")
COMP = os.path.join(KNOW, "components")
RENDER = os.path.join(KNOW, "_render")
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [RENDER, KNOW]
import gen_bento_matrix_217 as G   # noqa: E402  (the live generator, imported, untouched)

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def load_metas_with_proposal():
    prop = json.load(open(os.path.join(OUT, "population-proposal.json"), encoding="utf-8"))
    metas = {}
    for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
        if os.path.basename(f).startswith("EXAMPLE"): continue
        stem = os.path.basename(f)[:-len(".meta.json")]
        m = json.load(open(f, encoding="utf-8"))
        if os.path.basename(f) in prop["proposals"]:
            m = copy.deepcopy(m); m.setdefault("edges", {})["groupsWith"] = prop["proposals"][os.path.basename(f)]["edges"]["groupsWith"]
        metas[stem] = m
    return metas, prop

def derive_grouping(metas, template_stem="template-dashboard-bento"):
    """Groups = connected components of the groupsWith graph over the template's $composes members.
    Reads ONLY edges.groupsWith (+ $composes for the member set). No prose is parsed."""
    tpl = metas[template_stem]
    members = [c.split(":", 1)[1] for c in tpl.get("$composes", []) if c.startswith("component:")]
    edges, unresolved = [], []
    for stem in members:
        for e in metas[stem].get("edges", {}).get("groupsWith", []):
            if e["ref"] is None:
                unresolved.append({"on": "component:" + stem, "$note": e.get("$note", "")})
            else:
                edges.append(("component:" + stem, e["ref"]))
    # union-find over members that carry at least one resolved edge
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in edges: parent[find(a)] = find(b)
    comps = {}
    for a, b in edges:
        comps.setdefault(find(a), set()).update([a, b])
    groups = []
    for root, ms in sorted(comps.items(), key=lambda kv: sorted(kv[1])):
        ms = sorted(ms)
        groups.append({
            "members": ms,
            "kind": "same-kind (self-edge)" if len(ms) == 1 else "mixed-kind pair",
            "edges": ["%s -> %s" % (a, b) for a, b in edges if find(a) == root],
            "uniform_in_kind": len(ms) == 1,
            "$c2": "rB C2: members uniform in kind, or an explicitly declared mixed group" if len(ms) > 1 else "rB C2 satisfied by construction",
        })
    for u in tpl.get("edges", {}).get("groupsWith", []):
        unresolved.append({"on": "component:" + template_stem, "$note": u.get("$note", "")})
    return {
        "kind": "derived",
        "control": "none - DERIVED, never picked. s234-D4: grouping lives ONCE in the KG; this dial is a "
                   "CONSUMER generated from edges.groupsWith and is not a second home.",
        "$derived_from": "knowledge/components/<member>.meta.json edges.groupsWith, member set = the "
                         "template's $composes. TODAY the edge is a PROPOSAL "
                         "(knowledge/_tmp/l3-245/population-proposal.json) applied in memory.",
        "types": ["dashboard"],
        "themes": "all",
        "theme_locked": False,
        "ruled_by": "s234-D4",
        "rule": "A group exists when its members answer ONE question the user came with (rB). Members "
                "uniform in kind (C2), one containment signal (C5), one accessible name (C3), "
                "contiguous at every band (C8). Membership and group COUNT are product decisions and "
                "Dave's (template-dashboard-bento.meta.json:12).",
        "groups": groups,
        "unresolved": unresolved,
        "$unresolved_note": "ref:null edges. Each names what Dave must settle before the dial can "
                            "resolve it (one-member group legality - rB Q3; a group identity in the "
                            "node grammar). Listed, never guessed.",
        "role_names": {
            "today": ["tpl-group-kpi", "tpl-group-chart", "tpl-group-rail"],
            "floated": ["tpl-group-lead", "tpl-group-evidence", "tpl-group-context"],
            "status": "FLOATED, NOT RULED - the words are Dave's (v1.0.6 brief L3). The dial does not "
                      "emit a class name until he picks.",
        },
    }

def main():
    lines = []
    live_rails = G.RAILS_PATH
    h0 = sha(live_rails); gen0 = sha(G.__file__)
    lines.append("live rails file:      %s" % os.path.relpath(live_rails, ROOT))
    lines.append("  sha256 BEFORE:      %s" % h0)
    lines.append("live generator sha256: %s (%s)" % (gen0, os.path.relpath(G.__file__, ROOT)))
    fresh = G.rails_json()
    lines.append("generator default path == file on disk (byte-identical): %s" % (fresh == open(live_rails, encoding="utf-8").read()))
    # the live CLI, written to a scratch path, must also equal the disk file
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(), "_rails.live-cli.json")   # sandbox scratch, never the mount
    r = subprocess.run([sys.executable, G.__file__, "--rails", "--out", tmp], capture_output=True, text=True, cwd=ROOT)
    lines.append("`gen_bento_matrix_217.py --rails --out <tmp>` rc=%d; tmp == disk: %s" % (r.returncode, open(tmp, encoding="utf-8").read() == open(live_rails, encoding="utf-8").read()))
    os.remove(tmp)
    metas, prop = load_metas_with_proposal()
    live_doc = G.edit_rails()
    doc = copy.deepcopy(live_doc)
    doc["$generated_by"] = "knowledge/_tmp/l3-245/rails_from_edge.py (DRY RUN of a proposed `--rails-from-edge`; the live `--rails` output is untouched)"
    doc["$proposed"] = "#245 L3 — ONE dial added by addition: dials.grouping, derived from edges.groupsWith. Nothing else differs from the live file."
    doc["dials"]["grouping"] = derive_grouping(metas)
    doc["types"]["dashboard"]["dials"] = list(live_doc["types"]["dashboard"]["dials"]) + ["grouping"]
    text = json.dumps(doc, indent=2, sort_keys=False) + "\n"
    out = os.path.join(OUT, "_bento_edit_rails.proposed.json")
    open(out, "w", encoding="utf-8").write(text)
    # what differs
    live_keys = set(live_doc["dials"]); new_keys = set(doc["dials"])
    lines.append("proposed rails written: %s (%d B)" % (os.path.relpath(out, ROOT), len(text.encode())))
    lines.append("  dials live %d -> proposed %d; added: %s" % (len([k for k in live_keys if not k.startswith('$')]), len([k for k in new_keys if not k.startswith('$')]), sorted(new_keys - live_keys)))
    lines.append("  types.dashboard.dials live %s -> proposed %s" % (live_doc["types"]["dashboard"]["dials"], doc["types"]["dashboard"]["dials"]))
    g = doc["dials"]["grouping"]
    lines.append("  derived groups: %d (%s)" % (len(g["groups"]), "; ".join(" + ".join(x["members"]) for x in g["groups"])))
    lines.append("  unresolved (ref:null) edges: %d" % len(g["unresolved"]))
    # everything else byte-identical? strip the two added keys + the dial and compare
    chk = copy.deepcopy(doc); chk.pop("$proposed"); chk["$generated_by"] = live_doc["$generated_by"]; chk["dials"].pop("grouping"); chk["types"]["dashboard"]["dials"].remove("grouping")
    lines.append("  proposed minus the addition == live generation: %s" % (json.dumps(chk, indent=2) + "\n" == fresh))
    h1 = sha(live_rails); gen1 = sha(G.__file__)
    lines.append("  sha256 AFTER:       %s  (unchanged: %s)" % (h1, h0 == h1))
    lines.append("  generator AFTER:    %s  (unchanged: %s)" % (gen1, gen0 == gen1))
    txt = "\n".join(lines) + "\n"
    open(os.path.join(OUT, "rails-from-edge.txt"), "w", encoding="utf-8").write(txt)
    print(txt)
    return 0 if (h0 == h1 and gen0 == gen1) else 1

if __name__ == "__main__":
    sys.exit(main())
