import json
from playwright.sync_api import sync_playwright

DECK = "file:///sessions/fervent-affectionate-carson/mnt/UX-design/notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html"
OUT  = "/sessions/fervent-affectionate-carson/mnt/UX-design/notes/_lanes/291/P2/"

errs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
    pg.goto(DECK, wait_until="load")
    pg.wait_for_timeout(3000)

    for sid in ["s4", "s5", "s6", "s10"]:
        pg.eval_on_selector("#" + sid, "e => e.scrollIntoView()")
        pg.wait_for_timeout(2600)
        if sid != "s5":
            pg.locator("#" + sid).screenshot(path=OUT + sid + ".png")

    pg.eval_on_selector("#s10", "e => e.scrollIntoView()")
    pg.wait_for_timeout(1500)
    res = pg.evaluate("""() => {
      const out = {};
      out.slides = document.querySelectorAll('section.slide').length;
      out.cells = document.querySelectorAll('#s10 .grid5 > div').length;
      out.cols = getComputedStyle(document.querySelector('#s10 .grid4')).gridTemplateColumns;
      out.h2 = document.querySelector('#s10 h2').textContent;
      out.eyebrow = document.querySelector('#s10 .label').textContent;
      out.foot = document.querySelector('#s10 .foot').textContent.slice(0,40);
      out.gbHost = (() => { const c = document.getElementById('gb');
        return c ? {parent: c.parentNode.id, w: c.width, h: c.height,
                    rect: c.getBoundingClientRect().left} : null; })();
      const prints = {};
      ['gbPrint','bkPrint','brPrint','ctPrint','lwPrint','lnPrint','amPrint','cpPrint'].forEach(id => {
        const im = document.getElementById(id);
        prints[id] = im ? (im.src||'').slice(0,11) + '/len=' + (im.src||'').length : 'MISSING';
      });
      out.prints = prints;
      out.anatomy = window.anatomyState ? window.anatomyState() : null;
      out.orphans = ['an4','an5'].map(i => !!document.getElementById(i));
      out.gbStats = window.gbStats ? 'fn' : 'none';
      return out;
    }""")
    b.close()

print(json.dumps({"page_errors": errs, "probe": res}, indent=1)[:6000])
