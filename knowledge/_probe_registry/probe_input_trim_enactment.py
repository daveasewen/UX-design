#!/usr/bin/env python3
"""probe_input_trim_enactment.py — P-6: THE CANARY for text-box-trim inside FORM CONTROLS (W-45).

THE CLASS, and why this probe is a CANARY rather than a scanner. At #209 Dave ruled that the
leading-trim idiom should apply to text-bearing inputs, and the sweep landed: all 54 authored
trim blocks (and, at the same session, eleven previously blockless input-bearing snippets)
now name `input[type=text] … input:not([type]), textarea` inside the `:is(…)` vocabulary.
The declaration is ACCEPTED by the engine — `getComputedStyle(input).text-box-trim` returns
`trim-both` where it returned `none`. It is NOT ENACTED: MEASURED at #209 on Chromium
151.0.7922.34 at `line-height:2`, a `<span>` collapses 32.00px → 11.56px and a `<button>`
32.00px → 11.02px, while an `<input>` and a `<textarea>` carrying the identical declaration
both stay at 32.00px. Zero input boxes changed height across the whole sweep.

⇒ THE VOCABULARY IS INERT TODAY AND SELF-ENACTING LATER. The day a browser ships trim inside
form controls, EVERY field in the library moves — with no commit, no gate, no review and no
author. That is the defect this probe exists to catch, and it cannot be caught by reading the
repo: nothing in the repo will change. Only the BROWSER changes. So the probe asks the browser.

⛔ THE GREEN IS THE INERT STATE. findings=0 means "the engine still does not enact trim inside
form controls" — the state Dave reviewed and ruled KEEP on. findings=1 is the DAY IT CHANGES:
the class named in the finding is "browser began enacting text-box-trim in form controls —
every field in the library will move; Dave's review is owed BEFORE shipping". This inversion is
deliberate and is the whole point of a canary; it is stated here so no reader can mistake the
red for a regression in this repo.

WHAT IT MEASURES — a minimal, self-contained fixture (no repo file, no network), rendered in a
real browser. Three SUBJECTS, each rendered TWICE, identical but for the trim declaration:
    · `<span>`      — the POSITIVE CONTROL. The engine is KNOWN to trim this.
    · `<input type=text>` — the subject under watch.
    · `<textarea>`  — the subject under watch.
Same font stack as the library, `line-height:2`, zero padding/border, so the box height tracks
the leading and nothing else. The verdict is per-subject: `trimmed_height` vs `untrimmed_height`.

THE THRESHOLD, declared, not tuned: a subject counts as ENACTED when its box shrinks by
>= 1.00 CSS px AND >= 5% of its untrimmed height (`SHRINK_PX` / `SHRINK_FRAC`). Both arms,
because either alone lies at some size. The floor is set well above the #209 noise: the sweep's
largest measured movement on any real input was 0.75 CSS px of INK CENTRE with the box height
changing by exactly 0.00, so 1px + 5% cannot be reached by antialiasing. The span control at
#209 shrank 64%, so the enacted signal is an order of magnitude clear of the floor.

⛔ THE CONTROL IS LOAD-BEARING, AND ITS FAILURE IS A REFUSAL, NOT A PASS. If the `<span>`
control does NOT shrink, this engine does not enact `text-box-trim` on ANYTHING — so the
question "does it enact trim inside a form control?" was never asked, and a findings=0 here
would be a browser-capability fact wearing a green. That path exits **77 COULD-NOT-ASK**
(`knowledge/_could_not_ask.py`, #193) naming the control's own numbers. An environment fact
must never wear a red [[honest-refusal-needs-a-legal-form]] — and it must never wear a green
either [[feedback-measuring-tool-must-not-guess]].

⛔ WHAT IT CANNOT SEE:
  · WHICH library components would move, or by how much — it measures the MECHANISM on a
    fixture, not the 65 snippets. When it fires, the size of the change is still to be measured.
  · Engines other than the one this environment can launch (Chromium only, here). A Gecko or
    WebKit enactment lands unseen until this probe runs somewhere with that engine.
  · Partial enactment — an engine that trims `<textarea>` but not `<input>` is caught (the
    subjects are independent), but an engine that trims only SOME input types is not: the
    fixture carries `type=text`, the representative case, not all seven typed inputs.
  · Whether the ENACTED result is DESIRABLE. That is Dave's eye, which is exactly what the
    finding asks for. The probe never rules the design.
  · Anything about the authored CSS. A future lane that REMOVES the input vocabulary from the
    snippets does not silence this probe — the fixture carries its own declaration. That is
    deliberate: the canary watches the ENGINE, and the repo's own state is the static gates' job.

⛔ ENVIRONMENT SPLIT, DECLARED (#173): needs Chromium + Playwright per
`knowledge/_RUNBOOK-render-verify.md`. Runs in the SANDBOX today; UNPROVEN in CI, exactly as
P-3 is (`s204-D1` item 5 owns the CI render leg). Browser lookup is ROOTS × LAYOUTS + the
driver's own `executable_path`, the #209 shape P-3 was repaired into — one hardcoded leaf is
how a probe refuses in the one job that HAS a browser. Env vars (runbook §sandbox):
    PYTHONPATH=/var/tmp/pylibs-<n>  PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-<n>
    LD_LIBRARY_PATH=/var/tmp/chromelibs-<n>/root/usr/lib/aarch64-linux-gnu  TMPDIR=/var/tmp

USAGE
  python3 knowledge/_probe_registry/probe_input_trim_enactment.py --check
  python3 knowledge/_probe_registry/probe_input_trim_enactment.py --check --verbose
  python3 knowledge/_probe_registry/probe_input_trim_enactment.py --selftest
EXIT: 0 clean (still inert — the reviewed state) · 1 findings (ENACTMENT MEASURED — Dave's
review owed) · 77 COULD-NOT-ASK (no browser, or an engine that trims nothing at all).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import glob as globmod, os, shutil, subprocess, sys, tempfile
import _could_not_ask as cna  # noqa: E402 — the #193 convention: 77 + a `COULD-NOT-ASK:` line

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# THE ENACTMENT THRESHOLD — declared in one place so the selftest and the report share it.
SHRINK_PX = 1.00     # absolute floor: #209's largest real-input movement was 0.75px INK, 0.00 box
SHRINK_FRAC = 0.05   # relative floor: the span control shrank 64% at #209

# The declaration under watch, in the library's own words (knowledge/snippets/*.reference.html).
TRIM_DECL = "text-box-trim:trim-both;text-box-edge:cap alphabetic;"
FONT_STACK = '"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif'

# ⛔ THE SUBJECT TAG IS A PARAMETER, and that is the mutation control's whole hinge.
# `--simulate-enactment` renders the watched subject as a `<span>` — an element this engine
# DOES trim — so the finding path is driven by the SAME measurement code on a REAL browser,
# not by asserting a clause [[mutation-tests-the-clause-not-the-feature]]. A canary that cannot
# be made to sing is [[instrument-without-a-consumer]].
SUBJECTS = ("input", "textarea")


def fixture_html(simulate=False):
    """The whole page, self-contained: no repo file, no network, no font download."""
    def cell(key, tag, trimmed):
        cls = "trim" if trimmed else "notrim"
        eid = "%s-%s" % (key, cls)
        if tag == "input":
            el = '<input id="%s" class="probe %s" type="text" value="Handgloves">' % (eid, cls)
        elif tag == "textarea":
            el = '<textarea id="%s" class="probe %s" rows="1">Handgloves</textarea>' % (eid, cls)
        else:
            el = '<span id="%s" class="probe %s">Handgloves</span>' % (eid, cls)
        return '<div class="row">%s</div>' % el

    rows = [cell("control", "span", False), cell("control", "span", True)]
    for s in SUBJECTS:
        tag = "span" if simulate else s
        rows.append(cell(s, tag, False))
        rows.append(cell(s, tag, True))
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>P-6 text-box-trim enactment fixture</title>
<style>
  *{box-sizing:content-box;}
  body{margin:0;padding:0;background:#FFFFFF;color:#1A1A1A;}
  .row{margin:0;padding:0;}
  .probe{font-family:%s;font-size:16px;font-weight:400;line-height:2;
         display:block;margin:0;padding:0;border:0;background:#FFFF00;
         width:220px;overflow:hidden;resize:none;}
  .trim{%s}
</style></head><body>%s</body></html>""" % (FONT_STACK, TRIM_DECL, "\n".join(rows))


JS = r"""
() => {
  const out = {};
  for (const el of document.querySelectorAll('.probe')) {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    out[el.id] = {h: +r.height.toFixed(2), tag: el.tagName.toLowerCase(),
                  computed: (cs.getPropertyValue('text-box-trim') ||
                             cs.getPropertyValue('text-box') || '').trim()};
  }
  return out;
}
"""

_LAYOUTS = ("chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell",
            "chromium_headless_shell-*/chrome-linux/headless_shell",
            "chromium-*/chrome-linux64/chrome",
            "chromium-*/chrome-linux/chrome")


def _browser_roots():
    roots = []
    env = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "").strip()
    if env:                                   # honoured FIRST — an explicit WHERE outranks ours
        roots.append(env)
    roots.append(os.path.expanduser("~/.cache/ms-playwright"))
    roots += sorted(globmod.glob("/var/tmp/pw-browsers-*"))
    return roots


def _browser_env(roots=None, allow_own=True):
    """Return (launcher_kwargs, refusal). A missing browser is a DECLARED refusal, never a pass.

    `roots` / `allow_own` are injection points for the selftest's refusal arm: pointing at an
    empty root with the driver's own resolution disabled TAKES THE INPUT AWAY, which is the only
    thing a refusal may be keyed on (`_could_not_ask.py` — never on "am I in CI")."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, ("NOT-IN-THIS-ENVIRONMENT: playwright is not importable. Stage it per "
                      "knowledge/_RUNBOOK-render-verify.md (PYTHONPATH=/var/tmp/pylibs-<n>). "
                      "REFUSED — not a pass.")
    roots = _browser_roots() if roots is None else list(roots)
    for root in roots:
        for layout in _LAYOUTS:
            hits = sorted(globmod.glob(os.path.join(root, layout)))
            if hits:
                return {"executable_path": hits[0]}, None
    own = "not consulted (allow_own=False)"
    if allow_own:
        try:
            with sync_playwright() as p:
                own = p.chromium.executable_path
            if own and os.path.exists(own):
                return {}, None
        except Exception as e:
            own = "unavailable (%s: %s)" % (type(e).__name__, str(e)[:80])
    return None, ("NOT-IN-THIS-ENVIRONMENT: no chromium binary found. Looked for %d layout(s) "
                  "%s under root(s) %s, and playwright's own executable_path was %s. "
                  "REFUSED — not a pass." % (len(_LAYOUTS), list(_LAYOUTS), roots, own or "empty"))


def measure(simulate=False, roots=None, allow_own=True):
    """Render the fixture and return (readings, refusal). Readings are RAW heights, by id."""
    kwargs, refusal = _browser_env(roots=roots, allow_own=allow_own)
    if refusal:
        return None, refusal
    from playwright.sync_api import sync_playwright
    tmp = tempfile.mkdtemp(prefix="p6-fixture-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    path = os.path.join(tmp, "fixture.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(fixture_html(simulate=simulate))
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True,
                                  args=["--no-sandbox", "--disable-dev-shm-usage",
                                        "--disable-gpu"], **kwargs)
            pg = b.new_page(viewport={"width": 640, "height": 640})
            pg.goto("file://" + path)
            # SETTLE BEFORE READING (runbook 2026-07-27): a value read in the same task as a
            # class change is the PRE-transition value.
            pg.add_style_tag(content="*{transition:none!important;animation:none!important}")
            pg.wait_for_timeout(200)
            readings = pg.evaluate(JS)
            b.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return readings, None


def _verdict_for(readings, key):
    """(enacted, before_h, after_h, delta, frac) for one subject — the threshold in ONE place."""
    a = readings.get("%s-notrim" % key)
    b = readings.get("%s-trim" % key)
    if not a or not b:
        return None, None, None, None, None
    before, after = a["h"], b["h"]
    delta = round(before - after, 2)
    frac = (delta / before) if before else 0.0
    return (delta >= SHRINK_PX and frac >= SHRINK_FRAC), before, after, delta, frac


def check(simulate=False, verbose=False, roots=None, allow_own=True):
    readings, refusal = measure(simulate=simulate, roots=roots, allow_own=allow_own)
    if refusal:
        rc = cna.refuse("P-6 text-box-trim enactment canary", refusal)
        print("PROBE P-6 — findings=UNKNOWN (environment refused, exit %d)" % rc)
        return rc

    c_enacted, c_before, c_after, c_delta, c_frac = _verdict_for(readings, "control")
    if c_enacted is None:
        print("⛔ THE FIXTURE DID NOT RENDER ITS CONTROL — nothing was measured.")
        print("PROBE P-6 — findings=1")
        return 1
    print("P-6 text-box-trim enactment canary%s · threshold: shrink >= %.2f CSS px AND >= %.0f%%"
          % (" [SIMULATED ENACTMENT]" if simulate else "", SHRINK_PX, SHRINK_FRAC * 100))
    print("  CONTROL <span>            %6.2f → %6.2f px (Δ %5.2f, %4.1f%%) computed=%r"
          % (c_before, c_after, c_delta, c_frac * 100, readings["control-trim"]["computed"]))
    if not c_enacted:
        # ⛔ NOT A PASS AND NOT A RED: this engine does not enact trim on ANYTHING, so the
        # question about form controls was never asked. Keyed on the measured capability, which
        # IS the unreachable input here — never on the runner's identity.
        rc = cna.refuse("P-6 text-box-trim enactment canary",
                        "NOT-IN-THIS-ENVIRONMENT: the positive control did not move — a <span> "
                        "carrying `%s` measured %.2f → %.2f px (Δ %.2f, %.1f%%), below the "
                        "%.2fpx/%.0f%% floor. This engine does not enact text-box-trim on ANY "
                        "element, so it cannot be asked whether it enacts it inside a form "
                        "control. A findings=0 here would be a browser-capability fact wearing "
                        "a green. REFUSED — not a pass."
                        % (TRIM_DECL, c_before, c_after, c_delta, c_frac * 100,
                           SHRINK_PX, SHRINK_FRAC * 100))
        print("PROBE P-6 — findings=UNKNOWN (control dead, exit %d)" % rc)
        return rc

    findings = []
    for key in SUBJECTS:
        enacted, before, after, delta, frac = _verdict_for(readings, key)
        shown = readings.get("%s-trim" % key, {}).get("tag", "?")
        print("  SUBJECT <%-9s> %-10s %6.2f → %6.2f px (Δ %5.2f, %4.1f%%) computed=%r  %s"
              % (key, ("[as <%s>]" % shown) if shown != key else "",
                 before, after, delta, frac * 100,
                 readings["%s-trim" % key]["computed"],
                 "⛔ ENACTED" if enacted else "INERT (the reviewed state)"))
        if enacted:
            findings.append((key, before, after, delta, frac))

    for key, before, after, delta, frac in findings:
        print("  ⛔ FINDING — BROWSER BEGAN ENACTING text-box-trim IN FORM CONTROLS: <%s> "
              "carrying `%s` shrank %.2f → %.2f px (Δ %.2f, %.1f%%) where the #209 baseline "
              "measured NO movement at all. EVERY FIELD IN THE LIBRARY WILL MOVE — the "
              "vocabulary is authored in 65 snippet trim blocks and in canon.css, so this "
              "lands with no commit and no author. DAVE'S REVIEW IS OWED BEFORE SHIPPING "
              "(W-61 asked exactly this question and he ruled KEEP on the INERT reading)."
              % (key, TRIM_DECL, before, after, delta, frac * 100))
    if not findings:
        print("  ✅ still inert — the state Dave reviewed at #209 and ruled KEEP on. The "
              "authored vocabulary changes nothing a user can see, today, in this engine.")
    if verbose:
        print("  raw readings: %s" % readings)
    print("PROBE P-6 — findings=%d" % len(findings))
    return 1 if findings else 0


def selftest():
    """THREE ARMS, each DRIVING THE REAL BROWSER through the real measurement path:
      GREEN   — the real fixture must report findings=0 (today's inert state is the pass).
      FIRE    — the watched subject is rendered as a <span>, an element this engine DOES trim,
                which is enactment simulated at the only place it can be: the ELEMENT. The
                probe must report a finding on BOTH watched subjects and rc=1.
      REFUSE  — with the browser taken away the probe must exit 77 with a COULD-NOT-ASK line,
                proven BOTH in-process (empty roots, driver resolution off) and END-TO-END in a
                subprocess whose `playwright` import is shadowed by a stub that cannot load.
    """
    fails = []
    kwargs, refusal = _browser_env()
    if refusal:
        rc = cna.refuse("P-6 selftest", refusal)
        print("   This is a DECLARED environment gap (#173), reported as rc=%d COULD-NOT-ASK — "
              "never a pass, and distinguishable from the rc=1 a real red returns." % rc)
        return rc

    # ARM 1 — GREEN CONTROL. The real subjects, the real fixture.
    print("  · ARM 1 GREEN — real <input>/<textarea> subjects:")
    rc_green = check(simulate=False)
    if rc_green != 0:
        fails.append("GREEN CONTROL DID NOT HOLD: the real fixture returned rc=%d, so either "
                     "this engine has started enacting trim in form controls (a REAL finding, "
                     "not a test failure — read the output above) or the probe is miscalibrated"
                     % rc_green)

    # ARM 2 — MUTATION: simulate the enactment and require the canary to SING.
    print("\n  · ARM 2 FIRE — the watched subjects rendered as <span>, i.e. an element this "
          "engine really does trim (enactment, simulated at the element):")
    rc_fire = check(simulate=True)
    if rc_fire != 1:
        fails.append("CANARY CANNOT SING: with the subjects rendered as a genuinely-trimmed "
                     "element the probe returned rc=%d, not 1. A canary that cannot be made to "
                     "fire is an instrument without a consumer" % rc_fire)
    else:
        print("  ✅ the finding path is REACHABLE and was driven in a real browser, not asserted")

    # ARM 3a — REFUSAL, in process, with the input taken away rather than a flag set.
    empty = tempfile.mkdtemp(prefix="p6-noroots-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    rc_ref = check(roots=[empty], allow_own=False)
    shutil.rmtree(empty, ignore_errors=True)
    if rc_ref != cna.EXIT:
        fails.append("REFUSAL ARM: with no browser root reachable the probe returned rc=%d, "
                     "not %d — an environment fact must never wear a red" % (rc_ref, cna.EXIT))
    else:
        print("\n  ✅ refusal arm (in-process): no reachable root ⇒ rc=%d COULD-NOT-ASK"
              % cna.EXIT)

    # ARM 3b — REFUSAL, END TO END. Shadow `playwright` with a package that cannot import, run
    # the probe as a subprocess, and read the exit code and the marked line a consumer reads.
    shim = tempfile.mkdtemp(prefix="p6-shim-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    os.makedirs(os.path.join(shim, "playwright"))
    with open(os.path.join(shim, "playwright", "__init__.py"), "w") as fh:
        fh.write("raise ImportError('P-6 selftest: playwright removed from this environment')\n")
    env = dict(os.environ)
    env["PYTHONPATH"] = shim + os.pathsep + env.get("PYTHONPATH", "")
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--check"],
                       cwd=ROOT, capture_output=True, text=True, env=env)
    shutil.rmtree(shim, ignore_errors=True)
    out = (p.stdout or "") + (p.stderr or "")
    reason = cna.reason_in(out)
    if p.returncode != cna.EXIT or not reason:
        fails.append("END-TO-END REFUSAL ARM: with `playwright` shadowed by an unimportable "
                     "stub the probe exited %d (want %d) and %s a `COULD-NOT-ASK:` line — "
                     "the registry runner buckets on BOTH halves"
                     % (p.returncode, cna.EXIT, "carried" if reason else "did NOT carry"))
    else:
        print("  ✅ refusal arm (end-to-end): playwright unimportable ⇒ rc=%d + %r"
              % (p.returncode, reason[:90]))

    # HELP GATE — the #158 class: every entry point answers --help before doing any work.
    h = subprocess.run([sys.executable, os.path.abspath(__file__), "--help"],
                       cwd=ROOT, capture_output=True, text=True)
    if h.returncode != 0 or "CANARY" not in h.stdout:
        fails.append("HELP GATE: --help exited %d and %s the docstring"
                     % (h.returncode, "printed" if "CANARY" in h.stdout else "did NOT print"))
    else:
        print("  ✅ help gate: --help exits 0 with the docstring, writing nothing")

    if fails:
        print("\n⛔ P-6 selftest: %d failure(s)" % len(fails))
        for f in fails:
            print("   " + f)
        return 1
    print("\n✅ P-6 selftest PASS — the inert state reads GREEN, a simulated enactment MAKES "
          "THE CANARY SING (rc=1) in a real browser, and a browser taken away REFUSES with "
          "rc=%d in-process AND end-to-end." % cna.EXIT)
    return 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    sys.exit(check(simulate="--simulate-enactment" in argv, verbose="--verbose" in argv))
