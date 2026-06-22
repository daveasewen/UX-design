#!/usr/bin/env python3
"""
gate2_assembly.py — assembly-tier ("gate 2") enforcement for a generated screen.

Component gates ask "is each PART sound?" This gate asks the question a component
library, Figma Code Connect, and the generator itself CANNOT answer:
"once the parts are assembled and the numbers have to agree, is the SCREEN sound?"

Verification = enforcement: exits non-zero (withholds "done") on any BLOCK failure.
Runs on the screen as STRUCTURED DATA (screen.json), not pixels — you cannot check that
two amounts should match when they are just two unrelated text layers.

Usage:  python3 gate2_assembly.py [screen.json]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- WCAG contrast helpers ----------
def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def _luminance(h):
    r, g, b = _hex_to_rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def contrast(h1, h2):
    a, b = _luminance(h1), _luminance(h2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

def _is_reddish(h):
    r, g, b = _hex_to_rgb(h)
    return r > 150 and g < 110 and b < 110 and (r - g) > 80

# ---------- findings ----------
findings = []  # (id, severity, ok, msg)
def record(cid, severity, ok, msg):
    findings.append((cid, severity, ok, msg))

def gbp(n):
    return f"£{n:,.0f}"

def run(screen):
    cp = screen.get("cash_position", {})
    up = screen.get("upcoming_payments", {})
    rows = up.get("rows", [])

    # DATA-1 — cross-panel amount consistency
    amounts = {}
    for it in screen.get("pending_approval", []):
        amounts.setdefault(it["payee"], {}).setdefault(it["amount"], set()).add("pending approval")
    for r in rows:
        amounts.setdefault(r["payee"], {}).setdefault(r["amount"], set()).add("upcoming")
    mism = {p: a for p, a in amounts.items() if len(a) > 1}
    if mism:
        parts = []
        for p, a in mism.items():
            where = "; ".join(f"{gbp(amt)} in {', '.join(sorted(loc))}" for amt, loc in a.items())
            parts.append(f"{p}: {where}")
        record("DATA-1", "BLOCK", False, "Same payee, different amounts across panels — " + " | ".join(parts))
    else:
        record("DATA-1", "BLOCK", True, "All cross-panel amounts reconcile.")

    # DATA-2 — stated total reconciles with itemised rows
    shown_sum = sum(r["amount"] for r in rows)
    total_stated = up.get("total_stated")
    count_stated = up.get("count_stated")
    if total_stated is not None:
        if shown_sum > total_stated:
            record("DATA-2", "BLOCK", False,
                   f"{len(rows)} shown rows already sum to {gbp(shown_sum)}, exceeding the stated "
                   f"total {gbp(total_stated)} for {count_stated} payments.")
        elif len(rows) == count_stated and shown_sum != total_stated:
            record("DATA-2", "BLOCK", False,
                   f"All {count_stated} rows shown sum to {gbp(shown_sum)} but stated total is {gbp(total_stated)}.")
        else:
            record("DATA-2", "BLOCK", True, f"Stated total {gbp(total_stated)} ≥ shown rows {gbp(shown_sum)}.")

    # DATA-3 — reassurance must be backed by the data
    cov = screen.get("coverage_banner")
    if cov and cov.get("covered"):
        period = cov.get("period", "")
        oblig = sum(r["amount"] for r in rows if r.get("month") == period)
        available = cp.get("current_balance", 0)
        actual_buffer = available - oblig
        claimed = cov.get("claimed_buffer")
        ok = actual_buffer >= 0 and (claimed is None or actual_buffer >= claimed)
        if ok:
            record("DATA-3", "BLOCK", True,
                   f"'Covered through {period}' holds: balance {gbp(available)} − scheduled "
                   f"{gbp(oblig)} = {gbp(actual_buffer)}.")
        else:
            claim_txt = f" (banner claims +{gbp(claimed)} buffer)" if claimed is not None else ""
            record("DATA-3", "BLOCK", False,
                   f"'Covered through {period}' is FALSE: scheduled {period} payments {gbp(oblig)} "
                   f"vs balance {gbp(available)} -> shortfall {gbp(oblig - available)}{claim_txt}.")
    else:
        record("DATA-3", "BLOCK", True, "No unverified coverage claim.")

    # A11Y-1 — non-text contrast on action tiles (1.4.11)
    bad = []
    for t in screen.get("action_tiles", []):
        cr = contrast(t["glyph_color"], t["fill"])
        if cr < 3.0:
            bad.append(f"{t['label']} ({t['glyph_color']} on {t['fill']} = {cr:.2f}:1)")
    if bad:
        record("A11Y-1", "BLOCK", False, "Action-tile glyph contrast < 3:1 (1.4.11): " + "; ".join(bad))
    else:
        record("A11Y-1", "BLOCK", True, "All action-tile glyphs >= 3:1.")

    # BRAND-1 — red reserved for destructive
    redroutine = [t["label"] for t in screen.get("action_tiles", [])
                  if _is_reddish(t["fill"]) and t.get("role") != "destructive"]
    if redroutine:
        record("BRAND-1", "BLOCK", False, "Destructive/error red used for routine action(s): " + ", ".join(redroutine))
    else:
        record("BRAND-1", "BLOCK", True, "Red reserved for destructive actions.")

    # FLOW-1 — high-value approval needs confirmation
    noconfirm = [f"{it['payee']} {gbp(it['amount'])}" for it in screen.get("pending_approval", [])
                 if it["amount"] > 10000 and not it.get("confirmation_step")]
    if noconfirm:
        record("FLOW-1", "BLOCK", False, "High-value approval with no confirmation step: " + "; ".join(noconfirm))
    else:
        record("FLOW-1", "BLOCK", True, "High-value approvals require confirmation.")

    # COPY-1 — currency formatting consistency
    styles = set("symbol" if f.strip().startswith("£") else "code" for f in screen.get("currency_formats_seen", []))
    if len(styles) > 1:
        record("COPY-1", "WARN", False, "Mixed currency formats: " + ", ".join(screen.get("currency_formats_seen", [])))
    else:
        record("COPY-1", "WARN", True, "Consistent currency format.")

    # COPY-2 — all-caps labels
    caps = screen.get("labels_uppercase", [])
    record("COPY-2", "WARN", not caps,
           f"{len(caps)} all-caps labels/banners (readability)." if caps else "No all-caps labels.")

    # PII-1 — sort-code masking
    fullsort = [r["payee"] for r in rows if r.get("sort_code") and re.match(r"^\d\d-\d\d-\d\d$", r["sort_code"])]
    record("PII-1", "WARN", not fullsort,
           f"Sort code shown in full for {len(fullsort)} payee(s) — confirm masking policy."
           if fullsort else "Sort-code masking policy OK.")

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "screen.json")
    with open(path, encoding="utf-8") as fh:
        screen = json.load(fh)
    run(screen)

    blocks = [f for f in findings if f[1] == "BLOCK"]
    warns = [f for f in findings if f[1] == "WARN"]
    block_fail = [f for f in blocks if not f[2]]
    warn_fail = [f for f in warns if not f[2]]

    out = []
    out.append("# Gate 2 — assembly-tier report")
    out.append(f"*Screen: {screen.get('screen')} · source: {screen.get('source')}*\n")
    verdict = "🔴 FAIL" if block_fail else "✅ PASS"
    out.append(f"**Verdict: {verdict}** — {len(block_fail)}/{len(blocks)} blocking checks failed, "
               f"{len(warn_fail)}/{len(warns)} advisory flags.\n")
    out.append("## Blocking gates")
    for cid, sev, ok, msg in blocks:
        out.append(f"- {'✅' if ok else '🔴'} **{cid}** — {msg}")
    out.append("\n## Advisory")
    for cid, sev, ok, msg in warns:
        out.append(f"- {'✅' if ok else '🟡'} **{cid}** — {msg}")
    report = "\n".join(out)

    print(report)
    with open(os.path.join(HERE, "_GATE2-REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write(report + "\n")

    sys.exit(1 if block_fail else 0)

if __name__ == "__main__":
    main()
