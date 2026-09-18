#!/usr/bin/env python3
"""s282-D5 — _state.json: close W-282lr on the export + the ruling; open W-282ll for the
two things Dave did NOT settle (the 'Ask create' carry, and horizontal clear space)."""
import sys, json, pathlib
sys.path.insert(0, "/sessions/tender-hopeful-allen/mnt/UX-design/knowledge")
import _state as S

doc = S.load()
it = next(i for i in doc["items"] if i["id"] == "W-282lr")
assert it["state"] == "open", it["state"]
it["state"] = "done"
it["closed_by"] = (
    "notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json (his own export, "
    "2026-09-18T08:20:48.214Z: 12 rows, 9 answered, 3 moot under s282-D4, 4 notes, 3 "
    "overrules) + s282-D5, which inscribes every one of those answers. The exporter "
    "defects closed with s282-D4 (both were identifier files); the per-theme masthead "
    "default, the clear-space source, the hexagon-only permission, the guideline shape and "
    "the eight unreferenced lockups each have his answer and are enacted in #282 lane LL "
    "(notes/_subreports/2026-09-18-282-LL-logo-land.md)")
it["links"] = sorted(set(it["links"] + [
    "notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json",
    "notes/_subreports/2026-09-18-282-LL-logo-land.md",
    "knowledge/guidelines/logos.md",
    "W-282ll"]))

if not any(i["id"] == "W-282ll" for i in doc["items"]):
    S.add(doc,
        id="W-282ll",
        title=("#282 lane LL - the two things s282-D5 did NOT settle: the 'Ask create' "
               "re-integration carry, and HORIZONTAL logo clear space"),
        state="open", owner="dave", opened=282, project="apollo",
        condition="stated",
        closes_when=("Dave rules on BOTH: (1) whether the retired create.hsbc identifier "
                     "material is re-integrated as an AI-readable 'Ask create' assistant - "
                     "his own forward note on q6, filed by s282-D5 as a carry and not "
                     "enacted; and (2) what the HORIZONTAL digital clear space is, which "
                     "his q3 note does not state - logo26-009 rules the VERTICAL floor only "
                     "and says so in its own text"),
        home="notes/_subreports/2026-09-18-282-LL-logo-land.md",
        links=["notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json",
               "knowledge/guidelines/logos.md",
               "knowledge/_rulings.json",
               "W-282lr"],
        body=("TWO OPENS, ONE ITEM, BOTH HIS. (1) THE 'ASK CREATE' CARRY - his q6 note, "
              "verbatim: \"The identifier versions are placeholders for customised logos "
              "they aren't needed here, for our purposes. However in the future we will "
              "re-integrate this material as an AI readable version of create, we might "
              "have something like 'Ask create' assistant bot\". s282-D5 FILES this and does "
              "NOT enact it: no create.hsbc material is ingested, no assistant is built, no "
              "rule is written from it. (2) HORIZONTAL CLEAR SPACE - his q3 note says "
              "VERTICAL and nothing else: \"...so at 24 height we have 8px as the floor fer "
              "the vertical clearspace...\". logo26-009 rules the vertical floor (>= 0.25 x "
              "logo height snapped UP to the 4px grid: 24->8 28->8 32->8 36->12 40->12) and "
              "states in its own rule text that the horizontal axis is NOT stated and NOT "
              "ruled. It is NOT completed by symmetry - a designer has no horizontal figure "
              "to check against, and that is the honest shape until he says one. The PRINT "
              "rule (va25-014, 1x hexagon height on all sides) is unaffected and stays in "
              "visual-assets.md."))

ok, fails, rep = S.check(doc)
if not ok:
    print("REFUSED:"); [print("  -", f) for f in fails]; sys.exit(1)
S.save(doc)
print("W-282lr:", next(i["state"] for i in doc["items"] if i["id"] == "W-282lr"))
print("W-282ll:", next(i["state"] for i in doc["items"] if i["id"] == "W-282ll"))
print("counts:", {k: sum(1 for i in doc["items"] if i["state"] == k)
                  for k in sorted({i["state"] for i in doc["items"]})})
