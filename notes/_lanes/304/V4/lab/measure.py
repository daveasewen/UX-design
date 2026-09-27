"""measure.py <out-prefix> <file> [theme]: screenshot 1440 light+dark full page + per-svg measurement."""
import os, sys, json
from playwright.sync_api import sync_playwright
OUT, FILE = sys.argv[1], sys.argv[2]
JS = r"""() => {
  const R = [];
  for (const svg of document.querySelectorAll('svg.dv-svg')) {
    const b = svg.getBoundingClientRect(); if (!b.width) continue;
    const labs = [...svg.querySelectorAll('.dv-label[text-anchor=middle]')];
    const hidden = labs.filter(t => t.getAttribute('visibility') === 'hidden').length;
    let minx = 1e9, cutN = 0; const sb = svg.getBoundingClientRect();
    for (const t of svg.querySelectorAll('text')) { const r = t.getBoundingClientRect(); if (!r.width) continue; if (r.left < sb.left - 0.5) cutN++; minx = Math.min(minx, r.left - sb.left); }
    // collisions among visible middle labels on the same baseline
    let coll = 0; const vis = labs.filter(t => t.getAttribute('visibility') !== 'hidden');
    for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) { const a = vis[i].getBoundingClientRect(), c = vis[j].getBoundingClientRect(); if (a.top === c.top && a.right > c.left && c.right > a.left) coll++; }
    const fig = svg.closest('figure'); const fb = fig ? fig.getBoundingClientRect() : null;
    R.push({type: fig && fig.getAttribute('data-dv-type'), box: [Math.round(b.width), Math.round(b.height)], fig: fb && [Math.round(fb.width), Math.round(fb.height)],
            viewBox: svg.getAttribute('viewBox'), pl: svg.getAttribute('data-pl'), plfit: svg.getAttribute('data-pl-fit'), labels: labs.length, hidden, coll, minx: Math.round(minx * 10) / 10, cutN});
  }
  return R; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for theme in ('light', 'dark'):
        c = b.new_context(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1); pg = c.new_page()
        pg.goto('file://' + os.path.abspath(FILE)); pg.wait_for_timeout(1200)
        pg.evaluate("t => { document.documentElement.setAttribute('data-theme', t); }", theme)
        pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(2000)
        pass
        info = pg.evaluate(JS)
        pg.screenshot(path=OUT + '-' + theme + '.png', full_page=True)
        print(theme, json.dumps(info)); c.close()
    b.close()
