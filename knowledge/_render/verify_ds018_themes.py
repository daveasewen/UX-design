#!/usr/bin/env python3
"""
verify_ds018_themes.py — the ds-018 render-proof that was still OWED, driven across
FOUR THEMES x LIGHT+DARK (s212-D1 enactment, row W-99, session #213).

WHY THIS EXISTS
---------------
_DS-IMPROVEMENTS.md § ds-018 records the #12 enactment as "BUILD-GREEN" but
"⚠ NOT RENDER-PROVEN … **The render-proof is the one thing still owed on ds-018**".
recheck_ds018.py (#10) measured the DEFECT before the fix, on ONE theme. Nothing has
ever driven the FIXED state, and nothing has ever driven it per theme — which matters
because `data/control/label-disabled/color` aliases `color/neutral/9`, and Supercharge
rebinds neutral/* onto its own warm ramp (ADR-0014 DNA tier). So the ruled `#9D9D9D`
is THEME-RELATIVE by construction and a one-theme proof cannot see that.

WHAT IT ASSERTS, per (theme x mode) cell, on the real showroom harness:
  1. the Reset is genuinely `:disabled` AT REST (else we measured the wrong state)
  2. `--data-control-label-disabled` RESOLVES (non-empty) on the chart's own scope
     — ds-018's actual cause was that it resolved to '' and the property silently
     took its INITIAL value
  3. the resolved value equals the EXPECTED hex derived INDEPENDENTLY from
     knowledge/tokens/ (store + theme registry neutralRamp) — never read back from
     canon.css or the page, so the assertion cannot be circular
  4. computed `color` == that resolved token, COMPARED AS COLOURS (the declaration
     is DELIVERED, not merely declared)
  5. computed `color` != computed `--ink` — the ds-018 symptom was that the disabled
     control carried INK and out-shouted its own enabled state
  6. computed border-top-color == `--line` — B2 label-led, the ruled+accepted cost
  7. `--text-disabled` / `--border-disabled` do NOT resolve on the chart scope.
     ⚠ ABSENCE CLAIM — it carries a detectable-when-present arm: `--bite ds018`
     re-declares the pre-#12 binding and this assertion MUST go red.

DISCIPLINE (knowledge/_RUNBOOK-render-verify.md):
  * licensed HSBC cut asserted INSIDE the measured frame by CANVAS PROBE with two
    controls — document.fonts.check() returns true in a broken conf and cannot
    discriminate (#138).
  * transitions killed and the pointer parked BEFORE any computed read (ds-019's
    defect was reading at t=0 of a 0.16s transition).
  * colours parsed and compared AS COLOURS, never as strings.

BITES (a proof that cannot fail proves nothing — #104/#171):
  --bite ds018    re-declare `.dv-leg-reset:disabled{border-color:var(--border-disabled);
                  color:var(--text-disabled)}` in the frame  -> assertions 4/5/7 MUST fail
  --bite value    force --data-control-label-disabled:#FF0000 -> assertion 3 MUST fail
  --bite formtokens  DECLARE --text-disabled/--border-disabled on the chart scope
                  (the option A2 rejected) -> assertion 7, the ABSENCE claim, MUST fail
  --bite-the-bite force an IRRELEVANT var (--data-grid:#FF0000) -> everything MUST stay
                  green, proving the probe is not simply red on any mutation

Usage (after the runbook's env staging):
    PWLIBS=... PWSHELL=... python3 knowledge/_render/verify_ds018_themes.py
    ... --bite ds018        # expect RED
    ... --bite value        # expect RED
    ... --bite-the-bite     # expect GREEN
Exit 0 = the expectation for the selected mode was met; non-zero = it was not.
"""
from __future__ import annotations
import argparse, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))   # knowledge/_render
REPO = os.path.dirname(HERE)                        # knowledge/
ROOT = os.path.dirname(REPO)                        # repo root
sys.path.insert(0, HERE)
from cdp_matched_styles import parse_colour  # noqa: E402

TOKENS = os.path.join(REPO, "tokens")
THEMES = ["mono", "legacy", "console", "supercharge"]
MODES = ["light", "dark"]
TOKEN_PATH = "data/control/label-disabled/color"


class ProbeError(RuntimeError):
    """Fail LOUD and NAMED — a parse helper that guesses is the ds-025 defect."""


def _store(name):
    with open(os.path.join(TOKENS, name)) as fh:
        return json.load(fh)


def _dig(obj, path):
    for k in path.split("/"):
        if not isinstance(obj, dict) or k not in obj:
            raise ProbeError(f"token path not found: {path} (stopped at {k!r})")
        obj = obj[k]
    return obj


def expected_hex(theme: str, mode: str) -> str:
    """Derive the expected recessive grey from knowledge/tokens/ ALONE.

    Deliberately independent of canon.css and of the rendered page: an expectation
    read back from the artefact under test is not an expectation (#171).
    """
    node = _dig(_store("semantic-colour.json"), TOKEN_PATH)
    base = node[mode]["$value"]
    alias = node.get("$alias", {}).get(mode)          # e.g. color/neutral/9
    reg = _store("themes/_themes.json")["themes"]
    entry = next((v for v in reg.values() if v.get("attr") == theme), None)
    if entry is None:
        raise ProbeError(f"theme attr {theme!r} not in tokens/themes/_themes.json")
    ramp = entry.get("neutralRamp", "")               # e.g. "color/warm/1-15"
    if not alias or not alias.startswith("color/neutral/") or not ramp.startswith("color/"):
        return base.upper()
    fam, scale = ramp.split("/")[1], ramp.rsplit("/", 1)[1]
    # ⚠ Only the DNA-tier 1-15 ramps rebind neutral/*. Legacy declares
    # `color/grey/100-800` and the registry says so in its own words: "Legacy stays
    # explicit-per-path (reproduction, R-D24 posture) and does not ride the DNA tier."
    # A theme off the DNA scale therefore resolves to the BASE value, not to a
    # step number that does not exist on its ramp.
    if scale != "1-15" or fam in ("mono", "neutral"):
        return base.upper()
    step = alias.rsplit("/", 1)[1]
    return _dig(_store("colour.json"), f"color/{fam}/{step}")["$value"].upper()


FONT_PROBE = """
() => {
  const c = document.createElement('canvas').getContext('2d');
  const w = f => { c.font = '40px ' + f; return c.measureText('Handgloves 12345').width; };
  return {
    target: w('HSBC_MtUnivers_Latin'),
    alias:  w('"Univers Next for HSBC"'),
    real:   w('DejaVu Sans'),
    ghost:  w('__no_such_face__'),
  };
}
"""

SETTLE = """
() => { const s = document.createElement('style');
        s.setAttribute('data-probe','settle');
        s.textContent = '*,*::before,*::after{transition:none !important;animation:none !important}';
        document.head.appendChild(s); }
"""

BITES = {
    "ds018": ".dv-leg-reset:disabled{border-color:var(--border-disabled) !important;"
             "color:var(--text-disabled) !important;}",
    "value": "[data-theme]{--data-control-label-disabled:#FF0000 !important;}",
    # A7 is an ABSENCE claim, so it needs its own detectable-when-present arm: the
    # `ds018` bite only RE-CONSUMES the form tokens, it does not DECLARE them, so A7
    # stays (correctly) green under it. This bite declares them on the chart scope —
    # the A2 "import the form ladder wholesale" option ds-018 rejected — and A7 must
    # then go red. Without this, A7 would be an unfalsified absence.
    "formtokens": "[data-theme]{--text-disabled:#E1E1E1;--border-disabled:#E1E1E1;}",
    "irrelevant": "[data-theme]{--data-grid:#FF0000 !important;}",
}

READ = """
() => {
  const el = document.querySelector('.dv-leg-reset');
  if (!el) return {error: 'no .dv-leg-reset in this frame'};
  const cs = getComputedStyle(el);
  return {
    disabled_property: el.disabled === true,
    matches_disabled_pseudo: el.matches(':disabled'),
    hovered: el.matches(':hover'),
    token_label_disabled: cs.getPropertyValue('--data-control-label-disabled').trim(),
    token_text_disabled: cs.getPropertyValue('--text-disabled').trim(),
    token_border_disabled: cs.getPropertyValue('--border-disabled').trim(),
    token_line: cs.getPropertyValue('--line').trim(),
    token_ink: cs.getPropertyValue('--ink').trim(),
    computed_color: cs.color,
    computed_border: cs.borderTopColor,
  };
}
"""


def same_colour(a, b, tol=0.02):
    pa, pb = parse_colour(a), parse_colour(b)
    if not pa or not pb:
        return False
    return all(x is not None and y is not None and abs(x - y) < tol for x, y in zip(pa, pb))


def assess(row, theme, mode, exp):
    """Return list of (id, ok, detail). NEVER swallows a missing value as a pass."""
    out = []
    add = lambda i, ok, d: out.append((i, bool(ok), d))
    if row.get("error"):
        add("A0 frame", False, row["error"])
        return out
    add("A1 disabled-at-rest",
        row["disabled_property"] and row["matches_disabled_pseudo"] and not row["hovered"],
        f"disabled={row['disabled_property']} pseudo={row['matches_disabled_pseudo']} hovered={row['hovered']}")
    add("A2 token-resolves", bool(row["token_label_disabled"]),
        f"--data-control-label-disabled={row['token_label_disabled']!r}")
    add("A3 token==expected", same_colour(row["token_label_disabled"], exp),
        f"got {row['token_label_disabled']!r} expected {exp} (derived from tokens/)")
    add("A4 colour-delivered", same_colour(row["computed_color"], row["token_label_disabled"]),
        f"computed color {row['computed_color']} vs token {row['token_label_disabled']}")
    add("A5 not-ink", not same_colour(row["computed_color"], row["token_ink"]),
        f"computed color {row['computed_color']} vs --ink {row['token_ink']}")
    add("A6 border==line", same_colour(row["computed_border"], row["token_line"]),
        f"border {row['computed_border']} vs --line {row['token_line']}")
    add("A7 form-tokens-absent",
        not row["token_text_disabled"] and not row["token_border_disabled"],
        f"--text-disabled={row['token_text_disabled']!r} --border-disabled={row['token_border_disabled']!r}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", default=os.path.join(ROOT, "showroom", "chart-bar.html"))
    ap.add_argument("--width", type=int, default=1180)
    ap.add_argument("--bite", choices=["ds018", "value", "formtokens"], default=None)
    ap.add_argument("--bite-the-bite", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.bite and args.bite_the_bite:
        raise ProbeError("--bite and --bite-the-bite are mutually exclusive")
    inject = BITES["irrelevant"] if args.bite_the_bite else (BITES[args.bite] if args.bite else None)
    expect_red = bool(args.bite)

    sys.path.insert(0, os.environ.get("PWLIBS", ""))
    from playwright.sync_api import sync_playwright

    shell = glob.glob(os.environ.get(
        "PWSHELL", os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")))
    if not shell:
        raise ProbeError("no headless_shell — set PWSHELL. Not guessing (ds-025).")

    report, failures = {}, 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell[0], headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                                    "--allow-file-access-from-files"])
        for theme in THEMES:
            for mode in MODES:
                cell = f"{theme}/{mode}"
                pg = b.new_page(viewport={"width": args.width, "height": 1400})
                pg.goto(f"file://{os.path.abspath(args.page)}#theme={theme}&m={mode}")
                pg.wait_for_timeout(1500)
                frames = [f for f in pg.frames if "srcdoc" in (f.url or "")]
                if not frames:
                    report[cell] = {"error": "srcdoc frame not found"}
                    failures += 1
                    pg.close()
                    continue
                fr = frames[0]
                fp = fr.evaluate(FONT_PROBE)
                if not (abs(fp["target"] - fp["alias"]) < 0.5 and abs(fp["target"] - fp["ghost"]) > 0.5
                        and abs(fp["target"] - fp["real"]) > 0.5):
                    report[cell] = {"error": f"licensed cut NOT loaded — refusing to measure ({fp})"}
                    failures += 1
                    pg.close()
                    continue
                fr.evaluate(SETTLE)
                if inject:
                    fr.evaluate("(css) => { const s=document.createElement('style');"
                                " s.setAttribute('data-probe','bite'); s.textContent=css;"
                                " document.head.appendChild(s); }", inject)
                pg.mouse.move(2, 2)          # never measure a control the pointer sits on
                pg.wait_for_timeout(80)
                row = fr.evaluate(READ)
                exp = expected_hex(theme, mode)
                checks = assess(row, theme, mode, exp)
                row["_expected"] = exp
                row["_checks"] = [{"id": i, "ok": ok, "detail": d} for i, ok, d in checks]
                report[cell] = row
                failures += sum(1 for _, ok, _ in checks if not ok)
                pg.close()
        b.close()

    print("=" * 90)
    mode_label = ("BITE:" + args.bite) if args.bite else ("BITE-THE-BITE" if args.bite_the_bite else "GREEN CONTROL")
    print(f"ds-018 four-theme render-proof — {mode_label} — page {os.path.relpath(args.page, ROOT)} @ {args.width}px")
    print("=" * 90)
    for cell, row in report.items():
        if row.get("error"):
            print(f"  {cell:22s} ❌ {row['error']}")
            continue
        bad = [c for c in row["_checks"] if not c["ok"]]
        flag = "✅" if not bad else "❌"
        print(f"  {cell:22s} {flag} token={row['token_label_disabled']:<9} expected={row['_expected']:<9} "
              f"color={row['computed_color']:<20} border={row['computed_border']}")
        for c in bad:
            print(f"      ↳ FAIL {c['id']}: {c['detail']}")
    print("-" * 90)
    print(f"{len(report)} cell(s) · {failures} failed assertion(s)")

    if args.out:
        with open(args.out, "w") as fh:
            json.dump(report, fh, indent=2, default=str)

    if expect_red:
        ok = failures > 0
        print(f"BITE EXPECTATION: red required — {'MET' if ok else 'NOT MET (the probe cannot fail — it proves nothing)'}")
        return 0 if ok else 3
    ok = failures == 0
    label = "bite-the-bite" if args.bite_the_bite else "green control"
    print(f"{label.upper()} EXPECTATION: green required — {'MET' if ok else 'NOT MET'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
