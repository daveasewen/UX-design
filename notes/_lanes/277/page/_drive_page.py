#!/usr/bin/env python3
"""_drive_page.py — DRIVE the #277 lane CP review page (v2), then screenshot it.

Adapted from notes/_lanes/277/charts/_drive_page.py (lane CO's), which is NOT
touched. Every check CO's driver ran is kept, and five are added — because CO's
driver went ELEVEN-FOR-ELEVEN GREEN on a page that contradicted itself, which is
the whole finding of lane CV. A driver that cannot see the defect that shipped is
not a gate, so these five are written against that defect by name:

  7.  ORDER      — #decisions precedes every evidence section in the document,
                   and the first thing Dave can click sits in the top quarter of
                   the page. (CV R-6: v1's first decision was 64% down.)
  8.  ONE NUMBER — inside the D-3 card, every family total that appears is 47,
                   except where it is explicitly a named lane's own figure or the
                   declared 48-if-dv-013-stands. (CV R-4: v1's card carried
                   49/8/13 against 46/11/30.)
  9.  ATTRIBUTED — every recommendation paragraph in a card is immediately
                   followed by an attribution naming the lane that wrote it.
                   (CV R-4: the contradicting paragraph was unlabelled.)
  10. HERO COST  — the combined cost appears in the hero, once, as 76 and
                   81 -> 157. (CV A-8.)
  11. THE FLAG   — the 5-versus-6 conflict is on the page as its own line, names
                   the gate file, and is NOT one of the options. (CV item 7.)

Plus the six CO wrote: console, descenders (canvas probe on tight boxes), the
crop clause, nam-002 caps, export shape + localStorage round-trip, 390px, and
both themes at the two-red law values.

Screenshots: light and dark, full page, 1280 and 390.

    source knowledge/_render/seat_env.sh && \
      python3 notes/_lanes/277/page/_drive_page.py
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANE = Path(__file__).resolve().parent
PAGE = LANE / "REVIEW-charts-2026-09-15-v2.html"
URL = "file://" + str(PAGE)

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
  // Visible PROSE only — the page's OWN voice. Stripped, and why:
  //   code/pre   file paths and identifiers, kept verbatim
  //   blockquote s276-D5 quoted verbatim. Rewording a ruling to pass a gate is
  //              the tail wagging the dog.
  //   td.defn    the authored $why sentences and the declared drop reasons —
  //              the artefact under review, data on this page.
  const clone = document.body.cloneNode(true);
  clone.querySelectorAll('code, pre, script, style, blockquote, td.defn').forEach(e => e.remove());
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
  return {order: ids,
          pageH: document.documentElement.scrollHeight,
          firstAsk: Math.round(r.top + window.scrollY),
          d1: Math.round(document.querySelector('.dec[data-id="D-1"]').getBoundingClientRect().top + window.scrollY),
          d3: Math.round(document.querySelector('.dec[data-id="D-3"]').getBoundingClientRect().top + window.scrollY)};
}
"""

CARDS_JS = r"""
() => [...document.querySelectorAll('.dec')].map(d => ({
  id: d.dataset.id,
  lede: d.querySelector('p').innerText,
  opts: [...d.querySelectorAll('.opts label')].map(l => l.innerText),
  why: d.querySelector('.why') ? d.querySelector('.why').innerText : null,
  attrib: d.querySelector('.attrib') ? d.querySelector('.attrib').innerText : null,
  open: d.querySelector('.opencell') ? d.querySelector('.opencell').innerText : null,
  whyThenAttrib: !!(d.querySelector('.why') &&
                    d.querySelector('.why').nextElementSibling &&
                    d.querySelector('.why').nextElementSibling.classList.contains('attrib')),
  text: d.innerText}))
"""

SEL = [".label", ".decid", ".rec", ".stat b", ".stat span", ".said", "h3", "blockquote cite", ".tag"]
SCROLL_OK = ("div.tw", "pre.exp")
ACRONYM_OK = {"WCAG", "JSON", "HTML", "CSS", "KG", "UX", "HSBC", "SC", "URL", "URLS",
              "API", "COGA", "ARIA", "APG", "EAA", "EU", "ICT", "W3C", "WAI", "CX",
              "NEW", "AA", "PDF", "KB", "MB", "ID", "IDS"}
CAPS_RUN = re.compile(r"\b[A-Z][A-Z0-9]{3,}(?:[ \-][A-Z][A-Z0-9]{3,})*\b")
# The four figures that have ever been offered as "the family total". Only one of
# them may be presented as THIS page's answer.
RIVALS = ("46", "47", "48", "49")


def main():
    rows, fails = [], []

    def check(name, ok, detail=""):
        rows.append((name, ok, detail))
        if not ok:
            fails.append(name)

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
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
              f"{len(console)} console message(s), {len(bad)} bad, {len(errors)} page error(s) "
              f"{bad[:2]}{errors[:2]}")

        probes = []
        for s in SEL:
            probes += pg.evaluate(DESC_JS, s)
        worst = max([r["clip"] for r in probes] or [0.0])
        check("descenders intact on the tight boxes (the _validate_demo_page clause)", worst == 0.0,
              f"{len(probes)} element(s) across {len(SEL)} selectors · worst clip {worst:.2f}px"
              + (" · " + json.dumps(sorted(probes, key=lambda r: -r["clip"])[0]) if worst else ""))

        of = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
        check("no element crops its own content (overflow != visible and overflowing)", not of,
              json.dumps(of[:3]))

        caps = pg.evaluate(CAPS_JS)
        runs = sorted({m for m in CAPS_RUN.findall(caps["text"]) if m not in ACRONYM_OK})
        check("no text-transform:uppercase (nam-002)", not caps["transform"],
              str(caps["transform"][:4]))
        check("no ALL-CAPS runs in visible text (nam-002)", not runs, str(runs[:6]))

        # ---- 7. ORDER — the ask before the evidence (CV R-6) ------------------
        g = pg.evaluate(GEOM_JS)
        ev = [i for i, s in enumerate(g["order"]) if s in ("parta", "family", "q3", "evidence")]
        di = g["order"].index("decisions")
        pct = 100.0 * g["firstAsk"] / g["pageH"]
        check("decisions come before every evidence section, first ask in the top quarter",
              di < min(ev) and pct < 25.0,
              f"sections {g['order']} · page {g['pageH']:,}px · first ask {g['firstAsk']:,}px "
              f"= {pct:.1f}% · D-1 {g['d1']:,}px · D-3 {g['d3']:,}px")

        # ---- 8. ONE NUMBER — no card answers its own question twice (CV R-4) --
        cards = {c["id"]: c for c in pg.evaluate(CARDS_JS)}
        d3 = cards["D-3"]
        lede_rivals = sorted({r for r in RIVALS if r in d3["lede"]})
        optb = [o for o in d3["opts"] if o.startswith("(b)")][0]
        opt_rivals = sorted({r for r in RIVALS if r in optb})
        opta = [o for o in d3["opts"] if o.startswith("(a)")][0]
        # the "false cells" figure must be 57 - 47 = 10, not v1's 8 or CJ's 11
        false_ok = (" 10 " in opta or " 10 of" in opta) and "11 of" not in opta
        check("D-3 states one family total, and it is 47",
              lede_rivals == ["47"] and opt_rivals == ["47"] and false_ok,
              f"lede rivals {lede_rivals} · option (b) rivals {opt_rivals} · "
              f"option (a) false-cell figure ok={false_ok}")
        check("D-3's open cell is named as open, and both outcomes are priced",
              d3["open"] is not None and "dv-013" in d3["open"]
              and "47" in d3["open"] and "48" in d3["open"],
              (d3["open"] or "")[:90].replace("\n", " "))
        # and the contradiction CV R-5 named: "at most one" vs "none of the three"
        check("D-3 carries no at-most-one / none-of-the-three contradiction (CV R-5)",
              "at most one" not in d3["text"] and "none of the three" not in d3["text"],
              "neither phrase present")

        # ---- 9. ATTRIBUTED — every recommendation names its lane (CV R-4) -----
        unattributed = [c["id"] for c in cards.values()
                        if not c["whyThenAttrib"]
                        or not re.search(r"lane C[A-Z]", c["attrib"] or "", re.I)]
        check("every recommendation is followed, in the card, by the lane that wrote it",
              not unattributed, f"unattributed: {unattributed}" if unattributed
              else " · ".join(f"{c['id']}: {(c['attrib'] or '')[:38]}…" for c in cards.values()))

        # ---- 10. HERO COST — once, and the right one (CV A-8) ----------------
        hero = pg.inner_text("#headline")
        check("the hero states the combined cost once: 76 edges, 81 -> 157",
              "76" in hero and "81" in hero and "157" in hero and "110" not in hero,
              f"76 {'76' in hero} · 81->157 {'157' in hero} · v1's 110 absent "
              f"{'110' not in hero}")

        # ---- 11. THE FLAG — surfaced, not resolved, not an option ------------
        flags = pg.evaluate("() => [...document.querySelectorAll('.flag')].map(f => f.innerText)")
        cap = [f for f in flags if "dv-pie-009" in f]
        opts_all = " ".join(o for c in cards.values() for o in c["opts"])
        check("the 5-versus-6 cap conflict is its own flagged line, names the gate, is not an option",
              len(cap) == 1 and "_validate_dataviz.py" in cap[0] and "5 parts" in cap[0]
              and "dv-pie-009" not in opts_all,
              f"{len(flags)} flagged finding(s) · gate named {'_validate_dataviz.py' in (cap[0] if cap else '')} "
              f"· absent from every option {'dv-pie-009' not in opts_all}")
        check("D-2 says that (b) strands dv-pie-003",
              "dv-pie-003" in [o for o in cards["D-2"]["opts"] if o.startswith("(b)")][0],
              "named in option (b)")
        check("D-1's options are exclusive (land now / land after a read)",
              "Land now" in cards["D-1"]["opts"][0]
              and "Land after a per-component read" in cards["D-1"]["opts"][1],
              cards["D-1"]["opts"][0][:34] + " | " + cards["D-1"]["opts"][1][:38])

        # ---- export + localStorage round-trip --------------------------------
        pg.click("#D-1-a")
        pg.fill('textarea.note[data-id="D-3"]', "a note that must survive a reload")
        pg.click("#btnExport")
        pg.wait_for_timeout(400)
        exp = json.loads(pg.inner_text("#exp"))
        shape_ok = (set(exp) == {"page", "at", "decisions"}
                    and exp["page"] == PAGE.name and exp["page"].endswith(".html")
                    and [set(x) for x in exp["decisions"]] == [{"id", "choice", "note"}] * 3
                    and [x["id"] for x in exp["decisions"]] == [f"D-{i}" for i in range(1, 4)]
                    and exp["decisions"][0]["choice"] == "a"
                    and exp["decisions"][2]["note"] == "a note that must survive a reload")
        check("export is the RK shape, and page carries its .html", shape_ok,
              json.dumps(exp["page"]) + " · " + json.dumps(exp["decisions"][:1]))

        pg.reload()
        pg.wait_for_timeout(500)
        back = pg.evaluate("""() => ({
          a: document.querySelector('#D-1-a').checked,
          n: document.querySelector('textarea.note[data-id="D-3"]').value,
          said: document.getElementById('said').textContent})""")
        check("localStorage round-trips the choice and the note across a reload",
              back["a"] is True and back["n"] == "a note that must survive a reload"
              and back["said"].startswith("1 of 3"), json.dumps(back))

        pg.evaluate("() => localStorage.clear()")

        # ---- 390px, both themes ---------------------------------------------
        for theme in ("light", "dark"):
            pg.emulate_media(color_scheme=theme)
            pg.set_viewport_size({"width": 390, "height": 900})
            pg.reload()
            pg.wait_for_timeout(600)
            m = pg.evaluate("() => ({s: document.documentElement.scrollWidth, "
                            "c: document.documentElement.clientWidth})")
            of3 = [o for o in pg.evaluate(OVERFLOW_JS) if o["sel"] not in SCROLL_OK]
            check(f"390px {theme}: no horizontal scroll, nothing cropped",
                  m["s"] <= m["c"] and not of3, json.dumps(m) + f" · {len(of3)} overflowing")
            pg.screenshot(path=str(LANE / f"v2-390-{theme}.png"), full_page=True)

        # ---- both themes at 1280, two-red law --------------------------------
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
                  got == want and w2 == 0.0 and not of2,
                  f"accent {got} (want {want}) · worst clip {w2:.2f}px · {len(of2)} overflowing")
            pg.screenshot(path=str(LANE / f"v2-{theme}-1280.png"), full_page=True)
            pg.evaluate("() => document.querySelector('#decisions').scrollIntoView()")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(LANE / f"v2-decisions-{theme}.png"))

        b.close()

    w = max(len(r[0]) for r in rows)
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{w}s}  {detail}")
    for p_ in sorted(LANE.glob("v2-*.png")):
        print(f"  shot  {p_.name} ({p_.stat().st_size:,} bytes)")
    print("DRIVE PASS" if not fails else f"DRIVE FAIL — {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
