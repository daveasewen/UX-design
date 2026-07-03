#!/usr/bin/env python3
"""
_validate_advisory.py — ADVISORY signals: recorded prose rules, made executable.

Entry path per ADR-0005 §5: new check classes (heuristics, CX, content) enter at the
ADVISORY tier — they annotate, they never block. A check earns promotion to blocking
only by being bite-tested (see _tests/test_advisory.py) and surviving real use.

First three checks are distilled from RECORDED prose rules (G5, north-star mock;
"the fluff bites" — 2026-07-02):

  A. all-caps labels — house rule (test brief v2 §4: "avoid ALL-CAPS labels — overrides
     any styling convention that wants caps"). Flags text-transform:uppercase in CSS and
     multi-word ALL-CAPS runs in visible text.
     ★ PROMOTED to blocking 2026-07-02 (Dave ruling; type26-019 brand-source-backed;
     bite-tested) — now check 4 of _validate_snippets.py for gated snippets. The signal
     HERE stays live as the wider sweep over non-gated surfaces (_fitness-test screens).
  B. placeholder-as-label — recorded anti-pattern (text-input meta): an <input> carrying
     a placeholder with no matching <label for=…>.
  C. unmasked number runs — safety pattern (charter §2: masked sort/account numbers).
     Flags 8+ consecutive digits or a XX-XX-XX sort-code shape in visible text.

Sweep-batch additions (Dave ruling 2026-07-03 — these four RULED ADVISORY; their
exact-match siblings nam-001/avd-006-prefix/aca-004 went straight to blocking as
snippet-gate check 7):

  D. all-caps NAMES (nam-002) — a lone ALL-CAPS word ≥4 chars outside the acronym
     allowlist reads as a shouted product name ("CONNECTED MONEY" class). Names take
     Title Case. Single-word complement to check A's multi-word runs; needs a curated
     allowlist = judgment, hence advisory.
  E. directional phrases (aca-007, SC 1.3.3) — "button on the right" class; AT reflows
     location, so left/right instructions break. "above"/"below" acceptable per source.
     False-positive-prone by the source's own note, hence advisory.
  F. adjacent duplicate links (aca-005, SC 1.1.1 + 2.4.4) — adjacent <a> tags sharing
     one href combine into a single actionable element. Canon Cards already enact this;
     demo href="#" exempt.
  G. role-suffix accessible names (avd-006 suffix half) — aria-label ending
     "… button"/"… link" announces the element type AT already announces. NOT promoted
     with the prefix half: 4 live canon signals at ruling time (Cards "Example link");
     fix at the Cards revisit, then promote.

Scans <root>/snippets/*.reference.html and <root>/_fitness-test/*.canon.html.
Writes <root>/_ADVISORY-SIGNALS.md. ALWAYS exits 0 — advisory annotates, never blocks.

Usage: python3 _validate_advisory.py [--root DIR]   (--root exists for bite-tests)
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if "--root" in sys.argv:
    ROOT = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])

CAPS_CSS = re.compile(r'text-transform\s*:\s*uppercase', re.I)
CAPS_TEXT = re.compile(r'\b[A-Z]{2,}(?: [A-Z]{2,})+\b')
DIGIT_RUN = re.compile(r'\d{8,}')
SORT_CODE = re.compile(r'\b\d{2}[-–]\d{2}[-–]\d{2}\b')
INPUT_TAG = re.compile(r'<input\b[^>]*>', re.I)

# D — nam-002. Local mirror of the snippet gate's ACRONYMS (importing
# _validate_snippets executes the gate) + UK-gov/banking additions with live
# canon use (PAYE/HMRC swept clean 2026-07-03).
NAME_CAPS = re.compile(r'\b[A-Z]{4,}\b')
ACRONYMS = {
    "HSBC", "ARIA", "WCAG", "IBAN", "PAYE", "HMRC", "SEPA", "SWIFT",
    "CHAPS", "BACS", "HTML", "JSON",
}
# E — aca-007 (SC 1.3.3): sensory/directional location phrases.
DIRECTIONAL = re.compile(
    r'\b(?:on the (?:right|left)\b|(?:right|left)[- ]hand side\b'
    r'|to the (?:right|left) of\b|in the (?:top|bottom) (?:right|left)\b)', re.I)
# F — aca-005: adjacent <a> pair sharing an href (whitespace-only gap).
ADJ_LINKS = re.compile(
    r'<a\b[^>]*href="([^"]+)"[^>]*>.*?</a>\s*<a\b[^>]*href="([^"]+)"', re.S | re.I)
# G — avd-006 suffix half: role words in accessible names.
ROLE_SUFFIX = re.compile(r'\baria-label\s*=\s*"([^"]*\b(?:button|link))"', re.I)


def visible_text(html):
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S | re.I)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', t)


def check(path):
    html = open(path).read()
    name = os.path.basename(path)
    text = visible_text(html)
    signals = []

    # A — all-caps labels (house rule)
    for m in CAPS_CSS.finditer(html):
        signals.append(("all-caps", "text-transform:uppercase in CSS — house rule: no all-caps labels"))
    for m in set(CAPS_TEXT.findall(text)):
        signals.append(("all-caps", f'ALL-CAPS text run "{m}" — house rule: no all-caps labels'))

    # B — placeholder-as-label (recorded anti-pattern: placeholder as the ONLY accessible
    #     name). aria-label / aria-labelledby count as a name, so they don't signal.
    for tag in INPUT_TAG.findall(html):
        if re.search(r'\bplaceholder\s*=', tag, re.I):
            if re.search(r'\baria-label(ledby)?\s*=', tag, re.I):
                continue
            idm = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', tag)
            has_label = bool(idm) and bool(
                re.search(r'<label\b[^>]*\bfor\s*=\s*["\']%s["\']' % re.escape(idm.group(1)), html, re.I))
            if not has_label:
                signals.append(("placeholder-as-label", f"input with placeholder and no accessible name: {tag[:60]}…"))

    # C — unmasked number runs (safety pattern)
    for m in set(DIGIT_RUN.findall(text)):
        signals.append(("unmasked-digits", f'digit run "{m}" — account refs last-4 only, sort codes fully masked'))
    for m in set(SORT_CODE.findall(text)):
        signals.append(("unmasked-digits", f'sort-code shape "{m}" — sort codes are fully masked'))

    # D — all-caps names (nam-002, advisory 2026-07-03)
    for m in sorted(set(NAME_CAPS.findall(text)) - ACRONYMS):
        signals.append(("caps-name", f'ALL-CAPS word "{m}" — names take Title Case, caps are for acronyms (nam-002)'))

    # E — directional phrases (aca-007, advisory 2026-07-03)
    for m in sorted(set(DIRECTIONAL.findall(text))):
        signals.append(("directional", f'sensory instruction "{m}" — AT reflows location; name the control instead (aca-007)'))

    # F — adjacent duplicate links (aca-005, advisory 2026-07-03; demo "#" exempt)
    for m in ADJ_LINKS.finditer(html):
        if m.group(1) == m.group(2) and m.group(1) != "#":
            signals.append(("adjacent-links", f'adjacent links share href "{m.group(1)}" — combine into ONE actionable element (aca-005)'))

    # G — role-suffix accessible names (avd-006 suffix half, advisory 2026-07-03)
    for m in sorted(set(ROLE_SUFFIX.findall(html))):
        signals.append(("role-suffix", f'aria-label "{m}" announces the element type — AT announces the role itself (avd-006)'))

    return name, signals


def main():
    targets = sorted(glob.glob(os.path.join(ROOT, "snippets", "*.reference.html"))) + \
              sorted(glob.glob(os.path.join(ROOT, "_fitness-test", "*.canon.html")))
    rows = [check(p) for p in targets]
    total = sum(len(s) for _, s in rows)

    lines = ["# Advisory signals — prose rules (ADVISORY, non-gating)", "",
             "*Auto-generated by `_validate_advisory.py`. Checks distilled from recorded prose rules "
             "(house rules, anti-patterns, safety patterns). Signals annotate — they never block. "
             "Promotion to blocking requires bite-tests + a Dave ruling (ADR-0005 §5).*", "",
             f"**{len(rows)} file(s) scanned · {total} signal(s).**", ""]
    for name, signals in rows:
        if signals:
            lines.append(f"## {name} — {len(signals)} signal(s)")
            lines += [f"- **{kind}** — {msg}" for kind, msg in signals]
            lines.append("")
    if total == 0:
        lines.append("_No signals._")
    open(os.path.join(ROOT, "_ADVISORY-SIGNALS.md"), "w").write("\n".join(lines) + "\n")

    print(f"advisory signals: {len(rows)} file(s), {total} signal(s) — see _ADVISORY-SIGNALS.md (non-gating)")
    sys.exit(0)  # advisory: never blocks


if __name__ == "__main__":
    main()
