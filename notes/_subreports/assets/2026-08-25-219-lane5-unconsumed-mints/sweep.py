#!/usr/bin/env python3
import os, re, sys, json, collections
ROOT = "/sessions/pensive-cool-galileo/mnt/UX-design"
sys.path.insert(0, os.path.join(ROOT, "knowledge/canon"))
canon = open(os.path.join(ROOT, "knowledge/canon/canon.css")).read()

# ---- 1. MINTED: every custom property declared inside a [data-apollo-theme] rule
# brace scanner so nested blocks are safe
def minted_by_theme(css):
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    out = collections.defaultdict(dict)   # var -> {theme: line}
    scopes = collections.defaultdict(set) # var -> set of selector-scope kinds
    stack, buf, line = [], [], 1
    i, n = 0, len(css)
    while i < n:
        c = css[i]
        if c == "\n": line += 1
        if c == "{":
            stack.append(("".join(buf).strip(), line)); buf=[]
        elif c == "}":
            body = "".join(buf); sel = " ".join(s for s,_ in stack)
            m = re.search(r'\[data-apollo-theme="([a-z-]+)"\]', sel)
            if m:
                theme = m.group(1)
                bl = stack[-1][1] if stack else line
                off = 0
                for mm in re.finditer(r"(--[\w-]+)\s*:", body):
                    ln = bl + body[:mm.start()].count("\n")
                    out[mm.group(1)].setdefault(theme, ln)
                    # scope kind: root tier vs component tier
                    scopes[mm.group(1)].add("component" if ".cn-" in sel else "root")
            buf=[]
            if stack: stack.pop()
        else:
            buf.append(c)
        i += 1
    return out, scopes

minted, scopes = minted_by_theme(canon)

# ---- 2. CONSUMERS: var(--x) anywhere outside reviews/ + excluded trees + emitting generators
EXCLUDE_DIRS = {".git","_to_delete","_retired","archive","reviews","_review","runs","outputs",
                "second-system-govuk","designer-skills-v1","designer-skills-v2","memento-package",
                "_DECISION-HISTORY","notes","node_modules","__pycache__","_GM-ARCHIVE"}
EXT = (".css",".html",".js",".py",".json",".md",".svg")
VARRE = re.compile(r"var\(\s*(--[\w-]+)")
used = collections.defaultdict(set)
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in EXCLUDE_DIRS]
    for f in fns:
        if not f.endswith(EXT): continue
        p = os.path.join(dp,f)
        try: txt = open(p, errors="ignore").read()
        except Exception: continue
        rel = os.path.relpath(p, ROOT)
        for v in set(VARRE.findall(txt)):
            used[v].add(rel)
GEN = ("knowledge/canon/gen_","knowledge/gen_","knowledge/_render/gen_")

# ---- 3. FALSE-POSITIVE CLASS: mint-time $alias consumption
import gen_theme_cascade as G
amap = G.alias_map()
alias_targets = set()
for path, al in amap.items():
    for k,v in al.items():
        alias_targets.add(v)
alias_target_vars = {}
for t in alias_targets:
    alias_target_vars.setdefault(G.var_name(t), set()).add(t)

orphans, aliasfp = [], []
for v, themes in sorted(minted.items()):
    real = {f for f in used.get(v,()) if not f.startswith(GEN)}
    if real: continue
    if v in alias_target_vars:
        aliasfp.append((v, themes, sorted(alias_target_vars[v])))
    else:
        orphans.append((v, themes))

print("MINTED per-theme vars examined: %d" % len(minted))
print("  zero var() consumers (outside reviews/ + generators): %d" % (len(orphans)+len(aliasfp)))
print("  MINUS mint-time $alias-target false positives:        %d" % len(aliasfp))
print("  GENUINE orphans:                                      %d" % len(orphans))
print()
print("=== FALSE-POSITIVE CLASS ($alias targets, consumed at mint time) ===")
for v, themes, paths in aliasfp:
    print("  %-46s %-30s %s" % (v, ",".join(sorted(themes)), paths[0]))
print()
print("=== GENUINE ORPHANS ===")
for v, themes in orphans:
    print("  %-46s %-24s tier=%s  %s" % (v, ",".join(sorted(themes)),
        "+".join(sorted(scopes[v])),
        " ".join("%s:%d"%(t,l) for t,l in sorted(themes.items()))))
fam = collections.Counter("-".join(v.lstrip("-").split("-")[:2]) for v,_ in orphans)
print("\nBY FAMILY:")
for k,n in fam.most_common(): print("  %-30s %d" % (k,n))
