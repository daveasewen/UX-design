#!/usr/bin/env python3
"""_drive_review.py — DRIVE REVIEW-active-2026-09-16.html, then screenshot it fresh.

Pass 1 (driven context): first load is virgin; tick one of each kind of answer — a twin
on one base, "none" on another, a flag with two checkboxes on the three-candidate base —
type a note, export, and assert the JSON envelope:

  {page, at, exportedAt, answers: {<base>: {choice, twin, flags[], note}}}   × every base

then reload and assert localStorage round-trips all of it.

Pass 2 (NEVER-DRIVEN fresh context, storage cleared): light + dark × 1280 + 390, full
page, plus a 1280 crop of the first row. No residue from pass 1 can be in the PNGs.

    PLAYWRIGHT_BROWSERS_PATH=/tmp/pw LD_LIBRARY_PATH=/tmp/lib \\
      python3 notes/_lanes/279/active-review/_drive_review.py
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANE = Path(__file__).resolve().parent
PAGE = LANE / "REVIEW-active-2026-09-16.html"
URL = "file://" + str(PAGE)
SHOTS = LANE / "shots"
SHOTS.mkdir(exist_ok=True)

fails = []


def check(name, ok, detail=""):
    print(("  ok   " if ok else "  FAIL ") + name + (f"  — {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


html = PAGE.read_text(encoding="utf-8")
measured = json.loads(re.search(r'<script type="application/json" id="measured">(.*?)</script>', html, re.S).group(1))
N_BASES, N_CANDS = measured["bases"], measured["candidates"]
body = re.sub(r"<script.*?</script>|<style.*?</style>|<footer.*?</footer>", "", html, flags=re.S)
check("no ruling id in the body copy (footer only)", not re.search(r"\bs\d{3}-D\d+\b", body))
check("ruling id present once in the footer", html.count("s277-D6") == 1)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    ctx = b.new_context(viewport={"width": 1280, "height": 1400}, color_scheme="light")
    pg = ctx.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL)
    pg.evaluate("() => localStorage.clear()")
    pg.reload()
    pg.wait_for_timeout(500)

    # ---- structure ----------------------------------------------------------
    n_sec = pg.evaluate("() => document.querySelectorAll('section.base').length")
    n_cand = pg.evaluate("() => document.querySelectorAll('.card.on').length")
    n_svg = pg.evaluate("() => document.querySelectorAll('svg.g').length")
    check(f"{N_BASES} base rows on the page", n_sec == N_BASES, str(n_sec))
    check(f"{N_CANDS} candidate cards", n_cand == N_CANDS, str(n_cand))
    check("every glyph rendered 2 sizes × 2 chromes", n_svg == measured["glyphs"] * 4, str(n_svg))
    ids_ok = pg.evaluate("""() => { const s = new Set(); let dup = 0;
        for (const el of document.querySelectorAll('[id]')) { if (s.has(el.id)) dup++; s.add(el.id); } return dup; }""")
    check("no duplicate DOM ids (namespaced clip-paths)", ids_ok == 0, str(ids_ok))
    radios = pg.evaluate("() => document.querySelectorAll('input[type=radio]').length")
    check("radios = candidates + 2 per base", radios == N_CANDS + 2 * N_BASES, str(radios))
    boxes = pg.evaluate("() => document.querySelectorAll('input[type=checkbox]').length")
    check("one flag checkbox per candidate", boxes == N_CANDS, str(boxes))
    ticked = pg.evaluate("() => document.querySelectorAll('input:checked').length")
    notes = pg.evaluate("() => [...document.querySelectorAll('textarea.note')].filter(t => t.value).length")
    check("virgin first load: nothing ticked, no note", ticked == 0 and notes == 0)
    check("progress reads 0 of N", pg.inner_text("#prog").strip() == f"0 of {N_BASES} decided", pg.inner_text("#prog"))
    ov = pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("no horizontal overflow at 1280", ov <= 0, str(ov))
    # glyph paint: every 48px svg has a non-zero box
    zero = pg.evaluate("() => [...document.querySelectorAll('svg.g48')].filter(s => s.getBoundingClientRect().width < 40).length")
    check("every 48px glyph lays out at 48px", zero == 0, str(zero))

    # ---- drive one of each kind ---------------------------------------------
    bases = pg.evaluate("() => [...document.querySelectorAll('section.base')].map(s => s.dataset.base)")
    three = pg.evaluate("() => [...document.querySelectorAll('section.base')].find(s => s.querySelectorAll('.card.on').length === 3).dataset.base")
    twin_base = bases[0]
    none_base = [x for x in bases if x not in (twin_base, three)][0]
    twin_slug = pg.evaluate(f"() => document.querySelector('section[data-base=\"{twin_base}\"] .card.on').dataset.cand")
    pg.check(f'input[name="{twin_base}"][data-twin="{twin_slug}"]')
    pg.check(f'input[name="{none_base}"][value="none"]')
    flag_slugs = pg.evaluate(f"() => [...document.querySelectorAll('input[name=\"{three}--flag\"]')].slice(0, 2).map(c => c.value)")
    for s in flag_slugs:
        pg.check(f'input[name="{three}--flag"][value="{s}"]')
    check("ticking a flag checkbox selects the flag radio", pg.is_checked(f'input[name="{three}"][value="flag"]'))
    pg.fill(f'textarea.note[data-base="{twin_base}"]', "driver note")
    pg.wait_for_timeout(600)
    check("progress reads 3 of N", pg.inner_text("#prog").strip() == f"3 of {N_BASES} decided", pg.inner_text("#prog"))
    check("chosen twin card is marked", pg.evaluate(f"() => document.querySelector('section[data-base=\"{twin_base}\"] .card.chosen').dataset.cand") == twin_slug)

    # ---- export --------------------------------------------------------------
    with pg.expect_download() as dl:
        pg.click("#btnExport")
    d = dl.value
    check("export downloads the named file", d.suggested_filename == measured["export_filename"], d.suggested_filename)
    exp = json.loads(pg.inner_text("#exp"))
    check("envelope keys page/at/exportedAt/answers", set(exp) == {"page", "at", "exportedAt", "answers"}, str(sorted(exp)))
    check("page id matches", exp["page"] == measured["page"])
    check("at == exportedAt, ISO", exp["at"] == exp["exportedAt"] and exp["at"].endswith("Z"))
    check("answers keyed by every base", sorted(exp["answers"]) == sorted(bases))
    shape_ok = all(set(v) == {"choice", "twin", "flags", "note"} and isinstance(v["flags"], list) for v in exp["answers"].values())
    check("every answer is {choice, twin, flags[], note}", shape_ok)
    a = exp["answers"]
    check("twin answer", a[twin_base] == {"choice": "twin", "twin": twin_slug, "flags": [], "note": "driver note"}, json.dumps(a[twin_base]))
    check("none answer", a[none_base] == {"choice": "none", "twin": None, "flags": [], "note": ""}, json.dumps(a[none_base]))
    check("flag answer", a[three] == {"choice": "flag", "twin": None, "flags": flag_slugs, "note": ""}, json.dumps(a[three]))
    undecided = [k for k, v in a.items() if v["choice"] is None]
    check(f"{N_BASES - 3} undecided export as null choice", len(undecided) == N_BASES - 3, str(len(undecided)))
    (LANE / "_driver-export.json").write_text(json.dumps(exp, indent=2), encoding="utf-8")

    # ---- round-trip ----------------------------------------------------------
    pg.reload()
    pg.wait_for_timeout(500)
    rt = pg.evaluate("() => window.__reviewExport()")["answers"]
    check("localStorage round-trips every answer across a reload",
          {k: v for k, v in rt.items()} == a, "")
    check("progress restored after reload", pg.inner_text("#prog").strip() == f"3 of {N_BASES} decided")
    pg.evaluate("() => localStorage.clear()")
    ctx.close()
    check("no page errors in the driven pass", not errors, "; ".join(errors))

    # ---- pass 2: NEVER-DRIVEN fresh context ------------------------------------
    for theme in ("light", "dark"):
        for w, h in ((1280, 900), (390, 844)):
            c2 = b.new_context(viewport={"width": w, "height": h}, color_scheme=theme)
            p2 = c2.new_page()
            p2.goto(URL)
            p2.wait_for_timeout(600)
            t = p2.evaluate("() => document.querySelectorAll('input:checked').length + [...document.querySelectorAll('textarea.note')].filter(t => t.value).length")
            check(f"fresh context is virgin before the {theme} {w} PNG", t == 0, str(t))
            ov2 = p2.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(f"no horizontal overflow at {w} ({theme})", ov2 <= 0, str(ov2))
            p2.screenshot(path=str(SHOTS / f"ar-{w}-{theme}.png"), full_page=True)
            if w == 1280:
                p2.screenshot(path=str(SHOTS / f"ar-{w}-{theme}-top.png"), full_page=False)
                p2.locator("section.base").first.screenshot(path=str(SHOTS / f"ar-{w}-{theme}-row01.png"))
            else:
                p2.locator("section.base").first.screenshot(path=str(SHOTS / f"ar-{w}-{theme}-row01.png"))
            c2.close()
    b.close()

print(f"\n{len(fails)} failures" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
