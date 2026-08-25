#!/usr/bin/env python3
import os, re, collections
ROOT = "/sessions/pensive-cool-galileo/mnt/UX-design"
canon = open(os.path.join(ROOT, "knowledge/canon/canon.css")).read()
theme_block = re.compile(r'\[data-apollo-theme="([a-z-]+)"\][^{]*\{([^}]*)\}', re.S)
minted = collections.defaultdict(dict)
for m in theme_block.finditer(canon):
    theme, body = m.group(1), m.group(2)
    base = canon[:m.start()].count("\n") + 1
    for mm in re.finditer(r"(--[\w-]+)\s*:", body):
        minted[mm.group(1)].setdefault(theme, base + body[:mm.start()].count("\n") + 1)

EXCLUDE = ("/_to_delete/", "/_retired/", "/archive/", "/reviews/", "/_review/", "/runs/",
           "/outputs/", "/second-system-govuk/", "/designer-skills-v", "/memento-package/",
           "/_DECISION-HISTORY/", "/notes/", "/_GM-ARCHIVE", "/_LIVE-STATE-ARCHIVE",
           "/.git/", "/_fitness-test/register-spread")
EXT = (".css", ".html", ".js", ".py", ".json", ".md")
used = collections.defaultdict(set)
VARRE = re.compile(r"var\(\s*(--[\w-]+)")
for dirpath, dirnames, files in os.walk(ROOT):
    if any(e.strip("/") in dirpath.split(os.sep) for e in (".git",)):
        dirnames[:] = []
        continue
    for f in files:
        p = os.path.join(dirpath, f)
        if not p.endswith(EXT) or any(e in p for e in EXCLUDE):
            continue
        try:
            txt = open(p, errors="ignore").read()
        except Exception:
            continue
        for v in set(VARRE.findall(txt)):
            used[v].add(os.path.relpath(p, ROOT))

GENERATORS = ("knowledge/canon/gen_", "knowledge/gen_", "knowledge/_render/gen_")
orphans = []
for v, themes in sorted(minted.items()):
    real = {f for f in used.get(v, ()) if not f.startswith(GENERATORS)}
    if not real:
        orphans.append((v, themes))
print("MINTED per-theme vars examined: %d" % len(minted))
print("WITH ZERO CONSUMERS outside reviews/ (and outside the emitting generators): %d\n" % len(orphans))
fam = collections.Counter()
for v, themes in orphans:
    fam["-".join(v.lstrip("-").split("-")[:2])] += 1
    print("  %-48s %s" % (v, ", ".join("%s canon.css:%d" % (t, l) for t, l in sorted(themes.items()))))
print("\nBY FAMILY:")
for k, n in fam.most_common():
    print("  %-28s %d" % (k, n))
