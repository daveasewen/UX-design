import os, json, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath('.') + '/'
NEW = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
OLD = R + 'notes/_lanes/296/B2/v14-plain-before-b2.html'
D = R + 'notes/_lanes/296/B2/'
errs = {}; meas = {}
def shoot(pg, ids, prefix):
    order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>s.id)")
    for i in ids:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); time.sleep(2.5)
        pg.locator('#' + i).screenshot(path=D + prefix + i + '.png')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--no-sandbox"])
    for tag, F, ids, pre in [('new', NEW, ['s2', 's4p', 's5x', 's5r'], ''), ('before', OLD, ['s4p', 's5x'], 'before-')]:
        e = errs[tag] = []
        pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        pg.on('pageerror', lambda x, e=e: e.append('pageerror: %s' % x))
        pg.on('console', lambda m, e=e: e.append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
        pg.goto('file://' + F, wait_until='load'); time.sleep(2.5)
        shoot(pg, ids, pre)
        if tag == 'new':
            meas = pg.evaluate('''() => {
              const o = {};
              for (const id of ['s4p','s5x','s5r','s2']) { const s = document.getElementById(id);
                o[id] = {h: s.getBoundingClientRect().height, sh: s.scrollHeight, pn: s.querySelector('.pagenum').innerText}; }
              o.overflow = [...document.querySelectorAll('#s4p .c5>div, #s4p h3, #s5x .steps li, #s5x .steps p')]
                 .filter(n => n.scrollHeight > n.clientHeight + 1 || n.scrollWidth > n.clientWidth + 1)
                 .map(n => n.className + ':' + n.innerText.slice(0,30));
              o.stepsH = [...document.querySelectorAll('#s5x .steps li')].map(n => Math.round(n.getBoundingClientRect().height));
              const r = document.querySelector('#s5x .regen').getBoundingClientRect();
              const L = [...document.querySelectorAll('#s5x .steps li')].map(n => n.getBoundingClientRect());
              o.regen = {left: r.left, right: r.right, c3: (L[2].left+L[2].right)/2, c4: (L[3].left+L[3].right)/2, top: r.top, stepBottom: L[3].bottom};
              return o; }''')
        pg.close()
    b.close()
json.dump({'errors': errs, 'measured': meas}, open(D + 'measured.json', 'w'), indent=1)
print(json.dumps({'errors': errs, 'measured': meas}, indent=0))
fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else ImageFont.load_default()
for i in ['s4p', 's5x']:
    a = Image.open(D + 'before-' + i + '.png').convert('RGB'); c = Image.open(D + i + '.png').convert('RGB')
    W = a.width + c.width + 60; H = max(a.height, c.height) + 80
    sh = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sh)
    dr.text((20, 22), 'BEFORE  #' + i, fill='black', font=fnt); dr.text((a.width + 40, 22), 'AFTER (B2)  #' + i, fill=(218, 26, 0), font=fnt)
    sh.paste(a, (20, 70)); sh.paste(c, (a.width + 40, 70))
    sh.save(D + 'before-after-' + i + '.png')
print('done')
