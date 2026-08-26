#!/usr/bin/env python3
"""
verify_behaviour_218w3_nav.py — DRIVES the behaviour added to the #218 wave-3 NAV cluster
(Sidebar-nav, Navigations, Pagination) and asserts that ARIA STATE MOVED.

WHY IT IS IN THE REPO AND NOT A SCRATCH FILE (s191-D2): a verification that lives only in a
sandbox is a claim, not an instrument — it expires with the session. This one can be re-driven.

WHAT IT REFUSES TO DO
  A LOAD ASSERTION IS BANNED. "aria-current is present" is a property of the authored markup and
  was TRUE while the measured defect stood (receipt 2026-08-21-214-library-interface-v2.md,
  residual 2: a static aria-current no interaction could move). Every behaviour check here
  therefore drives a real click or key press and reads the state back off the LIVE DOM — the
  assertion is that the attribute moved from item A to item B, not that it exists.

THE --break ARM (a verifier that cannot fail proves nothing)
  Each snippet is copied to /var/tmp/218w3-nav/broken/ with its behaviour <script> stripped (the
  <script type="application/json" id="token-manifest"> block is left alone — it is not
  behaviour), and every behaviour check is required to go RED there BY NAME. The relative
  ../canon/ stylesheet path is mirrored alongside, so the broken copy differs from the real
  snippet in exactly one respect: the behaviour.

  ⚠ THE HARNESS CONTROLS. A page that failed to load makes every behaviour check fail, and a
  --break arm would read that as a pass. So each file also carries a `control/…markup-present`
  check that asserts the authored markup arrived. Controls must be GREEN IN BOTH ARMS; a red
  control in the break arm means the arm proved nothing and the run is reported as FAILED.

ENVIRONMENT (headless, proven this session)
  export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \
         FONTCONFIG_FILE=/var/tmp/fonts-218w3.conf \
         LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu

USAGE
  python3 knowledge/_render/verify_behaviour_218w3_nav.py            # the real snippets, all green
  python3 knowledge/_render/verify_behaviour_218w3_nav.py --break    # stripped copies, all red
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)


import os
import re
import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
SNIPPETS = REPO / "knowledge" / "snippets"
BROKEN = Path(os.environ.get("BW_MUTANT_DIR", "/var/tmp/218w3-nav")) / "broken"  # #218: shared-/var/tmp class fix (foreign-owned fixed paths refuse a fresh seat)

FILES = {
    "sidebar": "Sidebar-nav.reference.html",
    "navigations": "Navigations.reference.html",
    "pagination": "Pagination.reference.html",
}

# the behaviour block only — the JSON token-manifest opens with `<script type=...` and is untouched
BEHAVIOUR_SCRIPT = re.compile(r"[ \t]*<script>\n.*?\n[ \t]*</script>\n", re.S)

CHECKS = []          # (name, file_key, fn)  — must be RED with the script stripped
CONTROLS = []        # (name, file_key, fn)  — must be GREEN in both arms


def check(name, key):
    def deco(fn):
        CHECKS.append((name, key, fn))
        return fn
    return deco


def control(name, key):
    def deco(fn):
        CONTROLS.append((name, key, fn))
        return fn
    return deco


# ---------------------------------------------------------------- small DOM helpers

def cur(page, sel):
    """Accessible-ish label of the one element in `sel` carrying aria-current=page."""
    return page.eval_on_selector_all(
        sel,
        """els => { const c = els.filter(e => e.getAttribute('aria-current') === 'page');
                    return c.length === 1 ? c[0].textContent.trim() : '<' + c.length + ' current>'; }""",
    )


def press_on(page, sel, key, nth=0):
    page.eval_on_selector_all(sel, "(els, n) => els[n].focus()", nth)
    page.keyboard.press(key)


def active_text(page):
    return page.evaluate("() => (document.activeElement.textContent || '').trim()")


# ---------------------------------------------------------------- Sidebar-nav

SN1 = ".sn-frame:nth-of-type(1) nav.sn"
SN2 = ".sn-frame:nth-of-type(2) nav.sn"


@control("control/sidebar/markup-present", "sidebar")
def _(page):
    n = page.eval_on_selector_all("nav.sn", "e => e.length")
    links = page.eval_on_selector_all(f"{SN1} .sn-link", "e => e.length")
    assert n == 2, f"expected 2 nav.sn specimens, saw {n}"
    assert links == 7, f"expected 7 .sn-link in specimen 1, saw {links}"


@check("sidebar/current-moves-on-click", "sidebar")
def _(page):
    before = cur(page, f"{SN1} .sn-link")
    assert before == "Accounts", f"authored current should be Accounts, saw {before!r}"
    page.click(f"{SN1} .sn-link:has-text('Payments and transfers')")
    after = cur(page, f"{SN1} .sn-link")
    assert after == "Payments and transfers", f"aria-current did not move: still {after!r}"


@check("sidebar/current-moves-on-space", "sidebar")
def _(page):
    page.eval_on_selector_all(
        f"{SN1} .sn-link",
        "els => els.find(e => e.textContent.trim() === 'Spending').focus()",
    )
    page.keyboard.press("Space")
    after = cur(page, f"{SN1} .sn-link")
    assert after == "Spending", f"Space did not move aria-current: {after!r}"


@check("sidebar/current-moves-on-enter", "sidebar")
def _(page):
    page.eval_on_selector_all(
        f"{SN1} .sn-link",
        "els => els.find(e => e.textContent.trim() === 'Settings').focus()",
    )
    page.keyboard.press("Enter")
    after = cur(page, f"{SN1} .sn-link")
    assert after == "Settings", f"Enter did not move aria-current: {after!r}"


@check("sidebar/arrowdown-moves-focus", "sidebar")
def _(page):
    press_on(page, f"{SN1} .sn-link", "ArrowDown", 0)   # from Overview
    assert active_text(page) == "Accounts", f"ArrowDown left focus on {active_text(page)!r}"


@check("sidebar/group-collapses", "sidebar")
def _(page):
    page.click(f"{SN1} .sn-group-toggle")
    exp = page.get_attribute(f"{SN1} .sn-group-toggle", "aria-expanded")
    hidden = page.eval_on_selector("#sn1-cards", "e => e.hidden === true")
    assert exp == "false", f"aria-expanded should be false, saw {exp!r}"
    assert hidden, "#sn1-cards was not hidden by the disclosure"


@check("sidebar/rail-toggle-collapses-column", "sidebar")
def _(page):
    page.click(f"{SN1} .sn-toggle")
    state = page.eval_on_selector(
        SN1,
        """n => ({ rail: n.classList.contains('is-rail'),
                   navLabel: n.getAttribute('aria-label'),
                   exp: n.querySelector('.sn-toggle').getAttribute('aria-expanded'),
                   btnLabel: n.querySelector('.sn-toggle').getAttribute('aria-label'),
                   icon: n.querySelector('.sn-toggle use').getAttribute('href') })""",
    )
    assert state["rail"] is True, "column did not collapse to the rail"
    assert state["exp"] == "false", f"toggle aria-expanded {state['exp']!r}"
    assert state["navLabel"] == "Main, collapsed", f"nav name {state['navLabel']!r}"
    assert state["btnLabel"] == "Expand navigation", f"toggle name {state['btnLabel']!r}"
    assert state["icon"] == "#ic-chevron-right", f"chevron {state['icon']!r}"


@check("sidebar/specimens-are-independent", "sidebar")
def _(page):
    page.click(f"{SN2} .sn-link:has-text('Spending')")
    a = cur(page, f"{SN1} .sn-link")
    b = cur(page, f"{SN2} .sn-link")
    assert b == "Spending", f"specimen 2 current did not move: {b!r}"
    assert a == "Accounts", f"specimen 2 leaked into specimen 1: {a!r}"


# ---------------------------------------------------------------- Navigations

@control("control/navigations/markup-present", "navigations")
def _(page):
    n = page.eval_on_selector_all("nav.main a", "e => e.length")
    assert n == 4, f"expected 4 masthead links, saw {n}"


@check("navigations/current-moves-on-click", "navigations")
def _(page):
    before = cur(page, "nav.main a")
    assert before == "Accounts", f"authored current should be Accounts, saw {before!r}"
    page.click("nav.main a:has-text('Cards')")
    after = cur(page, "nav.main a")
    assert after == "Cards", f"aria-current did not move: still {after!r}"


@check("navigations/current-moves-on-space", "navigations")
def _(page):
    press_on(page, "nav.main a", "Space", 3)            # Support
    after = cur(page, "nav.main a")
    assert after == "Support", f"Space did not move aria-current: {after!r}"


@check("navigations/arrowright-moves-focus", "navigations")
def _(page):
    press_on(page, "nav.main a", "ArrowRight", 0)       # from Accounts
    assert active_text(page) == "Payments", f"ArrowRight left focus on {active_text(page)!r}"


# ---------------------------------------------------------------- Pagination

PREV = "nav.pg .ctrl[aria-label='Previous page']"
NEXT = "nav.pg .ctrl[aria-label='Next page']"


@control("control/pagination/markup-present", "pagination")
def _(page):
    n = page.eval_on_selector_all("nav.pg a", "e => e.length")
    assert n == 5, f"expected 5 page links, saw {n}"


@check("pagination/current-moves-on-click", "pagination")
def _(page):
    before = cur(page, "nav.pg a")
    assert before == "2", f"authored current should be 2, saw {before!r}"
    page.click("nav.pg a:text-is('4')")
    after = cur(page, "nav.pg a")
    label = page.get_attribute("nav.pg a:text-is('4')", "aria-label")
    stale = page.get_attribute("nav.pg a:text-is('2')", "aria-label")
    assert after == "4", f"aria-current did not move: still {after!r}"
    assert label == "Page 4, current page", f"new current name {label!r}"
    assert stale is None, f"old current kept its name: {stale!r}"


@check("pagination/next-advances-the-page", "pagination")
def _(page):
    page.click(NEXT)
    after = cur(page, "nav.pg a")
    assert after == "3", f"Next did not advance from 2: {after!r}"


@check("pagination/prev-steps-back", "pagination")
def _(page):
    page.click(PREV)
    after = cur(page, "nav.pg a")
    assert after == "1", f"Prev did not step back from 2: {after!r}"


@check("pagination/next-disables-at-upper-bound", "pagination")
def _(page):
    page.click("nav.pg a:text-is('12')")
    dis = page.eval_on_selector(NEXT, "b => b.disabled === true")
    other = page.eval_on_selector(PREV, "b => b.disabled === true")
    assert dis, "Next was not disabled on the last page"
    assert not other, "Prev was wrongly disabled on the last page"


@check("pagination/prev-disables-at-lower-bound", "pagination")
def _(page):
    page.click("nav.pg a:text-is('1')")
    dis = page.eval_on_selector(PREV, "b => b.disabled === true")
    other = page.eval_on_selector(NEXT, "b => b.disabled === true")
    assert dis, "Prev was not disabled on the first page"
    assert not other, "Next was wrongly disabled on the first page"


@check("pagination/focus-rescued-when-control-disables", "pagination")
def _(page):
    page.click(PREV)                                    # 2 -> 1, Prev disables under the pointer
    who = page.evaluate("() => document.activeElement.getAttribute('aria-label')")
    assert who == "Next page", f"focus was stranded on {who!r} when Prev disabled itself"


@check("pagination/space-selects-a-page", "pagination")
def _(page):
    page.eval_on_selector_all("nav.pg a", "els => els.find(e => e.textContent.trim() === '3').focus()")
    page.keyboard.press("Space")
    after = cur(page, "nav.pg a")
    assert after == "3", f"Space did not move aria-current: {after!r}"


@check("pagination/arrowright-moves-focus", "pagination")
def _(page):
    press_on(page, "nav.pg a", "ArrowRight", 0)         # from page 1
    assert active_text(page) == "2", f"ArrowRight left focus on {active_text(page)!r}"


# ---------------------------------------------------------------- the harness

def build_broken():
    """Mirror the snippets with the behaviour <script> removed, keeping ../canon/ resolvable."""
    if BROKEN.exists():
        shutil.rmtree(BROKEN)
    (BROKEN / "snippets").mkdir(parents=True)
    shutil.copytree(REPO / "knowledge" / "canon", BROKEN / "canon")
    for key, name in FILES.items():
        src = (SNIPPETS / name).read_text()
        out, n = BEHAVIOUR_SCRIPT.subn("", src)
        if n != 1:
            raise SystemExit(f"FATAL: expected exactly 1 behaviour <script> in {name}, stripped {n}")
        if "id=\"token-manifest\"" not in out:
            raise SystemExit(f"FATAL: stripped the token-manifest out of {name}")
        (BROKEN / "snippets" / name).write_text(out)


def run(broken):
    root = (BROKEN / "snippets") if broken else SNIPPETS
    urls = {k: (root / v).as_uri() for k, v in FILES.items()}
    results = []          # (kind, name, ok, detail)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for kind, bag in (("control", CONTROLS), ("check", CHECKS)):
            for name, key, fn in bag:
                page.goto(urls[key])                     # fresh state per assertion
                try:
                    fn(page)
                    results.append((kind, name, True, ""))
                except Exception as e:                   # a crash is a red, named (a-crash-is-not-a-fail)
                    results.append((kind, name, False, f"{type(e).__name__}: {e}".split("\n")[0][:160]))
        browser.close()
    return results


def main():
    broken = "--break" in sys.argv
    if broken:
        build_broken()
    results = run(broken)

    controls = [r for r in results if r[0] == "control"]
    checks = [r for r in results if r[0] == "check"]
    arm = "BREAK ARM (behaviour <script> stripped)" if broken else "REAL SNIPPETS"
    print(f"=== verify_behaviour_218w3_nav — {arm}")
    print(f"--- harness controls (must be GREEN in both arms)")
    for _, name, ok, detail in controls:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
    print(f"--- behaviour checks ({'must all be RED' if broken else 'must all be GREEN'})")
    for _, name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'RED '}  {name}{('  — ' + detail) if detail else ''}")

    bad_controls = [n for _, n, ok, _ in controls if not ok]
    if broken:
        wrong = [n for _, n, ok, _ in checks if ok]
        ok_run = not bad_controls and not wrong
        print(f"\ncontrols green {len(controls) - len(bad_controls)}/{len(controls)} · "
              f"behaviour red {len(checks) - len(wrong)}/{len(checks)}")
        if bad_controls:
            print("FAILED — a control went red, so the arm proved nothing: " + ", ".join(bad_controls))
        if wrong:
            print("FAILED — these passed WITHOUT behaviour, so they were never proving it: "
                  + ", ".join(wrong))
        if ok_run:
            print("BREAK ARM OK — every behaviour assertion is load-bearing.")
    else:
        bad = [n for _, n, ok, _ in checks if not ok]
        ok_run = not bad_controls and not bad
        print(f"\ncontrols green {len(controls) - len(bad_controls)}/{len(controls)} · "
              f"behaviour green {len(checks) - len(bad)}/{len(checks)}")
        print("GREEN" if ok_run else "FAILED — " + ", ".join(bad_controls + bad))
    return 0 if ok_run else 1


if __name__ == "__main__":
    os.environ.setdefault("TMPDIR", "/var/tmp")
    sys.exit(main())
