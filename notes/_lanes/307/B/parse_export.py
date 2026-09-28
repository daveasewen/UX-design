"""#307 lane B — parse Dave's export (the 78 answers) and lane A's card sources into one table: cards.json."""
import re, json
EXP = 'notes/_lanes/307/DAVE-RULINGS-2026-09-28-reopened-78.md'
t = open(EXP, encoding='utf-8').read()
lines = t.split('\n'); out = []; sec = None; i = 0
while i < len(lines):
    l = lines[i]
    m = re.match(r'## (\d+)\. (.*?) \((\d+) of', l)
    if m: sec = (int(m.group(1)), m.group(2))
    if l.startswith('- **'):
        q = re.match(r'- \*\*(.*)\*\*\s*$', l).group(1)
        a = lines[i+1].strip(); j = i + 2; extra = []
        while not lines[j].strip().startswith('`W-'):
            extra.append(lines[j].strip()); j += 1
        w = lines[j].strip()
        am = re.match(r'→ \*\*(.*?)\*\* · (.*?) · (click|take-all) · (\S+ \S+)$', a)
        wid, verdict, sess = [x.strip() for x in w.strip('`').split('·')]
        out.append(dict(n=len(out)+1, section=sec[0], theme=sec[1], q=q, label=am.group(1), rec=am.group(2),
                        how=am.group(3), at=am.group(4), note=' '.join(x for x in extra if x), wid=wid,
                        verdict=verdict, from_session=sess, wline=w))
        i = j
    i += 1
cards = {}
for f in ['cards-1.txt', 'cards-2.txt', 'cards-3.txt']:
    for blk in open('notes/_lanes/307/A/' + f, encoding='utf-8').read().split('\n@ ')[1:]:
        ls = blk.split('\n'); d = {}
        for x in ls[1:]:
            mm = re.match(r'^([A-Z]): (.*)', x)
            if mm: d.setdefault(mm.group(1), []).append(mm.group(2))
        d['opts'] = [x for x in ls if x[:2] in ('* ', '- ') and re.match(r'^[*-] [a-d]: ', x)]
        cards[ls[0].strip()] = d
for o in out:
    o['card'] = cards[o['wid']]
assert len(out) == 78 and len({o['wid'] for o in out}) == 78
json.dump(out, open('notes/_lanes/307/B/cards.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('78 parsed')
