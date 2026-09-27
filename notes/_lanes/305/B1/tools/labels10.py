"""labels10.py — #305 call-10 scope check. The labels call 10 names, before (HEAD canon) v after (live canon),
4 themes x light/dark, 1440, dsf 2: per element the computed colour/opacity, the composited contrast, and a
PIXEL diff of the element's own screenshot (PIL). Common must change (>=4.5:1); mono/console/supercharge must
be pixel-identical to HEAD. Also the Kpi-tile lock-up (label box, label-to-value, tile) for call 5."""
import os, io, json
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LIB = open(os.path.join(B, "tools/look.py"), encoding="utf-8").read().split('LIB = r"""')[1].split('"""')[0]
SETS = [("Kpi-tile", ".kpi-tile .kpi-lbl", 3), ("Kpi-tile", ".kpi-tile .kpi-per", 2),
        ("Template-dashboard-bento", ".kpi-tile .lbl16", 2), ("Template-dashboard-bento", ".delta .per", 2),
        ("App-shell-side-nav", ".sn-group-label", 2), ("Sidebar-nav", ".sn-group-label", 2)]
out = {}; rows = []
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for th in ("mono", "common", "console", "supercharge"):
        for m in ("light", "dark"):
            shots = {}
            for tag in ("before", "after"):
                cur_page = None
                for name, sel, n in SETS:
                    if cur_page != name:
                        if cur_page: c.close()
                        c = br.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=2, reduced_motion="reduce")
                        pg = c.new_page(); pg.goto("file://" + os.path.join(B, "fix", tag, name + ".html")); pg.wait_for_timeout(700); pg.evaluate(LIB)
                        pg.add_style_tag(content="*{transition:none!important;animation:none!important}")
                        pg.evaluate("([a,t])=>{document.documentElement.setAttribute('data-apollo-theme',a);document.documentElement.setAttribute('data-theme',t);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',t));}", [th, m])
                        pg.wait_for_timeout(300); cur_page = name
                    els = pg.locator(sel)
                    k = 0
                    for i in range(els.count()):
                        e = els.nth(i)
                        if not e.is_visible() or k >= n: continue
                        info = e.evaluate("e=>__b1.contrast(e)")
                        png = e.screenshot()
                        shots.setdefault((name, sel, k), {})[tag] = (info, png); k += 1
                    if name == "Kpi-tile" and sel.endswith("kpi-lbl"):
                        out["lockup-%s-%s-%s" % (tag, th, m)] = pg.evaluate("""()=>{const t=document.querySelector('.kpi-tile'); const l=t.querySelector('.kpi-lbl'), v=t.querySelector('.kpi-val');
                          return {lblBox:l.getBoundingClientRect().height, lblToVal:v.offsetTop-l.offsetTop, tile:+t.getBoundingClientRect().height.toFixed(2), ovY:getComputedStyle(l).overflowY};}""")
                c.close()
            for key, d in shots.items():
                if "before" not in d or "after" not in d: continue
                ia, pa = d["before"]; ib, pb = d["after"]
                A = Image.open(io.BytesIO(pa)).convert("RGB"); Bm = Image.open(io.BytesIO(pb)).convert("RGB")
                same = A.size == Bm.size and ImageChops.difference(A, Bm).getbbox() is None
                rows.append({"theme": th, "mode": m, "comp": key[0], "sel": key[1], "i": key[2], "pixelIdentical": same,
                             "before": [ia["ratio"], ia["ink"], ia["opacity"]], "after": [ib["ratio"], ib["ink"], ib["opacity"]]})
    br.close()
json.dump({"rows": rows, "lockup": out}, open(os.path.join(B, "renders/call10-scope-measure.json"), "w"), indent=1)
for th in ("mono", "common", "console", "supercharge"):
    for m in ("light", "dark"):
        r = [x for x in rows if x["theme"] == th and x["mode"] == m]
        print("%-11s %-5s elements %2d  pixel-identical %2d  after-ratios %s" % (th, m, len(r), sum(x["pixelIdentical"] for x in r), sorted(set(x["after"][0] for x in r))))
for k, v in sorted(out.items()): print(k, v)
