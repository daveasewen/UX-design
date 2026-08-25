#!/usr/bin/env python3
"""
verify_behaviour_218w3_overlay.py — DRIVES the behaviour added to the #218 wave-3 OVERLAY/ACTION
cluster and asserts that ARIA STATE MOVED.

SCOPE, AND WHY IT IS ONE FILE AND NOT ELEVEN
  The cluster brief named eleven snippets. Ten of them were JUDGED and left UNTOUCHED because
  their controls promise navigation or submission that a demo cannot honour — a CTA that goes
  nowhere, a state-showcase row where `.is-pressed` is a CSS :active specimen and not a toggle,
  a ledger whose own manifest rules it PASSIVE. Fake behaviour is worse than none, so there is
  nothing there to drive. Command-palette.reference.html is the one snippet that gained real
  behaviour (receipt 2026-08-21-214-library-interface-v2.md residual 1: a keyboard-summoned
  surface with no keyboard wiring), and it is the one snippet driven here.

WHAT IT REFUSES TO DO
  A LOAD ASSERTION IS BANNED. "the palette has role=dialog", "aria-activedescendant is present",
  "the footer advertises Ctrl+K" were all TRUE while the measured defect stood — the file shipped
  ZERO behaviour JS. Every behaviour check below therefore drives a real click or a real key
  press and reads the state back off the LIVE DOM. The assertion is that a value MOVED.

THE --break ARM (a verifier that cannot fail proves nothing)
  The snippet is copied to /var/tmp/218w3-overlay/broken/ with its behaviour <script> stripped
  (the <script type="application/json" id="token-manifest"> block is left alone — it is not
  behaviour), and every behaviour check is required to go RED there BY NAME. The relative
  ../canon/ stylesheet path is mirrored alongside, so the broken copy differs from the real
  snippet in exactly one respect: the behaviour.

  ⚠ THE HARNESS CONTROLS. A page that failed to load makes every behaviour check fail, and the
  --break arm would read that as a pass. So the file also carries `control/…` checks that assert
  the AUTHORED markup arrived. Controls must be GREEN IN BOTH ARMS; a red control in the break
  arm means the arm proved nothing and the run is reported FAILED.

ENVIRONMENT (headless, proven this session)
  export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \
         FONTCONFIG_FILE=/var/tmp/fonts-218w3.conf \
         LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu

USAGE
  python3 knowledge/_render/verify_behaviour_218w3_overlay.py          # real snippet, all green
  python3 knowledge/_render/verify_behaviour_218w3_overlay.py --break  # stripped copy, all red
"""

import os
import re
import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
SNIPPETS = REPO / "knowledge" / "snippets"
BROKEN = Path(os.environ.get("BW_MUTANT_DIR", "/var/tmp/218w3-overlay")) / "broken"  # #218: shared-/var/tmp class fix

FILES = {
    "palette": "Command-palette.reference.html",
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


# ---------------------------------------------------------------- the two specimens

S1 = ".specimens > div:nth-child(1) .cp-stage"          # open, query "stat", 5 options
S2 = ".specimens > div:nth-child(2) .cp-stage"          # open, query "zzzz", empty result set

P1, IN1 = S1 + " .cp", S1 + " input[role='combobox']"
P2 = S2 + " .cp"


# ---------------------------------------------------------------- small DOM helpers

def painted(page, sel):
    """True when the element is rendered — BOTH carriers agree (hidden attr + computed display)."""
    return page.eval_on_selector(
        sel,
        "e => !e.hidden && getComputedStyle(e).display !== 'none'",
    )


def attr(page, sel, name):
    return page.eval_on_selector(sel, "(e, n) => e.getAttribute(n)", name)


def inert(page, sel):
    return page.eval_on_selector(sel, "e => e.inert === true")


def focus(page, sel):
    page.eval_on_selector(sel, "e => e.focus()")


def active_is(page, sel):
    return page.eval_on_selector(sel, "e => e === document.activeElement")


def selected_ids(page, stage):
    return page.eval_on_selector_all(
        stage + " [role='option']",
        "els => els.filter(e => e.getAttribute('aria-selected') === 'true').map(e => e.id)",
    )


def close_palette_1(page):
    """Drive the documented dismissal — focus the field, press Escape."""
    focus(page, IN1)
    page.keyboard.press("Escape")


def wait_focus(page, sel):
    """The house open order focuses after two rAFs — wait for it rather than assuming."""
    page.wait_for_function(
        "s => { const e = document.querySelector(s); return e && e === document.activeElement; }",
        arg=sel,
        timeout=2000,
    )


# ---------------------------------------------------------------- harness controls

@control("control/palette/markup-present", "palette")
def _(page):
    stages = page.eval_on_selector_all(".cp-stage", "e => e.length")
    opts = page.eval_on_selector_all(S1 + " [role='option']", "e => e.length")
    val = page.eval_on_selector(IN1, "e => e.value")
    assert stages == 2, f"expected 2 .cp-stage specimens, saw {stages}"
    assert opts == 5, f"expected 5 authored options in specimen 1, saw {opts}"
    assert val == "stat", f"authored query should be 'stat', saw {val!r}"


@control("control/palette/authored-activedescendant", "palette")
def _(page):
    ad = attr(page, IN1, "aria-activedescendant")
    assert ad == "cp1-o2", f"authored aria-activedescendant should be cp1-o2, saw {ad!r}"


@control("control/palette/at-rest-render-unchanged", "palette")
def _(page):
    """STILL-VISIBLE BY CONSTRUCTION: the script must not re-filter the authored result set."""
    shown = page.eval_on_selector_all(
        S1 + " [role='option']",
        "els => els.filter(e => getComputedStyle(e).display !== 'none').length",
    )
    assert painted(page, P1), "specimen 1 panel must render at rest"
    assert painted(page, P2), "specimen 2 panel must render at rest"
    assert shown == 5, f"all 5 authored options must still paint at rest, saw {shown}"


# ---------------------------------------------------------------- behaviour: dismissal

@check("palette/background-inert-at-rest", "palette")
def _(page):
    assert inert(page, S1 + " .cp-stage-mock"), \
        "the app behind an open modal palette is not inert"


@check("palette/esc-closes", "palette")
def _(page):
    assert painted(page, P1), "precondition: specimen 1 opens at rest"
    close_palette_1(page)
    assert not painted(page, P1), "Escape did not hide the panel"
    assert attr(page, IN1, "aria-expanded") == "false", \
        f"aria-expanded stayed {attr(page, IN1, 'aria-expanded')!r}"
    assert attr(page, S1, "data-cp-open") == "false", "stage still reports data-cp-open"
    assert painted(page, P2), "Escape must close ONE palette, not every palette on the page"


@check("palette/esc-lifts-background-inert", "palette")
def _(page):
    # BOTH SIDES ASSERTED. "not inert after Escape" alone is true of a page with no behaviour at
    # all — the --break arm caught exactly that and this check was rewritten as a transition.
    assert inert(page, S1 + " .cp-stage-mock"), "precondition: the background is inert while open"
    close_palette_1(page)
    assert not inert(page, S1 + " .cp-stage-mock"), \
        "the background stayed inert after the palette closed — the app is unusable"


@check("palette/esc-returns-focus", "palette")
def _(page):
    close_palette_1(page)
    assert active_is(page, S1), (
        "focus was not returned; it is on "
        + page.evaluate("() => document.activeElement.tagName + '.' + document.activeElement.className")
    )


@check("palette/scrim-click-closes", "palette")
def _(page):
    assert painted(page, P2), "precondition: specimen 2 opens at rest"
    page.click(S2 + " .cp-scrim", position={"x": 10, "y": 10})   # above the panel's top edge
    assert not painted(page, P2), "clicking the scrim did not dismiss the palette"
    assert attr(page, S2, "data-cp-open") == "false", "stage 2 still reports data-cp-open"


# ---------------------------------------------------------------- behaviour: the shortcut

@check("palette/ctrl-k-reopens", "palette")
def _(page):
    close_palette_1(page)
    assert not painted(page, P1), "precondition: Escape closed it"
    page.keyboard.press("Control+KeyK")
    assert painted(page, P1), "Ctrl+K did not reopen the palette the footer says it reopens"
    assert attr(page, IN1, "aria-expanded") == "true", "aria-expanded did not return to true"


@check("palette/ctrl-k-focuses-the-field", "palette")
def _(page):
    # Focus is driven AWAY first. Without that, the field is still focused from close_palette_1
    # and the check passes on a page with no behaviour — the --break arm caught it.
    close_palette_1(page)
    page.evaluate("() => document.activeElement && document.activeElement.blur()")
    assert not active_is(page, IN1), "precondition: focus is off the field before the chord"
    page.keyboard.press("Control+KeyK")
    try:
        wait_focus(page, IN1)
    except Exception:
        pass
    assert active_is(page, IN1), "the palette reopened with no keyboard entry point"


@check("palette/ctrl-k-restores-background-inert", "palette")
def _(page):
    close_palette_1(page)
    page.keyboard.press("Control+KeyK")
    wait_focus(page, IN1)
    assert inert(page, S1 + " .cp-stage-mock"), \
        "reopened without making the background inert — the modal is a lie"


@check("palette/meta-k-reopens", "palette")
def _(page):
    close_palette_1(page)
    assert not painted(page, P1), "precondition: Escape closed it"
    page.keyboard.press("Meta+KeyK")
    assert painted(page, P1), "Cmd+K did not reopen the palette"


# ---------------------------------------------------------------- behaviour: roving

@check("palette/arrowdown-moves-aria-selected", "palette")
def _(page):
    focus(page, IN1)
    assert selected_ids(page, S1) == ["cp1-o2"], f"precondition: {selected_ids(page, S1)}"
    page.keyboard.press("ArrowDown")
    assert attr(page, IN1, "aria-activedescendant") == "cp1-o3", \
        f"activedescendant is {attr(page, IN1, 'aria-activedescendant')!r}, expected cp1-o3"
    assert selected_ids(page, S1) == ["cp1-o3"], \
        f"aria-selected did not move, it is on {selected_ids(page, S1)}"


@check("palette/arrowup-moves-aria-selected", "palette")
def _(page):
    focus(page, IN1)
    page.keyboard.press("ArrowUp")
    assert attr(page, IN1, "aria-activedescendant") == "cp1-o1", \
        f"ArrowUp gave {attr(page, IN1, 'aria-activedescendant')!r}, expected cp1-o1"
    assert selected_ids(page, S1) == ["cp1-o1"], f"aria-selected on {selected_ids(page, S1)}"


@check("palette/arrowup-wraps-across-groups", "palette")
def _(page):
    focus(page, IN1)
    page.keyboard.press("ArrowUp")      # cp1-o2 -> cp1-o1 (first)
    page.keyboard.press("ArrowUp")      # wrap to the last option of the SECOND group
    assert attr(page, IN1, "aria-activedescendant") == "cp1-o5", \
        f"no wrap: {attr(page, IN1, 'aria-activedescendant')!r}"


@check("palette/arrowdown-wraps-across-groups", "palette")
def _(page):
    focus(page, IN1)
    for _i in range(3):                 # o2 -> o3 -> o4 -> o5
        page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowDown")    # wrap back to the first option of the FIRST group
    assert attr(page, IN1, "aria-activedescendant") == "cp1-o1", \
        f"no wrap: {attr(page, IN1, 'aria-activedescendant')!r}"


# ---------------------------------------------------------------- behaviour: filtering

@check("palette/typing-filters-the-listbox", "palette")
def _(page):
    page.fill(IN1, "move")
    hidden = page.eval_on_selector_all(
        S1 + " [role='option']",
        "els => els.filter(e => e.hidden && getComputedStyle(e).display === 'none').map(e => e.id)",
    )
    assert hidden == ["cp1-o1", "cp1-o2", "cp1-o3", "cp1-o4"], \
        f"the four non-matching options should be hidden, hidden = {hidden}"
    assert painted(page, "#cp1-o5"), "the one matching option was hidden too"


@check("palette/empty-group-is-hidden", "palette")
def _(page):
    page.fill(IN1, "move")
    g = page.eval_on_selector_all(
        S1 + " .cp-group",
        "els => els.map(e => e.hidden && getComputedStyle(e).display === 'none')",
    )
    assert g == [True, False], f"the 'Go to' group should collapse when nothing in it matches: {g}"


@check("palette/typing-updates-the-live-count", "palette")
def _(page):
    before = page.eval_on_selector(S1 + " [role='status']", "e => e.textContent.trim()")
    assert before == "5 results", f"authored count should be '5 results', saw {before!r}"
    page.fill(IN1, "move")
    after = page.eval_on_selector(S1 + " [role='status']", "e => e.textContent.trim()")
    assert after == "1 result", f"the live count did not follow the filter: {after!r}"


@check("palette/filter-moves-activedescendant", "palette")
def _(page):
    page.fill(IN1, "move")
    assert attr(page, IN1, "aria-activedescendant") == "cp1-o5", (
        "the cursor was left on an option the filter removed: "
        + repr(attr(page, IN1, "aria-activedescendant"))
    )
    assert selected_ids(page, S1) == ["cp1-o5"], f"aria-selected on {selected_ids(page, S1)}"


@check("palette/clearing-the-filter-restores-every-option", "palette")
def _(page):
    # ROUND TRIP, both legs asserted — "5 visible" alone is the authored state and passes with
    # no behaviour at all. The --break arm caught it.
    def visible():
        return page.eval_on_selector_all(
            S1 + " [role='option']",
            "els => els.filter(e => getComputedStyle(e).display !== 'none').length",
        )
    page.fill(IN1, "move")
    assert visible() == 1, f"precondition: the filter should leave 1 option, left {visible()}"
    page.fill(IN1, "")
    assert visible() == 5, f"clearing the query left {visible()} of 5 options visible"


@check("palette/empty-result-set-appears", "palette")
def _(page):
    """Specimen 2 authors the empty block VISIBLE; drive specimen 2's own field to zero matches
    and require the block to still be the thing on screen while every option stays hidden."""
    page.fill(S2 + " input[role='combobox']", "nothing matches this")
    assert painted(page, S2 + " .cp-empty"), "the empty-result message did not survive a filter"
    left = page.eval_on_selector_all(
        S2 + " [role='option']",
        "els => els.filter(e => getComputedStyle(e).display !== 'none').length",
    )
    assert left == 0, f"{left} option(s) painted under a zero-match query"


@check("palette/authored-hidden-option-is-not-painted", "palette")
def _(page):
    """#cp2-o1 ships `hidden` in the markup, but .cp-opt{display:flex} is an AUTHOR rule and beats
    the UA [hidden] rule — so it painted. The script enacts the author's declared intent."""
    d = page.eval_on_selector("#cp2-o1", "e => getComputedStyle(e).display")
    assert d == "none", f"a markup-hidden option is still painted (display:{d})"


# ---------------------------------------------------------------- behaviour: activation

@check("palette/enter-activates-and-closes", "palette")
def _(page):
    page.fill(IN1, "move")
    focus(page, IN1)
    page.keyboard.press("Enter")
    assert attr(page, P1, "data-cp-activated") == "cp1-o5", (
        "Enter did not commit the active option: "
        + repr(attr(page, P1, "data-cp-activated"))
    )
    assert not painted(page, P1), "Enter committed but left the palette open"


@check("palette/click-activates-and-closes", "palette")
def _(page):
    page.click("#cp1-o3")
    assert attr(page, P1, "data-cp-activated") == "cp1-o3", (
        "clicking an option did not commit it: " + repr(attr(page, P1, "data-cp-activated"))
    )
    assert not painted(page, P1), "the palette stayed open after a result was chosen"


@check("palette/activation-returns-focus", "palette")
def _(page):
    page.fill(IN1, "move")
    focus(page, IN1)
    page.keyboard.press("Enter")
    assert active_is(page, S1), (
        "focus was stranded after activation, on "
        + page.evaluate("() => document.activeElement.tagName + '.' + document.activeElement.className")
    )


# ---------------------------------------------------------------- arms

def build_broken():
    """Mirror the snippet with the behaviour <script> removed, keeping ../canon/ resolvable."""
    if BROKEN.exists():
        shutil.rmtree(BROKEN)
    (BROKEN / "snippets").mkdir(parents=True)
    shutil.copytree(REPO / "knowledge" / "canon", BROKEN / "canon")
    for name in FILES.values():
        src = (SNIPPETS / name).read_text()
        out, n = BEHAVIOUR_SCRIPT.subn("", src)
        if n != 1:
            raise SystemExit(f"FATAL: expected exactly 1 behaviour <script> in {name}, stripped {n}")
        if 'id="token-manifest"' not in out:
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
                page.goto(urls[key])                 # fresh state per assertion
                try:
                    fn(page)
                    results.append((kind, name, True, ""))
                except Exception as e:               # a crash is a red, named (a-crash-is-not-a-fail)
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
    print(f"=== verify_behaviour_218w3_overlay — {arm}")
    print("--- harness controls (must be GREEN in both arms)")
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
