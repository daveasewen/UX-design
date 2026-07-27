from playwright.sync_api import sync_playwright
import glob,os,json
REPO='/sessions/sharp-friendly-mayer/mnt/UX-design'
shell=glob.glob(os.environ['PLAYWRIGHT_BROWSERS_PATH']+'/chromium_headless_shell-*/chrome-linux/headless_shell')
# every element carrying a t-cm-*/t-ed-* class must compute to that composite's declared size+weight
JS = """() => {
  const decl = {};                       // composite -> {size, weight} as DECLARED in type.css
  for (const s of document.styleSheets) {
    let rules; try { rules = s.cssRules } catch(e) { continue }
    for (const r of rules) {
      if (!r.selectorText) continue;
      for (const sel of r.selectorText.split(',')) {
        const t = sel.trim();
        if (/^\\.t-(cm|ed)-[a-z0-9-]+$/.test(t) && r.style.fontSize)
          decl[t.slice(1)] = { size: r.style.fontSize, weight: r.style.fontWeight || '' };
      }
    }
  }
  if (!Object.keys(decl).length) return { fatal: 'NO COMPOSITE RULES VISIBLE — type.css did not load' };
  const bad = [];
  for (const el of document.querySelectorAll('[class*="t-cm-"],[class*="t-ed-"]')) {
    for (const c of el.classList) {
      const d = decl[c]; if (!d) continue;
      const cs = getComputedStyle(el);
      const wantW = d.weight ? String(parseInt(d.weight)) : null;
      const sizeBad = cs.fontSize !== d.size;
      const weightBad = wantW && cs.fontWeight !== wantW;
      if (sizeBad || weightBad)
        bad.push({ c, tag: el.tagName.toLowerCase(),
                   want: d.size + '/' + (d.weight || '-'), got: cs.fontSize + '/' + cs.fontWeight,
                   txt: (el.textContent || '').trim().slice(0, 24) });
    }
  }
  return { checked: document.querySelectorAll('[class*="t-cm-"],[class*="t-ed-"]').length, bad };
}"""
pages=sorted(glob.glob(REPO+'/showroom/*.html'))
pages=[p for p in pages if not p.endswith('index.html')]
tot=devs=0; report={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shell[0],headless=True,args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--allow-file-access-from-files"])
    pg=b.new_page(viewport={"width":1180,"height":900})
    for f in pages:
        name=os.path.basename(f)[:-5]
        try:
            pg.goto('file://'+f); pg.wait_for_timeout(320)
            fr=[x for x in pg.frames if x!=pg.main_frame]
            if not fr: continue
            r=fr[0].evaluate(JS)
        except Exception as e:
            report[name]=[{'c':'ERROR','want':'-','got':str(e)[:60],'txt':'','tag':''}]; continue
        if r.get('fatal'): report[name]=[{'c':'FATAL','want':'-','got':r['fatal'],'txt':'','tag':''}]; continue
        tot+=r['checked']
        if r['bad']:
            devs+=len(r['bad'])
            seen={}
            for x in r['bad']: seen.setdefault((x['c'],x['want'],x['got']),x)
            report[name]=list(seen.values())
    b.close()
print("PANES %d · composite-bound elements checked %d · DEVIATIONS %d in %d pane(s)\n"%(len(pages),tot,devs,len(report)))
for name,rows in sorted(report.items(), key=lambda kv:-len(kv[1]))[:14]:
    print("── %s (%d distinct)"%(name,len(rows)))
    for x in rows[:4]:
        print("     %-22s want %-10s got %-10s  %s"%(x['c'],x['want'],x['got'],x['txt']))
json.dump(report, open('/sessions/sharp-friendly-mayer/mnt/outputs/type-sweep.json','w'), indent=1)
