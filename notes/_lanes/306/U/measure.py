# #306 U - the bloat check: today's boot-chain files and the #305 wrap's views, measured with the repo's gauge.
# count() returns (tokens, method); 'real' only on a content-hash cache hit or a reachable API, else 'cl100k-estimate'.
import sys, os, re, glob, json
sys.path.insert(0, 'knowledge')
import _gauge_tokens as g
import tiktoken
enc = tiktoken.get_encoding('cl100k_base')
def m(path, text=None):
    t = text if text is not None else open(path, encoding='utf-8').read()
    real, meth = g.count(t, allow_api=True, _cache_write=False)
    return dict(path=path, bytes=len(t.encode()), chars=len(t), cl100k=len(enc.encode(t)), gauge=real, method=meth)
out = {}
hs = sorted(glob.glob('_HANDOFF-*.md'), key=lambda p: int(re.match(r'_HANDOFF-(\d+)', p).group(1)))
out['handoffs_on_disk'] = len(hs)
out['newest_handoff'] = m(hs[-1])
out['chain'] = m('_CHAIN.md')
c = open('_CHAIN.md', encoding='utf-8').read()
i1 = c.find('## ⏱ LATEST DELTA'); i2 = c.find('## ⬛ OPEN WORK')
out['chain_part_head_and_banner'] = m('_CHAIN.md[0:delta]', c[:i1])
out['chain_part_ls_delta'] = m('_CHAIN.md[delta:openwork]', c[i1:i2])
out['chain_part_open_work_and_tail'] = m('_CHAIN.md[openwork:]', c[i2:])
# handoff trend (archived ones too)
arch = sorted(set(glob.glob('notes/_handoffs/_HANDOFF-*.md') + glob.glob('**/_HANDOFF-*.md', recursive=True)))
series = {}
for p in arch:
    mm = re.search(r'_HANDOFF-(\d+)', os.path.basename(p))
    if mm and '/_lanes/' not in p: series.setdefault(int(mm.group(1)), p)
trend = []
for n in sorted(series)[-30:]:
    t = open(series[n], encoding='utf-8').read()
    trend.append((n, series[n], len(t.encode()), len(enc.encode(t))))
out['handoff_trend'] = trend
for f in ['GOOD-MORNING.md', '_LIVE-STATE.md', 'notes/_lanes/305/W/memory_body_305.md']:
    if os.path.exists(f): out[f] = m(f)
# the #305 wrap's three long narrations
for f in sorted(glob.glob('notes/_lanes/305/W/*')):
    pass
json.dump(out, open('notes/_lanes/306/U/measure.json', 'w'), indent=1, ensure_ascii=False)
for k, v in out.items():
    if k == 'handoff_trend':
        for r in v: print('  trend', r)
    else: print(k, v)
