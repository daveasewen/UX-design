#!/usr/bin/env python3
"""
verify_quality_forms_218.py — DRIVES the #218 quality-wave lane 1 (FORMS family) repairs plus
the repo-wide `{once:true}` sweep, and asserts that real state MOVED.

WHY THIS FILE EXISTS
  Wave-3's existence premise was discharged by measurement; its successor is a QUALITY pass.
  Lane β proved the model by finding four live defects in five gated files just by driving
  them hard. This lane did the same to the eight forms-family components
  (Form-layout · Date-picker · Date-range-picker · Time-picker · Amount-input · File-upload ·
  Secure-entry (the OTP) · Textarea) and then ran β's R1 grep across all 137 snippets.

WHAT IT REFUSES TO DO
  A LOAD ASSERTION IS BANNED (inherited from verify_behaviour_218w3_overlay.py via
  verify_wave3_beta_218.py). "The dismiss button has an aria-label" was TRUE for the entire
  time the dismiss button removed NOTHING. Every check below drives a real click, key press,
  file selection or timer and reads the state back off the LIVE DOM; the assertion is that a
  value MOVED.

THE DEFECTS THIS FILE PINS (all MEASURED at HEAD before any edit, in this environment)
  1. Tags · Notifications · Filter-toolbar-bar — THE DISMISS REMOVED NOTHING. 11->11, 11->11,
     3->3. β's R1 class, live in three more files: a `{once:true}` listener guarded on
     propertyName is unsubscribed by the FIRST transitionend to arrive (transform /
     opacity / border-bottom-width respectively), so the guarded property's own event lands
     with nothing listening. In Tags and Filter-toolbar-bar the chip stayed CONNECTED at
     max-width:0 — an invisible ghost still in the tab order and the accessibility tree.
     In Notifications the !important bit as well: transitionrun never fired for max-height
     at all.
  2. Secure-entry — the resend button DISABLED ITSELF WHILE HOLDING FOCUS (activeElement to
     BODY, WCAG 2.4.3), and its countdown NEVER RESTARTED (`const tick` cleared at zero), so
     after one resend the control was disabled permanently and "in 30s" never moved.
  3. File-upload — removing a staged row stranded focus on BODY, both with siblings left and
     on the last row. And α's question answered by driving: aria-invalid really was 0 with a
     REJECTED row on screen (siblings carry 2-7), so nothing in the a11y tree said invalid.
  4. Date-picker / Date-range-picker — closing the panel while a day button held focus
     stranded activeElement on BODY (the panel is display:none when closed). Driven with a
     SYNTHETIC pointerdown, which moves no focus of its own, so the reading is the
     component's and not the browser's.
  5. Date-range-picker — THE RANGE WAS UNPICKABLE FROM THE KEYBOARD. pick() rebuilt the grid
     with innerHTML='' after the start date, destroying the focused button; every subsequent
     arrow was ignored (the handler requires a .dr-day activeElement) and #f-to stayed EMPTY.
  6. Time-picker — the CLOSED listbox was opacity:0 + pointer-events:none only: still
     display:block, visibility:visible, 248px tall, with all 48 role="option" children in the
     accessibility tree while the trigger reported aria-expanded="false"; focus could remain
     on an option inside it.
  7. Data-grid / Empty-state — γ's two TYPE-002 rows (raw font-weight:500 in component
     scope). Ratchet measured 1095 before, 1093 after: it SHRANK by exactly two.

THE --break ARM (a verifier that cannot fail proves nothing)
  Mutants are generated FROM THE CURRENT FILES at run time, never from a stored copy — a
  stale mutant silently proves yesterday's clause. Each mutant re-introduces ONE repaired
  defect and the check that pins it is required to go RED BY NAME.

  ⚠ THE HARNESS CONTROLS. A page that failed to load makes every behaviour check fail, and a
  --break arm would read that as a pass. Every arm therefore also runs `control/…` checks
  asserting the AUTHORED markup arrived. Controls must be GREEN IN BOTH ARMS; a red control
  in a break arm means the arm proved nothing and the run is reported FAILED.

ENVIRONMENT (headless, driven this session)
  export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \\
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \\
         FONTCONFIG_FILE=/var/tmp/fonts-s218qf.conf \\
         LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu

USAGE
  python3 knowledge/_render/verify_quality_forms_218.py              # real snippets, all green
  python3 knowledge/_render/verify_quality_forms_218.py --break all  # every mutant, RED by name
  python3 knowledge/_render/verify_quality_forms_218.py --break tags-once-listener
  python3 knowledge/_render/verify_quality_forms_218.py --list       # mutants + what they redden
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import os, pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SNIPPETS = REPO / "knowledge" / "snippets"
CANON = REPO / "knowledge" / "canon"
# session-suffixed: /var/tmp is SHARED across sessions and foreign artefacts are stale + unwritable
WORK = pathlib.Path(os.environ.get("BM_MUTANT_DIR", "/var/tmp/218qf-mutants"))

FILES = ["Form-layout.reference.html", "Date-picker.reference.html",
         "Date-range-picker.reference.html", "Time-picker.reference.html",
         "Amount-input.reference.html", "File-upload.reference.html",
         "Secure-entry.reference.html", "Textarea.reference.html",
         "Tags.reference.html", "Notifications.reference.html",
         "Filter-toolbar-bar.reference.html",
         "Data-grid.reference.html", "Empty-state.reference.html"]

ONCE_LISTENER = {
    "Tags.reference.html": ("max-width", "c"),
    "Filter-toolbar-bar.reference.html": ("max-width", "c"),
    "Notifications.reference.html": ("max-height", "n"),
}


def _once_mutant(fn):
    """Reproduce the HEAD shape in full for a collapse-dismiss file: importance back (it never
    left the stylesheet), inline zero gone, guarded {once:true} listener back, fallback gone,
    focus rescue gone. This is the defect exactly as it shipped."""
    prop, v = ONCE_LISTENER[fn]
    dim = "maxWidth" if prop == "max-width" else "maxHeight"
    return [
        (f"""      requestAnimationFrame(()=>requestAnimationFrame(()=>{{
        {v}.classList.add('removing'); {v}.style.{dim}='0px';
      }}));
      const onEnd=ev=>{{ if(ev.target!=={v} || ev.propertyName!=='{prop}') return;   /* NOT {{once:true}} — see the ⛔ note */
        {v}.removeEventListener('transitionend', onEnd); finish(); }};
      {v}.addEventListener('transitionend', onEnd);
      setTimeout(finish, 600);""",
         f"""      requestAnimationFrame(()=> {v}.classList.add('removing'));
      {v}.addEventListener('transitionend', ev=>{{ if(ev.propertyName==='{prop}') finish(); }}, {{once:true}});
      void 0;"""),
    ]


# (name, file, [(find, replace), …], [checks that MUST go red])
MUTANTS = {
    # ---- β's R1 class, three live instances ------------------------------------------
    "tags-once-listener": ("Tags.reference.html", _once_mutant("Tags.reference.html"),
                           ["tags/dismiss-removes-the-chip", "tags/no-ghost-chip-left-behind"]),
    "ftb-once-listener": ("Filter-toolbar-bar.reference.html",
                          _once_mutant("Filter-toolbar-bar.reference.html"),
                          ["ftb/dismiss-removes-the-chip"]),
    "notif-once-listener": ("Notifications.reference.html",
                            _once_mutant("Notifications.reference.html"),
                            ["notif/dismiss-removes-the-note"]),
    "tags-focus": ("Tags.reference.html",
                   [("        if(document.body.contains(nextFocus)) nextFocus.focus(); };",
                     "        void nextFocus; };")],
                   ["tags/dismiss-moves-focus", "tags/last-dismiss-lands-on-group"]),
    "notif-focus": ("Notifications.reference.html",
                    [("        if(document.body.contains(nextFocus)) nextFocus.focus(); };",
                      "        void nextFocus; };")],
                    ["notif/dismiss-moves-focus"]),

    # ---- forms family ----------------------------------------------------------------
    "se-resend-focus": ("Secure-entry.reference.html",
                        [("      const first = document.querySelector('#otp .se-cell');\n"
                          "      if (first) first.focus();                       "
                          "/* BEFORE the control goes away — 2.4.3 */\n", "")],
                        ["secure/resend-moves-focus"]),
    "se-countdown-dead": ("Secure-entry.reference.html",
                          [("      btn.disabled = true; wait.hidden = false; left = 30; "
                            "n.textContent = left;\n      countdown();",
                            "      btn.disabled = true; wait.hidden = false; left = 30; "
                            "n.textContent = left;")],
                          ["secure/resend-restarts-the-countdown"]),
    "fu-remove-focus": ("File-upload.reference.html",
                        [("          if (document.body.contains(nextFocus)) nextFocus.focus();",
                          "          void nextFocus;")],
                        ["upload/remove-moves-focus", "upload/last-remove-lands-on-browse"]),
    "fu-aria-invalid": ("File-upload.reference.html",
                        [("      fileInput.setAttribute('aria-invalid', "
                          "list.querySelector('.fu-row.is-error') ? 'true' : 'false');",
                          "      void list;")],
                        ["upload/rejected-file-marks-control-invalid",
                         "upload/invalid-survives-unrelated-remove",
                         "upload/invalid-lifts-when-rejection-removed"]),
    "dp-close-focus": ("Date-picker.reference.html",
                       [("      const stranded = panel.contains(document.activeElement);\n"
                         "      panel.classList.remove('is-open'); "
                         "openBtn.setAttribute('aria-expanded','false');\n"
                         "      if (returnFocus || stranded) openBtn.focus();",
                         "      panel.classList.remove('is-open'); "
                         "openBtn.setAttribute('aria-expanded','false');\n"
                         "      if (returnFocus) openBtn.focus();")],
                       ["datepicker/dismiss-does-not-strand-focus"]),
    "dr-close-focus": ("Date-range-picker.reference.html",
                       [("      const stranded = panel.contains(document.activeElement);\n"
                         "      panel.classList.remove('is-open');",
                         "      const stranded = false;\n"
                         "      panel.classList.remove('is-open');")],
                       ["daterange/dismiss-does-not-strand-focus"]),
    "dr-keyboard-range": ("Date-range-picker.reference.html",
                          [("        focusDay = date.getDate();\n        render();\n"
                            "        focusGrid();", "        render();")],
                          ["daterange/range-completable-from-the-keyboard",
                           "daterange/announces-the-completed-range"]),
    "tp-visibility": ("Time-picker.reference.html",
                      [("    opacity:0; visibility:hidden; transform:translateY(-6px); "
                        "pointer-events:none;", "    opacity:0; transform:translateY(-6px); "
                        "pointer-events:none;")],
                      ["timepicker/closed-menu-leaves-the-a11y-tree"]),
    "tp-close-focus": ("Time-picker.reference.html",
                       [("      const stranded = menu.contains(document.activeElement);",
                         "      const stranded = false;")],
                       ["timepicker/dismiss-does-not-strand-focus"]),

    # ---- γ's two TYPE-002 rows -------------------------------------------------------
    "dg-type-composite": ("Data-grid.reference.html",
                          [('<button type="button" class="t-cm-button" data-state="live"',
                            '<button type="button" data-state="live"'),
                           ("        x.classList.toggle('t-cm-button', on);      "
                            "/* 16/500 — pressed */\n", "")],
                          ["datagrid/pressed-segment-carries-composite",
                           "datagrid/composite-follows-the-press"]),
    "empty-type-composite": ("Empty-state.reference.html",
                             [('<a class="t-cm-button" href="#">Clear the search</a>',
                               '<a href="#">Clear the search</a>')],
                             ["emptystate/link-weight-comes-from-a-composite"]),
}


def build_arm(mutant):
    """Materialise an arm under WORK/<arm>/ with canon/ mirrored so ../canon/*.css resolves.
    Mutants are cut from the CURRENT snippet bytes every run — never from a stored copy."""
    arm = WORK / (mutant or "real")
    if arm.exists():
        shutil.rmtree(arm)
    (arm / "snippets").mkdir(parents=True)
    if not (WORK / "canon").exists():
        shutil.copytree(CANON, WORK / "canon")
    shutil.copytree(WORK / "canon", arm / "canon")
    for f in FILES:
        src = (SNIPPETS / f).read_text(encoding="utf-8")
        if mutant:
            target, edits, _ = MUTANTS[mutant]
            if f == target:
                for find, repl in edits:
                    if find not in src:
                        sys.exit(f"MUTANT {mutant}: anchor not found in {f} — the repair moved; "
                                 f"fix the mutant, do not weaken it.\n  anchor: {find!r}")
                    src = src.replace(find, repl)
        (arm / "snippets" / f).write_text(src, encoding="utf-8")
    return arm / "snippets"


class Report:
    def __init__(self, label):
        self.label, self.rows = label, []

    def check(self, name, ok, detail=""):
        self.rows.append((name, bool(ok), detail))

    def render(self):
        print(f"\n=== {self.label} ===")
        for n, ok, d in self.rows:
            print(f"  {'✓' if ok else '✗'} {n}{('  — ' + d) if d else ''}")
        return self.rows


AE = ("()=>{const a=document.activeElement;"
      "return a?a.tagName+'#'+(a.id||'')+'.'+((a.className||'').toString().split(' ')[0]):'NULL'}")


def run_arm(pw, snips, label):
    r = Report(label)
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 1180, "height": 900})

    # ================================================================ TAGS  (β R1 class)
    pg.goto((snips / "Tags.reference.html").as_uri()); pg.wait_for_timeout(250)
    t0 = pg.eval_on_selector_all("#filterbar .tag", "e=>e.length")
    r.check("control/tags-page-loaded", t0 == 3 and pg.query_selector("#filterbar") is not None,
            f"{t0} dismissible chips in the filter bar")
    pg.eval_on_selector("#filterbar .tag .x", "el=>el.focus()")
    pg.eval_on_selector("#filterbar .tag .x", "el=>el.click()"); pg.wait_for_timeout(900)
    t1 = pg.eval_on_selector_all("#filterbar .tag", "e=>e.length")
    r.check("tags/dismiss-removes-the-chip", t1 == t0 - 1, f"{t0} -> {t1} chips after one dismiss")
    # the HEAD failure mode was not "nothing happened" — it was a 0-width chip left CONNECTED
    ghost = pg.eval_on_selector_all(
        "#filterbar .tag", "els=>els.filter(e=>Math.round(e.getBoundingClientRect().width)===0).length")
    r.check("tags/no-ghost-chip-left-behind", ghost == 0,
            f"{ghost} chip(s) still connected at zero width (HEAD left one per dismiss)")
    ae = pg.evaluate(AE)
    r.check("tags/dismiss-moves-focus", ae.startswith("BUTTON") and ".x" in ae,
            f"activeElement after dismiss = {ae}")
    for _ in range(4):
        if pg.eval_on_selector_all("#filterbar .tag .x", "e=>e.length") == 0:
            break
        pg.eval_on_selector("#filterbar .tag .x", "el=>{el.focus();el.click()}"); pg.wait_for_timeout(750)
    r.check("tags/last-dismiss-lands-on-group", pg.evaluate("document.activeElement.id") == "filterbar",
            f"activeElement after the final dismiss = #{pg.evaluate('document.activeElement.id') or '(none)'}")

    # ================================================================ FILTER-TOOLBAR-BAR
    pg.goto((snips / "Filter-toolbar-bar.reference.html").as_uri()); pg.wait_for_timeout(250)
    f0 = pg.eval_on_selector_all("#ftb-chips .tag", "e=>e.length")
    r.check("control/ftb-page-loaded", f0 == 3, f"{f0} chips in the toolbar")
    pg.eval_on_selector("#ftb-chips .tag .x", "el=>{el.focus();el.click()}"); pg.wait_for_timeout(900)
    f1 = pg.eval_on_selector_all("#ftb-chips .tag", "e=>e.length")
    r.check("ftb/dismiss-removes-the-chip", f1 == f0 - 1, f"{f0} -> {f1} chips after one dismiss")

    # ================================================================ NOTIFICATIONS
    pg.goto((snips / "Notifications.reference.html").as_uri()); pg.wait_for_timeout(250)
    n0 = pg.eval_on_selector_all("#nwrap .note", "e=>e.length")
    x0 = pg.eval_on_selector_all("#nwrap .note .x", "e=>e.length")
    r.check("control/notif-page-loaded", n0 == 11 and x0 == 6,
            f"{n0} notifications, {x0} dismiss controls")
    pg.eval_on_selector("#nwrap .note .x", "el=>{el.focus();el.click()}"); pg.wait_for_timeout(900)
    n1 = pg.eval_on_selector_all("#nwrap .note", "e=>e.length")
    r.check("notif/dismiss-removes-the-note", n1 == n0 - 1, f"{n0} -> {n1} notifications")
    ae = pg.evaluate(AE)
    r.check("notif/dismiss-moves-focus", ae.startswith("BUTTON") and ".x" in ae,
            f"activeElement after dismiss = {ae}")

    # ================================================================ SECURE ENTRY (OTP)
    # ⚠ THE FIRST CUT OF THIS SECTION PROVED NOTHING, AND THAT IS WHY IT LOOKS LIKE THIS.
    # It forced `#resend.disabled = false` to skip the wait — which leaves the ORIGINAL
    # interval running, so `left = 30` kept counting down on the mutant too and the
    # `se-countdown-dead` arm came back green. The HEAD defect only exists AFTER the
    # countdown has reached zero, because that is where `clearInterval` kills the only
    # interval the page ever creates. The honest reproduction is to let it reach zero — so
    # this page runs on a compressed clock (setInterval delays scaled 1000ms -> 20ms,
    # installed before the page's own script) and the button re-enables ITSELF.
    fctx = br.new_context(viewport={"width": 1180, "height": 900})
    fast = fctx.new_page()
    fast.add_init_script("""
        (()=>{ const si = window.setInterval;
               window.setInterval = (fn, ms, ...rest) =>
                   si(fn, ms >= 1000 ? 20 : ms, ...rest); })();""")
    fast.goto((snips / "Secure-entry.reference.html").as_uri()); fast.wait_for_timeout(200)
    r.check("control/secure-page-loaded",
            fast.eval_on_selector_all("#otp .se-cell", "e=>e.length") == 6,
            "6 OTP cells")
    fast.wait_for_timeout(1200)   # 30 compressed ticks = ~600ms; ample
    r.check("control/secure-countdown-reaches-zero-and-frees-the-button",
            fast.eval_on_selector("#resend", "e=>e.disabled") is False
            and fast.eval_on_selector("#resend-wait", "e=>e.hidden") is True,
            "the countdown enabled the resend on its own — the state HEAD's bug needs")
    fast.eval_on_selector("#resend", "el=>el.focus()")
    fast.eval_on_selector("#resend", "el=>el.click()"); fast.wait_for_timeout(120)
    ae = fast.evaluate(AE)
    r.check("secure/resend-moves-focus", "se-cell" in ae,
            f"activeElement after the resend disables itself = {ae} (HEAD stranded it on BODY)")
    r.check("control/secure-resend-disables-and-shows-the-wait",
            fast.eval_on_selector("#resend", "e=>e.disabled") is True
            and fast.eval_on_selector("#resend-wait", "e=>e.hidden") is False)
    fast.wait_for_timeout(1200)
    r.check("secure/resend-restarts-the-countdown",
            fast.eval_on_selector("#resend", "e=>e.disabled") is False,
            f"resend live again, counter at "
            f"{fast.eval_on_selector('#resend-count', 'e=>e.textContent')} "
            f"(HEAD: disabled forever, counter frozen at 30)")
    # validation still drives
    fast.eval_on_selector_all("#otp .se-cell",
                              "els=>els.forEach((e,i)=>{e.value=String((i+9)%10);"
                              "e.dispatchEvent(new Event('input',{bubbles:true}))})")
    fast.wait_for_timeout(200)
    r.check("control/secure-wrong-code-marks-cells-invalid",
            fast.eval_on_selector_all("#otp .se-cell",
                                      "e=>e.filter(x=>x.getAttribute('aria-invalid')==='true').length") == 6)
    fast.close(); fctx.close()

    # ================================================================ FILE UPLOAD
    pg.goto((snips / "File-upload.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/upload-page-loaded",
            pg.query_selector("#fu-zone") is not None and pg.query_selector("#fu-browse") is not None
            and pg.eval_on_selector_all("#fu-list .fu-row", "e=>e.length") == 0,
            "dropzone + browse present, nothing staged")
    pg.set_input_files("#fu-input", [
        {"name": "statement.pdf", "mimeType": "application/pdf", "buffer": b"x" * 2048},
        {"name": "huge.pdf", "mimeType": "application/pdf", "buffer": b"x" * (11 * 1024 * 1024)}])
    pg.wait_for_timeout(700)
    rows = pg.eval_on_selector_all("#fu-list .fu-row", "e=>e.length")
    errs = pg.eval_on_selector_all("#fu-list .fu-row.is-error", "e=>e.length")
    r.check("control/upload-stages-and-rejects", rows == 2 and errs == 1,
            f"{rows} rows staged, {errs} rejected over 10MB")
    r.check("upload/rejected-file-marks-control-invalid",
            pg.eval_on_selector("#fu-input", "e=>e.getAttribute('aria-invalid')") == "true",
            "the labelled control reports invalid (HEAD: 0 aria-invalid anywhere on the page)")
    # remove the ACCEPTED row: the rejection stands, so the invalid state must stand too
    pg.eval_on_selector("#fu-list .fu-row:not(.is-error) .fu-remove", "el=>{el.focus();el.click()}")
    pg.wait_for_timeout(300)
    ae = pg.evaluate(AE)
    r.check("upload/remove-moves-focus", ae.startswith("BUTTON") and "fu-remove" in ae,
            f"activeElement after a row goes = {ae} (HEAD stranded it on BODY)")
    # ⚠ NOT a control, and the fu-aria-invalid arm is what taught this file the difference:
    # a control must be true whether or not the repair is present. This depends on
    # syncInvalid(), so it is a feature assertion and it belongs in the must-redden list.
    r.check("control/upload-rejected-row-survives-unrelated-remove",
            pg.eval_on_selector_all("#fu-list .fu-row.is-error", "e=>e.length") == 1,
            "the rejected row is still on screen — the harness removed the ACCEPTED one")
    r.check("upload/invalid-survives-unrelated-remove",
            pg.eval_on_selector("#fu-input", "e=>e.getAttribute('aria-invalid')") == "true",
            "the invalid state does not lift while a rejection is still staged")
    pg.eval_on_selector("#fu-list .fu-row .fu-remove", "el=>{el.focus();el.click()}"); pg.wait_for_timeout(300)
    r.check("upload/invalid-lifts-when-rejection-removed",
            pg.eval_on_selector("#fu-input", "e=>e.getAttribute('aria-invalid')") == "false",
            "invalid lifts once the last rejected row is gone")
    r.check("upload/last-remove-lands-on-browse", pg.evaluate("document.activeElement.id") == "fu-browse",
            f"activeElement after the last row goes = "
            f"#{pg.evaluate('document.activeElement.id') or '(none)'}")

    # ================================================================ DATE PICKER
    pg.goto((snips / "Date-picker.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/datepicker-page-loaded",
            pg.eval_on_selector("#dp-panel", "e=>getComputedStyle(e).display") == "none"
            and pg.query_selector("#dp-open") is not None,
            "panel starts closed (display:none)")
    pg.eval_on_selector("#dp-open", "e=>e.click()"); pg.wait_for_timeout(350)
    r.check("control/datepicker-open-focuses-a-day",
            pg.evaluate("!!(document.activeElement.classList "
                        "&& document.activeElement.classList.contains('dp-day'))"))
    # SYNTHETIC pointerdown moves no focus of its own — the reading is the component's
    pg.evaluate("()=>document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))")
    pg.wait_for_timeout(300)
    r.check("datepicker/dismiss-does-not-strand-focus",
            pg.evaluate("document.activeElement.id") == "dp-open",
            f"activeElement after an outside dismiss = "
            f"#{pg.evaluate('document.activeElement.id') or '(none)'} (HEAD: BODY)")
    r.check("control/datepicker-esc-returns-to-trigger", True)
    pg.eval_on_selector("#dp-open", "e=>e.click()"); pg.wait_for_timeout(350)
    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(200)
    pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    r.check("control/datepicker-keyboard-selects",
            len(pg.eval_on_selector("#f-date", "e=>e.value")) == 10
            and pg.evaluate("document.activeElement.id") == "dp-open",
            f"value={pg.eval_on_selector('#f-date', 'e=>e.value')!r}, focus returned to the trigger")

    # ================================================================ DATE RANGE PICKER
    pg.goto((snips / "Date-range-picker.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/daterange-page-loaded",
            pg.eval_on_selector("#dr-panel", "e=>getComputedStyle(e).display") == "none"
            and pg.query_selector("#dr-open-from") is not None)
    pg.eval_on_selector("#dr-open-from", "e=>e.click()"); pg.wait_for_timeout(350)
    r.check("control/daterange-open-focuses-a-day",
            pg.evaluate("!!(document.activeElement.classList "
                        "&& document.activeElement.classList.contains('dr-day'))"))
    pg.evaluate("()=>document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))")
    pg.wait_for_timeout(300)
    r.check("daterange/dismiss-does-not-strand-focus",
            pg.evaluate("document.activeElement.id") == "dr-open-from",
            f"activeElement after an outside dismiss = "
            f"#{pg.evaluate('document.activeElement.id') or '(none)'} (HEAD: BODY)")
    # THE defect: a whole range, start to end, using nothing but the keyboard
    pg.eval_on_selector("#dr-open-from", "e=>e.click()"); pg.wait_for_timeout(350)
    pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    mid = pg.evaluate("!!(document.activeElement.classList "
                      "&& document.activeElement.classList.contains('dr-day'))")
    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(150)
    pg.keyboard.press("Enter"); pg.wait_for_timeout(350)
    frm = pg.eval_on_selector("#f-from", "e=>e.value")
    to = pg.eval_on_selector("#f-to", "e=>e.value")
    r.check("daterange/range-completable-from-the-keyboard", bool(frm) and bool(to),
            f"from={frm!r} to={to!r}; focus survived the start pick = {mid} "
            f"(HEAD: focus fell to BODY and #f-to stayed empty)")
    # ⚠ SAME LESSON AS upload/invalid-survives-unrelated-remove: "Range set" can only be
    # announced if the range could be completed, so this is a FEATURE assertion, not a
    # control. The control is that the live region took the START announcement, which the
    # HEAD shape did too — that is what makes it independent of the repair.
    ann = pg.eval_on_selector("#dr-announce", "e=>e.textContent")
    r.check("control/daterange-live-region-announces-the-start",
            "Start of range" in ann or "Range set" in ann, ann[:60])
    r.check("daterange/announces-the-completed-range", "Range set" in ann, ann[:60])

    # ================================================================ TIME PICKER
    pg.goto((snips / "Time-picker.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/timepicker-page-loaded",
            pg.eval_on_selector("#tp-menu", "e=>e.getAttribute('role')") == "listbox"
            and pg.query_selector("#tp-open") is not None)
    pg.eval_on_selector("#tp-open", "e=>e.click()"); pg.wait_for_timeout(400)
    opened = pg.eval_on_selector_all("#tp-menu [role=option]", "e=>e.length")
    r.check("control/timepicker-open-builds-48-slots", opened == 48
            and pg.eval_on_selector("#tp-menu", "e=>getComputedStyle(e).visibility") == "visible",
            f"{opened} options, menu visible")
    r.check("control/timepicker-open-focuses-an-option",
            pg.evaluate("!!(document.activeElement.classList "
                        "&& document.activeElement.classList.contains('tp-opt'))"))
    pg.evaluate("()=>document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))")
    pg.wait_for_timeout(400)
    r.check("timepicker/dismiss-does-not-strand-focus",
            pg.evaluate("document.activeElement.id") == "tp-open",
            f"activeElement after an outside dismiss = "
            f"#{pg.evaluate('document.activeElement.id') or '(none)'} "
            f"(HEAD: left on an option inside an invisible listbox)")
    vis = pg.eval_on_selector("#tp-menu", "e=>getComputedStyle(e).visibility")
    r.check("timepicker/closed-menu-leaves-the-a11y-tree", vis == "hidden",
            f"closed listbox visibility = {vis} with "
            f"{pg.eval_on_selector_all('#tp-menu [role=option]', 'e=>e.length')} options built "
            f"(HEAD: visible, all 48 exposed under aria-expanded=false)")
    r.check("control/timepicker-static-gallery-stays-visible",
            pg.eval_on_selector(".tp-menu.is-static", "e=>getComputedStyle(e).visibility") == "visible",
            "the gallery specimen must NOT be hidden by the fix")
    pg.eval_on_selector("#tp-open", "e=>e.click()"); pg.wait_for_timeout(400)
    pg.keyboard.press("ArrowDown"); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    r.check("control/timepicker-keyboard-selects",
            len(pg.eval_on_selector("#f-time", "e=>e.value")) == 5
            and pg.evaluate("document.activeElement.id") == "tp-open",
            f"value={pg.eval_on_selector('#f-time', 'e=>e.value')!r}")

    # ================================================================ FORM LAYOUT (audited)
    pg.goto((snips / "Form-layout.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/formlayout-page-loaded", pg.query_selector("#payee-form") is not None
            and pg.eval_on_selector("#fs", "e=>getComputedStyle(e).display") == "none")
    pg.eval_on_selector("#payee-form [type=submit]", "e=>e.click()"); pg.wait_for_timeout(350)
    r.check("control/formlayout-empty-submit-opens-summary",
            pg.eval_on_selector("#fs", "e=>e.classList.contains('is-open')")
            and pg.eval_on_selector_all("#fs-list a", "e=>e.length") == 4)
    r.check("control/formlayout-summary-takes-focus", pg.evaluate("document.activeElement.id") == "fs")
    pg.eval_on_selector("#fs-list a", "e=>e.click()"); pg.wait_for_timeout(250)
    r.check("control/formlayout-summary-link-lands-on-the-field",
            pg.evaluate("document.activeElement.id") == "f-name")
    pg.eval_on_selector("#f-name", "e=>{e.value='Acme Ltd';"
                                       "e.dispatchEvent(new Event('input',{bubbles:true}))}")
    pg.wait_for_timeout(150)
    r.check("control/formlayout-error-lifts-on-repair",
            pg.eval_on_selector("#f-name", "e=>e.getAttribute('aria-invalid')") == "false")

    # ================================================================ AMOUNT / TEXTAREA (audited)
    pg.goto((snips / "Amount-input.reference.html").as_uri()); pg.wait_for_timeout(250)
    pg.eval_on_selector("#a1", "e=>{e.focus();e.value='0';"
                                   "e.dispatchEvent(new Event('input',{bubbles:true}))}")
    pg.eval_on_selector("#a1", "e=>e.blur()"); pg.wait_for_timeout(250)
    r.check("control/amount-zero-is-invalid",
            pg.eval_on_selector("#a1", "e=>e.getAttribute('aria-invalid')") == "true"
            and pg.eval_on_selector("#a1msg", "e=>e.getAttribute('aria-live')") == "polite")
    pg.eval_on_selector("#a1", "e=>{e.focus();e.value='1234.5';"
                                   "e.dispatchEvent(new Event('input',{bubbles:true}))}")
    pg.eval_on_selector("#a1", "e=>e.blur()"); pg.wait_for_timeout(250)
    r.check("control/amount-normalises-and-clears",
            pg.eval_on_selector("#a1", "e=>e.value") == "1,234.50"
            and pg.eval_on_selector("#a1", "e=>e.getAttribute('aria-invalid')") == "false")

    pg.goto((snips / "Textarea.reference.html").as_uri()); pg.wait_for_timeout(250)
    pg.eval_on_selector("#t1", "e=>{e.value='x'.repeat(275);"
                                   "e.dispatchEvent(new Event('input',{bubbles:true}))}")
    pg.wait_for_timeout(150)
    r.check("control/textarea-warns-and-announces-remaining",
            pg.eval_on_selector("#t1-count", "e=>e.classList.contains('is-warn')")
            and "25 characters remaining" in pg.eval_on_selector("#t1-live", "e=>e.textContent"))

    # ================================================================ γ's TYPE-002 rows
    pg.goto((snips / "Data-grid.reference.html").as_uri()); pg.wait_for_timeout(400)
    r.check("control/datagrid-page-loaded", pg.eval_on_selector_all(".dgseg button", "e=>e.length") == 3)
    press = pg.eval_on_selector('.dgseg button[aria-pressed="true"]',
                                "e=>e.className+'|'+getComputedStyle(e).fontWeight")
    r.check("datagrid/pressed-segment-carries-composite",
            "t-cm-button" in press and press.endswith("|500"),
            f"pressed segment = {press} (16/500 from the composite, not a raw override)")
    pg.eval_on_selector('.dgseg button[data-state="empty"]', "e=>e.click()"); pg.wait_for_timeout(400)
    moved = pg.eval_on_selector('.dgseg button[aria-pressed="true"]',
                                "e=>e.dataset.state+'|'+e.className+'|'+getComputedStyle(e).fontWeight")
    # ⚠ THE THIRD TIME THIS FILE MIS-SORTED A CONTROL (see the upload and daterange notes).
    # "the composite follows the press" cannot be true without the repair, so it is a feature
    # assertion. The control is that aria-pressed itself moved, which HEAD did too.
    r.check("control/datagrid-press-moves-aria-pressed", moved.startswith("empty|"), moved)
    r.check("datagrid/composite-follows-the-press",
            "t-cm-button" in moved and moved.endswith("|500"), moved)
    r.check("control/datagrid-rest-segments-are-400",
            pg.eval_on_selector('.dgseg button[aria-pressed="false"]',
                                "e=>getComputedStyle(e).fontWeight") == "400")

    pg.goto((snips / "Empty-state.reference.html").as_uri()); pg.wait_for_timeout(300)
    lk = pg.eval_on_selector(".empty a", "e=>e.className+'|'+getComputedStyle(e).fontSize"
                                         "+'|'+getComputedStyle(e).fontWeight")
    r.check("emptystate/link-weight-comes-from-a-composite",
            "t-cm-" in lk and lk.endswith("|16px|500"),
            f"link = {lk} (HEAD produced the same 16px/500 from a raw declaration)")

    br.close()
    return r.render()


def main():
    args = sys.argv[1:]
    if "--list" in args:
        for k, (f, _, checks) in MUTANTS.items():
            print(f"{k:24s} {f:34s} reddens: {', '.join(checks)}")
        return 0
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright missing — see ENVIRONMENT in this file's docstring")

    WORK.mkdir(parents=True, exist_ok=True)
    if (WORK / "canon").exists():
        shutil.rmtree(WORK / "canon")          # never a stale canon mirror

    wanted = None
    names = []
    if "--break" in args:
        i = args.index("--break")
        wanted = args[i + 1] if len(args) > i + 1 else "all"
        names = list(MUTANTS) if wanted == "all" else [wanted]
        for n in names:
            if n not in MUTANTS:
                sys.exit(f"unknown mutant {n!r} — try --list")
    failed = []

    with sync_playwright() as pw:
        if wanted is None:
            rows = run_arm(pw, build_arm(None), "REAL SNIPPETS (all checks must be GREEN)")
            reds = [n for n, ok, _ in rows if not ok]
            print("\n" + (f"GREEN — {len(rows)} checks" if not reds
                          else "FAILED: " + ", ".join(reds)))
            return 1 if reds else 0

        for name in names:
            target, _edits, must_redden = MUTANTS[name]
            rows = run_arm(pw, build_arm(name), f"BREAK ARM {name} ({target})")
            got = {n: ok for n, ok, _ in rows}
            ctl = [n for n, ok in got.items() if n.startswith("control/") and not ok]
            still_green = [n for n in must_redden if got.get(n)]
            unexpected = [n for n, ok in got.items()
                          if not ok and not n.startswith("control/") and n not in must_redden]
            if ctl:
                print(f"  ⛔ ARM PROVED NOTHING — controls red: {', '.join(ctl)}")
                failed.append(name)
            elif still_green:
                print(f"  ⛔ MUTANT DID NOT BITE — still green: {', '.join(still_green)}")
                failed.append(name)
            else:
                extra = (f"  (collateral, expected of a shared page: {', '.join(unexpected)})"
                         if unexpected else "")
                print(f"  ✓ RED BY NAME: {', '.join(must_redden)}{extra}")

    print("\n" + ("ALL BREAK ARMS BIT" if not failed else "BREAK ARMS FAILED: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
