"""ADR-0016 P2 proof — ds-014 calls (a) + (b), RULED-vs-RENDERED.

Reads the RULED values out of the source of truth and asserts the RENDERED values in a real
browser with the licensed cut. NOT a document-vs-document comparison — that is what we already
had, and it is what let dv-004 sit green on a 0.0px gap for weeks.

  (a) dv-004  — every stacked-column segment boundary separated by >= 2px
  (b) ds-014  — every alpha key >= 4.5:1 (AA) against the segment fill it is drawn on

Both are asserted on the SNIPPET *and* the SHOWROOM pane, at 1180 and 760 — the discriminator
pattern that separates a lost decision from a base-URL artefact (ds-013).

POTHOLE PINNED: last session's probe used querySelector('svg') and got the toolbar COPY ICON,
reporting a 16px-wide "chart canvas". Selectors here are explicit and guarded.
"""
from playwright.sync_api import sync_playwright
import glob, os, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = glob.glob(os.path.expanduser(
    "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))

JS = r"""
() => {
  const lin = c => { c/=255; return c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
  const L = ([r,g,b]) => 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b);
  const rgb = s => (s.match(/\d+(\.\d+)?/g) || []).slice(0,3).map(Number);
  const ratio = (a,b) => { const l1=L(a), l2=L(b), hi=Math.max(l1,l2), lo=Math.min(l1,l2);
                           return (hi+0.05)/(lo+0.05); };

  const fig = document.querySelector('figure[data-dv-type="stacked-column"]');
  if (!fig) return {error: 'no stacked-column figure'};
  const svg = fig.querySelector('svg.dv-svg');
  if (!svg) return {error: 'no svg.dv-svg inside the figure'};
  const box = svg.getBoundingClientRect();
  // guard against the toolbar-icon trap: a chart canvas is never this small
  if (box.width < 100) return {error: 'svg.dv-svg is only ' + box.width + 'px wide - wrong node'};

  const rects = [...svg.querySelectorAll('rect.dv-series')];
  const keys  = [...svg.querySelectorAll('text.dv-barkey')];

  // ---- (a) separation, measured in RENDERED CSS px -------------------------
  const cols = {};
  for (const r of rects) {
    const b = r.getBoundingClientRect();
    const k = Math.round(b.x * 10) / 10;
    (cols[k] = cols[k] || []).push({top: b.top, bottom: b.bottom, h: b.height});
  }
  const gaps = [];
  for (const k of Object.keys(cols)) {
    const seg = cols[k].sort((p, q) => p.top - q.top);
    for (let i = 0; i < seg.length - 1; i++)
      gaps.push({col: k, gap: +(seg[i+1].top - seg[i].bottom).toFixed(3)});
  }

  // ---- (b) alpha-key contrast against the fill BENEATH each key ------------
  const keyRes = [];
  for (const t of keys) {
    const kb = t.getBoundingClientRect();
    const cx = kb.x + kb.width/2, cy = kb.y + kb.height/2;
    let under = null;
    for (const r of rects) {
      const b = r.getBoundingClientRect();
      if (cx >= b.left && cx <= b.right && cy >= b.top && cy <= b.bottom) { under = r; break; }
    }
    const kf = getComputedStyle(t).fill;
    const uf = under ? getComputedStyle(under).fill : null;
    keyRes.push({
      ch: t.textContent.trim(),
      keyFill: kf,
      segFill: uf,
      onFill: !!under,
      ratio: uf ? +ratio(rgb(kf), rgb(uf)).toFixed(2) : null,
      fontPx: +getComputedStyle(t).fontSize.replace('px',''),
      weight: getComputedStyle(t).fontWeight
    });
  }
  return {
    svgWidth: +box.width.toFixed(1),
    viewBox: svg.getAttribute('viewBox'),
    scale: +(box.width / parseFloat(svg.getAttribute('viewBox').split(/\s+/)[2])).toFixed(4),
    rects: rects.length, keys: keys.length,
    gaps, keyRes,
    fontOK: document.fonts.check('16px HSBC_MtUnivers_Latin')
  };
}
"""

TARGETS = [("snippet", f"file://{ROOT}/knowledge/snippets/Chart-bar.reference.html"),
           ("showroom", f"file://{ROOT}/showroom/chart-bar.html")]

out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=SHELL[0] if SHELL else None, headless=True,
                          args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                                "--allow-file-access-from-files"])
    for width in (1180, 760):
        for name, url in TARGETS:
            pg = b.new_page(viewport={"width": width, "height": 1600})
            pg.goto(url)
            pg.wait_for_timeout(1400)
            # The showroom delivers each snippet into a pane IFRAME via srcdoc (ds-013), so the
            # figure is NOT in the top document. Search every frame and take the first that has
            # it. My first pass queried only the top document and reported "no stacked-column
            # figure" for the showroom — the same wrong-document error as last session's
            # querySelector('svg') toolbar-icon trap, which is why this loop exists.
            res = {"error": "figure not found in any of %d frame(s)" % len(pg.frames)}
            for fr in pg.frames:
                try:
                    r = fr.evaluate(JS)
                except Exception:
                    continue
                if not r.get("error"):
                    res = r
                    break
            out[f"{name}@{width}"] = res
            pg.close()
    b.close()

print(json.dumps(out, indent=1))

# ---- verdicts -----------------------------------------------------------------
print("\n" + "=" * 72)
fails = []
for k, r in out.items():
    if r.get("error"):
        fails.append(f"{k}: PROBE ERROR {r['error']}"); continue
    gmin = min(g["gap"] for g in r["gaps"]) if r["gaps"] else None
    onfill = [x for x in r["keyRes"] if x["onFill"]]
    cmin = min((x["ratio"] for x in onfill if x["ratio"] is not None), default=None)
    print(f"{k:<18} svg={r['svgWidth']}px scale={r['scale']}  font={r['fontOK']}  "
          f"rects={r['rects']} keys={r['keys']}")
    print(f"{'':<18} (a) smallest gap  = {gmin}px  over {len(r['gaps'])} boundaries")
    print(f"{'':<18} (b) worst contrast= {cmin}:1 over {len(onfill)} on-fill keys "
          f"({r['keyRes'][0]['keyFill'] if r['keyRes'] else '-'})")
    if gmin is None or gmin < 2.0:
        fails.append(f"{k}: dv-004 gap {gmin}px < 2px")
    if cmin is None or cmin < 4.5:
        fails.append(f"{k}: alpha-key contrast {cmin}:1 < 4.5:1")
    if not r["fontOK"]:
        fails.append(f"{k}: licensed face NOT loaded - measurements are not the real cut")
print("=" * 72)
print(("FAILS:\n  " + "\n  ".join(fails)) if fails else "ALL ASSERTIONS PASS")
sys.exit(1 if fails else 0)
