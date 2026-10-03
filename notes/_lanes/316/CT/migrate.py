"""#316 CT: strip the hand-written click-or-Tab copies from member snippets and add the
AUTO-BEHAVIOUR click-or-tab marker pair before </body> (the generator fills it)."""
import json, re, sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
reg = json.load(open(os.path.join(ROOT, 'knowledge/component-types.json')))
members = list(reg['component-type']['click-or-tab']['$members'])
PAIR = ("  <!-- ===== AUTO-BEHAVIOUR click-or-tab START (click-or-tab) ===== -->\n"
        "  <!-- ===== AUTO-BEHAVIOUR click-or-tab END ===== -->\n")
COMMENT = r'(?:[ \t]*//[^\n]*(?:input-modality|keyboard ring|marks the input|pointer"\] rule)[^\n]*\n)*'
L = lambda s: r"[ \t]*addEventListener\('" + s + r"'[^\n]*\n"
BLOCK = re.compile(COMMENT + r"[ \t]*\{ const root = document\.documentElement;\n" + L('keydown') + L('mousedown')
                   + r"[ \t]*addEventListener\('touchstart'[^\n]*\}[ \t]*\n")
PLAIN = re.compile(COMMENT + r"[ \t]*const root = document\.documentElement;\n" + L('keydown') + L('mousedown') + L('touchstart'))
for m in members:
    p = os.path.join(ROOT, 'knowledge/snippets', m + '.reference.html'); t = open(p).read(); o = t
    t, n1 = BLOCK.subn('', t); t, n2 = PLAIN.subn('', t)
    t, n3 = re.subn(r"[ \t]*<script>\s*</script>[ \t]*\n", '', t)   # a script left empty
    if 'AUTO-BEHAVIOUR click-or-tab START' not in t:
        assert t.count('</body>') == 1, m
        t = t.replace('</body>', PAIR + '</body>', 1)
    left = re.findall(r'dataset\.modality', t)
    print(f"{m:28} block={n1} plain={n2} emptied-script={n3} leftover-setters={len(left)}")
    if '--write' in sys.argv and t != o: open(p, 'w').write(t)
