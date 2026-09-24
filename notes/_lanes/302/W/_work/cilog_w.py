# #302 wrap seat, copied from #301 W's cilog_w.py; output path parametrised.
import subprocess, urllib.request, re, sys
url=subprocess.run(['git','config','remote.origin.url'],capture_output=True,text=True).stdout.strip()
m=re.search(r'//(?:([^@/]+)@)?github\.com/([^/]+/[^/.]+)', url)
tok=m.group(1); repo=m.group(2)
if tok and ':' in tok: tok=tok.split(':')[-1]
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
