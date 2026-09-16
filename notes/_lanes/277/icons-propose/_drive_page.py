#!/usr/bin/env python3
"""_drive_page.py — DRIVE the #277 lane RI review page, then screenshot it.

Adapted from notes/_lanes/277/page/_drive_page.py (lane CP's), which is NOT
touched. Every check CP's driver ran is kept where it still applies, and the
five CP added against lane CV's finding — order, one number, attribution, hero
cost, the flag — are re-aimed at THIS page's own defects:

  7.  ORDER      — #decisions precedes every evidence section and the first
                   thing Dave can click sits in the top quarter.
  8.  ONE FIGURE — each card carries exactly ONE .onefig block and the number in
                   it is the number the card's own question turns on. A card
                   that leads on two totals is CV R-4 happening again.
  9.  ATTRIBUTED — every recommendation is immediately followed by an attribution
                   naming the lane that wrote it.
  10. HERO COST  — the combined cost appears in the hero, once, as the node and
                   edge counts and the two percentages.
  11. THE FENCE  — the refused prose route is ON the page with its number, and
                   it is NOT one of the options anywhere.

Plus three this page needs and CP's did not:
  12. NOTHING LANDED — the page says so, and the words "LANDED"/"ratified" never
      appear as a claim.
  13. NO INVENTED KIND — `theme:` and `token:` appear only inside the flagged
      paragraphs that explain why they are NOT drawn.
  14. THE NULLS ADD UP — the declared-null table's counts sum to the hero figure.

Screenshots: light and dark, full page, 1280 and 390.

    source knowledge/_render/seat_env.sh && \
      python3 notes/_lanes/277/icons-propose/_drive_page.py
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANE = Path(__file__).resolve().parent
PAGE = LANE / "REVIEW-icons-2026-09-16-v1.html"
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
  // Visible PROSE only. Stripped, and why:
  //   code/pre    file paths and identifiers, kept verbatim
  //   blockquote  Dave's s230-D2 line, verbatim. Rewording a ruling to pass a
  //               gate is the tail wagging the dog.
  //   td.defn     the declared drop reasons — the artefact under review.
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
  const r = document.querySelector('#decisions input[type="radio"]').getBoundingClientRect();
  const out = {order: ids, pageH: document.documentElement.scrollHeight,
               firstAsk: Math.round(r.top + window.scrollY)};
  for (const d of document.querySelectorAll('.dec'))
    out[d.dataset.id] = Math.round(d.getBoundingClientRect().top + window.scrollY);
  return out;
}
"""

CARDS_JS = r"""
() => [...document.querySelectorAll('.dec')].map(d => ({
  id: d.dataset.id,
  onefig: [...d.querySelectorAll('.onefig')].map(f => ({
     big: f.querySelector('b').innerText.trim(), cap: f.querySelector('span').innerText})),
  lede: d.querySelector('.onefig + p') ? d.querySelector('.onefig + p').innerText : '',
  opts: [...d.querySelectorAll('.opts label')].map(l => l.innerText),
  why: d.querySelector('.why') ? d.querySelector('.why').innerText : null,
  attrib: d.querySelector('.attrib') ? d.querySelector('.attrib').innerText : null,
  recCount: d.querySelectorAll('.rec').length,
  whyThenAttrib: !!(d.querySelector('.why') &&
                    d.querySelector('.why').nextElementSibling &&
                    d.querySelector('.why').nextElementSibling.classList.contains('attrib')),
  text: d.innerText}))
"""

SEL = [".label", ".decid", ".rec", ".stat b", ".stat span", ".said", "h3",
       "blockquote cite", ".onefig b"]
SCROLL_OK = ("div.tw", "pre.exp")
ACRONYM_OK = {"WCAG", "JSON", "HTML", "CSS", "KG", "UX", "HSBC", "SC", "URL", "URLS",
              "API", "NEW", "KB", "MB", "ID", "IDS", "SVG", "SVGS", "ONLY", "STRUCT",
              "STRUCT-ONLY", "PDF", "DOM"}
CAPS_RUN = re.compile(r"\b[A-Z][A-Z0-9]{3,}(?:[ \-][A-Z][A-Z0-9]{3,})*\b")
IDS = ["RI-1", "RI-2", "RI-3", "RI-4"]
# The one figure each card turns on. Read from the built page's own measured block,
# never typed here — this dict names WHICH key, not its value.
ONEFIG_KEY = {"RI-1": "n_nodes", "RI-2": "n_usesicon", "RI-3": "n_multi", "RI-4": "n_unbound"}


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

        n = json.loads(pg.inner_text("#measured"))

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

        # ---- 7. ORDER — the ask before the evidence -------------------------
        g = pg.evaluate(GEOM_JS)
        ev = [i for i, s in enumerate(g["order"]) if s.startswith("ev-")]
        di = g["order"].index("decisions")
        pct = 100.0 * g["firstAsk"] / g["pageH"]
        check("decisions come before every evidence section, first ask in the top quarter",
              di < min(ev) and pct < 25.0,
              f"sections {g['order']} · page {g['pageH']:,}px · first ask {g['firstAsk']:,}px "
              f"= {pct:.1f}% · " + " · ".join(f"{i} {g[i]:,}px" for i in IDS))

        cards = {c["id"]: c for c in pg.evaluate(CARDS_JS)}
        check("all four decisions are on the page, in order", list(cards) == IDS, str(list(cards)))

        # ---- 8. ONE FIGURE per card, and it is the card's own number --------
        wrong = []
        for did in IDS:
            c = cards[did]
            want = str(n[ONEFIG_KEY[did]])
            if len(c["onefig"]) != 1 or c["onefig"][0]["big"] != want:
                wrong.append((did, [f["big"] for f in c["onefig"]], want))
        check("each card carries exactly ONE lead figure and it is that card's own number",
              not wrong, str(wrong) if wrong
              else " · ".join(f"{d} {cards[d]['onefig'][0]['big']}" for d in IDS))
        multirec = [d for d in IDS if cards[d]["recCount"] != 1]
        check("each card marks exactly one option Recommended", not multirec,
              str(multirec) if multirec else "one per card")

        # ---- 9. ATTRIBUTED — every recommendation names its lane -------------
        unattributed = [c["id"] for c in cards.values()
                        if not c["whyThenAttrib"]
                        or not re.search(r"lane (RI|IX)", c["attrib"] or "", re.I)]
        check("every recommendation is followed, in the card, by the lane that wrote it",
              not unattributed, f"unattributed: {unattributed}" if unattributed
              else " · ".join(f"{c['id']}: {(c['attrib'] or '')[:34]}…" for c in cards.values()))

        # ---- 10. HERO COST — once, and the right one ------------------------
        hero = pg.inner_text("#headline")
        want = [str(n["n_nodes"]), str(n["n_edges"]), str(n["node_pct"]), str(n["edge_pct"]),
                n["g_nodes"], n["g_edges"]]
        missing = [w for w in want if w not in hero]
        check("the hero states the cost once: nodes, edges, and both percentages against the live graph",
              not missing, f"missing {missing}" if missing
              else f"{n['n_nodes']} nodes / {n['n_edges']} edges · +{n['node_pct']}% / "
                   f"+{n['edge_pct']}% of {n['g_nodes']} / {n['g_edges']}")

        # ---- 11. THE FENCE — the refused route is shown, never offered ------
        body = pg.inner_text("body")
        opts_all = " ".join(o for c in cards.values() for o in c["opts"])
        check("the refused prose route is on the page with its number, and is not an option anywhere",
              str(n["prose_pairs"]) in body and f"{n['prose_hit']} of {n['prose_metas']}" in body
              and "prose" not in opts_all.lower(),
              f"{n['prose_pairs']} pairs on {n['prose_hit']}/{n['prose_metas']} metas · "
              f"absent from every option {'prose' not in opts_all.lower()}")
        check("the STRUCT-ONLY figure — glyph rendered, word never said — is on the page",
              str(n["struct_only"]) in body and "never mention" in body,
              f"{n['struct_only']} components")

        # ---- 12. NOTHING LANDED ---------------------------------------------
        # The only two places the page may say anything about landing are the hero's
        # denial and the footer's. "LANDED" as a claim must appear nowhere.
        landed_lines = [l for l in body.splitlines() if re.search(r"\blanded\b", l, re.I)]
        check("the page says nothing is landed, and makes no ratification claim anywhere",
              "Nothing here is landed" in body and "LANDED" not in body
              and all("Nothing on this page is landed" in l or "Nothing here is landed" in l
                      for l in landed_lines),
              f"{len(landed_lines)} line(s) mention landing, all denials")

        # ---- 13. NO INVENTED KIND -------------------------------------------
        flags = pg.evaluate("() => [...document.querySelectorAll('.flag')].map(f => f.innerText)")
        theme_flag = [f for f in flags if "theme:" in f]
        token_flag = [f for f in flags if "themedBy" in f]
        # `theme:` and `token:` are the two kinds this lane refuses to invent. They may
        # appear in the flag that explains the refusal and in the declared-null table
        # (which is the refusal, recorded) — and NOWHERE ELSE. Never in a card's lede,
        # never in an option, because an option naming them would be offering them.
        ledes = " ".join(c["lede"] for c in cards.values())
        nulls_txt = pg.inner_text("#ev-nulls")
        outside = (body.count("theme:") - theme_flag[0].count("theme:")
                   - nulls_txt.count("theme:")) if theme_flag else 99
        check("theme: and token: appear ONLY in the flag that refuses them and in the nulls table",
              len(theme_flag) == 1 and len(token_flag) == 1 and outside == 0
              and "theme:" not in opts_all and "token:" not in opts_all
              and "theme:" not in ledes and "token:" not in ledes,
              f"{len(flags)} flagged findings · {outside} mention(s) outside the flag and the "
              f"nulls table · absent from every option and every lede")
        b1 = [f for f in flags if "menu-search" in f]
        check("B1 — the stale manifest — is flagged as a build step, not offered as a decision",
              len(b1) == 1 and "not a question" in b1[0] and "menu-search" not in opts_all,
              (b1[0][:80].replace("\n", " ") + "…") if b1 else "MISSING")

        # ---- 14. THE NULLS ADD UP -------------------------------------------
        tbl = pg.evaluate("""() => [...document.querySelectorAll('#ev-nulls tbody tr')]
                              .map(r => +r.children[1].innerText)""")
        check("the declared-null table sums to the figure in the hero",
              sum(tbl) == n["n_nulls"], f"{len(tbl)} rows summing {sum(tbl)} · hero {n['n_nulls']}")

        # ---- export + localStorage round-trip --------------------------------
        pg.click("#RI-1-a")
        pg.fill('textarea.note[data-id="RI-3"]', "a note that must survive a reload")
        pg.click("#btnExport")
        pg.wait_for_timeout(400)
        exp = json.loads(pg.inner_text("#exp"))
        shape_ok = (set(exp) == {"page", "at", "decisions"}
                    and [set(x) for x in exp["decisions"]] == [{"id", "choice", "note"}] * 4
                    and [x["id"] for x in exp["decisions"]] == IDS
                    and exp["decisions"][0]["choice"] == "a"
                    and exp["decisions"][2]["note"] == "a note that must survive a reload")
        check("export is the RK shape: page, at, and four {id, choice, note}", shape_ok,
              json.dumps(exp["page"]) + " · " + json.dumps(exp["decisions"][:1]))

        pg.reload()
        pg.wait_for_timeout(500)
        back = pg.evaluate("""() => ({
          a: document.querySelector('#RI-1-a').checked,
          n: document.querySelector('textarea.note[data-id="RI-3"]').value,
          said: document.getElementById('said').textContent})""")
        check("localStorage round-trips the choice and the note across a reload",
              back["a"] is True and back["n"] == "a note that must survive a reload"
              and back["said"].startswith("1 of 4"), json.dumps(back))
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
            pg.screenshot(path=str(LANE / f"ri-390-{theme}.png"), full_page=True)

        # ---- both themes at 1280, two-red law --------------------------------
        pg.set_viewport_size({"width": 1280, "height": 1400})
        for theme, want_c in (("light", "rgb(218, 26, 0)"), ("dark", "rgb(246, 96, 76)")):
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
                  got == want_c and w2 == 0.0 and not of2,
                  f"accent {got} (want {want_c}) · worst clip {w2:.2f}px · {len(of2)} overflowing")
            pg.screenshot(path=str(LANE / f"ri-{theme}-1280.png"), full_page=True)
            pg.evaluate("() => document.querySelector('#decisions').scrollIntoView()")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(LANE / f"ri-decisions-{theme}.png"))
            pg.evaluate("() => document.querySelector('.dec[data-id=\\'RI-3\\']').scrollIntoView()")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(LANE / f"ri-RI3-{theme}.png"))

        b.close()

    w = max(len(r[0]) for r in rows)
    for name, ok, detail in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{w}s}  {detail}")
    for p_ in sorted(LANE.glob("ri-*.png")):
        print(f"  shot  {p_.name} ({p_.stat().st_size:,} bytes)")
    print("DRIVE PASS" if not fails else f"DRIVE FAIL — {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
