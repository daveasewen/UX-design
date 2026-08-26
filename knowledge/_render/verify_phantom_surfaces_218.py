#!/usr/bin/env python3
"""
verify_phantom_surfaces_218.py — DRIVES the seven phantom-affordance surfaces built (and in one
case DELIBERATELY NOT built) under s218-D4, and asserts the surfaces are real.

THE CLASS THIS INSTRUMENT EXISTS FOR
  #218 W3 found seven controls promising surfaces ABSENT from the DOM ("aria-expanded on nothing
  is a lie in ARIA"). Dave ruled the class: build them. A gate that only reads markup cannot tell
  a built surface from a described one — that is precisely how the class survived this long — so
  every check below drives a real click or key press and reads the state back off the LIVE DOM.

  ⛔ A LOAD ASSERTION IS BANNED. "the panel is in the markup" was TRUE of nothing that worked.
  Each check asserts a TRANSITION: hidden -> shown, closed -> open, chip absent -> chip present,
  two date groups -> three.

THE SEVEN, AND WHAT EACH ONE'S PROOF LOOKS LIKE
  1 Headers            "More options"      -> an APG menu button          (open/walk/dismiss)
  2 Navigations        Search + Account    -> a disclosure + a menu       (reveal/focus/dismiss)
  3 Avatar-group       "+N" and the group  -> the overflow list           (open/contents/exclusive)
  4 Standing-order row "Manage"            -> an inline action disclosure (open/pause/cancel)
  5 Kpi-tile           table CTA           -> ⛔ NOTHING WIRED, BY THE FILE'S OWN PROHIBITION.
                                              The panel is DRAWN as a marked specimen; the proof
                                              is that the drawing is there AND the CTA is still
                                              inert (no aria-controls, no aria-expanded).
  6 Confirmation       "the Replay button" -> ⛔ NOTHING BUILT, AND THAT IS THE FINDING. The
                                              button exists in the showroom's ONE BAR (#98-D1,
                                              ds-029/#103); the file's PROSE was the defect and
                                              the prose was repaired. Proof: the sentence now
                                              names the real control, and the component still
                                              owns no replay affordance of its own.
  7 Timeline           "Load older activity" -> a real load               (append/exhaust/rescue)

THE --break ARM (a verifier that cannot fail proves nothing)
  Each file is copied to /var/tmp/218ph/broken/ with its s218-D4 work REMOVED, and every check is
  required to go RED there BY NAME. The removal differs per file because the work differs:
    · behaviour files (Headers, Navigations, Avatar-group, Standing-order row, Timeline) — the
      inline behaviour <script> is stripped. The JSON <script type="application/json"> blocks
      (token-manifest, and Timeline's declared demo dataset) are left alone: they are not
      behaviour.
    · Kpi-tile — the S218-D4-KPI-SPECIMEN block is stripped. There is no script to strip: the
      file's own header forbids wiring the panel, and that prohibition was honoured.
    · Confirmation — the s218-D4 correction paragraph is stripped, restoring the prose that
      described a button living somewhere else as though it lived here.

  ⚠ THE HARNESS CONTROLS. A page that failed to load makes every behaviour check fail, and the
  --break arm would read that as a pass. So each file also carries control checks that assert the
  authored markup arrived. Controls must be GREEN IN BOTH ARMS; a red control means the arm proved
  nothing and the run is reported FAILED.

ENVIRONMENT (headless, driven this session)
  export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \
         FONTCONFIG_FILE=/var/tmp/fonts-s218ph.conf \
         LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu

USAGE
  python3 knowledge/_render/verify_phantom_surfaces_218.py            # the real files, all green
  python3 knowledge/_render/verify_phantom_surfaces_218.py --break    # mutated copies, all red
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
SHOWROOM = REPO / "showroom"
BROKEN = Path(os.environ.get("BW_MUTANT_DIR", "/var/tmp/218ph")) / "broken"

FILES = {
    "headers":  "Headers.reference.html",
    "nav":      "Navigations.reference.html",
    "avatar":   "Avatar-group.reference.html",
    "mandate":  "Standing-order-mandate-row.reference.html",
    "kpi":      "Kpi-tile.reference.html",
    "confirm":  "Confirmation.reference.html",
    "timeline": "Timeline.reference.html",
}

# the behaviour block only — a JSON island opens with `<script type=...` and is untouched
BEHAVIOUR_SCRIPT = re.compile(r"[ \t]*<script>\n.*?\n[ \t]*</script>\n", re.S)
KPI_SPECIMEN = re.compile(r"[ \t]*<!-- S218-D4-KPI-SPECIMEN START -->.*?<!-- S218-D4-KPI-SPECIMEN END -->\n", re.S)
CONFIRM_CORRECTION = re.compile(r"⬛ WHERE THE REPLAY BUTTON LIVES.*?is NOT built here\.\n", re.S)

CHECKS = []          # (name, file_key, fn)  — must be RED in the break arm
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

def attr(page, sel, name):
    return page.eval_on_selector(sel, "(el, n) => el.getAttribute(n)", name)


def hidden(page, sel):
    return page.eval_on_selector(sel, "el => el.hidden")


def active(page, prop="id"):
    return page.evaluate("(p) => { const a = document.activeElement; return a ? (a.getAttribute(p) || a.tagName + ':' + (a.textContent||'').trim().slice(0,40)) : null; }", prop)


def active_text(page):
    return page.evaluate("() => (document.activeElement.textContent || '').trim()")


def count(page, sel):
    return page.eval_on_selector_all(sel, "els => els.length")


def text_of(page, sel):
    return page.eval_on_selector_all(sel, "els => els.map(e => e.textContent.trim())")


# ================================================================ 1 · HEADERS

@control("control/headers/markup-present", "headers")
def _(page):
    assert count(page, "header.content-header") == 1, "the content header did not render"
    assert count(page, "#hdrMoreTrig") == 1, "the More options trigger is missing"


@check("headers/menu-opens-and-focuses-first-item", "headers")
def _(page):
    assert attr(page, "#hdrMoreTrig", "aria-expanded") == "false", "authored state should be closed"
    page.click("#hdrMoreTrig")
    assert attr(page, "#hdrMoreTrig", "aria-expanded") == "true", "aria-expanded did not move"
    assert attr(page, "#hdrMoreMenu", "data-open") == "true", "the panel did not open"
    assert active_text(page) == "Download statements", f"focus did not enter the menu: {active_text(page)!r}"


@check("headers/arrowdown-walks-the-items", "headers")
def _(page):
    page.click("#hdrMoreTrig")
    page.keyboard.press("ArrowDown")
    assert active_text(page) == "Filter by date", f"ArrowDown left focus on {active_text(page)!r}"


@check("headers/menuitem-dismisses-and-returns-focus", "headers")
def _(page):
    page.click("#hdrMoreTrig")
    page.click("#hdrMoreMenu .opt:nth-of-type(1)")
    assert attr(page, "#hdrMoreMenu", "data-open") == "false", "the menu stayed open after an item was chosen"
    assert active(page) == "hdrMoreTrig", f"focus was not returned to the trigger: {active(page)!r}"


@check("headers/escape-closes-and-returns-focus", "headers")
def _(page):
    # TWO-SIDED: the open leg is asserted first. Without it this check passed with the behaviour
    # stripped — "still closed, focus still on the trigger" is the authored state, not a transition.
    page.click("#hdrMoreTrig")
    assert attr(page, "#hdrMoreTrig", "aria-expanded") == "true", "the menu never opened, so closing it proves nothing"
    page.keyboard.press("Escape")
    assert attr(page, "#hdrMoreTrig", "aria-expanded") == "false", "Escape did not close the menu"
    assert active(page) == "hdrMoreTrig", f"Escape stranded focus at {active(page)!r}"


@check("headers/outside-click-closes", "headers")
def _(page):
    page.click("#hdrMoreTrig")
    assert attr(page, "#hdrMoreMenu", "data-open") == "true", "the menu never opened, so dismissing it proves nothing"
    page.click(".display h1")
    assert attr(page, "#hdrMoreMenu", "data-open") == "false", "clicking away left the menu open"


# ================================================================ 2 · NAVIGATIONS

@control("control/nav/markup-present", "nav")
def _(page):
    assert count(page, "header.masthead") == 1, "the masthead did not render"
    assert count(page, "#navSearchTrig") == 1 and count(page, "#navAcctTrig") == 1, "an action trigger is missing"
    assert count(page, "nav.main a") == 4, "the primary nav lost its links"


@check("nav/search-reveals-and-takes-focus", "nav")
def _(page):
    assert hidden(page, "#navSearch") is True, "the search bar should start hidden"
    page.click("#navSearchTrig")
    assert hidden(page, "#navSearch") is False, "the search bar did not reveal"
    assert attr(page, "#navSearchTrig", "aria-expanded") == "true", "aria-expanded did not move"
    assert active(page) == "navSearchInput", f"focus did not land in the field: {active(page)!r}"


@check("nav/search-escape-closes-and-returns-focus", "nav")
def _(page):
    page.click("#navSearchTrig")
    assert hidden(page, "#navSearch") is False, "the bar never revealed, so closing it proves nothing"
    assert active(page) == "navSearchInput", "focus never entered the field, so returning it proves nothing"
    page.keyboard.press("Escape")
    assert hidden(page, "#navSearch") is True, "Escape did not close the search bar"
    assert active(page) == "navSearchTrig", f"Escape stranded focus at {active(page)!r}"


@check("nav/clear-empties-the-field", "nav")
def _(page):
    page.click("#navSearchTrig")
    page.fill("#navSearchInput", "Meridian")
    page.click("#navSearch .clear")
    assert page.input_value("#navSearchInput") == "", "the clear button did not empty the field"
    assert active(page) == "navSearchInput", "the clear button stole focus out of the field"


@check("nav/account-menu-opens-and-focuses-first-item", "nav")
def _(page):
    page.click("#navAcctTrig")
    assert attr(page, "#navAcctTrig", "aria-expanded") == "true", "aria-expanded did not move"
    assert attr(page, "#navAcctMenu", "data-open") == "true", "the account menu did not open"
    assert active_text(page) == "Your profile", f"focus did not enter the menu: {active_text(page)!r}"


@check("nav/account-menu-escape-returns-focus", "nav")
def _(page):
    page.click("#navAcctTrig")
    assert attr(page, "#navAcctTrig", "aria-expanded") == "true", "the menu never opened, so closing it proves nothing"
    page.keyboard.press("Escape")
    assert attr(page, "#navAcctTrig", "aria-expanded") == "false", "Escape did not close the account menu"
    assert active(page) == "navAcctTrig", f"Escape stranded focus at {active(page)!r}"


@check("nav/w3-destination-selection-still-works", "nav")
def _(page):
    # REGRESSION GUARD: #218 W3 wired aria-current on this masthead. s218-D4 extended the same
    # script; this asserts the extension did not eat the behaviour it was added beside.
    page.click("nav.main a:has-text('Cards')")
    who = page.eval_on_selector_all(
        "nav.main a",
        "els => { const c = els.filter(e => e.getAttribute('aria-current') === 'page'); return c.length === 1 ? c[0].textContent.trim() : '<' + c.length + ' current>'; }")
    assert who == "Cards", f"aria-current did not move: {who!r}"


# ================================================================ 3 · AVATAR-GROUP

@control("control/avatar/markup-present", "avatar")
def _(page):
    assert count(page, "#avgMoreTrig") == 1 and count(page, "#avgAllTrig") == 1, "an overflow trigger is missing"
    assert count(page, ".avg") >= 6, "the stacks did not render"


@check("avatar/plus-n-opens-the-overflow-list", "avatar")
def _(page):
    assert hidden(page, "#avgMorePop") is True, "the overflow list should start hidden"
    page.click("#avgMoreTrig")
    assert hidden(page, "#avgMorePop") is False, "the overflow list did not open"
    assert attr(page, "#avgMoreTrig", "aria-expanded") == "true", "aria-expanded did not move"
    names = text_of(page, "#avgMorePop li")
    assert len(names) == 3, f"'+3' should list exactly the 3 members the stack hid, saw {len(names)}"


@check("avatar/one-target-lists-the-whole-set", "avatar")
def _(page):
    page.click("#avgAllTrig")
    assert hidden(page, "#avgAllPop") is False, "the group-as-one-target list did not open"
    names = text_of(page, "#avgAllPop li")
    assert len(names) == 6, f"'all 6 approvers' should list 6 people, saw {len(names)}"


@check("avatar/opening-one-list-closes-the-other", "avatar")
def _(page):
    page.click("#avgMoreTrig")
    assert hidden(page, "#avgMorePop") is False, "the first list never opened, so exclusivity proves nothing"
    page.click("#avgAllTrig")
    assert hidden(page, "#avgAllPop") is False, "the second list never opened"
    assert hidden(page, "#avgMorePop") is True, "two overflow lists were open at once"
    assert attr(page, "#avgMoreTrig", "aria-expanded") == "false", "the first trigger still claims to be expanded"


@check("avatar/escape-closes-and-returns-focus", "avatar")
def _(page):
    page.click("#avgMoreTrig")
    assert hidden(page, "#avgMorePop") is False, "the list never opened, so closing it proves nothing"
    page.keyboard.press("Escape")
    assert hidden(page, "#avgMorePop") is True, "Escape did not close the overflow list"
    assert active(page) == "avgMoreTrig", f"Escape stranded focus at {active(page)!r}"


# ================================================================ 4 · STANDING-ORDER / MANDATE ROW

ROW1 = "ul.mdlist li.mrow:nth-of-type(1)"
ROW2 = "ul.mdlist li.mrow:nth-of-type(2)"


@control("control/mandate/markup-present", "mandate")
def _(page):
    assert count(page, "ul.mdlist li.mrow") >= 6, "the mandate list did not render"
    assert count(page, ".mr-manage") == 8, "the manage controls are not all present"


@check("mandate/manage-opens-the-inline-surface", "mandate")
def _(page):
    trig = f"{ROW1} .mr-manage"
    assert attr(page, trig, "aria-expanded") == "false", "authored state should be closed"
    page.click(trig)
    assert attr(page, trig, "aria-expanded") == "true", "aria-expanded did not move"
    assert count(page, f"{ROW1} .mr-actions:not([hidden])") == 1, "the action surface did not open"
    assert active_text(page) == "Pause", f"focus did not enter the surface: {active_text(page)!r}"


@check("mandate/pause-moves-the-rows-own-state", "mandate")
def _(page):
    assert count(page, f"{ROW1} .status") == 0, "row 1 is the active row and should carry no chip"
    page.click(f"{ROW1} .mr-manage")
    page.click(f"{ROW1} [data-mr-action='pause']")
    chips = text_of(page, f"{ROW1} .status")
    assert chips and "Paused" in chips[0], f"the row did not take the paused state: {chips!r}"
    assert text_of(page, f"{ROW1} .mr-act")[0] == "Resume", "the control did not become its own inverse"


@check("mandate/cancel-reaches-the-drawn-cancelled-state", "mandate")
def _(page):
    page.click(f"{ROW2} .mr-manage")
    page.click(f"{ROW2} [data-mr-action='cancel']")
    assert count(page, f"{ROW2}.is-cancelled") == 1, "the row did not enter the cancelled state"
    assert "Cancelled" in " ".join(text_of(page, f"{ROW2} .status")), "the cancelled WORD is missing from the chip"
    assert page.eval_on_selector(f"{ROW2} .mr-manage", "el => el.disabled") is True, "the control stayed live on a cancelled mandate"
    assert page.evaluate("() => document.activeElement.classList.contains('mr-payee')") is True, \
        "focus was stranded on the control that disabled itself"


@check("mandate/only-one-row-manages-at-a-time", "mandate")
def _(page):
    page.click(f"{ROW1} .mr-manage")
    assert attr(page, f"{ROW1} .mr-manage", "aria-expanded") == "true", "row 1 never opened, so exclusivity proves nothing"
    page.click(f"{ROW2} .mr-manage")
    assert attr(page, f"{ROW2} .mr-manage", "aria-expanded") == "true", "row 2 never opened"
    assert attr(page, f"{ROW1} .mr-manage", "aria-expanded") == "false", "two mandate surfaces were open at once"


@check("mandate/escape-closes-and-returns-focus", "mandate")
def _(page):
    page.click(f"{ROW1} .mr-manage")
    assert attr(page, f"{ROW1} .mr-manage", "aria-expanded") == "true", "the surface never opened, so closing it proves nothing"
    assert count(page, f"{ROW1} .mr-actions:not([hidden])") == 1, "the panel never showed"
    page.keyboard.press("Escape")
    assert attr(page, f"{ROW1} .mr-manage", "aria-expanded") == "false", "Escape did not close the surface"
    assert page.evaluate("() => document.activeElement.classList.contains('mr-manage')") is True, \
        "Escape did not return focus to the manage control"


# ================================================================ 5 · KPI-TILE (drawn, NOT wired)

@control("control/kpi/markup-present", "kpi")
def _(page):
    assert count(page, ".kpi-tile") >= 7, "the tiles did not render"
    assert count(page, ".kpi-cta") == 1, "the optional table CTA is missing"


@control("control/kpi/cta-is-still-inert", "kpi")
def _(page):
    # INVARIANT, green in both arms: the file's own header forbids wiring this panel and s218-D4
    # did not overrule it. If a later hand wires the CTA, this control goes red and says why.
    assert attr(page, ".kpi-cta", "aria-controls") is None, "the CTA gained aria-controls — the panel was wired"
    assert attr(page, ".kpi-cta", "aria-expanded") is None, "the CTA gained aria-expanded — the panel was wired"


@check("kpi/panel-specimen-is-drawn-beside-the-tile", "kpi")
def _(page):
    rows = count(page, ".kpi-panel-spec tbody tr")
    assert rows == 12, f"the specimen should draw the sparkline's twelve points, saw {rows}"
    assert count(page, ".kpi-panel-spec caption") == 1, "the specimen table has no caption"
    assert count(page, ".kpi-panel-spec [role='region'][tabindex='0']") == 1, "the specimen is not reachable as a region"
    assert count(page, ".kpi-panel-spec th[scope='row']") == 12, "the specimen lost its row headers"


@check("kpi/specimen-is-marked-and-quotes-the-prohibition", "kpi")
def _(page):
    mark = text_of(page, ".kpi-panel-spec .spec-mark")
    assert mark and "not wired" in mark[0], f"the specimen is not marked as unwired: {mark!r}"
    body = page.evaluate("() => document.body.innerText")
    assert "canon by improvisation" in body, "the header's prohibition is not quoted on the page"


# ================================================================ 6 · CONFIRMATION (nothing built — the finding)

@control("control/confirm/markup-present", "confirm")
def _(page):
    assert count(page, ".confirm[role='group']") == 1, "the confirmation panel did not render"
    assert count(page, ".confirm__actions .btn") == 2, "the two real actions are missing"


@control("control/confirm/component-owns-no-replay-control", "confirm")
def _(page):
    # INVARIANT, green in both arms. #98-D1 purged demo controls out of the snippet sources; this
    # control is what would go red if s218-D4 (or a later hand) put one back.
    n = page.eval_on_selector_all(
        "button, a",
        "els => els.filter(e => /replay/i.test((e.textContent || '') + ' ' + (e.getAttribute('aria-label') || ''))).length")
    assert n == 0, f"an in-file replay control appeared ({n}) — that duplicates the ruled bar control (#98-D1)"


@check("confirm/motion-prose-names-the-real-control", "confirm")
def _(page):
    # The phantom here was a SENTENCE, so the repair is asserted where the sentence lives: the
    # file's own header comment, read out of the DOM as a comment node.
    doc = page.evaluate("""() => {
        const out = []; const w = document.createNodeIterator(document, NodeFilter.SHOW_COMMENT);
        let n; while ((n = w.nextNode())) out.push(n.nodeValue);
        return out.join('\\n').replace(/\\s+/g, ' '); }""")   # the prose wraps; match on collapsed whitespace
    assert "ONE BAR" in doc, "the header no longer says WHERE the Replay button lives"
    assert "#98-D1" in doc, "the header does not cite the ruling that put Replay in the bar"
    assert "gen_showroom.py" in doc, "the header does not name the artefact that owns the control"
    assert "ds-029" in doc, "the header does not cite the idiom ruling that keeps this snippet untouched"


@control("control/confirm/bar-replay-exists-and-is-enabled", "confirm")
def _(page):
    # THE PREMISE, DRIVEN RATHER THAN ASSERTED: the button the prose points at is real. Read off
    # the generated showroom page (never modified by this lane) in a second navigation.
    src = SHOWROOM / "confirmation.html"
    assert src.exists(), "showroom/confirmation.html is missing — the premise cannot be checked"
    page.goto(src.as_uri())          # the harness re-navigates before every assertion, so this is safe
    assert page.eval_on_selector("#replay", "el => !el.disabled") is True, \
        "the showroom bar's Replay is DISABLED for this component — the prose would be wrong again"


# ================================================================ 7 · TIMELINE

TL1 = "section.tl:nth-of-type(1)"


@control("control/timeline/markup-present", "timeline")
def _(page):
    assert count(page, f"{TL1} .tl-group") == 2, "the authored transaction history did not render"
    assert count(page, f"{TL1} .tl-list > li") == 5, "the authored entries are not all present"


@control("control/timeline/prohibited-roles-absent", "timeline")
def _(page):
    # INVARIANT, green in both arms: this component's header PROHIBITS aria-current and
    # progressbar, and the load behaviour must never introduce them. Driven after two loads.
    for _i in range(2):
        if count(page, "#tlMore"):
            page.click("#tlMore")
    assert count(page, "[role='progressbar']") == 0, "a progressbar appeared on a Timeline"
    assert count(page, "[aria-current]") == 0, "aria-current appeared on a Timeline"
    assert count(page, f"{TL1} .tl-list > li[tabindex]") == 0, "a loaded entry became focusable"


@check("timeline/load-appends-an-older-group", "timeline")
def _(page):
    before = count(page, f"{TL1} .tl-group")
    entries_before = count(page, f"{TL1} .tl-list > li")
    page.click("#tlMore")
    assert count(page, f"{TL1} .tl-group") == before + 1, "no older date group arrived"
    assert count(page, f"{TL1} .tl-list > li") == entries_before + 2, "the appended group carried no entries"


@check("timeline/load-is-announced", "timeline")
def _(page):
    page.click("#tlMore")
    said = page.eval_on_selector("#tlLive", "el => el.textContent.trim()")
    assert "older" in said and "August" in said, f"the load was silent to AT: {said!r}"


@check("timeline/second-load-exhausts-and-rescues-focus", "timeline")
def _(page):
    page.eval_on_selector("#tlMore", "el => el.focus()")
    page.keyboard.press("Enter")
    page.keyboard.press("Enter")
    assert count(page, "#tlMore") == 0, "the control survived an exhausted feed"
    assert count(page, f"{TL1} .tl-end") == 1, "no end note replaced the control"
    assert page.evaluate("() => document.activeElement.classList.contains('tl-end')") is True, \
        "focus was stranded when the button was removed"


@check("timeline/appended-entry-carries-its-word-not-just-a-dot", "timeline")
def _(page):
    page.click("#tlMore")
    words = text_of(page, f"{TL1} .tl-group:nth-of-type(3) .status")
    assert words and all(w.strip() for w in words), f"a loaded status chip carries no word: {words!r}"


# ---------------------------------------------------------------- the harness

def build_broken():
    """Mirror the files with their s218-D4 work removed, keeping ../canon/ resolvable."""
    if BROKEN.exists():
        shutil.rmtree(BROKEN)
    (BROKEN / "snippets").mkdir(parents=True)
    shutil.copytree(REPO / "knowledge" / "canon", BROKEN / "canon")
    for key, name in FILES.items():
        src = (SNIPPETS / name).read_text()
        if key == "kpi":
            out, n = KPI_SPECIMEN.subn("", src)
            what = "the S218-D4-KPI-SPECIMEN block"
        elif key == "confirm":
            out, n = CONFIRM_CORRECTION.subn("", src)
            what = "the s218-D4 prose correction"
        else:
            out, n = BEHAVIOUR_SCRIPT.subn("", src)
            what = "the behaviour <script>"
        if n != 1:
            raise SystemExit(f"FATAL: expected exactly 1 removal of {what} in {name}, made {n}")
        if 'id="token-manifest"' not in out:
            raise SystemExit(f"FATAL: the mutation ate the token-manifest in {name}")
        (BROKEN / "snippets" / name).write_text(out)


def run(broken):
    root = (BROKEN / "snippets") if broken else SNIPPETS
    urls = {k: (root / v).as_uri() for k, v in FILES.items()}
    results = []          # (kind, name, ok, detail)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        # ⚠ A SHORT ACTIONABILITY TIMEOUT IS PART OF THE BREAK ARM'S DESIGN. With the behaviour
        # stripped, a menu panel stays opacity:0/pointer-events:none, so Playwright would wait the
        # full 30s default for every click that can never land — the arm would take half an hour
        # and look like a hang rather than a red. 2.5s is far beyond any real interaction here.
        page.set_default_timeout(2500)
        for kind, bag in (("control", CONTROLS), ("check", CHECKS)):
            for name, key, fn in bag:
                page.goto(urls[key])                     # fresh state per assertion
                try:
                    fn(page)
                    results.append((kind, name, True, ""))
                except Exception as e:                   # a crash is a red, named
                    results.append((kind, name, False, f"{type(e).__name__}: {e}".split("\n")[0][:170]))
        browser.close()
    return results


def main():
    broken = "--break" in sys.argv
    if broken:
        build_broken()
    results = run(broken)

    controls = [r for r in results if r[0] == "control"]
    checks = [r for r in results if r[0] == "check"]
    arm = "BREAK ARM (s218-D4 work removed)" if broken else "REAL FILES"
    print(f"=== verify_phantom_surfaces_218 — {arm}")
    print("--- harness controls (must be GREEN in both arms)")
    for _, name, ok, detail in controls:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
    print(f"--- surface checks ({'must all be RED' if broken else 'must all be GREEN'})")
    for _, name, ok, detail in checks:
        print(f"  {'PASS' if ok else 'RED '}  {name}{('  — ' + detail) if detail else ''}")

    bad_controls = [n for _, n, ok, _ in controls if not ok]
    if broken:
        wrong = [n for _, n, ok, _ in checks if ok]
        ok_run = not bad_controls and not wrong
        print(f"\ncontrols green {len(controls) - len(bad_controls)}/{len(controls)} · "
              f"surfaces red {len(checks) - len(wrong)}/{len(checks)}")
        if bad_controls:
            print("FAILED — a control went red, so the arm proved nothing: " + ", ".join(bad_controls))
        if wrong:
            print("FAILED — these passed WITHOUT the s218-D4 work, so they were never proving it: "
                  + ", ".join(wrong))
        if ok_run:
            print("BREAK ARM OK — every surface assertion is load-bearing.")
    else:
        bad = [n for _, n, ok, _ in checks if not ok]
        ok_run = not bad_controls and not bad
        print(f"\ncontrols green {len(controls) - len(bad_controls)}/{len(controls)} · "
              f"surfaces green {len(checks) - len(bad)}/{len(checks)}")
        print("GREEN" if ok_run else "FAILED — " + ", ".join(bad_controls + bad))
    return 0 if ok_run else 1


if __name__ == "__main__":
    os.environ.setdefault("TMPDIR", "/var/tmp")
    sys.exit(main())
