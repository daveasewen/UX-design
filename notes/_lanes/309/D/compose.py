"""#309 lane D - one before/after PNG per moved page, for Dave's eye: the page at 1440 in light and dark,
HEAD before the move (b690a19b) on the left, after on the right, then the stat row and each arrow cropped in (4x).
The banking demo's crop rows run all four themes x two modes. Reads outputs/309/D/{before,after}/.
Run at the seat in ONE call (same env as capture.py): python3 notes/_lanes/309/D/compose.py"""
import os, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "outputs", "309", "D")
TITLES = {"banking-demo": "The #227 banking demo (console theme) - dashboards/international-banking-dashboard.canon.html",
          "progress-dashboard": "The progress dashboard - dashboard/index.html (the counts carry no delta, so no arrow)",
          "receipt-page": "The receipt-bearing regen - dashboards/international-banking-dashboard.regen-v2-receipt.html. Two things NOT from the move: the chart is empty on the right because the page was already stale at HEAD and regenerates against today's Chart-line (HEAD's own Stat-card spec regenerates to the same empty chart); and neither side draws an arrow, because a receipt splices the element, not the icon sprite."}
def cell(ph, f, w):
    return '<td><img style="width:%dpx" src="file://%s"></td>' % (w, os.path.join(SRC, ph, f))
def cropcell(ph, key):
    arrows = sorted(f for f in os.listdir(os.path.join(SRC, ph)) if f.startswith(key + "-arrow"))
    imgs = "".join('<img style="height:80px;margin:8px 16px 0 0;outline:1px solid #ccc" src="file://%s">'
                   % os.path.join(SRC, ph, f) for f in arrows)
    return '<td><img style="width:900px" src="file://%s"><div>%s</div></td>' % (os.path.join(SRC, ph, key + "-crop.png"), imgs)
def ink(ph, key):
    try:
        a = json.load(open(os.path.join(SRC, ph, "arrows.json")))[key]
    except Exception:
        return ""
    return " · ".join("%s %s" % (x["dir"].split()[-1], x["ink"]) for x in a)
css = ("body{margin:0;padding:24px;background:#fff;font:14px/1.4 Arial,sans-serif;color:#1a1a1a}"
       "h1{font-size:20px;margin:0 0 8px}h2{font-size:15px;margin:24px 0 8px}table{border-collapse:collapse}"
       "td,th{vertical-align:top;padding:6px 10px;border:1px solid #ccc;text-align:left}th{background:#f0f0f0}"
       ".k{font-size:12px;color:#444}")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for name, title in TITLES.items():
        h = ['<html><head><meta charset="utf-8"><style>%s</style></head><body>' % css,
             "<h1 style=\"max-width:1800px\">%s</h1>" % title,
             '<p class="k">Left: before (HEAD b690a19b, the stat card). Right: after (Metric, s309-D3). Rendered at 1440 at the seat; every style is the page\'s own plus canon.css.</p>',
             "<table><tr><th></th><th>Before - stat card</th><th>After - Metric</th></tr>"]
        for mode in ("light", "dark"):
            h.append("<tr><th>%s</th>%s%s</tr>" % (mode, cell("before", f"{name}-{mode}-ctx.png", 900), cell("after", f"{name}-{mode}-ctx.png", 900)))
        h.append("</table><h2>The stat row at 4x, and each arrow-bearing delta row cropped in</h2><table><tr><th></th><th>Before</th><th>After</th></tr>")
        keys = [(f"{name}-{t}-{m}", f"{t} {m}") for t in ("mono", "common", "console", "supercharge") for m in ("light", "dark")] \
            if name == "banking-demo" else [(f"{name}-{m}", m) for m in ("light", "dark")]
        for key, lab in keys:
            h.append('<tr><th>%s<br><span class="k">before: %s<br>after: %s</span></th>%s%s</tr>'
                     % (lab, ink("before", key), ink("after", key), cropcell("before", key), cropcell("after", key)))
        h.append("</table></body></html>")
        hp = os.path.join(SRC, name + "-compose.html")
        open(hp, "w").write("".join(h))
        pg = b.new_page(viewport={"width": 2100, "height": 900}, device_scale_factor=1)
        pg.goto("file://" + hp); pg.wait_for_timeout(500)
        out = os.path.join(HERE, name + "-before-after.png")
        pg.screenshot(path=out, full_page=True); pg.close()
        print("wrote", os.path.relpath(out, ROOT), os.path.getsize(out))
    b.close()
