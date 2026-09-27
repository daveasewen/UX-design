import json, os, sys, hashlib
V = sys.argv[1]; R = os.path.expanduser('~/w4a/runs-' + V); ST = os.path.expanduser('~/w4a/st/' + V)
SRC = os.path.expanduser('~/mnt/Projects--UX-design/notes/_lanes/304/W4b/runs')
for rid in sorted(os.listdir(ST)):
    m = json.load(open(os.path.join(SRC, rid, 'meta.json')))
    d = os.path.join(R, rid); os.makedirs(d, exist_ok=True)
    m['entry'] = os.path.join(ST, rid, 'out', 'index.html'); m['stage'] = os.path.join(ST, rid)
    m['pack_root_staged'] = os.path.join(ST, rid, 'pack'); m['page_sha256'] = hashlib.sha256(open(m['entry'], 'rb').read()).hexdigest()
    m['label'] = m['label'] + ' (' + V + ')'
    json.dump(m, open(os.path.join(d, 'meta.json'), 'w'), indent=1)
print('ok', R)
