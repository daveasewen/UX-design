import re, hashlib, json, glob, os
res={}
for i in (1,2,3):
    root=f'/home/claude/cr/G{i}/Apollo-Spider-v1.0.15'; html=open(f'{root}/out/dashboard.html').read()
    scopes=sorted(set(re.findall(r'class="[^"]*?\b(cn-[a-z0-9-]+)', html)))
    # script blocks
    scripts=re.findall(r'<script(?![^>]*application/json)[^>]*>(.*?)</script>', html, re.S)
    sh=[hashlib.sha256(s.strip().encode()).hexdigest() for s in scripts]
    # pack sources: snippet script blocks + canon js files
    src={}
    for f in glob.glob(f'{root}/knowledge/snippets/*.html')+glob.glob(f'{root}/knowledge/canon/*.js'):
        t=open(f,errors='ignore').read()
        blocks=[t] if f.endswith('.js') else re.findall(r'<script(?![^>]*application/json)[^>]*>(.*?)</script>', t, re.S)
        for b in blocks: src.setdefault(hashlib.sha256(b.strip().encode()).hexdigest(), os.path.relpath(f,root))
    matched=[(len(s), src[h]) for s,h in zip(scripts,sh) if h in src]
    # dv-behaviour substring check
    dvb=open(f'{root}/knowledge/canon/dv-behaviour.js').read() if os.path.exists(f'{root}/knowledge/canon/dv-behaviour.js') else ''
    charts=re.findall(r'class="[^"]*\b(cn-chart-[a-z-]+)', html)
    res[f'G{i}']=dict(scopes=scopes, nscopes=len(scopes), scripts=len(scripts), script_bytes=[len(s) for s in scripts],
        verbatim_matches=matched, dv_behaviour_verbatim=(dvb.strip() in html) if dvb else None,
        dvRender_calls=len(re.findall(r'dvRender\(',html)), charts=sorted(set(charts)), chart_count=len(charts),
        hardcoded_svg_paths=len(re.findall(r'<path d="M',html)), bytes=len(html))
json.dump(res,open('/home/claude/cr/m/inventory.json','w'),indent=1)
for g,v in res.items(): print(g, json.dumps(v)[:1500]); print()
