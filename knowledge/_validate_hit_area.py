#!/usr/bin/env python3
"""_validate_hit_area.py — the 44px minimum-hit-area consumer (ADVISORY tier).

WHY THIS EXISTS
---------------
`knowledge/tokens/layout.json` mints `target/min = 44px` — "the Apollo hit-area standard
(RULED by Dave 2026-07-24)… 44 = HSBC default / WCAG 2.5.5 AAA / Apple HIG / IBM Carbon.
Dial-down floor is 24 (WCAG 2.5.8 AA + spacing exception); never below."
**No gate has ever read that token.** A minted token with no consumer cannot fail, so real
breaches survived in shipped, gated components for weeks:

  * `Amount-input` — `.ai-box` standard money field renders **380 × 39** at 1180px and
    **457 × 39** at 480px: 5px under the ruled minimum, on the field a customer taps to
    enter money on a phone (measured #203 wave 3a, Lane C receipt finding 2).
  * `Secure-entry` — `.se-cell` OTP cell renders **42 × 50** at ≤480px: 2px under on the
    width, at exactly the breakpoint where a one-handed thumb enters an OTP (Lane C
    finding 3 — and note Lane C's own correction: read off the stylesheet the cell looks
    40px; the RENDERED box is 42px. A number read off CSS is not a measurement).

So this instrument measures **rendered geometry in a real browser at real viewport widths**,
never CSS text. That is the whole point: no static parse of `canon.css` could have produced
either number, because both come from padding + border + flex resolution at a breakpoint.

THE PSEUDO-ELEMENT EXPANDER — why a naive box measurement would be WRONG
------------------------------------------------------------------------
The canon idiom (`canon.css:1804-1805`, aid-009, copied from `.dv-vt`/`.dv-tbl-toggle`) is an
INVISIBLE `::before` that expands the hit area beyond the visible box:

    .cn-input-fields .help-btn::before{content:""; position:absolute; z-index:0;
      min-width:var(--hit,44px); min-height:var(--hit,44px); width:100%; height:100%;
      top:50%; left:50%; transform:translate(-50%,-50%);}

`.help-btn`'s visible box is **18 × 18** — and it is CORRECT, because its `::before` measures
44 × 44. A gate that read only `getBoundingClientRect()` would report a false breach on every
correctly-built control in the library. This gate therefore takes the **union of the element
box and any absolutely/fixed-positioned pseudo-element** (`::before`, `::after`) whose
`content` is not `none`, using the pseudo's USED width/height from `getComputedStyle(el, ps)`.
Driven, both legs (#203 Lane L):
  `.help-btn`      box 18 × 18   ::before 44 × 44        → PASS
  `.seg button`    box 48.3 × 32 ::before 48.28 × 44     → PASS  (Segmented-control, the token's
                                                                  own stated reference impl)
  `Button button`  box 105.9 × 44, no pseudo             → PASS
Run with `--ignore-pseudo` to switch the union off: `.help-btn` and `.seg button` flip to
UNDER. That is the built-in mutation lever — it proves the union is load-bearing and that the
gate CAN go red on a known-good file, i.e. the clause is real, not vacuous.

THE FIELD SHELL — the second reason a bare rect lies
-----------------------------------------------------
`.ai-box{padding:8px 16px}` + `.ai-box input{padding:0}`: the `<input>`'s own rect is **21px**,
while the bordered field a customer sees and taps is **39px**. Measuring the input alone would
have reported a −23px BREACH-FLOOR on a control whose real defect is −5px. So a form control
unions with its **field shell** — bounded: form controls only, ≤2 ancestors, the ancestor must
PAINT (border or non-transparent background) and must hold exactly ONE interactive descendant,
so `.se-cells` (six OTP inputs) is rejected and cannot mask its children. `--ignore-shell` is
the mutation lever: `Amount-input` flips UNDER (−5) → BREACH-FLOOR (−23).

THE HIT TEST — the third, and the one that invalidated this gate's first draft
------------------------------------------------------------------------------
**A bounding rect is not a hit region.** The canon leading trim (`text-box-trim:trim-both`,
ds-005) shrinks an anchor's rect to its CAP-HEIGHT span: `Breadcrumbs .crumb` measures
**39.4 × 10.1**. The first draft of this gate duly reported a −34px BREACH-FLOOR on it — and
that was WRONG: `document.elementFromPoint` returns the anchor 6px above and 6px below that
box, because the LINE box is what Chromium hit-tests. So the effective size is measured by
walking `elementFromPoint` outward from the target's centre (`--ignore-hittest` to switch off)
and taking the contiguous span it owns; occlusion truncates the walk, which is correct — an
overlapped strip is not clickable. The crumb reads **19px**, still under, but a −25 finding
rather than a phantom −34. Every leading-trimmed text link in the library was mis-measured by
the geometric reading; the sweep table's numbers are the hit-tested ones.
⚠ Calibration: the span is counted as sides-only (no centre pixel), because `Button`'s 44px
must read 44, not 45 — a +1 bias would have silently passed a 43px control.

⬛ EXEMPT, and why: **SVG data marks** (`rect.dv-series`, `circle.dv-hit`, `g.dv-marker`, donut
segments…) carry `tabindex`/roles and would otherwise dominate the sweep with ~350 findings.
Their geometry is data-determined, which is 2.5.5's *essential* exception, and every canon
chart ships an accessible data-table alternative. Counted and named in the report, never
silently dropped.

⬛ DECLARED LIMITATION (not a silent one): the union takes the pseudo's SIZE and assumes the
canon centring (`top/left:50% + translate(-50%,-50%)`). It does not verify the anchor offsets,
so a 44 × 44 expander deliberately parked off to one side would be scored as if centred. The
9-point anchor matrix in the token's `$description` is unmodelled. Also unmodelled: WCAG
2.5.8's spacing exception (an undersized target with ≥44px of clear space around it is
conformant) — so an UNDER verdict here is a SIGNAL to look, not a proof of non-conformance.
That is exactly why the tier is ADVISORY.

TIER — ADVISORY, and deliberately not wired
--------------------------------------------
⛔ NOT wired into `_build_all.py`. Wiring it, and any remedy for what it finds, is Dave's /
the conductor's call (#203 brief, Lane L fence). Exit code is **0 even with findings**; pass
`--strict` to get exit 1 on any UNDER/BREACH (for whoever eventually wires it). Exit **2** is
reserved for a harness failure (no Playwright, no browser) — an instrument that cannot run
must say so LOUD and NAMED, never return a green that means "I did not look".

VERDICTS
--------
  PASS            effective w ≥ min AND effective h ≥ min           (default min 44)
  UNDER           below min but ≥ the dial-down floor (24)
  BREACH-FLOOR    below 24 — "never below" per the token
  EXEMPT          disabled/inert · inline link in text flow (2.5.8 inline exception) ·
                  sr-only · zero-box / not rendered · aria-hidden subtree
Every exemption is COUNTED and listed by reason — an exemption that nobody can see is how a
sweep launders its own blind spots.

HARNESS
-------
Headless Chromium via Playwright, per `knowledge/_RUNBOOK-render-verify.md`:
`goto file://…` (⛔ `set_content()` is BANNED — it drops type.css silently), the fontconfig
symlink farm, and the `document.fonts.check('16px HSBC_MtUnivers_Latin')` assertion so a page
measured in a fallback face is reported, not silently trusted. Render the SNIPPET
(`knowledge/snippets/<X>.reference.html`), never the showroom harness page (it iframes the
component, so a top-frame query finds nothing and returns a clean empty pass).

Usage:
  python3 knowledge/_validate_hit_area.py --all                 # sweep every gated snippet
  python3 knowledge/_validate_hit_area.py knowledge/snippets/Amount-input.reference.html
  python3 knowledge/_validate_hit_area.py --all --widths 1180,480,320
  python3 knowledge/_validate_hit_area.py --all --out knowledge/_HIT-AREA-ADVISORY.md
  python3 knowledge/_validate_hit_area.py --all --ignore-pseudo # mutation lever (see above)
  python3 knowledge/_validate_hit_area.py --selftest            # acceptance: the 3 known cases
Exit 0 = ran (advisory) · 1 = --strict with findings · 2 = harness unavailable / selftest fail.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SNIPPETS = os.path.join(HERE, "snippets")

MIN_DEFAULT = 44          # tokens/layout.json  target/min — CONTROL tier
MARK_TARGET = 24          # s116-D1 (Dave, #116): data marks held to the 24×24 WCAG 2.5.8
                          # dense case — "exempt from the 44 CONTROL target, NOT exempt
                          # from the check"; the chart's table fallback is the stated
                          # justification. Mirrors TARGET_MARK in _a11y_target.py:61.
FLOOR = 24                # the token's stated dial-down floor, "never below"

# ---------------------------------------------------------------- the page probe
# Runs IN the page. Returns one record per interactive candidate. Everything it
# reports is a MEASUREMENT (px from the layout engine), never a parse of CSS text.
PROBE_JS = r"""
(opts) => {
  const SEL = [
    'button', 'a[href]', 'input', 'select', 'textarea', 'summary',
    '[role="button"]', '[role="link"]', '[role="tab"]', '[role="switch"]',
    '[role="checkbox"]', '[role="radio"]', '[role="menuitem"]',
    '[role="menuitemcheckbox"]', '[role="menuitemradio"]', '[role="option"]',
    '[role="slider"]', '[role="spinbutton"]', '[role="combobox"]',
    '[tabindex]:not([tabindex="-1"])', '[onclick]'
  ].join(',');

  const px = (s) => { const v = parseFloat(s); return isNaN(v) ? 0 : v; };
  const label = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.classList.length) s += '.' + [...el.classList].join('.');
    const t = (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ');
    return s + (t ? ' “' + t.slice(0, 28) + '”' : '');
  };

  const out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll(SEL)) {
    if (seen.has(el)) continue;
    seen.add(el);
    const cs = getComputedStyle(el);
    const r  = el.getBoundingClientRect();
    const rec = {
      sel: label(el),
      tag: el.tagName.toLowerCase(),
      box: [+r.width.toFixed(1), +r.height.toFixed(1)],
      pseudo: null,
      exempt: null,
      tier: 'control',
    };

    // --- exemptions, each NAMED (a silent skip is a laundered blind spot) ---
    // s116-D1 (Dave, #116): "Data marks are held to the 24x24 WCAG 2.5.8 dense-case
    // MINIMUM — exempt from the 44 CONTROL target, NOT exempt from the check."
    // So a mark is a TIER, never an exemption.
    if (/^(rect|circle|ellipse|path|polyline|polygon|line|g)$/.test(rec.tag) && el.closest('svg')) {
      rec.tier = 'mark';
    }
    if (el.closest('[aria-hidden="true"]'))              rec.exempt = 'aria-hidden subtree';
    else if (el.disabled || el.closest('[inert]'))       rec.exempt = 'disabled/inert (2.5.5 exception)';
    else if (el.type === 'hidden')                       rec.exempt = 'input[type=hidden]';
    else if (cs.display === 'none' || cs.visibility === 'hidden') rec.exempt = 'not rendered';
    else if (r.width <= 1 || r.height <= 1) {
      rec.exempt = (cs.position === 'absolute' && (cs.clip !== 'auto' || cs.clipPath !== 'none'))
        ? 'sr-only' : 'zero-box';
    } else if (el.tagName === 'A' && cs.display.startsWith('inline') &&
               el.parentElement && /^(P|LI|SPAN|TD|DD|DT|LABEL|SMALL|EM|STRONG)$/.test(el.parentElement.tagName)) {
      rec.exempt = 'inline link in text (2.5.8 inline exception)';
    }
    if (rec.exempt) { out.push(rec); continue; }

    // --- the union with any absolutely-positioned pseudo expander ---
    let w = r.width, h = r.height;
    if (!opts.ignorePseudo) {
      for (const ps of ['::before', '::after']) {
        const p = getComputedStyle(el, ps);
        if (!p || p.content === 'none' || p.content === 'normal') continue;
        if (p.position !== 'absolute' && p.position !== 'fixed') continue;
        const pw = Math.max(px(p.width), px(p.minWidth));
        const ph = Math.max(px(p.height), px(p.minHeight));
        if (pw > w || ph > h) {
          rec.pseudo = [ps, +pw.toFixed(1), +ph.toFixed(1)];
          w = Math.max(w, pw); h = Math.max(h, ph);
        }
      }
    }
    // --- the FIELD-SHELL union (see docstring: "the shell IS the field") ---
    // A text field's visible tap target is the bordered shell its padding lives on,
    // not the bare <input>: `.ai-box{padding:8px 16px}` + `.ai-box input{padding:0}`
    // means the input's own rect is ~23px while the field a customer sees is 39px.
    // Bounded on purpose: form controls only, <=2 levels up, the ancestor must PAINT
    // (border or non-transparent background) and must hold exactly ONE interactive
    // descendant - so `.se-cells` (six OTP inputs) is rejected and cannot mask.
    rec.shell = null;
    if (!opts.ignoreShell && /^(input|select|textarea)$/.test(rec.tag)) {
      let a = el.parentElement;
      for (let lvl = 0; lvl < 2 && a; lvl++, a = a.parentElement) {
        const acs = getComputedStyle(a), ar = a.getBoundingClientRect();
        const paints = px(acs.borderTopWidth) > 0 || px(acs.borderBottomWidth) > 0 ||
          (acs.backgroundColor !== 'rgba(0, 0, 0, 0)' && acs.backgroundColor !== 'transparent');
        const solo = a.querySelectorAll(SEL).length === 1 || a.tagName === 'LABEL';
        const contains = ar.width >= r.width - 0.5 && ar.height >= r.height - 0.5;
        if (paints && solo && contains && (ar.width > w || ar.height > h)) {
          rec.shell = [label(a).split(' ')[0], +ar.width.toFixed(1), +ar.height.toFixed(1)];
          w = Math.max(w, ar.width); h = Math.max(h, ar.height);
          break;
        }
      }
    }
    // --- THE HIT TEST: what the browser actually routes a tap to ---------------
    // A bounding rect is NOT a hit region. `text-box-trim:trim-both` (canon leading
    // trim, ds-005) shrinks an anchor's rect to its CAP-HEIGHT span — `.crumb`
    // measures 39.4 × 10.1 — while `document.elementFromPoint` still returns the
    // anchor 6px above and below that box, because the LINE box is what hit-tests.
    // Measuring the rect alone would have reported a −34px breach on a link that is
    // ~22px tall in the only sense that matters to a thumb. So we walk
    // elementFromPoint outward from the centre and report the contiguous span.
    // Occlusion truncates the walk, which is correct: an overlapped strip is not
    // clickable. Elements whose centre is occluded or unhittable fall back to the
    // geometric union above and are marked so.
    rec.hit = null;
    if (!opts.ignoreHittest) {
      try { el.scrollIntoView({ block: 'center', inline: 'center' }); } catch (e) {}
      const rr = el.getBoundingClientRect();
      const cx = Math.round(rr.x + rr.width / 2), cy = Math.round(rr.y + rr.height / 2);
      const owns = (n) => !!n && (n === el || el.contains(n));
      if (cx >= 0 && cy >= 0 && cx <= innerWidth && cy <= innerHeight &&
          owns(document.elementFromPoint(cx, cy))) {
        const CAP = 48;   // past the 44 threshold there is nothing to learn
        const grow = (dx, dy) => {
          let d = 1;
          while (d <= CAP && owns(document.elementFromPoint(cx + dx * d, cy + dy * d))) d++;
          return d - 1;
        };
        // NB: sides only, no +1 for the centre pixel — calibrated against Button,
        // whose 44px geometric height must read 44, not 45 (an off-by-one here
        // would silently pass a 43px control).
        const hw = grow(-1, 0) + grow(1, 0), hh = grow(0, -1) + grow(0, 1);
        rec.hit = [hw, hh];
        w = Math.max(w, hw); h = Math.max(h, hh);
      } else {
        rec.hitNote = 'centre not hittable — geometric reading only';
      }
    }

    rec.eff = [+w.toFixed(1), +h.toFixed(1)];
    out.push(rec);
  }
  return out;
}
"""


def _shell_path():
    """Locate the headless shell. Fails LOUD and NAMED, never guesses."""
    roots = []
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        roots.append(os.environ["PLAYWRIGHT_BROWSERS_PATH"])
    roots += glob.glob("/var/tmp/pw-browsers*")
    roots.append(os.path.expanduser("~/.cache/ms-playwright"))
    for root in roots:
        hits = sorted(glob.glob(os.path.join(
            root, "chromium_headless_shell-*", "chrome-linux", "headless_shell")))
        if hits:
            return hits[-1]
        hits = sorted(glob.glob(os.path.join(root, "chromium-*", "chrome-linux", "chrome")))
        if hits:
            return hits[-1]
    return None


def measure(files, widths, ignore_pseudo=False, minimum=MIN_DEFAULT, quiet=False,
            ignore_shell=False, ignore_hittest=False):
    """Render each file at each width and return (rows, font_ok_map).

    A harness problem raises RuntimeError — the caller turns that into exit 2.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:                                   # loud, named
        raise RuntimeError(
            "HIT-AREA: HARNESS UNAVAILABLE — playwright not importable (%s). "
            "Stage it per knowledge/_RUNBOOK-render-verify.md "
            "(PYTHONPATH=/var/tmp/pylibs-s<n>); this is NOT a pass." % exc)
    shell = _shell_path()
    if not shell:
        raise RuntimeError(
            "HIT-AREA: HARNESS UNAVAILABLE — no chromium headless_shell found under "
            "PLAYWRIGHT_BROWSERS_PATH / /var/tmp/pw-browsers* / ~/.cache/ms-playwright. "
            "See _RUNBOOK-render-verify.md step 3; this is NOT a pass.")

    rows, fonts = [], {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=shell, headless=True,
                              args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
        try:
            for f in files:
                name = os.path.basename(f).replace(".reference.html", "")
                for w in widths:
                    pg = b.new_page(viewport={"width": w, "height": 1400})
                    try:
                        pg.goto("file://" + os.path.abspath(f))   # ⛔ never set_content()
                        pg.wait_for_timeout(500)                  # settle entry motion/transitions
                        try:
                            fonts[name] = bool(pg.evaluate(
                                "document.fonts.check('16px HSBC_MtUnivers_Latin')"))
                        except Exception:
                            fonts[name] = None
                        recs = pg.evaluate(PROBE_JS, {"ignorePseudo": ignore_pseudo,
                                                      "ignoreShell": ignore_shell,
                                                      "ignoreHittest": ignore_hittest})
                    finally:
                        pg.close()
                    for rec in recs:
                        rec["file"] = name
                        rec["width"] = w
                        if rec.get("exempt"):
                            rec["verdict"] = "EXEMPT"
                        else:
                            # s116-D1: marks are held to 24, controls to 44.
                            tgt = MARK_TARGET if rec.get("tier") == "mark" else minimum
                            rec["target"] = tgt
                            e = rec["eff"]
                            small = min(e[0], e[1])
                            rec["verdict"] = ("PASS" if small >= tgt
                                              else "BREACH-FLOOR" if small < FLOOR else "UNDER")
                            rec["deficit"] = round(tgt - small, 1) if small < tgt else 0
                        rows.append(rec)
                    if not quiet:
                        bad = [r for r in recs if r.get("verdict") in ("UNDER", "BREACH-FLOOR")]
                        print("  %-22s @%-5s %3d candidates, %d finding(s)"
                              % (name, w, len(recs), len(bad)), flush=True)
        finally:
            b.close()
    return rows, fonts


def render_report(rows, fonts, widths, minimum, ignore_pseudo, scanned=None):
    findings = [r for r in rows if r["verdict"] in ("UNDER", "BREACH-FLOOR")]
    exempt = [r for r in rows if r["verdict"] == "EXEMPT"]
    checked = [r for r in rows if r["verdict"] != "EXEMPT"]
    files = sorted({r["file"] for r in rows})
    L = []
    L.append("# Hit-area advisory — the 44px minimum, measured on RENDERED geometry\n")
    L.append("*Auto-generated by `_validate_hit_area.py` (ADVISORY, non-gating, NOT wired into "
             "`_build_all.py`). Threshold `target/min = %dpx` from `knowledge/tokens/layout.json`; "
             "dial-down floor %dpx. An UNDER verdict is a SIGNAL to look — WCAG 2.5.8's spacing "
             "exception and pseudo-anchor offsets are unmodelled (see the module docstring's "
             "DECLARED LIMITATION).*\n" % (minimum, FLOOR))
    if ignore_pseudo:
        L.append("⚠ **`--ignore-pseudo` MUTATION RUN** — the pseudo-expander union is switched "
                 "OFF. Findings below include known-good controls by design. Not a sweep.\n")
    marks = [r for r in checked if r.get("tier") == "mark"]
    ctrl_find = [r for r in findings if r.get("tier") != "mark"]
    mark_find = [r for r in findings if r.get("tier") == "mark"]
    L.append("**%d snippet(s) scanned%s · %d with interactive candidates · %s px · "
             "%d target(s) measured (%d control @%dpx, %d mark @%dpx per `s116-D1`) · "
             "%d exempt · %d finding(s) — %d control, %d mark.**\n"
             % (len(scanned) if scanned else len(files),
                "" if scanned else " (files producing rows)",
                len(files), "/".join(str(w) for w in widths), len(checked),
                len(checked) - len(marks), int(minimum), len(marks), MARK_TARGET,
                len(exempt), len(findings), len(ctrl_find), len(mark_find)))
    L.append("*Prior art, and how this differs — `_validate_a11y.py` + `_a11y_target.py` "
             "(rebuilt #116 under `s114-D5`, wired into `_build_all.py`) already gate hit area "
             "**from the MARKUP**, parsing declared sizes out of the stylesheet. This instrument "
             "measures **rendered geometry in a browser at real viewport widths**, so it sees "
             "what a static parse states it must not guess at: layout- and breakpoint-determined "
             "sizes (`_a11y_target.py`: \"the other axis is layout-determined … this gate must "
             "not guess a size\"). The two are complements; the differential is the interesting "
             "output. Tiers and targets are kept identical to `_a11y_target.py:60-63` on purpose.*\n")
    bad_font = sorted(k for k, v in fonts.items() if v is not True)
    if bad_font:
        L.append("⚠ **HSBC face NOT asserted** on: %s — geometry measured in a fallback face is "
                 "suspect (`_RUNBOOK-render-verify.md`: assert with a control).\n"
                 % ", ".join(bad_font))

    L.append("\n*Reading the `from` column: `hit-test W × H` is the contiguous span "
             "`elementFromPoint` routes to the target, walked outward from its centre and "
             "**capped at 48px per side** (96 max) — a capped width is not a defect, the "
             "verdict always uses the larger of the geometric and hit-tested readings. "
             "`shell` = the bordered field wrapper a form control was unioned with. "
             "`::before/::after` = an invisible hit expander.*\n")
    L.append("\n## Findings\n")
    if not findings:
        L.append("_None._\n")
    else:
        L.append("| file | @px | target | tier | own box | effective | from | verdict | deficit |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for r in sorted(findings, key=lambda r: (-r["deficit"], r["file"], r["width"])):
            src = []
            if r.get("hit"):
                src.append("hit-test %g × %g" % tuple(r["hit"]))
            if r.get("shell"):
                src.append("shell `%s` %g × %g" % tuple(r["shell"]))
            if r.get("pseudo"):
                src.append("`%s` %g × %g" % tuple(r["pseudo"]))
            if r.get("hitNote"):
                src.append("⚠ " + r["hitNote"])
            src = " · ".join(src) or "own box"
            L.append("| `%s` | %s | `%s` | %s %g | %g × %g | **%g × %g** | %s | %s | −%gpx |"
                     % (r["file"], r["width"], r["sel"], r.get("tier", "control"),
                        r.get("target", minimum), r["box"][0], r["box"][1],
                        r["eff"][0], r["eff"][1], src, r["verdict"], r["deficit"]))
        L.append("")

    L.append("\n## Full sweep — per file\n")
    L.append("| file | @px | measured | pass | under | exempt | worst target |")
    L.append("|---|---|---|---|---|---|---|")
    for f in files:
        for w in widths:
            sub = [r for r in rows if r["file"] == f and r["width"] == w]
            if not sub:
                continue
            ch = [r for r in sub if r["verdict"] != "EXEMPT"]
            bad = [r for r in ch if r["verdict"] != "PASS"]
            worst = min(ch, key=lambda r: min(r["eff"])) if ch else None
            L.append("| `%s` | %s | %d | %d | %d | %d | %s |"
                     % (f, w, len(ch), len(ch) - len(bad), len(bad), len(sub) - len(ch),
                        ("`%s` %g × %g" % (worst["sel"].split(" ")[0], worst["eff"][0],
                                           worst["eff"][1])) if worst else "—"))
    L.append("")

    if scanned:
        silent = sorted(set(scanned) - set(files))
        L.append("\n## Scanned with NO interactive candidate (%d of %d)\n" % (len(silent), len(scanned)))
        L.append("*A file that produces no rows would otherwise vanish from the table above — "
                 "an absence has to be visible to be checkable. These are display-only "
                 "components; if one of them acquires a control, it should appear above.*\n")
        L.append(", ".join("`%s`" % s for s in silent) if silent else "_None._")
        L.append("")

    reasons = {}
    for r in exempt:
        reasons[r["exempt"]] = reasons.get(r["exempt"], 0) + 1
    L.append("\n## Exemptions, by reason (counted, never silent)\n")
    for k, v in sorted(reasons.items(), key=lambda kv: -kv[1]):
        L.append("- **%d** — %s" % (v, k))
    L.append("")
    return "\n".join(L)


# ------------------------------------------------------------------- selftest
# ACCEPTANCE (#203 Lane L brief): the instrument is only real once it has run on
# real data and caught the KNOWN failures. Two real breaches + one known-good.
SELFTEST = [
    # (file,               width, selector-substring, expect-verdict, note)
    ("Amount-input",  1180, ".ai-box", "UNDER", "39px standard money field, Lane C finding 2"),
    ("Amount-input",   480, ".ai-box", "UNDER", "39px at the narrow breakpoint too"),
    ("Secure-entry",   480, ".se-cell", "UNDER", "42px OTP cell ≤480px, Lane C finding 3"),
    ("Secure-entry",  1180, ".se-cell", "PASS", "50 × 58 at desktop — must NOT fire"),
    ("Button",        1180, "button", "PASS", "known-good 44px control"),
    ("Input-fields",  1180, ".help-btn", "PASS", "18px box + 44px ::before expander"),
]


def selftest(minimum):
    files = [os.path.join(SNIPPETS, n + ".reference.html")
             for n in ("Amount-input", "Secure-entry", "Button", "Input-fields")]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print("✖ HIT-AREA SELFTEST: missing fixture(s): %s" % missing, file=sys.stderr)
        return 2
    rows, _ = measure(files, [1180, 480], minimum=minimum, quiet=True)
    ok = True
    print("\nAcceptance — known breaches must be CAUGHT, known-good must PASS:")
    for f, w, sub, want, note in SELFTEST:
        hits = [r for r in rows if r["file"] == f and r["width"] == w
                and (sub in r["sel"] or (r.get("shell") and sub in r["shell"][0]))
                and r["verdict"] != "EXEMPT"]
        if not hits:
            print("  ✖ %-14s @%-5s %-10s NO MATCH (%s)" % (f, w, sub, note))
            ok = False
            continue
        got = min(hits, key=lambda r: min(r["eff"]))
        good = got["verdict"] == want
        ok = ok and good
        print("  %s %-14s @%-5s %-10s want %-5s got %-13s (%g × %g)  %s"
              % ("✔" if good else "✖", f, w, sub, want, got["verdict"],
                 got["eff"][0], got["eff"][1], note))
    print("SELFTEST %s" % ("PASS — the instrument catches both known breaches and clears the "
                           "known-good controls." if ok else "FAIL"))
    return 0 if ok else 2


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true", help="sweep knowledge/snippets/*.reference.html")
    ap.add_argument("--widths", default="1180,480")
    ap.add_argument("--min", type=float, default=MIN_DEFAULT)
    ap.add_argument("--ignore-pseudo", action="store_true", help="mutation lever, see docstring")
    ap.add_argument("--ignore-shell", action="store_true", help="mutation lever, see docstring")
    ap.add_argument("--ignore-hittest", action="store_true", help="mutation lever, see docstring")
    ap.add_argument("--out", default=None, help="write the advisory markdown here")
    ap.add_argument("--json", default=None, help="write a machine-readable sidecar here")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any finding")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0
    if a.selftest:
        return selftest(a.min)

    files = sorted(glob.glob(os.path.join(SNIPPETS, "*.reference.html"))) if a.all else \
        [f for f in a.files]
    if not files:
        print("✖ HIT-AREA: no input files. Pass paths or --all. (`--help` for the contract.)",
              file=sys.stderr)
        return 2
    widths = [int(x) for x in a.widths.split(",") if x.strip()]

    print("Hit-area sweep — %d file(s) × %s px, min %gpx%s"
          % (len(files), "/".join(map(str, widths)), a.min,
             "  [--ignore-pseudo MUTATION]" if a.ignore_pseudo else ""))
    rows, fonts = measure(files, widths, a.ignore_pseudo, a.min, ignore_shell=a.ignore_shell,
                          ignore_hittest=a.ignore_hittest)
    findings = [r for r in rows if r["verdict"] in ("UNDER", "BREACH-FLOOR")]
    report = render_report(rows, fonts, widths, a.min, a.ignore_pseudo,
                           scanned=[os.path.basename(f).replace(".reference.html", "")
                                    for f in files])

    if a.out:
        with open(a.out, "w") as fh:
            fh.write(report)
        print("wrote %s" % a.out)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump({"min": a.min, "floor": FLOOR, "widths": widths,
                       "ignore_pseudo": a.ignore_pseudo, "rows": rows, "fonts": fonts},
                      fh, indent=1)
        print("wrote %s" % a.json)
    if not a.out:
        print(report)

    checked = [r for r in rows if r["verdict"] != "EXEMPT"]
    print("\nADVISORY: %d target(s) measured, %d finding(s), %d exempt."
          % (len(checked), len(findings), len(rows) - len(checked)))
    for r in sorted(findings, key=lambda r: -r["deficit"])[:12]:
        print("  %-14s @%-5s %-42s %g × %g  %s −%gpx"
              % (r["file"], r["width"], r["sel"][:42], r["eff"][0], r["eff"][1],
                 r["verdict"], r["deficit"]))
    if findings and a.strict:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:               # harness failure: loud, named, never a green
        print("✖ %s" % e, file=sys.stderr)
        sys.exit(2)
