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
    legacy_exemption, _leaf_dark_hex,
    CONTRAST_ALLOWLIST,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(ROOT, "tokens")


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
        out[key] = {"label": t.get("label", key), "attr": t.get("attr", key),
                    "palette": rel, "surfaces": vals}
    if not out:
        raise PaletteRefusal("no theme in %s declares a ragPalette" % reg_path)
    return out


def theme_surface_map(base_surfaces, pal_surfaces):
    """Base surface map with palette-owned entries REPLACED by the theme's value.
    Only names the base map already knows are substituted — the palette does not
    mint surfaces, it re-values the ones the semantic tier declares."""
    s = dict(base_surfaces)
    for name, hx in pal_surfaces.items():
        if name in base_surfaces:
            s[name] = hx
    return s


def grade(name, node, surfaces, default_dark, raised_dark):
    """Grade one token against a given surface map. Returns a record or None."""
    dark_val = mode_val(node, "dark")
    if not (isinstance(dark_val, str) and dark_val.startswith("#")):
        return None
    surface, label = resolve_dark_surface(name, surfaces, default_dark, raised_dark)
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
    """Regrade every token whose surface MOVES under a theme's palette.

    Rows are emitted only where the theme's resolved surface differs from the
    base pass, so the activeBase reading is never double-counted. Legacy pairs
    are routed through _contrast_utils.legacy_exemption() per R-D24's own
    instruction; a hit is recorded as EXEMPTED (documented), never as a pass.
    A miss is a real failure and gates like any other.
    """
    palettes = load_theme_palettes(tok_dir)
    rows = []
    for tkey, meta in palettes.items():
        smap = theme_surface_map(base_surfaces, meta["surfaces"])
        for name, node in sorted(sem_leaves.items()):
            if not is_text_or_icon_token(name):
                continue
            if "light" not in node or "dark" not in node:
                continue
            base_rec = grade(name, node, base_surfaces, default_dark, raised_dark)
            th_rec = grade(name, node, smap, default_dark, raised_dark)
            if base_rec is None or th_rec is None:
                continue
            if th_rec["surface"] == base_rec["surface"]:
                continue  # palette does not move this pair; base pass covers it
            owner = next((n for n, hx in meta["surfaces"].items()
                          if hx == th_rec["surface"] and n in base_surfaces), None)
            exempt = legacy_exemption(name, owner or "") if meta["attr"] == "legacy" else None
            if th_rec["passes"]:
                status = "OK"
            elif exempt:
                status = "EXEMPTED"
            elif th_rec["allowlisted"]:
                status = "ALLOWED"
            else:
                status = "POOR_CONTRAST"
            th_rec.update({"theme": tkey, "theme_label": meta["label"],
                           "palette": meta["palette"], "surface_token": owner,
                           "base_surface": base_rec["surface"],
                           "base_contrast_ratio": base_rec["contrast_ratio"],
                           "status": status, "exemption_reason": exempt,
                           "allowlist_reason": CONTRAST_ALLOWLIST.get(name) if (th_rec["allowlisted"] and not th_rec["passes"]) else None})
            th_rec.pop("passes"); th_rec.pop("allowlisted")
            rows.append(th_rec)
    return palettes, rows


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
    check("A1e measured ratios match first-hand probe",
          ratios.get(("apollo-legacy", "rag/text/on-dark")) == 7.87
          and ratios.get(("apollo-legacy", "rag/text/on-information")) == 2.21
          and ratios.get(("apollo-console", "rag/text/on-dark")) == 6.02
          and ratios.get(("apollo-console", "rag/text/on-information")) == 2.89,
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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nselftest: %d arm(s), %d failed" % (len(arms), fails))
    return 1 if fails else 0


if "--selftest" in sys.argv[1:]:
    sys.exit(_selftest())


sem = leaves(json.load(open(os.path.join(TOK, "semantic-colour.json"))))
surfaces = load_dark_surfaces(sem)
DEFAULT_DARK, RAISED_DARK = standard_dark_surfaces(TOK)

audit, poor, skipped = [], [], []

for name, node in sorted(sem.items()):
    if not is_text_or_icon_token(name):
        continue
    if "light" not in node or "dark" not in node:
        continue
    dark_val = mode_val(node, "dark")
    if not (isinstance(dark_val, str) and dark_val.startswith("#")):
        continue

    surface, label = resolve_dark_surface(name, surfaces, DEFAULT_DARK, RAISED_DARK)
    if surface is None:
        skipped.append({"token": name, "dark_value": dark_val, "reason": label})
        continue

    context = "text" if "text" in name else "ui"
    threshold = 4.5 if context == "text" else 3.0
    ratio = contrast_ratio(dark_val, surface)
    passes = is_sufficient_contrast(ratio, context=context)
    allowlisted = name in CONTRAST_ALLOWLIST

    rec = {
        "token": name, "dark_value": dark_val,
        "surface": surface, "surface_label": label,
        "contrast_ratio": ratio, "threshold": threshold, "context": context,
        "status": "OK" if passes else ("ALLOWED" if allowlisted else "POOR_CONTRAST"),
        "allowlist_reason": CONTRAST_ALLOWLIST.get(name) if (allowlisted and not passes) else None,
    }
    audit.append(rec)
    if not passes and not allowlisted:
        poor.append(rec)

ok_count = sum(1 for r in audit if r["status"] == "OK")
allowed = [r for r in audit if r["status"] == "ALLOWED"]

# s169 ruling C': regrade palette-owned grounds per theme. A refusal here is
# fatal and NAMED — a theme whose declared palette cannot be read must not be
# silently graded against the base store, which was the whole defect (red 30).
try:
    theme_palettes, theme_rows = audit_themes(sem, surfaces, TOK, DEFAULT_DARK, RAISED_DARK)
except PaletteRefusal as e:
    sys.stderr.write("REFUSED (palette tier): %s\n" % e)
    sys.exit(2)
theme_poor = [r for r in theme_rows if r["status"] == "POOR_CONTRAST"]
theme_exempt = [r for r in theme_rows if r["status"] == "EXEMPTED"]

audit_json = {
    "$description": "Text/icon dark-mode contrast audit. Each token is tested against the worst-case (lightest) dark surface it can sit on, resolved from the store (page default + raised island, or its own group's surfaces). on-light tokens are excluded (light-only). Allowlisted disabled-state tokens are reported but do not gate. POOR_CONTRAST (non-allowlisted, below threshold) FAILS the build.",
    "generated": "2026-06-19",
    "default_dark_surface": DEFAULT_DARK,
    "raised_dark_surface": RAISED_DARK,
    "totals": {
        "text_icon_tokens": len(audit), "ok": ok_count,
        "allowed_exceptions": len(allowed), "poor_contrast": len(poor),
        "skipped_light_only": len(skipped),
        "per_theme_regraded": len(theme_rows),
        "per_theme_poor_contrast": len(theme_poor),
        "per_theme_exempted": len(theme_exempt),
    },
    "per_theme": {
        "$description": "s169 (ruling C'): pairs whose GROUND is palette-owned (s157-D2 tier, single-sourced by s158-D4) regraded per theme via tokens/themes/_themes.json -> ragPalette. Rows appear only where the theme's resolved surface DIFFERS from the base pass, so the activeBase (apollo-mono) reading is not double-counted. POOR_CONTRAST rows GATE on the same terms as the base pass; EXEMPTED = an R-D24 Legacy pair matched in _contrast_utils.LEGACY_THEME_EXEMPTIONS (documented, never counted as a pass).",
        "palettes": {k: v["palette"] for k, v in theme_palettes.items()},
        "rows": theme_rows,
        "poor_contrast": theme_poor,
    },
    "poor_contrast": poor,
    "allowed_exceptions": allowed,
    "skipped_light_only": skipped,
    "tokens": OrderedDict((r["token"], r) for r in audit),
}
json.dump(audit_json, open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.json"), "w"), indent=2, ensure_ascii=False)

L = [
    "# Text/icon token dark-mode contrast audit",
    "",
    f"> Each text/icon token is tested against the **worst-case (lightest) dark surface it can sit on**, resolved from the store — page default `{DEFAULT_DARK}` + raised island `{RAISED_DARK}`, or the token's own group surfaces. `on-light` tokens are excluded (light-only). Disabled-state tokens are allowlisted (reported, not gated). Text needs 4.5:1, icons/UI need 3:1.",
    "",
    f"**Result:** {ok_count} pass · {len(allowed)} allowed exception(s) · **{len(poor)} gating failure(s)** · {len(skipped)} skipped (light-only).",
    "",
    f"**Per-theme (s169):** {len(theme_rows)} pair(s) regraded on palette-owned grounds · **{len(theme_poor)} gating failure(s)** · {len(theme_exempt)} R-D24 exempted.",
    "",
]
if theme_rows:
    L += ["## Per-theme palette-resolved pairs (s157-D2 palette tier)", "",
          "> The base pass above reads the semantic store, i.e. the activeBase theme (**apollo-mono**). Grounds owned by the palette tier are re-resolved here per theme via `tokens/themes/_themes.json` → `ragPalette`. Only pairs whose ground MOVES are listed. `❌` rows gate the build exactly as base failures do; `EXEMPTED` = a Legacy pair matched in R-D24's table.", "",
          "| Theme | Palette | Token | Value | Ground (base → theme) | Contrast | Need | Status |",
          "|---|---|---|---|---|---|---|---|"]
    for r in theme_rows:
        badge = {"OK": "✅ OK", "ALLOWED": "🟡 ALLOWED", "EXEMPTED": "🟡 EXEMPTED", "POOR_CONTRAST": "❌ POOR"}[r["status"]]
        L.append(f"| **{r['theme_label']}** (`{r['theme']}`) | `{r['palette']}` | `{r['token']}` | `{r['dark_value']}` | `{r['surface_token']}` `{r['base_surface']}` → `{r['surface']}` | **{r['contrast_ratio']}:1** | {r['threshold']}:1 | {badge} |")
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
    badge = {"OK": "✅ OK", "ALLOWED": "🟡 ALLOWED", "POOR_CONTRAST": "❌ POOR"}[r["status"]]
    L.append(f"| `{r['token']}` | `{r['dark_value']}` | `{r['surface']}` | {r['contrast_ratio']}:1 | {badge} |")
open(os.path.join(ROOT, "_TEXT-CONTRAST-AUDIT.md"), "w").write("\n".join(L))

print(f"text/icon contrast audit: {ok_count} OK, {len(allowed)} allowed, {len(poor)} GATING FAIL, {len(skipped)} skipped(light-only)")
for r in poor:
    print(f"  ❌ {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} (need {r['threshold']}:1, {r['context']})")
print(f"per-theme palette grounds ({len(theme_palettes)} themes declared): {len(theme_rows)} regraded, {len(theme_poor)} GATING FAIL, {len(theme_exempt)} R-D24 exempted")
for r in theme_poor:
    print(f"  ❌ [{r['theme']}] {r['token']}: {r['contrast_ratio']}:1 on {r['surface']} ({r['surface_token']}, was {r['base_surface']} in base) (need {r['threshold']}:1, {r['context']})")
sys.exit(1 if (poor or theme_poor) else 0)
