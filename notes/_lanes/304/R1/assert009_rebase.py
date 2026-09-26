"""R1 — ASSERT-009 re-base 137 -> 138, BY ADDITION, run LAST. The growth: knowledge/components/legend.meta.json
added at 108493b6 (#261 L, 2026-09-09) — the only *.meta.json added under knowledge/components since the #239
re-base (git log --diff-filter=A --since=2026-09-02). Measured in the clone AND re-measured on the target tree
here: refuses unless the live glob count is exactly 138 and dir entries exactly 142. README.md:13 updated in the
same change (the #207 pattern). Format round-trip verified byte-exact (json indent=1, ensure_ascii=False, no
trailing newline). Idempotent. Usage: <repo> [--write]"""
import json, glob, os, sys
repo = sys.argv[1]; write = "--write" in sys.argv
P = os.path.join(repo, "knowledge", "_assertions.json"); R = os.path.join(repo, "knowledge", "README.md")
n = len(glob.glob(os.path.join(repo, "knowledge", "components", "*.meta.json")))
e = len(os.listdir(os.path.join(repo, "knowledge", "components")))
assert (n, e) == (138, 142), f"live count {n} / entries {e} is not the measured 138 / 142 — STOP, re-measure"
s = open(P, encoding="utf-8").read(); d = json.loads(s)
assert json.dumps(d, indent=1, ensure_ascii=False) == s, "format round-trip not byte-exact"
a = [x for x in d["assertions"] if x["id"] == "ASSERT-009"][0] if isinstance(d, dict) and "assertions" in d else None
if a is None:
    a = [x for x in (d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))) if isinstance(x, dict) and x.get("id") == "ASSERT-009"][0]
if a["predicate"]["n"] == 138:
    print("ASSERT-009 already 138"); sys.exit(0)
assert a["predicate"]["n"] == 137
a["predicate"]["n"] = 138
old = "The component-spec KG is 137 files at knowledge/components/*.meta.json (the directory holds 141 entries"
assert old in a["claim"]
a["claim"] = a["claim"].replace(old, "The component-spec KG is 138 files at knowledge/components/*.meta.json (the directory holds 142 entries")
a["last_verified"] = "2026-09-26"
a["provenance"] += (" Re-based #304 R1 2026-09-26 (BY ADDITION; the growth is the #261 L chart legend — legend.meta.json @ 108493b6, "
    "2026-09-09 — whose wave skipped the regen serial's 'ASSERT-009 re-base if metas grew' step, so this assertion ABORTED "
    "CI's build at step [10] behind the help-gate for 17 days, unseen until #304 lane A4's full clone survey): 137 -> 138 "
    "measured in a full-history clone and on the target tree (glob knowledge/components/*.meta.json = 138). Dir entries "
    "141 -> 142, same four non-meta files. README updated same commit. Run LAST among the #304 Run 1 edits, per the plan.")
out = json.dumps(d, indent=1, ensure_ascii=False)
rs = open(R, encoding="utf-8").read()
ro = "`components/` (137 metas — count registered as ASSERT-009, re-tested not repeated)"
assert rs.count(ro) == 1, "README anchor"
rn = rs.replace(ro, "`components/` (138 metas — count registered as ASSERT-009, re-tested not repeated)")
print("ASSERT-009 137 -> 138", "WRITTEN" if write else "(dry run)")
if write:
    open(P, "w", encoding="utf-8").write(out); open(R, "w", encoding="utf-8").write(rn)
