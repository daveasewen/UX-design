# #305 C1 - the token now lives behind the repo's credential helper (call 30, s305-D31), not in the remote URL.
# Read it through `git credential fill`; never print it.
import subprocess, re
def token_and_repo():
    url = subprocess.run(['git', 'config', 'remote.origin.url'], capture_output=True, text=True).stdout.strip()
    repo = re.search(r'github\.com/([^/]+/[^/.]+)', url).group(1)
    out = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n\n',
                         capture_output=True, text=True, env={'GIT_TERMINAL_PROMPT': '0', 'PATH': '/usr/bin:/bin:/usr/local/bin'}).stdout
    d = dict(l.split('=', 1) for l in out.splitlines() if '=' in l)
    return d.get('password'), repo
