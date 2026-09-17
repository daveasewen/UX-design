#!/usr/bin/env python3
"""#281 lane RO — drive RESTS-ON-2026-09-17.html at 1280 and 390.

Proves, at both widths: 59 cards, 222 radios, no page error, no horizontal
overflow, "Take all the recommendations" sets exactly 59 radios and produces the
export envelope with 59 answers, every answer's uxId agreeing with
proposals.json, overruled false everywhere on the take-all, and a hand-overrule
flipping exactly one row to overruled true with the typed principle carried.

Usage:
  source knowledge/_render/seat_env.sh && \
    python3 notes/_lanes/281/rests-on/verify_rests_on.py
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

REPO = pathlib.Path(__file__).resolve().parents[4]
DIR = REPO / "notes" / "_lanes" / "281" / "rests-on"
PAGE = DIR / "RESTS-ON-2026-09-17.html"
PROPS = json.loads((DIR / "proposals.json").read_text())["proposals"]

EXPECT_CARDS = 59
EXPECT_RADIOS = sum(len(p["options"]) + 2 for p in PROPS)
REC = {p["ruleId"]: p["recommend"] for p in PROPS}
RECUX = {p["ruleId"]: next((o["uxId"] for o in p["options"] if o["recommended"]), None)
         for p in PROPS}

fails = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


def run(pw, w, h):
    print("\n=== %dx%d ===" % (w, h))
    b = pw.chromium.launch(executable_path=SHELL, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": w, "height": h})
    errs = []
    pg.on("pageerror", lambda x: errs.append(str(x)))
    pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
    pg.goto(PAGE.as_uri())
    pg.wait_for_timeout(300)

    check(pg.eval_on_selector_all(".card", "e=>e.length") == EXPECT_CARDS,
          "cards = %d" % EXPECT_CARDS)
    check(pg.eval_on_selector_all("input[type=radio]", "e=>e.length") == EXPECT_RADIOS,
          "radios = %d" % EXPECT_RADIOS)
    names = pg.evaluate("[...new Set([...document.querySelectorAll('input[type=radio]')].map(e=>e.name))]")
    check(sorted(names) == sorted(REC), "one radio group per rule id, 59 distinct")

    ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(ov <= 0, "no horizontal overflow (scrollWidth-clientWidth = %d)" % ov)

    # take all the recommendations
    pg.click("#takeall")
    pg.wait_for_timeout(200)
    checked = pg.eval_on_selector_all("input[type=radio]:checked", "e=>e.length")
    check(checked == EXPECT_CARDS, "take-all checks exactly 59 radios (got %d)" % checked)
    env = json.loads(pg.inner_text("#exp"))
    check(env["page"] == "RESTS-ON-2026-09-17", "envelope page")
    check(set(env) == {"exportedAt", "page", "answers"}, "envelope keys exportedAt/page/answers")
    check(len(env["answers"]) == EXPECT_CARDS, "59 answers")
    bad = [r for r, a in env["answers"].items()
           if a["choice"] != REC[r] or a["recommended"] != REC[r] or a["overruled"]]
    check(not bad, "every answer is the recommendation, overruled false (%d bad)" % len(bad))
    badux = [r for r, a in env["answers"].items() if a["uxId"] != RECUX[r]]
    check(not badux, "every uxId matches proposals.json (%d bad: %s)" % (len(badux), badux[:3]))
    check(all(a["note"] == "" for a in env["answers"].values()), "notes empty by default")

    # overrule one, type a principle, add a note
    rid = "dv-pie-009"
    pg.check('input[name="%s"][value="d"]' % rid)
    pg.fill("#other-%s" % rid, "pr-hick")
    pg.fill("#note-%s" % rid, "six is arbitrary, say why six")
    pg.wait_for_timeout(200)
    env2 = json.loads(pg.inner_text("#exp"))
    a = env2["answers"][rid]
    check(a["choice"] == "d" and a["overruled"] is True and a["uxId"] == "pr-hick"
          and a["note"] == "six is arbitrary, say why six",
          "overrule round-trips: choice d, uxId pr-hick, note verbatim, overruled true")
    others = [r for r, x in env2["answers"].items() if x["overruled"] and r != rid]
    check(not others, "exactly one row overruled")
    check(pg.eval_on_selector_all("input[type=radio]:checked", "e=>e.length") == EXPECT_CARDS,
          "still 59 checked after the overrule")

    check(errs == [], "page errors [] (got %s)" % errs)
    pg.screenshot(path=str(DIR / ("verify-%d.png" % w)), full_page=False)
    b.close()


with sync_playwright() as pw:
    import glob
    import os
    SHELL = os.environ.get("RENDER_SHELL") or glob.glob(
        str(REPO / "outputs/_render-env-229/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell"))[0]
    run(pw, 1280, 900)
    run(pw, 390, 844)

print("\nVERDICT:", "GREEN" if not fails else "RED %d" % len(fails))
sys.exit(1 if fails else 0)
