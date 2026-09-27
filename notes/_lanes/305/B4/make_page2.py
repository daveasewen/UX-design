"""#305 B4: fills page2.src.html with the 102 parked rows (A2's D2 list, open in knowledge/_state.json today),
grouped by A2's theme, and writes page2.gen.html. Run from the repo root."""
import json, sys, html, collections
sys.path.insert(0, 'notes/_lanes/305/B4'); import rows
E = html.escape
S = json.load(open('knowledge/_state.json')); items = {i['id']: i for i in S['items']}
D = json.load(open('notes/_lanes/304/A2/decision_unblocks.json'))['D2 park stale ruling-shaped questions (>=14d)']
dq = {x['id']: x for x in json.load(open('notes/_lanes/304/A2/dave_queue.json'))}
hits = json.load(open('notes/_lanes/305/B4/d2_ruling_hits.json'))
live = [i for i in D if items[i]['state'] == 'open']
assert len(live) == 102 and set(live) == set(rows.ROWS)
def age(i): return dq[i]['age_days'] + 1          # A2 counted to 26 Sep; this page is 27 Sep
def grp(i):
    t = dq[i]['theme'][:2]
    return 'T9+T0' if t in ('T9', 'T0') else t
def cites(i):
    h = hits.get(i) or []
    if not h: return ''
    return ' · cited by ' + (', '.join(h) if len(h) <= 3 else '%s and %d more' % (', '.join(h[:2]), len(h) - 2))
def row(i, extra=''):
    q, trip = rows.ROWS[i]; it = items[i]
    return ('<li class="pr" data-id="%s"><label class="keep"><input type="checkbox" data-k="%s"><span>Keep open</span></label>'
            '<div class="rq"><p class="qq">%s</p>%s<p class="rm"><b>%d days</b> · from #%s · reopens when %s</p>'
            '<p class="rid">%s%s</p></div></li>') % (i, i, E(q), extra, age(i), it.get('opened'), E(trip), i, E(cites(i)))
by = collections.defaultdict(list)
for i in live: by[grp(i)].append(i)
parts = []
for n, (key, name, why) in enumerate(rows.GROUPS, 1):
    ids = sorted(by[key], key=lambda i: (-age(i), i))
    ages = [age(i) for i in ids]
    parts.append('<section class="grp" id="g-%s"><div class="wrap"><p class="label">Group %d of %d · %d questions · %d to %d days old</p>'
                 '<h2>%s</h2><p class="gwhy">%s</p><ol class="prs">%s</ol>'
                 '<label class="gnote"><span>Anything in this group, in your words</span><textarea data-g="%s" placeholder="A line is enough: keep, drop, merge, or ask."></textarea></label>'
                 '</div></section>' % (key.replace('+', ''), n, len(rows.GROUPS), len(ids), min(ages), max(ages), E(name), E(why),
                                       ''.join(row(i) for i in ids), key))
flags = ''.join(row(i, '<p class="fl">%s</p>' % E(r)) for i, r in rows.FLAGS)
oldest = max(age(i) for i in live); youngest = min(age(i) for i in live)
cited = sum(1 for i in live if hits.get(i))
t = open('notes/_lanes/305/B4/page2.src.html').read()
t = t.replace('{{GROUPS}}', ''.join(parts)).replace('{{FLAGS}}', flags)
t = t.replace('{{OLDEST}}', str(oldest)).replace('{{YOUNGEST}}', str(youngest)).replace('{{CITED}}', str(cited))
t = t.replace('{{JUMPS}}', ''.join('<li><a href="#g-%s">%s (%d)</a></li>' % (key.replace('+', ''), E(name), len(by[key])) for key, name, _ in rows.GROUPS))
t = t.replace('{{GROUPLIST}}', ' · '.join('%s %d' % (name, len(by[key])) for key, name, _ in rows.GROUPS))
t = t.replace('{{ROWDATA}}', json.dumps({i: {'q': rows.ROWS[i][0], 's': items[i].get('opened'), 'a': age(i)} for i in live}))
open('notes/_lanes/305/B4/page2.gen.html', 'w').write(t)
print('page2.gen.html', len(t), 'groups', {k: len(v) for k, v in by.items()})
