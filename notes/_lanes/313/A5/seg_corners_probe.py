"""#313 A5 — W-307qm (s307-D45): did the one-source segmented corner fix reach the toolbar segments?

For every canon scope that re-declares `.seg` (the chart toolbars, the filter toolbar, the templates,
view options, tab bar) a `.seg <scale>` is dropped inside `.cn-<scope>` and the same markup inside
`.cn-segmented-control` (the part itself), in all four themes x two modes, and the COMPUTED corner
radius of the frame (.seg), the thumb (.ind) and a segment (button) is read off the live DOM.
A MISMATCH is any scope whose corners differ from the part's at the same theme, mode and scale.
The chart toolbar's own boxes (.dv-toggle-seg, its .ind, .dv-vt, .dv-tbl-toggle) are read too.

Radius only: no font is needed, so this runs in any headless Chromium (cloud or seat).
  python3 notes/_lanes/313/A5/seg_corners_probe.py [--executable PATH]
Exit 0 = no mismatch; 1 = mismatches listed."""
import os, re, sys, json, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
CANON = REPO / "knowledge" / "canon" / "canon.css"
css = CANON.read_text(encoding="utf-8")
scopes = sorted(set(re.findall(r":where\(\.cn-([a-z0-9-]+)\) (?::is\()?\.seg[{ ,]", css)) - {"segmented-control"})
SCALES = ["", "xs", "s", "m", "l", "sm", "md", "lg"]
# Each scope is compared at the scale(s) ITS OWN snippet draws (read from the snippet markup), because a
# scope's local .seg copy only has to be right for the sizes it uses. "" = a bare `.seg` (no scale class).
SNIP = REPO / "knowledge" / "snippets"
def used_scales(scope):
    name = scope[:1].upper() + scope[1:] + ".reference.html"
    f = SNIP / name
    if not f.exists():
        return set(SCALES)
    return {m.strip() for m in re.findall(r'class="seg((?: [a-z]+)?)"', f.read_text(encoding="utf-8"))} or set(SCALES)
THEMES = ["mono", "console", "legacy", "supercharge"]
MODES = ["light", "dark"]
seg = lambda sc: ('<div class="seg %s" role="group" aria-label="p"><span class="ind" aria-hidden="true"></span>'
                  '<button type="button" aria-pressed="true">Aa</button><button type="button" aria-pressed="false">Bb</button></div>' % sc)
cells = []
body = []
for th in THEMES:
    for md in MODES:
        blocks = []
        for sc in SCALES:
            for scope in ["segmented-control"] + scopes:
                cid = "c%d" % len(cells); cells.append((th, md, sc, scope, cid))
                blocks.append('<div class="cn-%s" id="%s">%s</div>' % (scope, cid, seg(sc)))
        for scope in ("chart-line", "chart-combo"):   # the two snippets that draw .dv-toggle-seg
            cid = "c%d" % len(cells); cells.append((th, md, "toolbar", scope, cid))
            blocks.append('<div class="cn-%s" id="%s"><div class="dv-toggle-seg"><span class="ind"></span><button type="button">T</button></div>'
                          '<button type="button" class="dv-vt">V</button><button type="button" class="dv-tbl-toggle">C</button></div>' % (scope, cid))
        body.append('<div data-apollo-theme="%s"><div data-theme="%s">%s</div></div>' % (th, md, "".join(blocks)))
page = '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="%s"></head><body>%s</body></html>' % (CANON.as_uri(), "".join(body))
tmp = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "seg_corners_probe.html"
tmp.write_text(page, encoding="utf-8")
exe = None
if "--executable" in sys.argv: exe = sys.argv[sys.argv.index("--executable") + 1]
exe = exe or os.environ.get("RENDER_SHELL") or None
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(tmp.as_uri())
    got = pg.evaluate("""(ids)=>{const r={}; const R=e=>e?getComputedStyle(e).borderTopLeftRadius:null;
      for(const id of ids){const c=document.getElementById(id);
        r[id]={frame:R(c.querySelector('.seg')), thumb:R(c.querySelector('.seg .ind')), seg:R(c.querySelector('.seg button')),
               tseg:R(c.querySelector('.dv-toggle-seg')), tind:R(c.querySelector('.dv-toggle-seg .ind')),
               vt:R(c.querySelector('.dv-vt')), tbl:R(c.querySelector('.dv-tbl-toggle'))};}
      return r;}""", [c[4] for c in cells])
    b.close()
USED = {sc: used_scales(sc) for sc in scopes}
# A scope whose .seg is DRAWN to a different shape on purpose is named here with where it is drawn, and its
# difference is printed but not counted. Only one: the mobile tab bar's island is a 999px pill.
DECLARED = {"tab-bar": "the tab bar's island is a drawn 999px pill (Tab-bar.reference.html .tabbar-pills, lines 159-164), not the segmented part"}
ref = {(th, md, sc): got[cid] for th, md, sc, scope, cid in cells if scope == "segmented-control"}
mism, declared, n = [], [], 0
for th, md, sc, scope, cid in cells:
    if scope == "segmented-control" or sc == "toolbar": continue
    if sc not in USED[scope]: continue
    n += 1
    a, r = got[cid], ref[(th, md, sc)]
    d = {k: (a[k], r[k]) for k in ("frame", "thumb", "seg") if a[k] != r[k]}
    if d: (declared if scope in DECLARED else mism).append((th, md, sc, scope, d))
print("segmented corners: %d scope cells compared to the part (%d scopes, each at the scale(s) its own snippet draws, x 8 theme-modes)" % (n, len(scopes)))
for sc in scopes: print("  .cn-%-22s draws %s" % (sc, sorted(USED[sc]) and ", ".join(repr(x) for x in sorted(USED[sc]))))
for th in THEMES:
    for sc in SCALES:
        r = ref[(th, "light", sc)]
        print("  part %-11s %-4r frame %-5s thumb %-5s segment %s" % (th, sc, r["frame"], r["thumb"], r["seg"]))
print("toolbar boxes (light):")
for th, md, sc, scope, cid in cells:
    if sc == "toolbar" and md == "light":
        a = got[cid]; print("  %-11s %-12s toggle frame %-5s toggle fill %-5s view-as-table %-5s copy %s" % (th, scope, a["tseg"], a["tind"], a["vt"], a["tbl"]))
for k, v in DECLARED.items():
    print("DECLARED, not counted: .cn-%s differs in %d cells — %s" % (k, sum(1 for m in declared if m[3] == k), v))
print("MISMATCHES: %d" % len(mism))
for m in mism: print("  %s/%s %s .cn-%s  %s" % (m[0], m[1], m[2], m[3], json.dumps(m[4])))
sys.exit(1 if mism else 0)
