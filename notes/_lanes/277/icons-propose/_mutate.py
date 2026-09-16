#!/usr/bin/env python3
"""_mutate.py — the mutation harness for gen_kg_icons.py (#277 lane RI).

A bite that cannot fail is not a test, and a mutation test proves the CLAUSE, not
the feature. Each mutant below is a one-line edit to the generator's source; the
harness runs `--selftest` against the mutant in an ISOLATED tree and records which
bites turned RED. Nothing in the repo is touched — the mutant lives under
<scratch>/mutroot/ and the directory is removed at the end.

A SURVIVING MUTANT IS A FINDING, not a rounding error: it means the generator can
do that wrong thing and every bite stays green.

    python3 notes/_lanes/277/icons-propose/_mutate.py [scratch-dir]
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
SRC = (LANE / "gen_kg_icons.py").read_text(encoding="utf-8")

MUTANTS = [
    ("M1", "the manifest record's fields are truncated instead of carried whole",
     '        attrs = {f: r.get(f) for f in ICON_FIELDS}',
     '        attrs = {f: (r.get(f)[:4] if isinstance(r.get(f), str) else r.get(f))\n'
     '                 for f in ICON_FIELDS}'),

    ("M2", "the group key is dropped from the icon node (the one fact the record never holds)",
     '        attrs["group"] = g',
     '        pass'),

    ("M3", "the -active-N suffix is ignored, so -active-2 looks like a base of its own",
     'ACTIVE_RX = re.compile(r"-active(-\\d+)?$")',
     'ACTIVE_RX = re.compile(r"-active$")'),

    ("M4", "an ORPHAN active invents the missing base node instead of declaring the gap",
     '        if base in slugs:\n'
     '            link(ICON + r["slug"], ICON + base, "activeVariantOf")',
     '        if True:\n'
     '            link(ICON + r["slug"], ICON + base, "activeVariantOf")'),

    ("M5", "a base with two or three -active glyphs is silently given a defaultActive edge",
     '    for b, v in sorted(multi.items()):\n'
     '        unresolved.append({',
     '    for b, v in sorted(multi.items()):\n'
     '        link(ICON + sorted(v)[0], ICON + b, "defaultActive")\n'
     '        unresolved.append({'),

    ("M6", "norm() is dropped, so the byte-match becomes whitespace-sensitive",
     '    return re.sub(r"\\s+", " ", d.strip())',
     '    return d'),

    ("M7", "the gate-drift assertion always says yes (a drifted _validate_icons.py goes unnoticed)",
     "    return ('re.sub(r\"\\\\s+\", \" \", d.strip())' in src",
     "    return True or ('re.sub(r\"\\\\s+\", \" \", d.strip())' in src"),

    ("M8", "a byte-matched snippet with no component is attached to a guessed component",
     '            if comp is None:\n'
     '                declare(None, "usesIcon",',
     '            if comp is None:\n'
     '                comp = sorted(metas)[0]\n'
     '            if False:\n'
     '                declare(None, "usesIcon",'),

    ("M9", "the PROSE route is drawn as usesIcon (the s274-D12 / s276-D5 refusal removed)",
     '        for comp, ic in sorted(comp_icon):\n'
     '            link("component:" + comp, ICON + ic, "usesIcon",',
     '        for _c, _m in metas.items():\n'
     '            _t = json.dumps(_m, ensure_ascii=False)\n'
     '            for _s in slugs:\n'
     '                if re.search(r"(?<![A-Za-z0-9])" + re.escape(_s) + r"(?![A-Za-z0-9])", _t):\n'
     '                    comp_icon.add((_c, _s))\n'
     '        for comp, ic in sorted(comp_icon):\n'
     '            link("component:" + comp, ICON + ic, "usesIcon",'),

    ("M10", "a .svg on disk but absent from the manifest is given a node anyway (B1 papered over)",
     '    stale = sorted(set(disk) - slugs)',
     '    stale = sorted(set(disk) - slugs)\n'
     '    for _s in stale:\n'
     '        add(ICON + _s, _s, slug=_s, file=disk[_s], group="UNKNOWN")\n'
     '        slugs.add(_s)'),

    ("M11", "a ruling that governs an unmanifested .svg invents the icon: node to hang the edge on",
     '            if stem in slugs:\n'
     '                ruled_pairs.append((stem, r["id"]))',
     '            if True:\n'
     '                ruled_pairs.append((stem, r["id"]))'),

    ("M12", "ruledBy fires on the DIRECTORY and the manifest, not only on a named .svg",
     "GOVERNS_ICON_RX = re.compile(r'(?:^|/)assets/icons/(?:.+/)?([^/]+)\\.svg$')",
     "GOVERNS_ICON_RX = re.compile(r'(?:^|/)assets/icons/(?:.+/)?([^/]*)')"),

    ("M13", "a malformed logo filename is given a node with the three fields guessed",
     '            continue\n'
     '        f = m.groupdict()',
     '            pass\n'
     '        f = m.groupdict() if m else {"lockup": stem, "theme": "light",\n'
     '                                     "colourMode": "colour"}'),

    ("M14", "defaultFor invents a theme: node so the arrow lands (fence 3 removed)",
     '            declare(LOGO + stem, "defaultFor",',
     '            link(LOGO + stem, "theme:" + logo_fields[stem]["theme"], "defaultFor")\n'
     '            declare(LOGO + stem, "defaultFor",'),

    ("M15", "defaultFor matches any lockup word rather than the exact filename stem",
     '    named = text_default(dr, logo_fields) if not no_logos else set()',
     '    named = ({s for s in logo_fields if s.split("-")[0] in (text or "")}\n'
     '             if not no_logos else set())'),

    ("M16", "the s230-D2 residue is quietly completed instead of declared",
     '        for slug in sorted(metas):\n'
     '            if slug.lower() in low and slug not in bound:',
     '        for slug in sorted(metas):\n'
     '            if False:'),

    ("M17", "themedBy is drawn from fillMode after all (613 identical edges)",
     '    fillmodes = {}',
     '    for _g, _r in recs:\n'
     '        if _r.get("fillMode") == "currentColor":\n'
     '            link(ICON + _r["slug"], "token:icon/default", "themedBy")\n'
     '    fillmodes = {}'),

    ("M18", "the RATIFIES allowlist is bypassed — any real ruling opens the door",
     '    if ratified not in RATIFIES:',
     '    if False:'),

    ("M19", "--land accepts any ratified string at all",
     '    if not ruling_exists(ratified, corpus):',
     '    if False:'),

    ("M20", "the landed files keep the dry run's PROPOSED / NOT RATIFIED text",
     '        pay["$description"] = (f"RATIFIED {name} under {ratified}',
     '        pay["$_unused"] = (f"RATIFIED {name} under {ratified}'),

    ("M21", "--dry-run leaks the landed files into the corpus",
     '    report["mode"] = "dry-run"',
     '    (_k(corpus) / LANDED_ICONS).write_text("{}\\n", encoding="utf-8")\n'
     '    report["mode"] = "dry-run"'),

    ("M22", "--icons-only still emits iconGroup nodes and inGroup edges",
     '    if not icons_only:\n'
     '        for g, lst in man.get("groups", {}).items():',
     '    if True:\n'
     '        for g, lst in man.get("groups", {}).items():'),

    ("M23", "--no-logos is ignored and the logo family ships anyway",
     '    stems = [] if no_logos else logo_stems(corpus)',
     '    stems = logo_stems(corpus)'),

    ("M24", "edge_status claims usesIcon already EXISTS in the live graph",
     'EDGE_STATUS = {t: "NEW" for t in EDGE_TYPES}',
     'EDGE_STATUS = {t: "NEW" for t in EDGE_TYPES}\nEDGE_STATUS["usesIcon"] = "EXISTS"'),

    ("M25", "the chip ships ON by default (the s274-D11 / #275 precedent broken)",
     '        "chip": {"family": FAMILY, "default": "OFF",',
     '        "chip": {"family": FAMILY, "default": "ON",'),
]

BITE_RX = re.compile(r"^\s*(ok|FAIL)\s+bite (\d+):", re.M)


def main():
    scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    root = scratch / "mutroot"
    (root / "knowledge").mkdir(parents=True, exist_ok=True)
    hg = LANE.parents[3] / "knowledge" / "_helpgate.py"
    if hg.exists():
        shutil.copy(hg, root / "knowledge" / "_helpgate.py")

    def run(text):
        (root / "gen_kg_icons.py").write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, str(root / "gen_kg_icons.py"), "--selftest"],
                           capture_output=True, text=True, timeout=600)
        out = r.stdout + r.stderr
        return sorted(int(n) for st, n in BITE_RX.findall(out) if st == "FAIL"), "Traceback" in out

    base_red, base_crash = run(SRC)
    print(f"BASELINE red={base_red} crashed={base_crash} — "
          f"{'PASS' if not base_red and not base_crash else 'BROKEN, fix before mutating'}\n")

    rows, survived = [], []
    for mid, desc, old, new in MUTANTS:
        if SRC.count(old) != 1:
            rows.append((mid, desc, f"PATCH-MISS (anchor x{SRC.count(old)})"))
            survived.append(mid)
            continue
        red, crashed = run(SRC.replace(old, new, 1))
        if red:
            v = "RED " + ",".join(map(str, red))
        elif crashed:
            v = "CRASH (the mutant did not even run)"
            survived.append(mid)
        else:
            v = "GREEN — THE MUTANT SURVIVED"
            survived.append(mid)
        rows.append((mid, desc, v))

    w = max(len(r[1]) for r in rows)
    for mid, desc, v in rows:
        print(f"  {mid:5s} {desc:{w}s} -> {v}")
    print("\n" + ("ALL MUTANTS CAUGHT" if not survived else f"SURVIVORS: {survived}"))
    shutil.rmtree(root, ignore_errors=True)
    return 1 if survived or base_red else 0


if __name__ == "__main__":
    sys.exit(main())
