#!/usr/bin/env python3
"""#304 W5a planted test — _validate_screen.gate_icons reads MARKUP only.
usage: python3 test_icons_markup.py <knowledge-dir>   (exit 0 = all arms as expected)"""
import sys, os, importlib
K = os.path.abspath(sys.argv[1]); sys.path.insert(0, K); os.chdir(K)
S = importlib.import_module("_validate_screen")
lib = sorted(S.icons.build_library())
good_d = next(iter(lib))
ENGINE = ("<script>\n/* everything inside the <svg> and everything else */\n"
          "if (!svg) { bad('figure has no <svg class=\"dv-fit\"> canvas'); }\n"
          "var p=[]; g.innerHTML = '<path d=\"M' + p.join(' L') + ' Z\"/>';\n</script>\n")
REAL = '<svg class="ic" viewBox="0 0 24 24"><path d="%s"/></svg>' % good_d
BAD = '<svg class="ic" viewBox="0 0 24 24"><path d="M1 1 L9 9 Z"/></svg>'
arms = [
  ("P1 engine source mentioning <svg, then a LIBRARY icon in markup -> clean", ENGINE + REAL, 0),
  ("P2 engine source then an INVENTED icon in markup -> still caught (1)", ENGINE + BAD, 1),
  ("P3 invented icon in markup, no script -> caught (1)", BAD, 1),
  ("P4 invented icon only inside a script string -> not markup, not read", "<script>x='%s'</script>" % BAD, 0),
  ("P5 commented-out <script> does not blank the markup after it", "<!-- <script> -->" + BAD + "<script>1</script>", 1),
  ("P6 data-bespoke still skipped", BAD.replace('class="ic"', 'class="ic" data-bespoke'), 0),
]
ok = True
for label, html, want in arms:
    got = len(S.gate_icons("<html><body>%s</body></html>" % html))
    good = got == want; ok &= good
    print(("  ok " if good else "  XX ") + label + " -> %d finding(s)" % got)
# mutation: the pre-W5a reading (raw html) must FAIL P1
raw = [len(S.icons.DRE.findall(b)) and [d for d in S.icons.DRE.findall(b) if S.icons.norm(d) not in S.icons.build_library()]
       for b in S.icons.SVGRE.findall(ENGINE + REAL)]
bit = any(raw)
print(("  ok " if bit else "  XX ") + "M1 the raw-html reading (pre-W5a) reds on P1: %s" % bit); ok &= bit
print("ICON-MARKUP TEST: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
