#!/usr/bin/env python3
"""Lane EX3 (#280) — explorer 1.19's screenshots and the default-canvas identity gate.

Four states, light and dark, at 1280:
  legend-side     — the page as it opens (the base graph is portrait, so the legend takes the side)
  legend-bottom   — the same page after the `⇣ bottom` toggle, the legend on the bottom strip
  modal-served    — INSPECT open on a dug component, the file's contents IN the modal (served)
  modal-file      — the same modal from file://, the path named with a copy button

Every shot is taken in a FRESH browser.new_context. The two legend shots are NEVER DRIVEN except by
the one click the shot is of; `Object.keys(localStorage)` and the page errors are recorded for each.

The identity gate: 1.18 (git HEAD's shipped page) and 1.19, both at page defaults, both light, both
1280x800, fresh contexts — `cv.toDataURL()` md5 must be the same string.

  source knowledge/_render/seat_env.sh
  CONTROL=<1.18 page> SERVED=<http base url> python3 notes/_lanes/280/explorer-ux/shots.py
"""
import json, os, hashlib
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/explorer-ux/shots')
PAGE = 'file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html')
SERVED = os.environ.get('SERVED')
CONTROL = os.environ.get('CONTROL')
ONLY_MODAL = bool(os.environ.get('ONLY_MODAL'))
os.makedirs(OUT, exist_ok=True)

PROBE = """() => {const lg=document.getElementById('legend').getBoundingClientRect();
  const g=document.getElementById('cv');const m=document.getElementById('insp')||{classList:{contains:()=>false},querySelector:()=>null,querySelectorAll:()=>[]};
  return {legend:{x:Math.round(lg.x),y:Math.round(lg.y),w:Math.round(lg.width),h:Math.round(lg.height)},
    place:(typeof legPlace==='undefined')?'?':legPlace,
    strip:document.getElementById('legend').classList.contains('strip'),
    stats:document.getElementById('stats').innerText.replace(/\\s+/g,' ').trim(),
    view:{k:+view.k.toFixed(4),x:Math.round(view.x),y:Math.round(view.y)},
    modalOpen:m.classList.contains('on'),
    modalFileChars:(m.querySelector('.fbody')||{innerText:''}).innerText.length,
    modalPaths:[...m.querySelectorAll('.fpath code')].map(c=>c.textContent),
    md5src:g.toDataURL('image/png'), ls:Object.keys(localStorage).sort()}}"""

DIG = """()=>{setFocus(byId.get('component:button'))}"""
# the File section is the LAST of the modal's three, so the shot scrolls to it — that is the half of
# the modal the two runs are supposed to differ in
TOFILE = """()=>{const s=[...document.querySelectorAll('#insp .sec')].pop();if(s)s.scrollIntoView({block:'start'})}"""


def open_modal(pg):
    pg.evaluate(DIG); pg.wait_for_timeout(1400)
    pg.click('.rel[data-id] .insp'); pg.wait_for_timeout(1500)
    pg.evaluate(TOFILE)


def shoot(br, name, url, scheme, drive=None, w=1280, h=800):
    ctx = br.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme, device_scale_factor=1)
    pg = ctx.new_page(); errs = []; cons = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: cons.append(m.text) if m.type == 'error' else None)
    pg.goto(url, wait_until='load'); pg.wait_for_timeout(1800)
    if drive: drive(pg); pg.wait_for_timeout(1600)
    d = pg.evaluate(PROBE)
    d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
    d['errors'] = errs; d['console'] = cons; d['scheme'] = scheme; d['viewport'] = f'{w}x{h}'
    d['url'] = url
    p = os.path.join(OUT, name + '.png')
    pg.screenshot(path=p); d['bytes'] = os.path.getsize(p)
    print(f"{name:34} place={d['place']:<7} legend={tuple(d['legend'].values())} modal={d['modalOpen']} "
          f"fileChars={d['modalFileChars']:<6} k={d['view']['k']:<8} err={len(errs)} con={len(cons)} "
          f"ls={d['ls']} md5={d['canvasMd5'][:10]} {d['bytes']:,}B")
    ctx.close()
    return d


def main():
    res = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                               args=['--no-sandbox', '--force-device-scale-factor=1'])
        for s in ('light', 'dark'):
            if not ONLY_MODAL:
                res[f'kg-119-legend-side-{s}'] = shoot(br, f'kg-119-legend-side-{s}', PAGE, s)
                res[f'kg-119-legend-bottom-{s}'] = shoot(
                    br, f'kg-119-legend-bottom-{s}', PAGE, s, lambda pg: pg.click('.lplace'))
            res[f'kg-119-modal-file-{s}'] = shoot(br, f'kg-119-modal-file-{s}', PAGE, s, open_modal)
            if SERVED:
                res[f'kg-119-modal-served-{s}'] = shoot(
                    br, f'kg-119-modal-served-{s}', SERVED, s, open_modal)
        if CONTROL:
            res['kg-118-control-light'] = shoot(br, 'kg-118-control-light', 'file://' + CONTROL, 'light')
            res['kg-119-default-light'] = shoot(br, 'kg-119-default-light', PAGE, 'light')
        br.close()
    fp = os.path.join(OUT, 'shots.json')
    old = json.load(open(fp)) if os.path.exists(fp) else {}
    old.update(res); json.dump(old, open(fp, 'w'), indent=1)
    if CONTROL:
        a, b = res['kg-118-control-light']['canvasMd5'], res['kg-119-default-light']['canvasMd5']
        print('\nDEFAULT CANVAS 1.18 vs 1.19 (light, 1280x800, page defaults):',
              'SAME ' + a if a == b else f'DIFF {a} {b}')
    print('wrote', fp)


if __name__ == '__main__':
    main()
