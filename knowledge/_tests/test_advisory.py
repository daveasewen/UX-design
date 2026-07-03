#!/usr/bin/env python3
"""
test_advisory.py — bite-tests for the advisory signals (ADR-0005 §5 entry toll).

Advisory checks never fail a build, so their failure mode is silence: a check that
stops matching is indistinguishable from a clean canon. Same blind-spot class the
gate self-tests exist for (test_gates.py), applied to the advisory tier. Each case
feeds _validate_advisory.py a deliberately-broken fixture and asserts the expected
marker appears in the report; a control fixture asserts a clean file stays silent.

An advisory check may only be PROMOTED to blocking if its cases here bite.

Run:  python3 knowledge/_tests/test_advisory.py   (exits non-zero on any failure)
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(os.path.dirname(HERE), "_validate_advisory.py")

CLEAN = """<!DOCTYPE html><html lang="en-GB"><head><style>
.label{font-size:12px;letter-spacing:.1em}</style></head><body>
<label for="ni">National Insurance number</label>
<input id="ni" type="text">
<p>Account ···· 8842 · sort ··–··–··</p>
</body></html>"""

# (name, fixture_html, expected_marker, as_screen)
CASES = [
    ("caps-css", CLEAN.replace(".label{", ".label{text-transform:uppercase;"), "all-caps", False),
    ("caps-text", CLEAN.replace("<p>Account", "<p>AWAITING APPROVAL NOW</p><p>Account"), "all-caps", False),
    ("placeholder", CLEAN.replace('<input id="ni" type="text">',
                                  '<input id="po" type="text" placeholder="Enter your number">'),
     "placeholder-as-label", False),
    ("digits", CLEAN.replace("···· 8842", "12345678842"), "unmasked-digits", False),
    ("sortcode", CLEAN.replace("··–··–··", "12-34-56"), "unmasked-digits", False),
    # sweep-batch additions (Dave ruling 2026-07-03) — checks D/E/F/G
    ("caps-name", CLEAN.replace("<p>Account", "<p>Try INVESTNOW today</p><p>Account"), "caps-name", False),
    ("directional", CLEAN.replace("<p>Account", "<p>Use the button on the right</p><p>Account"), "directional", False),
    ("adjacent-links", CLEAN.replace("<p>Account",
                                     '<a href="/pay">icon</a> <a href="/pay">Payments</a><p>Account'),
     "adjacent-links", False),
    ("role-suffix", CLEAN.replace("<p>Account",
                                  '<a href="/x" aria-label="Example link">x</a><p>Account'),
     "role-suffix", False),
    # cost-0 harvest (Dave ruling 2026-07-03) — checks H–O
    ("skip-link", CLEAN, "skip-link", True),  # a screen with NO skip link bites
    ("skip-link-ok", CLEAN.replace("<body>", '<body><a href="#main">Skip to content</a>'),
     "0 signal(s)", True),  # …and one WITH stays silent
    ("html-lang", CLEAN.replace('<html lang="en-GB">', "<html>"), "html-lang", False),
    ("pinch-zoom", CLEAN.replace("<head>",
                                 '<head><meta name="viewport" content="width=device-width, user-scalable=no">'),
     "pinch-zoom", False),
    ("down-event", CLEAN.replace("<p>Account", '<button onmousedown="pay()">Pay now</button><p>Account'),
     "down-event", False),
    ("onchange-nav", CLEAN.replace("<p>Account",
                                   '<select onchange="location.href=this.value"><option>Go</option></select><p>Account'),
     "onchange-nav", False),
    ("aria-required", CLEAN.replace('<input id="ni" type="text">', '<input id="ni" type="text" required>'),
     "aria-required", False),
    ("input-hints", CLEAN.replace('<input id="ni" type="text">', '<input id="ni" type="email">'),
     "input-hints", False),
    ("paste-block", CLEAN.replace('<input id="ni" type="text">',
                                  '<input id="ni" type="text" onpaste="return false">'),
     "paste-block", False),
]

failures = []


def run_on(fixture_html, as_screen=False):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "snippets"))
    os.makedirs(os.path.join(d, "_fitness-test"))
    if as_screen:
        open(os.path.join(d, "_fitness-test", "Fixture.canon.html"), "w").write(fixture_html)
    else:
        open(os.path.join(d, "snippets", "Fixture.reference.html"), "w").write(fixture_html)
    r = subprocess.run([sys.executable, VALIDATOR, "--root", d], capture_output=True, text=True)
    report = open(os.path.join(d, "_ADVISORY-SIGNALS.md")).read()
    return r, report


# control — clean fixture must stay silent
r, report = run_on(CLEAN)
if "0 signal(s)" not in report:
    failures.append(f"CONTROL: clean fixture produced signals:\n{report}")
if r.returncode != 0:
    failures.append("CONTROL: advisory validator must always exit 0")

# bites
for name, html, marker, as_screen in CASES:
    r, report = run_on(html, as_screen)
    if marker not in report:
        failures.append(f"{name}: expected marker '{marker}' missing from report")
    if r.returncode != 0:
        failures.append(f"{name}: advisory validator must always exit 0 (advisory annotates, never blocks)")

n = 1 + len(CASES)
if failures:
    print(f"advisory bite-tests: {n} case(s), {len(failures)} FAILURE(S)")
    for f in failures:
        print("  ❌ " + f)
    sys.exit(1)
print(f"advisory bite-tests: {n} case(s), all bite ✅ (and none block — exit 0 throughout)")
