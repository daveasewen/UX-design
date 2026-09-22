# #297 lane R - render the review page for a visual check: top screen + full page sliced.
import os, sys, time, json
from playwright.sync_api import sync_playwright
from PIL import Image
page_path = os.path.abspath(sys.argv[1]); out = os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': W, 'height': 900}, device_scale_factor=1)
    errs = []; pg.on('pageerror', lambda x: errs.append(str(x)))
    pg.goto('file://' + page_path, wait_until='load'); time.sleep(1.5)
    pg.screenshot(path=os.path.join(out, 'top-%d.png' % W))
    info = pg.evaluate("""() => ({h: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, iw: innerWidth,
      secs: [...document.querySelectorAll('section.major, header.hero')].map(s => [s.id || s.className, Math.round(s.getBoundingClientRect().top + scrollY)]),
      imgs: [...document.images].filter(i => !i.complete || !i.naturalWidth).length,
      wide: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth + 1).slice(0,8).map(e => e.tagName + '.' + e.className)})""")
    pg.evaluate("() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    # scroll through to load lazy images
    for y in range(0, info['h'], 800):
        pg.evaluate('y => scrollTo(0, y)', y); time.sleep(0.05)
    time.sleep(1.0); pg.evaluate('() => scrollTo(0,0)')
    pg.screenshot(path=os.path.join(out, 'full-%d.png' % W), full_page=True)
    b.close()
im = Image.open(os.path.join(out, 'full-%d.png' % W)); H = im.height; n = 0
for y in range(0, H, 1600):
    im.crop((0, y, im.width, min(H, y + 1600))).save(os.path.join(out, 'seg-%d-%02d.png' % (W, n))); n += 1
info['errors'] = errs; info['segments'] = n
json.dump(info, open(os.path.join(out, 'info-%d.json' % W), 'w'), indent=1)
print(json.dumps(info))
