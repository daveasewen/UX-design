"""#261 G3 — drive the grid's header select-all in four themes x two modes x three states.

Dave, verbatim: "the grid header is fine except the checkbox is rendered oddly, can't we just
use the check component?" The grid used to RESTATE Selection-controls' anatomy on its own vars;
it now CONSUMES the component's rule block byte-identically under an alias layer. This driver
proves it against the RENDERED control (goto file:// only, never set_content —
knowledge/_RUNBOOK-render-verify.md), and is the receipt quoted in the G subreport.

Per theme x mode x state it reads: the box fill and border, the resolved glyph stroke, the
DRAWN length of each glyph (stroke-dashoffset — 0 = drawn, 22 = hidden), the label hit area,
and aria-checked. It also asserts the ONE thing that made the old fork drift: that the tick and
the dash are never drawn at the same time, and that neither is drawn at rest.
"""
import json, os, sys
ROOT = "/sessions/zen-funny-hawking/mnt/UX-design"
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
sys.path.insert(0, os.path.join(ROOT, "knowledge", "canon"))
import gen_theme_cascade as cascade
from playwright.sync_api import sync_playwright

SNIP = os.path.join(ROOT, "knowledge/snippets/Data-grid.reference.html")
OUT = os.path.join(ROOT, "notes/_lanes/261G3")
os.makedirs(OUT, exist_ok=True)
src = open(SNIP).read()
man = json.loads(src.split('<script type="application/json" id="token-manifest">')[1].split("</script>")[0])
theme_css = cascade.snippet_theme_css(man["vars"], "data-grid")

SET = """([c, i]) => { const x = document.getElementById('selAll');
  x.checked = c; x.indeterminate = i;
  if (i) x.setAttribute('aria-checked', 'mixed'); else x.removeAttribute('aria-checked'); }"""

PROBE = """() => {
  const inp = document.getElementById('selAll');
  const lab = document.querySelector('label[for="selAll"]');
  const box = lab.querySelector('.box');
  const tick = box.querySelector('.tick'), dash = box.querySelector('.mixed');
  const cs = e => getComputedStyle(e);
  const r = lab.getBoundingClientRect();
  const off = e => cs(e).strokeDashoffset;
  return {
    boxFill: cs(box).backgroundColor, boxBorder: cs(box).borderTopColor,
    boxSize: Math.round(box.getBoundingClientRect().width) + 'x' + Math.round(box.getBoundingClientRect().height),
    glyphStroke: cs(tick).stroke,
    tickDrawn: off(tick) === '0px', dashDrawn: off(dash) === '0px',
    tickDasharray: cs(tick).strokeDasharray, dashDasharray: cs(dash).strokeDasharray,
    hit: Math.round(r.width) + 'x' + Math.round(r.height),
    ariaChecked: inp.getAttribute('aria-checked'),
    glyphIsFilled: cs(tick).fill !== 'none'
  };
}"""

STATES = [("unchecked", False, False), ("indeterminate", False, True), ("checked", True, False)]
report, bad = [], []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1180, "height": 900}, device_scale_factor=3)
    for theme in ["mono", "legacy", "console", "supercharge"]:
        for mode in ["light", "dark"]:
            pg.goto("file://" + SNIP)
            pg.add_style_tag(content=theme_css)
            pg.evaluate(
                """([t,m]) => { if (t!=='mono') document.documentElement.setAttribute('data-apollo-theme', t);
                   else document.documentElement.removeAttribute('data-apollo-theme');
                   document.body.setAttribute('data-theme', m); }""", [theme, mode])
            pg.wait_for_timeout(120)
            for name, chk, ind in STATES:
                pg.evaluate(SET, [chk, ind])
                pg.wait_for_timeout(260)          # settle the --ease stroke draw before measuring
                row = {"theme": theme, "mode": mode, "state": name, **pg.evaluate(PROBE)}
                report.append(row)
                # the three clauses the old fork could not hold
                if row["glyphIsFilled"]:
                    bad.append(f"{theme}/{mode}/{name}: glyph has a FILL — that is the triangle")
                if row["tickDrawn"] and row["dashDrawn"]:
                    bad.append(f"{theme}/{mode}/{name}: tick AND dash drawn together")
                want = {"unchecked": (False, False), "indeterminate": (False, True), "checked": (True, False)}[name]
                if (row["tickDrawn"], row["dashDrawn"]) != want:
                    bad.append(f"{theme}/{mode}/{name}: drawn={row['tickDrawn']},{row['dashDrawn']} want={want}")
                if int(row["hit"].split("x")[0]) < 24 or int(row["hit"].split("x")[1]) < 24:
                    bad.append(f"{theme}/{mode}/{name}: hit {row['hit']} BREACH-FLOOR")
                pg.locator('label[for="selAll"] .box').screenshot(
                    path=os.path.join(OUT, f"{theme}-{mode}-{name}.png"))
    b.close()

print(json.dumps({"rows": report, "violations": bad}, indent=1))
print("\nG3 CHECKBOX DRIVE:", "GREEN" if not bad else f"RED — {len(bad)} violation(s)",
      f"({len(report)} rows = 4 themes x 2 modes x 3 states)")
sys.exit(1 if bad else 0)
