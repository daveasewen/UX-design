#!/usr/bin/env python3
"""#261 lane F — theme shoot for Filter-toolbar-bar.

Builds one standalone doc per theme (snippet bytes + the generated
gen_theme_cascade.snippet_theme_css() re-projection of its own manifest vars, exactly what
gen_showroom.py bakes into an Open-↗ doc), then goto file://… and screenshot.
⛔ never set_content() — knowledge/_RUNBOOK-render-verify.md.
"""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "knowledge", "canon"))
import gen_theme_cascade as gtc

SNIP = os.path.join(REPO, "knowledge", "snippets", "Filter-toolbar-bar.reference.html")
OUT = HERE
src = open(SNIP, encoding="utf-8").read()
mv = json.loads(re.search(r'id="token-manifest">\s*(\{.*?\})\s*</script>', src, re.S).group(1))["vars"]
theme_css = gtc.snippet_theme_css(mv, "filter-toolbar-bar")

TYPE = open(os.path.join(REPO, "knowledge", "canon", "type.css"), encoding="utf-8").read()
doc = src.replace('<link rel="stylesheet" href="../canon/type.css">',
                  "<style>\n" + TYPE + "\n</style>\n<style>\n" + theme_css + "\n</style>")

from playwright.sync_api import sync_playwright
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for theme in ("mono", "legacy", "console", "supercharge"):
        for mode in ("light", "dark"):
            d = doc
            if theme != "mono":
                d = d.replace('<html lang="en">', '<html lang="en" data-apollo-theme="%s">' % theme)
            d = d.replace('<body data-theme="light">', '<body data-theme="%s">' % mode)
            tmp = os.path.join(OUT, "_shoot-%s-%s.html" % (theme, mode))
            open(tmp, "w", encoding="utf-8").write(d)
            pg = b.new_page(viewport={"width": 1360, "height": 1100},
                            device_scale_factor=1)
            pg.goto("file://" + tmp, wait_until="load")
            pg.wait_for_timeout(500)
            probe = pg.evaluate("""()=>{const c=document.createElement('canvas').getContext('2d');
              c.font='40px HSBC_MtUnivers_Latin'; const a=c.measureText('Handgloves 12345').width;
              c.font='40px __nope__'; return [a, c.measureText('Handgloves 12345').width];}""")
            out = os.path.join(OUT, "261-F-filter-toolbar-%s-%s.png" % (theme, mode))
            pg.screenshot(path=out, full_page=True)
            shots.append((theme, mode, out, probe))
            pg.close()
            os.remove(tmp)
    b.close()
for t, m, o, pr in shots:
    print("%-12s %-5s %s  face-probe=%.2f vs %.2f" % (t, m, os.path.basename(o), pr[0], pr[1]))
