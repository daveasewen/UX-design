#!/usr/bin/env python3
"""#304 Run 2b — decide each of A2's 93 close candidates LIMB BY LIMB (READ-ONLY; writes close_plan.json).
A limb is RECEIPTED (commit exists and says so / file exists at HEAD / a later-session artefact cites the doc
by path / the commit is on origin), DECLARED (a chat-only act: relayed in chat, stub delivered, subject read
back — the repo cannot see chat; the gap is written into closed_by), or MISSING. A row CLOSES only when no limb
is MISSING and no limb needs Dave's word. Dave-owned rows are never candidates (asserted)."""
import json, re, os, subprocess, collections
S = {i['id']: i for i in json.load(open('knowledge/_state.json'))['items']}
A2 = json.load(open('notes/_lanes/304/A2/autonomous_close_candidates.json'))
CL = json.load(open('notes/_lanes/304/R2/cite_lines.json'))
C = {c['sha'][:8]: c for c in json.load(open('/tmp/r2/commits.json'))}
def git(*a): return subprocess.run(['git', '--no-optional-locks', *a], capture_output=True, text=True).stdout.strip()
REMOTE = git('rev-parse', '--verify', '-q', 'origin/main') or git('rev-parse', '--verify', '-q', 'refs/remotes/origin/HEAD')
def on_remote(sha): return bool(REMOTE) and subprocess.run(['git', '--no-optional-locks', 'merge-base', '--is-ancestor', sha, REMOTE]).returncode == 0
def at_head(p): return subprocess.run(['git', '--no-optional-locks', 'cat-file', '-e', f'571d458c:{p}'], capture_output=True).returncode == 0
# hand corrections to A2's receipts, each read at the seat (see report § closes): A2 named post-wrap commits of
# the PREVIOUS session as the #204 and #236 wrap commits; the sessions' own record commits are these.
FIX = {'W-43': ['#204 wrap commit 973d3fa8'], 'W-47': ['#204 wrap commit 973d3fa8'], 'W-488': ['#204 wrap commit 973d3fa8'],
       'W-354': ['#236 wrap commit f1bdd4da']}
for r in A2:
    if r['id'] in FIX: r['receipts_a2'] = r['receipts']; r['receipts'] = FIX[r['id']]
# a citation is admissible only if its SESSION is trustworthy: dated by filename, or by the nearest heading in a
# ledger whose headings ARE session numbers; generated pages (explorer, rulings page, pack copies, dashboards,
# dream proposals) and _LIVE-STATE-ARCHIVE (its '#NNN' are often CI run numbers — '#482') are excluded.
LEDGER = re.compile(r'^(_GM-ARCHIVE\.md|_CARRIES\.md|GOOD-MORNING\.md|notes/_GAUGE-LOG\.md)$')
GENERATED = re.compile(r'_KG-EXPLORER|_RULINGS\.html|designer-skills-v|dashboard|notes/_dream/|_LIVE-STATE|\.bak$|_lanes/30[04]/|_lanes/286/')
for k, v in CL.items():
    v['cites'] = [c for c in v['cites'] if not GENERATED.search(c['file']) and c['session'] and c['session'] <= 304 and
                  (c['how'] == 'filename' or LEDGER.search(c['file']))]
# limbs the regexes cannot see, each checked by hand at the seat on 2026-09-26 (commands in the report)
MANUAL_LIMBS = {
 'W-274': [{'limb': 'carries-written-to-_CARRIES.md', 'state': 'RECEIPTED', 'receipt': "_CARRIES.md:627 '## residual → #227' (the #226 wrap's carries, in the new home)"},
           {'limb': 'carry_wording_check-repoint', 'state': 'RECEIPTED', 'receipt': "knowledge/_capture_gate.py:3487 carry_wording_check follows the pointer into `_CARRIES.md`; landed by 846914e2 '#226: the carry gate stops being blind'"}],
 'W-344': [{'limb': 'three-drive-outputs-quoted', 'state': 'RECEIPTED', 'receipt': "notes/_subreports/2026-09-02-235-L1-receipt-gate.md:85 'Region 4 — driven. Three runs, quoted below' (DRIVE 1 at :196, DRIVE 2 :154, DRIVE 3 :145)"}],
 'W-347': [{'limb': 'plan-html-cites-by-path', 'state': 'RECEIPTED', 'receipt': "_PLAN-designers-brain-2026-09-02-v1.html and -v2.html each name 2026-09-02-236-R1-principles-survey.md (grep -c 2 / 1)"}],
 'W-348': [{'limb': 'plan-html-cites-by-path', 'state': 'RECEIPTED', 'receipt': "_PLAN-designers-brain-2026-09-02-v1.html and -v2.html each name 2026-09-02-236-R2-sdlc-playbook.md (grep -c 1 / 1)"}],
 'W-356': [{'limb': 'plan-v2-points-at-G-assets', 'state': 'RECEIPTED', 'receipt': "_PLAN-designers-brain-2026-09-02-v2.html names notes/_subreports/assets/2026-09-02-237-G… 9 times"}],
 'W-362': [{'limb': 'six-lane-reports-filed', 'state': 'RECEIPTED', 'receipt': "notes/_subreports/2026-09-02-238-{P,A,B,C,M,V}-*.md — all 6 present at HEAD"}],
 'W-395': [{'limb': 'seam-block-pointer-to-lane-P', 'state': 'MISSING', 'receipt': "notes/_subreports/assets/2026-09-02-239-F-polarity-fix/_seam_block.sh:3 names '#238 lane P' as the gate's origin — not a pointer to lane P's #242 copy; not proven"}],
 'W-416': [{'limb': 's203-D1-read-back-of-the-push', 'state': 'MISSING', 'receipt': "the '#245 push read-back run or explicitly carried' limb has no receipt located"}],
 'W-424': [{'limb': 'commit-outcome-acted-on', 'state': 'DECLARED', 'receipt': "the #246 record is in git (session #247's commits follow it); 'acted on' is a seat act"}],
 'W-441': [{'limb': '#248-record-in-git', 'state': 'RECEIPTED', 'receipt': "commit c05ff59c 'after #248 2026-09-06 — THE 4+2 WALL LANDED …'"}],
 'W-100ah': [{'limb': 'every-brief-step-run', 'state': 'DECLARED', 'receipt': "per-step completion is the wrap's own claim in notes/_subreports/2026-09-08-259-W-wrap.md"},
             {'limb': 'wrap-report-cited', 'state': 'RECEIPTED', 'receipt': "notes/_GAUGE-LOG.md names 2026-09-08-259-W-wrap.md"}],
}
out = []
for r in A2:
    it = S[r['id']]; assert it['owner'] == 'claude' and it['state'] == 'open', r['id']
    cw = it['closes_when']; limbs = []; lc = cw.lower()
    ns = [int(x) for x in re.findall(r'#(\d{3})\b', cw)]
    # --- event limb: the commit A2 named
    for rc in r['receipts']:
        m = re.search(r'(#\d+) (wrap commit|ran \(commit) ([0-9a-f]{8})', rc)
        if m:
            sha = m.group(3); c = C.get(sha); n = int(m.group(1)[1:])
            ss = [int(x) for x in re.findall(r'#(\d{3})\b', c['subject'][:40])] if c else []
            if m.group(2) == 'wrap commit':      # the wrap commit OF session n
                ok = bool(c) and n in ss and 'wrap' in (c['subject'] + c['body']).lower()
                what = f"the #{n} wrap commit"
            else:                                 # 'ran': any commit of a session >= n proves session n took place
                ok = bool(c) and bool(ss) and max(ss) >= n
                what = f"session #{n} took place (a commit labelled #{max(ss) if ss else '?'} exists; A2's '#{n} ran' label is loose)"
            limbs.append({'limb': 'event-commit', 'state': 'RECEIPTED' if ok else 'MISSING',
                          'receipt': (f"{what}: commit {sha} ({c['date'][:10]}) '{c['subject'][:110]}'") if c else f'{sha} not found'})
        m = re.search(r'(notes/\S+\.md) exists=True', rc)
        if m:
            p = m.group(1); ok = at_head(p)
            limbs.append({'limb': 'report-filed', 'state': 'RECEIPTED' if ok else 'MISSING', 'receipt': f'{p} present at HEAD 571d458c'})
    # --- push limb
    if re.search(r'pushed|push is verified|push result line', lc):
        shas = [re.search(r'[0-9a-f]{8}', x).group(0) for x in r['receipts'] if re.search(r'[0-9a-f]{8}', x)]
        ok = shas and on_remote(shas[0])
        limbs.append({'limb': 'pushed', 'state': 'RECEIPTED' if ok else 'MISSING',
                      'receipt': f"{shas[0] if shas else '?'} is an ancestor of origin/main ({REMOTE[:8]}) — it reached the remote" if ok else 'not on origin'})
    # --- chat-only limbs (declared)
    for pat, name in [(r'relayed to dave in chat|relayed both title lines in chat', 'relayed-in-chat'),
                      (r'stub is delivered to the conductor', 'stub-delivered'),
                      (r'subject (is )?read back|read back from git log', 'subject-read-back'),
                      (r"read its replay-these", 'replay-these-read')]:
        if re.search(pat, lc): limbs.append({'limb': name, 'state': 'DECLARED', 'receipt': 'a chat/seat act the repo cannot witness'})
    # --- citation limbs: a later artefact cites the row's docs
    need = None
    m = re.search(r'#(\d{3}) opener|#(\d{3})\'s opener|at the #(\d{3}) opener|#(\d{3}) opener or a later session', cw)
    if m: need = int([g for g in m.groups() if g][0])
    elif re.search(r'cited that report by path in the #(\d{3}) wrap', lc): need = int(re.search(r'#(\d{3}) wrap', cw).group(1))
    elif re.search(r'plan html cites it by path|plan v2 carries each discharge|banner cites this brief|cites this document by path', lc): need = it['opened']
    # PRIMARY docs = the paths the condition names, else the row's home (never its links: a link is context)
    PRIM = [p.rstrip('.,;)') for p in re.findall(r'(?:notes|reviews)/[\w./-]+\.(?:md|html|json)', cw)] or [it['home']]
    ALLD = set(CL[r['id']]['docs']) | {it['home']} | set(PRIM)
    WRAPF = re.compile(r'_DECISION-HISTORY/|_GM-ARCHIVE\.md|_LIVE-STATE|-wrap\.md|wrap-brief|WRAP|GOOD-MORNING|_CHAIN\.md|_HANDOFF-')
    if need is not None:
        wrapcite = bool(re.search(r'cited that report by path in the #\d{3} wrap|banner cites this brief', lc))
        cs = [c for c in CL[r['id']]['cites'] if c['session'] and c['session'] >= need and not c['file'].endswith('.bak')
              and c['doc'] in PRIM and c['file'] not in ALLD and (not wrapcite or (WRAPF.search(c['file']) and c['session'] == need))]
        cs.sort(key=lambda c: (c['how'] != 'filename', c['session']))
        limbs.append({'limb': f'cited-at-or-after-#{need}', 'state': 'RECEIPTED' if cs else 'MISSING',
                      'receipt': (f"{cs[0]['file']}:{cs[0]['line']} (session #{cs[0]['session']} by {cs[0]['how']}) names {os.path.basename(cs[0]['doc'])}"
                                  + (f"; also {cs[1]['file']}:{cs[1]['line']}" if len(cs) > 1 else '')) if cs else 'no later citation found'})
    # --- ruling-shaped questions: actioned or carried (receipt = a later carry/ledger citing the report)
    if re.search(r'ruling-shaped|rsq|explicitly carried', lc):
        cs = [c for c in CL[r['id']]['cites'] if c['session'] and c['session'] > it['opened'] and c['doc'] in PRIM and c['file'] not in ALLD and
              re.search(r'_CARRIES\.md|GOOD-MORNING|_GM-ARCHIVE|_HANDOFF|delegated-wrap-brief|wrap-brief|_LIVE-STATE', c['file'])]
        limbs.append({'limb': 'questions-carried', 'state': 'RECEIPTED' if cs else 'MISSING',
                      'receipt': (f"carried as a unit: {cs[0]['file']}:{cs[0]['line']} (session #{cs[0]['session']}) names the report — per-question carry NOT itemised") if cs else 'no later carry/ledger line names the report'})
    # --- Dave limbs
    dave = re.search(r'reached dave|dave has answered|dave retires|ruled by dave|dave has either ruled', lc)
    if dave:
        alt = re.search(r'\bor\b', lc[max(0, dave.start() - 80):dave.end() + 120])
        limbs.append({'limb': 'dave', 'state': 'DAVE-ALT' if alt else 'DAVE', 'receipt': cw[max(0, dave.start() - 40):dave.end() + 80]})
    # --- memory hook receipt inside the file
    if 'project memory' in lc:
        p = it['home']; txt = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else ''
        m2 = re.search(r'(?m)^#+ .*RECEIPT.*$', txt)
        limbs.append({'limb': 'memory-receipt-in-file', 'state': 'RECEIPTED' if m2 else 'MISSING',
                      'receipt': f"{p}:{txt[:m2.start()].count(chr(10)) + 1} '{m2.group(0)[:90]}'" if m2 else f'{p} carries no RECEIPT section'})
    for extra in MANUAL_LIMBS.get(r['id'], []): limbs.append(dict(extra))
    # a Dave limb that is one branch of an OR ('ruled by Dave OR explicitly carried') is satisfied by the receipted
    # carry branch; a Dave limb with no alternative (W-363 'have reached Dave') keeps the row open.
    if any(l['limb'] == 'questions-carried' and l['state'] == 'RECEIPTED' for l in limbs):
        for l in limbs:
            if l['limb'] == 'dave' and re.search(r'\bor\b', l['receipt']): l['state'] = 'DAVE-ALT'
    miss = [l for l in limbs if l['state'] in ('MISSING', 'DAVE')]
    out.append({'id': r['id'], 'closes_when': cw, 'limbs': limbs, 'verdict': 'CLOSE' if limbs and not miss else 'LEAVE-OPEN',
                'why_open': [l['limb'] for l in miss]})
json.dump(out, open('notes/_lanes/304/R2/close_plan.json', 'w'), ensure_ascii=False, indent=1)
print(collections.Counter(o['verdict'] for o in out)); print(collections.Counter(tuple(o['why_open']) for o in out if o['why_open']))
print('remote', REMOTE[:12])
