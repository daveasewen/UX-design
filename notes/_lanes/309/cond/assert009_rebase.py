"""#309 conductor — ASSERT-009 re-base 138 -> 139, BY ADDITION. The growth: knowledge/components/metric.meta.json
added at 879f9aae (#309 lane C), Dave's own ruled Metric (s308-D42, s309-D2) — the only *.meta.json added under
knowledge/components since the #304 re-base. Lane C skipped the regen serial's 'ASSERT-009 re-base if metas grew'
step, so CI's build ABORTED at step [10] on the push 528e8318 (run read by _ci_readback.py 2026-09-30).
Refuses unless the live glob count is exactly 139 and dir entries exactly 143. README.md:13 updated in the same
change (the #207 pattern). Format round-trip byte-exact. Idempotent. Usage: <repo> [--write]"""
import json, glob, os, sys
repo = sys.argv[1]; write = "--write" in sys.argv
P = os.path.join(repo, "knowledge", "_assertions.json"); R = os.path.join(repo, "knowledge", "README.md")
n = len(glob.glob(os.path.join(repo, "knowledge", "components", "*.meta.json")))
e = len(os.listdir(os.path.join(repo, "knowledge", "components")))
assert (n, e) == (139, 143), f"live count {n} / entries {e} is not the measured 139 / 143 — STOP, re-measure"
s = open(P, encoding="utf-8").read(); d = json.loads(s)
assert json.dumps(d, indent=1, ensure_ascii=False) == s, "format round-trip not byte-exact"
items = d["assertions"] if isinstance(d, dict) and "assertions" in d else (d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list)))
a = [x for x in items if isinstance(x, dict) and x.get("id") == "ASSERT-009"][0]
if a["predicate"]["n"] == 139:
    print("ASSERT-009 already 139"); sys.exit(0)
assert a["predicate"]["n"] == 138
a["predicate"]["n"] = 139
old = "The component-spec KG is 138 files at knowledge/components/*.meta.json (the directory holds 142 entries"
assert old in a["claim"]
a["claim"] = a["claim"].replace(old, "The component-spec KG is 139 files at knowledge/components/*.meta.json (the directory holds 143 entries")
a["last_verified"] = "2026-09-30"
a["provenance"] += (" Re-based #309 conductor 2026-09-30 (BY ADDITION; the growth is Dave's own ruled Metric — metric.meta.json "
    "@ 879f9aae, #309 lane C, s308-D42 and s309-D2 — whose lane skipped the regen serial's 'ASSERT-009 re-base if metas grew' "
    "step, so this assertion ABORTED CI's build at step [10] on the push 528e8318): 138 -> 139 measured on the tree at the seat "
    "(glob knowledge/components/*.meta.json = 139). Dir entries 142 -> 143, same four non-meta files. README updated same commit. "
    "stat-card and kpi-tile keep their meta files as alias seats, so the count rose by one, not fell.")
out = json.dumps(d, indent=1, ensure_ascii=False)
rs = open(R, encoding="utf-8").read()
ro = "`components/` (138 metas — count registered as ASSERT-009, re-tested not repeated)"
assert rs.count(ro) == 1, "README anchor"
rn = rs.replace(ro, "`components/` (139 metas — count registered as ASSERT-009, re-tested not repeated)")
print("ASSERT-009 138 -> 139", "WRITTEN" if write else "(dry run)")
if write:
    open(P, "w", encoding="utf-8").write(out); open(R, "w", encoding="utf-8").write(rn)
