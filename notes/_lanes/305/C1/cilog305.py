# #305 C1 (copied from #304 C6 cilog304.py; token via the credential helper, _ghtok.py).
import urllib.request, urllib.error, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ghtok import token_and_repo
tok, repo = token_and_repo()
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op=urllib.request.build_opener(NoRedir)
r=urllib.request.Request("https://api.github.com/repos/%s/actions/jobs/%s/logs"%(repo,sys.argv[1]))
if tok: r.add_header('Authorization','Bearer '+tok)
try:
    resp=op.open(r,timeout=40); raw=resp.read()
except urllib.error.HTTPError as e:
    loc=e.headers.get('Location'); raw=urllib.request.urlopen(loc,timeout=60).read()
raw=raw.decode('utf-8','replace')
open(sys.argv[2],'w').write(raw)
for ln in raw.split('\n'):
    s=ln.strip()
    if 'SURVEY:' in s or 'help-gate:' in s: print(s[-220:])
    if re.search(r'\[\d+\]', s) and ('✗' in s or '❌' in s or 'FAIL' in s[:120]): print('  ',s[-200:])
