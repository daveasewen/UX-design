import os, json, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath('.') + '/'
D = R + 'notes/_lanes/296/C/'
PLAIN = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
PLANT = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plant.html'
POS = "() => [...document.querySelectorAll('#chrail li')].map(l => { const m = l.querySelector('.cr-c,.cr-d').getBoundingClientRect(); return [Math.round((m.top+m.height/2)*10)/10, Math.round(m.width*10)/10]; })"
STATE = '''() => { const nav = document.getElementById('chrail'), rr = x => Math.round(x*10)/10; const cs = getComputedStyle(nav);
  const cur = nav.querySelector('.cr-ch.is-cur'); const cc = cur ? cur.querySelector('.cr-c').getBoundingClientRect() : null;
  const t = cur ? cur.querySelector('.cr-t') : null; const q = s => nav.querySelector(s);
  const line = getComputedStyle(nav.querySelector('ol'), '::before');
  return {cls: nav.className, opacity: cs.opacity, clickable: [...nav.querySelectorAll('.cr-row')].filter(n => getComputedStyle(n).pointerEvents !== 'none').length,
    ariaCur: nav.querySelectorAll('[aria-current]').length,
    cur: cur ? cur.textContent : null, cy: cc ? rr(cc.top + cc.height/2) : null, d: cc ? rr(cc.width) : null,
    title: t ? [getComputedStyle(t).fontSize, rr(t.getBoundingClientRect().height), rr(t.getBoundingClientRect().width), t.scrollWidth > t.clientWidth + 1] : null,
    sub: !!q('.cr-sub.is-cur'),
    col: {line: line.backgroundColor, other: q('.cr-ch:not(.is-cur) .cr-c') ? getComputedStyle(q('.cr-ch:not(.is-cur) .cr-c')).borderTopColor : null,
      otherDot: q('.cr-sub:not(.is-grp) .cr-d') ? getComputedStyle(q('.cr-sub:not(.is-grp) .cr-d')).backgroundColor : null,
      grpDot: q('.cr-sub.is-grp:not(.is-cur) .cr-d') ? getComputedStyle(q('.cr-sub.is-grp:not(.is-cur) .cr-d')).backgroundColor : null,
      curDot: q('.cr-sub.is-cur .cr-d') ? getComputedStyle(q('.cr-sub.is-cur .cr-d')).backgroundColor : null,
      stroke: cur ? getComputedStyle(cur.querySelector('.cr-c')).borderTopColor : null}}; }'''
errs = {'plain': [], 'plant': []}; out = {}
def page(b, F, tag, dpr=2):
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=dpr)
    pg.on('pageerror', lambda x: errs[tag].append('pageerror: %s' % x))
    pg.on('console', lambda m: errs[tag].append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
    pg.goto('file://' + F, wait_until='load'); time.sleep(2.5)
    return pg, pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>s.id)")
def jump(pg, order, tag):
    r = {}
    pg.evaluate('n => window.deckGo(n)', order.index('s2')); time.sleep(1.5)
    r['s2_pos'] = pg.evaluate(POS); r['s2_state'] = pg.evaluate(STATE)
    pg.evaluate('n => window.deckGo(n)', order.index('s3')); time.sleep(0.12)
    r['t120_pos'] = pg.evaluate(POS); r['t120_opacity'] = pg.evaluate("() => getComputedStyle(document.getElementById('chrail')).opacity")
    time.sleep(1.2); r['s3_pos'] = pg.evaluate(POS); r['s3_state'] = pg.evaluate(STATE)
    # and back s3 -> s2
    pg.evaluate('n => window.deckGo(n)', order.index('s2')); time.sleep(0.12); r['back_t120_pos'] = pg.evaluate(POS)
    r['s2_equals_s3'] = r['s2_pos'] == r['s3_pos']; r['t120_equals_s3'] = r['t120_pos'] == r['s3_pos']; r['back_equals'] = r['back_t120_pos'] == r['s3_pos']
    return r
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--no-sandbox"])
    # --- A. plain jump fix
    pg, order = page(b, PLAIN, 'plain')
    out['plain_jump'] = jump(pg, order, 'plain'); pg.close()
    pg, order = page(b, PLAIN, 'plain', 3)
    for i in ['s2', 's3']:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); time.sleep(1.5)
        if i == 's2':   # hidden rail: force visible for the crop only, to show where it sits
            pg.add_style_tag(content='#chrail.is-hidden{opacity:1 !important}'); time.sleep(0.3)
        pg.screenshot(path=D + 'v6-rail-%s.png' % i, clip={'x': 0, 'y': 0, 'width': 320, 'height': 900})
    pg.close()
    # --- B. plant
    pg, order = page(b, PLANT, 'plant')
    out['plant_order'] = order
    out['plant_jump'] = jump(pg, order, 'plant')
    SH = ['s1','s2','s3','s5insight','s6','s7','s9','s11','s12']
    out['plant'] = {}
    for i in order:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); time.sleep(2.2 if i in SH else 0.9)
        if i in SH: pg.screenshot(path=D + 'plant-%s.png' % i)
        out['plant'][i] = pg.evaluate(STATE)
    pg.close()
    pg, order = page(b, PLANT, 'plant', 3)
    for i in ['s3', 's7', 's12']:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); time.sleep(1.8)
        pg.screenshot(path=D + 'plant-rail-%s.png' % i, clip={'x': 0, 'y': 0, 'width': 360, 'height': 900})
    pg.close(); b.close()
json.dump({'errors': errs, 'out': out}, open(D + 'v6-plant-measured.json', 'w'), indent=1)
print('errors', errs)
for k in ['plain_jump', 'plant_jump']:
    j = out[k]; print(k, 's2==s3', j['s2_equals_s3'], 't120==s3', j['t120_equals_s3'], 'back==', j['back_equals'], 't120 opacity', j['t120_opacity'], 's2', {x: j['s2_state'][x] for x in ('cls','opacity','clickable','ariaCur','cur')}, 's3', {x: j['s3_state'][x] for x in ('cls','opacity','cur','cy')})
    print('  s3 pos', j['s3_pos'])
for i, v in out['plant'].items(): print(i, v['cls'], v['opacity'], v['cur'], 'cy', v['cy'], 'd', v['d'], 'sub', v['sub'], 'title', v['title'], v['col'])
fp = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fnt = ImageFont.truetype(fp, 22) if os.path.exists(fp) else ImageFont.load_default()
SH = ['s1','s2','s3','s5insight','s6','s7','s9','s11','s12']
tw, th = 720, 450
sh = Image.new('RGB', (3 * (tw + 20) + 20, 3 * (th + 50) + 20), 'white'); dr = ImageDraw.Draw(sh)
for k, i in enumerate(SH):
    im = Image.open(D + 'plant-%s.png' % i).convert('RGB').resize((tw, th)); x = 20 + (k % 3) * (tw + 20); y = 20 + (k // 3) * (th + 50)
    dr.text((x, y), '#%s  %s' % (i, out['plant'][i]['cur'] if out['plant'][i]['opacity'] != '0' else '(rail hidden)'), fill='black', font=fnt); sh.paste(im, (x, y + 32))
sh.save(D + 'plant-contact-sheet.png')
fnt2 = ImageFont.truetype(fp, 30) if os.path.exists(fp) else ImageFont.load_default()
ims = [Image.open(D + 'plant-rail-%s.png' % i).convert('RGB') for i in ['s3','s7','s12']]
s3 = Image.new('RGB', (sum(x.width for x in ims) + 160, ims[0].height + 90), (200, 200, 200)); dr = ImageDraw.Draw(s3); x = 40
for i, im in zip(['s3','s7','s12'], ims): dr.text((x, 25), '#' + i, fill='black', font=fnt2); s3.paste(im, (x, 70)); x += im.width + 40
s3.save(D + 'plant-rail-3up.png')
ims = [Image.open(D + 'v6-rail-%s.png' % i).convert('RGB') for i in ['s2','s3']]
s3 = Image.new('RGB', (sum(x.width for x in ims) + 120, ims[0].height + 90), (200, 200, 200)); dr = ImageDraw.Draw(s3); x = 40
for i, im in zip(['s2 (hidden, forced visible)','s3'], ims): dr.text((x, 25), '#' + i, fill='black', font=fnt2); s3.paste(im, (x, 70)); x += im.width + 40
s3.save(D + 'v6-rail-s2-s3.png'); print('done')
