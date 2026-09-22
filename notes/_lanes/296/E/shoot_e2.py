import os, json, time, math, base64
from playwright.sync_api import sync_playwright
from PIL import Image
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
    meas['sections'] = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s=>[s.id, Math.round(s.getBoundingClientRect().height), s.querySelector(':scope > .pagenum') ? s.querySelector(':scope > .pagenum').innerText : null])")
    for i in ['s7', 's8']:
        pg.evaluate('n => window.deckGo(n)', order.index(i)); pg.mouse.move(721, 450); pg.mouse.move(720, 450); time.sleep(2.3)
        pg.evaluate('() => { window.brSet && window.brSet(0,0); window.shlSet && window.shlSet(0,0); }'); time.sleep(0.3)
        pg.screenshot(path=D + 'e2-' + i + '.png')
    for pid in ['shlPrint', 'brPrint', 'bkPrint', 'cpPrint']:
        d = pg.evaluate("id => { const i = document.getElementById(id); return i && i.src && i.src.startsWith('data:') ? i.src : null; }", pid)
        meas[pid] = len(d) if d else 0
        if d: open(D + 'e2-' + pid + '.png', 'wb').write(base64.b64decode(d.split(',')[1]))
    meas['shl'] = pg.evaluate('() => window.shlState && window.shlState()')
    meas['anatomy'] = pg.evaluate('() => window.anatomyState && window.anatomyState()')
    b.close()
def ang(yaw, pit, psi):
    y, t, q = map(math.radians, (yaw, pit, psi)); out = []
    for dx, dy in [(math.cos(q), math.sin(q)), (-math.sin(q), math.cos(q))]:
        sx = math.cos(y)*dx + math.sin(y)*dy; sy = math.sin(t)*math.sin(y)*dx - math.sin(t)*math.cos(y)*dy
        a = math.degrees(math.atan2(sy, sx)) % 180; out.append(round(min(a, 180 - a), 2))
    return sorted(out)
meas['plate_edges_deg'] = {'gearbox': ang(-35, 20, 0), 'books': ang(-35, 20, 0), 'shells': ang(-35, 20, 0),
    'callipers_before(psi-62)': ang(-35, 20, -62), 'callipers_after(psi-90)': ang(-35, 20, -90), 'brain(-50)': ang(-50, 20, 0), 'catalogue(psi-5)': ang(-35, 20, -5)}
meas['errors'] = errs
json.dump(meas, open(D + 'e2-measured.json', 'w'), indent=1)
print(json.dumps({k: meas[k] for k in ['plate_edges_deg', 'errors', 'anatomy']}))
print(json.dumps(meas['shl']))
print(set(s[1] for s in meas['sections']), len(meas['sections']), [s[2] for s in meas['sections']])
ps = [Image.open(D + 'e2-' + n + '.png').convert('RGB') for n in ['shlPrint', 'brPrint', 'bkPrint', 'cpPrint']]
H = 500; ps = [im.resize((int(im.width * H / im.height), H)) for im in ps]
sh = Image.new('RGB', (sum(i.width for i in ps) + 10 * (len(ps) + 1), H + 20), 'white'); x = 10
for im in ps: sh.paste(im, (x, 10)); x += im.width + 10
sh.save(D + 'e2-four-up.png'); print('done')
