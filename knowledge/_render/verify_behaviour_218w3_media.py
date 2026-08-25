#!/usr/bin/env python3
"""Driven behaviour verifier — #218 worker wave 3, MEDIA/STATUS cluster.

Covers the two snippets this lane BUILT:
  · knowledge/snippets/Video-player.reference.html      (transport: play/pause, mute, seek)
  · knowledge/snippets/Payment-card-visual.reference.html (card-number reveal toggle)

⛔ PRESENCE / LOAD ASSERTIONS ARE BANNED HERE, and that ban is the whole point: a gate that
checks "a <script> exists" or "the button is in the DOM" cannot see behaviour. Every assertion
below drives a real click or keypress in a real browser and asserts an ARIA STATE TRANSITION —
the attribute value BEFORE the action and AFTER it, both read off the live DOM.

  --break  copies both snippets to /var/tmp/218w3-media-break/ with the behaviour <script>
           STRIPPED (the JSON token-manifest survives) and re-runs the identical drive. Every
           named behaviour assertion MUST go RED. A green in the break arm means the assertion
           was measuring the markup, not the behaviour, and is worthless.

  Assertions marked GUARD are excluded from the break-arm requirement by design: they assert
  that something did NOT change (e.g. the four cards with no reveal button keep their faces),
  which is trivially true with no script at all. They are declared, not hidden.

Environment (proven this session — export before running):
  export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \\
         PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \\
         FONTCONFIG_FILE=/var/tmp/fonts-218w3.conf \\
         LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu

Usage:  python3 knowledge/_render/verify_behaviour_218w3_media.py
        python3 knowledge/_render/verify_behaviour_218w3_media.py --break
"""
import os
import pathlib
import re
import shutil
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SNIPPETS = HERE.parent / "snippets"
BREAK_DIR = pathlib.Path(os.environ.get("BW_MUTANT_DIR", "/var/tmp/218w3-media-break"))  # #218: shared-/var/tmp class fix

# byte-matched library paths the behaviour swaps in (assets/icons/volume-and-audio/)
D_PAUSE = ("M14.4004 1.2V16.8H13.2004V1.2H14.4004ZM4.80039 1.2V16.8H3.60039V1.2H4.80039Z"
           "M15.6004 0H12.0004V18H15.6004V0ZM6.00039 0H2.40039V18H6.00039V0Z")
D_MUTED_HEAD = "M0 5V13H5L10 18V0L5 5H0Z"          # volume-off.svg opening sub-path
D_VOLUME_HEAD = "M11.89 6.299C"                     # volume-high.svg opening sub-path


class Results:
    def __init__(self):
        self.rows = []

    def check(self, name, fn, guard=False):
        try:
            ok, detail = fn()
        except Exception as exc:                     # a crash is a RED, named — never a skip
            ok, detail = False, "%s: %s" % (type(exc).__name__, exc)
        self.rows.append((name, bool(ok), detail, guard))

    @property
    def behaviour(self):
        return [r for r in self.rows if not r[3]]

    @property
    def guards(self):
        return [r for r in self.rows if r[3]]


def _try(fn):
    """Run a drive step; swallow its failure so the remaining assertions still report.
    Used only for ACTIONS (clicks, key presses), never for assertions."""
    try:
        fn()
    except Exception:
        pass


def eq(actual, expected, label):
    return actual == expected, "%s: %r (expected %r)" % (label, actual, expected)


# --------------------------------------------------------------------------- Video player
def drive_video(page, R):
    big = page.locator(".bigplay")
    play = page.locator('.bar button[aria-label="Play"], .bar button[aria-label="Pause"]').first
    mute = page.locator('.bar button[aria-label="Mute"], .bar button[aria-label="Unmute"]').first
    fs = page.locator('.bar button[aria-label="Fullscreen"], .bar button[aria-label="Exit fullscreen"]').first
    scrub = page.locator(".scrub")
    played = page.locator(".scrub .played")
    timelbl = page.locator(".time")

    # --- boot: the behaviour re-renders the seeded clock and makes the slider reachable ---
    R.check("VP-boot-rerender-valuetext",
            lambda: (scrub.get_attribute("aria-valuetext") == "1:12 of 3:24",
                     "aria-valuetext=%r (markup ships NONE; behaviour writes '1:12 of 3:24')"
                     % scrub.get_attribute("aria-valuetext")))
    R.check("VP-boot-slider-focusable",
            lambda: eq(scrub.get_attribute("tabindex"), "0",
                       "role=slider tabindex (markup ships none)"))
    R.check("VP-boot-mute-pressed-seeded",
            lambda: eq(mute.get_attribute("aria-pressed"), "false",
                       "mute aria-pressed seeded by behaviour (markup ships none)"))
    R.check("VP-boot-fullscreen-pressed-seeded",
            lambda: eq(fs.get_attribute("aria-pressed"), "false",
                       "fullscreen aria-pressed seeded by behaviour (markup ships none)"))

    # --- play/pause: ACCESSIBLE NAME is the state channel (APG) ---
    before_big = big.get_attribute("aria-label")
    before_bar = play.get_attribute("aria-label")
    _try(lambda: big.click())
    R.check("VP-play-bigplay-name-transition",
            lambda: ((before_big, big.get_attribute("aria-label")) == ("Play video", "Pause video"),
                     "bigplay aria-label %r -> %r" % (before_big, big.get_attribute("aria-label"))))
    R.check("VP-play-barbutton-name-transition",
            lambda: ((before_bar, play.get_attribute("aria-label")) == ("Play", "Pause"),
                     "bar play aria-label %r -> %r" % (before_bar, play.get_attribute("aria-label"))))
    R.check("VP-play-glyph-swaps-to-pause",
            lambda: (big.locator("path").get_attribute("d") == D_PAUSE,
                     "bigplay path d == control-pause.svg (byte-matched): %s"
                     % (big.locator("path").get_attribute("d") or "")[:32]))
    R.check("VP-play-dataflag",
            lambda: eq(page.locator(".player").get_attribute("data-playing"), "true",
                       ".player data-playing"))

    # --- the demo clock actually advances while playing ---
    v0 = scrub.get_attribute("aria-valuenow")
    t0 = timelbl.inner_text()
    page.wait_for_timeout(1500)
    R.check("VP-clock-advances-while-playing",
            lambda: (int(scrub.get_attribute("aria-valuenow")) > int(v0),
                     "aria-valuenow %s -> %s after 1.5s of play"
                     % (v0, scrub.get_attribute("aria-valuenow"))))
    R.check("VP-clock-readout-follows",
            lambda: (timelbl.inner_text() != t0 and " / 3:24" in timelbl.inner_text(),
                     ".time %r -> %r" % (t0, timelbl.inner_text())))

    # --- pause returns the names and the glyph ---
    # the PRE-state is captured while PLAYING, so the assertion is the RETURN TRANSITION.
    # (Asserting only the end state would pass on the shipped markup — the break arm caught that.)
    mid_big, mid_bar = big.get_attribute("aria-label"), play.get_attribute("aria-label")
    _try(lambda: play.click())
    R.check("VP-pause-restores-names",
            lambda: (((mid_big, big.get_attribute("aria-label")) == ("Pause video", "Play video")
                      and (mid_bar, play.get_attribute("aria-label")) == ("Pause", "Play")),
                     "bigplay %r -> %r · bar %r -> %r"
                     % (mid_big, big.get_attribute("aria-label"),
                        mid_bar, play.get_attribute("aria-label"))))
    R.check("VP-pause-dataflag",
            lambda: eq(page.locator(".player").get_attribute("data-playing"), "false",
                       ".player data-playing after pause"))
    v_paused = scrub.get_attribute("aria-valuenow")
    page.wait_for_timeout(700)
    # frozen AND already moved off the seeded 35 — "frozen" alone is true of a page with no clock.
    R.check("VP-clock-frozen-when-paused",
            lambda: (scrub.get_attribute("aria-valuenow") == v_paused and v_paused != "35",
                     "aria-valuenow held at %r across 700ms paused (and had advanced off the "
                     "seeded 35)" % v_paused))

    # --- Space / Enter reach the transport natively on the focused control ---
    _try(lambda: play.focus())
    n0 = play.get_attribute("aria-label")
    _try(lambda: page.keyboard.press("Space"))
    R.check("VP-key-Space-toggles-transport",
            lambda: ((n0, play.get_attribute("aria-label")) == ("Play", "Pause"),
                     "Space on focused bar button: %r -> %r"
                     % (n0, play.get_attribute("aria-label"))))
    n1 = play.get_attribute("aria-label")
    _try(lambda: page.keyboard.press("Enter"))
    R.check("VP-key-Enter-toggles-transport",
            lambda: ((n1, play.get_attribute("aria-label")) == ("Pause", "Play"),
                     "Enter on focused bar button: %r -> %r"
                     % (n1, play.get_attribute("aria-label"))))

    # --- mute is a real toggle: aria-pressed + name + byte-matched glyph ---
    m0 = mute.get_attribute("aria-pressed")
    _try(lambda: mute.click())
    R.check("VP-mute-pressed-transition",
            lambda: ((m0, mute.get_attribute("aria-pressed")) == ("false", "true"),
                     "mute aria-pressed %r -> %r" % (m0, mute.get_attribute("aria-pressed"))))
    R.check("VP-mute-name-transition",
            lambda: eq(mute.get_attribute("aria-label"), "Unmute", "mute aria-label after press"))
    R.check("VP-mute-glyph-swaps-to-volume-off",
            lambda: ((mute.locator("path").get_attribute("d") or "").startswith(D_MUTED_HEAD),
                     "mute path d starts with volume-off.svg: %s"
                     % (mute.locator("path").get_attribute("d") or "")[:32]))
    _try(lambda: mute.click())
    R.check("VP-unmute-pressed-transition",
            lambda: (mute.get_attribute("aria-pressed") == "false"
                     and mute.get_attribute("aria-label") == "Mute"
                     and (mute.locator("path").get_attribute("d") or "").startswith(D_VOLUME_HEAD),
                     "unmute: pressed=%r label=%r glyph=%s"
                     % (mute.get_attribute("aria-pressed"), mute.get_attribute("aria-label"),
                        (mute.locator("path").get_attribute("d") or "")[:16])))

    # --- seek: arrows / Home / End move aria-valuenow on the existing role="slider" ---
    _try(lambda: scrub.focus())
    _try(lambda: page.keyboard.press("Home"))
    R.check("VP-seek-Home-to-zero",
            lambda: (scrub.get_attribute("aria-valuenow") == "0"
                     and scrub.get_attribute("aria-valuetext") == "0:00 of 3:24",
                     "Home -> valuenow=%r valuetext=%r"
                     % (scrub.get_attribute("aria-valuenow"), scrub.get_attribute("aria-valuetext"))))
    s0 = int(scrub.get_attribute("aria-valuenow") or -1)
    _try(lambda: page.keyboard.press("ArrowRight"))
    R.check("VP-seek-ArrowRight-increases",
            lambda: (int(scrub.get_attribute("aria-valuenow")) > s0,
                     "ArrowRight: valuenow %s -> %s" % (s0, scrub.get_attribute("aria-valuenow"))))
    s1 = int(scrub.get_attribute("aria-valuenow") or -1)
    _try(lambda: page.keyboard.press("ArrowLeft"))
    R.check("VP-seek-ArrowLeft-decreases",
            lambda: (int(scrub.get_attribute("aria-valuenow")) < s1,
                     "ArrowLeft: valuenow %s -> %s" % (s1, scrub.get_attribute("aria-valuenow"))))
    s2 = int(scrub.get_attribute("aria-valuenow") or -1)
    _try(lambda: page.keyboard.press("PageUp"))
    # a DELTA, not a threshold: ">= 14" was true of the shipped valuenow="35" and the break arm
    # caught it staying green with no behaviour at all.
    R.check("VP-seek-PageUp-bigger-step",
            lambda: (int(scrub.get_attribute("aria-valuenow")) - s2 >= 10,
                     "PageUp (+30s of 204s ~= +15 points): valuenow %s -> %s"
                     % (s2, scrub.get_attribute("aria-valuenow"))))
    _try(lambda: page.keyboard.press("End"))
    R.check("VP-seek-End-to-max",
            lambda: (scrub.get_attribute("aria-valuenow") == "100"
                     and scrub.get_attribute("aria-valuetext") == "3:24 of 3:24",
                     "End -> valuenow=%r valuetext=%r"
                     % (scrub.get_attribute("aria-valuenow"), scrub.get_attribute("aria-valuetext"))))
    # geometry, not a string match: the browser normalises "100.00%" to "100%", so assert the
    # RENDERED reflection — the fill must actually fill the track at valuenow=100.
    def _fill_ratio():
        return page.evaluate(
            "() => { const s = document.querySelector('.scrub'),"
            " f = document.querySelector('.scrub .played');"
            " return s.getBoundingClientRect().width ?"
            " f.getBoundingClientRect().width / s.getBoundingClientRect().width : -1; }")

    R.check("VP-seek-fill-tracks-valuenow",
            lambda: (abs(_fill_ratio() - 1.0) < 0.01,
                     ".played/.scrub rendered width ratio at valuenow=100: %.4f" % _fill_ratio()))
    R.check("VP-seek-readout-tracks-valuenow",
            lambda: eq(timelbl.inner_text().strip(), "3:24 / 3:24", ".time after End"))

    # --- pointer seek on the slider ---
    box = None
    try:
        box = scrub.bounding_box()
    except Exception:
        pass
    if box:
        _try(lambda: page.mouse.click(box["x"] + box["width"] * 0.25, box["y"] + box["height"] / 2))
    R.check("VP-seek-pointer-click",
            lambda: (18 <= int(scrub.get_attribute("aria-valuenow")) <= 32,
                     "click at 25%% of the track -> valuenow=%s (expected ~25)"
                     % scrub.get_attribute("aria-valuenow")))


# ------------------------------------------------------------------- Payment card visual
def drive_pcv(page, R):
    btns = page.locator(".pcv-reveal")
    b1, b2 = btns.nth(0), btns.nth(1)
    pan1 = page.locator(".unit").nth(0).locator(".pcv-pan")
    pan2 = page.locator(".unit").nth(1).locator(".pcv-pan")
    name1 = page.locator("#pcv1-name")
    name2 = page.locator("#pcv2-name")

    # snapshot the four faces that carry NO reveal control — nothing may clobber them
    others0 = page.locator(".pcv.is-unusable .pcv-pan, .pcv--compact .pcv-pan").all_inner_texts()

    # --- unit 1: masked -> revealed ---
    p0, l0, t0 = b1.get_attribute("aria-pressed"), b1.inner_text().strip(), pan1.inner_text().strip()
    _try(lambda: b1.click())
    R.check("PCV-u1-pressed-transition",
            lambda: ((p0, b1.get_attribute("aria-pressed")) == ("false", "true"),
                     "unit1 aria-pressed %r -> %r" % (p0, b1.get_attribute("aria-pressed"))))
    R.check("PCV-u1-label-transition",
            lambda: ((l0, b1.inner_text().strip()) == ("Show number", "Hide number"),
                     "unit1 label %r -> %r" % (l0, b1.inner_text().strip())))
    R.check("PCV-u1-pan-revealed",
            lambda: ((t0, pan1.inner_text().strip())
                     == ("···· ···· ···· 4821", "4000 0000 0000 4821"),
                     "unit1 PAN %r -> %r" % (t0, pan1.inner_text().strip())))
    R.check("PCV-u1-accessible-name-follows",
            lambda: (name1.inner_text().strip().endswith("Card number shown.")
                     and "4000 0000 0000 4821" in name1.inner_text(),
                     "unit1 sr-only: %r" % name1.inner_text().strip()))

    # --- unit 1: revealed -> masked (round trip). The PRE-state is captured while REVEALED, so
    #     this is a transition; asserting the end state alone passed on the shipped markup. ---
    r0, rl0 = b1.get_attribute("aria-pressed"), b1.inner_text().strip()
    _try(lambda: b1.click())
    R.check("PCV-u1-roundtrip-to-masked",
            lambda: ((r0, b1.get_attribute("aria-pressed")) == ("true", "false")
                     and (rl0, b1.inner_text().strip()) == ("Hide number", "Show number")
                     and pan1.inner_text().strip() == "···· ···· ···· 4821"
                     and name1.inner_text().strip().endswith("Card number hidden."),
                     "unit1 round trip: pressed %r -> %r · label %r -> %r · pan=%r"
                     % (r0, b1.get_attribute("aria-pressed"), rl0, b1.inner_text().strip(),
                        pan1.inner_text().strip())))

    # --- unit 2 ships REVEALED: the same control must run the other way, independently ---
    q0, m0 = b2.get_attribute("aria-pressed"), b2.inner_text().strip()
    _try(lambda: b2.click())
    R.check("PCV-u2-pressed-transition-reverse",
            lambda: ((q0, b2.get_attribute("aria-pressed")) == ("true", "false"),
                     "unit2 aria-pressed %r -> %r" % (q0, b2.get_attribute("aria-pressed"))))
    R.check("PCV-u2-label-transition-reverse",
            lambda: ((m0, b2.inner_text().strip()) == ("Hide number", "Show number"),
                     "unit2 label %r -> %r" % (m0, b2.inner_text().strip())))
    R.check("PCV-u2-pan-masked",
            lambda: eq(pan2.inner_text().strip(), "···· ···· ···· 4821", "unit2 PAN after hide"))
    R.check("PCV-u2-accessible-name-follows",
            lambda: (name2.inner_text().strip().endswith("Card number hidden.")
                     and "4000 0000 0000 4821" not in name2.inner_text(),
                     "unit2 sr-only: %r" % name2.inner_text().strip()))
    # GUARD: an ISOLATION assertion (something must NOT change), so it is trivially true with no
    # script — reclassified after the break arm correctly refused to let it count as behaviour.
    R.check("PCV-GUARD-u1-unaffected-by-u2",
            lambda: eq(b1.get_attribute("aria-pressed"), "false",
                       "unit1 must not move when unit2 is clicked"),
            guard=True)

    # GUARD (excluded from the break arm by design — trivially true with no script)
    R.check("PCV-GUARD-other-faces-untouched",
            lambda: (page.locator(".pcv.is-unusable .pcv-pan, .pcv--compact .pcv-pan")
                     .all_inner_texts() == others0,
                     "the 3 faces with no reveal control kept their PANs: %r" % (others0,)),
            guard=True)


DRIVERS = {
    "Video-player": drive_video,
    "Payment-card-visual": drive_pcv,
}


def make_break_copies():
    """Copy each snippet with the behaviour <script> STRIPPED. The JSON token-manifest
    (<script type="application/json">) must survive — otherwise the break arm would be testing
    a different document, not a document without behaviour."""
    if BREAK_DIR.exists():
        shutil.rmtree(BREAK_DIR)
    BREAK_DIR.mkdir(parents=True)
    out = {}
    for name in DRIVERS:
        src = SNIPPETS / ("%s.reference.html" % name)
        html = src.read_text(encoding="utf-8")
        stripped, n = re.subn(r"\n[ \t]*<script>.*?</script>", "", html, flags=re.S)
        if n != 1:
            raise SystemExit("break arm: expected exactly 1 behaviour <script> in %s, found %d"
                             % (src.name, n))
        if 'id="token-manifest"' not in stripped:
            raise SystemExit("break arm: token-manifest was destroyed in %s" % src.name)
        dst = BREAK_DIR / src.name
        dst.write_text(stripped, encoding="utf-8")
        out[name] = dst
        print("  stripped %d bytes of behaviour -> %s"
              % (len(html) - len(stripped), dst))
    return out


def main():
    broke = "--break" in sys.argv
    paths = make_break_copies() if broke else {
        n: SNIPPETS / ("%s.reference.html" % n) for n in DRIVERS}

    all_rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, drv in DRIVERS.items():
            page = browser.new_page(viewport={"width": 1200, "height": 900})
            page.goto(paths[name].as_uri())
            page.wait_for_timeout(120)
            R = Results()
            drv(page, R)
            page.close()
            all_rows.append((name, R))
        browser.close()

    arm = "BREAK (behaviour script stripped)" if broke else "GREEN (as shipped)"
    print("\n=== verify_behaviour_218w3_media — %s ===" % arm)
    behaviour_pass = behaviour_fail = 0
    for name, R in all_rows:
        print("\n--- %s.reference.html" % name)
        for aname, ok, detail, guard in R.rows:
            tag = "GUARD" if guard else ("PASS " if ok else "FAIL ")
            print("  [%s] %-38s %s" % (tag if guard else tag, aname, detail))
            if not guard:
                if ok:
                    behaviour_pass += 1
                else:
                    behaviour_fail += 1

    total = behaviour_pass + behaviour_fail
    if broke:
        greens = [a for _, R in all_rows for (a, ok, _d, g) in R.rows if ok and not g]
        print("\nBREAK ARM: %d/%d behaviour assertions went RED as required."
              % (behaviour_fail, total))
        if greens:
            print("⛔ THESE STAYED GREEN WITHOUT THE BEHAVIOUR — they measure markup, not behaviour:")
            for g in greens:
                print("   X %s" % g)
            return 1
        print("✓ every named behaviour assertion is behaviour-dependent.")
        return 0

    print("\nGREEN ARM: %d passed, %d failed (of %d behaviour assertions; "
          "%d guard assertion(s) reported separately)."
          % (behaviour_pass, behaviour_fail, total,
             sum(len(R.guards) for _, R in all_rows)))
    bad_guards = [a for _, R in all_rows for (a, ok, _d, g) in R.rows if g and not ok]
    if bad_guards:
        print("⛔ GUARD FAILED: %s" % ", ".join(bad_guards))
        return 1
    return 1 if behaviour_fail else 0


if __name__ == "__main__":
    sys.exit(main())
