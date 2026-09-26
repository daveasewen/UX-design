#!/usr/bin/env python3
"""render.py — #304 R3 before/after render pairs for s245-D10 (console radius set).

Run at the seat, in ONE bash call:
  cd "$HOME/mnt/Projects--UX-design" && export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh;
  source knowledge/_render/seat_env.sh; python3 notes/_lanes/304/R3/render.py [CANON_BEFORE CANON_AFTER]
BEFORE canon defaults to `git --no-optional-locks show HEAD:knowledge/canon/canon.css` (read-only);
AFTER defaults to the working knowledge/canon/canon.css. Builds one specimen page per theme per
state in $TMPDIR (six snippet bodies wrapped in their canon .cn-<slug> scope: Button, Input-fields,
Cards, Modals, Notifications, Segmented-control), shoots 1440 and 390 full-page via goto(file://)
with the seat's RENDER_SHELL, and writes PNGs + diff counts + a side-by-side page into
notes/_lanes/304/R3/renders/. Font: asserts by canvas probe that "Univers Next for HSBC" resolves
to the HSBC face (width differs from the fallback) and prints the widths; refuses otherwise.
"""
import os, re, sys, json, subprocess
if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(".")
K = os.path.join(ROOT, "knowledge")
OUT = os.path.join(ROOT, "notes/_lanes/304/R3/renders"); os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(os.environ.get("TMPDIR", "/dev/shm"), "r3spec"); os.makedirs(TMP, exist_ok=True)
if len(sys.argv) > 2:
    cb, ca = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
else:
    cb = os.path.join(TMP, "canon-before.css")
    open(cb, "wb").write(subprocess.check_output(
        ["git", "--no-optional-locks", "show", "HEAD:knowledge/canon/canon.css"], cwd=ROOT))
    ca = os.path.join(K, "canon/canon.css")
TYPE = os.path.join(K, "canon/type.css")
COMPS = [("Button", "button"), ("Input-fields", "input-fields"), ("Cards", "cards"),
         ("Modals", "modals"), ("Notifications", "notifications"), ("Segmented-control", "segmented-control")]
THEMES = ["mono", "legacy", "console", "supercharge"]

def body_of(name):
    s = open(os.path.join(K, "snippets", name + ".reference.html"), encoding="utf-8").read()
    b = re.search(r"<body[^>]*>(.*)</body>", s, re.S).group(1)
    b = re.sub(r'<script type="application/json".*?</script>', "", b, flags=re.S)
    if name != "Segmented-control":   # its script places the sliding thumb (.ind) the ruling re-radii
        b = re.sub(r"<script.*?</script>", "", b, flags=re.S)
    return b

BODIES = {slug: body_of(n) for n, slug in COMPS}

def page(state, canon, theme):
    secs = "\n".join(
        '<section class="spec"><h6 class="lab">%s · %s</h6><div class="cn-%s">%s</div></section>'
        % (n, theme, slug, BODIES[slug]) for n, slug in COMPS)
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="file://%s"><link rel="stylesheet" href="file://%s">
<style>body{margin:0;padding:24px;background:#fff;font-family:"Univers Next for HSBC",sans-serif}
.lab{font:500 12px/16px "Univers Next for HSBC",sans-serif;margin:24px 0 8px;color:#767676;letter-spacing:0}
.spec{border-top:1px solid #eee}
/* determinism: freeze motion so a pixel diff measures the canon change, not a frame */
*,*::before,*::after{animation:none !important;transition:none !important;caret-color:transparent !important}
/* specimen only: keep modal overlays in flow so they are photographed */
.spec [class*="overlay"],.spec .scrim{position:relative !important;inset:auto !important}</style>
</head><body data-apollo-theme="%s" data-theme="light"><div data-apollo-theme="%s" data-theme="light">%s</div></body></html>""" % (
        TYPE, canon, theme, theme, secs)
    p = os.path.join(TMP, "spec-%s-%s.html" % (theme, state))
    open(p, "w", encoding="utf-8").write(html)
    return p

PROBE = """() => { const c=document.createElement('canvas').getContext('2d'); const w=f=>{c.font='40px '+f; return c.measureText('Handgloves 12345').width;};
 return {hsbc:w('"Univers Next for HSBC"'), fallback:w('"NoSuchFace-xyz"'), dejavu:w('"DejaVu Sans"'),
         check:document.fonts.check('16px "Univers Next for HSBC"')}; }"""
res = {"canon_before": cb, "canon_after": ca, "shots": []}
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], headless=True,
                           args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    for theme in THEMES:
        for state, canon in (("before", cb), ("after", ca)):
            src = page(state, canon, theme)
            for w, h in ((1440, 900), (390, 844)):
                pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
                pg.goto("file://" + src); pg.wait_for_timeout(500)
                probe = pg.evaluate(PROBE)
                if abs(probe["hsbc"] - probe["fallback"]) < 0.5:
                    sys.exit("REFUSE: HSBC face did not resolve — fallback render %s" % probe)
                facts = pg.evaluate("""() => { const g=s=>{const e=document.querySelector(s); return e?getComputedStyle(e).borderTopLeftRadius:null};
                  return {btn:g('.cn-button .btn'), card:g('.cn-cards .card'), dialog:g('.cn-modals .dialog'),
                          note:g('.cn-notifications .note.tint'), seg_xs:g('.cn-segmented-control .seg.xs'),
                          seg_l:g('.cn-segmented-control .seg.l'), thumb_xs:g('.cn-segmented-control .seg.xs .ind'), thumb_l:g('.cn-segmented-control .seg.l .ind'), field:g('.cn-input-fields input'),
                          scrollW:document.documentElement.scrollWidth}; }""")
                f = "%s-%d-%s.png" % (theme, w, state)
                pg.screenshot(path=os.path.join(OUT, f), full_page=True); pg.close()
                res["shots"].append({"theme": theme, "w": w, "state": state, "file": f, "probe": probe, "radii": facts})
                print(f, json.dumps(facts), "font", {k: round(v, 2) if isinstance(v, float) else v for k, v in probe.items()})
    br.close()
try:
    from PIL import Image, ImageChops
    res["diff"] = {}
    for theme in THEMES:
        for w in (1440, 390):
            a = Image.open(os.path.join(OUT, "%s-%d-before.png" % (theme, w))).convert("RGB")
            b = Image.open(os.path.join(OUT, "%s-%d-after.png" % (theme, w))).convert("RGB")
            if a.size != b.size:
                res["diff"]["%s-%d" % (theme, w)] = "size %s vs %s" % (a.size, b.size); continue
            bbox = ImageChops.difference(a, b).getbbox()
            n = 0 if bbox is None else sum(1 for px in ImageChops.difference(a, b).get_flattened_data() if px != (0, 0, 0))
            res["diff"]["%s-%d" % (theme, w)] = n
    print("PIXEL DIFF before->after:", res["diff"])
except ImportError:
    res["diff"] = "PIL absent at seat — not measured"; print(res["diff"])
json.dump(res, open(os.path.join(OUT, "_render-facts.json"), "w"), indent=1)
rows = "".join('<h2>%s · %dpx</h2><div class="pair"><figure><figcaption>before (HEAD)</figcaption><img src="renders/%s-%d-before.png"></figure><figure><figcaption>after (s245-D10)</figcaption><img src="renders/%s-%d-after.png"></figure></div>'
               % (t, w, t, w, t, w) for t in ["console"] + [x for x in THEMES if x != "console"] for w in (1440, 390))
open(os.path.join(ROOT, "notes/_lanes/304/R3/RENDER-PAIRS-s245-D10.html"), "w").write(
    """<!doctype html><meta charset="utf-8"><title>Console radius set — before and after</title><style>
body{font:15px/1.5 "Univers Next for HSBC",Helvetica,Arial,sans-serif;margin:24px;color:#1a1a1a}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}figure{margin:0}img{width:100%%;border:1px solid #ddd}
figcaption{font-size:13px;color:#555;margin-bottom:4px}</style>
<h1>Console radius set, before and after</h1><p>Your ruling of 3 September, "The radii is only for console": control 6, surface 8, container 12; segmented xs 4/2, s 6/4, m 8/6, l 10/6. Console first; the other three themes follow and should not move. Pixel difference per pair: %s. Rendered at the seat with the HSBC face resolved by canvas probe.</p>%s"""
    % (json.dumps(res["diff"]), rows))
print("WROTE notes/_lanes/304/R3/RENDER-PAIRS-s245-D10.html")
