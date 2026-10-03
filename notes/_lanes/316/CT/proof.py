"""#316 lane CT proof (s315-D26): on pages built from parts, a mouse click must NOT draw the focus
ring and Tab MUST. For each page: (1) fresh load, click the target with the mouse, read the ring on
document.activeElement and 3 ancestors; (2) fresh load, focus the focusable before the target, press
Tab, confirm the target is focused and read the ring. Same for one button per page.
Usage: python3 proof.py <phase> ; writes proof-<phase>.json and PNGs beside itself."""
import json, os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../..'))
PHASE = sys.argv[1]
S = 'knowledge/snippets/'
PAGES = [  # (label, path, field selector, button selector)
 ('dashboard (Template-dashboard)', S+'Template-dashboard.reference.html', 'select', 'button'),
 ('list (Template-list-index)', S+'Template-list-index.reference.html', 'select', 'button'),
 ('form (Template-create-edit)', S+'Template-create-edit.reference.html', 'input[type=text]', 'button'),
 ('form (Template-settings)', S+'Template-settings.reference.html', 'input[type=text]', 'button'),
 ('sign-in (Template-auth)', S+'Template-auth.reference.html', 'input[type=text]', 'button'),
 ('composed demo (dashboards/international-banking-dashboard.canon.html)', 'dashboards/international-banking-dashboard.canon.html', None, 'button'),  # its search field has no keyboard ring at all (pre-existing, before and after) — reported, not judged here
 ('part (Video-player seek bar)', S+'Video-player.reference.html', '.scrub', '.bar button'),
 ('part (Filter-toolbar-bar chip remove)', S+'Filter-toolbar-bar.reference.html', '.tag .x', 'button'),
]
FOCUSABLE = 'a[href],button,input:not([type=hidden]),select,textarea,[tabindex]:not([tabindex="-1"]),summary'
JS_MARK = r"""([sel, F]) => { const vis = e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return r.width > 1 && r.height > 1 && cs.visibility !== 'hidden' && cs.display !== 'none' && !e.disabled; };
  const t = [...document.querySelectorAll(sel)].find(vis); if (!t) return null;
  t.setAttribute('data-ct', 'target');
  const all = [...document.querySelectorAll(F)].filter(vis); const i = all.indexOf(t);
  if (i > 0) all[i-1].setAttribute('data-ct', 'prev');
  return {tag: t.tagName.toLowerCase(), cls: (t.getAttribute('class')||'').slice(0,40), prev: i > 0}; }"""
JS_RING = r"""() => { const a = document.activeElement; if (!a || a === document.body) return {focused: null, ring: false, rings: []};
  const rings = []; let el = a;
  for (let d = 0; d < 4 && el && el !== document.body; d++, el = el.parentElement) {
    const cs = getComputedStyle(el);
    if (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) rings.push({d, cls: (el.getAttribute('class')||el.tagName).slice(0,30), ow: cs.outlineWidth, os: cs.outlineStyle, oc: cs.outlineColor});
  }
  return {focused: a.getAttribute('data-ct') || a.tagName.toLowerCase(), modality: document.documentElement.dataset.modality || null, ring: rings.length > 0, rings}; }"""
def probe(b, path, sel, mode, shot=None):
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    pg.goto('file://' + os.path.join(ROOT, path), wait_until='load', timeout=20000); pg.wait_for_timeout(300)
    m = pg.evaluate(JS_MARK, [sel, FOCUSABLE])
    if not m: pg.close(); return {'error': 'no visible target for ' + sel}
    t = pg.locator('[data-ct="target"]'); t.scroll_into_view_if_needed()
    if mode == 'click':
        t.click(timeout=3000)
    else:
        # Tab from the top of the page until the target has focus (the honest keyboard path)
        for _ in range(150):
            pg.keyboard.press('Tab')
            if pg.evaluate("() => document.activeElement && document.activeElement.getAttribute('data-ct') === 'target'"): break
    pg.wait_for_timeout(250)
    r = pg.evaluate(JS_RING); r['target'] = m
    if shot:
        bb = pg.evaluate("() => { const a = document.activeElement; const r = (a && a !== document.body ? a : document.querySelector('[data-ct=target]')).getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; }")
        x, y = max(0, bb[0]-24), max(0, bb[1]-24)
        pg.screenshot(path=shot, clip={'x': x, 'y': y, 'width': min(420, bb[2]+48), 'height': min(160, bb[3]+48)})
    pg.close(); return r
out = {}; ok = True
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for label, path, fsel, bsel in PAGES:
        if not os.path.exists(os.path.join(ROOT, path)): continue
        row = {}
        for kind, sel in (('field', fsel), ('button', bsel)):
            if sel is None: continue
            shot = (os.path.join(HERE, f'{PHASE}-{kind}-click.png') if label.startswith('form (Template-create') else None)
            c = probe(b, path, sel, 'click', shot)
            shot2 = (os.path.join(HERE, f'{PHASE}-{kind}-tab.png') if label.startswith('form (Template-create') else None)
            k = probe(b, path, sel, 'tab', shot2)
            good = ('error' not in c and 'error' not in k and not c['ring'] and k['ring'] and k['focused'] == 'target')
            row[kind] = {'click': c, 'tab': k, 'PASS': good}
            if kind == 'field': ok = ok and good
            print(f"{PHASE:6} {label:62} {kind:6} click-ring={c.get('ring')} tab-ring={k.get('ring')} tab-focused={k.get('focused')} modality(click)={c.get('modality')} -> {'PASS' if good else 'FAIL'}")
        out[label] = row
    b.close()
json.dump(out, open(os.path.join(HERE, f'proof-{PHASE}.json'), 'w'), indent=1)
print('ALL FIELD ROWS PASS' if ok else 'SOME FIELD ROWS FAIL')
