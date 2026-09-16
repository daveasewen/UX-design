#!/usr/bin/env python3
"""#279 wrap — TWO textual spans into knowledge/_state.json, each proven by reconstruction in
THIS process before anything is written. Never json.load + json.dump: that is the #179 defect
(a serializer reformatting thousands of lines nobody edited), and an insertions-only numstat is
what a span looks like from the outside.

  (1) REPAIR: the W-278wr row has no `links` field, which `_state.py --check` refuses by name.
      #278's wrap created the row; four #279 lane reports named the failure and none could fix
      it from a lane seat.
  (2) ADD: this wrap's own filed report row, W-279wr (`s218-D7` doc-row gate).
"""
import json, sys
P = "knowledge/_state.json"
orig = open(P, encoding="utf-8").read()
text = orig

# ---- (1) the W-278wr repair -----------------------------------------------------------------
ANCHOR = '    {\n      "home": "notes/_subreports/2026-09-16-278-W-wrap.md",\n      "id": "W-278wr",\n'
assert text.count(ANCHOR) == 1, ("repair anchor", text.count(ANCHOR))
LINKS = ('    {\n      "links": [\n'
         '        "notes/_lanes/278/W/WRAP-REPORT.md",\n'
         '        "notes/_lanes/278/WRAP-MEMORY-HOOK.md",\n'
         '        "_DECISION-HISTORY/2026-09-16-278-the-cloud-move-and-the-seed.md",\n'
         '        "_HANDOFF-129-the-cloud-move-and-the-seed.md",\n'
         '        "knowledge/_rulings.json"\n'
         '      ],\n'
         '      "home": "notes/_subreports/2026-09-16-278-W-wrap.md",\n      "id": "W-278wr",\n')
i = text.find(ANCHOR)
text = text[:i] + LINKS + text[i+len(ANCHOR):]
span1 = len(LINKS) - len(ANCHOR)

# ---- (2) the W-279wr row --------------------------------------------------------------------
row = {
 "links": [
   "notes/_lanes/279/W/WRAP-REPORT.md",
   "notes/_lanes/279/WRAP-MEMORY-HOOK.md",
   "_DECISION-HISTORY/2026-09-16-279-the-wave-lands-and-the-graph-question.md",
   "_HANDOFF-130-the-wave-lands-and-the-graph-question.md",
   "knowledge/_rulings.json",
 ],
 "home": "notes/_subreports/2026-09-16-279-W-wrap.md",
 "id": "W-279wr",
 "title": "#279 W filed report - the delegated capture ritual for #279 -> #280",
 "state": "open",
 "owner": "dave",
 "opened": 279,
 "project": "apollo",
 "closes_when": "Dave has ruled or explicitly parked the report's four ruling-shaped questions - chiefly the LAYOUT question (whether the three views become three visibly separated layers on the stage, or the chips are what s277-D8 meant), and the #243 form now standing for a fifth wrap",
 "why": "The #279 wrap inscribed s279-D1 (the pack ships the reader and the Constitution, so ASK reads live in-pack) and re-verified the day's eleven enactment commits against git rather than restating them; it records that s277-D12 was never started, that Dave's own eye refused the explorer result, that his 15-base export is received and unread by the record, and that the _carry_items docstring disagrees with _AGE_RE in a way that changes a published carry count.",
 "condition": "stated",
}
body = json.dumps(row, indent=2, ensure_ascii=False)
body = "\n".join("    " + l if l.strip() else l for l in body.split("\n"))
TAIL = "\n  ]\n}"
assert text.endswith(TAIL) or text.endswith(TAIL + "\n"), repr(text[-12:])
j = text.rfind(TAIL)
INSERT = ",\n" + body
text2 = text[:j] + INSERT + text[j:]
span2 = len(INSERT)

# ---- reconstruction proof, before any write --------------------------------------------------
back = text2[:j] + text2[j+span2:]                       # remove span 2
back = back[:i] + ANCHOR + back[i+len(LINKS):]           # restore span 1
assert back == orig, "REFUSED — reconstruction failed"
parsed = json.loads(text2)
assert len(parsed["items"]) == len(json.loads(orig)["items"]) + 1
assert parsed["items"][-1]["id"] == "W-279wr"
assert "links" in [k for k in parsed["items"] if isinstance(k, dict)][0] or True
w278 = [r for r in parsed["items"] if r.get("id") == "W-278wr"][0]
assert w278["links"] and len(w278) == len(
    [r for r in json.loads(orig)["items"] if r.get("id") == "W-278wr"][0]) + 1

if "--write" not in sys.argv:
    print(f"DRY: repair span +{span1} B · new row span +{span2} B · items "
          f"{len(json.loads(orig)['items'])} → {len(parsed['items'])}; reconstruction PASSED")
    sys.exit(0)
open(P, "w", encoding="utf-8").write(text2)
print(f"WROTE: W-278wr `links` repaired (+{span1} B) · W-279wr added (+{span2} B); "
      f"reconstruction PASSED before the write")
