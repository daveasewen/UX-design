#!/usr/bin/env python3
"""BITE for the three edge-proposal defects lane E found at #267 (fixed under s267-D3).

    python3 knowledge/_bite_kg_edge_proposal.py     # prints PASS/FAIL per case, exits 1 on any FAIL

Drives the REAL objects from knowledge/_build_kg_explorer.py — VERB_RX, MENTION_RX and the
window/direction arithmetic of the mention loop — not a copy. Mutation-proven: widen VERB_RX back
to a left boundary only and cases 1-5 fail; drop the neighbour clamp and case W2 fails.
"""
import os, sys, importlib.util

spec = importlib.util.spec_from_file_location(
    'kgb', os.path.join(os.path.dirname(os.path.abspath(__file__)), '_build_kg_explorer.py'))
kgb = importlib.util.module_from_spec(spec); spec.loader.exec_module(kgb)

fails = []


def check(name, got, want):
    ok = got == want
    print(('PASS  ' if ok else 'FAIL  ') + name + f'   got={got!r} want={want!r}')
    if not ok: fails.append(name)


def verb(text):
    """First verb the generator would propose in `text` (nearest match wins, as at :249)."""
    hit = None
    for k, rx in kgb.VERB_RX.items():
        m = rx.search(text)
        if m and (hit is None or m.start() < hit[1]): hit = (k, m.start())
    return hit[0] if hit else None


# ---- defect 1: the stem needs a RIGHT boundary. Nouns and adverbs must not read as verbs.
print('-- defect 1: stem boundary (_build_kg_explorer.py:87)')
check('"enactment" is NOT a verb hit', verb('the enactment of s151-D1'), None)
check('"override sets" is NOT a verb hit', verb('the override sets in s151-D1'), None)
check('"overrides.json" is NOT a verb hit', verb('token overrides.json for s151-D1'), None)
check('"NARROWEST" is NOT a verb hit', verb('the NARROWEST reading of s151-D1'), None)
check('"correctly" is NOT a verb hit', verb('s151-D1 renders correctly'), None)
check('"refinement" is NOT a verb hit', verb('a refinement of s151-D1'), None)
check('"supersedes" IS supersedes', verb('this supersedes s151-D1'), 'supersedes')
check('"retired" IS retires', verb('s151-D1 is retired here'), 'retires')
check('"narrows" IS narrows', verb('this narrows s151-D1'), 'narrows')
check('"enacting" IS enacts', verb('enacting s151-D1 today'), 'enacts')

# ---- defect 2: the window must not cross a NEIGHBOURING mention id.
print('-- defect 2: window clamped to the neighbouring ids (:243-247)')


def windows(says):
    ms = list(kgb.MENTION_RX.finditer(says))
    out = []
    for i, m in enumerate(ms):
        lo = ms[i - 1].end() if i else 0
        hi = ms[i + 1].start() if i + 1 < len(ms) else len(says)
        a, b = max(lo, m.start() - 80), min(hi, m.end() + 80)
        out.append((m.group(0), verb(says[a:b])))
    return out


LIST = 'this supersedes s122-D1, s123-D1, s131-D1 and s132-D1 for good'
w = dict(windows(LIST))
check('W1 the FIRST id in the list keeps the verb', w['s122-D1'], 'supersedes')
check('W2 a LATER id in the list gets NO verb', [w['s123-D1'], w['s131-D1'], w['s132-D1']],
      [None, None, None])

# ---- defect 3: direction. Verb AFTER the mention ⇒ the mention is the subject ⇒ t->s.
print('-- defect 3: direction test (:255-259)')


def direction(says):
    ms = list(kgb.MENTION_RX.finditer(says))
    m = ms[0]
    lo, hi = 0, (ms[1].start() if len(ms) > 1 else len(says))
    a, b = max(lo, m.start() - 80), min(hi, m.end() + 80)
    win = says[a:b]
    hit = None
    for k, rx in kgb.VERB_RX.items():
        mm = rx.search(win)
        if mm and (hit is None or mm.start() < hit[1]): hit = (k, mm.start())
    if not hit: return None
    return 't->s' if a + hit[1] >= m.end() else 's->t'


check('"<this> supersedes <t>" runs s->t', direction('this supersedes s151-D1 outright'), 's->t')
check('"<t> supersedes this" runs t->s', direction('s151-D1 supersedes this clause'), 't->s')
# declared LIMIT: passive voice still reads s->t (lane E rec #1's shape).
check('LIMIT: passive "CORRECTED BY ... (see t)" still reads s->t',
      direction('CORRECTED BY THIS SESSION (see s151-D1)'), 's->t')

print(('\nBITE FAILED: ' + ', '.join(fails)) if fails else '\nBITE PASSED — all cases green')
sys.exit(1 if fails else 0)
