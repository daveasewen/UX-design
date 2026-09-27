"""probe_edge.py — R4s2 (#304): chart text cut by its OWN svg edge (the class the geometry gate's G8 does not see:
G8 reads overflow boxes and scroll-box start edges, not an svg viewport clipping its own label).
For every kept view of every run in a runs dir: count visible svg <text> whose ink box runs past the
owning chart svg's box by more than 1px on the left or right. Writes <runs dir>/../edge-<name>.json."""
import json, os, sys, glob, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'R4c', 'harness'))
import views as HV   # NAV_JS: the harness's own nav marking, so every kept view is reached by the same click
from playwright.sync_api import sync_playwright
JS = r"""() => { const out = [];
 for (const svg of document.querySelectorAll('figure svg.dv-svg, svg.dv-fit, figure[data-dv-type] svg')) {
   if (svg.closest('[hidden],template')) continue; const sr = svg.getBoundingClientRect(); if (sr.width < 60) continue;
   // the clip frame: the svg itself unless it overflows visibly, else its nearest ancestor that clips or scrolls
   let frame = svg; if (getComputedStyle(svg).overflow === 'visible') { frame = null;
     for (let a = svg.parentElement; a && a !== document.body; a = a.parentElement) { if (getComputedStyle(a).overflowX !== 'visible') { frame = a; break; } } }
   if (!frame) continue; const fr = frame.getBoundingClientRect();
   for (const t of svg.querySelectorAll('text')) { const s = getComputedStyle(t); if (s.visibility === 'hidden' || s.display === 'none' || !t.textContent.trim()) continue;
     const r = t.getBoundingClientRect(); if (!r.width) continue; const over = Math.max(fr.left - r.left, r.right - fr.right);
     if (over > 1) out.push({text: t.textContent.trim().slice(0, 30), px: Math.round(over), side: (fr.left - r.left) > (r.right - fr.right) ? 'left' : 'right', frame: frame.tagName + '.' + (frame.getAttribute('class')||'').split(' ')[0],
       cls: (t.getAttribute('class')||'').split(' ')[0], svg_w: Math.round(sr.width)}); } }
 return out; }"""
def main(runs_dir, ids, budget=160):
    t0 = time.time(); res = {}
    outp = os.path.join(os.path.dirname(runs_dir.rstrip('/')), 'edge-' + os.path.basename(runs_dir.rstrip('/')) + '.json')
    if os.path.exists(outp): res = json.load(open(outp))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
        for rid in ids:
            if rid in res: continue
            v = json.load(open(os.path.join(runs_dir, rid, 'views.json'))); per = {}
            for x in v['views']:
                if not x.get('kept'): continue
                if time.time() - t0 > budget: break
                m = json.load(open(os.path.join(runs_dir, rid, 'meta.json')))
                pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
                pg.goto('file://' + m['entry'], wait_until='load', timeout=30000); pg.wait_for_timeout(900)
                if x['key'] != 'entry':
                    pg.evaluate(HV.NAV_JS); pg.locator('[data-w4b-nav="%s"]' % x['key'][3:]).first.click(timeout=3000)
                    try: pg.wait_for_load_state('load', timeout=5000)
                    except Exception: pass
                pg.wait_for_timeout(1300)
                f = pg.evaluate(JS); pg.close()
                per[x['key']] = {'url': x['url'][-80:], 'n': len(f), 'charts': len({(i['svg_w']) for i in f}), 'sample': f[:4]}
            else:
                res[rid] = per; print(rid, sum(i['n'] for i in per.values()), 'cut texts on', sum(1 for i in per.values() if i['n']), 'views'); continue
            print(rid, 'INCOMPLETE (budget)'); break
        b.close()
    json.dump(res, open(outp, 'w'), indent=1)
main(sys.argv[1], sys.argv[2:])
