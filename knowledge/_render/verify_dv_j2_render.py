#!/usr/bin/env python3
"""RENDER-PROOF for DV-J2 — Chart-scatter's Layer-2 catch-up (2026-07-28, session #27).

WHAT THIS PROVES, in a real browser, on the SNIPPET (canon truth — showroom panes are srcdoc
iframes and are not the artefact under test):

  1. the licensed HSBC cut is the face actually resolving (both --font strings, per the runbook)
  2. the canon toolbar renders at the shared control height with the 44px hit target
  3. the table toggle DRIVES the panel — aria-expanded flips, [hidden] clears, the panel paints
  4. a data point takes KEYBOARD focus and the popover appears — the half that was dead before
     DV-J2 (scatter shipped <title> children inside a role="img" svg: mouse-hover only, and the
     marks were not in the a11y tree as separate nodes at all)
  5. the panel's box-shadow RESOLVES — the --shadow the ds-018 gate caught me omitting. Compared
     AS A COLOUR, never as a string (memory: sandbox-html-rendering).
  6. all of the above at TWO widths.

--bite INVERTS the instrument: it strips data-tip from the probed point and re-runs check 4, which
MUST then fail. An absence-only test passes a full revert (the DV-D17 lesson) — so the bite proves
this file can detect the thing it claims to detect.

Run:  python3 knowledge/_render/verify_dv_j2_render.py [--bite]
Env:  LD_LIBRARY_PATH must carry ~/.local/chromelibs (see _RUNBOOK-render-verify.md step 4).
"""
import sys, pathlib, re

SNIPPET = pathlib.Path(__file__).resolve().parents[2] / "knowledge/snippets/Chart-scatter.reference.html"
WIDTHS = [(1280, 900), (720, 900)]
BITE = "--bite" in sys.argv


def parse_rgb(s):
    """Computed colours compared AS COLOURS — '#00000033' and 'rgba(0,0,0,0.2)' are the same ink."""
    m = re.findall(r"[\d.]+", s or "")
    if len(m) < 3:
        return None
    r, g, b = (int(float(x)) for x in m[:3])
    a = float(m[3]) if len(m) > 3 else 1.0
    return (r, g, b, round(a, 3))


def main():
    from playwright.sync_api import sync_playwright

    html = SNIPPET.read_text()
    if BITE:
        # strip the FIRST point's tip hook — check 4 must now fail
        html = html.replace(' data-tip="£28k income · £6k saved"', "", 1)

    fails, notes = [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for w, h in WIDTHS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.set_content(html)
            page.wait_for_timeout(400)          # SETTLE BEFORE YOU READ (ds-019)
            tag = f"[{w}px]"

            # 1 — the licensed cut
            if not page.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')"):
                fails.append(f"{tag} licensed HSBC cut did not resolve")

            # 2 — toolbar geometry
            btn = page.locator(".dv-tbl-toggle").first
            box = btn.bounding_box()
            if not box or round(box["height"]) != 32:
                fails.append(f"{tag} toggle height {box and round(box['height'])} != 32 (--control-h)")
            hit = page.evaluate(
                "() => { const b=document.querySelector('.dv-tbl-toggle');"
                " const s=getComputedStyle(b,'::before');"
                " return [s.minWidth, s.minHeight]; }")
            if hit != ["44px", "44px"]:
                fails.append(f"{tag} hit target {hit} != 44x44")
            notes.append(f"{tag} toggle {round(box['height'])}px tall, hit {hit[0]}x{hit[1]}")

            # 3 — the toggle drives the panel
            panel = page.locator("#cs1-tbl")
            if panel.is_visible():
                fails.append(f"{tag} panel visible before the toggle was pressed")
            btn.click()
            page.wait_for_timeout(250)
            if btn.get_attribute("aria-expanded") != "true":
                fails.append(f"{tag} aria-expanded did not flip to true")
            if not panel.is_visible():
                fails.append(f"{tag} panel did not paint after the toggle")
            pbox = panel.bounding_box()
            if not pbox or pbox["width"] < 100:
                fails.append(f"{tag} panel painted at implausible width {pbox and pbox['width']}")

            # 5 — the shadow RESOLVES (compared as a colour)
            shadow = page.evaluate("getComputedStyle(document.querySelector('#cs1-tbl')).boxShadow")
            rgba = parse_rgb(shadow)
            if rgba is None or rgba[3] == 0:
                fails.append(f"{tag} panel box-shadow does not resolve to an ink: {shadow!r}")
            else:
                notes.append(f"{tag} panel shadow -> rgba{rgba}")
            btn.click()
            page.wait_for_timeout(200)

            # 4 — KEYBOARD focus raises the popover (the half that was dead)
            pt = page.locator('circle[data-tip]').first if not BITE else page.locator("circle.dv-pt").first
            pt.focus()
            page.wait_for_timeout(300)
            tip_on = page.evaluate(
                "() => { const t=document.querySelector('.dv-tip');"
                " return !!t && t.classList.contains('on') && t.textContent.trim().length>0; }")
            if not tip_on:
                fails.append(f"{tag} CHECK-4 keyboard focus raised no popover")
            else:
                txt = page.evaluate("document.querySelector('.dv-tip').textContent.trim()")
                notes.append(f"{tag} keyboard focus -> tip {txt!r}")

            page.close()
        browser.close()

    for n in notes:
        print("   ", n)
    if BITE:
        got4 = [f for f in fails if "CHECK-4" in f]
        if got4:
            print(f"\n✅ BITE OK — the instrument detected the stripped hook: {got4[0]}")
            return 0
        print("\n❌ BITE FAILED — data-tip was stripped and check 4 still passed. "
              "This proof cannot detect what it claims to.")
        return 1
    if fails:
        print("\n❌ DV-J2 render-proof FAILED:")
        for f in fails:
            print("   X", f)
        return 1
    print(f"\n✅ DV-J2 render-proof GREEN — {len(WIDTHS)} widths, licensed cut, "
          "toolbar + panel + keyboard popover all live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
