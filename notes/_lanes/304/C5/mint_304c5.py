# #304 C5 commit seat - mint the store rows for the wave-five filed reports (doc-row gate, s218-D7),
# and close W-304c4 (its final copy rides this commit). Modelled on C4's mint_304c4.py.
# IDs at most two suffix characters (ID_RE). V5 wrote its id as W-304fv5 (three chars, refused by ID_RE); minted as W-304v5.
import sys, os, json, re
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
def spec(path):
    for line in open(path):
        if line.startswith('{"id"'):
            return json.loads(line)
    raise SystemExit('no spec in ' + path)
KEEP = ('id','home','links','title','body','closes_when','owner','condition')
def pick(d):
    return {k: d[k] for k in KEEP if k in d}
W5A = S + '2026-09-27-304-W5a-gate-bugs-and-trim.md'
W5B = S + '2026-09-27-304-W5b-tuesday-sitting.md'
W5C = S + '2026-09-27-304-W5c-node-titles.md'
V5 = S + '2026-09-27-304-V5-verifier-wave-five.md'
F5 = S + '2026-09-27-304-F5-wave-five-fixes.md'
R4S2 = S + '2026-09-27-304-R4s2-candidate-2-scores.md'
C5 = S + '2026-09-27-304-C5-commit-seat-wave-five.md'
C4 = S + '2026-09-27-304-C4-commit-seat-wave-four.md'

fa = pick(spec(W5A))
fa['title'] = ("#304 W5a filed report - five no-ruling defects from candidate 2 fixed at their generators: receipt gate skips "
               "APOLLO-DEMO-fenced scripts, icon-source reads markup only, leading-trim scaffold stops at the next component scope "
               "(111 copies); the ROOT default change was narrowed by F5 to a chart-only restore and held back for Dave (call 41c); "
               "right chart gutter computed from labels (ds-012b twin), geometry frames = the chain of nested scroll boxes")
fa['body'] += (" Row minted by the C5 commit seat. F5 narrowed the trim: canon.css's root default is HEAD's again, 14 generated "
               "chart-only restores clear the legend clip; W5a's root version is held back in notes/_lanes/304/W5a/held-back/ for "
               "Dave (sitting call 41c).")
fa['links'] = fa['links'] + ['notes/_lanes/304/W5a/held-back/root-default-bounded.patch']

fb = pick(spec(W5B))
fb['body'] += (" Row minted by the C5 commit seat. Corrected by F5 per V5 (calls 1, 4, 5, 6, 11, 23 pointer, 53; slot 41a-41e "
               "filled; 58 decision boxes).")

fc = dict(id='W-304fc', home=W5C, owner='claude',
    links=['knowledge/gen_kg_titles.py','knowledge/_node_titles.json','notes/_lanes/304/W5c/tools/wire_kg_generators.py',
           'notes/_lanes/304/W5c/sample-30-handcheck.json','notes/_lanes/304/W5c/renders/kg-ruling-panel-s133-D1-1440.png'],
    title="#304 W5c - the explorer's 1,203 bare-code ruling/rule/session nodes get derived plain titles (code + title, v1.29); gen_kg_titles.py + _node_titles.json; wiring for both KG generators tested, handed over",
    body=("s218-D7 filed report, wave five seat W5c (#304); row minted by the C5 commit seat from the report's spec. Bare-code "
          "labels in the three kinds 1,203 -> 0; 30-sample hand check 0 misstated; node ids and edges identical, only label and "
          "titleFrom move; display only, no ruling text changed. Session count fixed by F5 (#n-Dk and '#n (...)' forms: #76 7, "
          "#31/#57/#79/#81/#82 1 each, #245 10 -> 11). The KG generator wiring (4 steps + 4 GATE routes, 148 -> 152) is applied "
          "by the C5 commit seat and lands in the wave-five commit."),
    closes_when="the wave commit carrying W5c is pushed with CI read back by name, wire_kg_generators.py has run on the mount after W5a's commit (4 steps green in CI), and Dave has looked at the dug canvas (section 3: code-only on the canvas, or code + title)")

v5 = pick(spec(V5)); v5['id'] = 'W-304v5'
v5['body'] += " Row minted by the C5 commit seat; V5 wrote the id as W-304fv5, which ID_RE refuses (three suffix characters), so it is W-304v5."

s2 = pick(spec(R4S2))
s2['body'] += " Row minted by the C5 commit seat."

f5 = pick(spec(F5))
f5['body'] += " Row minted by the C5 commit seat."

c5 = dict(id='W-304c5', home=C5, owner='claude', links=['knowledge/_git_commit.sh', 'notes/_lanes/304/C5/'],
    title="#304 C5 - the commit seat, wave five: W5a (narrowed by F5), W5c with the KG generator wiring, the Tuesday sitting page, candidate 2's runs and scores, V5, F5 and C4's final copy in one commit, pushed, CI read back",
    body="s218-D7 filed report, commit seat, wave five (#304). The interim copy rides the wave-five commit; the final copy with the sha, the push range and CI verdict by job rides the next commit.",
    closes_when="the final copy of this report, carrying the sha, the push range and CI verdict by job, is committed")

rows = [fa, fb, fc, v5, s2, f5, c5]
doc = st.load()
have = {i['id']: i for i in doc['items']}
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=304, state='open', **r)
    print('added', r['id'])
c4 = have['W-304c4']
if c4['state'] != 'done':
    c4['state'] = 'done'
    c4['closed_by'] = ("#304 C5 commit seat: the FINAL copy of notes/_subreports/2026-09-27-304-C4-commit-seat-wave-four.md "
                       "(sha 3100da99, push 86249459..3100da99, CI run 36291750194 by job, candidate-2 zip sha256 8a75ce32...) "
                       "and its transcripts in notes/_lanes/304/C4/ ride the wave-five commit, as the row's close condition says")
    print('closed W-304c4')
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
