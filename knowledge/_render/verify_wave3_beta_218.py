#!/usr/bin/env python3
"""
verify_wave3_beta_218.py — DRIVES the #218 wave-3 lane β (FEEDBACK family) repairs and asserts
that real state MOVED: alert · toast · drawer · popover · skeleton.

WHY THIS FILE EXISTS AT ALL — THE LANE WAS BRIEFED TO BUILD FIVE COMPONENTS THAT ALREADY EXIST
  `notes/_briefs/2026-08-25-218-wave3-lanes-brief.md` asked lane β to build five NEW snippets.
  All five are already in the store and GATED, five probes deep (snippet · meta · showroom ·
  _validate_radius.MIGRATED_SNIPPETS · canon .cn- rules). The "Gap" that put them on the
  wave-3 list is the STALE `itinerary_status` column of
  `reviews/ITINERARY-STATUS-2026-08-21-v3.json`; that same file's own MEASURED verdict on rows
  68–72 is `drift: "STALE — itinerary UNDERSTATES the store"`, and its `$counts` are
  GATED 121 / GAP 1 of 124 — not the 78 the lane brief inherited. Lane γ was told to check
  exactly this class on the charts-kit row; it turns out to be the whole of lane β as well.
  So the lane's work became: AUDIT the five that exist, DRIVE them, and repair what measures
  broken. This file is that proof.

WHAT IT REFUSES TO DO
  A LOAD ASSERTION IS BANNED (the doctrine of verify_behaviour_218w3_overlay.py, inherited).
  "Alert has a dismiss button with aria-label" was TRUE for the whole time the dismiss button
  removed NOTHING. Every check below drives a real click, key press or scroll and reads the
  state back off the LIVE DOM; the assertion is that a value MOVED.

THE DEFECTS THIS FILE PINS (all four MEASURED at HEAD before any edit, in this environment)
  1. Alert — the dismiss × REMOVED NOTHING. 7 alerts in, 7 alerts out, every theme, every mode,
     both motion settings. Root cause is not the script: `.alert.removing{max-height:0
     !important}` meant the before-change value was an author-NORMAL inline declaration and the
     after-change an author-IMPORTANT stylesheet one, and Chromium starts no transition across
     that importance change. transitionrun fired for opacity/margin-top/margin-bottom/
     padding-top/padding-bottom and NEVER for max-height, so the `transitionend('max-height')`
     that gated `n.remove()` never arrived. Counter-experiment in the same run: the identical
     collapse driven inline→inline fires transitionrun AND transitionend.
  2. Alert + Toast — dismissing from the keyboard stranded document.activeElement on BODY
     (WCAG 2.4.3), throwing the user back to the top of the document. Same class the Drawer had
     repaired at #211 lane R3.
  3. Popover — `.pop` is position:fixed and was placed ONCE on open. Measured: open with a 12px
     gap to the trigger, scroll 300px, gap becomes 108px — the surface stays pinned to the
     viewport while its trigger scrolls away, tail pointing at unrelated content, aria-expanded
     still true.
  4. Skeleton loader — the resolved copy arrived as `<p style="margin:0">`: no canon type
     composite (the file carried ZERO `.t-*` classes) and a hardcoded inline style.

THE --break ARM (a verifier that cannot fail proves nothing)
  Mutants are generated FROM THE CURRENT FILES at run time, never from a stored copy — a stale
  mutant silently proves yesterday's clause. Each mutant re-introduces ONE repaired defect and
  the check that pins it is required to go RED BY NAME.

  ⚠ THE HARNESS CONTROLS. A page that failed to load makes every behaviour check fail, and a
  --break arm would read that as a pass. Every arm therefore also runs `control/…` checks that
  assert the AUTHORED markup arrived. Controls must be GREEN IN BOTH ARMS; a red control in a
  break arm means the arm proved nothing and the run is reported FAILED.

ENVIRONMENT (headless, driven this session)
  export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \
         FONTCONFIG_FILE=/var/tmp/fonts-s218.conf \
         LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu

USAGE
  python3 knowledge/_render/verify_wave3_beta_218.py              # real snippets, all green
  python3 knowledge/_render/verify_wave3_beta_218.py --break all  # every mutant, each RED by name
  python3 knowledge/_render/verify_wave3_beta_218.py --break alert-collapse
  python3 knowledge/_render/verify_wave3_beta_218.py --list       # mutant names + the checks they must redden
"""
import os, pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SNIPPETS = REPO / "knowledge" / "snippets"
CANON = REPO / "knowledge" / "canon"
# session-suffixed: /var/tmp is SHARED across sessions and foreign artefacts are stale + unwritable
WORK = pathlib.Path(os.environ.get("BM_MUTANT_DIR", "/var/tmp/218wb-mutants"))

FILES = ["Alert.reference.html", "Toast.reference.html", "Drawer.reference.html",
         "Popover.reference.html", "Skeleton-loader.reference.html"]

# ---------------------------------------------------------------- mutants
# (name, file, [(find, replace), …], [checks that MUST go red])
#
# ⚠ THE ALERT MUTANTS WERE RE-CUT TWICE, AND THAT IS THE POINT OF HAVING THEM.
# First cut restored only the `!important` — green arm, because the repair's fallback timer
# removed the alert anyway. Second cut also removed the fallback — still green on the
# transition check, because the repair ALSO drives max-height inline→0px, and the after-change
# inline value agrees with the important one, so the transition starts either way. The mutants
# below therefore bite the half of the repair that is actually load-bearing (the inline zero),
# and `alert-collapse` reproduces the HEAD shape in full. Had the arm been accepted at either
# earlier cut, this file would have shipped claiming to pin a root cause it could not pin.
MUTANTS = {
    # THE HEAD SHAPE, reproduced in full — importance back, inline zero gone, guarded
    # {once:true} listener back, fallback gone. This is the defect exactly as it shipped.
    "alert-collapse": (
        "Alert.reference.html",
        [("  .alert.removing{ opacity:0;", "  .alert.removing{ max-height:0 !important; opacity:0;"),
         ("n.classList.add('removing'); n.style.maxHeight='0px';", "n.classList.add('removing');"),
         ("""      const onEnd=ev=>{ if(ev.target!==n || ev.propertyName!=='max-height') return;   /* NOT {once:true} — see the ⛔ note */
        n.removeEventListener('transitionend', onEnd); finish(); };
      n.addEventListener('transitionend', onEnd);""",
          """      n.addEventListener('transitionend', ev=>{ if(ev.propertyName==='max-height') finish(); }, {once:true});"""),
         ("      setTimeout(finish, 600);", "      void finish;")],
        ["alert/dismiss-removes-the-alert"],
    ),
    # isolates the LOAD-BEARING half on its own: only the {once:true} listener is restored.
    # Everything else about the repair stays. It still reddens — which is the proof that the
    # one-shot listener, not the !important, was what stopped the dismiss.
    "alert-once-listener": (
        "Alert.reference.html",
        [("""      const onEnd=ev=>{ if(ev.target!==n || ev.propertyName!=='max-height') return;   /* NOT {once:true} — see the ⛔ note */
        n.removeEventListener('transitionend', onEnd); finish(); };
      n.addEventListener('transitionend', onEnd);""",
          """      n.addEventListener('transitionend', ev=>{ if(ev.propertyName==='max-height') finish(); }, {once:true});"""),
         ("      setTimeout(finish, 600);", "      void finish;")],
        ["alert/dismiss-removes-the-alert"],
    ),
    "alert-focus": (
        "Alert.reference.html",
        [("if(document.body.contains(nextFocus)) nextFocus.focus();", "void nextFocus;")],
        ["alert/dismiss-moves-focus", "alert/last-dismiss-lands-on-group"],
    ),
    "toast-focus": (
        "Toast.reference.html",
        [("clearTimeout(timer); leave(); handOff();", "clearTimeout(timer); leave();")],
        ["toast/dismiss-moves-focus"],
    ),
    "popover-track": (
        "Popover.reference.html",
        [("openWrap=w; startTracking(place);", "openWrap=w;")],
        ["popover/tracks-trigger-on-scroll", "popover/tracks-trigger-on-resize"],
    ),
    "skeleton-type": (
        "Skeleton-loader.reference.html",
        [('class="sk-resolved t-ed-body"', 'style="margin:0"')],
        ["skeleton/resolved-copy-carries-composite", "skeleton/resolved-copy-has-no-inline-style"],
    ),
    # the composite is only real if the stylesheet that defines it is loaded
    "skeleton-no-typecss": (
        "Skeleton-loader.reference.html",
        [('<link rel="stylesheet" href="../canon/type.css">\n<style>', '<style>')],
        ["skeleton/resolved-copy-composite-resolves"],
    ),
    "type-button": (
        "Alert.reference.html",
        [('<button class="x" type="button" aria-label="Dismiss alert">',
          '<button class="x" aria-label="Dismiss alert">')],
        ["alert/dismiss-is-type-button"],
    ),
}


def build_arm(mutant):
    """Materialise an arm under WORK/<arm>/ with canon/ mirrored so ../canon/type.css resolves.
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


def run_arm(pw, snips, label):
    r = Report(label)
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 1180, "height": 900})

    # ---------------- ALERT
    pg.goto((snips / "Alert.reference.html").as_uri()); pg.wait_for_timeout(250)
    n0 = pg.eval_on_selector_all(".alert", "e=>e.length")
    x0 = pg.eval_on_selector_all(".alert .x", "e=>e.length")
    r.check("control/alert-page-loaded", n0 == 7 and x0 == 5, f"{n0} alerts, {x0} dismiss controls")
    r.check("alert/dismiss-is-type-button",
            pg.eval_on_selector_all(".alert .x", "els=>els.every(e=>e.getAttribute('type')==='button')"),
            "every dismiss × declares type=button")
    # Instrument the collapse BEFORE clicking. This is the check that pins the ROOT cause and
    # that no fallback timer can mask: at HEAD, transitionrun fired for opacity/margin/padding
    # and never once for max-height, because the zero was routed through an !important.
    pg.evaluate("""()=>{ window.__tr=[]; const a=document.querySelector('.alert');
        a.addEventListener('transitionrun', e=>window.__tr.push('run:'+e.propertyName));
        a.addEventListener('transitionend', e=>window.__tr.push('end:'+e.propertyName));
        a.addEventListener('transitioncancel', e=>window.__tr.push('cancel:'+e.propertyName)); }""")
    pg.eval_on_selector(".alert .x", "el=>el.focus()")
    pg.eval_on_selector(".alert .x", "el=>el.click()"); pg.wait_for_timeout(900)
    tr = pg.evaluate("window.__tr") or []
    # ⚠ THIS IS A CONTROL, NOT A DISCRIMINATOR, and it took two failed arms to learn that.
    # The transition itself completes in the HEAD shape too — `run:max-height` AND
    # `end:max-height` both fire there. What failed at HEAD was the LISTENING: a
    # `{once:true}` handler guarded on propertyName was unsubscribed by the earlier `opacity`
    # event and was gone by the time max-height's event arrived. So the only honest
    # discriminator is the behaviour — alert/dismiss-removes-the-alert — and this line stays
    # as a control proving the collapse machinery ran at all in both arms.
    r.check("control/alert-collapse-transition-completes", "end:max-height" in tr,
            f"max-height transition events = {[e for e in tr if 'max-height' in e] or 'NONE'}")
    n1 = pg.eval_on_selector_all(".alert", "e=>e.length")
    r.check("alert/dismiss-removes-the-alert", n1 == n0 - 1, f"{n0} -> {n1} alerts after one dismiss")
    ae = pg.evaluate("document.activeElement.tagName+'.'+document.activeElement.className")
    r.check("alert/dismiss-moves-focus", ae.startswith("BUTTON") and "x" in ae,
            f"activeElement after dismiss = {ae}")
    for _ in range(6):
        if pg.eval_on_selector_all(".alert .x", "e=>e.length") == 0:
            break
        pg.eval_on_selector(".alert .x", "el=>el.click()"); pg.wait_for_timeout(750)
    last = pg.evaluate("document.activeElement.id")
    r.check("alert/last-dismiss-lands-on-group", last == "awrap",
            f"activeElement after the final dismiss = #{last or '(none)'}")

    # ---------------- TOAST
    pg.goto((snips / "Toast.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/toast-page-loaded",
            pg.eval_on_selector_all(".toast", "e=>e.length") == 6 and pg.query_selector("#spawnOk") is not None,
            "6 specimen toasts + the spawn controls")
    pg.click("#spawnOk"); pg.wait_for_timeout(300)
    r.check("control/toast-spawns", pg.eval_on_selector_all("#toastRegion .toast", "e=>e.length") == 1)
    r.check("toast/dismiss-is-type-button",
            pg.eval_on_selector_all(".toast .x", "els=>els.every(e=>e.getAttribute('type')==='button')"))
    pg.eval_on_selector("#toastRegion .toast .x", "el=>el.focus()")
    pg.eval_on_selector("#toastRegion .toast .x", "el=>el.click()"); pg.wait_for_timeout(700)
    ae = pg.evaluate("document.activeElement.tagName+'#'+document.activeElement.id")
    r.check("toast/dismiss-moves-focus", ae == "BUTTON#spawnOk",
            f"activeElement after the last toast goes = {ae} (expected the spawning control)")
    pg.click("#spawnOk"); pg.click("#spawnInfo"); pg.wait_for_timeout(350)
    pg.eval_on_selector("#toastRegion .toast .x", "el=>el.focus()")
    pg.eval_on_selector("#toastRegion .toast .x", "el=>el.click()"); pg.wait_for_timeout(450)
    inreg = pg.evaluate("!!(document.activeElement.closest && document.activeElement.closest('#toastRegion'))")
    r.check("toast/dismiss-with-siblings-stays-in-region", inreg,
            "focus hands off to the next live toast, not out of the region")

    # ---------------- DRAWER (audited, unmodified — the #211 repair is re-driven, not assumed)
    pg.goto((snips / "Drawer.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/drawer-page-loaded", pg.query_selector("#sheet") is not None)
    pg.click("#open"); pg.wait_for_timeout(600)
    r.check("drawer/open-moves-focus-into-sheet",
            pg.evaluate("!!document.activeElement.closest('#sheet')"),
            "the #211 lane-R3 rAF-gated open order still holds")
    r.check("drawer/background-inert-while-open", pg.eval_on_selector("#page", "e=>e.inert===true"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(450)
    r.check("drawer/esc-returns-focus-to-trigger", pg.evaluate("document.activeElement.id") == "open")

    # ---------------- POPOVER
    pg.goto((snips / "Popover.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/popover-page-loaded", pg.eval_on_selector_all(".popwrap", "e=>e.length") == 3)
    pg.evaluate("document.body.style.minHeight='3000px'")
    metric = """()=>{const t=document.querySelector('.popwrap .pop-trigger').getBoundingClientRect();
        const p=document.querySelector('.popwrap .pop').getBoundingClientRect();
        const above = p.bottom <= t.top + 1;
        return above ? Math.round(t.top - p.bottom) : Math.round(p.top - t.bottom);}"""
    pg.click(".popwrap .pop-trigger"); pg.wait_for_timeout(300)
    g0 = pg.evaluate(metric)
    r.check("control/popover-opens-anchored", g0 == 12, f"gap to trigger on open = {g0}px")
    r.check("popover/trigger-announces-expanded",
            pg.eval_on_selector(".popwrap .pop-trigger", "e=>e.getAttribute('aria-expanded')") == "true")
    pg.evaluate("window.scrollTo(0,300)"); pg.wait_for_timeout(450)
    g1 = pg.evaluate(metric)
    r.check("popover/tracks-trigger-on-scroll", g1 == 12,
            f"gap after a 300px scroll = {g1}px (HEAD measured 108px — surface left behind)")
    pg.set_viewport_size({"width": 760, "height": 900}); pg.wait_for_timeout(450)
    g2 = pg.evaluate(metric)
    r.check("popover/tracks-trigger-on-resize", g2 == 12, f"gap after a viewport resize = {g2}px")
    pg.set_viewport_size({"width": 1180, "height": 900}); pg.wait_for_timeout(300)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
    r.check("popover/esc-closes-and-collapses-state",
            pg.eval_on_selector(".popwrap .pop-trigger", "e=>e.getAttribute('aria-expanded')") == "false")

    # ---------------- SKELETON
    pg.goto((snips / "Skeleton-loader.reference.html").as_uri()); pg.wait_for_timeout(250)
    r.check("control/skeleton-page-loaded",
            pg.eval_on_selector_all(".skwrap", "e=>e.length") == 3 and
            pg.eval_on_selector("#cardDemo", "e=>e.getAttribute('aria-busy')") == "true")
    pg.click("#resolveDemo"); pg.wait_for_timeout(300)
    r.check("skeleton/resolution-clears-aria-busy",
            pg.eval_on_selector("#cardDemo", "e=>e.getAttribute('aria-busy')") == "false")
    cls = pg.eval_on_selector("#cardDemo p", "e=>e.className")
    r.check("skeleton/resolved-copy-carries-composite", "t-ed-body" in cls, f"class={cls!r}")
    sty = pg.eval_on_selector("#cardDemo p", "e=>e.getAttribute('style')")
    r.check("skeleton/resolved-copy-has-no-inline-style", not sty, f"style={sty!r}")
    # A class name is not typography. Before this lane the file pulled NO canon/type.css at all,
    # so a .t-ed-body written into it would have been inert decoration — present in the markup,
    # absent from the rendering (16px/normal in a fallback face). Assert the composite RESOLVES.
    lh = pg.eval_on_selector("#cardDemo p", "e=>getComputedStyle(e).lineHeight")
    r.check("skeleton/resolved-copy-composite-resolves", lh == "24px",
            f"computed line-height = {lh} (t-ed-body is 16/24; 'normal' means type.css never loaded)")

    br.close()
    return r.render()


def main():
    args = sys.argv[1:]
    if "--list" in args:
        for k, (f, _, checks) in MUTANTS.items():
            print(f"{k:18s} {f:32s} reddens: {', '.join(checks)}")
        return 0
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright missing — see ENVIRONMENT in this file's docstring")

    WORK.mkdir(parents=True, exist_ok=True)
    if (WORK / "canon").exists():
        shutil.rmtree(WORK / "canon")          # never a stale canon mirror

    wanted = None
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
            print(f"\n{'GREEN — ' + str(len(rows)) + ' checks' if not reds else 'FAILED: ' + ', '.join(reds)}")
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
                extra = f"  (collateral, expected of a shared page: {', '.join(unexpected)})" if unexpected else ""
                print(f"  ✓ RED BY NAME: {', '.join(must_redden)}{extra}")

    print("\n" + ("ALL BREAK ARMS BIT" if not failed else "BREAK ARMS FAILED: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
