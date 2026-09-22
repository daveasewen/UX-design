import os, json, time, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath('.') + '/'
F = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
D = R + 'notes/_lanes/296/C/'
IDS = ['s1','s2','s3','s4p','s5x','s5r','s6','s6b','s7','s8','s9','s10','s10map','s11','s12']
errs = []; meas = {}
MJS = '''() => {
  const nav = document.getElementById('chrail'), r = nav.getBoundingClientRect();
  const rr = x => Math.round(x*10)/10;
  const cur = nav.querySelector('.cr-ch.is-cur'), sub = nav.querySelector('.cr-sub.is-cur');
  // visible rail extent = union of markers and titles actually drawn
  let right = 0;
  nav.querySelectorAll('.cr-c,.cr-d,.cr-t').forEach(n => { const b = n.getBoundingClientRect(); if (b.width && getComputedStyle(n).display!=='none') right = Math.max(right, b.right); });
  // content left edge on the current slide: leftmost visible text/graphic leaf within viewport
  const deck = document.getElementById('deck');
  const sl = [...document.querySelectorAll('section.slide')].find(s => Math.abs(s.getBoundingClientRect().top) < 5);
  let minL = 1e9, who = '', hits = [];
  const railBoxes = [...nav.querySelectorAll('.cr-c,.cr-d,.cr-t')].filter(n=>getComputedStyle(n).display!=='none').map(n=>{const b=n.getBoundingClientRect(); return {left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,k:n.className+(n.closest('.is-cur')?'@cur':'')};}).filter(b=>b.width);
  let markR = 0; nav.querySelectorAll('.cr-c,.cr-d').forEach(n=>{markR=Math.max(markR,n.getBoundingClientRect().right)});
  sl.querySelectorAll('*').forEach(n => {
    const cs = getComputedStyle(n); if (cs.visibility==='hidden' || cs.display==='none' || +cs.opacity===0) return;
    const hasText = [...n.childNodes].some(c => c.nodeType===3 && c.textContent.trim());
    if (!(hasText || /^(IMG|CANVAS|svg)$/i.test(n.tagName))) return;
    const b = n.getBoundingClientRect(); if (!b.width || b.bottom<0 || b.top>900) return;
    if (b.left < minL) { minL = b.left; who = n.tagName + '.' + (n.className && n.className.baseVal!==undefined ? n.className.baseVal : n.className) + ':' + (n.textContent||'').trim().slice(0,24); }
    for (const q of railBoxes) { if (q.right > b.left && q.left < b.right && q.bottom > b.top && q.top < b.bottom) { hits.push({el: n.tagName+':'+(n.textContent||'').trim().slice(0,24), kind: q.k, px: rr(q.right - b.left)}); break; } }
  });
  return {slide: sl && sl.id, box: [rr(r.left), rr(r.top), rr(r.width), rr(r.height)], opacity: getComputedStyle(nav).opacity,
    cls: nav.className, cur: cur ? cur.textContent : null, subCur: !!sub,
    grown: cur ? rr(cur.querySelector('.cr-c').getBoundingClientRect().width) : null,
    dot: rr(nav.querySelector('.cr-sub:not(.is-cur) .cr-d').getBoundingClientRect().width),
    subDot: sub ? rr(sub.querySelector('.cr-d').getBoundingClientRect().width) : null,
    chip: rr(nav.querySelector('.cr-ch:not(.is-cur) .cr-c').getBoundingClientRect().width),
    tinyFont: getComputedStyle(nav.querySelector('.cr-ch:not(.is-cur) .cr-t')).fontSize,
    curFont: cur ? getComputedStyle(cur.querySelector('.cr-t')).fontSize : null,
    railRight: rr(right), markerRight: rr(markR), contentLeft: rr(minL), contentLeftEl: who, overlaps: hits.slice(0,6)};
}'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--no-sandbox"])
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    pg.on('pageerror', lambda x: errs.append('pageerror: %s' % x))
    pg.on('console', lambda m: errs.append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
    pg.goto('file://' + F, wait_until='load'); time.sleep(2.5)
    order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>s.id)")
    assert order == IDS, order
    for i in IDS:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); time.sleep(2.3)
        pg.screenshot(path=D + i + '.png')
        meas[i] = pg.evaluate(MJS)
    # click test: click the chapter-6 circle from s12, expect s9 current
    pg.click('#chrail li.cr-ch:nth-of-type(1) >> nth=0') if False else None
    btn = pg.locator('#chrail .cr-ch .cr-row').nth(5); btn.click(); time.sleep(1.6)
    meas['click_ch6'] = pg.evaluate("() => [...document.querySelectorAll('section.slide')].find(s => Math.abs(s.getBoundingClientRect().top) < 5)?.id")
    pg.locator('#chrail .cr-sub .cr-row').nth(1).click(); time.sleep(1.6)
    meas['click_sub2'] = pg.evaluate("() => [...document.querySelectorAll('section.slide')].find(s => Math.abs(s.getBoundingClientRect().top) < 5)?.id")
    pg.keyboard.press('ArrowDown'); time.sleep(1.6)
    meas['key_down_after'] = pg.evaluate("() => document.querySelector('#chrail .is-cur .cr-t').textContent + ' sub=' + !!document.querySelector('#chrail .cr-sub.is-cur')")
    pg.close()
    # DPR 3 rail crops
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=3)
    pg.on('pageerror', lambda x: errs.append('pageerror3: %s' % x))
    pg.goto('file://' + F, wait_until='load'); time.sleep(2.5)
    for i in ['s6b', 's5r']:
        pg.evaluate('n => window.deckGo(n)', IDS.index(i)); time.sleep(2.3)
        bx = pg.evaluate("() => { const r = document.getElementById('chrail').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
        pg.screenshot(path=D + 'rail-' + i + '.png', clip={'x': 0, 'y': bx[1] - 24, 'width': 300, 'height': bx[3] + 48})
    pg.close(); b.close()
json.dump({'errors': errs, 'measured': meas}, open(D + 'measured.json', 'w'), indent=1)
print(json.dumps({'errors': errs}, indent=0))
for k, v in meas.items():
    if isinstance(v, dict):
        print(k, v['box'], v['opacity'], v['cls'], 'cur=', v['cur'], 'sub=', v['subDot'], 'grown=', v['grown'], 'railR=', v['railRight'], 'markR=', v['markerRight'], 'cL=', v['contentLeft'], v['contentLeftEl'][:40], 'ov=', v['overlaps'])
    else: print(k, v)
m = meas['s6b']; print('dot', m['dot'], 'chip', m['chip'], 'tiny', m['tinyFont'], 'curFont', m['curFont'])
# contact sheet 3 across
fp = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fnt = ImageFont.truetype(fp, 22) if os.path.exists(fp) else ImageFont.load_default()
tw, th = 720, 450; cols = 3; rows = (len(IDS) + 2) // 3
sh = Image.new('RGB', (cols * (tw + 20) + 20, rows * (th + 50) + 20), 'white'); dr = ImageDraw.Draw(sh)
for k, i in enumerate(IDS):
    im = Image.open(D + i + '.png').convert('RGB').resize((tw, th)); x = 20 + (k % 3) * (tw + 20); y = 20 + (k // 3) * (th + 50)
    dr.text((x, y), '%02d  #%s  %s' % (k + 1, i, meas[i]['cur'] or '-'), fill='black', font=fnt); sh.paste(im, (x, y + 32))
sh.save(D + 'contact-sheet.png'); print('done')
