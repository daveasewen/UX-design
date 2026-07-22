#!/usr/bin/env python3
"""State-snap gate (ADR-0014) — opacity-for-states is allowed IFF the composite is
engineered to land on a step of the ACTIVE THEME'S neutral primitive ramp.

Dave's test, ruled 2026-07-22 (theming clean-room; refines ADR-0009 §2-3):
  - A state token whose $extensions.apollo.state mechanism includes "opacity" must
    store, per mode, an EXACT step of the snap ramp (the stored colour equivalent —
    the portable form colour-only consumers resolve).
  - The operational flatten  alpha*fades + (1-alpha)*over  must sit within
    LUMA_TOL of that stored step ("engineered to snap", not coincidence). Calibrated
    on the two ruled consumers: button-sheet v7 hover (mono/7 / mono/10-class) and
    R-D23 tabs/inactive (mono/7 light / mono/10 dark) — both pass at TOL=8/255.
  - The check runs PER THEME whose registry stateMechanism.default is an opacity
    operator, against THAT theme's neutralRamp (snapPass is theme-parameterised:
    a warm theme must snap to warm steps). Themes with default "colour"/"explicit"
    resolve the stored colour instead — no snap duty (Supercharge, Legacy/R-D24).

TEXT-STATE AA (added same day, Dave: "the inactive tabs still have to pass Ally,
they're inactive not disabled remember"): when the fading token IS text (`fades`
starts with text/), the STORED colour must also pass 4.5:1 against its `over`
ground, resolved per theme under EVERY theme — inactive is an interactive state,
not disabled; no contrast exemption. Themes exempt as-built (Legacy, R-D24) are
skipped with an EXEMPTED note. First catch: SC dark tabs/inactive at warm/10 =
3.89:1 (the DNA index landing on a darker warm page) → warm/11 = 7.01:1.
Other snap AA remains with the contrast audits (ADR-0009 §4 unchanged); this
gate owns snap mechanics + the text-state floor. Fail = build failure (blocking).

Usage:
  python3 knowledge/_validate_state_snap.py             # gate
  python3 knowledge/_validate_state_snap.py --selftest  # fixture bite-test
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "canon"))
from gen_theme_cascade import load_themes, base_value  # noqa: E402  (single source for effective values)

TOK = os.path.join(HERE, "tokens")
LUMA_TOL = 8.0          # /255 — see calibration note above
OPACITY_DEFAULTS = ("opacity",)   # registry stateMechanism.default values that carry snap duty


# ---------------------------------------------------------------- colour maths
def _rgb(hx):
    hx = hx.strip().lstrip("#")
    return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))

def _luma(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def _flatten(alpha, fade_rgb, over_rgb):
    return tuple(alpha * f + (1 - alpha) * o for f, o in zip(fade_rgb, over_rgb))

def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def _rel_lum(rgb):
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def contrast(hex_a, hex_b):
    la, lb = _rel_lum(_rgb(hex_a)), _rel_lum(_rgb(hex_b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def check_text_state_aa(path, stored, over, theme_key):
    """Interactive-not-disabled floor: a text-state's stored colour vs its ground
    must pass WCAG AA 4.5:1 per mode. Returns failure strings."""
    fails = []
    for mode in ("light", "dark"):
        c = contrast(stored[mode], over[mode])
        if c < 4.5:
            fails.append(f"[{theme_key}] {path} ({mode}): text-state {stored[mode]} on "
                         f"{over[mode]} = {c:.2f}:1 < 4.5 — inactive is INTERACTIVE, not "
                         f"disabled (no exemption); pick a passing ramp step")
    return fails


# ---------------------------------------------------------------- pure checker
def check_token(path, stored, alpha, fades, over, ramp, ramp_name, theme_key):
    """All args are plain values: stored/fades/over = {'light': '#..', 'dark': '#..'},
    ramp = ordered list of step hexes. Returns a list of failure strings."""
    fails = []
    steps = {h.upper() for h in ramp}
    for mode in ("light", "dark"):
        s = stored[mode].upper()
        if s not in steps:
            fails.append(f"[{theme_key}] {path} ({mode}): stored {s} is NOT a step of {ramp_name} "
                         f"— the colour equivalent must be an exact ramp step (ADR-0014)")
            continue
        flat = _flatten(alpha, _rgb(fades[mode]), _rgb(over[mode]))
        drift = abs(_luma(flat) - _luma(_rgb(s)))
        if drift > LUMA_TOL:
            fails.append(f"[{theme_key}] {path} ({mode}): flatten of α={alpha} "
                         f"{fades[mode]} over {over[mode]} sits {drift:.1f}/255 luma from stored {s} "
                         f"(tol {LUMA_TOL}) — not engineered to snap; use colour mechanism or re-derive α")
    return fails


# ---------------------------------------------------------------- repo assembly
def _ramp_hexes(ramp_field):
    """'color/mono/1-15' -> ordered step hexes from the primitive store."""
    m = re.fullmatch(r"(.+)/(\d+)-(\d+)", ramp_field)
    if not m:
        raise SystemExit(f"state-snap: unparseable neutralRamp '{ramp_field}'")
    prefix, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
    return [str(base_value(f"{prefix}/{i}", "light")) for i in range(lo, hi + 1)]

def _opacity_tokens(store):
    out = []
    def walk(node, path=""):
        if not isinstance(node, dict):
            return
        st = node.get("$extensions", {}).get("apollo", {}).get("state", {})
        if "opacity" in st.get("mechanism", []):
            out.append((path, node, st))
        for k, v in node.items():
            if not k.startswith("$"):
                walk(v, f"{path}/{k}" if path else k)
    walk(store)
    return out

def _mode_pair(path, theme_ov):
    """Effective per-mode values for a token path under a theme (override wins, else base)."""
    ov = theme_ov.get(path)
    if ov:
        if "modeless" in ov:
            return {"light": ov["modeless"], "dark": ov["modeless"]}
        return {"light": ov["light"], "dark": ov["dark"]}
    return {"light": str(base_value(path, "light")), "dark": str(base_value(path, "dark"))}

def run_gate():
    reg = json.load(open(os.path.join(TOK, "themes", "_themes.json")))
    sem = json.load(open(os.path.join(TOK, "semantic-colour.json")))
    themes = {t["key"]: t for t in load_themes()}
    fails, checked = [], 0
    # --- text-state AA floor: EVERY theme (stored colour is what renders somewhere);
    #     Legacy = as-built, R-D24 exempt (skipped, documented by the ruling).
    for key, meta in reg["themes"].items():
        if (meta.get("stateMechanism") or {}).get("default") == "explicit":
            continue        # R-D24 as-built posture — exempt, never counted a pass
        ov = themes[key]["overrides"] if key in themes else {}
        for path, node, st in _opacity_tokens(sem):
            fades_path = st.get("fades", "")
            if not fades_path.startswith("text/"):
                continue
            stored = _mode_pair(path, ov)
            over = _mode_pair(st.get("over", "background/default"), ov)
            fails += check_text_state_aa(path, stored, over, key)
            checked += 1
    for key, meta in reg["themes"].items():
        mech = (meta.get("stateMechanism") or {}).get("default")
        if mech not in OPACITY_DEFAULTS:
            continue        # colour/explicit themes resolve stored colour; no snap duty
        ramp_field = meta.get("neutralRamp")
        if not ramp_field:
            fails.append(f"[{key}] stateMechanism=opacity but no neutralRamp declared — nothing to snap to")
            continue
        ramp = _ramp_hexes(ramp_field)
        ov = themes[key]["overrides"] if key in themes else {}
        for path, node, st in _opacity_tokens(sem):
            alpha = st.get("opacity")
            fades_path = st.get("fades") or re.sub(r"/[a-z-]+$", "/default", path)
            over_path = st.get("over", "background/default")
            if alpha is None:
                fails.append(f"[{key}] {path}: opacity mechanism without an opacity value")
                continue
            stored = _mode_pair(path, ov)
            fades = _mode_pair(fades_path, ov)
            over = _mode_pair(over_path, ov)
            fails += check_token(path, stored, alpha, fades, over, ramp, ramp_field, key)
            checked += 1
    return fails, checked

# ---------------------------------------------------------------- selftest
def selftest():
    ramp = ["#000000", "#1A1A1A", "#626262", "#B7B7B7", "#FFFFFF"]
    ok = check_token("t/x", {"light": "#626262", "dark": "#B7B7B7"}, 0.7,
                     {"light": "#1A1A1A", "dark": "#FFFFFF"},
                     {"light": "#FFFFFF", "dark": "#1A1A1A"}, ramp, "fix/1-5", "fix")
    fails = []
    if ok:
        fails.append("calibration fixture should PASS, got: " + "; ".join(ok))
    # bite 1: stored value off-ramp
    r = check_token("t/x", {"light": "#5F5F5F", "dark": "#B7B7B7"}, 0.7,
                    {"light": "#1A1A1A", "dark": "#FFFFFF"},
                    {"light": "#FFFFFF", "dark": "#1A1A1A"}, ramp, "fix/1-5", "fix")
    if not any("NOT a step" in f for f in r):
        fails.append("off-ramp stored value must bite")
    # bite 2: alpha not engineered (flatten far from claimed step)
    r = check_token("t/x", {"light": "#626262", "dark": "#B7B7B7"}, 0.35,
                    {"light": "#1A1A1A", "dark": "#FFFFFF"},
                    {"light": "#FFFFFF", "dark": "#1A1A1A"}, ramp, "fix/1-5", "fix")
    if not any("not engineered to snap" in f for f in r):
        fails.append("flatten drift must bite")
    # bite 3: theme-parameterised — a mono-snapped value against a WARM ramp fails membership
    warm = ["#000000", "#13110E", "#25211C", "#806E65", "#F7F6F4"]
    r = check_token("t/x", {"light": "#626262", "dark": "#B7B7B7"}, 0.7,
                    {"light": "#13110E", "dark": "#F7F6F4"},
                    {"light": "#F7F6F4", "dark": "#13110E"}, warm, "warm/1-5", "sc-fix")
    if len([f for f in r if "NOT a step" in f]) != 2:
        fails.append("warm-ramp membership must bite on both modes")
    # bite 4: text-state AA — the exact SC-dark catch (Dave 2026-07-22: inactive ≠ disabled).
    r = check_text_state_aa("t/tabs-like", {"light": "#493F39", "dark": "#806E65"},
                            {"light": "#F7F6F4", "dark": "#13110E"}, "sc-fix")
    if not any("INTERACTIVE, not" in f and "(dark)" in f for f in r) or any("(light)" in f for f in r):
        fails.append("text-state AA must bite on the 3.89:1 dark pair and pass the light pair")
    return fails

def main():
    if "--selftest" in sys.argv:
        fails = selftest()
        if fails:
            print("state-snap SELFTEST FAIL:")
            [print("  X " + f) for f in fails]
            sys.exit(1)
        print("state-snap selftest OK")
        return
    fails, checked = run_gate()
    if fails:
        print(f"state-snap gate: {len(fails)} failure(s) across {checked} check(s):")
        [print("  ❌ " + f) for f in fails]
        sys.exit(1)
    print(f"state-snap gate: OK — {checked} opacity-state check(s) snapped to their theme ramps.")

if __name__ == "__main__":
    main()
