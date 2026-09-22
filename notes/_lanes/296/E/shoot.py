import os, json, time, math, re, base64
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R = os.path.abspath('.') + '/'
NEW = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
D = R + 'notes/_lanes/296/E/'
errs = []; meas = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], args=["--no-sandbox"])
    pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    pg.on('pageerror', lambda x: errs.append('pageerror: %s' % x))
    pg.on('console', lambda m: errs.append('console.%s: %s' % (m.type, m.text)) if m.type == 'error' else None)
    pg.mouse.move(720, 450); pg.goto('file://' + NEW, wait_until='load'); pg.mouse.move(720, 450); time.sleep(3.0)
    order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>s.id)")
    meas['order'] = order
    meas['sections'] = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>[s.id, Math.round(s.getBoundingClientRect().height), s.querySelector(':scope > .pagenum') ? s.querySelector(':scope > .pagenum').innerText : null])")
    for i in ['s6', 's7', 's8', 's7b', 's6b', 's10']:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); pg.mouse.move(721, 450); pg.mouse.move(720, 450); time.sleep(2.3); pg.evaluate('() => { window.brSet && window.brSet(0,0); window.shlSet && window.shlSet(0,0); }'); time.sleep(0.2)
        pg.screenshot(path=D + i + '.png')
    # drawings at rest, straight from the baked prints
    for pid, name in [('shlPrint', 'shells-print.png'), ('brPrint', 'brain-print.png'), ('bkPrint', 'books-print.png'), ('gbPrint', 'gearbox-print.png')]:
        d = pg.evaluate("id => { const i = document.getElementById(id); return i && i.src && i.src.startsWith('data:') ? i.src : null; }", pid)
        meas[pid] = len(d) if d else 0
        if d: open(D + name, 'wb').write(base64.b64decode(d.split(',')[1]))
    meas['shl'] = pg.evaluate('() => window.shlState && window.shlState()')
    meas['anatomy'] = pg.evaluate('() => window.anatomyState && window.anatomyState()')
    meas['chrail'] = pg.evaluate("() => { const r = window.chRail && window.chRail.data; return r ? JSON.stringify(r).slice(0, 600) : null; }")
    b.close()
src = open(R + 'notes/_lanes/296/C/v14-plain-before-c.html', encoding='utf-8').read()
consts = re.findall(r"var YAW0 = (-?\d+)\*(?:Math\.PI/180|D2R), PIT0 = (\d+)\*", src)
meas['yaw_pit_constants_in_source'] = consts
def ang(yaw, pit):
    y, t = math.radians(yaw), math.radians(pit)
    ea = math.degrees(math.atan2(math.sin(t)*math.sin(y), math.cos(y)))     # a-edge, screen, + = rising to the right
    eu = math.degrees(math.atan2(-math.sin(t)*math.cos(y), math.sin(y)))    # u-edge
    return round(ea, 2), round(eu, 2)
meas['plinth_edge_angles'] = {'gearbox(-35,20)': ang(-35, 20), 'books(-35,20)': ang(-35, 20), 'shells(-35,20)': ang(-35, 20), 'brain(-50,20)': ang(-50, 20)}
meas['errors'] = errs
json.dump(meas, open(D + 'measured.json', 'w'), indent=1)
print(json.dumps(meas, indent=0)[:4000])
# contact sheet s6 .. s6b
ids = ['s6', 's7', 's8', 's7b', 's6b']
ims = [Image.open(D + i + '.png').convert('RGB').resize((720, 450)) for i in ids]
sh = Image.new('RGB', (720 * 3 + 40, 450 * 2 + 30), 'white')
for k, im in enumerate(ims): sh.paste(im, (10 + (k % 3) * 730, 10 + (k // 3) * 460))
sh.save(D + 'contact-s6-s6b.png')
# three-up of the drawings at matched height
ps = [Image.open(D + n).convert('RGB') for n in ['shells-print.png', 'brain-print.png', 'books-print.png', 'gearbox-print.png'] if os.path.exists(D + n)]
H = 500; ps = [im.resize((int(im.width * H / im.height), H)) for im in ps]
sh = Image.new('RGB', (sum(i.width for i in ps) + 10 * (len(ps) + 1), H + 20), 'white'); x = 10
for im in ps: sh.paste(im, (x, 10)); x += im.width + 10
sh.save(D + 'drawings-four-up.png')
print('done')
