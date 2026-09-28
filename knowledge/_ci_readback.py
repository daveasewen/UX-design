#!/usr/bin/env python3
"""_ci_readback.py — the CI read-back for one commit, as a SHORT run summary. Never the raw log.

Built #306 lane V for `s306-D7` (Dave, 2026-09-28 16:01 BST, call 4 of the wrap-redesign page:
"a · Yes, the next opener reads the follow-up's CI") and limit 8 of `s306-D10` ("The opener's CI
read prints the run summary (the 301-byte form), never the gates log"). It is PHASE 2 of the wrap
redesign's build order, and the one permanent tool that phase needed.

WHAT IT REPLACES. Every wrap from #303 to #305 re-authored the same two scripts, "modelled on" the
last wrap's (`notes/_lanes/305/C1/ci305.py`, `cilog305.py`, and `_ghtok.py` beside them). This is
their permanent form: one file, self-tested, in `knowledge/`.

CONSUMERS (named, so it is not an instrument without one):
  1. The wrap seat, at ritual step 5, for the WRAP commit's CI — the one wait the wrap keeps
     (`knowledge/_RUNBOOK-capture-ritual.md` § 5, as amended by `s306-D7`).
  2. The NEXT session's opener, for the 5b follow-up commit's CI, which the wrap no longer waits
     on: the handoff's post-wrap addendum carries a `CI owed:` line naming this tool, and
     `_capture_gate.py::ci_owed_check` refuses a 5b addendum that omits it.

WHAT IT PRINTS, per run on the sha: the run id, workflow, status and conclusion; per job its
status, conclusion and the names of its failing steps; and ONLY FOR A FAILED JOB, the blocking
lines parsed out of that job's log (at most MAX_LINES_PER_STEP per failing step, each cut to
LINE_CAP chars, timestamps stripped). The gates log runs to ~510,000 bytes (#305 W); it is fetched
only on red, parsed in memory, and never printed or written unless `--save-log` names a file.

THE TOKEN comes from the repo's credential helper (`git credential fill`, `s305-D30`) and is NEVER
printed, logged or sent anywhere but api.github.com: the job-log endpoint answers with a redirect
to blob storage, and that redirect is fetched WITHOUT the Authorization header. Bitten below.

EXIT CODES: 0 every run completed and green · 1 a run or job concluded red · 2 still running or
queued · 3 no run on that sha yet · 5 the API could not be reached (the error class is printed,
never a header).

Usage:
  python3 knowledge/_ci_readback.py --sha <sha-or-ref>     # one read, summary only
  python3 knowledge/_ci_readback.py --owed                 # the sha the newest handoff owes:
                                                           # the last commit touching it
  python3 knowledge/_ci_readback.py --sha <sha> --poll 170 # re-read until done, within one call
  python3 knowledge/_ci_readback.py --selftest             # canned API JSON, no network
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
API = "https://api.github.com"
MAX_LINES_PER_STEP = 12
LINE_CAP = 220
_TS = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ?")
_HANDOFF_RE = re.compile(r"_HANDOFF-(\d+)\b")


# ── the token and the repo slug ─────────────────────────────────────────────────────────────────
def repo_slug(root=ROOT):
    url = subprocess.run(["git", "config", "remote.origin.url"], capture_output=True, text=True,
                         cwd=root).stdout.strip()
    m = re.search(r"github\.com[/:]([^/]+/[^/]+?)(?:\.git)?/?$", url)
    return m.group(1) if m else None


def token(root=ROOT):
    """The credential helper's password for github.com, or None. NEVER printed."""
    env = {"GIT_TERMINAL_PROMPT": "0", "PATH": os.environ.get("PATH", "/usr/bin:/bin:/usr/local/bin")}
    if os.environ.get("HOME"):
        env["HOME"] = os.environ["HOME"]
    try:
        out = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                             capture_output=True, text=True, env=env, cwd=root, timeout=15).stdout
    except (OSError, subprocess.TimeoutExpired):
        return None
    d = dict(ln.split("=", 1) for ln in out.splitlines() if "=" in ln)
    return d.get("password") or None


# ── transport: the one place a request is made; the selftest swaps it for a fake ────────────────
def http_get(url, headers):
    """GET without following redirects. Returns (status, headers dict, body bytes)."""
    class _NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        resp = urllib.request.build_opener(_NoRedir).open(req, timeout=60)
        return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), b""


class Client:
    def __init__(self, slug, tok, get=http_get):
        self.slug, self._tok, self._get = slug, tok, get

    def _auth(self):
        h = {"Accept": "application/vnd.github+json", "User-Agent": "apollo-ci-readback"}
        if self._tok:
            h["Authorization"] = "Bearer " + self._tok
        return h

    def api(self, path):
        st, _, body = self._get(f"{API}/repos/{self.slug}{path}", self._auth())
        if st != 200:
            raise RuntimeError(f"GitHub API answered HTTP {st} for {path.split('?')[0]}")
        return json.loads(body.decode("utf-8"))

    def job_log(self, job_id):
        """The job log, in memory. The redirect target is fetched WITHOUT the token."""
        st, hdrs, body = self._get(f"{API}/repos/{self.slug}/actions/jobs/{job_id}/logs", self._auth())
        if st in (301, 302, 303, 307, 308):
            loc = hdrs.get("Location") or hdrs.get("location")
            if not loc:
                raise RuntimeError(f"job {job_id} log: redirect with no Location")
            st, _, body = self._get(loc, {"User-Agent": "apollo-ci-readback"})
        if st != 200:
            raise RuntimeError(f"job {job_id} log: HTTP {st}")
        return body.decode("utf-8", "replace")


# ── the log parser: the blocking lines of a failed job, never the log ───────────────────────────
def _clip(s):
    s = s.rstrip()
    return s if len(s) <= LINE_CAP else s[:LINE_CAP - 1] + "…"


def parse_failed_log(raw):
    """Return [(actions_step_title, [blocking lines])] for every Actions step that ended in
    `##[error]`. Blocking lines: the survey's `SURVEY:` summary and its `❌ [N]` rows; every
    UNINDENTED `❌` line, prefixed with the `=== [i/N] label` header it sits under (an INDENTED
    `❌ FAIL` is a selftest's planted fixture, not a verdict, and is skipped); an unindented
    `⛔ … FAIL` summary; and the `##[error]` line itself. A failed step with none of those
    gives its last three non-empty lines instead, so a red never prints as blank.
    ⛔ INSIDE A `_build_all.py` STEP (one that prints `=== [i/N]` headers) ONLY THE BUILD'S OWN
    VERDICT LINES COUNT: an unindented `❌` carrying `(exit N)` (every GATE remedy has the `{code}`
    slot, `_build_all.selftest` (a)), `❌ step … failed` and `❌ build gate failed`. In a CI log the
    children's output is INTERLEAVED with the build's buffered prints, so a child's own `❌`/`⛔`
    line lands under whichever header happens to precede it (#306 V, the first live read of
    dcb76d81: the evidence linter's `⛔ EVIDENCE GATE FAIL` printed under step [74]). The build's own
    lines keep their relative order, so a verdict line's header IS its step. A header block closed
    by `⚠ advisory step …` or `⊘ step … COULD-NOT-ASK` drops what it collected (belt and braces)."""
    steps, cur = [], None
    verdict = re.compile(r"^❌ (?:.*\(exit \d+\)|step '.*' failed|build gate failed)")
    for ln in raw.splitlines():
        s = _TS.sub("", ln)
        if s.startswith("##[group]Run "):
            cur = {"title": s[len("##[group]Run "):].strip(), "lines": [], "error": [], "hdr": None,
                   "tail": [], "build": False}
            steps.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"=== \[(\d+/\d+)\] (.+?)(?: — [^—]+)? ===$", s.strip())
        if m:
            cur["hdr"] = f"[{m.group(1)}] {m.group(2)}"
            cur["build"] = True
            continue
        if cur["hdr"] and (s.startswith("⚠ advisory step '") or
                           (s.startswith("⊘ step '") and "COULD-NOT-ASK" in s)):
            cur["lines"] = [x for x in cur["lines"] if x[0] != cur["hdr"]]
            continue
        if s.startswith("##[error]"):
            cur["error"].append(s)
            continue
        if s.strip():
            cur["tail"] = (cur["tail"] + [s.strip()])[-3:]
        h = cur["hdr"]
        if s.startswith("SURVEY:"):
            cur["lines"].append((None, s))
        elif re.match(r"^\s{1,4}❌ \[\s*\d+\]", s):
            cur["lines"].append((None, s.strip()))
        elif s.startswith("❌"):
            if s.startswith("❌ build gate failed"):
                cur["lines"].append((None, s))
            else:
                cur["lines"].append((h, f"{h} → {s}" if h else s))
        elif s.startswith("⛔") and "FAIL" in s:
            cur["lines"].append((h, f"{h} → {s}" if h else s))
    out = []
    for st in steps:
        if not st["error"]:
            continue
        if st["build"]:
            st["lines"] = [(h, x) for h, x in st["lines"]
                           if h is None or verdict.match(x.split(" → ", 1)[-1])]
        lines = [x for _, x in st["lines"]] or ["(no marked line; the step's last lines:)"] + st["tail"]
        lines = lines + st["error"][-1:]
        more = max(0, len(lines) - MAX_LINES_PER_STEP)
        lines = [_clip(x) for x in lines[:MAX_LINES_PER_STEP]]
        if more:
            lines.append(f"(+{more} more blocking line(s) not shown)")
        out.append((st["title"], lines))
    return out


# ── the read-back ───────────────────────────────────────────────────────────────────────────────
def resolve_sha(ref, root=ROOT):
    r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
                       capture_output=True, text=True, cwd=root)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def owed_sha(root=ROOT):
    """The sha the newest handoff owes: the last commit that touched `_HANDOFF-<max n>-*.md`.
    Returns (sha or None, handoff path or None)."""
    hs = [(int(_HANDOFF_RE.search(os.path.basename(p)).group(1)), p)
          for p in glob.glob(os.path.join(root, "_HANDOFF-*.md")) if _HANDOFF_RE.search(os.path.basename(p))]
    if not hs:
        return None, None
    path = max(hs)[1]
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", os.path.basename(path)],
                       capture_output=True, text=True, cwd=root)
    return (r.stdout.strip() or None), path


def readback(client, sha, out=print):
    """Print the summary for every run on `sha` (a full sha, or a prefix of ≥7). Return the rc."""
    full = len(sha) == 40
    q = f"?head_sha={sha}&per_page=20" if full else "?per_page=50"
    runs = [r for r in client.api(f"/actions/runs{q}").get("workflow_runs", [])
            if r.get("head_sha", "").startswith(sha)]
    if not runs:
        out(f"NO RUN YET on {sha[:12]} — none yet, or it was not the tip of its push (CI runs on a "
            f"push's tip only: read the tip that carried it). Read again later.")
        return 3
    rc = 0
    for r in sorted(runs, key=lambda x: x.get("id", 0)):
        out(f"RUN {r['id']} {r.get('name')} {r.get('status')}/{r.get('conclusion')} "
            f"{r.get('created_at')} sha {r.get('head_sha', '')[:8]}")
        jobs = client.api(f"/actions/runs/{r['id']}/jobs?per_page=50").get("jobs", [])
        for j in jobs:
            fails = [s.get("name", "")[:90] for s in j.get("steps") or [] if s.get("conclusion") == "failure"]
            out(f"   job {j.get('name')} {j.get('status')}/{j.get('conclusion')} {j.get('completed_at')}"
                + (f" | failing steps: {fails}" if fails else ""))
            if j.get("conclusion") == "failure":
                try:
                    parsed = parse_failed_log(client.job_log(j["id"]))
                except Exception as e:                                   # noqa: BLE001
                    out(f"      (log unreadable: {type(e).__name__}: {e})")
                    parsed = []
                for title, lines in parsed:
                    out(f"      ✗ {_clip(title)}")
                    for x in lines:
                        out(f"          {x}")
        concl = [r.get("conclusion")] + [j.get("conclusion") for j in jobs]
        if r.get("status") != "completed" or any(j.get("status") != "completed" for j in jobs):
            rc = max(rc, 2) if rc != 1 else 1
        if any(c in ("failure", "timed_out", "cancelled", "startup_failure") for c in concl if c):
            rc = 1
    verdict = {0: "GREEN — every run completed and passed", 1: "RED — see the failing steps above",
               2: "STILL RUNNING — read again later"}[rc]
    out(f"VERDICT {sha[:8]}: {verdict}")
    return rc


# ── selftest: canned API JSON through a fake transport; no network, no token ────────────────────
def _canned_log():
    ts = "2026-09-28T14:44:11.8486276Z "
    L = [ts + "##[group]Run actions/checkout@v6", ts + "fetching",
         ts + "##[group]Run python3 knowledge/_build_survey.py --timeout 60",
         ts + "  ✅ [87] KG token-group generator selftest — 8 bites (s277-D12)",
         ts + "  ❌ [88] KG node-title generator drift check — _node_titles.json vs the  exit 1",
         ts + "SURVEY: 68 pass · 1 FAIL · 6 COULD-NOT-ASK (self-declared refusals) · 0 unaskable",
         ts + "##[error]Process completed with exit code 1.",
         ts + "##[group]Run python3 knowledge/_build_all.py",
         ts + "=== [1/154] compliance knowledge graph — compliance/_build_compliance_kg.py ===",
         ts + "  ❌ FAIL GOOD-MORNING.md: PLANTED-FIXTURE-LINE, a selftest's own bite"]
    L += [ts + f"  ✅ [{i}] FILLER-STEP-{i} passes" for i in range(2, 20000)]
    L += [ts + "=== [141/154] claim-table evidence linter (advisory) — _validate_evidence.py ===",
          ts + "❌ ADVISORY-NOISE-LINE the manifest reads version 'v9' and NO zip carries it",
          ts + "⛔ EVIDENCE GATE FAIL — ADVISORY-NOISE 6 lint",
          ts + "=== [142/154] next step — x.py ===",
          ts + "❌ CHILD-INTERLEAVED-NOISE a child's own line with no exit slot"]
    L += [ts + "=== [143/154] advisory again — y.py ===",
          ts + "⚠ advisory step 'claim-table evidence linter (advisory)' reported findings (exit 1) — non-gating"]
    L += [ts + "=== [88/154] KG node-title generator drift check — gen_kg_titles.py ===", ts,
          ts + "❌ KG node titles are STALE (exit 1) — Run: python3 knowledge/gen_kg_titles.py --write",
          ts + "❌ build gate failed — see the reports above.",
          ts + "##[error]Process completed with exit code 1.",
          ts + "##[group]Run python3 knowledge/_tests/test_gates.py", ts + "ok"]
    return "\n".join(L) + "\n"


def selftest():
    import io
    SECRET = "ghp_SELFTEST_SECRET_never_printed"
    SHA_G, SHA_R, SHA_P = "a" * 40, "b" * 40, "c" * 40
    jobs_green = [{"id": 11, "name": n, "status": "completed", "conclusion": "success",
                   "completed_at": "T", "steps": [{"name": "s", "conclusion": "success"}]}
                  for n in ("release", "gates", "render")]
    jobs_red = [dict(jobs_green[0]),
                {"id": 22, "name": "gates", "status": "completed", "conclusion": "failure", "completed_at": "T",
                 "steps": [{"name": "Survey the COMMITTED tree", "conclusion": "failure"},
                           {"name": "Knowledge build — all derived views + blocking gates", "conclusion": "failure"}]},
                dict(jobs_green[2])]
    jobs_pend = [dict(jobs_green[0], status="in_progress", conclusion=None)]
    runs = {SHA_G: [{"id": 1, "name": "gates", "status": "completed", "conclusion": "success",
                     "created_at": "T", "head_sha": SHA_G}],
            SHA_R: [{"id": 2, "name": "gates", "status": "completed", "conclusion": "failure",
                     "created_at": "T", "head_sha": SHA_R}],
            SHA_P: [{"id": 3, "name": "gates", "status": "in_progress", "conclusion": None,
                     "created_at": "T", "head_sha": SHA_P}]}
    jobs = {1: jobs_green, 2: jobs_red, 3: jobs_pend}
    calls = []

    def fake(url, headers):
        calls.append((url, dict(headers)))
        u = urllib.parse.urlparse(url)
        if u.netloc == "blob.example.invalid":
            return 200, {}, _canned_log().encode()
        m = re.search(r"/actions/runs/(\d+)/jobs", u.path)
        if m:
            return 200, {}, json.dumps({"jobs": jobs[int(m.group(1))]}).encode()
        if u.path.endswith("/actions/runs"):
            sha = urllib.parse.parse_qs(u.query).get("head_sha", [""])[0]
            return 200, {}, json.dumps({"workflow_runs": runs.get(sha, [])}).encode()
        if re.search(r"/actions/jobs/\d+/logs$", u.path):
            return 302, {"Location": "https://blob.example.invalid/log?sig=x"}, b""
        return 404, {}, b""

    failures = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] ci-readback: {name}")
        if not cond:
            failures.append(name)

    def run(sha):
        buf = []
        c = Client("owner/repo", SECRET, get=fake)
        del calls[:]
        rc = readback(c, sha, out=buf.append)
        return rc, buf

    rc, buf = run(SHA_G)
    bite("GREEN control: all jobs success ⇒ rc 0, one line per job, a GREEN verdict",
         rc == 0 and sum(1 for x in buf if x.strip().startswith("job ")) == 3 and "GREEN" in buf[-1])
    bite("GREEN ⇒ no log is ever fetched", not any("/logs" in u for u, _ in calls))

    rc, buf = run(SHA_R)
    text = "\n".join(buf)
    bite("RED gates job ⇒ rc 1 and the failing step names are printed",
         rc == 1 and "Knowledge build — all derived views + blocking gates" in text and "RED" in buf[-1])
    bite("RED ⇒ the blocking lines are parsed out: the survey's ❌ [88] row and its SURVEY: line",
         "❌ [88] KG node-title generator drift check" in text and "SURVEY: 68 pass · 1 FAIL" in text)
    bite("RED ⇒ the build's unindented ❌ is printed under its === [88/154] header",
         "[88/154] KG node-title generator drift check → ❌ KG node titles are STALE" in text)
    bite("a selftest's INDENTED `❌ FAIL` fixture line is NOT read as a verdict",
         "PLANTED-FIXTURE-LINE" not in text)
    bite("an ADVISORY step's own ❌ / ⛔ lines are dropped once its `⚠ advisory step` line closes it",
         "ADVISORY-NOISE" not in text)
    bite("inside _build_all, a child's interleaved ❌ with no `(exit N)` is not read as a step verdict",
         "CHILD-INTERLEAVED-NOISE" not in text)
    raw = len(_canned_log())
    bite(f"the log is never dumped: {raw:,} bytes of log ⇒ ≤ 40 lines and ≤ 4,000 bytes printed, no filler",
         raw > 500_000 and len(buf) <= 40 and len(text.encode()) <= 4000 and "FILLER-STEP" not in text)
    bite("no raw-log timestamp survives into the output", not re.search(r"\d{4}-\d\d-\d\dT[\d:.]+Z", text))
    bite("the token is never printed", SECRET not in text)
    api_auth = [h.get("Authorization") for u, h in calls if urllib.parse.urlparse(u).netloc == "api.github.com"]
    blob_auth = [h.get("Authorization") for u, h in calls if urllib.parse.urlparse(u).netloc == "blob.example.invalid"]
    bite("the token goes to api.github.com and NOT to the log's redirect host",
         api_auth and all(a == "Bearer " + SECRET for a in api_auth) and blob_auth == [None])
    bite("the log is fetched only for the failed job (one fetch, job 22)",
         [u for u, _ in calls if u.endswith("/logs")] == ["https://api.github.com/repos/owner/repo/actions/jobs/22/logs"])

    rc, buf = run(SHA_P)
    bite("a run still in progress ⇒ rc 2, STILL RUNNING", rc == 2 and "STILL RUNNING" in buf[-1])
    rc, buf = run("d" * 40)
    bite("no run on the sha yet ⇒ rc 3, said out loud", rc == 3 and buf and buf[0].startswith("NO RUN YET"))

    # --owed: the newest handoff by NUMBER (100 beats 99 — a string sort would pick 99), and the sha is
    # the last commit that touched it. Built in a throwaway git repo; declared refusal if git is absent.
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as td:
            g = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c",
                                           "commit.gpgsign=false", *a], cwd=td, capture_output=True, text=True, check=True)
            g("init", "-q")
            for n in (99, 100):
                open(os.path.join(td, f"_HANDOFF-{n}-x.md"), "w").write(f"h{n}\n")
            g("add", "-A"); g("commit", "-q", "-m", "both")
            with open(os.path.join(td, "_HANDOFF-100-x.md"), "a") as f:
                f.write("## ⬛ POST-WRAP ADDENDUM (5b)\n")
            g("commit", "-q", "-am", "5b")
            want = g("rev-parse", "HEAD").stdout.strip()
            open(os.path.join(td, "other.txt"), "w").write("x\n")
            g("add", "-A"); g("commit", "-q", "-m", "later, not the handoff")
            sha, path = owed_sha(td)
            bite("--owed resolves the NEWEST handoff by number and the last commit touching it",
                 sha == want and path.endswith("_HANDOFF-100-x.md"))
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"[SKIP] ci-readback: --owed bite could not build a git fixture ({type(e).__name__}) — NOT a pass")
        failures.append("--owed bite could not run: git fixture unavailable")

    print(f"ci-readback selftest: {'PASS' if not failures else 'FAIL'} — "
          f"{'all bites held' if not failures else '; '.join(failures)}")
    return 0 if not failures else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="CI read-back for one commit — a short run summary, never the log.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sha", help="a commit sha (full or ≥7-char prefix) or a git ref such as HEAD")
    g.add_argument("--owed", action="store_true",
                   help="read the sha the newest _HANDOFF-*.md owes: the last commit that touched it")
    g.add_argument("--selftest", action="store_true", help="canned API JSON through a fake transport; no network")
    ap.add_argument("--poll", type=int, default=0, metavar="SECONDS",
                    help="re-read every 20 s until done or SECONDS pass (≤170: one tool call's budget)")
    ap.add_argument("--repo", help="owner/name; default: parsed from remote.origin.url")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.owed:
        sha, path = owed_sha()
        if not sha:
            print(f"NO OWED SHA — {'no _HANDOFF-*.md found' if not path else 'git has no commit touching ' + os.path.basename(path)}")
            return 3
        print(f"owed: {sha[:8]} — the last commit touching {os.path.basename(path)}")
    else:
        sha = resolve_sha(a.sha) or a.sha.lower()
        if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            print(f"not a sha and not a ref git can resolve: {a.sha!r}")
            return 3
    slug = a.repo or repo_slug()
    if not slug:
        print("no GitHub repo: remote.origin.url is not a github.com URL; pass --repo owner/name")
        return 5
    client = Client(slug, token())
    deadline = time.time() + min(max(a.poll, 0), 170)
    while True:
        buf = []
        try:
            rc = readback(client, sha, out=buf.append)
        except Exception as e:                                           # noqa: BLE001
            print(f"CI read-back could not reach the API: {type(e).__name__}: {e}")
            return 5
        if rc not in (2, 3) or time.time() + 20 > deadline:
            break
        time.sleep(20)
    print("\n".join(buf))
    return rc


if __name__ == "__main__":
    sys.exit(main())
