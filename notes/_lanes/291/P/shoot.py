import json, sys
from playwright.sync_api import sync_playwright

DECK = "file:///sessions/fervent-affectionate-carson/mnt/UX-design/notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html"
OUT  = "/sessions/fervent-affectionate-carson/mnt/UX-design/notes/_lanes/291/P/"

errs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
    pg.goto(DECK, wait_until="load")
    pg.wait_for_timeout(2500)

    for sid in ["s4", "s5", "s6", "s10"]:
        pg.eval_on_selector("#" + sid, "e => e.scrollIntoView()")
        pg.wait_for_timeout(2600)
        pg.locator("#" + sid).screenshot(path=OUT + sid + ".png")

    # back to s4 so the snap check reads a drawn canvas
    pg.eval_on_selector("#s4", "e => e.scrollIntoView()")
    pg.wait_for_timeout(1500)
    res = pg.evaluate("""() => {
      const out = {};
      out.canvases = ['lw','ln','ct','br','cp'].map(id => {
        const c = document.getElementById(id);
        return {id, present: !!c, w: c ? c.width : 0, h: c ? c.height : 0};
      });
      out.probes = {lw: typeof window.lwStats, ln: typeof window.lineStats,
                    lwSnap: typeof window.lwSnap, lnSnap: typeof window.lnSnap,
                    linePage: typeof window.linePage, lineGrip: typeof window.lineGrip,
                    lineClear: typeof window.lineClear};
      out.lwStats = window.lwStats ? window.lwStats() : null;
      out.lineStats = window.lineStats ? window.lineStats() : null;
      if (window.lwSnap) window.lwSnap();
      const prints = {};
      ['lwPrint','lnPrint','ctPrint','brPrint','cpPrint'].forEach(id => {
        const im = document.getElementById(id);
        prints[id] = im ? (im.src || '').slice(0,15) + '/len=' + (im.src||'').length : 'MISSING';
      });
      out.prints = prints;
      out.anatomy = window.anatomyState ? window.anatomyState() : null;
      out.slides = document.querySelectorAll('section.slide').length;
      out.gb = !!document.getElementById('gb');
      return out;
    }""")
    b.close()

print(json.dumps({"page_errors": errs, "probe": res}, indent=1)[:6000])
