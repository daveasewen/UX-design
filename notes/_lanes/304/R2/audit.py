#!/usr/bin/env python3
"""#304 Run 2a — the back-stamp audit (READ-ONLY; writes only its own JSON under notes/_lanes/304/R2/).

For every ruling in the audit population, gather receipts from three sources and PROPOSE a verdict:
  (1) commit messages (subject+body) that name the id, with range expansion (sNNN-D1..D4, D1/D2, D1–D4),
      split into clauses; a clause is POSITIVE when it carries a completed-enactment verb and no negation;
  (2) the tree at HEAD (git grep) — non-record files that carry the id;
  (3) later rulings whose text names the id with an enactment verb.
Verdicts proposed here: ENACTED (stampable: positive clause in a commit dated on/after the ruling that
ALSO touched one of the ruling's `governs` paths), UNCERTAIN (some receipt, not that strong), NOT-FOUND.
The proposal is a machine reading; stamping is gated on a hand read (review.py / decisions.json).
Usage: python3 audit.py /tmp/r2/commits.json /tmp/r2/treelines.txt out.json
"""
import json, re, sys, fnmatch, collections

REPO_RULINGS = 'knowledge/_rulings.json'
RECORD_PREFIX = ('notes/', 'reviews/', '_DECISION-HISTORY/', 'dashboard/', 'dashboards/', 'knowledge/_tmp/',
                 'designer-skills-v2/', 'designer-skills-v1/', 'archive/', '_retired/', '_review/', 'runs/')
RECORD_FILES = {'knowledge/_rulings.json', 'knowledge/_state.json', 'knowledge/_memento-index.json',
                'knowledge/_kg_history.json', 'knowledge/_REVIEW-SIGNOFF.md', 'knowledge/_GOVERNING-RECORDS.md',
                'knowledge/_mention-map.json', 'knowledge/_ruling_edges.json', 'knowledge/_CAPTURE-GATE.md'}
def is_record(f):
    if f in RECORD_FILES or f.startswith(RECORD_PREFIX): return True
    if '/' not in f and f.startswith('_') and f.endswith(('.md', '.html')): return True   # root ledgers, handoffs, chain, GM
    if f in ('GOOD-MORNING.md', 'README.md', 'AGENTS.md', 'MODEL-ROUTING.md'): return True
    return False

ID_RE = re.compile(r'(?<![\w-])(s\d{2,3})-D(\d+)(?![\d])')
# continuation after an id: range (..|…|–|-|to) D?n  or list (/|,|&|and) D n
CONT_RE = re.compile(r'\s*(\.\.\.?|…|–|—|-|to|/|,|&|and)\s*D?(\d+)(?![\d])')
POS = re.compile(r'\b(enacted|implemented|built|landed|lands|wired|minted|shipped|in code|discharged|'
                 r'stamped enacted|re-?based|executed|applied|enacts)\b', re.I)
NEG = re.compile(r'\b(not|un-?enacted|unbuilt|never|yet|owed|pending|queued|deferred|awaits?|awaiting|'
                 r'until|once|if|would|will|to be|next|rolls?|carried|carry|still|remains?|refused|'
                 r'proposed|draft|unproven|half)\b', re.I)

def expand(text):
    """Yield (id, start, end) for every ruling id named in text, ranges and lists expanded."""
    for m in ID_RE.finditer(text):
        pre, n = m.group(1), int(m.group(2))
        yield f'{pre}-D{n}', m.start(), m.end()
        pos, last = m.end(), n
        while True:
            c = CONT_RE.match(text, pos)
            if not c: break
            sep, k = c.group(1), int(c.group(2))
            # a bare '-' or ',' followed by a number that is not D-prefixed is ambiguous; require 'D' for those
            raw = text[c.start():c.end()]
            if sep in ('-', ',', 'and', '&') and 'D' not in raw: break
            if sep in ('..', '...', '…', '–', '—', 'to', '-') and k > last and k - last <= 120:
                for j in range(last + 1, k + 1): yield f'{pre}-D{j}', m.start(), c.end()
            else:
                yield f'{pre}-D{k}', m.start(), c.end()
            last, pos = k, c.end()

SPLIT = re.compile(r'(?<=[.;!?])\s+|\n+|\s+[—·|]\s+|\s+-\s+(?=[A-Z])')
def clauses(text):
    return [c.strip() for c in SPLIT.split(text) if c and c.strip()]

def classify(clause, rid):
    """POS / NEG / MENTION for one clause that names rid."""
    pv = list(POS.finditer(clause))
    if not pv: return 'MENTION'
    for v in pv:
        window = clause[max(0, v.start() - 60):v.start()]
        after = clause[v.end():v.end() + 12]
        if NEG.search(window) or re.match(r'\s*\?', after):
            continue
        return 'POS'
    return 'NEG'

def gmatch(f, governs):
    for g in governs:
        g = str(g).strip().split(' ')[0].split('#')[0].split(':')[0]
        if not g or '/' not in g and '.' not in g: continue
        if f == g or (g.endswith('/') and f.startswith(g)) or f.startswith(g.rstrip('/') + '/') or \
           (any(ch in g for ch in '*?[') and fnmatch.fnmatch(f, g)):
            return g
    return None

def main():
    commits = json.load(open(sys.argv[1]))
    treelines = sys.argv[2]
    rulings = json.load(open(REPO_RULINGS))['rulings']
    byid = {r['id']: r for r in rulings}
    order = {r['id']: i for i, r in enumerate(rulings)}

    def pop_class(r):
        s = r['status'].strip()
        if s.lower() == 'ruled': return 'bare'
        if re.search(r'not (yet )?(enacted|built)', s, re.I) and not s.upper().startswith('ENACTED'): return 'not-enacted-text'
        return None
    pop = {r['id']: pop_class(r) for r in rulings if pop_class(r)}

    # (1) commits
    hits = collections.defaultdict(list)
    for c in commits:
        text = (c['subject'] + '\n' + c['body'])
        if not ID_RE.search(text): continue
        for cl in clauses(text):
            ids = {i for i, _, _ in expand(cl)}
            for rid in ids & pop.keys():
                hits[rid].append((c, cl, classify(cl, rid)))
    # (2) tree lines at HEAD (non-record files)
    tree = collections.defaultdict(list)
    for line in open(treelines, encoding='utf-8', errors='replace'):
        parts = line.split(':', 3)
        if len(parts) < 4: continue
        _, f, ln, txt = parts
        if is_record(f): continue
        for rid, _, _ in expand(txt):
            if rid in pop: tree[rid].append((f, int(ln), txt.strip()[:240]))
    # (3) later rulings
    later = collections.defaultdict(list)
    for r in rulings:
        blob = ' '.join(str(r.get(k, '')) for k in ('ruled', 'says', 'status')) + ' ' + ' '.join(map(str, r.get('evidence') or []))
        for cl in clauses(blob):
            for rid in {i for i, _, _ in expand(cl)} & pop.keys():
                if rid == r['id']: continue
                later[rid].append((r['id'], cl[:300], classify(cl, rid)))

    out = []
    for rid, klass in pop.items():
        r = byid[rid]
        date = r.get('date', '')
        gov = r.get('governs') or []
        ch = []
        for c, cl, k in hits.get(rid, []):
            touched = sorted({g for g in (gmatch(f, gov) for f in c['files'] if not is_record(f)) if g})
            nonrec = [f for f in c['files'] if not is_record(f)]
            ch.append({'sha': c['sha'][:12], 'date': c['date'][:10], 'subject': c['subject'][:140], 'clause': cl[:400],
                       'kind': k, 'governs_touched': touched, 'nonrecord_files': len(nonrec),
                       'before_ruling': bool(date) and c['date'][:10] < date})
        strong = [h for h in ch if h['kind'] == 'POS' and h['governs_touched'] and not h['before_ruling']]
        posany = [h for h in ch if h['kind'] == 'POS' and not h['before_ruling']]
        negs = [h for h in ch if h['kind'] == 'NEG']
        th = tree.get(rid, [])
        th_gov = [t for t in th if gmatch(t[0], gov)]  # tree hits are already non-record
        lr = later.get(rid, [])
        if strong:
            v = 'ENACTED'
        elif posany or th_gov or any(k == 'POS' for _, _, k in lr) or th:
            v = 'UNCERTAIN'
        else:
            v = 'NOT-FOUND'
        out.append({'id': rid, 'population': klass, 'date': date, 'status': r['status'][:300],
                    'ruled': str(r.get('ruled', ''))[:300], 'governs': gov, 'proposed': v,
                    'strong': strong[:6], 'pos_other': [h for h in posany if h not in strong][:6],
                    'neg': negs[-4:], 'mentions': len(ch),
                    'tree': th[:8], 'tree_governs': th_gov[:8], 'tree_total': len(th),
                    'later_rulings': lr[:8]})
    out.sort(key=lambda o: order[o['id']])
    json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
    cnt = collections.Counter((o['population'], o['proposed']) for o in out)
    print(len(out), 'rulings in population'); [print(' ', k, n) for k, n in sorted(cnt.items())]

if __name__ == '__main__':
    main()
