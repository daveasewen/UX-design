# #305 C1 (copied from #304 C6 ci304.py; token via the credential helper, _ghtok.py) - CI read-back for a sha.
import json, urllib.request, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ghtok import token_and_repo
sha = sys.argv[1]
tok, repo = token_and_repo()
def api(p):
    r = urllib.request.Request("https://api.github.com/repos/%s%s" % (repo, p))
    if tok: r.add_header('Authorization', 'Bearer ' + tok)
    r.add_header('Accept', 'application/vnd.github+json')
    return json.load(urllib.request.urlopen(r, timeout=25))
d = api("/actions/runs?per_page=10")
runs = [r for r in d['workflow_runs'] if r['head_sha'].startswith(sha)]
if not runs: print("NO RUN YET on", sha); sys.exit(0)
for r in runs:
    print("RUN", r['id'], r['name'], r['status'], r['conclusion'], r['created_at'])
    j = api("/actions/runs/%d/jobs" % r['id'])
    for job in j['jobs']:
        fails = ['%s:%s' % (s['number'], s['name'][:70]) for s in job['steps'] if s['conclusion'] == 'failure']
        print("   job", job["id"], job["name"], job['status'], job['conclusion'], job.get('completed_at'), "| failing:", fails)
