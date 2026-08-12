#!/usr/bin/env python3
"""Render-verify the ds-018 decision review doc.

WHY this exists: the doc's whole value is that its numbers are MEASURED, not typed. If the specimens
fail to reproduce the defect, or the live contrast maths returns nothing, the page becomes a confident
false inscription handed to Dave at ruling time — the most expensive failure this project has.

Two-sided by construction (the lesson from DV-D17's one-sided proof):
  STEP 1  proves the defect IS REPRODUCED in the specimen (disabled border == hover border == ink).
          Without this, step 2 is satisfied by a page that renders nothing at all.
  STEP 2  proves the selected remedy CHANGES it (B-pane disabled label goes recessive, border drops
          to --line) — i.e. the live controller is wired, not decorative.

  --bite  declares --border-disabled on :root of a COPY, which resolves the lookup and so must make
          STEP 1 fail. If --bite comes back green, this probe is blind and its green means nothing.

Colours are parsed and compared AS COLOURS, never as strings (an oklab()/rgba() serialisation
difference is not a colour difference). Transitions are killed before any read.

Usage:  python3 knowledge/_render/verify_ds018_review.py [--bite]
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, re, sys, json, shutil, tempfile

DOC = "reviews/DS-018-DISABLED-STATE-2026-07-27-v1.html"
WIDTHS = [1180, 760]
BITE = "--bite" in sys.argv

INK_LIGHT = (26, 26, 26)
LINE_LIGHT = (225, 225, 225)
RECESSIVE_DEFAULT = (157, 157, 157)   # #9D9D9D — the doc's default candidate


def rgb(s):
    """Parse a computed colour to an (r,g,b) int tuple. Colours as colours, never as strings."""
    m = re.search(r"rgba?\(([^)]+)\)", s or "")
    if not m:
        return None
    parts = [p for p in re.split(r"[,\s/]+", m.group(1)) if p]
    return tuple(int(round(float(p))) for p in parts[:3])


def near(a, b, tol=2):
    return a is not None and b is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def main():
    from playwright.sync_api import sync_playwright

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    src = os.path.join(root, DOC)
    if not os.path.exists(src):
        print("FATAL: doc not found:", src)
        return 2

    target = src
    tmpdir = None
    if BITE:
        # Neuter a COPY. Canon is never mutated by a bite.
        tmpdir = tempfile.mkdtemp()
        target = os.path.join(os.path.dirname(src), "_BITE-ds018-review.html")
        html = open(src).read()
        html = html.replace(
            ":root{\n  --page:#FFFFFF;",
            ":root{\n  --border-disabled:#CCCCCC; --text-disabled:#CCCCCC;\n  --page:#FFFFFF;",
            1,
        )
        open(target, "w").write(html)
        print("BITE: --border-disabled/--text-disabled declared on :root of a COPY "
              "-> the lookup resolves -> STEP 1 MUST fail.\n")

    failures, checks = [], 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=next(
                os.path.join(dp, f)
                for dp, _, fs in os.walk(os.path.expanduser("~/.cache/ms-playwright"))
                for f in fs
                if f == "headless_shell"
            ),
            args=["--allow-file-access-from-files", "--no-sandbox"],
        )
        for w in WIDTHS:
            page = browser.new_page(viewport={"width": w, "height": 1400})
            page.goto("file://" + target)
            page.wait_for_timeout(400)

            ctx = f"@{w}"

            # ── FONT ASSERT, inside the frame being measured ────────────────
            checks += 1
            if not page.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')"):
                failures.append(f"{ctx} licensed cut NOT active — a fallback render proves nothing")

            # ── SETTLE: kill transitions before any computed read ───────────
            page.add_style_tag(content="*{transition:none !important; animation:none !important;}")
            page.wait_for_timeout(120)

            read = """(sel) => {
              const b = document.querySelector(sel);
              if(!b) return null;
              const cs = getComputedStyle(b);
              return {border: cs.borderTopColor, color: cs.color};
            }"""
            pagebg = page.evaluate(
                "() => getComputedStyle(document.getElementById('demoA')).backgroundColor")
            darkbg = page.evaluate(
                "() => getComputedStyle(document.getElementById('demoAd')).backgroundColor")

            A_en = page.evaluate(read, "#demoA .dv-leg-reset[data-k=enabled]")
            A_hv = page.evaluate(read, "#demoA .dv-leg-reset[data-k=hover]")
            A_di = page.evaluate(read, "#demoA .dv-leg-reset[data-k=disabled]")

            # ══ STEP 1 — THE DEFECT IS REPRODUCED ══════════════════════════
            checks += 1
            if not near(rgb(pagebg), (255, 255, 255)):
                failures.append(f"{ctx} STEP1 light pane is not white: {pagebg}")
            checks += 1
            if not near(rgb(A_en["border"]), LINE_LIGHT):
                failures.append(f"{ctx} STEP1 enabled border != --line #E1E1E1: {A_en['border']}")
            checks += 1
            if not near(rgb(A_hv["border"]), INK_LIGHT):
                failures.append(f"{ctx} STEP1 hover border != ink: {A_hv['border']}")
            checks += 1
            if not near(rgb(A_di["border"]), INK_LIGHT):
                failures.append(
                    f"{ctx} STEP1 THE DEFECT IS NOT REPRODUCED — disabled border {A_di['border']} "
                    f"is not ink; the doc would be showing Dave a defect it does not contain")
            checks += 1
            if not near(rgb(A_di["border"]), rgb(A_hv["border"])):
                failures.append(f"{ctx} STEP1 disabled != hover, so the inversion is not shown")
            checks += 1
            if not near(rgb(A_di["color"]), INK_LIGHT):
                failures.append(f"{ctx} STEP1 disabled label != ink: {A_di['color']}")

            # dark pane must be genuinely dark — coverage, not one pane twice
            checks += 1
            if not near(rgb(darkbg), INK_LIGHT):
                failures.append(f"{ctx} dark pane is not dark: {darkbg}")

            # ══ STEP 2 — THE LIVE CONTROLLER ACTUALLY CHANGES IT ═══════════
            B_di = page.evaluate(read, "#demoB .dv-leg-reset[data-k=disabled]")
            checks += 1
            if not near(rgb(B_di["color"]), RECESSIVE_DEFAULT):
                failures.append(
                    f"{ctx} STEP2 B-pane disabled label {B_di['color']} is not the selected "
                    f"recessive candidate #9D9D9D — the controller is decorative, not wired")
            checks += 1
            if not near(rgb(B_di["border"]), LINE_LIGHT):
                failures.append(
                    f"{ctx} STEP2 B-pane disabled border {B_di['border']} did not drop to --line")

            # ── the live maths must have produced real numbers ─────────────
            sq = page.evaluate("() => document.getElementById('squeeze').textContent")
            checks += 1
            if "NaN" in sq or "undefined" in sq or len(sq.strip()) < 60:
                failures.append(f"{ctx} §2 squeeze table did not compute: {sq[:90]!r}")
            # ⚠ INSTRUMENT NOTE (caught in first run, 2026-07-27): reading ratios off the table's
            # textContent straddles the adjacent hex cell — "#E1E1E1" + "1.31:1" concatenates to
            # "…E1E1E11.31:1" and a \d+\.\d+ regex greedily reports "11.31". The doc was correct;
            # the probe was wrong. Read CELLS, never the flattened text.
            checks += 1
            ratios = page.evaluate(
                "() => Array.from(document.querySelectorAll('#squeeze tbody tr'))"
                ".map(r => r.cells[2].textContent.trim())")
            if len(ratios) < 3 or not all(re.fullmatch(r"\d+\.\d+:1", r) for r in ratios):
                failures.append(f"{ctx} §2 live ratios malformed: {ratios}")
            checks += 1
            # the squeeze must actually BE a squeeze: enabled below 2:1, disabled far above it
            en_r = float(ratios[2].split(":")[0]) if len(ratios) > 2 else 0
            di_r = float(ratios[1].split(":")[0]) if len(ratios) > 1 else 0
            if not (en_r < 2.0 < di_r):
                failures.append(
                    f"{ctx} §2 does not show the squeeze: enabled {en_r} / disabled {di_r}")

            # readouts on every specimen
            ros = page.evaluate(
                "() => Array.from(document.querySelectorAll('[data-ro]')).map(e=>e.textContent)")
            checks += 1
            empty = [i for i, t in enumerate(ros) if not t.strip()]
            if empty:
                failures.append(f"{ctx} {len(empty)} of {len(ros)} specimen readouts are empty")

            # export must produce a non-trivial ruling block
            page.click("#doexp")
            page.wait_for_timeout(120)
            exp = page.evaluate("() => document.getElementById('expout').value")
            checks += 1
            if len(exp) < 400 or "CALL A" not in exp or "NOT PICKED" in exp:
                failures.append(f"{ctx} export block is short or incomplete ({len(exp)} chars)")

            if w == WIDTHS[0]:
                print(f"  OBSERVED {ctx}: enabled {A_en['border']} · hover {A_hv['border']} · "
                      f"disabled {A_di['border']}")
                print(f"  OBSERVED {ctx}: live ratios in §2 = {ratios[:3]}")
                print(f"  OBSERVED {ctx}: B-pane disabled label {B_di['color']} "
                      f"border {B_di['border']}")
            page.close()
        browser.close()

    print(f"\n{checks} checks · {len(failures)} failures")
    for f in failures:
        print("  FAIL:", f)

    rc = 1 if failures else 0
    if BITE:
        step1 = [f for f in failures if "STEP1" in f]
        if step1:
            print("\nBITE OK — STEP 1 went red under the neuter, so this probe is NOT blind.")
            rc = 0
        else:
            print("\nBITE FAILED — the neuter did not turn STEP 1 red. THE PROBE IS BLIND; "
                  "a green run from it means nothing.")
            rc = 1

    # ⚠ The sandbox cannot unlink under the repo mount (EPERM) — MOVE the bite copy aside,
    #   never os.remove(). Cleanup runs AFTER the verdict so a cleanup error can never
    #   swallow the result (it did exactly that on first run, 2026-07-27).
    #   Destination must be on the SAME MOUNT and gitignored — repo `outputs/` (.gitignore:45).
    #   A cross-mount shutil.move degrades to copy+unlink, and the unlink hits the same EPERM.
    if BITE and target != src and os.path.exists(target):
        try:
            quarantine = os.path.join(root, "outputs", "_bite")
            os.makedirs(quarantine, exist_ok=True)
            shutil.move(target, os.path.join(quarantine, "_BITE-ds018-review.html"))
            print("  (bite copy moved out of the repo; canon untouched)")
        except OSError as e:
            print(f"  WARN: bite copy left at {target} — move it aside manually ({e})")
    return rc


if __name__ == "__main__":
    sys.exit(main())
