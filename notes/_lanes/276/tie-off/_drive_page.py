#!/usr/bin/env python3
"""_drive_page.py — DRIVE the #276 lane TO review page, then screenshot it.

A green builder is not a review ([[art-director-reviews-lane-output-268]]), and no
gate in this repo parses a lane review page ([[no-gate-parses-the-artefact]]), so this
driver opens the real file in chromium and measures:

  1. console        — 0 errors and 0 page errors of any kind.
  2. descenders     — TWO measurements, because one alone lies here:
                      (a) the canvas-probe clause from knowledge/_validate_demo_page.py
                          (the PROVEN shape, not a new one) on the TIGHT-BOX selectors
                          it was written for: own box, one line, no vertical padding.
                          Applying it to a padded or multi-line element reports a clip
                          that is not there (clientHeight stops being n x line-height),
                          which is why the selector list below is narrow and named.
                      (b) no element that CLIPS its overflow is overflowing: for every
                          computed overflow-y other than visible, scrollHeight must fit
                          clientHeight, except the two deliberate scroll containers.
  3. all-caps       — nam-002: no text-transform:uppercase anywhere, and no ALL-CAPS
                      run of >=4 chars in VISIBLE PROSE. Text inside <code>/<pre> is
                      excluded: a file path in code voice is not a name in caps.
  4. export         — the control produces the byte-compatible RK shape
                      {page, at, decisions:[{id, choice, note}]}, and localStorage
                      round-trips a choice and a note across a reload.
  5. mobile         — at 390px the document does not scroll horizontally.
  6. both themes    — s151-D1, the two-red law: the accent computes #DA1A00 on white
                      and #F6604C on the dark ground, and the descender and crop
                      clauses are re-run per theme rather than once (four-themes hook:
                      flexibility is the requirement, so test PER THEME).

Then it writes screenshot.png (full page, desktop, LIGHT) beside the HTML.

    source knowledge/_render/seat_env.sh && \
      python3 notes/_lanes/276/tie-off/_drive_page.py
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
PAGE = LANE / "REVIEW-tie-off-2026-09-15-v1.html"
SHOT = LANE / "screenshot.png"
URL = "file://" + str(PAGE)

# The canvas probe from knowledge/_validate_demo_page.py:DESC_JS, retargeted at the
# small-type classes on this page. Same clause, same maths, different surface.
DESC_JS = r"""
(sel) => {
  const cvs = document.createElement('canvas'), ctx = cvs.getContext('2d');
  return [...document.querySelectorAll(sel)].map(el => {
    const cs = getComputedStyle(el);
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    const t = (el.textContent || '').trim().slice(0, 40);
    const m = ctx.measureText(t + 'gypq');
    const fA = m.fontBoundingBoxAscent, fD = m.fontBoundingBoxDescent;
    const aD = m.actualBoundingBoxDescent;
    const lh = cs.lineHeight === 'normal' ? (fA + fD) : parseFloat(cs.lineHeight);
    const ch = el.clientHeight, baseline = (lh - (fA + fD)) / 2 + fA;
    return {sel: sel, text: t, tt: cs.textTransform, lh: +lh.toFixed(2),
            boxH: +ch.toFixed(2), clip: +Math.max(0, (baseline + aD) - ch).toFixed(2)};
  });
}
"""

OVERFLOW_JS = r"""
() => {
  const out = [];
  for (const el of document.querySelectorAll('*')) {
    const c = getComputedStyle(el);
    if (c.overflowY === 'visible' && c.overflowX === 'visible') continue;
    if (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1)
      out.push({sel: el.tagName.toLowerCase() + '.' + (el.className || ''),
                oy: c.overflowY, ox: c.overflowX,
                dh: el.scrollHeight - el.clientHeight, dw: el.scrollWidth - el.clientWidth});
  }
  return out;
}
"""

CAPS_JS = r"""
() => {
  let tt = [];
  for (const el of document.querySelectorAll('*')) {
    const c = getComputedStyle(el);
    if (c.textTransform === 'uppercase' || c.fontVariantCaps === 'all-small-caps')
      tt.push(el.tagName + '.' + (el.className || ''));
  }
  // Visible PROSE only: strip code/pre, which carry file paths and identifiers.
  const clone = document.body.cloneNode(true);
  clone.querySelectorAll('code, pre, script, style').forEach(e => e.remove());
  document.body.appendChild(clone);
  const txt = clone.innerText;
  clone.remove();
  return {transform: [...new Set(tt)], text: txt};
}
"""

# Tight boxes only — own box, one line, no vertical padding. See the docstring.
SEL = [".label", ".decid", ".rec", ".stat b", ".stat span", ".said", "h3", "blockquote cite"]
# Deliberate scroll containers: the wide table and the export pane.
SCROLL_OK = ("div.tw", "pre.exp")
# nam-002 allows acronyms. Everything <=4 chars, plus the technical words this page
# must be able to print, is not a "name in caps".
ACRONYM_OK = {"WCAG", "JSON", "HTML", "CSS", "KG", "UX", "HSBC", "SC", "URL", "URLS",
              "API", "COGA", "ARIA", "APG", "EAA", "EU", "ICT", "W3C", "WAI", "CX",
              "NEW", "AA", "PDF", "KB", "MB", "ID", "IDS"}
CAPS_RUN = re.compile(r"\b[A-Z][A-Z0-9]{3,}(?:[ \-][A-Z][A-Z0-9]{3,})*\b")


def main():
    rows, fails = [], []

    def check(name, ok, detail=""):
        rows.append((name, ok, detail))
        if not ok:
            fails.append(name)

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1180, "height": 1400}, color_scheme="light")
        console, errors = [], []
        pg.on("console", lambda m: console.append((m.type, m.text)))
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(900)

        # 0 — the font actually loaded; a screenshot in a fallback face verifies nothing.
        font = pg.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')")
        check("font loaded (HSBC_MtUnivers_Latin)", bool(font), str(font))

        # 1 — console
        bad = [c for c in console if c[0] in ("error", "warning")]
        check("0 console errors / warnings / page errors", not bad and not errors,
              f"{len(console)} console message(s), {len(bad)} bad, {len(errors)} page error(s) "
              f"{bad[:2]}{errors[:2]}")

        # 2a — descenders, tight boxes, the _validate_demo_page clause
        probes = []
        for s in SEL:
            probes += pg.evaluate(DESC_JS, s)
        worst = max([r["clip"] for r in probes] or [0.0])
        check("descenders intact on the tight boxes (the _validate_demo_page clause)", worst == 0.0,
              f"{len(probes)} element(s) across {len(SEL)} selectors · worst clip {worst:.2f}px"
              + (" · " + json.dumps(sorted(probes, key=lambda r: -r["clip"])[0]) if worst else ""))

        # 2b — and nothing that clips its overflow is overflowing
        of = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
        check("no element crops its own content (overflow != visible and overflowing)", not of,
              json.dumps(of[:3]))

        # 3 — nam-002
        caps = pg.evaluate(CAPS_JS)
        runs = sorted({m for m in CAPS_RUN.findall(caps["text"]) if m not in ACRONYM_OK})
        check("no text-transform:uppercase (nam-002)", not caps["transform"],
              str(caps["transform"][:4]))
        check("no ALL-CAPS runs in visible text (nam-002)", not runs, str(runs[:6]))

        # 4 — export + localStorage round-trip
        pg.click("#D-1-a")
        pg.fill('textarea.note[data-id="D-3"]', "a note that must survive a reload")
        pg.click("#btnExport")
        pg.wait_for_timeout(400)
        exp = json.loads(pg.inner_text("#exp"))
        shape_ok = (set(exp) == {"page", "at", "decisions"}
                    and exp["page"] == PAGE.name
                    and [set(x) for x in exp["decisions"]] == [{"id", "choice", "note"}] * 6
                    and [x["id"] for x in exp["decisions"]] == [f"D-{i}" for i in range(1, 7)]
                    and exp["decisions"][0]["choice"] == "a"
                    and exp["decisions"][2]["note"] == "a note that must survive a reload")
        check("export is the RK shape {page, at, decisions:[{id, choice, note}]}", shape_ok,
              json.dumps(exp["decisions"][:2]))

        pg.reload()
        pg.wait_for_timeout(500)
        back = pg.evaluate("""() => ({
          a: document.querySelector('#D-1-a').checked,
          n: document.querySelector('textarea.note[data-id="D-3"]').value,
          said: document.getElementById('said').textContent})""")
        check("localStorage round-trips the choice and the note across a reload",
              back["a"] is True and back["n"] == "a note that must survive a reload"
              and back["said"].startswith("1 of 6"), json.dumps(back))

        # 5 — mobile
        pg.set_viewport_size({"width": 390, "height": 900})
        pg.wait_for_timeout(400)
        m = pg.evaluate("() => ({s: document.documentElement.scrollWidth, "
                        "c: document.documentElement.clientWidth})")
        check("390px: no horizontal scroll", m["s"] <= m["c"], json.dumps(m))

        # 6 — both themes. s151-D1 is background-keyed, so it has to be read per theme.
        pg.set_viewport_size({"width": 1180, "height": 1400})
        pg.evaluate("() => localStorage.clear()")
        for theme, want in (("light", "rgb(218, 26, 0)"), ("dark", "rgb(246, 96, 76)")):
            pg.emulate_media(color_scheme=theme)
            pg.reload()
            pg.wait_for_timeout(500)
            got = pg.evaluate("() => getComputedStyle(document.querySelector('.label')).color")
            probes2 = []
            for s in SEL:
                probes2 += pg.evaluate(DESC_JS, s)
            w2 = max([r["clip"] for r in probes2] or [0.0])
            of2 = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
            check(f"{theme}: accent is the two-red law value, 0 crop, 0 overflow (s151-D1)",
                  got == want and w2 == 0.0 and not of2,
                  f"accent {got} (want {want}) · worst clip {w2:.2f}px · {len(of2)} overflowing")

        # screenshot, desktop, full page, LIGHT — the artefact the art director reviews
        pg.emulate_media(color_scheme="light")
        pg.reload()
        pg.wait_for_timeout(900)
        pg.screenshot(path=str(SHOT), full_page=True)
        b.close()

    w = max(len(r[0]) for r in rows)
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{w}s}  {detail}")
    print(f"\nwrote {SHOT} ({SHOT.stat().st_size:,} bytes)")
    print("DRIVE PASS" if not fails else f"DRIVE FAIL — {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
