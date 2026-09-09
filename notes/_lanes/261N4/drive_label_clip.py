#!/usr/bin/env python3
"""#261 N4 — drive the nav label boxes and measure descender clipping.

For every .nv-label (and .sn-who b/small) on the three nav snippets, in 4 themes x 2 modes,
compute the ink bottom from the font's OWN metrics (canvas measureText: fontBoundingBoxAscent /
Descent + actualBoundingBoxDescent) and compare it with the element's clip box (clientHeight,
which is what overflow:hidden crops to). clip_px > 0 = a cut glyph.

goto file:// only; never set_content.
"""
import json, os, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
SNIPS = ["Sidebar-nav", "Navigations", "Tab-bar"]
THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]

extra = os.environ.get("APOLLO_PW_LD_LIBRARY_PATH")
if extra:
    os.environ["LD_LIBRARY_PATH"] = extra + ":" + os.environ.get("LD_LIBRARY_PATH", "")

JS = r"""
() => {
  const cvs = document.createElement('canvas');
  const ctx = cvs.getContext('2d');
  const out = [];
  const leaves = [...document.querySelectorAll('body *')].filter(el =>
    el.childNodes.length && [...el.childNodes].every(n => n.nodeType === 3) &&
    el.textContent.trim().length && !el.closest('.spec-h,script,style'));
  leaves.forEach((el, i) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (cs.clipPath && cs.clipPath !== 'none') return;              // sr-only
    if (cs.overflowY !== 'hidden' && cs.overflowY !== 'clip') return; // nothing crops it
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    // probe with a descender-heavy control string plus the real text
    const txt = (el.textContent || '').trim();
    const m = ctx.measureText(txt + 'gypq');
    const fA = m.fontBoundingBoxAscent, fD = m.fontBoundingBoxDescent;
    const aD = m.actualBoundingBoxDescent, aA = m.actualBoundingBoxAscent;
    const fs = parseFloat(cs.fontSize);
    let lh = cs.lineHeight === 'normal' ? (fA + fD) : parseFloat(cs.lineHeight);
    const ch = el.clientHeight;            // the crop box for overflow:hidden
    // baseline offset from the content-box top of a single-line box
    const half = (lh - (fA + fD)) / 2;
    const baseline = half + fA;
    const inkBottom = baseline + aD;
    const inkTop = baseline - aA;
    const clipsBottom = Math.max(0, inkBottom - ch);
    const clipsTop = Math.max(0, -inkTop);
    out.push({
      i, sel: el.className, text: txt.slice(0, 24),
      fontSize: fs, lineHeight: lh, clientH: ch,
      overflow: cs.overflow, tbTrim: cs.textBoxTrim || cs['text-box-trim'] || '',
      tbEdge: cs.textBoxEdge || cs['text-box-edge'] || '',
      ink: +(aA + aD).toFixed(2),
      clip_bottom: +clipsBottom.toFixed(2), clip_top: +clipsTop.toFixed(2)
    });
  });
  return out;
}
"""


def main():
    from playwright.sync_api import sync_playwright
    results = {}
    worst = 0.0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        for name in SNIPS:
            f = ROOT / "knowledge" / "snippets" / f"{name}.reference.html"
            pg.goto("file://" + str(f))
            pg.add_style_tag(content="*{transition:none!important;animation:none!important}")
            for th in THEMES:
                for md in MODES:
                    pg.evaluate(
                        "([t,m])=>{const h=document.documentElement;"
                        "if(t==='mono'){h.removeAttribute('data-apollo-theme');}"
                        "else{h.setAttribute('data-apollo-theme',t);}"
                        "h.setAttribute('data-theme',m);document.body.setAttribute('data-theme',m);}",
                        [th, md],
                    )
                    rows = pg.evaluate(JS)
                    key = f"{name}|{th}|{md}"
                    results[key] = rows
                    for r in rows:
                        worst = max(worst, r["clip_bottom"], r["clip_top"])
        b.close()
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/var/tmp/n4-clip.json")
    out.write_text(json.dumps(results, indent=1))
    bad = [(k, r) for k, rs in results.items() for r in rs if r["clip_bottom"] > 0.05 or r["clip_top"] > 0.05]
    print(f"combos={len(results)} labels={sum(len(v) for v in results.values())} worst_clip={worst:.2f}px clipped={len(bad)}")
    for k, r in bad[:12]:
        print(f"  CLIP {k} '{r['text']}' fs={r['fontSize']} lh={r['lineHeight']} clientH={r['clientH']} ink={r['ink']} bottom={r['clip_bottom']} top={r['clip_top']} ovf={r['overflow']}")
    print("->", out)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
