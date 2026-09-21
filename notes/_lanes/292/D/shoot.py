#!/usr/bin/env python3
"""#292 lane D — render the cold one-shot light+dark at 1440 and MEASURE it.

Run (one bash call, env re-exported every call — knowledge/_RUNBOOK-render-verify.md):

  export TMPDIR=/dev/shm
  export LD_LIBRARY_PATH=<MOUNT>/outputs/syslibs/usr/lib/aarch64-linux-gnu
  python3 notes/_lanes/292/D/shoot.py

Writes: overview-dashboard-oneshot-v1.png (light|dark side by side)
        overview-dashboard-oneshot-v1-light.png / -dark.png
        measured.json
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "file://" + os.path.join(HERE, "overview-dashboard-oneshot-v1.html")

PROBE = r"""() => {
  const out = {};
  const cs = el => el ? getComputedStyle(el) : null;
  const wall = document.querySelector('.c-bento[data-bento-role="dashboard"].wall-ops');
  const wg   = wall ? wall.querySelector(':scope > .c-bento__grid') : null;
  out.outerWall = wall ? {
    width: Math.round(wall.getBoundingClientRect().width),
    columnGap: cs(wg).columnGap, rowGap: cs(wg).rowGap,
    cols: cs(wg).gridTemplateColumns.split(' ').length,
    autoRows: cs(wg).gridAutoRows, flow: cs(wg).gridAutoFlow,
    padding: cs(wall).padding, radius: cs(wall).borderRadius, overflow: cs(wall).overflow
  } : null;
  out.innerWalls = [...document.querySelectorAll('.c-bento__tile.c-bento')].map(b => {
    const g = b.querySelector(':scope > .c-bento__grid');
    return { cls: b.className, width: Math.round(b.getBoundingClientRect().width),
             columnGap: cs(g).columnGap, rowGap: cs(g).rowGap,
             cols: cs(g).gridTemplateColumns.split(' ').length,
             colsNow: cs(g).getPropertyValue('--bento-cols-now').trim(),
             autoRows: cs(g).gridAutoRows };
  });
  // tiles of the outer wall, with span + geometry + clip test
  out.topTiles = [...wg.children].map(t => {
    const r = t.getBoundingClientRect();
    // deepest scrollable overflow inside the tile
    // A CLIP is only a clip when the box actually clips: overflow-y hidden|clip,
    // a real box (not an inline span, not the sr-only 1px box), content taller.
    let clipped = [];
    const scan = el => {
      const s = getComputedStyle(el);
      const oy = s.overflowY;
      const inline = s.display === 'inline';
      const srOnly = el.classList.contains('sr-only') || el.clientHeight <= 1;
      if (!inline && !srOnly && (oy === 'hidden' || oy === 'clip')
          && el.scrollHeight - el.clientHeight > 1) {
        clipped.push({ tag: el.tagName.toLowerCase(), cls: el.className.toString().slice(0,60),
                       over: el.scrollHeight - el.clientHeight });
      }
      [...el.children].forEach(scan);
    };
    scan(t);
    // dead band: the tile's own content bottom vs the tile bottom
    const kid = t.firstElementChild;
    const dead = kid ? Math.round(r.bottom - kid.getBoundingClientRect().bottom) : null;
    // DEAD GROUND INSIDE the card: the bottom of the last painted descendant
    // against the bottom of the surface it sits on. This is what the eye reads as
    // an empty tile, and the tile-level dead band above cannot see it.
    // Only LEAVES count — a container that stretches to the surface is not content.
    let lowest = 0;
    const walk = el => {
      const isSvg = el.tagName.toLowerCase() === 'svg';
      const leaf = el.children.length === 0 || isSvg;   // an svg is one painted box
      const paints = leaf && (el.textContent.trim().length > 0 || isSvg
                     || ['IMG','HR','INPUT'].includes(el.tagName.toUpperCase()));
      if (paints && !el.classList.contains('sr-only')) {
        const b = el.getBoundingClientRect();
        const st = getComputedStyle(el);
        if (b.height > 0 && st.visibility !== 'hidden' && b.bottom > lowest) { lowest = b.bottom; }
      }
      [...el.children].forEach(walk);
    };
    [...t.children].forEach(walk);
    const deadInside = lowest ? Math.round(r.bottom - lowest) : null;
    return { c: t.getAttribute('data-c'), r: t.getAttribute('data-r'),
             w: Math.round(r.width), h: Math.round(r.height),
             x: Math.round(r.left), y: Math.round(r.top),
             deadBandPx: dead, deadGroundInsidePx: deadInside, clipped };
  });
  // ORPHAN-CELL ARITHMETIC. A tile with data-r=2 occupies its columns in BOTH
  // rows, so the naive per-top sum under-counts the second row. Cells are counted
  // on the real row grid: row index from the tile's top, extent from data-r.
  const unit = parseFloat(cs(wg).gridAutoRows) || 320;
  const gap  = parseFloat(cs(wg).rowGap) || 0;
  const wallTop = wg.getBoundingClientRect().top;
  const rows = {};
  [...wg.children].forEach(t => {
    const r0 = Math.round((t.getBoundingClientRect().top - wallTop) / (unit + gap));
    const rr = parseInt(t.getAttribute('data-r') || '1', 10);
    const cc = parseInt(t.getAttribute('data-c') || '1', 10);
    for (let i = 0; i < rr; i++) { rows[r0 + i] = (rows[r0 + i] || 0) + cc; }
  });
  out.rowSpanSums = rows;
  out.wallColumns = parseInt(cs(wg).getPropertyValue('--bento-cols-now')) || null;
  out.orphanCells = Object.entries(rows)
      .filter(([, v]) => v % (out.wallColumns || 6) !== 0)
      .map(([k, v]) => ({ row: +k, sum: v }));
  // x-alignment census: distinct left edges of top-level tiles
  out.tileLeftEdges = [...new Set(out.topTiles.map(t => t.x))].sort((a,b)=>a-b);
  out.tileRightEdges = [...new Set(out.topTiles.map(t => t.x + t.w))].sort((a,b)=>a-b);
  // components actually used
  out.components = [...new Set([...document.querySelectorAll('[class]')]
      .flatMap(e => e.className.toString().split(/\s+/))
      .filter(c => /^cn-[a-z]/.test(c)))].sort();
  out.componentCount = out.components.length;
  out.bentos = document.querySelectorAll('.c-bento').length;
  out.tiles  = document.querySelectorAll('.c-bento__tile').length;
  out.headings = { h1: document.querySelectorAll('h1').length,
                   h2: document.querySelectorAll('h2').length,
                   h3: document.querySelectorAll('h3').length };
  out.svgCount = document.querySelectorAll('svg').length;
  out.tables = document.querySelectorAll('table').length;
  out.buttons = document.querySelectorAll('button').length;
  out.doc = { w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight };
  out.theme = { rootClass: document.documentElement.className,
                dataTheme: document.documentElement.getAttribute('data-theme'),
                apolloTheme: document.documentElement.getAttribute('data-apollo-theme') };
  // every custom property the page's OWN <style> references, resolved where used
  const src = [...document.querySelectorAll('style')].map(s => s.textContent).join('\n');
  const names = [...new Set((src.match(/var\(\s*(--[a-z0-9-]+)/gi) || [])
      .map(m => m.replace(/var\(\s*/i, '')))];
  const root = document.documentElement;
  out.varsReferenced = names.length;
  out.varsEmptyAtRoot = names.filter(n => !getComputedStyle(root).getPropertyValue(n).trim());
  // spacing values authored in the page's own CSS (the ruled stop set check)
  out.authoredPx = [...new Set((src.match(/(?:gap|margin|padding)[a-z-]*\s*:\s*[^;]+/gi) || [])
      .flatMap(d => d.match(/(\d+)px/g) || []))].sort((a,b)=>parseInt(a)-parseInt(b));
  // the BENTO DIALS only — what the ruled stop set actually governs
  out.bentoDialPx = [...new Set((src.match(/--bento-(?:gutter|outer-padding|row-unit)\s*:\s*[^;]+/gi) || [])
      .flatMap(d => d.match(/(\d+)px/g) || []))].sort((a,b)=>parseInt(a)-parseInt(b));
  // raw hex in the page's own DECLARATIONS (comments stripped first — the comments
  // quote session numbers and canon's own token values)
  const srcNoComments = src.replace(/\/\*[\s\S]*?\*\//g, '');
  out.hexInPageCss = (srcNoComments.match(/#[0-9a-f]{3,8}\b/gi) || []);
  // chart engine
  out.dvRender = typeof window.dvRender;
  out.chartMarks = { spend: document.querySelectorAll('#fig-spend .dv-svg rect').length,
                     gains: document.querySelectorAll('#fig-gains .dv-svg *').length };
  // kpi row
  const kpis = [...document.querySelectorAll('.kpi-tile')].map(k => {
    const r = k.getBoundingClientRect();
    return { w: Math.round(r.width), h: Math.round(r.height), y: Math.round(r.top) };
  });
  out.kpi = kpis;
  out.kpiDistinctHeights = [...new Set(kpis.map(k => k.h))];
  out.kpiDistinctTops = [...new Set(kpis.map(k => k.y))];
  out.kpiDistinctWidths = [...new Set(kpis.map(k => k.w))];
  return out;
}"""

def main():
    res = {}
    errs = {"light": [], "dark": []}
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        for mode in ("light", "dark"):
            pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
            pg.on("pageerror", lambda e, m=mode: errs[m].append(str(e)))
            pg.on("console", lambda msg, m=mode: errs[m].append("console:" + msg.text)
                  if msg.type == "error" else None)
            pg.goto(PAGE, wait_until="load")
            pg.evaluate("m => document.documentElement.setAttribute('data-theme', m)", mode)
            pg.wait_for_timeout(1400)
            pg.evaluate("() => window.dispatchEvent(new Event('resize'))")
            pg.wait_for_timeout(900)
            res[mode] = pg.evaluate(PROBE)
            pg.screenshot(path=os.path.join(HERE, "overview-dashboard-oneshot-v1-%s.png" % mode),
                          full_page=True)
            pg.close()
        b.close()

    # light | dark, side by side, at the required path
    try:
        from PIL import Image
        a = Image.open(os.path.join(HERE, "overview-dashboard-oneshot-v1-light.png"))
        b2 = Image.open(os.path.join(HERE, "overview-dashboard-oneshot-v1-dark.png"))
        h = max(a.height, b2.height)
        sheet = Image.new("RGB", (a.width + b2.width + 16, h), (128, 128, 128))
        sheet.paste(a, (0, 0)); sheet.paste(b2, (a.width + 16, 0))
        sheet.save(os.path.join(HERE, "overview-dashboard-oneshot-v1.png"))
    except Exception as e:                     # declared, never silent
        print("SIDE-BY-SIDE NOT WRITTEN: %s" % e, file=sys.stderr)

    out = {"page": PAGE, "viewport": "1440x1000 @2x", "pageErrors": errs, "measured": res}
    with open(os.path.join(HERE, "measured.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1)[:9000])

if __name__ == "__main__":
    main()
