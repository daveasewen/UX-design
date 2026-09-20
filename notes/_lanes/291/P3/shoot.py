#!/usr/bin/env python3
"""291 / P3 - render v12 at 1440x900 and measure slide 10's image boxes.

Reports, for each .pic on 10: the CSS box (width x height), the DRAWN size of
the picture inside it (object-fit:contain letterbox maths, from naturalWidth/
Height), the drawn width as a fraction of the cell width, and the device-pixel
size at DPR 2 against the baked PNG's natural size (the blur check).
Also: cell height, the inner's top/bottom slack inside the 900px slide, and
whether anything overflows.
"""
import json, sys
from playwright.sync_api import sync_playwright

ROOT = "/sessions/fervent-affectionate-carson/mnt/UX-design/"
DECK = "file://" + ROOT + "notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html"
OUT = ROOT + "notes/_lanes/291/P3/"
TAG = sys.argv[1] if len(sys.argv) > 1 else ""

PROBE = r"""() => {
  const o = {};
  o.slides = document.querySelectorAll('section.slide').length;
  o.sections = document.querySelectorAll('section').length;
  o.cols = getComputedStyle(document.querySelector('#s10 .grid4')).gridTemplateColumns;
  const cells = [...document.querySelectorAll('#s10 .grid5 > div')];
  o.cellCount = cells.length;
  o.cellH = cells.map(c => +c.getBoundingClientRect().height.toFixed(1));
  o.cellW = cells.map(c => +c.getBoundingClientRect().width.toFixed(1));
  o.pics = ['an1','an2','an3'].map((id, i) => {
    const im = document.getElementById(id);
    if (!im) return {id, missing:true};
    const r = im.getBoundingClientRect();
    const nw = im.naturalWidth, nh = im.naturalHeight;
    // object-fit: contain
    const s = Math.min(r.width / nw, r.height / nh);
    const dw = nw * s, dh = nh * s;
    const cw = cells[i].getBoundingClientRect().width;
    return {id, box:[+r.width.toFixed(1), +r.height.toFixed(1)],
            natural:[nw, nh],
            drawn:[+dw.toFixed(1), +dh.toFixed(1)],
            pctOfCell:+(100*dw/cw).toFixed(1),
            need2x:[Math.round(dw*2), Math.round(dh*2)],
            enough2x: nw >= dw*2 && nh >= dh*2};
  });
  const s10 = document.getElementById('s10'), sr = s10.getBoundingClientRect();
  const inner = s10.querySelector('.inner'), ir = inner.getBoundingClientRect();
  o.slideH = +sr.height.toFixed(1);
  o.innerH = +ir.height.toFixed(1);
  o.slackTop = +(ir.top - sr.top).toFixed(1);
  o.slackBot = +(sr.bottom - ir.bottom).toFixed(1);
  o.overflow = ir.height > sr.height || ir.top < sr.top - 0.5 || ir.bottom > sr.bottom + 0.5;
  o.scrollOverflow = s10.scrollHeight > Math.ceil(sr.height) + 1;
  const grid = s10.querySelector('.grid5').getBoundingClientRect();
  const h2 = s10.querySelector('h2').getBoundingClientRect();
  o.gapHeadlineToGrid = +(grid.top - h2.bottom).toFixed(1);
  o.gridTop = +(grid.top - sr.top).toFixed(1);
  o.gridBottom = +(grid.bottom - sr.top).toFixed(1);
  // empty band under the last line of copy inside each cell
  o.bandUnderCopy = cells.map(c => {
    const p = c.querySelector('p:last-of-type').getBoundingClientRect();
    return +(c.getBoundingClientRect().bottom - p.bottom).toFixed(1);
  });
  o.pagenum = document.querySelector('#s10 .pagenum').textContent.trim();
  o.anatomy = window.anatomyState ? window.anatomyState() : null;
  return o;
}"""

errs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
    pg.goto(DECK, wait_until="load")
    pg.wait_for_timeout(3200)
    for sid in ["s4", "s6", "s10"]:
        pg.eval_on_selector("#" + sid, "e => e.scrollIntoView()")
        pg.wait_for_timeout(2400)
        pg.locator("#" + sid).screenshot(path=OUT + sid + TAG + ".png")
    pg.eval_on_selector("#s10", "e => e.scrollIntoView()")
    pg.wait_for_timeout(1200)
    res = pg.evaluate(PROBE)
    b.close()

print(json.dumps({"page_errors": errs, "probe": res}, indent=1))
