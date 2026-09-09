"""#261 N — drive the nav family (sidebar-nav, navigations, tab-bar) in four themes x two modes.

goto file:// only (never set_content), per knowledge/_RUNBOOK-render-verify.md. Writes
261-N-nav-<slug>-<theme>-<mode>.png next to this file and prints the measured probe as JSON —
that print IS the receipt quoted in the subreport. The probe is not decorative: it measures the
hit areas by hand (no gate reads target/min), checks that the current-location indicator is a
real 3px inset on the family-ruled edge, and reads the SHARED nav tokens back off the live
cascade in every theme, so "one token set, three surfaces" is a measurement and not a claim.
"""
import json, os, sys
ROOT = "/sessions/zen-funny-hawking/mnt/UX-design"
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
sys.path.insert(0, os.path.join(ROOT, "knowledge", "canon"))
import gen_theme_cascade as cascade
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, "notes/_lanes")
SPECS = [
    ("sidebar-nav", "knowledge/snippets/Sidebar-nav.reference.html", 1180, 780,
     "nav.sn .nv-item[aria-current='page']", "inset 3px 0 0"),
    ("navigations", "knowledge/snippets/Navigations.reference.html", 1180, 260,
     "nav.main .nv-item[aria-current='page']", "inset 0 -3px 0"),
    ("tab-bar", "knowledge/snippets/Tab-bar.reference.html", 480, 420,
     ".tabbar .nv-item[aria-current='page']", "inset 0 3px 0"),
]
SHARED = ["--nav-surface", "--nav-text", "--nav-icon", "--nav-hover", "--nav-indicator",
          "--nav-focus", "--nav-count-bg", "--nav-count-fg", "--nav-row"]
THEMES = ["mono", "legacy", "console", "supercharge"]
report = []

with sync_playwright() as p:
    b = p.chromium.launch()
    for slug, rel, w, h in [(s[0], s[1], s[2], s[3]) for s in SPECS]:
        spec = [s for s in SPECS if s[0] == slug][0]
        snip = os.path.join(ROOT, rel)
        src = open(snip).read()
        man = json.loads(src.split('<script type="application/json" id="token-manifest">')[1].split("</script>")[0])
        theme_css = cascade.snippet_theme_css(man["vars"], slug)
        pg = b.new_page(viewport={"width": w, "height": h})
        for theme in THEMES:
            for mode in ["light", "dark"]:
                pg.goto("file://" + snip)
                pg.add_style_tag(content=theme_css)
                pg.evaluate(
                    """([t,m]) => { if (t!=='mono') document.documentElement.setAttribute('data-apollo-theme', t);
                       else document.documentElement.removeAttribute('data-apollo-theme');
                       document.body.setAttribute('data-theme', m); }""", [theme, mode])
                pg.wait_for_timeout(140)
                probe = pg.evaluate("""([sel, edge, shared]) => {
                  const cs = getComputedStyle(document.body);
                  const tok = {}; shared.forEach(v => tok[v] = cs.getPropertyValue(v).trim());
                  const cur = document.querySelector(sel);
                  const box = e => { const b = e.getBoundingClientRect();
                                     return [Math.round(b.width), Math.round(b.height)]; };
                  const rows = [...document.querySelectorAll('.nv-item')].filter(e => e.offsetParent !== null);
                  const smallest = rows.map(box).reduce((a,b)=> a[1] <= b[1] ? a : b, [999,999]);
                  const count = document.querySelector('.nv-count');
                  const dis = document.querySelector('.nv-item[aria-disabled="true"]');
                  return {
                    tokens: tok,
                    currentFound: !!cur,
                    indicatorGeometry: cur ? getComputedStyle(cur).boxShadow.replace(/^rgba?\([^)]*\)\s*/, "").replace(/px/g, "").replace(/\s+/g, " ").trim() : null,
                    indicatorExpected: edge.split(" ").slice(1).join(" ").replace(/px/g, "") + " 0 inset",
                    indicatorShadow: cur ? getComputedStyle(cur).boxShadow : null,
                    currentSurfaceEqualsHover: cur ? getComputedStyle(cur).backgroundColor : null,
                    smallestItem: smallest,
                    countBox: count ? box(count) : null,
                    disabledStated: dis ? dis.getAttribute('aria-disabled') + '/' + dis.getAttribute('tabindex') : null,
                    ariaCurrentCount: document.querySelectorAll('[aria-current="page"]').length,
                    indicatorOnCurrentSurface: (() => {
                      const hex = s => { const m = s.trim().match(/^#?([0-9a-f]{6})$/i);
                        if (m) return [0,2,4].map(i => parseInt(m[1].substr(i,2),16));
                        const n = s.match(/\d+/g); return n ? n.slice(0,3).map(Number) : null; };
                      const lum = c => { const f = c.map(v => { v/=255;
                        return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
                        return 0.2126*f[0] + 0.7152*f[1] + 0.0722*f[2]; };
                      const ind = hex(cs.getPropertyValue('--nav-indicator'));
                      const bg  = hex(cs.getPropertyValue('--nav-hover'));
                      if (!ind || !bg) return null;
                      const a = lum(ind), b = lum(bg);
                      return Math.round(((Math.max(a,b)+0.05)/(Math.min(a,b)+0.05))*100)/100;
                    })()
                  };
                }""", [spec[4], spec[5], SHARED])
                probe.update({"component": slug, "theme": theme, "mode": mode})
                report.append(probe)
                pg.screenshot(path=os.path.join(OUT, "261-N-nav-%s-%s-%s.png" % (slug, theme, mode)),
                              full_page=True)
        pg.close()
    b.close()

print(json.dumps(report, indent=1))
