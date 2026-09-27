# #304 C6 verify-and-commit seat - mint W-304w6 (W6's spec, verbatim) and W-304c6 (this seat, interim-report pattern),
# close W-304c5 (its final copy and transcripts ride the wave-six commit). Modelled on C5's mint_304c5.py.
import sys, os, json
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
W6 = S + '2026-09-27-304-W6-motion-fit-and-117.md'
C6 = S + '2026-09-27-304-C6-verify-and-commit-wave-six.md'
C5 = S + '2026-09-27-304-C5-commit-seat-wave-five.md'
def spec(path):
    for line in open(path):
        if line.startswith('{"id"'):
            return json.loads(line)
    raise SystemExit('no spec in ' + path)
KEEP = ('id','home','links','title','body','closes_when','owner','condition')
w6 = {k: v for k, v in spec(W6).items() if k in KEEP}
w6['body'] += (" Row minted by the C6 verify-and-commit seat, which re-measured before committing: c2r1 overview reduced motion "
               "HEAD 9/10 -> W6 0/10 unfitted (own probe), 0 viewBox writes after 1.5 s; Chart-combo 34,777/34,816; "
               "_LIVE-STATE.md diff = stamp + one row, byte-identical to W6's saved diff; fresh-clone chunks 31:70 71:100 101:127 "
               "0 differ from W6 by step, [117] green.")
c6 = dict(id='W-304c6', home=C6, owner='claude', condition='stated',
    links=['knowledge/canon/dv-behaviour.js', '_LIVE-STATE.md', 'notes/_lanes/304/C6/verify/'],
    title="#304 C6 - verify-and-commit seat, wave six: W6's reduced-motion fit fix and the [117] live-state row verified independently (probe, clone survey), then committed with C5's final copy, pushed, CI read back",
    body=("s218-D7 filed report, verify-and-commit seat, wave six (#304). Verify PASS: fit fix no loop/no thrash, one extra pass under "
          "reduced motion, none with motion, holder transitions cost one debounced pass, non-holders none; option (a) is dream pass 14's "
          "stamp + row carried by the 96c2f454/77a77eea precedent. The interim copy rides the wave-six commit; the final copy with the "
          "sha, the push range and CI verdict by job rides the next commit."),
    closes_when="the final copy of this report, carrying the sha, the push range and CI verdict by job, is committed")
doc = st.load()
have = {i['id']: i for i in doc['items']}
for r in (w6, c6):
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=304, state='open', **r)
    print('added', r['id'])
c5 = have['W-304c5']
if c5['state'] != 'done':
    c5['state'] = 'done'
    c5['closed_by'] = ("#304 C6 seat: the FINAL copy of notes/_subreports/2026-09-27-304-C5-commit-seat-wave-five.md (sha 52049781, "
                       "push 3100da99..52049781, CI run 36306939769 by job, the [117] cause) and its transcripts in notes/_lanes/304/C5/ "
                       "ride the wave-six commit, as the row's close condition says")
    print('closed W-304c5')
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
