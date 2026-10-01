#!/usr/bin/env python3
"""_screen_load.py — ONE headless load of a composed page, and a read of its console.

WHY (s308-D15, Dave 2026-09-29 08:05 BST, by click: "Take the three fixes, then run it again on
the next cut"; the page's first fix, verbatim: "one headless load with a console read as the
skill's default last step"). #307's blind cold run shipped a page whose first load threw
`Cannot set properties of null (setting 'innerHTML')` — and threw it again on every toolbar
change — because `renderAll()` wrote an element the Overview view had detached
(notes/_subreports/2026-09-28-307-E-cold-run.md, F01). Both of that run's faults "would have
shown on one load in a browser". The skill already told the reader to "open the console before
you claim it" (rule 16); nothing in the pack did it for them. This is that one load.

WHAT IT DOES
  Serves the page over http from the nearest ancestor that holds `knowledge/canon/canon.css`
  (the repo, or an unzipped pack) so the page's relative links resolve exactly as they do for a
  designer — never `file://` (a file origin starves scripts that fetch beside themselves,
  knowledge/_RUNBOOK-render-verify.md). Loads it once in headless Chromium, waits for `load`
  and a short settle (deferred work — rAF, timers — throws after `load`), and reads:
    * pageerror     — every uncaught exception (F01's class)
    * console error — every `console.error`, including the browser's own "Failed to load
                      resource" line for a missing script or stylesheet
  FAIL if either list is non-empty. No clicks, no themes, no screenshots: one load, one read.
  Driving the controls stays the skill's step 8 — this is the floor under it, not the drive.

BROWSER. `$RENDER_SHELL` when set (the seat's own, exported by knowledge/_render/seat_env.sh);
otherwise Playwright's bundled Chromium. Never `channel="chromium"` (the #311 loose end in
`_drive_chart_engine.py`). No Playwright or no browser on this box is COULD-NOT-ASK (exit 77,
knowledge/_could_not_ask.py) — not a pass, not a failure; the caller says "not loaded".

USAGE
  python3 knowledge/_screen_load.py path/to/screen.html [--settle-ms 800] [--json]
  python3 knowledge/_screen_load.py --selftest
  Exit: 0 clean · 1 errors on load · 2 usage · 77 could not ask.
  `_validate_screen.py --load` runs the same load as its step 5 and writes it to the record.

Built #313 lane B6 (W-308ic). The selftest plants F01's exact shape and mutates it clean.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import functools
import http.server
import json
import os
import socketserver
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _could_not_ask as cna  # noqa: E402 - ships in the gates group's helper closure

SETTLE_MS = 800


class CouldNotAsk(Exception):
    """The box cannot host the load (no Playwright, no browser, no page)."""


def serve_root(page):
    """-> the directory to serve: the nearest ancestor holding knowledge/canon/canon.css,
    else the page's own directory (a page that links nothing above itself)."""
    d = os.path.dirname(os.path.abspath(page))
    probe = d
    while True:
        if os.path.exists(os.path.join(probe, "knowledge", "canon", "canon.css")):
            return probe
        up = os.path.dirname(probe)
        if up == probe:
            return d
        probe = up


def _serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):      # the verdict is the output, not a web log
            pass
    httpd = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=root))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, "http://127.0.0.1:%d" % httpd.server_address[1]


def load(page, settle_ms=SETTLE_MS):
    """Load `page` once, headless. -> {"url", "pageerrors": [...], "console_errors": [...]}.
    Raises CouldNotAsk when the box cannot host the question."""
    if not os.path.isfile(page):
        raise CouldNotAsk("no page at %s" % page)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise CouldNotAsk("playwright is not importable here (%s) — pip install playwright && "
                          "python3 -m playwright install chromium" % e)
    root = serve_root(page)
    rel = os.path.relpath(os.path.abspath(page), root).replace(os.sep, "/")
    httpd, base = _serve(root)
    out = {"url": base + "/" + rel, "pageerrors": [], "console_errors": []}
    try:
        try:
            pw = sync_playwright().start()
        except Exception as e:                                   # pragma: no cover - env only
            raise CouldNotAsk("playwright would not start (%s)" % e)
        try:
            kw = {"args": ["--no-sandbox", "--disable-gpu"]}
            if os.environ.get("RENDER_SHELL"):
                kw["executable_path"] = os.environ["RENDER_SHELL"]
            try:
                browser = pw.chromium.launch(**kw)
            except Exception as e:
                raise CouldNotAsk("no Chromium this box can host (%s) — at Dave's seat, source "
                                  "knowledge/_render/seat_env.sh first" % str(e).split("\n")[0])
            pg = browser.new_page(viewport={"width": 1440, "height": 900})
            pg.on("pageerror", lambda e: out["pageerrors"].append(str(e).split("\n")[0]))
            pg.on("console", lambda m: m.type == "error" and out["console_errors"].append(m.text))
            pg.goto(out["url"], wait_until="load")
            pg.wait_for_timeout(settle_ms)
            browser.close()
        finally:
            pw.stop()
    finally:
        httpd.shutdown()
        httpd.server_close()
    return out


def verdict_lines(rep):
    """-> (ok, [lines]) in the screen-gate record's shape."""
    errs = ["uncaught: " + e for e in rep["pageerrors"]] + ["console: " + e for e in rep["console_errors"]]
    if not errs:
        return True, ["- load: ✅ one headless load, console clean (0 uncaught, 0 console errors)"]
    shown = "; ".join(errs[:6]) + (" … +%d more" % (len(errs) - 6) if len(errs) > 6 else "")
    return False, ["- load: ❌ %d uncaught, %d console error(s) on one headless load — %s"
                   % (len(rep["pageerrors"]), len(rep["console_errors"]), shown)]


# ------------------------------------------------------------------------------- BITE TEST
# F01 planted verbatim in shape: a render that writes a node the page has detached. Then the
# mutation that fixes it (a null guard) must come back clean — so the bite is the detection AND
# the clean case, never one alone [[mutation-tests-the-clause-not-the-feature]].
_F01 = """<!doctype html><html><head><meta charset="utf-8"><title>f01</title></head><body>
<main id="view"><ul id="acctList"></ul></main>
<script>
  function renderAll(){ document.getElementById('acctList').innerHTML = '<li>a</li>'; }
  document.getElementById('view').innerHTML = '<p>Overview</p>';   /* the view detaches #acctList */
  %s
  renderAll();
</script></body></html>"""
_GUARD = ("renderAll = function(){ var n=document.getElementById('acctList'); "
          "if(n){ n.innerHTML='<li>a</li>'; } };")
_MISSING = """<!doctype html><html><head><meta charset="utf-8"><title>missing</title>
<script src="no-such-engine.js"></script></head><body><p>x</p></body></html>"""
_LATE = """<!doctype html><html><head><meta charset="utf-8"><title>late</title></head><body>
<script>setTimeout(function(){ null.x = 1; }, 150);</script></body></html>"""


def selftest():
    ok, bad = 0, []

    def bite(name, got, want):
        nonlocal ok
        if got == want:
            ok += 1
        else:
            bad.append("%s: expected %r, got %r" % (name, want, got))

    with tempfile.TemporaryDirectory(prefix="screenload-") as d:
        def put(name, html):
            p = os.path.join(d, name)
            open(p, "w", encoding="utf-8").write(html)
            return p
        try:
            r1 = load(put("f01.html", _F01 % ""))
        except CouldNotAsk as e:
            return cna.refuse("_screen_load.py --selftest", str(e))
        bite("L1 F01's shape throws on load and is read", len(r1["pageerrors"]), 1)
        bite("L1b the read carries the browser's own words",
             "innerHTML" in (r1["pageerrors"] or [""])[0], True)
        bite("L1c the verdict fails", verdict_lines(r1)[0], False)
        r2 = load(put("f01-fixed.html", _F01 % _GUARD))
        bite("L2 MUTATION: the guarded render loads clean", (r2["pageerrors"], r2["console_errors"]), ([], []))
        bite("L2b the verdict passes", verdict_lines(r2)[0], True)
        r3 = load(put("missing.html", _MISSING))
        bite("L3 a missing script is a console error", len(r3["console_errors"]) >= 1, True)
        r4 = load(put("late.html", _LATE))
        bite("L4 an error thrown after `load` is caught by the settle", len(r4["pageerrors"]), 1)
        r5 = load(put("late.html", _LATE), settle_ms=0)
        bite("L5 MUTATION: with no settle the late error is missed (the settle is load-bearing)",
             len(r5["pageerrors"]), 0)
    root = serve_root(os.path.join(HERE, "snippets", "Button.reference.html"))
    bite("S1 a page inside the repo serves from the repo root",
         os.path.exists(os.path.join(root, "knowledge", "canon", "canon.css")), True)
    print("screen-load selftest: %d bite(s) green, %d failing" % (ok, len(bad)))
    for b in bad:
        print("  ✗ " + b)
    return 1 if bad else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in argv:
        return selftest()
    settle = SETTLE_MS
    if "--settle-ms" in argv:
        i = argv.index("--settle-ms")
        settle = int(argv[i + 1])
        del argv[i:i + 2]
    as_json = "--json" in argv
    pages = [a for a in argv if not a.startswith("--")]
    if len(pages) != 1:
        print("usage: python3 knowledge/_screen_load.py path/to/screen.html [--settle-ms N] [--json]",
              file=sys.stderr)
        return 2
    try:
        rep = load(pages[0], settle)
    except CouldNotAsk as e:
        return cna.refuse(pages[0], str(e))
    good, lines = verdict_lines(rep)
    print(json.dumps(rep, indent=2) if as_json else "\n".join(lines))
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
