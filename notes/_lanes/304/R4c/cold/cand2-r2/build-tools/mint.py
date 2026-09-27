"""Mint each page's provenance receipt with the pack's own generator, then align each region's
`script` with its meta's typed behaviour address (the meta is the one home, s234-D5). The pack's
mint takes the FIRST AUTO-BEHAVIOUR block in a chart snippet (dv-behaviour) while its own gate
demands the meta's address (dv-render) — a mint/gate disagreement found in this run, corrected
here by reading the meta, never by typing an address."""
import json, os, re, subprocess, sys
W = os.path.abspath(sys.argv[1]); PACK = os.path.join(W, 'pack'); K = os.path.join(PACK, 'knowledge')
sys.path.insert(0, K)
import _validate_receipt as VR
for f in sys.argv[2:]:
    p = os.path.abspath(f)
    r = subprocess.run([sys.executable, 'knowledge/gen_provenance_receipt.py', '--mint', p], cwd=PACK, capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    html = open(p, encoding='utf-8').read()
    rec, err = VR.parse_receipt(html)
    fixed = 0
    for reg in rec['regions']:
        if reg.get('kind') != 'markup' or not reg.get('snippet'):
            continue
        mp = VR.meta_path_for(reg['snippet'])
        meta = VR.load_meta(mp) if mp else None
        typed = VR.typed_behaviour(meta) if meta else None
        if isinstance(typed, dict) and typed.get('script') and reg.get('script') and reg['script'] != typed['script']:
            reg['script'] = typed['script']; fixed += 1
    rec['pack'] = '1.0.14'
    block = '<script type="application/json" id="%s">\n%s\n</script>' % (VR.RECEIPT_ID, json.dumps(rec, indent=1))
    html = VR.RECEIPT_RE.sub(lambda m: block, html, count=1)
    open(p, 'w', encoding='utf-8').write(html)
    print('  aligned %d chart region script(s) with their metas' % fixed)
