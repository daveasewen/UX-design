#!/usr/bin/env python3
"""Theme-provenance gate (ADR-0011, R-D19) — ADVISORY.

Makes "red = Legacy" mechanically visible. For every Mono-designated LIBRARY surface it flags any
colour that belongs to another theme's override set — including HARDCODED Legacy hexes in live CSS,
the blind spot the token-resolution leak gate (_validate_legacy_leak.py) cannot see because it only
walks token-manifest bindings.

Scope (see knowledge/_STYLE-PROVENANCE.md, the human record — this mirrors it):
  Mono-designated = snippets/ + _proforma/ + _review/ (the library).
  Excluded        = _fitness-test/ (test pages + pre-canon exploration + research).

ADVISORY: writes _THEME-PROVENANCE-GATE.md and always exits 0. Promote to blocking (exit 1 on
unwaived flags) once the migration in _STYLE-PROVENANCE.md §backlog is done (ADR-0011).
"""
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = json.load(open(os.path.join(HERE, "tokens", "themes", "_themes.json")))
BASE = THEMES.get("activeBase", "apollo-mono")

# Non-base themes' owned hexes = "must not appear in a Mono surface".
FOREIGN = {}
for tid, t in THEMES["themes"].items():
    if tid == BASE:
        continue
    for hexv, why in t.get("ownsHexes", {}).items():
        FOREIGN[hexv.upper()] = f"{t['label']}: {why}"

MONO_DIRS = ["snippets", "_proforma", "_review"]
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")


def strip_noise(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)          # html comments (token-manifests live here)
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)            # css comments
    t = re.sub(r'<script[^>]*application/json[^>]*>.*?</script>', "", t, flags=re.S)
    t = re.sub(r'<script[^>]*id="token-manifest"[^>]*>.*?</script>', "", t, flags=re.S)
    return t


def main():
    flags = []          # (dir, file, hex, reason, count)
    scanned = 0
    for d in MONO_DIRS:
        base = os.path.join(HERE, d)
        for root, _, files in os.walk(base):
            for fn in files:
                if not fn.endswith(".html"):
                    continue
                scanned += 1
                live = strip_noise(open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read())
                seen = {}
                for m in HEX_RE.finditer(live):
                    h = m.group(0).upper()
                    if h in FOREIGN:
                        seen[h] = seen.get(h, 0) + 1
                for h, n in sorted(seen.items()):
                    flags.append((d, fn, h, FOREIGN[h], n))

    lines = ["# Theme-provenance gate (ADR-0011, R-D19) — ADVISORY\n\n",
             f"Scanned **{scanned}** Mono-designated library files "
             f"({', '.join(MONO_DIRS)}). Foreign-theme hexes checked: "
             f"{', '.join(sorted(FOREIGN))}.\n\n",
             f"**{len(flags)}** hardcoded foreign-theme colour(s) found in live CSS "
             f"(comments + token-manifests excluded).\n"]
    if flags:
        lines.append("\n| Area | File | Hex | ×  | Belongs to |\n|---|---|---|---|---|\n")
        for d, fn, h, why, n in flags:
            lines.append(f"| {d} | {fn} | `{h}` | {n} | {why} |\n")
        lines.append("\n> These are the drift the record (`_STYLE-PROVENANCE.md` §backlog) tracks. "
                     "Re-home to Mono values, then promote this gate to blocking (ADR-0011).\n")
    else:
        lines.append("\n✅ No hardcoded foreign-theme colour in any Mono surface.\n")
    open(os.path.join(HERE, "_THEME-PROVENANCE-GATE.md"), "w", encoding="utf-8").writelines(lines)

    print(f"theme-provenance gate (ADVISORY): {len(flags)} hardcoded foreign-theme hex(es) "
          f"in {scanned} Mono files. See _THEME-PROVENANCE-GATE.md")
    sys.exit(0)   # advisory


if __name__ == "__main__":
    main()
