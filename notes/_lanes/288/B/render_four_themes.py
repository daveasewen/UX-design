#!/usr/bin/env python3
"""#288 lane B — render the dashboard-bento template in four themes + a Mono outer-gutter ramp.

READ-ONLY on the repo. Source under render is the SHOWROOM payload
(showroom/template-dashboard-bento.html, base64 <script id="payload">) because that payload —
and NOT knowledge/snippets/Template-dashboard-bento.reference.html on its own — carries the
gen_showroom.py per-theme re-projection block that binds --layout-bento-gutter per theme.

Every render copy is written under notes/_lanes/288/B/ only. No repo file is modified.
Renders use goto("file://…") — set_content() is BANNED (type.css must load).
"""
import base64, json, os, re, sys

REPO = "/sessions/trusting-youthful-franklin/mnt/UX-design"
LANE = os.path.join(REPO, "notes/_lanes/288/B")
PNG = os.path.join(LANE, "png")
WORK = os.path.join(LANE, "_render_src")
VIEWPORT_W = 1440

os.makedirs(PNG, exist_ok=True)
os.makedirs(WORK, exist_ok=True)

src = open(os.path.join(REPO, "showroom/template-dashboard-bento.html"), encoding="utf-8").read()
m = re.search(r'<script id="payload"[^>]*>(.*?)</script>', src, re.S)
PAYLOAD = base64.b64decode(m.group(1).strip()).decode("utf-8")
# the payload sits in showroom/ in the tree; our copies live elsewhere, so the two
# relative refs (type.css, the masterbrand svgs) become absolute file paths.
PAYLOAD = PAYLOAD.replace("../knowledge/", "file://" + REPO + "/knowledge/")

# ---- the twelve renders -------------------------------------------------------------------
# outer = the structural bento gutter; inner = the embedded bento / tile-group gutter.
# `override` None  -> render exactly what HEAD delivers (the 40/4 literal pin)
#          (o, i)  -> the pinned variables overridden IN THE RENDER ONLY.
R = []
# row 1 — four themes, TOKEN reading of the outer gutter (layout/bento/gutter, s217-D2)
#         + s219-D1 subSpacing for the inner.
for theme, o, i in [("mono", 0, 4), ("legacy", 24, 4), ("console", 24, 4), ("supercharge", 0, 2)]:
    R.append(dict(id=f"r1-{theme}", theme=theme, outer=o, inner=i, override=True, row=1))
# row 2 — Mono outer gutter ramp, inner held at 4
for o in (0, 8, 16, 24):
    R.append(dict(id=f"r2-mono-{o}", theme="mono", outer=o, inner=4, override=True, row=2))
# row 3 — the competing ruled reading: s219-D1 mainSpacing as the outer gutter
for theme, o, i in [("mono", 40, 4), ("legacy", 24, 4), ("console", 40, 4), ("supercharge", 24, 2)]:
    R.append(dict(id=f"r3-{theme}", theme=theme, outer=o, inner=i, override=True, row=3))
# row 0 — what HEAD delivers, untouched, one per theme (expected identical: the 40/4 pin)
for theme in ("mono", "legacy", "console", "supercharge"):
    R.append(dict(id=f"r0-{theme}", theme=theme, outer=None, inner=None, override=False, row=0))

# the showroom harness bar and the review overlay are demo chrome, not the template — hidden
# in the render so the contact sheet shows the delivered page and nothing else.
CHROME_OFF = """
<style id="lane-b-chrome-off">
.demo-bar{display:none !important;}
#rv-fab,#rv-markers,#rv-noodle,#rv-composer,#rv-panel{display:none !important;}
</style>
"""

OVERRIDE_TPL = """
<style id="lane-b-override">
/* LANE B RENDER-ONLY OVERRIDE — not in the repo, not in canon. Same selectors as the
   template's pinned rules (canon.css:18119 / :18121, snippet :802 / :804) so the literal
   pin is replaced rather than fought on specificity. */
.tpl-page .c-bento.tpl-wall[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento){
  --bento-gutter:%(outer)dpx; }
.tpl-page .c-bento.tpl-group[data-bento-role="dashboard"]{ --bento-gutter:%(inner)dpx; }
</style>
"""


def build(cfg):
    doc = PAYLOAD
    doc = doc.replace('<html lang="en">', '<html lang="en" data-apollo-theme="%s">' % cfg["theme"], 1)
    inject = CHROME_OFF
    if cfg["override"]:
        inject += OVERRIDE_TPL % {"outer": cfg["outer"], "inner": cfg["inner"]}
    doc = doc.replace("</head>", inject + "</head>", 1)
    p = os.path.join(WORK, cfg["id"] + ".html")
    open(p, "w", encoding="utf-8").write(doc)
    return p


MEASURE = r"""
() => {
  const px = n => Math.round(n * 100) / 100;
  function gaps(grid){
    if(!grid) return null;
    const kids = [...grid.children].map(e => e.getBoundingClientRect());
    let col = [], row = [];
    for(let a=0;a<kids.length;a++) for(let b=a+1;b<kids.length;b++){
      const A=kids[a], B=kids[b];
      const vOverlap = Math.min(A.bottom,B.bottom) - Math.max(A.top,B.top);
      const hOverlap = Math.min(A.right,B.right) - Math.max(A.left,B.left);
      if(vOverlap > 1 && B.left >= A.right - 0.5) col.push(B.left - A.right);
      if(vOverlap > 1 && A.left >= B.right - 0.5) col.push(A.left - B.right);
      if(hOverlap > 1 && B.top >= A.bottom - 0.5) row.push(B.top - A.bottom);
      if(hOverlap > 1 && A.top >= B.bottom - 0.5) row.push(A.top - B.bottom);
    }
    const mn = a => a.length ? px(Math.min(...a)) : null;
    const cs = getComputedStyle(grid);
    return { n_children: kids.length,
             measured_col_gap: mn(col), measured_row_gap: mn(row),
             col_samples: col.length, row_samples: row.length,
             computed_column_gap: cs.columnGap, computed_row_gap: cs.rowGap,
             var_bento_gutter: getComputedStyle(grid.parentElement)
                                 .getPropertyValue('--bento-gutter').trim() };
  }
  const R = e => { const r = e.getBoundingClientRect();
    return { x:px(r.left+scrollX), y:px(r.top+scrollY), w:px(r.width), h:px(r.height) }; };
  const wall = document.querySelector('.c-bento.tpl-wall[data-bento-role="dashboard"]');
  const outerGrid = wall ? wall.querySelector(':scope > .c-bento__grid') : null;
  const lead = document.querySelector('.c-bento.tpl-group-lead');
  const leadGrid = lead ? lead.querySelector(':scope > .c-bento__grid') : null;
  const ev = document.querySelector('.c-bento.tpl-group-evidence');
  const evGrid = ev ? ev.querySelector(':scope > .c-bento__grid') : null;
  return {
    /* the theme token is declared on the [data-theme] element (the BODY), not <html>,
       because gen_showroom.py's re-projection selector is
       [data-apollo-theme="X"][data-theme="light"] — so read it where it is consumed. */
    layout_bento_gutter_html: getComputedStyle(document.documentElement)
                           .getPropertyValue('--layout-bento-gutter').trim(),
    layout_bento_gutter_body: getComputedStyle(document.body)
                           .getPropertyValue('--layout-bento-gutter').trim(),
    layout_bento_gutter_at_wall: wall ? getComputedStyle(wall)
                           .getPropertyValue('--layout-bento-gutter').trim() : null,
    theme_attr: document.documentElement.getAttribute('data-apollo-theme'),
    outer: gaps(outerGrid),
    inner_lead: gaps(leadGrid),
    inner_evidence: gaps(evGrid),
    /* page-space rects, for the 1:1 detail crops on the contact sheet */
    rect_wall: wall ? R(wall) : null,
    rect_lead: lead ? R(lead) : null,
    rect_evidence: ev ? R(ev) : null,
  };
}
"""


def main():
    from playwright.sync_api import sync_playwright
    shell = os.environ["RENDER_SHELL"]
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=shell, args=["--no-sandbox"])
        page = b.new_page(viewport={"width": VIEWPORT_W, "height": 1400},
                          device_scale_factor=1)
        for cfg in R:
            p = build(cfg)
            page.goto("file://" + p, wait_until="load")
            page.wait_for_timeout(700)
            data = page.evaluate(MEASURE)
            shot = os.path.join(PNG, cfg["id"] + ".png")
            page.screenshot(path=shot, full_page=True)
            sz = os.path.getsize(shot)
            data["png"] = os.path.relpath(shot, LANE)
            data["png_bytes"] = sz
            data["cfg"] = cfg
            out[cfg["id"]] = data
            print(cfg["id"], "theme=", data["theme_attr"],
                  "--layout-bento-gutter@wall=", data["layout_bento_gutter_at_wall"],
                  "outer measured col/row=", data["outer"]["measured_col_gap"],
                  "/", data["outer"]["measured_row_gap"],
                  "inner(lead) col/row=", data["inner_lead"]["measured_col_gap"],
                  "/", data["inner_lead"]["measured_row_gap"],
                  "png=", sz, flush=True)
        b.close()
    json.dump(out, open(os.path.join(LANE, "measurements.json"), "w"), indent=1)
    print("WROTE", os.path.join(LANE, "measurements.json"))


if __name__ == "__main__":
    main()
