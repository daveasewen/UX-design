#!/usr/bin/env python3
"""Render-verify + DRIVE knowledge/_fitness-test/nio-dash-console-v2.canon.html.

v2 adds six things to v1 and every one of them is proved here by MEASUREMENT, not by a
screenshot alone (though the screenshots are taken and looked at too):

  1. PAGE GREY (v2 ①) — body's resolved background must differ from a card's, in BOTH modes,
     and must equal the token v2 claims (--surface-subtle in light, --background-default in
     dark). ⚠ POSITIVE CONTROL: v1 is loaded through the SAME probe and must FAIL the
     distinctness test in light — that is the defect v2 fixes, and a test that cannot show
     v1 failing proves nothing about v2 passing.
  2. 1600px MEASURE (v2 ②) — --l-max on <main> must read 1600px and main's rendered width
     must actually reach it at a viewport wider than 1600 (a var can be set and ignored).
  3. THE SEARCH-FIELD RADIUS (v2 ③) — .search.boxed's computed border-radius must equal
     --border-radius-control under Console (8px), for EVERY search field on the page, and
     v1's must read 0px through the same probe. Root cause, restated: the component draws a
     1px box and never consumes the token; the token itself was always correct.
  4. THEME SWITCH (v2 ④) — driven by CLICKING the button (not by poking data-theme), and by
     KEYBOARD (focus + Enter), because keyboard operability is the requirement.
  5. LEGEND PARITY (v2 ⑤) — the capsule and list legends are driven through the SAME two
     gestures (uncheck a swatch, isolate a label) and the SET OF GHOSTED SERIES must be
     identical in both, as must the donut's centre figure. Then a MUTATION: the assertion is
     re-run against a deliberately wrong series id, and must go red — a parity check that
     cannot fail is not a check.
  6. LIST CHROME (v2 ⑥) — card / flush / flush-plain are driven through the switch and the
     three chrome declarations are read back: ul.list background + border, the li+li
     separator (which must SURVIVE), and the tag border.

  7. VAR SWEEP — every page-local custom property v2 introduces, in Console light AND dark,
     must resolve non-empty. A dangling var renders silent black and no gate sees it.

Follows _RUNBOOK-render-verify.md: canvas font probe against TWO controls (never
document.fonts.check alone), env re-exported by the caller in every bash call, --stage
chunking so no call approaches the 45 s wall, verdict printed BEFORE any teardown, and
screenshots written to the outputs mount so they can be READ.

Homed in-repo per s191-D2.

Usage:  python3 verify_nio_dash_v2.py --stage a|b|shots
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
try:
    from _helpgate import help_gate as _help_gate
    _help_gate(__doc__, __name__, __file__)
except Exception:
    pass

import glob, os, sys

REPO = "/sessions/busy-clever-rubin/mnt/UX-design"
V2 = "file://" + REPO + "/knowledge/_fitness-test/nio-dash-console-v2.canon.html"
V1 = "file://" + REPO + "/knowledge/_fitness-test/nio-dash-console-v1.canon.html"
OUT = "/sessions/busy-clever-rubin/mnt/outputs"

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((bool(cond), name, detail))
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    return bool(cond)


def launch(p):
    sh = glob.glob(os.environ["PLAYWRIGHT_BROWSERS_PATH"]
                   + "/chromium_headless_shell-*/chrome-linux/headless_shell")
    return p.chromium.launch(executable_path=sh[0], headless=True,
                             args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])


FONT_PROBE = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const m = f => { c.font = '40px ' + f; return c.measureText('Handgloves 12345').width; };
  return { target: m('HSBC_MtUnivers_Latin'),
           uf: m('"Univers Next HSBC"'),
           ctrl_dejavu: m('"DejaVu Sans"'),
           ctrl_missing: m('"NoSuchFaceAnywhere"') };
}"""

# every custom property v2 introduces or re-points, plus the ones a dangling value would blank
# A custom property is only readable WHERE IT IS SET (it does not climb). Read each one at the
# element that owns it — reading --nio-max at <body> returns empty and says nothing about the page.
V2_VARS = ["--page", "--border-radius-control", "--border-radius-surface",
           "--surface-subtle", "--surface-raised", "--background-default", "--surface-transparent",
           "--divider", "--border", "--text"]

VAR_PROBE = """(names) => {
  const out = {};
  const rs = getComputedStyle(document.documentElement);
  const bs = getComputedStyle(document.body);
  for (const n of names) out[n] = (bs.getPropertyValue(n) || rs.getPropertyValue(n)).trim();
  out['--l-max@main'] = getComputedStyle(document.querySelector('main'))
                          .getPropertyValue('--l-max').trim();
  out['--nio-max@shell'] = getComputedStyle(document.querySelector('.nio-shell'))
                          .getPropertyValue('--nio-max').trim();
  // the two v2 harness properties that would render a broken column / legend if they dangled
  out['--sc@legrow'] = getComputedStyle(document.querySelector('#sp-legend-list .dv-leg-sw'))
                          .getPropertyValue('--sc').trim();
  const legList = document.getElementById('sp-legend-list');
  out['$legList-present'] = legList ? 'yes' : 'no';
  return out;
}"""


def hexify(rgb):
    """'rgb(26, 26, 26)' -> '#1A1A1A'. A computed colour and a token literal are the same value in
    two notations; comparing the strings raw manufactures a false failure."""
    # ⚠ Only convert what is ACTUALLY an rgb() string. A first pass ran the digit-scrape over
    # every input, so '#1A1A1A' yielded the digits 1,1,1 and became '#010101' — an instrument
    # that manufactures a mismatch out of a correct page. Gate on the notation first.
    import re as _re
    v = (rgb or "").strip()
    if not v.lower().startswith("rgb"):
        return v.upper()
    m = _re.findall(r"\d+", v)
    return "#%02X%02X%02X" % (int(m[0]), int(m[1]), int(m[2]))

SURFACE_PROBE = """() => {
  const bg = el => getComputedStyle(el).backgroundColor;
  const card = document.querySelector('.stat-card.tpl-panel');
  const donutSeg = document.querySelector('.dv-donut-seg');
  return {
    body: bg(document.body),
    card: bg(card),
    // the donut separates its arcs with stroke="var(--page)" — if re-pointing --page on <body>
    // had leaked into component scopes, THIS is where it would show up as grey seams.
    donutStroke: getComputedStyle(donutSeg).stroke,
    bodyMargin: getComputedStyle(document.body).marginTop,
    // ⚠ THE ds-039 SECOND-SPECIES PROBE. A page <style> whose comment contains a comment
    // terminator loses the rule that follows it — silently, with no error anywhere. Count the
    // rules the browser actually PARSED and look for the body rule by name.
    pageRules: (() => { const ss = [...document.styleSheets].find(s => !s.href);
      if (!ss) return { n: 0, hasBody: false };
      const sel = [...ss.cssRules].map(r => r.selectorText || '');
      return { n: sel.length, hasBody: sel.includes('body') }; })(),
  };
}"""

RADIUS_PROBE = """() => {
  const out = { fields: [], controls: {} };
  document.querySelectorAll('.search.boxed').forEach(el => {
    const cs = getComputedStyle(el);
    out.fields.push({ r: cs.borderTopLeftRadius, tok: cs.getPropertyValue('--border-radius-control').trim() });
  });
  const pick = (sel, k) => { const e = document.querySelector(sel);
    out.controls[k] = e ? getComputedStyle(e).borderTopLeftRadius : '(absent)'; };
  pick('.cn-amount-input .ai-box, .cn-amount-input input', 'amount-input');
  pick('.cn-dropdown .trigger', 'dropdown');
  pick('.cn-account-selector .as-trigger', 'account-selector');
  pick('.btn.primary', 'button');
  return out;
}"""

GHOST_PROBE = """() => {
  const g = [...document.querySelectorAll('.dv-series[data-series-group].is-ghost')]
              .map(e => e.getAttribute('data-series-group'));
  const val = document.querySelector('[data-dv-view="value"] .dv-val');
  return { ghost: [...new Set(g)].sort().join(','), centre: val ? val.textContent.trim() : '' };
}"""

LIST_CHROME_PROBE = """() => {
  const ul = document.querySelector('#acctList ul.list');
  const li2 = document.querySelectorAll('#acctList ul.list li')[1];
  const tag = document.querySelector('#acctList .row .tag');
  const cs = getComputedStyle(ul), ls = getComputedStyle(li2), ts = getComputedStyle(tag);
  return {
    ulBg: cs.backgroundColor, ulBorder: cs.borderTopWidth,
    sep: ls.borderTopWidth + ' ' + ls.borderTopStyle,
    tagBorder: ts.borderTopWidth,
    rowMinH: getComputedStyle(document.querySelector('#acctList .row')).minHeight,
  };
}"""


def drive_legend(pg, host_sel):
    """Two gestures on one legend, reading the chart back after each.
    gesture 1 = uncheck series 3's swatch   gesture 2 = isolate series 1 by its label."""
    seen = {}
    pg.click(host_sel + ' .dv-legrow[data-series="3"] .dv-leg-sw')
    pg.wait_for_timeout(260)          # settle: .is-ghost drives a transitioned opacity
    seen["uncheck3"] = pg.evaluate(GHOST_PROBE)
    pg.click(host_sel + ' .dv-leg-item[data-series="1"]')
    pg.wait_for_timeout(260)
    seen["isolate1"] = pg.evaluate(GHOST_PROBE)
    return seen


def stage_a(p):
    """Tokens, measure, radius, and the v1 POSITIVE CONTROLS."""
    b = launch(p)
    pg = b.new_page(viewport={"width": 1800, "height": 1200})

    # ---- font, with two controls (a boolean check cannot fail; a measurement can)
    pg.goto(V2); pg.wait_for_timeout(1100)
    f = pg.evaluate(FONT_PROBE)
    ok("font: HSBC cut resolves, distinct from both controls",
       abs(f["target"] - f["uf"]) < 0.5 and abs(f["target"] - f["ctrl_dejavu"]) > 1
       and abs(f["target"] - f["ctrl_missing"]) > 1, str(f))

    for mode, want_tok in (("light", "--surface-subtle"), ("dark", "--background-default")):
        pg.evaluate("m => document.documentElement.setAttribute('data-theme', m)", mode)
        pg.wait_for_timeout(300)

        # ---- 7. VAR SWEEP
        v = pg.evaluate(VAR_PROBE, V2_VARS)
        empty = [k for k, x in v.items() if not x]
        ok(f"[{mode}] var sweep — 0 empty of {len(v)}", not empty, str(empty))
        ok(f"[{mode}] v2's page <style> parsed WHOLE — body rule present",
           pg.evaluate(SURFACE_PROBE)["pageRules"]["hasBody"])

        # ---- 1. PAGE GREY
        s = pg.evaluate(SURFACE_PROBE)
        ok(f"[{mode}] v2 page background differs from card",
           s["body"] != s["card"], f"body {s['body']} vs card {s['card']}")
        ok(f"[{mode}] page --page reads {want_tok}",
           hexify(v["--page"]) == hexify(v[want_tok]),
           f"--page {v['--page']} / {want_tok} {v[want_tok]}")
        ok(f"[{mode}] body paints WITH that value (the rule is parsed, not merely written)",
           hexify(s["body"]) == hexify(v[want_tok]), f"body {s['body']}")
        ok(f"[{mode}] body margin is 0 — v1's dead rule also carried this",
           s["bodyMargin"] == "0px", s["bodyMargin"])
        ok(f"[{mode}] donut arc stroke NOT re-pointed by the body --page change",
           hexify(s["donutStroke"]) == hexify(v["--background-default"]),
           f"stroke {s['donutStroke']} vs --background-default {v['--background-default']}")

        # ---- 2. 1600px
        ok(f"[{mode}] --l-max on main is 1600px", v["--l-max@main"] == "1600px", v["--l-max@main"])
        w = pg.evaluate("() => document.querySelector('main').getBoundingClientRect().width")
        ok(f"[{mode}] main RENDERS at 1600px in an 1800px viewport", abs(w - 1600) < 1, f"{w}px")

        # ---- 3. SEARCH-FIELD RADIUS
        r = pg.evaluate(RADIUS_PROBE)
        ok(f"[{mode}] every .search.boxed radius == --border-radius-control ({len(r['fields'])} fields)",
           len(r["fields"]) >= 2 and all(x["r"] == x["tok"] and x["r"] != "0px" for x in r["fields"]),
           str(r["fields"]))
        ok(f"[{mode}] the rest of the control family already agreed",
           all(x == "8px" for x in r["controls"].values()), str(r["controls"]))

    # ================= POSITIVE CONTROLS on v1 — the tests must be ABLE to fail =============
    pg.goto(V1); pg.wait_for_timeout(900)
    v1s = pg.evaluate(SURFACE_PROBE)
    ok("CONTROL v1 (light): page background is NOT distinct from a card — the defect v2 ① fixes",
       v1s["body"] == v1s["card"], f"body {v1s['body']} == card {v1s['card']}")
    ok("CONTROL v1: its page <style> LOST its body rule to a comment terminator (ds-039 species 2)",
       not v1s["pageRules"]["hasBody"], f"{v1s['pageRules']['n']} rules parsed, body rule absent")
    ok("CONTROL v1: and so carries the browser's default body margin",
       v1s["bodyMargin"] != "0px", v1s["bodyMargin"])
    v1r = pg.evaluate(RADIUS_PROBE)
    ok("CONTROL v1: .search.boxed radius is 0px while the token says 8px — v2 ③'s root cause",
       all(x["r"] == "0px" and x["tok"] == "8px" for x in v1r["fields"]), str(v1r["fields"]))
    v1m = pg.evaluate("() => getComputedStyle(document.querySelector('main')).getPropertyValue('--l-max').trim()")
    ok("CONTROL v1: --l-max is canon's 1120px default", v1m == "1120px", v1m)

    # ============ INHERITED DEFECT, RECORDED NOT PASSED OVER ============================
    # canon's data-series palette stops at 5 (--data-series-6/7/8 are defined NOWHERE in
    # canon.css). The Nio donut has SIX categories, so its sixth arc falls back to pure black
    # in BOTH modes and its legend swatch — which paints from --sc:var(--data-series-6) — falls
    # back to TRANSPARENT and disappears. Present in v1 and inherited unchanged by v2, because
    # the honest fix is a new palette step and this page mints no colour. Asserted here so the
    # defect is a measurement in the record, not an impression.
    sw = pg.evaluate("""() => [...document.querySelectorAll('#sp-legend .dv-legrow')].map((r,i)=>{
        const e=r.querySelector('.dv-leg-sw'); const cs=getComputedStyle(e);
        const arc=document.querySelector('.dv-donut-seg[data-series-group="'+(i+1)+'"]');
        return { i:i+1, sc:cs.getPropertyValue('--sc').trim(), bg:cs.backgroundColor,
                 arc: getComputedStyle(arc).fill }; })""")
    ok("DEFECT (inherited): series 1-5 swatches paint from a defined --data-series-N",
       all(x["sc"] and x["bg"] != "rgba(0, 0, 0, 0)" for x in sw[:5]),
       str([x["sc"] for x in sw[:5]]))
    ok("DEFECT (inherited, DECLARED): series 6 has NO token — swatch transparent, arc silent black",
       sw[5]["sc"] == "" and sw[5]["bg"] == "rgba(0, 0, 0, 0)" and sw[5]["arc"] == "rgb(0, 0, 0)",
       f"--sc '{sw[5]['sc']}' swatch {sw[5]['bg']} arc {sw[5]['arc']}  [logged, NOT fixed here]")
    b.close()


def stage_b(p):
    """Drive the switches: theme (mouse + keyboard), legend parity + mutation, list chrome."""
    b = launch(p)
    pg = b.new_page(viewport={"width": 1800, "height": 1200})
    pg.goto(V2); pg.wait_for_timeout(1100)

    # ---- 4. THEME SWITCH — clicked, then keyboard-driven
    pg.click('#rvMode button[data-v="dark"]'); pg.wait_for_timeout(250)
    ok("theme switch: CLICK sets data-theme=dark",
       pg.evaluate("() => document.documentElement.getAttribute('data-theme')") == "dark")
    ok("theme switch: aria-pressed follows the click",
       pg.evaluate("""() => document.querySelector('#rvMode button[data-v="dark"]')
                        .getAttribute('aria-pressed')""") == "true")
    pg.focus('#rvMode button[data-v="light"]')
    pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    ok("theme switch: KEYBOARD (focus + Enter) returns to light",
       pg.evaluate("() => document.documentElement.getAttribute('data-theme')") == "light")
    ind = pg.evaluate("""() => { const s=document.querySelector('#rvMode .ind');
        return { w: s.style.width, l: s.style.left }; }""")
    ok("theme switch: canon's own placeSegs moved the segmented indicator",
       ind["w"] not in ("", "0px"), str(ind))

    # ---- 5. LEGEND PARITY
    cap = drive_legend(pg, "#sp-legend")
    r = pg.query_selector("#sp-legend .dv-leg-reset")
    if r and not r.is_disabled():
        r.click(); pg.wait_for_timeout(250)
    ok("capsule legend returns to rest after Reset",
       pg.evaluate(GHOST_PROBE)["ghost"] == "")

    pg.click('#rvLeg button[data-v="list"]'); pg.wait_for_timeout(350)
    ok("legend switch: exactly ONE .dv-leg is discoverable in the donut figure",
       pg.evaluate("""() => document.querySelector('#sp-legend').closest('figure')
                        .querySelectorAll('.dv-leg').length""") == 1)
    ok("legend switch: the list legend is the visible one",
       pg.evaluate("""() => { const l=document.getElementById('sp-legend-list');
           return !l.hasAttribute('hidden') && l.classList.contains('dv-leg'); }"""))
    ok("legend switch: the separate figures column is withdrawn in list mode",
       pg.evaluate("() => document.getElementById('spSummary').hidden"))
    ok("list legend carries swatch + letter + label + VALUE on every row",
       pg.evaluate("""() => [...document.querySelectorAll('#sp-legend-list .dv-legrow')]
           .every(r => r.querySelector('.dv-leg-sw') && r.querySelector('.dv-key')
                    && r.querySelector('.dv-leg-name') && r.querySelector('.nio-leg-val'))"""))

    # ---- the list legend must sit BESIDE the donut, not under it
    geo = pg.evaluate("""() => { const svg=document.querySelector('.dv-donut-row .dv-svg');
        const leg=document.getElementById('sp-legend-list');
        const a=svg.getBoundingClientRect(), b=leg.getBoundingClientRect();
        return { beside: b.left >= a.right - 4, svgRight: Math.round(a.right), legLeft: Math.round(b.left) }; }""")
    ok("list legend sits BESIDE the donut, not beneath it", geo["beside"], str(geo))

    lst = drive_legend(pg, "#sp-legend-list")

    for g in ("uncheck3", "isolate1"):
        ok(f"PARITY [{g}]: same series ghosted in capsule and list",
           cap[g]["ghost"] == lst[g]["ghost"],
           f"capsule '{cap[g]['ghost']}' vs list '{lst[g]['ghost']}'")
        ok(f"PARITY [{g}]: same donut centre figure",
           cap[g]["centre"] == lst[g]["centre"],
           f"capsule '{cap[g]['centre']}' vs list '{lst[g]['centre']}'")
    ok("PARITY: isolate LATCH (DV-D19) reached in both — isolate1 ghosts five of six",
       cap["isolate1"]["ghost"] == "2,3,4,5,6" == lst["isolate1"]["ghost"],
       cap["isolate1"]["ghost"])

    # MUTATION — a parity check that cannot fail is not a check.
    mutated = cap["uncheck3"]["ghost"].replace("3", "9")
    ok("MUTATION: the parity assertion GOES RED against a wrong series id",
       mutated != lst["uncheck3"]["ghost"], f"mutant '{mutated}'")

    # ---- 6. LIST CHROME
    r = pg.query_selector("#sp-legend-list .dv-leg-reset")
    if r and not r.is_disabled():
        r.click(); pg.wait_for_timeout(200)
    chrome = {}
    for v in ("card", "flush", "flush-plain"):
        pg.click(f'#rvList button[data-v="{v}"]'); pg.wait_for_timeout(260)
        chrome[v] = pg.evaluate(LIST_CHROME_PROBE)
        print("    list/" + v + ": " + str(chrome[v]))
    # ⚠ --surface-transparent is #FFFFFF00, so it computes to rgba(255,255,255,0) — transparent
    # WHITE, not transparent black. Assert the ALPHA, not a literal string: the notation is not
    # the fact. (A first pass compared against 'rgba(0, 0, 0, 0)' and went red on a correct page.)
    def alpha(c):
        import re as _re
        m = _re.findall(r"[\d.]+", c)
        return float(m[3]) if len(m) > 3 else 1.0

    ok("list CARD form draws the card: opaque background + a 1px border",
       chrome["card"]["ulBorder"] == "1px" and alpha(chrome["card"]["ulBg"]) == 1.0,
       chrome["card"]["ulBg"])
    for v in ("flush", "flush-plain"):
        ok(f"list {v}: card background and border are GONE",
           chrome[v]["ulBorder"] == "0px" and alpha(chrome[v]["ulBg"]) == 0.0,
           str(chrome[v]))
        ok(f"list {v}: the SEPARATOR survives (that is the brief)",
           chrome[v]["sep"].startswith("1px") and "solid" in chrome[v]["sep"], chrome[v]["sep"])
        ok(f"list {v}: row geometry and behaviour untouched (min-height)",
           chrome[v]["rowMinH"] == chrome["card"]["rowMinH"], chrome[v]["rowMinH"])
    ok("list flush KEEPS the tag outline; flush-plain drops it",
       chrome["flush"]["tagBorder"] == "1px" and chrome["flush-plain"]["tagBorder"] == "0px",
       f"flush {chrome['flush']['tagBorder']} / plain {chrome['flush-plain']['tagBorder']}")
    ok("row press/focus affordance survives chromeless (button rows still focusable)",
       pg.evaluate("""() => { const b=document.querySelector('#acctList .row');
           b.focus(); return document.activeElement === b; }"""))
    b.close()


def stage_shots(p):
    b = launch(p)
    os.makedirs(OUT, exist_ok=True)

    def shot(name, w, h, setup=None, clip_sel=None, full=True):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(V2); pg.wait_for_timeout(1200)
        if setup:
            setup(pg); pg.wait_for_timeout(500)
        path = os.path.join(OUT, name)
        if clip_sel:
            pg.query_selector(clip_sel).screenshot(path=path)
        else:
            pg.screenshot(path=path, full_page=full)
        pg.close()
        print("    shot -> " + path)

    shot("nio-v2-01-full-light-1800.png", 1800, 1200)
    shot("nio-v2-02-full-dark-1800.png", 1800, 1200,
         lambda pg: pg.click('#rvMode button[data-v="dark"]'))
    shot("nio-v2-03-donut-list-legend.png", 1800, 1200,
         lambda pg: pg.click('#rvLeg button[data-v="list"]'),
         clip_sel=".nio-donut-split")
    shot("nio-v2-04-donut-capsule-legend.png", 1800, 1200, None, clip_sel=".nio-donut-split")
    shot("nio-v2-05-list-chromeless.png", 1800, 1200,
         lambda pg: pg.click('#rvList button[data-v="flush"]'), clip_sel="#acctList")
    shot("nio-v2-06-list-chromeless-plain.png", 1800, 1200,
         lambda pg: pg.click('#rvList button[data-v="flush-plain"]'), clip_sel="#acctList")
    shot("nio-v2-07-list-card.png", 1800, 1200, None, clip_sel="#acctList")
    shot("nio-v2-08-masthead-1800.png", 1800, 600, None, full=False)
    shot("nio-v2-09-narrow-560.png", 560, 900, None)
    b.close()


def main():
    stage = "a"
    for a in sys.argv[1:]:
        if a.startswith("--stage"):
            stage = a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        {"a": stage_a, "b": stage_b, "shots": stage_shots}[stage](p)
    bad = [r for r in RESULTS if not r[0]]
    print("\n==================== VERDICT (stage %s) ====================" % stage)
    print("  %d checks, %d PASS, %d FAIL" % (len(RESULTS), len(RESULTS) - len(bad), len(bad)))
    for _, n, d in bad:
        print("  FAIL: " + n + "  " + d)
    print("  RESULT: " + ("RED" if bad else "GREEN"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
