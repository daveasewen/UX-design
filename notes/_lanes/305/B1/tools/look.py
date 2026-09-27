"""look.py <tag> — lane B1 (#305) renders + measures, on the canon fixtures (fix/<tag>/) and the raw
reference snippets (snippets dir given as argv[2]). 1440 wide. Writes renders/<tag>/*.png and
renders/<tag>/measure.json. Every number the calls are about is printed by the browser."""
import os, sys, json
from playwright.sync_api import sync_playwright
TAG = sys.argv[1]; SNIPS = os.path.abspath(sys.argv[2])
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIX = os.path.join(B, "fix", TAG); OUT = os.path.join(B, "renders", TAG); os.makedirs(OUT, exist_ok=True)
THEMES = ["mono", "common", "console", "supercharge"]; MODES = ["light", "dark"]
LIB = r"""
window.__b1 = (function(){
 const px = s => { const m = (s||'').match(/rgba?\(([^)]+)\)/); if(!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
 const lum = c => { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
 const over = (fg, bg) => ({r:fg.r*fg.a+bg.r*(1-fg.a), g:fg.g*fg.a+bg.g*(1-fg.a), b:fg.b*fg.a+bg.b*(1-fg.a), a:1});
 function ground(el){ const stack=[]; for(let e=el; e; e=e.parentElement){ const c=px(getComputedStyle(e).backgroundColor); if(c && c.a>0){ stack.push(c); if(c.a>=1) break; } }
   let g={r:255,g:255,b:255,a:1}; for(let i=stack.length-1;i>=0;i--) g=over(stack[i],g); return g; }
 function opac(el){ let o=1; for(let e=el; e; e=e.parentElement){ o*=parseFloat(getComputedStyle(e).opacity); } return o; }
 function contrast(el){ const cs=getComputedStyle(el); const c=px(cs.color); const g=ground(el); const fg=over({...c,a:c.a*opac(el)}, g);
   const L1=lum(fg), L2=lum(g); const hex=o=>'#'+[o.r,o.g,o.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join('');
   return {ratio:+((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)).toFixed(2), ink:hex(fg), ground:hex(g), color:cs.color, opacity:+opac(el).toFixed(3), size:cs.fontSize}; }
 function face(){ const cv=document.createElement('canvas').getContext('2d'); const s='Hamburgefonstiv 0123456789';
   cv.font='16px "Univers Next for HSBC", monospace'; const a=cv.measureText(s).width; cv.font='16px monospace'; const b=cv.measureText(s).width; return Math.abs(a-b)>1; }
 function eff(el){ return ground(el); }
 return {contrast, ground, face, px};
})();"""
def theme(pg, th, mode):
    pg.evaluate("""([th,m])=>{document.documentElement.setAttribute('data-apollo-theme',th);
      document.documentElement.setAttribute('data-theme',m); document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',m));}""", [th, mode])
    pg.wait_for_timeout(250)
M_KPI = r"""()=>{const rows=[]; const cv=document.createElement('canvas').getContext('2d');
 for(const t of [...document.querySelectorAll('.kpi-tile')].slice(0,4)){
  const l=t.querySelector('.kpi-lbl'), v=t.querySelector('.kpi-val'), p=t.querySelector('.kpi-per'); if(!l||!v) continue;
  const lr=l.getBoundingClientRect(), tr=t.getBoundingClientRect(); const cs=getComputedStyle(l);
  const rng=document.createRange(); rng.selectNodeContents(l); const ink=rng.getBoundingClientRect();
  // descender: paint check — the label's own box must contain the glyph's descent
  cv.font=cs.font; const m=cv.measureText(l.textContent.trim()); const base=ink.top + (ink.height - (m.fontBoundingBoxAscent+m.fontBoundingBoxDescent))/2 + m.fontBoundingBoxAscent;
  const spark=t.querySelector('.spark-inline');
  rows.push({lbl:l.textContent.trim().slice(0,22), tileH:+tr.height.toFixed(2), lblBoxH:+lr.height.toFixed(2),
   lbl_to_val_offsetTop:(v.offsetTop-l.offsetTop), overflowX:cs.overflowX, overflowY:cs.overflowY, textOverflow:cs.textOverflow,
   descBelowBox:+Math.max(0,(base+m.actualBoundingBoxDescent)-lr.bottom).toFixed(2), clipsY: cs.overflowY!=='visible',
   lbl:__b1.contrast(l), per:p?__b1.contrast(p):null, spark:spark?+spark.getBoundingClientRect().height.toFixed(1):null});
 }
 // ellipsis still works: force a long label on a clone
 const t0=document.querySelector('.kpi-tile .kpi-lbl'); let ell=null;
 if(t0){ const keep=t0.textContent; t0.textContent='A very long label that cannot possibly fit inside this tile at all, ever, gpy'; ell={scrollW:t0.scrollWidth, clientW:t0.clientWidth, truncates:t0.scrollWidth>t0.clientWidth}; t0.textContent=keep; }
 const first=document.querySelector('.kpi-tile'); const r=first.getBoundingClientRect();
 return {rows, ell, clip:{x:Math.max(0,r.left-8), y:Math.max(0,r.top-8+scrollY), width:Math.min(r.width+16,700), height:r.height+16}};}"""
M_BENTO = r"""()=>{const q=s=>document.querySelector(s); const bg=el=>el?__b1.ground(el):null; const hex=o=>o?'#'+[o.r,o.g,o.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join(''):null;
 const tile=q('.c-bento__tile'); const own=el=>el?getComputedStyle(el).backgroundColor:null;
 const kpis=[...document.querySelectorAll('.kpi-tile')].map(t=>({h:+t.getBoundingClientRect().height.toFixed(1), spark:t.querySelector('.spark-inline')?+t.querySelector('.spark-inline').getBoundingClientRect().height.toFixed(1):null}));
 const lbls=[...document.querySelectorAll('.kpi-tile .lbl16')].slice(0,2).map(e=>__b1.contrast(e));
 const rings=[...document.querySelectorAll('figure.dv[data-dv-type=donut], figure.dv[data-dv-type=pie]')].map(f=>{const t=f.closest('.c-bento__tile'); const s=f.querySelector('svg'); const row=t&&t.parentElement;
   return {tileW:t?+t.getBoundingClientRect().width.toFixed(1):null, tileH:t?+t.getBoundingClientRect().height.toFixed(1):null, figH:+f.getBoundingClientRect().height.toFixed(1), svgW:s?+s.getBoundingClientRect().width.toFixed(1):null, svgH:s?+s.getBoundingClientRect().height.toFixed(1):null, alignSelf:t?getComputedStyle(t).alignSelf:null}; });
 return {body:hex(bg(document.body)), bodyOwn:own(document.body), header:hex(bg(q('.tpl-header'))), headerOwn:own(q('.tpl-header')), page:hex(bg(q('.tpl-page'))), pageOwn:own(q('.tpl-page')), stack:hex(bg(q('.tpl-bento-stack'))), tile:hex(bg(tile)), tileOwn:own(tile), kpis, lbls, rings};}"""
M_SHELL = r"""()=>{const s=document.querySelector('.sh'); const g=[...document.querySelectorAll('.sn-group-label')].filter(e=>e.getBoundingClientRect().width>0).slice(0,1).map(e=>__b1.contrast(e));
 return {shellH:s?+s.getBoundingClientRect().height.toFixed(1):null, shellCss:s?getComputedStyle(s).height:null, group:g};}"""
M_NAV = r"""()=>[...document.querySelectorAll('.nv-count')].filter(e=>e.getBoundingClientRect().width>0).slice(0,8).map(e=>({t:e.textContent.trim(), w:+e.getBoundingClientRect().width.toFixed(2), pad:getComputedStyle(e).paddingLeft}))"""
M_NOTE = r"""()=>[...document.querySelectorAll('.note')].filter(e=>e.getBoundingClientRect().width>0).map(e=>{const cs=getComputedStyle(e); return {cls:e.className, bw:cs.borderTopWidth, bc:cs.borderTopColor, bs:cs.borderTopStyle, h:+e.getBoundingClientRect().height.toFixed(2), w:+e.getBoundingClientRect().width.toFixed(2)}; })"""
DENSE = r"""(n)=>{const figs=[...document.querySelectorAll('figure.dv')].filter(f=>/line|stacked/.test(f.getAttribute('data-dv-type')||''));
 const out=[]; for(const f of figs){ const sp=f.__dvSpec; if(!sp) { out.push({err:'no spec'}); continue; }
  const cats=[]; for(let i=0;i<n;i++) cats.push((i+1)+' Sep');
  const series=sp.series.slice(0,3).map((s,j)=>({name:s.name, values:cats.map((c,i)=>Math.round(40+20*j+12*Math.sin(i/3+j)+i*0.8))}));
  const spec=JSON.parse(JSON.stringify(sp)); spec.categories=cats; spec.series=series; if(spec.fn) delete spec.fn.domain;
  try{ window.dvRender(f, Object.assign({}, sp, {categories:cats, series:series})); }catch(e){ out.push({err:String(e).slice(0,200)}); continue; } }
 return out; }"""
COUNT = r"""()=>[...document.querySelectorAll('figure.dv')].filter(f=>/line|stacked/.test(f.getAttribute('data-dv-type')||'')).map(f=>{
  const painted=e=>{const c=getComputedStyle(e); return c.display!=='none'&&c.visibility!=='hidden'&&e.getBoundingClientRect().width>0;};
  const mk={}, lt={}, focus=f.querySelectorAll('g.dv-marker[tabindex]').length;
  f.querySelectorAll('.dv-mk').forEach(e=>{ if(!painted(e)) return; const g=e.closest('[data-series-group]'); const k=g?g.getAttribute('data-series-group'):(e.style.getPropertyValue('--sc')||'?'); mk[k]=(mk[k]||0)+1; });
  f.querySelectorAll('text.dv-barkey').forEach(e=>{ if(!painted(e)) return; const k=e.getAttribute('data-series-group'); lt[k]=(lt[k]||0)+1; });
  return {type:f.getAttribute('data-dv-type'), cats:(f.__dvSpec||{}).categories?f.__dvSpec.categories.length:null, markersBySeries:mk, lettersBySeries:lt, focusableMarkers:focus, tips:f.querySelectorAll('[data-tip]').length}; })"""
res = {}
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    def page(path, w=1440, h=1000, dsf=1, reduce=True):
        c = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=dsf, reduced_motion="reduce" if reduce else "no-preference")
        pg = c.new_page(); pg.goto("file://" + path); pg.wait_for_timeout(900); pg.evaluate(LIB); return c, pg
    # ---- face
    c, pg = page(os.path.join(FIX, "Kpi-tile.html")); res["face"] = pg.evaluate("__b1.face()"); c.close()
    # ---- call 5 / 10 / 41b: Kpi-tile (canon fixture), every theme x mode; 4x crops mono+common
    for th in THEMES:
        for m in MODES:
            c, pg = page(os.path.join(FIX, "Kpi-tile.html")); theme(pg, th, m); pg.wait_for_timeout(300)
            info = pg.evaluate(M_KPI); res["kpi-%s-%s" % (th, m)] = info; c.close()
            if th in ("mono", "common"):
                c, pg = page(os.path.join(FIX, "Kpi-tile.html"), dsf=4); pg.evaluate(LIB); theme(pg, th, m); pg.wait_for_timeout(300)
                i2 = pg.evaluate(M_KPI); pg.screenshot(path=os.path.join(OUT, "kpi-%s-%s-tile1-4x.png" % (th, m)), clip=i2["clip"], full_page=True); c.close()
    # the raw reference snippet too (the reviewed artefact itself)
    for m in MODES:
        c, pg = page(os.path.join(SNIPS, "Kpi-tile.reference.html")); theme(pg, "mono", m); res["kpi-snippet-%s" % m] = pg.evaluate(M_KPI)
        pg.screenshot(path=os.path.join(OUT, "kpi-snippet-%s-1440.png" % m), full_page=False); c.close()
    # ---- call 9 / 8 / 10 / 41b: the bento — raw snippet (has the page rule) + canon fixture
    for src, lab in ((os.path.join(SNIPS, "Template-dashboard-bento.reference.html"), "snippet"), (os.path.join(FIX, "Template-dashboard-bento.html"), "canon")):
        for th in (["mono"] if lab == "snippet" else THEMES):
            for m in MODES:
                c, pg = page(src, h=900); pg.add_style_tag(content=".demo-bar,.demo-controls{display:none!important}"); theme(pg, th, m); pg.wait_for_timeout(1500)
                res["bento-%s-%s-%s" % (lab, th, m)] = pg.evaluate(M_BENTO)
                if th in ("mono", "common"):
                    pg.screenshot(path=os.path.join(OUT, "bento-%s-%s-%s-1440.png" % (lab, th, m)), full_page=True)
                c.close()
    # ---- call 11 / 10: app shell (fixture) — shell height and group label
    for th in THEMES:
        for m in MODES:
            c, pg = page(os.path.join(FIX, "App-shell-side-nav.html")); theme(pg, th, m); res["shell-%s-%s" % (th, m)] = pg.evaluate(M_SHELL); c.close()
    for m in MODES:
        c, pg = page(os.path.join(FIX, "Sidebar-nav.html")); theme(pg, "common", m); res["sidebar-group-common-%s" % m] = pg.evaluate(M_SHELL); c.close()
    # ---- call 12: nav badge widths + 3x crop
    for nm in ("Sidebar-nav", "Navigations"):
        c, pg = page(os.path.join(FIX, nm + ".html"), dsf=3); pg.evaluate(LIB); res["badge-" + nm] = pg.evaluate(M_NAV)
        el = pg.locator(".nv-count").first
        try:
            bb = pg.evaluate("()=>{const e=[...document.querySelectorAll('.nv-count')].find(e=>e.getBoundingClientRect().width>0); const r=e.closest('a,li,button,.nv-item,.sn-item')||e.parentElement; const b=r.getBoundingClientRect(); return {x:Math.max(0,b.left-12),y:Math.max(0,b.top-12+scrollY),width:b.width+24,height:b.height+24};}")
            pg.screenshot(path=os.path.join(OUT, "badge-%s-3x.png" % nm), clip=bb, full_page=True)
        except Exception as e: res["badge-shot-err-" + nm] = str(e)[:120]
        c.close()
    # ---- call 26: notifications, every theme x mode
    for th in THEMES:
        for m in MODES:
            c, pg = page(os.path.join(FIX, "Notifications.html")); theme(pg, th, m); res["note-%s-%s" % (th, m)] = pg.evaluate(M_NOTE)
            if m == "light" or th in ("common", "supercharge"):
                pg.screenshot(path=os.path.join(OUT, "notes-%s-%s-1440.png" % (th, m)), full_page=True)
            c.close()
    # ---- call 7: dense series (30 points) injected through dvRender, light + dark
    for nm in ("Chart-line", "Chart-stacked-area"):
        for m in MODES:
            c, pg = page(os.path.join(FIX, nm + ".html")); theme(pg, "mono", m); pg.wait_for_timeout(600)
            errs = pg.evaluate(DENSE, 30); pg.wait_for_timeout(1500)
            res["dense-%s-%s" % (nm, m)] = {"errs": errs, "count": pg.evaluate(COUNT)}
            figs = pg.locator("figure.dv")
            for i in range(figs.count()):
                f = figs.nth(i)
                if not f.is_visible(): continue
                f.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
                f.screenshot(path=os.path.join(OUT, "dense-%s-%s-fig%d.png" % (nm, m, i)))
            c.close()
            # and the snippet's own (<=12 point) data, untouched
            c, pg = page(os.path.join(FIX, nm + ".html")); theme(pg, "mono", m); pg.wait_for_timeout(1200)
            res["own-%s-%s" % (nm, m)] = pg.evaluate(COUNT); c.close()
    br.close()
json.dump(res, open(os.path.join(OUT, "measure.json"), "w"), indent=1)
print("face", res["face"])
for k in sorted(res):
    if k.startswith(("kpi-mono-light","kpi-common-light","kpi-common-dark","kpi-snippet-light")): print(k, json.dumps(res[k]["rows"][:3])[:900], res[k].get("ell"))
for k in sorted(res):
    if k.startswith(("bento-", "shell-", "sidebar-", "badge-", "dense-", "own-")): print(k, json.dumps(res[k])[:700])
for k in ("note-mono-light","note-common-light","note-supercharge-dark","note-console-light"): print(k, json.dumps(res[k])[:900])
