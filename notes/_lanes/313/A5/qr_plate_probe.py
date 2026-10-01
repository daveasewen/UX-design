"""#313 A5 — W-307qs (s307-D50: 'QR codes stay dark on light in every mode').
Drops a `.qr` figure inside `.cn-qr-code` in all four themes x two modes and reads the COMPUTED plate and
module colours the symbol paints (the inherited --qr-plate / --qr-module), plus the page ground behind it.
PASS when every cell paints a LIGHT plate under DARK modules (plate lighter, contrast >= 15:1), the same pair in
both modes of a theme, whatever the page does. (Supercharge's pair is its warm white and warm black.)
Colour only: no font needed, any headless Chromium.
  python3 notes/_lanes/313/A5/qr_plate_probe.py [--canon PATH] [--executable PATH]"""
import os, sys, json, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
arg = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
canon = pathlib.Path(arg("--canon") or REPO / "knowledge" / "canon" / "canon.css")
exe = arg("--executable") or os.environ.get("RENDER_SHELL") or None
cells = [(t, m) for t in ("mono", "console", "legacy", "supercharge") for m in ("light", "dark")]
body = "".join('<div data-apollo-theme="%s"><div data-theme="%s"><div class="cn-qr-code" id="%s-%s" style="background:var(--page)">'
               '<figure class="qr size-s units-a"><svg viewBox="0 0 33 33"><rect width="33" height="33" fill="var(--qr-plate)"/>'
               '<rect x="4" y="4" width="7" height="7" fill="var(--qr-module)"/></svg></figure></div></div></div>' % (t, m, t, m) for t, m in cells)
page = '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="%s"></head><body>%s</body></html>' % (canon.as_uri(), body)
tmp = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "qr_plate_probe.html"; tmp.write_text(page, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe); pg = b.new_page(); pg.goto(tmp.as_uri())
    got = pg.evaluate("""(ids)=>ids.map(id=>{const c=document.getElementById(id); const r=c.querySelectorAll('rect');
        return [id, getComputedStyle(r[0]).fill, getComputedStyle(r[1]).fill, getComputedStyle(c).backgroundColor];})""",
        ["%s-%s" % c for c in cells])
    b.close()
def lum(rgb):
    v = [int(x) / 255 for x in rgb[rgb.index("(") + 1:-1].split(",")[:3]]
    v = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
ok, pairs = True, {}
for cid, plate, mod, ground in got:
    lp, lm = lum(plate), lum(mod)
    ratio = (max(lp, lm) + 0.05) / (min(lp, lm) + 0.05)
    good = lp > lm and ratio >= 15
    pairs.setdefault(cid.split("-")[0], set()).add((plate, mod))
    ok = ok and good
    print("  %-18s plate %-20s modules %-18s %5.2f:1  page %-20s %s" % (cid, plate, mod, ratio, ground, "dark on light" if good else "NOT dark on light"))
for th, prs in pairs.items():
    if len(prs) != 1:
        ok = False; print("  %s: the pair MOVES between modes: %s" % (th, sorted(prs)))
opt = "follows-theme" in canon.read_text(encoding="utf-8")
print("  canon carries a theme-following QR option: %s" % ("YES — the inverting variant is still offered" if opt else "no"))
ok = ok and not opt
print("PASS — dark on light in every theme and mode, and no inverting option" if ok else "FAIL")
sys.exit(0 if ok else 1)
