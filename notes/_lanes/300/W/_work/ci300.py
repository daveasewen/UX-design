# #300 wrap seat (copied from #299 W) - CI read-back for a sha (the #296 5b seat's method, knowledge/_tmp/ci296.py, parametrised).
import subprocess, json, urllib.request, re, sys
sha = sys.argv[1]
url = subprocess.run(['git', 'config', 'remote.origin.url'], capture_output=True, text=True).stdout.strip()
m = re.search(r'//(?:([^@/]+)@)?github\.com/([^/]+/[^/.]+)', url)
tok = m.group(1); repo = m.group(2)
if tok and ':' in tok: tok = tok.split(':')[-1]
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
