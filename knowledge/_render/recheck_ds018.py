#!/usr/bin/env python3
"""
recheck_ds018.py — re-verify ds-018 with the repo-homed harness, because its predecessor
was the SAME PROBE that produced the withdrawn ds-019.

WHY A RE-CHECK WAS OWED (2026-07-27, session #9 → #10)
------------------------------------------------------
ds-018 and ds-019 were measured in one session by one probe. ds-019 was later WITHDRAWN:
the probe had read a computed value in the same task as a class change, i.e. t=0 of a
0.16s transition. ds-018's evidence *should* be untouched by that defect — it measured a
RESTING disabled control, with no class change anywhere near it, and its census evidence
(29 declarations, ten form scopes, zero chart scopes) is independent of any render.

★ "Should not be affected" is not "is not affected." A defect entry that survives on the
reputation of a probe since discredited is exactly the confident-false-inscription this
project treats as the primary risk. So: measure it again, settled, colours as colours.

WHAT IT ASSERTS
    1. The Reset is genuinely `:disabled` at rest (else we are measuring the wrong state).
    2. --border-disabled / --text-disabled as they RESOLVE on the chart's own scope.
    3. The computed border-color, against --ink and against the :hover value.
    4. Whether the disabled treatment is indistinguishable from the hover treatment
       (the symptom Dave reported: "reset disabled style is set at the hover style").

It reports what it OBSERVES. It does not conclude, and it does not fix — the fix shape
(tier fix + which gate) is Dave's ruling, tracked in GOOD-MORNING §C·4.
"""
from __future__ import annotations
import argparse, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp_matched_styles import parse_colour  # noqa: E402

PROBE = """
() => {
  const out = [];
  document.querySelectorAll('.dv-leg-reset').forEach((el, i) => {
    const cs = getComputedStyle(el);
    out.push({
      index: i,
      disabled_property: el.disabled === true,
      matches_disabled_pseudo: el.matches(':disabled'),
      hovered: el.matches(':hover'),
      border_disabled_token: cs.getPropertyValue('--border-disabled'),
      text_disabled_token:   cs.getPropertyValue('--text-disabled'),
      ink_token:             cs.getPropertyValue('--ink').trim(),
      muted_token:           cs.getPropertyValue('--muted').trim(),
      computed_border: cs.borderTopColor,
      computed_color:  cs.color,
    });
  });
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--frame-url-contains", default=None)
    ap.add_argument("--frame-index", type=int, default=0)
    ap.add_argument("--widths", default="1180,760")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    sys.path.insert(0, os.environ.get("PWLIBS", ""))
    from playwright.sync_api import sync_playwright

    shell = glob.glob(os.path.expanduser(os.environ.get(
        "PWSHELL", "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")))
    if not shell:
        print("FATAL: no headless_shell. Set PWSHELL. Not guessing.", file=sys.stderr)
        return 2

    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0], headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                                    "--allow-file-access-from-files"])
        for w in [int(x) for x in args.widths.split(",")]:
            pg = b.new_page(viewport={"width": w, "height": 1400})
            pg.goto(f"file://{os.path.abspath(args.file)}")
            pg.wait_for_timeout(1500)
            target = pg
            if args.frame_url_contains:
                fr = [f for f in pg.frames if args.frame_url_contains in (f.url or "")]
                if len(fr) <= args.frame_index:
                    report[w] = {"error": "frame not found"}
                    pg.close(); continue
                target = fr[args.frame_index]
            if not target.evaluate("() => document.fonts.check('16px HSBC_MtUnivers_Latin')"):
                report[w] = {"error": "licensed cut not loaded — refusing to measure"}
                pg.close(); continue
            # settle anyway: this measures a resting control, but the cost is one line
            target.evaluate("() => { const s=document.createElement('style');"
                            " s.textContent='*,*::before,*::after{transition:none !important}';"
                            " document.head.appendChild(s); }")
            pg.mouse.move(2, 2)          # never measure a control the pointer is sitting on
            pg.wait_for_timeout(60)
            rows = target.evaluate(PROBE)
            for r in rows:
                r["computed_border_parsed"] = parse_colour(r["computed_border"])
                r["ink_parsed"] = parse_colour(r["ink_token"])
                r["border_disabled_resolves"] = bool(r["border_disabled_token"].strip())
                r["text_disabled_resolves"] = bool(r["text_disabled_token"].strip())
                bp, ip = r["computed_border_parsed"], r["ink_parsed"]
                r["border_equals_ink"] = bool(
                    bp and ip and all(x is not None and y is not None and abs(x - y) < 0.02
                                      for x, y in zip(bp, ip)))
            report[w] = rows
            pg.close()
        b.close()

    out = json.dumps(report, indent=2, default=str)
    if args.out:
        open(args.out, "w").write(out)

    print("=" * 78)
    for w, rows in report.items():
        if isinstance(rows, dict):
            print(f"[{w}px] {rows}"); continue
        for r in rows:
            print(f"[{w}px] reset#{r['index']} disabled={r['matches_disabled_pseudo']} "
                  f"hovered={r['hovered']}")
            print(f"        --border-disabled -> {r['border_disabled_token']!r}  "
                  f"resolves={r['border_disabled_resolves']}")
            print(f"        --text-disabled   -> {r['text_disabled_token']!r}  "
                  f"resolves={r['text_disabled_resolves']}")
            print(f"        --ink {r['ink_token']} · computed border-color "
                  f"{r['computed_border']} · equals ink: {r['border_equals_ink']}")
            print(f"        computed color {r['computed_color']}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
