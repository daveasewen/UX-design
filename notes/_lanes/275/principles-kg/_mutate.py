#!/usr/bin/env python3
"""_mutate.py — the mutation harness for knowledge/gen_kg_principles.py (#275 lane RP).

A bite that cannot fail is not a test, and a mutation test proves the CLAUSE, not
the feature. Each mutant below is a one-line edit to the generator's source; the
harness runs `--selftest` against the mutant in an ISOLATED tree and records which
bites turned RED. Nothing in the repo is touched — the mutant lives under
<scratch>/mutroot/knowledge/ and the directory is removed at the end.

    python3 notes/_lanes/275/principles-kg/_mutate.py [scratch-dir]
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
SRC = (REPO / "knowledge" / "gen_kg_principles.py").read_text(encoding="utf-8")

MUTANTS = [
    ("M1", "statement is truncated instead of carried whole",
     '            attrs[f] = p.get(f)',
     '            attrs[f] = (p.get(f) or "")[:40] if f == "statement" else p.get(f)'),

    ("M2", "derive_pairs drops the different-sides rule (the freshness proof goes blind)",
     '            if a.get("role") != b.get("role"):',
     '            if True:'),

    ("M3", "tensionWith stops carrying polarity + mediatingVariable",
     '             polarity=e["polarity"], mediatingVariable=e.get("mediating_variable"),\n'
     '             fromKind=e.get("from_kind"), toKind=e.get("to_kind"))',
     '             )'),

    ("M4", "any link type is accepted (the s238-D6 refusal removed)",
     '            if ty not in LINK_TYPES:',
     '            if False:'),

    ("M5", "a link to an unheld ruling invents the ruling: node",
     '            if ref in rids:\n'
     '                link(pid, "ruling:" + ref, ty, note=(l.get("quote") or "")[:300])',
     '            if True:\n'
     '                link(pid, "ruling:" + ref, ty, note=(l.get("quote") or "")[:300])'),

    ("M6", "a declared stub becomes an invented stub: node",
     '            elif ref in stubs:\n'
     '                declare(pid, "hasParty",',
     '            elif ref in stubs:\n'
     '                link(pid, add("stub:" + ref, ref), "hasParty")\n'
     '            elif False:\n'
     '                declare(pid, "hasParty",'),

    ("M7", "an edgeless polarity is dropped silently",
     '        if p["id"] not in with_edges:',
     '        if False:'),

    ("M8", "--no-polarity-nodes still emits the polarity-sourced edges",
     '            if not polarity_nodes:\n'
     '                continue\n'
     '            if ref in pids:',
     '            if False:\n'
     '                continue\n'
     '            if ref in pids:'),

    ("M9", "family edges are on by default (build signature flipped)",
     'def build(corpus=None, family_edges=False, evidence_edges=False,',
     'def build(corpus=None, family_edges=True, evidence_edges=False,'),

    ("M10", "grade is moved onto an edge too (s237-D1 says it is a field)",
     '        if family_edges:\n'
     '            link(UX + p["id"], add("family:" + str(p["family"]), str(p["family"])), "inFamily")',
     '        if family_edges:\n'
     '            link(UX + p["id"], add("family:" + str(p["family"]), str(p["family"])), "inFamily")\n'
     '            attrs.pop("grade", None); nodes[UX + p["id"]].pop("grade", None)\n'
     '            link(UX + p["id"], add("grade:" + str(p["grade"]), str(p["grade"])), "hasGrade")'),

    ("M11", "--land accepts any ratified string",
     '    if not ruling_exists(ratified, rulings_path):',
     '    if False:'),

    ("M12", "the landed file keeps the dry run's PROPOSED / NOT RATIFIED text",
     '    payload["$description"] = (f"RATIFIED ux: principle nodes',
     '    payload["$_unused"] = (f"RATIFIED ux: principle nodes'),

    ("M13", "--land also rewrites principles.json",
     '    out = _k(corpus) / LANDED\n'
     '    out.write_text(',
     '    (_k(corpus) / "brain" / "principles.json").write_text("{\\"principles\\": []}\\n", encoding="utf-8")\n'
     '    out = _k(corpus) / LANDED\n'
     '    out.write_text('),

    ("M14", "--dry-run leaks the landed file into the corpus",
     '    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n'
     '    return report',
     '    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\\n", encoding="utf-8")\n'
     '    (_k(corpus) / LANDED).write_text("{}\\n", encoding="utf-8")\n'
     '    return report'),

    ("M15", "edge_status claims tensionWith already EXISTS",
     'EDGE_STATUS["evidencedBy"] = "EXISTS"',
     'EDGE_STATUS["evidencedBy"] = "EXISTS"\nEDGE_STATUS["tensionWith"] = "EXISTS"'),

    ("M16", "the WCAG join is drawn by name match (the s274-D12 refusal removed)",
     '        add(UX + p["id"], p["id"], **attrs)',
     '        add(UX + p["id"], p["id"], **attrs)\n'
     '        for _w, _n in (("perceivable", "1"), ("operable", "2"),\n'
     '                       ("understandable", "3"), ("robust", "4")):\n'
     '            if _w in p["id"]:\n'
     '                link(UX + p["id"], "principle:" + _n, "tensionWith")'),

    ("M17", "gradeName is retyped in the generator instead of read from s237-D1's map",
     '    m = GRADE_NAMES_RX.search(p.read_text(encoding="utf-8"))\n'
     '    if not m:\n'
     '        return {}, False',
     '    m = GRADE_NAMES_RX.search(p.read_text(encoding="utf-8"))\n'
     '    if not m:\n'
     '        return {"A": "REPLICATED", "B": "STUDIED", "C": "PRACTISED",\n'
     '                "D": "DEBUNKED", "L": "OBLIGATION"}, True'),

    ("M18", "a ruling party is resolved as a ux: node",
     '            elif ref in rids:\n'
     '                link(pid, "ruling:" + ref, "hasParty", note=tag, role=pa.get("role"))',
     '            elif ref in rids:\n'
     '                link(pid, UX + ref, "hasParty", note=tag, role=pa.get("role"))'),
]

BITE_RX = re.compile(r"^\s*(ok|FAIL)\s+bite (\d+):", re.M)


def main():
    scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    root = scratch / "mutroot" / "knowledge"
    root.mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO / "knowledge" / "_helpgate.py", root / "_helpgate.py")
    shutil.copy(REPO / "knowledge" / "_rulings.json", root / "_rulings.json")

    def run(text):
        (root / "gen_kg_principles.py").write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, str(root / "gen_kg_principles.py"), "--selftest"],
                           capture_output=True, text=True, timeout=300)
        out = r.stdout + r.stderr
        return sorted(int(n) for st, n in BITE_RX.findall(out) if st == "FAIL"), "Traceback" in out

    base_red, base_crash = run(SRC)
    print(f"BASELINE red={base_red} crashed={base_crash} — "
          f"{'PASS' if not base_red and not base_crash else 'BROKEN, fix before mutating'}\n")

    rows, survived = [], []
    for mid, desc, old, new in MUTANTS:
        if SRC.count(old) != 1:
            rows.append((mid, desc, f"PATCH-MISS (anchor x{SRC.count(old)})")); survived.append(mid); continue
        red, crashed = run(SRC.replace(old, new, 1))
        if red:
            v = "RED " + ",".join(map(str, red))
        elif crashed:
            v = "CRASH (the mutant did not even run)"; survived.append(mid)
        else:
            v = "GREEN — THE MUTANT SURVIVED"; survived.append(mid)
        rows.append((mid, desc, v))

    w = max(len(r[1]) for r in rows)
    for mid, desc, v in rows:
        print(f"  {mid:5s} {desc:{w}s} -> {v}")
    print("\n" + ("ALL MUTANTS CAUGHT" if not survived else f"SURVIVORS: {survived}"))
    shutil.rmtree(scratch / "mutroot", ignore_errors=True)
    return 1 if survived or base_red else 0


if __name__ == "__main__":
    sys.exit(main())
