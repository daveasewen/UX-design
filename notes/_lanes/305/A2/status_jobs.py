# #305 lane A2 — the status writes and evidence amends from Dave's 2026-09-28 loose-ends export.
# Each job runs through knowledge/_inscribe_ruling.py (--amend-evidence / --set-status), dry run first for ALL jobs,
# then --write one at a time only if every dry run was clean. Usage: python3 status_jobs.py [--write]
import json, re, os, sys, subprocess
sys.path.insert(0, 'knowledge')
import _governs as g
EX = 'notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md'
PAGE = 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html'
STAMPS = 'notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html'
H1 = 'notes/_subreports/2026-09-27-305-H1-records.md'
B5 = 'notes/_subreports/2026-09-27-305-B5-loose-ends.md'
DIR = 'notes/_lanes/305/A2/entries/'
txt = open(EX, encoding='utf-8').read()
A = json.loads(re.search(r'```json\n(.*?)\n```', txt, re.S).group(1))['answers']
q = lambda s: '"' + s + '"'
v = lambda k: A[k]['verdict']
at = lambda k: A[k]['at'].split(' ')[1]
def R(): return {r['id']: r for r in json.load(open('knowledge/_rulings.json', encoding='utf-8'))['rulings']}
S0 = R()
was = lambda i: f" · was: {S0[i]['status']}"
D38 = ("#305 `s305-D38` (Dave, sitting call 38, verbatim \"yes to all six\"; kinds by `notes/_lanes/304/R6b/counts.json`), kind 5 "
       "'no trace of the build: add to the not-built list'")
jobs = []   # (kind, id, payload, sha)
# ---- s305-D25, the modal rule: evidence first (his verdict), then status back to enacted at the sha that carries R4a's wording
jobs.append(('amend', 's305-D25', S0['s305-D25']['evidence'] + [
    EX + '#4a · modal rule',
    PAGE + f" - group 4 part 4a: Dave accepted the wording on 2026-09-28, verdict, verbatim: {q(v('g4-modal'))} (saved {at('g4-modal')}). "
    "The wording he accepted is the `when` of modals.meta.json, split-button.meta.json and dropdown.meta.json as the page quoted it "
    "(R4a's draft, carried in by lane B2), which landed at 27efb7b6 and reads the same at HEAD 01fb005a; finding F3's hold is discharged"], None))
jobs.append(('status', 's305-D25',
    "enacted #305 2026-09-28 — DAVE ACCEPTED THE WORDING: loose-ends page 4a, verdict, verbatim: " + q(v('g4-modal')) +
    f" (saved {at('g4-modal')}). The words are R4a's draft `when` in the three metas (modals, split-button, dropdown), carried in by "
    "lane B2 at commit 27efb7b6 and unchanged at HEAD 01fb005a (`git log -S` on each meta names 27efb7b6), so the status returns to "
    "enacted at that sha; the return to `ruled` at fd607c74 was for his word, which is now given" + was('s305-D25'), '27efb7b6'))
# ---- kind 5 of call 38 (eight): s155-D1 settled, s229-D3 read as built, six to the not-built list
jobs.append(('amend', 's155-D1', S0['s155-D1']['evidence'] + [
    EX + '#3a · the two greens',
    PAGE + f" - group 3 part 3a: Dave's verdict on 2026-09-28, verbatim: {q(v('g3-green'))} (saved {at('g3-green')}); the page's "
    "recommendation was to say settled, #137F3C on white, #66CC8D everywhere else, for mono only, as this ruling's own amendment by "
    "addition at #155 records"], None))
jobs.append(('status', 's155-D1',
    "enacted — SETTLED AT #155 AND ALREADY IN THE TREE (#305 2026-09-28): Dave's verdict on the loose-ends page 3a, verbatim " +
    q(v('g3-green')) + " — the page's recommendation: #137F3C on white, #66CC8D everywhere else, for mono only, as this ruling's own "
    "amendment by addition at #155 records (\"VALUES RESOLVED AND SCOPE NARROWED, both Dave's\", by reference to `s144-D1`). It therefore "
    "leaves " + D38 + ": canon has emitted the pair since the rung was minted at a1995c0c (#145, `s145-D1`) — --rag-success-ink #137F3C "
    "in the light block and #66CC8D in the dark block of knowledge/canon/canon.css (lines 318 and 705 at HEAD 01fb005a) — and #156's "
    "measure found every existing seat already carries it. ⚠ NOT TAKEN: #156's residual (e), the positive-money green-text seat "
    "(amount-display's sign enum has no positive value), stays Dave's to rule as #156 recorded; canon switching the rung by mode "
    "rather than by ground is also not asked here" + was('s155-D1'), 'a1995c0c'))
jobs.append(('amend', 's229-D3', S0['s229-D3']['evidence'] + [
    EX + '#3b · one more in the same kind',
    H1 + " - call 38, kind 5: s229-D3 looks BUILT at the #229 wrap commit, the four segmented snippets carry the injected `seg-concentric` partial"], None))
jobs.append(('status', 's229-D3',
    "enacted — READ AS BUILT (#305 2026-09-28): Dave's verdict on the loose-ends page 3b, verbatim " + q(v('g3-seg')) +
    f" (saved {at('g3-seg')}), which takes it off " + D38 + ". Built at baf5458e (#229, 2026-08-31, the day of the ruling): the "
    "segmented partial group in knowledge/component-types.json and knowledge/gen_component_partials.py with the `$scan` membership "
    "sweep, wired in the build as 'component-partials sync' and its selftest; the four segmented snippets (Segmented-control, "
    "View-options, Filter-toolbar-bar, Template-dashboard) carry the generated `seg-concentric` partial at HEAD 01fb005a (H1's "
    "finding). Checked by lane A2: baf5458e resolves by `git cat-file` and its diff adds the `$scan` block" + was('s229-D3'), 'baf5458e'))
for i in ['s234-D4', 's212-D1', 's216-D1', 's244-D1', 's256-D1', 's262-D5']:
    jobs.append(('status', i,
        "ruled — NOT BUILT, ON THE NOT-BUILT LIST (" + D38 + "). No trace of its build was found (the stamps page, "
        f"{STAMPS}, kind 5: no build found, a receipt that says \"not built\", or two reports that disagree). The one of the eight that "
        "needed his word, the two green values of `s155-D1`, he answered on 2026-09-28, verbatim " + q(v('g3-green')) + "; `s155-D1` "
        "and `s229-D3` (" + q(v('g3-seg')) + ") left the list that day, and this one stays on it" + was(i), None))
# ---- s305-D38: kinds 1 to 5 discharged; 28 of kind 6 remain
jobs.append(('amend', 's305-D38', S0['s305-D38']['evidence'] + [
    H1 + " - kinds 1, 2, 3 and 4 stamped by lane H1 (6 enacted, 10 superseded, 14 standing, 7 part-enacted and parked); kind 6, "
    "36 of 64 stamped on a file-and-line receipt, 28 left because no line builds them",
    EX + " - kind 5 discharged on 2026-09-28 by lane A2 of #305 after Dave's two verdicts, verbatim " + q(v('g3-green')) + " and " +
    q(v('g3-seg')) + ": s155-D1 enacted at a1995c0c, s229-D3 enacted at baf5458e, the other six stamped ruled, NOT BUILT, on the "
    "not-built list. Kinds 1 to 5 are now fully discharged; only the 28 untraceable rulings of kind 6 remain, so this ruling stays ruled"], None))

def run(job, write):
    kind, rid, payload, sha = job
    if kind == 'amend':
        fn = f"{DIR}amend-{rid}.json"
        json.dump(payload, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        args = ['python3', 'knowledge/_inscribe_ruling.py', '--amend-evidence', '--id', rid, '--entry', fn]
    else:
        json.dump({'id': rid, 'status': payload, 'sha': sha}, open(f"{DIR}status-{rid}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        args = ['python3', 'knowledge/_inscribe_ruling.py', '--set-status', rid, payload] + (['--evidence-sha', sha] if sha else [])
    p = subprocess.run(args + (['--write'] if write else ['--dry-run']), capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()

# path-token hygiene on every new evidence line
for k, rid, payload, sha in jobs:
    if k == 'amend':
        for ln in payload[len(S0[rid]['evidence']):]:
            if g.evidence_form(ln) == 'anchor':
                _, err = g.resolve_anchor(ln); assert not err, (rid, ln, err)
            for t in g.PATHISH_RE.findall(ln):
                assert os.path.exists(t.rstrip('.')), (rid, t)
for sha in ['27efb7b6', 'a1995c0c', 'baf5458e']:
    assert subprocess.run(['git', '--no-optional-locks', 'cat-file', '-e', sha + '^{commit}']).returncode == 0, sha
write = '--write' in sys.argv
if not write:
    # a dry run of a status AFTER an amend of the same id is only meaningful once the amend is in; amends and statuses touch
    # different fields, so each is dry-run against the current file here, and again individually just before its write
    for j in jobs:
        rc, out = run(j, False); print(rc, j[0], j[1], out[:220]); assert rc == 0
    print('ALL DRY CLEAN', len(jobs))
else:
    for j in jobs:
        rc, out = run(j, False); print('dry', rc, j[0], j[1], out[:160]); assert rc == 0
        rc, out = run(j, True); print('write', rc, j[0], j[1], out[:220]); assert rc == 0
    print('ALL WRITTEN', len(jobs))
