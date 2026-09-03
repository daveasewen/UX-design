#!/usr/bin/env python3
"""L3 #245 — role-name RENAME, dry run only. `tpl-group-kpi/-chart/-rail` -> FLOATED `-lead/-evidence/-context`.
⛔ RENAMES NOTHING. The words are Dave's (v1.0.6 brief L3; s234-D4 'RE-CUT as role names', words not ruled).
Writes rename-grep-before.txt (every file + per-name counts, classified by what the file IS) and
rename-plan.json (the dry-run plan: which files a rename would EDIT, which would REGENERATE, which are
HISTORY and are never touched)."""
import json, os, re, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT = os.path.dirname(os.path.abspath(__file__))
OLD = ["tpl-group-kpi", "tpl-group-chart", "tpl-group-rail"]
NEW = {"tpl-group-kpi": "tpl-group-lead", "tpl-group-chart": "tpl-group-evidence", "tpl-group-rail": "tpl-group-context"}

def classify(rel):
    if rel.startswith("_to_delete/") or rel.startswith("archive/") or rel.startswith("_retired/"): return "ARCHIVE — never touched"
    if rel == "knowledge/snippets/Template-dashboard-bento.reference.html": return "SOURCE — the one hand-authored home (edit here, then regen)"
    if rel.startswith("knowledge/canon/canon.css"): return "GENERATED — projection of the snippet (gen_canon_components.py); regen, never edit"
    if rel.startswith("knowledge/_memento-index.json"): return "GENERATED — retrieval index; rebuilt by its own tool"
    if rel.startswith("knowledge/_TOKEN-FORK-LEDGER.json"): return "LEDGER — a dated record; leave, or by-addition note only"
    if rel.startswith("knowledge/_rulings.json"): return "RULINGS — Dave's words verbatim; NEVER edited"
    if rel.startswith("notes/_subreports/") or rel.startswith("notes/_briefs/"): return "HISTORY — filed reports/briefs (ADR-0017 / s192-D1); never re-edited"
    if rel.startswith("knowledge/_tmp/"): return "SCRATCH — wrap by-products; ignore"
    if rel in ("_CARRIES.md", "_LIVE-STATE-ARCHIVE.md", "_GM-ARCHIVE.md"): return "CONDUCTOR STATE — the conductor's, by addition at a wrap"
    if rel.startswith("reviews/"): return "REVIEW SURFACE — dated decision page; never re-edited"
    if rel.startswith("showroom/"): return "GENERATED — showroom (gen_showroom.py); regen"
    return "OTHER — read before deciding"

def main():
    pat = "|".join(OLD)
    r = subprocess.run(["grep", "-rIc", "-E", pat, ".", "--exclude-dir=.git", "--exclude-dir=__pycache__", "--exclude-dir=node_modules"], capture_output=True, text=True, cwd=ROOT)
    rows = []
    for line in r.stdout.splitlines():
        path, n = line.rsplit(":", 1)
        if int(n) == 0: continue
        rel = path[2:]
        txt = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
        per = {o: len(re.findall(re.escape(o) + r"(?![-a-z])", txt)) for o in OLD}
        rows.append({"file": rel, "lines_matching": int(n), "occurrences": per, "total": sum(per.values()), "class": classify(rel)})
    rows.sort(key=lambda x: (x["class"], x["file"]))
    # collision check for the floated words
    c = subprocess.run(["grep", "-rIl", "-E", "|".join(NEW.values()), ".", "--exclude-dir=.git", "--exclude-dir=__pycache__"], capture_output=True, text=True, cwd=ROOT)
    collisions = [p[2:] for p in c.stdout.splitlines() if not p[2:].startswith("knowledge/_tmp/l3-245/")]
    lines = ["RENAME GREP-BEFORE — %s (repo-wide, .git/__pycache__/node_modules excluded)" % " | ".join(OLD), ""]
    lines.append("%-4s %-6s %-6s %-6s  %-70s %s" % ("LINES", "kpi", "chart", "rail", "file", "class"))
    for x in rows:
        lines.append("%-5d %-6d %-6d %-6d  %-70s %s" % (x["lines_matching"], x["occurrences"]["tpl-group-kpi"], x["occurrences"]["tpl-group-chart"], x["occurrences"]["tpl-group-rail"], x["file"], x["class"]))
    tot = {o: sum(x["occurrences"][o] for x in rows) for o in OLD}
    lines += ["", "files: %d · occurrences: kpi %d · chart %d · rail %d · total %d" % (len(rows), tot["tpl-group-kpi"], tot["tpl-group-chart"], tot["tpl-group-rail"], sum(tot.values()))]
    by = {}
    for x in rows: by.setdefault(x["class"], []).append(x)
    lines.append("by class: " + " · ".join("%s %d file(s)/%d occ" % (k.split(" — ")[0], len(v), sum(y["total"] for y in v)) for k, v in sorted(by.items())))
    lines.append("floated words (%s) collide with existing text in: %s" % (", ".join(NEW.values()), collisions or "NOTHING (0 files outside this lane's scratch)"))
    open(os.path.join(OUT, "rename-grep-before.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    plan = {
        "$status": "DRY RUN — nothing renamed. The WORDS are Dave's; -lead/-evidence/-context are FLOATED (v1.0.6 brief L3).",
        "mapping_floated": NEW,
        "would_edit": [x["file"] for x in rows if x["class"].startswith("SOURCE")],
        "would_regenerate": [x["file"] for x in rows if x["class"].startswith("GENERATED")],
        "never_touch": [x["file"] for x in rows if x["class"].split(" — ")[0] in ("HISTORY", "RULINGS", "ARCHIVE", "REVIEW SURFACE", "SCRATCH", "LEDGER")],
        "conductor_by_addition": [x["file"] for x in rows if x["class"].startswith("CONDUCTOR")],
        "other_read_first": [x["file"] for x in rows if x["class"].startswith("OTHER")],
        "steps_if_ruled": [
            "1. Dave picks the three words (or others). Nothing before this.",
            "2. Edit ONLY knowledge/snippets/Template-dashboard-bento.reference.html: the 3 CSS rules (lines 737-739) and the 3 <section class> attributes (lines 840/901/946); keep the old class beside the new for one release if the pack must not break (by-addition), or cut clean — his call.",
            "3. Run the ORDERED regen serial (conductor, never a sub; never _build_all.py from a lane): gen_canon_components.py re-projects canon.css; gen_showroom.py; the memento index rebuild.",
            "4. grep-after: the three old names must remain ONLY in HISTORY/RULINGS/ARCHIVE files; 0 in SOURCE/GENERATED.",
            "5. The rails grouping dial's role_names.today/floated entries flip to the ruled words — derived, not edited.",
        ],
        "files": rows,
    }
    open(os.path.join(OUT, "rename-plan.json"), "w", encoding="utf-8").write(json.dumps(plan, indent=2) + "\n")
    print("\n".join(lines)); return 0

if __name__ == "__main__": sys.exit(main())
