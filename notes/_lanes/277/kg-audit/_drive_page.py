#!/usr/bin/env python3
"""_drive_page.py — DRIVE the #277 lane A2 review page, then screenshot it.

Adapted from notes/_lanes/277/page/_drive_page.py (lane CP's, not touched).
Keeps every generic check CP ran — font, console, descenders, overflow,
nam-002 caps, order (decisions before evidence, first ask in the top
quarter), attribution, export shape + localStorage round-trip, 390px both
themes, two-red law at 1280 — and replaces CP's page-specific checks with
this page's own:

  A. SIX decisions, D-1..D-6, D-1 is the layers question.
  B. Every card has exactly one Recommended option, except D-6 which follows
     A3's ranking (or is a marked placeholder with none).
  C. The hero states the answer rate once (6 of 12) and the design-time rate
     (4 of 12), read from the measured block, never typed.
  D. D-1 names the rulings it touches by id (s274-D11, s275-D6, s275-D4).
  E. Dave's words appear once, verbatim, in a blockquote with a cite.

Screenshots: light and dark, full page, 1280 and 390; plus the decisions
region at 1280 in both themes.

    source knowledge/_render/seat_env.sh && \
      python3 notes/_lanes/277/kg-audit/_drive_page.py
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANE = Path(__file__).resolve().parent
PAGE = LANE / "REVIEW-kg-audit-2026-09-16-v1.html"
URL = "file://" + str(PAGE)
PREFIX = "a2"

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
  const clone = document.body.cloneNode(true);
  clone.querySelectorAll('code, pre, script, style, blockquote, td.defn, td.slug, span.defn').forEach(e => e.remove());
  document.body.appendChild(clone);
  const txt = clone.innerText;
  clone.remove();
  return {transform: [...new Set(tt)], text: txt};
}
"""
GEOM_JS = r"""
() => {
  const ids = [...document.querySelectorAll('section')].map(s => s.id);
  const firstInput = document.querySelector('#decisions input[type="radio"]');
  const r = firstInput.getBoundingClientRect();
  return {order: ids, pageH: document.documentElement.scrollHeight,
          firstAsk: Math.round(r.top + window.scrollY),
          d1: Math.round(document.querySelector('.dec[data-id="D-1"]').getBoundingClientRect().top + window.scrollY)};
}
"""
CARDS_JS = r"""
() => [...document.querySelectorAll('.dec')].map(d => ({
  id: d.dataset.id, title: d.querySelector('h3').innerText,
  opts: [...d.querySelectorAll('.opts label')].map(l => l.innerText),
  recs: d.querySelectorAll('.opts .rec').length,
  why: d.querySelector('.why') ? d.querySelector('.why').innerText : null,
  attrib: d.querySelector('.attrib') ? d.querySelector('.attrib').innerText : null,
  whyThenAttrib: !!(d.querySelector('.why') && d.querySelector('.why').nextElementSibling &&
                    d.querySelector('.why').nextElementSibling.classList.contains('attrib')),
  text: d.innerText}))
"""
SEL = [".label", ".decid", ".rec", ".stat b", ".stat span", ".said", "h3", "blockquote cite", ".tag", ".layers b"]
SCROLL_OK = ("div.tw", "pre.exp")
ACRONYM_OK = {"WCAG", "JSON", "HTML", "CSS", "KG", "UX", "HSBC", "SC", "URL", "API", "COGA", "ARIA", "APG",
              "EAA", "EU", "ICT", "W3C", "WAI", "CX", "AA", "ID", "IDS", "DESK", "JTBD", "DTCG", "ASK", "CLOSURE",
              "SHAPES", "TOKENS", "NEIGHBOURS", "PLACEHOLDER", "BLOCKING", "ADVISORY", "REVIEW", "TASTE", "NOT", "WIRED", "PROPOSAL"}
CAPS_RUN = re.compile(r"\b[A-Z][A-Z0-9]{3,}(?:[ \-][A-Z][A-Z0-9]{3,})*\b")


def main():
    rows, fails = [], []

    def check(name, ok, detail=""):
        rows.append((name, ok, detail))
        if not ok:
            fails.append(name)

    measured = json.loads(re.search(r'id="measured">(.*?)</script>', PAGE.read_text(encoding="utf-8"), re.S).group(1))

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        pg = b.new_page(viewport={"width": 1280, "height": 1400}, color_scheme="light")
        console, errors = [], []
        pg.on("console", lambda m: console.append((m.type, m.text)))
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(900)

        font = pg.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')")
        check("font loaded (HSBC_MtUnivers_Latin)", bool(font), str(font))
        bad = [c for c in console if c[0] in ("error", "warning")]
        check("0 console errors / warnings / page errors", not bad and not errors,
              f"{len(console)} console message(s), {len(bad)} bad, {len(errors)} page error(s) {bad[:2]}{errors[:2]}")

        probes = []
        for s in SEL:
            probes += pg.evaluate(DESC_JS, s)
        worst = max([r["clip"] for r in probes] or [0.0])
        check("descenders intact on the tight boxes", worst == 0.0,
              f"{len(probes)} element(s) across {len(SEL)} selectors · worst clip {worst:.2f}px"
              + (" · " + json.dumps(sorted(probes, key=lambda r: -r["clip"])[0]) if worst else ""))
        of = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
        check("no element crops its own content", not of, json.dumps(of[:3]))
        caps = pg.evaluate(CAPS_JS)
        runs = sorted({m for m in CAPS_RUN.findall(caps["text"])
                       if not all(w in ACRONYM_OK for w in re.split(r"[ \-]", m))})
        check("no text-transform:uppercase (nam-002)", not caps["transform"], str(caps["transform"][:4]))
        check("no ALL-CAPS runs in visible prose (nam-002)", not runs, str(runs[:6]))

        g = pg.evaluate(GEOM_JS)
        ev = [i for i, s in enumerate(g["order"]) if s in ("evidence", "questions", "layers", "kinds", "gaps", "refuse")]
        di = g["order"].index("decisions")
        pct = 100.0 * g["firstAsk"] / g["pageH"]
        check("decisions come before every evidence section, first ask in the top quarter", di < min(ev) and pct < 25.0,
              f"sections {g['order']} · page {g['pageH']:,}px · first ask {g['firstAsk']:,}px = {pct:.1f}% · D-1 {g['d1']:,}px")

        cards = {c["id"]: c for c in pg.evaluate(CARDS_JS)}
        # A. six decisions, D-1 is the layers
        check("six decisions D-1..D-6, D-1 is the layers question",
              [c for c in cards] == [f"D-{i}" for i in range(1, 7)] and "layers" in cards["D-1"]["title"].lower(),
              " · ".join(f"{k}: {v['title'][:40]}" for k, v in cards.items()))
        # B. one Recommended per card (D-6 placeholder may have none)
        recs = {k: v["recs"] for k, v in cards.items()}
        d6_ok = recs["D-6"] in (0, 1)
        check("exactly one Recommended option on D-1..D-5; D-6 zero or one",
              all(recs[f"D-{i}"] == 1 for i in range(1, 6)) and d6_ok, json.dumps(recs))
        # C. hero states the two rates from the measured block
        hero = pg.inner_text("#headline").replace("\u00a0", " ")
        qa, qd = measured["q_answered"], measured["q_design"]
        check(f"the hero states the answer rate once ({qa} of 12) and the design-time rate ({qd} of 12)",
              f"{qa} of the 12" in hero and f"{qd} of 12" in hero and hero.count(f"{qa} of 12") == 1
              and hero.count(f"{qd} of 12") == 1,
              f"'{qa} of the 12' {f'{qa} of the 12' in hero} · '{qd} of 12' {f'{qd} of 12' in hero}")
        # D. D-1 names the rulings it touches
        d1 = cards["D-1"]["text"]
        need = ["s274-D11", "s275-D6", "s275-D4"]
        check("D-1 names the rulings a re-layering touches, by id", all(x in d1 for x in need),
              " · ".join(f"{x} {x in d1}" for x in need))
        # D-2 states the BLOCKING figure from the measured block
        d2 = cards["D-2"]["text"]
        bu, bl = measured["blocking_unbound"], measured["blocking"]
        check(f"D-2 carries the measured BLOCKING figure ({bu} of {bl})", f"{bu} of the {bl}" in d2 or f"{bu} of {bl}" in d2,
              f"present {f'{bu} of the {bl}' in d2}")
        # E. Dave's words once, verbatim, cited
        bq = pg.evaluate("() => [...document.querySelectorAll('blockquote')].map(b => ({t: b.innerText, c: b.querySelector('cite') ? b.querySelector('cite').innerText : ''}))")
        verb = "all the accessibility nodes should be design governance nodes"
        check("Dave's words appear once, verbatim, in a cited blockquote",
              len(bq) == 1 and verb in bq[0]["t"] and "Dave" in bq[0]["c"] and "corrcet" in bq[0]["t"],
              f"{len(bq)} blockquote(s) · cite '{bq[0]['c'] if bq else ''}'")
        unattributed = [c["id"] for c in cards.values() if not c["whyThenAttrib"] or not re.search(r"lane A[23]", c["attrib"] or "", re.I)]
        check("every recommendation is followed, in the card, by the lane that wrote it", not unattributed,
              f"unattributed: {unattributed}" if unattributed else "all six attributed")

        # export + localStorage round-trip
        pg.click("#D-1-a")
        pg.fill('textarea.note[data-id="D-3"]', "a note that must survive a reload")
        pg.click("#btnExport")
        pg.wait_for_timeout(400)
        exp = json.loads(pg.inner_text("#exp"))
        shape_ok = (set(exp) == {"page", "at", "decisions"} and exp["page"] == PAGE.name
                    and [set(x) for x in exp["decisions"]] == [{"id", "choice", "note"}] * 6
                    and [x["id"] for x in exp["decisions"]] == [f"D-{i}" for i in range(1, 7)]
                    and exp["decisions"][0]["choice"] == "a"
                    and exp["decisions"][2]["note"] == "a note that must survive a reload")
        check("export is the RK shape (page, at, decisions[6]{id, choice, note})", shape_ok,
              json.dumps(exp["page"]) + " · " + json.dumps(exp["decisions"][:1]))
        pg.reload()
        pg.wait_for_timeout(500)
        back = pg.evaluate("""() => ({a: document.querySelector('#D-1-a').checked,
          n: document.querySelector('textarea.note[data-id="D-3"]').value,
          said: document.getElementById('said').textContent})""")
        check("localStorage round-trips the choice and the note across a reload",
              back["a"] is True and back["n"] == "a note that must survive a reload" and back["said"].startswith("1 of 6"),
              json.dumps(back))
        # A FRESH CONTEXT for the screenshots: the page saves its state on beforeunload, so a
        # localStorage.clear() followed by a reload writes the driver's own click straight back
        # (lane RIV's AMBER on RI's page: driver residue in the shipped PNGs). New context = empty store.
        pg.evaluate("() => localStorage.clear()")
        pg.close()
        ctx = b.new_context(viewport={"width": 1280, "height": 1400}, color_scheme="light")
        pg = ctx.new_page()
        pg.goto(URL)
        pg.wait_for_timeout(500)
        residue = pg.evaluate("() => [...document.querySelectorAll('input[type=radio]')].filter(i => i.checked).length")
        check("screenshots are taken from a fresh context: no radio checked, no note", residue == 0, f"{residue} checked")

        for theme in ("light", "dark"):
            pg.emulate_media(color_scheme=theme)
            pg.set_viewport_size({"width": 390, "height": 900})
            pg.reload()
            pg.wait_for_timeout(600)
            m = pg.evaluate("() => ({s: document.documentElement.scrollWidth, c: document.documentElement.clientWidth})")
            of3 = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
            check(f"390px {theme}: no horizontal scroll, nothing cropped", m["s"] <= m["c"] and not of3,
                  json.dumps(m) + f" · {len(of3)} overflowing")
            pg.screenshot(path=str(LANE / f"{PREFIX}-390-{theme}.png"), full_page=True)

        pg.set_viewport_size({"width": 1280, "height": 1400})
        for theme, want in (("light", "rgb(218, 26, 0)"), ("dark", "rgb(246, 96, 76)")):
            pg.emulate_media(color_scheme=theme)
            pg.reload()
            pg.wait_for_timeout(700)
            got = pg.evaluate("() => getComputedStyle(document.querySelector('.label')).color")
            probes2 = []
            for s in SEL:
                probes2 += pg.evaluate(DESC_JS, s)
            w2 = max([r["clip"] for r in probes2] or [0.0])
            of2 = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
            check(f"{theme}: accent is the two-red law value, 0 crop, 0 overflow (s151-D1)",
                  got == want and w2 == 0.0 and not of2, f"accent {got} (want {want}) · worst clip {w2:.2f}px · {len(of2)} overflowing")
            pg.screenshot(path=str(LANE / f"{PREFIX}-{theme}-1280.png"), full_page=True)
            pg.evaluate("() => document.querySelector('#decisions').scrollIntoView()")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(LANE / f"{PREFIX}-decisions-{theme}.png"))
        b.close()

    w = max(len(r[0]) for r in rows)
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{w}s}  {detail}")
    for p_ in sorted(LANE.glob(f"{PREFIX}-*.png")):
        print(f"  shot  {p_.name} ({p_.stat().st_size:,} bytes)")
    print("DRIVE PASS" if not fails else f"DRIVE FAIL — {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
