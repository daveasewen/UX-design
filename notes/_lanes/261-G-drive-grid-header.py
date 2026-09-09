"""#261 G — drive the data-grid column header in four themes x two modes.

goto file:// only (never set_content), per knowledge/_RUNBOOK-render-verify.md. Chromium comes
from the lane-brief recipe; libXdamage1 is unpacked into a prefix and exported through
LD_LIBRARY_PATH before this runs. Writes the per-theme PNGs next to this file and prints the
measured probe as JSON — that print IS the receipt quoted in the subreport.
"""
import json, os, sys
ROOT = "/sessions/zen-funny-hawking/mnt/UX-design"
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
sys.path.insert(0, os.path.join(ROOT, "knowledge", "canon"))
import gen_theme_cascade as cascade
from playwright.sync_api import sync_playwright

SNIP = os.path.join(ROOT, "knowledge/snippets/Data-grid.reference.html")
OUT = os.path.join(ROOT, "notes/_lanes")
src = open(SNIP).read()
man = json.loads(src.split('<script type="application/json" id="token-manifest">')[1].split("</script>")[0])
theme_css = cascade.snippet_theme_css(man["vars"], "data-grid")

THEMES = ["mono", "legacy", "console", "supercharge"]
report = []

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1180, "height": 900})
    for theme in THEMES:
        for mode in ["light", "dark"]:
            pg.goto("file://" + SNIP)
            pg.add_style_tag(content=theme_css)
            pg.evaluate(
                """([t,m]) => { if (t!=='mono') document.documentElement.setAttribute('data-apollo-theme', t);
                   else document.documentElement.removeAttribute('data-apollo-theme');
                   document.body.setAttribute('data-theme', m); }""", [theme, mode])
            pg.click('th[data-key="date"] .sort')
            pg.click('th[data-key="date"] .sort')
            pg.click('th[data-key="payee"] .colf')
            pg.fill('#cf-payee', 'a')
            pg.press('#cf-payee', 'Enter')
            pg.wait_for_timeout(120)
            probe = pg.evaluate("""() => {
              const q = s => document.querySelector(s);
              const r = e => { const b = e.getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; };
              return {
                sorted: q('th[data-key="date"]').getAttribute('aria-sort'),
                filtered: q('th[data-key="payee"]').getAttribute('data-filtered'),
                rowcount: q('#tbl').getAttribute('aria-rowcount'),
                sortBtn: r(q('th[data-key="date"] .sort')),
                colf: r(q('th[data-key="date"] .colf')),
                rsz: r(q('th[data-key="date"] .rsz')),
                selLabel: r(q('#selAll + label')),
                grpH: Math.round(q('thead tr.grp th').getBoundingClientRect().height),
                stickyCols: getComputedStyle(q('thead tr.cols th')).position,
                stickyTop: getComputedStyle(q('thead tr.cols th')).top,
                hdrBg: getComputedStyle(q('thead tr.cols th')).backgroundColor,
                grpBg: getComputedStyle(q('thead tr.grp th')).backgroundColor,
                sortedShadow: getComputedStyle(q('th[data-key="date"] .th-in')).boxShadow,
                filteredShadow: getComputedStyle(q('th[data-key="payee"] .th-in')).boxShadow,
              };
            }""")
            report.append({"theme": theme, "mode": mode, **probe})
            if mode == "light":
                pg.screenshot(path=os.path.join(OUT, f"261-G-grid-header-{theme}.png"),
                              clip={"x": 0, "y": 0, "width": 1180, "height": 560})
            if theme == "mono" and mode == "light":
                pg.click('.dgden [data-density="compact"]')
                pg.wait_for_timeout(80)
                compact = pg.evaluate("""() => {
                  const r = e => { const b = e.getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; };
                  return { sortBtn: r(document.querySelector('th[data-key="date"] .sort')),
                           selLabel: r(document.querySelector('#selAll + label')),
                           colf: r(document.querySelector('th[data-key="date"] .colf')),
                           rsz: r(document.querySelector('th[data-key="date"] .rsz')),
                           grpH: Math.round(document.querySelector('thead tr.grp th').getBoundingClientRect().height) };
                }""")
                pg.screenshot(path=os.path.join(OUT, "261-G-grid-header-mono-compact.png"),
                              clip={"x": 0, "y": 0, "width": 1180, "height": 520})
                report.append({"theme": "mono", "mode": "light-COMPACT", **compact})
                pg.click('.dgden [data-density="comfortable"]')
                sticky = pg.evaluate("""() => { const sc = document.querySelector('.dg-scroll');
                  sc.scrollTop = 200; const th = document.querySelector('thead tr.cols th');
                  return { headerTopOffsetAfterScroll: Math.round(th.getBoundingClientRect().top - sc.getBoundingClientRect().top),
                           scrollTop: sc.scrollTop, scrollable: sc.scrollHeight > sc.clientHeight }; }""")
                report.append({"theme": "mono", "mode": "light-STICKY", **sticky})
                kb = pg.evaluate("""() => {
                  const th = document.querySelector('th[data-key="type"]');
                  th.focus();
                  th.dispatchEvent(new KeyboardEvent('keydown', {key:'ArrowRight', altKey:true, bubbles:true}));
                  const h = document.activeElement;
                  const before = h.getAttribute('aria-valuenow');
                  h.dispatchEvent(new KeyboardEvent('keydown', {key:'ArrowRight', bubbles:true}));
                  return { focusIsHandle: h.getAttribute('role'), before, after: h.getAttribute('aria-valuenow'),
                           colWidth: document.querySelector('col[data-col="type"]').style.width };
                }""")
                report.append({"theme": "mono", "mode": "light-RESIZE-KEYBOARD", **kb})
    b.close()

print(json.dumps(report, indent=1))
