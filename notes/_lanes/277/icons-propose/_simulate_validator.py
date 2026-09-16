#!/usr/bin/env python3
"""_simulate_validator.py — apply meta.schema.diff to a SCRATCH copy of knowledge/
and run _validate_kg.py against the simulated tree (#277 lane RI).

Why this exists. The diff proposes three node kinds and two new meta `edges`
fields. A diff nobody ran is a guess with a `+` in front of it, so this script
builds the tree the diff describes, plants metas that USE the new fields, and
reports what the real validator says — without writing one byte under knowledge/.

What it builds in the scratch tree:
  1. knowledge/ copied whole (symlink-free copy of the files the validator reads).
  2. _validate_kg.py patched: REF_RE + NODE_KINDS + icon_ids()/logo_ids() + the
     three resolver entries. Applied by ANCHORED textual span — never a re-dump.
  3. meta.schema.json patched: definitions.assetEdge + edges.usesIcon +
     edges.usesLogo + edges.$assets-contract, by loading, inserting and dumping
     with the file's own indent.
  4. THE PROOF METAS. The generator's own live output is written INTO the scratch
     metas: every component that the byte-match binds gets a real `usesIcon` list
     and every logo consumer gets a real `usesLogo` list, with $source naming the
     join. 105 + 9 metas are touched IN THE SCRATCH ONLY.
  5. Four NEGATIVE metas, so the run proves the grammar can say NO:
       N1  ref `icon:menu-search`   — the B1 slug, must FAIL to resolve
       N2  ref `icon:not-a-real-icon` — must FAIL
       N3  ref `logo:hexagon`       — a lockup WORD, not a stem; must FAIL
       N4  a usesIcon entry with no `$source` — must FAIL the schema arm
     These are run in a SECOND pass so the first pass can be clean.

    python3 notes/_lanes/277/icons-propose/_simulate_validator.py [scratch-dir]
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
K = REPO / "knowledge"

VK_OLD_REF = ('REF_RE = re.compile(r"^(component|pattern|context|snippet|ruling|role|intent'
              '|shape|rule|ux):.+$")\n'
              'NODE_KINDS = ("component", "pattern", "context", "snippet", "ruling", "role", '
              '"intent", "shape",\n              "rule", "ux")')
VK_NEW_REF = ('REF_RE = re.compile(r"^(component|pattern|context|snippet|ruling|role|intent'
              '|shape|rule|ux"\n                    r"|icon|iconGroup|logo):.+$")\n'
              'NODE_KINDS = ("component", "pattern", "context", "snippet", "ruling", "role", '
              '"intent", "shape",\n              "rule", "ux", "icon", "iconGroup", "logo")')

VK_OLD_STORES = 'UX_NODES = HERE / "_ux_principle_nodes.json"'
VK_NEW_STORES = VK_OLD_STORES + '''
# s277-Dn (#277 lane RI): the three asset kinds resolve against the file that IS their home.
ICON_MANIFEST = HERE / "assets" / "icons" / "icons.manifest.json"
LOGO_DIR = HERE / "assets" / "logos"


def icon_ids(path=None):
    path = path or ICON_MANIFEST
    if not path.exists():
        return set(), set()
    data = json.loads(path.read_text(encoding="utf-8"))
    groups = data.get("groups", {})
    icons = {f"icon:{r['slug']}" for lst in groups.values() for r in lst if r.get("slug")}
    gids = {"iconGroup:" + re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-") for g in groups}
    return icons, gids


def logo_ids(path=None):
    path = path or LOGO_DIR
    if not path.exists():
        return set()
    return {"logo:" + p.stem for p in sorted(path.glob("*.svg"))}'''

VK_OLD_RES = '        "ux": ux_ids(),\n    }'
VK_NEW_RES = ('        "ux": ux_ids(),\n'
              '        "icon": icon_ids()[0],\n'
              '        "iconGroup": icon_ids()[1],\n'
              '        "logo": logo_ids(),\n    }')

ASSET_EDGE = {
    "description": "s277-Dn (PROPOSED — s269-D1 STEP 4, lane RI #277). One GENERATED "
                   "reference from a component to a library asset: an icon:<slug> from "
                   "icons.manifest.json or a logo:<stem> from assets/logos/. NOT "
                   "definitions/edge (widening the shared pattern would let containedBy "
                   "point at an icon) and NOT definitions/obeysEdge ($why is required "
                   "there because obeys is AUTHORED; these are generated). $source is "
                   "REQUIRED instead, naming the join. ref is never null.",
    "type": "object",
    "required": ["ref", "$source"],
    "additionalProperties": False,
    "properties": {
        "ref": {"type": "string", "pattern": "^(icon|logo):.+$"},
        "$source": {"type": "string", "minLength": 20,
                    "description": "The join, named. Never a regex over prose."},
        "$note": {"type": "string"},
    },
}

SRC_ICON = ("byte-match of normalised <path d> against the icon library "
            "(_validate_icons.py norm()/DRE), via renderedBy")
SRC_LOGO = 'src="…/assets/logos/<file>.svg" in the renderedBy snippet'


def patch_validator(scratch_k):
    p = scratch_k / "_validate_kg.py"
    s = p.read_text(encoding="utf-8")
    for old, new, what in ((VK_OLD_REF, VK_NEW_REF, "REF_RE/NODE_KINDS"),
                           (VK_OLD_STORES, VK_NEW_STORES, "the two stores + two resolvers"),
                           (VK_OLD_RES, VK_NEW_RES, "the resolvers dict")):
        if s.count(old) != 1:
            raise SystemExit(f"ANCHOR MISS applying {what}: found {s.count(old)} of 1. "
                             "The live file moved; re-read it before trusting this diff.")
        s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    return ["REF_RE/NODE_KINDS", "the two stores + two resolvers", "the resolvers dict"]


def patch_schema(scratch_k):
    p = scratch_k / "components" / "meta.schema.json"
    sch = json.loads(p.read_text(encoding="utf-8"))
    defs, ep = sch["definitions"], sch["properties"]["edges"]["properties"]
    if "assetEdge" in defs or "usesIcon" in ep:
        raise SystemExit("the live schema already carries the addition — this diff is stale")
    # rebuild definitions so assetEdge sits directly after obeysEdge (insert, never append)
    out = {}
    for k, v in defs.items():
        out[k] = v
        if k == "obeysEdge":
            out["assetEdge"] = ASSET_EDGE
    sch["definitions"] = out
    nep = {}
    for k, v in ep.items():
        if k == "$contract":
            nep["usesIcon"] = {"type": "array", "items": {"$ref": "#/definitions/assetEdge"},
                               "description": "s277-Dn (PROPOSED). The library glyphs this "
                                              "component's REFERENCE SNIPPET renders, by "
                                              "byte-match. Four declared limits travel with it."}
            nep["usesLogo"] = {"type": "array", "items": {"$ref": "#/definitions/assetEdge"},
                               "description": "s277-Dn (PROPOSED). The logo lockups this "
                                              "component's reference snippet loads, from src=."}
            nep["$assets-contract"] = {"type": "string",
                                       "description": "s277-Dn (PROPOSED). The provenance "
                                                      "sentence for usesIcon / usesLogo."}
        nep[k] = v
    sch["properties"]["edges"]["properties"] = nep
    p.write_text(json.dumps(sch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(out), len(nep)


def plant(scratch_k, dry):
    """Write the generator's own live usesIcon / usesLogo output into the scratch metas."""
    by_comp = {}
    for pay in ("_icon_nodes.json", "_logo_nodes.json"):
        d = json.loads((LANE / pay).read_text(encoding="utf-8"))
        for e in d["edges"]:
            if e["type"] in ("usesIcon", "usesLogo") and e["t"] and str(e["s"]).startswith("component:"):
                by_comp.setdefault(e["s"][len("component:"):], []).append(e)
    touched, entries = 0, 0
    for slug, es in sorted(by_comp.items()):
        f = scratch_k / "components" / f"{slug}.meta.json"
        if not f.exists():
            continue
        m = json.loads(f.read_text(encoding="utf-8"))
        edges = m.setdefault("edges", {})
        for e in es:
            key = e["type"]
            src = SRC_ICON if key == "usesIcon" else SRC_LOGO
            edges.setdefault(key, []).append({"ref": e["t"], "$source": src})
            entries += 1
        edges["$assets-contract"] = ("GENERATED by notes/_lanes/277/icons-propose/"
                                     "gen_kg_icons.py — never authored, never from prose.")
        f.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        touched += 1
    return touched, entries


NEGATIVES = [
    ("N1", "icon:menu-search", "usesIcon", "the B1 slug: ruled in by s212-D9, on disk, NOT in the manifest"),
    ("N2", "icon:not-a-real-icon", "usesIcon", "a slug the manifest does not hold"),
    ("N3", "logo:hexagon", "usesLogo", "a lockup WORD, not a filename stem"),
]


def build_tree(sk):
    """Copy ONLY what _validate_kg.py reads. A whole-tree copytree dies on the 8.9 GB
    seat disk at the photography folder, and the validator never opens a .jpg or a
    .svg BODY: it reads the snippet FILENAMES and, with the diff applied, the logo
    FILENAMES. So those two are recreated as empty files with the right names, which
    is the same STORE the resolver sees, and it is declared here rather than hidden."""
    (sk / "components").mkdir(parents=True)
    (sk / "snippets").mkdir(parents=True)
    (sk / "guidelines").mkdir(parents=True)
    (sk / "assets" / "icons").mkdir(parents=True)
    (sk / "assets" / "logos").mkdir(parents=True)
    (sk.parent / "reviews").mkdir(parents=True, exist_ok=True)
    for f in sorted((K / "components").glob("*")):
        if f.is_file():
            shutil.copy2(f, sk / "components" / f.name)
    shutil.copytree(K / "_proforma", sk / "_proforma",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    # The snippets are copied WHOLE. An empty stand-in satisfies snippet_ids(), which
    # reads filenames, but _validate_kg.py's freshness arm re-runs gen_kg_edges.py on a
    # scratch copy and THAT reads the bodies — so a filename-only snippets/ turns the
    # baseline red for a reason that has nothing to do with this diff.
    shutil.copytree(K / "snippets", sk / "snippets", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for f in sorted((K / "assets" / "logos").glob("*.svg")):
        (sk / "assets" / "logos" / f.name).write_text("", encoding="utf-8")
    shutil.copy2(K / "assets" / "icons" / "icons.manifest.json",
                 sk / "assets" / "icons" / "icons.manifest.json")
    shutil.copy2(K / "guidelines" / "_rules-index.json", sk / "guidelines" / "_rules-index.json")
    for name in ("_validate_kg.py", "_helpgate.py", "gen_kg_edges.py", "_rulings.json",
                 "roles.json", "chart-intents.json", "shapes.json", "_ux_principle_nodes.json",
                 "_rule_nodes.json"):
        if (K / name).exists():
            shutil.copy2(K / name, sk / name)
    for f in sorted((REPO / "reviews").glob("KG-REVIEW-VERDICTS-*.json")):
        shutil.copy2(f, sk.parent / "reviews" / f.name)


def run_validator(scratch_k):
    r = subprocess.run([sys.executable, str(scratch_k / "_validate_kg.py")],
                       capture_output=True, text=True, cwd=str(scratch_k.parent), timeout=600)
    return r.returncode, (r.stdout + r.stderr)


def main():
    scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    root = scratch / "simtree"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    print(f"scratch: {root}")
    sk = root / "knowledge"
    build_tree(sk)

    print("\n--- 0. BASELINE, unpatched scratch copy (must match the live tree) ---")
    rc0, out0 = run_validator(sk)
    print("\n".join(out0.strip().splitlines()[-4:]) + f"\n  rc = {rc0}")

    print("\n--- 1. apply the diff ---")
    for what in patch_validator(sk):
        print(f"  _validate_kg.py: {what} — applied by anchored span")
    nd, ne = patch_schema(sk)
    print(f"  meta.schema.json: definitions {nd} keys, edges.properties {ne} keys")

    print("\n--- 2. plant the generator's live output into the scratch metas ---")
    t, e = plant(sk, LANE / "dry-run.json")
    print(f"  {t} metas given real usesIcon / usesLogo lists · {e} entries · "
          f"scratch only, live tree untouched")

    print("\n--- 3. PASS 1 — the validator on the simulated tree ---")
    rc1, out1 = run_validator(sk)
    print("\n".join("  " + l for l in out1.strip().splitlines()[-6:]))
    print(f"  rc = {rc1}  -> {'OK' if rc1 == 0 else 'FAIL'}")

    print("\n--- 4. PASS 2 — the negatives: can the new grammar say NO? ---")
    victim = sk / "components" / "accordion.meta.json"
    if not victim.exists():
        victim = sorted((sk / "components").glob("*.meta.json"))[0]
    keep = victim.read_text(encoding="utf-8")
    results = []
    for nid, ref, key, why in NEGATIVES:
        m = json.loads(keep)
        m.setdefault("edges", {}).setdefault(key, []).append({"ref": ref, "$source": SRC_ICON})
        victim.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rc, out = run_validator(sk)
        caught = rc != 0 and ref in out
        results.append((nid, ref, why, caught))
        print(f"  {nid}  {ref:24s} -> {'CAUGHT (rc=%d)' % rc if caught else 'MISSED — A FINDING'}"
              f"   [{why}]")
    # N4: the schema arm — a usesIcon entry with no $source
    m = json.loads(keep)
    m.setdefault("edges", {}).setdefault("usesIcon", []).append({"ref": "icon:alert"})
    victim.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rc, out = run_validator(sk)
    caught = rc != 0 and "$source" in out
    results.append(("N4", "no $source", "a generated entry that does not name its join", caught))
    print(f"  N4  {'no $source':24s} -> {'CAUGHT (rc=%d)' % rc if caught else 'MISSED — A FINDING'}"
          f"   [a generated entry that does not name its join]")
    victim.write_text(keep, encoding="utf-8")

    rc2, _ = run_validator(sk)
    print(f"\n  restored: rc = {rc2}")
    missed = [r[0] for r in results if not r[3]]
    print("\nRESULT  baseline rc=%d · simulated rc=%d · negatives %s"
          % (rc0, rc1, "ALL CAUGHT" if not missed else f"MISSED {missed} — FINDING"))
    print(f"live tree untouched: {K} (this script copied it and wrote only under {root})")
    return 0 if rc1 == 0 and not missed else 1


if __name__ == "__main__":
    sys.exit(main())
