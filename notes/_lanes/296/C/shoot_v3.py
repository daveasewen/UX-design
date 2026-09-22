import os, json, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath('.') + '/'
F = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
D = R + 'notes/_lanes/296/C/'
IDS = ['s3','s6b','s10map','s12']
CROP = ['s3','s12']
errs = []; meas = {}
MJS = '''() => {
  const nav = document.getElementById('chrail'), rr = x => Math.round(x*10)/10;
  const line = getComputedStyle(nav.querySelector('ol'), '::before');
  const olr = nav.querySelector('ol').getBoundingClientRect();
  const cur = nav.querySelector('.cr-ch.is-cur'), sub = nav.querySelector('.cr-sub.is-cur');
  const cc = cur ? cur.querySelector('.cr-c').getBoundingClientRect() : null;
  const all = [...nav.querySelectorAll('.cr-c,.cr-d')].map(n => n.getBoundingClientRect());
  const tt = [...nav.querySelectorAll('.cr-t')].map(n => n.getBoundingClientRect());
  const bgs = [...nav.querySelectorAll('.cr-c')].map(n => getComputedStyle(n).backgroundColor);
  const sl = [...document.querySelectorAll('section.slide')].find(s => Math.abs(s.getBoundingClientRect().top) < 5);
  // overlaps between rail items (markers + titles) - should be none
  const boxes = [...nav.querySelectorAll('.cr-c,.cr-d,.cr-t')].filter(n=>getComputedStyle(n).display!=='none').map(n=>n.getBoundingClientRect()).filter(b=>b.width);
  let clash = 0; for (let i=0;i<boxes.length;i++) for (let j=i+1;j<boxes.length;j++){ const a=boxes[i], b=boxes[j];
    if (a.right>b.left && a.left<b.right && a.bottom>b.top+0.5 && a.top<b.bottom-0.5) clash++; }
  return {slide: sl.id, cls: nav.className, cur: cur ? cur.textContent : null, subLit: !!sub,
    grownCy: cc ? rr(cc.top + cc.height/2) : null, grownD: cc ? rr(cc.width) : null, grownCx: cc ? rr(cc.left + cc.width/2) : null,
    numFont: cur ? getComputedStyle(cur.querySelector('.cr-c')).fontSize + '/' + getComputedStyle(cur.querySelector('.cr-c')).fontWeight : null,
    curTitle: cur ? getComputedStyle(cur.querySelector('.cr-t')).fontSize : null,
    chip: rr(nav.querySelector('.cr-ch:not(.is-cur) .cr-c').getBoundingClientRect().width),
    dot: rr(nav.querySelector('.cr-sub:not(.is-cur) .cr-d').getBoundingClientRect().width),
    subDot: sub ? rr(sub.querySelector('.cr-d').getBoundingClientRect().width) : null,
    tiny: getComputedStyle(nav.querySelector('.cr-ch:not(.is-cur) .cr-t')).fontSize,
    lineTop: rr(olr.top + parseFloat(line.top)), lineBottom: rr(olr.bottom - parseFloat(line.bottom)), vh: innerHeight,
    lineX: rr(olr.left + parseFloat(line.left) + 0.5),
    itemsTop: rr(Math.min(...all.map(b=>b.top), ...tt.map(b=>b.top))), itemsBottom: rr(Math.max(...all.map(b=>b.bottom), ...tt.map(b=>b.bottom))),
    circleBg: [...new Set(bgs)], slideBg: getComputedStyle(sl).backgroundColor, railClash: clash, tinyShown: [...nav.querySelectorAll('.cr-t')].filter(n=>getComputedStyle(n).display!=='none').map(n=>n.textContent), centres: [...nav.querySelectorAll('.cr-mk')].map(n=>{const b=n.firstChild.getBoundingClientRect(); return rr(b.top+b.height/2);})};
}'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--no-sandbox"])
    for dpr in (2, 3):
        pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=dpr)
        pg.on('pageerror', lambda x: errs.append('pageerror: %s' % x))
        pg.on('console', lambda m: errs.append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
        pg.goto('file://' + F, wait_until='load'); time.sleep(2.5)
        order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>s.id)")
        for i in (IDS if dpr == 2 else ['s3','s6b','s12']):
            pg.evaluate('n => window.deckGo(n)', order.index(i)); time.sleep(2.3)
            if dpr == 2:
                pg.screenshot(path=D + 'v3-' + i + '.png'); meas[i] = pg.evaluate(MJS)
            else:
                pg.screenshot(path=D + 'v3-rail-' + i + '.png', clip={'x': 0, 'y': 0, 'width': 320, 'height': 900})
        if dpr == 2:
            # animation check: mid-transition sample, 120ms after a slide change
            pg.evaluate('n => window.deckGo(n)', order.index('s7')); time.sleep(0.12)
            pg.evaluate('n => window.deckGo(n)', order.index('s3')); time.sleep(1.0)
            pg.evaluate('n => window.deckGo(n)', order.index('s9')); time.sleep(0.12)
            meas['midAnim_s3_to_s9_ch6_top_at_120ms'] = pg.evaluate("() => Math.round(document.querySelectorAll('#chrail .cr-ch')[5].getBoundingClientRect().top + 22)")
            time.sleep(0.6)
            meas['after_s9_ch6_centre'] = pg.evaluate("() => Math.round(document.querySelectorAll('#chrail .cr-ch')[5].getBoundingClientRect().top + 22)")
            meas['midAnim_s6b_to_s7'] = pg.evaluate("() => document.querySelector('#chrail .cr-ch.is-cur').style.top + ' / ' + Math.round(document.querySelector('#chrail .cr-ch.is-cur').getBoundingClientRect().top)")
        pg.close()
    b.close()
# line-through check: pixel on the line's x inside the grown circle, above the numeral
for i in IDS:
    m = meas[i]
    if not m['grownCy']: continue
    im = Image.open(D + 'v3-' + i + '.png').convert('RGB')
    x = int(m['lineX'] * 2); y = int((m['grownCy'] - 16) * 2); y2 = int((m['grownCy'] + 16) * 2)
    m['pxInsideAboveNum'] = im.getpixel((x, y)); m['pxInsideBelowNum'] = im.getpixel((x, y2))
    m['pxLineOutside'] = im.getpixel((x, int((m['grownCy'] - 60) * 2)))
json.dump({'errors': errs, 'measured': meas}, open(D + 'v3-measured.json', 'w'), indent=1)
print('errors', errs)
for k, v in meas.items():
    if isinstance(v, dict):
        c = v['centres']; d = [round(c[j+1]-c[j],1) for j in range(len(c)-1)]
        v['gaps'] = d
        print(k, 'cy', v['grownCy'], 'gaps', d, 'extent', v['itemsTop'], v['itemsBottom'], 'titles', v['tinyShown'], 'line', v['lineTop'], v['lineBottom'], 'clash', v['railClash'], 'mask', v.get('pxInsideAboveNum'), v['cls'], 'sub', v['subLit'])
    else: print(k, v)
json.dump({'errors': errs, 'measured': meas}, open(D + 'v3-measured.json', 'w'), indent=1)
fp = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fnt = ImageFont.truetype(fp, 30) if os.path.exists(fp) else ImageFont.load_default()
CROP = ['s3','s6b','s12']
ims = [Image.open(D + 'v3-rail-' + i + '.png').convert('RGB') for i in CROP]
W = sum(x.width for x in ims) + 40 * 4; H = ims[0].height + 90
sh = Image.new('RGB', (W, H), (200, 200, 200)); dr = ImageDraw.Draw(sh); x = 40
for i, im in zip(CROP, ims):
    dr.text((x, 25), '#' + i, fill='black', font=fnt); sh.paste(im, (x, 70)); x += im.width + 40
sh.save(D + 'v3-rail-3up.png'); print('done')
