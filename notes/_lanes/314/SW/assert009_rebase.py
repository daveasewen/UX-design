"""#314 lane SW — ASSERT-009 re-base 139 -> 143, BY ADDITION. The growth: four member metas,
knowledge/components/{switch,checkbox,radio,chip}.meta.json, the selection-controls family split into four
parts on Dave's word (s313-D56, 23:17 Thu 2026-10-01: "Four parts (the recommendation)"). The family meta
stays, so the count rises by four. Also corrects the claim's directory figure, which was already stale: #312
lane L2 added knowledge/components/extract_spec.py, so the directory held 144 entries (five non-meta files),
not 143; after the split it holds 148. Same shape as notes/_lanes/309/cond/assert009_rebase.py.
Refuses unless the live glob count is exactly 143 and dir entries exactly 148. README.md:13 updated in the
same change. Format round-trip byte-exact. Idempotent. Usage: <repo> [--write]"""
import json, glob, os, sys
repo = sys.argv[1]; write = "--write" in sys.argv
P = os.path.join(repo, "knowledge", "_assertions.json"); R = os.path.join(repo, "knowledge", "README.md")
n = len(glob.glob(os.path.join(repo, "knowledge", "components", "*.meta.json")))
e = len(os.listdir(os.path.join(repo, "knowledge", "components")))
assert (n, e) == (143, 148), f"live count {n} / entries {e} is not the measured 143 / 148 — STOP, re-measure"
s = open(P, encoding="utf-8").read(); d = json.loads(s)
assert json.dumps(d, indent=1, ensure_ascii=False) == s, "format round-trip not byte-exact"
items = d["assertions"]
a = [x for x in items if isinstance(x, dict) and x.get("id") == "ASSERT-009"][0]
if a["predicate"]["n"] == 143:
    print("ASSERT-009 already 143"); sys.exit(0)
assert a["predicate"]["n"] == 139
a["predicate"]["n"] = 143
old = ("The component-spec KG is 139 files at knowledge/components/*.meta.json (the directory holds 143 entries - "
       "the other four are meta.schema.json, _ACCESSIBILITY-CONFORMANCE.md, _nodes-context.json and _nodes-pattern.json;")
assert old in a["claim"]
a["claim"] = a["claim"].replace(old, (
    "The component-spec KG is 143 files at knowledge/components/*.meta.json (the directory holds 148 entries - "
    "the other five are meta.schema.json, _ACCESSIBILITY-CONFORMANCE.md, _nodes-context.json, _nodes-pattern.json "
    "and extract_spec.py;"))
a["last_verified"] = "2026-10-02"
a["provenance"] += (" Re-based #314 lane SW 2026-10-02 (BY ADDITION; the growth is Dave's s313-D56, 'Four parts (the "
    "recommendation)', 23:17 Thu 2026-10-01): 139 -> 143 measured on the tree (glob knowledge/components/*.meta.json "
    "= 143) — switch, checkbox, radio and chip each became a meta of their own; the selection-controls family meta "
    "stays (its snippet, its role and its catalogue entry), so the count rose by four. Dir entries 143 -> 148: the "
    "claim's 143 was already stale by one since #312 lane L2 added extract_spec.py (144 measured before the split), "
    "corrected here and named in the claim. README updated same change. Script: notes/_lanes/314/SW/assert009_rebase.py.")
out = json.dumps(d, indent=1, ensure_ascii=False)
rs = open(R, encoding="utf-8").read()
ro = "`components/` (139 metas — count registered as ASSERT-009, re-tested not repeated)"
assert rs.count(ro) == 1, "README anchor"
rn = rs.replace(ro, "`components/` (143 metas — count registered as ASSERT-009, re-tested not repeated)")
print("ASSERT-009 139 -> 143", "WRITTEN" if write else "(dry run)")
if write:
    open(P, "w", encoding="utf-8").write(out); open(R, "w", encoding="utf-8").write(rn)
