#!/usr/bin/env python3
"""#304 Run 2c — the MUTATION TEST for the regrowth arm, recorded (READ-ONLY on the store: works on an
in-memory copy; the mutant module is written to a temp dir, never over knowledge/_state.py).
  A. live store: how many rows the arm names today;
  B. planted: the live store + ONE planted row closing on '#250 opener' → it must be named (count +1);
  C. SOURCE MUTATION — the clause removed (`rg = past_session_closes(items)` → `rg = []`) → the planted row
     must NOT be named; and the mutant's own --selftest must go RED (the selftest bites the removal);
  D. a second mutant — the pattern gutted (PAST_SESSION_RE never matches) → planted row not named, selftest RED.
Writes notes/_lanes/304/R2/mutation_test.json."""
import json, os, sys, copy, tempfile, importlib.util, shutil, io, contextlib
REPO = os.getcwd(); SRC = os.path.join(REPO, 'knowledge', '_state.py')
def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path)); spec.loader.exec_module(m); return m
def named(mod, doc):
    ok, fs, ns = mod.check(doc)
    return ok, [x for x in fs + ns if 'REGROWTH' in x]
import re as _re
def check_count(hit):
    """the number of rows check() ITSELF names (parsed from its REGROWTH note), 0 when it names none"""
    m = _re.search(r'(\d+) live row\(s\)', hit[0]) if hit else None
    return int(m.group(1)) if m else 0
orig = load_mod(SRC, '_state_orig')
live = orig.load()
res = {'source': 'knowledge/_state.py'}
ok, hit = named(orig, live)
res['A_live'] = {'check_ok': ok, 'named_rows': len(orig.past_session_closes(live['items'])), 'note': hit[0][:300] if hit else None}
planted = copy.deepcopy(live)
row = dict(live['items'][0]); row.update(id='W-999', title='PLANTED by #304 R2 mutation test', state='open', owner='claude',
     opened=250, condition='stated', closes_when='the #250 opener has read this report and carried its questions')
row.pop('closed_by', None); planted['items'].append(row)
ok, hit = named(orig, planted)
res['B_planted'] = {'check_ok': ok, 'named_rows': len(orig.past_session_closes(planted['items'])), 'named_by_check': check_count(hit),
                    'planted_named': any(i == 'W-999' for i, _, _ in orig.past_session_closes(planted['items'])),
                    'note_mentions_planted': bool(hit) and ('W-999' in hit[0] or '+' in hit[0])}
src = open(SRC, encoding='utf-8').read()
mutants = {'C_clause_removed': ('    rg = past_session_closes(items)\n', '    rg = []  # MUTANT: the regrowth clause removed\n'),
           'D_pattern_gutted': ('PAST_SESSION_RE = re.compile(\n', 'PAST_SESSION_RE = re.compile(r"(?!x)x") or re.compile(\n')}
for key, (a, b) in mutants.items():
    assert src.count(a) == 1, key
    td = tempfile.mkdtemp(dir=os.environ.get('TMPDIR', '/tmp'))
    shutil.copy(os.path.join(REPO, 'knowledge', '_helpgate.py'), td)
    mp = os.path.join(td, '_state.py'); open(mp, 'w', encoding='utf-8').write(src.replace(a, b))
    mod = load_mod(mp, '_state_' + key); mod.STORE = orig.STORE; mod.HERE = orig.HERE
    ok, hit = named(mod, planted)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): st_fails, st_n = mod.selftest()
    res[key] = {'check_ok': ok, 'named_by_check': check_count(hit),
                'planted_named': check_count(hit) == res['B_planted']['named_by_check'],
                'regrowth_lines': len(hit), 'mutant_selftest_red': bool(st_fails),
                'selftest_fail_lines': [f[:160] for f in st_fails if 'regrowth' in f.lower()][:3]}
    shutil.rmtree(td)
st_fails, st_n = orig.selftest()
res['E_unmutated_selftest'] = {'green': not st_fails, 'bites': st_n}
res['VERDICT'] = ('BITES' if res['B_planted']['planted_named'] and not res['C_clause_removed']['planted_named']
                  and res['C_clause_removed']['mutant_selftest_red'] and not res['D_pattern_gutted']['planted_named']
                  and res['D_pattern_gutted']['mutant_selftest_red'] and res['E_unmutated_selftest']['green'] else 'DOES NOT BITE')
json.dump(res, open('notes/_lanes/304/R2/mutation_test.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
