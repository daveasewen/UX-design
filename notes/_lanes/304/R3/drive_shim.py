#!/usr/bin/env python3
"""drive_shim.py [ARGS...] — #304 R3: run knowledge/_drive_chart_engine.py UNCHANGED at a seat whose only
browser is the render env's headless shell. The driver launches with channel="chromium" (a full
Chromium build this seat does not carry); this shim rewrites exactly that launch to
executable_path=$RENDER_SHELL and passes every other argument through, then runs the driver as
__main__ with the given argv. Nothing in the driver or its receipts format is edited; the receipt
records whatever browser.version the shell reports. Run from the repo (or clone) root after
`source knowledge/_render/seat_env.sh`."""
import os, sys, runpy
if any(a in ("-h", "--help") for a in sys.argv[1:2]) and len(sys.argv) == 2:
    print(__doc__); sys.exit(0)
from playwright.sync_api._generated import BrowserType
_orig = BrowserType.launch
def _launch(self, *a, **kw):
    if kw.get("channel") == "chromium":
        kw.pop("channel"); kw["executable_path"] = os.environ["RENDER_SHELL"]
    return _orig(self, *a, **kw)
BrowserType.launch = _launch
sys.argv = ["knowledge/_drive_chart_engine.py"] + sys.argv[1:]
runpy.run_path(os.path.join(os.getcwd(), "knowledge", "_drive_chart_engine.py"), run_name="__main__")
