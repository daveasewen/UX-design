import json, time
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
F = '/home/claude/296/B/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
D = '/home/claude/296/B/'
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    pg.on('pageerror', lambda e: errs.append('pageerror: %s' % e))
    pg.on('console', lambda m: errs.append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
    pg.goto('file://' + F, wait_until='load')
    time.sleep(2.5)
    info = pg.evaluate('''() => [...document.querySelectorAll('section.slide')].map(s => {
        const h = s.querySelector('h1,h2'); const r = s.getBoundingClientRect();
        return {id: s.id, h: h ? h.innerText.replace(/\\s+/g,' ').trim() : '', height: r.height,
                scrollH: s.scrollHeight, pn: (s.querySelector('.pagenum')||{}).innerText || ''};
    })''')
    for i, x in enumerate(info):
        pg.evaluate('n => window.deckGo(n)', i)
        time.sleep(2.5)
        pg.locator('#' + x['id']).screenshot(path=D + x['id'] + '.png')
    b.close()
json.dump({'slides': info, 'errors': errs}, open(D + 'measured.json', 'w'), indent=1)
for x in info: print(x['pn'], x['id'], x['height'], x['scrollH'], '|', x['h'][:70])
print('errors', len(errs), errs)
# contact sheet, 3 per row
W, H = 720, 450; pad = 20; lab = 44
cols = 3; rows = (len(info) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (W + pad) + pad, rows * (H + lab + pad) + pad), 'white')
dr = ImageDraw.Draw(sheet)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: fnt = ImageFont.load_default()
for i, x in enumerate(info):
    im = Image.open(D + x['id'] + '.png').convert('RGB'); im.thumbnail((W, H))
    cx = pad + (i % cols) * (W + pad); cy = pad + (i // cols) * (H + lab + pad)
    t = '%02d  #%s  %s' % (i + 1, x['id'], x['h'])
    if len(t) > 80: t = t[:78] + '…'
    dr.text((cx, cy + 12), t, fill='black', font=fnt)
    sheet.paste(im, (cx, cy + lab)); dr.rectangle([cx, cy + lab, cx + im.width - 1, cy + lab + im.height - 1], outline=(200, 200, 200))
sheet.save(D + 'contact-sheet.png')
