#!/usr/bin/env python3
"""
verify_dv_d17_render.py — prove DV-D17 PAINTS, by driving the real gestures.

WHY THIS EXISTS, AND WHY THE OBVIOUS PROOF WAS WRONG (2026-07-27)
-----------------------------------------------------------------
DV-D17 ("a blank swatch checked while isolated ENDS isolation") was ENACTED and
DOM-PROVEN in jsdom — 108/108 + 27/27, three neutered controls. jsdom proves the state
machine. It does not prove that `.is-solo` stops PAINTING.

The acceptance test as originally specified was:

    "no `.dv-legrow` resolves the `.is-solo` treatment after isolate-then-check-on"

★ THAT TEST IS VACUOUS, and this file exists because of it. It asserts only an ABSENCE.
An absence is satisfied by a working fix, by a broken probe, by a mistyped selector, and
by a COMPLETE REVERT OF THE FIX. Session #8 ran it, printed `24 checks · 0 failures`, and
was measuring nothing. ⇒ **A one-sided proof of an absence is not a proof.**

THE SHAPE THAT ACTUALLY BITES — two sides, in one gesture sequence:

    STEP 1 · POSITIVE CONTROL (sensitivity). Isolate series A by its LABEL.
             Row A MUST paint the .is-solo treatment: border-color = --ink, background
             = 6% ink. If this side fails, the probe is BLIND and step 2 is worthless.
             This is the side the vacuous test never had.
    STEP 2 · THE RULING. Check series B on by its SWATCH (blank while isolated).
             Row A MUST return to resting (border = --line, background transparent) and
             NO row anywhere may still paint the treatment.

Step 1 is what makes step 2 mean anything. Run them in that order, on the same node, in
the same page, and a revert of DV-D17 fails step 2 while step 1 still passes — which is
exactly what `--bite` demonstrates on a NEUTERED COPY (canon is never mutated).

DESIGN RULES BAKED IN (each paid for by a real defect)
------------------------------------------------------
1. ★ SETTLE BEFORE READING (ds-019 — a false defect that survived a full session as canon).
   `.dv-legrow` transitions border-color + background over 0.16s. A computed value read in
   the same task as a class change is the PRE-transition value. This script injects
   `transition:none !important` BEFORE the first gesture, so a mid-transition read is
   structurally impossible. ⚠ `oklab(0 0 0 / 0)` is the signature of an IN-FLIGHT
   INTERPOLATION, not of a failed declaration.
2. COMPARE COLOURS AS COLOURS, never as strings. `oklab(0 0 0 / 0)` and `rgba(0, 0, 0, 0)`
   are textually different and visually identical; a control that passes on a serialisation
   difference is not a control. Expected values are READ FROM THE LIVE CUSTOM PROPERTIES
   (--ink, --line) at measurement time, never hardcoded.
3. OBSERVE, DO NOT INFER. Anything the engine does not tell us is reported UNKNOWN and
   fails the run. No defaults, no plausible-looking fills. [[feedback-measuring-tool-must-not-guess]]
4. NO SILENT FALLBACK. If a real pointer click cannot land, that is REPORTED loudly and
   recorded in the evidence — it is never swapped for a JS .click() behind your back.
5. THIS ONE MEASURES PAINT, so it ASSERTS THE LICENSED CUT FIRST
   (`document.fonts.check`) per _RUNBOOK-render-verify.md step 5 — inside the frame it is
   actually measuring, not the top document.

USAGE
    python3 knowledge/_render/verify_dv_d17_render.py --file knowledge/snippets/Chart-bar.reference.html
    python3 knowledge/_render/verify_dv_d17_render.py --file showroom/chart-bar.html \
            --frame-url-contains Chart-bar
    python3 knowledge/_render/verify_dv_d17_render.py --file <neutered copy> --bite

EXIT 0 = green · 1 = a check failed · 2 = the probe could not measure (never a pass)
"""
from __future__ import annotations
import argparse, glob, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
try:
    from cdp_matched_styles import parse_colour  # colours as colours — one implementation
except ImportError:  # pragma: no cover - the sibling is in the same directory by construction
    print("FATAL: cannot import parse_colour from cdp_matched_styles.py", file=sys.stderr)
    raise

EPS = 0.02  # channel/alpha tolerance; ink vs line differ by ~0.78 so this is not load-bearing


def close(a, b, eps=EPS):
    """True only if BOTH are parsed and every known channel agrees. UNKNOWN never passes."""
    if a is None or b is None:
        return False
    for x, y in zip(a, b):
        if x is None or y is None:
            return False
        if abs(x - y) > eps:
            return False
    return True


def alpha_of(c):
    return None if c is None else c[3]


READ_ROWS = """
() => {
  const out = [];
  document.querySelectorAll('.dv-leg').forEach((host, hi) => {
    host.querySelectorAll('.dv-legrow').forEach(r => {
      const cs = getComputedStyle(r);
      out.push({
        host: hi,
        series: r.getAttribute('data-series'),
        is_solo_class: r.classList.contains('is-solo'),
        /* ★ canon.css also paints an ink border on `.dv-legrow:hover`. A real pointer click
           leaves the cursor ON the row it clicked, so without this the sweep below reports
           the probe's own mouse position as an unnamed rule. OBSERVED, not assumed. */
        hovered: r.matches(':hover'),
        aria_pressed: (r.querySelector('.dv-leg-item') || {}).getAttribute
                      ? r.querySelector('.dv-leg-item').getAttribute('aria-pressed') : null,
        border: cs.borderTopColor,
        background: cs.backgroundColor,
        ink: cs.getPropertyValue('--ink').trim(),
        line: cs.getPropertyValue('--line').trim(),
      });
    });
  });
  return out;
}
"""


def measure(target):
    rows = target.evaluate(READ_ROWS)
    for r in rows:
        r["border_parsed"] = parse_colour(r["border"])
        r["background_parsed"] = parse_colour(r["background"])
        r["ink_parsed"] = parse_colour(r["ink"])
        r["line_parsed"] = parse_colour(r["line"])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--frame-url-contains", default=None,
                    help="measure inside an iframe (the showroom panes are srcdoc IFRAMES — "
                         "querying the top document finds nothing and returns cleanly)")
    ap.add_argument("--frame-index", type=int, default=0,
                    help="which matching frame (showroom pages carry a light AND a dark pane)")
    ap.add_argument("--widths", default="1180,760")
    ap.add_argument("--bite", action="store_true",
                    help="INVERT: step 2 is EXPECTED to fail (point at a neutered copy). "
                         "Exits 1 if step 2 passes, i.e. if the proof cannot detect a revert.")
    ap.add_argument("--png-dir", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    sys.path.insert(0, os.environ.get("PWLIBS", ""))
    from playwright.sync_api import sync_playwright

    shell = glob.glob(os.path.expanduser(os.environ.get(
        "PWSHELL", "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")))
    if not shell:
        print("FATAL: no headless_shell found. Set PWSHELL. Not guessing a path.", file=sys.stderr)
        return 2

    report, failures, blockers = {}, [], []

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0], headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                                    "--allow-file-access-from-files"])
        for w in [int(x) for x in args.widths.split(",")]:
            key = str(w)
            rec = report.setdefault(key, {})
            pg = b.new_page(viewport={"width": w, "height": 1600})
            pg.goto(f"file://{os.path.abspath(args.file)}")
            pg.wait_for_timeout(1500)  # entry motion completes BEFORE transitions are killed

            target = pg
            if args.frame_url_contains:
                frames = [f for f in pg.frames
                          if args.frame_url_contains in (f.url or "")
                          or args.frame_url_contains in (f.name or "")]
                if len(frames) <= args.frame_index:
                    blockers.append(f"{w}: no frame #{args.frame_index} matching "
                                    f"{args.frame_url_contains!r}; found {len(frames)}; "
                                    f"frames={[f.url[:60] for f in pg.frames]}")
                    pg.close(); continue
                target = frames[args.frame_index]
                rec["frame"] = f"#{args.frame_index} of {len(frames)} matching"

            # --- rule 5: the licensed cut, asserted in the frame being measured -------
            fonts_ok = target.evaluate("() => document.fonts.check('16px HSBC_MtUnivers_Latin')")
            rec["licensed_cut_asserted"] = bool(fonts_ok)
            if not fonts_ok:
                blockers.append(f"{w}: document.fonts.check failed — a fallback-face render "
                                f"passes while broken. Refusing to measure.")
                pg.close(); continue

            # --- rule 1: SETTLE, before any gesture ----------------------------------
            target.evaluate("() => { const s = document.createElement('style');"
                            " s.textContent = '*,*::before,*::after{transition:none !important;"
                            "animation:none !important}'; document.head.appendChild(s); }")

            base = measure(target)
            if not base:
                blockers.append(f"{w}: no .dv-legrow rows found — wrong document or wrong frame.")
                pg.close(); continue
            rec["rows_found"] = len(base)
            rec["baseline"] = base

            ids = [r["series"] for r in base if r["host"] == 0]
            if len(ids) < 2:
                blockers.append(f"{w}: need >=2 series in legend 0, found {ids}.")
                pg.close(); continue
            a_id, b_id = ids[0], ids[1]
            rec["series_isolated"], rec["series_added"] = a_id, b_id

            def click(sel, what):
                """Real pointer click. NO SILENT FALLBACK (rule 4)."""
                try:
                    target.click(sel, timeout=4000)
                    return "real-pointer-click"
                except Exception as e:  # noqa: BLE001 - reported, never swallowed
                    blockers.append(f"{w}: real click on {what} ({sel}) could not land: "
                                    f"{type(e).__name__}. NOT falling back to a JS click — "
                                    f"a hit area that cannot be clicked is itself a finding.")
                    return None

            # ================= STEP 1 · POSITIVE CONTROL =========================
            path = click(f'.dv-legrow[data-series="{a_id}"] .dv-leg-item', "label (isolate)")
            if path is None:
                pg.close(); continue
            rec["step1_click"] = path
            pg.wait_for_timeout(80)
            s1 = measure(target)
            rec["step1_isolated"] = s1
            if args.png_dir:
                pg.screenshot(path=os.path.join(args.png_dir, f"dv-d17-{w}-step1-isolated.png"),
                              full_page=True)

            row_a1 = next((r for r in s1 if r["host"] == 0 and r["series"] == a_id), None)
            if row_a1 is None:
                blockers.append(f"{w}: row {a_id} vanished after isolate.")
                pg.close(); continue

            if not row_a1["is_solo_class"]:
                failures.append(f"{w} STEP1: row {a_id} has no .is-solo class after isolating it.")
            if not close(row_a1["border_parsed"], row_a1["ink_parsed"]):
                failures.append(f"{w} STEP1 (SENSITIVITY): isolated row {a_id} border is "
                                f"{row_a1['border']} — expected --ink {row_a1['ink']}. "
                                f"The treatment is NOT painting, so step 2 proves nothing.")
            a1 = alpha_of(row_a1["background_parsed"])
            if a1 is None or abs(a1 - 0.06) > EPS:
                failures.append(f"{w} STEP1 (SENSITIVITY): isolated row {a_id} background is "
                                f"{row_a1['background']} — expected 6% ink. "
                                f"⚠ an oklab(...) serialisation here means the read landed "
                                f"MID-TRANSITION (ds-019); the settle step did not take.")

            # ================= STEP 2 · THE RULING ===============================
            path = click(f'.dv-legrow[data-series="{b_id}"] .dv-leg-sw', "swatch (check on)")
            if path is None:
                pg.close(); continue
            rec["step2_click"] = path
            # ★ PARK THE POINTER before measuring. `.dv-legrow:hover` also paints an ink
            # border, so a pointer left resting on the row it just clicked makes a correct
            # release look like a live defect. The first run of this script did exactly that
            # and the sweep fired — the check was working; the cause was the instrument.
            pg.mouse.move(2, 2)
            pg.wait_for_timeout(80)
            s2 = measure(target)
            rec["pointer_parked_before_read"] = True
            rec["step2_released"] = s2
            if args.png_dir:
                pg.screenshot(path=os.path.join(args.png_dir, f"dv-d17-{w}-step2-released.png"),
                              full_page=True)

            row_a2 = next((r for r in s2 if r["host"] == 0 and r["series"] == a_id), None)
            step2 = []
            if row_a2 is None:
                blockers.append(f"{w}: row {a_id} vanished after release.")
                pg.close(); continue
            if row_a2["is_solo_class"]:
                step2.append(f"{w} STEP2: row {a_id} STILL carries .is-solo after a second "
                             f"series was checked on — DV-D17 not honoured.")
            if not close(row_a2["border_parsed"], row_a2["line_parsed"]):
                step2.append(f"{w} STEP2: row {a_id} border is {row_a2['border']} — expected "
                             f"resting --line {row_a2['line']}. THE TREATMENT IS STILL PAINTED.")
            a2 = alpha_of(row_a2["background_parsed"])
            if a2 is None or a2 > EPS:
                step2.append(f"{w} STEP2: row {a_id} background is {row_a2['background']} — "
                             f"expected transparent.")
            for r in s2:
                if r["is_solo_class"]:
                    step2.append(f"{w} STEP2: some row still carries .is-solo "
                                 f"(host {r['host']}, series {r['series']}).")
                elif close(r["border_parsed"], r["ink_parsed"]):
                    if r.get("hovered"):
                        # `.dv-legrow:hover{border-color:var(--ink)}` is canon and correct.
                        # Named and skipped rather than silently filtered.
                        rec.setdefault("skipped_because_hovered", []).append(r["series"])
                        continue
                    step2.append(f"{w} STEP2: row {r['series']} (host {r['host']}) paints an ink "
                                 f"border with no .is-solo class and is NOT hovered — an unnamed "
                                 f"rule is painting it.")

            rec["step2_failures"] = step2
            if args.bite:
                if not step2:
                    failures.append(f"{w} BITE FAILED: step 2 PASSED on a neutered copy. "
                                    f"The proof cannot detect a revert of DV-D17 — it is blind.")
            else:
                failures.extend(step2)

            pg.close()
        b.close()

    out = json.dumps(report, indent=2, default=str)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out)

    print("=" * 78)
    for w, rec in report.items():
        print(f"[{w}px] licensed cut: {rec.get('licensed_cut_asserted')} · rows: "
              f"{rec.get('rows_found')} · isolated {rec.get('series_isolated')} → added "
              f"{rec.get('series_added')} · click path: {rec.get('step1_click')}")
    if blockers:
        print("\nCOULD NOT MEASURE (this is never a pass):")
        for x in blockers:
            print("  ⛔ " + x)
    if failures:
        print("\nFAILURES:")
        for x in failures:
            print("  ✗ " + x)
    if args.bite and not failures and not blockers:
        print("\n✅ BITE OK — step 2 failed on the neutered copy at every width, "
              "so a revert of DV-D17 is detectable.")
    elif not failures and not blockers:
        print("\n✅ GREEN — the treatment PAINTS when isolated (positive control) and "
              "STOPS painting when a second series is checked on (DV-D17).")
    print("=" * 78)

    if blockers:
        return 2
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
