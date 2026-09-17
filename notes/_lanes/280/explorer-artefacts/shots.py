#!/usr/bin/env python3
"""Lane EX4 (#280) — explorer 1.20's screenshots and the default-canvas identity gate.

Every shot is a FRESH `browser.new_context` at 1280x800 (900 for the modal shots, so the artefact
section is in frame), colour scheme emulated, `localStorage` and page errors recorded.

THE IDENTITY GATE. 1.19's shipped page (git HEAD) and 1.20 are opened at the page's own defaults,
`file://`, light, 1280x800 — `cv.toDataURL()` md5 must be the same string. The Constitution family
is OFF at the defaults, which is why inscribing `s280-D2` (which adds one ruling node, one artefact
and three evidence nodes to that family) cannot move the default picture: the gate is the proof,
not the claim.

  CONTROL=<path to the 1.19 control page> SERVED=<url> python3 notes/_lanes/280/explorer-artefacts/shots.py
"""
import hashlib, json, os
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/explorer-artefacts/shots')
PAGE = 'file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html')
SERVED = os.environ.get('SERVED')
CONTROL = os.environ.get('CONTROL')
os.makedirs(OUT, exist_ok=True)

PROBE = """() => {const g=document.getElementById('cv');
  const m=document.getElementById('insp')||{classList:{contains:()=>false},querySelector:()=>null,querySelectorAll:()=>[]};
  return {legend:(()=>{const r=document.getElementById('legend').getBoundingClientRect();
      return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}})(),
    stats:document.getElementById('stats').innerText.replace(/\\s+/g,' ').trim(),
    view:{k:+view.k.toFixed(4)},
    modalOpen:m.classList.contains('on'),
    modalTitle:(m.querySelector('h2')||{textContent:''}).textContent,
    tabs:[...m.querySelectorAll('.tabs button')].map(b=>b.textContent.trim()),
    tabOn:[...m.querySelectorAll('.tabs button[aria-selected="true"]')].map(b=>b.textContent.trim()),
    iframes:m.querySelectorAll('iframe.rframe').length,
    frameTheme:(()=>{const f=m.querySelector('iframe.rframe');try{return f&&f.contentDocument?f.contentDocument.body.getAttribute('data-theme'):null}catch(e){return 'blocked'}})(),
    frameLH:(()=>{const f=m.querySelector('iframe.rframe');try{const d=f&&f.contentDocument,t=d&&d.querySelector('.t-ed-body');
        return t?f.contentWindow.getComputedStyle(t).lineHeight:null}catch(e){return 'blocked'}})(),
    ends:m.querySelectorAll('.ends .end').length,
    md5src:g.toDataURL('image/png'), ls:Object.keys(localStorage).sort()}}"""


def open_component_render(pg):
    pg.fill('#q', 'Alert'); pg.wait_for_timeout(700)
    pg.click('#hits .hit .insp[data-insp="component:alert"]'); pg.wait_for_timeout(1600)
    # from file:// there are no tabs at all — the banner naming the serve command is the whole
    # artefact section, and that is exactly what the file:// shots are for
    if pg.locator('#insp .tabs button:text-is("Render")').count():
        pg.click('#insp .tabs button:text-is("Render")'); pg.wait_for_timeout(2200)
    pg.evaluate("()=>{const s=[...document.querySelectorAll('#insp .sec')][1];if(s)s.scrollIntoView({block:'start'})}")


def open_edge(pg):
    pg.evaluate("()=>{setFocus(byId.get('component:alert'))}"); pg.wait_for_timeout(1600)
    pg.click('#panel .rel [data-einsp]'); pg.wait_for_timeout(1400)


def open_ruling(pg):
    pg.fill('#q', 's280-D2'); pg.wait_for_timeout(700)
    pg.click('#hits .hit .insp[data-insp="ruling:s280-D2"]'); pg.wait_for_timeout(2000)
    pg.evaluate("()=>{const s=[...document.querySelectorAll('#insp .sec')][1];if(s)s.scrollIntoView({block:'start'})}")


def shoot(br, name, url, scheme, drive=None, w=1280, h=800):
    ctx = br.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme, device_scale_factor=1)
    pg = ctx.new_page(); errs = []; cons = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: cons.append(m.text) if m.type == 'error' else None)
    pg.goto(url, wait_until='load'); pg.wait_for_timeout(1800)
    if drive: drive(pg); pg.wait_for_timeout(1400)
    d = pg.evaluate(PROBE)
    d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
    d['errors'] = errs; d['console'] = cons; d['scheme'] = scheme
    d['viewport'] = f'{w}x{h}'; d['url'] = url
    p = os.path.join(OUT, name + '.png')
    pg.screenshot(path=p); d['bytes'] = os.path.getsize(p)
    print(f"{name:36} modal={str(d['modalOpen']):<5} tabOn={d['tabOn']} iframes={d['iframes']} "
          f"frameLH={d['frameLH']} theme={d['frameTheme']} ends={d['ends']} err={len(errs)} "
          f"con={len(cons)} ls={d['ls']} md5={d['canvasMd5'][:10]} {d['bytes']:,}B")
    ctx.close()
    return d


def main():
    res = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                               args=['--no-sandbox', '--force-device-scale-factor=1'])
        if CONTROL:
            res['kg-119-control-light'] = shoot(br, 'kg-119-control-light', 'file://' + CONTROL, 'light')
            res['kg-120-default-light'] = shoot(br, 'kg-120-default-light', PAGE, 'light')
        for s in ('light', 'dark'):
            res[f'kg-120-file-banner-{s}'] = shoot(
                br, f'kg-120-file-banner-{s}', PAGE, s, open_component_render, h=900)
            if SERVED:
                res[f'kg-120-component-render-{s}'] = shoot(
                    br, f'kg-120-component-render-{s}', SERVED, s, open_component_render, h=900)
                res[f'kg-120-edge-{s}'] = shoot(br, f'kg-120-edge-{s}', SERVED, s, open_edge, h=900)
                res[f'kg-120-ruling-{s}'] = shoot(br, f'kg-120-ruling-{s}', SERVED, s, open_ruling, h=900)
        br.close()
    fp = os.path.join(OUT, 'shots.json')
    old = json.load(open(fp)) if os.path.exists(fp) else {}
    old.update(res); json.dump(old, open(fp, 'w'), indent=1)
    if CONTROL:
        a = res['kg-119-control-light']['canvasMd5']
        b = res['kg-120-default-light']['canvasMd5']
        print('\nDEFAULT CANVAS 1.19 vs 1.20 (light, 1280x800, page defaults, file://):',
              ('SAME ' + a) if a == b else f'DIFF {a} {b}')
    print('wrote', fp)


if __name__ == '__main__':
    main()
