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

Cost-0 harvest (Dave ruling 2026-07-03 — all eight advisory-first per ADR-0005 §5):

  H. skip-link (acd-003, SC 2.4.1) — composed screens (*.canon.html) only: a full page
     with no skip-to-content link. ALL 5 screens signal at wiring time — real gap.
  I. <html lang> keep-true (acd-007, SC 3.1.1) — every file; swept clean at wiring.
  J. pinch-zoom never disabled (acd-010, SC 1.4.10) — user-scalable=no / maximum-scale=1
     in the viewport meta.
  K. no activation on down-events (acd-016, SC 2.5.2) — inline on(mouse|pointer|touch)-
     down/start attributes, or down-listeners whose one-liner body navigates/submits/
     clicks. Calibrated at wiring: input-modality listeners (set a dataset flag) and
     Reorder's drag pointerdown (drag ≠ activation) do NOT match — by design.
  L. no submit/navigation on change (acd-019, SC 3.2.2) — onchange/change listeners
     containing submit()/location/.href/window.open. UI-preference change handlers
     (List-items density, Selection-controls indeterminate) don't match — by design.
  M. aria-required on required fields (acd-024, SC 3.3.2) — required without
     aria-required. 0 signals at wiring (canon declares no required fields yet).
  N. inputmode/autocomplete on typed inputs (acd-025, SC 1.3.5) — email/tel/number
     inputs carrying neither. FIRES on canon email inputs at wiring time — evidence
     banked for the Input-fields supercharge.
  O. no paste-blocking (aid-020) — onpaste="return false"/preventDefault or paste
     listeners that preventDefault.

Scans <root>/snippets/*.reference.html and <root>/_fitness-test/*.canon.html.
Writes <root>/_ADVISORY-SIGNALS.md. ALWAYS exits 0 — advisory annotates, never blocks.

Usage: python3 _validate_advisory.py [--root DIR]   (--root exists for bite-tests)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
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
# H — acd-003: skip-to-content link (screens only).
SKIP_LINK = re.compile(r'<a\b[^>]*href="#[^"]*"[^>]*>[^<]*\bskip\b', re.I)
# I — acd-007: page language declared.
HTML_LANG = re.compile(r'<html\b[^>]*\blang\s*=', re.I)
# J — acd-010: pinch-zoom disabled.
VIEWPORT_BAD = re.compile(
    r'<meta\b[^>]*name\s*=\s*"viewport"[^>]*content\s*=\s*"[^"]*'
    r'(user-scalable\s*=\s*(?:no|0)|maximum-scale\s*=\s*1(?:\.0*)?(?![.\d]))', re.I)
# K — acd-016: activation on down-events (inline attrs always; listeners only when
#     the one-liner body navigates/submits/clicks — modality + drag listeners exempt).
DOWN_ATTR = re.compile(r'\bon(?:mousedown|pointerdown|touchstart)\s*=', re.I)
DOWN_LISTENER = re.compile(
    r"addEventListener\(\s*['\"](?:mousedown|pointerdown|touchstart)['\"]"
    r"[^\n]*(?:location|\.submit\(|\.click\(|\.href\s*=)", re.I)
# L — acd-019: submit/navigation inside change handlers.
CHANGE_ATTR = re.compile(r'\bonchange\s*=\s*"[^"]*(?:submit|location|\.href|window\.open)', re.I)
CHANGE_LISTENER = re.compile(
    r"addEventListener\(\s*['\"]change['\"][^\n]*(?:location|\.submit\(|\.href\s*=|window\.open)", re.I)
# M — acd-024: required fields carry aria-required.
FIELD_TAG = re.compile(r'<(?:input|select|textarea)\b[^>]*>', re.I)
# N — acd-025: typed inputs carry inputmode/autocomplete.
TYPED_INPUT = re.compile(r'<input\b[^>]*\btype\s*=\s*"(?:email|tel|number)"[^>]*>', re.I)
# O — aid-020: paste-blocking.
PASTE_ATTR = re.compile(r'\bonpaste\s*=\s*"[^"]*(?:return\s+false|preventDefault)', re.I)
PASTE_LISTENER = re.compile(r"addEventListener\(\s*['\"]paste['\"][^\n]*preventDefault", re.I)


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
    for m in sorted(set(CAPS_TEXT.findall(text))):  # sorted: deterministic report order (dream-pass v2 P2, 2026-07-26)
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
    for m in sorted(set(DIGIT_RUN.findall(text))):  # sorted: deterministic (P2)
        signals.append(("unmasked-digits", f'digit run "{m}" — account refs last-4 only, sort codes fully masked'))
    for m in sorted(set(SORT_CODE.findall(text))):  # sorted: deterministic (P2)
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

    # ---- cost-0 harvest, checks H–O (Dave ruling 2026-07-03) ----
    screen = "_fitness-test" in path

    # H — skip link on composed screens (acd-003)
    if screen and not SKIP_LINK.search(html):
        signals.append(("skip-link", "composed screen has no skip-to-content link (acd-003, 2.4.1)"))

    # I — <html lang> keep-true (acd-007)
    if not HTML_LANG.search(html):
        signals.append(("html-lang", "<html> carries no lang attribute (acd-007, 3.1.1)"))

    # J — pinch-zoom never disabled (acd-010)
    m = VIEWPORT_BAD.search(html)
    if m:
        signals.append(("pinch-zoom", f'viewport meta disables zoom via "{m.group(1)}" — never disable pinch-to-zoom (acd-010, 1.4.10)'))

    # K — no activation on down-events (acd-016)
    for m in sorted(set(DOWN_ATTR.findall(html))):
        signals.append(("down-event", "inline down-event handler attribute — activation belongs on the up-event (acd-016, 2.5.2)"))
    for m in DOWN_LISTENER.finditer(html):
        signals.append(("down-event", "down-event listener navigates/submits/clicks — activation belongs on the up-event (acd-016, 2.5.2)"))

    # L — no submit/navigation on change (acd-019)
    if CHANGE_ATTR.search(html) or CHANGE_LISTENER.search(html):
        signals.append(("onchange-nav", "change handler submits/navigates — context shifts only on user request (acd-019, 3.2.2)"))

    # M — aria-required on required fields (acd-024)
    for tag in FIELD_TAG.findall(html):
        if re.search(r'(?<![-\w])required\b', tag, re.I) and not re.search(r'aria-required', tag, re.I):
            signals.append(("aria-required", f"required field without aria-required: {tag[:60]}… (acd-024, 3.3.2)"))

    # N — inputmode/autocomplete on typed inputs (acd-025)
    for tag in TYPED_INPUT.findall(html):
        if not re.search(r'\b(?:inputmode|autocomplete)\s*=', tag, re.I):
            signals.append(("input-hints", f"typed input with neither inputmode nor autocomplete: {tag[:60]}… (acd-025, 1.3.5)"))

    # O — no paste-blocking (aid-020)
    if PASTE_ATTR.search(html) or PASTE_LISTENER.search(html):
        signals.append(("paste-block", "paste is blocked — never disable paste (aid-020)"))

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
