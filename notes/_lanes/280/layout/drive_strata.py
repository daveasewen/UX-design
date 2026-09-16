#!/usr/bin/env python3
"""Lane LY (#280) — the strata driver. Two things it proves, in one fresh context each:

  1. BANDS — with `?layout=strata` every node's LIVE y is its own `y2`, inside its view's band.
  2. The rest still works in strata — the tool-row switch both ways, a dig (focus), the scrub line,
     a legend chip toggle, search-and-fly, and Escape back to the surface — with page errors [] at
     the end of the run and the band invariant still holding after every one of them.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/layout/drive_strata.py
"""
import json, os
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
URL = 'file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html')

BAND_CHECK = """() => {
  const by = Object.fromEntries((KG.bands||[]).map(b => [b.id, b]));
  let out = 0, noband = 0, wrong = 0;
  for (const n of NODES) {
    const b = by[n.view]; if (!b) { noband++; continue; }
    if (n.y !== n.oy2) wrong++;
    if (n.y < b.y0 || n.y > b.y1) out++;
  }
  return {layout: LAYOUT, outOfBand: out, noBand: noband, notAtY2: wrong, n: NODES.length};
}"""

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
    log = {}

    # ---- 1. the band invariant, never driven
    ctx = br.new_context(viewport={'width': 1280, 'height': 800})
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL + '?layout=strata', wait_until='load'); pg.wait_for_timeout(1500)
    log['bands_never_driven'] = pg.evaluate(BAND_CHECK); log['bands_errors'] = list(errs)
    print('1 bands (never driven):', log['bands_never_driven'], 'errors', errs)
    ctx.close()

    # ---- 2. everything else, driven
    ctx = br.new_context(viewport={'width': 1280, 'height': 800})
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
    pg.goto(URL, wait_until='load'); pg.wait_for_timeout(1200)
    steps = {}
    steps['opens_as'] = pg.evaluate('() => LAYOUT')
    pg.click('#layout'); pg.wait_for_timeout(900)
    steps['after_switch'] = pg.evaluate(BAND_CHECK)
    steps['legend_is_strip'] = pg.evaluate("() => legend.classList.contains('strip')")

    # a dig: the highest-degree shown component
    pg.evaluate("() => {const n = LIVE.filter(x => x.type === 'component').sort((a,b) => b.deg - a.deg)[0]; setFocus(n)}")
    pg.wait_for_timeout(1200)
    steps['dig'] = pg.evaluate("""() => ({focus: focus && focus.label, halo: adj.get(focus.id).length,
      sectors: (sectors||[]).length, panel: (document.getElementById('panel').innerText||'').slice(0,40).trim()})""")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(1200)
    steps['after_surface'] = pg.evaluate(BAND_CHECK)

    # the scrub line, 12 days back and home again
    pg.evaluate('() => setT(T - 12)'); pg.wait_for_timeout(600)
    steps['scrub_back'] = pg.evaluate("() => document.getElementById('scounts').innerText.replace(/\\s+/g,' ').trim()")
    pg.evaluate('() => setT(SNAPS.length - 1)'); pg.wait_for_timeout(600)
    steps['scrub_home'] = pg.evaluate("() => document.getElementById('scounts').innerText.replace(/\\s+/g,' ').trim()")

    # a legend chip: the Constitution on, then off
    pg.click('.chip[data-fam="governance"]'); pg.wait_for_timeout(1000)
    steps['constitution_on'] = pg.evaluate("""() => ({stats: document.getElementById('stats').innerText.replace(/\\s+/g,' ').trim(),
      band: Object.assign({}, BANDBY_probe())})""".replace('BANDBY_probe()',
      "(()=>{const b=(KG.bands||[]).find(x=>x.id==='constitution');return {y0:b.y0,y1:b.y1,shown:famOn.governance===1}})()"))
    steps['constitution_bands'] = pg.evaluate(BAND_CHECK)
    pg.click('.chip[data-fam="governance"]'); pg.wait_for_timeout(900)

    # search → fly → dig → surface
    pg.fill('#q', 'button'); pg.wait_for_timeout(500)
    pg.click('.hit[data-i="0"]'); pg.wait_for_timeout(1800)
    steps['search_fly'] = pg.evaluate("() => focus && focus.label")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(1200)

    pg.click('#layout'); pg.wait_for_timeout(900)
    steps['back_to_force'] = pg.evaluate("() => ({layout: LAYOUT, atOy: NODES.every(n => n.y === n.oy)})")
    steps['legend_is_strip_after'] = pg.evaluate("() => legend.classList.contains('strip')")
    steps['errors'] = errs
    log['driven'] = steps
    for k, v in steps.items(): print(f"2 {k}: {v}")
    ctx.close()
    br.close()

json.dump(log, open(os.path.join(REPO, 'notes/_lanes/280/layout/shots/drive.json'), 'w'), indent=1)
