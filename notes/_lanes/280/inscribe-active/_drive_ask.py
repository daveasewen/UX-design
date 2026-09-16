#!/usr/bin/env python3
"""_drive_ask.py — drive ASK-2026-09-16.html, assert the envelope, then screenshot it never-driven.

  source knowledge/_render/seat_env.sh && python3 notes/_lanes/280/inscribe-active/_drive_ask.py

Pass 1 drives a context: ticks one answer of each kind, notes one row, exports, asserts the JSON is the
#279 sheet's envelope and that each answer carries exactly the drawings its option names, then reloads
to prove localStorage round-trips. Pass 2 opens a FRESH never-driven context (light + dark, 1280 + 390),
asserts it is virgin and free of horizontal overflow, and takes the PNGs. Disk is tight, so the shots
are the first viewport and the first row, not full pages.
"""
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
PAGE = LANE / "ASK-2026-09-16.html"
SHOTS = LANE / "shots"
SHOTS.mkdir(exist_ok=True)
URL = PAGE.as_uri()

fails = []


def check(name, ok, detail=""):
    print("  %s  %s%s" % ("ok   " if ok else "FAIL ", name, ("  [%s]" % detail) if detail and not ok else ""))
    if not ok:
        fails.append(name)


html = PAGE.read_text(encoding="utf-8")
measured = json.loads(html.split('id="measured">', 1)[1].split("</script>", 1)[0])
BASES = measured["bases"]
EXPORT_JSON = json.loads((REPO / "notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json")
                         .read_text(encoding="utf-8"))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    ctx = b.new_context(viewport={"width": 1280, "height": 1400}, color_scheme="light")
    pg = ctx.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL)
    pg.wait_for_timeout(400)

    check("one section per asked row", pg.locator("section.base").count() == len(BASES))
    check("every glyph is drawn four times (two sizes x two chromes)",
          pg.locator("svg.g").count() == measured["glyphs"] * 4)
    check("no ruling id in the body copy",
          "s277" not in pg.inner_text("header.hero") and
          not any("s277" in pg.locator("section.base").nth(i).inner_text() for i in range(len(BASES))))
    dupes = pg.evaluate("""() => {var s={},d=[];document.querySelectorAll('[id]').forEach(function(e){
        if(s[e.id])d.push(e.id);s[e.id]=1;});return d;}""")
    check("no duplicate DOM ids", not dupes, str(dupes[:5]))
    check("nothing is pre-selected on first load",
          pg.evaluate("() => document.querySelectorAll('input:checked').length") == 0)
    check("his own words are quoted on every row",
          all(EXPORT_JSON["answers"][bs]["note"].strip() in pg.inner_text('section[data-base="%s"]' % bs)
              for bs in BASES if EXPORT_JSON["answers"][bs]["note"].strip()))
    check("the progress line starts empty",
          pg.inner_text("#prog").strip() == "0 of %d answered" % len(BASES))

    # tick the first option on the first row, the last option on the second, note the third
    first, second, third = BASES[0], BASES[1], BASES[2]
    o1 = pg.locator('input[name="%s"]' % first).first
    want1 = {"twin": o1.get_attribute("data-twin") or None,
             "flags": [f for f in (o1.get_attribute("data-flags") or "").split(",") if f],
             "choice": o1.get_attribute("value")}
    o1.check()
    o2 = pg.locator('input[name="%s"]' % second).last
    want2 = {"twin": o2.get_attribute("data-twin") or None,
             "flags": [f for f in (o2.get_attribute("data-flags") or "").split(",") if f],
             "choice": o2.get_attribute("value")}
    o2.check()
    pg.fill('textarea.note[data-base="%s"]' % third, "driver note")
    pg.wait_for_timeout(600)
    check("progress counts only answered rows",
          pg.inner_text("#prog").strip() == "2 of %d answered" % len(BASES),
          pg.inner_text("#prog"))
    check("the chosen twin's card is marked",
          pg.locator('section[data-base="%s"] .card.chosen' % first).count()
          == (1 if want1["twin"] else 0))

    with pg.expect_download() as dl:
        pg.click("#btnExport")
    d = dl.value
    check("export downloads the named file", d.suggested_filename == measured["export_filename"],
          d.suggested_filename)
    exp = json.loads(pg.inner_text("#exp"))
    check("envelope keys page/at/exportedAt/answers", set(exp) == {"page", "at", "exportedAt", "answers"},
          str(sorted(exp)))
    check("page id matches", exp["page"] == measured["page"])
    check("at == exportedAt, ISO", exp["at"] == exp["exportedAt"] and exp["at"].endswith("Z"))
    check("answers keyed by every asked row", sorted(exp["answers"]) == sorted(BASES))
    check("every answer is {choice, twin, flags[], note}",
          all(set(v) == {"choice", "twin", "flags", "note"} and isinstance(v["flags"], list)
              for v in exp["answers"].values()))
    a = exp["answers"]
    check("the first row exports exactly what its option names",
          a[first] == {"choice": want1["choice"], "twin": want1["twin"], "flags": want1["flags"],
                       "note": ""}, json.dumps(a[first]))
    check("the last option of the second row exports as itself",
          a[second] == {"choice": want2["choice"], "twin": want2["twin"], "flags": want2["flags"],
                        "note": ""}, json.dumps(a[second]))
    check("a note with no answer still exports",
          a[third] == {"choice": None, "twin": None, "flags": [], "note": "driver note"},
          json.dumps(a[third]))
    check("unanswered rows export with a null choice",
          len([k for k, v in a.items() if v["choice"] is None]) == len(BASES) - 2)
    (LANE / "_driver-export.json").write_text(json.dumps(exp, indent=2), encoding="utf-8")

    pg.reload()
    pg.wait_for_timeout(500)
    rt = pg.evaluate("() => window.__askExport()")["answers"]
    check("localStorage round-trips every answer across a reload", rt == a)
    pg.evaluate("() => localStorage.clear()")
    ctx.close()
    check("no page errors in the driven pass", not errors, "; ".join(errors))

    for theme in ("light", "dark"):
        for w, h in ((1280, 900), (390, 844)):
            c2 = b.new_context(viewport={"width": w, "height": h}, color_scheme=theme)
            p2 = c2.new_page()
            p2.goto(URL)
            p2.wait_for_timeout(500)
            virgin = p2.evaluate("() => document.querySelectorAll('input:checked').length"
                                 " + [...document.querySelectorAll('textarea.note')]"
                                 ".filter(t => t.value).length")
            check("fresh context is virgin before the %s %d PNG" % (theme, w), virgin == 0, str(virgin))
            ov = p2.evaluate("() => document.documentElement.scrollWidth"
                             " - document.documentElement.clientWidth")
            check("no horizontal overflow at %d (%s)" % (w, theme), ov <= 0, str(ov))
            p2.screenshot(path=str(SHOTS / ("ask-%d-%s-top.png" % (w, theme))), full_page=False)
            p2.locator("section.base").first.screenshot(
                path=str(SHOTS / ("ask-%d-%s-row01.png" % (w, theme))))
            c2.close()
    b.close()

print("\n%d failures%s" % (len(fails), (": " + ", ".join(fails)) if fails else ""))
sys.exit(1 if fails else 0)
