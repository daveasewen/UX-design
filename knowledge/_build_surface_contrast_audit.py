#!/usr/bin/env python3
"""Text/icon token dark-mode contrast audit (fix #1b — resolved-surface + gating).

For every text/icon/label token, compute its dark-mode contrast against the
REAL worst-case dark surface it sits on (resolved from the token store), not a
single hardcoded surface. Mode-specific tokens (e.g. */on-light) are excluded
rather than false-flagged. Tokens in CONTRAST_ALLOWLIST (disabled states) are
reported but do not fail the build.

GATES the build: exits non-zero if any non-allowlisted token is below threshold.
Text needs 4.5:1 (WCAG 1.4.3 AA); icons/UI need 3:1 (1.4.11).
Writes knowledge/_TEXT-CONTRAST-AUDIT.json + .md

PER-THEME PALETTE RESOLUTION (s169, ruling C' — red 30). Until #169 this reader
did a SINGLE json.load of tokens/semantic-colour.json and never opened
tokens/themes/_themes.json or the s157-D2 palette tier, so it graded MONO's
rag/*-background value for all four themes. It now resolves palette-owned rag
surfaces PER THEME (themes/_themes.json -> ragPalette -> palettes/rag/*.json,
the s158-D4 single source) and regrades every pair whose surface MOVES under a
theme. The base pass is unchanged and is the activeBase (apollo-mono) reading.
Theme rows are reported by NAME and GATE on the same terms as the base pass.
No token file is read for a value the palette tier owns; nothing is written back.

PER-THEME TOKEN OVERRIDES (s170, ruling C' — the second leg). Resolving grounds
alone still graded MONO's INK under every theme: a theme that re-binds a token in
its own override set (themes/_themes.json -> overrideSet) was invisible to this
reader, so e.g. Legacy's ruled white rag/text/on-information (s131-D1) was graded
as the base ink. Overrides are now applied GENERICALLY — any override path that
names an audited text/icon token supplies that theme's ink, and any override path
that names a surface the base map knows re-values that ground (the palette tier
still wins on the keys it owns, per s158-D4). A declared overrideSet that cannot
be read is a NAMED refusal (OverrideRefusal), never a silent fall-back to base.

WARN (MINOR-DEFECT) TIER (s194-D1, Dave #194). A pair a ruling ABOLISHES is not
deleted from the report and is not a gating error either. It is MEASURED, printed
with its real ratio, stamped `⚠ minor (ruled <id>)`, and does NOT affect the exit
code. Dave: "this should be a warning not an error. if it was a proper ally review
it would be a minor defect". The severity vocabulary is pass / minor / gating and
is applied CONSERVATIVELY — `minor` is reachable only through the named pairs in
_contrast_utils.MINOR_PAIRS (theme-scoped), so every other row keeps the verdict it
had before. A general graded-defect rating is FLOATED (_DS-IMPROVEMENTS.md), not
ruled, and is deliberately NOT built here.

Usage:
  python3 knowledge/_build_surface_contrast_audit.py            # audit + write + gate
  python3 knowledge/_build_surface_contrast_audit.py --selftest  # reader selftest, no writes
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, sys
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(__file__))
from _contrast_utils import (
    contrast_ratio, is_sufficient_contrast,
    load_dark_surfaces, resolve_dark_surface, standard_dark_surfaces,
    legacy_exemption, _leaf_dark_hex, _group_prefix, _excluded_surfaces,
    luminance, hex_to_rgb,
    minor_pair, ground_names_for,
    CONTRAST_ALLOWLIST,
)

# --- s194-D1 (Dave, #194): the severity vocabulary this report speaks. --------
# Three verdicts, applied CONSERVATIVELY. "minor" is reachable ONLY through
# _contrast_utils.MINOR_PAIRS, i.e. only for a pair a ruling names; nothing else
# changes verdict. Dave #194: "this should be a warning not an error. if it was
# a proper ally review it would be a minor defect."
#   pass   -> OK / ALLOWED / EXEMPTED  (exit code unaffected)
#   minor  -> MINOR                    (measured, reported, stamped, NON-GATING)
#   gating -> POOR_CONTRAST            (fails the build, exactly as before)
# This is NOT a general grading system; the graded-rating idea is FLOATED in
# _DS-IMPROVEMENTS.md, promotion Dave's alone.
SEVERITY = {
    "OK": "pass", "ALLOWED": "pass", "EXEMPTED": "pass",
    "MINOR": "minor", "POOR_CONTRAST": "gating",
}

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")


def _active_base(tok_dir=None):
    """The registry's activeBase theme key — the theme the BASE pass reads.

    s194: the base pass is not theme-less, it IS apollo-mono. Naming it lets a
    theme-scoped ruled-pair exclusion apply to the base pass without a hardcoded
    theme name anywhere. Read from the registry, never assumed; a missing/broken
    registry falls back to the documented activeBase so the reader still runs
    (the per-theme legs raise their own NAMED refusals for that case).
    """
    try:
        reg = json.load(open(os.path.join(tok_dir or TOK, "themes", "_themes.json")))
        return reg.get("activeBase") or "apollo-mono"
    except Exception:
        return "apollo-mono"


ACTIVE_BASE = _active_base()


def leaves(node, path="", out=None):
    if out is None:
        out = {}
    if isinstance(node, dict):
        if any(k in node for k in ("$value", "light", "dark")):
            out[path] = node
            return out
        for k, v in node.items():
            if k.startswith("$"):
                continue
            leaves(v, (path + "/" + k).strip("/") if path else k, out)
    return out


def mode_val(n, m):
    x = n.get(m)
    return (x.get("$value") or x.get("value")) if isinstance(x, dict) else x


def is_text_or_icon_token(name):
    return any(x in name for x in ["text/", "icon/", "label"])


# --- s169 ruling C': per-theme resolution of palette-owned surfaces -----------
# The palette tier (s157-D2, single-sourced by s158-D4) owns the twelve core rag
# hue keys. A theme DECLARES which palette it consumes via ragPalette in
# tokens/themes/_themes.json. This reader mirrors that declaration: it never
# guesses a path and never falls back to the base value silently — a declared
# palette that is missing is a NAMED refusal, not a crash and not a pass.

class PaletteRefusal(Exception):
    """A theme's declared palette could not be read. Named, never swallowed."""


class OverrideRefusal(Exception):
    """A theme's declared overrideSet could not be read. Named, never swallowed.

    Distinct from PaletteRefusal on purpose: the two tiers fail for different
    reasons and a caller must be able to say WHICH one refused.
    """


def load_theme_overrides(tok_dir, key, rel):
    """Read one theme's override set -> {token path: token node}.

    `rel` is the registry's overrideSet path, relative to knowledge/tokens/.
    A None/absent declaration means the theme HAS no override set (apollo-mono,
    the activeBase) and yields {}. A DECLARED set that is missing, unreadable or
    malformed raises OverrideRefusal — it is never treated as 'no overrides',
    because that is indistinguishable from the base reading and would repeat the
    very defect the per-theme legs exist to fix.
    """
    if not rel:
        return {}
    path = os.path.join(tok_dir, rel)
    if not os.path.exists(path):
        raise OverrideRefusal(
            "theme %s declares overrideSet %r in tokens/themes/_themes.json "
            "but no file exists at %s" % (key, rel, path))
    try:
        doc = json.load(open(path))
    except ValueError as e:
        raise OverrideRefusal("theme %s: overrideSet %s is not valid JSON (%s)" % (key, rel, e))
    ov = doc.get("overrides")
    if not isinstance(ov, dict):
        raise OverrideRefusal(
            "theme %s: overrideSet %s has no 'overrides' object (got %s)"
            % (key, rel, type(ov).__name__))
    return {k: v for k, v in ov.items() if isinstance(v, dict)}


def load_theme_palettes(tok_dir):
    """theme key -> {label, attr, palette, surfaces{token-name: dark hex}}.

    Palette keys are BARE ('error-background'); the semantic token name they own
    is 'rag/<key>'. Only opaque dark hexes are kept (same rule as the base
    surface loader) — -ink/-graphic rungs are not surfaces and drop out when the
    caller intersects with the base surface map.
    """
    reg_path = os.path.join(tok_dir, "themes", "_themes.json")
    if not os.path.exists(reg_path):
        raise PaletteRefusal("theme registry not found: %s" % reg_path)
    reg = json.load(open(reg_path))
    out = OrderedDict()
    themes = reg.get("themes") or {}
    for key, t in sorted(themes.items(), key=lambda kv: kv[1].get("order", 99)):
        rel = t.get("ragPalette")
        if not rel:
            continue
        path = os.path.join(tok_dir, rel)
        if not os.path.exists(path):
            raise PaletteRefusal(
                "theme %s declares ragPalette %r in tokens/themes/_themes.json "
                "but no file exists at %s" % (key, rel, path))
        try:
            pal = json.load(open(path))
        except ValueError as e:
            raise PaletteRefusal("theme %s: ragPalette %s is not valid JSON (%s)" % (key, rel, e))
        vals = {}
        for k, node in (pal.get("keys") or {}).items():
            hx = _leaf_dark_hex(node)
            if hx:
                vals["rag/" + k] = hx
        ovrel = t.get("overrideSet")
        out[key] = {"label": t.get("label", key), "attr": t.get("attr", key),
                    "palette": rel, "surfaces": vals,
                    "override_set": ovrel,
                    "overrides": load_theme_overrides(tok_dir, key, ovrel)}
    if not out:
        raise PaletteRefusal("no theme in %s declares a ragPalette" % reg_path)
    return out


def theme_surface_map(base_surfaces, pal_surfaces, overrides=None):
    """Base surface map with the theme's own values substituted in.

    Two tiers, applied in declaration order: the theme's override set FIRST, then
    the palette tier, which WINS on the keys it owns (s158-D4 single source — a
    palette-owned ground must not be shadowed by a stale override entry). Only
    names the base map already knows are substituted: neither tier mints a
    surface, both re-value the ones the semantic tier declares.
    """
    s = dict(base_surfaces)
    for name, node in (overrides or {}).items():
        if name in base_surfaces:
            hx = _leaf_dark_hex(node)
            if hx:
                s[name] = hx
    for name, hx in pal_surfaces.items():
        if name in base_surfaces:
            s[name] = hx
    return s


# --- s170 (Dave, #170): STATE-MATCHED GROUNDS -------------------------------
# _contrast_utils.resolve_dark_surface grades a grouped ink against the LIGHTEST
# ground in its group, across every state. For a state-suffixed ink that is an
# INSTRUMENT ARTEFACT, not a real pairing: it imagined Legacy's white
# button/primary/label/default sitting on button/primary/background/PRESSED
# (#FFFFFF) and reported 1.0:1 — a component state that cannot co-occur. Dave
# ruled a label state may only be compared against its OWN matching background
# state. Where the group offers no same-state ground (the common case: ungrouped
# text/*, or a label whose state has no background twin) behaviour is UNCHANGED
# and falls through to the shared worst-case resolver, so no false negative is
# introduced anywhere the artefact did not exist.
STATE_SUFFIXES = ("default", "hover", "pressed", "active", "focus", "focused",
                  "selected", "visited", "disabled")


def _state_suffix(token_name):
    """'button/primary/label/default' -> 'default'; 'text/secondary' -> None."""
    last = token_name.rsplit("/", 1)[-1]
    return last if last in STATE_SUFFIXES else None


def resolve_ground(token_name, surfaces, default_dark, raised_dark, theme=None):
    """Return (surface_hex, label) with s170 state matching applied.

    s194: `theme` is the tokens/themes/_themes.json key the pair is being graded
    under (the base pass passes ACTIVE_BASE, i.e. apollo-mono). It is used ONLY
    to select theme-scoped ruled-pair exclusions; every other decision is
    theme-blind exactly as before.

    Delegates to resolve_dark_surface for every skip decision (light-only,
    on-inverse, the named per-token carve-outs) and for the fall-back, so this
    wrapper can only ever NARROW the candidate set — never widen it, never
    change which tokens are audited.
    """
    base = resolve_dark_surface(token_name, surfaces, default_dark, raised_dark, theme)
    if base[0] is None:
        return base
    state = _state_suffix(token_name)
    if not state:
        return base
    grp = _group_prefix(token_name)
    if not grp:
        return base
    excluded = _excluded_surfaces(token_name, theme)
    matched = [hx for nm, hx in surfaces.items()
               if nm.startswith(grp + "/") and nm not in excluded
               and _state_suffix(nm) == state]
    if not matched:
        return base
    # A group may still expose more than one same-state ground; worst-case
    # (lightest) WITHIN the matched state stays the conservative choice.
    worst = max(matched, key=lambda h: luminance(*hex_to_rgb(h)))
    return (worst, grp)


def grade(name, node, surfaces, default_dark, raised_dark, theme=None):
    """Grade one token against a given surface map. Returns a record or None."""
    dark_val = mode_val(node, "dark")
    if not (isinstance(dark_val, str) and dark_val.startswith("#")):
        return None
    surface, label = resolve_ground(name, surfaces, default_dark, raised_dark, theme)
    if surface is None:
        return None
    context = "text" if "text" in name else "ui"
    ratio = contrast_ratio(dark_val, surface)
    passes = is_sufficient_contrast(ratio, context=context)
    allowlisted = name in CONTRAST_ALLOWLIST
    return {"token": name, "dark_value": dark_val, "surface": surface,
            "surface_label": label, "contrast_ratio": ratio,
            "threshold": 4.5 if context == "text" else 3.0, "context": context,
            "passes": passes, "allowlisted": allowlisted}


def audit_themes(sem_leaves, base_surfaces, tok_dir, default_dark, raised_dark):
    """Regrade every token whose GROUND or INK moves under a theme.

    Rows are emitted only where the theme's resolved surface OR the theme's
    resolved ink differs from the base pass, so the activeBase reading is never
    double-counted (apollo-mono declares no override set and consumes the base
    palette, so it emits no rows at all). Legacy pairs
    are routed through _contrast_utils.legacy_exemption() per R-D24's own
    instruction; a hit is recorded as EXEMPTED (documented), never as a pass.
    A miss is a real failure and gates like any other.
    """
    palettes = load_theme_palettes(tok_dir)
    rows = []
    for tkey, meta in palettes.items():
        ovr = meta["overrides"]
        smap = theme_surface_map(base_surfaces, meta["surfaces"], ovr)
        for name, node in sorted(sem_leaves.items()):
            if not is_text_or_icon_token(name):
                continue
            if "light" not in node or "dark" not in node:
                continue
            th_node = ovr.get(name, node)
            # The base pass IS the activeBase theme's reading (apollo-mono), so it
            # is graded under ACTIVE_BASE; the theme leg under its own key. s194:
            # this is what keeps a mono-scoped exclusion out of Legacy/Console/SC.
            base_rec = grade(name, node, base_surfaces, default_dark, raised_dark, ACTIVE_BASE)
            th_rec = grade(name, th_node, smap, default_dark, raised_dark, tkey)
            if base_rec is None or th_rec is None:
                continue
            if (th_rec["surface"] == base_rec["surface"]
                    and th_rec["dark_value"] == base_rec["dark_value"]):
                continue  # theme moves neither ground nor ink; base pass covers it
            # Name the ground: prefer a surface the theme MOVED, else the base
            # name carrying that hex (an ink-only row still sits on a real ground).
            # s170: name the STATE-MATCHED ground first where one exists. The
            # hex-match search below is order-dependent and could otherwise
            # label the ground with an unrelated token that happens to carry
            # the same hex (observed: legacy's button/primary/background/default
            # #DB0011 reported as `badge/background`). The ratio was always
            # right; only the NAME was wrong, and a wrong name sends the reader
            # to the wrong token.
            state = _state_suffix(name)
            grp0 = _group_prefix(name)
            owner = None
            if state and grp0:
                owner = next((n for n, hx in sorted(smap.items())
                              if hx == th_rec["surface"] and n.startswith(grp0 + "/")
                              and _state_suffix(n) == state), None)
            if owner is None:
                owner = next((n for n, hx in smap.items()
                              if hx == th_rec["surface"] and n in base_surfaces
                              and base_surfaces[n] != hx), None)
            if owner is None:
                grp = _group_prefix(name)
                owner = next((n for n, hx in smap.items()
                              if hx == th_rec["surface"] and n in base_surfaces
                              and grp and n.startswith(grp + "/")), None)
            exempt = legacy_exemption(name, owner or "") if meta["attr"] == "legacy" else None
            # s194-D1 WARN tier, theme-scoped: only a pair the ruling names under
            # THIS theme is downgraded to MINOR. Legacy/Console/Supercharge are
            # not named, so their white-on-error rows stay measured and gating.
            minor = None if th_rec["passes"] else minor_pair(
                name, ground_names_for(name, th_rec["surface"], smap), tkey)
            if th_rec["passes"]:
                status = "OK"
            elif minor:
                status = "MINOR"
            elif exempt:
                status = "EXEMPTED"
            elif th_rec["allowlisted"]:
                status = "ALLOWED"
            else:
                status = "POOR_CONTRAST"
            th_rec.update({"severity": SEVERITY[status],
                           "ruling": (minor or {}).get("ruling"),
                           "minor_reason": (minor or {}).get("reason"),
                           "theme": tkey, "theme_label": meta["label"],
                           "palette": meta["palette"], "surface_token": owner,
                           "override_set": meta["override_set"],
                           "ink_source": "theme-override" if name in ovr else "base",
                           "base_dark_value": base_rec["dark_value"],
                           "moved": ("ink+ground" if (th_rec["dark_value"] != base_rec["dark_value"]
                                                      and th_rec["surface"] != base_rec["surface"])
                                     else ("ink" if th_rec["dark_value"] != base_rec["dark_value"]
                                           else "ground")),
                           "base_surface": base_rec["surface"],
                           "base_contrast_ratio": base_rec["contrast_ratio"],
                           "status": status, "exemption_reason": exempt,
                           "allowlist_reason": CONTRAST_ALLOWLIST.get(name) if (th_rec["allowlisted"] and not th_rec["passes"]) else None})
            th_rec.pop("passes"); th_rec.pop("allowlisted")
            rows.append(th_rec)
    return palettes, rows


def audit_base(sem_leaves, surfaces, default_dark, raised_dark):
    """The BASE pass (= the activeBase theme's reading). Returns (audit, poor, skipped).

    Factored out at s194 so the selftest DRIVES this reader rather than a copy of
    it: the arms below assert on the very records the report is built from, so a
    change to the verdict logic here cannot pass unnoticed. `poor` is the gating
    list — s194-D1 MINOR rows are deliberately NOT in it.
    """
    audit, poor, skipped = [], [], []
    for name, node in sorted(sem_leaves.items()):
        if not is_text_or_icon_token(name):
            continue
        if "light" not in node or "dark" not in node:
            continue
        dark_val = mode_val(node, "dark")
        if not (isinstance(dark_val, str) and dark_val.startswith("#")):
            continue

        surface, label = resolve_ground(name, surfaces, default_dark, raised_dark, ACTIVE_BASE)
        if surface is None:
            skipped.append({"token": name, "dark_value": dark_val, "reason": label})
            continue

        context = "text" if "text" in name else "ui"
        threshold = 4.5 if context == "text" else 3.0
        ratio = contrast_ratio(dark_val, surface)
        passes = is_sufficient_contrast(ratio, context=context)
        allowlisted = name in CONTRAST_ALLOWLIST
        # s194-D1: a ruled-abolished pairing is a MINOR defect — still measured,
        # still printed with its real ratio, stamped with the ruling, and NOT
        # gating. The base pass reads the activeBase theme, so it is tested
        # under ACTIVE_BASE.
        gnames = ground_names_for(name, surface, surfaces)
        minor = None if passes else minor_pair(name, gnames, ACTIVE_BASE)

        if passes:
            status = "OK"
        elif minor:
            status = "MINOR"
        elif allowlisted:
            status = "ALLOWED"
        else:
            status = "POOR_CONTRAST"

        rec = {
            "token": name, "dark_value": dark_val,
            "surface": surface, "surface_label": label,
            "surface_token": (minor or {}).get("surface_token") or (gnames[0] if gnames else None),
            "contrast_ratio": ratio, "threshold": threshold, "context": context,
            "status": status, "severity": SEVERITY[status],
            "ruling": (minor or {}).get("ruling"),
            "minor_reason": (minor or {}).get("reason"),
            "allowlist_reason": CONTRAST_ALLOWLIST.get(name) if (status == "ALLOWED") else None,
        }
        audit.append(rec)
        if status == "POOR_CONTRAST":
            poor.append(rec)
    return audit, poor, skipped


def _selftest():
    """Reader selftest: happy path + MUTATION control + NAMED refusal.

    The mutation arm is the one that can FAIL: it copies the token tree to a temp
    dir, changes ONE palette value there, and asserts the audit's verdict moves.
    A green without it would only assert that the code ran.
    """
    import shutil, tempfile, traceback
    arms, fails = [], 0

    def check(arm, cond, detail=""):
        nonlocal fails
        ok = bool(cond)
        if not ok:
            fails += 1
        arms.append((arm, ok, detail))
        print("%s %s%s" % ("✓" if ok else "✗", arm, (" — " + detail) if detail else ""))

    sem_l = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))
    surf = load_dark_surfaces(sem_l)
    dd, rd = standard_dark_surfaces(TOK)

    # --- Arm 1: happy path — the three palettes resolve, per theme.
    pals, rows = audit_themes(sem_l, surf, TOK, dd, rd)
    check("A1a registry: all four themes declare a readable ragPalette",
          len(pals) == 4, "themes=%s" % ",".join(pals))
    got = {r["theme"]: r["surface"] for r in rows if r["token"] == "rag/text/on-dark"}
    check("A1b legacy resolves its OWN error ground",
          got.get("apollo-legacy") == "#A8000B", "got %s" % got.get("apollo-legacy"))
    check("A1c console+supercharge resolve the shared ground",
          got.get("apollo-console") == "#B92F1E" and got.get("apollo-supercharge") == "#B92F1E",
          "console=%s supercharge=%s" % (got.get("apollo-console"), got.get("apollo-supercharge")))
    check("A1d apollo-mono emits NO theme row (== activeBase, no double count)",
          "apollo-mono" not in got, "mono rows=%d" % sum(1 for r in rows if r["theme"] == "apollo-mono"))
    ratios = {(r["theme"], r["token"]): r["contrast_ratio"] for r in rows}
    # s170: the #169 figures below were measured BEFORE the override leg. Legacy's
    # on-information was 2.21:1 only because this reader graded MONO's ink under
    # Legacy; with s131-D1's white applied it is 7.87:1. Console/Supercharge now
    # carry the same ruled white (#170), so their 2.89:1 reading — REAL, and a real
    # failure — is resolved to 6.02:1 on the SAME ground #B92F1E.
    check("A1e measured ratios match first-hand probe",
          ratios.get(("apollo-legacy", "rag/text/on-dark")) == 7.87
          and ratios.get(("apollo-legacy", "rag/text/on-information")) == 7.87
          and ratios.get(("apollo-console", "rag/text/on-dark")) == 6.02
          and ratios.get(("apollo-console", "rag/text/on-information")) == 6.02
          and ratios.get(("apollo-supercharge", "rag/text/on-information")) == 6.02,
          str({k[0] + "/" + k[1].split("/")[-1]: v for k, v in sorted(ratios.items())}))

    tmp = tempfile.mkdtemp(prefix="contrast-selftest-")
    try:
        # --- Arm 2: MUTATION control (temp copy — the real store is never touched).
        m = os.path.join(tmp, "mut")
        shutil.copytree(TOK, m)
        pp = os.path.join(m, "palettes", "rag", "legacy.json")
        pal = json.load(open(pp))
        pal["keys"]["error-background"]["light"]["$value"] = "#FFFFFF"
        pal["keys"]["error-background"]["dark"]["$value"] = "#FFFFFF"
        json.dump(pal, open(pp, "w"), indent=1, ensure_ascii=False)
        _, mrows = audit_themes(sem_l, surf, m, dd, rd)
        mg = {(r["theme"], r["token"]): r for r in mrows}
        moved = mg.get(("apollo-legacy", "rag/text/on-dark"))
        held = mg.get(("apollo-console", "rag/text/on-dark"))
        check("A2a mutation BITES: legacy ground follows the mutated palette file",
              moved is not None and moved["surface"] == "#FFFFFF",
              "surface=%s" % (moved and moved["surface"]))
        check("A2b mutation FLIPS the verdict (was OK 7.87 -> now POOR 1.0)",
              moved is not None and moved["status"] == "POOR_CONTRAST" and moved["contrast_ratio"] == 1.0,
              "%s %s:1" % (moved and moved["status"], moved and moved["contrast_ratio"]))
        check("A2c mutation is SCOPED: console/supercharge unmoved",
              held is not None and held["surface"] == "#B92F1E",
              "surface=%s" % (held and held["surface"]))
        check("A2d real store untouched by the mutation arm",
              json.load(open(os.path.join(TOK, "palettes", "rag", "legacy.json")))
              ["keys"]["error-background"]["dark"]["$value"] == "#A8000B")

        # --- Arm 3: NAMED refusal — declared palette missing.
        r = os.path.join(tmp, "ref")
        shutil.copytree(TOK, r)
        os.remove(os.path.join(r, "palettes", "rag", "legacy.json"))
        try:
            audit_themes(sem_l, surf, r, dd, rd)
            check("A3 missing palette -> NAMED refusal", False, "no refusal raised")
        except PaletteRefusal as e:
            check("A3 missing palette -> NAMED refusal (not a crash)",
                  "apollo-legacy" in str(e) and "palettes/rag/legacy.json" in str(e), str(e))
        except Exception as e:
            check("A3 missing palette -> NAMED refusal (not a crash)", False,
                  "crashed as %s: %s" % (type(e).__name__, e))
            traceback.print_exc()

        # --- Arm 4 (s170): OVERRIDE tier — happy path + mutation control.
        base_map = {(r["theme"], r["token"]): r for r in rows}
        li = base_map.get(("apollo-legacy", "rag/text/on-information"))
        check("A4a legacy ink comes from its OVERRIDE SET, not the base store",
              li is not None and li["ink_source"] == "theme-override"
              and li["dark_value"] == "#FFFFFF",
              "%s %s" % (li and li["ink_source"], li and li["dark_value"]))
        ci = base_map.get(("apollo-console", "rag/text/on-information"))
        # s170 (ruling 2): console + supercharge now carry the SAME ruled white,
        # so this token no longer exercises the base-ink leg. It asserts the
        # override leg for a SECOND theme instead...
        check("A4b console's on-information ink ALSO comes from its override set (s170 white)",
              ci is not None and ci["ink_source"] == "theme-override"
              and ci["dark_value"] == "#FFFFFF" and ci["base_dark_value"] == "#1A1A1A",
              "%s %s (base %s)" % (ci and ci["ink_source"], ci and ci["dark_value"],
                                   ci and ci["base_dark_value"]))
        # ...and the base-ink leg is kept alive on a token console does NOT override.
        cd = base_map.get(("apollo-console", "rag/text/on-dark"))
        check("A4b2 a token console does NOT override still retains the BASE ink",
              cd is not None and cd["ink_source"] == "base"
              and cd["dark_value"] == cd["base_dark_value"] and cd["moved"] == "ground",
              "%s %s moved=%s" % (cd and cd["ink_source"], cd and cd["dark_value"], cd and cd["moved"]))

        o = os.path.join(tmp, "ovr")
        shutil.copytree(TOK, o)
        op = os.path.join(o, "themes", "apollo-legacy.overrides.json")
        doc = json.load(open(op))
        doc["overrides"]["rag/text/on-information"]["dark"]["$value"] = "#1A1A1A"
        json.dump(doc, open(op, "w"), indent=1, ensure_ascii=False)
        _, orows = audit_themes(sem_l, surf, o, dd, rd)
        og = {(r["theme"], r["token"]): r for r in orows}
        omoved = og.get(("apollo-legacy", "rag/text/on-information"))
        oheld = og.get(("apollo-console", "rag/text/on-information"))
        check("A4c override mutation BITES: legacy ink follows the mutated file",
              omoved is not None and omoved["dark_value"] == "#1A1A1A",
              "ink=%s" % (omoved and omoved["dark_value"]))
        check("A4d override mutation FLIPS the verdict (%s -> POOR)" % (li and li["status"]),
              omoved is not None and li is not None
              and omoved["status"] == "POOR_CONTRAST" and omoved["status"] != li["status"],
              "%s %s:1 (was %s %s:1)" % (omoved and omoved["status"], omoved and omoved["contrast_ratio"],
                                         li and li["status"], li and li["contrast_ratio"]))
        check("A4e override mutation is SCOPED: console row unmoved",
              oheld is not None and ci is not None
              and oheld["dark_value"] == ci["dark_value"]
              and oheld["contrast_ratio"] == ci["contrast_ratio"],
              "console ink=%s %s:1" % (oheld and oheld["dark_value"], oheld and oheld["contrast_ratio"]))
        check("A4f real override set untouched by the mutation arm",
              json.load(open(os.path.join(TOK, "themes", "apollo-legacy.overrides.json")))
              ["overrides"]["rag/text/on-information"]["dark"]["$value"] == "#FFFFFF")

        # --- Arm 6 (s170, Dave #170): STATE-MATCHED GROUNDS.
        # The defect: a label state graded against the LIGHTEST ground across all
        # states, so Legacy's white button/primary/label/default was imagined on
        # button/primary/background/PRESSED (#FFFFFF) = 1.0:1 — a pairing that
        # cannot occur. Arm 6a asserts the phantom is gone; 6b that a genuinely
        # bad SAME-STATE pair still fails (the fix must not just silence rows);
        # 6c/6d/6e that the pairing is really being read (mutations bite, and the
        # OLD worst-case ground no longer moves the verdict) and stays scoped.
        bl = base_map.get(("apollo-legacy", "button/primary/label/default"))
        check("A6a phantom GONE: legacy primary label pairs default↔default, not ↔pressed",
              bl is not None and bl["surface"] == "#DB0011"
              and bl["surface_token"] == "button/primary/background/default"
              and bl["status"] == "OK" and bl["contrast_ratio"] == 5.22,
              "%s on %s (%s) %s:1" % (bl and bl["dark_value"], bl and bl["surface"],
                                      bl and bl["surface_token"], bl and bl["contrast_ratio"]))
        check("A6a2 no row anywhere still reports the 1.0:1 self-on-self phantom",
              all(r["contrast_ratio"] != 1.0 for r in rows),
              "1.0 rows=%s" % [r["token"] for r in rows if r["contrast_ratio"] == 1.0])
        # A6b's subject moved LEGITIMATELY at s170-D4 (Dave ruled the icon white, so the
        # live 2.42 POOR row this arm asserted no longer exists). The CLAUSE it proves —
        # a genuinely bad same-state pair still fails — is now proven on a temp copy with
        # the s170-D4 override REMOVED, which simultaneously proves that override is the
        # thing that closes the gap. The live row is asserted OK by A6b2.
        s0 = os.path.join(tmp, "state0")
        shutil.copytree(TOK, s0)
        sp0 = os.path.join(s0, "themes", "apollo-legacy.overrides.json")
        doc0 = json.load(open(sp0))
        del doc0["overrides"]["button/primary/icon/default"]
        json.dump(doc0, open(sp0, "w"), indent=1, ensure_ascii=False)
        _, s0rows = audit_themes(sem_l, surf, s0, dd, rd)
        s0g = {(r["theme"], r["token"]): r for r in s0rows}
        b0 = s0g.get(("apollo-legacy", "button/primary/icon/default"))
        check("A6b a genuinely BAD same-state pair still FAILS (s170-D4 override removed on a copy)",
              b0 is not None and b0["surface"] == "#DB0011"
              and b0["status"] == "POOR_CONTRAST" and b0["contrast_ratio"] == 2.42,
              "%s on %s = %s:1 %s" % (b0 and b0["dark_value"], b0 and b0["surface"],
                                      b0 and b0["contrast_ratio"], b0 and b0["status"]))
        bi = base_map.get(("apollo-legacy", "button/primary/icon/default"))
        check("A6b2 the LIVE icon row is white and OK under s170-D4",
              bi is not None and bi["surface"] == "#DB0011" and bi["dark_value"] == "#FFFFFF"
              and bi["status"] == "OK" and bi["contrast_ratio"] == 5.22,
              "%s on %s = %s:1 %s" % (bi and bi["dark_value"], bi and bi["surface"],
                                      bi and bi["contrast_ratio"], bi and bi["status"]))

        s1 = os.path.join(tmp, "state1")
        shutil.copytree(TOK, s1)
        sp = os.path.join(s1, "themes", "apollo-legacy.overrides.json")
        doc1 = json.load(open(sp))
        doc1["overrides"]["button/primary/background/default"]["dark"]["$value"] = "#FFFFFF"
        json.dump(doc1, open(sp, "w"), indent=1, ensure_ascii=False)
        _, s1rows = audit_themes(sem_l, surf, s1, dd, rd)
        s1g = {(r["theme"], r["token"]): r for r in s1rows}
        m1 = s1g.get(("apollo-legacy", "button/primary/label/default"))
        check("A6c mutation BITES on the MATCHED state: default ground moves the verdict",
              m1 is not None and m1["surface"] == "#FFFFFF"
              and m1["contrast_ratio"] == 1.0 and m1["status"] == "POOR_CONTRAST",
              "%s:1 on %s" % (m1 and m1["contrast_ratio"], m1 and m1["surface"]))

        s2 = os.path.join(tmp, "state2")
        shutil.copytree(TOK, s2)
        sp2 = os.path.join(s2, "themes", "apollo-legacy.overrides.json")
        doc2 = json.load(open(sp2))
        # The OLD worst-case model read THIS key for the default label. Under the
        # ruling it must be inert for that row — this arm re-enacts the reversal.
        doc2["overrides"]["button/primary/background/pressed"]["dark"]["$value"] = "#00FF00"
        json.dump(doc2, open(sp2, "w"), indent=1, ensure_ascii=False)
        _, s2rows = audit_themes(sem_l, surf, s2, dd, rd)
        s2g = {(r["theme"], r["token"]): r for r in s2rows}
        m2 = s2g.get(("apollo-legacy", "button/primary/label/default"))
        check("A6d the UNMATCHED state is INERT for that row (old model would have moved it)",
              m2 is not None and bl is not None
              and m2["surface"] == bl["surface"] and m2["contrast_ratio"] == bl["contrast_ratio"],
              "%s:1 on %s" % (m2 and m2["contrast_ratio"], m2 and m2["surface"]))
        check("A6e state arms are SCOPED: console rag rows unmoved by either mutation",
              ci is not None
              and s1g.get(("apollo-console", "rag/text/on-information"), {}).get("contrast_ratio") == ci["contrast_ratio"]
              and s2g.get(("apollo-console", "rag/text/on-information"), {}).get("contrast_ratio") == ci["contrast_ratio"],
              "s1=%s s2=%s base=%s" % (s1g.get(("apollo-console", "rag/text/on-information"), {}).get("contrast_ratio"),
                                       s2g.get(("apollo-console", "rag/text/on-information"), {}).get("contrast_ratio"),
                                       ci and ci["contrast_ratio"]))
        real_ovr = json.load(open(os.path.join(TOK, "themes", "apollo-legacy.overrides.json")))["overrides"]
        check("A6f real override set untouched by the state mutation arms",
              real_ovr["button/primary/background/default"]["dark"]["$value"] == "#DB0011"
              and real_ovr["button/primary/background/pressed"]["dark"]["$value"] == "#FFFFFF",
              "default=%s pressed=%s" % (real_ovr["button/primary/background/default"]["dark"]["$value"],
                                         real_ovr["button/primary/background/pressed"]["dark"]["$value"]))

        # --- Arm 7 (s194-D1, Dave #194): the WARN (MINOR-DEFECT) TIER.
        # The ruling changed the SHAPE of this decision: the mono white-on-error
        # pair is NOT removed from the report, it is DOWNGRADED. So the arms must
        # assert PRESENCE + ratio + stamp, never absence:
        #   7a — the mono row is PRESENT, measured at its real ratio, verdict
        #        MINOR/severity 'minor', stamped ruling s194-D1. This arm fails
        #        both on the pre-#194 body (row present but POOR/gating) AND on
        #        the exclusion form built earlier at #194 (row absent).
        #   7b — MINOR is NON-GATING: the row is not in the `poor` list the exit
        #        code is computed from, and the base pass has no gating failures.
        #   7c — the tier is THEME-SCOPED: legacy/console/supercharge are not
        #        named by the ruling, so their white-on-error rows stay measured
        #        and gating-eligible (they pass on merit, at their own ratios).
        #   7d — CONSERVATIVE: exactly ONE row in the whole report is minor.
        #   7e — _excluded_surfaces still ACCUMULATES across family prefixes (the
        #        pre-#194 first-match `return` dropped R-D3/R-D12 amber/green/info),
        #        and rag/error-background is NOT among the exclusions any more —
        #        the ruling forbids removing it.
        b_audit, b_poor, _b_skip = audit_base(sem_l, surf, dd, rd)
        b_map = {r["token"]: r for r in b_audit}
        woe_mono = b_map.get("rag/text/on-dark")
        check("A7a s194-D1 WARN tier: the mono white-on-error row is PRESENT, measured, stamped",
              woe_mono is not None
              and woe_mono["dark_value"] == "#FFFFFF"
              and woe_mono["surface"] == "#F6604C"
              and woe_mono["surface_token"] == "rag/error-background"
              and woe_mono["contrast_ratio"] == 3.14
              and woe_mono["status"] == "MINOR" and woe_mono["severity"] == "minor"
              and woe_mono["ruling"] == "s194-D1",
              "%s on %s (%s) = %s:1 %s/%s ruled %s" % (
                  woe_mono and woe_mono["dark_value"], woe_mono and woe_mono["surface"],
                  woe_mono and woe_mono["surface_token"], woe_mono and woe_mono["contrast_ratio"],
                  woe_mono and woe_mono["status"], woe_mono and woe_mono["severity"],
                  woe_mono and woe_mono["ruling"]))
        check("A7b MINOR is NON-GATING: it is absent from the gating list, base pass clean",
              woe_mono not in b_poor and len(b_poor) == 0,
              "gating rows=%s" % [r["token"] for r in b_poor])
        woe = {r["theme"]: r for r in rows
               if r["token"] == "rag/text/on-dark" and r["surface_token"] == "rag/error-background"}
        check("A7c the tier is THEME-SCOPED: the three NON-mono rows stay MEASURED and GATING-eligible",
              set(woe) == {"apollo-legacy", "apollo-console", "apollo-supercharge"}
              and all(r["status"] == "OK" and r["severity"] == "pass"
                      and r["ruling"] is None and r["dark_value"] == "#FFFFFF"
                      for r in woe.values()),
              "; ".join("%s %s on %s %s:1 %s" % (k, r["dark_value"], r["surface"],
                                                 r["contrast_ratio"], r["status"])
                        for k, r in sorted(woe.items())))
        all_min = [r for r in b_audit if r["status"] == "MINOR"] + \
                  [r for r in rows if r["status"] == "MINOR"]
        check("A7d CONSERVATIVE: exactly ONE minor row in the whole report; no other verdict moved",
              len(all_min) == 1 and all_min[0]["token"] == "rag/text/on-dark"
              and all(r["severity"] in ("pass", "gating")
                      for r in b_audit + rows if r["status"] != "MINOR"),
              "minor rows=%s" % [(r.get("theme", ACTIVE_BASE), r["token"]) for r in all_min])
        mono_x = _excluded_surfaces("rag/text/on-dark", ACTIVE_BASE)
        leg_x = _excluded_surfaces("rag/text/on-dark", "apollo-legacy")
        check("A7e exclusions ACCUMULATE across family prefixes, and error-background is NOT excluded",
              {"rag/warning-background", "rag/success-background",
               "rag/information-background"} <= set(mono_x)
              and {"rag/warning-background", "rag/success-background",
                   "rag/information-background"} <= set(leg_x)
              and "rag/error-background" not in mono_x
              and "rag/error-background" not in leg_x,
              "mono=%s" % sorted(mono_x))

        # --- Arm 5 (s170): NAMED refusal — declared overrideSet missing.
        r2 = os.path.join(tmp, "ref2")
        shutil.copytree(TOK, r2)
        os.remove(os.path.join(r2, "themes", "apollo-legacy.overrides.json"))
        try:
            audit_themes(sem_l, surf, r2, dd, rd)
            check("A5 missing overrideSet -> NAMED refusal", False, "no refusal raised")
        except OverrideRefusal as e:
            check("A5 missing overrideSet -> NAMED OverrideRefusal (not a crash, not a base fall-back)",
                  "apollo-legacy" in str(e) and "themes/apollo-legacy.overrides.json" in str(e), str(e))
        except Exception as e:
            check("A5 missing overrideSet -> NAMED OverrideRefusal", False,
                  "crashed as %s: %s" % (type(e).__name__, e))
            traceback.print_exc()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nselftest: %d arm(s), %d failed" % (len(arms), fails))
    return 1 if fails else 0


if "--selftest" in sys.argv[1:]:
    sys.exit(_selftest())


sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))
surfaces = load_dark_surfaces(sem)
DEFAULT_DARK, RAISED_DARK = standard_dark_surfaces(TOK)

audit, poor, skipped = audit_base(sem, surfaces, DEFAULT_DARK, RAISED_DARK)

ok_count = sum(1 for r in audit if r["status"] == "OK")
allowed = [r for r in audit if r["status"] == "ALLOWED"]
minor_rows = [r for r in audit if r["status"] == "MINOR"]

# s169 ruling C': regrade palette-owned grounds per theme. A refusal here is
# fatal and NAMED — a theme whose declared palette cannot be read must not be
# silently graded against the base store, which was the whole defect (red 30).
try:
    theme_palettes, theme_rows = audit_themes(sem, surfaces, TOK, DEFAULT_DARK, RAISED_DARK)
except PaletteRefusal as e:
    sys.stderr.write("REFUSED (palette tier): %s\n" % e)
    sys.exit(2)
except OverrideRefusal as e:
    sys.stderr.write("REFUSED (theme override set): %s\n" % e)
    sys.exit(2)
theme_poor = [r for r in theme_rows if r["status"] == "POOR_CONTRAST"]
theme_exempt = [r for r in theme_rows if r["status"] == "EXEMPTED"]
theme_minor = [r for r in theme_rows if r["status"] == "MINOR"]
# s194-D1: minor rows are NON-GATING. They are counted and printed, never added
# to `poor`/`theme_poor` — the two lists the exit code is computed from.
all_minor = minor_rows + theme_minor

audit_json = {
    "$description": "Text/icon dark-mode contrast audit. Each token is tested against the worst-case (lightest) dark surface it can sit on, resolved from the store (page default + raised island, or its own group's surfaces). s170 (Dave, #170): a STATE-SUFFIXED ink is paired only with its OWN state's ground (default<->default, pressed<->pressed); worst-case across states is used only where no state-matched ground exists. on-light tokens are excluded (light-only). Allowlisted disabled-state tokens are reported but do not gate. POOR_CONTRAST (non-allowlisted, below threshold) FAILS the build.",
    "generated": "2026-06-19",
    "default_dark_surface": DEFAULT_DARK,
    "raised_dark_surface": RAISED_DARK,
    "totals": {
        "text_icon_tokens": len(audit), "ok": ok_count,
        "allowed_exceptions": len(allowed), "poor_contrast": len(poor),
        "minor_defects": len(minor_rows),
        "skipped_light_only": len(skipped),
        "per_theme_regraded": len(theme_rows),
        "per_theme_poor_contrast": len(theme_poor),
        "per_theme_exempted": len(theme_exempt),
        "per_theme_minor_defects": len(theme_minor),
    },
    "per_theme": {
        "$description": "s169+s170 (ruling C'): pairs whose GROUND is palette-owned (s157-D2 tier, single-sourced by s158-D4) or whose INK the theme re-binds in its own overrideSet, regraded per theme via tokens/themes/_themes.json -> ragPalette + overrideSet. Rows appear only where the theme's resolved surface or ink DIFFERS from the base pass, so the activeBase (apollo-mono) reading is not double-counted; 'moved' names which of ink/ground/ink+ground shifted and 'ink_source' says whether the ink came from the theme's override set. POOR_CONTRAST rows GATE on the same terms as the base pass; EXEMPTED = an R-D24 Legacy pair matched in _contrast_utils.LEGACY_THEME_EXEMPTIONS (documented, never counted as a pass).",
        "palettes": {k: v["palette"] for k, v in theme_palettes.items()},
        "override_sets": {k: v["override_set"] for k, v in theme_palettes.items()},
        "rows": theme_rows,
        "poor_contrast": theme_poor,
        "minor_defects": theme_minor,
    },
    "poor_contrast": poor,
    "minor_defects": {
        "$description": "s194-D1 (Dave, #194) WARN tier: pairs a ruling ABOLISHES stay MEASURED and REPORTED with their real ratio, stamped with the ruling that downgrades them, and do NOT gate the build. Dave #194: 'this should be a warning not an error. if it was a proper ally review it would be a minor defect'. Reachable only via _contrast_utils.MINOR_PAIRS — a named pair under a named theme; every other row keeps its previous verdict. Severity vocabulary: pass / minor / gating.",
        "rows": all_minor,
    },
    "allowed_exceptions": allowed,
    "skipped_light_only": skipped,
    "tokens": OrderedDict((r["token"], r) for r in audit),
}
json.dump(audit_json, open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

L = [
    "# Text/icon token dark-mode contrast audit",
    "",
    f"> Each text/icon token is tested against the **worst-case (lightest) dark surface it can sit on**, resolved from the store — page default `{DEFAULT_DARK}` + raised island `{RAISED_DARK}`, or the token's own group surfaces. Since **s170** a state-suffixed ink (e.g. `.../label/default`) is paired only with its OWN state's ground — worst-case across states is a fall-back, not the rule. `on-light` tokens are excluded (light-only). Disabled-state tokens are allowlisted (reported, not gated). Text needs 4.5:1, icons/UI need 3:1.",
    "",
    f"**Result:** {ok_count} pass · {len(allowed)} allowed exception(s) · **{len(minor_rows)} minor defect(s) (⚠ warn, non-gating)** · **{len(poor)} gating failure(s)** · {len(skipped)} skipped (light-only).",
    "",
    f"**Per-theme (s169 grounds + s170 overrides):** {len(theme_rows)} pair(s) regraded where a theme moves the ground or the ink · **{len(theme_poor)} gating failure(s)** · {len(theme_minor)} minor (⚠ warn) · {len(theme_exempt)} R-D24 exempted.",
    "",
]
if theme_rows:
    L += ["## Per-theme palette-resolved pairs (s157-D2 palette tier)", "",
          "> The base pass above reads the semantic store, i.e. the activeBase theme (**apollo-mono**). Grounds owned by the palette tier are re-resolved here per theme via `tokens/themes/_themes.json` → `ragPalette`, and INKS are re-resolved per theme via that theme's `overrideSet` (s170). Only pairs whose ground or ink MOVES are listed; the `Moved` column says which. `❌` rows gate the build exactly as base failures do; `EXEMPTED` = a Legacy pair matched in R-D24's table.", "",
          "| Theme | Palette | Token | Moved | Ink (base → theme) | Ground (base → theme) | Contrast | Need | Status |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in theme_rows:
        badge = {"OK": "✅ OK", "ALLOWED": "🟡 ALLOWED", "EXEMPTED": "🟡 EXEMPTED",
                 "MINOR": "⚠ minor (ruled %s)" % (r.get("ruling") or "—"), "POOR_CONTRAST": "❌ POOR"}[r["status"]]
        ink = (f"`{r['base_dark_value']}` → `{r['dark_value']}`" if r["ink_source"] == "theme-override"
               else f"`{r['dark_value']}`")
        # surface_token is None when the ground is the page/raised fallback rather
        # than a named group surface — say so, never print a bare "None".
        gname = f"`{r['surface_token']}` " if r["surface_token"] else "page/raised "
        gnd = (f"{gname}`{r['base_surface']}` → `{r['surface']}`"
               if r["surface"] != r["base_surface"] else f"{gname}`{r['surface']}`")
        L.append(f"| **{r['theme_label']}** (`{r['theme']}`) | `{r['palette']}` | `{r['token']}` | {r['moved']} | {ink} | {gnd} | **{r['contrast_ratio']}:1** | {r['threshold']}:1 | {badge} |")
    L.append("")
if all_minor:
    L += ["## ⚠ Minor defects — measured, reported, NOT gating (s194-D1)", "",
          "> **s194-D1 (Dave, #194):** *\"this should be a warning not an error. if it was a proper ally review it would be a minor defect\"*. A pairing a ruling ABOLISHES is not deleted from this report and is not a build failure either — it is measured, printed with its real ratio, and stamped with the ruling that downgrades it. These rows do NOT affect the exit code.", "",
          "| Theme | Token | Ink | Ground | Contrast | Need | Verdict | Ruling |",
          "|---|---|---|---|---|---|---|---|"]
    for r in all_minor:
        L.append(f"| `{r.get('theme', ACTIVE_BASE)}` | `{r['token']}` | `{r['dark_value']}` | `{r.get('surface_token') or 'page/raised'}` `{r['surface']}` | **{r['contrast_ratio']}:1** | {r['threshold']}:1 | ⚠ minor | `{r.get('ruling')}` |")
    L += ["", "Why each is minor:", ""]
    for r in all_minor:
        L.append(f"- `{r['token']}` × `{r.get('surface_token')}` under `{r.get('theme', ACTIVE_BASE)}` — {r.get('minor_reason')}")
    L.append("")
if poor:
    L += ["## ❌ Gating failures — these FAIL the build", "",
          "| Token | Dark value | Surface | Contrast | Need | Context |",
          "|---|---|---|---|---|---|"]
    for r in poor:
        L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` ({r['surface_label']}) | **{r['contrast_ratio']}:1** | {r['threshold']}:1 | {r['context']} |")
    L.append("")
if allowed:
    L += ["## Allowed exceptions (reported, not gated)", "",
          "| Token | Dark value | Surface | Contrast | Reason |",
          "|---|---|---|---|---|"]
    for r in allowed:
        L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` | {r['contrast_ratio']}:1 | {r['allowlist_reason']} |")
    L.append("")
if skipped:
    L += ["## Skipped — light-mode-only tokens", "",
          "| Token | Reason |", "|---|---|"]
    for r in skipped:
        L.append(f"| `{r['token']}` | {r['reason']} |")
    L.append("")
L += ["## All audited text/icon tokens", "",
      "| Token | Dark value | Surface | Contrast | Status |", "|---|---|---|---|---|"]
for r in audit:
    badge = {"OK": "✅ OK", "ALLOWED": "🟡 ALLOWED",
             "MINOR": "⚠ minor (ruled %s)" % (r.get("ruling") or "—"),
             "POOR_CONTRAST": "❌ POOR"}[r["status"]]
    L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` | {r['contrast_ratio']}:1 | {badge} |")
open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.md"), "w").write("\n".join(L))

print(f"text/icon contrast audit: {ok_count} OK, {len(allowed)} allowed, {len(minor_rows)} MINOR(warn), {len(poor)} GATING FAIL, {len(skipped)} skipped(light-only)")
for r in all_minor:
    print(f"  \u26a0 minor (ruled {r.get('ruling')}) [{r.get('theme', ACTIVE_BASE)}] {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} ({r.get('surface_token')}) — non-gating")
for r in poor:
    print(f"  ❌ {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} (need {r['threshold']}:1, {r['context']})")
print(f"per-theme palette grounds ({len(theme_palettes)} themes declared): {len(theme_rows)} regraded, {len(theme_poor)} GATING FAIL, {len(theme_minor)} MINOR(warn), {len(theme_exempt)} R-D24 exempted")
for r in theme_poor:
    print(f"  ❌ [{r['theme']}] {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} ({r['surface_token']}, was {r['base_surface']} in base) (need {r['threshold']}:1, {r['context']})")
sys.exit(1 if (poor or theme_poor) else 0)
