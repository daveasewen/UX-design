#!/usr/bin/env python3
"""Lane EX3 (#280) — the DRIVEN gate for explorer 1.19.

Two things are proved here, both of them things Dave will do with a mouse:

  1. THE LEGEND DOES NOT MOVE BY ITSELF. Its bounding rect is measured, then three family chips are
     toggled, a node is dug, the scrub is scrubbed and a search is run — the rect must be unchanged
     at every step. Then the new `⇥ side / ⇣ bottom` toggle is pressed: the rect must MOVE. Then the
     page is reloaded in the SAME context: the place must be the one that was chosen.
  2. INSPECT. The modal is opened from a SEARCH row, from a DIG row and from a PATH row; each time
     the record, the relations and the File section must be present, Escape must close it, and the
     dig underneath must survive (Escape belongs to the modal while it is open).

Run twice — once from file:// (the File section must fall back to the path + copy button) and once
against a tiny `python3 -m http.server` (the File section must render the file's contents).

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/explorer-ux/drive.py [BASE_URL]
"""
import json, os, sys
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/explorer-ux/shots')
os.makedirs(OUT, exist_ok=True)
BASE = sys.argv[1] if len(sys.argv) > 1 else ('file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html'))
SERVED = not BASE.startswith('file://')

LEGRECT = """() => {const r=document.getElementById('legend').getBoundingClientRect();
  return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height),
          strip:document.getElementById('legend').classList.contains('strip'),
          place:(typeof legPlace==='undefined')?'?':legPlace,
          ls:Object.keys(localStorage).sort()}}"""

MODAL = """() => {const m=document.getElementById('insp');
  if(!m.classList.contains('on'))return {open:false};
  const secs=[...m.querySelectorAll('.sec>h3')].map(h=>h.textContent.trim());
  const fb=m.querySelector('.fbody');
  return {open:true, id:(m.querySelector('.id')||{}).textContent, title:(m.querySelector('h2')||{}).textContent,
          sections:secs, recRows:m.querySelectorAll('dl.rec dt').length,
          edgeGroups:m.querySelectorAll('.egroup').length, edgeRows:m.querySelectorAll('.erow').length,
          verbs:[...m.querySelectorAll('.egroup .verb')].map(v=>v.textContent.trim()).slice(0,6),
          reads:(m.querySelector('.reads')||{textContent:''}).textContent.trim().slice(0,110),
          paths:[...m.querySelectorAll('.fpath code')].map(c=>c.textContent),
          copyBtns:m.querySelectorAll('.fpath button[data-copy]').length,
          fileNote:[...m.querySelectorAll('.fnote')].map(p=>p.textContent.trim().slice(0,150)),
          fileBody:!!fb, fileChars:fb?fb.innerText.length:0,
          focusIn:m.contains(document.activeElement),
          focusables:m.querySelectorAll('button,[href],input,select,textarea').length}}"""


def step(pg, name, log, extra=None):
    d = pg.evaluate(LEGRECT)
    d['step'] = name
    if extra: d.update(extra)
    log.append(d)
    return d


def main():
    rep = {'base': BASE, 'served': SERVED}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                               args=['--no-sandbox', '--force-device-scale-factor=1'])
        # ---------------- 1. the legend stays put -------------------------------------------------
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}, color_scheme='light',
                             device_scale_factor=1)
        pg = ctx.new_page(); errs = []; cons = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: cons.append(m.text) if m.type == 'error' else None)
        pg.goto(BASE, wait_until='load'); pg.wait_for_timeout(1600)
        log = []
        base_rect = step(pg, 'load', log)
        for fam in ('assets', 'governance', 'uxprinciples'):
            pg.click(f'.chip[data-fam="{fam}"]'); pg.wait_for_timeout(900)
            step(pg, 'chip:' + fam, log)
        pg.evaluate("()=>{setFocus(byId.get('component:button'))}"); pg.wait_for_timeout(1400)
        step(pg, 'dig', log, {'panelRows': pg.evaluate("()=>document.querySelectorAll('.rel[data-id]').length")})
        pg.evaluate("()=>{setT(T-12)}"); pg.wait_for_timeout(700); step(pg, 'scrub-12', log)
        pg.evaluate("()=>{setT(SNAPS.length-1)}"); pg.wait_for_timeout(700); step(pg, 'scrub-home', log)
        pg.fill('#q', 'button'); pg.wait_for_timeout(600); step(pg, 'search', log)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        rects = [(d['x'], d['y'], d['w'], d['h']) for d in log]
        rep['legendStayed'] = all(r == rects[0] for r in rects)
        rep['legendSteps'] = log
        # the toggle MOVES it
        pg.evaluate("()=>{surface()}"); pg.wait_for_timeout(900)
        before = pg.evaluate(LEGRECT)
        pg.click('.lplace'); pg.wait_for_timeout(1000)
        after = pg.evaluate(LEGRECT)
        rep['toggleMoved'] = (before['x'], before['y']) != (after['x'], after['y'])
        rep['toggleBefore'] = before; rep['toggleAfter'] = after
        # ... and a RELOAD in the same context remembers it
        pg.reload(wait_until='load'); pg.wait_for_timeout(1600)
        reloaded = pg.evaluate(LEGRECT)
        rep['remembered'] = reloaded['place'] == after['place']
        rep['afterReload'] = reloaded
        # ... and a chip toggle after the reload still does not move it
        r0 = pg.evaluate(LEGRECT)
        pg.click('.chip[data-fam="assets"]'); pg.wait_for_timeout(900)
        r1 = pg.evaluate(LEGRECT)
        rep['stickyAfterReload'] = (r0['x'], r0['y']) == (r1['x'], r1['y'])
        # a LAYOUT switch does not override a chosen place either
        pg.click('#layout'); pg.wait_for_timeout(1200)
        rep['layoutKeptChoice'] = pg.evaluate(LEGRECT)['place'] == after['place']
        rep['errorsLegend'] = list(errs); rep['consoleLegend'] = list(cons)
        ctx.close()

        # ---------------- 2. INSPECT, from all three row kinds -------------------------------------
        ctx = br.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light',
                             device_scale_factor=1)
        pg = ctx.new_page(); errs2 = []; cons2 = []
        pg.on('pageerror', lambda e: errs2.append(str(e)))
        pg.on('console', lambda m: cons2.append(m.text) if m.type == 'error' else None)
        pg.goto(BASE, wait_until='load'); pg.wait_for_timeout(1600)
        ins = {}
        # (a) a SEARCH row
        pg.fill('#q', 'button'); pg.wait_for_timeout(600)
        pg.click('#hits .hit[data-i="0"] .insp'); pg.wait_for_timeout(1400)
        ins['search'] = pg.evaluate(MODAL)
        ins['search']['digSurvives'] = pg.evaluate("()=>!!focus")
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        ins['searchClosed'] = not pg.evaluate(MODAL)['open']
        # (b) a DIG row — the aside's group rows
        pg.evaluate("()=>{setFocus(byId.get('component:button'))}"); pg.wait_for_timeout(1500)
        pg.click('.rel[data-id] .insp'); pg.wait_for_timeout(1400)
        ins['dig'] = pg.evaluate(MODAL)
        ins['dig']['digSurvives'] = pg.evaluate("()=>!!focus")
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
        ins['digClosed'] = not pg.evaluate(MODAL)['open']
        ins['digStillDug'] = pg.evaluate("()=>focus?focus.id:null")
        # (c) a PATH row
        pg.evaluate("""()=>{const a=byId.get('component:button');
          const t=[...adj.get(a.id)].map(x=>x.other).find(id=>id.startsWith('pattern:')||id.startsWith('snippet:'));
          showPath(a, byId.get(t))}"""); pg.wait_for_timeout(1200)
        ins['pathSteps'] = pg.evaluate("()=>document.querySelectorAll('.path .steps .pstep').length")
        pg.click('.path .steps .pstep .insp'); pg.wait_for_timeout(1400)
        ins['path'] = pg.evaluate(MODAL)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        ins['pathClosed'] = not pg.evaluate(MODAL)['open']
        # (d) the keyboard — `i` on the focused node, and a click OUTSIDE closes
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.evaluate("()=>{setFocus(byId.get('component:button'))}"); pg.wait_for_timeout(1300)
        pg.evaluate("()=>document.body.focus()")
        pg.keyboard.press('i'); pg.wait_for_timeout(1400)
        ins['keyboard'] = pg.evaluate(MODAL)
        pg.mouse.click(8, 8); pg.wait_for_timeout(400)          # the veil
        ins['veilClosed'] = not pg.evaluate(MODAL)['open']
        # (e) a node whose record is a MARKDOWN file (a rule), and one whose record is a directory
        pg.evaluate("""()=>{const r=NODES.find(n=>n.type==='rule'&&n.file);famOn.guidelinerules=1;
          recount();renderStats();renderLegend();openInspect(r)}"""); pg.wait_for_timeout(1800)
        ins['ruleMd'] = pg.evaluate(MODAL)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.evaluate("()=>{openInspect(NODES.find(n=>n.type==='axe'))}"); pg.wait_for_timeout(1200)
        ins['axeDir'] = pg.evaluate(MODAL)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        # (f) served only: the HTTP-failure branch is a REAL fetch of a path that really 404s —
        # a live rule node with its `file` temporarily pointed at a name that does not exist.
        if SERVED:
            pg.evaluate("""()=>{const n=NODES.find(x=>x.type==='rule'&&x.file);
              n.__keep=n.file;n.file='no-such-file-EX3.md';
              famOn.guidelinerules=1;recount();renderStats();renderLegend();openInspect(n)}""")
            pg.wait_for_timeout(1600)
            ins['http404'] = pg.evaluate(MODAL)
            pg.evaluate("()=>{const n=NODES.find(x=>x.__keep);if(n){n.file=n.__keep;delete n.__keep}}")
            pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        rep['inspect'] = ins
        rep['errorsInspect'] = list(errs2); rep['consoleInspect'] = list(cons2)
        ctx.close()
        br.close()

    tag = 'served' if SERVED else 'file'
    fp = os.path.join(OUT, f'drive-{tag}.json')
    json.dump(rep, open(fp, 'w'), indent=1)
    print(f"--- {tag} ({BASE}) ---")
    print('legend rect unchanged through chips/dig/scrub/search :', rep['legendStayed'],
          '  steps:', [d['step'] for d in rep['legendSteps']])
    print('  rect at every step                                 :', rects[0], 'x', len(rects))
    print('toggle moves it                                      :', rep['toggleMoved'],
          rep['toggleBefore']['place'], '->', rep['toggleAfter']['place'])
    print('reload remembers it                                  :', rep['remembered'],
          rep['afterReload']['place'], 'ls', rep['afterReload']['ls'])
    print('sticky after reload / layout switch                  :', rep['stickyAfterReload'], rep['layoutKeptChoice'])
    for k in ('search', 'dig', 'path', 'keyboard', 'ruleMd', 'axeDir', 'http404'):
        if k not in ins: continue
        d = ins[k]
        print(f"modal {k:9} open={d.get('open')} rec={d.get('recRows')} groups={d.get('edgeGroups')} "
              f"rows={d.get('edgeRows')} paths={d.get('paths')} body={d.get('fileBody')} "
              f"chars={d.get('fileChars')} focusIn={d.get('focusIn')} copy={d.get('copyBtns')}")
        print(f"        note: {(d.get('fileNote') or [''])[-1][:120]}")
    print('closed by Escape (search/dig/path)                    :',
          rep['inspect']['searchClosed'], rep['inspect']['digClosed'], rep['inspect']['pathClosed'])
    print('closed by click outside                               :', rep['inspect']['veilClosed'])
    print('dig survives the modal                                :', rep['inspect']['digStillDug'])
    print('page errors (uncaught)                                :', rep['errorsLegend'], rep['errorsInspect'])
    print('console errors                                        :', rep['consoleLegend'], rep['consoleInspect'])
    print('wrote', fp)


if __name__ == '__main__':
    main()
