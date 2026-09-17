#!/usr/bin/env python3
"""Lane EX4 (#280) — the DRIVEN gate for explorer 1.20, s280-D2.

What is proved here, all of it by real clicks on a SERVED page:

  1. A COMPONENT'S RENDER TAB IS THE SNIPPET, AND type.css APPLIED TO IT. The modal is opened from a
     search row, the RENDER tab is clicked, and the iframe's own document is asked — from the parent,
     which is same-origin — for (a) the snippet's root element and (b) a COMPUTED style that only
     `knowledge/canon/type.css` can produce. `document.fonts.check` is NOT proof and is banned: a font
     may be present and the stylesheet still 404 (that is exactly the failure gen_showroom.py's rebase
     gate exists to kill). So the assertion is `getComputedStyle(p.t-ed-body).lineHeight === '24px'`,
     which is a declaration in type.css and is `normal` without it.
  2. EVERY OTHER KIND OPENS WITH CONTENT PRESENT — a snippet, a rule (its guideline markdown with its
     own row highlighted), a ruling (its record out of _rulings.json), an icon (drawn at 48 and 16 on
     both grounds), an artefact (its file), and AN EDGE (its own record, both ends as buttons).
  3. THE TRAIL WALKS — an edge opened from inside a node's modal, then one of its ends, then back by a
     crumb, without the modal ever closing.
  4. FROM `file://`, NEVER DRIVEN: the banner names `python3 knowledge/_serve_explorer.py`, and there
     are no page errors.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/explorer-artefacts/drive.py <BASE_URL|file://…>
"""
import json, os, sys
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/explorer-artefacts/shots')
os.makedirs(OUT, exist_ok=True)
BASE = sys.argv[1] if len(sys.argv) > 1 else ('file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html'))
SERVED = not BASE.startswith('file://')

MODAL = """() => {const m=document.getElementById('insp');
  if(!m.classList.contains('on'))return {open:false};
  return {open:true, id:(m.querySelector('.id')||{}).textContent,
          title:(m.querySelector('h2')||{}).textContent,
          kind:(m.querySelector('.kind')||{}).textContent,
          sections:[...m.querySelectorAll('.sec>h3')].map(h=>h.textContent.trim()),
          recRows:m.querySelectorAll('dl.rec dt').length,
          tabs:[...m.querySelectorAll('.tabs button')].map(b=>b.textContent.trim()),
          tabOn:[...m.querySelectorAll('.tabs button[aria-selected="true"]')].map(b=>b.textContent.trim()),
          paneChars:(m.querySelector('[data-pane]')||{innerText:''}).innerText.length,
          iframes:m.querySelectorAll('iframe.rframe').length,
          icells:m.querySelectorAll('.icell').length,
          mdHit:!!m.querySelector('#mdhit'),
          mdHitText:(m.querySelector('#mdhit')||{innerText:''}).innerText.trim().slice(0,90),
          ends:m.querySelectorAll('.ends .end').length,
          crumbs:[...m.querySelectorAll('.crumbs button,.crumbs .here')].map(b=>b.textContent.trim()),
          paths:[...m.querySelectorAll('.fpath code')].map(c=>c.textContent),
          notes:[...m.querySelectorAll('.fnote')].map(p=>p.textContent.trim().slice(0,400)),
          focusIn:m.contains(document.activeElement)}}"""

# THE RENDER PROOF. Asked of the FRAME's document from the parent (same-origin srcdoc), never of a
# font. `lineHeight` on `.t-ed-body` is 24px in knowledge/canon/type.css and `normal` without it.
FRAME = """() => {const f=document.querySelector('#insp iframe.rframe');
  if(!f)return {frame:false};
  const d=f.contentDocument;
  if(!d||!d.body)return {frame:true, doc:false};
  const root=d.querySelector('body>div[id], body>main, body>div, body>*');
  const links=[...d.querySelectorAll('link[rel="stylesheet"]')].map(l=>l.getAttribute('href'));
  const t=d.querySelector('.t-ed-body, .t-cm-body, [class*="t-"]');
  const cs=t?f.contentWindow.getComputedStyle(t):null;
  const body=f.contentWindow.getComputedStyle(d.body);
  return {frame:true, doc:true,
    theme:d.body.getAttribute('data-theme'),
    apolloTheme:d.documentElement.getAttribute('data-apollo-theme'),
    sandbox:f.getAttribute('sandbox'),
    rootId:root?(root.id||root.tagName):null,
    nodes:d.body.querySelectorAll('*').length,
    links:links,
    typeEl:t?t.className:null,
    typeLineHeight:cs?cs.lineHeight:null,
    typeFontSize:cs?cs.fontSize:null,
    bodyBg:body.backgroundColor,
    sheets:[...d.styleSheets].map(s=>{try{return (s.href||'inline')+':'+s.cssRules.length}catch(e){return (s.href||'inline')+':blocked'}})}}"""


def open_by_search(pg, term, want_id):
    """Open a node's modal the way Dave does — type in the search box and press the row's `i`."""
    pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
    pg.fill('#q', ''); pg.wait_for_timeout(150)
    pg.fill('#q', term); pg.wait_for_timeout(700)
    sel = '#hits .hit .insp[data-insp="%s"]' % want_id.replace('"', '\\"')
    if pg.locator(sel).count() == 0:
        return None
    pg.click(sel)
    pg.wait_for_timeout(1600)
    return pg.evaluate(MODAL)


def click_tab(pg, label):
    """From `file://` there are no tabs at all — the artefact section is the banner naming the serve
    command, which is what the never-driven file:// run is there to record. So a missing tab is a
    recorded fact, not a crash."""
    sel = f'#insp .tabs button:text-is("{label}")'
    if pg.locator(sel).count() == 0:
        return False
    pg.click(sel); pg.wait_for_timeout(1800)
    return True


def main():
    rep = {'base': BASE, 'served': SERVED}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                               args=['--no-sandbox', '--force-device-scale-factor=1'])
        ctx = br.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light',
                             device_scale_factor=1)
        pg = ctx.new_page(); errs = []; cons = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: cons.append(m.text) if m.type == 'error' else None)
        pg.goto(BASE, wait_until='load'); pg.wait_for_timeout(1700)
        got = {}

        # ---------------- 1. a COMPONENT — the RENDER tab -----------------------------------------
        m = open_by_search(pg, 'Alert', 'component:alert')
        got['component'] = m
        if m:
            click_tab(pg, 'Render')
            got['componentRender'] = pg.evaluate(MODAL)
            got['componentFrame'] = pg.evaluate(FRAME)
            # the SOURCE tab of the same component
            click_tab(pg, 'Snippet source')
            got['componentSource'] = pg.evaluate(MODAL)
            click_tab(pg, 'The meta record')
            got['componentMeta'] = pg.evaluate(MODAL)

        # ---------------- 2. the SNIPPET itself ---------------------------------------------------
        got['snippet'] = open_by_search(pg, 'Alert', 'snippet:Alert.reference.html')
        if got['snippet']:
            click_tab(pg, 'Render')
            got['snippetRender'] = pg.evaluate(MODAL)
            got['snippetFrame'] = pg.evaluate(FRAME)

        # ---------------- 3. a RULE — its guideline, its own row highlighted -----------------------
        got['rule'] = open_by_search(pg, 'aca-001', 'rule:aca-001')
        if got['rule']:
            pg.wait_for_timeout(1600)
            got['ruleTab'] = pg.evaluate(MODAL)

        # ---------------- 4. a RULING — its record out of _rulings.json ----------------------------
        got['ruling'] = open_by_search(pg, 's280-D2', 'ruling:s280-D2')
        if got['ruling']:
            pg.wait_for_timeout(1800)
            got['rulingTab'] = pg.evaluate(MODAL)

        # ---------------- 5. an ICON — drawn at 48 and 16, both grounds ----------------------------
        got['icon'] = open_by_search(pg, 'accessibility', 'icon:accessibility')
        if got['icon']:
            pg.wait_for_timeout(1400)
            got['iconTab'] = pg.evaluate(MODAL)

        # ---------------- 6. an ARTEFACT — the filed file ------------------------------------------
        got['artefact'] = open_by_search(pg, '_serve_explorer', 'artefact:knowledge/_serve_explorer.py')
        if got['artefact']:
            pg.wait_for_timeout(1400)
            got['artefactTab'] = pg.evaluate(MODAL)

        # ---------------- 7. an EDGE, and the TRAIL ------------------------------------------------
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.evaluate("()=>{setFocus(byId.get('component:alert'))}"); pg.wait_for_timeout(1500)
        got['panelEdgeButtons'] = pg.evaluate("()=>document.querySelectorAll('.rel [data-einsp]').length")
        pg.click('#panel .rel [data-einsp]'); pg.wait_for_timeout(1200)
        got['edgeFromPanel'] = pg.evaluate(MODAL)
        # walk: one END of the edge -> its own artefact, then a crumb BACK to the edge
        pg.click('#insp .ends .end'); pg.wait_for_timeout(1500)
        got['edgeEndWalk'] = pg.evaluate(MODAL)
        crumbs = pg.evaluate("()=>document.querySelectorAll('#insp .crumbs button').length")
        got['crumbButtons'] = crumbs
        if crumbs:
            pg.click('#insp .crumbs button'); pg.wait_for_timeout(1300)
            got['afterCrumb'] = pg.evaluate(MODAL)
        got['stillOpenThroughWalk'] = pg.evaluate("()=>document.getElementById('insp').classList.contains('on')")
        # an edge opened from INSIDE a node modal, from the relations section
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        m = open_by_search(pg, 'Alert', 'component:alert')
        pg.click('#insp .erow [data-einsp]'); pg.wait_for_timeout(1200)
        got['edgeFromModal'] = pg.evaluate(MODAL)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        got['closes'] = not pg.evaluate(MODAL)['open']
        got['digSurvives'] = pg.evaluate("()=>focus?focus.id:null")

        rep['probes'] = got
        rep['errors'] = list(errs); rep['console'] = list(cons)
        ctx.close(); br.close()

    name = 'drive-served.json' if SERVED else 'drive-file.json'
    fp = os.path.join(OUT, name)
    json.dump(rep, open(fp, 'w'), indent=1)
    print('wrote', fp)
    for k, v in got.items():
        if isinstance(v, dict) and v.get('open'):
            print(f"  {k:18} {str(v.get('title'))[:26]:28} tabs={v.get('tabs')} on={v.get('tabOn')} "
                  f"pane={v.get('paneChars')} iframes={v.get('iframes')} icells={v.get('icells')} "
                  f"mdHit={v.get('mdHit')} ends={v.get('ends')}")
        else:
            print(f"  {k:18} {v if not isinstance(v, dict) else 'CLOSED/None'}")
    fr = got.get('componentFrame') or {}
    print("  RENDER PROOF:", {k: fr.get(k) for k in
                              ('frame', 'doc', 'rootId', 'nodes', 'theme', 'apolloTheme', 'sandbox',
                               'typeEl', 'typeLineHeight', 'links', 'sheets')})
    print("  page errors:", rep['errors'])
    print("  console errors:", rep['console'])


if __name__ == '__main__':
    main()
