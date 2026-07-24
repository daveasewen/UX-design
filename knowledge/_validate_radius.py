#!/usr/bin/env python3
"""
_validate_radius.py — radius gate (build-out Phase 0, 2026-07-21).

Shape / border-radius is a THEME FLEX SLOT (ADR-0010; Dave 2026-07-21: divergence
axes — UI greys, shape/border-radius, future input error-condition — are
theme-overridable, NEVER hardcoded; Console = rounded NOW). A hardcoded
`border-radius:0` freezes a component square in every theme, which is exactly the
defect this session de-hardcoded out of canon.css (37 declarations).

RULE — every `border-radius` declaration (comments stripped) must be one of:
  * var(...)      the token route: var(--border-radius-default)
  * 50%           a genuine circle (avatar, radio, spinner, dot)
  * 999px         the pill idiom (badge, switch, tab-bar segment — deliberately
                  fully-round in every theme; distinct from the theme flex slot)
  * inherit
Anything else — `0`, bare px/em, multi-value corner shorthand — is a hardcode.

SCOPE (gate only as wide as its glob — the standing scope rule):
  STRICT (blocking):  canon/canon.css · canon/type.css · MIGRATED snippets
  ADVISORY (census):  the other reference snippets + _proforma tranches — they
                      migrate per-component during Phase 1/2; workers move a file
                      into MIGRATED_SNIPPETS in the same change that rebinds it.

Writes knowledge/_RADIUS-GATE.md. Exits non-zero on any STRICT failure.
Selftest: python3 knowledge/_validate_radius.py --selftest (bite test, ADR-0005 §5).
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "_RADIUS-GATE.md")

STRICT_FILES = [
    os.path.join(HERE, "canon", "canon.css"),
    os.path.join(HERE, "canon", "type.css"),
]

# Phase-1 migration ratchet: rebinding a snippet's radius onto the token
# (CSS + manifest + theme-block declarations) and adding it here is ONE change.
MIGRATED_SNIPPETS = {
    "Button.reference.html",
    "Cards.reference.html",
    "Tabs.reference.html",
    "Modals.reference.html",
    "Account-card.reference.html",
    "Table.reference.html",
    "List-items.reference.html",
    "Action-bar.reference.html",
    "Confirmation.reference.html",
    "Links.reference.html",
    "Video-player.reference.html",
    "Notifications.reference.html",
    "Input-fields.reference.html",
    "Selection-controls.reference.html",
    "Dropdown.reference.html",
    "Slider.reference.html",
    "Icon-button.reference.html",
    "Badge.reference.html",
    "Tags.reference.html",
    "Status-indicator.reference.html",
    "Progress-tracker.reference.html",
    # Phase-2 wave 1 (2026-07-22) — born on role tokens, strict from birth:
    "Form-layout.reference.html",
    "Amount-input.reference.html",
    "Textarea.reference.html",
    "Secure-entry.reference.html",
    "Alert.reference.html",
    "Toast.reference.html",
    "Banner.reference.html",
    "Skeleton-loader.reference.html",
    "Drawer.reference.html",
    "Popover.reference.html",
    "Modal-lightbox.reference.html",
    "Empty-state.reference.html",
    "Stat-card.reference.html",
    "Account-selector.reference.html",
    # Phase-2 wave 2:
    "Data-grid.reference.html",
    "Date-picker.reference.html",
    "Date-range-picker.reference.html",
    # Segmented control (2026-07-24) — atom promoted from View options; square radius, pill = 999 literal:
    "Segmented-control.reference.html",
    "Time-picker.reference.html",
    "File-upload.reference.html",
    "Stepper.reference.html",
    "Chart-bar.reference.html",
    "Chart-line.reference.html",
    "Chart-donut.reference.html",
    "Chart-sparkline.reference.html",
    "Chart-scatter.reference.html",
}

ADVISORY_GLOBS = [
    os.path.join(HERE, "snippets", "*.reference.html"),
    os.path.join(HERE, "_proforma", "*.html"),
]

DECL_RE  = re.compile(r'border-radius\s*:\s*([^;}]+)')
OK_VALUE = re.compile(r'^(var\(.*\)|50%|999px|inherit)$')

def strip_comments(text):
    # ds-008 (fixed 2026-07-22, ADR-0013 session): HTML comments stripped TOO — snippet
    # header prose like "border-radius:0" tripped the census (Badge + Tags each carried
    # one; ~50 Phase-2 files will carry header prose). CSS comments were always stripped.
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    return re.sub(r'/\*.*?\*/', '', text, flags=re.S)

def check_text(text):
    """-> list of offending border-radius values (comments already stripped)."""
    return [v.strip() for v in DECL_RE.findall(strip_comments(text))
            if not OK_VALUE.match(v.strip())]

def selftest():
    fails = []
    if check_text(".x{border-radius:var(--border-radius-default);}"):
        fails.append("token route flagged (must pass)")
    if check_text(".x{border-radius:50%;} .y{border-radius:999px;}"):
        fails.append("circle/pill idiom flagged (must pass)")
    if not check_text(".x{border-radius:0;}"):
        fails.append("hardcoded 0 NOT flagged (gate has no teeth)")
    if not check_text(".x{border-radius:4px;}"):
        fails.append("hardcoded px NOT flagged")
    if not check_text(".x{border-radius:0 0 4px 4px;}"):
        fails.append("corner shorthand NOT flagged")
    if check_text("/* border-radius:0 in prose */ .x{border-radius:inherit;}"):
        fails.append("comment mention flagged (comments must be stripped)")
    if check_text("<!-- header prose: SQUARE corners, border-radius:0 by brand -->\n.x{border-radius:var(--border-radius-control);}"):
        fails.append("HTML-comment prose flagged (ds-008 — HTML comments must be stripped)")
    return fails

def main():
    if "--selftest" in sys.argv:
        f = selftest()
        if f:
            print("_validate_radius SELFTEST FAIL:"); [print("  X " + x) for x in f]
            sys.exit(1)
        print("_validate_radius selftest OK")
        return

    strict_fails, advisory = [], []
    for p in STRICT_FILES:
        if not os.path.exists(p):
            continue
        for v in check_text(open(p).read()):
            strict_fails.append((os.path.relpath(p, HERE), v))
    snip_dir = os.path.join(HERE, "snippets")
    for pattern in ADVISORY_GLOBS:
        for p in sorted(glob.glob(pattern)):
            name = os.path.basename(p)
            bad = check_text(open(p).read())
            if not bad:
                continue
            if os.path.dirname(p) == snip_dir and name in MIGRATED_SNIPPETS:
                strict_fails += [(f"snippets/{name}", v) for v in bad]
            else:
                advisory.append((os.path.relpath(p, HERE), len(bad)))

    lines = ["# _RADIUS-GATE — border-radius is token-bound (theme flex slot, ADR-0010)",
             "",
             "*Generated by `_validate_radius.py`. Allowed values: `var(...)`, `50%` (circle),",
             "`999px` (pill idiom), `inherit`. STRICT = canon + migrated snippets (blocking).*",
             ""]
    if strict_fails:
        lines.append(f"## ❌ STRICT failures ({len(strict_fails)})\n")
        lines += [f"- `{f}` → `border-radius:{v}`" for f, v in strict_fails]
    else:
        lines.append("## ✅ STRICT surfaces clean (canon + " +
                     f"{len(MIGRATED_SNIPPETS)} migrated snippet(s))")
    lines.append("")
    if advisory:
        lines.append(f"## ⚠ ADVISORY — awaiting Phase-1/2 migration ({len(advisory)} file(s))\n")
        lines += [f"- `{f}` — {n} hardcoded declaration(s)" for f, n in advisory]
        lines.append("\n*Migrating a file = rebind its radius onto the token (CSS + manifest + "
                     "theme blocks) AND add it to `MIGRATED_SNIPPETS` in `_validate_radius.py` "
                     "in the same change.*")
    else:
        lines.append("## ✅ no advisory hardcodes remain")
    open(OUT, "w").write("\n".join(lines) + "\n")

    print(f"_validate_radius: {len(strict_fails)} strict fail(s), "
          f"{len(advisory)} advisory file(s) pending migration -> _RADIUS-GATE.md")
    if strict_fails:
        [print(f"  X {f}: border-radius:{v}") for f, v in strict_fails]
        sys.exit(1)

if __name__ == "__main__":
    main()
