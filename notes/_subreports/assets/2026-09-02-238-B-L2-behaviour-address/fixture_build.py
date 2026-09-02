#!/usr/bin/env python3
"""
fixture_build.py — #238 lane B. Builds the FIXTURE the generator and the gate are driven on —
NEVER the live tree (brief pitfall 1: a generator run on the live tree is a partial regen serial).

  python3 fixture_build.py <repo> <fixture_root>      e.g. … /sessions/…/UX-design /dev/shm/l2fix

What it does, in order (each step prints a measured line):
  1. copies knowledge/{*.py, component-types.json, snippets/, components/, tokens/, canon/}
     (knowledge/assets is 5.2 GB and is not copied — nothing here needs it);
  2. applies the PROPOSED schema (apply_schema.py) to the fixture's meta.schema.json;
  3. applies the 20 PROPOSED typed objects (behaviour-migration.json) to the fixture's 20 metas,
     BY ADDITION — the old prose is what sits under $note;
  4. validates all fixture metas against the fixture schema (the _build_integrity.py posture);
  5. runs gen_component_partials.py --check (expects 20 out-of-sync), then the write pass
     (expects 20 injected), then --check again (expects OK) — on the FIXTURE;
  6. composes ONE screen with L1's mint (gen_provenance_receipt.py --compose) from three
     snippets — Date-picker and Textarea (typed after step 3) and Stat-card (meta:NONE, the
     control) — then splices each typed snippet's inline <script> element VERBATIM into the
     page between APOLLO-SPLICE markers of kind=script and re-mints, because the L1 mint has
     no `kind: script` (finding, priced in the report).
/dev/shm is per-bash-call in this sandbox, so a drive script calls this first, every time.
"""
import glob, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sh(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=150)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    repo, root = sys.argv[1], sys.argv[2]
    K = os.path.join(root, "knowledge")
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(K)
    # 1. copy
    for f in glob.glob(os.path.join(repo, "knowledge", "*.py")) + [os.path.join(repo, "knowledge", "component-types.json")]:
        shutil.copy(f, K)
    for d in ("snippets", "components", "tokens", "canon"):
        shutil.copytree(os.path.join(repo, "knowledge", d), os.path.join(K, d))
    os.makedirs(os.path.join(root, "dashboards"))
    print("1. fixture: %d py, %d snippets, %d metas copied to %s" % (
        len(glob.glob(os.path.join(K, "*.py"))), len(glob.glob(os.path.join(K, "snippets", "*.reference.html"))),
        len(glob.glob(os.path.join(K, "components", "*.meta.json"))), root))
    # 2. schema
    rc, out = sh("python3 %s %s %s" % (os.path.join(HERE, "apply_schema.py"),
                                      os.path.join(K, "components", "meta.schema.json"),
                                      os.path.join(K, "components", "meta.schema.json")), repo)
    print("2. schema:", out.splitlines()[-1] if out else rc)
    assert rc == 0, out
    # 3. the 20 typed objects, by addition
    mig = json.load(open(os.path.join(HERE, "behaviour-migration.json"), encoding="utf-8"))
    n = 0
    for it in mig["items"]:
        mp = os.path.join(root, it["meta"])
        d = json.load(open(mp, encoding="utf-8"))
        assert d["behaviour"] == it["old"], "fixture meta prose differs from the migration's `old` — regenerate the migration"
        assert it["proposed"]["$note"] == it["old"], "by-addition broken: $note is not the old prose"
        d["behaviour"] = it["proposed"]
        json.dump(d, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        n += 1
    print("3. applied %d proposed typed objects to FIXTURE metas (prose kept under $note)" % n)
    # 4. validate
    import jsonschema
    schema = json.load(open(os.path.join(K, "components", "meta.schema.json"), encoding="utf-8"))
    V = jsonschema.Draft7Validator(schema, resolver=jsonschema.RefResolver(base_uri="", referrer=schema))
    metas = [f for f in glob.glob(os.path.join(K, "components", "*.meta.json")) if not os.path.basename(f).startswith("EXAMPLE")]
    bad = [os.path.basename(f) for f in metas if list(V.iter_errors(json.load(open(f, encoding="utf-8"))))]
    typed = sum(1 for f in metas if isinstance(json.load(open(f, encoding="utf-8")).get("behaviour"), dict)
                and "script" in json.load(open(f, encoding="utf-8"))["behaviour"])
    print("4. fixture metas vs fixture schema: %d/%d valid, %d TYPED behaviour, red: %s" % (len(metas) - len(bad), len(metas), typed, bad or "none"))
    assert not bad
    # 5. generator on the fixture
    rc, out = sh("python3 knowledge/gen_component_partials.py --check", root)
    oos = re.search(r"OUT OF SYNC: (.*)", out)
    n_oos = len(oos.group(1).split(", ")) if oos else 0
    print("5a. --check before: rc=%d, %d out-of-sync (behaviour-manifest): %s" % (rc, n_oos, (oos.group(1)[:120] + "…") if oos else out[-160:]))
    rc, out = sh("python3 knowledge/gen_component_partials.py", root)
    print("5b. write pass: rc=%d — %s" % (rc, out.splitlines()[-1] if out else ""))
    rc, out = sh("python3 knowledge/gen_component_partials.py --check", root)
    print("5c. --check after: rc=%d — %s" % (rc, out.splitlines()[-1] if out else ""))
    with_block = [os.path.basename(p) for p in glob.glob(os.path.join(K, "snippets", "*.reference.html"))
                  if 'id="behaviour-manifest"' in open(p, encoding="utf-8").read()]
    changed = []
    for p in glob.glob(os.path.join(K, "snippets", "*.reference.html")):
        live = os.path.join(repo, "knowledge", "snippets", os.path.basename(p))
        if open(p, encoding="utf-8").read() != open(live, encoding="utf-8").read():
            changed.append(os.path.basename(p))
    print("5d. snippets carrying #behaviour-manifest: %d; snippets that differ from the LIVE tree: %d (%s)" % (
        len(with_block), len(changed), "same set" if sorted(with_block) == sorted(changed) else "DIFFERENT SET"))
    # where does the block sit? beside #token-manifest, before the inline script
    dp = open(os.path.join(K, "snippets", "Date-picker.reference.html"), encoding="utf-8").read()
    tm = dp.index('id="token-manifest"'); bm = dp.index('id="behaviour-manifest"'); sc = dp.index("<script>\n", bm)
    print("5e. Date-picker: #token-manifest@%d < #behaviour-manifest@%d < first executable <script>@%d — %s" % (
        tm, bm, sc, "BESIDE, in order" if tm < bm < sc else "WRONG ORDER"))
    # 6. compose one screen
    spec = {"title": "L2 fixture — behaviour address drive", "pack": "1.0.5", "theme": "light",
            "regions": [
                {"region": "Date-picker#style", "snippet": "Date-picker", "kind": "style"},
                {"region": "Textarea#style", "snippet": "Textarea", "kind": "style"},
                {"region": "Stat-card#style", "snippet": "Stat-card", "kind": "style"},
                {"region": "Date-picker#markup", "snippet": "Date-picker", "select": ".dp", "kind": "markup", "variant": "single"},
                {"region": "Textarea#markup", "snippet": "Textarea", "select": ".tx-group", "kind": "markup"},
                {"region": "Stat-card#markup", "snippet": "Stat-card", "select": ".stat-card", "kind": "markup", "props": {"delta": "up"}},
            ]}
    spec_path = os.path.join(root, "dashboards", "l2-fixture.spec.json")
    json.dump(spec, open(spec_path, "w"), indent=1)
    page_path = os.path.join(root, "dashboards", "l2-fixture.html")
    rc, out = sh("python3 knowledge/gen_provenance_receipt.py --compose %s -o %s" % (spec_path, page_path), root)
    if rc != 0:
        print("6a. compose REFUSED:", out[-400:]); sys.exit(1)
    page = open(page_path, encoding="utf-8").read()
    sys.path.insert(0, K)
    import _validate_receipt as VR
    spliced = []
    for name in ("Date-picker", "Textarea"):
        sh_ = open(os.path.join(K, "snippets", name + ".reference.html"), encoding="utf-8").read()
        body, span = VR.inline_scripts(sh_)[0]
        # the WHOLE element, verbatim, so the body bytes are identical to what #script denotes
        el_start = sh_.rfind("<script", 0, span[0]); el_end = sh_.index("</script>", span[1]) + len("</script>")
        element = sh_[el_start:el_end]
        region = "%s#script" % name
        block = "%s\n%s\n%s" % (VR.splice_marker_start(region, "knowledge/snippets/%s.reference.html" % name, "script"),
                                element, VR.splice_marker_end(region))
        page = page.replace("</body>", block + "\n</body>", 1)
        spliced.append(region)
    open(page_path, "w", encoding="utf-8").write(page)
    rc, out = sh("python3 knowledge/gen_provenance_receipt.py --mint %s" % page_path, root)
    print("6b. composed %s (%d bytes), spliced %s verbatim, re-minted rc=%d" % (
        os.path.relpath(page_path, root), len(open(page_path, encoding="utf-8").read().encode("utf-8")), spliced, rc))
    print("FIXTURE READY:", root)


if __name__ == "__main__":
    main()
