#!/usr/bin/env python3
"""#305 H1 — call 36, the carry diet (s305-D36), on `_CARRIES.md` § residual → #305 ONLY.
The 342 are A2's exact list (`notes/_lanes/304/A2/carries_classified.json`, index-aligned with carries304.json, i.e. the
#304 line); each is mapped to its #305 segment (age +1, same _carry_norm, else same _carry_title) — 709/709 map uniquely.
An item is removed as a BLOCK: its aged `·`-segment plus the un-aged `·`-segments that follow it (its own continuation text).
HELD, not removed: (a) a splitter fragment whose parent item is KEPT (removing it would cut a live item mid-sentence);
(b) the newest item of each recurring series (the page: "recurring series keep one line each").
Nothing is re-worded; kept segments are byte-identical; every removed item stands verbatim in § residual → #304.
  python3 carry_diet.py --dry-run | --write"""
import json, sys, re, collections
sys.path.insert(0, 'knowledge'); import _capture_gate as c
WRITE = '--write' in sys.argv
LANE = 'notes/_lanes/305/H1'
text = open('_CARRIES.md', encoding='utf-8').read()
lines = text.split('\n')
idx = [i for i, l in enumerate(lines) if '**residual → #305:**' in l]; assert len(idx) == 1
L = lines[idx[0]]
it = json.load(open('notes/_lanes/304/A2/carries304.json')); K = json.load(open('notes/_lanes/304/A2/carries_classified.json'))
assert len(it) == len(K) == 709
m = re.match(r"^>?\s*\*\*residual\s*→\s*#\d+:?\*\*", L.strip()); pre = L[:L.index(m.group(0)) + len(m.group(0))]
body = L[len(pre):]
raw = body.split('·')
aged = [bool(c._AGE_RE.search(s) and len(c._carry_norm(s)) >= 20) for s in raw]
assert sum(aged) == len(c._carry_items(L)) == 715
aged_idx = [j for j, a in enumerate(aged) if a]
# block of aged raw j = j .. next aged raw - 1
block = {j: list(range(j, (aged_idx[n + 1] if n + 1 < len(aged_idx) else len(raw)))) for n, j in enumerate(aged_idx)}
seg = {j: (int(c._AGE_RE.search(raw[j]).group(1)), raw[j].strip()) for j in aged_idx}
byn = collections.defaultdict(list); byt = collections.defaultdict(list)
for j, (a, s) in seg.items(): byn[(a, c._carry_norm(s))].append(j); byt[(a, c._carry_title(s))].append(j)
used = set(); map305 = {}
for i, (a, t) in enumerate(it):
    cands = [j for j in byn[(a + 1, c._carry_norm(t))] if j not in used] or [j for j in byt[(a + 1, c._carry_title(t))] if j not in used]
    assert len(cands) >= 1, i
    map305[i] = cands[0]; used.add(cands[0])
cls = {i: K[i]['cls'] for i in range(709)}
DROPCLS = lambda k: k != 'substantive'
drop = {i for i in range(709) if DROPCLS(cls[i])}
assert len(drop) == 342, len(drop)
held = {}
# (b) series keep one line each — the recurring series (not the boilerplate, which the page calls copies, not a series)
series = collections.defaultdict(list)
for i in drop:
    if cls[i].startswith('series:') and 'boilerplate' not in cls[i]: series[cls[i]].append(i)
for k, ids in series.items():
    keep = min(ids, key=lambda i: (it[i][0], i))       # the newest (lowest age) line of the series
    held[keep] = f'kept as the one line of the recurring series "{k[8:]}" ({len(ids)} items)'
# (a) fragments whose parent is kept
order = sorted(range(709), key=lambda i: map305[i])
for n, i in enumerate(order):
    if cls[i].startswith('fragment'):
        p = n - 1
        while p >= 0 and cls[order[p]].startswith('fragment'): p -= 1
        parent = order[p] if p >= 0 else None
        if parent is None or parent not in drop or parent in held:
            held[i] = f'splitter fragment whose parent item ({"none" if parent is None else "#304 idx " + str(parent)}, {cls.get(parent)}) is KEPT — removing it would cut that live item mid-sentence'
removed = sorted(drop - set(held))
rm_raw = set()
for i in removed: rm_raw.update(block[map305[i]])
kept_raw = [s for j, s in enumerate(raw) if j not in rm_raw]
newL = pre + '·'.join(kept_raw)
after = c._carry_items(newL)
cnt = collections.Counter(cls[i] for i in removed); hcnt = collections.Counter(cls[i] for i in held)
print(('WRITE' if WRITE else 'DRY-RUN'), 'drop set', len(drop), 'removed', len(removed), 'held', len(held), '| live', 715, '->', len(after))
print(' removed by class', dict(cnt)); print(' held by class', dict(hcnt))
# proofs: every kept aged segment is byte-identical and in order; nothing outside the #305 line changes
kept_aged = [raw[j].strip() for j in aged_idx if j not in rm_raw]
assert [s for _, s in after] == kept_aged
assert len(after) == 715 - len(removed), (len(after), 715 - len(removed))
# every removed item exists verbatim in the #304 line
l304 = [l for l in lines if '**residual → #304:**' in l][0]
for i in removed: assert it[i][1] in l304
rec = {'provenance': '305 · 2026-09-27 · lane H1', 'ruling': 's305-D36', 'live_before': 715, 'live_after': len(after),
       'drop_set': 342, 'removed': [{'idx304': i, 'age305': it[i][0] + 1, 'cls': cls[i], 'head': K[i]['head'][:160]} for i in removed],
       'held': [{'idx304': i, 'cls': cls[i], 'why': w, 'head': K[i]['head'][:160]} for i, w in sorted(held.items())]}
json.dump(rec, open(f'{LANE}/carry_diet.json', 'w'), indent=1, ensure_ascii=False)
if WRITE:
    open(f'{LANE}/backup/residual-305-pre-diet.txt', 'w', encoding='utf-8').write(L + '\n')
    note = (f"<!-- CARRY DIET `s305-D36` (Dave, sitting call 36, 2026-09-27 14:28 BST, \"yes\" to 'The carry diet: drop 342 of 709 items from the live carry list?'), "
            f"applied by #305 lane H1: {len(removed)} of A2's 342 removed from the line below as whole items (struck, deck/Friday, boilerplate, recurring-series repeats, "
            f"and fragments whose parent item went too); {len(held)} held (one line per recurring series kept; fragments of KEPT items kept so no live item is cut mid-sentence). "
            f"Live list {715} -> {len(after)}. Every removed item stands VERBATIM in § residual → #304 (one age lower). Nothing below was re-worded; the kept text is byte-identical. "
            f"List: notes/_lanes/305/H1/carry_diet.json; the line as it stood before the diet: notes/_lanes/305/H1/backup/residual-305-pre-diet.txt -->")
    new_lines = lines[:idx[0]] + [note] + [newL] + lines[idx[0] + 1:]
    open('_CARRIES.md', 'w', encoding='utf-8').write('\n'.join(new_lines))
    print(' written')
