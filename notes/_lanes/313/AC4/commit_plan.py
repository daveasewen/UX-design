"""#313 AC4 — wave-3 commit plan: one commit per lane, each shared file in the LAST lane (in commit order) that
touches it, so no path is committed twice. Writes /tmp/ac4-plan/NN-<lane>.paths and the message files
notes/_lanes/313/AC4/_msg-<lane>.txt. Run at the repo root."""
import os, re
P = "knowledge/_tmp/313-patches"
ORDER = ["C3", "C4", "H3", "D4", "B6", "B5b", "A5", "A6", "B123", "B7", "N1nav", "N1nav-menus", "A2", "B5b-boxplot", "B4"]
LINE = {
 "C3": "Launchpad gates run as a service, with two fixtures and a selftest",
 "C4": "Launchpad chooser built over the mock catalogue",
 "H3": "Proposal page for Apollo Assembly and Studio, thirteen calls",
 "D4": "Metas, schema, verbs and explorer read the one edge register",
 "B6": "Third red traced and drawn; the a11y gate reads code, not comments",
 "B5b": "Fork picks built at source: hero sub-line and outline border follow the ink",
 "A5": "Component settles: tabs fill their container, QR theme variant removed, radius derivation wired",
 "A6": "Pack settles: fallback-drift gate blocks, focus ring on the library token, gallery kept",
 "B123": "Tree mark, today ring, double slider, rating and transfer list; the list-rows page",
 "B7": "Loose ends: dark roundels follow the ink, demo filters on one row, receipt page fixed",
 "N1nav": "Navigation answers: sections and panels, frame nav, mega menu, bottom edge, lock-up foot",
 "N1nav-menus": "The nine menus take the floating surface's bottom edge only",
 "A2": "Charts family one: stacked area grows, category cap ships, floor and template settle",
 "B5b-boxplot": "Boxplot grid binds data/grid/color at full alpha, as the bar chart does",
 "B4": "Split button on the square-corner token, radius gate tightened, with the canon regen",
}
REPORT = {"B5b": "notes/_subreports/2026-10-01-313-B5b-fork-picks.md", "N1nav-menus": "notes/_subreports/2026-10-01-313-N1nav.md",
          "B5b-boxplot": "notes/_subreports/2026-10-01-313-B5b-fork-picks.md"}
files = {}
for l in ORDER:
    txt = open(os.path.join(P, l + ".patch"), encoding="utf-8", errors="replace").read()
    files[l] = re.findall(r"(?m)^diff --git a/(\S+) b/", txt)
last = {}
for l in ORDER:
    for f in files[l]:
        last[f] = l
extra = {"B4": ["knowledge/canon/canon.css", "knowledge/_RADIUS-GATE.md"]}
os.makedirs("/tmp/ac4-plan", exist_ok=True)
for i, l in enumerate(ORDER, 1):
    mine = [f for f in files[l] if last[f] == l] + extra.get(l, [])
    moved = sorted({f for f in files[l] if last[f] != l})
    got = sorted({f for f in mine if f in files[l] and any(f in files[o] for o in ORDER if o != l)})
    msg = "notes/_lanes/313/AC4/_msg-%s.txt" % l
    mine.append(msg)
    open("/tmp/ac4-plan/%02d-%s.paths" % (i, l), "w").write("\n".join(mine) + "\n")
    body = ["Lane %s, cloud patch at base cdf17a12, landed by AC4 in #313 wave 3 (git apply --3way). Report: %s."
            % (l, REPORT.get(l, "notes/_subreports/2026-10-01-313-%s.md" % l))]
    if moved:
        body.append("Shared files this lane also edits ride in a later lane's commit: " + ", ".join(moved) + ".")
    if got:
        body.append("Carries other lanes' edits to shared files: " + ", ".join(got) + ".")
    if l == "A6":
        body.append("knowledge/_build_all.py: A5's and A6's appended steps were both kept (the one conflict, A5 first).")
    if l == "N1nav":
        body.append("dashboards/international-banking-dashboard.canon.html: N1nav's edits merged onto B7's by character (N1nav conflicted with B7 line by line; the merged file carries exactly N1nav's edit set).")
    if l == "B4":
        body.append("canon.css is the one regen of the whole wave (gen_canon_tokens, gen_snippet_tokens, gen_component_partials, gen_canon_components), so the radius-gate change and the canon regen land together; _RADIUS-GATE.md rewritten by _validate_radius.py.")
    body += ["", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
             "Claude-Session: https://claude.ai/code/session_01DWLoAT8tVg6mR7BDJTg6E8"]
    open(msg, "w").write(LINE[l] + " (lane " + l + ")\n\n" + "\n".join(body) + "\n")
    print("%02d %-12s %3d paths  moved-out %d" % (i, l, len(mine), len(moved)))
