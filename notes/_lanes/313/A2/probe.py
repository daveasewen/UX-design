import os, json, sys
from playwright.sync_api import sync_playwright
K='/tmp/a2/knowledge/snippets/'
OUT='/tmp/a2_probe'
GAPJS = r"""(t) => {
  const D = 760;
  document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * D; });
  const fig = document.querySelector('figure.dv[data-dv-type="stacked-area"]');
  const svg = fig.querySelector('svg.dv-svg');
  const bands = [...svg.querySelectorAll('path.dv-band')];
  const pts = (el) => { const d = el.getAttribute('d'); const nums = d.replace(/[MLZ]/g,' ').trim().split(/[\s,]+/).map(Number);
     const m = el.getScreenCTM(); const out = [];
     for (let i = 0; i < nums.length; i += 2) { const p = new DOMPoint(nums[i], nums[i+1]).matrixTransform(m); out.push([p.x, p.y]); } return out; };
  const sv = svg.getScreenCTM();
  const base = new DOMPoint(0, svg.viewBox.baseVal.height - (+svg.getAttribute('data-pb') || 30)).matrixTransform(sv).y;
  const P = bands.map(pts); const nc = P[0].length / 2;
  let minGap = 1e9, maxGap = -1e9;
  for (let i = 1; i < P.length; i++) for (let k = 0; k < nc; k++) {
    const topLow = P[i-1][k][1], footUp = P[i][2*nc-1-k][1];
    const g = topLow - footUp; minGap = Math.min(minGap, g); maxGap = Math.max(maxGap, g); }
  const footDev = Math.max(...P[0].slice(nc).map(p => Math.abs(p[1] - base)));
  const top = Math.min(...P[P.length-1].slice(0, nc).map(p => p[1]));
  const op = (sel) => [...svg.querySelectorAll(sel)].map(e => +getComputedStyle(e).opacity);
  const mk = op('g.dv-marker'), ky = op('text.dv-barkey');
  return {t, f: +getComputedStyle(svg).getPropertyValue('--dvfa'), minGap: +minGap.toFixed(3), maxGap: +maxGap.toFixed(3),
          footDev: +footDev.toFixed(3), stackH: +(base - top).toFixed(1), markersMaxOpacity: Math.max(...mk), keysMaxOpacity: Math.max(...ky)};
}"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for w, url in ((1180, 'Chart-stacked-area.reference.html'), (760, 'Chart-stacked-area.reference.html'), (1181, '../_tests/chart-engine/stacked-area.html')):
        pg = b.new_page(viewport={"width": w, "height": 900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto('file://' + K + url); pg.wait_for_timeout(300)
        rows = [pg.evaluate(GAPJS, t) for t in (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)]
        # long settle: let every animation finish (markers/keys fade after one growth)
        pg.evaluate("() => document.getAnimations().forEach(a => a.finish())")
        rows.append(pg.evaluate(GAPJS.replace("a.pause(); a.currentTime = t * D;", ""), 9))
        if w == 1180:
            for t in (0.25, 0.5):
                pg.evaluate(GAPJS, t)
                pg.locator('figure.dv[data-dv-type="stacked-area"] svg.dv-svg').screenshot(path=f"{OUT}/sa-t{int(t*100):02d}.png")
            pg.evaluate("() => document.getAnimations().forEach(a => a.finish())")
            pg.locator('figure.dv[data-dv-type="stacked-area"] svg.dv-svg').screenshot(path=f"{OUT}/sa-t100.png")
        res[f"motion-{w}-{url.split('/')[-1]}"] = {"rows": rows, "pageerrors": errs}; pg.close()
    # reduced motion: the final frame at once
    pg = b.new_page(viewport={"width": 1180, "height": 900}, reduced_motion="reduce")
    pg.goto('file://' + K + 'Chart-stacked-area.reference.html'); pg.wait_for_timeout(300)
    res["reduce"] = pg.evaluate(GAPJS.replace("document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * D; });", ""), -1); pg.close()
    # THE CAP — 8 series on the stacked area, 8 categories on the donut
    CAPJS = r"""([type, n]) => {
      const fig = document.querySelector('figure.dv[data-dv-type="' + type + '"]');
      const cats = type === 'donut' ? Array.from({length: n}, (_, i) => 'C' + (i + 1)) : ['Q1','Q2','Q3','Q4'];
      const series = type === 'donut' ? [{name: 'Cash', values: cats.map((_, i) => 10 + i)}]
        : Array.from({length: n}, (_, s) => ({name: 'S' + (s + 1), values: cats.map((_, i) => 5 + s + i)}));
      dvRender(fig, {type, categories: cats, series, caption: 'cap probe'});
      const svg = fig.querySelector('svg.dv-svg'), t = fig.querySelector('table.dv-table');
      const marks = type === 'donut' ? svg.querySelectorAll('path.dv-donut-seg').length : svg.querySelectorAll('path.dv-band').length;
      return {type, authored: n, marksDrawn: marks,
        tableHead: [...t.querySelectorAll('thead th')].map(e => e.textContent),
        tableRows: t.querySelectorAll('tbody tr').length,
        tips: [...svg.querySelectorAll('[data-tip]')].map(e => e.getAttribute('data-tip')).filter(s => /Other/.test(s)).slice(0, 3)}; }"""
    for snip, typ in (('Chart-stacked-area.reference.html', 'stacked-area'), ('Chart-donut.reference.html', 'donut')):
        pg = b.new_page(viewport={"width": 1180, "height": 900}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto('file://' + K + snip); pg.wait_for_timeout(200)
        try: res[f"cap-{typ}"] = [pg.evaluate(CAPJS, [typ, n]) for n in (6, 8)]
        except Exception as e: res[f"cap-{typ}"] = str(e)[:400]
        res[f"cap-{typ}-errors"] = errs; pg.close()
    b.close()
json.dump(res, open(f"{OUT}/probe.json", "w"), indent=1)
print(json.dumps(res, indent=None)[:6000])
