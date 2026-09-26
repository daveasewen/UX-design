import os, json
from playwright.sync_api import sync_playwright
W=os.path.expanduser('~/cold/cand-r1'); URL='file://'+W+'/out/index.html'
JS=r"""() => {
  const out = [];
  document.querySelectorAll('.ceo-view:not([hidden]) .cn-table table').forEach(function (t) {
    const rows = Array.from(t.querySelectorAll('tbody tr'));
    const tall = rows.filter(function (r) { return r.getBoundingClientRect().height > 40; });
    const heads = Array.from(t.querySelectorAll('thead th')).map(function (h) { return h.textContent; });
    const wrapped = {};
    tall.forEach(function (r) { Array.from(r.children).forEach(function (c, i) { if (c.firstElementChild && c.firstElementChild.getClientRects().length > 1) { wrapped[heads[i]] = 1; } }); });
    out.push(t.querySelector('caption').firstChild.textContent + ': ' + tall.length + '/' + rows.length + ' tall; wraps in ' + Object.keys(wrapped).join(', ') + '; scroll ' + t.parentElement.scrollWidth + '/' + t.parentElement.clientWidth);
  });
  return out;
}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL']); pg=b.new_page(viewport={'width':1440,'height':900})
    for v in ['accounts','liquidity','payments','fx','risk','trade','reports','messages']:
        pg.goto(URL+'?view='+v); pg.wait_for_timeout(700)
        print(v, pg.evaluate(JS))
    b.close()
