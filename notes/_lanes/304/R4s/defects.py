"""defects.py — R4s (#304): measure, in each run's rendered overview (1440 light, Common, as the run ships),
(a) the bento gutter Common actually gets, (d) contrast of the KPI label and the side-nav group label,
(f) KPI label ink clipped (descenders). Writes views/<run>/defects.json. Seat env in the same call."""
import functools, http.server, json, os, socketserver, sys, threading, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); STAGE = os.path.join(os.environ["HOME"], "r4c", "stage")
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
JS = r"""() => {
 const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(x=>parseFloat(x)); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
 const lum = c => { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
 const bgOf = el => { let stack=[]; for (let e=el; e; e=e.parentElement) { const c=parse(getComputedStyle(e).backgroundColor); if (c && c.a>0) { stack.push(c); if (c.a>=1) break; } }
   let out={r:255,g:255,b:255}; for (let i=stack.length-1;i>=0;i--){ const c=stack[i]; out={r:c.r*c.a+out.r*(1-c.a), g:c.g*c.a+out.g*(1-c.a), b:c.b*c.a+out.b*(1-c.a)}; } return out; };
 const cr = el => { const s=getComputedStyle(el); let f=parse(s.color); const b=bgOf(el); if (f.a<1) f={r:f.r*f.a+b.r*(1-f.a),g:f.g*f.a+b.g*(1-f.a),b:f.b*f.a+b.b*(1-f.a)};
   let op=1; for (let e=el; e; e=e.parentElement) op*=parseFloat(getComputedStyle(e).opacity||'1');
   if (op<1) f={r:f.r*op+b.r*(1-op),g:f.g*op+b.g*(1-op),b:f.b*op+b.b*(1-op)};
   const L1=lum(f), L2=lum(b); return {ratio: Math.round(((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05))*100)/100, color:s.color, bg:`rgb(${Math.round(b.r)},${Math.round(b.g)},${Math.round(b.b)})`, font:s.fontSize+'/'+s.fontWeight, cls:(typeof el.className==='string'?el.className:'').slice(0,60), opacity:Math.round(op*100)/100}; };
 const own = el => [...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
 const all = [...document.querySelectorAll('body *')].filter(e => { const r=e.getBoundingClientRect(); return r.width>0&&r.height>0; });
 const find = re => all.filter(e => re.test(own(e)) || (e.children.length===1 && re.test((e.innerText||'').trim()) && own(e)==='' && e.children[0].children.length===0 && false));
 const leaf = re => all.filter(e => re.test((e.innerText||'').trim()) && ![...e.children].some(c=>re.test((c.innerText||'').trim())));
 const kpi = leaf(/^available liquidity$/i)[0];
 const grp = leaf(/^money$/i)[0];
 const per = leaf(/^vs (27 Aug|30 days ago|start of period)$/i)[0] || all.filter(e=>/(^|\s)(per|kpi-per)(\s|$)/.test(typeof e.className==='string'?e.className:''))[0];
 const out = {kpi_label: kpi? cr(kpi): null, nav_group_label: grp? cr(grp): null, kpi_period: per? cr(per): null};
 // (f) KPI label ink clipped: label box vs its overflow-hidden ancestor, measured on the text range
 if (kpi) { const rg=document.createRange(); rg.selectNodeContents(kpi); const tr=rg.getBoundingClientRect(); let clip=null;
   for (let a=kpi; a && a!==document.body; a=a.parentElement){ const s=getComputedStyle(a); if(/(hidden|clip)/.test(s.overflowX+' '+s.overflowY)){ const ar=a.getBoundingClientRect(); clip={by:a.tagName.toLowerCase()+'.'+(typeof a.className==='string'?a.className.split(/\s+/).slice(0,2).join('.'):''), box_h: Math.round(ar.height*10)/10, text_h: Math.round(tr.height*10)/10, cut_bottom: Math.round((tr.bottom-ar.bottom)*10)/10, trim: s.textBoxTrim||s.getPropertyValue('text-box-trim')||'', line_height:s.lineHeight}; break; } }
   out.kpi_label_clip = clip; }
 // (a) the outer bento wall gutter
 const html = getComputedStyle(document.documentElement);
 out.bento_dashboard_main = html.getPropertyValue('--bento-dashboard-main').trim();
 out.bento_dashboard_sub = html.getPropertyValue('--bento-dashboard-sub').trim();
 const walls = [...document.querySelectorAll('.c-bento')].filter(w=>w.getBoundingClientRect().width>0);
 out.walls = walls.slice(0,6).map(w => { const g=w.querySelector(':scope > .c-bento__grid')||w; const s=getComputedStyle(g); return {cls:w.className.slice(0,70), gap:s.columnGap+' / '+s.rowGap, bento_gutter:getComputedStyle(w).getPropertyValue('--bento-gutter').trim()}; });
 const sh = document.querySelector('.sh'); out.shell_frame_h = sh ? Math.round(sh.getBoundingClientRect().height) : null;
 out.shell_frame_css_h = sh ? getComputedStyle(sh).height : null;
 return out; }"""
def dest(run): return "index.html" if run.startswith("v1013") else ("index.html?view=overview" if run=="cand-r1" else "index.html#/overview")
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory="/")); srv.daemon_threads=True
    threading.Thread(target=srv.serve_forever, daemon=True).start(); port=srv.server_address[1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])
        for run in sys.argv[1:]:
            pg = b.new_page(viewport={"width":1440,"height":1000})
            base = "/" + os.path.relpath(os.path.join(STAGE, "cold-"+run, "out"), "/")
            pg.goto("http://127.0.0.1:%d%s/%s" % (port, urllib.parse.quote(base), dest(run)), wait_until="load"); pg.wait_for_timeout(1500)
            r = pg.evaluate(JS); r["run"]=run
            pg.evaluate("() => document.documentElement.setAttribute('data-theme','dark')"); pg.wait_for_timeout(500)
            d = pg.evaluate(JS); r["dark_forced"] = {k: d.get(k) for k in ("kpi_label","nav_group_label","kpi_period")}
            json.dump(r, open(os.path.join(HERE, "views", run, "defects.json"), "w"), indent=1)
            print(run, {k:(r[k] or {}).get('ratio') for k in ('kpi_label','nav_group_label','kpi_period')}, {k:(r['dark_forced'][k] or {}).get('ratio') for k in ('kpi_label','nav_group_label','kpi_period')}, 'op', (r['kpi_label'] or {}).get('opacity'), (r['nav_group_label'] or {}).get('opacity'), 'gutter', r['walls'][0]['gap'] if r['walls'] else None, 'shell', r['shell_frame_css_h'], 'clip', r.get('kpi_label_clip')); pg.close()
        b.close()
