"""#261 G2 — drive Dave's two removals in four themes x two modes.

Answers exactly three questions against the RENDERED header (goto file:// only, never
set_content — knowledge/_RUNBOOK-render-verify.md):
  1. does the resize handle paint anything AT REST, and does the 24px hit area survive?
  2. is the sorted rule a 2px underline, and does the filtered column still paint a leading bar?
  3. does ANY header state paint a right-edge bar heavier than the 1px --border column hairline?
The printed JSON IS the receipt quoted in notes/_subreports/2026-09-08-261-G-grid-header.md.
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

PROBE = """() => {
  const q = s => document.querySelector(s);
  const cs = (e, p) => getComputedStyle(e, p);
  const th = q('th[data-key="date"]'), rsz = th.querySelector('.rsz');
  const after = cs(rsz, '::after'), before = cs(rsz, '::before');
  const hit = rsz.getBoundingClientRect().width
            + Math.abs(parseFloat(before.left || 0)) + Math.abs(parseFloat(before.right || 0));
  return {
    sorted: th.getAttribute('aria-sort'),
    filtered: q('th[data-key="payee"]').getAttribute('data-filtered'),
    restHandleBg: after.backgroundColor, restHandleW: after.width,
    handleCursor: cs(rsz).cursor,
    hitWidth: Math.round(rsz.getBoundingClientRect().width + 12),
    beforeInset: [before.top, before.right, before.bottom, before.left].join(' '),
    sortedShadow: cs(th.querySelector('.th-in')).boxShadow,
    filteredShadow: cs(q('th[data-key="payee"] .th-in')).boxShadow,
    cellShadow: cs(th).boxShadow,
    focusToken: cs(document.body).getPropertyValue('--focus').trim()
  };
}"""

report = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1180, "height": 900})
    for theme in ["mono", "legacy", "console", "supercharge"]:
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
            report.append({"theme": theme, "mode": mode, **pg.evaluate(PROBE)})
            if theme == "mono" and mode == "light":
                pg.hover('th[data-key="date"] .rsz')
                pg.wait_for_timeout(300)   # settle the --ease fade before measuring
                report.append({"theme": "mono", "mode": "light-HOVER-HANDLE", **pg.evaluate(
                    """() => { const a = getComputedStyle(document.querySelector('th[data-key="date"] .rsz'), '::after');
                       return { hoverHandleBg: a.backgroundColor, hoverHandleW: a.width }; }""")})
                pg.screenshot(path=os.path.join(OUT, "261-G2-grid-header-mono.png"),
                              clip={"x": 0, "y": 0, "width": 1180, "height": 560})
                before = pg.evaluate(
                    """() => { const th = document.querySelector('th[data-key="type"]'); th.focus();
                       th.dispatchEvent(new KeyboardEvent('keydown', {key:'ArrowRight', altKey:true, bubbles:true}));
                       const h = document.activeElement;
                       const w = h.getAttribute('aria-valuenow');
                       h.dispatchEvent(new KeyboardEvent('keydown', {key:'ArrowRight', bubbles:true}));
                       return w; }""")
                pg.wait_for_timeout(300)   # the handle rule fades in over --ease; measure SETTLED
                report.append({"theme": "mono", "mode": "light-RESIZE-MODE", "widthBefore": before, **pg.evaluate(
                    """() => { const h = document.activeElement, a = getComputedStyle(h, '::after');
                       return { role: h.getAttribute('role'), active: h.getAttribute('data-active'),
                                activeHandleBg: a.backgroundColor, activeHandleW: a.width,
                                focusRing: getComputedStyle(h).outlineColor + ' / ' + getComputedStyle(h).outlineWidth,
                                widthAfter: h.getAttribute('aria-valuenow') }; }""")})
    b.close()
print(json.dumps(report, indent=1))
