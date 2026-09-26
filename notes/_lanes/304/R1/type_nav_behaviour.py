"""R1 lane 1b(ii) — step [38] component-partials sync. PREMISE (probed #304 R1): s234-D5 makes the
meta the one home and the #behaviour-manifest block DERIVED; but #261 N (c0225a0e) hand-edited the
derived block in three snippets instead of the metas. The blocks match the snippets' own
addEventListener sets (Navigations click+keydown · Sidebar-nav click+keydown · Tab-bar
click+keydown+resize); the metas do not (navigations untyped; tab-bar events lack keydown;
sidebar-nav/tab-bar fallback prose pre-dates #261 N). So the metas are typed FROM the blocks
(the newer truth), and the generator then re-derives the blocks byte-exact. Prior meta values kept
verbatim under `$r1_304` (by addition). Byte-exact round-trip of the meta format verified first
(json indent=2, ensure_ascii=False, trailing newline). Idempotent. Usage: <repo> [--write]"""
import json, re, sys, os
repo = sys.argv[1]; write = "--write" in sys.argv
K = os.path.join(repo, "knowledge")
RE = re.compile(r'<script[^>]*id="behaviour-manifest"[^>]*>(.*?)</script>', re.S)
FIELDS = ("script", "partial", "events", "fallback")
WHY = ("typed #304 R1 from the #behaviour-manifest block #261 N hand-authored in the snippet at c0225a0e "
       "(s234-D5: the meta is the one home, so the block's four address fields are carried here verbatim and the "
       "block is re-derived). events match the snippet's own addEventListener set.")
for slug, snip in (("navigations", "Navigations"), ("sidebar-nav", "Sidebar-nav"), ("tab-bar", "Tab-bar")):
    mp = os.path.join(K, "components", slug + ".meta.json")
    src = open(mp, encoding="utf-8").read()
    d = json.loads(src)
    assert json.dumps(d, indent=2, ensure_ascii=False) + "\n" == src, "round-trip not byte-exact: " + mp
    blk = json.loads(RE.search(open(os.path.join(K, "snippets", snip + ".reference.html"), encoding="utf-8").read()).group(1))
    want = {k: blk.get(k) for k in FIELDS}
    b = d.get("behaviour")
    if isinstance(b, dict) and {k: b.get(k) for k in FIELDS} == want:
        print(slug, "already typed from block"); continue
    if b is None:
        # insert after `relationships` (sidebar-nav / tab-bar position), never at the end
        nd = {}
        for k, v in d.items():
            nd[k] = v
            if k == "relationships":
                nd["behaviour"] = dict(want, **{"$r1_304": WHY})
        assert "behaviour" in nd
        d = nd
    else:
        prior = {k: b.get(k) for k in FIELDS if b.get(k) != want[k]}
        for k in FIELDS:
            b[k] = want[k]
        b["$r1_304"] = {"why": WHY, "before": prior}
    out = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    print(slug, "typed" if write else "would type", "| changed fields:", [k for k in FIELDS if (b or {}).get(k) is not None] if b is None else list(prior))
    if write:
        open(mp, "w", encoding="utf-8").write(out)
