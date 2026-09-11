#!/usr/bin/env python3
"""_validate_demo_page.py — drive THE DEMO PAGE from the STAGED PACK, before the pin.

WHY THIS GATE EXISTS — v1.0.11 AND v1.0.12 BOTH SLIPPED THE SAME WAY
--------------------------------------------------------------------
Two releases in a row shipped a sidebar whose nav labels clip their descenders
("Pavments", "Liauiditv", "Settinas"), and in both cases every release gate was green
when the zip was pinned. Cold run 7 read the crop off the released v1.0.11 zip; the fix
went in at cause; cold run 8 then read the SAME crop off the released v1.0.12 zip,
because the fix had been mutation-tested against a page built to contain the fix — a
fixture carrying `.canon` and `.cn-sidebar-nav` and nothing else — while the page the
finding came from wears `cn-template-dashboard-bento`, which carries its own private
copy of the leading-trim default and outranks the ds-005 override two scopes away.

  [[conflated-fix-guarantees-recurrence]] — the fix was tested against a page built to
  contain the fix, not against the page the finding came from.
  [[no-gate-parses-the-artefact]] — nine release gates parsed the manifest, the file
  list and the version literals; not one opened the pack and LOOKED at the demo.

⇒ This gate opens the pack and looks at the demo. It is the consumer for a measurement
nothing was consuming [[instrument-without-a-consumer]].

WHAT IT DRIVES, AND WHY THAT PAGE
---------------------------------
The run-of-show (`notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html`, plot point 09 —
"The page lands. Drive it.") opens the generated dashboard, light theme, and the
operator's recovery arm for the same plot point names the artefact this repo actually
holds: `outputs/coldrun-267/arm-A-blind/dashboard.html`. That is a REAL generated page,
not a fixture: it is what a blind cold run produced from the frozen prompt, and it is
what Dave drives if the live build overruns. So it is the page this gate loads.

The page is staged with `canon/canon.css` and `canon/type.css` REPLACED BY THE PACK'S —
the whole question is whether the CSS that is about to ship renders that page correctly,
so the CSS must come out of the zip and nothing else may.

  ⛔ `file://` IS NOT USED. The page is served over http from the stage, because the
  arm's own scripts fetch beside themselves and a `file://` origin silently starves them
  (knowledge/_RUNBOOK-render-verify.md). `page.set_content()` is BANNED for the same
  class of reason — it drops linked stylesheets.

FOUR THEMES, THREE QUESTIONS EACH — ALL TWELVE MUST BE GREEN
------------------------------------------------------------
  1. DESCENDERS   every `.nv-label` computes `text-box-edge: text` and clips 0.00px.
                  Measured off the canvas metrics against the element's own clientHeight,
                  which is the same arithmetic cold runs 7 and 8 used, so a verdict here
                  is comparable with theirs term for term.
  2. NAV STYLED   `a.nv-item` is matched by canon rules, is not `display:inline`, has
                  padding, carries no underline, and stands at least 24px tall (s262-D2).
  3. DROPDOWNS    both toolbar dropdowns report `aria-expanded=true` after a click.
                  ⚠ DECLARED SOFT: cold run 7 finding 1 established that the ARM's own
                  script sets `aria-expanded` and not `data-open`, so the menu paints at
                  `opacity:0` and `is_visible()` cannot see that. That is the arm's
                  defect, not the pack's; this arm therefore asserts the attribute only
                  and SAYS SO, rather than claiming a green it has not earned.

POSTURE
-------
  BLOCKING when playwright is importable — a red is a red and the bake must stop.
  COULD-NOT-ASK (exit 77) when playwright, the browser or the page is absent. 77 is not
  a pass and not a failure; the survey counts it as a third verdict
  [[gate-cannot-pass-in-one-environment]].

⬛ DAVE'S — no ruling is claimed for this gate. It enacts an existing obligation
(ds-005, the descender clause, and s262-D2's 24px floor) against a new SURFACE. Whether
driving the demo page should become a standing pre-bake step of the release runbook is
his word; until then this file is the instrument and the runbook step is the habit.

Usage:
  python3 knowledge/_validate_demo_page.py --zip <pack.zip>
  python3 knowledge/_validate_demo_page.py --zip <pack.zip> --page <dashboard.html>
  python3 knowledge/_validate_demo_page.py --stage <unzipped pack dir>
  python3 knowledge/_validate_demo_page.py --json <out.json>     # bank the measurement
  python3 knowledge/_validate_demo_page.py --bite <zip>          # MUTATION ARM: re-inject
                                                                 # the pre-fix cascade and
                                                                 # require a RED
  python3 knowledge/_validate_demo_page.py --selftest

Environment (all overridable; the defaults are the runbook's):
  PLAYWRIGHT_BROWSERS_PATH, LD_LIBRARY_PATH, TMPDIR, FONTCONFIG_FILE
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse, functools, glob, http.server, json, os, shutil, socketserver
import sys, tempfile, threading, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _could_not_ask as cna  # noqa: E402 - after the path insert, by necessity

SCRATCH = os.environ.get("TMPDIR", "/var/tmp")
THEMES = ("mono", "legacy", "console", "supercharge")

# The page the run-of-show's plot point 09 drives. Named here in ONE place; a caller that
# wants a different page passes --page, and the report says which page was driven, so a
# verdict can never be read as being about a page it was not taken on.
DEMO_PAGE = os.path.join(REPO, "outputs", "coldrun-267", "arm-A-blind", "dashboard.html")

# The two files the pack must supply. Everything else in the stage comes from the page's
# own directory, untouched.
PACK_CSS = ("canon.css", "type.css")

# The measurement, in the page's own cascade. Identical arithmetic to cold runs 7 and 8:
# baseline + actualBoundingBoxDescent against the element's clientHeight.
DESC_JS = r"""
() => {
  const cvs = document.createElement('canvas'), ctx = cvs.getContext('2d');
  return [...document.querySelectorAll('.nv-label')].map(el => {
    const cs = getComputedStyle(el);
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    const t = (el.textContent || '').trim();
    const m = ctx.measureText(t + 'gypq');
    const fA = m.fontBoundingBoxAscent, fD = m.fontBoundingBoxDescent;
    const aD = m.actualBoundingBoxDescent;
    const lh = cs.lineHeight === 'normal' ? (fA + fD) : parseFloat(cs.lineHeight);
    const ch = el.clientHeight, baseline = (lh - (fA + fD)) / 2 + fA;
    return {text: t, edge: cs.textBoxEdge || cs['text-box-edge'] || '',
            boxH: +ch.toFixed(2), clip: +Math.max(0, (baseline + aD) - ch).toFixed(2)};
  });
}
"""

NAV_JS = r"""
() => {
  const el = document.querySelector('a.nv-item');
  if (!el) return null;
  const c = getComputedStyle(el);
  let hit = 0;
  for (const s of document.styleSheets) {
    try { for (const r of s.cssRules) {
      if (r.selectorText && r.selectorText.includes('nv-item')) hit++;
    } } catch (e) {}
  }
  return {display: c.display, padding: c.padding,
          textDecorationLine: c.textDecorationLine,
          height: el.getBoundingClientRect().height, rules: hit};
}
"""


class Unreachable(Exception):
    """The INSTRUMENT is absent — not a verdict about the pack."""


# ---------------------------------------------------------------------------------------
# staging
# ---------------------------------------------------------------------------------------

def pack_css(zip_or_dir):
    """Return {name: bytes} for canon.css and type.css, read OUT OF THE PACK.

    A zip is read as a zip; a directory is read as an unzipped pack. Both are the pack —
    what may never happen is reading these two files out of the working tree, because the
    whole question this gate asks is about the bytes that are ABOUT to ship.
    """
    want = {}
    if os.path.isdir(zip_or_dir):
        for name in PACK_CSS:
            hits = glob.glob(os.path.join(zip_or_dir, "**", "canon", name), recursive=True)
            if not hits:
                raise Unreachable("the staged pack has no knowledge/canon/%s" % name)
            want[name] = open(sorted(hits, key=len)[0], "rb").read()
        return want
    if not os.path.exists(zip_or_dir):
        raise Unreachable("no pack at %s" % zip_or_dir)
    with zipfile.ZipFile(zip_or_dir) as z:
        names = z.namelist()
        for name in PACK_CSS:
            hits = [n for n in names if n.endswith("/canon/" + name)]
            if not hits:
                raise Unreachable("%s carries no knowledge/canon/%s"
                                  % (os.path.basename(zip_or_dir), name))
            want[name] = z.read(sorted(hits, key=len)[0])
    return want


def stage(page, css, root=None):
    """Copy the page's own directory, then overwrite canon/ with the PACK's two files."""
    if not os.path.exists(page):
        raise Unreachable("no demo page at %s" % page)
    src = os.path.dirname(os.path.abspath(page))
    dst = root or tempfile.mkdtemp(prefix="demopage-", dir=SCRATCH)
    out = os.path.join(dst, "site")
    if os.path.isdir(out):
        shutil.rmtree(out)
    shutil.copytree(src, out)
    cdir = os.path.join(out, "canon")
    os.makedirs(cdir, exist_ok=True)
    for name, blob in css.items():
        open(os.path.join(cdir, name), "wb").write(blob)
    return out, os.path.basename(page)


def serve(root):
    """Serve the stage over http — NEVER file://, the arm's scripts fetch beside themselves."""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):      # the gate's output is the verdict, not a web log
            pass

    handler = functools.partial(Quiet, directory=root)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, "http://127.0.0.1:%d" % httpd.server_address[1]


# ---------------------------------------------------------------------------------------
# the drive
# ---------------------------------------------------------------------------------------

def drive(url, shots=None):
    """Load the page once and ask all three questions per theme. Returns the report dict."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise Unreachable("playwright is not importable here (%s)" % e)

    report = {"url": url, "themes": {}, "nav": None, "dropdowns": [],
              "console_errors": [], "pageerrors": []}
    try:
        pw = sync_playwright().start()
    except Exception as e:                                   # pragma: no cover - env only
        raise Unreachable("playwright would not start (%s)" % e)
    try:
        try:
            browser = pw.chromium.launch()
        except Exception as e:
            raise Unreachable("no chromium this box can host (%s) — "
                              "knowledge/_render/seat_env.sh names the seat's own" % e)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda m: m.type == "error" and report["console_errors"].append(m.text))
        page.on("pageerror", lambda e: report["pageerrors"].append(str(e)))
        page.goto(url, wait_until="networkidle")
        # Settle every transition BEFORE the first computed read (runbook, render-verify).
        page.add_style_tag(content="*{transition:none!important;animation:none!important}")

        report["nav"] = page.evaluate(NAV_JS)
        for tid, label in (("ddEntityT", "entity"), ("ddCurT", "currency")):
            row = {"control": label, "expanded": None, "error": None}
            try:
                page.click("#" + tid, timeout=5000)
                row["expanded"] = page.get_attribute("#" + tid, "aria-expanded")
            except Exception as e:
                row["error"] = type(e).__name__ + ": " + str(e).split("\n")[0][:140]
            report["dropdowns"].append(row)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass

        for theme in THEMES:
            page.evaluate("(t)=>{const h=document.documentElement;"
                          "if(t==='mono'){h.removeAttribute('data-apollo-theme');}"
                          "else{h.setAttribute('data-apollo-theme',t);}}", theme)
            rows = page.evaluate(DESC_JS)
            report["themes"][theme] = rows
            if shots:
                page.screenshot(path=os.path.join(shots, "demo-page-nav-%s.png" % theme),
                                clip={"x": 0, "y": 0, "width": 320, "height": 520})
        browser.close()
    finally:
        pw.stop()
    return report


def grade(report):
    """Turn the measurement into per-theme verdicts. Returns (rows, ok)."""
    rows, ok = [], True
    nav = report.get("nav")
    nav_ok = bool(nav) and nav["rules"] > 0 and nav["display"] != "inline" \
        and nav["padding"] not in ("0px", "", None) \
        and nav["textDecorationLine"] in ("none", "") and nav["height"] >= 24
    ok = ok and nav_ok
    rows.append(("nav styled (a.nv-item)", nav_ok,
                 "not found" if not nav else
                 "%d rules · display %s · padding %s · underline %s · %.1fpx"
                 % (nav["rules"], nav["display"], nav["padding"],
                    nav["textDecorationLine"] or "none", nav["height"])))

    for row in report.get("dropdowns", []):
        good = row["expanded"] == "true"
        ok = ok and good
        rows.append(("%s dropdown opens (SOFT — attribute only, cold-run-7 F1)" % row["control"],
                     good, row["error"] or "aria-expanded=%s" % row["expanded"]))

    for theme in THEMES:
        labels = report["themes"].get(theme) or []
        edges = sorted({r["edge"] for r in labels})
        worst = max([r["clip"] for r in labels] or [99.0])
        boxes = sorted({r["boxH"] for r in labels})
        good = bool(labels) and worst <= 0.05 and edges == ["text"]
        ok = ok and good
        rows.append(("descenders intact — %s" % theme, good,
                     "%d label(s) · edge %s · box %s · worst clip %.2fpx"
                     % (len(labels), edges or "-", boxes or "-", worst)))
    return rows, ok


def run(pack, page_path, shots=None, bank=None, bite=False):
    css = pack_css(pack)
    if bite:
        # MUTATION ARM. Re-inject the PRE-FIX cascade — the `:is(...)` spelling of the base
        # leading-trim default, at (0,1,2), scoped to the template class the real page wears —
        # and require the gate to go RED. A gate that cannot be made to fail is not measuring.
        css["canon.css"] = css["canon.css"] + (
            "\n:where(.cn-template-dashboard-bento) :is(button,a,.nv-label)"
            "{text-box-trim:trim-both;text-box-edge:cap alphabetic}\n").encode()
    root, page_name = stage(page_path, css)
    httpd, base = serve(root)
    try:
        report = drive(base + "/" + page_name, shots=shots)
    finally:
        httpd.shutdown()
        httpd.server_close()
    report["pack"] = os.path.abspath(pack)
    report["page"] = os.path.abspath(page_path)
    report["bite"] = bool(bite)
    rows, ok = grade(report)
    report["rows"] = [{"assertion": a, "pass": p, "detail": d} for a, p, d in rows]
    report["verdict"] = "PASS" if ok else "FAIL"
    if bank:
        os.makedirs(os.path.dirname(os.path.abspath(bank)) or ".", exist_ok=True)
        open(bank, "w").write(json.dumps(report, indent=1))
    return report, rows, ok


def report_lines(report, rows, ok):
    out = ["DEMO-PAGE GATE — %s" % os.path.basename(report["pack"]),
           "  page: %s" % report["page"],
           "  (run-of-show plot point 09 — the page the operator drives)"]
    for a, p, d in rows:
        out.append("  %s %-58s %s" % ("✓" if p else "✗", a, d))
    npass = sum(1 for _, p, _ in rows if p)
    out.append("  %s — %d/%d assertion(s), 4 theme(s)"
               % ("DEMO-PAGE GATE PASS" if ok else "DEMO-PAGE GATE FAIL", npass, len(rows)))
    return out


# ---------------------------------------------------------------------------------------
# selftest — the bites that do not need a browser
# ---------------------------------------------------------------------------------------

def selftest():
    fails = []
    asked = []

    def bite(name, got, want):
        asked.append(name)
        if got != want:
            fails.append("%s: got %r want %r" % (name, got, want))

    # 1-4 grade() is the whole verdict, so it is what the bites drive.
    good_nav = dict(rules=53, display="flex", padding="0px 16px",
                    textDecorationLine="none", height=44.0)
    clean = {t: [dict(text="Payments", edge="text", boxH=21.0, clip=0.0)] for t in THEMES}
    base = dict(nav=good_nav, themes=clean,
                dropdowns=[dict(control="entity", expanded="true", error=None),
                           dict(control="currency", expanded="true", error=None)])
    rows, ok = grade(base)
    bite("grade/clean-is-green", ok, True)
    bite("grade/row-count", len(rows), 1 + 2 + len(THEMES))

    clipped = json.loads(json.dumps(clean))
    clipped["console"][0].update(edge="cap alphabetic", boxH=12.0, clip=5.5)
    rows, ok = grade(dict(base, themes=clipped))
    bite("grade/one-theme-clipped-is-red", ok, False)
    bite("grade/the-red-names-the-theme",
         any("console" in a and not p for a, p, _ in rows), True)

    rows, ok = grade(dict(base, nav=dict(good_nav, height=20.0)))
    bite("grade/under-the-24px-floor-is-red", ok, False)
    rows, ok = grade(dict(base, nav=dict(good_nav, rules=0)))
    bite("grade/unstyled-nav-is-red", ok, False)
    rows, ok = grade(dict(base, nav=None))
    bite("grade/missing-nav-is-red", ok, False)
    rows, ok = grade(dict(base, dropdowns=[dict(control="entity", expanded="false", error=None)]))
    bite("grade/shut-dropdown-is-red", ok, False)
    rows, ok = grade(dict(base, themes={t: [] for t in THEMES}))
    bite("grade/no-labels-is-red-not-vacuous-green", ok, False)

    # 9-10 a pack that carries neither file is UNREACHABLE, never a quiet pass.
    empty = tempfile.mkdtemp(prefix="demopage-st-", dir=SCRATCH)
    try:
        pack_css(empty)
        bite("pack/empty-dir-refuses", "returned", "Unreachable")
    except Unreachable:
        bite("pack/empty-dir-refuses", "Unreachable", "Unreachable")
    try:
        pack_css(os.path.join(empty, "nope.zip"))
        bite("pack/missing-zip-refuses", "returned", "Unreachable")
    except Unreachable:
        bite("pack/missing-zip-refuses", "Unreachable", "Unreachable")
    shutil.rmtree(empty, ignore_errors=True)

    # 11 the page this gate names must be the one the run-of-show's plot point 09 names.
    ros = sorted(glob.glob(os.path.join(REPO, "notes", "_RUN-OF-SHOW-david-rice-*.html")))
    if ros:
        txt = open(ros[-1], encoding="utf-8").read()
        bite("page/named-by-the-run-of-show",
             "outputs/coldrun-267/arm-A-blind/dashboard.html" in txt, True)

    # a bare run REFUSES in the could-not-ask register, never as an argument error and
    # never as a red — the release probe reads the exit code, and 2 was read as a live red.
    bite("bare/refuses-with-77", main([]), cna.EXIT)

    print("selftest: %d bites, %d fail(s)" % (len(asked), len(fails)))
    for f in fails:
        print("  ✗ " + f)
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--zip", help="the pack zip whose canon is driven")
    ap.add_argument("--stage", help="an UNZIPPED pack directory, instead of --zip")
    ap.add_argument("--page", default=DEMO_PAGE, help="the demo page to drive")
    ap.add_argument("--json", help="bank the full measurement here")
    ap.add_argument("--shots", help="write a per-theme sidebar screenshot into this dir")
    ap.add_argument("--bite", action="store_true",
                    help="MUTATION ARM: re-inject the pre-fix cascade, require a RED")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    pack = a.stage or a.zip
    if not pack:
        # ⛔ IT WILL NOT GUESS A PACK, and the refusal is a COULD-NOT-ASK (77), not an argument
        # error (2). A gate that fell back to the working tree would answer a question about the
        # tree while being read as an answer about the zip — the exact confusion cold run 8 had
        # to unpick. And a bare run that exited 2 was read by the release probe as a LIVE RED
        # ("ran, verdict FAIL in the pack AND in the full repo"), which is a worse lie than the
        # honest one: this gate is REPO-BOUND by construction. It grades a pack from OUTSIDE,
        # against a page the pack does not carry, so inside the pack the question is unaskable.
        return cna.refuse(
            "demo-page gate",
            "no pack was named, and the page this gate drives is missing here — it is named by "
            "`notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html` (plot point 09) and lives in the "
            "source repo, not in the pack. Name the pack that is about to ship: "
            "`--zip <pack.zip>` or `--stage <dir>`")
    if a.shots:
        os.makedirs(a.shots, exist_ok=True)
    try:
        report, rows, ok = run(pack, a.page, shots=a.shots, bank=a.json, bite=a.bite)
    except Unreachable as e:
        return cna.refuse("demo-page gate", str(e))
    print("\n".join(report_lines(report, rows, ok)))
    if a.bite:
        # In the mutation arm a RED is the pass.
        print("  MUTATION ARM: a RED above is the PASS — the pre-fix cascade was re-injected.")
        return 0 if not ok else 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
